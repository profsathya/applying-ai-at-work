"""Remove the legacy link beneath hosted Canvas iframes, without changing the iframe.

The default is a live, read-only inventory. --apply is for the protected
Publish Canvas workflow and updates the matching canvas-state fingerprints.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.schema import parse_frontmatter
from canvas_sync.state import (
    canvas_fingerprint, check_state_instance, fetch_canvas_state, load_json,
    save_json_atomic, state_path_for_manifest, utc_now,
)


LINK = re.compile(
    r'<p><a href="(?P<href>[^"]+)" target="(?:_blank|_top)">'
    r'Open hosted page in a new tab</a></p>'
)
IFRAME = re.compile(r'<iframe\b[^>]*\bsrc="(?P<src>[^"]+)"')
BODY_FIELD = {
    "assignment": "description",
    "page": "body",
    "discussion": "message",
    "quiz": "description",
}
REPO_ROOT = Path(__file__).resolve().parent.parent


def without_legacy_link(body: str) -> str | None:
    """Return the exact shell with only its trailing legacy link removed."""
    if "Open hosted page in a new tab" not in body:
        return None
    if not body.startswith('<div class="hosted-html-shell">') or not body.endswith("</div>"):
        raise ValueError("legacy link is outside a complete hosted iframe shell")
    links = list(LINK.finditer(body))
    frames = list(IFRAME.finditer(body))
    if len(links) != 1 or len(frames) != 1:
        raise ValueError("expected one legacy link and one hosted iframe")
    link, frame = links[0], frames[0]
    if html.unescape(link.group("href")) != html.unescape(frame.group("src")):
        raise ValueError("legacy link does not match the hosted iframe URL")
    if not body[:link.start()].endswith("</iframe>") or body[link.end():] != "</div>":
        raise ValueError("legacy link is not immediately below the hosted iframe")
    return body[:link.start()] + body[link.end():]


def identity(kind: str, row: dict) -> tuple[str, str]:
    return kind, str(row["url"] if kind == "page" else row["id"])


def state_index(state: dict) -> dict[tuple[str, str], tuple[str, dict]]:
    index = {}
    for artifact_id, entry in state.get("artifacts", {}).items():
        kind = entry.get("canvas_type")
        value = entry.get("canvas_page_url") if kind == "page" else entry.get("canvas_id")
        if kind not in BODY_FIELD or value is None:
            continue
        key = kind, str(value)
        if key in index:
            raise ValueError(f"duplicate canvas-state identity: {key}")
        index[key] = artifact_id, entry
    return index


def state_allows_cleanup(entry: dict, live: dict, kind: str) -> bool:
    expected = entry.get("canvas_fingerprint")
    if expected == canvas_fingerprint(live, kind):
        return True
    # Some retired V1 items were unpublished in Canvas after their last state
    # snapshot. Accept that single known drift only when local MD agrees.
    if not isinstance(live.get("published"), bool):
        return False
    prior = {**live, "published": not live["published"]}
    if expected != canvas_fingerprint(prior, kind):
        return False
    local_path = entry.get("local_path")
    if not local_path:
        return False
    frontmatter, _ = parse_frontmatter(REPO_ROOT / local_path)
    return frontmatter.get("publish", True) == live["published"]


def inventory(client: CanvasClient) -> list[tuple[str, dict]]:
    rows = []
    for kind, endpoint in (
        ("assignment", "assignments"), ("page", "pages"),
        ("discussion", "discussion_topics"), ("quiz", "quizzes"),
    ):
        for row in client._request_paginated("GET", endpoint):
            if kind == "page":
                row = client.get_page(row["url"])
            rows.append((kind, row))
    return rows


def current(client: CanvasClient, kind: str, row: dict, entry: dict | None) -> dict:
    if entry is not None:
        live = fetch_canvas_state(client, entry)
        if live is None:
            raise ValueError("state-backed Canvas item is missing")
        return live
    if kind == "assignment":
        return client.get_assignment(row["id"])
    if kind == "page":
        return client.get_page(row["url"])
    if kind == "discussion":
        return client.get_discussion(row["id"])
    return client.get_quiz(row["id"])


def update(client: CanvasClient, kind: str, row: dict, body: str) -> None:
    if kind == "assignment":
        client.update_assignment(row["id"], {"description": body, "notify_of_update": False})
    elif kind == "page":
        client.update_page(row["url"], {"body": body})
    elif kind == "discussion":
        client.update_discussion(row["id"], {"message": body})
    else:
        client.update_quiz(row["id"], {"description": body, "notify_of_update": False})


def cleanup(manifest_path: Path, state_dir: Path, *, apply: bool) -> dict:
    manifest = load_json(manifest_path)
    state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
    state = load_json(state_path)
    check_state_instance(state, manifest, state_path)
    check_instance_ready(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = CanvasClient.from_env(course_id=int(manifest["instance"]["course_id"]))
    indexed = state_index(state)
    result = {
        "manifest": str(manifest_path), "state": str(state_path),
        "changed": [], "published": [], "failed": [], "drifted": [],
        "provisional": [], "hosted": None, "hosted_restored": [],
    }
    planned = []
    for kind, row in inventory(client):
        key = identity(kind, row)
        mapped = indexed.get(key)
        entry = mapped[1] if mapped else None
        field = BODY_FIELD[kind]
        if "Open hosted page in a new tab" not in (row.get(field) or ""):
            continue
        label = (entry or {}).get("local_path") or f"{kind}:{key[1]}"
        try:
            live = current(client, kind, row, entry)
            revised = without_legacy_link(live.get(field) or "")
            if revised is None:
                continue
            if entry and not state_allows_cleanup(entry, live, kind):
                raise ValueError("Canvas item differs from its state-backed fingerprint")
            planned.append((kind, row, live, revised, mapped, label))
            result["changed"].append({"file": label, "artifact_id": mapped[0] if mapped else None})
        except Exception as exc:  # preflight all targets before any write
            result["failed"].append({"file": label, "artifact_id": mapped[0] if mapped else None,
                                     "error": str(exc).splitlines()[0]})
    if result["failed"] or not apply:
        return result
    for kind, row, before, revised, mapped, label in planned:
        artifact_id, entry = mapped if mapped else (None, None)
        try:
            # Refuse a concurrent Canvas edit after preflight.
            latest = current(client, kind, row, entry)
            if canvas_fingerprint(latest, kind) != canvas_fingerprint(before, kind):
                raise ValueError("Canvas item changed during cleanup")
            update(client, kind, row, revised)
            after = current(client, kind, row, entry)
            if after.get(BODY_FIELD[kind]) != revised:
                raise ValueError("Canvas did not retain the link-free iframe shell")
            if entry:
                entry["canvas_fingerprint"] = canvas_fingerprint(after, kind)
                state["last_sync"] = utc_now()
                save_json_atomic(state_path, state)
            result["published"].append({"action": "updated", "file": label,
                                        "artifact_id": artifact_id,
                                        "canvas_id": row.get("id"),
                                        "canvas_page_url": row.get("url") if kind == "page" else None})
        except Exception as exc:
            result["failed"].append({"file": label, "artifact_id": artifact_id,
                                     "error": str(exc).splitlines()[0]})
    return result


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report-file", type=Path)
    args = parser.parse_args()
    result = cleanup(args.manifest.resolve(), args.state_dir.resolve(), apply=args.apply)
    report = {"results": [result], "completed": True}
    if args.report_file:
        args.report_file.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"matched": len(result["changed"]), "updated": len(result["published"]),
                      "failed": result["failed"], "apply": args.apply}, indent=2))
    return 1 if result["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

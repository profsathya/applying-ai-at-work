"""
Pull canvas state back into local MD files (drift reconciliation).

Usage:
  python canvas_sync/pull.py --manifest <path> --dry-run
  python canvas_sync/pull.py --manifest <path> --apply

Dry-run prints a diff report. Apply overwrites MD bodies where canvas has
newer content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_enabled
from canvas_sync.schema import parse_frontmatter


def html_to_markdown(html: str) -> str:
    """Convert canvas HTML back to markdown. Uses html2text with safe config."""
    try:
        import html2text
    except ImportError:
        raise RuntimeError("html2text required for --apply mode. pip install html2text")

    h = html2text.HTML2Text()
    h.body_width = 0  # no wrapping
    h.unicode_snob = True
    h.ignore_links = False
    h.ignore_images = False
    h.escape_snob = True
    return h.handle(html or "").strip()


def fetch_canvas_state(client: CanvasClient, artifact_entry: dict) -> dict | None:
    """Fetch current canvas state for an artifact. Returns None if orphaned."""
    atype = artifact_entry.get("canvas_type")
    cid = artifact_entry.get("canvas_id")
    page_url = artifact_entry.get("canvas_page_url")

    try:
        if atype == "assignment":
            return client.get_assignment(cid)
        if atype == "page":
            return client.get_page(page_url)
        if atype == "discussion":
            return client.get_discussion(cid)
        if atype == "quiz":
            return client.get_quiz(cid)
        return None
    except CanvasError as e:
        if e.status == 404:
            return None
        raise


def compute_drift(md_path: Path, canvas_state: dict, atype: str) -> dict:
    """Return a dict describing what differs between MD and canvas."""
    fm, body = parse_frontmatter(md_path)

    canvas_title = canvas_state.get("name") or canvas_state.get("title")
    canvas_body_html = (
        canvas_state.get("description")
        or canvas_state.get("body")
        or canvas_state.get("message")
        or ""
    )
    canvas_body_md = html_to_markdown(canvas_body_html)

    drift = {}
    if canvas_title != fm.get("title"):
        drift["title"] = {"local": fm.get("title"), "canvas": canvas_title}

    local_body_normalized = body.strip()
    canvas_body_normalized = canvas_body_md.strip()
    if local_body_normalized != canvas_body_normalized:
        drift["body"] = {
            "local_chars": len(local_body_normalized),
            "canvas_chars": len(canvas_body_normalized),
            "local_preview": local_body_normalized[:200],
            "canvas_preview": canvas_body_normalized[:200],
        }

    if atype in ("assignment", "quiz", "discussion"):
        canvas_points = canvas_state.get("points_possible")
        if canvas_state.get("assignment"):
            canvas_points = canvas_state["assignment"].get("points_possible", canvas_points)
        if canvas_points != fm.get("points"):
            drift["points"] = {"local": fm.get("points"), "canvas": canvas_points}

    return drift


def apply_drift(md_path: Path, canvas_state: dict, atype: str) -> None:
    fm, _old_body = parse_frontmatter(md_path)

    canvas_title = canvas_state.get("name") or canvas_state.get("title")
    canvas_body_html = (
        canvas_state.get("description")
        or canvas_state.get("body")
        or canvas_state.get("message")
        or ""
    )
    new_body = html_to_markdown(canvas_body_html)

    if canvas_title:
        fm["title"] = canvas_title

    if atype in ("assignment", "quiz", "discussion"):
        canvas_points = canvas_state.get("points_possible")
        if canvas_state.get("assignment"):
            canvas_points = canvas_state["assignment"].get("points_possible", canvas_points)
        if canvas_points is not None:
            fm["points"] = canvas_points

    # Rewrite the file preserving frontmatter order
    import yaml

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(fm, f, sort_keys=False, allow_unicode=True)
        f.write("---\n\n")
        f.write(new_body.rstrip() + "\n")


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--dry-run", action="store_true")
    mode_group.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    with open(args.manifest) as f:
        manifest = json.load(f)

    check_instance_enabled(manifest, manifest_label=str(args.manifest))
    check_env_matches_instance(manifest, manifest_label=str(args.manifest))
    client = CanvasClient.from_env(course_id=manifest["instance"]["course_id"])

    drift_report: list[dict] = []
    orphans: list[str] = []

    for rel_path, entry in manifest.get("artifacts", {}).items():
        md_path = Path(rel_path)
        if not md_path.exists():
            print(f"WARN: MD file missing locally: {rel_path}", file=sys.stderr)
            continue

        canvas_state = fetch_canvas_state(client, entry)
        if canvas_state is None:
            orphans.append(rel_path)
            continue

        drift = compute_drift(md_path, canvas_state, entry["canvas_type"])
        if drift:
            drift_report.append({"file": rel_path, "drift": drift})

        if args.apply and drift:
            apply_drift(md_path, canvas_state, entry["canvas_type"])

    print(json.dumps({
        "mode": "apply" if args.apply else "dry-run",
        "total_artifacts": len(manifest.get("artifacts", {})),
        "drifted": len(drift_report),
        "orphans": orphans,
        "report": drift_report,
    }, indent=2))

    if args.apply:
        # Mark orphans in manifest
        for orphan in orphans:
            manifest["artifacts"][orphan]["orphaned"] = True
        manifest["last_sync"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        with open(args.manifest, "w") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)
            f.write("\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

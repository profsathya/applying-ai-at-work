"""Hydrate external deployment state with live Canvas fingerprints."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.inspect_canvas import compute_inspection_drift
from canvas_sync.hosted_html import artifact_hosted_info, iframe_shell
from canvas_sync.pull import html_to_markdown
from canvas_sync.schema import parse_frontmatter, validate_canvas_state
from canvas_sync.state import (
    canvas_fingerprint,
    content_hash,
    fetch_canvas_state,
    load_json,
    save_json_atomic,
    state_path_for_manifest,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_manifests() -> list[Path]:
    return sorted(REPO_ROOT.glob("course*/manifests/production.json"))


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def hosted_canvas_drift(
    md_path: Path,
    manifest_path: Path,
    manifest: dict,
    canvas_state: dict,
    atype: str,
) -> dict:
    """Compare live Canvas state with the hosted iframe shell expected for this artifact."""
    fm, _body = parse_frontmatter(md_path)
    hosted_info = artifact_hosted_info(md_path, manifest_path, manifest, fm)
    if not hosted_info["enabled"]:
        return compute_inspection_drift(md_path, canvas_state, atype)

    canvas_title = canvas_state.get("name") or canvas_state.get("title")
    canvas_body_html = (
        canvas_state.get("description")
        or canvas_state.get("body")
        or canvas_state.get("message")
        or ""
    )
    canvas_body_md = html_to_markdown(canvas_body_html).strip()
    expected_body_md = html_to_markdown(iframe_shell(hosted_info["hosted_url"], fm["title"])).strip()

    drift: dict[str, object] = {}
    if canvas_title != fm.get("title"):
        drift["title"] = {"local": fm.get("title"), "canvas": canvas_title}
    if expected_body_md != canvas_body_md:
        drift["body"] = {
            "expected_chars": len(expected_body_md),
            "canvas_chars": len(canvas_body_md),
            "expected_preview": expected_body_md[:200],
            "canvas_preview": canvas_body_md[:200],
        }
    if atype in ("assignment", "quiz", "discussion"):
        canvas_points = canvas_state.get("points_possible")
        if canvas_state.get("assignment"):
            canvas_points = canvas_state["assignment"].get("points_possible", canvas_points)
        if canvas_points != fm.get("points"):
            drift["points"] = {"local": fm.get("points"), "canvas": canvas_points}
    return drift


def hydrate_manifest(manifest_path: Path, state_dir: Path) -> dict:
    manifest = load_json(manifest_path)
    state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
    result = {
        "manifest": repo_relative(manifest_path),
        "state": str(state_path),
        "hydrated": [],
        "skipped": [],
        "failed": [],
    }
    if not state_path.exists():
        result["failed"].append({"reason": "state file is missing"})
        return result

    state = load_json(state_path)
    client = CanvasClient.from_env(course_id=int(manifest["instance"]["course_id"]))
    changed = False

    for artifact_id, entry in sorted(state.get("artifacts", {}).items()):
        rel_path = entry.get("local_path")
        atype = entry.get("canvas_type")
        if atype == "module_header":
            continue
        if entry.get("canvas_fingerprint"):
            continue
        md_path = REPO_ROOT / rel_path if rel_path else None
        if not md_path or not md_path.exists():
            result["failed"].append(
                {"artifact_id": artifact_id, "file": rel_path, "reason": "local file is missing"}
            )
            continue
        if entry.get("content_hash") != content_hash(md_path):
            result["skipped"].append(
                {
                    "artifact_id": artifact_id,
                    "file": rel_path,
                    "reason": "local content differs from deployment state",
                }
            )
            continue

        live_state = fetch_canvas_state(client, entry)
        if live_state is None:
            result["failed"].append(
                {"artifact_id": artifact_id, "file": rel_path, "reason": "canvas object is missing"}
            )
            continue
        drift = hosted_canvas_drift(md_path, manifest_path, manifest, live_state, atype)
        if drift:
            result["failed"].append(
                {
                    "artifact_id": artifact_id,
                    "file": rel_path,
                    "reason": "canvas differs from expected hosted shell"
                    if manifest.get("hosted_html", {}).get("enabled")
                    else "canvas differs from local markdown",
                    "drift": drift,
                }
            )
            continue

        fingerprint = canvas_fingerprint(live_state, atype)
        if fingerprint:
            entry["canvas_fingerprint"] = fingerprint
            result["hydrated"].append({"artifact_id": artifact_id, "file": rel_path})
            changed = True

    if changed:
        save_json_atomic(state_path, state)
        errors = validate_canvas_state(state_path)
        if errors:
            result["failed"].append({"reason": "state validation failed", "errors": errors})
    return result


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--manifest", action="append", type=Path)
    group.add_argument("--all-manifests", action="store_true")
    parser.add_argument("--state-dir", type=Path, required=True)
    args = parser.parse_args()

    manifests = args.manifest if args.manifest else discover_manifests()
    results = []
    failed = False
    try:
        for manifest in manifests:
            result = hydrate_manifest(manifest.resolve(), args.state_dir.resolve())
            results.append(result)
            if result["failed"]:
                failed = True
    except Exception as exc:  # noqa: BLE001 - CLI should return a compact failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"results": results}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

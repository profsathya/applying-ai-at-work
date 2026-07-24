"""Publish changed Markdown artifacts using external Canvas deployment state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance
from canvas_sync.hosted_html import render_hosted_files
from canvas_sync.push import push_artifact
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import (
    content_hash,
    empty_state_from_manifest,
    fetch_canvas_state,
    canvas_fingerprint,
    load_json,
    state_path_for_manifest,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_manifests() -> list[Path]:
    return sorted(REPO_ROOT.glob("course*/manifests/production.json"))


def discover_artifact_files(manifest_path: Path) -> list[Path]:
    course_dir = manifest_path.parent.parent
    return sorted(course_dir.glob("sprints/sprint-*/*.md"))


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def load_state(manifest_path: Path, state_dir: Path, *, require_state: bool) -> tuple[dict, Path]:
    manifest = load_json(manifest_path)
    state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
    if state_path.exists():
        return load_json(state_path), state_path
    if require_state:
        raise FileNotFoundError(
            f"State file not found for {repo_relative(manifest_path)}: {state_path}. "
            "Run canvas_sync/bootstrap_state.py first."
        )
    return empty_state_from_manifest(manifest), state_path


def changed_artifacts(manifest_path: Path, state_dir: Path, *, require_state: bool) -> tuple[list[dict], dict]:
    state, state_path = load_state(manifest_path, state_dir, require_state=require_state)
    changed: list[dict] = []
    for md_path in discover_artifact_files(manifest_path):
        errors = validate_artifact(md_path)
        if errors:
            raise ValueError("; ".join(errors))
        frontmatter, _ = parse_frontmatter(md_path)
        artifact_id = frontmatter["artifact_id"]
        state_entry = state.get("artifacts", {}).get(artifact_id)
        hash_value = content_hash(md_path)
        if not state_entry or state_entry.get("content_hash") != hash_value:
            changed.append(
                {
                    "file": repo_relative(md_path),
                    "path": md_path,
                    "artifact_id": artifact_id,
                    "state_entry": state_entry,
                    "content_hash": hash_value,
                }
            )
    return changed, {"state": state, "state_path": state_path}


def drift_for_changed(manifest_path: Path, changed: list[dict]) -> list[dict]:
    manifest = load_json(manifest_path)
    course_id = int(manifest["instance"]["course_id"])
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = CanvasClient.from_env(course_id=course_id)
    drifted: list[dict] = []

    for item in changed:
        entry = item.get("state_entry") or {}
        if not entry or entry.get("canvas_type") == "module_header":
            continue
        expected = entry.get("canvas_fingerprint")
        if not expected:
            drifted.append(
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "reason": "state entry is missing canvas_fingerprint; run hydrate_state before publishing changes",
                }
            )
            continue
        live_state = fetch_canvas_state(client, entry)
        if live_state is None:
            drifted.append(
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "reason": "canvas object is missing",
                }
            )
            continue
        actual = canvas_fingerprint(live_state, entry["canvas_type"])
        if actual != expected:
            drifted.append(
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "reason": "canvas changed since last state-backed publish",
                    "expected_fingerprint": expected,
                    "actual_fingerprint": actual,
                }
            )
    return drifted


def publish_manifest(
    manifest_path: Path,
    state_dir: Path,
    *,
    dry_run: bool,
    check_drift: bool,
    require_state: bool,
    hosted_output_dir: Path | None = None,
    hosted_only: bool = False,
) -> dict:
    manifest = load_json(manifest_path)
    hosted_only = hosted_only or manifest.get("canvas_publish") is False
    changed, state_info = changed_artifacts(
        manifest_path,
        state_dir,
        require_state=require_state,
    )
    result: dict = {
        "manifest": repo_relative(manifest_path),
        "state": str(state_info["state_path"]),
        "changed": [
            {"file": item["file"], "artifact_id": item["artifact_id"]}
            for item in changed
        ],
        "published": [],
        "failed": [],
        "drifted": [],
        "hosted": None,
    }
    if hosted_only:
        if dry_run:
            return result
        if not hosted_output_dir:
            result["failed"].append(
                {
                    "file": "<hosted_html>",
                    "artifact_id": None,
                    "error": "--hosted-only requires --hosted-output-dir",
                }
            )
            return result
        try:
            result["hosted"] = render_hosted_files(
                manifest_path,
                hosted_output_dir,
                discover_artifact_files(manifest_path),
                state=state_info["state"],
            )
        except Exception as exc:  # noqa: BLE001 - surface hosted render failures in publish result
            result["failed"].append(
                {
                    "file": "<hosted_html>",
                    "artifact_id": None,
                    "error": str(exc),
                }
            )
        return result
    if dry_run:
        return result
    if not changed:
        if hosted_output_dir:
            try:
                result["hosted"] = render_hosted_files(
                    manifest_path,
                    hosted_output_dir,
                    discover_artifact_files(manifest_path),
                    state=state_info["state"],
                )
            except Exception as exc:  # noqa: BLE001 - surface hosted render failures in publish result
                result["failed"].append(
                    {
                        "file": "<hosted_html>",
                        "artifact_id": None,
                        "error": str(exc),
                    }
                )
        return result

    if check_drift:
        drifted = drift_for_changed(manifest_path, changed)
        result["drifted"] = drifted
        if drifted:
            return result

    for item in changed:
        try:
            kwargs = {"state_dir": state_dir}
            if hosted_output_dir:
                kwargs["hosted_output_dir"] = hosted_output_dir
            pushed = push_artifact(item["path"], manifest_path, **kwargs)
            result["published"].append(pushed)
        except Exception as exc:  # noqa: BLE001 - continue so partial success is visible
            result["failed"].append(
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "error": str(exc),
                }
            )
    if hosted_output_dir and result["published"]:
        try:
            latest_state, _state_path = load_state(manifest_path, state_dir, require_state=True)
            result["hosted"] = render_hosted_files(
                manifest_path,
                hosted_output_dir,
                discover_artifact_files(manifest_path),
                state=latest_state,
            )
        except Exception as exc:  # noqa: BLE001 - surface hosted render failures in publish result
            result["failed"].append(
                {
                    "file": "<hosted_html>",
                    "artifact_id": None,
                    "error": str(exc),
                }
            )
    return result


def main() -> int:
    load_dotenv()
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--manifest", action="append", type=Path)
    group.add_argument("--all-manifests", action="store_true")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--check-drift", action="store_true")
    parser.add_argument("--require-state", action="store_true")
    parser.add_argument("--hosted-output-dir", type=Path)
    parser.add_argument(
        "--hosted-only",
        action="store_true",
        help="Render hosted HTML from Markdown and state without Canvas reads or writes.",
    )
    args = parser.parse_args()
    if args.hosted_only and not args.hosted_output_dir:
        parser.error("--hosted-only requires --hosted-output-dir")

    manifests = args.manifest if args.manifest else discover_manifests()
    results = []
    hard_failure = False
    try:
        for manifest in manifests:
            result = publish_manifest(
                manifest.resolve(),
                args.state_dir.resolve(),
                dry_run=args.dry_run,
                check_drift=args.check_drift,
                require_state=args.require_state,
                hosted_output_dir=args.hosted_output_dir.resolve() if args.hosted_output_dir else None,
                hosted_only=args.hosted_only,
            )
            results.append(result)
            if result["failed"] or result["drifted"]:
                hard_failure = True
    except Exception as exc:  # noqa: BLE001 - CLI should return a compact failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"results": results}, indent=2))
    return 1 if hard_failure else 0


if __name__ == "__main__":
    sys.exit(main())

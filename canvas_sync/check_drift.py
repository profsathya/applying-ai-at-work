"""Check live Canvas objects against external deployment state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.state import (
    canvas_fingerprint,
    content_hash,
    fetch_canvas_state,
    load_json,
    state_path_for_manifest,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_manifests() -> list[Path]:
    return sorted(REPO_ROOT.glob("course*/manifests/production.json"))


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def check_manifest(manifest_path: Path, state_dir: Path) -> dict:
    manifest = load_json(manifest_path)
    state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
    result = {
        "manifest": repo_relative(manifest_path),
        "state": str(state_path),
        "canvas_drift": [],
        "orphans": [],
        "missing_local_files": [],
        "missing_fingerprints": [],
        "unpushed_local_changes": [],
        "skipped": [],
    }

    if not state_path.exists():
        result["skipped"].append("state file is missing")
        return result

    state = load_json(state_path)
    check_instance_ready(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = CanvasClient.from_env(course_id=int(manifest["instance"]["course_id"]))
    for artifact_id, entry in sorted(state.get("artifacts", {}).items()):
        rel_path = entry.get("local_path")
        md_path = REPO_ROOT / rel_path if rel_path else None
        if md_path and md_path.exists():
            current_hash = content_hash(md_path)
            if current_hash != entry.get("content_hash"):
                result["unpushed_local_changes"].append(
                    {
                        "artifact_id": artifact_id,
                        "file": rel_path,
                        "state_hash": entry.get("content_hash"),
                        "local_hash": current_hash,
                    }
                )
        else:
            result["missing_local_files"].append(
                {"artifact_id": artifact_id, "file": rel_path}
            )

        if entry.get("canvas_type") == "module_header":
            continue
        expected = entry.get("canvas_fingerprint")
        if not expected:
            result["missing_fingerprints"].append(
                {
                    "artifact_id": artifact_id,
                    "file": rel_path,
                    "reason": "missing canvas_fingerprint",
                }
            )
            continue
        live_state = fetch_canvas_state(client, entry)
        if live_state is None:
            result["orphans"].append({"artifact_id": artifact_id, "file": rel_path})
            continue
        actual = canvas_fingerprint(live_state, entry["canvas_type"])
        if actual != expected:
            result["canvas_drift"].append(
                {
                    "artifact_id": artifact_id,
                    "file": rel_path,
                    "expected_fingerprint": expected,
                    "actual_fingerprint": actual,
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
    args = parser.parse_args()

    manifests = args.manifest if args.manifest else discover_manifests()
    results = []
    failed = False
    try:
        for manifest in manifests:
            result = check_manifest(manifest.resolve(), args.state_dir.resolve())
            results.append(result)
            if (
                result["canvas_drift"]
                or result["orphans"]
                or result["missing_local_files"]
                or result["missing_fingerprints"]
                or result["unpushed_local_changes"]
            ):
                failed = True
    except Exception as exc:  # noqa: BLE001 - CLI should return a compact failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"results": results}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

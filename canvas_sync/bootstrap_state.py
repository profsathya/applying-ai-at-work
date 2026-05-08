"""Bootstrap external Canvas deployment state from legacy manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.schema import validate_canvas_state
from canvas_sync.state import save_json_atomic, state_from_manifest, state_path_for_manifest


REPO_ROOT = Path(__file__).resolve().parent.parent


def discover_manifests() -> list[Path]:
    return sorted(REPO_ROOT.glob("course*/manifests/production.json"))


def bootstrap_manifest(manifest_path: Path, state_dir: Path, *, skip_existing: bool) -> dict:
    manifest_path = manifest_path.resolve()
    state_dir = state_dir.resolve()
    state_path = state_path_for_manifest(manifest_path, state_dir)
    existed = state_path.exists()

    if skip_existing and existed:
        return {
            "manifest": str(manifest_path.relative_to(REPO_ROOT)),
            "state": str(state_path),
            "action": "skipped",
        }

    state = state_from_manifest(manifest_path, REPO_ROOT)
    save_json_atomic(state_path, state)
    errors = validate_canvas_state(state_path)
    if errors:
        raise ValueError("; ".join(errors))

    return {
        "manifest": str(manifest_path.relative_to(REPO_ROOT)),
        "state": str(state_path),
        "action": "written" if existed else "created",
        "artifacts": len(state.get("artifacts", {})),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--manifest", action="append", type=Path)
    group.add_argument("--all-manifests", action="store_true")
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--skip-existing", action="store_true")
    args = parser.parse_args()

    manifests = args.manifest if args.manifest else discover_manifests()
    results = []
    try:
        for manifest in manifests:
            results.append(
                bootstrap_manifest(
                    manifest,
                    args.state_dir,
                    skip_existing=args.skip_existing,
                )
            )
    except Exception as exc:  # noqa: BLE001 - CLI should return a compact failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps({"results": results}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

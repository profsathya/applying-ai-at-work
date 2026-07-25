"""Acknowledge a manually applied rubric change.

push.py does not publish rubrics to Canvas. When an artifact's rubric
frontmatter changes, every publish repeats a warning until the maintainer
applies the rubric in Canvas by hand and acknowledges it here, which records
the current rubric fingerprint in deployment state. Local files and state
only: this script makes no Canvas calls.

Usage:
  python canvas_sync/ack_rubric.py --artifact <artifact_id> \
    --manifest <course>/manifests/production.json [--state-dir <dir>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.push import rubric_fingerprint
from canvas_sync.schema import parse_frontmatter
from canvas_sync.state import CanvasStateStore, artifact_entry_key


REPO_ROOT = Path(__file__).resolve().parent.parent


class AckRubricError(ValueError):
    """Raised when the acknowledgment cannot be recorded safely."""


def find_artifact_file(manifest_path: Path, artifact_id: str) -> tuple[Path, dict]:
    course_dir = manifest_path.parent.parent
    for md_path in sorted(course_dir.glob("sprints/sprint-*/*.md")):
        try:
            fm, _body = parse_frontmatter(md_path)
        except Exception:  # noqa: BLE001 - unparseable files cannot match
            continue
        if fm.get("artifact_id") == artifact_id:
            return md_path, fm
    raise AckRubricError(
        f"No artifact with artifact_id {artifact_id!r} under {course_dir}/sprints/"
    )


def ack_rubric(
    artifact_id: str,
    manifest_path: Path,
    state_dir: Path | None = None,
    repo_root: Path | None = None,
) -> dict:
    repo_root = (repo_root or Path.cwd()).resolve()
    manifest_path = manifest_path.resolve()
    md_path, fm = find_artifact_file(manifest_path, artifact_id)
    rel_path = str(md_path.resolve().relative_to(repo_root))
    fingerprint = rubric_fingerprint(fm)

    store = CanvasStateStore(manifest_path=manifest_path, repo_root=repo_root, state_dir=state_dir)
    with store.locked() as (_manifest, deployment_state, state_path):
        artifacts = deployment_state.setdefault("artifacts", {})
        state_key = artifact_entry_key(fm, rel_path, external_state=store.external)
        entry = artifacts.get(state_key)
        if entry is None:
            raise AckRubricError(
                f"{artifact_id!r} has no deployment-state entry in {state_path}; "
                "publish the artifact before acknowledging its rubric"
            )
        previous = entry.get("rubric_hash")
        entry["rubric_hash"] = fingerprint
        store.save(deployment_state, state_path)

    return {
        "artifact_id": artifact_id,
        "file": rel_path,
        "state_path": str(state_path),
        "previous_rubric_hash": previous,
        "rubric_hash": fingerprint,
        "note": "rubric acknowledged; the publish warning stops until the rubric changes again",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", required=True, help="artifact_id from frontmatter")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--state-dir",
        type=Path,
        help="External deployment-state checkout, for example a canvas-state worktree.",
    )
    args = parser.parse_args()

    try:
        summary = ack_rubric(args.artifact, args.manifest, state_dir=args.state_dir)
    except AckRubricError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

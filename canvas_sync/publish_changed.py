"""Publish changed Markdown artifacts using external Canvas deployment state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_enabled
from canvas_sync.hosted_html import (
    SHARED_OUTPUT_NAMES,
    artifact_hosted_output_paths,
    course_shared_output_dir,
    render_hosted_files,
)
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
    invalid: list[dict] = []
    for md_path in discover_artifact_files(manifest_path):
        errors = validate_artifact(md_path)
        if errors:
            # A validation error in one artifact must not abort the others:
            # record it as that item's failure and keep scanning.
            artifact_id = None
            try:
                frontmatter, _ = parse_frontmatter(md_path)
                artifact_id = frontmatter.get("artifact_id")
            except Exception:  # noqa: BLE001 - unparseable frontmatter has no id
                pass
            invalid.append(
                {
                    "file": repo_relative(md_path),
                    "artifact_id": artifact_id,
                    "error": "; ".join(errors),
                }
            )
            continue
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
    return changed, {"state": state, "state_path": state_path, "invalid": invalid}


def drift_for_changed(manifest_path: Path, changed: list[dict]) -> list[dict]:
    manifest = load_json(manifest_path)
    course_id = int(manifest["instance"]["course_id"])
    check_instance_enabled(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = CanvasClient.from_env(course_id=course_id)
    drifted: list[dict] = []

    for item in changed:
        entry = item.get("state_entry") or {}
        if not entry or entry.get("canvas_type") == "module_header":
            continue
        if not (entry.get("canvas_id") or entry.get("canvas_page_url")):
            # The item was never created in Canvas (state entry has no Canvas
            # identity). This is a first-time publish, not drift: let the
            # create path run.
            item["first_publish"] = True
            continue
        expected = entry.get("canvas_fingerprint")
        try:
            live_state = fetch_canvas_state(client, entry)
        except Exception as exc:  # noqa: BLE001 - block only the item that could not be assessed
            drifted.append(
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "reason": f"drift check failed: {str(exc).splitlines()[0]}",
                }
            )
            continue
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
        if not expected:
            # Incomplete state, not drift: hydrate the fingerprint from live
            # Canvas as part of publish instead of hard-stopping the run. The
            # push records a fresh fingerprint after it lands.
            item["healed_fingerprint"] = actual
            continue
        if actual != expected:
            # Real drift: a stored fingerprint exists and live Canvas does not
            # match it. Refuse so Canvas-side edits are not silently replaced.
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


def snapshot_hosted_outputs(
    manifest_path: Path,
    manifest: dict,
    hosted_output_dir: Path,
    changed: list[dict],
) -> dict[str, list[tuple[Path, bytes | None]]]:
    """Baseline content of every changed artifact's hosted output files.

    Captured before any push so a blocked or failed artifact's hosted files
    can be restored afterward: renders regenerate the whole course, and a
    refused publish must never change what that artifact's Canvas iframe
    shows.
    """
    snapshots: dict[str, list[tuple[Path, bytes | None]]] = {}
    for item in changed:
        entries: list[tuple[Path, bytes | None]] = []
        for path in artifact_hosted_output_paths(
            item["path"], manifest_path, hosted_output_dir, manifest=manifest
        ):
            entries.append((path, path.read_bytes() if path.exists() else None))
        snapshots[item["artifact_id"]] = entries
    return snapshots


def snapshot_shared_outputs(
    manifest_path: Path,
    manifest: dict,
    hosted_output_dir: Path,
) -> dict[Path, bytes | None]:
    """Baseline of the course's shared hosted index files.

    Homepages, sprint indexes, and the progress map are rebuilt from every
    artifact's CURRENT Markdown, so a blocked artifact's new title, module,
    position, or homepage metadata would otherwise leak into them while its
    own page stays at baseline.
    """
    course_out = course_shared_output_dir(manifest_path, hosted_output_dir, manifest=manifest)
    snapshots: dict[Path, bytes | None] = {}
    for name in SHARED_OUTPUT_NAMES:
        path = course_out / name
        snapshots[path] = path.read_bytes() if path.exists() else None
    for path in sorted(course_out.glob("sprint-*.html")):
        snapshots[path] = path.read_bytes()
    return snapshots


def restore_shared_outputs(
    snapshots: dict[Path, bytes | None],
    course_out_dir: Path,
) -> list[str]:
    """Put the shared index files back to baseline, dropping new sprint pages."""
    restored: list[str] = []
    for path, baseline in snapshots.items():
        current = path.read_bytes() if path.exists() else None
        if current == baseline:
            continue
        if baseline is None:
            path.unlink()
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(baseline)
        restored.append(str(path))
    for path in sorted(course_out_dir.glob("sprint-*.html")):
        if path not in snapshots:
            path.unlink()
            restored.append(str(path))
    return restored


def restore_hosted_outputs(
    snapshots: dict[str, list[tuple[Path, bytes | None]]],
    artifact_ids: set[str],
) -> list[str]:
    """Put unsuccessful artifacts' hosted files back to their baseline."""
    restored: list[str] = []
    for artifact_id in sorted(artifact_ids):
        for path, baseline in snapshots.get(artifact_id, []):
            current = path.read_bytes() if path.exists() else None
            if current == baseline:
                continue
            if baseline is None:
                path.unlink()
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(baseline)
            restored.append(str(path))
    return restored


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
        "failed": list(state_info.get("invalid", [])),
        "drifted": [],
        "healed": [],
        "hosted": None,
        "hosted_restored": [],
        "provisional": [],
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

    # Baseline every changed artifact's hosted output before anything renders,
    # so files belonging to blocked or failed artifacts can be restored below.
    hosted_snapshots: dict[str, list[tuple[Path, bytes | None]]] = {}
    shared_snapshots: dict[Path, bytes | None] = {}
    if hosted_output_dir and manifest.get("hosted_html", {}).get("enabled"):
        hosted_snapshots = snapshot_hosted_outputs(
            manifest_path, manifest, hosted_output_dir, changed
        )
        shared_snapshots = snapshot_shared_outputs(
            manifest_path, manifest, hosted_output_dir
        )

    # A drift refusal blocks only the drifted artifact, never its neighbors.
    # Healthy changed artifacts always publish; blocked ones are reported in
    # "drifted" and the CLI still exits nonzero after the rest went through.
    blocked_ids: set[str] = set()
    if check_drift:
        try:
            drifted = drift_for_changed(manifest_path, changed)
        except Exception as exc:  # noqa: BLE001 - degrade to blocking, not aborting
            # A manifest-wide scan failure (bad credentials, guard refusal,
            # network) blocks the artifacts it could not assess instead of
            # aborting the whole run; other manifests still process.
            reason = f"drift scan failed: {str(exc).splitlines()[0]}"
            drifted = [
                {
                    "file": item["file"],
                    "artifact_id": item["artifact_id"],
                    "reason": reason,
                }
                for item in changed
            ]
        result["drifted"] = drifted
        blocked_ids = {d["artifact_id"] for d in drifted}
        for item in changed:
            if item.get("healed_fingerprint"):
                result["healed"].append(
                    {
                        "file": item["file"],
                        "artifact_id": item["artifact_id"],
                        "reason": "hydrated missing canvas_fingerprint from live canvas during publish",
                    }
                )
            elif item.get("first_publish"):
                result["healed"].append(
                    {
                        "file": item["file"],
                        "artifact_id": item["artifact_id"],
                        "reason": "no canvas identity in state; treated as first-time publish",
                    }
                )

    for item in changed:
        if item["artifact_id"] in blocked_ids:
            continue
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
    # A push that failed AFTER creating its Canvas object saved a provisional
    # identity into state. Surface those items so the workflow commits the
    # state even when nothing else succeeded; discarding the identity would
    # make the retry create a duplicate Canvas object.
    failed_ids = {f["artifact_id"] for f in result["failed"] if f.get("artifact_id")}
    if failed_ids:
        try:
            post_state, _post_path = load_state(manifest_path, state_dir, require_state=False)
        except FileNotFoundError:
            post_state = {"artifacts": {}}
        pre_artifacts = state_info["state"].get("artifacts", {})
        post_artifacts = post_state.get("artifacts", {})
        for item in changed:
            artifact_id = item["artifact_id"]
            if artifact_id not in failed_ids:
                continue
            pre = pre_artifacts.get(artifact_id) or {}
            post = post_artifacts.get(artifact_id) or {}
            pre_identity = (pre.get("canvas_id"), pre.get("canvas_page_url"))
            post_identity = (post.get("canvas_id"), post.get("canvas_page_url"))
            if any(post_identity) and post_identity != pre_identity:
                result["provisional"].append(
                    {
                        "file": item["file"],
                        "artifact_id": artifact_id,
                        "reason": "canvas identity recorded before the failure; "
                        "state must be committed so the retry updates instead of duplicating",
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

    # Renders regenerate the whole course, so put unsuccessful artifacts'
    # hosted files back to their baseline: a refused or failed publish must
    # never change what that artifact's Canvas iframe shows.
    if hosted_snapshots:
        unsuccessful = {
            entry["artifact_id"]
            for entry in [*result["failed"], *result["drifted"]]
            if entry.get("artifact_id")
        }
        result["hosted_restored"] = restore_hosted_outputs(hosted_snapshots, unsuccessful)
        if unsuccessful and shared_snapshots:
            # Shared indexes are rebuilt from every artifact's current
            # Markdown, so with any blocked artifact in the course they are
            # held at baseline; healthy pages are live and the indexes catch
            # up on the next clean run.
            result["hosted_restored"].extend(
                restore_shared_outputs(
                    shared_snapshots,
                    course_shared_output_dir(
                        manifest_path, hosted_output_dir, manifest=manifest
                    ),
                )
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
    parser.add_argument(
        "--report-file",
        type=Path,
        help="Also write the JSON results report to this file, even on failure.",
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
        write_report(args.report_file, results)
        return 1

    write_report(args.report_file, results)
    print(json.dumps({"results": results}, indent=2))
    return 1 if hard_failure else 0


def write_report(report_file: Path | None, results: list[dict]) -> None:
    if not report_file:
        return
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(
        json.dumps({"results": results}, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    sys.exit(main())

"""Review and reconcile Canvas changes into validated local Markdown.

Use --state-dir for GitOps deployments. --apply requires the token from the
same dry run; changed source, state, or Canvas content invalidates that token.
Hosted wrappers are never imported as instructional source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from contextlib import nullcontext
from pathlib import Path

import yaml
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError
from canvas_sync.drift import canvas_body, compute_drift, html_to_markdown
from canvas_sync.hosted_html import artifact_hosted_info
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.maintenance_state import MaintenanceState
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import (
    canvas_fingerprint,
    content_hash,
    fetch_canvas_state,
    utc_now,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


def reconciled_text(md_path: Path, live: dict, drift: dict, *, hosted: bool) -> str:
    fm, body = parse_frontmatter(md_path)
    for field in ("title", "points", "publish", "due"):
        if field in drift:
            value = drift[field]["canvas"]
            if value is None:
                fm.pop(field, None)
            else:
                fm[field] = value
    if "body" in drift and not hosted:
        body = html_to_markdown(canvas_body(live))
    return (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
        + "---\n\n"
        + body.rstrip()
        + "\n"
    )


def validate_candidate(md_path: Path, text: str) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        candidate = Path(tmp) / md_path.name
        candidate.write_text(text, encoding="utf-8")
        return validate_artifact(candidate)


def reconcile(
    manifest_path: Path,
    *,
    state_dir: Path | None = None,
    apply: bool = False,
    confirm_token: str | None = None,
    files: list[str] | None = None,
    repo_root: Path = REPO_ROOT,
    client: CanvasClient | None = None,
) -> dict:
    store = MaintenanceState(manifest_path, repo_root, state_dir)
    with store.locked() if apply else nullcontext(store.load()) as manifest:
        check_instance_ready(manifest, manifest_label=str(manifest_path))
        check_env_matches_instance(manifest, manifest_label=str(manifest_path))
        client = client or CanvasClient.from_env(
            course_id=manifest["instance"]["course_id"]
        )
        artifacts = manifest.get("artifacts", {})
        selected = sorted(files if files is not None else artifacts)
        unknown = set(selected) - artifacts.keys()
        if unknown:
            raise ValueError(
                f"Files are not in the selected deployment state: {sorted(unknown)}"
            )
        report = {
            "mode": "apply" if apply else "dry-run",
            "state_path": str(store.path),
            "total_artifacts": len(selected),
            "report": [],
            "orphans": [],
            "blocked": [],
            "local_changes": [],
            "applied": [],
        }
        candidates = {}
        snapshots = {}
        for rel_path in selected:
            entry = artifacts[rel_path]
            if entry.get("canvas_type") == "module_header":
                continue
            path = repo_root / rel_path
            if not path.exists():
                report["blocked"].append(
                    {"file": rel_path, "reason": "Local Markdown is missing"}
                )
                continue
            local_hash = content_hash(path)
            try:
                live = fetch_canvas_state(client, entry)
                snapshots[rel_path] = {"local_hash": local_hash, "canvas": live}
                if live is None:
                    report["orphans"].append(rel_path)
                    continue
                drift = compute_drift(
                    path,
                    live,
                    entry["canvas_type"],
                    manifest_path=manifest_path,
                    manifest=manifest,
                )
                fingerprint = canvas_fingerprint(live, entry["canvas_type"])
                # A stored baseline separates pending local work from Canvas edits.
                if entry.get(
                    "canvas_fingerprint"
                ) == fingerprint and local_hash != entry.get("content_hash"):
                    report["local_changes"].append(rel_path)
                    continue
                if not drift:
                    continue
                report["report"].append({"file": rel_path, "drift": drift})
                fm, _ = parse_frontmatter(path)
                hosted = artifact_hosted_info(path, manifest_path, manifest, fm)[
                    "enabled"
                ]
                reason = None
                if local_hash != entry.get("content_hash"):
                    reason = "Local source also differs from deployment state; merge the changes explicitly"
                elif hosted and "body" in drift:
                    reason = "Hosted Canvas wrapper differs; preserve Markdown and review the shell separately"
                elif "questions" in drift:
                    reason = "Quiz questions changed; review and import supported questions explicitly"
                if reason:
                    report["blocked"].append({"file": rel_path, "reason": reason})
                    continue
                text = reconciled_text(path, live, drift, hosted=hosted)
                errors = validate_candidate(path, text)
                if errors:
                    report["blocked"].append(
                        {
                            "file": rel_path,
                            "reason": "Reconciled Markdown fails validation",
                            "errors": errors,
                        }
                    )
                    continue
                candidates[rel_path] = (text, fingerprint)
            except Exception as exc:
                report["blocked"].append({"file": rel_path, "reason": str(exc)})
        report["drifted"] = len(report["report"])
        token_payload = {
            "manifest": manifest,
            "state_path": str(store.path),
            "selected": selected,
            "snapshots": snapshots,
        }
        token = hashlib.sha256(
            json.dumps(token_payload, sort_keys=True).encode()
        ).hexdigest()[:20]
        report["confirmation_token"] = token
        if apply:
            if not confirm_token or confirm_token != token:
                raise ValueError(
                    "--apply requires the matching --confirm-token from a fresh dry run"
                )
            if report["blocked"]:
                raise ValueError(
                    "Reconcile has blocked files; resolve them or dry-run a --file subset"
                )
            backup_dir = (
                manifest_path.parent.parent / "reports" / f"reconcile-backup-{token}"
            )
            if candidates or report["orphans"]:
                backup_dir.mkdir(parents=True, exist_ok=True)
                (backup_dir / "deployment-state.json").write_bytes(
                    store.path.read_bytes()
                )
            for rel_path, (text, fingerprint) in candidates.items():
                path = repo_root / rel_path
                # Recheck immediately before replacement in case another editor wrote during the scan.
                if content_hash(path) != snapshots[rel_path]["local_hash"]:
                    raise ValueError(f"{rel_path}: source changed during reconcile")
                backup = backup_dir / rel_path
                backup.parent.mkdir(parents=True, exist_ok=True)
                backup.write_bytes(path.read_bytes())
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=path.parent,
                    suffix=".tmp",
                    delete=False,
                ) as output:
                    output.write(text)
                    temp_path = Path(output.name)
                temp_path.replace(path)
                entry = artifacts[rel_path]
                entry.update(
                    content_hash=content_hash(path),
                    canvas_fingerprint=fingerprint,
                    last_pulled=utc_now(),
                )
                entry.pop("canvas_payload_hash", None)
                entry.pop("orphaned", None)
                manifest["last_sync"] = utc_now()
                store.save(
                    manifest
                )  # Record each completed file for partial-failure recovery.
                report["applied"].append(rel_path)
            for rel_path in report["orphans"]:
                artifacts[rel_path]["orphaned"] = True
            if report["orphans"]:
                manifest["last_sync"] = utc_now()
                store.save(manifest)
            if candidates or report["orphans"]:
                report["backup_dir"] = str(backup_dir)
        return report


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    parser.add_argument(
        "--file",
        action="append",
        help="Limit reconciliation to this repo-relative mapped file; repeatable.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-token")
    args = parser.parse_args()
    report = reconcile(
        args.manifest.resolve(),
        state_dir=args.state_dir,
        apply=args.apply,
        confirm_token=args.confirm_token,
        files=args.file,
    )
    print(json.dumps(report, indent=2))
    return 1 if report["blocked"] else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (CanvasError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

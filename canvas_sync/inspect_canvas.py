"""
Inspect live Canvas course state and compare it with a local manifest.

This script is read-only against Canvas. It may write local ledger files under
<course>/reports/ when --write-ledger is provided.

Usage:
  python canvas_sync/inspect_canvas.py --manifest course1/manifests/production.json --include-items
  python canvas_sync/inspect_canvas.py --manifest course1/manifests/production.json --include-items --drift --write-ledger --format markdown
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from typing import Any

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_enabled
from canvas_sync.pull import fetch_canvas_state, html_to_markdown
from canvas_sync.push import md_body_to_canvas_html
from canvas_sync.schema import parse_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent

CANVAS_ITEM_TYPE_BY_ARTIFACT = {
    "assignment": "Assignment",
    "page": "Page",
    "discussion": "Discussion",
    "quiz": "Quiz",
}


def load_manifest(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def course_dir_for_manifest(manifest_path: Path) -> Path:
    if manifest_path.parent.name == "manifests":
        return manifest_path.parent.parent
    return manifest_path.parent


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def artifact_canvas_key(entry: dict) -> tuple[str, Any] | None:
    atype = entry.get("canvas_type")
    if atype == "module_header":
        return None
    item_type = CANVAS_ITEM_TYPE_BY_ARTIFACT.get(atype)
    if not item_type:
        return None
    if atype == "page":
        value = entry.get("canvas_page_url")
    else:
        value = entry.get("canvas_id")
    if value in (None, ""):
        return None
    return item_type, value


def module_item_canvas_key(item: dict) -> tuple[str, Any] | None:
    item_type = item.get("type")
    if item_type == "Page":
        value = item.get("page_url") or item.get("url")
    else:
        value = item.get("content_id")
    if not item_type or value in (None, ""):
        return None
    return item_type, value


def artifact_record(rel_path: str, entry: dict) -> dict:
    path = REPO_ROOT / rel_path
    return {
        "file": rel_path,
        "canvas_type": entry.get("canvas_type"),
        "canvas_id": entry.get("canvas_id"),
        "canvas_page_url": entry.get("canvas_page_url"),
        "canvas_module_id": entry.get("canvas_module_id"),
        "last_pushed": entry.get("last_pushed"),
        "local_exists": path.exists(),
    }


def module_item_record(item: dict, manifest_file: str | None = None) -> dict:
    return {
        "module_item_id": item.get("id"),
        "position": item.get("position"),
        "title": item.get("title"),
        "type": item.get("type"),
        "content_id": item.get("content_id"),
        "page_url": item.get("page_url"),
        "canvas_url": item.get("url"),
        "published": item.get("published"),
        "manifest_file": manifest_file,
    }


def discover_unmanifested_local_files(course_dir: Path, artifacts: dict) -> list[dict]:
    records: list[dict] = []
    for md_path in sorted(course_dir.glob("sprints/sprint-*/*.md")):
        rel_path = repo_relative(md_path)
        if rel_path in artifacts:
            continue
        record: dict[str, Any] = {"file": rel_path}
        try:
            fm, _body = parse_frontmatter(md_path)
            record.update({
                "type": fm.get("type"),
                "title": fm.get("title"),
                "module": fm.get("module"),
                "position": fm.get("position"),
            })
        except Exception as exc:  # noqa: BLE001 - ledger should preserve parse failures
            record["error"] = str(exc)
        records.append(record)
    return records


def rendered_local_body_to_markdown(body: str) -> str:
    """Normalize local Markdown through the same render path used by Canvas push."""
    return html_to_markdown(md_body_to_canvas_html(body)).strip()


def compute_inspection_drift(md_path: Path, canvas_state: dict, atype: str) -> dict:
    fm, body = parse_frontmatter(md_path)

    canvas_title = canvas_state.get("name") or canvas_state.get("title")
    canvas_body_html = (
        canvas_state.get("description")
        or canvas_state.get("body")
        or canvas_state.get("message")
        or ""
    )
    canvas_body_md = html_to_markdown(canvas_body_html).strip()
    local_body_md = rendered_local_body_to_markdown(body)

    drift: dict[str, Any] = {}
    if canvas_title != fm.get("title"):
        drift["title"] = {"local": fm.get("title"), "canvas": canvas_title}

    if local_body_md != canvas_body_md:
        drift["body"] = {
            "local_chars": len(local_body_md),
            "canvas_chars": len(canvas_body_md),
            "local_preview": local_body_md[:200],
            "canvas_preview": canvas_body_md[:200],
        }

    if atype in ("assignment", "quiz", "discussion"):
        canvas_points = canvas_state.get("points_possible")
        if canvas_state.get("assignment"):
            canvas_points = canvas_state["assignment"].get("points_possible", canvas_points)
        if canvas_points != fm.get("points"):
            drift["points"] = {"local": fm.get("points"), "canvas": canvas_points}

    return drift


def compute_drift_report(client: CanvasClient, artifacts: dict) -> tuple[list[dict], list[dict], list[dict]]:
    drifted: list[dict] = []
    orphans: list[dict] = []
    errors: list[dict] = []

    for rel_path, entry in sorted(artifacts.items()):
        atype = entry.get("canvas_type")
        if atype == "module_header":
            continue
        md_path = REPO_ROOT / rel_path
        if not md_path.exists():
            continue

        try:
            canvas_state = fetch_canvas_state(client, entry)
            if canvas_state is None:
                orphans.append({"file": rel_path, "canvas_type": atype})
                continue
            drift = compute_inspection_drift(md_path, canvas_state, atype)
        except Exception as exc:  # noqa: BLE001 - report, do not hide remaining checks
            errors.append({"file": rel_path, "error": str(exc)})
            continue

        if drift:
            drifted.append({"file": rel_path, "drift": drift})

    return drifted, orphans, errors


def build_report(manifest_path: Path, *, include_items: bool, include_drift: bool) -> dict:
    load_dotenv(REPO_ROOT / ".env")

    manifest_path = manifest_path.resolve()
    manifest = load_manifest(manifest_path)
    course_dir = course_dir_for_manifest(manifest_path)
    artifacts = manifest.get("artifacts", {})
    instance = manifest.get("instance", {})
    course_id = instance.get("course_id")
    if not course_id:
        raise ValueError(f"{manifest_path}: manifest instance.course_id is required")

    check_instance_enabled(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = CanvasClient.from_env(course_id=course_id)
    live_modules = client.list_modules()

    manifest_by_module_id: dict[int, list[dict]] = defaultdict(list)
    manifest_module_ids: set[int] = set()
    manifest_item_keys: set[tuple[str, Any]] = set()
    manifest_files_by_item_key: dict[tuple[str, Any], list[str]] = defaultdict(list)
    missing_local_files: list[dict] = []

    for rel_path, entry in sorted(artifacts.items()):
        record = artifact_record(rel_path, entry)
        module_id = entry.get("canvas_module_id")
        if module_id is not None:
            manifest_by_module_id[int(module_id)].append(record)
            manifest_module_ids.add(int(module_id))
        if not record["local_exists"]:
            missing_local_files.append(record)
        key = artifact_canvas_key(entry)
        if key:
            manifest_item_keys.add(key)
            manifest_files_by_item_key[key].append(rel_path)

    live_module_ids = {int(m["id"]) for m in live_modules if m.get("id") is not None}
    live_item_keys: set[tuple[str, Any]] = set()
    canvas_items_not_in_manifest: list[dict] = []
    unpublished_items: list[dict] = []
    module_records: list[dict] = []

    for module in sorted(live_modules, key=lambda m: (m.get("position") or 999999, m.get("id") or 0)):
        module_id = int(module["id"])
        items = client.list_module_items(module_id) if include_items else []
        item_records = [
            module_item_record(
                item,
                (manifest_files_by_item_key.get(module_item_canvas_key(item)) or [None])[0],
            )
            for item in items
        ]

        for item, item_record in zip(items, item_records):
            key = module_item_canvas_key(item)
            if key:
                live_item_keys.add(key)
                if key not in manifest_item_keys:
                    canvas_items_not_in_manifest.append({
                        "module_id": module_id,
                        "module_name": module.get("name"),
                        **item_record,
                    })
            elif include_items:
                canvas_items_not_in_manifest.append({
                    "module_id": module_id,
                    "module_name": module.get("name"),
                    **item_record,
                })
            if item.get("published") is False:
                unpublished_items.append({
                    "module_id": module_id,
                    "module_name": module.get("name"),
                    **item_record,
                })

        module_records.append({
            "id": module_id,
            "position": module.get("position"),
            "name": module.get("name"),
            "published": module.get("published"),
            "items_count": module.get("items_count", len(items) if include_items else None),
            "manifest_artifacts": manifest_by_module_id.get(module_id, []),
            "items": item_records if include_items else None,
        })

    manifest_artifacts_not_in_module_items: list[dict] = []
    if include_items:
        for rel_path, entry in sorted(artifacts.items()):
            if entry.get("canvas_type") == "module_header":
                continue
            key = artifact_canvas_key(entry)
            if key and key not in live_item_keys:
                manifest_artifacts_not_in_module_items.append(artifact_record(rel_path, entry))

    drifted: list[dict] = []
    canvas_orphans: list[dict] = []
    drift_errors: list[dict] = []
    if include_drift:
        drifted, canvas_orphans, drift_errors = compute_drift_report(client, artifacts)

    canvas_modules_not_in_manifest = [
        {
            "id": int(module["id"]),
            "position": module.get("position"),
            "name": module.get("name"),
            "published": module.get("published"),
            "items_count": module.get("items_count"),
        }
        for module in sorted(live_modules, key=lambda m: (m.get("position") or 999999, m.get("id") or 0))
        if int(module["id"]) not in manifest_module_ids
    ]

    manifest_module_ids_not_live = [
        {
            "canvas_module_id": module_id,
            "artifacts": manifest_by_module_id[module_id],
        }
        for module_id in sorted(manifest_module_ids - live_module_ids)
    ]

    unpublished_modules = [
        {
            "id": int(module["id"]),
            "position": module.get("position"),
            "name": module.get("name"),
            "items_count": module.get("items_count"),
        }
        for module in live_modules
        if module.get("published") is False
    ]

    unmanifested_local_files = discover_unmanifested_local_files(course_dir, artifacts)

    checks = {
        "canvas_modules_not_in_manifest": canvas_modules_not_in_manifest,
        "manifest_module_ids_not_live": manifest_module_ids_not_live,
        "canvas_items_not_in_manifest": canvas_items_not_in_manifest if include_items else None,
        "manifest_artifacts_not_in_module_items": manifest_artifacts_not_in_module_items if include_items else None,
        "missing_local_files": missing_local_files,
        "unmanifested_local_files": unmanifested_local_files,
        "unpublished_modules": unpublished_modules,
        "unpublished_items": unpublished_items if include_items else None,
        "drifted_artifacts": drifted if include_drift else None,
        "canvas_orphans": canvas_orphans if include_drift else None,
        "drift_errors": drift_errors if include_drift else None,
    }

    summary = {
        "live_modules": len(live_modules),
        "manifest_module_ids": len(manifest_module_ids),
        "manifest_artifacts": len(artifacts),
        "missing_local_files": len(missing_local_files),
        "unmanifested_local_files": len(unmanifested_local_files),
        "canvas_modules_not_in_manifest": len(canvas_modules_not_in_manifest),
        "manifest_module_ids_not_live": len(manifest_module_ids_not_live),
        "unpublished_modules": len(unpublished_modules),
    }
    if include_items:
        summary.update({
            "canvas_items_not_in_manifest": len(canvas_items_not_in_manifest),
            "manifest_artifacts_not_in_module_items": len(manifest_artifacts_not_in_module_items),
            "unpublished_items": len(unpublished_items),
        })
    if include_drift:
        summary.update({
            "drifted_artifacts": len(drifted),
            "canvas_orphans": len(canvas_orphans),
            "drift_errors": len(drift_errors),
        })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "manifest": {
            "path": repo_relative(manifest_path),
            "last_sync": manifest.get("last_sync"),
            "instance": instance,
        },
        "options": {
            "include_items": include_items,
            "include_drift": include_drift,
        },
        "summary": summary,
        "modules": module_records,
        "checks": checks,
    }


def render_markdown(report: dict) -> str:
    instance = report["manifest"]["instance"]
    summary = report["summary"]
    lines = [
        "# Canvas Ledger",
        "",
        f"Generated: {report['generated_at']}",
        f"Manifest: `{report['manifest']['path']}`",
        f"Course: {instance.get('name', 'unknown')} ({instance.get('base_url', '').rstrip('/')}/courses/{instance.get('course_id')})",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]
    for key, value in summary.items():
        lines.append(f"| {key.replace('_', ' ')} | {value} |")

    lines.extend([
        "",
        "## Live Modules",
        "",
        "| Position | Canvas module ID | Module | Published | Items | Manifest artifacts |",
        "|---:|---:|---|---|---:|---:|",
    ])
    for module in report["modules"]:
        manifest_count = len(module.get("manifest_artifacts") or [])
        published = "yes" if module.get("published") else "no"
        items_count = module.get("items_count")
        lines.append(
            f"| {module.get('position') or ''} | {module['id']} | {module.get('name') or ''} | "
            f"{published} | {items_count if items_count is not None else ''} | {manifest_count} |"
        )

    checks = report["checks"]
    warning_sections = [
        ("Canvas Modules Not In Manifest", checks.get("canvas_modules_not_in_manifest") or []),
        ("Manifest Module IDs Not Live", checks.get("manifest_module_ids_not_live") or []),
        ("Canvas Items Not In Manifest", checks.get("canvas_items_not_in_manifest") or []),
        ("Manifest Artifacts Not In Module Items", checks.get("manifest_artifacts_not_in_module_items") or []),
        ("Missing Local Files", checks.get("missing_local_files") or []),
        ("Unmanifested Local Files", checks.get("unmanifested_local_files") or []),
        ("Unpublished Modules", checks.get("unpublished_modules") or []),
        ("Unpublished Items", checks.get("unpublished_items") or []),
        ("Drifted Artifacts", checks.get("drifted_artifacts") or []),
        ("Canvas Orphans", checks.get("canvas_orphans") or []),
        ("Drift Errors", checks.get("drift_errors") or []),
    ]

    for title, records in warning_sections:
        if not records:
            continue
        lines.extend(["", f"## {title}", ""])
        for record in records:
            label = (
                record.get("file")
                or record.get("title")
                or record.get("name")
                or record.get("module_name")
                or str(record.get("canvas_module_id") or record.get("id"))
            )
            lines.append(f"- `{label}`")

    if report["options"].get("include_items"):
        lines.extend(["", "## Module Items", ""])
        for module in report["modules"]:
            lines.extend(["", f"### {module.get('position')}. {module.get('name')} ({module['id']})", ""])
            items = module.get("items") or []
            if not items:
                lines.append("No module items returned.")
                continue
            lines.extend([
                "| Position | Module item ID | Type | Title | Published | Content ID | Page URL | Manifest file |",
                "|---:|---:|---|---|---|---:|---|---|",
            ])
            for item in items:
                published = "" if item.get("published") is None else ("yes" if item.get("published") else "no")
                lines.append(
                    f"| {item.get('position') or ''} | {item.get('module_item_id') or ''} | "
                    f"{item.get('type') or ''} | {item.get('title') or ''} | {published} | "
                    f"{item.get('content_id') or ''} | {item.get('page_url') or ''} | "
                    f"{item.get('manifest_file') or ''} |"
                )

    return "\n".join(lines).rstrip() + "\n"


def write_ledger_files(report: dict, manifest_path: Path, ledger_dir: Path | None) -> dict[str, str]:
    course_dir = course_dir_for_manifest(manifest_path.resolve())
    output_dir = ledger_dir.resolve() if ledger_dir else course_dir / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"canvas-ledger-{manifest_path.stem}"
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"

    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    return {
        "json": repo_relative(json_path),
        "markdown": repo_relative(md_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--include-items", action="store_true")
    parser.add_argument("--drift", action="store_true", help="Fetch known artifacts and report title/body/points drift.")
    parser.add_argument("--write-ledger", action="store_true", help="Write JSON and Markdown ledgers under <course>/reports/.")
    parser.add_argument("--ledger-dir", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()

    try:
        report = build_report(args.manifest, include_items=args.include_items, include_drift=args.drift)
        if args.write_ledger:
            report["ledger_paths"] = write_ledger_files(report, args.manifest, args.ledger_dir)

        if args.format == "markdown":
            print(render_markdown(report))
        else:
            print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except (CanvasError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

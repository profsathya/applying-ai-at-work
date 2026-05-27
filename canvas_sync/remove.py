"""
Remove manifest-backed Canvas modules or artifacts after an explicit dry run.

Usage:
  python canvas_sync/remove.py --manifest <path> --target module_id:123 --dry-run
  python canvas_sync/remove.py --manifest <path> --target module_id:123 --apply --confirm-token <token>

Targets:
  module_id:<canvas_module_id>
  module_position:<position>
  module_item_id:<module_item_id>
  file:<repo-relative-md-path>
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

if os.name == "nt":
    import msvcrt
else:
    import fcntl

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError


REPO_ROOT = Path(__file__).resolve().parent.parent

CANVAS_ITEM_TYPE_BY_ARTIFACT = {
    "assignment": "Assignment",
    "page": "Page",
    "discussion": "Discussion",
    "quiz": "Quiz",
}


class RemovalPlanError(ValueError):
    """Raised when a removal target or confirmation token is not acceptable."""


def load_manifest(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def save_manifest(path: Path, manifest: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


@contextmanager
def manifest_lock(path: Path):
    lock_path = path.with_suffix(path.suffix + ".lock")
    with open(lock_path, "w") as lock_file:
        if os.name == "nt":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock_file, fcntl.LOCK_UN)


def artifact_canvas_key(entry: dict) -> tuple[str, Any] | None:
    atype = entry.get("canvas_type")
    if atype == "module_header":
        return None
    item_type = CANVAS_ITEM_TYPE_BY_ARTIFACT.get(atype)
    if not item_type:
        return None
    value = entry.get("canvas_page_url") if atype == "page" else entry.get("canvas_id")
    if value in (None, ""):
        return None
    return item_type, value


def module_item_canvas_key(item: dict) -> tuple[str, Any] | None:
    item_type = item.get("type")
    value = item.get("page_url") if item_type == "Page" else item.get("content_id")
    if not item_type or value in (None, ""):
        return None
    return item_type, value


def parse_target(target: str) -> tuple[str, str]:
    if ":" not in target:
        raise RemovalPlanError(f"{target}: expected '<kind>:<value>'")
    kind, value = target.split(":", 1)
    if kind not in {"module_id", "module_position", "module_item_id", "file"}:
        raise RemovalPlanError(f"{target}: unsupported target kind")
    if not value:
        raise RemovalPlanError(f"{target}: target value is required")
    if kind != "file":
        try:
            int(value)
        except ValueError as exc:
            raise RemovalPlanError(f"{target}: numeric target value required") from exc
    if kind == "file":
        value = value[2:] if value.startswith("./") else value
        if Path(value).is_absolute():
            raise RemovalPlanError(f"{target}: file target must be repo-relative")
    return kind, value


def fetch_live_state(client: CanvasClient) -> tuple[list[dict], list[dict]]:
    modules: list[dict] = []
    items: list[dict] = []
    for module in sorted(
        client.list_modules(),
        key=lambda m: (m.get("position") or 999999, m.get("id") or 0),
    ):
        module_id = int(module["id"])
        module_record = {
            "module_id": module_id,
            "position": module.get("position"),
            "name": module.get("name"),
            "published": module.get("published"),
            "items_count": module.get("items_count"),
        }
        modules.append(module_record)
        for item in sorted(
            client.list_module_items(module_id),
            key=lambda i: (i.get("position") or 999999, i.get("id") or 0),
        ):
            item_record = {
                "module_id": module_id,
                "module_name": module.get("name"),
                "module_position": module.get("position"),
                "module_item_id": int(item["id"]),
                "position": item.get("position"),
                "title": item.get("title"),
                "type": item.get("type"),
                "content_id": item.get("content_id"),
                "page_url": item.get("page_url"),
                "published": item.get("published"),
            }
            item_record["canvas_key"] = module_item_canvas_key(item_record)
            items.append(item_record)
    return modules, items


def build_manifest_indexes(manifest: dict) -> dict:
    module_id_to_files: dict[int, list[str]] = defaultdict(list)
    key_to_files: dict[tuple[str, Any], list[str]] = defaultdict(list)
    for rel_path, entry in sorted(manifest.get("artifacts", {}).items()):
        module_id = entry.get("canvas_module_id")
        if module_id is not None:
            module_id_to_files[int(module_id)].append(rel_path)
        key = artifact_canvas_key(entry)
        if key:
            key_to_files[key].append(rel_path)
    return {
        "module_id_to_files": module_id_to_files,
        "key_to_files": key_to_files,
    }


def annotate_live_items(items: list[dict], key_to_files: dict[tuple[str, Any], list[str]]) -> None:
    for item in items:
        files = key_to_files.get(item.get("canvas_key"), [])
        item["manifest_files"] = files
        item["manifest_file"] = files[0] if files else None


def block(blocked: list[dict], target: str, reason: str, **extra: Any) -> None:
    record = {"target": target, "reason": reason}
    record.update(extra)
    blocked.append(record)


def select_module(
    *,
    target: str,
    module_id: int,
    modules_by_id: dict[int, dict],
    items_by_module_id: dict[int, list[dict]],
    artifacts: dict,
    module_id_to_files: dict[int, list[str]],
    selected_modules: set[int],
    selected_files: set[str],
    selected_module_item_ids: set[int],
    blocked: list[dict],
) -> None:
    if module_id not in modules_by_id:
        block(blocked, target, "module is not live in Canvas", module_id=module_id)
        return
    if module_id not in module_id_to_files:
        block(blocked, target, "module is not backed by the manifest", module_id=module_id)
        return

    module_items = items_by_module_id.get(module_id, [])
    canvas_only = [item for item in module_items if not item.get("manifest_files")]
    if canvas_only:
        for item in canvas_only:
            block(
                blocked,
                target,
                "module contains a Canvas-only item",
                module_id=module_id,
                module_item_id=item["module_item_id"],
                title=item.get("title"),
            )
        return

    files = module_id_to_files[module_id]
    missing_live_items = []
    for rel_path in files:
        entry = artifacts[rel_path]
        if entry.get("canvas_type") == "module_header":
            continue
        key = artifact_canvas_key(entry)
        if not any(item.get("canvas_key") == key for item in module_items):
            missing_live_items.append(rel_path)
    if missing_live_items:
        for rel_path in missing_live_items:
            block(
                blocked,
                target,
                "manifest artifact is not present as a live module item",
                module_id=module_id,
                file=rel_path,
            )
        return

    selected_modules.add(module_id)
    selected_files.update(files)
    selected_module_item_ids.update(item["module_item_id"] for item in module_items)


def select_file(
    *,
    target: str,
    rel_path: str,
    modules_by_id: dict[int, dict],
    items_by_module_id: dict[int, list[dict]],
    artifacts: dict,
    module_id_to_files: dict[int, list[str]],
    selected_modules: set[int],
    selected_files: set[str],
    selected_module_item_ids: set[int],
    blocked: list[dict],
) -> None:
    entry = artifacts.get(rel_path)
    if not entry:
        block(blocked, target, "file is not backed by the manifest", file=rel_path)
        return

    module_id = entry.get("canvas_module_id")
    if module_id is None:
        block(blocked, target, "manifest entry has no canvas_module_id", file=rel_path)
        return
    module_id = int(module_id)

    if entry.get("canvas_type") == "module_header":
        select_module(
            target=target,
            module_id=module_id,
            modules_by_id=modules_by_id,
            items_by_module_id=items_by_module_id,
            artifacts=artifacts,
            module_id_to_files=module_id_to_files,
            selected_modules=selected_modules,
            selected_files=selected_files,
            selected_module_item_ids=selected_module_item_ids,
            blocked=blocked,
        )
        return

    key = artifact_canvas_key(entry)
    if not key:
        block(blocked, target, "manifest entry has no Canvas content identifier", file=rel_path)
        return

    matching_items = [
        item for item in items_by_module_id.get(module_id, []) if item.get("canvas_key") == key
    ]
    if not matching_items:
        block(
            blocked,
            target,
            "manifest artifact is not present as a live module item",
            file=rel_path,
            module_id=module_id,
        )
        return

    selected_files.add(rel_path)
    selected_module_item_ids.update(item["module_item_id"] for item in matching_items)


def validate_no_unselected_content_links(
    *,
    artifacts: dict,
    key_to_files: dict[tuple[str, Any], list[str]],
    live_items_by_key: dict[tuple[str, Any], list[dict]],
    selected_files: set[str],
    selected_module_item_ids: set[int],
    blocked: list[dict],
) -> None:
    selected_keys = {
        artifact_canvas_key(artifacts[rel_path])
        for rel_path in selected_files
        if artifacts[rel_path].get("canvas_type") != "module_header"
    }
    for key in sorted(k for k in selected_keys if k is not None):
        unselected_files = [rel_path for rel_path in key_to_files.get(key, []) if rel_path not in selected_files]
        for rel_path in unselected_files:
            block(
                blocked,
                rel_path,
                "same Canvas content is mapped to another unselected manifest entry",
                file=rel_path,
            )

        unselected_items = [
            item
            for item in live_items_by_key.get(key, [])
            if item["module_item_id"] not in selected_module_item_ids
        ]
        for item in unselected_items:
            block(
                blocked,
                str(item["module_item_id"]),
                "same Canvas content appears in an unselected module item",
                module_id=item["module_id"],
                module_item_id=item["module_item_id"],
                title=item.get("title"),
            )


def validate_selected_modules_empty_after_item_deletes(
    *,
    selected_modules: set[int],
    selected_module_item_ids: set[int],
    items_by_module_id: dict[int, list[dict]],
    blocked: list[dict],
) -> None:
    for module_id in sorted(selected_modules):
        remaining = [
            item
            for item in items_by_module_id.get(module_id, [])
            if item["module_item_id"] not in selected_module_item_ids
        ]
        for item in remaining:
            block(
                blocked,
                f"module_id:{module_id}",
                "selected module would still contain an unselected module item",
                module_id=module_id,
                module_item_id=item["module_item_id"],
                title=item.get("title"),
            )


def content_operation(rel_path: str, entry: dict) -> dict:
    atype = entry["canvas_type"]
    op = {
        "action": "delete_content",
        "canvas_type": atype,
        "file": rel_path,
    }
    if atype == "page":
        op["canvas_page_url"] = entry.get("canvas_page_url")
    else:
        op["canvas_id"] = entry.get("canvas_id")
    return op


def build_operations(
    *,
    artifacts: dict,
    modules_by_id: dict[int, dict],
    items_by_id: dict[int, dict],
    selected_modules: set[int],
    selected_files: set[str],
    selected_module_item_ids: set[int],
) -> list[dict]:
    operations: list[dict] = []

    for item_id in sorted(
        selected_module_item_ids,
        key=lambda i: (
            items_by_id[i].get("module_position") or 999999,
            items_by_id[i].get("module_id") or 0,
            items_by_id[i].get("position") or 999999,
            i,
        ),
    ):
        item = items_by_id[item_id]
        operations.append({
            "action": "delete_module_item",
            "module_id": item["module_id"],
            "module_item_id": item["module_item_id"],
            "title": item.get("title"),
            "type": item.get("type"),
            "file": item.get("manifest_file"),
        })

    seen_content_keys: set[tuple[str, Any]] = set()
    for rel_path in sorted(selected_files):
        entry = artifacts[rel_path]
        if entry.get("canvas_type") == "module_header":
            continue
        key = artifact_canvas_key(entry)
        if key in seen_content_keys:
            continue
        seen_content_keys.add(key)
        operations.append(content_operation(rel_path, entry))

    for module_id in sorted(
        selected_modules,
        key=lambda mid: (modules_by_id[mid].get("position") or 999999, mid),
    ):
        module = modules_by_id[module_id]
        operations.append({
            "action": "delete_module",
            "module_id": module_id,
            "name": module.get("name"),
            "position": module.get("position"),
        })

    return operations


def confirmation_token_for(plan: dict) -> str:
    payload = {
        "manifest": plan["manifest"],
        "targets": sorted(plan["targets"]),
        "operations": plan["operations"],
        "manifest_entries_to_remove": plan["manifest_entries_to_remove"],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:12]


def build_removal_plan(manifest: dict, targets: list[str], client: CanvasClient, manifest_path: Path | None = None) -> dict:
    artifacts = manifest.get("artifacts", {})
    modules, live_items = fetch_live_state(client)
    indexes = build_manifest_indexes(manifest)
    key_to_files = indexes["key_to_files"]
    module_id_to_files = indexes["module_id_to_files"]
    annotate_live_items(live_items, key_to_files)

    modules_by_id = {module["module_id"]: module for module in modules}
    modules_by_position: dict[int, list[dict]] = defaultdict(list)
    for module in modules:
        if module.get("position") is not None:
            modules_by_position[int(module["position"])].append(module)

    items_by_id = {item["module_item_id"]: item for item in live_items}
    items_by_module_id: dict[int, list[dict]] = defaultdict(list)
    live_items_by_key: dict[tuple[str, Any], list[dict]] = defaultdict(list)
    for item in live_items:
        items_by_module_id[item["module_id"]].append(item)
        if item.get("canvas_key") is not None:
            live_items_by_key[item["canvas_key"]].append(item)

    selected_modules: set[int] = set()
    selected_files: set[str] = set()
    selected_module_item_ids: set[int] = set()
    blocked: list[dict] = []

    for raw_target in targets:
        try:
            kind, value = parse_target(raw_target)
        except RemovalPlanError as exc:
            block(blocked, raw_target, str(exc))
            continue

        if kind == "module_id":
            select_module(
                target=raw_target,
                module_id=int(value),
                modules_by_id=modules_by_id,
                items_by_module_id=items_by_module_id,
                artifacts=artifacts,
                module_id_to_files=module_id_to_files,
                selected_modules=selected_modules,
                selected_files=selected_files,
                selected_module_item_ids=selected_module_item_ids,
                blocked=blocked,
            )
        elif kind == "module_position":
            matches = modules_by_position.get(int(value), [])
            if len(matches) != 1:
                block(blocked, raw_target, "module position did not resolve to exactly one live module")
                continue
            select_module(
                target=raw_target,
                module_id=matches[0]["module_id"],
                modules_by_id=modules_by_id,
                items_by_module_id=items_by_module_id,
                artifacts=artifacts,
                module_id_to_files=module_id_to_files,
                selected_modules=selected_modules,
                selected_files=selected_files,
                selected_module_item_ids=selected_module_item_ids,
                blocked=blocked,
            )
        elif kind == "module_item_id":
            item = items_by_id.get(int(value))
            if not item:
                block(blocked, raw_target, "module item is not live in Canvas")
                continue
            if not item.get("manifest_files"):
                block(
                    blocked,
                    raw_target,
                    "module item is not backed by the manifest",
                    module_id=item["module_id"],
                    module_item_id=item["module_item_id"],
                    title=item.get("title"),
                )
                continue
            selected_files.update(item["manifest_files"])
            selected_module_item_ids.add(item["module_item_id"])
        elif kind == "file":
            select_file(
                target=raw_target,
                rel_path=value,
                modules_by_id=modules_by_id,
                items_by_module_id=items_by_module_id,
                artifacts=artifacts,
                module_id_to_files=module_id_to_files,
                selected_modules=selected_modules,
                selected_files=selected_files,
                selected_module_item_ids=selected_module_item_ids,
                blocked=blocked,
            )

    validate_no_unselected_content_links(
        artifacts=artifacts,
        key_to_files=key_to_files,
        live_items_by_key=live_items_by_key,
        selected_files=selected_files,
        selected_module_item_ids=selected_module_item_ids,
        blocked=blocked,
    )
    validate_selected_modules_empty_after_item_deletes(
        selected_modules=selected_modules,
        selected_module_item_ids=selected_module_item_ids,
        items_by_module_id=items_by_module_id,
        blocked=blocked,
    )

    operations = build_operations(
        artifacts=artifacts,
        modules_by_id=modules_by_id,
        items_by_id=items_by_id,
        selected_modules=selected_modules,
        selected_files=selected_files,
        selected_module_item_ids=selected_module_item_ids,
    )
    manifest_entries_to_remove = sorted(selected_files)
    plan = {
        "manifest": {
            "path": str(manifest_path) if manifest_path else None,
            "instance": manifest.get("instance", {}),
            "last_sync": manifest.get("last_sync"),
        },
        "targets": targets,
        "apply_allowed": not blocked and bool(operations),
        "blocked": blocked,
        "operations": operations,
        "manifest_entries_to_remove": manifest_entries_to_remove,
        "local_files_kept": manifest_entries_to_remove,
    }
    plan["confirmation_token"] = confirmation_token_for(plan) if plan["apply_allowed"] else None
    return plan


def execute_operation(client: CanvasClient, operation: dict) -> None:
    action = operation["action"]
    if action == "delete_module_item":
        client.delete_module_item(operation["module_id"], operation["module_item_id"])
    elif action == "delete_module":
        client.delete_module(operation["module_id"])
    elif action == "delete_content":
        atype = operation["canvas_type"]
        if atype == "assignment":
            client.delete_assignment(operation["canvas_id"])
        elif atype == "page":
            client.delete_page(operation["canvas_page_url"])
        elif atype == "discussion":
            client.delete_discussion(operation["canvas_id"])
        elif atype == "quiz":
            client.delete_quiz(operation["canvas_id"])
        else:
            raise RemovalPlanError(f"unsupported content type for deletion: {atype}")
    else:
        raise RemovalPlanError(f"unsupported removal operation: {action}")


def apply_plan_to_manifest(manifest: dict, plan: dict) -> None:
    artifacts = manifest.setdefault("artifacts", {})
    for rel_path in plan["manifest_entries_to_remove"]:
        artifacts.pop(rel_path, None)
    manifest["last_sync"] = datetime.now(timezone.utc).isoformat(timespec="seconds")


def apply_removal(
    manifest_path: Path,
    targets: list[str],
    confirm_token: str | None,
    client: CanvasClient,
) -> dict:
    if not confirm_token:
        raise RemovalPlanError("apply requires --confirm-token from a fresh dry run")

    manifest_path = manifest_path.resolve()
    with manifest_lock(manifest_path):
        manifest = load_manifest(manifest_path)
        plan = build_removal_plan(manifest, targets, client, manifest_path)
        if not plan["apply_allowed"]:
            raise RemovalPlanError("removal plan is blocked; run dry-run and resolve blocked targets")
        if confirm_token != plan["confirmation_token"]:
            raise RemovalPlanError("confirmation token does not match the current removal plan")

        for operation in plan["operations"]:
            execute_operation(client, operation)

        apply_plan_to_manifest(manifest, plan)
        save_manifest(manifest_path, manifest)

    applied = dict(plan)
    applied["mode"] = "apply"
    return applied


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--target", action="append", required=True)
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--dry-run", action="store_true")
    mode_group.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-token")
    args = parser.parse_args()

    try:
        manifest_path = args.manifest.resolve()
        if args.dry_run:
            manifest = load_manifest(manifest_path)
            client = CanvasClient.from_env(course_id=manifest["instance"]["course_id"])
            plan = build_removal_plan(manifest, args.target, client, manifest_path)
            plan["mode"] = "dry-run"
            print(json.dumps(plan, indent=2, sort_keys=True))
            return 0

        manifest = load_manifest(manifest_path)
        client = CanvasClient.from_env(course_id=manifest["instance"]["course_id"])
        applied = apply_removal(manifest_path, args.target, args.confirm_token, client)
        print(json.dumps(applied, indent=2, sort_keys=True))
        return 0
    except RemovalPlanError as exc:
        print(f"REMOVAL ERROR: {exc}", file=sys.stderr)
        return 2
    except CanvasError as exc:
        print(f"CANVAS ERROR: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

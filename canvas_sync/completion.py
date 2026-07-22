"""Canvas module completion requirement helpers and backfill CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import (
    CanvasStateStore,
    derive_artifact_id,
)


REPO_ROOT = Path(__file__).resolve().parent.parent

COMPLETION_VALUES = {
    "auto",
    "none",
    "must_view",
    "must_submit",
    "must_contribute",
    "must_mark_done",
    "min_score",
}

CANVAS_ITEM_TYPE_BY_ARTIFACT = {
    "assignment": "Assignment",
    "page": "Page",
    "discussion": "Discussion",
    "quiz": "Quiz",
}


def completion_requirement_for(frontmatter: dict, canvas_type: str) -> dict | None:
    """Return the Canvas completion_requirement payload for an artifact."""
    configured = frontmatter.get("completion_requirement", "auto")
    if configured not in COMPLETION_VALUES:
        raise ValueError(f"Unsupported completion_requirement: {configured!r}")
    if configured == "none" or canvas_type == "module_header":
        return None

    requirement_type = configured
    if configured == "auto":
        if canvas_type == "page":
            requirement_type = "must_view"
        elif canvas_type in {"assignment", "quiz"}:
            requirement_type = "must_submit"
        elif canvas_type == "discussion":
            requirement_type = "must_contribute"
        else:
            return None

    payload: dict[str, Any] = {"type": requirement_type}
    if requirement_type == "min_score":
        points = frontmatter.get("points")
        payload["min_score"] = int(points) if isinstance(points, (int, float)) and points > 0 else 1
    return payload


def completion_requirement_state_value(requirement: dict | None) -> str | None:
    if not requirement:
        return None
    return str(requirement.get("type") or "")


def same_completion_requirement(current: dict | None, desired: dict | None) -> bool:
    if not current and not desired:
        return True
    if not current or not desired:
        return False
    for key in ("type", "min_score"):
        if current.get(key) != desired.get(key):
            return False
    return True


def module_item_canvas_key(item: dict) -> tuple[str, Any] | None:
    item_type = item.get("type")
    if item_type == "Page":
        value = item.get("page_url") or item.get("url")
    else:
        value = item.get("content_id")
    if not item_type or value in (None, ""):
        return None
    return item_type, value


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


def _repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def _state_items(deployment_state: dict, *, external_state: bool) -> list[tuple[str, dict, str]]:
    items: list[tuple[str, dict, str]] = []
    for state_key, entry in sorted(deployment_state.get("artifacts", {}).items()):
        rel_path = entry.get("local_path") if external_state else state_key
        if not rel_path:
            continue
        items.append((state_key, entry, str(rel_path)))
    return items


def build_module_completion_plan(
    manifest_path: Path,
    state_dir: Path | None = None,
    *,
    client: CanvasClient | None = None,
) -> dict:
    """Build a dry-run plan for module item completion backfill."""
    repo_root = REPO_ROOT
    store = CanvasStateStore(manifest_path=manifest_path, repo_root=repo_root, state_dir=state_dir)
    with store.locked() as (manifest, deployment_state, state_path):
        course_id = int(manifest.get("instance", {}).get("course_id") or 0)
        if not course_id:
            raise ValueError(f"{manifest_path}: manifest instance.course_id is required")
        if client is None:
            check_env_matches_instance(manifest, manifest_label=str(manifest_path))
        canvas = client or CanvasClient.from_env(course_id=course_id)

        module_ids = sorted(
            {
                int(entry["canvas_module_id"])
                for _state_key, entry, _rel_path in _state_items(
                    deployment_state,
                    external_state=store.external,
                )
                if entry.get("canvas_module_id") is not None
            }
        )
        live_by_module: dict[int, list[dict]] = {
            module_id: canvas.list_module_items(module_id)
            for module_id in module_ids
        }
        live_by_key: dict[tuple[int, tuple[str, Any]], dict] = {}
        for module_id, items in live_by_module.items():
            for item in items:
                key = module_item_canvas_key(item)
                if key:
                    live_by_key[(module_id, key)] = item

        operations: list[dict] = []
        blocked: list[dict] = []
        state_updates: list[dict] = []

        for state_key, entry, rel_path in _state_items(deployment_state, external_state=store.external):
            atype = entry.get("canvas_type")
            if atype == "module_header":
                continue
            md_path = repo_root / rel_path
            if not md_path.exists():
                blocked.append({"file": rel_path, "reason": "local Markdown file is missing"})
                continue
            errors = validate_artifact(md_path)
            if errors:
                blocked.append({"file": rel_path, "reason": "; ".join(errors)})
                continue
            frontmatter, _body = parse_frontmatter(md_path)
            desired = completion_requirement_for(frontmatter, str(atype))
            module_id = entry.get("canvas_module_id")
            key = artifact_canvas_key(entry)
            if module_id is None or key is None:
                blocked.append({"file": rel_path, "reason": "state entry lacks Canvas module or content identity"})
                continue
            live_item = live_by_key.get((int(module_id), key))
            if not live_item:
                blocked.append({"file": rel_path, "reason": "matching live module item was not found"})
                continue

            module_item_id = live_item.get("id")
            current = live_item.get("completion_requirement")
            if desired is None and current:
                blocked.append(
                    {
                        "file": rel_path,
                        "reason": (
                            "local completion_requirement is none, but Canvas already has a module "
                            "completion requirement; clear it in Canvas before backfilling state"
                        ),
                    }
                )
                continue
            needs_canvas_update = desired is not None and not same_completion_requirement(current, desired)
            needs_state_update = (
                entry.get("canvas_module_item_id") != module_item_id
                or entry.get("completion_requirement") != completion_requirement_state_value(desired)
            )
            if needs_canvas_update:
                operations.append(
                    {
                        "file": rel_path,
                        "artifact_id": frontmatter.get("artifact_id") or derive_artifact_id(rel_path),
                        "canvas_module_id": module_id,
                        "canvas_module_item_id": module_item_id,
                        "title": frontmatter.get("title"),
                        "current_completion_requirement": current,
                        "completion_requirement": desired,
                    }
                )
            if needs_state_update:
                state_updates.append(
                    {
                        "state_key": state_key,
                        "file": rel_path,
                        "canvas_module_item_id": module_item_id,
                        "completion_requirement": completion_requirement_state_value(desired),
                    }
                )

        return {
            "manifest": _repo_relative(manifest_path),
            "state": str(state_path),
            "course_id": course_id,
            "operations": operations,
            "state_updates": state_updates,
            "blocked": blocked,
        }


def apply_module_completion_plan(
    manifest_path: Path,
    state_dir: Path | None = None,
    *,
    client: CanvasClient | None = None,
) -> dict:
    plan = build_module_completion_plan(manifest_path, state_dir, client=client)
    if plan["blocked"]:
        plan["applied"] = False
        return plan
    canvas = client
    if canvas is None:
        canvas = CanvasClient.from_env(course_id=int(plan["course_id"]))

    for operation in plan["operations"]:
        canvas.update_module_item(
            int(operation["canvas_module_id"]),
            int(operation["canvas_module_item_id"]),
            {"completion_requirement": operation["completion_requirement"]},
        )

    store = CanvasStateStore(manifest_path=manifest_path, repo_root=REPO_ROOT, state_dir=state_dir)
    with store.locked() as (_manifest, deployment_state, state_path):
        artifacts = deployment_state.setdefault("artifacts", {})
        for update in plan["state_updates"]:
            entry = artifacts.get(update["state_key"])
            if not entry:
                continue
            entry["canvas_module_item_id"] = update["canvas_module_item_id"]
            if update["completion_requirement"]:
                entry["completion_requirement"] = update["completion_requirement"]
            else:
                entry.pop("completion_requirement", None)
        store.save(deployment_state, state_path)

    plan["applied"] = True
    return plan


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        manifest = args.manifest.resolve()
        state_dir = args.state_dir.resolve() if args.state_dir else None
        if args.apply:
            result = apply_module_completion_plan(manifest, state_dir)
        else:
            result = build_module_completion_plan(manifest, state_dir)
            result["applied"] = False
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if result.get("blocked") else 0
    except Exception as exc:  # noqa: BLE001 - compact CLI failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

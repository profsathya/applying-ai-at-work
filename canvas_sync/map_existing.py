"""Map existing Canvas module items into external deployment state.

This script is read-only against Canvas. With --apply it writes only the
external state file under --state-dir so hosted progress rows can point at
existing Canvas module item IDs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_enabled
from canvas_sync.schema import parse_frontmatter, validate_artifact, validate_canvas_state
from canvas_sync.state import (
    CanvasStateStore,
    canvas_fingerprint,
    content_hash,
    fetch_canvas_state,
    load_json,
    save_json_atomic,
)


REPO_ROOT = Path(__file__).resolve().parent.parent

CANVAS_TYPE_BY_MODULE_ITEM_TYPE = {
    "Assignment": "assignment",
    "Page": "page",
    "Discussion": "discussion",
    "Quiz": "quiz",
}


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def normalize_title(value: str | None) -> str:
    text = (value or "").lower().replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_explicit_maps(values: list[str] | None) -> dict[str, int]:
    explicit: dict[str, int] = {}
    for value in values or []:
        if "=" not in value:
            raise ValueError(f"--map expects artifact_id=module_item_id, got {value!r}")
        artifact_id, module_item_id = value.split("=", 1)
        artifact_id = artifact_id.strip()
        if not artifact_id:
            raise ValueError(f"--map has an empty artifact_id: {value!r}")
        try:
            explicit[artifact_id] = int(module_item_id.strip())
        except ValueError as exc:
            raise ValueError(f"--map module_item_id must be an integer: {value!r}") from exc
    return explicit


def discover_local_artifacts(manifest_path: Path) -> list[dict]:
    course_dir = manifest_path.parent.parent
    artifacts: list[dict] = []
    for md_path in sorted(course_dir.glob("sprints/sprint-*/*.md")):
        errors = validate_artifact(md_path)
        if errors:
            raise ValueError("; ".join(errors))
        frontmatter, _body = parse_frontmatter(md_path)
        if frontmatter["type"] == "module_header":
            continue
        artifact_id = frontmatter["artifact_id"]
        artifacts.append(
            {
                "artifact_id": artifact_id,
                "file": repo_relative(md_path),
                "path": md_path,
                "title": frontmatter["title"],
                "source_type": frontmatter["type"],
                "frontmatter": frontmatter,
            }
        )
    return artifacts


def discover_live_items(client: CanvasClient) -> list[dict]:
    live_items: list[dict] = []
    for module in client.list_modules():
        module_id = int(module["id"])
        for item in client.list_module_items(module_id):
            item_type = item.get("type")
            canvas_type = CANVAS_TYPE_BY_MODULE_ITEM_TYPE.get(str(item_type))
            if not canvas_type:
                continue
            live_items.append(
                {
                    "module_id": module_id,
                    "module_name": module.get("name"),
                    "module_position": module.get("position"),
                    "module_item_id": int(item["id"]),
                    "position": item.get("position"),
                    "title": item.get("title"),
                    "module_item_type": item_type,
                    "canvas_type": canvas_type,
                    "canvas_id": item.get("content_id") if canvas_type != "page" else None,
                    "canvas_page_url": item.get("page_url") if canvas_type == "page" else None,
                    "completion_requirement": item.get("completion_requirement"),
                }
            )
    return live_items


def state_entry_for_match(local: dict, live: dict, client: CanvasClient) -> dict:
    completion_requirement = live.get("completion_requirement") or {}
    entry: dict[str, Any] = {
        "artifact_id": local["artifact_id"],
        "local_path": local["file"],
        "canvas_type": live["canvas_type"],
        "canvas_id": live.get("canvas_id"),
        "canvas_page_url": live.get("canvas_page_url"),
        "canvas_module_id": live["module_id"],
        "canvas_module_item_id": live["module_item_id"],
        "content_hash": content_hash(local["path"]),
        "last_pushed": None,
    }
    if completion_requirement.get("type"):
        entry["completion_requirement"] = str(completion_requirement["type"])
    if live["canvas_type"] != local["source_type"]:
        entry["source_type"] = local["source_type"]

    live_state = fetch_canvas_state(client, entry)
    fingerprint = canvas_fingerprint(live_state, live["canvas_type"])
    if fingerprint:
        entry["canvas_fingerprint"] = fingerprint
    return entry


def build_mapping_plan(
    manifest_path: Path,
    state_dir: Path,
    *,
    explicit_maps: dict[str, int] | None = None,
    client: CanvasClient | None = None,
) -> dict:
    manifest_path = manifest_path.resolve()
    manifest = load_json(manifest_path)
    course_id = int(manifest.get("instance", {}).get("course_id") or 0)
    if not course_id:
        raise ValueError(f"{manifest_path}: manifest instance.course_id is required")
    if client is None:
        check_instance_enabled(manifest, manifest_label=str(manifest_path))
        check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    canvas = client or CanvasClient.from_env(course_id=course_id)
    local_artifacts = discover_local_artifacts(manifest_path)
    live_items = discover_live_items(canvas)
    explicit = explicit_maps or {}

    live_by_id = {int(item["module_item_id"]): item for item in live_items}
    live_by_title: dict[str, list[dict]] = {}
    for item in live_items:
        live_by_title.setdefault(normalize_title(str(item.get("title") or "")), []).append(item)

    store = CanvasStateStore(manifest_path=manifest_path, repo_root=REPO_ROOT, state_dir=state_dir)
    with store.locked() as (_manifest, deployment_state, state_path):
        existing_artifacts = deployment_state.get("artifacts", {})

    matched: list[dict] = []
    unmatched: list[dict] = []
    ambiguous: list[dict] = []
    blocked: list[dict] = []

    for local in local_artifacts:
        artifact_id = local["artifact_id"]
        source = "title"
        candidates: list[dict]
        if artifact_id in explicit:
            source = "explicit"
            live_item = live_by_id.get(explicit[artifact_id])
            candidates = [live_item] if live_item else []
            if not live_item:
                blocked.append(
                    {
                        "artifact_id": artifact_id,
                        "file": local["file"],
                        "reason": f"explicit module_item_id {explicit[artifact_id]} was not found",
                    }
                )
                continue
        else:
            candidates = live_by_title.get(normalize_title(local["title"]), [])

        if not candidates:
            unmatched.append(
                {
                    "artifact_id": artifact_id,
                    "file": local["file"],
                    "title": local["title"],
                    "source_type": local["source_type"],
                }
            )
            continue
        if len(candidates) > 1:
            ambiguous.append(
                {
                    "artifact_id": artifact_id,
                    "file": local["file"],
                    "title": local["title"],
                    "candidates": [
                        {
                            "module_item_id": item["module_item_id"],
                            "title": item["title"],
                            "module": item["module_name"],
                            "type": item["module_item_type"],
                        }
                        for item in candidates
                    ],
                }
            )
            continue

        live = candidates[0]
        if live["canvas_type"] == "page" and not live.get("canvas_page_url"):
            blocked.append(
                {
                    "artifact_id": artifact_id,
                    "file": local["file"],
                    "reason": "matched Canvas page module item lacks page_url",
                }
            )
            continue
        if live["canvas_type"] != "page" and not live.get("canvas_id"):
            blocked.append(
                {
                    "artifact_id": artifact_id,
                    "file": local["file"],
                    "reason": "matched Canvas module item lacks content_id",
                }
            )
            continue

        entry = state_entry_for_match(local, live, canvas)
        existing = existing_artifacts.get(artifact_id)
        if not existing:
            state_action = "create"
        elif existing.get("canvas_module_item_id") == entry.get("canvas_module_item_id"):
            state_action = "refresh"
        else:
            state_action = "replace"
        matched.append(
            {
                "artifact_id": artifact_id,
                "file": local["file"],
                "title": local["title"],
                "source": source,
                "state_action": state_action,
                "source_type": local["source_type"],
                "canvas_type": entry["canvas_type"],
                "canvas_id": entry.get("canvas_id"),
                "canvas_page_url": entry.get("canvas_page_url"),
                "canvas_module_id": entry["canvas_module_id"],
                "canvas_module_item_id": entry["canvas_module_item_id"],
                "completion_requirement": entry.get("completion_requirement"),
                "entry": entry,
            }
        )

    return {
        "manifest": repo_relative(manifest_path),
        "state": str(store.state_path(manifest)),
        "course_id": course_id,
        "matched": matched,
        "unmatched": unmatched,
        "ambiguous": ambiguous,
        "blocked": blocked,
        "applied": False,
    }


def apply_mapping_plan(manifest_path: Path, state_dir: Path, explicit_maps: dict[str, int]) -> dict:
    plan = build_mapping_plan(manifest_path, state_dir, explicit_maps=explicit_maps)
    if plan["blocked"] or plan["ambiguous"]:
        return plan

    store = CanvasStateStore(manifest_path=manifest_path.resolve(), repo_root=REPO_ROOT, state_dir=state_dir.resolve())
    with store.locked() as (manifest, deployment_state, state_path):
        artifacts = deployment_state.setdefault("artifacts", {})
        for match in plan["matched"]:
            artifacts[match["artifact_id"]] = match["entry"]
        save_json_atomic(state_path, deployment_state)
        errors = validate_canvas_state(state_path)
        if errors:
            raise ValueError("; ".join(errors))
    for match in plan["matched"]:
        match.pop("entry", None)
    plan["applied"] = True
    plan["state"] = str(store.state_path(load_json(manifest_path.resolve())))
    return plan


def _redact_plan(plan: dict) -> dict:
    safe = dict(plan)
    safe["matched"] = [{k: v for k, v in item.items() if k != "entry"} for item in plan["matched"]]
    return safe


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--state-dir", type=Path, required=True)
    parser.add_argument("--map", action="append", dest="maps", help="Explicit artifact_id=module_item_id mapping")
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--dry-run", action="store_true")
    action.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        explicit_maps = parse_explicit_maps(args.maps)
        if args.apply:
            plan = apply_mapping_plan(args.manifest, args.state_dir, explicit_maps)
        else:
            plan = build_mapping_plan(
                args.manifest.resolve(),
                args.state_dir.resolve(),
                explicit_maps=explicit_maps,
            )
        print(json.dumps(_redact_plan(plan), indent=2, sort_keys=True))
        return 1 if plan["blocked"] or plan["ambiguous"] else 0
    except Exception as exc:  # noqa: BLE001 - compact CLI failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

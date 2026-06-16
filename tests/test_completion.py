from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from canvas_sync import completion
from canvas_sync.completion import (
    apply_module_completion_plan,
    build_module_completion_plan,
    completion_requirement_for,
)


def write_page(path: Path, *, completion_requirement: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    completion_line = (
        f"completion_requirement: {completion_requirement}\n"
        if completion_requirement is not None
        else ""
    )
    path.write_text(
        f"""---
type: page
title: "Stable Page"
slug: stable-page
artifact_id: stable-page
sprint: 0
module: "Test Module"
position: 1
points: null
submission_type: none
publish: true
{completion_line}\
---

# Stable Page

Body text.
""",
        encoding="utf-8",
    )


def write_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "instance": {
                    "name": "production",
                    "base_url": "https://example.instructure.com/",
                    "course_id": 12345,
                    "term": "Test Term",
                },
                "last_sync": None,
                "artifacts": {},
            }
        ),
        encoding="utf-8",
    )


def write_state(path: Path, *, completion_requirement: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    artifact = {
        "artifact_id": "stable-page",
        "local_path": "course1/sprints/sprint-0/stable-page.md",
        "canvas_type": "page",
        "canvas_id": 1001,
        "canvas_page_url": "stable-page",
        "canvas_module_id": 55,
        "content_hash": "a" * 64,
        "canvas_fingerprint": "b" * 64,
    }
    if completion_requirement:
        artifact["completion_requirement"] = completion_requirement
    path.write_text(
        json.dumps(
            {
                "instance": {
                    "name": "production",
                    "base_url": "https://example.instructure.com/",
                    "course_id": 12345,
                    "term": "Test Term",
                },
                "last_sync": None,
                "artifacts": {"stable-page": artifact},
            }
        ),
        encoding="utf-8",
    )


class FakeCanvasClient:
    def __init__(self, *, current_completion_requirement: dict | None = None) -> None:
        self.updates: list[tuple[int, int, dict]] = []
        self.current_completion_requirement = current_completion_requirement

    def list_module_items(self, module_id: int) -> list[dict]:
        self.listed_module_id = module_id
        return [
            {
                "id": 9001,
                "module_id": module_id,
                "title": "Stable Page",
                "type": "Page",
                "page_url": "stable-page",
                "completion_requirement": self.current_completion_requirement,
            }
        ]

    def update_module_item(self, module_id: int, module_item_id: int, payload: dict) -> dict:
        self.updates.append((module_id, module_item_id, payload))
        return {"id": module_item_id, **payload}


class CompletionTests(unittest.TestCase):
    def test_default_completion_requirement_derivation(self) -> None:
        self.assertEqual(completion_requirement_for({"type": "page"}, "page"), {"type": "must_view"})
        self.assertEqual(
            completion_requirement_for({"type": "discussion"}, "discussion"),
            {"type": "must_contribute"},
        )
        self.assertEqual(
            completion_requirement_for({"type": "discussion", "delivery_mode": "ai_activity"}, "assignment"),
            {"type": "must_submit"},
        )
        self.assertEqual(
            completion_requirement_for({"completion_requirement": "min_score", "points": 5}, "quiz"),
            {"type": "min_score", "min_score": 5},
        )
        self.assertIsNone(completion_requirement_for({"completion_requirement": "none"}, "page"))

    def test_backfill_plan_and_apply_update_canvas_and_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path)
            write_manifest(manifest_path)
            write_state(state_path)
            client = FakeCanvasClient()

            with patch.object(completion, "REPO_ROOT", repo_root):
                plan = build_module_completion_plan(manifest_path, state_dir, client=client)
                applied = apply_module_completion_plan(manifest_path, state_dir, client=client)

            self.assertEqual(plan["blocked"], [])
            self.assertEqual(plan["operations"][0]["canvas_module_item_id"], 9001)
            self.assertEqual(plan["operations"][0]["completion_requirement"], {"type": "must_view"})
            self.assertEqual(
                client.updates,
                [(55, 9001, {"completion_requirement": {"type": "must_view"}})],
            )
            self.assertTrue(applied["applied"])

            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["stable-page"]
            self.assertEqual(entry["canvas_module_item_id"], 9001)
            self.assertEqual(entry["completion_requirement"], "must_view")

    def test_existing_canvas_requirement_blocks_none_backfill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path, completion_requirement="none")
            write_manifest(manifest_path)
            write_state(state_path, completion_requirement="must_view")
            client = FakeCanvasClient(current_completion_requirement={"type": "must_view"})

            with patch.object(completion, "REPO_ROOT", repo_root):
                plan = build_module_completion_plan(manifest_path, state_dir, client=client)
                applied = apply_module_completion_plan(manifest_path, state_dir, client=client)

            self.assertEqual(plan["operations"], [])
            self.assertEqual(plan["state_updates"], [])
            self.assertEqual(len(plan["blocked"]), 1)
            self.assertIn("completion_requirement is none", plan["blocked"][0]["reason"])
            self.assertFalse(applied["applied"])
            self.assertEqual(client.updates, [])

            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["artifacts"]["stable-page"]["completion_requirement"], "must_view")


if __name__ == "__main__":
    unittest.main()

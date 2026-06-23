from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from canvas_sync import map_existing
from canvas_sync.map_existing import apply_mapping_plan, build_mapping_plan
from canvas_sync.schema import validate_canvas_state


def write_artifact(
    path: Path,
    *,
    artifact_type: str = "page",
    title: str = "Tuple Overview",
    slug: str = "tuple-overview",
    artifact_id: str = "tuple-overview",
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    points = "null" if artifact_type == "page" else "5"
    submission_type = "none" if artifact_type == "page" else "discussion_topic"
    path.write_text(
        f"""---
type: {artifact_type}
title: "{title}"
slug: {slug}
artifact_id: {artifact_id}
sprint: 0
module: "Test Module"
position: 1
points: {points}
submission_type: {submission_type}
publish: false
---

# {title}

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


class FakeCanvasClient:
    def list_modules(self) -> list[dict]:
        return [
            {"id": 55, "position": 1, "name": "Mapped Module", "published": True},
            {"id": 56, "position": 2, "name": "Other Module", "published": True},
        ]

    def list_module_items(self, module_id: int) -> list[dict]:
        if module_id == 55:
            return [
                {
                    "id": 9001,
                    "module_id": 55,
                    "position": 1,
                    "title": "Tuple Overview",
                    "type": "Page",
                    "page_url": "tuple-overview",
                    "completion_requirement": {"type": "must_view"},
                },
                {
                    "id": 9002,
                    "module_id": 55,
                    "position": 2,
                    "title": "Human Connections",
                    "type": "Assignment",
                    "content_id": 1002,
                    "completion_requirement": {"type": "must_submit"},
                },
            ]
        return [
            {
                "id": 9003,
                "module_id": 56,
                "position": 1,
                "title": "Niche Doc Week 2 ",
                "type": "Assignment",
                "content_id": 1003,
                "completion_requirement": {"type": "must_submit"},
            }
        ]

    def get_page(self, page_url: str) -> dict:
        return {
            "page_id": 1001,
            "url": page_url,
            "title": "Tuple Overview",
            "body": "<p>Canvas page body.</p>",
            "published": True,
        }

    def get_assignment(self, assignment_id: int) -> dict:
        titles = {
            1002: "Human Connections",
            1003: "Niche Doc Week 2 ",
        }
        return {
            "id": assignment_id,
            "name": titles[assignment_id],
            "description": "<p>Canvas assignment body.</p>",
            "points_possible": 5,
            "published": True,
        }


class MapExistingTests(unittest.TestCase):
    def test_build_plan_matches_unique_titles_and_records_live_canvas_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_manifest(manifest_path)
            write_artifact(repo_root / "course1" / "sprints" / "sprint-0" / "tuple-overview.md")
            write_artifact(
                repo_root / "course1" / "sprints" / "sprint-0" / "human-connections.md",
                artifact_type="discussion",
                title="Human Connections",
                slug="human-connections",
                artifact_id="human-connections",
            )

            with patch.object(map_existing, "REPO_ROOT", repo_root):
                plan = build_mapping_plan(manifest_path, state_dir, client=FakeCanvasClient())

            self.assertEqual(plan["blocked"], [])
            self.assertEqual(plan["ambiguous"], [])
            self.assertEqual(plan["unmatched"], [])
            by_id = {item["artifact_id"]: item for item in plan["matched"]}
            self.assertEqual(by_id["tuple-overview"]["canvas_type"], "page")
            self.assertEqual(by_id["tuple-overview"]["canvas_module_item_id"], 9001)
            self.assertEqual(by_id["human-connections"]["source_type"], "discussion")
            self.assertEqual(by_id["human-connections"]["canvas_type"], "assignment")
            self.assertEqual(by_id["human-connections"]["completion_requirement"], "must_submit")
            self.assertIn("canvas_fingerprint", by_id["human-connections"]["entry"])

    def test_apply_writes_external_state_with_explicit_map_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_manifest(manifest_path)
            write_artifact(
                repo_root / "course1" / "sprints" / "sprint-1" / "niche-doc-week-2-update.md",
                artifact_type="assignment",
                title="Niche Doc: Week 2 Update",
                slug="niche-doc-week-2-update",
                artifact_id="niche-doc-week-2-update",
            )

            with patch.object(map_existing, "REPO_ROOT", repo_root):
                with patch.object(map_existing.CanvasClient, "from_env", return_value=FakeCanvasClient()):
                    plan = apply_mapping_plan(
                        manifest_path,
                        state_dir,
                        {"niche-doc-week-2-update": 9003},
                    )

            self.assertTrue(plan["applied"])
            self.assertEqual(plan["blocked"], [])
            self.assertEqual(validate_canvas_state(state_path), [])
            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["niche-doc-week-2-update"]
            self.assertEqual(entry["canvas_id"], 1003)
            self.assertEqual(entry["canvas_module_id"], 56)
            self.assertEqual(entry["canvas_module_item_id"], 9003)
            self.assertEqual(entry["completion_requirement"], "must_submit")


if __name__ == "__main__":
    unittest.main()

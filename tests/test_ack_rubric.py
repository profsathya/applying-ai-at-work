"""The rubric warning persists until acknowledged; ack_rubric resolves it.

Full cycle: a publish with a changed rubric warns and does NOT advance the
stored rubric hash; a second publish warns again; running ack_rubric records
the current fingerprint; a third publish is quiet.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from canvas_sync import push
from canvas_sync.ack_rubric import AckRubricError, ack_rubric


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def write_assignment(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: assignment
title: "Tuple Lab"
slug: tuple-lab
artifact_id: tuple-lab
sprint: 99
module: "Module A"
position: 2
points: 10
submission_type: text_entry
publish: false
rubric:
- description: New criterion
  points: 5
---

# Tuple Lab

Assignment body.
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


def write_state(state_path: Path, *, rubric_hash: str) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "instance": {
                    "name": "production",
                    "base_url": "https://example.instructure.com/",
                    "course_id": 12345,
                    "term": "Test Term",
                },
                "last_sync": None,
                "artifacts": {
                    "tuple-lab": {
                        "artifact_id": "tuple-lab",
                        "local_path": "course1/sprints/sprint-99/tuple-lab.md",
                        "canvas_type": "assignment",
                        "canvas_id": 2001,
                        "canvas_page_url": None,
                        "canvas_module_id": 55,
                        "canvas_module_item_id": 9001,
                        "position": 2,
                        "completion_requirement": "must_submit",
                        "content_hash": "5" * 64,
                        "rubric_hash": rubric_hash,
                    }
                },
            }
        ),
        encoding="utf-8",
    )


class QuietClient:
    def update_assignment(self, assignment_id: int, payload: dict) -> dict:
        return {"id": assignment_id, **payload}

    def get_assignment(self, assignment_id: int) -> dict:
        return {
            "id": assignment_id,
            "name": "Tuple Lab",
            "description": "",
            "points_possible": 10,
            "published": False,
            "submission_types": ["online_text_entry"],
        }

    def update_module_item(self, *args: object, **kwargs: object) -> dict:
        return {}


OLD_RUBRIC_HASH = push.rubric_fingerprint(
    {"rubric": [{"description": "Old criterion", "points": 3}]}
)


class AckRubricCycleTests(unittest.TestCase):
    def test_warning_repeats_until_acknowledged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-lab.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_assignment(md_path)
            write_manifest(manifest_path)
            write_state(state_path, rubric_hash=OLD_RUBRIC_HASH)

            def publish() -> dict:
                with chdir(repo_root):
                    with patch.object(push.CanvasClient, "from_env", return_value=QuietClient()):
                        with patch.object(push, "resolve_or_create_module", return_value=55):
                            return push.push_artifact(md_path, manifest_path, state_dir=state_dir)

            # First publish: warns and does NOT advance the stored hash.
            result = publish()
            self.assertIn(push.RUBRIC_WARNING, result.get("warnings", []))
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-lab"]
            self.assertEqual(entry["rubric_hash"], OLD_RUBRIC_HASH)

            # Second publish (content re-edit): warns again.
            md_path.write_text(
                md_path.read_text(encoding="utf-8") + "\nMore body.\n", encoding="utf-8"
            )
            result = publish()
            self.assertIn(push.RUBRIC_WARNING, result.get("warnings", []))

            # Acknowledge after applying the rubric in Canvas by hand.
            summary = ack_rubric(
                "tuple-lab", manifest_path, state_dir=state_dir, repo_root=repo_root
            )
            self.assertEqual(summary["previous_rubric_hash"], OLD_RUBRIC_HASH)
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-lab"]
            self.assertEqual(entry["rubric_hash"], push.rubric_fingerprint(
                {"rubric": [{"description": "New criterion", "points": 5}]}
            ))

            # Third publish: quiet.
            md_path.write_text(
                md_path.read_text(encoding="utf-8") + "\nEven more body.\n", encoding="utf-8"
            )
            result = publish()
            self.assertNotIn("warnings", result)

    def test_ack_requires_existing_state_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-lab.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_assignment(md_path)
            write_manifest(manifest_path)
            state_dir = repo_root / ".canvas-state"
            (state_dir / "course1").mkdir(parents=True, exist_ok=True)
            (state_dir / "course1" / "production.json").write_text(
                json.dumps({"instance": {"name": "production"}, "artifacts": {}}),
                encoding="utf-8",
            )

            with self.assertRaises(AckRubricError):
                ack_rubric("tuple-lab", manifest_path, state_dir=state_dir, repo_root=repo_root)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import os
import re
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from canvas_sync import push
from canvas_sync.hosted_html import iframe_shell, render_hosted_artifact
from canvas_sync.state import state_path_for_manifest


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def write_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: page
title: "Tuple Overview"
slug: tuple-overview
artifact_id: tuple-overview
sprint: 99
module: "Hosted HTML Pilot"
position: 1
points: null
submission_type: none
publish: false
---

# Tuple Overview

Tuples store ordered values that should travel together.

## What to notice

- Tuples keep order.
- Tuples are immutable.
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
                "hosted_html": {
                    "enabled": True,
                    "base_url": "https://profsathya.github.io/Common-Curriculum/deanza",
                    "path_prefix": "deanza",
                },
                "last_sync": None,
                "artifacts": {},
            }
        ),
        encoding="utf-8",
    )


class RecordingCanvasClient:
    def __init__(self) -> None:
        self.page_payload: dict | None = None

    def create_page(self, payload: dict) -> dict:
        self.page_payload = payload
        return {"page_id": 1001, "url": "tuple-overview", **payload}

    def get_page(self, page_url: str) -> dict:
        return {
            "page_id": 1001,
            "url": page_url,
            "title": "Tuple Overview",
            "body": self.page_payload["body"] if self.page_payload else "",
            "published": False,
        }

    def add_module_item(self, module_id: int, **kwargs: object) -> dict:
        return {"id": 9001, "module_id": module_id, **kwargs}


class HostedHtmlTests(unittest.TestCase):
    def test_rendered_page_uses_career_intelligence_structure_and_skips_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path)
            write_manifest(manifest_path)

            first = render_hosted_artifact(md_path, manifest_path, output_dir)
            second = render_hosted_artifact(md_path, manifest_path, output_dir)

            html = Path(first["output_path"]).read_text(encoding="utf-8")
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(first["hosted_hash"], second["hosted_hash"])
            self.assertIn('class="activity"', html)
            self.assertIn("<h2>Learning goal</h2>", html)
            self.assertIn("<section>", html)
            self.assertIn("Submit to Canvas", html)
            self.assertIn("New._CTI_Logo_RGB-1.png", html)
            self.assertIn("Back to Module", html)

    def test_iframe_shell_contains_hosted_url_and_fallback_link(self) -> None:
        shell = iframe_shell("https://example.test/deanza/course1/sprint-99/tuple.html", "Tuple Page")

        self.assertIn("<iframe", shell)
        self.assertIn("https://example.test/deanza/course1/sprint-99/tuple.html?context=canvas", shell)
        self.assertIn("Open hosted page in a new tab", shell)

    def test_push_uses_iframe_shell_and_records_hosted_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            state_dir = repo_root / ".canvas-state"
            output_dir = repo_root / "Common-Curriculum"
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_page(md_path)
            write_manifest(manifest_path)
            client = RecordingCanvasClient()

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(
                            md_path,
                            manifest_path,
                            state_dir=state_dir,
                            hosted_output_dir=output_dir,
                        )

            self.assertEqual(result["hosted_url"], "https://profsathya.github.io/Common-Curriculum/deanza/course1/sprint-99/tuple-overview.html")
            self.assertIsNotNone(client.page_payload)
            self.assertFalse(client.page_payload["published"])
            self.assertIn("<iframe", client.page_payload["body"])

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["tuple-overview"]
            self.assertEqual(entry["hosted_path"], "course1/sprint-99/tuple-overview.html")
            self.assertEqual(entry["hosted_url"], result["hosted_url"])
            self.assertRegex(entry["hosted_hash"], re.compile(r"^[a-f0-9]{64}$"))

    def test_assignment_discussion_and_quiz_keep_canvas_native_metadata(self) -> None:
        class PayloadClient:
            def __init__(self) -> None:
                self.quiz_questions: list[dict] = []

            def create_assignment(self, payload: dict) -> dict:
                return {"id": 1, **payload}

            def create_discussion(self, payload: dict) -> dict:
                return {"id": 2, **payload}

            def create_quiz(self, payload: dict) -> dict:
                return {"id": 3, **payload}

            def add_quiz_question(self, quiz_id: int, payload: dict) -> dict:
                self.quiz_questions.append({"quiz_id": quiz_id, **payload})
                return payload

        client = PayloadClient()
        shell = iframe_shell("https://example.test/page.html", "Hosted")
        assignment = push.push_assignment(
            client,
            {"title": "Assignment", "points": 10, "submission_type": "text_entry", "publish": False},
            shell,
            None,
        )
        discussion = push.push_discussion(
            client,
            {"title": "Discussion", "points": 5, "publish": False},
            shell,
            None,
        )
        quiz = push.push_quiz(
            client,
            {
                "title": "Quiz",
                "points": 4,
                "submission_type": "online_quiz",
                "publish": False,
                "questions": [
                    {
                        "type": "true_false",
                        "prompt": "Tuples are immutable.",
                        "points": 1,
                        "answers": [
                            {"text": "True", "correct": True},
                            {"text": "False", "correct": False},
                        ],
                    }
                ],
            },
            shell,
            None,
        )

        self.assertEqual(assignment["submission_types"], ["online_text_entry"])
        self.assertEqual(assignment["points_possible"], 10)
        self.assertFalse(assignment["published"])
        self.assertIn("<iframe", assignment["description"])
        self.assertEqual(discussion["assignment"]["points_possible"], 5)
        self.assertFalse(discussion["published"])
        self.assertIn("<iframe", discussion["message"])
        self.assertEqual(quiz["points_possible"], 4)
        self.assertFalse(quiz["published"])
        self.assertIn("<iframe", quiz["description"])
        self.assertEqual(client.quiz_questions[0]["question_type"], "true_false_question")


if __name__ == "__main__":
    unittest.main()

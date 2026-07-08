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
from canvas_sync.hosted_html import (
    iframe_shell,
    render_hosted_artifact,
    render_hosted_files,
    validate_homepage_metadata,
)
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


def write_ai_discussion(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: discussion
title: "Tuple AI Discussion"
slug: tuple-ai-discussion
artifact_id: tuple-ai-discussion
sprint: 99
module: "Hosted HTML Pilot"
position: 2
points: 10
submission_type: file_upload
delivery_mode: ai_activity
publish: false
ai_activity:
  activity_id: deanza-course1-tuple-ai-discussion
  title: "Tuple AI Discussion"
  description: "Use AI follow-up questions to sharpen a tuple design."
  questions:
    - id: q1
      type: ai-discussion
      prompt: "Describe one work record that could be represented as a tuple."
      placeholder: "Name the record, the tuple values, and the tradeoff."
      minLength: 40
      numQuestions: 2
      aiContext: "Push for concrete tuple structure and maintainability."
---

# Tuple AI Discussion

Use the activity to test whether your tuple example is specific enough for another person to maintain.
""",
        encoding="utf-8",
    )


def write_second_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: page
title: "Second Overview"
slug: second-overview
artifact_id: second-overview
sprint: 99
module: "Hosted HTML Pilot"
position: 2
points: null
submission_type: none
publish: false
---

# Second Overview

A second page for homepage index checks.
""",
        encoding="utf-8",
    )


def write_third_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: page
title: "Third Overview"
slug: third-overview
artifact_id: third-overview
sprint: 100
module: "Second Hosted Module"
position: 1
points: null
submission_type: none
publish: false
---

# Third Overview

A third page in a new sprint for homepage index checks.
""",
        encoding="utf-8",
    )


def write_homepage(path: Path, *, body: str | None = None) -> None:
    path.write_text(
        body
        or """course:
  title: "Hosted HTML Pilot"
  lead: "A compact homepage for the hosted pilot."
  footer: "Computing Talent Initiative - Test"
modules:
  - sprint: 99
    tag: "Pilot"
    open: true
    learning_goals:
      - "Understand the hosted pilot."
      - "Use the generated links."
    prereq: "Start here."
    groups:
      - label: "Start here"
        items:
          - slug: "tuple-overview"
            meta: "Page - read first"
            badge: "Self-check"
            selfcheck: true
            verify: "Ask a peer to confirm the tuple example is concrete."
""",
        encoding="utf-8",
    )


def write_manifest(path: Path, artifacts: dict | None = None) -> None:
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
                "artifacts": artifacts or {},
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
            self.assertEqual(first["hosted_path"], "course1/activities/tuple-overview.html")
            self.assertTrue(first["output_path"].endswith("deanza/course1/activities/tuple-overview.html"))
            self.assertTrue(first["changed"])
            self.assertFalse(second["changed"])
            self.assertEqual(first["hosted_hash"], second["hosted_hash"])
            self.assertIn('class="activity"', html)
            self.assertIn("<h2>Learning goal</h2>", html)
            self.assertIn("<section>", html)
            self.assertIn("What counts as done", html)
            self.assertIn("No Canvas submission is required for this information page.", html)
            self.assertNotIn("Submit to Canvas", html)
            self.assertNotIn("Open the Canvas page", html)
            self.assertIn("New._CTI_Logo_RGB-1.png", html)
            self.assertIn("Back to Module", html)
            self.assertIn('href="../sprint-99.html?context=web"', html)

    def test_rendered_indexes_follow_common_curriculum_course_structure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path)
            write_homepage(repo_root / "course1" / "homepage.yaml")
            write_manifest(manifest_path)
            state = {
                "artifacts": {
                    "tuple-overview": {
                        "artifact_id": "tuple-overview",
                        "local_path": "course1/sprints/sprint-99/tuple-overview.md",
                        "canvas_type": "page",
                    "canvas_id": 1001,
                    "canvas_page_url": "tuple-overview",
                    "canvas_module_id": 55,
                    "canvas_module_item_id": 9001,
                    "completion_requirement": "must_view",
                    "content_hash": "a" * 64,
                }
            }
            }

            result = render_hosted_files(manifest_path, output_dir, [md_path], state=state)

            sprint_index = output_dir / "deanza" / "course1" / "sprint-99.html"
            course_index = output_dir / "deanza" / "course1" / "index.html"
            course_home = output_dir / "deanza" / "course1" / "home.html"
            progress_map = output_dir / "deanza" / "course1" / "progress-map.json"
            self.assertTrue(sprint_index.exists())
            self.assertTrue(course_index.exists())
            self.assertTrue(course_home.exists())
            self.assertTrue(progress_map.exists())
            self.assertEqual(result["indexes"][0]["path"], str(sprint_index))
            sprint_html = sprint_index.read_text(encoding="utf-8")
            home_html = course_home.read_text(encoding="utf-8")
            self.assertIn('class="course-header"', home_html)
            self.assertIn('class="module"', home_html)
            self.assertIn("Module Learning Goals", home_html)
            self.assertIn("Start here", home_html)
            self.assertIn("New._CTI_Logo_RGB-1.png", home_html)
            self.assertIn("data-canvas-href", home_html)
            self.assertIn('data-progress-id="tuple-overview"', home_html)
            self.assertIn('data-canvas-module-item-id="9001"', home_html)
            self.assertIn("canvas-progress", home_html)
            self.assertIn("Ask a peer to confirm the tuple example is concrete.", home_html)
            self.assertIn("activities/tuple-overview.html?context=web", sprint_html)
            self.assertIn("activities/tuple-overview.html?context=web", course_index.read_text(encoding="utf-8"))
            progress_data = json.loads(progress_map.read_text(encoding="utf-8"))
            self.assertEqual(progress_data["items"][0]["artifactId"], "tuple-overview")
            self.assertEqual(progress_data["items"][0]["canvasModuleItemId"], 9001)

    def test_homepage_yaml_can_override_item_icon_and_web_href(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            homepage_path = repo_root / "course1" / "homepage.yaml"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path)
            write_manifest(manifest_path)
            write_homepage(
                homepage_path,
                body="""modules:
  - sprint: 99
    groups:
      - label: "Start here"
        items:
          - slug: "tuple-overview"
            icon: "presentation"
            href: "../legacy/tuple-overview.html"
""",
            )

            render_hosted_files(manifest_path, output_dir, [md_path])

            home_html = (output_dir / "deanza" / "course1" / "home.html").read_text(encoding="utf-8")
            self.assertIn('href="../legacy/tuple-overview.html"', home_html)
            self.assertIn('<rect x="3" y="4" width="18" height="14" rx="2"/>', home_html)

    def test_hosted_homepage_renders_from_frontmatter_without_homepage_yaml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            first_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            second_path = repo_root / "course1" / "sprints" / "sprint-99" / "second-overview.md"
            third_path = repo_root / "course1" / "sprints" / "sprint-100" / "third-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(first_path)
            write_second_page(second_path)
            write_third_page(third_path)
            write_manifest(manifest_path)

            result = render_hosted_files(manifest_path, output_dir, [first_path, second_path, third_path])

            course_home = output_dir / "deanza" / "course1" / "home.html"
            sprint_99 = output_dir / "deanza" / "course1" / "sprint-99.html"
            sprint_100 = output_dir / "deanza" / "course1" / "sprint-100.html"
            progress_map = output_dir / "deanza" / "course1" / "progress-map.json"
            home_html = course_home.read_text(encoding="utf-8")
            self.assertTrue(sprint_99.exists())
            self.assertTrue(sprint_100.exists())
            self.assertTrue(progress_map.exists())
            self.assertIn("Hosted HTML Pilot", home_html)
            self.assertIn("Second Hosted Module", home_html)
            self.assertIn("Additional items", home_html)
            self.assertIn("tuple-overview.html?context=web", home_html)
            self.assertIn("second-overview.html?context=web", home_html)
            self.assertIn("third-overview.html?context=web", home_html)
            self.assertNotIn('data-progress-id="tuple-overview"', home_html)
            self.assertNotIn('class="progress-check"', home_html)
            self.assertIn("canvas-progress", home_html)
            self.assertIn(str(sprint_100), [item["path"] for item in result["indexes"]])
            progress_data = json.loads(progress_map.read_text(encoding="utf-8"))
            self.assertEqual(
                [item["artifactId"] for item in progress_data["items"]],
                ["tuple-overview", "second-overview", "third-overview"],
            )

    def test_homepage_indexes_add_and_remove_artifact_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            first_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            second_path = repo_root / "course1" / "sprints" / "sprint-99" / "second-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(first_path)
            write_second_page(second_path)
            write_homepage(repo_root / "course1" / "homepage.yaml")
            write_manifest(manifest_path)

            render_hosted_files(manifest_path, output_dir, [first_path, second_path])
            home_path = output_dir / "deanza" / "course1" / "home.html"
            home_html = home_path.read_text(encoding="utf-8")
            self.assertIn("second-overview.html?context=web", home_html)
            self.assertIn("Additional items", home_html)

            second_path.unlink()
            render_hosted_files(manifest_path, output_dir, [first_path])
            self.assertNotIn("second-overview.html?context=web", home_path.read_text(encoding="utf-8"))

    def test_homepage_yaml_can_override_course_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            homepage_path = repo_root / "course1" / "homepage.yaml"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path)
            write_manifest(manifest_path)
            write_homepage(
                homepage_path,
                body="""course:
  title: "Custom Hosted Course"
  lead: "Curated course copy without item-level grouping."
""",
            )

            errors = validate_homepage_metadata(repo_root / "course1")
            render_hosted_files(manifest_path, output_dir, [md_path])

            home_html = (output_dir / "deanza" / "course1" / "home.html").read_text(encoding="utf-8")
            self.assertEqual(errors, [])
            self.assertIn("Custom Hosted Course", home_html)
            self.assertIn("Curated course copy without item-level grouping.", home_html)
            self.assertIn("tuple-overview.html?context=web", home_html)

    def test_homepage_validation_rejects_stale_and_duplicate_slugs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            homepage_path = repo_root / "course1" / "homepage.yaml"
            write_page(md_path)
            write_homepage(
                homepage_path,
                body="""course:
  title: "Hosted HTML Pilot"
modules:
  - sprint: 99
    groups:
      - label: "Broken"
        items:
          - slug: "tuple-overview"
            icon: "not-an-icon"
          - slug: "tuple-overview"
          - slug: "missing-page"
""",
            )

            errors = validate_homepage_metadata(repo_root / "course1")

            self.assertTrue(any("duplicates slug 'tuple-overview'" in error for error in errors))
            self.assertTrue(any("references missing artifact slug 'missing-page'" in error for error in errors))
            self.assertTrue(any("unsupported icon 'not-an-icon'" in error for error in errors))

    def test_ai_activity_renders_wrapper_shell_and_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-ai-discussion.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_ai_discussion(md_path)
            write_manifest(manifest_path)

            result = render_hosted_artifact(md_path, manifest_path, output_dir)

            wrapper = output_dir / "deanza" / "course1" / "assignments" / "tuple-ai-discussion.html"
            shell = output_dir / "deanza" / "course1" / "activities" / "tuple-ai-discussion.html"
            config = output_dir / "activities" / "deanza" / "course1" / "tuple-ai-discussion.json"
            self.assertEqual(result["hosted_path"], "course1/assignments/tuple-ai-discussion.html")
            self.assertEqual(result["activity_hosted_path"], "course1/activities/tuple-ai-discussion.html")
            self.assertEqual(result["config_path"], "activities/deanza/course1/tuple-ai-discussion.json")
            self.assertTrue(wrapper.exists())
            self.assertTrue(shell.exists())
            self.assertTrue(config.exists())
            self.assertIn("../activities/tuple-ai-discussion.html?context=web", wrapper.read_text(encoding="utf-8"))
            self.assertIn("../../../js/activity-engine.js", shell.read_text(encoding="utf-8"))
            self.assertIn("../../../activities/deanza/course1/tuple-ai-discussion.json", shell.read_text(encoding="utf-8"))
            config_data = json.loads(config.read_text(encoding="utf-8"))
            self.assertEqual(config_data["activityId"], "deanza-course1-tuple-ai-discussion")
            self.assertEqual(config_data["settings"]["exportMode"], "json")
            self.assertEqual(
                config_data["settings"]["aiEndpoint"],
                "https://ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy",
            )
            self.assertEqual(config_data["questions"][0]["type"], "ai-discussion")

    def test_iframe_shell_contains_hosted_url_and_fallback_link(self) -> None:
        shell = iframe_shell("https://example.test/deanza/course1/activities/tuple.html", "Tuple Page")

        self.assertIn("<iframe", shell)
        self.assertIn("https://example.test/deanza/course1/activities/tuple.html?context=canvas", shell)
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

            self.assertEqual(result["hosted_url"], "https://profsathya.github.io/Common-Curriculum/deanza/course1/activities/tuple-overview.html")
            self.assertIsNotNone(client.page_payload)
            self.assertFalse(client.page_payload["published"])
            self.assertIn("<iframe", client.page_payload["body"])

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["tuple-overview"]
            self.assertEqual(entry["hosted_path"], "course1/activities/tuple-overview.html")
            self.assertEqual(entry["hosted_url"], result["hosted_url"])
            self.assertRegex(entry["hosted_hash"], re.compile(r"^[a-f0-9]{64}$"))
            self.assertTrue((output_dir / "deanza" / "course1" / "home.html").exists())
            self.assertTrue((output_dir / "deanza" / "course1" / "sprint-99.html").exists())

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

    def test_ai_activity_discussion_pushes_canvas_assignment_shell(self) -> None:
        class AiActivityClient:
            def __init__(self) -> None:
                self.assignment_payload: dict | None = None
                self.module_item: dict | None = None

            def create_assignment(self, payload: dict) -> dict:
                self.assignment_payload = payload
                return {"id": 77, **payload}

            def get_assignment(self, assignment_id: int) -> dict:
                return {
                    "id": assignment_id,
                    "name": "Tuple AI Discussion",
                    "description": self.assignment_payload["description"] if self.assignment_payload else "",
                    "points_possible": 10,
                    "submission_types": ["online_upload"],
                    "published": False,
                }

            def create_discussion(self, payload: dict) -> dict:
                raise AssertionError("AI activity should not create a Canvas discussion")

            def create_quiz(self, payload: dict) -> dict:
                raise AssertionError("AI activity should not create a Canvas quiz")

            def add_module_item(self, module_id: int, **kwargs: object) -> dict:
                self.module_item = {"id": 9001, "module_id": module_id, **kwargs}
                return self.module_item

        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            state_dir = repo_root / ".canvas-state"
            output_dir = repo_root / "Common-Curriculum"
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-ai-discussion.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_ai_discussion(md_path)
            write_manifest(manifest_path)
            client = AiActivityClient()

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(
                            md_path,
                            manifest_path,
                            state_dir=state_dir,
                            hosted_output_dir=output_dir,
                        )

            self.assertEqual(result["canvas_id"], 77)
            self.assertEqual(
                result["hosted_url"],
                "https://profsathya.github.io/Common-Curriculum/deanza/course1/assignments/tuple-ai-discussion.html",
            )
            self.assertIsNotNone(client.assignment_payload)
            self.assertEqual(client.assignment_payload["submission_types"], ["online_upload"])
            self.assertIn("<iframe", client.assignment_payload["description"])
            self.assertEqual(client.module_item["content_type"], "Assignment")

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["tuple-ai-discussion"]
            self.assertEqual(entry["canvas_type"], "assignment")
            self.assertEqual(entry["source_type"], "discussion")
            self.assertEqual(entry["delivery_mode"], "ai_activity")
            self.assertEqual(entry["hosted_path"], "course1/assignments/tuple-ai-discussion.html")
            self.assertTrue((output_dir / "activities" / "deanza" / "course1" / "tuple-ai-discussion.json").exists())

    def test_ai_activity_existing_native_canvas_type_blocks_migration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            rel_path = "course1/sprints/sprint-99/tuple-ai-discussion.md"
            md_path = repo_root / rel_path
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_ai_discussion(md_path)
            write_manifest(
                manifest_path,
                artifacts={
                    rel_path: {
                        "canvas_type": "discussion",
                        "canvas_id": 44,
                        "canvas_page_url": None,
                        "canvas_module_id": 55,
                        "content_hash": "a" * 64,
                    }
                },
            )

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=object()):
                    with self.assertRaisesRegex(ValueError, "remove-canvas workflow"):
                        push.push_artifact(md_path, manifest_path)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import yaml

from canvas_sync import publish_changed, push
from canvas_sync.schema import parse_frontmatter, validate_canvas_state
from tests.test_canvas_state import chdir
from tests.test_publish_changed import write_manifest, write_page_with_id


class MemoryCanvas:
    def _request(self, method, path):
        return {"position": 1, "quiz_submissions": []}

    def __init__(self):
        self.pages = {}
        self.quiz = {}
        self.questions = []
        self.page_creates = 0
        self.page_updates = 0
        self.quiz_creates = 0
        self.fail_question = False

    def create_page(self, payload):
        self.page_creates += 1
        url = f"page-{self.page_creates}"
        self.pages[url] = {"page_id": self.page_creates, "url": url, **payload}
        return self.pages[url]

    def update_page(self, url, payload):
        self.page_updates += 1
        self.pages[url].update(payload)
        return self.pages[url]

    def get_page(self, url):
        return dict(self.pages[url])

    def add_module_item(self, module_id, **kwargs):
        return {"id": 100 + self.page_creates, "module_id": module_id}

    def update_module_item(self, *args):
        return {}

    def create_quiz(self, payload):
        self.quiz_creates += 1
        self.quiz = {"id": 700, **payload}
        return self.quiz

    def update_quiz(self, quiz_id, payload):
        self.quiz.update(payload)
        return self.quiz

    def get_quiz(self, quiz_id):
        return dict(self.quiz)

    def list_quiz_questions(self, quiz_id):
        return list(self.questions)

    def add_quiz_question(self, quiz_id, payload):
        if self.fail_question:
            raise RuntimeError("question creation failed")
        self.questions.append({"id": len(self.questions) + 1, **payload})

    def delete_quiz_question(self, quiz_id, question_id):
        self.questions = [q for q in self.questions if q["id"] != question_id]


class PublishRecoveryTests(unittest.TestCase):
    def test_native_quiz_publishes_complete_questions_without_notifications(self):
        client = Mock()
        client.create_quiz.return_value = {"id": 701, "published": False}
        client.update_quiz.return_value = {"id": 701, "published": True}
        fm = {
            "title": "Test quiz", "publish": True, "points": 1,
            "questions": [{"type": "essay", "prompt": "Explain.", "points": 1}],
        }
        result = push.push_quiz(client, fm, "Instructions", None)
        calls = client.mock_calls
        self.assertFalse(client.create_quiz.call_args.args[0]["published"])
        self.assertEqual([c[0] for c in calls], ["create_quiz", "add_quiz_question", "update_quiz"])
        self.assertEqual(client.update_quiz.call_args.args[1], {
            "published": True, "notify_of_update": False,
        })
        self.assertTrue(result["published"])

    def test_question_failure_does_not_publish_partial_quiz(self):
        client = Mock()
        client.create_quiz.return_value = {"id": 701, "published": False}
        client.add_quiz_question.side_effect = RuntimeError("question rejected")
        fm = {"title": "Test quiz", "publish": True, "questions": [{"prompt": "Explain.", "type": "essay"}]}
        with self.assertRaisesRegex(RuntimeError, "question rejected"):
            push.push_quiz(client, fm, "Instructions", None)
        client.update_quiz.assert_not_called()

    def test_quiz_update_suppresses_notification_and_publishes_after_replacement(self):
        client = Mock()
        client.update_quiz.return_value = {"id": 701}
        client.list_quiz_questions.return_value = [{"id": 1}]
        client._request.return_value = {"quiz_submissions": []}
        fm = {"title": "Test quiz", "publish": True, "questions": [{"prompt": "New?", "type": "essay"}]}
        push.push_quiz(client, fm, "Instructions", 701)
        self.assertEqual([c[0] for c in client.mock_calls], [
            "list_quiz_questions", "_request", "update_quiz", "delete_quiz_question",
            "add_quiz_question", "update_quiz",
        ])
        for call in client.update_quiz.call_args_list:
            self.assertFalse(call.args[1]["notify_of_update"])
        self.assertNotIn("published", client.update_quiz.call_args_list[0].args[1])

    def test_batch_renders_course_once_and_repeat_or_body_edit_does_not_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            manifest = root / "course1/manifests/production.json"
            state_dir = root / ".canvas-state"
            state_path = state_dir / "course1/production.json"
            output = root / "hosted"
            write_manifest(manifest, hosted=True)
            for slug in ["first-page", "second-page"]:
                write_page_with_id(
                    root / f"course1/sprints/sprint-0/{slug}.md", slug, slug, slug
                )
            state_path.parent.mkdir(parents=True)
            state_path.write_text(
                json.dumps(
                    {
                        "instance": json.loads(manifest.read_text())["instance"],
                        "artifacts": {},
                    }
                )
            )
            client = MemoryCanvas()
            with (
                chdir(root),
                patch.object(publish_changed, "REPO_ROOT", root),
                patch.object(push.CanvasClient, "from_env", return_value=client),
                patch.object(push, "resolve_or_create_module", return_value=55),
                patch.object(
                    push, "render_hosted_files", wraps=push.render_hosted_files
                ) as inner,
                patch.object(
                    publish_changed,
                    "render_hosted_files",
                    wraps=publish_changed.render_hosted_files,
                ) as full,
            ):

                def run():
                    return publish_changed.publish_manifest(
                        manifest,
                        state_dir,
                        dry_run=False,
                        check_drift=True,
                        require_state=True,
                        hosted_output_dir=output,
                    )

                result = run()
                self.assertEqual(result["failed"], [])
                self.assertEqual(len(result["published"]), 2)
                self.assertEqual(inner.call_count, 0)
                self.assertEqual(full.call_count, 1)
                self.assertEqual(client.page_creates, 2)
                self.assertEqual(run()["published"], [])
                path = root / "course1/sprints/sprint-0/first-page.md"
                path.write_text(path.read_text() + "\nImproved evidence.\n")
                result = run()
                self.assertEqual(result["published"][0]["action"], "content_update")
                self.assertEqual(client.page_creates, 2)
                self.assertEqual(client.page_updates, 0)
                rendered = output / "deanza/course1/activities/first-page.html"
                self.assertIn("Improved evidence.", rendered.read_text())
                self.assertEqual(validate_canvas_state(state_path), [])
                renamed = path.with_name("renamed-source.md")
                path.rename(renamed)
                result = run()
                self.assertEqual(result["published"][0]["action"], "content_update")
                self.assertEqual(client.page_creates, 2)
                saved = json.loads(state_path.read_text())["artifacts"]["first-page"]
                self.assertEqual(
                    saved["local_path"], renamed.relative_to(root).as_posix()
                )

    def test_quiz_question_failure_preserves_identity_for_explicit_retry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            manifest = root / "course1/manifests/production.json"
            path = root / "course1/sprints/sprint-0/native-quiz.md"
            state_dir = root / ".canvas-state"
            write_manifest(manifest)
            write_page_with_id(path, "native-quiz", "Native Quiz", "native-quiz")
            fm, body = parse_frontmatter(path)
            fm.update(
                type="quiz",
                points=1,
                submission_type="online_quiz",
                questions=[
                    {"type": "essay", "prompt": "Explain your evidence.", "points": 1}
                ],
            )
            path.write_text("---\n" + yaml.safe_dump(fm) + "---\n\n" + body)
            client = MemoryCanvas()
            client.fail_question = True
            with (
                chdir(root),
                patch.object(push.CanvasClient, "from_env", return_value=client),
                patch.object(push, "resolve_or_create_module", return_value=55),
            ):
                with self.assertRaisesRegex(RuntimeError, "question creation failed"):
                    push.push_artifact(path, manifest, state_dir=state_dir)
                state_path = state_dir / "course1/production.json"
                saved = json.loads(state_path.read_text())["artifacts"]["native-quiz"]
                self.assertEqual(saved["canvas_id"], 700)
                self.assertEqual(saved["content_hash"], push.PROVISIONAL_CONTENT_HASH)
                client.fail_question = False
                result = push.push_artifact(path, manifest, state_dir=state_dir)
                self.assertEqual(result["action"], "updated")
                self.assertEqual(client.quiz_creates, 1)
                self.assertEqual(len(client.questions), 1)
                self.assertEqual(client.questions[0]["question_type"], "essay_question")
                self.assertEqual(validate_canvas_state(state_path), [])

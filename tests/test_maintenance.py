from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import yaml

from canvas_sync import inspect_canvas, pull, remove, update_artifact
from canvas_sync.drift import compute_drift
from canvas_sync.hosted_html import (
    artifact_hosted_info,
    iframe_shell,
    markdown_body_to_html,
)
from canvas_sync.maintenance_state import MaintenanceState
from canvas_sync.publish_targets import resolve_targets
from canvas_sync.schema import parse_frontmatter, validate_canvas_state
from canvas_sync.state import canvas_fingerprint, content_hash
from tests.test_publish_changed import write_manifest, write_page


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.manifest_path = self.root / "course1/manifests/production.json"
        self.path = self.root / "course1/sprints/sprint-0/stable-page.md"
        self.rel = self.path.relative_to(self.root).as_posix()
        self.state_dir = self.root / ".canvas-state"
        self.state_path = self.state_dir / "course1/production.json"
        write_manifest(self.manifest_path)
        write_page(self.path, body="- One\n- Two\n\n**Judgment** matters.")
        fm, body = parse_frontmatter(self.path)
        self.live = {
            "page_id": 1001,
            "url": "stable-page",
            "title": fm["title"],
            "body": markdown_body_to_html(body),
            "published": True,
        }
        self.entry = {
            "artifact_id": "stable-page",
            "local_path": self.rel,
            "canvas_type": "page",
            "canvas_id": 1001,
            "canvas_page_url": "stable-page",
            "canvas_module_id": 55,
            "canvas_module_item_id": 9001,
            "content_hash": content_hash(self.path),
            "canvas_fingerprint": canvas_fingerprint(self.live, "page"),
        }
        self.client = Mock()
        self.client.get_page.side_effect = lambda url: dict(self.live)
        self.client.list_modules.return_value = [
            {"id": 55, "name": "Test Module", "position": 1, "published": True}
        ]
        self.client.list_module_items.return_value = [
            {
                "id": 9001,
                "type": "Page",
                "title": fm["title"],
                "page_url": "stable-page",
                "position": 1,
                "published": True,
            }
        ]
        self.save_state()

    def save_state(self):
        config = json.loads(self.manifest_path.read_text())
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        self.state_path.write_text(
            json.dumps(
                {
                    "instance": config["instance"],
                    "artifacts": {"stable-page": self.entry},
                }
            )
        )

    def run_reconcile(self, **kwargs):
        return pull.reconcile(
            self.manifest_path,
            state_dir=self.state_dir,
            repo_root=self.root,
            client=self.client,
            **kwargs,
        )

    def hosted(self):
        config = json.loads(self.manifest_path.read_text())
        config["hosted_html"] = {
            "enabled": True,
            "base_url": "https://example.test/deanza",
            "path_prefix": "deanza",
        }
        self.manifest_path.write_text(json.dumps(config))
        info = artifact_hosted_info(self.path, self.manifest_path, config)
        self.live["body"] = iframe_shell(info["hosted_url"], self.live["title"])
        self.entry["canvas_fingerprint"] = canvas_fingerprint(self.live, "page")
        self.save_state()

    def test_external_state_is_authoritative_and_follows_stable_id_after_rename(self):
        config = json.loads(self.manifest_path.read_text())
        config["artifacts"] = {"course1/sprints/sprint-0/old.md": {"canvas_id": 999}}
        self.manifest_path.write_text(json.dumps(config))
        renamed = self.path.with_name("renamed.md")
        self.path.rename(renamed)
        store = MaintenanceState(self.manifest_path, self.root, self.state_dir)
        view = store.load()
        self.assertEqual(
            list(view["artifacts"]), [renamed.relative_to(self.root).as_posix()]
        )
        self.assertEqual(next(iter(view["artifacts"].values()))["canvas_id"], 1001)
        original = self.manifest_path.read_bytes()
        store.save(view)
        self.assertEqual(self.manifest_path.read_bytes(), original)
        self.assertEqual(validate_canvas_state(self.state_path), [])

    def test_missing_external_state_and_wrong_instance_fail_closed(self):
        data = json.loads(self.state_path.read_text())
        data["instance"]["course_id"] = 999
        self.state_path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "course_id"):
            self.run_reconcile()
        self.client.get_page.assert_not_called()
        self.state_path.unlink()
        with self.assertRaises(FileNotFoundError):
            self.run_reconcile()

    def test_native_roundtrip_is_a_noop(self):
        original = self.path.read_bytes()
        report = self.run_reconcile()
        self.assertEqual(report["report"], [])
        self.assertEqual(report["blocked"], [])
        self.assertEqual(self.path.read_bytes(), original)

    def test_native_apply_has_backup_validation_and_fresh_state(self):
        original = self.path.read_bytes()
        manifest_before = self.manifest_path.read_bytes()
        self.live.update(title="A clearer title", body="<p>Changed in Canvas.</p>")
        report = self.run_reconcile()
        applied = self.run_reconcile(
            apply=True, confirm_token=report["confirmation_token"]
        )
        self.assertEqual(applied["applied"], [self.rel])
        self.assertEqual(
            (Path(applied["backup_dir"]) / self.rel).read_bytes(), original
        )
        self.assertEqual(parse_frontmatter(self.path)[0]["title"], "A clearer title")
        self.assertEqual(self.run_reconcile()["report"], [])
        state = json.loads(self.state_path.read_text())["artifacts"]["stable-page"]
        self.assertEqual(state["content_hash"], content_hash(self.path))
        self.assertEqual(
            state["canvas_fingerprint"], canvas_fingerprint(self.live, "page")
        )
        self.assertEqual(self.manifest_path.read_bytes(), manifest_before)
        self.assertEqual(validate_canvas_state(self.state_path), [])

    def test_stale_token_and_invalid_canvas_text_never_overwrite_source(self):
        original = self.path.read_bytes()
        self.live["title"] = "Changed title"
        report = self.run_reconcile()
        self.live["title"] = "Changed again"
        with self.assertRaisesRegex(ValueError, "confirm-token"):
            self.run_reconcile(apply=True, confirm_token=report["confirmation_token"])
        self.assertEqual(self.path.read_bytes(), original)
        self.live["body"] = "<p>Invalid source: \u2014</p>"
        report = self.run_reconcile()
        self.assertTrue(report["blocked"])
        with self.assertRaisesRegex(ValueError, "blocked"):
            self.run_reconcile(apply=True, confirm_token=report["confirmation_token"])
        self.assertEqual(self.path.read_bytes(), original)

    def test_local_changes_are_not_canvas_drift_and_conflicts_are_blocked(self):
        self.path.write_text(self.path.read_text() + "\nLocal edit.\n")
        self.assertEqual(self.run_reconcile()["local_changes"], [self.rel])
        self.live["title"] = "Concurrent Canvas edit"
        report = self.run_reconcile()
        self.assertIn("Local source also differs", report["blocked"][0]["reason"])

    def test_hosted_shell_is_not_source_and_wrong_iframe_is_detected(self):
        self.hosted()
        original = self.path.read_bytes()
        self.assertEqual(self.run_reconcile()["report"], [])
        # The fallback link remains correct; html2text alone cannot see this edit.
        self.live["body"] = self.live["body"].replace(
            'src="https://example.test/', 'src="https://wrong.test/'
        )
        report = self.run_reconcile()
        self.assertIn("Hosted Canvas wrapper", report["blocked"][0]["reason"])
        self.assertEqual(self.path.read_bytes(), original)

    def test_hosted_metadata_apply_preserves_instructional_body(self):
        self.hosted()
        body = parse_frontmatter(self.path)[1]
        self.live["title"] = "Updated Canvas title"
        report = self.run_reconcile()
        self.run_reconcile(apply=True, confirm_token=report["confirmation_token"])
        self.assertEqual(parse_frontmatter(self.path)[1], body)

    def test_inspection_uses_external_mapping_and_hosted_representation(self):
        self.hosted()
        with (
            patch.object(inspect_canvas, "REPO_ROOT", self.root),
            patch.object(
                inspect_canvas.CanvasClient, "from_env", return_value=self.client
            ),
        ):
            report = inspect_canvas.build_report(
                self.manifest_path,
                include_items=True,
                include_drift=True,
                state_dir=self.state_dir,
            )
        self.assertEqual(report["summary"]["manifest_artifacts"], 1)
        self.assertEqual(report["summary"]["drifted_artifacts"], 0)
        self.assertEqual(report["summary"]["canvas_items_not_in_manifest"], 0)
        self.assertEqual(report["manifest"]["state_path"], str(self.state_path))

    def test_removal_updates_external_state_only_after_token(self):
        store = MaintenanceState(self.manifest_path, self.root, self.state_dir)
        plan = remove.build_removal_plan(
            store.load(), ["module_item_id:9001"], self.client, self.manifest_path
        )
        original = self.manifest_path.read_bytes()
        with self.assertRaises(remove.RemovalPlanError):
            remove.apply_removal(
                self.manifest_path,
                ["module_item_id:9001"],
                "wrong",
                self.client,
                state_dir=self.state_dir,
            )
        self.client.delete_page.assert_not_called()
        remove.apply_removal(
            self.manifest_path,
            ["module_item_id:9001"],
            plan["confirmation_token"],
            self.client,
            state_dir=self.state_dir,
        )
        self.assertEqual(json.loads(self.state_path.read_text())["artifacts"], {})
        self.assertEqual(self.manifest_path.read_bytes(), original)
        self.assertTrue(self.path.exists())

    def test_hosted_ai_activity_prepare_preserves_source_type_and_body(self):
        fm, body = parse_frontmatter(self.path)
        fm.update(
            type="discussion",
            points=10,
            submission_type="file_upload",
            delivery_mode="ai_activity",
            ai_activity={
                "activity_id": "stable-page",
                "title": "Stable Page",
                "questions": [
                    {
                        "id": "q1",
                        "type": "ai-discussion",
                        "prompt": "Explain your reasoning.",
                    }
                ],
            },
        )
        self.path.write_text("---\n" + yaml.safe_dump(fm) + "---\n\n" + body)
        self.hosted()
        self.entry.update(
            canvas_type="assignment",
            canvas_page_url=None,
            source_type="discussion",
            delivery_mode="ai_activity",
            content_hash=content_hash(self.path),
        )
        assignment = {
            "id": 1001,
            "name": fm["title"],
            "description": self.live["body"],
            "published": True,
            "points_possible": 10,
        }
        self.entry["canvas_fingerprint"] = canvas_fingerprint(assignment, "assignment")
        self.save_state()
        self.client.get_assignment.return_value = assignment
        self.client.list_module_items.return_value = [
            {
                "id": 9001,
                "type": "Assignment",
                "title": fm["title"],
                "content_id": 1001,
                "position": 1,
            }
        ]
        original = self.path.read_bytes()
        result = update_artifact.prepare_artifact(
            12345,
            9001,
            repo_root=self.root,
            client=self.client,
            state_dir=self.state_dir,
        )
        self.assertEqual(result["type"], "discussion")
        self.assertEqual(self.path.read_bytes(), original)
        result = update_artifact.verify_artifact(
            12345,
            9001,
            self.path,
            repo_root=self.root,
            client=self.client,
            state_dir=self.state_dir,
        )
        self.assertEqual(result["status"], "verified")

    def test_named_course_targets_and_state_schema(self):
        named = self.root / "career-tools/manifests/production.json"
        write_manifest(named)
        self.assertEqual(
            resolve_targets(self.root, ["career-tools/sprints/sprint-0/page.md"]),
            ["career-tools/manifests/production.json"],
        )
        self.assertEqual(resolve_targets(self.root, ["canvas_sync/push.py"]), [])
        with self.assertRaises(ValueError):
            resolve_targets(self.root, [], course="../course1")
        self.entry["local_path"] = "career-tools/sprints/sprint-0/page.md"
        self.save_state()
        self.assertEqual(validate_canvas_state(self.state_path), [])

    def test_push_refuses_wrong_instance_and_missing_migrated_state_before_client(self):
        from canvas_sync import push
        from tests.test_canvas_state import chdir

        data = json.loads(self.state_path.read_text())
        data["instance"]["course_id"] = 777
        self.state_path.write_text(json.dumps(data))
        with chdir(self.root), patch.object(push.CanvasClient, "from_env") as client:
            with self.assertRaisesRegex(ValueError, "course_id"):
                push.push_artifact(
                    self.path, self.manifest_path, state_dir=self.state_dir
                )
            self.state_path.unlink()
            manifest = json.loads(self.manifest_path.read_text())
            manifest["artifacts"][self.rel] = self.entry
            self.manifest_path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(ValueError, "bootstrap"):
                push.push_artifact(
                    self.path, self.manifest_path, state_dir=self.state_dir
                )
            client.assert_not_called()


class SourceParsingTests(unittest.TestCase):
    def test_scalar_frontmatter_is_reported_and_triple_hyphens_in_title_are_valid(self):
        from canvas_sync.schema import validate_artifact

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "page.md"
            for malformed in ("a scalar", "- a list"):
                path.write_text(f"---\n{malformed}\n---\n\nBody\n")
                errors = validate_artifact(path)
                self.assertTrue(any("YAML mapping" in error for error in errors))
            write_page(path)
            path.write_text(
                path.read_text().replace('"Stable Page"', '"Before --- After"')
            )
            self.assertEqual(validate_artifact(path), [])
            self.assertEqual(parse_frontmatter(path)[0]["title"], "Before --- After")

    def test_quiz_drift_includes_answers_and_unknown_types_are_not_coerced(self):
        from canvas_sync.update_artifact import (
            UpdateArtifactError,
            import_quiz_questions,
        )

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "quiz.md"
            write_page(path)
            fm, body = parse_frontmatter(path)
            fm.update(
                type="quiz",
                points=1,
                submission_type="online_quiz",
                questions=[
                    {
                        "type": "short_answer",
                        "prompt": "Name the evidence.",
                        "points": 1,
                        "answers": [{"text": "Observation", "correct": True}],
                    }
                ],
            )
            path.write_text("---\n" + yaml.safe_dump(fm) + "---\n\n" + body)
            question = {
                "question_type": "short_answer_question",
                "question_text": "Name the evidence.",
                "points_possible": 1,
                "answers": [{"answer_text": "Observation", "answer_weight": 100}],
            }
            live = {
                "title": fm["title"],
                "description": markdown_body_to_html(body),
                "points_possible": 1,
                "questions": [question],
            }
            self.assertEqual(compute_drift(path, live, "quiz"), {})
            question["answers"][0]["answer_text"] = "Inference"
            self.assertIn("questions", compute_drift(path, live, "quiz"))
            client = Mock()
            from canvas_sync.push import push_quiz

            client.create_quiz.return_value = {"id": 1}
            push_quiz(client, fm, "", None)
            self.assertEqual(
                client.add_quiz_question.call_args.args[1]["answers"],
                [{"answer_text": "Observation", "answer_weight": 100}],
            )
            client.list_quiz_questions.return_value = [question]
            self.assertEqual(
                import_quiz_questions(client, 1)[0]["answers"][0]["text"], "Inference"
            )
            question["question_type"] = "matching_question"
            with self.assertRaisesRegex(UpdateArtifactError, "Unsupported"):
                import_quiz_questions(client, 1)

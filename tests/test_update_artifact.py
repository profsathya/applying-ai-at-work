from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from canvas_sync.schema import parse_frontmatter, validate_artifact, validate_manifest
from canvas_sync.update_artifact import (
    SprintRequiredError,
    UpdateArtifactError,
    list_artifacts,
    prepare_artifact,
    render_list_markdown,
    resolve_manifest_for_course_id,
    verify_artifact,
)


HASH = "a" * 64


class FakeCanvasClient:
    def __init__(
        self,
        *,
        modules: list[dict],
        items_by_module: dict[int, list[dict]],
        pages: dict[str, dict] | None = None,
        assignments: dict[int, dict] | None = None,
        discussions: dict[int, dict] | None = None,
        quizzes: dict[int, dict] | None = None,
        quiz_questions: dict[int, list[dict]] | None = None,
    ):
        self.modules = modules
        self.items_by_module = items_by_module
        self.pages = pages or {}
        self.assignments = assignments or {}
        self.discussions = discussions or {}
        self.quizzes = quizzes or {}
        self.quiz_questions = quiz_questions or {}

    def list_modules(self) -> list[dict]:
        return self.modules

    def list_module_items(self, module_id: int) -> list[dict]:
        return self.items_by_module.get(module_id, [])

    def get_page(self, page_url: str) -> dict:
        return self.pages[page_url]

    def get_assignment(self, assignment_id: int) -> dict:
        return self.assignments[int(assignment_id)]

    def get_discussion(self, topic_id: int) -> dict:
        return self.discussions[int(topic_id)]

    def get_quiz(self, quiz_id: int) -> dict:
        return self.quizzes[int(quiz_id)]

    def list_quiz_questions(self, quiz_id: int) -> list[dict]:
        return self.quiz_questions.get(int(quiz_id), [])


def module(module_id: int = 10, name: str = "Module One", position: int = 1) -> dict:
    return {
        "id": module_id,
        "name": name,
        "position": position,
        "published": True,
        "items_count": 1,
    }


def page_item(module_item_id: int = 1001, page_url: str = "page-one", position: int = 1) -> dict:
    return {
        "id": module_item_id,
        "position": position,
        "title": "Page One",
        "type": "Page",
        "content_id": None,
        "page_url": page_url,
        "published": True,
    }


def assignment_item(
    module_item_id: int = 1002,
    assignment_id: int = 201,
    title: str = "Assignment One",
    position: int = 2,
) -> dict:
    return {
        "id": module_item_id,
        "position": position,
        "title": title,
        "type": "Assignment",
        "content_id": assignment_id,
        "page_url": None,
        "published": True,
    }


def discussion_item(module_item_id: int = 1003, topic_id: int = 301) -> dict:
    return {
        "id": module_item_id,
        "position": 3,
        "title": "Discussion One",
        "type": "Discussion",
        "content_id": topic_id,
        "page_url": None,
        "published": True,
    }


def quiz_item(module_item_id: int = 1004, quiz_id: int = 401) -> dict:
    return {
        "id": module_item_id,
        "position": 4,
        "title": "Quiz One",
        "type": "Quiz",
        "content_id": quiz_id,
        "page_url": None,
        "published": True,
    }


def create_repo(course_id: int = 42, artifacts: dict | None = None) -> tuple[tempfile.TemporaryDirectory, Path]:
    tmp = tempfile.TemporaryDirectory()
    root = Path(tmp.name).resolve()
    course_dir = root / "course1"
    for sprint in range(0, 6):
        (course_dir / "sprints" / f"sprint-{sprint}").mkdir(parents=True, exist_ok=True)
    (course_dir / "manifests").mkdir(parents=True, exist_ok=True)
    manifest = {
        "instance": {
            "name": "production",
            "base_url": "https://canvas.example/",
            "course_id": course_id,
        },
        "last_sync": None,
        "artifacts": artifacts or {},
    }
    (course_dir / "manifests" / "production.json").write_text(
        json.dumps(manifest), encoding="utf-8"
    )
    return tmp, root


def write_md(root: Path, rel_path: str, frontmatter: dict, body: str = "# Old\n\nOld body.") -> None:
    path = root / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    import yaml

    with path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(frontmatter, f, sort_keys=False)
        f.write("---\n\n")
        f.write(body.rstrip() + "\n")


def manifest_entry(
    *,
    canvas_type: str,
    module_id: int = 10,
    canvas_id: int | None = None,
    page_url: str | None = None,
) -> dict:
    return {
        "canvas_type": canvas_type,
        "canvas_id": canvas_id,
        "canvas_page_url": page_url,
        "canvas_module_id": module_id,
        "content_hash": HASH,
        "last_pushed": "2026-05-01T00:00:00+00:00",
    }


class UpdateArtifactTests(unittest.TestCase):
    def test_resolves_exactly_one_manifest_for_course_id(self) -> None:
        tmp, root = create_repo(course_id=42)
        self.addCleanup(tmp.cleanup)

        manifest = resolve_manifest_for_course_id(42, root)
        self.assertEqual(manifest, root / "course1" / "manifests" / "production.json")

        with self.assertRaises(UpdateArtifactError):
            resolve_manifest_for_course_id(99, root)

        course2_manifest = root / "course2" / "manifests" / "production.json"
        course2_manifest.parent.mkdir(parents=True)
        course2_manifest.write_text(
            json.dumps(
                {
                    "instance": {"name": "production", "base_url": "https://canvas.example/", "course_id": 42},
                    "artifacts": {},
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(UpdateArtifactError):
            resolve_manifest_for_course_id(42, root)

    def test_list_reports_module_item_ids_and_manifest_files(self) -> None:
        rel_path = "course1/sprints/sprint-0/page-one.md"
        tmp, root = create_repo(
            artifacts={rel_path: manifest_entry(canvas_type="page", page_url="page-one")}
        )
        self.addCleanup(tmp.cleanup)
        client = FakeCanvasClient(
            modules=[module()],
            items_by_module={10: [page_item()]},
            pages={"page-one": {"title": "Page One", "body": "<p>Body</p>"}},
        )

        report = list_artifacts(42, client=client, repo_root=root)
        self.assertEqual(report["items"][0]["module_item_id"], 1001)
        self.assertEqual(report["items"][0]["manifest_file"], rel_path)
        rendered = render_list_markdown(report)
        self.assertIn("module_item_id", rendered)
        self.assertIn("1001", rendered)

    def test_prepare_refreshes_manifest_backed_page(self) -> None:
        rel_path = "course1/sprints/sprint-0/page-one.md"
        tmp, root = create_repo(
            artifacts={rel_path: manifest_entry(canvas_type="page", page_url="page-one")}
        )
        self.addCleanup(tmp.cleanup)
        write_md(
            root,
            rel_path,
            {
                "type": "page",
                "title": "Old Page",
                "slug": "page-one",
                "sprint": 0,
                "module": "Module One",
                "position": 1,
                "publish": True,
            },
        )
        client = FakeCanvasClient(
            modules=[module()],
            items_by_module={10: [page_item()]},
            pages={"page-one": {"title": "Live Page", "body": "<h1>Live Page</h1><p>Fresh body.</p>"}},
        )

        result = prepare_artifact(42, 1001, client=client, repo_root=root)

        self.assertEqual(result["action"], "refreshed")
        fm, body = parse_frontmatter(root / rel_path)
        self.assertEqual(fm["title"], "Live Page")
        self.assertIn("Fresh body", body)
        manifest = json.loads((root / "course1/manifests/production.json").read_text())
        self.assertIn("last_pulled", manifest["artifacts"][rel_path])
        self.assertEqual(validate_manifest(root / "course1/manifests/production.json"), [])

    def test_prepare_refreshes_manifest_backed_assignment_discussion_and_quiz(self) -> None:
        cases = [
            (
                "assignment",
                "course1/sprints/sprint-0/assignment-one.md",
                assignment_item(),
                {"name": "Live Assignment", "description": "<p>Assignment body.</p>", "points_possible": 7, "submission_types": ["online_upload"]},
                "assignments",
            ),
            (
                "discussion",
                "course1/sprints/sprint-0/discussion-one.md",
                discussion_item(),
                {"title": "Live Discussion", "message": "<p>Discussion body.</p>", "assignment": {"points_possible": 3}},
                "discussions",
            ),
            (
                "quiz",
                "course1/sprints/sprint-0/quiz-one.md",
                quiz_item(),
                {"title": "Live Quiz", "description": "<p>Quiz body.</p>", "points_possible": 2},
                "quizzes",
            ),
        ]
        for canvas_type, rel_path, item, state, state_bucket in cases:
            with self.subTest(canvas_type=canvas_type):
                entry = manifest_entry(
                    canvas_type=canvas_type,
                    canvas_id=item["content_id"],
                )
                tmp, root = create_repo(artifacts={rel_path: entry})
                self.addCleanup(tmp.cleanup)
                fm = {
                    "type": canvas_type,
                    "title": "Old",
                    "slug": Path(rel_path).stem,
                    "sprint": 0,
                    "module": "Module One",
                    "position": item["position"],
                    "points": 1,
                    "submission_type": "online_quiz" if canvas_type == "quiz" else "text_entry",
                    "publish": True,
                }
                if canvas_type == "quiz":
                    fm["questions"] = [{"type": "short_answer", "prompt": "Old?", "points": 1}]
                write_md(root, rel_path, fm)
                buckets = {state_bucket: {item["content_id"]: state}}
                client = FakeCanvasClient(
                    modules=[module()],
                    items_by_module={10: [item]},
                    quiz_questions={
                        401: [
                            {
                                "question_type": "multiple_choice_question",
                                "question_text": "Pick one",
                                "points_possible": 2,
                                "answers": [
                                    {"answer_text": "A", "answer_weight": 100},
                                    {"answer_text": "B", "answer_weight": 0},
                                ],
                            }
                        ]
                    },
                    **buckets,
                )

                result = prepare_artifact(42, item["id"], client=client, repo_root=root)

                self.assertEqual(result["action"], "refreshed")
                updated_fm, body = parse_frontmatter(root / rel_path)
                self.assertIn(canvas_type.capitalize().split("_")[0], updated_fm["title"])
                self.assertIn("body", body.lower())
                if canvas_type == "assignment":
                    self.assertEqual(updated_fm["points"], 7)
                    self.assertEqual(updated_fm["submission_type"], "file_upload")
                if canvas_type == "discussion":
                    self.assertEqual(updated_fm["points"], 3)
                    self.assertEqual(updated_fm["submission_type"], "discussion_topic")
                if canvas_type == "quiz":
                    self.assertEqual(updated_fm["questions"][0]["type"], "multiple_choice")
                    self.assertTrue(updated_fm["questions"][0]["answers"][0]["correct"])

    def test_prepare_imports_canvas_only_item_when_sprint_is_inferred(self) -> None:
        existing_rel = "course1/sprints/sprint-2/existing-page.md"
        tmp, root = create_repo(
            artifacts={existing_rel: manifest_entry(canvas_type="page", page_url="existing-page")}
        )
        self.addCleanup(tmp.cleanup)
        write_md(
            root,
            existing_rel,
            {
                "type": "page",
                "title": "Existing",
                "slug": "existing-page",
                "sprint": 2,
                "module": "Module One",
                "position": 1,
                "publish": True,
            },
        )
        selected = assignment_item(1002, 202, "New Assignment", 2)
        client = FakeCanvasClient(
            modules=[module()],
            items_by_module={10: [page_item(1001, "existing-page", 1), selected]},
            pages={"existing-page": {"title": "Existing", "body": "<p>Existing</p>"}},
            assignments={202: {"name": "New Assignment", "description": "<p>Imported body.</p>", "points_possible": 5, "submission_types": ["online_text_entry"]}},
        )

        result = prepare_artifact(42, 1002, client=client, repo_root=root)

        self.assertEqual(result["action"], "imported")
        self.assertEqual(result["file"], "course1/sprints/sprint-2/new-assignment.md")
        self.assertIsNotNone(result["added_module_header"])
        fm, body = parse_frontmatter(root / result["file"])
        self.assertEqual(validate_artifact(root / result["file"]), [])
        self.assertNotIn("canvas_id", fm)
        self.assertEqual(fm["sprint"], 2)
        self.assertIn("Imported body", body)
        manifest = json.loads((root / "course1/manifests/production.json").read_text())
        self.assertEqual(manifest["artifacts"][result["file"]]["canvas_id"], 202)

    def test_prepare_requires_sprint_for_canvas_only_item_when_not_inferred(self) -> None:
        tmp, root = create_repo()
        self.addCleanup(tmp.cleanup)
        client = FakeCanvasClient(
            modules=[module()],
            items_by_module={10: [page_item()]},
            pages={"page-one": {"title": "Page One", "body": "<p>Body</p>"}},
        )

        with self.assertRaises(SprintRequiredError):
            prepare_artifact(42, 1001, client=client, repo_root=root)

    def test_verify_accepts_allowed_edits_and_blocks_identity_edits(self) -> None:
        rel_path = "course1/sprints/sprint-1/assignment-one.md"
        tmp, root = create_repo(
            artifacts={rel_path: manifest_entry(canvas_type="assignment", canvas_id=201)}
        )
        self.addCleanup(tmp.cleanup)
        base_fm = {
            "type": "assignment",
            "title": "Assignment One",
            "slug": "assignment-one",
            "sprint": 1,
            "module": "Module One",
            "position": 2,
            "points": 5,
            "submission_type": "text_entry",
            "publish": True,
        }
        client = FakeCanvasClient(
            modules=[module()],
            items_by_module={10: [assignment_item()]},
            assignments={201: {"name": "Assignment One", "description": "<p>Body</p>", "points_possible": 5, "submission_types": ["online_text_entry"]}},
        )

        write_md(root, rel_path, {**base_fm, "title": "Edited Title", "points": 8}, "# Edited\n\nNew body.")
        verified = verify_artifact(42, 1002, Path(rel_path), client=client, repo_root=root)
        self.assertEqual(verified["status"], "verified")

        for field, value in [
            ("type", "page"),
            ("module", "Different Module"),
            ("position", 9),
            ("sprint", 2),
            ("slug", "renamed"),
        ]:
            with self.subTest(field=field):
                changed = dict(base_fm)
                changed[field] = value
                write_md(root, rel_path, changed)
                with self.assertRaises(UpdateArtifactError):
                    verify_artifact(42, 1002, Path(rel_path), client=client, repo_root=root)


if __name__ == "__main__":
    unittest.main()

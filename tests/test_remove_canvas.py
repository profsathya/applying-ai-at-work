from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from canvas_sync.remove import RemovalPlanError, apply_removal, build_removal_plan


HASH = "a" * 64


class FakeCanvasClient:
    def __init__(self, modules: list[dict], items_by_module: dict[int, list[dict]]):
        self.modules = modules
        self.items_by_module = items_by_module
        self.calls: list[tuple] = []

    def list_modules(self) -> list[dict]:
        return self.modules

    def list_module_items(self, module_id: int) -> list[dict]:
        return self.items_by_module.get(module_id, [])

    def delete_module_item(self, module_id: int, module_item_id: int) -> dict:
        self.calls.append(("delete_module_item", module_id, module_item_id))
        return {}

    def delete_module(self, module_id: int) -> dict:
        self.calls.append(("delete_module", module_id))
        return {}

    def delete_assignment(self, assignment_id: int) -> dict:
        self.calls.append(("delete_assignment", assignment_id))
        return {}

    def delete_page(self, page_url: str) -> dict:
        self.calls.append(("delete_page", page_url))
        return {}

    def delete_discussion(self, topic_id: int) -> dict:
        self.calls.append(("delete_discussion", topic_id))
        return {}

    def delete_quiz(self, quiz_id: int) -> dict:
        self.calls.append(("delete_quiz", quiz_id))
        return {}


def base_manifest() -> dict:
    return {
        "instance": {
            "name": "test",
            "base_url": "https://canvas.example/",
            "course_id": 42,
        },
        "last_sync": "2026-05-01T00:00:00+00:00",
        "artifacts": {
            "course1/sprints/sprint-0/module.md": {
                "canvas_type": "module_header",
                "canvas_id": None,
                "canvas_page_url": None,
                "canvas_module_id": 10,
                "content_hash": HASH,
                "last_pushed": "2026-05-01T00:00:00+00:00",
            },
            "course1/sprints/sprint-0/page.md": {
                "canvas_type": "page",
                "canvas_id": 101,
                "canvas_page_url": "page-one",
                "canvas_module_id": 10,
                "content_hash": HASH,
                "last_pushed": "2026-05-01T00:00:00+00:00",
            },
            "course1/sprints/sprint-0/quiz.md": {
                "canvas_type": "quiz",
                "canvas_id": 201,
                "canvas_page_url": None,
                "canvas_module_id": 10,
                "content_hash": HASH,
                "last_pushed": "2026-05-01T00:00:00+00:00",
            },
        },
    }


def base_client(extra_items: dict[int, list[dict]] | None = None) -> FakeCanvasClient:
    modules = [
        {
            "id": 10,
            "position": 1,
            "name": "Module One",
            "published": True,
            "items_count": 2,
        }
    ]
    items_by_module = {
        10: [
            {
                "id": 1001,
                "position": 1,
                "title": "Page One",
                "type": "Page",
                "content_id": None,
                "page_url": "page-one",
                "published": True,
            },
            {
                "id": 1002,
                "position": 2,
                "title": "Quiz One",
                "type": "Quiz",
                "content_id": 201,
                "page_url": None,
                "published": True,
            },
        ]
    }
    if extra_items:
        for module_id, items in extra_items.items():
            items_by_module.setdefault(module_id, []).extend(items)
    return FakeCanvasClient(modules, items_by_module)


class CanvasRemovalPlanTests(unittest.TestCase):
    def test_module_target_expands_to_manifest_backed_items(self) -> None:
        plan = build_removal_plan(base_manifest(), ["module_id:10"], base_client())

        self.assertTrue(plan["apply_allowed"])
        self.assertEqual(plan["blocked"], [])
        self.assertEqual(
            [op["action"] for op in plan["operations"]],
            [
                "delete_module_item",
                "delete_module_item",
                "delete_content",
                "delete_content",
                "delete_module",
            ],
        )
        self.assertEqual(
            plan["manifest_entries_to_remove"],
            [
                "course1/sprints/sprint-0/module.md",
                "course1/sprints/sprint-0/page.md",
                "course1/sprints/sprint-0/quiz.md",
            ],
        )

    def test_item_target_deletes_item_and_underlying_content_only(self) -> None:
        plan = build_removal_plan(base_manifest(), ["module_item_id:1001"], base_client())

        self.assertTrue(plan["apply_allowed"])
        self.assertEqual(
            [op["action"] for op in plan["operations"]],
            ["delete_module_item", "delete_content"],
        )
        self.assertEqual(plan["operations"][1]["canvas_type"], "page")
        self.assertEqual(plan["manifest_entries_to_remove"], ["course1/sprints/sprint-0/page.md"])

    def test_apply_keeps_local_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory(dir=".") as tmp:
            tmp_path = Path(tmp)
            local_md = tmp_path / "page.md"
            local_rel = local_md.resolve().relative_to(Path.cwd().resolve()).as_posix()
            local_md.write_text("---\ntitle: Test\n---\n\nBody\n", encoding="utf-8")

            manifest = base_manifest()
            manifest["artifacts"][local_rel] = manifest["artifacts"].pop(
                "course1/sprints/sprint-0/page.md"
            )
            manifest["artifacts"].pop("course1/sprints/sprint-0/module.md")
            manifest["artifacts"].pop("course1/sprints/sprint-0/quiz.md")
            manifest_path = tmp_path / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            client = FakeCanvasClient(
                modules=[{"id": 10, "position": 1, "name": "Module One", "items_count": 1}],
                items_by_module={
                    10: [
                        {
                            "id": 1001,
                            "position": 1,
                            "title": "Page One",
                            "type": "Page",
                            "content_id": None,
                            "page_url": "page-one",
                        }
                    ]
                },
            )
            plan = build_removal_plan(manifest, [f"file:{local_rel}"], client, manifest_path.resolve())

            apply_removal(manifest_path, [f"file:{local_rel}"], plan["confirmation_token"], client)

            self.assertTrue(local_md.exists())
            updated = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertNotIn(local_rel, updated["artifacts"])

    def test_canvas_only_item_blocks_module_target(self) -> None:
        client = base_client(
            {
                10: [
                    {
                        "id": 1003,
                        "position": 3,
                        "title": "External Link",
                        "type": "ExternalUrl",
                        "content_id": None,
                        "page_url": None,
                    }
                ]
            }
        )

        plan = build_removal_plan(base_manifest(), ["module_id:10"], client)

        self.assertFalse(plan["apply_allowed"])
        self.assertIn("Canvas-only", plan["blocked"][0]["reason"])

    def test_duplicate_content_in_unselected_module_blocks_delete(self) -> None:
        manifest = base_manifest()
        client = FakeCanvasClient(
            modules=[
                {"id": 10, "position": 1, "name": "Module One", "items_count": 1},
                {"id": 11, "position": 2, "name": "Module Two", "items_count": 1},
            ],
            items_by_module={
                10: [
                    {
                        "id": 1001,
                        "position": 1,
                        "title": "Page One",
                        "type": "Page",
                        "content_id": None,
                        "page_url": "page-one",
                    }
                ],
                11: [
                    {
                        "id": 1101,
                        "position": 1,
                        "title": "Page One Duplicate",
                        "type": "Page",
                        "content_id": None,
                        "page_url": "page-one",
                    }
                ],
            },
        )

        plan = build_removal_plan(manifest, ["module_item_id:1001"], client)

        self.assertFalse(plan["apply_allowed"])
        self.assertEqual(
            plan["blocked"][0]["reason"],
            "same Canvas content appears in an unselected module item",
        )

    def test_apply_refuses_missing_mismatched_and_stale_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest = base_manifest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            client = base_client()
            plan = build_removal_plan(manifest, ["module_item_id:1001"], client, manifest_path.resolve())

            with self.assertRaises(RemovalPlanError):
                apply_removal(manifest_path, ["module_item_id:1001"], None, client)

            with self.assertRaises(RemovalPlanError):
                apply_removal(manifest_path, ["module_item_id:1001"], "wrong-token", client)

            stale_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            stale_manifest["last_sync"] = "2026-05-02T00:00:00+00:00"
            manifest_path.write_text(json.dumps(stale_manifest), encoding="utf-8")

            with self.assertRaises(RemovalPlanError):
                apply_removal(manifest_path, ["module_item_id:1001"], plan["confirmation_token"], client)

    def test_course_clear_includes_canvas_only_items_and_modules(self) -> None:
        manifest = base_manifest()
        client = FakeCanvasClient(
            modules=[
                {"id": 10, "position": 1, "name": "Module One", "items_count": 2},
                {"id": 11, "position": 2, "name": "Canvas Only Module", "items_count": 1},
            ],
            items_by_module={
                10: [
                    {
                        "id": 1001,
                        "position": 1,
                        "title": "Page One",
                        "type": "Page",
                        "content_id": None,
                        "page_url": "page-one",
                    },
                    {
                        "id": 1002,
                        "position": 2,
                        "title": "Quiz One",
                        "type": "Quiz",
                        "content_id": 201,
                        "page_url": None,
                    },
                ],
                11: [
                    {
                        "id": 1101,
                        "position": 1,
                        "title": "Canvas Only Assignment",
                        "type": "Assignment",
                        "content_id": 301,
                        "page_url": None,
                    }
                ],
            },
        )

        plan = build_removal_plan(manifest, [], client, course_clear=True)

        self.assertTrue(plan["apply_allowed"])
        self.assertTrue(plan["course_clear"])
        self.assertEqual(plan["blocked"], [])
        self.assertEqual(
            [op["action"] for op in plan["operations"]],
            [
                "delete_module_item",
                "delete_module_item",
                "delete_module_item",
                "delete_content",
                "delete_content",
                "delete_content",
                "delete_module",
                "delete_module",
            ],
        )
        self.assertEqual(
            sorted(op["module_item_id"] for op in plan["operations"] if op["action"] == "delete_module_item"),
            [1001, 1002, 1101],
        )
        self.assertEqual(
            sorted(op["module_id"] for op in plan["operations"] if op["action"] == "delete_module"),
            [10, 11],
        )
        self.assertEqual(plan["manifest_entries_to_remove"], sorted(manifest["artifacts"]))

    def test_course_clear_apply_clears_manifest_after_token_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest = base_manifest()
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            client = base_client()
            plan = build_removal_plan(
                manifest,
                [],
                client,
                manifest_path.resolve(),
                course_clear=True,
            )

            applied = apply_removal(
                manifest_path,
                [],
                plan["confirmation_token"],
                client,
                course_clear=True,
            )

            self.assertEqual(applied["mode"], "apply")
            self.assertEqual(
                [call[0] for call in client.calls],
                [
                    "delete_module_item",
                    "delete_module_item",
                    "delete_page",
                    "delete_quiz",
                    "delete_module",
                ],
            )
            updated = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(updated["artifacts"], {})

    def test_course_clear_requires_matching_confirmation_token(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = Path(tmp) / "manifest.json"
            manifest_path.write_text(json.dumps(base_manifest()), encoding="utf-8")

            with self.assertRaises(RemovalPlanError):
                apply_removal(
                    manifest_path,
                    [],
                    "wrong-token",
                    base_client(),
                    course_clear=True,
                )


if __name__ == "__main__":
    unittest.main()

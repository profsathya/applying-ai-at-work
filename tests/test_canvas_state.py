from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from canvas_sync import push
from canvas_sync.schema import validate_canvas_state
from canvas_sync.state import state_from_manifest, state_path_for_manifest


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def write_page(path: Path, artifact_id: str = "test-page") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: page
title: "Test Page"
slug: test-page
artifact_id: {artifact_id}
sprint: 0
module: "Test Module"
position: 1
points: null
submission_type: none
publish: true
---

# Test Page

Body text.
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
                "last_sync": None,
                "artifacts": artifacts or {},
            }
        ),
        encoding="utf-8",
    )


class FakeCanvasClient:
    def create_page(self, payload: dict) -> dict:
        return {"page_id": 1001, "url": "test-page", **payload}

    def get_page(self, page_url: str) -> dict:
        return {
            "page_id": 1001,
            "url": page_url,
            "title": "Test Page",
            "body": "<h1>Test Page</h1>\n<p>Body text.</p>",
            "published": True,
        }

    def add_module_item(self, module_id: int, **kwargs: object) -> dict:
        return {"id": 9001, "module_id": module_id, **kwargs}


class CanvasStateTests(unittest.TestCase):
    def test_state_from_manifest_uses_artifact_id_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "test-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            rel_path = "course1/sprints/sprint-0/test-page.md"
            write_page(md_path, artifact_id="stable-page")
            write_manifest(
                manifest_path,
                artifacts={
                    rel_path: {
                        "canvas_type": "page",
                        "canvas_id": 1001,
                        "canvas_page_url": "test-page",
                        "canvas_module_id": 55,
                        "content_hash": "a" * 64,
                    }
                },
            )

            state = state_from_manifest(manifest_path, repo_root)

            self.assertIn("stable-page", state["artifacts"])
            self.assertEqual(state["artifacts"]["stable-page"]["local_path"], rel_path)
            self.assertEqual(state["artifacts"]["stable-page"]["canvas_page_url"], "test-page")

    def test_state_backed_push_writes_state_without_mutating_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            state_dir = repo_root / ".canvas-state"
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "test-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_page(md_path, artifact_id="stable-page")
            write_manifest(manifest_path)

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=FakeCanvasClient()):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(md_path, manifest_path, state_dir=state_dir)

            self.assertEqual(result["artifact_id"], "stable-page")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["artifacts"], {})

            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(validate_canvas_state(state_path), [])
            self.assertIn("stable-page", state["artifacts"])
            self.assertEqual(
                state["artifacts"]["stable-page"]["local_path"],
                "course1/sprints/sprint-0/test-page.md",
            )
            self.assertEqual(state["artifacts"]["stable-page"]["canvas_module_id"], 55)
            self.assertIn("canvas_fingerprint", state["artifacts"]["stable-page"])


if __name__ == "__main__":
    unittest.main()

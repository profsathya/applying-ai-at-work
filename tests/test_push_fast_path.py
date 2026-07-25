"""Tests for the content-only fast path in canvas_sync/push.py.

For hosted courses the Canvas body is only the iframe shell, so a change that
touches only the hosted body text leaves the Canvas payload identical. The
fast path skips the Canvas API write, regenerates hosted HTML, and records
state; any payload-affecting difference falls back to a normal Canvas push.
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
from canvas_sync.hosted_html import artifact_hosted_info, iframe_shell
from canvas_sync.state import state_path_for_manifest


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def write_page(path: Path, *, title: str = "Tuple Overview", body: str = "Original body.") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: page
title: "{title}"
slug: tuple-overview
artifact_id: tuple-overview
sprint: 99
module: "Hosted HTML Pilot"
position: 1
points: null
submission_type: none
publish: false
---

# {title}

{body}
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


def write_state(state_path: Path) -> None:
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
                    "tuple-overview": {
                        "artifact_id": "tuple-overview",
                        "local_path": "course1/sprints/sprint-99/tuple-overview.md",
                        "canvas_type": "page",
                        "canvas_id": 1001,
                        "canvas_page_url": "tuple-overview",
                        "canvas_module_id": 55,
                        "completion_requirement": "must_view",
                        "content_hash": "0" * 64,
                    }
                },
            }
        ),
        encoding="utf-8",
    )


class FakeClient:
    """Serves live objects; records whether any Canvas write happened."""

    def __init__(self, live_page: dict | None = None, live_assignment: dict | None = None) -> None:
        self.live_page = live_page
        self.live_assignment = live_assignment
        self.writes: list[str] = []

    def get_page(self, page_url: str) -> dict | None:
        return self.live_page

    def get_assignment(self, assignment_id: int) -> dict | None:
        return self.live_assignment

    def update_assignment(self, assignment_id: int, payload: dict) -> dict:
        self.writes.append("update_assignment")
        return {"id": assignment_id, **payload}

    def update_page(self, page_url: str, payload: dict) -> dict:
        self.writes.append("update_page")
        return {"page_id": 1001, "url": page_url, **payload}

    def create_page(self, payload: dict) -> dict:
        self.writes.append("create_page")
        return {"page_id": 1001, "url": "tuple-overview", **payload}

    def update_module_item(self, *args: object, **kwargs: object) -> dict:
        self.writes.append("update_module_item")
        return {}

    def add_module_item(self, *args: object, **kwargs: object) -> dict:
        self.writes.append("add_module_item")
        return {"id": 9001}


def write_assignment(path: Path, *, submission_type: str = "text_entry") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: assignment
title: "Tuple Lab"
slug: tuple-lab
artifact_id: tuple-lab
sprint: 99
module: "Hosted HTML Pilot"
position: 2
points: 10
submission_type: {submission_type}
publish: false
---

# Tuple Lab

Edited hosted body text only.
""",
        encoding="utf-8",
    )


def write_assignment_state(state_path: Path) -> None:
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
                        "completion_requirement": "must_submit",
                        "content_hash": "0" * 64,
                    }
                },
            }
        ),
        encoding="utf-8",
    )


class ContentOnlyFastPathTests(unittest.TestCase):
    def _setup(self, tmp: str, *, live_title: str = "Tuple Overview") -> tuple[Path, Path, Path, Path, FakeClient]:
        repo_root = Path(tmp).resolve()
        md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
        manifest_path = repo_root / "course1" / "manifests" / "production.json"
        state_dir = repo_root / ".canvas-state"
        output_dir = repo_root / "Common-Curriculum"
        write_page(md_path, body="Edited hosted body text only.")
        write_manifest(manifest_path)
        write_state(state_dir / "course1" / "production.json")

        hosted_url = artifact_hosted_info(md_path, manifest_path)["hosted_url"]
        live_page = {
            "page_id": 1001,
            "url": "tuple-overview",
            "title": live_title,
            "body": iframe_shell(hosted_url, live_title),
            "published": False,
        }
        return repo_root, md_path, manifest_path, state_dir, FakeClient(live_page), output_dir

    def test_body_only_change_skips_canvas_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, md_path, manifest_path, state_dir, client, output_dir = self._setup(tmp)

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    result = push.push_artifact(
                        md_path,
                        manifest_path,
                        state_dir=state_dir,
                        hosted_output_dir=output_dir,
                    )

            self.assertEqual(result["action"], "content_update")
            self.assertEqual(result["note"], "content update - live via hosted page")
            self.assertEqual(client.writes, [])

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-overview"]
            self.assertNotEqual(entry["content_hash"], "0" * 64)
            self.assertEqual(entry["canvas_id"], 1001)
            self.assertTrue(entry.get("canvas_fingerprint"))
            self.assertTrue(entry.get("hosted_hash"))
            hosted_page = output_dir / "deanza" / "course1" / "activities" / "tuple-overview.html"
            self.assertIn("Edited hosted body text only.", hosted_page.read_text(encoding="utf-8"))

    def test_title_change_falls_back_to_canvas_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, md_path, manifest_path, state_dir, client, output_dir = self._setup(
                tmp, live_title="Old Title In Canvas"
            )

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(
                            md_path,
                            manifest_path,
                            state_dir=state_dir,
                            hosted_output_dir=output_dir,
                        )

            self.assertEqual(result["action"], "updated")
            self.assertIn("update_page", client.writes)

    def _setup_assignment(
        self, tmp: str, *, fm_submission_type: str, live_submission_types: list[str]
    ) -> tuple[Path, Path, Path, Path, FakeClient, Path]:
        repo_root = Path(tmp).resolve()
        md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-lab.md"
        manifest_path = repo_root / "course1" / "manifests" / "production.json"
        state_dir = repo_root / ".canvas-state"
        output_dir = repo_root / "Common-Curriculum"
        write_assignment(md_path, submission_type=fm_submission_type)
        write_manifest(manifest_path)
        write_assignment_state(state_dir / "course1" / "production.json")

        hosted_url = artifact_hosted_info(md_path, manifest_path)["hosted_url"]
        live_assignment = {
            "id": 2001,
            "name": "Tuple Lab",
            "description": iframe_shell(hosted_url, "Tuple Lab"),
            "points_possible": 10,
            "published": False,
            "submission_types": live_submission_types,
        }
        return repo_root, md_path, manifest_path, state_dir, FakeClient(
            live_assignment=live_assignment
        ), output_dir

    def test_assignment_matching_submission_type_takes_fast_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, md_path, manifest_path, state_dir, client, output_dir = (
                self._setup_assignment(
                    tmp,
                    fm_submission_type="text_entry",
                    live_submission_types=["online_text_entry"],
                )
            )

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    result = push.push_artifact(
                        md_path,
                        manifest_path,
                        state_dir=state_dir,
                        hosted_output_dir=output_dir,
                    )

            self.assertEqual(result["action"], "content_update")
            self.assertEqual(client.writes, [])

    def test_assignment_submission_type_change_falls_back_to_canvas_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, md_path, manifest_path, state_dir, client, output_dir = (
                self._setup_assignment(
                    tmp,
                    fm_submission_type="file_upload",
                    live_submission_types=["online_text_entry"],
                )
            )

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(
                            md_path,
                            manifest_path,
                            state_dir=state_dir,
                            hosted_output_dir=output_dir,
                        )

            self.assertEqual(result["action"], "updated")
            self.assertIn("update_assignment", client.writes)

    def test_without_hosted_output_dir_normal_push_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, md_path, manifest_path, state_dir, client, _output_dir = self._setup(tmp)

            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(
                            md_path,
                            manifest_path,
                            state_dir=state_dir,
                        )

            self.assertEqual(result["action"], "updated")
            self.assertIn("update_page", client.writes)


if __name__ == "__main__":
    unittest.main()

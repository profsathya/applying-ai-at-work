"""A retry after a mid-run failure must update, never create a duplicate.

push.py persists the created object's Canvas identity immediately after
creation. If module placement (or anything later) fails, the identity survives
in state with a sentinel content hash, so a rerun takes the update path and
still re-publishes the content.
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


class CountingClient:
    def __init__(self) -> None:
        self.creates = 0
        self.updates = 0

    def create_page(self, payload: dict) -> dict:
        self.creates += 1
        return {"page_id": 1001, "url": "tuple-overview", **payload}

    def update_page(self, page_url: str, payload: dict) -> dict:
        self.updates += 1
        return {"page_id": 1001, "url": page_url, **payload}

    def get_page(self, page_url: str) -> dict:
        return {"page_id": 1001, "url": page_url, "title": "Tuple Overview", "body": "", "published": False}

    def add_module_item(self, module_id: int, **kwargs: object) -> dict:
        return {"id": 9001, "module_id": module_id, **kwargs}


class CreateIdentityPersistenceTests(unittest.TestCase):
    def test_identity_survives_failure_and_rerun_updates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-overview.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_page(md_path)
            write_manifest(manifest_path)
            client = CountingClient()

            def module_failure(*args: object, **kwargs: object) -> int:
                raise RuntimeError("module placement blew up mid-run")

            # First run: creation succeeds, then module placement fails.
            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", module_failure):
                        with self.assertRaises(RuntimeError):
                            push.push_artifact(md_path, manifest_path, state_dir=state_dir)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-overview"]
            self.assertEqual(entry["canvas_id"], 1001)
            self.assertEqual(entry["canvas_page_url"], "tuple-overview")
            # Sentinel hash keeps the artifact detected as changed for the retry.
            self.assertEqual(entry["content_hash"], "0" * 64)
            self.assertEqual(client.creates, 1)

            # Retry: same content, module placement now works. The existing
            # identity must route through the update path; no second create.
            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", return_value=client):
                    with patch.object(push, "resolve_or_create_module", return_value=55):
                        result = push.push_artifact(md_path, manifest_path, state_dir=state_dir)

            self.assertEqual(result["action"], "updated")
            self.assertEqual(client.creates, 1)
            self.assertEqual(client.updates, 1)
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-overview"]
            self.assertNotEqual(entry["content_hash"], "0" * 64)
            self.assertEqual(entry["canvas_module_id"], 55)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from canvas_sync.hosted_html import iframe_shell
from canvas_sync.hydrate_state import hosted_canvas_drift


def write_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: page
title: "Hosted Page"
slug: hosted-page
artifact_id: hosted-page
sprint: 1
module: "Sprint 1"
position: 1
points: null
submission_type: none
publish: true
---

# Hosted Page

This is the full Markdown source that should render in Common Curriculum.
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
                "hosted_html": {
                    "enabled": True,
                    "base_url": "https://example.test/deanza",
                    "path_prefix": "deanza",
                },
                "artifacts": {},
            }
        ),
        encoding="utf-8",
    )


class HydrateStateTests(unittest.TestCase):
    def test_hosted_canvas_shell_is_not_body_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-1" / "hosted-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_page(md_path)
            write_manifest(manifest_path)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            canvas_state = {
                "title": "Hosted Page",
                "body": iframe_shell(
                    "https://example.test/deanza/course1/activities/hosted-page.html",
                    "Hosted Page",
                ),
                "published": True,
            }

            self.assertEqual(
                hosted_canvas_drift(md_path, manifest_path, manifest, canvas_state, "page"),
                {},
            )

    def test_hosted_canvas_shell_reports_wrong_url(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-1" / "hosted-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_page(md_path)
            write_manifest(manifest_path)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

            canvas_state = {
                "title": "Hosted Page",
                "body": iframe_shell(
                    "https://example.test/deanza/course1/activities/old.html",
                    "Hosted Page",
                ),
                "published": True,
            }

            drift = hosted_canvas_drift(md_path, manifest_path, manifest, canvas_state, "page")

            self.assertIn("body", drift)


if __name__ == "__main__":
    unittest.main()

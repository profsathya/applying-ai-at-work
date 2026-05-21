from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from canvas_sync import publish_changed
from canvas_sync.state import content_hash


def write_page(path: Path, artifact_id: str = "stable-page", body: str = "Body text.") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: page
title: "Stable Page"
slug: stable-page
artifact_id: {artifact_id}
sprint: 0
module: "Test Module"
position: 1
points: null
submission_type: none
publish: true
---

# Stable Page

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
                "last_sync": None,
                "artifacts": {},
            }
        ),
        encoding="utf-8",
    )


def write_state(path: Path, *, hash_value: str, fingerprint: str = "a" * 64) -> None:
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
                "artifacts": {
                    "stable-page": {
                        "artifact_id": "stable-page",
                        "local_path": "course1/sprints/sprint-0/stable-page.md",
                        "canvas_type": "page",
                        "canvas_id": 1001,
                        "canvas_page_url": "stable-page",
                        "canvas_module_id": 55,
                        "content_hash": hash_value,
                        "canvas_fingerprint": fingerprint,
                    }
                },
            }
        ),
        encoding="utf-8",
    )


class PublishChangedTests(unittest.TestCase):
    def test_unchanged_artifacts_are_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path)
            write_manifest(manifest_path)
            write_state(state_path, hash_value=content_hash(md_path))

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed") as drift:
                    with patch.object(publish_changed, "push_artifact") as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                        )

            self.assertEqual(result["changed"], [])
            self.assertEqual(result["published"], [])
            self.assertEqual(result["drifted"], [])
            drift.assert_not_called()
            push.assert_not_called()

    def test_changed_artifacts_publish_against_external_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path, body="Updated body text.")
            write_manifest(manifest_path)
            write_state(state_path, hash_value="b" * 64)

            pushed = {"artifact_id": "stable-page", "action": "updated"}
            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "push_artifact", return_value=pushed) as push:
                    result = publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                    )

            self.assertEqual(
                result["changed"],
                [{"file": "course1/sprints/sprint-0/stable-page.md", "artifact_id": "stable-page"}],
            )
            self.assertEqual(result["published"], [pushed])
            push.assert_called_once_with(md_path, manifest_path, state_dir=state_dir)

    def test_drift_blocks_publish(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path, body="Updated body text.")
            write_manifest(manifest_path)
            write_state(state_path, hash_value="c" * 64)
            drifted = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "reason": "canvas changed since last state-backed publish",
                }
            ]

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed", return_value=drifted):
                    with patch.object(publish_changed, "push_artifact") as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                        )

            self.assertEqual(result["drifted"], drifted)
            self.assertEqual(result["published"], [])
            push.assert_not_called()

    def test_require_state_fails_when_state_file_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_page(md_path)
            write_manifest(manifest_path)

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with self.assertRaises(FileNotFoundError):
                    publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                    )


if __name__ == "__main__":
    unittest.main()

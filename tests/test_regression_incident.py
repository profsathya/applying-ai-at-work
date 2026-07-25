"""Regression tests for the run-29963770727 incident and its failure family.

The historical run found 3 changed course1 artifacts, published none, and
exited 1 because ONE state entry was missing canvas_fingerprint. These tests
pin the fixed behavior: the same three-artifact batch publishes everything,
healing the incomplete entry, and a push exception in one artifact never
blocks its neighbors.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from canvas_sync import publish_changed
from canvas_sync.state import canvas_fingerprint


LIVE_PAGE = {
    "page_id": 1000,
    "url": "page",
    "title": "Live Page",
    "body": "live body",
    "published": True,
}
LIVE_FINGERPRINT = canvas_fingerprint(LIVE_PAGE, "page")


def write_page(path: Path, artifact_id: str, title: str, slug: str, position: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: page
title: "{title}"
slug: {slug}
artifact_id: {artifact_id}
sprint: 2
module: "Sprint 2: Direct AI Deliberately"
position: {position}
points: null
submission_type: none
publish: true
---

# {title}

Edited body for the incident regression test.
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


def write_incident_state(path: Path) -> None:
    """Two healthy entries plus the incident entry with no canvas_fingerprint."""
    entries = {}
    for artifact_id, slug, cid, fingerprint in (
        ("edit-one", "edit-one", 2001, LIVE_FINGERPRINT),
        ("edit-two", "edit-two", 2002, LIVE_FINGERPRINT),
        ("start-here-direct-ai-deliberately", "start-here-direct-ai-deliberately", 3470, None),
    ):
        entry = {
            "artifact_id": artifact_id,
            "local_path": f"course1/sprints/sprint-2/{slug}.md",
            "canvas_type": "page",
            "canvas_id": cid,
            "canvas_page_url": slug,
            "canvas_module_id": 1947,
            "content_hash": "f" * 64,
        }
        if fingerprint:
            entry["canvas_fingerprint"] = fingerprint
        entries[artifact_id] = entry
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
                "artifacts": entries,
            }
        ),
        encoding="utf-8",
    )


class HistoricalIncidentTests(unittest.TestCase):
    def _repo(self, tmp: str) -> tuple[Path, Path, Path]:
        repo_root = Path(tmp).resolve()
        sprint = repo_root / "course1" / "sprints" / "sprint-2"
        write_page(sprint / "edit-one.md", "edit-one", "Edit One", "edit-one", 1)
        write_page(sprint / "edit-two.md", "edit-two", "Edit Two", "edit-two", 2)
        write_page(
            sprint / "start-here-direct-ai-deliberately.md",
            "start-here-direct-ai-deliberately",
            "Start Here: Direct AI Deliberately",
            "start-here-direct-ai-deliberately",
            3,
        )
        manifest_path = repo_root / "course1" / "manifests" / "production.json"
        state_dir = repo_root / ".canvas-state"
        write_manifest(manifest_path)
        write_incident_state(state_dir / "course1" / "production.json")
        return repo_root, manifest_path, state_dir

    def test_three_artifact_incident_batch_all_publish_one_heals(self) -> None:
        """The exact historical shape: 2 healthy + 1 missing fingerprint."""
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)

            def fake_push(md_path, _manifest_path, **_kwargs):
                return {"artifact_id": Path(md_path).stem, "action": "updated"}

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                    with patch.object(
                        publish_changed, "fetch_canvas_state", return_value=LIVE_PAGE
                    ):
                        with patch.object(
                            publish_changed, "push_artifact", side_effect=fake_push
                        ):
                            result = publish_changed.publish_manifest(
                                manifest_path,
                                state_dir,
                                dry_run=False,
                                check_drift=True,
                                require_state=True,
                            )

            self.assertEqual(result["drifted"], [])
            self.assertEqual(result["failed"], [])
            self.assertEqual(len(result["published"]), 3)
            self.assertEqual(len(result["healed"]), 1)
            self.assertEqual(
                result["healed"][0]["artifact_id"], "start-here-direct-ai-deliberately"
            )
            self.assertIn("hydrated missing canvas_fingerprint", result["healed"][0]["reason"])

    def test_push_exception_in_one_artifact_does_not_block_neighbors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)

            def flaky_push(md_path, _manifest_path, **_kwargs):
                if Path(md_path).stem == "edit-two":
                    raise RuntimeError("canvas 500 during push")
                return {"artifact_id": Path(md_path).stem, "action": "updated"}

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                    with patch.object(
                        publish_changed, "fetch_canvas_state", return_value=LIVE_PAGE
                    ):
                        with patch.object(
                            publish_changed, "push_artifact", side_effect=flaky_push
                        ):
                            result = publish_changed.publish_manifest(
                                manifest_path,
                                state_dir,
                                dry_run=False,
                                check_drift=True,
                                require_state=True,
                            )

            published_ids = {p["artifact_id"] for p in result["published"]}
            self.assertEqual(
                published_ids, {"edit-one", "start-here-direct-ai-deliberately"}
            )
            self.assertEqual(len(result["failed"]), 1)
            self.assertEqual(result["failed"][0]["artifact_id"], "edit-two")
            self.assertIn("canvas 500 during push", result["failed"][0]["error"])


if __name__ == "__main__":
    unittest.main()

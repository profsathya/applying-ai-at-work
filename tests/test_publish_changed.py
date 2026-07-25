from __future__ import annotations

import json
import sys
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


def write_manifest(path: Path, *, hosted: bool = False, canvas_publish: bool | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "instance": {
            "name": "production",
            "base_url": "https://example.instructure.com/",
            "course_id": 12345,
            "term": "Test Term",
        },
        "last_sync": None,
        "artifacts": {},
    }
    if hosted:
        payload["hosted_html"] = {
            "enabled": True,
            "base_url": "https://profsathya.github.io/Common-Curriculum/deanza",
            "path_prefix": "deanza",
        }
    if canvas_publish is not None:
        payload["canvas_publish"] = canvas_publish
    path.write_text(json.dumps(payload), encoding="utf-8")


def write_page_with_id(path: Path, artifact_id: str, title: str, slug: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
type: page
title: "{title}"
slug: {slug}
artifact_id: {artifact_id}
sprint: 0
module: "Test Module"
position: 2
points: null
submission_type: none
publish: true
---

# {title}

Edited body text.
""",
        encoding="utf-8",
    )


def write_two_entry_state(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entries = {}
    for artifact_id, slug, cid in (
        ("stable-page", "stable-page", 1001),
        ("healthy-page", "healthy-page", 1002),
    ):
        entries[artifact_id] = {
            "artifact_id": artifact_id,
            "local_path": f"course1/sprints/sprint-0/{slug}.md",
            "canvas_type": "page",
            "canvas_id": cid,
            "canvas_page_url": slug,
            "canvas_module_id": 55,
            "content_hash": "f" * 64,
            "canvas_fingerprint": "a" * 64,
        }
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

    def test_one_drifted_artifact_does_not_block_the_others(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            drifted_md = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            healthy_md = repo_root / "course1" / "sprints" / "sprint-0" / "healthy-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(drifted_md, body="Edited while canvas drifted.")
            write_page_with_id(healthy_md, "healthy-page", "Healthy Page", "healthy-page")
            write_manifest(manifest_path)
            write_two_entry_state(state_path)
            drifted = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "reason": "canvas changed since last state-backed publish",
                }
            ]
            pushed = {"artifact_id": "healthy-page", "action": "updated"}

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed", return_value=drifted):
                    with patch.object(
                        publish_changed, "push_artifact", return_value=pushed
                    ) as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                        )

            self.assertEqual(result["drifted"], drifted)
            self.assertEqual(result["published"], [pushed])
            push.assert_called_once_with(healthy_md, manifest_path, state_dir=state_dir)

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

    def test_homepage_only_change_renders_hosted_files_without_canvas_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path)
            write_manifest(manifest_path, hosted=True)
            write_state(state_path, hash_value=content_hash(md_path))

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "push_artifact") as push:
                    result = publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                        hosted_output_dir=output_dir,
                    )

            self.assertEqual(result["changed"], [])
            self.assertEqual(result["published"], [])
            self.assertIsNotNone(result["hosted"])
            self.assertTrue((output_dir / "deanza" / "course1" / "home.html").exists())
            push.assert_not_called()

    def test_hosted_only_renders_changed_artifacts_without_canvas_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path, body="Changed body text.")
            write_manifest(manifest_path, hosted=True)
            write_state(state_path, hash_value="d" * 64)

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed") as drift:
                    with patch.object(publish_changed, "push_artifact") as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                            hosted_output_dir=output_dir,
                            hosted_only=True,
                        )

            self.assertEqual(
                result["changed"],
                [{"file": "course1/sprints/sprint-0/stable-page.md", "artifact_id": "stable-page"}],
            )
            self.assertEqual(result["published"], [])
            self.assertEqual(result["drifted"], [])
            self.assertIsNotNone(result["hosted"])
            self.assertTrue((output_dir / "deanza" / "course1" / "home.html").exists())
            drift.assert_not_called()
            push.assert_not_called()

    def test_canvas_publish_false_renders_changed_artifacts_without_canvas_push(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(md_path, body="Changed body text.")
            write_manifest(manifest_path, hosted=True, canvas_publish=False)
            write_state(state_path, hash_value="e" * 64)

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed") as drift:
                    with patch.object(publish_changed, "push_artifact") as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                            hosted_output_dir=output_dir,
                        )

            self.assertEqual(
                result["changed"],
                [{"file": "course1/sprints/sprint-0/stable-page.md", "artifact_id": "stable-page"}],
            )
            self.assertEqual(result["published"], [])
            self.assertEqual(result["drifted"], [])
            self.assertIsNotNone(result["hosted"])
            self.assertTrue((output_dir / "deanza" / "course1" / "home.html").exists())
            drift.assert_not_called()
            push.assert_not_called()


class PerItemHardeningTests(unittest.TestCase):
    """One bad artifact or one failed check never zeroes the batch."""

    def test_invalid_artifact_fails_alone_and_others_publish(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            invalid_md = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            healthy_md = repo_root / "course1" / "sprints" / "sprint-0" / "healthy-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_page(invalid_md, body="Broken — em dash body.")
            write_page_with_id(healthy_md, "healthy-page", "Healthy Page", "healthy-page")
            write_manifest(manifest_path)
            write_two_entry_state(state_dir / "course1" / "production.json")

            pushed = {"artifact_id": "healthy-page", "action": "updated"}
            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(
                    publish_changed, "push_artifact", return_value=pushed
                ) as push:
                    result = publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                    )

            self.assertEqual(result["published"], [pushed])
            push.assert_called_once_with(healthy_md, manifest_path, state_dir=state_dir)
            self.assertEqual(len(result["failed"]), 1)
            self.assertEqual(
                result["failed"][0]["file"], "course1/sprints/sprint-0/stable-page.md"
            )
            self.assertIn("em-dash", result["failed"][0]["error"])

    def test_whole_drift_scan_failure_blocks_items_without_aborting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_page(md_path, body="Changed body.")
            write_manifest(manifest_path)
            write_state(state_dir / "course1" / "production.json", hash_value="2" * 64)

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(
                    publish_changed,
                    "drift_for_changed",
                    side_effect=RuntimeError("credentials exploded"),
                ):
                    with patch.object(publish_changed, "push_artifact") as push:
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                        )

            self.assertEqual(result["published"], [])
            self.assertEqual(len(result["drifted"]), 1)
            self.assertIn("drift scan failed: credentials exploded", result["drifted"][0]["reason"])
            push.assert_not_called()

    def test_drift_check_exception_blocks_only_that_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_manifest(manifest_path)
            changed = [
                {
                    "file": "course1/sprints/sprint-0/broken-fetch.md",
                    "artifact_id": "broken-fetch",
                    "state_entry": {
                        "canvas_type": "page",
                        "canvas_id": 1001,
                        "canvas_page_url": "broken-fetch",
                        "canvas_fingerprint": "a" * 64,
                    },
                },
                {
                    "file": "course1/sprints/sprint-0/still-checked.md",
                    "artifact_id": "still-checked",
                    "state_entry": {
                        "canvas_type": "page",
                        "canvas_id": 1002,
                        "canvas_page_url": "still-checked",
                        "canvas_fingerprint": "b" * 64,
                    },
                },
            ]

            live = {"page_id": 1002, "title": "x", "body": "y", "published": True}

            def fake_fetch(client, entry):
                if entry["canvas_id"] == 1001:
                    raise RuntimeError("timeout talking to canvas")
                return live

            with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                with patch.object(publish_changed, "fetch_canvas_state", side_effect=fake_fetch):
                    drifted = publish_changed.drift_for_changed(manifest_path, changed)

            reasons = {d["artifact_id"]: d["reason"] for d in drifted}
            self.assertIn("drift check failed: timeout talking to canvas", reasons["broken-fetch"])
            # The second item was still assessed (its real mismatch reported).
            self.assertEqual(
                reasons["still-checked"], "canvas changed since last state-backed publish"
            )


class ProvisionalIdentityReportTests(unittest.TestCase):
    def test_failed_push_with_recorded_identity_reports_provisional(self) -> None:
        """A push that saved a Canvas identity before failing is surfaced so
        the workflow commits state and the retry updates, not duplicates."""
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path, body="First-time publish body.")
            write_manifest(manifest_path)
            write_state(state_path, hash_value="3" * 64)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            entry = state["artifacts"]["stable-page"]
            entry["canvas_id"] = None
            entry["canvas_page_url"] = None
            entry.pop("canvas_fingerprint", None)
            state_path.write_text(json.dumps(state), encoding="utf-8")

            def push_saves_identity_then_dies(_md_path, _manifest_path, **_kwargs):
                current = json.loads(state_path.read_text(encoding="utf-8"))
                current["artifacts"]["stable-page"]["canvas_id"] = 4242
                current["artifacts"]["stable-page"]["canvas_page_url"] = "stable-page"
                current["artifacts"]["stable-page"]["content_hash"] = "0" * 64
                state_path.write_text(json.dumps(current), encoding="utf-8")
                raise RuntimeError("hosted render exploded after create")

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(
                    publish_changed, "push_artifact", side_effect=push_saves_identity_then_dies
                ):
                    result = publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                    )

            self.assertEqual(result["published"], [])
            self.assertEqual(len(result["failed"]), 1)
            self.assertEqual(len(result["provisional"]), 1)
            self.assertEqual(result["provisional"][0]["artifact_id"], "stable-page")
            self.assertIn("retry updates instead of duplicating", result["provisional"][0]["reason"])

    def test_failed_push_without_identity_reports_no_provisional(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            write_page(md_path, body="Changed body.")
            write_manifest(manifest_path)
            write_state(state_dir / "course1" / "production.json", hash_value="4" * 64)

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(
                    publish_changed,
                    "push_artifact",
                    side_effect=RuntimeError("create itself failed"),
                ):
                    result = publish_changed.publish_manifest(
                        manifest_path,
                        state_dir,
                        dry_run=False,
                        check_drift=False,
                        require_state=True,
                    )

            self.assertEqual(len(result["failed"]), 1)
            self.assertEqual(result["provisional"], [])


class HostedRestoreTests(unittest.TestCase):
    """Blocked artifacts' hosted output stays at baseline; healthy output goes live."""

    def test_blocked_artifact_hosted_output_restored_to_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            blocked_md = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            healthy_md = repo_root / "course1" / "sprints" / "sprint-0" / "healthy-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(blocked_md, body="Blocked new content that must not go live.")
            write_page_with_id(healthy_md, "healthy-page", "Healthy Page", "healthy-page")
            write_manifest(manifest_path, hosted=True)
            write_two_entry_state(state_path)

            baseline = "OLD BASELINE CONTENT"
            blocked_out = output_dir / "deanza" / "course1" / "activities" / "stable-page.html"
            blocked_out.parent.mkdir(parents=True, exist_ok=True)
            blocked_out.write_text(baseline, encoding="utf-8")

            drifted = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "reason": "canvas changed since last state-backed publish",
                }
            ]
            pushed = {"artifact_id": "healthy-page", "action": "updated"}

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed", return_value=drifted):
                    with patch.object(publish_changed, "push_artifact", return_value=pushed):
                        result = publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                            hosted_output_dir=output_dir,
                        )

            # The final course render rewrote every page; the blocked one must
            # be back to baseline while the healthy one carries new content.
            self.assertEqual(blocked_out.read_text(encoding="utf-8"), baseline)
            healthy_out = output_dir / "deanza" / "course1" / "activities" / "healthy-page.html"
            self.assertIn("Edited body text.", healthy_out.read_text(encoding="utf-8"))
            self.assertIn(str(blocked_out), result["hosted_restored"])

    def test_blocked_artifact_without_baseline_file_is_deleted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            blocked_md = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            healthy_md = repo_root / "course1" / "sprints" / "sprint-0" / "healthy-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            output_dir = repo_root / "Common-Curriculum"
            write_page(blocked_md, body="Blocked new content.")
            write_page_with_id(healthy_md, "healthy-page", "Healthy Page", "healthy-page")
            write_manifest(manifest_path, hosted=True)
            write_two_entry_state(state_path)

            drifted = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "reason": "canvas changed since last state-backed publish",
                }
            ]
            pushed = {"artifact_id": "healthy-page", "action": "updated"}

            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed, "drift_for_changed", return_value=drifted):
                    with patch.object(publish_changed, "push_artifact", return_value=pushed):
                        publish_changed.publish_manifest(
                            manifest_path,
                            state_dir,
                            dry_run=False,
                            check_drift=True,
                            require_state=True,
                            hosted_output_dir=output_dir,
                        )

            blocked_out = output_dir / "deanza" / "course1" / "activities" / "stable-page.html"
            self.assertFalse(blocked_out.exists())


class ReportFileTests(unittest.TestCase):
    def test_report_file_written_alongside_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            report_path = repo_root / "out" / "publish-result.json"
            write_page(md_path, body="Changed body.")
            write_manifest(manifest_path)
            write_state(state_dir / "course1" / "production.json", hash_value="1" * 64)

            argv = [
                "publish_changed.py",
                "--manifest",
                str(manifest_path),
                "--state-dir",
                str(state_dir),
                "--dry-run",
                "--report-file",
                str(report_path),
            ]
            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(sys, "argv", argv):
                    exit_code = publish_changed.main()

            self.assertEqual(exit_code, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(len(report["results"]), 1)
            self.assertEqual(
                report["results"][0]["changed"],
                [{"file": "course1/sprints/sprint-0/stable-page.md", "artifact_id": "stable-page"}],
            )


class DriftSelfHealTests(unittest.TestCase):
    """Missing state is healed during publish; only real drift refuses."""

    LIVE_PAGE = {"page_id": 1001, "url": "stable-page", "title": "Stable Page", "body": "x", "published": True}

    def _drift(self, entry: dict | None, live: dict | None):
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_manifest(manifest_path)
            changed = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "state_entry": entry,
                }
            ]
            with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                with patch.object(publish_changed, "fetch_canvas_state", return_value=live):
                    drifted = publish_changed.drift_for_changed(manifest_path, changed)
            return drifted, changed[0]

    def test_missing_fingerprint_with_canvas_id_is_healed_not_drifted(self) -> None:
        entry = {"canvas_type": "page", "canvas_id": 1001, "canvas_page_url": "stable-page"}
        drifted, item = self._drift(entry, self.LIVE_PAGE)
        self.assertEqual(drifted, [])
        self.assertEqual(
            item["healed_fingerprint"],
            publish_changed.canvas_fingerprint(self.LIVE_PAGE, "page"),
        )

    def test_no_canvas_identity_is_first_time_publish(self) -> None:
        entry = {"canvas_type": "page", "canvas_id": None, "canvas_page_url": None}
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            write_manifest(manifest_path)
            changed = [
                {
                    "file": "course1/sprints/sprint-0/stable-page.md",
                    "artifact_id": "stable-page",
                    "state_entry": entry,
                }
            ]
            with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                with patch.object(publish_changed, "fetch_canvas_state") as fetch:
                    drifted = publish_changed.drift_for_changed(manifest_path, changed)
        self.assertEqual(drifted, [])
        self.assertTrue(changed[0]["first_publish"])
        fetch.assert_not_called()

    def test_matching_fingerprint_is_not_drifted(self) -> None:
        fingerprint = publish_changed.canvas_fingerprint(self.LIVE_PAGE, "page")
        entry = {
            "canvas_type": "page",
            "canvas_id": 1001,
            "canvas_page_url": "stable-page",
            "canvas_fingerprint": fingerprint,
        }
        drifted, _ = self._drift(entry, self.LIVE_PAGE)
        self.assertEqual(drifted, [])

    def test_real_drift_still_refuses(self) -> None:
        entry = {
            "canvas_type": "page",
            "canvas_id": 1001,
            "canvas_page_url": "stable-page",
            "canvas_fingerprint": "b" * 64,
        }
        drifted, _ = self._drift(entry, self.LIVE_PAGE)
        self.assertEqual(len(drifted), 1)
        self.assertEqual(drifted[0]["reason"], "canvas changed since last state-backed publish")

    def test_missing_canvas_object_still_refuses(self) -> None:
        entry = {"canvas_type": "page", "canvas_id": 1001, "canvas_page_url": "stable-page"}
        drifted, _ = self._drift(entry, None)
        self.assertEqual(len(drifted), 1)
        self.assertEqual(drifted[0]["reason"], "canvas object is missing")

    def test_publish_manifest_heals_and_publishes_missing_fingerprint_entry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "stable-page.md"
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            state_dir = repo_root / ".canvas-state"
            state_path = state_dir / "course1" / "production.json"
            write_page(md_path, body="Edited after fingerprint went missing.")
            write_manifest(manifest_path)
            write_state(state_path, hash_value="9" * 64)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            del state["artifacts"]["stable-page"]["canvas_fingerprint"]
            state_path.write_text(json.dumps(state), encoding="utf-8")

            pushed = {"artifact_id": "stable-page", "action": "updated"}
            with patch.object(publish_changed, "REPO_ROOT", repo_root):
                with patch.object(publish_changed.CanvasClient, "from_env", return_value=object()):
                    with patch.object(
                        publish_changed, "fetch_canvas_state", return_value=self.LIVE_PAGE
                    ):
                        with patch.object(
                            publish_changed, "push_artifact", return_value=pushed
                        ) as push:
                            result = publish_changed.publish_manifest(
                                manifest_path,
                                state_dir,
                                dry_run=False,
                                check_drift=True,
                                require_state=True,
                            )

            self.assertEqual(result["drifted"], [])
            self.assertEqual(result["published"], [pushed])
            self.assertEqual(len(result["healed"]), 1)
            self.assertIn("hydrated missing canvas_fingerprint", result["healed"][0]["reason"])
            push.assert_called_once()


if __name__ == "__main__":
    unittest.main()

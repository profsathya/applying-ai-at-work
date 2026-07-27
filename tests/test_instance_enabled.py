"""Tests for the fail-closed scaffold guard (instance.enabled: false).

A manifest whose instance block carries "enabled": false is an unfinished
scaffold; every Canvas-touching entry point must refuse before building a
Canvas client. An absent flag means enabled, so production manifests are
unaffected.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from canvas_sync.instance_guard import (  # noqa: E402
    InstanceDisabledError,
    PlaceholderCourseIdError,
    SENTINEL_COURSE_ID,
    check_course_id_is_real,
    check_instance_enabled,
    check_instance_ready,
)


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def manifest_payload(*, enabled: bool | None, course_id: int = SENTINEL_COURSE_ID) -> dict:
    instance = {
        "name": "deanza",
        "base_url": "https://deanza.instructure.com/",
        "course_id": course_id,
        "term": "TBD",
    }
    if enabled is not None:
        instance["enabled"] = enabled
    return {"instance": instance, "last_sync": None, "artifacts": {}}


def write_manifest(path: Path, *, enabled: bool | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest_payload(enabled=enabled)), encoding="utf-8")


def write_page(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: page
title: "Scaffold Page"
slug: scaffold-page
artifact_id: scaffold-page
sprint: 0
module: "Test Module"
position: 1
points: null
submission_type: none
publish: true
---

# Scaffold Page

Body.
""",
        encoding="utf-8",
    )


def forbidden_client(*args, **kwargs):
    raise AssertionError("Canvas client must not be built for a disabled instance")


class CheckInstanceEnabledTests(unittest.TestCase):
    def test_enabled_false_refuses(self) -> None:
        with self.assertRaises(InstanceDisabledError) as ctx:
            check_instance_enabled(manifest_payload(enabled=False), manifest_label="x.json")
        message = str(ctx.exception)
        self.assertIn("x.json", message)
        self.assertIn("instance.enabled", message)

    def test_absent_flag_means_enabled(self) -> None:
        check_instance_enabled(manifest_payload(enabled=None))

    def test_enabled_true_is_noop(self) -> None:
        check_instance_enabled(manifest_payload(enabled=True))

    def test_repo_deanza_scaffold_is_disabled(self) -> None:
        manifest = json.loads(
            (REPO_ROOT / "course1" / "manifests" / "deanza.json").read_text(encoding="utf-8")
        )
        with self.assertRaises(InstanceDisabledError):
            check_instance_enabled(manifest)

    def test_repo_production_manifests_are_enabled(self) -> None:
        for path in sorted(REPO_ROOT.glob("course*/manifests/production.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            check_instance_enabled(manifest, manifest_label=str(path))


class SentinelCourseIdTests(unittest.TestCase):
    """The placeholder course id refuses independently of instance.enabled."""

    def test_sentinel_refuses_even_when_enabled(self) -> None:
        manifest = manifest_payload(enabled=True)
        with self.assertRaises(PlaceholderCourseIdError) as ctx:
            check_course_id_is_real(manifest, manifest_label="deanza.json")
        self.assertIn("999999999", str(ctx.exception))
        self.assertIn("deanza.json", str(ctx.exception))

    def test_real_course_id_passes(self) -> None:
        check_course_id_is_real(manifest_payload(enabled=True, course_id=180))

    def test_ready_check_enforces_both_guards(self) -> None:
        # enabled false fires first; enabled true still hits the sentinel.
        with self.assertRaises(InstanceDisabledError):
            check_instance_ready(manifest_payload(enabled=False))
        with self.assertRaises(PlaceholderCourseIdError):
            check_instance_ready(manifest_payload(enabled=True))
        check_instance_ready(manifest_payload(enabled=True, course_id=180))

    def test_repo_production_manifests_pass_ready_check(self) -> None:
        for path in sorted(REPO_ROOT.glob("course*/manifests/production.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            check_instance_ready(manifest, manifest_label=str(path))

    def test_entry_points_refuse_sentinel_with_enabled_true(self) -> None:
        """Wiring check: flipping enabled without a real course id still refuses."""
        from canvas_sync import inspect_canvas, publish_changed, push, update_artifact

        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            manifest_path = repo_root / "course1" / "manifests" / "production.json"
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                json.dumps(manifest_payload(enabled=True)), encoding="utf-8"
            )

            with patch.object(publish_changed.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(PlaceholderCourseIdError):
                    publish_changed.drift_for_changed(
                        manifest_path,
                        [{"file": "f", "artifact_id": "a", "state_entry": {"canvas_type": "page", "canvas_id": 1}}],
                    )

            with patch.object(inspect_canvas.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(PlaceholderCourseIdError):
                    inspect_canvas.build_report(
                        manifest_path, include_items=False, include_drift=False
                    )

            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "scaffold-page.md"
            write_page(md_path)
            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", forbidden_client):
                    with self.assertRaises(PlaceholderCourseIdError):
                        push.push_artifact(
                            md_path, manifest_path, state_dir=repo_root / ".canvas-state"
                        )

            with self.assertRaises(PlaceholderCourseIdError):
                update_artifact.get_client(
                    SENTINEL_COURSE_ID,
                    None,
                    manifest=manifest_payload(enabled=True),
                    manifest_label="deanza.json",
                )


class EntryPointRefusalTests(unittest.TestCase):
    """Each Canvas-touching entry point refuses before creating a client."""

    def _repo(self, tmp: str) -> tuple[Path, Path, Path]:
        repo_root = Path(tmp).resolve()
        manifest_path = repo_root / "course1" / "manifests" / "production.json"
        state_dir = repo_root / ".canvas-state"
        write_manifest(manifest_path, enabled=False)
        return repo_root, manifest_path, state_dir

    def test_publish_changed_drift_refuses(self) -> None:
        from canvas_sync import publish_changed

        with tempfile.TemporaryDirectory() as tmp:
            _repo_root, manifest_path, _state_dir = self._repo(tmp)
            with patch.object(publish_changed.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(InstanceDisabledError):
                    publish_changed.drift_for_changed(
                        manifest_path,
                        [{"file": "f", "artifact_id": "a", "state_entry": {"canvas_type": "page", "canvas_id": 1}}],
                    )

    def test_push_artifact_refuses(self) -> None:
        from canvas_sync import push

        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)
            md_path = repo_root / "course1" / "sprints" / "sprint-0" / "scaffold-page.md"
            write_page(md_path)
            with chdir(repo_root):
                with patch.object(push.CanvasClient, "from_env", forbidden_client):
                    with self.assertRaises(InstanceDisabledError):
                        push.push_artifact(md_path, manifest_path, state_dir=state_dir)

    def test_inspect_canvas_refuses(self) -> None:
        from canvas_sync import inspect_canvas

        with tempfile.TemporaryDirectory() as tmp:
            _repo_root, manifest_path, _state_dir = self._repo(tmp)
            with patch.object(inspect_canvas.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(InstanceDisabledError):
                    inspect_canvas.build_report(
                        manifest_path, include_items=False, include_drift=False
                    )

    def test_update_artifact_get_client_refuses(self) -> None:
        from canvas_sync import update_artifact

        with self.assertRaises(InstanceDisabledError):
            update_artifact.get_client(
                999999999,
                None,
                manifest=manifest_payload(enabled=False),
                manifest_label="deanza.json",
            )

    def test_pull_refuses(self) -> None:
        from canvas_sync import pull

        with tempfile.TemporaryDirectory() as tmp:
            _repo_root, manifest_path, _state_dir = self._repo(tmp)
            argv = ["pull.py", "--manifest", str(manifest_path), "--dry-run"]
            with patch.object(pull.CanvasClient, "from_env", forbidden_client):
                with patch.object(sys, "argv", argv):
                    with self.assertRaises(InstanceDisabledError):
                        pull.main()

    def test_remove_refuses(self) -> None:
        from canvas_sync import remove

        with tempfile.TemporaryDirectory() as tmp:
            _repo_root, manifest_path, _state_dir = self._repo(tmp)
            argv = [
                "remove.py",
                "--manifest",
                str(manifest_path),
                "--target",
                "artifact:whatever",
                "--dry-run",
            ]
            # remove.main() reports refusals as a nonzero exit instead of
            # letting the exception escape; the forbidden client still proves
            # no Canvas client was built.
            with patch.object(remove.CanvasClient, "from_env", forbidden_client):
                with patch.object(sys, "argv", argv):
                    self.assertNotEqual(remove.main(), 0)

    def test_hydrate_state_refuses(self) -> None:
        from canvas_sync import hydrate_state
        from canvas_sync.state import state_path_for_manifest

        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)
            manifest = manifest_payload(enabled=False)
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            write_manifest(state_path, enabled=False)
            with patch.object(hydrate_state, "REPO_ROOT", repo_root):
                with patch.object(hydrate_state.CanvasClient, "from_env", forbidden_client):
                    with self.assertRaises(InstanceDisabledError):
                        hydrate_state.hydrate_manifest(manifest_path, state_dir)

    def test_check_drift_refuses(self) -> None:
        from canvas_sync import check_drift
        from canvas_sync.state import state_path_for_manifest

        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)
            manifest = manifest_payload(enabled=False)
            state_path = state_path_for_manifest(manifest_path, state_dir, manifest)
            write_manifest(state_path, enabled=False)
            with patch.object(check_drift, "REPO_ROOT", repo_root):
                with patch.object(check_drift.CanvasClient, "from_env", forbidden_client):
                    with self.assertRaises(InstanceDisabledError):
                        check_drift.check_manifest(manifest_path, state_dir)

    def test_completion_refuses(self) -> None:
        from canvas_sync import completion

        with tempfile.TemporaryDirectory() as tmp:
            repo_root, manifest_path, state_dir = self._repo(tmp)
            with patch.object(completion.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(InstanceDisabledError):
                    completion.build_module_completion_plan(manifest_path, state_dir)

    def test_map_existing_refuses(self) -> None:
        from canvas_sync import map_existing

        with tempfile.TemporaryDirectory() as tmp:
            _repo_root, manifest_path, state_dir = self._repo(tmp)
            with patch.object(map_existing.CanvasClient, "from_env", forbidden_client):
                with self.assertRaises(InstanceDisabledError):
                    map_existing.build_mapping_plan(manifest_path, state_dir)


if __name__ == "__main__":
    unittest.main()

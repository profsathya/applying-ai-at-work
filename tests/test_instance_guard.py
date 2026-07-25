"""Tests for the instance/token guardrail (canvas_sync/instance_guard.py).

Proves that the existing CTI production path still passes the guard and that a
deliberate cross-instance mismatch (a De Anza URL against the CTI profile) is
caught with a message that names both disagreeing values.
"""

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from canvas_sync.instance_guard import (  # noqa: E402
    InstanceMismatchError,
    check_env_matches_instance,
)

PRODUCTION_MANIFEST = REPO_ROOT / "course1" / "manifests" / "production.json"
DEANZA_MANIFEST = REPO_ROOT / "course1" / "manifests" / "deanza.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class InstanceGuardTest(unittest.TestCase):
    def test_production_path_still_passes(self):
        """The current CTI/production case is a no-op (must not raise)."""
        manifest = load(PRODUCTION_MANIFEST)
        # Env URL has no trailing slash (as in .env / CanvasClient); manifest
        # base_url has one. They still match on host.
        check_env_matches_instance(
            manifest, env_url="https://cti-courses.instructure.com"
        )

    def test_trailing_slash_and_case_are_tolerated(self):
        manifest = load(PRODUCTION_MANIFEST)
        check_env_matches_instance(
            manifest, env_url="https://CTI-Courses.instructure.com/"
        )

    def test_deanza_profile_matches_deanza_env(self):
        manifest = load(DEANZA_MANIFEST)
        check_env_matches_instance(
            manifest, env_url="https://deanza.instructure.com"
        )

    def test_deanza_url_against_cti_profile_is_caught(self):
        """A De Anza URL pointed at the CTI profile must be refused, naming both."""
        manifest = load(PRODUCTION_MANIFEST)
        with self.assertRaises(InstanceMismatchError) as ctx:
            check_env_matches_instance(
                manifest,
                env_url="https://deanza.instructure.com",
                manifest_label="course1/manifests/production.json",
            )
        message = str(ctx.exception)
        self.assertIn("deanza.instructure.com", message)
        self.assertIn("cti-courses.instructure.com", message)
        self.assertIn("course1/manifests/production.json", message)

    def test_reads_canvas_api_url_from_environ(self):
        """When env_url is omitted, the check reads CANVAS_API_URL from os.environ."""
        manifest = load(PRODUCTION_MANIFEST)
        with mock.patch.dict(
            os.environ, {"CANVAS_API_URL": "https://deanza.instructure.com"}
        ):
            with self.assertRaises(InstanceMismatchError):
                check_env_matches_instance(manifest)

    def test_unset_environ_is_noop(self):
        """No CANVAS_API_URL set: from_env owns that error, so the guard is a no-op."""
        manifest = load(PRODUCTION_MANIFEST)
        with mock.patch.dict(os.environ, {}, clear=True):
            check_env_matches_instance(manifest, env_url=None)

    def test_empty_env_url_is_noop(self):
        check_env_matches_instance(load(PRODUCTION_MANIFEST), env_url="")

    def test_manifest_without_instance_is_noop(self):
        check_env_matches_instance({"artifacts": {}}, env_url="https://anything.example")


class GuardWiredIntoManifestEntryPointsTest(unittest.TestCase):
    """The guard is enforced by manifest-backed entry points, not only push.py.

    Each check runs before the Canvas client is built, so a mismatch raises
    without any network call. We use a De Anza-style manifest (base_url deanza,
    instance enabled) with a CTI CANVAS_API_URL to force the mismatch. The repo
    deanza.json scaffold is not used here because its instance.enabled false
    guard fires first.
    """

    MISMATCH_ENV = {"CANVAS_API_URL": "https://cti-courses.instructure.com"}

    def _write_enabled_deanza_manifest(self, tmp: str) -> Path:
        manifest_path = Path(tmp) / "course1" / "manifests" / "production.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(
                {
                    "instance": {
                        "name": "deanza",
                        "base_url": "https://deanza.instructure.com/",
                        "course_id": 999999999,
                        "term": "TBD",
                    },
                    "last_sync": None,
                    "artifacts": {},
                }
            ),
            encoding="utf-8",
        )
        return manifest_path

    def test_inspect_canvas_refuses_on_mismatch(self):
        import tempfile

        from canvas_sync import inspect_canvas

        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = self._write_enabled_deanza_manifest(tmp)
            with mock.patch.dict(os.environ, self.MISMATCH_ENV):
                with self.assertRaises(InstanceMismatchError):
                    inspect_canvas.build_report(
                        manifest_path, include_items=False, include_drift=False
                    )

    def test_publish_changed_drift_refuses_on_mismatch(self):
        import tempfile

        from canvas_sync import publish_changed

        with tempfile.TemporaryDirectory() as tmp:
            manifest_path = self._write_enabled_deanza_manifest(tmp)
            with mock.patch.dict(os.environ, self.MISMATCH_ENV):
                with self.assertRaises(InstanceMismatchError):
                    publish_changed.drift_for_changed(manifest_path, [])


if __name__ == "__main__":
    unittest.main()

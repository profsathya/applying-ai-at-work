from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from canvas_sync import init_course
from canvas_sync import push
from canvas_sync.schema import validate_manifest, validate_prd


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def minimal_manifest(course_id: int = 12345) -> dict:
    return {
        "instance": {
            "name": "production",
            "base_url": "https://example.instructure.com/",
            "course_id": course_id,
            "term": "Test Term",
        },
        "last_sync": None,
        "artifacts": {},
    }


def write_module_header(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        """---
type: module_header
title: "Test Module"
slug: test-module
sprint: 0
module: "Test Module"
position: 1
points: null
submission_type: none
publish: true
---

# Test Module

Local setup check.
""",
        encoding="utf-8",
    )


class InitCourseTests(unittest.TestCase):
    def test_creates_valid_directory_scaffold_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            with patch.object(init_course, "REPO_ROOT", repo_root):
                summary = init_course.init_course(
                    course_key="course-test-init",
                    canvas_course_id=999999,
                    base_url="https://example.instructure.com",
                    title="Test Init Course",
                    term="Test Term",
                    instance_name="production",
                    course_code=None,
                    context_spec_source=None,
                    context_spec_inline_file=None,
                    force=False,
                )

            course_dir = repo_root / "course-test-init"
            self.assertTrue((course_dir / "design").is_dir())
            for sprint in range(0, 6):
                self.assertTrue((course_dir / "sprints" / f"sprint-{sprint}").is_dir())
            self.assertTrue((course_dir / "reports").is_dir())

            manifest_path = course_dir / "manifests" / "production.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["instance"]["course_id"], 999999)
            self.assertEqual(manifest["instance"]["base_url"], "https://example.instructure.com/")
            self.assertEqual(validate_manifest(manifest_path), [])

            prd_path = course_dir / "prd.json"
            self.assertEqual(validate_prd(prd_path), [])

            context_path = repo_root / "context" / "course-specs" / "course-test-init-context.md"
            self.assertTrue(context_path.exists())
            self.assertEqual(summary["context_spec_path"], "context/course-specs/course-test-init-context.md")

    def test_rejects_unsafe_course_keys(self) -> None:
        unsafe_keys = [
            "../course3",
            "course 3",
            "course3;rm",
            "Course3",
            "course_3",
            "course3/child",
            "course3.",
        ]
        for key in unsafe_keys:
            with self.subTest(key=key):
                with self.assertRaises(init_course.InitCourseError):
                    init_course.validate_course_key(key)

    def test_refuses_existing_course_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            with patch.object(init_course, "REPO_ROOT", repo_root):
                init_course.init_course(
                    course_key="course-test-init",
                    canvas_course_id=999999,
                    base_url="https://example.instructure.com",
                    title="Test Init Course",
                    term="Test Term",
                    instance_name="production",
                    course_code=None,
                    context_spec_source=None,
                    context_spec_inline_file=None,
                    force=False,
                )
                with self.assertRaises(init_course.InitCourseError):
                    init_course.init_course(
                        course_key="course-test-init",
                        canvas_course_id=999999,
                        base_url="https://example.instructure.com",
                        title="Test Init Course",
                        term="Test Term",
                        instance_name="production",
                        course_code=None,
                        context_spec_source=None,
                        context_spec_inline_file=None,
                        force=False,
                    )


class PushCourseRoutingTests(unittest.TestCase):
    def test_rejects_mismatched_artifact_and_manifest_course_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            with chdir(repo_root):
                md_path = repo_root / "course1" / "sprints" / "sprint-0" / "test-module.md"
                manifest_path = repo_root / "course3" / "manifests" / "production.json"
                write_module_header(md_path)
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(json.dumps(minimal_manifest()), encoding="utf-8")

                with self.assertRaisesRegex(ValueError, "must live under"):
                    push.push_artifact(md_path, manifest_path)

    def test_reads_course_id_from_manifest_not_course_specific_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo_root = Path(tmp).resolve()
            with chdir(repo_root):
                md_path = repo_root / "course3" / "sprints" / "sprint-0" / "test-module.md"
                manifest_path = repo_root / "course3" / "manifests" / "production.json"
                write_module_header(md_path)
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(json.dumps(minimal_manifest(12345)), encoding="utf-8")

                with patch.dict(os.environ, {"COURSE1_CANVAS_ID": "111", "COURSE2_CANVAS_ID": "222"}):
                    with patch.object(push.CanvasClient, "from_env", return_value=object()) as from_env:
                        with patch.object(push, "resolve_or_create_module", return_value=555):
                            result = push.push_artifact(md_path, manifest_path)

                from_env.assert_called_once_with(course_id=12345)
                self.assertEqual(result["canvas_module_id"], 555)
                updated_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertIn("course3/sprints/sprint-0/test-module.md", updated_manifest["artifacts"])


if __name__ == "__main__":
    unittest.main()

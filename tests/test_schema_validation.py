from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from canvas_sync.hosted_html import validate_homepage_metadata
from canvas_sync.schema import validate_artifact


def write_artifact(path: Path, frontmatter: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
{frontmatter.strip()}
---

# Artifact

Complete the activity with a real work example.
""",
        encoding="utf-8",
    )


VALID_AI_DISCUSSION = """
type: discussion
title: "AI Discussion"
slug: ai-discussion
artifact_id: ai-discussion
sprint: 1
module: "Sprint 1"
position: 1
points: 10
submission_type: file_upload
delivery_mode: ai_activity
publish: false
ai_activity:
  activity_id: deanza-course1-ai-discussion
  questions:
    - id: q1
      type: ai-discussion
      prompt: "What assumption should the AI push on?"
"""


class SchemaValidationTests(unittest.TestCase):
    def test_artifact_references_resolve_within_course_and_reject_canvas_urls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            course = Path(tmp) / "course1"
            target = course / "sprints/sprint-1/target.md"
            source = course / "sprints/sprint-1/source.md"
            write_artifact(target, '''
type: page
title: Target
slug: target
artifact_id: target-id
sprint: 1
module: Sprint 1
position: 1
points: null
submission_type: none
publish: false
''')
            write_artifact(source, '''
type: page
title: Source
slug: source
artifact_id: source-id
sprint: 1
module: Sprint 1
position: 2
points: null
submission_type: none
publish: false
''')
            source.write_text(source.read_text() + "\n[Target](artifact:target-id)\n")
            self.assertEqual(validate_artifact(source), [])
            source.write_text(source.read_text().replace("artifact:target-id", "artifact:missing-id"))
            self.assertTrue(any("unknown or non-renderable artifact reference 'missing-id'" in error for error in validate_artifact(source)))
            source.write_text(source.read_text().replace("artifact:missing-id", "artifact:"))
            self.assertTrue(any("invalid artifact reference ''" in error for error in validate_artifact(source)))
            source.write_text(source.read_text().replace(
                "artifact:",
                "https://cti-courses.instructure.com/courses/180/pages/target",
            ))
            self.assertTrue(any("must not contain an instance-specific Canvas course URL" in error for error in validate_artifact(source)))

    def test_homepage_rejects_optional_language_for_required_published_submission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            course = Path(tmp) / 'course1'
            artifact = course / 'sprints/sprint-1/required.md'
            write_artifact(artifact, '''
type: assignment
title: Required
slug: required
artifact_id: required
sprint: 1
module: Sprint 1
position: 1
points: 0
submission_type: text_entry
completion_requirement: must_submit
publish: true
''')
            homepage = course / 'homepage.yaml'
            homepage.write_text('''modules:\n  - sprint: 1\n    groups:\n      - label: Work\n        items:\n          - slug: required\n            meta: "Assignment - submission optional for progress"\n''')
            errors = validate_homepage_metadata(course)
            self.assertTrue(any('required submission as optional' in error for error in errors))
            homepage.write_text('''modules:\n  - sprint: 1\n    groups:\n      - label: Work\n        items:\n          - slug: required\n            meta: "Assignment - submission required for module completion"\n''')
            self.assertEqual(validate_homepage_metadata(course), [])

    def test_ai_activity_discussion_frontmatter_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "course1" / "sprints" / "sprint-1" / "ai-discussion.md"
            write_artifact(artifact, VALID_AI_DISCUSSION)

            self.assertEqual(validate_artifact(artifact), [])

    def test_ai_activity_requires_file_upload_submission(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "course1" / "sprints" / "sprint-1" / "ai-discussion.md"
            write_artifact(artifact, VALID_AI_DISCUSSION.replace("submission_type: file_upload", "submission_type: discussion_topic"))

            errors = validate_artifact(artifact)

            self.assertTrue(any("requires submission_type file_upload" in error for error in errors))

    def test_ai_activity_rejects_native_canvas_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "course1" / "sprints" / "sprint-1" / "ai-quiz.md"
            write_artifact(
                artifact,
                """
type: quiz
title: "AI Quiz"
slug: ai-quiz
artifact_id: ai-quiz
sprint: 1
module: "Sprint 1"
position: 2
points: 5
submission_type: file_upload
delivery_mode: ai_activity
publish: false
questions:
  - type: short_answer
    prompt: "Native question"
ai_activity:
  activity_id: deanza-course1-ai-quiz
  questions:
    - id: q1
      type: open-ended
      prompt: "Activity question"
""",
            )

            errors = validate_artifact(artifact)

            self.assertTrue(any("uses ai_activity.questions" in error for error in errors))

    def test_ai_activity_requires_quiz_or_discussion_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "course1" / "sprints" / "sprint-1" / "ai-assignment.md"
            write_artifact(artifact, VALID_AI_DISCUSSION.replace("type: discussion", "type: assignment"))

            errors = validate_artifact(artifact)

            self.assertTrue(any("only supported for quiz or discussion" in error for error in errors))

    def test_ai_activity_object_requires_ai_delivery_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            artifact = Path(tmp) / "course1" / "sprints" / "sprint-1" / "ai-discussion.md"
            write_artifact(artifact, VALID_AI_DISCUSSION.replace("delivery_mode: ai_activity\n", ""))

            errors = validate_artifact(artifact)

            self.assertTrue(any("ai_activity requires delivery_mode ai_activity" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

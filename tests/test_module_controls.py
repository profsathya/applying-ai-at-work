from datetime import datetime, timezone
from pathlib import Path
from unittest import TestCase

from canvas_sync.module_controls import module_control_payload, verify_module_controls
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.guided_assignment import render_guided_body


class ModuleControlsTests(TestCase):
    def test_prerequisites_resolve_by_identity_and_must_precede_module(self):
        fm = {'prerequisite_modules': ['orientation']}
        artifacts = {'orientation': {'canvas_type': 'module_header', 'canvas_module_id': 1}}
        modules = [{'id': 1, 'position': 1, 'published': True}, {'id': 2, 'position': 2}]
        self.assertEqual(module_control_payload(fm, artifacts, modules, 2),
                         {'prerequisite_module_ids': [1]})
        modules[0]['position'] = 3
        with self.assertRaisesRegex(ValueError, 'preceding'):
            module_control_payload(fm, artifacts, modules, 2)

    def test_canvas_returned_utc_release_is_verified_by_instant(self):
        verify_module_controls({'id': 2, 'unlock_at': '2026-10-19T06:59:00Z'},
                               {'unlock_at': '2026-10-18T23:59:00-07:00'})
        with self.assertRaisesRegex(ValueError, 'unlock_at'):
            verify_module_controls({'id': 2, 'unlock_at': '2026-10-19T07:59:00Z'},
                                   {'unlock_at': '2026-10-18T23:59:00-07:00'})

    def test_course_release_dates_and_reflection_scope(self):
        course = Path(__file__).resolve().parents[1] / 'course1/sprints'
        expected = {16: '2026-10-19T06:59:00+00:00', 15: '2026-11-02T07:59:00+00:00',
                    8: '2026-11-16T07:59:00+00:00', 9: '2026-11-30T07:59:00+00:00'}
        for sprint, instant in expected.items():
            headers = [parse_frontmatter(p)[0] for p in (course / f'sprint-{sprint}').glob('*.md')
                       if parse_frontmatter(p)[0]['type'] == 'module_header']
            self.assertEqual(len(headers), 1)
            release = datetime.fromisoformat(headers[0]['module_unlock_at'])
            self.assertEqual(release.astimezone(timezone.utc).isoformat(), instant)
        for sprint in [14, 16, 15, 8]:
            for p in (course / f'sprint-{sprint}').glob('*reflection*.md'):
                fm, _ = parse_frontmatter(p)
                self.assertEqual((fm['points'], fm['grading_type'], fm['completion_requirement']),
                                 (0, 'pass_fail', 'must_submit'))
                self.assertEqual(validate_artifact(p), [])
        fm, _ = parse_frontmatter(course / 'sprint-14/problem-frame.md')
        self.assertGreater(fm['points'], 0)

    def test_practice_page_retains_quiz_without_submission_or_copy_controls(self):
        p = Path(__file__).resolve().parents[1] / 'course1/sprints/sprint-14/sprint-1-concept-check.md'
        fm, _ = parse_frontmatter(p)
        self.assertEqual(validate_artifact(p), [])
        doc = render_guided_body({**fm, '_assignment_copy_ui': False}, '')
        self.assertIn('Check my answer', doc)
        self.assertIn('No submission or grade', doc)
        self.assertNotIn('id="copy-answers"', doc)
        self.assertNotIn('id="copy-output"', doc)
        self.assertNotIn('reading-submit', doc.split('</style>')[-1].split('<script')[0])
        self.assertNotIn('Download my answers', doc)

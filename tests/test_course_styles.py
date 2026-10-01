"""Theme delivery boundaries and preservation of instructional documents."""
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from canvas_sync.course_styles import apply_course_styles
from canvas_sync.hosted_html import render_hosted_artifact, render_hosted_files
from tests.test_hosted_html import write_ai_discussion, write_manifest, write_page


class CourseStyleTests(unittest.TestCase):
    def test_theme_does_not_change_markup_or_other_courses(self):
        original = '<html><head><title>Test</title></head><body><form><textarea id="answer"></textarea><a href="https://example.org">Submit</a></form><script>window.test = 1;</script></body></html>'
        themed = apply_course_styles(original, 'course1')
        self.assertEqual(re.sub(r'<style data-course-theme="applying-ai-at-work">.*?</style>\n', '', themed, flags=re.S), original)
        self.assertEqual(apply_course_styles(themed, 'course1'), themed)
        self.assertEqual(apply_course_styles(original, 'course2'), original)

    def test_regular_ai_and_index_delivery_preserve_non_style_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / 'course1/manifests/production.json'
            regular = root / 'course1/sprints/sprint-99/tuple-overview.md'
            ai = root / 'course1/sprints/sprint-99/ai-discussion.md'
            write_manifest(manifest)
            write_page(regular)
            write_ai_discussion(ai)
            before, after = root / 'before', root / 'after'
            # Compare the real renderer with and without the theme. JSON, links,
            # task configuration, scripts and authored content must be identical.
            with patch('canvas_sync.hosted_html.apply_course_styles', side_effect=lambda doc, key: doc):
                render_hosted_files(manifest, before, [regular, ai])
            render_hosted_files(manifest, after, [regular, ai])
            html_count = 0
            for baseline in before.rglob('*'):
                if not baseline.is_file():
                    continue
                actual = after / baseline.relative_to(before)
                old, new = baseline.read_text(), actual.read_text()
                if baseline.suffix == '.html':
                    self.assertIn('data-course-theme="applying-ai-at-work"', new)
                    new = re.sub(r'<style data-course-theme="applying-ai-at-work">.*?</style>\n', '', new, flags=re.S)
                    html_count += 1
                self.assertEqual(new, old, str(baseline.relative_to(before)))
            self.assertGreaterEqual(html_count, 5)

    def test_theme_is_included_in_delivery_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / 'course1/manifests/production.json'
            source = root / 'course1/sprints/sprint-99/tuple-overview.md'
            write_manifest(manifest)
            write_page(source)
            with patch('canvas_sync.hosted_html.apply_course_styles', side_effect=lambda doc, key: doc):
                before = render_hosted_artifact(source, manifest, root / 'before')
            after = render_hosted_artifact(source, manifest, root / 'after')
            self.assertNotEqual(before['hosted_hash'], after['hosted_hash'])


if __name__ == '__main__':
    unittest.main()

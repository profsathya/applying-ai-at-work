import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from canvas_sync.preview_module import build_preview, check_browser
from tests.test_hosted_html import write_manifest, write_page, write_ai_discussion


class ModulePreviewTests(unittest.TestCase):
    def fixture(self, root):
        md = root / 'professional-learning/sprints/sprint-99/tuple-overview.md'
        manifest = root / 'professional-learning/manifests/production.json'
        write_page(md)
        write_manifest(manifest)
        return md, manifest

    def test_baseline_keeps_original_render_and_assets_across_slug_change(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            md, manifest = self.fixture(root)
            image = md.parent / 'assets/example.webp'
            image.parent.mkdir(); image.write_bytes(b'original image bytes')
            md.write_text(md.read_text() + '\n![The relationship](assets/example.webp)\n')
            original_source = md.read_bytes()
            before = root / 'before'
            first = build_preview(manifest, 99, before)
            self.assertEqual(md.read_bytes(), original_source)
            self.assertEqual(first['browser_status'], 'not_run')
            self.assertIn('professional-learning', first['pages'][0]['after'])
            old_html = (before / first['pages'][0]['after']).read_bytes()
            md.write_text(md.read_text().replace('slug: tuple-overview', 'slug: renamed-overview') + '\nOne more explanation.\n')
            image.write_bytes(b'revised image bytes')
            after = root / 'after'
            second = build_preview(manifest, 99, after, before)
            item = second['pages'][0]
            self.assertEqual(item['status'], 'matched')  # Identity, not slug, matches a revision.
            self.assertEqual(item['metadata_changes'], ['slug'])
            self.assertEqual((after / item['before']).read_bytes(), old_html)
            self.assertEqual((before / first['pages'][0]['after']).read_bytes(), old_html)
            self.assertIn(b'original image bytes', [p.read_bytes() for p in (after / 'baseline').rglob('*.webp')])
            self.assertIn(b'revised image bytes', [p.read_bytes() for p in (after / 'current').rglob('*.webp')])
            self.assertGreater(item['counts']['body'], item['before_counts']['body'])
            self.assertEqual(second['manual_review'], 'pending')

    def test_invalid_sources_and_output_overlap_fail_without_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); md, manifest = self.fixture(root)
            with self.assertRaisesRegex(ValueError, 'separate from course source'):
                build_preview(manifest, 99, md.parent / 'preview')
            with self.assertRaisesRegex(ValueError, 'No artifacts'):
                build_preview(manifest, 98, root / 'empty')
            md.write_text(md.read_text() + '\n![Missing](assets/no.png)\n')
            with self.assertRaisesRegex(ValueError, 'missing local image'):
                build_preview(manifest, 99, root / 'invalid')
            self.assertFalse((root / 'invalid').exists())

    def test_existing_output_wrong_baseline_and_ai_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); md, manifest = self.fixture(root)
            before = root / 'before'; build_preview(manifest, 99, before)
            with self.assertRaisesRegex(ValueError, 'new or empty'):
                build_preview(manifest, 99, before)
            record = json.loads((before / 'preview.json').read_text()); record['course'] = 'another-course'
            (before / 'preview.json').write_text(json.dumps(record))
            with self.assertRaisesRegex(ValueError, 'same course'):
                build_preview(manifest, 99, root / 'after', before)
            write_ai_discussion(md.parent / 'ai-discussion.md')
            result = build_preview(manifest, 99, root / 'ai-preview')
            self.assertIsNone(result['pages'][1]['after'])
            self.assertIn('delivery-specific', result['pages'][1]['skipped'])

    def test_browser_start_failure_is_recorded_as_failed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); md, manifest = self.fixture(root)
            output = root / 'preview'; build_preview(manifest, 99, output)
            with patch('canvas_sync.preview_module.subprocess.run', side_effect=FileNotFoundError('Node not found')):
                self.assertEqual(check_browser(output), 1)
            self.assertEqual(json.loads((output / 'preview.json').read_text())['browser_status'], 'failed')
            self.assertEqual(json.loads((output / 'browser-results.json').read_text())['status'], 'failed')
            self.assertIn('Node not found', (output / 'browser.log').read_text())


if __name__ == '__main__':
    unittest.main()

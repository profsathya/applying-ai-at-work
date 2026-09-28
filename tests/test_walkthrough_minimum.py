"""Opt-in Word download minimums and response recovery."""
import copy
import shutil
import subprocess
import unittest
from pathlib import Path

import jsonschema

from canvas_sync.schema import load_schema, validate_guided_assignment
from canvas_sync.walkthrough import render_walkthrough_body

ROOT = Path(__file__).resolve().parents[1]


def artifact():
    return {'type': 'assignment', 'title': 'Frames', 'slug': 'frames', 'artifact_id': 'frames',
            'sprint': 1, 'module': 'Module', 'position': 2, 'publish': False,
            'submission_type': 'file_upload', 'delivery_mode': 'guided_assignment',
            'walkthrough_after': 'source', 'guided_assignment': {
                'version': '1', 'presentation': 'walkthrough', 'export_filename': 'frames.docx',
                'feedback_omission_reason': 'Independent work.', 'tasks': [
                    {'id': 'frame-1', 'kind': 'response', 'prompt': 'Frame 1',
                     'criteria': ['Name the people and their costs.'], 'min_response_chars': 100}]}}


class WalkthroughMinimumTests(unittest.TestCase):
    def test_schema_rejects_invalid_or_unsupported_minimums(self):
        schema = load_schema('frontmatter')
        fm = artifact()
        jsonschema.validate(fm, schema)
        self.assertEqual(validate_guided_assignment('test', fm), [])
        for value in (0, -1, 16001, 1.5, True, '100'):
            invalid = copy.deepcopy(fm)
            invalid['guided_assignment']['tasks'][0]['min_response_chars'] = value
            with self.subTest(value=value), self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(invalid, schema)
        for change in ('reading', 'text_entry', 'pdf_from_document', 'group', 'no_export'):
            invalid = copy.deepcopy(fm)
            config = invalid['guided_assignment']
            if change == 'reading': config['presentation'] = change
            elif change == 'text_entry': invalid['submission_type'] = change
            elif change == 'pdf_from_document': config['submission_format'] = change
            elif change == 'group': config['tasks'][0].update(kind='group', fields=[], repeat_count=1)
            else: config.pop('export_filename')
            with self.subTest(change=change):
                self.assertTrue(any('min_response_chars requires' in e
                                    for e in validate_guided_assignment('test', invalid)))

    def test_render_has_accessible_disabled_download_and_recovery(self):
        fm = artifact()
        rendered = render_walkthrough_body(fm, '', {}).split('<script')[0]
        self.assertIn('id="walk-download" disabled aria-describedby="walk-download-requirements"', rendered)
        self.assertIn('Frame 1', rendered)
        self.assertIn('id="walk-recovery" hidden', rendered)
        self.assertNotIn('id="walk-copy"', rendered)
        self.assertLess(rendered.index('data-walk-answer="frame-1"'), rendered.index('class="walk-check"'))
        fm['guided_assignment']['tasks'][0].pop('min_response_chars')
        unguarded = render_walkthrough_body(fm, '', {}).split('<script')[0]
        self.assertNotIn('walk-download-requirements', unguarded)
        self.assertIn('id="walk-download">', unguarded)

    @unittest.skipUnless(shutil.which('node'), 'Node required for shipped runtime checks')
    def test_shipped_runtime(self):
        subprocess.run(['node', 'tests/walkthrough_minimum_runtime.cjs'], cwd=ROOT, check=True)


if __name__ == '__main__':
    unittest.main()

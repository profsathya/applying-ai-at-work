"""Opt-in Chromium regression for the standard walk-through module preview checker."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from canvas_sync.preview_module import check_browser
from canvas_sync.walkthrough import render_walkthrough_body
from canvas_sync.walkthrough_tables import create_task
from tests.test_walkthrough_tables import candidate_task, rectangular_block


class WalkthroughPreviewBrowserTests(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('PLAYWRIGHT_MODULE') and os.environ.get('BROWSER_EXECUTABLE'),
                         'Set PLAYWRIGHT_MODULE and BROWSER_EXECUTABLE to run Chromium preview checks')
    def test_table_and_non_table_walkthroughs_in_normal_preview(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / 'current').mkdir()
            (output / 'baseline').mkdir()

            def write_page(path, title, artifact_id, tasks, *, feedback=False, submission='text_entry'):
                config = {'version': '1', 'presentation': 'walkthrough',
                          'export_filename': 'review.docx', 'tasks': tasks}
                if feedback:
                    config.update(feedback_endpoint='https://example.invalid/.netlify/functions/walkthrough-feedback',
                                  feedback_protocol='walkthrough-v1')
                else:
                    config['feedback_omission_reason'] = 'Source activity does not permit AI feedback.'
                frontmatter = {'type': 'assignment', 'title': title, 'artifact_id': artifact_id,
                               'submission_type': submission, 'delivery_mode': 'guided_assignment',
                               'walkthrough_after': 'source-example', 'guided_assignment': config}
                path.write_text('<!doctype html><html lang="en"><meta charset="utf-8">'
                                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                                f'<h1>{title}</h1>' + render_walkthrough_body(frontmatter, '', {}) + '</html>')

            candidate = candidate_task()
            reference = create_task(rectangular_block(2), 'reference', 'Read the reference grid', read_only=True)
            wide = create_task(rectangular_block(5), 'wide-grid', 'Complete the wide grid',
                               ['Check your entry.'], response_cells={(2, 1), (3, 5)})
            write_page(output / 'baseline/table.html', 'Table Activity', 'table-activity',
                       [candidate], feedback=True)
            write_page(output / 'current/table.html', 'Table Activity', 'table-activity',
                       [candidate, reference, wide], feedback=True)
            write_page(output / 'current/non-table.html', 'Non-Table Activity', 'non-table-activity',
                       [{'id': 'reflection', 'kind': 'response', 'prompt': 'Reflect',
                         'criteria': ['Be specific.']}], feedback=True)
            write_page(output / 'current/file-upload.html', 'File Upload Activity', 'file-upload-activity',
                       [{'id': 'reflection', 'kind': 'response', 'prompt': 'Reflect',
                         'criteria': ['Be specific.']}], submission='file_upload')
            (output / 'comparison.html').write_text('<!doctype html><html lang="en"><select id="page">'
                                                    '<option>Table</option><option>Non-table</option>'
                                                    '<option>File upload</option></select>')
            (output / 'preview.json').write_text(json.dumps({
                'version': 1, 'course': 'test', 'sprint': 1,
                'pages': [
                    {'id': 'table-activity', 'title': 'Table Activity', 'after': 'current/table.html',
                     'before': 'baseline/table.html'},
                    {'id': 'non-table-activity', 'title': 'Non-Table Activity',
                     'after': 'current/non-table.html', 'before': None},
                    {'id': 'file-upload-activity', 'title': 'File Upload Activity',
                     'after': 'current/file-upload.html', 'before': None},
                ],
            }))
            code = check_browser(output, node=os.environ.get('NODE_BIN', 'node'),
                                 playwright_module=os.environ['PLAYWRIGHT_MODULE'],
                                 browser_executable=os.environ['BROWSER_EXECUTABLE'])
            report = json.loads((output / 'browser-results.json').read_text())
            self.assertEqual(code, 2, report)
            self.assertEqual(report['status'], 'partial')  # Live AI request is deliberately blocked.
            self.assertTrue(all(not page['errors'] for page in report['results']), report)
            table_checks = report['results'][0]['checks']
            self.assertTrue(any('baseline drafts restored' in check for check in table_checks))
            self.assertIn('row feedback preview and below-table result', table_checks)
            self.assertIn('rich clipboard tables and plain text retain grid, answers, and source text', table_checks)
            self.assertIn('Word export retains table grids and answers', table_checks)
            self.assertIn('table horizontal scrolling on narrow screens', table_checks)
            self.assertIn('desktop/mobile overflow and enlarged base text', table_checks)
            self.assertIn('clipboard-denial text fallback', report['results'][1]['checks'])
            self.assertIn('non-table step feedback preview', report['results'][1]['checks'])
            self.assertIn('file-upload Word document retains answers', report['results'][2]['checks'])
            self.assertTrue(all('walk-through context and Canvas submission action' in page['checks']
                                for page in report['results']))
            self.assertTrue(all('AI feedback controls cover every writable step or have a recorded exception'
                                in page['checks'] for page in report['results']))


if __name__ == '__main__':
    unittest.main()

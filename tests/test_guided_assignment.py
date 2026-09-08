from __future__ import annotations
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import yaml
from canvas_sync.schema import validate_artifact
from canvas_sync.guided_assignment import render_guided_body

ROOT = Path(__file__).resolve().parent.parent


def frontmatter():
    return {'type': 'assignment', 'title': 'Decide with evidence', 'slug': 'decide', 'artifact_id': 'decide',
            'sprint': 11, 'module': 'Sprint One', 'position': 7, 'points': 20, 'publish': False,
            'submission_type': 'text_entry', 'delivery_mode': 'guided_assignment',
            'guided_assignment': {'version': '1', 'tasks': [{'id': 'reasons', 'prompt': 'Give your reasons.',
             'criteria': ['Name a deciding check.']}, {'id': 'check', 'kind': 'choice', 'prompt': 'Which describes a gap?',
             'criteria': ['Compare current and possible states.'], 'options': ['A complaint', 'A gap'], 'correct_index': 1,
             'explanation': 'The gap compares what happens now with what could happen.'}]}}


class GuidedAssignmentTests(unittest.TestCase):
    def validate(self, fm):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'page.md'; p.write_text('---\n' + yaml.safe_dump(fm) + '---\n\nSource instructions.\n')
            return validate_artifact(p)

    def test_plain_text_canvas_delivery_and_question_shape(self):
        fm = frontmatter(); self.assertEqual(self.validate(fm), [])
        fm['submission_type'] = 'file_upload'; self.assertTrue(any('text_entry' in e for e in self.validate(fm)))
        fm['submission_type'] = 'text_entry'; fm['guided_assignment']['tasks'][1]['correct_index'] = 2
        self.assertTrue(any('outside options' in e for e in self.validate(fm)))

    def test_no_ambiguous_native_or_ai_payload_and_unique_task_ids(self):
        fm = frontmatter(); fm['questions'] = [{'type': 'essay', 'prompt': 'Wrong route'}]
        self.assertTrue(any('native quiz' in e for e in self.validate(fm)))
        fm.pop('questions'); fm['guided_assignment']['tasks'][1]['id'] = 'reasons'
        self.assertTrue(any('unique' in e for e in self.validate(fm)))
        fm['delivery_mode'] = 'canvas_native'
        self.assertTrue(any('requires its delivery mode' in e for e in self.validate(fm)))

    def test_render_escapes_configuration_and_retains_full_authored_guidance(self):
        fm = frontmatter(); fm['guided_assignment']['tasks'][0]['prompt'] = '</script><img src=x onerror=bad()>'
        result = render_guided_body(fm, '<section><p>Original authored wording.</p></section>')
        self.assertIn('<p>Original authored wording.</p>', result)
        self.assertNotIn('<img src=x', result)
        self.assertIn('\\u003c/script\\u003e', result)
        self.assertIn('Copy my answers', result)
        self.assertNotIn('data-feedback="reasons"', result)

    @unittest.skipUnless(shutil.which('node'), 'Node required for browser-script behavioral tests')
    def test_response_script_behavior(self):
        proc = subprocess.run(['node', str(ROOT / 'tests/guided_assignment_runtime.cjs')], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn('guided runtime passed', proc.stdout)

from __future__ import annotations
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml
from canvas_sync import push
from canvas_sync.schema import validate_artifact, validate_canvas_state, validate_manifest
from canvas_sync.guided_assignment import render_guided_body
from canvas_sync.maintenance_state import MaintenanceState
from tests.test_canvas_state import chdir, write_manifest

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
    def test_publish_persists_guided_delivery_in_valid_maintenance_state(self):
        class Client:
            def create_assignment(self, payload):
                self.assignment = {'id': 17, **payload}
                return self.assignment

            def get_assignment(self, assignment_id):
                return self.assignment

            def add_module_item(self, module_id, **kwargs):
                return {'id': 29, 'module_id': module_id, **kwargs}

        for external in (False, True):
            with self.subTest(external=external), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                md = root / 'course1/sprints/sprint-11/decide.md'
                manifest = root / 'course1/manifests/production.json'
                state_dir = root / 'canvas-state' if external else None
                md.parent.mkdir(parents=True)
                md.write_text('---\n' + yaml.safe_dump(frontmatter()) + '---\n\nInstructions.\n')
                write_manifest(manifest)
                with chdir(root), patch.object(push.CanvasClient, 'from_env', return_value=Client()), patch.object(push, 'resolve_or_create_module', return_value=8):
                    result = push.push_artifact(md, manifest, state_dir=state_dir)
                state_path = Path(result['state_path'])
                validator = validate_canvas_state if external else validate_manifest
                self.assertEqual(validator(state_path), [])
                persisted = json.loads(state_path.read_text())['artifacts']
                entry = next(iter(persisted.values()))
                self.assertEqual(entry['delivery_mode'], 'guided_assignment')
                self.assertEqual(entry['canvas_type'], 'assignment')
                self.assertEqual(entry['canvas_id'], 17)
                MaintenanceState(manifest, root, state_dir).load()

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

from __future__ import annotations
import json
import hashlib
import html
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import yaml
from canvas_sync import push
from canvas_sync.schema import parse_frontmatter, validate_artifact, validate_canvas_state, validate_manifest
from canvas_sync.guided_assignment import (DOJO_PRIVACY_NOTICE, DOJO_TRANSCRIPT_SOURCE_AUTHORITY,
                                           DOJO_TRANSCRIPT_TASK_PROMPT,
                                           load_dojo_transcript_prompt, render_guided_body)
from canvas_sync.hosted_html import markdown_body_to_html, render_artifact_document
from canvas_sync.instruction_sections import partition_instruction_sections
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


def dojo_frontmatter():
    fm = frontmatter()
    fm.update(title='Dojo Lab: decide', slug='dojo-lab-decide', publish=True,
              completion_requirement='must_submit', dojo_submission={'mode': 'transcript', 'prompt_version': 'v1'})
    fm['guided_assignment'] = {
        'version': '2.0',
        'standing_instruction': 'Submit the complete transcript.',
        'tasks': [{'id': 'dojo-transcript', 'kind': 'response', 'prompt': DOJO_TRANSCRIPT_TASK_PROMPT,
                   'criteria': ['Include every turn.', 'Keep every CONTINUED marker.']}],
    }
    return fm


class GuidedAssignmentTests(unittest.TestCase):
    def test_dojo_transcript_registry_render_and_canonical_artifacts(self):
        prompt = load_dojo_transcript_prompt('v1')
        self.assertEqual(hashlib.sha256(prompt.encode()).hexdigest(),
                         'd0ae8bbe651ab92bb2b45b08abd1419d2bacf0e1848f7246d8a57079626cfbfb')
        self.assertTrue(prompt.endswith('\n'))
        registry_record = json.loads((ROOT / 'canvas_sync/assets/dojo-transcript-prompt-v1.json').read_text())
        self.assertEqual(registry_record['source_authority'], DOJO_TRANSCRIPT_SOURCE_AUTHORITY)
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            load_dojo_transcript_prompt('v99')
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / 'dojo-transcript-prompt-v1.json'
            registry.write_text(json.dumps({'version': 'v1', 'source_authority': DOJO_TRANSCRIPT_SOURCE_AUTHORITY,
                                            'sha256': '0' * 64, 'text': prompt}))
            with patch('canvas_sync.guided_assignment.ASSETS', Path(tmp)):
                with self.assertRaisesRegex(ValueError, 'digest mismatch'):
                    load_dojo_transcript_prompt('v1')

        fm = dojo_frontmatter()
        self.assertEqual(self.validate(fm), [])
        rendered = render_guided_body(fm, '<p>First authored AI prompt.</p>')
        self.assertLess(rendered.index(html.escape(DOJO_PRIVACY_NOTICE)), rendered.index('First authored AI prompt.'))
        match = re.search(r'<textarea id="transcript-request-text"[^>]*>(.*?)</textarea>', rendered, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(html.unescape(match.group(1)), prompt)
        editable = [tag for tag in re.findall(r'<textarea\b[^>]*>', rendered) if 'readonly' not in tag]
        self.assertEqual(len(editable), 1)
        self.assertIn('data-answer="dojo-transcript"', editable[0])
        self.assertNotIn('maxlength=', editable[0])
        self.assertIn('The complete transcript is the only evidence you submit for this Dojo Lab.', rendered)
        self.assertIn('Copy transcript request', rendered)
        self.assertIn('Copy transcript', rendered)
        self.assertIn('maxlength="20000"', render_guided_body(frontmatter(), '<p>Instructions.</p>'))

        for relative in (
            'course1/sprints/sprint-14/dojo-lab-test-widen-choose.md',
            'course1/sprints/sprint-15/dojo-lab-test-widen-choose-v3.md',
            'course1/sprints/sprint-8/dojo-lab-design-the-learning-path-v3.md',
        ):
            with self.subTest(relative=relative):
                path = ROOT / relative
                self.assertEqual(validate_artifact(path), [])
                actual_fm, body = parse_frontmatter(path)
                actual = render_guided_body(actual_fm, markdown_body_to_html(body))
                self.assertEqual(actual.count('data-answer="dojo-transcript"'), 1)
                self.assertEqual(actual.count('id="copy-answers"'), 1)
                request = re.search(r'<textarea id="transcript-request-text"[^>]*>(.*?)</textarea>', actual, re.S)
                self.assertEqual(html.unescape(request.group(1)), prompt)
                editable = [tag for tag in re.findall(r'<textarea\b[^>]*>', actual) if 'readonly' not in tag]
                self.assertEqual(len(editable), 1)
                self.assertNotIn('maxlength=', editable[0])

    def test_dojo_transcript_semantic_mutations_fail_closed(self):
        cases = {
            'wrong type': ('type', 'page'),
            'wrong submission': ('submission_type', 'file_upload'),
            'wrong completion': ('completion_requirement', 'must_view'),
            'wrong delivery': ('delivery_mode', 'canvas_native'),
        }
        for name, (key, value) in cases.items():
            fm = dojo_frontmatter(); fm[key] = value
            with self.subTest(name=name):
                self.assertTrue(self.validate(fm))
        for mutation in ('extra task', 'wrong id', 'wrong kind', 'wrong prompt'):
            fm = dojo_frontmatter(); task = fm['guided_assignment']['tasks'][0]
            if mutation == 'extra task':
                fm['guided_assignment']['tasks'].append(dict(task, id='other'))
            elif mutation == 'wrong id':
                task['id'] = 'other'
            elif mutation == 'wrong kind':
                task.update(kind='choice', options=['A', 'B'], correct_index=0, explanation='A')
            else:
                task['prompt'] = 'Paste a summary.'
            with self.subTest(mutation=mutation):
                self.assertTrue(any('dojo-transcript' in error or 'longer' in error for error in self.validate(fm)))
        fm = dojo_frontmatter(); fm.pop('dojo_submission')
        self.assertTrue(any('canonical Dojo' in error for error in self.validate(fm)))
        fm['publish'] = False
        self.assertEqual(self.validate(fm), [])
    def test_compact_presentation_is_opt_in_single_response_and_keeps_tools(self):
        fm = frontmatter()
        g = fm['guided_assignment']
        g['presentation'] = 'compact'
        g['tasks'] = g['tasks'][:1]
        g['tasks'][0]['instruction_section'] = 'Build'
        body = '## Start\n\nStart here.\n\n## Build\n\nBuild from your observations.\n'
        self.assertEqual(self.validate(fm, body), [])
        result = render_artifact_document(fm, body,
            {'canvas_base_url': 'https://example.invalid', 'canvas_course_id': 180},
            {'hosted_path': 'deanza/course1/pages/decide.html'}, {})
        self.assertIn('guided-workspace guided-compact', result)
        self.assertEqual(result.count('data-answer="reasons"'), 1)
        self.assertEqual(result.count('id="copy-answers"'), 1)
        self.assertIn('<details id="more-options"><summary>More options</summary>', result)
        self.assertLess(result.index('id="more-options"'), result.index('id="copy-tasks"'))
        self.assertLess(result.index('id="more-options"'), result.index('id="copy-output"'))
        self.assertNotIn('<div class="submit">', result)
        self.assertNotIn('class="full-instructions"', result)
        g['tasks'].append({'id': 'other', 'prompt': 'Other', 'criteria': ['Other']})
        self.assertTrue(any('one response' in e for e in self.validate(fm, body)))
        g['tasks'] = g['tasks'][:1]
        g['tasks'][0].pop('instruction_section')
        self.assertTrue(any('one response' in e for e in self.validate(fm, body)))
        g['tasks'][0]['instruction_section'] = 'Build'
        g['feedback_endpoint'] = 'https://example.invalid/feedback'
        self.assertTrue(any('AI feedback' in e for e in self.validate(fm, body)))

    def test_reading_preserves_mixed_tasks_and_uses_one_export_area(self):
        fm = frontmatter()
        fm['guided_assignment']['presentation'] = 'reading'
        fm['guided_assignment']['tasks'][0]['instruction_section'] = 'Reasons'
        body = 'Opening.\n\n## Reasons\n\nUse your evidence.\n'
        self.assertEqual(self.validate(fm, body), [])
        result = render_artifact_document(fm, body,
            {'canvas_base_url': 'https://example.invalid', 'canvas_course_id': 180},
            {'hosted_path': 'deanza/course1/pages/decide.html'}, {})
        self.assertIn('guided-workspace guided-reading', result)
        self.assertEqual(result.count('data-answer="reasons"'), 1)
        self.assertIn('fieldset aria-labelledby="question-check"', result)
        self.assertEqual(result.count('name="check"'), 2)
        self.assertEqual(result.count('Use your evidence.'), 1)
        self.assertLess(result.index('Use your evidence.'), result.index('data-answer="reasons"'))
        self.assertEqual(result.count('<summary>Self-check</summary>'), 1)
        self.assertEqual(result.count('id="copy-answers"'), 1)
        self.assertLess(result.index('id="more-options"'), result.index('id="copy-output"'))
        self.assertNotIn('<div class="submit">', result)
        self.assertIn('question 2</span>', result)
        fm['guided_assignment']['feedback_endpoint'] = 'https://example.invalid/feedback'
        self.assertTrue(any('AI feedback' in e for e in self.validate(fm, body)))

    def test_reading_page_is_opt_in_and_rejects_assignments(self):
        fm = frontmatter()
        fm.pop('guided_assignment'); fm.pop('delivery_mode')
        fm['page_presentation'] = 'reading'
        self.assertTrue(any('requires a page' in e for e in self.validate(fm)))
        fm['type'] = 'page'; fm['submission_type'] = 'none'; fm['points'] = None
        self.assertEqual(self.validate(fm), [])
        result = render_artifact_document(fm, '## Route\n\nRead here.', {}, {'hosted_path':'course1/pages/test.html'})
        self.assertIn('class="activity reading-page"', result)
        self.assertNotIn('What counts as done', result)
        self.assertNotIn('<h2>Learning goal</h2>', result)
        fm.pop('page_presentation')
        legacy = render_artifact_document(fm, '## Route\n\nRead here.', {}, {'hosted_path':'course1/pages/test.html'})
        self.assertNotIn('class="activity reading-page"', legacy)
        self.assertNotIn('Opt-in reading layouts', legacy)

    def test_reading_discussion_keeps_native_submission_and_settings(self):
        fm = frontmatter()
        fm.pop('guided_assignment'); fm.pop('delivery_mode')
        fm.update(type='discussion', submission_type='discussion_topic', points=0,
                  grading_type='pass_fail', omit_from_final_grade=True,
                  completion_requirement='must_contribute', learner_labels=True,
                  page_presentation='reading')
        self.assertEqual(self.validate(fm), [])
        original = dict(fm)
        manifest = {'instance': {'base_url': 'https://example.invalid', 'course_id': 180}}
        body = 'Introduce yourself.\n\n## Share\n\n- Your interests.\n'
        result = render_artifact_document(fm, body, manifest,
            {'hosted_path': 'course1/activities/intro.html'},
            {'canvas_type': 'discussion', 'canvas_id': 1533})
        self.assertEqual(fm, original)
        self.assertIn('class="activity reading-page"', result)
        self.assertNotIn('<h2>Overview</h2>', result)
        self.assertEqual(result.count('<div class="submit">'), 1)
        self.assertIn('https://example.invalid/courses/180/discussion_topics/1533', result)
        self.assertIn('Peer replies are optional.', result)
        self.assertNotIn('id="copy-answers"', result)
        fm.pop('page_presentation')
        legacy = render_artifact_document(fm, body, manifest,
            {'hosted_path': 'course1/activities/intro.html'}, {'canvas_id': 1533})
        self.assertNotIn('class="activity reading-page"', legacy)
        self.assertIn('<h2>Overview</h2>', legacy)

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

    def validate(self, fm, body='Source instructions.\n'):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'page.md'; p.write_text('---\n' + yaml.safe_dump(fm) + '---\n\n' + body)
            return validate_artifact(p)

    def test_instruction_references_require_one_unique_top_level_heading(self):
        fm = frontmatter()
        task = fm['guided_assignment']['tasks'][0]
        task['instruction_section'] = 'Find & compare'
        body = '## Find & compare\n\nA worked example.\n\n### A detail\n\nUse this detail.\n'
        self.assertEqual(self.validate(fm, body), [])
        for bad in ['', '## Something else\n', body + '\n## Find & compare\nAgain.',
                    '> ## Find & compare\n> Nested in a quote.\n',
                    '```\n## Find & compare\n```\n']:
            with self.subTest(body=bad):
                self.assertTrue(any('exactly one' in error for error in self.validate(fm, bad)))
        fm['guided_assignment']['tasks'][1]['instruction_section'] = 'Find & compare'
        self.assertTrue(any('only one task' in error for error in self.validate(fm, body)))
        task['instruction_section'] = '   '
        self.assertTrue(any('nonempty' in error for error in self.validate(fm, body)))

    def test_section_order_and_remaining_teaching(self):
        tasks = [{'id': 'b', 'instruction_section': 'Second'}, {'id': 'a', 'instruction_section': 'First & foremost'}]
        rendered = markdown_body_to_html('Opening.\n\n## First & **foremost**\n\nFirst example.\n\n'
                                         '### Detail\n\nFirst detail.\n\n## Extra\n\nShared context.\n\n'
                                         '## Second\n\nSecond example.\n')
        remainder, sections = partition_instruction_sections(rendered, tasks)
        self.assertIn('Shared context.', remainder)
        self.assertNotIn('First example.', remainder)
        self.assertEqual(list(sections), ['b', 'a'])
        self.assertIn('First detail.', sections['a'])
        self.assertNotIn('Shared context.', sections['a'])
        self.assertEqual(partition_instruction_sections(rendered, []), (rendered, {}))

    def test_hosted_teaching_precedes_each_task_once_and_legacy_is_unchanged(self):
        fm = frontmatter()
        fm['guided_assignment']['tasks'][0]['instruction_section'] = 'Reasons'
        fm['guided_assignment']['tasks'][1]['instruction_section'] = 'Distinguish'
        body = '# Decide\n\nShared prerequisite.\n\n## Distinguish\n\nChoice example.\n\n## Reasons\n\nReason example.\n'
        kwargs = {'manifest': {'canvas_base_url': 'https://example.invalid', 'canvas_course_id': 180},
                  'hosted_info': {'hosted_path': 'deanza/course1/pages/decide.html'}, 'state_entry': {}}
        result = render_artifact_document(fm, body, **kwargs)
        self.assertNotIn('class="full-instructions"', result)
        for text in ('Shared prerequisite.', 'Choice example.', 'Reason example.'):
            self.assertEqual(result.count(text), 1)
        self.assertLess(result.index('Reason example.'), result.index('data-task="reasons"'))
        self.assertLess(result.index('data-task="reasons"'), result.index('Choice example.'))
        self.assertLess(result.index('Choice example.'), result.index('data-task="check"'))
        self.assertLess(result.index('data-task="check"'), result.index('id="copy-tasks"'))
        self.assertIn('<details><summary>Self-check</summary>', result)
        legacy = render_artifact_document(frontmatter(), body, **kwargs)
        self.assertIn('class="full-instructions"', legacy)
        self.assertEqual(legacy.count('Reason example.'), 1)
        self.assertNotIn('class="task-teaching"', legacy)
        self.assertIn('<details><summary>Guidance and self-check</summary>', legacy)
        self.assertLess(legacy.index('id="copy-tasks"'), legacy.index('data-task="reasons"'))

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

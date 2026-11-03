import copy
from pathlib import Path
import unittest
from unittest.mock import patch

from canvas_sync.hosted_html import iframe_shell
from canvas_sync.state import canvas_fingerprint
from maintenance.retire_course180_context_reading import (
    ARTIFACT, HOSTED, ITEM, MODULE, PATH, SLUG, ScopedClient, digest, prepare, prepare_progress, verify_after,
)


class ContextRetirementTests(unittest.TestCase):
    def setUp(self):
        self.source = (Path(__file__).resolve().parents[1] / PATH).read_bytes()
        self.previous = self.source.replace(b'publish: false\n', b'publish: true\n')
        self.page = {'page_id': 3627, 'url': SLUG, 'title': 'Working with AI: Context',
                     'body': iframe_shell(HOSTED, 'Working with AI: Context'),
                     'published': False, 'hide_from_students': True, 'front_page': False}
        self.entry = {'artifact_id': ARTIFACT, 'local_path': PATH, 'canvas_type': 'page',
                      'canvas_id': 3627, 'canvas_page_url': SLUG, 'canvas_module_id': MODULE,
                      'canvas_module_item_id': ITEM, 'completion_requirement': 'must_view',
                      'canvas_fingerprint': canvas_fingerprint({**self.page, 'published': True}, 'page'),
                      'content_hash': digest(self.previous), 'source_commit': 'a' * 40,
                      'hosted_url': HOSTED, 'hosted_hash': 'b' * 64, 'last_pushed': 'old',
                      'canvas_payload_hash': 'old-payload'}
        self.state = {'instance': {'course_id': 180, 'base_url': 'https://cti-courses.instructure.com'},
                      'artifacts': {ARTIFACT: self.entry, 'unrelated': {'canvas_id': 7178}}}
        self.modules = [{'id': MODULE, 'name': 'Sprint 2: Is This Problem Worth Pursuing?',
                         'published': True, 'items_count': 2, 'requirement_type': 'all'},
                        {'id': 2082, 'name': 'Sprint 4', 'published': True, 'items_count': 1}]
        self.items = {MODULE: [
            {'id': 18011, 'type': 'Assignment', 'content_id': 7178, 'position': 3,
             'published': True, 'completion_requirement': {'type': 'must_submit', 'completed': False}},
            {'id': ITEM, 'type': 'Page', 'page_url': SLUG, 'position': 13,
             'published': False, 'completion_requirement': {'type': 'must_view', 'completed': True}}],
            2082: [{'id': 18000, 'type': 'Assignment', 'content_id': 7168, 'position': 1}]}

    def plan(self):
        return prepare(self.state, self.page, self.modules, self.items,
                       self.source, self.previous, 'c' * 40)

    def test_exact_retirement_preserves_page_and_unrelated_state(self):
        before = copy.deepcopy(self.state)
        proposed, report = self.plan()
        self.assertEqual(self.state, before)
        self.assertEqual(proposed['artifacts']['unrelated'], before['artifacts']['unrelated'])
        entry = proposed['artifacts'][ARTIFACT]
        for key in ('canvas_id', 'canvas_page_url', 'canvas_module_id', 'hosted_hash', 'last_pushed'):
            self.assertEqual(entry[key], self.entry[key])
        self.assertIsNone(entry['canvas_module_item_id'])
        self.assertNotIn('completion_requirement', entry)
        self.assertEqual(entry['content_hash'], digest(self.source))
        self.assertEqual(entry['canvas_fingerprint'], canvas_fingerprint(self.page, 'page'))
        self.assertEqual(report['operations'], [{'action': 'delete_module_item', 'module_id': MODULE, 'module_item_id': ITEM}])

    def test_rejects_unreviewed_state_source_shell_visibility_or_placement(self):
        changes = [
            lambda: self.state['instance'].update(course_id=999),
            lambda: self.entry.update(canvas_fingerprint='d' * 64),
            lambda: self.entry.update(content_hash='d' * 64),
            lambda: self.entry.update(canvas_id=999),
            lambda: self.entry.update(canvas_module_item_id=999),
            lambda: self.entry.update(completion_requirement='must_submit'),
            lambda: self.state['artifacts'].update(duplicate=copy.deepcopy(self.entry)),
            lambda: setattr(self, 'source', self.source + b'Changed content.\n'),
            lambda: self.page.update(published=True),
            lambda: self.page.update(body=self.page['body'].replace(HOSTED, 'https://wrong.example')),
            lambda: self.page.update(hide_from_students=False),
            lambda: self.items[MODULE][-1].update(published=True),
            lambda: self.items[MODULE][-1].update(page_url='different'),
            lambda: self.items[MODULE][-1].update(completion_requirement={'type': 'must_submit'}),
            lambda: self.items[2082].append(copy.deepcopy(self.items[MODULE][-1])),
            lambda: self.modules[0].update(published=False),
        ]
        for change in changes:
            with self.subTest(change=change):
                self.setUp()
                change()
                with self.assertRaises(ValueError):
                    self.plan()

    def test_token_binds_source_state_and_live_requirements(self):
        token = self.plan()[1]['confirmation_token']
        self.items[MODULE][0]['completion_requirement']['type'] = 'must_view'
        self.assertNotEqual(token, self.plan()[1]['confirmation_token'])
        self.setUp()
        self.state['artifacts']['unrelated']['canvas_id'] = 999
        self.assertNotEqual(token, self.plan()[1]['confirmation_token'])

    def test_known_canvas_boolean_serialization_still_requires_exact_prior_fingerprint(self):
        self.page['body'] = self.page['body'].replace('allowfullscreen>', 'allowfullscreen="">')
        self.entry['canvas_fingerprint'] = canvas_fingerprint({**self.page, 'published': True}, 'page')
        self.plan()
        self.page['body'] += '<p>Unreviewed edit.</p>'
        with self.assertRaises(ValueError):
            self.plan()

    def test_progress_proposal_clears_exactly_two_fields_and_rejects_identity_drift(self):
        row = {'artifactId': ARTIFACT, 'canvasId': 3627, 'canvasModuleId': MODULE,
               'canvasPageUrl': SLUG, 'canvasType': 'page', 'localPath': PATH,
               'canvasModuleItemId': ITEM, 'completionRequirement': 'must_view'}
        progress = {'canvasCourseId': 180, 'courseKey': 'course1',
                    'items': [row, {'artifactId': 'unrelated', 'canvasModuleItemId': 18011}]}
        result = prepare_progress(progress)
        self.assertEqual(result['items'][1], progress['items'][1])
        self.assertEqual({k for k in row if row[k] != result['items'][0][k]},
                         {'canvasModuleItemId', 'completionRequirement'})
        self.assertEqual(prepare_progress(result), result)
        self.assertEqual(row['canvasModuleItemId'], ITEM)
        for key, value in [('canvasId', 999), ('canvasModuleItemId', 999), ('completionRequirement', 'must_submit')]:
            changed = copy.deepcopy(progress)
            changed['items'][0][key] = value
            with self.assertRaises(ValueError):
                prepare_progress(changed)

    def test_retry_after_placement_delete_and_reconciled_state_is_idempotent(self):
        proposed, _ = self.plan()
        self.items[MODULE].pop()
        self.assertEqual(self.plan()[1]['operations'], [])
        self.state = proposed
        self.entry = proposed['artifacts'][ARTIFACT]
        self.previous = self.source
        again, report = self.plan()
        self.assertEqual(again, proposed)
        self.assertEqual(report['changes'], [])

    def test_readback_requires_every_other_placement_and_requirement_unchanged(self):
        before = (self.page, self.modules, self.items)
        after = copy.deepcopy(before)
        after[1][0]['items_count'] -= 1
        after[2][MODULE].pop()
        verify_after(before, after)
        after[2][MODULE][0]['completion_requirement']['type'] = 'must_view'
        with self.assertRaisesRegex(ValueError, 'Other placements'):
            verify_after(before, after)
        after = copy.deepcopy(before)
        after[1][0]['items_count'] -= 1
        after[2][MODULE].pop()
        after[0]['published'] = True
        with self.assertRaisesRegex(ValueError, 'Retained page'):
            verify_after(before, after)

    def test_transport_cannot_publish_delete_page_or_read_student_work(self):
        client = ScopedClient('https://cti-courses.instructure.com', 'not-a-token', 180)
        with patch('requests.request') as request:
            for method, route in [('PUT', f'pages/{SLUG}'), ('DELETE', f'pages/{SLUG}'),
                                  ('DELETE', f'modules/{MODULE}/items/18011'),
                                  ('GET', 'assignments/7178/submissions'), ('GET', 'users')]:
                with self.assertRaises(ValueError):
                    client._request_response(method, route)
            request.assert_not_called()


if __name__ == '__main__':
    unittest.main()

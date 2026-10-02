from copy import deepcopy
from unittest import TestCase

from canvas_sync.concept_page_conversion import convert_empty_assignment
from canvas_sync.state import canvas_fingerprint


class Client:
    def __init__(self, submitted=False, fail_publish=False, null_points=False):
        self.submitted, self.fail_publish, self.null_points = submitted, fail_publish, null_points
        self.calls = []
        self.item = {'id': 12, 'type': 'Assignment', 'content_id': 7,
                     'position': 8, 'published': True}
        self.assignment = {'id': 7, 'has_submitted_submissions': submitted,
                           'published': True, 'points_possible': 5, 'grading_type': 'points',
                           'submission_types': ['online_text_entry'], 'omit_from_final_grade': False}

    def get_assignment(self, ident):
        return deepcopy(self.assignment)

    def list_assignment_submissions(self, ident):
        return [{'workflow_state': 'submitted' if self.submitted else 'unsubmitted'}]

    def list_modules(self):
        return [{'id': 1}]

    def list_module_items(self, ident):
        return [self.item] if self.item else []

    def create_page(self, payload):
        self.calls.append(('create_page', payload))
        return {'page_id': 30, 'url': 'concept-practice'}

    def add_module_item(self, ident, **payload):
        self.calls.append(('add_module_item', payload))
        return {'id': 31}

    def update_assignment(self, ident, payload):
        self.calls.append(('update_assignment', payload))
        self.assignment.update(payload)
        if self.null_points:
            self.assignment['points_possible'] = None
        self.item['published'] = payload['published']
        return deepcopy(self.assignment)

    def delete_module_item(self, module, ident):
        self.calls.append(('delete_module_item', ident))
        self.item = None

    def update_page(self, url, payload):
        if self.fail_publish:
            raise RuntimeError('Interrupted at publication')
        self.calls.append(('update_page', payload))
        return payload


class ConceptPageConversionTests(TestCase):
    def fixture(self):
        fm = {'type': 'page', 'title': 'Sprint 1 Concept check', 'delivery_mode': 'guided_assignment',
              'submission_type': 'none', 'publish': True}
        entry = {'canvas_type': 'assignment', 'canvas_id': 7,
                 'canvas_module_id': 1, 'canvas_module_item_id': 12, 'content_hash': '1' * 64}
        return fm, entry

    def test_preserves_position_retires_gradebook_shell_and_deletes_only_placement(self):
        fm, entry = self.fixture(); client = Client(); saved = []
        result = convert_empty_assignment(client, fm, entry, '<iframe></iframe>', saved.append)
        self.assertEqual(result['canvas_type'], 'page')
        self.assertEqual(result['completion_requirement'], 'must_view')
        self.assertEqual(result['retired_assignment']['points_possible'], 5)
        placement = next(payload for call, payload in client.calls if call == 'add_module_item')
        self.assertEqual(placement['position'], 8)
        self.assertEqual(placement['completion_requirement'], {'type': 'must_view'})
        retired = next(payload for call, payload in client.calls if call == 'update_assignment')
        self.assertEqual(retired['submission_types'], ['none'])
        self.assertEqual(retired['grading_type'], 'not_graded')
        self.assertEqual(retired['points_possible'], 0)
        self.assertEqual([call for call, _ in client.calls].count('delete_module_item'), 1)
        self.assertEqual(saved[-1]['canvas_module_item_id'], 31)

    def test_submitted_work_stops_before_any_write(self):
        fm, entry = self.fixture(); client = Client(submitted=True)
        with self.assertRaisesRegex(ValueError, 'submitted work'):
            convert_empty_assignment(client, fm, entry, '', lambda entry: None)
        self.assertEqual(client.calls, [])

    def test_canvas_null_points_for_an_ungraded_shell_are_verified(self):
        fm, entry = self.fixture(); client = Client(null_points=True)
        result = convert_empty_assignment(client, fm, entry, '', lambda entry: None)
        self.assertEqual(result['canvas_type'], 'page')
        self.assertIsNone(client.assignment['points_possible'])
        self.assertEqual(client.assignment['grading_type'], 'not_graded')

    def test_known_partial_retirement_reuses_draft_page_and_item(self):
        fm, entry = self.fixture(); client = Client(null_points=True)
        entry['page_conversion'] = {'page_id': 30, 'page_url': 'concept-practice', 'item_id': 31,
                                    'position': 8, 'previous_assignment': deepcopy(client.assignment)}
        client.assignment.update(published=False, points_possible=None,
                                 submission_types=['not_graded'], omit_from_final_grade=True)
        client.item['published'] = False
        result = convert_empty_assignment(client, fm, entry, '', lambda entry: None)
        self.assertEqual(result['canvas_id'], 30)
        self.assertFalse(any(call in ('create_page', 'add_module_item') for call, _ in client.calls))
        self.assertEqual(client.assignment['submission_types'], ['none'])

    def test_unexpected_unpublication_does_not_resume_without_checkpoint(self):
        fm, entry = self.fixture(); client = Client(); client.item['published'] = False
        with self.assertRaisesRegex(ValueError, 'publication changed'):
            convert_empty_assignment(client, fm, entry, '', lambda entry: None)
        self.assertEqual(client.calls, [])

    def test_content_drift_during_partial_retirement_stops_before_any_write(self):
        fm, entry = self.fixture(); client = Client()
        client.assignment.update(name='Concept', description='Original instructions')
        entry['canvas_fingerprint'] = canvas_fingerprint(client.assignment, 'assignment')
        entry['page_conversion'] = {'page_id': 30, 'page_url': 'concept-practice', 'item_id': 31,
                                    'position': 8, 'previous_assignment': {
                                        key: client.assignment.get(key) for key in (
                                            'published', 'points_possible', 'grading_type',
                                            'submission_types', 'omit_from_final_grade')}}
        client.assignment.update(published=False, points_possible=None,
                                 submission_types=['not_graded'], omit_from_final_grade=True,
                                 description='Changed in Canvas')
        client.item['published'] = False
        with self.assertRaisesRegex(ValueError, 'content changed'):
            convert_empty_assignment(client, fm, entry, '', lambda entry: None)
        self.assertEqual(client.calls, [])

    def test_resume_adopts_checkpoint_without_duplicate_page_or_item(self):
        fm, entry = self.fixture(); client = Client(fail_publish=True); saved = []
        with self.assertRaises(RuntimeError):
            convert_empty_assignment(client, fm, entry, '', saved.append)
        checkpoint = deepcopy(saved[-1]); client.fail_publish = False
        result = convert_empty_assignment(client, fm, checkpoint, '', saved.append)
        self.assertEqual([call for call, _ in client.calls].count('create_page'), 1)
        self.assertEqual([call for call, _ in client.calls].count('add_module_item'), 1)
        self.assertNotIn('page_conversion', result)

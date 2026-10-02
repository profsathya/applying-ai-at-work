from copy import deepcopy
from unittest import TestCase

from canvas_sync.concept_page_conversion import convert_empty_assignment


class Client:
    def __init__(self, submitted=False, fail_publish=False):
        self.submitted, self.fail_publish = submitted, fail_publish
        self.calls = []
        self.item = {'id': 12, 'type': 'Assignment', 'content_id': 7,
                     'position': 8, 'published': True}

    def get_assignment(self, ident):
        return {'id': ident, 'has_submitted_submissions': self.submitted,
                'published': True, 'points_possible': 5, 'submission_types': ['online_text_entry']}

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
        return {'id': ident, **payload}

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
        self.assertEqual(retired['submission_types'], ['not_graded'])
        self.assertEqual(retired['points_possible'], 0)
        self.assertEqual([call for call, _ in client.calls].count('delete_module_item'), 1)
        self.assertEqual(saved[-1]['canvas_module_item_id'], 31)

    def test_submitted_work_stops_before_any_write(self):
        fm, entry = self.fixture(); client = Client(submitted=True)
        with self.assertRaisesRegex(ValueError, 'submitted work'):
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

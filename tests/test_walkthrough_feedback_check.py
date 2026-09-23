import json
from pathlib import Path
import tempfile
import unittest

from canvas_sync.walkthrough_feedback_check import check_registration, enabled_checkpoints


class FeedbackRegistryTests(unittest.TestCase):
    def test_every_enabled_checkpoint_requires_reviewed_criteria(self):
        fm = {'artifact_id': 'example', 'guided_assignment': {
            'presentation': 'walkthrough', 'feedback_endpoint': 'https://service.example/feedback',
            'tasks': [{'id': 'draft'}, {'id': 'reference', 'read_only': True},
                      {'id': 'identity', 'feedback_enabled': False}, {'id': 'revise'}]}}
        self.assertEqual(enabled_checkpoints(fm), ['draft', 'revise'])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'guidance.json'
            registry = {'example': {'title': 'Example', 'rule': 'Review, never write.',
                                    'checkpoints': {'draft': 'Use evidence.'}}}
            path.write_text(json.dumps(registry))
            self.assertEqual(len(check_registration(fm, path)), 1)
            self.assertIn('revise', check_registration(fm, path)[0])
            registry['example']['checkpoints']['revise'] = 'Explain what changed.'
            path.write_text(json.dumps(registry))
            self.assertEqual(check_registration(fm, path), [])

    def test_no_endpoint_requires_no_service_registration(self):
        self.assertEqual(check_registration({'guided_assignment': {'presentation': 'walkthrough',
                          'tasks': [{'id': 'independent'}]}}), [])

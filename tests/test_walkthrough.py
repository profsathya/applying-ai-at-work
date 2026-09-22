"""Local walk-through rendering and release guard checks; no Canvas writes."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from canvas_sync.hosted_html import artifact_hosted_info, render_artifact_document
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import load_json
from canvas_sync.walkthrough_release import preflight_pair, release_pairs, rollback_pair

ROOT = Path(__file__).resolve().parents[1]


class CanvasStub:
    def __init__(self):
        self.assignments = {
            1: {'id': 1, 'name': 'Source', 'published': True, 'points_possible': 35,
                'submission_types': ['online_upload'], 'grading_type': 'points'},
            2: {'id': 2, 'name': 'Replacement', 'published': False, 'points_possible': 35,
                'submission_types': ['online_upload'], 'grading_type': 'points'},
        }
        self.submissions = []
        self.module_items = [{'id': 10, 'position': 1, 'published': True},
                             {'id': 11, 'position': 2, 'published': False}]

    def get_assignment(self, assignment_id, *, include=None):
        return dict(self.assignments[assignment_id])

    def list_assignment_submissions(self, assignment_id):
        return list(self.submissions) if assignment_id == 1 else []

    def list_assignment_overrides(self, assignment_id):
        return []

    def list_module_items(self, module_id):
        return [dict(item) for item in self.module_items]

    def update_module_item(self, module_id, module_item_id, payload):
        item = next(item for item in self.module_items if item['id'] == module_item_id)
        item.update(payload)
        return dict(item)

    def update_assignment(self, assignment_id, payload):
        self.assignments[assignment_id].update(payload)
        return dict(self.assignments[assignment_id])


class WalkthroughChecks(unittest.TestCase):
    def test_stakeholder_example_renders_without_forbidden_chrome_or_ai(self):
        artifact = ROOT / 'examples/walkthroughs/stakeholder-map-local-dry-run.md'
        self.assertEqual(validate_artifact(artifact), [])
        fm, body = parse_frontmatter(artifact)
        manifest_path = ROOT / 'course1/manifests/production.json'
        manifest = load_json(manifest_path)
        html = render_artifact_document(fm, body, manifest,
                                        artifact_hosted_info(artifact, manifest_path, manifest, fm))
        self.assertEqual(html.count('data-walk-answer='), 101)
        self.assertEqual(html.count('data-walk-feedback='), 0)
        self.assertNotIn('<h2>Learning goal</h2>', html)
        self.assertNotIn('<h2>Submit to Canvas</h2>', html)
        self.assertIn('Download Word document', html)
        self.assertIn('Download text copy', html)
        self.assertEqual(html.count('>Profile four stakeholders</h2>'), 1)
        self.assertEqual(html.count('<table class="walk-response-table">'), 9)
        self.assertEqual(html.count('<th scope="col">Confirmed or Inferred, and why</th>'), 4)
        self.assertIn('<th scope="row">Role in relation to the problem', html)
        self.assertIn('Example and guidance</summary>', html)

    def test_release_requires_pair_and_assessment_parity(self):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / 'source.md'
            new_path = Path(directory) / 'new.md'
            source_path.write_text('---\nartifact_id: source\ntype: assignment\nmodule: M\npoints: 35\nsubmission_type: file_upload\npublish: false\n---\n')
            new_path.write_text('---\nartifact_id: new\ntype: assignment\nmodule: M\npoints: 35\nsubmission_type: file_upload\nwalkthrough_after: source\npublish: true\n---\n')
            source = {'artifact_id': 'source', 'path': source_path, 'file': 'source.md'}
            new = {'artifact_id': 'new', 'path': new_path, 'file': 'new.md'}
            self.assertEqual(release_pairs([new, source], [source_path, new_path]), [(source, new)])
            state = {'artifacts': {
                'source': {'artifact_id': 'source', 'canvas_id': 1, 'canvas_type': 'assignment',
                           'canvas_module_id': 5, 'canvas_module_item_id': 10},
                'new': {'artifact_id': 'new', 'canvas_id': 2, 'canvas_type': 'assignment',
                        'canvas_module_id': 5, 'canvas_module_item_id': 11},
            }}
            client = CanvasStub()
            self.assertEqual(preflight_pair(client, source, new, state)['module_order'], [10, 11])
            client.assignments[2]['points_possible'] = 20
            with self.assertRaisesRegex(ValueError, 'points_possible'):
                preflight_pair(client, source, new, state)
            client.assignments[2]['points_possible'] = 35
            client.module_items[1]['published'] = True
            with self.assertRaisesRegex(ValueError, 'module items'):
                preflight_pair(client, source, new, state)
            client.module_items[1]['published'] = False
            client.submissions = [{'submitted_at': '2026-09-22T12:00:00Z'}]
            with self.assertRaisesRegex(ValueError, 'submission'):
                preflight_pair(client, source, new, state)

    def test_rollback_restores_visibility_and_invalidates_hashes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'state.json'
            state = {'artifacts': {
                'source': {'artifact_id': 'source', 'canvas_id': 1, 'canvas_type': 'assignment',
                           'canvas_module_id': 5, 'canvas_module_item_id': 10, 'content_hash': 'old'},
                'new': {'artifact_id': 'new', 'canvas_id': 2, 'canvas_type': 'assignment',
                        'canvas_module_id': 5, 'canvas_module_item_id': 11, 'content_hash': 'new'},
            }}
            path.write_text(json.dumps(state))
            client = CanvasStub()
            client.assignments[1]['published'] = False
            client.assignments[2]['published'] = True
            client.module_items[0]['published'] = False
            client.module_items[1]['published'] = True
            pair = {'source': state['artifacts']['source'], 'replacement': state['artifacts']['new']}
            self.assertEqual(rollback_pair(client, pair, path), [])
            self.assertTrue(client.assignments[1]['published'])
            self.assertFalse(client.assignments[2]['published'])
            self.assertTrue(client.module_items[0]['published'])
            self.assertFalse(client.module_items[1]['published'])
            saved = load_json(path)
            self.assertEqual(saved['artifacts']['source']['content_hash'], '')
            self.assertEqual(saved['artifacts']['new']['content_hash'], '')


if __name__ == '__main__':
    unittest.main()

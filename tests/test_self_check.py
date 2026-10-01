"""Synthetic contract checks; no submissions, network or Canvas writes."""
import copy
import json
import unittest
from pathlib import Path
from canvas_sync.self_check import load_record, validate_record, render_full_credit, score_rungs
from canvas_sync.walkthrough import render_walkthrough_body

REFERENCE = 'course1/design/self-check-records/first-frames.json'


class SelfCheckTests(unittest.TestCase):
    def setUp(self):
        self.record = load_record(REFERENCE)

    def test_exact_guide_example(self):
        r = self.record
        self.assertEqual(validate_record(r, grading=True), [])
        self.assertEqual([c['full']['points'] for c in r['criteria']], [10,8,8,8,6,10])
        self.assertEqual([c['rank'] for c in r['criteria']], [6,1,3,4,5,2])
        for rung, total in [('full',50),('3',36),('1',11)]:
            result = score_rungs(r, {c['id']:rung for c in r['criteria']}, gate_passed=True)
            self.assertEqual(result['raw_sum'], total)
        # Exact source wording/rung values remain traceable to the approved guide.
        guide = (Path(__file__).resolve().parents[1] / 'course1/design/self-check-guide.md').read_text()
        for c in r['criteria']:
            self.assertIn(c['full']['text'], guide)
            for rung in ('3','1'):
                self.assertIn(f"{c[rung]['text']} ({c[rung]['points']})", guide)

    def test_gate_never_invents_grade(self):
        choices = {c['id']:'full' for c in self.record['criteria']}
        for gate in (False, None):
            result = score_rungs(self.record, choices, gate_passed=gate)
            self.assertEqual(result['raw_sum'], 50)
            self.assertIsNone(result['numeric_grade'])
            self.assertTrue(result['requires_human_review'])
        self.assertFalse(score_rungs(self.record, choices, gate_passed=False)['passes'])

    def test_drafts_fail_closed_for_scoring(self):
        directory = Path(__file__).resolve().parents[1] / 'course1/design/self-check-records'
        for path in directory.glob('*.json'):
            record = json.loads(path.read_text())
            self.assertEqual(validate_record(record), [], path.name)
            if record['id'] != 'first-frames':
                self.assertTrue(validate_record(record, grading=True), path.name)
        for slug, totals in [('stakeholder-map', [50,35,9]), ('stakeholder-conversation',[50,35,11])]:
            record = json.loads((directory / f'{slug}.json').read_text())
            self.assertEqual([sum(c[r]['points'] for c in record['criteria']) for r in ('full','3','1')], totals)

    def test_invalid_contracts(self):
        for mutate in (lambda r: r['criteria'][0].update(rank=1),
                       lambda r: r['criteria'][0]['full'].update(points=11),
                       lambda r: r['criteria'][0].update(tag='effort'),
                       lambda r: r['criteria'][0]['1'].update(points=0)):
            record = copy.deepcopy(self.record); mutate(record)
            self.assertTrue(validate_record(record, grading=True))
        with self.assertRaises(ValueError):
            score_rungs(self.record, {'1':'2'}, gate_passed=True)
        with self.assertRaises(ValueError):
            load_record('../../secret.json')

    def test_walkthrough_uses_only_full_credit_projection(self):
        fm = {'artifact_id':'synthetic', 'title':'Synthetic', 'submission_type':'text_entry',
              'guided_assignment':{'version':'v1','tasks':[], 'self_check_record':REFERENCE,
                                   'final_check':['OLD LIST']}}
        output = render_walkthrough_body(fm, '', {})
        self.assertIn(render_full_credit(self.record), output)
        self.assertNotIn('OLD LIST', output)
        self.assertNotIn('<details class="walk-check self-check"', output)
        for c in self.record['criteria']:
            self.assertNotIn(c['3']['text'], output)
        self.assertNotIn('failure_grade', output)
        self.assertNotIn('open_questions', output)
        fm['guided_assignment'].pop('self_check_record')
        self.assertIn('OLD LIST', render_walkthrough_body(fm, '', {}))

    def test_reference_accepted_by_frontmatter_schema(self):
        import jsonschema
        from canvas_sync.schema import load_schema
        field = load_schema('frontmatter')['properties']['guided_assignment']['properties']['self_check_record']
        jsonschema.validate(REFERENCE, field)
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate('../../secret.json', field)

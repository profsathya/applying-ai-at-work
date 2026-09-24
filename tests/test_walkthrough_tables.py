"""Rectangular source table mapping and walkthrough rendering checks."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml
from canvas_sync.schema import load_schema, validate_guided_assignment
from canvas_sync.walkthrough import render_walkthrough_body
from canvas_sync.walkthrough_tables import TableMappingError, compare_task, create_task, table_matrix
import jsonschema

ROOT = Path(__file__).resolve().parents[1]


def candidate_log_block():
    headings = ['The situation', 'How it works now', 'What it costs, and whom', 'The gap']
    guidance = [
        'Restate the item from Part A, a phrase.',
        'Two or three sentences. Who does what, in what order. The actions that happen now, not how they should be and not possible solutions.',
        'Who is impacted, and for each of them, what the cost is in time, money, errors, or strain.',
        'One sentence. What could be different, and who feels the cost. Name who does not know, cannot do, or has to redo what.',
    ]
    def cell(text):
        return {'blocks': [{'kind': 'paragraph', 'text': {'base': text, 'proposed': text}, 'flags': []}]}
    return {'id': 'd-example:tab/one/body/3', 'kind': 'table', 'flags': [],
            'rows': [[cell(text) for text in row] for row in [headings, guidance, *([[''] * 4] * 5)]]}


def candidate_task():
    return create_task(candidate_log_block(), 'candidate-log', 'Get underneath three to five',
                       ['Complete three to five candidate rows.'], response_rows=set(range(3, 8)))


def rectangular_block(width):
    def cell(text):
        return {'blocks': [{'kind': 'paragraph', 'text': {'base': text, 'proposed': text}, 'flags': []}]}
    return {'id': f'table-{width}', 'kind': 'table', 'flags': [],
            'rows': [[cell(f'Column {index}') for index in range(1, width + 1)],
                     [cell(f'Guidance {index}\nSecond line') for index in range(1, width + 1)],
                     [cell('') for _ in range(width)]]}


class WalkthroughTableTests(unittest.TestCase):
    def test_headerless_form_preserves_first_row_and_single_row_tables(self):
        block = rectangular_block(2)
        block['rows'] = [block['rows'][1]]
        task = create_task(block, 'form', 'Your form', ['Use your own evidence.'],
                           header_rows=0, column_labels=['Field', 'Your answer'], response_cells={(1, 2)})
        self.assertEqual(len(task['rows']), 1)
        self.assertEqual(compare_task(block, task, header_rows=0, response_cells={(1, 2)}), [])
        rendered = render_walkthrough_body({'title': 'Form', 'artifact_id': 'form',
            'submission_type': 'file_upload', 'guided_assignment': {'version': '1', 'tasks': [task],
            'records_destination': {'label': 'your map', 'url': 'https://docs.google.com/document/d/test/copy'}}}, '', {})
        self.assertNotIn('<thead>', rendered.split('<script')[0])
        self.assertIn('data-walk-answer="form.row-1.column-2"', rendered)
        self.assertIn('Keep your own copy in <a', rendered)
        self.assertIn('Guidance 1<br>Second line', rendered)
        with self.assertRaisesRegex(TableMappingError, 'accessible label'):
            create_task(block, 'form', 'Your form', ['Check it.'], header_rows=0, response_cells={(1, 2)})

    def test_candidate_log_maps_four_columns_and_five_response_rows(self):
        block = candidate_log_block(); task = candidate_task()
        self.assertEqual(len(task['columns']), 4)
        self.assertEqual(len(task['rows']), 6)
        self.assertEqual(sum(bool(cell.get('response')) for row in task['rows'] for cell in row['cells']), 20)
        self.assertEqual(compare_task(block, task), [])
        task['rows'][0]['cells'][0]['text'] = 'Changed'
        self.assertIn('body row 1', compare_task(block, task)[0])

    def test_ragged_and_merged_tables_are_rejected(self):
        block = candidate_log_block(); block['rows'][-1].pop()
        with self.assertRaisesRegex(TableMappingError, 'equally wide'):
            table_matrix(block)
        block = candidate_log_block(); block['flags'] = ['render_unsupported']
        with self.assertRaisesRegex(TableMappingError, 'Merged'):
            table_matrix(block)

    def test_structural_revision_requires_reviewed_decision(self):
        block = candidate_log_block()
        block['flags'] = ['structural_revision']
        with self.assertRaisesRegex(TableMappingError, 'reviewed-structure'):
            table_matrix(block)
        self.assertEqual(len(table_matrix(block, reviewed_structure=True)), 7)
        task = create_task(block, 'candidate-log', 'Fill the log', ['Use source guidance.'],
                           response_rows=set(range(3, 8)), reviewed_structure=True)
        self.assertEqual(compare_task(block, task, reviewed_structure=True), [])

    def test_source_text_can_share_a_cell_with_a_response(self):
        task = create_task(candidate_log_block(), 'candidate-log', 'Fill the log', ['Use source guidance.'],
                           response_cells={(2, 1)})
        self.assertEqual(task['rows'][0]['cells'][0]['text'], 'Restate the item from Part A, a phrase.')
        self.assertTrue(task['rows'][0]['cells'][0]['response'])
        self.assertFalse(task['rows'][0]['cells'][1].get('response', False))

    def test_two_and_five_column_tables_preserve_mixed_cells_and_line_breaks(self):
        for width in (2, 5):
            block = rectangular_block(width)
            task = create_task(block, f'grid-{width}', 'Complete the grid', ['Check your entry.'],
                               response_cells={(2, 1), (3, width)})
            self.assertEqual(len(task['columns']), width)
            self.assertEqual(task['rows'][0]['cells'][0]['text'], 'Guidance 1\nSecond line')
            self.assertTrue(task['rows'][0]['cells'][0]['response'])
            self.assertEqual(compare_task(block, task, response_cells={(2, 1), (3, width)}, read_only=False), [])
            rendered = render_walkthrough_body({'type': 'assignment', 'title': 'Grid', 'artifact_id': f'grid-{width}',
                                                'submission_type': 'text_entry',
                                                'guided_assignment': {'version': '1', 'tasks': [task],
                                                                      'export_filename': 'grid.docx'}}, '', {})
            self.assertIn(f'--walk-table-min-width:{width * 180}px', rendered)
            self.assertIn('Guidance 1<br>Second line', rendered)

    def test_read_only_table_needs_no_response_criteria_or_feedback(self):
        task = create_task(candidate_log_block(), 'reference-log', 'Read the Candidate Log', read_only=True)
        self.assertTrue(task['read_only'])
        self.assertNotIn('criteria', task)
        self.assertFalse(any(cell.get('response') for row in task['rows'] for cell in row['cells']))
        self.assertEqual(compare_task(candidate_log_block(), task, response_cells=set(), read_only=True), [])
        config = {'version': '1', 'presentation': 'walkthrough', 'export_filename': 'reference-log.docx',
                  'feedback_endpoint': 'https://example.invalid/.netlify/functions/walkthrough-feedback',
                  'feedback_protocol': 'walkthrough-v1',
                  'tasks': [task]}
        fm = {'type': 'assignment', 'title': 'Reference Log', 'artifact_id': 'reference-log-example',
              'submission_type': 'text_entry', 'delivery_mode': 'guided_assignment',
              'walkthrough_after': 'source-example', 'guided_assignment': config}
        jsonschema.validate(config, load_schema('frontmatter')['properties']['guided_assignment'])
        self.assertEqual(validate_guided_assignment('fixture', fm), [])
        rendered = render_walkthrough_body(fm, '', {})
        self.assertIn('Use this table as a reference.', rendered)
        self.assertNotIn('<details class="walk-check">', rendered)
        self.assertNotIn('data-walk-answer="', rendered)
        self.assertNotIn('data-walk-feedback="', rendered)
        self.assertIn('How this walk-through works', rendered)
        self.assertIn('This Canvas walk-through assignment includes a reference table.', rendered)
        self.assertIn('Copy reference table', rendered)
        self.assertIn('Download Word copy of table', rendered)
        self.assertIn('This page has no response to submit.', rendered)
        self.assertNotIn('Submit this walk-through in Canvas', rendered)
        with self.assertRaisesRegex(TableMappingError, 'cannot mark response'):
            create_task(candidate_log_block(), 'invalid', 'Read', read_only=True, response_rows={3})
        with self.assertRaisesRegex(TableMappingError, 'do not have self-check'):
            create_task(candidate_log_block(), 'invalid', 'Read', ['Invented check'], read_only=True)
        with self.assertRaisesRegex(TableMappingError, 'Mark at least one'):
            create_task(candidate_log_block(), 'invalid', 'Write', ['Check it'])
        task['criteria'] = ['Unexpected check']
        self.assertTrue(any('read-only table cannot contain self-check' in error
                            for error in validate_guided_assignment('fixture', fm)))
        del task['criteria']
        task['rows'][0]['cells'][0]['response'] = True
        self.assertTrue(any('read-only table cannot contain response' in error
                            for error in validate_guided_assignment('fixture', fm)))

    def test_read_only_mapper_cli_round_trip_and_mode_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            block = rectangular_block(2)
            packet = root / 'source-packet.json'
            packet.write_text(json.dumps({'documents': [{'sections': [{'blocks': [block]}]}]}))
            common = [sys.executable, str(ROOT / 'canvas_sync/walkthrough_tables.py'),
                      '--packet', str(packet), '--block', block['id'], '--view', 'base', '--task-id', 'reference']
            drafted = subprocess.run([*common, '--prompt', 'Use this grid', '--read-only'], cwd=ROOT,
                                     capture_output=True, text=True)
            self.assertEqual(drafted.returncode, 0, drafted.stderr)
            task = yaml.safe_load(drafted.stdout)
            artifact = root / 'reference.md'
            artifact.write_text('---\n' + yaml.safe_dump({'guided_assignment': {'tasks': [task]}}) + '---\n')
            verified = subprocess.run([*common, '--artifact', str(artifact), '--read-only'], cwd=ROOT,
                                      capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            mismatch = subprocess.run([*common, '--artifact', str(artifact), '--response-row', '3'], cwd=ROOT,
                                      capture_output=True, text=True)
            self.assertNotEqual(mismatch.returncode, 0)
            self.assertIn('read-only selection', mismatch.stderr)

    def test_schema_and_render_keep_single_source_grid(self):
        task = candidate_task()
        config = {'version': '1', 'presentation': 'walkthrough', 'export_filename': 'candidate-log.docx',
                  'feedback_endpoint': 'https://example.invalid/.netlify/functions/walkthrough-feedback',
                  'feedback_protocol': 'walkthrough-v1',
                  'tasks': [task]}
        fm = {'type': 'assignment', 'title': 'Candidate Log', 'artifact_id': 'candidate-log-example',
              'submission_type': 'text_entry', 'delivery_mode': 'guided_assignment',
              'walkthrough_after': 'source-example', 'guided_assignment': config}
        jsonschema.validate(config, load_schema('frontmatter')['properties']['guided_assignment'])
        self.assertEqual(validate_guided_assignment('fixture', fm), [])
        rendered = render_walkthrough_body(fm, '', {})
        self.assertEqual(rendered.count('<table class="walk-source-table">'), 1)
        self.assertEqual(rendered.count('<th scope="col">'), 4)
        self.assertEqual(rendered.count('data-walk-answer='), 20)
        self.assertEqual(rendered.count('data-walk-feedback='), 5)
        self.assertLess(rendered.index('data-walk-feedback='), rendered.index('</table>'))
        self.assertIn('walk-table-with-feedback', rendered)
        self.assertIn('The situation</th>', rendered)
        self.assertIn('This is a Canvas walk-through assignment.', rendered)
        self.assertIn('Submit this walk-through in Canvas', rendered)
        self.assertIn('Copy text for Canvas submission', rendered)
        self.assertIn('paste it into the text-entry box, and submit it', rendered)
        self.assertLess(rendered.index('id="walk-copy"'), rendered.index('id="walk-download"'))
        self.assertIn('walk-rich-output', rendered)
        task['rows'][1]['cells'].pop()
        self.assertTrue(any('column count' in error for error in validate_guided_assignment('fixture', fm)))

    def test_non_table_walkthrough_submission_routes(self):
        task = {'id': 'reflection', 'kind': 'response', 'prompt': 'Reflect',
                'criteria': ['Be specific.']}
        config = {'version': '1', 'presentation': 'walkthrough', 'tasks': [task],
                  'export_filename': 'reflection.docx'}
        fm = {'type': 'assignment', 'title': 'Reflection', 'artifact_id': 'reflection-example',
              'delivery_mode': 'guided_assignment', 'walkthrough_after': 'source-example',
              'submission_type': 'text_entry', 'guided_assignment': config}
        text_entry = render_walkthrough_body(fm, '', {})
        self.assertIn('How this walk-through works', text_entry)
        self.assertIn('Copy text for Canvas submission', text_entry)
        self.assertIn('paste it into the text-entry box', text_entry)
        fm['submission_type'] = 'file_upload'
        file_upload = render_walkthrough_body(fm, '', {})
        self.assertIn('Download Word document for Canvas submission', file_upload)
        self.assertIn('Copy work for your records', file_upload)
        self.assertIn('select Submit Assignment, upload the file', file_upload)
        self.assertNotIn('paste it into the text-entry box', file_upload)
        self.assertLess(file_upload.index('id="walk-download"'), file_upload.index('id="walk-copy"'))

    def test_writable_feedback_requires_endpoint_or_recorded_exception(self):
        task = {'id': 'reflection', 'kind': 'response', 'prompt': 'Reflect',
                'criteria': ['Be specific.']}
        config = {'version': '1', 'presentation': 'walkthrough', 'tasks': [task]}
        fm = {'type': 'assignment', 'title': 'Reflection', 'artifact_id': 'reflection-example',
              'delivery_mode': 'guided_assignment', 'walkthrough_after': 'source-example',
              'submission_type': 'text_entry', 'guided_assignment': config}
        self.assertTrue(any('require feedback_endpoint or feedback_omission_reason' in error
                            for error in validate_guided_assignment('fixture', fm)))
        config['feedback_omission_reason'] = 'The source prohibits AI feedback.'
        self.assertEqual(validate_guided_assignment('fixture', fm), [])
        del config['feedback_omission_reason']
        config['feedback_endpoint'] = 'https://example.invalid/.netlify/functions/walkthrough-feedback'
        config['feedback_protocol'] = 'walkthrough-v1'
        self.assertEqual(validate_guided_assignment('fixture', fm), [])
        task['feedback_enabled'] = False
        self.assertTrue(any('disabled AI feedback requires feedback_omission_reason' in error
                            for error in validate_guided_assignment('fixture', fm)))
        task['feedback_omission_reason'] = 'This response contains restricted source material.'
        self.assertEqual(validate_guided_assignment('fixture', fm), [])

    def test_javascript_table_output_and_word_export(self):
        result = subprocess.run(['node', str(ROOT / 'tests/walkthrough_tables_runtime.cjs')],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_authoring_helper_drafts_and_compares_source_grid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            block = candidate_log_block()
            packet = root / 'source-packet.json'
            packet.write_text(json.dumps({'documents': [{'sections': [{'blocks': [block]}]}]}))
            common = ['--packet', str(packet), '--block', block['id'], '--view', 'base',
                      '--task-id', 'candidate-log']
            responses = [part for source_row in range(3, 8) for part in ('--response-row', str(source_row))]
            command = [sys.executable, str(ROOT / 'canvas_sync/walkthrough_tables.py'),
                       *common, '--prompt', 'Get underneath three to five',
                       '--criterion', 'Complete three to five candidate rows.', *responses]
            drafted = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(drafted.returncode, 0, drafted.stderr)
            task = yaml.safe_load(drafted.stdout)
            self.assertEqual(compare_task(block, task), [])
            artifact = root / 'candidate-log.md'
            artifact.write_text('---\n' + yaml.safe_dump({'guided_assignment': {'tasks': [task]}}) + '---\n')
            verified = subprocess.run([sys.executable,
                                       str(ROOT / 'canvas_sync/walkthrough_tables.py'), *common,
                                       '--artifact', str(artifact), *responses], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            task['rows'][1]['cells'][0].pop('response')
            artifact.write_text('---\n' + yaml.safe_dump({'guided_assignment': {'tasks': [task]}}) + '---\n')
            mismatch = subprocess.run([sys.executable,
                                       str(ROOT / 'canvas_sync/walkthrough_tables.py'), *common,
                                       '--artifact', str(artifact), *responses], cwd=ROOT, capture_output=True, text=True)
            self.assertNotEqual(mismatch.returncode, 0)
            self.assertIn('response-cell selections', mismatch.stderr)


if __name__ == '__main__':
    unittest.main()

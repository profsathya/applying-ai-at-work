"""Draft and compare rectangular walkthrough tasks against an intake table.

This reads a private source packet and writes only to stdout. Response-cell roles
are explicit authoring decisions; blank source cells are never inferred as inputs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from canvas_sync.schema import parse_frontmatter
from canvas_sync.source_intake import walk_blocks


class TableMappingError(ValueError):
    pass


def find_table(packet: dict, block_id: str) -> dict:
    matches = [block for document in packet.get('documents', []) for section in document.get('sections', [])
               for block in walk_blocks(section.get('blocks', [])) if block.get('id') == block_id]
    if len(matches) != 1 or matches[0].get('kind') != 'table':
        raise TableMappingError('Source table reference must resolve to exactly one table block')
    return matches[0]


def table_matrix(block: dict, view: str = 'base', *, reviewed_structure: bool = False,
                 header_rows: int = 1) -> list[list[str]]:
    if header_rows not in (0, 1):
        raise TableMappingError('Choose zero or one header row')
    if view not in ('base', 'proposed'):
        raise TableMappingError('Choose a base or proposed source view')
    review_flags = {'render_unsupported', 'answer_key', 'raw_configuration', 'editorial_marker', 'diagram_source'}
    if block.get('kind') != 'table' or review_flags.intersection(block.get('flags', [])):
        raise TableMappingError('Merged, review-only, or unsupported tables need a reviewed adaptation')
    if 'structural_revision' in block.get('flags', []) and not reviewed_structure:
        raise TableMappingError('Structural revision needs an explicit --reviewed-structure decision')
    matrix = []
    for row in block.get('rows', []):
        values = []
        for cell in row:
            parts = cell.get('blocks', [])
            if any(part.get('kind') != 'paragraph' or review_flags.intersection(part.get('flags', [])) for part in parts):
                raise TableMappingError('Nested, review-only, or unsupported table cells need a reviewed adaptation')
            values.append('\n'.join(part.get('text', {}).get(view, '') for part in parts))
        matrix.append(values)
    if len(matrix) <= header_rows or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise TableMappingError('Table needs equally wide body rows')
    if header_rows and any(not heading.strip() for heading in matrix[0]):
        raise TableMappingError('Each column needs a single visible header')
    return matrix


def create_task(block: dict, task_id: str, prompt: str, criteria: list[str] | None = None, *, view: str = 'base',
                response_rows: set[int] | None = None, response_cells: set[tuple[int, int]] | None = None,
                reviewed_structure: bool = False, read_only: bool = False,
                header_rows: int = 1, column_labels: list[str] | None = None) -> dict:
    matrix = table_matrix(block, view, reviewed_structure=reviewed_structure, header_rows=header_rows)
    if header_rows == 0 and (not column_labels or len(column_labels) != len(matrix[0])
                             or any(not label.strip() for label in column_labels)):
        raise TableMappingError('Headerless tables need an accessible label for each column')
    if not re.fullmatch(r'[a-z][a-z0-9-]*', task_id):
        raise TableMappingError('Task ID must be lowercase kebab-case')
    chosen = response_coordinates(matrix, response_rows or set(), response_cells or set(),
                                  read_only=read_only, header_rows=header_rows)
    if read_only and criteria:
        raise TableMappingError('Read-only tables do not have self-check criteria')
    if not read_only and not criteria:
        raise TableMappingError('Editable tables need at least one self-check criterion')
    rows = []
    response_number = 0
    for source_row, values in enumerate(matrix[header_rows:], header_rows + 1):
        cells = [{'text': text, **({'response': True} if (source_row, column) in chosen else {})}
                 for column, text in enumerate(values, 1)]
        row = {'id': f'row-{source_row - header_rows}', 'cells': cells}
        if any(cell.get('response') for cell in cells):
            response_number += 1
            row['label'] = f'Entry {response_number}'
        rows.append(row)
    task = {'id': task_id, 'kind': 'table', 'prompt': prompt,
            'columns': [{'id': f'column-{i}', 'label': heading}
                        for i, heading in enumerate(matrix[0] if header_rows else column_labels, 1)], 'rows': rows}
    if not header_rows:
        task['header_rows'] = 0
    if read_only:
        task['read_only'] = True
    else:
        task['criteria'] = criteria
    return task


def response_coordinates(matrix: list[list[str]], response_rows: set[int],
                         response_cells: set[tuple[int, int]], *, read_only: bool = False,
                         header_rows: int = 1) -> set[tuple[int, int]]:
    chosen = {(row, column) for row in response_rows for column in range(1, len(matrix[0]) + 1)} | response_cells
    if read_only:
        if chosen:
            raise TableMappingError('Read-only tables cannot mark response rows or cells')
        return set()
    if not chosen or any(row <= header_rows or row > len(matrix) or column < 1 or column > len(matrix[0])
                         for row, column in chosen):
        raise TableMappingError('Mark at least one valid body cell as a response')
    return chosen


def compare_task(block: dict, task: dict, *, view: str = 'base',
                 response_cells: set[tuple[int, int]] | None = None,
                 reviewed_structure: bool = False, read_only: bool | None = None,
                 header_rows: int = 1) -> list[str]:
    matrix = table_matrix(block, view, reviewed_structure=reviewed_structure, header_rows=header_rows)
    errors = []
    if task.get('header_rows', 1) != header_rows:
        errors.append('header-row selection differs from the recorded authoring map')
    if read_only is not None and (task.get('read_only') is True) != read_only:
        errors.append('read-only selection differs from the recorded authoring map')
    if header_rows and [column.get('label') for column in task.get('columns', [])] != matrix[0]:
        errors.append('column headings differ from the source table')
    rows = task.get('rows', [])
    if len(task.get('columns', [])) != len(matrix[0]):
        errors.append('column count differs from the source table')
    if len(rows) != len(matrix) - header_rows:
        errors.append('body row count differs from the source table')
    for index, (row, source_row) in enumerate(zip(rows, matrix[header_rows:]), 1):
        if [cell.get('text') for cell in row.get('cells', [])] != source_row:
            errors.append(f'body row {index} text or width differs from the source table')
    if response_cells is not None:
        actual = {(row_index, column_index) for row_index, row in enumerate(rows, header_rows + 1)
                  for column_index, cell in enumerate(row.get('cells', []), 1) if cell.get('response')}
        if actual != response_cells:
            errors.append('response-cell selections differ from the recorded authoring map')
    if task.get('read_only') is True and any(cell.get('response') for row in rows for cell in row.get('cells', [])):
        errors.append('read-only table has response cells')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--block', required=True, help='Source packet table block ID')
    parser.add_argument('--view', choices=['base', 'proposed'], required=True)
    parser.add_argument('--header-rows', type=int, choices=[0, 1], default=1)
    parser.add_argument('--column-label', action='append', help='Accessible column label for a headerless grid; not added as a source row')
    parser.add_argument('--reviewed-structure', action='store_true',
                        help='Acknowledge a reviewed structural revision after checking the visible grid')
    parser.add_argument('--task-id', required=True)
    parser.add_argument('--artifact', type=Path, help='Verify an existing walkthrough task against the source')
    parser.add_argument('--prompt', help='New task prompt when drafting')
    parser.add_argument('--criterion', action='append', default=[], help='Self-check criterion when drafting')
    parser.add_argument('--read-only', action='store_true', help='Preserve the table as a reference with no response fields')
    parser.add_argument('--response-row', action='append', type=int, default=[],
                        help='One-based source table row, including the header row')
    parser.add_argument('--response-cell', action='append', default=[], metavar='ROW:COL',
                        help='One-based source table cell, including the header row')
    args = parser.parse_args()
    try:
        packet = json.loads(args.packet.read_text())
        block = find_table(packet, args.block)
        cells = set()
        for item in args.response_cell:
            if not re.fullmatch(r'[1-9][0-9]*:[1-9][0-9]*', item):
                raise TableMappingError('Response cells must use one-based ROW:COL coordinates')
            cells.add(tuple(map(int, item.split(':'))))
        if args.read_only and args.criterion:
            raise TableMappingError('Read-only tables do not have self-check criteria')
        chosen = response_coordinates(table_matrix(block, args.view, reviewed_structure=args.reviewed_structure,
                                                    header_rows=args.header_rows),
                                      set(args.response_row), cells, read_only=args.read_only, header_rows=args.header_rows)
        if args.artifact:
            frontmatter, _ = parse_frontmatter(args.artifact)
            tasks = frontmatter.get('guided_assignment', {}).get('tasks', [])
            matches = [task for task in tasks if task.get('id') == args.task_id and task.get('kind') == 'table']
            if len(matches) != 1:
                raise TableMappingError('Artifact must contain exactly one matching table task')
            errors = compare_task(block, matches[0], view=args.view, response_cells=chosen,
                                  reviewed_structure=args.reviewed_structure, read_only=args.read_only,
                                  header_rows=args.header_rows)
            if errors:
                raise TableMappingError('; '.join(errors))
            print('Table headings, source cell text, and grid dimensions match the selected source block.')
            return 0
        if not args.prompt:
            raise TableMappingError('Drafting needs a prompt')
        task = create_task(block, args.task_id, args.prompt, args.criterion, view=args.view,
                           response_rows=set(args.response_row), response_cells=cells,
                           reviewed_structure=args.reviewed_structure, read_only=args.read_only,
                           header_rows=args.header_rows, column_labels=args.column_label)
        print(yaml.safe_dump(task, sort_keys=False, allow_unicode=True).rstrip())
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Table mapping: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

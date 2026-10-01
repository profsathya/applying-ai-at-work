"""Versioned self-check contract. No Canvas access or model scoring."""
from __future__ import annotations
import hashlib
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAGS = {'completeness', 'specificity', 'honesty', 'judgment'}


def validate_record(record: dict, *, grading: bool = False) -> list[str]:
    errors = []
    if not isinstance(record, dict):
        return ['record must be an object']
    if type(record.get('version')) is not int or record['version'] != 1 or not isinstance(record.get('id'), str) or not record['id'].strip():
        errors.append('version 1 and a record id are required')
    lines = record.get('criteria', [])
    if not isinstance(lines, list) or any(not isinstance(line, dict) for line in lines):
        return ['criteria must be an array of objects']
    if not 1 <= len(lines) <= 10:
        errors.append('one to ten criteria required')
    if record.get('total') != 50 or record.get('passing') != 35 or record.get('blank_rung') != '1':
        errors.append('total 50, passing 35 and blank_rung 1 required')
    ids = [line.get('id') for line in lines]
    if any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        errors.append('criterion ids must be unique nonempty strings')
    totals = {rung: 0 for rung in ('full', '3', '1')}
    complete = True
    for line in lines:
        points = []
        for rung in totals:
            value = line.get(rung, {})
            if not isinstance(value, dict):
                errors.append(f'{rung} must be an object')
                complete = False
                points.append(None)
                continue
            p = value.get('points')
            if not isinstance(value.get('text'), str) or not value['text'].strip():
                errors.append(f'{line.get("id")}: {rung} text required')
            if p is None and rung != 'full' and not grading:
                complete = False
            elif type(p) is not int or p <= 0:
                errors.append(f'{line.get("id")}: exact positive integer {rung} points required')
            else:
                totals[rung] += p
            points.append(p)
        if all(type(p) is int for p in points) and not points[0] > points[1] > points[2]:
            errors.append(f'{line.get("id")}: require full > 3 > 1')
        tag = line.get('tag')
        if (not isinstance(tag, str) or tag not in TAGS) and (grading or tag is not None):
            errors.append(f'{line.get("id")}: approved tag required')
    ranks = [line.get('rank') for line in lines]
    known = [rank for rank in ranks if rank is not None]
    if any(type(rank) is not int or not 1 <= rank <= len(lines) for rank in known) or len(set(known)) != len(known) or (grading and len(known) != len(lines)):
        errors.append('unique ranks 1 to N required')
    if totals['full'] != 50:
        errors.append('full points must sum to 50')
    if complete and totals['3'] < 35:
        errors.append('partial everywhere must reach 35')
    if not isinstance(record.get('grading_note'), str) or not record['grading_note'].strip():
        errors.append('grading note required')
    gate = record.get('gate')
    if not isinstance(gate, dict):
        errors.append('explicit gate record required')
    else:
        rule = gate.get('rule')
        if 'rule' not in gate or (rule is not None and (not isinstance(rule, str) or not rule.strip())) or (grading and rule is None):
            errors.append('gate rule must be explicit; null remains a grading blocker')
        if 'failure_grade' not in gate or gate['failure_grade'] is not None:
            errors.append('gate failure grade must remain null until a policy is implemented')
    return errors


def load_record(reference: str) -> dict:
    # Deliberately restricted to course design records, never deployment state.
    if not isinstance(reference, str) or not re.fullmatch(r'course\d+/design/self-check-records/[a-z0-9-]+\.json', reference):
        raise ValueError('invalid self-check record reference')
    path = (ROOT / reference).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('self-check reference escapes repository')
    record = json.loads(path.read_text())
    errors = validate_record(record)
    if errors:
        raise ValueError('; '.join(errors))
    return record


def render_full_credit(record: dict) -> str:
    errors = validate_record(record)
    if errors:
        raise ValueError('; '.join(errors))
    lines = ''.join(f'<li>{html.escape(line["full"]["text"])} <strong>({line["full"]["points"]} points)</strong></li>' for line in record['criteria'])
    return f'<section class="walk-check self-check"><h2>Self-check</h2><ul>{lines}</ul></section>'


def score_rungs(record: dict, choices: dict[str, str], *, gate_passed: bool | None) -> dict:
    """Lookup only; caller supplies evidence-reviewed rung and gate judgments.

    Numeric grade is intentionally withheld for failed or unreviewed gates.
    Never treat a checked box as evidence or a rung label as points.
    """
    errors = validate_record(record, grading=True)
    if errors:
        raise ValueError('; '.join(errors))
    if set(choices) != {line['id'] for line in record['criteria']} or any(v not in ('full', '3', '1') for v in choices.values()):
        raise ValueError('exactly one allowed rung per criterion required')
    if gate_passed is not None and type(gate_passed) is not bool:
        raise ValueError('gate outcome must be bool or None')
    raw = sum(line[choices[line['id']]]['points'] for line in record['criteria'])
    return {'record_id': record['id'], 'record_version': record['version'],
            'record_sha256': hashlib.sha256(json.dumps(record, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'raw_sum': raw, 'gate_passed': gate_passed,
            'passes': raw >= 35 if gate_passed is True else False if gate_passed is False else None,
            'numeric_grade': raw if gate_passed is True else None,
            'requires_human_review': True}

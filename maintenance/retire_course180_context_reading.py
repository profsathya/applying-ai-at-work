"""Retire only page 3627's obsolete module placement, preserving the page.

Dry-run first. Apply rechecks the token and uses the repository's locked,
external deployment-state workflow. No page writes, publishing, or student reads.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.schema import parse_frontmatter_text, validate_artifact, validate_canvas_state
from canvas_sync.state import (
    canvas_fingerprint, canvas_snapshot, check_state_instance, file_lock,
    load_json, save_json_atomic, state_path_for_manifest, utc_now,
)
from maintenance.prepare_course180_repair import check_shell

PATH = 'course1/sprints/sprint-16/working-with-ai-context.md'
ARTIFACT = 'course1-sprints-sprint-16-working-with-ai-context'
PAGE, MODULE, ITEM = 3627, 2084, 18013
SLUG = 'working-with-ai-context'
HOSTED = 'https://profsathya.github.io/Common-Curriculum/deanza/course1/activities/working-with-ai-context.html'


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class ScopedClient(CanvasClient):
    def _request_response(self, method, path, json_body=None, params=None):
        route = urlsplit(path).path.removeprefix('/api/v1/courses/180/')
        allowed = ((method == 'GET' and re.fullmatch(
            r'(pages/working-with-ai-context|modules(/\d+/items)?)', route))
            or (method == 'DELETE' and route == f'modules/{MODULE}/items/{ITEM}'))
        if not allowed:
            raise ValueError('Retirement permits only module/page metadata reads and the exact placement delete')
        return super()._request_response(method, path, json_body, params)


def item_config(item: dict) -> dict:
    result = {k: v for k, v in item.items() if k != 'completion_requirement'}
    requirement = item.get('completion_requirement')
    if requirement:
        result['completion_requirement'] = {k: v for k, v in requirement.items() if k != 'completed'}
    return result


def module_config(module: dict) -> dict:
    return {k: v for k, v in module.items() if k not in ('state', 'completed_at')}


def prepare(state, page, modules, items, source, previous, source_commit):
    """Prove publication-only drift and prepare a single-entry reconciliation."""
    instance = state.get('instance', {})
    if (instance.get('course_id'), instance.get('base_url', '').rstrip('/')) != (180, 'https://cti-courses.instructure.com'):
        raise ValueError('Expected CTI course 180')
    if not re.fullmatch(r'[0-9a-f]{40}', source_commit):
        raise ValueError('Expected exact retirement source commit')
    fm, _ = parse_frontmatter_text(source.decode(), PATH)
    if (fm.get('artifact_id'), fm.get('type'), fm.get('slug'), fm.get('publish')) != (ARTIFACT, 'page', SLUG, False):
        raise ValueError('Source must retain the exact page identity and publish: false')
    entry = state.get('artifacts', {}).get(ARTIFACT, {})
    matches = [key for key, value in state.get('artifacts', {}).items()
               if value.get('canvas_type') == 'page' and
               (value.get('canvas_id') == PAGE or value.get('canvas_page_url') == SLUG)]
    if matches != [ARTIFACT]:
        raise ValueError('Page deployment identity is ambiguous')
    if (entry.get('canvas_type'), entry.get('canvas_id'), entry.get('canvas_module_id'),
            entry.get('canvas_page_url'), entry.get('local_path'), entry.get('hosted_url')) != (
            'page', PAGE, MODULE, SLUG, PATH, HOSTED):
        raise ValueError('Deployment identity changed')
    if entry.get('canvas_module_item_id') not in (ITEM, None) or entry.get('completion_requirement') not in ('must_view', None):
        raise ValueError('Deployment placement/completion changed')
    if digest(previous) != entry.get('content_hash'):
        raise ValueError('Recorded source does not match deployment content hash')
    if source != previous and source != previous.replace(b'publish: true\n', b'publish: false\n', 1):
        raise ValueError('Source differs beyond the reviewed retirement flag')
    if (page.get('page_id'), page.get('url'), page.get('title'), page.get('published'),
            page.get('hide_from_students'), page.get('front_page')) != (PAGE, SLUG, fm['title'], False, True, False):
        raise ValueError('Expected the retained unpublished page, hidden from participants')
    check_shell(page, fm['title'], HOSTED)
    actual = canvas_fingerprint(page, 'page')
    prior = canvas_fingerprint({**page, 'published': True}, 'page')
    if entry.get('canvas_fingerprint') not in (actual, prior):
        raise ValueError('Canvas drift is not provably publication-only')
    matching_modules = [m for m in modules if m['id'] == MODULE]
    if len(matching_modules) != 1:
        raise ValueError('Target module is missing or ambiguous')
    module = matching_modules[0]
    if module.get('name') != fm['module'] or module.get('published') is not True:
        raise ValueError('Target module changed')
    for mid, rows in items.items():
        for item in rows:
            if item['id'] == ITEM and (mid != MODULE or item.get('type') != 'Page' or item.get('page_url') != SLUG):
                raise ValueError('Exact module item identity changed')
    placements = [(mid, item) for mid, rows in items.items() for item in rows
                  if item.get('type') == 'Page' and item.get('page_url') == SLUG]
    if placements:
        if len(placements) != 1 or (placements[0][0], placements[0][1]['id']) != (MODULE, ITEM):
            raise ValueError('Page placement moved or duplicated')
        item = placements[0][1]
        if item.get('published') is not False or item.get('completion_requirement', {}).get('type') != 'must_view':
            raise ValueError('Expected unpublished must_view placement')
        if entry.get('canvas_module_item_id') != ITEM:
            raise ValueError('Live placement is not state-backed')
    proposal = copy.deepcopy(state)
    target = proposal['artifacts'][ARTIFACT]
    target.update(canvas_module_item_id=None, canvas_fingerprint=actual,
                  content_hash=digest(source), source_commit=source_commit)
    target.pop('completion_requirement', None)
    target.pop('canvas_payload_hash', None)
    changes = [{
        'field': field, 'before': entry.get(field), 'after': target.get(field)
    } for field in sorted(set(entry) | set(target)) if entry.get(field) != target.get(field)]
    evidence = {'state': state, 'page': canvas_snapshot(page, 'page'),
                'modules': [module_config(m) for m in modules],
                'items': {mid: [item_config(i) for i in rows] for mid, rows in items.items()},
                'source_hash': digest(source), 'source_commit': source_commit}
    token = digest(json.dumps(evidence, sort_keys=True).encode())[:20]
    report = {'page_id': PAGE, 'module_id': MODULE, 'module_item_id': ITEM,
              'operations': ([{'action': 'delete_module_item', 'module_id': MODULE,
                               'module_item_id': ITEM}] if placements else []),
              'page_published': False, 'expected_fingerprint': entry['canvas_fingerprint'],
              'live_fingerprint': actual, 'publication_only_prior_fingerprint': prior,
              'changes': changes, 'confirmation_token': token}
    return proposal, report


def collect(client):
    page = client.get_page(SLUG)
    modules = client.list_modules()
    items = {m['id']: client.list_module_items(m['id']) for m in modules}
    return page, modules, items


def verify_after(before, after):
    old_page, old_modules, old_items = before
    page, modules, items = after
    if page != old_page:
        raise ValueError('Retained page changed during removal')
    expected_modules = copy.deepcopy(old_modules)
    next(m for m in expected_modules if m['id'] == MODULE)['items_count'] -= 1
    if [module_config(m) for m in modules] != [module_config(m) for m in expected_modules]:
        raise ValueError('Module configuration changed unexpectedly')
    expected_items = {mid: [item_config(i) for i in rows if not (mid == MODULE and i['id'] == ITEM)]
                      for mid, rows in old_items.items()}
    if {mid: [item_config(i) for i in rows] for mid, rows in items.items()} != expected_items:
        raise ValueError('Other placements, ordering, or completion requirements changed')


def prepare_progress(progress):
    """Clear only the retained page's removed placement in generated metadata."""
    if (progress.get('canvasCourseId'), progress.get('courseKey')) != (180, 'course1'):
        raise ValueError('Expected course 180 progress map')
    result = copy.deepcopy(progress)
    rows = [row for row in result['items'] if row.get('artifactId') == ARTIFACT]
    if len(rows) != 1:
        raise ValueError('Retired progress row is missing or ambiguous')
    row = rows[0]
    if (row.get('canvasId'), row.get('canvasModuleId'), row.get('canvasPageUrl'),
            row.get('canvasType'), row.get('localPath')) != (PAGE, MODULE, SLUG, 'page', PATH):
        raise ValueError('Retired progress identity changed')
    if row.get('canvasModuleItemId') not in (ITEM, None) or row.get('completionRequirement') not in ('must_view', None):
        raise ValueError('Retired progress placement/completion changed')
    row.update(canvasModuleItemId=None, completionRequirement=None)
    return result


def git_source(commit, path):
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Missing exact source provenance commit')
    return subprocess.run(['git', 'show', f'{commit}:{path}'], cwd=ROOT,
                          check=True, capture_output=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state-dir', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--env-file', type=Path, default=ROOT / '.env')
    parser.add_argument('--evidence-dir', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--confirm-token')
    args = parser.parse_args()
    load_dotenv(args.env_file)
    manifest_path = ROOT / 'course1/manifests/production.json'
    manifest = load_json(manifest_path)
    check_instance_ready(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    state_path = state_path_for_manifest(manifest_path, args.state_dir.resolve(), manifest)
    errors = validate_artifact(ROOT / PATH) + validate_canvas_state(state_path)
    if errors:
        raise ValueError('; '.join(errors))
    args.evidence_dir.mkdir(parents=True, exist_ok=False)
    client = ScopedClient.from_env(course_id=180)
    with file_lock(state_path):
        state = load_json(state_path)
        check_state_instance(state, manifest, state_path)
        source = (ROOT / PATH).read_bytes()
        if source != git_source(args.source_commit, PATH):
            raise ValueError('Local source differs from exact retirement commit')
        previous = git_source(state['artifacts'][ARTIFACT]['source_commit'], PATH)
        before = collect(client)
        proposal, report = prepare(state, *before, source, previous, args.source_commit)
        save_json_atomic(args.evidence_dir / 'before.json', {'state': state, 'page': before[0],
                         'modules': before[1], 'items': before[2]})
        report['mode'] = 'apply' if args.apply else 'dry-run'
        save_json_atomic(args.evidence_dir / 'plan.json', report)
        save_json_atomic(args.evidence_dir / 'proposed-state.json', proposal)
        if validate_canvas_state(args.evidence_dir / 'proposed-state.json'):
            raise ValueError('Proposed deployment state fails schema validation')
        if args.apply:
            if args.confirm_token != report['confirmation_token']:
                raise ValueError('Apply requires the matching fresh dry-run token')
            if report['operations']:
                client.delete_module_item(MODULE, ITEM)
                after = collect(client)
                save_json_atomic(args.evidence_dir / 'after.json', {'page': after[0], 'modules': after[1], 'items': after[2]})
                verify_after(before, after)
            else:
                after = before
            if (ROOT / PATH).read_bytes() != source or load_json(state_path) != state:
                raise ValueError('Source/state changed during removal; inspect before reconciling state')
            prepare(state, *after, source, previous, args.source_commit)
            proposal['artifacts'][ARTIFACT]['last_pulled'] = utc_now()
            proposal['last_sync'] = utc_now()
            save_json_atomic(state_path, proposal)
            report['verified'] = True
            save_json_atomic(args.evidence_dir / 'result.json', report)
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

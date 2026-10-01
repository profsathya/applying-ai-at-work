"""Prepare an exact, read-only course 180 reconciliation proposal.

No Canvas writes, submission reads, state-branch updates, rendering or export.
Run again after an approved publication to record the replacement's verified state.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.hosted_html import with_context
from canvas_sync.schema import parse_frontmatter_text
from canvas_sync.state import canvas_fingerprint, utc_now
from canvas_sync.walkthrough_release import ASSESSMENT_KEYS, _rubric_shape

ROOT = Path(__file__).resolve().parents[1]
TARGETS = {
    7149: ('course1/sprints/sprint-14/brainstorm-your-list.md', 2079, 17977),
    7185: ('course1/sprints/sprint-14/brainstorm-your-list-walk-through.md', 2079, 18020),
    3624: ('course1/sprints/sprint-14/the-problem-frame.md', 2079, 17985),
    7180: ('course1/sprints/sprint-15/sprint-3-concept-check-v4.md', 2081, 18014),
}


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


class ReadOnlyClient(CanvasClient):
    def _request_response(self, method, path, json_body=None, params=None):
        # Pagination may be absolute; CanvasClient also enforces the same origin.
        route = path.split('?', 1)[0].split('/api/v1/courses/180/')[-1]
        if method != 'GET' or not re.fullmatch(
            r'(assignments/(7149|7185|7180)|pages/the-problem-frame|modules(/\d+/items)?)', route
        ):
            raise ValueError('Repair preflight allows only target metadata and module GETs')
        return super()._request_response(method, path, json_body, params)


class Shell(HTMLParser):
    """Accept only the generated shell and known Canvas sanitizer normalization."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []

    def handle_starttag(self, tag, attrs):
        if len(dict(attrs)) != len(attrs):
            raise ValueError('Duplicate shell attributes')
        values = dict(attrs)
        if 'style' in values:
            css = {}
            for rule in values['style'].split(';'):
                if rule.strip():
                    key, value = rule.split(':', 1)
                    key, value = key.strip(), value.strip()
                    if key in css:
                        raise ValueError('Duplicate shell style')
                    css[key] = value
            if css.get('border') in ('0', '0px none currentcolor'):
                css['border'] = '0'
            values['style'] = css
        if values.get('allowfullscreen') in (None, '', 'allowfullscreen') and 'allowfullscreen' in values:
            values['allowfullscreen'] = True
        self.tags.append(('start', tag, values))

    def handle_endtag(self, tag):
        self.tags.append(('end', tag))

    def handle_data(self, data):
        if data.strip():
            raise ValueError('Unexpected instructional text in hosted shell')

    def handle_comment(self, data):
        raise ValueError('Unexpected hosted shell comment')


def check_shell(live, title, hosted_url):
    parser = Shell()
    parser.feed(live.get('description', live.get('body', '')))
    expected = [
        ('start', 'div', {'class': 'hosted-html-shell'}),
        ('start', 'iframe', {'title': title, 'src': with_context(hosted_url, 'canvas'),
                            'width': '100%', 'height': '900', 'loading': 'lazy',
                            'style': {'border': '0', 'width': '100%', 'min-height': '900px'},
                            'allowfullscreen': True}),
        ('end', 'iframe'), ('end', 'div'),
    ]
    if parser.tags != expected:
        raise ValueError('Hosted wrapper differs beyond reviewed sanitizer normalization')


def prepare(state, live, modules, items, sources, released, hosted_hashes, source_commit):
    """Pure local proposal; fail closed if any of the four reviewed items changed."""
    if state.get('instance', {}).get('course_id') != 180 or state['instance'].get('base_url', '').rstrip('/') != 'https://cti-courses.instructure.com':
        raise ValueError('Expected CTI course 180 state')
    if not re.fullmatch('[0-9a-f]{40}', source_commit):
        raise ValueError('Expected exact source commit')
    proposed = copy.deepcopy(state)
    changes = []
    module_by_id = {m['id']: m for m in modules}
    for ident, (path, module_id, item_id) in TARGETS.items():
        matches = [(k, e) for k, e in state['artifacts'].items() if e.get('canvas_id') == ident and e.get('local_path') == path]
        if len(matches) != 1:
            raise ValueError(f'{ident}: exact state identity missing or ambiguous')
        key, entry = matches[0]
        expected_type = 'page' if ident == 3624 else 'assignment'
        if (entry.get('canvas_type'), entry.get('canvas_module_id'), entry.get('canvas_module_item_id')) != (expected_type, module_id, item_id):
            raise ValueError(f'{ident}: deployment placement changed')
        obj = live[ident]
        if obj.get('page_id' if ident == 3624 else 'id') != ident:
            raise ValueError(f'{ident}: wrong live object')
        if module_by_id.get(module_id, {}).get('published') is not True:
            raise ValueError(f'{ident}: expected published module')
        placements = [(mid, i) for mid, rows in items.items() for i in rows
                      if ((ident == 3624 and i.get('type') == 'Page' and i.get('page_url') == 'the-problem-frame')
                          or (ident != 3624 and i.get('type') == 'Assignment' and i.get('content_id') == ident))]
        if len(placements) != 1 or (placements[0][0], placements[0][1]['id']) != (module_id, item_id):
            raise ValueError(f'{ident}: live placement missing, moved or duplicated')
        if type(obj.get('published')) is not bool or placements[0][1].get('published') is not obj['published']:
            raise ValueError(f'{ident}: object/module visibility mismatch')
        if ident != 7185 and obj['published'] is not (ident != 3624):
            raise ValueError(f'{ident}: reviewed live publication changed')
        raw = sources[path]
        fm, body = parse_frontmatter_text(raw, path)
        old_fm, old_body = parse_frontmatter_text(released[path], path)
        if digest(released[path]) != entry['content_hash']:
            raise ValueError(f'{ident}: released source fingerprint mismatch')
        if {k: v for k, v in fm.items() if k != 'publish'} != {k: v for k, v in old_fm.items() if k != 'publish'} or body != old_body:
            raise ValueError(f'{ident}: source changed beyond reviewed publication flag')
        if fm.get('publish') is not (ident != 3624):
            raise ValueError(f'{ident}: source publication intent is not reconciled')
        if obj.get('name', obj.get('title')) != fm['title']:
            raise ValueError(f'{ident}: live title differs')
        if ident != 3624 and (obj.get('points_possible') != fm['points'] or obj.get('submission_types') != ['online_text_entry']):
            raise ValueError(f'{ident}: live grading/submission contract changed')
        if ident in (7149, 7185) and (obj.get('grading_type'), obj.get('assignment_group_id')) != ('pass_fail', 429):
            raise ValueError(f'{ident}: Brainstorm grading configuration changed')
        if ident == 7180 and (obj.get('grading_type'), obj.get('assignment_group_id')) != ('points', 429):
            raise ValueError('7180: Concept Check grading configuration changed')
        if hosted_hashes.get(ident) != entry.get('hosted_hash'):
            raise ValueError(f'{ident}: hosted HTML changed; review before accepting a new baseline')
        check_shell(obj, fm['title'], entry['hosted_url'])
        fingerprint = canvas_fingerprint(obj, expected_type)
        if ident in (3624, 7180) and fingerprint != entry['canvas_fingerprint'] and canvas_fingerprint(dict(obj, published=not obj['published']), expected_type) != entry['canvas_fingerprint']:
            raise ValueError(f'{ident}: stored drift exceeds a publication-only change')
        if ident == 7149 and fingerprint != entry['canvas_fingerprint']:
            raise ValueError('7149: original changed; preserve and review')
        new_entry = proposed['artifacts'][key]
        new_entry['canvas_fingerprint'] = fingerprint
        # An unpublished replacement remains staged. Never mark publish:true
        # source as released until a fresh read proves publication succeeded.
        if fm['publish'] is obj['published'] and digest(raw) != entry['content_hash']:
            new_entry['content_hash'] = digest(raw)
            new_entry['source_commit'] = source_commit
        for field in new_entry:
            if new_entry[field] != entry.get(field):
                changes.append({'canvas_id': ident, 'field': field, 'before': entry.get(field), 'after': new_entry[field]})
    old, new = live[7149], live[7185]
    if any(old.get(k) != new.get(k) for k in ASSESSMENT_KEYS) or _rubric_shape(old.get('rubric')) != _rubric_shape(new.get('rubric')):
        raise ValueError('Brainstorm assessment settings differ; do not publish')
    # Per-person dates/overrides require a separate review, without fetching identities.
    if old.get('has_overrides') or new.get('has_overrides') or old.get('only_visible_to_overrides') or new.get('only_visible_to_overrides'):
        raise ValueError('Brainstorm override configuration requires instructor review')
    order = [i['id'] for i in sorted(items[2079], key=lambda i: i['position'])]
    if order.index(18020) != order.index(17977) + 1:
        raise ValueError('Brainstorm replacement no longer follows original')
    material = {'state': state, 'live': live, 'modules': modules, 'items': items,
                'source_commit': source_commit, 'sources': sources, 'hosted_hashes': hosted_hashes}
    token = digest(json.dumps(material, sort_keys=True, separators=(',', ':')))
    return proposed, {'mode': 'review-only', 'checked_at': utc_now(), 'source_commit': source_commit,
                      'review_token': token, 'changes': changes,
                      'brainstorm_published': new['published'],
                      'next_action': 'Verify export readiness; no further Canvas publication needed' if new['published'] else
                      'After separate approval, publish assignment 7185 only, preserving its wrapper/settings and all original 7149 data; read back object and module visibility, then rerun this planner.',
                      'original_module_removal': 'Not included. Requires separate approval after replacement verification; delete module item 17977 only, never assignment 7149 or its publication state.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--hosted-root', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    state = json.loads(args.state.read_text())
    client = ReadOnlyClient.from_env(course_id=180)
    if client.base_url != 'https://cti-courses.instructure.com':
        raise ValueError('Expected CTI Canvas credentials')
    modules = client.list_modules()
    items = {m['id']: client.list_module_items(m['id']) for m in modules}
    sources, released, live, hosted_hashes = {}, {}, {}, {}
    for ident, (path, _, _) in TARGETS.items():
        e = next(e for e in state['artifacts'].values() if e.get('canvas_id') == ident and e.get('local_path') == path)
        sources[path] = (ROOT / path).read_text()
        committed = subprocess.check_output(['git', 'show', commit + ':' + path], cwd=ROOT, text=True)
        if sources[path] != committed:
            raise ValueError('Commit reviewed source edits before preparing a provenance-bearing proposal')
        released[path] = subprocess.check_output(['git', 'show', e['source_commit'] + ':' + path], cwd=ROOT, text=True)
        live[ident] = client.get_page('the-problem-frame') if ident == 3624 else client.get_assignment(ident)
        hosted_path = Path(e['hosted_path'])
        if hosted_path.is_absolute() or '..' in hosted_path.parts:
            raise ValueError('Unsafe hosted path')
        hosted_hashes[ident] = hashlib.sha256((args.hosted_root / 'deanza' / hosted_path).read_bytes()).hexdigest()
    proposal, report = prepare(state, live, modules, items, sources, released, hosted_hashes, commit)
    args.output_dir.mkdir(parents=True, exist_ok=False)
    (args.output_dir / 'production.proposed.json').write_text(json.dumps(proposal, indent=2, sort_keys=True) + '\n')
    (args.output_dir / 'review.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

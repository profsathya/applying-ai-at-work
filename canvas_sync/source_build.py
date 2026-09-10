"""Assemble a reviewed document build map without rewriting selected source blocks.

python canvas_sync/source_build.py --packet DIR/source-packet.json --map MAP.json --output NEW_DIR
python canvas_sync/source_build.py --verify ARTIFACT.md

Adjacent *.sources.json files are portable selected-source evidence, not raw private
corpora. Normal schema validation checks exact body/title fidelity against this record.
Rebuild from the original packet to change sourced wording or accept a different view.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

if __package__ in (None, ''):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.source_intake import (IntakeError, digest, json_bytes, parse_source,
                                       read_limited, render_block, walk_blocks)


class BuildError(ValueError):
    pass


def block_index(document):
    return {b['id']: b for section in document['sections'] for b in walk_blocks(section['blocks'])}


def has_changes(block):
    return any(s.get('changes') for b in walk_blocks([block]) for s in b.get('segments', []))


def selection(block, spec):
    if spec.get('view') not in ('base', 'proposed'):
        raise BuildError('Every source selection needs an explicit base or proposed view')
    all_flags = {f for b in walk_blocks([block]) for f in b.get('flags', [])}
    if 'render_unsupported' in all_flags:
        raise BuildError(f"{block['id']}: unsupported presentation; use a labelled adaptation with source references")
    if (has_changes(block) or all_flags or any(b.get('comment_ids') for b in walk_blocks([block]))) and not spec.get('decision'):
        raise BuildError(f"{block['id']}: revisions, comments, or flags require a recorded decision")
    risky = all_flags & {'answer_key', 'raw_configuration', 'editorial_marker', 'diagram_source'}
    if risky - set(spec.get('allow_flags', [])):
        raise BuildError(f"{block['id']}: review-only flags {sorted(risky)} cannot enter learner content without explicit classification")
    return render_block(block, spec['view'])


def verify_evidence(frontmatter, body, evidence):
    """Return new prose for the style gate; validate complete sourced passages, not a bypass flag."""
    if evidence.get('evidence_version') != 1 or evidence.get('artifact_id') != frontmatter.get('artifact_id'):
        raise BuildError('Source evidence version/identity mismatch')
    if evidence.get('frontmatter_sha256') != digest(json_bytes(frontmatter)):
        raise BuildError('Frontmatter differs from the reviewed build; rebuild or update the map')
    expected, new = [], []
    for part in evidence['parts']:
        if part.get('kind') == 'source':
            if not re.fullmatch('[0-9a-f]{64}', part.get('source_sha256', '')) or not part.get('source_name'):
                raise BuildError('Missing source fingerprint/name')
            if not part['block']['id'].startswith('d-' + part['source_sha256'][:16] + ':'):
                raise BuildError('Source reference does not match snapshot fingerprint')
            if part.get('block_sha256') != digest(json_bytes(part['block'])):
                raise BuildError('Source block evidence was altered')
            text = selection(part['block'], part)
            if text != part['markdown']:
                raise BuildError('Selected source Markdown no longer matches its evidence')
        elif part.get('kind') == 'new':
            text = part['markdown']; new.append(text)
            if not part.get('reason'):
                raise BuildError('New/adapted prose requires a reason')
        else:
            raise BuildError('Unknown evidence part kind')
        expected.append(text)
    expected_body = '\n\n'.join(expected) + '\n'
    if body != expected_body or digest(body.encode()) != evidence['body_sha256']:
        raise BuildError('Body differs from source-backed assembly; edit the build map and rebuild')
    title_source = evidence.get('title_source')
    if title_source:
        if title_source['block_sha256'] != digest(json_bytes(title_source['block'])):
            raise BuildError('Title source evidence was altered')
        selection(title_source['block'], title_source)
        if frontmatter['title'] != title_source['block']['text'][title_source['view']]:
            raise BuildError('Title differs from selected source text')
    else:
        new.append(frontmatter.get('title', ''))
    return '\n'.join(new)


def validate_source_evidence(md_path: Path, frontmatter: dict, body: str) -> tuple[list[str], str]:
    name = frontmatter.get('source_provenance')
    if not name:
        return [], body + '\n' + str(frontmatter.get('title', ''))
    try:
        if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9-]+\.sources\.json', name):
            raise BuildError('Source provenance must be an adjacent <slug>.sources.json file')
        path = md_path.parent / name
        if path.is_symlink():
            raise BuildError('Source evidence cannot be a symlink')
        evidence = json.loads(read_limited(path))
        return [], verify_evidence(frontmatter, body, evidence)
    except (OSError, ValueError, KeyError, TypeError) as e:
        return [f'{md_path}: source fidelity: {e}'], body + '\n' + str(frontmatter.get('title', ''))


def assemble(packet_path: Path, map_path: Path, output: Path, *, publish_ready: bool = False) -> dict:
    if output.exists():
        raise BuildError('Output already exists; choose a new draft directory (no overwrite)')
    packet_raw = read_limited(packet_path); packet = json.loads(packet_raw)
    build_map = json.loads(read_limited(map_path))
    if packet.get('packet_version') != 1 or build_map.get('map_version') != 1:
        raise BuildError('Unsupported packet or build-map version')
    if build_map.get('packet_sha256') != digest(packet_raw):
        raise BuildError('Packet changed since the build map was prepared')
    target = build_map['target']
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', target.get('course', '')) or type(target.get('sprint')) is not int or target['sprint'] < 0:
        raise BuildError('Build map needs a valid target course and storage sprint number')
    if not build_map.get('artifacts'):
        raise BuildError('Build map has no artifacts')
    documents = {}; lookup = {}
    for doc in packet['documents']:
        rel = Path(doc['raw_path'])
        raw_path = packet_path.parent / rel
        if rel.is_absolute() or '..' in rel.parts or not raw_path.resolve().is_relative_to(packet_path.parent.resolve()):
            raise BuildError('Source raw path escapes packet directory')
        raw = read_limited(raw_path)
        if digest(raw) != doc['sha256']:
            raise BuildError('Raw source snapshot changed')
        # Reparse original bytes so an edited packet cannot masquerade as source wording.
        parsed = parse_source(raw, doc['name'])
        index = block_index(parsed)
        if index != block_index(doc):
            raise BuildError('Packet blocks no longer match the original snapshot')
        if doc['id'] in documents:
            raise BuildError('Duplicate source snapshot IDs; intake distinct versions separately')
        documents[doc['id']] = doc
        lookup.update({k: (doc, b) for k, b in index.items()})
    roles = build_map.get('source_roles', {})
    for doc_id in documents:
        if not isinstance(roles.get(doc_id), dict) or not roles[doc_id].get('role') or not roles[doc_id].get('reason'):
            raise BuildError(f'Source role and reason required for {doc_id}')
    selected = set(); prepared = []; slugs = set(); identities = set(); positions = set()
    def source_part(spec):
        ref = spec['ref']
        if ref not in lookup:
            raise BuildError(f'Unknown source reference: {ref}')
        doc, block = lookup[ref]
        if any('unverified' in item.lower() or 'incomplete' in item.lower() for item in doc['limitations']) and not roles[doc['id']].get('coverage_decision'):
            raise BuildError('Incomplete remote coverage needs a source_roles coverage_decision before using its text')
        if spec.get('role') != 'learner':
            raise BuildError('Source body selections must explicitly identify role: learner')
        text = selection(block, spec)
        selected.update(b['id'] for b in walk_blocks([block]))
        return {**spec, 'kind': 'source', 'source_name': doc['name'], 'source_sha256': doc['sha256'],
                'block': block, 'block_sha256': digest(json_bytes(block)), 'markdown': text}
    for artifact in build_map['artifacts']:
        fm = dict(artifact['frontmatter']); slug = fm['slug']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
            raise BuildError('Invalid artifact slug')
        if slug in slugs or fm['artifact_id'] in identities or fm['position'] in positions:
            raise BuildError('Duplicate artifact slug, identity, or module position')
        slugs.add(slug); identities.add(fm['artifact_id']); positions.add(fm['position'])
        if (fm.get('publish') is not False and not publish_ready) or fm.get('sprint') != target['sprint']:
            raise BuildError('Document builds must be unpublished drafts in the map target sprint')
        fm['source_provenance'] = slug + '.sources.json'
        parts = []
        for part in artifact['parts']:
            if 'ref' in part:
                parts.append(source_part(part))
            elif 'new' in part and part.get('reason'):
                if any(ref not in lookup for ref in part.get('based_on', [])):
                    raise BuildError('Unknown adaptation source reference')
                parts.append({'kind': 'new', 'markdown': part['new'], 'reason': part['reason'], 'based_on': part.get('based_on', [])})
            else:
                raise BuildError('Each part needs a source ref or labelled new prose with a reason')
        body = '\n\n'.join(part['markdown'] for part in parts) + '\n'
        evidence = {'evidence_version': 1, 'artifact_id': fm['artifact_id'], 'packet_sha256': digest(packet_raw),
                    'map_sha256': digest(read_limited(map_path)), 'body_sha256': digest(body.encode()),
                    'frontmatter_sha256': digest(json_bytes(fm)), 'parts': parts,
                    'metadata_decisions': artifact.get('metadata_decisions', []),
                    'source_roles': roles, 'decisions': build_map.get('decisions', [])}
        if artifact.get('title_source'):
            evidence['title_source'] = source_part(artifact['title_source'])
        verify_evidence(fm, body, evidence)
        prepared.append((slug, fm, body, evidence))
    report = {'target': target, 'artifacts': [s + '.md' for s, *_ in prepared],
              'selected_blocks': len(selected), 'unselected_blocks': sorted(set(lookup) - selected),
              'source_roles': roles, 'decisions': build_map.get('decisions', []),
              'open_questions': build_map.get('open_questions', []),
              'note': 'Unselected blocks remain in the private packet. This report is not publishing approval.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix='.build-', dir=output.parent))
    try:
        for slug, fm, body, evidence in prepared:
            (staging / (slug + '.md')).write_text('---\n' + yaml.safe_dump(fm, allow_unicode=True, sort_keys=False) + '---\n\n' + body, encoding='utf-8')
            (staging / fm['source_provenance']).write_bytes(json_bytes(evidence))
        from canvas_sync.schema import validate_artifact
        errors = [e for slug, *_ in prepared for e in validate_artifact(staging / (slug + '.md'))]
        if errors:
            raise BuildError('\n'.join(errors))
        output.mkdir()
        for child in staging.iterdir():
            shutil.move(str(child), output / child.name)
    finally:
        shutil.rmtree(staging, ignore_errors=True)
    report_path = map_path.with_suffix('.review.json')
    report_path.write_bytes(json_bytes(report))
    return report


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', type=Path); p.add_argument('--map', type=Path); p.add_argument('--output', type=Path)
    p.add_argument('--verify', type=Path)
    p.add_argument('--publish-ready', action='store_true', help='Allow reviewed publish values in local output; never writes Canvas')
    args = p.parse_args(argv)
    try:
        if args.verify:
            from canvas_sync.schema import validate_artifact
            errors = validate_artifact(args.verify)
            if errors:
                raise BuildError('\n'.join(errors))
            print(f'Validated {args.verify}')
        elif args.packet and args.map and args.output:
            report = assemble(args.packet, args.map, args.output, publish_ready=args.publish_ready)
            print(f"Built {len(report['artifacts'])} local artifacts in {args.output}")
        else:
            p.error('Use --verify or all of --packet, --map, --output')
    except (IntakeError, OSError, ValueError, KeyError, TypeError) as e:
        print(f'Build failed: {e}', file=sys.stderr); return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

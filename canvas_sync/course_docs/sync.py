"""Build and deliver independent Google Doc sections from a published release.

Adapted from Common Curriculum's build_course_context.py and CourseDocSync.
No HTML crawl or upstream workflow invocation is used.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import urllib.request
from datetime import datetime, timezone

CORE_URL = 'https://profsathya.github.io/Common-Curriculum/common/dojo/dojo-core.txt'
TITLE = 'CIS 501: Reframing Problems with AI — Dojo and Course Context'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def course_section(release):
    if release.get('schema_version') != 1 or not release.get('release_id') or not release.get('generated_at'):
        raise ValueError('Invalid release metadata')
    if not isinstance(release.get('pages'), list):
        raise ValueError('Missing release pages')
    pages, seen = [], set()
    for page in release['pages']:
        path = page.get('path', '')
        if not path or path.startswith('/') or '..' in path.split('/') or path in seen:
            raise ValueError('Invalid or duplicate release path')
        if not all(isinstance(page.get(k), str) and page[k].strip() for k in ('title', 'source_url', 'content')):
            raise ValueError('Incomplete release page')
        if not page['source_url'].startswith('https://'):
            raise ValueError('Source must use HTTPS')
        seen.add(path)
        pages.append(dict(page, content='Source: ' + page['source_url'] + '\n' + page['content']))
    return dict(tab='Course', heading=TITLE, intro='Published course material. Check source links for requirements.',
                release_id=release['release_id'], released_at=release['generated_at'], pages=pages, glossary=[])


def dojo_section(core):
    lines = core.strip().splitlines()
    if len(lines) < 2 or 'dojo' not in lines[0].lower() or '<html' in core.lower():
        raise ValueError('Canonical Core response is not valid Dojo text')
    return dict(tab='Dojo', heading='The Dojo: how to work with this material',
                pages=[dict(path=CORE_URL, title=lines[0], content='Source: ' + CORE_URL + '\n' + '\n'.join(lines[1:]))], glossary=[])


def build(release, core, generation, repository, commit_sha):
    if generation < 1 or not repository or not commit_sha:
        raise ValueError('A positive main-branch generation and source identity are required')
    sections = []
    if release is not None:
        sections.append(course_section(release))
    if core is not None:
        sections.append(dojo_section(core))
    if not sections:
        raise ValueError('No document section selected')
    for section in sections:
        section['content_digest'] = digest(section)
    payload = dict(course='course1', title=TITLE,
                generated_at_pacific=datetime.now(timezone.utc).isoformat(),
                metadata=dict(generation=generation, repository=repository, commit_sha=commit_sha), sections=sections)
    for section in sections:
        section['rendered_digest'] = rendered_digest(section, payload)
    return payload


def rendered_digest(section, payload):
    lines = [section['heading']]
    if section.get('intro'):
        lines.append(section['intro'])
    lines.extend(['Last updated ' + payload['generated_at_pacific'] + '.',
                  'Source version: ' + section.get('release_id', section['content_digest']) +
                  ' | Generation: ' + str(payload['metadata']['generation'])])
    for page in section['pages']:
        lines.append(page.get('title') or page['path'])
        for line in page['content'].splitlines():
            heading = re.match(r'^#{1,6}\s+(.+)$', line)
            if heading:
                line = heading[1].strip()
            elif line.startswith('- '):
                line = line[2:]
            elif re.match(r'^\*\*(.+)\*\*$', line):
                line = line[2:-2]
            lines.append(line)
    normalized = '\n'.join(line.strip() for line in lines if line.strip())
    return hashlib.sha256(normalized.encode()).hexdigest()


def verify_response(payload, response, document_id):
    if not document_id or response.get("document_id") != document_id:
        raise ValueError("Receiver returned an unexpected document")
    if response.get('ok') is not True:
        raise ValueError('Document endpoint rejected update: ' + str(response.get('error', 'unknown')))
    for section in payload['sections']:
        actual = response.get('versions', {}).get(section['tab'], {})
        if (actual.get('content_digest') != section['content_digest'] or
                actual.get('generation') != payload['metadata']['generation'] or
                actual.get('rendered_digest') != section['rendered_digest']):
            raise ValueError('Document endpoint did not confirm expected section version')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path)
    parser.add_argument('--section', choices=['course', 'dojo', 'all'], default='all')
    parser.add_argument('--generation', type=int, required=True)
    parser.add_argument('--repository', required=True)
    parser.add_argument('--commit-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    release = core = None
    if args.section in ('course', 'all'):
        if not args.release:
            parser.error('--release is required for Course updates')
        release = json.loads(args.release.read_text())
    if args.section in ('dojo', 'all'):
        with urllib.request.urlopen(CORE_URL, timeout=30) as response:
            core = response.read().decode('utf-8')
    payload = build(release, core, args.generation, args.repository, args.commit_sha)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + '\n')
    if args.send:
        url = os.environ['COURSE_DOC_SYNC_URL']
        if not url.startswith('https://script.google.com/'):
            raise ValueError('Expected HTTPS Google Apps Script endpoint')
        config = json.loads(Path('config/course-docs.json').read_text())
        if not config.get('document_id'):
            raise ValueError('Configure the expected document ID before sending')
        request_payload = dict(payload, token=os.environ['COURSE_DOC_SYNC_TOKEN'], document_id=config['document_id'])
        request = urllib.request.Request(url, data=json.dumps(request_payload).encode(),
                                         headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(request, timeout=180) as response:
            result = json.load(response)
        verify_response(payload, result, config['document_id'])
        print('Confirmed document sections: ' + ', '.join(s['tab'] for s in payload['sections']))


if __name__ == '__main__':
    main()

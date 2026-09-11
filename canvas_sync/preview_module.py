#!/usr/bin/env python3
"""Build an immutable local module preview and optional browser review evidence."""
from __future__ import annotations

import argparse
from functools import partial
import hashlib
import html
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from threading import Thread

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.hosted_html import (
    discover_artifact_files, hosted_output_path, is_ai_activity_delivery,
    markdown_body_to_html, render_hosted_artifact,
)
from canvas_sync.local_images import local_image_assets
from canvas_sync.schema import parse_frontmatter, validate_artifact, validate_manifest
from canvas_sync.state import course_dir_for_manifest


def word_counts(fm: dict, body: str) -> dict:
    def count(text):
        return len(re.findall(r"\b[\w]+(?:['’-][\w]+)*\b", text))
    tasks = fm.get('guided_assignment', {}).get('tasks', [])
    return {'body': count(body), 'prompts': sum(count(t['prompt']) for t in tasks),
            'criteria': sum(count(c) for t in tasks for c in t.get('criteria', []))}


def read_baseline(path: Path, course: str, sprint: int) -> dict:
    record = json.loads((path / 'preview.json').read_text())
    if (record.get('version'), record.get('course'), record.get('sprint')) != (1, course, sprint):
        raise ValueError('Baseline must be a version-1 preview of the same course and storage sprint')
    if any(p.is_symlink() for p in (path / 'current').rglob('*')):
        raise ValueError('Baseline output must not contain symlinks')
    for item in record['pages']:
        if item['after']:
            target = (path / item['after']).resolve()
            if not target.is_relative_to((path / 'current').resolve()) or not target.is_file():
                raise ValueError('Baseline page must exist inside its current/ directory')
    return record


def build_preview(manifest_path: Path, sprint: int, output: Path,
                  baseline: Path | None = None, state_dir: Path | None = None) -> dict:
    manifest_path, output = manifest_path.resolve(), output.resolve()
    course_dir = course_dir_for_manifest(manifest_path).resolve()
    if sprint < 0:
        raise ValueError('Sprint must be non-negative')
    if output.is_relative_to(course_dir) or course_dir.is_relative_to(output):
        raise ValueError('Preview output must be separate from course source')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a new or empty output directory to preserve review snapshots')
    if baseline:
        baseline = baseline.resolve()
        if output.is_relative_to(baseline) or baseline.is_relative_to(output):
            raise ValueError('Baseline and output directories must be separate')
    errors = validate_manifest(manifest_path)
    files = discover_artifact_files(manifest_path, sprint)
    if not files:
        raise ValueError(f'No artifacts found in {course_dir.name}/sprints/sprint-{sprint}')
    for p in files:
        errors.extend(validate_artifact(p))
    if errors:
        raise ValueError('\n'.join(errors))
    items = sorted(((p, *parse_frontmatter(p)) for p in files), key=lambda x: (x[1]['position'], x[0].name))
    items = [item for item in items if item[1]['type'] != 'module_header']
    ids = [fm['artifact_id'] for _, fm, _ in items]
    if not items or len(ids) != len(set(ids)):
        raise ValueError('Module must contain participant artifacts with unique artifact IDs')
    manifest = json.loads(manifest_path.read_text())
    state = json.loads((state_dir / course_dir.name / 'production.json').read_text()) if state_dir else None
    previous = read_baseline(baseline, course_dir.name, sprint) if baseline else None
    output.mkdir(parents=True, exist_ok=True)
    if previous:
        shutil.copytree(baseline / 'current', output / 'baseline' / 'current')
    pages = []
    for p, fm, body in items:
        source_dir = output / 'sources'
        source_dir.mkdir(exist_ok=True)
        shutil.copy2(p, source_dir / p.name)
        if fm.get('source_provenance'):
            evidence = p.parent / fm['source_provenance']
            shutil.copy2(evidence, source_dir / evidence.name)
        assets = local_image_assets(p, markdown_body_to_html(body))
        for asset in assets:
            target = source_dir / 'assets' / asset['path'].relative_to((p.parent / 'assets').resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset['path'], target)
        skipped = 'AI activity requires its delivery-specific engine preview' if is_ai_activity_delivery(fm) else None
        after = None
        if not skipped:
            result = render_hosted_artifact(p, manifest_path, output / 'current', manifest=manifest, state=state)
            after = Path(result['output_path']).relative_to(output).as_posix()
        old = next((x for x in previous['pages'] if x['id'] == fm['artifact_id']), None) if previous else None
        changes = [key for key in sorted(set(fm) | set(old['frontmatter']))
                   if fm.get(key) != old['frontmatter'].get(key)] if old else []
        pages.append({'id': fm['artifact_id'], 'slug': fm['slug'], 'title': fm['title'],
                      'type': fm['type'], 'source': str(p.relative_to(course_dir)),
                      'source_sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                      'frontmatter': fm, 'counts': word_counts(fm, body), 'after': after,
                      'before': 'baseline/' + old['after'] if old and old['after'] else None,
                      'before_counts': old['counts'] if old else None, 'metadata_changes': changes,
                      'status': 'matched' if old else ('added' if previous else 'current'),
                      'skipped': skipped, 'images': [{'source': a['source'], 'sha256': a['hash']} for a in assets]})
    removed = [x['id'] for x in previous['pages'] if x['id'] not in ids] if previous else []
    record = {'version': 1, 'course': course_dir.name, 'sprint': sprint, 'title': items[0][1]['module'],
              'pages': pages, 'removed_artifacts': removed, 'baseline': str(baseline) if baseline else None,
              'browser_status': 'not_run', 'manual_review': 'pending',
              'scope': 'Local selected-module preview; no Canvas or AI endpoint calls'}
    (output / 'current').mkdir(exist_ok=True)
    # Paths in module navigation are relative to the hosted course directory.
    nav_path = hosted_output_path(output / 'current', manifest, f'{course_dir.name}/sprint-{sprint}.html')
    links = ''.join(f'<li><a href="{html.escape(Path(x["after"]).relative_to(nav_path.parent.relative_to(output)).as_posix(), quote=True)}">{html.escape(x["title"])}</a></li>'
                    for x in pages if x['after'])
    nav = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(record["title"])}</title><h1>{html.escape(record["title"])}</h1><p>Local preview of this module only.</p><ul>{links}</ul></html>'
    nav_path.parent.mkdir(parents=True, exist_ok=True)
    nav_path.write_text(nav)
    (nav_path.parent / 'index.html').write_text(nav)
    template = (Path(__file__).parent / 'assets/module-comparison.html').read_text()
    document = template.replace('__TITLE__', html.escape(record['title'])).replace('__PAGES_JSON__', json.dumps(pages, default=str).replace('<', '\\u003c'))
    (output / 'comparison.html').write_text(document)
    (output / 'index.html').write_text(document)
    (output / 'preview.json').write_text(json.dumps(record, indent=2, default=str) + '\n')
    return record


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def check_browser(output: Path, *, node: str = 'node', playwright_module: str | None = None,
                  browser_executable: str | None = None) -> int:
    handler = partial(_QuietHandler, directory=str(output.resolve()))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    cmd = [node, str(Path(__file__).with_name('module_preview_browser.cjs')), str(output.resolve()),
           f'http://127.0.0.1:{server.server_port}']
    if playwright_module:
        cmd.extend(['--playwright-module', playwright_module])
    if browser_executable:
        cmd.extend(['--browser-executable', browser_executable])
    try:
        completed = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        (output / 'browser.log').write_text(completed.stdout + completed.stderr)
        result = completed.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        (output / 'browser.log').write_text(str(exc))
        result = 1
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
    record = json.loads((output / 'preview.json').read_text())
    record['browser_status'] = 'passed' if result == 0 else ('partial' if result == 2 else 'failed')
    if not (output / 'browser-results.json').exists():
        (output / 'browser-results.json').write_text(json.dumps({
            'status': 'failed', 'results': [], 'manual_review': 'pending',
            'error': 'Browser checker did not complete; see browser.log',
        }, indent=2) + '\n')
    (output / 'preview.json').write_text(json.dumps(record, indent=2) + '\n')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--sprint', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--check-browser', action='store_true')
    parser.add_argument('--node', default='node')
    parser.add_argument('--playwright-module')
    parser.add_argument('--browser-executable')
    args = parser.parse_args()
    try:
        result = build_preview(args.manifest, args.sprint, args.output, args.baseline, args.state_dir)
        print(f'Rendered {sum(bool(p["after"]) for p in result["pages"])} pages: {args.output.resolve() / "comparison.html"}')
        if args.check_browser:
            code = check_browser(args.output, node=args.node, playwright_module=args.playwright_module,
                                 browser_executable=args.browser_executable)
            print(f'Browser results: {args.output / "browser-results.json"}; log: {args.output / "browser.log"}')
            return code
        print('Browser checks not run. Manual editorial review remains pending.')
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f'Preview failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

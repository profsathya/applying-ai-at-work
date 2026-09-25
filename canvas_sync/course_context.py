"""Export only verified, released learner content. This module never writes Canvas."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.maintenance_state import MaintenanceState
from canvas_sync.schema import parse_frontmatter_text
from canvas_sync.state import canvas_fingerprint, fetch_canvas_state, save_json_atomic, utc_now

REPO_ROOT = Path(__file__).resolve().parent.parent


def learner_content(fm: dict, body: str) -> str:
    """Explicit allowlist: never serialize arbitrary frontmatter or feedback config."""
    parts = [body.strip()]
    guided = fm.get('guided_assignment', {})
    for key in ('purpose', 'builds_on', 'standing_instruction'):
        if guided.get(key):
            parts.append(str(guided[key]))
    for task in guided.get('tasks', []):
        parts.append(str(task['prompt']))
        parts.extend('- ' + str(x) for x in task.get('options', []))
        # Choice criteria can disclose the answer; only response criteria are exported.
        if task.get('kind', 'response') == 'response':
            parts.extend('- ' + str(x) for x in task.get('criteria', []))
    for question in fm.get('questions', []):
        parts.append(str(question['prompt']))
        parts.extend('- ' + str(a['text']) for a in question.get('answers', []))
    for question in fm.get('ai_activity', {}).get('questions', []):
        parts.append(str(question['prompt']))
    for row in fm.get('rubric', []):
        parts.append(f"- {row['description']} ({row['points']} points)")
    return '\n\n'.join(p for p in parts if p).strip() + '\n'


def published_placement(entry: dict, modules: dict, items: dict) -> tuple[dict, dict] | None:
    """Find a learner-visible placement for a manifest-backed Canvas object."""
    module_id = entry.get('canvas_module_id')
    module = modules.get(module_id)
    if not module or module.get('published') is not True:
        return None
    atype = entry.get('canvas_type')
    candidates = [i for i in items.get(module_id, []) if i.get('published') is True and
                  ((atype == 'page' and i.get('type') == 'Page' and i.get('page_url') == entry.get('canvas_page_url')) or
                   (atype != 'page' and i.get('type') == {'assignment': 'Assignment', 'discussion': 'Discussion', 'quiz': 'Quiz'}.get(atype) and i.get('content_id') == entry.get('canvas_id')))]
    if not candidates:
        return None
    return module, min(candidates, key=lambda i: i.get('position', 0))


def released_source(repo_root: Path, path: str, entry: dict) -> dict:
    """Read the exact source recorded at publication, even if a newer draft exists."""
    relative = Path(path)
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'Unsafe released source path: {path}')
    expected = entry.get('content_hash')
    if not expected:
        raise ValueError(f'Missing released source hash: {path}')
    md = repo_root / relative
    raw = md.read_bytes() if md.exists() else None
    if raw is None or hashlib.sha256(raw).hexdigest() != expected:
        commit = entry.get('source_commit', '')
        if not re.fullmatch(r'[0-9a-f]{40}', commit):
            raise ValueError(f'Unreleased local changes and no source commit: {path}')
        try:
            raw = subprocess.run(
                ['git', 'show', f'{commit}:{path}'], cwd=repo_root,
                check=True, capture_output=True,
            ).stdout
        except subprocess.CalledProcessError as error:
            raise ValueError(f'Missing recorded released source: {path}') from error
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f'Recorded source does not match released hash: {path}')
    fm, body = parse_frontmatter_text(raw.decode('utf-8'), path)
    return {'frontmatter': fm, 'body': body, 'content_hash': expected}


def build_release(*, artifacts: dict, sources: dict,
                  modules: list[dict], items: dict, objects: dict,
                  generated_at: str | None = None) -> dict:
    """Pure builder. sources maps local paths to {frontmatter, body, content_hash}.

    objects maps those paths to freshly fetched Canvas objects; items maps module
    IDs to their fresh module-item lists. Missing evidence never authorizes export.
    """
    live_modules = {m['id']: m for m in modules}
    pages = []
    seen = set()
    for path, entry in artifacts.items():
        placement = published_placement(entry, live_modules, items)
        if not placement:
            continue
        source = sources.get(path)
        if not source:
            raise ValueError(f'Missing local source for published Canvas item: {path}')
        fm = source['frontmatter']
        if fm.get('publish') is not True or fm.get('type') == 'module_header':
            raise ValueError(f'Published Canvas item is not a released local artifact: {path}')
        atype = entry['canvas_type']
        module, item = placement
        live = objects.get(path)
        if live is None:
            raise ValueError(f'Missing live object: {path}')
        if live.get('published') is not True:
            continue
        if source['content_hash'] != entry.get('content_hash'):
            raise ValueError(f'Unreleased local changes: {path}')
        if not entry.get('canvas_fingerprint') or canvas_fingerprint(live, atype) != entry['canvas_fingerprint']:
            raise ValueError(f'Canvas drift or missing fingerprint: {path}')
        identity = (atype, entry.get('canvas_page_url') if atype == 'page' else entry.get('canvas_id'))
        if identity in seen:
            continue
        seen.add(identity)
        hosted = entry.get('hosted_path', '')
        # Deployment hosted paths start with the course directory.
        relative = hosted.split('/', 1)[1] if '/' in hosted else ''
        if not relative or '..' in Path(relative).parts or Path(relative).is_absolute():
            raise ValueError(f'Missing or unsafe hosted path: {path}')
        url = live.get('html_url') or entry.get('hosted_url')
        if not url or not url.startswith('https://'):
            raise ValueError(f'Missing source URL: {path}')
        pages.append(((module.get('position', 0), item.get('position', 0), path), {
            'path': relative, 'title': fm['title'], 'source_url': url,
            'content': learner_content(fm, source['body']),
        }))
    result = [p for _, p in sorted(pages, key=lambda p: p[0])]
    if not result:
        raise ValueError('No verified published course content; refusing empty export')
    digest = hashlib.sha256(json.dumps(result, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()).hexdigest()
    return {'schema_version': 1, 'release_id': digest, 'generated_at': generated_at or utc_now(), 'pages': result}


def export_release(manifest_path: Path, state_dir: Path | None = None, *, repo_root: Path = REPO_ROOT, client=None) -> dict:
    manifest = MaintenanceState(manifest_path, repo_root, state_dir).load()
    check_instance_ready(manifest, manifest_label=str(manifest_path))
    check_env_matches_instance(manifest, manifest_label=str(manifest_path))
    client = client or CanvasClient.from_env(course_id=manifest['instance']['course_id'])
    modules = client.list_modules()
    items = {m['id']: client.list_module_items(m['id']) for m in modules}
    live_modules = {m['id']: m for m in modules}
    sources, objects = {}, {}
    for path, entry in manifest['artifacts'].items():
        if entry.get('canvas_type') == 'module_header' or not published_placement(entry, live_modules, items):
            continue
        source = released_source(repo_root, path, entry)
        sources[path] = source
        if source['frontmatter'].get('publish') is True:
            objects[path] = fetch_canvas_state(client, entry)
    return build_release(artifacts=manifest['artifacts'], sources=sources, modules=modules, items=items, objects=objects)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--state-dir', type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    load_dotenv(REPO_ROOT / '.env')
    release = export_release(args.manifest.resolve(), args.state_dir)
    save_json_atomic(args.output, release)
    print(f"Exported {len(release['pages'])} verified published pages")


if __name__ == '__main__':
    main()

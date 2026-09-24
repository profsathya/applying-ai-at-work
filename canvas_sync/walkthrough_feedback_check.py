"""Validate approved checkpoints, optionally exercise the deployed feedback service.

Live checks use explicitly supplied synthetic responses, never browser drafts.
They do not retry failed requests or write to Canvas.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / 'services/course-ai/netlify/functions/walkthrough-guidance.json'


def enabled_checkpoints(frontmatter: dict) -> list[str]:
    config = frontmatter.get('guided_assignment') or {}
    if config.get('presentation') != 'walkthrough' or not config.get('feedback_endpoint'):
        return []
    return [task['id'] for task in config.get('tasks', []) if isinstance(task, dict)
            and isinstance(task.get('id'), str) and not task.get('read_only')
            and task.get('feedback_enabled', True)]


def check_registration(frontmatter: dict, registry_path: Path = REGISTRY) -> list[str]:
    checkpoints = enabled_checkpoints(frontmatter)
    if not checkpoints:
        return []
    try:
        registry = json.loads(registry_path.read_text())
    except (OSError, ValueError) as exc:
        return [f'Cannot read walkthrough feedback registry: {exc}']
    if not isinstance(registry, dict):
        return ['Walkthrough feedback registry must be an object']
    entry = registry.get(frontmatter.get('artifact_id'))
    if not isinstance(entry, dict) or not all(isinstance(entry.get(key), str) and entry[key].strip()
                                             for key in ('title', 'rule')):
        return ['Walkthrough feedback needs a reviewed activity title and rule in the server registry']
    registered = entry.get('checkpoints', {})
    if not isinstance(registered, dict):
        return ['Walkthrough feedback checkpoints must be an object']
    return [f'Walkthrough feedback checkpoint {checkpoint!r} has no server-approved criteria'
            for checkpoint in checkpoints if not isinstance(registered.get(checkpoint), str)
            or not registered[checkpoint].strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--live', action='store_true', help='Make one real provider request per enabled checkpoint')
    parser.add_argument('--samples', type=Path, help='JSON mapping checkpoint IDs to synthetic participant responses')
    parser.add_argument('--origin', default='https://profsathya.github.io')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(ROOT))
    from canvas_sync.schema import parse_frontmatter
    fm, _ = parse_frontmatter(args.artifact)
    errors = check_registration(fm)
    checks = []
    ids = enabled_checkpoints(fm)
    if args.live and not errors:
        if not args.samples or not args.output:
            parser.error('--live requires --samples and --output to retain test evidence')
        samples = json.loads(args.samples.read_text())
        if set(samples) != set(ids) or any(not isinstance(value, str) or not value.strip() for value in samples.values()):
            parser.error('Supply exactly one nonempty synthetic response for every enabled checkpoint')
        import requests
        for checkpoint in ids:
            result = {'checkpoint': checkpoint}
            try:
                response = requests.post(fm['guided_assignment']['feedback_endpoint'],
                    headers={'Origin': args.origin}, timeout=55,
                    json={'activity': fm['artifact_id'], 'checkpoint': checkpoint, 'response': samples[checkpoint]})
                result.update(status=response.status_code, response=response.json())
                result['passed'] = response.ok and isinstance(result['response'].get('content'), str) and bool(result['response']['content'].strip())
            except (requests.RequestException, ValueError) as exc:
                result.update(passed=False, error=str(exc))
            checks.append(result)
            print(f'{checkpoint}: {"PASS" if result["passed"] else "FAIL"}', flush=True)
        errors.extend(f'{check["checkpoint"]}: live feedback failed' for check in checks if not check['passed'])
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'artifact_id': fm['artifact_id'],
              'artifact_sha256': hashlib.sha256(args.artifact.read_bytes()).hexdigest(),
              'registry_sha256': hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),
              'registered_checkpoints': ids, 'live_requested': args.live, 'live_checks': checks, 'errors': errors}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'registered_checkpoints': ids, 'errors': errors}))
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())

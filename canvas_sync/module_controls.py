"""Resolve source-owned module prerequisites and release times safely."""

from datetime import datetime


def module_control_payload(frontmatter, artifacts, modules, module_id):
    payload = {}
    if 'require_sequential_progress' in frontmatter:
        payload['require_sequential_progress'] = frontmatter['require_sequential_progress']
    if 'module_unlock_at' in frontmatter:
        payload['unlock_at'] = frontmatter['module_unlock_at']
    if 'prerequisite_modules' in frontmatter:
        current = next((m for m in modules if int(m['id']) == int(module_id)), None)
        if current is None:
            raise ValueError('Selected module is missing from Canvas')
        prerequisites = []
        for artifact_id in frontmatter['prerequisite_modules']:
            matches = [entry for key, entry in artifacts.items()
                       if key == artifact_id or entry.get('artifact_id') == artifact_id]
            if len(matches) != 1 or matches[0].get('canvas_type') != 'module_header':
                raise ValueError(f'Prerequisite {artifact_id} must resolve to one module header')
            prerequisite_id = matches[0].get('canvas_module_id')
            prerequisite = next((m for m in modules if m['id'] == prerequisite_id), None)
            if (prerequisite is None or not prerequisite.get('published')
                    or prerequisite['position'] >= current['position']):
                raise ValueError(f'Prerequisite {artifact_id} must be a published preceding module')
            prerequisites.append(prerequisite_id)
        payload['prerequisite_module_ids'] = prerequisites
    return payload


def verify_module_controls(module, payload):
    for key, desired in payload.items():
        actual = module.get(key)
        if key == 'unlock_at' and desired is not None and actual is not None:
            same = (datetime.fromisoformat(actual.replace('Z', '+00:00'))
                    == datetime.fromisoformat(desired.replace('Z', '+00:00')))
        elif key == 'prerequisite_module_ids':
            same = sorted(actual or []) == sorted(desired)
        else:
            same = actual == desired
        if not same:
            raise ValueError(f"Module {module['id']}: Canvas did not confirm {key}")

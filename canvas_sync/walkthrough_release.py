"""Preflight and rollback for a reviewed Canvas walk-through replacement."""
from __future__ import annotations

from pathlib import Path
from yaml import YAMLError

from canvas_sync.schema import parse_frontmatter
from canvas_sync.state import canvas_fingerprint, fetch_canvas_state, load_json, save_json_atomic


ASSESSMENT_KEYS = (
    'points_possible', 'submission_types', 'due_at', 'unlock_at', 'lock_at',
    'grading_type', 'omit_from_final_grade', 'assignment_group_id',
    'allowed_extensions', 'only_visible_to_overrides', 'peer_reviews',
    'automatic_peer_reviews', 'anonymous_peer_reviews', 'use_rubric_for_grading',
    'rubric_settings', 'hide_in_gradebook', 'moderated_grading',
    'allowed_attempts', 'post_manually',
)


def _rubric_shape(value: object) -> object:
    if not isinstance(value, list):
        return value
    return [{
        'description': criterion.get('description'), 'long_description': criterion.get('long_description'),
        'points': criterion.get('points'),
        'ratings': [{'description': rating.get('description'), 'points': rating.get('points')}
                    for rating in criterion.get('ratings', [])],
    } for criterion in value if isinstance(criterion, dict)]


def _override_shape(value: list[dict]) -> list[dict]:
    keep = ('title', 'due_at', 'unlock_at', 'lock_at', 'student_ids', 'group_id', 'course_section_id')
    return sorted(({key: entry.get(key) for key in keep if entry.get(key) is not None} for entry in value),
                  key=lambda entry: str(sorted(entry.items())))


def release_pairs(changed: list[dict], course_paths: list[Path]) -> list[tuple[dict, dict]]:
    """Find a coordinated source/new publish flip in the selected changes."""
    all_fm = {}
    for path in course_paths:
        try:
            fm, _ = parse_frontmatter(path)
        except (ValueError, YAMLError):
            continue  # The existing publisher reports invalid neighbors per artifact.
        all_fm[fm['artifact_id']] = fm
    changed_by_id = {item['artifact_id']: item for item in changed}
    pairs = []
    claimed = set()
    for item in changed:
        fm = all_fm[item['artifact_id']]
        source_id = fm.get('walkthrough_after')
        if not source_id or not fm.get('publish', True):
            continue
        source = all_fm.get(source_id)
        if not source:
            raise ValueError(f"Walk-through {item['artifact_id']}: source {source_id} is missing")
        if source.get('publish', True):
            raise ValueError(f"Walk-through {item['artifact_id']}: release requires source publish: false")
        source_item = changed_by_id.get(source_id)
        if not source_item:
            raise ValueError(f"Walk-through {item['artifact_id']}: release requires changed source {source_id} in the same batch")
        if source_id in claimed:
            raise ValueError(f'Walk-through source {source_id}: release has more than one replacement')
        claimed.add(source_id)
        pairs.append((source_item, item))
    for item in changed:
        fm = all_fm[item['artifact_id']]
        if fm.get('publish', True) is not False or item['artifact_id'] in claimed:
            continue
        replacements = [new for new in all_fm.values() if new.get('walkthrough_after') == item['artifact_id']]
        if replacements and any(new.get('publish', True) for new in replacements):
            raise ValueError(f"Source {item['artifact_id']}: publish flip must include its replacement in the same batch")
    return pairs


def _has_submissions(client, assignment_id: int) -> bool:
    submissions = client.list_assignment_submissions(assignment_id)
    return any(entry.get('submitted_at') or entry.get('workflow_state') in
               ('submitted', 'graded', 'pending_review') for entry in submissions)


def assert_source_has_no_submissions(client, source_entry: dict) -> None:
    if source_entry['canvas_type'] == 'assignment' and _has_submissions(client, int(source_entry['canvas_id'])):
        raise ValueError(f"{source_entry['artifact_id']}: a submission appeared before unpublishing")


def preflight_pair(client, source_item: dict, new_item: dict, state: dict) -> dict:
    """Read live Canvas once more before a release; raise without writing."""
    source_fm, _ = parse_frontmatter(source_item['path'])
    new_fm, _ = parse_frontmatter(new_item['path'])
    entries = state.get('artifacts', {})
    source_entry, new_entry = entries.get(source_item['artifact_id']), entries.get(new_item['artifact_id'])
    if not source_entry or not new_entry or not new_entry.get('canvas_id'):
        raise ValueError(f"{new_item['artifact_id']}: both Canvas items must be staged in deployment state")
    if source_entry.get('canvas_type') not in ('assignment', 'page'):
        raise ValueError(f"{source_item['artifact_id']}: release supports an assignment or page source")
    if new_entry.get('canvas_type') != 'assignment':
        raise ValueError(f"{new_item['artifact_id']}: replacement must be a Canvas assignment")
    source_live = fetch_canvas_state(client, source_entry)
    new_live = client.get_assignment(int(new_entry['canvas_id']), include=['overrides', 'all_dates'])
    if not source_live or not new_live:
        raise ValueError(f"{source_item['artifact_id']} / {new_item['artifact_id']}: Canvas item is missing")
    if source_live.get('published') is not True or new_live.get('published') is not False:
        raise ValueError(f"{source_item['artifact_id']} / {new_item['artifact_id']}: expected published source and unpublished replacement")
    source_module = source_entry.get('canvas_module_id')
    source_module_item = source_entry.get('canvas_module_item_id')
    new_module = new_entry.get('canvas_module_id')
    new_module_item = new_entry.get('canvas_module_item_id')
    if not all((source_module, source_module_item, new_module, new_module_item)) or source_module != new_module:
        raise ValueError(f"{new_item['artifact_id']}: source and replacement must have module items in the same module")
    ordered = [int(entry['id']) for entry in sorted(client.list_module_items(int(source_module)), key=lambda entry: entry['position'])]
    if int(source_module_item) not in ordered or ordered.index(int(source_module_item)) + 1 >= len(ordered) or ordered[ordered.index(int(source_module_item)) + 1] != int(new_module_item):
        raise ValueError(f"{new_item['artifact_id']}: replacement is not directly below its source")
    items_by_id = {int(item['id']): item for item in client.list_module_items(int(source_module))}
    if items_by_id[int(source_module_item)].get('published') is not True or items_by_id[int(new_module_item)].get('published') is not False:
        raise ValueError(f"{new_item['artifact_id']}: expected published source and unpublished replacement module items")
    if source_entry['canvas_type'] == 'assignment':
        assert_source_has_no_submissions(client, source_entry)
        source_live = client.get_assignment(int(source_entry['canvas_id']), include=['overrides', 'all_dates'])
        mismatches = [key for key in ASSESSMENT_KEYS if source_live.get(key) != new_live.get(key)]
        if _rubric_shape(source_live.get('rubric')) != _rubric_shape(new_live.get('rubric')):
            mismatches.append('rubric')
        old_overrides = client.list_assignment_overrides(int(source_entry['canvas_id']))
        new_overrides = client.list_assignment_overrides(int(new_entry['canvas_id']))
        if _override_shape(old_overrides) != _override_shape(new_overrides):
            mismatches.append('assignment overrides')
        if mismatches:
            raise ValueError(f"{new_item['artifact_id']}: assessment settings differ from source: {', '.join(mismatches)}")
        if source_fm.get('points') != new_fm.get('points') or source_fm.get('submission_type') != new_fm.get('submission_type'):
            raise ValueError(f"{new_item['artifact_id']}: local points or submission type differ from source")
    elif new_fm.get('points') != 0:
        raise ValueError(f"{new_item['artifact_id']}: page replacement must be ungraded")
    return {'source': source_entry, 'replacement': new_entry, 'module_order': ordered}


def _set_published(client, entry: dict, published: bool) -> None:
    if entry['canvas_type'] == 'assignment':
        client.update_assignment(int(entry['canvas_id']), {'published': published})
    elif entry['canvas_type'] == 'page':
        client.update_page(entry['canvas_page_url'], {'published': published})
    else:
        raise ValueError(f"Unsupported source type {entry['canvas_type']}")
    live = fetch_canvas_state(client, entry)
    if not live or live.get('published') is not published:
        raise ValueError(f"Canvas did not confirm {'published' if published else 'unpublished'} state")
    module_id, item_id = entry.get('canvas_module_id'), entry.get('canvas_module_item_id')
    if module_id and item_id:
        client.update_module_item(int(module_id), int(item_id), {'published': published})
        item = next((item for item in client.list_module_items(int(module_id)) if int(item['id']) == int(item_id)), None)
        if not item or item.get('published') is not published:
            raise ValueError(f"Canvas did not confirm {'published' if published else 'unpublished'} module item")


def rollback_pair(client, pair_state: dict, state_path: Path) -> list[str]:
    """Restore published source and unpublished replacement, then invalidate hashes."""
    failures = []
    for entry, published in ((pair_state['source'], True), (pair_state['replacement'], False)):
        try:
            _set_published(client, entry, published)
        except Exception as exc:  # noqa: BLE001 - attempt the other restoration too
            failures.append(f"{entry.get('artifact_id')}: {exc}")
    state = load_json(state_path)
    for entry in (pair_state['source'], pair_state['replacement']):
        artifact_id = entry['artifact_id']
        current = state.get('artifacts', {}).get(artifact_id)
        if current:
            live = fetch_canvas_state(client, current)
            current['canvas_fingerprint'] = canvas_fingerprint(live, current['canvas_type'])
            current['content_hash'] = ''  # A retry must not accept the release as already synced.
    save_json_atomic(state_path, state)
    return failures


def verify_walkthrough_adjacency(client, course_paths: list[Path], state: dict) -> list[str]:
    """Verify every staged or released replacement remains under its source."""
    artifacts = state.get('artifacts', {})
    checked = []
    for path in course_paths:
        fm, _ = parse_frontmatter(path)
        source_id = fm.get('walkthrough_after')
        if not source_id:
            continue
        new_entry, source_entry = artifacts.get(fm['artifact_id']), artifacts.get(source_id)
        if not new_entry or not new_entry.get('canvas_module_item_id'):
            continue  # Local only; nothing to verify in Canvas yet.
        if not source_entry or source_entry.get('canvas_module_id') != new_entry.get('canvas_module_id'):
            raise ValueError(f"{fm['artifact_id']}: source or module is missing from deployment state")
        ordered = [int(item['id']) for item in sorted(
            client.list_module_items(int(source_entry['canvas_module_id'])), key=lambda item: item['position'])]
        source_item, new_item = int(source_entry['canvas_module_item_id']), int(new_entry['canvas_module_item_id'])
        if source_item not in ordered or ordered.index(source_item) + 1 >= len(ordered) or ordered[ordered.index(source_item) + 1] != new_item:
            raise ValueError(f"{fm['artifact_id']}: Canvas item is not directly below source {source_id}")
        checked.append(fm['artifact_id'])
    return checked

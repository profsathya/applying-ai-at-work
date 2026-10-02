"""Recoverably replace an empty concept assignment's placement with a practice page.

No assignment or page object is deleted. Checkpoints belong to deployment state,
so an interrupted conversion can adopt its already-created page and placement.
"""

from copy import deepcopy


def convert_empty_assignment(client, frontmatter, entry, body, save_checkpoint):
    if entry.get('canvas_type') == 'page':
        return entry
    if (entry.get('canvas_type') != 'assignment' or frontmatter.get('type') != 'page'
            or frontmatter.get('delivery_mode') != 'guided_assignment'
            or 'concept check' not in frontmatter.get('title', '').lower()
            or frontmatter.get('submission_type') != 'none'):
        raise ValueError('Only an explicitly configured concept-check assignment can become a practice page')
    assignment_id = entry['canvas_id']
    assignment = client.get_assignment(assignment_id)
    submissions = client.list_assignment_submissions(assignment_id)
    if assignment.get('has_submitted_submissions') or any(
            s.get('submitted_at') or s.get('workflow_state') not in (None, 'unsubmitted')
            for s in submissions):
        raise ValueError('Concept assignment has submitted work; conversion is blocked')
    module_id, old_item_id = entry['canvas_module_id'], entry['canvas_module_item_id']
    checkpoint = deepcopy(entry.get('page_conversion') or {})
    placements = [(m['id'], i) for m in client.list_modules()
                  for i in client.list_module_items(m['id'])
                  if i.get('type') == 'Assignment' and i.get('content_id') == assignment_id]
    if not checkpoint.get('old_placement_removed'):
        if len(placements) != 1 or placements[0][0] != module_id or placements[0][1]['id'] != old_item_id:
            raise ValueError('Original concept assignment placement is missing, moved, or ambiguous')
        old_item = placements[0][1]
        if old_item.get('published') is not frontmatter.get('publish', True):
            raise ValueError('Concept-check publication changed; reconcile before converting')
        checkpoint.setdefault('position', old_item['position'])
    elif placements:
        raise ValueError('A retired concept assignment has a new placement; reconcile before resuming')
    checkpoint.setdefault('previous_assignment', {k: assignment.get(k) for k in (
        'id', 'published', 'points_possible', 'grading_type', 'submission_types', 'omit_from_final_grade')})

    def persist():
        entry['page_conversion'] = deepcopy(checkpoint)
        save_checkpoint(deepcopy(entry))

    if not checkpoint.get('page_url'):
        page = client.create_page({'title': frontmatter['title'], 'body': body, 'published': False})
        checkpoint.update(page_id=page['page_id'], page_url=page['url'])
        persist()
    if not checkpoint.get('item_id'):
        requirement = None if frontmatter.get('publish') is False else {'type': 'must_view'}
        item = client.add_module_item(module_id, title=frontmatter['title'], content_type='Page',
                                     page_url=checkpoint['page_url'], position=checkpoint['position'],
                                     completion_requirement=requirement)
        checkpoint['item_id'] = item['id']
        persist()
    if not checkpoint.get('old_placement_removed'):
        retired = client.update_assignment(assignment_id, {'published': False, 'points_possible': 0,
                                                          'submission_types': ['not_graded'],
                                                          'omit_from_final_grade': True})
        if (retired.get('published') is not False or retired.get('points_possible') != 0
                or retired.get('submission_types') != ['not_graded']
                or retired.get('omit_from_final_grade') is not True):
            raise ValueError('Canvas did not confirm the original concept shell as inactive and ungraded')
        client.delete_module_item(module_id, old_item_id)
        checkpoint['old_placement_removed'] = True
        persist()
    page = client.update_page(checkpoint['page_url'], {'published': frontmatter.get('publish', True)})
    if page.get('published') is not frontmatter.get('publish', True):
        raise ValueError('Canvas did not confirm the practice page publication state')
    result = {**entry, 'canvas_type': 'page', 'source_type': 'page',
              'canvas_id': checkpoint['page_id'], 'canvas_page_url': checkpoint['page_url'],
              'canvas_module_item_id': checkpoint['item_id'], 'content_hash': '0' * 64,
              'retired_assignment': checkpoint['previous_assignment']}
    result.pop('page_conversion', None)
    result.pop('canvas_payload_hash', None)
    result.pop('canvas_fingerprint', None)
    if frontmatter.get('publish') is False:
        result.pop('completion_requirement', None)
    else:
        result['completion_requirement'] = 'must_view'
    save_checkpoint(deepcopy(result))
    return result

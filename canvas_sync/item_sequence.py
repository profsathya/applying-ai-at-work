"""Sprint positions, independent of learner completion and storage directories."""
from __future__ import annotations

import re


def sequence_label(position: tuple[int, int] | None) -> str:
    if position is None:
        return ''
    index, total = position
    if not 1 <= index <= total:
        raise ValueError('Invalid sprint item position')
    remaining = total - index
    return f'Item {index} of {total} · {remaining} {"item" if remaining == 1 else "items"} remaining'


def sequence_line(position: tuple[int, int] | None) -> str:
    label = sequence_label(position)
    return (f'<p class="item-sequence" style="color: #526175; font-size: 0.9rem; '
            f'line-height: 1.5; margin: 0.5rem 0 1rem;">{label}</p>') if label else ''


def update_sequence_line(document: str, position: tuple[int, int] | None) -> str:
    """Refresh only the heading annotation, preserving already released content."""
    document = re.sub(r'\n?\s*<p class="item-sequence"[^>]*>[^<]*</p>', '', document)
    line = sequence_line(position)
    return re.sub(r'(</h1>)', lambda match: match[0] + '\n    ' + line,
                  document, count=1) if line else document


def live_sequences(modules: list[dict], items: dict, *, hidden_modules=()) -> dict:
    """Map module-item IDs to dense positions in published learner-facing order.

    Canvas positions can be sparse. Optional items count; unpublished items and
    structural subheaders do not. No learner completion data is requested.
    """
    result = {}
    for module in modules:
        if module.get('published') is not True or module.get('name') in hidden_modules:
            continue
        visible = sorted((item for item in items.get(module['id'], [])
                          if item.get('published') is True and item.get('type') in
                          {'Page', 'Assignment', 'Quiz', 'Discussion', 'ExternalUrl', 'ExternalTool'}),
                         key=lambda item: (item['position'], item['id']))
        for index, item in enumerate(visible, 1):
            result[item['id']] = (index, len(visible))
    return result


def source_sequences(items: list[tuple], *, hidden_modules=()) -> dict:
    """Deterministic preview of intended publication, grouped by actual module.

    Walkthroughs can be stored in another sprint directory. Their anchor sets
    their place even when the original is retired in this release.
    """
    by_id = {fm['artifact_id']: fm for _, fm in items if fm.get('artifact_id')}
    modules = {}
    for _, fm in items:
        if (not fm.get('publish', True) or fm.get('type') == 'module_header'
                or fm.get('module') in hidden_modules):
            continue
        anchor = by_id.get(fm.get('walkthrough_after'))
        order = (anchor or fm).get('position', 9999)
        modules.setdefault(fm['module'], []).append((order, bool(anchor), fm['artifact_id']))
    return {artifact_id: (index, len(rows)) for rows in modules.values()
            for index, (_, _, artifact_id) in enumerate(sorted(rows), 1)}

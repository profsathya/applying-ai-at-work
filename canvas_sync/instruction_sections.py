"""Resolve guided-task teaching references against rendered Markdown h2 sections."""
from __future__ import annotations

from html.parser import HTMLParser


class _SectionHeadings(HTMLParser):
    """Find top-level h2 boundaries without treating code or blockquotes as sections."""

    VOID_TAGS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self, rendered):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.headings = []
        self.current = None
        self.offsets = [0]
        for line in rendered.splitlines(keepends=True):
            self.offsets.append(self.offsets[-1] + len(line))

    def handle_starttag(self, tag, attrs):
        if tag == 'h2' and not self.stack:
            line, column = self.getpos()
            self.current = [self.offsets[line - 1] + column, []]
        if tag not in self.VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        if tag == 'h2' and self.current is not None:
            start, text = self.current
            self.headings.append((start, ''.join(text).strip()))
            self.current = None
        if tag in self.stack:
            del self.stack[len(self.stack) - 1 - self.stack[::-1].index(tag):]

    def handle_data(self, data):
        if self.current is not None:
            self.current[1].append(data)


def partition_instruction_sections(rendered: str, tasks: list[dict]) -> tuple[str, dict[str, str]]:
    """Return unmatched introductory teaching and sections keyed by task ID.

    References are exact visible level-two heading titles (inline emphasis is okay).
    A section includes subsequent content through the next h2. Referenced sections
    move to task order; unmatched content remains visible before the tasks.
    """
    references = [task['instruction_section'] for task in tasks if 'instruction_section' in task]
    if not references:
        return rendered, {}
    if any(not isinstance(ref, str) or not ref.strip() for ref in references):
        raise ValueError('instruction_section must be a nonempty heading title')
    if len(set(references)) != len(references):
        raise ValueError('Each instruction_section may be referenced by only one task')
    parser = _SectionHeadings(rendered)
    parser.feed(rendered)
    headings = parser.headings
    sections = {}
    remainder = [rendered[:headings[0][0]]] if headings else [rendered]
    for index, (start, title) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(rendered)
        section = rendered[start:end]
        if title in references:
            sections.setdefault(title, []).append(section)
        else:
            remainder.append(section)
    for ref in references:
        if len(sections.get(ref, [])) != 1:
            raise ValueError(f'instruction_section {ref!r} must match exactly one level-two Markdown heading')
    return ''.join(remainder).strip(), {
        task['id']: sections[task['instruction_section']][0]
        for task in tasks if 'instruction_section' in task
    }

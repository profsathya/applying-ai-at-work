"""Keep orientation handoffs as prose without losing useful course references."""
from collections import Counter
from pathlib import Path
import re
import unittest

from canvas_sync.hosted_html import markdown_body_to_html


ORIENTATION = Path(__file__).resolve().parents[1] / 'course1/sprints/sprint-6'
PREFIX = 'course1-sprints-welcome-and-orientation-v2-'
LINK = re.compile(r'\[([^]]+)\]\(artifact:([^)]+)\)')


class OrientationNavigationTests(unittest.TestCase):
    def test_sequential_handoffs_render_as_text(self):
        expected = {
            'start-here-v2': ['Welcome'],
            'welcome-v2': ['How This Course Works'],
            'how-this-course-works-v2': ['Your First Week'],
            'your-first-week-v2': [
                'Set up your AI Dojo', 'Help and Resources',
                'Sprint 1: Find the Problem Worth Solving',
            ],
            'set-up-your-ai-dojo-v2': ['Introduction Post'],
            'introduction-post-v2': [
                'Help and Resources', 'Sprint 1: Find the Problem Worth Solving',
            ],
            'help-and-resources-v2': ['Sprint 1: Find the Problem Worth Solving'],
        }
        for slug, names in expected.items():
            with self.subTest(slug=slug):
                lines = (ORIENTATION / f'{slug}.md').read_text().splitlines()
                handoffs = '\n\n'.join(line for line in lines if line.startswith((
                    'Continue to ', 'After the Dojo setup',
                    'When you have finished orientation',
                )))
                rendered = markdown_body_to_html(handoffs)
                self.assertNotIn('<a ', rendered)
                for name in names:
                    self.assertIn(name, rendered)

    def test_checklist_help_and_submission_references_remain(self):
        expected = {
            'start-here-v2': ['welcome-v2', 'how-this-course-works-v2',
                              'your-first-week-v2', 'set-up-your-ai-dojo-v2',
                              'introduction-post-v2', 'help-and-resources-v2'],
            'your-first-week-v2': ['welcome-v2', 'how-this-course-works-v2',
                                   'introduction-post-v2'],
            'how-this-course-works-v2': ['help-and-resources-v2'],
            'help-and-resources-v2': ['set-up-your-ai-dojo-v2'],
            'welcome-and-orientation-v2': ['start-here-v2', 'help-and-resources-v2'],
        }
        for path in ORIENTATION.glob('*.md'):
            with self.subTest(page=path.name):
                actual = Counter(target for _, target in LINK.findall(path.read_text()))
                self.assertEqual(actual, Counter(PREFIX + slug for slug in expected.get(path.stem, [])))

import unittest
from pathlib import Path
from canvas_sync.hosted_html import _module_backlink
from canvas_sync.schema import parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]

class ModuleBacklinkTests(unittest.TestCase):
    def test_stored_sprint16_walkthroughs_return_to_actual_sprint3_directory(self):
        for slug in ("stakeholder-map", "stakeholder-conversation"):
            fm, _ = parse_frontmatter(ROOT / f"course1/sprints/sprint-16/{slug}-canvas-walkthrough.md")
            html = '<a class="back-link" href="../sprint-16.html?context=web">Back</a><a href="../sprint-16.html?context=web">Authored reference</a>'
            result = _module_backlink(html, ROOT / "course1/manifests/production.json", fm)
            self.assertIn('class="back-link" href="../sprint-15.html?context=web"', result)
            self.assertIn('<a href="../sprint-16.html?context=web">Authored reference</a>', result)

if __name__ == "__main__":
    unittest.main()

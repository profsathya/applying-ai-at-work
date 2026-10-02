"""Portable hosted navigation must not change learning or submission controls."""
import json
from pathlib import Path
import tempfile
import unittest
from canvas_sync.native_canvas import apply_native_canvas
from canvas_sync.hosted_html import render_hosted_files
from tests.test_hosted_html import write_manifest, write_page, write_ai_discussion

NATIVE = {'hosted_html': {'native_canvas_navigation': True}}

class NativeCanvasTests(unittest.TestCase):
    def test_only_navigation_is_removed(self):
        controls = '<textarea id="answer"></textarea><button id="walk-download">Download as Word document</button><a href="https://docs.google.com/document/d/template/copy">Template</a><script>saveDraft();</script><p>Attach your Week 7 Word file and select Submit Assignment.</p>'
        old = '<html><head></head><body>' + controls + '<a hidden data-canvas-only data-canvas-href="https://cti-courses.instructure.com/courses/180/assignments/1">Open the Canvas assignment</a><a href="help.html" data-canvas-href="https://cti-courses.instructure.com/courses/180/pages/help">Help</a></body></html>'
        new = apply_native_canvas(old, NATIVE)
        self.assertIn(controls, new)
        self.assertIn('<a href="help.html">Help</a>', new)
        self.assertNotIn('cti-courses', new)
        self.assertNotIn('Open the Canvas assignment', new)
        self.assertNotIn('Submit work in the Canvas activity', new)
        self.assertNotIn('native-canvas-notice', new)
        self.assertIn('html.native-canvas-context .back-link', new)
        self.assertEqual(apply_native_canvas(new, NATIVE), new)
        self.assertEqual(apply_native_canvas(old, {}), old)

    def test_real_renderer_removes_progress_but_keeps_ai_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / 'course1/manifests/production.json'
            regular = root / 'course1/sprints/sprint-99/tuple-overview.md'
            ai = root / 'course1/sprints/sprint-99/ai-discussion.md'
            write_manifest(manifest); write_page(regular); write_ai_discussion(ai)
            render_hosted_files(manifest, root/'old', [regular, ai])
            data = json.loads(manifest.read_text())
            data['hosted_html']['native_canvas_navigation'] = True
            manifest.write_text(json.dumps(data))
            render_hosted_files(manifest, root/'new', [regular, ai])
            for old in (root/'old').rglob('*'):
                if not old.is_file(): continue
                new = root/'new'/old.relative_to(root/'old')
                if old.suffix == '.html':
                    text = new.read_text()
                    self.assertIn('data-native-canvas-navigation', text)
                    self.assertNotIn('var progressEndpoint', text)
                    self.assertNotIn('class="progress-check"', text)
                    self.assertNotIn('data-canvas-href=', text)
                else:
                    self.assertEqual(old.read_bytes(), new.read_bytes())

    def test_schedule_preserves_deployment_navigation_without_progress(self):
        config = {'help': {'web': 'help.html', 'canvas': 'CTI'}, 'orientation': {'canvas_href':'CTI'}, 'sprints':[{'canvas_href':'CTI'}]}
        old = '<html><head></head><body><script id="course-schedule" type="application/json">'+json.dumps(config)+'</script></body></html>'
        new = apply_native_canvas(old, NATIVE)
        self.assertIn('CTI', new)
        self.assertIn('"native_completion": true', new)
        self.assertIn('help.html', new)

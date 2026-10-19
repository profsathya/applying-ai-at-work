import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from canvas_sync.course_mirror import mirror_url, render, validate_config
from canvas_sync.mirror_native import CourseApi, mirrored_body, plan

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "tests/fixtures/course-mirror.json"


class CourseMirrorTests(unittest.TestCase):
    def setUp(self):
        self.config = json.loads(CONFIG.read_text())

    def test_rejects_credentials_cross_origin_and_path_traversal(self):
        for key, value in [("sharedBaseUrl", "https://user:secret@example.org/course/"),
                           ("mirrorBaseUrl", "https://other.example.org/mirror/"),
                           ("pages", ["../course2/home.html"])]:
            config = copy.deepcopy(self.config)
            config[key] = value
            with self.assertRaises(ValueError): validate_config(config)
        config = dict(self.config, token="must-never-be-published")
        with self.assertRaises(ValueError): validate_config(config)

    def test_canvas_iframe_and_old_bookmarks_share_the_live_adapter(self):
        expected = mirror_url(self.config, "home.html")
        body = '<div><iframe title="Home" src="' + self.config['sharedBaseUrl'] + 'home.html?context=canvas"></iframe></div>'
        self.assertIn(expected.replace('&', '&amp;'), mirrored_body(body, self.config))
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            render(self.config, base/'adapter', legacy_dir=base/'old')
            old = (base/'old/home.html').read_text()
            self.assertIn('location.replace', old)
            self.assertNotIn('Find the problem worth solving', old)
            self.assertEqual(json.loads((base/'adapter/config.json').read_text()), self.config)
            self.assertIn('cache: "no-store"', (base/'adapter/course-mirror.js').read_text())
        with self.assertRaises(ValueError): mirror_url(self.config, 'unmapped.html')

    def test_existing_ids_context_and_unmapped_ids_in_runtime(self):
        code = r'''
const assert = require('node:assert/strict');
const runtime = require(process.argv[1]);
const cfg = JSON.parse(require('node:fs').readFileSync(process.argv[2]));
assert.equal(runtime.canvasLink(cfg.sourceCanvasUrl+'/modules/items/3', cfg), cfg.destinationCanvasUrl+'/modules/items/103');
assert.equal(runtime.canvasLink(cfg.sourceCanvasUrl+'/assignments/2?module_item_id=3', cfg), cfg.destinationCanvasUrl+'/assignments/102?module_item_id=103');
assert.equal(runtime.remapText(cfg.sourceCanvasUrl+'/assignments/2?module_item_id=3&amp;other=2', cfg), cfg.destinationCanvasUrl+'/assignments/102?module_item_id=103&amp;other=2');
assert.throws(() => runtime.canvasLink(cfg.sourceCanvasUrl+'/assignments/999999', cfg));
assert.throws(() => runtime.remapText(cfg.sourceCanvasUrl+'/unknown/5', cfg));
assert.equal(new URL(runtime.hostedLink('#part-1', cfg.sharedBaseUrl+'home.html', cfg, 'canvas')).hash, '#part-1');
assert.equal(new URL(runtime.hostedLink('#part-1', cfg.sharedBaseUrl+'home.html', cfg, 'canvas')).searchParams.get('page'), 'home.html');
const url = new URL(runtime.hostedLink('../sprint-1.html?context=web#one', cfg.sharedBaseUrl+'assignments/problem-frame.html', cfg, 'canvas'));
assert.equal(url.searchParams.get('context'), 'canvas');
assert.equal(url.searchParams.get('page'), 'sprint-1.html');
assert.equal(url.hash, '#one');
assert.equal(new URL(runtime.hostedLink(cfg.mirrorBaseUrl+'sprint-1.html?context=web', cfg.sharedBaseUrl+'home.html', cfg, 'web')).searchParams.get('page'), 'sprint-1.html');
assert.equal(new URL(runtime.hostedLink(new URL('../sprint-1.html', cfg.mirrorBaseUrl).href, cfg.sharedBaseUrl+'assignments/problem-frame.html', cfg, 'canvas')).searchParams.get('page'), 'sprint-1.html');
assert.throws(() => runtime.hostedLink('new.html', cfg.sharedBaseUrl+'home.html', cfg, 'web'));
assert.equal(runtime.hostedLink('../../shared/template.docx', cfg.sharedBaseUrl+'assignments/a.html', cfg, 'web'), '../../shared/template.docx');
assert.equal(runtime.canvasLink('https://deanza.instructure.com/courses/46601/assignments/1636805', cfg), 'https://deanza.instructure.com/courses/46601/assignments/1636805');
'''
        subprocess.run(['node', '-e', code, str(ROOT/'canvas_sync/assets/course-mirror.js'), str(CONFIG)], check=True, capture_output=True, text=True)

    def test_native_client_cannot_write_source_or_access_people(self):
        api = CourseApi.__new__(CourseApi)
        api.origin = 'https://cti-courses.instructure.com'
        api.prefix = '/api/v1/courses/180'
        api.writable = False
        for method, endpoint in [('PUT','/assignments/7172'), ('GET','/enrollments'), ('GET','/users'), ('GET','/submissions'), ('GET','https://deanza.instructure.com/api/v1/courses/46601/pages/home')]:
            with self.assertRaises(ValueError): api.request(method, endpoint)
        api.writable = True
        for method, endpoint in [('POST','/assignments'), ('PUT',''), ('DELETE','/modules/2075'), ('PUT','/users/1')]:
            with self.assertRaises(ValueError): api.request(method, endpoint)

    def test_destination_institutional_chrome_is_preserved(self):
        source = '<div><iframe title="Home" src="'+self.config['sharedBaseUrl']+'home.html?context=canvas"></iframe></div>'
        prefix = '<link rel="stylesheet" href="https://instructure-uploads.s3.amazonaws.com/account_1/attachments/2/dp_app.css">'
        suffix = '<script src="https://instructure-uploads.s3.amazonaws.com/account_1/attachments/3/dp_app.js"></script>'
        destination = prefix + source + suffix
        desired = mirrored_body(source, self.config, destination)
        self.assertEqual(desired, prefix + mirrored_body(source, self.config) + suffix)
        self.assertEqual(mirrored_body(source, self.config, desired), desired)

    def test_source_position_gaps_do_not_reorder_destination(self):
        config = copy.deepcopy(self.config)
        config['mapping'] = {'modules':{'1':101},'module_items':{'2':102},'assignments':{},'discussion_topics':{},'page_urls':{'home':'home'}}
        source_module = {'id':1,'name':'A','position':8,'published':True,'unlock_at':None,'prerequisite_module_ids':[], 'require_sequential_progress':True,'completion_requirements':[], 'items':[{'id':2,'type':'Page','title':'Home','position':7,'published':True,'page_url':'home','completion_requirement':{}}]}
        destination_module = copy.deepcopy(source_module)
        destination_module.update(id=101,position=1)
        destination_module['items'][0].update(id=102,position=1)
        common = {'assignments':[],'discussion_topics':[],'pages':[],'assignment_groups':[]}
        before = {'source':dict(common,course={},modules=[source_module]),'destination':dict(common,course={'workflow_state':'unpublished'},modules=[destination_module])}
        self.assertEqual(plan(before,config,{'assignment_groups':{}})['operations'],[])


if __name__ == '__main__': unittest.main()

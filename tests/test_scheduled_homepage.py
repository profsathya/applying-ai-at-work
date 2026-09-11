from __future__ import annotations

import copy
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from canvas_sync.scheduled_homepage import calendar_data, render_scheduled_homepage, validate_schedule
from canvas_sync.hosted_html import render_hosted_files, validate_homepage_metadata
from tests.test_hosted_html import write_manifest, write_page


ROOT = Path(__file__).resolve().parents[1]


def homepage():
    return {"modules": [{"sprint": 99}], "schedule": {
        "timezone": "America/Los_Angeles", "start_date": "2026-10-05", "sprint_days": 14,
        "orientation_sprint": 99, "help_slug": "tuple-overview",
        "sprints": [
            {"number": 1, "sprint": 99, "ready": True, "title": "Find the problem", "summary": "Choose using evidence."},
            *[{"number": n, "sprint": None, "ready": False, "title": f"Topic {n}", "summary": "Work with evidence."} for n in range(2, 6)],
        ],
    }}


class ScheduledHomepageTests(unittest.TestCase):
    def test_calendar_includes_all_five_fortnights(self):
        data = calendar_data(homepage()["schedule"])
        self.assertEqual([e["start"] for e in data["sprints"]], ["2026-10-05", "2026-10-19", "2026-11-02", "2026-11-16", "2026-11-30"])
        self.assertEqual(data["sprints"][-1]["end"], "2026-12-13")
        self.assertIsNone(data["sprints"][1]["href"])

    def test_invalid_schedule_is_rejected_without_type_errors(self):
        for field, value in [("start_date", "10/05/2026"), ("start_date", "2026-02-30"),
                             ("timezone", "Mars/Olympus"), ("sprint_days", True),
                             ("sprint_days", 0), ("help_slug", []), ("orientation_sprint", 100),
                             ("override", 6), ("override", True), ("sprints", [])]:
            with self.subTest(field=field, value=value):
                data = homepage()
                data["schedule"][field] = value
                self.assertTrue(validate_schedule(data, {"tuple-overview"}, {99}))
        data = homepage()
        data["schedule"]["sprints"][0]["sprint"] = []
        self.assertTrue(validate_schedule(data, {"tuple-overview"}, {99}))

    def test_hidden_or_missing_modules_cannot_be_ready(self):
        data = homepage()
        data["modules"][0]["hidden"] = True
        self.assertTrue(any("visible" in e for e in validate_schedule(data, {"tuple-overview"}, {99})))
        data = homepage()
        data["schedule"]["sprints"][1]["ready"] = True
        self.assertTrue(any("cannot be ready" in e for e in validate_schedule(data, {"tuple-overview"}, {99})))

    def test_render_integration_keeps_module_pages_and_replaces_only_landing_layout(self):
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "course1/sprints/sprint-99/tuple-overview.md"
            manifest = root / "course1/manifests/production.json"
            write_page(md)
            write_manifest(manifest)
            (root / "course1/homepage.yaml").write_text(yaml.safe_dump(homepage()))
            self.assertEqual(validate_homepage_metadata(root / "course1"), [])
            render_hosted_files(manifest, root / "out", [], state={"artifacts": {}})
            directory = root / "out/deanza/course1"
            home = (directory / "home.html").read_text()
            self.assertEqual(home, (directory / "index.html").read_text())
            self.assertIn('id="course-schedule"', home)
            self.assertNotIn("Module Learning Goals", home)
            self.assertIn("Module Learning Goals", (directory / "sprint-99.html").read_text())
            self.assertIn('href="modules.html?context=web"', home)
            self.assertEqual(home.count('alt="Computing Talent Initiative"'), 1)
            self.assertEqual(home.count("New._CTI_Logo_RGB-1.png"), 2)
            self.assertIn('id="sprint-activities" open', home)
            self.assertIn('class="activity-title">Tuple Overview</span>', home)
            self.assertNotIn('id="sprint-action"', home)
            self.assertNotIn('id="all-modules"', home)
            self.assertIn('id="course-modules"', home)
            directory_html = (directory / "modules.html").read_text()
            self.assertIn("Modules and dates", directory_html)
            self.assertIn("Materials in preparation", directory_html)
            self.assertNotIn('id="sprint-activities"', directory_html)

    def test_direct_canvas_activity_links_use_deployment_state_and_curated_labels(self):
        import yaml
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md = root / "course1/sprints/sprint-99/tuple-overview.md"
            manifest = root / "course1/manifests/production.json"
            write_page(md)
            write_manifest(manifest)
            data = homepage()
            data["modules"][0]["groups"] = [{"label": "Begin", "items": [{"slug": "tuple-overview", "nav_meta": "Read", "meta": "Long instructions stay on the module page."}]}]
            (root / "course1/homepage.yaml").write_text(yaml.safe_dump(data))
            state = {"artifacts": {"tuple-overview": {"canvas_module_item_id": 731, "canvas_page_url": "tuple-overview", "canvas_type": "page"}}}
            render_hosted_files(manifest, root / "out", [], state=state)
            home = (root / "out/deanza/course1/home.html").read_text()
            instance = json.loads(manifest.read_text())["instance"]
            self.assertIn(f'data-canvas-href="{instance["base_url"].rstrip("/")}/courses/{instance["course_id"]}/modules/items/731"', home)
            self.assertIn('class="activity-meta">Read</span>', home)
            self.assertNotIn("Long instructions stay", home)

    def test_unready_panels_are_excluded_and_activity_labels_are_escaped(self):
        data = homepage()["schedule"]
        data["sprints"][1]["sprint"] = 100
        groups = {99: [{"label": "Start", "items": [{"title": "A < B", "meta": "Read & think", "web": "item.html?x=1&y=2", "canvas": None}]}],
                  100: [{"label": "Draft", "items": [{"title": "Unpublished material", "meta": "Draft", "web": "draft.html", "canvas": None}]}]}
        home = render_scheduled_homepage({"title": "Course", "footer": "CTI"}, data, logo_url="logo.png", help_link={"web": "help.html", "canvas": None}, module_groups=groups)
        self.assertIn("A &lt; B", home)
        self.assertIn("Read &amp; think", home)
        self.assertNotIn("Unpublished material", home)
        self.assertNotIn('data-activities="100"', home)

    def test_json_payload_and_copy_are_html_safe(self):
        data = homepage()["schedule"]
        data["sprints"][0]["summary"] = '</script><img src=x onerror="bad()">'
        rendered = render_scheduled_homepage({"title": "Course <test>", "footer": "CTI"}, data, logo_url="https://example.org/logo.png", help_link={"web": "help.html", "canvas": None})
        payload = re.search(r'<script id="course-schedule" type="application/json">(.*?)</script>', rendered, re.S)[1]
        self.assertEqual(json.loads(payload)["sprints"][0]["summary"], data["sprints"][0]["summary"])
        self.assertNotIn("<img src=x", rendered)
        self.assertIn("Course &lt;test&gt;", rendered)

    @unittest.skipUnless(shutil.which("node"), "Node is needed for browser calendar behavior")
    def test_browser_calendar_boundaries_and_overrides(self):
        script = ROOT / "canvas_sync/assets/scheduled-homepage.js"
        data = calendar_data(homepage()["schedule"])
        runner = r'''
const assert = require('node:assert/strict');
const {selectSprint} = require(process.argv[1]);
const schedule = JSON.parse(process.argv[2]);
const cases = [
  ['2026-10-05T06:59:59Z','orientation',undefined],
  ['2026-10-05T07:00:00Z','current',1],
  ['2026-10-19T06:59:59Z','current',1],
  ['2026-10-19T07:00:00Z','current',2],
  ['2026-11-02T07:59:59Z','current',2],
  ['2026-11-02T08:00:00Z','current',3],
  ['2026-11-16T07:59:59Z','current',3],
  ['2026-11-16T08:00:00Z','current',4],
  ['2026-11-30T07:59:59Z','current',4],
  ['2026-11-30T08:00:00Z','current',5],
  ['2026-12-14T07:59:59Z','current',5],
  ['2026-12-14T08:00:00Z','review',5]
];
for (const [instant,phase,number] of cases) {
 const result = selectSprint(schedule,new Date(instant));
 assert.equal(result.phase,phase,instant);
 assert.equal(result.entry.number,number,instant);
}
schedule.override=3;
assert.equal(selectSprint(schedule,new Date('2026-09-11T12:00:00Z')).entry.number,3);
schedule.override='orientation';
assert.equal(selectSprint(schedule,new Date('2026-12-15T12:00:00Z')).phase,'orientation');
'''
        result = subprocess.run(["node", "-e", runner, str(script), json.dumps(data)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

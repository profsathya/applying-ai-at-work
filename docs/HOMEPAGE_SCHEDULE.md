# Scheduled course homepage

An optional top-level `schedule` in `<course>/homepage.yaml` selects the focused current-sprint homepage. Courses without it retain the existing module-list homepage. CTI identity remains in the header and footer. The homepage shows a short current-sprint card and one large button that opens that module directly. The other modules appear below the card, with their activity lists collapsed. Detailed instructions remain on the activity pages.

`Open orientation` or `Open Sprint N` opens the corresponding generated `sprint-<storage-number>.html` module page. Beneath the card, each available module title also opens its own module directly. A separate arrow button reveals or hides that module's activities without navigating. The featured module is omitted from this lower list. The standalone `modules.html` directory retains all scheduled modules and the same title/arrow controls. Both views use the curated course inventory: the native Canvas Modules page still contains published legacy versions. No legacy publication settings change. Help stays visible on both pages.

Directory activity titles and order come from the artifact source and existing homepage groups. Item-level `nav_meta` in homepage YAML holds only concise navigation labels such as `Read`, `Practice · Encouraged`, or `35 points`; full `meta` descriptions remain on the detailed module pages. Zero points alone does not imply optional work. In Canvas, directory activity links use deployment-state module-item URLs and open in the existing Canvas window, retaining the native activity sequence. Outside Canvas, they open the hosted activity. No personal progress is fabricated on the homepage.

Course 1 starts October 5, 2026, which is two weeks after September 21. Its five 14-day windows are October 5-18, October 19-November 1, November 2-15, November 16-29, and November 30-December 13. Before October 5, the homepage features orientation. After December 13, it shows course review with the final sprint.

The browser selects by the calendar date in `America/Los_Angeles`, including daylight saving changes. It checks on load, each minute, on page restoration, and when the tab becomes visible. Selection uses the device's current clock. Scheduled transitions do not require another deployment. Editing the schedule or module readiness requires normal regeneration and publishing.

## Configuration

- `timezone`: valid IANA timezone.
- `start_date`: quoted ISO calendar date, such as `'2026-10-05'`.
- `sprint_days`: number of calendar days per sprint.
- `orientation_sprint`: existing visible storage sprint for orientation.
- `help_slug`: existing Help and Resources artifact slug.
- `sprints`: ordered entries, numbered consecutively from 1. Each has `number`, `sprint`, `ready`, `title`, `summary`, and optional `note`.
- Optional `override`: a displayed sprint number or `orientation`. Remove it or set it to null to restore automatic selection. An override affects everyone viewing this course homepage.

`number` is the participant-facing sprint number. `sprint` is the existing storage folder number; for example, Course 1's displayed Sprint 1 uses storage sprint 12. Do not rename artifacts or deployment identities to make those numbers match.

An entry may have `sprint: null` and `ready: false` while material is being prepared. It still appears in the calendar and becomes the featured sprint on schedule, but shows preparation status instead of a broken activity link. For Course 1, Sprint 2 has no active replacement and Sprint 5 is a placeholder. Assign the correct storage sprint and set `ready: true` only when the intended module is available, then regenerate and publish the homepage. Readiness is curated, not a live Canvas publication check.

The schedule changes homepage emphasis only. It does not change assignment due dates, publish Canvas modules, lock future work, mark anything complete, or override individual progress. Available modules remain reachable throughout. Canvas context and the existing progress session are carried into module navigation.

## Validation

Run the repository virtualenv:

```bash
.venv/bin/python canvas_sync/schema.py --homepage course1/homepage.yaml
.venv/bin/python canvas_sync/schema.py --all
.venv/bin/python -m unittest tests.test_scheduled_homepage tests.test_hosted_html
```

For the full fake-API test suite on a machine with a production `.env`, exclude those credentials:

```bash
env -u CANVAS_API_URL -u CANVAS_API_TOKEN -u DEFAULT_COURSE_ID PYTHON_DOTENV_DISABLED=1 .venv/bin/python -m unittest discover
```

Render through `canvas_sync.hosted_html.render_hosted_files` with authoritative deployment state. Publish `home.html`, its `index.html` alias, and `modules.html` together. Never hand-edit generated pages. Verify desktop/mobile layout, the large button destination, independent module-title links and arrow disclosures, before-start behavior, each date boundary, and unavailable material. Static no-JavaScript fallback keeps all module-title links available for manual navigation and hides inactive disclosure buttons.

## Design references

- [University of Minnesota: Canvas Hall of Fame, Organize](https://teachingsupport.umn.edu/canvas-course-site-hall-fame-awards-2026/canvas-hall-fame-organize): focus the homepage on current work and provide direct activity links.
- [Johns Hopkins: Canvas Home Page](https://canvas.jhu.edu/faculty-resources/home-page/): simple, uncluttered layout and consistent navigation.
- [Quality Matters: Bill of Rights for Online Learners](https://www.qualitymatters.org/qa-resources/resource-center/articles-resources/bill-of-rights-for-online-learners): readable screens, efficient navigation, and sufficient instructions at the point of use.
- [Instructure: How to Use Modules](https://www.instructure.com/resources/blog/how-use-modules-build-courses-canvas): organize activities into a coherent sequence.
- [W3C: Disclosure Navigation](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/): ordinary disclosure buttons and links suit website navigation. Separate native buttons use `aria-expanded` and `aria-controls`; module-title links remain independent of the disclosure.

These principles informed the design. The user selected a prominent current-module button with the other modules and expandable activity lists directly below it on the homepage. No single homepage layout is a universal accessibility requirement or evidence of improved learning.

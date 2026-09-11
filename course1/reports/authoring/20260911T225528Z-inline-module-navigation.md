# Course 180 inline module navigation revision

Implemented the user's clarified interaction: the large button opens the scheduled current module directly, other modules remain visible below it, module titles open their respective modules, and separate arrows disclose activity links in place. The editorial assessment is the agent's; the user authorized the change but has not separately reviewed this final rendering.

Scope: course1 / Canvas 180. The manifest ID was asserted before generation, and the hosted deployment diff was constrained to exactly `deanza/course1/home.html`, `index.html`, and `modules.html`. CTI header/footer, Pacific-time schedule, module readiness, curriculum, grading, due dates, and curated homepage YAML are unchanged. The lower list omits the featured module. Unready modules retain preparation status without broken links.

Sources reviewed: latest user correction; existing renderer, JavaScript, CSS, tests, schedule documentation; course1 manifest; local generated Sprint 1 and Sprint 3 destinations; previous report `20260911T224541Z-compact-modules-button.md`. Source implementation commit: `1073f7d` in draft PR 54. Previously consulted writing-to-teach revision 4 and reviewing-course-text revision 5 continue to inform this presentation review. No artifact or curated-metadata change required homepage-maintainer routing. The review-record contract was reread for this report.

This revision changes navigation and collapsed activity visibility. No lesson body, assignment prompt, criterion, or homepage summary was rewritten, so substantive prose counts remain unchanged. The removed extra directory step is replaced by direct per-module navigation. Activity links are visible only when their arrow is expanded. No consequential issue was found in this changed interaction. No participant testing was performed; these checks do not establish teaching effectiveness.

Observed validation:

- Repository virtualenv `canvas_sync/schema.py --all` passed in the isolated source checkout. `-m unittest tests.test_scheduled_homepage tests.test_hosted_html -q` passed all 25 tests in both shared and isolated checkouts. Coverage includes the existing 12 Pacific-time boundaries, daylight saving, readiness, escaping, and activity destinations. Full suite was not repeated for this presentation revision.
- `git diff --check` passed. Only the five intended source files were copied into the isolated source checkout.
- Desktop browser: Sprint 3 arrow expanded activities without navigation; its title opened the correct Sprint 3 module (`sprint-7.html`). The large Open Sprint 1 button opened the correct Sprint 1 module (`sprint-12.html`).
- At 390px viewport width, the homepage and expanded Sprint 1 activities had 390px document width, with no horizontal overflow. Arrow targets measured 44 x 44px. Enter collapsed the focused arrow. CTI branding and readable wrapping were visually inspected.
- The actual-date preview featured orientation; a Sprint 2 preview showed preparation status with no active primary link. Previews used local-only overrides and were not deployed. A browser back operation timed out; state was recovered and the remaining navigation checks passed. No full screen-reader audit was performed.

## Reviewed fingerprints

| Path | SHA-256 |
|---|---|
| `canvas_sync/scheduled_homepage.py` | `d8c9d5dab793694fe9e2dd192a1bb60041563634ab01972ee7ad38d18bf6d984` |
| `canvas_sync/assets/scheduled-homepage.css` | `6e3eca741faa2572d0aec3f70abf1afad8c5a9535671f339bf8c6709a7bac04f` |
| `canvas_sync/assets/scheduled-homepage.js` | `e2ce8e4c98ccb075e8647cc185f44eb2ba45e6973e244f1286ac2c80fc2dde55` |
| `tests/test_scheduled_homepage.py` | `b6dfc3b27e2f97cb1da1a7c6e5c1f2b6aaa2552c3e326bca40dd082ec314aaec` |
| `docs/HOMEPAGE_SCHEDULE.md` | `286f9bb7fb1d79ca36b25fa54f211d2c81ee30434f5ac20d90d492a22cd0fa8f` |
| `course1/homepage.yaml (read-only context)` | `efd4e895f3387afb4be773282546958a3adaaedcd4d42bc84f4d2ef6c0ed0054` |
| `course1/manifests/production.json (read-only context)` | `84d7a2ae96de5bae9ca351a1bbdb4b232e025bbb29ab92f75f7ec944ac16b435` |
| `.agents/skills/writing-to-teach/SKILL.md (read-only context)` | `9c8aa8c9d7651dc9a044b2354d73c6090a10fad53131a3271bdd0196be8df349` |
| `.agents/skills/reviewing-course-text/SKILL.md (read-only context)` | `8aec18d4e2f0984167c5198baf40e63cd724a71357cc18f187121580d4c7ee74` |
| `.agents/skills/reviewing-course-text/references/review-record.md (read-only context)` | `7f52a9ff5d1fc508e48158e952e4afd83b1a3137e4a33d60a1cb72436c4f23a4` |
| `deanza/course1/home.html` (generated for publication) | `dccc9ded52c8dbd7d841f684d11acd2c0646ad356afc50552379a567f3f988ba` |
| `deanza/course1/index.html` (generated for publication) | `dccc9ded52c8dbd7d841f684d11acd2c0646ad356afc50552379a567f3f988ba` |
| `deanza/course1/modules.html` (generated for publication) | `d169fd04c1dc60054292600646910b2fe8f3a085e78b59e559b608bb79435e8e` |

## Publication and live verification

Common-Curriculum commit `2ab1d3f0673193127593a9b51ddee2eee473cccb` deployed successfully in [Pages run 34655965121](https://github.com/profsathya/Common-Curriculum/actions/runs/34655965121). All three canonical live files returned HTTP 200 and matched the generated hashes above byte for byte. Evidence: `.source-intake/homepage-inline-modules/live-verification.json`.

In live Canvas course 180, the homepage showed the large Open orientation button and the other modules below it. Sprint 1's arrow expanded the six activity links in place. The large button opened the orientation module; the Sprint 3 title opened the correct Sprint 3 module. Both navigations stayed inside course 180. Back to course home returned successfully, and the finished homepage was left open. The first frame wait expired while Canvas was loading; the following accessibility snapshot showed the updated page, and all interaction checks passed. No Canvas API writes or other-course deployments occurred. The source PR remains a draft and unmerged.

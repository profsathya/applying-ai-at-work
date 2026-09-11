# Course 1 scheduled homepage review

Status: implemented revision, deployed to the existing hosted Canvas homepage. The user selected the current-sprint design and explicitly requested calculating the dates and updating the homepage. That authorizes implementation and publication; the final copy has not received a separate human editorial review. The editorial assessment below is the agent's.

## Schedule and behavior

Interpreted “two weeks from 9/21/2026 on monday” as Monday, October 5, 2026, and communicated this interpretation before implementation. Each sprint is 14 calendar days in America/Los_Angeles.

| Featured sprint | Inclusive dates in 2026 | Material readiness at publication |
|---|---|---|
| 1 | October 5–18 | First half available |
| 2 | October 19–November 1 | In preparation; no active replacement module |
| 3 | November 2–15 | Available |
| 4 | November 16–29 | Available |
| 5 | November 30–December 13 | In preparation; existing module is a placeholder |

Orientation appears before October 5. The card follows the calendar, including Pacific daylight-saving changes, on page load and within a minute on an open page. After December 13 it becomes course review. This is cohort pacing, not an inference about individual completion. Available modules remain reachable in the expandable directory. Dates do not change Canvas release restrictions or assignment due dates. Publishing future materials and updating their readiness is still required.

## Decisions, sources, and alignment

Kept CTI branding at the top and bottom, one short purpose and entry button, visible orientation/help links, and a collapsed module directory. Retained the Sprint 1 first-half/no-AI constraint. Version/rebuild labels were removed from landing-page titles; technical module identities remain stable. Detailed goals, task instructions, submission prompts, and assessment criteria stay on the module/activity pages.

The homepage-maintainer reviewed `course1/homepage.yaml`; orientation Start Here, How This Course Works, and Help and Resources in `course1/sprints/sprint-6/`; Sprint 1 introduction and Test and commit in `sprint-12/`; Sprint 3 introduction and Stakeholder Conversation in `sprint-7/`; Sprint 4 introduction and Learn and Check in `sprint-8/`; and the Sprint 5 placeholder introduction in `sprint-9/`. Parent context includes the earlier live audit and report `20260911T215607Z-homepage-audit-and-options.md`, the supplied prompt, renderer/source/state configuration, and `docs/AUTHORING.md` plus `docs/AUTHORING_PRESENTATION.md`. Design directories remained read-only.

Alignment: Sprint 1 compares real observations and candidate problems using a cumulative table and reasoned choice; Sprint 3 uses actual stakeholder evidence to revise a problem frame; Sprint 4 ties learning gaps to recorded claim checks. Sprint 2 and Sprint 5 summaries describe planned capabilities, explicitly paired with unavailable materials. They do not claim completed activities exist.

The baseline audit counted 299 words of Sprint 1 goals, prerequisite notes, and row descriptions. The new featured Sprint 1 support copy has 24 words: a 15-word purpose and 9-word readiness/no-AI note. The five scheduled summaries total 68 words; the orientation summary has 11. These are different navigation structures, not equivalent lesson-body counts. Response prompts and criteria were not revised; their before/after text is identical within this task's scope. Repeated navigation-level instruction is deferred to its existing point of use. Source adaptation was curated paraphrase, not exact-wording conversion. No participant testing was performed. Later module-page rebuild notes remain outside the homepage scope. No other consequential editorial issues were found in this scope.

Skills consulted by the homepage-maintainer: `.agents/skills/maintain-homepage/SKILL.md` (unversioned; hash below), `.agents/skills/writing-to-teach/SKILL.md` revision 4, `.agents/skills/writing-learning-goals/SKILL.md` revision 2, and `.agents/skills/reviewing-course-text/SKILL.md` revision 5. Parent followed the review-record contract and presentation guidance; reference hashes are below.

## Observed validation and publication

Parent-observed checks:

- `.venv/bin/python canvas_sync/schema.py --homepage course1/homepage.yaml` and `.venv/bin/python canvas_sync/schema.py --all`: passed. The worker separately reported homepage schema validation passing.
- `.venv/bin/python -m unittest tests.test_scheduled_homepage tests.test_hosted_html -q`: 23 tests passed, including date boundaries, Pacific daylight-saving change, overrides, unavailable modules, safe HTML/JSON, and integration.
- `env -u CANVAS_API_URL -u CANVAS_API_TOKEN -u DEFAULT_COURSE_ID PYTHON_DOTENV_DISABLED=1 .venv/bin/python -m unittest discover -q`: 229 tests passed in the shared checkout and 216 in the isolated source branch. Initial runs had 4 failures and 35 errors because real environment/.env Canvas settings contaminated fake-URL fixtures; disabling dotenv as well as removing inherited variables resolved them. Logs are in `.source-intake/homepage-schedule-20261005/`.
- `git diff --check`: passed. Draft PR 54's GitHub validation check also passed.
- Local desktop and 390px mobile previews: readable layout, loaded CTI logos, no observed horizontal overflow. Previewed Sprint 1 and an unavailable Sprint 2 card. Runtime tests exercised all five calendar windows and exact UTC transitions.
- Actual Canvas course 180: verified the new embedded homepage, opened Sprint 1 and orientation, and observed native Canvas completion status load after navigation. Expanded/collapsed the module directory with Enter. Restored the collapsed homepage. Full screen-reader testing and text enlargement were not performed; these checks are not accessibility certification or evidence of improved learning.
- Hosted home/index and ready module/help destinations returned HTTP 200. Deployed home/index bytes matched the generated SHA-256 below.

Only `deanza/course1/home.html` and `deanza/course1/index.html` were deployed to Common-Curriculum main at commit `d8923b5705492bffd297f9c89ac380aa87486c30`. [Pages deployment 34653560052](https://github.com/profsathya/Common-Curriculum/actions/runs/34653560052) succeeded. The existing Canvas iframe picked up the update; no Canvas API write occurred.

Source implementation was isolated from concurrent checkout work at commit `7fa459d` in [draft PR 54](https://github.com/profsathya/applying-ai-at-work/pull/54). It is not merged into source main. Source baseline: `c2182cc007b3f47f18ed633b0ca2de16610a2f55`; deployment-state revision: `237638e5cd92d33b7d24a99ec5b502aa4afcfd97`. Concurrent artifact/source edits were preserved and excluded from this PR. The shared-checkout hashes below identify the reviewed working bytes; notably hosted_html.py and homepage.yaml also contain pre-existing concurrent edits that are not in the isolated PR.

## Final fingerprints

| Reviewed output in shared checkout | SHA-256 |
|---|---|
| `course1/homepage.yaml` | `f54f8e38170badc1944bcab481377dc6054260ff99b37205cfde759fe372f18c` |
| `canvas_sync/hosted_html.py` | `aeba031d28df39778539e2fde80dde4ea8c57155adaa260361648fa66859a40d` |
| `canvas_sync/scheduled_homepage.py` | `ed8043899e4e2ab4fbbae0c1c65e4eb42aca6338eef47cc18c449123eb81c264` |
| `canvas_sync/assets/scheduled-homepage.css` | `372f5408295646cb810a68d6276423ee0c6fab8c07b6218666c9d85fdcb7cea8` |
| `canvas_sync/assets/scheduled-homepage.js` | `2c58814bd7087d4854640271498dd4f846ad96372c7ec057467eb018416c14c4` |
| `tests/test_scheduled_homepage.py` | `98fb3c4016c4c1f8439db20a39e9fa79717b1710462de47f005911296ef99a4e` |
| `docs/HOMEPAGE_SCHEDULE.md` | `9f7c069c612158752cec8ac33e28bd448c1acac0910bf0aec4672be12f59dfb3` |

| Reference | SHA-256 |
|---|---|
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `docs/AUTHORING.md` | `c73410117b4dd313c68ada6fe458e9098e83396eb3cca23277fa0dde1143cac7` |
| `docs/AUTHORING_PRESENTATION.md` | `fd86cdd9a726e34e0e5413eb8a850fa4d7989ff5b0d78eb614344c7f69a02688` |

Generated/deployed `deanza/course1/home.html` and `deanza/course1/index.html` each: `12e9d2c777e347c6f35ba8b5c6dcd224e6b416057ce237194f97b6859f3d5daa`.

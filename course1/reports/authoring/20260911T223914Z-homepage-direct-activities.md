# Homepage direct activity navigation

Status: implemented and live for Course 1, Canvas course 180. The user explicitly requested researching course-homepage best practices and implementing activity dropdowns plus Go to Modules. That authorization covers this revision and publication; it is not a separate human approval of the final text. Editorial judgments are the agent's.

## Research and decisions

| Guidance reviewed | Applied decision |
|---|---|
| [University of Minnesota: Canvas Hall of Fame, Organize](https://teachingsupport.umn.edu/canvas-course-site-hall-fame-awards-2026/canvas-hall-fame-organize) recommends current work and direct activity links. | Current-sprint activities are visible by default and open directly. The list can collapse. |
| [Johns Hopkins: Canvas Home Page](https://canvas.jhu.edu/faculty-resources/home-page/) recommends an uncluttered layout and consistent navigation. | Compact activity rows, one Go to Modules shortcut, and visible help. |
| [Quality Matters: Bill of Rights](https://www.qualitymatters.org/qa-resources/resource-center/articles-resources/bill-of-rights-for-online-learners) calls for readable screens, efficient navigation, and sufficient instructions. | Preserve readable type and activity instructions while shortening only navigation labels. |
| [Instructure: Using Modules](https://www.instructure.com/resources/blog/how-use-modules-build-courses-canvas) explains module sequencing. | Direct Canvas links use existing module-item IDs, retaining native activity context. |
| [W3C: Disclosure Navigation](https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/examples/disclosure-navigation/) distinguishes ordinary disclosure links from complex menu widgets. | Native details/summary and ordinary links, without copying the illustrative ARIA widget code. |

Opening the current dropdown by default is a contextual design judgment, not a universal accessibility rule. For 32 working professionals, including the stated audience in their 40s–50s, the design emphasizes scanability, predictable routes, and readable controls without assuming limited technical ability.

The first page now offers one-click activity entry; its previous Open Sprint route required navigating to an intermediate module page. Go to Modules opens a separate, compact directory with the same direct activity dropdowns. Read-only inspection found 11 published Canvas modules, including legacy course versions. The new directory uses only the curated current course inventory, avoiding those duplicates on this route. Native Canvas sidebar navigation and publication settings remain unchanged.

CTI header/footer and Pacific-time calendar are retained. Orientation appears before October 5, 2026; five 14-day sprints follow. Sprint 1 remains first-half-only, and Sprint 2 and Sprint 5 remain explicitly in preparation. No release, due date, completion, prompt, or grading rule was changed.

## Copy and alignment

The homepage-maintainer added 24 nav_meta labels across storage modules 6, 12, 7, and 8. Reading rows say Read; encouraged practice retains that distinction; native practice quizzes say Practice · Ungraded; assessed work shows actual points. Zero points was not treated as evidence of optional status. The introduction post retains its complete/incomplete distinction. Detailed meta, goals, summaries, titles, dates, and artifact bodies were preserved.

The intended learning is unchanged: compare candidate problems using observations and reasons; use actual stakeholder evidence; identify learning gaps and check claims. Activities retain their existing group order and lead directly to the source-authored teaching and submission instructions. Homepage labels are curated adaptations, not quotations or replacement assessment criteria.

Whitespace-token counts exclude titles, group headings, dates, branding, and navigation controls. Comparing the immediately previous scheduled homepage with this revision:

| Featured view | Prior supporting copy | New supporting copy including activity labels | Direct activity links before/after |
|---|---:|---:|---:|
| Orientation | 11 | 21 | 0 / 6 |
| Sprint 1 | 24 | 38 | 0 / 6 |

The added words label direct actions; they do not repeat procedural paragraphs. Response prompts and assessment criteria are unchanged within this task. This trades a small amount of visible navigation text for removal of an intermediate page. No participant testing or learning-effectiveness measurement was performed.

## Sources and skills

Parent reviewed the user request, live homepage and Modules page, generated source, deployment state, research above, existing homepage metadata, previous review records, and docs/AUTHORING.md plus docs/AUTHORING_PRESENTATION.md. Baseline live HTML was saved before editing in `.source-intake/homepage-direct-activities/before-home.html`.

The homepage-maintainer reviewed frontmatter and existing metadata for all 24 linked artifacts in `course1/sprints/sprint-6/`, `sprint-12/`, `sprint-7/`, and `sprint-8/`, additionally checking native practice-quiz settings, Introduction Post directions, and AI Exchange configuration. No design-input or artifact file was edited by this task. Skills actually applied: maintain-homepage (unversioned, hash below); writing-to-teach revision 4; writing-learning-goals revision 2 (maintainer); reviewing-course-text revision 5. Parent owns this record.

## Observed validation

- Worker-reported homepage and all-schema checks passed. Parent observed `.venv/bin/python canvas_sync/schema.py --all` passing in shared and isolated checkouts.
- `.venv/bin/python -m unittest tests.test_scheduled_homepage tests.test_hosted_html -q`: 25 tests passed after correcting a test expectation that included a duplicate URL slash. Coverage includes direct deployment-state links, concise metadata, excluded unready panels, safe escaping, page aliases, and the existing date-boundary tests.
- `env -u CANVAS_API_URL -u CANVAS_API_TOKEN -u DEFAULT_COURSE_ID PYTHON_DOTENV_DISABLED=1 .venv/bin/python -m unittest discover -q`: 231 tests passed in the shared checkout. The same command with the absolute repository virtualenv path passed 218 tests in the isolated source checkout after final edits. `git diff --check` passed.
- All 24 generated Canvas activity links matched published items in published modules from a read-only API check. All 24 hosted activity fallbacks returned HTTP 200.
- Observed desktop and 390px mobile layout, full mobile footer, readable wrapping, and no horizontal page overflow at 390px. Activity targets were at least 44px high. Current dropdown expanded by default; Enter collapsed it and Tab moved directly to Go to Modules, skipping hidden activities. Reviewed the separate directory and unavailable Sprint 2 state. Verified Sprint 4 selects seven hosted activity links in standalone web context.
- Live Canvas: homepage loaded successfully; one click on Start Here opened its native Canvas page with `module_item_id=17937`; Go to Modules opened the clean directory inside the course iframe; Back to home restored the featured list. The final homepage was left open.
- Browser zoom shortcuts did not produce a verified zoom change in automation, so actual text-enlargement behavior remains unverified. Full screen-reader and learner-account testing were not performed. These checks are not accessibility certification.

Publication: generated `home.html`, `index.html`, and `modules.html` deployed in Common-Curriculum commit `5bcb987cbefda4773548ebc087efeca87eed3073`. [Pages run 34654688545](https://github.com/profsathya/Common-Curriculum/actions/runs/34654688545) succeeded, and all three live files matched the generated bytes exactly. No Canvas API write occurred. Source is maintained separately in [draft PR 54](https://github.com/profsathya/applying-ai-at-work/pull/54), excluding concurrent course/renderer edits. Evidence and logs are in `.source-intake/homepage-direct-activities/`.

Deferred: missing Sprint 2/5 materials and published legacy Canvas modules remain outside this homepage revision. Schema success does not establish teaching effectiveness. No other consequential issue was identified in the changed navigation scope.

## Output fingerprints

Hashes identify the isolated source used to generate the live pages. The shared checkout also contains concurrent edits in hosted_html.py and homepage.yaml; those hashes are recorded separately below.

| Published source file | SHA-256 |
|---|---|
| `course1/homepage.yaml` | `efd4e895f3387afb4be773282546958a3adaaedcd4d42bc84f4d2ef6c0ed0054` |
| `canvas_sync/hosted_html.py` | `8cea2ad3e10831db1deedb54acf739160a79c9a57f1f863f1b33e690ec150385` |
| `canvas_sync/scheduled_homepage.py` | `893fc4ecba2a6218d181d15d379ff499a230ad111733fbd3a0a9d1afe4b1c253` |
| `canvas_sync/assets/scheduled-homepage.css` | `158bc8bd99108a6f31cc55e1860a5e45172b24f4fa11f8e94493e5b9c03e0aba` |
| `canvas_sync/assets/scheduled-homepage.js` | `44ae0587f5f0f09bc1b64690a9541b202d6279dfdb25a75d98ee7c64f6434cd3` |
| `tests/test_scheduled_homepage.py` | `cf87ca4a20565d5b0ef496d181a6c94b8d0b2ce34483a63bed5a73e441949504` |
| `docs/HOMEPAGE_SCHEDULE.md` | `eaf6db2960684def6878cc1e2db58215fe3fc2b8446a1896afa335cb27f824a6` |

| Shared checkout or reference | SHA-256 |
|---|---|
| `course1/homepage.yaml` | `1814ae450d654e48272f0d701b75b84cab9d025249d401401a9655c26d7fac49` |
| `canvas_sync/hosted_html.py` | `2b03e16d123e3598cda8b1e1cab47f97575e9f0b88049170cd38982e8498ae0d` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `docs/AUTHORING.md` | `c73410117b4dd313c68ada6fe458e9098e83396eb3cca23277fa0dde1143cac7` |
| `docs/AUTHORING_PRESENTATION.md` | `fd86cdd9a726e34e0e5413eb8a850fa4d7989ff5b0d78eb614344c7f69a02688` |

| Deployed file | SHA-256 |
|---|---|
| `deanza/course1/home.html` | `40baf564d136fbf599649f54233fa858f1b9fac6b0d4a1df7bc2a0dac8bd4054` |
| `deanza/course1/index.html` | `40baf564d136fbf599649f54233fa858f1b9fac6b0d4a1df7bc2a0dac8bd4054` |
| `deanza/course1/modules.html` | `fce1314f8144b398590ce255047ae2bb1c72ab3f619b2612c1efe025f07ed350` |

Baseline hosted HTML SHA-256: `12e9d2c777e347c6f35ba8b5c6dcd224e6b416057ce237194f97b6859f3d5daa`.

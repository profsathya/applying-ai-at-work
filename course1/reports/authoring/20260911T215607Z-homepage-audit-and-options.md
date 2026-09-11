# CIS 501 homepage audit and design options

Status: recommendations-only review of the live homepage, with three separate design drafts. Editorial conclusions are the agent's assessment. The user authorized the audit and examples; approval of a design has not been requested or observed. No production course content, Canvas state, or homepage metadata was changed by this task.

## Assessment

The homepage asks readers to process too much instructional detail before choosing an activity. The CTI identity is useful and worth preserving. The main opportunity is clearer hierarchy and placement of information, rather than compressing the same material into smaller type.

The audience is 32 working professionals in Silicon Valley, primarily in their 40s and 50s. Design for readable text, predictable navigation, quick return visits, and access to help. Do not infer limited technical skill or reduced ability from age. Cohort size does not justify displaying a leaderboard or adding a social dashboard.

| Finding | Evidence inspected | Recommendation |
|---|---|---|
| The first action is delayed | Sprint 1 has 77 words of learning goals and 74 words of prerequisite/release notes before its first activity. At a 390 x 844 viewport, its first activity link begins at approximately y=850 on the standalone hosted page. | Show one short purpose, a clear sprint entry, and essential constraints. Put detailed goals and directions on the linked introduction and activities. |
| Each activity row teaches and explains submission again | Six row descriptions total 148 words. Copy-and-submit directions recur across five rows. | Use titles and short decision-relevant metadata. Preserve optional status, points, and observation over a day or two. Leave task procedures at their point of use. |
| Small supporting text makes a dense layout harder to scan | Live item descriptions compute to 12px, prerequisite text to 12.5px. The layout has several gray, blue, and green bands, separators, icons, badges, and completion boxes. | Start drafts around 16px body text and 15px supporting text, with stronger text contrast and fewer competing surfaces. This is a design recommendation, not a claim of a measured accessibility failure. |
| Production history leaks into the participant experience | V2 appears in titles and tags; Sprint 3 describes a reviewed rebuild kept separate for comparison; Sprint 4 also describes a rebuild. | Remove version and review labels from the participant-facing presentation. Retain technical identities in source/deployment state. |
| Availability is unclear | Visible order is orientation, Sprint 1, Sprint 3, Sprint 4, Sprint 5. Sprint 5 opens to a placeholder; Sprint 1 has only its first half. | Explain the intended Sprint 2 release before adoption. Label incomplete work clearly. Do not create an invented date, replacement module, or release status. |
| Completion may look actionable or obligatory | Status is drawn as checkbox-shaped indicators; some optional practice has completion tracking. The observed Canvas account shows 9 of 25 complete. | If retaining progress, use explicit read-only status and keep optional practice distinct from requirements. Do not copy the instructor account's progress into a learner example. |
| Help is buried | Help and Resources is inside collapsed orientation. | Keep one direct Help and resources link visible in every design. |

The Canvas page was inspected in the user's instructor view. Its administrative controls and sidebars are not attributed to the participant homepage design. The embedded page repeats the course title already displayed by Canvas. Final implementation should coordinate the host title and embedded heading rather than treating both as required visual headers.

## Three draft directions

**A. Current sprint, recommended.** CTI header, course title, one highlighted sprint with a short purpose and Open Sprint 1 action, orientation/help links, and an expandable module list. This gives return visits a clear starting point. Featuring Sprint 1 is based on the currently expanded live panel, not a verified calendar date or personalized next incomplete activity.

**B. Compact checklist.** Keep all six Sprint 1 activity links visible, organized into introduction, optional practice, and submissions for points. Preserve activity names, the 5 completion points and 35 points, the no-AI constraint, one cumulative table, and the day-or-two observation requirement. This has more vertical content than A but fewer competing explanations than the current page. It is the best candidate for the page reached from A.

**C. Course directory.** Show one concise row per available module and a clearly marked Sprint 5 item in preparation. This supports direct selection by participants who already know where they are going; it provides less guidance about the next action than A.

All three reuse the existing CTI logo, preserve Computing Talent Initiative and De Anza College attribution in the footer, and link to observed course destinations. These are adapted navigation examples, not replacements for teaching, prompts, or assessment criteria. The drafts do not claim personal progress or invent due dates. Sprint 2's absence remains an explicit implementation decision to resolve; its reason is not guessed in the drafts.

## Content alignment and measurements

Sprint 1 develops the ability to identify and compare candidate problems using real observations. Prior work is participants' own experience. Practice builds one cumulative table, including workarounds and requests. Evidence is the concept check and a reasoned choice with alternatives and uncertainty in Test and commit. The draft summary does not promise AI deployment or validated causes. Work remains without AI in the first half.

Counts use whitespace-separated tokens, including standalone punctuation. Exclude titles, group labels, navigation, branding, and progress announcements. The baseline counts learning-goal text, the prerequisite paragraph, and six row descriptions. Draft counts include marked supporting copy and point/optional/pacing notes. These count navigation copy, not the complete instructional experience.

| Scope | Body/supporting copy | Response prompts | Assessment criteria |
|---|---:|---|---|
| Current Sprint 1 homepage panel | 299 | No prompt revision | No criteria revision |
| Draft A, visible supporting copy | 18 | Unchanged in source | Unchanged in source |
| Draft B, supporting copy | 35 | Unchanged in source | Unchanged in source |
| Draft C, supporting copy across directory | 44 | Unchanged in source | Unchanged in source |

These are different homepage structures, not equivalent lesson word counts. Detail is deferred to linked pages, not removed from the course. A full implementation must verify that the destination introduction contains the full goals and necessary directions. No participant testing was performed; no claim of improved learning or faster task completion is made.

## Sources reviewed

- Live Canvas homepage: https://cti-courses.instructure.com/courses/180, including the embedded page and the original visible progress state.
- Hosted homepage: https://profsathya.github.io/Common-Curriculum/deanza/course1/home.html?context=web. Expanded and read all five visible modules; inspected desktop and 390px mobile renderings.
- `course1/homepage.yaml`, `canvas_sync/hosted_html.py`, `docs/AUTHORING.md`, and `docs/AUTHORING_PRESENTATION.md`.
- All six non-header Markdown artifacts in `course1/sprints/sprint-12/`: introduction, three practice activities, concept check, and Test and commit. Also `course1/sprints/sprint-6/help-and-resources-v2.md`.
- Existing official logo observed on the live page: https://computingtalentinitiative.org/wp-content/uploads/2026/06/New._CTI_Logo_RGB-1.png. Reused only for the requested CTI-branded drafts, with the top image's alternative text retained and the footer image decorative beside written attribution. No broader image license determination was made.
- Repository orientation: `AGENTS.md`, `README.md`, `README-BUILDER.md`, and `docs/codex-migration/migration-plan.md`.

The checkout contains pre-existing and concurrent work. In particular, the local introduction and its homepage description differ from the initially observed live wording. No reconciliation or publication was attempted, and local activity revisions are not presented as verified live changes. Later sprint activity bodies were not reviewed; their homepage summaries were reviewed.

## Skills and observed checks

Skills consulted: `reviewing-course-text` local revision 4, `writing-to-teach` revision 3, `writing-learning-goals` revision 2; `maintain-homepage` was read for scope and source ownership, with no YAML maintenance needed for separate drafts. `visualize` and its `tweak.md` reference were used for the examples. The narrow editorial review did not require a course inventory or a Canvas inspection subagent.

- Rendered the fragment with `.venv/bin/python /Users/shaw8048/.codex/plugins/cache/openai-bundled/visualize/1.0.32/skills/visualize/scripts/render.py /Users/shaw8048/.codex/visualizations/2026/09/11/01a09273-6dc8-7660-95f4-009db96f7b14/cti-homepage-options.html --serve --port 8779`: succeeded.
- Visually inspected A, B, and C at a 736px content width, and A at a 358px content width. All six logo images loaded.
- Browser DOM checks across all three drafts at 358px and 320px content widths found no horizontal overflow among headings, paragraphs, links, or footers.
- Expanded A's module list by click and collapsed it with Return; Tab then reached the next focusable link. Native disclosure semantics were observed. Full screen-reader testing, text enlargement, dark appearance, and the host Tweak selector were not exercised in the standalone browser.
- The guarded design selector shows A by default in supported conversation hosts; the standalone renderer displays all three options for comparison.
- Course schema validation and unit tests were not run: no schema-controlled source artifact, homepage YAML, or renderer code was changed by this task. The draft is a separate presentation example. Checks do not establish accessibility certification or participant learning.

## Final fingerprints

| File | SHA-256 |
|---|---|
| `course1/homepage.yaml` (review target, unchanged by this task) | `c6ba6b54386d0d89cbb2de55f9effd4820d6a08bc8becbc8ec2bb24b467d87a0` |
| `canvas_sync/hosted_html.py` (read-only context) | `fd615761deb2893de7ac62f4cb902e047ff90e42cd6821a28f6373fe6b92d4e9` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `docs/AUTHORING.md` | `4c3046d8ac5313d57935acfc16f038d722d5558d27d043ed6bd045a5c17a324d` |
| `docs/AUTHORING_PRESENTATION.md` | `6fb5a458bac04a20f6808654ac5f4f451b1935174fcd077bed3b80d51ea997ce` |
| Visualize `SKILL.md` at the consulted plugin path | `f1509260a68ecf31aa7f21059236f37c4e85f22b9582c6b8e94c1caa57ad7d47` |
| Visualize `tweak.md` at the consulted plugin path | `106a0ee783d601794891952ac4236fcff4f28a593f6a6d448037b4c344f2e7a4` |
| `/Users/shaw8048/.codex/visualizations/2026/09/11/01a09273-6dc8-7660-95f4-009db96f7b14/cti-homepage-options.html` | `867ed9341b3fa9c7e1c11700384be0da425255e64606572777e77a3ac9407524` |

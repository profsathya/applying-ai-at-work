# Stakeholder Map Canvas Walkthrough: authoring and implementation review

## Target and status

Course1, Canvas course 180, original Stakeholder Map assignment 7159 and module item 17991 in module 2081. One new draft: **Stakeholder Map Canvas Walkthrough**, stored in sprint-16 and anchored to the original Sprint 3 module. The user explicitly authorized an unpublished Canvas push after the agent's review. This is the agent's editorial assessment, with an independent read-only review; no human approval of the resulting text or participant usability study is claimed. Other assignments in the user's example list were not converted.

## Sources and decisions

Read the supplied Stakeholder Map Google Doc (`1Z0Sg2_2lnQNiryTOpzerdhIovuE4a4-AGivkxR2bRP4`), all visible body blocks and tables, document metadata and comments, the live Canvas assignment/settings/module order, its actual hosted iframe instructions, and local `course1/sprints/sprint-15/stakeholder-map-v3.md`. Read the relevant Dojo Lab, Brainstorm source and guided version, and approved sprint-12 Test and commit example. Source capture is private under `.source-intake/stakeholder-walkthrough-20260923/`. The Google capture used PREVIEW_WITHOUT_SUGGESTIONS; no comments were returned. Hidden suggestions remain unverified; none were accepted or inferred.

The intended capability remains profiling four real stakeholders, distinguishing evidence from inference, identifying two or three consequential assumptions, and selecting a first contact and backup. Kept 35 points and file upload, with no invented rubric or dates. The original has no rubric, overrides, or due/availability dates. Direct second-person voice, four relationship names, field questions, Dana's handover examples, traps, restrained emphasis, and later-use reflection/outreach tables remain recognizable. Examples are expandable beside the relevant field. Source prose was deliberately adapted through `source_build.py` with provenance; tables were mapped directly from structured source cells, separately verified. This is not a verbatim prose conversion.

The user's explicit request for interwoven feedback changes the original no-AI rule for this alternative. Participants write first, keep their first draft, can continue without AI, and receive formative feedback on only the selected row. Setup/identity fields have an explicit feedback omission reason; two later-use tables are read-only. Eight content task IDs have reviewed server criteria. Browser drafts, copying, downloads, and feedback do not submit work. The shared opening requires a durable copy and links the supplied template.

## Audit findings and resolutions

| Finding | Resolution and observed evidence |
| --- | --- |
| Source tables without headers could lose the first row or require invented headings. | Added zero-header support across mapper, schema, renderer, rich clipboard, Word export and preview checks. All 11 source grids match exactly; seven are headerless, including one single-row table. |
| Local sample feedback could be mistaken for a working provider integration; registry was empty. | Added schema-enforced registry coverage, eight source-specific checkpoints, a live check CLI, deployed the service and reviewed actual provider responses. Local browser report remains honestly PARTIAL for its skipped provider call; separate live evidence resolves that requirement. |
| First live assumption feedback contradicted the original worked example. | Revised criteria to accept a conditional change in who to talk to or investigating a prior attempt. Retested all eight checkpoints; all respond, and the three assumption results now recognize the valid source pattern. |
| Real paste was only an optional/unverified workflow step. | Skill now requires actual browser paste and exported/native structure inspection. Actual Copy work -> Command-V in a blank Google Doc -> Google Doc DOCX export preserved all 11 grids and 138 cells, including four entered answers and a multiline answer. |
| Shared opening lacked explicit durable workbook instructions. | Added consistent records instructions plus an optional destination link. Inspected rendered opening on desktop and 390-pixel mobile. |
| Placement retry could duplicate a module item; sparse Canvas positions made array offsets unreliable. | Save provisional placement before verifying order; calculate from live anchor position. Regression tests cover retry identity and sparse positions. |
| Skill naming, source tone review, batch inference and real acceptance gates were underspecified. | Updated skill and live-check reference for exact suffix, source comparison, `(yes)` lists, repeated document links, example-only scope, and already-authorized staging without redundant confirmation. |

Independent reviewer confirmed source tone, assessment, instructions, all table mappings, and the 138 exported Google Doc cells. Homepage-maintainer reviewed `course1/homepage.yaml`, kept it unchanged because this is an unpublished alternative, and reported homepage and all-schema validation passing. No blocking editorial issue remains in this scope. Merged/nested tables still require a deliberate documented adaptation; the skill does not claim universal lossless conversion for unsupported structures.

## Observed validation

- `canvas_sync/source_intake.py` captured the Google Doc; `source_build.py` built only the selected artifact and sidecar. All 11 `walkthrough_tables.compare_task` comparisons passed for source text, dimensions, header selection, response roles, and read-only state.
- `.venv/bin/python canvas_sync/schema.py --all`: PASS. `canvas_sync/link_audit.py --all`: 167 artifacts, 57 links, 0 errors. Skill `quick_validate.py`: valid. `git diff --check`: passed.
- `env -u CANVAS_API_URL -u CANVAS_API_TOKEN -u DEFAULT_COURSE_ID PYTHON_DOTENV_DISABLED=1 .venv/bin/python -m unittest discover`: 295 tests, OK, one skip. Initial full run accidentally loaded the local production URL into mocked example-course tests and failed the institution guard; disabling dotenv only for the mock test process resolved that environment collision. Production guards were not weakened.
- `npm test --prefix services/course-ai`: 10 passed. Independent reviewer additionally reported 22 targeted Python tests and 10 service tests passed.
- `preview_module.py --manifest course1/manifests/production.json --state-dir <original checkout>/.canvas-state --sprint 16 --output <intake>/preview --check-browser` with bundled Node/Playwright and Chrome: all local interaction/layout checks pass; live provider is deliberately skipped in that runner. Checked labels, headings, table shape, save/reload, preview feedback placement, rich copy, clipboard-denial selectable fallback, Word export, mobile table scrolling, desktop/mobile page overflow and enlarged text. Parent manually inspected desktop opening/tables and 390-pixel opening/table. No human participant testing claimed.
- Actual Google Docs paste: scratch document `https://docs.google.com/document/d/1VacQO4ob5V3wW5pgzSBQDaVVnGOIIzUK565_mp2oc5A/edit`. Dimensions: 2x2, 1x2, four 8x3, three 4x2, two 3x2. All source cells and entered text match, normalizing NBSP padding and outer whitespace only; internal line breaks checked. Export SHA-256: `ea886b4dee22a08350be2ee6bd9732908ecbda9df592aea7d9dad12e752c3d8d`.
- `walkthrough_feedback_check.py --artifact course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md --live --samples <intake>/feedback-samples.json --output <intake>/live-feedback-results-final.json`: 8/8 real requests pass after the criteria correction; parent reviewed relevance, evidence handling, one revision question, and no grading/answer generation. Final Netlify deploy: `6ab436caa11f44fc55b65a9d`. Model and credentials unchanged. Runtime feedback is nondeterministic; these are observed samples, not a guarantee about all future feedback.
- Fresh Canvas preflight confirms the original assignment and module order still match the intake. Planned new item is unpublished after item 17991, before the Dojo Lab. Hosted button/iframe and final live Canvas placement will be recorded in a separate deployment verification after the authorized push.

## Reviewed output fingerprints

| Output | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` | `7b169fcae73ea6d60db233d44e7ba1e82438c12ffa5abef99184fc768f27da70` |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.sources.json` | `a84d54b67e8c5fae7b768348fcddea8c3d4267e51ff2b50850fedbe129dc61ee` |
| `services/course-ai/netlify/functions/walkthrough-guidance.json` | `80bc7f8e5cc3084d05b168db0273be8cdb444d58a5c7d7e6c9d55cc5e772c441` |

## Skills consulted

Parent consulted these skills; maintain-homepage was used by the homepage-maintainer worker. Independent review also consulted reviewing-course-text.

| Skill | Version |
| --- | --- |
| `.agents/skills/create-canvas-walkthrough-assignments/SKILL.md` | `85a26af647be74e7cca91e93f755784dfb380acac69c41cf19caeb37c1c8aeed` |
| `.agents/skills/inspect-canvas/SKILL.md` | `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404` |
| `.agents/skills/sync/SKILL.md` | `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b` |
| `.agents/skills/writing-assignments/SKILL.md` | local revision 4 |
| `.agents/skills/writing-to-teach/SKILL.md` | local revision 5 |
| `.agents/skills/writing-learning-goals/SKILL.md` | local revision 2 |
| `.agents/skills/reviewing-course-text/SKILL.md` | local revision 6 |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `/Users/shaw8048/.codex/skills/.system/skill-creator/SKILL.md` | `6656e54755638e8efcf275a472b9672eaa8a9a1b9e59dc210e275b03b59e1e66` |
| `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/google-drive/0.1.16/skills/google-drive/SKILL.md` | `dabae8a192c861b76cf7b5742bdf14f8ed35e67d8e6cacfd5f746ffbefd6da5c` |
| `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/google-drive/0.1.16/skills/google-docs/SKILL.md` | `8e5c26053d800e2980b74ab82c2ce95db94a17fbb443f8f6e30baeb442f1d464` |
| `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/netlify/1.0.0/skills/netlify-ai-gateway/SKILL.md` | `f5424f5a4eb755c82d27e29bbb57947f32c8afda0a18beed197b603ef1449e0a` |
| `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/netlify/1.0.0/skills/netlify-deploy/SKILL.md` | `8d39dd6d03415fcab770a28fba303cf23c995ea7b8be372a9d1587381a912f04` |

### Reference fingerprints

| Reference | SHA-256 |
| --- | --- |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |
| `.agents/skills/create-canvas-walkthrough-assignments/references/live-checks.md` | `b3390a37deb2e5d39fd91c9783c58f7678b57e4909accf91503d09864041da6e` |
| `docs/AUTHORING.md` | `cca09dec02d660db8ba107060aeb85a49461cf75f39c32b062bc24a1e4754af4` |
| `docs/AUTHORING_PRESENTATION.md` | `5d9a732651a1a9c4d95b5fec7ac152b56e7c52f270c3f8779c1d4679a9be5ba8` |
| `docs/DOCUMENT_INTAKE.md` | `c9242550d0b13d84cb77e764091b9a35db5e05621fa5c0f43f1d870f666aa55c` |

### Private evidence fingerprints

| Evidence | SHA-256 |
| --- | --- |
| `packet/source-packet.json` | `8ff1627fc37bdea2bf5421fcc4dff230bbe96a0248363d4851ce1362094c6b37` |
| `table-map.json` | `0b0d151901d4ec4fa96f8e37dfbcdecd8e5cc577fbef735cdab9fe27c6668a8b` |
| `table-comparison.json` | `9d73ac976800844afd44655fe3d2d31b9ef83f2422e84e34a1e917679ac49612` |
| `google-docs-paste-result.json` | `59a42fbc26ebdb3a4a74a81bf1eac2fe6136e77170c47715275f2a8a901c8484` |
| `live-feedback-results-final.json` | `3d622476cc4e845f44f993a584919f3063fde60213f6106544673ce68fbad3f8` |
| `preview/browser-results.json` | `d2e3bed1635381713ed937971176a159a5d4cbca1ff7b613161be0b898f013c4` |
| `canvas-preflight.json` | `85f23062acc170fd8909b31afd4668a888813b8141b89cf4759a6a03667109b2` |

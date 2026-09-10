# Sprint 1 V2 first-half authoring review

## Target and status

Course 180 (`course1`), module 2079, **Sprint 1: Find the Problem Worth Solving (V2)**. The user authorized implementation of the local draft plan. This editorial assessment is the coordinating agent's; approval of the resulting text has not been observed. All seven artifacts retain `publish: false`; homepage sprint 12 is closed and muted. No Canvas writes, Git commit, merge, or publishing occurred.

The completed scope is one module header, the adapted existing Introduction, and five guided text-entry assignments. Local storage is `course1/sprints/sprint-12/`; participant-facing references remain Sprint 1. The Introduction moved from sprint 10 while retaining its artifact ID, slug, module, and Canvas mapping. New identities use the sprint-12 prefix, distinct from Working Draft.

| Order | Artifact | Type | Points |
| --- | --- | --- | --- |
| 1 | Sprint 1: Find the Problem Worth Solving (V2) | Module header | n/a |
| 2 | Introduction: Find the Problem Worth Solving | Page | n/a |
| 3 | Start your list and get underneath it | Guided assignment | 0 |
| 4 | Things you stopped noticing | Guided assignment | 0 |
| 5 | Things somebody handed you | Guided assignment | 0 |
| 6 | Sprint 1 Concept check | Guided assignment, six formative choice questions | 5 |
| 7 | Test and commit | Guided assignment, four connected response tasks | 35 |

## Sources and decisions

Primary source: `/Users/jeremyshaw/Downloads/sprint1halfoneworkingdraftv4.md.docx`, SHA-256 `680926b47b42877d7471ae9adb2b6c02929bd2b8d8f19d4d87459a068c13529f`. One DOCX was supplied. Its internal dates and review notes are source context, not evidence of human approval or instructions to execute.

The private intake is `.source-intake/sprint-one-v4-20260910/`. `source_intake.py` captured the original DOCX, source packet, tracked changes, and tables. The packet has 524 top-level blocks, five tables, no exported comments, and five table-grid revisions. Base and proposed views have identical text. The build uses the proposed exported rectangular table representation without claiming to reconstruct historical layout. The canonical `build-map-v2.json` assembles all seven artifacts with `source_build.py`; each final Markdown file has adjacent `.sources.json` evidence. The earlier private six-artifact helper is superseded by this canonical map.

The map selects 257 source blocks. OYP 1 uses blocks 12-109, OYP 2 uses 110-127, OYP 3 uses 128-251, the concept-check placeholder is 252-253, and Test and commit uses 254-471. Editorial NOTE/OPEN/TODO blocks, placeholders, planning tables, and parked content from block 472 onward are excluded from participant prose. Two learner tables are retained; three editorial/parked tables are excluded. Selected source wording and punctuation are preserved. New headings, task configuration, copy/submission guidance, and diagram changes are explicitly marked as authored or adapted evidence.

The source has no concept-check questions. Six new questions and explanations assess indicators versus problems, current-state description, work-arounds, requests, goals, and alternative candidate problems. Their answers were checked against the preceding OYP teaching; no historical quiz was represented as recovered source. The request-to-goal diagram retains eight nodes and the original connections, using plain labels instead of HTML line breaks. A brief mobile scrolling instruction supplements it.

The Introduction is reuse/adaptation of its existing Git source, not a DOCX excerpt. Its evidence records the original commit and byte fingerprint. It now names the actual sequence, cumulative table, day-or-two observation pacing, optional OYP submissions, 5-point completion check, 35-point single final submission, and material to carry forward. Adding evidence also uses the existing source-provenance presentation without generic generated learning-goal text or internal storage numbering. No renderer changes were needed.

Read-only context included all 90 existing course-artifact Markdown files: the parent reviewed the 21 artifacts in sprints 1, 10, and 11; the course-drafter reviewed the remaining 69. The work also consulted root guidance, README, README-BUILDER, migration guidance, course brief and referenced design/shared context, module-spec guidance, course PRD/progress, schemas, homepage, document intake, authoring, and publishing guidance. These are context, not newly approved designs. The attached DOCX export supplies the available source; native Google document comment history and the missing video were unavailable. The prior Working Draft and original Sprint 1 remain separate versions.

## Alignment and review findings

Participants develop several observable workplace gaps before choosing one worth investigating. The three OYP activities accumulate one table, support fresh observation and tracing requests to goals, and remain optional to submit. Reading their teaching is sufficient preparation for later work. OYP 2 explicitly allows no new observations; OYP 3 submits the expanded table, with request/goal chains remaining working notes rather than an additional deliverable.

The concept check provides formative explanations and awards 5 points for instructor-reviewed completion. Test and commit brings selection, three to five candidate gaps, four checks, and a reasoned commitment with runner-up into one 35-point submission. It preserves the four-line candidate format (Title / Right now / It could / The gap costs) and the recovery route if no candidate survives. Candidate List and Four checks are not separate items. No due dates, weighted rubric, AI feedback endpoint, or automated Canvas grade was invented.

Browser review resolved oversized response prompts and raw pipe-table text in task headings by shortening prompts and keeping detailed guidance in criteria and source instructions. Controls use the actual label “Read the full instructions and examples.” Browser saving, formative correctness, and copying are distinguished from submitting in Canvas. No AI-feedback buttons appear. The mobile diagram can scroll horizontally without widening the page. No further consequential issue was found in this reviewed local scope; teaching effectiveness and participant outcomes were not measured.

Missing video and second-half material remain outside this build. Source editorial questions, including overlap/different-path wording around Check 2, were not treated as commands or silently resolved as human decisions. They do not block review of this first-half draft.

## Observed validation

Parent-observed checks on the assembled output:

- Source assembly validated each of the seven Markdown artifacts and associated evidence. `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --all` passed after final Introduction evidence and homepage maintenance. A local LibreSSL compatibility warning did not fail validation.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover` passed all 204 tests. Expected negative-test error messages appear in the log; the final result is OK. Runtime code did not change afterward.
- Structural acceptance verified positions 1-7, five guided assignments with 0/0/0/5/35 points, task counts 1/1/1/6/4, false publication flags, no AI endpoint, retained Introduction identity, and absence of identity collisions with Working Draft.
- `canvas_sync.hosted_html.render_hosted_files` rendered six participant pages and course/module navigation using the current remote Canvas state snapshot. The parent ran `browser-check.cjs`, `media-check.cjs`, and `navigation-check.cjs` in the private QA directory with Playwright and installed Chrome. Five activities passed save/reload restoration, choice explanations, copied answers and prompts, instruction-panel visibility, and 390px mobile checks. No page errors or non-GET browser requests occurred.
- Table checks confirmed both four-row tables; the diagram rendered eight nodes. Navigation verified all six module links returned HTTP 200, the Introduction retained its Canvas URL, the V2 homepage remained closed/muted, and the mobile diagram scrolls. The parent visually inspected desktop activity screenshots, mobile tables/diagram/module, and the final Introduction.
- SHA-256 comparisons confirmed all 17 baseline Working Draft/source-evidence and smoke-test files unchanged. Existing homepage entries 0-11 match Git HEAD. `git diff --check` passed.

Worker contributions: the course-drafter authored and reviewed six source-built artifacts and supplied findings; the parent adapted the Introduction, assembled the final seven, reviewed the rendered sequence, and owns this record. The homepage-maintainer updated only homepage metadata. Canvas-inspector supplied read-only inventory and drift findings. Local/browser validation does not establish live deployment behavior; no Canvas submission or grading was tested.

Private reproducibility evidence is under `.source-intake/sprint-one-v4-20260910/qa/`: `unit-tests.log`, `acceptance-results.json`, `browser-results.json`, `media-results.json`, `navigation-results.json`, screenshots, and generated preview. Regenerate into a new private directory with `source_build.py --packet .../source-packet.json --map .../build-map-v2.json --output NEW_DIR`; the source packet/map are private intake, while all final per-artifact evidence is beside the Markdown.

## Canvas publishing and setup handoff

Read-only inspection used remote `canvas-state` commit `bf98db4e30ca6d1fd581a95996a143808c09c27d`, last sync `2026-09-10T18:05:18Z`, plus live Canvas reads. Module 2079 is unpublished. The tracked Introduction is page 3621 / module item 17969 (`introduction-find-the-problem-worth-solving-2`). Its second, untracked Introduction at module item 17967 is preserved. Working Draft module 2078 is published and unchanged. The tracked Introduction and six Working Draft items had no detected drift. This does not cover the untracked duplicate's content.

Before a separately authorized release, refresh live drift and current deployment state. Use the protected publishing workflow for this reviewed artifact set and moved Introduction; keep all V2 content and the module unpublished for setup/review. Do not delete either Introduction or alter Working Draft. Resolve new Canvas IDs from the resulting deployment state rather than guessing. The header should resolve the existing exact-name module, not create another version.

Prepare a dedicated **Own Your Progress** assignment group for the three OYP activities. Set each to zero points and explicitly set `omit_from_final_grade: true`. The inspected course has `apply_assignment_group_weights: false` and only the Assignments group (323), so zero group weight alone is insufficient. Current artifact publishing does not configure these administrative fields; they require separately authorized Canvas setup and readback. No schema, application API, manifest, or runtime extension was introduced for this build.

All five assignments declare `completion_requirement: must_submit`. Preserve `require_sequential_progress: false`, empty prerequisite modules, and no unlock date. The three optional OYP submissions must not lock later work. Keep the concept check a guided text-entry assignment, not a native quiz; instructor-reviewed completion earns its 5 points. The final assignment is one 35-point submission, not four graded assignments. Browser correctness/completion is never a Canvas grade.

When the user authorizes publication, deliberately update the reviewed publication metadata and, if rebuilding source evidence, use the reviewed map with `--publish-ready`; that flag only allows metadata and does not itself publish. Validate the resulting files and use the protected workflow after authorization. Confirm administrative settings and duplicate preservation through live readback before opening V2 on the homepage. No publication approval is implied by this draft record.

## Skills and instruction versions

The parent/course-drafter consulted the following authoring skills. Homepage and inspection workflows were consulted by their respective workers.

- `.agents/skills/writing-to-teach/SKILL.md`: local revision 1.
- `.agents/skills/writing-learning-goals/SKILL.md`: local revision 2.
- `.agents/skills/writing-assignments/SKILL.md`: local revision 1.
- `.agents/skills/reviewing-course-text/SKILL.md`: local revision 2.

Workflow and additional reference SHA-256 fingerprints:

| Path | SHA-256 |
| --- | --- |
| `.agents/skills/build-sprint/SKILL.md` | `e752094a3dee648b9103e637dcb68e4c7964f703c94c3b356122e391dfcdc944` |
| `.agents/skills/inspect-canvas/SKILL.md` | `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404` |
| `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| `.agents/skills/reviewing-course-text/references/review-record.md` | `7f52a9ff5d1fc508e48158e952e4afd83b1a3137e4a33d60a1cb72436c4f23a4` |
| `docs/AUTHORING.md` | `7f1a32b8485bcaebfc38269a985c55d70b4f96e7d07472f3ce01664880077d24` |
| `docs/DOCUMENT_INTAKE.md` | `74151b24aecfbb69eaae4dd386e5be06f773c8439707e04aa825c5308fef8f4a` |

## Reviewed output fingerprints

Computed after final edits, homepage maintenance, validation, and review.

| Path | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.md` | `c67ff212000bbb565b5da97ffc11c5437aef8b9fce66f8f4eead5c4a6faa520e` |
| `course1/sprints/sprint-12/introduction-find-the-problem-worth-solving-v2.sources.json` | `f0ac611f5b237a93c6c2a5d7232040a6ef1657c4181a5c5c1e71a2eb357629b7` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.md` | `d9328ac25e6499fb4af9f809da4a7c4156d882e8266b58235b98760ae8072654` |
| `course1/sprints/sprint-12/sprint-1-concept-check-v2.sources.json` | `b69a2d3d78c24fa37b07f2db6d5e24ed0f64e8b1d6f83865b817461571c50e7f` |
| `course1/sprints/sprint-12/sprint-1-find-the-problem-worth-solving-v2.md` | `534e4cd42a488300935d075f337ac012909d3b9d6a4729254f42c77ca3616ae9` |
| `course1/sprints/sprint-12/sprint-1-find-the-problem-worth-solving-v2.sources.json` | `6b64286de8be44455a3c331d97f7c17d9a2e9aadd8fc205ea9f40501eba3cf45` |
| `course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.md` | `437b117307bb5d4b1102a7e5db67ef7184a79f01507ab80befaf8f7f7a6d12dc` |
| `course1/sprints/sprint-12/start-your-list-and-get-underneath-it-v2.sources.json` | `c58e900eb3223d393d4ff68459f4f57435d6f3d258a9f9fc42c518aa2378145a` |
| `course1/sprints/sprint-12/test-and-commit-v2.md` | `43a701754dd60a35dbcb3238f5009b700cfab066ca48587245527bac45a2b72c` |
| `course1/sprints/sprint-12/test-and-commit-v2.sources.json` | `ccf57acadcb993403ba32177355f619b020693e99860f1ea79b369a78304fe71` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.md` | `bdc285b3f178bd8d7d3e7bebb629af7e4c402268a5c42422c8ed3559090e3dc2` |
| `course1/sprints/sprint-12/things-somebody-handed-you-v2.sources.json` | `8ae0ef7a1a09d7895a3b58ceb5e8f5745242a0964794892dd9fc517b3b11edc5` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.md` | `e2baf6e5af4183b5e8a9d9bf30fb0d372b0716f80af0c73280d2a483a292eea2` |
| `course1/sprints/sprint-12/things-you-stopped-noticing-v2.sources.json` | `ad83e4432727b4cb442668911c9904f45478ace5609959b51c388f6850341e58` |
| `course1/homepage.yaml` | `6d63663e947a7db78ab2dde102e46c87f5f97e0052653475012c1c4325c9911b` |

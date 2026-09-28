# First frames Canvas Walkthrough authoring review

Course 1, Sprint 14 (live Sprint 1 V2), separate replacement draft. The user explicitly authorized implementation and unpublished Canvas staging of this scope. This editorial assessment is the agent's; the final wording has not received human approval. Release remains pending Leslie's revised DOCX.

## Sources and decisions

Reviewed the original `course1/sprints/sprint-14/first-frames.md` and provenance, `the-problem-frame.md`, Get underneath three to five, Dojo, `course1/homepage.yaml`, approved Sprint 1 presentation examples, and `docs/AUTHORING.md` / `docs/AUTHORING_PRESENTATION.md`. The author worker also read the Sprint 12 Test and commit and existing Sprint 16 assumptions examples. Read-only planning context: `course1/design/sprint-1-rework-plan.md`, `sprint-1-working-draft-v1.md`, and `sprint-1-decisions.md`.

The explicit implementation plan combines [Leslie's September 28 direction](https://cs-you-monterey.slack.com/archives/C06DH8365S7/p1790616297317219) and [Sathya's four revisions](https://cs-you-monterey.slack.com/archives/C06DH8365S7/p1790528437936099). The newer design notes propose grids, AI feedback, and a merged teaching page. Those choices conflict with this user's explicit five-response-area, no-AI scope and were not applied. The revised DOCX was not supplied; it is a required release input, not evidence claimed in this draft.

The adaptation keeps three required and two optional seven-part frames, 35 points, no AI, and the existing problem-first drafting order. It removes the separate Candidate Log workflow from this replacement, resolves The problem frame through an artifact link, and repeats complete self-checks below each response. The intended evidence is participants' own problem descriptions, people/costs, handling/failure, improved state, labeled assumptions and consultation targets, unknowns, and shared goal. The 100 non-whitespace-character check is explicitly only a text-length check. Independent artifact identity preserves original draft storage. Word is the sole finish action, with browser draft and text recovery on failure.

The new source sidecar records adaptation rather than verbatim fidelity, preserving original packet/block references and current output hashes. The original source and identity are unchanged. Homepage-maintainer reported no homepage change is appropriate during unpublished review; navigation still points to the published original. Final release must reconcile surrounding Candidate Log references, homepage routing and completion requirements, then verify no submissions before renaming/unpublishing the original after successful replacement publication.

## Findings and measurements

Original body/prompt/criteria source word counts: 456 / 72 / 162. Replacement: 537 / 12 / 975. This is a replacement, not a reduction target: prompt repetition was removed, while fully spelled-out self-checks were deliberately repeated five times. The rendering places each check beneath its response and uses Part headings without a second numbering scheme. No additional findings in this scope after corrections to standalone Part 6 criteria, prerequisite text, and visible points.

## Observed validation

Parent observed:

- `CANVAS_API_URL='' CANVAS_API_TOKEN='' /Users/jeremyshaw/Projects/applying-ai-at-work/.venv/bin/python canvas_sync/schema.py --all`: PASS after final artifact edits, including provenance validation.
- `canvas_sync/link_audit.py --all`: 187 artifacts, 61 links, zero errors.
- `python -m unittest discover`: 313 tests, OK, one optional browser test skipped. That browser test was subsequently run explicitly with `PLAYWRIGHT_MODULE`, `BROWSER_EXECUTABLE`, and bundled Node on PATH: `python -m unittest tests.test_walkthrough_preview_browser -v`, PASS. It covers existing table, text-entry and ungated Word workflows.
- `preview_module.py --manifest course1/manifests/production.json --sprint 14 --output .source-intake/first-frames-20260928/final --baseline .source-intake/first-frames-20260928/before --check-browser` with installed Chrome, bundled Node and Playwright: all ten pages PASS. Includes whitespace-only and 99/100 boundaries, deletion, optional independence, save/reload, export retention, forced export failure/recovery, clearing, desktop/mobile/enlarged text and baseline draft behavior.
- Runtime tests cover non-whitespace Unicode counting, handler guard, independent original storage, storage failure and unchanged ungated behavior. Source checks cover five complete self-checks and no feedback controls.
- Dedicated Chrome and visible Codex right-panel preview inspected. Chrome draft restoration, actual Word download, reference navigation and clear/reload verified. Synthetic local draft cleared. A download-event observer timed out even though Chrome saved the file; the actual downloaded DOCX was parsed and rendered rather than treating that timeout as export failure.
- Downloaded `chrome-first-frames.docx`: all three complete synthetic multiline responses preserved, headings Frame 1 through Frame 5 in order, optional frames blank. Rendered with documents skill and all pages (one) visually inspected: readable, no clipping. Local screenshots show no horizontal overflow at desktop/mobile widths. No coursework submitted. No participant usability study was performed; schema/browser checks do not establish teaching effectiveness.
- Pre-staging live read: original 7151 remains published, unpublishable, no submissions, 35 points, group 323, points grading, unlimited attempts and no dates or overrides. Original item 17979 is fifth in module 2079. Replacement must use live anchor adjacency rather than reset neighbors to local positions. Canvas writes and embedded verification are recorded separately after staging.

Homepage worker reported homepage validation and schema --all PASS with no YAML changes. Original hash remains `5dbffad6acafeeae5282c6ff187fa75a378088bb6e897803052c1f20a2fe5dc7`.

## Skills consulted

Author worker: canvas-author, add-artifact, writing-learning-goals, writing-to-teach, writing-assignments, reviewing-course-text. Homepage worker: maintain-homepage and relevant authoring guidance. Parent: walkthrough workflow, update-artifact, add-artifact, writing-assignments, reviewing-course-text, sync and documents for export inspection. Versions below identify the files actually consulted.

| Skill or reference | Revision or SHA-256 |
| --- | --- |
| `.agents/skills/canvas-author/SKILL.md` | b7f5842af40f231255d8ce4b2bac78e4086fe0f70308a277b2199fde3cd59ca0 |
| `.agents/skills/add-artifact/SKILL.md` | cd588807a2880d5074207e2c1c0f164a0ab0dcb18478ec381c2d7691d967b4c9 |
| `.agents/skills/create-canvas-walkthrough-assignments/SKILL.md` | 380c99712205951c5c826aa7f0ee4c45853c032b11cb0e23dbaf0fce7a857917 |
| `.agents/skills/writing-assignments/SKILL.md` | revision "4" |
| `.agents/skills/writing-to-teach/SKILL.md` | revision "5" |
| `.agents/skills/writing-learning-goals/SKILL.md` | revision "2" |
| `.agents/skills/reviewing-course-text/SKILL.md` | revision "6" |
| `.agents/skills/update-artifact/SKILL.md` | 443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80 |
| `.agents/skills/maintain-homepage/SKILL.md` | 69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7 |
| `.agents/skills/sync/SKILL.md` | 2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b |
| `.agents/skills/reviewing-course-text/references/review-record.md` | 3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e |
| `.agents/skills/create-canvas-walkthrough-assignments/references/live-checks.md` | 9f4130e239bc8426144c34619218408987502f5d7a5e6a5b01f42c6ad2088b18 |
| `/Users/jeremyshaw/.codex/plugins/cache/openai-primary-runtime/documents/26.904.11930/skills/documents/SKILL.md` | 3154ace095b79bace582d7dc53c7744a40f835fe762726220708bde2360749aa |

## Final reviewed output fingerprints

| Output | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-14/first-frames-canvas-walkthrough.md` | cd66c203ac8f0c2b5cf0f022caac1d32af6fad940fe5c6e46d5d81d550bed693 |
| `course1/sprints/sprint-14/first-frames-canvas-walkthrough.sources.json` | 8dde199ccb160d4f23da7ab3b632a5d4c26af411e50e29205f77a02f8bdb547a |
| `canvas_sync/assets/guided-walkthrough.js` | f8523ae0d1c7cac48e5dd9225b9f12417c4d57783e7dedd387478635115ab87f |
| `canvas_sync/walkthrough.py` | a6e604f3aa51a218221709f8479b336236c2ff978ee96d63dac33b87ce5db899 |
| `canvas_sync/schema.py` | 50ba74c16a2ec1793ed5a075d5329694f2cf15d5cbab75cb7da18ccdeea86719 |
| `canvas_sync/module_preview_walkthrough.cjs` | 24248cb7f4f21d553e766cc212e5492c48415bcdc0f462035f248918f93b1163 |
| `schema/frontmatter.schema.json` | 3c022b340168d70a1a68469bbc81303512b4f92415120d41e7227e707052dd79 |
| `tests/test_walkthrough_minimum.py` | 1e4ece06af017387b6f404c97a7958e04ad597905722e07c179b8799ef9e37e6 |
| `tests/walkthrough_minimum_runtime.cjs` | 6c406de0cf83a1290c50b9ccea77afe411ad3b308eba0ed9dc489aabffc31fd2 |
| `docs/AUTHORING_PRESENTATION.md` | 4b6a2176c68476261989bee9c3165354de0845c19a9331b4729c6ed0653e8bf3 |

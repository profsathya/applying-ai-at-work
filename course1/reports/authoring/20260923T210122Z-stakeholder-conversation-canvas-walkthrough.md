# Stakeholder Conversation Canvas Walkthrough: authoring review

## Target and status

Course 1, Sprint 3 V3 in live Canvas course 180. The user selected the Stakeholder Conversation for a single-shot Canvas walk-through conversion and supplied the Stakeholder Validation Report template. This is an unpublished alternative draft, stored in `sprint-16` and anchored after the original. The editorial judgment below is the agent's, not a participant study or human approval of the finished text. Canvas staging and hosted iframe verification are recorded separately after deployment.

## Sources and decisions

The live source is Canvas assignment 7158, module item 17990 in module 2081, at position 7. It is published, 50 points, file upload, with no due or availability dates, rubric, overrides, or submitted work. Four enrollment submission records are unsubmitted. The original stays intact. The new assignment keeps 50 points and file upload and targets the position immediately after the source. The current Google Doc template (`1MUOWS7Y8nMMFu5wWP3_aK2-eGQvvEBUr3yV3d36_Ekw`) was read through the authenticated connector with metadata and all visible tab content; no comments were returned. Its connector view was `PREVIEW_WITHOUT_SUGGESTIONS`, so hidden suggestions are unverified. None were adopted. Private capture, packet, and build map are under `.source-intake/stakeholder-validation-report/`.

The original Canvas text and local `course1/sprints/sprint-15/stakeholder-conversation-v3.md` set the task: prepare three questions, hold a real conversation, record the stakeholder's account, revise or confirm the Problem Frame, and submit three files. The supplied report has four timed sections and six headerless two-column tables. All 22 source rows and 44 cells retain their order and source text. Every right-hand cell is an answer field; accessible column labels were added without a visible invented header row. The prose is an instructional adaptation, not a claim of verbatim preservation. The adjacent Stakeholder Map walkthrough, Dojo Lab, Sprint 3 reflection, and approved Sprint 1 Test and commit page informed the sequence and presentation.

The guided renderer exports the report as DOCX but does not produce the original AI activity's JSON evidence. The new page links to the existing hosted Part 1 AI question exchange solely for that exchange and JSON download, then directs participants back to this Canvas assignment for the same three-file upload: JSON, report, and updated Stakeholder Map. This preserves assessment evidence without changing the original AI activity. Optional row feedback covers question wording, immediate impressions, and the final evidence-based conclusion. Identity, meeting setup, and another person's raw conversation notes have recorded feedback omissions for privacy. Participants write first, can finish without AI, and make the final judgment. No image was needed: the source's six tables provide the working visual structure.

## Review findings

The first meaningful action is to send the ask, as in the original, then prepare questions while waiting. Each report section places its response immediately after the relevant direction. Section B keeps the stakeholder's account separate from the first impressions in C and the judgment in D. A supported no-change conclusion remains valid. The original direct voice, four stakeholder relationships, three/five-day outreach timing, and privacy restrictions remain recognizable. The full page and screenshots were inspected at desktop and mobile widths; the table scroll cue and row-side controls remain visible, and the single finish area points to Canvas submission. The shared opening covers browser draft recovery and durable records. The separate original AI page is an extra navigation step required by the retained JSON evidence; the page explicitly tells participants to return. This remains a workflow limitation, not an assessment change.

Homepage maintenance found no YAML edit needed: the new artifact is unpublished and the published original's curated Sprint 3 entry remains accurate. No unresolved editorial defect was found in this scope. No participant usability testing was performed.

## Observed validation

- `canvas_sync/source_intake.py` captured one Google Doc; `source_build.py` assembled and verified the Markdown and provenance sidecar. All six `walkthrough_tables.compare_task` checks passed for dimensions, source cells, and selected answer cells.
- `.venv/bin/python canvas_sync/schema.py --artifact ...` and `--all`: PASS. `canvas_sync/link_audit.py --all`: 168 artifacts, 58 links, zero errors. `git diff --check`: PASS. Homepage maintainer separately ran `schema.py --homepage course1/homepage.yaml` and `--all`: both PASS.
- `npm test --prefix services/course-ai`: 10 tests passed. With production Canvas environment variables disabled for mock tests, `.venv/bin/python -m unittest discover`: 295 tests ran, 294 passed and one skipped. The existing urllib3 LibreSSL warning does not affect results.
- `preview_module.py --sprint 16 --output .source-intake/stakeholder-validation-report/preview-final --check-browser` used bundled Node/Playwright and Chrome. Both rendered pages had zero browser errors; the new page passed headings, control names, draft save/reload, table shape, row feedback preview/placement, rich and plain copy, Word structure, clipboard-denial fallback, horizontal mobile scrolling, and overflow/enlarged-text checks. The runner marked the live AI endpoint as skipped and the report as `partial`, as designed. Manual inspection of desktop and mobile screenshots found no content clipping or competing panels.
- The actual Chrome **Copy work** button, native Command-V into a signed-in blank Google Doc, and that Doc's DOCX export preserved all six tables, 44 cells, seven headings, blank cells, four synthetic answers, and two multiline answers. Only surrounding whitespace and NBSP padding were normalized. Scratch Doc: `https://docs.google.com/document/d/1-G-zrFjUEPLzv4D4jWNGxm0fm5FiPoGwGMSu88rjmo4/edit`; export SHA-256 `f0f85323a8430feec5dd275a7cf348dbfc0ec24b0cd96f3716ffe94e178bbe41`. The browser account and connector account differ, so native connector readback was unavailable; the browser export supplied the structure check.
- Reviewed registry deployed to `cti-course-ai` production as Netlify deploy `6ab43d3e60d281fded6c9a06`, with the existing model and credentials unchanged. `walkthrough_feedback_check.py --live` returned 3/3 HTTP 200 content responses. The sampled feedback stayed on the selected row, recognized evidence and uncertainty, asked useful revision questions, and did not grade or invent stakeholder facts. Provider behavior remains nondeterministic. A real button on the new production hosted page remains to be checked after GitOps staging.

## Output fingerprints

| Output | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.md` | `f3729ae675349c505589114766dcaa58471ce2a752bc5a200e0f909311c44caf` |
| `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.sources.json` | `dffadddb8b7f722240cdeed3868cf10e38e4d5574ce364a1482f8bf6fd2cc035` |
| `services/course-ai/netlify/functions/walkthrough-guidance.json` | `20369354dfc92c4db6bbd4b43bd47bbabc9882cefdbe4006cbd81c83ecfe0799` |

## Skills consulted

- `create-canvas-walkthrough-assignments` SHA-256 `85a26af647be74e7cca91e93f755784dfb380acac69c41cf19caeb37c1c8aeed`; its `live-checks.md` SHA-256 `b3390a37deb2e5d39fd91c9783c58f7678b57e4909accf91503d09864041da6e`.
- `inspect-canvas` SHA-256 `87abe2d3c73d3c7ee313d75574b5d74c6891e5cfff4f8edf02a9a652e9e45404`; `sync` SHA-256 `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b`.
- `writing-assignments` local revision 4; `writing-to-teach` revision 5; `reviewing-course-text` revision 6. Homepage maintainer additionally consulted `maintain-homepage` (SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`), `writing-learning-goals` revision 2, and the other authoring skills listed above.
- Google Drive skill SHA-256 `dabae8a192c861b76cf7b5742bdf14f8ed35e67d8e6cacfd5f746ffbefd6da5c`; Netlify deploy skill SHA-256 `8d39dd6d03415fcab770a28fba303cf23c995ea7b8be372a9d1587381a912f04`.
- Review-record contract SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.

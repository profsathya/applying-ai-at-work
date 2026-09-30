# Stakeholder Map walkthrough: repeated tables

## Target and status

Course 1, sprint 16, `course1-stakeholder-map-canvas-walkthrough`. This is a presentation revision of Steps 3 to 6 (Stakeholder Tables 1 to 4): one field guide in Step 3, field names only in each table, one shared "What to check in your work" after Step 6, and collapsible steps with Not started, In progress, and Done status. The editorial assessment is the agent's. Human approval of the resulting page was not observed. The user approved the approach: edit the source and the renderer rather than the generated Common-Curriculum HTML.

## Sources and files reviewed

- Read: `AGENTS.md`, `CLAUDE.md`, `docs/AUTHORING.md`, `docs/AUTHORING_PRESENTATION.md` (preview and renderer sections), the target Markdown and its `.sources.json`, `canvas_sync/walkthrough.py`, `canvas_sync/assets/guided-walkthrough.js` and `.css`, `canvas_sync/module_preview_walkthrough.cjs`, and the guided-assignment parts of `canvas_sync/schema.py` and `schema/frontmatter.schema.json`.
- Changed: the target Markdown front matter (the new `guided_assignment.repeated_tables` block only), its evidence map (front matter hash and one `metadata_decisions` line), the renderer, the schema, the validator, the preview checker, a unit test, and two new renderer assets.
- Unavailable: the Common-Curriculum repository. It was not needed, because the hosted page is regenerated from this source.

## Skills consulted

- `.agents/skills/writing-to-teach/SKILL.md`, local revision 5.
- `.agents/skills/reviewing-course-text/references/review-record.md`, SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.

## Decisions and alignment

- Task data is unchanged. `guided_assignment.tasks` still holds each row's question, example, trap, and criteria, and the page reads the new block without adding it to the guided-config JSON. The embedded config, answer keys, AI feedback requests, rich copy, and Word export are therefore identical to the previous build.
- The guide is built from Stakeholder Table 1's rows, so the question, example, and trap text is moved word for word. The validator requires all four tables to keep identical field text, guidance, and criteria.
- Teaching text for Steps 3 to 6 is byte-identical. New participant-facing text is limited to the guide heading and one guide sentence, the shared-check sentence, the "Done, go to next" button, and the status labels. The guide sentence tells participants to reopen Step 3, because the guide is otherwise out of view while they work in later steps.
- Closed panels use `hidden` but stay in the DOM. Open and done state is saved under `course-response:<artifact>:steps` in localStorage, in try/catch like the draft. "Clear this browser draft" also resets that state.

## Findings

- Resolved: the preview checker already failed on this page before the change, because it expected first-column text without the "Ask yourself:" label. The checker now models that label, field-name-only tables, the shared check, and collapsed steps.
- Resolved: at 320px with enlarged text, the status label overflowed the header. On narrow screens it now sits on its own line.
- Deferred: `course1-sprints-sprint-16-what-solutions-already-exist` fails the 320px enlarged-text overflow check. Its rendered HTML is unchanged by this work.
- No participant testing was observed.

## Observed validation

- `.venv/bin/python canvas_sync/schema.py --artifact course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` and `--all`: PASS.
- `.venv/bin/python -m pytest -q tests` with `PLAYWRIGHT_MODULE` and `BROWSER_EXECUTABLE` set: 313 passed, including the Chromium preview test that is otherwise skipped. `node tests/walkthrough_tables_runtime.cjs` and `node tests/guided_assignment_runtime.cjs`: pass.
- `canvas_sync/preview_module.py --manifest course1/manifests/production.json --sprint 16 --check-browser` against a saved baseline: the target page passes every check. Only the target page's HTML changed.
- A targeted Chromium script compared the before and after pages:
  - The guided-config JSON, the existing scripts, and every textarea, id, answer key, and feedback control are identical.
  - The Word `document.xml` is identical when both pages hold the same answers.
  - Only Step 3 starts open. Typing saves the draft and changes the status to In progress. AI feedback enables after writing.
  - "Done, go to next" closes the step, marks it Done, opens the next step, and moves focus to it. Step 6 moves focus to the shared check. Headers respond to Enter and Space.
  - Reload keeps answers, including those in closed steps, and keeps the open and done state. The Word download includes all four tables.
  - With storage blocked, the steps still work. There is no horizontal overflow at 390px, and there were no page errors.
- Desktop and 390px screenshots were inspected. The live AI endpoint and Canvas were not exercised.

## Reviewed output fingerprints

| Path | SHA-256 |
|---|---|
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` | `de8d93ef4282f094c0989565f1c56e980b5bc5f54dba3a13361eb6228e7f9426` |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.sources.json` | `6a19c2ddec465d1ec0751f0ef0a3186948c6da7e9f8e93bb6dd96cf3471a81dd` |
| `canvas_sync/walkthrough.py` | `ef11a3d2a92f060fee3e94986cb3a11eb8d7190eaa24feb43e8bcf02a72c60dc` |
| `canvas_sync/assets/walkthrough-steps.css` | `e49eeaca8507684763b58102c0370be44a8f4b83cb0f8a6d3bbab452d6d5de2a` |
| `canvas_sync/assets/walkthrough-steps.js` | `23642d04dfe57196b68168329c7e53bbf7a1fb00cc88c02dc58447eb2bfb5833` |

# Stakeholder Map walk-through dry run

## Scope and status

This is the agent's editorial review of a **local example** for course1, Sprint 3 (stored as `sprint-15`). The requested workflow and the later table-layout correction were approved for implementation. The human has not approved this particular participant-facing draft for a Canvas course. No Canvas item was created or changed, and no participant testing was observed.

## Sources and files reviewed

- Read-only context: `course1/sprints/sprint-15/stakeholder-map-v3.md`, `course1/sprints/sprint-15/dojo-lab-test-widen-choose-v3.md`, the Brainstorm source and guided pair named in the skill, and the approved Sprint 1 presentation reference `course1/sprints/sprint-12/test-and-commit-v2.md`.
- Linked Google Doc template: [Stakeholder Map TEMPLATE](https://docs.google.com/document/d/1Z0Sg2_2lnQNiryTOpzerdhIovuE4a4-AGivkxR2bRP4). Its four profile tables, confirmed/inferred evidence column, assumption blocks, first-contact choice, and later-use sections informed the example. The example did not inspect the live Canvas assignment or deployment state; the repeatable skill requires that inspection for an actual conversion.
- Reviewed output: `examples/walkthroughs/stakeholder-map-local-dry-run.md`. The renderer, schema, export, release guard, and skill were changed as implementation output. No homepage metadata changed because the example is outside `course1/sprints/`.

## Skills consulted

- `.agents/skills/reviewing-course-text/SKILL.md`, local revision 6; its `references/review-record.md` SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.
- `.agents/skills/create-canvas-walkthrough-assignments/SKILL.md`, SHA-256 `24a4b0e938adde7a8827cb968c018103e96efd998e962af96fb37fd812c71fe8`.
- `/Users/shaw8048/.codex/skills/.system/skill-creator/SKILL.md`, SHA-256 `6656e54755638e8efcf275a472b9672eaa8a9a1b9e59dc210e275b03b59e1e66`.
- `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/google-drive/0.1.16/skills/google-drive/SKILL.md`, SHA-256 `dabae8a192c861b76cf7b5742bdf14f8ed35e67d8e6cacfd5f746ffbefd6da5c`.
- `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/google-drive/0.1.16/skills/google-docs/SKILL.md`, SHA-256 `8e5c26053d800e2980b74ab82c2ce95db94a17fbb443f8f6e30baeb442f1d464`.
- `/Users/shaw8048/.codex/plugins/cache/openai-curated-remote/netlify/1.0.0/skills/netlify-ai-gateway/SKILL.md`, SHA-256 `f5424f5a4eb755c82d27e29bbb57947f32c8afda0a18beed197b603ef1449e0a`.

## Decisions and findings

The participant first maps four real stakeholders independently, distinguishes evidence from inference for each field, identifies two or three assumptions, and chooses a first contact and backup. This preserves the source's 35-point file-upload evidence and its prohibition on AI for the first draft. The later Dojo Lab remains the place to widen the map with AI. The example provides a browser draft, text copy, and a local Word export with the source table structure and later-use headings. The four profiles use three-column tables; the other source table sections use two columns. Expandable row guidance restores the original page's question, example, and common mistake without filling the table with teaching text.

The first rendered version was too visually dense. The human requested tables where the source had tables; this was resolved in the renderer and reviewed on desktop and mobile. This is a source adaptation, not an exact wording transfer. The local example has no AI endpoint, so feedback behavior was inspected with a separate synthetic local sample rather than participant data. No consequential content decision remains for this dry run. An actual conversion still needs live Canvas source and rubric/override inspection, plus human review of the new assignment.

## Observed validation

- `/Users/shaw8048/Projects/applying-ai-at-work/.venv/bin/python canvas_sync/schema.py --all`: PASS. The same Python with `canvas_sync/link_audit.py --all`: 166 artifacts, 57 links, 0 errors.
- The same Python with `-m unittest discover -s tests`: 277 passed. `npm test` in `services/course-ai`: 10 passed. `git diff --check`: clean. Skill quick validator: valid.
- Served and visually inspected the rendered local page in Codex at `http://127.0.0.1:8765/stakeholder-map.html` at desktop and 390 px mobile widths. The mobile table rows stack without horizontal clipping. Checked browser draft reload, copy, Word download, and the generated DOCX package and table structure. No live Canvas publish or release check was run. Schema and visual checks do not establish teaching effectiveness or participant usability.

## Reviewed output fingerprint

- `examples/walkthroughs/stakeholder-map-local-dry-run.md`: SHA-256 `83d4cea12ec50163ed13c68923ccaed7a580c1ef951d585eae7f2c01f24b40f3`.

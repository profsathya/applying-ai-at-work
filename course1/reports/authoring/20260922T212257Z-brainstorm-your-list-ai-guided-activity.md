# Authoring Review: Brainstorm Your List AI-guided Activity

## Target and status

Course 180, standalone Sprint 15 demo item “Brainstorm Your List AI-guided activity.” This is a new interleaved guided-assignment rendering of the existing human-authored activity, approved by the course owner for addition to the live Canvas course. The Canvas item and module remain unpublished, matching the demo's existing visibility. Editorial assessment by the agent; the course owner reviewed and approved the local draft. No participant testing was observed.

## Sources and files reviewed

- Source assignment: `course1/sprints/sprint-14/brainstorm-your-list.md`; its body is preserved byte-for-byte in the new artifact.
- Output: `course1/sprints/sprint-15/brainstorm-your-list-ai-guided-activity.md`.
- Read-only course-style references: six participant pages in `course1/sprints/sprint-12/` (`introduction-find-the-problem-worth-solving-v2.md`, `sprint-1-concept-check-v2.md`, `test-and-commit-v2.md`, `things-you-stopped-noticing-v2.md`, `things-somebody-handed-you-v2.md`, and `start-your-list-and-get-underneath-it-v2.md`), plus the relevant Sprint 0 and Sprint 1 pages.
- Live Canvas identity and deployment state were inspected for the existing module item. The regular Sprint 1 “Brainstorm Your List” assignment is a separate artifact and remains untouched.
- `course1/homepage.yaml` was reviewed. It already defines the Sprint 15 module but does not list this unpublished sandbox item. No curated homepage change was made, so the sandbox does not gain a public course-index link.

## Skills consulted

Existing skills have no `metadata.local_revision`; SHA-256 identifies the consulted bytes.

| Skill or contract | Local path | SHA-256 |
|---|---|---|
| update-artifact | `.agents/skills/update-artifact/SKILL.md` | `443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80` |
| sync | `.agents/skills/sync/SKILL.md` | `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b` |
| writing-assignments | `.agents/skills/writing-assignments/SKILL.md` | `767ad4bbc05b0333c0b95c8ec6632c872b389f403540d0d0794689b48ba0b4c2` |
| reviewing-course-text | `.agents/skills/reviewing-course-text/SKILL.md` | `1614ebaf7e321064f02c7a9041d5443e3c1c45c800a278a0fd54cd539fb7401c` |
| maintain-homepage | `.agents/skills/maintain-homepage/SKILL.md` | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |
| Netlify AI Gateway | `/Users/jeremyshaw/.codex/plugins/cache/openai-curated-remote/netlify/1.0.0/skills/netlify-ai-gateway/SKILL.md` | `f5424f5a4eb755c82d27e29bbb57947f32c8afda0a18beed197b603ef1449e0a` |
| Netlify CLI and deploy | `/Users/jeremyshaw/.codex/plugins/cache/openai-curated-remote/netlify/1.0.0/skills/netlify-cli-and-deploy/SKILL.md` | `dccc4b22dc4a5ddec35a10b93588dd34ecb655a30d6e63e598c1a5e47d0411f0` |
| Authoring review-record contract | `.agents/skills/reviewing-course-text/references/review-record.md` | `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e` |

## Decisions and alignment

The page retains the original three-stage sequence, wording, examples, and long-list guidance. Each Work, Home, or Other example sits in the same response card as the participant's editable list and its contextual feedback control. The optional custom category label is reused consistently in the card, feedback request, saved response, and copied output. The final control copies the assembled list and directs the participant to paste it into the Canvas text-entry assignment. Responses remain browser-local.

The browser sends only the selected activity section, current category label, and participant response (or assembled list) on an explicit feedback request. Assignment context and criteria are fixed server-side. The endpoint uses the current Claude Sonnet model, supplies no tools, rejects unsupported inputs and origins, and treats participant text as untrusted assignment data rather than instructions. Synthetic prompt-steering checks used no learner data. The course owner authorized updating the existing demo item, not changing its unpublished state.

## Findings

No source-content divergence found in this scope. No homepage text change was appropriate because the item is a standalone, unpublished sandbox rather than a curated learner-facing link. Canvas learner visibility remains unchanged; a separate decision would be needed to publish the item/module.

## Observed validation

- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover`: 271 tests passed.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --all`: passed.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/schema.py --homepage course1/homepage.yaml`: passed.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python canvas_sync/link_audit.py --all`: 166 artifacts, 57 links, 0 errors.
- `npm test --prefix services/course-ai`: 7 tests passed; `node --check canvas_sync/assets/brainstorm-interleaved.js`: passed.
- Live `update_artifact.py verify` confirmed the source mapping and immutable Canvas module-item identity for the selected item.
- A direct, read-only Canvas drift check for the selected item returned no drift.
- The filtered publisher dry run selected only this artifact. Dry-run does not perform a live drift check; the separate read-only check above did.
- The body-equality test confirms exact preservation of the human-authored source. `git diff --check` passed.
- The synthetic live endpoint check had previously confirmed the deployed endpoint returns assignment-focused feedback while resisting instruction steering; this did not test a learner session.
- The protected GitHub publishing workflow and Common Curriculum hosted-page deployment have not run yet. No Canvas write is claimed in this record.

## Reviewed output fingerprints

Hashes describe the reviewed bytes at record creation.

| Repository path | SHA-256 |
|---|---|
| `course1/sprints/sprint-15/brainstorm-your-list-ai-guided-activity.md` | `53b89f5ac851084e495566f3188fdb904b60a86ef72dc39da9f83b0ce30a8e99` |
| `course1/reports/authoring/20260922T212257Z-brainstorm-your-list-ai-guided-activity.md` | not hashed into itself |

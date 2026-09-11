# Repeatable module authoring and visual review

Scope: user-authorized updates to the existing authoring workflow, reference material, and reusable local preview checks. Course pages, homepage metadata, renderer presentation rules, assessments, source design inputs, agent routing/configuration, and publication permissions remain unchanged in this pass. Existing uncommitted work was preserved. The user approved the illustrated Sprint 1 direction; that is a design reference, not participant-learning evidence.

## Changes

- `writing-to-teach` local revision 3 → 4: choose a relevant reference pattern, give each image a purpose, reuse suitable assets with provenance, and hand visual briefs from restricted authors to the coordinator. The shared source pin remains `81a051324df61c41af464a0220f8085627729ad9`.
- `reviewing-course-text` revision 4 → 5: use saved preview baselines, interpret actual browser results, and answer the adult-learner questions about next action, useful sections, repeated directions, meaningful visuals/text equivalents, and resuming work. Its upstream pin is unchanged.
- The existing authoring contract now connects authoring, illustration, rendering, inspection, revision, homepage maintenance, and the existing final review record. Exact-wording/date-only boundaries and parent/worker file ownership remain intact.
- The presentation reference maps six Sprint 1 page patterns, supplies an adaptable illustration brief and asset-reuse/credit rules, and documents course-independent preview commands. There is no fixed image, step, example, or word-count requirement.
- `preview_module.py` accepts a manifest, storage sprint, new output directory, optional baseline/local state, and optional browser checks. It validates local inputs, snapshots source/evidence/assets, renders the selected module, and builds a comparison matched by artifact identity. Baselines preserve their original rendered HTML/styles/images. Counts and changed metadata are diagnostics. Named course directories are supported. No Canvas API, AI endpoint, publishing, or source edits are performed.
- The browser helper uses isolated Chromium contexts and a temporary localhost server. It checks local image loading/alternatives, heading order, control names, selected keyboard/focus behavior, overflow, enlarged base text, all guided responses/choices, baseline draft restoration, copying, fallback, and concept feedback. It captures screenshots. Unsupported delivery, external images, missing dependencies, and failures are explicit rather than silently passing.

## Observed verification

- Skill-creator `quick_validate.py` passed for both changed skills; local links passed after excluding fenced examples. Seven agent TOML files parsed successfully, and configuration hashes match the turn-start snapshot.
- `.venv/bin/python canvas_sync/schema.py --all`: PASS. `git diff --check`: PASS. Every snapshotted course1 file remained byte-identical, so homepage maintenance was not applicable to this instruction/tooling-only pass.
- `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover -s tests`: **223 tests passed**. Four new tests cover named-course previews, immutable baseline images/HTML across a slug change, metadata/count reporting, missing image validation, source/output overlap, existing output refusal, wrong-course baselines, unsupported AI delivery, and explicit browser startup failure. Environment overrides isolate existing Canvas URL fixtures; the existing urllib3/LibreSSL warning remains.
- The new CLI with `--check-browser` passed across all six Sprint 1 pages with a saved baseline. A separate run passed across four isolated trial pages. Node/Playwright used the existing bundled runtime and local Chrome, via the documented override options. No dependency was installed.
- A deliberately broken image in a copied preview produced a nonzero browser-check result with an image-load finding. The successful evidence was retained separately.
- The parent inspected the comparison at desktop/mobile widths and representative short-practice, multi-response, and concept-page screenshots. The comparison clearly separates saved/current content, and the trial examples retain immediate actions, adjacent responses, and a readable narrow semantic table. The unchanged Sprint 1 before/current pair is an integration check, not a claimed new course revision.

## Isolated authoring scenarios and limits

The parent authored isolated examples from five recorded requests: a single-response activity, a two-response activity with preserved task IDs, a concept explanation using a semantic comparison, an exact-wording conversion, and a date-only update to the short practice. These yielded two-step single-response practice, two distinct reading-layout responses, a concept table without a submission or raster image, exact retention of the protected two-sentence explanation, and a due-only frontmatter change with identical body and other metadata. All four resulting pages validated and passed the browser checks. Manual inspection then caught an unwanted generic Learning goal panel on the newly authored compact practice. The final trial uses the already supported single-response reading layout, opening directly without fabricated source provenance or a renderer change. The presentation reference now documents this choice. The final trial preview passed again against its saved baseline, and the revised mobile page was visually inspected. These are parent-executed scenarios, not independent-agent or participant evaluations.

Visual usefulness, appropriate image reuse, essential reasoning, reading sequence, actual browser zoom, and screen-reader behavior still require scoped human/agent inspection. Enlarged-base-text automation is explicitly distinguished from full browser zoom. External requests are blocked during QA, so remote image loading and AI feedback are not claimed as tested. The preview records `manual_review: pending` until the separate authoring record supplies the editorial judgment. No claim of participant engagement or learning improvement is made.

Skills read: skill-creator, writing-to-teach, reviewing-course-text, and the existing build-sprint/build-course workflows for integration context. The changes were made in the existing owners; no new skill or competing instruction layer was introduced.

## Reproduction and evidence

The executable examples and dependency options are in `docs/AUTHORING_PRESENTATION.md`, under Module preview and checks. Private evidence is under `.source-intake/repeatable-module-workflow/`: turn-start hashes, before/after/final previews, trial requests and observations, isolated trial sources/preview, separate negative-image check, screenshots, browser JSON/logs, and full test/schema logs. These generated outputs remain outside participant content and version control.

## Reviewed output fingerprints

Validated at 2026-09-11T22:14:18.995719+00:00.

| File | SHA-256 |
| --- | --- |
| `.agents/skills/writing-to-teach/SKILL.md` | `53c1d049c14a1fcfa6ba7edb5e24b52b1ea87fbdefa773ec1ab3c82169ab1f08` |
| `.agents/skills/reviewing-course-text/SKILL.md` | `d678b608d5610c0314bab6276621bcac64cdf44898382b07deed606149626db2` |
| `docs/AUTHORING.md` | `c73410117b4dd313c68ada6fe458e9098e83396eb3cca23277fa0dde1143cac7` |
| `docs/AUTHORING_PRESENTATION.md` | `fd86cdd9a726e34e0e5413eb8a850fa4d7989ff5b0d78eb614344c7f69a02688` |
| `canvas_sync/preview_module.py` | `0c19629562a194392e07c8776e9da912d013f140709f33b6f90ebc023e9367df` |
| `canvas_sync/module_preview_browser.cjs` | `297346c735c96964f277f04904214accd8d2a92b21955ab75e81a7ce9db758d0` |
| `canvas_sync/assets/module-comparison.html` | `1cde259a97c02dac6e637bc86c44b64491527e218afcac9f0de80636a0502e4b` |
| `tests/test_preview_module.py` | `ae906a755562d6786171697275691bcd34a217384568388412b20d9329822337` |

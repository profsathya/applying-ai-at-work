# Authoring and Review

Ordinary authoring requests use the local teaching skills automatically through the existing workflows. These are instruction-only adaptations of Common Curriculum revision `81a0513`, maintained in this repository. Authoring and review need no sibling Common Curriculum checkout. Publishing retains its existing generated-output dependencies and permissions.

## Shared source of guidance

| Skill | Owns |
|---|---|
| [writing-to-teach](../.agents/skills/writing-to-teach/SKILL.md) | Participant knowledge, explanation, examples, application, and reading effort |
| [writing-learning-goals](../.agents/skills/writing-learning-goals/SKILL.md) | Credible capability and value, connected to practice and evidence |
| [writing-assignments](../.agents/skills/writing-assignments/SKILL.md) | Purpose, prior work, tasks, criteria, submission, and useful reflection |
| [reviewing-course-text](../.agents/skills/reviewing-course-text/SKILL.md) | Final editorial review in context and evidence for the saved record |

Read the relevant skills before using them. Workflow and agent instructions link here and to skills instead of copying their teaching principles.

## Scope and source authority

Follow the user's explicit request, the supplied design, and `AGENTS.md` source-authority rules. During build, artifact Markdown is authoritative. For live material, reconcile Canvas-side drift before further local edits using the existing workflow and its permissions. Design inputs in `context/`, `<course>/design/`, and `archive/` remain read-only unless the user explicitly authorizes source changes.

Before substantive authoring, establish the audience, intended capability and value, prior work, and assessment evidence from supplied context and relevant neighboring artifacts. State reasonable assumptions. Surface consequential missing design decisions, such as an unspecified assessment or conflicting deliverable, rather than silently inventing them. Continue independent work where possible. Existing authorization is sufficient for routine improvements within scope; these skills add no approval stage or publishing permission.

Preserve a supplied structure when it serves the design. No skill mandates headings, reflection sections, word counts, or artifact counts. If the request protects exact source wording, preserve it and provide recommendations separately. Flag a conflict with validation requirements rather than silently "correcting" protected text. Preserve existing artifact identity and requested edit scope. Read neighboring material to check dependencies, but do not expand writes into it without authorization.

## Source conversion and instructional adaptation

Determine the mode from the request. Faithful conversion preserves selected source wording and documents mechanical changes. An authorized instructional adaptation may shorten, reorganize, or rewrite source prose while preserving the requested learning and assessment design. Label revised passages as adaptations with reasons and source references; do not claim they are verbatim. Explicit exact-wording constraints still apply. Source design files remain read-only unless separately authorized.

For page structure, visuals, and supported renderer choices, use [the presentation implementation reference](AUTHORING_PRESENTATION.md). It documents an example and current capabilities; the owning skills retain the teaching and review principles.

The asynchronous review evaluates the assembled participant experience, including rendered teaching, prompts, criteria, and navigation. Follow the writing and review skills for this assessment; successful schema or browser checks are not an editorial pass.

## Repeatable module production

For substantive module builds and revisions, the coordinator carries the work through authoring, illustration where useful, rendering, inspection, and revision. Use the [Sprint 1 reference set, illustration brief, and preview commands](AUTHORING_PRESENTATION.md) within the supplied design. For a revision, save a rendered baseline before editing; for new content, begin with the current preview. If a baseline was not saved, state that limitation rather than reconstructing an alleged before version.

The author chooses a suitable presentation and returns any visual needs with the instructional purpose, subject, and placement. Restricted authors keep their existing file boundaries. The coordinator reuses or produces authorized assets, records generation or reuse evidence, integrates Markdown references and provenance, and runs the module preview checks. Image generation follows the available image-generation skill; no specific plugin, external provider, or paid service is required by this contract. Missing generation capability does not justify broken image placeholders or a claim that visuals were completed.

The coordinator inspects the full desktop/mobile sequence using the adult-learner questions in reviewing-course-text, fixes in-scope issues, maintains homepage alignment, completes applicable validation, and saves the existing authoring review record. Deliver the local preview/comparison, actual automated results, manual findings, and unresolved limitations. Publishing remains a separate authorized operation. Exact-wording and mechanical requests retain their existing boundaries.

## Routing and record ownership

| Work | Guidance and handoff |
|---|---|
| Planning a supplied design | `sprint-planner` uses goal discipline to check goal, practice, and evidence; returns gaps without replacing the course design |
| Course or sprint authoring | `course-drafter` follows its build skill, uses relevant shared skills, and reviews the assembled sequence |
| One artifact | `canvas-author` uses relevant shared skills, writes exactly one artifact, validates it, and returns findings |
| Adding one artifact | `add-artifact` coordinates the author, contextual review, homepage maintenance, validation, and saved record |
| Substantive revision | A local path edit follows this contract directly; a live Canvas item uses `update-artifact` to prepare it first. Review the changed content and relevant neighbors |
| Homepage copy | `homepage-maintainer` uses goal and concise-copy guidance, validates only authorized YAML edits, and returns findings |

After artifact additions, edits, or removals, route homepage maintenance when the course has `homepage.yaml`, as required by `AGENTS.md`. The maintainer changes only curated copy made inaccurate by the artifact change. A purely mechanical change may require no copy edit and does not activate a general editorial pass.

For substantive work, the coordinating parent collects worker findings, completes any remaining contextual review with `reviewing-course-text`, runs final applicable validation, and writes [the authoring review record](../.agents/skills/reviewing-course-text/references/review-record.md) under `<course>/reports/authoring/`. A main task doing the authoring itself is also the parent. A delegated course drafter or planner returns its findings within its existing file boundary; the caller owns the record. The parent reports the record path with the result. This applies to substantive homepage-only edits as well as artifact work; one record may cover a whole assembled sprint and its homepage changes.

For a direct local artifact revision, run `python3 canvas_sync/schema.py --artifact <file>` for each changed artifact and `python3 canvas_sync/schema.py --all` after any homepage maintenance. Use the repository virtualenv as described in `AGENTS.md`. Other workflows retain their specific validators. A recommendations-only review reports checks actually performed and fingerprints the unchanged target; it does not imply an edit or successful validation.

Date-only changes, read-only inspection, reconcile, and sync mechanics keep their narrow workflows. They do not trigger a curriculum rewrite or an authoring record unless the user separately requests substantive authoring or editorial review.

## Maintaining the adaptations

Each shared skill records its originating file, full upstream commit, local revision, and intentional adaptations. These are reviewed local copies, not live imports or a claim of Sathya's approval. Course-specific grading, Canvas IDs, HTML conventions, slide systems, private dependencies, and the upstream review script are excluded.

For an upstream update, explicitly compare the pinned source with the proposed revision, assess local fit, update only reviewed guidance, increment the affected skill's `metadata.local_revision`, and update its provenance. Do not automatically copy upstream files. Keep principles in their owning skill and orchestration in the workflow or this contract.

Validate changed skills with the skill-creator validator, parse agent TOML, check local links, and try realistic isolated authoring requests, including source-preservation and non-trigger cases. Mechanical checks complement editorial judgment; neither constitutes human approval or observed participant learning.

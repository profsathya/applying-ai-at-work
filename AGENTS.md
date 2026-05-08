# Applying AI At Work Agent Guide

This is the root guidance file for OpenAI Codex and other repo-aware agents. It also keeps build learnings from earlier course builds. Preserve the `## Learnings` heading because future build workflows may append there.

## Repository Role

This repo builds the "Applying AI at Work" certificate for CTI and De Anza. It has local Canvas LMS course directories such as `course1` and `course2`, and can initialize additional course keys as needed. Course content is authored as canvas-agnostic Markdown, validated locally, then published to Canvas through the deterministic Python sync layer in `canvas_sync/`. Production publishing should flow through the protected GitHub Actions workflow and the `canvas-state` branch.

## Core Principles

1. MD is authoritative during build. Canvas IDs live only in deployment state, never in artifact frontmatter.
2. Canvas wins on drift once a course is live. Reconcile Canvas-side edits back into MD before further local edits.
3. Generate broad course changes locally first, validate them, then ask before Canvas writes.
4. Schema validation is mandatory before any Canvas push.
5. Artifact bodies must remain Canvas-native Markdown. Do not add HTML, iframes, JavaScript, inline styles, or external CDN references.
6. Design docs are read-only build inputs: `context/`, `<course>/design/`, and `archive/`.

## Style Conventions

- No em dashes. Use hyphens, colons, or sentence breaks.
- Use lowercase kebab-case slugs.
- Write for working professionals, not undergraduates. Never address participants as "students."
- Keep CTI framework names internal unless a design doc explicitly says otherwise. Exercise the behavior without naming the framework.
- Ask participants to work with real stakeholders and real work. Do not ask for role-play or simulation.

## File And State Conventions

- Artifact MD: `<course>/sprints/sprint-<n>/<slug>.md`
- Optional course context specs: `context/course-specs/<course>-<slug>.md`
- Optional module context specs: `context/module-specs/<course>-sprint-<n>-<slug>.md`
- Manifest: `<course>/manifests/production.json` for static Canvas course config and legacy local state
- Deployment state branch: `canvas-state`, with files like `<course>/production.json`
- PRD: `<course>/prd.json`
- Progress log: `<course>/progress.md`
- Brief: `briefs/<course>.md`
- Design docs: `<course>/design/`
- Shared design: `context/`

Sprint numbers start at `sprint-0` and extend for however many modules the human requests. Course 1 historically uses `sprint-0` for Week 1 orientation, `sprint-1` through `sprint-4` for the middle 8 weeks, and `sprint-5` for Week 10 capstone.

## Codex Migration Guidance

- Prefer Codex skills in `.agents/skills/` for repeatable workflows.
- Prefer direct Python script calls for validation, Canvas publish, and Canvas pull. Do not wrap deterministic scripts in an LLM worker unless a human asks for analysis.
- Use `.codex/agents/` only for role-specialized LLM work that benefits from a separate context window, especially course drafting, course planning, and artifact authoring.
- The old external orchestration files have been removed. Use `.agents/skills/`, `.codex/agents/`, and the deterministic scripts in `canvas_sync/`.
- Treat Canvas writes as real side effects. For production, prefer merge-to-main publishing through GitHub Actions. For interactive local workflows, validate first and ask for explicit confirmation before running `canvas_sync/push.py` or `canvas_sync/pull.py --apply`.
- Do not run a sandbox or approval bypass for Canvas-writing workflows until it has been explicitly approved for a sandbox course.

## Fresh Session Reading Order

1. `AGENTS.md`
2. `README.md`
3. `README-BUILDER.md`
4. `docs/codex-migration/migration-plan.md`
5. `context/course-specs/` or `context/module-specs/` if building from a human spec
6. `briefs/<target>.md` and the referenced design docs if planning
7. `<course>/progress.md` and `<course>/prd.json` if building or reconciling existing state

## Commit Message Conventions

- `feat: plan <target>, N artifacts queued`
- `build-course: <target>/<course-title>`
- `build: <target>/<artifact-title>`
- `blocked: <artifact-title>`
- `failed: <artifact-title>`
- `feat: <target> build complete`
- `feat: add <artifact-title>`
- `sync: <N> artifact(s) pushed to canvas`
- `chore: pull canvas drift (<target>, <N> artifacts reconciled)`
- `chore: add codex migration scaffold`

## Agent Learnings

This file accumulates patterns, gotchas, and discoveries across course builds. Agents append here when they notice something worth remembering. Future agents and human maintainers read this first.

Keep entries concise. One line per learning. Reference specific files or PRs when useful.

## Build history

- 2026-04-20: course1 build complete. 35 artifacts planned, 33 built across 6 modules in De Anza canvas course 180 (cti-courses.instructure.com). 2 failed on `due_at` format (ids 17, 21) and were left in `failed` state; MD files corrected but PRD not reset (human review required). Wall-clock: ~90 min total including ~25 min of failed attempts while the permission-mode bug was diagnosed. 1 transient provider overload occurred mid-run; one iteration was lost before retry-with-backoff was added to the legacy runner.
- 2026-04-20: PRD written for course1, 35 artifacts across 6 sprints (sprint-0 orientation, sprint-1..4 middle, sprint-5 capstone).

## Learnings

- Canvas pushes are real side effects. Validate locally first, then call `canvas_sync/push.py` only after explicit human approval for the target artifact set.
- Production Canvas publishes should run through `.github/workflows/publish-canvas.yml`, which writes mutable Canvas IDs and hashes to the protected `canvas-state` branch rather than to `main`.
- Prefer the repo virtualenv for deterministic validation and pushes: `.venv/bin/python canvas_sync/schema.py --all` and `.venv/bin/python canvas_sync/push.py --file ...`.
- Transient provider overloads can happen mid-build under load. Retrying the same unit of work with a short backoff is safer than silently advancing build state.
- sprint-planner catches schema bugs when course conventions conflict with JSON schema bounds (e.g., `sprint: minimum: 1` vs. sprint-0 orientation). Trust its relaxations when the conflict is real, verify when it is not.
- Historical timing: planning or complex authoring took 2-5 minutes; typical artifact authoring plus push took 30-90 seconds. A course with about 35 artifacts finished in about 90 minutes once the legacy loop was running cleanly.
- Failed items stay in `failed` state when using PRD-backed workflows. After a build with any failures, a human must decide whether to reset the PRD item to `pending` if the underlying cause has been fixed, or accept the gap and close out.
- Schemas `schema/prd.schema.json` and `schema/frontmatter.schema.json` originally defined `sprint: minimum: 1`, which conflicted with Course 1's orientation at `sprint-0`. Sprint values now allow any non-negative integer so the human can choose the course/module count.
- Canvas's assignment API expects `online_text_entry`/`online_upload` in `submission_types`, not the shortened `text_entry`/`file_upload` we use in frontmatter. Added `CANVAS_SUBMISSION_TYPE_MAP` in `canvas_sync/push.py` to translate on the way out. First assignment push (Choose Your Problem) 400'd before the fix.
- Canvas's `due_at` requires full ISO 8601 with timezone (e.g. `2026-10-15T23:59:00Z`). A bare local datetime like `2026-10-15T23:59` will 400. Course1 assignments to date omit `due` entirely; canvas-author should not invent a `due` field unless the PRD item specifies one. (Synthesize What You Heard id=17 and AI-Fit Analysis id=21 both failed on first push for this reason.)
- 2026-04-22: Added sprint/module builder workflow and `/build-sprint`. It fills the gap between `/add-artifact` (one artifact) and a full course build: given a context doc + target course + sprint number, the agent reads every built sprint in the target course, infers the scaffolding (artifact count, type mix, rubric pattern, voice), and produces 4-6 coherent MD files. High-reasoning authoring is load-bearing here: authoring a coherent 6-artifact set with aligned rubrics and pacing is design work, not mechanical composition. Smoke tests confirmed three behaviors: matches course1's 1/1/3/1 skeleton when context doc is silent; falls back to course1 inference with an explicit caveat when course2/sprints/ is empty; follows the context doc over the inferred pattern when they disagree (4-artifact, no-peer-discussion shape).
- 2026-04-22: Orientation Check (canvas_id 2912) showed "This question was imported from an external source. It was a 'true_false' question, which is not supported in this quiz tool." banners on every question when viewed in New Quizzes. Three compounding bugs in `canvas_sync/push.py`: (1) `question_type` was sent as our short names (`multiple_choice`, `true_false`, `short_answer`), but Canvas Classic Quiz API requires the `_question` suffix (`multiple_choice_question`, etc.). Unrecognized values got stored and NQ's display layer flagged them as unsupported. (2) Answers payload was only built for `multiple_choice`; `true_false` never got its answer structure. (3) On update, questions were appended rather than replaced, so earlier broken pushes accumulated. Fixed by adding `list_quiz_questions` + `delete_quiz_question` to `canvas_client.py`, and updating `push_quiz` to wipe existing questions on update and map all four schema types to full Canvas names. If the error reappears, check whether the institution is using New Quizzes as the backend (not just display) - that would require `/api/quiz/v1/...` endpoints, not the Classic API we use.

# Applying AI At Work Agent Guide

This is the root guidance file for OpenAI Codex and other repo-aware agents. It also keeps the build learnings that earlier Ralph and Claude runs appended over time. Preserve the `## Learnings` heading because existing build prompts may still append there while Claude compatibility is retained.

## Repository Role

This repo builds the "Applying AI at Work" certificate for CTI and De Anza. It has two canvas-LMS courses, `course1` and `course2`. Course content is authored as canvas-agnostic Markdown, validated locally, then pushed to Canvas through the deterministic Python sync layer in `canvas_sync/`.

## Core Principles

1. MD is authoritative during build. Canvas IDs live only in manifests, never in artifact frontmatter.
2. Canvas wins on drift once a course is live. Reconcile Canvas-side edits back into MD before further local edits.
3. One artifact per autonomous BUILD iteration. Predictable failures are easier to recover than broad partial changes.
4. Schema validation is mandatory before any Canvas push.
5. Artifact bodies must remain Canvas-native Markdown. Do not add HTML, iframes, JavaScript, inline styles, or external CDN references.
6. Design docs are read-only build inputs: `context/`, `course1/design/`, `course2/design/`, and `archive/`.

## Style Conventions

- No em dashes. Use hyphens, colons, or sentence breaks.
- Use lowercase kebab-case slugs.
- Write for working professionals, not undergraduates. Never address participants as "students."
- Keep CTI framework names internal unless a design doc explicitly says otherwise. Exercise the behavior without naming the framework.
- Ask participants to work with real stakeholders and real work. Do not ask for role-play or simulation.

## File And State Conventions

- Artifact MD: `course<N>/sprints/sprint-<n>/<slug>.md`
- Manifest: `course<N>/manifests/production.json`
- PRD: `course<N>/prd.json`
- Progress log: `course<N>/progress.md`
- Brief: `briefs/course<N>.md`
- Design docs: `course<N>/design/`
- Shared design: `context/`

Sprint numbers are `sprint-0` for Week 1 orientation, `sprint-1` through `sprint-4` for the middle 8 weeks, and `sprint-5` for Week 10 capstone.

## Codex Migration Guidance

- Prefer Codex skills in `.agents/skills/` for repeatable workflows.
- Prefer direct Python script calls for validation, Canvas push, and Canvas pull. Do not wrap deterministic scripts in an LLM worker unless a human asks for analysis.
- Use `.codex/agents/` only for role-specialized LLM work that benefits from a separate context window, especially course planning and artifact authoring.
- The legacy Claude orchestration files have been removed. Use `codex-ralph.sh`, `.agents/skills/`, `.codex/agents/`, and `prompts/codex/ralph-prompt.md`.
- Treat Canvas writes as real side effects. For interactive workflows, validate first and ask for explicit confirmation before running `canvas_sync/push.py` or `canvas_sync/pull.py --apply`.
- Do not run a sandbox or approval bypass for Canvas-writing workflows until it has been explicitly approved for a sandbox course.

## Fresh Session Reading Order

1. `AGENTS.md`
2. `README.md`
3. `README-BUILDER.md`
4. `docs/codex-migration/migration-plan.md`
5. `prompts/codex/ralph-prompt.md` if working on the Codex Ralph loop
6. `briefs/<target>.md` and the referenced design docs if planning
7. `course<N>/progress.md` and `course<N>/prd.json` if building or reconciling

## Commit Message Conventions

- `feat: plan <target>, N artifacts queued`
- `build: <target>/<artifact-title>`
- `blocked: <artifact-title>`
- `failed: <artifact-title>`
- `feat: <target> build complete`
- `feat: add <artifact-title>`
- `sync: <N> artifact(s) pushed to canvas`
- `chore: pull canvas drift (<target>, <N> artifacts reconciled)`
- `chore: add codex migration scaffold`

## Agent Learnings

This file accumulates patterns, gotchas, and discoveries across course builds. Subagents append here during BUILD when they notice something worth remembering. Future Ralph iterations and future human maintainers read this first.

Keep entries concise. One line per learning. Reference specific files or PRs when useful.

## Build history

The following entries include legacy Claude-era build notes. They are retained as postmortem context, not as current operating instructions.

- 2026-04-20: course1 build complete. 35 artifacts planned, 33 built across 6 modules in De Anza canvas course 180 (cti-courses.instructure.com). 2 failed on `due_at` format (ids 17, 21) and were left in `failed` state; MD files corrected but PRD not reset (human review required). Wall-clock: ~90 min total including ~25 min of failed attempts while the permission-mode bug was diagnosed. 1 transient Anthropic API overload mid-run (iteration 3 of successful run); lost one iteration before retry-with-backoff was added to `ralph.sh`.
- 2026-04-20: PRD written for course1, 35 artifacts across 6 sprints (sprint-0 orientation, sprint-1..4 middle, sprint-5 capstone).

## Learnings

- `--permission-mode bypassPermissions` is required for autonomous bash calls from subagents. `acceptEdits` only covers file edits; it does not authorize Bash tools and leaves every `python3 canvas_sync/push.py` prompting for approval. The first two course1 loop attempts burned ~25 min on this before the flag was corrected in `ralph.sh`.
- Subagents invoke Python as `python3`, not `python`. `.claude/settings.json` must allowlist both forms (`Bash(python canvas_sync/*.py:*)` AND `Bash(python3 canvas_sync/*.py:*)`), plus `python -m` / `python3 -m` for module-style invocation.
- Transient Anthropic API overloads (`"type":"overloaded_error"`) happen mid-run under load. `ralph.sh` now retries the same iteration up to 3 times with a 30s backoff rather than silent-ticking the counter.
- sprint-planner catches schema bugs when CLAUDE.md conventions conflict with JSON schema bounds (e.g., `sprint: minimum: 1` vs. sprint-0 orientation). Trust its relaxations when the conflict is real, verify when it is not.
- Iteration timing: iteration 1 runs opus (2-5 min, PLAN or complex BUILD). Typical BUILD iterations are 30-90 seconds (sonnet author + haiku push). A course with ~35 artifacts finishes in about 90 minutes once the loop is running cleanly.
- Failed items stay in `failed` state; the loop does not auto-retry. After a build with any failures, a human must decide whether to reset the PRD item to `pending` (if the underlying cause has been fixed) or accept the gap and close out.
- Schemas `schema/prd.schema.json` and `schema/frontmatter.schema.json` originally defined `sprint: minimum: 1`, which conflicted with the CLAUDE.md convention that orientation is `sprint-0` and capstone is `sprint-5`. Relaxed to `minimum: 0, maximum: 5` during course1 planning.
- Canvas's assignment API expects `online_text_entry`/`online_upload` in `submission_types`, not the shortened `text_entry`/`file_upload` we use in frontmatter. Added `CANVAS_SUBMISSION_TYPE_MAP` in `canvas_sync/push.py` to translate on the way out. First assignment push (Choose Your Problem) 400'd before the fix.
- Canvas's `due_at` requires full ISO 8601 with timezone (e.g. `2026-10-15T23:59:00Z`). A bare local datetime like `2026-10-15T23:59` will 400. Course1 assignments to date omit `due` entirely; canvas-author should not invent a `due` field unless the PRD item specifies one. (Synthesize What You Heard id=17 and AI-Fit Analysis id=21 both failed on first push for this reason.)
- 2026-04-22: Added `sprint-module-builder` (opus) and `/build-sprint`. Fills the gap between `/add-artifact` (one artifact) and a full course re-plan: given a context doc + target course + sprint number, the agent reads every built sprint in the target course, infers the scaffolding (artifact count, type mix, rubric pattern, voice), and produces 4-6 coherent MD files. Opus is load-bearing: authoring a coherent 6-artifact set with aligned rubrics and pacing is design work, not mechanical composition. Smoke tests confirmed three behaviors: matches course1's 1/1/3/1 skeleton when context doc is silent; falls back to course1 inference with an explicit caveat when course2/sprints/ is empty; follows the context doc over the inferred pattern when they disagree (4-artifact, no-peer-discussion shape).
- 2026-04-22: Project `.claude/settings.json` had a broad `Bash(rm -rf:*)` deny that blocked even scoped cleanups. Narrowed to path-specific denies (`/`, `~`, `$HOME`, `..`, `.`, `*`) and added scoped allows (`course*/sprints/sprint-*`, `/tmp/smoke-test-*`, `/tmp/test-sprint-*`). Deny still takes precedence over allow across all settings files, so you can't override a broad deny with a narrower allow in `settings.local.json`; you have to narrow the deny itself.
- 2026-04-22: Orientation Check (canvas_id 2912) showed "This question was imported from an external source. It was a 'true_false' question, which is not supported in this quiz tool." banners on every question when viewed in New Quizzes. Three compounding bugs in `canvas_sync/push.py`: (1) `question_type` was sent as our short names (`multiple_choice`, `true_false`, `short_answer`), but Canvas Classic Quiz API requires the `_question` suffix (`multiple_choice_question`, etc.). Unrecognized values got stored and NQ's display layer flagged them as unsupported. (2) Answers payload was only built for `multiple_choice`; `true_false` never got its answer structure. (3) On update, questions were appended rather than replaced, so earlier broken pushes accumulated. Fixed by adding `list_quiz_questions` + `delete_quiz_question` to `canvas_client.py`, and updating `push_quiz` to wipe existing questions on update and map all four schema types to full Canvas names. If the error reappears, check whether the institution is using New Quizzes as the backend (not just display) - that would require `/api/quiz/v1/...` endpoints, not the Classic API we use.

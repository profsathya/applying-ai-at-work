# Project Conventions

This repo is the "Applying AI at Work" certificate (CTI + De Anza). It builds two canvas-LMS courses (`course1` and `course2`) from canvas-agnostic markdown using a Ralph-loop pipeline. Per-course manifests map MD files to canvas IDs.

## Core principles

1. **MD is authoritative during build.** Canvas IDs live only in manifests, never in MD frontmatter.
2. **Canvas wins on drift.** Once the course is live, direct canvas edits take precedence. `/reconcile` pulls them back into MD.
3. **One artifact per BUILD iteration.** Each Ralph loop iteration does exactly one unit of work.
4. **Schema validation is non-negotiable.** Nothing pushes to canvas without passing `schema-validator`.
5. **No HTML in MD.** Artifact bodies are canvas-native markdown. HTML conversion happens at push time only.
6. **Design docs are read-only during build.** `context/`, `course1/design/`, `course2/design/`, and `archive/` are authoritative inputs the builder reads but never modifies.

## Style conventions

- **No em dashes.** Use hyphens, colons, or sentence breaks. This is enforced by `schema-validator`.
- **Lowercase slugs, kebab-case.** `gap-statement`, not `GapStatement` or `gap_statement`.
- **Working-professional voice.** Direct, respects time, assumes professional judgment. Never address as "students."
- **Frameworks-present-not-labeled.** CTI framework terms (Slow Down, Know Yourself, SDL, IS, AB, Superagency, HVP, 3Cs, UMPIRE, DIKW) are internal vocabulary, not participant-facing. Exercise them through design, not by naming them.

## File naming

- Artifact MD: `course<N>/sprints/sprint-<n>/<slug>.md`
- Manifest: `course<N>/manifests/production.json`
- PRD: `course<N>/prd.json`
- Progress log: `course<N>/progress.md`
- Briefs: `briefs/course<N>.md`
- Design docs: `course<N>/design/`
- Shared design: `context/`

Sprint numbers: `sprint-0` for Week 1 orientation, `sprint-1` through `sprint-4` for the middle 8 weeks, `sprint-5` for Week 10 capstone.

## Commit message conventions

- `feat: plan <target>, N artifacts queued`
- `build: <target>/<artifact-title>`
- `blocked: <artifact-title>` (validation failure)
- `failed: <artifact-title>` (canvas API failure)
- `feat: <target> build complete`
- `feat: add <artifact-title>` (mid-semester additions)
- `sync: <N> artifact(s) pushed to canvas`
- `chore: pull canvas drift (<target>, <N> artifacts reconciled)`

## Subagent conventions

Subagents run in isolated context windows. Each one:

- Has a narrow, documented job
- Is restricted to the tools it actually needs
- Uses the cheapest model that can do the job reliably (haiku for mechanical, sonnet for authoring, opus for planning)
- Never retries (retry logic lives in the Ralph loop or in the slash command)
- Never invokes other subagents (subagents can't spawn subagents)
- Never modifies design docs (`context/`, `course*/design/`, `archive/`)

## Reading order for a fresh Claude Code session

1. This file
2. `README.md` (builder + teammate usage, first-read overview)
3. `README-BUILDER.md` (deep-dive technical reference)
4. `prompts/ralph-prompt.md` (the loop prompt)
5. `AGENTS.md` (accumulated learnings from prior builds)
6. `briefs/<target>.md` and the referenced design docs (if planning)
7. `course<N>/progress.md` (most recent course, if building)

## Audience

This certificate serves working professionals, not undergraduates. See `context/audience.md`. Course mechanics assume participants have real jobs, real stakeholders, and existing institutional knowledge. Never ask them to pretend or simulate what they can do for real.

## Known issues and gotchas

For anyone modifying the scaffold itself (as distinct from operators running it; operator-facing gotchas live in `README.md`).

- **Settings.json requires both `python` and `python3` matcher forms.** Subagent prompts sometimes invoke `python` and sometimes `python3`. If the allowlist has only one form, pushes stall. Always keep both `Bash(python canvas_sync/*.py:*)` AND `Bash(python3 canvas_sync/*.py:*)`, plus the `-m` module variants.
- **Hook references must point to real scripts.** An earlier scaffold referenced `./scripts/guard-manifest-writes.sh` as a PreToolUse hook without the script ever being written. The hook block has since been removed from settings.json. If you add hooks back, verify every referenced script exists and is executable before committing.
- **`--permission-mode bypassPermissions` is what `ralph.sh` uses, not `acceptEdits`.** `acceptEdits` only authorizes file edits; Bash tools will still prompt for approval, which deadlocks the loop because there is no human present. If you modify `ralph.sh`, keep this flag.
- **Overloaded API errors.** `ralph.sh` retries the same iteration up to 3 consecutive times with a 30s backoff on `"type":"overloaded_error"` or `"message":"Overloaded"`. Repeated overloads past that threshold mean waiting, not raising the retry cap. State is safe to re-run.
- **`course<N>/prd.json` and `course<N>/manifests/*.json` are generated.** Don't hand-edit. Edit the design docs and re-plan, or use `/sync` / `/reconcile` to drive state changes through the pipeline.
- **`course<N>/design/` is authoritative input; `course<N>/sprints/` and `course<N>/manifests/` are generated output.** The builder reads design, writes sprints and manifests. This directionality is a core invariant — the scaffold should never write into `design/`.

## What Jeremy cares about

- Honest, direct feedback over reassurance.
- Directive guidance, not general advice.
- Minimal over-explanation.
- Superagency as a design principle: AI amplifies human capability, doesn't replace it. The instructor stays in the loop.

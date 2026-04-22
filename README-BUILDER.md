# Canvas Course Builder — Technical Reference

Deep-dive reference for the builder itself. The top-level `README.md` is the first-read doc for anyone using the repo (operators, teammates, new hires). Read that first; come here when you need to modify the scaffold, debug the pipeline, or understand architectural choices.

This builder supersedes the legacy iframe pattern. See `archive/legacy-iframe-template/WHY-ARCHIVED.md`.

## Pipeline at a glance

```
design docs (context/, course<N>/design/) --> sprint-planner --> prd.json
                                                                    |
                                                                    v
prd.json --> canvas-author --> MD file --> schema-validator --> canvas-pusher --> Canvas API
                                                                    |
                                                                    v
                                                          course<N>/manifests/production.json
```

- **MD is authoritative during build.** Canvas IDs live only in manifests, never in MD frontmatter.
- **Canvas wins on drift.** Once the course is live, direct canvas edits take precedence. `/reconcile` pulls them back.
- **One artifact per BUILD iteration.** Ralph's determinism: predictable failures beat unpredictable successes.
- **Schema validator is a hard gate.** Catching errors before canvas is cheap; catching them from confused participants a week later is expensive.
- **No HTML in MD.** Markdown stays portable; canvas-flavored HTML is a conversion concern handled at push time only.

## One-time setup (first install in this repo)

Most users can follow `README.md`'s Quick Start. The full sequence, including the migration step that was run once at repo adoption:

1. Unzip the builder scaffold on top of the repo.
2. Run `./migrate.sh` from the repo root (idempotent). This moves design docs into `course<N>/design/`, archives the legacy template, and writes a decision-log entry.
3. Review and commit.
4. `python3 -m venv .venv && source .venv/bin/activate && pip install -r canvas_sync/requirements.txt`.
5. `npm install -g @anthropic-ai/claude-code` if not already installed.
6. Create two empty canvas course shells in De Anza's instance (one per course). Note their course IDs.
7. `cp .env.example .env` and fill in `CANVAS_API_URL`, `CANVAS_API_TOKEN`, `COURSE1_CANVAS_ID`, `COURSE2_CANVAS_ID`.
8. Smoke test: `DEFAULT_COURSE_ID=<id> python canvas_sync/canvas_client.py`. Should print `Connected to course <id>. Found N modules.`

## The Ralph loop

`ralph.sh` is the driver for initial course builds. It repeatedly calls `claude -p` with `prompts/ralph-prompt.md` until the course is fully in canvas (the model emits `<promise>COURSE_COMPLETE</promise>`) or a HALT condition fires.

Key mechanics:

- **Permission mode.** The loop uses `--permission-mode bypassPermissions`. This authorizes Bash tools non-interactively; `acceptEdits` only covers file edits and will stall subagent push attempts.
- **Allowlist.** `.claude/settings.json` allowlists `python` and `python3` canvas_sync calls (both direct script and `-m` module-style invocation). Both forms are required because some subagent prompts call `python3` explicitly.
- **Overload retry.** Transient `overloaded_error` responses from the Anthropic API trigger a 30s backoff and retry of the same iteration, capped at 3 consecutive retries before the counter advances normally.
- **Halt signals.** Any `<promise>HALT: ...</promise>` exits the loop with code 1. Used when a failed artifact requires human review.
- **Iteration budget.** Default `MAX_ITERATIONS=100`, overridable via env var. A 35-artifact course finishes in ~35-40 iterations plus planning and verification.

Iteration timing (observed on course1):

- Iteration 1: 2-5 minutes (opus planning, or opus-level judgment on complex builds).
- Typical BUILD iterations: 30-90 seconds (sonnet authoring + haiku push).

## Subagents

Six narrow subagents, each in its own context window. Defined in `.claude/agents/`.

- `sprint-planner` (opus) — reads design docs, writes `course<N>/prd.json` and initializes the manifest. Runs once at start of build.
- `canvas-author` (sonnet) — writes one MD artifact per iteration. Has no canvas access.
- `schema-validator` (haiku) — validates frontmatter + manifest + PRD against the JSON schemas in `schema/`.
- `canvas-pusher` (haiku) — runs `canvas_sync/push.py`, updates the manifest with the canvas ID.
- `canvas-puller` (haiku) — only invoked by `/reconcile`. Diffs canvas state against MD and writes canvas changes back to MD.
- `due-date-updater` (sonnet) — only invoked by `/update-dues`. Updates the `due` field in one or more artifact MD files from NLP, a slug-to-date mapping file, or a path plus date. Normalizes to `YYYY-MM-DDTHH:MM:SSZ`. No canvas access.

Rules subagents must obey (enforced by their prompts):

- Narrow, documented job.
- Restricted to the tools they need.
- Cheapest model that can do the job reliably.
- Never retry; retry logic lives in the Ralph loop or slash command.
- Never spawn other subagents.
- Never modify design docs (`context/`, `course*/design/`, `archive/`).

## Slash commands

Four slash commands in `.claude/commands/`. These are for day-to-day work after the initial build. The top-level `README.md` covers operator usage; the internals:

- `/add-artifact` — natural language in, one new MD file + schema validation + push + manifest update + commit out.
- `/sync` — push an already-authored MD file to canvas. Used after hand-editing.
- `/reconcile` — pull canvas drift back into MD. Canvas wins. Shows the diff and asks before applying.
- `/update-dues` — change the `due` field on one or many artifacts. Accepts a file path plus ISO date, `--from <mapping-file>` (YAML or markdown table keyed by slug or path), or a natural-language description. Invokes `due-date-updater`, then `schema-validator`, then asks before pushing via `canvas-pusher`.

## Schemas

`schema/` holds three JSON schemas that the validator enforces:

- `frontmatter.schema.json` — artifact-level YAML frontmatter. Defines type (assignment, page, discussion, quiz, module_header), sprint bounds (0-5, matching the `sprint-0` orientation and `sprint-5` capstone convention), submission types, etc.
- `manifest.schema.json` — the per-course manifest structure. Canvas IDs are scoped here; no canvas IDs in artifact frontmatter.
- `prd.schema.json` — the PRD the planner produces. Sprint numbers align with the frontmatter schema.

**No em dashes.** The validator flags them in any text field. Use hyphens, colons, or sentence breaks.

## Canvas sync layer

`canvas_sync/` is hand-authored Python (not generated). Three pieces:

- `canvas_client.py` — thin wrapper over the Canvas REST API with auth.
- `push.py` — reads an MD file, converts to canvas-flavored HTML, creates or updates the artifact, attaches to the correct module, writes the canvas ID back to the manifest. Honors `CANVAS_SUBMISSION_TYPE_MAP` for frontmatter→API translation (e.g., `text_entry` → `online_text_entry`).
- `pull.py` — reads canvas state and produces an MD representation for diffing during `/reconcile`.

Canvas quirks captured in push.py:

- `submission_types` API expects `online_text_entry` / `online_upload`, not the shortened `text_entry` / `file_upload` we use in frontmatter. Mapped in the push layer.
- `due_at` requires full ISO 8601 with timezone (`2026-10-15T23:59:00Z`). Bare local datetimes fail. Let `canvas-author` omit the `due` field unless the PRD item specifies one. To change or add dues after the initial build, use `/update-dues` rather than hand-editing frontmatter; the agent normalizes any malformed values it encounters.

## Grading

Lives in `n8n/`, separate from the build runtime. See `n8n/README.md`. Flow: canvas submission webhook → Claude API with SRL-grounded feedback prompt → HITL review queue (Google Sheet or n8n human-approval node) → instructor approves → grade posted to canvas → audit log.

## Troubleshooting

**Push blocked by permission system.** The classic first-build blocker. See `README.md`'s Gotchas section. Check `.claude/settings.json` has both `python` and `python3` canvas_sync entries, and that `ralph.sh` uses `--permission-mode bypassPermissions`.

**Migration complains about missing files.** `migrate.sh` is idempotent but expects the base repo structure. Run from the repo root; `context/decision-log.md` must exist.

**Loop halts with "scaffold incomplete".** Unzip didn't complete, or a file was accidentally deleted. Check the error, restore, rerun.

**Loop halts with "planner produced invalid PRD".** Read `course<N>/progress.md` for schema errors. Delete the PRD and rerun to let the planner retry.

**Canvas push 401.** Token is invalid or lacks scope. Regenerate.

**Canvas push 404.** Wrong `course_id` in `.env`. Verify in the canvas URL.

**Canvas push 400 on `due_at`.** Bare local datetime; must be full ISO 8601 with timezone, or omitted entirely.

**Artifact landed in wrong module.** The planner produced a module name that doesn't match what you expected. Check the PRD item's `module` field and edit if needed, then rerun `/sync` on that file.

**Failed items stay failed.** The loop does not auto-retry items with `status: "failed"`. After a build with any failures, a human must decide to reset the item to `pending` (if the underlying cause is fixed) or accept the gap.

**Repeated overloaded_errors.** The loop retries up to 3 times. Beyond that, stop and come back later rather than raising the cap; state is safe to re-run.

## Design rationale

See `context/design-principles.md` for the pedagogical principles and `context/decision-log.md` for the builder-adoption decision. Summary of the technical choices:

- **Canvas-agnostic MD is the source of truth.** Canvas IDs live only in manifests so the same content can be pushed to multiple shells (sandbox, production, cloning to a new term).
- **Canvas wins on drift.** Once live, direct canvas edits take precedence. `/reconcile` pulls them back.
- **One artifact per BUILD iteration.** Predictable failures beat unpredictable successes.
- **Schema validator is a hard gate.** Catching errors before canvas is cheap.
- **No HTML in MD.** Markdown stays portable; canvas-flavored HTML is a conversion concern, not a content concern.
- **Frameworks present, not labeled.** Participants experience the frameworks; they do not memorize them. The schema validator does not enforce this, but the subagent prompts do.

## See also

- `README.md` — first-read doc (operator + teammate usage)
- `CLAUDE.md` — project conventions
- `AGENTS.md` — accumulated learnings across builds
- `context/build-notes/` — post-build reports per course
- `prompts/ralph-prompt.md` — the system prompt every loop iteration sees

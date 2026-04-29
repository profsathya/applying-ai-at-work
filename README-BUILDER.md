# Canvas Course Builder Technical Reference

This is the deep-dive reference for the builder. The top-level `README.md` is the first-read operator guide.

The builder supersedes the legacy iframe pattern in `archive/legacy-iframe-template/`.

## Pipeline

```text
design docs (context/, course<N>/design/) -> sprint-planner -> prd.json
                                                                   |
                                                                   v
prd.json -> canvas-author -> MD file -> schema validation -> push.py -> Canvas API
                                                                   |
                                                                   v
                                                        course<N>/manifests/production.json
```

Core invariants:

- MD is authoritative during build.
- Canvas IDs live only in manifests.
- Canvas wins on live-course drift.
- Schema validation is a hard gate before Canvas writes.
- Artifact bodies stay Canvas-native Markdown.
- `context/`, `course*/design/`, and `archive/` are read-only build inputs.

## Codex Orchestration

Codex is the supported orchestration layer.

- `AGENTS.md` - root Codex guidance, repo conventions, and accumulated build learnings.
- `.agents/skills/` - reusable workflows for daily operations and build tasks.
- `.codex/agents/` - specialized planner and author agents.
- `prompts/codex/ralph-prompt.md` - Codex Ralph loop prompt.
- `codex-ralph.sh` - autonomous loop runner.

Mechanical operations should call Python scripts directly. Do not reintroduce LLM wrappers around validation, push, or pull unless there is a concrete reason.

## One-Time Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
npm i -g @openai/codex
cp .env.example .env
```

Fill in Canvas credentials and course IDs in `.env`.

Smoke test:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=$COURSE1_CANVAS_ID python canvas_sync/canvas_client.py
```

## Codex Ralph Loop

`codex-ralph.sh` is the driver for initial course builds. It repeatedly calls `codex exec` with `prompts/codex/ralph-prompt.md` until the model emits `<promise>COURSE_COMPLETE</promise>`, emits a `HALT`, or reaches `MAX_ITERATIONS`.

Key mechanics:

- **Fresh context:** each iteration starts from repository files.
- **One unit of work:** BUILD handles exactly one pending PRD item.
- **State:** PRD, progress log, manifest, git commits, and `AGENTS.md` learnings.
- **Failure:** failed Canvas pushes are not retried in the same iteration.
- **Safety:** do not use dangerous Codex bypass modes against production Canvas without an explicit sandbox-proven approval policy.

Run:

```bash
TARGET_COURSE=course2 ./codex-ralph.sh --verbose
```

Useful environment variables:

- `TARGET_COURSE`: `course1` or `course2`.
- `MAX_ITERATIONS`: default `100`.
- `CODEX_RALPH_ARGS`: overrides the default `codex exec` arguments.

## Skills

Codex skills live in `.agents/skills/`.

- `sync` - validate and push one or more existing artifact MD files.
- `add-artifact` - add one new artifact from a natural-language request.
- `build-sprint` - generate one sprint from a context document, validate, then optionally push after review.
- `update-dues` - edit `due` fields, validate, and optionally push.
- `reconcile` - dry-run Canvas drift, then optionally apply Canvas changes locally.
- `ralph-build-loop` - run or maintain the autonomous loop.
- `canvas-author` - write exactly one artifact from a PRD-shaped item.
- `sprint-planner` - decompose course design into PRD, metadata, progress log, and manifest.

## Custom Agents

Codex custom agents live in `.codex/agents/`.

- `sprint-planner.toml` - high-context course decomposition.
- `canvas-author.toml` - artifact authoring.

Use direct Python commands for validation, push, and pull.

## Schemas

`schema/` holds:

- `frontmatter.schema.json`
- `manifest.schema.json`
- `prd.schema.json`

Run all validation:

```bash
python3 canvas_sync/schema.py --all
```

Rules enforced or expected:

- No em dashes.
- Sprint bounds are 0 through 5.
- Pages and module headers have no points.
- Assignments, quizzes, and graded discussions have points.
- Artifact bodies cannot contain iframes, scripts, styles, or JavaScript URLs.

## Canvas Sync Layer

`canvas_sync/` is hand-authored Python:

- `canvas_client.py` - Canvas REST API wrapper.
- `push.py` - validates one MD file, converts Markdown to Canvas HTML, creates or updates the Canvas artifact, adds it to the module, and updates the manifest.
- `pull.py` - fetches Canvas state, reports drift, and optionally writes Canvas changes back to MD.
- `schema.py` - validates artifacts, manifests, and PRDs.

Canvas quirks:

- Frontmatter `text_entry` maps to Canvas `online_text_entry`.
- Frontmatter `file_upload` maps to Canvas `online_upload`.
- `due_at` requires full ISO 8601 with timezone, such as `2026-10-15T23:59:00Z`.

## Grading

`n8n/` is separate from the builder runtime. It contains a grading workflow with Canvas webhooks, a review queue, and a human-in-the-loop approval step. It still uses Anthropic in the current repo and should be migrated separately if needed.

## Troubleshooting

**Codex command not found.** Install with `npm i -g @openai/codex`.

**`.env` not found.** Copy `.env.example` to `.env` and fill in Canvas credentials.

**Canvas push 401.** Token is invalid or lacks scope.

**Canvas push 404.** Wrong course ID in `.env` or the manifest.

**Canvas push 400 on `due_at`.** Use full ISO 8601 with timezone or remove the `due` field.

**Loop halts with scaffold incomplete.** Check `AGENTS.md`, `.agents/skills/`, `prompts/codex/ralph-prompt.md`, schemas, and Canvas sync files.

**Failed items stay failed.** A human must decide whether to reset a PRD item to `pending` after fixing the cause.

## See Also

- `README.md` - operator guide.
- `AGENTS.md` - root agent guide and build learnings.
- `docs/codex-migration/` - migration audit and plan.
- `context/build-notes/` - historical build notes.

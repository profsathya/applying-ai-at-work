# Canvas Course Builder Technical Reference

This is the deep-dive reference for the builder. The top-level `README.md` is the first-read operator guide.

The builder supersedes the legacy iframe pattern in `archive/legacy-iframe-template/`.

## Pipeline

```text
course spec or module spec -> Codex skill -> MD files -> schema validation -> review
                                                                       |
                                                                       v
                                                             push.py -> Canvas API
                                                                       |
                                                                       v
                                                    <course>/manifests/production.json
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

Mechanical operations should call Python scripts directly. Do not reintroduce LLM wrappers around validation, push, or pull unless there is a concrete reason.

## Builder And Content Boundary

The builder tooling is intentionally separable from the current certificate content.

Reusable builder layer:

- `canvas_sync/` - Canvas API push, pull, and client code.
- `schema/` - artifact, manifest, and PRD schemas.
- `.agents/skills/` - repeatable Codex workflows.
- `.codex/agents/` - specialized Codex agent definitions.
- `context/course-specs/README.md` and `context/module-specs/README.md` - spec formats.

Course-specific layer:

- `<course>/` - authored artifacts, manifests, PRDs, and course metadata.
- `course*/design/` - course-specific structure and outcomes.
- Most shared design docs in `context/` - certificate-specific audience, principles, and framework notes.
- `briefs/` - pointers for this certificate's planning workflow.

The likely future shape is to extract the reusable builder layer into a template repo, package, or `builder/` directory once `build-course` has been used successfully on at least one real course and one sandbox Canvas push. Do not extract it yet if the workflow is still changing; premature extraction would make iteration slower.

## One-Time Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
npm i -g @openai/codex
cp .env.example .env
```

Fill in Canvas API credentials in `.env`. Course-specific Canvas IDs live in `<course>/manifests/production.json`.

Smoke test:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=<existing Canvas course ID> python canvas_sync/canvas_client.py
```

## New Local Course Setup

Use `canvas_sync/init_course.py` when Canvas already has a course shell and the repo needs a local course directory. This is a local-only setup step. It does not create a Canvas course and does not write to Canvas.

Configure an empty course:

```bash
python3 canvas_sync/init_course.py \
  --course course3 \
  --canvas-course-id 12345 \
  --base-url https://example.instructure.com \
  --title "Applying AI at Work, Cohort 3" \
  --term "Spring 2027"
```

Prompt example:

```text
Configure a new course called course3 for Canvas course ID 12345. Create an empty shell and stop before Canvas writes.
```

After setup:

```text
Draft course3 from context/course-specs/course3-context.md and stop before Canvas.
```

Push after review:

```text
Push reviewed course3 sprint 0 files to Canvas.
```

The setup script creates `<course>/design/`, six sprint folders, `<course>/manifests/production.json`, `<course>/reports/`, starter progress and PRD files, and a course context spec under `context/course-specs/`.

## Full Course Builds

Use `build-course` when a human provides one spec for a whole course. The skill generates all local Markdown first, validates the generated artifacts, reports the file list, and stops before Canvas writes unless a human explicitly confirms a push.

Course specs can be pasted into chat or saved under `context/course-specs/`. If exactly one file matches `context/course-specs/<course>-*.md`, the skill can use it without a full path.

## Skills

Codex skills live in `.agents/skills/`.

- `sync` - validate and push one or more existing artifact MD files.
- `configure-course` - create a new local course shell for an existing Canvas course ID without Canvas writes.
- `add-artifact` - add one new artifact from a natural-language request.
- `build-course` - generate a full course from pasted context or a course spec file, validate, then optionally push after review.
- `build-sprint` - generate one sprint from pasted context or a spec file, validate, then optionally push after review.
- `update-dues` - edit `due` fields, validate, and optionally push.
- `inspect-canvas` - read live Canvas modules and module items, compare with the manifest and local files, and write a local ledger under `<course>/reports/`.
- `reconcile` - dry-run Canvas drift, then optionally apply Canvas changes locally.
- `remove-canvas` - inspect Canvas, dry-run manifest-backed removals, then delete only after confirmation token approval.
- `canvas-author` - write exactly one artifact from a PRD-shaped item.
- `sprint-planner` - decompose course design into PRD, metadata, progress log, and manifest.

`build-course` accepts course context in two forms: pasted directly into chat or saved as a Markdown file under `context/course-specs/`. If exactly one file matches `context/course-specs/<course>-*.md`, the skill can use it without a full path. Use `context/course-specs/README.md` for the recommended spec structure.

`build-sprint` accepts module context in two forms: pasted directly into chat or saved as a Markdown file under `context/module-specs/`. If exactly one file matches `context/module-specs/<course>-sprint-<n>-*.md`, the skill can use it without a full path. Use `context/module-specs/README.md` for the recommended spec structure.

## Custom Agents

Codex custom agents live in `.codex/agents/`.

- `course-drafter.toml` - full-course and sprint/module drafting through `build-course` or `build-sprint`.
- `course-configurator.toml` - local course shell setup through `configure-course` and `init_course.py`.
- `sprint-planner.toml` - high-context course decomposition.
- `canvas-author.toml` - artifact authoring.
- `canvas-inspector.toml` - read-only Canvas inventory and reconcile-readiness reporting through `inspect-canvas`.
- `canvas-remover.toml` - destructive manifest-backed Canvas removals through `remove-canvas`.

Use direct Python commands for validation, inspect, push, pull, and remove.

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
- `init_course.py` - local-only course directory, manifest, starter metadata, and context spec setup for an existing Canvas course ID.
- `push.py` - validates one MD file, converts Markdown to Canvas HTML, creates or updates the Canvas artifact, adds it to the module, and updates the manifest.
- `inspect_canvas.py` - reads live Canvas modules and module items, compares them with the manifest and local Markdown files, and writes JSON/Markdown ledgers under `<course>/reports/`.
- `pull.py` - fetches Canvas state, reports drift, and optionally writes Canvas changes back to MD.
- `remove.py` - dry-runs and applies confirmed deletion of manifest-backed Canvas modules/items while keeping local Markdown files.
- `schema.py` - validates artifacts, manifests, and PRDs.

Canvas quirks:

- Frontmatter `text_entry` maps to Canvas `online_text_entry`.
- Frontmatter `file_upload` maps to Canvas `online_upload`.
- `due_at` requires full ISO 8601 with timezone, such as `2026-10-15T23:59:00Z`.

## Troubleshooting

**Codex command not found.** Install with `npm i -g @openai/codex`.

**`.env` not found.** Copy `.env.example` to `.env` and fill in Canvas credentials.

**Canvas push 401.** Token is invalid or lacks scope.

**Canvas push 404.** Wrong course ID in `.env` or the manifest.

**Canvas push 400 on `due_at`.** Use full ISO 8601 with timezone or remove the `due` field.

**Failed items stay failed.** A human must decide whether to reset a PRD item to `pending` after fixing the cause.

## See Also

- `README.md` - operator guide.
- `AGENTS.md` - root agent guide and build learnings.
- `docs/codex-migration/` - migration audit and plan.
- `context/build-notes/` - historical build notes.

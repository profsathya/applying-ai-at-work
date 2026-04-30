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

- `course1/` and `course2/` - authored artifacts, manifests, PRDs, and course metadata.
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

Fill in Canvas credentials and course IDs in `.env`.

Smoke test:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=$COURSE1_CANVAS_ID python canvas_sync/canvas_client.py
```

## Full Course Builds

Use `build-course` when a human provides one spec for a whole course. The skill generates all local Markdown first, validates the generated artifacts, reports the file list, and stops before Canvas writes unless a human explicitly confirms a push.

Course specs can be pasted into chat or saved under `context/course-specs/`. If exactly one file matches `context/course-specs/<course>-*.md`, the skill can use it without a full path.

## Skills

Codex skills live in `.agents/skills/`.

- `sync` - validate and push one or more existing artifact MD files.
- `add-artifact` - add one new artifact from a natural-language request.
- `build-course` - generate a full course from pasted context or a course spec file, validate, then optionally push after review.
- `build-sprint` - generate one sprint from pasted context or a spec file, validate, then optionally push after review.
- `update-dues` - edit `due` fields, validate, and optionally push.
- `reconcile` - dry-run Canvas drift, then optionally apply Canvas changes locally.
- `canvas-author` - write exactly one artifact from a PRD-shaped item.
- `sprint-planner` - decompose course design into PRD, metadata, progress log, and manifest.

`build-course` accepts course context in two forms: pasted directly into chat or saved as a Markdown file under `context/course-specs/`. If exactly one file matches `context/course-specs/<course>-*.md`, the skill can use it without a full path. Use `context/course-specs/README.md` for the recommended spec structure.

`build-sprint` accepts module context in two forms: pasted directly into chat or saved as a Markdown file under `context/module-specs/`. If exactly one file matches `context/module-specs/<course>-sprint-<n>-*.md`, the skill can use it without a full path. Use `context/module-specs/README.md` for the recommended spec structure.

## Custom Agents

Codex custom agents live in `.codex/agents/`.

- `course-drafter.toml` - full-course and sprint/module drafting through `build-course` or `build-sprint`.
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

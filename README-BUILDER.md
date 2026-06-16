# Canvas Course Builder Technical Reference

This is the deep-dive reference for the builder. The top-level `README.md` is the first-read operator guide.

The builder supersedes the legacy iframe pattern in `archive/legacy-iframe-template/`.

## Pipeline

```text
course spec or module spec -> Codex skill -> MD files -> schema validation -> review
                                                                       |
                                                                       v
                                                   protected publish workflow -> push.py -> Canvas API
                                                                       |
                                                                       v
                                                               canvas-state branch
```

Core invariants:

- MD is authoritative during build.
- Common Curriculum HTML and activity JSON are generated output, not source.
- Canvas IDs live only in deployment state. Legacy local pushes may still write manifest state.
- Canvas wins on live-course drift.
- Schema validation is a hard gate before Canvas writes.
- Production Canvas writes run through GitHub Actions with one serialized publisher.
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

Fill in Canvas API credentials in `.env`. Course-specific Canvas course IDs live in `<course>/manifests/production.json`. Mutable production deployment state lives on the protected `canvas-state` branch.

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
  --term "Spring 2027" \
  --sprint-count 4
```

Prompt example:

```text
Configure a new four-module course called course3 for Canvas course ID 12345. Create an empty shell and stop before Canvas writes.
```

After setup:

```text
Draft course3 from context/course-specs/course3-context.md and stop before Canvas.
```

Push after review:

```text
Push reviewed course3 sprint <n> files to Canvas.
```

The setup script creates `<course>/design/`, the requested number of sprint folders, `<course>/manifests/production.json`, `<course>/reports/`, starter progress and PRD files, and a course context spec under `context/course-specs/`.

## Full Course Builds

Use `build-course` when a human provides one spec for a whole course. The skill generates all local Markdown first, validates the generated artifacts, reports the file list, and stops before Canvas writes unless a human explicitly confirms a push.

Course specs can be pasted into chat or saved under `context/course-specs/`. If exactly one file matches `context/course-specs/<course>-*.md`, the skill can use it without a full path.

## Skills

Codex skills live in `.agents/skills/`.

- `sync` - validate and push one or more existing artifact MD files for approved admin or sandbox use.
- `configure-course` - create a new local course shell for an existing Canvas course ID without Canvas writes.
- `add-artifact` - add one new artifact from a natural-language request.
- `build-course` - generate a full course from pasted context or a course spec file, validate, then optionally push after review.
- `build-sprint` - generate one sprint from pasted context or a spec file, validate, then optionally push after review.
- `update-dues` - edit `due` fields, validate, and optionally push.
- `inspect-canvas` - read live Canvas modules and module items, compare with the manifest and local files, and write a local ledger under `<course>/reports/`.
- `update-artifact` - list live Canvas module items, prepare exactly one `module_item_id` for local Markdown editing, validate the edited artifact, and stop before Canvas writes.
- `reconcile` - dry-run Canvas drift, then optionally apply Canvas changes locally.
- `remove-canvas` - inspect Canvas, dry-run manifest-backed removals or an explicit full-course content clear, then delete only after confirmation token approval.
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
- `canvas-remover.toml` - destructive manifest-backed removals or explicit full-course content clears through `remove-canvas`.

Use direct Python commands for validation, inspect, push, pull, and remove.

## Hosted Content Updates

Hosted Canvas content is still authored in Markdown under `<course>/sprints/`. The Common Curriculum checkout receives generated HTML and JSON only when the publish layer renders it.

When `<course>/homepage.yaml` exists, it is the curated source for the generated hosted landing pages. The renderer combines that YAML with artifact frontmatter and deployment state to write `deanza/<course>/home.html`, `index.html`, and `sprint-<n>.html`.

Hosted homepages can show learner-specific progress only when opened through the Canvas LTI progress launch. The generated static HTML never contains private learner data. It renders read-only progress indicators and `deanza/<course>/progress-map.json`; the browser fills them from the Common Curriculum progress function after a valid LTI launch.

Canvas module requirements are the progress source of truth:

- Default requirements are `must_view` for pages, `must_submit` for assignments and quizzes, `must_contribute` for native discussions, and `must_submit` for hosted AI activities that publish as Canvas assignments.
- Artifact frontmatter may set `completion_requirement` to `auto`, `none`, `must_view`, `must_submit`, `must_contribute`, `must_mark_done`, or `min_score`.
- `completion_requirement: none` omits a requirement for new module items. If Canvas already has a requirement, clear it in Canvas first; the backfill command reports that case as blocked instead of changing local state.
- Deployment state records `canvas_module_item_id` and `completion_requirement` so hosted progress can map Canvas module items back to homepage rows.

To inspect and backfill existing Canvas module items, run dry-run first:

```bash
python canvas_sync/completion.py \
  --manifest course1/manifests/production.json \
  --state-dir ../canvas-state \
  --dry-run
```

Apply only after reviewing the dry run:

```bash
python canvas_sync/completion.py \
  --manifest course1/manifests/production.json \
  --state-dir ../canvas-state \
  --apply
```

For a changed hosted module or artifact:

1. Update the Markdown source.
2. Validate the artifact or the repo.
3. Use the protected `Publish Canvas` workflow for production.
4. For approved local admin or sandbox pushes, pass `--hosted-output-dir ../common-curriculum` to `canvas_sync/push.py`.

Do not patch generated files under `../common-curriculum/deanza/<course>/` as the source of a course change. Those files should be regenerated from Markdown.

## Schemas

`schema/` holds:

- `frontmatter.schema.json`
- `manifest.schema.json`
- `canvas_state.schema.json`
- `prd.schema.json`

Run all validation:

```bash
python3 canvas_sync/schema.py --all
```

Rules enforced or expected:

- No em dashes.
- Artifact frontmatter includes stable `artifact_id`.
- Sprint values are non-negative integers. Course setup creates the count requested by the human.
- Pages and module headers have no points.
- Assignments, quizzes, and graded discussions have points.
- Artifact bodies cannot contain iframes, scripts, styles, or JavaScript URLs.

## GitOps Publish Layer

Production publishing uses `.github/workflows/publish-canvas.yml`:

```text
main checkout + canvas-state checkout -> validate -> bootstrap missing state -> hydrate fingerprints -> publish changed artifacts -> commit canvas-state
```

- `canvas-state` stores `<course>/production.json` files keyed by `artifact_id`.
- The workflow also checks out Common Curriculum, renders hosted De Anza HTML/activity JSON for changed hosted artifacts, and commits those files when publishing succeeds.
- The workflow uses the protected `canvas-production` environment and a single concurrency group.
- `canvas_sync/bootstrap_state.py` converts legacy manifest state into external state files.
- `canvas_sync/hydrate_state.py` records live Canvas fingerprints only when Canvas still matches local Markdown.
- `canvas_sync/publish_changed.py` publishes only artifacts whose content hash differs from state.
- For approved local hosted publishes, pass `--hosted-output-dir ../common-curriculum` so Canvas iframe shells point at files that are rendered into the Common Curriculum checkout before Canvas is updated.
- `canvas_sync/check_drift.py` compares live Canvas with `canvas-state` and local Markdown for nightly drift detection.
- Direct local `push.py` without `--state-dir` is retained for backwards compatibility and emergency repair.

Recommended repository controls:

- Protect `main`: require a pull request, require the `Validate schemas / validate` check, require conversations to be resolved, and block force pushes.
- Protect `canvas-state`: restrict direct pushes to GitHub Actions or admins.
- Keep `canvas-production` as a protected GitHub Environment for Canvas secrets.
- Do not add a mandatory staging Canvas environment unless course volume or reviewer count grows enough to justify it.

## Canvas Sync Layer

`canvas_sync/` is hand-authored Python:

- `canvas_client.py` - Canvas REST API wrapper.
- `init_course.py` - local-only course directory, manifest, starter metadata, and context spec setup for an existing Canvas course ID.
- `push.py` - validates one MD file, converts Markdown to Canvas HTML, creates or updates the Canvas artifact, adds it to the module, and updates legacy manifest state or external `canvas-state`.
- `state.py` - shared deployment-state helpers, state file locks, state bootstrap conversion, and Canvas fingerprints.
- `bootstrap_state.py` - writes initial external state files from existing manifests.
- `publish_changed.py` - publishes changed artifacts against external state.
- `check_drift.py` - checks live Canvas against external state.
- `inspect_canvas.py` - reads live Canvas modules and module items, compares them with the manifest and local Markdown files, and writes JSON/Markdown ledgers under `<course>/reports/`.
- `update_artifact.py` - lists live module items by `module_item_id`, refreshes or imports one selected item into local Markdown for editing, and verifies that identity fields stayed fixed.
- `pull.py` - fetches Canvas state, reports drift, and optionally writes Canvas changes back to MD.
- `remove.py` - dry-runs and applies confirmed deletion of manifest-backed Canvas modules/items, or a token-gated full course content clear, while keeping local Markdown files.
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

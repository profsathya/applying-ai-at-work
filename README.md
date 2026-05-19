# Applying AI at Work

This repo builds Canvas course materials from Markdown.

For most users, the workflow is simple:

```text
plain-English request -> local Markdown draft -> validation -> human review -> merge to main -> protected Canvas publish
```

Codex is the supported course-building assistant. Users do not need to choose the right internal tool. They describe the work, the target course or sprint, and whether Canvas publishing is allowed. Codex routes the request through the right workflow, writes local Markdown, validates it, and stops before Canvas unless the user clearly approves a push. Production publishes normally happen through the protected GitHub Actions workflow after reviewed Markdown is merged to `main`; direct local pushes are reserved for approved admin repair or sandbox pilots.

## Start Here

From your checkout:

```bash
cd /path/to/applying-ai-at-work
source .venv/bin/activate
codex
```

Then ask for what you want in plain English.

```text
Draft course4 from context/course-specs/course4-context.md and stop before Canvas.
```

```text
Configure a new four-module course called course5 for Canvas course ID 12345. Create an empty shell and stop before Canvas writes.
```

```text
Draft course3 from context/course-specs/course3-context.md and stop before Canvas.
```

```text
Draft course4 sprint 3 from pasted module context and stop before Canvas.
```

```text
Add a page to course1 sprint 0 called "How to ask for help".
```

```text
Publish reviewed Markdown through the protected workflow after this branch is merged to main.
```

```text
For an approved sandbox push, sync this reviewed file to Canvas: course4/sprints/sprint-1/testing-and-applied-project.md
```

```text
Move all course1 sprint 3 assignment due dates to 2026-10-22T23:59:00Z.
```

```text
Canvas was edited directly for course1. Show me the dry-run reconcile report before applying anything.
```

```text
Inspect course1 on Canvas, include module items, and update the local ledger.
```

```text
For Canvas course 180, list artifact module item IDs and prepare module_item_id:123 for editing.
```

```text
Remove the manifest-backed Canvas item module_item_id:123 from course1. Show the dry run first and ask me for the confirmation token before deleting anything.
```

## What Codex Does

Codex infers the workflow from the request:

| User asks for | Codex uses |
|---|---|
| A whole course from one spec | `course-drafter` with `build-course` |
| A new local course shell for an existing Canvas course | `course-configurator` with `configure-course` |
| One sprint or module | `course-drafter` with `build-sprint` |
| One page, assignment, quiz, discussion, or module header | `add-artifact` |
| Reviewed Markdown published to Canvas | merge the reviewed branch to `main` for GitOps publish, or `sync` for approved admin or sandbox use |
| Due date changes | `update-dues` |
| Live Canvas module/item inventory and ledger | `canvas-inspector` with `inspect-canvas` |
| One live Canvas artifact prepared for local editing by module item ID | `update-artifact` |
| Canvas edits pulled back into the repo | `reconcile` dry-run first |
| Manifest-backed Canvas modules/items removed | `canvas-remover` with `remove-canvas` |

The tool names are optional. They are here so maintainers can understand the routing.

## Expected Response

For draft-only work, Codex should report the files it created and the validation result:

```text
Drafted 5 local Markdown artifacts.

Validation:
- artifact validation: PASS
- full schema validation: PASS

No Canvas changes were made. Review the files, then ask to push if approved.
```

For protected GitOps publishes, the GitHub Actions run publishes changed artifacts and commits deployment state to the `canvas-state` branch. For approved direct local pushes, Codex should report the fields returned by `canvas_sync/push.py`:

```text
Synced 1 file to Canvas.

action: updated
artifact_id: course3-sprints-sprint-0-repo-inspection-practice
canvas_id: 6731
canvas_module_id: 1900
state_path: course3/manifests/production.json
```

For Canvas inspections, Codex should report the live-course summary and ledger paths:

```text
Inspected course1 on Canvas.

Ledger:
- course1/reports/canvas-ledger-production.md
- course1/reports/canvas-ledger-production.json

No Canvas writes were made.
```

For Canvas removal dry runs, Codex should report the planned operations, blocked targets, local files that will be kept, manifest entries that would be removed, and the confirmation token required before any delete call:

```text
Removal dry run complete.

Apply allowed: yes
Operations: 2
Local Markdown files kept.
Confirmation token: abc123

No Canvas changes were made.
```

## Context Specs

Codex can work from either pasted context or a Markdown spec file.

- Whole-course specs go in `context/course-specs/`.
- Sprint or module specs go in `context/module-specs/`.
- Templates and examples live in those folders.

A single course spec can describe a whole course. Codex will generate the local Markdown sprint by sprint, validate the files, and stop before Canvas unless a push is approved.

## Configure A New Local Course

Use this when Canvas already has a course shell and the repo needs a matching local course directory. This does not create a Canvas course and does not write to Canvas.

```bash
python3 canvas_sync/init_course.py \
  --course course5 \
  --canvas-course-id 12345 \
  --base-url https://example.instructure.com \
  --title "Applying AI at Work, Cohort 5" \
  --term "Spring 2027" \
  --sprint-count 4
```

Prompt example:

```text
Configure a new four-module course called course5 for Canvas course ID 12345. Create an empty shell and stop before Canvas writes.
```

After setup:

```text
Draft course5 from context/course-specs/course5-context.md and stop before Canvas.
```

Publish after review:

```text
Merge reviewed course5 Markdown to main for protected publish, or ask for an approved sandbox sync.
```

## Local Validation

Run these before a commit or Canvas push:

```bash
source .venv/bin/activate
python canvas_sync/schema.py --all
python -m unittest discover
```

If your shell `python3` does not have the repo dependencies, activate the virtualenv first:

```bash
source .venv/bin/activate
```

## GitOps Canvas Publishing

Production publishing is branch based:

```text
instructor branch -> local validation and configured checks -> merge to main -> protected Publish Canvas workflow -> Canvas API -> canvas-state branch
```

- Markdown stays on `main` as the desired course content.
- `artifact_id` in frontmatter is the stable deployment identity. Do not change it after creation.
- Mutable Canvas IDs, module IDs, page URLs, publish hashes, and Canvas fingerprints live on the protected `canvas-state` branch.
- `.github/workflows/publish-canvas.yml` triggers for `course*/sprints/**`, `course*/manifests/production.json`, `schema/**`, `canvas_sync/**`, and `tests/**`. It serializes Canvas writes and uses the protected `canvas-production` GitHub Environment.
- `.github/workflows/validate-schemas.yml` runs the schema and unit test checks for its configured path filters. Update those filters when a new course folder should receive PR validation.
- Existing state is hydrated with live Canvas fingerprints before changed artifacts publish, so Canvas-side edits block overwrite instead of being silently replaced.
- `.github/workflows/reconcile-check.yml` checks live Canvas against `main` plus `canvas-state` nightly.
- Direct local `canvas_sync/push.py` remains available for admin repair or sandbox pilots, but it is not the normal production path.

## Canvas Safety

Canvas writes are real side effects.

- Draft requests should say `stop before Canvas`.
- Codex validates before publishing.
- Production publishes happen after merge through the protected GitHub Actions workflow.
- `canvas_sync/inspect_canvas.py` is read-only against Canvas and can update local ledgers under `<course>/reports/`.
- Use `canvas-inspector` before reconcile when you need a current Canvas module/item inventory and manifest alignment check.
- `canvas_sync/push.py` reads the Canvas course ID from `<course>/manifests/production.json`. Without `--state-dir`, it updates legacy manifest-backed state; with `--state-dir`, it updates external deployment state such as a local `canvas-state` checkout.
- `canvas_sync/remove.py` requires a dry-run confirmation token before deleting Canvas content and keeps local Markdown files.
- Do not write Canvas IDs into Markdown frontmatter.
- Do not commit `.env`.

## One-Time Setup

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
npm i -g @openai/codex
cp .env.example .env
```

Fill in `.env` with Canvas API credentials.
Course-specific Canvas course IDs live in manifests. Mutable deployment IDs live in `canvas-state` for production publishing.

Check the Canvas connection:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=<existing Canvas course ID> python canvas_sync/canvas_client.py
```

Expected output:

```text
Connected to course <id>. Found N modules.
```

## Repo Map

```text
<course>/                   Course design, sprint Markdown, manifests, PRDs
context/                    Shared design docs and course/module specs
canvas_sync/                Deterministic Canvas push, pull, and validation scripts
course*/reports/            Generated Canvas inspection ledgers
schema/                     JSON schemas for artifacts, manifests, deployment state, and PRDs
.agents/skills/             Reusable Codex workflows
.codex/agents/              Specialized Codex agents
.github/workflows/          PR validation, protected Canvas publish, drift checks
README-BUILDER.md           Technical reference for maintainers
AGENTS.md                   Agent guidance and build learnings
docs/codex-migration/       Migration history
archive/                    Superseded reference material
```

## Useful Rules

- Use full Canvas-compatible due dates, such as `2026-10-22T23:59:00Z`.
- Omit due dates when they are not known.
- Keep generated artifacts under `<course>/sprints/sprint-<n>/`.
- Keep course design decisions in `<course>/design/` or `context/`, then draft from that source.
- Use `README-BUILDER.md` for low-level commands and troubleshooting.

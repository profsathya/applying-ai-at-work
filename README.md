# Applying AI at Work

This repo builds Canvas course materials from Markdown.

For most users, the workflow is simple:

```text
plain-English request -> local Markdown draft -> validation -> human review -> explicit Canvas push
```

Codex is the supported course-building assistant. Users do not need to choose the right internal tool. They describe the work, the target course or sprint, and whether Canvas publishing is allowed. Codex routes the request through the right workflow, writes local Markdown, validates it, and stops before Canvas unless the user clearly approves a push.

## Start Here

From the repo root:

```bash
cd applying-ai-at-work
source .venv/bin/activate
codex
```

Then ask for what you want in plain English.

```text
Draft course2 from context/course-specs/course2-ai-implementation.md and stop before Canvas.
```

```text
Configure a new course called course3 for Canvas course ID 12345. Create an empty shell and stop before Canvas writes.
```

```text
Draft course3 from context/course-specs/course3-context.md and stop before Canvas.
```

```text
Draft course2 sprint 1 from context/module-specs/course2-sprint-1-stakeholder-framing.md and stop before Canvas.
```

```text
Add a page to course1 sprint 0 called "How to ask for help".
```

```text
Push these reviewed files to Canvas: course2/sprints/sprint-1/example.md
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
| Reviewed Markdown pushed to Canvas | `sync` |
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

For Canvas pushes, Codex should report the Canvas IDs:

```text
Pushed 5 files to Canvas.

Module ID: 1896
Page ID: 3352
Assignment ID: 6721
Quiz ID: 2914
Discussion ID: 1391
Manifest updated.
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

## Local Validation

Run these before a commit or Canvas push:

```bash
python3 canvas_sync/schema.py --all
python3 -m unittest discover
```

If your shell `python3` does not have the repo dependencies, activate the virtualenv first:

```bash
source .venv/bin/activate
```

## Canvas Safety

Canvas writes are real side effects.

- Draft requests should say `stop before Canvas`.
- Codex validates before pushing.
- Codex only pushes after explicit approval.
- `canvas_sync/inspect_canvas.py` is read-only against Canvas and can update local ledgers under `<course>/reports/`.
- Use `canvas-inspector` before reconcile when you need a current Canvas module/item inventory and manifest alignment check.
- `canvas_sync/push.py` reads the Canvas course ID from `<course>/manifests/production.json` and owns Canvas IDs and manifest updates.
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
Course-specific Canvas IDs live in manifests. Use `canvas_sync/init_course.py` to create a local course manifest for each Canvas course.

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
schema/                     JSON schemas for artifacts, manifests, and PRDs
.agents/skills/             Reusable Codex workflows
.codex/agents/              Specialized Codex agents
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

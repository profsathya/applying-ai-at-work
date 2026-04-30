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

## What Codex Does

Codex infers the workflow from the request:

| User asks for | Codex uses |
|---|---|
| A whole course from one spec | `course-drafter` with `build-course` |
| One sprint or module | `course-drafter` with `build-sprint` |
| One page, assignment, quiz, discussion, or module header | `add-artifact` |
| Reviewed Markdown pushed to Canvas | `sync` |
| Due date changes | `update-dues` |
| Canvas edits pulled back into the repo | `reconcile` dry-run first |

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

## Context Specs

Codex can work from either pasted context or a Markdown spec file.

- Whole-course specs go in `context/course-specs/`.
- Sprint or module specs go in `context/module-specs/`.
- Templates and examples live in those folders.

A single course spec can describe a whole course. Codex will generate the local Markdown sprint by sprint, validate the files, and stop before Canvas unless a push is approved.

## Canvas Safety

Canvas writes are real side effects.

- Draft requests should say `stop before Canvas`.
- Codex validates before pushing.
- Codex only pushes after explicit approval.
- `canvas_sync/push.py` owns Canvas IDs and manifest updates.
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

Fill in `.env` with Canvas credentials and course IDs.

Check the Canvas connection:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=$COURSE1_CANVAS_ID python canvas_sync/canvas_client.py
```

Expected output:

```text
Connected to course <id>. Found N modules.
```

## Repo Map

```text
course1/ and course2/       Course design, sprint Markdown, manifests, PRDs
context/                    Shared design docs and course/module specs
canvas_sync/                Deterministic Canvas push, pull, and validation scripts
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
- Keep generated artifacts under `course<N>/sprints/sprint-<n>/`.
- Keep course design decisions in `course<N>/design/` or `context/`, then draft from that source.
- Use `README-BUILDER.md` for low-level commands and troubleshooting.

# Applying AI at Work

This repo is two things in one: a Canvas course builder, and the design for the "Applying AI at Work" workforce certificate (CTI + De Anza). Course content is authored as Canvas-agnostic Markdown in `course1/` and `course2/`, validated locally, then pushed to Canvas through the Python sync layer in `canvas_sync/`.

OpenAI Codex is now the supported orchestration layer. Durable repo guidance lives in `AGENTS.md`; reusable workflows live in `.agents/skills/`; specialized authoring and planning agents live in `.codex/agents/`; the autonomous build loop is `codex-ralph.sh`.

## What's In This Repo

- `course1/` and `course2/` - the two certificate courses. Each has `design/`, `sprints/`, and `manifests/`.
- `context/` - shared design docs: audience, frameworks, design principles, SDT, stakeholder engagement, AI partnership, certificate overview, decision log.
- `canvas_sync/` - deterministic Python sync engine for Canvas API calls, pull, push, and schema validation.
- `.agents/skills/` - Codex skills for `sync`, `add-artifact`, `build-sprint`, `update-dues`, `reconcile`, `ralph-build-loop`, `canvas-author`, and `sprint-planner`.
- `.codex/` - Codex project config and custom agent definitions.
- `prompts/codex/ralph-prompt.md` - the Codex Ralph loop prompt for initial builds.
- `codex-ralph.sh` - the Codex-backed autonomous build loop.
- `schema/` - JSON schemas for PRDs, manifests, and artifact frontmatter.
- `briefs/` - pointer files the planner reads.
- `docs/codex-migration/` - migration audit, compatibility matrix, plan, and open questions.
- `n8n/` - optional grading workflow, separate from the course-builder runtime.
- `archive/` - superseded iframe pattern, kept for reference.

## Quick Start

One-time setup after cloning:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
npm i -g @openai/codex
codex
cp .env.example .env
```

Fill in `.env` with Canvas credentials and course IDs.

Confirm the Canvas connection works:

```bash
set -a
source .env
set +a
DEFAULT_COURSE_ID=$COURSE1_CANVAS_ID python canvas_sync/canvas_client.py
```

Expected output: `Connected to course <id>. Found N modules.`

## How Teammates Use This

Most day-to-day work happens in a Codex session from the repo root. Ask Codex to use one of the repo skills by name, or describe the task in plain English. The skills encode the safe workflow: validate first, write through the Python sync layer, and ask before broad Canvas changes.

Start an interactive session:

```bash
cd applying-ai-at-work
source .venv/bin/activate
codex
```

Then ask for the workflow you want:

```text
Use the sync skill for course1/sprints/sprint-2/synthesize-what-you-heard.md.
```

```text
Use the add-artifact skill to add a page to course 1 sprint 0 called "How to ask for help" explaining the three channels we use and when to use each.
```

```text
Use the update-dues skill to push all sprint 3 assignments to 2026-10-22T23:59:00Z.
```

```text
Use the reconcile skill for course1 and show me the dry-run report before applying anything.
```

You can also pass the first prompt directly when starting Codex:

```bash
codex "Use the sync skill for course1/sprints/sprint-5/codex-pilot-final-readiness-check.md."
```

Use `codex exec` for non-interactive runs when the task is already concrete:

```bash
codex exec "Validate all course artifacts and summarize any failures."
```

Canvas-writing `codex exec` tasks should stay narrow. Prefer one file or one explicit workflow at a time.

## Invoking Skills, Agents, And Tools

This repo gives Codex three kinds of capability:

1. **Skills** in `.agents/skills/`: reusable workflows.
2. **Custom agents** in `.codex/agents/`: specialized LLM workers for planner and author roles.
3. **Python tools** in `canvas_sync/`: deterministic scripts that validate, push, and pull Canvas content.

### Skills

Ask for a skill by name in plain language:

```text
Use the build-sprint skill for course2 sprint 1 using /tmp/sprint-1-context.md. Write MD only and stop before any Canvas push.
```

```text
Use the update-dues skill to remove the due date from course1/sprints/sprint-3/ai-fit-analysis.md, validate it, and ask before pushing.
```

Available skills:

| Skill | Use it when |
|---|---|
| `sync` | An existing MD artifact should be pushed to Canvas. |
| `add-artifact` | You need one new assignment, page, discussion, quiz, or module header. |
| `build-sprint` | You need a coherent sprint/module built from a context document. |
| `update-dues` | You need due dates changed without touching other content. |
| `reconcile` | Canvas was edited directly and the repo needs to pull those changes back. |
| `ralph-build-loop` | You are running or maintaining the autonomous build loop. |
| `canvas-author` | You need exactly one artifact written from a PRD-shaped item. |
| `sprint-planner` | A course needs a PRD, metadata file, progress log, and empty manifest. |

### Custom Agents

Custom agents are for specialized LLM work, not mechanical script execution. Ask for them explicitly when the task benefits from a separate role:

```text
Use the sprint-planner agent to inspect briefs/course2.md and draft a plan. Do not push to Canvas.
```

```text
Use the canvas-author agent to write exactly one artifact from this PRD item, then validate the file.
```

Current custom agents:

- `sprint-planner`
- `canvas-author`

### Direct Python Tools

Codex can run these scripts directly, and the skills are written to use them:

```bash
python3 canvas_sync/schema.py --all
python3 canvas_sync/schema.py --artifact course1/sprints/sprint-5/codex-pilot-final-readiness-check.md
python3 canvas_sync/push.py --file course1/sprints/sprint-5/codex-pilot-final-readiness-check.md --manifest course1/manifests/production.json
python3 canvas_sync/pull.py --manifest course1/manifests/production.json --dry-run
```

Use direct tools when you already know the exact file and operation. Use skills when target resolution, sequencing, validation, or user review matters.

## Workflow Guide

| Workflow | What it does | Touches Canvas? | Confirmation expected? |
|---|---|---:|---:|
| `sync` | Push one or more edited MD files to Canvas | yes | yes unless the current request explicitly says to push |
| `add-artifact` | Add one new assignment, page, discussion, quiz, or module header | yes | yes before push unless explicitly requested |
| `build-sprint` | Build a whole sprint from a context doc | yes | yes |
| `update-dues` | Change due dates on one or many artifacts | optional | yes before push |
| `reconcile` | Pull Canvas-side edits back into MD | no Canvas write | yes before local apply |
| `ralph-build-loop` | Maintain or run the Codex initial-build loop | yes during BUILD | only after sandbox policy is settled |

## Build Course 2

The autonomous loop is only for an initial build or a from-scratch rebuild:

```bash
TARGET_COURSE=course2 ./codex-ralph.sh --verbose
```

Expect a full course to take many iterations. The loop reads file state each time and picks up from the first pending PRD item. Do not run unattended against production Canvas until the sandbox pilot has passed.

## Rule Of Thumb

- One existing artifact changed: use `sync`.
- One new artifact: use `add-artifact`.
- Due dates only: use `update-dues`.
- One sprint of artifacts: use `build-sprint`.
- Canvas changed directly: use `reconcile`.
- Whole course from scratch: run `codex-ralph.sh`.
- Course structure changed broadly: edit `course<N>/design/` first, then re-plan.

## Repo Layout

```text
applying-ai-at-work/
  AGENTS.md                      # Codex root guidance and build learnings
  README.md                      # operator overview
  README-BUILDER.md              # technical reference
  .env.example                   # Canvas credentials template
  codex-ralph.sh                 # Codex-backed build loop
  migrate.sh                     # historical one-time migration utility

  .agents/skills/                # Codex workflow skills
  .codex/                        # Codex project config and custom agents
  prompts/codex/                 # Codex loop prompt
  docs/codex-migration/          # migration audit and plan

  canvas_sync/                   # Python Canvas sync layer
  schema/                        # JSON schemas
  briefs/                        # planner pointer files
  context/                       # shared design docs
  course1/                       # course 1 design, sprints, manifests, PRD
  course2/                       # course 2 design, sprints, manifests, PRD
  n8n/                           # optional grading workflow
  archive/                       # legacy reference materials
```

## Gotchas

- `.env` is local and contains secrets. Never commit it.
- `canvas_sync/canvas_client.py` does not auto-load `.env`; `push.py` and `pull.py` do.
- Canvas rejects bare local due dates like `2026-10-15T23:59`. Use `2026-10-15T23:59:00Z` or omit `due`.
- Do not hand-edit `course<N>/prd.json` unless you are deliberately repairing build state.
- Do not write Canvas IDs into MD frontmatter. Manifests own Canvas IDs.
- Do not edit `course<N>/design/` from generated build workflows. Design docs are authoritative inputs.

## Deeper References

- `README-BUILDER.md` - technical reference.
- `AGENTS.md` - Codex guidance and accumulated build learnings.
- `docs/codex-migration/` - migration audit and implementation plan.
- `context/certificate-overview.md` - certificate design.
- `context/design-principles.md` - pedagogical principles.

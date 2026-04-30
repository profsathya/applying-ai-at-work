# Applying AI at Work

This repo is two things in one: a Canvas course builder, and the design for the "Applying AI at Work" workforce certificate (CTI + De Anza). Course content is authored as Canvas-agnostic Markdown in `course1/` and `course2/`, validated locally, then pushed to Canvas through the Python sync layer in `canvas_sync/`.

OpenAI Codex is now the supported orchestration layer. Durable repo guidance lives in `AGENTS.md`; reusable workflows live in `.agents/skills/`; specialized authoring and planning agents live in `.codex/agents/`.

## What's In This Repo

- `course1/` and `course2/` - the two certificate courses. Each has `design/`, `sprints/`, and `manifests/`.
- `context/` - shared design docs: audience, frameworks, design principles, SDT, stakeholder engagement, AI partnership, certificate overview, decision log.
- `context/course-specs/` - optional human-authored specs for building a whole course from one Markdown file.
- `context/module-specs/` - optional human-authored specs for building whole sprints/modules.
- `canvas_sync/` - deterministic Python sync engine for Canvas API calls, pull, push, and schema validation.
- `.agents/skills/` - Codex skills for `build-course`, `build-sprint`, `sync`, `add-artifact`, `update-dues`, `reconcile`, `canvas-author`, and `sprint-planner`.
- `.codex/` - Codex project config and custom agent definitions.
- `schema/` - JSON schemas for PRDs, manifests, and artifact frontmatter.
- `briefs/` - pointer files the planner reads.
- `docs/codex-migration/` - migration audit, compatibility matrix, plan, and open questions.
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

Then ask for what you want in plain English:

```text
Draft course2 from context/course-specs/course2-ai-implementation.md. Generate the Markdown files and stop before Canvas.
```

```text
Draft course2 sprint 1 from context/module-specs/course2-sprint-1-stakeholder-framing.md. Generate the Markdown files and stop before Canvas.
```

```text
Add a page to course1 sprint 0 called "How to ask for help" explaining the three channels we use and when to use each.
```

```text
Push the reviewed course2 files to Canvas.
```

```text
Move all course1 sprint 3 assignment due dates to 2026-10-22T23:59:00Z.
```

```text
Canvas was edited directly for course1. Show me the dry-run reconcile report before applying anything.
```

For course or module drafting, Codex routes through the `course-drafter` agent. You do not need to name the internal skills unless you want advanced control.

You can also pass a request directly when starting Codex:

```bash
codex "Draft course2 from context/course-specs/course2-ai-implementation.md and stop before Canvas."
```

## Drafting Workflow

Use plain English as the front door for new course content:

1. Write or paste a course spec or module spec.
2. Ask Codex to draft the course or module.
3. Codex routes full-course requests through `build-course` and one-sprint/module requests through `build-sprint`.
4. Codex generates local Markdown under `course<N>/sprints/sprint-<n>/`.
5. Codex validates every generated artifact and runs the full validator.
6. Codex reports the file list, artifact types, and validation result.
7. You review the local Markdown.
8. Codex pushes to Canvas only after explicit confirmation.

Use one file per whole course in `context/course-specs/`, or one file per sprint/module in `context/module-specs/`. Pasted specs work too.

## Advanced Controls

Skill and agent names are optional. Use them when you want to be precise:

Available skills:

| Skill | Use it when |
|---|---|
| `build-course` | You need a full course generated from one pasted context spec or spec file. |
| `sync` | An existing MD artifact should be pushed to Canvas. |
| `add-artifact` | You need one new assignment, page, discussion, quiz, or module header. |
| `build-sprint` | You need a coherent sprint/module built from a pasted context spec or spec file. |
| `update-dues` | You need due dates changed without touching other content. |
| `reconcile` | Canvas was edited directly and the repo needs to pull those changes back. |
| `canvas-author` | You need exactly one artifact written from a PRD-shaped item. |
| `sprint-planner` | A course needs a PRD, metadata file, progress log, and empty manifest. |

### Custom Agents

Custom agents are for specialized drafting, planning, and authoring:

Current custom agents:

- `course-drafter`
- `sprint-planner`
- `canvas-author`

Direct Python commands are documented in `README-BUILDER.md`. Most users should use plain English requests instead.

## Which Request Should I Make?

- Whole course from one spec: "Draft course2 from `context/course-specs/...` and stop before Canvas."
- One sprint or module from one spec: "Draft course2 sprint 1 from `context/module-specs/...` and stop before Canvas."
- One new item: "Add a page/assignment/quiz/discussion to course1 sprint 2 called ..."
- Reviewed local edits ready for Canvas: "Push these reviewed files to Canvas: ..."
- Due dates only: "Move course1 sprint 3 due dates to `2026-10-22T23:59:00Z`."
- Canvas was edited directly: "Show me a dry-run reconcile report for course1."
- Course structure changed broadly: update `course<N>/design/` first, then ask Codex to draft from the updated design or a new course spec.

## Repo Layout

```text
applying-ai-at-work/
  AGENTS.md                      # Codex root guidance and build learnings
  README.md                      # operator overview
  README-BUILDER.md              # technical reference
  .env.example                   # Canvas credentials template

  .agents/skills/                # Codex workflow skills
  .codex/                        # Codex project config and custom agents
  docs/codex-migration/          # migration audit and plan

  canvas_sync/                   # Python Canvas sync layer
  schema/                        # JSON schemas
  briefs/                        # planner pointer files
  context/                       # shared design docs
  context/course-specs/          # optional whole-course build specs
  context/module-specs/          # optional whole-module build specs
  course1/                       # course 1 design, sprints, manifests, PRD
  course2/                       # course 2 design, sprints, manifests, PRD
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

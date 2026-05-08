---
type: page
title: "Course Builder Map"
slug: course-builder-map
artifact_id: course3-sprints-sprint-0-course-builder-map
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 2
points: null
submission_type: none
publish: false
---

# Course Builder Map

The repository turns Canvas course materials into reviewable local files before anything touches Canvas.

The working flow is:

```text
plain-English request -> local Markdown draft -> schema validation -> human review -> explicit Canvas push
```

Your first job in the workflow is to know which layer owns which decision.

## Main repo references

Start with these files:

1. `AGENTS.md`: root agent guidance, style rules, safety rules, and build learnings.
2. `README.md`: operator guide for plain-English Codex workflows.
3. `README-BUILDER.md`: technical reference for setup, skills, agents, schemas, and Canvas sync scripts.
4. `schema/frontmatter.schema.json`: the allowed frontmatter shape for each Canvas artifact.

These files are not course content. They are operating guidance. When they conflict with an idea you had for a workflow, follow the repo guidance unless a maintainer explicitly changes it.

## Course content layer

Course artifacts live under a course folder:

```text
course3/sprints/sprint-0/<slug>.md
course3/sprints/sprint-1/<slug>.md
course3/sprints/sprint-2/<slug>.md
course3/sprints/sprint-3/<slug>.md
```

Each artifact has YAML frontmatter followed by Canvas-native Markdown. Canvas IDs do not belong in artifact frontmatter. Canvas IDs belong in the manifest after a push.

For this staged course, the manifest path is:

```text
course3/manifests/production.json
```

That file tells the sync layer which Canvas course the local course maps to. You inspect it when orienting yourself, but you do not hand-edit it during normal drafting.

## Workflow layer

Codex skills live in:

```text
.agents/skills
```

Skills define repeatable workflows such as `build-course`, `build-sprint`, `sync`, `inspect-canvas`, `reconcile`, and `remove-canvas`.

Specialized Codex agents live in:

```text
.codex/agents
```

Agents provide role-specific instructions, such as course drafting, course configuration, Canvas inspection, and Canvas removal. They are useful when a task benefits from a separate role and a focused context window.

Project-scoped Codex settings live in:

```text
.codex/config.toml
```

That file keeps the project conservative because Canvas writes are real side effects.

## Script layer

The deterministic Python scripts live in:

```text
canvas_sync
```

Use this mental model:

- `canvas_sync/schema.py` checks local artifacts, manifests, and PRDs.
- `canvas_sync/init_course.py` creates a local course shell for an existing Canvas course.
- `canvas_sync/inspect_canvas.py` reads Canvas and can write a local ledger.
- `canvas_sync/pull.py` pulls Canvas-side drift back into local Markdown after approval.
- `canvas_sync/push.py` writes reviewed local artifacts to Canvas and updates the manifest.
- `canvas_sync/remove.py` removes manifest-backed Canvas items only after inspection, dry run, and confirmation.

Codex can help you choose the right workflow, but these scripts own the mechanical work.

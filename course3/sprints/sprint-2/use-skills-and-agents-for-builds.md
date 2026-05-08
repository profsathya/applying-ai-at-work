---
type: page
title: "Use Skills and Agents for Builds"
slug: use-skills-and-agents-for-builds
artifact_id: course3-sprints-sprint-2-use-skills-and-agents-for-builds
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 3
points: null
submission_type: none
publish: false
---

# Use Skills and Agents for Builds

This repo uses skills for repeatable workflows and agents for role-specialized work.

You can usually ask in plain language. Codex should route the request through the right skill. When you need to be explicit, name the workflow in your request.

## Skills

Skills live in:

```text
.agents/skills
```

Common build-related skills include:

- `build-course`: builds a complete course from pasted context or a course spec.
- `build-sprint`: builds one sprint or module from pasted context or a module spec.
- `add-artifact`: adds one artifact to an existing course.
- `canvas-author`: writes exactly one artifact from a PRD-shaped item.
- `sync`: validates and pushes reviewed files to Canvas after approval.

Common maintenance skills include:

- `inspect-canvas`: reads live Canvas state and writes a local ledger.
- `reconcile`: dry-runs Canvas drift, then applies only after approval.
- `remove-canvas`: inspects, dry-runs, and removes manifest-backed Canvas targets only after confirmation.

## Agents

Agents live in:

```text
.codex/agents
```

Common agents include:

- `course-drafter.toml`: full-course and sprint drafting through build skills.
- `course-configurator.toml`: local course shell setup through `configure-course` and `init_course.py`.
- `canvas-author.toml`: focused single-artifact authoring.
- `canvas-inspector.toml`: read-only Canvas inventory and reconcile readiness.
- `canvas-remover.toml`: guarded destructive removal workflow.

Agents are not a replacement for deterministic scripts. They help Codex hold the right role and context. The scripts still perform validation, inspection, push, pull, and removal.

## How to ask for the right thing

If you are drafting, give source context and stop before Canvas:

```text
Use the build-sprint workflow to draft course3 sprint 3 from the notes below. Keep edits under course3/sprints/sprint-3. Validate files and stop before Canvas.
```

If you are publishing, name the reviewed files and manifest:

```text
Push these reviewed files to Canvas using course3/manifests/production.json: course3/sprints/sprint-2/example.md
```

If you are inspecting, keep it read-only:

```text
Inspect course3 on Canvas with module items and update the local ledger. Do not push, pull with apply, or remove anything.
```

The request shape matters because it tells Codex which side effects are allowed.

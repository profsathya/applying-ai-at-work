---
type: page
title: "Safety Boundaries and Human Review"
slug: safety-boundaries-and-human-review
artifact_id: course3-sprints-sprint-0-safety-boundaries-and-human-review
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 4
points: null
submission_type: none
publish: false
---

# Safety Boundaries and Human Review

This repo separates local drafting from Canvas side effects. That separation is the main safety feature.

Local Markdown is safe to draft, inspect, revise, and validate. Canvas writes require explicit human approval because they change the live course.

## Local work

Local work includes:

- Drafting artifacts under `course3/sprints/sprint-<n>/`.
- Running `canvas_sync/schema.py` against one artifact or the full repo.
- Reading `AGENTS.md`, `README.md`, `README-BUILDER.md`, skills, agents, manifests, and design notes.
- Inspecting local diffs before deciding whether to publish.

Local work can still create confusion if it overwrites someone else's edits. Before writing, Codex should inspect the target folder and the git status.

## Read-only Canvas work

Read-only Canvas inspection uses:

```text
canvas_sync/inspect_canvas.py
```

This can read the live course and write a local ledger under the course reports folder. It does not change Canvas. It is the right starting point when you need to know what is live before a reconcile, removal, or publish decision.

## Canvas write work

Canvas writes include:

- `canvas_sync/push.py`: creates or updates Canvas pages, assignments, discussions, quizzes, and module placement.
- `canvas_sync/pull.py --apply`: writes Canvas-side drift back into local Markdown.
- `canvas_sync/remove.py --apply`: deletes manifest-backed Canvas modules or module items after confirmation.

Do not treat these as tests against a production course. Use a known sandbox for experiments. Use this course locally until review is complete.

## Paid API caution

Codex and other AI tools may use paid APIs depending on your environment. Before asking for broad generation, large rewrites, or repeated retries, confirm that you are using the intended account and model settings.

Do not paste secrets into chat. Use placeholders in content and keep real values in local environment files.

Example placeholders:

```text
CANVAS_API_URL=<your-canvas-base-url>
CANVAS_API_TOKEN=<your-canvas-api-token>
OPENAI_API_KEY=<your-openai-api-key>
```

## Review gate

Before Canvas writes, confirm:

1. The local artifacts validate.
2. The full validator passes.
3. The target manifest is the correct manifest.
4. The target Canvas course is the intended course.
5. The human has reviewed the local diff.
6. The current request explicitly approves the push, apply, or remove operation.

That review gate is not ceremony. It is what keeps a staged local build from becoming an accidental live-course change.

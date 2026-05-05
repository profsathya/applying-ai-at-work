---
type: module_header
title: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
slug: module-1-orientation-to-the-repo-codex-and-agentic-workflow
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 1
points: null
submission_type: none
publish: false
---

# Module 1: Orientation to the Repo, Codex, and the Agentic Workflow

This module gives you a working map of the repository and the agentic workflow it supports.

You will learn where guidance lives, what Codex should handle, what deterministic scripts handle, and where the human review boundary sits. The goal is not to memorize every file. The goal is to know how to orient yourself before asking Codex to draft, inspect, reconcile, or publish course content.

By the end of this module, you should be able to:

1. Explain the local Markdown to validation to review to Canvas workflow.
2. Identify the difference between repo guidance, Codex skills, Codex agents, and Canvas sync scripts.
3. Recognize which operations are safe local drafting work and which operations write to Canvas.
4. Write a clear Codex app or IDE request that respects the repo's boundaries.

You will not push anything to Canvas in this module.

## Estimated Time

60 to 90 minutes.

## Audience Note

If you are non-technical, focus on the repo map, safety language, and review responsibilities. If you are technical, also pay attention to file boundaries, local skills, subagents, and deterministic scripts.

## Required Artifacts

Complete these items in order:

1. Course Builder Map
2. Codex App and IDE Workflow
3. Safety Boundaries and Human Review
4. Orientation Workflow Check
5. Repo Inspection Practice

## Learning Sequence

Start by mapping the repo. Then learn how to open the repo in Codex app or an IDE, how to frame safe requests, and how to review before Canvas. Finish by asking Codex to inspect the repo without changing files.

## Formative Check

Complete `Orientation Workflow Check`.

## Applied Task

Complete `Repo Inspection Practice`.

## Completion Criteria

You are done when you can explain the local draft to validation to human review to explicit Canvas push workflow and can write a Codex prompt that inspects before editing.

## Common Misunderstandings

- Canvas is not the draft space. Local Markdown is the draft space.
- You do not need to memorize every skill or subagent name.
- Validation checks structure and guardrails, not full instructional quality.
- A clear prompt still needs human review after Codex finishes.

## Repository-Specific References

- `AGENTS.md`
- `README.md`
- `README-BUILDER.md`
- `.agents/skills/`
- `.codex/agents/`
- `canvas_sync/`
- `course3/shared/repo-map.md`

## Codex App Or IDE Workflow Notes

Open the repo root, ask Codex to inspect before acting, and require Codex to list the route, file scope, risk, and verification plan before local edits.

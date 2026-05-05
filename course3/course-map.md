# Course Map

## Four-Module Overview

This course teaches team members to operate the repository through Codex app or Codex in an IDE. The repo names its Canvas module folders `sprints`, so each module below maps to one sprint folder.

| Module | Repo folder | Estimated time | Main outcome |
|---|---|---:|---|
| 1. Orientation to the Repo, Codex, and the Agentic Workflow | `course3/sprints/sprint-0/` | 60 to 90 minutes | Explain the repo, Codex surfaces, agentic workflow, and review responsibilities. |
| 2. Setup, Configuration, and Safe First Run | `course3/sprints/sprint-1/` | 75 to 120 minutes | Prepare local dependencies and run a safe local-only workflow. |
| 3. Building and Publishing Content with Codex and Agents | `course3/sprints/sprint-2/` | 90 to 150 minutes | Draft or simulate content changes with Codex and route to local skills or subagents. |
| 4. Verification, Maintenance, and Extension | `course3/sprints/sprint-3/` | 90 to 150 minutes | Verify outputs, handle drift and failures, and decide when to extend the workflow. |

Total estimated learner time: 5.25 to 8.5 hours.

## Learning Progression

1. Understand the repository and why Canvas writes are separated from local drafting.
2. Prepare the local environment and learn which credentials are sensitive.
3. Use Codex to scope, route, draft, review, and optionally prepare content for Canvas.
4. Verify the work, handle drift, maintain course structure, and extend the repo responsibly.

## Module Dependencies

Module 1 is required before the rest. Module 2 should be completed before any technical learner runs validation or Canvas inspection. Module 3 depends on the safety boundaries from Modules 1 and 2. Module 4 depends on learners knowing the difference between draft, inspect, reconcile, push, and remove.

## Artifact Inventory

Each module contains:

- One `module_header`.
- Multiple `page` artifacts.
- One `quiz` formative check.
- One applied task as an `assignment` or `discussion`.

Shared resources live under `course3/shared/` and are not Canvas artifacts unless a maintainer chooses to publish them later.

## Canvas Mapping

Canvas mapping files are included at the course root:

- `canvas-build-plan.md`
- `canvas-module-manifest.md`
- `canvas-page-manifest.md`
- `canvas-assignment-manifest.md`
- `canvas-quiz-manifest.md`

These files describe intended Canvas placement. The production Canvas ID source remains `course3/manifests/production.json`, and that JSON should be updated only by `canvas_sync/push.py` or `canvas_sync/remove.py`.

## Assessment Strategy

Formative checks test practical safety decisions rather than trivia. Applied tasks ask learners to inspect, document, prompt, review, or verify a real repo workflow. The final applied task requires evidence that the learner can scope a safe Codex request, inspect relevant files, choose the right local workflow, and verify the result without publishing to Canvas.

## Technical And Non-Technical Pathways

Non-technical learners focus on safe prompting, review, artifact quality, and escalation. Technical learners add environment setup, schema validation, Canvas inspection, drift checks, and extension decisions.

## Codex App And IDE Usage Pathway

The course assumes learners use either the Codex app or Codex in an IDE. Codex CLI is not taught as the primary interface. Repository commands appear only where this repo requires them for setup, validation, or technical troubleshooting.

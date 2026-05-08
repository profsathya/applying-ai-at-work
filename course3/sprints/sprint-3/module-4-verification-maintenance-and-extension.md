---
type: module_header
title: "Module 4: Verification, Maintenance, and Extension"
slug: module-4-verification-maintenance-and-extension
artifact_id: course3-sprints-sprint-3-module-4-verification-maintenance-and-extension
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 1
points: null
submission_type: none
publish: false
---

# Module 4: Verification, Maintenance, and Extension

This module covers the workflows that keep a live course aligned and safe over time.

You will learn how to inspect Canvas, handle drift, remove content with guardrails, and propose workflow extensions without weakening the safety model.

By the end of this module, you should be able to:

1. Use read-only inspection before deciding whether to push, pull, or remove.
2. Explain the dry-run and approval pattern for reconcile and removal.
3. Identify what belongs in skills, agents, schemas, and scripts.
4. Propose a small workflow extension with validation and rollback thinking.

## Estimated Time

90 to 150 minutes.

## Audience Note

If you are non-technical, focus on inspect-first decisions, dry-run review, and when to escalate. If you are technical, also inspect ledger outputs, reconcile behavior, removal targets, schema boundaries, and extension ownership.

## Required Artifacts

Complete these items in order:

1. Inspect Before You Change
2. Reconcile and Remove Safely
3. Extend the Workflow
4. Verification and Maintenance Check
5. Workflow Extension Proposal

## Learning Sequence

Start with read-only Canvas inspection. Then learn how reconcile and removal use dry-run and approval gates. Next, study how to extend the repo without weakening safety. Finish by proposing a narrow, verifiable extension.

## Formative Check

Complete `Verification and Maintenance Check`.

## Applied Task

Complete `Workflow Extension Proposal`.

## Completion Criteria

You are done when you can choose between inspect, reconcile, push, and remove, explain the approval gates, and propose an extension with read scope, write scope, validation, rollback, and stop conditions.

## Common Misunderstandings

- Inspection is read-only against Canvas, but it can still write local ledger files.
- Reconcile apply changes local Markdown and should follow a dry run.
- Removal is destructive on Canvas even though local Markdown is kept.
- A new agent is not the right fix for every workflow gap.

## Repository-Specific References

- `.agents/skills/inspect-canvas/SKILL.md`
- `.agents/skills/reconcile/SKILL.md`
- `.agents/skills/remove-canvas/SKILL.md`
- `.codex/agents/canvas-inspector.toml`
- `.codex/agents/canvas-remover.toml`
- `canvas_sync/inspect_canvas.py`
- `canvas_sync/pull.py`
- `canvas_sync/remove.py`

## Codex App Or IDE Workflow Notes

Ask Codex to inspect before changing a live-course workflow. Require dry-run output before reconcile apply or Canvas removal, and require explicit approval for any side effect.

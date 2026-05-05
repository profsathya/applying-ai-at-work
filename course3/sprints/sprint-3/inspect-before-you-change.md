---
type: page
title: "Inspect Before You Change"
slug: inspect-before-you-change
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 2
points: null
submission_type: none
publish: false
---

# Inspect Before You Change

Inspection is the safest first move when Canvas may differ from local Markdown.

The read-only inspection script is:

```text
canvas_sync/inspect_canvas.py
```

The matching skill is:

```text
.agents/skills/inspect-canvas/SKILL.md
```

The matching agent is:

```text
.codex/agents/canvas-inspector.toml
```

## What inspection answers

Inspection can help answer:

- What modules exist on Canvas?
- What module items exist on Canvas?
- Which local files map to Canvas items through the manifest?
- Which Canvas items are not represented locally?
- Which local files are not present on Canvas?
- Are there possible drift issues that need review before a push?

## Typical read-only inspection request

Use the app or IDE and keep the boundary explicit:

```text
Inspect course3 on Canvas using course3/manifests/production.json. Include module items and write the local ledger. Do not push, pull with apply, or remove anything.
```

The workflow uses a command shaped like this:

```text
canvas_sync/inspect_canvas.py --manifest course3/manifests/production.json --include-items --write-ledger --format markdown
```

Add drift reporting only when you need reconcile readiness:

```text
canvas_sync/inspect_canvas.py --manifest course3/manifests/production.json --include-items --drift --write-ledger --format markdown
```

## What to do with the ledger

Read the ledger before you decide on next action.

If local Markdown is behind Canvas, use the reconcile workflow. If Canvas has unexpected items, investigate before pushing. If you are preparing removal, use the ledger to select manifest-backed targets.

Inspection should make your next action narrower, not broader.

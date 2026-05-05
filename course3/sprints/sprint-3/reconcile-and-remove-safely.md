---
type: page
title: "Reconcile and Remove Safely"
slug: reconcile-and-remove-safely
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 3
points: null
submission_type: none
publish: false
---

# Reconcile and Remove Safely

Live courses can drift. Someone may edit Canvas directly, delete an item, rename a module, or change assignment details. This repo treats Canvas as the source to inspect when a course is live.

## Reconcile

Reconcile pulls Canvas-side changes back into local Markdown.

The script is:

```text
canvas_sync/pull.py
```

The skill is:

```text
.agents/skills/reconcile/SKILL.md
```

The safe sequence is:

1. Inspect Canvas.
2. Run a dry run.
3. Review the drift report.
4. Apply only after explicit human approval.
5. Validate changed artifacts.

The dry-run command shape is:

```text
canvas_sync/pull.py --manifest course3/manifests/production.json --dry-run
```

The apply command shape is:

```text
canvas_sync/pull.py --manifest course3/manifests/production.json --apply
```

Do not apply drift without reviewing the dry run first.

## Remove

Removal deletes manifest-backed Canvas content. It is destructive on Canvas, even though local Markdown files are kept.

The script is:

```text
canvas_sync/remove.py
```

The skill is:

```text
.agents/skills/remove-canvas/SKILL.md
```

The agent is:

```text
.codex/agents/canvas-remover.toml
```

The safe sequence is:

1. Inspect Canvas and write a ledger.
2. Select manifest-backed targets.
3. Run a dry-run removal plan.
4. Review operations, blocked targets, manifest entries, and local files kept.
5. Apply only when the human repeats the current confirmation token.

Accepted target forms include:

```text
module_id:<canvas_module_id>
module_position:<position>
module_item_id:<module_item_id>
file:<repo-relative-md-path>
```

Do not remove Canvas-only targets in the current workflow. Do not delete local Markdown files as part of Canvas removal.

## Push after drift

If Canvas was edited directly, inspect and reconcile before pushing local changes. A push can overwrite the targeted Canvas item. That is useful when intended and risky when accidental.

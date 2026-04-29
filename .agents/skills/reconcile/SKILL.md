---
name: reconcile
description: Pull Canvas-side drift back into local Markdown by running dry-run first, then applying only after explicit user approval.
---

# Reconcile Skill

Canvas wins on live-course drift. This workflow pulls Canvas changes back into the repo.

## Workflow

1. Resolve target course and manifest.
2. Run dry-run first:

   ```bash
   python3 canvas_sync/pull.py --manifest <manifest_path> --dry-run
   ```

3. Show the drift report to the user.
4. Ask whether to apply all, none, or a specific subset.
5. Apply only after explicit approval:

   ```bash
   python3 canvas_sync/pull.py --manifest <manifest_path> --apply
   ```

6. Review local changes before commit.

## Rules

- Never apply drift without showing dry-run output first.
- Never modify Canvas during reconcile.
- Do not delete local MD files automatically when Canvas reports an orphan.
- Validate changed artifacts after apply when feasible.

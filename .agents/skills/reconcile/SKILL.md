---
name: reconcile
description: Pull Canvas-side drift back into local Markdown by running dry-run first, then applying only after explicit user approval.
---

# Reconcile Skill

Canvas wins on live-course drift. This workflow pulls Canvas changes back into the repo.

## Workflow

1. Resolve the target course and manifest. For GitOps courses, use a current checkout of `canvas-state` and pass `--state-dir <state_dir>` below. Omit it only for an explicitly legacy deployment. Missing external state must not fall back to old manifest mappings.
2. Run dry-run first:

   ```bash
   python3 canvas_sync/pull.py --manifest <manifest_path> --state-dir <state_dir> --dry-run
   ```

3. Show the drift report to the user.
4. Show blocked files and the confirmation token. For a subset, rerun dry-run with one or more `--file <repo-relative-path>` arguments and use that subset's token. Local/Canvas conflicts and hosted wrapper changes require explicit resolution before apply.
5. Apply only after explicit approval:

   ```bash
   python3 canvas_sync/pull.py --manifest <manifest_path> --state-dir <state_dir> --apply --confirm-token <token>
   ```

6. Review local changes and the reported backup directory. Validate the selected state with `schema.py --state <state-file>`. Retain the state update with the reconciled source so later publishes use the new Canvas baseline. If sprint content changed and the course has `homepage.yaml`, route through `homepage-maintainer` before final schema validation.

## Rules

- Never apply drift without showing dry-run output first.
- Never modify Canvas during reconcile.
- Do not delete local MD files automatically when Canvas reports an orphan.
- The script validates candidate Markdown before replacing files and preserves backups. A changed source, state, or Canvas snapshot invalidates the dry-run token.
- Hosted Canvas wrappers never replace the Markdown body. Native quiz question changes are reported for explicit supported-question import, not silently dropped.

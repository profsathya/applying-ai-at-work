---
description: Pull canvas edits back into local MD files (Canvas-wins drift resolution).
---

Reconcile canvas drift: pull any changes made directly in canvas back into local MD files.

Arguments: `$ARGUMENTS` (optional: specific artifact slug, or blank for full reconcile)

Workflow:

1. Determine the active manifest from `courses/<course-slug>/manifests/`.
2. Invoke `canvas-puller` in `--dry-run` mode. Show the diff report to the user.
3. Ask the user: "Apply these changes? (yes/no/partial)"
   - `yes`: invoke `canvas-puller` with `--apply` on all drifted artifacts.
   - `no`: exit without changes.
   - `partial`: ask which artifacts to apply, then run `--apply` on just those.
4. After applying, review the MD changes one more time with the user before committing.
5. Commit changes with message: `chore: pull canvas drift (<N> artifacts reconciled)`.

Never apply changes without showing the diff first. Never commit without user confirmation when in partial mode.

If any artifact shows as `orphaned` (exists in manifest but gone from canvas), ask whether to delete the MD file or keep it as an archive.

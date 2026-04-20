---
description: Push one or more MD artifacts to canvas. Use after manually editing an MD file.
---

Push the specified markdown file(s) to canvas using the active manifest.

Arguments: `$ARGUMENTS` (file path, or comma-separated paths)

Workflow:

1. Determine the active manifest from `courses/<course-slug>/manifests/`. If multiple exist, ask which instance to target.
2. For each file path in $ARGUMENTS:
   a. Invoke `schema-validator` on the file.
   b. If validation passes, invoke `canvas-pusher` with the file path and manifest path.
   c. Report the canvas_id and action (created/updated).
3. If any push fails, report the error and stop. Do not attempt to roll back previous pushes in the batch.
4. Commit changes with message: `sync: <N> artifact(s) pushed to canvas`.

Never push a file that fails schema validation. Never bypass the validator.

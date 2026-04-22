---
description: Build a complete sprint/module from a context doc, inferring scaffolding from existing sprints. Produces MD files for review before push.
---

Build a complete sprint for an existing course based on a context document. Arguments: `$ARGUMENTS` (should include a context doc path, a target course, and a sprint number - ask if any are missing).

Workflow:

1. Confirm target course, sprint number, and context doc path with the user before invoking the agent. Show them what you will pass in.
2. Invoke `sprint-module-builder`. Show the returned summary.
3. For each file written, invoke `schema-validator`. If any fail, report the errors and stop. Do not auto-fix - the user decides whether to edit the MD files or re-invoke the builder with refined context.
4. Show the user the list of files written and ask: "Review the MD files before pushing? (yes/no - recommend yes)"
5. If yes: list the file paths and wait for the user to confirm they are ready to push. Never push without explicit confirmation.
6. On push confirmation: for each file, invoke `canvas-pusher` with the active manifest (`<target>/manifests/production.json`).
7. After pushes complete, ask whether to append the new artifacts to `<target>/prd.json` as `status: done` items. Some sprint additions belong in the PRD (so `/reconcile` and audit tooling see them); some are ad-hoc and do not. Let the user decide.
8. Commit all changes with message: `feat: build sprint-<n> in <target> (<N> artifacts)`.

Never skip schema validation. Never push without user confirmation. If the user's context doc is ambiguous about sprint number or target, stop and ask.

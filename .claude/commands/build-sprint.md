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
8. Append the sprint build log to `<target>/progress.md`:
   1. Append a blank line, then a section header `## Sprint <n> added post-build (<iso-timestamp>)`, then a blank line. Use ISO 8601 UTC.
   2. For each successfully pushed file, append one line in push order:
      - module_headers: `BUILT <title>, canvas module ID <id>, <iso-timestamp>.`
      - other types: `BUILT <title>, canvas ID <id>, <iso-timestamp>.`
      - `<title>` is the artifact's frontmatter `title`. Timestamps reflect when each push succeeded, not when the command was invoked.
   3. For any files that failed to push, append `FAILED <title>, <error summary truncated to 120 chars>, <iso-timestamp>.` in the same section.
   4. After the last BUILT/FAILED line, append one summary line: `(sprint-<n> built via /build-sprint from context doc: <context-doc-path>)`.

   Only append when canvas was actually called. If the user declined the push in step 5, skip this step entirely - `progress.md` tracks canvas state, not local drafts.

   If `<target>/progress.md` does not exist, stop and report an error - the course was never planned.

   If the progress.md append itself fails, do not roll back any canvas push. Report the failure and proceed with the commit - canvas state is correct, only the local log is stale.

9. Commit all changes with message: `feat: build sprint-<n> in <target> (<N> artifacts)`.

Never skip schema validation. Never push without user confirmation. If the user's context doc is ambiguous about sprint number or target, stop and ask.

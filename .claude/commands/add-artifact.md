---
description: Add one new artifact (assignment, page, discussion, quiz) to an existing course using natural language.
---

Add one new artifact to an existing course based on a natural-language description.

Arguments: `$ARGUMENTS` (description of what to add, e.g., "15-point reflection in week 10 called Mid-sprint check")

Workflow:

1. Parse the natural-language request. Identify:
   - Course (if not inferrable, ask which one)
   - Artifact type (assignment, page, discussion, quiz, module_header)
   - Sprint and week
   - Title
   - Points (if applicable)
   - Submission type (infer from type, or ask if ambiguous)
   - Body brief (what the artifact should cover)

2. Look up the course's existing PRD to determine the next `id` and appropriate `position` within the target module.

3. Construct a single PRD-shaped item (same schema as PRD entries). Do NOT append to the original PRD (that one is frozen post-planning). Instead, pass the item directly to `canvas-author`.

4. Invoke `canvas-author` with the constructed item. It writes the MD file.

5. Invoke `schema-validator` on the new file.

6. Invoke `canvas-pusher`. Canvas creates the artifact and returns the ID.

7. Append the new artifact to the manifest.

8. Append one line to `<target>/progress.md` using the format the Ralph loop already uses:
   - For module_headers: `BUILT <title>, canvas module ID <id>, <iso-timestamp>.`
   - For all other types: `BUILT <title>, canvas ID <id>, <iso-timestamp>.`
   - Use ISO 8601 UTC for the timestamp (e.g., `2026-05-10T14:22:00Z`). Use the time the push succeeded, not when the command was invoked.
   - `<title>` is the artifact's frontmatter `title`, not the slug or path.
   - Do not add a header, section break, or leading bullet. One line, appended to the end of the file.

   Then append a second line: `  (added mid-build via /add-artifact, <short reason from user input>)`. The leading two spaces are intentional and visually distinguish post-build additions from initial-build entries without breaking grep.

   On push failure (step 6 returned an error): append `FAILED <title>, <error summary truncated to 120 chars>, <iso-timestamp>.` instead. Do not append the mid-build context line on failure.

   Only append when canvas was actually called. If the user declined the push or no canvas call happened, skip this step.

   If `<target>/progress.md` does not exist, stop and report an error - the course was never planned.

   If the progress.md append itself fails (permissions, disk), do not roll back the canvas push. Report the failure and proceed with the commit - canvas state is correct, only the local log is stale.

9. Commit with message: `feat: add <artifact-title>`.

Never push without validation. Never skip the schema check. If the user's description is ambiguous (no sprint, no points on an assignment, etc.), ask one clarifying question before proceeding.

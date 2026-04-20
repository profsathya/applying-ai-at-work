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

8. Append to `progress.md`: "Added <title> mid-build, canvas ID <id>, <timestamp>."

9. Commit with message: `feat: add <artifact-title>`.

Never push without validation. Never skip the schema check. If the user's description is ambiguous (no sprint, no points on an assignment, etc.), ask one clarifying question before proceeding.

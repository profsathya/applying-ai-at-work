---
name: update-artifact
description: Prepare exactly one live Canvas module item for local Markdown editing by module_item_id, validate the edit, and stop before any Canvas push.
---

# Update Artifact Skill

Use this when an instructor wants to update one existing Canvas artifact by Canvas course ID and `module_item_id`.

This workflow may read Canvas and update one local Markdown file plus its manifest mapping. It must not push to Canvas.

## Workflow

1. Resolve the Canvas course ID from the request.
2. List live module items:

   ```bash
   python3 canvas_sync/update_artifact.py list --course-id <canvas_course_id> --format markdown
   ```

3. Ask the instructor for the `module_item_id` if they have not already provided one.
4. Prepare the selected artifact:

   ```bash
   python3 canvas_sync/update_artifact.py prepare --course-id <canvas_course_id> --module-item-id <module_item_id>
   ```

5. If prepare returns `status: sprint_required`, ask for sprint `0` through `5`, then rerun:

   ```bash
   python3 canvas_sync/update_artifact.py prepare --course-id <canvas_course_id> --module-item-id <module_item_id> --sprint <n>
   ```

6. Ask what should change in the prepared file.
7. Edit only the prepared artifact Markdown file.
8. Allowed edits:
   - body text
   - title
   - points
   - publish
   - due
   - rubric
   - quiz questions
9. Do not edit these identity fields:
   - type
   - slug
   - sprint
   - module
   - position
10. Validate the artifact:

    ```bash
    python3 canvas_sync/schema.py --artifact <prepared_file>
    python3 canvas_sync/update_artifact.py verify --course-id <canvas_course_id> --module-item-id <module_item_id> --file <prepared_file>
    ```

11. Report the file path and validation result.
12. Stop before Canvas writes. If the instructor later explicitly asks to push this reviewed artifact, use the `sync` skill.

## Rules

- The instructor-facing selector is `module_item_id`.
- The Canvas course ID must match exactly one local production manifest.
- If the selected item is Canvas-only, import it before editing.
- Never edit Canvas directly from this workflow.
- Never push the prepared file unless the instructor gives a separate explicit push request.

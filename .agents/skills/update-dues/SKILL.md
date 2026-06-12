---
name: update-dues
description: Update due dates on one or more course artifacts from a path, mapping file, or natural language request, then validate and optionally push.
---

# Update Dues Skill

Update only the `due` field in artifact frontmatter.

## Workflow

1. Resolve target files under `course*/sprints/sprint-*/*.md`.
2. Only update assignments, quizzes, and graded discussions.
3. Normalize every written due date to `YYYY-MM-DDTHH:MM:SSZ`.
4. If the target set is ambiguous, list candidates and stop.
5. Edit only the `due` line. If adding a due date, insert it near `submission_type`.
6. Validate each changed file:

   ```bash
   python3 canvas_sync/schema.py --artifact <file>
   ```

7. Ask before pushing due-date changes to Canvas.
8. Push changed files through the `sync` skill only after confirmation. If `hosted_html.enabled` is true, the push must include `--hosted-output-dir ../common-curriculum`.

## Rules

- Do not edit body content or unrelated frontmatter.
- Markdown is the source of truth. Do not hand-edit generated Common Curriculum HTML or activity JSON.
- Do not add `due: null`; remove the key when clearing a due date.
- Do not push files that fail schema validation.
- Do not guess vague dates like "sometime next week"; ask for a concrete date.

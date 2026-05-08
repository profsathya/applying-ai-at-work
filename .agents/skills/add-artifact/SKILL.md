---
name: add-artifact
description: Add one new assignment, page, discussion, quiz, or module header to an existing course from a natural-language request.
---

# Add Artifact Skill

Add exactly one new Canvas artifact to an existing course.

## Workflow

1. Parse the request for course, sprint, week, title, artifact type, points, submission type, and body brief.
2. If course or required grading details are ambiguous, ask one concise clarification before writing. If the request is for a new standalone module and no sprint is named, use the next unused local sprint number by listing `<course>/sprints/sprint-*`; otherwise ask when sprint placement is ambiguous.
3. Read the target course PRD to infer the next id and module position, but do not append to the frozen PRD unless the user explicitly asks.
4. Create one PRD-shaped item and invoke the `canvas-author` workflow or agent to write one MD file.
5. Run:

   ```bash
   python3 canvas_sync/schema.py --artifact <md_file_path>
   ```

6. Ask for confirmation before pushing to Canvas unless the user explicitly requested an immediate push.
7. For production, stop after validation so the reviewed branch can publish through GitHub Actions after merge. For an approved direct admin or sandbox push, run `python3 canvas_sync/push.py --file <file> --manifest <manifest>`.
8. Append a `BUILT` or `FAILED` line to `<target>/progress.md` only if Canvas was called.
9. Commit only when the user requested commit behavior or the surrounding workflow requires it.

## Rules

- One artifact per invocation.
- No Canvas push without schema validation.
- No edits to `context/`, `course*/design/`, `archive/`, or schema files.
- Omit `due` unless the request provides a full ISO 8601 timestamp with timezone.

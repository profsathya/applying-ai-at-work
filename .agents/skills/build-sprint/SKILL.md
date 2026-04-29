---
name: build-sprint
description: Build a complete sprint/module from a context document, infer scaffolding from existing sprints, validate generated MD, and optionally push after review.
---

# Build Sprint Skill

Build one sprint worth of artifacts for an existing course.

## Required Inputs

- Context document path
- Target course: `course1` or `course2`
- Sprint number: `0` through `5`

Ask before writing if any input is missing.

## Workflow

1. Confirm the target course, sprint number, and context doc path with the user.
2. Read the context doc, `AGENTS.md`, relevant course design docs, shared context docs, schemas, and existing built sprints.
3. If the target course has no built sprints, infer scaffolding from `course1` and say so.
4. Write MD files only under `<target>/sprints/sprint-<n>/`.
5. Validate every written file:

   ```bash
   python3 canvas_sync/schema.py --artifact <file>
   ```

6. Show the file list and validation result. Ask the user to review before pushing.
7. Push only after explicit confirmation, one file at a time, through `canvas_sync/push.py`.
8. Append a post-build section to `<target>/progress.md` only if Canvas was called.

## Rules

- Do not modify PRD or manifest directly.
- Do not push before human review and confirmation.
- Use Canvas-native Markdown only.
- Do not write due dates unless explicitly provided.

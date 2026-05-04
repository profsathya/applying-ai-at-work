---
name: build-course
description: Build a complete course from pasted context or a course context spec file, generate all sprint/module Markdown locally, validate everything, and optionally push after review.
---

# Build Course Skill

Build a full course worth of Canvas artifact Markdown for an existing target course.

This workflow is intentionally single-pass at the local file layer: generate the course files first, validate them, show the human what changed, and only then consider Canvas writes.

## Required Inputs

- Target course: any existing local course directory, for example `course1`, `course2`, `course3`, or a named course key
- Course context, supplied in one of two ways:
  - Inline pasted context in the user's request
  - A Markdown file path, preferably under `context/course-specs/`

If the user gives a target course but no context source, look for exactly one matching file:

```text
context/course-specs/<course>-*.md
```

Use it if exactly one match exists. Ask before writing if there is no match, more than one match, or the target course is still ambiguous.

## Course Context Spec

Use `context/course-specs/README.md` as the recommended spec. A full spec may include course goals, audience, module map, artifact list by sprint, required ideas, assessment strategy, constraints, tone, source material, and open questions.

If the user pastes context directly into chat, use it as the course context. Do not require a file path. If the user supplies a file path, read that file first. If the user relies on folder lookup, report which spec file was selected before writing.

## Workflow

1. Confirm the target course and course context source.
2. Read the course context if it is a file. If it is pasted inline, treat the pasted text as the source.
3. Read `context/course-specs/README.md`, `context/module-specs/README.md`, `AGENTS.md`, relevant course design docs, shared context docs, schemas, and existing built sprints.
4. Treat explicit course context instructions as higher priority than inferred sprint patterns, unless they violate repo rules or schema constraints.
5. Generate or update Markdown files under `<target>/sprints/sprint-<n>/` only.
6. Stay within sprint numbers `0` through `5` unless the schema is deliberately changed in a separate user-approved task.
7. Validate every written file:

   ```bash
   python3 canvas_sync/schema.py --artifact <file>
   ```

8. Run the full repo validator:

   ```bash
   python3 canvas_sync/schema.py --all
   ```

9. Show the file list, artifact types, and validation result. Ask the user to review before pushing.
10. Push only after explicit confirmation, one file at a time, through `canvas_sync/push.py`.
11. Append a post-build section to `<target>/progress.md` only if Canvas was called.

## Rules

- Do not require or create a PRD unless the user explicitly asks for one.
- Do not modify manifests directly.
- Do not push before human review and confirmation.
- Use Canvas-native Markdown only.
- Do not write due dates unless explicitly provided.
- Do not edit files under `context/course-specs/` or `context/module-specs/` unless the user explicitly asks to create or update a spec.

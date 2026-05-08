---
name: build-sprint
description: Build a complete sprint/module from pasted context or a module context spec file, infer scaffolding from existing sprints, validate generated MD, and optionally push after review.
---

# Build Sprint Skill

Build one sprint worth of artifacts for an existing course.

## Required Inputs

- Target course: any existing local course directory, for example `course1`, `course2`, `course3`, or a named course key
- Sprint number: any non-negative integer, unless the user asks for a new standalone module and leaves placement to the repo
- Module context, supplied in one of two ways:
  - Inline pasted context in the user's request
  - A Markdown file path, preferably under `context/module-specs/`

If the user gives course and sprint but no context source, look for exactly one matching file:

```text
context/module-specs/<course>-sprint-<n>-*.md
```

Use it if exactly one match exists. Ask before writing if there is no match, more than one match, or any required input is still missing.

If the user asks to add a new standalone module but does not name a sprint number, use the next unused local sprint number by listing `<course>/sprints/sprint-*` and choosing one greater than the highest existing number.

## Module Context Spec

Use `context/module-specs/README.md` as the recommended spec. A full spec may include target, purpose, audience, artifact list, required ideas, prompts, constraints, tone, source material, and open questions.

If the user pastes context directly into chat, use it as the module context. Do not require a file path. If the user supplies a file path, read that file first. If the user relies on folder lookup, report which spec file was selected before writing.

## Workflow

1. Confirm the target course, sprint number or next unused sprint selection, and module context source with the user.
2. Read the module context if it is a file. If it is pasted inline, treat the pasted text as the source.
3. Read `context/module-specs/README.md`, `AGENTS.md`, relevant course design docs, shared context docs, schemas, and existing built sprints.
4. Treat explicit module context instructions as higher priority than inferred sprint patterns, unless they violate repo rules or schema constraints.
5. If the target course has no built sprints, infer scaffolding from a comparable built course such as `course1` and say so.
6. Write MD files only under `<target>/sprints/sprint-<n>/`.
7. Validate every written file:

   ```bash
   python3 canvas_sync/schema.py --artifact <file>
   ```

8. Show the file list and validation result. Ask the user to review before pushing.
9. For production, stop after validation and review so merge to `main` can publish through the protected GitHub Actions workflow. Use direct `canvas_sync/push.py` only for an approved admin or sandbox push.
10. Append a post-build section to `<target>/progress.md` only if Canvas was called.

## Rules

- Do not modify PRD or manifest directly.
- Do not push before human review and confirmation. Prefer the GitOps publish workflow for production courses.
- Use Canvas-native Markdown only.
- Do not write due dates unless explicitly provided.
- Do not edit files under `context/module-specs/` unless the user explicitly asks to create or update a spec.

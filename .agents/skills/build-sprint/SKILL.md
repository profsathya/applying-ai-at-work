---
name: build-sprint
description: Build a sprint/module from human context, a Google Doc file link, DOCX, ZIP, or module spec; preserve source wording, validate local artifacts, and prepare a reviewed Canvas handoff.
---

# Build Sprint Skill

Build one sprint worth of artifacts for an existing course.

## Required Inputs

- Target course: any existing local course directory, for example `course1`, `course2`, `course3`, or a named course key
- Sprint number: any non-negative integer, unless the user asks for a new standalone module and leaves placement to the repo
- Module context, supplied in any of these ways:
  - Inline pasted context in the user's request
  - A Markdown file path, preferably under `context/module-specs/`
  - One Google Doc file link, a local DOCX, a ZIP of exported documents, or a source packet

For document inputs, follow [Document Intake](../../../docs/DOCUMENT_INTAKE.md) before authoring. Authors do not prepare internal YAML or Markdown. Use the Google Drive read tools for native tabs/comments when accessible; use the bounded public DOCX export or downloaded file as a documented fallback. Never treat flattened paragraph text as a complete tracked-changes source.

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

1. Establish the target course, sprint placement, and source from the request and repository. Ask only for missing information that matters. For an authorized alternative to an existing live sprint, use the next unused storage sprint, retain the semantic title, and keep `publish: false`.
2. Read the module context if it is a file. If it is pasted inline, treat the pasted text as the source.
3. Read `context/module-specs/README.md`, `AGENTS.md`, relevant course design docs, shared context docs, schemas, and existing built sprints.
4. Treat explicit module context instructions as higher priority than inferred sprint patterns, unless they violate repo rules or schema constraints.
   - If the context asks for AI-powered quiz or discussion activities, author them as `delivery_mode: ai_activity` with `submission_type: file_upload` and `ai_activity.questions`; do not create native Canvas quiz `questions` for those items.
5. If the target course has no built sprints, infer scaffolding from a comparable built course such as `course1` and say so.
6. For document inputs, build a source map and use `canvas_sync/source_build.py` to preserve selected blocks with adjacent source evidence. Mark newly authored prose, question/configuration metadata, heading changes, and cross-reference adaptations. Source sequence and scope override inferred artifact counts; do not invent a missing half of a sprint. Write authorized course builds under `<target>/sprints/sprint-<n>/`, or use an ignored preview directory when the user requests a demonstration. Never overwrite an existing live sprint as a side effect of intake.
   - Record exact tracked-edit/version choices and local comment resolutions; do not mutate source comments. Source review notes, raw configuration, keys, and draft banners stay out of learner prose.
   - Preserve human punctuation in verified source segments. Newly written text follows repository style. Do not paraphrase to pass validation.
   - Read current Common Curriculum mechanisms when the user provides an assessment reference; do not assume a native Canvas quiz or an AI activity is the intended mechanism.
   - For the Common Curriculum task/response/copy pattern, use `delivery_mode: guided_assignment`, `type: assignment`, and `submission_type: text_entry`. Follow the configuration and service limitations in Document Intake. This supports formative choice checks as well as response tasks; neither browser completion counts nor AI feedback are Canvas grades. Keep the first own-thinking activity free of AI requests.
   - For actual course artifacts, route through `homepage-maintainer` before final validation. Keep alternate drafts closed and unpublished in metadata.
7. Validate every written file:

   ```bash
   python3 canvas_sync/schema.py --artifact <file>
   ```

8. Inspect the rendered participant experience locally. Show the file list, source/adaptation decisions, material remaining questions, and validation result. Ask for review only when needed for a next action; do not stop before completing already authorized local work. Publishing requires the existing explicit confirmation.
9. For production, stop after validation and review so merge to `main` can publish through the protected GitHub Actions workflow. That workflow renders Common Curriculum hosted files before Canvas is updated.
10. Use direct `canvas_sync/push.py` only for an approved admin or sandbox push. If `hosted_html.enabled` is true, route through the `sync` skill so the push includes `--hosted-output-dir ../common-curriculum`.
11. Append a post-build section to `<target>/progress.md` only if Canvas was called.

## Rules

- Do not modify PRD or manifest directly.
- Do not push before human review and confirmation. Prefer the GitOps publish workflow for production courses.
- Markdown files under `<target>/sprints/` are the source of truth. Common Curriculum HTML and activity JSON are generated output.
- Use Canvas-native Markdown only.
- Do not write due dates unless explicitly provided.
- Do not edit files under `context/module-specs/` unless the user explicitly asks to create or update a spec.

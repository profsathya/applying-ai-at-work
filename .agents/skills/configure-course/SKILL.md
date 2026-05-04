---
name: configure-course
description: Configure a new local course shell for an existing Canvas course ID, including directories, manifest, starter metadata, and optional course context, without Canvas writes.
---

# Configure Course Skill

Use this when a human asks to add, initialize, configure, scaffold, onboard, or set up a new local course for an existing Canvas course.

This workflow creates local files only. It must not create a Canvas course shell, push artifacts, pull drift, remove Canvas content, or otherwise write to Canvas.

## Required Inputs

- Local course key, such as `course3` or `ai-feedback-course`
- Canvas course ID for an existing Canvas course
- Canvas base URL, or clear confirmation that `CANVAS_API_URL` from `.env` should be used
- Course title

## Optional Inputs

- Term or cohort label
- Course code
- Pasted course context
- Path to a course context file
- Whether to scaffold empty or from a spec

## Clarification Rules

- Ask only for missing required inputs.
- If the Canvas course ID is missing, ask for it.
- If the Canvas base URL is missing and `.env` is available, use `CANVAS_API_URL`; otherwise ask for the base URL.
- If context is missing, proceed with a placeholder context spec. Do not block.
- If pasted context is supplied, save it to a temporary file and pass it as `--context-spec-inline-file`.
- If a context file path is supplied, pass it as `--context-spec-source`.

## Workflow

1. Resolve the required inputs and confirm that the target course key is new unless the user explicitly asked to force setup.
2. Run the deterministic setup script:

   ```bash
   python3 canvas_sync/init_course.py \
     --course <course_key> \
     --canvas-course-id <canvas_course_id> \
     --base-url <canvas_base_url> \
     --title "<course title>" \
     --term "<term or cohort>" \
     --instance-name production
   ```

   Add `--course-code`, `--context-spec-source`, `--context-spec-inline-file`, or `--force true` only when applicable.

3. Validate the new manifest:

   ```bash
   python3 canvas_sync/schema.py --manifest <course>/manifests/production.json
   ```

4. Validate the starter PRD if it was created:

   ```bash
   python3 canvas_sync/schema.py --prd <course>/prd.json
   ```

5. Do not push to Canvas.
6. Report the JSON summary from `init_course.py`, validation results, and next commands.

## Next Step Examples

```text
Draft <course> from context/course-specs/<course>-context.md and stop before Canvas.
```

```text
Draft <course> sprint 0 from context/module-specs/<course>-sprint-0-<slug>.md and stop before Canvas.
```

```text
Push reviewed <course> sprint 0 files to Canvas.
```

## Rules

- Manifest owns the Canvas course ID.
- Never write Canvas IDs into Markdown frontmatter.
- Create artifacts only under `<course>/sprints/sprint-<n>/<slug>.md` after setup.
- Keep reports under `<course>/reports/`.
- Do not edit existing course manifests unless the user explicitly asked for a safe force operation.

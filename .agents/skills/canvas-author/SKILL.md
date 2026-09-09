---
name: canvas-author
description: Author exactly one Canvas-agnostic Markdown artifact from a PRD-shaped item.
---

# Canvas Author Skill

Write one artifact Markdown file from one PRD-shaped item.

## Authoring and Review

Follow [the authoring contract](../../../docs/AUTHORING.md). Read [writing-learning-goals](../writing-learning-goals/SKILL.md) and [writing-to-teach](../writing-to-teach/SKILL.md); also read [writing-assignments](../writing-assignments/SKILL.md) for assignments or other tasks. Use the supplied audience, capability, prior work, evidence, and relevant neighboring artifacts. Preserve the requested design, including exact wording or unconventional structures.

Review the final artifact with [reviewing-course-text](../reviewing-course-text/SKILL.md) and validate after any fixes. Return the files/sources actually read, skills consulted and revisions, authoring decisions and goal-to-evidence relationship, resolved/deferred/human-decision findings, and actual validation results to the parent. State any unavailable context. The parent owns homepage coordination, broader sequence review, and the saved review record. Do not write a report, homepage, or second artifact.

## Required Output

Write exactly one file:

```text
<target>/sprints/sprint-<n>/<slug>.md
```

## Frontmatter

Copy PRD fields exactly where applicable:

- `type`
- `title`
- `slug`
- `artifact_id`
- `sprint`
- `week`
- `module`
- `position`
- `points`
- `submission_type`
- `delivery_mode`
- `ai_activity`
- `publish`
- `rubric`
- `questions`

If the PRD item lacks `artifact_id`, set it to a stable lowercase kebab-case ID derived from the target course, sprint, and slug. Do not change it after the file exists.

Do not include `canvas_id`, `canvas_module_id`, `status`, `last_built_at`, or `error`.

For AI-powered quiz or discussion activities, keep `type: quiz` or `type: discussion`, set `delivery_mode: ai_activity`, set `submission_type: file_upload`, and put ActivityEngine-compatible prompts under `ai_activity.questions`. Do not include native Canvas `questions` on these artifacts. The sync layer publishes them as Canvas assignment shells with Common Curriculum hosted HTML and JSON submission.

## Body Rules

- Canvas-native Markdown only.
- No em dashes.
- No HTML, iframes, JavaScript, scripts, inline styles, or external CDN references.
- Write for working professionals in second person.
- Make the human contribution visible when AI is involved.
- Do not name internal CTI frameworks unless the design doc explicitly says to.

## Validation

After writing, run:

```bash
python3 canvas_sync/schema.py --artifact <file>
```

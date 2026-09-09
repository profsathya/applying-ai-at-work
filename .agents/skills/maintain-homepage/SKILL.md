---
name: maintain-homepage
description: Update a course homepage.yaml after course artifact files are added, edited, or removed.
---

# Maintain Homepage Skill

Keep `<course>/homepage.yaml` aligned with the Markdown artifacts under `<course>/sprints/`.

## Workflow

1. Identify the affected course from the changed artifact paths.
2. Read `<course>/homepage.yaml`, the affected artifact frontmatter and relevant body text, and surrounding sprint material needed to understand goals and prerequisites. For substantive copy, follow [the authoring contract](../../../docs/AUTHORING.md), [writing-learning-goals](../writing-learning-goals/SKILL.md), and the concise-copy guidance in [writing-to-teach](../writing-to-teach/SKILL.md). Keep goals grounded in the linked work; preserve supplied wording constraints. Mechanical changes do not require a general editorial pass.
3. Update only `<course>/homepage.yaml`.
4. Preserve the hybrid source model:
   - Artifact title, slug, type, sprint, position, module, hosted path, and Canvas state come from Markdown and deployment state.
   - Homepage YAML contains only curated copy: lead, footer, module tags, open or muted state, learning goals, prerequisite text, group labels, item meta, badges, and verification notes.
5. For added artifacts, place the slug in the most appropriate existing group and write concise meta text.
6. For removed artifacts, remove the stale slug from the YAML.
7. For edited artifacts, update only the curated copy that is now inaccurate.
8. For substantive copy changes, review the affected metadata in context using [reviewing-course-text](../reviewing-course-text/SKILL.md). Resolve only in-scope YAML issues. Validate before stopping:

```bash
python3 canvas_sync/schema.py --homepage <course>/homepage.yaml
python3 canvas_sync/schema.py --all
```

9. Return files/sources read, skills consulted and revisions, copy decisions and goal-to-evidence relationships, findings outside YAML scope, and actual validation results. The parent writes [the authoring record](../reviewing-course-text/references/review-record.md) for substantive work. Do not write that record yourself. If curated copy needs no change, report that finding without rewriting it.

## Rules

- Do not edit generated Common Curriculum HTML or JSON.
- Do not edit Canvas state, manifests, or artifact Markdown from this skill.
- Do not push to Canvas.
- Do not invent Canvas IDs or due dates.
- Keep prose direct, concise, and written for working professionals.
- Do not use em dashes, HTML, iframes, scripts, styles, JavaScript URLs, or external CDN references in homepage YAML.

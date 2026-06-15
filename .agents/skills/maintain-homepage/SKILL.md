---
name: maintain-homepage
description: Update a course homepage.yaml after course artifact files are added, edited, or removed.
---

# Maintain Homepage Skill

Keep `<course>/homepage.yaml` aligned with the Markdown artifacts under `<course>/sprints/`.

## Workflow

1. Identify the affected course from the changed artifact paths.
2. Read `<course>/homepage.yaml`, the affected artifact frontmatter, and the surrounding sprint artifact frontmatter.
3. Update only `<course>/homepage.yaml`.
4. Preserve the hybrid source model:
   - Artifact title, slug, type, sprint, position, module, hosted path, and Canvas state come from Markdown and deployment state.
   - Homepage YAML contains only curated copy: lead, footer, module tags, open or muted state, learning goals, prerequisite text, group labels, item meta, badges, and verification notes.
5. For added artifacts, place the slug in the most appropriate existing group and write concise meta text.
6. For removed artifacts, remove the stale slug from the YAML.
7. For edited artifacts, update only the curated copy that is now inaccurate.
8. Validate before stopping:

```bash
python3 canvas_sync/schema.py --homepage <course>/homepage.yaml
python3 canvas_sync/schema.py --all
```

## Rules

- Do not edit generated Common Curriculum HTML or JSON.
- Do not edit Canvas state, manifests, or artifact Markdown from this skill.
- Do not push to Canvas.
- Do not invent Canvas IDs or due dates.
- Keep prose direct, concise, and written for working professionals.
- Do not use em dashes, HTML, iframes, scripts, styles, JavaScript URLs, or external CDN references in homepage YAML.

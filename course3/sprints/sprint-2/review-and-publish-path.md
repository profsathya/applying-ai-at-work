---
type: page
title: "Review and Publish Path"
slug: review-and-publish-path
artifact_id: course3-sprints-sprint-2-review-and-publish-path
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 4
points: null
submission_type: none
publish: false
---

# Review and Publish Path

Publishing is a separate decision from drafting.

The repo supports a careful sequence:

```text
draft locally -> validate -> review local diff -> approve push -> push serially -> manifest updates
```

## Validate before review

For each artifact:

```text
canvas_sync/schema.py --artifact <file>
```

For the full repo:

```text
canvas_sync/schema.py --all
```

If validation fails, repair the local artifact first. Do not publish a file that fails validation.

## Review the local diff

Check:

1. The file path is under the intended sprint folder.
2. The artifact type matches the module plan.
3. Positions start at `1` and run cleanly in the module.
4. `publish` is set intentionally.
5. Quiz questions are practical and have point values.
6. Rubrics match the task.
7. There are no secrets, Canvas IDs in frontmatter, due dates without a full timestamp, HTML, scripts, or external embeds.

## Approve the push

Only after review should a human approve the push. The sync skill uses:

```text
canvas_sync/push.py --file <file> --manifest <course>/manifests/production.json
```

Pushes should be serial. Do not run concurrent push processes against the same manifest.

## Understand what push changes

`canvas_sync/push.py` can:

- Create or update the Canvas artifact.
- Add it to the Canvas module.
- Update the local manifest with Canvas IDs and module mappings.

That means a push can overwrite the targeted Canvas item if it already exists. For live courses, inspect and reconcile first when Canvas may have been edited directly.

## Stop conditions

Stop before publishing if:

- The manifest may point to the wrong course.
- The validator fails.
- The local diff includes files outside the approved scope.
- A secret appears in content, logs, or screenshots.
- Canvas has possible direct edits that have not been inspected.
- The current request did not explicitly approve a Canvas write.

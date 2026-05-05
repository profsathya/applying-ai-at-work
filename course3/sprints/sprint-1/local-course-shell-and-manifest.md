---
type: page
title: "Local Course Shell and Manifest"
slug: local-course-shell-and-manifest
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 2
points: null
submission_type: none
publish: false
---

# Local Course Shell and Manifest

A local course shell maps a repo folder to an existing Canvas course. It does not create a Canvas course.

The setup script is:

```text
canvas_sync/init_course.py
```

It creates the local structure a course needs: sprint folders, a manifest, starter metadata, a starter PRD, a progress log, reports folder, and a course context spec. In day-to-day operation, you normally ask Codex to configure the shell through the app or IDE, and Codex uses the setup workflow.

## The manifest

For this staged course, the manifest is:

```text
course3/manifests/production.json
```

The manifest stores the Canvas base URL, the Canvas course ID, the sync instance name, and the Canvas IDs created during pushes.

Do not write Canvas IDs into artifact frontmatter. Do not hand-edit the manifest during normal drafting. Let `canvas_sync/push.py` and `canvas_sync/remove.py` own manifest updates when they perform Canvas-side operations.

## What to check before drafting

Before drafting course artifacts, confirm:

1. The target course folder exists.
2. The target sprint folder exists.
3. The manifest points to the intended Canvas course.
4. The sprint folder does not already contain files you might overwrite.
5. The request clearly says whether Canvas writes are allowed.

For this local course, content should be generated under:

```text
course3/sprints/sprint-0
course3/sprints/sprint-1
course3/sprints/sprint-2
course3/sprints/sprint-3
```

## What to check before publishing

Before a push, confirm:

1. Every artifact validates.
2. The full repo validator passes.
3. The local diff is reviewed.
4. The manifest is the correct manifest.
5. The Canvas course is the intended course.
6. The current request explicitly approves the push.

If any item is uncertain, stop and inspect before writing to Canvas.

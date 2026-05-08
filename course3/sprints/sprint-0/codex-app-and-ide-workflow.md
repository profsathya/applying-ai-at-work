---
type: page
title: "Codex App and IDE Workflow"
slug: codex-app-and-ide-workflow
artifact_id: course3-sprints-sprint-0-codex-app-and-ide-workflow
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 3
points: null
submission_type: none
publish: false
---

# Codex App and IDE Workflow

Use Codex from the app or your IDE as a repo-aware collaborator. You do not need to teach it the whole system every time. You do need to give it a clear target, a clear scope, and clear permission boundaries.

## A useful request shape

A strong request usually includes:

1. **Target:** the course and sprint, such as `course3 sprint 1`.
2. **Task:** draft, inspect, reconcile, update, or push.
3. **Source context:** pasted notes or a file path under `context/course-specs/` or `context/module-specs/`.
4. **Write scope:** the paths Codex may edit.
5. **Canvas boundary:** whether Canvas writes are forbidden or explicitly approved.
6. **Validation expectation:** which local checks should run before the work is considered ready.

Example:

```text
Draft course3 sprint 2 from this pasted module plan. Write only under course3/sprints/sprint-2. Validate each generated artifact with .venv/bin/python canvas_sync/schema.py --artifact <file>. Do not push to Canvas.
```

## What Codex should do

Codex should read the relevant guidance first, inspect the current repo state, then make the smallest appropriate local edits.

For course drafting, that usually means:

1. Read `AGENTS.md`, `README.md`, `README-BUILDER.md`, the relevant skill, and the schema.
2. Check for existing files in the target sprint so it does not overwrite unrelated work.
3. Write artifact Markdown under the requested sprint folder.
4. Validate every generated file.
5. Run the full validator when the workflow calls for it.
6. Stop before Canvas writes unless you explicitly approved a push in the current request.

## What Codex should not do

Codex should not treat Canvas writes as a background detail. Pushing, pulling with apply, and removing Canvas content are real side effects.

Codex should not write Canvas IDs into artifact frontmatter. The local artifact frontmatter stays Canvas-agnostic. The manifest owns Canvas mappings.

Codex should not rewrite design docs, schemas, manifests, or context specs unless the request specifically asks for that work and the change is in scope.

## How to review Codex output

Review the output like a working operator:

1. Confirm the file paths are inside the allowed course sprint folder.
2. Confirm each artifact has the expected type and position.
3. Scan for forbidden content such as HTML, scripts, external embeds, or em dashes.
4. Check that the Markdown speaks to working professionals in second person.
5. Check that Canvas writes were not run unless you approved them.

If the output fails one of those checks, ask Codex to repair the specific issue before continuing.

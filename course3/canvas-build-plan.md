# Canvas Build Plan

This plan describes how the local course artifacts would map into Canvas course ID `181`. It is planning documentation only. It does not publish anything.

## Publication Principle

Keep this course unpublished during testing. Every generated Canvas artifact currently uses `publish: false`. Push only after local review, schema validation, and explicit human approval.

## Before You Push

1. Review all Markdown under `course3/sprints/sprint-0` through `course3/sprints/sprint-3`.
2. Confirm the course title and Canvas course ID.
3. Confirm `course3/manifests/production.json` is the intended manifest.
4. Validate the full repo:

```bash
.venv/bin/python canvas_sync/schema.py --all
```

5. Inspect Canvas if the course may already contain content:

```bash
.venv/bin/python canvas_sync/inspect_canvas.py --manifest course3/manifests/production.json --include-items --write-ledger --format markdown
```

6. Push reviewed files serially only after explicit approval.

## Recommended Canvas Module Order

1. Module 1: Orientation to the Repo, Codex, and the Agentic Workflow
2. Module 2: Setup, Configuration, and Safe First Run
3. Module 3: Building and Publishing Content with Codex and Agents
4. Module 4: Verification, Maintenance, and Extension

## Testing Recommendation

If this course is pushed to Canvas for review, keep all items unpublished until a reviewer confirms:

- Module order is correct.
- Artifact order is correct.
- Quizzes render correctly.
- Assignments show the expected rubrics.
- Links to repo paths are understandable as training references.
- No secrets or real tokens appear.

## Recovery Concept

If a push goes to the wrong course or creates incorrect items, stop immediately. Inspect Canvas, review `course3/manifests/production.json`, and use the guarded `remove-canvas` workflow only after a fresh dry run and confirmation token.

---
type: page
title: "Reviewing Drafts Before Canvas"
slug: codex-builder-tutorial-review-and-push
sprint: 5
week: 10
module: "Using This Codex Course Builder"
position: 17
points: null
submission_type: none
publish: true
---

# Reviewing Drafts Before Canvas

Codex should usually stop after it creates local Markdown and validates the files. That gives you a review point before anything changes in Canvas.

For course and module builds, review is not a formality. Validation confirms that the files match the repo schema. You still decide whether the module sequence, activity instructions, examples, quiz questions, and discussion prompts fit the coworker audience and the source tutorial.

## What Codex should report

For draft-only work, expect a response like this:

```text
Drafted 6 local Markdown artifacts.

Validation:
- artifact validation: PASS
- full schema validation: PASS

No Canvas changes were made.
```

For Canvas pushes, expect a response that includes Canvas IDs:

```text
Pushed 6 files to Canvas.

Module ID: 1234
Page IDs: 1235, 1236, 1237
Quiz ID: 1238
Discussion ID: 1239
Manifest updated.
```

For Canvas inspection, expect a response that summarizes the live course and names the ledger files:

```text
Inspected course1 on Canvas.

Ledger:
- course1/reports/canvas-ledger-production.md
- course1/reports/canvas-ledger-production.json

Summary:
- live modules: 8
- canvas items not in manifest: 0
- unpublished modules: 1
- drifted artifacts: 2
```

## What to review

Before approving a push, check:

- The files are in the intended course and sprint folder.
- The module title is correct.
- Each artifact type, position, point value, and submission type is correct.
- The content follows the source tutorial or spec you provided.
- Course-level requests produced a coherent sprint sequence.
- Module-level requests produced a coherent artifact sequence inside the target sprint.
- The language is clear for the coworker audience.
- The content does not include due dates, file uploads, or external material unless you asked for them.
- The draft did not edit manifests, design docs, or Canvas IDs during a draft-only request.
- The response says no Canvas changes were made during drafting.

If you are new to the repo, focus on the visible learning experience first: titles, order, instructions, quiz questions, discussion prompt, and whether a participant would know what to do next. A maintainer can help with lower-level implementation details.

## When to inspect Canvas

Use `canvas-inspector` when you need to know what is already live in Canvas before deciding what to edit or reconcile. It is read-only against Canvas, but it writes an up-to-date local ledger under `course<N>/reports/`.

Ask for it directly:

```text
Use canvas-inspector for course1, include module items and drift, and update the ledger.
```

The ledger helps you answer practical review questions:

- Which modules and items are currently on Canvas?
- Which Canvas items are missing from the manifest?
- Which local files are not represented in Canvas?
- Which modules or items are unpublished?
- Which known artifacts may need reconcile before local editing continues?

Inspection does not apply Canvas changes back to local Markdown. If the ledger shows drift that should be pulled down, ask for a reconcile dry run first. Reconcile apply should happen only after a human reviews the dry-run report.

## When to approve a push

Approve a push only when the local Markdown is ready to become live Canvas content.

Use explicit language:

```text
Push these reviewed files to Canvas: <file paths>
```

That instruction tells Codex to use the deterministic Canvas sync script. The script validates the files, creates or updates Canvas items, adds them to the Canvas module, and updates the manifest with Canvas IDs.

If you are unsure, ask Codex to revise locally first.

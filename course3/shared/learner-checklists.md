# Learner Checklists

## Before Asking Codex To Edit

- I opened the repo root in Codex app or IDE.
- I named the target course, sprint, module, or file.
- I named the source context or asked Codex to inspect first.
- I said what should not change.
- I said whether Canvas publishing is allowed.
- I included done criteria such as validation, file list, or review summary.

## Safe Draft Checklist

- Prompt includes `Generate local Markdown only`.
- Prompt includes `Validate the files`.
- Prompt includes `Stop before Canvas`.
- Codex reports changed file paths.
- Codex reports validation result or a reason validation was not run.
- No manifest or Canvas ID was edited during draft-only work.

## Before Canvas Inspection

- I am authorized to use Canvas credentials.
- I understand inspection is read-only against Canvas but writes local ledger files.
- I know which manifest applies.
- I asked for `include module items` when item-level review matters.
- I asked for `drift` only when reconcile readiness matters.

## Before Canvas Push

- The exact files are reviewed.
- Schema validation passed.
- The changed Markdown has the right titles, module names, positions, points, and submission types.
- Live Canvas drift has been inspected if the course is already live.
- The prompt explicitly names the reviewed files to push.
- I understand the push can create or overwrite Canvas content and update the manifest.

## After Codex Finishes

- I reviewed the changed files.
- I reviewed the diff or review pane.
- I checked validation and tests.
- I documented any unresolved questions.
- I asked Codex to correct misunderstandings in a narrow follow-up.

---
name: inspect-canvas
description: Inspect a live Canvas course in one read-only pass, list modules and module items, compare them with the local production manifest and local Markdown files, optionally report reconcile drift, and write an up-to-date local Canvas ledger under <course>/reports/.
---

# Inspect Canvas Skill

Use this when a human asks what is currently on Canvas, wants a module or item inventory, wants to know whether Canvas and the local manifest line up, or wants a pre-reconcile report.

This workflow reads Canvas and may write local ledger files. It must not write to Canvas.

## Workflow

1. Resolve the target course and manifest:
   - `<course>` -> `<course>/manifests/production.json`
2. Run the inspector with module items and ledger output:

   ```bash
   python3 canvas_sync/inspect_canvas.py --manifest <manifest_path> --include-items --write-ledger --format markdown
   ```

3. If the user asks about reconciliation readiness or drift, add `--drift`:

   ```bash
   python3 canvas_sync/inspect_canvas.py --manifest <manifest_path> --include-items --drift --write-ledger --format markdown
   ```

4. Report the summary, notable warnings, and ledger paths.
5. If drift should be applied, switch to the `reconcile` skill. Do not apply drift from this skill.

## Output

The script writes:

```text
<course>/reports/canvas-ledger-production.json
<course>/reports/canvas-ledger-production.md
```

The ledger includes live Canvas modules, module items, publish state, manifest mappings, local-file gaps, Canvas-only items, unpublished modules/items, and optional drift findings.

## Rules

- Read-only against Canvas.
- Do not run `canvas_sync/push.py`.
- Do not run `canvas_sync/pull.py --apply`.
- Do not edit manifests manually.
- Keep generated ledgers out of `course*/manifests/`; that folder is reserved for schema-validated manifest JSON.

---
name: remove-canvas
description: Inspect live Canvas modules/items, generate a dry-run removal plan for manifest-backed targets or an explicit full-course clear, and apply destructive Canvas removals only after an explicit confirmation token.
---

# Remove Canvas Skill

Use this when a human wants to remove modules, module items, pages, assignments, quizzes, or discussions from Canvas.

This workflow writes to Canvas only after a fresh inspection, a dry-run plan, and explicit token confirmation.

## Workflow

1. Resolve the target course and manifest:
   - `<course>` -> `<course>/manifests/production.json`
2. Invoke the existing Canvas inspection path first:

   ```bash
   python3 canvas_sync/inspect_canvas.py --manifest <manifest_path> --include-items --write-ledger --format markdown
   ```

3. Show the live module/item inventory and ledger paths. Ask which manifest-backed targets to remove, unless the human explicitly requested a full course clear.
4. Generate a dry-run removal plan for targeted removals:

   ```bash
   python3 canvas_sync/remove.py --manifest <manifest_path> --target <target> --dry-run
   ```

   Accepted targets:

   ```text
   module_id:<canvas_module_id>
   module_position:<position>
   module_item_id:<module_item_id>
   file:<repo-relative-md-path>
   ```

   Repeat `--target` for multiple removals in one plan.

   For a full course reset that must include Canvas-only modules and items, use:

   ```bash
   python3 canvas_sync/remove.py --manifest <manifest_path> --course-clear --dry-run
   ```

5. Show the operations, manifest entries to remove, blocked targets, local files kept, and confirmation token.
6. Apply only if the human explicitly confirms the token from the current dry run:

   ```bash
   python3 canvas_sync/remove.py --manifest <manifest_path> --target <target> --apply --confirm-token <token>
   ```

   For a confirmed full course reset, use:

   ```bash
   python3 canvas_sync/remove.py --manifest <manifest_path> --course-clear --apply --confirm-token <token>
   ```

7. Run schema validation after a successful apply:

   ```bash
   python3 canvas_sync/schema.py --manifest <manifest_path>
   ```

## Rules

- Never skip the inspection step.
- Never apply without a fresh dry-run confirmation token.
- Targeted removals only remove manifest-backed targets.
- Full course clear is destructive and includes Canvas-only module items and modules. Use it only when the human explicitly asks to clear the course contents.
- Keep local Markdown files. The remover only updates the manifest after successful Canvas deletes.
- Do not edit manifests manually; `canvas_sync/remove.py` owns manifest updates during removal.
- Do not run this against a production Canvas course as a test. Use dry-run or a known sandbox course for pilot validation.

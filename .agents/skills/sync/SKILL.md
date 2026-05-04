---
name: sync
description: Push one or more existing course artifact Markdown files to Canvas through the deterministic schema and push scripts. Use after a human asks to sync or push edited MD files.
---

# Sync Skill

Push specified artifact Markdown files to Canvas using the active production manifest.

## Workflow

1. Resolve each requested file path. It must live under `<course>/sprints/sprint-<n>/`.
2. Determine the manifest from the file prefix:
   - `<course>/...` -> `<course>/manifests/production.json`
3. Run validation first:

   ```bash
   python3 canvas_sync/schema.py --artifact <md_file_path>
   ```

4. If validation fails, stop and report the errors. Do not push.
5. Before any Canvas write, confirm the user really wants to push the listed files unless the user already gave explicit push/sync instruction in the current turn.
6. Push files serially with:

   ```bash
   python3 canvas_sync/push.py --file <md_file_path> --manifest <course>/manifests/production.json
   ```

7. Report `action`, `canvas_id`, and `canvas_module_id` from the JSON output.

## Rules

- Never push a file that fails schema validation.
- Never edit the manifest directly; `push.py` owns manifest updates.
- Do not run multiple `push.py` processes against the same manifest in parallel.
- Never retry a failed Canvas API push in the same workflow without human confirmation.
- Do not run this against a production Canvas course as a test. Use a known sandbox course for pilot validation.

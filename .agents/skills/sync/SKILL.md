---
name: sync
description: Push one or more existing course artifact Markdown files to Canvas through the deterministic schema and push scripts. Use after a human asks to sync or push edited MD files.
---

# Sync Skill

Push specified artifact Markdown files to Canvas using the active production manifest. For production courses, prefer the GitOps path: merge reviewed Markdown to `main` and let the protected `Publish Canvas` workflow update Canvas and the `canvas-state` branch. Use direct local pushes only for admin repair, sandbox pilots, or a human-approved emergency.

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
6. Check the manifest. If `hosted_html.enabled` is true, the local push must render hosted output into a sibling Common Curriculum checkout before Canvas points at it:

   ```bash
   python3 canvas_sync/push.py --file <md_file_path> --manifest <course>/manifests/production.json --hosted-output-dir ../common-curriculum
   ```

   Use the plain push command only when hosted HTML is disabled:

   ```bash
   python3 canvas_sync/push.py --file <md_file_path> --manifest <course>/manifests/production.json
   ```

   If publishing through a local checkout of the deployment-state branch, pass:

   ```bash
   --state-dir <path-to-canvas-state-checkout>
   ```

7. Report `action`, `artifact_id`, `canvas_id`, `canvas_module_id`, and `state_path` from the JSON output.

## Rules

- Never push a file that fails schema validation.
- Markdown is the source of truth. Common Curriculum HTML and activity JSON are generated output from `canvas_sync/hosted_html.py`.
- For hosted courses, do not run a direct local push without `--hosted-output-dir ../common-curriculum`.
- Never edit deployment state directly; `push.py` owns manifest or `canvas-state` updates.
- Do not run multiple `push.py` processes against the same manifest in parallel.
- Do not use local direct push as the normal production publishing path.
- Never retry a failed Canvas API push in the same workflow without human confirmation.
- Do not run this against a production Canvas course as a test. Use a known sandbox course for pilot validation.

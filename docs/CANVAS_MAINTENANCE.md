# Canvas maintenance and recovery

For a GitOps course, the production manifest supplies static configuration and the `canvas-state` branch supplies mutable Canvas IDs and fingerprints. Use a current checkout of that branch for inspection, reconciliation, updates, and removal. Passing `--state-dir` selects it exclusively; missing or mismatched external state is an error, not permission to use old manifest IDs. Commands without the flag retain legacy local-deployment behavior.

Run from the repository root with the repository virtualenv. The examples below are operator commands, not authorization to execute Canvas writes.

## Inspect and prepare

```bash
.venv/bin/python canvas_sync/inspect_canvas.py \
  --manifest course1/manifests/production.json \
  --state-dir ../canvas-state --include-items --drift --write-ledger

.venv/bin/python canvas_sync/update_artifact.py list \
  --course-id 180 --state-dir ../canvas-state
```

Use `prepare` and `verify` with the same `--state-dir`. Hosted AI activities keep their source semantic type (`quiz` or `discussion`) even though Canvas exposes an assignment shell. Preparation preserves the existing hosted Markdown. A hosted item without a mapping needs its real source mapped first. Native Canvas-only content can be imported when its types are supported; unsupported quiz question types are reported rather than coerced to short answers.

## Reconcile a reviewed set

```bash
.venv/bin/python canvas_sync/pull.py \
  --manifest course1/manifests/production.json \
  --state-dir ../canvas-state --dry-run
```

The report distinguishes Canvas differences, pending local work, conflicts, missing files, and orphaned Canvas objects. Native Markdown is normalized through the actual renderer to avoid formatting-only false alarms. Hosted shells are compared with the expected iframe and fallback URL; they never become the instructional body.

For a subset, repeat the dry run with `--file <repo-relative-path>` for each selected artifact. Review that result and its token. After explicit approval, run the same scope with `--apply --confirm-token <token>`. The token binds the selected state, source bytes, and Canvas snapshots. Any change requires another dry run.

Apply validates candidate Markdown before replacement, preserves backups under `<course>/reports/reconcile-backup-<token>/`, and updates the selected deployment state's hashes and fingerprints. A file with both local and Canvas changes needs a deliberate merge. Changed native quiz questions need explicit supported-question import. Hosted-wrapper changes need shell review while keeping the source body intact. The command does not write to Canvas.

Validate the changed source and external state, review the diff, and preserve both sides of the reconciliation:

```bash
.venv/bin/python canvas_sync/schema.py --all
.venv/bin/python canvas_sync/schema.py --state ../canvas-state/course1/production.json
```

If sprint content changed in a course with `homepage.yaml`, update that metadata through `homepage-maintainer` before final validation. Reconciled source belongs on the content branch; external deployment state belongs on `canvas-state`. Do not copy external IDs into Markdown or commit the state file onto `main`. Coordinate their reviewed integration so the next publish uses the reconciled baseline.

## Publish and recovery

- An absent fingerprint is recoverable automatically only when live Canvas already matches the source representation. A different live object is blocked for reconciliation; other healthy artifacts still publish.
- Successful object creation records its ID before module placement or quiz-question creation. If a later step fails, inspect the partial result and preserved state before an approved retry. Partially populated quizzes may require explicit recovery because their question list does not yet match source.
- A timeout or server error on a creation request has an uncertain outcome. The client does not replay that POST automatically. Inspect Canvas and map a created object if one exists before retrying. This cannot make a remote write and local filesystem save atomic.
- Batch hosted publishing renders affected artifacts and then renders the course once. Standalone pushes retain their complete rendering behavior. Failed or drifted artifacts retain the existing restoration protections.
- Course-specific changes select that course's production manifest, including named keys such as `career-tools`. Shared-code-only changes validate but do not imply permission to publish all pending course content. Dispatch the protected workflow for the reviewed course when shared renderer or sync changes should be deployed; select `hosted_only` when appropriate.
- Rubrics remain manually applied and acknowledged with `ack_rubric.py`. The builder does not silently publish rubric edits.

## Removal

Use the inspection and token-confirmed removal workflow with the same `--state-dir` throughout. Validate the external state after removal. The operation preserves Markdown, so a later course publish can recreate a removed artifact if it is still in the active source tree. Resolve that lifecycle choice before republishing. A removal failure can leave some remote deletes completed; inspect and generate a fresh plan rather than reusing the old token.

## Verification limits

Repository tests use deterministic API fakes and rendered files. A sandbox smoke test is still needed for institution-specific Canvas behavior, Classic versus New Quizzes, real permissions, hosted deployment, browser/LTI progress, and human review of the participant experience. Never merge to `main` solely to test a publish.

# Course 180: retire the Context reading without deleting its page

PR232 (`684cc09945a3d2d7b6215239c5fea120f7a8bf14`) sets
`course1/sprints/sprint-16/working-with-ai-context.md` to `publish: false`
and removes its step from the Introduction. The page was already unpublished in
Canvas, but deployment state still fingerprinted it as published. Publish run
37023887386 updated the Introduction and deployed hosted output, then correctly
blocked the reading's stale baseline.

The ordinary `remove.py` workflow deletes both a module placement and its
underlying content. That is broader than this repair, which retains page3627.
`pull.py` reports no source drift when the current hosted source already agrees
with Canvas, so it cannot acknowledge this stale fingerprint by itself.

`maintenance/retire_course180_context_reading.py` is a narrowly bounded admin
repair using the existing Canvas client, instance guards, state schema, file
lock, atomic state writer, and reviewed iframe sanitizer check. It accepts only
CTI course180, page3627, module2084 and item18013. It proves that source differs
from the recorded source only by `publish: true` becoming `publish: false`, and
that the live fingerprint matches the old fingerprint with only publication
flipped. Missing or unexplained baselines, content changes, changed identities,
duplicate/moved placements, and unexpected requirements fail closed.

The transport permits module/page metadata GETs and one exact placement DELETE.
It cannot publish, edit/delete a page, or read submissions/users. A dry-run token
binds source, external state, page snapshot and module/item configuration. Apply
re-reads the evidence, removes the placement, then verifies the page is unchanged
and all remaining placements, order, publication flags and requirements across
all modules are unchanged. It retains before/after evidence and the state backup.
An interrupted operation can reconcile a verified absent placement on a new run.

```sh
python maintenance/retire_course180_context_reading.py \
  --state-dir ../canvas-state \
  --source-commit 684cc09945a3d2d7b6215239c5fea120f7a8bf14 \
  --env-file /path/to/existing/course/.env \
  --evidence-dir /path/to/new/dry-run-evidence
```

After review and authorization, repeat with a new evidence directory,
`--apply --confirm-token <fresh-token>`. No credentials are copied into evidence.
Validate the resulting state and retain it on `canvas-state` with a normal
fast-forward push. Never overwrite a newer state snapshot or force-push.

The source remains unpublished. The reconciled state retains the page identity,
hosted content hash and last-published timestamp, clears its placement and
completion requirement, invalidates its old payload hash, and records the exact
retirement source hash/commit with the verified live fingerprint. The unchanged
retired source then has no pending publisher change.

`prepare_progress()` provides an idempotent, two-field-only correction to the
matching generated Common Curriculum progress row. Apply it to fresh hosted
metadata after live removal verification. Preserve every other row and file;
do not regenerate the course to reconcile this retirement.

This maintenance-code draft does not authorize merging, dispatching a broader
publisher, changing Sprint4 decisions, or exporting/importing a De Anza course.

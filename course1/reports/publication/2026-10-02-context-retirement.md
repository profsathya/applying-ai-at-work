# Context reading retirement repair, 2026-10-02

Authorized scope: finish deployed PR232's retirement of Working with AI: Context
in CTI Canvas course180. Inspection used source main
`9e37486e86c48a6c1158b295b607918c56f2854f` and state
`88499160acdf9e9f57265151fc4e40a13738b6d8`, preserving PR233.
The existing course checkout was left untouched; work used an isolated clone.

## Live before and after

At 15:45:52 UTC, the scoped maintenance workflow removed only module2084
item18013. Page3627 (`working-with-ai-context`) was retained byte-for-byte,
`published: false`, `hide_from_students: true`. No page update occurred.

| Field | Before | After |
|---|---|---|
| Page3627 publication | unpublished | unpublished |
| Placement18013 | module2084, position13 | absent |
| Placement completion | must_view | absent |
| Module2084 items | 11 | 10 |
| Module2084 publication | published | published |
| All other module-item configurations | baseline | unchanged |

Readback compared all six modules and every placement. All49 remaining items
retain identity, relative order, position, publication state and completion
requirements. Other modules are unchanged; module2084 only loses one item from
its count. No submission, grade, user, or Test Student endpoint was accessed.

The stored fingerprint was
`611b957382e9b3d9de20aae6701399adeecad0226a8c6644d97dbd52f3d1499d`.
The verified live fingerprint is
`44c1076e5f46c4ddfd2026a42499202adb3a6049f1fe58e8cc81f96a7ca52520`.
Changing only the live snapshot's publication flag back to true reproduces the
stored fingerprint exactly. The source likewise differs from its recorded
deployment revision only by the retirement flag.

## Deployment state

State commit `ce3769e2874b281ebb7dd3f0cef66a74e6d9ba74`, verified on remote
`canvas-state`, reconciles only this artifact plus `last_sync`: placement
ID becomes null, completion and stale payload hash are removed, live fingerprint
is recorded, and source commit becomes PR232's
`684cc09945a3d2d7b6215239c5fea120f7a8bf14`. Source content hash changes from
`dd0be81477320bb88d2a4a9cf379a09468900340702845c450822db442ecd128` to
`efc862fbfcf429e9b97a13bd81e824d01d25960da001e4dde6d7e6e718267aa2`.
Canvas page/module identity and hosted content hash remain unchanged.
The exact-file publisher scan selects zero changes for this reading.

## Publication and course context

No broad publisher or new content deployment was invoked for Canvas cleanup.
PR233 Publish Canvas run37027913329 succeeded, and Course context sync
run37028187013 succeeded. After cleanup, a fresh read-only course-context export
contains39 verified published pages and excludes the retired reading.
Its release digest is exactly the successful publication/refresh digest:
`b898d667f40a10b973bef21498e415561ead706204b8230e6cdae9f1c051d408`.
The hidden placement cleanup requires no additional document refresh.

The Common Curriculum progress map at `725ff1f7` still retained the obsolete
item/completion fields. A separate exact metadata correction clears only those
two fields; its integration/deployment outcome must be recorded separately.

## Validation and evidence

- Full offline unit suite before cleanup:367 tests passed, one skipped.
- Final offline unit suite after progress-map tests:369 tests passed, one skipped.
- Retirement regression tests:8 passed, covering rejection of source/shell/state,
  identity and placement drift; exact fingerprint proof; transport restrictions;
  readback preservation; retry/idempotency; and the two-field progress transform.
- Repository schema and external state schema:PASS.
- Link audit:172 artifacts,59 links, zero errors.
- Before/after metadata, dry-run token, plan, state backup, release inventories,
  document-sync payload and logs are retained in the isolated task workspace.
- Verification used API/CLI only. Browser/native UI was left available to the
  tutorial recording task. No De Anza export/import or Sprint4 policy change.

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
Canvas's direct item18013 GET still returns HTTP200 with an unpublished retained
record, but its completion requirement is absent. It is absent from the active
module-item listing; this repair does not claim the direct URL returns404.

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
item/completion fields. Jeremy separately approved merging/deploying the exact
two-field correction at15:50:42UTC. Common Curriculum PR494 merged at15:54:37UTC,
commit `96256a9bf2b1616056e9e28ed1f13d343f864f1f`. GitHub Pages deployment
run37030274198 succeeded. Canonical and fresh public URLs both returned the exact
approved62102-byte file, SHA256
`c55166ef5ac338fbc32386573bbb4f045a33e9cef4b64951cadc7bf4a8e41a77`.
Only the retired row's `canvasModuleItemId` and `completionRequirement` become
null. All119 other rows and every other hosted file are unchanged.

The maintenance code remains separate in applying-ai-at-work draft PR238,
unmerged. Its GitHub Validate schemas check succeeded at15:55:19UTC. No additional
code merge, broad course publish or document refresh was authorized or performed.

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

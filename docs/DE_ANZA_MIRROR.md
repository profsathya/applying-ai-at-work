# De Anza course 46601 mirror

Course 180 remains the source for the selected Course 1 teaching content. Its
normal protected publish workflow generates the live HTML under
`Common-Curriculum/deanza/course1/`. De Anza's credential-free adapter fetches
those same pages on every visit with `cache: no-store`, then resolves source
Canvas links through the explicit public deployment mapping in
the deployed public `deanza/mirrors/deanza46601/config.json`.

The adapter lives outside the source workflow's generated course directory, at
`Common-Curriculum/deanza/mirrors/deanza46601/`. Future collaborators continue
editing Course 1 Markdown and publishing course 180 normally. Existing hosted
instructions, questions, examples, downloads, and page layouts reach De Anza
through the same live HTML. Old isolated HTML URLs redirect to the adapter and
contain no second copy of the teaching text.

The adapter has no credential and makes no Canvas API calls. It uses the source
renderer’s native Canvas navigation/completion mode. A source page that adds an
unmapped Canvas ID, an unlisted HTML page, or an LTI progress client stops or
disables the affected link until the mirror is reviewed. It never sends someone
to a guessed destination or reuses CTI progress authentication.

## Native changes remain local

Canvas titles, assignment points/submission types, module items/order,
publication flags, prerequisites, completion requirements, and release dates
are separate objects in each institution's Canvas. Hosted text cannot update
them. `canvas_sync/mirror_native.py` provides a bounded local snapshot, plan,
apply, and verification workflow for existing mapped objects. New objects,
item moves, deleted objects, or changed mappings require a separate reviewed
mapping update; the tool does not create, delete, reimport, or enroll anyone.

The destination shell stays unpublished. Institution-specific course name,
timezone, term/dates, homepage setting, enrollments, submissions, and grades are
preserved. Existing destination DesignPLUS stylesheet/script wrappers are also
preserved around the mirrored iframe. The selected modules retain their logical order even if source
position numbers have gaps from retired content.

All credentials remain in local ignored `.env` files. There is no De Anza CI
credential, token upload, scheduled native synchronization, or account-role
change. The existing disabled De Anza GitOps scaffold is not enabled by this
adapter.

## Build and sync

Build the public adapter into a Common Curriculum checkout:

```bash
python canvas_sync/course_mirror.py \
  --config ../common-curriculum/deanza/mirrors/deanza46601/config.json \
  --output ../common-curriculum/deanza/mirrors/deanza46601 \
  --legacy-dir ../common-curriculum/deanza/cis501-46601/course1
```

Validate Course 1 artifacts with `python canvas_sync/schema.py --all`, and verify
the deployed adapter before changing Canvas iframe URLs. Native sync requires
explicit local paths to each institution's credential and the original import
mapping receipt (which also maps page IDs and assignment groups):

```bash
python canvas_sync/mirror_native.py \
  --config ../common-curriculum/deanza/mirrors/deanza46601/config.json \
  --mapping /path/to/destination-mapping.json \
  --source-env /local/cti-checkout/.env \
  --destination-env /local/deanza-checkout/.env \
  --receipts /local/deanza-mirror-receipts \
  --phase snapshot
```

Run the same command with `--phase plan`, inspect `plan.json`, then use
`--phase apply` only when the human has authorized the live sync. The snapshot
cannot overwrite an existing backup. Each PUT checks the destination against
that backup and has no automatic retry. `--phase verify` takes fresh source and
destination reads and requires zero remaining operations and unchanged course
settings. Receipts contain teaching definitions only; no credentials or person,
submission, or grade records are saved.

The Python tests include mapping and configuration guardrails. The browser check
in `tests/check_course_mirror_browser.cjs` uses an isolated context with public
content fixtures, verifies all 56 mapped pages and native/web navigation, and
changes a mock upstream page after the adapter was built to confirm the next
visit receives the change.

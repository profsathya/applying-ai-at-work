# Course 180: bounded release and reconciliation repair

This is a reviewed source and tooling proposal. It does not authorize a merge,
Canvas write, state-branch update, hosted deployment or Google Doc refresh.
PR #202's ten-link cleanup is separate.

## Diagnosis and source decisions

- Brainstorm original 7149 is published and has a prior submission-guard receipt.
  Preserve the assignment, its publication, settings, submissions and grades.
  Restore its source `publish: true` to match live Canvas, preventing the normal
  publisher's staged-item restoration from trying to unpublish it.
- Replacement 7185 remains unpublished. Its current wrapper has only the known
  Canvas serializer form of the approved iframe shell. Accept that exact wrapper
  into a reviewed baseline instead of overwriting it. Source and hosted learning
  content must remain identical to the recorded release except the publish flag.
- The problem frame 3624 is already unpublished in source and Canvas; reconcile
  only its stale fingerprint and publication-source provenance.
- Sprint 3 Concept Check 7180 was staged unpublished on September 25. The current
  live module has this assignment published as its Concept Check. Reconcile the
  source flag to true, retaining all content, grading and the live placement.
- Get underneath 7152 is aligned. Leave its source, state and Canvas object alone.
- `verify_walkthrough_adjacency` still called `int(None)` for intentionally retired
  original placements, after the publisher already supported those placements.
  It now uses the same identity, uniqueness, intended-module and original-absence
  checks as `walkthrough_position` without recreating or moving anything.

## Read-only proposal

Fetch the latest `canvas-state:course1/production.json` into a temporary directory
and refresh the Common-Curriculum checkout. Do not use the legacy manifest's IDs.
Commit the reviewed source edits before creating a provenance-bearing proposal.

```sh
python maintenance/prepare_course180_repair.py \
  --state /tmp/current-canvas-state/course1/production.json \
  --hosted-root /path/to/Common-Curriculum \
  --output-dir /tmp/new-course180-proposal
python canvas_sync/schema.py --state /tmp/new-course180-proposal/production.proposed.json
```

The command can issue only GETs for the four instructional objects and module
metadata. It cannot write Canvas or read submission/user endpoints. It does not
fetch overrides containing participant identities; any flagged override requires
separate instructor review. It leaves the input state untouched and writes a new
proposal plus a review token. The token identifies the exact evidence, not a
production authorization or an apply command.

The proposal checks all four exact identities, unique current placements,
published parent modules, matching object/item visibility, preserved grading,
Brainstorm assessment parity, unchanged hosted hashes and instructional source.
It accepts only the known iframe sanitizer normalization, never arbitrary wrapper
text, scripts, targets or behavior. Problem frame and Concept Check drift must
be provably publication-only against stored fingerprints.

Before 7185 is published, only its fingerprint is reconciled; its staged content
hash and released source commit remain unchanged. Re-run after an approved
publication to adopt `publish: true` source only once a fresh object/module read
confirms it. No hypothetical future Canvas state is marked released.

## Exact production boundary for separate approval

1. Review the draft diff and current preflight token; refresh all evidence again.
   Land this code and source through a controlled merge arrangement that prevents
   the normal broad publisher and subsequent course-context document refresh.
   Changes to `canvas_sync/**`, `tests/**` and sprint files normally trigger that
   workflow on main. Do not merge normally or dispatch the full-course publisher.
   Any temporary workflow suspension and restoration also needs explicit approval.
2. Apply only the reviewed field changes to the latest remote state, with a
   compare-and-swap check on its commit. Do not replace a collaborator's newer
   state with an older complete proposal. Expected initial changes concern
   7185's fingerprint, and 3624/7180 publication fingerprints, content hashes and
   source commits. Original 7149 and Get underneath 7152 stay unchanged in state.
3. Publish **assignment 7185 only** using a publication-only payload:
   `{"assignment":{"published":true,"notify_of_update":false}}`.
   Preserve its exact wrapper, grading, submission type, dates, rubric and group.
   Do not invoke the normal two-item replacement flow: it requires unpublishing
   the original and rightly refuses a submission-bearing source.
4. Read back assignment 7185 and module item 18020, plus original 7149/item17977.
   Confirm both remain published, original content/settings unchanged, and all
   module ordering preserved. Rerun the proposal to record verified release
   provenance. If Canvas does not confirm publication, stop and inspect; do not
   automatically unpublish either assignment as rollback, since participants may
   have submitted during the interval.
5. Verify the released-source export in memory, reporting only success/count or
   blockers. Do not upload an export or refresh the Google Doc. This proposal
   requires no Common-Curriculum HTML regeneration or deployment.

### Optional later module-only removal

Publishing the replacement while retaining the original is an explicit exception
to the normal unpublish-and-replace policy. The submission guard remains intact.
After publication verification, and **only if separately authorized**, remove
module item **17977** from module **2079**. Never delete or unpublish assignment
7149. Preserve its gradebook/submissions and instructor access. Verify the full
module order differs only by that one removed item and replacement18020 remains.
Then review a scoped state/progress-map placement update: clear original7149's
module-item ID and completion requirement, retaining assignment identity and all
other fields. This optional removal is not performed or proposed as an already
applied state by the read-only tool.

## Separate homepage limitation

The curated homepage still links Brainstorm's original and the older Sprint 3 v3
Concept Check; v3's source still says published although the current live module
uses v4. Do not regenerate the homepage or republish all course artifacts as part
of this repair. A later explicitly scoped homepage/release cleanup must resolve
those older references; it is not a reason to overwrite current Canvas placement.

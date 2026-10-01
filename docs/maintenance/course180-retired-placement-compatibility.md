# Course 180: released walkthroughs after original placement removal

The eight originals below remain assignments in CTI course 180. Only their
module placements were removed with user approval. Preserve their identities,
content, publish state, grading configuration, and submissions.

| Original | Removed item | Walkthrough | Retained item | Module |
|---:|---:|---:|---:|---:|
|7151|17979|7184|18019|2079|
|7152|17980|7183|18018|2079|
|7169|18001|7178|18011|2084|
|7158|17990|7166|17998|2081|
|7159|17991|7165|17997|2081|
|7176|18009|7179|18012|2084|
|7160|17992|7168|18000|2082|
|7134|17954|7167|17999|2082|

## Compatibility behavior

Existing live anchors retain their current adjacency behavior. If an anchor is
absent, publishing requires the original assignment still to exist and the
walkthrough to have exactly one live assignment placement, matching its stored
item ID in the intended module. Its actual position and full module order are
preserved. Missing, duplicate, moved or identity-mismatched placements fail before
assignment writes. Any remaining placement of the original also stops this
fallback for reconciliation. No original placement is recreated.

## Review-only metadata proposal

`maintenance/reconcile_course180_placements.py` performs local JSON transforms,
with no network or Canvas writes. It validates CTI/course identity and exact
original/replacement mappings. It clears `canvas_module_item_id` and removes the
originals' `completion_requirement` from state. Corresponding progress-map fields
become null. All other fields and records remain unchanged. Re-running the
transform on its result is idempotent; output files are exclusively created.

Use freshly fetched `canvas-state:course1/production.json` and hosted
`deanza/course1/progress-map.json`, not a full stored snapshot applied over newer
state. Before applying, recheck live original absence and unique walkthrough
placement. Reject drift. Review precisely 16 changed fields in each JSON file.
No homepage, index, assignment HTML or course-content regeneration is needed.

Example local preparation:

```sh
python maintenance/reconcile_course180_placements.py \
  --state /path/to/current/production.json \
  --progress /path/to/current/progress-map.json \
  --output-dir /path/to/new/proposal
python canvas_sync/schema.py --state /path/to/new/proposal/production.json
```

Apply only after review, through an explicitly approved state update and a
progress-map-only hosted change. Retain assignment IDs, module IDs as intended
module context, source provenance and hashes. Brainstorm original 7149/item17977
and historical First frames walkthrough 7182/item18016 are excluded.

## Release constraint

**Do not simply merge this draft.** Changes to `canvas_sync/**` or `tests/**` on
main trigger `publish-canvas.yml`; its success can trigger the course-context
Google Doc refresh. Approval must cover a controlled release arrangement that
prevents a broad publisher/document refresh while landing compatibility code and
the two metadata changes. This proposal does not disable workflows, merge, deploy,
update remote state, alter the Google Doc, or dispatch any publishing workflow.

Tests cover all eight pairs with stale and cleared anchors, existing sparse
anchors, retry persistence, missing/duplicate/moved/identity-mismatched placements,
originals placed elsewhere, original identity validation, exact metadata changes,
idempotency and unchanged module order on a subsequent push. Local suite: 55 tests
across retired placement, push identity/structural/fast-path, state and hosted HTML.

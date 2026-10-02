# Course 180 pre-migration batch

Prepared from main `4d6857c7442f4aac3274e3c38664ffba1067faf0`, with deployment state `9372e02612f2165ca547fff590e6b2f099c4cb3e`. This preparation made no live Canvas changes and copied no credentials. Execution belongs to the original CTI task and its existing runtime. De Anza migration/import is outside this batch.

## Prepared behavior

- Sprint 1–5 concept checks become Canvas pages with the existing hosted questions and feedback. They have no submission or grade; published pages require viewing. Previous hosted assignment paths render the same practice document so bookmarks remain usable.
- Generated response-copy controls are removed throughout this course. Answer downloads and Word/document exports remain; copying the approved Dojo transcript request remains available.
- Sprint 1–4 reflections stay text-entry submission assignments, with zero points and complete/incomplete grading. Graded deliverables keep their points.
- Sprint 0 is a prerequisite to every later sprint. Each later sprint also requires its immediate predecessor. Required items run sequentially in their existing live order.
- Sprint 2 unlocks 2026-10-18 23:59 Pacific (`2026-10-19T06:59:00Z`). Sprint 3, 4 and 5 unlock on November 1, 15 and 29 at 23:59 Pacific (`2026-11-02T07:59:00Z`, `2026-11-16T07:59:00Z`, `2026-11-30T07:59:00Z`).
- Unpublished Sprint 5 work remains unpublished and outside completion requirements. Its configured requirements return when source publication is enabled.
- The obsolete Sprint 3 overview source is reconciled to `publish: false`. The obsolete Sprint 1 reading was already unpublished. Both are absent from the curated homepage.

## Application order in the established CTI runtime

1. Use a fresh source checkout of this prepared commit. Keep the original worker's dirty checkout intact. Use a current `canvas-state` checkout and the Common Curriculum checkout as explicit paths. Never copy a token into the prepared checkout.
2. Inspect course 180 again and back up the current state and live inventory. Confirm the exact IDs, publication flags and no submitted concept-check work. A changed/missing/ambiguous placement stops conversion.
3. Render all course hosted files from this source and deploy the generated output before Canvas points at new practice URLs. `render_hosted_files` supports offline preparation; final indexes must later use `render_published_hosted_files` with the updated state. Preserve the current hosted provider/workflow.
4. Convert the five concept checks, sequentially, with the command below. The explicit flag retains each original assignment as unpublished, ungraded and excluded from the final grade; it deletes only the old module placement. Checkpoints in deployment state preserve new page/item identities if a step fails. Do not automatically retry an API failure; report it and inspect the checkpoint.
5. Push the four reflections, the updated Brainstorm walkthrough instructions, and the eight unpublished Sprint 5 work artifacts normally. The latter clears their requirements using Canvas's supported empty completion-requirement object and verifies the response. All original publication flags stay intact.
6. Freshly verify page 3624 / module item 17985 in module 2079 and page 3628 / item 18017 in module 2081 are still unpublished. Remove only those two module items with `CanvasClient.delete_module_item`. Retain the underlying pages. Preserve a recovery record and clear the removed module-item IDs in their corresponding deployment-state entries through `CanvasStateStore`, preserving the retained page identities. Never call `delete_page` or `delete_assignment`. Assignment 7153 / module item 17982 is the current graded Problem Frame and stays intact.
7. Push the five later module headers, then verify prerequisite IDs and release instants. Re-lock modules 2079, 2084, 2081, 2082 and 2076 using `PUT modules/<id>/relock` so previously unlocked progress is recalculated under the new requirements. Canvas documents this step for requirements added to an active course.
8. Re-render final hosted indexes from actual published module positions and updated deployment state. Inspect every active concept page/iframe, the homepage, reflection grading/submission fields, all module prerequisite/date settings, and unpublished-item requirements. Compare published flags, item order, and every graded deliverable's points against the backup. Validate the final state and save the verification report.
9. Commit/publish generated hosted output and mutable state through their established workflows, then merge the reviewed source change through the protected GitOps path. The default publish workflow must not encounter the old assignment-to-page identities: complete and record the approved conversion before merging this source. No remote branch, PR, merge, state push or deployment was performed during preparation.

The source credential target remains the CTI production manifest. No additional user approval was requested during preparation; normal repository checks or protected publishing approvals may still apply in the original task.

## Exact source commands

Run from the prepared source checkout, using its validation Python or the existing runtime Python. Set `STATE_DIR` and `HOSTED_DIR` to the established checkouts; these variables hold paths, never credentials.

```sh
python canvas_sync/push.py --file <concept-file> \
  --manifest course1/manifests/production.json \
  --state-dir "$STATE_DIR" --hosted-output-dir "$HOSTED_DIR" \
  --convert-concept-page
```

Concept files and original assignment IDs:

| File | Assignment |
|---|---:|
| `course1/sprints/sprint-14/sprint-1-concept-check.md` | 7154 |
| `course1/sprints/sprint-16/sprint-2-self-check.md` | 7174 |
| `course1/sprints/sprint-15/sprint-3-concept-check-v4.md` | 7180 |
| `course1/sprints/sprint-8/sprint-4-concept-check-v4.md` | 7181 |
| `course1/sprints/sprint-9/sprint-5-concept-check.md` | 7189 |

Use the same command without `--convert-concept-page` for normal artifact pushes:

- `course1/sprints/sprint-14/sprint-1-reflection-what-changed-v54.md` (7155)
- `course1/sprints/sprint-16/sprint-2-reflection-what-the-world-said-back.md` (7173)
- `course1/sprints/sprint-15/sprint-3-reflection-and-mid-course-problem-frame-revision-v3.md` (7157)
- `course1/sprints/sprint-8/sprint-4-reflection-what-changed-v3.md` (7161)
- `course1/sprints/sprint-14/brainstorm-your-list-walk-through.md`
- The eight Sprint 5 sources with `completion_requires_published: true`
- Module headers `sprint-14/sprint-1-find-the-problem-worth-solving.md`, `sprint-16/sprint-2-is-this-problem-worth-pursuing.md`, `sprint-15/sprint-3-integrate-people-and-context-v3.md`, `sprint-8/sprint-4-close-the-learning-gap-v3.md`, and `sprint-9/sprint-5-synthesize-and-show-readiness-v2.md`, each under `course1/sprints/`.

## Preparation verification

Full source schema and homepage validation passed. The Python suite passed 367 tests with one existing skip. The shipped guided-response runtime passed, including practice with absent copy controls. JavaScript syntax checks passed. Link audit: 172 artifacts, 59 links, zero errors. Hosted preview rendered 99 artifacts; all five concept documents and their previous hosted assignment aliases were checked for retained practice, no submission guidance and no response-copy controls. No live result is claimed by these local checks.

API reference: https://developerdocs.instructure.com/services/canvas/resources/modules

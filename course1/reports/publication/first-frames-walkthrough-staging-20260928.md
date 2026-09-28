# First frames Canvas Walkthrough: unpublished staging

The user's approved implementation plan authorized this separate unpublished replacement. Final release is deferred until Leslie's revised Sprint 1 DOCX is reconciled.

Protected Publish Canvas run: https://github.com/profsathya/applying-ai-at-work/actions/runs/36459953039

Source commit: `6548e2d393a21ebc9222f2e5c6d6db756312617c`, draft PR https://github.com/profsathya/applying-ai-at-work/pull/132. Exact workflow target: `course1/sprints/sprint-14/first-frames-canvas-walkthrough.md`. Hosted commit `83d97877b82ea4d2f4d1de5c65904a930371e155` adds only the replacement HTML. No shared hosted pages or original assignment content were republished.

## Live state verified

| Item | Assignment | Module item | Visibility | Submission |
| --- | --- | --- | --- | --- |
| First frames | 7151 | 17979 | Published | Text entry |
| First frames Canvas Walkthrough | 7182 | 18016 | Unpublished | File upload |

Both assignments are in module 2079, worth 35 points, in assignment group 323. All inspected assessment settings other than the explicitly requested submission type match, including dates, grading, attempts, rubric settings and empty overrides. The original still has no submissions. The new assignment has a must-submit completion marker, inactive for participants while unpublished. Homepage routing still targets the original.

The live module order is 17981, 17977, 17980, 17985, **17979, 18016**, 17978, 17983, 17982, 17984, 17967. Removing the new ID reproduces the exact preflight order. API comparison and the existing desktop Chrome Canvas module view both verify adjacency and publication state. An initial baseline comparison checked an unsnapshotted field and was corrected to compare only captured original fields; full replacement-to-original assessment comparison passes.

Deployment IDs and hashes are recorded by the workflow in `canvas-state:course1/production.json`, never in artifact frontmatter. Private local evidence is under `.source-intake/first-frames-20260928/`, including the preflight/readback JSON, Chrome export, rendered Word page, preview results and screenshots.

## Browser checks and limits

See the authoring review for local automated checks and Word inspection. Additional manual checks: Codex right-panel input at 99 versus 100 characters correctly toggles Download; Chrome keyboard Tab then Return opens a self-check; all five self-checks expose the same nine complete criteria. Synthetic Codex and Chrome preview drafts were cleared. No coursework was submitted.

Hosted Pages deployment [36460129602](https://github.com/profsathya/Common-Curriculum/actions/runs/36460129602) completed successfully. The first iframe visit showed a transient 404 while deployment ran; after completion, the normal Canvas assignment page loaded the full walkthrough. No content retry or bypass was used.

In the real Canvas iframe, three synthetic responses enabled Word download, survived a Canvas-page reload, and produced `first-frames (1).docx` containing all three responses. Clearing and reloading left all test fields empty and disabled Download. The artifact reference opened the native Canvas **The problem frame** page. The Canvas page visibly reports **35 points**, **file upload**, and **Unpublished**. The original publication indicator remains green in the adjacent module row. No assignment was started or submitted; no Student View publication/access claim is made while the replacement is unpublished.

The local preview remains open in Codex's right-side panel and a dedicated Chrome tab. The existing desktop Canvas tab is left on the staged replacement. Screenshot `canvas-staged.png` records module order and publication indicators. All entered synthetic draft responses were cleared.

## Before final release

Reconcile Leslie's revised DOCX, including its relationship to the September 27 grid/AI/merged-page design and surrounding Candidate Log references. Keep the user's explicit five-box/no-AI design unless a later instruction changes it. Rerun affected authoring, provenance, homepage and browser checks.

Refresh live state and submission status, route homepage/completion to the replacement, rename the source to `First frames (Original)`, and coordinate the visibility switch through the protected publisher. Publish and verify the replacement before unpublishing the original; retain the pre-release visibility snapshot for rollback. The current `walkthrough_release.py` conversion exception covers only zero-point text-entry-to-Word conversions; its guarded comparison must be extended and tested for this expressly authorized equal-35-point conversion before release. Do not bypass its other assessment, submission, adjacency or rollback safeguards.

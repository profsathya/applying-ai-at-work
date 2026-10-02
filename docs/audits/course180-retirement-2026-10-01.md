# Course 180 obsolete-content retirement

After a verified, privately retained full-course Canvas export (export 745), retire only the approved unpublished legacy content:

- Assignments 6947–6952, 6965–6970, and 7182.
- Pages 3470, 3471, 3476, 3477, 3594, and 3620.
- Legacy module containers 1947 and 1950.

The Canvas readback confirms exactly these removals. All retained instructional metadata is unchanged; module positions shift as expected. The course still has 40 published module activities, 50 assignments, 16 pages, 3 quizzes, 1 discussion, and 8 modules. New walkthroughs, Sprint 5 shell assignments 7186–7193, protected pages 3627/3628, check-in 3629, and retained original submission targets remain intact.

The old sprint-2 and sprint-5 Markdown, including their module headers, is preserved without content changes under `archive/course180-retired-2026-10-01/`. Removing it from active `course1/sprints/` prevents a full publisher run from recreating retired objects. The two corresponding hidden homepage groups are removed; the current schedule and visible homepage groups are unchanged. The obsolete 7182 source file was already absent. Authoritative deployment state removes only the retired artifact mappings. Hosted cleanup disables twelve stale native assignment anchors and six AI-engine Canvas targets; it preserves the archived instructional HTML, activity data and assets.

## Recovery

The pre-cleanup export is 173891 bytes, SHA-256 `88f8e33e528a1bec843c9a47bc2d2535220a884656755f163bcd15688618e05c`. ZIP integrity, the IMS manifest, and coverage of all 19 objects and both containers were verified before deletion. The owner retains the private Drive copy; a separate local baseline retains source, hosted files, state, instructional metadata and the deletion receipts.

Canvas's ordinary course-content restore interface supports assignments, pages and modules. If an item is unavailable there, import the retained IMSCC through Settings → Import Course Content → Canvas Course Export Package, choosing only the required archived content. Recheck titles, iframe URLs, unpublished state, module placement and completion settings after restoration. Imported objects may receive new IDs. Restore the matching source/state mappings deliberately before any subsequent publisher run; do not overwrite the current deployment state with the old complete state file.

The IMSCC is course content, not student submissions or grades. Remote hosted files are separate and remain preserved. No student work was read or exported during this retirement. No De Anza import or broad Canvas publishing was performed.

Validation: schema and link audit pass; existing unit suite passes (356 tests, one skipped). Homepage-maintainer review confirmed that only the two hidden metadata groups required adjustment.

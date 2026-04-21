# Course 1 — First Build Notes (2026-04-20)

Post-build report for the first real canvas-course-builder run, pushing Course 1 (Problem Framing with AI, AIW-101) into De Anza canvas course 180.

## Shape delivered

- **35 artifacts** across **6 modules** (sprint-0 orientation, sprints 1-4, week 10 capstone). 33 built successfully, 2 failed on `due_at` formatting and remain in `failed` state.
- **Type breakdown:** 16 assignments, 6 pages, 6 discussions, 6 module_headers, 1 quiz.
- **Real-stakeholder touchpoints:** one per sprint, as the design spec requires. Listening conversation (sprint 1), second interview (sprint 2), success-criteria validation (sprint 3), decision-maker validation (sprint 4).
- **Wall-clock:** ~90 minutes total, including ~25 minutes lost to the permission-mode bug on the first two loop attempts. Once the loop was running cleanly, typical iteration was 30-90 seconds; opus planning iteration ran 2-5 min.

## Sprint-level read

| Sprint | Title | Coherence |
|--------|-------|-----------|
| 0 | Week 1: Orientation | Coherent. Choose-your-problem + initial stakeholder map do real work on day one. |
| 1 | Surfacing the Problem | Coherent. First-pass statement → assumption audit → listening conversation is a legible arc. |
| 2 | Scope and Stakeholders | Coherent, but the "Synthesize What You Heard" assignment failed to push, so the arc has a visible gap until that item is repaired. |
| 3 | AI Fit and Success Criteria | Coherent theme, but "AI-Fit Analysis" failed to push and is the sprint's anchor. Same gap problem as sprint 2. |
| 4 | Validated Framing | Coherent. Integrated frame → decision-maker validation → revise is the strongest arc. |
| 5 | Week 10 Capstone | Coherent as delivered, but thin — five artifacts, no peer exchange discussion like the other sprints have. |

Sprints 1-4 share an identical skeleton: module_header, briefing page, three capability assignments, one peer exchange/critique discussion. This rhythm is partly by design (working-professional audience benefits from predictable cadence) but it makes the sprints feel interchangeable in shape even when their content differs.

## Gaps in `course1/design/`

The four sprints could have been assembled with fewer distinctive cues than the planner actually gave them. The design docs under-specify:

- **Capstone format.** `design/structure.md` says "demonstrate problem framing to peers and stakeholders" with no guidance on artifact type, length, audience, or rubric. The planner improvised three capstone artifacts that work but feel generic.
- **Per-sprint theming.** `design/outcomes.md` lists four high-level outcomes but does not map them to sprints. The planner made the mapping (sprint 1 → surfacing, sprint 2 → scope, sprint 3 → AI fit, sprint 4 → validation), and it's a reasonable mapping, but it was not specified.
- **Rubric patterns.** No guidance on how points should distribute across "structured thinking," "stakeholder validation," and "human judgment articulation" within an assignment. Every generated rubric was the planner's judgment call.
- **Peer exchange structure.** Each sprint has a "Peer Exchange" or "Peer Critique" discussion. The design docs do not differentiate these; the planner generated near-parallel prompts. The discussions could either be more differentiated or consolidated to one per course.

## Two failed items (ids 17, 21)

Both failed on canvas's strict `due_at` ISO 8601 + timezone requirement. The canvas-author subagent invented local-time `due` values the PRD did not request. MD files were subsequently corrected (the `due` field removed) but the PRD items were left in `failed` status and not reset to `pending`. Running the loop again will not retry them; a human must decide to reset or accept the gap.

Proposed fix before the next build: canvas-author's prompt should be tightened to never invent a `due_at` value that is not explicitly present in the PRD item.

## Recommendation

**Update design docs first, then rebuild.** The current build is usable as a starting point, and `/add-artifact` can close the two failed-item gaps. But the sprints feel more interchangeable than the course intends. Before the next design pass:

1. Flesh out `design/structure.md` with per-sprint themes, the specific stakeholder touchpoint expected, and the capability growth between sprints.
2. Add a `design/capstone.md` (or equivalent section) specifying capstone format, audience, length, and rubric shape.
3. Add a `design/rubrics.md` with the 3-5 canonical rubric patterns assignments should draw from, so the planner stops inventing them per-assignment.

Then re-plan (not rebuild from scratch). Manifest idempotency means only changed items will actually hit canvas.

## Immediate next steps

- Reset PRD items 17 and 21 to `pending`, or delete them if the sprint should have 5 artifacts instead of 6.
- Decide whether sprint 5 needs a peer exchange discussion.
- Review the two canvas modules that shipped with a missing assignment (sprint 2 and sprint 3) for module ordering.

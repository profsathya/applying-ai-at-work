# CIS 501: local Sprint 3 rubric example

**Recovered review draft, September 30, 2026.** These previews retain the assignment
snapshot reviewed on September 29. The authoritative assignment has since changed.
The rubric weights, submission wording, and evidence mappings need review against
the current assignment before production integration. Historical checks in
`validation.json` describe the September 29 draft; current recovery checks and the
stash disposition are recorded in [reconciliation.md](reconciliation.md).

This draft demonstrates a 50-point rubric for **Stakeholder Conversation Canvas Walkthrough**. It adds an assessment section to a locally rendered copy of the existing assignment. The authoritative assignment Markdown and Canvas have not been changed by this prototype.

Open the [participant view](http://127.0.0.1:8873/preview/index.html#rubric) or the [instructor scoring view](http://127.0.0.1:8873/preview/instructor.html). The instructor view lets you assign ratings and load an illustrative score example. It contains no participant submissions and sends no grades to Canvas.

The editable content is in [participant-self-check.md](participant-self-check.md), [instructor-rubric.md](instructor-rubric.md), and [rubric.json](rubric.json). The JSON is the shared source for the two views. Serve this directory on localhost port 8873 to inspect the preserved previews. The builder checks the recorded assignment hash and pinned Common Curriculum revision before writing. It currently stops because the assignment has changed. Reconcile the rubric with the current assignment and review its evidence before deliberately updating the provenance and rebuilding with `.venv/bin/python course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/build_preview.py` from the repository root.

## What changed in Sathya's latest approach

The checked Common Curriculum revision is `0f6ef025cd8b0526370909d5770c518cf902629c`, fetched September 29, 2026. The sibling checkout was read without pulling its older working tree forward.

- [Writing assignments v10, September 27](https://github.com/profsathya/Common-Curriculum/blob/0f6ef025cd8b0526370909d5770c518cf902629c/skills/writing-assignments/SKILL.md) calls for about ten weighted self-check items, in submission order. Each participant-facing line describes full-credit evidence. The 3 and 1 rungs, feedback priorities, and quality tags stay in the internal record. The instructor verifies each item; checked boxes alone earn no points.
- [CST349: How I learned, and my Sprint 2 growth goal, revised September 28](https://github.com/profsathya/Common-Curriculum/blob/0f6ef025cd8b0526370909d5770c518cf902629c/cst349/my-sprint-2-growth-goal-online-chat.md) implements nine weighted self-check items totaling 100 points. It permits a conversation to confirm a goal, suggest revision, or identify further investigation. This is the closest recent implementation used here.
- [CST499 Learning Plan](https://github.com/profsathya/Common-Curriculum/blob/0f6ef025cd8b0526370909d5770c518cf902629c/cst499/learning-plan.html) supplies observable criteria, self-checks, and a distinction between complete and strong work. Some pages still retain an older Done/Strong presentation; the newer guidance is more specific about the weighted checklist.
- [CST499 Project Proposal](https://github.com/profsathya/Common-Curriculum/blob/0f6ef025cd8b0526370909d5770c518cf902629c/cst499/project-proposal.html) asks participants to create project-specific A/B/C rubric descriptors. That is a project deliverable, rather than the latest universal assignment scoring structure.
- The files under [config/rubrics](https://github.com/profsathya/Common-Curriculum/blob/0f6ef025cd8b0526370909d5770c518cf902629c/config/rubrics/README.md) are older LLM submission-analysis prompts. Their most recent path history is April 5, 2026. Their existence does not establish an attached native Canvas rubric.

This is an adaptation of the maintained guidance, not a claim that Sathya reviewed or approved this CIS 501 rubric. The dated source snapshots and hashes are retained under `.source-intake/cis501-rubric-20260929/common-source/` and in `source-provenance.json`.

## CIS 501 adaptation

| Criterion | Points | Existing evidence |
| --- | ---: | --- |
| Starting point and stakeholder | 5 | Report A, current map and frame |
| Three questions that seek evidence | 6 | Question table |
| What each question could establish | 4 | What I hope to learn responses |
| Question review with AI | 5 | Required Part 1 JSON |
| Record of the real conversation | 10 | Report B |
| Immediate interpretation and next question | 5 | Report C |
| Evidence-supported Problem Frame | 8 | Report D |
| Evidence carried into the map | 5 | Updated Stakeholder Map |
| Usable submission | 2 | Identification, section organization and readability |
| **Total** | **50** | **Existing three-file submission** |

The points emphasize investigation and evidence. Preparation uses the participant's prior work; AI helps examine questions; a real stakeholder provides the account; the participant decides what that account establishes. Section D's remaining uncertainties feed Sprint 4's learning gaps. The original map's quality is assessed in its own assignment; this rubric assesses its conversation-driven updates.

The proposed conversion is maximum points multiplied by the 5/3/1 rating divided by five, plus zero for absent evidence. This conversion, the weights, and the CIS 501 capability tags are local design proposals. They are not copied scoring decisions from Sathya's courses. Internal tags reuse the item scores and do not create another grade.

Confirmation, revision, and justified uncertainty can each earn full credit. The rubric rewards supported progress from the starting frame. It requires neither a changed belief nor an AI mistake, and it does not score writing polish, AI agreement, or optional feedback use. Feedback addresses one or two priority gaps and leaves the participant to reason through the next move.

The participant sees only full-credit criteria and points. The grader's partial-credit ladder appears on a separate instructor page in this review package. A later Canvas implementation should preserve that distinction rather than automatically displaying all internal descriptors in participant-facing content.

## Preview boundary

The participant view uses the repository's normal hosted renderer for the unchanged assignment, then adds the proposed assessment section before submission controls. The original teaching, six report tables, task identities, and existing three required files are retained. The prototype has its own browser draft identifier and disables the row AI endpoint.

The self-check states are appended to the existing Word report using the renderer's document suffix. This demonstrates how those claims could travel with the submission without requiring a fourth file. That integration exists only in this local prototype; it has not been added to the production renderer or the assignment source.

This is a proposed participant experience and an instructor review tool, not an exact reproduction of Canvas's native rubric editor. The current sync code detects rubric changes but does not automatically publish native rubric associations. No Canvas creation, grading, submission, or publishing action was performed for this draft.

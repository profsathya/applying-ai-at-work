# Assignment 7166 AI feedback verification

- Assignment: https://cti-courses.instructure.com/courses/180/assignments/7166
- Source at the time of this feedback check: `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.md` (SHA-256 `f3729ae675349c505589114766dcaa58471ce2a752bc5a200e0f909311c44caf`). The later Word-submission update is recorded separately in commit `eace8a3`.
- Server guidance: `services/course-ai/netlify/functions/walkthrough-guidance.json` (SHA-256 `40a2b3323241067a77797638b4747e2e758c15c7cecfdea341d241d08e1abb74`). The `report-conclusion` criterion now treats a named future comparison as a plausible check and does not demand completed evidence in that row.
- Production service deploy: `6ab540fd7b500f77796426b7`, https://app.netlify.com/projects/cti-course-ai/deploys/6ab540fd7b500f77796426b7.
- Validation: artifact schema passed; JSON parsed; `git diff --check` passed; course AI service tests passed 10/10.
- Live provider check: all three registered checkpoints returned HTTP 200 and formative feedback with synthetic responses. After the final deploy, `report-conclusion` again returned HTTP 200 and recognized both the unresolved claim and the proposed record comparison.
- Canvas computer-use check: in the embedded assignment, the Question 1 AI button returned feedback on its selected row. The test answer and feedback survived a page reload. After the final deploy, the `What still needs validation` button returned feedback below the correct table, recognized the proposed check, and asked one focused follow-up. Student View displayed the published assignment and its Question 1 button also returned live feedback. Synthetic browser drafts were cleared through the assignment control, and the browser was returned to instructor view.
- Detailed synthetic samples and provider responses are in ignored `.source-intake/20260924-assignment-7166-feedback/`. No Canvas submission was made.

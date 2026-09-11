# V2 publication and Student View audit

Date: September 11, 2026. Target: [Canvas course 180](https://cti-courses.instructure.com/courses/180).

## Publication result

All existing current V2 content is published: five modules containing 25 content items. This includes the first half of Sprint 1; it does not mean the entire V2 curriculum has been authored.

| Module | Canvas module ID | Published content items |
| --- | --- | --- |
| Welcome and Orientation (V2) | 2075 | 6 |
| Sprint 1: Find the Problem Worth Solving (V2), first half | 2079 | 6 |
| Sprint 3 (V2) | 2071 | 5 |
| Sprint 4 (V2) | 2074 | 7 |
| Sprint 5 (V2), introduction placeholder | 2076 | 1 |

Source commit: `21e6b38`. The change set only switched publication flags in 23 Markdown files, including four module headers. Sprint 1 was already published. Local schema validation passed. [Protected Publish Canvas run 34624047918](https://github.com/profsathya/applying-ai-at-work/actions/runs/34624047918) succeeded with 23 artifacts published and zero failures; deployment state advanced to `4037c1a`. Live readback confirmed all five selected modules and all 25 mapped content items published.

The homepage retains the intended V2 module order. V1 modules remain published below the V2 modules in Canvas, as previously requested, and are excluded from the homepage. Unpublished duplicate/draft modules were not treated as current V2 content.

## Actual Student View testing

Testing used Canvas's real **View as Student** in Chrome, with the disposable Test Student account, rather than only an instructor preview or API inspection.

| Check | Result |
| --- | --- |
| Open every homepage-linked V2 item | All 25 accessible; pages, discussion, assignments, quizzes, and embedded content rendered. |
| Guided response save and reload, assignment 7144 | Response persisted after reload. |
| Copy guided response | Manual selection/copy fallback appeared; it clearly said copying did not submit work. Automatic clipboard copying was not demonstrated. |
| Native Canvas text-entry submission, assignment 7144 | Submitted a clearly marked QA response; Canvas displayed Submitted and submission details. |
| Sprint 1 concept check, assignment 7143 | Wrong-answer feedback and revised correct-answer feedback worked. |
| Sprint 3 native concept check, quiz 3096 | All five questions rendered, including true/false; submitted a test attempt and received 5/5. No unsupported-question banners appeared. |
| Sprint 4 AI Exchange, assignment 7131 | Activity opened, but generating follow-up questions failed. See finding 1. |
| Homepage completion readback | Progress advanced from 0/25 to 10/25 during testing; the submitted guided assignment showed completed. |
| Native Modules sequence | Primary V2 modules appeared first, but several item sequences differed from the homepage and source. See finding 2. |

Cleanup: cleared the saved browser drafts for assignments 7144 and 7143 and verified their cleared status; cleared the AI Exchange test prompt. Canvas confirmed **The test student has been reset successfully**, clearing test history, including the submission and quiz attempt. Left Student View and verified the instructor **View as Student** control returned.

Coverage limits: no discussion replies were posted; no real stakeholder messages were sent; external Dojo setup was not exercised. Representative submission, quiz, and guided interactions were tested, not every possible response path or every AI activity. The AI Exchange failure prevented verification of its downstream JSON export. Findings below were recorded, not repaired by this publication pass.

## Findings

### 1. Blocking: AI Exchange cannot generate follow-up questions

[AI Exchange: Is This a Gap?](https://cti-courses.instructure.com/courses/180/assignments/7131) opened its hosted activity successfully. A fictional, nonsensitive 274-character QA prompt satisfied the minimum length. Clicking **Get Follow-up Questions** produced:

> Could not generate questions. Empty response from AI service

The browser also logged `AI discussion error: Error: Empty response from AI service` from `activity-components.js:1542:15` at `2026-09-11T16:53:40.814Z`. This blocks the tested follow-up workflow. The underlying service cause was not established, and JSON export after a successful exchange remains unverified.

### 2. High: native Canvas item order differs from the learning sequence

Confirmed through live inventory and the Student View Modules page. The homepage order is correct; native module navigation can lead participants through a different sequence.

| Module | Observed Canvas sequence | Intended homepage/source sequence |
| --- | --- | --- |
| Orientation | Start Here; Welcome; Your First Week; How This Course Works; Introduction Post; Help and Resources | Start Here; Welcome; How This Course Works; Your First Week; Introduction Post; Help and Resources |
| Sprint 3 | Introduction; Concept Check; Stakeholder Conversation; Reflection; Dojo Lab: Stakeholder Map | Introduction; Concept Check; Dojo Lab: Stakeholder Map; Stakeholder Conversation; Reflection |
| Sprint 4 | Introduction; Concept Check; Name the Gap; Reflection; AI Exchange; Learn and Check; Dojo Lab: Design Path | Introduction; Concept Check; Name the Gap; AI Exchange; Dojo Lab: Design Path; Learn and Check; Reflection |

For example, AI Exchange's native Previous link points to Reflection, even though Reflection should close Sprint 4. Sprint 1's mapped content order was correct.

### 3. High: grading configuration contradicts participant instructions

- Sprint 3 concept check (quiz `3096`, assignment `7118`) and Sprint 4 concept check (quiz `3099`, assignment `7135`) say they are not graded assessments. Both are configured as assignment quizzes worth five points with one attempt. The actual Sprint 3 test attempt produced a 5/5 score.
- Introduction Post (discussion `1533`, assignment `7121`) describes complete/incomplete grading, but Canvas uses points grading with zero possible points and `omit_from_final_grade: false`.

These require a decision about intended assessment behavior before changing either prose or settings.

### 4. High: source rubrics are absent from three live Sprint 3 assignments

Live Canvas rubric arrays were empty for:

| Assignment | Canvas ID | Source rubric criteria |
| --- | --- | --- |
| Dojo Lab: Stakeholder Map | 7117 | 6 |
| Stakeholder Conversation | 7120 | 7 |
| Sprint 3 Reflection | 7119 | 4 |

The publisher explicitly warned that rubric changes are not automatically published and require manual application followed by the rubric acknowledgment workflow. Successful content publication therefore does not establish rubric parity.

### 5. Content gaps and visible authoring placeholders

- Sprint 2 V2 is absent.
- Sprint 1 contains its first half only; its introduction describes later work that is not yet present.
- Sprint 5 contains only a published introduction placeholder stating that its rebuild is not written. There is no final assignment in that module.
- Orientation exposes unfinished welcome video/bio, weekly time estimate, Canvas/Dojo/JSON guidance, and contact/response-time placeholders.
- Sprint 4 AI Exchange contains unfinished mechanics/save/upload guidance, and its Dojo Lab includes a walkthrough-video placeholder.

These are existing content-readiness gaps made visible by publishing, not publication failures.

### 6. Medium: generated labels and directions are confusing

- Some rendered headers expose storage sprint numbers alongside learner-facing numbers, such as `course1 · Sprint 6 · Sprint 0 ... V2`. Storage sprints 7, 8, and 9 similarly represent learner-facing Sprints 3, 4, and 5.
- Some activity headers say Discussion or Quiz although the native Canvas object is a file-upload assignment, including Stakeholder Conversation and AI Exchange.
- Introduction Post's generated learning goal says to compare practical uses of Introduction Post, which does not describe the introduction task.
- Introduction Post's generated submission footer asks for peer replies, while its body asks participants to read others' introductions.

## Recommended correction order

1. Restore the AI Exchange's working generation path and retest through export/submission.
2. Align native Canvas item positions with the existing homepage sequence while preserving item identities.
3. Resolve assessment intent, align grading settings, and deploy the missing rubrics.
4. Complete or explicitly label unfinished V2 sections and replace visible placeholders.
5. Correct generated labels and duplicate/conflicting directions, then repeat focused Student View checks.

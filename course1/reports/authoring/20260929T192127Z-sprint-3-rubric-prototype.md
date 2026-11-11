# CIS 501 Sprint 3 rubric prototype review

Status: local draft authorized for demonstration. Editorial assessment is the agent's; human approval of this rubric and Sathya's approval were not assessed. Canvas and authoritative course artifacts were not edited by this prototype.

## Scope and evidence

Target: Stakeholder Conversation Canvas Walkthrough, participant self-check and separate instructor scoring record. The intended capability is testing a workplace Problem Frame with a real stakeholder, separating evidence from inference, and carrying justified conclusions into an updated map and Sprint 4 learning gaps.

Read-only context: the target assignment and its source-provenance metadata; Stakeholder Map Canvas Walkthrough; Name the Gap Canvas Walkthrough; course1/homepage.yaml; course1/design/outcomes.md and the relevant Sprint 3 and AI-use passages in course1/design/problem-spine.md. Approved presentation reference inspected: course1/sprints/sprint-12/test-and-commit-v2.md, for a longer assignment with adjacent instructions and responses. The prototype uses the normal renderer for the unchanged source and adds one assessment section before submission controls. No baseline revision was required for the newly drafted rubric; the unchanged original was rendered into .source-intake/cis501-rubric-20260929/baseline/ before drafting.

Common Curriculum origin/main inspected at 0f6ef025cd8b0526370909d5770c518cf902629c. The latest relevant writing-assignments guidance is v10, September 27; the September 28 CST349 growth-goal assignment implements nine weighted self-check items. Additional comparisons: CST499 Learning Plan and Project Proposal. Older config/rubrics prompts were distinguished from current Fall criteria and from native Canvas associations. Exact snapshots and hashes are in source-provenance.json and the ignored evidence directory.

## Decisions and review findings

The nine weighted items total 50 points and use only evidence already requested in the report, map, and required Part 1 AI JSON. The full-credit lines are participant-facing; 3/1/0 rungs, internal capability tags and feedback priorities are separate. The weighted conversion and zero for absent evidence are explicitly local proposals. Confirmation, revision, and justified uncertainty can each receive full credit. No new interview, peer requirement, word count, deadline or late policy was added.

Resolved: question quality is scored separately from the diagnostic AI exchange; the prior Stakeholder Map is not graded again; the readability item does not repeat a missing-file deduction; clearing the browser draft resets added self-check states as well as original responses; the inherited module link was changed to an assessment link for this isolated preview. Text alone serves the rubric comparison; no new illustration was needed.

Adult-learner review: the first assessment action is to compare the report with nine evidence statements. Each statement maps to existing work in submission order, and the shared export remains adjacent to the rubric. The required teaching remains in the original assignment. Added text explains assessment rather than repeating the conversation procedure. Resume checks restored both a synthetic response and a checked box. The mobile self-check stayed in one readable column; the instructor ladder stacked in rating order. No participant learning or engagement was measured.

Deferred: production integration of the self-check into the renderer and any Canvas rubric association are outside this local-demonstration request. A future implementation should preserve the learner/instructor distinction in the current guidance. The prototype is not a native Canvas rubric-editor screenshot.

## Observed validation

- `.venv/bin/python course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/build_preview.py`: PASS after fixing the generated config tag selector. Rebuilds preserved the authoritative assignment hash.
- `.venv/bin/python canvas_sync/schema.py --all`: PASS. Report/prototype files are outside the course artifact schema; this does not validate a native rubric payload.
- CUA manual browser review: desktop and 390px mobile layouts, nine accessible checkbox labels, keyboard checkbox/disclosure operation, reload persistence, native clear behavior, instructor 50.0/50 full-evidence total, 30.0/50 all-partial total and 41.2/50 illustrative total all observed. Feedback selected the frame judgment and updated-map rows in priority order. Synthetic responses and checks were cleared; illustrative instructor scores are clearly labelled as invented.
- Bundled Node ran `.source-intake/cis501-rubric-20260929/check-export.cjs`: PASS for the exact prototype initialization and native Word-export JavaScript, without a browser or network. Python ZipFile/XML inspection confirmed a valid DOCX, six original report tables, synthetic response, two checked and seven unchecked self-check statements.
- CUA displayed the Word-downloaded status, but its download-event waiter timed out and reset the runtime. The browser file receipt was not retrieved; exported bytes were verified independently offline.
- Git status: the nine earlier source/homepage modifications were preserved. This turn added only the rubric-prototype report directory and this review record. Common Curriculum remained clean.
- Not run: full module-preview browser suite, enlarged-text/zoom testing, screen-reader certification, live AI feedback, Canvas writes or submissions.

## Skills and reference versions

Applied: writing-assignments local revision 4 and reviewing-course-text local revision 6. update-artifact was consulted to establish the live-edit boundary; its preparation/apply workflow was not invoked because authoritative content was not revised. Upstream writing-foundation, writing-assignments and writing-to-teach were read as requested comparison sources; their hashes are recorded in source-provenance.json.

| Local reference | SHA-256 |
| --- | --- |
| .agents/skills/writing-assignments/SKILL.md | 767ad4bbc05b0333c0b95c8ec6632c872b389f403540d0d0794689b48ba0b4c2 |
| .agents/skills/reviewing-course-text/SKILL.md | 1614ebaf7e321064f02c7a9041d5443e3c1c45c800a278a0fd54cd539fb7401c |
| .agents/skills/update-artifact/SKILL.md | 443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80 |
| .agents/skills/reviewing-course-text/references/review-record.md | 3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e |
| docs/AUTHORING.md | cca09dec02d660db8ba107060aeb85a49461cf75f39c32b062bc24a1e4754af4 |
| docs/AUTHORING_PRESENTATION.md | 5d9a732651a1a9c4d95b5fec7ac152b56e7c52f270c3f8779c1d4679a9be5ba8 |

## Final reviewed outputs

| Output | SHA-256 |
| --- | --- |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/README.md | 131e186d3a7de928e2b299a26c1d5b1fa312aca2ccecd660ca4fe8bf705fbe29 |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/build_preview.py | d9846e10f9be7d9df2d0c58003595b3b49edca6603adc7193266183aa216e010 |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/instructor-rubric.md | d7d99856dcede775b1390aa0d8e7b168336dc8e7a7a386c9cd4fdfaa8e6ce642 |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/participant-self-check.md | 436529b30ed21b85b22e92b24f8ef52b334e290db0302b257203fc3d49d00de2 |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/preview/index.html | dff72c08fd0f15d86a5f0b0353938c2a3b594e6414f125fb3505c31b64380c6d |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/preview/instructor.html | b0b277c70a4fbd6dee2bbe4e3db069795fa160d55e4a45227c64692c5685a9df |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/rubric.json | 05f7f464a61134ca0300f8d3dd6d09ef6842e698d046f473ad56bc7d66fe7c79 |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/source-provenance.json | 6a202829e12f214dc8cb53d291c2dcffcadb07bccf9ac5244999c2badb5845ef |
| course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/validation.json | 1cb7e1732b93c8ee1aa58a2e6512bf7535b9d7fc82791e62755f62e169a7d4db |

Screenshots: .source-intake/cis501-rubric-20260929/participant-desktop.png, participant-mobile.png, instructor-desktop.png, instructor-mobile.png. Detailed checks: course1/reports/rubric-prototypes/sprint-3-stakeholder-conversation/validation.json.

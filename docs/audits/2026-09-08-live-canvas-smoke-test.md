# Course 180 live smoke test

The audited builder created and published one additive test module in the live Canvas test course. API readback passed for its page, text-entry assignment, and native Classic quiz. Repeating publication preserved object IDs and produced no duplicates. A subsequent page-body edit used the hosted-content update path with zero Canvas writes.

## Target and scope

- Instance: `https://cti-courses.instructure.com`, course ID `180`.
- Actual course name and code: `cti-de-anza-test-course`. It was already published (`available`) and private.
- New module: **Course Builder Smoke Test - 2026-09-08**, ID `2077`, position `15`, published.
- Local source: `course1/sprints/sprint-10/`, with three unique artifact IDs. Homepage metadata now includes an optional technical-review group.
- Existing course state: all 14 previous modules and 74 previous module items retained their metadata and order. Selected global settings, including course publication, privacy, default view, timezone, and dates, were unchanged. No existing content object was targeted for an update.
- No learner submissions, grades, enrollments, messages, or notifications were intentionally created. Quiz update requests explicitly suppress update notifications.

## Review links

[Open the test module](https://cti-courses.instructure.com/courses/180/modules#module_2077). Module-item links below were returned by Canvas API readback.

| Item | Canvas ID / module-item ID | Result |
| --- | --- | --- |
| [Read Me page](https://cti-courses.instructure.com/courses/180/modules/items/17958) | `3616` / `17958` | Published Page; first item; `must_view` |
| [One Work Task assignment](https://cti-courses.instructure.com/courses/180/modules/items/17959) | `7137` / `17959` | Published Assignment; second item; one point; `online_text_entry`; `must_submit`; no due date |
| [Definition Check quiz](https://cti-courses.instructure.com/courses/180/modules/items/17960) | `3100` / `17960` | Published Classic Quiz; third item; three points; `must_submit`; no due date |

The quiz has exactly three one-point questions: `multiple_choice_question`, `true_false_question`, and `short_answer_question`. API readback matched every question prompt, answer text, answer weight, and total point value to the Markdown input. The short-answer key is `stakeholder`.

## Native Canvas and hosted instructions

The production manifest stayed unchanged, with hosting enabled. All three artifacts explicitly use `delivery_mode: canvas_native`. This preserves genuine Canvas Page, Assignment, and Quiz types, while their instructional bodies use the existing hosted iframe and fallback-link integration. The quiz was not converted into an AI activity.

Only four generated files were deployed to Common Curriculum: the three smoke-test instruction pages and `deanza/course1/sprint-10.html`. Rendering used `canvas_sync.hosted_html`; no generated HTML was edited by hand. The rest of the course was rendered only into isolated staging and was not deployed. The public course homepage was not replaced, avoiding publication of unrelated course drafts. Open the test through its Canvas module or [standalone test sprint index](https://profsathya.github.io/Common-Curriculum/deanza/course1/sprint-10.html).

The hosted pages were deployed and checked before Canvas was pointed at them. A second scoped deployment added the actual Canvas links and the harmless page edit. Final network and deployment results are recorded below.

## Changes found while testing

1. **New-module visibility.** Canvas returned an unpublished module after creation despite the requested published flag. During the three-item creation, the next artifact's existing-module path published it. The resolver now checks the create response and explicitly publishes the new module immediately when necessary, so a one-item push does not stop at an unpublished module. Regression coverage reproduces this response and checks that unnecessary visibility writes are skipped. The original live response and successful subsequent publication supplied the evidence; an additional module was not created merely to exercise the fix.
2. **Quiz publication order and notifications.** Preparation against the official API documentation exposed that quiz updates default to notifying users. The builder now sends `notify_of_update: false`, creates new quizzes as drafts, builds all questions, and publishes after the questions succeed. Both initial publication and repeat publication passed live. Regression tests cover call order, failure before publication, and silent updates. See the [official quiz API](https://developerdocs.instructure.com/services/canvas/resources/quizzes).

## Validation evidence

| Check | Outcome |
| --- | --- |
| Full local suite | 174 tests passed |
| Full schema validation and Python compilation | Passed |
| Native types, titles, points, visibility, order, completion, and submission method | Passed API readback |
| Three quiz question types, prompts, answer structure, and weights | Passed initial and repeat readback |
| Unchanged repeat publication | Same module/item/content IDs; exactly three quiz questions; no duplicate objects |
| Harmless Read Me edit | `content_update`, zero Canvas writes; source and hosted hashes updated |
| Existing modules/items and selected course settings | Unchanged across baseline, initial, repeat, and final verification |
| Authoritative external state | Schema-valid; exactly three new entries; all 85 prior entries preserved byte-equivalently as JSON values |
| Public hosted output | All four canonical URLs returned HTTP 200 and matched generated SHA-256 bytes; all five distinct relative navigation links returned HTTP 200 |
| Final GitHub Pages deployment | [Run 34280583932](https://github.com/profsathya/Common-Curriculum/actions/runs/34280583932) succeeded |
| Downstream context-doc workflow | [Run 34280585744](https://github.com/profsathya/Common-Curriculum/actions/runs/34280585744) succeeded; no configured course matched the scoped De Anza paths, so document writes were skipped |
| Audit-branch CI | No run expected or triggered: validation runs on main or pull requests, production publication on main; no PR or merge was created |

Direct single-artifact quiz re-publication currently replaces its question set even when source is unchanged. The smoke re-run exercised that behavior: eight quiz API writes, no notifications requested, stable quiz ID, and three replacement questions. Batch publication has its own unchanged-source filtering. This test does not establish safe question replacement for quizzes with real submissions.

## Source and deployment records

- Audit branch: [codex/audit-canvas-maintenance](https://github.com/profsathya/applying-ai-at-work/tree/codex/audit-canvas-maintenance).
- Original audit commit: `bbf2bb4bf33ad0c06181314f62ded2ae88698790`.
- Smoke source and quiz fix: `8c4a334`.
- Module visibility fix and harmless page edit: `e6d0de1`.
- Deployment state: [canvas-state commit f88db58](https://github.com/profsathya/applying-ai-at-work/commit/f88db58c1f96fbaacdf78aea7faf5f9c587cd18c), `course1/production.json`.
- Hosted output: [Common Curriculum commit e4a8afb](https://github.com/profsathya/Common-Curriculum/commit/e4a8afb4c88b451c52970b4dfff31056f0a86e63), following initial test-page deployment `7b47d15`.
- Applying AI at Work `main` remained at `a078404`; no production source merge or production publishing workflow was triggered.
- Local API snapshots, request summaries, verification results, and attended scripts: `course1/reports/smoke-20260908/` (ignored generated diagnostics).
- Current live ledger: `course1/reports/canvas-ledger-production.json` and `.md`.
- Isolated state checkout: `/tmp/applying-ai-canvas-state-smoke-20260908`.
- Isolated hosted checkout: `/tmp/common-curriculum-smoke-20260908`.

The sources remain on the audit branch while their test deployment records are on `canvas-state`. Use that audit branch to maintain the smoke artifacts until it is reviewed and merged. Existing unrelated missing-local-path and empty-module warnings were preserved.

## Limits

This verifies the authored content and the live API publication/update path in Course 180, plus its hosted instruction delivery. It does not verify New Quizzes, a learner quiz attempt or grade calculation, real submissions, browser or mobile usability, LTI progress, AI-activity execution, or the protected merge-to-main workflow. No discussion was added; the three-item scope covered the requested page, assignment, and quiz. The user can now inspect the retained module directly.

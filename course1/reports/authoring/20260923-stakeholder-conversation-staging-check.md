# Stakeholder Conversation Canvas Walkthrough: staging check

## Deployment

- Source branch: `codex/stakeholder-conversation-walkthrough`, commit `068a11d`, [PR #112](https://github.com/profsathya/applying-ai-at-work/pull/112) stacked on the existing walkthrough audit branch.
- [Protected exact-file Canvas workflow](https://github.com/profsathya/applying-ai-at-work/actions/runs/35919971467): validation and publish jobs succeeded. The new assignment is staged as an unpublished Canvas item.
- Hosted Common Curriculum commit `958d0f5`; [Pages deployment](https://github.com/profsathya/Common-Curriculum/actions/runs/35920113972) succeeded. The [hosted walkthrough](https://profsathya.github.io/Common-Curriculum/deanza/course1/assignments/stakeholder-conversation-canvas-walkthrough.html) returned HTTP 200 with the expected title and supplied report-copy link. Served HTML SHA-256: `ee539cfdf468d5f3b90906e45ba9426d58bf8fbe4c06e16c73ce058f4eb60b49`.
- Reviewed feedback registry deployed to production Netlify site `cti-course-ai` as deploy `6ab43d3e60d281fded6c9a06`. The existing model and credentials were unchanged.

## Canvas state after staging

Live Canvas course 180, module 2081, read through the Canvas API after the protected workflow:

| Position | Module item | Assignment | State |
| --- | --- | --- | --- |
| 7 | 17990, Stakeholder Conversation | 7158 | Published source |
| 8 | 17996, Stakeholder Conversation Canvas Walkthrough | 7164 | Unpublished staged alternative |
| 9 | 17989, Sprint 3 Reflection and Mid-Course Problem Frame Revision | 7157 | Published |

The [staged Canvas assignment](https://cti-courses.instructure.com/courses/180/assignments/7164) loaded its full hosted iframe in Chrome. Canvas labeled it **Unpublished**. Source and replacement match on 50 points, file upload, points grading, no dates, and no rubric. Both have zero overrides; the replacement has zero submitted work. The original remains published and unchanged. The private readback is `.source-intake/stakeholder-validation-report/canvas-post-stage.json`.

## Live interaction

In the actual Canvas iframe, a synthetic validation question enabled its row feedback button. The production provider responded with formative feedback about the question's specific past-experience prompt and a useful caution that it presupposed delay. The original answer stayed in its cell; no grade or invented stakeholder fact appeared. Earlier direct production samples returned 3/3 HTTP 200 responses, recorded privately in `.source-intake/stakeholder-validation-report/live-feedback.json`.

The iframe's **Copy work** button reported that it copied a table. Native Command-V into a blank signed-in Google Doc reported **Pasted table cells**. The exported DOCX retained six two-column tables, all 22 source rows and 44 cells, the seven headings, four synthetic answers, two internal multiline answers, and all blank cells. The left-column labels and heading sequence matched the prior source-checked export; differences after normalization were only the four test answers. The scratch Doc is [here](https://docs.google.com/document/d/1clAdxC9m-KI6ODOCBSNPC0y6BiprFQPvNS-xRWFr09M/edit); export SHA-256 `1c0714a5a50291927e74fbd42653b8474f6ef524d1f131e6731330f4dd30ea94`. Private comparison: `.source-intake/stakeholder-validation-report/google-paste-live-result.json`, with zero errors. The browser account and connector account differ, so the browser-exported DOCX supplied the structure check.

The synthetic Canvas browser draft was then cleared. All four edited fields became blank. No Canvas submission was made.

## Release boundary

This check covers unpublished staging and production service behavior. A later release would publish the new item and unpublish the original only after explicit approval and another pre-release state check. The linked original Part 1 AI exchange remains accessible for its required JSON evidence.

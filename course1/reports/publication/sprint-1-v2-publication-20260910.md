# Sprint 1 V2 publication verification

User authorization: push the reviewed draft to main, publish Canvas, and update the homepage. Completed 2026-09-10.

- Content commit: `ff82750d4e7652a752f31257807ba24bfd47bfda` on applying-ai-at-work main.
- Protected [Publish Canvas run 34517237291](https://github.com/profsathya/applying-ai-at-work/actions/runs/34517237291): success. Seven artifacts processed; no Canvas drift or per-artifact failures.
- Deployment state commit: `f1107ad` on canvas-state. IDs were read from this state, not invented or written manually.
- Generated Common Curriculum commit: `73eb41f2742f95b0892e8efa82d17c9c9e4432d1`; GitHub Pages build completed successfully.
- [Canvas module 2079](https://cti-courses.instructure.com/courses/180/modules/2079) is published, nonsequential, without prerequisites or unlock date.
- [Course homepage](https://profsathya.github.io/Common-Curriculum/deanza/course1/home.html) has the V2 section open and unmuted, with all six learner links. Existing Canvas front page 3467 (`home`) already embeds this hosted homepage through external tool 203; no replacement front page was needed.

## Live readback

| Position | Item | Canvas ID | Points |
| --- | --- | --- | --- |
| 2 | Tracked Introduction | Page 3621 / module item 17969 | n/a |
| 3 | Start your list and get underneath it | Assignment 7144 / module item 17971 | 0 |
| 4 | Things you stopped noticing | Assignment 7147 / module item 17974 | 0 |
| 5 | Things somebody handed you | Assignment 7146 / module item 17973 | 0 |
| 6 | Sprint 1 Concept check | Assignment 7143 / module item 17970 | 5 |
| 7 | Test and commit | Assignment 7145 / module item 17972 | 35 |

All five assignments are published, allow online text entry, have no due/unlock/lock dates, and have `must_submit` completion markers. The first half totals 40 points. The module header is local metadata resolving the existing module; it does not create an extra learner page or subheader.

Created dedicated Own Your Progress group **429** and assigned the three zero-point OYP assignments to it. Each has `omit_from_final_grade: true`; the 5- and 35-point assignments remain included. These narrowly scoped administrative updates used CanvasClient after the protected content publish because the existing frontmatter publisher does not configure these fields. Course grading remains unweighted and sequential access remains off. API fields were checked against the official [assignment documentation](https://developerdocs.instructure.com/services/canvas/resources/assignments) and [assignment-group documentation](https://developerdocs.instructure.com/services/canvas/resources/assignment_groups).

Creation order required a final module-item position adjustment to match the authored sequence. Canvas also published the preexisting untracked Introduction when the module was opened. Verification detected this; its prior unpublished state was restored without changing its body or identity. It remains at module item **17967**, after the new sequence at position 8. The initial duplicate-preservation assertion was too strict about its shifted position; final readback checks preserved identity, title, content, and unpublished state. Both Introductions remain present.

Working Draft module **2078**, its six items, and all tracked content fingerprints remained unchanged. Final readback also confirmed all new tracked content matches deployment-state fingerprints. No state file, manifest, schema, or runtime API code was edited for the administrative setup.

## Verification and limits

Full local schema validation and 204 unit tests passed before the push; GitHub's validation job also passed. Public-site browser verification confirmed V2 is open/unmuted, all six content URLs return HTTP 200, all six Canvas destinations are populated, the original Introduction URL is retained, and the mobile diagram works. The rendered live module was visually inspected. Earlier local browser QA covers response saving, copying, six choice explanations, tables, and mobile layout; this release did not change participant prose or controls.

An initial front-page lookup used the wrong `/pages/front_page` endpoint and returned 404. The correct `/front_page` endpoint confirmed the published existing homepage and its hosted destination. No production submissions or grades were created as tests.

Private evidence: `.source-intake/sprint-one-v4-20260910/release-live-after.json`, `release-canvas-home.json`, `qa/live-navigation-results.json`, `qa/release-workflow.log`, and screenshot files. Final source fingerprints are in `authoring/20260910T185450Z-sprint-1-v2-release.md`; the earlier draft record retains the editorial assessment and provenance decisions.

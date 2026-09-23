# Four Canvas walkthroughs: unpublished staging check

## Protected deployment

Reviewed source commit `8007f92c036ba04b0ed47e66872c56f7496e68df` on `codex/four-canvas-walkthroughs`, [PR #113](https://github.com/profsathya/applying-ai-at-work/pull/113). The four exact-file [Publish Canvas workflow](https://github.com/profsathya/applying-ai-at-work/actions/workflows/publish-canvas.yml) runs succeeded, in order: [Stakeholder Map](https://github.com/profsathya/applying-ai-at-work/actions/runs/35926434058), [Stakeholder Conversation](https://github.com/profsathya/applying-ai-at-work/actions/runs/35926608252), [Name the Gap](https://github.com/profsathya/applying-ai-at-work/actions/runs/35926830123), [Learning Plan](https://github.com/profsathya/applying-ai-at-work/actions/runs/35927041251). The four [Common Curriculum Pages deployments](https://github.com/profsathya/Common-Curriculum/actions) also succeeded, latest run [35927166013](https://github.com/profsathya/Common-Curriculum/actions/runs/35927166013). Production course AI service deploy `6ab44ce260d28179906c9a1e` was live before staging.

Authoritative `canvas-state` commit `3ece950` contains all four new IDs, module items, source commit, content hashes, and hosted hashes. Each public hosted page returned HTTP 200; served SHA-256 matched its state `hosted_hash`. The two previous Sprint 3 unpublished Canvas alternatives had been deleted before this request, so the protected workflow created fresh assignments 7165 and 7166 from their existing reviewed local Markdown.

## Canvas result

All four originals remain **published** and unchanged. Every replacement is **unpublished**, directly after its source in the same module. The original description hashes match the intake snapshots; source and replacement match on points, points grading, file upload, and no due/availability dates. Every pair has no rubric, overrides, or submitted work in the final readback.

| Original activity | Original Canvas link and position | Staged Canvas link and position | Points |
| --- | --- | --- | ---: |
| Stakeholder Map | [7159](https://cti-courses.instructure.com/courses/180/assignments/7159) at 4 | [7165](https://cti-courses.instructure.com/courses/180/assignments/7165) at 5 | 35 |
| Stakeholder Conversation | [7158](https://cti-courses.instructure.com/courses/180/assignments/7158) at 7 | [7166](https://cti-courses.instructure.com/courses/180/assignments/7166) at 8 | 50 |
| Name the Gap | [7134](https://cti-courses.instructure.com/courses/180/assignments/7134) at 3 | [7167](https://cti-courses.instructure.com/courses/180/assignments/7167) at 4 | 35 |
| Learning Plan and Updated Problem Frame | [7160](https://cti-courses.instructure.com/courses/180/assignments/7160) at 6 | [7168](https://cti-courses.instructure.com/courses/180/assignments/7168) at 7 | 50 |

Module 2081 contains the first two pairs, and module 2082 contains the second two. The final Canvas API comparison used list order as well as each module item's position, so deleted-item gaps in earlier Sprint 3 position numbers did not masquerade as adjacency.

## Live interaction and fidelity

In authenticated Chrome, each unpublished Canvas assignment loaded its actual hosted iframe. One synthetic writable row per item was entered, its actual **Get AI feedback** button was pressed, and feedback appeared below the selected table. Each response addressed that row, offered a concrete revision question, did not grade or invent workplace evidence, and left the answer intact. The synthetic answer fields were cleared afterward; no Canvas submission was created. A preexisting browser draft in Stakeholder Map was preserved.

Each iframe's actual **Copy work** button reported a table copy, and the browser clipboard contained both `text/html` and `text/plain`. The two Sprint 4 pages explicitly directed the participant to paste into the continuing Learning Plan document, export PDF, and upload the PDF; their Word download is labeled a backup. Earlier, native Command-V into four signed-in Google Docs and DOCX readback had preserved 11/11, 6/6, 4/4, and 8/8 tables respectively, all source cells, blanks, synthetic multiline answers, and table order. Direct live AI checks covered every configured checkpoint: 8/8, 3/3, 5/5, and 7/7. The local browser preview checked the selectable-table fallback when clipboard access was denied. This is technical and editorial QA, not human participant testing.

## Private evidence fingerprints

- `.source-intake/four-walkthroughs-20260923/canvas-final-verification.json` SHA-256 `b7612a9318621b3f99fb16fde0ad737bc96075aee4b246806f0a4054fa442c4d`
- `.source-intake/four-walkthroughs-20260923/assessment-final.json` SHA-256 `9e8ab48ca640872f29a778822d3e71a571a20700d4cbadaf4b599976311b0cbd`
- `.source-intake/four-walkthroughs-20260923/hosted-final.json` SHA-256 `c05fdaee7ded7a0cbbfe87f46ea7b69acc0807106b9af6e8445d48d429253cb4`
- `.source-intake/four-walkthroughs-20260923/canvas-browser-live.json` SHA-256 `3aa28f023710ba9f619b693b0c6c385646eacbcda9c6f11a20ab4a67d3ddf251`
- `.source-intake/four-walkthroughs-20260923/paste-comparison.json` SHA-256 `2c22f4b77801aab28afa33eef851d41b50b5d4d89aa3426fc96b5cc3185a34dd`

The new items remain unpublished. Releasing them to participants would require a separate approval and visibility switch for each original/replacement pair.

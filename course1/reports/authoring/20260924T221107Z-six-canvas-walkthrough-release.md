# Course 180 Canvas Walkthrough review and release

## Scope and status

The agent reviewed and released the six existing Canvas Walkthrough replacements in Sprints 2–4 under the user's explicit release plan. The editorial assessment below is the agent's. The user approved implementing the release plan; separate human review of every final sentence was not requested or observed. No participant testing was observed.

| Sprint | Original assignment | Replacement assignment | Final Test Student receipt |
| --- | ---: | ---: | --- |
| 2, Dig into your assumptions | 7169 | 7178 | One Word file |
| 2, What solutions already exist | 7176 | 7179 | One Word file |
| 3, Stakeholder Map | 7159 | 7165 | One Word file |
| 3, Stakeholder Conversation | 7158 | 7166 | Report Word file, updated map Word file, Part 1 AI response JSON |
| 4, Name the Gap | 7134 | 7167 | Week 7 Word file |
| 4, Learning Plan and Updated Problem Frame | 7160 | 7168 | Separate Week 7 and Week 8 Word files |

Originals remain in Canvas and unpublished; all replacements are published. Assignment IDs, artifact IDs, hosted paths, and module item positions were preserved. The paired positions are 2/3 and 6/7 in module 2084, 4/5 and 7/8 in module 2081, and 3/4 and 6/7 in module 2082. The last item of each pair is the visible replacement. Pre-release readback found no participant submissions on any original; assignment 7166's one existing submission was Test Student user 5815.

## Sources and editorial decisions

The reviewed inputs were the user's approved plan, the six existing replacement Markdown files and neighboring original assignments, their source-provenance sidecars, the prior Sprint 3–4 walkthrough authoring record, live Canvas assignment settings and descriptions, and the shared renderer, release preflight, hosted homepage builder, and walkthrough skill. The source documents and original learning sequence were treated as read-only design inputs. The four source-derived table sets remain present, including 11 Stakeholder Map tables, six Stakeholder Conversation tables, four Name the Gap tables, and eight Week 8 Learning Plan tables. The Sprint 2 assumption page has seven table blocks and What solutions already exist has its source grid.

Every writable walkthrough now presents **Download as Word document** as its sole finish action, followed by **Start Assignment**, attach the named Word file or files, and **Submit Assignment**. The shared headings and interface text use **Canvas Walkthrough**. The Sprint 2 pair remains free of AI feedback in accordance with its source directions. Week 8 keeps Part A/C1 in the separate Week 7 file while the new Week 8 file holds Part B/C2. Stakeholder Conversation still requires its updated map and AI response JSON. The optional feedback pages continue to require participants to write first, identify uncertainty, and avoid sending confidential details. No new rubric, deadline, point value, or simulated stakeholder work was added.

The shared renderer and walkthrough skill now make the Word upload route the repeatable default for future walkthroughs. The release preflight permits the two ungraded Sprint 2 text-entry-to-file-upload conversions only after checking for source submissions; it accepts the already-published 7166 replacement and preserves both sides' initial publication flags for rollback. The homepage builder resolves curated links across sprint storage folders. The homepage-maintainer subagent updated the six curated links to the replacement module items.

No unresolved editorial issue was found in the six walkthroughs. The local Sprint 2 preview runner still reports an unrelated pre-existing skipped heading level on the Sprint 2 Concept check; all four walkthroughs in that sprint passed their individual browser checks.

## Validation and live checks

- `.venv/bin/python canvas_sync/schema.py --all`: pass. `.venv/bin/python canvas_sync/link_audit.py --all`: 184 artifacts, 60 links, zero errors. `CANVAS_API_URL='' CANVAS_API_TOKEN='' .venv/bin/python -m unittest discover`: 308 tests, one skipped, pass. `npm test --prefix services/course-ai`: ten tests pass. The unmasked first unit-test run picked up the repository's production `.env` and failed an offline fixture's instance guard; the environment-isolated rerun passed.
- Local hosted rendering and module preview checked every walkthrough's source grid, response cells, draft save/reload, Word export, desktop/mobile layout, and feedback placement. Sprint 17 had zero errors on its two walkthroughs; Sprint 16 had zero errors on its four walkthroughs. All six synthetic DOCX exports opened with `python-docx` and contained the test response. Table counts were 7, 1, 11, 6, 4, and 8 in the row order above.
- Real production AI requests passed all 23 configured checkpoints across the four feedback-enabled activities. Agent-reviewed replies stayed on the selected response, raised a relevant observation or revision question, and did not grade or invent workplace evidence. In the live Canvas embed, a Name the Gap feedback button activated after a synthetic response and displayed a relevant question; the test response was then cleared. The two Sprint 2 pages exposed zero AI controls.
- In the Codex in-app browser, each of the six live pages showed one Word button, file-upload submission mode, and the named attachments in its directions. A synthetic answer on each page survived a refresh, then was cleared. Clicking the live Word button on all six produced the "Word document downloaded" status; the exported DOCX bytes and tables were checked in the local browser preview. Fresh deployed hosted URLs showed the common intro and finish headings on all six. The Codex browser cache retained older embedded headings on 7165 and 7166 even after ordinary reload and reopening the assignment; cache-busted hosted URLs returned the deployed version. GitHub Pages served a 600-second cache lifetime. The browser's requested mobile viewport override did not change its measured 1280px viewport, so mobile-width evidence comes from the local preview rather than a successful in-app mobile resize.
- Protected GitHub publish runs `36064541290` (staging) and `36064909919` (release) succeeded. Content commits: `1953cac` and `03fcb52` on `main`; Canvas state commit: `38eb9ed` for the release. Common Curriculum hosted commit `b18877e` completed its Pages build. Live API readback confirmed all six originals unpublished, all six replacements published with `online_upload`, adjacent module positions unchanged, and no legacy external-site footer link in the Canvas assignment shells. The fresh hosted homepage linked to module items 18011, 18012, 17997, 17998, 17999, and 18000; Test Student module-item readback omitted all six originals and included all six replacements. A direct Student View visit to original 7169 returned Access Denied.
- As Test Student 5815, Canvas received the actual exported synthetic files for all six activities, including three attachments on 7166 and two distinct Word files on 7168. Student View showed “Submitted!”, “Submission Details”, and the correct attachment names on every replacement. The Codex in-app browser did not expose its native file chooser to automation despite using the documented chooser flow, so file upload and submission used Canvas's documented API with Test Student masquerading; the completed receipts were checked in the Student View UI. Reusing the Week 7 export on 7168 made Canvas rename that attachment `learning-plan-week-7-1.docx`; its size matched the original file. Reset Student replaced user 5815 with a fresh Test Student 5816; the old test submissions then returned 404. Instructor view was restored and all six assignment tabs were left open.

## Skills consulted

- `.agents/skills/create-canvas-walkthrough-assignments/SKILL.md` SHA-256 `380c99712205951c5c826aa7f0ee4c45853c032b11cb0e23dbaf0fce7a857917`
- `.agents/skills/maintain-homepage/SKILL.md` SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` (homepage-maintainer subagent)
- `.agents/skills/sync/SKILL.md` SHA-256 `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b`
- `.agents/skills/reviewing-course-text/references/review-record.md` SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`
- `.agents/skills/reviewing-course-text/SKILL.md` local revision 6; `.agents/skills/writing-to-teach/SKILL.md` revision 5; `.agents/skills/writing-learning-goals/SKILL.md` revision 2; `.agents/skills/writing-assignments/SKILL.md` revision 4.

## Reviewed output fingerprints

| Repository path | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-16/dig-into-your-assumptions-walk-through.md` | `bd1795af9ddecba9af3a3ca4f8e2317ef6095c5f0e74171639e90aa0ef8e0a03` |
| `course1/sprints/sprint-16/what-solutions-already-exist-walk-through.md` | `cb214baa36966ee37c2b1b4bd7af70376559ad6f0a42188843165b66a6bea45a` |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` | `1c2a75c0bfcc348e59b7a56cdd25e1301ca62c8a07ca75630c04ad0c4947d5e6` |
| `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.md` | `1b07c5425ffecb269215fa22f980819102f0efd086e1b2a9654208ca846e16b3` |
| `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.md` | `0b423084b28125466fc1e7154a458ef4eebef134fd023fc63c7ba1e139c6ce70` |
| `course1/sprints/sprint-17/learning-plan-and-updated-problem-frame-canvas-walkthrough.md` | `dece19cd6c5001abe3575063abc626228eec8c0d3fccb5adb101b0b5ca702a2f` |
| `course1/homepage.yaml` | `24e020442a2753e3b826c2f97fb5c3424583c7f102175fa9a4a3e6f8f81c2de8` |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.sources.json` | `965f2becf877a5933593176a68c116452fd7410218409707ff3ea57595a18056` |
| `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.sources.json` | `2ad1daae440d4eb29d349c0b6ebc23d743165bc9cf9267b2ff82ecc9691356a9` |
| `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.sources.json` | `38163a659045186df4103a8d32890d192fec8a9fae569292e753b0e915152f52` |
| `course1/sprints/sprint-17/learning-plan-and-updated-problem-frame-canvas-walkthrough.sources.json` | `9ec8fb9de69641e9caf69ebb56da2d8928616006bd8edcad5c582ca2aa3a4e05` |
| `canvas_sync/walkthrough.py` | `59a5b3886be23299829e9cef397572380dce7471e944e7ce90e3a5eeec73ae9b` |
| `canvas_sync/walkthrough_release.py` | `5e2dddfb1eed1043fcc45ea59e80681a5b3df5fbf4b73440ae1cc6b6533bfcc5` |
| `canvas_sync/hosted_html.py` | `ac651bdfdf6e0eb7843e206d74f5708e37ca085e2893ae56ed8583741b72754d` |
| `canvas_sync/module_preview_walkthrough.cjs` | `bb7f46e0727d10e9e8b516d03aab6a4eb576696815cc951fc0c5b41611f5df56` |

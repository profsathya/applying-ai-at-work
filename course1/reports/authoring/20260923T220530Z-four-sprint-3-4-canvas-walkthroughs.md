# Four Sprint 3 and 4 Canvas walkthroughs: authoring review

## Scope and status

Course 180, four instructor-selected alternatives. Agent editorial assessment completed before unpublished Canvas staging. The user's current request authorizes staging these exact four drafts, not participant release. Human approval of the resulting prose was not requested or observed. The two earlier Stakeholder Map and Stakeholder Conversation Canvas assignments were absent from live Canvas when inspected, although their reviewed local Markdown remained; these will be recreated from the existing local files. The two Sprint 4 walkthroughs are new local artifacts.

| Live original | New artifact | Source document | Assessment retained |
| --- | --- | --- | --- |
| Stakeholder Map, assignment 7159, module 2081 item 17991 | `course1-stakeholder-map-canvas-walkthrough` | Stakeholder Map template `1Z0Sg2_2lnQNiryTOpzerdhIovuE4a4-AGivkxR2bRP4` | 35 points, file upload |
| Stakeholder Conversation, 7158, module 2081 item 17990 | `course1-stakeholder-conversation-canvas-walkthrough` | Stakeholder Validation Report `1MUOWS7Y8nMMFu5wWP3_aK2-eGQvvEBUr3yV3d36_Ekw` | 50 points, file upload |
| Name the Gap, 7134, module 2082 item 17954 | `course1-name-the-gap-canvas-walkthrough` | Learning Plan template `1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA`, Part A and C1 | 35 points, PDF file upload |
| Learning Plan and Updated Problem Frame, 7160, module 2082 item 17992 | `course1-learning-plan-and-updated-problem-frame-canvas-walkthrough` | Same template, Part B and C2 | 50 points, PDF file upload |

Each new artifact is marked `publish: false` and anchored by `walkthrough_after` to the live original. Final positions must be verified from Canvas after the protected workflow. The original descriptions and assignment settings matched fresh baseline snapshots before staging, and no new item with one of these titles was present. All four originals were published and had no rubric, dates, overrides, or submissions at intake.

## Sources, decisions, and editorial findings

Read each live Canvas assignment and hosted instructions, relevant neighboring module items, the three supplied Google Docs through Document Intake, source packets in `.source-intake/four-walkthroughs-20260923/`, existing local Sprint 3 walkthroughs and their prior authoring records, and the original Sprint 4 local artifacts. The source Google Docs were read in base text view; unreturned suggestions were not adopted. Source documents and originals were not edited.

The converted practice remains real stakeholder mapping, a real conversation and report, a participant-authored inventory of consequential unknowns, and a plan tied to an updated seven-part Problem Frame. The evidence route stays as each original requires. Name the Gap's original no-AI direction is expressly adapted under this request for live AI feedback: participants first make their own list, then may request narrow optional critique, with a complete no-AI path. Its four-row A2 grid and later-use Part D grid remain intact. The week 8 walkthrough continues the same Learning Plan file, retains Part A and C1, and submits a complete PDF with Part B and C2. The renderer was extended to state this PDF path clearly and keep Word as a backup. No new points, rubrics, dates, or stakeholder role-play were added.

Table fidelity comparisons: Stakeholder Map 11/11 source tables; Stakeholder Conversation 6/6; Name the Gap 3/3 source-derived tables; Learning Plan 4/4 source-derived tables. Other participant response tables are instructional adaptations of the seven-part frame and plan, identified as such. Source cell text, grid dimensions, blank cells, selected response cells, and read-only states passed comparison. The user-requested tone and task sequence were retained; the new prose uses concise directions and keeps the document sections tied to the activity that assesses them. No unresolved editorial issue was found in this scope. No human participant testing was claimed.

`course1/homepage.yaml` was checked under `maintain-homepage` and validated. Because these are unpublished alternatives, its participant-facing links and curated copy were left as they were; none of the four draft slugs was added to the homepage.

## Observed validation and live evidence

- `.venv/bin/python canvas_sync/schema.py --all`: PASS. `.venv/bin/python canvas_sync/schema.py --homepage course1/homepage.yaml`: PASS. `.venv/bin/python canvas_sync/link_audit.py --all`: 170 artifacts, 60 links, zero errors. `CANVAS_API_URL=https://example.instructure.com CANVAS_API_TOKEN=test-only .venv/bin/python -m unittest discover`: 295 tests, OK, one skipped. The first local unit run had the repository's production `.env` loaded into fixture tests and failed the instance guard; rerunning with the test URL passed. `npm test --prefix services/course-ai`: 10/10 PASS. `git diff --check`: PASS.
- `preview_module.py --check-browser` results in the private `sprint16-after` and `sprint17-final-preview` directories: two walkthroughs per preview, zero browser errors. The preview runner reported `partial` solely because it intentionally skips the live provider. It checked headings, accessible controls, response save/reload, feedback placement with labeled local samples, source tables, rich clipboard, Word export, clipboard-denial selectable fallback, and desktop/mobile overflow. Agent visual inspection found no clipping in sampled desktop and mobile screens; this was not participant testing.
- Native browser paste: clicked each rendered **Copy work** button, used Command-V in a signed-in blank Google Doc, observed pasted table cells, exported the saved Docs, and compared every table in order. Stakeholder Map 11 tables/138 cells, Stakeholder Conversation 6/44, Name the Gap 4/62, Learning Plan 8/105, all with zero errors. Synthetic answers, multiline answers, blanks, headings, and original source text were retained. Only outer cell whitespace and NBSP padding were normalized. Scratch Doc URLs and export hashes are in private `paste-comparison.json`.
- Production AI service deploy `6ab44ce260d28179906c9a1e` is live. `walkthrough_feedback_check.py --live` used synthetic responses for every enabled checkpoint: Map 8/8, Conversation 3/3, Name the Gap 5/5, Learning Plan 7/7 HTTP 200 and checker PASS. Detailed outputs are in private `*-feedback-release.json`, except Name the Gap's final run in `name-gap-feedback-final2.json`. Agent reviewed the responses for a relevant observation and revision question, no grade or invented workplace evidence, and no demands for unseen rows. Initial incomplete responses and several overly broad prompts were corrected in the service and registry, redeployed, and retested before staging. Provider responses are nondeterministic. A real button in each production hosted page or Canvas iframe remains to be checked after GitOps staging.

## Skills consulted

- `.agents/skills/create-canvas-walkthrough-assignments/SKILL.md` SHA-256 `85a26af647be74e7cca91e93f755784dfb380acac69c41cf19caeb37c1c8aeed`
- `.agents/skills/create-canvas-walkthrough-assignments/references/live-checks.md` SHA-256 `b3390a37deb2e5d39fd91c9783c58f7678b57e4909accf91503d09864041da6e`
- `.agents/skills/maintain-homepage/SKILL.md` SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`
- `.agents/skills/sync/SKILL.md` SHA-256 `2dca43a30dc30d7b87e02c22f208635039c459f7c624556618ed57dc949fca8b`
- `.agents/skills/reviewing-course-text/references/review-record.md` SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`
- `.agents/skills/reviewing-course-text/SKILL.md` local revision 6; `.agents/skills/writing-to-teach/SKILL.md` revision 5; `.agents/skills/writing-learning-goals/SKILL.md` revision 2; `.agents/skills/writing-assignments/SKILL.md` revision 4. These guided the substantive editorial review; the parent performed the review directly.

## Reviewed output fingerprints

| Repository path | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md` | `7b169fcae73ea6d60db233d44e7ba1e82438c12ffa5abef99184fc768f27da70` |
| `course1/sprints/sprint-16/stakeholder-conversation-canvas-walkthrough.md` | `f3729ae675349c505589114766dcaa58471ce2a752bc5a200e0f909311c44caf` |
| `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.md` | `203fd31c8acefaa87fa1e9b6a08fb6860690ec5c954aa3756bc5c755447699ae` |
| `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.sources.json` | `55fcd3a48f5bb0715fa098896600e01b7f359db06c238dcd5397d0cb37f6c26c` |
| `course1/sprints/sprint-17/learning-plan-and-updated-problem-frame-canvas-walkthrough.md` | `bbb9a2d0a5f6cb86ce3b40aaa3532425c2ed47b6eb3cdbdb69248daa1dc12724` |
| `course1/sprints/sprint-17/learning-plan-and-updated-problem-frame-canvas-walkthrough.sources.json` | `6319454986a11852ffc6208926c5c78ba726251474d465d6797dd4a66ff5a1aa` |
| `canvas_sync/walkthrough.py` | `a3a6213db1678428c00fecbc0cc4c0fcf0724512bdd94d6cbba74f450c849997` |
| `canvas_sync/assets/guided-walkthrough.js` | `7c920a8a9b3c9fde1992bf5fcc5d8466380af2b17f6dd5c56916cae92712f7f8` |
| `canvas_sync/module_preview_walkthrough.cjs` | `eb78bdb6881d6016959b7c66387eb4a71def205b5f01b9b552a511d7e1777f41` |
| `schema/frontmatter.schema.json` | `ba49627df50aea9974fe324ae73008bea4762bf8e2ba625fdda4a4159d6f267e` |
| `services/course-ai/netlify/functions/walkthrough-feedback.mts` | `06769f7f956834e96f42ba719967819889fb9b3d619ed4d14a08003044bcef3c` |
| `services/course-ai/netlify/functions/walkthrough-guidance.json` | `caf33e104555399b8ff57c923a6d0c8532e484f9e650b4accd727be45e9e1f58` |
| `services/course-ai/tests/walkthrough-feedback.test.mjs` | `0f3cab07e6c2e73b4d29326b2be7718d3df0199655a349f351828aae4dbf3ad8` |

# Sprint 0 publication and source alignment

## Result

Source revision `153dbeb06a740a2a41b52bf4482ae2cd0e9eb11a` was published by [Publish Canvas run 35036913818](https://github.com/profsathya/applying-ai-at-work/actions/runs/35036913818). Both validation and publication jobs succeeded. Course 180 retains Sprint 0 module **2075** and its six participant-facing items. The user explicitly authorized this publication and sequential completion.

## What was prepared

| Google Doc tab | Published content and adaptation |
| --- | --- |
| Overview | Module overview and homepage goals describe the actual orientation route, weekly workload, introduction, and help. |
| Start Here | Five pages and one discussion; concise orientation goals; clear route and first action. |
| Welcome | Real-life investigation, human context and judgment, the integrated problem document, goals, and evolving thinking. Missing bio/video material was omitted. A new illustration in the approved art style replaces the reused Sprint 1 visual. |
| How this course works | Recommended ten-week schedule, two weeks per sprint, 4-6 hours weekly. A mobile-readable five-part roadmap separates cumulative course evidence from Canvas submissions. Available Sprint 1 work is distinguished from planned later activities. |
| Your First Week | One checklist for reading, scheduling work, finding Canvas Inbox, and introducing yourself. Discussion prompts appear only in the discussion. The unavailable-video dependency is removed. |
| Introduction Post | Five prompts covering identity, career context or aspirations, motivation, learning interests, and joy. Comfortable disclosure and optional replies remain explicit. Reading typography and blue accents now align with the other pages; posting remains native to Canvas. |
| Help and Resources | Working Inbox and submission guidance, text-entry copying versus JSON upload where relevant, tool setup at the relevant activity, and the no-AI boundary for available Sprint 1 work. |

The original source remains [the seven-tab Google Doc](https://docs.google.com/document/d/1LeI0UpHqaWjEViZtoOPl0Ay660vwwBsuyHor6gnYoVA/edit). A fresh connector read before publishing matched the preserved structured capture exactly. Every tab is referenced by adjacent source-evidence files. Source concepts and learning intent are preserved through authorized instructional adaptation, not represented as a verbatim transcription.

The most consequential adaptations are current course names and working links, removal of missing-material placeholders, concise explanations, the recommended pacing language, and explicit boundaries around activities that are not yet available. Office hours and response-time promises were not invented. Reviewer emphasis on goals and evolving thinking remains in the course explanation. Source-supported Superagency, Human Value, Symbiotic Thinking, 3Cs, and UMPIRE are retained in plain-language explanations or reference material.

### Source review limits

The connector exposes the document but incompletely covers review metadata: its refreshed comments call again returned an empty list. Earlier same-session browser review found 17 open comments and one remaining suggestion that inserts blank lines only. That browser evidence supplements the raw capture. This is not a complete revision-history archive. Raw captures remain private; the repository contains Markdown, provenance sidecars, illustration provenance, and authoring records.

## Completion sequence

| Order | Item | Canvas item ID | Completion requirement |
| --- | --- | --- | --- |
| 1 | Start Here | 17937 | View |
| 2 | Welcome | 17938 | View |
| 3 | How This Course Works | 17935 | View |
| 4 | Your First Week | 17939 | View |
| 5 | Introduction Post | 17936 | Contribute |
| 6 | Help and Resources | 17934 | View |

The live module settings UI confirms **Complete all** and **Students must move through requirements in sequential order** are selected. Five page requirements are View; the discussion is Contribute. The introduction is zero points, complete/incomplete, excluded from the final grade. It keeps discussion 1533 and assignment 7121. No new due dates or module prerequisites were added.

The first-week help-location task now points to Canvas Inbox; detailed Help follows the introduction. This avoids making the early checklist depend on a later locked page. Viewing completion records opening the Canvas page, not comprehension or time spent reading. Existing completed progress was not reset.

## Validation

- Full offline repository schema and all adjacent source evidence: passed.
- Full unittest discovery: **235 tests passed**.
- Final six-item browser preview: passed at desktop 1280px, mobile 390px, and enlarged base text at 320px; headings, image loading and text alternatives, control names, and overflow checked.
- Fresh preflight: all 12 mapped Sprint 0 and Sprint 1 fingerprints matched deployment state; no target drift.
- Dry run: exactly seven Sprint 0 artifacts, including the module header.
- Protected publication: success. The publisher applies sequential progression from module-header metadata and requires an affirmative Canvas readback before recording success.

Earlier detailed records are in `course1/reports/authoring/20260915T231006Z-sprint-0-revision.md`, `20260915T231534Z-sprint-0-visual-adjustments.md`, `20260915T231957Z-introduction-post-reading-style.md`, and `20260915-sprint-0-publication-preflight.md`. Their local-only status describes their earlier review times; this report records the subsequent authorized publication.

## Live verification

- [GitHub Pages deployment 35036987671](https://github.com/profsathya/Common-Curriculum/actions/runs/35036987671): success.
- Canvas-state commit: `1ff4e14b80075733d847a3557aad1bf09bcd5462`.
- Hosted commit: `e38ef80ddc51dc3641def04bfd315f75a9a5f22d`.
- Read-only API verification confirms module 2075 is published with sequential progression true and all requirements. Original item IDs, order, publication states, and introduction grading are preserved.
- All six Sprint 0 public HTML files return HTTP 200 and exactly match the new deployment-state hashes. The Welcome image returns HTTP 200 with its expected content-addressed hash. Homepage bytes match the hosted commit.
- Browser verification confirms the saved sequential settings, native discussion prompts and Reply control, consistent reading layout/blue accents, and homepage Open orientation link to module 2075. The new Welcome illustration and copy were visually inspected on the deployed hosted page with a fresh cache key.
- A browser session opened during deployment continued displaying cached old Welcome iframe content after ordinary reload. Direct HTTP readback of both the plain and `?context=canvas` URLs returns the new page, and the fresh-cache-key browser view shows it correctly. This was a browser-cache observation, not an unresolved deployment mismatch.
- Sprint 1 Canvas identities, fingerprints, settings, order, and requirements are unchanged. Three generated Sprint 1 pages gained the shared native-discussion CSS rules; content outside style blocks is unchanged in all six. Those three older deployment-state hosted hashes remain stale for the CSS-only change. No manual state edits were made.

Detailed private evidence is in `.source-intake/sprint-0-publish/postflight/live-verification.json`, `committed-hosted-verification.json`, `canvas-state-production.json`, and `summary.md`. Source freshness evidence is in `source-refresh-verification.json` alongside that directory. The final local comparison remains in `.source-intake/sprint-0-revision-20260915T225941Z/publish-final/comparison.html`.

## Assessment and boundaries

The delivered revision adheres to the reviewed document's instructional intent and the explicitly approved adaptation plan. It preserves all seven tab mappings, course-level concepts, personal disclosure choices, and the sole orientation submission while correcting outdated operational material. The latest requested visual changes and sequential completion setting are now published.

No new discussion post was submitted and no participant progress was reset. Sequential configuration was checked in both the API and Canvas settings; a fresh participant's full unlock sequence through a posted introduction was not exercised. Responsive and enlarged-text checks were performed against the final local render, while live browser checks covered the settings, discussion, homepage, and hosted Welcome. No claim of learning effectiveness or accessibility certification is made. Unrelated legacy course drift and unpublished duplicate modules were outside this Sprint 0 publication scope.

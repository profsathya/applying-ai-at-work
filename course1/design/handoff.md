---
purpose: Everything needed to continue the Sprint 1 V2 rebuild in a new conversation
last_updated: 2026-09-14
read_first: true
---

# Handoff

New chat? Read this, then `problem-spine.md`, then `sprint-1-decisions.md` from the session of
14 September onward; those entries supersede anything above them that conflicts. The live
first half is in `course1/sprints/sprint-12/` but is about to be replaced: the whole sprint is
redrafted on a new sequence in `course1/design/sprint-1-working-draft-v5.md` (now v5.1).

---

## What this is

A V2 rebuild of Sprint 1 of course1, *Reframing Problems with AI*, for a community college
cohort of about 32 people, cap 40, mixed employment, starting in roughly three weeks. The
course is asynchronous and self-paced, delivered in Canvas, and will be run by an instructor
who did not write any of it.

The whole course was originally AI-generated from minimal prompting. Leslie and Melisa are
rebuilding it because it does not work as written. Everything is on the table. Leslie owns
Sprints 1 and 2; Melisa owns 3 and 4 and can adjust them to fit.

Leslie makes the judgment calls and the team reacts. Clare is the instructor and final
reviewer. Jeremy (back 8 September) owns the build pipeline: document intake, the
`guided_assignment` delivery mode, Canvas publication, the AI proxy, and the review of
Sprints 0, 3, and 4.

**The plan as of 11 September.** Solid whole course by 15 September; six days of edits with
Clare; share with the instructor 21 September; later move to the De Anza Canvas. Leslie:
Sprint 1 and Sprint 2. Jeremy: first half review, then Sprints 0, 3, 4. Melisa: run the
first half as a participant. Rubrics and points decided soon. Sprint 5 has no owner.

## Where things live

```
course1/design/sprint-1-working-draft-v5.md       THE LIVE DRAFT (v5.1): the whole sprint, ten items,
                                                   on the 14 September resequence. Leslie reviewing.
course1/design/sprint-1-resequence-outline.md     why the sequence changed (14 September)
course1/design/sprint-2-outline.md                 Sprint 2, outline; must receive the claims table
course1/design/dojo-setup-note.md                  the course-wide Dojo tool, for Jeremy (15 September)
course1/design/dojo-module-problem-frame.md        Sprint 1 Dojo Lab as a Dojo module, v0.3, PARKED
course1/design/problem-spine.md                    course-level design
course1/design/sprint-1-decisions.md               every judgment call, dated
course1/design/handoff.md                          this file
course1/sprints/sprint-12/                         Sprint 1 first half as cut 11 September, published to
                                                   Canvas module 2079, locked by .sources.json; to be
                                                   replaced by the cut of v5
course1/sprints/sprint-13/                         Jeremy's AI feedback demo (14 September)
course1/design/sprint-1-half-two-working-draft-v1.md   v1.1, superseded by v5
course1/design/sprint-1-half-two-outline.md        superseded by the resequence outline
course1/design/sprint-1-half-one-working-draft-v4.md   FROZEN at v4.2; record only
course1/design/sprint-1-half-one-working-draft-v3.md   superseded
```

**The rule (Leslie, 12 September): once content is cut into artifacts, the artifact is the
source of truth and the design draft is frozen.** The sprint-12 pages are locked by Jeremy's
`.sources.json` sidecars: validation rejects any direct body edit ("edit the build map and
rebuild"). That lock is moot for the first half now, because v5 replaces those pages with a
new source rather than editing them.

`sprint-10` no longer exists. `sprint-11` (Working Draft) is retired under `course1/retired/`.

## The design, in one paragraph

Sprint 1 ends with one chosen problem plus an honest frame, version two, with every claim
marked confirmed or unverified. The sequence (Leslie's own run, 14 September): brainstorm a
wide list by category; get underneath three to five of them in a four-column table (the
situation, how it works now, what it costs and whom, the gap); read the seven-part problem
frame and take the concept check; write a first frame for every candidate; have AI test and
widen the frames in the Dojo Lab and choose one; submit the Goal Plan (frame version two,
what changed, which claims first); reflect. The hinge moved: commitment now comes after
framing, because the frame is how you find out which candidate to commit to. The marked
claims are what Sprint 2 works on.

## Current state

| Piece | State |
|---|---|
| Sprint 1, whole | Draft v5.1 in `course1/design/`. Leslie's first pass (module header through the Dojo Lab's Choose step) applied 14 September. Goal Plan and Reflection unreviewed by her. Two [OPEN] items are hers: the Dojo Lab's selection criteria and a live test of its two prompts |
| Sprint 1 first half, live | Jeremy's 11 September cut, published in sprint-12. Melisa is running this version. It is superseded by v5 and will be replaced at the cut |
| Sprint 1 concept check | Six questions redrafted in v5.1 against the new pages; Jeremy's call on format. Now sits after The problem frame |
| Sprint 2 | Outline written 12 September. Must receive the claims table (not a single riskiest assumption), the runner-up, and the set-aside list. Claude can build it directly as artifacts |
| Sprint 0, 3, 4 | V2 published; Jeremy reviewing. Sprint 0 owes an introduction of "own your progress" and "graded item" |
| Sprint 5 | One placeholder page. No owner |
| AI proxy | Working. CTI-owned, on Jeremy's Netlify, Anthropic direct, since 14 September (`docs/audits/2026-09-14-owned-course-ai-proxy.md`). Unblocks ai_activity reflections and the Sprint 4 AI Exchange |

## Sprint 1 on the resequence (v5.1), 100 points

| Position | Item | Kind | Points | Week |
|---|---|---|---|---|
| 1 | Module header | | | |
| 2 | Introduction | Page | | One |
| 3 | Brainstorm your list | Own your progress | 0 | One |
| 4 | Get underneath three to five | Own your progress | 0 | One |
| 5 | The problem frame | Page | | One |
| 6 | Concept check | Self-check | 5 | One |
| 7 | First frames | Graded item | 35 | One |
| 8 | Dojo Lab: test, widen, choose | Own your progress | 0 | Two |
| 9 | Goal Plan and Problem Frame | Graded item | 50 | Two |
| 10 | Sprint 1 Reflection: what changed | Graded item | 10 | Two |

Points approved by Leslie 14 September. One graded item per week, concept check as
self-check, reflection as `delivery_mode: ai_activity` like Sprints 3 and 4.

## What to do next

1. **Leslie finishes her pass on v5.1**: the Goal Plan and the Reflection, plus the
   selection criteria for the Dojo Lab's Choose step. The Dojo prompts are PARKED: the
   activity is drafted as a module for Sathya's Dojo (`dojo-module-problem-frame.md`) and
   waits on the course-wide Dojo doc (`dojo-setup-note.md`, with Jeremy) and on a second
   person's frame to test against. Do not re-tune it on Leslie's frame.
2. **The cut.** The 14 September build path: Jeremy cuts items 1 to 4 through his intake;
   items 5 to 10 can be written directly as artifacts by Claude (a guided_assignment
   artifact with several boxes and no sidecar validates PASS, tested 12 September). First
   frames carries eight boxes; the seam if the mode strains is noted on the page. Every
   cut artifact stays `publish: false`; Claude opens the PR and stops for Leslie's merge,
   since merging publishes to Canvas.
3. **Rebuild the Candidate Log template** (Google Doc, id below) to v5's sections: A
   brainstorm by category, B four-column table, C the seven-part frame repeated per
   candidate, D Goal Plan. Then link it from the Introduction and each activity.
4. **Sprint 2 prose** on `sprint-2-outline.md`, adjusted for the claims table.
5. **Points and rubrics proposal** across all five sprints, for the team decision.
6. **Collect Melisa's and Clare's run results.** Melisa is on the old first half; what
   transfers is anything about the brainstorm, the table, and the concept check.
7. **Spine and Sprint 0 updates** listed under "Owed elsewhere" at the foot of v5.1.

## Things that only exist outside the repo

- **Candidate Log template**, Google Doc in Leslie's Drive, id
  `1aTgaDgf1ugkQujJkgvo-EHXUqm9ztN1jMA5SDy3lTjI`. Built to the old first-half sequence;
  needs the rebuild above. A Word copy was sent to Leslie on 12 September.
- **The test edition** (six docx files, v4.2 text) and the live-first-half readback docx are
  with Leslie. Both are regenerable from the repo.
- **Jeremy's intake packets and build maps** are in his private `.source-intake/`.
- **Leslie's own run** (her fourteen items, three frames, and the AI exchange that
  restructured the frame) is a fixture held outside the repo and kept out of the material.

## How we work

Leslie thinks conversationally before building, wants pushback, works one thing at a time,
and wants an outline or a diagram before prose when deciding structure. She reviews in Word
or Google Docs and returns a `.docx`. Her reviews come in passes; she says where she stopped.

**Merging (Leslie's ruling, 10 September).** Claude merges design-doc PRs itself: anything
under `course1/design/`, the decisions log, this file. Since Jeremy path-filtered the
`validate` workflow, design-only PRs run no checks; merge when the PR is clean. The review of
that work happens in the document, not in the PR. Claude stops and asks before merging
anything under `course1/sprints/`, because those merges run the Canvas publish.

**Reading her reviews.** Export must be `.docx`, not markdown; Google's markdown export
drops comments and flattens suggestions. Walk the XML tree rather than using regex, because
Word nests insertions inside deletions. `word/comments.xml` holds comment threads with
anchors. **Apply every change individually and audit each one afterward**: grep each
insertion present and each deletion gone. A wholesale rewrite discards line edits silently.
This has gone wrong once. If she edits without tracking, diff against the current markdown.

Google Docs round trips introduce curly apostrophes and contractions ("you'd"), use hyphens
as dashes, and occasionally drop a space. Straighten all of it. Mermaid fences and heading
levels do not survive; use the in-repo markdown as the base and apply her changes to it.

## Conventions

- **No em dashes.** No "student"; write for working professionals, use "you" or "participants."
- No curly quotes or apostrophes.
- Markdown only. No HTML, iframes, or scripts in artifact bodies.
- Filenames match slugs; `artifact_id` ends with the slug.
- Working drafts live in `course1/design/`, never under `sprints/`: the validator scans every
  `.md` under `sprints/`.
- Design notes in drafts are marked [NOTE]; items for Leslie to rule are marked [OPEN].

## Traps

**Sprint numbers.** `sprint-6` is Welcome V2, `sprint-7` is Sprint 3 V2, `sprint-8` and
`sprint-9` hold Sprint 4, `sprint-12` is Sprint 1's live first half, `sprint-13` is Jeremy's
feedback demo. Older sections of the decisions log say `sprint-8` or `sprint-10` for Sprint
1, which is wrong.

**Claude's filesystem resets between sessions, but the repo does not.** Anything not committed
is lost; commit rather than download. Uploaded review files land in
`/root/.claude/uploads/`, not the scratchpad.

**A checkout can be behind main.** Another session may have merged since this one started.
`git fetch origin main` and `git reset --hard origin/main` before grepping for a file that
"should" exist.

**Docx conversion loses more than paragraphs.** Word stores tables outside the paragraph
stream and formatting inside run properties, so a paragraph walk silently drops every
table, all bold and italic, and the indentation that marks blockquotes. Extract `w:tbl`
elements, run formatting, and indents explicitly, and diff the round trip before trusting it.

**Regex over already-rewritten text doubles.** A term-expansion pass once produced "candidate
problem problems" in eleven places.

**Editing the decisions log with `str_replace` can eat a header.** Append instead, and read
the file back.

**The concept check gates whatever it draws on.** Its questions are verified against v5.1's
pages. Re-verify if those pages move again.

**`reading` presentation has no AI feedback.** In `guided_assignment`, `presentation: reading`
(several boxes) does not support the feedback endpoint; only `compact` (one box) does.
Multi-box pages get no AI feedback in the current mode.

## Repo facts

- **Mermaid renders.** `canvas_sync/hosted_html.py` converts the fences and injects mermaid 11.16; Canvas iframes the hosted page. Diagrams cost only the drawing.
- **Video cannot be embedded from markdown.** Manual step on the Canvas page after publish.
- The manifest keys artifacts on relative path, so renaming a pushed file means updating the manifest in the same change.
- `python canvas_sync/schema.py --artifact <file>` validates one artifact; needs `pip install jsonschema markdown` (and `defusedxml lxml` for the docx validator).

## Blocked, and on whom

- **Dojo setup.** Sathya's current model is the learner's own chatbot project plus one linked Google Doc (Dojo, Course, Syllabus tabs); no API key. That doc does not exist for course1. With Jeremy since 15 September (`dojo-setup-note.md`).
- **Root Cause Analysis naming.** Three names for one artifact. Team decision.
- **Cohort or self-paced** governs whether any peer mechanic is possible.
- **Sathya's AI-assisted grading tooling**, whether our instructor will have it. Nothing is blocked on it; the design was made insensitive to the answer.
- **CIS395 alignment** on the abstraction ladder cut. Needs an owner.

## Things worth knowing that are recorded nowhere else

**Sathya's Common-Curriculum repo** is design-level (writing-to-teach, writing-assignments,
writing-learning-goals, reviewing-course-text) where ours is operational (build-sprint,
add-artifact, canvas-author). Worth borrowing: provenance footers splitting human and AI
contributions, dated decisions with reasons, named gaps, checklists containing only things
checkable by looking. Not portable: his Canvas pipeline builds HTML in iframes, which our
rules forbid.

**Welcome V2 defers three things to Sprint 1**: choosing the problem, writing the goal, and
setting up the AI tool. It also has to introduce "own your progress" and "graded item."

**Sprint 4 V3 is the model for the own-thinking-first move.** *Name the Gap* is a standalone
graded artifact before any AI, followed by an AI Exchange that tests it. Sprint 1 matches this
with First frames before the Dojo Lab. **Sprint 2 has no version of it.**

**A course-level worry Leslie has not resolved:** whether the course is light on content for
ten weeks. Claude's read is that the thinness is not word count but contact with reality.
Across ten weeks there is exactly one point of contact outside the learner's own head and a
chat window, the Sprint 3 stakeholder conversation. Deferred deliberately, not settled.

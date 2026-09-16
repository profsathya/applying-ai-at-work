---
purpose: Everything needed to continue the Sprint 1 V2 rebuild in a new conversation
last_updated: 2026-09-16, evening
read_first: true
---

# Handoff

New chat? Read this, then `problem-spine.md`, then `sprint-1-decisions.md` from the session of
14 September onward; those entries supersede anything above them that conflicts. Sprint 1 is
cut-ready in `course1/design/sprint-1-working-draft-v5.md` (v5.4.2) and with Jeremy for the
rebuild as of 16 September. The next piece of work is Sprint 2; see "Starting Sprint 2" below.

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
course1/design/sprint-2-outline.md                 Sprint 2, outline v3 (16 September), with Leslie for a ruling on structure
course1/design/candidate-log-template-v2.md        the Log template, v2 (15 September), source for the Google Doc
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

Sprint 1 ends with one chosen problem plus an honest Problem Frame, with every assumption
marked confirmed or unverified. The sequence (Leslie's own run, 14 September): brainstorm a
wide list by category; get underneath three to five of them in a four-column table (the
situation, how it works now, what it costs and whom, the gap); read the seven-part problem
frame and take the concept check; write a first frame for every candidate; have AI test and
widen the frames in the Dojo Lab and choose one; submit the Problem Frame (the frame rewritten,
what changed, which claims first); reflect. The hinge moved: commitment now comes after
framing, because the frame is how you find out which candidate to commit to. The marked
claims are what Sprint 2 works on.

## Current state

| Piece | State |
|---|---|
| Sprint 1, whole | **v5.4, cut-ready**, in `course1/design/sprint-1-working-draft-v5.md`, with a cover note for Jeremy at the top. Content is v5.3, reviewed by Leslie on every page. Four [TEAM DECISION] markers and one [INTERIM] marker carry the open items into the pages for reviewers. Jeremy rebuilds the whole sprint from this file (docx or repo path) |
| Sprint 1 first half, live | Jeremy's 11 September cut, published in sprint-12. Melisa is running this version. It is superseded by v5 and will be replaced at the cut |
| Sprint 1 concept check | Six questions redrafted in v5.1 against the new pages; Jeremy's call on format. Now sits after The problem frame |
| Sprint 2 | Outline v3, 16 September, on the arc Leslie set that evening (is this worth pursuing: break-the-frame assumptions and one check, what exists, what a change costs, a verdict). Sent as a docx. Waits on her ruling on structure before prose. Part 3 moves here |
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

1. **Jeremy rebuilds Sprint 1 from v5.4.** The cover note at the top of the draft is
   his instruction set: carry the text as written, markers into the pages, [BUILD] blocks
   are configuration. He sends back the readback before the pages go to Clare. The old
   sprint-12 module is his to retire.
2. **Leslie re-pastes the Candidate Log v2.1 docx** into the Google Doc (same id), so the
   table headers are bold and the bullets are on separate lines. The link is already in
   the draft.
3. **Name ripple.** "Problem Frame" replaces "Goal Plan and Problem Frame"
   in the Welcome five-artifact map, the home page, and Sprint 3 V2's mid-course goal
   plan revision. Jeremy and Melisa.
4. **Clare's review** of the rendered pages, with the markers visible. Reviewer comments
   come back to this draft, then to Jeremy's build map, not to the pages directly.
5. **The four team decisions** in the markers, plus the Concept check's position, when
   the content has been seen whole.
6. **Sprint 2 prose** on `sprint-2-outline.md`, receiving the assumptions list, the claim
   kinds, and possibly the Problem Frame's Part 3 as its opening activity.
7. **Points and rubrics proposal** across all five sprints, after Clare's review. The
   pipeline does not publish rubrics; they are applied in Canvas by hand and acknowledged.
8. **The Dojo work**, parked: `dojo-setup-note.md` (with Jeremy) and
   `dojo-module-problem-frame.md` (resume when the course doc exists and a second
   person's frame is available).
9. **Collect Melisa's and Clare's run results.**

## Starting Sprint 2

Sprint 2 is Leslie's. The outline is `sprint-2-outline.md`, v3 as of 16 September evening, on
the arc she set in conversation (see the decisions log, 16 September evening, later). It is
with her for a ruling on structure. Its 12 September version was out of date in five ways,
recorded here because the conventions in point 5 still govern the draft:

1. **What it receives.** It says "frame version 2, the riskiest assumption, the list of
   unverified claims." What Sprint 1 now hands on is the **Problem Frame** (no version
   numbers anywhere), its part 6 **assumptions list** (each confirmed or unverified, with
   who could tell you), the Problem Frame's **Part 3** (the two or three assumptions whose
   failure would break the frame, which may move to open Sprint 2; a [TEAM DECISION]
   marker on the Sprint 1 page), the framings considered in the Dojo Lab, the runner-up,
   and the set-aside list. The single riskiest assumption is gone.
2. **The claim kinds land here.** Checkable, prediction, causal bet were cut from Sprint 1
   on 15 September because nothing there used them. They belong where the checking
   happens: the kind decides how an assumption gets checked (ask someone; gather signal;
   split into a checkable present-tense claim and a bet). Sprint 2 introduces them.
3. **Dojo Labs are modules.** The outline has two (What Already Exists; Test the Frame).
   Each is written as a module for Sathya's Dojo core, in the format of
   `dojo-module-problem-frame.md`: what is mine vs what you carry, rounds with named
   characters, start here. Until the course-wide Dojo doc exists, each page also ships an
   interim any-chatbot version of its prompts, capped (a verdict, three findings, one
   question), under an [INTERIM] marker, exactly as Sprint 1's Dojo Lab does.
4. **The proxy works.** The outline's risk "the AI proxy is down" is closed; the reflection
   can be `ai_activity` like Sprint 1's.
5. **Register and conventions** are the Sprint 1 ones: three to eight hundred words a page,
   guidance then example then box, two core examples named at the head of the draft
   (account handovers and the garden plot carry over, so the story holds across sprints),
   no colons standing in for dashes, no "version one/two," no "student," nothing from
   Leslie's own run in the material, [NOTE] for build instructions and [TEAM DECISION] /
   [INTERIM] for reviewer-visible markers.

The way it goes: revise the outline against those five and send it to Leslie as a docx
(she rules on structure before prose); then draft the whole sprint as one working draft in
`course1/design/` on the Sprint 1 model (cover note, one item per `##`, an italic line and
a Response tasks block per item); she reviews in Google Docs and returns a docx; apply
every change individually, log each disposition, merge the design PR yourself. Sprint 2
does not wait on Jeremy's Sprint 1 rebuild. It does wait on Leslie's ruling on Part 3's
home, which changes its first item.

Points: the outline proposes 30 and 55 across two graded items; the team decision on
points and rubrics across all five sprints is still open, so hold the outline's numbers
as a proposal.

## Things that only exist outside the repo

- **Candidate Log template**, Google Doc in a CTI shared drive, id
  `1aTgaDgf1ugkQujJkgvo-EHXUqm9ztN1jMA5SDy3lTjI`, shared anyone-with-link as viewer. Holds
  template v2.1 (source: `candidate-log-template-v2.md`). The copy-on-click link is in the
  Introduction of the draft.
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

**Before any hand-off to Jeremy,** re-read `docs/AUTHORING.md` and `docs/AUTHORING_PRESENTATION.md`.
He changes them without notice, and his run follows them, not us. Name the mode in his
vocabulary (faithful conversion, or instructional adaptation) in the cover note.

**The Drive connector is not a rendering check.** Its text export shows bold in table
cells as literal asterisks and runs empty bullets together. Do not report a formatting
problem in a Google Doc from that evidence; ask Leslie to look, or render the docx.

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
- **No colons standing in for dashes** in participant text (Leslie, 15 September: tell-tale
  AI). Colons survive only as labels. Write the second half as its own sentence.
- **Two core examples per sprint**, named in a NOTE at the head of the draft, with extras
  only for colour. Nothing from Leslie's own run enters the material.
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

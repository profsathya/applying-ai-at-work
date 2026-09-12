---
purpose: Everything needed to continue the Sprint 1 V2 rebuild in a new conversation
last_updated: 2026-09-12
read_first: true
---

# Handoff

New chat? Read this, then `problem-spine.md`, then `sprint-1-decisions.md`. Start at the session
of 10 September in the decisions log; it supersedes anything above it that conflicts.

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
`guided_assignment` delivery mode, Canvas publication, and the review of Sprints 0, 3, and 4.

**The plan as of 11 September.** Solid whole course by 15 September; six days of edits with
Clare; share with the instructor 21 September; later move to the De Anza Canvas. Leslie:
Sprint 1 half two and Sprint 2. Jeremy: first half review, then Sprints 0, 3, 4. Melisa:
run the first half as a participant. Rubrics and points decided soon. Sprint 5 has no owner.

## Where things live

```
course1/sprints/sprint-12/                         Sprint 1 first half, seven artifacts, CANONICAL,
                                                   published to Canvas module 2079 on 10 September
course1/design/sprint-1-half-two-outline.md        half two, outline for Leslie's review
course1/design/sprint-2-outline.md                 Sprint 2, outline for Leslie's review
course1/design/problem-spine.md                    course-level design
course1/design/sprint-1-decisions.md               every judgment call
course1/design/sprint-1-half-one-working-draft-v4.md   FROZEN at v4.2; record only, the artifacts win
course1/design/sprint-1-half-one-working-draft-v3.md   superseded
course1/design/handoff.md                          this file
```

**The rule (Leslie, 12 September): once content is cut into artifacts, the artifact is the
source of truth and the design draft is frozen.** Edits to the first half go to sprint-12,
not to v4. Jeremy's `.sources.json` files sit beside each artifact; whether they permit
direct body edits is an open question for him. Half two and Sprint 2 are drafted in
`course1/design/` until cut.

`sprint-10` no longer exists. `sprint-11` (Working Draft) is retired under `course1/retired/`.

## The design, in one paragraph

Sprint 1 ends with a committed problem plus an honest first frame whose gaps are marked as
gaps. It runs in two halves with opposite dispositions. **Half one: look widely, hold
loosely** (gather indicators, get underneath them, test, rule out, commit). **Half two: go
deep, take it seriously** (meet the frame, find the goal underneath, widen with AI, mark what
you do not know, reflect). The hinge is commitment. The marked gaps are what Sprint 2 works
on, which is what makes the join real.

## Current state

| Piece | State |
|---|---|
| Sprint 1 first half | Cut, published, canonical in sprint-12. Leslie's own read of Check 2, Check 3, Reading the results, and Commit is still owed, now against the artifacts. Jeremy reviewing. Melisa running it |
| Sprint 1 concept check | Six questions written by Jeremy's agent, live, unreviewed by Leslie |
| Sprint 1 half two | Outline written 12 September, decisions pending |
| Sprint 2 | Outline written 12 September, decisions pending. V1 only in the repo |
| Sprint 0, 3, 4 | V2 published; Jeremy reviewing |
| Sprint 5 | One placeholder page. No owner |

## Week 1 on the own-your-progress rhythm, roughly 100 points across the sprint

| Item | Kind | Points | Week |
|---|---|---|---|
| Start your list and get underneath it | Own your progress | 0 | One |
| Things you stopped noticing | Own your progress | 0 | One |
| Things somebody handed you | Own your progress | 0 | One |
| Concept check | Self-check | 5 | One |
| Test and commit | Graded item | 35 | One |
| Your First Frame | Graded item | 15 | Two |
| Goal Plan and Problem Frame | Graded item | 35 | Two |
| Reflection | Graded item | 10 | Two |

Week 1 matches Sathya's rhythm exactly. Week 2 is the 4 September lineup and still carries
three graded items; whether that changes is the deferred course-level call.

House style from the repo: Sprint 3 V2 runs five items, Sprint 4 V3 runs seven, both near 100
points, both badge the concept check as a self-check, both run reflections as
`delivery_mode: ai_activity` with AI follow-ups and a JSON upload. **Sprint 1's reflection
should match that mechanism.** Item count varies with the learning; the skeleton does not.

## What to do next

1. **Leslie rules on the half-two outline's four decisions**, then Claude drafts half two
   as one working document in `course1/design/`, same loop as half one.
2. **Leslie rules on the Sprint 2 outline's four decisions**, then the same for Sprint 2.
3. **Jeremy cuts each into artifacts** through his intake once it survives review. Half two
   continues sprint-12 at positions 8 to 12; Sprint 2 takes the next storage number.
4. **Points and rubrics proposal** across all five sprints, for the team decision. Claude
   can draft it from what exists.
5. **Collect Melisa's and Clare's run results** and read them against sprint-12.
6. **Ask Jeremy** the four open questions in the 12 September decisions entry.

## How we work

Leslie thinks conversationally before building, wants pushback, works one thing at a time,
and wants an outline or a diagram before prose when deciding structure. She reviews in Word
or Google Docs and returns a `.docx`.

**Merging (Leslie's ruling, 10 September).** Claude merges design-doc PRs itself as soon as
the validate check passes: anything under `course1/design/`, the decisions log, this file.
The review of that work happens in the document, not in the PR. Claude stops and asks before
merging anything under `course1/sprints/`, because those merges run the Canvas publish and
put an unpublished module in the course shell.

**Reading her reviews.** Export must be `.docx`, not markdown; Google's markdown export
drops comments and flattens suggestions. Walk the XML tree rather than using regex, because
Word nests insertions inside deletions. `word/comments.xml` holds comment threads with
anchors. **Apply every change individually and audit each one afterward.** A wholesale
rewrite discards line edits silently. This has gone wrong once. If she edits without tracking,
diff against the current markdown rather than eyeballing.

Google Docs round trips introduce curly apostrophes and occasionally drop a space. Check for
both. Mermaid fences survive the trip; heading levels do not, so use the in-context document
text rather than reconstructing from the `.docx`.

## Conventions

- **No em dashes.** No "student"; write for working professionals, use "you" or "participants."
- No curly quotes or apostrophes.
- Markdown only. No HTML, iframes, or scripts in artifact bodies.
- Filenames match slugs; `artifact_id` ends with the slug.
- Frontmatter: `type`, `title`, `slug`, `artifact_id`, `sprint`, `week`, `module`, `position`, `points`, `submission_type`, `publish`. Everything stays `publish: false`.
- Section letters A-F are scaffolding for us and get stripped before Canvas.

## Traps

**Sprint numbers.** `sprint-6` is Welcome V2, `sprint-7` is Sprint 3 V2, `sprint-8` and
`sprint-9` hold Sprint 4. Sprint 1 V2 uses **`sprint: 10`**. The old handoff had 6 and 7
reversed; older sections of the decisions log say `sprint-8`, which is wrong.

**Claude's filesystem resets between sessions, but the repo does not.** Anything not committed is lost; commit rather than download.

**Docx conversion loses more than paragraphs.** Word stores tables outside the paragraph
stream and formatting inside run properties, so a paragraph walk silently drops every
table, all bold and italic, and the indentation that marks blockquotes. This happened on
9 September and cost a rebuild. Extract `w:tbl` elements, run formatting, and indents
explicitly, and diff the round trip before trusting it.

**Google Docs round trips drop the mermaid fence.** The v3 draft arrived twice with the
`flowchart TD` block as bare text. Restore the fence before the file goes anywhere near
`sprints/`, or the diagram renders as prose.

**Regex over already-rewritten text doubles.** A term-expansion pass once produced "candidate
problem problems" in eleven places.

**Editing the decisions log with `str_replace` can eat a header.** Append instead, and read
the file back rather than trusting the tool's success message.

**The concept check gates whatever it draws on.** Its six questions were verified against v3
pages that no longer exist in that shape. Re-verify against v4 before rebuilding the quiz.

## Repo facts

- **Mermaid renders.** `canvas_sync/hosted_html.py` converts the fences and injects mermaid 11.16; Canvas iframes the hosted page. Diagrams cost only the drawing.
- **Video cannot be embedded from markdown.** Manual step on the Canvas page after publish. One placeholder, in C1.
- The manifest keys artifacts on relative path, so renaming a pushed file means updating the manifest in the same change. Nothing here has been pushed.

## Blocked, and on whom

- **API key / Dojo setup.** Unresolved since Sprint 0. Blocks the half-two Dojo Lab and all of Sprint 2 unless those activities are written to run in any chatbot, which both outlines do. Team decision.
- **The AI proxy is down** (`ai-assisted-pedagogy` Netlify site, per Jeremy's 11 September audit). Blocks the Sprint 4 AI Exchange and every ai_activity reflection. Sathya's to deploy.
- **Root Cause Analysis naming.** Three names for one artifact. Team decision.
- **Cohort or self-paced** governs whether any peer mechanic is possible.
- **Sathya's AI-assisted grading tooling**, whether our instructor will have it. Nothing is blocked on it; the design was made insensitive to the answer.
- **CIS395 alignment** on the abstraction ladder cut. Needs an owner.

## Open questions inside the draft

Listed at the foot of `sprint-1-half-one-working-draft-v4.md`. The three needing Leslie: the
no-AI note in OYP 1, the declined-and-flagged "requires a different solution" line in OYP 3,
and her review of Parts 3 through 5 of the graded item. The A1 nudge is settled: kept, reworded.

## The test fixture

Leslie ran the opening of half one on herself and produced four items. They are held
**separately** and deliberately kept out of the teaching material: a document built on her
items will always work on her items, which destroys the only independent check available.
That run killed the six-indicator table, produced the three-source structure, and found the
item the move failed on. **Upgraded 9 Sept: Melisa and Clare run the half-one material as participants** rather than
supplying four cold items. Their items still work as an independent fixture, since the
examples were not built on their lives. Blocked on Leslie's review of E and the test edition.

## Things worth knowing that are recorded nowhere else

**Sathya's Common-Curriculum repo** is design-level (writing-to-teach, writing-assignments,
writing-learning-goals, reviewing-course-text) where ours is operational (build-sprint,
add-artifact, canvas-author). Worth borrowing: provenance footers splitting human and AI
contributions, dated decisions with reasons, named gaps, checklists containing only things
checkable by looking. Not portable: his Canvas pipeline builds HTML in iframes, which our
rules forbid. His own principle is that a skill gets written the first time real work
exercises it, so copying his wholesale would violate the thing that produced them.

**Welcome V2 defers three things to Sprint 1**: choosing the problem, writing the goal, and
setting up the AI tool. The last is load Sprint 1 did not previously carry.

**Sprint 4 V3 is the model for the own-thinking-first move.** *Name the Gap* is a standalone
graded artifact at 15 points before any AI, followed by an AI Exchange that tests it. Sprint 1
matches this with Your First Frame. **Sprint 2 has no version of it.**

**A course-level worry Leslie has not resolved:** whether the course is light on content for
ten weeks. Claude's read is that the thinness is not word count but contact with reality.
Across ten weeks there is exactly one point of contact outside the learner's own head and a
chat window, the Sprint 3 stakeholder conversation. Adding pages will not fix that. Deferred
deliberately, not settled.

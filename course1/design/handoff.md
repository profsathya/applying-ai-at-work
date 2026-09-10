---
purpose: Everything needed to continue the Sprint 1 V2 rebuild in a new conversation
last_updated: 2026-09-10
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
reviewer.

## Where things live

Everything is in the `applying-ai-at-work` repo, committed 9 September 2026 on the
`claude/eloquent-goodall-qvfhpn` branch. Leslie still holds the review copies she exchanges
with reviewers as `.docx`; the repo is the record.

```
course1/design/problem-spine.md                    course-level design
course1/design/sprint-1-decisions.md               every judgment call
course1/design/sprint-1-half-one-working-draft-v4.md   half one, restructured 10 Sept; the live draft
course1/design/sprint-1-half-one-working-draft-v3.md   superseded by v4; kept for the diff
course1/design/handoff.md                          this file
course1/sprints/sprint-10/introduction-find-the-problem-worth-solving-v2.md
                                                   02 Introduction, five owed edits applied
```

The working draft sits in `course1/design/` rather than `sprint-10/` because the schema
validator checks every Markdown file under `sprints/` for artifact frontmatter. It moves into
`sprint-10/` as artifacts once the page and submission cuts are made.

Five earlier files are **superseded and should be deleted** if they are still around:
`03-concept-finding-the-problem-underneath-v2.md`, `S-half-one-outline.md`,
`03-section-B-rebuild.md`, `S-half-one-working-draft.md` (v1), and
`S-half-one-working-draft-v2.md`, superseded by v3 on 9 September. Three fragments drifted out of
alignment within a day, which is why half one is now one file.

## The design, in one paragraph

Sprint 1 ends with a committed problem plus an honest first frame whose gaps are marked as
gaps. It runs in two halves with opposite dispositions. **Half one: look widely, hold
loosely** (gather indicators, get underneath them, test, rule out, commit). **Half two: go
deep, take it seriously** (meet the frame, find the goal underneath, widen with AI, mark what
you do not know, reflect). The hinge is commitment. The marked gaps are what Sprint 2 works
on, which is what makes the join real.

## Current state

| Section of v4 | What it is | State |
|---|---|---|
| 02 Introduction | Separate artifact in sprint-10 | Solid. Small edits owed once v4 settles, listed in v4's Open items |
| OYP 1 | Start your list and get underneath it | Reviewed twice. Second-round edits applied 10 Sept; the rewritten three-pass example is unreviewed |
| OYP 2 | Things you stopped noticing | Rebuilt 10 Sept from C1 plus a new activity |
| OYP 3 | Things somebody handed you | Rebuilt 10 Sept from C2, C3, and B5 plus a new activity |
| Concept check | Self-check, 5 points | Placement defaulted after OYP 3; questions need re-verification against v4 |
| Graded item, Parts 1-2 | Choose rows, write as candidate problems | Reviewed once; edits applied 10 Sept. Part 2's shape is now a titled list |
| Graded item, Part 3 opening | What the checks are for | Reviewed once; edits applied |
| Graded item, Checks 1-4 and after | Checks, reading results, AI exchange, commit | v3's E and F, **unreviewed**. Check 2 carries an open flag |
| Half two | Everything | **Not started** |
| 01 module header | Summarizes the rest | Written last, by design |

**Five edits owed to 02, applied 9 September in the repo copy.** The four-check list said "testable at this size" and
contradicted E5. The problem frame (Term 2) moves out into half two. The Next section and
Week 1 bullet point to the superseded concept page. Time Guidance says "the noticing step,"
a name that stopped existing when section A was renamed. And "you own the goal, the
standards, and the final judgment calls" gets rewritten toward Welcome V2's Human Value
term, dropping "standards" (Leslie: never understood what standards meant).

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

1. **Leslie finishes reviewing v4** from Check 1 onward, plus the rewritten three-pass
   example in OYP 1 and OYP 2 and 3, which she has not commented on yet. Rulings riding
   along: the no-AI note in OYP 1, the "different path" line in OYP 3, the concept check
   placement, and the Check 2 overlap flag.
2. **Cut v4 into `sprint-10/` artifacts** per the cut plan at the foot of v4. Mechanical
   once the review lands. Strip the [NOTE] and [OPEN] blocks; keep the participant text.
3. **Re-verify the concept check** against the v4 pages, both content coverage and answer
   integrity, then rebuild the quiz artifact.
4. **Build the test edition for Melisa and Clare**: the cut artifacts, plus the ask. Do it,
   do not critique it, time yourself, note where you stall.
5. **Apply the small Introduction edits** listed in v4's Open items.
6. **Draft half two.** Must open with the first guess and the assumptions.
7. **Rebuild Sprint 2.** Urgent by week three. Must receive the riskiest assumption, carry
   check 2's widening, and gain its own think-first artifact.
8. **Log the course-level call** on whether other sprints adopt the OYP rhythm, when it is
   made. Also a maintainer task: the ungraded grade group in the course1 manifest.

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

- **API key / Dojo setup.** Unresolved since Sprint 0. Blocks the E8 AI exchange and the half-two Dojo Lab. Team decision.
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

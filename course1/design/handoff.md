---
purpose: Everything needed to continue the Sprint 1 V2 rebuild in a new conversation
last_updated: 2026-09-09
read_first: true
---

# Handoff

New chat? Read this, then `S-problem-spine.md`, then `S-DECISIONS.md`. Start at the session
of 9 September in the decisions log; it supersedes anything above it that conflicts.

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
course1/design/sprint-1-half-one-working-draft-v3.md   sections A-F, the whole of half one
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

| Section | What it is | State |
|---|---|---|
| 02 Introduction | Separate file | Solid. Two edits owed, see below |
| A | Start with what bugs you | Drafted, Leslie reviewed |
| B | Getting underneath | Drafted, Leslie reviewed |
| C | Two other places to look | Drafted, Leslie reviewed |
| D | Build your list out | Rebuilt 9 Sept from Leslie's review: D1 compressed, promotion sentence in D3, assumptions link in D4 |
| E | Find out which survive | Substantially new 9 Sept: E1 teaches what the checks are for, Checks 1-4 rebuilt to the question / why / how-to-run / pass-fail / what-failing-tells-you pattern. Household test restored into Check 4. Needs Leslie's review |
| F | Commit | Updated 9 Sept: why-you line in F2, bored-survivor exit in F4. Needs Leslie's review |
| Half two | Everything | **Not started** |
| 01 module header | Summarizes the rest | Written last, by design |

**Five edits owed to 02, applied 9 September in the repo copy.** The four-check list said "testable at this size" and
contradicted E5. The problem frame (Term 2) moves out into half two. The Next section and
Week 1 bullet point to the superseded concept page. Time Guidance says "the noticing step,"
a name that stopped existing when section A was renamed. And "you own the goal, the
standards, and the final judgment calls" gets rewritten toward Welcome V2's Human Value
term, dropping "standards" (Leslie: never understood what standards meant).

## Graded outputs: six items, roughly 100 points

| Item | Points | Half |
|---|---|---|
| Concept Check | 5 | One |
| Candidate List (section D) | 15 | One |
| Test and Commit (sections E and F) | 20 | One |
| Your First Frame | 15 | Two |
| Goal Plan and Problem Frame | 35 | Two |
| Reflection | 10 | Two |

House style from the repo: Sprint 3 V2 runs five items, Sprint 4 V3 runs seven, both near 100
points, both badge the concept check as a self-check, both run reflections as
`delivery_mode: ai_activity` with AI follow-ups and a JSON upload. **Sprint 1's reflection
should match that mechanism.** Item count varies with the learning; the skeleton does not.

## What to do next

1. **Leslie reviews v3's D through F**, especially the new E. Two rulings ride along: the
   no-AI instruction for D (her review comment questions it; v3 keeps the narrow version
   pending her call) and the para 133 wording in C2.
2. **Build the test edition for Melisa and Clare** once E survives review: v3 with markers
   and scaffolding stripped, plus the ask. Framing per the 9 Sept ruling: do it, do not
   critique it, time yourself, note where you stall. This supersedes "send them the arc."
3. **The activities pass**: build the Candidate Log (decided 9 Sept, unbuilt), one
   collecting document started in A with D5 and F5 as snapshots, template visibly asking
   for roughness. Then the page and submission cuts; strongest break after D5.
4. **Apply the five edits to 02.**
5. **Draft half two.** Must open with the first guess and the assumptions (moved there
   deliberately; 02's Carry Forward points at them).
6. **Rebuild Sprint 2.** Urgent by week three. Must receive the riskiest assumption, carry
   check 2's widening (the literature-review layer, per the frameability ruling), and gain
   its own think-first artifact.
7. Done 9 September: spine, decisions, handoff, and working draft in `course1/design/`; the Introduction in `course1/sprints/sprint-10/`.

## How we work

Leslie thinks conversationally before building, wants pushback, works one thing at a time,
and wants an outline or a diagram before prose when deciding structure. She reviews in Word
or Google Docs and returns a `.docx`.

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

**Regex over already-rewritten text doubles.** A term-expansion pass once produced "candidate
problem problems" in eleven places.

**Editing the decisions log with `str_replace` can eat a header.** Append instead, and read
the file back rather than trusting the tool's success message.

**The concept check gates whatever it draws on.** The six-row table it drew on is gone. As
of 9 Sept the D-to-E hinge placement has something real to gate: E1's what-the-checks-are-for
teaching. Placement still open.

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

Listed at the foot of `S-half-one-working-draft-v3.md`. The four needing Leslie: the
other-people nudge in A1, the declined-and-flagged "requires a different solution" line in
C2, the no-AI rule for section D, and her review of the new E section itself.

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

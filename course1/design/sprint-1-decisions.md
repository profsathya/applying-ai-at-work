# Sprint 1 V2: Decisions Log

Drafted 19 August 2026. Every call made while building these artifacts, including the
ones that were not mine to make. Overturn freely.

Skeleton signed off by Leslie before drafting. Content decisions below were made by
Claude unless marked otherwise.

---

## Decisions carried from the problem spine

These were agreed in the working session and are implemented here rather than decided
here.

| # | Decision | Where it shows up |
|---|---|---|
| 1 | Noticing, not recall, is the entry point | Introduction, What You Already Notice |
| 2 | Compartmentalizing framed as a skill, not a failure | Introduction |
| 3 | Four checks with the "plausibly not a definite no" bar | Introduction, Test Your Candidates |
| 4 | Killing a candidate is a success | Module header, Test Your Candidates |
| 5 | Stuck on understanding vs stuck on execution | Introduction |
| 6 | Conditions, decisions, grievances, wishes named as non-problems | Introduction |
| 7 | Household test for personal problems | Introduction, Test Your Candidates |
| 8 | Exit windows stated: free through Sprint 2 | Module header, Test Your Candidates, Goal Plan |
| 9 | Own thinking before AI, with the mechanism explained | Introduction, What You Already Notice |
| 10 | Real pushback is specific and costly | Introduction, Dojo Lab, rubrics |
| 11 | Confirmed / inferred marking, continuous with Sprint 3 V2 | Goal Plan |
| 12 | Explain to someone outside the course | Introduction, Test Your Candidates, Goal Plan |

---

## Calls made in drafting

### Structure

**Seven artifacts, not five.** Sprint 3 V2 collapsed to five. Sprint 1 carries first-time
Dojo setup, first Dojo use, and problem selection, none of which Sprint 3 carries. Seven
was the smallest number that fit without a single activity doing three jobs.

**"How to Get Help" cut as a standalone page.** Folded into the Introduction as a short
section. Welcome V2's Help and Resources page now covers the logistics half, so a separate
Sprint 1 page would have duplicated it. This reverses my earlier recommendation to keep it.

**The old AI Exchange and Problem Framing Check are gone as separate artifacts.** Their
content is now Part 1 and Part 3 of the Goal Plan, following the Sprint 3 V2 pattern of
absorbing standalone AI activities into the deliverable they serve.

**Points: 95, up from about 85.** Weighted toward the terminal artifact (35) and the Dojo
Lab (20). The noticing step carries 10 despite being the highest-value work, because
weighting it higher would invite polish where roughness is wanted.

### Content

**The abstraction ladder stays**, per the sign-off. It is taught once, on the Introduction,
with a five-rung worked example built on the onboarding case. Everywhere else references
it rather than re-explaining it. The Dojo Lab uses it as the organizing move for @framer.

**A new worked example runs through the sprint.** The onboarding case (nine-day access
delay, unowned handoff) appears in the ladder, in check 2, in the Goal Plan's weak/strong
pairs, and in the concept check. One case seen from several angles beats several unrelated
cases. The two existing Concept page examples were not carried over; the resume-rewrite one
could be added back if you want a non-workplace instance.

**Three candidates is the floor**, not one. This is the change that makes the checks
teachable, since a check that never kills anything is not a check.

**A candidate can die at check 1 and stop there.** Running all four on a dead candidate is
busywork, and the worked example demonstrates stopping early.

**"Evidence, not agreement"** language carried forward from Sprint 3 V2's conversation
prompt, introduced early in the Goal Plan's Part 1 so it is familiar by Sprint 3.

**Two named Dojo personas: @framer and @challenger**, in that order, matching the current
Sprint 1 Dojo prompt. If the persona set has changed, these need updating.

### Rubrics

All rows name something checkable by looking. No row says "demonstrates understanding" or
restates an adjective from the goal. Two rows explicitly reward honest uncertainty and
honest non-change, so that holding your ground and saying you were unsure are both
gradeable as success rather than as gaps.

---

## Left as placeholders

Two `TODO` and one `TEAM DECISION` marker remain, all in the Dojo Lab's Part 1:

1. Dojo setup steps. Blocked on the Dojo Setup and How-To page in the Welcome module,
   which is still `[TODO: content pending]`.
2. The API key decision. Copied forward from Sprint 0's existing `TEAM DECISION` marker:
   API key via the built Dojo, or converting your own chatbot. This blocks setup and
   therefore blocks the whole sprint.
3. The Dojo how-to video. Note that video cannot be embedded from Markdown and must be
   added on the Canvas page after publish.

Everything else that was a placeholder in Sprint 1 has been written or removed. The
original eight placeholders are gone.

---

## What these artifacts do not resolve

**The Root Cause Analysis naming conflict.** I named the terminal artifact "Goal Plan and
Problem Frame," dropping "Reframing Document." The course brief calls it a Root Cause
Analysis and Sprint 0's glossary is blocked on this. My change makes the conflict worse,
not better, until someone decides. Flagging rather than hiding it.

**The peer question.** Held per your instruction. The "explain it to someone outside this
course" instruction appears three times and is the one piece that works regardless of the
pacing decision. No participant-to-participant activity was added.

**Whether the module header's three learning goals are right.** I wrote them from the
spine's hierarchy: one terminal goal, one enabling goal, one AI move. They differ from both
existing lists. The homepage.yaml goals will need to match whatever you settle on.

**Sprint 2's dependencies.** These artifacts hand Sprint 2 two things it does not currently
expect: a riskiest assumption to build a confirmation plan from, and check 2 as the thing
Sprint 2 tests. If Sprint 2 is not rebuilt to receive them, the handoff will not land.

---

## Build notes

- Path: `course1/sprints/sprint-8/`, following the parked-V2 convention used by sprint-6
  (Sprint 3 V2) and sprint-7 (Welcome V2).
- `sprint: 8` in frontmatter, `module: 'Sprint 1 - Reviewed (V2)'`.
- All eight files `publish: false`.
- Artifact IDs follow `course1-sprints-sprint-1-reviewed-v2-<slug>`.
- Filenames match slugs. Frontmatter validated against `schema/frontmatter.schema.json`.
- No em dashes. No occurrences of "student."
- `homepage.yaml` is not included and will need Sprint 1 entries plus updated learning
  goals and `verify` lines.

---

## Revisions after first review

**19 August, register.** Both openings led with stakes: "everything you do for the next
ten weeks runs on the problem you choose here," and "the problem you will carry for the
next ten weeks." Flagged by Leslie as the opposite of the agreed design. It was also
inaccurate, since candidates are meant to die and switching is free through Sprint 2.

Both now lead with release: you do not need to arrive with a problem, most candidates will
not survive, that is the design. The module header's "What happens if you pick wrong"
heading became "You can change your mind," because the old heading framed switching as
recovery from an error rather than as the expected path. The cheap-now-expensive-later
principle is kept but stated as the reason for the sprint's shape rather than as a warning.

**19 August, vocabulary.** The Introduction argued the course's central case in fresh
words, duplicating Welcome V2 with different terms. Welcome V2 already establishes
**Superagency**, **Human Value**, and **Symbiotic Thinking**, and names the first two in
its module learning goals. A participant would have met two framings of one idea two pages
apart.

Superagency is the same idea as the generative framing developed in the working session:
previously unreachable problems now reachable. Human Value is the same idea as the
mechanism behind own-thinking-first: your context is what AI cannot supply.

"Why choosing is the hard part" was replaced with "Why this sprint works the way it does,"
which names both terms, borrows Welcome V2's line that most work that fails fails because
the wrong problem got solved very well, and then spends its length on three narrower whys
specific to this sprint: why noticing rather than picking, why several candidates rather
than one, why your own thinking before AI.

Two further connections made: the Dojo Lab now identifies itself as the tool introduction
Welcome V2 promised for Sprint 1, including the no-cost statement and the thinking-partner
framing. The Reflection now names Superagency as what the before-and-after record is
evidence for.

**19 August, structure.** The Introduction did not match the section pattern every other
sprint opening page uses. Sprint 3 V2, and the Start Here pages in Sprints 2, 3, and 5, all
end with Two-Week Sprint Map, Time Guidance, Working Standard, and Carry Forward, in that
order, with near-identical wording. Sprint 1 V2 had only Next.

All four added, boilerplate wording kept where it is shared so the page reads as part of
the same course. Two are adapted rather than copied: Time Guidance names the noticing step
as the one not to rush, and Working Standard adds a line saying rough writing is wanted in
places, since this sprint asks for it explicitly. Carry Forward names why the first-guess
paragraph must stay unedited, because two later activities compare against it.

Structure matched; proportions deliberately not. Sprint 3 V2's Introduction runs about 60
lines of body against Sprint 1 V2's 180, because Sprint 1 is the entry point and teaches
more. Matching its length would have meant cutting content that belongs on the page.

Two duplications removed instead. The four checks were taught in full in the Introduction
and restated in full in Test Your Candidates; the Introduction now introduces them in a
numbered list with the bar and the kill rule, and the operational detail, weak and strong
examples, and kill conditions live in the assignment where the page will actually be open.
The weak-versus-strong pushback example appeared in both the Introduction and the Dojo Lab
and now appears only in the Dojo Lab.

Net effect on the Introduction is roughly neutral in length: about 30 lines of duplication
removed, about 28 lines of standard sections added. The content is better placed rather
than shorter. If further trimming is wanted, Getting Help is the next candidate, since
Welcome V2's Help and Resources page covers part of it.

**19 August, abstraction ladder cut.** Decision from Melisa. The ladder is removed from
Sprint 1 V2 entirely: no separate concept page, no Introduction section, no Dojo Lab
organizing move, no rubric row, no reflection reference.

Nothing was orphaned by this. The ladder's real job in Sprint 1 was scope movement, and
check 4, testable at this size, already covers scope. The Dojo Lab's widening move was the
only thing that needed replacing.

It now widens through **alternative framings** instead: three other ways to see the same
situation, each with what it makes visible, what it makes you miss, and who would have to
be involved. Two follow-up prompts were added, one asking which framing would be hardest to
test in ten weeks, and one asking whether any framing reveals the problem is already
handled. This is better suited to the sprint than the ladder was, because it is directly
about framing choices rather than about a vocabulary that has to be taught first, and it
needs no prior instruction.

**Still open:** the current Sprint 1 Start Here page carries a note to align the
abstraction-ladder framework with CIS395. Someone should confirm who owns that dependency
before the cut is final.

**19 August, Introduction rebuilt to the course template.** Leslie's call: hold consistency
in the Introduction and add pages elsewhere if instructional content needs a home.

The earlier draft had eleven top-level sections and did not match how any other sprint
opens. Sprint 3 V2's Introduction is: overview, **Sprint N Road Map**, **Sprint N
Concepts** with `###` sub-sections, then the four standard sections and Next. The Road Map
and Concepts wrapper had been missed entirely in the first draft.

Rebuilt to that exact shape. Four concept sub-sections against Sprint 3's four:

- Noticing What You Have Stopped Seeing
- Goal, Problem, and Frame
- What Makes a Problem Workable
- Problems You Cannot Work

The Introduction went from 195 lines to 112. Sprint 3 V2's is comparable. Three things
moved to where they get used: the six noticing signals to What You Already Notice, and the
honest-looking bar and household test to Test Your Candidates. The three narrow whys, why
noticing, why several candidates, why own thinking first, were distributed into the
sub-sections they belong to rather than sitting as their own section.

The exit window moved **up** into the overview, which fixes a real defect: concept check
question 6 tests which sprint you can switch through, and the previous Introduction never
said. All six quiz questions are now answerable from the Introduction alone.

Superagency and Human Value are no longer named. Sprint 3 V2's Introduction does not name
them either, and Welcome V2 carries the full argument. The ideas remain, in the overview's
second paragraph, in the same register Sprint 3 uses.

**Not yet aligned:** the module header uses its own section names (Learning goals, What you
will produce, Where your problem comes from, You can change your mind, Completion criteria,
Time). The course-standard module header sections are Sprint Rhythm, Portfolio Thread, and
Completion Criteria. Worth a pass if consistency should extend to module headers.

---

**20 August, overview rewritten by Leslie.** The page opened inside its own frame: "work is
full of friction" assumes the reader has already accepted that noticing friction is the
activity. Leslie's rewrite moves outward first, to what you finish the course with, then
narrows to the course, then to this sprint, then to how AI is used. Adopted with four
adjustments: "criteria that will make them useful for this course" became criteria that
separate a workable problem from one that will stall, since the checks are about reality
rather than about assignment constraints; "we're going to use AI in certain ways" was cut
as empty; the closing was firmed from "maybe even have thought about what solving it might
look like" to naming what you would need to find out next, with the solution note kept as a
secondary sentence; and a stray space was fixed.

**"Try on" replaces "candidates are meant to die."** Leslie's phrasing. It is better,
because it needs no reframe: abandoning something you tried on is ordinary rather than
notably brave. Propagated through the module header and Test Your Candidates.

**20 August, noticing was too narrow.** Flagged by Leslie. The earlier draft made noticing
the only route into a problem, which excludes the person who already has an obvious one and
the person whose manager just handed them something. The original insight was narrower than
I built it: some people have not labeled their frictions as problems, not all people arrive
empty.

A new concepts sub-section, **Where Candidate Problems Come From**, names four routes:
something obvious and current, something someone handed you, something you gave up on, and
nothing comes to mind. The second route connects to the surface request concept already on
the page, which is exactly what a manager's request is. Noticing is now the fourth route
rather than the frame around all of them, and its sub-section opens with "if nothing comes
to mind."

**What You Already Notice renamed to Find Your Candidates.** The old title committed to one
route in the name. The new one is route-agnostic and pairs with Test Your Candidates. Its
"Before you write" section now lists the routes first and offers the noticing prompts as a
fallback for people who come up short, with a line saying the noticing list is worth running
once even if you arrived confident. Slug, artifact_id, and all five cross-references
updated.

**20 August, exit windows removed from Sprint 1.** Leslie's call. Stating in week 1 that
switching is free through Sprint 2 and that Sprint 3 is the last exit is procedural detail
about a future the reader cannot picture yet, and it implies picking wrong is a live danger
with a deadline attached. "You will try on more than one" is the lived version of the same
fact and carries no threat.

Removed from the Introduction overview, and the module header's "You can change your mind"
section became "You will try on more than one." Forward-dated procedure was softened in Test
Your Candidates and the Goal Plan. Concept check question 6, which tested the switching
window, was deleted.

That deletion also fixed a defect: the quiz declared 5 points and contained six 1-point
questions. It is now five questions at 1 point each.

**Owed to the spine.** Section 8, Exit rules, needs revising. The windows still hold as
design, but they are no longer stated up front. Sprints 2 and 3 should carry the message at
the point where it becomes actionable: if this is not the right problem, here is what to do.
The Goal Plan now points forward to Sprint 2 for that read.

---

**20 August, concepts trimmed to vocabulary.** Flagged by Leslie: the Concepts section had
drifted into instruction, covering material that Find Your Candidates and Test Your
Candidates already carry.

Sprint 3 V2 is the calibration. Its concepts are short definitions, and the doing lives in
the Dojo Lab and the Stakeholder Conversation. Sprint 1's now match that: five sub-sections,
each a definition or a claim, no procedure.

- Goal, Problem, and Frame
- Surface Requests, split out from the previous sub-section so it can be named
- Why Problems Hide
- What Makes a Problem Workable
- Problems You Cannot Work

Moved out or cut: the four routes into a problem, which Find Your Candidates now lists; the
per-check detail, examples, and kill conditions, which Test Your Candidates carries; the
household test, likewise; and the forward pointers, which the Road Map already covers.

The four checks remain in the Introduction as four one-line names plus the bar and the kill
rule. That is the minimum a reader needs to understand what the sprint is doing, and it is
what the concept check gates on.

The Concepts section went from roughly 85 lines to 51. The Introduction is 114 lines total.

**One clause added back.** The trim removed the reason behind starting with your own
thinking, which concept check question 5 tests. A single clause was added to Leslie's AI
paragraph: that order matters, because it is hard to judge what AI hands you on a problem
you have not thought through yourself. All five quiz questions are now verified answerable
from Introduction text.

---

**20 August, quiz corruption found and fixed.** Compiling the outline document surfaced a
real defect. When concept check question 6 was deleted, the removal matched only up to the
first `correct: false` line, so three of question 6's four answer options were left behind
and absorbed into question 5. Question 5 ended up with seven options and two marked correct.

Fixed. The quiz now validates: five questions, four options each except the true/false, one
correct answer per question, and five question points against five declared.

Worth noting how this was missed. The earlier verification only checked that each quiz
prompt was supported by Introduction text. It never checked answer integrity, so a broken
quiz passed. Any future edit to the quiz should be validated on both counts: content
coverage and structural soundness.

---

## File naming

**28 August.** Filenames now carry a two-digit order prefix matching the `position`
frontmatter field, so the sequence is readable from a directory listing. Supplements that
are not course artifacts carry an `S-` prefix instead.

```
01-sprint-1-find-the-problem-worth-solving-v2.md   module header
02-introduction-find-the-problem-worth-solving-v2.md
03-concept-from-request-to-problem-v2.md
04-sprint-1-concept-check-v2.md                    6 pts
05-find-your-candidates-v2.md                      10 pts
06-test-your-candidates-v2.md                      15 pts
07-dojo-lab-widen-the-frame-v2.md                  20 pts
08-goal-plan-and-problem-frame-v2.md               35 pts
09-sprint-1-reflection-what-changed-v2.md          10 pts
S-DECISIONS.md
S-problem-spine.md
```

**This is safe but it diverges from the repo convention.** Two things were checked before
renaming:

- `derive_artifact_id()` in `canvas_sync/state.py` builds an id from the relative path, but
  `artifact_id_for_file()` only falls back to it when frontmatter has no `artifact_id`. All
  nine files carry one explicitly.
- `update_artifact.py` falls back to `Path(rel_path).stem` for `slug`, but only when
  importing a new artifact from Canvas with no existing frontmatter. All nine carry an
  explicit slug.
- The manifest keys artifacts on relative path. These files have never been pushed, so
  there are no manifest entries to orphan. If they are pushed and then renamed later, the
  manifest entry must be updated in the same change.

The divergence worth knowing about: every other sprint in the repo names files exactly
`<slug>.md`. If Sprint 1 V2 keeps the prefixes into the repo, either the convention changes
course-wide or Sprint 1 is a deliberate exception. An agent working from repo conventions
may try to "correct" the prefixed names back.

Note also that `S-problem-spine.md` is a course-level document. Its home is
`course1/design/`, not the sprint directory. It is grouped here only for convenience while
Sprint 1 is being built.

---

## Concept page restructured for throughline

**28 August.** Leslie's three criticisms, and the third named the underlying problem: the
page stated a principle, enumerated cases, and cross-referenced between them. Organized for
completeness, not for someone reading top to bottom. Her words: it feels written for AI to
understand, not a human.

**Duplication removed.** The opening listed six indicators as bullets and the table listed
the same six again with more columns. The reader met them twice. The bullet list is gone;
Leslie's opening paragraph now leads straight into the table, which was always the better
presentation because it carries the hiding mechanism and the move alongside each indicator.

**The direction insight became the throughline.** Leslie's observation: five of the six moves
run broad or vague or invisible down to specific. Requests run the other way, arriving
already specific, so the move is up to the goal and then back down. A new section, **Why the
Last Row Is Different**, states this and uses it to justify the length of what follows.
Previously the requests section was simply long, with a one-line hand-off. Now the page
explains why one row needs more work than the other five, which turns the imbalance into an
argument rather than a defect.

**The Door Is Wider Than You Think moved to Find Your Candidates**, as a subsection titled
"Does it count?" It is about whether something qualifies, which is a decision made while
gathering rather than while getting underneath. Moving it removed an interruption between the
opening and the table, and removed a near-duplicate of the Introduction's definition section.

**A second duplication surfaced during the move.** Find Your Candidates had its own six-item
noticing list that substantially overlapped the concept page's indicator table. It now points
at the table as the canonical list and keeps only the three signals the table does not cover:
bracing before something recurring, explaining the same thing repeatedly, and disproportionate
irritation.

Resulting order: opening and table, then if none of these fit, then why the last row is
different, then requests in depth, then the test. Each section answers the question the
previous one raises.

Concept page 162 lines to 143. Find Your Candidates 113 to 120.

**Bug found and fixed.** The earlier term-expansion pass had run its plural rule and singular
rule in sequence, producing "candidate problem problems" in eleven places across five files.
A regex that rewrites text it has already rewritten needs a guard; this one had none.

---

## Rule: when a term gets a numbered slot

**31 August.** Derived while closing a gap in the Introduction, and worth keeping because it
prevents the concepts section from turning back into a glossary.

**A term gets a numbered slot in a sprint's Concepts section if either is true:**

1. The reader's everyday meaning would mislead them.
2. The sprint runs on it.

**Otherwise the term is defined where it is first used.**

Sprint 1's three terms tested against it. *Problem* passes both: everyone's intuition differs,
and the whole sprint is about finding one. *Problem frame* and *candidate problem* pass the
second only; nobody has a wrong intuition about them, they are just central enough that a
participant needs them held still.

*Goal* passes neither. It means roughly what people expect, and the sprint does not turn on
it, so it gets no slot and no definition in the Introduction.

A clause was briefly added to the frame component list, glossing goal and pointing forward.
Leslie rejected it: the list is seven parallel noun phrases and one item carrying a
definition reads like a footnote wedged into a table of contents. Reverted.

The right answer under the rule turned out to be nothing at all. Page 03 is the point of
use, and its two tests for having reached a goal, that nobody would dispute it and that it
says nothing about what to build, define it better than a gloss could. The paragraph below
the component list also uses the word naturally: almost nobody starts with a clean goal and
works their way to a problem.

Worth noting what went wrong in the reasoning. The concern was that three terms had
definitions and a fourth did not, which is a symmetry concern rather than a comprehension
one. No reader stalls on "the goal it serves" in a list of frame components. The rule was
right; applying it to satisfy an aesthetic pattern was not.

*Confirmed* and *inferred* are the near case. They are used precisely, Sprint 3 depends on
them, and they sit in the same component list. They fail test 1 and arguably fail test 2 for
Sprint 1, so they stay defined at point of use in the Goal Plan. If they were promoted, the
Introduction would start accreting a glossary.

**Two notes on the rule itself.**

It is sprint-scoped, not course-scoped. The test is whether *this* sprint runs on the term.
That predicts Sprint 3 numbering *stakeholder* and *validation conversation*, which is exactly
what its Concepts section already does. The rule matches a design decision made independently,
which is some evidence it describes something real rather than rationalising Sprint 1.

Test 2 is the one that will creep, because "important" can be argued for anything. If it needs
a harder edge, one candidate: the term appears in the sprint's learning goals or in its
terminal artifact. *Problem frame* is in both. *Confirmed* and *inferred* are in the artifact
but not the goals, which is why point-of-use feels right for them.

**Correction while deriving this.** The gap was mine, not Leslie's. I said her revision removed
the definition of *goal*. It did not. An earlier draft had a section called "Goal, Problem, and
Frame" that defined it; that definition disappeared when the concepts were restructured after
her "too much depth" comment, several rounds before this one, and nobody noticed. Her revision
only removed a sentence that used the term without defining it. Verified against the review
document generated from the draft she edited, rather than from memory.

**Owed to the spine.** This rule belongs in the spine alongside the register rule and the
vocabulary rule, all three of which are still outstanding.

---

## Comment round on the concept page

**28 August.** Three comments and 12 tracked changes on
`03-concept-finding-the-problem-underneath-v2.md`. All tracked changes applied first, then
audited individually, per the rule added after the previous round.

Leslie stopped partway through, deliberately, because she did not want to edit material that
the earlier comments would change. Everything from the Requests section onward is therefore
still unreviewed.

**Tracked changes.** The opening assertion was cut and the six surface forms became a
bulleted list, each one sharpened: a situation you stopped noticing *because you figured out
a work-around*; a condition you *think* you cannot change; a complaint *or frustration* about
someone *or something*; a solution somebody *else* has already picked *that doesn't feel
quite right*. "The definition from the Introduction" became "our definition for a problem."
The requests lead now says that at work you will often meet something presented as a problem
that is actually a solution already picked. The surface request paragraph gained a line
acknowledging there is a reason someone wants the app.

**Parser bug, found by Leslie.** The first extraction of this document reported change 1 as a
pure deletion of the opening line. It was not: it replaced that line with a new paragraph.

Cause: the extractor used a regex, and a self-closing `<w:del/>` inside the paragraph
properties, which marks the paragraph mark as deleted, was matched as an opening tag. The
regex then ran to the first real `</w:del>`, swallowing the insertion nested inside the
`<w:ins>` element. Word nests insertions and deletions freely, so a regex was never going to
be reliable here.

Replaced with `extract_changes.py`, which walks the XML tree and tracks ins/del state by
ancestry, skipping empty marker elements. Re-ran it against every document reviewed so far:

- Concept page: two changes had been missed, the opening paragraph and the deletion of "what
  you actually encounter is." Both now applied.
- Introduction round two: output identical to the original extraction. Nothing was missed.
- Sprint 3 spec from Melisa: contains no tracked changes at all, only comments. Nothing missed.

Leslie's new opening is in as written: problems rarely arrive as a tidily shaped package, most
people have to think a while to uncover where a problem might be, and there are a few
indicators that one is lurking nearby. It also introduces her term, **indicator**, which the
table section then picks up.

**C0: the hiding section was not comprehensive.** It explained only work-arounds while the
page lists six surface forms. Rewritten as **Why You May Not Already See Your Problem**: it
now states that each form hides the problem in its own way, names how briefly, and points at
the table for the rest. The work-around case keeps its own treatment, since it is the one a
participant is least likely to catch alone, and it retains the compartmentalizing reframe and
the video placeholder.

**Hiding section rewritten again, 28 August.** Leslie flagged four problems with it: it used
"form" as if the word had been defined, when the page had just called them **indicators**; it
pointed forward to a table three sections away, which is unfollowable; the work-around
material was entirely abstract; and the whole thing did not feel like it belonged there.

All four were fair. The section had been trying to do three jobs at once: preview the table,
teach the work-around idea, and reassure. Now it does one, and its title says which:
**If Nothing Comes to Mind**.

It opens by naming the reader who came up empty, explains that this usually means the
opposite of what it feels like, and then gives a concrete case instead of an abstraction: the
monthly report exported in the wrong format, pasted into a spreadsheet and fixed by hand,
twenty minutes a month for two years, which nobody would call a problem. They would call it
how I do the report. The compartmentalizing reframe and the video placeholder follow.

The forward reference is gone. The word "form" is gone. The page's own vocabulary,
indicator, is now used consistently from the opening through the table.

**C1: the table needed an entry point.** Leslie drafted one and it is used close to as
written. The section is now **Surface Entry Points and the Moves Underneath**, opening with
the observation that people start at the surface, that conditions and decisions and requests
are problem indicators rather than workable problems, and that a move is needed to get
underneath.

**C2: the definitions folded into the table.** The four prose paragraphs on conditions,
decisions, grievances, and wishes are gone. The table gained a middle column, **why the
problem stays hidden**, and its rows now carry a concrete example each. Six rows, matching
the six bullets in the page lead, which the previous five-row version did not.

This also answers C0 structurally rather than by adding prose: the hiding mechanism for every
form is now visible in one place, next to the move that defeats it.

**Consequential fix.** The closing Test still read "the same holds for the other four" and
named a grievance. With six rows it now names all five non-request forms correctly. This was
not flagged; it was a consequence of the restructure that would have shipped as an
inconsistency.

**Concept check re-verified.** Q1 and Q4 both depend on this page and both still hold. Q4's
condition example, "my industry is shrinking," survives as a table row.

---

## Second comment round on the Introduction

**28 August.** Ten comments and 33 tracked changes.

**Correction, same day.** This log previously claimed all tracked changes were taken as
written. They were not. The concepts section was rewritten from scratch and Leslie's line
edits were lost in the rewrite. She caught it. All ten have since been applied and audited
individually against the files.

The lesson is procedural: when a review contains line edits and the response is a structural
rewrite, the edits have to be re-applied to the rewritten text deliberately. A wholesale
rewrite discards them silently, and nothing in the process catches it.

Her edits, now in place: the overview promises a problem that works for this course rather
than one you want to work on; the AI paragraph is reframed around directing AI, with the
pattern stated plainly and the reason given as an output you cannot judge; road map step 1
introduces the term inline, gathering possible problems we will call candidate problems; step
3 asks participants to be able to say why one survived and the others did not; the
loaded-word line about "problem" is restored ahead of the definition; the table lead-in is
plainer; and the honest-looking paragraph is hers nearly verbatim, including the concrete
expectation of 1 out of 3 to 5.

**A usable test emerged from C5 and C8.** If a header inside Sprint 1 Concepts feels like it
should be a subheader of another header in that section, it is a layer too deep for the
Introduction. Mechanical enough to apply without re-litigating each time.

Applying it moved Surface Requests, Why Problems Hide, and Problems You Cannot Work out. The
Introduction keeps three concept sections: The Problem Frame, Problems and Candidate
Problems, and What Makes a Problem Workable. It went from 175 lines to 116.

**The two concept pages became one.** The displaced material and the existing request page
were the same topic. Conditions, decisions, grievances, wishes, and requests are all things
that look like problems and are not, and each has its own move to get underneath it. Requests
are the most common and the only one whose method needs a diagram.

`03-concept-finding-the-problem-underneath-v2.md` opens with a five-row table pairing each
disguise with its move, treats the first four briefly, and gives the rest of the page to
requests. `concept-from-request-to-problem-v2` was deleted; its content is intact in the new
page.

**C0: the two definitions did conflict, and are reconciled.** The gap definition is now
primary and bolded, per C2, with a line saying that relative to a goal the problem is what
stands in the way. Same thing from two angles: the gap is what it is, blocking the goal is
what it does.

**C4: the small-and-specific bullet was doing harm.** It implied "our culture resists change"
should be discarded. Rewritten: big and vague is not disqualifying, it is not workable yet,
and there is a specific problem inside it to find.

**C6: candidate problem is defined** in the Introduction, as one you are considering but have
not committed to. Per Leslie the term always appears as both words; a pass expanded every
bare use across seven files. Two exceptions remain, flagged not decided: the artifact titles
Find Your Candidates and Test Your Candidates. Changing them means new slugs, artifact_ids,
filenames, and cross-references.

**C9: the sprint map line** now says the sprint runs across two weeks in one Canvas module,
so the labels are a pacing guide rather than two sections to look for.

**C1: the filled frame example moved to the Goal Plan**, position 08, where participants
build one. It was modelling an output a week before the output gets built.

**Quiz coverage re-verified.** Three questions answer from the Introduction, three from the
concept page. None orphaned.

**01 module header deliberately not updated.** It summarizes the pages, so it is written last.

**Log integrity note.** Two entries in this file were damaged by careless edits: a
`str_replace` consumed the "Surface Requests split into its own page" header, and a later
script reported success while silently matching nothing. Both repaired. Edits to this log
should be verified by reading it back, not by trusting a script's own output.

---

## Surface Requests split into its own page

**28 August.** Leslie's principle: the skeleton is what stays consistent across sprints, not
the artifact count. Every sprint has an Introduction, a Concept Check, a Dojo activity, a
terminal artifact, and a Reflection. Sprints add pages when the learning needs them. This
replaces the earlier working assumption that Sprint 1 should match Sprint 3 V2's count of
five.

Surface Requests moved out of the Introduction into **Concept: From Request to Problem**,
position 3, before the concept check so the check gates both pages.

Two reasons. It was the longest section on the page, and it was the wrong kind of thing to
sit in a concepts list: everything else there is a definition, and this is a method, a move
you perform, with a chain and a diagram. It is also the sprint's central intellectual move,
and it was the third item in a list of six.

The new page carries what it could not as a sub-section:

- The why-chain and the mermaid diagram, unchanged.
- A test for knowing you have reached the goal: nobody would dispute it, and it says nothing
  about what to build. If your answer still contains a solution, you have not gone far
  enough.
- **A second worked example that is not workplace-shaped.** "I need to fix my resume" run
  through the same chain to a goal, then fanned out to three possible problems: wrong
  targeting, responsibilities rather than evidence, and cold applications where roles are
  filled by referral. Only one is a resume problem. The onboarding case was the most
  workplace-shaped example possible, and many participants will not be in that setting.
- **The request you handed yourself.** Self-issued requests are harder to notice than ones
  from a manager, because when your boss hands you a solution it is at least visibly
  someone else's answer.
- A closing test: does the thing in front of you name what should be different, or what
  should be built?

The Introduction keeps a six-line Surface Requests sub-section with the definition, both
short examples, and a pointer forward. It dropped from 214 lines to 174.

Positions shifted: everything from the concept check down moved one place. Sprint 1 is now
nine artifacts. Points unchanged at 95 for the assignments.

**The concept check gained a sixth question.** After the split, all five existing questions
were still answerable from the Introduction alone, which left a required page with no
coverage. The new question tests the page's distinctive move: you ask why and land on "so
we have better visibility," and the answer is that you have not reached the goal, because it
still names something to build. Quiz is now six questions, six points, verified one correct
answer each.

---

Nine comments, 24 August. Eight produced changes; one was a question.

**[5], [3], [4] all pointed at the same structural error, and it was real.** Goal, problem,
and frame were introduced as three parallel terms, and then two of them were listed as
components of the third. They are not parallel. The frame is the container.

Restructured frame-first. **The Problem Frame** now opens by saying what you are building,
lists the seven components, and then defines goal and problem as the two inside it that
people conflate. The convoluted two-jobs paragraph is gone, replaced by a plainer statement
of the messiness Leslie named: you will not fill this in from the top down, almost nobody
starts with a clean goal, you are more likely to start in the middle and work outward.

**[4] specifically:** "Most people arrive with a goal and think they have a problem" was
false. Most arrive with a solution somebody already picked. That sentence now opens Surface
Requests, corrected.

**[7], [8]: the goal-surfacing move was wrong.** "Ask what this would accomplish if it
worked" returns another visibility answer, not the goal. It is repeated **why**. Now a
four-step chain from the request down to a goal nobody would dispute, with a test for
knowing you have arrived: it says nothing about what to build. The abrupt transition Leslie
flagged is gone.

**[6]: the gap definition needed testing against more than one scenario.** A four-row table
now runs it across onboarding, job search, caregiving, and volunteer work, with how it works
now, how it could work, and what the gap costs. Leslie's own career-change example is one of
the rows. Closing line: none of those is a crisis, all of them cost someone something.

**[0]: adopted Leslie's rewrite.** "You will always start with your own thinking" became
"Your own thinking is non-negotiable." Stating it as a standard is stronger than describing
a sequence, and "always" invited exceptions.

**[1]: "kill" removed from all eight artifacts.** Replaced with "rule out." Verdicts in Test
Your Candidates are now **still in** and **ruled out**. The reflection question, a rubric
row, and five check instructions changed with it. The register was borrowed from violence
and sat badly next to "try on."

**[2] was a question, not an edit.** Yes, participants write the frame in Sprint 1, and Road
Map step 5 describes it accurately. But the question surfaces a naming problem: "problem
frame" is now both a concept and half an artifact name, on top of the unresolved Root Cause
Analysis conflict. Three names for adjacent things. Belongs in the key terms pass.

## Media added

**A filled-in frame example**, as a two-column table in The Problem Frame. The seven
components were listed and never shown assembled, which left no guide to length or
specificity. Ends by naming what a frame does not contain: a solution.

**A mermaid diagram of the why-chain** in Surface Requests. The chain narrows from request
to goal, then fans out to three possible problems, then converges on the frame as a choice.
The branch is the concept, and a bulleted list made the three problems look like a menu
rather than forks.

**A video placeholder** in Why Problems Hide, following the format Melisa used in Welcome
V2. Two to three minutes, someone describing a workaround of their own they had stopped
seeing. This concept cannot be argued into someone; watching recognition happen does more
than describing it.

**Mermaid renders in this pipeline.** `canvas_sync/hosted_html.py` converts mermaid fences
into `<div class="mermaid">` and injects mermaid 11.16 from CDN; Canvas shows the hosted
page in an iframe. Existing proof is in `deanza/course1/assignments/pre-dojo-goal-pause.html`.
So diagrams cost nothing beyond drawing them, version with the repo, and need no manual
Canvas step, unlike video. Prefer them wherever they would do.

Unverified: the diagram uses dotted arrows, which no existing course1 diagram does. Standard
syntax, supported in mermaid 11, but it could not be rendered locally and should be checked
on first publish.

---

**Bug found outside Sprint 1.** Sprint 2's Start Here page has a live "Test Section"
containing "Test bullet point 1, 2, 3" in the rendered output. Scaffolding that got
published.

---

**Owed to the spine.** Neither problem would have been caught by the spine as written. Two
additions are outstanding, to be made after Sprint 1 settles: a register rule (lead with
what is released, put the exit before the commitment) and a vocabulary section (use the
terms Welcome V2 established rather than arguing the same ideas in new words). The second
will matter more in Sprints 2 through 5 than it did here.

---

## Provenance

Human (Leslie): the skeleton and its sign-off; the decision to keep the abstraction ladder;
the noticing entry and the insight that people may not know they are bugged; the four
checks, adapted from a build-question filter developed for a separate project; the
instruction to record differences; catching the pressure-first openings; asking whether the
Introduction needed more of a why, which surfaced the vocabulary fork.

AI (Claude): the artifact copy; the onboarding worked example; the rubric rows; the
concept check questions; the placement of check 2 in the Goal Plan's current-handling
section; the decision to cut How to Get Help as a standalone page.

Both errors found in review were mine, and neither was a writing slip. The pressure opening
and the reinvented vocabulary each came from drafting against the spine without checking
what the Welcome module had already established.

Not validated with participants. Nothing here has been tested with a learner.

---

# Session of 4 September 2026: the half-one rebuild

A long working session with Leslie that restructured Sprint 1 rather than revising it.
Everything below supersedes anything above it that conflicts. Recorded at Leslie's request
so nothing is lost to a session reset.

## The end state of Sprint 1, decided

**Sprint 1 ends with a committed problem plus an honest first frame whose gaps are marked
as gaps.** What the person does not know is part of the deliverable, not a failure of it.

Leslie's call, after Claude argued that Sprint 1 held two incompatible versions of "done":
commitment on one hand, a seven-component frame worth 35 points on the other. The spine
already settles it. Section 8 says revising the frame is expected throughout, and Sprint 5
produces the integrated document, so Sprint 1's frame is version one. This resolves three
things at once: the teaching load in half two drops, because the target is a truthful frame
rather than a good one; two weeks becomes survivable; and the marked gaps become the raw
material Sprint 2 works on, which makes the handoff real rather than aspirational.

## The two-half arc

Sprint 1 does two jobs with opposite dispositions, and nothing previously told anyone the
instruction flips.

- **Half one: look widely, hold loosely.** Gather, get underneath, test, rule out, commit.
- **Half two: go deep, take it seriously.** Frame it, widen with AI, mark the gaps, reflect.

The hinge is commitment, which was previously a sentence buried inside Test Your Candidates.
It is now a named movement (section F) with its own output.

**Consequence: the first guess and the assumptions move out of 05.** They were half-two
material sitting in half one, asking someone to get attached to a favourite during the half
built on detachment. This is the defect the old handoff attributed to 06; it was in 05 all
along. They become the opening of half two.

**Consequence: the problem frame moves out of the Introduction.** It was the only idea in 02
that nothing in half one uses. Introduced in 02, unused for three pages, reintroduced in half
two where it is needed. It belongs where it is used.

## The teaching hole in half two

Half one had an Introduction section, a full concept page, and a gated check. Half two asked
for a 35-point frame having taught nothing about frames beyond a bulleted list. **A concept
treatment of the frame is required in half two**, plus a separate graded first-frame artifact
before any AI. Not yet drafted.

## Graded outputs: six items, roughly 100 points

| Item | Points | Half |
|---|---|---|
| Concept Check | 5 | One |
| Candidate List (section D) | 15 | One |
| Test and Commit (sections E and F) | 20 | One |
| Your First Frame | 15 | Two |
| Goal Plan and Problem Frame | 35 | Two |
| Reflection | 10 | Two |

Route to this number: Claude first proposed three graded items plus a quiz, on instructor
load grounds, roughly 190 submissions per sprint across 32 people being unreadable. Leslie
supplied a CTI grading document derived from Sathya's Common Curriculum repo. Two moves in it
mattered.

**Move 2, points as signal (0%-weighted grade groups), was considered and then dropped.**
It would have preserved the own-thinking-first boundary without instructor cost. It became
unnecessary once the repo showed Sprint 4 V3 grading its equivalent artifact outright.

**Move 5, AI-drafted grading with a human gate, is not depended on.** It exists in Sathya's
courses and may not be available to our instructor. The design was made insensitive to the
answer: the two branches differ by one frontmatter field. **Open, and a Sathya conversation:
whether that tooling will be available.** Nothing is blocked on it.

**Moves 3 and 7 (scoring the same work twice, grading movement) were considered and
declined for Sprint 1.** Both need an unrehearsed instrument an asynchronous course does not
have, which the source document itself names as its unresolved question. Declined rather than
designed around.

**Move 6 (no gating across units) flagged to Leslie and Melisa as a course-level call.** It
matters more here than in an in-person course, because an asynchronous person who stalls in
Sprint 1 has no visible path into Sprint 2.

**Precedent that settled it:** Sprint 4 V3's *Name the Gap* is a standalone graded assignment
at 15 points with its own no-AI heading, followed by a separate AI Exchange that tests it.
Sprint 1's Your First Frame matches at 15. Sprint 1 and Sprint 4 doing the same move two
different ways would be an inconsistency a learner feels without being able to name.

**House style confirmed from the repo:** Sprint 3 V2 runs five items, Sprint 4 V3 runs seven,
both near 100 points, both badge the concept check as a self-check, and both run reflections
as `delivery_mode: ai_activity` with AI follow-up questions and a JSON upload. **Sprint 1's
reflection should match that mechanism rather than inventing one.** Item count varies with
the learning; the skeleton does not.

## The six-indicator table is cut

Leslie ran the opening of half one on herself and produced four real items. Three of the six
"move underneath" questions did not fit any of them. Diagnosis: each move had been written
backwards from the example sentence printed beside it, so it worked on that sentence and
nothing else.

**Replaced by one move, derived from the course's own definition of a problem:** describe how
it actually works now, in enough detail that the gap becomes visible. Consistent with 02,
reusable in half two, and it does not depend on which row someone picked. The six questions
survive as stall prompts in B3, which is what they were good for.

**The six categories collapse to three sources:** things that bug you, things you stopped
noticing, things somebody handed you. The page already had this structure without saying so,
since work-arounds and requests each had their own section. Leslie's call: "things you keep
putting off" folds into the bug-you family rather than becoming a seventh category.

## "Some things will not go underneath" was wrong

Claude's first draft claimed some items have no current state to describe, using Leslie's
"I should be better at using AI at work" as the example. Leslie then described the current
state in four sentences, which disproved it.

**Correct diagnosis: that item is a solution, not an indicator.** "Use AI" is an answer
already picked, which makes it a self-issued request needing the C2 why-chain rather than the
B1 move. Section B5 now teaches that, and points at C2. This is better than the invented
category and it strengthens the request material, since it is the case where a self-issued
request is disguised as a wish rather than a task.

## Check 1 changed job; Check 4 recast

**Check 1 duplicated the gap statement.** Leslie caught this. D3's gap shape already asks who
is paying and what it costs them. Cost cannot wait for E, because cost is the definition of a
problem. Check 1 now tests whether the named cost is *specific*, roles or people rather than
categories, with a passes/does-not-pass table. Escalation, not repetition.

**Check 4 recast from "testable at this size."** The old wording was vague and caught neither
failure mode. Wrong size fails in two opposite directions:

- **Too small:** only you touch it, one decision resolves it, nothing to find out. Fix: go up, ask what this is an instance of.
- **Too big:** cannot describe the current state in a paragraph, nobody owns it, everyone affected. Fix: go down, pick one instance.

So Check 4 is a **calibration, not a gate**. The bar: one paragraph describes the current
state, at least one person other than you with a stake who would talk to you, and at least one
thing you would have to find out. Those three map to what half two, Sprint 3, and Sprint 4
respectively demand, so a failure names the week it would have stalled in.

**Open and owed: Sprint 1's Introduction still carries the old four-check list and now
contradicts E5.**

## AI use in half one: the doctrine version is dropped

Leslie's pushback: the course is about applying AI at work, CTI's framework is that you use AI
but never cede ownership, and a general "own thinking first, then AI" rule contradicts the
course's own title.

**Accepted.** The no-AI rule survives only in section D, with a narrow reason: the raw
material has to come from your own life, and AI has no access to what you stopped noticing.
Not a principle about sequencing.

**02 was examined and left alone.** Claude initially claimed 02 stated the doctrine version;
on rereading, it does not. "This is about you directing AI to get what you want" is CTI's
framework almost verbatim, and its reason is a real reason rather than a rule. Only 05
carried the doctrine version, and 05 is being replaced.

**An AI exchange is added at E8**, after the checks and before commitment: hand it your
candidates and your check answers, ask where you are asserting rather than knowing, record
two or three challenges and your response to each. Placed after the checks deliberately, so
AI tests the thinking rather than producing it. Folded into the Test and Commit submission
rather than standing alone, to avoid a third deadline around one afternoon's work. **Depends
on the unresolved Dojo and API key decision.**

## Elapsed time cannot be designed

Claude proposed an overnight gap between gathering and judging. **Leslie's correction: the
course is self-paced and asynchronous, so gaps may be longer or shorter than a night.** What
was actually wanted was distance between gathering and judging, which a submission boundary
supplies regardless of clock time. Pacing language stays advisory and relative, framed against
the two-week sprint guideline and the few-days noticing period.

**This is why section D became its own submission** rather than being folded into a single
candidate-and-commitment artifact.

## Structure of the working document

**One file, `S-half-one-working-draft.md`, superseding four fragments.** Sections A through F
with letter scaffolding in the headers, stripped before Canvas. Reason: three separate files
(a page draft, an outline, a section rebuild) had already drifted out of alignment with each
other within a day. The map and the content must be the same object.

**Page and submission divisions are deferred until the arc is written**, then made as a
mechanical split. Leslie's call: "I want an arc in its entirety, then I want to think about
where to divide that learning up." Noted constraint: on Canvas a page and an assignment are
different objects, so a cut between teaching and doing is free while a cut that adds a
submission adds a deadline.

**Break points currently marked:** after B6, after C3, after D5. Strongest is after D5.

## Leslie's front-half review, applied 4 September

71 insertions, 72 deletions, 5 comments, extracted from `.docx` via a tree-walking script
rather than regex. All applied individually and audited afterward: 46 of 47 distinctive
insertions verbatim, 25 of 25 deletions honored. Three typos introduced by the Google Docs
round trip were fixed (two doubled periods, one dropped space in "They are assuming").

**Structural moves agreed in that review:**

- The A header renamed. "You have more than you think" did not connect; the section is about building a starting list.
- The deleted enumeration (complaints, wishes, postponed decisions, things put off, conditions you cannot change) relocated into the A1 jotting prompt, where someone facing a blank page can use it.
- **A3 relocated to the end of B as B6.** Leslie's question: section C covers these more fully, so should the concept wait? Resolved by moving rather than cutting. At the end of B the reader has tried the move and may have run dry, which is when knowing there are other places to look is useful rather than abstract. C's old opening line was cut as redundant; this is the one insertion of hers not carried forward, by agreement.
- A worked three-pass example added to B4, per her comment asking whether the multi-pass point should be demonstrated.

**One edit of Leslie's declined, and flagged rather than applied silently.** She changed "each
one sends you somewhere completely different" to "each one requires a different solution." The
paragraph's work is separating problems from solutions, so ending it by sorting problems by
their solutions works against it. Rendered as "would send you down a different path."
**Still Leslie's to settle.**

## Test fixture, held separately from the course material

Leslie's four items from her own run are kept **out** of the teaching material and used as a
standing test set instead. Reasons: teaching examples need deliberate coverage (one at work
and one not, one involving other people, one needing several passes, one that fails) which a
five-minute list will not supply; and a document built on her items will always work on her
items, which destroys the only independent check available.

**Her run already returned more than most reviews:** it killed the six-row table, produced the
three-source structure, surfaced the missing put-off category, exposed the pull toward
personal and solo problems, and found the item the move failed on.

**Outstanding: ask Melisa and Clare for four items each.** Three sets from three people would
show quickly whether the move holds for anyone other than its authors.

## Errors in the previous handoff, corrected

- **`sprint-6` is Welcome V2 and `sprint-7` is Sprint 3 V2.** The handoff had these reversed.
- **Sprint 4 V3 files sit in `sprint-8` but carry `artifact_id`s built on `sprint-9`,** while the archive note claims V3 lives in `sprint-9`. Inconsistent. Does not affect Sprint 1, which uses `sprint: 10`. **Flag to Melisa.**
- **The Build notes section of this log** still said `sprint-8` and `sprint: 8` for Sprint 1 V2, which would have collided with Sprint 4 V2. Superseded by `sprint: 10`.
- **The File naming section** lists `03-concept-from-request-to-problem-v2.md`, a file this same log records as deleted and merged.
- **Point total.** The log said 95; the lineup added to 96 after the concept check went to six questions. Both are now superseded by the six-item, ~100-point structure above.

## Open, carried forward

1. The other-people nudge in A1: keep it, or drop it and let D2 do the work. It asks for filtering one line after telling people not to filter.
2. The Introduction's four-check list, which now contradicts E5.
3. Concept check placement: after C3, or at the D-to-E hinge. Either way it can no longer draw on the six-row table.
4. Section C's branches are unequal: C1 about 200 words, C2 about 1,000.
5. The AI exchange at E8 depends on the Dojo and API key decision, still unresolved since Sprint 0.
6. The para 133 wording, above.
7. Half two is undrafted: the frame concept treatment, Your First Frame, the Dojo Lab, the Goal Plan, the Reflection.
8. Whether Sathya's AI-assisted grading tooling will be available to this course's instructor.
9. Root Cause Analysis naming, cohort-or-self-paced, and CIS395 alignment all remain open from earlier sessions.

## Provenance for this session

Human (Leslie): the decision to establish the arc before writing content; running half one on
herself, which produced the four findings above; the correction that a general own-thinking-
first rule contradicts the course's premise; the correction that elapsed time cannot be
designed in a self-paced course; catching that Check 1 duplicated the gap statement; catching
that D through F had no stated outputs; the judgment that examples should be held separately
as a test fixture; the front-half line edits and five comments; the ruling that the jotting
need not be enforced because D catches anyone who skips it.

AI (Claude): the two-half framing and the hinge; the argument that the end state was
undecided; the instructor-load arithmetic; the reading of the CTI grading document and which
moves to take; the single-move replacement for the six-row table; the Check 4 calibration; the
worked hard call in F2; the AI exchange placement; the drafting throughout.

Errors Claude made this session, both caught by Leslie: claiming some items have no current
state to describe (B5, wrong, corrected above), and proposing an overnight gap in a self-paced
course. Both came from designing without running the material.

Still not validated with participants. Leslie's own run is the only test so far.

---

# Session of 9 September 2026

## Week one screens for frameability, not solvability

**Leslie's ruling.** The four checks ask whether a problem can carry nine weeks of framing.
Whether it can be solved in the partner course is Sprint 5's readiness judgment, which is the
existing gate between the courses. Week one is the worst-informed moment in the arc to
predict solvability, and by week ten the problem will not be the one they started with.

What this settles downstream:

- **Check 2 stays local in Sprint 1**: "who or what copes with this here," honest-looking
  depth. The literature-review version (does a solution already exist in the world) is
  Sprint 2's widening, per spine sections 6 and 9. Sprint 2 rebuild must carry it.
- **No solvability check is added** to the four.
- **Right size means "enough left to find out,"** not "small enough to fix next course."

Context: Leslie raised that Check 2 was originally a literature review pointed at the
partner course, and that "right size" felt unresolved. Claude's read, accepted: three of
the four worries were course 2 leaking backward into week one.

## Personal problems: cost can be yours, the conversation cannot be

**Leslie's ruling.** The whole idea is that problems can be your own. The cost of a problem
may fall entirely on the learner. What every problem must have is at least one reachable
person outside the learner who is affected by it **or holds knowledge about it**, because
Sprint 3's conversation needs someone with information, not necessarily a victim. A
job-search problem passes via a recruiter or hiring manager. The household test already
draws this line for caregiving.

Text changes owed:

1. **Check 1** must stop implying the affected people are necessarily other people. The
   check tests specificity of who pays, and "me, and here is what it costs me" is a
   specific answer.
2. **Check 4, second test** reads "at least one person other than you with a stake in it
   or knowledge about it, who would talk to you about it."

Not yet applied to the draft.

## Caring about the problem: not a fifth check, two placements in F

**Leslie's ruling: both.** The checklist stays at four; commitment-to-the-problem is a
choosing criterion, not a screening criterion, since nobody can honestly rate their
investment in five problems listed yesterday.

1. **A required line in the F2 commitment**: why you, why this one, what keeps you here
   when it gets tedious. Makes explicit what "worth nine weeks" gestures at.
2. **A sentence in F4's territory** covering the untied case: a sole survivor that bores
   you is a reason to go back to your list, not a reason to commit to it.

Rationale for not-a-check: checks rule candidates out; caring ranks survivors. And "four
checks" is load-bearing language in the Introduction, spine, and artifacts.

Not yet applied to the draft.

## Right size gets calibrated by testers, with material in hand

**Leslie's ruling, extending the standing fixture ask.** Melisa and Clare test the
half-one material by running it, not by reviewing it. This upgrades the original
four-items request: instead of items generated cold, they work A through F as
participants, which tests the instruction and the checks against real items at once.
Their items remain an independent fixture in the sense that matters: they come from
lives the examples were not built on.

What this requires: a clean test edition of half one. Decision 2 and 3 text changes
applied, the four check treatments assembled into E, the checks opener written, D1
salvaged, internal markers ([NOTE], [OPEN], [BREAK?], letter scaffolding kept or
stripped per Leslie) removed from the copy they receive.

The ask to them should say: do it, do not critique it. Time yourself, note where you
stall, keep what you write. Participant mode produces failures; reviewer mode produces
comments. Failures are worth more here.

## Calls made building v3 (Claude, per rulings above)

- **E1 is now "What the checks are for,"** absorbing old E1 and E7's clean-pass warning.
  Answers Leslie's review comment that the checks' purpose was never stated. Frames each
  check as a course demand arriving early.
- **Checks 1 through 4 rebuilt to the approved pattern**: question, why it exists, how to
  run it, a pass and a fail, what failing tells you. Fail examples deliberately not drawn
  from the running cases, which are too well-shaped to fail believably.
- **Check 1 reworked per the personal-problems ruling**: "me, and what it costs me" is a
  valid specific answer; the reach requirement moved wholly to Check 4.
- **Household test restored into Check 4**, as the personal-problem version of its second
  test, rewritten without "stakeholder" (Sprint 3 vocabulary, and it contrasts with
  knowledge-holder). It had been moved out of the Introduction toward Test Your Candidates
  and lost in transit.
- **Stuck-on-understanding placed as a named special case of too-small** in Check 4, per
  Leslie: fine if it fits logically, droppable if not. It fits.
- **D1 compressed** to the four non-duplicative bullets. Cut: "does not have to be broken"
  (Introduction covers it) and "big and vague" (now Check 4's too-big, with the culture
  example).
- **Candidate promotion sentence added to D3**: the moment the list becomes "your candidate
  problems," closing the loop from the Introduction's Term 3. Leslie's catch.
- **D4 links the question marks forward** to the assumptions named in half two.
- **F2 gains a required "why you" line**, modeled in the worked example. **F4 gains the
  bored-survivor sentence.** Both per the caring ruling. F5's reasons bullet updated to
  match.
- **02 owed-edits list is now five items**, recorded in the draft's Open items, including
  the Human Value rewrite dropping "standards" (Leslie: never understood what standards
  meant).

## Recovered from review, previously untracked

**The Candidate Log (Leslie's ruling, made mid-session and initially unlogged).** Learners
get one collecting document, started in section A and filled as they go, instead of notes
scattered across papers. The two submissions become snapshots of it: D5 submits the
candidate section, F5 submits checks through commitment. Design constraint: the template
must visibly ask for roughness, with question-mark marking built in, since labeled boxes
invite polish. **Not yet built.** Belongs to the activities pass. Origin: Leslie's review
comment on D3-D5 asking what the learner actually produces and whether a template exists.

**The no-AI rule for section D is open, not settled.** Leslie's review comment questioned
whether D needs to exclude AI at all. V3 keeps the narrow version (raw material must come
from the participant's own life) because the learner-output map supports it, but the
ruling is Leslie's and has not been made. The text stands as drafted pending her call.

## Error caught by Leslie, 9 September: the docx conversion dropped every table

The v2 docx-to-markdown conversion walked only top-level paragraphs, so all four tables
were silently lost: B1's what-bugs-you worked table, old E2's pass/fail table, old E5's
diagnosis-and-move table, and the graded-items table at the foot. Leslie caught B1's.
V3 was rebuilt from a corrected conversion, verified by diff: tables were the only loss.

Placement calls on the two tables inside the replaced E section, made by Claude since
Leslie approved the new treatments without either party able to see these tables:

- **Old E2's pass/fail table restored into new Check 1**, replacing Claude's scale bullets,
  which did the same job worse. The blockquote pass/fail pair stays; it works at a
  different grain (full gap-cost lines vs naming phrases).
- **Old E5's diagnosis table restored into new Check 4**, replacing Claude's invented
  too-small example (calendar sync) with the table's export-report case. The culture
  example, which Claude had duplicated in prose, now lives only in the table.
- Tables 1 and 4 (B1, graded items) restored verbatim.

Also corrected for the record: Claude's earlier audit claim that old E2 "had almost
nothing" was wrong. It had this table.

**Second conversion defect, also caught by Leslie:** the same paragraph walk dropped all
run formatting (84 bold runs, 2 italic) and the indentation marking blockquotes. Rebuilt
again from a formatting-aware conversion, verified by stripping the formatting back out
and diffing against the plain conversion: identical content. New material matched to house
style: bold lead-ins on the too-small and too-big paragraphs and the F2 bullets, [OPEN]
markers as bold blockquotes, worked examples as blockquotes. A trap entry went into the
handoff so the next conversion does not repeat either loss.

---

# Session of 10 September 2026: v4, the own-your-progress restructure

Leslie's first review of v3 covered A through D, nine comments and two sets of tracked
changes, returned as a `.docx` after a Markdown export dropped the comments. E and F were
not reviewed and are carried into v4 unchanged, to be read there in place.

## Week 1 runs on Sathya's rhythm

**Leslie's ruling.** Week 1 of Sprint 1 adopts the Fall 2026 own-your-progress mechanic:
one to three ungraded activities and at most one graded item per week. Own-your-progress
items are Canvas assignments at zero points with a must-submit completion mark, in an
ungraded grade group. Encouraged, not required.

Sprint 1 goes first. Whether Melisa's sprints and the grading document follow, or Sprint 1
comes back into line with them, is a course-level call deferred on purpose.

Context: Claude's first outline had four OYPs and two graded items in week 1, against his
ceiling of three and one. Merging the first list with getting underneath it gave three OYPs.
Folding the separate Candidate List submission into the graded item gave one graded item.
That reverses the 4 September choice to grade the gathering step outright, which had been
made to match Sprint 4 V3 rather than on pedagogy. Six graded items across the two weeks was
already triple his rate before v4; v4 leaves week 2 as it was.

## Each activity teaches a move and then runs it

**Leslie's direction, from comments C1, C2, C4, C6.** The prose-then-one-big-submission
shape is gone. Each OYP teaches one move and immediately has the learner run it on their
own list, with guidance, guardrails, and the three-column table as the template. The stall
prompts sit inside the activity. The table is the Candidate Log ruled on 9 September, now
structural rather than a template to build later.

**Depth rule (Claude, on Leslie's question).** No row leaves an activity with an empty
middle column. OYP 1 runs the move on every item at least once and goes multiple passes
on the one with the most to say; Leslie asked whether learners should get under more than
one item, and the answer is yes, because one rep does not build the skill and items that
respond differently teach the range. OYP 2 and 3 run the move on each new row as it is
added. The table's three columns define the depth: enough to describe the current state
and see the gap, not yet who specifically pays or why it is unfixed. The graded item adds
that layer, which is exactly what Check 1 tests.

**A selection step, new (Leslie's question).** v3 said "write three to five of them as
gaps" and never said how to get there from a longer list. Part 1 of the graded item now
does it: keep every row where the move worked, set aside the rest without deleting, take
the five where the gap is clearest if there are more, go looking if fewer than three.
Clearest, not most important: the four checks stay the only screening criteria, so "four
checks" stays true. It sits on the judging side of the submission boundary so it benefits
from the gap in time. F4's "go back to your list" now has a real list.

## Comment dispositions

- **C0, "Is 'I' anywhere else?"** No. The heading was the only first-person singular on
  the page; body text says "we." Heading is now "What we did not ask for."
- **C1, guidance and guardrails for the practice.** Built as "Your turn: build your table"
  with three guardrails for the middle column and one line for the third.
- **C2, where the stall prompts go.** Inside the activity, after the instruction, before
  the no-AI note.
- **C3, move B5 to C2.** Done. It sits in OYP 3 as "When the move gave nothing back,"
  immediately before "The requests you hand yourself," and picks up any row the learner
  marked in OYP 1.
- **C4, C gets its own activities.** OYP 2 (watch for a day or two, add rows, run the move)
  and OYP 3 (go up the chain, fan out, add rows, run the move). "Where you are now" makes
  the three-source result explicit.
- **C5, remove the time estimate.** Removed.
- **C6, C7, C8, fold D3 through D5.** D3 is Part 2 of the graded item with D4 as guidance
  inside it; D5's submission list merged into the graded item's "What to submit."
- **D1 deleted (tracked change).** Leslie: it half-matches criteria already given. Agreed.
- **A1 tracked changes** applied as written: "nudge" to "thing to consider," "thing" to
  "item," design note deleted.

## Calls made building v4 (Claude)

- Concept check defaulted to after OYP 3, where the teaching ends. Its six questions need
  re-verification against the v4 pages on both counts.
- Points: graded item at 35, absorbing the 15 from the Candidate List. Total still 100.
- The no-AI note kept in its narrow form inside OYP 1, marked open. Leslie's call.
- The "different path" line in the fan-out paragraph still open. Leslie's call.
- E and F carried verbatim except: the "Submission 2 of 2" line removed, cross-references
  to old section letters reworded, the resolved Introduction note under Check 4, and F5's
  list gaining the five-line candidate problems as its first item.

## Process

- **Review E and F in v4, not v3.** Check 1 reads off the "who is paying" line, and v4
  changes when that line gets written. Reviewing E against v3's D would be reviewing against
  a superseded input.
- **One working document, then a mechanical cut.** v4 stays in `course1/design/` with `##`
  headings as artifact boundaries, because one document reviews more easily than seven.
  The cut into `sprint-10/` artifacts follows the review; the cut plan is at the foot of v4.
- **Docx round trip, confirmed working.** Comments and tracked changes extracted by
  walking the document tree; every change applied individually and audited. The Markdown
  export Leslie tried first carried one flattened suggestion and no comments.

## Provenance for this session

Human (Leslie): the own-your-progress direction and every comment above; the ruling that
week 1 adopts Sathya's rhythm and other sprints decide later; cutting D1; asking whether
the OYPs build on each other, whether the process is the same in all three, and how far
under the items go, which exposed the uneven depth in v3; asking whether learners should
get under more than one item; asking where the longer list narrows to three to five, which
exposed the missing selection step.

AI (Claude): the comparison against Sathya's rhythm and the graded-item count as the real
divergence; the depth rule; the selection step and its "clearest, not most important"
criterion; the guardrails text; the placement of B5; the concept check default; the
drafting.

Still not validated with participants.

---

## 10 September, later: second review round, OYP 1 and the graded item through E1

Ten comments and tracked changes in seventeen paragraphs, returned as a `.docx` late in the
evening. Leslie got through OYP 1 and the graded item as far as "What the checks are for."
Everything from Check 1 onward is still unreviewed. All tracked changes applied
individually; four needed a punctuation repair where a suggestion left a fragment, noted
below. No structural rewrite this round, so nothing was lost to one.

**Tracked changes applied as written.** "We are going to do some pushing" is now "You are
going"; the table's report row became "Every analyst spends thirty minutes solving the same
formatting problem every month"; "the gap in column 3"; the graded item's opening paragraph
in Leslie's words; the "checks work better on a list you did not write ten minutes ago"
sentence cut from Part 1; "make a mental note of" and "set aside, but don't delete"; "not
necessarily the most important"; "we're looking for clear, meaningful gaps"; the
uncertainty paragraph in her words, which drops the forward links to Sprint 3's
confirmed/inferred marking and to half two's assumptions; the three E1 edits, including
"it is perfectly okay if some or most of your list doesn't survive"; and her replacement for
the "course, arriving early" paragraph.

**Repairs made while applying.** "If what you get on your first pass is still too vague ...
else. Run the move again" joined into one sentence. "Make a mental note of every row where
you were able to get underneath successfully. Where the middle column ..." joined with a
colon. "Not the necessarily the" de-doubled. "OYPs" in participant text written out as
"the own-your-progress activities," since the abbreviation is ours. "3-5" written as
"three to five."

**Consequential fix.** The OYP 2 teaching example said the report took twenty minutes;
the table now says thirty. Harmonised to thirty. Check 4's diagnosis table still says "the
export format for my monthly report is wrong," which is the same case and still reads.

**C0 and C1, the three-pass example.** Leslie: the answers did not sound like a human, and
the moves between passes skipped logical steps. Rewritten. Pass 1 uses her sentence nearly
verbatim. Between each pass there is now a short paragraph naming what the answer did and
did not say, and which part to ask about next. A closing rule states the move between
passes generally: find the part of your answer that says something happens without saying
who does it or why, and ask how that part works now. Claude's drafting, unreviewed.

**C2, the stopping rule referenced cost before it was introduced.** Fair. The rule now
points at the table's third column, which the learner has already seen: stop when the gap
is specific enough to write there, what is different from how it could be and who feels it.

**C3, do the table's gaps cover all three things the instruction asked for.** Honestly, no.
The rows name who and roughly what it costs, and leave the gap implicit. Rather than
rewrite three rows Leslie has already edited, the instruction was tightened to the two
things the rows do show: what is different from how it could be, and who feels it. Cost
arrives in Part 2, where it gets its own line.

**C4, "Five parts, one document at the end."** Rewritten as two plain sentences.

**C5, "second and third activities."** Named: Things You Stopped Noticing and Things
Somebody Handed You.

**C6 and C7, the candidate problem shape.** Leslie: not a paragraph; each problem needs a
title, which is the emerging gap from the table, then how it works now pulled from the
table, then a cost that can often be quantified, then the last two lines. Rebuilt as a
six-line labeled list. The worked example is now her report case with her arithmetic:
fifteen analysts, thirty minutes each, monthly, about forty dollars of time per fix, roughly
seven thousand a year. The handover example is gone from Part 2; Check 1's pass example
still uses it, and the handover row is still in the OYP 1 table, so nothing dangles. (?) at
the end of a line replaces the question mark at the end of a sentence, per C7, and the
worked example shows one.

**C8, Check 2 overlaps the "Right now" line.** Leslie flagged this before reading Check 2.
Not changed. An [OPEN] block at Check 2 records the overlap and one way through: make Check
2 an escalation of the Right-now line, the way Check 1 escalates the cost line, so the test
becomes whether the line names the mechanism and the exact place it stops working. Her call
once she reads the check.

**C9, "They are the course, arriving early."** Her replacement sentence drops it. Applied.

**Lost in this round, worth knowing.** The uncertainty paragraph no longer points forward
to Sprint 3's confirmed/inferred marking or to the assumptions in half two. The spine's
section 11 treats the (?) marks as the soft ancestor of confirmed/inferred. If that
continuity still matters, the pointer belongs in half two where the assumptions get named,
not here. Logged, not restored.

**Provenance.** Human (Leslie): every ruling above; the human-sounding pass 1 answer; the
titled-list shape and the quantified cost example. AI (Claude): the passes 2 and 3 text
and the between-pass paragraphs; the general rule for moving between passes; the C3
tightening; the Check 2 escalation idea, offered not applied.

---

# Session of 11 September 2026

## Is half one doing too much? Leslie's worry, Claude's read

**Leslie's concern.** That practically the whole course is covered in the first half of
Sprint 1.

**Claude's read, accepted as the frame for the next round.** The arc holds: half one does
Sprint 1's work and none of Sprints 2 through 5's. What it does is teach every later
sprint's criterion at verification depth when the spine sets the bar at honest looking.
Each check runs three to six hundred words with a failure taxonomy and a recovery move.
The time estimate for half one as written, five to six hours, already exceeds the
Introduction's four-to-six-hour budget for the whole sprint. Proposed cuts, each with a
destination:

1. **Part 4, the AI exchange.** Its job is Sprint 2's capacity and Sprint 3's
   confirmed/inferred; Sprint 1's AI capacity is widen, which half two's Dojo Lab does.
2. **Two of Part 2's six lines.** "This has been going on" is Check 3 in other words;
   "It has not been fixed because" is a cause hypothesis, Sprint 2's work. Title, right
   now, it could, cost are the course's own definition of a problem.
3. **Each check cut to the stated bar**: question, one pass, one fail, what failing tells
   you. Scale tables, failure shapes, the diagnosis table, and the re-run instruction move
   to the sprints that test those checks.
4. **"What would make you switch" in Part 5.** The spine puts the switching message in
   Sprints 2 and 3 where it is actionable.

Leave alone: the three OYPs, the four check names, commitment with reasons and why-you.

**Not yet ruled on.** Leslie had already made a third review pass before this exchange
and asked Claude to sort her edits against it rather than redo them herself.

## Third review round: twelve tracked changes and one comment, sorted against the cuts

Eleven of twelve are compatible with the cuts, and most trim in the same direction. All
eleven applied individually as written: the "What the checks are for" rewrite in her
words, with the "hour now" sentence moved up and the "course, arriving early" residue
gone; "one thing to keep in mind" for "one warning"; Check 1 losing the "cannot be
unreachable" hand-off and gaining "a result to make note of"; Check 4's "doesn't
necessarily kill anything, but it makes you think about how the scope may need to change"
and "the trickiest check"; "Pick one" in her softer register, dropping "disposable on
purpose."

**C0, "Run all four on each candidate": where, and what does it look like?** Answered
with a per-candidate block, drafted by Claude: title, four checks each with an answer and
a verdict, Check 4's verdict being right size / too small, go up / too big, go down. Same
document as Parts 2 and 5, so one submission. Unreviewed.

**The one conflict: Part 4.** Leslie's edit keeps the AI exchange and reframes its opening
in Welcome V2's Human Value terms ("you have brought a lot of your human value and insights
to the first stage"). Claude's assessment the same morning named it the clearest cut.
Her wording is applied and an [OPEN] block at Part 4 records both positions. Her call.

**Consequence worth noting.** Her Check 4 edit ("doesn't necessarily kill anything") and
the C0 template's verdict line ("too small, go up / too big, go down") already move the
check toward a two-line calibration, which is what cut 3 asks for. The remaining depth in
Checks 1 through 4 is the diagnosis table, the three failure shapes, and the re-run
instruction, all untouched by her pass and all still on the cut list.

**Provenance.** Human (Leslie): the too-much worry; every edit above. AI (Claude): the
arc-versus-depth diagnosis, the time estimate, the four cuts and their destinations, the
check block, the Part 4 flag.

## 11 September, later: the four rulings, applied as v4.2

**Leslie's rulings.** (1) The AI exchange moves to half two, with "we can always add it
back." (2) Cut the check depth. (3) Part 2 down to four lines. (4) Drop "what would make
you switch."

**Applied.**

- **Part 4 is gone from the graded item**, which now has four parts. Its text, with
  Leslie's 11 September opening, sits in a "Parked for half two" section at the foot of the
  draft. The submission list loses the AI-exchange bullet. The Dojo and API key decision
  still governs it wherever it lands.
- **Check 3** keeps question, why it matters, the test, and the pass/fail pair, and closes
  with one sentence on what failing tells you. The three failure shapes are parked, with
  Sprint 3 as the suggested destination.
- **Check 4** keeps Leslie's edited opening and why-it-matters, the three tests, the
  household version, and the too-small and too-big descriptions. Cut: the paragraph
  mapping the three tests to later sprints (parked, suggested destination the spine),
  the diagnosis table and the re-run-all-four rule (parked, suggested destination half two
  or Sprint 2). In their place, one paragraph: too small, ask what it is an instance of;
  too big, pick one instance; note the change; size gets looked at again in the frame.
- **Part 2** is title, right now, it could, the gap costs. The worked example loses its
  last two lines and the (?) moves to the "it could" line. The guess line now names "it
  could" and "costs."
- **Part 4 (Commit)** loses the switch line from the worked example, the bullet, the
  "notice what that does" clause, and the submission list entry.

**Not cut.** Check 1's pass/fail table and blockquote pair, since Leslie restored the table
herself on 9 September and edited the section on 11 September. Check 2, since she has not
read it and it carries the overlap flag. "Reading the results" (murky, wrong size, passes
cleanly), which is short and is the reading guide for the check block.

**Time estimate after the cuts**, same rough method as the morning's: the graded item
drops from about three hours to about two, and half one from five to six hours to about
four to four and a half. Still over the Introduction's budget for the whole sprint once
half two is added. The Introduction's four-to-six-hour line is now on the owed-edits list
as a number to revisit, not a target to hit.

**Provenance.** Human (Leslie): all four rulings. AI (Claude): the trims, the parking
section and its suggested destinations, the replacement sentences.

## 11 September, later still: the test edition went to Leslie for Melisa and Clare

**Leslie's ruling.** Send now, before her own pass over the remaining sections, on the
argument that participant-mode failures will say more about Check 2 than rereading it.

**What was built.** Six Word files from v4.2 as merged (commit a1c9161), one per Canvas
item plus a read-me-first: the Introduction (from its sprint-10 artifact, with the Next
line pointed at the first activity), the three own-your-progress activities, and Test and
Commit. Each `##` section became one file; design notes, open flags, and the parked
section were stripped; the mermaid diagram became a one-paragraph description with a note
that a diagram replaces it on Canvas; the video TODO became an italic placeholder. The
module header and the concept check appear as placeholder rows in the read-me-first
rather than as empty files.

**The ask, as written on the cover.** Do it, do not review it, on your own real situation.
Record time per page, every stall, and everything you produced. Do not fix the text. If a
page says submit, keep it in your own document. Send it all to Leslie untidied.

**Not in the repo.** The packet is a generated review artifact, not course content, so it
lives with Leslie. Rebuilding it is mechanical from the draft's `##` boundaries.

**Known rough edges shipped on purpose.** Check 2 still carries the overlap question in
the design notes (stripped from the packet) and Leslie has not read it; the trims from
earlier today are unreviewed; the Introduction's Week 1 bullet and Time Guidance still
describe the sprint in pre-v4 terms.

---

# Session of 12 September 2026: Jeremy's return, the team plan, and the next two outlines

## What changed while we worked

Jeremy returned on 8 September after six weeks away and, between 8 and 11 September, built
a document-intake pipeline (docx to artifact, with a `.sources.json` evidence file beside
each artifact), ported Sathya's four writing skills, cut the v4.2 half-one draft into seven
artifacts in `course1/sprints/sprint-12/`, wrote a six-question concept check, built a
`guided_assignment` delivery mode with browser-saved response boxes and a copy-into-Canvas
step, and published the whole first half to Canvas course 180 as module 2079 with an
ungraded assignment group. He then published every V2 module, retired the Working Draft and
smoke test, and ran a Student View audit. The participant prose in sprint-12 is v4.2's,
unchanged; his additions are submission guidance, the diagram redrawn for mobile, and the
Introduction's owed edits. `sprint-10` no longer exists.

Open items from that review, for Jeremy: whether his source-evidence validation permits
direct edits to artifact bodies; the homepage line "Work without AI in this half," which
states a rule Leslie has not made; whether course 180 is test or production; and the AI
proxy outage that blocks the Sprint 4 AI Exchange and will block half two's Dojo Lab.

## The team plan (Leslie, 11 September)

Leslie: Sprint 1 half two and Sprint 2. Jeremy: review and edit Sprint 1 first half, then
Sprints 0, 3, and 4. Melisa: run the first half as a participant. Rubrics and point values
decided soon. Target: a solid whole course in four days (15 September), six days of edits
with Clare, share with the instructor on 21 September, later move to the De Anza Canvas.

Flagged, not resolved: Sprint 5 has no owner; Sprint 2 is the largest unbuilt piece and its
subject is directing AI while the AI proxy is down.

## Rule: the artifact is canonical once cut

**Leslie's ruling, 12 September.** The moment content is cut into artifacts, the artifact is
the source of truth and the design draft is frozen as record. `sprint-1-half-one-working-
draft-v4.md` is frozen at v4.2. Half two and Sprint 2 are drafted in `course1/design/`
until they are cut, then the same rule applies. The decisions log remains the record for
design rulings; Jeremy's authoring and publication records remain the record for builds.

## Two outlines written, prose not started

`sprint-1-half-two-outline.md` and `sprint-2-outline.md`, both in `course1/design/`, both
for Leslie's review before any prose. Each ends with its decisions. The half-two outline
recommends extending the week-1 own-your-progress rhythm into week 2 and folding the parked
AI exchange into the Dojo Lab. The Sprint 2 outline gives Sprint 2 the think-first artifact
the spine says it lacks, makes Check 2's widening its first Dojo Lab, states the switching
rule where it is actionable, and names the Confirmation Plan as the hand-off Sprint 3 V2's
stakeholder map already asks for. Every AI activity in both is written to run in any
chatbot, because of the proxy outage.

**Provenance.** Human (Leslie): the team plan and dates, the canonical-artifact ruling. AI
(Claude): the review of Jeremy's work, the flagged questions, both outlines.

## 12 September, later: Jeremy's rewrite is canonical; half two drafted to its register

**What happened.** On 11 September, with Leslie's go-ahead that length was the major
concern, Jeremy and his agent rewrote all six first-half artifacts in sprint-12: body text
from about 9,100 words to about 2,700, a compact single-column layout with the response
box directly under the teaching, and three AI-generated illustrations. Merged as PR #54 and
published to Canvas module 2079 the same evening. Only one line per page survives verbatim
from v4.2.

**Leslie's ruling, 12 September.** Accept it as the canonical text and take a pass at it;
the direction is right and it likely needs tweaks. The arc was checked element by element
against the live text and is intact: one table across three sources, the move with a second
pass, indicators, self-issued requests, the why-chain and fan-out, the day-or-two watch, the
three-to-five selection, the four-line shape, (?) marks, all four checks with verdicts
including "cannot answer yet," knowledge-holder and household conditions, Check 4 as a scope
change, commit with why-you, runner-up, and recovery. Concept check at position 6.

**Meaning-level changes for Leslie's pass**, as distinct from wording:

1. "Work without AI" now appears on the Introduction, the concept check, and Test and
   Commit. The ruling was the narrow version, first activity only, still open.
2. The bored-sole-survivor exit in commit is gone; his text has "or the only survivor does
   not matter to you," which covers it more briefly. Probably fine.
3. The "try on" register is gone. Nothing says candidates are expected to be dropped
   except "set clear failures aside."
4. No explicit carry-forward line beyond "keep your full table and final answers for the
   framing work that follows." Adequate.
5. Curly quotes appear in his text, against house style.

**Half two drafted** as `sprint-1-half-two-working-draft-v1.md`, in his register and at his
length, on the outline's recommended defaults: OYP rhythm in week 2, First Frame and Dojo
Lab ungraded, Goal Plan 50, Reflection 10, AI exchange folded into the Dojo Lab. Each
activity carries its response tasks with criteria so the cut is mechanical. Roughly three
hours of participant time.

**Process line added to the rule.** An artifact rewrite that changes participant prose goes
to the content owner before it merges, with the publish held until they have read it. Not
yet agreed with Jeremy.

## 12 September, evening: the response box problem and the Candidate Log template

**The finding.** Jeremy's guided assignments render each first-half activity as one large,
unlabeled, placeholder-less text box, with the mechanics (drafts save in the browser, copy
does not submit, paste into Canvas) explained below it. The three table activities ask for a
three-column table in a plain text field. Test and Commit has four boxes, one per part, and
is better, but Part 2 asks for three to five four-line candidates in one box. Sathya's pages
use one small box per question with the question as its label.

**Direct edits are not possible.** Tested: a one-sentence prose change and a task-config
change to a sprint-12 artifact both fail validation with "edit the build map and rebuild."
The build map and source packet are in Jeremy's private, git-ignored intake directory.
Placeholder text is not a feature of the task schema or the renderer. The compact layout
allows exactly one box. Every first-half change therefore routes through Jeremy until he
changes the fidelity check or provides an accept-edit command. Asks recorded for him: that
command or a warning-level check; a placeholder field; a multi-box presentation; the
how-this-works line above the first box.

**Leslie's ruling: the Candidate Log as a Google Doc template.** Of five options (template
document, boxes that assemble into a table, fixed row boxes, Canvas's own table editor, a
spreadsheet), the template needs no code and is the Candidate Log ruled on 9 September.
Built 12 September and placed in Leslie's Drive as "Candidate Log (Sprint 1) - TEMPLATE,
make a copy," Google Doc id `1aTgaDgf1ugkQujJkgvo-EHXUqm9ztN1jMA5SDy3lTjI`. Parts: A, the
three-column table with one example row and the set-aside rule; B, the request chain;
C, Test and Commit's four parts with three candidate blocks and three check tables; D, the
first frame's seven parts for half two. Rough-is-the-point and (?) conventions in the header.

**Still to do.** Leslie sets the sharing to anyone-with-link, view only. Jeremy links it from
the three table activities and from Test and Commit, with the response box instruction
becoming "paste the section this activity names, or a link to your Candidate Log." Option 2,
boxes that assemble into a table, stays as the medium-term ask.

## 12 September, late: the five open items, and a finding that changes two of them

**Finding.** A new artifact written directly into `course1/sprints/sprint-12/` with a full
`guided_assignment` configuration (two labeled response boxes, `presentation: reading`,
criteria, instruction sections) and no source-evidence sidecar passes validation. So does a
plain page. The source-fidelity lock applies only to files that carry `source_provenance`,
which today means the six first-half artifacts Jeremy built through his intake. New content
does not need his intake to reach Canvas: write the artifact, open a PR, Leslie approves the
merge, the protected workflow publishes it as an unpublished Canvas item.

**The five items on the table, as Leslie listed them, with their status.**

1. **Workflow so that not everything routes through Jeremy.** Narrowed. Only the six
   first-half files are locked. Ask him to unlock them (accept-edit command, or the fidelity
   check as a warning), or to drop the sidecars once the content is stable.
2. **Assignments more guided than a blank box.** The Candidate Log covers the table work
   for the four first-half assignments and the first frame. Prose-shaped parts, Test and
   Commit's four parts and everything in half two, belong in short labeled boxes, which the
   `reading` presentation supports and which Claude can write directly for new pages. The
   live first-half pages still need Jeremy to link the Log and relabel the box.
3. **Too much guidance stripped from the first half.** Sathya's answer is not a separate
   instructional page. His activity pages keep a short visible backbone and put worked
   examples, reference, and method one click away in collapsed sections on the same page:
   backbone visible, detours behind clicks. Jeremy's layout has the same mechanism ("Read the
   full instructions and examples") and his compact pass hid it. The fix is to restore the
   v4.2 teaching, frozen in the repo, as collapsed sections inside each activity. A
   presentation change on locked files, so Jeremy's, and the most useful single ask.
4. **Half two.** Not a docx. Claude converts `sprint-1-half-two-working-draft-v1.md` into
   five sprint-12 artifacts with boxes, criteria, and collapsed teaching, `publish: false`.
   Leslie reviews the real pages. Merge needs her go, per the rule.
5. **Sprint 2.** Same path, in the next storage folder. The only Jeremy dependency is an
   AI feedback button on the pushback box, if wanted, which needs the proxy restored.

**Jeremy's list shrinks to three:** unlock the first half, restore its teaching as collapsed
sections, link the Candidate Log from the four first-half activities.

# Session of 13 September 2026

## Half two, first review round: the frame page and Your first frame

Eight comments and one tracked change from Leslie, all on pages 8 and 9. They share one
cause: the frame page taught seven parts, then Your first frame opened with "Find the goal
underneath," the part the previous page had just said comes last, and nowhere did a learner
see a finished first frame. Fixed structurally; dispositions below.

- **C0, is "look widely, hold loosely" in the first half?** No. It was our design language
  from the 4 September session and never reached participant text, in v4.2 or in Jeremy's
  rewrite. Cut, replaced with a plain sentence about gathering several and keeping one.
- **Tracked change** on the frame definition applied as written: "It is as important to
  mark clearly what you do not yet know as it is to detail what you do know. You will spend
  the next eight weeks filling in the gaps of what you do not know. That is the point."
- **C1, "starting to sketch out."** Yes, more accurate for version one. Adopted.
- **C2, why lean on "disagree with it."** The intent was testability: a frame nobody could
  disagree with is too vague to check. The word read as argumentative. Now "specific enough
  that someone who knows the situation could tell you where you are wrong."
- **C3, is the report example big enough to carry through?** Better question than it
  looks. The live first half runs three cases: volunteer onboarding (first activity), the
  report (second activity and Test and commit's Part 2 example), and account handovers
  (the check examples and the commit example). The commit example chooses handovers. So
  the frame that follows must be the handover frame or the story breaks at the hinge.
  Switched, on both the frame page and the Goal Plan's example. Handovers also carry the
  people Sprint 3 needs: four managers, two clients, an account lead.
- **C4, should they start building it somewhere; the transition is abrupt.** Yes. The frame
  page now says which three parts the learner already holds and where, and the worked
  example shows a complete rough first frame with "I do not know yet" in it. Your first
  frame points at Part D of the Candidate Log as the place to build.
- **C5, "you have not gone far enough."** Judgment where an action was needed. Now: if
  your line names a tool or a process, ask what would be different once it existed, and
  write that. The frame page names the two solution-shaped traps (parts 5 and 7) once.
- **C6, are these instructions; what is the final output; would optional guidance help.**
  The prose was a draft of instructions with the output implied. Now the output is shown
  first (the worked frame), the steps follow the order people fill, and a NOTE specifies
  the collapsed "more help" content per step for the cut: the candidate beside the frame
  parts it feeds, two solution lines rewritten as states, a why-chain on the handover case.
- **C7, does "find the goal first" conflict with "the goal comes last"?** It did. Your first
  frame is reordered: carry over parts 2 to 4, write assumptions, say what fixed looks
  like, find the goal, name what to find out next. Step 4 says why the goal comes late.

Pages 10 to 12 unreviewed. Provenance: Leslie, every comment and the tracked change;
Claude, the restructure, the handover frame, the step order.

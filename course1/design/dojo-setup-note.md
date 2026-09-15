---
purpose: Put the course-wide Dojo setup on Jeremy's radar, from Leslie's 15 September test of the Sprint 1 Dojo Lab prompts
status: note, 15 September 2026, for Jeremy; nothing decided yet
depends_on: sprint-1-working-draft-v5.md (the Dojo Lab), Sathya's CST499 Dojo material in Common-Curriculum
---

# The Dojo as a course-wide tool: what we found and what needs building

Leslie tested the Sprint 1 Dojo Lab prompts on her own problem frame in ChatGPT on
15 September. The test raised the tool question for the whole course, and the answer
turns out to be a thing that has to be created once and maintained, not a thing to
configure per activity. This note is what Jeremy needs to look into.

## What Sathya's Dojo is now

Not a separate app. For CST499 the Dojo is the learner's own ChatGPT, Claude, or Gemini,
set up once as a project (a Gem, in Gemini) with two things:

1. **A one-paragraph project instruction**, pasted once. It says: you are my Sensei, a
   metacognitive coach; at the start of every chat read the Dojo tab of the Google Doc in
   this project and follow it as your instructions; always read the latest version from
   Drive, never a cached copy; read all the tabs; if you cannot read the document, say so
   before we start. The exact text is on `cst499/setup-your-ai-dojo.html` in
   Common-Curriculum.
2. **One Google Doc, linked by its Drive link**, with three tabs:
   - **Dojo.** The core method (`common/dojo/dojo-core.txt`, v1.13.0: one question at a
     time, replies under 120 words, ask for the learner's answer before offering its own,
     never rewrite, never decide for them, named characters such as Auditor, Challenger,
     Reflector, Writer, a recap at the end, an "evaluate the conversation" read on
     request), followed by **modules**, one per piece of work, written as numbered rounds
     that name which character runs each.
   - **Course.** The material, one page per item, each opening with a `Source:` line
     linking to the Canvas item so the Dojo can point learners at the page.
   - **Syllabus.** Policies, schedule, grading, what is required.

The Drive link matters: the doc is edited through the semester and a linked doc updates
with it, so prompts and modules can be fixed without touching Canvas or the learners'
projects. Setup is Sathya's first assignment, about ten minutes, and the check that it
worked is whether the Dojo comes back short with one question rather than an essay.

## How this differs from what course1 points at today

The Sprint 3 and 4 Dojo Labs link to the older built Symbiotic Thinking Dojo: personas
(@framer, @reflector, @auditor), a Gemini API key configured in the browser, "Learn +
Solve mode," a JSON export the reflection uploads. The tutorials page still carries
"[TEAM DECISION: API key via the built Dojo, or converting your own chatbot]" and three
[TODO] setup pages. The newer path needs no API key, which is the thing that has been
blocked since Sprint 0.

## What Leslie's test showed

- The bare Sprint 1 test prompt, run one-shot in ChatGPT, produced about 1,400 words: a
  full audit of every claim. It found the right things (the empty 4b, a prediction that
  was really a causal bet, costs with no bearer, her own time uncounted) but at
  first-draft stage an exhaustive audit is the wrong ask. Most claims are unverified by
  design; the course exists to check them.
- A capped version (readiness verdict, three ranked findings, one question) came back at
  about 150 words and was right.
- Working the findings one at a time in a plain chat needed explicit instructions to
  label each finding and not to move on until the fix was written, and it still moved on
  early once. Every one of those instructions is already in the Dojo core method.

Conclusion: the conversational discipline belongs in the core, the frame-specific
standard belongs in a module, and the activity page should get shorter, not longer.

## What has to be created

1. **The course doc** for course1, three tabs, in Leslie's or a CTI Drive, shared
   anyone-with-link view. Dojo tab: the core text plus our modules. Course tab: the
   material with `Source:` lines. Syllabus tab: whatever the Canvas syllabus says. The
   Course tab is the piece with a pipeline question in it: it is the same content as the
   hosted HTML, so it could be generated from the markdown on publish rather than
   maintained by hand.
2. **One module per Dojo Lab.** Sprint 1's is drafted (Problem Frame Dojo, four rounds:
   readiness, fix one at a time, widen, move on; in the decisions log, 15 September).
   Sprints 2, 3, and 4 need theirs, converted from the persona prompts on the current
   pages.
3. **A Sprint 0 setup item**, mirroring Sathya's, replacing the three [TODO] tutorial
   pages and the API-key path. Sprint 0 is Jeremy's.
4. **The Dojo Lab pages** rewritten to "open your Dojo, say what you are working on, paste
   your work, work the rounds, submit the recap."

## Questions for Jeremy

- Has he seen Sathya's newer setup (the project plus linked doc), and is there anything
  in the Canvas pipeline that assumes the built Dojo (the JSON upload for reflections,
  the "Open the Symbiotic Thinking Dojo" links)?
- Can the Course tab be generated from the repo on publish, the way the hosted HTML is?
- Who owns the doc, and where does it live so that all three of us can edit it?
- Does the ai_activity reflection (JSON upload from the built Dojo) survive if learners
  are in their own chatbot instead? Sathya's answer for CST499 is a "reproduce our entire
  conversation as one message" prompt pasted into a Canvas text box.

## Provenance

Human (Leslie): the test, the two findings about length and about resolving one item at
a time, the ask to put this on Jeremy's radar. AI (Claude): the reading of Sathya's Dojo
material, the module draft, this note.

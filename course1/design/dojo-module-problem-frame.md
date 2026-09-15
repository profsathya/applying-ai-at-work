---
purpose: The Sprint 1 Dojo Lab as a module for Sathya's Dojo core method, in his module format
status: v0.3, 15 September 2026, PARKED after three test runs on one frame; resume when the course-wide Dojo doc exists and a second person's frame is available
depends_on: dojo-setup-note.md; Sathya's dojo-core.txt (Common-Curriculum, common/dojo/)
---

# Problem Frame Dojo module, v0.3

Written to sit in the Dojo tab of the course doc after the core method, the way Sathya's
resume and search-strategy modules do. Plain text below is the module as pasted; the notes
after it are what three test runs taught.

```
PROBLEM FRAME DOJO - module (v0.3, use with the Dojo Core)

This module makes you my problem frame tester. I have written a first draft of a problem frame. Most of my claims are unverified, and that is expected, because the next nine weeks of the course are for checking them. Your job is to tell me whether the frame is a good enough starting point and to make me fix the few things that would stop it being one. You behave per the Dojo Core; the rounds below are your method.

What is mine vs what you carry

The frame is mine: every sentence in it stays in my words, and you never rewrite a part or suggest a solution. You carry the standard: the seven-part frame on the frame page in the Course section below, the three claim kinds (checkable, prediction, causal bet), and the rule that part 5 is a changed state and never a solution.

The rounds

1. Readiness (Auditor). Read my frame against the frame page. Tell me in one line whether it is specific enough to be a starting point, yes or not yet, with one reason. Then name the three findings that matter most before I move on, ranked, one line each, quoting my words and naming the part. Look especially for a cost with nobody attached, a solution hiding in part 5 or 7, a causal bet labeled as something else, and a part still empty. Then ask me one question: does that ranking match my own sense of where the frame is weakest? Wait for my answer before Round 2.

2. Fix, one at a time (Challenger). Take the findings in order. Begin each question by naming the finding in a few words. Ask one question, then stop. When I answer, say in two or three lines what my answer settles and what, if anything, is still missing. At most one follow-up question per finding; then move on. This is a first draft, so when my answer settles the finding well enough to carry forward, say so and move on. Do not press for precision the next nine weeks will supply, and do not ask me to reword a part unless the finding was about the wording. If the fix is more than a line or two of work (an empty part, the whole claims audit), do not do that work here: tell me in one line what to go and do in my Candidate Log, and move to the next finding. My Log is where the frame lives; ask me to keep it open beside this chat and make every change there. Before you leave each finding, make me say the actual change I will make in the Log.

3. Widen (Framer). Give me three other ways to see the same situation, two lines each: what it makes visible that my frame does not, and who would have to be involved. Ask me which one, if any, changes my frame and what I would change. Then tell me in one line whether any of them suggests this problem is already handled somewhere I have not looked.

4. Move on? (Sensei). One line: is the frame ready to carry forward. Then the recap I can keep: what I changed, what I chose to leave unverified, and what I should check first.

Start here

Start as the Sensei: greet me briefly, ask me to paste my frame, and begin Round 1. One question at a time.
```

## How to run it as a test without the project setup

One clean chat. Type this line in the message box, then paste under it, in order: the
core text, the module, the frame page from v5.1 and the three claim kinds (as a Course
section), then send. Paste the frame as the second message.

    Follow the attached text as your instructions for this chat. Read all of it, then begin as its "Start here" says.

The line has to be typed, not pasted: ChatGPT turns a long paste into an attachment, and
an instruction inside an attachment reads as a document to ask about.

## What the three runs on 15 September taught

1. **The bare one-shot prompt over-delivers.** About 1,400 words auditing every claim.
   The capped ask (readiness verdict, three ranked findings, one question) came back at
   150 words and was right.
2. **"Nothing else yet" kills the closing question.** The core wants every reply to end
   with a question; a module line that says stop wins over it. Round 1 now ends with a
   question about the ranking.
3. **"Do not move on until the fix is written" over-corrects.** Challenger held Leslie on
   one claim through four turns of real but stage-irrelevant precision ("do you mean no
   report exists or that you checked what each person knows"), then asked her to reword
   part 2. Round 2 now allows one follow-up per finding, says good enough for now is
   good enough, and never asks for a reword unless the finding was about wording.
4. **A finding whose fix is a whole part gets sent to the Log, not run in the chat.**
   The third finding was "the audit is incomplete," and Challenger began the audit one
   claim at a time. That is First frames step 5, desk work.
5. **The frame must live in the Log, not the chat.** Leslie asked "what is my current
   wording?" mid-run. The page and the module now say keep the Log open beside the chat.
6. **Round 1 works.** Under 100 words, Auditor named, source cited, the same top two
   findings as the one-shot run, and a third that was better (a solution wearing a
   claim's clothes in part 6).

## What is untested

Rounds 3 and 4. A frame that has been through the audit (all three runs used a frame
with part 6 unstarted, a harder case than participants will bring). Anyone's frame but
Leslie's. The real project setup with a linked doc instead of a paste. Claude and Gemini.

## Provenance

Human (Leslie): the three runs, the two findings about length and about holding on a
finding, the pause. AI (Claude): the module and its revisions, the packet, this record.

## For v0.4, when the work resumes (Leslie's question, 15 September)

Leslie asked whether the Dojo could track the changes as they happen, or hand back the
updated parts, so that people update the Log themselves (which forces the work) but AI
helps once wording is agreed. That is the core's Writer rule applied to the frame. Three
options were considered; the middle one is the recommendation:

1. Manual only (v0.3 as written).
2. **Read-back.** In Round 2, once the participant has said the change, the Dojo hands
   back the exact line or row to paste, in the participant's words, and nothing else;
   where no words were given for a slot it leaves [your words here] rather than filling
   it. In Round 4 it hands back the whole frame with only the agreed changes, each changed
   part tagged [changed], to paste into Part D of the Log as version two. The tags are
   the diff, and they feed Goal Plan Part 2 and the Reflection. Works in any chatbot.
   Reflector's "that is my read you are echoing" guards against rewording.
3. A live side document (ChatGPT Canvas, Claude Artifacts, Gemini Canvas). Best to use,
   worst fit: differs by tool, moves the frame out of the Log, and does not protect
   version one, which the Reflection needs unedited. Allowed as an extra, not the default.

Consequence for the draft: the participant leaves the Dojo Lab with version two already
drafted and marked. The Goal Plan page should say "rewrite the frame with every change
you made in the Log during the Dojo Lab," not "with everything the Dojo Lab changed."

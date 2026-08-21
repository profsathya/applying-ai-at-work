---
type: discussion
title: Learn and Verify
slug: learn-and-verify-v2
artifact_id: course1-sprints-sprint-4-close-the-learning-gap-v2-learn-and-verify-v2
sprint: 8
week: 7
module: 'Sprint 4: Close the Learning Gap (V2)'
position: 5
points: 50
submission_type: file_upload
delivery_mode: ai_activity
publish: false
ai_activity:
  activity_id: course1-learn-and-verify-v2
  version: "1.0"
  title: 'Learn and Verify: Sharpen Your Checks'
  description: Use AI follow-up questions to test whether the two checks you designed can actually come back negative.
  questions:
    - id: q1-sharpen-your-checks
      type: ai-discussion
      prompt: >
        Share both claims your frame will rest on, the check you designed for
        each, and the result that would tell you the claim is wrong. For the
        human check, name the person's role and the one question you plan to
        ask them.
      placeholder: >
        Include both claims stated so they could be false, what you will check
        each one against, the failing result you wrote down before looking, and
        the role of the person you will ask.
      minLength: 120
      numQuestions: 3
      aiContext: >
        This is Sprint 4 of Reframing Problems with AI. The participant is
        testing whether their verification checks are real before spending a
        week relying on them. Diagnose each check as circular (an AI
        explanation checked against another AI explanation), unfalsifiable (no
        result would change their mind), or vague (no named source they could
        actually go to). Push for an independent source and a named failing
        result. Do not run the checks for them and do not supply the answers.
      generateButtonText: Get Follow-up Questions
      loadingText: Generating follow-up questions...
      discussionPrompt: >
        Use these questions to sharpen both checks. Your final response should
        state each claim so it could be false, name an independent source, and
        name the result that would show you were wrong.
      summaryLabel: Your Sharpened Checks
      summaryPlaceholder: >
        Rewrite both checks. For each, give the claim, the independent source
        you will check it against, and the result that would make you change
        your mind. Confirm which check involves a person.
      saveButtonText: Save Response
      updateButtonText: Update Response
      digDeeperText: Dig deeper with AI guidance
rubric:
  - description: Checks were revised after AI diagnosis, and each names a result that would show the claim is wrong
    points: 7
  - description: The learning path is reported as actually run, with named sources and where it changed
    points: 6
  - description: Everything claimed as known is marked confirmed or inferred, and the marking is honest
    points: 7
  - description: Both checks are logged with claim, original source, independent source, and what came back
    points: 8
  - description: One check involved a person, named by role and date, with what they said in their terms
    points: 5
  - description: 'AI is used as learning infrastructure rather than an answer machine: the prompts show direction, and what AI produced was judged rather than accepted'
    points: 6
  - description: Goal Plan revision responds to evidence; a confirmed frame is reported honestly
    points: 6
  - description: Human judgment is visible in what was prioritised and what was set aside
    points: 3
  - description: What remains uncertain is named
    points: 2
---

# Learn and Verify

Now run the path you designed. Use AI as much as you want for the learning itself. That's what it's good at. The constraint is on what you're allowed to call known at the end.

This activity has four parts: sharpening your checks, setting up the one conversation, doing the learning, and documenting what you found.

## Part 1: Sharpen Your Checks

Before you go looking, use AI to test whether the two checks you designed in the Dojo Lab are real. The point is to catch a check that can't fail before you spend a week relying on it.

### What a Weak Check Costs You

Say your frame assumes: "New hires wait nine days for system access."

**Check A (weak):** "I'll verify the nine-day figure with documentation."

There's no way for this to come back negative. Documentation for the ticketing product will describe how the product measures things in general, which will match what you already believe, and you'll finish more confident and no better informed. It confirms rather than tests.

**Check B (strong):** "I'll look at our own admin console to see how ticket age is calculated, and ask the service desk lead what actually happens to a ticket that gets reassigned. If reassigned tickets are closed and reopened as new ones, the nine days is undercounting and I have to re-measure before I take this anywhere."

This has an independent source, and it names the result that would make you wrong. It can also produce the outcome that's most common and most useful: not confirmed, not contradicted, but complicated.

Check your own two against that pattern before you run them.

1. **Write your starting draft.** Both claims, both checks, the failing result for each, and for the human check, the person's role and your one question.
2. **Generate AI follow-up questions.** Start the AI activity below. Use the questions to diagnose your draft. Look for places where the response reveals that your check is:
   - **Circular:** the independent source isn't independent, an AI explanation checked against another AI explanation.
   - **Unfalsifiable:** no result would make you change your mind.
   - **Vague:** "documentation," "an expert," "the team," nothing you could actually go do on a Tuesday.
3. Use the deeper AI guidance button if a check still can't come back negative.

When you're done, copy or download the JSON response file from the activity. You'll submit it with your report at the end.

## Part 2: Set Up the One Conversation

This is lighter than Sprint 3. You aren't running a validation conversation. You're asking one person one question, and fifteen minutes is usually plenty.

- Send the ask at the start of week two, before you know exactly what you'll want to ask. Refine the question while you wait. Keep the ask short: who you are, that you're checking one specific thing, that it should take about fifteen minutes, and two times that work. A specific question is much easier to say yes to than "can I pick your brain."
- Your Sprint 3 stakeholder is a fine choice if the claim is in their area. A follow-up to someone who already talked to you is the lowest-friction version of this.
- No reply in three days? Follow up once in the same thread and offer to send the question in writing instead.
- Still nothing by day five? Go to your backup. Note the switch, and note what the non-response tells you about access to this part of the problem.
- If the claim is genuinely one nobody at your organization can speak to, say so in your report and name who could. That gap in access is itself a finding, and Sprint 5 will want it.

## Part 3: Do the Learning and Run the Checks

1. Work the path from the Dojo Lab. Keep notes as you go rather than reconstructing afterwards, and specifically keep track of where each thing you now believe came from.
2. Keep the prompts you use to direct the learning. Not every exchange, just the ones where you were steering: setting the context, asking for a range rather than an answer, pushing back on something that sounded too clean.
3. If the path turns out to be wrong, change it and say so. Finding in step two that step three was unnecessary is the path working.
4. Run both checks. Take notes in the source's own terms. For the conversation, stay as close to the person's actual words as you can, without confidential details.
5. Fill in the verification log below as you go, not at the end.

### Verification Log

One row per check. Fill in the first three fields before you run it and the last two after.

| Field | What to record |
| :---- | :---- |
| The claim | Stated so it could be false |
| What told you it | AI, a document, a conversation, a number you saw |
| What would make it wrong | The result that would change your mind, written before you look |
| What you checked it against | Something independent of the source above. For the human check: role and date |
| What came back | **Confirmed**, **Contradicted**, or **Complicated**, and what specifically |

**Complicated** is the most common outcome and the one people round off to Confirmed. If the answer was "yes, but," write down the "but." That's usually the finding.

**A filled-in example.** *The claim:* our ticket system measures ticket age from creation to close, so the nine-day figure is the real wait. *What told me it:* the Dojo, and the vendor's general documentation. *What would make it wrong:* if the count restarts when a ticket changes hands. *What I checked it against:* our own admin console, and a fifteen-minute call with the service desk lead, 3 November. *What came back:* **Complicated.** The console does measure creation to close, but she says reassigned tickets are routinely closed and reopened as new ones, so nine days undercounts. Her estimate is closer to fourteen. That's her estimate, not a measurement, so it stays inferred.

## Part 4: Document What You Learned

After the learning and the checks, write a report with the following sections.

**The gap:**

- What you didn't know, and the decision that was waiting on it.

**What you did:**

- The path as you actually ran it, including where it changed and why.
- Sources, named. The actual ones, not "documentation" or "an article."
- Two or three of the prompts you used to direct the learning, and one line each on what you were trying to get AI to do.
- Roughly how long it took against your estimate.

**What you now know:**

- Each item, marked **Confirmed** or **Inferred**, with its source. Most will be inferred. That's correct.
- Your verification log, both checks, complete.

**What changes as a result:**

- **Goal Plan revision.** Open your Goal Plan and revise whichever part the learning touched: the problem statement, the assumptions, or the riskiest assumption. Paste the before and the after. Revise on evidence, not on interpretation. If the learning fully confirmed your existing frame, report that honestly and say what evidence would have changed it. A clear confirmation is a real and valuable result also.
- **What remains uncertain.** What you're still not ready to claim, and what would settle it.
- **What you decided, and what AI didn't decide for you.** Two or three sentences. What you prioritised and what you set aside, and why those were your calls to make. Name one thing AI got you to faster than you'd have got there alone, and one thing it told you that you set aside, along with what setting it aside cost you.

## Submission

Upload two files to this assignment: the JSON response file from the AI activity in Part 1, and your written report from Part 4.

## Portfolio Capture

This report is the learning-evidence section of your Sprint 5 **Integrated Problem Document and Readiness Report**. Your verification log carries over directly: what you marked confirmed is what your final argument gets to stand on, and what you marked inferred is what an honest final document names as still open.

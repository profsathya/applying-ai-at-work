---
type: assignment
title: Test and Commit
slug: test-and-commit
artifact_id: course1-sprint-one-v2-test-and-commit
sprint: 11
module: 'Sprint One: Find a Problem Worth Working On (First Half)'
position: 7
publish: false
points: 20
submission_type: text_entry
delivery_mode: guided_assignment
guided_assignment:
  version: '1'
  purpose: Use four checks to choose a problem you can investigate, then defend your
    choice, name a runner-up, and keep uncertainty visible.
  builds_on: Your Candidate List and the examples on Four checks for a workable problem.
    Keep the same candidate names across your responses so you can compare the results.
  standing_instruction: Complete the first four tasks from your own observations before
    using AI feedback. In each of those tasks, answer the named check for every candidate
    and label the candidates consistently. Keep ? marks wherever a claim is uncertain.
    Then use AI to challenge assumptions, make your own decision, and copy your final
    answers into Canvas. Guidance and reflection are self-checks, not extra submissions.
  feedback_endpoint: https://ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy
  tasks:
  - id: check-people
    kind: response
    prompt: Check 1. Are the people real and specific?
    criteria:
    - For every candidate, name the specific people or roles who pay the cost. Use
      names only in your private notes; use non-identifying roles in anything shared
      with AI.
    - Explain what you know about their involvement. Categories such as everyone or
      the team are not enough by themselves.
    - If you cannot name who is affected, write that as a result rather than inventing
      an answer. Note how you could find out; an interview is not required yet.
    reflection: Which person or role could tell you something about the current state
      that you do not already know?
  - id: check-current-handling
    kind: response
    prompt: Check 2. Is something already handling it, and falling short?
    criteria:
    - 'For every candidate, complete: X handles this today, but it does not ___. Name
      the person, process, or work-around and the remaining gap.'
    - Describe current handling rather than proposing a new solution. Include a concrete
      example when you have one.
    - If nothing appears to handle it, distinguish what you have observed from what
      you have not checked. Keep uncertainty visible.
    reflection: Who is absorbing the cost of the current arrangement, and which part
      of that claim is still a guess?
  - id: check-current-occurrence
    kind: response
    prompt: Check 3. Is it live right now?
    criteria:
    - For every candidate, say whether it is happening currently. Describe a recent
      instance you know about or state that you do not know when it last happened.
    - Explain whether you could observe it in the next two weeks. A past irritation
      or hypothetical future event does not supply current evidence.
    - Do not fabricate an event to make a candidate pass. Record the candidate as
      uncertain or set it aside when the evidence calls for that.
    reflection: What could you actually observe, rather than remember or imagine?
  - id: check-size
    kind: response
    prompt: Check 4. Is it the right size?
    criteria:
    - For every candidate, check whether you can describe how it works now in one
      paragraph, name at least one other person with a stake, and identify at least
      one thing you need to find out.
    - If it is too small, ask what larger pattern it is an instance of. If it is too
      big, choose one instance you have actually seen. Write any changed scope.
    - Read all four check results together. State whether the candidate fails, is
      murky, needs a size adjustment, or passes, and keep unanswerable checks visible.
    reflection: What could you still learn about this candidate that would change
      your understanding?
  - id: ai-challenges
    kind: response
    prompt: Record two or three challenges from your AI exchange, and your response
      to each.
    criteria:
    - After completing your own four checks, use the optional AI feedback on your
      responses or take your two or three strongest candidate gaps and check answers
      to an AI tool permitted for your context. Remove confidential details first.
    - Ask which claims you are asserting rather than knowing and where someone familiar
      with the work might disagree. Ask it not to choose the problem for you.
    - 'Record two or three challenges and your response to each: accept, reject, or
      investigate, with a reason grounded in what you know. Keep new uncertainty visible.'
    - If the feedback service is unavailable, your answers remain here and the self-check
      criteria still work. Use another permitted AI tool for the exchange if available;
      if you cannot complete the exchange, record the limitation honestly instead
      of inventing AI feedback.
    reflection: Which challenge changed your thinking, and which did you reject because
      you have direct evidence?
  - id: committed-gap
    kind: response
    prompt: Write your committed problem as a gap.
    criteria:
    - 'Choose the candidate that came through the checks in the best shape and write
      it using the five fields: Right now; It could; The gap costs; This has been
      going on; It has not been fixed because.'
    - Keep the gap grounded in the current situation and retain uncertainty marks.
      Do not turn the commitment into a promise to build a specific solution.
    - 'If nothing survived, say so and describe your next attempt: adjust the size
      of a candidate or go looking for another current work-around. Do not force a
      choice you do not believe in.'
    reflection: Does this still describe a gap you can investigate, or has a preferred
      solution slipped into the statement?
  - id: decision-reasons
    kind: response
    prompt: Why this one. Why not the others. What would make you switch.
    criteria:
    - Explain which checks made the chosen problem worth pursuing and why it can support
      further inquiry. Use your actual situation rather than importance alone.
    - Give one or two sentences for each alternative, naming the deciding check and
      acknowledging what the alternative had going for it.
    - Name one condition that would make you switch. If no candidate survived, explain
      the failures and why your recovery plan is the next reasonable step.
    reflection: What is the strongest reason for your runner-up, and why does your
      present choice still make sense?
  - id: runner-up
    kind: response
    prompt: Name your runner-up.
    criteria:
    - Name the candidate you would return to if your chosen problem became a dead
      end. One line is enough.
    - Keep any uncertainty marks visible. If no candidate is viable, state that and
      refer to the recovery plan you described rather than inventing a fallback.
    reflection: Could you return to this option without starting again from a blank
      page?
source_provenance: test-and-commit.sources.json
---

## Run all four on each candidate

Go through your list one at a time. A few sentences per check. Rough is fine.

Where you cannot answer a check, write that instead of guessing. "I do not know who else this costs" is a result, and a more useful one than an invented answer.

## Reading the results

Not every failure means dropping something.

- **Fails outright.** Nothing to name for Check 1, or it is a memory. Set it aside.

- **Murky.** You could not answer, but you can imagine finding out this week. Keep it live and note what you would need.

- **Wrong size.** Passes in principle but is too small or too big. Move it up or down and run the checks again on the moved version.

- **Passes cleanly.** Rarer than you expect. If more than two do this, look again, because you may be answering from assumption rather than knowledge.

Before sharing your work with an AI tool, remove names and confidential details. Use a tool permitted for your context and keep enough non-sensitive detail for it to challenge your reasoning.

## Take your checks to AI

Now bring AI in, and notice what you are using it for. Not to find problems, and not to run the checks. You have already done both. You are using it to find out where you answered from assumption instead of knowledge, which is difficult to see in your own writing.

Give it your two or three strongest candidate problems and your check answers, and ask something like:

Here are candidate problems I am considering and my answers to four checks. For each one, tell me which claims I am asserting rather than actually knowing, and where someone who works in this area would likely disagree with me. Do not tell me which to pick.

Then read what comes back critically. Some of it will be generic and worth ignoring, because it cannot see your situation. Some of it will land, and the ones that land are usually the places you wrote quickly.

**Record two or three challenges it raised and your response to each.** Your response can be "fair, I do not actually know that," or "no, I have seen this directly and here is how." Both are good answers. Only agreeing with everything is a bad answer, and so is dismissing all of it.

## Commit

### Pick one

This is the turn of the sprint. Everything up to here was disposable on purpose. From this point on, one problem gets the rest of your attention for nine weeks.

Pick the candidate problem that came through the checks in the best shape. Not the one you like most, and not the one that would be most impressive if you solved it.

### Say why it, and why not the others

Real choices are rarely clean. Here is what one looks like when two candidates both mostly passed:

I am going with the account handovers over the volunteer onboarding.

Both passed Checks 1 through 3. Handovers won on Check 4. For the volunteer problem I could only name one person other than me with a stake, our board chair, and she is hard to reach and would mostly tell me what she wants to be true. For handovers I can name four account managers and two clients, and I sit next to three of them.

The volunteer problem is arguably more important. I picked handovers because I can actually find things out about it in ten weeks, and I could not say the same for the other one.

What would make me switch: if the handover problem turns out to be one person's habit rather than a missing process, there is much less to find out than I think, and it becomes too small.

Notice what that does. It names the deciding check, it admits the choice was not obvious, it says out loud what the runner-up had going for it, and it names the condition that would reverse the decision. That last line is the one people skip and the one worth most in week five.

Write your own version:

- **Why this one.** Which checks it passed cleanly, and what makes it worth nine weeks.

- **Why not the others.** One or two sentences per candidate problem, naming the check that ruled it out.

- **What would make you switch.** One line.

### Name your runner-up

One line. Which candidate problem you would take up if this one turned out to be a dead end.

You will probably not need it. It costs nothing now, and it means that if something goes wrong in week three, you have somewhere to go that is not back to a blank page.

### If nothing survived

It happens, and it is recoverable.

Go back to your list first and look for something you set aside that was the wrong size rather than the wrong problem. Most apparent dead ends are size problems, and “Check 4. Is it the right size?” tells you which direction to move. If that genuinely does not work, go back to Two other places to look and spend two days hunting rather than recalling. Work-arounds are where the surviving problems usually hide.

If you get here, say so in your submission rather than forcing a choice. Committing to a problem you do not believe in is worse than being a few days late to one you do.

### What to submit

One document containing:

- **Your four checks**, run against each candidate problem, with unanswerable checks noted rather than guessed

- **Two or three challenges from your AI exchange**, and your response to each

- **Your committed problem**, written as a gap

- **Your reasons**: why this one, why not the others, and what would make you switch

- **Your runner-up**, one line

- **Your uncertainty marks**, still marked

Next week you take this one problem, find the goal underneath it, and build your first frame.

## Submission template

Draft one document with these sections, or use the response boxes. Copy your final answers into the Canvas assignment text-entry box and submit there:

1. **Checks by candidate:** Your four check responses for every candidate, including unknowns, any scope changes, and the resulting status.
2. **AI challenges and your judgment:** Two or three challenges the tool raised. For each, record whether you accept, reject, or need to investigate it, and why.
3. **Committed problem:** Your chosen problem in the five-line gap shape.
4. **Reasons:** Why this one; why not each alternative; what would make you switch. Name the checks and evidence that matter.
5. **Runner-up:** One line naming the candidate you would return to.
6. **Uncertainty:** Keep the `?` marks visible wherever a claim remains a guess.

If no candidate survived, describe what failed and your next attempt instead of forcing a choice. Save this document for later framing and conversations with people who know the current situation.

## How your work is reviewed

| Criterion | Points |
| --- | --- |
| Four checks on each candidate, with unknowns and scope changes visible | 5 |
| Two or three AI challenges with your reasoned response | 3 |
| A committed gap and defensible reasons addressing alternatives and a switch condition, or a well-supported recovery plan if nothing survived | 9 |
| A runner-up and retained uncertainty marks | 3 |
| **Total** | **20** |

The strongest work makes your reasoning visible. Agreeing with AI is not the goal; deciding what its challenge means in your actual context is.

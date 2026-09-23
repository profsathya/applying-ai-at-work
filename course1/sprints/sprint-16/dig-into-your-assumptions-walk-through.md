---
type: assignment
title: Dig into your assumptions walk-through
slug: dig-into-your-assumptions-walk-through
artifact_id: course1-sprints-sprint-16-dig-into-your-assumptions-walk-through
sprint: 16
week: 1
module: 'Sprint 2: Is This Problem Worth Pursuing?'
position: 3
points: 0
submission_type: text_entry
delivery_mode: guided_assignment
completion_requirement: must_submit
learner_labels: true
walkthrough_after: course1-sprints-sprint-16-dig-into-your-assumptions
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  export_filename: assumptions-walk.docx
  purpose: Walk every assumption in your Problem Frame, decide which are risky, and write
    the one check you will make this week.
  builds_on: Bring your Problem Frame from Sprint 1. Work without AI on this page.
  standing_instruction: Own your progress · 0 points. Submit to complete this module requirement,
    and keep the exported file for week 2.
  tasks:
  - id: the-walk
    kind: group
    prompt: Walk your assumptions, one row each
    instruction_section: Walk your assumptions
    repeat_count: 8
    layout: table
    repeat_labels:
    - Assumption 1
    - Assumption 2
    - Assumption 3
    - Assumption 4 (optional)
    - Assumption 5 (optional)
    - Assumption 6 (optional)
    - Assumption 7 (optional)
    - Assumption 8 (optional)
    fields:
    - id: assumption
      label: My assumption
      kind: text
      guidance:
        ask: One line from Part 6 of your frame, as you wrote it.
        example: All four managers are affected, not just the one I sat next to.
        avoid: Rewriting it into something safer than what you actually assumed.
    - id: questions
      label: Questions behind my assumption
      kind: textarea
      guidance:
        ask: What would you have to find out to know whether this is true?
        example: Are the other managers affected? All four? In the same way? How bad is it?
        avoid: One question that just restates the assumption with a question mark.
    - id: answers
      label: Different answers that could change my problem
      kind: textarea
      guidance:
        ask: Two or three ways the answer could come back, and what each would do to your
          problem.
        example: None of them see it, so I rethink the problem. Two do and two do not, so
          I dig into the difference. All do, so I proceed.
        avoid: Three answers that all lead to "so I proceed."
    - id: risky
      label: Risky?
      kind: textarea
      guidance:
        ask: Could an answer end the problem? Write "could end it, because," "accepted, because,"
          or "not yet."
        example: Could end it. If only one manager sees this, it is one person's habit.
        avoid: '"Accepted" with no reason, or marking every row risky.'
    criteria:
    - Give every assumption from Part 6 a row.
    - Write at least one question behind each assumption.
    - Vary the different-answers lines rather than repeating one formula.
    - Give a reason with every "accepted."
    - Write "nothing much" where that is the honest answer.
  - id: your-check
    kind: group
    prompt: Choose one to check, and write it before you look
    instruction_section: Choose one to check
    repeat_count: 1
    layout: table
    repeat_labels:
    - The one I will check
    fields:
    - id: assumption
      label: My assumption, stated so that it could be wrong
      kind: textarea
      guidance:
        ask: Which row, in a form that a real answer could contradict.
        example: Account managers see account handovers as a problem in caring for clients.
        avoid: A statement nobody could disagree with.
    - id: wrong
      label: What result would tell me it was wrong
      kind: textarea
      guidance:
        ask: What you would have to hear or see to drop this.
        example: A manager tells me this is not an issue at all.
        avoid: A result you would explain away.
    - id: who-when
      label: Who I will ask, or what I will look at, and when
      kind: text
      guidance:
        ask: A named person or a specific thing, and a day this week.
        example: Rae, at our one-on-one next Tuesday.
        avoid: '"The team," "soon."'
    - id: ask
      label: What I will ask
      kind: textarea
      guidance:
        ask: The actual words, or what you will look for if it is an observation.
        example: I heard Sam say she starts from scratch when she takes over an account. Is
          that your experience?
        avoid: A question that tells them the answer you want.
    - id: why-this
      label: Why this one
      kind: textarea
      guidance:
        ask: Why this row and not another risky one.
        example: It could end the problem, and they sit near me.
        avoid: '"It seemed easiest."'
    criteria:
    - Choose a row you marked risky, or say why none is.
    - Make the wrong-result line concrete.
    - Name a person or an observation and a day this week.
    - If you are asking, write the question out.
    document_after:
    - What came back
    - 'Leave this blank now. Fill it in week 2, after you have made the check: what you checked
      it against and when, what came back, and what you make of it.'
publish: false
---

# Dig into your assumptions

Open your Problem Frame from Sprint 1. The Problem Frame is a living document, and you are going to be making changes, additions, and adjustments to it throughout the course. During this sprint you are going to expand on Part 6: your assumptions, and on Part 3: who is affected and costs.

Let's start by looking at Part 6: your assumptions. Every line there is something you wrote as if it were true, but you do not really know yet. Behind each assumption are questions, whose answers could change the shape of your problem, or show you that it is not a problem worth working on. The frame is only as good as the assumptions it stands on, so this sprint starts here.

Work without AI on this page. The next activity has AI push back on what you write here, and that only works if you bring your own thinking. This page is a table, one row per assumption, and a short block at the end for the one you will check. You get a Word file of it when you finish; keep it for week 2.

## Walk your assumptions

Take each assumption from Part 6 in turn and ask two things. What are the questions behind this assumption? And what different answers could change my problem? For some you might have many thoughts. For others, very little. Uneven answers are the normal result, and "nothing much" is a real answer for some lines.

Then decide: is this one risky? It is risky if an answer that went the other way would end the problem. Some could end it in principle but you already have reason to think they will not: customer service hears about it from clients all the time, or managers have mentioned frustration before. That is you accepting an assumption after looking at what you know, and you write the reason down with it.

> **Example, one row.**
>
> **My assumption:** All four managers are affected by account handovers not happening, not just the one I sat next to.
>
> **Questions behind my assumption:** Are the other managers affected by this problem? Is it all four of them? Are they affected in the same way? How bad is the impact?
>
> **Different answers that could change my problem:** None of them think this is a problem, so maybe I need to rethink my problem altogether. Two of them think it is a huge problem and the other two think it is mild, so I dig into the differences, but there is enough to proceed. All of them see it, so I proceed with a plan for finding out more from each.
>
> **Risky?** Could end it. If only one manager sees this, it is one person's habit, not a problem for nine weeks.

*More help: a row where the answer changes little.* *Managers act on stale ownership for days.* Questions: how long, really? Different answers: one day, several days, a week; none changes the problem, because even one day means the client repeats their history. Risky? Accepted, because the length does not change whether this is worth pursuing. A real row, and short.

*More help: a real kill, from the garden plot.* *New plot-holders quit because they had no one to ask.* Questions: why did last year's new people actually stop coming? Different answers: no one to ask, which is my frame; the plots were too far away or too big; they never meant to stay past one season. If it is either of the last two, pairing new people with old hands fixes nothing. Risky? Could end it, and it is the one I would check.

## Choose one to check

From the rows you marked as risky, pick one to actually follow up on this week: talk to one person about it, or look into something that can tell you more. Two criteria: you marked it risky, and you can follow up on it this week. If none of your rows is very risky, pick one that would be useful to learn more about. Even if you are pretty confident, you can sit down with one manager for ten minutes, or check the customer service logs.

Write up exactly what you want to check, before you look. Most of it comes from the row you already wrote.

> **Example.**
>
> **My assumption, stated so that it could be wrong:** Account managers see account handovers as a problem in effectively caring for clients.
>
> **What result would tell me it was wrong:** A manager tells me this is not an issue at all.
>
> **Who I will ask, or what I will go and look at, and when:** [Name of manager], at our one-on-one next Tuesday.
>
> **What I will ask:** I heard [other manager's name] mention that she gets frustrated when she takes over an account because she feels like she is starting from scratch having to understand the relationship. Is that your experience? Do you feel like you have to ask clients for a bunch of information you should already have? Does that seem like a problem for you? For the clients?

*More help: a check you look at rather than ask.* Garden plot: most new plot-holders quit by midsummer. Wrong if more than half of last year's new names are still gardening in August. What I will look at: last year's sign-up sheet against a walk past the plots this weekend. What I will ask: how many people have plots this year who were signed up last year?

This check is a temperature check. You are collecting information and using your judgement to decide whether to keep looking into this problem.

## What happens to the other assumptions

The assumptions you are not checking do not disappear. They stay in Part 6 of your frame, and in the last column, added this sprint, you write "not yet" against the ones still open and "accepted, because" against the ones you have made the call on. Sprint 3 is built for the open ones: that is where you take them to a real person. Checking one now is the start of that, not the whole of it.

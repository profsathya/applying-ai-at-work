---
type: assignment
title: Learning Plan and Updated Problem Frame Canvas Walkthrough
slug: learning-plan-and-updated-problem-frame-canvas-walkthrough
artifact_id: course1-learning-plan-and-updated-problem-frame-canvas-walkthrough
sprint: 17
week: 8
module: 'Sprint 4: Close the Learning Gap (V3)'
position: 7
walkthrough_after: course1-sprints-sprint-8-learning-plan-and-updated-problem-frame-v3
points: 50
submission_type: file_upload
completion_requirement: must_submit
delivery_mode: guided_assignment
learner_labels: true
learning_goal: Plan how to investigate every blocking gap and update the Problem Frame
  so its assumptions and unknowns match that plan.
publish: true
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  purpose: Plan how to investigate every blocking gap and update the Problem Frame
    to match.
  export_filename: learning-plan-week-8.docx
  feedback_endpoint: https://cti-course-ai.netlify.app/.netlify/functions/walkthrough-feedback
  feedback_protocol: walkthrough-v1
  document_prefix:
  - Learning Plan, week 8. Attach this Word file and the separate Week 7 Word file
    from Name the Gap. Keep Part A and C1 in that earlier file unchanged.
  tasks:
  - id: template-timing
    kind: table
    prompt: When to fill each part
    columns:
    - id: column-1
      label: Part
    - id: column-2
      label: Fill it in during
    rows:
    - id: row-1
      cells:
      - text: A. My gaps
      - text: Name the Gap (Week 1)
    - id: row-2
      cells:
      - text: B. My learning plan
      - text: Dojo Lab (Week 1), then Learning Plan (Week 2)
    - id: row-3
      cells:
      - text: 'C. My Problem Frame: C1 coming in, C2 updated'
      - text: C1 in Name the Gap (Week 1), C2 in Learning Plan (Week 2)
    - id: row-4
      cells:
      - text: D. Results
      - text: CIS 502
    read_only: true
    instruction_section: Bring your Week 7 Word file
  - id: plan-gap-1
    kind: table
    prompt: Part B. Gap 1
    columns:
    - id: field
      label: Field
      width: 4
    - id: answer
      label: Your answer
      width: 8
    rows:
    - id: row-1
      label: Raw material from the Dojo
      cells:
      - text: Raw material from the Dojo
      - text:  
        response: true
    - id: row-2
      label: What I need to learn
      cells:
      - text: What I need to learn
      - text:  
        response: true
    - id: row-3
      label: Why my Problem Frame needs it
      cells:
      - text: Why my Problem Frame needs it
      - text:  
        response: true
    - id: row-4
      label: Where I will learn it
      cells:
      - text: Where I will learn it
      - text:  
        response: true
    - id: row-5
      label: Steps, in order, with a rough time
      cells:
      - text: Steps, in order, with a rough time
      - text:  
        response: true
    - id: row-6
      label: How I will know I learned it
      cells:
      - text: How I will know I learned it
      - text:  
        response: true
    criteria:
    - For the selected row, use the gap's real context, specific sources or steps,
      and an independent check that could prove a claim wrong.
    instruction_section: Plan for Gap 1
  - id: plan-gap-2
    kind: table
    prompt: Part B. Gap 2
    columns:
    - id: field
      label: Field
      width: 4
    - id: answer
      label: Your answer
      width: 8
    rows:
    - id: row-1
      label: Raw material from the Dojo
      cells:
      - text: Raw material from the Dojo
      - text:  
        response: true
    - id: row-2
      label: What I need to learn
      cells:
      - text: What I need to learn
      - text:  
        response: true
    - id: row-3
      label: Why my Problem Frame needs it
      cells:
      - text: Why my Problem Frame needs it
      - text:  
        response: true
    - id: row-4
      label: Where I will learn it
      cells:
      - text: Where I will learn it
      - text:  
        response: true
    - id: row-5
      label: Steps, in order, with a rough time
      cells:
      - text: Steps, in order, with a rough time
      - text:  
        response: true
    - id: row-6
      label: How I will know I learned it
      cells:
      - text: How I will know I learned it
      - text:  
        response: true
    criteria:
    - For the selected row, use the gap's real context, specific sources or steps,
      and an independent check that could prove a claim wrong.
    instruction_section: Plan for Gap 2
  - id: plan-gap-3
    kind: table
    prompt: Part B. Gap 3
    columns:
    - id: field
      label: Field
      width: 4
    - id: answer
      label: Your answer
      width: 8
    rows:
    - id: row-1
      label: Raw material from the Dojo
      cells:
      - text: Raw material from the Dojo
      - text:  
        response: true
    - id: row-2
      label: What I need to learn
      cells:
      - text: What I need to learn
      - text:  
        response: true
    - id: row-3
      label: Why my Problem Frame needs it
      cells:
      - text: Why my Problem Frame needs it
      - text:  
        response: true
    - id: row-4
      label: Where I will learn it
      cells:
      - text: Where I will learn it
      - text:  
        response: true
    - id: row-5
      label: Steps, in order, with a rough time
      cells:
      - text: Steps, in order, with a rough time
      - text:  
        response: true
    - id: row-6
      label: How I will know I learned it
      cells:
      - text: How I will know I learned it
      - text:  
        response: true
    criteria:
    - For the selected row, use the gap's real context, specific sources or steps,
      and an independent check that could prove a claim wrong.
    instruction_section: Plan for Gap 3
  - id: additional-gap-plans
    kind: response
    prompt: Additional planned gaps, if needed
    criteria:
    - For each additional gap, include the same six template lines, including
      an independent check.
    instruction_section: If your plan has more than three gaps
  - id: dojo-choices
    kind: table
    prompt: Choices from the Dojo Lab
    feedback_enabled: false
    feedback_omission_reason: This table records completed Dojo Lab decisions rather than requesting a new AI review.
    criteria:
    - Record the Dojo suggestions you kept or rejected and why each choice fits your context.
    columns:
    - id: column-1
      label: Suggestion
    - id: column-2
      label: Keep or reject
    - id: column-3
      label: Why, in my context
    rows:
    - id: row-1
      cells:
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
    - id: row-2
      cells:
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
    - id: row-3
      cells:
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
    instruction_section: Keep your Dojo decisions
  - id: frame-c2
    kind: table
    prompt: C2. My updated frame
    columns:
    - id: field
      label: Field
      width: 4
    - id: answer
      label: Your answer
      width: 8
    rows:
    - id: row-1
      label: '1. The goal it serves'
      cells:
      - text: '1. The goal it serves'
      - text:  
        response: true
    - id: row-2
      label: '2. The problem'
      cells:
      - text: '2. The problem'
      - text:  
        response: true
    - id: row-3
      label: '3. Who is affected, what it costs them, and what fixing it would ask of them'
      cells:
      - text: '3. Who is affected, what it costs them, and what fixing it would ask of them'
      - text:  
        response: true
    - id: row-4
      label: '4. How it is handled today, and where that falls short'
      cells:
      - text: '4. How it is handled today, and where that falls short'
      - text:  
        response: true
    - id: row-5
      label: '5. What fixed would look like'
      cells:
      - text: '5. What fixed would look like'
      - text:  
        response: true
    - id: row-6
      label: '6. Assumptions: confirmed or inferred, and which gap checks each inference'
      cells:
      - text: '6. Assumptions: confirmed or inferred, and which gap checks each inference'
      - text:  
        response: true
    - id: row-7
      label: '7. What I do not know yet: planned gaps in order and interesting gaps left out'
      cells:
      - text: '7. What I do not know yet: planned gaps in order and interesting gaps left out'
      - text:  
        response: true
    criteria:
    - For the selected frame part, keep supported claims, mark uncertainty, and align
      parts 6 and 7 with the plan.
    instruction_section: C2. Update your Problem Frame
  - id: assumption-checks
    kind: table
    prompt: C2. Assumptions and their checks
    columns:
    - id: column-1
      label: Assumption
    - id: column-2
      label: Confirmed or inferred
    - id: column-3
      label: Checked by which gap
    rows:
    - id: row-1
      cells:
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 1
    - id: row-2
      cells:
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 2
    criteria:
    - For the selected row, distinguish confirmed evidence from inference and identify
      the gap that will check it.
    instruction_section: Track what will test each assumption
  - id: other-frame-changes
    kind: response
    prompt: Anything else I changed, and why
    criteria:
    - Name the part of the frame changed and the planning evidence or reasoning behind
      the change.
    instruction_section: Record any other correction
  - id: later-results
    kind: table
    prompt: Part D. Results for CIS 502
    columns:
    - id: column-1
      label: Gap
    - id: column-2
      label: What I found
    - id: column-3
      label: Confirmed, wrong, or complicated
    - id: column-4
      label: What it changed in my frame
    rows:
    - id: row-1
      cells:
      - text: '1'
      - text:  
      - text:  
      - text:  
    - id: row-2
      cells:
      - text: '2'
      - text:  
      - text:  
      - text:  
    - id: row-3
      cells:
      - text: '3'
      - text:  
      - text:  
      - text:  
    read_only: true
    instruction_section: Keep Part D for later
source_provenance: learning-plan-and-updated-problem-frame-canvas-walkthrough.sources.json
---

# Learning Plan and Updated Problem Frame Canvas Walkthrough

**Learning goal:** Write a learning plan that says for each gap why it matters, where you will learn it, the steps, and how you will know, then update your Problem Frame to match.

## Purpose

Plan how you will close the gaps in your Problem Frame, and update the frame so it shows what you know, what you are still assuming, and how you will find out.

You are not doing the learning now. You will follow this plan in CIS 502. What you write here needs to be clear enough that you could pick it up on the first day of that course and start.

Continue with Part B below, then Part C. Your Dojo Lab bullets are the raw material: pick from them, cut what did not survive, and write the five questions in full sentences, in your own words. Two things are yours to write here: the reason each gap matters to your frame, and the updated frame itself.

Write your own answers before requesting optional AI feedback. A selected row may be sent for formative feedback, but the service cannot know your workplace or supply evidence. Remove names and confidential details from any row you send. You can use the self-checks and finish every part without AI.

## Bring your Week 7 Word file

The [Learning Plan template](https://docs.google.com/document/d/1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA/copy) is a reference if you need to see the layout. Keep your Week 1 Word file with Part A and C1 unchanged. This walkthrough produces a separate Week 2 Word file with Part B and C2. Attach both files in this assignment. The table below shows when each part belongs.

## Plan for Gap 1

For each gap in your plan, in rank order, answer five questions. One or two sentences each is enough.

- **What do I need to learn?** The gap, in one line, and whether it is blocking or useful.
- **Why does my Problem Frame need it?** The part of the frame that depends on it, from A4.
- **Where will I learn it?** The sources: a person, a document, a system, an observation. Name them. A person counts; say how you will reach them.
- **What steps will I take, and in what order?** Small steps you could finish in one sitting, with a rough time for each.
- **How will I know I learned it?** What you will be able to show, and the independent thing you will check it against, which could confirm it or prove you wrong.

*Example, gap 1:*

**Learn:** Whether the other account managers really find out late when an account changes hands. Blocking.

**Why:** Part 3 of my frame, who is affected, says all four managers are. If they are not, the problem is smaller than I said.

**Where:** The four account managers. Dana, who sees every handover. The last three handover emails.

**Steps:** First, ask Dana for the dates of the last three handovers (15 min). Then ask each manager when they found out about those handovers (four short chats, about 1 hour). Then compare the dates (30 min).

**Know:** I can say, for each of the last three handovers, how many days passed before each manager knew. Confirmed if most managers found out more than a day late; wrong if most knew the same day. Checked against: the managers’ own answers, set beside the handover email dates.

If a gap does not fit in five small steps, it is probably a topic. Go back and narrow it.

First paste your Dojo Lab bullets for this gap into 'Raw material from the Dojo'. Then answer the five questions in the rows below it.

## Plan for Gap 2

Use the next planned gap, if you have one. Keep it separate from Gap 1 so the source, steps, and independent check fit this specific unknown. If you have only one planned gap, leave this block blank.

## Plan for Gap 3

Use this block for a third planned gap. Leave it blank if your ranked list stops earlier. Every blocking gap from Part A still belongs in the plan, even if the template's three example blocks are not enough.

## If your plan has more than three gaps

Add a block for each remaining planned gap here. Use the same six lines as the template: Dojo raw material and the five planning questions. Keep the ranking from Part A unless your Dojo work gave you a reason to change it; record that reason here.

## Keep your Dojo decisions

Look back at your Dojo transcript for the context you gave, which suggestions you kept or rejected, and what rejecting cost you. Enter up to three decisions that affected your plan in the table below. This records choices you already made; it is not a request to repeat the Dojo or accept a new suggestion now.

## C2. Update your Problem Frame

Open your Problem Frame document. You update the frame there first, then copy it here. Leave C1 in your Week 1 Word file as it is. In your Problem Frame document, update parts 6 and 7 so they match your plan:

- **Part 6, assumptions.** Keep each assumption marked confirmed or inferred. For each one still inferred, add which gap in your plan will check it, in place of “who could tell me.”
- **Part 7, what you do not know yet.** Rewrite it so it lists the gaps in your plan, in rank order, plus the interesting ones you left out.

If the Dojo or writing the plan showed you that another part of the frame is wrong or vague, fix it in your Problem Frame document, and note which part you changed.

Then change the line at the top of your document to "Last updated: Sprint 4" and the date. Copy each of the seven parts into the matching row of C2, "My updated frame," below. If you change anything in C2 after that, make the same change in your Problem Frame document so the two match.

*Example, part 6:*

From part 3: All four managers are affected. Status: inferred. Checked by: Gap 1 in my plan.

From part 4: The shared sheet stopped because the person who set it up left. Status: inferred. Checked by: Gap 2 in my plan.

The response rows below help you review all seven parts. If a selected row contains private workplace details, use the self-check without sending it for feedback.

## Track what will test each assumption

Use this table to link each inference to a gap. A confirmed claim still needs a real basis. If you have more than two assumptions, keep the rest in row 6 of the C2 table above; this table shows only two.

## Record any other correction

If planning changed another part of your frame, name the part and explain what made you revise it. A justified no-change conclusion is also possible.

## Keep Part D for later

This table records what you find while following the plan in CIS 502. Leave it blank for now.

Select **Download as Word document** below. In Canvas, select **Start Assignment**, attach this Week 2 Word file **and** your separate Week 1 Word file, then select **Submit Assignment**. The assessed work is Part B and C2; Part A and C1 in the Week 1 file provide the starting record. Keep your Dojo Lab decisions with these files. Saving a browser draft or downloading the file alone does not submit your work.

### Portfolio Capture

This plan is part of your readiness report in Sprint 5, and it is where you start in CIS 502. Your Problem Frame document, with "Last updated: Sprint 4" at the top, is your current frame. Bring it to Sprint 5 and to CIS 502.

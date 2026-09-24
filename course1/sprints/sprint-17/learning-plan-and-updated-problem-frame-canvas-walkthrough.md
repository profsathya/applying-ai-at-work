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
      - text: Name the Gap (week 7)
    - id: row-2
      cells:
      - text: B. My learning plan
      - text: Dojo Lab (week 7), then Learning Plan (week 8)
    - id: row-3
      cells:
      - text: 'C. My Problem Frame: C1 coming in, C2 updated'
      - text: C1 in Name the Gap (week 7), C2 in Learning Plan (week 8)
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
    - For each additional gap, include the same six source-template lines, including
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
      label: The goal it serves
      cells:
      - text: The goal it serves
      - text:  
        response: true
    - id: row-2
      label: The problem
      cells:
      - text: The problem
      - text:  
        response: true
    - id: row-3
      label: Who is affected, and what it costs them
      cells:
      - text: Who is affected, and what it costs them
      - text:  
        response: true
    - id: row-4
      label: How it is handled today, and where that falls short
      cells:
      - text: How it is handled today, and where that falls short
      - text:  
        response: true
    - id: row-5
      label: What fixed would look like
      cells:
      - text: What fixed would look like
      - text:  
        response: true
    - id: row-6
      label: 'Assumptions: confirmed or inferred, and which gap checks each inference'
      cells:
      - text: 'Assumptions: confirmed or inferred, and which gap checks each inference'
      - text:  
        response: true
    - id: row-7
      label: 'What I do not know yet: planned gaps in order and interesting gaps left
        out'
      cells:
      - text: 'What I do not know yet: planned gaps in order and interesting gaps
          left out'
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

Bring the **Week 7 Word file** you submitted for Name the Gap. Keep Part A and C1 there as your week 7 record. Use your Dojo Lab bullets to finish Part B here, then carry C1 into C2 and update your frame. You are planning how to learn in CIS 502, not claiming you have already closed these gaps.

Write your own answers before requesting optional AI feedback. A selected row may be sent for formative feedback, but the service cannot know your workplace or supply evidence. Remove names and confidential details from any row you send. You can use the self-checks and finish every part without AI.

## Bring your Week 7 Word file

The [Learning Plan template](https://docs.google.com/document/d/1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA/copy) is a reference if you need to see the source layout. Keep your Week 7 Word file with Part A and C1 unchanged. This walkthrough produces a separate Week 8 Word file with Part B and C2. Attach both files in this assignment. The table below shows when each part belongs.

## Plan for Gap 1

Start with your highest-ranked gap. Bring the raw options you wrote in the Dojo Lab, then answer the five template questions in full sentences. Name the source you can actually reach, make the steps small and ordered with a rough time, and say what independent evidence could confirm your conclusion or show you were wrong. A person can be a source; say how you will reach them.

For example, checking whether managers hear about handovers late could mean comparing their accounts with dated handover emails. Saying only that you will ask AI whether delays happen would not check the real process.

## Plan for Gap 2

Use the next planned gap, if you have one. Keep it separate from Gap 1 so the source, steps, and independent check fit this specific unknown. If you have only one planned gap, leave this block blank.

## Plan for Gap 3

Use this block for a third planned gap. Leave it blank if your ranked list stops earlier. Every blocking gap from Part A still belongs in the plan, even if the template's three example blocks are not enough.

## If your plan has more than three gaps

Add a block for each remaining planned gap here. Use the same six lines as the template: Dojo raw material and the five planning questions. Keep the ranking from Part A unless your Dojo work gave you a reason to change it; record that reason in your Week 8 file.

## Keep your Dojo decisions

Keep your Dojo Lab record of the context you gave AI, which suggestions you kept or rejected, and what changed. Enter up to three decisions that affected your plan in the source grid below. This records choices you already made; it is not a request to repeat the Dojo or accept a new suggestion now.

## C2. Update your Problem Frame

Use C1 in your Week 7 Word file to complete C2 here. Keep C1 unchanged. Update **part 6** so each assumption is marked Confirmed or Inferred and each remaining inference names the gap that will check it. Update **part 7** with planned gaps in rank order plus interesting gaps you left out. Correct another part only if planning showed it was wrong or vague, and record why.

The response rows below help you review all seven parts. If a selected row contains private workplace details, use the self-check without sending it for feedback.

## Track what will test each assumption

Use the source template's assumption table to link each inference to a gap. A confirmed claim still needs a real basis. If you have more than two assumptions, record the additional ones in the response below the table; the source grid shows only two.

## Record any other correction

If planning changed another part of your frame, name the part and explain what made you revise it. A justified no-change conclusion is also possible.

## Keep Part D for later

This source table records what you find while following the plan in CIS 502. Leave it blank for now.

Select **Download as Word document** below. In Canvas, select **Start Assignment**, attach this Week 8 Word file **and** your separate Week 7 Word file, then select **Submit Assignment**. The assessed work is Part B and C2; Part A and C1 in the Week 7 file provide the starting record. Keep your Dojo Lab decisions with these files. Saving a browser draft or downloading the file alone does not submit your work.

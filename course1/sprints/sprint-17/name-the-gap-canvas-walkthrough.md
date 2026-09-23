---
type: assignment
title: Name the Gap Canvas Walkthrough
slug: name-the-gap-canvas-walkthrough
artifact_id: course1-name-the-gap-canvas-walkthrough
sprint: 17
week: 7
module: 'Sprint 4: Close the Learning Gap (V3)'
position: 4
walkthrough_after: course1-sprints-sprint-9-name-the-gap-v3
points: 35
submission_type: file_upload
completion_requirement: must_submit
delivery_mode: guided_assignment
learner_labels: true
learning_goal: Identify and rank the unknowns that could change your Problem Frame,
  then connect each planned gap to a decision.
publish: false
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  purpose: Identify and rank the unknowns that could change your Problem Frame.
  export_filename: learning-plan-week-7-backup.docx
  submission_format: pdf_from_document
  records_destination:
    label: your continuing Learning Plan document
    url: https://docs.google.com/document/d/1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA/copy
  feedback_endpoint: https://cti-course-ai.netlify.app/.netlify/functions/walkthrough-feedback
  feedback_protocol: walkthrough-v1
  document_prefix:
  - Name the Gap, week 7. Keep Part A and C1 in the same Learning Plan file you will
    use in week 8.
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
    instruction_section: Keep one working document
  - id: what-i-know
    kind: response
    prompt: A1. What I already understand well enough
    criteria:
    - Name two or three things and the observation, conversation, or record that supports
      each.
    instruction_section: A1. Start from what you know
  - id: gap-inventory
    kind: table
    prompt: A2. What I do not know yet
    columns:
    - id: column-1
      label: '#'
    - id: column-2
      label: What I do not know
    - id: column-3
      label: Until I know this, I can't...
    - id: column-4
      label: Blocking, useful, or interesting
    rows:
    - id: row-1
      cells:
      - text: '1'
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 1
    - id: row-2
      cells:
      - text: '2'
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 2
    - id: row-3
      cells:
      - text: '3'
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 3
    - id: row-4
      cells:
      - text: '4'
      - text:  
        response: true
      - text:  
        response: true
      - text:  
        response: true
      label: Entry 4
    criteria:
    - Each unknown names a decision or next step, then marks its priority honestly.
    instruction_section: A2. Name and sort your gaps
  - id: other-gaps
    kind: response
    prompt: More gaps, if your list needs them
    criteria:
    - Use the same four fields as A2 for every additional gap.
    instruction_section: If you need more than four rows
  - id: learning-order
    kind: response
    prompt: A3. My learning order
    criteria:
    - Include every blocking gap, explain what goes first, and state when an interesting
      gap would start to matter.
    instruction_section: A3. Put them in order
  - id: frame-dependencies
    kind: response
    prompt: A4. Why each planned gap matters to my frame
    criteria:
    - For each planned gap, name the frame part that depends on it and what a different
      answer would change.
    instruction_section: A4. Explain the stakes
  - id: frame-c1
    kind: table
    prompt: C1. My frame coming in
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
      label: Assumptions
      cells:
      - text: Assumptions
      - text:  
        response: true
    - id: row-7
      label: What I do not know yet
      cells:
      - text: What I do not know yet
      - text:  
        response: true
    criteria:
    - Copy the Sprint 3 frame into all seven slots; note a slot you cannot yet fill.
    instruction_section: C1. Keep your Sprint 3 frame
    feedback_enabled: false
    feedback_omission_reason: C1 carries the participant's existing Sprint 3 frame;
      feedback belongs with the new gap judgments.
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
source_provenance: name-the-gap-canvas-walkthrough.sources.json
---

# Name the Gap Canvas Walkthrough

Start with the Problem Frame you revised after your real stakeholder conversation. This week, identify what you know, what you still need to learn, and which unknowns could change your next decision. Make your own first list before using any feedback. That list is the material you will test in the Dojo Lab.

The original Name the Gap assignment asks for work without AI. This Canvas Walkthrough adds instructor-requested, optional formative feedback **after** you write. It reviews only the response or row you select; it cannot know your workplace, add evidence, or decide your ranking. Leave out names and confidential details in any feedback request. You can use the self-checks and complete every part without AI.

## Keep one working document

[Make one copy of the Learning Plan template](https://docs.google.com/document/d/1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA/copy) and keep using that same file through week 8. Part A and C1 are due here. Part B begins in the Dojo Lab and is completed in Learning Plan; C2 is updated then. Part D stays empty until CIS 502. The table below keeps that schedule visible.

## A1. Start from what you know

Write two or three things about your problem that you already understand well enough. Add one line for each showing how you know. A stakeholder's account, your observation, or a reliable record can support a claim. Keep this short so your gaps start from solid ground.

## A2. Name and sort your gaps

Read your Sprint 3 validation report, the Inferred fields on your stakeholder map, and the assumptions and unknowns in your frame. Also look for vague language that may hide a missing fact. In each row, write one specific unknown and complete the sentence **Until I know this, I can't...** Then mark it **Blocking** if a decision waits on it, **Useful** if it improves the work without stopping it, or **Interesting** if no next step depends on it yet. Keep the numbered source rows and leave unused rows blank.

An illustrative blocking gap is whether managers hear about a handover too late. Until that is checked, you cannot say the delay affects the whole team. By contrast, learning how another company handles handovers may be interesting but outside this plan unless your real stakeholders make it relevant.

## If you need more than four rows

The source grid has four rows. If your frame still contains a consequential unknown, add it here and in your continuing Learning Plan document using the same fields: unknown, decision it affects, and priority. Do not stop at four merely because the table ends.

## A3. Put them in order

Every blocking gap goes into your plan. Rank those gaps, starting with the answer that could change what the others mean. Add useful gaps below if you choose. List interesting gaps outside the plan, with one line about what would make each start to matter. If none of your gaps is blocking after checking your frame twice, say what you examined and why no decision is waiting.

## A4. Explain the stakes

For each gap entering your plan, name the part of your seven-part Problem Frame that depends on it. State what would change if the answer went the other way. If the answer would change nothing, reconsider whether the gap is blocking.

## C1. Keep your Sprint 3 frame

Copy the frame from Section D of your Stakeholder Validation Report into these seven slots. If that revision is a paragraph, separate it into the seven parts as well as you can. Note any slot you cannot fill. Leave C1 unchanged after this week so C2 can show what planning changed.

## Keep Part D for later

The source template includes this results table for CIS 502. Keep it in your continuing file, but leave it blank now.

Copy the completed Part A and C1 work into your one Learning Plan document. Export that document as a **PDF** and upload it in this Canvas assignment. Part A and C1 are graded here. Keep working in the same file for the Dojo Lab and week 8. Saving a browser draft or pasting into your own document does not submit the PDF.

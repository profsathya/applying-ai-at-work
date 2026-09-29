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
publish: true
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  purpose: Identify and rank the unknowns that could change your Problem Frame.
  export_filename: learning-plan-week-7.docx
  feedback_endpoint: https://cti-course-ai.netlify.app/.netlify/functions/walkthrough-feedback
  feedback_protocol: walkthrough-v1
  document_prefix:
  - Name the Gap, week 7. Keep this Word file with your Sprint 4 work. You will attach
    it alongside a separate week 8 Word file in the next assignment.
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
    instruction_section: Keep your Week 7 Word file
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

**Learning goal:** Gather what you do not yet know about your own problem, in your own words, before any AI gets involved. Sort and rank it as blocking, useful, or interesting, and determine which part of your Problem Frame each gap holds up.

## Do this part without AI

If you ask an AI what someone working on your problem would need to learn, it will hand you a clean, sensible list. But it will be generic, not tailored to you. AI comes in at the Dojo Lab. Right now, the list has to come from your thinking.

The original Name the Gap assignment asks for work without AI. This Canvas Walkthrough adds instructor-requested, optional formative feedback **after** you write. It reviews only the response or row you select; it cannot know your workplace, add evidence, or decide your ranking. Leave out names and confidential details in any feedback request. You can use the self-checks and complete every part without AI.

## Keep your Week 7 Word file

Use this walkthrough to complete Part A and C1. The [Learning Plan template](https://docs.google.com/document/d/1XgCf1cTadZOCQtHdLEoebhJ8FWNjV6IzKUslKAtqxIA/copy) is available if you want to compare the source layout. Part B begins in the Dojo Lab and is completed in week 8; C2 is updated then. Part D stays empty until CIS 502. The table below keeps that schedule visible. Download and keep your Week 7 Word file. You will attach it alongside a separate Week 8 Word file in the next assignment.

## A1. Start from what you know

### Start with your frame

Your latest Problem Frame is the one you revised in Sprint 3, after your stakeholder conversation. It is in Section D of your Stakeholder Validation Report. Copy that version into C1 of your template, “My frame coming in.” After this week, leave C1 as it is. It is your record of where you started.

### Where to look for gaps

With your frame in front of you, and your Sprint 3 report open next to it, look for four things:

1. **Your assumptions** (part 6): anything still unverified or inferred. If your frame never marked them, mark them now.
2. **What you do not know yet** (part 7).
3. **Section D of your Sprint 3 report:** what still needs validation.
4. **Anything you describe vaguely** because you do not know the specifics.

The fourth is the easiest to miss. Vagueness in how you describe your own problem is usually a gap you have been routing around.

Write two or three things about your problem that you understand well enough. One line each on how you know.

*Example:* I know the outgoing manager tells the incoming manager directly. I have watched it happen twice, and Dana described it the same way.

Keep this short. It is here so you start from solid ground, not a list of everything you do not know.

## A2. Name and sort your gaps

Write your gaps, one line each.

**How many should you have?** It depends on where Sprint 3 left you. You tested one assumption with a real person, so one of your blocks may already be settled, and that conversation probably raised things you had not thought of before. Some people arrive with two open items, some with six.

You have enough when you can read your Problem Frame end to end and every part that could still be wrong has a gap pointing at it. Nothing unnamed. Most people land between three and five, but the number is a result, not a target.

**If you only find one or two,** look again in three places: what your stakeholder said that you had no answer for, anything in your frame you describe vaguely, and the parts of the frame the conversation never touched.

Run the sentence test on each: “Until I know this, I can’t ___.” If the blank will not fill, you have written a topic. Rewrite it or replace it.

Then sort each one:

- **Blocking.** A decision or next step is waiting on it. If you cannot name the decision, it is not blocking.
- **Useful.** It would improve the work, but nothing is stopped.
- **Interesting.** You want to know it, and nothing you do next depends on it.

A finished list looks like this:

1. I don’t know whether the other managers really find out late when an account changes hands. **Blocking.** I can’t say the problem is real for the whole team until I know.
2. I don’t know whether anyone tried to fix handovers before. **Blocking.** If a fix was tried and failed, the real problem is whatever killed it.
3. I don’t know how many handovers happen each month. **Useful.** It would show the size of the problem, but I can move without it.
4. I don’t know how other companies handle handovers. **Interesting.** Nothing I do next depends on it.

Be honest about the marks. There is no right number of blocking gaps. If none are blocking, go back to “Where to look for gaps,” especially the vagueness step. Lists with nothing blocking are usually too polite. If you have looked twice and still find none, say so and describe what you looked at.

Keep the numbered source rows and leave unused rows blank.

## If you need more than four rows

The source grid has four rows. If your frame still contains a consequential unknown, add it here using the same fields: unknown, decision it affects, and priority. Do not stop at four merely because the table ends.

## A3. Put them in order

Every blocking gap goes into your plan. Rank them. Ask: **which answer could change what the other gaps mean?** That one goes first.

Useful gaps can go into your plan too, below the blocking ones. You decide.

Interesting gaps stay on your list but not in your plan. For each one, write one line: what would tell you it has started to matter.

*Example:* Not in my plan: how other companies handle handovers. It starts to matter if Dana says the team wants to copy another company’s approach.

## A4. Explain the stakes

For each gap going into your plan, write one or two sentences: **which part of your Problem Frame depends on it, and what would change if the answer went the other way?**

*Example:* Gap 1 sits under part 3 of my frame, who is affected, where I wrote that all four managers are affected. If most managers already know about handovers, the problem is smaller than I said, and it may only affect new managers.

If the answer would change nothing in your frame, it is not blocking. Move it down.

## C1. Keep your Sprint 3 frame

The seven slots are already there, from Sprint 1: the goal, the problem, who is affected, how it is handled today, what fixed looks like, your assumptions, and what you do not know yet. If your Sprint 3 revision came out as a paragraph rather than seven parts, split it back out as best you can. A slot you cannot fill is a finding, not a failure. Note it and carry on.

## Keep Part D for later

The source template includes this results table for CIS 502. Keep it with your Word file, but leave it blank now.

Select **Download as Word document** below. In Canvas, select **Start Assignment**, attach your Week 7 Word file, and select **Submit Assignment**. Part A and C1 are graded here. Keep this file for the Dojo Lab and week 8. Saving a browser draft or downloading the file alone does not submit your work.

Next: take your list to the Dojo Lab, later this week. Leave yourself time for it. The Dojo Lab only works once this list exists, so the two go back to back.

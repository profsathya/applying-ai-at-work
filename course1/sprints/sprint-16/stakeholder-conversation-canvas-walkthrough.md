---
type: assignment
title: Stakeholder Conversation Canvas Walkthrough
slug: stakeholder-conversation-canvas-walkthrough
artifact_id: course1-stakeholder-conversation-canvas-walkthrough
sprint: 16
week: 6
module: 'Sprint 3: Integrate People and Context (V3)'
position: 8
walkthrough_after: course1-sprints-sprint-15-stakeholder-conversation
points: 50
submission_type: file_upload
completion_requirement: must_submit
delivery_mode: guided_assignment
learner_labels: true
learning_goal: Hold a real validation conversation, capture what the stakeholder actually
  said, and separate what it confirmed from what it complicated.
publish: true
guided_assignment:
  version: '1.1'
  presentation: walkthrough
  purpose: Hold a real validation conversation, document what the stakeholder said,
    and revise or confirm your Problem Frame based on evidence.
  feedback_endpoint: https://cti-course-ai.netlify.app/.netlify/functions/walkthrough-feedback
  feedback_protocol: walkthrough-v1
  export_filename: stakeholder-validation-report.docx
  records_destination:
    label: your own Stakeholder Validation Report document
    url: https://docs.google.com/document/d/1MUOWS7Y8nMMFu5wWP3_aK2-eGQvvEBUr3yV3d36_Ekw/copy
  document_prefix:
  - 'Complete this report across the conversation: Section A before, Section B during,
    Section C within five minutes, and Section D the same day or next.'
  - Submit this report together with the JSON response file from the Part 1 AI exchange
    and your updated Stakeholder Map.
  tasks:
  - id: report-name
    kind: table
    prompt: Your name
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Your name
      - text:   
        response: true
      label: Your name
    header_rows: 0
    criteria:
    - Record your name in your own working copy.
    instruction_section: Set up your report
    feedback_enabled: false
    feedback_omission_reason: Identity field is setup and does not need AI feedback.
  - id: meeting-plan
    kind: table
    prompt: A. Before the meeting
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Stakeholder name and role
      - text:   
        response: true
      label: Stakeholder name and role
    - id: row-2
      cells:
      - text: 'Relationship to the problem

          Which of the four, and does more than one apply?'
      - text:   
        response: true
      label: Relationship to the problem
    - id: row-3
      cells:
      - text: 'Format, date, and time

          In person, phone, video, or written.'
      - text:   
        response: true
      label: Format, date, and time
    - id: row-4
      cells:
      - text: 'The assumption this conversation is meant to test

          One assumption, from your map.'
      - text:   
        response: true
      label: The assumption this conversation is meant to test
    - id: row-5
      cells:
      - text: 'Your starting Problem Frame

          A sentence or two, as it stands right now.'
      - text:   
        response: true
      label: Your starting Problem Frame
    header_rows: 0
    criteria:
    - Carry over the selected stakeholder, relationship, and assumption from your
      Stakeholder Map. Record the actual conversation format, date, and time. Keep
      the starting Problem Frame as it stands before this conversation.
    instruction_section: A. Before the meeting
    feedback_enabled: false
    feedback_omission_reason: This table records identity, plans, and carried-over
      material; review the question wording and analysis in later steps.
  - id: validation-questions
    kind: table
    prompt: Your three validation questions
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Question 1
      - text:   
        response: true
      label: Question 1
    - id: row-2
      cells:
      - text: What I hope to learn
      - text:   
        response: true
      label: 'Question 1: what I hope to learn'
    - id: row-3
      cells:
      - text: Question 2
      - text:   
        response: true
      label: Question 2
    - id: row-4
      cells:
      - text: What I hope to learn
      - text:   
        response: true
      label: 'Question 2: what I hope to learn'
    - id: row-5
      cells:
      - text: Question 3
      - text:   
        response: true
      label: Question 3
    - id: row-6
      cells:
      - text: What I hope to learn
      - text:   
        response: true
      label: 'Question 3: what I hope to learn'
    header_rows: 0
    criteria:
    - For the selected question row, ask about an experience, decision, or tradeoff
      the chosen stakeholder can describe without nudging toward your preferred solution.
      For the selected learning row, say what that question could reveal about the
      single assumption. Review only this row.
    instruction_section: Your three validation questions
    feedback_enabled: true
  - id: conversation-notes
    kind: table
    prompt: B. During the meeting
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Their words, as close as you can capture them
      - text:   
        response: true
      label: Their words, as close as you can capture them
    - id: row-2
      cells:
      - text: Anything you did not expect
      - text:   
        response: true
      label: Anything you did not expect
    - id: row-3
      cells:
      - text: Anything they offered to follow up on
      - text:   
        response: true
      label: Anything they offered to follow up on
    header_rows: 0
    criteria:
    - Record the stakeholder’s words or a privacy-safe paraphrase. Keep observation
      separate from your interpretation.
    instruction_section: B. During the meeting
    feedback_enabled: false
    feedback_omission_reason: Conversation notes may contain another person’s words
      or identifying context. Keep them private and use the self-check.
  - id: first-impressions
    kind: table
    prompt: C. Within five minutes of finishing
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: What they confirmed
      - text:   
        response: true
      label: What they confirmed
    - id: row-2
      cells:
      - text: What they challenged or complicated
      - text:   
        response: true
      label: What they challenged or complicated
    - id: row-3
      cells:
      - text: 'Your first read: does the Problem Frame change?'
      - text:   
        response: true
      label: 'Your first read: does the Problem Frame change?'
    - id: row-4
      cells:
      - text: The next question you would ask
      - text:   
        response: true
      label: The next question you would ask
    header_rows: 0
    criteria:
    - For the selected row, name the evidence or uncertainty behind the first impression.
      Do not treat a possible change to the Problem Frame as settled before examining
      the whole conversation.
    instruction_section: C. Within five minutes of finishing
    feedback_enabled: true
  - id: report-conclusion
    kind: table
    prompt: D. Afterward, same day or next
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Revised Problem Frame, or an honest statement that it held
      - text:   
        response: true
      label: Revised Problem Frame, or an honest statement that it held
    - id: row-2
      cells:
      - text: What moved from Inferred to Confirmed on your map
      - text:   
        response: true
      label: What moved from Inferred to Confirmed on your map
    - id: row-3
      cells:
      - text: What still needs validation
      - text:   
        response: true
      label: What still needs validation
    header_rows: 0
    criteria:
    - For the selected row, distinguish what the real stakeholder confirmed from what
      remains inferred. A supported no-change conclusion is valid. Do not invent evidence
      or replace the participant’s judgment.
    instruction_section: D. Afterward, same day or next
    feedback_enabled: true
source_provenance: stakeholder-conversation-canvas-walkthrough.sources.json
---

# Stakeholder Conversation Canvas Walkthrough

Now test your Problem Frame with a real stakeholder. This report keeps your preparation, their account, your first impressions, and your evidence-based conclusion together. Bring your current Stakeholder Map and Problem Frame. You will submit the report, your updated map, and the JSON file from the question-check activity.

**Send the ask first.** Choose a channel the person uses. Ask for 20 to 30 minutes, then work through your questions while you wait. If there is no reply in three days, follow up once and offer a shorter or written option. If there is still no reply by day five, contact your backup and note the switch on your map. Confirm the format, time, and length when someone agrees.

Write before requesting optional AI feedback. It sees only the selected row, cannot know what happened in your workplace, and cannot supply evidence. Use roles or initials in feedback requests, leave out confidential details, and keep a path through every step without feedback. You decide what to revise.

## Set up your report

Enter your name for the report you will keep with your portfolio. This setup field stays out of AI feedback.

## A. Before the meeting

Carry the stakeholder, relationship, assumption, and starting Problem Frame over from your Stakeholder Map. Do not write a new assumption just for this report. Record the planned format, date, and time, then correct those details if the conversation moves. The map names four stakeholder relationships: affected, influential, responsible for a constraint, and positioned to challenge your frame. Name each relationship that applies.

## Your three validation questions

Bring the questions from your map's assumption blocks that this person can answer. If only two fit, take the third from that stakeholder's **Next question to ask** field. For each question, state what you hope to learn about the one assumption you are testing. Ask about a specific experience, past behavior, decision, or tradeoff. A question that invites approval of your solution is unlikely to reveal much.

After writing your draft questions here, [open the existing Part 1 AI question exchange](https://profsathya.github.io/Common-Curriculum/deanza/course1/assignments/stakeholder-conversation-v3.html). Give it your three questions, this stakeholder's relationship to the problem, what you hope to learn, and the one assumption you are testing. Use its follow-up questions to diagnose leading wording, vague questions, or missing evidence. **Rewrite the weak questions yourself** in this table. Download the JSON response file from that exchange. Use that page for the AI exchange and JSON download, then return to this walkthrough to finish the report. Upload all three files through this Canvas assignment. The AI exchange is preparation; your real conversation supplies the evidence.

The row feedback in this walkthrough is optional and narrower than the Part 1 exchange. It checks only the question or learning statement you choose, so it cannot judge whether all three questions work together. If feedback is unavailable, use the criteria above and continue.

## B. During the meeting

Ask your prepared questions and stay open to answers you did not expect. Keep these notes short so you can listen. Record the person's words as closely as you can, or paraphrase sensitive material without changing its meaning. Leave your interpretation for Sections C and D. This table has no AI button because it may contain another person's account.

## C. Within five minutes of finishing

While the conversation is still fresh, write a line or two for each first impression. What did the person confirm? What challenged or complicated your view? Does the Problem Frame seem to change? What would you ask next? These are provisional notes, not a polished conclusion. Optional row feedback can help you check whether an impression points to actual evidence.

## D. Afterward, same day or next

Give each answer a short paragraph. Revise your Problem Frame using what the stakeholder actually said, or explain honestly why your original frame held. Identify what moved from **Inferred** to **Confirmed** on your map, and what still needs validation. A clear confirmation is a useful result; do not force a change to show progress.

Then update your Stakeholder Map: correct fields this conversation settled, keep uncertainty visible, and add any stakeholder this person helped you identify. Keep your **What changed, and why** paragraph at the top. Download this report as a Word document below. In Canvas, submit **three files**: the Part 1 AI JSON response, this completed report, and the updated Stakeholder Map. Downloading or saving a browser draft does not submit them.

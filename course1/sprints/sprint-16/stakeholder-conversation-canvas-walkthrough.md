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
  final_check:
  - Section A is complete and carried over from your Stakeholder Map.
  - Your three validation questions are sharpened, not just copied.
  - Section B uses the stakeholder's own words, not your interpretation.
  - Section C records your first impressions right after the conversation.
  - Section D is based on evidence, and everything is submitted as one Word document.
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

          One assumption, from the assumption blocks on your Stakeholder Map.'
      - text:   
        response: true
      label: The assumption this conversation is meant to test
    - id: row-5
      cells:
      - text: 'Your problem, from The problem (Part 2) of your Problem Frame

          As it stands right now.'
      - text:   
        response: true
      label: Your problem, from The problem (Part 2) of your Problem Frame
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

Now it's time to test your Problem Frame against an actual stakeholder, not AI. This activity has four parts: preparing for the conversation, setting it up, having it, and documenting what you learned. Bring your current Stakeholder Map and Problem Frame. You will submit the report, your updated map, and the JSON file from the AI question exchange in Part 1.

Write before requesting optional AI feedback. It sees only the selected row, cannot know what happened in your workplace, and cannot supply evidence. Use roles or initials in feedback requests, leave out confidential details, and keep a path through every step without feedback. You decide what to revise.

## Set up your report

Enter your name for the report you will keep with your portfolio. This setup field stays out of AI feedback.

## A. Before the meeting

Carry the stakeholder, relationship, assumption, and starting Problem Frame over from your Stakeholder Map. Do not write a new assumption just for this report. Record the planned format, date, and time, then correct those details if the conversation moves. The map names four stakeholder relationships: affected, influential, responsible for a constraint, and positioned to challenge your frame. Name each relationship that applies.

## Your three validation questions

### Part 1: Prepare for the Conversation

**1. Bring your three questions.**

Your three questions come from the assumption blocks in your Stakeholder Map, the ones your chosen stakeholder can actually answer. Bring them here rather than writing new ones. If only two of your assumptions fit this person, take the third from their "Next question to ask" field in your map. Use the full weak-and-strong examples and self-check in the Stakeholder Map if you need a refresher.

You may sharpen the wording, and you may swap one out if something has changed since you wrote them, but start from what you already have. Each question should help this specific person describe an experience, decision, or tradeoff that bears on the one assumption you need to test.

Write each question into the table below with what you hope to learn from it.

**2. Run the AI exchange.**

The Dojo Lab polished these before you knew who would say yes; this pass is for the specific person who did.

This step uses the built-in AI activity, not your own AI chat. [Open the AI question exchange](https://profsathya.github.io/Common-Curriculum/deanza/course1/activities/stakeholder-conversation-v3.html?context=web) Start it and ask AI to respond to your draft with follow-up questions. Use them to diagnose your own questions. Look for places where AI's response reveals that your question is:

- **Leading:** it nudges the stakeholder toward the answer you want.
- **Vague:** it's unclear what you're really asking, so any answer would be hard to use.
- **Missing evidence:** it asks for an opinion rather than something you could verify, such as an experience, a specific example, or a real decision they made.

Use the deeper AI guidance button for more targeted help in refining your three questions.

**3. Rewrite the weak ones yourself**, and update the table below.

When you're done working with the AI, copy or download the JSON response file from the activity. You will submit it together with your report at the end.

The row feedback in this walkthrough is optional and narrower than the Part 1 exchange. It checks only the question or learning statement you choose, so it cannot judge whether all three questions work together. If feedback is unavailable, use the criteria above and continue.

## B. During the meeting

### Part 2: Set Up the Conversation

- Pick the method of communication this person actually answers: in person to set a time if you see them regularly; email if you want it in writing; phone or text if that is how you two normally talk.
- Send the ask, and note the date in the **Outreach log** of your Stakeholder Map. Keep it short: who you are, that you're investigating the problem, and that you would like 20 to 30 minutes.
- No reply in 3 days? Follow up once in the same thread, and make it easier to say yes: offer 15 minutes, or offer to send two questions they can answer in writing.
- Still no reply by day 5? Go to your backup stakeholder and start again. Note the switch in the **Outreach log**. A stakeholder who does not respond is itself information about access and influence.
- Got a yes? Confirm the time, the format, and the length, so you both arrive expecting the same conversation.

This is a real problem in your own work, and it is in both your interests to connect early. The sooner you talk, the more of this sprint you have left to act on what you hear.

### Part 3: Have the Conversation

- Check that the format, date, and time you wrote in Section A match what actually happened, and correct them if the meeting moved.
- Ask the validation questions you've prepared. Stay open to answers you didn't expect.
- Take notes in Section B, in the stakeholder's own words, as closely as you can capture them. Do not include confidential details, protect the person's privacy, and paraphrase anything sensitive. Don't add your interpretation; stay as close as you can to how the stakeholder described their experience.

Keep this short. You are listening, not writing. This table has no AI button because it may contain another person's account.

## C. Within five minutes of finishing

Within five minutes of finishing, fill in Section C, while it is still fresh. A line or two for each. You are catching your first impressions, not polishing them. Optional row feedback can help you check whether an impression points to actual evidence.

## D. Afterward, same day or next

### Part 4: Document What You Learned

Complete Section D of your report, the same day or the next. This is the only section that asks for new thinking rather than a record of what happened. A short paragraph for each. This is the section that asks for your thinking, so give it room.

Two things to hold on to as you write it. Update your Problem Frame on evidence, not on your own interpretation of what you heard. If the conversation fully confirmed your original frame, report that honestly. A clear confirmation is a real and valuable result. The same holds the other way: if the person told you the problem is not what you framed, or not there at all, say so. A supported "my frame did not hold" is also a valid result.

In your Problem Frame, update: the **Status** column in **Your assumptions** (Part 6) for every assumption this conversation tested; **The problem** (Part 2), **Who is affected** (Part 3a), or **How it is handled today** (Part 4a) if what you heard changed them; **What you do not know yet** (Part 7); and **Last updated** at the top: Sprint 3 and the date.

Then open your Stakeholder Map and make those changes in it. Update the status of every field the conversation settled, correct anything that turned out to be wrong, and add any stakeholder this person made you aware of. Leave your "What changed, and why" paragraph from the Dojo Lab sitting at the top of the file. You submit the updated map with your report.

Download this report as a Word document below. In Canvas, select **Start Assignment**, attach **three files** (the Part 1 AI JSON response, this completed report, and the updated Stakeholder Map), then select **Submit Assignment**. Downloading or saving a browser draft does not submit them.

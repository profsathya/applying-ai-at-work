---
type: assignment
title: Stakeholder Map walk-through (local example)
slug: stakeholder-map-walk-through-local-example
artifact_id: course1-sprints-sprint-15-stakeholder-map-walk-through-example
sprint: 15
week: 5
module: 'Sprint 3: Integrate People and Context (V3)'
position: 5
walkthrough_after: course1-sprints-sprint-15-stakeholder-map
points: 35
submission_type: file_upload
completion_requirement: must_submit
delivery_mode: guided_assignment
learner_labels: true
publish: false
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  export_filename: stakeholder-map.docx
  purpose: Draft an evidence-aware map of four real stakeholders in your own problem.
  tasks:
    - id: map-context
      kind: group
      prompt: Set up your map
      instruction_section: Set up your map
      repeat_count: 1
      layout: table
      repeat_labels: [Your map]
      fields:
        - {id: name, label: Your name, kind: text}
        - {id: problem-frame, label: Your starting Problem Frame in one sentence, kind: textarea}
      criteria:
        - Use your own current Problem Frame.
        - Keep a copy of the exported file because you will update it later in this sprint.
      document_after:
        - What changed, and why
        - Leave this section blank now. Complete it after the Dojo Lab, then keep it in this file.
    - id: stakeholder-profiles
      kind: group
      prompt: Profile four stakeholders
      instruction_section: Profile four stakeholders
      repeat_count: 4
      layout: table
      repeat_labels:
        - 'Stakeholder 1 of 4: Affected'
        - 'Stakeholder 2 of 4: Influential'
        - 'Stakeholder 3 of 4: Responsible for a constraint'
        - 'Stakeholder 4 of 4: Positioned to challenge your frame'
      fields:
        - id: role
          label: Role in relation to the problem
          kind: textarea
          evidence_status: true
          guidance:
            ask: Who is this person in relation to the problem, beyond their job title?
            example: Dana assigns accounts during handovers and is the only person who sees every handover.
            avoid: A job title without a connection to the problem.
        - id: relationship
          label: Relationship to the problem
          kind: textarea
          evidence_status: true
          guidance:
            ask: Which of the four relationships apply? Could more than one fit?
            example: Dana is responsible for a constraint and may also challenge my frame.
            avoid: Choosing only one relationship because there is one row.
        - id: impact
          label: Impact level and why
          kind: textarea
          evidence_status: true
          guidance:
            ask: How directly and strongly does the problem affect this person?
            example: Dana assigns accounts but may not carry the client relationship through a handover gap.
            avoid: Treating impact and authority as the same thing.
        - id: influence
          label: Influence or authority level and why
          kind: textarea
          evidence_status: true
          guidance:
            ask: How much say does this person have over a possible change?
            example: Dana sets the current handover announcement practice, so a change would need her involvement.
            avoid: Writing only high or low without saying what they can influence.
        - id: need
          label: Need in their terms
          kind: textarea
          evidence_status: true
          guidance:
            ask: What does this person need from a solution, in their own terms?
            example: Dana may need to avoid another step in a process she already considers complete.
            avoid: Putting your proposed solution in the stakeholder's voice.
        - id: constraints
          label: Constraints or risks they may see
          kind: textarea
          evidence_status: true
          guidance:
            ask: What risk, history, relationship, or policy might you be missing?
            example: Dana may have tried an earlier fix that failed for a reason I do not yet know.
            avoid: Listing only budget and policy constraints.
        - id: next-question
          label: Next question to ask
          kind: textarea
          evidence_status: true
          guidance:
            ask: What would you still need to learn from this person?
            example: When an account changed hands badly in the past, what happened next?
            avoid: A question that asks the person to approve your idea.
      criteria:
        - Include one person or group in each of the four required relationships.
        - Mark each field Confirmed or Inferred and explain the status.
        - Name every relationship that applies, even when it differs from the slot label.
        - Ask about a real experience or tradeoff rather than asking for approval of your idea.
    - id: assumption-blocks
      kind: group
      prompt: Write two or three assumption blocks
      instruction_section: Write assumption blocks
      repeat_count: 3
      layout: table
      repeat_labels: [Assumption 1, Assumption 2, 'Assumption 3 (optional)']
      fields:
        - {id: assumption, label: Assumption, kind: textarea}
        - {id: why, label: Why it matters, kind: textarea}
        - {id: question, label: Question to ask, kind: textarea}
        - {id: change, label: What a different answer changes, kind: textarea}
      criteria:
        - Complete at least two blocks, with all four lines in each.
        - Choose guesses that would change your next move if wrong.
        - Ask an open question that could challenge your current frame.
    - id: first-contact
      kind: group
      prompt: Choose your first contact and a backup
      instruction_section: Choose your first contact
      repeat_count: 1
      layout: table
      repeat_labels: [Your choice]
      fields:
        - {id: first, label: First choice and role, kind: text}
        - {id: backup, label: Backup and role, kind: text}
        - {id: reasoning, label: 'Why this person before anyone else?', kind: textarea}
      criteria:
        - Name a real first contact and a backup.
        - Explain why the first contact can test an important assumption or fill a meaningful gap.
      document_after:
        - Outreach log
        - Complete this section later during the Stakeholder Conversation.
        - 'Date I sent the ask:'
        - 'Date I followed up:'
        - 'Date I switched to my backup:'
---

# Stakeholder Map walk-through

This is a local design example based on the original Stakeholder Map Canvas assignment and its linked document template. Work with real people connected to your own problem. **Do this draft without AI.** You will test and widen it in the later Dojo Lab.

## Set up your map

Write your name and the current Problem Frame you are using. The exported Word file is yours to keep and update through the sprint. The file includes a blank "What changed, and why" section for the later Dojo Lab.

## Profile four stakeholders

Choose one stakeholder in each relationship: Affected, Influential, Responsible for a constraint, and Positioned to challenge your frame. A person may hold more than one relationship. For every field, write your answer, choose **Confirmed** or **Inferred**, and explain why. Confirmed means supported by a conversation, observation, or reliable documentation. Inferred means a reasoned hypothesis that still needs testing.

Use one to three sentences per field. For example, a role should describe the person's connection to the problem, not just a job title. An impact level should say how the problem reaches them; influence describes their say over a possible solution. For the last field, ask about a specific experience or tradeoff so the person can surprise you.

## Write assumption blocks

Look back at the fields you marked Inferred. Pick two or three assumptions that would change what you do next if they proved wrong. For each, state the assumption, why it matters, a question that could test it, and what a different answer would change. Leave the third block empty if two are enough.

## Choose your first contact

Name the person you will approach first and a backup in case they do not respond. Explain in two or three sentences why the first person can test a risky assumption or fill a gap in what you know. The exported file includes an outreach log to fill in during the later Stakeholder Conversation.

---
type: assignment
title: Stakeholder Map Canvas Walkthrough
slug: stakeholder-map-canvas-walkthrough
artifact_id: course1-stakeholder-map-canvas-walkthrough
sprint: 16
week: 5
module: 'Sprint 3: Integrate People and Context (V3)'
position: 5
walkthrough_after: course1-sprints-sprint-15-stakeholder-map
points: 35
submission_type: file_upload
completion_requirement: must_submit
delivery_mode: guided_assignment
learner_labels: true
learning_goal: Profile four stakeholders in your own problem, mark every field confirmed
  or inferred, and name the guesses a real conversation would have to settle.
publish: false
guided_assignment:
  version: '1.1'
  presentation: walkthrough
  purpose: Profile four stakeholders in your own problem, mark every field confirmed
    or inferred, and name the guesses a real conversation would have to settle.
  feedback_endpoint: https://cti-course-ai.netlify.app/.netlify/functions/walkthrough-feedback
  feedback_protocol: walkthrough-v1
  export_filename: stakeholder-map.docx
  records_destination:
    label: your own Stakeholder Map document
    url: https://docs.google.com/document/d/1Z0Sg2_2lnQNiryTOpzerdhIovuE4a4-AGivkxR2bRP4/copy
  document_prefix:
  - Keep this file. You will update it in the Dojo Lab and after your stakeholder
    conversation.
  - Write in your own words. Keep your first draft before revising it with optional
    feedback.
  tasks:
  - id: map-context
    kind: table
    prompt: Set up your map
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
    - id: row-2
      cells:
      - text: Your starting Problem Frame, in one sentence
      - text:   
        response: true
      label: Your starting Problem Frame, in one sentence
    header_rows: 0
    criteria:
    - Bring the Problem Frame you are already working on.
    instruction_section: Set up your map
    feedback_enabled: false
    feedback_omission_reason: Setup records your identity and existing frame; feedback
      belongs with the stakeholder judgments below.
  - id: later-reflection
    kind: table
    prompt: What changed, and why
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: 'After the Dojo Lab

          One short paragraph, in your own words: what moved between your first map
          and this one, what argument or evidence moved it, and one thing the AI suggested
          that you rejected, and why.'
      - text:   
      label: After the Dojo Lab
    header_rows: 0
    read_only: true
    instruction_section: What changed, and why
  - id: stakeholder-1
    kind: table
    prompt: 'Stakeholder 1 of 4: Affected'
    columns:
    - id: column-1
      label: Field
      width: 4
    - id: column-2
      label: Your answer
      width: 5
    - id: column-3
      label: Confirmed or Inferred, and why
      width: 5
    rows:
    - id: row-1
      cells:
      - text: 'Role

          Who is this person in relation to my problem, not on the org chart?'
      - text:   
        response: true
      - text:   
        response: true
      label: Role
      guidance:
        example: Dana, the account lead. She assigns accounts when they change hands
          and is the only person who sees every handover. Confirmed. I have watched
          her make the assignment twice.
        avoid: A job title with no relationship attached. "Account lead" is a title.
          "The only person who sees every handover" is a relationship.
    - id: row-2
      cells:
      - text: 'Relationship to the problem

          Which of the four applies? Does more than one?'
      - text:   
        response: true
      - text:   
        response: true
      label: Relationship to the problem
      guidance:
        example: 'Responsible for a constraint, and positioned to challenge my frame.
          She controls how handovers get announced, and she has been here longest,
          so she may know this was tried before. Constraint: Confirmed. She sets the
          practice. Challenge: Inferred. I am guessing at her history.'
        avoid: Picking one label because there is one row. Name every relationship
          that applies.
    - id: row-3
      cells:
      - text: 'Impact level

          How directly and strongly does the problem affect this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Impact level
      guidance:
        example: Low. She assigns the account and moves on. She does not carry a client
          relationship through the gap. Inferred. I have not asked whether the fallout
          reaches her.
        avoid: 'Merging impact with authority. They are separate fields because they
          are separate facts: the person who feels the problem most is often the one
          least able to change it.'
    - id: row-4
      cells:
      - text: 'Influence or authority level

          How much say does this person have over any solution?'
      - text:   
        response: true
      - text:   
        response: true
      label: Influence or authority level
      guidance:
        example: High. Nothing about how handovers get announced changes without her.
          Confirmed. She set the current practice.
        avoid: Writing "high" with nothing attached. High over what, specifically?
    - id: row-5
      cells:
      - text: 'Need

          What does this person need from a solution, in their terms?'
      - text:   
        response: true
      - text:   
        response: true
      label: Need
      guidance:
        example: To not add another step to a process she already considers finished.
          Inferred. This is my read of her, not something she has said.
        avoid: Writing a solution in the stakeholder's voice. "She needs a shared
          tracker" is your idea. "She needs to not add a step" is her interest.
    - id: row-6
      cells:
      - text: 'Constraints

          What constraint or risk might this person see that I have not?'
      - text:   
        response: true
      - text:   
        response: true
      label: Constraints
      guidance:
        example: She may have tried a fix before and watched it die, which would mean
          my real problem is whatever killed it. Inferred. Nobody I asked remembers,
          which is not the same as nobody having tried.
        avoid: Listing only budget and policy. A constraint can be a history, a relationship,
          or a reputation.
    - id: row-7
      cells:
      - text: 'Next question to ask

          What would I still need to find out from this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Next question to ask
      guidance:
        example: '"When an account changed hands badly in the past, what happened
          next?"'
        avoid: A question you already know the answer to.
    criteria:
    - Describe the person in relation to your real problem. Name every relationship
      that applies.
    - Write one to three sentences per field. Mark each field Confirmed or Inferred
      and explain why.
    - Distinguish impact from authority. State a need in the stakeholder’s terms and
      ask a question that could surprise you.
    instruction_section: 'Stakeholder 1 of 4: Affected'
  - id: stakeholder-2
    kind: table
    prompt: 'Stakeholder 2 of 4: Influential'
    columns:
    - id: column-1
      label: Field
      width: 4
    - id: column-2
      label: Your answer
      width: 5
    - id: column-3
      label: Confirmed or Inferred, and why
      width: 5
    rows:
    - id: row-1
      cells:
      - text: 'Role

          Who is this person in relation to my problem, not on the org chart?'
      - text:   
        response: true
      - text:   
        response: true
      label: Role
      guidance:
        example: Dana, the account lead. She assigns accounts when they change hands
          and is the only person who sees every handover. Confirmed. I have watched
          her make the assignment twice.
        avoid: A job title with no relationship attached. "Account lead" is a title.
          "The only person who sees every handover" is a relationship.
    - id: row-2
      cells:
      - text: 'Relationship to the problem

          Which of the four applies? Does more than one?'
      - text:   
        response: true
      - text:   
        response: true
      label: Relationship to the problem
      guidance:
        example: 'Responsible for a constraint, and positioned to challenge my frame.
          She controls how handovers get announced, and she has been here longest,
          so she may know this was tried before. Constraint: Confirmed. She sets the
          practice. Challenge: Inferred. I am guessing at her history.'
        avoid: Picking one label because there is one row. Name every relationship
          that applies.
    - id: row-3
      cells:
      - text: 'Impact level

          How directly and strongly does the problem affect this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Impact level
      guidance:
        example: Low. She assigns the account and moves on. She does not carry a client
          relationship through the gap. Inferred. I have not asked whether the fallout
          reaches her.
        avoid: 'Merging impact with authority. They are separate fields because they
          are separate facts: the person who feels the problem most is often the one
          least able to change it.'
    - id: row-4
      cells:
      - text: 'Influence or authority level

          How much say does this person have over any solution?'
      - text:   
        response: true
      - text:   
        response: true
      label: Influence or authority level
      guidance:
        example: High. Nothing about how handovers get announced changes without her.
          Confirmed. She set the current practice.
        avoid: Writing "high" with nothing attached. High over what, specifically?
    - id: row-5
      cells:
      - text: 'Need

          What does this person need from a solution, in their terms?'
      - text:   
        response: true
      - text:   
        response: true
      label: Need
      guidance:
        example: To not add another step to a process she already considers finished.
          Inferred. This is my read of her, not something she has said.
        avoid: Writing a solution in the stakeholder's voice. "She needs a shared
          tracker" is your idea. "She needs to not add a step" is her interest.
    - id: row-6
      cells:
      - text: 'Constraints

          What constraint or risk might this person see that I have not?'
      - text:   
        response: true
      - text:   
        response: true
      label: Constraints
      guidance:
        example: She may have tried a fix before and watched it die, which would mean
          my real problem is whatever killed it. Inferred. Nobody I asked remembers,
          which is not the same as nobody having tried.
        avoid: Listing only budget and policy. A constraint can be a history, a relationship,
          or a reputation.
    - id: row-7
      cells:
      - text: 'Next question to ask

          What would I still need to find out from this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Next question to ask
      guidance:
        example: '"When an account changed hands badly in the past, what happened
          next?"'
        avoid: A question you already know the answer to.
    criteria:
    - Describe the person in relation to your real problem. Name every relationship
      that applies.
    - Write one to three sentences per field. Mark each field Confirmed or Inferred
      and explain why.
    - Distinguish impact from authority. State a need in the stakeholder’s terms and
      ask a question that could surprise you.
    instruction_section: 'Stakeholder 2 of 4: Influential'
  - id: stakeholder-3
    kind: table
    prompt: 'Stakeholder 3 of 4: Responsible for a constraint'
    columns:
    - id: column-1
      label: Field
      width: 4
    - id: column-2
      label: Your answer
      width: 5
    - id: column-3
      label: Confirmed or Inferred, and why
      width: 5
    rows:
    - id: row-1
      cells:
      - text: 'Role

          Who is this person in relation to my problem, not on the org chart?'
      - text:   
        response: true
      - text:   
        response: true
      label: Role
      guidance:
        example: Dana, the account lead. She assigns accounts when they change hands
          and is the only person who sees every handover. Confirmed. I have watched
          her make the assignment twice.
        avoid: A job title with no relationship attached. "Account lead" is a title.
          "The only person who sees every handover" is a relationship.
    - id: row-2
      cells:
      - text: 'Relationship to the problem

          Which of the four applies? Does more than one?'
      - text:   
        response: true
      - text:   
        response: true
      label: Relationship to the problem
      guidance:
        example: 'Responsible for a constraint, and positioned to challenge my frame.
          She controls how handovers get announced, and she has been here longest,
          so she may know this was tried before. Constraint: Confirmed. She sets the
          practice. Challenge: Inferred. I am guessing at her history.'
        avoid: Picking one label because there is one row. Name every relationship
          that applies.
    - id: row-3
      cells:
      - text: 'Impact level

          How directly and strongly does the problem affect this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Impact level
      guidance:
        example: Low. She assigns the account and moves on. She does not carry a client
          relationship through the gap. Inferred. I have not asked whether the fallout
          reaches her.
        avoid: 'Merging impact with authority. They are separate fields because they
          are separate facts: the person who feels the problem most is often the one
          least able to change it.'
    - id: row-4
      cells:
      - text: 'Influence or authority level

          How much say does this person have over any solution?'
      - text:   
        response: true
      - text:   
        response: true
      label: Influence or authority level
      guidance:
        example: High. Nothing about how handovers get announced changes without her.
          Confirmed. She set the current practice.
        avoid: Writing "high" with nothing attached. High over what, specifically?
    - id: row-5
      cells:
      - text: 'Need

          What does this person need from a solution, in their terms?'
      - text:   
        response: true
      - text:   
        response: true
      label: Need
      guidance:
        example: To not add another step to a process she already considers finished.
          Inferred. This is my read of her, not something she has said.
        avoid: Writing a solution in the stakeholder's voice. "She needs a shared
          tracker" is your idea. "She needs to not add a step" is her interest.
    - id: row-6
      cells:
      - text: 'Constraints

          What constraint or risk might this person see that I have not?'
      - text:   
        response: true
      - text:   
        response: true
      label: Constraints
      guidance:
        example: She may have tried a fix before and watched it die, which would mean
          my real problem is whatever killed it. Inferred. Nobody I asked remembers,
          which is not the same as nobody having tried.
        avoid: Listing only budget and policy. A constraint can be a history, a relationship,
          or a reputation.
    - id: row-7
      cells:
      - text: 'Next question to ask

          What would I still need to find out from this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Next question to ask
      guidance:
        example: '"When an account changed hands badly in the past, what happened
          next?"'
        avoid: A question you already know the answer to.
    criteria:
    - Describe the person in relation to your real problem. Name every relationship
      that applies.
    - Write one to three sentences per field. Mark each field Confirmed or Inferred
      and explain why.
    - Distinguish impact from authority. State a need in the stakeholder’s terms and
      ask a question that could surprise you.
    instruction_section: 'Stakeholder 3 of 4: Responsible for a constraint'
  - id: stakeholder-4
    kind: table
    prompt: 'Stakeholder 4 of 4: Positioned to challenge your frame'
    columns:
    - id: column-1
      label: Field
      width: 4
    - id: column-2
      label: Your answer
      width: 5
    - id: column-3
      label: Confirmed or Inferred, and why
      width: 5
    rows:
    - id: row-1
      cells:
      - text: 'Role

          Who is this person in relation to my problem, not on the org chart?'
      - text:   
        response: true
      - text:   
        response: true
      label: Role
      guidance:
        example: Dana, the account lead. She assigns accounts when they change hands
          and is the only person who sees every handover. Confirmed. I have watched
          her make the assignment twice.
        avoid: A job title with no relationship attached. "Account lead" is a title.
          "The only person who sees every handover" is a relationship.
    - id: row-2
      cells:
      - text: 'Relationship to the problem

          Which of the four applies? Does more than one?'
      - text:   
        response: true
      - text:   
        response: true
      label: Relationship to the problem
      guidance:
        example: 'Responsible for a constraint, and positioned to challenge my frame.
          She controls how handovers get announced, and she has been here longest,
          so she may know this was tried before. Constraint: Confirmed. She sets the
          practice. Challenge: Inferred. I am guessing at her history.'
        avoid: Picking one label because there is one row. Name every relationship
          that applies.
    - id: row-3
      cells:
      - text: 'Impact level

          How directly and strongly does the problem affect this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Impact level
      guidance:
        example: Low. She assigns the account and moves on. She does not carry a client
          relationship through the gap. Inferred. I have not asked whether the fallout
          reaches her.
        avoid: 'Merging impact with authority. They are separate fields because they
          are separate facts: the person who feels the problem most is often the one
          least able to change it.'
    - id: row-4
      cells:
      - text: 'Influence or authority level

          How much say does this person have over any solution?'
      - text:   
        response: true
      - text:   
        response: true
      label: Influence or authority level
      guidance:
        example: High. Nothing about how handovers get announced changes without her.
          Confirmed. She set the current practice.
        avoid: Writing "high" with nothing attached. High over what, specifically?
    - id: row-5
      cells:
      - text: 'Need

          What does this person need from a solution, in their terms?'
      - text:   
        response: true
      - text:   
        response: true
      label: Need
      guidance:
        example: To not add another step to a process she already considers finished.
          Inferred. This is my read of her, not something she has said.
        avoid: Writing a solution in the stakeholder's voice. "She needs a shared
          tracker" is your idea. "She needs to not add a step" is her interest.
    - id: row-6
      cells:
      - text: 'Constraints

          What constraint or risk might this person see that I have not?'
      - text:   
        response: true
      - text:   
        response: true
      label: Constraints
      guidance:
        example: She may have tried a fix before and watched it die, which would mean
          my real problem is whatever killed it. Inferred. Nobody I asked remembers,
          which is not the same as nobody having tried.
        avoid: Listing only budget and policy. A constraint can be a history, a relationship,
          or a reputation.
    - id: row-7
      cells:
      - text: 'Next question to ask

          What would I still need to find out from this person?'
      - text:   
        response: true
      - text:   
        response: true
      label: Next question to ask
      guidance:
        example: '"When an account changed hands badly in the past, what happened
          next?"'
        avoid: A question you already know the answer to.
    criteria:
    - Describe the person in relation to your real problem. Name every relationship
      that applies.
    - Write one to three sentences per field. Mark each field Confirmed or Inferred
      and explain why.
    - Distinguish impact from authority. State a need in the stakeholder’s terms and
      ask a question that could surprise you.
    instruction_section: 'Stakeholder 4 of 4: Positioned to challenge your frame'
  - id: assumption-1
    kind: table
    prompt: Assumption 1
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: 'Assumption

          The thing you are guessing.'
      - text:   
        response: true
      label: Assumption
    - id: row-2
      cells:
      - text: 'Why it matters

          What it holds up in your frame.'
      - text:   
        response: true
      label: Why it matters
    - id: row-3
      cells:
      - text: 'Question to ask

          The question that would settle it.'
      - text:   
        response: true
      label: Question to ask
    - id: row-4
      cells:
      - text: 'What a different answer changes

          If you cannot answer this, it is probably not high stakes.'
      - text:   
        response: true
      label: What a different answer changes
    header_rows: 0
    criteria:
    - Choose an assumption whose opposite would change what you do next.
    - Complete all four lines. Your question should ask about experience, past behavior,
      or a concrete tradeoff.
    instruction_section: Assumption 1
  - id: assumption-2
    kind: table
    prompt: Assumption 2
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: 'Assumption

          The thing you are guessing.'
      - text:   
        response: true
      label: Assumption
    - id: row-2
      cells:
      - text: 'Why it matters

          What it holds up in your frame.'
      - text:   
        response: true
      label: Why it matters
    - id: row-3
      cells:
      - text: 'Question to ask

          The question that would settle it.'
      - text:   
        response: true
      label: Question to ask
    - id: row-4
      cells:
      - text: 'What a different answer changes

          If you cannot answer this, it is probably not high stakes.'
      - text:   
        response: true
      label: What a different answer changes
    header_rows: 0
    criteria:
    - Choose an assumption whose opposite would change what you do next.
    - Complete all four lines. Your question should ask about experience, past behavior,
      or a concrete tradeoff.
    instruction_section: Assumption 2
  - id: assumption-3
    kind: table
    prompt: Assumption 3 (only if you have a third)
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: 'Assumption

          The thing you are guessing.'
      - text:   
        response: true
      label: Assumption
    - id: row-2
      cells:
      - text: 'Why it matters

          What it holds up in your frame.'
      - text:   
        response: true
      label: Why it matters
    - id: row-3
      cells:
      - text: 'Question to ask

          The question that would settle it.'
      - text:   
        response: true
      label: Question to ask
    - id: row-4
      cells:
      - text: 'What a different answer changes

          If you cannot answer this, it is probably not high stakes.'
      - text:   
        response: true
      label: What a different answer changes
    header_rows: 0
    criteria:
    - Choose an assumption whose opposite would change what you do next.
    - Complete all four lines. Your question should ask about experience, past behavior,
      or a concrete tradeoff.
    instruction_section: Assumption 3 (only if you have a third)
  - id: first-contact
    kind: table
    prompt: Who you will talk to first
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: 'First choice

          Name and role.'
      - text:   
        response: true
      label: First choice
    - id: row-2
      cells:
      - text: 'Backup

          In case your first choice does not respond.'
      - text:   
        response: true
      label: Backup
    - id: row-3
      cells:
      - text: 'Why this person, before anyone else?

          Two or three sentences.'
      - text:   
        response: true
      label: Why this person, before anyone else?
    header_rows: 0
    criteria:
    - Name your first choice and backup for a real conversation.
    - Explain in two or three sentences why this person can test an important assumption
      or fill a meaningful gap.
    instruction_section: Who you will talk to first
  - id: outreach-log
    kind: table
    prompt: Outreach log
    columns:
    - id: column-1
      label: Field
    - id: column-2
      label: Your answer
    rows:
    - id: row-1
      cells:
      - text: Date I sent the ask
      - text:   
      label: Date I sent the ask
    - id: row-2
      cells:
      - text: Date I followed up (if no reply after 3 days)
      - text:   
      label: Date I followed up (if no reply after 3 days)
    - id: row-3
      cells:
      - text: Date I switched to my backup (if no reply by day 5)
      - text:   
      label: Date I switched to my backup (if no reply by day 5)
    header_rows: 0
    read_only: true
    instruction_section: Outreach log
source_provenance: stakeholder-map-canvas-walkthrough.sources.json
---

# Stakeholder Map Canvas Walkthrough

Before you talk to anyone, write down what you already believe about the people connected to your problem, and be honest about which parts you actually know. Bring your current **Problem Frame**. You will leave with four stakeholder profiles, two or three assumptions to test, and a first contact.

**Write each response yourself before asking for feedback.** In this walkthrough, the optional AI check points to a gap or asks a question about what you wrote. It cannot know your workplace or supply your evidence. You decide what to revise, in your own words. Keep your first draft before revising it so you have a view to test in the later Dojo Lab.

## Set up your map

Write your name and the Problem Frame you are using. This is the map you will keep working in throughout the sprint. Use roles or initials for other people, and keep confidential details out of responses you send for feedback.

## What changed, and why

*Leave this table blank for now.* It stays in your copied or downloaded map so you can fill it in after the **Dojo Lab: test, widen, choose**.

## Stakeholder 1 of 4: Affected

Start with someone the problem reaches directly. If you do not have a workplace stakeholder, choose a mentor, community member, customer, or another person with a genuine relationship to the problem.

Across the next four tables, profile **one stakeholder in each relationship**. A person may hold several relationships; name every one that applies. Write **one to three sentences per field** and give every field a status and a reason. **Confirmed** means supported by a conversation, observation, or reliable documentation. **Inferred** means a reasoned hypothesis you still need to test.

For the question field, mark whether the concern behind your question is Confirmed or Inferred and say why. You are not claiming to know the person's answer.

The optional examples beside the fields describe Dana, the account lead in the course's handover example. Read them together for one complete profile, then write about your own situation. Feedback beside a row reviews only that row.

## Stakeholder 2 of 4: Influential

Choose someone who has a say over what changes. Keep impact and authority separate: the person who feels the problem most may have the least power to change it. If you write “high,” say what this person has influence over.

## Stakeholder 3 of 4: Responsible for a constraint

Choose someone responsible for a condition any change must work within. A constraint can be a policy or budget, but it can also be a history, a relationship, or a reputation. Mark what you are guessing.

## Stakeholder 4 of 4: Positioned to challenge your frame

Choose the person most likely to tell you that you are solving the wrong problem. That is much cheaper to hear now than after you have built something. Think about who sees a part of the situation you do not.

## Assumption 1

Look back at what you marked **Inferred**. Some guesses barely matter. A few hold your whole frame up. Pick **two or three assumptions** that would change what you do next if you turned out to be wrong.

Imagine the stakeholder tells you the opposite of what you assumed. Would you choose a different problem, different people to speak with, or a different picture of what fixed would look like? If you would carry on the same way, choose a more consequential assumption.

A useful question invites a real account. **“Do you agree that X is the main problem?”** leads the person toward your answer. **“Walk me through the last time X happened. What did you actually do?”** leaves room for something you have not considered.

> **Illustrative example from the handover problem**
>
> **Assumption:** Nobody has tried to fix the handover problem before.
>
> **Why it matters:** If someone tried and it died, the real problem is whatever killed the fix, and that changes my Problem Frame.
>
> **Question to ask:** “When an account changed hands badly in the past, what happened next?”
>
> **What a different answer changes:** If she names a failed attempt, my next conversation is with whoever ran it, not with the four managers.

Write your own four lines below.

## Assumption 2

Choose a second assumption and complete all four lines. Ask about a specific experience, past behavior, or concrete tradeoff. If your question asks the stakeholder to approve your solution, rewrite it.

## Assumption 3 (only if you have a third)

Add a third block if another assumption would change your next move. Otherwise, leave this table blank. If you cannot say what a different answer would change, the assumption probably does not belong on this list.

## Who you will talk to first

Choose the person you will approach first for your real validation conversation, and name a backup in case they do not respond. Explain in **two or three sentences** why this person comes before anyone else.

They might be able to break your riskiest assumption, be the most affected person you know least about, sit at a point of disagreement, or speak for a larger group. Make the reason specific to your map.

## Outreach log

*Leave this table blank now.* Fill it in during the **Stakeholder Conversation**, as it happens.

Before you submit, check that your map has **four stakeholders**, every field marked **Confirmed or Inferred with a reason**, **two or three complete assumption blocks**, and **a first choice, a backup, and your reasoning**. Keep this file with your portfolio. You will update it in the Dojo Lab and after your conversation, then upload it again with your Stakeholder Conversation.

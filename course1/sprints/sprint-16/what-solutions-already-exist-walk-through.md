---
type: assignment
title: What solutions already exist walk-through
slug: what-solutions-already-exist-walk-through
artifact_id: course1-sprints-sprint-16-what-solutions-already-exist-walk-through
sprint: 16
week: 2
module: 'Sprint 2: Is This Problem Worth Pursuing?'
position: 7
points: 0
submission_type: text_entry
delivery_mode: guided_assignment
completion_requirement: must_submit
learner_labels: true
walkthrough_after: course1-sprints-sprint-16-what-solutions-already-exist
guided_assignment:
  version: '1.0'
  presentation: walkthrough
  feedback_omission_reason: 'No AI on this page by design: the learner''s own view is written
    here first, and the next activity, a Dojo Lab, is where AI tests it.'
  export_filename: what-already-exists.docx
  purpose: Start a table of what already exists that could solve or ease your problem, on
    your own, before AI.
  builds_on: Bring your Problem Frame. Work without AI on this page; the next activity fills
    the table in.
  standing_instruction: Own your progress · 0 points. Submit to complete this module requirement,
    and keep the exported file for the Dojo Lab.
  tasks:
  - id: your-table
    kind: group
    prompt: Your table, one row per thing that exists
    instruction_section: Build your understanding about what exists
    repeat_count: 6
    layout: table
    repeat_labels:
    - Row 1
    - Row 2
    - Row 3
    - Row 4 (optional)
    - Row 5 (optional)
    - Row 6 (optional)
    fields:
    - id: exists
      label: What exists
      kind: text
      guidance:
        ask: A thing that exists somewhere now, or a question about one.
        example: An owner field in our CRM.
        avoid: Something you would build.
    - id: how
      label: How it works, as far as I know
      kind: textarea
      guidance:
        ask: What you have actually seen, where it lives, who can change or see it, and what
          you do not know.
        example: I have seen the field, grayed out. I don't know who can set it or whether
          it can be turned on.
        avoid: Describing how it probably works as if you had seen it.
    - id: means
      label: 'What it means for my problem: good, bad, not sure'
      kind: textarea
      guidance:
        ask: Reasons it would be good for your problem, reasons it might be bad, and what
          you are not sure about.
        example: 'Good: already in a product we use. Bad: not on, and people barely use the
          CRM. Not sure: what turning it on costs, and who decides.'
        avoid: Deciding it is the answer before you have looked.
    criteria:
    - Fill at least three rows; questions count.
    - Keep solutions you would build out of the first column.
    - Leave blanks and "not sure" as they are rather than filling them with guesses dressed
      as facts.
    document_after:
    - After the Dojo Lab
    - 'Fill this in during the next activity: which rows AI added and which you kept; for
      each row you went and looked at, where you looked and what you found; and your table
      as it now stands.'
publish: false
---

# What solutions already exist

## What you need for this activity

- Your draft **Problem Frame**.
- Your **Sprint 2 working book**, to paste your table into when you finish.

You will do your work within Canvas. Work without AI on this page; the next activity is where AI helps you fill the table in.

The goal of this activity is for you to brainstorm and look into what already exists that could solve or ease your problem.

## Start by brainstorming what exists

With your problem in mind, think about existing solutions that might be related to your problem. What products or services do you know of that claim to have solutions in this problem space? Do you know anyone who is already handling this problem well? Do you know anything about how AI might be able to help solve this problem? Remember, this is a brainstorm, so anything counts - things you know of, things you have heard of, guesses, and even questions you have about what might exist should be included.

> **Example.** Problem: account handovers happen with no record. Possible solutions that exist: there is an owner field in our CRM that isn't being used; the sales team uses a handover checklist that might be similar; is there a weekly "accounts that moved" note, or does it ever come up in a weekly team meeting?

Then, for each item you thought of, you're going to describe what you know about it and how its existence might impact your problem.

## Build your understanding about what exists

With that in mind, start building a table that addresses these three questions:

1. What solutions already exist?
2. How do they work?
3. What does that mean for my problem?

The table below will help you think this through.

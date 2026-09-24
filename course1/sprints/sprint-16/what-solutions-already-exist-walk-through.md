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
    instruction_section: Build your table
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

The goal of this activity is for you to start a table of what already exists that could solve or ease your problem. Week 2 looks outward. Can you find other examples of people trying to solve this problem, or one like it, in your own situation or out in the world? Are there products, practices, or someone else who already does this well? If you find an existing solution, it does not necessarily mean your problem is not worth pursuing, but it might change how you think about it.

> **Example:** Our CRM has an owner field on every account. I have seen it, grayed out. I do not know whether ours is switched on.

You are listing what exists, not designing anything. "An agenda tool" is a thing that exists; "we should build an agenda tool" is a solution, and it waits. Things you know of, things you have heard of, guesses, and questions all count. As always, marking what you don't know is better than making something up. A table that is mostly questions will still be very useful for the next activity.

## Build your table

With your problem in mind, ask three things about each thing that might already exist:

- What exists?
- How does it work, as far as I know?
- What does it mean for my problem?

To find things for the first question, ask yourself: What products or services claim to have solutions in this problem space? Do I know anyone who has a similar problem but seems to be handling it well? Does my own organization, or do I personally, already have something for this, used or not? Could AI help with this problem?

The table below will help you think through each one. Fill one row per thing. Do the first column for everything you can think of, then the other two columns one row at a time.

*More help: if nothing comes to mind.* Turn your frame into questions and make each one a row. Is there a name for this problem, and are people talking about it online? What does the place next door do that we do not? Did anyone here try something before? Four questions and no answers, but there is real thinking here. That is what is needed.

*More help: take another look at the first column.* Everything in it should be something that exists, somewhere, now, or a question about one. If a row describes what you would build, move it out. That is a solution, and Sprint 2 is not where solutions get chosen.

When you finish, paste your table into your Sprint 2 working book. The next activity fills it in.

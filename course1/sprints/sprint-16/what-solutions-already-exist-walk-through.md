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
  feedback_omission_reason: "No AI on this page by design: the learner's own view is written here first, and the next activity, a Dojo Lab, is where AI tests it."
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
    instruction_section: 'Columns 2 and 3: one row at a time'
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

# What solutions already exist walk-through

For the first part of this sprint, you looked at your assumptions to see how a better understanding of them might change your problem. Week 2 starts by looking outward. Can you find other examples of people trying to solve this problem, or one like it, in your own situation or out in the world? Are there products, practices, or someone else who already does this well? If you find an existing solution, it does not necessarily mean your problem is not worth pursuing, but it might change how you think about it.

## Reflect on how you've been working with AI: providing Context

In two activities so far, you have thought first and then come to AI with your thinking already developed: your draft frames in Sprint 1 and your walk in week 1. That is you providing **Context** to AI, to get more useful results. Instead of handing AI the problem and having it generate the work, which it would not have been able to do a very good job of, you gave AI your thinking, which it read and pushed against. Context is the first C of Symbiotic Thinking, the partnership you met by name in Welcome, and it is one way to make your conversations with AI useful.

There are two other kinds of context you can provide: what AI needs to know about your situation, such as that you are doing this for school or work or yourself, that you have a deadline, that you want to share it with someone else; and how you want the AI to work with you, such as that you want no more than 150-word answers, that it should not change anything without asking you first, that you do not want colons. Your Dojo is set up with many of those instructions already. Go take a look at the course document you attached to the project; you will see many instructions for how the Dojo is supposed to interact with you.

[INTERIM: the sentence about the course document attached to the project is true once the Dojo doc and the Sprint 0 setup item exist. If they are not ready at the cut, it becomes "Once your Dojo is set up, its course document carries many of those instructions."]

## Back to existing solutions

This page is a table, three columns: what exists, how it works as far as you know, and what it means for your problem. As always, questions and question marks where you don't know something are encouraged. It is better to mark what you don't know than make something up; a table that is mostly questions will still be very useful for the next activity. You get a Word file of it when you finish; keep it, because the next activity fills it in.

Two passes: first everything you can think of for column 1, then columns 2 and 3 together, one row at a time.

## Column 1: what exists

With your problem in mind, brainstorm existing solutions that might be related to part or all of your problem. Ask yourself:

- What products or services do I know of that claim to have solutions in this problem space?
- Do I know anyone who has a similar problem but seems to be handling it well?
- Does my own organization, or do I personally, already have something for this, used or not?
- Do I know anything about how AI might be able to help solve this problem?

You are listing what exists, not designing anything. "An agenda tool" is a thing that exists. "We should build an agenda tool" is a solution, and it waits. Things you know of, things you have heard of, guesses, and questions all count.

> **Example, column 1 for account handovers.** Problem: account handovers happen with no record. Possible solutions that exist: an owner field in our CRM; a handover checklist (the sales team next door has one); is there a weekly "accounts that moved" note, or does it ever come up in a weekly team meeting?

*More help: the garden plot. If you don't know what solutions exist, you can ask questions.* Problem: new plot-holders start alone in April, and most stop coming by midsummer. Possible solutions that exist: do other community gardens pair new people with returning ones? Is there a name for this problem, and are people talking about it online? What does the garden two streets over do that ours does not? Did anyone here try something before? Four questions and no answers, but there is real thinking here. That is what is needed.

## Columns 2 and 3: one row at a time

Now take each row in turn and fill the other two columns while that thing is in your head.

**Column 2, how it works, as far as you know.** Write what you actually know about how it works, and be honest about what you do not. Have you seen it yourself? Where does it live? Who can change it, and who can see it? If you have not seen it, how do you know it exists? Who would have to switch it on? A row that is mostly "I do not know" is fine; that is what the next activity is for.

**Column 3, what it means for your problem.** Reasons this would be good for your problem, reasons it might be bad, and what you are honestly not sure about. Before you have looked into anything, most of this column will be "not sure," and that is the right result.

> **Example, one row, the CRM owner field.** Column 2: I have seen a CRM owner field, but it's grayed out. I don't know who can set it or if it can be turned on. If it can be, would the old owner change the name at the handover point? How would the new owner, or any of the other managers, be notified? Column 3: Good: it seems to already exist as a feature in a product we already use. Bad: it's not turned on, and people aren't using the CRM much as it is, so it might not make a difference. Not sure: whether turning it on costs anything, and who decides.

*More help: take another look at the first column.* Everything in it should be something that exists, somewhere, now, or a question about one. If a row describes what you would build, move it out. That is a solution, and Sprint 2 is not where solutions get chosen.

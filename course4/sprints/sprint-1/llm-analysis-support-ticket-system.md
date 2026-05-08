---
type: assignment
title: "LLM Analysis: Support Ticket System"
slug: llm-analysis-support-ticket-system
artifact_id: course4-sprints-sprint-1-llm-analysis-support-ticket-system
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 8
points: 35
submission_type: text_entry
publish: false
rubric:
  - description: "Defines the support ticket system before prompting AI"
    points: 8
  - description: "Explains starter code structure, fields, and workflow"
    points: 7
  - description: "Creates or proposes one feature with clear reasoning"
    points: 8
  - description: "Includes debugging or testing evidence"
    points: 6
  - description: "Reflects on AI partnership and verification"
    points: 6
---

# LLM Analysis: Support Ticket System

## Purpose

Analyze and extend a pre-generated support ticket system.

Everyone will use the same starter code. Do not generate a new system from scratch. The purpose is to practice defining a system, reading code, refining AI output, and protecting behavior with tests.

## Define The System First

Before prompting AI, write your own definition of the system.

Your definition must include:

- `title`: short description of the issue.
- `text`: full message from the person needing help.
- `supportee`: person or group affected.
- `warning_level`: numeric indicator of urgency or risk.
- `classification`: category such as account, billing, technical, or unknown.
- `status`: current state such as open, waiting, or closed.

Also define one workflow:

```text
new ticket -> validate fields -> classify -> assign priority -> save -> notify
```

## Read The Starter Code

Use the starter support ticket code from your instructor.

Annotate:

1. Where the ticket data is stored.
2. Which functions or methods change the ticket.
3. How classification works.
4. How priority is assigned.
5. Where files or databases are used, if included.
6. What tests exist, if any.

## Prompt AI After You Define The System

Use a prompt like:

```text
I am reading starter code for a support ticket system. The required fields are title, text, supportee, warning_level, classification, and status. Explain how this code represents the system, then identify missing checks or tests. Do not rewrite the whole system.
```

## Feature Options

Choose one feature to add or design:

- Save and load tickets with `sqlite3`.
- Define a priority system using warning level and classification.
- Add a simple spam filter.
- Generate tags from ticket text.
- Add a status update message for the supportee.

## Submission

Submit:

- Your system definition.
- Your annotated explanation of the starter code.
- The AI prompt you used and what you accepted or rejected.
- Your feature implementation or feature design.
- Evidence from running the code or tests.
- A short reflection on what you needed to decide before AI could help.

## Quality Standard

The strongest submissions show that you led the design. AI can help explain and refine, but it should not decide what the support ticket system means.

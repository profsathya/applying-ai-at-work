---
type: page
title: "Welcome to Week 2: Modeling Real Work"
slug: welcome-to-week-2-modeling-real-work
artifact_id: course4-sprints-sprint-1-welcome-to-week-2-modeling-real-work
sprint: 1
week: 2
module: "Module 2: Data Models, Control Flow, Objects, Files, and Testing"
position: 2
points: null
submission_type: none
publish: false
---

# Welcome to Week 2: Modeling Real Work

Last week you worked with functions and basic operations. This week you will use code to represent real things.

A support ticket is not only text. It has a title, a person who needs help, a warning level, a classification, tags, and a status. A phone in a dataset is not only a row. It has features that may or may not help predict price.

Programming becomes more useful when you can decide which details matter.

## The Main Shift

Week 1 asked:

- What does this function do?
- What input does it receive?
- What output does it produce?
- What happens when it fails?

Week 2 adds:

- What real-world thing does this code represent?
- Which details are stored?
- Which rules change the state?
- Which collection type fits the task?
- Which tests would protect the behavior?

## Why Objects Matter

Objects help you group related data and behavior.

For example, a support ticket might include:

- `title`
- `text`
- `supportee`
- `warning_level`
- `classification`
- `status`

Those fields belong together because they describe one thing the system needs to manage.

## Why Tests Matter

When code grows, reading is not enough. You also need evidence.

Tests let you describe expected behavior in code:

- A high warning level should produce a higher priority.
- A ticket with spam-like text should be flagged.
- A classifier should make predictions using the feature vector you selected.

Testing is not separate from understanding. It is one way understanding becomes visible.

## This Week's Mindset

Define the system before prompting AI.

If you ask for "a support ticket system" without defining the fields and rules, AI will invent a system for you. That may look helpful, but it moves the thinking away from you.

Start by naming what the system needs to represent. Then use AI to critique, explain, and refine.

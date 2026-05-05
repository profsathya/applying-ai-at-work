---
type: quiz
title: "Setup and First Run Check"
slug: setup-and-first-run-check
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 5
points: 6
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "What is the purpose of canvas_sync/init_course.py?"
    points: 1
    answers:
      - text: "To create a local course shell for an existing Canvas course"
        correct: true
      - text: "To create a new Canvas course in Canvas"
        correct: false
      - text: "To publish all Markdown files immediately"
        correct: false
      - text: "To delete old Canvas modules"
        correct: false
  - type: true_false
    prompt: "A real CANVAS_API_TOKEN should be pasted into a Codex chat when asking for help."
    points: 1
    answers:
      - text: "True"
        correct: false
      - text: "False"
        correct: true
  - type: multiple_choice
    prompt: "Which command validates a single local artifact in this repo?"
    points: 1
    answers:
      - text: ".venv/bin/python canvas_sync/schema.py --artifact <file>"
        correct: true
      - text: ".venv/bin/python canvas_sync/push.py --all"
        correct: false
      - text: ".venv/bin/python canvas_sync/remove.py --apply"
        correct: false
      - text: ".venv/bin/python canvas_sync/pull.py --apply"
        correct: false
  - type: multiple_choice
    prompt: "Where should Canvas IDs created by pushes be stored?"
    points: 1
    answers:
      - text: "The course manifest"
        correct: true
      - text: "Each Markdown artifact title"
        correct: false
      - text: "The assignment body"
        correct: false
      - text: "README.md"
        correct: false
  - type: short_answer
    prompt: "Name one check you should complete before asking for a first Canvas push."
    points: 1
  - type: essay
    prompt: "Describe how you would ask Codex in the app or IDE to perform a safe local first run without pushing to Canvas."
    points: 1
---

# Setup and First Run Check

Use this check to confirm that you can distinguish setup, validation, read-only inspection, and Canvas writes.

Answer practically. The goal is to show that you can operate the first run without exposing secrets or changing the live course by accident.

## Answer Key

1. To create a local course shell for an existing Canvas course.
2. False. Real tokens should not be pasted into Codex chat.
3. `.venv/bin/python canvas_sync/schema.py --artifact <file>`.
4. The course manifest.
5. Strong answers include validating artifacts, reviewing diffs, confirming the correct manifest, confirming the target Canvas course, checking for secrets, or getting explicit approval.
6. Strong answers include a Codex app or IDE prompt that asks for local inspection, validation, changed-file reporting, and `Do not push to Canvas`.

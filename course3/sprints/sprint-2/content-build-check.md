---
type: quiz
title: "Content Build Check"
slug: content-build-check
artifact_id: course3-sprints-sprint-2-content-build-check
sprint: 2
week: 3
module: "Module 3: Building and Publishing Content with Codex and Agents"
position: 5
points: 6
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "Which skill is the best fit for drafting a complete course from one pasted course plan?"
    points: 1
    answers:
      - text: "build-course"
        correct: true
      - text: "remove-canvas"
        correct: false
      - text: "reconcile"
        correct: false
      - text: "sync"
        correct: false
  - type: multiple_choice
    prompt: "Which script performs reviewed Canvas writes for one artifact and updates the manifest?"
    points: 1
    answers:
      - text: "canvas_sync/push.py"
        correct: true
      - text: "canvas_sync/schema.py"
        correct: false
      - text: "canvas_sync/inspect_canvas.py"
        correct: false
      - text: "schema/frontmatter.schema.json"
        correct: false
  - type: true_false
    prompt: "It is safe to run concurrent push processes against the same manifest if each file validates."
    points: 1
    answers:
      - text: "True"
        correct: false
      - text: "False"
        correct: true
  - type: multiple_choice
    prompt: "What is the safest next step when Canvas may have been edited directly after the last local push?"
    points: 1
    answers:
      - text: "Inspect Canvas and reconcile as needed before pushing local changes"
        correct: true
      - text: "Push immediately because Markdown is always newer"
        correct: false
      - text: "Delete the manifest and rebuild it manually"
        correct: false
      - text: "Paste the Canvas token into the artifact"
        correct: false
  - type: short_answer
    prompt: "Name one frontmatter field you should check before approving a generated artifact."
    points: 1
  - type: essay
    prompt: "Explain why drafting and publishing are separate steps in this repository."
    points: 1
---

# Content Build Check

Use this check to confirm that you can select the right build workflow and protect the publish boundary.

Answer as an operator who may need to explain the workflow to someone else before approving a Canvas change.

## Answer Key

1. `build-course`.
2. `canvas_sync/push.py`.
3. False. Pushes against the same manifest should be serial.
4. Inspect Canvas and reconcile as needed before pushing local changes.
5. Strong answers include `type`, `slug`, `sprint`, `week`, `module`, `position`, `points`, `submission_type`, `publish`, `rubric`, or `questions`.
6. Strong answers explain that drafting creates reviewable local Markdown, while publishing changes Canvas and updates the manifest, so validation and human approval are required before side effects.

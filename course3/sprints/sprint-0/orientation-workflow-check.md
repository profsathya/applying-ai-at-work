---
type: quiz
title: "Orientation Workflow Check"
slug: orientation-workflow-check
artifact_id: course3-sprints-sprint-0-orientation-workflow-check
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 5
points: 6
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "Which file is the root guidance file for repo-aware agents working in this repository?"
    points: 1
    answers:
      - text: "AGENTS.md"
        correct: true
      - text: "course3/manifests/production.json"
        correct: false
      - text: "canvas_sync/push.py"
        correct: false
      - text: ".env"
        correct: false
  - type: true_false
    prompt: "Canvas IDs should be written into artifact frontmatter so Codex can find them later."
    points: 1
    answers:
      - text: "True"
        correct: false
      - text: "False"
        correct: true
  - type: multiple_choice
    prompt: "Which path contains reusable Codex workflow skills for this repo?"
    points: 1
    answers:
      - text: ".agents/skills"
        correct: true
      - text: "course3/shared"
        correct: false
      - text: "archive"
        correct: false
      - text: "schema/frontmatter.schema.json"
        correct: false
  - type: multiple_choice
    prompt: "What should happen before canvas_sync/push.py is run against reviewed course files?"
    points: 1
    answers:
      - text: "Local validation and explicit human approval"
        correct: true
      - text: "Manual manifest editing"
        correct: false
      - text: "A Canvas removal dry run"
        correct: false
      - text: "A new PRD in every workflow"
        correct: false
  - type: short_answer
    prompt: "Name one detail you should include when asking Codex to draft or revise course artifacts in this repo."
    points: 1
  - type: essay
    prompt: "In a few sentences, explain the difference between local drafting and a Canvas write in this workflow."
    points: 1
---

# Orientation Workflow Check

Use this short check to confirm that you can identify the repo's main workflow boundaries.

Answer from the operator's perspective. You are checking whether you know where to look, what to protect, and when to ask for human review.

## Answer Key

1. `AGENTS.md`.
2. False. Canvas IDs belong in manifests, not artifact frontmatter.
3. `.agents/skills`.
4. Local validation and explicit human approval.
5. Strong answers include target course, sprint, source context, allowed file scope, Canvas boundary, validation expectation, or review criteria.
6. Strong answers explain that local drafting changes reviewable Markdown in the repo, while a Canvas write changes live Canvas state or local state based on Canvas and requires explicit approval.

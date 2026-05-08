---
type: quiz
title: "Verification and Maintenance Check"
slug: verification-maintenance-check
artifact_id: course3-sprints-sprint-3-verification-maintenance-check
sprint: 3
week: 4
module: "Module 4: Verification, Maintenance, and Extension"
position: 5
points: 6
submission_type: online_quiz
publish: false
questions:
  - type: multiple_choice
    prompt: "Which script is the read-only starting point for checking live Canvas modules and module items?"
    points: 1
    answers:
      - text: "canvas_sync/inspect_canvas.py"
        correct: true
      - text: "canvas_sync/push.py"
        correct: false
      - text: "canvas_sync/remove.py --apply"
        correct: false
      - text: "canvas_sync/init_course.py"
        correct: false
  - type: true_false
    prompt: "The reconcile workflow should run a dry run and show the drift report before applying Canvas changes locally."
    points: 1
    answers:
      - text: "True"
        correct: true
      - text: "False"
        correct: false
  - type: multiple_choice
    prompt: "Which workflow requires inspection, a dry-run plan, and a matching confirmation token before destructive Canvas action?"
    points: 1
    answers:
      - text: "remove-canvas"
        correct: true
      - text: "build-course"
        correct: false
      - text: "canvas-author"
        correct: false
      - text: "configure-course"
        correct: false
  - type: multiple_choice
    prompt: "Where should a repeatable Codex orchestration workflow normally live?"
    points: 1
    answers:
      - text: ".agents/skills"
        correct: true
      - text: "course3/sprints"
        correct: false
      - text: "course3/manifests/production.json"
        correct: false
      - text: ".env"
        correct: false
  - type: short_answer
    prompt: "Name one stop condition that should prevent a Canvas push, apply, or removal."
    points: 1
  - type: essay
    prompt: "Describe a small workflow extension and explain which layer should own it: documentation, skill, agent, script, or schema."
    points: 1
---

# Verification and Maintenance Check

Use this check to confirm that you can maintain the workflow after the first build.

Focus on the safety pattern: inspect first, dry run when appropriate, validate local files, and require explicit approval before side effects.

## Answer Key

1. `canvas_sync/inspect_canvas.py`.
2. True.
3. `remove-canvas`.
4. `.agents/skills`.
5. Strong answers include failed validation, wrong manifest, possible secret exposure, unexpected write scope, unreviewed drift, missing confirmation token, or lack of explicit approval.
6. Strong answers name a narrow extension and correctly place it in documentation, `.agents/skills`, `.codex/agents`, `canvas_sync`, or `schema/` based on whether the work is guidance, orchestration, role-specialized reasoning, deterministic side effects, or data contract.

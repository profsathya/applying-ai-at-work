---
type: assignment
title: "Repo Inspection Practice"
slug: repo-inspection-practice
sprint: 0
week: 1
module: "Module 1: Orientation to the Repo, Codex, and the Agentic Workflow"
position: 6
points: 10
submission_type: text_entry
publish: false
rubric:
  - description: "Prompt asks Codex to inspect before changing files"
    points: 3
  - description: "Summary identifies the repo workflow and major safety boundaries"
    points: 3
  - description: "Submission includes evidence of review and a local-only boundary"
    points: 2
  - description: "Technical or non-technical path is chosen and explained"
    points: 2
---

# Repo Inspection Practice

## Purpose

Practice using Codex app or Codex in an IDE to inspect this repo without changing files.

## Scenario

You are joining the team and need to understand how this repository turns local Markdown into Canvas content. You are not ready to edit or publish anything.

## Task Instructions

1. Open the repo root in Codex app or your IDE.
2. Ask Codex to inspect the repo without editing files.
3. Ask Codex to identify the workflow, local skills or subagents, Canvas safety rules, and validation path.
4. Review the answer and note anything that seems unclear or risky.
5. Submit your prompt, Codex's summary in your own words, and one follow-up question.

## Deliverable

A short text submission with:

- The prompt you used.
- A 5 to 8 sentence workflow summary.
- One safety rule you will follow.
- One question or blocker you would raise with a maintainer.

## Submission Format

Text entry.

## Expected Evidence Of Success

Your summary should mention local Markdown, validation, human review, explicit Canvas push, `.agents/skills/`, `.codex/agents/`, and `canvas_sync/`.

## Simplified Path For Non-Technical Users

Focus on what the repo does, what Codex should inspect, and how to avoid accidental Canvas changes. You do not need to run terminal commands.

## Extension Option For Technical Users

Ask Codex to identify the deterministic scripts and validation commands it would use for a draft-only workflow, then compare the answer with `README-BUILDER.md`.

## Suggested Codex Prompt Starter

```text
Inspect this repo before changing anything. Summarize the course-building workflow, local skills and subagents, Canvas safety rules, and validation commands. Do not edit files.
```

## Review Checklist Before Accepting Codex Changes

No changes should be made for this task. If Codex edits a file, stop and ask it to explain what changed and why.

---
type: assignment
title: "Week 3 Project: Fork and Pull Request a Feature"
slug: project-3-fork-and-pull-request-a-feature
artifact_id: course4-sprints-sprint-2-project-3-fork-and-pull-request-a-feature
sprint: 2
week: 3
module: "Module 3: Project Development, Git, Dependencies, Debugging, and Contribution"
position: 11
points: 50
submission_type: text_entry
publish: false
rubric:
  - description: "Chooses a scoped feature or bug fix appropriate to the project"
    points: 8
  - description: "Explains project structure and relevant files before changing code"
    points: 8
  - description: "Uses Git branch, commit, push, and pull request workflow"
    points: 8
  - description: "Includes evidence of running, testing, or manually verifying the change"
    points: 10
  - description: "Pull request description clearly explains purpose, change, and validation"
    points: 8
  - description: "Reflection explains AI use, review, and remaining risk"
    points: 8
---

# Week 3 Project: Fork and Pull Request a Feature

## Purpose

Practice making a scoped contribution to an existing project.

Your pull request does not need to be accepted upstream. The learning target is the workflow: read the project, choose a small change, make it on a branch, test it, explain it, and open a reviewable pull request.

## Project Source

Use the self-hosted project or repository provided by your instructor.

If your instructor approves an open-source AI project instead, choose a small documentation, test, or feature change that you can understand and explain. Do not choose a large architectural change.

## Required Steps

1. Fork or clone the project using your instructor's directions.
2. Read the README and any project guidance files.
3. Identify the files likely related to your change.
4. Create a branch.
5. Make one scoped feature, bug fix, documentation improvement, or test addition.
6. Run the available tests or a manual verification.
7. Commit the change with a clear message.
8. Push your branch.
9. Open a pull request.

## Pull Request Description

Your pull request should include:

- What changed.
- Why the change matters.
- How you tested it.
- Any known limitation.
- Whether AI helped and how you reviewed the result.

Example:

```text
Summary:
- Added validation for empty ticket title.
- Added one test for the validation behavior.

Validation:
- Ran pytest.
- Manually tried submitting an empty title.

AI use:
- Asked AI to explain the existing validation function.
- Wrote and reviewed the final change myself.
```

## Submission

Submit:

- A link to your pull request or a text copy of the pull request if links are not available.
- The branch name and commit message.
- The files you changed.
- Evidence of testing or manual verification.
- A short reflection on what you understood before using AI and what you had to verify afterward.

## Scope Guardrail

Keep the change small enough that another person could review it in five minutes.

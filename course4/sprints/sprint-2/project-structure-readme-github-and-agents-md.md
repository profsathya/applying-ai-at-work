---
type: page
title: "Project Structure, README, GitHub, and AGENTS.md"
slug: project-structure-readme-github-and-agents-md
artifact_id: course4-sprints-sprint-2-project-structure-readme-github-and-agents-md
sprint: 2
week: 3
module: "Module 3: Project Development, Git, Dependencies, Debugging, and Contribution"
position: 4
points: null
submission_type: none
publish: false
---

# Project Structure, README, GitHub, and AGENTS.md

A project structure helps people and tools know where things belong.

A small Python project might look like this:

```text
my-project/
  README.md
  AGENTS.md
  requirements.txt
  src/
    app.py
    helpers.py
  tests/
    test_helpers.py
```

The exact structure can vary. The important point is that the structure communicates how to work in the project.

## README.md

A README is the front door.

A useful README usually answers:

- What does this project do?
- How do I install it?
- How do I run it?
- How do I test it?
- What should I know before changing it?

If an AI tool reads a clear README, it has a better chance of helping within the actual project rules.

## AGENTS.md

AGENTS.md is a guidance file for AI coding assistants and repo-aware agents.

It can explain:

- Project purpose.
- Coding conventions.
- Validation commands.
- Files that should not be changed.
- Deployment or safety boundaries.
- Preferred workflows.

AGENTS.md is useful for you and your copilot. It turns hidden expectations into written context.

## Git And GitHub

Git tracks changes. GitHub hosts repositories and supports collaboration.

Basic workflow:

```text
clone or fork repository
  -> create a branch
  -> make a small change
  -> run tests
  -> commit
  -> push
  -> open pull request
```

You do not need to be a Git expert this week. You need to understand that version control records what changed, why it changed, and how others can review it.

## Documentation As Control

Documentation is not decoration. It is a way to control project behavior.

When a README, AGENTS.md, or context file explains the goal and constraints, you reduce the chance that an AI tool invents the wrong project.

Before asking AI to change a project, write or find:

- A short project description.
- The exact feature or bug.
- The files that seem relevant.
- The command to run tests.
- A definition of done.

That context improves both human and AI work.

---
type: page
title: "Starting Codex From The Repo"
slug: codex-builder-tutorial-starting-codex
artifact_id: course1-sprints-sprint-5-codex-builder-tutorial-starting-codex
sprint: 5
week: 10
module: "Using This Codex Course Builder"
position: 15
points: null
submission_type: none
publish: true
---

# Starting Codex From The Repo

Codex works best when you start it from the repo root. The repo root is the main project folder, the folder that contains `README.md`, `course1/`, `course2/`, `context/`, and `canvas_sync/`. Starting there gives Codex access to the course files, tutorial docs, schemas, skills, and Canvas sync scripts.

## What you need first

Before you start, make sure a course maintainer has given you:

- Access to this repo on your computer.
- The target course name, such as `course1` or `course2`.
- The source context for the course or module you want to build.
- Permission status for Canvas publishing. When in doubt, draft locally and stop before Canvas.

You do not need to memorize the folder structure. Codex can inspect it from the repo root.

Open a terminal and run:

```bash
cd applying-ai-at-work
source .venv/bin/activate
codex
```

If the virtual environment has not been created yet, ask Codex to help with the setup from `README.md`, or ask a maintainer to prepare the repo before you draft course content.

## Start with the tutorial

Before asking Codex to draft a course or module, skim the repo tutorial:

- `README.md` for the everyday workflow.
- `README-BUILDER.md` for the deeper builder reference.
- `context/course-specs/README.md` when you are asking for a full course.
- `context/module-specs/README.md` when you are asking for one sprint or Canvas module.

These files show the expected path: describe the work, draft local Markdown, validate, review, and only then approve any Canvas push.

If you are not sure which tutorial file applies, ask Codex:

```text
I want to draft one Canvas module. Which repo tutorial or spec file should I use before writing the build request?
```

## What Codex can see

From the repo root, Codex can inspect:

- Course files under `course1/` and `course2/`.
- Shared context documents under `context/`.
- Course and module spec formats under `context/course-specs/` and `context/module-specs/`.
- Build workflows under `.agents/skills/`.
- Agent definitions under `.codex/agents/`.
- Validation and Canvas sync scripts under `canvas_sync/`.

That context lets Codex respond to plain-English requests without asking you to choose every internal tool by name.

## What you should say first

Start with the outcome you want. For a full course, name the target course and source context:

```text
Draft course2 from context/course-specs/course2-ai-implementation.md and stop before Canvas.
```

For one module, name the target course, sprint, and source context:

```text
Draft course2 sprint 1 from context/module-specs/course2-sprint-1-stakeholder-framing.md and stop before Canvas.
```

The phrase `stop before Canvas` matters. It tells Codex to create local Markdown only, validate it, and wait for review.

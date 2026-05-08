---
type: page
title: "Technical Appendix: Setup Commands"
slug: technical-appendix-setup-commands
artifact_id: course3-sprints-sprint-1-technical-appendix-setup-commands
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 4
points: null
submission_type: none
publish: false
---

# Technical Appendix: Setup Commands

This page is a reference for technical operators. It is not the main learner workflow. Most people should work through Codex in the app or IDE and ask it to use the repo's documented workflows.

Use commands only when you are responsible for local setup or verification.

## One-time local setup

From the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r canvas_sync/requirements.txt
cp .env.example .env
```

Then fill `.env` with local credentials. Do not commit `.env`.

## Configure a local course shell

Use this only when Canvas already has a course shell and you need the repo to track it locally:

```bash
.venv/bin/python canvas_sync/init_course.py \
  --course course3 \
  --canvas-course-id 181 \
  --base-url https://cti-courses.instructure.com/ \
  --title "Using the Agentic Course Workflow" \
  --instance-name production
```

This is a local setup operation. It does not create a Canvas course and it does not push course content.

## Validate local files

Validate one artifact:

```bash
.venv/bin/python canvas_sync/schema.py --artifact course3/sprints/sprint-0/example-artifact.md
```

Validate the full local repo:

```bash
.venv/bin/python canvas_sync/schema.py --all
```

## Inspect Canvas without writing to Canvas

Use inspection before reconcile, removal, or a publish decision:

```bash
.venv/bin/python canvas_sync/inspect_canvas.py \
  --manifest course3/manifests/production.json \
  --include-items \
  --write-ledger \
  --format markdown
```

This reads Canvas and writes local ledger files. It does not write to Canvas.

## Stop before side effects

Do not run `canvas_sync/push.py`, `canvas_sync/pull.py --apply`, or `canvas_sync/remove.py --apply` unless the current task has explicit human approval and the local validation and review checks have passed.

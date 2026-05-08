---
type: module_header
title: "Module 2: Setup, Configuration, and Safe First Run"
slug: module-2-setup-configuration-and-safe-first-run
artifact_id: course3-sprints-sprint-1-module-2-setup-configuration-and-safe-first-run
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 1
points: null
submission_type: none
publish: false
---

# Module 2: Setup, Configuration, and Safe First Run

This module moves from orientation to a controlled first run.

You will learn how a local course shell is configured, where secrets belong, how to validate files, and how to ask Codex for a safe first operation from the app or IDE.

By the end of this module, you should be able to:

1. Explain how `canvas_sync/init_course.py` connects a local course key to an existing Canvas course shell.
2. Identify where configuration belongs and where secrets do not belong.
3. Run or request local validation without writing to Canvas.
4. Prepare a safe first-run checklist for a staged course.

You will still stop before Canvas writes unless a separate reviewed push is explicitly approved.

## Estimated Time

75 to 120 minutes.

## Audience Note

If you are non-technical, focus on what setup means, what should stay private, and when to ask a maintainer for help. If you are technical, also inspect the virtual environment, manifest, schema validator, and Canvas connection requirements.

## Required Artifacts

Complete these items in order:

1. Local Course Shell and Manifest
2. Secrets and Environment Placeholders
3. Technical Appendix: Setup Commands
4. Setup and First Run Check
5. Safe First Run Plan

## Learning Sequence

First, learn how a local course shell maps to an existing Canvas course. Next, learn how environment variables and secrets are handled. Then review the setup commands as a technical appendix and complete a local-only first-run plan.

## Formative Check

Complete `Setup and First Run Check`.

## Applied Task

Complete `Safe First Run Plan`.

## Completion Criteria

You are done when you can identify the target manifest, protect secrets, explain what validation can run locally, and name which actions require explicit Canvas approval.

## Common Misunderstandings

- `init_course.py` creates a local shell. It does not create a Canvas course.
- A manifest course ID does not prove the course content has been pushed.
- A missing `.env` blocks Canvas operations, not local Markdown review.
- A first run should not be a production Canvas write.

## Repository-Specific References

- `canvas_sync/init_course.py`
- `canvas_sync/requirements.txt`
- `canvas_sync/schema.py`
- `course3/manifests/production.json`
- `README-BUILDER.md`
- `course3/shared/command-reference.md`

## Codex App Or IDE Workflow Notes

Ask Codex to inspect setup readiness before proposing commands. If you are not authorized to use Canvas credentials, tell Codex to keep the workflow local and document which credentialed checks were skipped.

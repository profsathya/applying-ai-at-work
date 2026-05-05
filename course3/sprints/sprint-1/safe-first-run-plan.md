---
type: assignment
title: "Safe First Run Plan"
slug: safe-first-run-plan
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 6
points: 20
submission_type: text_entry
publish: false
rubric:
  - description: "Plan identifies the target course, manifest, allowed write scope, and no-push boundary"
    points: 6
  - description: "Plan includes secret-handling and paid API precautions"
    points: 4
  - description: "Plan includes artifact validation and full validation before any publish request"
    points: 5
  - description: "Plan includes a clear human review checkpoint before Canvas writes"
    points: 5
---

# Safe First Run Plan

## Purpose

Write a short first-run plan for operating this repo safely from Codex in the app or IDE.

Your plan should be specific enough that another operator could follow it without guessing your intent.

## Scenario

A teammate has opened the repo in Codex app or an IDE for the first time. They want to confirm the local course shell, validate files, and understand what is safe before anyone publishes to Canvas.

## Include these sections

**1. Target and scope**

Name the target course, manifest, and sprint folders. For this staged course, include:

```text
course3/manifests/production.json
course3/sprints/sprint-0
course3/sprints/sprint-1
course3/sprints/sprint-2
course3/sprints/sprint-3
```

State clearly that Canvas writes are not allowed during the first run unless a later reviewed request explicitly approves them.

**2. Codex request**

Draft the exact request you would give Codex in the app or IDE. Include the target, source context, allowed edit paths, validation expectation, and no-push boundary.

**3. Secret and cost precautions**

Explain how you will avoid exposing API tokens or keys. Also state how you will avoid unnecessary paid API usage, such as by giving bounded requests and reviewing failures before retrying.

**4. Verification steps**

List the local checks you expect before approval:

- Artifact validation with `canvas_sync/schema.py`.
- Full validation with `canvas_sync/schema.py --all`.
- Review of generated file paths, artifact types, positions, and publish flags.
- Review of the local diff.

**5. Go or no-go decision**

Name the condition that would make you stop. Examples include a wrong manifest, a failed validator, an unexpected file path, a possible secret exposure, or any request that would write to Canvas without approval.

## Deliverable

Submit a first-run plan with the five sections above.

## Submission Format

Text entry.

## Expected Evidence Of Success

Your plan should name `course3/manifests/production.json`, at least one `course3/sprints/sprint-<n>` folder, `canvas_sync/schema.py`, the no-push boundary, and a human review checkpoint.

## Extension Option For Technical Users

Add the exact validation commands you would run and the expected pass or failure output you would accept before review.

## Simplified Path For Non-Technical Users

Do not run commands. Ask Codex to inspect the setup files and produce a local-only first-run checklist that a maintainer can review.

## Suggested Codex Prompt Starter

```text
Inspect the course3 setup and repo validation workflow. Prepare a local-only first-run plan for Codex app or IDE use. Include target manifest, allowed file scope, secret handling, validation expectations, and stop conditions. Do not edit files and do not touch Canvas.
```

## Review Checklist Before Accepting Codex Changes

- Codex did not edit files unless you explicitly requested an edit.
- The plan uses placeholders for secrets.
- The plan does not run or approve `push.py`, `pull.py --apply`, or `remove.py --apply`.
- The plan includes local validation and human review before any Canvas write.

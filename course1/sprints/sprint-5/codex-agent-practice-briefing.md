---
type: page
title: "Codex Agent Practice Briefing"
slug: codex-agent-practice-briefing
artifact_id: course1-sprints-sprint-5-codex-agent-practice-briefing
sprint: 5
week: 10
module: "Practice: Using Codex Agents"
position: 10
points: null
submission_type: none
publish: true
---

# Codex Agent Practice Briefing

Codex can help draft course artifacts in this repo, but it works best when you treat it like a careful assistant rather than a publishing system. You give it a clear request. It drafts Markdown files. You review the files. Then you validate them locally. Canvas is updated only after a human explicitly approves a push.

This workflow is intentionally plain English. You do not need to know the Python scripts in detail to request a small module, page, assignment, quiz, or discussion. You do need to be specific about the course, sprint, artifact types, audience, constraints, and what should not happen.

## A useful request includes

- The target course and sprint.
- The Canvas module title.
- The artifact list in order.
- Any required titles, slugs, points, and submission types.
- The audience and purpose.
- Constraints such as no due dates, no file uploads, no Canvas push, or no edits outside a specific folder.

Plain English is enough. For example: "Create one page and one text-entry assignment for course1 sprint 5. Use Canvas-native Markdown only. Do not push to Canvas. Validate the files and report the results."

## What you review

After Codex writes files, review the Markdown before anything is pushed. Look for practical issues first:

- Does the artifact match the request?
- Is the audience addressed as working professionals?
- Are the instructions clear enough for someone to act on?
- Are points and submission types correct?
- Are there any due dates, file uploads, or unwanted external content?
- Would this artifact make sense inside the surrounding module?

You do not need to review every line like a software engineer. You are checking whether the learning activity is useful, accurate, and controlled.

## What validation does

Validation checks the local files against the repo schema. It catches issues such as missing frontmatter, invalid artifact types, unsupported submission types, forbidden HTML patterns, and em dashes.

Validation does not decide whether the activity is pedagogically good. That remains your job. A file can pass validation and still need revision because the prompt is too vague, too long, or not useful for the audience.

## Where the workflow stops

The default stopping point is local Markdown plus validation results. A Canvas push is a real write to a live course. Codex should not push unless you explicitly approve that step.

That separation matters. It gives you a review point between drafting and publication, and it keeps small experiments from becoming accidental course changes.

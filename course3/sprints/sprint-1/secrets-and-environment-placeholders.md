---
type: page
title: "Secrets and Environment Placeholders"
slug: secrets-and-environment-placeholders
artifact_id: course3-sprints-sprint-1-secrets-and-environment-placeholders
sprint: 1
week: 2
module: "Module 2: Setup, Configuration, and Safe First Run"
position: 3
points: null
submission_type: none
publish: false
---

# Secrets and Environment Placeholders

Secrets make the workflow powerful and risky. Treat them as operational credentials, not course content.

Do not paste real API keys, access tokens, or personal credentials into Codex chat, Markdown artifacts, commits, screenshots, or discussion posts.

## Where secrets belong

Local secrets belong in environment files or your local shell environment.

Common placeholders are:

```text
CANVAS_API_URL=<your-canvas-base-url>
CANVAS_API_TOKEN=<your-canvas-api-token>
OPENAI_API_KEY=<your-openai-api-key>
```

Use placeholders in training content. Use real values only in the local environment where the scripts run.

## Canvas credentials

Canvas API credentials allow scripts to inspect, create, update, or remove Canvas content depending on the command you run.

That means:

- `canvas_sync/inspect_canvas.py` can read live Canvas state.
- `canvas_sync/push.py` can write live Canvas content.
- `canvas_sync/pull.py --apply` can change local Markdown based on Canvas.
- `canvas_sync/remove.py --apply` can delete Canvas content after confirmation.

Before using a token, confirm which Canvas account, course, and permission scope it belongs to.

## Paid API caution

AI calls may incur cost depending on the account and model being used. The safest habit is to use bounded requests:

- Ask for one course or module at a time.
- Provide source context up front.
- Ask Codex to inspect first when the current state is unclear.
- Validate once the local draft is complete.
- Avoid repeated broad retries without reviewing the actual failure.

## Redaction habit

When sharing logs or screenshots, remove:

- API tokens.
- Authorization headers.
- User access tokens.
- `.env` contents.
- Internal course IDs if they are not needed for the audience.
- Personal participant data from Canvas.

If you are not sure whether a value is sensitive, replace it with a placeholder before sharing.

# Codex Review Checklist

## Review The Scope

- Did Codex change only the files in scope?
- Did it avoid `course*/manifests/production.json` during draft-only work?
- Did it avoid `context/`, `course*/design/`, `archive/`, schemas, and `canvas_sync/` unless the task required those files?
- Did it avoid real secrets and tokens?

## Review The Content

- Are titles, slugs, modules, positions, points, and submission types correct?
- Does the body use Canvas-native Markdown?
- Does it avoid HTML, iframes, scripts, styles, and external CDN references?
- Does it avoid em dashes?
- Does it write for working professionals rather than undergraduates?
- Does it ask for real workplace work rather than role-play?

## Review The Workflow

- Did Codex explain which skill or subagent it used or would use?
- Did Codex validate changed artifacts?
- Did Codex run full repo validation when appropriate?
- Did Codex report no Canvas writes for local-only work?
- Did Codex separate inspect, reconcile, push, and remove decisions?

## Review Canvas Risk

- If this was an inspect task, was it read-only against Canvas?
- If this was a push task, were exact reviewed files named?
- If this was a removal task, was there a fresh dry run and confirmation token?
- If Canvas drift exists, was reconcile dry run reviewed before local edits continued?

## Review The Diff

Use the Codex app review pane or IDE diff view:

- Inspect every changed file.
- Leave inline comments for targeted corrections.
- Ask Codex to address comments with minimal scope.
- Stage only what should be accepted.
- Keep unrelated user changes separate.

---
description: Update the due date(s) of one or more assignments by NLP, file path + date, or a mapping file.
---

Update due dates for canvas artifacts. Arguments: `$ARGUMENTS` (NLP description, `<path> <iso-date>`, or `--from <mapping-file>`).

Workflow:

1. Invoke `due-date-updater` with the argument string. Show the returned summary.
2. If AMBIGUOUS entries were returned, ask the user to disambiguate before re-invoking. Do not proceed until targets are concrete.
3. For each UPDATED file, invoke `schema-validator`. If any fail, stop and report. The user decides whether to revert manually or fix.
4. Show the user the list of modified files and ask: "Push these due-date changes to canvas? (yes/no)"
5. On yes: invoke `canvas-pusher` on each modified file with the active manifest (`course<N>/manifests/production.json`, selected by which course the files live under). On no: exit with MD changes still in place and remind the user they can run `/sync <file>` later.
6. Commit modified files with message: `chore: update due dates (<N> artifacts)`.

Never skip schema validation. Never push without explicit user confirmation. If the user's NLP instruction has no concrete date ("sometime next week"), ask for a specific date before invoking the agent.

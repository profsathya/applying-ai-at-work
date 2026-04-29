---
name: ralph-build-loop
description: Run or maintain the Codex Ralph loop for initial course builds using file-backed PLAN, BUILD, and VERIFY phases.
---

# Ralph Build Loop Skill

Use this skill when maintaining or running `codex-ralph.sh` and `prompts/codex/ralph-prompt.md`.

## Contract

- Each iteration starts from repo files, not from conversation memory.
- Each BUILD iteration processes exactly one pending PRD item.
- State persists in `course<N>/prd.json`, `course<N>/progress.md`, manifests, git commits, and `AGENTS.md` learnings.
- Completion is signaled only by `<promise>COURSE_COMPLETE</promise>`.
- Human-required failures are signaled by `<promise>HALT: ...</promise>`.

## Safety

- Do not run an unattended Canvas-writing build against production until the Codex pilot has passed on a sandbox course.
- Prefer `codex exec --full-auto` for local unattended testing only when the sandbox and approvals are understood.
- Do not use dangerous bypass modes unless a human explicitly approves them for a controlled run.

## Validation

- `python3 canvas_sync/schema.py --all`
- Review `course<N>/prd.json` status counts.
- Review `course<N>/manifests/production.json` artifact count.
- Confirm no failed item is retried without a human resetting it.

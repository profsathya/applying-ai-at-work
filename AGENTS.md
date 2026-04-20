# Agent Learnings

This file accumulates patterns, gotchas, and discoveries across course builds. Subagents append here during BUILD when they notice something worth remembering. Future Ralph iterations and future human maintainers read this first.

Keep entries concise. One line per learning. Reference specific files or PRs when useful.

## Build history

- 2026-04-20: PRD written for course1, 35 artifacts across 6 sprints (sprint-0 orientation, sprint-1..4 middle, sprint-5 capstone).

## Learnings

- Schemas `schema/prd.schema.json` and `schema/frontmatter.schema.json` originally defined `sprint: minimum: 1`, which conflicted with the CLAUDE.md convention that orientation is `sprint-0` and capstone is `sprint-5`. Relaxed to `minimum: 0, maximum: 5` during course1 planning.
- Canvas's assignment API expects `online_text_entry`/`online_upload` in `submission_types`, not the shortened `text_entry`/`file_upload` we use in frontmatter. Added `CANVAS_SUBMISSION_TYPE_MAP` in `canvas_sync/push.py` to translate on the way out. First assignment push (Choose Your Problem) 400'd before the fix.
- Canvas's `due_at` requires full ISO 8601 with timezone (e.g. `2026-10-15T23:59:00Z`). A bare local datetime like `2026-10-15T23:59` will 400. Course1 assignments to date omit `due` entirely; canvas-author should not invent a `due` field unless the PRD item specifies one. (Synthesize What You Heard, id=17, failed on first push.)

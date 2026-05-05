# Codex Guide For Technical Users

## Your Job

Use Codex to accelerate repo-grounded work while keeping deterministic scripts in charge of side effects.

## Working Pattern

1. Open the repo root in Codex app or IDE.
2. Ask Codex to inspect `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, `canvas_sync/`, `schema/`, and the target course.
3. Define file scope and non-goals.
4. Let Codex edit local files.
5. Run targeted artifact validation.
6. Run full schema validation and tests when scope warrants it.
7. Review diffs before staging or publishing.

## Deterministic Boundaries

Use Python scripts for:

- Course shell setup: `canvas_sync/init_course.py`.
- Artifact, manifest, and PRD validation: `canvas_sync/schema.py`.
- Canvas push: `canvas_sync/push.py`.
- Canvas inspection: `canvas_sync/inspect_canvas.py`.
- Reconcile dry run and apply: `canvas_sync/pull.py`.
- Manifest-backed Canvas removal: `canvas_sync/remove.py`.

Do not replace these with loose LLM reasoning. Codex should orchestrate them, not reimplement them.

## Extension Decisions

Create a new skill when a repeated workflow needs reliable routing, inputs, validation, and guardrails. Create a subagent when the work benefits from separate role instructions, isolated context, or parallel execution. Create a deterministic script when the workflow writes to Canvas, changes manifests, handles credentials, or needs repeatable parsing.

## Known Technical Gaps

- Current GitHub workflow paths include `course1/**` and `course2/**`, but not `course3/**`.
- The due-date schema and Canvas timestamp guidance should be reconciled before adding due dates to artifacts.
- `.claude/settings.local.json` remains as a historical local settings file and should not be treated as the active orchestration path.

# Codex Migration Plan

## Current Status

The scaffold from this plan has been implemented and the legacy Claude Code orchestration files have been removed from the active runtime. Remaining work is validation against a sandbox Canvas course.

## Target-State Architecture

**Repo facts**

- Canvas state and course content are already file-backed.
- Python scripts own validation, push, pull, and Canvas API behavior.
- Codex now supplies orchestration guidance, role prompts, and operator workflows. The legacy Claude runtime files have been removed.

**External facts**

- Codex uses `AGENTS.md` for durable repo guidance.
- Codex skills are reusable workflow packages available to CLI, IDE, and app.
- Codex supports subagents and Codex-as-MCP-server orchestration, but neither is a direct `.claude` file replacement.

**Recommendation**

Use this smallest viable target:

- `AGENTS.md` is the root guidance and build memory.
- `.agents/skills/*` holds repeatable workflows.
- `.codex/agents/*` holds only role-specialized LLM workers that need separate context.
- `canvas_sync/*` stays as the side-effect boundary.
- `build-course` is the full-course path: generate local Markdown, validate, review, then optionally push.
- Legacy Claude files have been removed; Codex is the supported runtime.

## Migration Strategy

- Migrate from narrow to broad workflows.
- Replace mechanical Claude subagents with direct script calls.
- Keep the migration audit for history, but do not reintroduce the Claude runner unless a rollback is explicitly requested.
- Require explicit approval for Canvas writes in interactive workflows.

## Phased Plan

### Phase 0: Establish Audit Artifacts And Decision Criteria

- **Objective:** Make the migration evidence explicit and reviewable.
- **Scope:** `docs/codex-migration/*`.
- **Expected changes:** Add repo audit, compatibility matrix, migration plan, and open questions.
- **Risks:** The docs can drift from code if future changes skip updates.
- **Validation:** `python3 canvas_sync/schema.py --all`; review links and file references.
- **Exit criteria:** Maintainers accept these docs as the migration source of truth.

### Phase 1: Isolate Claude-Specific Orchestration Surfaces

- **Objective:** Ensure every Claude dependency has a known target.
- **Scope:** Legacy shell runner, legacy prompt, `.claude/*`, `CLAUDE.md`, `README*`.
- **Expected changes:** Add inventory and compatibility docs, then remove Claude files once Codex scaffolding exists.
- **Risks:** Hidden user-level Claude settings may still affect local behavior but are outside repo scope.
- **Validation:** Repeat `rg -i 'claude|anthropic|mcp|codex|subagent|permission|approval'`.
- **Exit criteria:** All Claude surfaces are classified as hard dependency, optional integration, docs, or stale.

### Phase 2: Define Codex Target Architecture And Migration Seams

- **Objective:** Establish Codex-native instruction and workflow locations.
- **Scope:** `AGENTS.md`, `.agents/skills/*`, `.codex/*`, `prompts/codex/*`.
- **Expected changes:** Add Codex skills, selected agent configs, and a project Codex config.
- **Risks:** Codex sandbox and approval semantics are not a direct match for Claude `bypassPermissions`.
- **Validation:** Start Codex in read-only or approval-gated mode and confirm it sees `AGENTS.md` and skills.
- **Exit criteria:** Codex can explain the intended workflow without reading `.claude` files.

### Phase 3: Implement A Small Pilot Migration Path

- **Objective:** Prove a narrow Codex workflow before broad migration.
- **Scope:** `sync` skill and existing `canvas_sync/schema.py` / `canvas_sync/push.py`.
- **Expected changes:** Codex skill validates one MD artifact, resolves the manifest, and pushes only after explicit approval.
- **Risks:** Canvas writes are real side effects.
- **Validation:** First run schema-only; then use a sandbox Canvas course for one controlled push.
- **Exit criteria:** A known artifact can be updated safely through Codex.

### Phase 4: Migrate Remaining Orchestration Components

- **Objective:** Reach day-to-day workflow parity and one full-course build path.
- **Scope:** `add-artifact`, `update-dues`, `reconcile`, `build-sprint`, `build-course`, planner/author prompts.
- **Expected changes:** Convert workflows to Codex skills, convert planner/author to Codex agents or skills, and add a single-pass full-course build workflow.
- **Risks:** LLM output quality may change; unattended runner behavior may differ; Canvas writes need approval policy testing.
- **Validation:** Build one `course2` sprint locally in review mode before pushing; run `schema.py --all`.
- **Exit criteria:** Codex handles daily operations and one full-course dry run.

### Phase 5: Remove Deprecated Claude-Specific Code And Update Docs/Tests/Ops

- **Objective:** Make Codex the primary runtime after parity.
- **Scope:** `.claude/*`, `CLAUDE.md`, `README*`, CI paths.
- **Expected changes:** Delete Claude config and runner, update operator docs.
- **Risks:** Removing Claude loses the immediate old-runner rollback path.
- **Validation:** Keep the Claude runner available until Codex completes a real workflow.
- **Exit criteria:** New operators can run documented workflows without installing Claude Code.

## Pilot Recommendation

Start with the Codex `sync` skill. It has the smallest behavioral surface:

1. Resolve a single artifact path under `course*/sprints/`.
2. Run `python3 canvas_sync/schema.py --artifact <file>`.
3. Resolve `course<N>/manifests/production.json`.
4. Ask for explicit confirmation before Canvas write.
5. Run `python3 canvas_sync/push.py --file <file> --manifest <manifest>`.
6. Report the JSON result and commit only if the user requested it.

## Rollback / Fallback

- Legacy shell runner, `.claude/*`, and `CLAUDE.md` have been removed. Rollback would require restoring them from git history.
- Do not modify `canvas_sync/*` for the first pilot.
- If Codex runner behavior is unreliable, use Codex as an MCP server from a small OpenAI Agents SDK orchestrator.
- If Canvas push fails, rely on manifest idempotency and do not retry in the same workflow unless a human confirms.

## Validation Strategy

- Always run `python3 canvas_sync/schema.py --all` after migration scaffolding changes.
- Run `git diff --check` before finalizing.
- Use a sandbox Canvas course for the first push.
- Confirm CI now watches `course1/**` and `course2/**`.
- Confirm Codex sees `AGENTS.md` and the relevant skills.

## Acceptance Criteria

- Audit docs exist under `docs/codex-migration/`.
- CI path globs match the actual repo layout.
- `AGENTS.md` contains operational Codex guidance and preserves `## Learnings`.
- Codex skills exist for daily workflows.
- Codex planner and author surfaces exist.
- `build-course` exists for full-course local generation from one course context spec.
- No application code or Canvas sync behavior changed in the initial migration scaffold.

## Implementation Backlog

1. Add audit docs.
2. Fix CI course path globs.
3. Add Codex guidance to `AGENTS.md`.
4. Add `.agents/skills/sync`.
5. Add remaining Codex workflow skills.
6. Add `.codex/agents/sprint-planner.toml`.
7. Add `.codex/agents/canvas-author.toml`.
8. Add `build-course`.
9. Pilot one schema-only full-course generation, then one sandbox Canvas push.

## Sources

- Codex CLI: https://developers.openai.com/codex/cli
- Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Codex skills: https://developers.openai.com/codex/skills
- Codex subagents: https://developers.openai.com/codex/subagents
- Codex as MCP server: https://developers.openai.com/codex/guides/agents-sdk
- Claude subagents: https://code.claude.com/docs/en/sub-agents
- Claude settings: https://code.claude.com/docs/en/settings

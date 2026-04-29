# Codex Migration Open Questions

## Human Clarifications Needed

- Which Canvas course should be used as the sandbox for the first Codex-driven push?
- Should the old Claude runner remain restorable from git history only, or should a tagged archive branch be created for rollback?
- Should the optional n8n grading workflow migrate to OpenAI now, or remain Anthropic-backed until build orchestration is complete?
- Who should approve Canvas-writing Codex runs: the local operator only, or a named course owner?
- Should `codex-ralph.sh` ever run with a dangerous bypass mode, or should unattended Canvas builds require a separate orchestrator with explicit guardrails?

## Assumptions That Might Be Wrong

- Codex `exec` is sufficient for the Ralph loop without moving to Codex-as-MCP-server orchestration.
- Existing prompts can be ported with minimal behavior changes once Claude metadata is removed.
- `AGENTS.md` can carry both durable operating rules and accumulated build memory without becoming too long for effective instruction loading.
- Course2 remains the safest pilot target because it is less built out than course1.
- Canvas sync scripts do not need provider-specific changes.

## Decisions Before Full Implementation

- Choose the Codex model mapping for planning, authoring, and lightweight workflows.
- Decide whether Codex project config should include active command rules/hooks or only documented approval expectations.
- Decide whether to create a tagged archive branch for the removed Claude runtime.
- Decide how to document operator commands: skills only, README recipes, or small wrapper scripts.
- Decide whether commits remain part of agent workflows or become explicit human-controlled steps.

## Blockers To Resolve During Pilot

- Verify Codex approval behavior for `python3 canvas_sync/push.py`.
- Verify that Codex can access local `.env` only when intended.
- Verify that a failed Canvas push does not corrupt manifests.
- Verify that Codex skill discovery works from the repository root.
- Verify that CI catches course changes after path fixes.

## Source Links

- Codex CLI: https://developers.openai.com/codex/cli
- Codex config reference: https://developers.openai.com/codex/config-reference
- Codex skills: https://developers.openai.com/codex/skills
- Codex subagents: https://developers.openai.com/codex/subagents
- Codex MCP: https://developers.openai.com/codex/mcp
- Claude settings and permissions: https://code.claude.com/docs/en/settings

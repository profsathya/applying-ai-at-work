# Codex Migration Repo Audit

## Current Status

The legacy Claude Code orchestration files identified in this audit have now been removed from the active runtime. The audit preserves the pre-removal evidence so future maintainers can understand what was migrated.

## Executive Summary

This repository is split into a portable Canvas sync backend and a Codex orchestration layer. The Canvas backend in `canvas_sync/`, the course state in `course*/`, and the schemas in `schema/` are preserved. The previous Claude-specific runner, prompt, agents, commands, and permissions were replaced by Codex guidance, skills, and custom agents.

## Evidence Legend

- **Repo fact:** observed directly in this repository.
- **External fact:** verified from current official documentation during the audit.
- **Recommendation:** implementation judgment based on repo facts plus external facts.

## Current Orchestration Overview

**Pre-removal repo facts**

- Initial course builds previously started in a legacy shell runner, which repeatedly called `claude -p` with a file-backed prompt and `--permission-mode bypassPermissions`.
- The legacy prompt was a file-backed state machine. It checked scaffold integrity, selected a target course, then entered PLAN, BUILD, or VERIFY.
- PLAN invokes `sprint-planner`; BUILD invokes `canvas-author`, `schema-validator`, and `canvas-pusher`; VERIFY runs manifest and schema checks.
- Day-to-day operations are Claude slash commands under `.claude/commands/`: `add-artifact`, `build-sprint`, `sync`, `reconcile`, and `update-dues`.
- The actual Canvas integration is deterministic Python:
  - `canvas_sync/schema.py` validates artifacts, manifests, and PRDs.
  - `canvas_sync/push.py` writes Markdown artifacts to Canvas and updates legacy manifests or external deployment state.
  - `canvas_sync/pull.py` reconciles Canvas drift back into Markdown.
  - `canvas_sync/canvas_client.py` wraps Canvas REST API calls.

**External facts**

- Codex reads `AGENTS.md` automatically with layered project/global discovery. Source: https://developers.openai.com/codex/guides/agents-md
- Codex skills package reusable workflows in `.agents/skills/<name>/SKILL.md`. Source: https://developers.openai.com/codex/skills
- Codex supports subagents, but custom agent definitions are Codex-specific and do not read `.claude/agents/*.md`. Source: https://developers.openai.com/codex/subagents

**Implemented recommendation**

The Canvas sync layer stayed unchanged. Claude orchestration was removed from the active runtime and replaced with Codex guidance, skills, selected Codex agents, and a Codex runner.

## Legacy Claude-Related Inventory

| Path | Role | Classification | Notes |
|---|---|---|---|
| `.claude/agents/*.md` | Specialized worker prompts | hard production dependency | Uses Claude frontmatter: `name`, `description`, `tools`, `model`, `color`. |
| `.claude/commands/*.md` | Operator workflows | hard production dependency | Claude slash commands. Codex does not consume these directly. |
| `.claude/settings.json` | Claude permissions | hard production dependency | Claude-specific allow/deny syntax and Bash matchers. |
| `.claude/settings.local.json` | Local push allowance | development-only dependency | Gitignored local override. |
| `CLAUDE.md` | Operational conventions | development/runtime guidance | Must be merged into `AGENTS.md` for Codex. |
| `AGENTS.md` | Build memory and now Codex guidance | runtime guidance | Codex-native durable repo instructions. |
| `README.md`, `README-BUILDER.md` | Operator and technical docs | documentation-only reference | Currently Claude-first; should be updated after Codex pilot. |
| `course1/sprints/.../assumption-audit-with-ai.md` | Participant-facing example | documentation-only reference | Mentions Claude as one possible learner tool. |

## Dependency Classification

**Removed hard production dependencies**

- `.claude/agents/*.md`
- `.claude/commands/*.md`
- `.claude/settings.json`

**Removed or historical development-only dependencies**

- `.claude/settings.local.json`
- Claude installation instructions in `README.md` and `README-BUILDER.md`
- Claude-specific gotchas in `CLAUDE.md` and `AGENTS.md`

**Documentation-only references**

- Participant-facing mentions of Claude alongside ChatGPT, Gemini, and Copilot.
- Historical build notes in `AGENTS.md` and `context/build-notes/`.

**Dead, stale, or ambiguous**

- `.github/workflows/*` referenced `courses/**` even though the repo uses `course1/` and `course2/`. This has been fixed.
- `.claude/commands/sync.md` and `.claude/commands/reconcile.md` mention `courses/<course-slug>/manifests/`, also stale relative to repo layout.
- `config/README.md` and `scripts/README.md` still describe placeholder future work.
- No repo-local MCP config was found.
- No repo-local Codex config existed before this migration scaffold.

## Runtime Flow

**Repo facts**

1. Operator asks Codex to use a skill.
2. Full-course builds use `build-course` to read a course context spec or pasted context.
3. Codex writes Markdown under `course*/sprints/sprint-*`.
4. Validation runs before every push.
5. `push.py` writes to Canvas and updates `canvas-state` for GitOps publishing or `course*/manifests/production.json` for legacy local pushes.
6. The workflow reports changed files and asks before Canvas writes.

## Implicit Behavior Needing Documentation

- `course*/prd.json` is a queue and checkpoint, not a hand-edited source of truth.
- `canvas-state` is the production Canvas ID store. `course*/manifests/production.json` remains the static course config and legacy local state store.
- `AGENTS.md` is build memory and Codex guidance; keep `## Learnings` intact because existing prompts append there.
- Canvas push side effects are real and should require explicit approval outside the autonomous build runner.
- Claude subagent model labels encode workload type, not just model preference: planning/design, authoring/date editing, and mechanical script execution.

## Stale Or Risky Areas

- CI path globs must match `course1/**` and `course2/**`.
- Claude permissions did not map directly to Codex. The replacement uses Codex project config plus explicit skill-level safety rules.
- Cloud Codex is not the default target for Canvas writes because secrets, internet access, and side-effect approvals need deliberate setup.

## External Sources

- OpenAI Codex CLI: https://developers.openai.com/codex/cli
- OpenAI AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- OpenAI skills: https://developers.openai.com/codex/skills
- OpenAI MCP: https://developers.openai.com/codex/mcp
- OpenAI subagents: https://developers.openai.com/codex/subagents
- OpenAI Codex with Agents SDK: https://developers.openai.com/codex/guides/agents-sdk
- Claude subagents: https://code.claude.com/docs/en/sub-agents
- Claude hooks: https://code.claude.com/docs/en/hooks
- Claude settings: https://code.claude.com/docs/en/settings
- Claude Agent SDK: https://code.claude.com/docs/en/agent-sdk/overview

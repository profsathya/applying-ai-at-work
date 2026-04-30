# Claude To Codex Compatibility Matrix

## Current Status

This matrix records the legacy Claude mechanisms that were migrated. The old Claude runtime files are no longer active; restore from git history only if a rollback is explicitly requested.

## Legend

- **Repo fact:** observed directly in this repository.
- **External fact:** verified from official docs.
- **Recommendation:** migration design choice.

| Mechanism | Current files | Current role | Claude-specific dependency | Recommended Codex replacement | Difficulty | Confidence | Evidence |
|---|---|---|---|---|---|---|---|
| Project guidance | `CLAUDE.md` | Core repo conventions | Codex does not read it by default | Essential rules merged into `AGENTS.md` | low | high | Legacy file removed after migration. |
| Build memory | `AGENTS.md` | Accumulated gotchas | Previously treated as memory only | Keep and expand as Codex root guide with build learnings preserved | low | high | Repo fact: build workflows preserve `## Learnings`. |
| Planner worker | `.claude/agents/sprint-planner.md` | Course design to PRD | Claude agent Markdown frontmatter and model alias `opus` | Codex custom agent plus `sprint-planner` skill | medium | high | External fact: Codex custom agents and skills use different file formats. |
| Author worker | `.claude/agents/canvas-author.md` | One PRD item to Markdown artifact | Claude agent Markdown frontmatter and model alias `sonnet` | Codex custom agent plus `canvas-author` skill | medium | high | Role prompt body is portable; metadata is not. |
| Mechanical validator | `.claude/agents/schema-validator.md` | Runs `schema.py` | Unnecessary LLM wrapper | Direct script call inside skills and runner | low | high | Repo fact: validation is deterministic Python. |
| Mechanical pusher | `.claude/agents/canvas-pusher.md` | Runs `push.py` | Unnecessary LLM wrapper plus Claude permissions | Direct script call gated by explicit approval | low | high | Repo fact: `push.py` owns Canvas side effects and manifest updates. |
| Mechanical puller | `.claude/agents/canvas-puller.md` | Runs `pull.py` | Unnecessary LLM wrapper | Direct script call with dry-run first | low | high | Repo fact: `pull.py` has `--dry-run` and `--apply`. |
| Date updater | `.claude/agents/due-date-updater.md` | Surgical frontmatter edits from NLP | Claude agent frontmatter | Codex skill with same rules; use direct edits and validation | medium | high | Prompt body is portable; tool restrictions need Codex policy. |
| Sprint builder | `.claude/agents/sprint-module-builder.md` | Coherent sprint authoring | Claude agent frontmatter and model alias `opus` | Codex skill, optionally custom agent for high-context authoring | medium | medium | Needs pilot because output quality is design-sensitive. |
| Add artifact command | `.claude/commands/add-artifact.md` | One new artifact workflow | Claude slash command discovery | Codex skill `add-artifact` | medium | high | Codex skills are workflow packages. |
| Build sprint command | `.claude/commands/build-sprint.md` | Multi-artifact workflow | Claude slash command discovery | Codex skill `build-sprint` | medium | high | Requires explicit push approval. |
| Sync command | `.claude/commands/sync.md` | Push edited MD to Canvas | Claude slash command discovery | Codex pilot skill `sync` | low | high | Best first pilot because it is script-backed. |
| Reconcile command | `.claude/commands/reconcile.md` | Pull Canvas drift | Claude slash command discovery | Codex skill `reconcile` | low | high | Must preserve dry-run before apply. |
| Update dues command | `.claude/commands/update-dues.md` | Edit due fields and optionally push | Claude slash command discovery | Codex skill `update-dues` | medium | high | Needs careful target resolution. |
| Permissions | `.claude/settings.json` | Allows and denies tools | Claude matcher syntax | Codex sandbox and approval policy; optional hooks/rules later | high | medium | External fact: Codex uses `approval_policy` and `sandbox_mode`. |
| MCP | none found | Not currently used | none | Optional `.codex/config.toml` MCP entries later | low | high | External fact: Codex MCP config uses `config.toml`. |
| CI path filters | `.github/workflows/*.yml` | Schema and reconcile checks | stale path, not Claude-specific | Replace `courses/**` with `course1/**` and `course2/**` | low | high | Repo fact: course roots are `course1/` and `course2/`. |

## Model Mapping Recommendation

This is a recommendation, not an externally guaranteed mapping:

| Claude role label | Repo use | Codex target |
|---|---|---|
| `opus` | planning, sprint-level design, course decomposition | strongest available Codex coding/reasoning model, high reasoning |
| `sonnet` | artifact authoring and due-date interpretation | default Codex model, medium/high reasoning |
| `haiku` | script execution and validation summaries | direct script calls first; if an agent is needed, use a lower-cost Codex model |

## Sources

- Codex CLI: https://developers.openai.com/codex/cli
- Codex AGENTS.md: https://developers.openai.com/codex/guides/agents-md
- Codex skills: https://developers.openai.com/codex/skills
- Codex subagents: https://developers.openai.com/codex/subagents
- Codex MCP: https://developers.openai.com/codex/mcp
- Claude subagents: https://code.claude.com/docs/en/sub-agents
- Claude hooks: https://code.claude.com/docs/en/hooks
- Claude settings: https://code.claude.com/docs/en/settings

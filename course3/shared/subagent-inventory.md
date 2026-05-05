# Subagent And Skill Inventory

This inventory was created by inspecting `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, `.codex/config.toml`, README files, Canvas scripts, and workflow docs.

## Repo-Local Custom Agents

| Agent | File | Use when | Inputs | Outputs | Guardrails |
|---|---|---|---|---|---|
| `course-drafter` | `.codex/agents/course-drafter.toml` | Drafting a full course or one module from context. | Target course, sprint or whole-course scope, context spec or pasted context. | Canvas-native Markdown under `<course>/sprints/sprint-<n>/`, validation report. | No manifest edits, no Canvas push without approval, no due dates unless explicit. |
| `course-configurator` | `.codex/agents/course-configurator.toml` | Creating a local course shell for an existing Canvas course. | Course key, Canvas course ID, base URL, title, optional term and context. | Local course folders, manifest, PRD, progress, design notes, context spec. | Local files only. Does not create a Canvas course. |
| `sprint-planner` | `.codex/agents/sprint-planner.toml` | Planning from existing design into PRD and metadata. | Target course and brief/design files. | PRD, course metadata, progress, empty manifest. | Does not write artifact bodies or push to Canvas. |
| `canvas-author` | `.codex/agents/canvas-author.toml` | Writing exactly one artifact from a PRD-shaped item. | One PRD-shaped item and target course. | One Markdown artifact. | Artifact only. No manifests, design docs, schemas, or Canvas IDs. |
| `canvas-inspector` | `.codex/agents/canvas-inspector.toml` | Inspecting live Canvas modules, items, manifest alignment, and drift readiness. | Target course manifest, whether to include items or drift. | Local ledger under `<course>/reports/` and summary. | Read-only against Canvas. No push or apply. |
| `canvas-remover` | `.codex/agents/canvas-remover.toml` | Removing manifest-backed Canvas modules or items. | Target course, ledger, manifest-backed targets. | Dry-run removal plan, confirmation token, optional apply result. | Fresh inspection first, exact token required, no Canvas-only deletes, local Markdown kept. |

## Repo-Local Skills

| Skill | File | Use when | Verification |
|---|---|---|---|
| `build-course` | `.agents/skills/build-course/SKILL.md` | Generate a full course locally from a course context spec or pasted context. | Validate each artifact and run full schema validation. |
| `build-sprint` | `.agents/skills/build-sprint/SKILL.md` | Generate one sprint or Canvas module locally. | Validate each generated artifact. |
| `add-artifact` | `.agents/skills/add-artifact/SKILL.md` | Add exactly one page, assignment, discussion, quiz, or module header. | Validate the new artifact. |
| `canvas-author` | `.agents/skills/canvas-author/SKILL.md` | Author one artifact from a PRD-shaped item. | Validate the artifact. |
| `configure-course` | `.agents/skills/configure-course/SKILL.md` | Configure a local course shell for an existing Canvas course. | Validate manifest and PRD. |
| `inspect-canvas` | `.agents/skills/inspect-canvas/SKILL.md` | Read live Canvas inventory and write a local ledger. | Check ledger paths and summary. |
| `reconcile` | `.agents/skills/reconcile/SKILL.md` | Pull Canvas-side drift back locally. | Dry run first, apply only after approval. |
| `remove-canvas` | `.agents/skills/remove-canvas/SKILL.md` | Remove manifest-backed Canvas items. | Inspect, dry run, exact token, validate manifest after apply. |
| `sync` | `.agents/skills/sync/SKILL.md` | Push reviewed artifacts to Canvas. | Validate first, push serially, report Canvas IDs. |
| `update-dues` | `.agents/skills/update-dues/SKILL.md` | Update only due fields. | Validate changed files and ask before push. |
| `sprint-planner` | `.agents/skills/sprint-planner/SKILL.md` | Build PRD and metadata from existing design. | Validate PRD and manifest. |

## Example Prompts

```text
Use the repo-local course-drafter for course3 sprint 2. Draft local Markdown only, validate it, and stop before Canvas.
```

```text
Use canvas-inspector for course3. Include module items and drift, write the local ledger, and do not apply anything.
```

```text
Choose the safest repo-local skill or subagent for removing a Canvas item. Explain the dry-run and confirmation-token process before doing anything.
```

## Known Limitations

- Learners should not need to memorize names. They should ask Codex to select and explain the route.
- Subagent visibility differs by Codex surface. The app surfaces subagent activity; IDE visibility may be less explicit.
- The local deterministic scripts still require correct credentials for Canvas operations.
- The legacy `.claude/settings.local.json` file is not the active workflow.

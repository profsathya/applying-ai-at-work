# Internal Implementation Note

Generated for `course3`, Canvas course ID `181`, on 2026-05-05.

## Repository Findings

- The repo builds Canvas LMS materials from Canvas-native Markdown.
- The supported workflow is plain-English request, local Markdown draft, validation, human review, and explicit Canvas push.
- `AGENTS.md` is the root Codex guidance file and includes safety rules, style conventions, file conventions, and build learnings.
- `.agents/skills/` contains repeatable Codex workflows.
- `.codex/agents/` contains project-scoped subagent definitions.
- `canvas_sync/` owns deterministic validation, setup, inspection, push, pull, and removal.
- `course3/manifests/production.json` maps the local course to Canvas course ID `181`.

## Research Findings Applied

- Codex works best with clear goal, context, constraints, and done criteria.
- Codex app and IDE support repo-grounded workflows, review, diffs, skills, and configuration.
- Skills can be invoked explicitly or selected implicitly by task description.
- Subagents are useful for parallel or role-specialized work, but should be requested explicitly.
- Review and verification are part of the workflow, not optional cleanup.

## Build Choices

- Used `course3` as the course root because the repo already had a configured course shell.
- Mapped exactly four modules to `sprint-0` through `sprint-3`.
- Kept Canvas publish state as `publish: false` in new course artifacts until human review.
- Created shared resources under `course3/shared/`.
- Did not run Canvas writes.

## Ambiguities To Resolve Later

- Whether course3 should remain titled only for internal training or receive a Canvas-visible code and term.
- Whether the GitHub validation workflow should include `course3/**`, because current workflow paths include `course1/**` and `course2/**`.
- Whether the frontmatter `due` schema should accept timezone suffixes. Repo guidance says Canvas requires timezone, while the current schema pattern does not accept `Z`.

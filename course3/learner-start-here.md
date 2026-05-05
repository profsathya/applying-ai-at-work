# Learner Start Here

## Who This Course Is For

This course is for team members who need to use the `applying-ai-at-work` repository with Codex. You may be technical, non-technical, or somewhere in between. You do not need to know Canvas APIs, Git, Python, or agent terminology before starting.

## What You Will Be Able To Do

By the end, you will be able to:

- Explain what this repo builds and where the important files live.
- Open the repo in the Codex app or an IDE with Codex installed.
- Ask Codex to inspect before making changes.
- Scope a safe request for a course, module, artifact, inspection, reconcile, due-date update, or Canvas push.
- Ask Codex to choose the right local skill or subagent.
- Review changed files before accepting or publishing.
- Verify local Markdown, schema validation, and Canvas readiness.
- Document blockers and recover when Codex misunderstands a request.

## What You Need Before Starting

- Local access to this repository.
- The Codex app or an IDE with Codex installed.
- Permission to view the repo files.
- A clear answer from a maintainer about whether Canvas publishing is allowed for your task.
- For technical setup only: access to Python, the repo virtual environment, and Canvas credentials if you are authorized to inspect or publish.

Do not start by asking Codex to push to Canvas. Start by asking it to inspect the repo and explain the relevant workflow.

## How To Use The Course

Use the modules in order. Each module has:

- A short overview.
- Practical pages.
- A formative check.
- An applied task.
- Technical expansion notes where useful.

If you are non-technical, focus on the pages, examples, and review checklists. If you are technical, also read the command reference and extension guidance.

## Choosing A Path

Non-technical path:

1. Use Codex app or the IDE sidebar.
2. Ask Codex to inspect files and explain what it found.
3. Use prompt starters from `course3/shared/codex-prompt-patterns.md`.
4. Review titles, instructions, artifact order, and safety boundaries.
5. Ask a maintainer before running any Canvas write.

Technical path:

1. Use Codex app or IDE Agent mode with the repo open.
2. Let Codex inspect `AGENTS.md`, `.agents/skills/`, `.codex/agents/`, `canvas_sync/`, and `schema/`.
3. Run local validation when Codex changes files.
4. Review Git diffs and check schema/test output.
5. Use the deterministic scripts for setup, validation, inspection, push, pull, and removal.

## Using Codex App Or IDE

In the Codex app, select this project folder and choose Local for normal repo work. In an IDE, open the repository root and use the Codex sidebar. You can mention files in your prompt when you know they matter, but you can also ask Codex to discover the relevant files first.

Good first prompt:

```text
Inspect this repo before changing anything. Summarize the course-building workflow, the local skills and subagents, the Canvas safety rules, and the validation commands. Do not edit files.
```

## Avoiding Accidental Production Changes

Use these phrases when you want local-only work:

```text
Generate local Markdown only. Validate the files. Stop before Canvas.
```

```text
Inspect Canvas read-only and write the local ledger. Do not push, pull apply, or remove anything.
```

```text
Show me the proposed file list and plan before editing.
```

Canvas publishing is allowed only when you explicitly say which reviewed files should be pushed.

## Getting Help Or Documenting Blockers

If Codex cannot proceed safely, ask it to document the blocker:

```text
Stop and write a short blocker note. Include what you inspected, what is missing, what risk remains, and the safest next question for a maintainer.
```

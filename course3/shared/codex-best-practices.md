# Codex Best Practices For This Repo

This summary adapts current official Codex guidance to the `applying-ai-at-work` repository.

## Sources Consulted

- [Codex app](https://developers.openai.com/codex/app)
- [Codex IDE extension](https://developers.openai.com/codex/ide)
- [Codex best practices](https://developers.openai.com/codex/learn/best-practices)
- [Codex prompting](https://developers.openai.com/codex/prompting)
- [AGENTS.md guidance](https://developers.openai.com/codex/guides/agents-md)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Codex subagents](https://developers.openai.com/codex/subagents)
- [Codex app review](https://developers.openai.com/codex/app/review)
- [Codex app worktrees](https://developers.openai.com/codex/app/worktrees)
- [Codex sandboxing](https://developers.openai.com/codex/concepts/sandboxing)

## Adapted Practices

### Start With Goal, Context, Constraints, And Done Criteria

For this repo, a strong Codex request names:

- Goal: the course, module, artifact, inspection, or maintenance task.
- Context: relevant paths such as `course3/`, `context/course-specs/`, `.agents/skills/`, or `canvas_sync/`.
- Constraints: local-only, no Canvas push, no manifest edits, no due dates, no HTML.
- Done criteria: validation passed, changed files listed, no Canvas writes, review notes included.

### Ask For Inspection Before Action

Use this when you are unsure:

```text
Inspect this repo and identify the right workflow before editing. Explain which files you read, which skill or subagent should apply, what is risky, and what you would verify. Do not change files yet.
```

### Use AGENTS.md As The Repo Contract

Codex reads `AGENTS.md` automatically when the repo is opened from the right root. In this repo, it defines the safety model, style conventions, Canvas side-effect rules, file paths, and migration guidance.

### Let Codex Select Skills, But Ask It To Explain The Route

Skills under `.agents/skills/` can be selected explicitly or implicitly. Learners do not need to memorize every skill name. They should ask:

```text
Choose the safest repo-local skill or subagent for this task and explain the route before acting.
```

### Use Subagents Deliberately

Subagents are useful for role-specialized or parallel work, but Codex spawns them only when explicitly asked. For this repo, ask for a subagent when the task clearly matches a local custom agent such as `course-drafter`, `canvas-inspector`, or `canvas-remover`.

### Review Is Part Of The Work

Use the Codex app review pane or IDE diff tools to inspect changes. Review all uncommitted changes, not only what Codex says it edited. This matters because the review pane reflects the Git working tree.

### Keep Permissions Tight

Default app and IDE settings should keep sandboxing and approvals active. Loosen permissions only for trusted workflows and only when the task requires it. Canvas writes remain human-approved even when local file edits are allowed.

### Split Large Work

Good split for this repo:

1. Inspect and route.
2. Draft local Markdown.
3. Validate.
4. Review files and diff.
5. Inspect Canvas if live-course drift matters.
6. Push only after explicit approval.

### Treat External Context As Untrusted Until Verified

When Codex uses web search, Canvas, GitHub, or other connected tools, ask it to cite what it used and explain what it inferred. For course publishing, local repo rules and Canvas inspection results should override assumptions.

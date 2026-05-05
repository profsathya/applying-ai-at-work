# Codex Guide For Non-Technical Users

## Your Job

You do not need to know the internal command names. Your job is to describe the outcome, name the target course or module, set boundaries, and review the result.

## What To Tell Codex

Include:

- What you want to produce or inspect.
- Which course or module matters.
- What source material Codex should use.
- Whether Canvas publishing is allowed.
- What you want Codex to show you before and after work.

## Safe Prompt

```text
I want to update course3 locally. Inspect the repo first and choose the right workflow. Do not push to Canvas. Show me the plan, the files you expect to change, and how I should review the result.
```

## What To Review

Focus on the learner experience:

- Would a new team member know what to do?
- Is the warning about Canvas clear?
- Are there too many steps at once?
- Does the activity ask for real evidence?
- Does the wording avoid jargon or define it?
- Does the content fit this actual repo?

## When To Ask For Help

Ask a maintainer when:

- Codex mentions tokens, API keys, `.env`, or Canvas credentials.
- Codex wants to push to Canvas.
- Codex wants to apply reconcile changes.
- Codex wants to delete or remove Canvas content.
- Validation fails and the fix is not obvious.

## What Not To Do

- Do not paste real API tokens into Codex prompts.
- Do not approve a Canvas push because validation passed. Review content first.
- Do not ask Codex to "fix everything" without naming scope.
- Do not treat Canvas as a sandbox unless a maintainer confirms it is one.

# Subagent Routing Guide

## Plain-Language Rule

Tell Codex the job. Ask it to choose the safest repo-local workflow. You do not need to memorize every subagent name.

## Routing Prompt

```text
I need to [task]. Inspect the repo instructions and choose the safest local skill or subagent. Explain the route, expected inputs, expected outputs, risks, and verification steps before changing files or calling Canvas.
```

## Common Routes

| Task | Ask Codex to use | Why |
|---|---|---|
| Draft a whole course | `course-drafter` with `build-course` | It reads course context and writes local artifacts. |
| Draft one module | `course-drafter` with `build-sprint` | It infers module scaffolding and validates files. |
| Add one artifact | `add-artifact` and `canvas-author` | It keeps the work to one file. |
| Configure a course shell | `course-configurator` with `configure-course` | It uses the deterministic setup script. |
| Inspect Canvas | `canvas-inspector` with `inspect-canvas` | It is read-only against Canvas and writes a ledger. |
| Pull Canvas drift | `reconcile` | It dry-runs first and applies only after approval. |
| Push reviewed files | `sync` | It validates and calls `push.py` serially. |
| Remove Canvas items | `canvas-remover` with `remove-canvas` | It inspects, dry-runs, and requires a token. |
| Update due dates | `update-dues` | It edits only due fields and validates. |

## How To Verify The Route

Ask Codex to report:

- The skill or subagent it chose.
- The instruction file it followed.
- The deterministic script it will use, if any.
- The files it expects to read or change.
- The validation it will run.
- Whether Canvas will be read, written, or untouched.

## When To Avoid Subagents

Avoid subagents for a tiny single-file correction, a simple explanation, or any task where parallel work could create conflicting edits. Use a subagent when the work is specialized, high-context, or can be split cleanly.

## If Direct Invocation Is Not Visible

In some IDE flows, you may not see a separate subagent panel. That does not mean the route is unsafe. Ask Codex to document the simulated route:

```text
If direct subagent invocation is unavailable here, document which repo-local subagent should be used, why, the exact prompt you would pass to it, and how I can verify the outcome.
```

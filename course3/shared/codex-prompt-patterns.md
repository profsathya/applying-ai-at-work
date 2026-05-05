# Codex Prompt Patterns

## Inspect Before Acting

```text
Inspect this repo before making changes. Read AGENTS.md, README.md, README-BUILDER.md, .agents/skills, .codex/agents, and the relevant course folder. Summarize the workflow, risks, and recommended next step. Do not edit files.
```

## Ask Codex To Route To The Right Skill Or Subagent

```text
I need to [describe task]. Choose the safest repo-local skill or subagent for this task. Explain why, list the expected inputs and outputs, and ask before any Canvas write.
```

## Local Course Or Module Draft

```text
Draft [course key] [sprint or module] from [source path or pasted context]. Generate Canvas-native Markdown only under the target sprint folder. Validate the files, list changed paths, and stop before Canvas.
```

## One Artifact

```text
Add one [page or assignment or discussion or quiz] to [course key] sprint [number] called "[title]". Use existing repo conventions. Validate the artifact and stop before Canvas.
```

## Read-Only Canvas Inspection

```text
Use canvas-inspector for [course key]. Include module items, write the local ledger, and report manifest alignment. Do not push, pull apply, or remove anything.
```

## Reconcile Dry Run

```text
Canvas may have changed for [course key]. Run the reconcile dry run only. Show drift and ask before applying anything.
```

## Reviewed Canvas Push

```text
Push these reviewed files to Canvas: [file list]. Validate first. Push serially through the repo sync workflow. Report Canvas IDs and manifest updates.
```

## Recovery When Codex Misunderstands

```text
Stop. The current direction is too broad. Re-scope to only [files or task]. Do not change Canvas. Explain what you already changed and what you will do next.
```

## Non-Technical User Starter

```text
I am not editing code directly. Help me use this repo safely. Inspect the relevant files, explain the workflow in plain language, and propose a local-only next step that I can review.
```

## Technical User Starter

```text
Inspect the repo workflow and identify the deterministic script path for this task. Then propose a minimal file scope, validation commands, expected outputs, and rollback or recovery steps before editing.
```

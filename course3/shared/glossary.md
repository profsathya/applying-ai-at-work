# Glossary

## Agent

An AI worker with instructions, tools, and context. In this repo, Codex is the main agent learners interact with.

## Applied Task

A practical learner activity where the learner uses Codex to inspect, plan, draft, review, or verify a repo workflow.

## Artifact

A Canvas-ready Markdown file under `<course>/sprints/sprint-<n>/`. Artifact types include `module_header`, `page`, `assignment`, `discussion`, and `quiz`.

## Canvas Manifest

The JSON file at `<course>/manifests/production.json`. It stores Canvas course ID and Canvas item IDs. Learners should not edit it manually.

## Canvas-Native Markdown

Markdown that can be rendered into Canvas content without HTML, iframes, JavaScript, inline styles, or external CDN references.

## Codex App

The desktop Codex interface used to open a project, run local threads, review diffs, use worktrees, and manage Git-oriented workflows.

## Codex IDE Extension

Codex inside an editor such as VS Code, Cursor, Windsurf, or JetBrains IDEs. It can use open files and selected code as context.

## Drift

A difference between live Canvas content and local Markdown or the local manifest.

## Local Draft

Markdown generated in the repo before any Canvas push. Local drafts are safe to review and validate before publication.

## Reconcile

The workflow that pulls Canvas-side changes back into local Markdown after a dry-run report and explicit approval.

## Skill

A reusable workflow package under `.agents/skills/`. Skills tell Codex how to handle repeated work such as building a sprint, syncing reviewed files, or inspecting Canvas.

## Subagent

A specialized Codex agent defined under `.codex/agents/` or built into Codex. Subagents are useful for specialized or parallel work when the user explicitly asks Codex to use them.

## Validation

Local checks that confirm Markdown, manifests, and PRDs follow repo schemas and guardrails.

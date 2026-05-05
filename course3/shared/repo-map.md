# Repository Map

## Plain-Language Map

This repo turns local Markdown files into Canvas course content. Codex helps draft and revise the files. Python scripts validate and, when authorized, publish or inspect Canvas.

## Main Directories And Files

| Path | What it does | Who needs it |
|---|---|---|
| `AGENTS.md` | Root instructions for Codex and repo-aware agents. | Everyone using Codex. |
| `README.md` | Everyday operator guide and prompt examples. | Everyone. |
| `README-BUILDER.md` | Technical builder reference. | Maintainers and technical learners. |
| `.agents/skills/` | Reusable Codex workflows for course building, sync, inspect, reconcile, removal, due dates, and setup. | Everyone indirectly, maintainers directly. |
| `.codex/agents/` | Project-scoped subagent definitions. | Learners asking Codex to route specialized work. |
| `.codex/config.toml` | Repo-level Codex defaults: workspace write, approval on request, multi-agent enabled. | Technical learners and maintainers. |
| `canvas_sync/` | Deterministic Canvas and schema scripts. | Technical learners and maintainers. |
| `schema/` | JSON schemas for artifact frontmatter, manifests, and PRDs. | Technical learners and reviewers. |
| `context/` | Shared design context and course/module spec templates. | Course authors and planners. |
| `course1/`, `course2/`, `course3/` | Local course directories. | Everyone working on a target course. |
| `<course>/sprints/sprint-<n>/` | Canvas artifact Markdown. | Course authors and reviewers. |
| `<course>/manifests/production.json` | Canvas IDs and sync state. | Scripts own this file. Humans review but do not hand-edit. |
| `<course>/reports/` | Canvas inspection ledgers. | Reviewers and reconcile workflows. |
| `.github/workflows/` | Schema validation and reconcile check automation. | Maintainers. |

## Course3 Map

`course3` is the local course shell for Canvas course ID `181`. This course adds local training content and shared resources:

```text
course3/
  learner-start-here.md
  course-map.md
  instructor-notes.md
  sprints/
    sprint-0/  Module 1
    sprint-1/  Module 2
    sprint-2/  Module 3
    sprint-3/  Module 4
  shared/
    Codex, subagent, review, troubleshooting, and checklist resources
  manifests/
    production.json
```

## What Can Go Wrong

- Starting Codex outside the repo root can hide local instructions and skills.
- Editing `production.json` manually can break Canvas ID tracking.
- Publishing before review can overwrite live Canvas content.
- Using old Claude files as active guidance can confuse the current Codex workflow.

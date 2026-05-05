# Using the Agentic Course Workflow

Subtitle: A practical self-paced course for configuring, operating, verifying, and extending this repository's agentic workflow.

This local course lives in `course3` and maps to Canvas course ID `181` through `course3/manifests/production.json`. The course is staged locally. Nothing in this build pushes to Canvas.

## Course Shape

The repo uses `sprints/` as the Canvas module source folder, so this four-module course uses four sprint folders:

| Course module | Repo folder | Purpose |
|---|---|---|
| Module 1: Orientation to the Repo, Codex, and the Agentic Workflow | `course3/sprints/sprint-0/` | Understand the repo, Codex app and IDE workflows, and human review responsibilities. |
| Module 2: Setup, Configuration, and Safe First Run | `course3/sprints/sprint-1/` | Prepare local dependencies, credentials, manifests, and a safe test workflow. |
| Module 3: Building and Publishing Content with Codex and Agents | `course3/sprints/sprint-2/` | Scope Codex tasks, route to local skills or subagents, draft content, and review changes. |
| Module 4: Verification, Maintenance, and Extension | `course3/sprints/sprint-3/` | Verify outputs, diagnose failure modes, maintain courses, and decide when to extend the workflow. |

## Start Here

Begin with `course3/learner-start-here.md`, then use `course3/course-map.md` to choose the technical or non-technical pathway.

The main workflow taught here is:

```text
open repo in Codex app or IDE -> ask Codex to inspect -> give a scoped task -> review plan -> let Codex edit local files -> validate -> review diffs -> decide whether Canvas push is allowed
```

## Safety Defaults

- Draft locally first.
- Ask Codex to report which files it read and changed.
- Keep Canvas publishing as a separate, explicit decision.
- Use placeholders such as `CANVAS_API_TOKEN`, `CANVAS_API_URL`, and `OPENAI_API_KEY`.
- Never paste real secrets into course content.
- Never manually write Canvas IDs into Markdown frontmatter.

## Key Shared Resources

- `course3/shared/repo-map.md`
- `course3/shared/subagent-inventory.md`
- `course3/shared/subagent-routing-guide.md`
- `course3/shared/codex-best-practices.md`
- `course3/shared/codex-review-checklist.md`
- `course3/shared/troubleshooting.md`

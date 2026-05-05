# Troubleshooting

## Codex Cannot Find The Repo Workflow

Likely cause: The project folder opened in Codex is not the repo root.

Recovery:

- In Codex app, select the folder containing `AGENTS.md`, `README.md`, `canvas_sync/`, and `course3/`.
- In an IDE, open the repository root, not a nested sprint folder.
- Ask Codex: `Show which repo instructions, skills, and agent files you can see. Do not edit files.`

## Codex Starts Making Changes Too Soon

Likely cause: The prompt did not ask for inspection or a plan first.

Recovery:

- Stop the thread or ask Codex to pause.
- Use: `Before editing, inspect the relevant files and propose a plan with file scope, risks, and verification steps.`

## Schema Validation Fails

Likely causes:

- Missing YAML frontmatter.
- Invalid slug format.
- `points` missing on assignments, quizzes, or graded discussions.
- Page has points.
- Body includes forbidden HTML or JavaScript.
- The file contains an em dash.

Recovery:

- Ask Codex to fix only the validation errors.
- Re-run validation on the changed files.
- Review the diff before accepting the fix.

## Canvas Push Fails With 401

Likely cause: Invalid or unauthorized `CANVAS_API_TOKEN`.

Recovery:

- Do not paste the token into chat.
- Ask a Canvas administrator or maintainer to verify token scope.
- Re-run a read-only connection check only when authorized.

## Canvas Push Fails With 404

Likely causes:

- Wrong Canvas course ID in `course3/manifests/production.json`.
- Wrong `CANVAS_API_URL`.
- User does not have access to the course.

Recovery:

- Confirm Canvas course ID `181` with a maintainer.
- Confirm the Canvas base URL.
- Do not manually edit manifest artifact IDs.

## Canvas Push Fails On Due Dates

Repo guidance says Canvas expects full timestamps with timezone for `due_at`. The current frontmatter schema accepts a narrower pattern. Avoid due dates unless a maintainer supplies a repo-approved format.

Recovery:

- Remove the `due` field for training drafts.
- Ask a maintainer to resolve the schema versus Canvas timestamp rule before adding due dates.

## Canvas Has Changed Since Local Draft

Likely cause: Someone edited Canvas directly.

Recovery:

- Use `canvas-inspector` first.
- Ask for a reconcile dry run.
- Do not push local Markdown over live Canvas changes until a human reviews drift.

## Codex Picked The Wrong Skill Or Agent

Recovery:

- Ask Codex to explain the route it chose.
- Point it to `course3/shared/subagent-routing-guide.md`.
- Re-state the task using the routing prompt starter.
- If the task is broad, split it into inspect, draft, validate, review, and publish decisions.

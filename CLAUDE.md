# Claude Guide: Applying AI At Work

Guidance for Claude sessions in this repo, especially chat-app sessions helping
content editors. `AGENTS.md` is the full agent guide; this file is the short
version of the rules that must never be broken. If the two ever disagree,
`AGENTS.md` wins.

## What this repo is

Course content for the "Applying AI at Work" certificate, authored as
Canvas-agnostic Markdown. Markdown is the source of truth. A protected GitHub
Actions workflow publishes merged changes to Canvas; nothing here talks to
Canvas directly during editing.

## Hard rules

1. Edit only Markdown under `course*/sprints/`. That is where course content
   lives. Do not create or rename files unless asked; content edits stay in
   the existing file.
2. Never edit generated Common-Curriculum output (hosted HTML or activity
   JSON, in this repo or the Common-Curriculum repo). It is regenerated from
   Markdown on every publish; hand edits are overwritten.
3. Never write to Canvas and never make Canvas API calls. Publishing happens
   automatically through the protected `Publish Canvas` workflow after a merge
   to `main`. There is nothing for the assistant to publish by hand.
4. Open a pull request for every change. Never push to `main`. The human's
   merge click is the approval step, and the workflow comments the publish
   result on the merged PR.
5. Do not put Canvas IDs in Markdown frontmatter, and do not change an
   artifact's `artifact_id` after creation.
6. Keep artifact bodies Canvas-native Markdown: no HTML, iframes, scripts,
   styles, or external embeds. No em dashes anywhere; use hyphens, colons, or
   sentence breaks.

## Validate before opening a PR

When a Python environment is available, validate the edited file:

```bash
python canvas_sync/schema.py --artifact <edited-file.md>
```

Or validate everything:

```bash
python canvas_sync/schema.py --all
```

If validation cannot be run (for example, a chat-app session without a
runtime), say so in the PR description; the `Validate schemas` check runs on
the PR either way.

## Who edits what

Content editors change wording, instructions, examples, and explanations in
existing pages. Structural changes (new pages, renames, points, due dates,
publish state, reordering, anything touching manifests, schemas, or
`canvas_sync/`) go to the repo maintainer. See `docs/CONTENT_TEAM_GUIDE.md`.

## Read next

- `AGENTS.md`: full agent guidance and build learnings.
- `README.md`: operator guide and workflow reference.
- `docs/CONTENT_TEAM_GUIDE.md`: the non-technical editing walkthrough.

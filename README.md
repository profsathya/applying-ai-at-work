# Applying AI at Work

This repo is two things in one: a canvas course builder, and the design for the "Applying AI at Work" workforce certificate (CTI + De Anza). Course content is authored as canvas-agnostic markdown in `course1/` and `course2/`, then pushed to canvas by a Ralph-loop-driven pipeline that talks to the Canvas REST API. Once a course is live, day-to-day edits happen through three slash commands in a Claude Code session; the loop is only for the initial build or a from-scratch rebuild. The certificate's pedagogical design (audience, frameworks, outcomes) lives in `context/certificate-overview.md`.

## What's in this repo

- `course1/` and `course2/` — the two certificate courses. Each has `design/` (authoritative design docs, hand-authored), `sprints/` (canvas artifacts, generated), and `manifests/` (canvas instance state, generated).
- `context/` — shared design docs that inform both courses: audience, frameworks, design principles, SDT, stakeholder engagement, AI partnership, certificate overview, decision log.
- `canvas_sync/` — the Python sync engine (Canvas API client, push, pull, schema validation).
- `.claude/agents/` — the five subagents (sprint-planner, canvas-author, canvas-pusher, canvas-puller, schema-validator).
- `.claude/commands/` — the three slash commands (`/add-artifact`, `/sync`, `/reconcile`).
- `prompts/ralph-prompt.md` — the system prompt for initial builds.
- `ralph.sh` — the Ralph loop driver.
- `schema/` — JSON schemas for PRDs, manifests, and artifact frontmatter.
- `briefs/` — pointer files the planner reads.
- `n8n/` — the grading workflow (separate service).
- `archive/` — the superseded iframe-embedding pattern, kept for reference.

## Quick start (new machine)

One-time setup after cloning:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r canvas_sync/requirements.txt
    npm install -g @anthropic-ai/claude-code
    claude                             # log in, Ctrl+C once authenticated
    cp .env.example .env               # fill in canvas token + course IDs

Confirm the canvas connection works:

    set -a; source .env; set +a
    DEFAULT_COURSE_ID=$COURSE1_CANVAS_ID python canvas_sync/canvas_client.py

Expected output: `Connected to course <id>. Found N modules.`

## How teammates use this

The Ralph loop is only for the initial build or a from-scratch rebuild. Day-to-day, everyone edits course content through a regular Claude Code session using three slash commands. Here is what that looks like in practice.

### Start a session

    claude

Now you are talking to Claude with access to the repo, the subagents, and the slash commands.

### Add one artifact

    /add-artifact add a 20-point reflection to course 1 sprint 2 called "Stakeholder Midpoint Check" asking participants to summarize one conversation that surprised them

Claude writes the MD file, validates it, pushes to canvas, updates the manifest, commits. 30 seconds end to end.

### Edit an existing artifact

    Open course1/sprints/sprint-1/gap-statement.md. Change the rubric so "validates with a real stakeholder" is 15 points and "applies structured thinking" is 5, then push the change to canvas.

Claude edits the MD file and runs `/sync` on it. The push updates the canvas artifact in place.

### Push after manually editing an MD file

If you hand-edited a markdown file and want it in canvas:

    /sync course1/sprints/sprint-2/stakeholder-interview.md

### Pull canvas edits back into the repo

If someone edited a page directly in canvas (Sathya rearranging a module, an admin fixing a typo) and you want the repo to catch up:

    /reconcile course1

Claude shows the diff first and asks before applying.

### Restructure one sprint

    Sprint 3 currently has five artifacts. Restructure it around three themes: information diet audit, source evaluation, claim formation. Reduce to four artifacts total: one per theme plus a capstone discussion. Write the new MD files, delete the ones that no longer fit (both locally and in canvas), and push everything.

Give Claude Opus for this, not Haiku. Mid-size restructures need judgment.

### Restructure a whole course

Don't do this in chat. Edit `course1/design/structure.md` first (this is the authoritative design spec). Then:

    Re-plan course 1. The design docs in course1/design/ have changed since the original build. Produce a new PRD, show me the diff against the old PRD before touching canvas, and do not push anything until I approve.

Claude invokes the sprint-planner subagent, produces a new PRD, you review, approve, push. Only changed items actually hit canvas (manifest idempotency). 10 minutes, not 90.

### Build Course 2

This is the one case where you run the loop:

    TARGET_COURSE=course2 ./ralph.sh --verbose

Same command used for Course 1 initially.

### The rule of thumb

- **One artifact**: use `/add-artifact` or `/sync` in a chat session.
- **Many artifacts**: edit the design doc first, then ask Claude to re-plan.
- **Whole course from scratch**: run `./ralph.sh`.

### What teammates don't need to understand

- Subagents. Never invoked directly. The orchestrator picks them automatically.
- The Ralph loop internals. Only matters for initial builds.
- The Canvas API. `canvas_sync/push.py` handles it. You talk to Claude.
- Manifests and PRDs. Claude reads and updates them on your behalf.

### What teammates DO need to understand

- `course<N>/design/` is the design spec. Edit it to restructure the course.
- `course<N>/sprints/` and `course<N>/manifests/` are generated output. Edit individual sprint files with `/sync`; don't restructure the directory manually.
- `/add-artifact`, `/sync`, `/reconcile` cover almost all day-to-day work.
- `.env` is local and has secrets. Never commit it.

## Repo layout

```
applying-ai-at-work/
  README.md                      # this file (builder + teammate usage)
  README-BUILDER.md              # deep-dive technical reference
  CLAUDE.md                      # project conventions for Claude Code
  AGENTS.md                      # accumulated build learnings (cross-iteration memory)
  index.html                     # marketing landing page

  .env.example                   # canvas credentials template
  ralph.sh                       # the build loop driver
  migrate.sh                     # one-time migration (idempotent)

  prompts/
    ralph-prompt.md              # system prompt for every loop iteration

  .claude/
    settings.json                # permissions (python + python3 both allowlisted)
    agents/*.md                  # five subagents
    commands/*.md                # three slash commands

  canvas_sync/                   # Python sync layer (hand-authored)
    canvas_client.py             # Canvas REST API client
    push.py                      # MD -> canvas
    pull.py                      # canvas -> MD (for /reconcile)
    schema.py                    # validation
    requirements.txt

  schema/                        # JSON schemas (hand-authored)
    frontmatter.schema.json
    manifest.schema.json
    prd.schema.json

  briefs/                        # pointer files for the planner (hand-authored)
    course1.md
    course2.md

  context/                       # shared design docs (hand-authored)
    certificate-overview.md
    audience.md
    frameworks.md
    design-principles.md
    sdt-design.md
    stakeholder-engagement.md
    ai-partnership.md
    decision-log.md
    open-questions.md
    glossary.md
    build-notes/                 # post-build reports

  course1/                       # same pattern as course2/
    README.md                    # navigation
    design/                      # design docs (hand-authored, authoritative)
      README.md
      structure.md
      outcomes.md
    sprints/                     # canvas artifacts (generated)
    manifests/                   # canvas instance state (generated)
    prd.json                     # build plan (generated by planner)
    course.yaml                  # metadata (generated)
    progress.md                  # build log (generated)

  course2/                       # same structure as course1/

  archive/
    legacy-iframe-template/      # superseded pattern, kept for reference

  n8n/                           # grading workflow (separate service)
    grading-workflow.json
    grading-prompt-template.md
    README.md
```

## Gotchas (from real builds)

- **Push blocked by permission system.** If you see subagents stalling on "requires approval" for `python3 canvas_sync/push.py`, confirm `.claude/settings.json` has both `Bash(python canvas_sync/*.py:*)` AND `Bash(python3 canvas_sync/*.py:*)` in the allow list, and that `ralph.sh` uses `--permission-mode bypassPermissions` (not `acceptEdits`). This was the first-build blocker for course1 and cost ~25 minutes to diagnose.
- **Overloaded API errors.** Transient 529s from the Anthropic API happen under load. The loop now retries with 30s backoff, capped at 3 consecutive retries. If you see 3+ consecutive overloads, stop the loop and come back later. The state is safe; re-running resumes.
- **`.env` not loading.** `canvas_sync/canvas_client.py`'s smoke test doesn't auto-load `.env`; `push.py` and `pull.py` do. For manual canvas connection tests, run `set -a; source .env; set +a` first.
- **Invalid `due_at` formats.** Canvas rejects bare local datetimes like `2026-10-15T23:59`. Use full ISO 8601 with timezone (`2026-10-15T23:59:00Z`) or omit `due` entirely. Two course1 artifacts failed on this during the first build.
- **`course<N>/prd.json` got edited by hand.** Don't hand-edit the PRD. Edit `course<N>/design/*.md` instead and ask Claude to re-plan.

## Deeper technical reference

See `README-BUILDER.md` for the full architectural reference: subagent internals, schema details, Ralph loop mechanics, n8n grading workflow, troubleshooting beyond the common gotchas above.

## Certificate design

See `context/certificate-overview.md` for the pedagogical design of the certificate itself. See `context/frameworks.md`, `context/design-principles.md`, and `context/sdt-design.md` for the underlying theory. See `context/decision-log.md` for why things are the way they are.

# Applying AI at Work

This repo is two things in one: a canvas course builder, and the design for the "Applying AI at Work" workforce certificate (CTI + De Anza). Course content is authored as canvas-agnostic markdown in `course1/` and `course2/`, then pushed to canvas by a Ralph-loop-driven pipeline that talks to the Canvas REST API. Once a course is live, day-to-day edits happen through five slash commands in a Claude Code session (`/add-artifact`, `/build-sprint`, `/sync`, `/update-dues`, `/reconcile`); the loop is only for the initial build or a from-scratch rebuild. The certificate's pedagogical design (audience, frameworks, outcomes) lives in `context/certificate-overview.md`.

New to the repo? Skip to [Your first session (novice walkthrough)](#your-first-session-novice-walkthrough) and the [Slash commands at a glance](#slash-commands-at-a-glance) table. That's the minimum you need to start editing course content today.

## What's in this repo

- `course1/` and `course2/` — the two certificate courses. Each has `design/` (authoritative design docs, hand-authored), `sprints/` (canvas artifacts, generated), and `manifests/` (canvas instance state, generated).
- `context/` — shared design docs that inform both courses: audience, frameworks, design principles, SDT, stakeholder engagement, AI partnership, certificate overview, decision log.
- `canvas_sync/` — the Python sync engine (Canvas API client, push, pull, schema validation).
- `.claude/agents/` — the seven subagents (sprint-planner, sprint-module-builder, canvas-author, canvas-pusher, canvas-puller, schema-validator, due-date-updater).
- `.claude/commands/` — the five slash commands (`/add-artifact`, `/build-sprint`, `/sync`, `/reconcile`, `/update-dues`).
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

The Ralph loop is only for the initial build or a from-scratch rebuild. Day-to-day, everyone edits course content through a regular Claude Code session using five slash commands. If you have never used this repo before, the rest of this section is the only part you need to read.

### Your first session (novice walkthrough)

1. Open a terminal.
2. `cd` into this repo: `cd applying-ai-at-work`.
3. Activate the virtualenv if it isn't already: `source .venv/bin/activate`.
4. Start Claude Code: `claude`.
5. You should see a `>` prompt. You're now talking to an orchestrator that can read the repo, call the subagents, and run the five slash commands.
6. Type a slash: `/`. An autocomplete menu appears listing every available command. Pick one and keep typing the rest of the sentence.
7. Press Enter. Claude narrates each step (write MD, validate, push, commit). Anything risky (pushing to canvas, deleting a file) waits for your `yes` first.
8. To end the session: Ctrl+C or type `/exit`.

If something goes wrong: Ctrl+C to stop the current action. Your MD files and manifest are safe - every step commits, so `git log` shows exactly how far it got. You can restart `claude` and ask Claude to resume.

### Slash commands at a glance

| Command | What it does | Touches canvas? | Asks before pushing? |
|---|---|---|---|
| `/add-artifact` | Add one new assignment/page/discussion/quiz from a plain-English description | yes | no (pushes directly) |
| `/build-sprint` | Build a whole sprint (4-6 artifacts) from a context doc | yes | yes |
| `/sync` | Push a hand-edited MD file to canvas | yes | no |
| `/update-dues` | Change due dates on one or many artifacts | yes | yes |
| `/reconcile` | Pull canvas-side edits back into the MD files | no (pulls) | yes (shows diff first) |

The ones that don't ask are the narrow, safe ones; the ones that ask are the broad, coarse ones. Either way, every step commits to git so you can always `git log` and `git diff` to see what changed.

### Start a session

    claude

Now you are talking to Claude with access to the repo, the subagents, and the slash commands.

### `/add-artifact` — add one assignment, page, discussion, or quiz

Use this when you need exactly one new item somewhere in an already-built course. It takes a plain-English description. You do not need to know what MD looks like, which sprint folder to write to, or how the manifest works.

Copy-paste example (novice):

    /add-artifact add a page to course 1 sprint 0 called "How to ask for help" explaining the three channels we use and when to use each

Slightly richer example:

    /add-artifact add a 20-point reflection to course 1 sprint 2 called "Stakeholder Midpoint Check" asking participants to summarize one conversation that surprised them

What you'll see: Claude writes the MD file, validates it, pushes to canvas, updates the manifest, appends a `BUILT` entry to `course1/progress.md` (with an indented `(added mid-build via /add-artifact, ...)` line below it), and commits. 30 seconds end to end.

If your description is missing something critical (sprint number, point value on a graded item), Claude asks one clarifying question instead of guessing.

### `/sync` — push after hand-editing an MD file

Use this after you or a teammate opened a markdown file in an editor, changed something, and want canvas to reflect the change. Don't use it as a general "apply my changes" command - it's specifically for MD-file changes.

Copy-paste example:

    /sync course1/sprints/sprint-2/stakeholder-interview.md

You can also let Claude find the file for you by describing the edit you want:

    Open course1/sprints/sprint-1/gap-statement.md. Change the rubric so "validates with a real stakeholder" is 15 points and "applies structured thinking" is 5, then push the change to canvas.

Claude edits the MD file and runs `/sync` on it. The push updates the canvas artifact in place.

What you'll see: schema-validator output (should say `PASS`), then a push confirmation with the canvas ID and the action (`updated` for an existing artifact, `created` if it's new).

### `/build-sprint` — build a whole sprint from a context doc

Use this when you need more than one artifact but less than a full course re-plan (e.g., adding a new sprint to an already-built course, or rebuilding one sprint from scratch because the design shifted). The context doc is a markdown file you write first describing what the sprint should contain - a formal design-doc excerpt, an informal brief, or a rebuild note. Save it anywhere (`/tmp/` is fine).

Copy-paste example:

    /build-sprint course2 sprint 1 /tmp/sprint-1-context.md

The sprint-module-builder agent reads your context doc alongside every existing sprint in the target course, infers the scaffolding (artifact count, type mix, rubric pattern, voice), and produces a coherent set of 4-6 MD files: module header, briefing, capability assignments, optional stakeholder touchpoint, peer discussion.

MD only - the slash command then validates, asks you to review, and waits for explicit confirmation before pushing. If course2 has no built sprints yet, the agent reads course1 sprints and flags that cross-course inference in its summary.

After a successful push, the command appends a `## Sprint N added post-build (<timestamp>)` section to `<target>/progress.md` with one `BUILT` line per artifact and a summary line referencing the context doc path. This mirrors how the Ralph loop logs initial builds, so post-build additions show up in the same history surface.

Use this instead of chaining `/add-artifact` six times. Use `/add-artifact` for a single addition and design-doc-then-re-plan for whole-course restructures.

### `/update-dues` — change due dates

Shift one or many deadlines without touching anything else in the artifact. Three input modes:

One file, one date:

    /update-dues course1/sprints/sprint-3/ai-fit-analysis.md 2026-10-22T23:59:00Z

All matching artifacts at once (natural language):

    /update-dues push all sprint 3 assignments to 2026-10-22T23:59:00Z

Bulk changes from a mapping file:

    /update-dues --from /tmp/fall-dues.yaml

Claude resolves the targets, updates only the `due` field in each MD file, runs schema-validator, asks before pushing, then commits. If the natural-language phrase resolves to more than one candidate, the command lists them and stops instead of guessing - that's your signal to narrow the description.

The agent always writes full ISO 8601 with timezone (`YYYY-MM-DDTHH:MM:SSZ`). Canvas 400s on bare local datetimes, so the agent also normalizes any malformed `due` values it encounters on the target files.

### `/reconcile` — pull canvas edits back into the repo

If someone edited a page directly in canvas (Sathya rearranging a module, an admin fixing a typo) and you want the repo to catch up:

    /reconcile course1

Claude shows the diff first (dry run), then asks "Apply these changes? (yes/no/partial)". Pick `partial` if you want to cherry-pick which artifacts to pull. Nothing gets written locally until you say yes.

### Things you can ask Claude without a slash command

The slash commands are the safe lanes for the common work. For larger or more nuanced changes, just describe what you want. Claude picks the right subagents and tools.

Restructure one sprint:

    Sprint 3 currently has five artifacts. Restructure it around three themes: information diet audit, source evaluation, claim formation. Reduce to four artifacts total: one per theme plus a capstone discussion. Write the new MD files, delete the ones that no longer fit (both locally and in canvas), and push everything.

Give Claude Opus for this, not Haiku. Mid-size restructures need judgment.

Restructure a whole course (design-doc first, then replan):

Don't do this in chat as an ad-hoc request. Edit `course1/design/structure.md` first (this is the authoritative design spec). Then:

    Re-plan course 1. The design docs in course1/design/ have changed since the original build. Produce a new PRD, show me the diff against the old PRD before touching canvas, and do not push anything until I approve.

Claude invokes the sprint-planner subagent, produces a new PRD, you review, approve, push. Only changed items actually hit canvas (manifest idempotency). 10 minutes, not 90.

### Build Course 2 (the one time you run the loop)

This is the only case where you leave Claude Code and run a shell script:

    TARGET_COURSE=course2 ./ralph.sh --verbose

Same command used for Course 1 initially. Expect ~90 minutes for a ~35-artifact course. The loop commits after every iteration, so you can Ctrl+C at any point and resume later - it will pick up from the first `pending` PRD item.

### The rule of thumb

- **One artifact**: use `/add-artifact` or `/sync` in a chat session.
- **Due dates only**: use `/update-dues` (single file, mapping file, or natural language).
- **One sprint's worth of artifacts**: use `/build-sprint` with a context doc describing the sprint.
- **Canvas changed out from under you**: use `/reconcile`.
- **Many artifacts across sprints**: edit the design doc first, then ask Claude to re-plan.
- **Whole course from scratch**: run `./ralph.sh`.

### What teammates don't need to understand

- Subagents. Never invoked directly. The orchestrator picks them automatically.
- The Ralph loop internals. Only matters for initial builds.
- The Canvas API. `canvas_sync/push.py` handles it. You talk to Claude.
- Manifests and PRDs. Claude reads and updates them on your behalf.

### What teammates DO need to understand

- `course<N>/design/` is the design spec. Edit it to restructure the course.
- `course<N>/sprints/` and `course<N>/manifests/` are generated output. Edit individual sprint files with `/sync`; don't restructure the directory manually.
- `/add-artifact`, `/build-sprint`, `/sync`, `/update-dues`, `/reconcile` cover almost all day-to-day work.
- `.env` is local and has secrets. Never commit it.

### Common first-session hiccups

- **"Command not found: claude".** The Claude Code CLI isn't installed or isn't on your PATH. Run `npm install -g @anthropic-ai/claude-code`.
- **"ERROR: .env not found" when running `./ralph.sh`.** Copy `.env.example` to `.env` and fill in the canvas credentials.
- **Claude says "course1 has no PRD yet".** The course was never planned. Either run `./ralph.sh` to plan + build, or ask Claude to invoke the sprint-planner directly for a PRD-only run.
- **Canvas push returns 400 on `due_at`.** You (or an MD file) have a bare local datetime. Run `/update-dues` on that file with a full ISO-8601 Zulu timestamp, or delete the `due` line entirely.
- **"requires approval" loops.** You ran `ralph.sh` but it was edited to use `acceptEdits` instead of `bypassPermissions`. Put it back - see the Gotchas section.

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
    agents/*.md                  # seven subagents
    commands/*.md                # five slash commands

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
- **Invalid `due_at` formats.** Canvas rejects bare local datetimes like `2026-10-15T23:59`. Use full ISO 8601 with timezone (`2026-10-15T23:59:00Z`) or omit `due` entirely. Two course1 artifacts failed on this during the first build. `/update-dues` normalizes to the canonical form automatically.
- **`course<N>/prd.json` got edited by hand.** Don't hand-edit the PRD. Edit `course<N>/design/*.md` instead and ask Claude to re-plan.

## Deeper technical reference

See `README-BUILDER.md` for the full architectural reference: subagent internals, schema details, Ralph loop mechanics, n8n grading workflow, troubleshooting beyond the common gotchas above.

## Certificate design

See `context/certificate-overview.md` for the pedagogical design of the certificate itself. See `context/frameworks.md`, `context/design-principles.md`, and `context/sdt-design.md` for the underlying theory. See `context/decision-log.md` for why things are the way they are.

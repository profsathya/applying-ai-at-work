# Course Context Spec: Using the Agentic Course Workflow

## Target
- Course: course3
- Course title: Using the Agentic Course Workflow
- Course code:
- Term or delivery context: Self-paced internal training for the agentic course workflow

## Course Purpose
Teach team members how to understand, configure, use, verify, and extend this repository's agentic workflow through Codex app or Codex in an IDE.

## Audience And Situation
The audience includes technical and non-technical team members. Learners may draft content, review generated artifacts, configure course shells, inspect Canvas, push reviewed work, or maintain the workflow. They should not need a live lecture or prior agentic workflow experience.

## Course Arc
The course progresses from repo orientation, to setup and safe first run, to building and publishing content with Codex and local agents, to verification, maintenance, and extension.

## Sprint / Module Map

### Sprint 0: Orientation to the Repo, Codex, and the Agentic Workflow
- Week: 1
- Purpose: Learners understand the repo map, Codex app and IDE workflow, local drafting, validation, review, and Canvas safety boundaries.
- Required artifacts: module header, repo map page, Codex app and IDE workflow page, safety boundaries page, formative check, repo inspection practice assignment.

### Sprint 1: Setup, Configuration, and Safe First Run
- Weeks: 2
- Purpose: Learners understand local course shells, manifests, credentials, setup commands as a technical appendix, local validation, and safe first-run planning.
- Required artifacts: module header, local course shell page, secrets and environment page, technical setup appendix, formative check, safe first-run plan assignment.

### Sprint 2: Building and Publishing Content with Codex and Agents
- Weeks: 3
- Purpose: Learners scope Codex tasks, ask Codex to route to local skills or subagents, draft local Markdown, review artifacts, and prepare publish decisions without automatic Canvas writes.
- Required artifacts: module header, drafting page, skills and agents page, review and publish page, formative check, staged module build review assignment.

### Sprint 3: Verification, Maintenance, and Extension
- Weeks: 4
- Purpose: Learners inspect Canvas, understand reconcile and removal guardrails, maintain course structure, and propose safe workflow extensions.
- Required artifacts: module header, inspect-before-change page, reconcile and remove page, extension page, formative check, workflow extension proposal assignment.

### Sprint 4: Not used in this four-module course
- Weeks:
- Purpose:
- Required artifacts:

### Sprint 5: Not used in this four-module course
- Week:
- Purpose:
- Required artifacts:

## Assessment Strategy
Each module includes a practical formative quiz and an applied task. Quizzes emphasize safe decisions, not trivia. Applied tasks require prompt drafting, setup auditing, staged content review, and a final workflow extension proposal.

## Required Ideas
- Codex app and IDE are the primary learner interfaces.
- Codex CLI should not be taught as the main workflow.
- Local Markdown drafting is separate from Canvas publishing.
- Repo-local skills and subagents should be selected by task shape, not memorized.
- Canvas inspection, reconcile, push, and removal have distinct safety gates.
- Secrets must remain out of prompts, Markdown, screenshots, and commits.

## Constraints
- Due dates, if any, must be full Canvas-compatible timestamps.
- Use `publish: false` until human review.
- Use Canvas-native Markdown only.
- Do not include real secrets or API tokens.
- Do not add HTML, iframes, JavaScript, inline styles, or external CDN references.
- Do not center learner instructions on Codex CLI usage.

## Tone And Voice
Clear, professional, direct, and accessible to technical and non-technical team members.

## Source Material
Use `AGENTS.md`, `README.md`, `README-BUILDER.md`, `.agents/skills/`, `.codex/agents/`, `canvas_sync/`, `schema/`, `docs/codex-migration/`, and official Codex documentation.

## Open Questions
- Should `course3/**` be added to GitHub validation workflow path filters?
- Should the due-date schema be reconciled with the Canvas timestamp guidance before future due dates are added?
- Should course3 be pushed to a sandbox first or directly staged in Canvas course ID 181 after review?

---
name: sprint-planner
description: Decompose a pre-designed course into a build-ready PRD, course metadata, progress log, and empty manifest.
---

# Sprint Planner Skill

Use this when a target course has no PRD or a human explicitly requests a re-plan.

## Inputs

- Target course: any existing local course directory, for example `course1`, `course2`, `course3`, or a named course key
- Brief file: `briefs/<target>.md`
- Sprint/module count, either stated directly by the human or clearly specified in the brief or design docs

## Read Order

1. `briefs/<target>.md`
2. `<target>/design/structure.md`
3. `<target>/design/outcomes.md`
4. `<target>/design/README.md`
5. Shared context docs in `context/`
6. `schema/prd.schema.json`
7. `schema/manifest.schema.json`
8. `AGENTS.md`

## Outputs

1. `<target>/prd.json`
2. `<target>/course.yaml`
3. `<target>/progress.md`
4. `<target>/manifests/production.json`

## Rules

- Decompose the existing design. Do not invent course structure.
- If the sprint/module count is missing, ask for it before writing.
- Do not write artifact bodies.
- Do not push to Canvas.
- Use non-negative sprint numbers that match the human-provided course structure.
- Keep body briefs participant-facing but do not name internal framework labels.
- Validate the PRD and manifest after writing.

# Briefs

Briefs are short pointer files. They tell the optional Codex `sprint-planner` workflow which course to plan and where to find the authoritative design.

For normal whole-course generation, prefer a course context spec in `context/course-specs/` and the `build-course` skill. Briefs remain useful when a human explicitly wants a PRD-backed planning pass.

## Invoking The Planner

```text
Use the sprint-planner skill to plan course2 from briefs/course2.md.
```

## Editing A Brief

If the design for a course changes, update the design docs in `course1/design/` or `course2/design/`, not the brief. The brief just points.

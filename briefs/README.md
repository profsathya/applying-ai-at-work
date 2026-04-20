# Briefs

Briefs are short pointer files. They tell the sprint-planner subagent which course to plan and where to find the authoritative design.

This repo already has well-developed design docs in `course1/design/`, `course2/design/`, and `context/`. Briefs do not duplicate that content. They point at it.

## Invoking a build

To build Course 1:

```
./ralph.sh
```

(defaults to Course 1 if no target is specified)

To build Course 2 after Course 1 is done:

```
TARGET_COURSE=course2 ./ralph.sh
```

Or invoke the planner directly for a specific course:

```
claude -p "Plan course 2 using briefs/course2.md"
```

## Editing a brief

If the design for a course changes (new sprint theme, updated outcomes, different assessment philosophy), update the design docs in `course1/design/` or `course2/design/`, not the brief. The brief just points.

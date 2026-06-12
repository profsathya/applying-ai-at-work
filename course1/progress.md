# Course 1 Reset Progress

Course: Problem Framing with AI (AIW-101)
Target: course1
Reset at: 2026-06-12

## Reset Log

- 2026-06-12: Local `course1` source reset to an empty shell. Sprint Markdown artifacts were removed. PRD items and manifest artifacts were cleared.
- 2026-06-12: Preserved `course1/course.yaml`, `course1/README.md`, `course1/design/`, `course1/reports/`, manifest instance config, hosted HTML config, and `.gitkeep` files.
- 2026-06-12: Generated Common Curriculum course1 output was cleared from `../common-curriculum/deanza/course1` and `../common-curriculum/activities/deanza/course1`.
- 2026-06-12: Live Canvas course 180 content clear remains token-gated through `canvas_sync/remove.py --course-clear`. Apply only after a fresh dry-run token is confirmed in the current turn.

## Current State

`course1` is ready for new module builds from Markdown source. Generated hosted HTML and activity JSON should be recreated by the publish workflow or an approved local sync with `--hosted-output-dir ../common-curriculum`.

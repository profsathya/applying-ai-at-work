# Reframing Problems with AI Build Progress

Course: Reframing Problems with AI (CIS 501)
Target: course1
Canvas course ID: 180
Term: Fall 2026
Reset at: 2026-06-12

## Reset Log

- 2026-06-12: Local `course1` source reset to an empty shell. Sprint Markdown artifacts were removed. PRD items and manifest artifacts were cleared.
- 2026-06-12: Preserved `course1/course.yaml`, `course1/README.md`, `course1/design/`, `course1/reports/`, manifest instance config, hosted HTML config, and `.gitkeep` files.
- 2026-06-12: Generated Common Curriculum course1 output was cleared from `../common-curriculum/deanza/course1` and `../common-curriculum/activities/deanza/course1`.
- 2026-06-12: Live Canvas course 180 content clear remains token-gated through `canvas_sync/remove.py --course-clear`. Apply only after a fresh dry-run token is confirmed in the current turn.

## Current State

`course1` is the local shell for CIS 501: Reframing Problems with AI. The local draft uses `/Users/jeremyshaw/Downloads/cis501_reframing_problems_with_ai_course_build_spec.md` as its course build source. Generated hosted HTML and activity JSON should be recreated by the publish workflow or an approved local sync with `--hosted-output-dir ../common-curriculum`.

Canvas writes have now been made for this build. See the publish log below.

## Publish Log

- 2026-06-12T23:16:40+00:00: Published 45 CIS 501 artifacts directly to Canvas course 180 using `canvas_sync/push.py` with hosted output rendering. Created Canvas modules 1938, 1939, 1940, 1941, and 1942. Rendered 40 hosted HTML files to `../common-curriculum/deanza/course1/` and pushed them to Common Curriculum `main` at commit `b09e87c`.

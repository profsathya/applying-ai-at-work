# Retired course modules

Retired on 2026-09-11 at the course owner's request:

- Course Builder Smoke Test - 2026-09-08 (Canvas module 2077): three items.
- Working Draft (Canvas module 2078): six items and a local module header.

The original Markdown and source-provenance files are preserved here unchanged, outside the active `course1/sprints/` publishing inventory. Homepage metadata for sprints 10 and 11 was removed. The current Sprint 1 V2 module remains active.

Live removal used `canvas_sync/remove.py` with current external deployment state, after inspection and a scoped dry run. It removed the two modules, their nine module items and underlying content objects, and ten deployment-state records. Other deployment artifact records were verified unchanged.

Local schema validation and regenerated homepage checks passed. Publication and live verification are recorded in the task and Git history.

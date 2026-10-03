# Mac rubric draft recovery, September 30, 2026

Recovered the ten unpublished report/prototype files from stash
`9557e1990cb8eeb9d585b4fff71292bddc91fde9` onto main
`cb1d6b83fe1f18c7e6e5a72d8f9dcaa3cdf483c3`. The original stash and binary patch backup remain
preserved. The backup SHA-256 is `3d22b92ec5c1ee14cd7f04fafaaedd17ad335bd50e4289f617c3a1b523a0eec4`.

## Retained work

The September 29 authoring record, rubric JSON, participant checklist, instructor
ladder, source provenance, historical validation and two generated previews are
retained for review. The README and both preview banners now identify the dated
assignment snapshot. The builder uses the recorded Common Curriculum commit and
checks every source hash before writing. It rejects the changed assignment before
modifying any preview or provenance. Original and recovered hashes for all ten
files are in `recovery-validation.json`.

This package is a proposal with nine criteria totaling 50 points. It has no Canvas
rubric association and no production renderer integration. Existing
`validation.json` and the September 29 authoring report are historical records;
the recovery checks are separate.

## Superseded work

These nine tracked stash changes only raised three assignments and their labels
from 35 to 50 points, with accompanying source-evidence hashes and mechanical
revision records. Current main already contains the intended 50-point values and
newer source revisions. The old introduction evidence file was removed in later
main. Reapplying this portion would conflict with newer content or restore stale
provenance, so none of these changes were restored:

- `course1/homepage.yaml`
- `course1/sprints/sprint-14/first-frames.md`
- `course1/sprints/sprint-14/first-frames.sources.json`
- `course1/sprints/sprint-14/introduction-find-the-problem-worth-solving.md`
- `course1/sprints/sprint-14/introduction-find-the-problem-worth-solving.sources.json`
- `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.md`
- `course1/sprints/sprint-16/stakeholder-map-canvas-walkthrough.sources.json`
- `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.md`
- `course1/sprints/sprint-17/name-the-gap-canvas-walkthrough.sources.json`

The two older unrelated stashes were retained without application or deletion.
Previously pushed branches, including the narrated-video branch, were not merged
again. The separately pushed receiver diagnostic branch is outside this recovery.

## Alignment needed before integration

The assignment hash reviewed on September 29 is
`d56367cfa2cefd1e7b5ab62e49a3fe6d13e917ab2bdab893d1152cf2fd67d871`.
Current source clarifies the Outreach log, assumption blocks in the Stakeholder
Map, named Problem Frame sections, the Part 1 AI exchange, disconfirmation and the
final check. Review criterion mappings and submission wording against that source
before changing the provenance or rebuilding. The local rubric weights and
5/3/1/0 conversion still need an instructor decision before adoption.

## Recovery checks

- Schema validation: PASS.
- Link audit: 190 artifacts, 63 links, zero errors.
- Rubric: nine unique criteria, priorities 1 through 9, complete scoring rungs,
  total 50 points. Eight pinned Common Curriculum evidence hashes verified.
- Builder compiles; stale-source rejection verified with no file writes.
- Isolated Chrome at 1280px and 375px: checkbox keyboard operation, response and
  checkbox reload persistence, clear behavior, score totals 50.0/30.0/41.2,
  illustrative feedback priorities and reset all passed. No page overflow or
  JavaScript errors. External requests were blocked; AI endpoint remains disabled.
- Browser Word download at both widths: valid DOCX, six original tables, the
  synthetic response, two checked and seven unchecked criteria. QA responses were
  cleared in the isolated browser.
- Authoritative course sources, homepage, renderer, schema and agent instructions
  are unchanged. No Canvas, Netlify or hosted publication was performed.

No screen-reader, participant or instructional approval is implied by these
mechanical checks. Current assignment rebuild is intentionally blocked pending
rubric reconciliation.

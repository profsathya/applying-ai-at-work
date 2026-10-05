# Shared orientation and Sprint 1 cleanup review

Revision prepared for authorized publication. Editorial assessment is the agent's. The user explicitly authorized the audited copy cleanup and existing publication workflow; no separate human approval of the resulting wording was observed. Native course46601 order, settings and participant records, live48509, bookings, staffing, dates and policy are outside the write scope.

## Sources and scope

Source main: `0fa335c69e853e31c82576d03c57bdb01b764631`. Existing hosted baseline: Common-Curriculum `486947fc2c686fb3428cf0e4a1f8a1924f7563bc`. Reviewed the seven Markdown files fingerprinted below, homepage YAML, active Sprint 1 Brainstorm/Get underneath/First frames walkthroughs, Sprint 2 introduction, AGENTS, authoring contract/presentation and the unchanged course46601 mirror adapter/config. User-supplied native audit establishes the published activity order. No new native Canvas inspection was performed here.

Approved examples actually inspected: sprint-12 `sprint-1-concept-check-v2.md` (parent) and `start-your-list-and-get-underneath-it-v2.md` (homepage worker). The presentation reference's linked sprint-12 introduction Markdown is absent. Existing layout, illustrations and media remain sufficient for these copy and label changes; no new visuals were required.

## Decisions and alignment

The sequence continues to develop observations into candidate gaps, independent draft frames, Dojo testing with participant judgment, then a chosen Problem Frame supported by reasons. Orienting copy now agrees with the active rules: write independently before optional built-in feedback in Brainstorm/Get underneath; First frames remains without AI. Concept check now follows the Dojo Lab and supports finalizing Problem Frame, matching the published sequence. Its six task IDs, options, keys, criteria and saved-work version are preserved. Sprint 2 roadmap now describes assumptions and existing solutions. Learner labels replace internal storage labels on four active pages without changing artifact identities or positions.

Homepage prerequisite and item descriptions name separate downloads and the First frames Word file, removing the unsupported single Candidate Log requirement. Exactly four YAML values changed; other groups, order, goals, dates, points and metadata remain identical. The two provenance sidecars update only authored `new` parts and hashes, with user-authorized adaptation reasons; original source selections are preserved.

Booking links remain intentionally pending the stated management decision. No other consequential design decision was found in this scope. This review includes no participant testing and makes no claim of learning effectiveness or full auditory review of the previously published Claude video.

## Observed review and validation

- Parent-observed `env -u CANVAS_API_URL -u CANVAS_API_TOKEN -u CANVAS_TOKEN /workspace/leslie-review/venv/bin/python canvas_sync/schema.py --all`: PASS after final homepage maintenance; source fidelity included. Homepage worker separately reports homepage/all-schema and diff checks passing.
- Parent-observed same interpreter/env with `canvas_sync/link_audit.py --all`: 172 artifacts, 61 links, 0 errors. `python -m unittest discover`: 373 tests, 10.965 seconds, OK, one existing skip. `git diff --check`: clean.
- Initial pre-edit render did not complete before edits. A reconstructed immutable baseline from unchanged source main and an archive of exact hosted bytes were used and labeled accordingly. Full-course render of unchanged main reproduces hosted baseline with zero changes. Full-course render after cleanup changes only seven pages, two module overviews and the existing Concept check alias: ten HTML outputs, no media or unrelated outputs.
- Existing `module_preview_browser.cjs` checker passed reading/index hierarchy and layout checks but failed on an obsolete `#copy-answers` selector on Concept check, Dojo Lab and Problem Frame. It also verified old saved responses persisted and correct/incorrect choice feedback before that failure. The harness was not changed. Direct scoped browser checks exercised the actual controls instead.
- `python3 /workspace/course-cleanup-evidence/check_mirror.py`: passed 18 checks across nine distinct changed pages at 1280/390 px, plus 320 px enlarged base text. Used the actual course46601 adapter/config with local reviewed shared bytes, blocked external requests, and checked no JS errors, no page overflow, heading hierarchy, known mirror navigation, removed storage labels, corrected copy, six choice answers/radio keyboard operation, saved-response reload, keyboard downloads and exact transcript-request copy. Downloaded outputs contain the scoped QA responses. External institutional logos were blocked; no Canvas or AI service was contacted by browser QA.
- `python3 /workspace/leslie-review/check_video_page.py --root /workspace/course-cleanup-evidence/after --out /workspace/course-cleanup-evidence/video-review`: desktop/mobile playback and caption cues pass for all three videos; Claude duration 308.9 seconds, 72 cues, original 13,402,322-byte download; 375 px iframe playback passes. All six video/caption assets and setup instructions from Get started onward are byte-identical to baseline.
- Manually inspected rendered desktop pages and mobile screenshots. Corrected route and AI boundary are readable; Concept check leads into the chosen frame; separate downloads and next meaningful actions remain clear; headings and response controls retain their existing hierarchy; mobile cards, choices, downloads and media fit the viewport. Existing Dojo prompt cards and illustration remain unchanged. Resume behavior was observed in fresh browser QA, not participant data.

Evidence is under `/workspace/course-cleanup-evidence/`: `expected-hosted-changes.json`, `protected-scope-checks.json`, `unit-tests.txt`, `schema-final.txt`, `review/browser-results.json`, `mirror-review/results.json`, `video-review/browser-results.json`, screenshots and comparison. Direct public HTTP/playback verification remains unavailable in this executor because the network proxy rejects the public Pages host. Publication must use the existing hosted-only protected workflow; it does not write native Canvas state. Final workflow/deployed-byte evidence will be reported separately after publication.

## Skills consulted

| Skill path | Local revision | SHA-256 |
|---|---|---|
| `.agents/skills/writing-to-teach/SKILL.md` | 5 | `7cd409b3a8bee0d7b5c5316ddbc152940753823cb649989d59174e20cafd2ca5` |
| `.agents/skills/writing-learning-goals/SKILL.md` | 2 | `0a9427039031806b7eea78d5bf6a9fb22c629bf70b9cd20e42169fe817eca9da` |
| `.agents/skills/writing-assignments/SKILL.md` | 4 | `767ad4bbc05b0333c0b95c8ec6632c872b389f403540d0d0794689b48ba0b4c2` |
| `.agents/skills/reviewing-course-text/SKILL.md` | 6 | `1614ebaf7e321064f02c7a9041d5443e3c1c45c800a278a0fd54cd539fb7401c` |
| `.agents/skills/maintain-homepage/SKILL.md` | unversioned; homepage worker | `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7` |

Teaching skills pin upstream `81a051324df61c41af464a0220f8085627729ad9`. The record contract `.agents/skills/reviewing-course-text/references/review-record.md` has SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`. Homepage-worker checks and skill use are attributed above; parent observed the remaining checks.

## Reviewed output fingerprints

| Repository-relative output | SHA-256 |
|---|---|
| `course1/sprints/sprint-6/how-this-course-works-v2.md` | `d39862f576420d0aba69539516d21dc9d8243cfa3916ee0a5da3fad486d0fa68` |
| `course1/sprints/sprint-6/your-first-week-v2.md` | `9eb7946664820a92f39c1bc0cdf3e78bcdd1721b38735f3613891cd2bb2eced6` |
| `course1/sprints/sprint-6/set-up-your-ai-dojo-v2.md` | `55043c2d91e7686445930847c29e82285aa5c0d65409d57bc628780256bb4bb8` |
| `course1/sprints/sprint-14/introduction-find-the-problem-worth-solving.md` | `2b577f47359c4dfe2d01318b0fba51c86aca76d5b5f3551b415edba05a5712c5` |
| `course1/sprints/sprint-14/sprint-1-concept-check.md` | `b9b009577ac46c748bb30b2079df112f45a83673a5847e0f1a0a2cbf95ec898c` |
| `course1/sprints/sprint-14/dojo-lab-test-widen-choose.md` | `4229bcc05ad715a32a1bf33a446fe7dc0c82c6bd00baf202d8e52f2c071283ce` |
| `course1/sprints/sprint-14/problem-frame.md` | `5cedbde0a17c7b646e1e4c9c8f6ab528a276b5ed3cb1207707b472aaddf745bc` |
| `course1/sprints/sprint-6/how-this-course-works-v2.sources.json` | `3d471c558bfb00dace55c6567e772ac0cc015cb221755d9c92dc9df24b49a7ad` |
| `course1/sprints/sprint-6/your-first-week-v2.sources.json` | `2997af24dc7a3c99d81679cedc75c96e007b5e9d6c6cf8b09bfedcf6cc9527a3` |
| `course1/homepage.yaml` | `b41657b39e08698b26fa74115627b9acf3ca0b7c24f0af838ddde11c16830bb9` |

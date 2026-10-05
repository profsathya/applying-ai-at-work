# Shared check-in booking review

Revision of the Sprint 0 check-in page and its Start Here/homepage references. The user explicitly authorized replacing the individual booking placeholders with one shared booking page and publishing this narrow change. Editorial assessment is the agent's; approval of these final words and participant testing were not separately observed.

## Sources and decisions

Reviewed source main `ac656e48eb405c6dc58f64b027981fbfe14ee2df`, PR #264 head `52bd94b8058a5bf5b38e99ee152a1a450ad80142`, the check-in page, Start Here and its provenance, homepage YAML, and the previously reviewed Welcome/How This Course Works orientation context. The delegated native parent verified the supplied Calendar landing page as CIS501 Check-ins/Support, 15-minute Zoom appointments shared by Leslie, Jeremy and Melisa. This executor did not independently inspect that landing page; its web request was inaccessible. No availability or advance-notice policy was established.

The final page keeps Leslie's explanation that any of the three course-team members can help. One descriptive booking link uses the exact supplied long Calendar URL. Instructions ask participants to check the time zone and use the booking confirmation for Zoom details and appointment changes. Fixed October availability, the separate Zoom URL, individual placeholders and unsupported scheduling promises are removed. Brief questions are welcome, and check-ins remain optional with no submission or completion requirement. Start Here changes only the matching route row; homepage maintenance changes only the booking summary. Existing artifact identities, slug, positions, other frontmatter, other route rows, captured source evidence and all earlier course/video additions are preserved. No Calendar appointment/settings or native Canvas write is included.

This is a source revision of an existing orientation support page, with its narrow authorized addition recorded in the Start Here sidecar. It helps participants reach the shared booking page and join the resulting meeting. It adds no learning activity, assessment or prerequisite. No consequential missing decision was found within this scope; booking availability remains the booking page's responsibility.

## Skills consulted

Parent used `.agents/skills/writing-to-teach/SKILL.md` revision 5, `.agents/skills/reviewing-course-text/SKILL.md` revision 6, and `.agents/skills/update-artifact/SKILL.md` (no local revision; SHA-256 `443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80`). Review contract `.agents/skills/reviewing-course-text/references/review-record.md` SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`.

The required homepage worker used `.agents/skills/maintain-homepage/SKILL.md` (no revision; SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`), `.agents/skills/writing-learning-goals/SKILL.md` revision 2, and the same writing-to-teach/reviewing-course-text revisions. It reported homepage and full-schema passes and exactly one YAML summary change.

## Observed validation

- Artifact schema checks for both changed pages and `canvas_sync/schema.py --all`: PASS. `canvas_sync/link_audit.py --manifest course1/manifests/production.json`: 111 artifacts, 44 links, zero errors. `python -m unittest discover`: 373 tests, OK, one skipped. Canvas environment variables were removed for these checks.
- Before/after Sprint 6 module previews rendered eight pages. Their generic browser checker was not run; separate browser checks inspected the complete final render.
- Complete baseline render matches all 162 files checked against hosted main `0469bdb0a198e26211295012bbdc31ec1838739f`. Final render changes exactly seven paths: check-in HTML, Start Here HTML, home/index/modules/Sprint 0 HTML, and one title in progress-map JSON. Comparison verifies unchanged assets and unchanged identifiers, completion/settings and all other generated content. An initial expectation omitted the modules and progress-map title propagation; inspecting those differences established their exact title-only scope.
- Playwright with system Chromium: all six changed shared HTML pages at 1280/375px and all five registered De Anza mirror pages at 1280/390px. Mirror checks include navigation mapped to course46601, heading order, no page errors or overflow, and 320px enlarged text. Home orientation was expanded to inspect the booking label. Desktop/mobile booking screenshots and mobile homepage were visually reviewed.
- Five keyboard booking checks, including a 375px iframe, request the exact supplied Calendar URL by GET with the established `_top` target. External requests were intercepted and aborted; no appointment was created. All 23 page/iframe checks passed. Initial QA assertions mistakenly matched `5-minute` within `15-minute`, assumed an exact title without the course suffix, treated collapsed homepage text as visible, and attempted an unregistered `modules.html` mirror route. Correcting the fixture and checking that page directly resolved those QA failures without source changes.
- Protected-source checks confirm only the allowed page title/frontmatter change, preserved optional completion, unchanged other Start Here rows, and unchanged Welcome/Dojo sources. Live public HTTP and native Canvas were not inspected here. Exact deployed bytes, Pages build and unchanged Canvas state are checked separately during publication; the native parent can perform the final public-page read.

Evidence and screenshots are in `/workspace/booking-retry-evidence/`. Schema validity and browser layout do not establish teaching effectiveness.

## Reviewed output fingerprints

| Repository path | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-6/schedule-a-five-minute-check-in.md` | `27bb610f5f72dbf003ee85f9b080a4acc2da6dc54c973ea043197bcb9f6ccd9f` |
| `course1/sprints/sprint-6/start-here-v2.md` | `0e3a6cb36a8b384a629e5f882120ab4c44261891ab40d9a2941e6463decf433f` |
| `course1/sprints/sprint-6/start-here-v2.sources.json` | `8decb01938f2e10d584832a7f19dcf2157a170ac19d3a641ed1aad456bb567db` |
| `course1/homepage.yaml` | `67d906f264ad92db7d5212e54a3481d3cf50b11d42d383faf72029e12d49f5ef` |

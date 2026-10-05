# Help and Resources AI guidance follow-up

Prepared revision for the user-authorized cleanup and narrow publication. Editorial assessment is the agent's; authorization was supplied, but separate human approval of final wording was not assessed. A native live review confirmed the earlier ten deployed pages and found this missed contradiction in Help and Resources.

## Scope, sources, and decisions

Source main `4b8de5646b43e14459858a4571fb50104e3f033b`; hosted baseline `3a31c227b775d9cf4d46521bb5c7d2059f392f03`. Changed only the Use AI tools blockquote in `course1/sprints/sprint-6/help-and-resources-v2.md` and its one authored `new` provenance part. It now says to write own answers before optional built-in AI feedback in Brainstorm/Get underneath, retains First frames **without AI**, and retains subsequent Dojo use and activity-page guidance. All frontmatter, original selected-source identities, submission instructions, source links, and other prose are unchanged.

The first independent writing develops observations and candidate descriptions before feedback; First frames captures participants' own judgment before the Dojo tests their frames. This follows the active walkthroughs without changing practice, evidence, criteria or policy. Existing prose/callout presentation is sufficient; no new visual was needed. Approved examples inspected earlier in this cleanup remain sprint-12 Concept check (parent) and Start your list/Get underneath (homepage worker); the referenced sprint-12 introduction Markdown is absent.

Reviewed all 16 active orientation/Sprint 1 source files identified by curated homepage membership and the mirror allowlist, including their AI guidance and task dependencies. Source list saved at `/workspace/help-ai-fix-evidence/active-source-files.json`. No further blanket prohibition for the two feedback activities was found in this scope. Specific no-AI directions for First frames, Concept check and personal reflection remain. Retired/non-curated legacy originals and hidden Sprint 12 are unchanged. Homepage worker reviewed current metadata and reported no YAML edit needed; homepage hash remains `b41657b39e08698b26fa74115627b9acf3ca0b7c24f0af838ddde11c16830bb9`. Bookings, staffing, dates, course policy, native order/settings and participant records remain outside scope.

## Observed validation and limitations

- Baseline render saved before editing and compared byte-for-byte with the exact hosted Help page. After rendering the whole course against the same published sequence, only `deanza/course1/activities/help-and-resources-v2.html` changes, SHA-256 `8842330ecc562bcbf4b7dee68c40f85f33b4db401324a9cbf78a82c899e08f1c`. No media, overview or other output changes.
- Parent observed `/workspace/leslie-review/venv/bin/python canvas_sync/schema.py --artifact course1/sprints/sprint-6/help-and-resources-v2.md` and `--all`, with Canvas environment variables removed: PASS. `canvas_sync/link_audit.py --all`: 172 artifacts, 61 links, 0 errors. `git diff --check`: clean. All frontmatter and selected-source identity comparisons pass. Local unit tests were not repeated for this paragraph change; standard PR/publication CI will run the full suite before deployment.
- `python3 /workspace/help-ai-fix-evidence/check_mirror.py`: two scoped checks pass at 1280/390 px, plus 320 px enlarged base text. The actual unchanged mirror adapter/config runs with local reviewed bytes; corrected text, First frames restriction, navigation, heading hierarchy, no JS errors and no overflow are checked. Manually inspected full desktop/mobile rendering: the existing AI callout is readable and follows the setup link, and surrounding reference sections remain intact. Institutional logo requests were blocked; no Canvas or AI service was contacted.
- Parent-provided native live review is attributed above. This executor cannot fetch the public Pages host due to its proxy; exact deployed bytes and Pages success will be verified after authorized publication. No participant testing or new full auditory video review was performed.

## Skills and output fingerprints

Reused actually-read `.agents/skills/writing-to-teach/SKILL.md` revision 5, `writing-learning-goals/SKILL.md` revision 2, `writing-assignments/SKILL.md` revision 4, `reviewing-course-text/SKILL.md` revision 6, and homepage worker's `maintain-homepage/SKILL.md` (unversioned). Their unchanged hashes and upstream pin are recorded in `20261005T170514Z-shared-orientation-sprint1-cleanup.md`. The review-record contract hash is `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`. Update-artifact instructions were inspected for routing; this is a shared-source edit under existing GitOps authorization, without native Canvas preparation or push. That skill's SHA-256 is `443d44074f11ae4b9caf65ab0820967a67314b6351a22758428515436ba13d80`.

| Output | SHA-256 |
|---|---|
| `course1/sprints/sprint-6/help-and-resources-v2.md` | `f824a81ed6b333e9cf07bcd1208235395e2bcdc5f870d8223079999751d06436` |
| `course1/sprints/sprint-6/help-and-resources-v2.sources.json` | `a8b6ccced65bbb396817ef46f27114c206fd7c197d8305a4950d26b1e438086b` |

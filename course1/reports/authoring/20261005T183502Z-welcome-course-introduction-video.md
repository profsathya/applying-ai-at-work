# Welcome course-introduction video review

Revision of `course1/sprints/sprint-6/welcome-v2.md`. User approved adding the updated welcome recording to the shared Welcome page and explicitly approved public repository hosting and shared-site publication. Editorial judgments below are the agent's; this is no claim of participant testing or full auditory listening.

The page adds one supported video fence after the opening paragraph, before the existing illustration. Its title rounds the measured 256.698-second duration to 4:17. All previous prose, illustration, frontmatter, navigation, outcomes, completion and submission settings remain identical. The homepage maintainer found the existing curated copy accurate and made no YAML change.

## Sources and scope

Reviewed current source main `69823aaf0abd74d26147b85b907511cf0ebfc590`, Welcome and its source evidence, How This Course Works, existing Dojo/Sprint 1 video patterns, and the approved Sprint 1 Start your list presentation example. The presentation reference's retired Sprint 12 introduction is unavailable in current source. The updated original video and English VTT came from verified handoff commit `9b7ff4ddba4054abb406f9a29f036c37a2a4f327`; all six transfer parts were checked and reconstructed without merging the handoff branch or re-encoding. Only the reconstructed MP4/VTT are included. Existing captured source parts and packet/map fingerprints remain intact; the new media block is explicitly recorded as a user-authorized addition.

Native parent reported prior media checks for the revised 720p/25 fps recording, original voices and Tacey opening before Leslie. Here, FFprobe measured 256.698 seconds with H.264 video and stereo AAC audio; a complete video/audio decode emitted no errors. Fifteen-second visual samples show Tacey, Leslie, Melisa, Jeremy, then Tacey closing. No private screen information was observed in those samples. This executor did not perform full auditory comparison or external transcription.

The supplied VTT has 70 ordered, non-overlapping cues from 3.040 to 252.310 seconds, within the recording. Browser seeks verify the named introductions and closing captions. Five supplied cues are shorter than one second; timings were preserved rather than making unsupported audio edits. The recording's existing Get Live Help reference is retained. Booking links and support arrangements remain outside this change.

## Skills and alignment

Used `.agents/skills/writing-to-teach/SKILL.md` revision 5 and `.agents/skills/reviewing-course-text/SKILL.md` revision 6 within the narrow media-addition boundary. Review contract `.agents/skills/reviewing-course-text/references/review-record.md` SHA-256 `3db21621b6d48db06a73b9eb063b150c017797b3839e426ce916e53dc91b9b0e`. The homepage worker used `.agents/skills/maintain-homepage/SKILL.md`, SHA-256 `69667d75625fd82ece0872206d867b5e38ac9520a1ad858190114b8f972a65e7`, and reported passing homepage-schema validation. Unchanged homepage SHA-256: `b41657b39e08698b26fa74115627b9acf3ca0b7c24f0af838ddde11c16830bb9`.

The introduction lets a new participant meet the people in the supplied recording and understand the course's problem-framing approach before reading the rest of Welcome. It creates no new assessment, prerequisite or policy. Rendered desktop/mobile review found a clear opening, standard video controls and caption/download access, followed by the original illustration and reading sequence. Each existing section still serves its original purpose; no directions are duplicated or replaced. The page retains its next step and introduces no new saved-work controls.

## Observed validation

- `/workspace/leslie-review/venv/bin/python canvas_sync/schema.py --artifact course1/sprints/sprint-6/welcome-v2.md` and `--all`: PASS, with inherited Canvas variables removed.
- `canvas_sync/link_audit.py --manifest course1/manifests/production.json`: 111 artifacts, 43 links, zero errors. An initial unsupported `--course` invocation was corrected to the documented manifest argument.
- `python -m unittest discover`: 373 tests, OK, one skipped, with inherited Canvas variables removed.
- Saved before/after Sprint 6 module previews. Their generic browser checker was not requested; separate checks below inspected the exact full-render output.
- Complete shared page: 1280px and 375px, working playback, all 70 cues, introductory/closing seeks, full 46,723,676-byte download, default English captions, inline controls, no overflow or page errors. A 375px iframe also played successfully.
- Actual deployed De Anza mirror adapter/config with local reviewed page/media bytes: 1280px and 390px, video/captions, mapped navigation, heading order, no overflow or page errors; 320px enlarged text also fits. The first local fixture did not honor MP4 range responses and timed out seeking; correcting that fixture yielded passing checks. Two external institutional logo requests were blocked during offline QA.
- Full before render matched every current hosted file checked. Full after preflight changes exactly three paths: Welcome HTML and its content-addressed MP4/VTT. No other hosted page, homepage, configuration, setting or asset changes.
- `git -c core.whitespace=-blank-at-eof diff --cached --check`: passed. The supplied valid VTT retains its final blank cue separator, which the default Git whitespace check flags. Other whitespace checks remain enabled. Native Canvas and live public HTTP playback were not inspected on this executor; publication is verified separately through deployed bytes and Pages status, with native parent's direct-HTTP check available.

## Reviewed output fingerprints

| Repository path | SHA-256 |
| --- | --- |
| `course1/sprints/sprint-6/welcome-v2.md` | `ae63ee5f22ca2e464d299654fba1fef2ae32074128427982bcbb62f152d07a82` |
| `course1/sprints/sprint-6/welcome-v2.sources.json` | `c0cc47adfabb2027b28164f137c0f25f8b4ca718ef0fc977919d468846c2ee8b` |
| `course1/sprints/sprint-6/assets/course-intro/cis501-course-introduction-with-tacey-opening.mp4` | `74f19f15789135bb30de198c668b80947fc43159b95c42b6ab3401ee924cc22e` |
| `course1/sprints/sprint-6/assets/course-intro/cis501-course-introduction-with-tacey-opening.vtt` | `1d42fb51d952878f6465b48568b39a944ecf9257a06ef146435c26699809065a` |

Evidence and screenshots: `/workspace/welcome-video-update/evidence/`. No participant testing observed.

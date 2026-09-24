# Live walkthrough checks

Use synthetic answers. Keep source captures, answer fixtures, exports, and detailed provider responses under ignored `.source-intake/<run>/`; put concise findings and hashes in the authoring record.

## AI feedback

1. Validate registry coverage with `canvas_sync/walkthrough_feedback_check.py --artifact <file>`. This also runs through artifact schema validation.
2. Run the course AI service tests. Deploy reviewed criteria to the existing `cti-course-ai` service using its README and the Netlify deployment skill when authorized as part of the requested working conversion. Do not change another service or model speculatively.
3. Create a JSON object mapping each enabled task ID to a synthetic response string. For table tasks, use the same labeled selected-row content the browser sends. Run:

   ```sh
   .venv/bin/python canvas_sync/walkthrough_feedback_check.py --artifact <file> --live --samples <fixture.json> --output <report.json>
   ```

4. Inspect every returned response against the source and server criteria. Check relevance, a concrete revision question, no invented evidence or participant answer, no grade, and no demands for rows that were not sent. Diagnose failures before rerunning; do not silently substitute preview feedback. Stop if credentials, provider access, or required approval cannot be resolved within the authorized task.
5. On the real hosted page or Canvas iframe, fill one representative response, press its AI button, and confirm feedback appears below the correct table while the writing stays intact. Localhost samples do not satisfy this check. Keep the automatic browser preview's live-provider status distinct from this separate evidence.

## Real Google Docs paste

Run this section only when the walk-through exposes a Copy action for its required submission route. A Word-upload walk-through uses the downloaded DOCX and has no competing Copy action.

1. In the rendered walkthrough, enter synthetic values, including a multiline cell, and leave some cells blank. Click the actual Copy work button.
2. Create a disposable blank Google Doc in the browser's signed-in account. Paste normally with the system paste shortcut. Do not use a generated DOCX import, HTML parser, or connector-created table as a substitute.
3. Inspect the result visually. Export that saved Google Doc to DOCX (or read its native table structure through an authorized connector). Compare **all** tables in order, their row/column counts, headings, source cells, blank cells, multiline answers, and entered responses. Page breaks do not create new logical tables. Normalize only nonsemantic surrounding whitespace or NBSP padding, and record that normalization.
4. Retain the scratch document URL, exported file hash, expected dimensions, method, and outcome. If source and browser accounts differ, create the scratch document in the browser account; source editing or new sharing access is unnecessary.
5. Test the selectable table fallback when clipboard access is denied. Keep this distinct from the successful rich clipboard path. After Canvas staging, confirm the iframe's copy controls are available and the hosted page still produces the tested rich table output.

If the user requests actual paste or actual AI verification, an unavailable browser, document account, or provider is an unfinished requirement. Complete independent local work, report the concrete blocker, and do not call that check passed.

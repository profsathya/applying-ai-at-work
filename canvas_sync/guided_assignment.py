"""Render an optional response workspace following Common Curriculum's task/copy pattern.

Canvas still receives ordinary text entry. No automatic grading or backend provisioning.
"""
from __future__ import annotations

import html
import hashlib
import json
import re
from pathlib import Path

ASSETS = Path(__file__).parent / 'assets'
DOJO_TRANSCRIPT_TASK_ID = 'dojo-transcript'
DOJO_TRANSCRIPT_TASK_PROMPT = 'Paste the complete Dojo transcript, including every CONTINUED chunk, in order.'
DOJO_TRANSCRIPT_SOURCE_AUTHORITY = 'User-approved course policy, 2026-09-18'
DOJO_PRIVACY_NOTICE = ('Before you begin, replace names and remove confidential workplace, client, education, patient, '
                       'financial, or personal details. Use role labels and approximate details when the exact detail is '
                       'not needed. Do this before you send anything to the AI. Do not edit the transcript later; it must '
                       'preserve the exact words and order of the conversation.')


def _canvas_only_link(canvas_url: str | None) -> str:
    if not canvas_url:
        return ''
    return (
        f'<a hidden data-canvas-only data-canvas-href="{html.escape(canvas_url, quote=True)}" '
        'data-canvas-target="_top">Open the Canvas assignment</a>'
    )


def load_dojo_transcript_prompt(version: str) -> str:
    """Load an approved transcript request and fail closed on unknown or altered versions."""
    if not isinstance(version, str) or not re.fullmatch(r'v[1-9][0-9]*', version):
        raise ValueError(f'Unknown Dojo transcript prompt version: {version!r}')
    path = ASSETS / f'dojo-transcript-prompt-{version}.json'
    if not path.exists():
        raise ValueError(f'Unknown Dojo transcript prompt version: {version!r}')
    try:
        record = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'Invalid Dojo transcript prompt registry for {version!r}') from exc
    text = record.get('text')
    digest = record.get('sha256')
    if (record.get('version') != version or record.get('source_authority') != DOJO_TRANSCRIPT_SOURCE_AUTHORITY
            or not isinstance(text, str) or not isinstance(digest, str)):
        raise ValueError(f'Invalid Dojo transcript prompt registry for {version!r}')
    actual = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if actual != digest:
        raise ValueError(f'Dojo transcript prompt digest mismatch for {version!r}')
    return text


def render_guided_body(frontmatter: dict, instructions_html: str, *, task_sections: dict[str, str] | None = None, canvas_url: str | None = None) -> str:
    config = frontmatter['guided_assignment']
    if frontmatter.get('dojo_submission', {}).get('mode') == 'transcript':
        return render_dojo_transcript_body(frontmatter, instructions_html, canvas_url)
    if config.get('presentation') == 'interleaved':
        return render_interleaved_brainstorm_body(frontmatter, instructions_html, canvas_url)
    if config.get('presentation') == 'reading':
        return render_reading_body(frontmatter, instructions_html, task_sections or {}, canvas_url)
    if config.get('presentation') == 'compact':
        return render_compact_body(frontmatter, instructions_html, task_sections or {}, canvas_url)
    payload = {'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'],
               'module': frontmatter['module'], **config}
    cards = []
    task_sections = task_sections or {}
    check_label = 'Self-check' if task_sections else 'Guidance and self-check'
    for n, task in enumerate(config['tasks'], 1):
        ident = task['id']; prompt = html.escape(task['prompt'])
        criteria = ''.join('<li>' + html.escape(c) + '</li>' for c in task['criteria'])
        reflection = f'<p><strong>Reflect:</strong> {html.escape(task["reflection"])}</p>' if task.get('reflection') else ''
        if task.get('kind', 'response') == 'choice':
            fields = ''.join(f'<label class="choice"><input type="radio" name="{ident}" value="{i}"> {html.escape(option)}</label>' for i, option in enumerate(task['options']))
            fields += f'<button type="button" data-check="{ident}">Check my answer</button><p data-result="{ident}" role="status"></p>'
        else:
            fields = f'<label for="answer-{ident}">Your response</label><textarea id="answer-{ident}" data-answer="{ident}" maxlength="20000" rows="6"></textarea>'
            if config.get('feedback_endpoint'):
                fields += f'<button type="button" data-feedback="{ident}">Get AI feedback</button><p data-feedback-result="{ident}" role="status"></p>'
        teaching = ''
        if ident in task_sections:
            section = re.sub(r'<table\b', '<div class="teaching-table" tabindex="0" role="region" aria-label="Teaching table"><table', task_sections[ident])
            section = section.replace('</table>', '</table></div>')
            teaching = f'<section class="task-teaching">{section}</section>'
        cards.append(teaching + f'<section class="response-task" data-task="{ident}"><h3>{n}. {prompt}</h3>'
                     f'<details><summary>{check_label}</summary><ul>{criteria}</ul>{reflection}</details>{fields}</section>')
    feedback_note = '<p>Optional AI feedback sends only the response you choose and its task criteria to the course feedback service. Remove confidential details first. Feedback is guidance, not a grade; the self-check works without it.</p>' if config.get('feedback_endpoint') else ''
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    framing = ''.join(f'<h2>{label}</h2><p>{html.escape(config[field])}</p>' for field, label in [('purpose', 'Purpose'), ('builds_on', 'What you are building on')] if config.get(field))
    teaching_panel = instructions_html if task_sections else f'<details class="full-instructions"><summary>Read the full instructions and examples</summary>{instructions_html}</details>'
    mechanics = '<p>Answer the tasks in your own document, or use the optional response boxes here. Copy the final text into the Canvas assignment. Saving or copying here does not submit work to Canvas.</p>'
    standing = f'<p>{html.escape(config.get("standing_instruction", "Keep uncertainty visible in your answers."))}</p>'
    copy_tasks = '<button type="button" id="copy-tasks">Copy the questions</button>'
    save_status = '<p id="save-status" role="status">Responses save in this browser on this device. Keep your own copy before leaving.</p>'
    if task_sections:
        framing = ''.join(f'<p>{html.escape(config[field])}</p>' for field in ('purpose', 'builds_on') if config.get(field))
        opening = framing + standing + teaching_panel + feedback_note
        export_controls = '<h2>Save and submit</h2>' + mechanics + save_status + copy_tasks
    else:
        opening = framing + mechanics + teaching_panel + '<h2>Your tasks</h2>' + copy_tasks + standing + save_status + feedback_note
        export_controls = ''
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}</style>
<div class="guided-workspace" id="guided-workspace">
{opening}
{''.join(cards)}
{export_controls}
<p id="completion-status" role="status"></p>
<button type="button" id="copy-answers">Copy my answers</button>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear only this assignment's saved draft in this browser? Copy any work you want to keep first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<p id="copy-status" role="status"></p>
<label for="copy-output">The text to copy</label><textarea id="copy-output" readonly rows="8"></textarea>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'guided-assignment.js').read_text()}</script>
</div>'''


def render_interleaved_brainstorm_body(frontmatter: dict, instructions_html: str, canvas_url: str | None) -> str:
    """Keep each source example and its participant response in one category card."""
    config = frontmatter['guided_assignment']
    if config.get('feedback_protocol') != 'brainstorm-list-v1' or not config.get('feedback_endpoint'):
        raise ValueError('Interleaved presentation requires the brainstorm-list-v1 feedback protocol and endpoint')
    if len(config.get('tasks', [])) != 1:
        raise ValueError('Interleaved brainstorm presentation requires one final-list task')

    chunks = re.split(r'(?=<h2\b)', instructions_html)
    sections: dict[str, str] = {}
    for chunk in chunks:
        match = re.match(r'<h2\b[^>]*>(.*?)</h2>', chunk, re.S)
        if not match:
            continue
        heading = html.unescape(re.sub(r'<[^>]+>', '', match.group(1))).strip()
        sections[heading] = chunk[match.end():]
    labels = ('1. Set up your categories', '2. Walk your week and write everything down', '3. If your list is short')
    if any(label not in sections for label in labels):
        raise ValueError('Interleaved brainstorm requires the original three source sections')

    setup, walk, short = (sections[label] for label in labels)
    example = re.search(r'<blockquote\b[^>]*>.*?</blockquote>', walk, re.S)
    if not example:
        raise ValueError('Interleaved brainstorm could not locate the source example list')
    examples = {}
    for key, title in (('work', 'Work'), ('home', 'Home'), ('other', 'Other')):
        pattern = rf'<p\b[^>]*>\s*<strong>\s*{title}\s*</strong>\s*</p>\s*(<ul\b[^>]*>.*?</ul>)'
        found = re.search(pattern, example.group(0), re.S)
        if not found:
            raise ValueError(f'Interleaved brainstorm could not locate the {title} source examples')
        examples[key] = found.group(1)
    walk = walk[:example.start()] + walk[example.end():]

    categories = ''.join(
        f'<label>{caption}<input type="text" data-category="{key}" value="{default}" maxlength="80"></label>'
        for key, caption, default in (
            ('work', 'First heading', 'Work'), ('home', 'Second heading', 'Home'),
            ('other', 'Third heading', 'Other'),
        )
    ) + '<label>Custom heading, if useful<input type="text" data-category="additional" placeholder="For example: Caregiving" maxlength="80"></label>'

    cards = []
    for key, title in (('work', 'Work'), ('home', 'Home'), ('other', 'Other')):
        cards.append(f'''<article class="category-card" data-category-card="{key}">
<div class="category-example"><p class="example-kicker"><strong>Here is an example list</strong></p><h3>{title}</h3>{examples[key]}</div>
<div class="category-response"><label for="list-{key}"><span data-heading-display="{key}">{title}</span> list</label>
<p class="field-note">Write one situation per line. Get feedback only after you have written your own observations.</p>
<textarea id="list-{key}" data-entry="{key}" maxlength="16000" rows="5" placeholder="One situation per line"></textarea>
<button type="button" data-ai="{key}" disabled>Get AI feedback on this list</button>
<div class="feedback" data-feedback="{key}" role="status" aria-live="polite"></div></div></article>''')
    cards.append('''<article class="category-card" data-category-card="additional" hidden>
<div class="category-response"><label for="list-additional"><span data-heading-display="additional">Custom heading</span> list</label>
<p class="field-note">Use this box only if you added a fourth heading.</p>
<textarea id="list-additional" data-entry="additional" maxlength="16000" rows="5" placeholder="One situation per line"></textarea>
<button type="button" data-ai="additional" disabled>Get AI feedback on this list</button>
<div class="feedback" data-feedback="additional" role="status" aria-live="polite"></div></div></article>''')

    criteria = ''.join(f'<li>{html.escape(item)}</li>' for item in config['tasks'][0]['criteria'])
    payload = {
        'artifactId': frontmatter['artifact_id'], 'version': config['version'],
        'feedbackEndpoint': config['feedback_endpoint'], 'feedbackProtocol': config['feedback_protocol'],
        'title': frontmatter['title'], 'criteria': config['tasks'][0]['criteria'],
    }
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    link = _canvas_only_link(canvas_url)
    safe_note = ('AI feedback is optional and formative, not a grade. When you request feedback, this page sends the activity section, current category label, and response text, or your assembled list for the final review, to the course feedback service. The activity context and criteria are applied server-side. Remove confidential or identifying details before sending. Your saved draft stays in this browser; it is not sent unless you request feedback.')
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}
{(ASSETS / 'guided-reading.css').read_text()}
{(ASSETS / 'guided-interleaved.css').read_text()}</style>
<div class="guided-workspace guided-reading guided-interleaved" id="guided-workspace">
<aside class="tool-note"><p><strong>This is an AI-guided activity.</strong> Work from your own week first. The AI gives feedback on text you choose to send; it will not add situations, rank them, or choose for you.</p>
<p>Responses save in this browser on this device when storage is available. Keep your own copy before leaving.</p>
<p>{html.escape(safe_note)}</p><p id="save-status" class="save-line" role="status" aria-live="polite">Your draft will save in this browser as you type.</p>
<p id="storage-warning" class="storage-warning" hidden>Browser saving is unavailable. Your writing will stay on this page for this visit, but it may not survive a reload. Copy your list before you leave.</p></aside>
<section><h2>1. Set up your categories</h2>{setup}<div class="response-task category-setup"><h3>Your headings</h3><p>Keep or rename these headings so they fit your week. Add a fourth only if you need it.</p><div class="category-grid">{categories}</div></div></section>
<section><h2>2. Walk your week and write everything down</h2>{walk}{''.join(cards)}</section>
<section><h2>3. If your list is short</h2>{short}
<div class="response-task final-review"><h3>Review your assembled list</h3><p>Use the original activity criteria:</p><ul>{criteria}</ul>
<button type="button" data-ai="final" disabled>Get AI feedback on my full list</button><div class="feedback" data-feedback="final" role="status" aria-live="polite"></div></div></section>
<section class="reading-submit"><h2>Copy your list</h2><p>Copy your assembled list. Paste it into the matching <strong>Brainstorm your list</strong> Canvas text-entry submission to complete the module requirement. This page does not submit anything for you. {link}</p>
<button type="button" id="copy-list" disabled>Copy my brainstorm list</button><p id="copy-status" class="status" role="status" aria-live="polite"></p>
<label for="summary-output">The text that gets copied</label><textarea id="summary-output" class="summary-output" readonly rows="10"></textarea></section>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear only this assignment's saved draft in this browser? Copy any work you want to keep first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'brainstorm-interleaved.js').read_text()}</script>
</div>'''


def render_dojo_transcript_body(frontmatter: dict, instructions_html: str, canvas_url: str | None) -> str:
    """Render one uncapped transcript field as the sole Canvas evidence for a Dojo assignment."""
    config = frontmatter['guided_assignment']
    task = config['tasks'][0]
    version = frontmatter['dojo_submission']['prompt_version']
    transcript_request = load_dojo_transcript_prompt(version)
    payload = {
        'artifactId': frontmatter['artifact_id'],
        'title': frontmatter['title'],
        'module': frontmatter['module'],
        **config,
        'dojoSubmission': frontmatter['dojo_submission'],
        'transcriptRequest': transcript_request,
    }
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    criteria = ''.join(f'<li>{html.escape(item)}</li>' for item in task['criteria'])
    link = _canvas_only_link(canvas_url)
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}
{(ASSETS / 'guided-reading.css').read_text()}</style>
<div class="guided-workspace guided-reading dojo-transcript" id="guided-workspace">
<p class="dojo-privacy">{html.escape(DOJO_PRIVACY_NOTICE)}</p>
{instructions_html}
<section class="dojo-transcript-submit">
<h2>Submit the complete transcript</h2>
<p>The complete transcript is the only evidence you submit for this Dojo Lab.</p>
<ol>
<li>Before requesting the transcript, send one final <code>Me:</code> turn that states the decisions this activity asks you to make, in your own words.</li>
<li>Paste the transcript request below into the same conversation exactly as written.</li>
</ol>
<label for="transcript-request-text">Transcript request</label>
<textarea id="transcript-request-text" readonly rows="18">{html.escape(transcript_request)}</textarea>
<button type="button" id="copy-transcript-request">Copy transcript request</button>
<ol start="3">
<li>If the response ends with <code>CONTINUED</code>, reply <code>continue</code>. Repeat until the conversation is complete.</li>
<li>Paste every chunk into the one Canvas text-entry field in order. Keep any <code>CONTINUED</code> markers. Do not submit a summary, link, separate answer, or edited excerpt.</li>
<li>Check that the transcript begins with the required header and includes every turn from your first message through the transcript request, then submit it in Canvas.</li>
</ol>
<div class="response-task" data-task="{html.escape(task['id'], quote=True)}">
<label for="answer-{html.escape(task['id'], quote=True)}">{html.escape(task['prompt'])}</label>
<textarea id="answer-{html.escape(task['id'], quote=True)}" data-answer="{html.escape(task['id'], quote=True)}" rows="20" aria-describedby="save-status"></textarea>
<details><summary>Self-check</summary><ul>{criteria}</ul></details>
</div>
<p id="save-status" role="status">Drafts save in this browser. Keep your own copy.</p>
<p>{html.escape(config.get('standing_instruction', ''))}</p>
<button type="button" id="copy-answers">Copy transcript</button>
<p>Paste the complete transcript into Canvas to submit. Copying or saving here does not submit your work. {link}</p>
<p id="copy-status" role="status"></p>
<details id="more-options"><summary>More options</summary>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear this saved draft? Keep a copy first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<label for="copy-output">Select and copy manually</label><textarea id="copy-output" readonly rows="10"></textarea>
<p id="completion-status"></p>
</details>
</section>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'guided-assignment.js').read_text()}</script>
</div>'''


def render_compact_body(frontmatter: dict, instructions_html: str, task_sections: dict[str, str], canvas_url: str | None) -> str:
    """One continuous lesson and response, with secondary export tools disclosed."""
    config = frontmatter['guided_assignment']
    tasks = config['tasks']
    if (len(tasks) != 1 or tasks[0].get('kind', 'response') != 'response'
            or tasks[0]['id'] not in task_sections or config.get('feedback_endpoint')):
        raise ValueError('Compact presentation requires one mapped response task without AI feedback')
    task = tasks[0]
    ident = html.escape(task['id'], quote=True)
    criteria = ''.join(f'<li>{html.escape(c)}</li>' for c in task['criteria'])
    reflection = f'<p>{html.escape(task["reflection"])}</p>' if task.get('reflection') else ''
    payload = {'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'], 'module': frontmatter['module'], **config}
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    link = _canvas_only_link(canvas_url)
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}
{(ASSETS / 'guided-compact.css').read_text()}</style>
<div class="guided-workspace guided-compact" id="guided-workspace">
{instructions_html}
<section class="task-teaching">{task_sections[task['id']]}</section>
<div class="response-task" data-task="{ident}">
<label for="answer-{ident}">{html.escape(task['prompt'])}</label>
<textarea id="answer-{ident}" data-answer="{ident}" maxlength="20000" rows="7" aria-describedby="save-status"></textarea>
<p id="save-status" role="status">Drafts save in this browser. Keep your own copy.</p>
<details><summary>Self-check</summary><ul>{criteria}</ul>{reflection}</details>
</div>
<div class="compact-submit">
<p>{html.escape(config.get('standing_instruction', ''))}</p>
<button type="button" id="copy-answers">Copy my answers</button>
<p>Paste into Canvas to submit. Copying or saving here does not submit your work. {link}</p>
<p id="copy-status" role="status"></p>
<details id="more-options"><summary>More options</summary>
<button type="button" id="copy-tasks">Copy the questions</button>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear this saved draft? Keep a copy first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<label for="copy-output">Select and copy manually</label><textarea id="copy-output" readonly rows="6"></textarea>
<p id="completion-status" hidden></p>
</details>
</div>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'guided-assignment.js').read_text()}</script>
</div>'''


def render_reading_body(frontmatter: dict, instructions_html: str, task_sections: dict[str, str], canvas_url: str | None) -> str:
    """A continuous reading sequence for multiple response or choice tasks."""
    config = frontmatter['guided_assignment']
    if config.get('feedback_endpoint'):
        raise ValueError('Reading presentation does not support an AI feedback endpoint')
    cards = []
    for n, task in enumerate(config['tasks'], 1):
        ident = html.escape(task['id'], quote=True)
        prompt = html.escape(task['prompt'])
        teaching = task_sections.get(task['id'], '')
        if teaching:
            cards.append(f'<section class="task-teaching">{teaching}</section>')
        if task.get('kind') == 'choice':
            options = ''.join(f'<label class="choice"><input type="radio" name="{ident}" value="{i}"><span>{html.escape(option)}</span></label>' for i, option in enumerate(task['options']))
            cards.append(f'<section class="response-task choice-task" data-task="{ident}">'
                         f'<h3 id="question-{ident}"><span class="question-number">{n}.</span> {prompt}</h3>'
                         f'<fieldset aria-labelledby="question-{ident}">{options}</fieldset>'
                         f'<button type="button" class="secondary" data-check="{ident}">Check my answer<span class="sr-only">: question {n}</span></button>'
                         f'<p data-result="{ident}" role="status"></p></section>')
        else:
            criteria = ''.join(f'<li>{html.escape(c)}</li>' for c in task['criteria'])
            reflection = f'<p>{html.escape(task["reflection"])}</p>' if task.get('reflection') else ''
            cards.append(f'<div class="response-task" data-task="{ident}">'
                         f'<label for="answer-{ident}">{prompt}</label>'
                         f'<textarea id="answer-{ident}" data-answer="{ident}" maxlength="20000" rows="7" aria-describedby="save-status"></textarea>'
                         f'<details><summary>Self-check</summary><ul>{criteria}</ul>{reflection}</details></div>')
    payload = {'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'], 'module': frontmatter['module'], **config}
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    link = _canvas_only_link(canvas_url)
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}
{(ASSETS / 'guided-reading.css').read_text()}</style>
<div class="guided-workspace guided-reading" id="guided-workspace">
{instructions_html}
{''.join(cards)}
<p id="save-status" role="status">Drafts save in this browser. Keep your own copy.</p>
<div class="reading-submit">
<p>{html.escape(config.get('standing_instruction', ''))}</p>
<button type="button" id="copy-answers">Copy my answers</button>
<p>Paste into Canvas to submit. Copying or saving here does not submit your work. {link}</p>
<p id="copy-status" role="status"></p>
<details id="more-options"><summary>More options</summary>
<button type="button" id="copy-tasks">Copy the questions</button>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear this saved draft? Keep a copy first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<label for="copy-output">Select and copy manually</label><textarea id="copy-output" readonly rows="6"></textarea>
<p id="completion-status"></p>
</details>
</div>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'guided-assignment.js').read_text()}</script>
</div>'''

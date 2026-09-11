"""Render an optional response workspace following Common Curriculum's task/copy pattern.

Canvas still receives ordinary text entry. No automatic grading or backend provisioning.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ASSETS = Path(__file__).parent / 'assets'


def render_guided_body(frontmatter: dict, instructions_html: str, *, task_sections: dict[str, str] | None = None, canvas_url: str | None = None) -> str:
    config = frontmatter['guided_assignment']
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
    link = f'<a href="{html.escape(canvas_url, quote=True)}" target="_blank" rel="noopener">Open the Canvas assignment</a>' if canvas_url else ''
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
    link = f'<a href="{html.escape(canvas_url, quote=True)}" target="_blank" rel="noopener">Open the Canvas assignment</a>' if canvas_url else ''
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

"""Render an optional response workspace following Common Curriculum's task/copy pattern.

Canvas still receives ordinary text entry. No automatic grading or backend provisioning.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ASSETS = Path(__file__).parent / 'assets'


def render_guided_body(frontmatter: dict, instructions_html: str) -> str:
    config = frontmatter['guided_assignment']
    payload = {'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'],
               'module': frontmatter['module'], **config}
    cards = []
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
        cards.append(f'<section class="response-task" data-task="{ident}"><h3>{n}. {prompt}</h3>'
                     f'<details><summary>Guidance and self-check</summary><ul>{criteria}</ul>{reflection}</details>{fields}</section>')
    feedback_note = '<p>Optional AI feedback sends only the response you choose and its task criteria to the course feedback service. Remove confidential details first. Feedback is guidance, not a grade; the self-check works without it.</p>' if config.get('feedback_endpoint') else ''
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    framing = ''.join(f'<h2>{label}</h2><p>{html.escape(config[field])}</p>' for field, label in [('purpose', 'Purpose'), ('builds_on', 'What you are building on')] if config.get(field))
    return f'''<style>{(ASSETS / 'guided-assignment.css').read_text()}</style>
<div class="guided-workspace" id="guided-workspace">
{framing}
<p>Answer the tasks in your own document, or use the optional response boxes here. Copy the final text into the Canvas assignment. Saving or copying here does not submit work to Canvas.</p>
<details class="full-instructions"><summary>Read the full instructions and examples</summary>{instructions_html}</details>
<h2>Your tasks</h2>
<button type="button" id="copy-tasks">Copy the questions</button>
<p>{html.escape(config.get('standing_instruction', 'Keep uncertainty visible in your answers.'))}</p>
<p id="save-status" role="status">Responses save in this browser on this device. Keep your own copy before leaving.</p>
{feedback_note}
{''.join(cards)}
<p id="completion-status" role="status"></p>
<button type="button" id="copy-answers">Copy my answers</button>
<button type="button" id="clear-draft">Clear this browser draft</button>
<div id="clear-confirmation" hidden><p>Clear only this assignment's saved draft in this browser? Copy any work you want to keep first.</p><button type="button" id="confirm-clear">Clear saved responses</button><button type="button" id="cancel-clear">Keep my responses</button></div>
<p id="copy-status" role="status"></p>
<label for="copy-output">The text to copy</label><textarea id="copy-output" readonly rows="8"></textarea>
<script type="application/json" id="guided-config">{serialized}</script>
<script>{(ASSETS / 'guided-assignment.js').read_text()}</script>
</div>'''

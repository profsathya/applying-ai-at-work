"""Render source-driven walk-through tasks without activity-specific HTML."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ASSETS = Path(__file__).parent / 'assets'


def _guidance(field: dict) -> str:
    guidance = field.get('guidance') or {}
    if not guidance:
        return ''
    labels = (('ask', 'Ask yourself'), ('example', 'Example'), ('avoid', 'Watch for'))
    parts = ''.join(f'<p><strong>{label}:</strong> {html.escape(guidance[key])}</p>'
                    for key, label in labels if guidance.get(key))
    return f'<details class="walk-field-guidance"><summary>Example and guidance</summary>{parts}</details>'


def _field(task_id: str, repeat: int | None, field: dict) -> str:
    key = '.'.join(str(part) for part in (task_id, repeat, field['id']) if part is not None)
    control_id = 'walk-' + key.replace('.', '-')
    label = html.escape(field['label'])
    kind = field.get('kind', 'textarea')
    if kind == 'select':
        options = '<option value="">Choose one</option>' + ''.join(
            f'<option value="{html.escape(option, quote=True)}">{html.escape(option)}</option>'
            for option in field['options']
        )
        control = f'<select id="{control_id}" data-walk-answer="{key}">{options}</select>'
    elif kind == 'text':
        control = f'<input id="{control_id}" data-walk-answer="{key}" type="text" maxlength="2000">'
    else:
        control = f'<textarea id="{control_id}" data-walk-answer="{key}" maxlength="16000" rows="4"></textarea>'
    evidence = ''
    if field.get('evidence_status'):
        evidence = (f'<label class="walk-field walk-evidence" for="{control_id}-status"><span>Status for {label}</span>'
                    f'<select id="{control_id}-status" data-walk-answer="{key}.status"><option value="">Choose status</option>'
                    '<option>Confirmed</option><option>Inferred</option></select></label>'
                    f'<label class="walk-field walk-evidence" for="{control_id}-reason"><span>Why this status?</span>'
                    f'<textarea id="{control_id}-reason" data-walk-answer="{key}.reason" maxlength="16000" rows="2"></textarea></label>')
    return f'<label class="walk-field" for="{control_id}"><span>{label}</span>{control}</label>{_guidance(field)}{evidence}'


def _table_row(task_id: str, repeat: int, field: dict, *, with_evidence: bool) -> str:
    key = f"{task_id}.{repeat}.{field['id']}"
    control_id = 'walk-' + key.replace('.', '-')
    label = html.escape(field['label'])
    kind = field.get('kind', 'textarea')
    if kind == 'select':
        options = '<option value="">Choose one</option>' + ''.join(
            f'<option value="{html.escape(option, quote=True)}">{html.escape(option)}</option>'
            for option in field['options'])
        answer = f'<select id="{control_id}" data-walk-answer="{key}">{options}</select>'
    elif kind == 'text':
        answer = f'<input id="{control_id}" data-walk-answer="{key}" type="text" maxlength="2000">'
    else:
        answer = f'<textarea id="{control_id}" data-walk-answer="{key}" maxlength="16000" rows="2"></textarea>'
    status = ''
    if field.get('evidence_status'):
        status = (f'<td data-label="Confirmed or Inferred, and why"><label class="walk-sr-only" for="{control_id}-status">Status for {label}</label>'
                  f'<select id="{control_id}-status" data-walk-answer="{key}.status"><option value="">Choose status</option>'
                  '<option>Confirmed</option><option>Inferred</option></select>'
                  f'<label class="walk-sr-only" for="{control_id}-reason">Why this status for {label}?</label>'
                  f'<textarea id="{control_id}-reason" data-walk-answer="{key}.reason" maxlength="16000" rows="2" '
                  'placeholder="Why this status?"></textarea></td>')
    elif with_evidence:
        status = '<td data-label="Confirmed or Inferred, and why"></td>'
    return (f'<tr><th scope="row">{label}{_guidance(field)}</th><td data-label="Your answer"><label class="walk-sr-only" for="{control_id}">'
            f'Your answer for {label}</label>{answer}</td>{status}</tr>')


def render_walkthrough_body(frontmatter: dict, intro_html: str, task_sections: dict[str, str]) -> str:
    config = frontmatter['guided_assignment']
    cards: list[str] = []
    for number, task in enumerate(config['tasks'], 1):
        ident = task['id']
        teaching = task_sections.get(ident, '')
        teaching = re.sub(r'^\s*<h2(?:\s[^>]*)?>.*?</h2>', '', teaching, count=1, flags=re.IGNORECASE | re.DOTALL)
        criteria = ''.join(f'<li>{html.escape(item)}</li>' for item in task['criteria'])
        has_feedback = bool(config.get('feedback_endpoint')) and task.get('feedback_enabled', True)
        kind = task.get('kind', 'response')
        if kind == 'group':
            labels = task.get('repeat_labels') or [f'Entry {i}' for i in range(1, task['repeat_count'] + 1)]
            entries = []
            for index, name in enumerate(labels, 1):
                if task.get('layout') == 'table':
                    evidence = any(field.get('evidence_status') for field in task['fields'])
                    headings = '<th scope="col">Field</th><th scope="col">Your answer</th>' + ('<th scope="col">Confirmed or Inferred, and why</th>' if evidence else '')
                    rows = ''.join(_table_row(ident, index, field, with_evidence=evidence) for field in task['fields'])
                    fields = f'<div class="walk-table-scroll" role="region" aria-label="{html.escape(name, quote=True)} table" tabindex="0"><table class="walk-response-table"><thead><tr>{headings}</tr></thead><tbody>{rows}</tbody></table></div>'
                else:
                    fields = ''.join(_field(ident, index, field) for field in task['fields'])
                feedback = (f'<button type="button" data-walk-feedback="{ident}.{index}" data-checkpoint="{ident}" disabled>Get AI feedback on this entry</button>'
                            f'<p class="walk-feedback" data-walk-feedback-result="{ident}.{index}" role="status" aria-live="polite"></p>') if has_feedback else ''
                expanded = ' open' if index == 1 else ''
                entries.append(f'''<details class="walk-entry" data-walk-entry="{ident}.{index}"{expanded}>
<summary>{html.escape(name)}</summary>{fields}{feedback}</details>''')
            response = ''.join(entries)
        else:
            key = html.escape(ident, quote=True)
            feedback = (f'<button type="button" data-walk-feedback="{key}" data-checkpoint="{key}" disabled>Get AI feedback</button>'
                        f'<p class="walk-feedback" data-walk-feedback-result="{key}" role="status" aria-live="polite"></p>') if has_feedback else ''
            response = f'''<label class="walk-field" for="walk-{key}"><span>Your response</span>
<textarea id="walk-{key}" data-walk-answer="{key}" maxlength="16000" rows="6"></textarea></label>
{feedback}'''
        cards.append(f'''<section class="walk-step" data-walk-step="{html.escape(ident, quote=True)}">
<p class="walk-step-number">Step {number}</p><h2>{html.escape(task['prompt'])}</h2>
<div class="walk-teaching">{teaching}</div>
<details class="walk-check"><summary>What to check in your work</summary><ul>{criteria}</ul></details>
{response}</section>''')
    submission = frontmatter['submission_type']
    if submission == 'file_upload':
        final_direction = 'Download your Word document, then upload that file through this Canvas assignment. You can also copy your work into a personal Google Doc or the original template. A saved browser draft is not a Canvas submission.'
        download = '<button type="button" id="walk-download">Download Word document</button>'
    else:
        final_direction = 'Copy your work into this Canvas assignment’s text-entry box. You can also keep a copy in a personal Google Doc. A saved browser draft is not a Canvas submission.'
        download = ''
    feedback_intro = ('<p>AI feedback is optional and is not a grade. It reviews only the response you choose to send. Remove confidential or identifying details before asking for feedback.</p>'
                      if config.get('feedback_endpoint') else '')
    payload = {
        'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'],
        'version': config['version'], 'tasks': config['tasks'],
        'feedbackEndpoint': config.get('feedback_endpoint'),
        'exportFilename': config.get('export_filename'), 'submissionType': submission,
        'documentPrefix': config.get('document_prefix', []),
        'documentSuffix': config.get('document_suffix', []),
    }
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    docx_script = (ASSETS / 'walkthrough-docx.js').read_text() if submission == 'file_upload' else ''
    return f'''<style>{(ASSETS / 'guided-walkthrough.css').read_text()}</style>
<div class="guided-workspace guided-walkthrough" id="guided-workspace">
<aside class="walk-intro"><p><strong>Work through this assignment in your own words.</strong> Your responses save in this browser on this device when storage is available. Keep a separate copy before leaving.</p>
{feedback_intro}
<p id="walk-save-status" role="status" aria-live="polite">Your draft will save as you type.</p></aside>
{intro_html}{''.join(cards)}
<section class="walk-finish"><h2>Keep and submit your work</h2><p>{html.escape(final_direction)}</p>
<button type="button" id="walk-copy">Copy all my responses</button><button type="button" id="walk-text-download">Download text copy</button>{download}
<p id="walk-copy-status" role="status" aria-live="polite"></p>
<label for="walk-output">Your assembled responses</label><textarea id="walk-output" readonly rows="12"></textarea>
<button type="button" id="walk-clear">Clear this browser draft</button>
<div id="walk-clear-confirm" hidden><p>Clear this saved draft? Keep a copy first.</p><button type="button" id="walk-clear-yes">Clear draft</button><button type="button" id="walk-clear-no">Keep draft</button></div>
</section><script type="application/json" id="guided-config">{serialized}</script>
<script>{docx_script}</script><script>{(ASSETS / 'guided-walkthrough.js').read_text()}</script></div>'''

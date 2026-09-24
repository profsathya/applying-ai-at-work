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


def _source_table(task: dict, *, has_feedback: bool) -> str:
    ident = task['id']
    columns = task['columns']
    minimum_width = len(columns) * 180
    weights = [column.get('width', 1) for column in columns]
    total = sum(weights)
    colgroup = '<colgroup>' + ''.join(
        f'<col style="width:{weight / total * 100:.4f}%">' for weight in weights) + '</colgroup>'
    headings = ''.join(f'<th scope="col">{html.escape(column["label"])}</th>' for column in columns)
    header = f'<thead><tr>{headings}</tr></thead>' if task.get('header_rows', 1) else ''
    rows = []
    controls = []
    response_number = 0
    for row in task['rows']:
        cells = []
        response_row = any(cell.get('response') for cell in row['cells'])
        if response_row:
            response_number += 1
        row_label = row.get('label') or f'Row {response_number}'
        feedback_key = html.escape(f'{ident}.{row["id"]}', quote=True) if response_row and has_feedback else ''
        feedback_result_id = f'walk-feedback-{ident}-{row["id"]}' if feedback_key else ''
        for column_index, (column, cell) in enumerate(zip(columns, row['cells'])):
            source_text = html.escape(cell['text']).replace('\n', '<br>')
            content = f'<div class="walk-source-cell-text">{source_text}</div>' if source_text else ''
            if column_index == 0:
                content += _guidance(row)
            if cell.get('response'):
                key = f'{ident}.{row["id"]}.{column["id"]}'
                control_id = 'walk-' + key.replace('.', '-')
                accessible = html.escape(f'{row_label}: {column["label"]}')
                placeholder = (f' placeholder="{html.escape(row_label, quote=True)}"'
                               if column_index == 0 else '')
                content += (f'<label class="walk-sr-only" for="{control_id}">{accessible}</label>'
                            f'<textarea id="{control_id}" data-walk-answer="{key}" maxlength="16000"'
                            f' rows="2"{placeholder}></textarea>')
            classes = []
            if cell.get('response'):
                classes.append('walk-source-input-cell')
            if feedback_key and column_index == len(columns) - 1:
                classes.append('walk-feedback-anchor')
                content += (f'<div class="walk-row-feedback-control"><button type="button" '
                            f'data-walk-feedback="{feedback_key}" '
                            f'data-checkpoint="{html.escape(ident, quote=True)}" '
                            f'aria-label="Get AI feedback on {html.escape(row_label, quote=True)}" '
                            f'aria-controls="{feedback_result_id}" disabled>'
                            f'<span>AI feedback</span><small>{html.escape(row_label)}</small></button></div>')
            cell_class = f' class="{" ".join(classes)}"' if classes else ''
            cells.append(f'<td{cell_class}>{content}</td>')
        row_class = 'walk-source-response-row' if response_row else 'walk-source-static-row'
        rows.append(f'<tr class="{row_class}">' + ''.join(cells) + '</tr>')
        if feedback_key:
            controls.append(
                f'<div class="walk-row-feedback-result"><strong>{html.escape(row_label)}</strong>'
                f'<p id="{feedback_result_id}" class="walk-feedback" '
                f'data-walk-feedback-result="{feedback_key}" role="status" '
                'aria-live="polite"></p></div>')
    scroll_class = 'walk-table-scroll walk-table-with-feedback' if controls else 'walk-table-scroll'
    help_text = ('Use this table as a reference.' if task.get('read_only') else
                 'Write in the open cells. Use the AI feedback control beside a row after you write in it.'
                 if controls else 'Write in the open cells. Each row grows as you type.')
    table = (f'<p class="walk-table-help">{help_text}</p>'
             '<p class="walk-table-scroll-hint">Scroll sideways to see all columns.</p>'
             f'<div class="{scroll_class}" role="region" aria-label="{html.escape(task["prompt"], quote=True)} table" '
             f'style="--walk-table-min-width:{minimum_width}px" tabindex="0"><table class="walk-source-table"><caption class="walk-sr-only">'
             f'{html.escape(task["prompt"])}</caption>{colgroup}{header}'
             f'<tbody>{"".join(rows)}</tbody></table></div>')
    feedback = (f'<section class="walk-row-feedback-results" aria-label="AI feedback results">'
                f'{"".join(controls)}</section>' if controls else '')
    return table + feedback


def render_walkthrough_body(frontmatter: dict, intro_html: str, task_sections: dict[str, str]) -> str:
    config = frontmatter['guided_assignment']
    cards: list[str] = []
    for number, task in enumerate(config['tasks'], 1):
        ident = task['id']
        teaching = task_sections.get(ident, '')
        teaching = re.sub(r'^\s*<h2(?:\s[^>]*)?>.*?</h2>', '', teaching, count=1, flags=re.IGNORECASE | re.DOTALL)
        criteria = ''.join(f'<li>{html.escape(item)}</li>' for item in task.get('criteria', []))
        self_check = (f'<details class="walk-check"><summary>What to check in your work</summary>'
                      f'<ul>{criteria}</ul></details>') if criteria else ''
        has_feedback = (bool(config.get('feedback_endpoint')) and task.get('feedback_enabled', True)
                        and not task.get('read_only'))
        kind = task.get('kind', 'response')
        if kind == 'table':
            response = _source_table(task, has_feedback=has_feedback)
        elif kind == 'group':
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
{self_check}
{response}</section>''')
    submission = frontmatter['submission_type']
    pdf_from_document = config.get('submission_format') == 'pdf_from_document'
    has_table = any(task.get('kind') == 'table' for task in config['tasks'])
    has_writable = any(task.get('kind') != 'table' or not task.get('read_only') for task in config['tasks'])
    if not has_writable:
        intro = ('This Canvas walk-through assignment includes a reference table. Read it as you work through '
                 'the activity. There is nothing to enter on this page; you can keep a copy of the table below.')
        finish_heading = 'Keep the reference table'
        final_direction = 'Copy or download this table if useful. This page has no response to submit.'
        copy_label = 'Copy reference table'
        download_label = 'Download Word copy of table'
    elif submission == 'file_upload':
        intro = ('This is a Canvas walk-through assignment. Work through the activity one step at a time, '
                 'writing in the spaces provided. Your draft saves in this browser on this device when storage '
                 'is available. At the bottom, copy your work into your continuing document, export it as PDF, '
                 'and submit that PDF in Canvas.' if pdf_from_document else
                 'This is a Canvas walk-through assignment. Work through the activity one step at a time, '
                 'writing in the spaces provided. Your draft saves in this browser on this device when storage '
                 'is available. At the bottom, download your work and submit the file in Canvas.')
        finish_heading = 'Submit this walk-through in Canvas'
        final_direction = ('Copy your completed work into the same working document used for this sprint. '
                           'Export the completed document as PDF. In Canvas, select Submit Assignment, upload '
                           'that PDF, and submit it. Saving, copying, or downloading here does not submit your work.'
                           if pdf_from_document else
                           'Download your Word document. In Canvas, select Submit Assignment, upload the file, '
                           'and submit it. Saving, copying, or downloading here does not submit your work.')
        copy_label = 'Copy work into your document' if pdf_from_document else 'Copy work for your records'
        download_label = 'Download Word backup' if pdf_from_document else 'Download Word document for Canvas submission'
    else:
        intro = ('This is a Canvas walk-through assignment. Work through the activity one step at a time, '
                 'writing in the spaces provided. Your draft saves in this browser on this device when storage '
                 'is available. At the bottom, copy your work and submit it in Canvas.')
        finish_heading = 'Submit this walk-through in Canvas'
        final_direction = ('Copy your completed work. In Canvas, select Submit Assignment, paste it into the '
                           'text-entry box, and submit it. Tables copy with their rows and columns when your '
                           'browser supports rich copy. Saving or copying here does not submit your work.'
                           if has_table else 'Copy your completed work. In Canvas, select Submit Assignment, '
                           'paste it into the text-entry box, and submit it. Saving or copying here does not '
                           'submit your work.')
        copy_label = 'Copy text for Canvas submission'
        download_label = 'Download Word copy for your records'
    download_class = ' class="walk-secondary"' if submission != 'file_upload' or not has_writable or pdf_from_document else ''
    copy_class = ' class="walk-secondary"' if submission == 'file_upload' and has_writable and not pdf_from_document else ''
    download = (f'<button type="button" id="walk-download"{download_class}>'
                f'{html.escape(download_label)}</button>' if config.get('export_filename') else '')
    copy_button = (f'<button type="button" id="walk-copy"{copy_class}>'
                   f'{html.escape(copy_label)}</button>')
    text_download = '<button type="button" id="walk-text-download" class="walk-secondary">Download text copy</button>'
    actions = (download + copy_button + text_download if submission == 'file_upload' and has_writable and not pdf_from_document
               else copy_button + text_download + download)
    feedback_intro = ('<p>AI feedback is optional and is not a grade. It reviews only the response you choose to send. Remove confidential or identifying details before asking for feedback.</p>'
                      if config.get('feedback_endpoint') and has_writable else '')
    destination = config.get('records_destination')
    records = ('Keep your own copy in your workbook or another document you can return to. '
               'Use the copy or download controls below before leaving this page.')
    if destination:
        records = (f'Keep your own copy in <a href="{html.escape(destination["url"], quote=True)}" '
                   f'target="_blank" rel="noopener">{html.escape(destination["label"])}</a>. '
                   'Use the copy control below to paste your completed tables and responses into that document, '
                   'or download a Word copy before leaving this page.')
    payload = {
        'artifactId': frontmatter['artifact_id'], 'title': frontmatter['title'],
        'version': config['version'], 'tasks': config['tasks'], 'hasWritable': has_writable,
        'feedbackEndpoint': config.get('feedback_endpoint'),
        'feedbackOmissionReason': config.get('feedback_omission_reason'),
        'exportFilename': config.get('export_filename'), 'submissionType': submission,
        'pdfFromDocument': pdf_from_document,
        'documentPrefix': config.get('document_prefix', []),
        'documentSuffix': config.get('document_suffix', []),
    }
    serialized = json.dumps(payload, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    docx_script = (ASSETS / 'walkthrough-docx.js').read_text() if config.get('export_filename') else ''
    table_script = (ASSETS / 'walkthrough-tables.js').read_text() if has_table else ''
    plain_output = ('<details class="walk-plain-output"><summary>Plain text backup</summary>'
                    '<label for="walk-output">Your assembled responses as text</label><textarea id="walk-output" readonly rows="12"></textarea></details>'
                    if has_table else '<label for="walk-output">Your assembled responses</label><textarea id="walk-output" readonly rows="12"></textarea>')
    rich_output = ('<div id="walk-rich-output" class="walk-rich-output" hidden tabindex="0" '
                   'aria-label="Tables and responses for manual copying"></div>' if has_table else '')
    save_message = 'Your draft will save as you type.' if has_writable else 'No browser draft is needed for this reference table.'
    clear_controls = ('<button type="button" id="walk-clear">Clear this browser draft</button>'
                      '<div id="walk-clear-confirm" hidden><p>Clear this saved draft? Keep a copy first.</p>'
                      '<button type="button" id="walk-clear-yes">Clear draft</button>'
                      '<button type="button" id="walk-clear-no">Keep draft</button></div>' if has_writable else '')
    return f'''<style>{(ASSETS / 'guided-walkthrough.css').read_text()}</style>
<div class="guided-workspace guided-walkthrough" id="guided-workspace">
<aside class="walk-intro"><h2>How this walk-through works</h2><p>{html.escape(intro)}</p>
<p>{records}</p>
{feedback_intro}
<p id="walk-save-status" role="status" aria-live="polite">{html.escape(save_message)}</p></aside>
{intro_html}{''.join(cards)}
<section class="walk-finish"><h2>{html.escape(finish_heading)}</h2><p>{html.escape(final_direction)}</p>
{actions}
<p id="walk-copy-status" role="status" aria-live="polite"></p>
{plain_output}{rich_output}
{clear_controls}
</section><script type="application/json" id="guided-config">{serialized}</script>
<script>{table_script}</script><script>{docx_script}</script><script>{(ASSETS / 'guided-walkthrough.js').read_text()}</script></div>'''

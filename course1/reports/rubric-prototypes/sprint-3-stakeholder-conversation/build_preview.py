"""Build a review prototype only from the recorded assignment and source revision."""
from pathlib import Path
import hashlib
import html
import json
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COMMON = ROOT.parent / 'common-curriculum'
sys.path.insert(0, str(ROOT))
from canvas_sync.hosted_html import render_hosted_artifact

data = json.loads((HERE / 'rubric.json').read_text())
items = data['items']
assert sum(item['points'] for item in items) == data['total_points'] == 50
assert len({item['id'] for item in items}) == len(items) == 9
assert sorted(item['priority'] for item in items) == list(range(1, 10))
for item in items:
    assert all(item[str(level)] for level in (5, 3, 1, 0))
    assert item['source_tasks'] and item['quality_tag']

# Check all recorded evidence before writing previews or replacing provenance.
# Recovery must not silently turn a dated review into a claim about current sources.
recorded = json.loads((HERE / 'source-provenance.json').read_text())
source_md = ROOT / data['assignment_source']
if recorded['assignment_source'] != data['assignment_source']:
    raise SystemExit('Assignment identity changed. Review the rubric and provenance before rebuilding.')
if hashlib.sha256(source_md.read_bytes()).hexdigest() != recorded['assignment_sha256']:
    raise SystemExit('Assignment changed since this rubric was reviewed. Reconcile the rubric and review its provenance before rebuilding; preserved previews were not modified.')
commit = recorded['common_curriculum_commit']
sources = [
    'skills/writing-foundation/SKILL.md',
    'skills/writing-assignments/SKILL.md',
    'skills/writing-to-teach/SKILL.md',
    'cst349/my-sprint-2-growth-goal-online-chat.md',
    'cst349/my-sprint-2-growth-goal-online-chat.html',
    'cst499/learning-plan.html',
    'cst499/project-proposal.html',
    'config/rubrics/README.md',
]
evidence = ROOT / '.source-intake/cis501-rubric-20260929'
provenance = {'common_curriculum_commit': commit, 'sources': []}
expected = {entry['path']: entry['sha256'] for entry in recorded['sources']}
payloads = {}
for source in sources:
    payload = subprocess.check_output(['git', '-C', str(COMMON), 'show', f'{commit}:{source}'])
    if hashlib.sha256(payload).hexdigest() != expected.get(source):
        raise SystemExit(f'Recorded source differs: {source}. Review provenance before rebuilding.')
    payloads[source] = payload
for source, payload in payloads.items():
    target = evidence / 'common-source' / source
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(payload)
    provenance['sources'].append({'path': source, 'sha256': hashlib.sha256(payload).hexdigest()})
source_md = ROOT / data['assignment_source']
provenance['assignment_source'] = data['assignment_source']
provenance['assignment_sha256'] = hashlib.sha256(source_md.read_bytes()).hexdigest()
(HERE / 'source-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')

participant = [
    '# How this assignment is assessed', '',
    'CIS 501 · Sprint 3 · Stakeholder Conversation · 50 points · Main Assignments', '',
    'Use the self-check to review your report and updated map before submitting. Each line describes full-credit evidence. Your instructor checks the evidence; checking a box does not award points.', '',
    '## Self-check', '',
]
for item in items:
    participant.append(f"- [ ] {item['5']} **{item['points']} points**")
participant += [
    '', '## What makes it strong', '', data['strong'], '',
    '## Grading and next use', '',
    'Your instructor assesses the submitted evidence and reasoning using these criteria. The work is worth 50 points in Main Assignments, which counts toward your final grade. AI feedback supports your question review; the instructor determines your grade. Optional row feedback earns no points.', '',
    'Use the feedback and the remaining uncertainties in Section D when you identify your learning gaps in Sprint 4. A clear, evidence-supported decision to retain the original frame can earn full credit.', '',
    'Submit the existing three files: the completed report, the updated Stakeholder Map, and the Part 1 AI exchange JSON. In this local prototype, the report download also includes your self-check states. The self-check is part of the report, not a fourth file.', '',
]
(HERE / 'participant-self-check.md').write_text('\n'.join(participant))

instructor = [
    '# CIS 501 instructor rubric: Stakeholder Conversation', '',
    '**Local draft.** Nine items total 50 points. Participant-facing content is in participant-self-check.md; the partial-credit ladder and internal priorities stay in this instructor record.', '',
    '## Proposed scoring', '',
    'Score each item once: 5 = full evidence, 3 = partial evidence, 1 = minimal evidence, 0 = no assessable evidence. Item points = maximum points × rating ÷ 5. Sum before rounding; display one decimal place. The point conversion and zero are proposed CIS 501 adaptations, rather than a scoring formula verified in Sathya\'s courses.', '',
    'Judge the quality of the investigation relative to the starting frame. A confirmed frame, a revised frame, or justified uncertainty can earn full credit. Do not require an AI error, a changed belief, a discovered surprise, or a proposed AI solution. Do not grade prose polish, AI agreement, or use of optional row feedback.', '',
    'Grade the final questions only under item 2; item 3 assesses their investigative purpose and item 4 assesses the required exchange process. Item 8 assesses the conversation-driven map updates, not the original map already graded separately. Item 9 assesses identification and readability, not a second penalty for a missing content file. A missing file leaves its own substantive evidence unassessable; do not repeat that deduction elsewhere for the same omission.', '',
    '## Criterion ladder', '',
]
for index, item in enumerate(items, 1):
    instructor += [
        f"### {index}. {item['title']} ({item['points']} points)", '',
        f"Evidence: {item['evidence']}. Internal feedback priority: {item['priority']} (1 is highest). CIS 501 capability tag: {item['quality_tag']}.", '',
        '| Rating | Award | Observable evidence and feedback |', '| --- | ---: | --- |',
    ]
    for level in (5, 3, 1, 0):
        award = item['points'] * level / 5
        instructor.append(f"| {level} | {award:g} | {item[str(level)]} |")
    instructor.append('')
instructor += [
    '## Feedback', '',
    'After scoring, select one or two highest-priority items with incomplete evidence. Quote or identify the exact place in the participant\'s submission, use the relevant ladder text as the nudge, and ask one focused question. Leave the participant to supply the evidence and decide the revision. Capability tags use the same item scores; do not create a second grade for the tags.', '',
    '**Illustrative feedback, not a participant quotation:** “Section D treats the handover delay as confirmed for the whole team, while Section B records only the account lead\'s experience. Which part of that account establishes the wider claim, and what still needs validation?”', '',
    'No new interview, peer review, word count, late penalty, or submission is added to this assignment. This draft does not define an exception policy for a conversation that has not yet occurred.', '',
]
(HERE / 'instructor-rubric.md').write_text('\n'.join(instructor))

result = render_hosted_artifact(source_md, ROOT / 'course1/manifests/production.json', evidence / 'native-render')
document = Path(result['output_path']).read_text()
preview = HERE / 'preview'
preview.mkdir(exist_ok=True)
base_style = re.search(r'<style>(.*?)</style>', document, re.S).group(1)
extra_style = '''
.review-banner {background:#eaf1f6;border:1px solid #bfd0dd;border-radius:8px;padding:12px 16px;margin:0 0 20px;font-size:14px}
.review-banner p {margin:4px 0}.review-nav {display:flex;gap:8px 18px;flex-wrap:wrap}
.rubric-checks {list-style:none;padding:0}.rubric-checks li {margin:0;padding:12px 0;border-bottom:1px solid #e0e0e0}
.rubric-checks label {display:grid;grid-template-columns:20px 1fr;gap:10px;align-items:start;cursor:pointer}
.rubric-checks input {width:18px;height:18px;margin-top:5px;accent-color:#2c5282}
.rubric-points {display:inline-block;color:#2c5282;font-weight:700;white-space:nowrap;margin-left:4px}
.rubric-lead {color:#555;font-size:14px}details.rubric-selfcheck summary {font-weight:700;cursor:pointer;padding:10px 0}
.rubric-selfcheck summary:focus-visible,a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible {outline:3px solid #1b6aa5;outline-offset:3px}
.score-summary {background:#ebf4ff;border:1px solid #b7cce3;border-radius:8px;padding:14px 18px;margin:16px 0}
.score-summary output {font-size:26px;font-weight:700;display:block}.score-tools {display:flex;gap:10px;flex-wrap:wrap}
button {font:inherit;border:1px solid #b7cce3;background:#ebf4ff;color:#173d67;border-radius:6px;padding:8px 12px;cursor:pointer}
.score-row {display:flex;justify-content:space-between;align-items:start;gap:12px;flex-wrap:wrap}
.score-row h2 {margin:0}.score-row label {font-size:14px}.score-row select {font:inherit;max-width:100%;padding:6px}
.ladder {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:12px}
.rung {background:#f6f8fa;border-radius:6px;padding:12px;font-size:14px}.rung h3 {margin:0 0 6px;font-size:15px}
.evidence {font-size:13px;color:#555;margin-bottom:0}.missing {font-size:13px;color:#555;margin-top:12px}
@media(max-width:620px){.ladder{grid-template-columns:1fr}section{padding:16px}body{padding:12px}.activity{max-width:100%}}
'''
checklist = ''.join(
    f'<li><label><input type="checkbox" id="rubric-{html.escape(i["id"])}" data-rubric-check="{html.escape(i["id"])}"><span>{html.escape(i["5"])} <span class="rubric-points">{i["points"]} pts</span></span></label></li>'
    for i in items
)
rubric_section = f'''<section id="rubric" aria-labelledby="rubric-title">
<p class="meta">CIS 501 · Main Assignments · 50 points</p>
<h2 id="rubric-title">How this assignment is assessed</h2>
<p class="rubric-lead">Use the self-check to review your report and updated map before submitting. Each line describes full-credit evidence. Your instructor checks the evidence; checking a box does not award points.</p>
<details class="rubric-selfcheck" open><summary>Self-check · nine criteria · 50 points</summary><ul class="rubric-checks">{checklist}</ul></details>
<p id="rubric-progress" role="status">0 of 9 items self-checked.</p>
<h3>What makes it strong</h3><p>{html.escape(data['strong'])}</p>
<h3>Grading and next use</h3>
<p>Your instructor assesses the submitted evidence and reasoning using these criteria. The work is worth 50 points in Main Assignments, which counts toward your final grade. AI feedback supports your question review; the instructor determines your grade. Optional row feedback earns no points.</p>
<p>Use the feedback and the remaining uncertainties in Section D when you identify your learning gaps in Sprint 4. A clear, evidence-supported decision to retain the original frame can earn full credit.</p>
</section>'''
banner = '''<aside class="review-banner" aria-label="Local review tools"><p><strong>Local rubric draft for Jeremy</strong> · Assignment snapshot reviewed September 29, 2026, with proposed assessment section. The current assignment has changed; see the design notes before integrating this draft. Canvas has not been changed.</p><nav class="review-nav" aria-label="Review views"><a href="#rubric">Jump to participant self-check</a><a href="instructor.html">Instructor scoring view</a><a href="../README.md">Design notes</a></nav><p>AI feedback is disabled in this local copy. Responses and checks save only in this browser. The report download includes the checked and unchecked items.</p></aside>'''
document = document.replace('</style>', extra_style + '\n</style>', 1)
assert '<div class="activity source-derived">' in document
document = document.replace('<div class="activity source-derived">', '<div class="activity source-derived">' + banner, 1)
document = document.replace('<a class="back-link" href="../sprint-16.html?context=web" data-keep-context>&larr; Back to Module</a>', '<a class="back-link" href="#rubric">View assessment criteria</a>', 1)
assert '<section class="walk-finish">' in document
document = document.replace('<section class="walk-finish">', rubric_section + '<section class="walk-finish">', 1)
# This snapshot has its own draft key and no feedback endpoint. The authoritative
# Markdown and renderer remain unchanged. The new self-check travels in the existing
# Word report via its ordinary documentSuffix, rather than adding a fourth file.
match = re.search(r'(<script type="application/json" id="guided-config">)(.*?)(</script>)', document, re.S)
assert match
config = json.loads(match.group(2))
config['artifactId'] += '-rubric-local-prototype'
config['feedbackEndpoint'] = ''
document = document[:match.start(2)] + json.dumps(config).replace('<', '\\u003c') + document[match.end(2):]
hook = "const config = JSON.parse(document.getElementById('guided-config').textContent);"
assert hook in document
item_json = json.dumps([{'id': i['id'], 'line': i['5'], 'points': i['points']} for i in items]).replace('<', '\\u003c')
injection = '''
  const rubricItems = __ITEMS__;
  const rubricKey = 'cis501-rubric-prototype-selfcheck-v1';
  function refreshRubric() {
    const state = {};
    const suffix = ['Self-check: participant claims, verified by the instructor'];
    for (const item of rubricItems) {
      const checked = document.getElementById('rubric-' + item.id).checked;
      state[item.id] = checked;
      suffix.push((checked ? '[x] ' : '[ ] ') + item.line + ' (' + item.points + ' points)');
    }
    config.documentSuffix = suffix;
    document.getElementById('rubric-progress').textContent = Object.values(state).filter(Boolean).length + ' of 9 items self-checked.';
    try { localStorage.setItem(rubricKey, JSON.stringify(state)); } catch (_) {}
  }
  try {
    const stored = JSON.parse(localStorage.getItem(rubricKey) || '{}');
    for (const item of rubricItems) document.getElementById('rubric-' + item.id).checked = !!stored[item.id];
  } catch (_) {}
  for (const item of rubricItems) document.getElementById('rubric-' + item.id).addEventListener('change', refreshRubric);
  refreshRubric();
'''.replace('__ITEMS__', item_json)
document = document.replace(hook, hook + injection, 1)
clear_hook = '\n      state = {answers: Object.create(null), feedback: Object.create(null)};'
assert clear_hook in document
document = document.replace(clear_hook, clear_hook + "\n      for (const item of rubricItems) document.getElementById('rubric-' + item.id).checked = false;\n      refreshRubric();", 1)
(preview / 'index.html').write_text('\n'.join(line.rstrip() for line in document.splitlines()) + '\n')

cards = []
for index, item in enumerate(items, 1):
    options = '<option value="">Not scored</option>' + ''.join(
        f'<option value="{level}">{level} · {item["points"] * level / 5:g} / {item["points"]} pts</option>' for level in (5, 3, 1, 0)
    )
    ladder = ''.join(
        f'<div class="rung"><h3>{level} · {item["points"] * level / 5:g} pts</h3><p>{html.escape(item[str(level)])}</p></div>' for level in (5, 3, 1)
    )
    cards.append(f'''<section><div class="score-row"><h2>{index}. {html.escape(item['title'])} · {item['points']} pts</h2><label>Rating<select data-score="{item['id']}" aria-label="Rating for {html.escape(item['title'])}">{options}</select></label></div><p class="evidence">Evidence: {html.escape(item['evidence'])}. Feedback priority: {item['priority']}. Capability: {html.escape(item['quality_tag'])}.</p><div class="ladder">{ladder}</div><p class="missing">0 · 0 pts: {html.escape(item['0'])}</p></section>''')
instructor_js = '''
const rubric = __DATA__;
const scores = [...document.querySelectorAll('[data-score]')];
function update() {
  let total = 0, count = 0;
  const incomplete = [];
  for (const select of scores) {
    const item = rubric.items.find(i => i.id === select.dataset.score);
    if (select.value === '') continue;
    count++;
    total += item.points * Number(select.value) / 5;
    if (Number(select.value) < 5) incomplete.push({item, level: select.value});
  }
  document.getElementById('score-total').textContent = total.toFixed(1) + ' / 50';
  document.getElementById('score-count').textContent = count + ' of 9 criteria scored' + (count < 9 ? ' · total is provisional' : '');
  const list = document.getElementById('feedback-priorities'); list.replaceChildren();
  incomplete.sort((a, b) => a.item.priority - b.item.priority).slice(0, 2).forEach(({item, level}) => {
    const entry = document.createElement('li');
    entry.textContent = item.title + ': ' + item[level]; list.appendChild(entry);
  });
  if (!incomplete.length) {const li = document.createElement('li');li.textContent = count < 9 ? 'Score the evidence to identify feedback priorities.' : 'All criteria have full evidence. Identify a specific strength in the reasoning.';list.appendChild(li);}
}
scores.forEach(s => s.addEventListener('change', update));
document.getElementById('example').addEventListener('click', () => {
  const example = [5, 5, 3, 5, 5, 3, 3, 3, 5];
  scores.forEach((s, i) => s.value = String(example[i]));update();
  document.getElementById('example-status').textContent = 'Illustrative scores loaded. These are invented for this demonstration; no participant work was graded.';
});
document.getElementById('reset').addEventListener('click', () => {scores.forEach(s => s.value = '');update();document.getElementById('example-status').textContent = 'Illustrative scores cleared.';});
update();
'''.replace('__DATA__', json.dumps(data).replace('<', '\\u003c'))
instructor_html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CIS 501 · Instructor rubric draft</title><style>{base_style}\n{extra_style}</style></head><body><main class="activity" style="max-width:1080px"><aside class="review-banner"><p><strong>Instructor review prototype</strong> · September 29, 2026 draft. Assignment source has since changed; review alignment before integration. No Canvas connection.</p><nav class="review-nav"><a href="index.html#rubric">Participant self-check</a><a href="../instructor-rubric.md">Rubric in Markdown</a><a href="../README.md">Design notes and sources</a></nav></aside><p class="meta">CIS 501 · Sprint 3 · Main Assignments</p><h1>Stakeholder Conversation · 50-point rubric</h1><p>Score the submitted evidence once per item. The participant sees the full-credit self-check; the partial-credit descriptions and priorities belong to this instructor record.</p><p>Proposed conversion: 5 = full points, 3 = 60%, 1 = 20%, 0 = no assessable evidence. Confirmation, revision, and justified uncertainty can earn full credit.</p><div class="score-tools"><button id="example" type="button">Load illustrative scores</button><button id="reset" type="button">Clear scores</button></div><p id="example-status" role="status">No participant work is loaded.</p><div class="score-summary"><output id="score-total" aria-label="Proposed total">0.0 / 50</output><p id="score-count" role="status"></p></div>{''.join(cards)}<section><h2>Focus the feedback</h2><p>Address one or two highest-priority items with incomplete evidence. Identify the relevant place in the submission, use the matching rung as the nudge, and ask one focused question. The participant supplies the evidence and decides the revision.</p><ul id="feedback-priorities"></ul><p>AI agreement, polished wording, optional feedback use, and a forced change of belief earn no additional points. Item 9 concerns readability and identification; do not repeat a deduction for a missing content file.</p></section><script>{instructor_js}</script></main></body></html>'''
(preview / 'instructor.html').write_text('\n'.join(line.rstrip() for line in instructor_html.splitlines()) + '\n')
print(json.dumps({'total': 50, 'items': 9, 'common_commit': commit, 'preview': str(preview / 'index.html')}, indent=2))

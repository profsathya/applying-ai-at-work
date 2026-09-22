(function () {
  'use strict';
  const config = JSON.parse(document.getElementById('guided-config').textContent);
  const key = 'course-response:' + config.artifactId;
  const output = document.getElementById('walk-output');
  const saveStatus = document.getElementById('walk-save-status');
  const copyStatus = document.getElementById('walk-copy-status');
  const inputs = Array.from(document.querySelectorAll('[data-walk-answer]'));
  const buttons = Array.from(document.querySelectorAll('[data-walk-feedback]'));
  let state = {answers: Object.create(null), feedback: Object.create(null)};
  let saveTimer;

  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && saved.answers && typeof saved.answers === 'object' && !Array.isArray(saved.answers)) {
      state.answers = Object.assign(Object.create(null), saved.answers);
      for (const input of inputs) {
        const value = saved.answers[input.dataset.walkAnswer];
        if (typeof value === 'string') state.answers[input.dataset.walkAnswer] = value.slice(0, 16000);
      }
      if (saved.feedback && typeof saved.feedback === 'object') {
        for (const button of buttons) {
          const value = saved.feedback[button.dataset.walkFeedback];
          if (value && typeof value.text === 'string' && typeof value.onText === 'string') {
            state.feedback[button.dataset.walkFeedback] = value;
          }
        }
      }
      if (Object.values(state.answers).some(value => typeof value === 'string' && value.trim())) {
        saveStatus.textContent = 'Your saved responses from this browser are loaded. Keep your own copy before leaving.';
      }
    }
  } catch (_) {
    saveStatus.textContent = 'This browser could not load a saved draft. Copy your work before leaving.';
  }

  function save() {
    try {
      localStorage.setItem(key, JSON.stringify(state));
      saveStatus.textContent = 'Saved in this browser on this device. Keep your own copy before leaving.';
    } catch (_) {
      saveStatus.textContent = 'Browser saving is unavailable. Copy or download your work before leaving.';
    }
  }

  function responseFor(task, index) {
    if (task.kind !== 'group') return String(state.answers[task.id] || '').trim();
    return task.fields.map(field => {
      const value = String(state.answers[task.id + '.' + index + '.' + field.id] || '').trim();
      const status = field.evidence_status ? String(state.answers[task.id + '.' + index + '.' + field.id + '.status'] || '').trim() : '';
      const reason = field.evidence_status ? String(state.answers[task.id + '.' + index + '.' + field.id + '.reason'] || '').trim() : '';
      return value || status || reason ? field.label + ': ' + (value || '(not entered)') +
        (field.evidence_status ? ' | ' + (status || 'Status not entered') + ': ' + (reason || 'reason not entered') : '') : '';
    }).filter(Boolean).join('\n');
  }

  function assembledText() {
    const lines = [config.title, '', ...(config.documentPrefix || []), ''];
    for (const task of config.tasks) {
      lines.push(task.prompt);
      if (task.kind === 'group') {
        for (let i = 1; i <= task.repeat_count; i++) {
          lines.push('', task.repeat_labels?.[i - 1] || 'Entry ' + i, responseFor(task, i) || '(not entered)');
        }
      } else lines.push(responseFor(task) || '(not entered)');
      lines.push('');
      if (task.document_after) lines.push(...task.document_after, '');
    }
    lines.push(...(config.documentSuffix || []));
    return lines.join('\n').trim() + '\n';
  }

  function responseForButton(button) {
    const task = config.tasks.find(item => item.id === button.dataset.checkpoint);
    if (!task) return '';
    const parts = button.dataset.walkFeedback.split('.');
    return responseFor(task, parts.length > 1 ? Number(parts[1]) : undefined);
  }

  function showFeedback(button, message, stale, preview) {
    const target = document.querySelector('[data-walk-feedback-result="' + button.dataset.walkFeedback + '"]');
    target.textContent = (preview
      ? (stale ? 'Preview sample feedback on an earlier draft: ' : 'Preview sample feedback: ')
      : (stale ? 'AI feedback on an earlier draft: ' : 'AI feedback: ')) + message;
    target.hidden = false;
  }

  function update() {
    for (const button of buttons) {
      const response = responseForButton(button);
      const previous = state.feedback[button.dataset.walkFeedback];
      button.disabled = Boolean(!response || (previous && previous.onText === response && !previous.preview));
      if (previous) showFeedback(button, previous.text, previous.onText !== response, previous.preview);
    }
    if (output.value) output.value = assembledText();
  }

  inputs.forEach(input => {
    input.value = state.answers[input.dataset.walkAnswer] || '';
    input.addEventListener('input', () => {
      state.answers[input.dataset.walkAnswer] = input.value;
      update(); clearTimeout(saveTimer); saveTimer = setTimeout(save, 350);
    });
    input.addEventListener('blur', save);
  });

  buttons.forEach(button => button.addEventListener('click', async () => {
    const response = responseForButton(button);
    if (!response) return;
    const responseKey = response;
    button.disabled = true;
    const result = document.querySelector('[data-walk-feedback-result="' + button.dataset.walkFeedback + '"]');
    result.hidden = false;
    result.textContent = 'Reviewing what you wrote...';
    if (['localhost', '127.0.0.1'].includes(location.hostname)) {
      state.feedback[button.dataset.walkFeedback] = {
        onText: responseKey, preview: true,
        text: 'The live service will review this response against this step. What could you make more specific or verify before submitting?'
      };
      save(); update(); return;
    }
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 45000);
    try {
      const reply = await fetch(config.feedbackEndpoint, {
        method: 'POST', signal: controller.signal, headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({activity: config.artifactId, checkpoint: button.dataset.checkpoint, response}),
      });
      const data = await reply.json();
      if (!reply.ok || typeof data.content !== 'string' || !data.content.trim()) throw new Error('Unavailable');
      state.feedback[button.dataset.walkFeedback] = {onText: responseKey, text: data.content.trim()};
      save(); update();
    } catch (_) {
      result.textContent = 'AI feedback is unavailable. Your writing is still here; use the self-check above and try again later.';
      button.disabled = false;
    } finally { clearTimeout(timeout); }
  }));

  document.getElementById('walk-copy').addEventListener('click', async () => {
    output.value = assembledText();
    try {
      await navigator.clipboard.writeText(output.value);
      copyStatus.textContent = 'Copied. Paste into your own Google Doc, the original template, or the Canvas submission area. Copying has not submitted your work.';
    } catch (_) {
      output.focus(); output.select();
      copyStatus.textContent = 'Select and copy the text shown here. Copying has not submitted your work.';
    }
  });
  document.getElementById('walk-text-download').addEventListener('click', () => {
    const blob = new Blob([assembledText()], {type: 'text/plain;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = config.artifactId + '-responses.txt'; link.hidden = true;
    document.body.appendChild(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 60000);
    copyStatus.textContent = 'Text copy downloaded. Keep it for your records; downloading is not a Canvas submission.';
  });
  const download = document.getElementById('walk-download');
  if (download) download.addEventListener('click', () => {
    try {
      const blob = globalThis.WalkthroughDocx.build(config, state.answers);
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url; link.download = config.exportFilename; link.hidden = true;
      document.body.appendChild(link); link.click(); link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 60000);
      copyStatus.textContent = 'Word document downloaded. Upload it through this Canvas assignment; downloading is not a submission.';
    } catch (_) {
      output.value = assembledText(); output.focus(); output.select();
      copyStatus.textContent = 'Download is unavailable. Copy this text into a document, then upload that document to Canvas.';
    }
  });
  document.getElementById('walk-clear').addEventListener('click', () => { document.getElementById('walk-clear-confirm').hidden = false; });
  document.getElementById('walk-clear-no').addEventListener('click', () => { document.getElementById('walk-clear-confirm').hidden = true; });
  document.getElementById('walk-clear-yes').addEventListener('click', () => {
    clearTimeout(saveTimer);
    try { localStorage.removeItem(key); }
    catch (_) { saveStatus.textContent = 'Could not clear the saved draft. Keep a copy of your responses.'; return; }
    state = {answers: Object.create(null), feedback: Object.create(null)};
    inputs.forEach(input => { input.value = ''; });
    buttons.forEach(button => {
      document.querySelector('[data-walk-feedback-result="' + button.dataset.walkFeedback + '"]').textContent = '';
    });
    output.value = ''; copyStatus.textContent = '';
    document.getElementById('walk-clear-confirm').hidden = true;
    saveStatus.textContent = 'This browser draft was cleared.';
    update();
  });
  update();
}());

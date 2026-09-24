(function () {
  'use strict';
  const config = JSON.parse(document.getElementById('guided-config').textContent);
  const key = 'course-response:' + config.artifactId;
  const output = document.getElementById('walk-output');
  const saveStatus = document.getElementById('walk-save-status');
  const copyStatus = document.getElementById('walk-copy-status');
  const richOutput = document.getElementById('walk-rich-output');
  const hasTable = config.tasks.some(task => task.kind === 'table');
  const pdfFromDocument = Boolean(config.pdfFromDocument);
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
      if (config.hasWritable && Object.values(state.answers).some(value => typeof value === 'string' && value.trim())) {
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
    if (task.kind === 'table') {
      const row = task.rows.find(item => item.id === index);
      return row ? globalThis.WalkthroughTables.rowResponse(task, row, state.answers) : '';
    }
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
      if (task.kind === 'table') {
        lines.push(globalThis.WalkthroughTables.tsv(task, state.answers));
      } else if (task.kind === 'group') {
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
    const suffix = button.dataset.walkFeedback.slice(task.id.length + 1);
    return responseFor(task, task.kind === 'table' ? suffix : suffix ? Number(suffix) : undefined);
  }

  function assembledHtml() {
    const escape = value => String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    const parts = ['<div>', '<h1>' + escape(config.title) + '</h1>'];
    for (const line of config.documentPrefix || []) parts.push('<p>' + escape(line) + '</p>');
    for (const task of config.tasks) {
      parts.push('<h2>' + escape(task.prompt) + '</h2>');
      if (task.kind === 'table') parts.push(globalThis.WalkthroughTables.html(task, state.answers));
      else if (task.kind === 'group') {
        for (let i = 1; i <= task.repeat_count; i++) {
          parts.push('<h3>' + escape(task.repeat_labels?.[i - 1] || 'Entry ' + i) + '</h3>');
          parts.push('<p>' + escape(responseFor(task, i)).replace(/\n/g, '<br>') + '</p>');
        }
      } else parts.push('<p>' + escape(responseFor(task)).replace(/\n/g, '<br>') + '</p>');
      for (const line of task.document_after || []) parts.push('<p>' + escape(line) + '</p>');
    }
    for (const line of config.documentSuffix || []) parts.push('<p>' + escape(line) + '</p>');
    parts.push('</div>');
    return parts.join('');
  }

  async function copyTables() {
    const html = assembledHtml(), plain = assembledText();
    let asyncWrite;
    try {
      asyncWrite = navigator.clipboard.write([new ClipboardItem({
        'text/html': new Blob([html], {type: 'text/html'}),
        'text/plain': new Blob([plain], {type: 'text/plain'}),
      })]);
    } catch (_) { /* Canvas may not expose the async Clipboard API. */ }
    richOutput.innerHTML = html;
    richOutput.hidden = false;
    richOutput.classList.add('walk-copy-staging');
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(richOutput);
    selection.removeAllRanges(); selection.addRange(range);
    let copied = false;
    const handleCopy = event => {
      if (!event.clipboardData) return;
      event.clipboardData.setData('text/html', html);
      event.clipboardData.setData('text/plain', plain);
      event.preventDefault();
      copied = true;
    };
    document.addEventListener('copy', handleCopy);
    try { copied = document.execCommand('copy') && copied; }
    catch (_) { copied = false; }
    document.removeEventListener('copy', handleCopy);
    if (asyncWrite) {
      try { await asyncWrite; copied = true; }
      catch (_) { /* Keep the synchronous copy result or show the fallback. */ }
    }
    richOutput.classList.remove('walk-copy-staging');
    if (copied) {
      selection.removeAllRanges();
      richOutput.hidden = true;
      copyStatus.textContent = !config.hasWritable
        ? 'Copied the reference table. Paste it into a document if useful; copying has not submitted anything to Canvas.'
        : pdfFromDocument
        ? 'Copied as a table. Paste it into your continuing document, export the completed document as PDF, then submit that PDF in Canvas.'
        : config.submissionType === 'file_upload'
        ? 'Copied as a table for your records. Download the Word document and upload it through Submit Assignment in Canvas.'
        : 'Copied as a table. In Canvas, select Submit Assignment, paste into the text-entry box, and submit. Copying here has not submitted your work.';
    } else {
      richOutput.focus();
      range.selectNodeContents(richOutput);
      selection.removeAllRanges(); selection.addRange(range);
      copyStatus.textContent = pdfFromDocument
        ? 'Clipboard access is unavailable. Select and copy the table below into your continuing document, then export it as PDF for Canvas.'
        : config.submissionType === 'file_upload' && config.hasWritable
        ? 'Clipboard access is unavailable. Download the Word document and upload it through Submit Assignment in Canvas.'
        : 'Clipboard access is unavailable. Copy the selected table below, or download the Word document. Copying has not submitted your work.';
    }
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

  function resizeTableInput(input) {
    if (!input.closest('.walk-source-table')) return;
    input.style.height = 'auto';
    input.style.height = Math.max(62, Math.min(input.scrollHeight, 320)) + 'px';
    input.style.overflowY = input.scrollHeight > 320 ? 'auto' : 'hidden';
  }

  inputs.forEach(input => {
    input.value = state.answers[input.dataset.walkAnswer] || '';
    resizeTableInput(input);
    input.addEventListener('input', () => {
      state.answers[input.dataset.walkAnswer] = input.value;
      resizeTableInput(input);
      update(); clearTimeout(saveTimer); saveTimer = setTimeout(save, 350);
    });
    input.addEventListener('blur', save);
  });

  buttons.forEach(button => button.addEventListener('click', async () => {
    const response = responseForButton(button);
    if (!response) return;
    if (response.length > 16000) {
      const target = document.querySelector('[data-walk-feedback-result="' + button.dataset.walkFeedback + '"]');
      target.hidden = false;
      target.textContent = 'This row is too long for feedback. Shorten it before asking, or continue using your own review.';
      return;
    }
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
    if (hasTable) { await copyTables(); return; }
    try {
      await navigator.clipboard.writeText(output.value);
      copyStatus.textContent = pdfFromDocument
        ? 'Copied. Paste it into your continuing document, export the completed document as PDF, then submit that PDF in Canvas.'
        : config.submissionType === 'file_upload'
        ? 'Copied. This copy is for your records. Download the Word document and upload it through Submit Assignment in Canvas.'
        : 'Copied. In Canvas, select Submit Assignment, paste into the text-entry box, and submit. Copying here has not submitted your work.';
    } catch (_) {
      output.focus(); output.select();
      copyStatus.textContent = pdfFromDocument
        ? 'Select and copy this text into your continuing document, then export it as PDF for Canvas.'
        : config.submissionType === 'file_upload'
        ? 'Select and copy the text shown here for your records. Download the Word document to submit in Canvas.'
        : 'Select and copy the text shown here. Then paste it into the Canvas text-entry box and submit. Copying here has not submitted your work.';
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
      copyStatus.textContent = !config.hasWritable
        ? 'Reference Word document downloaded for your records. Downloading has not submitted anything to Canvas.'
        : pdfFromDocument
        ? 'Word backup downloaded. Keep working in your continuing document and export that completed document as PDF for Canvas.'
        : config.submissionType === 'file_upload'
        ? 'Word document downloaded. Upload it through this Canvas assignment; downloading is not a submission.'
        : 'Word document downloaded for your records. Submit your response through this Canvas assignment; downloading is not a submission.';
    } catch (_) {
      if (hasTable) {
        richOutput.innerHTML = assembledHtml(); richOutput.hidden = false; richOutput.focus();
        copyStatus.textContent = 'Download is unavailable. Select and copy the table below into a document.';
      } else {
        output.value = assembledText(); output.focus(); output.select();
        copyStatus.textContent = pdfFromDocument
          ? 'Download is unavailable. Copy this text into your continuing document, then export it as PDF for Canvas.'
          : 'Download is unavailable. Copy this text into a document, then upload that document to Canvas.';
      }
    }
  });
  const clearButton = document.getElementById('walk-clear');
  if (clearButton) {
    clearButton.addEventListener('click', () => { document.getElementById('walk-clear-confirm').hidden = false; });
    document.getElementById('walk-clear-no').addEventListener('click', () => { document.getElementById('walk-clear-confirm').hidden = true; });
    document.getElementById('walk-clear-yes').addEventListener('click', () => {
      clearTimeout(saveTimer);
      try { localStorage.removeItem(key); }
      catch (_) { saveStatus.textContent = 'Could not clear the saved draft. Keep a copy of your responses.'; return; }
      state = {answers: Object.create(null), feedback: Object.create(null)};
      inputs.forEach(input => { input.value = ''; resizeTableInput(input); });
      buttons.forEach(button => {
        document.querySelector('[data-walk-feedback-result="' + button.dataset.walkFeedback + '"]').textContent = '';
      });
      output.value = ''; copyStatus.textContent = '';
      if (richOutput) { richOutput.innerHTML = ''; richOutput.hidden = true; }
      document.getElementById('walk-clear-confirm').hidden = true;
      saveStatus.textContent = 'This browser draft was cleared.';
      update();
    });
  }
  update();
}());

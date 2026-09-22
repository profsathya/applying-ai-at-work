(function () {
  'use strict';
  const config = JSON.parse(document.getElementById('guided-config').textContent);
  const storageKey = 'course-response:' + config.artifactId + ':' + config.version;
  const keys = ['work', 'home', 'other', 'additional'];
  const defaults = {categories: {work: 'Work', home: 'Home', other: 'Other', additional: ''}, entries: {work: '', home: '', other: '', additional: ''}, feedback: Object.create(null)};
  let state = defaults;
  let storageOK = true;
  let saveTimer;
  const byId = id => document.getElementById(id);
  const all = selector => Array.from(document.querySelectorAll(selector));
  function validObject(value) { return value && typeof value === 'object' && !Array.isArray(value); }
  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
      if (!validObject(saved)) return;
      for (const key of keys) {
        if (typeof saved.categories?.[key] === 'string') state.categories[key] = saved.categories[key].slice(0, 80);
        if (typeof saved.entries?.[key] === 'string') state.entries[key] = saved.entries[key].slice(0, 16000);
        if (validObject(saved.feedback?.[key]) && typeof saved.feedback[key].text === 'string' && typeof saved.feedback[key].onText === 'string') state.feedback[key] = saved.feedback[key];
      }
      if (validObject(saved.feedback?.final) && typeof saved.feedback.final.text === 'string' && typeof saved.feedback.final.onText === 'string') state.feedback.final = saved.feedback.final;
      byId('save-status').textContent = 'Your saved responses from this browser are loaded.';
    } catch (_) { storageOK = false; }
  }
  function save() {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); storageOK = true; }
    catch (_) { storageOK = false; }
    byId('storage-warning').hidden = storageOK;
    byId('save-status').textContent = storageOK
      ? 'Saved in this browser on this device. Keep your own copy before leaving.'
      : 'Browser saving is unavailable. Copy your list before leaving or reloading.';
  }
  function saveSoon() { clearTimeout(saveTimer); saveTimer = setTimeout(save, 400); }
  function heading(key) {
    const value = String(state.categories[key] || '').trim();
    return value || (key === 'additional' ? 'Custom heading' : key[0].toUpperCase() + key.slice(1));
  }
  function lines(key) {
    return String(state.entries[key] || '').replace(/\r/g, '').split('\n')
      .map(line => line.trim().replace(/^[-*\u2022]\s*/, '')).filter(Boolean);
  }
  function categories() {
    return keys.filter(key => key !== 'additional' || String(state.categories.additional || '').trim() || lines('additional').length);
  }
  function assembled(includeEmpty = false) {
    return categories().filter(key => includeEmpty || lines(key).length).map(key => {
      const items = lines(key);
      return heading(key) + '\n' + (items.length ? items.map(item => '- ' + item).join('\n') : '(no entries yet)');
    }).join('\n\n');
  }
  function reviewText(key) {
    if (key === 'final') return assembled(false);
    const items = lines(key);
    return items.length ? heading(key) + '\n' + items.map(item => '- ' + item).join('\n') : '';
  }
  function feedbackKey(key) { return JSON.stringify([key === 'final' ? 'all' : heading(key), reviewText(key)]); }
  function showFeedback(key, text, onText, error = false) {
    const box = document.querySelector('[data-feedback="' + key + '"]');
    if (!box) return;
    box.replaceChildren();
    const label = document.createElement('span');
    label.className = 'label';
    const stale = onText !== feedbackKey(key);
    label.textContent = error ? 'AI feedback' : stale ? 'Feedback on an earlier draft' : 'AI feedback';
    box.append(label, document.createTextNode(text));
    box.style.display = 'block';
  }
  function update() {
    all('[data-heading-display]').forEach(node => { node.textContent = heading(node.dataset.headingDisplay); });
    const custom = byId('list-additional');
    const customHasWork = Boolean(String(state.categories.additional || '').trim() || lines('additional').length);
    document.querySelector('[data-category-card="additional"]').hidden = !customHasWork;
    for (const key of [...keys, 'final']) {
      const button = document.querySelector('[data-ai="' + key + '"]');
      const current = reviewText(key);
      const stored = state.feedback[key];
      button.disabled = !current.trim() || (stored && stored.onText === feedbackKey(key));
      if (stored) showFeedback(key, stored.text, stored.onText);
    }
    byId('copy-list').disabled = !keys.some(key => lines(key).length);
    const output = byId('summary-output');
    if (output.value && output.style.display === 'block') output.value = copyText();
  }
  function copyText() {
    const groups = categories().filter(key => lines(key).length);
    return 'Brainstorm Your List\n\n' + groups.map(key => heading(key) + '\n' + lines(key).map(item => '- ' + item).join('\n')).join('\n\n');
  }
  async function requestFeedback(key, button) {
    const text = reviewText(key).trim();
    if (!text) return;
    const category = key === 'final' ? 'All categories' : heading(key);
    const box = document.querySelector('[data-feedback="' + key + '"]');
    const requestKey = feedbackKey(key);
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 45000);
    button.disabled = true;
    box.style.display = 'block';
    box.textContent = 'Reading what you wrote...';
    try {
      const response = await fetch(config.feedbackEndpoint, {
        method: 'POST', signal: controller.signal,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({target: key, category, response: text}),
      });
      const data = await response.json();
      if (!response.ok || typeof data.content !== 'string' || !data.content.trim()) throw new Error('Feedback unavailable');
      state.feedback[key] = {onText: requestKey, text: data.content.trim()};
      save();
      showFeedback(key, state.feedback[key].text, requestKey);
    } catch (_) {
      showFeedback(key, 'Feedback is unavailable right now. Your response is still here. Use the activity criteria and try again later.', requestKey, true);
    } finally {
      clearTimeout(timeout);
      update();
    }
  }
  load();
  all('[data-category]').forEach(input => {
    const key = input.dataset.category;
    input.value = state.categories[key];
    input.addEventListener('input', () => { state.categories[key] = input.value.slice(0, 80); update(); saveSoon(); });
    input.addEventListener('blur', save);
  });
  all('[data-entry]').forEach(input => {
    const key = input.dataset.entry;
    input.value = state.entries[key];
    input.addEventListener('input', () => { state.entries[key] = input.value.slice(0, 16000); update(); saveSoon(); });
    input.addEventListener('blur', save);
  });
  all('[data-ai]').forEach(button => button.addEventListener('click', () => requestFeedback(button.dataset.ai, button)));
  byId('copy-list').addEventListener('click', async () => {
    const output = byId('summary-output');
    const text = copyText();
    output.value = text;
    output.style.display = 'block';
    state.copiedAt = new Date().toISOString();
    save();
    try {
      await navigator.clipboard.writeText(text);
      byId('copy-status').className = 'status ok';
      byId('copy-status').textContent = 'Copied. Paste this into the matching Canvas text-entry submission. This page has not submitted your work.';
    } catch (_) {
      byId('copy-status').className = 'status';
      byId('copy-status').textContent = 'Copy did not work in this browser. Select and copy the text shown below.';
      output.focus(); output.select();
    }
  });
  byId('clear-draft').addEventListener('click', () => { byId('clear-confirmation').hidden = false; });
  byId('cancel-clear').addEventListener('click', () => { byId('clear-confirmation').hidden = true; });
  byId('confirm-clear').addEventListener('click', () => {
    try { localStorage.removeItem(storageKey); }
    catch (_) { byId('save-status').textContent = 'Could not clear the saved draft. Your current responses are still here.'; return; }
    state = {categories: {work: 'Work', home: 'Home', other: 'Other', additional: ''}, entries: {work: '', home: '', other: '', additional: ''}, feedback: Object.create(null)};
    all('[data-category]').forEach(input => { input.value = state.categories[input.dataset.category]; });
    all('[data-entry]').forEach(input => { input.value = ''; });
    all('.feedback').forEach(box => { box.replaceChildren(); box.style.display = 'none'; });
    byId('summary-output').value = ''; byId('summary-output').style.display = 'none';
    byId('clear-confirmation').hidden = true; byId('copy-status').textContent = '';
    update(); byId('save-status').textContent = 'This browser draft was cleared.';
  });
  update();
  if (!storageOK) { byId('storage-warning').hidden = false; }
}());

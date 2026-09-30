(function () {
  'use strict';
  // Collapsible repeated-table steps. Closed panels stay in the page, so drafts save and export as before.
  const steps = Array.from(document.querySelectorAll('[data-walk-repeated-table]'));
  if (!steps.length) return;
  const config = JSON.parse(document.getElementById('guided-config').textContent);
  const key = 'course-response:' + config.artifactId + ':steps';
  const ids = steps.map(step => step.dataset.walkStep);
  let open = new Set([ids[0]]);
  let done = new Set();

  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && Array.isArray(saved.open) && Array.isArray(saved.done)) {
      open = new Set(saved.open.filter(id => ids.includes(id)));
      done = new Set(saved.done.filter(id => ids.includes(id)));
    }
  } catch (_) { /* Storage is unavailable; use the default state for this visit. */ }

  function persist() {
    try { localStorage.setItem(key, JSON.stringify({open: [...open], done: [...done]})); }
    catch (_) { /* Open and done state still works for this visit. */ }
  }

  function resize(step) {
    step.querySelectorAll('.walk-source-table textarea').forEach(input => {
      input.style.height = 'auto';
      input.style.height = Math.max(62, Math.min(input.scrollHeight, 320)) + 'px';
      input.style.overflowY = input.scrollHeight > 320 ? 'auto' : 'hidden';
    });
  }

  function showStatus(step) {
    const id = step.dataset.walkStep;
    const writing = Array.from(step.querySelectorAll('[data-walk-answer]')).some(input => input.value.trim());
    const state = done.has(id) ? 'done' : writing ? 'in-progress' : 'not-started';
    const status = step.querySelector('[data-walk-status]');
    status.dataset.state = state;
    status.textContent = {'done': 'Done', 'in-progress': 'In progress', 'not-started': 'Not started'}[state];
  }

  function render(step) {
    const expanded = open.has(step.dataset.walkStep);
    const panel = step.querySelector('.walk-accordion-panel');
    step.querySelector('.walk-accordion-toggle').setAttribute('aria-expanded', String(expanded));
    const opening = expanded && panel.hidden;
    panel.hidden = !expanded;
    if (opening) resize(step);
    showStatus(step);
  }

  steps.forEach((step, index) => {
    const id = ids[index];
    const toggle = step.querySelector('.walk-accordion-toggle');
    toggle.addEventListener('click', () => {
      if (open.has(id)) open.delete(id); else open.add(id);
      render(step); persist();
    });
    step.addEventListener('input', () => showStatus(step));
    step.querySelector('[data-walk-done]').addEventListener('click', () => {
      done.add(id); open.delete(id);
      const next = steps[index + 1];
      if (next) open.add(ids[index + 1]);
      steps.forEach(render); persist();
      const target = next ? next.querySelector('.walk-accordion-toggle')
        : step.nextElementSibling?.querySelector('summary') || toggle;
      target.focus({preventScroll: true});
      const still = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
      (next || step.nextElementSibling || step).scrollIntoView({block: 'start', behavior: still ? 'auto' : 'smooth'});
    });
  });

  const clearYes = document.getElementById('walk-clear-yes');
  if (clearYes) clearYes.addEventListener('click', () => {
    // The draft script hides the confirmation only after it clears the draft.
    if (!document.getElementById('walk-clear-confirm').hidden) return;
    open = new Set([ids[0]]); done = new Set();
    try { localStorage.removeItem(key); } catch (_) { /* Nothing saved to remove. */ }
    steps.forEach(render);
  });

  steps.forEach(render);
}());

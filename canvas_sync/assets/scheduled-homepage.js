(function (root) {
  "use strict";
  function dayInZone(now, timezone) {
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: timezone, year: "numeric", month: "2-digit", day: "2-digit"
    }).formatToParts(now);
    const values = Object.fromEntries(parts.map(p => [p.type, p.value]));
    return `${values.year}-${values.month}-${values.day}`;
  }
  function selectSprint(schedule, now) {
    const day = dayInZone(now, schedule.timezone);
    if (schedule.override === "orientation") return { phase: "orientation", entry: schedule.orientation };
    if (Number.isInteger(schedule.override)) {
      return { phase: "override", entry: schedule.sprints[schedule.override - 1] };
    }
    if (day < schedule.start) return { phase: "orientation", entry: schedule.orientation };
    const active = schedule.sprints.find(entry => day >= entry.start && day < entry.until);
    return active ? { phase: "current", entry: active } : { phase: "review", entry: schedule.sprints[schedule.sprints.length - 1] };
  }
  function formatDate(value) {
    return new Intl.DateTimeFormat("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).format(new Date(value + "T12:00:00Z"));
  }
  const api = { dayInZone, selectSprint, formatDate };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (!root.document) return;
  const doc = root.document;
  const config = doc.getElementById("course-schedule");
  if (!config) return;
  const schedule = JSON.parse(config.textContent);
  const timezoneLabel = schedule.timezone === "America/Los_Angeles" ? "Pacific time" : schedule.timezone;
  const params = new URLSearchParams(root.location.search);
  const context = params.get("context") || (root.self !== root.top ? "canvas" : "web");
  const hash = new URLSearchParams(root.location.hash.slice(1));
  const incomingToken = hash.get("progress_token") || params.get("progress_token");
  let unsavedToken = null;
  if (incomingToken) {
    try {
      root.sessionStorage.setItem("canvas_progress_token", incomingToken);
      params.delete("progress_token");
      hash.delete("progress_token");
      root.history.replaceState(null, "", root.location.pathname + (params.size ? "?" + params : "") + (hash.size ? "#" + hash : ""));
    } catch (_error) { unsavedToken = incomingToken; }
  }
  function moduleHref(href) {
    const url = new URL(href, root.location.href);
    url.searchParams.set("context", context === "canvas" ? "canvas" : "web");
    // Only carry a token to this course's same-origin module page if storage is blocked.
    if (unsavedToken && url.origin === root.location.origin) url.hash = new URLSearchParams({progress_token:unsavedToken}).toString();
    return url.href;
  }
  doc.querySelectorAll("[data-module-link]").forEach(link => { link.href = moduleHref(link.getAttribute("href")); });
  const help = doc.getElementById("course-help");
  if (context === "canvas" && schedule.help.canvas) {
    help.href = schedule.help.canvas;
    help.target = "_top";
  } else {
    help.href = schedule.help.web;
  }
  for (const entry of schedule.sprints) {
    const row = doc.querySelector(`[data-sprint="${entry.number}"]`);
    row.querySelector(".module-dates").textContent = `${formatDate(entry.start)} - ${formatDate(entry.end)}`;
  }
  let previousKey = null;
  function refresh() {
    const selected = selectSprint(schedule, new Date());
    const entry = selected.entry;
    const key = `${selected.phase}:${entry.number || 0}`;
    if (key === previousKey) return;
    const orientation = selected.phase === "orientation";
    doc.getElementById("sprint-label").textContent = orientation ? "Getting started" : selected.phase === "review" ? "Course review" : selected.phase === "override" ? `Featured sprint · Sprint ${entry.number}` : `Current sprint · Sprint ${entry.number}`;
    doc.getElementById("sprint-title").textContent = entry.title;
    doc.getElementById("sprint-summary").textContent = entry.summary;
    doc.getElementById("sprint-dates").textContent = orientation ? `Sprint 1 begins ${formatDate(schedule.start)} · ${timezoneLabel}` : `${formatDate(entry.start)} - ${formatDate(entry.end)} · ${timezoneLabel}`;
    const action = doc.getElementById("sprint-action");
    action.hidden = !entry.href;
    if (entry.href) {
      action.href = moduleHref(entry.href);
      action.textContent = orientation ? "Open orientation" : selected.phase === "review" ? `Review Sprint ${entry.number}` : `Open Sprint ${entry.number}`;
    } else {
      action.removeAttribute("href");
    }
    const note = doc.getElementById("sprint-note");
    note.textContent = entry.note || "";
    note.hidden = !entry.note;
    doc.getElementById("sprint-unavailable").hidden = Boolean(entry.href);
    doc.querySelectorAll(".module-list a").forEach(link => link.removeAttribute("aria-current"));
    if (!orientation && entry.href) doc.querySelector(`[data-sprint="${entry.number}"] a`)?.setAttribute("aria-current", "step");
    if (previousKey !== null) doc.getElementById("schedule-announcement").textContent = `The featured module is now ${orientation ? "orientation" : "Sprint " + entry.number}.`;
    previousKey = key;
  }
  refresh();
  root.setInterval(refresh, 60000);
  root.addEventListener("pageshow", refresh);
  doc.addEventListener("visibilitychange", () => { if (!doc.hidden) refresh(); });
})(typeof window !== "undefined" ? window : globalThis);

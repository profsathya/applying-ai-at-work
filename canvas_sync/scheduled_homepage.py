"""Opt-in course-calendar landing page; never changes Canvas release settings."""

from __future__ import annotations

import html
import json
import re
from datetime import date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def validate_schedule(homepage: dict, slugs: set[str], artifact_sprints: set[int]) -> list[str]:
    schedule = homepage.get("schedule")
    if schedule is None:
        return []
    if not isinstance(schedule, dict):
        return ["schedule must be a mapping"]
    errors = []
    try:
        value = schedule.get("start_date")
        if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError
        date.fromisoformat(value)
    except ValueError:
        errors.append("schedule start_date must be a quoted YYYY-MM-DD calendar date")
    try:
        ZoneInfo(schedule.get("timezone", ""))
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        errors.append("schedule timezone must be a valid IANA timezone")
    days = schedule.get("sprint_days")
    if type(days) is not int or not 1 <= days <= 366:
        errors.append("schedule sprint_days must be an integer between 1 and 366")
    hidden = {m.get("sprint") for m in homepage.get("modules", []) if isinstance(m, dict) and m.get("hidden") and type(m.get("sprint")) is int}
    orientation = schedule.get("orientation_sprint")
    if type(orientation) is not int or orientation not in artifact_sprints or orientation in hidden:
        errors.append("schedule orientation_sprint must reference an existing visible module")
    if not isinstance(schedule.get("help_slug"), str) or schedule["help_slug"] not in slugs:
        errors.append("schedule help_slug must reference an existing artifact")
    entries = schedule.get("sprints")
    if not isinstance(entries, list) or not entries:
        return errors + ["schedule sprints must be a nonempty list"]
    seen = set()
    for number, entry in enumerate(entries, 1):
        label = f"schedule sprint {number}"
        if not isinstance(entry, dict):
            errors.append(f"{label} must be a mapping")
            continue
        if type(entry.get("number")) is not int or entry["number"] != number:
            errors.append(f"{label} number must be sequential, starting at 1")
        for key in ("title", "summary"):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                errors.append(f"{label} requires nonempty {key}")
        if "note" in entry and not isinstance(entry["note"], str):
            errors.append(f"{label} note must be text")
        ready = entry.get("ready")
        if type(ready) is not bool:
            errors.append(f"{label} ready must be a boolean")
        target = entry.get("sprint")
        if target is not None:
            if type(target) is not int or target not in artifact_sprints:
                errors.append(f"{label} sprint must reference an existing module or be null")
            if type(target) is int:
                if target in seen:
                    errors.append(f"{label} repeats a scheduled module")
                seen.add(target)
        if ready and (type(target) is not int or target in hidden):
            errors.append(f"{label} cannot be ready without an existing visible module")
    override = schedule.get("override")
    if override is not None and override != "orientation" and (
        type(override) is not int or not 1 <= override <= len(entries)
    ):
        errors.append("schedule override must be orientation, a scheduled sprint number, or null")
    return errors


def calendar_data(schedule: dict) -> dict:
    """Compute calendar dates in Python; browser selects using the course timezone."""
    start = date.fromisoformat(schedule["start_date"])
    days = schedule["sprint_days"]
    entries = []
    for index, entry in enumerate(schedule["sprints"]):
        first = start + timedelta(days=index * days)
        stop = first + timedelta(days=days)
        entries.append({
            **entry,
            "start": first.isoformat(),
            "end": (stop - timedelta(days=1)).isoformat(),
            "until": stop.isoformat(),
            "href": f"sprint-{entry['sprint']}.html" if entry["ready"] else None,
        })
    return {
        "timezone": schedule["timezone"],
        "start": start.isoformat(),
        "override": schedule.get("override"),
        "orientation": {
            "sprint": schedule["orientation_sprint"],
            "title": "Welcome and orientation",
            "summary": "Get familiar with the course and prepare for your first sprint.",
            "href": f"sprint-{schedule['orientation_sprint']}.html",
        },
        "sprints": entries,
    }


def _activity_groups_html(groups: list[dict]) -> str:
    sections = []
    for group in groups:
        rows = []
        for item in group["items"]:
            canvas = f' data-canvas-href="{html.escape(item["canvas"], quote=True)}"' if item.get("canvas") else ""
            rows.append(
                f'<li><a href="{html.escape(item["web"], quote=True)}" data-activity-link{canvas}>'
                f'<span class="activity-title">{html.escape(item["title"])}</span> '
                f'<span class="activity-meta">{html.escape(item["meta"])}</span></a></li>'
            )
        if rows:
            sections.append(f'<section class="activity-group"><h3>{html.escape(group["label"])}</h3><ul class="activity-list">{"".join(rows)}</ul></section>')
    return "".join(sections)


def render_scheduled_homepage(
    course: dict, schedule: dict, *, logo_url: str, help_link: dict,
    module_groups: dict | None = None, directory: bool = False,
) -> str:
    esc = html.escape
    data = calendar_data(schedule)
    data["help"] = help_link
    module_groups = module_groups or {}
    # Escape HTML-significant bytes even in non-executable JSON script elements.
    payload = json.dumps(data, ensure_ascii=True).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    assets = Path(__file__).parent / "assets"
    style = (assets / "scheduled-homepage.css").read_text()
    script = (assets / "scheduled-homepage.js").read_text()
    orientation = schedule["orientation_sprint"]
    rows = [f'<li><details class="directory-module"><summary>Welcome and orientation<span class="module-dates" id="orientation-dates">Before {esc(data["start"])}</span></summary>{_activity_groups_html(module_groups.get(orientation, []))}</details></li>']
    for entry in data["sprints"]:
        title = esc(f"Sprint {entry['number']}: {entry['title']}")
        dates = f'<span class="module-dates">{entry["start"]} to {entry["end"]}</span>'
        if entry["ready"]:
            row = f'<details class="directory-module"><summary>{title}{dates}</summary>{_activity_groups_html(module_groups.get(entry["sprint"], []))}</details>'
        else:
            row = f'<span>{title}</span>{dates}<span class="availability">Materials in preparation</span>'
        rows.append(f'<li data-sprint="{entry["number"]}">{row}</li>')
    if directory:
        content = f'''<a href="home.html?context=web" data-module-link>Back to home</a>
  <h2>Modules and dates</h2>
  <ul class="module-list">{"".join(rows)}</ul>
  <nav class="quick-links" aria-label="Course support"><a href="{esc(help_link['web'])}" id="course-help">Help and resources</a></nav>'''
    else:
        content = f'''<section class="current-sprint" aria-labelledby="sprint-title">
    <p class="eyebrow" id="sprint-label">Getting started</p>
    <h2 id="sprint-title">Welcome and orientation</h2>
    <p id="sprint-summary">Get familiar with the course and prepare for your first sprint.</p>
    <p class="dates" id="sprint-dates">Sprint 1 begins {data['start']}</p>
    <p class="note" id="sprint-note" hidden></p>
    <p class="availability" id="sprint-unavailable" hidden>Materials are in preparation. Visit Modules for available work.</p>
    <a class="primary" href="modules.html?context=web" id="course-modules">Go to Modules <span aria-hidden="true">→</span></a>
  </section>
  <p class="sr-only" id="schedule-announcement" aria-live="polite"></p>
  <nav class="quick-links" aria-label="Course navigation">
    <a href="{esc(help_link['web'])}" id="course-help">Help and resources</a>
  </nav>
  <noscript><p>Use Modules and its dates to find your current sprint.</p></noscript>'''
    title = esc(course["title"])
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - {"Modules" if directory else "Home"}</title>
<style>{style}</style>
</head>
<body>
<main class="course-home">
  <header class="brand"><img src="{esc(logo_url)}" alt="Computing Talent Initiative"><span>De Anza College</span></header>
  <h1>{title}</h1>
  {content}
  <footer><img src="{esc(logo_url)}" alt=""><span>{esc(course['footer'])}</span></footer>
</main>
<script id="course-schedule" type="application/json">{payload}</script>
<script>{script}</script>
</body>
</html>
'''

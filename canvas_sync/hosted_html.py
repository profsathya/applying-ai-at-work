"""Render Canvas Markdown artifacts as hosted static HTML pages.

The Markdown files remain the source of truth. This module renders those files
into the Common Curriculum static site shape and builds Canvas iframe shells
that point at the hosted pages.
"""

from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import course_dir_for_manifest, derive_artifact_id, load_json


DEFAULT_BASE_URL = "https://profsathya.github.io/Common-Curriculum/deanza"
DEFAULT_PATH_PREFIX = "deanza"
DEFAULT_AI_ENDPOINT = "https://ai-assisted-pedagogy.netlify.app/.netlify/functions/ai-proxy"
DEFAULT_PROGRESS_ENDPOINT = "https://canvas-progress-lti.netlify.app/.netlify/functions/canvas-progress"
CTI_LOGO_URL = (
    "https://computingtalentinitiative.org/wp-content/uploads/2026/06/"
    "New._CTI_Logo_RGB-1.png"
)


@dataclass(frozen=True)
class HostedConfig:
    enabled: bool
    base_url: str
    path_prefix: str
    progress_endpoint: str


def hosted_config_from_manifest(manifest: dict) -> HostedConfig:
    config = manifest.get("hosted_html") or {}
    return HostedConfig(
        enabled=bool(config.get("enabled", False)),
        base_url=str(config.get("base_url") or DEFAULT_BASE_URL).rstrip("/"),
        path_prefix=str(config.get("path_prefix") or DEFAULT_PATH_PREFIX).strip("/"),
        progress_endpoint=str(config.get("progress_endpoint") or DEFAULT_PROGRESS_ENDPOINT),
    )


def markdown_body_to_html(body: str) -> str:
    import markdown

    return markdown.markdown(
        body,
        extensions=["extra", "sane_lists", "smarty", "toc"],
        output_format="html5",
    )


def with_context(url: str, context: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.setdefault("context", context)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def iframe_shell(hosted_url: str, title: str, *, height: int = 900) -> str:
    canvas_url = with_context(hosted_url, "canvas")
    escaped_url = html_lib.escape(canvas_url, quote=True)
    escaped_title = html_lib.escape(title, quote=True)
    return (
        '<div class="hosted-html-shell">'
        f'<iframe title="{escaped_title}" src="{escaped_url}" width="100%" '
        f'height="{height}" loading="lazy" '
        'style="border:0; width:100%; min-height:900px;" '
        'allowfullscreen></iframe>'
        f'<p><a href="{escaped_url}" target="_blank" rel="noopener">'
        "Open hosted page in a new tab</a></p>"
        "</div>"
    )


def is_ai_activity_delivery(frontmatter: dict) -> bool:
    return frontmatter.get("delivery_mode", "canvas_native") == "ai_activity"


def _artifact_subdir(artifact_type: str) -> str:
    if artifact_type == "assignment":
        return "assignments"
    return "activities"


def _artifact_course_relative_path(frontmatter: dict) -> str:
    if is_ai_activity_delivery(frontmatter):
        return f"assignments/{frontmatter['slug']}.html"
    subdir = _artifact_subdir(frontmatter["type"])
    return f"{subdir}/{frontmatter['slug']}.html"


def _ai_activity_shell_course_relative_path(frontmatter: dict) -> str:
    return f"activities/{frontmatter['slug']}.html"


def _ai_activity_config_site_path(course_key: str, frontmatter: dict, manifest: dict) -> Path:
    config = hosted_config_from_manifest(manifest)
    return Path("activities") / config.path_prefix / course_key / f"{frontmatter['slug']}.json"


def artifact_hosted_info(
    md_path: Path,
    manifest_path: Path,
    manifest: dict | None = None,
    frontmatter: dict | None = None,
) -> dict:
    manifest_data = manifest or load_json(manifest_path)
    config = hosted_config_from_manifest(manifest_data)
    fm = frontmatter or parse_frontmatter(md_path)[0]
    course_key = course_dir_for_manifest(manifest_path).name
    hosted_path = f"{course_key}/{_artifact_course_relative_path(fm)}"
    quoted_path = "/".join(quote(part) for part in hosted_path.split("/"))
    return {
        "enabled": config.enabled,
        "hosted_path": hosted_path,
        "hosted_url": f"{config.base_url}/{quoted_path}",
        "output_path": Path(config.path_prefix) / hosted_path,
    }


def hosted_output_path(output_dir: Path, manifest: dict, hosted_path: str) -> Path:
    config = hosted_config_from_manifest(manifest)
    return output_dir / config.path_prefix / hosted_path


def _strip_leading_h1(rendered: str) -> str:
    return re.sub(
        r"^\s*<h1(?:\s[^>]*)?>.*?</h1>\s*",
        "",
        rendered,
        count=1,
        flags=re.IGNORECASE | re.DOTALL,
    )


def _wrap_sections(rendered: str) -> str:
    rendered = rendered.strip()
    if not rendered:
        return "<section><p>No page content was provided.</p></section>"
    if not re.search(r"<h2(?:\s|>)", rendered, flags=re.IGNORECASE):
        return f"<section>\n{rendered}\n</section>"

    pieces = re.split(r"(<h2[^>]*>.*?</h2>)", rendered, flags=re.IGNORECASE | re.DOTALL)
    sections: list[str] = []
    prelude = pieces[0].strip()
    if prelude:
        sections.append(f"<section>\n<h2>Overview</h2>\n{prelude}\n</section>")
    for index in range(1, len(pieces), 2):
        heading = pieces[index].strip()
        content = pieces[index + 1].strip() if index + 1 < len(pieces) else ""
        sections.append(f"<section>\n{heading}\n{content}\n</section>")
    return "\n\n".join(sections)


def _learning_goal(frontmatter: dict) -> str:
    title = frontmatter["title"]
    artifact_type = frontmatter["type"]
    if artifact_type == "assignment":
        return f"Apply the core idea from {title} in a focused Canvas submission."
    if artifact_type == "discussion":
        return f"Compare practical uses of {title} with peers and connect them to real work."
    if artifact_type == "quiz":
        return f"Check your understanding of {title} before moving forward."
    return f"Understand {title} and connect it to the work in this module."


def _type_label(artifact_type: str) -> str:
    labels = {
        "assignment": "Assignment",
        "discussion": "Discussion",
        "page": "Page",
        "quiz": "Quiz",
    }
    return labels.get(artifact_type, artifact_type.replace("_", " ").title())


def _state_entry_for_artifact(
    md_path: Path,
    manifest_path: Path,
    frontmatter: dict,
    state: dict | None,
) -> dict:
    if not state:
        return {}
    repo_root = course_dir_for_manifest(manifest_path).parent
    rel_path = str(md_path.resolve().relative_to(repo_root.resolve()))
    artifact_id = frontmatter.get("artifact_id") or derive_artifact_id(rel_path)
    artifacts = state.get("artifacts", {})
    return artifacts.get(rel_path) or artifacts.get(artifact_id) or {}


def _artifact_progress_id(md_path: Path, manifest_path: Path, frontmatter: dict) -> str:
    repo_root = course_dir_for_manifest(manifest_path).parent
    rel_path = str(md_path.resolve().relative_to(repo_root.resolve()))
    return str(frontmatter.get("artifact_id") or derive_artifact_id(rel_path))


def _canvas_item_url(manifest: dict, frontmatter: dict, entry: dict) -> str | None:
    instance = manifest.get("instance", {})
    base_url = str(instance.get("base_url") or "").rstrip("/")
    course_id = instance.get("course_id")
    if not base_url or not course_id:
        return None
    artifact_type = entry.get("canvas_type") or frontmatter["type"]
    canvas_id = entry.get("canvas_id")
    if artifact_type == "page" and entry.get("canvas_page_url"):
        page_url = quote(str(entry["canvas_page_url"]), safe="")
        return f"{base_url}/courses/{course_id}/pages/{page_url}"
    if artifact_type == "assignment" and canvas_id:
        return f"{base_url}/courses/{course_id}/assignments/{canvas_id}"
    if artifact_type == "discussion" and canvas_id:
        return f"{base_url}/courses/{course_id}/discussion_topics/{canvas_id}"
    if artifact_type == "quiz" and canvas_id:
        return f"{base_url}/courses/{course_id}/quizzes/{canvas_id}"
    if entry.get("canvas_module_id"):
        return f"{base_url}/courses/{course_id}/modules/{entry['canvas_module_id']}"
    return None


def _submit_guidance(frontmatter: dict, canvas_url: str | None) -> str:
    artifact_type = frontmatter["type"]
    if is_ai_activity_delivery(frontmatter):
        guidance = (
            "Complete the interactive activity, copy or download the JSON response file, "
            "and upload it to the Canvas assignment."
        )
        link = ""
        if canvas_url:
            escaped = html_lib.escape(canvas_url, quote=True)
            link = f'\n      <p><a href="{escaped}" target="_blank" rel="noopener">Open the Canvas assignment</a></p>'
        return (
            '<div class="submit">\n'
            "      <h2>Submit to Canvas</h2>\n"
            f"      <p>{html_lib.escape(guidance)}</p>"
            f"{link}\n"
            "    </div>"
        )
    guidance = {
        "assignment": "Use the Canvas assignment to submit your work.",
        "discussion": "Use the Canvas discussion to post your response and reply to peers.",
        "page": "Read this page in full. No Canvas submission is required.",
        "quiz": "Use the Canvas quiz to complete the check.",
    }.get(artifact_type, "Return to Canvas for the next step.")
    link = ""
    if canvas_url:
        escaped = html_lib.escape(canvas_url, quote=True)
        label = html_lib.escape(_type_label(artifact_type).lower())
        link = f'\n      <p><a href="{escaped}" target="_blank" rel="noopener">Open the Canvas {label}</a></p>'
    return (
        '<div class="submit">\n'
        "      <h2>Submit to Canvas</h2>\n"
        f"      <p>{html_lib.escape(guidance)}</p>"
        f"{link}\n"
        "    </div>"
    )


def render_artifact_document(
    frontmatter: dict,
    body: str,
    manifest: dict,
    hosted_info: dict,
    state_entry: dict | None = None,
) -> str:
    rendered = _strip_leading_h1(markdown_body_to_html(body))
    sections = _wrap_sections(rendered)
    title = html_lib.escape(frontmatter["title"])
    module = html_lib.escape(frontmatter["module"])
    course_key = html_lib.escape(str(hosted_info["hosted_path"]).split("/", 1)[0])
    artifact_type = html_lib.escape(_type_label(frontmatter["type"]))
    sprint = int(frontmatter["sprint"])
    goal = html_lib.escape(_learning_goal(frontmatter))
    canvas_url = _canvas_item_url(manifest, frontmatter, state_entry or {})
    submit_guidance = _submit_guidance(frontmatter, canvas_url)
    back_href = f"../sprint-{sprint}.html?context=web"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {module}</title>
  <style>
    :root {{
      --bg: #fafafa;
      --surface: #ffffff;
      --text: #1a1a1a;
      --muted: #555;
      --border: #e0e0e0;
      --accent: #2c5282;
      --accent-light: #ebf4ff;
      --radius: 8px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 20px 16px;
      font: 16px/1.65 -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      color: var(--text);
      background: var(--bg);
    }}
    .activity {{ max-width: 760px; margin: 0 auto; }}
    .meta {{
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin: 0 0 6px;
    }}
    h1 {{ font-size: 22px; font-weight: 700; margin: 0 0 18px; line-height: 1.3; }}
    .goal {{
      background: var(--accent-light);
      border-left: 4px solid var(--accent);
      border-radius: var(--radius);
      padding: 14px 16px;
      margin: 0 0 20px;
    }}
    .goal h2, .submit h2 {{
      margin: 0 0 6px;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }}
    .goal h2 {{ color: var(--accent); }}
    .goal p {{ margin: 0; }}
    section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin: 0 0 16px;
    }}
    section h2 {{ margin: 0 0 10px; font-size: 17px; font-weight: 700; }}
    section h3 {{ margin: 16px 0 8px; font-size: 15px; }}
    section p {{ margin: 8px 0; }}
    ol, ul {{ padding-left: 22px; margin: 8px 0; }}
    li {{ margin-bottom: 6px; }}
    code {{
      background: #f3f4f6;
      border: 1px solid #e5e7eb;
      border-radius: 4px;
      padding: 1px 4px;
      font-size: 0.92em;
    }}
    pre {{
      background: #111827;
      color: #f9fafb;
      border-radius: var(--radius);
      padding: 12px 14px;
      overflow-x: auto;
    }}
    pre code {{ background: transparent; border: 0; color: inherit; padding: 0; }}
    a {{ color: var(--accent); word-break: break-word; }}
    .submit {{
      background: #ecfdf5;
      border: 1px solid #6ee7b7;
      border-left: 4px solid #10b981;
      border-radius: var(--radius);
      padding: 14px 18px;
      margin: 22px 0 12px;
    }}
    .submit h2 {{ color: #065f46; }}
    .submit p {{ margin: 4px 0; }}
    footer {{ text-align: center; margin: 28px 0 8px; opacity: 0.55; }}
    footer img {{ height: 22px; }}
    .back-link {{
      display: none;
      font-size: 13px;
      color: var(--accent);
      text-decoration: none;
      margin: 0 0 12px;
    }}
    .back-link:hover {{ text-decoration: underline; }}
    .ctx-web .back-link {{ display: inline-block; }}
  </style>
  <script>
    (function() {{
      var ctx = new URLSearchParams(location.search).get('context')
        || (window.self !== window.top ? 'canvas' : 'web');
      if (ctx !== 'canvas') {{
        document.documentElement.classList.add('ctx-web');
      }}
      document.addEventListener('DOMContentLoaded', function() {{
        document.querySelectorAll('a[data-keep-context]').forEach(function(a) {{
          try {{
            var u = new URL(a.getAttribute('href'), location.href);
            if (!u.searchParams.has('context')) {{
              u.searchParams.set('context', ctx);
              a.href = u.href;
            }}
          }} catch (e) {{ }}
        }});
      }});
    }})();
  </script>
</head>
<body>
  <div class="activity">
    <a class="back-link" href="{back_href}" data-keep-context>&larr; Back to Module</a>
    <p class="meta">{course_key} &middot; Sprint {sprint} &middot; {module} &middot; {artifact_type}</p>
    <h1>{title}</h1>

    <div class="goal">
      <h2>Learning goal</h2>
      <p>{goal}</p>
    </div>

    {sections}

    {submit_guidance}

    <footer><img src="{CTI_LOGO_URL}" alt="Computing Talent Initiative" onerror="this.style.display='none'"></footer>
  </div>
</body>
</html>
"""


def _plain_description_from_body(body: str) -> str:
    for paragraph in re.split(r"\n\s*\n", body):
        paragraph = paragraph.strip()
        if not paragraph or paragraph.startswith("#"):
            continue
        cleaned = re.sub(r"[#*_`>]+", "", paragraph)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if cleaned:
            return cleaned[:320]
    return ""


def _ai_activity_settings(frontmatter: dict, manifest: dict) -> dict:
    activity = frontmatter.get("ai_activity") or {}
    settings = dict(activity.get("settings") or {})
    manifest_activity = manifest.get("ai_activity") or {}
    endpoint = (
        activity.get("ai_endpoint")
        or settings.get("aiEndpoint")
        or manifest_activity.get("default_ai_endpoint")
        or DEFAULT_AI_ENDPOINT
    )
    settings["aiEndpoint"] = endpoint
    settings.setdefault("exportMode", "json")
    settings.setdefault("maxRetries", 3)
    settings.setdefault("showHintsAfterAttempt", 2)
    return settings


def _ai_activity_config(frontmatter: dict, body: str, manifest: dict, course_key: str) -> dict:
    activity = frontmatter.get("ai_activity") or {}
    config: dict = {
        "activityId": activity["activity_id"],
        "version": str(activity.get("version") or "1.0"),
        "course": activity.get("course") or course_key,
        "title": activity.get("title") or frontmatter["title"],
        "description": activity.get("description") or _plain_description_from_body(body),
        "settings": _ai_activity_settings(frontmatter, manifest),
        "questions": activity.get("questions") or [],
    }
    version_notes = activity.get("version_notes") or activity.get("versionNotes")
    if version_notes:
        config["versionNotes"] = version_notes
    if activity.get("roster"):
        config["roster"] = activity["roster"]
    return config


def _ai_activity_course_theme(frontmatter: dict, manifest: dict) -> str:
    activity = frontmatter.get("ai_activity") or {}
    manifest_activity = manifest.get("ai_activity") or {}
    return activity.get("course_theme") or manifest_activity.get("course_theme") or "cst349"


def _render_ai_activity_wrapper_document(
    frontmatter: dict,
    body: str,
    manifest: dict,
    hosted_info: dict,
    state_entry: dict | None = None,
) -> str:
    rendered = _strip_leading_h1(markdown_body_to_html(body))
    sections = _wrap_sections(rendered)
    title = html_lib.escape(frontmatter["title"])
    module = html_lib.escape(frontmatter["module"])
    course_key = html_lib.escape(str(hosted_info["hosted_path"]).split("/", 1)[0])
    artifact_type = html_lib.escape(_type_label(frontmatter["type"]))
    sprint = int(frontmatter["sprint"])
    points = frontmatter.get("points")
    canvas_url = _canvas_item_url(manifest, frontmatter, state_entry or {})
    canvas_link = ""
    if canvas_url:
        canvas_link = (
            f'<a class="secondary" href="{html_lib.escape(canvas_url, quote=True)}" '
            'target="_blank" rel="noopener">Submit on Canvas</a>'
        )
    activity_href = f"../activities/{html_lib.escape(frontmatter['slug'], quote=True)}.html?context=web"
    back_href = f"../sprint-{sprint}.html?context=web"
    points_text = "Ungraded" if points is None else f"{points:g} points"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | {module}</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 20px 16px;
      font: 16px/1.65 -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      color: #111827;
      background: #f8fafc;
    }}
    .activity {{ max-width: 760px; margin: 0 auto; }}
    .meta {{
      font-size: 12px;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin: 0 0 6px;
    }}
    h1 {{ font-size: 24px; line-height: 1.25; margin: 0 0 18px; }}
    section, .launch, .submit {{
      background: #fff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 18px 20px;
      margin: 0 0 16px;
    }}
    section h2, .launch h2, .submit h2 {{ margin: 0 0 10px; font-size: 17px; }}
    .launch {{
      border-left: 4px solid #4f46e5;
      background: #eef2ff;
    }}
    .submit {{
      border-left: 4px solid #059669;
      background: #ecfdf5;
    }}
    .actions {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 14px; }}
    a.button, a.secondary {{
      display: inline-block;
      padding: 11px 16px;
      border-radius: 8px;
      text-decoration: none;
      font-weight: 700;
    }}
    a.button {{ color: #fff; background: #4f46e5; }}
    a.secondary {{ color: #065f46; background: #d1fae5; }}
    a {{ color: #4f46e5; word-break: break-word; }}
    .back-link {{
      display: none;
      font-size: 13px;
      margin: 0 0 12px;
    }}
    .ctx-web .back-link {{ display: inline-block; }}
  </style>
  <script>
    (function() {{
      var ctx = new URLSearchParams(location.search).get('context')
        || (window.self !== window.top ? 'canvas' : 'web');
      if (ctx !== 'canvas') {{
        document.documentElement.classList.add('ctx-web');
      }}
    }})();
  </script>
</head>
<body>
  <div class="activity">
    <a class="back-link" href="{back_href}">&larr; Back to Module</a>
    <p class="meta">{course_key} &middot; Sprint {sprint} &middot; {module} &middot; {artifact_type} &middot; {html_lib.escape(points_text)}</p>
    <h1>{title}</h1>

    {sections}

    <div class="launch">
      <h2>Start the AI activity</h2>
      <p>Complete the interactive activity in one sitting on the same device. Your responses are saved in this browser while you work.</p>
      <div class="actions">
        <a class="button" href="{activity_href}">Open activity &rarr;</a>
      </div>
    </div>

    <div class="submit">
      <h2>Submit to Canvas</h2>
      <p>When you finish, copy or download the JSON response file from the activity and upload it to the Canvas assignment.</p>
      <div class="actions">{canvas_link}</div>
    </div>
  </div>
</body>
</html>
"""


def _render_ai_activity_shell_document(
    frontmatter: dict,
    manifest: dict,
    course_key: str,
    state_entry: dict | None = None,
) -> str:
    title = html_lib.escape(frontmatter["title"])
    config = hosted_config_from_manifest(manifest)
    config_url = f"../../../activities/{config.path_prefix}/{course_key}/{frontmatter['slug']}.json"
    canvas_url = _canvas_item_url(manifest, frontmatter, state_entry or {}) or ""
    course_theme = _ai_activity_course_theme(frontmatter, manifest)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="../../../css/activity-styles.css">
  <style>
    body {{
      margin: 0;
      background: #f8fafc;
      min-height: 100vh;
    }}
  </style>
</head>
<body>
  <div id="activity-container"></div>

  <script src="../../../js/activity-components.js"></script>
  <script src="../../../js/activity-engine.js"></script>
  <script>
    ActivityEngine.init({{
      containerId: 'activity-container',
      configUrl: {json.dumps(config_url)},
      courseTheme: {json.dumps(course_theme)},
      canvasUrl: {json.dumps(canvas_url)}
    }});
  </script>
</body>
</html>
"""


def _render_ai_activity_artifact(
    md_path: Path,
    manifest_path: Path,
    output_dir: Path,
    *,
    manifest: dict,
    state: dict | None,
) -> dict:
    fm, body = parse_frontmatter(md_path)
    course_key = course_dir_for_manifest(manifest_path).name
    hosted_info = artifact_hosted_info(md_path, manifest_path, manifest, fm)
    state_entry = _state_entry_for_artifact(md_path, manifest_path, fm, state or manifest)
    wrapper = _render_ai_activity_wrapper_document(fm, body, manifest, hosted_info, state_entry)
    shell = _render_ai_activity_shell_document(fm, manifest, course_key, state_entry)
    activity_config = _ai_activity_config(fm, body, manifest, course_key)

    wrapper_path = hosted_output_path(output_dir, manifest, hosted_info["hosted_path"])
    shell_hosted_path = f"{course_key}/{_ai_activity_shell_course_relative_path(fm)}"
    shell_path = hosted_output_path(output_dir, manifest, shell_hosted_path)
    config_site_path = _ai_activity_config_site_path(course_key, fm, manifest)
    config_path = output_dir / config_site_path

    wrapper_changed, wrapper_hash = _write_if_changed(wrapper_path, wrapper)
    shell_changed, shell_hash = _write_if_changed(shell_path, shell)
    config_changed, config_hash = _write_if_changed(
        config_path,
        json.dumps(activity_config, indent=2, sort_keys=False) + "\n",
    )
    hosted_hash = hashlib.sha256(
        f"{wrapper_hash}:{shell_hash}:{config_hash}".encode("utf-8")
    ).hexdigest()

    return {
        "file": str(md_path),
        "hosted_path": hosted_info["hosted_path"],
        "hosted_url": hosted_info["hosted_url"],
        "output_path": str(wrapper_path),
        "activity_hosted_path": shell_hosted_path,
        "activity_output_path": str(shell_path),
        "config_path": str(config_site_path),
        "config_output_path": str(config_path),
        "hosted_hash": hosted_hash,
        "changed": wrapper_changed or shell_changed or config_changed,
        "outputs": [
            {"path": str(wrapper_path), "hash": wrapper_hash, "changed": wrapper_changed},
            {"path": str(shell_path), "hash": shell_hash, "changed": shell_changed},
            {"path": str(config_path), "hash": config_hash, "changed": config_changed},
        ],
    }


def _write_if_changed(path: Path, text: str) -> tuple[bool, str]:
    payload = text.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == digest:
        return False, digest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(payload)
    return True, digest


def render_hosted_artifact(
    md_path: Path,
    manifest_path: Path,
    output_dir: Path,
    *,
    manifest: dict | None = None,
    state: dict | None = None,
) -> dict:
    manifest_data = manifest or load_json(manifest_path)
    config = hosted_config_from_manifest(manifest_data)
    if not config.enabled:
        raise ValueError(f"Hosted HTML is not enabled for {manifest_path}")
    fm, body = parse_frontmatter(md_path)
    if fm["type"] == "module_header":
        raise ValueError(f"Module headers do not render as hosted HTML: {md_path}")
    if is_ai_activity_delivery(fm):
        return _render_ai_activity_artifact(
            md_path,
            manifest_path,
            output_dir,
            manifest=manifest_data,
            state=state,
        )
    hosted_info = artifact_hosted_info(md_path, manifest_path, manifest_data, fm)
    state_entry = _state_entry_for_artifact(md_path, manifest_path, fm, state or manifest_data)
    document = render_artifact_document(fm, body, manifest_data, hosted_info, state_entry)
    output_path = hosted_output_path(output_dir, manifest_data, hosted_info["hosted_path"])
    changed, hosted_hash = _write_if_changed(output_path, document)
    return {
        "file": str(md_path),
        "hosted_path": hosted_info["hosted_path"],
        "hosted_url": hosted_info["hosted_url"],
        "output_path": str(output_path),
        "hosted_hash": hosted_hash,
        "changed": changed,
    }


def _artifact_sort_key(item: tuple[Path, dict]) -> tuple[int, int, str]:
    _path, fm = item
    return (int(fm.get("sprint", 0)), int(fm.get("position", 9999)), fm.get("title", ""))


def _load_artifact_items(paths: list[Path]) -> list[tuple[Path, dict]]:
    items: list[tuple[Path, dict]] = []
    for md_path in paths:
        fm, _body = parse_frontmatter(md_path)
        if fm["type"] != "module_header":
            items.append((md_path, fm))
    return sorted(items, key=_artifact_sort_key)


def _homepage_path(course_dir: Path) -> Path:
    return course_dir / "homepage.yaml"


def _load_homepage_metadata(course_dir: Path) -> dict | None:
    path = _homepage_path(course_dir)
    if not path.exists():
        return None
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: homepage metadata must be a mapping")
    return payload


def _walk_homepage_strings(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        strings: list[str] = []
        for item in value:
            strings.extend(_walk_homepage_strings(item))
        return strings
    if isinstance(value, dict):
        strings = []
        for item in value.values():
            strings.extend(_walk_homepage_strings(item))
        return strings
    return []


def _homepage_entry_slug(entry: object) -> str | None:
    if isinstance(entry, str):
        return entry
    if isinstance(entry, dict) and isinstance(entry.get("slug"), str):
        return entry["slug"]
    return None


def validate_homepage_metadata(course_dir: Path) -> list[str]:
    path = _homepage_path(course_dir)
    if not path.exists():
        return []

    errors: list[str] = []
    try:
        payload = _load_homepage_metadata(course_dir)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        return [f"{path}: {exc}"]

    if payload is None:
        return []

    forbidden = ("<iframe", "<script", "<style", "javascript:", "onload=")
    for text in _walk_homepage_strings(payload):
        lowered = text.lower()
        for pattern in forbidden:
            if pattern in lowered:
                errors.append(f"{path}: contains forbidden homepage text pattern {pattern!r}")
        if "\u2014" in text:
            errors.append(f"{path}: contains em-dash; use hyphen, colon, or sentence break")

    modules = payload.get("modules", [])
    if modules is None:
        modules = []
    if not isinstance(modules, list):
        errors.append(f"{path}: modules must be a list")
        return errors

    artifact_slugs: set[str] = set()
    for md_path in sorted((course_dir / "sprints").glob("sprint-*/*.md")):
        try:
            fm, _body = parse_frontmatter(md_path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{md_path}: {exc}")
            continue
        if fm.get("type") == "module_header":
            continue
        slug = fm.get("slug")
        if not isinstance(slug, str):
            continue
        if slug in artifact_slugs:
            errors.append(f"{md_path}: duplicate artifact slug {slug!r}")
        artifact_slugs.add(slug)

    configured_slugs: dict[str, str] = {}
    for module_index, module in enumerate(modules, start=1):
        label = f"{path}: module {module_index}"
        if not isinstance(module, dict):
            errors.append(f"{label} must be a mapping")
            continue
        if not isinstance(module.get("sprint"), int):
            errors.append(f"{label} requires integer sprint")
        groups = module.get("groups", [])
        if not isinstance(groups, list):
            errors.append(f"{label} groups must be a list")
            continue
        for group_index, group in enumerate(groups, start=1):
            group_label = f"{label} group {group_index}"
            if not isinstance(group, dict):
                errors.append(f"{group_label} must be a mapping")
                continue
            items = group.get("items", [])
            if not isinstance(items, list):
                errors.append(f"{group_label} items must be a list")
                continue
            for item_index, entry in enumerate(items, start=1):
                slug = _homepage_entry_slug(entry)
                item_label = f"{group_label} item {item_index}"
                if not slug:
                    errors.append(f"{item_label} requires slug")
                    continue
                if slug in configured_slugs:
                    errors.append(
                        f"{item_label} duplicates slug {slug!r}; already used by {configured_slugs[slug]}"
                    )
                configured_slugs[slug] = item_label
                if slug not in artifact_slugs:
                    errors.append(f"{item_label} references missing artifact slug {slug!r}")

    return errors


def _course_metadata(course_dir: Path, course_key: str, homepage: dict | None) -> dict:
    course_yaml = course_dir / "course.yaml"
    course_data: dict = {}
    if course_yaml.exists():
        try:
            loaded = yaml.safe_load(course_yaml.read_text(encoding="utf-8")) or {}
            if isinstance(loaded, dict) and isinstance(loaded.get("course"), dict):
                course_data = loaded["course"]
        except (OSError, yaml.YAMLError):
            course_data = {}
    homepage_course = homepage.get("course", {}) if isinstance(homepage, dict) else {}
    if not isinstance(homepage_course, dict):
        homepage_course = {}
    title = homepage_course.get("title") or course_data.get("name") or f"{course_key} hosted course pages"
    lead = homepage_course.get("lead") or (
        "Your path through the course. Every module opens with what you will learn and why, "
        "so you always know where you are and what you are building toward."
    )
    footer = homepage_course.get("footer") or "Computing Talent Initiative - De Anza College"
    return {"course_key": course_key, "title": str(title), "lead": str(lead), "footer": str(footer)}


def _module_config_by_sprint(homepage: dict | None) -> dict[int, dict]:
    configs: dict[int, dict] = {}
    if not isinstance(homepage, dict):
        return configs
    modules = homepage.get("modules", [])
    if not isinstance(modules, list):
        return configs
    for module in modules:
        if isinstance(module, dict) and isinstance(module.get("sprint"), int):
            configs[module["sprint"]] = module
    return configs


def _homepage_item_groups(
    sprint_items: list[tuple[Path, dict]],
    module_config: dict,
) -> list[tuple[str, list[tuple[Path, dict, dict]]]]:
    by_slug = {fm["slug"]: (path, fm) for path, fm in sprint_items}
    used: set[str] = set()
    groups: list[tuple[str, list[tuple[Path, dict, dict]]]] = []

    for group in module_config.get("groups", []) if isinstance(module_config.get("groups", []), list) else []:
        if not isinstance(group, dict):
            continue
        label = str(group.get("label") or "Items")
        group_items: list[tuple[Path, dict, dict]] = []
        for entry in group.get("items", []) if isinstance(group.get("items", []), list) else []:
            slug = _homepage_entry_slug(entry)
            if not slug or slug not in by_slug:
                continue
            item_config = dict(entry) if isinstance(entry, dict) else {"slug": slug}
            path, fm = by_slug[slug]
            group_items.append((path, fm, item_config))
            used.add(slug)
        if group_items:
            groups.append((label, group_items))

    additional = [(path, fm, {"slug": fm["slug"]}) for path, fm in sprint_items if fm["slug"] not in used]
    if additional:
        label = str(module_config.get("additional_label") or "Additional items")
        groups.append((label, additional))
    return groups


def _homepage_icon_svg(kind: str, *, selfcheck: bool = False) -> str:
    if selfcheck:
        return (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
            '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.5 2.5 5-5.5"/></svg>'
        )
    if kind == "assignment":
        return (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/>'
            '<path d="M14 3v6h6"/><path d="M8 13h8M8 17h5"/></svg>'
        )
    if kind == "discussion":
        return (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
        )
    if kind == "quiz":
        return (
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
            '<path d="M3 17l6-6 4 4 8-8"/><path d="M14 7h6v6"/></svg>'
        )
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">'
        '<path d="M5 3h11l3 3v15H5z"/><path d="M8 8h8M8 12h8M8 16h5"/></svg>'
    )


def _default_homepage_meta(frontmatter: dict) -> str:
    labels = {
        "assignment": "Assignment - submit in Canvas",
        "discussion": "Discussion - post and respond in Canvas",
        "page": "Page - read before the applied work",
        "quiz": "Quiz - check your understanding before moving on",
    }
    return labels.get(frontmatter["type"], _type_label(frontmatter["type"]))


def _render_homepage_item(
    md_path: Path,
    frontmatter: dict,
    item_config: dict,
    manifest_path: Path,
    manifest: dict,
    state: dict | None,
) -> str:
    title = html_lib.escape(str(item_config.get("title") or frontmatter["title"]))
    meta = html_lib.escape(str(item_config.get("meta") or _default_homepage_meta(frontmatter)))
    badge = item_config.get("badge")
    badge_html = ""
    if badge:
        badge_class = " optional" if str(badge).lower() == "optional" else ""
        badge_html = f'<span class="badge{badge_class}">{html_lib.escape(str(badge))}</span>'
    selfcheck = bool(item_config.get("selfcheck")) or bool(badge)
    item_class = "item selfcheck" if selfcheck else "item"
    href = f"{_artifact_course_relative_path(frontmatter)}?context=web"
    state_entry = _state_entry_for_artifact(md_path, manifest_path, frontmatter, state or manifest)
    canvas_url = _canvas_item_url(manifest, frontmatter, state_entry)
    canvas_attr = f' data-canvas-href="{html_lib.escape(canvas_url, quote=True)}"' if canvas_url else ""
    module_item_id = state_entry.get("canvas_module_item_id")
    progress_attrs = ""
    progress_html = ""
    if module_item_id is not None:
        progress_id = html_lib.escape(_artifact_progress_id(md_path, manifest_path, frontmatter), quote=True)
        completion = state_entry.get("completion_requirement")
        completion_attr = (
            f' data-completion-requirement="{html_lib.escape(str(completion), quote=True)}"'
            if completion else ""
        )
        progress_attrs = (
            f' data-progress-id="{progress_id}"'
            f' data-canvas-module-item-id="{html_lib.escape(str(module_item_id), quote=True)}"'
            f'{completion_attr} data-progress-state="unavailable"'
        )
        progress_html = (
            '<span class="progress-check" aria-label="Progress unavailable" title="Progress unavailable">'
            '<span class="progress-box"></span><span class="progress-label">Progress unavailable</span>'
            '</span>'
        )
    verify = item_config.get("verify")
    verify_html = ""
    if verify:
        verify_html = (
            '<div class="verify">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">'
            '<path d="M16 11a4 4 0 1 0-4-4 4 4 0 0 0 4 4z"/>'
            '<path d="M3 21v-2a5 5 0 0 1 5-5h3"/><path d="M16 14l2 2 4-4"/></svg>'
            f"<span>{html_lib.escape(str(verify))}</span></div>"
        )
    return (
        f'<div class="{item_class}"{progress_attrs}>'
        f'<span class="ico">{_homepage_icon_svg(frontmatter["type"], selfcheck=selfcheck)}</span>'
        '<div class="body">'
        f'<div class="title"><a target="_blank" rel="noopener" href="{html_lib.escape(href, quote=True)}"'
        f'{canvas_attr}>{title}</a>{badge_html}</div>'
        f'<div class="meta">{meta}</div>{verify_html}'
        '</div>'
        f'{progress_html}</div>'
    )


def _render_goal_block(module_config: dict) -> str:
    goals = module_config.get("learning_goals") or module_config.get("goal")
    if isinstance(goals, list):
        items = "\n".join(f"<li>{html_lib.escape(str(goal))}</li>" for goal in goals)
        goal_body = f'<ul class="goal-list">\n{items}\n</ul>'
    elif goals:
        goal_body = html_lib.escape(str(goals))
    else:
        goal_body = "Complete this module and carry the work forward."
    return (
        '<div class="goal">'
        '<div class="label">Module Learning Goals</div>'
        f'<div class="text">{goal_body}</div>'
        '</div>'
    )


def _render_prereq(module_config: dict, *, first: bool) -> str:
    text = module_config.get("prereq") or ("Start here." if first else "")
    if not text:
        return ""
    if first:
        icon = '<path d="M12 2l3 7h7l-5.5 4 2 7L12 17l-6.5 3 2-7L2 9h7z"/>'
    else:
        icon = '<path d="M5 12h14M13 6l6 6-6 6"/>'
    return (
        '<div class="prereq">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">{icon}</svg>'
        f'<span>{html_lib.escape(str(text))}</span>'
        '</div>'
    )


def _render_career_module(
    sprint: int,
    sprint_items: list[tuple[Path, dict]],
    module_config: dict,
    manifest_path: Path,
    manifest: dict,
    state: dict | None,
    *,
    first: bool,
    force_open: bool = False,
) -> str:
    module_title = str(module_config.get("title") or sprint_items[0][1].get("module") or f"Sprint {sprint}")
    tag = str(module_config.get("tag") or f"Sprint {sprint}")
    open_attr = " open" if force_open or module_config.get("open") else ""
    muted = bool(module_config.get("muted")) and not force_open
    module_class = "module module--muted" if muted else "module"
    not_ready = '<span class="not-ready">Not ready yet</span>' if muted else ""
    groups_html = []
    for label, group_items in _homepage_item_groups(sprint_items, module_config):
        groups_html.append(f'<div class="group-label">{html_lib.escape(label)}</div>')
        for md_path, fm, item_config in group_items:
            groups_html.append(_render_homepage_item(md_path, fm, item_config, manifest_path, manifest, state))
    return (
        f'<details class="{module_class}"{open_attr}>'
        '<summary class="module-head">'
        f'<span class="name">{html_lib.escape(module_title)}</span>'
        f'<span class="tag">{html_lib.escape(tag)}</span>{not_ready}<span class="chev">&#9656;</span>'
        '</summary>'
        f'{_render_goal_block(module_config)}'
        f'{_render_prereq(module_config, first=first)}'
        '<div class="items">'
        + "\n".join(groups_html)
        + '</div></details>'
    )


def _career_homepage_document(
    course_meta: dict,
    modules_html: str,
    *,
    title_suffix: str = "Home",
    back_href: str | None = None,
    progress_endpoint: str | None = None,
) -> str:
    back = ""
    if back_href:
        back = f'<a class="back-link" href="{html_lib.escape(back_href, quote=True)}" data-keep-context>&larr; Back to course home</a>'
    progress_endpoint_json = json.dumps(progress_endpoint or DEFAULT_PROGRESS_ENDPOINT)
    course_key_json = json.dumps(str(course_meta.get("course_key") or ""))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_lib.escape(course_meta["title"])} - {html_lib.escape(title_suffix)}</title>
<style>
  :root{{
    --blue:#0374B5; --blue-dark:#0a5a8a; --text:#2D3B45; --muted:#6B7780;
    --border:#C7CDD1; --border-light:#E8EAEC;
    --modhead:#F5F5F5; --goal-bg:#F3F8FB; --goal-border:#0374B5;
    --check-bg:#F2FAF5; --check-border:#0B874B; --check:#0B874B; --warn:#9B6A00;
    --font:"Lato","Helvetica Neue",Helvetica,Arial,sans-serif;
  }}
  *{{box-sizing:border-box;}}
  html,body{{margin:0;padding:0;}}
  body{{font-family:var(--font);color:var(--text);background:#fff;font-size:14px;line-height:1.45;-webkit-font-smoothing:antialiased;}}
  a{{color:var(--blue);text-decoration:none;}}
  a:hover{{text-decoration:underline;color:var(--blue-dark);}}
  .page{{max-width:1040px;margin:0 auto;padding:22px 22px 56px;}}
  .back-link{{display:inline-block;font-size:13px;margin:0 0 14px;}}
  .course-header{{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;border-bottom:1px solid var(--border-light);padding-bottom:16px;margin-bottom:20px;}}
  .course-header h1{{font-size:23px;font-weight:700;margin:0 0 4px;}}
  .course-header .lead{{color:var(--muted);font-size:13.5px;max-width:660px;}}
  .cti-logo{{height:34px;width:auto;display:block;opacity:.9;}}
  .cti-logo-fallback{{display:none;font-size:11px;color:var(--muted);font-weight:700;letter-spacing:.3px;text-align:right;line-height:1.2;}}
  .module{{border:1px solid var(--border);border-radius:4px;margin-bottom:20px;overflow:hidden;}}
  details.module > summary{{list-style:none;cursor:pointer;}}
  details.module > summary::-webkit-details-marker{{display:none;}}
  .module-head{{background:var(--modhead);border-bottom:1px solid var(--border);padding:11px 14px;display:flex;align-items:center;gap:12px;}}
  details.module:not([open]) > .module-head{{border-bottom:none;}}
  .module-head .name{{font-size:15px;font-weight:700;color:var(--text);flex:1;}}
  .module-head .tag{{font-size:12px;color:var(--muted);white-space:nowrap;}}
  .module-head .chev{{display:inline-block;font-size:11px;color:var(--muted);transition:transform .15s ease;flex-shrink:0;}}
  details.module[open] > .module-head .chev{{transform:rotate(90deg);}}
  .module-head:hover{{background:#EFEFEF;}}
  .module.module--muted{{opacity:.68;}}
  .module.module--muted .module-head{{background:#ECECEE;}}
  .module.module--muted .module-head:hover{{background:#E4E4E6;}}
  .module.module--muted .name,
  .module.module--muted .tag{{color:#7C8A93;}}
  .module-head .not-ready{{display:none;font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#5F6B73;background:#D8DCDF;border-radius:3px;padding:1px 7px;}}
  .module.module--muted .module-head .not-ready{{display:inline-block;}}
  .goal{{background:var(--goal-bg);border-left:4px solid var(--goal-border);padding:11px 14px;}}
  .goal .label{{font-size:10.5px;font-weight:700;letter-spacing:.7px;text-transform:uppercase;color:var(--blue);margin-bottom:3px;}}
  .goal .text{{font-size:14px;color:var(--text);}}
  .goal-list{{margin:4px 0 0 0;padding-left:18px;}}
  .prereq{{padding:8px 14px 4px;color:var(--muted);font-size:12.5px;display:flex;gap:7px;align-items:flex-start;border-bottom:1px solid var(--border-light);}}
  .prereq svg{{width:14px;height:14px;flex:0 0 14px;margin-top:2px;}}
  .items{{padding:2px 0 4px;}}
  .item{{display:flex;gap:11px;padding:11px 14px 11px 26px;border-bottom:1px solid var(--border-light);align-items:flex-start;}}
  .item:last-child{{border-bottom:none;}}
  .item .ico{{flex:0 0 18px;margin-top:1px;color:var(--muted);}}
  .item .ico svg{{width:18px;height:18px;display:block;}}
  .item .body{{flex:1;min-width:0;}}
  .item .title{{font-size:14.5px;font-weight:600;}}
  .item .meta{{color:var(--muted);font-size:12px;margin-top:2px;}}
  .progress-status{{font-size:12px;color:var(--muted);margin:-10px 0 14px;}}
  .progress-check{{margin-left:auto;display:inline-flex;align-items:center;gap:6px;color:var(--muted);font-size:11.5px;white-space:nowrap;padding-left:10px;}}
  .progress-box{{width:18px;height:18px;border:1.5px solid var(--border);border-radius:3px;background:#fff;display:inline-flex;align-items:center;justify-content:center;}}
  .progress-label{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;}}
  .item[data-progress-state="loading"] .progress-box{{background:linear-gradient(90deg,#fff,#F2F4F5,#fff);}}
  .item[data-progress-state="complete"] .progress-box{{border-color:var(--check);background:var(--check);color:#fff;}}
  .item[data-progress-state="complete"] .progress-box::after{{content:"";width:9px;height:5px;border-left:2px solid #fff;border-bottom:2px solid #fff;transform:rotate(-45deg);margin-top:-2px;}}
  .item[data-progress-state="complete"] .title a{{color:#24543A;}}
  .group-label{{padding:10px 14px 4px;font-size:10.5px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--muted);background:#FAFBFC;border-bottom:1px solid var(--border-light);}}
  .item.selfcheck{{background:var(--check-bg);}}
  .item.selfcheck .ico{{color:var(--check);}}
  .selfcheck .badge{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:#fff;background:var(--check);border-radius:3px;padding:1px 6px;margin-left:8px;vertical-align:middle;}}
  .selfcheck .badge.optional{{background:#7C8A93;}}
  .selfcheck .verify{{margin-top:5px;font-size:12.5px;color:#3d5346;display:flex;gap:6px;align-items:flex-start;}}
  .selfcheck .verify svg{{width:14px;height:14px;flex:0 0 14px;margin-top:2px;}}
  .page-footer{{margin-top:30px;padding-top:16px;border-top:1px solid var(--border-light);display:flex;align-items:center;gap:10px;color:var(--muted);font-size:11.5px;}}
  .page-footer img{{height:20px;opacity:.55;}}
</style>
</head>
<body>
  <div class="page">
    {back}
    <div class="course-header">
      <div>
        <h1>{html_lib.escape(course_meta["title"])}</h1>
        <div class="lead">{html_lib.escape(course_meta["lead"])}</div>
      </div>
      <div>
        <img class="cti-logo" src="{CTI_LOGO_URL}" alt="Computing Talent Initiative" onerror="this.style.display='none';this.nextElementSibling.style.display='block';">
        <div class="cti-logo-fallback">Computing Talent<br>Initiative</div>
      </div>
    </div>
    <div class="progress-status" id="progress-status" hidden></div>
    {modules_html}
    <footer class="page-footer">
      <img src="{CTI_LOGO_URL}" alt="" onerror="this.style.display='none'">
      <span>{html_lib.escape(course_meta["footer"])}</span>
    </footer>
  </div>
  <script>
    (function() {{
      var ctx = new URLSearchParams(location.search).get('context')
        || (window.self !== window.top ? 'canvas' : 'web');
      document.querySelectorAll('a[data-canvas-href]').forEach(function(a) {{
        if (ctx === 'canvas') {{
          a.href = a.getAttribute('data-canvas-href');
        }} else {{
          try {{
            var u = new URL(a.getAttribute('href'), location.href);
            u.searchParams.set('context', 'web');
            a.href = u.pathname + u.search + u.hash;
          }} catch (e) {{ }}
        }}
      }});
      document.querySelectorAll('a[data-keep-context]').forEach(function(a) {{
        try {{
          var u = new URL(a.getAttribute('href'), location.href);
          u.searchParams.set('context', ctx === 'canvas' ? 'canvas' : 'web');
          a.href = u.pathname + u.search + u.hash;
        }} catch (e) {{ }}
      }});

      var progressEndpoint = {progress_endpoint_json};
      var courseKey = {course_key_json};
      var statusEl = document.getElementById('progress-status');
      function setStatus(text, visible) {{
        if (!statusEl) return;
        statusEl.textContent = text || '';
        statusEl.hidden = !visible;
      }}
      function setItemState(item, state, label) {{
        item.setAttribute('data-progress-state', state);
        var check = item.querySelector('.progress-check');
        var labelEl = item.querySelector('.progress-label');
        if (check) {{
          check.setAttribute('aria-label', label);
          check.setAttribute('title', label);
        }}
        if (labelEl) labelEl.textContent = label;
      }}
      function progressToken() {{
        var params = new URLSearchParams(location.search);
        var fromQuery = params.get('progress_token');
        var hash = new URLSearchParams((location.hash || '').replace(/^#/, ''));
        var fromHash = hash.get('progress_token');
        var token = fromHash || fromQuery || sessionStorage.getItem('canvas_progress_token');
        if (fromHash || fromQuery) {{
          try {{
            sessionStorage.setItem('canvas_progress_token', token);
            params.delete('progress_token');
            hash.delete('progress_token');
            var next = location.pathname + (params.toString() ? '?' + params.toString() : '') + (hash.toString() ? '#' + hash.toString() : '');
            history.replaceState(null, '', next);
          }} catch (e) {{ }}
        }}
        return token;
      }}
      function loadProgress() {{
        var items = Array.prototype.slice.call(document.querySelectorAll('.item[data-progress-id]'));
        if (!items.length) return;
        if (ctx !== 'canvas') {{
          items.forEach(function(item) {{ setItemState(item, 'unavailable', 'Progress available in Canvas'); }});
          return;
        }}
        var token = progressToken();
        if (!token) {{
          setStatus('Progress is unavailable until this page is opened through Canvas.', true);
          items.forEach(function(item) {{ setItemState(item, 'unavailable', 'Progress unavailable'); }});
          return;
        }}
        items.forEach(function(item) {{ setItemState(item, 'loading', 'Checking progress'); }});
        setStatus('Checking Canvas progress...', true);
        var url = new URL(progressEndpoint, location.href);
        if (courseKey) url.searchParams.set('course', courseKey);
        fetch(url.href, {{ headers: {{ Authorization: 'Bearer ' + token }} }})
          .then(function(response) {{
            if (!response.ok) throw new Error('Progress request failed');
            return response.json();
          }})
          .then(function(data) {{
            var byModuleItem = {{}};
            (data.items || []).forEach(function(item) {{
              if (item.moduleItemId != null) byModuleItem[String(item.moduleItemId)] = item;
            }});
            var completeCount = 0;
            items.forEach(function(row) {{
              var moduleItemId = row.getAttribute('data-canvas-module-item-id');
              var progress = moduleItemId ? byModuleItem[String(moduleItemId)] : null;
              if (progress && progress.completed) {{
                completeCount += 1;
                setItemState(row, 'complete', 'Completed in Canvas');
              }} else if (progress) {{
                setItemState(row, 'incomplete', 'Not completed in Canvas');
              }} else {{
                setItemState(row, 'unavailable', 'Progress unavailable for this item');
              }}
            }});
            setStatus(completeCount + ' of ' + items.length + ' items completed in Canvas.', true);
          }})
          .catch(function() {{
            setStatus('Canvas progress could not be loaded right now.', true);
            items.forEach(function(item) {{ setItemState(item, 'unavailable', 'Progress unavailable'); }});
          }});
      }}
      loadProgress();
    }})();
  </script>
</body>
</html>
"""


def _render_career_sprint_index(
    output_dir: Path,
    manifest_path: Path,
    manifest: dict,
    course_key: str,
    sprint: int,
    sprint_items: list[tuple[Path, dict]],
    homepage: dict | None,
    state: dict | None,
) -> dict:
    course_dir = course_dir_for_manifest(manifest_path)
    course_meta = _course_metadata(course_dir, course_key, homepage)
    module_config = _module_config_by_sprint(homepage).get(sprint, {})
    module_html = _render_career_module(
        sprint,
        sprint_items,
        module_config,
        manifest_path,
        manifest,
        state,
        first=True,
        force_open=True,
    )
    document = _career_homepage_document(
        course_meta,
        module_html,
        title_suffix=f"Sprint {sprint}",
        back_href="home.html?context=web",
        progress_endpoint=hosted_config_from_manifest(manifest).progress_endpoint,
    )
    path = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key / f"sprint-{sprint}.html"
    changed, digest = _write_if_changed(path, document)
    return {"path": str(path), "changed": changed, "hash": digest}


def _render_career_course_index(
    output_dir: Path,
    manifest_path: Path,
    manifest: dict,
    course_key: str,
    items_by_sprint: dict[int, list[tuple[Path, dict]]],
    homepage: dict | None,
    state: dict | None,
) -> dict:
    course_dir = course_dir_for_manifest(manifest_path)
    course_meta = _course_metadata(course_dir, course_key, homepage)
    configs = _module_config_by_sprint(homepage)
    modules = []
    for index, sprint in enumerate(sorted(items_by_sprint), start=1):
        modules.append(
            _render_career_module(
                sprint,
                items_by_sprint[sprint],
                configs.get(sprint, {}),
                manifest_path,
                manifest,
                state,
                first=index == 1,
            )
        )
    document = _career_homepage_document(
        course_meta,
        "\n".join(modules),
        progress_endpoint=hosted_config_from_manifest(manifest).progress_endpoint,
    )
    course_dir_out = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key
    index_changed, index_digest = _write_if_changed(course_dir_out / "index.html", document)
    home_changed, home_digest = _write_if_changed(course_dir_out / "home.html", document)
    return {
        "path": str(course_dir_out / "index.html"),
        "changed": index_changed or home_changed,
        "hash": index_digest,
        "aliases": [
            {"path": str(course_dir_out / "home.html"), "changed": home_changed, "hash": home_digest}
        ],
    }


def _progress_map_item(
    md_path: Path,
    manifest_path: Path,
    manifest: dict,
    frontmatter: dict,
    state: dict | None,
) -> dict:
    repo_root = course_dir_for_manifest(manifest_path).parent
    rel_path = str(md_path.resolve().relative_to(repo_root.resolve()))
    state_entry = _state_entry_for_artifact(md_path, manifest_path, frontmatter, state or manifest)
    return {
        "artifactId": _artifact_progress_id(md_path, manifest_path, frontmatter),
        "localPath": rel_path,
        "slug": frontmatter.get("slug"),
        "title": frontmatter.get("title"),
        "type": frontmatter.get("type"),
        "sprint": frontmatter.get("sprint"),
        "canvasType": state_entry.get("canvas_type") or frontmatter.get("type"),
        "canvasId": state_entry.get("canvas_id"),
        "canvasPageUrl": state_entry.get("canvas_page_url"),
        "canvasModuleId": state_entry.get("canvas_module_id"),
        "canvasModuleItemId": state_entry.get("canvas_module_item_id"),
        "completionRequirement": state_entry.get("completion_requirement"),
    }


def _render_progress_map(
    output_dir: Path,
    manifest_path: Path,
    manifest: dict,
    course_key: str,
    items: list[tuple[Path, dict]],
    state: dict | None,
) -> dict:
    config = hosted_config_from_manifest(manifest)
    payload = {
        "courseKey": course_key,
        "canvasCourseId": manifest.get("instance", {}).get("course_id"),
        "progressEndpoint": config.progress_endpoint,
        "items": [
            _progress_map_item(md_path, manifest_path, manifest, frontmatter, state)
            for md_path, frontmatter in items
        ],
    }
    path = output_dir / config.path_prefix / course_key / "progress-map.json"
    changed, digest = _write_if_changed(
        path,
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
    )
    return {"path": str(path), "changed": changed, "hash": digest}


def _index_document(
    title: str,
    meta: str,
    sections: str,
    *,
    back_href: str | None = None,
) -> str:
    back = ""
    if back_href:
        back = f'    <a class="back-link" href="{back_href}" data-keep-context>&larr; Back</a>\n'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html_lib.escape(title)}</title>
  <style>
    :root {{
      --bg: #fafafa;
      --surface: #ffffff;
      --text: #1a1a1a;
      --muted: #555;
      --border: #e0e0e0;
      --accent: #2c5282;
      --accent-light: #ebf4ff;
      --radius: 8px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      padding: 20px 16px;
      font: 16px/1.65 -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
      color: var(--text);
      background: var(--bg);
    }}
    .activity {{ max-width: 760px; margin: 0 auto; }}
    .meta {{
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin: 0 0 6px;
    }}
    h1 {{ font-size: 22px; font-weight: 700; margin: 0 0 18px; line-height: 1.3; }}
    section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 16px 20px;
      margin: 0 0 16px;
    }}
    section h2 {{ margin: 0 0 10px; font-size: 17px; font-weight: 700; }}
    a {{ color: var(--accent); word-break: break-word; }}
    li {{ margin-bottom: 6px; }}
    footer {{ text-align: center; margin: 28px 0 8px; opacity: 0.55; }}
    footer img {{ height: 22px; }}
    .back-link {{
      display: none;
      font-size: 13px;
      color: var(--accent);
      text-decoration: none;
      margin: 0 0 12px;
    }}
    .ctx-web .back-link {{ display: inline-block; }}
  </style>
  <script>
    (function() {{
      var ctx = new URLSearchParams(location.search).get('context')
        || (window.self !== window.top ? 'canvas' : 'web');
      if (ctx !== 'canvas') {{
        document.documentElement.classList.add('ctx-web');
      }}
      document.addEventListener('DOMContentLoaded', function() {{
        document.querySelectorAll('a[data-keep-context]').forEach(function(a) {{
          try {{
            var u = new URL(a.getAttribute('href'), location.href);
            if (!u.searchParams.has('context')) {{
              u.searchParams.set('context', ctx);
              a.href = u.href;
            }}
          }} catch (e) {{ }}
        }});
      }});
    }})();
  </script>
</head>
<body>
  <div class="activity">
{back}    <p class="meta">{html_lib.escape(meta)}</p>
    <h1>{html_lib.escape(title)}</h1>
    {sections}
    <footer><img src="{CTI_LOGO_URL}" alt="Computing Talent Initiative" onerror="this.style.display='none'"></footer>
  </div>
</body>
</html>
"""


def _render_sprint_index(
    output_dir: Path,
    manifest: dict,
    course_key: str,
    sprint: int,
    items: list[tuple[Path, dict]],
) -> dict:
    links = []
    for _path, fm in items:
        href = f"{_artifact_course_relative_path(fm)}?context=web"
        label = html_lib.escape(f"{fm['title']} ({_type_label(fm['type'])})")
        links.append(f'<li><a href="{href}" data-keep-context>{label}</a></li>')
    sections = "<section>\n<h2>Module activities</h2>\n<ul>\n" + "\n".join(links) + "\n</ul>\n</section>"
    document = _index_document(
        f"Sprint {sprint}",
        f"{course_key} · Sprint {sprint}",
        sections,
        back_href="home.html?context=web",
    )
    path = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key / f"sprint-{sprint}.html"
    changed, digest = _write_if_changed(path, document)
    return {"path": str(path), "changed": changed, "hash": digest}


def _render_course_index(
    output_dir: Path,
    manifest: dict,
    course_key: str,
    items_by_sprint: dict[int, list[tuple[Path, dict]]],
) -> dict:
    sections = []
    for sprint in sorted(items_by_sprint):
        module = html_lib.escape(items_by_sprint[sprint][0][1].get("module", f"Sprint {sprint}"))
        href = f"sprint-{sprint}.html?context=web"
        sections.append(
            "<section>\n"
            f"<h2>{module}</h2>\n"
            f'<p><a href="{href}" data-keep-context>Open Sprint {sprint}</a></p>\n'
            "</section>"
        )
    document = _index_document(
        f"{course_key} hosted course pages",
        f"{course_key} · Hosted HTML",
        "\n".join(sections),
    )
    course_dir = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key
    index_changed, index_digest = _write_if_changed(course_dir / "index.html", document)
    home_changed, home_digest = _write_if_changed(course_dir / "home.html", document)
    return {
        "path": str(course_dir / "index.html"),
        "changed": index_changed or home_changed,
        "hash": index_digest,
        "aliases": [
            {"path": str(course_dir / "home.html"), "changed": home_changed, "hash": home_digest}
        ],
    }


def render_hosted_files(
    manifest_path: Path,
    output_dir: Path,
    files: list[Path],
    *,
    manifest: dict | None = None,
    state: dict | None = None,
) -> dict:
    manifest_data = manifest or load_json(manifest_path)
    course_key = course_dir_for_manifest(manifest_path).name
    course_dir = course_dir_for_manifest(manifest_path)
    index_files = discover_artifact_files(manifest_path)
    results = []
    for md_path in files:
        errors = validate_artifact(md_path)
        if errors:
            raise ValueError("; ".join(errors))
        fm, _body = parse_frontmatter(md_path)
        if fm["type"] == "module_header":
            continue
        results.append(
            render_hosted_artifact(
                md_path,
                manifest_path,
                output_dir,
                manifest=manifest_data,
                state=state or manifest_data,
            )
        )

    for md_path in index_files:
        errors = validate_artifact(md_path)
        if errors:
            raise ValueError("; ".join(errors))

    homepage = _load_homepage_metadata(course_dir)
    if homepage is not None:
        homepage_errors = validate_homepage_metadata(course_dir)
        if homepage_errors:
            raise ValueError("; ".join(homepage_errors))

    items = _load_artifact_items(index_files)
    items_by_sprint: dict[int, list[tuple[Path, dict]]] = {}
    for item in items:
        sprint = int(item[1]["sprint"])
        items_by_sprint.setdefault(sprint, []).append(item)

    indexes = []
    progress_map = None
    for sprint, sprint_items in sorted(items_by_sprint.items()):
        indexes.append(
            _render_career_sprint_index(
                output_dir,
                manifest_path,
                manifest_data,
                course_key,
                sprint,
                sprint_items,
                homepage,
                state or manifest_data,
            )
        )
    if items_by_sprint:
        indexes.append(
            _render_career_course_index(
                output_dir,
                manifest_path,
                manifest_data,
                course_key,
                items_by_sprint,
                homepage,
                state or manifest_data,
            )
        )
        progress_map = _render_progress_map(
            output_dir,
            manifest_path,
            manifest_data,
            course_key,
            items,
            state or manifest_data,
        )

    result = {"rendered": results, "indexes": indexes}
    if progress_map is not None:
        result["progress_map"] = progress_map
    return result


def discover_artifact_files(manifest_path: Path, sprint: int | None = None) -> list[Path]:
    course_dir = course_dir_for_manifest(manifest_path)
    pattern = f"sprints/sprint-{sprint}/*.md" if sprint is not None else "sprints/sprint-*/*.md"
    return sorted(course_dir.glob(pattern))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--file", type=Path, action="append")
    parser.add_argument("--sprint", type=int)
    args = parser.parse_args()

    try:
        files = args.file if args.file else discover_artifact_files(args.manifest, args.sprint)
        result = render_hosted_files(args.manifest.resolve(), args.output_dir.resolve(), [p.resolve() for p in files])
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:  # noqa: BLE001 - compact CLI failure
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

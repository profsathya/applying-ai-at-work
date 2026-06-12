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

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import course_dir_for_manifest, derive_artifact_id, load_json


DEFAULT_BASE_URL = "https://profsathya.github.io/Common-Curriculum/deanza"
DEFAULT_PATH_PREFIX = "deanza"
CTI_LOGO_URL = (
    "https://computingtalentinitiative.org/wp-content/uploads/2026/06/"
    "New._CTI_Logo_RGB-1.png"
)


@dataclass(frozen=True)
class HostedConfig:
    enabled: bool
    base_url: str
    path_prefix: str


def hosted_config_from_manifest(manifest: dict) -> HostedConfig:
    config = manifest.get("hosted_html") or {}
    return HostedConfig(
        enabled=bool(config.get("enabled", False)),
        base_url=str(config.get("base_url") or DEFAULT_BASE_URL).rstrip("/"),
        path_prefix=str(config.get("path_prefix") or DEFAULT_PATH_PREFIX).strip("/"),
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
    sprint = int(fm["sprint"])
    slug = fm["slug"]
    hosted_path = f"{course_key}/sprint-{sprint}/{slug}.html"
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


def _canvas_item_url(manifest: dict, frontmatter: dict, entry: dict) -> str | None:
    instance = manifest.get("instance", {})
    base_url = str(instance.get("base_url") or "").rstrip("/")
    course_id = instance.get("course_id")
    if not base_url or not course_id:
        return None
    artifact_type = frontmatter["type"]
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
    back_href = "index.html?context=web"
    if "/" in str(hosted_info["hosted_path"]):
        back_href = "../index.html?context=web"

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
        href = f"{fm['slug']}.html?context=web"
        label = html_lib.escape(f"{fm['title']} ({_type_label(fm['type'])})")
        links.append(f'<li><a href="{href}" data-keep-context>{label}</a></li>')
    sections = "<section>\n<h2>Module activities</h2>\n<ul>\n" + "\n".join(links) + "\n</ul>\n</section>"
    document = _index_document(
        f"Sprint {sprint}",
        f"{course_key} · Sprint {sprint}",
        sections,
        back_href="../index.html?context=web",
    )
    path = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key / f"sprint-{sprint}" / "index.html"
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
        href = f"sprint-{sprint}/index.html?context=web"
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
    path = output_dir / hosted_config_from_manifest(manifest).path_prefix / course_key / "index.html"
    changed, digest = _write_if_changed(path, document)
    return {"path": str(path), "changed": changed, "hash": digest}


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

    items = _load_artifact_items(files)
    items_by_sprint: dict[int, list[tuple[Path, dict]]] = {}
    for item in items:
        sprint = int(item[1]["sprint"])
        items_by_sprint.setdefault(sprint, []).append(item)

    indexes = []
    for sprint, sprint_items in sorted(items_by_sprint.items()):
        indexes.append(_render_sprint_index(output_dir, manifest_data, course_key, sprint, sprint_items))
    if items_by_sprint:
        indexes.append(_render_course_index(output_dir, manifest_data, course_key, items_by_sprint))

    return {"rendered": results, "indexes": indexes}


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

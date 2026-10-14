"""Publish a credential-free adapter to an existing course's live hosted content.

This does not publish Canvas objects or store credentials. Native course IDs are
explicit deployment mappings; unknown IDs and pages fail closed in the browser.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path, PurePosixPath
from urllib.parse import urlencode, urlsplit


ASSET = Path(__file__).parent / "assets" / "course-mirror.js"


def validate_config(config: dict) -> dict:
    required = {"sourceCanvasUrl", "destinationCanvasUrl", "sharedBaseUrl",
                "mirrorBaseUrl", "pages", "mapping"}
    if set(config) != required:
        raise ValueError("Mirror configuration must contain only public URLs, pages, and ID mappings")
    origins = []
    for key in ("sourceCanvasUrl", "destinationCanvasUrl", "sharedBaseUrl", "mirrorBaseUrl"):
        parsed = urlsplit(config[key])
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise ValueError("Mirror URLs must be public HTTPS URLs without credentials or query parameters")
        origins.append((parsed.scheme, parsed.netloc))
    if origins[2] != origins[3]:
        raise ValueError("Shared content and its adapter must have the same origin")
    for key in ("sourceCanvasUrl", "destinationCanvasUrl"):
        parts = urlsplit(config[key]).path.strip("/").split("/")
        if len(parts) != 2 or parts[0] != "courses" or not parts[1].isdigit():
            raise ValueError("Canvas URLs must identify one course")
    if not config["sharedBaseUrl"].endswith("/") or not config["mirrorBaseUrl"].endswith("/"):
        raise ValueError("Hosted base URLs must end with a slash")
    if not config["pages"] or len(config["pages"]) != len(set(config["pages"])):
        raise ValueError("Mirror pages must be a nonempty unique allowlist")
    for value in config["pages"]:
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or str(path) != value or not value.endswith(".html"):
            raise ValueError("Mirror pages must be normalized relative HTML paths")
    if set(config["mapping"]) != {"modules", "module_items", "assignments", "discussion_topics", "page_urls"}:
        raise ValueError("Unexpected native mapping category")
    for kind, rows in config["mapping"].items():
        if not isinstance(rows, dict) or not rows:
            raise ValueError("Native mapping categories cannot be empty")
        for source, destination in rows.items():
            if kind == "page_urls":
                if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in source + str(destination)):
                    raise ValueError("Invalid Canvas page slug")
            elif not source.isdigit() or not isinstance(destination, int) or destination <= 0:
                raise ValueError("Native IDs must be positive integers")
    return config


def mirror_url(config: dict, page: str, context: str = "canvas") -> str:
    if page not in config["pages"] or context not in ("canvas", "web"):
        raise ValueError("Unknown mirror page or context")
    return config["mirrorBaseUrl"] + "?" + urlencode({"page": page, "context": context})


def render(config: dict, output: Path, *, legacy_dir: Path | None = None) -> list[Path]:
    validate_config(config)
    output.mkdir(parents=True, exist_ok=True)
    entry = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Course content</title></head><body><p id="mirror-status" role="status">Loading course content...</p>
<noscript>This course page requires JavaScript to load its current content.</noscript>
<script src="course-mirror.js"></script></body></html>
"""
    files = []
    for name, text in (("index.html", entry), ("config.json", json.dumps(config, indent=2, sort_keys=True) + "\n"),
                       ("course-mirror.js", ASSET.read_text())):
        path = output / name
        path.write_text(text)
        files.append(path)
    if legacy_dir:
        for page in config["pages"]:
            target = mirror_url(config, page, "web")
            # Keep old bookmarks, but never retain a second copy of teaching text.
            script_target = json.dumps(target).replace("<", "\\u003c")
            text = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Course content</title></head>'
                    '<body><p><a href="' + html.escape(target, quote=True) + '">Open current course content</a></p>'
                    '<script>var u = new URL(' + script_target + ');'
                    'var p = new URLSearchParams(location.search);'
                    'u.searchParams.set("context", p.get("context") === "canvas" ? "canvas" : "web");'
                    'u.hash = location.hash; location.replace(u.href);</script></body></html>\n')
            path = legacy_dir / page
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            files.append(path)
        for name in ("deanza46601-config.json", "progress-map.json"):
            path = legacy_dir / name
            if not path.exists():
                continue
            metadata = json.loads(path.read_text())
            metadata.update(hostedBaseUrl=config["mirrorBaseUrl"].rstrip("/"),
                            sharedContentBaseUrl=config["sharedBaseUrl"], contentMode="live_shared_mirror",
                            sourceRelease={"mode": "live_shared_content", "sourceHostedBaseUrl": config["sharedBaseUrl"]})
            path.write_text(json.dumps(metadata, indent=2) + "\n")
            files.append(path)
        guidance = legacy_dir / "course-guidance.txt"
        if guidance.exists():
            guidance.write_text("The course now uses live shared course guidance.\n"
                                "Use the Course source linked from Set up your AI Dojo:\n"
                                + mirror_url(config, "activities/set-up-your-ai-dojo-v2.html", "web") + "\n")
            files.append(guidance)
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--legacy-dir", type=Path)
    args = parser.parse_args()
    files = render(json.loads(args.config.read_text()), args.output, legacy_dir=args.legacy_dir)
    print(json.dumps({"files": len(files), "canvas_writes": 0}))


if __name__ == "__main__":
    main()

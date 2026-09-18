"""Validate learner-facing links after the production Markdown render.

This audit is intentionally deterministic and offline. It verifies the link
contract that the repository controls: safe destinations, absence of obvious
placeholders, valid same-page fragments, and top-level navigation for links
that would otherwise remain trapped inside Canvas's hosted iframe.
"""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.hosted_html import (
    discover_artifact_files,
    link_requires_top_level_navigation,
    markdown_body_to_html,
)
from canvas_sync.schema import parse_frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
ALLOWED_SCHEMES = {"", "http", "https", "mailto", "tel"}
PLACEHOLDER_RE = re.compile(
    r"(?:example\.com|placeholder|replace[-_ ]?me|doc[-_ ]?id|"
    r"link[-_ ]?to[-_ ]?be[-_ ]?supplied|your[-_ ]?(?:url|link))",
    re.IGNORECASE,
)


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a":
            self.links.append(values)


def audit_rendered_html(rendered: str, source: str) -> list[str]:
    parser = _LinkParser()
    parser.feed(rendered)
    errors: list[str] = []
    for index, link in enumerate(parser.links, start=1):
        href = str(link.get("href") or "").strip()
        label = f"{source}: link {index}"
        if not href:
            errors.append(f"{label} has no href")
            continue
        if PLACEHOLDER_RE.search(href):
            errors.append(f"{label} contains a placeholder URL: {href}")
        parsed = urlsplit(href)
        scheme = parsed.scheme.lower()
        if scheme not in ALLOWED_SCHEMES:
            errors.append(f"{label} uses unsupported URL scheme {scheme!r}: {href}")
        if link_requires_top_level_navigation(href) and link.get("target") != "_top":
            errors.append(f"{label} does not escape the Canvas iframe: {href}")
        if href.startswith("#") and href[1:] not in parser.ids:
            errors.append(f"{label} points to missing fragment {href}")
    return errors


def audit_artifact(path: Path) -> tuple[int, list[str]]:
    _frontmatter, body = parse_frontmatter(path)
    rendered = markdown_body_to_html(body)
    parser = _LinkParser()
    parser.feed(rendered)
    return len(parser.links), audit_rendered_html(rendered, str(path))


def manifest_paths(root: Path, requested: list[Path] | None) -> list[Path]:
    if requested:
        return [path.resolve() for path in requested]
    return sorted(root.glob("*/manifests/production.json"))


def run(manifests: list[Path]) -> dict:
    artifacts: set[Path] = set()
    for manifest in manifests:
        artifacts.update(path.resolve() for path in discover_artifact_files(manifest))

    errors: list[str] = []
    link_count = 0
    for artifact in sorted(artifacts):
        count, artifact_errors = audit_artifact(artifact)
        link_count += count
        errors.extend(artifact_errors)
    return {
        "manifests": len(manifests),
        "artifacts": len(artifacts),
        "links": link_count,
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Audit all production manifests")
    group.add_argument("--manifest", action="append", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    manifests = manifest_paths(REPO_ROOT, args.manifest)
    report = run(manifests)
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(
            f"Link audit: {report['artifacts']} artifacts, {report['links']} links, "
            f"{len(report['errors'])} errors"
        )
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

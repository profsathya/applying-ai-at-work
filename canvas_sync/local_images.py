"""Resolve course-local raster illustrations for deterministic hosted output."""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class _Images(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.sources = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            source = dict(attrs).get('src', '')
            if source and source not in self.sources:
                self.sources.append(source)


def local_image_assets(md_path: Path, rendered: str) -> list[dict]:
    """Only relative assets/ images are copied; remote URLs keep their behavior.

    Content-addressed names make a changed image change the page hash as well.
    Each artifact owns its output assets so publish recovery can restore them.
    """
    parser = _Images()
    parser.feed(rendered)
    result = []
    root = (md_path.parent / 'assets').resolve()
    for source in parser.sources:
        url = urlsplit(source)
        if url.scheme or url.netloc or source.startswith('/'):
            continue
        path = (md_path.parent / unquote(url.path)).resolve()
        if not path.is_relative_to(root):
            raise ValueError(f'{md_path}: local image must be inside adjacent assets/: {source}')
        if path.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
            raise ValueError(f'{md_path}: unsupported local image format: {source}')
        if not path.is_file():
            raise ValueError(f'{md_path}: missing local image: {source}')
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        result.append({'source': source, 'path': path, 'hash': digest,
                       'url': f'assets/{md_path.stem}/{digest[:16]}{path.suffix.lower()}', 'payload': payload})
    return result

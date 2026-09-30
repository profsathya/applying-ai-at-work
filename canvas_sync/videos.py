"""Render explicit Markdown video blocks with native accessible controls."""
from __future__ import annotations

import html
import json
import re
from pathlib import PurePosixPath
from urllib.parse import unquote, urlsplit

VIDEO_BLOCK = re.compile(r'<pre><code class="(?:language-)?video">(.*?)</code></pre>', re.DOTALL)


def render_video_blocks(rendered: str) -> str:
    def replace(match):
        try:
            config = json.loads(html.unescape(match.group(1)))
        except json.JSONDecodeError as exc:
            raise ValueError('Video block must contain valid JSON') from exc
        if not isinstance(config, dict) or set(config) != {'src', 'title', 'captions'}:
            raise ValueError('Video block requires exactly src, title, and captions')
        if not isinstance(config['title'], str) or not config['title'].strip():
            raise ValueError('Video title must be nonempty text')
        for key, extension in [('src', '.mp4'), ('captions', '.vtt')]:
            value = config[key]
            if not isinstance(value, str):
                raise ValueError(f'Video {key} must be a local assets/ path')
            url = urlsplit(value)
            path = PurePosixPath(unquote(url.path))
            if (url.scheme or url.netloc or url.query or url.fragment
                    or not path.parts or path.parts[0] != 'assets'
                    or '..' in path.parts or path.suffix.lower() != extension):
                raise ValueError(f'Video {key} must be a local assets/ {extension} path')
        title, src, captions = (html.escape(config[k], quote=True) for k in ('title', 'src', 'captions'))
        return (f'<figure class="course-video">'
                f'<video controls preload="metadata" playsinline aria-label="{title}">'
                f'<source src="{src}" type="video/mp4">'
                f'<track kind="captions" src="{captions}" srclang="en" label="English" default>'
                f'Your browser cannot play this video. <a href="{src}" download>Download {title}</a>.'
                f'</video><figcaption>{title}. <a href="{src}" download>Download video</a></figcaption></figure>')
    return VIDEO_BLOCK.sub(replace, rendered)

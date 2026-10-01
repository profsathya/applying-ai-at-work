"""Shared visual foundation for Applying AI at Work hosted surfaces.

Embed at render time so individual releases are self-contained. Other courses
and the shared Common Curriculum activity engine retain their own themes.
"""
from pathlib import Path


def apply_course_styles(document: str, course_key: str) -> str:
    if course_key != "course1":
        return document
    marker = '<style data-course-theme="applying-ai-at-work">'
    if marker in document:
        return document
    if "</head>" not in document:
        raise ValueError("Course theme requires a complete HTML document")
    styles = (Path(__file__).parent / "assets" / "course-theme.css").read_text()
    return document.replace("</head>", f"{marker}\n{styles}</style>\n</head>", 1)

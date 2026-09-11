"""Compare editable source with the Canvas representation actually published."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path

from canvas_sync.hosted_html import (
    artifact_hosted_info,
    iframe_shell,
    markdown_body_to_html,
)
from canvas_sync.schema import parse_frontmatter


def html_to_markdown(html: str) -> str:
    import html2text

    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.unicode_snob = True
    converter.ignore_links = False
    converter.ignore_images = False
    converter.escape_snob = True
    return converter.handle(html or "").strip()


def canvas_body(state: dict) -> str:
    return state.get("description") or state.get("body") or state.get("message") or ""


def canvas_points(state: dict):
    return (state.get("assignment") or {}).get(
        "points_possible", state.get("points_possible")
    )


class IframeSources(HTMLParser):
    def __init__(self, html: str):
        super().__init__()
        self.sources = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "iframe":
            self.sources.append(dict(attrs).get("src"))


def comparable_questions(questions: list[dict], *, canvas: bool) -> list[dict]:
    result = []
    for question in questions:
        qtype = (
            question.get("question_type", "").removesuffix("_question")
            if canvas
            else question.get("type")
        )
        item = {
            "type": qtype,
            "prompt": html_to_markdown(question.get("question_text", ""))
            if canvas
            else html_to_markdown(question.get("prompt", "")),
            "points": question.get("points_possible", 1)
            if canvas
            else question.get("points", 1),
        }
        if qtype in ("multiple_choice", "true_false", "short_answer"):
            item["answers"] = [
                {
                    "text": a.get("text", a.get("answer_text", "")),
                    "correct": (a.get("weight", a.get("answer_weight", 0)) or 0) > 0
                    if canvas
                    else bool(a.get("correct")),
                }
                for a in (question.get("answers") or [])
            ]
        result.append(item)
    return result


def compute_drift(
    md_path: Path,
    live: dict,
    atype: str,
    *,
    manifest_path: Path | None = None,
    manifest: dict | None = None,
) -> dict:
    fm, body = parse_frontmatter(md_path)
    expected_html = markdown_body_to_html(body)
    hosted = False
    if manifest_path is not None and manifest is not None:
        info = artifact_hosted_info(md_path, manifest_path, manifest, fm)
        hosted = info["enabled"] and atype != "module_header"
        if hosted:
            expected_html = iframe_shell(info["hosted_url"], fm["title"])
    actual_html = canvas_body(live)
    expected_md = html_to_markdown(expected_html)
    actual_md = html_to_markdown(actual_html)
    result = {}
    title = live.get("name") or live.get("title")
    if title != fm.get("title"):
        result["title"] = {"local": fm.get("title"), "canvas": title}
    if expected_md != actual_md or (
        hosted
        and IframeSources(expected_html).sources != IframeSources(actual_html).sources
    ):
        result["body"] = {
            "local_chars": len(expected_md),
            "canvas_chars": len(actual_md),
            "local_preview": expected_md[:200],
            "canvas_preview": actual_md[:200],
        }
    if atype in ("assignment", "quiz", "discussion") and canvas_points(live) != fm.get(
        "points"
    ):
        result["points"] = {"local": fm.get("points"), "canvas": canvas_points(live)}
    if "published" in live and live["published"] != fm.get("publish", True):
        result["publish"] = {
            "local": fm.get("publish", True),
            "canvas": live["published"],
        }
    due_state = live.get("assignment") or live
    if atype in ("assignment", "quiz", "discussion") and "due_at" in due_state:
        if due_state["due_at"] != fm.get("due"):
            result["due"] = {"local": fm.get("due"), "canvas": due_state["due_at"]}
    setting_state = live.get("assignment") or live
    for key in ("quiz_type", "allowed_attempts", "grading_type", "omit_from_final_grade"):
        if key in fm:
            actual = live.get(key) if key in ("quiz_type", "allowed_attempts") else setting_state.get(key)
            if actual != fm[key]:
                result[key] = {"local": fm[key], "canvas": actual}
    if atype == "quiz" and "questions" in live:
        if comparable_questions(
            fm.get("questions", []), canvas=False
        ) != comparable_questions(live["questions"], canvas=True):
            result["questions"] = {
                "reason": "Native quiz questions differ; explicit question import is required"
            }
    return result


def hosted_canvas_drift(md_path, manifest_path, manifest, canvas_state, atype):
    return compute_drift(
        md_path, canvas_state, atype, manifest_path=manifest_path, manifest=manifest
    )

"""
Push one MD artifact to canvas.

Reads the MD file, extracts frontmatter, checks manifest for an existing
canvas_id, then either creates or updates the artifact via the Canvas API.
Writes canvas_id and canvas_module_id back to the manifest atomically.

Usage:
  python canvas_sync/push.py --file <md_path> --manifest <manifest_path>

Exit codes:
  0 = success (prints JSON to stdout with canvas_id, canvas_module_id, action)
  1 = hard failure
  2 = validation failure
  3 = canvas API error
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import fcntl
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError, resolve_or_create_module
from canvas_sync.schema import parse_frontmatter, validate_artifact


def md_body_to_canvas_html(body: str) -> str:
    """
    Convert canvas-agnostic markdown to canvas-compatible HTML.

    Canvas accepts HTML in assignment descriptions, page bodies, discussion
    messages, and quiz descriptions. We use the 'markdown' library with safe
    defaults.
    """
    import markdown

    return markdown.markdown(
        body,
        extensions=["extra", "sane_lists", "smarty", "toc"],
        output_format="html5",
    )


def load_manifest(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with open(path) as f:
        return json.load(f)


def save_manifest(path: Path, manifest: dict) -> None:
    # Atomic write via temp file
    tmp = path.with_suffix(".json.tmp")
    with open(tmp, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


@contextmanager
def manifest_lock(path: Path):
    """Serialize manifest reads/writes across concurrent push processes."""
    lock_path = path.with_suffix(path.suffix + ".lock")
    with open(lock_path, "w") as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def course_dir_for_manifest(manifest_path: Path) -> Path:
    if manifest_path.parent.name != "manifests":
        raise ValueError(
            f"Manifest must live under <course>/manifests/: {manifest_path}"
        )
    return manifest_path.parent.parent


def validate_artifact_manifest_pair(md_path: Path, manifest_path: Path) -> None:
    course_dir = course_dir_for_manifest(manifest_path)
    sprint_dir = course_dir / "sprints"
    try:
        md_path.relative_to(sprint_dir)
    except ValueError as exc:
        raise ValueError(
            f"Artifact {md_path} must live under {sprint_dir} for manifest {manifest_path}"
        ) from exc


CANVAS_SUBMISSION_TYPE_MAP = {
    "text_entry": "online_text_entry",
    "file_upload": "online_upload",
    "online_quiz": "online_quiz",
    "discussion_topic": "discussion_topic",
    "none": "none",
    "on_paper": "on_paper",
    "media_recording": "media_recording",
    "online_url": "online_url",
    "external_tool": "external_tool",
}


def push_assignment(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    submission_type = fm.get("submission_type", "text_entry")
    canvas_submission_type = CANVAS_SUBMISSION_TYPE_MAP.get(submission_type, submission_type)
    payload = {
        "name": fm["title"],
        "description": html,
        "points_possible": fm.get("points"),
        "submission_types": [canvas_submission_type],
        "published": fm.get("publish", True),
    }
    if fm.get("due"):
        payload["due_at"] = fm["due"]

    if existing_id:
        return client.update_assignment(existing_id, payload)
    return client.create_assignment(payload)


def push_page(client: CanvasClient, fm: dict, html: str, existing_url: str | None) -> dict:
    payload = {
        "title": fm["title"],
        "body": html,
        "published": fm.get("publish", True),
    }
    if existing_url:
        return client.update_page(existing_url, payload)
    return client.create_page(payload)


def push_discussion(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    payload = {
        "title": fm["title"],
        "message": html,
        "discussion_type": "threaded",
        "published": fm.get("publish", True),
    }
    if fm.get("points") is not None:
        payload["assignment"] = {
            "points_possible": fm["points"],
            "due_at": fm.get("due"),
        }
    if existing_id:
        return client.update_discussion(existing_id, payload)
    return client.create_discussion(payload)


def push_quiz(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    payload = {
        "title": fm["title"],
        "description": html,
        "quiz_type": "assignment",
        "points_possible": fm.get("points"),
        "published": fm.get("publish", True),
    }
    if fm.get("due"):
        payload["due_at"] = fm["due"]

    if existing_id:
        result = client.update_quiz(existing_id, payload)
    else:
        result = client.create_quiz(payload)

    quiz_id = result["id"]

    # Wipe existing questions so an update replaces rather than appends.
    if existing_id:
        for q in client.list_quiz_questions(quiz_id):
            client.delete_quiz_question(quiz_id, q["id"])

    question_type_map = {
        "multiple_choice": "multiple_choice_question",
        "true_false": "true_false_question",
        "short_answer": "short_answer_question",
        "essay": "essay_question",
    }

    for q in fm.get("questions", []):
        q_type = q.get("type", "short_answer")
        canvas_q_type = question_type_map.get(q_type, q_type)
        question_payload = {
            "question_name": q.get("prompt", "")[:50],
            "question_text": q.get("prompt", ""),
            "question_type": canvas_q_type,
            "points_possible": q.get("points", 1),
        }
        if q_type in ("multiple_choice", "true_false"):
            question_payload["answers"] = [
                {"answer_text": a["text"], "answer_weight": 100 if a.get("correct") else 0}
                for a in q.get("answers", [])
            ]
        client.add_quiz_question(quiz_id, question_payload)

    return result


def push_artifact(md_path: Path, manifest_path: Path) -> dict:
    repo_root = Path.cwd().resolve()
    md_path = md_path.resolve()
    manifest_path = manifest_path.resolve()
    validate_artifact_manifest_pair(md_path, manifest_path)

    # Validate first
    errors = validate_artifact(md_path)
    if errors:
        raise ValueError(f"Validation failed: {errors}")

    fm, body = parse_frontmatter(md_path)
    html = md_body_to_canvas_html(body)

    with manifest_lock(manifest_path):
        manifest = load_manifest(manifest_path)

        rel_path = str(md_path.relative_to(repo_root))
        manifest_course_id = manifest.get("instance", {}).get("course_id") or 0
        if not manifest_course_id:
            raise ValueError(
                f"{manifest_path}: manifest instance.course_id is required and must be greater than zero"
            )
        course_id = int(manifest_course_id)

        client = CanvasClient.from_env(course_id=course_id)

        # Look up existing canvas entry for this file
        artifacts = manifest.setdefault("artifacts", {})
        existing = artifacts.get(rel_path, {})
        existing_id = existing.get("canvas_id")
        existing_page_url = existing.get("canvas_page_url")

        artifact_type = fm["type"]
        action = "updated" if (existing_id or existing_page_url) else "created"

        if artifact_type == "assignment":
            result = push_assignment(client, fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif artifact_type == "page":
            result = push_page(client, fm, html, existing_page_url)
            canvas_id = result.get("page_id")
            canvas_page_url = result.get("url")
        elif artifact_type == "discussion":
            result = push_discussion(client, fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif artifact_type == "quiz":
            result = push_quiz(client, fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif artifact_type == "module_header":
            canvas_id = None
            canvas_page_url = None
            result = {}
        else:
            raise ValueError(f"Unknown artifact type: {artifact_type}")

        # Resolve module and add to it if not already present
        module_id = resolve_or_create_module(client, fm["module"])

        if artifact_type != "module_header" and action == "created":
            content_type_map = {
                "assignment": "Assignment",
                "page": "Page",
                "discussion": "Discussion",
                "quiz": "Quiz",
            }
            client.add_module_item(
                module_id,
                title=fm["title"],
                content_type=content_type_map[artifact_type],
                content_id=canvas_id if artifact_type != "page" else None,
                page_url=canvas_page_url if artifact_type == "page" else None,
                position=fm.get("position"),
            )

        # Update manifest
        import hashlib
        from datetime import datetime, timezone

        content_hash = hashlib.sha256(md_path.read_bytes()).hexdigest()

        artifacts[rel_path] = {
            "canvas_type": artifact_type,
            "canvas_id": canvas_id,
            "canvas_page_url": canvas_page_url,
            "canvas_module_id": module_id,
            "content_hash": content_hash,
            "last_pushed": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        manifest["last_sync"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        save_manifest(manifest_path, manifest)

        return {
            "action": action,
            "file": rel_path,
            "canvas_id": canvas_id,
            "canvas_module_id": module_id,
        }


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    try:
        result = push_artifact(args.file, args.manifest)
        print(json.dumps(result, indent=2))
        return 0
    except ValueError as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        return 2
    except CanvasError as e:
        print(f"CANVAS ERROR: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

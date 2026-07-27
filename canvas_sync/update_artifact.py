"""
Prepare and verify one Canvas module item for local editing.

Usage:
  python canvas_sync/update_artifact.py list --course-id 180 --format markdown
  python canvas_sync/update_artifact.py prepare --course-id 180 --module-item-id 12345
  python canvas_sync/update_artifact.py prepare --course-id 180 --module-item-id 12345 --sprint 2
  python canvas_sync/update_artifact.py verify --course-id 180 --module-item-id 12345 --file course1/sprints/sprint-2/item.md

The script never pushes to Canvas. It reads Canvas, writes or refreshes one
local Markdown artifact, updates the manifest mapping when needed, and verifies
that later local edits did not change the artifact identity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError
from canvas_sync.instance_guard import check_env_matches_instance, check_instance_ready
from canvas_sync.pull import html_to_markdown
from canvas_sync.schema import parse_frontmatter, validate_artifact


REPO_ROOT = Path(__file__).resolve().parent.parent

CANVAS_ITEM_TYPE_BY_ARTIFACT = {
    "assignment": "Assignment",
    "page": "Page",
    "discussion": "Discussion",
    "quiz": "Quiz",
}

ARTIFACT_TYPE_BY_CANVAS_ITEM = {
    "Assignment": "assignment",
    "Page": "page",
    "Discussion": "discussion",
    "Quiz": "quiz",
}

CANVAS_SUBMISSION_TO_LOCAL = {
    "online_text_entry": "text_entry",
    "online_upload": "file_upload",
    "online_quiz": "online_quiz",
    "discussion_topic": "discussion_topic",
    "none": "none",
    "on_paper": "none",
}

QUESTION_TYPE_TO_LOCAL = {
    "multiple_choice_question": "multiple_choice",
    "multiple_choice": "multiple_choice",
    "true_false_question": "true_false",
    "true_false": "true_false",
    "short_answer_question": "short_answer",
    "short_answer": "short_answer",
    "essay_question": "essay",
    "essay": "essay",
}

IMMUTABLE_FRONTMATTER_FIELDS = ("type", "slug", "sprint", "module", "position")


class UpdateArtifactError(ValueError):
    """Raised for update-artifact planning or verification failures."""


class SprintRequiredError(UpdateArtifactError):
    """Raised when a Canvas-only item cannot be placed in a local sprint."""

    def __init__(self, module_item: dict):
        self.module_item = module_item
        super().__init__(
            "sprint is required because the selected Canvas module has no single local sprint"
        )


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def repo_relative(path: Path, repo_root: Path = REPO_ROOT) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def artifact_id_from_rel_path(rel_path: str) -> str:
    return "-".join(Path(rel_path).with_suffix("").parts).replace("_", "-")


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(path)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or "canvas-artifact"


def normalize_text(value: str | None) -> str:
    return (value or "").replace("\u2014", "-")


def markdown_from_html(html: str | None) -> str:
    return normalize_text(html_to_markdown(html or "")).strip()


def clean_number(value: Any) -> int | float:
    number = float(value or 0)
    if number.is_integer():
        return int(number)
    return number


def resolve_manifest_for_course_id(course_id: int, repo_root: Path = REPO_ROOT) -> Path:
    matches: list[Path] = []
    for manifest_path in sorted(repo_root.glob("*/manifests/production.json")):
        try:
            manifest = load_json(manifest_path)
        except (json.JSONDecodeError, OSError):
            continue
        if int(manifest.get("instance", {}).get("course_id") or 0) == int(course_id):
            matches.append(manifest_path)

    if not matches:
        raise UpdateArtifactError(
            f"no production manifest found for Canvas course ID {course_id}"
        )
    if len(matches) > 1:
        joined = ", ".join(repo_relative(path, repo_root) for path in matches)
        raise UpdateArtifactError(
            f"Canvas course ID {course_id} matches multiple manifests: {joined}"
        )
    return matches[0]


def artifact_canvas_key(entry: dict) -> tuple[str, Any] | None:
    atype = entry.get("canvas_type")
    if atype == "module_header":
        return None
    canvas_type = CANVAS_ITEM_TYPE_BY_ARTIFACT.get(atype)
    if not canvas_type:
        return None
    value = entry.get("canvas_page_url") if atype == "page" else entry.get("canvas_id")
    if value in (None, ""):
        return None
    return canvas_type, value


def module_item_canvas_key(item: dict) -> tuple[str, Any] | None:
    item_type = item.get("type")
    if item_type == "Page":
        value = item.get("page_url")
    else:
        value = item.get("content_id")
    if not item_type or value in (None, ""):
        return None
    return item_type, value


def manifest_files_by_canvas_key(manifest: dict) -> dict[tuple[str, Any], list[str]]:
    files_by_key: dict[tuple[str, Any], list[str]] = {}
    for rel_path, entry in sorted(manifest.get("artifacts", {}).items()):
        key = artifact_canvas_key(entry)
        if key:
            files_by_key.setdefault(key, []).append(rel_path)
    return files_by_key


def fetch_live_module_items(client: CanvasClient, manifest: dict) -> list[dict]:
    files_by_key = manifest_files_by_canvas_key(manifest)
    records: list[dict] = []
    for module in sorted(
        client.list_modules(),
        key=lambda m: (m.get("position") or 999999, m.get("id") or 0),
    ):
        module_id = int(module["id"])
        for item in sorted(
            client.list_module_items(module_id),
            key=lambda i: (i.get("position") or 999999, i.get("id") or 0),
        ):
            key = module_item_canvas_key(item)
            manifest_files = files_by_key.get(key, []) if key else []
            records.append(
                {
                    "module_id": module_id,
                    "module_name": module.get("name"),
                    "module_position": module.get("position"),
                    "module_published": module.get("published"),
                    "module_item_id": int(item["id"]),
                    "position": item.get("position"),
                    "title": item.get("title"),
                    "type": item.get("type"),
                    "content_id": item.get("content_id"),
                    "page_url": item.get("page_url"),
                    "published": item.get("published"),
                    "manifest_file": manifest_files[0] if manifest_files else None,
                    "manifest_files": manifest_files,
                }
            )
    return records


def find_module_item(items: list[dict], module_item_id: int) -> dict:
    matches = [item for item in items if int(item["module_item_id"]) == int(module_item_id)]
    if not matches:
        raise UpdateArtifactError(f"module_item_id:{module_item_id} is not live in Canvas")
    if len(matches) > 1:
        raise UpdateArtifactError(f"module_item_id:{module_item_id} matched multiple live items")
    return matches[0]


def get_client(
    course_id: int,
    client: CanvasClient | None = None,
    *,
    manifest: dict | None = None,
    manifest_label: str = "the selected profile",
) -> CanvasClient:
    if client is not None:
        return client
    if manifest is not None:
        check_instance_ready(manifest, manifest_label=manifest_label)
        check_env_matches_instance(manifest, manifest_label=manifest_label)
    return CanvasClient.from_env(course_id=course_id)


def list_artifacts(
    course_id: int,
    *,
    client: CanvasClient | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict:
    manifest_path = resolve_manifest_for_course_id(course_id, repo_root)
    manifest = load_json(manifest_path)
    live_items = fetch_live_module_items(
        get_client(course_id, client, manifest=manifest, manifest_label=str(manifest_path)),
        manifest,
    )
    return {
        "course_id": course_id,
        "manifest": repo_relative(manifest_path, repo_root),
        "items": live_items,
    }


def render_list_markdown(report: dict) -> str:
    lines = [
        "# Canvas Artifact List",
        "",
        f"Course ID: {report['course_id']}",
        f"Manifest: `{report['manifest']}`",
        "",
        "| Module | Type | Title | Published | module_item_id | Content ID | Page URL | Local file |",
        "|---|---|---|---|---:|---:|---|---|",
    ]
    for item in report["items"]:
        published = "" if item.get("published") is None else ("yes" if item["published"] else "no")
        local_file = item.get("manifest_file") or ""
        lines.append(
            f"| {item.get('module_name') or ''} | {item.get('type') or ''} | "
            f"{item.get('title') or ''} | {published} | {item['module_item_id']} | "
            f"{item.get('content_id') or ''} | {item.get('page_url') or ''} | {local_file} |"
        )
    return "\n".join(lines) + "\n"


def fetch_canvas_state(client: CanvasClient, item: dict) -> dict:
    item_type = item.get("type")
    if item_type == "Assignment":
        return client.get_assignment(int(item["content_id"]))
    if item_type == "Page":
        return client.get_page(item["page_url"])
    if item_type == "Discussion":
        return client.get_discussion(int(item["content_id"]))
    if item_type == "Quiz":
        return client.get_quiz(int(item["content_id"]))
    raise UpdateArtifactError(f"module_item_id:{item['module_item_id']} has unsupported type {item_type}")


def title_from_state(state: dict, item: dict) -> str:
    return normalize_text(state.get("name") or state.get("title") or item.get("title") or "")


def published_from_state(state: dict, item: dict) -> bool:
    if item.get("published") is not None:
        return bool(item.get("published"))
    if state.get("published") is not None:
        return bool(state.get("published"))
    return True


def body_from_state(state: dict) -> str:
    html = state.get("description") or state.get("body") or state.get("message") or ""
    return markdown_from_html(html)


def points_from_state(state: dict, questions: list[dict] | None = None) -> int | float:
    points = state.get("points_possible")
    if points is None and state.get("assignment"):
        points = state["assignment"].get("points_possible")
    if points is None and questions is not None:
        points = sum(float(question.get("points", 0) or 0) for question in questions)
    return clean_number(points)


def assignment_submission_type(state: dict) -> str:
    submission_types = state.get("submission_types") or []
    first = submission_types[0] if submission_types else "online_text_entry"
    return CANVAS_SUBMISSION_TO_LOCAL.get(first, "text_entry")


def import_quiz_questions(client: CanvasClient, quiz_id: int) -> list[dict]:
    questions: list[dict] = []
    for question in client.list_quiz_questions(quiz_id):
        q_type = QUESTION_TYPE_TO_LOCAL.get(question.get("question_type"), "short_answer")
        imported: dict[str, Any] = {
            "type": q_type,
            "prompt": markdown_from_html(
                question.get("question_text") or question.get("question_name") or ""
            ),
            "points": clean_number(question.get("points_possible")),
        }
        if q_type in {"multiple_choice", "true_false"}:
            answers = []
            for answer in question.get("answers") or []:
                text = answer.get("answer_text") or answer.get("text") or ""
                weight = answer.get("answer_weight", answer.get("weight", 0)) or 0
                answers.append({"text": normalize_text(str(text)), "correct": float(weight) > 0})
            if answers:
                imported["answers"] = answers
        questions.append(imported)
    return questions


def build_frontmatter(
    *,
    client: CanvasClient,
    item: dict,
    state: dict,
    sprint: int,
    slug: str,
    artifact_id: str,
    existing_frontmatter: dict | None = None,
) -> dict:
    local_type = ARTIFACT_TYPE_BY_CANVAS_ITEM.get(item.get("type"))
    if not local_type:
        raise UpdateArtifactError(f"unsupported Canvas item type: {item.get('type')}")

    fm = dict(existing_frontmatter or {})
    fm.update(
        {
            "type": local_type,
            "title": title_from_state(state, item),
            "slug": fm.get("slug") or slug,
            "artifact_id": fm.get("artifact_id") or artifact_id,
            "sprint": fm.get("sprint", sprint),
            "module": item["module_name"],
            "position": int(item.get("position") or 1),
            "publish": published_from_state(state, item),
        }
    )

    if local_type == "page":
        fm.pop("points", None)
        fm.pop("submission_type", None)
        fm.pop("questions", None)
    elif local_type == "assignment":
        fm["points"] = points_from_state(state)
        fm["submission_type"] = assignment_submission_type(state)
        fm.pop("questions", None)
    elif local_type == "discussion":
        fm["points"] = points_from_state(state)
        fm["submission_type"] = "discussion_topic"
        fm.pop("questions", None)
    elif local_type == "quiz":
        questions = import_quiz_questions(client, int(item["content_id"]))
        fm["points"] = points_from_state(state, questions)
        fm["submission_type"] = "online_quiz"
        if questions:
            fm["questions"] = questions
        else:
            fm.pop("questions", None)
    return fm


def write_artifact(md_path: Path, frontmatter: dict, body: str) -> str:
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.safe_dump(frontmatter, f, sort_keys=False, allow_unicode=True)
        f.write("---\n\n")
        f.write(normalize_text(body).rstrip())
        f.write("\n")
    return hashlib.sha256(md_path.read_bytes()).hexdigest()


def unique_artifact_path(
    course_dir: Path,
    sprint: int,
    slug: str,
    manifest: dict,
    repo_root: Path = REPO_ROOT,
) -> Path:
    used = set(manifest.get("artifacts", {}).keys())
    sprint_dir = course_dir / "sprints" / f"sprint-{sprint}"
    candidate = sprint_dir / f"{slug}.md"
    suffix = 2
    while repo_relative(candidate, repo_root) in used or candidate.exists():
        candidate = sprint_dir / f"{slug}-{suffix}.md"
        suffix += 1
    return candidate


def sprint_from_path(rel_path: str) -> int | None:
    match = re.search(r"/sprints/sprint-(\d+)/", f"/{rel_path}")
    if not match:
        return None
    return int(match.group(1))


def infer_sprint_for_module(manifest: dict, module_id: int, repo_root: Path = REPO_ROOT) -> int | None:
    sprints: set[int] = set()
    for rel_path, entry in manifest.get("artifacts", {}).items():
        if int(entry.get("canvas_module_id") or 0) != int(module_id):
            continue
        md_path = repo_root / rel_path
        if md_path.exists():
            try:
                fm, _body = parse_frontmatter(md_path)
                if fm.get("sprint") is not None:
                    sprints.add(int(fm["sprint"]))
                    continue
            except Exception:
                pass
        path_sprint = sprint_from_path(rel_path)
        if path_sprint is not None:
            sprints.add(path_sprint)
    return next(iter(sprints)) if len(sprints) == 1 else None


def module_header_exists(manifest: dict, module_id: int) -> bool:
    return any(
        entry.get("canvas_type") == "module_header"
        and int(entry.get("canvas_module_id") or 0) == int(module_id)
        for entry in manifest.get("artifacts", {}).values()
    )


def add_module_header_if_needed(
    *,
    manifest: dict,
    course_dir: Path,
    module_item: dict,
    sprint: int,
    pulled_at: str,
    repo_root: Path = REPO_ROOT,
) -> str | None:
    if module_header_exists(manifest, int(module_item["module_id"])):
        return None

    module_name = module_item["module_name"]
    path = unique_artifact_path(course_dir, sprint, slugify(module_name), manifest, repo_root)
    rel_path = repo_relative(path, repo_root)
    fm = {
        "type": "module_header",
        "title": module_name,
        "slug": path.stem,
        "artifact_id": artifact_id_from_rel_path(rel_path),
        "sprint": sprint,
        "module": module_name,
        "position": int(module_item.get("module_position") or 1),
        "publish": bool(module_item.get("module_published", True)),
    }
    body = f"# {module_name}\n\nImported from live Canvas for single-artifact editing."
    content_hash = write_artifact(path, fm, body)
    manifest["artifacts"][rel_path] = {
        "canvas_type": "module_header",
        "canvas_id": None,
        "canvas_page_url": None,
        "canvas_module_id": int(module_item["module_id"]),
        "content_hash": content_hash,
        "last_pushed": None,
        "last_pulled": pulled_at,
    }
    return rel_path


def manifest_entry_for_item(item: dict, local_type: str, content_hash: str, pulled_at: str) -> dict:
    return {
        "canvas_type": local_type,
        "canvas_id": None if local_type == "page" else int(item["content_id"]),
        "canvas_page_url": item.get("page_url") if local_type == "page" else None,
        "canvas_module_id": int(item["module_id"]),
        "content_hash": content_hash,
        "last_pushed": None,
        "last_pulled": pulled_at,
    }


def prepare_artifact(
    course_id: int,
    module_item_id: int,
    *,
    sprint: int | None = None,
    client: CanvasClient | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict:
    manifest_path = resolve_manifest_for_course_id(course_id, repo_root)
    manifest = load_json(manifest_path)
    course_dir = manifest_path.parent.parent
    client = get_client(course_id, client, manifest=manifest, manifest_label=str(manifest_path))
    items = fetch_live_module_items(client, manifest)
    item = find_module_item(items, module_item_id)
    local_type = ARTIFACT_TYPE_BY_CANVAS_ITEM.get(item.get("type"))
    if not local_type:
        raise UpdateArtifactError(f"unsupported Canvas item type: {item.get('type')}")

    rel_path = item.get("manifest_file")
    inferred_sprint = infer_sprint_for_module(manifest, int(item["module_id"]), repo_root)
    target_sprint = sprint if sprint is not None else inferred_sprint
    if rel_path is None and target_sprint is None:
        raise SprintRequiredError(item)

    existing_fm: dict | None = None
    if rel_path:
        md_path = repo_root / rel_path
        if not md_path.exists() and sprint_from_path(rel_path) is None and target_sprint is None:
            raise SprintRequiredError(item)
        if md_path.exists():
            existing_fm, _old_body = parse_frontmatter(md_path)
        target_sprint = target_sprint if target_sprint is not None else sprint_from_path(rel_path)
        if target_sprint is None:
            raise SprintRequiredError(item)
        slug = existing_fm.get("slug") if existing_fm else Path(rel_path).stem
    else:
        md_path = unique_artifact_path(
            course_dir,
            int(target_sprint),
            slugify(item["title"]),
            manifest,
            repo_root,
        )
        rel_path = repo_relative(md_path, repo_root)
        slug = md_path.stem

    state = fetch_canvas_state(client, item)
    pulled_at = now_utc()
    fm = build_frontmatter(
        client=client,
        item=item,
        state=state,
        sprint=int(target_sprint),
        slug=slug,
        artifact_id=(existing_fm or {}).get("artifact_id") or artifact_id_from_rel_path(rel_path),
        existing_frontmatter=existing_fm,
    )
    body = body_from_state(state)
    content_hash = write_artifact(md_path, fm, body)

    if not item.get("manifest_file"):
        added_header = add_module_header_if_needed(
            manifest=manifest,
            course_dir=course_dir,
            module_item=item,
            sprint=int(target_sprint),
            pulled_at=pulled_at,
            repo_root=repo_root,
        )
        manifest["artifacts"][rel_path] = manifest_entry_for_item(
            item, local_type, content_hash, pulled_at
        )
        action = "imported"
    else:
        added_header = None
        entry = manifest["artifacts"][rel_path]
        entry.update(
            {
                "canvas_type": local_type,
                "canvas_id": None if local_type == "page" else int(item["content_id"]),
                "canvas_page_url": item.get("page_url") if local_type == "page" else None,
                "canvas_module_id": int(item["module_id"]),
                "content_hash": content_hash,
                "last_pulled": pulled_at,
            }
        )
        action = "refreshed"

    manifest["last_sync"] = pulled_at
    save_json(manifest_path, manifest)

    return {
        "status": "prepared",
        "action": action,
        "course_id": course_id,
        "manifest": repo_relative(manifest_path, repo_root),
        "module_item_id": int(module_item_id),
        "file": rel_path,
        "type": local_type,
        "title": fm["title"],
        "added_module_header": added_header,
    }


def verify_artifact(
    course_id: int,
    module_item_id: int,
    file_path: Path,
    *,
    client: CanvasClient | None = None,
    repo_root: Path = REPO_ROOT,
) -> dict:
    manifest_path = resolve_manifest_for_course_id(course_id, repo_root)
    manifest = load_json(manifest_path)
    client = get_client(course_id, client, manifest=manifest, manifest_label=str(manifest_path))
    items = fetch_live_module_items(client, manifest)
    item = find_module_item(items, module_item_id)
    rel_path = repo_relative((repo_root / file_path).resolve() if not file_path.is_absolute() else file_path, repo_root)

    if item.get("manifest_file") != rel_path:
        raise UpdateArtifactError(
            f"{rel_path} is not the manifest-backed file for module_item_id:{module_item_id}"
        )
    entry = manifest.get("artifacts", {}).get(rel_path)
    if not entry:
        raise UpdateArtifactError(f"{rel_path} is not present in the manifest")

    md_path = repo_root / rel_path
    errors = validate_artifact(md_path)
    if errors:
        raise UpdateArtifactError("; ".join(errors))
    fm, _body = parse_frontmatter(md_path)

    expected_type = ARTIFACT_TYPE_BY_CANVAS_ITEM.get(item.get("type"))
    expected = {
        "type": expected_type,
        "slug": md_path.stem,
        "sprint": sprint_from_path(rel_path),
        "module": item.get("module_name"),
        "position": int(item.get("position") or 1),
    }
    for key in IMMUTABLE_FRONTMATTER_FIELDS:
        if fm.get(key) != expected.get(key):
            raise UpdateArtifactError(
                f"{rel_path}: {key} is immutable for this workflow "
                f"(expected {expected.get(key)!r}, found {fm.get(key)!r})"
            )

    expected_key = module_item_canvas_key(item)
    manifest_key = artifact_canvas_key(entry)
    if expected_key != manifest_key:
        raise UpdateArtifactError(
            f"{rel_path}: manifest Canvas identity does not match module_item_id:{module_item_id}"
        )
    if int(entry.get("canvas_module_id") or 0) != int(item["module_id"]):
        raise UpdateArtifactError(
            f"{rel_path}: manifest canvas_module_id does not match module_item_id:{module_item_id}"
        )

    return {
        "status": "verified",
        "course_id": course_id,
        "manifest": repo_relative(manifest_path, repo_root),
        "module_item_id": int(module_item_id),
        "file": rel_path,
        "type": expected_type,
        "title": fm.get("title"),
    }


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def main() -> int:
    load_dotenv(REPO_ROOT / ".env")

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--course-id", type=int, required=True)
    list_parser.add_argument("--format", choices=("json", "markdown"), default="markdown")

    prepare_parser = subparsers.add_parser("prepare")
    prepare_parser.add_argument("--course-id", type=int, required=True)
    prepare_parser.add_argument("--module-item-id", type=int, required=True)
    prepare_parser.add_argument("--sprint", type=int, choices=range(0, 6))

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--course-id", type=int, required=True)
    verify_parser.add_argument("--module-item-id", type=int, required=True)
    verify_parser.add_argument("--file", type=Path, required=True)

    args = parser.parse_args()

    try:
        if args.command == "list":
            report = list_artifacts(args.course_id)
            if args.format == "json":
                print_json(report)
            else:
                print(render_list_markdown(report), end="")
            return 0
        if args.command == "prepare":
            print_json(
                prepare_artifact(
                    args.course_id,
                    args.module_item_id,
                    sprint=args.sprint,
                )
            )
            return 0
        if args.command == "verify":
            print_json(verify_artifact(args.course_id, args.module_item_id, args.file))
            return 0
    except SprintRequiredError as exc:
        print_json(
            {
                "status": "sprint_required",
                "message": str(exc),
                "module_item_id": exc.module_item.get("module_item_id"),
                "module": exc.module_item.get("module_name"),
                "title": exc.module_item.get("title"),
                "type": exc.module_item.get("type"),
            }
        )
        return 4
    except (UpdateArtifactError, CanvasError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    sys.exit(main())

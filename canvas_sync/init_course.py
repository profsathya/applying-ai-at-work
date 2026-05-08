"""
Initialize a local course directory for an existing Canvas course.

This script only writes local files. It does not call Canvas and does not
create a Canvas course shell.

Usage:
  python3 canvas_sync/init_course.py \
    --course course3 \
    --canvas-course-id 12345 \
    --base-url https://example.instructure.com \
    --title "Applying AI at Work, Cohort 3" \
    --term "Spring 2027" \
    --sprint-count 6

Safe smoke check:
  python3 canvas_sync/init_course.py \
    --course course-test-init \
    --canvas-course-id 999999 \
    --base-url https://example.instructure.com \
    --title "Test Init Course" \
    --term "Test Term" \
    --sprint-count 4

Then inspect the created files and remove course-test-init plus
context/course-specs/course-test-init-context.md.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent.parent
COURSE_KEY_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class InitCourseError(ValueError):
    """Raised when local course setup cannot proceed safely."""


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "y"}:
        return True
    if normalized in {"0", "false", "no", "n"}:
        return False
    raise argparse.ArgumentTypeError(f"Expected true or false, got {value!r}")


def validate_sprint_count(sprint_count: int) -> int:
    if sprint_count < 1:
        raise InitCourseError("sprint-count must be at least 1")
    return sprint_count


def validate_course_key(course_key: str) -> str:
    if not COURSE_KEY_RE.fullmatch(course_key):
        raise InitCourseError(
            "course must be lowercase kebab-case using only letters, numbers, and single hyphens"
        )
    path = Path(course_key)
    if path.is_absolute() or path.name != course_key or ".." in path.parts:
        raise InitCourseError("course must be a safe repo-root directory name")
    return course_key


def normalize_base_url(base_url: str) -> str:
    parsed = urlparse(base_url.strip())
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise InitCourseError("base-url must be an absolute http or https URL")
    return base_url.strip().rstrip("/") + "/"


def slugify(value: str, fallback: str = "context") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug or fallback


def repo_relative(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT.resolve()))


def write_text_file(
    path: Path,
    content: str,
    *,
    force: bool,
    created_files: list[str],
    skipped_files: list[str],
    overwritten_files: list[str],
) -> None:
    if path.exists() and not force:
        skipped_files.append(repo_relative(path))
        return
    existed = path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if existed:
        overwritten_files.append(repo_relative(path))
    else:
        created_files.append(repo_relative(path))


def write_json_file(
    path: Path,
    payload: dict,
    *,
    force: bool,
    created_files: list[str],
    skipped_files: list[str],
    overwritten_files: list[str],
) -> None:
    write_text_file(
        path,
        json.dumps(payload, indent=2) + "\n",
        force=force,
        created_files=created_files,
        skipped_files=skipped_files,
        overwritten_files=overwritten_files,
    )


def build_manifest(instance_name: str, base_url: str, canvas_course_id: int, term: str) -> dict:
    return {
        "instance": {
            "name": instance_name,
            "base_url": base_url,
            "course_id": canvas_course_id,
            "term": term,
        },
        "last_sync": None,
        "artifacts": {},
    }


def build_prd(course_key: str, title: str, course_code: str | None, term: str) -> dict:
    return {
        "course": {
            "slug": course_key,
            "name": title,
            "code": course_code or course_key,
            "term": term,
            "planned_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        },
        "items": [],
    }


def build_progress(course_key: str, title: str, canvas_course_id: int, term: str) -> str:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    term_line = f"Term: {term}\n" if term else ""
    return (
        f"# {title} Build Progress\n\n"
        f"Course: {title}\n"
        f"Target: {course_key}\n"
        f"Canvas course ID: {canvas_course_id}\n"
        f"{term_line}"
        f"Initialized at: {timestamp}\n\n"
        "## Setup log\n\n"
        f"- {timestamp}: Local course shell initialized. No Canvas writes were made.\n\n"
        "## Build log\n\n"
        "(Build workflows append one line here when Canvas is called.)\n"
    )


def build_design_readme(course_key: str, title: str, term: str, course_code: str | None) -> str:
    code_line = f"- Course code: {course_code}\n" if course_code else "- Course code:\n"
    term_line = f"- Term or cohort: {term}\n" if term else "- Term or cohort:\n"
    return (
        f"# {title} Design Notes\n\n"
        "Use this file for local course design decisions that should inform drafting.\n\n"
        "## Course Identity\n\n"
        f"- Local course key: {course_key}\n"
        f"- Course title: {title}\n"
        f"{code_line}"
        f"{term_line}"
        "\n## Course Purpose\n\n"
        "Describe what participants should be able to do by the end of the course.\n\n"
        "## Audience And Situation\n\n"
        "Describe participants, workplace context, constraints, and prior knowledge.\n\n"
        "## Course Arc\n\n"
        "Summarize the sequence from the first module through the final module.\n\n"
        "## Assessment Strategy\n\n"
        "Describe points, rubrics, quiz expectations, discussions, stakeholder evidence, and capstone expectations.\n\n"
        "## Constraints\n\n"
        "List due-date rules, submission types, required language, and anything to avoid.\n"
    )


def build_context_placeholder(
    course_key: str,
    title: str,
    term: str,
    course_code: str | None,
    sprint_count: int,
) -> str:
    code = course_code or ""
    term_value = term or ""
    sprint_sections = []
    for sprint in range(sprint_count):
        label = "Orientation Title" if sprint == 0 else "Module Title"
        sprint_sections.append(
            f"### Sprint {sprint}: <{label}>\n"
            "- Week or sequence position:\n"
            "- Purpose:\n"
            "- Required artifacts:\n"
        )
    return (
        f"# Course Context Spec: {title}\n\n"
        "## Target\n"
        f"- Course: {course_key}\n"
        f"- Course title: {title}\n"
        f"- Course code: {code}\n"
        f"- Term or delivery context: {term_value}\n"
        f"- Sprint/module count: {sprint_count}\n\n"
        "## Course Purpose\n"
        "Describe what participants should be able to do by the end of the course.\n\n"
        "## Audience And Situation\n"
        "Name what participants already know, what workplace context they bring, and what constraints matter.\n\n"
        "## Course Arc\n"
        "Summarize the sequence from the first module through the final module.\n\n"
        "## Sprint / Module Map\n\n"
        + "\n".join(sprint_sections)
        + "\n\n"
        "## Assessment Strategy\n"
        "Describe points, rubrics, quiz expectations, discussions, stakeholder evidence, and capstone expectations.\n\n"
        "## Required Ideas\n"
        "- Idea, concept, or behavior that must appear.\n\n"
        "## Constraints\n"
        "- Due dates, if any, must be full Canvas-compatible timestamps.\n"
        "- Name required submission types.\n"
        "- Name anything to avoid.\n\n"
        "## Tone And Voice\n"
        "Describe the desired tone if it differs from the course default.\n\n"
        "## Source Material\n"
        "Link or summarize any human-provided notes Codex should use.\n\n"
        "## Open Questions\n"
        "List anything Codex should ask before writing.\n"
    )


def copy_context_source(
    source: Path,
    course_key: str,
    *,
    force: bool,
    created_files: list[str],
    skipped_files: list[str],
    overwritten_files: list[str],
) -> Path:
    source = source.expanduser().resolve()
    if not source.exists() or not source.is_file():
        raise InitCourseError(f"context-spec-source not found: {source}")

    context_dir = REPO_ROOT / "context" / "course-specs"
    context_dir.mkdir(parents=True, exist_ok=True)

    try:
        source.relative_to(context_dir.resolve())
        skipped_files.append(repo_relative(source))
        return source
    except ValueError:
        pass

    source_slug = slugify(source.stem)
    if source_slug.startswith(f"{course_key}-"):
        dest_name = f"{source_slug}.md"
    else:
        dest_name = f"{course_key}-{source_slug}.md"
    dest = context_dir / dest_name

    if dest.exists() and not force:
        skipped_files.append(repo_relative(dest))
        return dest

    existed = dest.exists()
    shutil.copyfile(source, dest)
    if existed:
        overwritten_files.append(repo_relative(dest))
    else:
        created_files.append(repo_relative(dest))
    return dest


def init_course(
    *,
    course_key: str,
    canvas_course_id: int,
    base_url: str,
    title: str,
    term: str,
    instance_name: str,
    course_code: str | None,
    context_spec_source: Path | None,
    context_spec_inline_file: Path | None,
    sprint_count: int,
    force: bool,
) -> dict:
    course_key = validate_course_key(course_key)
    sprint_count = validate_sprint_count(sprint_count)
    base_url = normalize_base_url(base_url)
    if canvas_course_id <= 0:
        raise InitCourseError("canvas-course-id must be a positive integer")
    if not title.strip():
        raise InitCourseError("title is required")
    if not instance_name.strip():
        raise InitCourseError("instance-name is required")
    if context_spec_source and context_spec_inline_file:
        raise InitCourseError("use either context-spec-source or context-spec-inline-file, not both")

    course_dir = REPO_ROOT / course_key
    if course_dir.exists() and not course_dir.is_dir():
        raise InitCourseError(f"{course_key} exists but is not a directory")
    if course_dir.exists() and not force:
        raise InitCourseError(f"{course_key} already exists. Re-run with --force true to modify it.")

    created_dirs: list[str] = []
    skipped_dirs: list[str] = []
    created_files: list[str] = []
    skipped_files: list[str] = []
    overwritten_files: list[str] = []

    directories = [
        course_dir,
        course_dir / "design",
        course_dir / "sprints",
        *(course_dir / "sprints" / f"sprint-{i}" for i in range(sprint_count)),
        course_dir / "manifests",
        course_dir / "reports",
        REPO_ROOT / "context" / "course-specs",
    ]
    for directory in directories:
        if directory.exists():
            skipped_dirs.append(repo_relative(directory))
        else:
            directory.mkdir(parents=True, exist_ok=True)
            created_dirs.append(repo_relative(directory))

    manifest_path = course_dir / "manifests" / f"{instance_name}.json"
    write_json_file(
        manifest_path,
        build_manifest(instance_name, base_url, canvas_course_id, term),
        force=force,
        created_files=created_files,
        skipped_files=skipped_files,
        overwritten_files=overwritten_files,
    )

    progress_path = course_dir / "progress.md"
    write_text_file(
        progress_path,
        build_progress(course_key, title, canvas_course_id, term),
        force=force,
        created_files=created_files,
        skipped_files=skipped_files,
        overwritten_files=overwritten_files,
    )

    prd_path = course_dir / "prd.json"
    write_json_file(
        prd_path,
        build_prd(course_key, title, course_code, term),
        force=force,
        created_files=created_files,
        skipped_files=skipped_files,
        overwritten_files=overwritten_files,
    )

    design_readme_path = course_dir / "design" / "README.md"
    write_text_file(
        design_readme_path,
        build_design_readme(course_key, title, term, course_code),
        force=force,
        created_files=created_files,
        skipped_files=skipped_files,
        overwritten_files=overwritten_files,
    )

    context_spec_path: Path
    if context_spec_source:
        context_spec_path = copy_context_source(
            context_spec_source,
            course_key,
            force=force,
            created_files=created_files,
            skipped_files=skipped_files,
            overwritten_files=overwritten_files,
        )
    else:
        context_spec_path = REPO_ROOT / "context" / "course-specs" / f"{course_key}-context.md"
        if context_spec_inline_file:
            inline_path = context_spec_inline_file.expanduser().resolve()
            if not inline_path.exists() or not inline_path.is_file():
                raise InitCourseError(f"context-spec-inline-file not found: {inline_path}")
            content = inline_path.read_text(encoding="utf-8")
        else:
            content = build_context_placeholder(course_key, title, term, course_code, sprint_count)
        write_text_file(
            context_spec_path,
            content,
            force=force,
            created_files=created_files,
            skipped_files=skipped_files,
            overwritten_files=overwritten_files,
        )

    return {
        "course": course_key,
        "sprint_count": sprint_count,
        "manifest_path": repo_relative(manifest_path),
        "context_spec_path": repo_relative(context_spec_path),
        "created_directories": created_dirs,
        "skipped_directories": skipped_dirs,
        "created_files": created_files,
        "skipped_files": skipped_files,
        "overwritten_files": overwritten_files,
        "next_recommended_commands": [
            f"python3 canvas_sync/schema.py --manifest {repo_relative(manifest_path)}",
            f"python3 canvas_sync/schema.py --prd {repo_relative(prd_path)}",
            f"Draft {course_key} from {repo_relative(context_spec_path)} and stop before Canvas.",
            f"Draft {course_key} sprint 0 from a module spec and stop before Canvas.",
            f"Push reviewed {course_key} files to Canvas.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--course", required=True)
    parser.add_argument("--canvas-course-id", type=int, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--term", default="")
    parser.add_argument("--sprint-count", type=int, required=True)
    parser.add_argument("--instance-name", default="production")
    parser.add_argument("--course-code")
    parser.add_argument("--context-spec-source", type=Path)
    parser.add_argument("--context-spec-inline-file", type=Path)
    parser.add_argument("--force", nargs="?", const="true", default="false", type=parse_bool)
    args = parser.parse_args()

    try:
        summary = init_course(
            course_key=args.course,
            canvas_course_id=args.canvas_course_id,
            base_url=args.base_url,
            title=args.title,
            term=args.term,
            instance_name=args.instance_name,
            course_code=args.course_code,
            context_spec_source=args.context_spec_source,
            context_spec_inline_file=args.context_spec_inline_file,
            sprint_count=args.sprint_count,
            force=args.force,
        )
    except InitCourseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
Schema validation for artifact frontmatter, manifests, and PRDs.

Usage:
  python canvas_sync/schema.py --artifact <md_file>
  python canvas_sync/schema.py --manifest <json_file>
  python canvas_sync/schema.py --state <json_file>
  python canvas_sync/schema.py --prd <json_file>
  python canvas_sync/schema.py --all

Exit codes:
  0 = all checks passed
  1 = validation errors (printed to stderr)
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schema"
COURSE_KEY_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ARTIFACT_LINK_RE = re.compile(
    r"\]\(\s*artifact:([^\s)]*)"
)
CANVAS_COURSE_URL_RE = re.compile(
    r"https?://[^\s)>]+/courses/\d+(?:/|\b)",
    re.IGNORECASE,
)
ARTIFACT_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)


def parse_frontmatter(md_path: Path) -> tuple[dict, str]:
    """Split an MD file into (frontmatter_dict, body_str)."""
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{md_path}: missing YAML frontmatter")
    closing = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == "---"), None)
    if closing is None:
        raise ValueError(f"{md_path}: malformed frontmatter (no closing ---)")
    frontmatter = yaml.safe_load("".join(lines[1:closing]))
    if not isinstance(frontmatter, dict):
        raise ValueError(f"{md_path}: frontmatter must be a YAML mapping")
    body = "".join(lines[closing + 1:]).lstrip("\n")
    return frontmatter, body


def _course_dir_for_artifact(md_path: Path) -> Path | None:
    for parent in md_path.resolve().parents:
        if parent.name == "sprints":
            return parent.parent
    return None


def validate_artifact_references(md_path: Path, body: str) -> list[str]:
    raw_references = ARTIFACT_LINK_RE.findall(body)
    references = [value for value in raw_references if ARTIFACT_ID_RE.fullmatch(value)]
    errors: list[str] = []
    if CANVAS_COURSE_URL_RE.search(body):
        errors.append(
            f"{md_path}: participant-facing Markdown must not contain an "
            "instance-specific Canvas course URL; use artifact:<artifact_id>"
        )
    for value in sorted(set(raw_references) - set(references)):
        errors.append(
            f"{md_path}: invalid artifact reference {value!r}; "
            "expected artifact:<artifact_id>"
        )
    if not raw_references:
        return errors
    course_dir = _course_dir_for_artifact(md_path)
    if course_dir is None:
        return errors + [
            f"{md_path}: cannot resolve artifact references outside a course sprints directory"
        ]
    known: set[str] = set()
    for candidate in course_dir.glob("sprints/sprint-*/**/*.md"):
        try:
            frontmatter, _candidate_body = parse_frontmatter(candidate)
        except (ValueError, yaml.YAMLError):
            continue
        artifact_id = frontmatter.get("artifact_id")
        if artifact_id and frontmatter.get("type") != "module_header":
            known.add(str(artifact_id))
    for artifact_id in sorted(set(references)):
        if artifact_id not in known:
            errors.append(
                f"{md_path}: unknown or non-renderable artifact reference "
                f"{artifact_id!r}"
            )
    return errors


def validate_artifact(md_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter, body = parse_frontmatter(md_path)
    except (ValueError, yaml.YAMLError) as e:
        return [str(e)]

    schema = load_schema("frontmatter")
    try:
        jsonschema.validate(frontmatter, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{md_path}: {e.message} (at {'/'.join(str(p) for p in e.path)})")

    errors.extend(validate_ai_activity_delivery(md_path, frontmatter))
    errors.extend(validate_guided_assignment(md_path, frontmatter, body))
    errors.extend(validate_artifact_references(md_path, body))
    source_id = frontmatter.get('walkthrough_after')
    if source_id:
        course_dir = _course_dir_for_artifact(md_path)
        if course_dir:
            sources = []
            for candidate in course_dir.glob('sprints/sprint-*/*.md'):
                try:
                    candidate_fm, _ = parse_frontmatter(candidate)
                except (ValueError, yaml.YAMLError):
                    continue
                if candidate_fm.get('artifact_id') == source_id:
                    sources.append(candidate_fm)
            if len(sources) != 1 or sources[0].get('module') != frontmatter.get('module'):
                errors.append(f'{md_path}: walkthrough_after must resolve to one source in the same course module')

    for key in ("quiz_type", "allowed_attempts"):
        if key in frontmatter and (frontmatter.get("type") != "quiz" or frontmatter.get("delivery_mode") == "ai_activity"):
            errors.append(f"{md_path}: {key} requires a native quiz")
    if "grading_type" in frontmatter and frontmatter.get("type") != "discussion":
        errors.append(f"{md_path}: grading_type requires a discussion")

    # Soft checks that aren't easily expressed in JSON Schema
    if frontmatter.get("type") in ("assignment", "quiz", "discussion"):
        if frontmatter.get("points") is None:
            errors.append(f"{md_path}: {frontmatter['type']} requires points")

    if frontmatter.get("type") == "page" and frontmatter.get("points") is not None:
        errors.append(f"{md_path}: pages must not have points")

    # HTML leakage check (critical: MD must stay canvas-agnostic)
    forbidden_patterns = ["<iframe", "<script", "<style", "javascript:", "onload="]
    for pattern in forbidden_patterns:
        if pattern in body.lower():
            errors.append(f"{md_path}: body contains forbidden pattern '{pattern}'")

    from canvas_sync.local_images import local_image_assets
    from canvas_sync.hosted_html import markdown_body_to_html
    try:
        local_image_assets(md_path, markdown_body_to_html(body))
    except ValueError as exc:
        errors.append(str(exc))

    # Human-authored source punctuation is preserved only inside verified source segments.
    from canvas_sync.source_build import validate_source_evidence
    fidelity_errors, newly_authored = validate_source_evidence(md_path, frontmatter, body)
    errors.extend(fidelity_errors)
    if "\u2014" in newly_authored:
        errors.append(f"{md_path}: contains em-dash; use hyphen, colon, or sentence break")

    return errors


def validate_guided_assignment(label: object, payload: dict, body: str | None = None) -> list[str]:
    errors = []
    if "require_sequential_progress" in payload and payload.get("type") != "module_header":
        errors.append(f"{label}: require_sequential_progress requires a module_header")
    if payload.get("page_presentation") and payload.get("type") not in {"page", "discussion"}:
        errors.append(f"{label}: page_presentation requires a page or discussion")
    mode = payload.get("delivery_mode")
    config = payload.get("guided_assignment")
    dojo = payload.get('dojo_submission')
    canonical_dojo = bool(payload.get('publish')) and (
        str(payload.get('slug', '')).startswith('dojo-lab-')
        or str(payload.get('title', '')).startswith('Dojo Lab:')
    )
    if canonical_dojo and not isinstance(dojo, dict):
        errors.append(f'{label}: published canonical Dojo assignments require dojo_submission')
    if mode != "guided_assignment":
        return errors + ([f"{label}: guided_assignment requires its delivery mode"] if config is not None else [])
    quiz_backed_assignment = (
        payload.get("type") == "quiz"
        and isinstance(config, dict)
        and config.get("presentation") == "interleaved"
        and config.get("feedback_protocol") == "brainstorm-list-v1"
    )
    walkthrough = config.get('presentation') == 'walkthrough' if isinstance(config, dict) else False
    permitted_submissions = {'text_entry', 'file_upload'} if walkthrough else {'text_entry'}
    if (payload.get("type") != "assignment" and not quiz_backed_assignment) or payload.get("submission_type") not in permitted_submissions:
        errors.append(f"{label}: guided_assignment requires an assignment with text_entry (or file_upload for walkthrough)")
    if not isinstance(config, dict):
        return errors + [f"{label}: guided_assignment requires configuration"]
    if payload.get("questions") or payload.get("ai_activity"):
        errors.append(f"{label}: guided_assignment cannot include native quiz or ai_activity questions")
    if isinstance(dojo, dict):
        from canvas_sync.guided_assignment import DOJO_TRANSCRIPT_TASK_ID, DOJO_TRANSCRIPT_TASK_PROMPT, load_dojo_transcript_prompt
        if (payload.get('type') != 'assignment' or payload.get('submission_type') != 'text_entry'
                or payload.get('completion_requirement') != 'must_submit' or mode != 'guided_assignment'):
            errors.append(f'{label}: dojo_submission requires assignment, text_entry, must_submit, and guided_assignment')
        tasks = config.get('tasks', [])
        valid_task = (isinstance(tasks, list) and len(tasks) == 1 and isinstance(tasks[0], dict)
                      and tasks[0].get('id') == DOJO_TRANSCRIPT_TASK_ID
                      and tasks[0].get('kind', 'response') == 'response'
                      and tasks[0].get('prompt') == DOJO_TRANSCRIPT_TASK_PROMPT)
        if not valid_task:
            errors.append(f'{label}: dojo_submission requires exactly one canonical dojo-transcript response task')
        try:
            load_dojo_transcript_prompt(dojo.get('prompt_version'))
        except ValueError as exc:
            errors.append(f'{label}: {exc}')
    ids = []
    for task in config.get("tasks", []) if isinstance(config.get("tasks"), list) else []:
        if not isinstance(task, dict):
            continue  # JSON Schema reports malformed task shapes.
        ids.append(task.get("id"))
        options, index = task.get("options"), task.get("correct_index")
        if task.get("kind") == "choice" and isinstance(options, list) and isinstance(index, int) and index >= len(options):
            errors.append(f"{label}: choice correct_index is outside options")
    if len(set(str(i) for i in ids)) != len(ids):
        errors.append(f"{label}: guided task IDs must be unique")
    tasks = config.get('tasks', [])
    if not isinstance(tasks, list):
        tasks = []
    if not walkthrough and any(isinstance(task, dict) and task.get('kind') == 'table' for task in tasks):
        errors.append(f'{label}: table tasks require walkthrough presentation')
    if walkthrough:
        writable_tasks = [task for task in tasks if isinstance(task, dict)
                          and not (task.get('kind') == 'table' and task.get('read_only') is True)]
        if writable_tasks and not config.get('feedback_endpoint') and not config.get('feedback_omission_reason'):
            errors.append(f'{label}: walkthrough response tasks require feedback_endpoint or feedback_omission_reason')
        if not payload.get('walkthrough_after'):
            errors.append(f'{label}: walkthrough requires walkthrough_after source artifact ID')
        if payload.get('type') != 'assignment':
            errors.append(f'{label}: walkthrough requires type assignment')
        if payload.get('submission_type') == 'file_upload' and not config.get('export_filename'):
            errors.append(f'{label}: file-upload walkthrough requires export_filename')
        if any(isinstance(task, dict) and task.get('kind') == 'table' for task in tasks) and not config.get('export_filename'):
            errors.append(f'{label}: table walkthrough requires export_filename')
        if config.get('feedback_protocol') and not config.get('feedback_endpoint'):
            errors.append(f'{label}: feedback_protocol requires feedback_endpoint')
        if (isinstance(config.get('feedback_endpoint'), str) and not config['feedback_endpoint'].rstrip('/').endswith(
                '/.netlify/functions/walkthrough-feedback')):
            errors.append(f'{label}: walkthrough feedback_endpoint must use the shared walkthrough-feedback route')
        if payload.get('walkthrough_after') == payload.get('artifact_id'):
            errors.append(f'{label}: walkthrough_after cannot refer to itself')
        for task in tasks if isinstance(tasks, list) else []:
            if not isinstance(task, dict):
                continue
            if task.get('kind') != 'table' and 'read_only' in task:
                errors.append(f'{label}: read_only applies only to table tasks')
            if (task in writable_tasks and task.get('feedback_enabled') is False
                    and not task.get('feedback_omission_reason')):
                errors.append(f'{label}: {task.get("id")}: disabled AI feedback requires feedback_omission_reason')
            if task.get('feedback_enabled') and not config.get('feedback_endpoint'):
                errors.append(f'{label}: task feedback requires feedback_endpoint')
            if task.get('kind') == 'group':
                fields = task.get('fields') or []
                field_ids = [field.get('id') for field in fields if isinstance(field, dict)]
                if len(field_ids) != len(set(field_ids)):
                    errors.append(f'{label}: group field IDs must be unique')
                labels = task.get('repeat_labels') or []
                if labels and len(labels) != task.get('repeat_count'):
                    errors.append(f'{label}: repeat_labels must match repeat_count')
                for field in fields:
                    if isinstance(field, dict) and field.get('kind') == 'select' and not field.get('options'):
                        errors.append(f'{label}: select field requires options')
            elif task.get('kind') == 'table':
                columns = task.get('columns') or []
                rows = task.get('rows') or []
                read_only = task.get('read_only') is True
                column_ids = [column.get('id') for column in columns if isinstance(column, dict)]
                row_ids = [row.get('id') for row in rows if isinstance(row, dict)]
                if len(column_ids) != len(set(column_ids)):
                    errors.append(f'{label}: table column IDs must be unique')
                if len(row_ids) != len(set(row_ids)):
                    errors.append(f'{label}: table row IDs must be unique')
                if any(isinstance(row, dict) and len(row.get('cells', [])) != len(columns) for row in rows):
                    errors.append(f'{label}: every table row must match the column count')
                has_response = any(isinstance(cell, dict) and cell.get('response') for row in rows if isinstance(row, dict)
                                   for cell in row.get('cells', []))
                if read_only and has_response:
                    errors.append(f'{label}: read-only table cannot contain response cells')
                if read_only and 'criteria' in task:
                    errors.append(f'{label}: read-only table cannot contain self-check criteria')
                if read_only and task.get('feedback_enabled'):
                    errors.append(f'{label}: read-only table cannot enable AI feedback')
                if not read_only and not has_response:
                    errors.append(f'{label}: table requires at least one response cell')
            elif task.get('kind') == 'choice':
                errors.append(f'{label}: walkthrough supports response, group, and table tasks only')
    if config.get('presentation') == 'reading' and config.get('feedback_endpoint'):
        errors.append(f'{label}: reading presentation does not support an AI feedback endpoint')
    if config.get('presentation') == 'compact':
        if (not isinstance(tasks, list) or len(tasks) != 1 or not isinstance(tasks[0], dict)
                or tasks[0].get('kind', 'response') != 'response' or not tasks[0].get('instruction_section')):
            errors.append(f'{label}: compact presentation requires one response task with instruction_section')
        if config.get('feedback_endpoint'):
            errors.append(f'{label}: compact presentation does not support an AI feedback endpoint')
    if (body is not None and isinstance(tasks, list)
            and all(isinstance(task, dict) and isinstance(task.get('id'), str) for task in tasks)
            and any('instruction_section' in task for task in tasks)):
        from canvas_sync.instruction_sections import partition_instruction_sections
        from canvas_sync.hosted_html import markdown_body_to_html
        try:
            partition_instruction_sections(markdown_body_to_html(body), tasks)
        except ValueError as exc:
            errors.append(f'{label}: {exc}')
    return errors


def validate_ai_activity_delivery(label: object, payload: dict) -> list[str]:
    errors: list[str] = []
    delivery_mode = payload.get("delivery_mode", "canvas_native")
    has_ai_activity = "ai_activity" in payload
    artifact_type = payload.get("type")

    if delivery_mode == "ai_activity":
        if artifact_type not in ("quiz", "discussion"):
            errors.append(f"{label}: delivery_mode ai_activity is only supported for quiz or discussion artifacts")
        if not has_ai_activity:
            errors.append(f"{label}: delivery_mode ai_activity requires ai_activity")
        if payload.get("submission_type") != "file_upload":
            errors.append(f"{label}: delivery_mode ai_activity requires submission_type file_upload")
        if payload.get("questions"):
            errors.append(
                f"{label}: delivery_mode ai_activity uses ai_activity.questions, not native Canvas questions"
            )
    elif has_ai_activity:
        errors.append(f"{label}: ai_activity requires delivery_mode ai_activity")

    return errors


def validate_manifest(manifest_path: Path) -> list[str]:
    try:
        with open(manifest_path) as f:
            manifest = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"{manifest_path}: {e}"]

    schema = load_schema("manifest")
    errors: list[str] = []
    try:
        jsonschema.validate(manifest, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{manifest_path}: {e.message} (at {'/'.join(str(p) for p in e.path)})")
    return errors


def validate_canvas_state(state_path: Path) -> list[str]:
    try:
        with open(state_path) as f:
            state = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"{state_path}: {e}"]

    schema = load_schema("canvas_state")
    errors: list[str] = []
    try:
        jsonschema.validate(state, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{state_path}: {e.message} (at {'/'.join(str(p) for p in e.path)})")

    for artifact_id, entry in state.get("artifacts", {}).items():
        if entry.get("artifact_id") != artifact_id:
            errors.append(
                f"{state_path}: artifact key {artifact_id!r} does not match "
                f"entry artifact_id {entry.get('artifact_id')!r}"
            )
    return errors


def validate_prd(prd_path: Path) -> list[str]:
    try:
        with open(prd_path) as f:
            prd = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return [f"{prd_path}: {e}"]

    schema = load_schema("prd")
    errors: list[str] = []
    try:
        jsonschema.validate(prd, schema)
    except jsonschema.ValidationError as e:
        errors.append(f"{prd_path}: {e.message} (at {'/'.join(str(p) for p in e.path)})")

    for index, item in enumerate(prd.get("items", []), start=1):
        item_label = f"{prd_path}: item {item.get('id', index)}"
        errors.extend(validate_ai_activity_delivery(item_label, item))

    # ID uniqueness
    ids = [item["id"] for item in prd.get("items", [])]
    if len(ids) != len(set(ids)):
        errors.append(f"{prd_path}: duplicate PRD item ids")

    return errors


def validate_homepage(homepage_path: Path) -> list[str]:
    if homepage_path.name != "homepage.yaml":
        return [f"{homepage_path}: homepage metadata file must be named homepage.yaml"]
    from canvas_sync.hosted_html import validate_homepage_metadata

    return validate_homepage_metadata(homepage_path.parent)


def discover_course_dirs() -> list[Path]:
    course_dirs: list[Path] = []
    for path in sorted(REPO_ROOT.iterdir()):
        if not path.is_dir():
            continue
        if not COURSE_KEY_RE.fullmatch(path.name):
            continue
        if (path / "sprints").is_dir() or (path / "manifests").is_dir():
            course_dirs.append(path)
    return course_dirs


def validate_all() -> list[str]:
    errors: list[str] = []
    artifact_ids: dict[str, Path] = {}

    for course_path in discover_course_dirs():
        md_pattern = str(course_path / "sprints" / "sprint-*" / "**" / "*.md")
        for md_file in glob.glob(md_pattern, recursive=True):
            md_path = Path(md_file)
            errors.extend(validate_artifact(md_path))
            try:
                frontmatter, _ = parse_frontmatter(md_path)
            except (ValueError, yaml.YAMLError):
                continue
            artifact_id = frontmatter.get("artifact_id")
            if not artifact_id:
                continue
            if artifact_id in artifact_ids:
                errors.append(
                    f"{md_path}: duplicate artifact_id {artifact_id!r}; "
                    f"already used by {artifact_ids[artifact_id]}"
                )
            else:
                artifact_ids[artifact_id] = md_path

        for manifest_file in glob.glob(str(course_path / "manifests" / "*.json")):
            errors.extend(validate_manifest(Path(manifest_file)))

        prd_path = course_path / "prd.json"
        if prd_path.exists():
            errors.extend(validate_prd(prd_path))

        homepage_path = course_path / "homepage.yaml"
        if homepage_path.exists():
            errors.extend(validate_homepage(homepage_path))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artifact", type=Path)
    group.add_argument("--manifest", type=Path)
    group.add_argument("--state", type=Path)
    group.add_argument("--prd", type=Path)
    group.add_argument("--homepage", type=Path)
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.artifact:
        errors = validate_artifact(args.artifact)
    elif args.manifest:
        errors = validate_manifest(args.manifest)
    elif args.state:
        errors = validate_canvas_state(args.state)
    elif args.prd:
        errors = validate_prd(args.prd)
    elif args.homepage:
        errors = validate_homepage(args.homepage)
    else:
        errors = validate_all()

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())

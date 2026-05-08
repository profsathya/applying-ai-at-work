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


def load_schema(name: str) -> dict:
    path = SCHEMA_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)


def parse_frontmatter(md_path: Path) -> tuple[dict, str]:
    """Split an MD file into (frontmatter_dict, body_str)."""
    content = md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        raise ValueError(f"{md_path}: missing YAML frontmatter")
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{md_path}: malformed frontmatter (no closing ---)")
    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return frontmatter, body


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

    # Em-dash check (Jeremy's stylistic preference enforced as hard rule)
    if "\u2014" in body or "\u2014" in str(frontmatter.get("title", "")):
        errors.append(f"{md_path}: contains em-dash; use hyphen, colon, or sentence break")

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

    # ID uniqueness
    ids = [item["id"] for item in prd.get("items", [])]
    if len(ids) != len(set(ids)):
        errors.append(f"{prd_path}: duplicate PRD item ids")

    return errors


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

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artifact", type=Path)
    group.add_argument("--manifest", type=Path)
    group.add_argument("--state", type=Path)
    group.add_argument("--prd", type=Path)
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

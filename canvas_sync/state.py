"""Canvas deployment state helpers.

The content branch keeps Markdown and static course config. GitOps publishing
can keep mutable Canvas IDs and publish hashes in a separate state checkout.
Legacy local workflows can still use the production manifest as the state file.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any

if os.name == "nt":
    import msvcrt
else:
    import fcntl

from canvas_sync.canvas_client import CanvasClient, CanvasError
from canvas_sync.schema import parse_frontmatter


def load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json_atomic(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp.replace(path)


@contextmanager
def file_lock(path: Path):
    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "w", encoding="utf-8") as lock_file:
        if os.name == "nt":
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_LOCK, 1)
        else:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                lock_file.seek(0)
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock_file, fcntl.LOCK_UN)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_hash_without_artifact_id(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return content_hash(path)
    output: list[str] = []
    in_frontmatter = True
    for index, line in enumerate(lines):
        if in_frontmatter and index > 0 and line.strip() == "---":
            in_frontmatter = False
        if in_frontmatter and line.startswith("artifact_id:"):
            continue
        output.append(line)
    return hashlib.sha256("".join(output).encode("utf-8")).hexdigest()


def course_dir_for_manifest(manifest_path: Path) -> Path:
    if manifest_path.parent.name != "manifests":
        raise ValueError(f"Manifest must live under <course>/manifests/: {manifest_path}")
    return manifest_path.parent.parent


def course_key_for_manifest(manifest_path: Path) -> str:
    return course_dir_for_manifest(manifest_path).name


def derive_artifact_id(rel_path: str) -> str:
    path = Path(rel_path).with_suffix("")
    return "-".join(path.parts).replace("_", "-")


def artifact_id_for_file(md_path: Path, repo_root: Path) -> str:
    rel_path = md_path.resolve().relative_to(repo_root).as_posix()
    frontmatter, _ = parse_frontmatter(md_path)
    return frontmatter.get("artifact_id") or derive_artifact_id(rel_path)


def state_path_for_manifest(manifest_path: Path, state_dir: Path, manifest: dict | None = None) -> Path:
    manifest_data = manifest or load_json(manifest_path)
    instance_name = manifest_data.get("instance", {}).get("name") or manifest_path.stem
    return state_dir / course_key_for_manifest(manifest_path) / f"{instance_name}.json"


def empty_state_from_manifest(manifest: dict) -> dict:
    return {
        "instance": dict(manifest.get("instance", {})),
        "last_sync": None,
        "artifacts": {},
    }


def state_from_manifest(manifest_path: Path, repo_root: Path) -> dict:
    manifest = load_json(manifest_path)
    state = {
        "instance": dict(manifest.get("instance", {})),
        "last_sync": manifest.get("last_sync"),
        "artifacts": {},
    }
    for rel_path, entry in sorted(manifest.get("artifacts", {}).items()):
        md_path = repo_root / rel_path
        artifact_id = derive_artifact_id(rel_path)
        if md_path.exists():
            try:
                artifact_id = artifact_id_for_file(md_path, repo_root)
            except Exception:
                artifact_id = derive_artifact_id(rel_path)
        state_entry = dict(entry)
        if md_path.exists() and state_entry.get("content_hash") == content_hash_without_artifact_id(md_path):
            state_entry["content_hash"] = content_hash(md_path)
        state_entry["artifact_id"] = artifact_id
        state_entry["local_path"] = rel_path
        state["artifacts"][artifact_id] = state_entry
    return state


@dataclass
class CanvasStateStore:
    manifest_path: Path
    repo_root: Path
    state_dir: Path | None = None

    def __post_init__(self) -> None:
        self.manifest_path = self.manifest_path.resolve()
        self.repo_root = self.repo_root.resolve()
        self.state_dir = self.state_dir.resolve() if self.state_dir else None

    @property
    def external(self) -> bool:
        return self.state_dir is not None

    def load_manifest(self) -> dict:
        return load_json(self.manifest_path)

    def state_path(self, manifest: dict | None = None) -> Path:
        if not self.state_dir:
            return self.manifest_path
        return state_path_for_manifest(self.manifest_path, self.state_dir, manifest)

    @contextmanager
    def locked(self):
        manifest = self.load_manifest()
        lock_path = self.state_path(manifest) if self.external else self.manifest_path
        with file_lock(lock_path):
            manifest = self.load_manifest()
            state_path = self.state_path(manifest)
            if self.external:
                if state_path.exists():
                    state = load_json(state_path)
                else:
                    state = empty_state_from_manifest(manifest)
            else:
                state = manifest
            yield manifest, state, state_path

    def save(self, state: dict, state_path: Path) -> None:
        save_json_atomic(state_path, state)


def artifact_entry_key(frontmatter: dict, rel_path: str, *, external_state: bool) -> str:
    if external_state:
        return frontmatter.get("artifact_id") or derive_artifact_id(rel_path)
    return rel_path


def entry_for_push(
    *,
    artifact_id: str,
    rel_path: str,
    artifact_type: str,
    canvas_id: int | None,
    canvas_page_url: str | None,
    canvas_module_id: int | None,
    hash_value: str,
    pushed_at: str,
    source_commit: str | None = None,
    canvas_fingerprint: str | None = None,
    external_state: bool,
) -> dict:
    entry = {
        "canvas_type": artifact_type,
        "canvas_id": canvas_id,
        "canvas_page_url": canvas_page_url,
        "canvas_module_id": canvas_module_id,
        "content_hash": hash_value,
        "last_pushed": pushed_at,
    }
    if external_state:
        entry["artifact_id"] = artifact_id
        entry["local_path"] = rel_path
        if source_commit:
            entry["source_commit"] = source_commit
        if canvas_fingerprint:
            entry["canvas_fingerprint"] = canvas_fingerprint
    return entry


def fetch_canvas_state(client: CanvasClient, artifact_entry: dict) -> dict | None:
    atype = artifact_entry.get("canvas_type")
    cid = artifact_entry.get("canvas_id")
    page_url = artifact_entry.get("canvas_page_url")

    try:
        if atype == "assignment":
            return client.get_assignment(cid)
        if atype == "page":
            return client.get_page(page_url)
        if atype == "discussion":
            return client.get_discussion(cid)
        if atype == "quiz":
            state = client.get_quiz(cid)
            state["questions"] = client.list_quiz_questions(cid)
            return state
        return None
    except CanvasError as exc:
        if exc.status == 404:
            return None
        raise


def canvas_snapshot(canvas_state: dict, atype: str) -> dict[str, Any]:
    points = canvas_state.get("points_possible")
    if canvas_state.get("assignment"):
        points = canvas_state["assignment"].get("points_possible", points)

    snapshot: dict[str, Any] = {
        "type": atype,
        "title": canvas_state.get("name") or canvas_state.get("title"),
        "body": (
            canvas_state.get("description")
            or canvas_state.get("body")
            or canvas_state.get("message")
            or ""
        ),
        "points": points,
        "published": canvas_state.get("published"),
    }
    if atype == "quiz":
        snapshot["questions"] = [
            {
                "question_text": q.get("question_text"),
                "question_type": q.get("question_type"),
                "points_possible": q.get("points_possible"),
                "answers": q.get("answers"),
            }
            for q in canvas_state.get("questions", [])
        ]
    return snapshot


def canvas_fingerprint(canvas_state: dict | None, atype: str) -> str | None:
    if canvas_state is None:
        return None
    canonical = json.dumps(canvas_snapshot(canvas_state, atype), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

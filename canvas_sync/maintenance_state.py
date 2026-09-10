"""Path-indexed maintenance view of legacy or external deployment state.

The external file remains authoritative when selected. Never merge its IDs with
stale legacy manifest IDs, or silently fall back when the selected file is absent.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from canvas_sync.schema import parse_frontmatter, validate_canvas_state
from canvas_sync.state import (
    artifact_id_for_file,
    check_state_instance,
    course_dir_for_manifest,
    file_lock,
    load_json,
    save_json_atomic,
    state_path_for_manifest,
)


class MaintenanceState:
    def __init__(
        self, manifest_path: Path, repo_root: Path, state_dir: Path | None = None
    ):
        self.manifest_path = manifest_path.resolve()
        self.repo_root = repo_root.resolve()
        self.config = load_json(self.manifest_path)
        self.external = state_dir is not None
        self.path = (
            state_path_for_manifest(
                self.manifest_path, state_dir.resolve(), self.config
            )
            if state_dir is not None
            else self.manifest_path
        )

    def load(self) -> dict:
        data = load_json(self.path)  # Missing external state is an error.
        course_dir = course_dir_for_manifest(self.manifest_path)
        current_paths = {}
        if self.external:
            errors = validate_canvas_state(self.path)
            if errors:
                raise ValueError("; ".join(errors))
            check_state_instance(data, self.config, self.path)
            for md_path in sorted(course_dir.glob("sprints/sprint-*/*.md")):
                fm, _ = parse_frontmatter(md_path)
                artifact_id = fm.get("artifact_id")
                if artifact_id in current_paths:
                    raise ValueError(f"Duplicate local artifact_id: {artifact_id}")
                if artifact_id:
                    current_paths[artifact_id] = md_path.relative_to(
                        self.repo_root
                    ).as_posix()

        artifacts = {}
        for key, original in data.get("artifacts", {}).items():
            entry = dict(original)
            rel_path = (
                current_paths.get(key, entry.get("local_path"))
                if self.external
                else key
            )
            md_path = (self.repo_root / rel_path).resolve()
            if not md_path.is_relative_to(course_dir / "sprints"):
                raise ValueError(
                    f"{self.path}: artifact path is outside this course: {rel_path}"
                )
            if rel_path in artifacts:
                raise ValueError(f"{self.path}: duplicate local path: {rel_path}")
            if self.external:
                entry["local_path"] = rel_path
                if (
                    md_path.exists()
                    and artifact_id_for_file(md_path, self.repo_root) != key
                ):
                    raise ValueError(
                        f"{rel_path}: local artifact_id does not match state key {key}"
                    )
            artifacts[rel_path] = entry
        self.original = data
        return {
            **self.config,
            "artifacts": artifacts,
            "last_sync": data.get("last_sync"),
        }

    def save(self, view: dict) -> None:
        if not self.external:
            save_json_atomic(self.path, view)
            return
        entries = {}
        for rel_path, original in view["artifacts"].items():
            entry = dict(original)
            artifact_id = entry.get("artifact_id") or artifact_id_for_file(
                self.repo_root / rel_path, self.repo_root
            )
            if artifact_id in entries:
                raise ValueError(f"Duplicate deployment artifact_id: {artifact_id}")
            entry.update(artifact_id=artifact_id, local_path=rel_path)
            entries[artifact_id] = entry
        save_json_atomic(
            self.path,
            {**self.original, "artifacts": entries, "last_sync": view.get("last_sync")},
        )

    @contextmanager
    def locked(self):
        with file_lock(self.path):
            yield self.load()

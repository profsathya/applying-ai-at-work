"""Structural Canvas-setting changes must be APPLIED, not just detected.

End-state assertions: the exact update payload carries due_at null on due
removal; module/position changes update the existing module item via the
module-items API; state records the new location only after the move
succeeded.
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from canvas_sync import push
from canvas_sync.state import state_path_for_manifest


@contextmanager
def chdir(path: Path):
    old_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


def write_assignment(
    path: Path,
    *,
    due: str | None = None,
    module: str = "Module A",
    position: int = 2,
    completion: str | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    due_line = f"due: \"{due}\"\n" if due else ""
    completion_line = f"completion_requirement: {completion}\n" if completion else ""
    path.write_text(
        f"""---
type: assignment
title: "Tuple Lab"
slug: tuple-lab
artifact_id: tuple-lab
sprint: 99
module: "{module}"
position: {position}
points: 10
submission_type: text_entry
publish: false
{due_line}{completion_line}---

# Tuple Lab

Assignment body.
""",
        encoding="utf-8",
    )


def write_manifest(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "instance": {
                    "name": "production",
                    "base_url": "https://example.instructure.com/",
                    "course_id": 12345,
                    "term": "Test Term",
                },
                "last_sync": None,
                "artifacts": {},
            }
        ),
        encoding="utf-8",
    )


def write_state(
    state_path: Path,
    *,
    module_id: int = 55,
    module_item_id: int | None = 9001,
    position: int | None = 2,
) -> None:
    entry = {
        "artifact_id": "tuple-lab",
        "local_path": "course1/sprints/sprint-99/tuple-lab.md",
        "canvas_type": "assignment",
        "canvas_id": 2001,
        "canvas_page_url": None,
        "canvas_module_id": module_id,
        "completion_requirement": "must_submit",
        "content_hash": "5" * 64,
    }
    if module_item_id is not None:
        entry["canvas_module_item_id"] = module_item_id
    if position is not None:
        entry["position"] = position
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "instance": {
                    "name": "production",
                    "base_url": "https://example.instructure.com/",
                    "course_id": 12345,
                    "term": "Test Term",
                },
                "last_sync": None,
                "artifacts": {"tuple-lab": entry},
            }
        ),
        encoding="utf-8",
    )


class StructuralClient:
    def __init__(self, *, fail_module_item_update: bool = False) -> None:
        self.assignment_payloads: list[dict] = []
        self.module_item_updates: list[tuple[int, int, dict]] = []
        self.fail_module_item_update = fail_module_item_update

    def update_assignment(self, assignment_id: int, payload: dict) -> dict:
        self.assignment_payloads.append(payload)
        return {"id": assignment_id, **payload}

    def get_assignment(self, assignment_id: int) -> dict:
        return {
            "id": assignment_id,
            "name": "Tuple Lab",
            "description": "",
            "points_possible": 10,
            "published": False,
            "submission_types": ["online_text_entry"],
        }

    def update_module_item(self, module_id: int, item_id: int, payload: dict) -> dict:
        if self.fail_module_item_update:
            raise RuntimeError("module item update rejected by canvas")
        self.module_item_updates.append((module_id, item_id, payload))
        return {"id": item_id, **payload}


class StructuralChangeTests(unittest.TestCase):
    def _run(
        self,
        tmp: str,
        *,
        due: str | None = None,
        module: str = "Module A",
        position: int = 2,
        completion: str | None = None,
        state_module_id: int = 55,
        state_module_item_id: int | None = 9001,
        state_position: int | None = 2,
        resolved_module_id: int = 55,
        client: StructuralClient | None = None,
    ):
        repo_root = Path(tmp).resolve()
        md_path = repo_root / "course1" / "sprints" / "sprint-99" / "tuple-lab.md"
        manifest_path = repo_root / "course1" / "manifests" / "production.json"
        state_dir = repo_root / ".canvas-state"
        write_assignment(md_path, due=due, module=module, position=position, completion=completion)
        write_manifest(manifest_path)
        manifest = {"instance": {"name": "production"}}
        state_path = state_dir / "course1" / "production.json"
        write_state(
            state_path,
            module_id=state_module_id,
            module_item_id=state_module_item_id,
            position=state_position,
        )
        client = client or StructuralClient()

        with chdir(repo_root):
            with patch.object(push.CanvasClient, "from_env", return_value=client):
                with patch.object(
                    push, "resolve_or_create_module", return_value=resolved_module_id
                ):
                    result = push.push_artifact(md_path, manifest_path, state_dir=state_dir)
        entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-lab"]
        return result, client, entry, state_path

    def test_due_removal_sends_explicit_null(self) -> None:
        """The update payload must carry due_at: null, not omit the field."""
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, _entry, _sp = self._run(tmp, due=None)
        self.assertEqual(len(client.assignment_payloads), 1)
        payload = client.assignment_payloads[0]
        self.assertIn("due_at", payload)
        self.assertIsNone(payload["due_at"])

    def test_due_set_sends_value(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, _entry, _sp = self._run(tmp, due="2026-10-15T23:59:00Z")
        self.assertEqual(client.assignment_payloads[0]["due_at"], "2026-10-15T23:59:00Z")

    def test_module_change_moves_existing_item_and_updates_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, entry, _sp = self._run(
                tmp, module="Module B", resolved_module_id=66
            )
        # The move call targets the item's CURRENT module and carries the new
        # module_id plus the declared position.
        self.assertEqual(
            client.module_item_updates,
            [(55, 9001, {"module_id": 66, "position": 2})],
        )
        self.assertEqual(entry["canvas_module_id"], 66)

    def test_position_change_repositions_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, entry, _sp = self._run(tmp, position=5)
        self.assertEqual(
            client.module_item_updates,
            [(55, 9001, {"position": 5})],
        )
        self.assertEqual(entry["position"], 5)

    def test_move_happens_before_completion_update_at_new_module(self) -> None:
        """A module change plus a completion change: the item moves first, then
        the completion update addresses the module the item now lives in."""
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, entry, _sp = self._run(
                tmp, module="Module B", resolved_module_id=66, completion="min_score"
            )
        self.assertEqual(
            client.module_item_updates,
            [
                (55, 9001, {"module_id": 66, "position": 2}),
                (66, 9001, {"completion_requirement": {"type": "min_score", "min_score": 10}}),
            ],
        )
        self.assertEqual(entry["canvas_module_id"], 66)

    def test_unchanged_module_and_position_move_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _result, client, _entry, _sp = self._run(tmp)
        self.assertEqual(client.module_item_updates, [])

    def test_failed_move_keeps_state_at_old_location(self) -> None:
        client = StructuralClient(fail_module_item_update=True)
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):
                self._run(tmp, module="Module B", resolved_module_id=66, client=client)
            repo_root = Path(tmp).resolve()
            state_path = repo_root / ".canvas-state" / "course1" / "production.json"
            entry = json.loads(state_path.read_text(encoding="utf-8"))["artifacts"]["tuple-lab"]
        # State still shows the old, true location and the old content hash:
        # the failed item republishes fully on retry.
        self.assertEqual(entry["canvas_module_id"], 55)
        self.assertEqual(entry["content_hash"], "5" * 64)

    def test_module_change_without_item_id_warns_and_keeps_old_module(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, client, entry, _sp = self._run(
                tmp,
                module="Module B",
                resolved_module_id=66,
                state_module_item_id=None,
                state_position=None,
            )
        self.assertEqual(client.module_item_updates, [])
        self.assertIn(push.MODULE_MOVE_WARNING, result.get("warnings", []))
        self.assertEqual(entry["canvas_module_id"], 55)


if __name__ == "__main__":
    unittest.main()

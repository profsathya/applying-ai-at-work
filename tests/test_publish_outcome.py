"""Tests for canvas_sync/publish_outcome.py (workflow gating + truth helpers)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from canvas_sync.publish_outcome import (  # noqa: E402
    HOSTED_DEPLOY_FAILED,
    demote_content_updates,
    revert_entries,
    summarize,
)


def result(*, published=0, failed=0, drifted=0, hosted=False, content_updates=0) -> dict:
    pub = [
        {"file": f"f{i}.md", "artifact_id": f"a{i}", "action": "updated"}
        for i in range(published)
    ]
    pub += [
        {"file": f"c{i}.md", "artifact_id": f"c{i}", "action": "content_update"}
        for i in range(content_updates)
    ]
    return {
        "state": "/work/canvas-state/course1/production.json",
        "published": pub,
        "failed": [{"file": f"x{i}.md", "artifact_id": f"x{i}", "error": "boom"} for i in range(failed)],
        "drifted": [{"file": f"d{i}.md", "artifact_id": f"d{i}", "reason": "drift"} for i in range(drifted)],
        "hosted": {"ok": True} if hosted else None,
    }


class SummarizeTests(unittest.TestCase):
    def test_fully_failed_run_commits_nothing(self) -> None:
        s = summarize([result(failed=2)])
        self.assertFalse(s["commit_state"])
        self.assertFalse(s["hosted_commit"])
        self.assertEqual(s["failed"], 2)

    def test_partial_success_commits_per_item(self) -> None:
        s = summarize([result(published=1, drifted=1)])
        self.assertTrue(s["commit_state"])
        self.assertTrue(s["hosted_commit"])
        self.assertFalse(s["clean"])

    def test_clean_housekeeping_run_commits(self) -> None:
        s = summarize([result(hosted=True)])
        self.assertTrue(s["clean"])
        self.assertTrue(s["commit_state"])
        self.assertTrue(s["hosted_commit"])

    def test_drifted_counts_as_failed(self) -> None:
        s = summarize([result(drifted=3)])
        self.assertEqual(s["failed"], 3)
        self.assertFalse(s["commit_state"])


class DemoteContentUpdatesTests(unittest.TestCase):
    def test_content_updates_move_to_failed_and_map_state(self) -> None:
        results = [result(published=1, content_updates=2)]
        adjusted, demoted = demote_content_updates(results)
        self.assertEqual(len(adjusted[0]["published"]), 1)
        self.assertEqual(adjusted[0]["published"][0]["action"], "updated")
        errors = [f["error"] for f in adjusted[0]["failed"]]
        self.assertEqual(errors, [HOSTED_DEPLOY_FAILED] * 2)
        self.assertEqual(
            demoted, {"/work/canvas-state/course1/production.json": ["c0", "c1"]}
        )

    def test_no_content_updates_is_noop(self) -> None:
        results = [result(published=2)]
        adjusted, demoted = demote_content_updates(results)
        self.assertEqual(len(adjusted[0]["published"]), 2)
        self.assertEqual(demoted, {})


class RevertEntriesTests(unittest.TestCase):
    def test_entry_restored_from_baseline(self) -> None:
        current = {"artifacts": {"a": {"content_hash": "new"}, "b": {"content_hash": "keep"}}}
        baseline = {"artifacts": {"a": {"content_hash": "old"}}}
        out = revert_entries(current, baseline, ["a"])
        self.assertEqual(out["artifacts"]["a"], {"content_hash": "old"})
        self.assertEqual(out["artifacts"]["b"], {"content_hash": "keep"})

    def test_entry_absent_from_baseline_is_removed(self) -> None:
        current = {"artifacts": {"new-item": {"content_hash": "new"}}}
        out = revert_entries(current, {"artifacts": {}}, ["new-item"])
        self.assertNotIn("new-item", out["artifacts"])


if __name__ == "__main__":
    unittest.main()

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
    HOSTED_DEPLOY_FAILED_CANVAS,
    demote_hosted_publishes,
    revert_entries,
    summarize,
    summarize_report,
)


def result(
    *,
    published=0,
    failed=0,
    drifted=0,
    hosted=False,
    content_updates=0,
    hosted_updates=0,
    hosted_creates=0,
    provisional=0,
) -> dict:
    pub = [
        {"file": f"f{i}.md", "artifact_id": f"a{i}", "action": "updated"}
        for i in range(published)
    ]
    pub += [
        {"file": f"c{i}.md", "artifact_id": f"c{i}", "action": "content_update"}
        for i in range(content_updates)
    ]
    pub += [
        {"file": f"h{i}.md", "artifact_id": f"h{i}", "action": "updated", "hosted_url": "https://x/h.html"}
        for i in range(hosted_updates)
    ]
    pub += [
        {"file": f"n{i}.md", "artifact_id": f"n{i}", "action": "created", "hosted_url": "https://x/n.html"}
        for i in range(hosted_creates)
    ]
    return {
        "state": "/work/canvas-state/course1/production.json",
        "published": pub,
        "failed": [{"file": f"x{i}.md", "artifact_id": f"x{i}", "error": "boom"} for i in range(failed)],
        "drifted": [{"file": f"d{i}.md", "artifact_id": f"d{i}", "reason": "drift"} for i in range(drifted)],
        "provisional": [
            {"file": f"p{i}.md", "artifact_id": f"p{i}", "reason": "identity recorded"}
            for i in range(provisional)
        ],
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

    def test_provisional_identity_forces_state_commit(self) -> None:
        """A fully-failed run still commits state when an identity was recorded."""
        s = summarize([result(failed=1, provisional=1)])
        self.assertFalse(s["clean"])
        self.assertTrue(s["commit_state"])
        self.assertFalse(s["hosted_commit"])


class SummarizeReportTests(unittest.TestCase):
    """An empty or incomplete report is never treated as a clean run."""

    def test_unreadable_report_is_a_failure(self) -> None:
        s = summarize_report(None, 1)
        self.assertFalse(s["completed"])
        self.assertFalse(s["clean"])
        self.assertFalse(s["commit_state"])
        self.assertFalse(s["hosted_commit"])
        self.assertGreaterEqual(s["failed"], 1)

    def test_report_without_completed_marker_is_a_failure(self) -> None:
        s = summarize_report({"results": [result(published=2)]}, 1)
        self.assertFalse(s["completed"])
        self.assertFalse(s["hosted_commit"])

    def test_missing_manifest_results_is_a_failure(self) -> None:
        s = summarize_report({"results": [result(published=1)], "completed": True}, 2)
        self.assertFalse(s["completed"])
        self.assertGreaterEqual(s["failed"], 1)
        self.assertFalse(s["hosted_commit"])

    def test_complete_report_matches_summarize(self) -> None:
        s = summarize_report({"results": [result(published=1)], "completed": True}, 1)
        self.assertTrue(s["completed"])
        self.assertTrue(s["commit_state"])
        self.assertTrue(s["hosted_commit"])

    def test_incomplete_report_still_commits_provisional_identities(self) -> None:
        """The duplicate-prevention invariant survives a crashed run."""
        s = summarize_report(
            {"results": [result(failed=1, provisional=1)], "completed": False}, 1
        )
        self.assertFalse(s["completed"])
        self.assertTrue(s["commit_state"])
        self.assertFalse(s["hosted_commit"])


class DemoteHostedPublishesTests(unittest.TestCase):
    def test_content_updates_move_to_failed_and_map_state(self) -> None:
        results = [result(published=1, content_updates=2)]
        adjusted, demoted = demote_hosted_publishes(results)
        self.assertEqual(len(adjusted[0]["published"]), 1)
        self.assertEqual(adjusted[0]["published"][0]["action"], "updated")
        errors = [f["error"] for f in adjusted[0]["failed"]]
        self.assertEqual(errors, [HOSTED_DEPLOY_FAILED] * 2)
        self.assertEqual(
            demoted, {"/work/canvas-state/course1/production.json": ["c0", "c1"]}
        )

    def test_hosted_canvas_writes_demote_in_report_only(self) -> None:
        """Created/updated hosted items demote without state revert; created
        items keep their new identity via a provisional annotation."""
        results = [result(hosted_updates=1, hosted_creates=1)]
        adjusted, demoted = demote_hosted_publishes(results)
        self.assertEqual(adjusted[0]["published"], [])
        errors = [f["error"] for f in adjusted[0]["failed"]]
        self.assertEqual(errors, [HOSTED_DEPLOY_FAILED_CANVAS] * 2)
        # No state revert for real Canvas writes.
        self.assertEqual(demoted, {})
        # The created item's identity is preserved through commit gating.
        provisional_ids = [p["artifact_id"] for p in adjusted[0]["provisional"]]
        self.assertEqual(provisional_ids, ["n0"])
        self.assertTrue(summarize(adjusted)["commit_state"])

    def test_non_hosted_items_stay_published(self) -> None:
        results = [result(published=2)]
        adjusted, demoted = demote_hosted_publishes(results)
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

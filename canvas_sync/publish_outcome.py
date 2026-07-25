"""Pure helpers for interpreting a publish run's results.

Used by the Publish Canvas workflow (and unit tests) so the gating logic that
decides what gets committed, and how the run is reported, lives in tested
Python instead of inline YAML.
"""

from __future__ import annotations

HOSTED_DEPLOY_FAILED = "hosted deploy failed - content not live"


def summarize(results: list[dict]) -> dict:
    """Counts and commit gates for a publish run.

    - ``commit_state``: canvas-state may be committed when at least one
      artifact actually published, or the run was fully clean (housekeeping
      only). Fully-failed runs commit nothing.
    - ``hosted_commit``: hosted output may be committed per-item; blocked
      artifacts' files are already restored to baseline by publish_changed.
    """
    published = sum(len(r.get("published", [])) for r in results)
    failed = sum(len(r.get("failed", [])) for r in results)
    drifted = sum(len(r.get("drifted", [])) for r in results)
    hosted_ok = any(r.get("hosted") for r in results)
    clean = failed == 0 and drifted == 0
    return {
        "published": published,
        "failed": failed + drifted,
        "hosted_ok": hosted_ok,
        "clean": clean,
        "commit_state": published > 0 or clean,
        "hosted_commit": published > 0 or hosted_ok or clean,
    }


def demote_content_updates(
    results: list[dict], reason: str = HOSTED_DEPLOY_FAILED
) -> tuple[list[dict], dict[str, list[str]]]:
    """Move published content-only items into failed when hosted deploy failed.

    A content_update item's change lives only on its hosted page; when the
    Common Curriculum push failed, the item is not live and must not be
    reported or recorded as published. Returns the adjusted results plus a
    map of state-file path -> artifact ids whose state entries must be
    reverted to their pre-run baseline.
    """
    demoted: dict[str, list[str]] = {}
    for result in results:
        kept: list[dict] = []
        for item in result.get("published", []):
            if item.get("action") == "content_update":
                result.setdefault("failed", []).append(
                    {
                        "file": item.get("file"),
                        "artifact_id": item.get("artifact_id"),
                        "error": reason,
                    }
                )
                demoted.setdefault(str(result.get("state", "")), []).append(
                    item.get("artifact_id")
                )
            else:
                kept.append(item)
        result["published"] = kept
    return results, demoted


def revert_entries(
    current_state: dict, baseline_state: dict, artifact_ids: list[str]
) -> dict:
    """Restore the given artifacts' state entries from the baseline state.

    Entries absent from the baseline are removed entirely, so a failed hosted
    deploy leaves no record that the item was published.
    """
    artifacts = current_state.setdefault("artifacts", {})
    baseline = baseline_state.get("artifacts", {})
    for artifact_id in artifact_ids:
        if not artifact_id:
            continue
        if artifact_id in baseline:
            artifacts[artifact_id] = baseline[artifact_id]
        else:
            artifacts.pop(artifact_id, None)
    return current_state

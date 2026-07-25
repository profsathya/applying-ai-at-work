"""Pure helpers for interpreting a publish run's results.

Used by the Publish Canvas workflow (and unit tests) so the gating logic that
decides what gets committed, and how the run is reported, lives in tested
Python instead of inline YAML.
"""

from __future__ import annotations

HOSTED_DEPLOY_FAILED = "hosted deploy failed - content not live"
HOSTED_DEPLOY_FAILED_CANVAS = (
    "hosted deploy failed - canvas object updated but hosted page not deployed"
)
PROVISIONAL_REASON = (
    "canvas identity recorded; state must be committed so the retry updates "
    "instead of duplicating"
)


def summarize(results: list[dict]) -> dict:
    """Counts and commit gates for a publish run.

    - ``commit_state``: canvas-state may be committed when at least one
      artifact actually published, the run was fully clean (housekeeping
      only), or a failed item recorded a provisional Canvas identity that a
      retry needs to avoid creating a duplicate object. Fully-failed runs with
      no recorded identities commit nothing.
    - ``hosted_commit``: hosted output may be committed per-item; blocked
      artifacts' files are already restored to baseline by publish_changed.
    """
    published = sum(len(r.get("published", [])) for r in results)
    failed = sum(len(r.get("failed", [])) for r in results)
    drifted = sum(len(r.get("drifted", [])) for r in results)
    provisional = sum(len(r.get("provisional", [])) for r in results)
    hosted_ok = any(r.get("hosted") for r in results)
    clean = failed == 0 and drifted == 0
    return {
        "published": published,
        "failed": failed + drifted,
        "provisional": provisional,
        "hosted_ok": hosted_ok,
        "clean": clean,
        "commit_state": published > 0 or clean or provisional > 0,
        "hosted_commit": published > 0 or hosted_ok or clean,
    }


def demote_hosted_publishes(
    results: list[dict],
) -> tuple[list[dict], dict[str, list[str]]]:
    """Demote hosted items from published when the hosted deploy failed.

    Every hosted artifact's learner-facing content lives on its hosted page,
    so when the Common Curriculum push failed nothing hosted is actually live:

    - content_update items are demoted AND their state entries queued for
      revert (returned map of state-file path -> artifact ids); nothing
      touched Canvas, so the pre-run baseline is the whole truth.
    - created/updated hosted items are demoted in the REPORT only: their
      Canvas write really happened, so state is kept. A created item is also
      annotated under "provisional" so commit gating preserves its new Canvas
      identity for a safe retry. The next clean run re-renders and deploys the
      hosted pages.
    - items with no hosted output stay published untouched.
    """
    demoted: dict[str, list[str]] = {}
    for result in results:
        kept: list[dict] = []
        for item in result.get("published", []):
            action = item.get("action")
            if action == "content_update":
                result.setdefault("failed", []).append(
                    {
                        "file": item.get("file"),
                        "artifact_id": item.get("artifact_id"),
                        "error": HOSTED_DEPLOY_FAILED,
                    }
                )
                demoted.setdefault(str(result.get("state", "")), []).append(
                    item.get("artifact_id")
                )
            elif item.get("hosted_url"):
                result.setdefault("failed", []).append(
                    {
                        "file": item.get("file"),
                        "artifact_id": item.get("artifact_id"),
                        "error": HOSTED_DEPLOY_FAILED_CANVAS,
                    }
                )
                if action == "created":
                    result.setdefault("provisional", []).append(
                        {
                            "file": item.get("file"),
                            "artifact_id": item.get("artifact_id"),
                            "reason": PROVISIONAL_REASON,
                        }
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

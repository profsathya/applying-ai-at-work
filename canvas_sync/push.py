"""
Push one MD artifact to canvas.

Reads the MD file, extracts frontmatter, checks deployment state for an
existing canvas_id, then either creates or updates the artifact via the Canvas
API. By default this keeps legacy manifest-backed state. In GitOps mode,
--state-dir writes mutable Canvas IDs and publish hashes outside the content
branch.

Usage:
  python canvas_sync/push.py --file <md_path> --manifest <manifest_path>

Exit codes:
  0 = success (prints JSON to stdout with canvas_id, canvas_module_id, action)
  1 = hard failure
  2 = validation failure
  3 = canvas API error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.canvas_client import CanvasClient, CanvasError, resolve_or_create_module
from canvas_sync.completion import (
    completion_requirement_for,
    completion_requirement_state_value,
)
from canvas_sync.instance_guard import check_env_matches_instance
from canvas_sync.hosted_html import (
    artifact_hosted_info,
    discover_artifact_files as discover_hosted_artifact_files,
    iframe_shell,
    render_hosted_artifact,
    render_hosted_files,
)
from canvas_sync.schema import parse_frontmatter, validate_artifact
from canvas_sync.state import (
    CanvasStateStore,
    artifact_entry_key,
    canvas_fingerprint,
    content_hash,
    course_dir_for_manifest,
    derive_artifact_id,
    entry_for_push,
    fetch_canvas_state,
    utc_now,
)


def md_body_to_canvas_html(body: str) -> str:
    """
    Convert canvas-agnostic markdown to canvas-compatible HTML.

    Canvas accepts HTML in assignment descriptions, page bodies, discussion
    messages, and quiz descriptions. We use the 'markdown' library with safe
    defaults.
    """
    import markdown

    return markdown.markdown(
        body,
        extensions=["extra", "sane_lists", "smarty", "toc"],
        output_format="html5",
    )


def validate_artifact_manifest_pair(md_path: Path, manifest_path: Path) -> None:
    course_dir = course_dir_for_manifest(manifest_path)
    sprint_dir = course_dir / "sprints"
    try:
        md_path.relative_to(sprint_dir)
    except ValueError as exc:
        raise ValueError(
            f"Artifact {md_path} must live under {sprint_dir} for manifest {manifest_path}"
        ) from exc


CANVAS_SUBMISSION_TYPE_MAP = {
    "text_entry": "online_text_entry",
    "file_upload": "online_upload",
    "online_quiz": "online_quiz",
    "discussion_topic": "discussion_topic",
    "none": "none",
    "on_paper": "on_paper",
    "media_recording": "media_recording",
    "online_url": "online_url",
    "external_tool": "external_tool",
}


def delivery_mode_for(frontmatter: dict) -> str:
    return frontmatter.get("delivery_mode", "canvas_native")


def is_ai_activity_delivery(frontmatter: dict) -> bool:
    return delivery_mode_for(frontmatter) == "ai_activity"


def canvas_type_for(frontmatter: dict) -> str:
    if is_ai_activity_delivery(frontmatter):
        return "assignment"
    return frontmatter["type"]


def frontmatter_for_canvas_push(frontmatter: dict) -> dict:
    if not is_ai_activity_delivery(frontmatter):
        return frontmatter
    canvas_frontmatter = dict(frontmatter)
    canvas_frontmatter["submission_type"] = "file_upload"
    return canvas_frontmatter


def guard_canvas_type_migration(
    *,
    rel_path: str,
    existing: dict,
    canvas_artifact_type: str,
    source_type: str,
    delivery_mode: str,
) -> None:
    existing_canvas_type = existing.get("canvas_type")
    if not existing_canvas_type or existing_canvas_type == canvas_artifact_type:
        return

    raise ValueError(
        f"{rel_path}: existing Canvas state is {existing_canvas_type!r}, but this artifact now "
        f"publishes as {canvas_artifact_type!r} (source type {source_type!r}, delivery mode "
        f"{delivery_mode!r}). Use the remove-canvas workflow to dry-run and confirm removal of "
        "the existing Canvas object, then publish again so Canvas can create the new assignment shell."
    )


def canvas_payload_matches_live(
    *,
    md_path: Path,
    manifest_path: Path,
    manifest: dict,
    canvas_fm: dict,
    canvas_artifact_type: str,
    existing: dict,
    live_state: dict,
    completion_requirement: dict | None,
) -> bool:
    """True when publishing would leave the Canvas object unchanged.

    For hosted courses the Canvas body is only the iframe shell, so a
    body-text-only edit keeps the whole Canvas payload identical: same shell,
    same title, same points, same published flag, same due date, same module
    completion requirement. In that case the Canvas API write can be skipped
    and the hosted page alone carries the change.
    """
    # Imported here, not at module level: hydrate_state pulls in
    # inspect_canvas, which imports back from this module.
    from canvas_sync.hydrate_state import hosted_canvas_drift

    if hosted_canvas_drift(md_path, manifest_path, manifest, live_state, canvas_artifact_type):
        return False
    if live_state.get("published") != canvas_fm.get("publish", True):
        return False
    if canvas_fm.get("due"):
        live_due = live_state.get("due_at")
        if live_state.get("assignment"):
            live_due = live_state["assignment"].get("due_at", live_due)
        if live_due != canvas_fm["due"]:
            return False
    if completion_requirement_state_value(completion_requirement) != existing.get(
        "completion_requirement"
    ):
        return False
    if canvas_artifact_type == "assignment":
        submission_type = canvas_fm.get("submission_type", "text_entry")
        expected_submission = CANVAS_SUBMISSION_TYPE_MAP.get(submission_type, submission_type)
        if list(live_state.get("submission_types") or []) != [expected_submission]:
            return False
    return True


def push_assignment(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    submission_type = fm.get("submission_type", "text_entry")
    canvas_submission_type = CANVAS_SUBMISSION_TYPE_MAP.get(submission_type, submission_type)
    payload = {
        "name": fm["title"],
        "description": html,
        "points_possible": fm.get("points"),
        "submission_types": [canvas_submission_type],
        "published": fm.get("publish", True),
    }
    if fm.get("due"):
        payload["due_at"] = fm["due"]

    if existing_id:
        return client.update_assignment(existing_id, payload)
    return client.create_assignment(payload)


def push_page(client: CanvasClient, fm: dict, html: str, existing_url: str | None) -> dict:
    payload = {
        "title": fm["title"],
        "body": html,
        "published": fm.get("publish", True),
    }
    if existing_url:
        return client.update_page(existing_url, payload)
    return client.create_page(payload)


def push_discussion(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    payload = {
        "title": fm["title"],
        "message": html,
        "discussion_type": "threaded",
        "published": fm.get("publish", True),
    }
    if fm.get("points") is not None:
        payload["assignment"] = {
            "points_possible": fm["points"],
            "due_at": fm.get("due"),
        }
    if existing_id:
        return client.update_discussion(existing_id, payload)
    return client.create_discussion(payload)


def push_quiz(client: CanvasClient, fm: dict, html: str, existing_id: int | None) -> dict:
    payload = {
        "title": fm["title"],
        "description": html,
        "quiz_type": "assignment",
        "points_possible": fm.get("points"),
        "published": fm.get("publish", True),
    }
    if fm.get("due"):
        payload["due_at"] = fm["due"]

    if existing_id:
        result = client.update_quiz(existing_id, payload)
    else:
        result = client.create_quiz(payload)

    quiz_id = result["id"]

    # Wipe existing questions so an update replaces rather than appends.
    if existing_id:
        for q in client.list_quiz_questions(quiz_id):
            client.delete_quiz_question(quiz_id, q["id"])

    question_type_map = {
        "multiple_choice": "multiple_choice_question",
        "true_false": "true_false_question",
        "short_answer": "short_answer_question",
        "essay": "essay_question",
    }

    for q in fm.get("questions", []):
        q_type = q.get("type", "short_answer")
        canvas_q_type = question_type_map.get(q_type, q_type)
        question_payload = {
            "question_name": q.get("prompt", "")[:50],
            "question_text": q.get("prompt", ""),
            "question_type": canvas_q_type,
            "points_possible": q.get("points", 1),
        }
        if q_type in ("multiple_choice", "true_false"):
            question_payload["answers"] = [
                {"answer_text": a["text"], "answer_weight": 100 if a.get("correct") else 0}
                for a in q.get("answers", [])
            ]
        client.add_quiz_question(quiz_id, question_payload)

    return result


def push_artifact(
    md_path: Path,
    manifest_path: Path,
    state_dir: Path | None = None,
    hosted_output_dir: Path | None = None,
) -> dict:
    repo_root = Path.cwd().resolve()
    md_path = md_path.resolve()
    manifest_path = manifest_path.resolve()
    validate_artifact_manifest_pair(md_path, manifest_path)

    # Validate first
    errors = validate_artifact(md_path)
    if errors:
        raise ValueError(f"Validation failed: {errors}")

    fm, body = parse_frontmatter(md_path)
    html = md_body_to_canvas_html(body)
    rel_path = str(md_path.relative_to(repo_root))
    artifact_id = fm.get("artifact_id") or derive_artifact_id(rel_path)
    artifact_type = fm["type"]
    delivery_mode = delivery_mode_for(fm)
    canvas_artifact_type = canvas_type_for(fm)
    canvas_fm = frontmatter_for_canvas_push(fm)
    completion_requirement = completion_requirement_for(fm, canvas_artifact_type)

    store = CanvasStateStore(manifest_path=manifest_path, repo_root=repo_root, state_dir=state_dir)
    with store.locked() as (manifest, deployment_state, state_path):
        manifest_course_id = manifest.get("instance", {}).get("course_id") or 0
        if not manifest_course_id:
            raise ValueError(
                f"{manifest_path}: manifest instance.course_id is required and must be greater than zero"
            )
        course_id = int(manifest_course_id)

        # Guardrail: refuse to run when the environment's CANVAS_API_URL points
        # at a different Canvas instance than the selected profile. No-op when
        # they match (the current CTI/production case), so behavior is
        # unchanged there. Prevents pointing one institution's token/URL at
        # another institution's profile (the silent 401).
        check_env_matches_instance(manifest, manifest_label=str(manifest_path))

        client = CanvasClient.from_env(course_id=course_id)

        # Look up existing canvas entry for this file
        artifacts = deployment_state.setdefault("artifacts", {})
        state_key = artifact_entry_key(fm, rel_path, external_state=store.external)
        existing = artifacts.get(state_key, {})
        existing_id = existing.get("canvas_id")
        existing_page_url = existing.get("canvas_page_url")
        guard_canvas_type_migration(
            rel_path=rel_path,
            existing=existing,
            canvas_artifact_type=canvas_artifact_type,
            source_type=artifact_type,
            delivery_mode=delivery_mode,
        )

        hosted_info = artifact_hosted_info(md_path, manifest_path, manifest, fm)
        if is_ai_activity_delivery(fm) and not hosted_info["enabled"]:
            raise ValueError(f"{rel_path}: delivery_mode ai_activity requires hosted_html.enabled")
        if hosted_info["enabled"] and artifact_type != "module_header":
            html = iframe_shell(hosted_info["hosted_url"], fm["title"])

        action = "updated" if (existing_id or existing_page_url) else "created"

        # Content-only fast path: when the hosted iframe design means the
        # Canvas-side payload is identical (only hosted body text changed),
        # regenerate the hosted HTML and record state without any Canvas API
        # write. Quizzes are excluded because their native questions are not
        # covered by the hosted payload comparison. Requires hosted_output_dir
        # so the change always lands somewhere.
        if (
            action == "updated"
            and hosted_output_dir is not None
            and hosted_info["enabled"]
            and artifact_type != "module_header"
            and canvas_artifact_type != "quiz"
        ):
            live_state = fetch_canvas_state(client, existing)
            if live_state is not None and canvas_payload_matches_live(
                md_path=md_path,
                manifest_path=manifest_path,
                manifest=manifest,
                canvas_fm=canvas_fm,
                canvas_artifact_type=canvas_artifact_type,
                existing=existing,
                live_state=live_state,
                completion_requirement=completion_requirement,
            ):
                pushed_at = utc_now()
                entry = dict(existing)
                entry["content_hash"] = content_hash(md_path)
                entry["last_pushed"] = pushed_at
                entry["hosted_path"] = hosted_info["hosted_path"]
                entry["hosted_url"] = hosted_info["hosted_url"]
                if store.external:
                    fingerprint = canvas_fingerprint(live_state, canvas_artifact_type)
                    if fingerprint:
                        entry["canvas_fingerprint"] = fingerprint
                artifacts[state_key] = entry
                hosted_result = render_hosted_artifact(
                    md_path,
                    manifest_path,
                    hosted_output_dir,
                    manifest=manifest,
                    state=deployment_state,
                )
                entry["hosted_hash"] = hosted_result["hosted_hash"]
                entry["hosted_last_rendered"] = pushed_at
                render_hosted_files(
                    manifest_path,
                    hosted_output_dir,
                    discover_hosted_artifact_files(manifest_path),
                    manifest=manifest,
                    state=deployment_state,
                )
                deployment_state["last_sync"] = pushed_at
                store.save(deployment_state, state_path)
                return {
                    "action": "content_update",
                    "note": "content update - live via hosted page",
                    "file": rel_path,
                    "artifact_id": artifact_id,
                    "canvas_id": existing.get("canvas_id"),
                    "canvas_module_id": existing.get("canvas_module_id"),
                    "state_path": str(state_path),
                    "hosted_url": entry.get("hosted_url"),
                }

        if canvas_artifact_type == "assignment":
            result = push_assignment(client, canvas_fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif canvas_artifact_type == "page":
            result = push_page(client, canvas_fm, html, existing_page_url)
            canvas_id = result.get("page_id")
            canvas_page_url = result.get("url")
        elif canvas_artifact_type == "discussion":
            result = push_discussion(client, canvas_fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif canvas_artifact_type == "quiz":
            result = push_quiz(client, canvas_fm, html, existing_id)
            canvas_id = result["id"]
            canvas_page_url = None
        elif canvas_artifact_type == "module_header":
            canvas_id = None
            canvas_page_url = None
            result = {}
        else:
            raise ValueError(f"Unknown artifact type: {canvas_artifact_type}")

        # Resolve module and add to it if not already present
        module_id = resolve_or_create_module(
            client,
            fm["module"],
            publish=fm.get("publish", True),
        )

        canvas_module_item_id = existing.get("canvas_module_item_id")
        if canvas_artifact_type != "module_header" and action == "created":
            content_type_map = {
                "assignment": "Assignment",
                "page": "Page",
                "discussion": "Discussion",
                "quiz": "Quiz",
            }
            module_item = client.add_module_item(
                module_id,
                title=fm["title"],
                content_type=content_type_map[canvas_artifact_type],
                content_id=canvas_id if canvas_artifact_type != "page" else None,
                page_url=canvas_page_url if canvas_artifact_type == "page" else None,
                position=fm.get("position"),
                completion_requirement=completion_requirement,
            )
            canvas_module_item_id = module_item.get("id")
        elif (
            canvas_artifact_type != "module_header"
            and canvas_module_item_id
            and completion_requirement
            and (
                existing.get("completion_requirement") != completion_requirement_state_value(completion_requirement)
                or completion_requirement.get("type") == "min_score"
            )
        ):
            client.update_module_item(
                module_id,
                int(canvas_module_item_id),
                {"completion_requirement": completion_requirement},
            )
        elif (
            canvas_artifact_type != "module_header"
            and canvas_module_item_id
            and not completion_requirement
            and existing.get("completion_requirement")
        ):
            raise ValueError(
                f"{rel_path}: completion_requirement none cannot safely clear an existing Canvas "
                "module completion requirement through the artifact push path"
            )

        pushed_at = utc_now()
        entry = entry_for_push(
            artifact_id=artifact_id,
            rel_path=rel_path,
            artifact_type=canvas_artifact_type,
            canvas_id=canvas_id,
            canvas_page_url=canvas_page_url,
            canvas_module_id=module_id,
            canvas_module_item_id=canvas_module_item_id,
            hash_value=content_hash(md_path),
            pushed_at=pushed_at,
            source_commit=os.environ.get("GITHUB_SHA"),
            hosted_path=hosted_info["hosted_path"] if hosted_info["enabled"] else None,
            hosted_url=hosted_info["hosted_url"] if hosted_info["enabled"] else None,
            completion_requirement=completion_requirement_state_value(completion_requirement),
            source_type=artifact_type,
            delivery_mode=delivery_mode,
            external_state=store.external,
        )
        artifacts[state_key] = entry
        if hosted_info["enabled"] and artifact_type != "module_header" and hosted_output_dir:
            hosted_result = render_hosted_artifact(
                md_path,
                manifest_path,
                hosted_output_dir,
                manifest=manifest,
                state=deployment_state,
            )
            entry["hosted_hash"] = hosted_result["hosted_hash"]
            entry["hosted_last_rendered"] = pushed_at
            render_hosted_files(
                manifest_path,
                hosted_output_dir,
                discover_hosted_artifact_files(manifest_path),
                manifest=manifest,
                state=deployment_state,
            )

        if store.external:
            live_state = fetch_canvas_state(client, entry)
            fingerprint = canvas_fingerprint(live_state, canvas_artifact_type)
            if fingerprint:
                entry["canvas_fingerprint"] = fingerprint

        artifacts[state_key] = entry
        deployment_state["last_sync"] = pushed_at
        store.save(deployment_state, state_path)

        return {
            "action": action,
            "file": rel_path,
            "artifact_id": artifact_id,
            "canvas_id": canvas_id,
            "canvas_module_id": module_id,
            "state_path": str(state_path),
            "hosted_url": entry.get("hosted_url"),
        }


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--state-dir",
        type=Path,
        help="External deployment-state checkout, for example a canvas-state branch worktree.",
    )
    parser.add_argument(
        "--hosted-output-dir",
        type=Path,
        help="Common Curriculum checkout root for rendering hosted HTML before saving state.",
    )
    args = parser.parse_args()

    try:
        result = push_artifact(
            args.file,
            args.manifest,
            state_dir=args.state_dir,
            hosted_output_dir=args.hosted_output_dir,
        )
        print(json.dumps(result, indent=2))
        return 0
    except ValueError as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        return 2
    except CanvasError as e:
        print(f"CANVAS ERROR: {e}", file=sys.stderr)
        return 3
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

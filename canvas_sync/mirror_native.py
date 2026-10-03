"""Plan/apply an existing native course mirror with local-only credentials.

No course/account/user/enrollment writes, object creation, deletion, imports,
submission reads, or grade reads are supported. A snapshot and reviewable plan
precede PUTs to existing mapped teaching objects. The shell remains unpublished.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import stat
import sys
from urllib.parse import urlsplit

import requests
from dotenv import dotenv_values

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from canvas_sync.course_mirror import mirror_url, validate_config


COURSE_FIELDS = ("id", "name", "workflow_state", "time_zone", "default_view", "start_at", "end_at")
ASSIGNMENT_FIELDS = ("id", "name", "description", "published", "submission_types", "points_possible", "grading_type", "omit_from_final_grade", "assignment_group_id", "due_at", "unlock_at", "lock_at", "allowed_extensions", "allowed_attempts")
PAGE_FIELDS = ("page_id", "url", "title", "body", "published", "front_page")
DISCUSSION_FIELDS = ("id", "title", "message", "published", "assignment_id")
MODULE_FIELDS = ("id", "name", "position", "published", "unlock_at", "prerequisite_module_ids", "require_sequential_progress", "completion_requirements")
ITEM_FIELDS = ("id", "type", "title", "position", "published", "content_id", "page_url", "completion_requirement")


def pick(row, fields):
    return {key: row.get(key) for key in fields}


class CourseApi:
    def __init__(self, course_url: str, env_path: Path, *, writable=False):
        parsed = urlsplit(course_url)
        self.origin = parsed.scheme + "://" + parsed.netloc
        self.prefix = "/api/v1" + parsed.path.rstrip("/")
        if env_path.is_symlink() or not env_path.is_file() or stat.S_IMODE(env_path.stat().st_mode) != 0o600:
            raise ValueError("Credential file must be a local regular file with mode 0600")
        config = dotenv_values(env_path)
        if config.get("CANVAS_API_URL", "").rstrip("/") != self.origin or not config.get("CANVAS_API_TOKEN"):
            raise ValueError("Local credential does not match the selected Canvas instance")
        self.session = requests.Session()
        self.session.trust_env = False
        self.session.headers["Authorization"] = "Bearer " + config["CANVAS_API_TOKEN"]
        config.clear()
        self.writable = writable

    def request(self, method, path, **kwargs):
        url = path if path.startswith("https://") else self.origin + self.prefix + path
        parsed = urlsplit(url)
        if parsed.scheme + "://" + parsed.netloc != self.origin or not (parsed.path == self.prefix or parsed.path.startswith(self.prefix + "/")):
            raise ValueError("Cross-course or cross-origin request refused")
        forbidden = {"users", "students", "enrollments", "submissions", "grades", "gradebook"}
        if forbidden.intersection(parsed.path.split("/")):
            raise ValueError("Person, submission, and grade endpoints are excluded")
        if method != "GET":
            if not self.writable or method != "PUT" or not re.fullmatch(re.escape(self.prefix) + r"/(?:pages/[A-Za-z0-9_-]+|assignments/\d+|discussion_topics/\d+|modules/\d+(?:/items/\d+)?)", parsed.path):
                raise ValueError("Only PUTs to existing destination teaching objects are supported")
        try:
            response = self.session.request(method, url, timeout=40, allow_redirects=False, **kwargs)
        except requests.RequestException:
            raise RuntimeError("Canvas transport failure; no automatic write retry") from None
        if response.status_code != 200:
            raise RuntimeError(f"Canvas {method} {parsed.path}: HTTP {response.status_code}; no write retry")
        return response.json(), response.links.get("next", {}).get("url")

    def get(self, path, params=None):
        return self.request("GET", path, params=params)[0]

    def listing(self, path):
        data, next_url = self.request("GET", path, params={"per_page": 100})
        while next_url:
            more, next_url = self.request("GET", next_url)
            data.extend(more)
        return data


def snapshot(api, config, side, extra):
    mapping = config["mapping"]
    source = side == "source"
    ids = lambda kind: {int(i) for i in (mapping[kind].keys() if source else mapping[kind].values())}
    data = {"course": pick(api.get(""), COURSE_FIELDS)}
    data["discussion_topics"] = [pick(row, DISCUSSION_FIELDS) for row in api.listing("/discussion_topics") if row["id"] in ids("discussion_topics")]
    assignments = api.listing("/assignments")
    data["assignments"] = [pick(row, ASSIGNMENT_FIELDS) for row in assignments if row["id"] in ids("assignments")]
    backing_ids = {row["assignment_id"] for row in data["discussion_topics"] if row.get("assignment_id")}
    data["discussion_assignments"] = [pick(row, ASSIGNMENT_FIELDS) for row in assignments if row["id"] in backing_ids]
    slugs = mapping["page_urls"].keys() if source else mapping["page_urls"].values()
    data["pages"] = [pick(api.get("/pages/" + slug), PAGE_FIELDS) for slug in slugs]
    data["modules"] = []
    for row in api.listing("/modules"):
        if row["id"] not in ids("modules"):
            continue
        module = pick(row, MODULE_FIELDS)
        module["completion_requirements"] = [pick(r, ("id", "type", "min_score")) for r in (row.get("completion_requirements") or [])]
        module["items"] = []
        for item in api.listing("/modules/" + str(row["id"]) + "/items"):
            value = pick(item, ITEM_FIELDS)
            requirement = item.get("completion_requirement") or {}
            value["completion_requirement"] = {k: requirement[k] for k in ("type", "min_score") if k in requirement}
            module["items"].append(value)
        data["modules"].append(module)
    data["assignment_groups"] = [pick(row, ("id", "name", "position", "group_weight")) for row in api.listing("/assignment_groups")]
    assert len(data["assignments"]) == len(mapping["assignments"])
    assert len(data["discussion_topics"]) == len(mapping["discussion_topics"])
    assert len(data["modules"]) == len(mapping["modules"])
    assert sum(len(m["items"]) for m in data["modules"]) == len(mapping["module_items"]), "New or missing native items need an explicit mapping update"
    return data


def mirrored_body(body, config):
    def replace(match):
        source = urlsplit(html.unescape(match[2]))
        base = urlsplit(config["sharedBaseUrl"])
        if source.netloc != base.netloc or not source.path.startswith(base.path):
            raise ValueError("Unexpected source iframe origin or course path")
        page = source.path[len(base.path):]
        return match[1] + html.escape(mirror_url(config, page), quote=True) + match[3]
    result, count = re.subn(r'(<iframe\b[^>]*\bsrc=")(.*?)(")', replace, body)
    if count != 1 or config["sourceCanvasUrl"] in result:
        raise ValueError("Expected exactly one shared hosted iframe without source Canvas links")
    return result


def plan(before, config, extra):
    src, dst = before["source"], before["destination"]
    assert dst["course"]["workflow_state"] == "unpublished"
    mapping = config["mapping"]
    operations = []
    checks = []
    for source_id, target_id in extra["assignment_groups"].items():
        source_group = next(row for row in src["assignment_groups"] if row["id"] == int(source_id))
        target_group = next(row for row in dst["assignment_groups"] if row["id"] == target_id)
        assert all(source_group[k] == target_group[k] for k in ("name", "group_weight")), "Assignment group drift needs explicit review"
    def change(path, desired, current, wrapper):
        differing = {k: v for k, v in desired.items() if current.get(k) != v}
        if differing:
            operations.append({"path": path, "wrapper": wrapper, "before": {k: current.get(k) for k in differing}, "desired": differing})
        checks.append({"path": path, "fields": list(desired), "matches": not differing})
    for original in src["assignments"]:
        target_id = mapping["assignments"][str(original["id"])]
        current = next(row for row in dst["assignments"] if row["id"] == target_id)
        desired = {k: original[k] for k in ASSIGNMENT_FIELDS if k not in ("id", "description", "assignment_group_id")}
        desired["description"] = mirrored_body(original["description"], config)
        desired["assignment_group_id"] = extra["assignment_groups"][str(original["assignment_group_id"])]
        change("/assignments/" + str(target_id), desired, current, "assignment")
    for original in src["pages"]:
        slug = mapping["page_urls"][original["url"]]
        current = next(row for row in dst["pages"] if row["url"] == slug)
        assert current["page_id"] == extra["pages"][str(original["page_id"])]
        assert original["front_page"] == current["front_page"], "Front-page identity must remain unchanged"
        change("/pages/" + slug, {"title": original["title"], "body": mirrored_body(original["body"], config), "published": original["published"]}, current, "wiki_page")
    for original in src["discussion_topics"]:
        target_id = mapping["discussion_topics"][str(original["id"])]
        current = next(row for row in dst["discussion_topics"] if row["id"] == target_id)
        change("/discussion_topics/" + str(target_id), {"title": original["title"], "message": mirrored_body(original["message"], config), "published": original["published"]}, current, None)
        if original.get("assignment_id"):
            # Canvas owns the discussion's backing assignment and updates its
            # description from the topic message. Verify its grading separately.
            source_assignment = next(row for row in src.get("discussion_assignments", []) if row["id"] == original["assignment_id"])
            target_assignment = next(row for row in dst.get("discussion_assignments", []) if row["id"] == current["assignment_id"])
            desired = {k: source_assignment[k] for k in ASSIGNMENT_FIELDS if k not in ("id", "description", "assignment_group_id")}
            desired["assignment_group_id"] = extra["assignment_groups"][str(source_assignment["assignment_group_id"])]
            change("/assignments/" + str(target_assignment["id"]), desired, target_assignment, "assignment")
    for module_position, original in enumerate(sorted(src["modules"], key=lambda row: row["position"]), 1):
        target_id = mapping["modules"][str(original["id"])]
        current = next(row for row in dst["modules"] if row["id"] == target_id)
        desired = {k: original[k] for k in MODULE_FIELDS if k not in ("id", "prerequisite_module_ids", "completion_requirements")}
        # Source positions can have gaps left by retired/unselected objects.
        # Mirror the selected teaching order, keeping destination IDs stable.
        desired["position"] = module_position
        desired["prerequisite_module_ids"] = [mapping["modules"][str(i)] for i in original["prerequisite_module_ids"]]
        desired["completion_requirements"] = [dict(row, id=mapping["module_items"][str(row["id"])]) for row in original["completion_requirements"]]
        change("/modules/" + str(target_id), desired, current, "module")
        assert [mapping["module_items"][str(row["id"])] for row in original["items"]] == [row["id"] for row in current["items"]], "Native item identities/order must remain stable"
        for item_position, item in enumerate(sorted(original["items"], key=lambda row: row["position"]), 1):
            target_item = mapping["module_items"][str(item["id"])]
            current_item = next(row for row in current["items"] if row["id"] == target_item)
            assert item["type"] == current_item["type"]
            if item["type"] == "Page":
                assert mapping["page_urls"][item["page_url"]] == current_item["page_url"]
            else:
                kind = {"Assignment": "assignments", "Discussion": "discussion_topics"}[item["type"]]
                assert mapping[kind][str(item["content_id"])] == current_item["content_id"]
            assert item["published"] == current_item["published"]
            assert item["completion_requirement"] == current_item["completion_requirement"]
            change(f"/modules/{target_id}/items/{target_item}", {"title": item["title"], "position": item_position}, current_item, "module_item")
    return {"operations": operations, "checks": checks, "course_stays_unpublished": True}


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--source-env", type=Path, required=True)
    parser.add_argument("--destination-env", type=Path, required=True)
    parser.add_argument("--receipts", type=Path, required=True)
    parser.add_argument("--phase", choices=("snapshot", "plan", "apply", "verify"), required=True)
    args = parser.parse_args()
    config = validate_config(json.loads(args.config.read_text()))
    extra = json.loads(args.mapping.read_text())["mapping"]
    args.receipts.mkdir(parents=True, exist_ok=True)
    before_file = args.receipts / "before.json"
    plan_file = args.receipts / "plan.json"
    if args.phase in ("snapshot", "verify"):
        src = CourseApi(config["sourceCanvasUrl"], args.source_env)
        dst = CourseApi(config["destinationCanvasUrl"], args.destination_env)
        result = {"at": datetime.now(timezone.utc).isoformat(), "source": snapshot(src, config, "source", extra), "destination": snapshot(dst, config, "destination", extra)}
        if args.phase == "snapshot":
            if before_file.exists(): raise ValueError("Never overwrite the original backup")
            save(before_file, result)
            print(json.dumps({"snapshot": str(before_file), "destination_unpublished": result["destination"]["course"]["workflow_state"] == "unpublished"}))
        else:
            save(args.receipts / "after.json", result)
            parity = plan(result, config, extra)
            original = json.loads(before_file.read_text())["destination"]
            assert result["destination"]["course"] == original["course"], "Course settings changed"
            assert not parity["operations"], "Native mirror is not idempotent"
            save(args.receipts / "verification.json", {"at": result["at"], "passed": True, "native_objects_checked": len(parity["checks"]), "remaining_operations": 0, "course_unchanged": True})
            print(json.dumps({"passed": True, "native_objects_checked": len(parity["checks"]), "remaining_operations": 0}))
    elif args.phase == "plan":
        result = plan(json.loads(before_file.read_text()), config, extra)
        save(plan_file, result)
        print(json.dumps({"operations": len(result["operations"]), "changed_fields": sorted({k for op in result["operations"] for k in op["desired"]})}))
    else:
        dst = CourseApi(config["destinationCanvasUrl"], args.destination_env, writable=True)
        assert dst.get("")["workflow_state"] == "unpublished"
        for operation in json.loads(plan_file.read_text())["operations"]:
            current = dst.get(operation["path"])
            fields = operation["desired"]
            if all(current.get(k) == v for k, v in fields.items()):
                outcome = "already_matches"
            else:
                assert all(current.get(k) == v for k, v in operation["before"].items()), "Destination drift since backup"
                payload = dict(fields, notify_of_update=False)
                if operation["wrapper"]: payload = {operation["wrapper"]: payload}
                result, _ = dst.request("PUT", operation["path"], json=payload)
                assert all(result.get(k) == v for k, v in fields.items()), "Canvas did not preserve desired fields"
                outcome = "updated"
            with (args.receipts / "writes.jsonl").open("a") as file:
                file.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), "path": operation["path"], "fields": list(fields), "outcome": outcome}) + "\n")
            print(operation["path"], outcome, flush=True)
        assert dst.get("")["workflow_state"] == "unpublished"


if __name__ == "__main__":
    main()

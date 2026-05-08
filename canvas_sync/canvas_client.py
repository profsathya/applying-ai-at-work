"""
Canvas LMS REST API client.

Handles authentication, request construction, and error translation for the
artifact types the course builder cares about: assignments, pages, discussions,
quizzes, modules, and module items.

Canvas API docs: https://canvas.instructure.com/doc/api/

Environment variables required:
  CANVAS_API_URL      e.g., https://csumb.instructure.com
  CANVAS_API_TOKEN    personal access token with course-authoring scope
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import requests


class CanvasError(Exception):
    """Raised for canvas-side failures (non-2xx responses, rate limits, auth)."""

    def __init__(self, message: str, status: int | None = None, payload: Any = None):
        super().__init__(message)
        self.status = status
        self.payload = payload


@dataclass
class CanvasClient:
    base_url: str
    token: str
    course_id: int
    timeout: int = 30
    max_retries: int = 3

    @classmethod
    def from_env(cls, course_id: int | None = None) -> "CanvasClient":
        base_url = os.environ.get("CANVAS_API_URL")
        token = os.environ.get("CANVAS_API_TOKEN")
        cid = course_id or int(os.environ.get("DEFAULT_COURSE_ID", "0"))
        if not base_url or not token or not cid:
            raise CanvasError(
                "Missing env vars: CANVAS_API_URL, CANVAS_API_TOKEN, DEFAULT_COURSE_ID"
            )
        return cls(base_url=base_url.rstrip("/"), token=token, course_id=cid)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(
        self, method: str, path: str, json_body: dict | None = None, params: dict | None = None
    ) -> dict | list:
        url = urljoin(self.base_url + "/", f"api/v1/courses/{self.course_id}/{path.lstrip('/')}")
        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                resp = requests.request(
                    method,
                    url,
                    headers=self._headers(),
                    json=json_body,
                    params=params,
                    timeout=self.timeout,
                )

                if resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", "10"))
                    time.sleep(retry_after)
                    continue

                if resp.status_code >= 500 and attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

                if not resp.ok:
                    raise CanvasError(
                        f"{method} {url} -> {resp.status_code}: {resp.text[:500]}",
                        status=resp.status_code,
                        payload=resp.text,
                    )

                if resp.status_code == 204 or not resp.content:
                    return {}
                return resp.json()

            except requests.RequestException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise CanvasError(f"Network error: {e}") from e

        raise CanvasError(f"Exhausted retries: {last_error}")

    def _request_paginated(self, method: str, path: str, params: dict | None = None) -> list[dict]:
        """Fetch all pages for Canvas list endpoints."""
        merged_params = dict(params or {})
        merged_params.setdefault("per_page", 100)
        page = 1
        results: list[dict] = []

        while True:
            page_params = {**merged_params, "page": page}
            result = self._request(method, path, params=page_params)
            if not isinstance(result, list):
                return results

            results.extend(result)
            if len(result) < int(merged_params["per_page"]):
                return results
            page += 1

    # ---- Assignments ----

    def create_assignment(self, payload: dict) -> dict:
        return self._request("POST", "assignments", {"assignment": payload})

    def update_assignment(self, assignment_id: int, payload: dict) -> dict:
        return self._request("PUT", f"assignments/{assignment_id}", {"assignment": payload})

    def get_assignment(self, assignment_id: int) -> dict:
        return self._request("GET", f"assignments/{assignment_id}")

    def delete_assignment(self, assignment_id: int) -> dict:
        return self._request("DELETE", f"assignments/{assignment_id}")

    # ---- Pages ----

    def create_page(self, payload: dict) -> dict:
        return self._request("POST", "pages", {"wiki_page": payload})

    def update_page(self, page_url: str, payload: dict) -> dict:
        return self._request("PUT", f"pages/{page_url}", {"wiki_page": payload})

    def get_page(self, page_url: str) -> dict:
        return self._request("GET", f"pages/{page_url}")

    def delete_page(self, page_url: str) -> dict:
        return self._request("DELETE", f"pages/{page_url}")

    # ---- Discussions ----

    def create_discussion(self, payload: dict) -> dict:
        return self._request("POST", "discussion_topics", payload)

    def update_discussion(self, topic_id: int, payload: dict) -> dict:
        return self._request("PUT", f"discussion_topics/{topic_id}", payload)

    def get_discussion(self, topic_id: int) -> dict:
        return self._request("GET", f"discussion_topics/{topic_id}")

    def delete_discussion(self, topic_id: int) -> dict:
        return self._request("DELETE", f"discussion_topics/{topic_id}")

    # ---- Quizzes ----

    def create_quiz(self, payload: dict) -> dict:
        return self._request("POST", "quizzes", {"quiz": payload})

    def update_quiz(self, quiz_id: int, payload: dict) -> dict:
        return self._request("PUT", f"quizzes/{quiz_id}", {"quiz": payload})

    def get_quiz(self, quiz_id: int) -> dict:
        return self._request("GET", f"quizzes/{quiz_id}")

    def delete_quiz(self, quiz_id: int) -> dict:
        return self._request("DELETE", f"quizzes/{quiz_id}")

    def add_quiz_question(self, quiz_id: int, question: dict) -> dict:
        return self._request(
            "POST", f"quizzes/{quiz_id}/questions", {"question": question}
        )

    def list_quiz_questions(self, quiz_id: int) -> list[dict]:
        result = self._request(
            "GET", f"quizzes/{quiz_id}/questions", params={"per_page": 100}
        )
        return result if isinstance(result, list) else []

    def delete_quiz_question(self, quiz_id: int, question_id: int) -> dict:
        return self._request(
            "DELETE", f"quizzes/{quiz_id}/questions/{question_id}"
        )

    # ---- Modules ----

    def list_modules(self) -> list[dict]:
        return self._request_paginated("GET", "modules")

    def list_module_items(self, module_id: int) -> list[dict]:
        return self._request_paginated("GET", f"modules/{module_id}/items")

    def delete_module(self, module_id: int) -> dict:
        return self._request("DELETE", f"modules/{module_id}")

    def update_module(self, module_id: int, payload: dict) -> dict:
        return self._request("PUT", f"modules/{module_id}", {"module": payload})

    def create_module(
        self,
        name: str,
        position: int | None = None,
        published: bool | None = True,
    ) -> dict:
        payload = {"module": {"name": name}}
        if position is not None:
            payload["module"]["position"] = position
        if published is not None:
            payload["module"]["published"] = published
        return self._request("POST", "modules", payload)

    def add_module_item(
        self,
        module_id: int,
        *,
        title: str,
        content_type: str,  # Assignment | Page | Discussion | Quiz | SubHeader
        content_id: int | None = None,
        page_url: str | None = None,
        position: int | None = None,
    ) -> dict:
        item: dict[str, Any] = {"type": content_type, "title": title}
        if content_id is not None:
            item["content_id"] = content_id
        if page_url is not None:
            item["page_url"] = page_url
        if position is not None:
            item["position"] = position
        return self._request("POST", f"modules/{module_id}/items", {"module_item": item})

    def delete_module_item(self, module_id: int, module_item_id: int) -> dict:
        return self._request("DELETE", f"modules/{module_id}/items/{module_item_id}")

    # ---- Rubrics ----

    def create_rubric(self, payload: dict) -> dict:
        return self._request("POST", "rubrics", payload)


def resolve_or_create_module(
    client: CanvasClient,
    module_name: str,
    *,
    publish: bool | None = None,
) -> int:
    """Idempotent: find module by name, create if missing, return module_id."""
    modules = client.list_modules()
    for m in modules:
        if m.get("name") == module_name:
            if publish and not m.get("published"):
                client.update_module(m["id"], {"published": True})
            return m["id"]
    result = client.create_module(module_name, published=publish)
    return result["id"]


if __name__ == "__main__":
    # Smoke test: confirm credentials work by listing modules
    from dotenv import load_dotenv

    load_dotenv()
    client = CanvasClient.from_env()
    modules = client.list_modules()
    print(f"Connected to course {client.course_id}. Found {len(modules)} modules.")
    for m in modules[:5]:
        print(f"  - {m['id']}: {m['name']}")

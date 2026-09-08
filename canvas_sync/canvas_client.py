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
from urllib.parse import urljoin, urlsplit

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

    def _url(self, path: str) -> str:
        if urlsplit(path).scheme:
            url = path
        else:
            url = urljoin(self.base_url + "/", f"api/v1/courses/{self.course_id}/{path.lstrip('/')}")
        base = urlsplit(self.base_url)
        target = urlsplit(url)
        if (base.scheme, base.netloc) != (target.scheme, target.netloc):
            raise CanvasError("Refusing to send Canvas credentials to a different pagination origin")
        return url

    def _request_response(self, method: str, path: str, json_body=None, params=None):
        url = self._url(path)
        retryable = method.upper() in {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}
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
                    if attempt < self.max_retries - 1:
                        try:
                            retry_after = max(0, float(resp.headers.get("Retry-After", "10")))
                        except ValueError:
                            retry_after = 10
                        time.sleep(retry_after)
                        continue

                if retryable and resp.status_code >= 500 and attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue

                if not resp.ok:
                    raise CanvasError(
                        f"{method} {url} -> {resp.status_code}: {resp.text[:500]}",
                        status=resp.status_code,
                        payload=resp.text,
                    )

                return resp

            except requests.RequestException as e:
                last_error = e
                if retryable and attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise CanvasError(f"Network error: {e}") from e

        raise CanvasError(f"Exhausted retries: {last_error}")

    def _request(self, method: str, path: str, json_body=None, params=None) -> dict | list:
        response = self._request_response(method, path, json_body=json_body, params=params)
        if response.status_code == 204 or not response.content:
            return {}
        return response.json()

    def _request_paginated(self, method: str, path: str, params: dict | None = None) -> list[dict]:
        """Follow Canvas's opaque next links, including server-capped short pages."""
        page_params = {"per_page": 100, **(params or {})}
        results = []
        seen = set()
        while path:
            url = self._url(path)
            if url in seen:
                raise CanvasError("Canvas returned a repeated pagination URL")
            seen.add(url)
            response = self._request_response(method, path, params=page_params)
            result = response.json()
            if not isinstance(result, list):
                raise CanvasError("Canvas list endpoint returned a non-list response")
            results.extend(result)
            path = response.links.get("next", {}).get("url")
            page_params = None  # A next URL already contains all of its parameters.
        return results

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

    def list_module_items(
        self,
        module_id: int,
        *,
        student_id: int | str | None = None,
        include: list[str] | None = None,
    ) -> list[dict]:
        params: dict[str, Any] = {}
        if student_id is not None:
            params["student_id"] = student_id
        if include:
            params["include[]"] = include
        return self._request_paginated("GET", f"modules/{module_id}/items", params=params)

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
        completion_requirement: dict | None = None,
    ) -> dict:
        item: dict[str, Any] = {"type": content_type, "title": title}
        if content_id is not None:
            item["content_id"] = content_id
        if page_url is not None:
            item["page_url"] = page_url
        if position is not None:
            item["position"] = position
        if completion_requirement:
            item["completion_requirement"] = completion_requirement
        return self._request("POST", f"modules/{module_id}/items", {"module_item": item})

    def update_module_item(self, module_id: int, module_item_id: int, payload: dict) -> dict:
        return self._request(
            "PUT",
            f"modules/{module_id}/items/{module_item_id}",
            {"module_item": payload},
        )

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
    # Canvas can ignore published on module creation. Honor the requested
    # visibility immediately, including single-artifact module pushes.
    if publish and not result.get("published"):
        client.update_module(result["id"], {"published": True})
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

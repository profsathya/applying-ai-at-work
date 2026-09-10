import json
import unittest
from unittest.mock import patch

import requests

from canvas_sync.canvas_client import CanvasClient, CanvasError, resolve_or_create_module


def response(payload, *, status=200, next_url=None):
    result = requests.Response()
    result.status_code = status
    result._content = json.dumps(payload).encode()
    if next_url:
        result.headers["Link"] = f'<{next_url}>; rel="next"'
    return result


class CanvasTransportTests(unittest.TestCase):
    def setUp(self):
        self.client = CanvasClient("https://example.test", "test-token", 42)

    def test_new_module_is_published_when_canvas_ignores_creation_visibility(self):
        with patch("requests.request", side_effect=[
            response([]), response({"id": 55, "published": False}),
            response({"id": 55, "published": True}),
        ]) as request:
            self.assertEqual(resolve_or_create_module(self.client, "Test", publish=True), 55)
        self.assertEqual(request.call_args_list[-1].args, (
            "PUT", "https://example.test/api/v1/courses/42/modules/55",
        ))
        self.assertEqual(request.call_args_list[-1].kwargs["json"], {"module": {"published": True}})

    def test_new_module_visibility_does_not_add_unneeded_writes(self):
        for requested, actual in ((False, False), (None, False), (True, True)):
            with self.subTest(requested=requested, actual=actual), patch(
                "requests.request", side_effect=[response([]), response({"id": 55, "published": actual})],
            ) as request:
                self.assertEqual(resolve_or_create_module(self.client, "Test", publish=requested), 55)
                self.assertEqual(request.call_count, 2)

    def test_short_page_follows_opaque_next_link_without_replacing_parameters(self):
        next_url = "https://example.test/api/v1/courses/42/modules?cursor=opaque-token"
        with patch(
            "requests.request",
            side_effect=[
                response([{"id": 1}], next_url=next_url),
                response([{"id": 2}]),
            ],
        ) as request:
            self.assertEqual(self.client.list_modules(), [{"id": 1}, {"id": 2}])
        self.assertEqual(request.call_args_list[1].args[1], next_url)
        self.assertIsNone(request.call_args_list[1].kwargs["params"])

    def test_untrusted_next_origin_does_not_receive_credentials(self):
        with patch(
            "requests.request",
            return_value=response([{"id": 1}], next_url="https://other.test/modules"),
        ) as request:
            with self.assertRaisesRegex(CanvasError, "different pagination origin"):
                self.client.list_modules()
        self.assertEqual(request.call_count, 1)

    def test_non_list_and_pagination_loops_are_errors(self):
        with patch("requests.request", return_value=response({})):
            with self.assertRaisesRegex(CanvasError, "non-list"):
                self.client.list_modules()
        url = "https://example.test/api/v1/courses/42/modules"
        with patch("requests.request", return_value=response([], next_url=url)):
            with self.assertRaisesRegex(CanvasError, "repeated pagination"):
                self.client.list_modules()

    def test_ambiguous_create_is_not_automatically_replayed(self):
        for failure in [
            requests.ReadTimeout("response lost"),
            response({}, status=503),
        ]:
            with (
                self.subTest(failure=failure),
                patch("requests.request", side_effect=[failure]) as request,
                patch("time.sleep"),
            ):
                with self.assertRaises(CanvasError):
                    self.client.create_page({"title": "One page"})
                self.assertEqual(request.call_count, 1)

    def test_reads_retry_and_explicit_rate_limit_can_retry_create(self):
        with (
            patch(
                "requests.request",
                side_effect=[requests.ReadTimeout(), response({"id": 1})],
            ) as request,
            patch("time.sleep"),
        ):
            self.assertEqual(self.client.get_page("page"), {"id": 1})
            self.assertEqual(request.call_count, 2)
        with (
            patch(
                "requests.request",
                side_effect=[response({}, status=429), response({"page_id": 1})],
            ),
            patch("time.sleep"),
        ):
            self.assertEqual(
                self.client.create_page({"title": "One page"}), {"page_id": 1}
            )

import unittest
from unittest.mock import patch

from canvas_sync.cleanup_hosted_links import (
    same_except_body, state_allows_cleanup, state_needs_link_cleanup_heal,
    without_legacy_link,
)
from canvas_sync.state import canvas_fingerprint


class HostedLinkCleanupTests(unittest.TestCase):
    def test_removes_only_link_for_both_legacy_targets(self):
        for target in ("_blank", "_top"):
            with self.subTest(target=target):
                iframe = ('<iframe title="Example" src="https://example.test/page?context=canvas" '
                          'width="100%"></iframe>')
                body = ('<div class="hosted-html-shell">' + iframe +
                        '<p><a href="https://example.test/page?context=canvas" target="' + target +
                        '">Open hosted page in a new tab</a></p></div>')
                self.assertEqual(without_legacy_link(body),
                                 '<div class="hosted-html-shell">' + iframe + '</div>')

    def test_refuses_a_link_to_another_page(self):
        body = ('<div class="hosted-html-shell"><iframe src="https://example.test/a"></iframe>'
                '<p><a href="https://example.test/b" target="_top">'
                'Open hosted page in a new tab</a></p></div>')
        with self.assertRaisesRegex(ValueError, "does not match"):
            without_legacy_link(body)

    def test_leaves_other_content_alone(self):
        self.assertIsNone(without_legacy_link('<p>Read this page.</p>'))
        with self.assertRaisesRegex(ValueError, "outside a complete"):
            without_legacy_link('<p>Open hosted page in a new tab</p>')

    def test_accepts_only_a_locally_reconciled_publication_change(self):
        live = {"name": "Example", "description": "<div>same body</div>",
                "points_possible": 0, "published": False}
        entry = {"local_path": "course1/sprints/sprint-1/example.md",
                 "canvas_fingerprint": canvas_fingerprint({**live, "published": True}, "assignment")}
        with patch("canvas_sync.cleanup_hosted_links.parse_frontmatter",
                   return_value=({"publish": False}, "")):
            self.assertTrue(state_allows_cleanup(entry, live, "assignment"))
        with patch("canvas_sync.cleanup_hosted_links.parse_frontmatter",
                   return_value=({"publish": True}, "")):
            self.assertFalse(state_allows_cleanup(entry, live, "assignment"))
        self.assertFalse(state_allows_cleanup(entry, {**live, "name": "Canvas edit"}, "assignment"))

    def test_recognizes_link_removed_through_linked_canvas_object(self):
        frame = '<iframe src="https://example.test/page?context=canvas"></iframe>'
        clean = '<div class="hosted-html-shell">' + frame + '</div>'
        old = (clean[:-6] + '<p><a href="https://example.test/page?context=canvas" '
               'target="_blank">Open hosted page in a new tab</a></p></div>')
        live = {"title": "Example", "message": clean, "published": True}
        entry = {"canvas_fingerprint": canvas_fingerprint({**live, "message": old}, "discussion")}
        self.assertTrue(state_needs_link_cleanup_heal(entry, live, "discussion"))
        self.assertTrue(same_except_body({**live, "message": old}, live, "discussion"))
        self.assertFalse(same_except_body({**live, "title": "Other"}, live, "discussion"))


if __name__ == "__main__":
    unittest.main()

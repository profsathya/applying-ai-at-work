from pathlib import Path
import tempfile
import unittest

from canvas_sync.link_audit import audit_artifact, audit_rendered_html


class LinkAuditTests(unittest.TestCase):
    def test_rendered_link_policy_accepts_supported_link_classes(self) -> None:
        rendered = """
        <h2 id="details">Details</h2>
        <a href="https://example.edu/resource" target="_top">Web</a>
        <a href="mailto:teacher@example.edu" target="_top">Email</a>
        <a href="next.html">Next</a>
        <a href="#details">Details</a>
        <a href="artifact:target-id">Course artifact</a>
        """
        self.assertEqual(audit_rendered_html(rendered, "fixture"), [])

    def test_rendered_link_policy_rejects_iframe_and_placeholder_failures(self) -> None:
        errors = audit_rendered_html(
            '<a href="https://example.com/DOC-ID">Template</a>'
            '<a href="#missing">Missing</a>'
            '<a href="javascript:alert(1)">Unsafe</a>',
            "fixture",
        )
        self.assertTrue(any("placeholder URL" in error for error in errors))
        self.assertTrue(any("does not escape the Canvas iframe" in error for error in errors))
        self.assertTrue(any("missing fragment" in error for error in errors))
        self.assertTrue(any("unsupported URL scheme" in error for error in errors))

    def test_artifact_audit_uses_production_renderer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.md"
            path.write_text(
                "---\n"
                "title: Link fixture\n"
                "slug: link-fixture\n"
                "type: page\n"
                "sprint: 1\n"
                "module: Link fixture\n"
                "position: 1\n"
                "published: true\n"
                "---\n\n"
                "[Template](https://docs.google.com/document/d/abc/copy)\n",
                encoding="utf-8",
            )
            count, errors = audit_artifact(path)
            self.assertEqual(count, 1)
            self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

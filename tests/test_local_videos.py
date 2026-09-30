from pathlib import Path
import json
import tempfile
import unittest

from canvas_sync.hosted_html import artifact_hosted_output_paths, markdown_body_to_html, render_hosted_artifact
from canvas_sync.schema import validate_artifact
from tests.test_hosted_html import write_manifest, write_page


def block(**overrides):
    config = dict(src='assets/setup.mp4', title='Setup <coach> "video"', captions='assets/setup.vtt')
    config.update(overrides)
    return '\n```video\n' + json.dumps(config) + '\n```\n'


class LocalVideoTests(unittest.TestCase):
    def fixture(self, root):
        md = root / 'course1/sprints/sprint-99/tuple-overview.md'
        manifest = root / 'course1/manifests/production.json'
        write_page(md)
        write_manifest(manifest)
        assets = md.parent / 'assets'
        assets.mkdir()
        (assets / 'setup.mp4').write_bytes(b'original video fixture')
        (assets / 'setup.vtt').write_text('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nSet up your coach.\n')
        md.write_text(md.read_text() + block())
        return md, manifest, assets

    def test_accessible_player_and_escaped_title(self):
        rendered = markdown_body_to_html(block())
        self.assertIn('<video controls preload="metadata" playsinline', rendered)
        self.assertIn('aria-label="Setup &lt;coach&gt; &quot;video&quot;"', rendered)
        self.assertIn('kind="captions"', rendered)
        self.assertIn('srclang="en" label="English" default', rendered)
        self.assertIn('download>Download video</a>', rendered)
        self.assertNotIn('<coach>', rendered)

    def test_copy_hash_recovery_paths_and_restored_missing_asset(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            md, manifest, assets = self.fixture(root)
            self.assertEqual(validate_artifact(md), [])
            output = root / 'site'
            first = render_hosted_artifact(md, manifest, output)
            paths = artifact_hosted_output_paths(md, manifest, output)
            self.assertEqual(len(paths), 3)
            self.assertEqual(set(map(str, paths)), {item['path'] for item in first['outputs']})
            html = paths[0].read_text()
            for asset in paths[1:]:
                self.assertTrue(asset.exists())
                self.assertIn(asset.name, html)
            self.assertNotIn('href="assets/setup.mp4"', html)
            self.assertFalse(render_hosted_artifact(md, manifest, output)['changed'])
            paths[1].unlink()
            self.assertTrue(render_hosted_artifact(md, manifest, output)['changed'])
            self.assertTrue(paths[1].exists())
            (assets / 'setup.vtt').write_text('WEBVTT\n\n00:00:00.000 --> 00:00:01.000\nUpdated caption.\n')
            second = render_hosted_artifact(md, manifest, output)
            self.assertNotEqual(first['hosted_hash'], second['hosted_hash'])
            self.assertTrue(paths[2].exists())

    def test_block_validation_rejects_unsafe_paths_and_bad_shape(self):
        for overrides in [dict(src='../private.mp4'), dict(src='assets/../private.mp4'),
                          dict(src='https://example.org/file.mp4'), dict(src='assets/%2e%2e/private.mp4'),
                          dict(captions='assets/script.js'), dict(title=''), dict(src=42),
                          dict(src='assets/setup.mp4?token=private')]:
            with self.subTest(overrides=overrides), self.assertRaises(ValueError):
                markdown_body_to_html(block(**overrides))
        with self.assertRaises(ValueError):
            markdown_body_to_html('\n```video\n{invalid}\n```\n')
        with self.assertRaises(ValueError):
            markdown_body_to_html('\n```video\n{"src":"assets/setup.mp4"}\n```\n')

    def test_missing_asset_bad_captions_and_symlink_fail_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            md, manifest, assets = self.fixture(root)
            (assets / 'setup.vtt').write_text('not captions')
            self.assertTrue(any('WebVTT' in error for error in validate_artifact(md)))
            (assets / 'setup.vtt').unlink()
            self.assertTrue(any('missing local image' in error for error in validate_artifact(md)))
            outside = root / 'private.vtt'
            outside.write_text('WEBVTT\n')
            (assets / 'setup.vtt').symlink_to(outside)
            self.assertTrue(any('inside adjacent assets' in error for error in validate_artifact(md)))

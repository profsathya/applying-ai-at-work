from pathlib import Path
import tempfile
import unittest

from canvas_sync.hosted_html import (render_hosted_artifact, artifact_hosted_output_paths, markdown_body_to_html)
from canvas_sync.local_images import local_image_assets
from canvas_sync.schema import validate_artifact
from tests.test_hosted_html import write_page, write_manifest


class LocalImageTests(unittest.TestCase):
    def test_copy_hash_change_and_publish_recovery_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            md = root / 'course1/sprints/sprint-99/tuple-overview.md'
            manifest = root / 'course1/manifests/production.json'
            write_page(md); write_manifest(manifest)
            image = md.parent / 'assets/example.webp'
            image.parent.mkdir(); image.write_bytes(b'first image fixture')
            md.write_text(md.read_text() + '\n![Illustrative handoff](assets/example.webp)\n')
            output = root / 'site'
            first = render_hosted_artifact(md, manifest, output)
            paths = artifact_hosted_output_paths(md, manifest, output)
            self.assertEqual(len(paths), 2)
            self.assertTrue(all(p.exists() for p in paths))
            self.assertEqual(paths[1].read_bytes(), image.read_bytes())
            self.assertIn(paths[1].name, paths[0].read_text())
            self.assertIn('alt="Illustrative handoff"', paths[0].read_text())
            self.assertFalse(render_hosted_artifact(md, manifest, output)['changed'])
            image.write_bytes(b'second image fixture')
            second = render_hosted_artifact(md, manifest, output)
            self.assertNotEqual(first['hosted_hash'], second['hosted_hash'])
            new_paths = artifact_hosted_output_paths(md, manifest, output)
            self.assertNotEqual(paths[1], new_paths[1])
            self.assertTrue(paths[1].exists())  # The old page's asset remains available during recovery.
            self.assertEqual(set(p['path'] for p in second['outputs']), set(map(str, new_paths)))

    def test_missing_escape_symlink_and_remote_images(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); md = root / 'course1/sprints/sprint-99/tuple-overview.md'
            write_page(md)
            md.write_text(md.read_text()+'\n![Example](assets/missing.png)\n')
            self.assertTrue(any('missing local image' in e for e in validate_artifact(md)))
            with self.assertRaisesRegex(ValueError, 'inside adjacent assets'):
                local_image_assets(md, markdown_body_to_html('![No](../secret.png)'))
            (md.parent/'assets').mkdir(); outside=root/'secret.png';outside.write_bytes(b'secret')
            (md.parent/'assets/link.png').symlink_to(outside)
            with self.assertRaisesRegex(ValueError, 'inside adjacent assets'):
                local_image_assets(md, markdown_body_to_html('![No](assets/link.png)'))
            self.assertEqual(local_image_assets(md, markdown_body_to_html('![Remote](https://example.org/a.png)')), [])

    def test_duplicate_and_reference_images_copy_once(self):
        with tempfile.TemporaryDirectory() as directory:
            md=Path(directory)/'page.md';(md.parent/'assets').mkdir()
            (md.parent/'assets/a.png').write_bytes(b'png fixture')
            rendered=markdown_body_to_html('![One][picture]\n\n![Two](assets/a.png)\n\n[picture]: assets/a.png')
            self.assertEqual(len(local_image_assets(md,rendered)),1)

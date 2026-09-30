"""Position is publication order, never learner completion or directory order."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from tests.test_hosted_html import write_page, write_manifest
from canvas_sync.hosted_html import render_hosted_files
from canvas_sync.item_sequence import live_sequences, source_sequences, sequence_label, update_sequence_line
from canvas_sync.hosted_html import render_artifact_document, _render_ai_activity_wrapper_document


class ItemSequenceTests(unittest.TestCase):
    def test_sparse_positions_optional_items_and_visibility(self):
        modules = [{'id': 1, 'published': True, 'name': 'Current'},
                   {'id': 2, 'published': True, 'name': 'Historic'},
                   {'id': 3, 'published': False, 'name': 'Draft'}]
        items = {1: [dict(id=10, position=2, published=True, type='Page'),
                     dict(id=11, position=5, published=False, type='Assignment'),
                     dict(id=12, position=8, published=True, type='SubHeader'),
                     dict(id=13, position=15, published=True, type='Quiz'),
                     dict(id=14, position=21, published=True, type='Discussion')],
                 2: [dict(id=20, position=1, published=True, type='Page')],
                 3: [dict(id=30, position=1, published=True, type='Page')]}
        positions = live_sequences(modules, items, hidden_modules={'Historic'})
        self.assertEqual(positions, {10: (1, 3), 13: (2, 3), 14: (3, 3)})
        self.assertEqual(sequence_label(positions[10]), 'Item 1 of 3 · 2 items remaining')
        self.assertEqual(sequence_label(positions[13]), 'Item 2 of 3 · 1 item remaining')
        self.assertEqual(sequence_label(positions[14]), 'Item 3 of 3 · 0 items remaining')
        self.assertEqual(sequence_label((1, 1)), 'Item 1 of 1 · 0 items remaining')

    def test_replacement_and_cross_folder_preview(self):
        def item(identity, module='Sprint 1', position=1, **kwargs):
            return (identity, dict(artifact_id=identity, type='page', module=module,
                                   position=position, publish=True, **kwargs))
        old = item('old', position=3)
        old[1]['publish'] = False
        rows = [item('first'), old,
                item('replacement', position=30, walkthrough_after='old', sprint=16),
                item('last', position=9), item('other', module='Sprint 2', sprint=15)]
        self.assertEqual(source_sequences(rows), {'first': (1, 3), 'replacement': (2, 3),
                                                   'last': (3, 3), 'other': (1, 1)})
        rows.pop(0)
        self.assertEqual(source_sequences(rows)['replacement'], (1, 2))
        self.assertNotIn('other', source_sequences(rows, hidden_modules={'Sprint 2'}))

    def test_refresh_changes_only_annotation_and_is_idempotent(self):
        original = '<h1>Keep this title</h1>\n<p>Released content, not a new draft.</p>'
        updated = update_sequence_line(original, (2, 3))
        self.assertIn('Item 2 of 3 · 1 item remaining', updated)
        self.assertIn('<h1>Keep this title</h1>', updated)
        self.assertIn('<p>Released content, not a new draft.</p>', updated)
        self.assertEqual(update_sequence_line(updated, (2, 3)), updated)
        moved = update_sequence_line(updated, (1, 1))
        self.assertNotIn('Item 2', moved)
        self.assertEqual(moved.count('class="item-sequence"'), 1)
        self.assertNotIn('item-sequence', update_sequence_line(moved, None))

    def test_partial_render_refreshes_siblings_without_publishing_draft_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "course1/manifests/production.json"
            write_manifest(manifest)
            first = root / "course1/sprints/sprint-99/first.md"
            second = root / "course1/sprints/sprint-99/second.md"
            write_page(first)
            write_page(second)
            second.write_text(second.read_text().replace('tuple-overview', 'second').replace('Tuple Overview', 'Second'))
            output = root / "site"
            result = render_hosted_files(manifest, output, [first, second], include_indexes=False,
                                        item_positions={'tuple-overview': (1, 2), 'second': (2, 2)})
            sibling = Path(result['rendered'][1]['output_path'])
            released = sibling.read_text()
            second.write_text(second.read_text().replace('Tuples store ordered values', 'UNRELEASED DRAFT'))
            updated = render_hosted_files(manifest, output, [first], include_indexes=False,
                                         item_positions={'tuple-overview': (2, 2), 'second': (1, 2)})
            self.assertIn('Item 1 of 2 · 1 item remaining', sibling.read_text())
            self.assertNotIn('UNRELEASED DRAFT', sibling.read_text())
            self.assertEqual(update_sequence_line(released, (1, 2)), sibling.read_text())
            self.assertTrue(any(row.get('sequence_only') for row in updated['rendered']))

    def test_live_render_failure_rolls_back_partial_files_and_new_assets(self):
        from canvas_sync.hosted_html import render_published_hosted_files
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "course1/manifests/production.json"
            write_manifest(manifest)
            output = root / "site"
            course = output / "deanza/course1"
            course.mkdir(parents=True)
            page = course / "home.html"
            page.write_text("Previous release")
            new_asset = course / "new-asset.svg"

            def partial_render(*args, **kwargs):
                page.write_text("Incomplete release")
                new_asset.write_text("New asset")
                raise RuntimeError("render interrupted")

            with patch("canvas_sync.hosted_html._published_item_positions", return_value={}), \
                 patch("canvas_sync.hosted_html.render_hosted_files", side_effect=partial_render):
                with self.assertRaisesRegex(RuntimeError, "render interrupted"):
                    render_published_hosted_files(manifest, output, [])
            self.assertEqual(page.read_text(), "Previous release")
            self.assertFalse(new_asset.exists())

    def test_both_heading_renderers_preserve_title_and_wrap_on_mobile(self):
        fm = dict(type='page', title='A long authored title', module='Sprint 1', sprint=1,
                  slug='example', points=None)
        info = dict(hosted_path='course1/sprint-1/example.html', hosted_url='https://example.org/example')
        for renderer in (render_artifact_document, _render_ai_activity_wrapper_document):
            document = renderer(fm, '## Learn\n\nContent.', {}, info, item_position=(1, 2))
            self.assertIn('<h1>A long authored title</h1>\n    <p class="item-sequence"', document)
            self.assertIn('Item 1 of 2 · 1 item remaining', document)
            line = document.split('class="item-sequence"', 1)[1].split('</p>', 1)[0]
            self.assertNotIn('white-space', line)
            self.assertNotIn('width:', line)


if __name__ == '__main__':
    unittest.main()

from pathlib import Path
import tempfile
import unittest

from canvas_sync.publish_targets import resolve_artifact_files, resolve_targets


class PublishTargetTests(unittest.TestCase):
    def test_push_artifact_scope_contains_only_changed_course_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for path in (
                'course1/sprints/sprint-15/activity.md',
                'course1/sprints/sprint-15/notes.txt',
                'course1/homepage.yaml',
            ):
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('')
            changed = [
                'course1/sprints/sprint-15/activity.md',
                'course1/sprints/sprint-15/notes.txt',
                'course1/homepage.yaml',
                '../outside/sprints/sprint-1/escape.md',
                '/absolute/course1/sprints/sprint-1/escape.md',
            ]
            self.assertEqual(resolve_artifact_files(root, changed), ['course1/sprints/sprint-15/activity.md'])

    def test_automatic_publish_scope_does_not_expand_beyond_changed_course(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'course1/manifests').mkdir(parents=True)
            (root / 'course1/manifests/production.json').write_text('{}')
            self.assertEqual(
                resolve_targets(root, ['course1/sprints/sprint-15/activity.md', 'canvas_sync/push.py']),
                ['course1/manifests/production.json'],
            )


if __name__ == '__main__':
    unittest.main()

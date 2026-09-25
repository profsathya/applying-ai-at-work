import unittest
from hashlib import sha256
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import patch

from canvas_sync.course_context import build_release, learner_content, released_source
from canvas_sync.state import canvas_fingerprint


def fixture():
    live = {'title': 'Welcome', 'body': 'Published', 'published': True, 'html_url': 'https://canvas.example/pages/welcome'}
    return dict(artifacts={'a.md': {'canvas_type': 'page', 'canvas_page_url': 'welcome', 'canvas_module_id': 1, 'content_hash': 'hash', 'canvas_fingerprint': canvas_fingerprint(live, 'page'), 'hosted_path': 'course1/activities/welcome.html'}},
                sources={'a.md': {'frontmatter': {'type': 'page', 'sprint': 6, 'slug': 'welcome', 'title': 'Welcome', 'publish': True}, 'body': 'Published', 'content_hash': 'hash'}},
                modules=[{'id': 1, 'published': True, 'position': 1}],
                items={1: [{'type': 'Page', 'page_url': 'welcome', 'published': True, 'position': 1}]}, objects={'a.md': live})


class CourseContextTests(unittest.TestCase):
    def test_release_deterministic_and_relative_path(self):
        args = fixture()
        a = build_release(**args, generated_at='first')
        b = build_release(**args, generated_at='second')
        assert a['release_id'] == b['release_id']
        assert a['pages'][0]['path'] == 'activities/welcome.html'
        assert a['pages'][0]['content'] == 'Published\n'


    def test_unpublished_content_excluded_and_visible_source_mismatch_fails(self):
        for change in ['local_unpublished', 'module_unpublished', 'item_unpublished', 'object_unpublished']:
            with self.subTest(change=change):
                args = fixture()
                if change == 'local_unpublished': args['sources']['a.md']['frontmatter']['publish'] = False
                if change == 'module_unpublished': args['modules'][0]['published'] = False
                if change == 'item_unpublished': args['items'][1][0]['published'] = False
                if change == 'object_unpublished': args['objects']['a.md']['published'] = False
                if change in ('local_unpublished', 'object_unpublished'):
                    with self.assertRaises(ValueError): build_release(**args)
                else:
                    with self.assertRaisesRegex(ValueError, 'No verified'): build_release(**args)


    def test_drift_fails_closed(self):
        for change in ['local', 'live', 'missing_fingerprint', 'missing_live']:
            with self.subTest(change=change):
                args = fixture()
                if change == 'local': args['sources']['a.md']['content_hash'] = 'edited'
                if change == 'live': args['objects']['a.md']['body'] = 'Canvas edit'
                if change == 'missing_fingerprint': del args['artifacts']['a.md']['canvas_fingerprint']
                if change == 'missing_live': args['objects'] = {}
                with self.assertRaises(ValueError): build_release(**args)


    def test_explicit_learner_allowlist(self):
        fm = {'guided_assignment': {'purpose': 'Purpose', 'feedback_endpoint': 'SECRET', 'tasks': [
            {'prompt': 'Choose', 'kind': 'choice', 'options': ['Alpha', 'Beta'], 'criteria': ['ANSWER KEY'], 'correct_index': 1, 'explanation': 'SECRET'},
            {'prompt': 'Explain', 'criteria': ['Use evidence'], 'system': 'SECRET'}]},
            'ai_activity': {'system': 'SECRET', 'questions': [{'prompt': 'Reflect', 'answer': 'SECRET'}]},
            'questions': [{'prompt': 'Question', 'answers': [{'text': 'Visible', 'correct': True}], 'explanation': 'SECRET'}]}
        text = learner_content(fm, 'Body')
        for expected in ['Purpose', 'Choose', 'Alpha', 'Explain', 'Use evidence', 'Reflect', 'Question', 'Visible']: assert expected in text
        for excluded in ['SECRET', 'ANSWER KEY', 'correct']: assert excluded not in text


    def test_missing_retired_source_does_not_block_but_published_does(self):
        args = fixture()
        args['artifacts']['course1/sprints/sprint-0/retired.md'] = {}
        assert len(build_release(**args)['pages']) == 1
        args['artifacts']['course1/sprints/sprint-6/welcome.md'] = dict(args['artifacts']['a.md'])
        with self.assertRaisesRegex(ValueError, 'Missing local source'):
            build_release(**args)

    def test_visible_module_is_included_regardless_of_storage_sprint(self):
        args = fixture()
        args['sources']['a.md']['frontmatter']['sprint'] = 17
        assert len(build_release(**args)['pages']) == 1
        # A removed module item cannot survive in the next inventory.
        args['items'][1] = []
        with self.assertRaisesRegex(ValueError, 'No verified'): build_release(**args)

    def test_released_source_uses_recorded_commit_when_working_copy_is_newer(self):
        published = b'---\ntype: page\ntitle: Published\npublish: true\n---\n\nPublished body\n'
        draft = b'---\ntype: page\ntitle: Draft\npublish: true\n---\n\nDraft body\n'
        entry = {'content_hash': sha256(published).hexdigest(), 'source_commit': 'a' * 40}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'page.md').write_bytes(draft)
            with patch('canvas_sync.course_context.subprocess.run', return_value=subprocess.CompletedProcess([], 0, published)) as git_show:
                source = released_source(root, 'page.md', entry)
            assert source['frontmatter']['title'] == 'Published'
            assert source['body'] == 'Published body\n'
            git_show.assert_called_once()
            with patch('canvas_sync.course_context.subprocess.run', return_value=subprocess.CompletedProcess([], 0, draft)):
                with self.assertRaisesRegex(ValueError, 'does not match released hash'):
                    released_source(root, 'page.md', entry)
            with self.assertRaisesRegex(ValueError, 'no source commit'):
                released_source(root, 'page.md', {'content_hash': entry['content_hash']})

if __name__ == "__main__":
    unittest.main()

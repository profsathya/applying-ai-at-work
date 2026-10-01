import copy
import unittest
from unittest.mock import patch

from canvas_sync.hosted_html import iframe_shell
from canvas_sync.state import canvas_fingerprint
from maintenance.prepare_course180_repair import TARGETS, REVIEWED_HOSTED_HASHES, ReadOnlyClient, check_shell, digest, prepare


class Course180RepairTests(unittest.TestCase):
    def setUp(self):
        self.state = {'instance': {'course_id': 180, 'base_url': 'https://cti-courses.instructure.com/'},
                      'artifacts': {'unrelated': {'canvas_id': 7152, 'content_hash': 'untouched'}}}
        self.live, self.sources, self.released, self.hashes = {}, {}, {}, {}
        self.modules = [{'id': 2079, 'published': True}, {'id': 2081, 'published': True}, {'id': 2082, 'published': True}]
        self.items = {2079: [], 2081: [], 2082: []}
        for ident, (path, module, item) in TARGETS.items():
            title = f'Activity {ident}'
            is_page = ident == 3624
            raw = f'---\ntitle: {title}\npoints: {5 if ident in (7180, 7181) else 0}\npublish: {str(not is_page).lower()}\n---\n\nKeep instructions.\n'
            old = raw.replace('publish: true', 'publish: false') if ident in (7185, 7180, 7181) else raw.replace('publish: false', 'publish: true')
            self.sources[path], self.released[path] = raw, old
            url = f'https://profsathya.github.io/Common-Curriculum/deanza/course1/assignments/{ident}.html'
            published = ident in (7149, 7180, 7181)
            obj = {'page_id' if is_page else 'id': ident, 'title' if is_page else 'name': title,
                   'body' if is_page else 'description': iframe_shell(url, title), 'published': published}
            if not is_page:
                obj.update(points_possible=5 if ident in (7180, 7181) else 0, submission_types=['online_text_entry'],
                           grading_type='points' if ident in (7180, 7181) else 'pass_fail', assignment_group_id=429)
            self.live[ident] = obj
            previous = dict(obj, published=ident in (7149, 3624))
            self.state['artifacts'][str(ident)] = {
                'canvas_id': ident, 'canvas_type': 'page' if is_page else 'assignment', 'local_path': path,
                'canvas_module_id': module, 'canvas_module_item_id': item, 'content_hash': digest(old),
                'canvas_fingerprint': canvas_fingerprint(previous, 'page' if is_page else 'assignment'),
                'source_commit': 'a' * 40, 'hosted_hash': f'hosted-{ident}', 'hosted_url': url}
            self.hashes[ident] = f'hosted-{ident}'
            placement = {'id': item, 'position': len(self.items[module]) + 1, 'published': published,
                         'type': 'Page' if is_page else 'Assignment'}
            placement.update({'page_url': 'the-problem-frame'} if is_page else {'content_id': ident})
            self.items[module].append(placement)
        # Simulate Canvas's equivalent serializer change on the staged wrapper.
        self.live[7185]['description'] = self.live[7185]['description'].replace(
            'border:0; width:100%; min-height:900px;', 'width: 100%; min-height: 900px; border: 0px none currentcolor;')

    def run_plan(self):
        return prepare(self.state, self.live, self.modules, self.items, self.sources,
                       self.released, self.hashes, 'b' * 40)

    def test_scoped_baseline_preserves_original_and_staged_release_hash(self):
        before = copy.deepcopy(self.state)
        proposal, report = self.run_plan()
        self.assertEqual(self.state, before)
        self.assertEqual(proposal['artifacts']['7149'], before['artifacts']['7149'])
        self.assertEqual(proposal['artifacts']['unrelated'], before['artifacts']['unrelated'])
        self.assertEqual(proposal['artifacts']['7185']['content_hash'], before['artifacts']['7185']['content_hash'])
        self.assertNotEqual(proposal['artifacts']['7185']['canvas_fingerprint'], before['artifacts']['7185']['canvas_fingerprint'])
        self.assertFalse(report['brainstorm_published'])
        self.assertEqual({x['field'] for x in report['changes']}, {'canvas_fingerprint', 'content_hash', 'source_commit'})
        self.assertEqual({x['canvas_id'] for x in report['changes']}, {7185, 3624, 7180, 7181})

    def test_post_publication_records_only_freshly_verified_release(self):
        self.live[7185]['published'] = True
        self.items[2079][1]['published'] = True
        proposal, report = self.run_plan()
        entry = proposal['artifacts']['7185']
        self.assertEqual(entry['content_hash'], digest(self.sources[TARGETS[7185][0]]))
        self.assertEqual(entry['source_commit'], 'b' * 40)
        self.assertTrue(report['brainstorm_published'])

    def test_rejects_grading_overrides_source_hosted_and_placement_changes(self):
        changes = [
            lambda: self.live[7185].update(assignment_group_id=999),
            lambda: self.live[7185].update(has_overrides=True),
            lambda: self.live[7185].update(due_at='2026-10-05'),
            lambda: self.live[7180].update(points_possible=99),
            lambda: self.live[7149].update(published=False),
            lambda: self.hashes.update({7185: 'new-html'}),
            lambda: self.sources.update({TARGETS[7180][0]: self.sources[TARGETS[7180][0]] + 'New content'}),
            lambda: self.items[2079].append(dict(self.items[2079][1], id=999)),
            lambda: self.items[2079][1].update(published=True),
            lambda: self.modules[0].update(published=False),
            lambda: self.state['instance'].update(course_id=999),
            lambda: self.state['artifacts']['3624'].update(canvas_fingerprint='unexplained'),
        ]
        for change in changes:
            self.setUp()
            change()
            with self.assertRaises(ValueError):
                self.run_plan()

    def test_shell_rejects_target_content_or_behavior_changes(self):
        entry = self.state['artifacts']['7185']
        check_shell(self.live[7185], 'Activity 7185', entry['hosted_url'])
        for change in [lambda s: s.replace('?context=canvas', '?context=web'),
                       lambda s: s + '<p>Changed instructions</p>',
                       lambda s: s.replace('<iframe ', '<iframe onload="alert(1)" '),
                       lambda s: s.replace('height="900"', 'height="100"')]:
            obj = dict(self.live[7185], description=change(self.live[7185]['description']))
            with self.assertRaises(ValueError):
                check_shell(obj, 'Activity 7185', entry['hosted_url'])

    def test_token_changes_when_live_evidence_changes(self):
        token = self.run_plan()[1]['review_token']
        self.live[7180]['updated_at'] = 'new timestamp'
        self.assertNotEqual(token, self.run_plan()[1]['review_token'])

    def test_client_refuses_writes_and_student_endpoints_before_transport(self):
        client = ReadOnlyClient('https://cti-courses.instructure.com', 'not-a-token', 180)
        with patch('requests.request') as request:
            for method, path in [('PUT', 'assignments/7185'), ('GET', 'assignments/7149/submissions'),
                                 ('GET', 'users'), ('GET', 'assignments/9999')]:
                with self.assertRaises(ValueError):
                    client._request_response(method, path)
            request.assert_not_called()

    def test_only_explicitly_reviewed_hosted_variations_are_preserved(self):
        for ident, reviewed in REVIEWED_HOSTED_HASHES.items():
            self.hashes[ident] = reviewed
        proposal, report = self.run_plan()
        self.assertEqual(set(report['preserved_hosted_differences']), {7149, 3624, 7180, 7181})
        for ident in REVIEWED_HOSTED_HASHES:
            self.assertEqual(proposal['artifacts'][str(ident)]['hosted_hash'], self.state['artifacts'][str(ident)]['hosted_hash'])
        self.hashes[7180] = 'unreviewed edit'
        with self.assertRaisesRegex(ValueError, 'hosted HTML changed'):
            self.run_plan()

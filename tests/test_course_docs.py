import unittest
from canvas_sync.course_docs.sync import build, verify_response


class CourseDocsTests(unittest.TestCase):
    def release(self):
        return {'schema_version': 1, 'release_id': 'released', 'generated_at': '2026-09-16T00:00:00Z',
                'pages': [{'path': 'activities/start.html', 'title': 'Start', 'source_url': 'https://example.org/start', 'content': 'Approved question?'}]}

    def test_only_explicit_content_and_order(self):
        result = build(self.release(), None, 3, 'owner/repo', 'sha')
        self.assertEqual([s['tab'] for s in result['sections']], ['Course'])
        self.assertIn('Source: https://example.org/start', result['sections'][0]['pages'][0]['content'])

    def test_empty_release_removes_withdrawn_content(self):
        release = self.release(); release['pages'] = []
        self.assertEqual(build(release, None, 3, 'owner/repo', 'sha')['sections'][0]['pages'], [])

    def test_core_only(self):
        result = build(None, 'DOJO CORE v1\nAsk one question.', 3, 'owner/repo', 'sha')
        self.assertEqual([s['tab'] for s in result['sections']], ['Dojo'])
        self.assertEqual(len(result['sections'][0]['pages']), 1)

    def test_invalid_inventory_fails_before_payload(self):
        release = self.release(); release['pages'][0]['path'] = '../draft.html'
        with self.assertRaises(ValueError): build(release, None, 3, 'owner/repo', 'sha')

    def test_response_must_confirm_exact_version(self):
        payload = build(self.release(), None, 3, 'owner/repo', 'sha')
        response = {'ok': True, 'document_id': 'doc', 'versions': {'Course': {'generation': 3, 'content_digest': payload['sections'][0]['content_digest'], 'rendered_digest': payload['sections'][0]['rendered_digest']}}}
        verify_response(payload, response, 'doc')
        response['versions']['Course']['generation'] = 2
        with self.assertRaises(ValueError): verify_response(payload, response, 'doc')

    def test_timestamp_does_not_change_section_digest(self):
        first = build(self.release(), None, 3, 'owner/repo', 'sha')
        second = build(self.release(), None, 4, 'owner/repo', 'newsha')
        self.assertEqual(first['sections'][0]['content_digest'], second['sections'][0]['content_digest'])

class PreparedReleaseTests(unittest.TestCase):
    def test_mismatched_source_never_reaches_hosting_or_writes(self):
        import io
        import json
        import zipfile
        from unittest.mock import patch
        from canvas_sync.course_docs import prepare_release
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('course-context-release.json', json.dumps({'source_commit': 'wrong'}))
        run = {'id': 7, 'head_sha': 'right', 'head_branch': 'main', 'head_repository': {'full_name': 'owner/repo'}}
        responses = [{'workflow_runs': [run]}, {'artifacts': [{'id': 8, 'name': 'course-context-release', 'expired': False}]}, buffer.getvalue()]
        with patch.dict('os.environ', {'GITHUB_REPOSITORY': 'owner/repo'}), patch.object(prepare_release, 'api', side_effect=responses), patch.object(prepare_release.subprocess, 'run'), patch.object(prepare_release.Path, 'read_text', return_value=json.dumps({'release_artifact': 'course-context-release'})), patch.object(prepare_release.Path, 'write_bytes') as write:
            with self.assertRaisesRegex(ValueError, 'source differs'):
                prepare_release.main()
            write.assert_not_called()

    def test_artifact_path_traversal_is_not_extracted(self):
        import io
        import json
        import zipfile
        from unittest.mock import patch
        from canvas_sync.course_docs import prepare_release
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('../course-context-release.json', '{}')
        run = {'id': 7, 'head_sha': 'right', 'head_branch': 'main', 'head_repository': {'full_name': 'owner/repo'}}
        responses = [{'workflow_runs': [run]}, {'artifacts': [{'id': 8, 'name': 'course-context-release', 'expired': False}]}, buffer.getvalue()]
        with patch.dict('os.environ', {'GITHUB_REPOSITORY': 'owner/repo'}), patch.object(prepare_release, 'api', side_effect=responses), patch.object(prepare_release.subprocess, 'run'), patch.object(prepare_release.Path, 'read_text', return_value=json.dumps({'release_artifact': 'course-context-release'})):
            with self.assertRaisesRegex(ValueError, 'root release'):
                prepare_release.main()

class ReceiptAndRedirectTests(unittest.TestCase):
    def test_wrong_document_rejected(self):
        payload = build(None, 'DOJO CORE\nAsk first.', 3, 'owner/repo', 'sha')
        with self.assertRaisesRegex(ValueError, 'unexpected document'):
            verify_response(payload, {'ok': True, 'document_id': 'other'}, 'expected')

    def test_saved_text_digest_required(self):
        payload = build(None, 'DOJO CORE\nAsk first.', 3, 'owner/repo', 'sha')
        section = payload['sections'][0]
        response = {'ok': True, 'document_id': 'doc', 'versions': {'Dojo': {'generation': 3, 'content_digest': section['content_digest'], 'rendered_digest': 'wrong'}}}
        with self.assertRaisesRegex(ValueError, 'expected section version'):
            verify_response(payload, response, 'doc')

    def test_post_redirect_returns_get_receipt_without_token_body(self):
        from http.server import BaseHTTPRequestHandler, HTTPServer
        import threading
        import urllib.request
        seen = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                seen.append(('POST', self.rfile.read(int(self.headers['Content-Length']))))
                self.send_response(302); self.send_header('Location', '/receipt'); self.end_headers()
            def do_GET(self):
                seen.append(('GET', self.headers.get('Content-Length')))
                self.send_response(200); self.end_headers(); self.wfile.write(b'{"ok":true}')
            def log_message(self, *args): pass
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            request = urllib.request.Request(f'http://127.0.0.1:{server.server_port}/exec', data=b'{"token":"test-only"}')
            with urllib.request.urlopen(request) as response:
                self.assertEqual(response.read(), b'{"ok":true}')
            self.assertEqual(seen[1], ('GET', None))
        finally:
            server.shutdown(); server.server_close(); thread.join()


class DeploymentStatusTests(unittest.TestCase):
    def test_superseded_successful_deployment_still_verifies_release(self):
        from canvas_sync.course_docs.prepare_release import deployment_succeeded
        self.assertTrue(deployment_succeeded([{'state': 'inactive'}, {'state': 'success'}]))
        self.assertFalse(deployment_succeeded([{'state': 'failure'}, {'state': 'pending'}]))
        self.assertFalse(deployment_succeeded([]))

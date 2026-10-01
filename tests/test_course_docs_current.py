import json
import os
import unittest
from unittest.mock import patch
from canvas_sync.course_docs import prepare_release

class CurrentContextTests(unittest.TestCase):
    def test_current_refresh_requires_successful_current_hosting_before_canvas_reads(self):
        with patch.dict(os.environ, {'GH_TOKEN':'test'}), patch.object(prepare_release, 'api', side_effect=[{'sha':'a'*40}, []]), patch('canvas_sync.course_context.export_release') as export:
            with self.assertRaisesRegex(ValueError, 'has not deployed'):
                prepare_release.refresh_current_release({'hosted_repository':'owner/hosted'}, hosting_attempts=1)
            export.assert_not_called()

    def test_current_refresh_uses_get_only_client_and_current_state(self):
        def export(manifest, state, **kwargs):
            self.assertEqual(state.name, '.canvas-state')
            with self.assertRaisesRegex(ValueError, 'cannot write Canvas'):
                kwargs['client']._request_response('DELETE', 'assignments/1')
            return {'pages':[{'title':'Current item'}]}
        with patch.dict(os.environ, {'GH_TOKEN':'test','CANVAS_API_URL':'https://canvas.example','CANVAS_API_TOKEN':'test'}), patch.object(prepare_release, 'api', side_effect=[{'sha':'a'*40}, [{'id':7}], [{'state':'success'}]]), patch.object(prepare_release.Path, 'read_text', return_value=json.dumps({'instance':{'course_id':180}})), patch.object(prepare_release.Path, 'write_text'), patch.object(prepare_release.subprocess, 'check_output', return_value='b'*40), patch('canvas_sync.course_context.export_release', side_effect=export):
            result=prepare_release.refresh_current_release({'hosted_repository':'owner/hosted'})
            self.assertEqual(result['pages'],[{'title':'Current item'}])
            self.assertEqual(result['hosted_commit'],'a'*40)

if __name__ == '__main__':
    unittest.main()

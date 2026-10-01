import copy
import unittest
from unittest.mock import Mock
from canvas_sync import push
from maintenance.reconcile_course180_placements import PAIRS, reconcile

class ReleasedPlacementTests(unittest.TestCase):
    def setup_pair(self, pair, stale=True):
        original, removed, replacement, retained, module = pair
        self.client=Mock()
        self.client.list_modules.return_value=[{'id':module,'name':'Sprint'}, {'id':99,'name':'Other'}]
        self.items=[{'id':retained,'position':7,'type':'Assignment','content_id':replacement}, {'id':123,'position':9,'type':'Page'}]
        self.client.list_module_items.side_effect=lambda m:self.items if m==module else []
        self.client._request.return_value={'id':original}
        self.state={'source':{'canvas_id':original,'canvas_type':'assignment','canvas_module_id':module,'canvas_module_item_id':removed if stale else None}}
        self.kw={'module_name':'Sprint','current_item_id':retained,'current_content_id':replacement}
    def call(self):return push.walkthrough_position(self.client,'source',self.state,**self.kw)
    def test_all_eight_keep_live_position_with_stale_or_cleared_state(self):
        for pair in PAIRS:
            for stale in (True,False):
                with self.subTest(pair=pair,stale=stale):
                    self.setup_pair(pair,stale)
                    self.assertEqual(self.call(),(pair[4],None,7,[pair[3],123]))
                    self.assertEqual(self.client._request.call_args.args,('GET',f'assignments/{pair[0]}'))
                    self.client.add_module_item.assert_not_called()
    def test_missing_duplicate_moved_or_replaced_walkthrough_stops(self):
        for mode in ('missing','duplicate','moved','wrong_identity','original_replaced','original_missing'):
            with self.subTest(mode=mode):
                self.setup_pair(PAIRS[0])
                if mode=='missing':self.items.pop(0)
                if mode=='duplicate':self.items.append(dict(self.items[0],id=999))
                if mode=='moved':
                    moved=self.items[0];self.items=self.items[1:]
                    self.client.list_module_items.side_effect=lambda m:self.items if m==PAIRS[0][4] else [moved]
                if mode=='wrong_identity':self.items[0]['id']=999
                if mode=='original_replaced':self.items.append({'id':888,'position':10,'type':'Assignment','content_id':PAIRS[0][0]})
                if mode=='original_missing':self.client._request.return_value={}
                with self.assertRaises(ValueError):self.call()
    def test_new_walkthrough_cannot_use_missing_anchor(self):
        self.setup_pair(PAIRS[0]);self.kw['current_item_id']=None
        with self.assertRaises(ValueError):self.call()
    def test_reconciliation_changes_only_placement_metadata_and_is_idempotent(self):
        state={'instance':{'course_id':180,'base_url':'https://cti-courses.instructure.com/'},'artifacts':{}};progress={'canvasCourseId':180,'items':[]}
        for a,old,b,new,m in PAIRS:
            for ident,item in [(a,old),(b,new)]:
                state['artifacts'][str(ident)]={'canvas_id':ident,'canvas_type':'assignment','canvas_module_id':m,'canvas_module_item_id':item,'completion_requirement':'must_submit','points':50}
            progress['items'].append({'canvasType':'assignment','canvasId':a,'canvasModuleItemId':old,'completionRequirement':'must_submit'})
        untouched={'canvas_id':7149,'canvas_module_item_id':17977}
        state['artifacts']['brainstorm']=untouched
        before=copy.deepcopy(state);after,mapping=reconcile(state,progress)
        self.assertEqual(state,before)
        for a,old,b,new,m in PAIRS:
            expected=dict(before['artifacts'][str(a)],canvas_module_item_id=None)
            expected.pop('completion_requirement')
            self.assertEqual(after['artifacts'][str(a)],expected)
            self.assertEqual(after['artifacts'][str(b)],before['artifacts'][str(b)])
        self.assertEqual(after['artifacts']['brainstorm'],untouched)
        self.assertEqual(reconcile(after,mapping),(after,mapping))
        state['artifacts'][str(PAIRS[0][0])]['canvas_module_item_id']=777
        with self.assertRaises(ValueError):reconcile(state,progress)

class FinalPlacementVerificationTests(unittest.TestCase):
    """The final post-publish verifier must accept the same retired anchors."""
    setup_pair = ReleasedPlacementTests.setup_pair
    def verify(self):
        from tempfile import TemporaryDirectory
        from pathlib import Path
        from canvas_sync.walkthrough_release import verify_walkthrough_adjacency
        self.state['new'] = {'canvas_id': self.kw['current_content_id'],
                             'canvas_module_item_id': self.kw['current_item_id'],
                             'canvas_module_id': self.state['source']['canvas_module_id']}
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / 'new.md'
            path.write_text('---\nartifact_id: new\nwalkthrough_after: source\nmodule: Sprint\n---\n')
            return verify_walkthrough_adjacency(self.client, [path], {'artifacts': self.state})

    def test_final_verifier_accepts_all_eight_retired_anchors_without_writes(self):
        for pair in PAIRS:
            for stale in (True, False):
                with self.subTest(pair=pair, stale=stale):
                    self.setup_pair(pair, stale)
                    before = copy.deepcopy(self.items)
                    self.assertEqual(self.verify(), ['new'])
                    self.assertEqual(self.items, before)
                    self.client.update_module_item.assert_not_called()
                    self.client.update_assignment.assert_not_called()
                    self.client.delete_module_item.assert_not_called()

    def test_final_verifier_rejects_ambiguous_retired_placement(self):
        self.setup_pair(PAIRS[0], False)
        self.items.append(dict(self.items[0], id=999))
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            self.verify()

    def test_final_verifier_still_requires_adjacency_for_present_anchor(self):
        self.setup_pair(PAIRS[0])
        self.items.insert(0, {'id': PAIRS[0][1], 'position': 1, 'type': 'Assignment', 'content_id': PAIRS[0][0]})
        self.items.insert(1, {'id': 777, 'position': 3, 'type': 'Page'})
        with self.assertRaisesRegex(ValueError, 'directly below'):
            self.verify()

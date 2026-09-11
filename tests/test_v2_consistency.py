import unittest
from unittest.mock import Mock
from canvas_sync.push import enforce_module_order, push_quiz, push_discussion, canvas_payload_hash
from canvas_sync.hosted_html import _learning_goal, _submit_guidance

class V2ConsistencyTests(unittest.TestCase):
    def test_live_order_and_repeat_preserve_unselected_items(self):
        class Client:
            ids = [10, 30, 20, 99]
            writes = 0
            def list_module_items(self, module):
                return [{'id': x, 'position': 3*i+2} for i,x in enumerate(self.ids)]
            def update_module_item(self, module, item, payload):
                self.writes += 1
                self.ids.remove(item)
                index = next((i for i in range(len(self.ids)) if 3*i+2 >= payload['position']), len(self.ids))
                self.ids.insert(index,item)
        client=Client()
        desired=[({'canvas_module_id':1,'canvas_module_item_id':i,'position':p},p) for p,i in enumerate([10,20,30],1)]
        enforce_module_order(client, desired)
        self.assertEqual(client.ids,[10,20,30,99])
        writes=client.writes
        enforce_module_order(client, desired)
        self.assertEqual(client.writes,writes)

    def test_settings_only_quiz_keeps_questions(self):
        client=Mock()
        client.list_quiz_questions.return_value=[{'id':44,'question_type':'essay_question','question_text':'Explain.', 'points_possible':1}]
        client.update_quiz.return_value={'id':12}
        fm={'title':'Check','points':1,'quiz_type':'practice_quiz','allowed_attempts':-1,'questions':[{'type':'essay','prompt':'Explain.','points':1}]}
        push_quiz(client,fm,'body',12)
        self.assertEqual(client.update_quiz.call_args_list[0].args[1]['quiz_type'],'practice_quiz')
        self.assertEqual(client.update_quiz.call_args_list[0].args[1]['allowed_attempts'],-1)
        client.delete_quiz_question.assert_not_called();client.add_quiz_question.assert_not_called()

    def test_discussion_settings_and_hash(self):
        client=Mock();fm={'title':'Intro','points':0,'grading_type':'pass_fail','omit_from_final_grade':True}
        push_discussion(client,fm,'body',3)
        self.assertEqual(client.update_discussion.call_args.args[1]['assignment']['grading_type'],'pass_fail')
        self.assertTrue(client.update_discussion.call_args.args[1]['assignment']['omit_from_final_grade'])
        self.assertNotEqual(canvas_payload_hash(fm,'discussion',None),canvas_payload_hash({**fm,'grading_type':'points'},'discussion',None))

    def test_intro_display_directions(self):
        fm={'type':'discussion','title':'Introduction Post','learner_labels':True,'learning_goal':'Introduce your context.'}
        self.assertEqual(_learning_goal(fm),'Introduce your context.')
        self.assertIn('Peer replies are optional',_submit_guidance(fm,None))

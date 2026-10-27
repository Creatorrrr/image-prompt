import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import unittest
from photo_h_f2_source_relevance import order_source_relevance
from photo_h_f2_pose_answers import same_owner_arm_pair

class ExtraGuards(unittest.TestCase):
 def test_unmodeled_gaze_not_camera_question(self):
  _,t=order_source_relevance([], '여성의 몸은 카메라를 향해 어떻게 돌아가 있고, 시선은 어디를 향해 있어?', {})
  self.assertEqual(t['property_answer_lane']['intent'], {})
 def test_ingredient_layout_not_subject_position(self):
  _,t=order_source_relevance([], '재료를 놓은 정물 사진의 프레임 배치는 어떻게 되어 있어?', {})
  self.assertEqual(t['property_answer_lane']['intent'].get('requested_features'), ['composition_layout'])
 def test_seated_is_context(self):
  _,t=order_source_relevance([], 'Which parts stay sharp, and which parts fall out of focus in this seated portrait?', {})
  self.assertIn('seated_portrait',t['property_answer_lane']['intent'].get('context_anchors', []))
 def test_page_and_values_abstain(self):
  for q in ['How are the portrait variations arranged on the page?', 'Is the red hand sharp and the background blurred?']:
   _,t=order_source_relevance([],q,{})
   self.assertEqual(t['property_answer_lane']['intent'], {})
 def test_curly_apostrophe_and_quotation(self):
  self.assertIsNotNone(same_owner_arm_pair('The woman’s one arm rises while her other arm hangs.'))
  self.assertIsNone(same_owner_arm_pair('“One arm rises while her other arm hangs.”'))

import copy
import hashlib
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_source_relevance import compile_profiles, order_source_relevance, verify_source_relevance_trace

class ProductionTraceTests(unittest.TestCase):
 def setUp(self):
  text="The woman's face is sharp; the background is blurred."
  digest=hashlib.sha256(text.encode()).hexdigest()
  self.units=[{'pointer':'/content/en','literal_id':'actual-id','source_sha256':digest,'text':text}]
  self.effects={'properties':[{'property':'focus.face','target':'face sharp'}, {'property':'focus.background','target':'background blurred'}]}
  self.query="Is the woman's face sharp while the background is blurred?"
  self.rows=[{'id':f'{i}|base','cid':str(i),'rid':'base','rrf':1/(10+i)} for i in range(1,11)]
  self.profiles=compile_profiles({'10|base':''},source_units=lambda _:self.units,source_effects=lambda _:self.effects)
 def test_promoted_witness_and_replay_binding(self):
  ordered, trace=order_source_relevance(self.rows,self.query,self.profiles)
  self.assertEqual(ordered[0]['id'],'10|base')
  item=trace['top8_source_witnesses'][0]
  self.assertEqual(item['rank_before'],10)
  self.assertEqual(item['source_lane_contribution'],0)
  self.assertEqual(item['property_answer_contribution'],0)
  self.assertEqual(trace['property_answer_lane']['top8_witnesses'][0]['primary_metadata'],item['primary_metadata'])
  self.assertEqual(item['base_rrf'],self.rows[-1]['rrf'])
  self.assertEqual(item['primary_metadata']['/content/en'],{'literal_id':'actual-id','source_sha256':self.units[0]['source_sha256']})
  self.assertEqual(item['property_answer_witness']['common_primary_pointers'],['/content/en'])
  self.assertTrue(any(f['support']=='direct_primary_text_and_same_selected_rid_effect' for f in item['supported_features']))
  verify_source_relevance_trace(self.rows,self.query,self.profiles,trace)
  changed=copy.deepcopy(trace);changed['top8_source_witnesses'][0]['primary_metadata']['/content/en']['source_sha256']='0'*64
  with self.assertRaises(ValueError): verify_source_relevance_trace(self.rows,self.query,self.profiles,changed)
  changed=copy.deepcopy(trace);changed['top8_source_witnesses'][0]['property_answer_witness']['common_primary_pointers']=['/other']
  with self.assertRaises(ValueError): verify_source_relevance_trace(self.rows,self.query,self.profiles,changed)
  changed_profiles=copy.deepcopy(self.profiles);changed_profiles['10|base']['primary_metadata']['/content/en']['source_sha256']='0'*64
  with self.assertRaises(ValueError): verify_source_relevance_trace(self.rows,self.query,changed_profiles,trace)
 def test_new_lane_requires_question_and_single_lane_unaffected(self):
  _,trace=order_source_relevance(self.rows,'The face is sharp while the background is blurred.',self.profiles)
  self.assertEqual(trace['property_answer_lane']['candidate_count'],0)
  self.assertFalse(trace['single_property_lane']['applicable'])

if __name__=='__main__': unittest.main()

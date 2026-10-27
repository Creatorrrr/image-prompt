import hashlib,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_h_f2_source_relevance import compile_profiles,order_source_relevance,verify_source_relevance_trace
from photo_h_f2_property_answers import owned_support_query
class OwnedSupport(unittest.TestCase):
 def setUp(self):
  self.query='In the bench portrait, who is leaning on whom, and where is his arm?'
  self.text="A man and a woman sit on a bench. The man's arm rests along the bench back. She leans against his chest."
  self.effects={'properties':[{'property':'body.contact.back_to_chest','target':'woman and man'},{'property':'arm.position.man_arm','target':'man arm along bench back'}]}
 def units(self,text):return [{'pointer':'/content/en','literal_id':'a','source_sha256':hashlib.sha256(text.encode()).hexdigest(),'text':text}]
 def assess(self,text,effects):
  i='a|base';u=self.units(text);p=compile_profiles({i:''},source_units=lambda _:u,source_effects=lambda _:effects)
  rows=[{'id':i,'cid':'a','rid':'base','rrf':.01}];_,t=order_source_relevance(rows,self.query,p);verify_source_relevance_trace(rows,self.query,p,t);return t['owned_support_lane']['candidate_count']
 def test_positive_and_opposite_support_direction_unbound(self):
  self.assertEqual(self.assess(self.text,self.effects),1)
  self.assertEqual(self.assess("A man and a woman sit on a bench. The man's arm rests along the bench back. He leans against her chest.",self.effects),1)
 def test_no_effect_effect_only_wrong_arm_negation_and_unrelated(self):
  self.assertEqual(self.assess(self.text,{}),0)
  woman_effects={'properties':[{'property':'body.contact.back_to_chest','target':'woman and man'},{'property':'arm.position.woman_arm','target':'woman arm on bench'}]}
  self.assertEqual(self.assess(self.text,woman_effects),0)
  generic_wrong={'properties':[{'property':'body.contact.back_to_chest','target':'woman and man'},{'property':'arm.position','target':"woman's arm behind man"}]}
  self.assertEqual(self.assess(self.text,generic_wrong),0)
  self.assertEqual(self.assess('A man and a woman sit on a bench.',self.effects),0)
  self.assertEqual(self.assess("A man and a woman sit on a bench. The woman's arm rests along the bench back. She leans against his chest.",self.effects),0)
  self.assertEqual(self.assess("A man and a woman sit on a bench. The man's arm rests along the bench back. She does not lean against his chest.",self.effects),0)
  self.assertEqual(self.assess("A man and a woman sit on a bench. The man's arm rests along the bench back. They smile.",self.effects),0)
 def test_support_and_arm_cannot_cross_primary_units(self):
  a=self.units("A man and woman sit on a bench. The man's arm rests along the bench back.")
  b=self.units('A man and woman sit on a bench. She leans against his chest.')
  b[0]['pointer']='/content/ko';u=a+b;i='a|base'
  p=compile_profiles({i:''},source_units=lambda _:u,source_effects=lambda _:self.effects)
  _,t=order_source_relevance([{'id':i,'cid':'a','rid':'base','rrf':.01}],self.query,p)
  self.assertEqual(t['owned_support_lane']['candidate_count'],0)
 def test_effects_not_borrowed_from_another_rid(self):
  u=self.units(self.text);v=self.units('A man and woman sit on a bench.')
  units={'a|base':u,'b|base':v};profiles=compile_profiles(units,source_units=lambda i:units[i],source_effects=lambda i:self.effects if i=='b|base' else {})
  rows=[{'id':i,'cid':i[0],'rid':'base','rrf':.01} for i in units];_,t=order_source_relevance(rows,self.query,profiles)
  self.assertEqual(t['owned_support_lane']['candidate_count'],0)
 def test_unmodeled_additional_constraints_abstain(self):
  i='a|base';u=self.units(self.text);p=compile_profiles({i:''},source_units=lambda _:u,source_effects=lambda _:self.effects)
  rows=[{'id':i,'cid':'a','rid':'base','rrf':.01}]
  for q in [self.query[:-1]+' in a red setting?', self.query[:-1]+' and what is the camera height?', self.query[:-1]+' when it is raised?']:
   _,t=order_source_relevance(rows,q,p)
   self.assertEqual(t['owned_support_lane']['candidate_count'],0)
 def test_bound_and_other_question_classes_abstain(self):
  for q in ["At the bench, the woman rests against the man. Whose arm runs along the backrest?",'벤치에서 여성이 남성의 가슴에 기대고 있어. 팔은 누구의 팔이야?', 'Find a man leaning on a woman on a bench.', 'Who is leaning on whom, and where is his arm?']:
   self.assertFalse(owned_support_query(q))
if __name__=='__main__': unittest.main()

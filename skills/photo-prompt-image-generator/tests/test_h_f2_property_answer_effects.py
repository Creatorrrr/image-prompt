import hashlib
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from photo_h_f2_source_relevance import compile_profiles, order_source_relevance

class FocusEffects(unittest.TestCase):
 def evaluate(self, units, effects, query="Is the woman's face sharp while the background is blurred?"):
  profiles=compile_profiles(units,source_units=lambda i:units[i],source_effects=lambda i:effects.get(i,{}))
  rows=[{'id':i,'cid':i.split('|')[0],'rid':i.split('|',1)[1],'rrf':.05} for i in units]
  return order_source_relevance(rows,query,profiles)[1]['property_answer_lane']
 def unit(self,text):
  return [{'pointer':'/content/en','literal_id':'source','source_sha256':hashlib.sha256(text.encode()).hexdigest(),'text':text}]
 def effects(self,*items):
  return {'properties':[{'property':p,'target':t} for p,t in items]}
 def test_requires_effect_and_direct_owner_bound_text(self):
  source=self.unit("The woman's face is sharp; the background is blurred.")
  good=self.effects(('focus.face','face sharp'),('focus.background','background blurred'))
  yes=self.evaluate({'x|base':source},{'x|base':good})
  self.assertEqual(yes['candidate_count'],1)
  witness=yes['top8_witnesses'][0]['witness']['witnesses']['focus_partition'][0]
  self.assertTrue(witness['effect_properties'])
  self.assertTrue(all('property' in p and 'target' in p for p in witness['effect_properties']))
  self.assertEqual(self.evaluate({'x|base':source},{})['candidate_count'],0)
  self.assertEqual(self.evaluate({'x|base':self.unit('A woman stands by a wall.')},{'x|base':good})['candidate_count'],0)
  self.assertEqual(self.evaluate({'x|base':self.unit("The woman's face is blurred; the background is sharp.")},{'x|base':good})['candidate_count'],0)
 def test_effect_cannot_cross_rid(self):
  source=self.unit("The woman's face is sharp; the background is blurred.")
  good=self.effects(('focus.face','face sharp'),('focus.background','background blurred'))
  trace=self.evaluate({'same|selected':source,'same|unselected':self.unit('A person stands.')},{'same|unselected':good})
  self.assertEqual(trace['candidate_count'],0)
 def test_seated_context_requires_posture_effect(self):
  source=self.unit('The seated woman has a sharp face; the background is blurred.')
  focus=self.effects(('focus.face','face sharp'),('focus.background','background blurred'))
  both=self.effects(('focus.face','face sharp'),('focus.background','background blurred'),('body.posture','seated woman'))
  q='Which parts stay sharp, and which parts fall out of focus in this seated portrait?'
  self.assertEqual(self.evaluate({'x|base':source},{'x|base':focus},q)['candidate_count'],0)
  wrong=self.effects(('focus.face','face sharp'),('focus.background','background blurred'),('body.posture','standing woman'))
  self.assertEqual(self.evaluate({'x|base':source},{'x|base':wrong},q)['candidate_count'],0)
  trace=self.evaluate({'x|base':source},{'x|base':both},q)
  self.assertEqual(trace['candidate_count'],1)
  context=trace['top8_witnesses'][0]['witness']['context_witnesses']['seated_portrait'][0]
  self.assertTrue(context['effect_properties'])
if __name__=='__main__': unittest.main()

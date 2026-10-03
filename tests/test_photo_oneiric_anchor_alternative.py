"""Preserve object/pattern/threshold comparison across the same local seam."""
import sys,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(S));import prompt_generator as g
PID='oneiric_dream_logic_discontinuity';FIELD='comparison_anchor_phrase'
NEW='the same distinctive object pattern or threshold appears on both sides'
OLD='the same distinctive object appears clearly on both sides of the seam'
class OneiricAnchorAlternativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  reg=g.load_visual_obligation_registry(S.parent/'assets/photo_prompt_visual_obligations.json');cls.p=next(p for p in reg['profiles']if p['id']==PID)
 def binding(self,text):
  return g.validate_visual_intent_binding(obligation_index=0,field=FIELD,phrase=text,requirement=self.p['evidence_requirements'][FIELD])
 def test_legacy_and_authored_alternative_bind(self):
  for branch in (OLD,NEW):self.binding(branch+' with identical diagonal spacing and an unbroken dark edge')
  self.assertEqual(self.p['evidence_requirements'][FIELD]['must_mention_any'],[OLD,NEW])
 def test_unrelated_pattern_not_comparison_evidence(self):
  with self.assertRaises(ValueError):self.binding('Different decorative patterns lie in unrelated rooms without shared identity or a continuous visible comparison')
 def test_all_five_groups_remain_required(self):
  c=self.p['semantics']['component_semantics'];self.assertEqual(c['minimum_component_groups'],5);self.assertEqual(len(c['required_group_ids']),5)
  terms=[x['any_terms'][0]for x in c['groups']];self.assertTrue(g.candidate_pack_visual_component_match(self.p,'; '.join(terms)))
  for i in range(5):self.assertIsNone(g.candidate_pack_visual_component_match(self.p,'; '.join(v for j,v in enumerate(terms)if j!=i)))
 def test_five_gates_and_nine_word_minimum_remain(self):
  self.assertEqual(len(self.p['render_gates']),5);self.assertEqual(self.p['evidence_requirements'][FIELD]['min_content_words'],9)

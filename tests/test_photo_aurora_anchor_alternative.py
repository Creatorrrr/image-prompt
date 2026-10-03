"""Retain the authored atmospheric anchor and legacy horizon label."""
import sys,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'skills/photo-prompt-image-generator/scripts'
sys.path.insert(0,str(S));import prompt_generator as g
class AuroraAnchorAlternativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  reg=g.load_visual_obligation_registry(S.parent/'assets/photo_prompt_visual_obligations.json')
  cls.p=next(p for p in reg['profiles']if p['id']=='auroral_arc_curtain_atmosphere')
 def test_old_label_preserved_new_label_additive(self):
  self.assertEqual(self.p['runtime_expression']['prompt_label_terms'],['auroral arcs and ray-filled curtains above a planetary horizon','auroral arcs and ray-filled curtains with an atmospheric anchor'])
 def test_gate_and_composition_allow_original_anchor_alternative(self):
  self.assertIn('planetary horizon or atmospheric layer',self.p['composition_instruction'])
  self.assertIn('planetary horizon or atmospheric layer',self.p['render_gates'][0]['description'])
 def test_strict_morphology_retained(self):
  c=self.p['semantics']['component_semantics'];self.assertEqual(c['required_group_ids'],['atmospheric_horizon','auroral_arc','curtain_folds','vertical_rays']);self.assertEqual(c['minimum_component_groups'],4)
  terms=[row['any_terms'][0]for row in c['groups']]
  self.assertEqual(g.candidate_pack_visual_component_match(self.p,'; '.join(terms)),'component_semantics')
  for i in range(4):self.assertIsNone(g.candidate_pack_visual_component_match(self.p,'; '.join(v for j,v in enumerate(terms)if i!=j)))

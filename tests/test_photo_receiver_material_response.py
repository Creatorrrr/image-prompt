"""Lighting contracts respect existing diffuse and glossy receivers."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

class ReceiverMaterialResponseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profiles=[p for p in reg['profiles'] if p['id'] in {'hard_light_shadow_edge_relation','soft_light_shadow_edge_relation'}]

    def test_complete_glossy_and_diffuse_component_variants(self):
        self.assertEqual(len(self.profiles),2)
        for p in self.profiles:
            groups=p['semantics']['component_semantics']['groups']
            for receiver in groups[3]['any_terms']:
                parts=[receiver if i==3 else g['any_terms'][0] for i,g in enumerate(groups)]
                self.assertTrue(pg.candidate_pack_visual_component_match(p,'; '.join(parts)))
                for i in range(5):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(v for j,v in enumerate(parts) if i!=j)))

    def test_receiver_evidence_and_gates_preserve_material(self):
        for p in self.profiles:
            req=p['evidence_requirements'][p['id']+'_component_4_phrase']
            self.assertEqual(req['min_content_words'],5)
            self.assertTrue(req['must_mention_any'][0].startswith('specular'))
            self.assertTrue(any(t.startswith('matte receivers retain diffuse') for t in req['must_mention_any']))
            self.assertIn('without adding gloss or another object',p['render_gates'][3]['description'])
            self.assertEqual(len(p['render_gates']),5)

    def test_single_relation_is_not_a_complete_paraphrase(self):
        for p in self.profiles:
            for g in p['semantics']['component_semantics']['groups'][:3]:
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,g['any_terms'][0]))
            for text in p['semantics']['paraphrase_examples']:
                self.assertTrue(pg.candidate_pack_visual_component_match(p,text))

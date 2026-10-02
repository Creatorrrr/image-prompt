"""Positive catalog alternatives must not trigger their own confound guards."""
import re
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

class ResidualPositiveGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profiles={p['id']:p for p in reg['profiles']}

    def test_korean_ghost_positive_retains_geometry_without_own_exclusion(self):
        p=self.profiles['human_ghost_identity_breach']
        terms=[]
        for g in p['semantics']['component_semantics']['groups']:
            terms.append(next((t for t in g['any_terms'] if re.search('[가-힣]',t)),g['any_terms'][0]))
        text='; '.join(terms)
        self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'component_semantics')
        self.assertIn('장면 기하가 일관되게 유지',text)
        self.assertIsNone(pg.candidate_pack_visual_component_match(p,text+'; 홀로그램'))
        self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],3)

    def test_regional_boubou_boundary_is_positive_and_guarded(self):
        p=self.profiles['west_african_grand_boubou_volume_system']
        groups=p['semantics']['component_semantics']['groups']
        text='; '.join(g['any_terms'][1 if i==4 else 0] for i,g in enumerate(groups))
        self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'component_semantics')
        for confound in ['agbada','caftan']:
            self.assertIsNone(pg.candidate_pack_visual_component_match(p,text+'; '+confound))
        self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],4)

    def test_repair_paraphrase_contains_complete_components(self):
        p=self.profiles['material_replacement_deferral_repair_cycle'];text=p['semantics']['paraphrase_examples'][0]
        self.assertEqual(pg.candidate_pack_visual_component_match(p,text),'component_semantics')
        self.assertIsNone(pg.candidate_pack_visual_component_match(p,text+'; decorative distressing'))
        self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],5)
        self.assertTrue(p['activation']['requires_adult_character'])

"""Render judgments preserve already-authored leading-path alternatives."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

class LeadingLineGateAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profile=next(p for p in reg['profiles'] if p['id']=='leading_line_target_continuity')

    def test_render_gate_keeps_existing_origin_alternative(self):
        g=next(g for g in self.profile['render_gates'] if g['id']=='vo_composition_line_origin_away')
        self.assertEqual(g['description'],'A physical line or aligned scene edge begins away from the primary subject.')

    def test_render_gate_keeps_existing_rhythmic_alternative(self):
        p=self.profile;g=next(g for g in p['render_gates'] if g['id']=='vo_composition_line_path_continuous')
        self.assertEqual(g['description'],'The line remains visibly continuous or rhythmically linked across the intervening frame.')
        self.assertTrue(any('rhythmically linked' in t for t in p['evidence_requirements']['line_continuity_phrase']['must_mention_any']))
        self.assertEqual(len(p['render_gates']),4)

    def test_existing_complete_components_and_missing_groups(self):
        p=self.profile;groups=p['semantics']['component_semantics']['groups']
        for lang in [0,1]:
            terms=[g['any_terms'][lang] for g in groups]
            self.assertTrue(pg.candidate_pack_visual_component_match(p,'; '.join(terms)))
            for i in range(len(terms)):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(t for j,t in enumerate(terms) if i!=j)))

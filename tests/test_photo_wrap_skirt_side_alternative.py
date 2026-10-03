"""Wrap-skirt evidence supports both already-defined overlap placements."""
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/photo-prompt-image-generator'
sys.path.insert(0,str(SKILL/'scripts'))
import prompt_generator as pg

class WrapSkirtSideAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg=pg.load_visual_obligation_registry(SKILL/'assets/photo_prompt_visual_obligations.json')
        cls.profile=next(p for p in reg['profiles'] if p['id']=='wrap_skirt_overlap_closure')

    def test_front_neutral_korean_and_explicit_side_variants(self):
        p=self.profile;groups=p['semantics']['component_semantics']['groups']
        for language in [0,1]:
            for alternative in [language,language+2]:
                parts=[g['any_terms'][alternative if i==2 else language] for i,g in enumerate(groups)]
                self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(parts)),'component_semantics')
                for i in range(5):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(t for j,t in enumerate(parts) if i!=j)))

    def test_evidence_keeps_front_and_adds_side_at_same_floor(self):
        req=self.profile['evidence_requirements']['diagonal_overlap_phrase']
        self.assertEqual(req['min_content_words'],10)
        self.assertEqual(req['must_mention_any'],[
            'one panel crosses diagonally over the other across the skirt front',
            'one panel crosses diagonally over the other across the skirt side'])
        self.assertEqual(len(self.profile['render_gates']),5)

    def test_side_does_not_relax_declared_confounds(self):
        p=self.profile;groups=p['semantics']['component_semantics']['groups']
        text='; '.join(g['any_terms'][2 if i==2 else 0] for i,g in enumerate(groups))
        self.assertEqual(p['semantics']['component_semantics']['minimum_component_groups'],5)
        for term in p['activation'].get('exclude_if_any_terms',[]):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p,text+'; '+term))

"""Positive dress examples should express construction without self-exclusion."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class DressPositiveParaphraseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in cls.registry['profiles'] if p['id'] == 'one_piece_dress_construction')

    def test_detailed_positive_example_matches_its_own_context(self):
        p = self.profile
        text = p['semantics']['paraphrase_examples'][7]
        self.assertIn('one continuous skirt-shaped dress silhouette', text)
        self.assertEqual(pg.visual_profile_context_applicability(p, text, has_authorial_core_context=True), (True, 'context_applicable'))
        self.assertEqual(pg.candidate_pack_visual_component_match(p, text), 'semantic_paraphrase_example')

    def test_seams_panels_closure_and_drape_remain_explicit(self):
        text = self.profile['semantics']['paraphrase_examples'][7]
        for phrase in ['neckline through bodice to skirt hem', 'waist seam or multiple panels', 'upper and lower parts remain one dress', 'Seams, overlapping closure and fabric drape']:
            self.assertIn(phrase, text)

    def test_adjacent_senses_remain_excluded(self):
        p = self.profile
        self.assertIn('trouser legs', p['activation']['context_disambiguation']['exclude_if_any_terms'])
        for text in ['dress garment with trouser legs', 'dress garment shown as swimwear product', 'dress garment from an anime franchise']:
            self.assertEqual(pg.visual_profile_context_applicability(p, text, has_authorial_core_context=True), (False, 'context_disambiguation_exclusion'))

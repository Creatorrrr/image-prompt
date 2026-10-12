"""Composition and review prose preserve existing environment alternatives."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class EnvironmentAlternativeConsistencyTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.registry = native_profile_registry()
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}

    def test_wetland_saturation_survives_materialization(self):
        p = self.profiles['cand_a32d99b4c0225e498880f853708517a5']
        o = pg.candidate_pack_visual_profile_obligation(p, self.registry, activation_source='test', source_intent_ids=[])
        self.assertIn('shallow water or visibly saturated low ground', o['composition_instruction'])
        soil = next((g for g in o['render_gates'] if g['id'] == 'vo_natural_wetland_soil_contact'))
        self.assertEqual(soil['description'], 'Exposed mud, dark saturated soil, or a soft waterlogged margin remains visible with plausible ground contact.')
        self.assertEqual(soil['review_scale'], 'native')

    def test_dune_transport_alternative_keeps_connected_geometry(self):
        p = self.profiles['cand_1c8b81fb31c45c2f81d1ab3bcb2fa7d4']
        o = pg.candidate_pack_visual_profile_obligation(p, self.registry, activation_source='test', source_intent_ids=[])
        self.assertIn('aligned fine sand ripples or short saltation traces', o['composition_instruction'])
        for phrase in ['oblique side view', 'gentle stoss slope', 'crest line', 'steep lee slip face', 'one connected dune body']:
            self.assertIn(phrase, o['composition_instruction'])

    def test_both_profiles_keep_all_four_required_components(self):
        for pid in ['cand_a32d99b4c0225e498880f853708517a5', 'cand_1c8b81fb31c45c2f81d1ab3bcb2fa7d4']:
            p = self.profiles[pid]
            c = p['semantics']['component_semantics']
            self.assertEqual(c['minimum_component_groups'], 4)
            self.assertEqual(len(c['required_group_ids']), 4)
            self.assertEqual(len(p['render_gates']), 5)
            parts = [g['any_terms'][0] for g in c['groups']]
            self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
            for missing in range(4):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join((v for i, v in enumerate(parts) if i != missing))))
from tests.photo_native_runtime import native_profile_registry

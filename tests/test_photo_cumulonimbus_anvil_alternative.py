"""Preserve authored anvil alternatives without weakening storm geometry."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class CumulonimbusAnvilAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in cls.registry['profiles'] if p['id'] == 'cumulonimbus_tower_anvil_precipitation_outflow')

    def test_materialized_composition_preserves_alternatives_and_complete_storm(self):
        obligation = pg.candidate_pack_visual_profile_obligation(self.profile, self.registry, activation_source='test', source_intent_ids=[])
        for phrase in ['wide vertical frame', 'low dark base', 'full convective tower', 'flattened fibrous or striated anvil', 'descending precipitation shaft', 'one connected cloud system']:
            self.assertIn(phrase, obligation['composition_instruction'])

    def test_all_four_components_and_five_render_gates_remain(self):
        p = self.profile
        c = p['semantics']['component_semantics']
        self.assertEqual(c['minimum_component_groups'], 4)
        self.assertEqual(len(c['required_group_ids']), 4)
        self.assertEqual(len(p['render_gates']), 5)
        self.assertIn('storm_severity_claim_from_pixels', p['reject_substitutes'])
        parts = [g['any_terms'][0] for g in c['groups']]
        self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
        for missing in range(4):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i, v in enumerate(parts) if i != missing)))

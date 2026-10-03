"""Preserve all authored glacier directional-surface alternatives."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class GlacierSurfaceAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in cls.registry['profiles'] if p['id'] == 'active_glacier_flow_valley_moraine_system')

    def test_three_surface_alternatives_materialize_without_losing_connected_geometry(self):
        obligation = pg.candidate_pack_visual_profile_obligation(self.profile, self.registry, activation_source='test', source_intent_ids=[])
        composition = obligation['composition_instruction']
        for phrase in ['wide down-valley or oblique view', 'U-shaped trough', 'continuous ice', 'crevasses, flow bands, or debris stripes', 'coherent down-valley surface direction', 'moraine debris', 'terminus meltwater', 'without hiding their contacts']:
            self.assertIn(phrase, composition)

    def test_all_four_existing_components_remain_required(self):
        p = self.profile
        c = p['semantics']['component_semantics']
        self.assertEqual(c['minimum_component_groups'], 4)
        self.assertEqual(len(c['required_group_ids']), 4)
        parts = [g['any_terms'][0] for g in c['groups']]
        self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
        for missing in range(4):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i, v in enumerate(parts) if i != missing)))

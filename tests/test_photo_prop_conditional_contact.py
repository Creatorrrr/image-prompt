"""Object morphology keeps person presence owned by the requested scene."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class PropConditionalContactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}

    def test_halberd_hand_spacing_is_conditional_without_losing_head_geometry(self):
        p = self.profiles['halberd_axe_point_rear_spike']
        o = pg.candidate_pack_visual_profile_obligation(p, self.registry, activation_source='test', source_intent_ids=[])
        for phrase in ['lower shaft', 'socket', 'lateral axe blade', 'apical spear point', 'rear beak', 'whether any person is present', 'When a person holds the shaft', 'hand spacing and contacts coherent']:
            self.assertIn(phrase, o['composition_instruction'])

    def test_crossbow_gate_keeps_object_integrity_and_conditional_contact(self):
        p = self.profiles['crossbow_stock_prod_release_system']
        o = pg.candidate_pack_visual_profile_obligation(p, self.registry, activation_source='test', source_intent_ids=[])
        self.assertIn('When a person supports the crossbow', o['composition_instruction'])
        gate = next(g for g in o['render_gates'] if g['id'] == 'vo_weapon_crossbow_contact_coherence')
        self.assertEqual(gate['review_scale'], 'native')
        for phrase in ['stock, string, prod, and trigger region', 'one coherent crossbow', 'When hands support', 'no hand is required for an object-only display']:
            self.assertIn(phrase, gate['description'])

    def test_five_morphology_components_remain_fail_closed(self):
        for pid in ['halberd_axe_point_rear_spike', 'crossbow_stock_prod_release_system']:
            p = self.profiles[pid]
            self.assertFalse(p['activation']['requires_adult_character'])
            c = p['semantics']['component_semantics']
            self.assertEqual(c['minimum_component_groups'], 5)
            self.assertEqual(len(c['required_group_ids']), 5)
            self.assertEqual(len(p['render_gates']), 5)
            for lang in [0, 1]:
                parts = [g['any_terms'][lang] for g in c['groups']]
                self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
                for missing in range(5):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i, v in enumerate(parts) if i != missing)))

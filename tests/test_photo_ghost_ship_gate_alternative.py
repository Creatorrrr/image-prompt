"""Keep the authored bounded-translucency branch in the rendered contract."""
import sys
import unittest
from pathlib import Path
SKILL = Path(__file__).resolve().parents[1] / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class GhostShipGateAlternativeTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        registry = native_profile_registry()
        cls.profile = next((p for p in registry['profiles'] if p['id'] == 'cand_33e0096e59a5582a8844388034c8833a'))

    def test_bounded_gate_preserves_three_authored_branches(self):
        gate = next((g for g in self.profile['render_gates'] if g['id'] == 'vo_legend_ghost_ship_bounded_breach'))
        self.assertEqual(gate['description'], 'One bounded connected region breaks into spectral translucency, absence, or displacement.')
        self.assertEqual(gate['review_scale'], 'both')

    def test_all_five_obligations_remain(self):
        self.assertEqual(self.profile['required_evidence_fields'], ['vessel_identity_phrase', 'physical_hull_phrase', 'spectral_breach_phrase', 'service_residue_phrase', 'present_anomaly_phrase'])
        self.assertEqual(len(self.profile['render_gates']), 5)

    def test_material_baseline_is_not_relaxed(self):
        gate = next((g for g in self.profile['render_gates'] if g['id'] == 'vo_legend_ghost_ship_physical_baseline'))
        self.assertEqual(gate['description'], 'A substantial opaque solid water-interacting hull region remains readable.')
from tests.photo_native_runtime import native_profile_registry

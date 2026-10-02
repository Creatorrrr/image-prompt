"""Preserve moisture-weighted damp bundles without forcing surface contact."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class WetHairWeightAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in registry['profiles'] if p['id'] == 'wet_damp_clumped_hair_state')

    def test_contact_and_noncontact_keep_all_five_required_components(self):
        p = self.profile
        comp = p['semantics']['component_semantics']
        groups = comp['groups']
        self.assertEqual(comp['minimum_component_groups'], 5)
        self.assertEqual(len(comp['required_group_ids']), 5)
        for weight in [groups[2]['any_terms'][0], groups[2]['any_terms'][-1]]:
            parts = [g['any_terms'][1 if i == 3 else 0] for i, g in enumerate(groups)]
            parts[2] = weight
            self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
            for missing in range(5):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i, v in enumerate(parts) if i != missing)))

    def test_evidence_floor_and_original_contact_anchors_stay(self):
        req = self.profile['evidence_requirements']
        self.assertEqual({k: v['min_content_words'] for k, v in req.items()}, {
            'reduced_volume_phrase': 8, 'strand_bundling_phrase': 8,
            'weighted_adherence_phrase': 9, 'moisture_coherence_phrase': 9,
            'gloss_confound_phrase': 9,
        })
        self.assertEqual(req['weighted_adherence_phrase']['must_mention_any'], [
            'weighted damp sections adhere locally to the face neck or garment',
            'moisture pulls selected bundles downward against nearby surfaces',
            'moisture pulls selected damp bundles downward into weighted sections',
        ])
        self.assertEqual(len(self.profile['render_gates']), 5)

    def test_generic_gravity_gloss_or_gel_does_not_replace_moisture_weight(self):
        p = self.profile
        groups = p['semantics']['component_semantics']['groups']
        parts = [g['any_terms'][1 if i == 3 else 0] for i, g in enumerate(groups)]
        for wrong in ['dry hair hangs down under gravity', 'bright glossy hair highlights', 'sleek gel styling', 'wet hair label alone']:
            parts[2] = wrong
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(parts)))

"""Keep the existing lightweight-cloth kebaya alternative in hard evidence."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class KebayaMaterialAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in registry['profiles'] if p['id'] == 'kebaya_front_open_blouse_sarong_system')

    def test_plain_and_embroidered_material_preserve_required_components(self):
        profile = self.profile
        component = profile['semantics']['component_semantics']
        groups = component['groups']
        self.assertEqual(component['minimum_component_groups'], 4)
        self.assertEqual(len(component['required_group_ids']), 4)
        self.assertEqual(len(groups), 5)
        for material in [groups[1]['any_terms'][0], groups[1]['any_terms'][-1]]:
            parts = [g['any_terms'][0] for g in groups[:4]]
            parts[1] = material
            self.assertEqual(pg.candidate_pack_visual_component_match(profile, '; '.join(parts)), 'component_semantics')
            for missing in range(4):
                alternative = [v for i, v in enumerate(parts) if i != missing] + [groups[4]['any_terms'][0]]
                self.assertIsNone(pg.candidate_pack_visual_component_match(profile, '; '.join(alternative)))

    def test_material_evidence_retains_original_anchors_and_floor(self):
        requirements = self.profile['evidence_requirements']
        self.assertEqual(len(requirements), 5)
        self.assertTrue(all(r['min_content_words'] == 4 for r in requirements.values()))
        self.assertEqual(requirements['embroidered_surface_phrase']['must_mention_any'], [
            'fine embroidered voile with finished scalloped edges',
            'lightweight lace or embroidered cloth retains visible weave',
            'fine lightweight cloth retains visible weave and finished front edges',
        ])
        self.assertEqual(len(self.profile['render_gates']), 5)

    def test_plain_cloth_does_not_override_exclusions(self):
        p = self.profile
        groups = p['semantics']['component_semantics']['groups']
        parts = [g['any_terms'][-1 if i == 1 else 0] for i, g in enumerate(groups[:4])]
        for excluded in p['activation'].get('exclude_if_any_terms', []):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(parts + [excluded])))

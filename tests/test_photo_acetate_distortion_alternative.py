"""Accept the declared definite distortion branch without changing film duties."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
NEW = 'image distortion follows the network'
OLD = ['image distortion or delamination follows the network', 'image delamination']

class AcetateDistortionAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in reg['profiles'] if p['id']=='acetate_channeling_shrinkage_relation')

    def binding(self, text):
        pg.validate_visual_intent_binding(obligation_index=0, field='image_delamination_phrase', phrase=text,
            requirement=self.profile['evidence_requirements']['image_delamination_phrase'])

    def test_legacy_disjunction_and_delamination_bindings_remain(self):
        for text in OLD:
            self.binding(text)
        self.assertEqual(self.profile['evidence_requirements']['image_delamination_phrase']['must_mention_any'][:2], OLD)

    def test_definite_distortion_branch_has_canonical_binding(self):
        self.binding(NEW)

    def test_all_five_film_relations_remain_required(self):
        p = self.profile; c = p['semantics']['component_semantics']
        expected = ['plastic_film_support','differential_shrinkage','channel_network','image_delamination','less_damaged_edge']
        self.assertEqual(c['minimum_component_groups'],5)
        self.assertEqual(c['required_group_ids'],expected)
        self.assertEqual(len(p['required_evidence_fields']),5)
        self.assertEqual(len(p['render_gates']),5)
        for branch in OLD + [NEW]:
            terms = [g['any_terms'][0] for g in c['groups']]; terms[3] = branch
            self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(terms)),'component_semantics')
            for missing in range(5):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(v for i,v in enumerate(terms) if i != missing)))

    def test_unrelated_damage_does_not_supply_image_relation(self):
        for text in ['dry mud cracks spread across a bare earthen surface',
                     'random scratches cross clear glass without any photographic image',
                     'a digital warp filter bends the screen pixels']:
            with self.assertRaisesRegex(ValueError,'must contain one profile component anchor'):
                self.binding(text)

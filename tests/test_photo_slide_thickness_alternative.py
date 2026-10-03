"""Accept the declared film-thickness branch without changing carrier duties."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
NEW = 'film edge thickness'
OLD = ['film edge density or thickness', 'film edge density']

class SlideThicknessAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in reg['profiles'] if p['id']=='mounted_slide_transparency_object_relation')

    def binding(self, text):
        pg.validate_visual_intent_binding(obligation_index=0, field='film_edge_density_phrase', phrase=text,
            requirement=self.profile['evidence_requirements']['film_edge_density_phrase'])

    def test_legacy_disjunction_and_density_bindings_remain(self):
        for text in OLD:
            self.binding(text)
        self.assertEqual(self.profile['evidence_requirements']['film_edge_density_phrase']['must_mention_any'][:2], OLD)

    def test_thickness_branch_has_canonical_binding(self):
        self.binding(NEW)

    def test_all_five_film_relations_remain_required(self):
        p = self.profile; c = p['semantics']['component_semantics']
        expected = ['transparent_film','physical_mount','transmitted_light','image_in_aperture','film_edge_density']
        self.assertEqual(c['minimum_component_groups'],5)
        self.assertEqual(c['required_group_ids'],expected)
        self.assertEqual(len(p['required_evidence_fields']),5)
        self.assertEqual(len(p['render_gates']),5)
        for branch in OLD + [NEW]:
            terms = [g['any_terms'][0] for g in c['groups']]; terms[4] = branch
            self.assertEqual(pg.candidate_pack_visual_component_match(p,'; '.join(terms)),'component_semantics')
            for missing in range(5):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p,'; '.join(v for i,v in enumerate(terms) if i != missing)))

    def test_mount_or_screen_thickness_does_not_supply_film_evidence(self):
        for text in ['cardboard mount thickness is visible beside an empty opening',
                     'monitor bezel thickness surrounds a bright digital image',
                     'an opaque paper card has a thick printed border']:
            with self.assertRaisesRegex(ValueError,'must contain one profile component anchor'):
                self.binding(text)

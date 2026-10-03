"""Source-authorized nonhuman alternatives preserve independent component gates."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class NonhumanSourceAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}

    def check_binding(self, pid, field, phrase):
        pg.validate_visual_intent_binding(obligation_index=0, field=field, phrase=phrase,
                                         requirement=self.profiles[pid]['evidence_requirements'][field])

    def test_independent_biohybrid_without_visible_operator_has_ownership_evidence(self):
        self.check_binding('biohybrid_robot_living_synthetic_integration', 'operator_separation_phrase',
            'The complete independent robot body occupies the water alone with tissue and scaffold contained within its own outline')

    def test_existing_operator_boundaries_and_incomplete_substitutes_remain_distinct(self):
        pid = 'biohybrid_robot_living_synthetic_integration'
        for phrase in [
            'The robot remains separate from the operator across the tank glass and the visible gap',
            "The cables end at the robot rather than entering the engineer's body across the visible control desk",
            'A separate human operator stands at the remote control desk behind the tank',
        ]:
            self.check_binding(pid, 'operator_separation_phrase', phrase)
        for field, phrase in [
            ('operator_separation_phrase', "Living muscles and synthetic wires enter the engineer's forearm through an implant"),
            ('operator_separation_phrase', 'A cropped polymer fin and one rib fill the laboratory photograph'),
            ('operator_separation_phrase', 'A mechanical device rests beside a laboratory water tank'),
            ('living_tissue_phrase', 'Pink painted molded plastic bands decorate the synthetic chassis'),
            ('functional_interface_phrase', 'Living tissue lies nearby but never joins the engineered scaffold'),
        ]:
            with self.subTest(field=field, phrase=phrase), self.assertRaises(ValueError):
                self.check_binding(pid, field, phrase)

    def test_biohybrid_required_components_and_pixel_gates_are_preserved(self):
        p = self.profiles['biohybrid_robot_living_synthetic_integration']
        c = p['semantics']['component_semantics']
        required = ['living_biological_component', 'engineered_synthetic_component', 'functional_interface', 'independent_robot_body']
        self.assertEqual(c['minimum_component_groups'], 4)
        self.assertEqual(c['required_group_ids'], required)
        parts = [next(g for g in c['groups'] if g['id']==key)['any_terms'][0] for key in required]
        self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
        for missing in range(4):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i,v in enumerate(parts) if i != missing)))
        gate = next(g for g in p['render_gates'] if g['id']=='vo_biohybrid_independent_robot_body')
        self.assertEqual(gate['description'], 'The complete biohybrid reads as an independent robot body separate from any human operator.')
        self.assertEqual(len(p['render_gates']), 5)

    def test_summoner_composition_keeps_its_existing_local_consequence_alternatives(self):
        p = self.profiles['summoner_distinct_entity_arrival']
        o = pg.candidate_pack_visual_profile_obligation(p, self.registry, activation_source='test', source_intent_ids=[])
        self.assertIn('local dust, light, shadow, or displaced-object response', o['composition_instruction'])
        for phrase in ['operator', 'complete source boundary', 'emerging entity', 'directional gesture or gaze', 'readable cause-and-effect frame']:
            self.assertIn(phrase, o['composition_instruction'])
        c = p['semantics']['component_semantics']
        self.assertEqual(c['minimum_component_groups'], 5)
        self.assertEqual(len(c['required_group_ids']), 5)
        parts = [g['any_terms'][0] for g in c['groups']]
        self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
        for missing in range(5):
            self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i,v in enumerate(parts) if i != missing)))
        self.assertEqual(len(p['render_gates']), 5)
        self.assertIn('generic glow', next(g for g in p['render_gates'] if g['id']=='vo_fantasy_summoner_not_companion')['description'])

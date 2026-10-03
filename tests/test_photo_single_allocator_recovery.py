"""Retain legacy group evidence while restoring source-owned single allocation."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

OLD = 'the same group of unmistakably adult household members actively divides contents from that one source'
NEW = 'the same unmistakably adult allocator or adult household group actively divides contents from that one source'

class SingleAllocatorRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in registry['profiles'] if p['id']=='household_food_depletion_portioning_event')

    def binding(self, text):
        pg.validate_visual_intent_binding(obligation_index=0, field='active_same_source_portioning_phrase',
            phrase=text, requirement=self.profile['evidence_requirements']['active_same_source_portioning_phrase'])

    def test_legacy_group_binding_remains_accepted(self):
        self.binding(OLD)
        p = self.profile
        action = next(g for g in p['semantics']['component_semantics']['groups'] if g['id']=='active_same_source_portioning')
        self.assertIn(OLD, action['any_terms'])
        self.assertIn(OLD, p['evidence_requirements']['active_same_source_portioning_phrase']['must_mention_any'])

    def test_single_allocator_alternative_has_a_canonical_binding(self):
        self.binding(NEW)

    def test_instruction_and_gate_preserve_the_one_or_existing_group_scope(self):
        p = self.profile
        self.assertIn(NEW, p['composition_instruction'])
        gate = next(g for g in p['render_gates'] if g['id']=='vo_pov_food_portion_2')
        self.assertIn(NEW, gate['description'])
        self.assertTrue(p['activation']['requires_adult_character'])
        self.assertIn('an adult portions the last visible staple supply from one source container across several meals in the same frame', p['activation']['exact_terms'])
        for term in ['tasting menu','meal prep','diet portions','food styling','camping rations','ordinary shared meal']:
            self.assertIn(term, p['activation']['exclude_if_any_terms'])

    def test_both_actor_paths_keep_all_five_required_relations(self):
        p = self.profile
        c = p['semantics']['component_semantics']
        ids = ['single_nearly_depleted_source','active_same_source_portioning','multiple_bounded_portions','source_to_portion_continuity','post_allocation_depletion_trace']
        self.assertEqual(c['minimum_component_groups'], 5)
        self.assertEqual(c['required_group_ids'], ids)
        self.assertEqual(len(p['required_evidence_fields']), 5)
        self.assertEqual([g['id'] for g in p['render_gates']], [f'vo_pov_food_portion_{n}' for n in range(1,6)])
        original = [next(g for g in c['groups'] if g['id']==key)['any_terms'][0] for key in ids]
        for actor_phrase in [OLD, NEW]:
            parts = original.copy();parts[1] = actor_phrase
            with self.subTest(actor_phrase=actor_phrase):
                self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
                for missing in range(5):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i,v in enumerate(parts) if i != missing)))

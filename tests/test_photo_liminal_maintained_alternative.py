"""Keep source-declared maintained-cue alternatives without dropping old evidence."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

class LiminalMaintainedAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in cls.registry['profiles'] if p['id']=='liminal_transition_use_gap')

    def binding(self, phrase):
        pg.validate_visual_intent_binding(obligation_index=0, field='maintained_cues_phrase', phrase=phrase,
            requirement=self.profile['evidence_requirements']['maintained_cues_phrase'])

    def test_old_all_cue_conjunction_remains_accepted(self):
        self.binding('working lights clean surfaces furniture and route markers imply normal service')

    def test_existing_component_alternative_is_accepted_without_rewording(self):
        component = next(g for g in self.profile['semantics']['component_semantics']['groups'] if g['id']=='familiar_maintained_service_cues')
        literal = 'working lights clean surfaces furniture signs or route markers imply normal use'
        self.assertIn(literal, component['any_terms'])
        self.binding(literal)

    def test_five_required_groups_and_render_gates_are_preserved(self):
        p = self.profile
        c = p['semantics']['component_semantics']
        self.assertEqual(c['minimum_component_groups'], 5)
        self.assertEqual(len(c['required_group_ids']), 5)
        self.assertEqual(len(p['required_evidence_fields']), 5)
        self.assertEqual(len(p['render_gates']), 5)
        parts = [g['any_terms'][0] for g in c['groups']]
        self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(parts)), 'component_semantics')
        for missing in range(5):
            with self.subTest(missing=missing):
                self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(v for i,v in enumerate(parts) if i != missing)))
        gate = next(g for g in p['render_gates'] if g['id']=='vo_imaginal_liminal_maintained_cues')
        self.assertEqual(gate['description'], 'Working maintained cues make the expected ordinary use concrete.')
        self.assertEqual(p['evidence_requirements']['maintained_cues_phrase']['min_content_words'], 9)

    def test_unsupported_maintained_evidence_and_explicit_exclusions_remain_rejected(self):
        for phrase in ['An abandoned ruined building has broken fixtures and no functioning service equipment',
                       'An ordinary closed office has locked doors after the work day has ended',
                       'A generic empty room contains plain walls and a blank ceiling']:
            with self.subTest(phrase=phrase), self.assertRaises(ValueError):
                self.binding(phrase)
        for term in ['ordinary empty room','abandoned ruin','monster hallway','horror creature','generic backrooms']:
            self.assertIn(term, self.profile['activation']['exclude_if_any_terms'])

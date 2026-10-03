"""Preserve existing shadow geometry while accepting the declared lattice alternative."""
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg

EN = 'an identifiable lattice occluder grammar shapes the cast pattern'
KO = '식별 가능한 격자 차폐 문법이 투사 패턴을 만듦'

class LatticeShadowAlternativeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        reg = pg.load_visual_obligation_registry(SKILL / 'assets/photo_prompt_visual_obligations.json')
        cls.profile = next(p for p in reg['profiles'] if p['id'] == 'patterned_cast_shadow_receiver_continuity')

    def test_declared_lattice_has_complete_canonical_evidence(self):
        pg.validate_visual_intent_binding(obligation_index=0, field='pattern_occluder_phrase', phrase=EN + ' with repeated opaque edge silhouettes',
            requirement=self.profile['evidence_requirements']['pattern_occluder_phrase'])

    def test_english_and_korean_lattice_components_are_reachable(self):
        c = self.profile['semantics']['component_semantics']
        for lang in [0, 1]:
            phrases = [g['any_terms'][lang] for g in c['groups']]
            phrases[1] = [EN, KO][lang]
            self.assertEqual(pg.candidate_pack_visual_component_match(self.profile, '; '.join(phrases)), 'component_semantics')
            for missing in range(5):
                self.assertIsNone(pg.candidate_pack_visual_component_match(self.profile, '; '.join(v for i,v in enumerate(phrases) if i != missing)))

    def test_legacy_anchors_and_five_required_relations_remain(self):
        p = self.profile; c = p['semantics']['component_semantics']
        self.assertEqual(c['minimum_component_groups'], 5)
        self.assertEqual(len(c['required_group_ids']), 5)
        self.assertEqual(len(p['required_evidence_fields']), 5)
        self.assertEqual(len(p['render_gates']), 5)
        for lang in [0, 1]:
            self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(g['any_terms'][lang] for g in c['groups'])), 'component_semantics')
        r = p['evidence_requirements']['pattern_occluder_phrase']
        self.assertEqual(len(r['must_mention_any']), 2)
        pg.validate_visual_intent_binding(obligation_index=0, field='pattern_occluder_phrase', phrase=r['must_mention_any'][0] + ' with repeated opaque edge silhouettes', requirement=r)

    def test_generic_lattice_decoration_does_not_supply_occluder_evidence(self):
        for phrase in ['a printed lattice motif decorates the wall without any cast illumination pattern, showing blue painted ornamental squares',
                       'a flat lattice overlay crosses the picture without a physical cast pattern, showing blue painted ornamental squares']:
            with self.assertRaisesRegex(ValueError, "must contain one profile component anchor"):
                pg.validate_visual_intent_binding(obligation_index=0, field='pattern_occluder_phrase', phrase=phrase,
                    requirement=self.profile['evidence_requirements']['pattern_occluder_phrase'])

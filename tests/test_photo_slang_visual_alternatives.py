"""Reviewed alternatives preserve visible relation, source ownership and scope."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/photo-prompt-image-generator'
ASSETS = SKILL / 'assets'
sys.path.insert(0, str(SKILL / 'scripts'))
import prompt_generator as pg
import photo_candidate_semantics as semantics
import photo_contracts as contracts


class PhotoSlangVisualAlternativesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {p['id']: p for p in cls.registry['profiles']}
        cls.index = pg.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', cls.registry)
        cls.data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.entries = {e['id']: (s, e) for s, rows in cls.data['slots'].items() for e in rows}
        cls.extension = json.loads((ASSETS / 'photo_prompt_slang_visual_extension.json').read_text())
        cls.new_profiles = json.loads((ASSETS / 'photo_prompt_visual_obligations_slang_visual.json').read_text())['profiles']

    def hard(self, text, source='user_requirement', polarity='required', adult=True):
        result = pg.resolve_visual_profile_hits(self.registry, [
            {'source': source, 'text': text, 'polarity': polarity}], adult_context=adult)
        return {hit['profile_id'] for hit in result['hits'] if hit['hard_eligible']}

    def test_technical_terms_are_contextual_and_exact_not_broad_slang_aliases(self):
        for p in self.new_profiles:
            term = p['activation']['exact_terms'][0]
            with self.subTest(profile=p['id']):
                self.assertIn(p['id'], self.hard('an adult actor shows ' + term))
                self.assertNotIn(p['id'], self.hard('an adult actor shows ' + term, adult=False))
                self.assertNotIn(p['id'], self.hard('an adult actor shows ' + term, polarity='excluded'))
                self.assertNotIn(p['id'], self.hard('an adult actor shows ' + term, source='authorial_core_interpretation', polarity='advisory'))
        aliases = {term.casefold() for p in self.new_profiles for term in p['activation']['exact_terms']}
        self.assertTrue({'heart eyes', '하트눈', 'inmon', '음문', '淫紋', 'm자', '만세', '뚱뚱', '가슴', '육덕'}.isdisjoint(aliases))

    def test_new_component_proofs_need_every_relation_and_owner(self):
        for raw in self.new_profiles:
            p = self.profiles[raw['id']]
            groups = p['semantics']['component_semantics']['groups']
            proof = [group['any_terms'][1] for group in groups]
            self.assertEqual(pg.candidate_pack_visual_component_match(p, '; '.join(proof)), 'component_semantics')
            for removed in range(len(proof)):
                with self.subTest(profile=p['id'], removed=removed):
                    self.assertIsNone(pg.candidate_pack_visual_component_match(p, '; '.join(t for i, t in enumerate(proof) if i != removed)))

    def test_qualified_alternative_phrases_are_optional_discovery_not_new_assertions(self):
        for raw in self.new_profiles:
            text = raw['semantics']['paraphrase_examples'][0]
            p = self.profiles[raw['id']]
            self.assertIsNotNone(pg.candidate_pack_visual_component_match(p, text))
            self.assertNotIn(p['id'], self.hard(text, source='authorial_core_interpretation', polarity='advisory'))

    def test_pose_and_marking_have_distinct_support_and_carrier_requirements(self):
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['sv_supported_m_legs'], 'the standing feet are grounded and widely separated'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['sv_seated_knees_apart'], 'one connected leg on each side of a chair backrest'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['sv_lower_abdominal_skin_marking'], 'a heart symbol printed on the lower shirt'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['sv_pupil_heart_motif'], 'a heart-shaped reflection from a lamp in the eye'))
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['sv_declared_skin_motif_topology'], 'a generic symmetrical glowing heart tattoo'))

    def test_cross_dimension_and_temporal_drafts_are_not_hidden_in_slots(self):
        effects = {
            'sv_upward_pupils': ('expression', 'face.expression'),
            'sv_tongue_lip_boundary': ('expression', 'face.expression'),
            'sv_pupil_heart_motif': ('appearance', 'face'),
            'sv_supported_m_legs': ('pose', 'body.support_and_configuration'),
            'sv_lower_abdominal_skin_marking': ('appearance', 'body.markings'),
            'sv_padded_garment_contour': ('appearance', 'body.garment'),
        }
        for cid, (dim, prop) in effects.items():
            slot, entry = self.entries[cid]
            record = semantics.semantic_source(entry, slot, self.data['candidate_semantic_policy'])
            self.assertEqual(record['affected_dimensions'], [dim])
            self.assertEqual(record['affected_properties'], [{'dimension': dim, 'target': 'main_subject', 'property': prop}])
        for cid in ('sv_face_double_v', 'sv_whole_eye_hearts', 'sv_two_actor_size_comparison', 'sv_motion_sequence', 'sv_edit_before_after'):
            self.assertNotIn(cid, self.entries)

    def test_parent_property_effects_cannot_bypass_child_locks(self):
        for cid, dim, locked_property in (
            ('sv_pupil_heart_motif', 'appearance', 'face.iris_color'),
            ('sv_local_cheek_redness', 'appearance', 'face.skin_color'),
            ('sv_seated_knees_apart', 'pose', 'body.support_and_configuration.foot_contact'),
            ('sv_lower_abdominal_skin_marking', 'appearance', 'body.markings.upper_arm'),
        ):
            slot, entry = self.entries[cid]
            record = semantics.semantic_source(entry, slot, self.data['candidate_semantic_policy'])
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [
                {'dimension': dim, 'target': 'main_subject', 'property': locked_property}]}
            self.assertFalse(contracts.property_effects_allowed(lock, record['affected_dimensions'], record['affected_properties']))

    def test_equivalent_overlays_preserve_authored_labels_effects_and_guards(self):
        owners = {}
        for filename in ('photo_prompt_tags.json', *pg.RESEARCH_EXTENSION_FILENAMES):
            raw = json.loads((ASSETS / filename).read_text())
            owners.update({e['id']: e for rows in raw.get('slots', {}).values() for e in rows})
        for slot, changes in self.extension['existing_slot_context_extensions'].items():
            for cid in changes:
                actual_slot, entry = self.entries[cid]
                self.assertEqual(actual_slot, slot)
                self.assertEqual({k: v for k, v in entry.items() if k not in ('paraphrases', 'contextual_usage')},
                                 {k: v for k, v in owners[cid].items() if k not in ('paraphrases', 'contextual_usage')})
                self.assertTrue(set(changes[cid]['paraphrases']) <= set(entry['paraphrases']))

    def test_research_and_interpretation_limits_stay_out_of_positive_index_text(self):
        for raw in self.new_profiles:
            text = pg.visual_profile_semantic_text(self.profiles[raw['id']])
            self.assertNotIn('user acceptance', text)
            self.assertNotIn('source_ids', text)
            self.assertNotIn('research-evidence', text)
        for cid in ('sv_pupil_heart_motif', 'sv_lower_abdominal_skin_marking'):
            slot, entry = self.entries[cid]
            fields = pg.semantic_bm25f_fields_for_entry(entry, slot, kind='slot')
            self.assertNotIn('contextual_usage', fields)
            self.assertNotIn('sexual ecstasy', str(fields))

    def test_composite_variants_are_not_forced_into_small_o_blush_fatigue(self):
        p = self.profiles['composite_overwhelmed_expression']
        fields = set(p['required_evidence_fields'])
        self.assertEqual(fields, {'adult_safe_context_phrase', 'eye_configuration_phrase', 'open_mouth_phrase', 'external_tongue_tip_phrase', 'simultaneous_expression_phrase'})
        proof = 'eyes rolled upward; dropped open jaw; tongue visibly crosses the outer lip boundary'
        self.assertEqual(pg.candidate_pack_visual_component_match(p, proof), 'component_semantics')
        self.assertEqual(pg.candidate_pack_visual_component_match(p, 'eyes rolled upward; open mouth'), 'component_semantics')
        self.assertNotIn('composite_overwhelmed_expression', self.hard('eyes rolled upward; open mouth', source='authorial_core_interpretation', polarity='advisory'))
        self.assertIn('external_tongue_tip_phrase', fields)
        self.assertTrue(any('sexual ecstasy' in limit for limit in p['semantics']['claim_limits']))
        self.assertNotIn('sexual ecstasy', pg.visual_profile_semantic_text(p))
        for term in ('ahegao', '아헤가오', 'アヘ顔'):
            self.assertIn(term, p['runtime_expression']['runtime_forbidden_labels'])

    def test_neutral_geometry_age_metadata_does_not_require_adult_content_controls(self):
        for cid in ('sv_pupil_heart_motif', 'sv_lower_abdominal_skin_marking', 'sv_supported_m_legs'):
            slot, entry = self.entries[cid]
            self.assertIn('age_context_only', entry['tags'])
            self.assertNotIn('adult', pg.adult_semantic_tokens(entry))
            self.assertIsNone(pg.entry_block_reason(entry, slot, {'adult_allowed': False, 'subject_category': 'human', 'intent_constraints': {}}))
        # Explicit adult-content candidates retain the ordinary control guard.
        self.assertEqual(pg.entry_block_reason({'id': 'explicit_adult_styling', 'tags': ['adult', 'fetish']}, 'eye_detail', {'adult_allowed': False}), 'adult_not_allowed')


if __name__ == '__main__': unittest.main()

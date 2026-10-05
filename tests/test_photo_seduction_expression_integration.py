"""Regression boundaries for equivalent expressions and current visible states."""
from __future__ import annotations
import json
import sys
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
sys.path.insert(0, str(ASSETS.parent / 'scripts'))
import prompt_generator as pg
from photo_contracts import property_effects_allowed


class SeductionExpressionIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pg.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.candidates = {slot + '.' + row['id']: row for slot, rows in cls.data['slots'].items() for row in rows}
        cls.registry = pg.load_visual_obligation_registry(ASSETS / 'photo_prompt_visual_obligations.json')
        cls.profiles = {row['id']: row for row in cls.registry['profiles']}
        cls.baseline = json.loads((ROOT / 'tests/fixtures/photo_prompt/seduction_expression_integration_baseline.json').read_text())
        cls.new_registry = {**cls.registry, 'profiles': [p for p in cls.registry['profiles'] if p['id'].startswith('se_profile_')]}
        cls.new_index = pg.build_visual_profile_index_payload(cls.new_registry)

    def test_existing_candidate_labels_and_real_prerequisites_survive(self):
        # Compare this frozen integration oracle before the later cute context
        # overlay. Current merged guards are exercised by the tests below and
        # cute overlay source invariants by test_photo_cute_visual_forms.
        filenames = tuple(name for name in pg.RESEARCH_EXTENSION_FILENAMES
                          if name != 'photo_prompt_cute_visual_forms_extension.json')
        with mock.patch.object(pg, 'RESEARCH_EXTENSION_FILENAMES', filenames):
            historical = pg.load_json(ASSETS / 'photo_prompt_tags.json')
        candidates = {slot + '.' + row['id']: row
                      for slot, rows in historical['slots'].items() for row in rows}
        for key, invariant in self.baseline['candidate_invariants'].items():
            with self.subTest(candidate=key):
                current = candidates[key]
                self.assertEqual({field: current.get(field) for field in invariant}, invariant)

    def test_profile_alternatives_keep_all_original_duties_and_pixel_gates(self):
        for key, invariant in self.baseline['profile_invariants'].items():
            with self.subTest(profile=key):
                current = self.profiles[key]
                projected = {field: current[field] for field in ('activation', 'required_evidence_fields', 'render_gates')}
                projected['definition'] = current['semantics']['definition']
                for field in ('minimum_component_groups', 'required_group_ids'):
                    projected[field] = current['semantics']['component_semantics'][field]
                self.assertEqual(projected, invariant)

    def test_bilingual_components_are_all_of_and_one_missing_component_is_not_complete(self):
        ids = list(self.baseline['profile_invariants']) + [p['id'] for p in self.new_registry['profiles']]
        for profile_id in ids:
            profile = self.profiles[profile_id]
            groups = profile['semantics']['component_semantics']['groups']
            for language_index in (-2, -1):
                parts = [group['any_terms'][language_index] for group in groups]
                with self.subTest(profile=profile_id, language=language_index):
                    self.assertEqual(pg.candidate_pack_visual_component_match(profile, '; '.join(parts)), 'component_semantics')
                    for index in range(len(parts)):
                        self.assertNotEqual(pg.candidate_pack_visual_component_match(profile, '; '.join(parts[:index] + parts[index+1:])), 'component_semantics')

    def test_advisory_exact_terms_never_become_requester_obligations(self):
        for profile in self.new_registry['profiles']:
            resolution = pg.resolve_visual_profile_hits(self.new_registry, [{
                'source': 'authorial_core_interpretation', 'polarity': 'advisory',
                'text': profile['activation']['exact_terms'][0],
            }], visual_profile_index=self.new_index, adult_context=True)
            self.assertFalse(any(hit['hard_eligible'] for hit in resolution['hits']))

    def test_broad_mood_and_motion_labels_do_not_exact_activate_new_shapes(self):
        for text in ['seductive', '유혹적', 'sensual', 'bedroom eyes', 'come-hither look', 'lip lick', '입술을 적시는 동작', 'beckoning gesture', 'eye-to-lip glance', 'looking up']:
            with self.subTest(text=text):
                resolution = pg.resolve_visual_profile_hits(self.new_registry, [{
                    'source': 'user_requirement', 'polarity': 'required', 'text': text,
                }], visual_profile_index=self.new_index, adult_context=True)
                self.assertFalse(any(hit['hard_eligible'] for hit in resolution['hits']))

    def test_current_contact_is_distinct_from_a_tongue_crossing_the_lip_boundary(self):
        profile = self.profiles['se_profile_tongue_lip_contact_state']
        protrusion_only = 'the visible tongue passes beyond the mouth outer lip edge; the tongue continues into the same actor mouth'
        self.assertIsNone(pg.candidate_pack_visual_component_match(profile, protrusion_only))
        self.assertEqual(self.profiles['sv_tongue_lip_boundary']['semantics']['definition'], self.baseline['profile_invariants']['sv_tongue_lip_boundary']['definition'])

    def test_hover_does_not_become_loaded_chin_support(self):
        hover = self.profiles['se_profile_hand_hover_below_chin']
        supported = 'the underside of the chin bears on the same actor palm or knuckles; the loaded arm reaches a visible elbow or forearm support surface; the supporting hand arm and head form one readable actor chain'
        self.assertIsNone(pg.candidate_pack_visual_component_match(hover, supported))
        gap = '; '.join(group['any_terms'][-2] for group in hover['semantics']['component_semantics']['groups'])
        self.assertNotEqual(pg.candidate_pack_visual_component_match(self.profiles['pv_profile_chin_support'], gap), 'component_semantics')

    def test_lapel_touch_cannot_substitute_for_gripping_and_opposing_cloth(self):
        touch = self.candidates['contact_point.se_lapel_fingertip_touch']
        grip = self.candidates['contact_point.pv_lapel_grip']
        self.assertIn('fingertip pads meet one exposed side of the lapel edge', touch['concept_units'])
        self.assertIn('fingers pinch or grip a visible collar or lapel edge', grip['concept_units'])
        self.assertIsNone(pg.candidate_pack_visual_component_match(self.profiles['se_profile_lapel_fingertip_touch'], 'fingers pinch or grip a visible collar or lapel edge; the fabric edge responds to that contact; hand remains attached to its owner'))

    def test_different_owner_or_target_does_not_complete_the_self_cheek_profile(self):
        text = 'the fingers touch another person cheek at the pads; the palm remains separated from the cheek by visible air; the touching fingers hand and forearm form one continuous limb'
        self.assertNotEqual(pg.candidate_pack_visual_component_match(self.profiles['se_profile_cheek_fingertip_light_touch'], text), 'component_semantics')

    def test_coarse_wardrobe_and_hair_effects_respect_partial_locks(self):
        for key, prop, dimension in [('contact_point.se_small_garment_fold_pinch', 'wardrobe.color', 'appearance'), ('hand_pose.tucking_hair_behind_ear', 'hair.color', 'appearance'), ('contact_point.se_existing_pendant_fingertip_hold', 'accessories.identity', 'appearance')]:
            candidate = self.candidates[key]
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'target': 'main_subject', 'property': prop, 'dimension': dimension}]}
            with self.subTest(candidate=key):
                self.assertFalse(property_effects_allowed(lock, candidate['affected_dimensions'], candidate['affected_properties']))

    def test_task_expression_cannot_claim_compatibility_with_locked_task(self):
        candidate = self.candidates['expression.ctx_c126']
        lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'target': 'main_subject', 'property': 'body.action_configuration', 'dimension': 'action'}]}
        self.assertFalse(property_effects_allowed(lock, candidate['affected_dimensions'], candidate['affected_properties']))

    def test_head_eye_relation_declares_both_effects_and_respects_each_lock(self):
        candidate = self.candidates['gaze_target.head_eye_counterorientation_relation']
        self.assertEqual(set(candidate['affected_dimensions']), {'pose', 'expression'})
        for dimension, prop in [('pose', 'head.orientation'), ('expression', 'eyes.gaze_direction')]:
            lock = {'contract_version': 'photo-intent-lock/v2', 'semantic_anchors': [{'target': 'main_subject', 'property': prop, 'dimension': dimension}]}
            with self.subTest(property=prop):
                self.assertFalse(property_effects_allowed(lock, candidate['affected_dimensions'], candidate['affected_properties']))

    def test_added_maintenance_seals_resolve_to_canonical_external_records(self):
        import photo_candidate_semantics
        count = 0
        for name in pg.RESEARCH_EXTENSION_FILENAMES:
            payload = json.loads((ASSETS / name).read_text())
            reference = payload.get('maintenance_ref') or {}
            if not reference.get('record_id', '').startswith('seduction-expression-integration-20261005-photo_prompt_'):
                continue
            record = json.loads((ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' / (reference['record_id'] + '.json')).read_text())
            self.assertTrue(record['maintenance_only'])
            self.assertEqual(reference['sha256'], photo_candidate_semantics.digest(record))
            self.assertEqual(record['seduction_integration_record_id'], 'seduction-expression-integration-20261005-v2')
            source = {key: value for key, value in payload.items() if key != 'maintenance_ref'}
            self.assertEqual(record['authored_source_sha256'], photo_candidate_semantics.digest(source))
            count += 1
        self.assertEqual(count, 6)

    def test_resealing_preserves_every_prior_maintenance_evidence_field(self):
        for name in pg.RESEARCH_EXTENSION_FILENAMES:
            payload = json.loads((ASSETS / name).read_text())
            reference = payload.get('maintenance_ref') or {}
            if not reference.get('record_id', '').startswith('seduction-expression-integration-20261005-photo_prompt_'):
                continue
            directory = ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance'
            record = json.loads((directory / (reference['record_id'] + '.json')).read_text())
            prior = record['prior_maintenance_reference']
            if prior is None:
                continue
            original = json.loads((directory / (prior['record_id'] + '.json')).read_text())
            self.assertEqual(prior['sha256'], pg.photo_candidate_semantics.digest(original))
            for field in set(original) - {'record_id', 'authored_source_sha256', 'runtime_keys'}:
                self.assertEqual(record[field], original[field], (name, field))

    def test_historical_scope_projection_rejects_unsealed_member_changes(self):
        import copy
        from tests import photo_prompt_fixtures as fixtures
        delta = fixtures.seduction_scope_delta()
        self.assertEqual(len(delta['metadata_rows']), 10)
        restored = fixtures.seduction_historical_source_scope(self.data)
        for change in delta['metadata_rows']:
            row = next(r for r in restored['slots'][change['slot']] if r['id'] == change['id'])
            for field in change['changed_fields']:
                self.assertEqual(row.get(field), change['before'].get(field))
        fixtures.seduction_historical_bundles(self.data['candidate_bundles'])
        corrupted = copy.deepcopy(self.data['candidate_bundles'])
        member = next(m for b in corrupted for m in b['member_candidates'] if m['id'] == 'slot:light_shape:lit_clean_vertical_catchlight_pair')
        member['affected_dimensions'].append('appearance')
        with self.assertRaisesRegex(AssertionError, 'Unsealed bundle member change'):
            fixtures.seduction_historical_bundles(corrupted)

    def test_optional_bundle_members_keep_independent_profile_activation(self):
        bundles = [b for b in self.data['candidate_bundles'] if b['id'].startswith('se_option_')]
        self.assertTrue(bundles)
        for bundle in bundles:
            self.assertEqual(bundle['adoption'], 'optional')
            self.assertEqual(bundle['profile_activation'], 'independent_request_evidence_only')
            for member in bundle['member_candidates']:
                self.assertEqual(member['adoption'], 'optional')
                self.assertTrue(member['affected_dimensions'])

    def test_generated_visual_index_contains_alternatives_without_maintenance_prose(self):
        index = pg.load_visual_profile_index(ASSETS / 'photo_prompt_visual_profile_index.json', self.registry)
        for profile in self.new_registry['profiles']:
            text = index['entries'][profile['id']]['text']
            self.assertIn(profile['semantics']['paraphrase_examples'][0], text)
            for forbidden in ('source_ids', 'P02', 'research-only', 'core_existing_', 'MAINTENANCE-RECORD', 'frozen actor'):
                self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()

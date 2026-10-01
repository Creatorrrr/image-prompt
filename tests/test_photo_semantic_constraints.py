"""Local, source-bound semantic grammar tests; no paid models or catalog IDs."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skills/photo-prompt-image-generator/scripts'))
import semantic_constraints as semantic


def core(request='', baseline=None, **kwargs):
    baseline = request if baseline is None else baseline
    return {
        'contract_version': 'photo-authorial-core/v3', 'canonical_sha256': 'f' * 64,
        'source_request': request, 'baseline_prompt_en': baseline,
        'request_binding': {'active_spans': [{'span_id': 'r1', 'text': request, 'start': 0, 'end': len(request)}] if request else []},
        'intent_lock': {'contract_version': 'photo-intent-lock/v2', 'priority': 'requesting_user',
                        'locked_dimensions': ['concept', 'subject', 'event'],
                        'open_dimensions': ['lighting', 'camera'], 'semantic_anchors': []},
        **kwargs,
    }


class SemanticConstraintsTests(unittest.TestCase):
    def assess(self, request, label, slot='lighting', baseline=None):
        return semantic.assess_candidate(core(request, baseline), {'en': label}, slot)

    def test_pure_source_bound_api_and_hashes(self):
        c = core('The lamp is switched off. No people.')
        before = copy.deepcopy(c)
        result = semantic.extract_constraints(c)
        self.assertEqual(c, before)
        self.assertEqual(result['source_request_sha256'], hashlib.sha256(c['source_request'].encode()).hexdigest())
        self.assertTrue(result['locked_facts'])
        for fact in result['facts']:
            self.assertIn(fact['evidence'].casefold(), fact['source_context'].casefold())
            self.assertTrue({'entity', 'property', 'value', 'polarity', 'relation', 'ownership', 'source'} <= fact.keys())
        self.assertFalse(result['coverage']['complete'])

    def test_open_baseline_state_is_never_a_lock(self):
        c = core('', 'The lamp is switched off.')
        c['intent_lock']['locked_dimensions'].append('lighting')
        self.assertFalse(semantic.extract_constraints(c)['locked_facts'])
        self.assertEqual(semantic.assess_candidate(c, {'en': 'The lamp emits light.'}, 'lighting')['status'], 'compatible')

    def test_inactive_source_contradiction_and_qualified_entity(self):
        for request, label in [
            ('The lamp is switched off.', 'The lamp emits light.'),
            ('The brass desk lamp is unlit.', 'The lamp produces a localized pool on the adjacent wall and table.'),
            ('A switched-off brass lamp stands on the table.', 'The lamp illuminates the room.'),
            ('The lamp must remain switched off.', 'The lamp glows.'),
        ]:
            with self.subTest(request=request, label=label):
                self.assertEqual(self.assess(request, label)['status'], 'contradiction')

    def test_shadow_is_not_an_emitting_source(self):
        result = self.assess('The lamp is switched off.', 'The lamp casts a sharp shadow on the table.')
        self.assertEqual(result['status'], 'unknown')
        self.assertFalse(result['contradictions'])
        self.assertFalse(any(f['property'] == 'lighting.state' and f['value'] == 'active' for f in result['facts']))

    def test_distinct_entities_and_multiple_lamps_are_not_collapsed(self):
        for request, label in [
            ('The desk lamp is switched off.', 'The ceiling lamp illuminates the room.'),
            ('The desk lamp is off. The ceiling lamp glows.', 'The lamp emits light.'),
        ]:
            self.assertFalse(self.assess(request, label)['contradictions'])

    def test_no_inversion_of_negated_states(self):
        for request in ('The lamp is not switched off.', 'The lamp is not inactive.'):
            self.assertFalse(self.assess(request, 'The lamp emits light.')['contradictions'])
        for label in ('The lamp does not emit light.', 'The lamp emits no light.', 'The lamp produces no illumination.'):
            self.assertEqual(self.assess('The lamp is switched off.', label)['status'], 'compatible', label)

    def test_off_camera_and_off_white_are_not_inactive(self):
        for request in ('The lamp is off camera.', 'The lamp is off-white.'):
            self.assertFalse(self.assess(request, 'The lamp emits light.')['contradictions'])

    def test_positive_and_negative_source_constraints(self):
        self.assertEqual(self.assess('Only candlelight illuminates the scene.', 'direct sunlight')['status'], 'contradiction')
        self.assertEqual(self.assess('No daylight, electric lights, or flash.', 'studio flash lighting')['status'], 'contradiction')
        self.assertEqual(self.assess('Window light illuminates the room.', 'warm tungsten light')['status'], 'unknown')

    def test_lighting_direction_conflict_and_camera_independence(self):
        self.assertEqual(self.assess('Light enters from the left.', 'side light from camera right')['status'], 'contradiction')
        self.assertEqual(self.assess('The camera is at eye level.', 'overhead top light')['status'], 'compatible')
        self.assertFalse(self.assess('The lamp is above the table.', 'underlighting from below')['contradictions'])

    def test_camera_viewpoint_and_roll_are_separate(self):
        self.assertEqual(self.assess('The camera is at eye level.', 'high angle looking down at a floor-seated subject', 'camera_direction')['status'], 'contradiction')
        self.assertEqual(self.assess('The camera is at eye level.', 'slightly tilted Dutch angle viewpoint', 'camera_direction')['status'], 'compatible')
        self.assertEqual(self.assess('The camera roll is level.', 'slightly tilted Dutch angle viewpoint', 'camera_direction')['status'], 'contradiction')
        self.assertEqual(self.assess('Shoot from eye level.', 'eye-level frontal view', 'camera_direction')['status'], 'compatible')

    def test_subject_gaze_and_carried_camera_do_not_set_viewpoint(self):
        for request in ('An adult woman looks upward.', 'She holds a camera pointed upward.'):
            self.assertFalse(self.assess(request, 'top-down 90-degree overhead view', 'camera_direction')['contradictions'])
            self.assertFalse(any(f['property'].startswith('camera.') for f in semantic.extract_constraints(core(request))['locked_facts']))

    def test_depicted_scene_is_not_a_physical_scene_constraint(self):
        c = core('A poster of a woman with a glowing lamp hangs on the wall.')
        self.assertFalse(any(f['entity'] == 'people' or f['property'] == 'lighting.state' for f in semantic.extract_constraints(c)['locked_facts']))
        self.assertNotEqual(semantic.assess_candidate(c, {'en': 'soft window light'}, 'lighting')['status'], 'contradiction')
        self.assertNotEqual(self.assess('No people.', 'A painting of a woman.', 'composition')['status'], 'contradiction')

    def test_output_photo_narration_does_not_imply_depiction(self):
        facts = semantic.extract_constraints(core('A photograph of an adult woman holding a ceramic mug.'))['locked_facts']
        self.assertTrue(any(f['entity'] == 'people' for f in facts))
        self.assertTrue(any(f['entity'] == 'ceramic mug' for f in facts))

    def test_cross_slot_people_and_objects(self):
        for slot in ('lighting', 'camera_direction', 'composition', 'prop'):
            self.assertEqual(self.assess('No people.', 'The person stands beside the lamp.', slot)['status'], 'contradiction')
        self.assertEqual(self.assess('An adult woman holds a ceramic mug.', 'without a mug', 'composition')['status'], 'contradiction')
        self.assertEqual(self.assess('No visitors.', 'An adult woman sits.', 'lighting')['status'], 'contradiction')

    def test_loose_keyword_and_compound_do_not_establish_people(self):
        for label in ('human-scale lighting', 'a person-shaped vase', 'a woman statue', 'humanistic mood'):
            self.assertFalse(self.assess('No people.', label)['contradictions'], label)

    def test_valid_property_anchor_does_not_lock_entire_baseline(self):
        c = core('Keep eye level.', 'The camera is at eye level. The camera roll is level. The lamp is switched off.')
        c['intent_lock']['semantic_anchors'] = [{'anchor_id': 'view', 'source_text': 'Keep eye level.',
            'dimension': 'camera', 'target': 'camera', 'property': 'height', 'prompt_evidence': 'eye level'}]
        facts = semantic.extract_constraints(c)['locked_facts']
        self.assertTrue(any(f['property'] == 'camera.viewpoint.elevation' for f in facts))
        self.assertFalse(any(f['property'] == 'camera.roll' or f['property'] == 'lighting.state' for f in facts))

    def test_invalid_and_unbound_anchors_do_not_lock(self):
        c = core('Choose freely.', 'The lamp is switched off.')
        for anchor in [
            {'source_text': 'not in request', 'dimension': 'lighting', 'target': 'lamp', 'property': 'state', 'prompt_evidence': 'The lamp is switched off.'},
            {'source_text': 'Choose freely.', 'dimension': 'lighting', 'target': 'lamp', 'property': 'state', 'prompt_evidence': 'The lamp is active.'},
        ]:
            c['intent_lock']['semantic_anchors'] = [anchor]
            self.assertFalse(semantic.extract_constraints(c)['locked_facts'])
            self.assertTrue(semantic.extract_constraints(c)['unknowns'])

    def test_unbound_active_request_and_precore_audit_are_ignored(self):
        c = core('No people.')
        c['request_binding']['active_spans'][0]['text'] = 'The lamp is switched off.'
        c['precore_feature_selection'] = {'evidence': 'Only candlelight.'}
        self.assertFalse(semantic.extract_constraints(c)['locked_facts'])

    def test_candidate_metadata_and_identifiers_do_not_supply_semantics(self):
        c = core('The lamp is switched off.')
        left = semantic.assess_candidate(c, {'id': 'off', 'en': 'The lamp emits light.'}, 'lighting')
        right = semantic.assess_candidate(c, {'id': 'arbitrary', 'en': 'The lamp emits light.', 'concept_units': ['safe'], 'relations': []}, 'lighting')
        self.assertEqual(left, right)

    def test_unknown_remains_unknown_and_no_conflict_is_not_safe(self):
        for label in ('a mysterious quality', 'perhaps the lamp emits light', 'the viewpoint is indescribable'):
            self.assertEqual(self.assess('The lamp is switched off.', label)['status'], 'unknown')
        result = self.assess('The lamp is switched off.', 'soft window light. A mysterious lighting alteration.')
        self.assertEqual(result['status'], 'unknown')

    def test_open_declarations_do_not_create_camera_locks(self):
        c = core('The lamp is switched off. Keep the camera position and lens your choice.')
        result = semantic.extract_constraints(c)
        self.assertFalse(any(f['entity'] == 'camera' for f in result['locked_facts']))
        self.assertFalse(result['unknowns'])

    def test_final_reports_contradicting_addition_and_missing_facts(self):
        c = core('The lamp is switched off. The camera is at eye level. No people.')
        bad = semantic.validate_final(c, c['baseline_prompt_en'] + ' The lamp emits light.')
        self.assertEqual(bad['status'], 'contradiction')
        self.assertTrue(bad['contradictions'])
        missing = semantic.validate_final(c, 'The lamp is switched off.')
        self.assertEqual(missing['status'], 'unknown')
        self.assertTrue(missing['missing_locked_facts'])
        self.assertFalse(missing['contradictions'])
        good = semantic.validate_final(c, c['baseline_prompt_en'] + ' Textural detail gives the frame quiet depth.')
        self.assertEqual(good['status'], 'compatible')

    def test_unsupported_modifier_and_direction_identity_are_unknown(self):
        self.assertEqual(self.assess('No people.', 'soft window light with a mysterious lighting alteration')['status'], 'unknown')
        self.assertEqual(self.assess('Window light enters from the left.', 'side light from camera right')['status'], 'unknown')

    def test_final_has_no_claim_of_full_coverage(self):
        result = semantic.validate_final(core('The lamp is switched off.'), 'The lamp is switched off.')
        self.assertEqual(result['status'], 'compatible')
        self.assertFalse(result['coverage']['complete'])
        self.assertTrue(result['coverage']['limitations'])

    def test_source_changes_require_bounded_change_mode(self):
        c = core('Window light illuminates the room.')
        for label, status, mode in [
            ('soft window light', 'compatible', 'same_source_refinement'),
            ('warm tungsten light', 'unknown', 'unknown'),
            ('warm tungsten light as secondary fill', 'compatible', 'explicit_secondary_addition'),
            ('Replace window illumination with warm tungsten light.', 'contradiction', 'explicit_replacement'),
        ]:
            result = semantic.assess_candidate(c, {'en': label}, 'lighting')
            self.assertEqual((result['status'], result['change_mode']), (status, mode), label)
        open_core = core('', 'Window light illuminates the room.')
        self.assertEqual(semantic.assess_candidate(open_core, {'en': 'Replace window illumination with warm tungsten light.'}, 'lighting')['status'], 'compatible')

    def test_final_checks_internal_combinations_on_open_properties(self):
        c = core('No people.', 'No people. The camera is at eye level.')
        result = semantic.validate_final(c, 'No people. The camera is at eye level. A top-down overhead view.')
        self.assertEqual(result['status'], 'contradiction')
        self.assertTrue(result['combination_conflicts'])
        self.assertEqual(semantic.validate_final(c, 'No people. A top-down overhead view.')['status'], 'compatible')
        separate = semantic.validate_final(core('The desk lamp is off. The ceiling lamp emits light.'), 'The desk lamp is off. The ceiling lamp emits light.')
        self.assertFalse(separate['combination_conflicts'])

    def test_inactive_source_family_fragment_is_unknown_not_certified(self):
        for actor in ('lamp', 'brass desk lamp'):
            c = core(f'The {actor} is switched off.')
            result = semantic.assess_candidate(c, {'en': 'warm lamp lighting'}, 'lighting')
            self.assertEqual(result['status'], 'unknown')
            self.assertFalse(result['contradictions'])
            self.assertTrue(any(u['reason'] == 'source_family_inactive_actor_identity_unresolved' for u in result['unknowns']))
            final = semantic.validate_final(c, c['baseline_prompt_en'] + ' Warm lamp lighting.')
            self.assertEqual(final['status'], 'unknown')
            self.assertFalse(final['contradictions'])
            self.assertEqual(semantic.assess_candidate(c, {'en': 'The lamp emits light.'}, 'lighting')['status'], 'contradiction')

    def test_explicit_other_source_is_not_the_inactive_source(self):
        c = core('The desk lamp is switched off.')
        for label in ('The ceiling lamp emits light.', 'ceiling lamp lighting'):
            self.assertEqual(semantic.assess_candidate(c, {'en': label}, 'lighting')['status'], 'compatible', label)
            self.assertEqual(semantic.validate_final(c, c['baseline_prompt_en'] + ' ' + label)['status'], 'compatible', label)
        self.assertEqual(semantic.assess_candidate(c, {'en': 'desk lamp lighting'}, 'lighting')['status'], 'unknown')

    def test_real_catalog_labels_without_catalog_identifier_rules(self):
        data = json.loads((ROOT / 'skills/photo-prompt-image-generator/assets/photo_prompt_tags.json').read_text())
        wanted = {'soft window light', 'hard on-camera flash', 'eye-level frontal view', 'slightly tilted Dutch angle viewpoint'}
        found = []
        for slot in ('lighting', 'camera_direction'):
            for entry in data['slots'][slot]:
                if entry['en'] in wanted:
                    result = semantic.assess_candidate(core('No people.'), entry, slot)
                    self.assertEqual(result['status'], 'compatible', entry['en'])
                    found.append(entry['en'])
        self.assertEqual(set(found), wanted)


if __name__ == '__main__':
    unittest.main()

from __future__ import annotations
from tests import photo_native_runtime as current_fixtures
import copy
import hashlib
import json
import random
import sys
import unittest
from unittest import mock
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / 'skills' / 'photo-prompt-image-generator' / 'scripts'
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
import prompt_generator
import audit_composed_prompt
REQUEST = '성인 네코미미 츤데레 메이드가 다친 동료를 퉁명스럽게 돌보는 장면'
BASELINE = "An adult cat-eared maid in a quiet service corridor keeps her stern professional posture while an injured adult coworker sits beside her. A dropped first-aid tin triggers the moment. She wraps the coworker's scraped wrist with practical care, looks away before checking their reaction, and leaves a warm cup within reach. The coworker's relieved shoulders answer the gesture, while her compact ears tilt toward them and the same dark uniform keeps her identity continuous."
YANDERE_REQUEST = '성인 얀데레 간호사가 같은 성인 환자를 다정히 돌보면서 퇴원 일정과 병실 출입을 통제하는 장면'
YANDERE_BASELINE = "An adult fictional nurse gently adjusts a blanket for the same adult patient in a quiet recovery room. A signed discharge note triggers the moment. Her sincere devoted care stays visible as she takes control of the patient's discharge schedule and quietly keeps the visitor pass, with a slightly asymmetric tender smile under an overfocused steady gaze and faint lower-lid tension. The same adult patient's reaching hand stops at the missing visitor pass, and the altered discharge schedule is already visible on the bedside chart. Affection and boundary control coexist in one frame, while the same white clinical uniform keeps her identity continuous."
REALITY_ERROR_REQUEST = '푸른 바다에서 밀짚모자와 흰 원피스를 입은 성인 여성, 현실 오류'
REALITY_ERROR_BASELINE = 'An adult woman in a white summer dress and straw hat stands beside a blue sea. An optically clean camera record establishes an ordinary physical beach baseline. One spatial coordinate rule fails at an invisible vertical boundary, shifting the horizon, wave crests, her shadow, and the dress hem by the same measured offset. The unaffected sand, anatomy, lighting, and perspective remain physically coherent, so the frame feels ordinary at first glance and impossible on a second look.'

def envelope(request_id: str='native-request') -> dict:
    return {'contract_version': 'photo-request-envelope/v1', 'provenance': 'requesting_user', 'request_id': request_id, 'request_text': REQUEST, 'request_sha256': hashlib.sha256(REQUEST.encode('utf-8')).hexdigest(), 'active_spans': [{'span_id': 'topic', 'start': 0, 'end': len(REQUEST), 'text': REQUEST}]}

def core() -> dict:
    return {'contract_version': 'photo-authorial-core/v3', 'provenance': 'agent_prepack', 'source_request': REQUEST, 'interpreted_intent': 'An adult guarded maid reveals concealed peer affection through practical care', 'subject': 'one adult cat-eared maid and one adult coworker', 'setting': 'a quiet staff service corridor after closing', 'event': "she treats a coworker's scraped wrist after a dropped medical tin", 'visual_priorities': ['guarded practical peer care', 'recipient reaction and consequence', 'restrained feline ear reflex'], 'baseline_prompt_en': BASELINE, 'user_definitions': [], 'interpretation_provenance': [{'term': '츤데레', 'source_text': '츤데레', 'basis': 'agent_general_knowledge', 'resolution': 'guarded outward behavior with concealed positive affiliation toward a peer', 'sources': []}], 'unresolved_ambiguities': [], 'user_exclusions': [], 'runtime_forbidden_labels': [], 'intent_lock': {'contract_version': 'photo-intent-lock/v2', 'priority': 'requesting_user', 'semantic_anchors': [{'anchor_id': 'concept', 'source_text': REQUEST, 'dimension': 'concept', 'prompt_evidence': "wraps the coworker's scraped wrist with practical care"}, {'anchor_id': 'subject', 'source_text': REQUEST, 'dimension': 'subject', 'prompt_evidence': 'An adult cat-eared maid'}, {'anchor_id': 'event', 'source_text': REQUEST, 'dimension': 'event', 'prompt_evidence': 'A dropped first-aid tin triggers the moment'}, {'anchor_id': 'character_response', 'source_text': REQUEST, 'dimension': 'character_response', 'prompt_evidence': 'looks away before checking their reaction'}], 'locked_dimensions': ['concept', 'subject', 'event', 'character_response'], 'open_dimensions': ['framing', 'composition', 'lighting', 'camera', 'color']}, 'semantic_assertions': [{'assertion_id': 'guarded_peer_care', 'dimension': 'character_response', 'polarity': 'required', 'source_span_ids': ['topic'], 'affected_dimensions': ['character_response'], 'axes': {'surface_affect': 'guarded', 'underlying_affiliation': 'positive', 'relationship_target': 'adult_coworker', 'primary_action': 'practical_care', 'affect_leak_timing': 'delayed', 'affect_leak_channels': ['gaze'], 'affect_leak_intentionality': 'minimized', 'event_phase': 'unfinished'}, 'relations': [{'operator': 'contrasts', 'left': 'surface_affect', 'right': 'underlying_affiliation'}, {'operator': 'same_target', 'members': ['relationship_target', 'primary_action', 'affect_leak']}, {'operator': 'temporal_order', 'first': 'surface_affect', 'then': 'affect_leak'}], 'evidence': {'actor_phrase': 'An adult cat-eared maid', 'baseline_phrase': 'keeps her stern professional posture', 'trigger_phrase': 'A dropped first-aid tin triggers the moment', 'target_phrase': 'an injured adult coworker sits beside her', 'primary_action_phrase': "wraps the coworker's scraped wrist with practical care", 'visible_response_phrase': "The coworker's relieved shoulders answer the gesture", 'immediate_consequence_phrase': 'leaves a warm cup within reach', 'continuity_phrase': 'the same dark uniform keeps her identity continuous', 'affective_leak_phrase': 'looks away before checking their reaction', 'nonhuman_reflex_phrase': 'her compact ears tilt toward them'}}], 'request_lineage': None, 'style': {'domain': 'character_editorial', 'family': 'restrained narrative portrait', 'evidence': ['quiet corridor depth', 'tactile first-aid props']}, 'variation_key': 'typed-v6-test'}

def yandere_envelope(request_id: str='native-yandere-request') -> dict:
    return {'contract_version': 'photo-request-envelope/v1', 'provenance': 'requesting_user', 'request_id': request_id, 'request_text': YANDERE_REQUEST, 'request_sha256': hashlib.sha256(YANDERE_REQUEST.encode('utf-8')).hexdigest(), 'active_spans': [{'span_id': 'topic', 'start': 0, 'end': len(YANDERE_REQUEST), 'text': YANDERE_REQUEST}]}

def yandere_core() -> dict:
    return {'contract_version': 'photo-authorial-core/v3', 'provenance': 'agent_prepack', 'source_request': YANDERE_REQUEST, 'interpreted_intent': 'An adult fictional nurse directs sincere care and possessive access control toward the same adult patient', 'subject': 'one adult fictional nurse and one adult patient', 'setting': 'a quiet adult recovery room', 'event': 'care for the patient becomes control of discharge and visitor access', 'visual_priorities': ['sincere care and boundary control in one frame', 'same adult affection target', 'visible changed access consequence'], 'baseline_prompt_en': YANDERE_BASELINE, 'user_definitions': [], 'interpretation_provenance': [{'term': '얀데레', 'source_text': '얀데레', 'basis': 'agent_general_knowledge', 'resolution': 'sincere affection toward one adult target escalating into a boundary-crossing control action toward that same target', 'sources': []}], 'unresolved_ambiguities': [], 'user_exclusions': [], 'runtime_forbidden_labels': ['얀데레'], 'intent_lock': {'contract_version': 'photo-intent-lock/v2', 'priority': 'requesting_user', 'semantic_anchors': [{'anchor_id': 'concept', 'source_text': YANDERE_REQUEST, 'dimension': 'concept', 'prompt_evidence': 'Affection and boundary control coexist in one frame'}, {'anchor_id': 'subject', 'source_text': YANDERE_REQUEST, 'dimension': 'subject', 'prompt_evidence': 'An adult fictional nurse'}, {'anchor_id': 'event', 'source_text': YANDERE_REQUEST, 'dimension': 'event', 'prompt_evidence': "takes control of the patient's discharge schedule and quietly keeps the visitor pass"}, {'anchor_id': 'character_response', 'source_text': YANDERE_REQUEST, 'dimension': 'character_response', 'prompt_evidence': 'Her sincere devoted care stays visible'}], 'locked_dimensions': ['concept', 'subject', 'event', 'character_response'], 'open_dimensions': ['framing', 'composition', 'lighting', 'camera', 'color']}, 'semantic_assertions': [{'assertion_id': 'affection_control_same_target', 'dimension': 'character_response', 'polarity': 'required', 'source_span_ids': ['topic'], 'affected_dimensions': ['character_response'], 'axes': {'surface_affect': 'openly affectionate', 'underlying_affiliation': 'possessive', 'relationship_target': 'same_adult_patient', 'primary_action': 'appropriates_access', 'affect_leak_timing': 'immediate', 'affect_leak_channels': ['gaze'], 'event_phase': 'unfinished', 'affect_leak_intentionality': 'deliberate'}, 'relations': [{'operator': 'same_target', 'members': ['relationship_target', 'surface_affect', 'primary_action', 'immediate_consequence']}, {'operator': 'temporal_order', 'first': 'trigger', 'then': 'primary_action'}, {'operator': 'contrasts', 'left': 'surface_affect', 'right': 'immediate_consequence'}], 'evidence': {'actor_phrase': 'An adult fictional nurse', 'baseline_phrase': 'Her sincere devoted care stays visible', 'trigger_phrase': 'A signed discharge note triggers the moment', 'target_phrase': 'the same adult patient', 'primary_action_phrase': "takes control of the patient's discharge schedule and quietly keeps the visitor pass", 'affective_leak_phrase': 'a slightly asymmetric tender smile under an overfocused steady gaze and faint lower-lid tension', 'visible_response_phrase': "The same adult patient's reaching hand stops at the missing visitor pass", 'immediate_consequence_phrase': 'the altered discharge schedule is already visible on the bedside chart', 'continuity_phrase': 'the same white clinical uniform keeps her identity continuous'}}], 'request_lineage': None, 'style': {'domain': 'character_editorial', 'family': 'restrained relational narrative portrait', 'evidence': ['quiet recovery room', 'bedside access traces']}, 'variation_key': 'typed-v6-yandere-test'}

def reality_error_envelope(request_id: str='native-reality-error-request') -> dict:
    return {'contract_version': 'photo-request-envelope/v1', 'provenance': 'requesting_user', 'request_id': request_id, 'request_text': REALITY_ERROR_REQUEST, 'request_sha256': hashlib.sha256(REALITY_ERROR_REQUEST.encode('utf-8')).hexdigest(), 'active_spans': [{'span_id': 'topic', 'start': 0, 'end': len(REALITY_ERROR_REQUEST), 'text': REALITY_ERROR_REQUEST}]}

def reality_error_core() -> dict:
    return {'contract_version': 'photo-authorial-core/v3', 'provenance': 'agent_prepack', 'source_request': REALITY_ERROR_REQUEST, 'interpreted_intent': 'A cleanly photographed beach world violates one spatial invariant while the requested adult subject, sea, straw hat, and white dress remain intact', 'subject': 'one adult woman wearing a white summer dress and straw hat', 'setting': 'a physically coherent blue seaside under natural daylight', 'event': 'one invisible coordinate boundary shifts several crossed surfaces by the same measured offset', 'visual_priorities': ['clean photographic capture', 'one repeated world-rule failure', 'ordinary first read and impossible second read'], 'baseline_prompt_en': REALITY_ERROR_BASELINE, 'user_definitions': [], 'interpretation_provenance': [{'term': '현실 오류', 'source_text': '현실 오류', 'basis': 'request_context', 'resolution': 'the captured world violates one invariant while the photographic medium remains optically clean', 'sources': []}], 'unresolved_ambiguities': [], 'user_exclusions': [], 'runtime_forbidden_labels': [], 'intent_lock': {'contract_version': 'photo-intent-lock/v2', 'priority': 'requesting_user', 'semantic_anchors': [{'anchor_id': 'concept', 'source_text': '현실 오류', 'dimension': 'concept', 'prompt_evidence': 'One spatial coordinate rule fails at an invisible vertical boundary'}, {'anchor_id': 'subject', 'source_text': REALITY_ERROR_REQUEST, 'dimension': 'subject', 'prompt_evidence': 'An adult woman in a white summer dress and straw hat'}, {'anchor_id': 'event', 'source_text': REALITY_ERROR_REQUEST, 'dimension': 'event', 'prompt_evidence': 'shifting the horizon, wave crests, her shadow, and the dress hem by the same measured offset'}], 'locked_dimensions': ['concept', 'subject', 'event'], 'open_dimensions': ['framing', 'composition', 'lighting', 'camera', 'color']}, 'semantic_assertions': [], 'request_lineage': None, 'style': {'domain': 'general_photo', 'family': 'restrained coastal reality-error editorial', 'evidence': ['clean natural daylight', 'coherent blue seaside depth']}, 'variation_key': 'typed-v6-reality-error-test'}

def core_with_concept_assertion() -> dict:
    payload = core()
    payload['semantic_assertions'].append({'assertion_id': 'guarded_care_concept', 'dimension': 'concept', 'polarity': 'required', 'source_span_ids': ['topic'], 'affected_dimensions': ['concept'], 'axes': {'controlled_surface': 'stern_professional_posture', 'contained_affect_leak': 'delayed_gaze_check', 'connection_trace': 'practical_peer_care'}, 'evidence': {'controlled_surface_phrase': 'keeps her stern professional posture', 'contained_affect_leak_phrase': 'looks away before checking their reaction', 'connection_trace_phrase': "wraps the coworker's scraped wrist with practical care"}})
    return payload

class NativeAuthorialMeaningTests(unittest.TestCase):

    def normalize(self, payload: dict, request_id: str='native-request') -> dict:
        normalized_envelope = prompt_generator.normalize_request_envelope(envelope(request_id))
        return prompt_generator.normalize_authorial_core(payload, request_envelope=normalized_envelope)

    def test_v3_freezes_typed_character_response_evidence(self):
        normalized = self.normalize(core())
        assertion = normalized['semantic_assertions'][0]
        self.assertEqual(assertion['dimension'], 'character_response')
        self.assertEqual(assertion['axes']['surface_affect'], 'guarded')
        self.assertEqual({row['operator'] for row in assertion['relations']}, {'contrasts', 'same_target', 'temporal_order'})
        self.assertIn(assertion['evidence']['trigger_phrase'], BASELINE)
        self.assertRegex(normalized['canonical_sha256'], '^[0-9a-f]{64}$')

    def test_required_assertion_rejects_unfrozen_or_unlocked_evidence(self):
        not_literal = core()
        not_literal['semantic_assertions'][0]['evidence']['trigger_phrase'] = 'an invented trigger absent from the baseline'
        with self.assertRaisesRegex(ValueError, 'must occur in baseline_prompt_en'):
            self.normalize(not_literal)
        unlocked = core()
        unlocked['intent_lock']['locked_dimensions'].remove('character_response')
        unlocked['intent_lock']['semantic_anchors'] = [row for row in unlocked['intent_lock']['semantic_anchors'] if row['dimension'] != 'character_response']
        unlocked['intent_lock']['open_dimensions'].append('character_response')
        with self.assertRaisesRegex(ValueError, 'must affect only locked dimensions'):
            self.normalize(unlocked)
        multiple_actions = core()
        multiple_actions['semantic_assertions'][0]['axes']['primary_action'] = ['wraps the scraped wrist', 'hands over a warm drink']
        with self.assertRaisesRegex(ValueError, 'exactly one primary_action'):
            self.normalize(multiple_actions)
        malformed_relation = core()
        malformed_relation['semantic_assertions'][0]['relations'][1]['members'] = ['relationship_target', 'relationship_target']
        with self.assertRaisesRegex(ValueError, 'distinct semantic members'):
            self.normalize(malformed_relation)
        unknown_relation_member = core()
        unknown_relation_member['semantic_assertions'][0]['relations'][1]['members'].append('invented_relation_member')
        with self.assertRaisesRegex(ValueError, 'distinct semantic members'):
            self.normalize(unknown_relation_member)
        missing_target_member = core()
        missing_target_member['semantic_assertions'][0]['relations'][1]['members'].remove('relationship_target')
        with self.assertRaisesRegex(ValueError, 'distinct semantic members'):
            self.normalize(missing_target_member)

    def test_authorial_budget_expands_advisory_ceiling_for_required_evidence(self):
        required_phrase = ' '.join((f'required{index}' for index in range(600)))
        prompt = required_phrase + ' ' + ' '.join((f'optional{index}' for index in range(240)))
        pack = {'contract_version':'photo-candidate-pack/v9','candidate_pool':{},'role_views':{},'role_proposals':{},'candidate_bindings':{},'authorial_core': {'intent_lock': {'semantic_anchors': [{'prompt_evidence': required_phrase}]}}}
        metrics = audit_composed_prompt.authorial_prompt_budget_metrics(pack, {}, prompt)
        self.assertEqual(metrics['actual_words'], 840)
        self.assertEqual(metrics['required_evidence_words'], 600)
        self.assertEqual(metrics['optional_prose_words'], 240)
        self.assertEqual(metrics['effective_recommended_maximum_words'], 920)
        capped_phrase = ' '.join((f'required{index}' for index in range(1000)))
        pack['authorial_core']['intent_lock']['semantic_anchors'][0]['prompt_evidence'] = capped_phrase
        capped_metrics = audit_composed_prompt.authorial_prompt_budget_metrics(pack, {}, capped_phrase + ' ' + ' '.join((f'optional{index}' for index in range(240))))
        self.assertEqual(capped_metrics['required_evidence_words'], 1000)
        self.assertEqual(capped_metrics['effective_recommended_maximum_words'], 1280)

    def test_blanket_negative_rewrite_is_rejected_before_core_freeze(self):
        payload = core()
        payload['baseline_prompt_en'] += ' No injection, contact, gore, sexuality, cleavage, or extra people.'
        with self.assertRaisesRegex(ValueError, 'blanket negative directives'):
            self.normalize(payload)
        inline = core()
        inline['baseline_prompt_en'] = inline['baseline_prompt_en'].replace('with practical care,', 'with practical care, never touching anyone,')
        with self.assertRaisesRegex(ValueError, 'blanket negative directives'):
            self.normalize(inline)
        self.assertEqual(prompt_generator.find_blanket_negative_directives('Keep the scene intense. Constraints: no contact or gore.'), ['no contact or gore'])

    def test_retry_lineage_is_hash_bound_and_dimension_disjoint(self):
        payload = core()
        payload['request_lineage'] = {'parent_request_id': 'native-parent', 'parent_core_sha256': 'a' * 64, 'preserved_dimensions': ['concept', 'subject', 'character_response'], 'allowed_changes': ['framing', 'lighting']}
        normalized = self.normalize(payload)
        self.assertEqual(normalized['request_lineage']['parent_core_sha256'], 'a' * 64)
        overlap = copy.deepcopy(payload)
        overlap['request_lineage']['allowed_changes'].append('concept')
        with self.assertRaisesRegex(ValueError, 'must be disjoint'):
            self.normalize(overlap)
if __name__ == '__main__':
    unittest.main()

"""Required golem evidence remains independent of optional candidate adoption."""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import unittest
from tests import photo_native_runtime as fixtures
import prompt_generator as g
import audit_composed_prompt as ca
import audit_image_render_request as ra
ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/photo_prompt/native_golem_composition'

class PhotoSlotRetrievalIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = g.load_runtime_data()
        input_path = ROOT / 'docs/research-evidence/photo-prompt/shared-candidate-pool-20261012/stage01/inputs/holdout-10-fantasy-ko'
        values = {k: json.loads((input_path / f).read_text()) for k, f in [('authorial_core_input', 'authorial-core.json'), ('request_envelope_input', 'request-envelope.json'), ('creative_controls', 'creative-controls.json'), ('embodiment_review', 'embodiment-review.json')]}
        cls.core = g.normalize_authorial_core(values['authorial_core_input'], request_envelope=g.normalize_request_envelope(values['request_envelope_input']), creative_control_snapshot=values['creative_controls'])
        cls.pack = g.generate_candidate_pack(cls.data, cls.core, values['creative_controls'], values['embodiment_review'], seed=17, retrieval_mode='keyword_only')
        cls.spec = json.loads((FIXTURES / 'golem-composition-authoring.json').read_text())

    def composed(self):
        pack = self.pack
        core = pack['authorial_core']
        lock = core['intent_lock']
        spec = self.spec
        prompt = core['baseline_prompt_en'] + ' ' + spec['label_phrase'] + ' ' + ' '.join(spec['evidence'].values())
        review = copy.deepcopy(pack['embodiment_preflight']['baseline_review'])
        review.update(provenance='agent_postcomposition', prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), summary='Full final prose review: ' + spec['review']['present_action'] + ' ' + spec['review']['ownership'] + ' ' + spec['review']['support'] + ' ' + spec['review']['reach_contact'] + ' ' + spec['review']['projection'])
        result = dict(pack_id=pack['pack_id'], composer='agent', prompt_en=prompt, negative_en=pack['negative_en'], chosen_candidate_ids=[], chosen_visual_concept_ids=[], candidate_interpretations=[], global_retrieval_sha256=pack['global_retrieval']['canonical_sha256'], embodiment_review=dict(source_contract_sha256=pack['embodiment_preflight']['canonical_sha256'], review=review), visual_obligation_evidence={'cand_ca170e155ac0549cb35086c0c3ad95eb': spec['evidence']}, required_hard_gates=pack['visual_obligations']['required_hard_gates'], authorial_core_binding=dict(source_authorial_core_sha256=core['canonical_sha256'], source_intent_lock_sha256=lock['canonical_sha256'], preserved_anchor_ids=[row['anchor_id'] for row in lock['semantic_anchors']], preserved_evidence=[], authorial_decisions=[]), creative_augmentation_brief={'decisions': [dict(candidate_id=row['id'], decision='rejected', rationale='Retain the stationary figure and complete only the existing hard golem meaning.') for row in pack['creative_augmentation']['candidates']]}, semantic_clarification_decisions=[dict(clarification_id=row['id'], decision='applied' if row.get('required_in_final_prompt') else 'rejected', rationale='Preserve the frozen stone figure and current stillness; reject optional reinterpretation.', prompt_evidence=lock['semantic_anchors'][0]['prompt_evidence']) for row in pack['semantic_clarification']['candidates']])
        contract = pack.get('semantic_assertion_obligations')
        if contract:
            result['semantic_assertion_evidence'] = dict(source_contract_sha256=contract['canonical_sha256'], evidence={row['assertion_id']: row['frozen_evidence'] for row in contract['obligations']})
        return result

    def request(self, composed):
        pack = self.pack
        return dict(schema_version='photo-image-render-request/v2', pack_id=pack['pack_id'], global_retrieval_sha256=pack['global_retrieval']['canonical_sha256'], source_intent_lock_sha256=pack['authorial_core']['intent_lock']['canonical_sha256'], source_embodiment_preflight_sha256=pack['embodiment_preflight']['canonical_sha256'], runtime_prompt_en=composed['prompt_en'] + ('\n\nAvoid: ' + composed['negative_en'] if composed.get('negative_en') is not None else ''), runtime_negative_en=composed['negative_en'], references=[], audit_boundary=dict(composed_prompt_audit_status='pass', runtime_prompt_audit_status='not_run', inherits_composed_prompt_pass=False))

    def test_complete_required_evidence_can_reject_every_optional_candidate_and_stay_still(self):
        composed = self.composed()
        result = ca.audit_composed_prompt(self.pack, composed, source_data=self.data)
        self.assertEqual(result['status'], 'pass', result['failures'])
        self.assertEqual(ra.audit_image_render_request(self.pack, composed, self.request(composed))['status'], 'pass')
        self.assertEqual(composed['chosen_candidate_ids'], [])
        self.assertTrue(composed['prompt_en'].startswith(self.core['baseline_prompt_en']))
        self.assertIn('the golem itself stands still at this shutter moment', composed['prompt_en'])
        self.assertEqual(composed['required_hard_gates'], self.pack['visual_obligations']['required_hard_gates'])

    def test_missing_component_evidence_is_rejected_even_with_zero_optional_choices(self):
        composed = self.composed()
        del composed['visual_obligation_evidence']['cand_ca170e155ac0549cb35086c0c3ad95eb']['task_phrase']
        failures = ca.audit_visual_obligations(self.pack, composed, composed['prompt_en'])
        self.assertTrue(any((row['check'] == 'visual_obligation_evidence' for row in failures)), failures)

    def test_unreviewed_runtime_addition_and_stale_final_review_are_rejected(self):
        composed = self.composed()
        request = self.request(composed)
        request['runtime_prompt_en'] += ' The figure reaches forward and lifts a new load.'
        self.assertEqual(ra.audit_image_render_request(self.pack, composed, request)['status'], 'fail')
        composed['prompt_en'] += ' Diffuse light makes the existing seams clearer.'
        self.assertTrue(ca.photo_embodiment.audit_composed(self.pack, composed))
if __name__ == '__main__':
    unittest.main()

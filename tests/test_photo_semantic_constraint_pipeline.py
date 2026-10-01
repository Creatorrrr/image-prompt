"""Opt-in plumbing tests; semantic accuracy is tested/evaluated separately."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch
from tests import photo_prompt_fixtures
import prompt_generator as g
import audit_composed_prompt as audit


class SemanticConstraintPipelineTests(unittest.TestCase):
    def test_gate_preserves_core_and_removes_all_indirect_handles(self):
        import semantic_constraints as sc
        core = {'canonical_sha256': 'core-sha', 'intent_lock': {'canonical_sha256': 'lock-sha'}, 'baseline_prompt_en': 'bad'}
        ids = ['slot:lighting:keep', 'slot:lighting:bad', 'slot:camera_direction:unknown']
        pack = {'authorial_core': copy.deepcopy(core), 'slots': {
            'lighting': {'candidates': [{'id': ids[0]}, {'id': ids[1]}]},
            'camera_direction': {'candidates': [{'id': ids[2]}]},
            'prop': {'candidates': [{'id': 'slot:prop:untouched'}]}},
            'visual_proposition': {'core_candidates': [{'id': ids[1]}]},
            'candidate_bundles': {'candidates': [{'id': 'bundle', 'member_candidates': ids}]}}
        entries = {candidate_id: ('slot', candidate_id.split(':')[1], {'en': status})
                   for candidate_id, status in zip(ids, ['compatible', 'contradiction', 'unknown'])}
        with patch.object(sc, 'assess_candidate', side_effect=lambda c,e,s: {'status': e['en']}), patch.object(sc, 'extract_constraints', return_value={'facts': []}):
            result = g.candidate_pack_apply_semantic_constraints(pack, entries)
        self.assertEqual(result['authorial_core'], core)
        self.assertEqual([r['id'] for r in result['slots']['lighting']['candidates']], ids[:1])
        self.assertEqual(result['slots']['camera_direction']['candidates'], [])
        self.assertEqual(result['visual_proposition']['core_candidates'], [])
        self.assertEqual(result['candidate_bundles']['candidates'], [])
        self.assertEqual(result['slots']['prop']['candidates'][0]['id'], 'slot:prop:untouched')
        self.assertEqual(result['semantic_constraint_validation']['candidate_decisions'][ids[2]]['status'], 'unknown')
        self.assertEqual(result['slots']['lighting']['semantic_abstention_count'], 1)

    def test_actual_prompt_is_sent_to_validator_not_candidate_labels(self):
        import semantic_constraints as sc
        pack = {'authorial_core': {'canonical_sha256': 'core-sha'},
                'semantic_constraint_validation': {'policy': 'structured-v1', 'source_authorial_core_sha256': 'core-sha'}}
        composed = {'prompt_en': 'Actual transformed prose with an incompatible addition.', 'chosen_candidate_ids': []}
        with patch.object(sc, 'validate_final', return_value={'status': 'contradiction', 'violations': [{'reason': 'addition'}]}) as validate:
            report = audit.audit_semantic_constraint_gate(pack, composed)
        validate.assert_called_once_with(pack['authorial_core'], composed['prompt_en'])
        self.assertEqual(report['status'], 'contradiction')
        self.assertTrue(report['enabled'])

    def test_real_final_validator_rejects_new_addition_without_chosen_ids(self):
        request = 'No people. The desk lamp is unplugged.'
        core = {'canonical_sha256': 'core-sha', 'source_request': request,
                'baseline_prompt_en': request,
                'request_binding': {'active_spans': [{'text': request, 'start': 0, 'end': len(request)}]}}
        pack = {'authorial_core': core,
                'semantic_constraint_validation': {'policy': 'structured-v1', 'source_authorial_core_sha256': 'core-sha'}}
        report = audit.audit_semantic_constraint_gate(pack, {'prompt_en': request + ' The desk lamp glows.', 'chosen_candidate_ids': []})
        self.assertEqual(report['status'], 'contradiction')
        self.assertTrue(report['contradictions'])
        self.assertEqual(core['baseline_prompt_en'], request)

    def test_off_never_invokes_semantic_validator(self):
        self.assertEqual(audit.audit_semantic_constraint_gate({}, {'prompt_en': 'Anything'}), {'enabled': False, 'status': 'not_run'})

    def test_hash_binding_mismatch_blocks(self):
        pack = {'authorial_core': {'canonical_sha256': 'new'},
                'semantic_constraint_validation': {'policy': 'structured-v1', 'source_authorial_core_sha256': 'old'}}
        self.assertEqual(audit.audit_semantic_constraint_gate(pack, {'prompt_en': 'Text'})['status'], 'contradiction')

    def test_defaults_and_independent_flags(self):
        import argparse
        original = argparse.ArgumentParser.parse_args
        parsed = []
        class ParserCaptured(Exception):
            pass
        def capture(parser, argv):
            parsed.append(original(parser, argv))
            raise ParserCaptured
        for argv in (['--n', '1'], ['--semantic-constraint-policy', 'structured-v1', '--recall-lane-policy', 'reserve-leaders']):
            with patch.object(argparse.ArgumentParser, 'parse_args', capture), self.assertRaises(ParserCaptured):
                g.main(argv)
        self.assertEqual(parsed[0].semantic_constraint_policy, 'off')
        self.assertEqual(parsed[0].recall_lane_policy, 'off')
        self.assertEqual(parsed[1].semantic_constraint_policy, 'structured-v1')
        self.assertEqual(parsed[1].slot_retrieval_policy, 'stable')

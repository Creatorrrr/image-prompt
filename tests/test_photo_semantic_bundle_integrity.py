"""Source-only atomic bundle regression; no benchmark data or model calls."""
from __future__ import annotations
import copy
import unittest
from unittest.mock import patch
from tests import photo_prompt_fixtures
import prompt_generator as g
import photo_candidate_semantics as semantics
import audit_composed_prompt as audit


def scene():
    request = 'The desk lamp is switched off. No people.'
    return {'canonical_sha256': 'core', 'source_request': request, 'baseline_prompt_en': request,
            'request_binding': {'active_spans': [{'text': request, 'start': 0, 'end': len(request)}]},
            'intent_lock': {'canonical_sha256': 'lock', 'open_dimensions': ['lighting', 'camera']}}


def fixture(label):
    member = {'id': 'slot:lighting:test', 'slot': 'lighting', 'entry_id': 'test', 'affected_dimensions': ['lighting']}
    source = {'id': 'test', 'source_sha256': 'source', 'associated_profile_ids': [],
              'components': [{'id': 'light', 'concept_units': ['desk lamp'], 'minimum_realizations': 1}],
              'member_candidates': [member], 'confusion_boundaries': [], 'relations': [],
              'adoption': 'optional', 'profile_activation': 'independent_request_evidence_only'}
    data = {'slots': {'lighting': [{'id': 'test', 'en': label}]}, 'candidate_bundles': [source]}
    pack = {'contract_version': 'photo-candidate-pack/v6', 'candidate_semantic_surface_version': semantics.SURFACE_VERSION,
            'authorial_core': scene(), 'slots': {'lighting': {'candidates': [{'id': member['id'], 'applicability': {'status': 'eligible'}}]}},
            'semantic_constraint_validation': {'policy': 'structured-v1'}, 'provenance': {'seed': 1}}
    return data, pack


class SemanticBundleIntegrityTests(unittest.TestCase):
    def test_atomic_source_recomputation_agrees_with_auditor_without_selection(self):
        for label in ('The desk lamp emits light.', 'warm lamp lighting'):
            with self.subTest(label=label):
                data, pack = fixture(label)
                pack['candidate_bundles'] = g.candidate_pack_candidate_bundles(data, pack)
                self.assertEqual(pack['candidate_bundles']['candidates'], [])
                self.assertEqual(pack['candidate_bundles']['semantic_constraint_admission']['before_count'], 1)
                with patch.object(g, 'load_json', return_value=copy.deepcopy(data)), patch.object(g, 'load_quality_layers', return_value={}):
                    failures = audit.audit_candidate_semantic_contracts(pack, '', set(), {}, [])
                self.assertEqual(failures, [])

    def test_bundle_only_member_is_checked_and_intact_when_compatible(self):
        for label, expected in [('The desk lamp emits light.', 0), ('warm lamp lighting', 0), ('soft window light', 1)]:
            with self.subTest(label=label):
                data, pack = fixture(label)
                public = semantics.public_bundles(data, pack, {'test': {'all_member_guards_satisfied': True}})
                pack['slots'] = {}  # Member exists only in the independent bundle inventory.
                before = copy.deepcopy(public['candidates'][0])
                filtered = g.candidate_pack_semantic_bundle_admission(data, pack, public)
                self.assertEqual(len(filtered['candidates']), expected)
                decisions = filtered['semantic_constraint_admission']['bundle_member_decisions']['bundle:test']
                self.assertIn('slot:lighting:test', decisions)
                if expected:
                    self.assertEqual(filtered['candidates'][0], before)
                    self.assertEqual(before['source_contract_sha256'], semantics.digest(semantics.bundle_source_material(before)))

    def test_joint_only_production_admission_and_auditor_recompute_agree(self):
        for label, expected in [('The desk lamp emits light.', 0), ('warm lamp lighting', 0), ('soft window light', 1)]:
            with self.subTest(label=label):
                data, pack = fixture(label)
                pack['slots'] = {}
                data['candidate_semantic_policy'] = {'joint_adoption': {
                    'maximum_members_per_bundle': 2, 'minimum_shared_content_words': 1,
                    'context_policy': 'self_contained', 'maximum_bundles': 4}}
                data['candidate_bundles'][0]['member_candidates'][0]['concept_units'] = ['desk lamp']
                pack['candidate_bundles'] = g.candidate_pack_candidate_bundles(data, pack)
                self.assertEqual(len(pack['candidate_bundles']['candidates']), expected)
                self.assertEqual(pack['candidate_bundles']['semantic_constraint_admission']['before_count'], 1)
                with patch.object(g, 'load_json', return_value=copy.deepcopy(data)), patch.object(g, 'load_quality_layers', return_value={}):
                    failures = audit.audit_candidate_semantic_contracts(pack, '', set(), {}, [])
                self.assertEqual(failures, [])

    def test_existing_bundle_removed_as_whole_not_partially_rehashed(self):
        data, pack = fixture('The desk lamp emits light.')
        pack['candidate_bundles'] = semantics.public_bundles(data, pack)
        original = copy.deepcopy(pack['candidate_bundles']['candidates'][0])
        result = g.candidate_pack_apply_semantic_constraints(pack, {'slot:lighting:test': ('slot', 'lighting', data['slots']['lighting'][0])})
        self.assertEqual(result['candidate_bundles']['candidates'], [])
        self.assertEqual(original['source_contract_sha256'], semantics.digest(semantics.bundle_source_material(original)))

    def test_default_policy_preserves_bundle_contract_exactly(self):
        data, pack = fixture('The desk lamp emits light.')
        pack.pop('semantic_constraint_validation')
        expected = semantics.public_bundles(data, pack)
        self.assertEqual(g.candidate_pack_candidate_bundles(data, pack), expected)

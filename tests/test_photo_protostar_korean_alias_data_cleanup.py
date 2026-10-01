"""A sourced Korean protostar alias preserves the authored disk/outflow subject."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
E = ROOT / 'docs/research-evidence/photo-prompt/protostar-korean-alias-data-cleanup-20261001'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


common = load_module('protostar_frozen_common', E / 'cycle_common.py')
with patch.dict(sys.modules, {'cycle_common': common}):
    public_gate = load_module('protostar_public_gate', E / 'check_v6_preservation.py')


class ProtostarKoreanAliasDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = common.load_freeze()
        cls.states = common.states_from_freeze(cls.frozen)
        cls.target = next(row for row in cls.frozen['inventory'] if row['decision'] == 'fix')
        cls.current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')

    def test_frozen_inventory_probes_and_bounded_cost(self):
        self.assertEqual(hashlib.sha256((E / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
                         'a364c2fce6683fe4115f79a5b9036de5a4d09d167db84bc3a52f360d4eb44816')
        self.assertEqual(len(self.frozen['inventory']), 20)
        self.assertEqual(sum(row['decision'] == 'keep' for row in self.frozen['inventory']), 19)
        self.assertEqual(len(self.frozen['queries']), 13)
        self.assertEqual(len(self.frozen['pending_input_sha256']), 12)
        self.assertEqual(self.frozen['maximum_paid_attempts'], 13)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'], .0212992)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        self.assertNotIn('manual_recovery', self.frozen)
        original_raw = (E / 'preparation-revisions/pre-replay-test-isolation/frozen-inventory-queries.json').read_bytes()
        self.assertEqual(hashlib.sha256(original_raw).hexdigest(),
                         'c40e9b6659fb8daedcf21eb0497395f7b2a82c10180abcc05c43f2924613a0f1')
        original = json.loads(original_raw)
        for field in ['inventory', 'queries', 'approved_inputs', 'acceptance', 'source_file',
                      'state_dictionary_hashes', 'previous_tracked_cost_upper_usd',
                      'maximum_paid_attempts', 'maximum_additional_cost_usd']:
            self.assertEqual(self.frozen[field], original[field])

    def test_complete_raw_space_extension_has_only_one_qualified_alias_append(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        expected = copy.deepcopy(before)
        row = next(r for r in expected['slots']['subject'] if r['id'] == self.target['id'])
        self.assertEqual(row, self.target['before'])
        row['aliases'].append('원시성 원반 분출계')
        self.assertEqual(json.loads((ROOT / self.frozen['source_file']).read_text()), expected)
        self.assertEqual(expected['maintenance_ref'], before['maintenance_ref'])

    def test_complete_current_merged_state_and_nineteen_keeps_are_exact(self):
        self.assertEqual(self.current, self.states['proposal'])
        self.assertEqual(self.current['candidate_bundles'], self.states['baseline']['candidate_bundles'])
        for item in self.frozen['inventory']:
            current = next(r for r in self.current['slots'][item['slot']] if r['id'] == item['id'])
            self.assertEqual(current, item['proposal'])
            if item['decision'] == 'keep':
                self.assertEqual(current, item['before'])

    def test_existing_name_and_disk_outflow_specialization_are_unchanged(self):
        before, after = self.target['before'], self.target['proposal']
        self.assertEqual(after['aliases'], before['aliases'] + ['원시성 원반 분출계'])
        self.assertEqual({k: v for k, v in after.items() if k != 'aliases'},
                         {k: v for k, v in before.items() if k != 'aliases'})
        self.assertIn('원시별 원반 분출계', after['aliases'])
        self.assertNotIn('원시성', after['aliases'])
        self.assertEqual(after['en'], 'an embedded protostellar system with dust disk and bipolar outflow')
        self.assertEqual(after['kind'], ['environment'])

    def test_actual_v6_full_pack_detail_and_overview_preserve_genuine_subject_context(self):
        report = public_gate.check()
        for key in ['candidate_equal', 'full_pack_equal', 'detail_equal', 'overview_equal',
                    'genuine_subject_compatibility_without_force',
                    'narrow_location_compatibility_without_force', 'generated_soft_policy_preserved',
                    'negative_guard_preserved', 'frozen_core_preserved']:
            self.assertTrue(report[key])
        before = json.loads((E / 'baseline-actual-v6.json').read_text())
        after = json.loads((E / 'proposal-actual-v6.json').read_text())
        self.assertEqual(before, after)
        self.assertEqual(after['full_pack']['pack_id'], 'c1132577fdbe6d73')
        self.assertEqual(after['candidate']['concept_units'], [self.target['before']['en']])
        self.assertEqual(after['candidate']['adoption'], 'optional')
        self.assertEqual(report['api_calls'], 0)
        self.assertEqual(report['query_retrieval_executions'], 0)

    def test_independent_probes_names_and_controls_are_existing_subjects(self):
        queries = self.frozen['queries']
        scout = json.loads((E / 'scout/frozen-proposal-and-unmeasured-probes.json').read_text())
        self.assertEqual(len(scout['queries']), 8)
        self.assertTrue({q['query'] for q in scout['queries']} <= {q['query'] for q in queries})
        self.assertTrue({'protostar', '원시별', '원시성'} <= {q['query'] for q in queries})
        self.assertTrue(all(q['slot'] == 'subject' for q in queries))
        subjects = {'slot:subject:' + row['id'] for row in self.current['slots']['subject']}
        self.assertTrue(all(q['target'] in subjects for q in queries))

    def test_all_other_merged_rows_and_previously_accepted_natural_rows_are_exact(self):
        for slot, rows in self.states['baseline']['slots'].items():
            for row in rows:
                if slot == 'subject' and row['id'] == self.target['id']:
                    continue
                self.assertEqual(next(r for r in self.current['slots'][slot] if r['id'] == row['id']), row)
        krummholz = next(r for r in self.current['slots']['surface_material'] if r['id'] == 'treeline_wind_pruned_krummholz_surface')
        self.assertIn('왜성변형수 바람형 패치', krummholz['aliases'])
        reef = next(r for r in self.current['slots']['action'] if r['id'] == 'reef_flat_crest_forereef_wave_gradient')
        self.assertEqual(reef['concept_units'], [reef['en']])


    def test_acceptance_binds_name_gain_score_costs_and_target_absence(self):
        raw = (E / 'acceptance-decisions.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         'f9990a29ec003edf16d29e60c3289aa7ed5468e6dd94303df9fbe4e0c0cb9f53')
        decision = json.loads(raw)
        self.assertEqual(decision['accepted_ids'], [self.target['id']])
        self.assertEqual(decision['accepted_fields'], ['aliases'])
        self.assertEqual(decision['accepted_dictionary_hash'], common.g.dictionary_hash(self.current))
        gain = decision['measured_benefit']['bare_korean_name_lexical']
        self.assertTrue(gain['no_hits']['baseline'])
        self.assertFalse(gain['no_hits']['proposal'])
        self.assertIsNone(gain['primary_target']['baseline']['rank'])
        self.assertEqual(gain['primary_target']['proposal']['rank'], 1)
        for row in decision['tradeoffs']['all_four_near_misses_remain_dense_rank_one']:
            self.assertEqual(row['primary_target']['baseline']['rank'], 1)
            self.assertEqual(row['primary_target']['proposal']['rank'], 1)
            if row['query_id'] in ('n01_ko', 'n02_ko'):
                self.assertGreater(row['primary_target']['proposal']['score'], row['primary_target']['baseline']['score'])
        for row in decision['tradeoffs']['absent_targets_in_nonempty_lexical_results']:
            for state in ('baseline', 'proposal'):
                self.assertIsNone(row['primary_target'][state]['rank'])
                self.assertFalse(row['no_hits'][state])
                self.assertGreater(row['returned_hits'][state], 0)
        self.assertEqual(decision['cost']['attempts'], 12)
        self.assertEqual(decision['cost']['failed_or_uncertain_attempts'], 0)
        self.assertFalse(decision['preservation']['output_improvement_claimed'])
        for name, expected in decision['evidence_sha256'].items():
            self.assertEqual(hashlib.sha256((E / name).read_bytes()).hexdigest(), expected)
        roles = json.loads((E / 'existing-role-regression-comparison.json').read_text())
        self.assertTrue(roles['all_three_top12_orders_identical'])
        self.assertEqual(roles['states']['proposal'][2]['top12'][6]['document_id'],
                         'slot:social_cue:multi_observer_recognition_cue')


if __name__ == '__main__':
    unittest.main()

"""Returned-item Korean state must agree with its existing action and English unit."""
from pathlib import Path
import copy
import hashlib
import gzip
import importlib.util
import json
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
E = ROOT / 'docs/research-evidence/photo-prompt/shelf-return-korean-state-data-cleanup-20261001'
NEXT = ROOT / 'docs/research-evidence/photo-prompt/liminal-active-use-korean-data-cleanup-20261002'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


common = load_module('shelf_return_frozen_common', E / 'cycle_common.py')
with patch.dict(sys.modules, {'cycle_common': common}):
    public_gate = load_module('shelf_return_public_gate', E / 'check_v6_preservation.py')


class ShelfReturnKoreanStateDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = common.load_freeze()
        cls.states = common.states_from_freeze(cls.frozen)
        cls.target = next(row for row in cls.frozen['inventory'] if row['decision'] == 'fix')
        cls.current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.accepted_snapshot = json.loads(gzip.decompress((NEXT / 'baseline-merged-data.json.gz').read_bytes()))

    def test_frozen_inventory_probes_and_bounded_cost(self):
        self.assertEqual(hashlib.sha256((E / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
                         '7daef186b40a69cff877ac9e65527cc5521b7005f806afd7cfac9c834d9631dd')
        self.assertEqual(len(self.frozen['inventory']), 12)
        self.assertEqual(sum(r['decision'] == 'keep' for r in self.frozen['inventory']), 11)
        self.assertEqual(len(self.frozen['queries']), 12)
        self.assertEqual(len(self.frozen['pending_input_sha256']), 13)
        self.assertEqual(self.frozen['maximum_paid_attempts'], 14)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'], .0229376)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        self.assertNotIn('manual_recovery', self.frozen)

    def test_complete_raw_extension_changes_only_the_one_korean_state(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        expected = copy.deepcopy(before)
        row = next(r for r in expected['slots']['aftermath_trace'] if r['id'] == self.target['id'])
        self.assertEqual(row, self.target['before'])
        row['ko'] = common.PROPOSED_KO
        current = json.loads((ROOT / self.frozen['source_file']).read_text())
        expected['maintenance_ref'] = self.frozen['maintenance_revision']['new_reference']
        self.assertEqual(current, expected)
        self.assertEqual(before['maintenance_ref'], self.frozen['maintenance_revision']['old_reference'])
        self.assertEqual((ROOT / self.frozen['source_file']).read_bytes(), common.raw_proposal(self.frozen))

    def test_maintenance_revision_preserves_experiment_and_original_record(self):
        revision = self.frozen['maintenance_revision']
        old = json.loads((E / 'preparation-revisions/pre-maintenance-binding/frozen-inventory-queries.json').read_text())
        self.assertEqual(common.sha((E / 'preparation-revisions/pre-maintenance-binding/frozen-inventory-queries.json').read_bytes()), revision['original_freeze_sha256'])
        for key in set(old) | set(self.frozen):
            if key not in revision['allowed_freeze_changes']:
                self.assertEqual(old[key], self.frozen[key])
        original = json.loads((ROOT / revision['old_record_file']).read_text())
        current = json.loads((ROOT / revision['new_record_file']).read_text())
        self.assertEqual({k:v for k,v in original.items() if k not in ('record_id','authored_source_sha256')},
                         {k:v for k,v in current.items() if k not in ('record_id','authored_source_sha256')})
        self.assertEqual(common.objsha(original), revision['old_reference']['sha256'])
        self.assertEqual(common.objsha(current), revision['new_reference']['sha256'])
        for prefix in ('old','new'):
            self.assertEqual(common.sha((ROOT / revision[prefix+'_record_file']).read_bytes()), revision[prefix+'_record_file_sha256'])
        for name, digest in revision['unchanged_measured_artifact_sha256'].items():
            self.assertEqual(common.sha((E / name).read_bytes()), digest)
        for name, digest in old['artifact_sha256'].items():
            preserved = E / 'preparation-revisions/pre-maintenance-binding' / name
            self.assertEqual(common.sha((preserved if preserved.exists() else E / name).read_bytes()), digest)

    def test_acceptance_binds_catalog_benefit_and_all_adverse_evidence(self):
        self.assertEqual(common.sha((E / 'acceptance-decisions.json').read_bytes()), 'a72136476b06b6237eab4acda91e06d44349d73b640ba9356887cfff200ccb09')
        decision = json.loads((E / 'acceptance-decisions.json').read_text())
        self.assertEqual(decision['accepted_ids'], [self.target['id']])
        self.assertEqual(decision['accepted_fields'], ['ko'])
        self.assertEqual(decision['accepted_dictionary_hash'], common.g.dictionary_hash(self.accepted_snapshot))
        for name, digest in decision['artifact_sha256'].items():
            self.assertEqual(common.sha((E / name).read_bytes()), digest)
        report = json.loads((E / 'korean-catalog-consumer.json').read_text())
        self.assertEqual(report['source_rows'], 53)
        self.assertEqual(len(report['changed_display_rows']), 1)
        self.assertTrue(report['all_other_catalog_lines_exact'])
        self.assertTrue(report['current_live_cli_equals_proposal'])
        tradeoffs = decision['tradeoffs']
        harm = tradeoffs['raw_coexistence_en_lexical']['primary_target']
        self.assertEqual([harm[s]['rank'] for s in ('baseline','proposal')], [5,6])
        self.assertEqual(tradeoffs['unrelated_flame_rank_before_after'], [6,5])
        self.assertEqual(len(tradeoffs['all_six_near_misses_remain_dense_rank_one']), 6)
        for item in tradeoffs['all_six_near_misses_remain_dense_rank_one']:
            self.assertEqual([item['primary_target'][s]['rank'] for s in ('baseline','proposal')], [1,1])
        for key in ['wrong_source_english_dense', 'wrong_source_korean_lexical']:
            target = tradeoffs[key]['primary_target']
            self.assertGreater(target['proposal']['score'], target['baseline']['score'])
        conditional = decision['measured_benefit']['conditional_compatible_pool']
        self.assertEqual(conditional['target_rank_before_after'], [1,1])
        self.assertTrue(conditional['full_order_exact'])
        self.assertEqual(decision['cost']['attempts'], 13)
        self.assertEqual(decision['cost']['retries'], 0)

    def test_historical_merged_state_and_current_eleven_keeps_are_exact(self):
        self.assertEqual(self.accepted_snapshot, self.states['proposal'])
        self.assertEqual(self.current['candidate_bundles'], self.states['baseline']['candidate_bundles'])
        for item in self.frozen['inventory']:
            current = next(r for r in self.current['slots'][item['slot']] if r['id'] == item['id'])
            self.assertEqual(current, item['proposal'])
            if item['decision'] == 'keep':
                self.assertEqual(current, item['before'])

    def test_returned_item_owns_its_restored_position_without_global_stock_rule(self):
        before, after = self.target['before'], self.target['proposal']
        self.assertEqual(before['ko'], common.BEFORE_KO)
        self.assertEqual(after['ko'], common.PROPOSED_KO)
        self.assertEqual({k: v for k, v in after.items() if k != 'ko'},
                         {k: v for k, v in before.items() if k != 'ko'})
        self.assertIn('되돌린 한 품목이 놓인 원래 진열 위치', after['ko'])
        self.assertIn('결제된 더 작은 필수 식품 묶음', after['ko'])
        self.assertNotIn('진열 공백', after['ko'])
        self.assertEqual(after['concept_units'], [before['en']])
        self.assertEqual(after['requires_primary_any_tags'], ['food_access_budget_choice_event'])
        self.assertEqual(after['affected_dimensions'], ['timing'])

    def test_historical_v6_full_pack_detail_and_overview_preserve_genuine_adult_context(self):
        report = public_gate.check()
        for key in ['candidate_equal', 'full_pack_equal', 'detail_equal', 'overview_equal',
                    'genuine_human_adult_subject_compatibility_without_force',
                    'all_12_reviewed_rows_compatible_with_source_adult_subjects',
                    'generated_soft_policy_preserved', 'negative_guard_preserved',
                    'frozen_core_preserved', 'fixture_provenance_preserved']:
            self.assertTrue(report[key])
        before = json.loads((E / 'baseline-actual-v6.json').read_text())
        after = json.loads((E / 'proposal-actual-v6.json').read_text())
        self.assertEqual(before, after)
        self.assertEqual(report['pack_id'], '946d69ecd0b85dc6')
        self.assertEqual(after['candidate']['concept_units'], [self.target['before']['en']])
        self.assertEqual(after['candidate']['adoption'], 'optional')
        self.assertEqual(after['candidate']['affected_dimensions'], ['timing'])
        self.assertEqual(report['api_calls'], 0)
        self.assertEqual(report['query_retrieval_executions'], 0)
        self.assertEqual(report['writes'], 0)

    def test_korean_field_projection_changes_only_the_local_aftermath(self):
        summary = json.loads((E / 'scout/surface-summary.json').read_text())
        subject = summary['fixture']['subject_row']
        outputs = {}
        for label, data in self.states.items():
            row = next(r for r in data['slots']['aftermath_trace'] if r['id'] == self.target['id'])
            owner = next(r for r in data['slots']['subject'] if r['id'] == subject['id'])
            self.assertEqual(owner, subject)
            outputs[label] = common.g.build_fields({'subject': owner, 'aftermath_trace': row}, 'ko', data=data)
        self.assertEqual(outputs['baseline']['aftermath_trace'], common.BEFORE_KO)
        self.assertEqual(outputs['proposal']['aftermath_trace'], common.PROPOSED_KO)
        self.assertEqual({k: v for k, v in outputs['baseline'].items() if k != 'aftermath_trace'},
                         {k: v for k, v in outputs['proposal'].items() if k != 'aftermath_trace'})

    def test_scout_and_reviewer_state_contrasts_remain_frozen(self):
        queries = self.frozen['queries']
        texts = {q['query'] for q in queries}
        scout = json.loads((E / 'scout/frozen-proposal-and-unmeasured-probes.json').read_text())
        self.assertEqual(len(scout['probes']), 8)
        self.assertTrue({q['query'] for q in scout['probes']} <= texts)
        self.assertIn('A shopper finishes paying for fewer essentials, but the omitted package remains beside the till and its original shelf position is empty.', texts)
        self.assertIn('구매자는 더 적은 필수 식품만 계산했지만 빼놓은 품목은 계산대 옆에 있고 원래 진열 자리는 비어 있다.', texts)
        self.assertTrue(all(q['slot'] == 'aftermath_trace' for q in queries))
        available = {'slot:aftermath_trace:' + row['id'] for row in self.current['slots']['aftermath_trace']}
        self.assertTrue(all(q['target'] in available for q in queries))

    def test_previous_published_aliases_and_reef_unit_remain_exact(self):
        for slot, entry_id in [('subject', 'embedded_protostar_observation_subject'),
                               ('surface_material', 'treeline_wind_pruned_krummholz_surface'),
                               ('action', 'reef_flat_crest_forereef_wave_gradient')]:
            current = next(r for r in self.current['slots'][slot] if r['id'] == entry_id)
            original = next(r for r in self.states['baseline']['slots'][slot] if r['id'] == entry_id)
            self.assertEqual(current, original)


if __name__ == '__main__':
    unittest.main()

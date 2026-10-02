"""A suspended use is distinct from removing all evidence of prior use."""
from pathlib import Path
import copy
import importlib.util
import json
import sys
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
E = ROOT / 'docs/research-evidence/photo-prompt/liminal-active-use-korean-data-cleanup-20261002'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


common = load_module('liminal_active_use_frozen_common', E / 'cycle_common.py')


class LiminalActiveUseKoreanDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = common.load_freeze()
        cls.states = common.states_from_freeze(cls.frozen)
        cls.target = next(row for row in cls.frozen['inventory'] if row['decision'] == 'fix')
        cls.current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')

    def test_frozen_source_inventory_queries_and_bounded_workload(self):
        self.assertEqual(common.sha((E / 'frozen-inventory-queries.json').read_bytes()), '603d19882bc0192fc6263800beac14dad69adc666143bf45bc9cf6f561b1b1c1')
        self.assertEqual(self.frozen['scout_freeze_sha256'], 'cc355a36cc40b957de3a76cb9c976ca835ca18d3bef5bc13f8f5df5ac5f5e03f')
        self.assertEqual(len(self.frozen['inventory']), 22)
        self.assertEqual(sum(x['decision'] == 'keep' for x in self.frozen['inventory']), 21)
        self.assertEqual(len(self.frozen['queries']), 14)
        self.assertEqual(len(self.frozen['pending_input_sha256']), 13)
        self.assertEqual(len(self.frozen['reused_cache_provenance']), 2)
        self.assertEqual(self.frozen['maximum_paid_attempts'], 14)
        self.assertEqual(self.frozen['maximum_additional_cost_usd'], .0229376)
        self.assertEqual(self.frozen['planned_result_rows'], 56)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        self.assertNotIn('manual_recovery', self.frozen)

    def test_complete_raw_source_changes_only_ko_and_predeclared_reference(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        expected = copy.deepcopy(before)
        row = next(x for x in expected['slots']['action'] if x['id'] == self.target['id'])
        self.assertEqual(row, self.target['before'])
        row['ko'] = '이동 기능과 도착 기능 사이에서 예상된 이용 활동 없이 머무는'
        expected['maintenance_ref'] = self.frozen['maintenance_revision']['new_reference']
        source = ROOT / self.frozen['source_file']
        self.assertEqual(json.loads(source.read_text()), expected)
        self.assertEqual(source.read_bytes(), common.raw_proposal(self.frozen))

    def test_historical_provenance_is_preserved_and_current_source_is_bound(self):
        revision = self.frozen['maintenance_revision']
        old = json.loads((ROOT / revision['old_record_file']).read_text())
        new = json.loads((ROOT / revision['new_record_file']).read_text())
        self.assertEqual(common.sha((ROOT / revision['old_record_file']).read_bytes()), revision['old_record_file_sha256'])
        self.assertEqual(common.sha((E / revision['historical_source_snapshot']).read_bytes()), old['authored_source_sha256'])
        self.assertEqual(common.objsha(old), revision['old_reference']['sha256'])
        self.assertEqual(common.objsha(new), revision['new_reference']['sha256'])
        self.assertEqual({k:v for k,v in old.items() if k not in ('record_id','authored_source_sha256')},
                         {k:v for k,v in new.items() if k not in ('record_id','authored_source_sha256')})
        source = json.loads((ROOT / self.frozen['source_file']).read_text())
        self.assertEqual(common.objsha({k:v for k,v in source.items() if k != 'maintenance_ref'}), new['authored_source_sha256'])
        self.assertEqual((ROOT / revision['new_record_file']).read_bytes(), (E / revision['new_record_snapshot']).read_bytes())

    def test_complete_merged_state_and_twenty_one_keeps_remain_exact(self):
        self.assertEqual(self.current, self.states['proposal'])
        self.assertEqual(self.current['candidate_bundles'], self.states['baseline']['candidate_bundles'])
        differences = []
        for slot, rows in self.states['baseline']['slots'].items():
            for before, after in zip(rows, self.current['slots'][slot]):
                if before != after:
                    differences.append((slot, before['id']))
        self.assertEqual(differences, [('action','waiting_in_between_use_space')])
        for item in self.frozen['inventory']:
            after = next(x for x in self.current['slots'][item['slot']] if x['id'] == item['id'])
            self.assertEqual(after, item['proposal'])
            if item['decision'] == 'keep':
                self.assertEqual(after, item['before'])

    def test_absent_activity_allows_traces_without_changing_scope_or_guards(self):
        before, after = self.target['before'], self.target['proposal']
        self.assertIn('사용 흔적 없이', before['ko'])
        self.assertNotIn('사용 흔적 없이', after['ko'])
        self.assertIn('예상된 이용 활동 없이', after['ko'])
        self.assertEqual({k:v for k,v in before.items() if k != 'ko'}, {k:v for k,v in after.items() if k != 'ko'})
        self.assertEqual(after['en'], 'waiting in a maintained transition space between expected uses')
        self.assertEqual(after['requires_primary_any_tags'], ['liminal_space','transition','between_use'])
        self.assertIn('a lone subject waits', after['embedding_text'])
        self.assertIn('clean maintained route', after['embedding_text'])
        self.assertIn('expected active use and arrival point are absent', after['embedding_text'])

    def test_actual_korean_catalog_consumer_changes_one_line(self):
        with patch.dict(sys.modules, {'cycle_common':common}):
            catalog = load_module('liminal_catalog_regression', E / 'check_korean_catalog_consumer.py')
        report = catalog.check(require_live_proposal=True)
        self.assertEqual(report['source_rows'], 963)
        self.assertEqual(report['changed_display_rows'], 1)
        self.assertTrue(report['all_other_catalog_lines_exact'])
        self.assertEqual(report['actual_live_state'], 'proposal')
        self.assertEqual(report['api_calls'], 0)
        self.assertEqual(report['source_index_runtime_writes'], 0)

    def test_complete_v6_exposes_both_genuine_actions_without_changing_core(self):
        with patch.dict(sys.modules, {'cycle_common':common}):
            public_gate = load_module('liminal_public_regression', E / 'check_v6_preservation.py')
        report = public_gate.check()
        for key in ['full_pack_equal','candidate_equal','overview_equal','verified_detail_equal',
                    'genuine_elderly_human_and_source_liminal_location_unforced']:
            self.assertTrue(report[key])
        self.assertEqual(report['actual_difference_paths'], [])
        self.assertEqual(report['api_calls'], 0)
        self.assertEqual(report['rule_generations'], 0)
        self.assertEqual(report['retrieval_executions'], 0)
        self.assertEqual(report['writes'], 0)
        before = json.loads((E / 'baseline-actual-v6.json').read_text())
        after = json.loads((E / 'proposal-actual-v6.json').read_text())
        self.assertEqual(before, after)
        self.assertEqual(after['full_pack']['pack_id'], '9a9674d57112ec23')
        self.assertEqual(after['candidate']['id'], common.TARGET)
        ids = {r['id'] for r in after['full_pack']['slots']['action']['candidates']}
        self.assertTrue({common.TARGET,'slot:action:waiting_train'} <= ids)

    def test_acceptance_binds_gains_costs_and_immutable_recovery_history(self):
        self.assertEqual(common.sha((E / 'acceptance-decisions.json').read_bytes()), '7922ebd083519a2c05d229f3c89a3bdc5e245ae74fe2d87323c84ed8c0a77722')
        d = json.loads((E / 'acceptance-decisions.json').read_text())
        self.assertEqual(d['accepted_ids'], [self.target['id']])
        self.assertEqual(d['accepted_fields'], ['ko'])
        self.assertEqual(d['accepted_dictionary_hash'], common.g.dictionary_hash(self.current))
        for name, digest in d['artifact_sha256'].items():
            self.assertEqual(common.sha((E / name).read_bytes()), digest)
        for name, ranks in [('station_positive_ko_lexical',[21,4]),('pool_positive_ko_lexical',[8,1])]:
            item = d['measured_benefits'][name]
            self.assertEqual([item[s]['rank'] for s in ('baseline','proposal')], ranks)
        for name, ranks in [('bedroom_dense_en',[1,1]),('bedroom_dense_ko',[2,2])]:
            item = d['tradeoffs'][name]
            self.assertEqual([item[s]['rank'] for s in ('baseline','proposal')], ranks)
            self.assertGreater(item['proposal']['score'], item['baseline']['score'])
        item = d['tradeoffs']['coexistence_footprints_ko_lexical']
        self.assertEqual([item[s]['rank'] for s in ('baseline','proposal')], [15,15])
        self.assertLess(item['proposal']['score'], item['baseline']['score'])
        for item in d['comparison_summaries']:
            if item['kind'].startswith(('coexistence','near_miss','existing_same_slot_control')):
                self.assertEqual(item['top12_ids']['baseline'], item['top12_ids']['proposal'])
        attempts = json.loads((E / 'api-attempts.json').read_text())
        recovery = json.loads((E / 'confirmed-recovery-plan.json').read_text())
        self.assertEqual(attempts[:2], recovery['recovery']['historical_attempts'])
        self.assertEqual(len(attempts), 15)
        self.assertEqual(sum(x['status']=='completed' for x in attempts), 13)
        self.assertEqual(attempts[2]['number'], 3)
        self.assertEqual(attempts[2]['status'], 'completed')
        self.assertEqual(attempts[2]['sha256'], recovery['recovery']['retry_input_sha256'])
        self.assertEqual(d['cost']['cumulative_project_upper_usd'], 1.2959744)

    def test_independent_queries_and_same_slot_controls_stay_exact(self):
        scout = json.loads((E / 'scout/frozen-proposal-and-unmeasured-probes.json').read_text())
        self.assertEqual([q['original_query'] for q in self.frozen['queries'][:12]], scout['queries'])
        self.assertTrue(all(q['slot'] == 'action' for q in self.frozen['queries']))
        self.assertEqual([q['target'] for q in self.frozen['queries'][-2:]],
                         ['slot:action:ed_cafe_pickup_wait_candidate','slot:action:ed_bus_stop_ready_candidate'])
        available = {'slot:action:'+r['id'] for r in self.current['slots']['action']}
        self.assertTrue(all(q['target'] in available for q in self.frozen['queries']))


if __name__ == '__main__':
    unittest.main()

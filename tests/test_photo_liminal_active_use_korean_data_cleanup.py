"""A suspended use is distinct from removing all evidence of prior use."""
from pathlib import Path
import copy
import importlib.util
import json
import unittest
from unittest.mock import patch
from tests import photo_prompt_fixtures as fixtures

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
        cls.frozen = fixtures.historical_freeze(E)
        cls.states = fixtures.historical_states(E, cls.frozen)
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
        current = json.loads(source.read_text())
        self.assertEqual(current['slots'], expected['slots'])
        self.assertNotIn('auto_optional_policy', current)
        self.assertNotIn('presets', current)

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
        self.assertEqual((ROOT / revision['new_record_file']).read_bytes(), (E / revision['new_record_snapshot']).read_bytes())
        source = json.loads((ROOT / self.frozen['source_file']).read_text())
        live_ref = source['maintenance_ref']
        live = json.loads((ROOT / 'docs/research-evidence/photo-prompt/extension-maintenance' /
                           (live_ref['record_id'] + '.json')).read_text())
        self.assertEqual(common.objsha(live), live_ref['sha256'])
        self.assertEqual(common.objsha({k:v for k,v in source.items() if k != 'maintenance_ref'}), live['authored_source_sha256'])
        self.assertEqual(live['runtime_keys'], ['schema_version', 'slots'])

    def test_complete_merged_state_and_twenty_one_keeps_remain_exact(self):
        # Compare the historical source before later pose/body/acting/iconography overlays.
        # Body integration adds structured semantics to these 13 base entries;
        # every pre-existing field must still equal the frozen historical row.
        # Neither the historical expected values nor the lexical holdouts change.
        filenames = tuple(name for name in common.g.RESEARCH_EXTENSION_FILENAMES
                          if name not in {'photo_prompt_pose_vocabulary_extension.json',
                                          'photo_prompt_body_morphology_extension.json',
                                          'photo_prompt_acting_expression_extension.json',
                                          'photo_prompt_neutral_expression_extension.json',
                                          'photo_prompt_religion_iconography_extension.json',
                                          'photo_prompt_slang_visual_extension.json',
                                          'photo_prompt_subculture_appearance_extension.json',
                                          'photo_prompt_motion_graphics_extension.json'})
        with patch.object(common.g, 'RESEARCH_EXTENSION_FILENAMES', filenames):
            historical_current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')
        # Undo only the independently sealed uniform overlay before the
        # older Vocaloid/body projections. The historical oracle stays exact.
        uniform = ROOT / 'docs/research-evidence/photo-prompt/uniform-costume-integration-20261004'
        delta_path = uniform / 'authored-candidate-delta.json'
        self.assertEqual(common.sha(delta_path.read_bytes()),
                         '531c31e6602b378228bba0005cd4dcaf8703ddfd2d1de8f4d06034a4516a4cb1')
        delta = json.loads(delta_path.read_text())
        uniform_rows = {(item['slot'], item['id']): item for item in delta['rows']
                        if item['file'] == 'photo_prompt_tags.json' or item['file'] in filenames}
        seen_uniform = set()
        for slot, rows in historical_current['slots'].items():
            retained = []
            for row in rows:
                key = (slot, row['id'])
                change = uniform_rows.get(key)
                if change is None:
                    retained.append(row)
                    continue
                self.assertEqual(row, change['after'])
                self.assertEqual(change['before'] is None, change['new'])
                if not change['new']:
                    self.assertEqual({k: v for k, v in row.items()
                                      if k not in {'paraphrases', 'keywords', 'embedding_text'}},
                                     {k: v for k, v in change['before'].items()
                                      if k not in {'paraphrases', 'keywords', 'embedding_text'}})
                    retained.append(copy.deepcopy(change['before']))
                seen_uniform.add(key)
            rows[:] = retained
        self.assertEqual(seen_uniform, set(uniform_rows))
        # Project only the declared later Vocaloid additions. Verify every
        # prior field and the exact positive additions before comparing the
        # original historical dictionary; new IDs cannot shadow existing rows.
        vocaloid = ROOT / 'docs/research-evidence/photo-prompt/vocaloid-appearance-integration-20261004'
        ledger = json.loads((vocaloid / 'INTEGRATION-LEDGER.json').read_text())
        declared = {(item['slot'], item['id']): item for item in ledger['candidate_changes']
                    if item['file'] == 'photo_prompt_tags.json' or item['file'] in filenames}
        with patch.object(common.g, 'RESEARCH_EXTENSION_FILENAMES', filenames):
            before_vocaloid = common.g.load_json(vocaloid / 'baseline/photo_prompt_tags.json')
        original_rows = {(slot, row['id']): row for slot, rows in before_vocaloid['slots'].items() for row in rows}
        current_keys = {(slot, row['id']) for slot, rows in historical_current['slots'].items() for row in rows}
        new_keys = {key for key, item in declared.items() if item['new']}
        self.assertEqual(current_keys - set(original_rows), new_keys)
        self.assertTrue(set(original_rows).issubset(current_keys))
        enriched_fields = {'paraphrases', 'keywords', 'embedding_text'}
        seen_updates = set()
        for slot, rows in historical_current['slots'].items():
            rows[:] = [row for row in rows if (slot, row['id']) not in new_keys]
            for row in rows:
                key = (slot, row['id'])
                item = declared.get(key)
                if not item:
                    continue
                original = original_rows[key]
                self.assertEqual({field: value for field, value in row.items() if field not in enriched_fields},
                                 {field: value for field, value in original.items() if field not in enriched_fields})
                for field in ('paraphrases', 'keywords'):
                    expected_values = list(dict.fromkeys(original.get(field, []) + item['added_paraphrases']))
                    self.assertEqual(row[field], expected_values)
                expected_text = original.get('embedding_text', original.get('en', ''))
                for phrase in item['added_paraphrases']:
                    if phrase not in expected_text:
                        expected_text += ' | ' + phrase
                self.assertEqual(row['embedding_text'], expected_text)
                for field in enriched_fields:
                    if field in original:
                        row[field] = copy.deepcopy(original[field])
                    else:
                        row.pop(field)
                seen_updates.add(key)
        self.assertEqual(seen_updates, set(declared) - new_keys)
        # Main subsequently adds exact canonical opacity effects to two
        # textile candidates. Check those additions before this older replay.
        scope = json.loads((vocaloid / 'main-merge/UPSTREAM-EFFECT-ADDITIONS.json').read_text())
        seen_effects = set()
        for item in scope['changes']:
            if item['kind'] != 'candidate' or item['file'] not in filenames:
                continue
            self.assertEqual(item['removed'], [])
            self.assertEqual(item['added'], [{'dimension': 'appearance', 'target': 'main_subject',
                                             'property': 'wardrobe.surface.sheer_opacity'}])
            row = next(row for rows in historical_current['slots'].values() for row in rows
                       if row['id'] == item['id'])
            self.assertEqual(row['affected_properties'], item['after'])
            row['affected_properties'] = copy.deepcopy(item['before'])
            seen_effects.add(item['id'])
        self.assertEqual(seen_effects, {'clt_ct091_v1', 'clt_ct091_v2'})
        body_enriched_ids = {
            'philtral_columns_cupid_bow', 'clavicle_supraclavicular_hollow',
            'decolletage_neckline_exposure_boundary', 'trochanteric_depression_hip_dip',
            'posterior_psis_dimples_pair', 'infragluteal_crease_boundary',
            'calf_to_ankle_taper', 'bust_to_ribcage_projection_relation',
            'slender_linear_build', 'soft_full_figure_volume',
            'curvilinear_figure_relation', 'toned_muscular_definition',
            'willowy_long_limb_proportion',
        }
        added_fields = {'paraphrases', 'concept_units', 'relations',
                        'affected_dimensions', 'affected_properties', 'core_assertion_discovery'}
        seen = set()
        for slot, rows in historical_current['slots'].items():
            expected = {row['id']: row for row in self.states['proposal']['slots'][slot]}
            for row in rows:
                if row['id'] not in body_enriched_ids:
                    continue
                original = expected[row['id']]
                self.assertTrue(added_fields.isdisjoint(original))
                self.assertEqual(set(row) - set(original), added_fields)
                self.assertEqual({key: row[key] for key in original}, original)
                for field in added_fields:
                    self.assertTrue(row[field])
                for field in added_fields:
                    row.pop(field)
                seen.add(row['id'])
        self.assertEqual(seen, body_enriched_ids)
        # Later instrument corrections change only these six label/text fields.
        # Check their complete authored values, then project the historical rows
        # for the original whole-dictionary and twenty-one-keep assertions below.
        instrument_revisions = {
            ('action', 'trumpet_lip_valve_action'): {
                'ko': '컵 마우스피스에 입술을 대고 왼손으로 트럼펫을 지지하며 오른손 손가락으로 밸브를 조작하는',
                'en': 'playing a trumpet at the cup mouthpiece with left-hand support and right-hand valve fingering',
                'embedding_text': "the player's lips meet a trumpet cup mouthpiece while the left hand supports the folded brass tubing and the right-hand fingers rest on or press a note-appropriate combination of the three aligned piston valves",
            },
            ('body_pose', 'wind_embouchure_two_hand_key_pose'): {
                'ko': '관악기 마우스피스에 입술을 대고 각 손을 악기에 맞는 연주·지지 위치에 둔 자세',
                'en': 'a wind-instrument embouchure pose with each hand in its instrument-specific playing or support role',
                'embedding_text': "the adult player maintains plausible neck and shoulder support while the lips meet the correct mouthpiece and each hand takes the instrument's appropriate playing or support role",
            },
        }
        seen_revisions = set()
        for slot, rows in historical_current['slots'].items():
            expected = {row['id']: row for row in self.states['proposal']['slots'][slot]}
            for row in rows:
                key = (slot, row['id'])
                if key not in instrument_revisions:
                    continue
                original = expected[row['id']]
                revisions = instrument_revisions[key]
                self.assertEqual(set(row), set(original))
                self.assertEqual({field: row[field] for field in revisions}, revisions)
                self.assertEqual({field: value for field, value in row.items() if field not in revisions},
                                 {field: value for field, value in original.items() if field not in revisions})
                for field in revisions:
                    row[field] = original[field]
                seen_revisions.add(key)
        self.assertEqual(seen_revisions, set(instrument_revisions))
        self.assertEqual(historical_current['slots'], self.states['proposal']['slots'])
        historical_bundles = self.states['baseline']['candidate_bundles']
        self.assertEqual(fixtures.bundle_meanings(self.current['candidate_bundles'], within=historical_bundles),
                         fixtures.bundle_meanings(historical_bundles))
        differences = []
        for slot, rows in self.states['baseline']['slots'].items():
            for before, after in zip(rows, historical_current['slots'][slot]):
                if before != after:
                    differences.append((slot, before['id']))
        self.assertEqual(differences, [('action','waiting_in_between_use_space')])
        # The iconography overlay adds only full, equivalent paraphrases to
        # declared existing rows. Protect the exact addition and project those
        # later fields before comparing this frozen twenty-one-keep inventory.
        iconography = json.loads((ASSETS / 'photo_prompt_religion_iconography_extension.json').read_text())
        iconographic_contexts = iconography['existing_slot_context_extensions']
        for item in self.frozen['inventory']:
            after = copy.deepcopy(next(x for x in self.current['slots'][item['slot']] if x['id'] == item['id']))
            update = iconographic_contexts.get(item['slot'], {}).get(item['id'])
            if update:
                self.assertEqual(set(after.get('paraphrases', [])),
                                 set(item['proposal'].get('paraphrases', [])) | set(update['paraphrases']))
                if 'paraphrases' in item['proposal']:
                    after['paraphrases'] = item['proposal']['paraphrases']
                else:
                    after.pop('paraphrases')
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

    def test_archived_korean_catalog_changes_one_line_and_current_text_preserves_it(self):
        report = json.loads((E / 'korean-catalog-consumer.json').read_text())
        self.assertEqual(report['source_rows'], 963)
        self.assertEqual(len(report['changed_display_rows']), 1)
        self.assertTrue(report['all_other_lines_exact'])
        self.assertEqual(report['api_calls'], 0)
        before = (E / 'catalog-baseline.txt').read_text().splitlines()
        after = (E / 'catalog-proposal.txt').read_text().splitlines()
        self.assertEqual([{'before': b, 'proposal': a} for b, a in zip(before, after) if b != a],
                         report['changed_display_rows'])
        row = next(x for x in self.current['slots']['action'] if x['id'] == self.target['id'])
        self.assertIn(row['ko'], common.g.semantic_text_for_entry(row, 'action'))

    def test_historical_v6_preservation_and_current_candidate_projection(self):
        report = json.loads((E / 'actual-v6-preservation.json').read_text())
        self.assertTrue(all(report['checks'].values()))
        self.assertEqual(report['api_calls'], 0)
        self.assertEqual(report['retrieval_executions'], 0)
        self.assertEqual(report['new_rule_generations'], 0)
        self.assertEqual(report['repository_writes'], 0)
        before = json.loads((E / 'baseline-actual-v6.json').read_text())
        after = json.loads((E / 'proposal-actual-v6.json').read_text())
        self.assertEqual(before, after)
        self.assertEqual(after['full_pack']['pack_id'], '9a9674d57112ec23')
        self.assertEqual(after['candidate']['id'], common.TARGET)
        ids = {r['id'] for r in after['full_pack']['slots']['action']['candidates']}
        self.assertTrue({common.TARGET,'slot:action:waiting_train'} <= ids)
        for entry_id in (self.target['id'], 'waiting_train'):
            before_row = next(x for x in self.states['baseline']['slots']['action'] if x['id'] == entry_id)
            after_row = next(x for x in self.current['slots']['action'] if x['id'] == entry_id)
            self.assertEqual(fixtures.project_slot_candidate(self.current, 'action', before_row),
                             fixtures.project_slot_candidate(self.current, 'action', after_row))

    def test_acceptance_binds_gains_costs_and_immutable_recovery_history(self):
        self.assertEqual(common.sha((E / 'acceptance-decisions.json').read_bytes()), '7922ebd083519a2c05d229f3c89a3bdc5e245ae74fe2d87323c84ed8c0a77722')
        d = json.loads((E / 'acceptance-decisions.json').read_text())
        self.assertEqual(d['accepted_ids'], [self.target['id']])
        self.assertEqual(d['accepted_fields'], ['ko'])
        self.assertEqual(d['accepted_dictionary_hash'], self.frozen['state_dictionary_hashes']['proposal'])
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

"""Qualified Korean name coverage must preserve the authored krummholz surface."""
from pathlib import Path
import copy
import hashlib
import gzip
import importlib.util
import json
import unittest
from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
E = ROOT / 'docs/research-evidence/photo-prompt/krummholz-korean-alias-data-cleanup-20261001'
NEXT = ROOT / 'docs/research-evidence/photo-prompt/protostar-korean-alias-data-cleanup-20261001'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


common = load_module('krummholz_frozen_common', E / 'cycle_common.py')
import compose_pack_view as views
from tests import test_photo_authorial_core_v6 as v6_fixtures


class KrummholzKoreanAliasDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = fixtures.historical_freeze(E)
        cls.states = fixtures.historical_states(E, cls.frozen)
        cls.target = next(row for row in cls.frozen['inventory'] if row['decision'] == 'fix')
        cls.current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')
        cls.accepted_snapshot = json.loads(gzip.decompress((NEXT / 'baseline-merged-data.json.gz').read_bytes()))
        cls.runtime = v6_fixtures.PhotoAuthorialCoreV6Tests().runtime_data()
        cls.runtime.pop(common.g.SEMANTIC_INDEX_DATA_KEY, None)
        cls.fixture = json.loads((E / 'scout/synthetic-rule-contract-result.json').read_text())

    def test_exact_frozen_scope_queries_and_budget(self):
        self.assertEqual(hashlib.sha256((E / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
                         '59c87310619cdd8421b8464f2b616466cb904d75da92c05740b3dfb077e42dab')
        self.assertEqual(len(self.frozen['inventory']), 11)
        self.assertEqual(len(self.frozen['queries']), 13)
        self.assertEqual(len({q['query'] for q in self.frozen['queries']}), 13)
        self.assertEqual(self.frozen['maximum_paid_attempts'], 15)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'], .024576)
        self.assertEqual(len(self.frozen['pending_input_sha256']), 12)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        recovery = self.frozen['manual_recovery']
        self.assertEqual(recovery['original_freeze_sha256'],
                         'a230261b40b655517f04700f814d077d9bff53af6c3c390b6b639966aa170938')
        self.assertEqual(recovery['maximum_manual_retries'], 1)
        self.assertEqual(recovery['retry_attempt_number'], 2)
        self.assertEqual(recovery['planned_total_attempts_including_original_failure'], 13)
        self.assertEqual(recovery['retry_input_sha256'], self.frozen['proposal_document']['sha256'])
        original = json.loads((E / 'recovery-revisions/pre-manual-retry/frozen-inventory-queries.json').read_text())
        for field in ['inventory', 'queries', 'approved_inputs', 'acceptance', 'source_file',
                      'state_dictionary_hashes', 'previous_tracked_cost_upper_usd',
                      'maximum_paid_attempts', 'maximum_additional_cost_usd']:
            self.assertEqual(self.frozen[field], original[field])

    def test_complete_raw_extension_has_only_one_alias_append(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        expected = copy.deepcopy(before)
        row = next(r for r in expected['slots'][self.target['slot']] if r['id'] == self.target['id'])
        self.assertEqual(row, self.target['before'])
        row['aliases'].append('왜성변형수 바람형 패치')
        current = json.loads((ROOT / self.frozen['source_file']).read_text())
        self.assertEqual(current['slots'], expected['slots'])
        self.assertEqual(current['maintenance_ref'], before['maintenance_ref'])

    def test_historical_merged_state_and_current_ten_keeps_are_exact(self):
        self.assertEqual(self.accepted_snapshot, self.states['proposal'])
        self.assertEqual(fixtures.bundle_meanings(self.current['candidate_bundles']), fixtures.bundle_meanings(self.states['baseline']['candidate_bundles']))
        for item in self.frozen['inventory']:
            row = next(r for r in self.current['slots'][item['slot']] if r['id'] == item['id'])
            self.assertEqual(row, item['proposal'])
            if item['decision'] == 'keep':
                self.assertEqual(row, item['before'])

    def test_specialization_existing_names_and_every_other_field_are_preserved(self):
        before, after = self.target['before'], self.target['proposal']
        self.assertEqual(after['aliases'], before['aliases'] + ['왜성변형수 바람형 패치'])
        self.assertEqual({k: v for k, v in after.items() if k != 'aliases'},
                         {k: v for k, v in before.items() if k != 'aliases'})
        self.assertEqual(after['en'], 'wind-pruned krummholz patches hugging the ground and sheltering behind rocks')
        self.assertEqual(after['for_any'], ['environment', 'plant'])
        self.assertNotIn('왜성변형수', after['aliases'])

    def test_current_semantic_surface_preserves_frozen_krummholz_meaning(self):
        slot, eid = self.target['slot'], self.target['id']
        outputs = []
        for label, entry in [('before', self.target['before']), ('proposed', self.target['proposal'])]:
            data = {**self.runtime, 'slots': {**self.runtime['slots'], slot: [copy.deepcopy(entry) if row['id'] == eid else row for row in self.runtime['slots'][slot]]}}
            candidate = common.g.photo_candidate_semantics.semantic_source(entry, slot, data['candidate_semantic_policy'])
            self.assertEqual(candidate['concept_units'], [self.target['before']['en']])
            self.assertEqual(candidate['affected_dimensions'], ['material'])
            self.assertEqual(candidate['adoption'], 'optional')
            self.assertEqual(candidate['relations'], [])
            outputs.append(candidate)
        self.assertEqual(outputs[0], outputs[1])

    def test_bare_names_and_independent_probe_texts_remain_frozen(self):
        texts = {q['query'] for q in self.frozen['queries']}
        self.assertTrue({'krummholz', '크룸홀츠', '왜성변형수'} <= texts)
        scout = json.loads((E / 'scout/frozen-proposal-and-unmeasured-probes.json').read_text())
        self.assertEqual(len(scout['queries']), 8)
        self.assertTrue({q['query'] for q in scout['queries']} <= texts)
        self.assertIn('Tall coastal pine shaped by wind', texts)
        self.assertIn('Pruned bonsai beside a garden rock', texts)
        self.assertTrue(all(q['slot'] == 'surface_material' for q in self.frozen['queries']))

    def test_previous_reef_correction_and_all_other_source_rows_remain_intact(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        current = json.loads((ROOT / self.frozen['source_file']).read_text())
        for slot, rows in before['slots'].items():
            for row in rows:
                if slot == self.target['slot'] and row['id'] == self.target['id']:
                    continue
                self.assertEqual(next(r for r in current['slots'][slot] if r['id'] == row['id']), row)
        reef = next(row for row in current['slots']['action'] if row['id'] == 'reef_flat_crest_forereef_wave_gradient')
        self.assertEqual(reef['concept_units'], [reef['en']])
        self.assertEqual(len(reef['en'].split()), 26)


    def test_acceptance_binds_lexical_gain_dense_cost_and_all_attempts(self):
        raw = (E / 'acceptance-decisions.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '04138bc7873da90baae7783b4bf488846d8091d17149a93921ba3d20f44f6ab7')
        decision = json.loads(raw)
        self.assertEqual(decision['accepted_ids'], [self.target['id']])
        self.assertEqual(decision['accepted_fields'], ['aliases'])
        self.assertEqual(decision['accepted_dictionary_hash'], self.frozen['state_dictionary_hashes']['proposal'])
        gain = decision['measured_benefit']['bare_korean_name_lexical']['primary_target']
        self.assertIsNone(gain['baseline']['rank'])
        self.assertEqual(gain['proposal']['rank'], 1)
        cost = decision['tradeoffs']['bare_korean_name_dense']['primary_target']
        self.assertEqual((cost['baseline']['rank'], cost['proposal']['rank']), (24, 31))
        self.assertLess(cost['proposal']['score'], cost['baseline']['score'])
        for row in decision['tradeoffs']['near_misses_remain_dense_rank_one']:
            self.assertEqual(row['primary_target']['baseline']['rank'], 1)
            self.assertEqual(row['primary_target']['proposal']['rank'], 1)
        self.assertEqual(decision['cost']['attempts'], 13)
        self.assertEqual(decision['cost']['unique_successful_inputs'], 12)
        self.assertEqual(decision['cost']['attempted_input_utf8_bytes'], 1644)
        self.assertFalse(decision['preservation']['output_improvement_claimed'])
        for name, expected in decision['evidence_sha256'].items():
            self.assertEqual(hashlib.sha256((E / name).read_bytes()).hexdigest(), expected)


if __name__ == '__main__':
    unittest.main()

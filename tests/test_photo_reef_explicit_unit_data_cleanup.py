"""Source-only reef process correction, with historical deferral preserved."""
from pathlib import Path
import copy
import gzip
import hashlib
import importlib.util
import json
import unittest
from tests import photo_prompt_fixtures as fixtures

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'
E = ROOT / 'docs/research-evidence/photo-prompt/reef-wave-explicit-unit-data-cleanup-20261001'
PUBLIC = ROOT / 'docs/research-evidence/photo-prompt/published-data-v6-surface-audit-20261001'
NEXT = ROOT / 'docs/research-evidence/photo-prompt/krummholz-korean-alias-data-cleanup-20261001'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


common = load_module('reef_explicit_frozen_common', E / 'cycle_common.py')
surface = load_module('reef_explicit_public_surface', PUBLIC / 'replay_public_surfaces.py')
import photo_candidate_semantics as semantics


class ReefExplicitUnitDataCleanupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = fixtures.historical_freeze(E)
        cls.states = fixtures.historical_states(E, cls.frozen)
        cls.target = next(row for row in cls.frozen['inventory'] if row['decision'] == 'fix')
        cls.current = common.g.load_json(ASSETS / 'photo_prompt_tags.json')
        # The following cycle froze the exact published reef state before any
        # further edits. Keep this historical acceptance immutable while the
        # new cycle enforces its own complete current-source delta.
        cls.accepted_snapshot = json.loads(gzip.decompress((NEXT / 'baseline-merged-data.json.gz').read_bytes()))
        cls.runtime = surface.runtime_data()
        cls.contract = json.loads((PUBLIC / 'generated-contract-result.json').read_text())
        cls.preflight = json.loads((E / 'source-and-public-preflight.json').read_text())

    def test_frozen_separate_proposal_queries_and_cost_bound(self):
        self.assertEqual(hashlib.sha256((E / 'frozen-inventory-queries.json').read_bytes()).hexdigest(),
                         '79ce7771737221398456b9d3ff1ce7fa54ea195d8de35d9c0fa7a5721f262f7a')
        self.assertEqual(len(self.frozen['inventory']), 17)
        self.assertEqual(len(self.frozen['queries']), 30)
        self.assertEqual(len({q['query'] for q in self.frozen['queries']}), 30)
        self.assertEqual(self.frozen['maximum_paid_attempts'], 2)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'], .0032768)
        self.assertEqual(self.frozen['automatic_retries'], 0)
        self.assertEqual(len(self.frozen['fresh_document']['text'].encode()), 991)
        self.assertEqual(self.frozen['fresh_document']['sha256'],
                         'ea93ec6f75d76cd12e942ba6b4326abd69337466149e254be242d03bbc6841f1')

    def test_historical_raw_delta_and_current_reef_fields_are_exact(self):
        before = json.loads((E / 'baseline-raw-extension.json').read_text())
        expected = copy.deepcopy(before)
        rows = expected['slots'][self.target['slot']]
        i = next(i for i, row in enumerate(rows) if row['id'] == self.target['id'])
        self.assertEqual(rows[i], self.target['before'])
        rows[i] = copy.deepcopy(self.target['fresh_explicit_unit'])
        current = json.loads((ROOT / self.frozen['source_file']).read_text())
        self.assertEqual(json.loads((NEXT / 'baseline-raw-extension.json').read_text()), expected)
        current_reef = next(row for row in current['slots'][self.target['slot']] if row['id'] == self.target['id'])
        self.assertEqual(current_reef, self.target['fresh_explicit_unit'])
        self.assertEqual(current['maintenance_ref'], before['maintenance_ref'])
        old, new = self.target['before'], self.target['fresh_explicit_unit']
        self.assertEqual({k: v for k, v in old.items() if k not in ('en', 'ko')},
                         {k: v for k, v in new.items() if k not in ('en', 'ko', 'concept_units')})
        self.assertEqual({k: v for k, v in new.items() if k != 'concept_units'}, self.target['old_corrected_labels'])

    def test_historical_merged_delta_and_current_sixteen_controls_are_exact(self):
        self.assertEqual(self.accepted_snapshot, self.states['fresh_explicit_unit'])
        self.assertEqual(self.accepted_snapshot['candidate_bundles'], self.states['baseline']['candidate_bundles'])
        for item in self.frozen['inventory']:
            if item['decision'] != 'keep':
                continue
            with self.subTest(entry=item['id']):
                row = next(row for row in self.current['slots'][item['slot']] if row['id'] == item['id'])
                self.assertEqual(row, item['before'])
                self.assertEqual(row, item['original_inventory_object']['before'])

    def test_exact_old_labels_and_explicit_unit_are_not_tuned_to_results(self):
        old = self.target['old_corrected_labels']
        fresh = self.target['fresh_explicit_unit']
        original = self.target['original_inventory_object']['proposed_after']
        self.assertEqual(old, original)
        self.assertEqual(len(old['en'].split()), 26)
        self.assertEqual(fresh['concept_units'], [old['en']])
        self.assertIn('seaward fore-reef slope', fresh['concept_units'][0])
        self.assertIn('sheltered shallow reef flat on the landward side', fresh['concept_units'][0])

    def test_semantic_surfaces_keep_the_frozen_full_process(self):
        names = [('baseline', 'current_before'), ('old_corrected_labels', 'old_deferred_corrected'),
                 ('fresh_explicit_unit', 'fresh_explicit_unit_proposal')]
        for key, saved_key in names:
            with self.subTest(state=key):
                entry = self.target[key]
                current = common.g.photo_candidate_semantics.semantic_source(entry, self.target['slot'], self.runtime['candidate_semantic_policy'])
                saved = self.preflight['states'][saved_key]['candidate']
                for field in ('concept_units', 'affected_dimensions', 'relations', 'adoption'):
                    self.assertEqual(current[field], saved[field])
                expected_units = entry['keywords'] if key == 'old_corrected_labels' else [entry['en']]
                self.assertEqual(current['concept_units'], expected_units)

    def test_all_original_queries_and_comparator_cache_remain_exact(self):
        cache = common.load_reused_cache(self.frozen)
        self.assertEqual(len(cache), 31)
        for query in self.frozen['queries']:
            self.assertEqual(cache[query['query_sha256']]['text'], query['original_query']['query'])
        self.assertNotIn(self.frozen['fresh_document']['sha256'], cache)

    def test_ebb_is_coexistence_and_direction_probes_are_not_exclusion_guards(self):
        queries = [q['original_query'] for q in self.frozen['queries'][:14]]
        self.assertEqual(sum(q['kind'] == 'coexistence_control' for q in queries), 2)
        self.assertEqual(sum(q['kind'] == 'direction_diagnostic' for q in queries), 2)
        for key in ('for_any', 'tags', 'weight', 'aliases', 'keywords', 'embedding_text'):
            self.assertEqual(self.target['before'][key], self.target['fresh_explicit_unit'][key])
        self.assertEqual(semantics.semantic_source(self.target['fresh_explicit_unit'], 'action', self.current['candidate_semantic_policy'])['relations'], [])

    def test_original_trial_stays_deferred_and_portability_preserves_values(self):
        self.assertFalse(self.frozen['historical_trial']['acceptance_flip'])
        self.assertIn('deferred', self.frozen['historical_trial']['status'])
        old = json.loads((E / 'historical/frozen-inventory-queries.json').read_text())
        self.assertEqual([row['original_inventory_object'] for row in self.frozen['inventory']], old['inventory'])
        self.assertEqual(self.target['old_corrected_labels'], next(row for row in old['inventory'] if row['decision'] == 'fix')['proposed_after'])
        self.assertTrue((E / 'preparation-revisions').is_dir())
        self.assertIn('defer', (E / 'historical/PUBLICATION-DEFERRED.md').read_text().lower())

    def test_acceptance_binds_the_tradeoff_and_retains_adverse_results(self):
        raw = (E / 'acceptance-decisions.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         '24974952019fb46f24b5b4030a4e78d0f9598b9b5dd9bdea27993a071ce54489')
        decision = json.loads(raw)
        self.assertEqual(decision['accepted_ids'], [self.target['id']])
        self.assertEqual(set(decision['accepted_fields']), {'en', 'ko', 'concept_units'})
        self.assertEqual(decision['accepted_dictionary_hash'], self.frozen['state_dictionary_hashes']['fresh_explicit_unit'])
        self.assertEqual(decision['measured_limits']['top5_membership_changes'], 0)
        self.assertEqual(decision['measured_limits']['top12_membership_changes'], 0)
        adverse = {(row['method'], row['query_id']): row for row in decision['adverse_cases']}
        for query in ('reef_primary:q04', 'reef_primary:q06', 'reef_primary:q07', 'reef_primary:q08'):
            self.assertIn(('dense', query), adverse)
        for query in ('reef_primary:q11', 'reef_primary:q12'):
            row = adverse['dense', query]['primary_target']
            self.assertGreater(row['fresh_explicit_unit']['score'], row['baseline']['score'])
        no_hits = {row['query_id'] for row in decision['measured_limits']['korean_lexical_no_hits']}
        self.assertEqual(no_hits, {'reef_primary:q04', 'reef_primary:q08'})
        for filename, expected_hash in decision['evidence_sha256'].items():
            self.assertEqual(hashlib.sha256((E / filename).read_bytes()).hexdigest(), expected_hash)


if __name__ == '__main__':
    unittest.main()

"""Evidence-local safety/shape tests. No runtime writes and no API calls."""
import copy
import datetime as dt
import json
from pathlib import Path
import unittest
from unittest import mock
import cycle_common as c
import evaluate_cycle as ev


class FrozenCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = c.load_freeze()
        cls.states = c.states_from_freeze(cls.frozen)

    def test_exact_scope_and_full_unit(self):
        item = next(x for x in self.frozen['inventory'] if x['decision'] == 'fix')
        old, fresh = item['old_corrected_labels'], item['fresh_explicit_unit']
        self.assertEqual(len(old['en'].split()), 26)
        self.assertEqual(fresh['concept_units'], [old['en']])
        self.assertEqual({k: v for k, v in fresh.items() if k != 'concept_units'}, old)
        for state in self.states.values():
            self.assertEqual(len(c.g.iter_semantic_entries(state)), 10174)
        changed = [(slot, b['id']) for slot, rows in self.states['baseline']['slots'].items() for b, f in zip(rows, self.states['fresh_explicit_unit']['slots'][slot]) if b != f]
        self.assertEqual(changed, [('action', 'reef_flat_crest_forereef_wave_gradient')])

    def test_exact_original_probes(self):
        self.assertEqual(len(self.frozen['queries']), 30)
        self.assertEqual(len({q['query'] for q in self.frozen['queries']}), 30)
        self.assertEqual(len({q['id'] for q in self.frozen['queries']}), 30)
        for q in self.frozen['queries']:
            self.assertEqual(q['query'], q['original_query']['query'])
            self.assertEqual(q['original_query_sha256'], c.objsha(q['original_query']))

    def test_exact_cached_inputs(self):
        cache = c.load_reused_cache(self.frozen)
        self.assertEqual(len(cache), 31)
        self.assertNotIn(self.frozen['fresh_document']['sha256'], cache)
        for q in self.frozen['queries']:
            c.validate_vector(cache[q['query_sha256']], q['query'])
        self.assertEqual(len(self.frozen['fresh_document']['text'].encode()), 991)

    def test_minimal_apply_does_not_write(self):
        path = c.R / self.frozen['source_file']
        original = path.read_bytes()
        proposed = c.raw_proposal(self.frozen)
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(c.sha(proposed), self.frozen['proposed_raw_source_sha256'])
        before, after = json.loads(original), json.loads(proposed)
        self.assertEqual(before['maintenance_ref'], after['maintenance_ref'])
        self.assertEqual(before['auto_optional_policy'], after['auto_optional_policy'])

    def test_bad_cache_rejected(self):
        vector = {'model': c.g.SEMANTIC_MODEL_ID, 'dimensions': 768, 'text': 'test', 'vector': [1.0] * 768}
        c.validate_vector(vector, 'test')
        for bad in [dict(vector, dimensions=767), dict(vector, text='different'), dict(vector, vector=[0.0]*768), dict(vector, vector=[float('nan')]*768)]:
            with self.assertRaises(ValueError):
                c.validate_vector(bad, 'test')

    def test_wrong_paid_input_is_rejected_before_env_or_network(self):
        with mock.patch.object(ev.builder, 'load_project_env', side_effect=AssertionError('Credential read')), mock.patch.object(ev.urllib.request, 'build_opener', side_effect=AssertionError('Network')):
            with self.assertRaises(ValueError):
                ev.call_one_document(self.frozen, {'kind':'query','key':'bad','text':'not the frozen input'}, {}, [], None)

    def test_previous_uncertain_or_failed_attempt_is_never_retried(self):
        work = {'kind':'document','key':c.REEF,'text':self.frozen['fresh_document']['text']}
        for status in ['attempt_started', 'failed_http_no_retry', 'failed_or_uncertain_no_retry', 'completed']:
            with mock.patch.object(ev.builder, 'load_project_env', side_effect=AssertionError('Credential read')), mock.patch.object(ev.urllib.request, 'build_opener', side_effect=AssertionError('Network')):
                with self.assertRaises(ValueError):
                    ev.call_one_document(self.frozen, work, {}, [{'sha256':self.frozen['fresh_document']['sha256'],'status':status}], None)

    def test_stop_deadline_and_budget_guards(self):
        ledger = {'deadline_utc':'2026-10-02T11:46:56Z','tracked_project_cost_upper_usd':1.2075008,'hard_project_budget_usd':10.0}
        with mock.patch.object(c.Path, 'exists', return_value=True):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen)
        for override in [{'deadline_utc':'2000-01-01T00:00:00Z'}, {'tracked_project_cost_upper_usd':10.0}]:
            with mock.patch.object(c.Path, 'exists', return_value=False), mock.patch.object(c, 'read_json', return_value={**ledger, **override}):
                with self.assertRaises(ValueError):
                    c.guard_window(self.frozen, prospective_attempts=1)


if __name__ == '__main__':
    unittest.main(verbosity=2)

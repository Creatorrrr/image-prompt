"""Offline preparation/safety tests; synthetic network mocks, no real calls or retrieval."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import cycle_common as c
import evaluate_cycle as ev


class FrozenCycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen = c.load_freeze()
        cls.states = c.states_from_freeze(cls.frozen)

    def test_exact_append_only_scope(self):
        changed = next(x for x in self.frozen['inventory'] if x['decision'] == 'fix')
        self.assertEqual(changed['proposal']['aliases'],changed['before']['aliases']+[c.ALIAS])
        self.assertEqual({k:v for k,v in changed['proposal'].items() if k != 'aliases'},{k:v for k,v in changed['before'].items() if k != 'aliases'})
        self.assertEqual(len(self.frozen['inventory']),11)
        self.assertEqual(sum(x['decision'] == 'keep' for x in self.frozen['inventory']),10)
        changed_rows = [(slot,b['id']) for slot,rows in self.states['baseline']['slots'].items() for b,p in zip(rows,self.states['proposal']['slots'][slot]) if b != p]
        self.assertEqual(changed_rows,[('surface_material','treeline_wind_pruned_krummholz_surface')])
        for data in self.states.values():
            self.assertEqual(len(c.g.iter_semantic_entries(data)),self.frozen['baseline_document_count'])
            for slot,rows in data['slots'].items():
                for row in rows:
                    if 'treeline' in row.get('tags',[]):
                        self.assertFalse(set(row.get('aliases',[])).intersection(['krummholz','크룸홀츠','왜성변형수']))

    def test_accepted_reef_unit_and_guards_unchanged(self):
        source = json.loads(c.raw_proposal(self.frozen))
        before = c.read_json(c.E / 'baseline-raw-extension.json')
        for key in source:
            if key != 'slots':
                self.assertEqual(source[key],before[key])
        for slot,rows in source['slots'].items():
            if slot != 'surface_material':
                self.assertEqual(rows,before['slots'][slot])
        for data in self.states.values():
            reef = next(r for r in data['slots']['action'] if r['id'] == 'reef_flat_crest_forereef_wave_gradient')
            self.assertEqual(reef['concept_units'],[reef['en']])

    def test_exact_probes_and_existing_unrelated_targets(self):
        queries = self.frozen['queries']
        scout = c.read_json(c.E / 'scout/frozen-proposal-and-unmeasured-probes.json')
        self.assertEqual([q['original_query'] for q in queries[:8]],scout['queries'])
        self.assertEqual([q['query'] for q in queries[8:11]],['krummholz','크룸홀츠','왜성변형수'])
        actual = {'slot:surface_material:'+row['id']:row for row in self.states['baseline']['slots']['surface_material']}
        self.assertEqual([q['target'] for q in queries[-2:]],['slot:surface_material:matte_concrete_surface','slot:surface_material:translucent_glass_block'])
        for q in queries:
            self.assertIn(q['target'],actual)
            self.assertEqual(q['query_sha256'],c.sha(q['query'].encode()))
        self.assertTrue(all('treeline' not in actual[q['target']].get('tags',[]) for q in queries[-2:]))

    def test_exact_cache_and_pending_inputs(self):
        cache = c.load_reused_cache(self.frozen)
        self.assertEqual(len(cache),2)
        self.assertEqual(len(self.frozen['pending_input_sha256']),12)
        self.assertEqual(len(self.frozen['approved_inputs']),14)
        for q in self.frozen['queries'][-2:]:
            c.validate_vector(cache[q['query_sha256']],q['query'])
        self.assertNotIn(self.frozen['proposal_document']['sha256'],cache)
        self.assertEqual(self.frozen['maximum_paid_attempts'],15)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'],.024576)

    def test_minimal_proposal_is_read_only(self):
        path = c.R / self.frozen['source_file']
        original = path.read_bytes()
        proposed = c.raw_proposal(self.frozen)
        self.assertEqual(path.read_bytes(),original)
        self.assertEqual(c.sha(proposed),self.frozen['proposed_raw_source_sha256'])

    def test_saved_controlled_final_surface_equality(self):
        before = c.read_json(c.E / 'scout/before-actual-v6.json')
        after = c.read_json(c.E / 'scout/proposed-actual-v6.json')
        self.assertEqual(before,after)
        for view in ['candidate','detail','overview','full_pack']:
            self.assertEqual(before[view],after[view])
        candidate = before['candidate']
        self.assertEqual(candidate['affected_dimensions'],['material'])
        self.assertEqual(candidate['relations'],[])
        self.assertEqual(candidate['adoption'],'optional')
        result = c.read_json(c.E / 'scout/actual-v6-preservation-result.json')
        self.assertEqual(result['api_calls'],0)
        self.assertEqual(result['retrieval_probe_executions'],0)
        self.assertTrue(all(result['checks'].values()))

    def test_bad_cache_rejected(self):
        good = {'model':c.g.SEMANTIC_MODEL_ID,'dimensions':768,'text':'synthetic','vector':[1.0]*768}
        c.validate_vector(good,'synthetic')
        for bad in [dict(good,model='different'),dict(good,dimensions=767),dict(good,text='different'),dict(good,vector=[0.0]*768),dict(good,vector=[float('nan')]*768),dict(good,vector=[True]*768)]:
            with self.assertRaises(ValueError):
                c.validate_vector(bad,'synthetic')

    def test_wrong_or_reused_input_rejected_before_credentials_or_network(self):
        wrong = {'kind':'query','key':'wrong','text':'not approved','sha256':c.sha(b'not approved')}
        reused = self.frozen['approved_inputs'][-1]
        for work in [wrong,reused]:
            with mock.patch.object(ev.builder,'load_project_env',side_effect=AssertionError('Credentials')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network')):
                with self.assertRaises(ValueError):
                    ev.call_one_input(self.frozen,work,{},[],None)

    def test_previous_attempts_are_never_retried(self):
        work = self.frozen['approved_inputs'][0]
        for status in ['attempt_started','failed_http_no_retry','failed_or_uncertain_no_retry','completed']:
            for h in [work['sha256'],'different']:
                if status == 'completed' and h == 'different':
                    continue
                with mock.patch.object(ev.builder,'load_project_env',side_effect=AssertionError('Credentials')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network')):
                    with self.assertRaises(ValueError):
                        ev.call_one_input(self.frozen,work,{},[{'sha256':h,'status':status}],None)

    def test_stop_deadline_and_live_budget_guards(self):
        ledger = {'deadline_utc':'2026-10-02T11:46:56Z','tracked_project_cost_upper_usd':1.2091392,'hard_project_budget_usd':10.0}
        with mock.patch.object(c.Path,'exists',return_value=True):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen)
        for override in [{'deadline_utc':'2000-01-01T00:00:00Z'},{'tracked_project_cost_upper_usd':10.0}]:
            with mock.patch.object(c.Path,'exists',return_value=False),mock.patch.object(c,'read_json',return_value={**ledger,**override}):
                with self.assertRaises(ValueError):
                    c.guard_window(self.frozen,prospective_attempts=1)
        with mock.patch.object(c.Path,'exists',return_value=False),mock.patch.object(c,'read_json',return_value=ledger):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen,charged_attempts=15,prospective_attempts=1)

    def test_redirect_is_rejected(self):
        self.assertIsNone(ev.NoRedirect().redirect_request(None,None,302,'redirect',{},'https://other.example/'))

    def test_durable_pre_send_log_and_single_mock_call(self):
        work = self.frozen['approved_inputs'][0]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            response = io.StringIO(json.dumps({'embedding':{'values':[1.0]*768}}))
            opener = mock.Mock()
            def open_once(*args,**kwargs):
                durable = c.read_json(temp / 'api-attempts.json')
                self.assertEqual(len(durable),1)
                self.assertEqual(durable[0]['status'],'attempt_started')
                self.assertEqual(durable[0]['sha256'],work['sha256'])
                return response
            opener.open.side_effect = open_once
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'R',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev.builder,'load_project_env'),mock.patch.dict(ev.os.environ,{'GEMINI_API_KEY':'synthetic-test-value'},clear=True),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                attempts,cache = [],{}
                ev.call_one_input(self.frozen,work,cache,attempts,None)
            self.assertEqual(opener.open.call_count,1)
            self.assertEqual(attempts[0]['status'],'completed')
            ev.validate_attempts(self.frozen,attempts,c.read_json(temp / 'new-vector-cache.json'))

    def test_failed_mock_request_logged_without_retry(self):
        work = self.frozen['approved_inputs'][0]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            opener = mock.Mock()
            opener.open.side_effect = TimeoutError('synthetic')
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'R',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev.builder,'load_project_env'),mock.patch.dict(ev.os.environ,{'GEMINI_API_KEY':'synthetic-test-value'},clear=True),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                with self.assertRaises(SystemExit):
                    ev.call_one_input(self.frozen,work,{},[],None)
            self.assertEqual(opener.open.call_count,1)
            self.assertEqual(c.read_json(temp / 'api-attempts.json')[0]['status'],'failed_or_uncertain_no_retry')
            self.assertFalse((temp / 'new-vector-cache.json').exists())

    def test_synthetic_matrix_keeps_no_hits_and_all_deltas(self):
        target = c.TARGET
        data = {'slots':{'surface_material':[{'id':target.split(':')[-1]}]}}
        queries = [{'id':f'synthetic-{i}','query':'synthetic test','query_sha256':'synthetic','kind':'synthetic','slot':'surface_material','target':target} for i in range(13)]
        index = {'entries':{target:{'vector':[1.0,1.0]}}}
        with mock.patch.object(ev.g,'semantic_bm25f_payload_from_index',return_value={}),mock.patch.object(ev,'rank_bm25f',return_value=[]):
            rows = ev.evaluate({'queries':queries},{s:data for s in c.STATES},{s:index for s in c.STATES},{'synthetic':{'vector':[1.0,1.0]}})
        self.assertEqual(len(rows),52)
        self.assertEqual(sum(r['no_hits'] for r in rows),26)
        report = ev.exposure_report(rows)
        self.assertEqual(len(report['comparisons']),26)
        self.assertEqual(len(report['no_hit_cases']),26)
        self.assertTrue(all(x['changed_ranking_entry_count'] == 0 for x in report['comparisons']))


if __name__ == '__main__':
    unittest.main(verbosity=2)

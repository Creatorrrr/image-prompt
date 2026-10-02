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

    def test_exact_ko_only_scope(self):
        changed = next(x for x in self.frozen['inventory'] if x['decision'] == 'fix')
        self.assertEqual(changed['before']['ko'],c.BEFORE_KO)
        self.assertEqual(changed['proposal']['ko'],c.PROPOSED_KO)
        self.assertEqual({k:v for k,v in changed['proposal'].items() if k != 'ko'},{k:v for k,v in changed['before'].items() if k != 'ko'})
        self.assertEqual(len(self.frozen['inventory']),12)
        self.assertEqual(sum(x['decision'] == 'keep' for x in self.frozen['inventory']),11)
        changed_rows = [(slot,b['id']) for slot,rows in self.states['baseline']['slots'].items() for b,p in zip(rows,self.states['proposal']['slots'][slot]) if b != p]
        self.assertEqual(changed_rows,[('aftermath_trace','pov_reduced_purchase_set_trace')])
        for data in self.states.values():
            self.assertEqual(len(c.g.iter_semantic_entries(data)),self.frozen['baseline_document_count'])

    def test_all_other_fields_guards_and_scopes_unchanged(self):
        source = json.loads(c.raw_proposal(self.frozen))
        before = c.read_json(c.E / 'baseline-raw-extension.json')
        for key in source:
            if key not in ('slots', 'maintenance_ref'):
                self.assertEqual(source[key],before[key])
        for slot,rows in source['slots'].items():
            if slot != 'aftermath_trace':
                self.assertEqual(rows,before['slots'][slot])
        self.assertEqual(source['maintenance_ref'], self.frozen['maintenance_revision']['new_reference'])
        self.assertEqual(before['maintenance_ref'], self.frozen['maintenance_revision']['old_reference'])
        changed = next(x for x in self.frozen['inventory'] if x['decision'] == 'fix')
        self.assertEqual(changed['proposal']['concept_units'],[changed['before']['en']])
        self.assertNotIn('진열 공백',changed['proposal']['ko'])
        self.assertIn('결제된 더 작은 필수 식품 묶음',changed['proposal']['ko'])

    def test_exact_probes_and_existing_unrelated_targets(self):
        queries = self.frozen['queries']
        scout = c.read_json(c.E / 'scout/frozen-proposal-and-unmeasured-probes.json')
        self.assertEqual([q['original_query'] for q in queries[:8]],scout['probes'])
        additions = c.read_json(c.E / 'provenance/additional-probes.json')['queries']
        self.assertEqual([q['original_query'] for q in queries[8:]],additions)
        self.assertTrue(all(q['kind'] == 'near_miss_paid_completion_wrong_source_position' for q in queries[8:10]))
        actual = {'slot:aftermath_trace:'+row['id']:row for row in self.states['baseline']['slots']['aftermath_trace']}
        self.assertEqual([q['target'] for q in queries[-2:]],['slot:aftermath_trace:cooling_untouched_drink','slot:aftermath_trace:ep_luggage_beside_waiting_position'])
        for q in queries:
            self.assertIn(q['target'],actual)
            self.assertEqual(q['query_sha256'],c.sha(q['query'].encode()))
            self.assertEqual(q['slot'],'aftermath_trace')
        self.assertTrue(all('food_access_budget_choice_event' not in actual[q['target']].get('tags',[]) for q in queries[-2:]))

    def test_exact_cache_and_pending_inputs(self):
        cache = c.load_reused_cache(self.frozen)
        self.assertEqual(len(cache),0)
        self.assertEqual(len(self.frozen['pending_input_sha256']),13)
        self.assertEqual(len(self.frozen['approved_inputs']),13)
        self.assertEqual(self.frozen['maximum_paid_attempts'],14)
        self.assertAlmostEqual(self.frozen['maximum_additional_cost_usd'],.0229376)
        self.assertEqual(self.frozen['pending_input_utf8_bytes'],sum(len(x['text'].encode()) for x in self.frozen['approved_inputs']))
        self.assertTrue(all(len(x['text'].encode()) <= 8192 for x in self.frozen['approved_inputs']))

    def test_minimal_proposal_is_read_only(self):
        path = c.R / self.frozen['source_file']
        original = path.read_bytes()
        proposed = c.raw_proposal(self.frozen)
        self.assertEqual(path.read_bytes(),original)
        self.assertEqual(c.sha(proposed),self.frozen['proposed_raw_source_sha256'])

    def test_saved_controlled_final_surface_equality(self):
        before = c.read_json(c.E / 'baseline-actual-v6.json')
        after = c.read_json(c.E / 'proposal-actual-v6.json')
        self.assertEqual(before,after)
        for surface in ['candidate','detail','overview','full_pack']:
            self.assertEqual(before[surface],after[surface])
        self.assertEqual(before['candidate']['adoption'],'optional')
        result = c.read_json(c.E / 'actual-v6-preservation.json')
        self.assertEqual(result['api_calls'],0)
        self.assertEqual(result['rule_generation_executions'],0)
        self.assertEqual(result['writes'],0)
        self.assertTrue(result['genuine_human_adult_subject_compatibility_without_force'])
        self.assertEqual(c.read_json(c.E / 'scout/before-actual-v6.json'),c.read_json(c.E / 'scout/proposed-actual-v6.json'))
        self.assertTrue(all(c.read_json(c.E / 'scout/surface-summary.json')['checks'].values()))

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
                    ev.call_one_input(self.frozen,work,{reused['sha256']:{}} if work == reused else {},[],None)

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
        ledger = {'deadline_utc':'2026-10-02T11:46:56Z','tracked_project_cost_upper_usd':1.2500992,'hard_project_budget_usd':10.0}
        with mock.patch.object(c.Path,'exists',return_value=True):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen)
        for override in [{'deadline_utc':'2000-01-01T00:00:00Z'},{'tracked_project_cost_upper_usd':10.0}]:
            with mock.patch.object(c.Path,'exists',return_value=False),mock.patch.object(c,'read_json',return_value={**ledger,**override}):
                with self.assertRaises(ValueError):
                    c.guard_window(self.frozen,prospective_attempts=1)
        with mock.patch.object(c.Path,'exists',return_value=False),mock.patch.object(c,'read_json',return_value=ledger):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen,charged_attempts=14,prospective_attempts=1)

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
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'R',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev,'verify_execution_identity'),mock.patch.object(ev.builder,'load_project_env'),mock.patch.dict(ev.os.environ,{'GEMINI_API_KEY':'synthetic-test-value'},clear=True),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
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
            opener.open.side_effect = ev.urllib.error.URLError(ConnectionRefusedError(111,'secret URL header or credential'))
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'R',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev,'verify_execution_identity'),mock.patch.object(ev.builder,'load_project_env'),mock.patch.dict(ev.os.environ,{'GEMINI_API_KEY':'synthetic-test-value'},clear=True),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                with self.assertRaises(SystemExit):
                    ev.call_one_input(self.frozen,work,{},[],None)
            self.assertEqual(opener.open.call_count,1)
            self.assertEqual(c.read_json(temp / 'api-attempts.json')[0]['status'],'failed_or_uncertain_no_retry')
            self.assertFalse((temp / 'new-vector-cache.json').exists())
            record = c.read_json(temp / 'api-attempts.json')[0]
            self.assertEqual(record['reason_type'],'ConnectionRefusedError')
            self.assertEqual(record['reason_errno'],111)
            self.assertNotIn('secret',(temp / 'api-attempts.json').read_text())

    def test_synthetic_matrix_keeps_no_hits_and_all_deltas(self):
        target = c.TARGET
        data = {'slots':{'aftermath_trace':[{'id':target.split(':')[-1]}]}}
        queries = [{'id':f'synthetic-{i}','query':'synthetic test','query_sha256':'synthetic','kind':'synthetic','slot':'aftermath_trace','target':target} for i in range(12)]
        index = {'entries':{target:{'vector':[1.0,1.0]}}}
        with mock.patch.object(ev.g,'semantic_bm25f_payload_from_index',return_value={}),mock.patch.object(ev,'rank_bm25f',return_value=[]):
            rows = ev.evaluate({'queries':queries},{s:data for s in c.STATES},{s:index for s in c.STATES},{'synthetic':{'vector':[1.0,1.0]}})
        self.assertEqual(len(rows),48)
        self.assertEqual(sum(r['no_hits'] for r in rows),24)
        report = ev.exposure_report(rows)
        self.assertEqual(len(report['comparisons']),24)
        self.assertEqual(len(report['no_hit_cases']),24)
        self.assertTrue(all(x['changed_ranking_entry_count'] == 0 for x in report['comparisons']))



    def test_attempt_and_cache_inconsistency_fails_closed(self):
        work = self.frozen['approved_inputs'][0]
        record = {'number':1,'sha256':work['sha256'],'kind':work['kind'],'key':work['key'],'input_utf8_bytes':len(work['text'].encode()),'per_attempt_upper_usd':self.frozen['per_attempt_upper_usd'],'status':'completed','vector_sha256':'not-a-real-hash'}
        with self.assertRaises(ValueError):
            ev.validate_attempts(self.frozen,[record],{})
        for bad in [[record,{**record,'number':2}],[{**record,'status':'unknown'}],[{**record,'manual_recovery_id':'old'}]]:
            with self.assertRaises(ValueError):
                ev.validate_attempts(self.frozen,bad,{})

    def test_replay_missing_vectors_is_read_only_without_api_fallback(self):
        from argparse import Namespace
        before = (c.E / 'baseline-raw-extension.json').read_bytes()
        proposed = c.raw_proposal(self.frozen)
        index = {'entries':{q['target']:{'slot':'aftermath_trace'} for q in self.frozen['queries']}}
        # Isolate both the applied source and mutable execution artifacts. This
        # must reach the missing-vector guard before and after real measurement,
        # regardless of the live source state or live cache/attempt log.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / 'evidence'
            evidence.mkdir()
            source = root / self.frozen['source_file']
            source.parent.mkdir(parents=True)
            source.write_bytes(proposed)
            (evidence / 'baseline-raw-extension.json').write_bytes(before)
            (evidence / 'frozen-inventory-queries.json').write_bytes((c.E / 'frozen-inventory-queries.json').read_bytes())
            self.assertFalse((evidence / 'new-vector-cache.json').exists())
            self.assertFalse((evidence / 'api-attempts.json').exists())
            snapshot = {str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            with mock.patch.object(ev,'E',evidence),mock.patch.object(ev,'R',root),mock.patch.object(ev,'load_baseline_index',return_value=(index,[])),mock.patch.object(ev.g,'load_json',return_value=self.states['proposal']),mock.patch.object(ev,'write_json',side_effect=AssertionError('Write forbidden')),mock.patch.object(ev,'call_one_input',side_effect=AssertionError('API forbidden')),mock.patch.object(ev.builder,'write_sharded_payload',side_effect=AssertionError('Index write forbidden')),mock.patch.object(ev.builder,'load_project_env',side_effect=AssertionError('Credentials forbidden')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network forbidden')):
                with self.assertRaisesRegex(ValueError,'Replay missing vector; API fallback forbidden'):
                    ev.run(Namespace(execute=False,replay=True,stop_file=None))
            self.assertEqual(snapshot,{str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()})
            self.assertFalse((evidence / 'new-vector-cache.json').exists())
            self.assertFalse((evidence / 'api-attempts.json').exists())

    def test_live_ledger_growth_is_not_hidden(self):
        ledger = {'deadline_utc':'2026-10-02T11:46:56Z','tracked_project_cost_upper_usd':9.999,'hard_project_budget_usd':10.0}
        with mock.patch.object(c.Path,'exists',return_value=False),mock.patch.object(c,'read_json',return_value=ledger):
            with self.assertRaises(ValueError):
                c.guard_window(self.frozen,charged_attempts=1,prospective_attempts=1)

    def test_exact_raw_ko_replacement_preserves_all_other_bytes(self):
        before = (c.E / 'baseline-raw-extension.json').read_bytes()
        after = c.raw_proposal(self.frozen)
        old = json.dumps(c.BEFORE_KO,ensure_ascii=False).encode()
        new = json.dumps(c.PROPOSED_KO,ensure_ascii=False).encode()
        self.assertEqual(before.count(old),1)
        self.assertEqual(after.count(new),1)
        self.assertEqual(after.replace(new,old,1),before)

    def test_diagnostics_never_include_string_reason(self):
        error = ev.urllib.error.URLError('secret URL header or credential')
        self.assertEqual(ev.safe_transport_diagnostics(error),{'error_class':'URLError','reason_type':'str','reason_errno':None})


if __name__ == '__main__':
    unittest.main(verbosity=2)

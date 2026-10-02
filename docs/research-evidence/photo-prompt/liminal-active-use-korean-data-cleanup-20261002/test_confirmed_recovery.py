"""Synthetic attempt3 recovery safety tests; no real network or credentials."""
import copy
import datetime as dt
import inspect
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import cycle_common as c
import evaluate_manual_recovery as prior
import evaluate_confirmed_recovery as ev


class ConfirmedRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen=ev.load_freeze();cls.history=cls.frozen['manual_recovery']['historical_attempts'];cls.work=cls.frozen['approved_inputs'][0]

    def attempts(self):return copy.deepcopy(self.history)

    def completion(self):
        vector=[1.0]*768;r=self.frozen['manual_recovery']
        attempt={**self.history[1],'number':3,'status':'completed','manual_retry_of_attempt':2,'manual_recovery_id':r['id'],'manual_retry_of_attempt_sha256':c.objsha(self.history[1]),'manual_recovery_history_sha256':r['historical_attempts_sha256'],'vector_sha256':c.objsha(vector)}
        cache={self.work['sha256']:{'text':self.work['text'],'model':'gemini-embedding-2','dimensions':768,'vector':vector}}
        return self.attempts()+[attempt],cache

    def test_original_plans_helpers_and_raw_histories_preserved(self):
        snapshots=c.E/'confirmed-recovery/prior-state'
        for name in ['frozen-inventory-queries.json','frozen-sha256.txt','manual-recovery-plan.json','manual-recovery-plan-sha256.txt','evaluate_manual_recovery.py','test_manual_recovery.py']:
            self.assertEqual((c.E/name).read_bytes(),(snapshots/name).read_bytes())
        self.assertEqual(c.sha((c.E/'frozen-inventory-queries.json').read_bytes()),ev.ORIGINAL_FREEZE_SHA256)
        self.assertEqual(c.sha((c.E/'manual-recovery-plan.json').read_bytes()),'5dc6d37a9c1e6041935eb21c28000f09bff475009bd96cfdb6eb63d7d1c73c6b')
        self.assertEqual(self.history[0]['status'],'failed_or_uncertain_no_retry')
        self.assertEqual(self.history[1]['status'],'attempt_started')
        original=prior.load_freeze();effective={**original,'manual_recovery':self.frozen['manual_recovery'],'maximum_paid_attempts':15,'maximum_additional_cost_usd':.024576,'maximum_cumulative_tracked_upper_usd':1.2959744}
        self.assertEqual(self.frozen,effective)

    def test_ranking_index_and_collateral_functions_are_exact(self):
        for name in ['make_index','evaluate','exposure_report']:
            self.assertEqual(inspect.getsource(getattr(ev,name)),inspect.getsource(getattr(prior,name)))

    def test_only_explicit_same_document_with_exact_history_is_permitted(self):
        self.assertTrue(ev.may_retry_confirmed_document(self.frozen,self.work,self.attempts(),True))
        self.assertFalse(ev.may_retry_confirmed_document(self.frozen,self.work,self.attempts(),False))
        for work in [self.frozen['approved_inputs'][1],{**self.work,'sha256':'changed'},{**self.work,'kind':'query'},{**self.work,'key':'different'}]:
            self.assertFalse(ev.may_retry_confirmed_document(self.frozen,work,self.attempts(),True))
        for history in [self.history[:1],[{**self.history[0],'status':'completed'},self.history[1]],[self.history[0],{**self.history[1],'status':'failed_or_uncertain_no_retry'}]]:
            self.assertFalse(ev.may_retry_confirmed_document(self.frozen,self.work,history,True))
        with mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network')):
            with self.assertRaises(ValueError):ev.call_one_input(self.frozen,self.work,{},self.attempts(),None)

    def test_terminal_window_and_no_cache_or_results_are_required(self):
        with tempfile.TemporaryDirectory() as directory,mock.patch.object(ev,'E',Path(directory)):
            ev.require_initial_confirmed_retry_state(self.frozen,self.attempts())
            for name in ['new-vector-cache.json','ranking-results.json','collateral-exposure-comparison.json','validation.json']:
                p=Path(directory)/name;p.write_text('{}')
                with self.assertRaisesRegex(ValueError,'Existing cache/result'):ev.require_initial_confirmed_retry_state(self.frozen,self.attempts())
                p.unlink()
            changed=copy.deepcopy(self.frozen);changed['manual_recovery']['historical_attempts'][1]['utc']=dt.datetime.now(dt.timezone.utc).isoformat()
            with self.assertRaisesRegex(ValueError,'transport window'):ev.require_initial_confirmed_retry_state(changed,changed['manual_recovery']['historical_attempts'])

    def test_exact_attempt3_one_request_durable_history_then_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory);attempts=self.attempts();cache={};c.write_json(temp/'api-attempts.json',attempts)
            opener=mock.Mock()
            def once(request,**kwargs):
                saved=c.read_json(temp/'api-attempts.json');self.assertEqual(saved[:2],self.history)
                self.assertEqual(saved[2]['number'],3);self.assertEqual(saved[2]['status'],'attempt_started');self.assertEqual(saved[2]['manual_retry_of_attempt'],2)
                self.assertEqual(saved[2]['manual_recovery_history_sha256'],c.objsha(self.history))
                self.assertEqual(request.full_url,'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent')
                self.assertEqual(json.loads(request.data),{'model':'models/gemini-embedding-2','content':{'parts':[{'text':self.work['text']}]},'outputDimensionality':768})
                return io.StringIO(json.dumps({'embedding':{'values':[1.0]*768}}))
            opener.open.side_effect=once
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'guard_window',return_value={})as budget,mock.patch.object(ev,'verify_execution_identity')as identity,mock.patch.object(ev,'transient_project_credential',return_value='synthetic'),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                ev.call_one_input(self.frozen,self.work,cache,attempts,None,manual_retry=True)
            self.assertEqual(opener.open.call_count,1);self.assertEqual(identity.call_count,1);self.assertEqual(budget.call_count,2)
            ev.validate_attempts(self.frozen,attempts,c.read_json(temp/'new-vector-cache.json'));ev.require_continuation(self.frozen,attempts)
            self.assertEqual(attempts[:2],self.history)

    def test_new_failure_stops_all_further_requests(self):
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory);attempts=self.attempts();c.write_json(temp/'api-attempts.json',attempts)
            opener=mock.Mock();opener.open.side_effect=ev.urllib.error.URLError(OSError('synthetic private diagnostic'))
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev,'verify_execution_identity'),mock.patch.object(ev,'transient_project_credential',return_value='synthetic'),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                with self.assertRaises(SystemExit):ev.call_one_input(self.frozen,self.work,{},attempts,None,manual_retry=True)
            self.assertEqual(opener.open.call_count,1);self.assertEqual(attempts[:2],self.history);self.assertFalse((temp/'new-vector-cache.json').exists())
            ev.validate_attempts(self.frozen,attempts,{})
            self.assertNotIn('private diagnostic',(temp/'api-attempts.json').read_text())
            for work in [self.work,self.frozen['approved_inputs'][1]]:
                with mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network')):
                    with self.assertRaises(ValueError):ev.call_one_input(self.frozen,work,{},attempts,None,manual_retry=True)

    def test_unknown_duplicate_success_or_history_mutation_fails_closed(self):
        good,cache=self.completion();ev.validate_attempts(self.frozen,good,cache)
        bads=[good[1:],self.attempts()+[{**good[2],'number':4}],self.attempts()+[{**good[2],'sha256':self.frozen['approved_inputs'][1]['sha256']}],self.attempts()+[{**good[2],'status':'unknown'}],self.attempts()+[{**good[2],'manual_recovery_history_sha256':'changed'}],good+[{**good[2],'number':4}]]
        for bad in bads:
            with self.assertRaises(ValueError):ev.validate_attempts(self.frozen,bad,cache)
        for work,provided in [(self.work,cache),(self.work,{}),(self.frozen['approved_inputs'][-1],{})]:
            with mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network')):
                with self.assertRaises(ValueError):ev.call_one_input(self.frozen,work,provided,good,None,manual_retry=True)
        with self.assertRaises(ValueError):ev.validate_attempts(self.frozen,good,{})

    def ledger(self,total=1.2746752):
        return {'deadline_utc':self.frozen['deadline_utc'],'tracked_project_cost_upper_usd':total,'hard_project_budget_usd':10.,'cycles':[{'cycle':16,'frozen_sha256':ev.ORIGINAL_FREEZE_SHA256,'baseline_commit':self.frozen['baseline_commit'],'actual_attempts':2,'actual_attempt_upper_usd':.0032768,'cumulative_tracked_upper_usd':1.2746752}]}

    def test_two_charged_attempts_fifteen_cap_and_independent_growth(self):
        with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=self.ledger()):
            guard=ev.guard_window(self.frozen,charged_attempts=2,prospective_attempts=13);self.assertAlmostEqual(guard['accounted_tracked_upper_usd'],1.2746752)
            guard=ev.guard_window(self.frozen,charged_attempts=15);self.assertAlmostEqual(guard['accounted_tracked_upper_usd'],1.2959744)
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=15,prospective_attempts=1)
        with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=self.ledger(total=9.999)):
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=2,prospective_attempts=1)
        with mock.patch.object(ev.Path,'exists',return_value=True):
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=2)
        ledger=self.ledger();ledger['deadline_utc']='2000-01-01T00:00:00Z'
        with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=ledger):
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=2)

    def test_identity_rechecks_prior_and_confirmed_contracts(self):
        with mock.patch.object(prior,'git',return_value=(self.frozen['baseline_commit']+'\n').encode()):ev.verify_execution_identity(self.frozen)
        with mock.patch.object(prior,'verify_execution_identity',side_effect=ValueError('changed original source/runtime/HEAD')):
            with self.assertRaisesRegex(ValueError,'changed original'):ev.verify_execution_identity(self.frozen)
        with mock.patch.object(prior,'verify_execution_identity'),mock.patch.object(ev,'load_freeze',return_value={}):
            with self.assertRaisesRegex(ValueError,'effective cap changed'):ev.verify_execution_identity(self.frozen)

    def test_offline_replay_missing_vectors_never_writes_or_calls(self):
        from argparse import Namespace
        attempts,cache=self.completion();states=c.states_from_freeze(self.frozen);index={'entries':{q['target']:{'slot':'action'}for q in self.frozen['queries']}}
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory);c.write_json(temp/'api-attempts.json',attempts);c.write_json(temp/'new-vector-cache.json',cache)
            for name in ['frozen-inventory-queries.json','confirmed-recovery-plan.json','baseline-raw-extension.json']:(temp/name).write_bytes((c.E/name).read_bytes())
            before={p.name:p.read_bytes()for p in temp.iterdir()}
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'load_freeze',return_value=self.frozen),mock.patch.object(ev,'load_baseline_index',return_value=(index,[])),mock.patch.object(ev.g,'load_json',return_value=states['proposal']),mock.patch.object(ev,'write_json',side_effect=AssertionError('Write')),mock.patch.object(ev,'call_one_input',side_effect=AssertionError('API')),mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials')),mock.patch.object(ev.builder,'write_sharded_payload',side_effect=AssertionError('Index write')):
                with self.assertRaisesRegex(ValueError,'Replay missing vector; API fallback forbidden'):ev.run(Namespace(execute=False,replay=True,stop_file=None,manual_retry_document_attempt_three=False))
            self.assertEqual(before,{p.name:p.read_bytes()for p in temp.iterdir()})


if __name__=='__main__':unittest.main(verbosity=2)

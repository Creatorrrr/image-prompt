"""Synthetic-only recovery safety tests. No real credential/network/API activity."""
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import evaluate_manual_recovery as ev
import evaluate_cycle as original
import cycle_common as c


class ManualRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.frozen=ev.load_freeze()
        cls.first=cls.frozen['manual_recovery']['failed_attempt']
        cls.work=cls.frozen['approved_inputs'][0]
        cls.next_work=cls.frozen['approved_inputs'][1]

    def initial(self):
        return [copy.deepcopy(self.first)]

    def completed_retry(self):
        vector=[1.0]*768
        recovery=self.frozen['manual_recovery']
        record={**self.first,'number':2,'status':'completed','manual_retry_of_attempt':1,'manual_recovery_id':recovery['id'],'manual_retry_of_attempt_sha256':recovery['failed_attempt_object_sha256'],'vector_sha256':c.objsha(vector)}
        value={'text':self.work['text'],'vector':vector,'model':'gemini-embedding-2','dimensions':768}
        return record,{self.work['sha256']:value}

    def test_original_freeze_scripts_and_failure_bytes_are_exact(self):
        for name in ['frozen-inventory-queries.json','frozen-sha256.txt','evaluate_cycle.py','cycle_common.py','test_frozen_cycle.py']:
            self.assertEqual((c.E/name).read_bytes(),(c.E/'manual-recovery/original'/name).read_bytes())
        self.assertEqual(c.sha((c.E/'frozen-inventory-queries.json').read_bytes()),ev.ORIGINAL_FREEZE_SHA256)
        self.assertEqual(c.read_json(c.E/'manual-recovery/original/api-attempts.json'),[self.first])
        self.assertEqual(self.frozen['maximum_paid_attempts'],14)
        self.assertEqual(self.frozen['maximum_additional_cost_usd'],.0229376)
        self.assertEqual(self.frozen['planned_result_rows'],56)

    def test_default_and_original_evaluators_refuse_retry(self):
        for module in [original,ev]:
            with mock.patch.object(module,'transient_project_credential',side_effect=AssertionError('Credentials forbidden')),mock.patch.object(module.urllib.request,'build_opener',side_effect=AssertionError('Network forbidden')):
                with self.assertRaises(ValueError):
                    module.call_one_input(self.frozen,self.work,{},self.initial(),None)

    def test_only_exact_first_document_can_use_explicit_flag(self):
        self.assertTrue(ev.may_retry_first_document(self.frozen,self.work,self.initial(),True))
        self.assertFalse(ev.may_retry_first_document(self.frozen,self.work,self.initial(),False))
        for work in [self.next_work,{**self.work,'sha256':'changed'},{**self.work,'kind':'query'},{**self.work,'key':'different'}]:
            self.assertFalse(ev.may_retry_first_document(self.frozen,work,self.initial(),True))
        for attempts in [[],[{**self.first,'status':'completed'}],[{**self.first,'error_class':'changed'}]]:
            self.assertFalse(ev.may_retry_first_document(self.frozen,self.work,attempts,True))

    def test_explicit_retry_has_one_same_payload_request_after_durable_log(self):
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory);attempts=self.initial();cache={}
            c.write_json(temp/'api-attempts.json',attempts)
            opener=mock.Mock()
            def request_once(request,**kwargs):
                durable=c.read_json(temp/'api-attempts.json')
                self.assertEqual(durable[0],self.first)
                self.assertEqual(durable[1]['number'],2)
                self.assertEqual(durable[1]['status'],'attempt_started')
                self.assertEqual(durable[1]['manual_retry_of_attempt'],1)
                self.assertEqual(request.full_url,'https://generativelanguage.googleapis.com/v1beta/models/gemini-embedding-2:embedContent')
                payload=json.loads(request.data)
                self.assertEqual(payload,{'model':'models/gemini-embedding-2','content':{'parts':[{'text':self.work['text']}]},'outputDimensionality':768})
                self.assertEqual(c.sha(payload['content']['parts'][0]['text'].encode()),ev.RETRY_INPUT_SHA256)
                return io.StringIO(json.dumps({'embedding':{'values':[1.0]*768}}))
            opener.open.side_effect=request_once
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'guard_window',return_value={}) as budget,mock.patch.object(ev,'verify_execution_identity') as identity,mock.patch.object(ev,'transient_project_credential',return_value='synthetic'),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                ev.call_one_input(self.frozen,self.work,cache,attempts,None,manual_retry=True)
            self.assertEqual(opener.open.call_count,1)
            self.assertEqual(identity.call_count,1)
            self.assertEqual(budget.call_count,2)
            self.assertEqual(attempts[0],self.first)
            ev.validate_attempts(self.frozen,attempts,c.read_json(temp/'new-vector-cache.json'))
            ev.require_continuation(self.frozen,attempts)
            self.assertFalse(ev.may_retry_first_document(self.frozen,self.work,attempts,True))

    def test_retry_failure_is_terminal_and_original_is_immutable(self):
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory);attempts=self.initial();c.write_json(temp/'api-attempts.json',attempts)
            opener=mock.Mock();opener.open.side_effect=ev.urllib.error.URLError(OSError('synthetic sensitive diagnostics'))
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'guard_window',return_value={}),mock.patch.object(ev,'verify_execution_identity'),mock.patch.object(ev,'transient_project_credential',return_value='synthetic'),mock.patch.object(ev.urllib.request,'build_opener',return_value=opener):
                with self.assertRaises(SystemExit):
                    ev.call_one_input(self.frozen,self.work,{},attempts,None,manual_retry=True)
            self.assertEqual(opener.open.call_count,1)
            self.assertEqual(attempts[0],self.first)
            self.assertEqual(attempts[1]['status'],'failed_or_uncertain_no_retry')
            self.assertFalse((temp/'new-vector-cache.json').exists())
            self.assertNotIn('sensitive',(temp/'api-attempts.json').read_text())
            ev.validate_attempts(self.frozen,attempts,{})
            for work in [self.work,self.next_work]:
                for flag in [False,True]:
                    with mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials forbidden')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network forbidden')):
                        with self.assertRaises(ValueError):
                            ev.call_one_input(self.frozen,work,{},attempts,None,manual_retry=flag)

    def test_no_successful_or_reused_input_can_be_retried(self):
        retry,cache=self.completed_retry();attempts=self.initial()+[retry]
        for work,provided in [(self.work,cache),(self.work,{}),(self.frozen['approved_inputs'][-1],{})]:
            with mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials forbidden')),mock.patch.object(ev.urllib.request,'build_opener',side_effect=AssertionError('Network forbidden')):
                with self.assertRaises(ValueError):
                    ev.call_one_input(self.frozen,work,provided,attempts,None,manual_retry=True)

    def test_attempt_validation_rejects_scope_and_provenance_changes(self):
        retry,cache=self.completed_retry();good=self.initial()+[retry]
        ev.validate_attempts(self.frozen,good,cache)
        bad_cases=[[],[{**self.first,'error_class':'altered'},retry],self.initial()+[{**retry,'manual_retry_of_attempt':0}],self.initial()+[{**retry,'manual_unrecognized':'bad'}],self.initial()+[{**retry,'status':'unknown'}],good+[{**retry,'number':3}],good+[{**retry,'number':3,'sha256':self.next_work['sha256']}]]
        for bad in bad_cases:
            with self.subTest(attempts=len(bad)):
                with self.assertRaises(ValueError):ev.validate_attempts(self.frozen,bad,cache)
        with self.assertRaises(ValueError):ev.validate_attempts(self.frozen,good,{})

    def ledger(self,credited=1,total=1.2730368):
        return {'deadline_utc':self.frozen['deadline_utc'],'tracked_project_cost_upper_usd':total,'hard_project_budget_usd':10.,'cycles':[{'cycle':16,'frozen_sha256':ev.ORIGINAL_FREEZE_SHA256,'baseline_commit':self.frozen['baseline_commit'],'actual_attempts':credited,'actual_attempt_upper_usd':credited*self.frozen['per_attempt_upper_usd'],'cumulative_tracked_upper_usd':self.frozen['previous_tracked_cost_upper_usd']+credited*self.frozen['per_attempt_upper_usd']}]}

    def test_budget_counts_failure_once_and_preserves_independent_live_growth(self):
        with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=self.ledger()):
            guard=ev.guard_window(self.frozen,charged_attempts=1,prospective_attempts=13)
            self.assertAlmostEqual(guard['accounted_tracked_upper_usd'],1.2730368)
            self.assertEqual(guard['ledger_cycle_attempts_already_credited'],1)
            guard=ev.guard_window(self.frozen,charged_attempts=14)
            self.assertAlmostEqual(guard['accounted_tracked_upper_usd'],1.294336)
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=14,prospective_attempts=1)
        with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=self.ledger(total=9.999)):
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=1,prospective_attempts=1)

    def test_stop_deadline_and_inconsistent_ledger_fail_closed(self):
        with mock.patch.object(ev.Path,'exists',return_value=True):
            with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=1)
        ledger=self.ledger();ledger['deadline_utc']='2000-01-01T00:00:00Z'
        bad_credit=self.ledger(credited=2)
        bad_identity=self.ledger();bad_identity['cycles'][0]['frozen_sha256']='different'
        bad_charge=self.ledger();bad_charge['cycles'][0]['actual_attempt_upper_usd']=0
        for bad in [ledger,bad_credit,bad_identity,bad_charge]:
            with mock.patch.object(ev.Path,'exists',return_value=False),mock.patch.object(ev,'read_json',return_value=bad):
                with self.assertRaises(ValueError):ev.guard_window(self.frozen,charged_attempts=1,prospective_attempts=1)

    def test_identity_checker_rechecks_all_frozen_runtime_and_metadata(self):
        # Execution identity is checked against the baseline HEAD; synthetic
        # HEAD keeps this safety test valid after the owner publishes evidence.
        with mock.patch.object(ev,'git',return_value=(self.frozen['baseline_commit']+'\n').encode()):
            ev.verify_execution_identity(self.frozen)
        for name in ['load_freeze','raw_proposal']:
            with mock.patch.object(ev,'git',return_value=(self.frozen['baseline_commit']+'\n').encode()),mock.patch.object(ev,name,side_effect=ValueError('synthetic changed evidence')):
                with self.assertRaisesRegex(ValueError,'changed evidence'):
                    ev.verify_execution_identity(self.frozen)
        with mock.patch.object(ev,'git',return_value=b'different-head\n'):
            with self.assertRaisesRegex(ValueError,'HEAD changed'):
                ev.verify_execution_identity(self.frozen)

    def test_unknown_or_late_recovery_flag_is_rejected(self):
        from argparse import Namespace
        retry,cache=self.completed_retry()
        self.assertFalse(ev.may_retry_first_document(self.frozen,self.work,self.initial()+[retry],True))
        with self.assertRaises(ValueError):ev.require_continuation(self.frozen,self.initial())
        ev.require_continuation(self.frozen,self.initial(),permit_initial_manual_retry=True)
        with self.assertRaises(ValueError):ev.require_continuation(self.frozen,self.initial()+[{**retry,'status':'attempt_started'}])

    def test_replay_missing_vector_never_calls_api_or_writes(self):
        from argparse import Namespace
        # A successful synthetic recovery with remaining queries must hit the
        # offline missing-vector guard, without a provider or index fallback.
        retry,cache=self.completed_retry();attempts=self.initial()+[retry]
        states=c.states_from_freeze(self.frozen)
        index={'entries':{q['target']:{'slot':'action'}for q in self.frozen['queries']}}
        with tempfile.TemporaryDirectory() as directory:
            temp=Path(directory)
            c.write_json(temp/'api-attempts.json',attempts);c.write_json(temp/'new-vector-cache.json',cache)
            (temp/'frozen-inventory-queries.json').write_bytes((c.E/'frozen-inventory-queries.json').read_bytes())
            (temp/'manual-recovery-plan.json').write_bytes((c.E/'manual-recovery-plan.json').read_bytes())
            (temp/'baseline-raw-extension.json').write_bytes((c.E/'baseline-raw-extension.json').read_bytes())
            before={p.name:p.read_bytes()for p in temp.iterdir()}
            with mock.patch.object(ev,'E',temp),mock.patch.object(ev,'load_freeze',return_value=self.frozen),mock.patch.object(ev,'load_baseline_index',return_value=(index,[])),mock.patch.object(ev.g,'load_json',return_value=states['proposal']),mock.patch.object(ev,'write_json',side_effect=AssertionError('Write forbidden')),mock.patch.object(ev,'call_one_input',side_effect=AssertionError('API forbidden')),mock.patch.object(ev,'transient_project_credential',side_effect=AssertionError('Credentials forbidden')),mock.patch.object(ev.builder,'write_sharded_payload',side_effect=AssertionError('Index write forbidden')):
                with self.assertRaisesRegex(ValueError,'Replay missing vector; API fallback forbidden'):
                    ev.run(Namespace(execute=False,replay=True,stop_file=None,manual_retry_first_document=False))
            self.assertEqual(before,{p.name:p.read_bytes()for p in temp.iterdir()})


if __name__=='__main__':
    unittest.main(verbosity=2)

"""Writer/intake/review regressions against an exact sealed native closure.

PHOTO_H_F2_TEST_NATIVE may select a staged release. No generation/provider calls.
"""
import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1]
CONFIG = json.loads((SKILL / 'retrieval-runtime.json').read_bytes())
NATIVE = Path(os.environ.get('PHOTO_H_F2_TEST_NATIVE', Path.home() /
    '.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations' / CONFIG['native_generation_id']))
sys.path[:0] = [str(NATIVE / 'scripts'), str(NATIVE / 'precore')]
import record_image_run as recorder
import photo_workflow as workflow
import photo_workflow_reviews as reviews
import photo_native_bridge as bridge
import photo_api_render as api
import photo_workflow_worker as worker
import prepare_photo_run as intake
import audit_image_render_review as generic
import audit_moe_render_review as visual


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Recorder(unittest.TestCase):
    def args(self, *extra):
        return recorder.parse_args(['--ts', '2026-10-21T00:00:00Z', '--attempt', '1',
            '--status', 'error', '--failure-reason', 'Synthetic contract fixture; no provider call.',
            '--tool', 'contract_fixture', '--prompt-en', 'Synthetic writer contract fixture.',
            '--candidate-pack-version', 'v10', *extra])

    def test_version_is_derived_from_actual_contract(self):
        self.assertEqual(recorder.candidate_pack_version({'contract_version': 'photo-candidate-pack/v10'}), 'v10')
        for pack in ({}, {'contract_version': 'photo-candidate-pack/v9'}, [], None):
            with self.subTest(pack=pack), self.assertRaises(ValueError):
                recorder.candidate_pack_version(pack)

    def test_old_cli_selector_is_rejected_before_write(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            self.args('--candidate-pack-version', 'v9')

    def test_programmatic_old_selector_is_rejected(self):
        args = self.args(); args.candidate_pack_version = 'v9'
        with self.assertRaises(ValueError): recorder.build_entry(args)

    def test_manifest_and_ledger_share_current_version(self):
        args = self.args('--arm-id', 'synthetic', '--worktree-id', 'contract-fixture',
            '--skill-sha256', 'a'*64, '--source-ref', 'synthetic-unit-test',
            '--authorial-core-sha256', 'b'*64, '--intent-lock-sha256', 'c'*64,
            '--image-call-count', '1', '--independent-no-cross-arm-inputs')
        entry = recorder.build_entry(args)
        manifest = recorder.build_independent_manifest(entry, args)
        self.assertEqual(entry['candidate_pack_version'], 'v10')
        self.assertEqual(manifest['candidate_pack_version'], 'v10')
        entry['candidate_pack_version'] = 'v9'
        with self.assertRaises(ValueError): recorder.build_independent_manifest(entry, args)

    def test_append_preserves_historical_row_bytes(self):
        old = b'{"run_id":"historic","candidate_pack_version":"v9"}\n'
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory)/'history.ndjson'; ledger.write_bytes(old)
            entry = recorder.build_entry(self.args())
            recorder.append_entry(ledger, entry)
            self.assertTrue(ledger.read_bytes().startswith(old))
            recorder.append_entry(ledger, entry)
            self.assertEqual(len(ledger.read_bytes().splitlines()), 2)

    def test_independent_workflow_flags_use_current_version(self):
        args = NS(manifest=Path('/synthetic/manifest.json'), arm_id='arm', worktree_id='fixture',
            skill_sha256='a'*64, source_ref='fixture', image_call_count=0,
            independent_no_cross_arm_inputs=True, reference_sha256=[])
        flags = workflow.native_manifest_flags(args, pack_version=recorder.candidate_pack_version(
            {'contract_version': 'photo-candidate-pack/v10'}))
        self.assertEqual(flags[flags.index('--candidate-pack-version')+1], 'v10')

    def test_native_validator_derives_and_rejects_conflicting_label(self):
        pack = {'contract_version':'photo-candidate-pack/v10', 'pack_id':'fixture',
                'authorial_core':{'canonical_sha256':'a'*64,'intent_lock':{'canonical_sha256':'b'*64}}}
        composed = {'prompt_en':'Fixture prompt.', 'negative_en':None,
                    'chosen_candidate_ids':[], 'chosen_visual_concept_ids':[]}
        request = {'runtime_prompt_en':'Fixture prompt.'}
        plan = {'schema_version':'photo-native-plan/v1','operation_id':'fixture',
                'timestamp':'time','inputs':{},'runtime_store':'/synthetic',
                'payload':{'prompt':'Fixture prompt.','transparent_background':False}}
        entry = {'workflow_operation_id':'fixture:1','ts':'time','pack_id':'fixture',
                 **composed, 'authorial_core_sha256':'a'*64,'intent_lock_sha256':'b'*64}
        values = {'pack':pack, 'composed':composed, 'render_request':request}
        audits = {key:{'status':'pass','failures':[]} for key in ('composed_audit','runtime_audit')}
        with tempfile.TemporaryDirectory() as directory, patch.object(worker,'audit_bound',return_value=audits), \
                patch.object(bridge,'value',side_effect=lambda state,role:values[role]):
            path = Path(directory)/'plan.json'; raw = json.dumps(plan).encode(); path.write_bytes(raw)
            self.assertEqual(bridge.validate_native_record(path,sha(raw),entry)['candidate_pack_version'],'v10')
            with self.assertRaisesRegex(ValueError,'native_record_pack_version_mismatch'):
                bridge.validate_native_record(path,sha(raw),{**entry,'candidate_pack_version':'v9'})

    def test_api_validator_binds_original_pack_not_label(self):
        inputs = {}
        for key,value in {'pack':{'contract_version':'photo-candidate-pack/v10'},'receipt':{},'composed':{},'request':{}}.items():
            raw=json.dumps(value);inputs[key]={'raw_utf8':raw,'sha256':api.text_digest(raw),'value':value,'path':'/synthetic'}
        execution = {'model':'fixture','size':'fixture','prompt_en':'Fixture','negative_en':None,
            'pack_id':'fixture','chosen_candidate_ids':[],'chosen_visual_concept_ids':[],
            'composer':'agent','runtime_prompt_sha256':sha(b'Fixture'),'authorial_core_sha256':'a'*64,
            'intent_lock_sha256':'b'*64,'runtime_prompt_en':'Fixture'}
        document = {'schema_version':api.VERSION,'status':'pass','inputs':inputs,'execution':execution,'runtime_store':None}
        entry = {k:execution[k] for k in ('prompt_en','negative_en','pack_id','chosen_candidate_ids',
            'chosen_visual_concept_ids','composer','runtime_prompt_sha256','authorial_core_sha256','intent_lock_sha256')}
        entry.update(audit_status='pass',requested_image_model='fixture',image_size='fixture')
        with tempfile.TemporaryDirectory() as directory, patch.object(api,'audit_inputs',return_value={}):
            path=Path(directory)/'preflight.json';raw=json.dumps(document).encode();path.write_bytes(raw)
            self.assertEqual(api.validate_api_render_input(path,sha(raw),entry)['candidate_pack_version'],'v10')
            with self.assertRaisesRegex(ValueError,'actual pack'):
                api.validate_api_render_input(path,sha(raw),{**entry,'candidate_pack_version':'v9'})


class Intake(unittest.TestCase):
    def test_offsets_and_exact_quote_are_equivalent_unicode(self):
        request='가🙂나\r\n끝';span={'span_id':'scene','start':1,'end':3}
        expected=[{**span,'text':'🙂나'}]
        self.assertEqual(intake.normalize_input_spans(request,[span]),expected)
        self.assertEqual(intake.normalize_input_spans(request,expected),expected)
        self.assertNotIn('text',span)

    def test_bad_spans_rejected(self):
        base={'span_id':'scene','start':0,'end':2}
        for change in ({'text':'wrong'},{'start':True},{'start':0.0},{'end':99},{'start':-1},
                       {'end':0},{'extra':'untrusted'}):
            with self.subTest(change=change),self.assertRaises(ValueError):
                intake.normalize_input_spans('가🙂나',[{**base,**change}])

    def test_real_init_preserves_bytes_and_rejects_before_creating_run(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);request=root/'request.txt';raw='가🙂나\r\nSave.'.encode();request.write_bytes(raw)
            spans=root/'spans.json';spans.write_text(json.dumps([{'span_id':'scene','start':0,'end':3,'text':'가🙂나'}]))
            argv=[sys.executable,str(NATIVE/'precore/prepare_photo_run.py'),'init','--request',str(request),
                '--spans',str(spans),'--mode','prompt_only','--run',str(root/'valid')]
            result=subprocess.run(argv,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            state=json.loads((root/'valid/workflow.json').read_bytes())
            self.assertEqual(Path(state['artifacts']['request_raw']['path']).read_bytes(),raw)
            spans.write_text(json.dumps([{'span_id':'scene','start':0,'end':3,'text':'invented'}]))
            argv[-1]=str(root/'invalid');result=subprocess.run(argv,capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertIn('span_text_mismatch',result.stdout+result.stderr)
            self.assertFalse((root/'invalid').exists())

    def test_only_omitted_disabled_axes_are_stamped(self):
        pack={'adult_appeal':{'enabled':True,'axes':{'disabled':{'intensity':0},'active':{'intensity':2}}}}
        composed={'prompt_en':'Authored','adult_appeal_brief':{'axes':{}}}
        workflow.bind_disabled_appeal_axes(pack,composed)
        self.assertEqual(composed,{'prompt_en':'Authored','adult_appeal_brief':{'axes':{'disabled':{'intensity':0}}}})
        composed['adult_appeal_brief']['axes']['disabled']={'intensity':3}
        workflow.bind_disabled_appeal_axes(pack,composed)
        self.assertEqual(composed['adult_appeal_brief']['axes']['disabled']['intensity'],3)
        self.assertNotIn('active',composed['adult_appeal_brief']['axes'])


class Review(unittest.TestCase):
    def row(self,**extra):
        return {'status':'pass','evidence':'The actual visible connection is described here.',
                'reviewed_scales':['native'],'observability':'visible',**extra}

    def review(self,**row):
        return {'hard_gates':{'relation':self.row(**row)},'user_judgment':{
            'baseline_available':False,'genuinely_moe':'pending',
            'better_than_baseline':'not_applicable','source':'not_yet_received'}}

    def test_pending_judgment_is_valid_shape_not_acceptance(self):
        self.assertEqual(reviews.input_failures(self.review(),'visual_review'),[])

    def test_null_or_unhashable_judgment_fields_return_paths(self):
        for field in ('baseline_available','genuinely_moe','better_than_baseline','source'):
            for value in (None,{}):
                review=self.review();review['user_judgment'][field]=value
                failures=reviews.input_failures(review,'visual_review')
                self.assertIn('user_judgment.'+field,[r['check'] for r in failures])

    def test_partial_and_unobservable_cannot_pass(self):
        for coverage in ('partial','unobservable','unreviewed',{},None):
            failures=reviews.input_failures(self.review(observability=coverage),'visual_review')
            self.assertIn('hard_gates.relation.observability',[r['check'] for r in failures])

    def test_partial_failure_is_valid_record(self):
        self.assertEqual(reviews.input_failures(self.review(status='fail',observability='partial'),'visual_review'),[])

    def test_new_managed_review_requires_coverage_but_historical_auditor_allows_omission(self):
        review=self.review();del review['hard_gates']['relation']['observability']
        self.assertIsNone(generic.observability_failure(review['hard_gates']['relation'],'relation'))
        self.assertIn('hard_gates.relation.observability',[r['check'] for r in reviews.input_failures(review,'visual_review')])

    def test_wrong_gate_types_are_diagnostics_not_crashes(self):
        for change in ({'status':{}},{'reviewed_scales':[{}]},{'reviewed_scales':['native','native']},{'evidence':None}):
            self.assertTrue(reviews.input_failures(self.review(**change),'visual_review'))

    def test_invalid_record_never_enters_native_audit_or_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'review.json';review=self.review();review['user_judgment']['source']=None
            path.write_text(json.dumps(review));state={'artifacts':{},'operations':[]}
            with patch.object(reviews,'locked_state',return_value=contextlib.nullcontext(state)), \
                    patch.object(workflow,'ensure'),patch.object(reviews,'audit_bound') as audit, \
                    patch.object(reviews,'commit_stage') as commit:
                result=reviews.review_audit(NS(run=Path(directory),visual_review=path,generic_review=None))
            self.assertFalse(result['record_valid']);self.assertFalse(result['native_audit_started'])
            audit.assert_not_called();commit.assert_not_called()

    def test_review_template_requires_baseline_before_audit(self):
        with patch.object(reviews,'audit_bound') as audit,self.assertRaises(ValueError):
            reviews.review_shape(NS(run=Path('/synthetic'),baseline_available=None))
        audit.assert_not_called()

    def test_templates_leave_pixel_decisions_unreviewed(self):
        for available in ('yes','no'):
            with self.subTest(available=available),tempfile.TemporaryDirectory() as directory:
                root=Path(directory);image=root/'image.fixture';image.write_bytes(b'synthetic bytes; not a generated image')
                state={'phase':'test','artifacts':{}}
                contracts={'composed_audit':{'status':'pass'},'runtime_audit':{'status':'pass'},
                    'effective_visual':{'contract_version':'fixture/v1','obligations':[{'render_gates':[{'id':'relation','review_scale':'native'}]}]}}
                outputs={}
                def commit(run,state,phase,values):
                    outputs.update(values)
                    state['artifacts'].update({k:{'path':str(root/k)} for k in values})
                with patch.object(reviews,'locked_state',return_value=contextlib.nullcontext(state)), \
                        patch.object(workflow,'ensure'),patch.object(reviews,'audit_bound',return_value=contracts), \
                        patch.object(reviews,'value',return_value={'pack_id':'fixture'}),patch.object(reviews,'commit_stage',side_effect=commit):
                    reviews.review_shape(NS(run=root,image=image,baseline_available=available))
                shape=json.loads(outputs['visual_review_shape'])['review']
                self.assertEqual(shape['user_judgment']['genuinely_moe'],'pending')
                self.assertEqual(shape['user_judgment']['source'],'not_yet_received')
                self.assertEqual(shape['user_judgment']['better_than_baseline'],'pending' if available=='yes' else 'not_applicable')
                self.assertIsNone(shape['hard_gates']['relation']['status'])
                self.assertEqual(shape['hard_gates']['relation']['observability'],'unreviewed')

    def test_full_visual_auditor_enforces_coverage_and_baseline(self):
        with tempfile.TemporaryDirectory() as directory:
            image=Path(directory)/'image.fixture';image.write_bytes(b'synthetic hash fixture')
            contract={'contract_version':'fixture/v1','required_hard_gates':['relation'],'strict_gate_set':True}
            review={**self.review(),'schema_version':visual.REVIEW_SCHEMA_VERSION,'pack_id':'fixture',
                'contract_version':'fixture/v1','reviewer':'contract-test','result_image':str(image),
                'result_sha256':sha(image.read_bytes())}
            with patch.object(visual,'derive_character_response_render_gates',return_value=(None,[],[])), \
                    patch.object(visual.audit_composed_prompt.photo_embodiment,'render_gate_ids',return_value=([],[])), \
                    patch.object(visual.audit_composed_prompt,'derive_effective_visual_obligation_contract',return_value=(contract,[])):
                run=lambda r:visual.audit_moe_render_review({'pack_id':'fixture'},r,composed={})
                self.assertTrue(run(review)['technical_qualified'])
                partial=copy.deepcopy(review);partial['hard_gates']['relation']['observability']='partial'
                self.assertTrue(run(partial)['schema_failures'])
                partial['hard_gates']['relation']['status']='fail'
                self.assertFalse(run(partial)['schema_failures']);self.assertFalse(run(partial)['technical_qualified'])
                invalid=copy.deepcopy(review);invalid['user_judgment']['baseline_available']=None
                self.assertIn('user_judgment.baseline_available',[r['check'] for r in run(invalid)['schema_failures']])

    def test_full_generic_auditor_distinguishes_valid_failure_from_partial_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            image=Path(directory)/'image.fixture';image.write_bytes(b'synthetic hash fixture')
            contract={'canonical_sha256':'a'*64,'targets':[{'render_gates':[{'id':'relation','review_scale':'native'}]}]}
            review={'schema_version':generic.SCHEMA_VERSION,'pack_id':'fixture',
                'source_render_repair_contract_sha256':'a'*64,'result':{'path':str(image),'sha256':sha(image.read_bytes())},
                'reviewer':{'reviewer_id':'contract-test','method':'direct_pixel_inspection'},
                'gates':[{'gate_id':'relation',**self.row()}]}
            with patch.object(generic.audit_composed_prompt,'expected_render_repair_contract',return_value=contract):
                run=lambda r:generic.audit_image_render_review({'pack_id':'fixture','render_repair':contract},{'pack_id':'fixture'},r)
                self.assertTrue(run(review)['technical_qualified'])
                historical=copy.deepcopy(review);del historical['gates'][0]['observability']
                self.assertTrue(run(historical)['technical_qualified'])
                review['gates'][0]['observability']='partial'
                self.assertEqual(run(review)['status'],'fail')
                review['gates'][0]['status']='fail'
                self.assertEqual(run(review)['status'],'pass');self.assertFalse(run(review)['technical_qualified'])


if __name__ == '__main__':
    unittest.main()

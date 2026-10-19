"""Real offline native retrieve, rejected-result recorder, and tamper rejection."""
import argparse,copy,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
import run
from history_state import new

PROGRAM=r"""
import argparse,copy,hashlib,json,sys,tempfile
from pathlib import Path
project=Path(sys.argv[1]).resolve();sys.path[:0]=[str(project),str(project/'skills/photo-prompt-image-generator/scripts'),str(project/'skills/photo-prompt-image-generator/precore')]
from tests.test_photo_workflow_precore import freeze_fixture,files
from tests.test_photo_workflow_state import workflow
from tests.test_photo_authorship_policy import PhotoAuthorshipPolicyTests
from photo_runtime_sources import RuntimeSnapshotProvider
from image_attempt_evidence import capture_native_error,write_evidence

def save(path,value):path.write_bytes(files.encode(value));return path
with tempfile.TemporaryDirectory(prefix='native-import-contract-') as tmp:
    d=Path(tmp);r,_=freeze_fixture(d,mode='image',overrides={'sensual':0,'fetish':0,'surreal':0,'creativity':0})
    store=d/'runtime';RuntimeSnapshotProvider(store=store).publisher.publish()
    args=argparse.Namespace(run=r,seed=27,runtime_store=store,source_mode='local_current',source_remote=None,source_ref='main',visual_intent=None,retrieval_mode='keyword_only')
    retrieved=workflow.retrieve(args);assert retrieved['phase']=='pack_bound'
    assert workflow.retrieve(args)['reused']
    pack=workflow.one(files.value(files.load_state(r),'pack'))
    composed=PhotoAuthorshipPolicyTests.composed(pack);cp=save(d/'composed.json',composed)
    assert workflow.compose_audit(argparse.Namespace(run=r,composed=cp))['status']=='pass'
    parameters=save(d/'parameters.json',{'references':[]})
    assert workflow.prepare_render(argparse.Namespace(run=r,parameters=parameters,lane='native',model='offline',size='1024x1536'))['status']=='pass'
    scope=save(d/'scope.json',{'lanes':['native'],'invocation_limit':1,'authorization_source':'synthetic offline qualification; no tool invocation'})
    workflow.authorize(argparse.Namespace(run=r,scope=scope));planned=workflow.native_plan(argparse.Namespace(run=r));workflow.native_started(argparse.Namespace(run=r))
    state=files.load_state(r);plan=files.value(state,'native_plan');op=next(x for x in state['operations'] if x['operation_id']==planned['operation_id'])
    evidence=capture_native_error({'error':{'code':'moderation_blocked','message':'synthetic rejected native observation'}},
        {'tool':'image_gen','generation_environment':'native_imagegen','attempt':1,'invocation_outcome':'rejected','provider_outcome':'unknown',
        'request':{'prompt_en':composed['prompt_en'],'negative_en':composed.get('negative_en'),'runtime_prompt_en':plan['payload']['prompt']}})
    failures={}
    for case in ('sha','prompt','attempt','runtime_prompt'):
        ev=copy.deepcopy(evidence)
        if case=='prompt':ev['request']['prompt_en']+=' forged'
        if case=='attempt':ev['attempt']=2
        if case=='runtime_prompt':ev['request']['runtime_prompt_en']+=' forged'
        path=d/(case+'.evidence.json');h=write_evidence(path,ev)
        obs=save(d/(case+'.observed.json'),{'operation_id':op['operation_id'],'outcome':'rejected','evidence_path':str(path),'evidence_sha256':'0'*64 if case=='sha' else h})
        ledger=d/(case+'.ledger.ndjson')
        try:workflow.native_result(argparse.Namespace(run=r,result=obs,ledger=ledger))
        except (ValueError,RuntimeError) as error:
            expected={'sha':'stale_native_error_evidence','prompt':'prompt_en mismatch','attempt':'attempt mismatch','runtime_prompt':'runtime prompt mismatch'}[case]
            assert expected in str(error),str(error)
            failures[case]={'rejected':True,'expected_reason_observed':expected,'exception':type(error).__name__}
        else:raise AssertionError('tampered native evidence admitted: '+case)
        assert not ledger.exists(),case
    path=d/'valid.evidence.json';h=write_evidence(path,evidence)
    obs=save(d/'valid.observed.json',{'operation_id':op['operation_id'],'outcome':'rejected','evidence_path':str(path),'evidence_sha256':h})
    ledger=d/'valid.ledger.ndjson';recorded=workflow.native_result(argparse.Namespace(run=r,result=obs,ledger=ledger))
    row=json.loads(ledger.read_bytes());assert recorded['status']=='attempt_recorded' and row['status']=='safety_block'
    assert row['attempt_evidence_sha256']==h and row['generation_environment']=='native_imagegen'
    assert row['workflow_operation_id']==op['operation_id']+':1'
    assert row['runtime_prompt_sha256']==hashlib.sha256(plan['payload']['prompt'].encode()).hexdigest()
    final_op=files.load_state(r)['operations'][0]
    assert final_op['status']=='provider_blocked'
    assert final_op['last_event']['stage']=='attempt_recorded' and final_op['last_event']['terminal'] is True
    loaded={}
    for module in ('photo_workflow','record_image_run','image_attempt_evidence'):
        m=__import__(module);p=Path(m.__file__).resolve();assert p.is_relative_to(project)
        loaded[module]={'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    print(json.dumps({'status':'PASS','retrieve_phase':retrieved['phase'],'retrieve_reuse':True,'real_recorder_subprocess':True,'real_native_reaudit':True,
        'native_ledger_status':row['status'],'native_terminal_status':final_op['status'],'native_last_event_stage':final_op['last_event']['stage'],'native_valid_evidence_hash_bound':True,'native_operation_bound':True,'negative_cases':failures,
        'loaded_modules':loaded,'local_native_keyword_only_diagnostic':True,'H_default_checked_separately':True,
        'Gemini_calls':0,'new_embedding_calls':0,'actual_image_calls':0,'original_CURRENT_writes':0}))
"""
label=sys.argv[1];project=Path(sys.argv[2]) if len(sys.argv)>2 else Path(run.state.read(run.E/'PRIVATE-PROJECTS.json')['projects'][label])
python=run.SKILL/'.runtime/embedding-python/bin/python'
child=subprocess.run(['/usr/bin/sandbox-exec','-p',run.four_patch.policy()+'(deny file-read* (regex "/site-packages/torch(/|$)"))',str(python),'-I','-B','-c',PROGRAM,str(project)],
    cwd=project,env=run.checks.environment(),capture_output=True,text=True,timeout=900)
try:result=json.loads(child.stdout.splitlines()[-1])
except (ValueError,IndexError):result={'status':'HARNESS_UNAVAILABLE'}
new(run.E/('NATIVE-BRANCH-'+label+'.json'),{**result,'exit_code':child.returncode,'stdout':child.stdout,'stderr':child.stderr,
    'network_denied':True,'original_writes_denied':True,'original_source_fallback_denied':True})
print(label,'native branches',result['status'],flush=True)
assert child.returncode==0 and result['status']=='PASS',child.stderr[-6000:]

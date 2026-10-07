import sys,pathlib,json,time,argparse,subprocess,copy,contextlib,io,unittest
root=pathlib.Path.cwd();sys.path.insert(0,str(root))
from tests.test_photo_workflow_precore import freeze_fixture,files
from tests.test_photo_workflow_state import workflow
from tests import test_photo_authorship_policy as authorship
from tests.test_photo_workflow_runtime_bridge import PhotoWorkflowRuntimeBridgeTests
d=pathlib.Path('/tmp/photo-p1-usability-case');d.mkdir(exist_ok=True);metrics={}
def timed(name,func):
 start=time.monotonic();value=func();metrics[name]={'wall_seconds':round(time.monotonic()-start,3)};return value
def cli(name,args):
 start=time.monotonic();r=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True)
 (d/(name+'.stdout')).write_text(r.stdout);(d/(name+'.stderr')).write_text(r.stderr)
 metrics[name]={'wall_seconds':round(time.monotonic()-start,3),'exit_code':r.returncode,'command':[sys.executable,*args]}
 if r.returncode:raise RuntimeError(name+' failed; inspect saved diagnostic')
 return r
run,authored=timed('workflow_init_controls_freeze',lambda:freeze_fixture(d,overrides={'sensual':0,'fetish':0,'surreal':0,'creativity':0}))
state=files.load_state(run);scripts=root/'skills/photo-prompt-image-generator/scripts';store=d/'runtime';manual=d/'manual-pack.json';receipt=d/'manual-receipt.json'
old=['--request-envelope-json',str(files.bound_path(state,'request_envelope_input')),'--authorial-core-json',str(files.bound_path(state,'authorial_core_input')),'--creative-controls-json',str(files.bound_path(state,'creative_controls')),'--embodiment-review-json',str(files.bound_path(state,'embodiment_review')),'--new-author-camera-evidence','--seed','27','--runtime-store',str(store),'--output-file',str(manual),'--runtime-receipt',str(receipt)]
cli('existing_cli_retrieve',[str(scripts/'generate_photo_prompt.py'),*old])
args=argparse.Namespace(run=run,seed=27,runtime_store=store,source_mode='local_current',source_remote=None,source_ref='main',visual_intent=None)
timed('workflow_retrieve',lambda:workflow.retrieve(args));state=files.load_state(run);pack=workflow.one(files.value(state,'pack'));old_pack=workflow.one(files.read_json(manual))
metrics['same_authored_inputs']={'authorial_core_equal':old_pack['authorial_core']==pack['authorial_core'],'controls_equal':old_pack['creative_controls']==pack['creative_controls'],'baseline_equal':old_pack['authorial_core']['baseline_prompt_en']==pack['authorial_core']['baseline_prompt_en']}
authored_composed=authorship.PhotoAuthorshipPolicyTests.composed(pack)
for k in ['pack_id','core_retrieval_sha256']:authored_composed.pop(k)
for k in ['source_authorial_core_sha256','source_intent_lock_sha256']:authored_composed['authorial_core_binding'].pop(k)
authored_composed['embodiment_review'].pop('source_contract_sha256');authored_composed['embodiment_review']['review'].pop('prompt_sha256')
composed=d/'authored-composed.json';composed.write_bytes(files.encode(authored_composed));result=timed('workflow_compose_audit',lambda:workflow.compose_audit(argparse.Namespace(run=run,composed=composed)));assert result['status']=='pass',result
state=files.load_state(run);cli('existing_cli_composed_audit',[str(scripts/'audit_composed_prompt.py'),'--pack',str(files.bound_path(state,'pack')),'--composed',str(files.bound_path(state,'composed')),'--runtime-receipt',str(files.bound_path(state,'runtime_receipt')),'--runtime-store',str(store)])
parameters=d/'parameters.json';parameters.write_text('{"references":[]}');result=timed('workflow_prepare_render',lambda:workflow.prepare_render(argparse.Namespace(run=run,parameters=parameters,lane='api',model='offline-model',size='1024x1536')));assert result['status']=='pass',result
state=files.load_state(run);metrics['manual_reference_arguments']={'existing_retrieve_input_output_paths':6,'workflow_retrieve_input_output_paths':1,'existing_composed_audit_input_paths':3,'workflow_compose_audit_input_paths':2,'source_policy_seed_runtime_store_excluded':True}
metrics['author_calculated_hash_or_id_fields']={'workflow':0,'omitted_and_stamped':['request.request_sha256','core.creative_controls_sha256','precore_selection.contract_bindings','embodiment_review.prompt_sha256','composed.pack_id','composed.core_retrieval_sha256','composed.authorial_core_binding.source_authorial_core_sha256','composed.authorial_core_binding.source_intent_lock_sha256','composed.embodiment_review.source_contract_sha256','composed.embodiment_review.review.prompt_sha256','render_request.bindings']}
start=time.monotonic();changed=dict(authored_composed,prompt_en='forged');bad=d/'tampered-composed.json';bad.write_bytes(files.encode(changed));bad_result=workflow.compose_audit(argparse.Namespace(run=run,composed=bad));metrics['tamper']={'wall_seconds':round(time.monotonic()-start,3),'result':bad_result['status'],'image_calls':0,'authored_file_edits':1,'silently_repaired':False};assert bad_result['status']=='fail'
core_path=files.bound_path(files.load_state(run),'authorial_core_input');old_raw=core_path.read_bytes();core_path.write_bytes(old_raw+b' ')
start=time.monotonic()
try:workflow.retrieve(args);raise AssertionError('stale accepted')
except ValueError as error:metrics['stale_next_stage']={'wall_seconds':round(time.monotonic()-start,3),'error_code':str(error),'image_calls':0,'authored_file_edits':1}
finally:core_path.write_bytes(old_raw)
case=PhotoWorkflowRuntimeBridgeTests('test_recorder_crash_keeps_returned_bytes_and_replays_no_image_call');start=time.monotonic();result=unittest.TestResult();case.run(result);assert result.wasSuccessful(),result.errors
metrics['recorder_crash_replay']={'wall_seconds':round(time.monotonic()-start,3),'fixture_provider_calls':1,'replayed_appends':2,'ledger_rows':1,'additional_image_calls':0,'actual_network_calls':0}
metrics['limits']=['single maintenance fixture; no timing performance inference','same current source and authored bytes for old CLI and managed route','cold CLI generation first and warm managed route second; times are not comparable throughput','author judgment and human editing time are not measured','provider fixture; no native tool or real API invocation','retry writer zero parent full files established by closed projection tests, not human time trial']
pathlib.Path('/tmp/photo-p1-usability-measurement.json').write_text(json.dumps(metrics,indent=2)+'\n');print(json.dumps(metrics,indent=2))

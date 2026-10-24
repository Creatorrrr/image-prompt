"""Transport-only zero-call recovery through official immutable commit_stage.
Copies no sources across arms; caller supplies its own source and target.
"""
import gc;gc.disable()
import argparse,copy,json,sys,uuid
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--kernel',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--target',type=Path,required=True);p.add_argument('--sidecar',action='append',default=[]);p.add_argument('--reviewed-prompt-sha256',required=True);p.add_argument('--reference-role',required=True);a=p.parse_args()
sys.path.insert(0,str(a.kernel/'scripts'))
from photo_workflow_state import locked_state,commit_stage,bound_path,verify_freeze,digest
from prepare_retry_context import verify_child
from photo_h_f2_receipts import verify_bound
old=a.source.resolve();new=a.target.resolve();oldraw=(old/'workflow.json').read_bytes();source=json.loads(oldraw)
assert source['operations']==[],'Only zero-operation source runs are supported'
assert old!=new,'Distinct new managed run required'
assert digest(json.loads(bound_path(source,'composed').read_bytes())['prompt_en'].encode())==a.reviewed_prompt_sha256,'Source prompt differs from reviewed SHA'
omitted={'render_request','runtime_audit'};assert omitted<=set(source['artifacts'])
state=copy.deepcopy(source);state['run_id']=uuid.uuid4().hex;state['artifacts']={};state.pop('transport',None)
outputs={k:bound_path(source,k).read_bytes() for k in source['artifacts'] if k not in omitted}
with locked_state(new) as existing:
 assert existing is None,'Target already bound; never replace existing run'
 commit_stage(new,state,'composition_audited',outputs)
checks={};verify_freeze(state);checks['verify_freeze']='pass';verify_child(state);checks['verify_child']='pass';verify_bound(state);checks['verify_bound']='pass'
sidecars={}
for name in a.sidecar:
 assert Path(name).name==name and name not in {'workflow.json'},'Only exact run-local sidecar basenames'
 raw=(old/name).read_bytes()
 with (new/name).open('xb') as f:f.write(raw)
 sidecars[name]=digest(raw)
assert digest((old/'workflow.json').read_bytes())==digest(oldraw),'Source state changed during fork'
proof={'schema':'photo-transport-fork-proof/v1','source_run':str(old),'target_run':str(new),'source_workflow_sha256':digest(oldraw),'old_actual_image_call_count':0,'old_operations':[],'old_invalid_transport_preserved':{k:source['artifacts'][k] for k in omitted},'copied_artifacts':{k:{'source_sha256':source['artifacts'][k]['sha256'],'target_sha256':state['artifacts'][k]['sha256'],'target_path':state['artifacts'][k]['path']} for k in outputs},'copied_sidecars':sidecars,'source_binding_unchanged':state['source_binding']==source['source_binding'],'h_f2_binding_unchanged':state['h_f2_binding']==source['h_f2_binding'],'retrieval_seed_unchanged':state['retrieval_seed']==source['retrieval_seed'],'no_retrieval_or_resampling':True,'checks':checks,'exact_closed_reference_role':a.reference_role,'reviewed_prompt_sha256':a.reviewed_prompt_sha256,'root_review_reused_by_exact_prompt_and_testcase_bytes':True}
with (new/'transport-fork-proof.json').open('x') as f:json.dump(proof,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'pass','checks':checks,'artifact_count':len(outputs),'target':str(new),'proof':str(new/'transport-fork-proof.json')}))

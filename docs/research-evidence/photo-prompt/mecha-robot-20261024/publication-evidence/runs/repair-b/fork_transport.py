import gc;gc.disable()
import json,hashlib,copy,uuid,sys,shutil
from pathlib import Path
kernel=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed/generations/578fd501437e5f3e4927330cf8c1a7f319a1aafb05f7f8627d09f10b23ccb7a9')
sys.path.insert(0,str(kernel/'scripts'))
from photo_workflow_state import locked_state,commit_stage,bound_path,verify_freeze,digest
from prepare_retry_context import verify_child
from photo_h_f2_receipts import verify_bound
old=Path('/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-anchored-b');new=Path('/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-repair2-transport-b')
oldraw=(old/'workflow.json').read_bytes();source=json.loads(oldraw)
assert source['operations']==[] and source['render_scope'] is None
omitted={'render_request','runtime_audit'}
assert omitted <= set(source['artifacts'])
state=copy.deepcopy(source);state['run_id']=uuid.uuid4().hex;state['phase']='composition_audited';state['artifacts']={};state.pop('transport',None)
outputs={k:bound_path(source,k).read_bytes() for k in source['artifacts'] if k not in omitted}
with locked_state(new) as existing:
 assert existing is None,'target already bound'
 commit_stage(new,state,'composition_audited',outputs)
checks={}
verify_freeze(state);checks['verify_freeze']='pass'
verify_child(state);checks['verify_child']='pass'
verify_bound(state);checks['verify_bound']='pass'
copied={}
for f in ['baseline.original.txt','final.prompt.txt','immutable-pixel-testcase.json','exposure.json','material-source-reviews.json','full-source-review-input.json','composition-comparison.md','semantic-self-review.json','transport.parameters.json','authorization.scope.json','SKILL.snapshot.md','SKILL.snapshot.sha256']:
 raw=(old/f).read_bytes();(new/f).write_bytes(raw);copied[f]=digest(raw)
assert digest((old/'workflow.json').read_bytes())==digest(oldraw),'old run changed during fork'
proof={'schema':'photo-transport-fork-proof/v1','source_run':str(old),'target_run':str(new),'source_workflow_sha256':digest(oldraw),'old_actual_image_call_count':0,'old_operations':[],'old_invalid_transport_preserved':{k:source['artifacts'][k] for k in omitted},'copied_artifacts':{k:{'source_sha256':source['artifacts'][k]['sha256'],'target_sha256':state['artifacts'][k]['sha256'],'target_path':state['artifacts'][k]['path']} for k in outputs},'copied_sidecars':copied,'source_binding_unchanged':state['source_binding']==source['source_binding'],'h_f2_binding_unchanged':state['h_f2_binding']==source['h_f2_binding'],'retrieval_seed_unchanged':state['retrieval_seed']==source['retrieval_seed'],'no_retrieval_or_resampling':True,'checks':checks,'exact_closed_reference_role':'visible facial and hair appearance reference; fictional scene and clothing are open','reviewed_prompt_sha256':'164f0a7e7d417eebfa36262b382a46ba2862957eaf55373bb002338e70be2b9b','root_review_reused_by_exact_prompt_and_testcase_bytes':True}
with (new/'transport-fork-proof.json').open('x') as f:json.dump(proof,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({'status':'pass','checks':checks,'artifact_count':len(outputs),'target':str(new),'proof':str(new/'transport-fork-proof.json')}))

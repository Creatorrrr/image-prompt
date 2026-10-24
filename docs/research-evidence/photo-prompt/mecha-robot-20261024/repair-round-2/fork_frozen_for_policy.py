"""Preserve exact independently frozen meaning across an authorized policy fix.

No authoring, source choice or new freeze is manufactured here. The maintained
freeze validator verifies copied bytes and slot intent binding independently.
Pre-fix material and every decision remain in their original runs.
"""
from pathlib import Path
import gc,json,sys,uuid
gc.disable()
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'skills/photo-prompt-image-generator/scripts'))
from photo_workflow_state import load_state,verify_freeze,bound_path,value,locked_state,commit_stage
roles=['request_raw','request_envelope_input','authoring_shapes','creative_controls','retry_proof','retry_context','authorial_core_input','authorial_core_normalized','request_envelope_normalized','embodiment_review','feature_selection','catalog','baseline','freeze_author_input_hashes','freeze_receipt','slot_intent_material','slot_expression_plan']
out=[]
for arm in 'abc':
 source=R/'generated/photo-runs'/('mecha-20261024-repair2-scoped-'+arm)
 target=R/'generated/photo-runs'/('mecha-20261024-repair2-anchored-'+arm)
 old=load_state(source);verify_freeze(old)
 assert not old['operations'],'Pre-fix run already reserved or invoked an image.'
 material=value(old,'h_f2_material');assert material['sampling_policy']['schema']=='photo-h-f2-sampling/v1'
 required_roles=list(dict.fromkeys(roles+list(value(old,'freeze_receipt')['files'])))
 payload={role:bound_path(old,role).read_bytes() for role in required_roles}
 origin={'user_request_sha256':old['artifacts']['request_raw']['sha256'],'pre_fix_run':str(source),'pre_fix_material':old['artifacts']['h_f2_material'],'pre_fix_sampling_policy':material['sampling_policy'],'pre_fix_sampling_seed':material['sampling_seed'],'reason':'Explicit user-authorized confirmed non-exposure policy repair; exact frozen core and authored slot plan preserved; no pre-fix images.'}
 with locked_state(target) as existing:
  if existing is not None:
   assert not existing['operations'] and not existing['source_binding'] and 'pack' not in existing['artifacts']
   assert existing['policy_repair_origin']==origin
   assert all(row['sha256']==old['artifacts'][r]['sha256'] for r,row in existing['artifacts'].items())
   state=existing;payload={r:raw for r,raw in payload.items() if r not in state['artifacts']}
  else:
   state={'schema_version':old['schema_version'],'run_id':uuid.uuid4().hex,'mode':old['mode'],'phase':'slot_intents_authored','artifacts':{},'source_binding':None,'render_scope':None,'operations':[]}
  if payload:commit_stage(target,state,'slot_intents_authored',payload,metadata={'slot_intent_binding':old['slot_intent_binding'],'policy_repair_origin':origin})
  verify_freeze(state)
  assert all(state['artifacts'][r]['sha256']==old['artifacts'][r]['sha256'] for r in required_roles)
 out.append({'arm':arm,'source':str(source),'target':str(target),'status':'pass','exact_copied_roles':required_roles,'baseline_sha256':state['artifacts']['baseline']['sha256'],'core_sha256':value(state,'authorial_core_normalized')['canonical_sha256'],'image_calls_before_fork':0,'query_seed_comparison':'Fresh one-pass draw under changed policy; paired policy replay uses original issued seeds separately.'})
(O/'policy-fix/forks.json').write_text(json.dumps({'status':'pass','rows':out},indent=2)+'\n')
print(json.dumps(out),flush=True)

#!/usr/bin/env python3
"""Record one observed native result through the shared recorder and managed journal, with independent arm provenance. Never invokes an image tool."""
import json, sys
from pathlib import Path
SKILL=Path('/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator')
sys.path.insert(0,str(SKILL/'scripts'))
from photo_workflow import load_state, value, bound_path, update_operation
from generate_images_via_api import record
arm=Path(__file__).resolve().parent
run=arm/'run'
state=load_state(run)
plan=value(state,'native_plan')
op=next(o for o in state['operations'] if o['operation_id']==plan['operation_id'])
observed=json.loads((arm/'native_observation.json').read_bytes())
assert op['status'] in {'invocation_started','record_ready','recorder_failed'}
assert observed['operation_id']==op['operation_id']
composed=value(state,'composed')
pack=value(state,'pack')
pack=pack[0] if isinstance(pack,list) else pack
flags=['--ts',op['timestamp'],'--prompt-en',composed['prompt_en'],'--attempt','1','--workflow-operation-id',op['operation_id']+':1','--tool','image_gen','--generation-environment','native_imagegen','--pack-id',pack['pack_id'],'--authorial-core-sha256',pack['authorial_core']['canonical_sha256'],'--intent-lock-sha256',pack['authorial_core']['intent_lock']['canonical_sha256'],'--image-call-count','1','--chosen-candidate-ids-json',json.dumps(composed['chosen_candidate_ids']),'--chosen-visual-concept-ids-json',json.dumps(composed['chosen_visual_concept_ids']),'--composer','agent','--audit-status','pass','--ledger',str(arm/'image_runs.ndjson'),'--native-render-plan-json',str(bound_path(state,'native_plan')),'--native-render-plan-sha256',state['artifacts']['native_plan']['sha256'],'--arm-id','b','--worktree-id','independent-arm-b:shared-checkout-isolated-artifacts','--skill-sha256','9e9b87e6f0b2c1ec1c36bd8e9d55f90950d53529a0b873722b546924dfc7043b','--source-ref','photo-source-generation:'+state['source_binding']['generation_id'],'--candidate-pack-version','v6','--independent-no-cross-arm-inputs','--manifest',str(arm/'run_manifest.json')]
if composed.get('negative_en') is not None: flags+=['--negative-en',composed['negative_en']]
for ref in plan['references']: flags+=['--reference-sha256',ref['sha256']]
if composed.get('chosen_visual_concept_ids'):
 flags+=['--effective-visual-contract-sha256',value(state,'composed_audit')['effective_visual_contract_sha256']]
if observed['outcome']=='returned':
 image=Path(observed['image_path']).resolve()
 assert image.is_file()
 flags+=['--status','success','--image-path',str(image)]
 image_arg=str(image)
 terminal_outcome="returned"
 provider_outcome="returned"
else:
 from photo_run_files import digest
 evidence=json.loads(Path(observed['evidence_path']).read_bytes())
 assert digest(Path(observed['evidence_path']).read_bytes())==observed['evidence_sha256']
 flags+=['--status',evidence['outcome']['status'],'--failure-reason',evidence['outcome']['display_message'],'--attempt-evidence-json',observed['evidence_path'],'--attempt-evidence-sha256',observed['evidence_sha256']]
 image_arg=None
 terminal_outcome="safety_block" if evidence["outcome"]["status"]=="safety_block" else "error"
 provider_outcome="returned" if terminal_outcome=="safety_block" else evidence.get("provider_outcome","unknown")
update_operation(run,op['operation_id'],{'stage':'record_ready','ledger_args':flags,'image_path':image_arg})
try: recorded=record(flags)
except RuntimeError:
 update_operation(run,op['operation_id'],{'stage':'recorder_failed','ledger_args':flags})
 raise
update_operation(run,op['operation_id'],{'stage':'attempt_recorded','ledger_run_id':recorded['run_id'],'terminal':True,'outcome':terminal_outcome,'provider_outcome':provider_outcome})
print(json.dumps({'status':'attempt_recorded','ledger_run_id':recorded['run_id'],'manifest':str(arm/'run_manifest.json'),'image_call_count':1}))

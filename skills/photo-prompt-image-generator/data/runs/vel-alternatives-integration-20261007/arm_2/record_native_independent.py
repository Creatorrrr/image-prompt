"""Arm-local manual native recording using the skill's audited recorder and journal."""
import argparse, pathlib, json, sys, hashlib, subprocess
ROOT=pathlib.Path('/Users/chasoik/.codex/worktrees/vel-appearance-integration/image-prompt')
ARM=ROOT/'skills/photo-prompt-image-generator/data/runs/vel-alternatives-integration-20261007/arm_2'
sys.path.insert(0,str(ROOT/'skills/photo-prompt-image-generator/scripts'))
from photo_workflow import update_operation, bound_path, value
parser=argparse.ArgumentParser(); parser.add_argument('--image-path'); parser.add_argument('--evidence-path'); args=parser.parse_args()
state=json.loads((ARM/'workflow.json').read_text()); plan=value(state,'native_plan'); composed=value(state,'composed'); raw=value(state,'pack'); pack=raw[0] if isinstance(raw,list) else raw
operation=next(op for op in state['operations'] if op['operation_id']==plan['operation_id'])
assert operation['status'] in {'invocation_started','record_ready','recorder_failed'}
assert len(operation['attempts'])==1
flags=['--ts',operation['timestamp'],'--prompt-en',composed['prompt_en'],'--attempt','1','--workflow-operation-id',operation['operation_id']+':1','--tool','image_gen','--generation-environment','native_imagegen','--pack-id',pack['pack_id'],'--authorial-core-sha256',pack['authorial_core']['canonical_sha256'],'--intent-lock-sha256',pack['authorial_core']['intent_lock']['canonical_sha256'],'--image-call-count','1','--chosen-candidate-ids-json',json.dumps(composed['chosen_candidate_ids']),'--chosen-visual-concept-ids-json',json.dumps(composed['chosen_visual_concept_ids']),'--composer','agent','--audit-status','pass','--ledger',str(ARM/'image_runs.ndjson'),'--native-render-plan-json',str(bound_path(state,'native_plan')),'--native-render-plan-sha256',state['artifacts']['native_plan']['sha256']]
if composed.get('negative_en') is not None: flags+=['--negative-en',composed['negative_en']]
for ref in plan['references']: flags+=['--reference-sha256',ref['sha256']]
assert not composed['chosen_visual_concept_ids'] and not pack.get('render_repair')
skill=ROOT/'skills/photo-prompt-image-generator/SKILL.md'; skill_bytes=skill.read_bytes(); (ARM/'skill_snapshot.md').write_bytes(skill_bytes)
flags+=['--arm-id','arm_2','--worktree-id',str(ROOT),'--skill-sha256',hashlib.sha256(skill_bytes).hexdigest(),'--source-ref','runtime-generation:'+state['source_binding']['generation_id']+';source-fingerprint:'+state['source_binding']['source_fingerprint'],'--candidate-pack-version','v6','--independent-no-cross-arm-inputs','--manifest',str(ARM/'run_manifest.json')]
image_path=None
if args.image_path:
 assert not args.evidence_path
 image_path=pathlib.Path(args.image_path).resolve(); assert image_path.is_relative_to(ARM.resolve()) and image_path.is_file()
 flags+=['--status','success','--image-path',str(image_path)]; outcome='returned'
elif args.evidence_path:
 evidence_path=pathlib.Path(args.evidence_path).resolve(); assert evidence_path.is_relative_to(ARM.resolve())
 evidence=json.loads(evidence_path.read_text()); flags+=['--status',evidence['outcome']['status'],'--attempt-evidence-json',str(evidence_path),'--attempt-evidence-sha256',hashlib.sha256(evidence_path.read_bytes()).hexdigest()]; outcome='safety_block' if evidence['outcome']['status']=='safety_block' else 'error'
else:raise ValueError('An actual image path or captured evidence path is required')
(ARM/'recorder_invocation.json').write_text(json.dumps({'python':sys.executable,'script':str(ROOT/'skills/photo-prompt-image-generator/scripts/record_image_run.py'),'arguments':flags,'boundary':'Existing recorder freshly audits the exact saved native plan and original pack, receipt, composition and runtime inputs. No source code was changed.'},ensure_ascii=False,indent=2)+'\n')
update_operation(ARM,operation['operation_id'],{'stage':'record_ready','ledger_args':flags,'image_path':str(image_path) if image_path else None})
child=subprocess.run([sys.executable,str(ROOT/'skills/photo-prompt-image-generator/scripts/record_image_run.py'),*flags],cwd=ROOT,capture_output=True,text=True)
(ARM/'recorder_stdout.json').write_text(child.stdout); (ARM/'recorder_stderr.txt').write_text(child.stderr)
if child.returncode:
 update_operation(ARM,operation['operation_id'],{'stage':'recorder_failed','ledger_args':flags}); print(child.stderr); raise SystemExit(child.returncode)
recorded=json.loads(child.stdout)
update_operation(ARM,operation['operation_id'],{'stage':'attempt_recorded','ledger_run_id':recorded['run_id'],'terminal':True,'outcome':outcome,'provider_outcome':'returned' if image_path else evidence.get('provider_outcome','returned')})
print(json.dumps({'status':'attempt_recorded','ledger_run_id':recorded['run_id'],'manifest':str(ARM/'run_manifest.json'),'image_call_count':1},ensure_ascii=False,indent=2))

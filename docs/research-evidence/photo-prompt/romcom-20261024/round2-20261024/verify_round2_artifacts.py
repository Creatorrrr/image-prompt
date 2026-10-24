"""File/binding evidence only. Pixel judgments are separately authored after direct inspection."""
from pathlib import Path
import json,hashlib,sys,re
R=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def one(x):return x[0] if isinstance(x,list) and len(x)==1 else x

def main():
 frozen={r['arm']:r for r in read(O/'frozen-inputs.json')['arms']};new=set(read(R/'skills/photo-prompt-image-generator/assets/photo_candidate_romcom_20261024.json')['candidates']);report={'status':'pass','scope':'Saved artifacts, ledger and exact bindings; not independent tool attestation or semantic/pixel approval.','arms':[]}
 arms=sys.argv[1] if len(sys.argv)>1 else 'abc'
 assert arms and set(arms)<=set('abc')
 for a in arms:
  root=R/'generated/photo-runs'/f'romcom-20261024-r2-{a}';run=root/'compatible-run';state=read(run/'workflow.json')
  for name,row in state['artifacts'].items():assert sha(run/row['path'])==row['sha256'],(a,name,'artifact changed')
  for name,value in frozen[a]['bindings'].items():assert state['artifacts'][name]['sha256']==value,(a,name,'frozen binding changed')
  value=lambda k:one(read(run/state['artifacts'][k]['path']))
  core=value('authorial_core_normalized');composed=value('composed');runtime=value('render_request');plan=value('native_plan');material=value('h_f2_material');receipt=value('runtime_receipt')
  assert state['h_f2_binding']['generation_id']==read(O/'merged-successor.json')['generation_id']==material['generation_id']
  assert receipt['generation_id']==read(O/'merged-successor.json')['native_generation_id']
  assert plan['payload']['prompt']==runtime['runtime_prompt_en']
  for role in ('pack','runtime_receipt','composed','render_request'):assert plan['inputs'][role]['sha256']==state['artifacts'][role]['sha256']
  refs=plan['payload'].get('referenced_image_paths',[]);assert refs==['/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'];assert sha(Path(refs[0]))=='06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
  rows={}
  ledger_paths=list(root.rglob('*.ndjson'))+[R/'generated/photo-runs/image_runs.ndjson']
  for file in ledger_paths:
   if not file.exists():continue
   for line in file.read_text().splitlines():
    if not line.strip():continue
    row=json.loads(line)
    if row.get('pack_id')==composed['pack_id'] and row.get('image_call_count',0)>0:rows[row['run_id']]=row
  assert len(rows)==1,(a,'exactly one recorded child render result required',list(rows));ledger=next(iter(rows.values()));assert ledger['status']=='success'
  attempts=[attempt for operation in state['operations'] for attempt in operation['attempts']]
  assert len(attempts)==1,(a,'one actual child attempt required',len(attempts))
  parent_rows=[json.loads(line) for line in (R/'generated/photo-runs'/f'romcom-20261024-{a}'/'image_runs.ndjson').read_text().splitlines() if line.strip()]
  parent_count=max(row['image_call_count'] for row in parent_rows)
  assert parent_count==1 and ledger['image_call_count']==parent_count+len(attempts),(a,'cumulative arm call count',ledger['image_call_count'])
  assert ledger['prompt_en']==composed['prompt_en'] and ledger['runtime_prompt_sha256']==hashlib.sha256(runtime['runtime_prompt_en'].encode()).hexdigest()
  assert ledger['cross_arm_inputs_used'] is False and ledger['authorial_core_sha256']==core['canonical_sha256'] and ledger['intent_lock_sha256']==core['intent_lock']['canonical_sha256']
  assert ledger['chosen_candidate_ids']==composed['chosen_candidate_ids'] and ledger['chosen_visual_concept_ids']==composed['chosen_visual_concept_ids']
  assert len(ledger['image_paths'])==1
  im=Path(ledger['image_paths'][0]);im=im if im.is_absolute() else R/im;assert im.is_file();image_sha=sha(im)
  assert any(row['sha256']==image_sha for row in ledger['image_hashes'])
  review=value('review_audit')
  assert review['generic']['status']=='pass' and not review['generic']['failures']
  assert not review['visual']['schema_failures']
  assert review['generic']['reviewed_result_sha256']==image_sha
  assert review['visual']['user_judgment']['source']=='not_yet_received'
  pixel=read(O/f'root-pixel-review-{a}.json');assert pixel['image_sha256']==image_sha
  argument_files=list(root.rglob('native-tool-arguments.json'))+list(root.rglob('native-args.json'))+list(root.rglob('native-tool-args.json'))
  matching_arguments=[p for p in argument_files if read(p)==plan['payload']]
  assert matching_arguments,(a,'saved actual tool arguments must equal audited payload')
  matching_returns=[]
  for p in root.rglob('native-tool-result.json'):
   result=read(p);match=re.search(r' as (/Users/[^\n]+\.png) by default\.',result.get('output_hint',''))
   if match and Path(match.group(1)).is_file() and sha(Path(match.group(1)))==image_sha:matching_returns.append((p,match.group(1)))
  assert matching_returns,(a,'explicit tool-return path must match saved image')
  exact=root/'runtime-prompt-exact.txt';exact.write_text(runtime['runtime_prompt_en'])
  decisions=composed['h_f2_material_decisions'];retained={r['candidate_id'] for r in decisions if r['use']=='inspiration_only'}
  report['arms'].append({'arm':a,'run':str(run),'image':str(im),'image_sha256':image_sha,'core_sha256':core['canonical_sha256'],'intent_lock_sha256':core['intent_lock']['canonical_sha256'],'runtime_prompt_sha256':sha(exact),'exact_prompt_file':str(exact),'actual_tool_arguments_file':str(matching_arguments[0]),'actual_tool_arguments_equal_plan':True,'tool_return_file':str(matching_returns[0][0]),'original_returned_image':matching_returns[0][1],'original_and_copy_sha256_equal':True,'ledger_run_id':ledger['run_id'],'current_round_image_calls':len(attempts),'parent_image_call_count':parent_count,'cumulative_arm_image_call_count':ledger['image_call_count'],'new_material_exposed':len(set(material['sources'])&new),'new_retained_inspiration':sorted(retained&new),'all_retained_inspiration':sorted(retained),'native_selection_count':len(composed['chosen_candidate_ids']),'reference_sha256':sha(Path(refs[0])),'cross_arm_inputs_used':False,'managed_review_record_valid':True,'managed_generic_technical_qualified':review['generic']['technical_qualified'],'managed_body_technical_qualified':review['visual']['technical_qualified'],'strict_scenario_status_root':pixel['original_scenario_status'],'selected_general_guidance_status_root':pixel['selected_guidance_status'],'user_acceptance':'pending'})
 name='arm-artifact-verification.json' if arms=='abc' else f'arm-artifact-verification-{arms}.json'
 (O/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

from pathlib import Path
import json,hashlib,shutil,datetime
from PIL import Image
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';O=R/'docs/research-evidence/photo-prompt/campus-fiction-20261024/query-core-retest-20261024';ref=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg');refsha=hashlib.sha256(ref.read_bytes()).hexdigest();results=[]
for arm,filename in [('a','image.png'),('b2','image.png'),('c','actual1.png')]:
 run=R/f'generated/photo-runs/campus-query-core-20261024-{arm}';state=json.loads((run/'workflow.json').read_text());read=lambda k:json.loads(Path(state['artifacts'][k]['path']).read_text());composed=read('composed');render=read('render_request');review=read('review_audit');op=state['operations'][0];ledger=[json.loads(v) for v in (run/'image_runs.ndjson').read_text().splitlines() if v.strip()];row=ledger[0];p=run/filename;sha=hashlib.sha256(p.read_bytes()).hexdigest()
 assert state['phase']=='review_record_validated' and len(state['operations'])==1 and op['status']=='complete'
 assert len(op['attempts'])==len(ledger)==row['image_call_count']==1
 assert row['cross_arm_inputs_used'] is False and row['reference_sha256']==[refsha]
 assert row['skill_sha256']=='8c82b646c7c13c909696342dc799547a4d38c52ce22a9bd429321d28f678d6bb'
 assert row['prompt_en']==composed['prompt_en']==render['runtime_prompt_en']
 assert render['referenced_image_paths']==[str(ref)] and render['references'][0]['sha256']==refsha
 assert op['result_binding']['sha256']==sha and Path(op['result_binding']['path'])==p
 assert not row['chosen_candidate_ids'] and not review['visual']['schema_failures']
 dest=O/'arms'/arm;dest.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest/'image.png');assert hashlib.sha256((dest/'image.png').read_bytes()).hexdigest()==sha
 (dest/'prompt.txt').write_bytes(composed['prompt_en'].encode());shutil.copyfile(run/'candidate-transmission.json',dest/'candidate-transmission.json');shutil.copyfile(state['artifacts']['review_audit']['path'],dest/'managed-review-audit.json')
 with Image.open(p) as img:size=list(img.size)
 results.append({'arm':arm,'run':str(run),'review_record_valid':True,'technical_qualification':state['technical_qualification'],'strict_new_source_pixel_pass':False,'new_source_prompt_contributions':0 if arm=='c' else 1,'partial_new_source_pixel_transmission':arm!='c','image_calls':1,'ledger_rows':len(ledger),'run_id':row['run_id'],'image_sha256':sha,'dimensions':size,'prompt_sha256':hashlib.sha256(composed['prompt_en'].encode()).hexdigest(),'reference_sha256':refsha,'observed_model':None,'user_judgment':'pending','image_deliverable':str(dest/'image.png'),'prompt_deliverable':str(dest/'prompt.txt')})
(O/'FINAL-VALIDATION.json').write_text(json.dumps({'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'focused_tests':json.loads((O/'FOCUSED-TESTS.json').read_text()),'arms':results,'image_calls_total':sum(r['image_calls'] for r in results),'new_source_prompt_transmissions':2,'partial_new_source_pixel_transmissions':2,'strict_new_source_pixel_passes':0,'native_whole_source_qualification_claimed':False},indent=2))
p=O/'PARENT-PIXEL-REVIEW.json';j=json.loads(p.read_text());b=next(a for a in j['arms'] if a['arm']=='b2');b['preauthored_gate_reconciliation']={'complete_bed_shapes':'partial','count_observation':'Two beds remain countable; the preauthored gate additionally requires complete shapes, and the doorframe/crop hides boundaries. No gate was relaxed.','storage_relation':'partial','strict_outcome':'fail'};p.write_text(json.dumps(j,ensure_ascii=False,indent=2))
print(json.dumps({'images':len(results),'actual_calls':3,'valid_review_records':3,'technical':[r['technical_qualification'] for r in results],'new_prompt_transmission':2,'partial_new_pixel_transmission':2,'strict_new_pixel_pass':0},indent=2))

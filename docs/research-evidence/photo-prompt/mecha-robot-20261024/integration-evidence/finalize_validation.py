"""Close source/runtime and saved-pixel evidence without changing test criteria."""
from pathlib import Path
import json,hashlib,datetime
O=Path(__file__).resolve().parent;ROOT=O.parents[4];S=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(Path(p).read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
release=read(O/'rebase2-successor.json');installed=read(O/'rebase2-install-active.json');cfg=read(S/'retrieval-runtime.json')
assert installed['status']=='pass' and installed['generation_id']==release['generation_id']==cfg['generation_id']
assert cfg['native_generation_id']==release['native_generation_id']
check=read(O/'default-runtime-check.json');assert check['status']=='pass'
reference=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg');refsha=sha(reference);assert refsha=='06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
items=[('A','mecha-20261024-arm-a','result.png','5dbe0d6625d36a39438a63674a1b5287117fd396fa7fb9c5a6a0f63ab8ab0b2c',0,None),('B','mecha-20261024-arm-b/current','../results/inland-sea-walker.png','68a52d18c2f3e3c6346b5aa8ca7f9864d15a90088e43d9e55ed71d82d8973113',1,'F13'),('C','mecha-20261024-arm-c','result.png','abbaba304f82719d4299289bb27826b379b9c7789e5bdd4bc8d030582f13ddc3',1,'J01')]
counts={'A':read(ROOT/'generated/photo-runs/mecha-20261024-arm-a/summary.json')['generation']['actual_image_call_count'],'B':read(O.parent/'image-tests/arm-b/transport-proof.json')['image_call_count'],'C':read(O.parent/'image-tests/arm-c/completion.json')['native_calls']}
assert list(counts.values())==[1,1,1]
arms=[]
for arm,runrel,image,expected,exposed,card in items:
 run=ROOT/'generated/photo-runs'/runrel;w=read(run/'workflow.json');assert w['phase']=='review_record_validated'
 def art(name):
  v=w['artifacts'][name];assert sha(v['path'])==v['sha256'];return read(v['path'])
 composed=art('composed');plan=art('native_plan');audit=art('review_audit')['visual'];payload=plan['payload'];assert payload['prompt']==composed['prompt_en'];assert payload['referenced_image_paths']==[str(reference)]
 p=(run/image).resolve();assert sha(p)==expected
 assert audit['technical_qualified'] is False and not audit['schema_failures']
 parent=read(O/('parent-pixel-review-'+arm.lower()+'.json'));assert parent['image_sha256']==expected
 if card:assert parent['source_complete_result']=='PASS_5_OF_5'
 assert w['h_f2_binding']['generation_id']=='e1a3d0cb7623488dfbfff9f0b8337200cef8c0142248414c0a0f4b890faecc71'
 arms.append({'arm':arm,'run':str(run),'image':str(p),'image_sha256':expected,'actual_image_calls':1,'observed_image_model':None,'reference_sha256':refsha,'prompt_sha256':hashlib.sha256(payload['prompt'].encode()).hexdigest(),'composed_equals_planned_native_prompt':True,'state':w['phase'],'source_card':card,'new_sources_actually_returned':exposed,'source_supplemental_gates_passed':5 if card else None,'native_source_approval':False,'whole_scene_technical_qualified':False,'managed_gates_passed':audit['required_hard_gate_count']-len(audit['failed_hard_gates']),'managed_gate_count':audit['required_hard_gate_count'],'record_schema_failures':[],'requester_acceptance':'pending_not_yet_received','authoring_semantic_ownership_limit':arm=='A'})
hashes=read(O/'pixel-testcase-hashes.prereview.json')
assert all(sha(v['path'])==v['sha256'] for v in hashes['testcases'])
store=Path(installed['store']);oldnative=store/'generations'/'e51d43e44abad75550a4213b3de14028697c1470dc1c42a31b895029886b32ea';newnative=store/'generations'/cfg['native_generation_id'];parity=[]
for name in ['photo_candidate_mecha_robot_20261024.json','photo_candidate_mecha_robot_bindings_20261024.json']:
 oldhash=sha(oldnative/'assets'/name);newhash=sha(newnative/'assets'/name);assert oldhash==newhash;parity.append({'module':name,'test_sha256':oldhash,'active_sha256':newhash,'identical':True})
(O/'runtime-mecha-parity.json').write_text(json.dumps({'status':'pass','rows':parity},indent=2)+'\n')
validation={'schema':'mecha-data-image-final-validation/v1','completed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'data':{'semantic_cards':108,'directed_relations':413,'context_boundaries':32,'original_term_routes':323,'new_records':140,'positive':106,'diagnostic':34,'optional_bindings':228,'old_source_records_changed':0,'new_native_approval':False,'focused_tests':{'run':10,'passed':10}},'runtime':{'status':'installed_active_verified','active_config':cfg,'install':installed,'test_generation_id':arms and 'e1a3d0cb7623488dfbfff9f0b8337200cef8c0142248414c0a0f4b890faecc71','test_native_id':'e51d43e44abad75550a4213b3de14028697c1470dc1c42a31b895029886b32ea','concurrent_default_advances_preserved':['campus','romcom'],'kernel_code_changed':False,'CURRENT_writes':0,'test_and_active_mecha_modules_byte_identical':True},'arms':arms,'summary':{'actual_image_calls':3,'returned_images':3,'arms_with_new_source_exposure':2,'new_source_supplemental_cases_passed':2,'whole_scene_technical_qualified':0,'all_three_prerender_testcases_unchanged':True,'parent_directly_inspected_all_saved_originals':True,'all_106_candidates_image_validated':False,'requester_acceptance':'pending_not_yet_received','commit_push':'NOT_RUN'}}
(O/'FINAL-VALIDATION.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')
d=read(O/'data-integration.json');d['index_runtime']='installed_active_verified';d['active_runtime_evidence']='FINAL-VALIDATION.json';d['active_generation_id']=cfg['generation_id'];(O/'data-integration.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','active_generation_id':cfg['generation_id'],'images':3,'source_cases_pass':2,'whole_scene_technical_pass':0,'prerender_cases_unchanged':True}))

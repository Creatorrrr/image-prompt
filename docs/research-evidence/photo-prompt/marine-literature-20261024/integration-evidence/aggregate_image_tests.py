from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parent;Q=O.parent;R=O.parents[4]
read=lambda p:json.loads(Path(p).read_bytes())
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
pix=read(O/'root-pixel-review.json');reports={'a':read(Q/'image-tests/a/arm-report.json'),'b':read(Q/'image-tests/b/summary.json'),'c':read(Q/'image-tests/c/arm-summary.json')}
new=set(read(O/'new-visual-cids.json'));expected='3643bb6b2a4143f1a2f3ccccfacb63c5d98808319dac5753849304127f17e166';skill='f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089';rows=[]
for image in pix['cases']:
 a=image['arm'];d=reports[a];run=R/('generated/photo-runs/marine-literature-20261024-'+a);w=read(run/'workflow.json')
 assert w['phase']=='review_record_validated' and w['technical_qualification']=='fail'
 assert len(w['operations'])==1 and w['operations'][0]['status']=='complete'
 assert w['h_f2_binding']['generation_id']==expected
 assert w['artifacts']['request_raw']['sha256']==sha(Q/'image-tests/request.txt')
 m=read(w['artifacts']['h_f2_material']['path']);seen=set(m['sources']);exposed=sorted(new&seen)
 if a=='a':prompt=d['prompt']['final_path'];prompt_hash=d['prompt']['runtime_prompt_sha256'];calls=d['generation']['actual_tool_invocations'];ss=d['frozen_skill_sha256'];model=d['generation']['observed_image_model'];used=d['retrieval']['new_retained_ids']
 elif a=='b':prompt=str(Q/'image-tests/b/prompt.runtime.exact.txt');prompt_hash=d['prompt_sha256'];calls=d['actual_image_tool_calls'];ss=skill;model=d['observed_image_model'];used=d['new_used_cids']
 else:prompt=d['prompt_path'];prompt_hash=d['runtime_prompt_sha256'];calls=d['generation']['actual_image_tool_calls'];ss=d['skill_sha256'];model=d['generation']['observed_image_model'];used=[]
 assert ss==skill and calls==1 and not used
 file_hash=sha(prompt)
 assert file_hash==prompt_hash,'Prompt export differs from executed runtime string; do not trim silently.'
 rows.append({'arm':a,'run':str(run),'skill_sha256':ss,'H_F2_generation':expected,'native_generation':'7907fa1dcf32e7a0915a7f1a2833408f3bef41f62ee2371cdafbf44657ac0e74','queries':len(m['goals']),'returned_occurrences':sum(len(x['candidates']) for x in m['goals'].values()),'returned_unique_sources':len(seen),'new_exposed_CIDs':exposed,'new_used_CIDs':used,'actual_image_calls':calls,'observed_image_model':model,'prompt':prompt,'prompt_sha256':file_hash,'image':image['image'],'image_sha256':image['sha256'],'actual_dimensions':[image['width'],image['height']],'phase':w['phase'],'technical_qualification':w['technical_qualification'],'operation_complete':True,'root_case_gate_passes':image['passed_gates'],'root_case_gates':len(image['gates']),'root_prompt_fidelity':image.get('prompt_fidelity',image['limit']),'native_source_pixel_qualification':'NOT_DEMONSTRATED','user_acceptance':'PENDING'})
out={'schema':'three-independent-image-tests-aggregate/v1','actual_image_calls':sum(x['actual_image_calls'] for x in rows),'images_present':len(rows),'image_files_exact_to_tool_originals':3,'selected_runtime_prompt_exports_exact_to_reported_hash':True,'human_readable_export_byte_note':'image-tests/b/prompt-export-byte-note.json','request_bytes_common':True,'same_skill_hash':True,'all_managed_operations_complete':True,'technical_qualification_passes':0,'new_visual_source_uptake_arms':0,'new_source_pixel_qualification':'NOT_DEMONSTRATED','user_acceptance':'PENDING','cases':rows};(O/'image-tests-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['actual_image_calls','images_present','technical_qualification_passes','new_source_pixel_qualification']}))

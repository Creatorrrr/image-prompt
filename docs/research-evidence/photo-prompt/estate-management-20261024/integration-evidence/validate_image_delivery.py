"""Validate three actual deliveries; this cannot replace direct pixel review."""
from pathlib import Path
import hashlib, json, struct, datetime

ROOT=Path('/Users/chasoik/Projects/image-prompt')
O=Path(__file__).resolve().parent
R=ROOT/'generated/photo-runs'
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
REFERENCE=Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg')
REFSHA='06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
G='5eab1979465e7ed0627ab628e44c15d4686ddf633937d3e5e9990884488c1de1'
S='f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089'
assert sha(REFERENCE)==REFSHA
assert sha(ROOT/'skills/photo-prompt-image-generator/SKILL.md')==S
specs=[
 ('a','곡물 타작장 점검','authored/final-prompt.txt','image.png','run_manifest.json','image_runs.ndjson','review-audit-output.json','pixel-test-review.json','A01','COMPLETE_ADVISORY_ROUTE_PARTIAL_FAIL',2,4),
 ('b','토지 경계 청원과 도면·장부 대조','final-prompt.txt','image.png','run_manifest.json','image_runs.ndjson','review-audit-result.json','strict-pixel-test.json','B06','FRAGMENT_INSPIRATION_ONLY_FULL_BUNDLE_NOT_ATTEMPTED',2,3),
 ('c','공동 화덕의 빵 전달과 곡물 기록','authored/final-prompt.txt','images/public-bakehouse-initial.png','run-manifest.json','image-runs.ndjson','pixel-review-audit-command.json','concept-pixel-review.json','A07','COMPLETE_ADVISORY_VISIBLE_REALIZATION_PASS',4,1),
]
rows=[]
for arm,concept,prompt,image,manifest,ledger,audit,review,card,source_result,passed,failed in specs:
 run=R/('estate-20261024-arm-'+arm)
 m=read(run/manifest); logs=[json.loads(l) for l in (run/ledger).read_text().splitlines() if l.strip()]
 assert len(logs)==1
 l=logs[0];p=run/prompt;im=run/image;h=sha(im)
 assert m['image_call_count']==l['image_call_count']==1 and l['attempt']==1
 assert m['ledger_run_id']==l['run_id'] and l['status']==m['status']=='success'
 assert m['cross_arm_inputs_used'] is l['cross_arm_inputs_used'] is False
 workflow=read((run/'scoped-run' if arm=='c' else run)/'workflow.json')
 assert workflow['phase']=='review_record_validated'
 receipts={}
 for key in ('h_f2_receipt','runtime_receipt'):
  artifact=workflow['artifacts'][key];path=Path(artifact['path'])
  assert sha(path)==artifact['sha256'];receipts[key]=read(path)
 assert receipts['h_f2_receipt']['generation_id']==G
 assert receipts['runtime_receipt']['generation_id']=='21f5af297d9aba186bc9d41838bfcaf1c4787ee97c1d13f2105a21e38a8c6538'
 assert m['source_ref']==l['source_ref']
 assert l['source_ref'] in ('h-f2:'+G,receipts['runtime_receipt']['source_fingerprint'])
 assert m['skill_sha256']==l['skill_sha256']==S
 assert m['reference_sha256']==l['reference_sha256']==[REFSHA]
 assert m['runtime_prompt_sha256']==l['runtime_prompt_sha256']==sha(p)
 assert l['prompt_en'].strip()==p.read_text().strip()
 assert l['chosen_candidate_ids']==[] and l['chosen_visual_concept_ids']==[]
 for x in l['image_hashes']:
  assert x['sha256']==h==sha(Path(x['path']))
 b=im.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';dims=list(struct.unpack('>II',b[16:24]));assert dims==[1536,1024]
 # PNG chunk CRC and complete stream, without changing pixels.
 import zlib
 offset=8;chunks=[]
 while offset<len(b):
  size=struct.unpack('>I',b[offset:offset+4])[0];kind=b[offset+4:offset+8];body=b[offset+8:offset+8+size]
  assert len(body)==size
  assert zlib.crc32(kind+body)&0xffffffff==struct.unpack('>I',b[offset+8+size:offset+12+size])[0]
  chunks.append(kind.decode('ascii'));offset+=12+size
 assert chunks[-1]=='IEND' and offset==len(b)
 a=read(run/audit);assert a['status']=='pass' and a['record_valid'] is True and a['technical_qualification']=='fail'
 v=read(run/review);assert v['image_sha256']==h
 if arm=='a':assert (v['passed_count'],v['failed_count'])==(passed,failed)
 elif arm=='b':assert (v['pass_count'],v['fail_count'])==(passed,failed)
 else:assert sum(g['status']=='pass' for g in v['gates'])==passed and sum(g['status']=='fail' for g in v['gates'])==failed
 rows.append({'arm':arm.upper(),'concept':concept,'run':str(run),'prompt':str(p),'prompt_sha256':sha(p),'image':str(im),'image_sha256':h,'dimensions':dims,'ledger':str(run/ledger),'ledger_run_id':l['run_id'],'actual_calls':1,'cross_arm_inputs_used':False,'appearance_reference_only':True,'material_use':'inspiration_only','retained_source_card':card,'source_realization':source_result,'topic_gates_pass':passed,'topic_gates_fail':failed,'whole_scene_strict':'FAIL','managed_review_record':'VALID','managed_technical_qualification':'FAIL','pixel_review':str(run/review),'review_audit':str(run/audit),'observed_model':None,'user_acceptance':'PENDING'})
report={'schema':'estate-image-delivery-validation/v1','validated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_DELIVERY_BINDINGS_AND_REVIEW_RECORDS','test_generation_id':G,'skill_sha256':S,'reference':str(REFERENCE),'reference_sha256':REFSHA,'actual_image_calls':3,'image_count':3,'dimensions_each':[1536,1024],'direct_original_pixel_review_performed_by_root':True,'broad_estate_workflow_visible':3,'strict_whole_scene_pass':0,'strict_whole_scene_fail':3,'new_A07_complete_advisory_cue':'PASS_REVIEWER_OBSERVATION','native_source_qualification':False,'causal_improvement_proven':False,'baseline_image_count':0,'original_192_research_cases_executed':False,'user_acceptance':'PENDING','arms':rows,'limits':['Three independently authored unpaired examples are not an accuracy estimate or a causal comparison.','Source registration, natural retrieval exposure, prompt use, direct pixel observation, native qualification and user judgment remain separate.','partial_is_fail; UNOBSERVABLE_NOT_PASS; BLOCKED_UNSCORED.','An occluded contact is insufficient evidence, not a diagnosis of hidden deformation.']}
(O/'image-test-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('arms','limits')},ensure_ascii=False))

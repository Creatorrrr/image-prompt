from pathlib import Path
import json,hashlib,shutil,datetime,subprocess
R=Path('/Users/chasoik/Projects/image-prompt');S=R/'skills/photo-prompt-image-generator';O=Path(__file__).resolve().parent
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pre=read(O/'parent-pre-render-input-check.json');pixels=read(O/'parent-pixel-review.json');arms=[]
reports={'a':'arm-result.json','b':'final-result.json','c':'arm-final-report.json'}
for saved,pixel in zip(pre['arms'],pixels['arms'],strict=True):
 a=saved['arm'];P=Path(saved['run']);state=read(P/'workflow.json');assert state['phase']=='review_record_validated'
 for role,expected in saved['protected_inputs'].items():
  assert state['artifacts'][role]==expected;assert sha(Path(expected['path']))==expected['sha256']
 assert state['h_f2_binding']==saved['h_f2_binding']
 assert len(state['operations'])==1 and state['operations'][0]['status']=='complete'
 lines=[v for v in (P/'image_runs.ndjson').read_text().splitlines() if v.strip()];assert len(lines)==1;row=json.loads(lines[0]);assert row['status']=='success' and row['image_call_count']==1 and row['cross_arm_inputs_used'] is False
 assert row['candidate_pack_version']=='h-f2-v2' and row['chosen_candidate_ids']==[] and row['chosen_visual_concept_ids']==[]
 prompt=(O/'arms'/a/'parent-submitted-prompt.txt').read_text();assert row['prompt_en']==prompt
 assert pre['reference']['sha256'] in json.dumps(row['reference_sha256']);assert pixel['sha256'] in json.dumps(row['image_hashes']);assert sha(Path(pixel['image']))==pixel['sha256']==sha(Path(pixel['report_image']))
 D=O/'arms'/a;shutil.copyfile(P/'image_runs.ndjson',D/'parent-ledger-snapshot.ndjson');shutil.copyfile(P/('independent-run-manifest.json' if a=='b' else 'run_manifest.json'),D/'parent-manifest-snapshot.json')
 audits=[p for p in P.glob('*review-audit*.json') if p.stat().st_size];assert len(audits)==1;review=read(audits[0]);assert review['record_valid'] is True
 shutil.copyfile(audits[0],D/'parent-managed-review-audit.json');report=D/reports[a];assert report.exists()
 arms.append({'arm':a,'run_id':row['run_id'],'image_calls':row['image_call_count'],'ledger_sha256':sha(P/'image_runs.ndjson'),'prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(),'image_sha256':pixel['sha256'],'preplanned_scene_result':pixel['overall'],'preplanned_gate_count':{'pass':pixel['passed_gates'],'total':pixel['total_gates']},'managed_record_valid':review['record_valid'],'managed_technical_qualification':review['technical_qualification'],'report':str(report),'report_sha256':sha(report),'frozen_inputs_unchanged':True,'other_arm_inputs_reported':False})
assert sha(S/'SKILL.md')==pre['latest_skill_sha256'];assert sha(Path(pre['reference']['path']))==pre['reference']['sha256']
assert read(S/'assets/photo_candidate_campus_life_20261024.json')['candidates']==read(O/'new-native-records.json')
assert read(S/'retrieval-runtime.json')==read(O/'post-test-default-observation.json')['current_default']
assert read(O/'research-snapshot-preservation.json')['status']=='pass';assert read(O/'source-validation.final.json')['errors']==[]
r={'status':'DATA_APPLIED_TESTS_COMPLETE_WITH_LIMITATIONS','finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'data':read(O/'source-preservation.json'),'source_index_validation':read(O/'source-validation.final.json'),'installed_test_release':read(O/'installed-release.json'),'current_default_observation':read(O/'post-test-default-observation.json'),'retrieval':read(O/'retrieval-qualification.json')['summary'],'semantic_regression_tests':{'passed':12,'failures':0,'evidence':'semantic-tests.log'},'images':pixels['summary'],'arms':arms,'methodology_status':read(O/'parent-methodology-review.json')['status'],'source_native_approval':False,'user_acceptance':'PENDING','git':{'head_observed_at_finish':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'commit_performed_by_this_task':False,'push_performed_by_this_task':False},'scope':'Source applied and requested three independent generation/review attempts completed. Scene gates 1/3 pass; new-source pixel attribution 0/3 not established; semantic anchor/methodology limitations are retained.'}
(O/'FINAL-VALIDATION.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':r['status'],'image_calls':sum(a['image_calls'] for a in arms),'scene_pass':r['images']['scene_gate_pass_cases'],'source_attribution_cases':r['images']['new_source_pixel_qualification_cases'],'records_valid':[a['managed_record_valid'] for a in arms],'technical_qualifications':[a['managed_technical_qualification'] for a in arms]}))

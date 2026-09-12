"""Artifact integrity checks, deliberately separate from image quality."""
from pathlib import Path
import hashlib,json
ROOT=Path.cwd();RUN=ROOT/'artifacts/photo-runs/model-editorial-three-arm-20260912';OUT=ROOT/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):checks.append({'check':name,'status':'PASS' if condition else 'FAIL'})
snapshot=read(RUN/'source_snapshot.json')
check('frozen_runtime_source_files_unchanged',all(sha(ROOT/p)==h for p,h in snapshot['files'].items()))
reference_hash=sha(RUN/'reference.jpg');manifests=[]
for a in 'abc':
 arm=RUN/f'arm-{a}';m=read(arm/'run_manifest.json');manifests.append(m)
 check(a+'_independent_manifest_one_native_call',m['contract_version']=='photo-independent-run-manifest/v2' and m['image_call_count']==1 and m['cross_arm_inputs_used'] is False)
 check(a+'_image_bytes_match_manifest',all(Path(i['path']).is_file() and sha(Path(i['path']))==i['sha256'] for i in m['image_hashes']))
 check(a+'_same_actual_reference',m['reference_sha256']==[reference_hash])
 check(a+'_local_ledger_exactly_one_row',len([l for l in (arm/'image_runs.ndjson').read_text().splitlines() if l.strip()])==1)
 pack=read(arm/'candidate_pack.json');pack=pack[0] if isinstance(pack,list) else pack
 check(a+'_frozen_pack_core_manifest_match',m['pack_id']==pack['pack_id'] and m['authorial_core_sha256']==pack['authorial_core']['canonical_sha256'] and m['intent_lock_sha256']==pack['authorial_core']['intent_lock']['canonical_sha256'])
 for label,options in [('composed',['composed-audit.json','composed_audit.json']),('runtime',['runtime-audit.json','runtime_audit.json'])]:
  p=next(arm/n for n in options if (arm/n).exists());d=read(p);check(a+'_'+label+'_audit_pass',d['status']=='pass' and not d['failures'])
 p=next(arm/n for n in ['pixel-review-audit.json','pixel_review_audit.json','render_review_audit.json'] if (arm/n).exists());d=read(p)
 check(a+'_pixel_review_schema_valid',not d['schema_failures'])
 check(a+'_user_judgment_not_fabricated',d['user_judgment']['source']=='not_yet_received' and d['representative_eligible'] is False)
check('three_distinct_images',len({m['image_hashes'][0]['sha256'] for m in manifests})==3)
check('three_distinct_cores',len({m['authorial_core_sha256'] for m in manifests})==3)
result={'contract_version':'model-editorial-delivery-integrity/v1','status':'PASS' if all(c['status']=='PASS' for c in checks) else 'FAIL','checks':checks,'image_calls':3,'strict_full_case_pass_count':0,'selected_new_profiles_pixel_pass':['mep_beauty_detail'],'unexercised_new_profile_count':20,'boundary':'Integrity PASS does not mean visual quality PASS. Parent and agent pixel reviews remain all-of FAIL for every complete randomized case.'}
(OUT/'delivery-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],len(checks),'artifact checks; strict complete scene results 0/3')
assert result['status']=='PASS'

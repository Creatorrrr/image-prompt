from pathlib import Path
import json,hashlib,datetime
ROOT=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={
 'a':('8401e63cc6a87f51686cec971e1761701b8a58ec92018f3811f123218f1dae6c','7db96a0623317c1f9160fcfc7704a0f4bf5e24b86b636152092961912f2a7619'),
 'b':('21b1591fcb1b6d855fc555597250cb2a4090c4779a60cccc2447fbd6fbbfa3ef','a51b9367117379f2bec308d1b58cf2c45478d3534120f6e6c5ba217d17a4b325'),
 'c':('4304edd337352c0e372a4418e16f829af1cf36f6636128017dd876801ce0ae2e','dda7f477e647b163f262b022f8a8d7f1c1bbfe3dc1598b340c8165d20c752219')}
images={
 'a':ROOT/'generated/images/school-life-appearance-poses-20261023-a/original.png',
 'b':ROOT/'generated/photo-runs/school-life-appearance-poses-20261023-b/results/school-life-b-original.png',
 'c':ROOT/'generated/images/school-life-appearance-poses-20261023-c/native-original-0b1ce71013b2.png'}
imagehash={'a':'ec9270321f435223bd1b375ada55d08a6635b41645b86cd49659fdb083aefb77','b':'08a6def4b1cbac028d0ebc43db59f09f064228cbb0b34e89e173170aa37f86f3','c':'0b1ce71013b2732e3d79e548e6c56682b896a044d7ddcfc9956b19fd6d15a4d2'}
prompts={a:O/('arms/'+a+'/native-prompt-exact.txt') for a in 'abc'}
native_originals={
 'a':Path('/Users/chasoik/.codex/generated_images/01a16865-0c77-7e43-bc85-f5ddd5aaedc9/exec-0c0f2a60-b1aa-4298-82fc-bf942c339453.png'),
 'b':Path('/Users/chasoik/.codex/generated_images/01a16865-5068-70e1-8f32-9224e244eba1/exec-a506c9a3-858c-4e5a-a3a7-1356480a4d4c.png'),
 'c':Path('/Users/chasoik/.codex/generated_images/01a16865-947e-7f21-afc9-b0dc583e3e24/exec-2f8c9a43-a57e-4198-af31-a129c349f382.png')}
rows=[]
for a,(core,planhash) in expected.items():
 run=ROOT/('generated/photo-runs/school-life-appearance-poses-20261023-'+a);w=read(run/'workflow.json');assert w['phase']=='prompt_delivered',(a,w['phase'])
 roles=w['artifacts'];checked=[]
 for role,ref in roles.items():
  path=Path(ref['path']);assert path.is_file(),(a,role,'missing');assert sha(path)==ref['sha256'],(a,role,'SHA mismatch');checked.append(role)
 assert read(Path(roles['authorial_core_normalized']['path']))['canonical_sha256']==core
 plan=O/'arms/a/test_plan.json' if a=='a' else run/'test_plan.json';assert sha(plan)==planhash
 assert sha(images[a])==imagehash[a]
 ledger=run/'image_runs.ndjson';records=[json.loads(s) for s in ledger.read_text().splitlines() if s.strip()];assert len(records)==1,(a,'ledger count',len(records))
 rec=records[0];assert rec['status']=='success' and rec['image_call_count']==1
 assert rec['prompt_en'].encode()==prompts[a].read_bytes()
 assert hashlib.sha256(rec['prompt_en'].encode()).hexdigest()==rec['runtime_prompt_sha256']
 assert rec['reference_sha256']==['06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7']
 assert rec['chosen_candidate_ids']==[] and rec['chosen_visual_concept_ids']==[]
 assert sha(native_originals[a])==sha(images[a]),(a,'native original copy mismatch')
 rows.append({'arm':a,'workflow_phase':w['phase'],'artifact_roles_verified':len(checked),'core_unchanged':True,'predeclared_test_plan_unchanged':True,'ledger_rows':len(records),'image_path':str(images[a]),'image_sha256':imagehash[a],'native_original_byte_equal':True,'final_prompt_byte_equal_to_native_record':True,'reference_hash_matches':True,'adopted_CIDs':0})
S=ROOT/'skills/photo-prompt-image-generator';before=read(O/'working-source-before-locked.json');old_changes=[n for n,h in before['modules'].items() if sha(S/'assets'/n)!=h]
config=read(S/'retrieval-runtime.json');assert config['generation_id']==read(O/'successor.json')['generation_id'],'Default changed after installation; inspect/rebase without overwriting parallel work'
skillsha=sha(S/'SKILL.md');assert skillsha=='f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089'
assert sha(Path('/Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg'))=='06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7'
assert not old_changes,('Old module bytes changed after registration',old_changes)
out={'status':'pass','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'arms':rows,'total_artifact_roles_verified':sum(x['artifact_roles_verified'] for x in rows),'actual_image_calls_from_independent_native_records':3,'additional_image_generation':False,'installed_default_generation':config['generation_id'],'SKILL_sha256':skillsha,'old_source_module_bytes_preserved':True,'reference_bytes_unchanged':True,'no_staging_commit_push':True,'claim_limit':'Record/transport integrity only. A/B pixel FAIL and C pixel PASS remain separate; user judgment pending.'}
(O/'final-delivery-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))

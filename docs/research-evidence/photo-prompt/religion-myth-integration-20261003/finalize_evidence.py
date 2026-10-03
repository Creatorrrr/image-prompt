#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,struct,subprocess,sys,unittest
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT))
def read(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return s.removeprefix('tests.')
initial_ids=set();initial_bad=set();initial_pass=set()
for i in range(4):
 plan=read(HERE/f'full-suite-shard-{i}-plan.json');r=read(HERE/f'full-suite-shard-{i}-result.json')
 ids=set(map(norm,plan['test_ids']));bad=set(map(norm,r['errors']+r['failures']));initial_ids|=ids;initial_bad|=bad;initial_pass|=ids-bad
final=[];final_ids=set()
for group in ('authored','boundary','retrieval'):
 r=read(HERE/f'final-verification-{group}.json');assert r['successful'] and not r['failures'] and not r['errors'];final.append(r);final_ids|=set(map(norm,r['test_ids']))
suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'))
def flatten(s):
 for x in s:
  if isinstance(x,unittest.TestSuite):yield from flatten(x)
  else:yield x
current_ids={norm(x.id()) for x in flatten(suite)}
missing=sorted(current_ids-(initial_pass|final_ids));assert not missing,missing
assert initial_bad<=final_ids,initial_bad-final_ids
v={'schema_version':'religion-myth-verification-summary/v1','initial_full_discovery_tests':len(initial_ids),'initial_full_suite_failures':sorted(initial_bad),'initial_full_suite_snapshot':'First integrated snapshot before final guard and alternative-expression tightening; original logs retained.','final_affected_tests':sum(x['tests_run'] for x in final),'final_affected_unique_ids':len(final_ids),'final_groups':[{'group':x['group'],'tests_run':x['tests_run'],'successful':x['successful'],'evidence':f"final-verification-{x['group']}.json"} for x in final],'all_initial_failures_rechecked_pass':True,'new_current_cases_tested':len(current_ids-initial_ids),'current_discovered_cases':len(current_ids),'coverage_missing_ids':missing,'coverage_latest_observations_pass':True,'full_suite_rerun_on_final_snapshot':False,'note':'Complete initial suite plus final affected-case rechecks and newly added tests. Do not label this a complete rerun on the final snapshot. Invalid manually typed test targets in earlier diagnostic logs were invocation errors, corrected in the structured final verification.','dictionary_validation':'PASS','visual_profile_index':'PASS','semantic_index_metadata_and_shards':'PASS','git_diff_check':'PASS'}
write(HERE/'VERIFICATION.json',v)
a=read(HERE/'INTEGRATION-AUDIT.json');idx=read(HERE/'FINAL-INDEX-CHECK.json')
a['authored_delta'].update(new_profile_component_groups=157,new_profile_paraphrases=281,narrow_discovery_alternatives=113,owned_junction_discovery_alternatives=6)
a['index'].update(dictionary_hash=idx['dictionary_hash'],visual_registry_sha256=idx['visual_registry_sha256'],existing_profile_vectors_changed=idx['existing_vectors_changed'],existing_profile_vectors_unchanged=idx['existing_vectors_unchanged'],new_profile_vectors=idx['new_vectors'])
more=['tests/test_photo_religion_iconography_boundary_history.py','tests/test_photo_liminal_active_use_korean_data_cleanup.py','skills/subculture-illustration-image-generator/assets/photo_regression_baseline_v6.json','skills/subculture-illustration-image-generator/assets/universal_scene_baseline_v2.json','skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py']
for rel in list(a['file_byte_sha256'])+more:a['file_byte_sha256'][rel]=sha(ROOT/rel)
a['qualification_layers'].update(targeted_tests=f"{v['final_affected_tests']}_PASS_FINAL_AFFECTED_CASES",full_suite={'initial_cases_executed':v['initial_full_discovery_tests'],'initial_failures':len(initial_bad),'initial_failures_resolved':True,'current_case_coverage':v['current_discovered_cases'],'final_full_suite_rerun':False},three_native_image_arms={'arms':3,'native_calls':6,'final_PASS':0,'final_FAIL':3,'retry_per_arm':1,'core_or_pixel_gates_relaxed':False},final_source_retrieval_replay='PASS_ALL_ORIGINALLY_SELECTED_MEANINGS_EXPOSED',native_pixel_qualification_on_final_snapshot='NOT_PERFORMED_GENERATION_SNAPSHOT_PRESERVED')
a['native_generation_snapshot']='native-generation-source-snapshot/MANIFEST.json';a['historical_photo_baseline_versions_preserved']=[1,2,3,4,5];a['current_photo_baseline_version']=6;a['verification_summary']='VERIFICATION.json';write(HERE/'INTEGRATION-AUDIT.json',a)
images=[]
for arm,files,prompt in [('a',['attempt_1.png','attempt_2.png'],'standalone_prompt_attempt_2.txt'),('b',['image_attempt_1.png','image_attempt_2.png'],'standalone_prompt.txt'),('c',['attempt_01/image.png','attempt_02/image.png'],'standalone_prompt.txt')]:
 base=HERE/'qualification'/f'arm_{arm}'
 for n,file in enumerate(files,1):
  im=base/file;b=im.read_bytes();assert b[:8]==b'\x89PNG\r\n\x1a\n';images.append({'arm':arm,'attempt':n,'file':str(im.relative_to(ROOT)),'sha256':sha(im),'dimensions':list(struct.unpack('>II',b[16:24])),'latest_attempt':n==2,'native_pixel_result':'FAIL','tool':'image_gen.imagegen','model_id':'unknown_not_returned'})
 assert (base/prompt).exists()
write(HERE/'NATIVE-ARTIFACTS.json',{'schema_version':'religion-myth-six-native-artifacts/v1','reference':{'path':read(HERE/'BASELINE.json')['reference_path'],'sha256':read(HERE/'BASELINE.json')['reference_sha256']},'images':images,'native_call_count':6,'final_PASS':0,'final_FAIL':3,'qualification_source_snapshot':'native-generation-source-snapshot/MANIFEST.json','final_source_retrieval_evidence':'qualification/FINAL-SOURCE-REPLAY.json','final_source_native_calls':0,'technical_success_does_not_establish_user_acceptance':True})
print(json.dumps({'initial_full_cases':len(initial_ids),'final_affected_cases':v['final_affected_tests'],'current_case_coverage':len(current_ids),'missing':len(missing),'native_images':len(images),'final_pixel_pass':0}))

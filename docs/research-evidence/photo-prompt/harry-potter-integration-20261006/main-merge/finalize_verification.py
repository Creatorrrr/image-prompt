from pathlib import Path
import json,collections,hashlib,subprocess
ROOT=Path.cwd();OUT=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def save(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
plan=read(OUT/'FULL-SUITE-RESUME-PLAN.json');expected=set(plan['discovery_ids']);outcomes={};initial=[];extra=[]
for number in range(len(plan['parts'])):
 worker=read(OUT/f'full-suite-part-{number}.json');assert worker['status']=='COMPLETE'
 outcomes.update({k:v for k,v in worker['outcomes'].items() if k in expected})
 extra.extend([k for k in worker['outcomes'] if k not in expected]);initial.extend(worker['details'])
for name in ['REPAIRED-TESTS.json','DEPENDENCY-RERUNS.json']:
 rerun=read(OUT/name);outcomes.update(rerun['outcomes'])
missing=expected-set(outcomes);assert not missing,sorted(missing)
assert set(outcomes)==expected
known={
 'test_photo_character_appearance_100.CharacterAppearance100Tests.test_all_previous_profiles_keep_meaning_activation_effects_and_native_gates':'MAIN-BASELINE-CHARACTER-FAILURE.json',
 'test_photo_candidate_semantics.PhotoCandidateSemanticsTests.test_maintenance_prose_is_external_and_hash_bound':'MAIN-BASELINE-MAINTENANCE-FAILURE.json',
 'test_photo_liminal_active_use_korean_data_cleanup.LiminalActiveUseKoreanDataCleanupTests.test_complete_merged_state_and_twenty_one_keeps_remain_exact':'MAIN-BASELINE-LIMINAL-FAILURE.json'}
unresolved={name:value for name,value in outcomes.items() if value!='PASS'}
assert set(unresolved)==set(known),unresolved
proof=read(OUT/'V27-APPEARANCE-DATA-PROOF.json')
for field in ['source_files_after','active_shards_after']:
 assert all(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha for name,sha in proof[field].items())
summary={'status':'ALL_TESTS_COVERED_WITH_THREE_REPRODUCED_MAIN_FAILURES','all_discovered_tests_covered':True,'test_total':len(expected),'unique_tests_covered':len(outcomes),'outcome_counts':dict(collections.Counter(outcomes.values())),'full_suite_successful':False,'new_appearance_and_boundary_tests_pass':True,'final_scoped_tests':read(OUT/'REPAIRED-TESTS.json')['tests_run'],'unresolved':[{ 'test_id':name,'status':value,'sealed_main_reproduction':known[name]} for name,value in sorted(unresolved.items())],'outcomes':outcomes,'initial_failure_details':initial,'initial_class_setup_errors_resolved_by_exact_predecessor_registration':extra,'historical_expectations_or_native_verdicts_rewritten':False,'prior_three_arm_native_results':{'arm_a':'PASS','arm_b':'FAIL','arm_c':'FAIL'},'main_photo_scene_code_and_budget_v3_preserved':True,'current_dictionary_hash':proof['current_dictionary_hash']}
save(OUT/'FINAL-TEST-COVERAGE.json',summary)
p=OUT/'README.md';s=p.read_text().replace('Full-suite final coverage is recorded separately after completion; initial failures and final repairs remain auditable.',f"The full suite covers all {len(expected):,} discovered tests: {summary['outcome_counts'].get('PASS',0):,} pass, two fail and one errors. Those three cases reproduce on authenticated pre-integration main DATA; the complete suite is explicitly not all-pass. [Final per-test coverage](FINAL-TEST-COVERAGE.json) retains initial failures and final repairs.")
p.write_text(s)
print(json.dumps({k:summary[k] for k in ['status','test_total','outcome_counts','final_scoped_tests','full_suite_successful']}))

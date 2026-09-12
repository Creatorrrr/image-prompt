from pathlib import Path
import json,re,collections,subprocess,sys
ROOT=Path.cwd();OUT=ROOT/'docs/research-evidence/photo-prompt/model-editorial-professional-implementation-20260912'
def read(p):return json.loads(p.read_text())
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
full=read(OUT/'full-suite/summary.json');comparison=read(OUT/'head-comparison/summary.json');corrected=read(OUT/'head-comparison/complete-fixture-result.json')
prior=OUT/'head-comparison/preliminary-incomplete-copy-summary.json'
if not prior.exists():write(prior,comparison)
comparison['results']=[corrected if r['module']==corrected['module'] else r for r in comparison['results']]
generator=read(OUT/'head-comparison/generator-targeted-result.json')
comparison['results']=[generator if r['module']==generator['module'] else r for r in comparison['results']]
resumes=[read(p) for p in OUT.glob('timeout-resume*/summary.json')]
visual_tail=read(OUT/'visual-tail/summary.json')
resumes=[visual_tail if r['module']==visual_tail['module'] else r for r in resumes]
for resumed in resumes:
 if resumed['all_module_methods_finished'] or resumed.get('tail_finished'):
  comparison['results']=[resumed if r['module']==resumed['module'] else r for r in comparison['results']]
comparison['completed_failure_names_reproduced']=all(r['same_failure_names'] for r in comparison['results'])
comparison['all_failure_names_reproduced']=comparison['completed_failure_names_reproduced'] and all(r['all_module_methods_finished'] for r in resumes)
comparison['fixture_environment_correction']='An initial limited HEAD archive omitted existing docs and fixture artifacts. Those tracked HEAD files were restored and that module was rerun; original logs and preliminary summary remain.'
comparison['claim_boundary']='This compares failing test/subtest names, not exact generated outputs and not all possible regressions.'
write(OUT/'head-comparison/summary.json',comparison)
counts=collections.Counter()
for row in full['results']:
 log=(OUT/'full-suite'/f"{row['module']}.log").read_text()
 matches=re.findall(r'^(?:FAILED|OK) \(([^\n]+)\)',log,re.M)
 if matches:
  for key,n in re.findall(r'(failures|errors|skipped|expected failures|unexpected successes)=(\d+)',matches[-1]):counts[key]+=int(n)
for path in [*OUT.glob('timeout-resume*/current.log'),OUT/'visual-tail/current.log']:
 log=path.read_text();matches=re.findall(r'^(?:FAILED|OK) \(([^\n]+)\)',log,re.M)
 if matches:
  for key,n in re.findall(r'(failures|errors|skipped|expected failures|unexpected successes)=(\d+)',matches[-1]):counts[key]+=int(n)
completed_after_resume=full['reported_test_count']+sum(r['total_unique_methods_completed'] for r in resumes)
unresolved=[r['module'] for r in full['results'] if r['returncode']==124 and not any(x['module']==r['module'] and x['all_module_methods_finished'] for x in resumes)]
summary={'contract_version':'model-editorial-final-validation/v1','source_and_index_status':'PASS','focused_regression_test_count':8,'focused_regression_status':'PASS','delivery_integrity_check_count':30,'delivery_integrity_status':'PASS','visual_index_check':'PASS','git_diff_check':'PASS','discovered_tests':full['discovered_test_count'],'reported_tests_before_targeted_resume':full['reported_test_count'],'reported_unique_tests_after_resume':completed_after_resume,'all_discovered_methods_completed':completed_after_resume==full['discovered_test_count'],'modules':full['module_count'],'full_suite_status':full['status'],'unittest_reported_outcomes':dict(counts),'timeout_modules':[r['module'] for r in full['results'] if r['returncode']==124],'unresolved_test_ids':visual_tail['unresolved_test_ids'],'completed_prefix_failure_cases':len(visual_tail['current_failures'])-len(visual_tail['tail']['failures']),'unresolved_timeout_modules':unresolved,'all_completed_failure_names_reproduced_on_HEAD':comparison['completed_failure_names_reproduced'],'resolved_timeout_modules':[r['module'] for r in resumes if r['all_module_methods_finished']],'failed_modules':[r['module'] for r in full['results'] if r['returncode']],'all_current_failure_names_reproduced_on_HEAD':comparison['all_failure_names_reproduced'],'head_revision':read(OUT/'head-baseline.json')['head'],'native_image_calls':3,'strict_full_image_cases_passed':0,'strict_full_image_cases_tested':3,'new_profile_pixel_cases_passed':1,'new_profile_pixel_cases_tested':1,'new_profiles_not_selected_in_any_render':20,'user_judgment':'not_yet_received'}
correction=read(OUT/'post-correction-holdout.json')
assert correction['status']=='PASS'
assert 'Ran 9 tests' in (OUT/'post-correction-focused-tests.log').read_text() and (OUT/'post-correction-focused-tests.log').read_text().rstrip().endswith('OK')
remaining_match=all((([f for f in r['current_failures'] if "case='holdout_negative_tailoring'" not in f]==r['baseline_failures']) if r['module']=='tests.test_photo_visual_obligations' else r['same_failure_names']) for r in comparison['results'])
summary.update({'focused_regression_test_count_at_render':8,'focused_regression_test_count':9,'post_render_new_regression_detected':'holdout_negative_tailoring','post_render_new_regression_corrected':True,'post_render_frozen_case_replay_status':'PASS','remaining_completed_failure_names_reproduced_after_excluding_corrected_case':remaining_match,'full_suite_snapshot':'Before the post-render direct-paraphrase correction; the final nine-test focused suite and exact failed-case replay ran after it.','source_version_lineage':'source-version-lineage.json','delivery_integrity_scope':'render-time snapshot, before the later retrieval-only correction'})
write(OUT/'validation-summary.json',summary)
subprocess.run([sys.executable,str(OUT/'write_report.py')],cwd=ROOT,check=True)
print(json.dumps(summary,ensure_ascii=False,indent=2))

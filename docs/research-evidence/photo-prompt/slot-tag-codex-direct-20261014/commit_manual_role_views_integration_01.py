"""Finalize exact reviewed role-view/domain integration after actual offline publication."""
import ast,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[3];OUT=R/'manual-role-view-integration-01'
def read(p):return json.loads(p.read_bytes())
def raw(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
 with p.open('x')as f:json.dump(v,f,ensure_ascii=False,sort_keys=True,indent=2);f.write('\n')
Hpath=R/'worker-notes/native-role-view-integration-FINAL-handoff-20261015-01.json';assert raw(Hpath)=='ad86f13322c8e6831a7aa258f0b493bf35dd5f642f926c65857c2b4e31f13ef8';H=read(Hpath);T=read(R/'run_manual_role_views_root_integration_01.json');V=read(OUT/'native-v4-runtime-01/VERIFICATION.json');C=read(R/'ROOT-ENTRY-DOMAIN-OVERRIDE-CHECK-02.json')
assert T['successful']and T['executions']==543 and T['unique_tests']==519 and T['subtests']==1158 and T['source_bytes_stable']and not(T['errors']or T['failures']or T['skipped']or T['blocked_embedding_attempts']or T['model_imports_loaded'])
for name,sha in T['after_hashes'].items():assert raw(ROOT/name)==sha,name
assert V['canonical_record_count']==18250 and V['canonical_slot_count']==139 and V['canonical_native_qualified_records']==0 and V['build']['vector_reuse']==18180 and not V['build']['provider_calls']and not V['build']['provider_cache_hits']
assert C['unit_tests']==6 and len(C['full_compact_actual_source_oldbinding_checks'])==48 and C['dependency_generation'].endswith(V['actual_acquire']['generation_id'])
published={}
G=Path('/Users/chasoik/.cache/image-prompt/photo-shared-runtime/generations')/V['actual_acquire']['generation_id']
for name,sha in T['after_hashes'].items():
 prefix='skills/photo-prompt-image-generator/'
 if name.startswith(prefix):
  q=G/name[len(prefix):];assert q.is_file()and raw(q)==sha,name;published[name]=sha
assert published['skills/photo-prompt-image-generator/scripts/photo_semantic_evidence.py']=='f74a5ef91bc07048c8bf312b66680c5b92b3b7b388f31f1890f31c8578609dee'
paths={Path(__file__).resolve(),ROOT/'skills/photo-prompt-image-generator/scripts/prompt_generator.py',ROOT/'tests/test_photo_entry_domain_override.py',ROOT/'skills/photo-prompt-image-generator/references/maintenance.md'}
for row in H['allowed_five_files']+H['read_only_pins']:
 p=ROOT/row['file'];assert raw(p)==row['raw_sha256'];paths.add(p)
for p in (R/'worker-notes').glob('native-role-view-integration*'):
 if p.is_file():paths.add(p)
 elif p.is_dir():paths.update(x for x in p.rglob('*')if x.is_file())
for name in ['check_entry_domain_override_root_01.py','check_entry_domain_override_root_02.py','ROOT-ENTRY-DOMAIN-OVERRIDE-CHECK-01.json','ROOT-ENTRY-DOMAIN-OVERRIDE-CHECK-02.json','run_manual_role_views_root_integration_01.py','run_manual_role_views_root_integration_01.json','run_manual_role_views_root_integration_01.log','run_manual_role_views_runtime_01.py','prepare_first50_149_root_01.py']:paths.add(R/name)
paths.update(p for p in (R/'native-inputs/first50-catalog149-recheck-plan-10').iterdir()if p.is_file());paths.update(p for p in (R/'native-inputs/prepared/review11870-01250-01300-05').iterdir()if p.is_file())
for name in ['FROZEN-PRODUCTION-PINS.json','native-v4-runtime-01/PREFLIGHT.json','native-v4-runtime-01/VERIFICATION.json','native-v4-runtime-01/build-cache/BUILD-REPORT.json']:paths.add(OUT/name)
report={'schema':'photo-root-manual-role-view-domain-integration/v1','actor':'/root','root_whole_three_production_diffs_and_two_new_tests_read':True,'root_typed_domain_fix_and_test_reviewed':True,'worker_handoff':str(Hpath.relative_to(ROOT)),'worker_final':H['actual_final'],'root_regression':{'executions':543,'unique':519,'subtests':1158,'failures':0,'errors':0,'skips':0,'all_selected_current_asset_configuration_classes_included':True,'file':'run_manual_role_views_root_integration_01.json'},'actual1264_root_checks':{'unit_tests':6,'full_compact_actual_source_oldbinding_cases':48,'file':'ROOT-ENTRY-DOMAIN-OVERRIDE-CHECK-02.json','actual_object_visual_structure_positive':True,'source_guards_binding_denials_adult_no_people_all_actual_E_and_receiver_locks_preserved':True},'runtime':V,'published_module_hashes_verified_against_current_root_pins':published,'manual_view_meaning_requires_direct_review':True,'synthetic_public_pack_not_expected_authority':True,'nonoptin_additional_authority_payload_reads':0,'new_operating_source_proof_or_tag_approvals':0,'operating_native_qualified':0,'research_catalog149_not_activated':True,'Gemini_and_new_model_inference_calls':0,'actual_final149_corebound_hybrid_quality_or_pixels':False,'stages05_08_complete':False};reportpath=R/'ROOT-MANUAL-ROLE-VIEW-INTEGRATION-01.json';save(reportpath,report);paths.add(reportpath)
plan=ROOT/'docs/analysis/2026-10-13-full-corpus-slot-tag-enrichment-plan.md';text=plan.read_text();marker='## 6단계';assert marker in text
paragraph=('같은 canonical 사실의 [수동 역할 view 소비자 통합](../research-evidence/photo-prompt/slot-tag-codex-direct-20261014/ROOT-MANUAL-ROLE-VIEW-INTEGRATION-01.json)을 완료했다. 전체 원문·guard·효과 검증 뒤 정확한 인용 안의 검토 구절을 명시적으로 결합하며, compact와 공개 후보팩의 자체 hash 대신 독립적으로 적재한 전체 원문에서 binding을 다시 만든다. 실제 속성·값·모드·operation·모든 receiver·전제는 그대로이고 새 효과나 permission을 만들지 않는다. 담당자464회·고유458개·1,094 subtest와 루트543회·고유519개·1,158 subtest가 실패·오류·skip 없이 통과했다. 도메인 예외를 다시 차단하던 추가 필터도 보정하여 실제1264 기존 binding의 object+visual_structure 양성 및 원문 조건·제외·잠금 등을 full/compact48경우와 단위6개로 확인했다. 같은 공간 벡터18,180개를 재사용하고 새 추론·Gemini0회로 세대 `'+V['actual_acquire']['generation_id']+'`를 발행·실제 acquire했다. 운영 catalog139개·native0건은 유지하며 연구 catalog149와 개별 의미 심사를 자동 적용하지 않았다. [열한 번째 초안 체크포인트](../research-evidence/photo-prompt/slot-tag-codex-direct-20261014/ROOT-MANUAL-DRAFT-CHECKPOINT-11.json)는 중복 없는 직접 검토 초안6,715개를 보존한 범위이고 정식 승인 수가 아니다. 5단계 전수 심사와 6~8단계는 계속 진행한다.\n\n')
assert 'ROOT-MANUAL-ROLE-VIEW-INTEGRATION-01.json'not in text;plan.write_text(text.replace(marker,paragraph+marker,1));paths.add(plan)
assert not subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT)
for p in paths:
 assert p.is_file()and not p.is_symlink()
 if p.suffix=='.py':ast.parse(p.read_bytes())
 if p.suffix=='.json':read(p)
names=sorted(str(p.relative_to(ROOT))for p in paths);subprocess.run(['git','add','--',*names],cwd=ROOT,check=True);patches={n for n in names if n.endswith('.patch')};check=subprocess.run(['git','diff','--cached','--check','--',*[n for n in names if n not in patches]],cwd=ROOT,capture_output=True,text=True)
if check.returncode:
 save(R/'ROOT-MANUAL-ROLE-VIEW-COMMIT-CHECK-FAILED-01.json',{'actual_returncode':check.returncode,'actual_output':check.stdout,'no_archived_bytes_changed':True});raise AssertionError(check.stdout)
a=R/'ROOT-MANUAL-ROLE-VIEW-INTEGRATION-01-COMMIT-ALLOWLIST.json';save(a,{'schema':'photo-root-exact-commit-allowlist/v1','files':names+[str(a.relative_to(ROOT))],'hashes':{str(p.relative_to(ROOT)):raw(p)for p in sorted(paths)},'archived_patch_whitespace_exempt':sorted(patches),'no_operating_tag_activation':True});paths.add(a);subprocess.run(['git','add','--',str(a.relative_to(ROOT))],cwd=ROOT,check=True);assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=ROOT,text=True).splitlines())<={str(p.relative_to(ROOT))for p in paths}
for p in paths:assert subprocess.check_output(['git','show',':'+str(p.relative_to(ROOT))],cwd=ROOT)==p.read_bytes(),p
print(json.dumps({'verified_files':len(paths),'root_tests':543,'actual1264checks':48,'generation':V['actual_acquire']['generation_id'],'new_operating_native':0}))

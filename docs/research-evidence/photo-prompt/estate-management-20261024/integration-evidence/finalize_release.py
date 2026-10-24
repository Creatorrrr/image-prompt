"""Close evidence only after real installed-default and query qualification."""
from pathlib import Path
import json,hashlib,datetime
ROOT=Path('/Users/chasoik/Projects/image-prompt');O=Path(__file__).resolve().parent;SKILL=ROOT/'skills/photo-prompt-image-generator'
read=lambda p:json.loads(p.read_bytes())
write=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
target=read(O/'DEFAULT-PUBLICATION-TARGET.json');F=Path(target['folder']);release=read(F/'successor.json');installed=read(F/'install-active.json');probes=read(F/'runtime-probes.json');current=read(SKILL/'retrieval-runtime.json');before=read(F/'before.json')['config']
assert installed['status']=='pass' and current['generation_id']==release['generation_id']
assert current['native_generation_id']==release['native_generation_id']
assert current['code_sha256']==before['code_sha256']=='ec29f441dbfc26930e7f4fb71ced759bf5ae271e672176110b21d2a7f6c846ef'
assert installed['CURRENT_writes']==release['CURRENT_writes']==0
assert probes['generation_id']==release['generation_id'] and probes['source_exposure']['status']=='pass'
assert probes['source_exposure']['new_positive_indexed']==22 and probes['source_exposure']['diagnostics_excluded']==56 and probes['source_exposure']['new_source_roundtrips_exact']==78
native=Path(installed['store'])/'generations'/current['native_generation_id']
assert read(native/'assets/photo_candidate_estate_management_bindings_20261024.json')['slot_bindings']==read(O/'new-bindings.json')
images=read(O/'image-test-results.json');assert images['actual_image_calls']==3 and images['strict_whole_scene_pass']==0
skillsha=sha(SKILL/'SKILL.md');assert skillsha==images['skill_sha256']
controls=[r for r in probes['results'] if r['expected_card'] is None]
proof={'schema':'estate-final-default-selection/v1','checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','prior_default_config':before,'selected_config':current,'all_prior_source_records_preserved':read(F/'canonical-source-validation.json'),'installed_release':installed,'default_matches_qualified_release':True,'new_records_exact_first_and_final_source_roundtrips':78,'new_optional_bindings_exact':56,'new_positive_indexed':22,'diagnostics_excluded_from_positive_index':56,'source_inputs_identical_to_image_test_generation':True,'global_source_pool_differs_from_image_tests':True,'image_generation_repeated_on_final_default':False,'natural_queries':probes['natural_queries'],'target_presented_8':probes['target_presented_8'],'target_rank_1':sum(r['expected_rank']==1 for r in probes['results'] if r['expected_card'] is not None),'control_queries':len(controls),'controls_without_new_estate_candidates':sum(not r['new_CIDs_presented'] for r in controls),'CURRENT_writes':0,'skill_sha256':skillsha,'full_deployed_validators_passed':True,'native_source_qualification':False}
write(F/'final-default-selection.json',proof)
target.update({'status':'ACTIVE_DEFAULT_FULLY_VALIDATED','generation_id':release['generation_id'],'native_generation_id':release['native_generation_id'],'final_proof':str(F/'final-default-selection.json')});write(O/'DEFAULT-PUBLICATION-TARGET.json',target)
p=SKILL/'assets/photo_estate_management_semantics_20261024.json';sidecar=read(p);reg=sidecar['registration'];reg.update({'operating_search_and_images':'COMPLETE','default_runtime_publication':'ACTIVE_DEFAULT_FULLY_VALIDATED','test_generation_id':images['test_generation_id'],'default_generation_id':release['generation_id'],'default_native_generation_id':release['native_generation_id'],'final_default_proof':str(F/'final-default-selection.json'),'native_qualification_changed':False});write(p,sidecar);write(O/'DATA-INTEGRATION.json',reg)
final={'schema':'estate-management-final-result/v1','status':'COMPLETE_WITH_STRICT_PIXEL_FAILURES','completed_at_utc':proof['checked_at_utc'],'data_integration':reg,'default_runtime':proof,'image_tests':images,'source_index_checks':'PASS','prompt_and_runtime_audits':'PASS','strict_whole_scene_pixels':'0_PASS_3_FAIL','A07_complete_advisory_visible_relation':'PASS_REVIEWER_OBSERVATION','native_source_qualification':False,'user_acceptance':'PENDING','commits_created_by_this_task':0,'pushes_by_this_task':0,'unrelated_dirty_work_preserved_by_scope':'No existing candidate source was rewritten; concurrent drift observed, not reverted.','report':str(O.parent/'INTEGRATION-AND-IMAGE-TESTS.md')};write(O/'FINAL-RESULT.json',final)
report=O.parent/'INTEGRATION-AND-IMAGE-TESTS.md';s=report.read_text();head=s.split('## 기본 런타임의 최종 반영\n')[0]
canonical=proof['all_prior_source_records_preserved']
text=f'''## 기본 런타임의 최종 반영

최종 기본 런타임 선택과 설치 검증을 완료했다. 그 사이 갱신된 법정·캠퍼스·로맨틱
코미디·메카·군사 등 다른 주제의 데이터가 포함된 기본 세대를 기준으로 이번 후보·연결만 추가했다.
기준 후보 {canonical['old_CIDs']:,}개와 기존 역할·정책·연결을 모두 보존했고, 새 후보
78개를 더했다. 기존 후보 수정은 0개다. 순위 정책과 봉인된 커널 코드는 같다.
오래된 기준의 중간 빌드는 기본값으로 선택하지 않았다.

- 최종 기본 H-F2 세대: `{release['generation_id']}`
- 최종 기본 native 세대: `{release['native_generation_id']}`
- 신규 긍정 후보 22개 모두 인덱스 포함, 진단 56개 모두 긍정 검색 제외.
- 테스트 세대와 최종 기본 세대의 신규 원문 78개 및 연결 56개가 정확히 같다.
- 최종 세대에서도 유지보수 조회 {probes['natural_queries']}개를 실행했다. 주제 조회 8개 중 {probes['target_presented_8']}개가 상위 8개에 포함됐고, {proof['target_rank_1']}개가 1위였다. 일반 대조 조회 4개 중 {proof['controls_without_new_estate_candidates']}개에는 이번 신규 후보가 노출되지 않았다.
- 설치본에 대해 배포된 H-F2/native 전체 검증을 실행했다. 원본 기준을 읽은 뒤 기본 설정이 바뀌지 않았는지 확인하는 CAS를 통과한 후 기본 설정을 선택했다. `CURRENT` 쓰기는 0회다.

세 이미지는 최초 고정 테스트 세대에서 생성했다. 최종 기본 세대는 다른 주제의
후속 데이터를 더 포함하므로 전체 검색 풀은 다르다. 이번 원문이 같다는 사실을
최종 기본 세대에서 이미지 생성까지 다시 검증했다는 주장으로 확대하지 않는다.

[최종 기본 설정 확인]({F}/final-default-selection.json) ·
[최종 조회 결과]({F}/runtime-probes.json) ·
[전체 완료 기록]({O}/FINAL-RESULT.json)

시각 의미 sidecar에는 A01의 부분 실패, B06의 부분 영감 사용, A07의 한 사례 가시
관계 통과를 증거와 함께 연결했다. 374개 표제의 정의·복합 표제 전체가 검증됐다는
표시는 만들지 않았다. 후보·연결의 원문·조건·effects는 이미지 테스트에 사용한 입력과
동일하게 유지했다. 봉인 후보 안의 연구 상태는 등록 시점의 스냅샷이며,
이후의 픽셀 관찰은 sidecar와 실행 증거에 따로 기록한다. 이번 작업에서 커밋·푸시는 하지 않았다.
'''
report.write_text(head+text)
print(json.dumps({'status':'complete','default_generation_id':release['generation_id'],'strict_pixels':'0/3','A07':'pass_visible_advisory_relation'},ensure_ascii=False))

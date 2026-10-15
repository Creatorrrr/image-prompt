"""Write final evidence only after all bounded runtime checks have passed."""
import re
from common import *


def main():
    runtime = read(HERE / 'RUNTIME.json')
    oracle = read(HERE / 'OFFLINE-ORACLE.json')
    relations = read(HERE / 'RELATION-REGRESSION.json')
    installed = read(HERE / 'STAGE04.json')
    assert runtime['status'] == oracle['status'] == relations['status'] == 'PASS'
    assert runtime['generation_id'] == installed['publication']['generation_id']
    assert runtime['requested_slots'] == runtime['independent_query_hashes'] == 149
    assert runtime['positive_population'] == 18180
    assert runtime['issued_receipt_replayed'] and not runtime['independent_retrieval_audit_failures']
    assert len(oracle['roles']) == 6
    log = (HERE / 'FINAL-REGRESSION.log').read_text()
    match = re.search(r'Ran (\d+) tests in ([0-9.]+)s', log)
    assert match and '\nOK\n' in log and int(match.group(1)) == 39
    result = {'schema': 'photo-bounded-existing-tag-reuse-closeout/v1', 'status': 'complete_bounded_scope',
        'stages': {str(n): 'complete' for n in range(1, 6)},
        'generation_id': runtime['generation_id'], 'corpus_sha256': runtime['corpus_sha256'],
        'layout_id': runtime['layout_id'], 'slots': 149, 'candidates': 18250, 'positive_candidates': 18180,
        'candidates_read': 9, 'relationship_cases': 19, 'supplement_candidates': 0,
        'new_bindings': 10, 'deferred_released': 6, 'existing_relations_retained': 3,
        'operating_bindings': 12101, 'remaining_deferred': 3483, 'reviewed_relation_metadata': 40,
        'dependency_suspended_before': 1245, 'dependency_suspended_after': 1242, 'dependency_recovered': 3,
        'candidate_body_condition_effect_kind_changes': 0, 'catalog_changes': 0,
        'native_qualified': 1, 'new_native_qualifications': 0,
        'relationship_adoption_status': 'all19_review_required_native_source_unqualified',
        'local_document_vectors_reused': 18180, 'document_inferences': 0,
        'query_cache_hits': runtime['query_cache_hits'], 'new_local_query_vectors': 149-runtime['query_cache_hits'],
        'actual_slot_queries': 149, 'whole_pool_offline_oracle_roles': 6,
        'relation_positive_cases': 19, 'binding_negative_cases': 19,
        'related_final_tests': 39, 'related_final_tests_status': 'PASS',
        'receipt_replay': 'PASS', 'independent_retrieval_audit': 'PASS',
        'Gemini_calls': 0, 'network': 'OS-denied throughout apply/build/runtime/oracle',
        'whole_corpus_semantic_review': False, 'whole_corpus_tag_enrichment_complete': False,
        'new_images_or_pixel_review': False, 'pushed': False}
    save('STAGE05.json', result)
    current_path = RESEARCH / 'CURRENT.json'
    current = read(current_path)
    current['applied'].update(operating_generation=result['generation_id'], operating_bindings=12101,
        new_persistent_bindings=12, deferred_binding_relations=3483,
        new_persistent_binding_baseline=12089, bounded_reuse_new_persistent_bindings=10)
    current['bounded_tag_reuse'] = {**result, 'report': str((HERE/'REPORT.ko.md').relative_to(ROOT))}
    current['next_exit'] = 'No remaining work in approved bounded149 migration or existing-tag reuse. Remaining3483 deferred relations, broader source qualifications and whole-corpus tagging stay deferred.'
    current_path.write_text(json.dumps(current, ensure_ascii=False, indent=2)+'\n')
    ko = RESEARCH / 'CURRENT.ko.md'
    old = ko.read_text()
    ko.write_text('# 기존 검토 재사용의 제한된 태그 개선 완료\n\n'
        '후보9개·관계19쌍만 확인해 신규 연결10개, 보류 해제6개, 기존 유지3개를 반영했다. '
        '운영149슬롯·18,250후보·12,101연결·보류3,483개이며 보류 의존 제시 중지는1,242개다. '
        '원본·조건·효과·명세와 native 자격1개는 그대로이며 추가 관계19개는 계속 review_required다.\n\n'
        '149개 실제 독립 hybrid 검색·receipt 재생·독립 감사, 영향6역할 전체 스캔 대조, 관련39테스트를 통과했다. '
        '로컬 문서 벡터18,180개와 질의149개를 재사용했고 Gemini 호출0이다. '
        '[최신 리포트](../slot-tag-bounded-reuse-20261015/REPORT.ko.md)를 참고한다. '
        '아래는 직전149개 구조 적용 및 그 이전 마감의 역사 기록이다.\n\n---\n\n'+old)
    plan = ROOT / 'docs/analysis/2026-10-15-bounded-slot-tag-reuse-plan.md'
    text = plan.read_text().replace('상태: **계획 작성 완료, 구현·운영 적용 미착수**.',
        '상태: **1~5단계 구현·검증·단계별 커밋 완료**. '
        '[실행 결과](../research-evidence/photo-prompt/slot-tag-bounded-reuse-20261015/REPORT.ko.md)를 참고한다.')
    text = text.replace('이번 요청에서는 계획 문서와 읽기 전용 기준선만 작성했다. 운영 데이터·코드·인덱스·활성 runtime을 변경하거나 구현 커밋·push를 수행하지 않았다. 후속 실행에서는 단계마다 구현·검증 후 해당 변경만 커밋하며, 무관한174개 기존 tracked 변경과 미추적 작업을 보존한다.',
        '계획 수립 시에는 문서와 읽기 전용 기준선만 작성했다. 이후 실행 요청에 따라 origin/main pull 확인 후 1~5단계를 완료했다. 보충0개·우선9개·19관계로 범위를 고정했고 신규10·보류 해제6·기존 유지3을 운영 반영했다. 전수 검토·native 자격 추가·push는 수행하지 않았다. 실행 착수 시의 무관한175개 tracked 변경과 미추적 작업을 보존했다. 각 단계의 커밋과 상세 검증은 실행 리포트에 기록한다.')
    plan.write_text(text)
    io = runtime['reader_metrics_after_pack']
    report = f'''# 기존 검토 재사용의 제한된 슬롯 태그 개선 결과

승인된 1~5단계를 구현·검증하고 단계마다 커밋했다. 착수 시 origin/main pull은 already up to date였으며 충돌은 없었다. 전수 의미 검토와 추가 후보 발굴로 확대하지 않았다.

## 적용 결과

| 항목 | 결과 |
|---|---|
| 직접 확인 범위 | 기존 수용 후보9개·관계19쌍 |
| 보충 배치 | 0개: 현재 원문·관련 명세·기존 조건을 유지하며 변경할 수 있는 사례가 없음 |
| 신규 연결 / 보류 해제 / 기존 유지 | 10 / 6 / 3 |
| 운영 슬롯 / 후보 / 연결 | 149 / 18,250 / 12,101 |
| 남은 보류 연결 | 3,483 |
| 보류 의존 제시 중지 | 1,245 →1,242; 차단 해소3개, 실제 노출·채택 보장은 아님 |
| 후보 본문·조건·효과·종류·출처·기존 binding 값 | 전부 보존 |
| 슬롯 명세 | 149개 전체 불변 |
| native 의미 자격 | 기존1개 유지, 신규0개 |

새 태그와 보류 해제는 관계 의미를 확인한 결과다. 해당19개 역할 제안은 실제 소비자에서 모두 `review_required/native_source_unqualified_stage05c`로 남았으며 채택 권한으로 승격되지 않았다. 새 application_contract·native proof·원본 보정은 적용하지 않았다. 나머지3,483개 보류와 그 의존성 차단을 유지했다.

## 검증

- [관계 회귀](RELATION-REGRESSION.json):19개 실제 role proposal·source replay, 조건 불충족 음성19개, 의존 차단 해소3개와 남은 제시 차단 확인.
- [최종 회귀](FINAL-REGRESSION.log):39개 관련 테스트 통과. 전체 테스트 suite나 픽셀 품질 검증으로 표시하지 않는다.
- [실행 검증](RUNTIME.json):149개 서로 다른 슬롯 질의의 실제 BM25F·로컬 cosine/RRF, issued receipt 발급·완전 재생·독립 감사 PASS. 조건 적용 후 검색 가능 후보는{runtime['eligible_population_after_intrinsic_guards']:,}개이며 검색 대상은 태그로 분할하지 않은 전체 positive18,180개다.
- [독립 전체 스캔 대조](OFFLINE-ORACLE.json):영향6역할에서 전체 positive 풀의 두 lane ID·점수·순위·RRF와 shard 생략 증명 일치. 이는 오프라인 기술 검증이며 새 의미 심사나 운영 eager fallback이 아니다.
- [빌드](STAGE04.json):같은 ID·전체 text·recipe·로컬 공간의 문서 벡터18,180개 전부 재사용. 새 문서 추론0회이며 재사용이 안 되면 추론하지 않고 오류를 내도록 실행했다. 질의149개도 정확 캐시를 재사용해 새 질의 추론0회다.
- 원본 반영·빌드·게시·실행·oracle은 OS network denial 아래 수행했고 Gemini 호출0회다. 설치된 로컬 공간만 사용했다.

실제 acquire는 metadata1회·23,476,525bytes만 읽고 vector/payload 본문 읽기는0회였다. 첫 전체149슬롯 팩 생성에서는 총{io['read_bytes']:,}bytes, 그중 vector{io['vector_bytes']:,}bytes를 읽었다. cache peak는{io['cache_peak_bytes']:,}bytes로64MiB 이내이고 vector descriptor는{runtime['descriptor_count']}개로64개 이내다. 이 한도는 reader cache이며 전체 프로세스나 모델 RSS가 아니다. 모든 질의가 적은 shard만 읽거나 기존보다 읽기량이 줄었다고 주장하지 않는다. 실제149검색·재생·감사의 경과 시간은{runtime['elapsed_seconds']}초다.

관계 검증기의 첫 시도는 raw source lookup에도 제시 차단을 기대해 실패했다. [최초 코드](verify_relations.attempt01.py)와 [실패 이유](RELATION-REGRESSION-ATTEMPT01.json)를 보존했고, 기존 실제 realization eligibility 경로를 검사하도록 고쳤다. 운영 코드·guard를 테스트 기대에 맞춰 바꾸지 않았다.

## 실행 세대와 커밋

- generation: `{runtime['generation_id']}`
- corpus: `{runtime['corpus_sha256']}`
- layout: `{runtime['layout_id']}`
- 1단계 `1580d572b`:기존 검토 범위·비교 근거 동결.
- 2단계 `2a9054ac9`:19개 관계 판정·수용 근거 재검증.
- 3단계 `37d4d4164`:격리 적용·무결성·의존 차단·변조 거부 검증.
- 4단계 `ee4814ae5`:운영 연결·정책·로컬 인덱스·게시·실제 acquire.
- 5단계:이 리포트를 포함하는 최종 검증·마감 커밋. 커밋 자신의 SHA는 Git 이력과 최종 응답에서 확인한다.

기존175개 tracked 변경을 포함한 현재 checkout을 보존한 상태에서 실행했다. 원래 dirty였던 audit_composed_prompt.py 등 다른 작업은 이번 커밋에 포함하지 않는다. 과거 연구 판정123건·파일럿609건·초안9,685건을 전수 승인으로 바꾸지 않았다. 이번 요청에서는 push·새 이미지 생성·픽셀 평가·전문가 검증·전수 태그 완성을 수행하지 않았다.

[완료 대장](STAGE05.json)과 [원래 계획](../../../analysis/2026-10-15-bounded-slot-tag-reuse-plan.md)에 완료 경계를 기록했다. 남은 보류·본문 보정·추가 native 자격·전체 태그 보강은 후속으로 남긴다.
'''
    with (HERE / 'REPORT.ko.md').open('x') as handle:
        handle.write(report)
    print(json.dumps(result))


if __name__ == '__main__':
    main()

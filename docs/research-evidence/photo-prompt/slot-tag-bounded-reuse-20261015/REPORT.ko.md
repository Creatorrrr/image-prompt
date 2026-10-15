# 기존 검토 재사용의 제한된 슬롯 태그 개선 결과

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
- [실행 검증](RUNTIME.json):149개 서로 다른 슬롯 질의의 실제 BM25F·로컬 cosine/RRF, issued receipt 발급·완전 재생·독립 감사 PASS. 조건 적용 후 검색 가능 후보는8,963개이며 검색 대상은 태그로 분할하지 않은 전체 positive18,180개다.
- [독립 전체 스캔 대조](OFFLINE-ORACLE.json):영향6역할에서 전체 positive 풀의 두 lane ID·점수·순위·RRF와 shard 생략 증명 일치. 이는 오프라인 기술 검증이며 새 의미 심사나 운영 eager fallback이 아니다.
- [빌드](STAGE04.json):같은 ID·전체 text·recipe·로컬 공간의 문서 벡터18,180개 전부 재사용. 새 문서 추론0회이며 재사용이 안 되면 추론하지 않고 오류를 내도록 실행했다. 질의149개도 정확 캐시를 재사용해 새 질의 추론0회다.
- 원본 반영·빌드·게시·실행·oracle은 OS network denial 아래 수행했고 Gemini 호출0회다. 설치된 로컬 공간만 사용했다.

실제 acquire는 metadata1회·23,476,525bytes만 읽고 vector/payload 본문 읽기는0회였다. 첫 전체149슬롯 팩 생성에서는 총4,679,314,026bytes, 그중 vector4,400,912,962bytes를 읽었다. cache peak는67,108,861bytes로64MiB 이내이고 vector descriptor는61개로64개 이내다. 이 한도는 reader cache이며 전체 프로세스나 모델 RSS가 아니다. 모든 질의가 적은 shard만 읽거나 기존보다 읽기량이 줄었다고 주장하지 않는다. 실제149검색·재생·감사의 경과 시간은348.435초다.

관계 검증기의 첫 시도는 raw source lookup에도 제시 차단을 기대해 실패했다. [최초 코드](verify_relations.attempt01.py)와 [실패 이유](RELATION-REGRESSION-ATTEMPT01.json)를 보존했고, 기존 실제 realization eligibility 경로를 검사하도록 고쳤다. 운영 코드·guard를 테스트 기대에 맞춰 바꾸지 않았다.

## 실행 세대와 커밋

- generation: `e19503164fc58237496b2b32a6f547544e20e48e87e28376a5ba1a57cf16a906`
- corpus: `07f3ef7d294767eef533cb9866e83a3f41b0cd72a003fc591c0bda04ec73bfb0`
- layout: `2b40e6433faf99d82be64d30f4e8bb506abc308bed5061ff77914a0e72126d37`
- 1단계 `1580d572b`:기존 검토 범위·비교 근거 동결.
- 2단계 `2a9054ac9`:19개 관계 판정·수용 근거 재검증.
- 3단계 `37d4d4164`:격리 적용·무결성·의존 차단·변조 거부 검증.
- 4단계 `ee4814ae5`:운영 연결·정책·로컬 인덱스·게시·실제 acquire.
- 5단계:이 리포트를 포함하는 최종 검증·마감 커밋. 커밋 자신의 SHA는 Git 이력과 최종 응답에서 확인한다.

기존175개 tracked 변경을 포함한 현재 checkout을 보존한 상태에서 실행했다. 원래 dirty였던 audit_composed_prompt.py 등 다른 작업은 이번 커밋에 포함하지 않는다. 과거 연구 판정123건·파일럿609건·초안9,685건을 전수 승인으로 바꾸지 않았다. 이번 요청에서는 push·새 이미지 생성·픽셀 평가·전문가 검증·전수 태그 완성을 수행하지 않았다.

[완료 대장](STAGE05.json)과 [원래 계획](../../../analysis/2026-10-15-bounded-slot-tag-reuse-plan.md)에 완료 경계를 기록했다. 남은 보류·본문 보정·추가 native 자격·전체 태그 보강은 후속으로 남긴다.

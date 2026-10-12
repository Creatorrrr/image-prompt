# 9단계 — 레거시 제거 및 삭제 후 검증

신규 공통 후보 원본만 운영한다. 구 슬롯 원본·registry·manifest, 구 semantic/profile 인덱스, 슬롯 소속으로 검색 범위를 자르던 코드, 구 팩·receipt·workflow reader와 historical worker를 제거했다. 구 입력을 자동 변환하는 호환 경로는 제공하지 않는다. 단일 후보 원본과 슬롯 연결은 별도 소유하며, 역할 뷰가 원본을 복제하지 않는다.

원본 18,266행을 공통 후보 18,250건과 연결 12,020건으로 이관했다. 의미와 효과까지 동일한 16개 그룹만 병합했고, 내용이 다른 68개 동일 bare-ID 그룹은 분리했다. profile 3,834개, graph 184개, bundle 2,204개와 부속 정책·참조를 보존했다. 원래 슬롯 적용 표의 중복 소유 한 곳을 제거한 뒤 독립 비교 931,826개 필드의 실패는 0건이다. `FIELD-COVERAGE.json`, `POLICY-AUTHORITY-RETIREMENT.json`이 근거다.

양성 검색 대상 18,186건과 현재 인덱스 shard 143개를 엄격히 검증했다. diagnostic 64건은 긍정 후보 검색에서 제외한다. 마지막 인덱스 재생성은 현재 native 벡터 18,186개를 검증하여 재사용했고 신규 provider 호출은 0회였다. 최초 새 문서 벡터 14,352개 및 query 벡터는 실제 provider 응답이며, 재사용 profile 벡터 3,834개는 identity·전체 text·provider/model/dimension/recipe를 검증했다. transport 결과를 알 수 없던 최초 15개 시도는 성공 또는 무료 호출로 계산하지 않는다.

`ASSET-REMOVAL.json`의 1,709개 구 자료와 미참조 파생 자료, 추가 native 파생 shard 143개, 별도의 구 photo regression baseline 63개, 레거시 test/fixture와 기준선 팩 20개를 운영 checkout에서 제거했다. 삭제 전 바이트·SHA와 복구 사본은 checkout 밖에 보관했다. 레거시 전용 검사를 제거한 사실과 의미 회귀의 새 검증 위치는 `TEST-RETIREMENT.json`에 기록했다. 삭제한 과거 전체 suite가 통과했다는 주장은 하지 않는다. 현재 유지한 전체 회귀 388개가 통과했다. 수집기 회귀 7개도 통과했다.

실제 골렘 팩의 별도 프로세스 재검증에서 BM25F 필드 합산 순서에 따른 마지막 소수점 차이를 발견했다. JSON 저장 전후의 필드 순서를 고정하여 해결했으며 검증 허용 오차를 늘리지 않았다. JSON 재적재·mapping 순서 회귀를 포함한 최종 코드 집중 검사 76개가 통과했다. 전체 388개 검사는 이 마지막 BM25F 수정 전 결과이며, 이후에는 영향 범위 검사와 실제 공개 조회·독립 재계산·fresh worker 검증을 수행했다. 잘못된 모듈 이름이 포함된 별도 집중 검사 명령은 중단했고 통과 수에 넣지 않았다.

최종 공개 hybrid 사례와 모든 동결 요청의 결과는 `release-golem-fixed/SUMMARY.json`, `release-blue-cup-fixed/SUMMARY.json`, `FROZEN-COMPARISON.json`에 고정한다. 골렘의 기존 필수 profile와 hard gate 5개를 보존하고 optional 후보 전부를 거절한 구성도 통과했다. 각 공개 사례는 원본 v7 팩·native receipt로 view/compose/transport를 재감사하고 새 worker 2개에서 API 사전 검증까지 수행한다. 실제 provider cache를 사용하며 이미지 호출은 없다. 레거시 파일·import·기존 runtime cache 접근을 차단한 외부 filesystem trace에서 해당 의존은 0건이다.

의미 검색 품질은 7단계의 제한을 유지한다. 비블라인드 유지보수 진단 precision@5 41.67%는 완전한 의미 정확도나 이미지 품질을 뜻하지 않는다. 방향 기준·owner·비슷한 의복 구조·부정절의 순위 혼동은 남으며 optional 결과의 검토가 필요하다. 이미지·native pixel·사용자 선호 검증은 수행하지 않았다.

이 커밋은 격리 구현 checkout의 삭제와 검증을 기록한다. 마지막 `main` 통합 및 primary 소유 구 workflow/cache의 정확한 제거, 기본 native namespace에서의 공개 조회 증거는 `PRIMARY-LEGACY-RETIREMENT.json`과 최종 실행 리포트에 추가한다. 관련 없는 dirty 문서와 기존 이미지·동결 artifact는 보존한다. 다른 checkout의 runtime namespace와 공유된 cache closure는 이 작업의 삭제 대상에 넣지 않는다.

최종 동결 요청 20건: 필수 의미·core·두 lane 실행 실패 0건, warm 요청 p50 15.1035초/p95 17.115초. 골렘 새 namespace cold 공개 CLI 57.235초, 기본 blue-cup fresh CLI 31.354초다. 최종 generation은 `b2355b41f513205671335936e88470aa99d4d2d3d3298fa8d0f0e75a6b2892a2`다.

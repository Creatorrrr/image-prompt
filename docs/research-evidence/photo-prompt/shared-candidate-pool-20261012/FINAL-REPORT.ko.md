# 공통 후보 데이터풀 전환 최종 실행 리포트

공통 원본·다대다 슬롯 연결·전역 BM25F/embedding 검색 전환 1~9단계의 구현, 단계별 검증·커밋 및 `main` 통합을 완료했다. 운영 경로는 신규 native 계약만 받는다. 레거시 후보·manifest·index·reader·resolver·historical worker·호환 fallback은 제거했다.

작업 시작 시 `origin/main`을 `6baa89ab0781401c5565cbdbbffe30153979b317`까지 pull/fast-forward하고, 원격 EMT·토양 맥락과 기존 로컬 원본 변경을 함께 고정했다. 그 후 격리 branch에서 아래 순서로 구현·검증·커밋했다. 마지막 원격 재조회에서도 추가 변경이 없어 해당 branch를 `main`에 fast-forward했다. 원격 push는 수행하지 않았다.

| 단계 | 결과 | 커밋 |
|---|---|---|
| 1 | 전체 원본·dirty/private 데이터·참조·20개 비교 입력 고정 | `a5a3a32e` |
| 2 | 공통 후보·슬롯 catalog·다대다 연결 및 strict validator | `d0aad8bf` |
| 3 | 전체 원본·profile·graph·bundle·정책·참조 이관 | `7215fda3` |
| 4 | 공통 positive index와 실제 provider 문서/query embedding | `3d4d89c9` |
| 5 | 슬롯 소속 필터 없는 global hybrid와 native v7 pack | `5c8ff9e1` |
| 6 | 전체 corpus 순위·배분의 독립 재계산과 native receipt | `82780e03` |
| 7 | 동결 요청·guard·의미 보존·지연 시간 qualification | `3e6dd4a4` |
| 8 | 운영 도구·workflow/retry/record·문서 전환 | `537b4c97` |
| 9 | 레거시 물리적 제거, 삭제 후 공개 CLI·worker·감사 검증 | `d4ea0d31` |

원본 18,266행을 후보 18,250건과 연결 12,020건으로 옮겼다. 슬롯은 원본을 소유하는 부모가 아니라 112개 관리 태그다. 후보 하나가 여러 태그와 연결되거나 태그 없이 존재할 수 있다. 동일한 의미·효과의 16개 그룹을 병합했고, 내용이 다른 68개 동일 bare-ID 그룹은 별도 후보로 보존했다. profile 3,834건, graph 184건, bundle 2,204건과 member 조건을 포함한 독립 비교 931,826개 필드에서 이관 실패 0건이다. 중복 적용 표 한 곳은 catalog/binding으로 소유권을 통일했다.

전체 positive 후보 18,186건에서 BM25F와 exact cosine을 실행한다. diagnostic 64건은 positive 검색 대상이 아니다. 슬롯 태그가 없거나 다른 태그여도 검색될 수 있으며 역할 조건·owner·제외·닫힌 property guard는 별도로 적용한다. candidate 원본·벡터·unique 예산은 한 번만 계산한다. 여러 역할 뷰는 ID를 참조한다. 기본은 `hybrid_required`이고, `keyword_only`는 명시적 진단 모드다. embedding 준비 실패를 hybrid 성공으로 표시하지 않는다.

문서 벡터는 실제 신규 provider 성공 응답 14,352건과 엄격히 검증한 profile 재사용 3,834건이다. 공간은 gemini / gemini-embedding-2 / 768차원이다. query 벡터도 실제 provider 응답 또는 그 검증된 cache를 사용했다. 마지막 index refresh와 최종 공개 검증의 신규 provider 호출은 0회다. 최초 결과가 불명확했던 transport 시도 15건의 원격 처리·비용은 성공 수치나 무료 호출로 간주하지 않는다.

이관 후 유지한 전체 회귀 검사 388건, 수집기 검사 7건이 통과했다. 마지막 별도 worker에서 발견한 BM25F JSON 필드 순서에 따른 소수점 차이는 계산 순서를 고정하여 수정했다. 검증을 느슨하게 하지 않았으며 최종 수정 관련 76건이 통과했다. 전체 388건은 마지막 BM25F 수정 전 결과이고, 이후에는 해당 영향 범위와 실제 공개 경로를 다시 검증했다. 삭제한 레거시 전용 suite를 통과했다고 주장하지 않는다.

최종 코드로 동결 요청 20건의 core·필수 의미·실제 두 lane 실행 실패가 0건이다. warm 요청 p50 15.1035초, p95 17.115초로 사전 30초 예산을 통과했다. 골렘 cold 공개 CLI는 57.235초로 180초 예산 내이며 원래 필수 profile와 hard gate 5개를 보존했다. blue-cup과 골렘의 공개 v7 pack·receipt를 view/compose/transport에서 감사하고, 각각 새 worker 2개와 API 사전 검증에서도 통과했다. 이미지 호출은 수행하지 않았다.

`main`에서는 구 workflow 상태 33건을 백업·SHA 검증 후 제거했다. 원래 상태의 성공·예약·예산을 신규 작업의 성공으로 승계하지 않는다. 이 primary checkout이 소유한 레거시 receipt 182건과 더 이상 공유되지 않는 generation 22개, 관련 source/cache 및 구 index 잔여 파일을 운영 위치 밖으로 옮겼다. 2개 공유 generation과 다른 namespace 포인터 35개는 참조가 남아 보존했다. 다른 작업의 cache GC는 수행하지 않았다. 이 checkout의 구 포인터는 제거했고 기본 `photo-shared-runtime`의 native v2 포인터와 같은 source/code/index 바이트로 공개 조회 및 worker 재감사를 완료했다.

기존 이미지·동결 artifact 7,518개, 5,094,747,664바이트는 동일 경로·동일 SHA로 보존했다. 관련 없는 dirty 문서 2개도 변경하지 않았다. 초기 파생 index stash와 main 통합 전 원본 stash `be4e74d5d45930c6f6f2efc5b2d5f9da451734dd`는 복구용으로 남겨 두었다. 복구 자료와 제거 기록은 `/Users/chasoik/.codex/workspace-backups/shared-candidate-pool-20261012-before-pull`에 있으며 native runtime이 이 기록을 로딩하지 않는다.

의미 순위 품질은 완전한 정확도를 뜻하지 않는다. 7단계의 비블라인드 유지보수 query 진단 precision@5는 41.67%였으며 방향 기준·owner·유사 의복 구조·부정절의 혼동이 남는다. 후보 검색과 검토의 개선을 구조·데이터 무결성, 이미지 품질, native pixel 또는 사용자 선호 보증으로 확대하지 않는다. optional 후보 전부를 거절하는 경로도 유지했다.

세부 근거는 `EXECUTION.json`, 각 단계의 `REPORT.md`, `stage09/FIELD-COVERAGE.json`, `stage09/FINAL-INTEGRITY.json`, `stage09/FROZEN-COMPARISON.json`, `stage09/PRIMARY-LEGACY-RETIREMENT.json`, `stage09/PRIMARY-PRESERVATION.json`, `stage09/primary-native-public/SUMMARY.json`에 저장했다. 레거시 파일·import·기존 cache 접근을 차단한 공개 조회·감사·fresh worker의 filesystem trace도 별도로 기록했다.

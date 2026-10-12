# 8단계 — 운영 경로 전환

공통 manifest·전역 ID를 유지보수 도구와 현재 작업 상태 v2, 재시도 proof v2, 실행 기록 v7, 스킬·구성·검색·runtime 문서에 연결했다. 구 부모 manifest 가져오기와 historical worker 지원 경로를 제거했다. 구 데이터·비활성 검색 코드는 9단계의 물리적 제거 대상이다.

- 원본 18,266행 → 공통 원본 18,250건, 슬롯 연결 12,020건. 독립 비교 필드 931,827개, 누락·변경 실패 0건. 서로 다른 의미 68개 동일 bare-ID 그룹은 합치지 않았다.
- 집중 구조·검색·독립 순위 감사 42건, 네이티브 유지보수 회귀 3건 통과. 실제 전체 원본 maintenance draft 검사 오류 0건. 반복 표현 검토 항목은 의미 품질 통과로 간주하지 않았다.
- 실제 공개 CLI: generation `0d0fa064ffdd768c1db5619d4b6322c7befb33cd5ae53952befb73e66a7c823e`, 54.904초, 전역 unique 64건, BM25F·embedding 각각 384건. 검증된 실제 provider query cache 사용, 이번 재게시 신규 API 호출 0회.
- view 재계산·구성·전송 감사 통과. 별도 두 worker에서 현재 native receipt를 해소하여 구성·전송 재감사 통과. 이 검사는 이미지 호출 없이 실행했다.
- 기존 workflow state 33건의 경로·SHA·phase·보관 사본을 `WORKFLOW-DISPOSITION.json`에 기록했다. 실행 중인 렌더 프로세스 없음. old success를 새 상태로 승격하지 않으며 이미지·동결 요청은 보존한다. 정확한 old state 삭제와 빈 캐시·새 worker 검사는 9단계에서 수행한다.

검색 의미 품질은 7단계의 제한을 유지한다. post-hoc 유지보수 query Hit@5 91.67%, precision@5 41.67%는 비블라인드 진단이며 전체 운영 요청·이미지 품질의 보증이 아니다. 스킬이 요청한 사전 저작과 사용자 판단 경계는 유지했다.

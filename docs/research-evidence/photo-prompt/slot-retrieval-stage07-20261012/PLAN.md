# 7단계: 슬롯 조회 통합 검증과 runtime 정합성

기준 커밋은 6단계 공개 커밋 `270222f9e6c9b8e80a03808a2d60c3f0cb73d7ae`이다. 원래 `FIX-PLAN.md`의 7단계 절차를 실행하며, 원본 폴더의 기존 추적 변경 22개·미추적 작업·default CURRENT를 보존한다. 구현·검증은 별도 관리 worktree와 이 폴더의 격리 runtime store에서 수행한다. 이번 요청은 7단계 실행이며 새 커밋·main 병합·푸시는 별도 실행 상태로 보고한다.

## 고정 기준과 검증 순서

1. 현재 원본 HEAD/index/dirty 파일 해시와 CURRENT를 고정한다. 새 worktree의 code/source/index/shard 및 고정 fixture 바이트를 기록한다. 기존 114개 역할표와 의도한 guard 슬롯 이동을 현재 112개 source 등록과 대응시킨다.
2. 단일 source manifest의 source → loader → lexical/semantic ID 정합성을 전수 확인하고, 현재 en/ko/명시 alias를 owning-slot 전체에서 production ranker로 exact 조회한다. cap 안의 조회와 전체 addressability는 별도 분모로 보고한다. source 유래 probe는 독립적인 창작 성공률에 합산하지 않는다.
3. 고정 자연어 20개(개발 8·holdout 12)와 native alias 20개를 실제 공개 CLI·composer view·receipt·source recomputation audit로 검증한다. 필요 호환 후보 13개 보존, native 양성 10/10·가까운 음성/제외 오노출 0/10, core/controls·64/4/2 예산·optional/public 경계의 변경 0을 기준으로 삼는다.
4. 자연어 사례에 대해 후보 전부 거절 composition을 작성하고, 별도의 대표 adoption 사례에서는 source 의미와 owner/context를 읽고 호환 가능한 후보만 채택한다. 완전한 final prompt를 다시 검토한 postcomposition embodiment record를 작성한다. 전체 composed audit 및 runtime request audit를 실제 matching worker에서 실행한다. 선택·거절 이유와 의미 판정을 구조 PASS와 분리한다.
5. source/ID/hash·후보 삭제·core retrieval binding·stale postcomposition review·runtime-only prose·stale receipt/code/cache·미완성 publication·지연 publisher를 검증한다. 기존 generation/receipt는 보존하고 source_update 및 publisher의 원자적 활성화를 확인한다. 실제 API/이미지 호출은 없다.
6. composition/view/runtime/embodiment/소유 경계의 관련 회귀 검사를 실행한다. 이전 전체 suite의 99개 기준선 재현 결과는 현재 code/source가 동일할 때만 참조한다. 새 실패는 현재 커밋의 수정 전 기준선에서 재현하고, 변경·기존·미해결을 구분한다. 필요한 수정이 생기면 좁게 수정하고 영향 범위를 다시 검증한다.

## 완료와 보고 기준

source/loader/index ID 누락·중복, freshness 및 CLI/receipt/audit 오류, core/lock/negative-intent 경계 위반은 0이어야 한다. 후보의 선택적 지위를 유지하고 전부 거절 경로가 통과해야 한다. source-derived probe, 선언/구조 audit, 최종 prompt 의미 판단을 구분한다. 두 잔여 subject advisory와 기존 49개 cap/source 진단을 숨기거나 해결로 승격하지 않는다.

현재 source·tokenizer·document recipe가 바뀌지 않았다면 인덱스 바이트와 호환 벡터를 검증해 재사용한다. 변경이 필요하면 source부터 수정하고 derived index는 빌더로 재생성한다. 새 code에 matching publisher/CLI/worker를 사용하며 원본 default store는 이번 격리 검증으로 바꾸지 않는다.

이미지·픽셀 품질·실제 사용자 선호는 원래 계획에 따라 별도 범위다. 이 단계에서는 runtime 요청과 감사까지 검증하고 이미지 생성·API 호출·사용자 수용 PASS를 주장하지 않는다. 전체 suite의 미실행 범위와 잔여 의미 제한을 최종 보고서에 명시한다.

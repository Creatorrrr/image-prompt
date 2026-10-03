# 선 표현·중립 재서술 연구 패키지

2026-10-03. 참조 대화 `6abf91b4-b870-83ee-b77e-49f3bd1387b9`의 181개 키워드 그룹과 25개 작성 예시를 검토했다. 외부 자료 85개, 관찰·관계 단위 44개, 맥락 기록 12개, 후보 초안 24개, 회귀 제안 84개를 정리했다. 운영 데이터·코드·인덱스 반영은 이번 작업의 범위가 아니다.

- [상세 연구와 의미 보존 원칙](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/RESEARCH.md)
- [우선순위·파일별 반영·검증 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/IMPLEMENTATION-PLAN.md)
- [표현별 보존·반영·보류 결정 206건](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/TERM-DECISIONS.json)
- [관찰·관계 단위와 맥락 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/SEMANTIC-UNITS.json)
- [슬롯·속성 효과를 선언한 후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/CANDIDATE-DRAFTS.json)
- [회귀 제안과 실행 상태](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/REGRESSION-PROPOSALS.json)
- [외부 출처·사용 범위·접근 한계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/SOURCES.md)
- [패키지 검증·입력 해시 변화](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/neutral-expression-semantics-20261003/VALIDATION.json)

44개는 새 프로필 수가 아니다. 28개 단위에서 기존 프로필 42개를 참조했다. 24개 후보 중 5개는 현재 슬롯 소유 차원을 넘어 반영 보류다. 외부 근거 미연결 78개 키워드 행은 넓은 exact 별칭으로 자동 반영하지 않는다. JSON은 연구 스키마이며 runtime export는 모두 비활성이다.

실행한 것은 초기 스냅샷에서 exact-only resolver 진단 12개와 연구 패키지 구조 검증이다. 84개 회귀는 `PROPOSED_NOT_RUN`이다. 구조 검증 PASS와 별도로 마감 시 입력 74개 중 8개 해시 변화·기존 데이터 3개 파일의 병합 충돌이 관찰돼 `LIVE_CHECKOUT_MERGE_CONFLICTED`로 기록했다. 마감 구조 검증은 충돌 전 성공한 참조 확인의 스냅샷을 사용한다. 기존 충돌은 수정하지 않았다. 전체 core·후보팩·이미지 검증과 운영 반영 전에 충돌이 해소된 최신 입력을 다시 고정해야 한다.

원문·감사 자료는 `CONVERSATION-RECEIPT.json`, `TERM-INVENTORY.json`, `CURRENT-DATA-AUDIT.json`, `CORPUS-RECEIPT.json`, `EXACT-ROUTING-DIAGNOSTICS.json`, `WEB-ACCESS-RECEIPTS.json`, `REFERENCE-CATALOG-SNAPSHOT.json`이다. `.psv` 파일은 작성한 결정·정의의 원본이며 `build_research_package.py`가 JSON과 출처 표를 만든다. `audit_research_inputs.py`는 시작 입력 감사와 진단을 만드는 도구이므로 재실행하여 최초 영수증을 덮어쓰지 않는다.

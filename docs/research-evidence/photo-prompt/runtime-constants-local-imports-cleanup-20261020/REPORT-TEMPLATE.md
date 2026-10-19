# 상수 14개와 지역 import 6개 정리

상태: 검증 완료 후 확정한다.

- 승인된 8개 제품 소스에서 상수 14개·178행과 함수 내부 import 바인딩 6개만 정리했다. 코드 변화는 추가 1행·삭제 184행, 순감 183행이다. 지역 import 하나는 같은 문장의 provider import를 유지한 채 바인딩만 제외했다. 상수 공급·활성 계약·선택/권한/오류 검증 구현은 유지했다.
- 관련 없는 AST가 동일하고, HEAD 기반 index 패치와 현재 작업본 패치를 따로 검증했다. 기존 generator·auditor 미커밋 diff 내용과 다른 파일/다른 worktree, 원래 index를 보존했다.
- 변경 소스의 운영 48건·기본 관련 43건과 추가 permission/realization/오류 증거 계약 67건을 통과했다. 추가 67건은 원본과 변경본 모두 통과했다. 그룹 간 중복은 있으며 독립 테스트 개수 합계로 해석하지 않는다. 추가 테스트 개수는 RESULTS.json 참조. HEAD 대조는 양쪽 각각 43건 중 41건 통과, 기존 실패 2건 동일, 새 회귀 0건이다.
- 격리된 원본/변경본에서 실제 native keyword_only diagnostic retrieve·재사용·composition/runtime audit·native plan/시작·거부된 결과의 실제 recorder subprocess를 실행했다. SHA/프롬프트/attempt/runtime-prompt 조작 4개를 ledger 쓰기 전에 거부하고, 정확한 합성 거부 관찰은 source/receipt를 재감사해 기록했다. 이미지 도구를 실행하지 않았으며 실제 발생한 사용자 실행으로 취급하지 않는다. H 기본 경로와는 별도 native 분기 검증이다.
- 공통 풀 전체 H 단독+F2의 관리 CLI 5개 명령을 원본·격리 변경본·실제 적용본에서 실행하여 top8/전체 순서/점수 동일성을 검증했다. 슬롯당 BM25F 1회·로컬 cosine 1회, 18,180 CID·18,182 RID가 유지된다. 실제 query vector는 기존 검증 cache를 재사용했다.
- installed/issued/frozen audit·파생 native view·archive 450개 순서/17개 테스트·잘못된 CLI 거부를 확인했다. 과거 품질 HOLD는 유지했다. 과거 코드 복사본/manifest/receipt/archive를 수정하지 않았다. 현행 구현 지문 검사를 완화하지 않았다.
- 정책 데이터 6경로, 불명확한 재export, 모델 의존성 import 등 승인 범위 밖 항목은 그대로다. 요청한 20개 대상 중 검증 실패나 불명확한 참조로 보류한 항목은 없다.
- 원래 CURRENT/모델/자산/미커밋·미추적 자료의 시작 지문과 변경 후 지문을 대조했다. 경로 수·Git 상태·추가 동시 작업은 BASELINE-DELTA.json.gz 및 AFTER-PRESERVATION.json에 있다. 이번 검증 자료와 승인 소스 patch만 커밋한다.
- 네트워크 차단·원본 쓰기 금지·격리 소스 fallback 금지에서 검증했다. Gemini·새 임베딩 추론·실제 이미지 생성·원래 CURRENT 쓰기·publish·push는 0회다. native 진단은 임시 store만 발행하고 제거했다.

근거: TARGETS.json, REFERENCE-CHECK.json, HEAD-COMPARISON.json, NATIVE-BRANCH-COMPARISON.json, SOURCE-*.json, MANAGED-*.json, HISTORY-*.json, RESULTS.json, STAGED-CHECK.json. 패치와 출력은 이 디렉터리에 보존되며 임시 실행 경로는 유일한 복구 자료가 아니다.

검증 환경 보완: 최초 추가 테스트의 문서 누락 1건과 native 기준본의 전체 .runtime 공유 링크 거부는 실패 기록을 그대로 보존했다. 원본 문서와 독립 모델 패키지를 제공한 뒤 재검증했으며 제품 코드/보호 검사를 바꿔 통과시키지 않았다. 상세는 HARNESS-INPUT-REPAIR.json, NATIVE-HARNESS-REPAIR.json 참조.

native 마지막 검사의 기대값 보완: 기존 update_operation의 terminal 규칙은 safety_block 관찰을 provider_blocked로 기록한다. 첫 검사가 중간 이벤트명 attempt_recorded를 최종 상태로 잘못 기대한 실패를 보존했다. 제품 함수를 수정하지 않고 기존 규칙에 맞는 terminal/last_event 검사를 넣어 양쪽을 다시 실행했다(NATIVE-TERMINAL-HARNESS-REVIEW.json).

# 해리포터 외형 연구 패키지

2026-10-06 KST. 참조 대화의 수신 키워드 149행을 바탕으로 한 리서치와 데이터 반영 계획이다. 연구용 초안이며 활성 자산에 적용하지 않았다.

- [리서치 보고서](RESEARCH.md): 확인한 사실, 판본/팬 사례, 현행 데이터의 빈틈, 적용 방향.
- [파일별 반영 계획](IMPLEMENTATION-PLAN.md): 우선순위, 원본 배치, 계약 투영, index/pack/pixel 검증.
- [상세 의미 카드 120개](SEMANTIC-CARDS.md), [키워드 149행 대조](KEYWORD-AUDIT.md), [출처와 한계](SOURCES.md).
- [후보 초안 111개](CANDIDATE-DRAFTS.json), [선택형 묶음 8개](BUNDLE-DRAFTS.json), [실제 기존 ID와 배치 제안](RUNTIME-MAPPING.json).
- [profile 형식 예시 3개](PROFILE-PROTOTYPES.json), [회귀 명세 1,080건](REGRESSION-PLAN.json), [원본 이미지 검증 계획 20개 그룹](PIXEL-QUALIFICATION-PLAN.json).
- [구조·참조·compiler projection 검증](VALIDATION.json), [연구 시점 원본 해시](CHECKOUT-SNAPSHOT.json), [전체 연구 수치](RESEARCH-STATS.json).

회귀/이미지 계획은 실행한 테스트 수가 아니다. 출처 일부 사실을 재확인한 행도 whole-row verification을 뜻하지 않는다. 참조 메시지는 20,000자 제한으로 마지막 부분이 잘렸으며 [수신본](REFERENCE-PREVIEW.md)에 범위를 남겼다.

`build_research.py`는 CARD-INPUT.psv와 수신 inventory/source/catalog에서 연구 초안을 재생성한다. `validate_research.py`는 연구 연결과 현재 원본 해시를 검사하며 활성 원본을 수정하지 않는다. `snapshot_current.py`는 초기 기준점 작성용이므로 이번 기준점을 보존하려면 재실행하지 않는다.

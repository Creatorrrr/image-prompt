# 전기 용어 리서치 패키지

2026-10-08 연구·계획 산출물. 원문 26개 범주와 435개 keyword row를 복구했다. 상세 카드 116개, 후보 설계 초안 95개, 출처 레코드 42개, 후속 회귀 계획 36개를 담는다.

- [상세 리서치](RESEARCH.md): 핵심 구분, 조사 결과, 원문 범주별 처리, 기존 데이터와 대조.
- [반영 계획](IMPLEMENTATION-PLAN.md): 첫 12개 원자, 이후 우선순위, source/index/pack/픽셀 검증 단계.
- [상세 카드 목록](CARD-CATALOG.md): 발생원·구성요소·관계·혼동·한계·출처.
- [구조화 연구 데이터](research.json), [후보 설계 초안](CANDIDATE-BLUEPRINTS.json).
- [원문 키워드](SEED-KEYWORDS.json), [항목별 처리 ledger](SEED-COVERAGE.tsv), [출처와 읽기 수준](SOURCES.json).
- [계획 회귀 사례](REGRESSION-PLAN.json), [패키지 구조 검사](PACKAGE-VALIDATION.json), [작업 종료 시점 관측](FINAL-STATE.json).

현재 완료는 연구 패키지의 구조 검사까지다. 원본 데이터 등록, 인덱스·임베딩, 실제 후보팩 실행, 이미지 생성, 픽셀 검증, 커밋·푸시는 실행하지 않았다. `runtime_ready`와 `effects_verified`는 모든 초안에서 false다. 후속 36개 사례는 계획이며 실행한 테스트가 아니다.

연구 중 보호 파일 469개 중 467개는 해시가 유지됐다. semantic index manifest와 기존 history 테스트 한 파일에서 조사 창 사이의 변경을 관측했다. 이번 작업은 이 새 연구 폴더에만 파일을 작성했으며, 기존 두 파일을 덮어쓰거나 되돌리지 않았다. 다음 구현 때 최신 source/index 상태를 다시 확인한다.

`build_research.py`는 이 폴더의 입력 표에서 seed/card/source/blueprint/coverage/regression/catalog 통계를 재생성한다. runtime 모듈을 import하거나 source/index를 수정·게시하지 않는다. `CHECKOUT-BEFORE.json`, `REPO-COVERAGE.json`, `PACKAGE-VALIDATION.json`, `FINAL-STATE.json`은 관측 시점의 별도 evidence이며 builder가 재작성하지 않는다.

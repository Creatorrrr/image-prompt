# 하렘물 시각 의미·후보 데이터 리서치

2026-10-23. [하렘물 용어 조사](https://chatgpt.com/c/6adb5af5-62c0-83ee-ac08-0af3cfba439a)의 용어 **314행과 조합 6행**을 Chrome의 전체 표와 대조하고, 상세 조사와 반영 계획을 작성했다.

가장 중요한 보강 방향은 **복수 인물의 관계 방향·접촉 소유자·복식/매체의 연결 경계**다. 성격·과거·친족·동의·혼인·결말은 필요한 문맥으로 유지한다. 기존 후보의 자기/상대 손 범위, 영어 OR/한국어 AND, 클립/스타킹의 번역 누락, 진행 중인 반응과 aftermath 역할의 구별도 구체 심사했다.

먼저 [상세 리서치](RESEARCH.md), 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|14개 논점: 관계망·게임/패널·성격·접촉·복식·성인/폭력 분류·역사/비평·기존 데이터|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|P0/P1/P2, 사진/일러스트레이션 반영 경로, 실제 role·효과·조건·source/index/search/pixel/활성화·복구|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|전체 320행 연결. 용어 중 240행 카드 연결, 문맥 세부 38행·외형 36행 추가 심사, 조합 6행 별도|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|90카드: 형태/배치 68·선택적 대리 장면 8·문맥 경계 14|
|[candidate-drafts.json](candidate-drafts.json)|위 카드의 부분집합인 한영 초안 76개; 운영 import·native 승인 없음|
|[SOURCES.md](SOURCES.md) / [sources.json](sources.json)|외부 26건의 실제 접근 깊이: 본문 일부 20·검색 추출 1·실패 5|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [existing-source-decisions.json](existing-source-decisions.json)|95모듈·21,252 CID의 지정 어휘 조사, 일치 121레코드 보존, 기존 CID 18개 구체 판단|
|[SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)|원 대화의 6개 창작 조합별 두 장면 대안과 혼동 경계|
|[PENDING-DETAILS.md](PENDING-DETAILS.md)|미연결 외형 36행의 구체 검토 목표와 문맥 38행의 추가 확인 범위|
|[development-cases.json](development-cases.json) / [BOUNDARY-CASES.tsv](BOUNDARY-CASES.tsv)|카드 파생 180질의+경계 36쌍 144질의=개발 324질의 설계; 검색 미실행·독립 holdout 아님|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|첫 12장면×2팔=24장 비교 제안; 생성·픽셀 NOT_RUN|
|[SOURCE-CAPTURE.md](SOURCE-CAPTURE.md)|도구의 20,000자 제한·Chrome 전체 표 확인·표제 전사 대조 및 도판 한계|
|[BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json)|기준 HEAD·기존 dirty 상태·보호 파일 hash·연구 구조와 보존 검사|
|[WORKSPACE-OBSERVATIONS.md](WORKSPACE-OBSERVATIONS.md)|공유 manifest/runtime의 별도 변동과 실제 반영 전 기준 재확인 필요|
|[SHA256SUMS](SHA256SUMS)|연구 파일 바이트 무결성; 사실성·검색·이미지 품질 인증 아님|

314개 정의를 모두 외부 검증한 자료는 아니다. 원 표제는 전수 연결했으며 미확인 정의·접근 실패·추가 도판 심사는 남겼다. 후보의 geometry는 연구자가 저술한 선택지다. 외부 출처가 모든 배치나 관계를 증명한 것은 아니다. FIT 내부 도판은 깨진 썸네일 때문에 전체 실물 형태를 픽셀로 검토하지 못했다.

연구 구조 검사는 24/24 통과했다. 보호 파일 검사에서는 공유 manifest와 runtime의 별도 변동을 관찰했으므로 최종 상태는 `STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE`이다. 현재 source 기준으로 후속 심사해야 한다.

완료 범위는 조사·기존 source 읽기 전용 진단·연구 카드/후보 초안·상세 반영 및 평가 계획·연구 구조 검증이다. **운영 데이터 변경, native qualification, index build/verify, 실제 검색·선택·compose, 이미지 생성/픽셀 평가, 설치 활성화, 사용자 수용, commit/push는 수행하지 않았다.** 공유 작업 트리의 별도 변경 여부는 VALIDATION의 drift를 따른다.

재생성·검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/harem-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/harem-20261023/build_audit_report.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/harem-20261023/evaluation_design.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/harem-20261023/validate_research.py
```

builder는 연구 폴더에만 쓴다. `audit_corpus.py`는 snapshot이 있으면 중단하며 연구 당시의 source를 덮어쓰지 않는다. 실제 반영 단계에서는 새로운 evidence 폴더에서 현재 기준을 수집한다.

# 수사물 시각 의미·후보 데이터 리서치

> 후속 반영 작업: 2026-10-25 사용자 요청에 따라 시각 후보 66개, 진단용
> 47개, 선택적 binding 132개를 실제 source에 추가하고 기존 5개 표현을
> 좁게 수정했다. 연구 당시의 미반영 상태와 해시 검증은 아래에 역사적
> 기록으로 보존한다. 설치·검색·독립 이미지 테스트의 현재 결과는
> [반영 결과](INTEGRATION-RESULTS.md)와 `integration-evidence/`를 확인한다.

2026-10-25 KST. 참조 대화 **수사물 용어 정리**를 전체 확인하고, 현재 사진 corpus와 비교해 만든 조사·초안·반영 계획이다. 먼저 [상세 리서치](RESEARCH.md)와 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽는다.

|자료|내용|
|---|---|
|[전체 키워드 지도](KEYWORD-ATLAS.md)|용어 321개, 원 뜻·선택 대안·문맥 경계; 별도 혼동 10개·원 조합 8개|
|[시각·문맥 카드](VISUAL-CARDS.md)|시각 대안 76개와 문맥 경계 40개; 한영·소유·연결·가시 판정·추론 한계|
|[후보 초안](candidate-drafts.json)|운영 CID 없는 76개 제안과 필요한 source/effects/native 심사|
|[기존 원천 관찰](CORPUS-FINDINGS.md)|22,899개 원천·17,836개 binding의 기준과 lexical 관찰 한계|
|[기존 source 비교](existing-source-decisions.json)|28개 CID의 전체 원문·조건·효과·binding과 재사용/수정/분리 판단|
|[출처](SOURCES.md)|외부 자료 29개와 원 대화; 주장별 지원 범위·접근 수준·잔여 확인|
|[혼동 요청](boundary-cases.tsv)|30쌍의 한영 대비 요청과 기대 구분|
|[개발 요청](development-cases.json)|258개 작성자 노출 개발 요청; 검색 미실행·독립 holdout 아님|
|[픽셀 계획](PIXEL-PLAN.md)|14장면×baseline/stage, 초기 3쌍부터 진행하는 평가안; 생성 미실행|
|[검증 결과](VALIDATION.json)|ID·참조·한영·슬롯·현재 source 해시·연구 상태 검증|

시각 대안은 65개 현재 상태, 4개 서사 proxy, 1개 별도 교육도, 6개 근거 보류로 나뉜다. 76개를 모두 신규 운영 후보로 넣지 않는다. 기존 source 재사용과 실제 심사에 따라 수량이 달라진다. 321개 전체를 개별 학술/법률 검증한 것도 아니다.

도구 응답은 20,000자에서 잘려 Chrome의 30,689자·17절·24표를 끝까지 확인했다. [복구 기록](reference-capture.json)은 원문/표제 전사/설명 요약의 실제 보존 범위를 명시한다. 폭력·성적 소재도 용어·문맥에 포함했으며, 외형·실제 행위·의학/법적 결론·이미지 생성 가능성을 구별했다.

연구 graph와 출처는 native facts·소유자 선택·효과 권한·source qualification을 주지 않는다. 운영 원천·manifest·index·설치 selector 변경, 검색/compose 실행, 이미지 생성, commit/push는 하지 않았다. 이번 검증의 성공은 후속 단계의 성공이 아니다.

아래는 연구 단계 당시의 재현 명령이다. 후속 반영으로 운영 source가 의도적으로
달라졌으므로, 당시 source 무변경을 전제로 한 `VALIDATION.json`은 역사적
증거다. 현재 반영 검증은 `integration-evidence/validate_final_integration.py`와
그 결과를 사용한다. 연구 builder는 연구 Markdown을 다시 쓰므로 후속 안내를
보존한 상태에서 사용해야 한다. `audit_corpus.py`는 기존 baseline을 덮어쓰지
않는 별도 read-only 수집이며 다시 실행할 필요가 없다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/investigative-fiction-20261025/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/investigative-fiction-20261025/validate_research.py
```

입력: `cards.tsv`, `context-cards.tsv`, `keyword-supplement.tsv`, `research_sources.py`, 첫 13개 원문 표와 corpus snapshot. 산출물: `semantic-cards.json`, `keyword-routes.json`, `candidate-drafts.json`, `BUILD-SUMMARY.json`, 각 Markdown 지도. [파일 해시](FILES.sha256.json)는 validator 실행 시 연구 폴더의 파일을 기록한다.


## 2026-10-25 관계 개선 재시험

[원인 분석·변경·동일 3컨셉 재시험 결과](retest-20261025/RESULTS.md).
18개 일반 관계 대안·3개 diagnostic·39개 binding을 추가하고 요청 계보 비교 오류를
수정했다. 독립 3개 arm에서 신규 일반 기여 6개의 실제 프롬프트·도구 입력 반영을
확인했으며, 추가효과 전체 픽셀 기준은 2/6, 전체 장면은 0/3 통과했다.
원래 통합 증거는 과거 결과로 보존한다. 상세 CID/hash·이미지·리뷰 대조는
[재시험 FINAL](retest-20261025/integration-evidence/FINAL.json)에 있다.

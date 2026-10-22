# 다크 판타지·그림다크 리서치 패키지

2026-10-22. 초기 연구 결과와 데이터 반영 계획을 보존한 패키지다.
후속 데이터 등록·검색 실행·독립 이미지 실험은
[INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md)와 `integration-evidence/`에서 확인한다.
아래 NOT_RUN과 초기 VALIDATION의 비활성 상태는 연구 단계의 기록이다.

먼저 [RESEARCH.md](RESEARCH.md)를 읽고 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)로 이어서 보면 된다.

| 산출물 | 내용 |
|---|---|
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 대화의 키워드 247개 전체를 시각·정황·문맥·시간·감각·판본 경로로 구분 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 카드 72개: 성분·소유자·방향 관계·혼동·주장 한계·출처·검토 gate |
| [candidate-drafts.json](candidate-drafts.json) | 위 카드 중 한영 시각 후보 초안 68개. runtime loader 입력/CID/RID/native approval이 아님 |
| [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md) | 원 대화의 조합 예시 7개를 행동·반응·사물·공간과 남은 서사 경계에 연결 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 출처 46개, URL·실제 읽은 범위·확인 가능한 의미와 한계 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 기존 원문·조건·효과와의 구체적인 재사용/보완 판단 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | 19,006개 후보 스냅샷의 지정 field 어휘 진단. 실제 검색/의미 부재 판정 아님 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 레코드 18개와 연결의 full snapshot·해시. 순위·전체 native 승인을 뜻하지 않음 |
| [topology-neighbors.json](topology-neighbors.json) | 추가 고정 필드 결합 탐색의 3개 이웃; 2개 일반 의복 오탐과 1개 유기 외피 사례 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 24·경계 16·일반 대조 12·비가시 대조 4, 총 56사례/112개 한영 질의, NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 36장 비교와 조건부 추가 36장 계획, NOT_RUN |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 참조 대화 복원·접근 실패·요약/검색 본문만 읽은 자료·남은 원전 조사 |
| [BASELINE.json](BASELINE.json) | 시작 HEAD·dirty 목록·추적 파일 3,634개 및 선택한 untracked 자료의 해시 |
| [RUNTIME-CHECK.json](RUNTIME-CHECK.json) | 읽기 전용 의존성/installed recorder 확인. 연구 자료의 운영 채택 증거 아님 |
| [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 참조/graph/표본/해시 등 연구 패키지 검사와 동시 작업에 따른 원본 변화 관찰 |

72개 카드와 68개 초안의 수는 중첩되므로 합산하지 않는다. 247개 개별 정의 모두를 독립 사전에서 검증한 것은 아니다. 외부 자료는 개념군·주요 구분을 지원하고 구체적인 시각 실현은 저술한 제안이다.

파생 문서 재생성·검증:

```sh
python3 docs/research-evidence/photo-prompt/dark-fantasy-grimdark-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/dark-fantasy-grimdark-20261022/validate_research.py
```

`build_research.py`는 이 폴더의 파생 문서·JSON·평가 TSV만 쓰고 현재 slot catalog를 읽는다. `audit_corpus.py`는 소스를 다시 읽어 **이 폴더의 스냅샷 증거를 새로 쓴다.** 구현 후 소스가 달라졌다면 옛 증거를 덮기 전에 별도 스냅샷으로 보존해야 한다. 임베딩/이미지 API·운영 등록·게시를 수행하지 않는다.

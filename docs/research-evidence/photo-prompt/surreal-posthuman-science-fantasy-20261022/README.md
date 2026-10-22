# 초현실·포스트휴먼·사이언스 판타지 데이터 보강 리서치

2026-10-22 KST. 대상 대화: [초현실 조합 용어 조사](chatgpt-conversation://6ad98716-5014-83ee-b7a8-856a91f6e97c).

핵심 제안은 **장르별 묘사 묶음을 늘리는 대신, 서로 다른 대상이 어떻게 이어지고 어긋나며 같은 형상으로 읽히는지를 선택 가능한 완전한 관계로 보강하는 것**이다. 개념·과학적 설명·서사적 사실은 가시 형태와 각각의 증거 범위를 유지한다.

이번 산출물은 182개 원 대화 키워드, 33개 외부 자료의 열람 범위, 12개 관계군의 가시 초안 72개, 문맥 기록 16개, 기존 source 36개 스냅샷, 평가 설계 112사례/224질의를 담는다. 33개 원전 전체를 읽었거나 182개 정의를 독립적으로 검증했다는 뜻은 아니다. `keyword-register.json`은 직접 연결한 개념별 자료와 가족군 배경 자료를 구별한다. 초안의 구체적인 장면은 이번에 저술한 제안이며 인용 작품의 정본 디자인이 아니다.

| 문서 | 내용 |
|---|---|
| [REPORT.md](REPORT.md) | 상세 조사 결과, 중요 개념의 차이, 12개 관계군, 충분성 기준 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 재사용→정제→신규→검증→설치의 단계와 종료 조건 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 실제 source 규모, 원문 차이, 재사용 판단과 공백의 증거 한계 |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 12군×3 arm=36장 초기 비교 제안과 평가 기준, NOT_RUN |
| [sources.json](sources.json) | 33개 자료의 URL·실제 열람 범위·지원 주장·한계 |
| [keyword-register.json](keyword-register.json) / [seed-keywords.tsv](seed-keywords.tsv) | 182개 키워드의 정의 출발점·sense·경로·혼동 경계 |
| [KEYWORD-MAP.md](KEYWORD-MAP.md) / [CANDIDATE-ATLAS.md](CANDIDATE-ATLAS.md) | 사람이 읽기 쉬운 키워드별 표와 한영 후보 초안 도감 |
| [semantic-cards.json](semantic-cards.json) | 72개 한영 가시 초안, 소유자·방향 관계·혼동 예·픽셀 조건 |
| [candidate-drafts.json](candidate-drafts.json) | 운영 loader 입력이 아닌 후보 저술 검토안, CID/RID 미발급 |
| [context-records.json](context-records.json) | 16개 비가시·문맥 경계. 긍정 이미지 효과 없음 |
| [CORPUS-AUDIT.json](CORPUS-AUDIT.json) | 19,275개 source의 지정 어휘 진단과 55개 모듈 해시 |
| [existing-source-snapshots.json](existing-source-snapshots.json) | 36개 이웃 후보의 전체 원문·조건·효과·binding 스냅샷 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발72·경계16·일반12·비가시12, 전부 NOT_RUN |
| [BASELINE.json](BASELINE.json) / [RUNTIME-OBSERVATION.json](RUNTIME-OBSERVATION.json) | 시작 HEAD·dirty·추적 파일 6,139개 해시와 설치 recorder 읽기 검사 |
| [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 패키지 참조·관계·수량·원본 drift 검사 |

대화 조회 도구는 20,000자에서 잘렸으므로 Chrome에서 같은 대화의 14절까지 추가로 읽고, 네 축과 15개 용어 표의 182개 레이블을 기록했다. 저장한 `REFERENCE-PREFIX.md`는 조회 도구의 **부분 원문**이다. 10개 결합 예시와 8개 작품은 키워드 182개 수에 넣지 않았다.

운영 source 등록·임베딩·인덱스 빌드/게시·검색 실행·이미지 생성·픽셀 판정·사용자 수용·커밋/푸시는 이번 범위에서 수행하지 않았다. 기존 작업 파일의 보존/동시 변경 결과는 `VALIDATION.json`을 따른다. 설치 recorder 검사의 PASS는 검색이나 이미지 품질의 PASS가 아니다.

오프라인 재생성 및 검사:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/surreal-posthuman-science-fantasy-20261022/validate_research.py
```

두 명령은 이 연구 폴더 안의 산출물만 쓴다. `audit_corpus.py`는 읽기 당시 증거를 새로 만드는 일회성 스냅샷 도구이며 기존 스냅샷 덮어쓰기를 거부한다. 후속 구현에서는 별도 단계 폴더에 새로운 기준 증거를 남긴다.

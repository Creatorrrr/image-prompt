# SCP 시각 의미·후보 데이터 조사 패키지

2026-10-22. 상세 조사와 반영 계획이다. 운영 후보·인덱스·설치본은 변경하지 않았다.

먼저 [조사 보고서](RESEARCH.md), 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

| 산출물 | 내용 |
|---|---|
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 참조 대화 20개 분야·표 항목 268개 전체 경로. 표 밖 110-몽토크 경계도 포함 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 의미 카드 103개: 한영 실현·소유/성분·방향 관계·혼동·주장 한계·출처·픽셀 판정 제안 |
| [candidate-drafts.json](candidate-drafts.json) / [REALIZATIONS.tsv](REALIZATIONS.tsv) | 위 카드 중 선택 가능한 가시 초안 70개. native CID/RID·승인·runtime import가 아님 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 원전 73개 접근, 70개 핵심 구간 검토. 읽은 범위·한계·저작자 탐지 상태·본문 해시 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 현재 소스의 재사용·보완·신규·문맥·보류 판단 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | 19,078개 source record의 지정 primary field 어휘 진단. 실제 검색·의미 부재 검증이 아님 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 15개 CID의 full record·binding·해시와 비교 제안 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 양성38·경계20·일반12·비가시8, 총 78사례/156개 한영 입력, NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 최초 12사례/36장 비교 제안, NOT_RUN |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) / [LICENSE-NOTE.md](LICENSE-NOTE.md) | 참조 복원·읽기 한계·미해결 근거·파생 자료/개별 이미지 권리 구분 |
| [BASELINE.json](BASELINE.json) / SOURCE-DRIFT.json | 시작 HEAD·dirty 상태·추적 파일 해시와 최종 소스 변화 대조 |
| [RUNTIME-CHECK.json](RUNTIME-CHECK.json) | 설치된 recorder/의존성의 읽기 전용 확인. SCP 자료 채택 증거가 아님 |
| VALIDATION.json / SHA256SUMS | 연구 자료의 참조·그래프·슬롯·snapshot·mutation rejection 및 무결성 검사 |

103개 카드와 70개 초안은 중첩되므로 합산하지 않는다. 표 항목 268개의 모든 정의를 독립 원전에서 하나씩 검증한 것은 아니다. 구체적인 장면 기하와 실현은 저술한 제안이며, source/version이 지정된 경우에도 전체 numbered-character fidelity를 뜻하지 않는다.

파생 자료 재생성 및 구조 검사:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/scp-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/scp-20261022/validate_research.py
```

`build_research.py`는 저장한 출처 metadata/카드/참조 표와 현재 catalog를 읽고 이 폴더의 파생 JSON/Markdown/TSV만 쓴다. 임시 원문 cache가 없어도 재생성할 수 있다. `validate_research.py`는 이 폴더에 검증·해시·drift 기록만 쓴다.

`collect_sources.py`는 공공 원전의 현재 본문을 다시 가져오고 출처 metadata를 덮어쓴다. `audit_corpus.py`도 현재 소스를 읽어 이 폴더의 비교 snapshot을 덮어쓴다. **후속 실행 전 기존 증거를 별도 보존해야 한다.** 두 명령은 운영 source/index에 쓰지 않는다. 모든 연구 스크립트에 임베딩·이미지·설치·게시 동작은 없다.

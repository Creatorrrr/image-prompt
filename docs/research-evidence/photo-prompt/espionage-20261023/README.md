# 첩보물 시각 의미·후보 데이터 연구

2026-10-23. [RESEARCH.md](RESEARCH.md)에 조사 결과, [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 반영 순서와 완료 기준을 정리했다.

| 자료 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 장르/역할/서사와 화면의 분리, 분야별 조사 결과, 근거·남은 범위 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | reuse/refine/new/context/defer, 등록·qualification·검색·픽셀·활성화 계획 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md), [keyword-routes.json](keyword-routes.json) | 복원된 340개 완결 용어의 경로. 미연결 외형 65개 포함 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md), [semantic-cards.json](semantic-cards.json) | 138개 카드의 보이는 성분·소유자·접점·혼동·gate·한계 |
| [candidate-drafts.json](candidate-drafts.json) | 같은 138개 카드의 한영 후보 초안. loader/CID/RID/proof가 아님 |
| [context-distinctions.json](context-distinctions.json) | 원문 문맥 160개와 보충 12개. positive visual 검색 입력이 아님 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 기존 24개 원문·조건·효과·binding의 구체적 비교 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 소스와 binding의 full snapshot·해시 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | authored 후보 20,871개/연결 15,839개 읽기 시점 감사. 실제 검색 아님 |
| [SOURCES.tsv](SOURCES.tsv), [sources.json](sources.json) | 외부 26출처의 접근 범위·지원 의미·한계 |
| [EVALUATION-PLAN.md](EVALUATION-PLAN.md), [evaluation-cases.json](evaluation-cases.json) | 206사례/412한영 질의, NOT_RUN. 원문 smoke와 자연어를 분리 |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 초기 12장면 × 2조건 24장 계획. 현재 생성 0장 |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 참조 원문 잘림, 검색 발췌, timeout/404, 도판 미검토 |
| [BASELINE.json](BASELINE.json), [RUNTIME-CHECK.json](RUNTIME-CHECK.json) | 시작 상태·보호 해시, 읽기 전용 runtime 확인 |
| [VALIDATION.json](VALIDATION.json), [SHA256SUMS](SHA256SUMS) | 패키지 참조/그래프/출처/상태/해시 검사. 내용 진실·이미지 품질 검사와 별개 |

340개 용어를 모두 독립 사전에서 검증한 것은 아니다. 138개 카드와 후보 초안은 같은 대상을 세므로 합산하지 않는다. 장면 설계는 연구자의 제안이고 출처는 그 개념군을 지원한다.

현재 결과: 연구 자료 작성 및 로컬 무결성 검사. 운영 소스/인덱스 등록, 검색 평가, 이미지 생성, 설치 활성화, commit/push는 수행하지 않았다. 런타임 확인은 0 image calls / 0 source writes의 읽기 전용 검사다.

연구 파생 자료 재생성:

    python3 docs/research-evidence/photo-prompt/espionage-20261023/build_research.py
    python3 docs/research-evidence/photo-prompt/espionage-20261023/validate_research.py

build_research.py는 이 폴더의 파생 자료만 쓴다. audit_corpus.py는 현재 source를 다시 읽고 이 폴더의 감사 스냅샷을 **덮어쓴다**. 후속 구현 뒤 옛 감사 증거를 보존하려면 먼저 별도로 복사해야 한다. validator는 운영 파일을 수정하지 않는다.

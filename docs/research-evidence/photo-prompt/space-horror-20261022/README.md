# 스페이스 호러 리서치 패키지

2026-10-22. 참조 대화의 **핵심 180항목·보조 어휘 20개**, 작품 8개와 조합 8개를 바탕으로 작성했다. **상세 연구와 반영 계획까지 완료한 상태**이며 운영 데이터 등록이나 이미지 품질의 완료를 뜻하지 않는다.

먼저 [연구 보고서](RESEARCH.md), 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|12개 주제의 근거·과학/허구 구분·데이터 보완 결론|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|reuse/refine/new/context/defer, 예정 파일, 연결/효과 검토, 검색·이미지 평가, 설치·롤백|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [JSON](keyword-routes.json)|200개 전체 경로: still 48·proxy 29·sequence 22·context 79·nonvisual 22|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [JSON](semantic-cards.json)|64개 구체 장면: 한영·소유자·방향 관계·혼동·주장 한계·출처·211개 관계 gate|
|[candidate-drafts.json](candidate-drafts.json)|61개 후보 초안. V41·V47·V61은 문맥 단서로 보류; V45·V56·V57은 도상/물리/투영 검토 선행|
|[adoption-matrix.json](adoption-matrix.json)|64개 카드별 잠정 reuse/refine/new/context/defer와 실제 기존 CID 이웃·반영 전 필수 검토|
|[CONTEXT-DISTINCTIONS.md](CONTEXT-DISTINCTIONS.md) / [JSON](context-records.json)|20개 개념군의 문맥·인과·질병·의식·동의·혈연·시간·감각 경계|
|[SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md)|작품 8개 조사 범위와 조합 8개의 목표·갈등·가시 관계·대안·남은 서사|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|기존 후보·조건·효과·연결의 구체적인 재사용/분리 판단|
|[CORPUS-AUDIT.json](CORPUS-AUDIT.json) / [기존 원문 40개](existing-source-snapshots.json)|19,801후보·14,246연결·67모듈의 지정 필드 어휘 진단; 실제 검색 아님|
|[SYNONYM-NEIGHBORS.json](SYNONYM-NEIGHBORS.json)|추가 18개 표기 검사와 hair lock/air lock·포장 진공·산호 군체 등 오탐|
|[sources.json](sources.json) / [TSV](SOURCES.tsv)|36개 출처 기록: 본문/초록/소개 등 29·검색 발췌 5·접근 실패 2|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md)|참조 대화 복원·접근 실패·원전 미독·남은 심화 조사 범위|
|[평가 입력 TSV](EVALUATION-CASES.tsv) / [JSON](evaluation-cases.json)|148사례·296개 한영 질의, 모두 NOT_RUN; 독립 holdout 아님|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|12장면 × 3 arms × 독립 반복 2회 = 72회 생성 제안, NOT_RUN|
|[BASELINE.json](BASELINE.json) / [PRESERVATION.json](PRESERVATION.json)|시작 HEAD·dirty·보호 파일 해시와 종료 시점 drift 관찰|
|[RUNTIME-CHECK.json](RUNTIME-CHECK.json)|선택 설치본의 의존성·recorder 읽기 전용 검사; 신규 자료의 운영 반영 아님|
|[RUNTIME-OBSERVATION.json](RUNTIME-OBSERVATION.json)|조사 스냅샷 이후의 manifest 모듈 추가와 설치 선택자 비교|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|연구 파일 구조·참조·그래프·범위·해시 검증 결과|

64개 카드와 61개 초안의 수는 중첩된다. 211개 gate는 실제 관찰 횟수가 아니다. 원문 200개 각각을 독립 사전으로 검증한 것은 아니며 출처가 지원하는 정의/작품 문맥과 저술한 시각 실현을 분리했다. 의식·인과·강압·혈연·시간·실제 과학 측정을 단일 사진으로 입증하지 않는다.

재생성/검증:

```sh
python3 docs/research-evidence/photo-prompt/space-horror-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/space-horror-20261022/build_evaluation.py
python3 docs/research-evidence/photo-prompt/space-horror-20261022/build_adoption_matrix.py
python3 docs/research-evidence/photo-prompt/space-horror-20261022/validate_research.py
```

생성기는 이 연구 폴더에만 쓴다. `audit_corpus.py baseline|audit|preservation`은 현재 소스를 읽고 이 폴더의 관찰 증거를 새로 쓴다. 향후 운영 소스가 달라지면 기존 연구 시점 증거를 먼저 보존하고 다른 파일명/디렉터리에 새 기준을 기록해야 한다. 이미지·임베딩 API·운영 등록·설치 활성화·커밋·push는 이번에 수행하지 않았다.

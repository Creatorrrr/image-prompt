# 스페이스 오페라 리서치 패키지

2026-10-23. [연구 보고서](RESEARCH.md)와 [반영 계획](IMPLEMENTATION-PLAN.md)을 먼저 읽으면 된다. 참조 대화에서 복원한 291항목·9작품·3인과 조합을 바탕으로 상세 연구와 후속 데이터 반영 설계를 작성했다. 운영 데이터 강화가 이미 설치·검증되었다는 뜻은 아니다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|14개 연구 축의 근거·과학/허구·가시/비가시 구분·현재 공백|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|카드별 심사·예정 파일·native 조건/효과·분리 인덱스·검색/픽셀·설치/회복 계획|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [JSON](keyword-routes.json)|291개 전체 경로: still 45·proxy 69·sequence 34·context 118·nonvisual 15·versioned 10|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [JSON](semantic-cards.json)|72카드·197방향 관계. 한영 장면·성분·소유자·혼동·주장 한계·출처·가시 gates|
|[candidate-drafts.json](candidate-drafts.json)|위 카드 중 후보 초안 65개. runtime CID·native facts/conditions/effects 승인이 아님|
|[CONTEXT-DISTINCTIONS.md](CONTEXT-DISTINCTIONS.md) / [JSON](context-records.json)|26개 문맥 구분. 선정적·폭력적 원문 항목도 보존|
|[SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md)|작품 9개 조사 범위와 원문 인과 조합 3개·전체 장면 대안|
|[SOURCE-LEDGER.md](SOURCE-LEDGER.md) / [sources.json](sources.json) / [TSV](SOURCES.tsv)|45출처: 본문/해당 구간 41·검색 발췌 3·본문 실패 1|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|기존 의미·조건·효과·연결과의 구체 비교 및 어휘 오탐|
|[CORPUS-AUDIT.json](CORPUS-AUDIT.json)|20,054후보·14,687연결·75모듈의 지정 긍정 필드 진단. 실제 검색 아님|
|[원문 이웃](existing-source-snapshots.json) / [구조 이웃](topology-neighbors.json)|29개 원문 선택과 8개 구조 이웃. 중첩 가능. full record·연결·해시|
|[adoption-matrix.json](adoption-matrix.json)|reuse 3·refine 11·new 51·context 3·defer 4의 잠정 판단. new도 전체 의미 심사 전 제안|
|[평가 사례 TSV](EVALUATION-CASES.tsv) / [JSON](evaluation-cases.json)|개발 65·경계 20·일반 대조 12 = 97사례/194한영 질의. 전부 NOT_RUN|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|12장면×3 arms=36장 제안, 조건부 확인 반복 최대 36장. 현재 생성 0장|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md)|원 대화 잘림/복원·자료 미독·접근 실패·주장 경계·조사 분담과 자기 검토 범위|
|[BASELINE.json](BASELINE.json) / [PRESERVATION.json](PRESERVATION.json)|시작 원본/dirty 해시와 종료 시점 변화 관측|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|연구 자료의 ID·참조·관계·원문 해시·비활성 상태·링크·체크섬 검사|

72카드와 65초안은 중첩된다. 원 조사자 메모의 카드 24개도 최종 카드와 중첩하므로 합산하지 않는다. 197 gates는 관찰 횟수가 아니다. Ringworld 상세·coilgun 비교·glassing 범위·ectogenesis 원전은 채택 전 보완이 필요하다. 291개 정의 모두를 독립 원전으로 검증하지 않았고 구체적인 장면 기하는 저술 제안이다.

종료 관측에서 HEAD가 `be52bda6`에서 `9b654b63`으로 바뀌었고 보호한 기존 파일 중 `references/maintenance.md` 한 개의 내용 변화가 있었다. 이는 동시 작업의 관측 기록이며 이 연구가 commit하거나 해당 파일을 수정했다는 뜻은 아니다. 후속 구현 전에 최신 원본으로 다시 기준을 고정해야 한다.

재생성과 검증:

```sh
python3 docs/research-evidence/photo-prompt/space-opera-20261023/build_research.py
python3 docs/research-evidence/photo-prompt/space-opera-20261023/validate_research.py
```

생성기는 이 폴더의 파생 연구 자료만 쓴다. `audit_corpus.py baseline|audit|preservation`은 읽기 전용으로 현재 원본을 조사해 **이 폴더의 관측 기록을 새로 쓴다.** 후속 구현 뒤 현재 연구 시점의 baseline/audit을 조용히 덮어쓰지 말고 별도 이름으로 새 관측을 남겨야 한다. 운영 등록·임베딩 API·이미지 API·인덱스 재생성·설치·commit·push는 이번에 수행하지 않았다.

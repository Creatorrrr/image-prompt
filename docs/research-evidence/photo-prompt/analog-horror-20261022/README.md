# 아날로그 호러 리서치와 데이터 반영 계획

2026-10-22. 먼저 [상세 리서치](RESEARCH.md)를, 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

핵심은 기록 형식·물리 매체·재생 장비·표시 래스터·신호 결함·디지털 전송을 구분하고, 기록의 신뢰가 깨지는 관계를 데이터로 표현하는 것이다. 장르 라벨로 VHS 노이즈·괴물·피해를 한꺼번에 추가하지 않는다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|주요 조사 결과, 기술 혼동 경계, 서사·비가시·인접 장르의 반영 판단|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|재사용→의미 정정→최소 신규→독립 index→검색/픽셀 검증→설치·롤백의 순서와 완료 조건|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|원 대화 200개 용어 전체의 처리 경로. 가시/proxy 56·혼합 40·문맥 64·시간 7·비시각 15·판본 18|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|78개 카드: 성분·owner·방향 관계·한영 표현·혼동 경계·주장 한계·출처·픽셀 gate 제안|
|[candidate-drafts.json](candidate-drafts.json)|비운영 후보 초안 72개. 세부 근거가 필요한 6개 카드는 보류. native CID/RID·승인·선택 결과가 아님|
|[SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md)|원 대화의 8개 창작 조합을 보존한 장면 설계·관찰 한계|
|[SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json)|38개 URL의 접근 수준·읽은 범위·뒷받침하는 주장. 33개 본문 부분 검토, 5개 제한 접근|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|19개 기존 전체 source 표본의 재사용·정정·다의어 거절 판단|
|[CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json)|19,801개 후보의 제한된 필드 어휘 진단. 실제 retrieval/rank/qualification은 아님|
|[existing-source-mapping.json](existing-source-mapping.json)|위 19개 source와 직접 binding의 전체 snapshot·원문 해시·연구 판단|
|[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)|80개 사례/160개 한영 질의: 양성 24·경계 32·일반 대조 16·비가시 대조 8, 모두 NOT_RUN|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|12개 대표 사례 × 3 arms × 2회 = 최대 72장 1차 비교 계획, NOT_RUN|
|[ACCESS-LIMITS.md](ACCESS-LIMITS.md)|대화 복원·원전 확인 공백·접근 실패·출처 등급·실행 한계|
|[BASELINE.json](BASELINE.json) / [BASELINE-DRIFT.json](BASELINE-DRIFT.json)|시작 source 기준과 완료 시점의 외부 변화 관찰. 동시 작업은 되돌리지 않음|
|[RUNTIME-CHECK.json](RUNTIME-CHECK.json)|설치된 recorder·의존성의 read-only 점검 pass. 연구 데이터의 운영 채택을 뜻하지 않음|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|키워드·graph·출처·slot·초안·평가 계획·문서 링크·해시의 구조 검사|

200·78·72는 중첩되는 수치이며 합산하지 않는다. 원 용어 200개의 독립 정의 검증, 운영 후보의 순증 수, 실제 이미지 품질 향상을 완료했다고 주장하지 않는다. 6개 보류 카드는 VHS-C/어댑터, 특정 시험표, 텔레텍스트 격자, 형상 지각, 애니매트로닉 기구 접점, 정확한 모스 부호다.

운영 source·index 등록, embedding, 실제 검색 평가, candidate 선택, 이미지 생성, native 픽셀 검토, 설치 전환, 커밋·push는 이번에 수행하지 않았다.

재생성·검증:

```sh
python3 docs/research-evidence/photo-prompt/analog-horror-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/analog-horror-20261022/validate_research.py
python3 docs/research-evidence/photo-prompt/analog-horror-20261022/validate_research.py --check-sealed
```

`build_research.py`는 이 폴더의 연구 파생물만 쓴다. `audit_corpus.py`는 운영 source를 읽고 **이 폴더의 snapshot을 새로 쓰므로**, 후속 구현 뒤에는 옛 증거를 별도 보존한 다음 실행한다. 검증기는 source drift를 승인하지 않으며 실제 구현 전 재기준화를 요구한다.

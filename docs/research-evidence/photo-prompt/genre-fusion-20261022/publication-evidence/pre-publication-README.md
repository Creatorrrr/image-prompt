# 장르 조합 시각 의미·후보 데이터 리서치

2026-10-22. Dying Earth × New Weird × Cozy Fantasy × Cosmic Horror.

**후속 반영·실험 완료:** 시각 의미 96개·긍정 후보 84개·진단 12개·binding 168개를 실제 source와 설치 검색 세대에 반영했다. 한영 검색 136개와 회귀 테스트 97개를 실행하고, 최신 스킬·첨부 reference로 독립 arm 3개에서 이미지를 각각 한 장 생성했다. 복합 관계 전체 통과는 0/3이며 신규 후보의 완전 채택도 0이다. [반영·검증 결과](INTEGRATION-RESULTS.md), [이미지·프롬프트·판정](IMAGE-TEST-REPORT.md), [정확한 경로·해시](IMAGE-TEST-RESULTS.json)를 먼저 확인한다.

아래 표와 선행 VALIDATION의 NOT_RUN은 **리서치 단계 종료 당시 기록**이다. 후속 실행의 최신 상태는 위 결과와 INTEGRATION-VALIDATION.json을 따른다. 원래 README와 checksum은 integration-evidence에 보관했고, 현재 SHA256SUMS는 후속 산출물을 포함한 파일 무결성 목록이다.

**핵심 제안:** 장르 표식을 늘리기보다 낡은 세계를 유지하는 사람·낯선 몸·도구·시설·자원의 구체적인 관계를 보강한다. 환대·수선·분배·돌봄의 순간과, 그 장면만으로 확정할 수 없는 시간·신앙·권리·동의·우주적 해석을 구분한다.

처음에는 [RESEARCH.md](RESEARCH.md), 다음에는 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 읽으면 된다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|문헌 구분·8개 데이터 영역·현재 corpus 진단·한계|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|원 대화 150개 번호 전부의 경로·관련 카드·혼동 경계|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|96개 카드: 소유자·방향 관계·출처·가시성·217개 관계 gate|
|[candidate-drafts.json](candidate-drafts.json)|카드에서 구체화한 한영 후보 초안 84개. 96개와 합산하지 않음|
|[SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md)|원 대화 12개 조합 표현의 실제 장면 제안과 남는 서사 경계|
|[SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json)|외부 32개 자료의 URL·실제 읽은 범위·지원 의미·접근 제한|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)|기존 source 19,179개 지정 어휘 진단과 구체적 재사용/정제 판단|
|[existing-source-mapping.json](existing-source-mapping.json)|선택 CID 24개의 원문·binding·조건/effect·해시 스냅샷. 자격 승인 아님|
|[EVALUATION-CASES.tsv](EVALUATION-CASES.tsv)|68개 한영 사례: 개발32·경계16·일반12·비가시8, 질의136개, NOT_RUN|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|첫 12군×3 arm = 36장 비교 제안, NOT_RUN|
|[BASELINE.json](BASELINE.json)|시작 HEAD·기존 dirty 목록·추적 파일 6,139개 hash|
|[RUNTIME-OBSERVATION.json](RUNTIME-OBSERVATION.json)|현재 installed config/source 선언의 읽기 전용 관찰. 실행 자격·검색 증거 아님|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|패키지 참조·수량·graph·문맥 분리·snapshot/원본 drift 검사|

32개 자료는 원전 전체 32권을 읽었다는 뜻이 아니다. 출판사 소개·장 요약·공식 인덱스 본문만 읽은 자료, 403/확인 화면 때문에 직접 열람이 제한된 자료를 따로 표시했다. 150개 모든 정의를 독립 사전에서 검증하지 않았다. 초안의 구체적인 물건·기하·동작은 새로 저술한 선택적 제안이며 인용한 작품의 정본 디자인이 아니다.

리서치 단계 종료 당시 runtime 등록·인덱스 생성/게시·임베딩·검색·이미지 생성·픽셀 평가·사용자 수용·커밋/푸시는 미실행이었다. 후속 데이터 반영·실행은 INTEGRATION-RESULTS를 따른다. 사용자 수용·커밋/푸시는 여전히 미실행이다. 선행 구조 검증의 drift 결과는 VALIDATION, 후속 보존 검증은 integration-evidence/protection-final.json을 따른다.

재생성·확인:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/genre-fusion-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/genre-fusion-20261022/validate_research.py
```

두 명령은 이 폴더의 문서/연구 JSON과 검증 결과만 쓴다. `audit_corpus.py`는 현재 source를 다시 읽어 **스냅샷 증거를 새로 쓰므로**, 구현 후 기존 증거를 덮지 말고 별도 단계 폴더로 보존해야 한다. 어떤 스크립트도 모델·이미지·검색 API나 운영 등록을 실행하지 않는다.

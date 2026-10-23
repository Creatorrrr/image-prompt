> 최신 결과와 저장소 내 이미지·프롬프트는 [발행 안내](PUBLICATION.md)와 [2차 재검토 보고서](full-review-r2/REPORT.md)를 참조한다. 아래 집계는 1차 연구 당시 기록이다.

> 후속 데이터 반영 및 독립 이미지 테스트는 [INTEGRATION-AND-IMAGE-TESTS.md](INTEGRATION-AND-IMAGE-TESTS.md)에 기록한다. 아래 내용은 연구 단계 snapshot이다. 원본 README/SHA256SUMS/VALIDATION은 integration-evidence/research-stage-*로 보존했다.

# 궁중물·궁정물 시각 의미·후보 데이터 리서치

2026-10-23. [궁중물 용어 조사](https://chatgpt.com/c/6adb17fb-6238-83e8-a54e-d5e467110649)를 바탕으로 상세 조사와 후속 반영 계획을 작성했다. **이 폴더는 연구 산출물이며 운영 후보/검색/생성 개선이 완료됐다는 뜻은 아니다.**

먼저 [상세 리서치](RESEARCH.md), 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

| 산출물 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) |16개 논점: 시대·지역·복식/부품·포즈·접근/노동·비가시 문맥·기존 데이터 판단 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | P0/P1/P2, 실제 반영 파일,149-slot 적합성·효과·조건·native/인덱스·검색·픽셀·게시/롤백 기준 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 대화34개 번호 장·표622행+표 밖 초야권1항목; 정확한 정의 조사 보류도 보존 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) |88개 카드: 형태61·저술한 관계 장면12·문맥15; 주인·방향 관계·혼동·근거·가시성 gate |
| [candidate-drafts.json](candidate-drafts.json) | 위 카드의 부분집합인73개 한영 선택적 초안; 실제 CID/binding 없음 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [existing-source-mapping.json](existing-source-mapping.json) |20,871개 source의 지정 어휘 일치81개 snapshot,19개 기존 CID의 구체 처리 판단 |
| [sources.json](sources.json) |40개 출처의 실제 접근 깊이·검토 지점·지원 범위와 제약 |
| [SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md) | 원 대화8개 조합 예별 두 장면 대안과 남는 경계 |
| [evaluation-cases.json](evaluation-cases.json) / [CONFUSION-CASES.tsv](CONFUSION-CASES.tsv) | 개발/문맥88개+혼동24쌍48개 case=136개; 한영272개 query 설계, 실제 검색 NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 최초8군×baseline/보강2팔=16장 제안; 생성·픽셀 NOT_RUN |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) | 기준 HEAD·보호 hash·기존 dirty 상태 및 구조/보존 검사 |
| [SHA256SUMS](SHA256SUMS) | 연구 파일 바이트 무결성; 역사적 사실성이나 생성 품질 인증 아님 |

40개 출처 중37개는 지정 본문 구절을 읽었고,2개는 검색 요약에 제한되며,1개는 링크만 확보하고 open 실패했다. 본문 확인도 완독·모든 사진·모든 사료 검증이 아니다. 직접 본 실물 사진은 서울공예박물관 당의의 펼친 앞면뿐이다. 의미 카드40개는 추가 원전/도판 고증이 필요하다. 표제 연결이 없는312행은 분야 안내를 남기고 정확한 개별 정의 검증을 보류했다. 카드 표제 연결 역시 어휘 seed이며 역사적 동의어 승인으로 간주하지 않는다.

이번에 완료한 것은 조사·현재 source의 읽기 전용 진단·연구 카드/초안·반영 및 평가 설계·연구 구조 검증이다. **운영 source/manifest 변경, native 자격, 인덱스/embedding/실제 검색, 설치 활성화, 프롬프트 실행/이미지 생성/픽셀 평가, 사용자 수용, 커밋/푸시는 실행하지 않았다.** 공유 작업 트리의 다른 변화 여부는 VALIDATION의 관찰 결과와 구분한다.

재생성/검증 명령:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/court-palace-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/court-palace-20261023/build_adoption.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/court-palace-20261023/validate_research.py
```

두 build는 이 폴더에만 쓰며 원 대화 및 corpus snapshot은 다시 수집하지 않는다. validator는 현재 보호 파일과 baseline의 차이를 관찰하며 runtime·검색·이미지 API를 호출하지 않는다. 후속 구현은 새로운 증거 폴더에서 시작하여 연구 원본을 보존한다.

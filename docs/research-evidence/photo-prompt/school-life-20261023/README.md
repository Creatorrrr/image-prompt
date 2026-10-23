# 학원물 시각 의미·후보 데이터 리서치

2026-10-23. [학원물 용어 정리](https://chatgpt.com/c/6adafc0d-dc50-83ee-b22e-eec239f83ca7)의 **210개 키워드 전체**를 대상으로 상세 조사와 반영 계획을 작성했다.

핵심 보강 방향은 **학교 공동체의 구체 활동·소유 관계·혼동 경계**다. 학생회 회의, 동아리 모집, 공동학습, 배식, 청소, 계주, 기숙 생활 등을 선택 가능한 구조로 확장하고, 인물 신분·인기·선후배·동의·학대 의도·시간 반복·소리처럼 한 장으로 증명할 수 없는 의미는 문맥으로 유지한다.

먼저 [상세 리서치](RESEARCH.md), 다음으로 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

|산출물|내용|
|---|---|
|[RESEARCH.md](RESEARCH.md)|14개 논점, 출처 판단, 문화/시대/장르 경계, 추가 고증 범위|
|[IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)|P0/P1, 실제 변경 경로, 재사용 심사, source/role/검색/픽셀/설치/발행 단계|
|[KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json)|원 대화 14범주·210항목의 전체 연결|
|[VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json)|90카드: 가시 50·대리 장면 16·문맥 22·시간 1·음향 1|
|[candidate-drafts.json](candidate-drafts.json)|가시/대리 카드에서 파생한 한영 선택적 실현 66개; runtime import 불가|
|[sources.tsv](sources.tsv) / [sources.json](sources.json)|외부 25건: 지정 본문 22·공식 색인만 1·접근 실패 2; 참조 대화 별도|
|[CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [corpus-snapshot.json](corpus-snapshot.json)|81모듈·20,341 CID의 좁힌 어휘 조사, 기존 CID 10건 전체 원문·조건·효과·binding 및 triage|
|[WORK-EXAMPLES.md](WORK-EXAMPLES.md)|원 대화의 작품 조합 13사례와 독립 확인/미확인 범위|
|[development-cases.json](development-cases.json)|카드 파생 한영 개발 scaffold 90개, 180질의; 독립 holdout 아님|
|[BOUNDARY-CASES.tsv](BOUNDARY-CASES.tsv)|32개 한영 경계/일반 사례, 총 64질의; 실제 검색 미실행|
|[PIXEL-PLAN.md](PIXEL-PLAN.md)|첫 12사례×3 arms=36장 비교 제안; 이미지 생성·픽셀 리뷰 미실행|
|[BASELINE.json](BASELINE.json)|조사 도중 HEAD·기존 dirty/untracked와 보호 대상 212개 파일 SHA|
|[VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS)|참조·owner graph·문맥 분리·범위·링크·snapshot 및 보호 파일 비교|
|[WORKSPACE-OBSERVATIONS.md](WORKSPACE-OBSERVATIONS.md)|공유 source의 별도 변동 6개 파일과 통합 전 재기준화 필요|

66개 초안은 90개 카드의 부분집합이다. 카드·키워드·초안 수를 더해 실제 신규 후보 수나 품질 검증 수로 세지 않는다. 제안 구도는 연구자의 저술이며 source가 모든 geometry를 증명한 것은 아니다. 외부 문서 전체 완독·작품 전편 감상·원 소장품/미디어 픽셀 검토도 수행하지 않았다.

완료 범위는 **문헌/공식 소개 조사, 기존 source의 읽기 전용 진단, 연구 카드/실현 초안, 반영 계획, 연구 패키지 구조 검증**이다. 운영 source/manifest 변경, native qualification, 실제 검색/embedding/인덱스 빌드·verify, installed 활성화, 이미지 생성/픽셀, 사용자 수용, 커밋/푸시는 수행하지 않았다. 공유 작업 트리의 변동은 VALIDATION의 drift로 별도 기록한다.

최종 연구 구조 검사는 23/23 통과했다. 조사 도중 기존 후보 모듈 5개와 manifest의 별도 변경을 관찰했으므로 최종 상태는 `STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE`이다. 실제 반영 전 최신 source로 다시 심사하며 조사 당시 스냅샷은 보존한다.

재생성·검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/school-life-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/school-life-20261023/validate_research.py
```

`audit_corpus.py`는 보존된 corpus snapshot이 있으면 중단한다. 후속 통합 후에는 별도 단계 폴더에서 새 evidence를 수집하며 이 연구 당시의 snapshot이나 baseline을 덮어쓰지 않는다. SHA256SUMS는 파일 바이트 무결성 기록이며 자료의 사실성·의미·검색·픽셀의 인증이 아니다.

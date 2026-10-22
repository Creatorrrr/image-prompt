# 이번 데이터의 main 게시 범위와 검증

2026-10-22. 기준 main `8a67fe575092d46fecc4b80d530cf36e74e92685`에 이번 Decadent Aesthetic × Domestic Thriller × Splatter Horror 자료만 더했다. 기존 main의 원문과 연결, catalog, policy를 보존했고, 다른 작업의 미커밋 source·코드·설치 설정은 포함하지 않았다.

|항목|게시용 main 구성|선행 로컬 실험 snapshot|
|---|---|---|
|전체 후보|19,184|19,383|
|긍정 후보|18,950|19,115|
|진단·문맥 후보|234|268|
|선택적 연결|13,176|13,500|
|이번 추가|86 긍정 + 22 진단, 172 연결|동일한 CID·원문|

수량 차이는 이번 자료 누락이 아니다. 선행 실험에는 다른 미커밋 후보·원문 수정이 포함됐다. 게시에서는 기준 main의 후보 19,076개와 연결 13,004개를 모두 유지한다. 연구의 기존-source mapping과 생성 실험 기록은 해당 시점의 로컬 snapshot 증거이며 게시 corpus의 모든 이웃 CID가 같다는 주장은 하지 않는다.

- 시각 의미 카드 108개, keyword route 189개, 방향 관계 gate 252개를 원문 그대로 게시한다.
- 게시 source SHA-256: `c990e051930d5ec1dcc37c6e12bf25674f3cdecf6856be696fcc8cecb86e949c`
- 게시 lazy-index layout: `cccc6af1b9ec15898fd9efa6183fd33709197cdcfc039150623fcbaabaa506dd`
- 전체 source/index closure 검증 PASS, dictionary 오류 0개, 기존 관련 회귀 테스트 242개 PASS.
- 기존 일치 벡터 18,864개 재사용; 로컬 pinned EmbeddingGemma에서 새 문서 86개 생성, cache hit 0개. 외부 embedding API 호출 없음.
- 새로운 source의 native approval은 여전히 false다. 검색 등록과 whole-source 채택 자격을 구분한다.

`retrieval-runtime.json`은 기준 main의 H-F2 `13d885356aa63c72ec29b0409e8cce23469b3cbc0f9c0adbaf840ff7584d70db`를 유지하며 native CURRENT를 쓰지 않는다. 선행 이미지 실험은 별도 로컬 설치 세대 `3633746531a13fadf48051978d5b5d21bbbcaa0cfd976edf18270835f6d4ae73`에서 실행됐다. 기본 체크아웃의 이 선택과 기존 미커밋 파일 바이트를 보존한다. source/index 게시와 installed release 활성화는 별개다.

원래 연구·통합 보고서와 `SHA256SUMS`, `INTEGRATION-SHA256SUMS`는 수정하지 않았다. 시점별 수치와 NOT_RUN 표기를 과거 실험의 현재 성공으로 바꾸지 않는다. 이번 게시 검증은 [publication-evidence](publication-evidence/) 및 `PUBLICATION-SHA256SUMS`를 따른다.

## 보존한 실제 생성 이미지

세 번의 실제 도구 호출 중 B·C 두 장이 반환됐고 A는 출력 moderation으로 차단됐다. 이미지 재생성·수정 없이 원본 바이트를 아래에 복사했다. 전체 사전 기준은 B 7/7 통과, C 5/6 부분 미충족이다. 신규 source 채택은 세 arm 모두 0이므로 이번 데이터가 이미지 결과를 개선했다는 인과 결론은 내리지 않는다. 자세한 원래 판단은 [INTEGRATION-RESULTS.md](INTEGRATION-RESULTS.md)와 [IMAGE-TEST-RESULTS.json](IMAGE-TEST-RESULTS.json)을 따른다.

![Arm B: 사전 기준 7/7 통과](publication-evidence/images/arm-b.png)

![Arm C: 사전 기준 5/6, 하체 지지 상태 관찰 불가](publication-evidence/images/arm-c.png)

임시 워크트리의 ignored 모델은 기본 체크아웃에 존재하는 동일 hash 파일의 독립 복사본이고 Python 링크는 기존 runtime을 가리킨다. 고유 증거 파일은 모두 게시하거나 기본 체크아웃에 보존한다.

이 검증 뒤 커밋·origin/main pull·병합·push·실제 원격 SHA 확인을 수행한다. 결과는 Git 이력과 기본 체크아웃의 `generated/maintenance/decadent-domestic-splatter-20261022/publication-main/`에 별도 기록한다. 이 문서는 아직 실행하지 않은 Git 동작을 성공으로 주장하지 않는다.

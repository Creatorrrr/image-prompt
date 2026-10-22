# LitRPG 연구 패키지

[Git 발행 범위와 검증](PUBLICATION.md)은 main 기준의 원문 보존, 결합 인덱스, 휴대 가능한 이미지 실험 archive와 설치 버전 경계를 설명한다.

리서치 후 사용자 요청에 따라 의미 카드 78개(시각 실현 60개·진단 18개), 바인딩 128개를 원문과 설치된 검색 버전에 반영했다. 개발 검색 48개와 관련 회귀 검사 68개를 마쳤다. 독립 서브에이전트 3개가 첨부 사진으로 각 1회 생성했고, 핵심 주제 관계는 2개 통과·1개 부분 실패, 정확한 동작/전체 끝점까지 포함한 전체 테스트는 0/3 통과다. [반영 및 독립 이미지 실험 결과](INTEGRATION-RESULTS.md)가 현재 단계의 결과 문서다. 초기 연구 계획의 이미지 6개 제안과 이후 요청받은 실제 독립 실험 3개는 구분한다.

- [리서치 본문](RESEARCH.md): 판단·기능별 의미·매체 사례·증거 한계.
- [반영 계획](IMPLEMENTATION-PLAN.md): 기존 소스 재사용, 제안 파일, 우선순위, 검증·발행 단계.
- [전체 키워드](KEYWORD-ATLAS.md): 참조 대화 용어 255행과 보조 42행, 총 297개 경로.
- [시각 의미 카드](VISUAL-CARDS.md): 78개. 직접 관계 22 / 표시 내용 38 / 문맥 14 / 연속 증거 4.
- [후보 초안](CANDIDATE-ATLAS.md): 전체 양언어 의미와 조건을 가진 60개 검토 초안.
- [현재 코퍼스 대조](CORPUS-FINDINGS.md): 19,813개 레코드의 제한된 어휘 감사와 기존 LitRPG 실현 8개 상세 비교.
- [출처](SOURCES.md): 접근 제한을 구별한 27개 기록. 작품별 모든 화면을 검증했다는 뜻이 아니다.
- [평가 계획](EVALUATION-PLAN.md): 미실행 평가 입력 48개와 후속 이미지 장면 6개.
- [초기 연구 검증](VALIDATION.json): 당시 연구 내부 참조·관계 끝점·개수 검사와 운영 파일 변경 관찰 기록.
- [데이터 반영 검증](integration-evidence/DATA-VALIDATION.json): 원문 보존·설치·인덱스·개발 질의·관련 회귀 검사.
- [이미지 실험 집계](integration-evidence/IMAGE-TEST-SUMMARY.json): 실제 호출·고정 설치 세대·참고 사진·원본·사전 기준 일치와 실패를 포함한 픽셀 결과.

기계 판독용 자료는 `reference-register.json`, `keyword-routes.json`, `semantic-cards.json`, `candidate-drafts.json`, `sources.json`, `evaluation-cases.json`이다. `research_data.py`와 `build_research.py`가 연구 자료를 재생성하고 `create_evaluation.py`가 평가 입력을 만든다. `build_research.py --keep-corpus-snapshot`은 기존 코퍼스 스냅샷을 보존하고 연구 카드만 다시 만든다. 옵션 없는 실행은 현재 코퍼스를 다시 읽으므로 과거 audit 파일을 먼저 보존해야 한다.

초기 연구 검사 중 운영 파일 3개의 동시 변경을 관찰했고 [WORKSPACE-DRIFT.json](WORKSPACE-DRIFT.json)에 이전·관찰 hash를 보관했다. 후속 반영은 최신 원문과 시작 시점 설치 스냅샷을 다시 대조한 뒤, 다른 미발행 작업 12개를 보존하면서 별도 검증된 설치 버전을 만들었다. 정확한 차이와 현재 변경 범위는 반영 결과 문서를 따른다.

`native_approval:false`와 `partial_is_fail`/`UNOBSERVABLE_NOT_PASS` 경계를 유지한다. 초기 연구의 미등록 상태와 이후 실제 검색 등록을 구분한다. 유효한 JSON·출처 링크·어휘 일치만으로 원전 적격성 승인·검색 노출·채택·이미지 의미 충족·사용자 승인이 생기지 않는다.

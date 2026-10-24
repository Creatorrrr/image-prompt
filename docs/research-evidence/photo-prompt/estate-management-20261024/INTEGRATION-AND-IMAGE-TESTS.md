# 영지물 데이터 반영과 독립 이미지 테스트

2026-10-24, Asia/Seoul. 이 문서는 최초 조사와 후속 데이터·이미지 실행을 구분한다.

## 반영한 데이터

| 항목 | 실제 반영 | 해석 범위 |
|---|---:|---|
| 시각 의미 카드 | 60개 | 관찰 요소·소유자·연결·혼동·출처·픽셀 기준 보존 |
| 문맥 진단 카드 | 20개 | 법적 권리·신분·역사·동의·시간을 시각 사실로 승격하지 않음 |
| 신규 선택형 시각 후보 | 22개 | 한영 완전한 실현 문장, 명시적 조건·effects·출처 |
| 보류 시각 진단 | 36개 | 추가 자료·도판 확인 전까지 긍정 검색에서 제외 |
| 문맥 진단 후보 | 20개 | 긍정 검색에서 제외 |
| 기존 완전한 후보 재사용 | 2개 | 포트컬리스와 파니에. 기존 원문·조건·effects 불변 |
| 선택형 역할 연결 | 56개 | 실제 역할 ID·semantic_role과 연결 무결성 확인 |
| 원 대화 표제 경로 | 374행 | 탐색용 연결. 복합 표제 전체의 정의 검증이나 자동 활성화 권한이 아님 |

소스 파일:

- [신규 후보·진단 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_estate_management_20261024.json)
- [선택형 역할 연결 모듈](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_candidate_estate_management_bindings_20261024.json)
- [시각 의미·출처·픽셀 관찰 sidecar](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_estate_management_semantics_20261024.json)
- [스킬의 영지물 참조 문서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/estate-management-semantics.md)

후보·연결 모듈은 corpus manifest에 등록했다. 의미 sidecar는 관찰 구조와
출처·보류 상태를 보존하며 그 자체로 검색 점수를 가산하지 않는다. 모든 새
긍정 후보는 선택형 자료다. 연구 그래프가 native 자격이나 사용자 요구를 만들지 않는다.
추가 고증이 필요한 구조를 완성된 역사 재현으로 취급하지 않는다.

## 검색 스냅샷과 검증 경계

동시 작업이 있는 기존 checkout 전체를 배포하지 않고, 시작 시 설치된 봉인
스냅샷에 이번 후보 78개와 연결 56개만 추가했다. 기존 후보 21,706개와 기존
역할·정책·연결은 보존했다. 그중 긍정 기본 인덱스는 기존 벡터 20,623개를
재사용하고 새 후보 22개만 계산했다. H-F2 문서는 기존 20,625개 벡터를
그대로 재사용하고 새 문서 22개를 추가했다. 순위 정책·커널은 바꾸지 않았다.

- 고정 H-F2 세대: `5eab1979465e7ed0627ab628e44c15d4686ddf633937d3e5e9990884488c1de1`
- 고정 native 세대: `21f5af297d9aba186bc9d41838bfcaf1c4787ee97c1d13f2105a21e38a8c6538`
- 설치 저장소: `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`
- 현재 canonical SKILL.md SHA-256: `f1b6e6356e76ad22abcdcbdf4ca0aa6543a65f50ed2692f57c45f24b6286a089`

세 테스트는 위 세대와 저장소를 명시적으로 고정했다. 이후 다른 작업이 갱신한
기본 런타임을 보존하며 이번의 동일한 후보·연결만 더한 후속 세대를 별도로 만들어 선택했다.
테스트 세대와 최종 기본 세대의 검증을 혼동하지 않는다. `CURRENT`를 직접 쓰지 않는다.
최종 선택 상태는 아래 “기본 런타임의 최종 반영”과 별도 설치 증거에 기록한다.

[반영 무결성 검사](integration-evidence/integration-validation.json),
[기존 정본 보존 검사](integration-evidence/canonical-source-validation.json),
[기본 인덱스 검사](integration-evidence/native-index-build.json),
[H-F2 전체 봉인 결과](integration-evidence/successor.json)에 실제 결과를 저장했다.
고정 설치본은 배포된 H-F2/native 검증도 통과했다. 유지보수 조회 12개 중 주제 조회 8개는 모두 목표 신규 후보가 1위로 노출됐고, 일반 대조 조회 4개에서는 이번 신규 후보가 노출되지 않았다. 이는 이 표본의 검색 결과이며 전체 정확도나 이미지 품질 지표가 아니다. 상세는 [조회 실행 결과](integration-evidence/runtime-probes.json)와 [설치 결과](integration-evidence/install.json)에 있다. 세 이미지의 실제 결과는 아래와 같다. 최초 연구의 192개
평가 사례는 계획이며, 이번에 모두 실행했다는 뜻이 아니다.

## 독립성과 참조 이미지

세 서브에이전트는 `fork_turns=none`으로 시작했다. 실제 사용자 요청과
이전 사용자 메시지의 영지물 주제, 참조 이미지 경로, 서로 다른 넓은 장면 범위만
전달했다. 각자 후보·연구 자료를 보기 전에 컨셉·기본 프롬프트·판정 기준을
작성하고 동결했다. 다른 에이전트의 프롬프트나 결과를 전달하지 않았다.
[검색 연결 전 상태와 해시](integration-evidence/pre-data-ready-freeze-proof.json)를 보존했다.
관리된 상태·해시는 절차적 증거이며 접근할 수 없는 내부 상태를 증명하지 않는다.

사용자는 무작위 컨셉 선정과 테스트 설계를 위임했다. 농업 점검·토지기록·공적 교류·주민 같은 구체적 장면은 작성자 통제 조건이다. 보수적으로 좁게 동결된 concept/subject/event 문구와 기계 감사의 통과를 사용자가 그 장면을 직접 요구했다는 증거로 재사용하지 않는다. 이 구분은 [실험 범위 검토](integration-evidence/experimental-scope-review.json)에 기록했다.

| 실험 | 독립적으로 선택한 컨셉 | 주요 사전 판정 기준 |
|---|---|---|
| A | 가동 중인 곡물 타작장 점검 | 관리자·현장 책임자·작업, 곡물 운반·건조 보관, 배수와 도면 대응 |
| B | 토지 경계 청원과 도면·장부 대조 | 두 청원자의 동일 구획 지목, 지도 경계·끝점과 장부 대응, 결정·기록 연결 |
| C | 공동 화덕에서 빵을 건네는 주민 만남 | 인물별 손·빵 접점, 화덕 작업과 주민 대기, 공동 생산·전달 관계 |

참조 이미지의 SHA-256은
`06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`이다.
얼굴·짧은 짙은 단발·앞머리의 외형 참조로 사용한다. 실존 신원·연령·배경·성격을
확정하지 않는다. 실제 도구에 첨부한 경로·해시·프롬프트와 출력 파일을 실험별로
기록한다. 화면의 법적 권리, 신분, 과거 수리, 최초성, 시간적 인과는 픽셀 통과 조건으로 삼지 않는다.

## 실행 결과

최신 canonical 스킬을 확인한 독립 서브에이전트 3개가 첨부 이미지와 각자의 최종
프롬프트로 내장 `image_gen`을 한 번씩 호출했다. **실제 생성 3회, 결과 3장,
각 1536×1024, 재시도 0회**다. 도구는 모델 버전을 보고하지 않았으므로 특정 모델명을
실제 호출 모델로 단정하지 않는다.

원본 픽셀을 각 작성자와 총괄이 직접 확인했다. **영지 운영이라는 장면은 3/3에서
읽히지만, 사전 기준을 모두 만족하는 엄격한 전체 장면은 0/3**이다. C의 신규 A07
관계만은 완전한 가시 실현을 확인했다. 검색·프롬프트 감사 PASS와 유효한 리뷰 기록은
픽셀의 완전 통과를 뜻하지 않는다.

| 실험 | 실제 검색·사용 | 직접 확인한 결과 | 엄격 판정 |
|---|---|---|---|
| A · 타작장 점검 | 5개 조회, 40회 노출, 고유 소스 36개 완문 검토. 신규 A01의 마을·밭·창고 연결 경로를 inspiration_only로 사용 | 인물의 지시, 현장 도면, 곡물 작업·수레·창고·저택은 보임. 현장 책임자는 지시 경로 대신 주인공을 보고, 타작장 출구·운반 경로·배수 끝점과 A01의 연속 길 일부는 가림/화면 밖 | 주제 기준 2 PASS / 4 FAIL. 전체 FAIL |
| B · 토지 경계 청원 | 6개 조회, 48회 노출, 고유 소스 44개 완문 검토. B06의 대응 기록 원리를 fragment inspiration으로 사용. 두 장부를 대조하는 전체 원본 후보는 채택하지 않음 | 지도와 기록에 비슷한 강·다리·경계 도형이 반복됨. 두 청원자는 서로 다른 구획을 가리키고, 서기관은 대응 장부 대신 뒤의 별도 종이에 씀. 경계 끝점 연결 일부도 가림 | 주제 기준 2 PASS / 3 FAIL. 전체 FAIL |
| C · 공동 화덕의 교류 | 4개 조회, 32회 노출, 고유 소스 30개 완문 검토. 자연 노출된 신규 A07만 inspiration_only로 사용 | 열린 함·실제 곡물, 별도의 닫힌 함·뚜껑, 담당자·열린 기록이 같은 화면에 모두 보임. 이 A07 관계는 PASS. 빵을 받치는 두 번째 손 접점 일부가 가리고, 작은 초기 찢김보다 크게 갈라짐 | 주제 기준 4 PASS / 1 FAIL. 전체 FAIL |

세 장면은 각기 다른 기준을 가지므로 세부 gate 수를 합산한 공통 정확도로 표현하지
않는다. 정식 신체 관계 검토도 세 실험 모두 `record_valid=true`,
`technical_qualification=fail`이다. A의 신발 밑창 접지와 C의 가린 손은 보이지 않아
판정을 보류할 증거이며, 숨겨진 신체 변형을 진단한 것은 아니다. 모든 장면에 신발
노출이 필수라는 일반 규칙을 만들지 않는다.

### A · 곡물 타작장 점검

![A 곡물 타작장 점검](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-a/image.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-a/authored/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-a/report.md) · [픽셀 기준별 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-a/pixel-test-review.json)

### B · 토지 경계 청원

![B 토지 경계 청원](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-b/image.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-b/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-b/arm-b-report.md) · [픽셀 기준별 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-b/strict-pixel-test.json)

### C · 공동 화덕과 곡물 기록

![C 공동 화덕과 곡물 기록](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-c/images/public-bakehouse-initial.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-c/authored/final-prompt.txt) · [독립 보고서](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-c/arm-c-report.md) · [A07의 관계별 판정](/Users/chasoik/Projects/image-prompt/generated/photo-runs/estate-20261024-arm-c/source-A07-pixel-review.json)

### 절차·증거와 해석 한계

- 15개 자연 조회에서 총 120회 노출된 결과를 검토했다. 고유 소스 수 36/44/30은 실험별 수이며, 합계 110을 전체 고유 소스 수로 부르지 않는다. 주제 전체 조회에는 잡음이 있어 그대로 보존했고 목표 후보를 강제 주입하거나 추가 조회로 바꾸지 않았다.
- 세 실험 모두 후보 원문의 native 채택 ID는 비어 있고, 사용한 자료는 inspiration_only다. C의 완전한 가시 관계 확인도 native 자격 자동 승격을 뜻하지 않는다. B06 전체 후보의 성공/실패율을 B의 부분 영감 사용으로 대신하지 않는다.
- C는 최초 준비의 전체 역할 범위를 제자리에서 바꾸지 않고, 검색 전에 동일 코어 바이트로 범위를 정한 별도 준비를 만들었다. 첫 프롬프트 감사의 입력 필드 오류는 필드만 수정했다. 코어·예상 픽셀 기준·최종 프롬프트는 바꾸지 않았다. 실패 기록도 남겼다.
- 원본/저장본 해시, 첨부 이미지 해시, 프롬프트 해시, 실험별 1행 호출 원장, 동결 상태와 H-F2/native 세대 연결을 교차 확인했다. PNG 청크 CRC와 크기도 확인했다. 이 무결성 검사는 직접 픽셀 판정을 대체하지 않는다.
- 대조군 이미지 없이 독립 사례 3개를 실행했으므로 데이터 추가로 인한 인과적 개선이나 전체 성능을 증명하지 않는다. 실패 원인을 데이터·프롬프트·모델 중 하나로 분리할 수도 없다. 사용자의 미적 판단은 아직 받지 않았다.
- 법적 소유·작위·주민의 자발성·세목·과거 수리·경제 성장·역사적 정확성은 이 이미지들로 입증하지 않는다.

[호출·해시·리뷰 교차검증](integration-evidence/image-test-results.json),
[총괄 A 판정](integration-evidence/independent-pixel-review-a.json),
[A 시선 조건의 엄격 재판정](integration-evidence/pixel-adjudication-a.json),
[총괄 B 판정](integration-evidence/independent-pixel-review-b.json),
[총괄 C 판정](integration-evidence/independent-pixel-review-c.json)에 근거를 보존했다.

### 다음 개선에서 유지할 기준

A는 카메라와 장애물 배치를 바꿔 길·타작장 출구·배수의 양 끝점이 끊김 없이 보이게
할 필요가 있다. B는 지도 위 한 구획의 두 지시 접점과 장부 위 실제 펜 접점을 구분해
보이게 해야 한다. C는 빵을 잡는 네 손의 독립된 접점과 작은 찢김 상태를 분명히
보여야 한다. 이들은 후속 테스트 계획이며 이번에 추가 이미지를 생성한 것은 아니다.
실패 뒤 기준을 약화하거나 partial을 PASS로 바꾸지 않았다. 직접 관찰한 9개 경계와
후속 테스트 설계는 [픽셀 회귀 관찰](integration-evidence/pixel-regression-observations.json)에
별도로 보존했다. 이 후속 제안은 아직 실행하지 않았다.

## 기본 런타임의 최종 반영

최종 기본 런타임 선택과 설치 검증을 완료했다. 그 사이 갱신된 법정·캠퍼스·로맨틱
코미디·메카·군사 등 다른 주제의 데이터가 포함된 기본 세대를 기준으로 이번 후보·연결만 추가했다.
기준 후보 22,260개와 기존 역할·정책·연결을 모두 보존했고, 새 후보
78개를 더했다. 기존 후보 수정은 0개다. 순위 정책과 봉인된 커널 코드는 같다.
오래된 기준의 중간 빌드는 기본값으로 선택하지 않았다.

- 최종 기본 H-F2 세대: `bb77d341a1306eccbb763cc3cb18a3d89e693b85c829dec238ef2a413412ccb5`
- 최종 기본 native 세대: `4473daa5fbaf75084739e611995e2a79aa42c729f357600fd1139ce67ac98425`
- 신규 긍정 후보 22개 모두 인덱스 포함, 진단 56개 모두 긍정 검색 제외.
- 테스트 세대와 최종 기본 세대의 신규 원문 78개 및 연결 56개가 정확히 같다.
- 최종 세대에서도 유지보수 조회 12개를 실행했다. 주제 조회 8개 중 8개가 상위 8개에 포함됐고, 8개가 1위였다. 일반 대조 조회 4개 중 4개에는 이번 신규 후보가 노출되지 않았다.
- 설치본에 대해 배포된 H-F2/native 전체 검증을 실행했다. 원본 기준을 읽은 뒤 기본 설정이 바뀌지 않았는지 확인하는 CAS를 통과한 후 기본 설정을 선택했다. `CURRENT` 쓰기는 0회다.

세 이미지는 최초 고정 테스트 세대에서 생성했다. 최종 기본 세대는 다른 주제의
후속 데이터를 더 포함하므로 전체 검색 풀은 다르다. 이번 원문이 같다는 사실을
최종 기본 세대에서 이미지 생성까지 다시 검증했다는 주장으로 확대하지 않는다.

[최종 기본 설정 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/estate-management-20261024/integration-evidence/current-default-successor-3cc98eb3/final-default-selection.json) ·
[최종 조회 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/estate-management-20261024/integration-evidence/current-default-successor-3cc98eb3/runtime-probes.json) ·
[전체 완료 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/estate-management-20261024/integration-evidence/FINAL-RESULT.json)

시각 의미 sidecar에는 A01의 부분 실패, B06의 부분 영감 사용, A07의 한 사례 가시
관계 통과를 증거와 함께 연결했다. 374개 표제의 정의·복합 표제 전체가 검증됐다는
표시는 만들지 않았다. 후보·연결의 원문·조건·effects는 이미지 테스트에 사용한 입력과
동일하게 유지했다. 봉인 후보 안의 연구 상태는 등록 시점의 스냅샷이며,
이후의 픽셀 관찰은 sidecar와 실행 증거에 따로 기록한다. 이번 작업에서 커밋·푸시는 하지 않았다.


## 후속 실패 보완과 재시험

같은 첨부 이미지·세 컨셉으로 독립 작성자 3명이 다시 생성한 결과와 데이터 보완은
[후속 보고서](repair-20261024/REPAIR-AND-RETEST-RESULTS.md)에 별도로 기록했다.
이 문서의 최초 실행 결과는 그대로 보존한다. 후속 엄격 전체 장면도 0/3이며,
보완 후보는 재시험 뒤 최종 긍정 7건·진단 보류 1건, 연결 21건이다.

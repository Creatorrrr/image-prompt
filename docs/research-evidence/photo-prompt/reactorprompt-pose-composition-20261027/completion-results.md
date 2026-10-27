**포즈·구도 잔여 표현 반영과 검증 결과**

Luna max 분담 저술·독립 검토를 통합해, 이번 추출에서 고정한 원문 표기 2,475개와 표현·의미 조합 3,457개 전체를 처리했다. 작업 파일과 기본 설치 런타임에 반영했으며 기본 경로의 실제 조회도 통과했다. 코퍼스는 중복 제거 2,974문서(SHA-256 `75fc5c60a1ba56ff47bc3a2dca97302765c3428d782cdb2f64120fe99409cbde`)다.

| 데이터 | 반영 결과 |
|---|---:|
| 의미 항목 | 기존 481개 보존, 세부 의미 48개 추가 → 529개 |
| 긍정 후보 | 기존 304개 보존, 608개 추가 → 912개 |
| 기존 후보 보완 | 301개 |
| 진단 전용 기록 | 64개, 긍정 검색 풀 포함 0개 |
| 긍정 후보에 연결된 표현·의미 조합 | 3,278개 |
| 진단·원문 한계로 보존한 조합 | 179개: 진단 177, 보류 2 |
| 원문 표기 전수 조회 연결 | 2,475개 / 2,475개 |

[의미·설명·특징·태그 전체 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/coverage/MEANING-DATA-FINAL.csv)와 [표현별 최종 연결·처리 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/coverage/EXPRESSION-ROUTES-FINAL.csv)에서 전체 항목을 확인할 수 있다. CSV에는 출처 개수·위치 요약과 전체 JSON 근거 링크를 넣어 긴 근거 배열이 셀 한도에서 잘리지 않도록 했다. 조합 수와 고유 문자열 수는 단위가 다르며, 한 문자열은 서로 다른 의미와 연결될 수 있다.

주체·대상, 몸·얼굴·눈·카메라의 기준축, 접촉과 하중, 신체 방향과 카메라 위치, 크롭과 가시 범위, 수치와 근사 범위를 원문에 맞춰 나눴다. 한영 본문·정의·검색 단서·조건·효과와 출처를 연결했다. 29개 새 장면 단위로 44개 평가 사례를 연결했다(38개 저술, 기존 단위 재사용 4개, 원문 한계 2개).

128개 보완 항목을 최종 데이터에 대조하면서 저술용 용어집과 배포용 설명 필드의 불일치도 찾아 수정했다. 실질 의미 누락 8개를 포함한 의미 11개의 84개 필드와 표현 경로 1개를 보완했다. 팔뚝 그림자에서 실제 지지를 추론하던 설명, 머리-등받이 방향을 접촉으로 쓰던 특징, 명시되지 않은 앉은 조건·전신 가시성·프레임 모서리 방향 등을 바로잡았다. [항목별 최종 대조 기록](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/coverage/backlog-resolution/BACKLOG-RESOLUTION.final.json)과 [정확한 필드 변경·원문 검토](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/review/completion/SEMANTIC-SIDECAR-ERRATUM-ROOT-REVIEW.json)에 근거가 있다. 최초 동결 자료와 중간 검증 입력은 재현을 위해 보존했다.

원문 한계로 남긴 두 조합은 `visual balance`의 보이지 않는 참조에 의존한 장면 관계와 `weight forward on both forearms' shadow`의 팔뚝 접촉·하중 해석이다. 후자는 그림자를 실제 접촉면으로 해석하지 않았다. 진단·보류 표현도 조회 가능하며 긍정 문구나 벡터로 승격하지 않는다.

| 고정 질의의 한 CID 완전 일치 | 이전 기본 세대 | 보강본 | 영문 / 한글 |
|---|---:|---:|---:|
| 원문 장면·관계 | 0/60 | 41/60 | 24/30 · 17/30 |
| 용어 의미·특징 | 6/24 | 24/24 | 12/12 · 12/12 |

장면 평가는 64질의 중 보류 4질의를 분모에서 제외했다. 보강본은 완전 일치 41개, 부분 일치 18개, 미노출 1개이며 보류의 거짓 통과는 0개다. 의미 평가의 기존 통과 6개도 유지됐다. 두 평가 모두 한 CID/RID의 실제 긍정 본문을 기준으로 판정했으며 별칭, 태그, 일반 `human` 조건을 누락 사실의 증거로 쓰지 않았다. 서로 다른 후보를 합쳐 단일 후보 통과로 계산하지 않았다.

[장면 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/judging-original/judgments.json), [의미 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/judging-meaning/ACTUAL-B-MEANING-JUDGMENTS.json), [판정과 실제 결과의 해시·본문 대조](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/ROOT-JUDGMENT-REFERENCE-CHECK.json)를 보존했다. 88개 저장 질의 벡터를 그대로 재사용했다. 데이터 비교 단계 B는 모델·112파일 코드·순위 계산을 유지했다. 설치 단계 C는 표현 조회와 검토한 네이티브 증거를 추가했고, 긍정 문구·D1/F2 투영·벡터 바이트·순위 계산을 B와 동일하게 유지했다. 캐시 질의 4개 재생에서도 top 8 ID·점수·표시·전체 대상 순위가 같았다. 이 88질의는 개발·회귀 자료이며 독립 일반화 성능으로 해석하지 않는다.

작업용과 설치용 전체 사전은 모두 오류 0개다. 전체 런타임은 27,063 후보, 긍정 24,988 CID / 24,990 RID이며 기존 binding은 24,508개를 보존했다. 기존 Sports의 네이티브 관계 ID 328개를 106개 기록에 복원했고, 작업용 원본과 D1/F2 긍정 문구·효과·권한은 유지했다.

[실제 설치 세대의 전수 표현 조회](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/SEALED-EXPRESSION-COVERAGE.json)는 모든 3,457개 조합의 대상·분류 연결을 통과했다. [실제 CLI 8개 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/installed-expression-tests/reports/installed-expression-tests-20261026T230047Z.json)는 긍정·진단·다의어·미등록 표현·공백/대소문자 처리, 코어 동결 이전 접근 차단, 기존 실행의 세대 고정, 위조된 내부 옵션 거부를 확인했다. 조회가 사실이나 역할 자격을 자동 부여하지 않는 것도 검증했다.

실제 Native provider 로딩과 카메라 높이 1개 후보의 요청별 역할 제안·검증·transport는 통과했다. [설치본 provider 검증](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/review/qualification/ACTUAL-C-PROVIDER-AUDIT.json)에 `eligible`과 출처가 고정돼 있다. 역할 증거는 검토한 V4 설치본에만 추가했고 작업용 V3는 증거 없이 유지했다. 새 자료의 후보는 조회·검토 단계로 제공되며 역할 자격은 사용 시 개별 검토한다. 영구 binding이나 최종 프롬프트 채택은 이번 검증에서 만들지 않았다.

기존 패션 46질의도 같은 저장 벡터로 비교했다. 35질의는 top 8 구성원이 모두 같았고, 9질의는 7/8, 2질의는 6/8이 같았다(355/368 유지). 11질의에서 밀린 기존 결과 13개는 전체 순위 9~12위에 남아 있으며 출처 해시와 긍정 본문이 동일하다. 일부 목둘레 구조·색상·손/액세서리 질의는 세부 관계의 순위 개선 과제로 남았다. [패션 비교](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/fashion-regression/review-findings.md)와 [원래 질의 범위를 구분한 최종 평가](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/evaluation/fashion-regression/ROOT-ASSESSMENT.json)에 순위 변동과 한계를 기록했다. 패션 의미 품질 전체의 통과를 주장하는 비교는 아니다.

남은 장문 장면 질의 19개는 완전한 대상 후보가 전체 풀에 있으나 top 8 밖에 있다. 특히 한국어의 복합 주체·관계·촬영 조건을 함께 요구하는 질의에서 차이가 컸다. 후보 ID 우대나 신규 데이터 할당량은 넣지 않았다. 원문 출현 24,954건 전체의 의미적 재판정을 완료한 것도 아니며, 자동 추출 당시 불확실 9,949건은 전수 인적 검토로 승격하지 않는다. 이번 검증 범위는 데이터·조회·검색·설치·요청별 역할 제안이다. 이미지 생성·픽셀 판정은 0건이다.

현재 기본 H2는 `1f3979c3564a394f0de88bf2f6da6647c9598a8bf1205f19291a86e09d87de0a`, Native는 `fd7b80758da8d80d8791c26f1784ee7aae9cddc30cd759d63fde46dfbb73cf9f`, 코드 폐쇄 SHA는 `1fc93708acaf0e1f76cb5b9a950b9d9cf60ef058835aa9fa9121d9f5ffb8d75a`다. [기본 전환과 실제 기본 경로 조회](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/runtime/DEFAULT-ACTIVATION-RESULT.json)를 확인했다. 이전 세대와 검색 shard는 보존했고 `CURRENT` 쓰기는 0건이다. 새 표현 조회 사용법은 [데이터 참고 문서](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/reactorprompt-pose-composition.md)에 추가했다.

보호한 85,526경로의 최종 대조는 허용 목록 밖 변경 0개다. 다른 작업에서 이미 바뀐 계획 문서는 관찰된 내용 그대로 보존했다. HEAD `09d099efdc12712524f3a8fbb8fcdbe8df6af7f0`와 staging은 유지했고 commit/push는 수행하지 않았다. 최종 보존 검증은 [보존 결과](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/coverage/FINAL-PRESERVATION-AFTER-GUIDE.json)에 기록한다.

최종 적용 파일과 검증 해시는 [적용 명세](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/DELIVERY.json)에 고정했다.

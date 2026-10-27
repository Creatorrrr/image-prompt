# ReactorPrompt 포즈·구도 의미 및 후보 데이터

초기 수집 텍스트 2,974개 전체에서 원문 표현을 추출하고 제한된 문맥 검수를 거쳐,
먼저 481개 용어·의미 항목과 304개 관찰 가능한 후보 단위를 정리했다.
아래 보완 후의 현재 수량과 원문 의미의 전수 판정 범위는 별도로 구분한다.
동의어와 원문 관측 표현은 구분하며, 정확한 원문 인용과 원본 프롬프트는 비공개 수집 폴더에 보존한다.

한영 의미 설명, 관찰 특징, 주체와 대상, 신체·시선·카메라의 서로 다른 축, 혼동 경계,
조건·영향 속성 및 원문 문서/글자 위치를 연결한다. 검색에는 후보의 definition,
aliases, keywords, paraphrases가 실제 정규 검색 필드로 투영되는지 별도로 검증한다.
이 참고 문서와 의미 sidecar 자체를 검색 인덱스나 실행 권한으로 간주하지 않는다.

후보는 discovery-only이며 native 역할 자격이나 생성 픽셀 검증을 부여하지 않았다.
금지·예시·선택지·불명확한 표현은 별도 경로로 보존하며 긍정 후보를 자동으로 승인하지 않는다.
원문 조합 검색 64개 질의와 독립 용어 의미 검색 24개 질의를 고정해 전후 결과를 따로 비교한다.

모듈: `photo_candidate_reactorprompt_pose_composition_20261026.json`. 의미 데이터: `photo_reactorprompt_pose_composition_semantics_20261026.json`.
입력 말뭉치 SHA-256: `75fc5c60a1ba56ff47bc3a2dca97302765c3428d782cdb2f64120fe99409cbde`.
원문·방법·검수·검색 영수증은 `generated/trend-scout/raw/reactorprompt-pose-composition-20261026/`에 있다.

## 2026-10-27 reviewed completion data

This reviewed local dataset combines the frozen 304-record source with reviewed A/B/C and source-scene updates. It contains 912 positive candidates and 64 non-positive diagnostic records (976 total), 529 meaning keys, 301 updated baseline candidate records, and 672 added candidate IDs. The 3,457 frozen term-expression pairs have explicit route rows: 3278 positive indexed routes and 179 diagnostic/held lookup routes.

Diagnostic lookup forms are retained in the semantic route registry and in exact aliases of diagnostic records. Their diagnostic record kind excludes them from positive search documents and vectors; the lookup forms do not assert visual facts. Source-scene review retains 38 authored cases, 4 existing-unit reuses, and 2 source-limited holds.

The source-contract review and all frozen expression routes are closed. Native qualification, retrieval ranking, installed-runtime checks, and generated-pixel compliance are tracked separately in the completion report.

## 검증된 표현 조회

유효한 저술 코어를 동결한 뒤 [photo_workflow.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_workflow.py)의 `view --run <동결된-run-경로> --expression <원문-표현>`으로 표현을 조회한다. 코어 동결 전에는 후보를 읽지 않는다. 실행에 저장된 generation이 있으면 그 세대를 유지하며, 현재 세대로 대체하지 않는다.

이 조회는 영문 대소문자와 공백만 정규화해 등록된 원문 표현을 찾고, 같은 표기에 연결된 의미가 여럿이면 함께 돌려준다. 각 의미의 실제 본문, 주체·대상·기준축, 조건·효과와 원문 근거를 검토해 사용 범위를 결정한다. 미등록 표현은 `unrecognized`이며, 진단·보류 경로는 긍정 후보와 구분된다. 별칭·태그는 조회 단서이며 사실·역할 자격을 부여하지 않는다.

데이터 검수는 `view --maintenance --expression <원문-표현>`을 사용한다. 이는 저술 코어의 동결이나 후보 채택을 대신하지 않는다. 현재 적용 수량, 독립 의미 판정, 실제 설치 검증과 남은 검색 순위 한계는 [보완 결과](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/completion-20261027/RESULTS.md)에 기록한다.

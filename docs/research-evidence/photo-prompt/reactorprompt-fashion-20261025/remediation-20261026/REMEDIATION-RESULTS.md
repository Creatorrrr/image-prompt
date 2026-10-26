# ReactorPrompt 패션 검색·선택 보완

현재 상태: 소스·절차 보완, 설치·검색 검증과 기본 경로 전환, 독립 세 이미지 생성·기록·감사 및 root 픽셀 검토 완료. 신규 코호트 문구 기여는 재시험에서도 0/3이며 신규 데이터 반영 검증은 미통과다.

## 0건의 원인

이전 테스트에서 신규 패션 코호트 2,430개 중 5개 CID가 7회 반환되었으나 모두 제외되었다. 전체 반환은 160회, 서로 다른 CID는 133개였다. 신규 데이터가 검색에서 완전히 차단된 것은 아니다. 노출된 카드들은 아동복 모티프 분기, 두 인물의 교복, 특정 의상에 종속된 장식, 동일 착용자의 의상-액세서리 관계, 착용자 어깨를 덮는 니트/울 대안 등 당시 장면과 다른 인원·소유자·조건을 포함했다.

한 테스트는 사용자가 지정하지 않은 의상·소재까지 닫고 framing만 열었다. 검색 주제에는 무작위/서로 다른 컨셉이라는 실행 지시도 섞여 있었다. 또한 2,430개 모두 EN/KO 본문을 갖고 있었지만 2,426개는 한국어 별칭 하나뿐이어서 자연 의상 표현의 검색 경로가 약했다. 번역 부재나 native 승인 부재 하나로 일반적 영감 기여 0건 전체를 설명할 수는 없다.

## 반영한 변경

- 스킬: 예시 open-dimension 목록을 기본 제한으로 쓰지 않도록 명확히 했다. 사진의 얼굴·머리카락 참조는 해당 속성 범위에서 다루고, 사용자가 정하지 않은 의상·소재 선택은 열어 둔다.
- 주제 범위: 무작위/차별화 실행 지시와 실제 시각 주제를 구분한다. 실제 시각적 대비·수식어까지 제거하는 키워드 필터는 추가하지 않았다.
- 후보: 기존 8개 CID에 자연스러운 EN/KO 별칭 32개만 추가했다. 다른 2,422개 레코드, 본문, 조건, 효과, 소유자 관계, 바인딩, 승인 상태는 보존했다. 검토되지 않은 중복 카드 5개 제안은 반영하지 않았다.
- 선택 기록: 생성 전에 baseline과 새 최종 문구의 차이, 출처 CID/RID/hash, 열린 선택 범위, 전체 원문 조건, 관찰 기준을 기록한다. 기존 문구 확인과 미선택 대안은 기여 0건으로 센다.
- 검색기: 전체 positive pool, BM25F/local cosine 두 lane, 기존 sampler를 유지했다. CID 우대, 코호트 할당량, seed 재추첨은 추가하지 않았다.

## 검증 범위

V3 소스 검증은 26,087개 후보/24,508개 바인딩에서 오류 없이 통과했다. 후속 설치본은 H-F2 `e8d4f9039129c78559622bbe9fc1779a96a9f68c266ae90312b72ab9af82806f`, native `7c878e032ac2f2ac1c3e3e468e1be591ba22946d63f52fb58de908dd61767d1f`이다. H-F2의 변경 없는 24,070개 RID 벡터는 보존했고 8개만 다시 계산했다.

봉인된 V4 사전에는 기존 스포츠 후보 `cand_007db1a9c5a552a3a1c16dbbaa6d0e1e`의 relations 오류 1건이 그대로 남아 있다. 패션 후보 오류는 없으며, 이를 전체 V4 사전 PASS로 보고하지 않는다.

3개 독립 컨셉은 모든 2,556개 추출 용어의 이미지 검증이 아니다. 검색 노출, 일반적 출처 영감, native 계약 선택, 이미지 관찰, 사용자 수용은 별도 지표다. 렌더링한 baseline 대조군이 없으므로 이미지 품질의 인과적 향상은 주장하지 않는다.

후속 최종 기록: [RESULTS.md](/Users/chasoik/Projects/image-prompt/generated/photo-runs/reactorprompt-fashion-retest-20261026/RESULTS.md)와 같은 디렉터리의 `FINAL.json`에 실제 이미지·문구·출처 검증을 기록한다.

## 완료된 검색 검증

후속 설치본은 실제 기본 경로로 선택됐고 bound Python/NumPy/installed recorder 및 sealed dispatcher 검사를 통과했다. 세 arm은 동일 후속 설치본을 정상 managed 경로로 사용했다. 예전 세대나 working source로 fallback하지 않았다.

용어 질의는 5,112개 중 384개만 후속 재생을 완료했다. 이 3개 checkpoint는 보존했으며 나머지는 미완료다. 별도 natural46은 전량 비교했고 43개 top8 순서 동일, 3개 순서 변경이다. general/control16은 동일 질의 벡터로 before/after를 비교했다. 독립 검토자는 114개 고유 원문과 256개 순위 배치를 확인해 주요 관련성/대조군 회귀를 찾지 못했다. EN roomy pullover 및 KO rolled-sleeve shirt의 8위/5위 진입은 partial→direct 교체다. 다만 KO wool/woven coat 질의에서 exact 후보가 1→2위로 내려간 top1 정확도 손실은 남아 있다. 비패션 대조 4개는 top8 CID 순서까지 동일했다. 이는 고정 질의의 제한된 검색 검증이며 실제 채택/이미지 품질 증명이 아니다.

검증 증거: `runtime/FINAL-RESULT.json`, `runtime/ROOT-FINAL-REVIEW.json`, `runtime/INDEPENDENT-RELEVANCE-REVIEW.json`. release 당시 `runtime/ROOT-REVIEW.json`과 동결 입력은 보존했다.

## 재시험에서 발견해 교정한 역할 질의 문제

초기 재시험의 role_focus/scene_context에는 agent의 운영 설명(`not a requester lock`, `do not infer…`, 선택사항이라는 해설)이 반복됐다. 봉인된 scope parser는 이를 unmodeled restriction으로 해석해 A의 7개, B의 12개, C의 6개 역할에서 결과를 0개로 투영했다. A의 garment_detail은 추상 owner 문구가 prop-placement 관계로 읽혀 별도의 source-witness 모드에서 0개였다. 이는 이전 테스트의 0건 원인과 구별되는 후속 재시험 중 발견 사항이다.

25개 질의의 role_focus/scene_context만 실제 긍정 시각 duty와 기존 장면으로 최소 교정했다. 제약·open scope·review metadata는 보존했고, 실제 사용자 부정 조건이나 source guard를 제거하지 않았다. 최신 SKILL `77145606ecdbebd93949d9f01849f0da4752c610dc641c595f0745bee1c97207`에 작성·진단 절차를 명시했다. 순수 문자열 검사 후 새 managed run으로 동결 입력을 재현했으며, root는 세 core/controls/selection/embodiment/baseline/request 파일이 원본과 바이트 동일함을 검증했다. 실제 재검색에서 25개 역할 모두 ordinary projection, 전체 24,076 CID 후보/32개 rank window/8개 sample로 복구됐다.

관리형 API는 수정된 새 run에 이전 sampling seed를 넘길 수 없다. 원래 세 실행의 seed·material·views·workflow를 보존하고, 수정 실행마다 정상 발급된 첫 seed 하나만 사용했다. seed를 고르는 반복은 하지 않았으며, 같은 seed의 전후 비교나 이미지 품질 인과효과는 주장하지 않는다. 이미지 호출 전의 처리 범위 교정으로, 기존 컨셉을 새로 쓰지 않았다.

관련 증거: retest의 `SOURCE-SNAPSHOT.v2.json`, `ROOT-REPLAY-EQUIVALENCE.json`, `QUERY-REPAIR-RESULT.json` 및 본 디렉터리의 `query-repair/RECOVERY-PATH.md`, `process/query-repair/FINAL-INDEPENDENT-REVIEW.json`.

## 실제 재시험 결과

Luna max 독립 서브에이전트 3개가 같은 첨부 사진으로 각 1회 생성했다. 336회/193개 고유 원문을 검토했고, 신규 코호트는 rank window 21회, 실제 sample 5회/5개 CID가 노출됐으나 모두 제외됐다. 최종 신규 문구 기여 0, 신규 native 채택 0이다. 별칭을 보강한 8개는 이번 세 컨셉의 rank window에도 들지 않았다. 따라서 보강된 데이터의 실제 이미지 효과는 입증되지 않았다.

기존 라이브러리의 일반적 영감은 6개 고유 CID/8회였다. 저장 픽셀의 엄격한 세부 표현 검사는 재킷 직조 1개 충족, 나머지 5개 부분 충족이다. 세 이미지의 패션 장면과 얼굴·머리 시각 가이드는 확인됐지만 이 사실을 신규 데이터의 기여로 세지 않는다. 절차 복구와 제한된 자연 질의 검색 개선은 완료됐고, 신규 데이터의 선택·이미지 반영 문제는 남아 있다.

관리형 사후 review 기록은 모두 schema-valid다. A·C는 기술 자격을 통과했고, B는 mid-thigh crop에서 서 있는 발·하체 지지가 보이지 않아 support/balance gate가 실패했다. 이 실패도 보존했다.

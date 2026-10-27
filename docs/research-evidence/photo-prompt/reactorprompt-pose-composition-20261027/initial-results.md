# ReactorPrompt 포즈·구도 추출 및 보강 결과

완료: 2026-10-27 01:12 KST. Luna max로 원문 추출 4분할, 후보 저술, 독립 검토를 분담했다. 검증한 신규 데이터를 기본 검색에 연결했다.

## 수집본과 추출 결과

수집된 프롬프트 파일 4,613개와 번역 프롬프트 항목 2,872개를 원본·해시와 대조해, 중복 제거한 2,974문서 전체를 처리했다. [범위 대조 기록](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/SOURCE-SCOPE-VERIFICATION.json)

- 원문에서 확인한 표기 2,475종. 대소문자·철자 변형을 포함한 표현 수이며, 의미 수와 다르다.
- 의미 항목 481개: 포즈 278개, 구도 203개.
- 의미 배정 24,954건, 고유 원문 구간 23,768곳. positive 10,579 / contextual 4,135 / uncertain 9,949 / negative 291.
- 모든 보존 인용의 문서·해시·문자 위치를 검증했다. 구조 검사 오류·경고 0. 독립 수동 검토는 범위를 정한 표본 검토이며, 의미 누락이 전혀 없다는 보증은 아니다. 추가 주석 12건은 동결 원문을 변경하지 않고 별도로 보존했다.

[원문 표현 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/exports/final-1/pose-composition-observed-keywords.csv) · [의미·특징·태그 CSV](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/exports/final-1/pose-composition-keywords.csv) · [전체 근거 JSON](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/exports/final-1/pose-composition-lexicon.json)

## 의미와 검색 데이터

한영 정의, 관찰 가능한 특징, 검색 별칭·태그, 신체/카메라의 주체, 접촉 대상, 좌우·시선·머리·카메라 방향, 크롭 경계, 혼동되는 인접 의미와 원문 근거를 정리했다. 예를 들어 눈높이 카메라와 위로 향하는 시선, 신체 좌우와 화면 좌우, 접촉과 가림, 전신 크롭과 프레임 밖 신체 부위를 구분한다.

481개 의미에 각각 명시적 경로를 연결했다. 근거가 있는 전체 또는 범위를 제한한 구성요소 경로 434개, 진단 경로 42개, 보류 5개다. 이 경로들이 304개 새 visual_option 후보에 대응한다. 후보의 긍정 문구는 원문이 지지하는 한정된 단위로 작성했고, 혼동 경계·불확실성·제외 설명은 별도 의미 자료에 보존했다.

검색에 투영한 문구는 정의 304개, 별칭 1,360개, 키워드 1,954개, 패러프레이즈 902개다. 동일 후보의 여러 원본 필드에 반복된 376개 문구는 canonical 문서에서 한 번씩 표현되며, 원본 필드 역할과 실제 D/F2 문서의 값 보존을 확인했다. 다른 후보의 문구나 부분 문자열로 대체하지 않았다. [최종 조립 기록](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/integration/FINAL-ASSEMBLY.json) · [실제 D/F2 투영 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/successor-builds/58ffe7010c46f093/positive-projection-verification.json)

## 실제 검색 평가

보강 전에 동결한 질의와 로컬 임베딩 벡터를 재사용했다. 검색 모델·랭커·가중치·코드는 바꾸지 않았고 전체 positive 후보 24,380개, RID 24,382개에서 표준 상위 8개를 평가했다. 추가 질의 재작성이나 신규 후보 우선 필터는 사용하지 않았다. Luna max 독립 검토자가 각 영문·한글 질의에 대해 반환된 한 CID가 필수 의미·주체·대상·조건·방향·효과 전체를 담는지 판정했다. 부분 일치나 여러 CID의 합은 통과로 세지 않았다.

| 평가 | 보강 전 완전 일치 | 보강 후 완전 일치 | 보강 후 영문 | 보강 후 한글 |
|---|---:|---:|---:|---:|
| 원문 장면·관계 | 0/60 | 0/60 | 0/30 | 0/30 |
| 키워드 의미·특징 | 0/24 | 6/24 | 3/12 | 3/12 |

첫 평가의 관찰 불가능/보류 2사례·4질의는 위 60질의 분모에서 제외했고, 통과로 세지 않았다. 의미 중심 평가의 24질의는 모두 분모에 유지했다. 신규 후보 노출 자체는 첫 평가 60/64질의·104종, 의미 평가 22/24질의·46종으로 확인됐다. 노출 수와 완전 의미 일치 수는 별도 지표다.

완전 일치율은 여전히 낮다. 의미 중심 평가에서 포즈는 0/12, 구도는 6/12였다. 반환된 가까운 후보의 누락에는 standing/crouching 같은 자세 문맥, 정량 각도·넓이 표현, 카메라 기준 좌우 관계, 한 후보 안에서의 복합 조건 연결이 포함된다. 이는 검색된 일부 구성요소를 전체 장면의 근거로 승격하지 않은 결과다. 초기 판정에서 질의 문맥으로 누락된 주체·앉은 상태를 보충한 4개 complete를 발견해 모두 partial로 정정했다. 정정 전후와 고정 기준은 별도 기록에 보존했다. 이 평가로 데이터 전체에 해당 의미가 없다고 결론 내리지는 않는다. 태그와 정의 보강은 완료했으나 복합 질의의 완전 일치가 충분히 해결됐다고 주장하지 않는다.

[주체·자세 조건 재판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/successor-builds/58ffe7010c46f093/explicit-evaluation/successor-owner-adjudication.json) · [장면·관계별 전체 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/successor-builds/58ffe7010c46f093/explicit-evaluation/successor-judgments.json) · [의미·특징별 전체 판정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/successor-builds/58ffe7010c46f093/explicit-keyword-meaning-evaluation/successor-judgments.json) · [판정 집계·식별 검증](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/JUDGMENT-SUMMARY.json)

## 기본 검색 반영과 검증 경계

작업용 전체 사전은 후보 26,391개·연결 24,508개로 오류 없이 통과했고, 전체 검색 인덱스도 검증했다. 기존 26,087개 후보와 연결·권한 기록을 보존했다. 설치용 검색에서는 기존 RID 24,078개의 벡터가 바이트 단위로 같고, 신규 304개 문서만 로컬에서 임베딩했다. 봉인 코드 112개 파일의 해시 묶음은 그대로다.

기본 H-F2 generation은 `563a9fa9e5e2882cac80436c5b7f962935863dbcb133aac3ee5746579c0149f0`, native generation은 `dc9cbf9a60ff109ac63c339c2f3319a29930e10c1577cf336212952f86bd0ebd`이다. 기본 설정은 이 두 식별자만 바꿨고 실행 검사를 통과했다. 전환 후 캐시된 영한 질의 4개를 기본 설정으로 다시 검색해 사전 명시 generation 결과와 상위 8개 CID/RID가 같은지 확인했다. [기본 반영](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/default-activation.json) · [기본 검색 재확인](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/default-search-replay.json)

설치용 native 전체 사전 검사에는 기존 Sports 후보 `cand_007db1a9c5a552a3a1c16dbbaa6d0e1e`의 relations 스키마 오류 1건이 남아 있다. 보강 전·후 오류 목록이 같고 신규 후보 오류는 0이다. 따라서 설치용 전체 사전이 완전 통과했다고 주장하지 않는다. [봉인 빌드 및 차이 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/successor-builds/58ffe7010c46f093/build-result.json)

신규 후보에 native binding이나 생성 승인 근거를 만들지 않았다. 이번 검증은 추출·의미·검색까지이며 이미지 생성 0회, 실제 이미지 반영은 검증하지 않았다.

초기에 해시를 저장한 보호 경로 2,847개를 대조했고, 이번 작업의 명시적 자산·인덱스·참고 문서·기본 설정 외 해시 변경은 없다. HEAD와 스테이징 상태를 보존했다. 초기 해시 목록 밖에 있는 현재의 dirty/untracked 경로는 별도 목록으로 남겼으며, 그 파일들의 작업 전후 바이트 동일성은 이 검사로 보증하지 않는다. 이번 요청에서는 커밋·푸시를 수행하지 않았다. [보존 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/protected-source.final.json)

## 실행 도우미 보정 기록

작업용 도우미에서 stage의 자동 생성 bytecode, 동일 후보 안의 문구 canonical 중복, 검증 JSON의 map 정렬, 설치 검증 함수 연결 오류를 확인하고 보정했다. 봉인된 검색 코드·모델·랭커·최종 후보 값은 바꾸지 않았다. 원래 실패 기록을 보존하고, 같은 generation 데이터와 이전/이후 record 값의 동일성 및 별도 프로세스 재검증을 거쳐 완료했다. 설치 중단 후에는 정확히 일치하는 기존 no-activate 설치 기록과 전체 봉인 사본 해시를 확인해 재사용했다.

[stage cache 보정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/STAGE-RECOVERY.json) · [동일 후보 문구 보존](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/CANONICAL-DEDUP-OWNERSHIP.json) · [검증 기록 재현](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/CANONICAL-RECEIPT-REPLAY-COMPARISON.json) · [자체 검사](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/canonical-receipt-self-test.json) · [설치 연결 보정](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/runtime/INSTALL-WRAPPER-RECOVERY.json)

기계 판독용 집계: [RESULTS.json](/Users/chasoik/Projects/image-prompt/generated/trend-scout/raw/reactorprompt-pose-composition-20261026/RESULTS.json)

# 다크 판타지·그림다크 데이터 반영과 독립 이미지 실험

2026-10-22. 앞선 연구 초안을 실제 데이터로 등록하고, 최신 스킬과 참조
이미지로 독립 서브에이전트 세 개의 실험을 진행한 후속 기록이다.
초기 `VALIDATION.json`, `EVALUATION-CASES.tsv`의 NOT_RUN, `PIXEL-PLAN.md`는
연구 단계의 스냅샷이다. 아래 실행 증거와 구분한다.

## 반영한 데이터

| 항목 | 추가 | 현재 전체 |
|---|---:|---:|
| 시각 의미 카드 | 72 | 이번 주제 72 |
| 원 대화 키워드 경로 | 247 | 이번 주제 247 |
| 선택형 시각 후보 | 68 | 검색 대상 positive CID 18,876 |
| 문맥·진단 레코드 | 4 | 전체 CID 19,078에 포함 |
| 선택형 슬롯 바인딩 | 136 | 13,015 |
| 후보·바인딩 모듈 | 2 | 51 |

작업용 파일:

- `skills/photo-prompt-image-generator/assets/photo_dark_fantasy_grimdark_semantics_20261022.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_dark_fantasy_grimdark_20261022.json`
- `skills/photo-prompt-image-generator/assets/photo_candidate_dark_fantasy_grimdark_bindings_20261022.json`
- 후속 참고 문서 `references/dark-fantasy-grimdark-semantics.md`

각 시각 후보는 완전한 한영 문구, 개별 구성요소·소유자·방향 관계,
관찰 게이트, 혼동 경계와 주장 한계를 보존한다. 문맥 4개(X05–X08)는
positive 검색에서 제외한다. 247개 경로를 247개 강제 장면으로 바꾸지 않는다.
기존 19,006개 후보·12,879개 바인딩·슬롯 카탈로그·정책은 모두 그대로다.

기존의 속 빈 자율 갑옷과 별도로, M07은 같은 성인 착용자의 팔 갑옷
안쪽 테두리에서 나온 유기 촉수가 그 착용자의 피부에 닿는 구조다.
기존 자료의 빈 내부나 피부와의 틈 조건을 지우지 않았다. 성유물/함,
장식 괴물/배수구, 가시적 저주 흔적/보이지 않는 인과도 구분한다.

46개 출처는 용어 정의와 맥락을 지원한다. 구체적인 허구 장면의 기하는
직접 저술한 선택형 제안이다. provenance의 SHA는 연구 명세를 식별하며
다운로드한 웹페이지 바이트의 해시가 아니다. 그래프는 검토 메타데이터다.
새 후보의 native approval은 모두 false이며, 등록·검색·이미지 성공만으로
기존 소유자 권한, typed native fact, 전체 native 적합성을 부여하지 않는다.

## 작업용·설치용 검색 반영

작업용 V3 소스와 설치용 V4 canonical 소스를 구분했다. V4 변환은 원문
literal과 조건·효과·출처를 손실 없이 보존하고, canonical native snapshot을
원본 72개와 각각 대조했다. 기존 설치 코드와 임베딩 공간은 유지했다.

- 최신 SKILL SHA: `7fe5b6cfc2da6e65dd9b9dc999e46d70a1fac7dce8c47157e53c1cba43b00f35`
- H-F2 generation: `b3d888f3909bd20a34403da1b9de3f11cf91d5dcf6a47172d7c6bfb9e2a6342e`
- native generation: `e12a8251dc946d2e14c3f88e9287aba89de0d531c097cb40cfef0b00dff6e4b1`
- 설치 코드 SHA: `96b67dedcfea019115cd46c6542287d7102e46cd12a486f1e817d79f3c634d0e`
- 설치 store: `/Users/chasoik/.cache/image-prompt/photo-shared-runtime/h-f2-installed`

작업용 인덱스는 기존 18,808개 벡터를 재사용하고 68개를 로컬
EmbeddingGemma 2로 추가했다. 설치용 H-F2는 기존 18,810개 RID 벡터를
보존하고 68개를 추가해 18,878 RID가 됐다. BM25F의 전역 통계는 새
전체 풀에 맞춰 다시 계산했다. 설치 사본의 실제 봉인 코드로 H-F2와
native validator를 실행한 뒤 기본 generation을 위 버전으로 선택했다.
이 작업은 CURRENT를 게시하는 경로를 호출하지 않았다.

## 실제 질의와 경계 검토

56사례의 한국어·영어 112개 질의를 이전/이후 전체 풀에 각각 실행했다.
각 실행은 BM25F 1회와 local cosine 1회다. 질의 임베딩과 각 상위 8개,
목표 순위, generation을 보존했다.

| 구분 | 실제 질의 수 | 결과 |
|---|---:|---|
| 개발 | 48 | 목표 후보 상위 8개: 48/48 |
| 경계 | 32 | 새 후보가 상위 8개에 노출: 18/32 |
| 일반 대조 | 24 | 새 후보가 상위 8개에 노출: 4/24 |
| 비가시 대조 | 8 | 새 후보가 상위 8개에 노출: 2/8 |

대조군의 새 노출 24개 질의를 모두 검토했다. 피부 접점이 없다는 질의에
M07, 정상 작물에 시든 작물 M12, 배수 금지에 물줄기 O04가 검색되는
경우는 완전한 source 의미와 충돌하므로 skip해야 한다. 빈 손 모양 함에
O02, 실제 부서진 후광에 O12가 노출되는 경우처럼 양립 가능한 결과도
있다. 따라서 노출 수를 일괄 오탐 수나 정밀도라고 부르지 않는다.

비가시 대조의 훼손된 제단은 신의 침묵을 증명하지 못한다. 자유로운
동의는 혼례 소품으로 판정하지 않는다. 이 경계를 검색 순위가 해결한
것으로 주장하지 않는다. 후보 검토·skip 및 원래 장면의 의미 보존이 필요하다.

이 질의는 연구 중 작성한 개발·경계 사례다. 독립 holdout, 슬롯별 전체
정밀도, 이미지 품질 향상, 인과적 개선을 입증하는 실험은 아니다.
신규 목표가 이전 풀에 없다는 사실 자체를 품질 개선 점수로 세지 않았다.
별도 기존 의미·primary proof·topic/negative 경계 회귀 49개도 통과했다.

## 독립 실험의 방법

각 에이전트는 다른 arm의 prompt·후보·이미지를 보지 않았다. 후보와 연구
카드에 접근하기 전에 자체 난수 선택으로 복잡한 장면을 정하고, 기준
프롬프트·요청 의미·creative controls·선택·embodiment 검토를 freeze했다.
이후 자신의 사전 슬롯 질의를 새 generation에서 실행했다.

반환된 material을 완전하게 검토하고, 적합한 항목은 inspiration_only,
나머지는 skip으로 결정한다. 새 데이터 사용을 강제하지 않는다. 사용할
경우 CID/card → 최종 프롬프트의 실제 문구 → 같은 원본 이미지의 관찰로
연결한다. source-specific 게이트는 이미지 호출 전에 고정한다.

세 arm 모두 동일한 로컬 참조 파일을 사용한다. 참조는 보이는 얼굴·머리
인상에 한정하며 실제 신원·나이·성격을 추론하지 않는다. 이미지 속 역할은
허구의 성인이다. 참조 SHA:
`06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`.

일반 embodiment, 장면의 다크 판타지 의미, 선택한 새 source의 완전한
구조, 참조 외형, 서사적 한계는 각각 검토한다. 부분·가림·너무 작음은
완전한 게이트의 통과가 아니다. 참조 원본은 같은 장면의 대조 생성물이
아니므로 데이터 추가 전후의 A/B 이미지 비교로 세지 않는다.

## 이미지 실험 결과

세 에이전트가 내장 image_gen을 각각 정확히 1회 호출해 원본 3장을
받았다. API/CLI fallback과 추가 생성은 없다. 별도 ledger 3개와 독립
manifest 3개에서 동일한 최신 SKILL·참조 SHA·새 generation을 확인했다.
최종 `delivery-image.png`는 도구 원본과 바이트·SHA가 같은 전달 사본이다.
`delivery-prompt.txt`는 실제 native plan payload의 prompt 바이트다.

| 독립 장면 | 실제 검색/발생/고유 source | 새 데이터 | 원본 픽셀의 엄격한 판정 |
|---|---|---|---|
| 잠긴 성당의 마지막 뿌리 | 6/40/38 | 반환 0, 사용 0 | 고딕·침수·이상한 유물과 참조 인상은 보임. 정확한 나사 날개 접촉과 뿌리가 종 추를 감싸는 끝점은 부분 → FAIL |
| 점령군 채무 법정의 해방 거래 | 6/48/47 | 반환 0, 사용 0 | 법정·족쇄·표식·마법 실은 보임. 토큰 지지팔에 족쇄가 붙고 장부 연결점이 흐림. 끊김도 봉인 밖 → FAIL |
| 생체 갑옷을 수문 뿌리에 이식 | 6/48/44 | M08 반환 1, inspiration_only 사용 1 | 유기 내피와 조직 경첩은 실제 구현. 상단이 잘려 완전한 내피 경로는 부분 확인; 단일 끈도 복수처럼 보임 → 엄격한 전체 사례 FAIL |

세 장면의 다크 판타지 외형과 참조 얼굴·헤어 인상은 관찰된다. 첫 두
사례는 신규 source를 사용하지 않았으므로 새 데이터 효과를 입증하지
못한다. 세 번째만 새 source → 실제 prompt → 실제 픽셀의 연결이 있으며,
M08의 가시적 국소 구조 5개 게이트는 모두 확인했다. source가 문틀의
360도 전 둘레를 요구하는 것은 아니며, 보이는 문틀 가장자리–내피–조직
접힘의 관계는 성립한다. 별도로 생성 전 계획의 완전한 문틀 프레임과
갑옷 이식의 단일 끈 조건까지 통과한 것은 아니다. coordinator 엄격 전체
사례 통과는 0/3이다. 신규 source의 국소 구현 통과와 전체 장면 실패를
구분하며, 이를 native 승인이나 68개 전체 검증으로 확대하지 않는다.

M08의 source SHA는
`f5f242665b509ff59b558e5697819c1c254d93ef45b5efee1ae4ddaa89bd4d69`다.
구성요소 3개와 방향 관계 2개를 이미지 전에 고정했고 coordinator도
native-start 전 SHA를 별도로 기록했다. 실제 최종 문구는
`One continuous ribbed organic lining follows its exposed stone arch and right jamb,
folding without a break into a flexible tissue hinge at the doorway edge`다.
픽셀에서는 오른쪽 문틀을 따르는 주름 조직과 접힌 연결부가 보인다.
잘린 문틀 상단의 연결을 추정해 전체 프레이밍까지 complete로 승격하지
않았다. coordinator의 초기 프레이밍 판독도 이 source 국소 조건과
저술한 전체 프레임 조건을 분리해 최종 검토했다.

초기 카드의 `pixel_status: not_rendered`는 등록 당시의 immutable source
스냅샷이다. 이후 결과는 원본 source SHA에 묶인
[image-test-summary.json](integration-evidence/image-test-summary.json)과
개별 root review로 분리했다. 봉인된 후보 원문을 사후 수정하거나
native approval을 올리지 않았다.

| 장면 | 실제 이미지 | 실제 도구 프롬프트 | coordinator 픽셀 검토 |
|---|---|---|---|
| 고딕 | [원본 전달 사본](../../../../generated/photo-runs/dark-fantasy-gothic-20261022-7e2c/delivery-image.png) | [prompt](integration-evidence/gothic-runtime-prompt.txt) | [review](integration-evidence/root-pixel-review-gothic.json) |
| 그림다크 | [원본 전달 사본](../../../../generated/photo-runs/dark-fantasy-grimdark-20261022-d02d55/delivery-image.png) | [prompt](integration-evidence/grimdark-runtime-prompt.txt) | [review](integration-evidence/root-pixel-review-grimdark.json) |
| 유기 건축 | [원본 전달 사본](../../../../generated/photo-runs/dark-fantasy-organic-20261022-5845ac7a/delivery-image.png) | [prompt](integration-evidence/organic-runtime-prompt.txt) | [review](integration-evidence/root-pixel-review-organic.json) |

원본 이미지 SHA:

- 고딕: `99f42ccc9f282150ec278f09cec48d6c6fdad0be48922364f06cb3115ae321ad`
- 그림다크: `ea03d9767ba9dd84eea373520d6972d8423b077ebbd5a2ecec918279471aadf0`
- 유기 건축: `bc1d39d1bb71b5bc42fd6a32e4c8b62ba9b34978ea13eb1a499252d5a28d35a4`

Gothic의 broad embodiment 5개 감사는 pass여도 세부 접촉/종 추 관계
실패를 뒤집지 않는다. Grimdark는 broad embodiment도 1/5만 통과하고
4개 실패한 기록을 유효하게 감사했다. Organic은 broad embodiment와
M08 국소 게이트가 각각 5/5이고, 완전한 문틀 프레임 등 별도 실패를
보존한 채 review-audit를 통과했다. `review-audit pass`는 실패 기록의
유효성과 실제 픽셀 기술 판정을 구분해 읽어야 한다. 사용자 판단은 모두
pending이다. Coordinator review는 개별 arm 검토와 대조했으며 맹검
심미 평가나 객관적 정체성 인증으로 주장하지 않는다.

실행 중 현행 bridge의 observe가 독립 manifest 인자를 전달하지 않는
절차 경계를 확인했다. 문서가 허용한 manual native 경로로 durable
native-started → 정확한 내장 도구 payload 1회 → 실제 결과 observation →
manifest 인자를 포함한 native-result를 수행했다. 봉인 코드는 고치지
않았다. Organic의 neutral role scope 준비 실수도 로컬 준비 오류로
기록하고, 최초 작성한 실제 검색 4개 외 역할은 zero-search로 닫았다.

## 테스트에서 남은 보완 계획

1. 첫 두 독립 장면의 0개 신규 반환은 source 부재와 동일하지 않다.
   저장된 전체 순위·샘플과 full source를 대조해 의미 불일치, 순위,
   표본 노출을 구분한다. Gothic의 `without losing...` 표현이
   nonpositive로 처리되어 light_type 반환이 0인 사례는 별도 질의 경계
   개발 사례로 남긴다. 최초 독립 결과를 재검색 성공으로 덮지 않는다.
2. M08은 문틀 전체와 조직 경첩을 한 평면에 담을 수 있는 크기·여백을
   먼저 확보하는 표적 후속 사례가 필요하다. 기존 source를 잘라 의미를
   약화하지 않고, 별도 실현이 필요하면 독립된 완전한 대안으로 검토한다.
3. 손가락–나사 날개, 서로 다른 팔, 장부 attachment, 봉인–실 절단점의
   최소 기하 사례를 우선 시험한 뒤 복잡한 장면으로 돌아간다. 전체 장면의
   소유자 수와 겹침을 줄이되 기존 실패 원본·프롬프트·게이트를 보존한다.
4. 하나의 고딕 이미지에서 glamour가 수리 몰입보다 앞선 관찰은 그
   프롬프트의 후속 구도 선택에 반영한다. 이를 특정 의상·광택·표정에
   대한 범용 금지 규칙으로 확장하지 않는다.
5. 이상의 후속은 계획이며 이번 3회의 추가 생성으로 세지 않는다. 전체
   68개 후보 적합성이나 개선 효과를 확인하려면 별도의 소유자·관계·일반
   대조와 신규 독립 장면이 필요하다.

## 증거와 남은 범위

실행 산출물 루트:
`generated/maintenance/dark-fantasy-grimdark-20261022/`.
`source-preservation.json`, `canonical-source-validation.json`,
`native-index-build.json`, `working-index-build.json`, `successor.json`,
`install-validation.json`, `install-activation.json`,
`retrieval-qualification.json`, `control-exposure-review.json`,
`focused-checks.json`, `final-integrity.json`을 구분해 읽는다.

초기 36장/조건부 추가 36장의 연구 계획 전체를 실행한 것이 아니다.
이번 요청 범위는 독립 에이전트 세 개의 개별 장면 실험이다. 전체 68개
시각 후보의 픽셀 적합성, 참조 얼굴의 신원 일치, 예술적 개선과 사용자
수용은 별도로 남는다. 이 작업은 커밋·푸시하지 않았다. 작업 중 별도
liminal 게시 커밋으로 HEAD가 움직인 사실은 무결성 기록에서 분리한다.

# 반영 계획

2026-10-23. 이 문서는 후속 구현 계획이다. 현재 실행한 것은 연구 폴더 작성, 소스 스냅샷 대조와 연구 자료 검증이다.

## 1. 반영 단위와 우선순위

| 우선순위 | 대상 | 반영 내용 | 완료 조건 |
|---|---|---|---|
| P0 | 의미 분리 | 역할/충성/동기/법적 지위/동의/효능을 문맥으로 유지. 배우 포즈-카메라, 실물-매체상, 자기 손-상대 옷 분리 | 혼동 사례가 물리적 의미를 바꾸거나 추가 사건을 만들지 않음 |
| P1 | 전달·시선·접촉 | 봉투의 두 끝, 미완료 전달의 빈틈, 장치-귀-손, 수화기 양 끝, 거울 경계, 상대 타이, 부축, 수갑 연결 | 선택한 실현의 소유자와 모든 핵심 접점이 보존됨 |
| P1 | 기존 소스의 주장 정밀화 | 무흔적 장갑, 이어피스/수화기 모호성, 피팅 전제, 의복 층/드레이프의 기존 추가효과 검토 | 원래 조건을 우회하지 않으며 비가시 성능을 새 시각 사실로 쓰지 않음 |
| P2 | 의복 구조 | 별도 조끼, 여밈, 라펠, 트렌치 부품, 망사/안감/개구, 가터 연결, 리그/캐리어 | 구조별 완결 대안과 조건·효과 검토 완료 |
| P2 | 일반 외형 재사용 | 직접 카드가 없는 외형 용어 65개를 기존 후보의 전체 의미와 비교 | 각 항목을 reuse/refine/new/context/defer 중 하나로 결정 |
| P3 | 미세·실물·시간 | 역사 카메라, 미세 점, 숫자/문서 판독, 재단/소재/방호 주장 | 실제 도판·투영 검토 뒤 구체적 범위만 승격; 단일 프레임으로 증명 못 하는 내용은 계속 문맥 |

65개 미연결 외형 항목은 [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md)의 defer 행이다. 순서: 포즈·손·지지 → 여밈/칼라/일체형 경계 → 안경/가방/신발 착용 → 헤어/표면. ‘평범한 옷’·‘핀업’·‘페티시웨어’·‘직업복’ 같은 상위 문맥은 하나의 자세나 노출로 축소하지 않는다.

## 2. 소스별 결정을 확정한다

먼저 현재 HEAD, manifest, source module closure, native CURRENT와 설치된 H-F2 선택을 다시 읽는다. 연구 시작 때 이미 많은 별도 변경이 있었으므로 이 패키지의 해시를 현재 구현 원본으로 가정하지 않는다.

기존 24개 원문·조건·효과·binding 스냅샷은 [existing-source-mapping.json](existing-source-mapping.json)에 있다. 구체적인 판정은 [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md)를 따른다.

- **reuse**: 기존 완전 문장의 뜻과 모든 부수 효과가 현재 요청/실현에 맞을 때 ID와 원문을 유지한다.
- **refine**: 누락된 소유자·접점·번역 범위·효과 표기가 있으면 바뀌는 의미를 명시한다. 영향받는 기존 문맥을 조사하고 별도 대안을 만들지 여부를 결정한다.
- **new**: 전체 기존 소스와 비교해 같은 완전 실현이 없을 때만 신규 CID/RID를 부여한다. 어휘 0건은 근거가 되지 않는다.
- **context**: 장르·기관 역할·충성·동기·의도·효능은 positive visual 후보와 분리된 진단/문맥으로 둔다.
- **defer**: 표본, 소스, 실제 owner 계약, 화면 판독이 부족한 경우 보류한다. 보류는 삭제나 의미 부정이 아니다.

트렌치 세 레코드나 슬립 드레스 이웃 네 레코드를 단순 합쳐 완결 후보로 취급하지 않는다. 다른 소스의 조건이나 선택하지 않은 branch의 사실을 빌려오지 않는다. 별도 조끼·티셔츠·카디건·젖은 헤어처럼 기존 소스가 실제로 바꾸는 요소를 유지하거나 다른 완결 대안을 선택한다.

## 3. 운영 데이터 초안을 만든다

제안 파일:

- assets/photo_espionage_semantics_20261023.json: 의미 경계, 출처와 명시적 문맥 경로.
- assets/photo_candidate_espionage_20261023.json: 승인한 완결 시각 대안만.
- assets/photo_candidate_espionage_bindings_20261023.json: 실제 역할과 적용 조건을 검토한 optional binding만.
- references/espionage-semantics.md: 등록 범위·제약·검증 결과.

위 파일은 현재 생성하지 않았다. 운영 스키마는 구현 시점의 유지보수 계약을 따른다. 연구의 draft ID/esp_* ID를 runtime ID로 개명하는 것만으로는 반영이 성립하지 않는다.

각 실제 CID/RID에 한영 본문, 전체 intrinsic conditions/effects, 각 소유자와 실제 property 경로, 필요한 기존 구성원, role binding 조건을 작성한다. 정적 배열에 불필요한 새 행위자·이력을 넣지 않는다. 귀-장치-손 후보가 귀의 기존 장치가 필요하다면 그 전제를 명시한다. 장치를 새로 추가하는 대안은 별도 효과를 검토한다.

연구 그래프는 native frozen fact나 source proof가 아니다. 각 실제 realization의 positive field-local source anchor, owner/receiver, source guard, 전체 효과와 선택된 의무를 현재 도구로 검토한다. 태그·출처 URL·카드 gate가 그 증거를 대체하지 않는다. qualification이 없는 데이터는 discovery-only/review-required 상태를 유지한다.

새 슬롯은 우선 만들지 않는다. body_pose/hand_pose/contact_point/gaze_target/relational_action/prop_state/wearable_accessory 등의 현재 catalog 정의와 구체적인 속성 범위에 맞는 binding만 채택한다. 연구 카드의 role 목록은 탐색 후보이지 동일한 후보를 모든 role에 허용하는 명령이 아니다. 특히 의복 구조의 주 role은 catalog의 해당 garment property와 원래 appearance 조건을 먼저 검토한다.

## 4. 소스 무결성과 인덱스를 별도로 검증한다

먼저 실제 반영한 데이터에 dictionary/source/owner/binding 검사를 실행한다. 영향을 받는 기존 계약의 focused tests를 우선한다. 후보 검증, role 경계, H-F2 의미/전제/원문 경계가 대상이다. 변경 범위나 실패가 넓은 회귀 위험을 보일 때만 검사를 확장한다.

검증 명령은 현재 checkout에서 실제 지원을 확인한 후 실행한다. 현재 계획에 참고한 entrypoint:

    python3 skills/photo-prompt-image-generator/scripts/photo_installed_h_f2.py --check-runtime
    python3 skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
    python3 skills/photo-prompt-image-generator/scripts/build_shared_candidate_index.py --verify

연구 검증기는 위 source 검증을 대신하지 않는다. 실제 소스 변경 후에는 **정확한 최종 source union**으로 별도 staging index를 만든다. 문서 ID·텍스트 해시·recipe·provider/model·차원·vector integrity가 모두 맞는 벡터만 재사용한다. 예전 벡터를 새 recipe로 재표기하지 않는다. 모델 파일 경로와 런타임 Python도 재확인한다.

source/index의 closure, 통계와 문서/vector 수, 선택된 realization을 검증한 뒤 설치를 별도로 진행한다. H-F2는 설치된 sealed copy를 읽으므로 assets 편집이나 native index 성공만으로 기본 검색이 달라지지 않는다. 검증 전 CURRENT나 설치 선택을 바꾸지 않는다.

## 5. 검색 평가와 실제 채택을 분리한다

[EVALUATION-PLAN.md](EVALUATION-PLAN.md)의 206사례/412질의를 원본과 stage에 같은 조건으로 실행한다. 원문 smoke 138개와 자연어 24개를 나눠 보고한다. 기존 코드가 지원하는 실제 전체 공통 pool의 BM25F/local embedding/RRF 결과를 저장한다. 임의 slot prefilter, 별도 주제 전용 pool, 키워드 강제 승격으로 성능을 만들지 않는다.

topic·baseline·해당 slot의 독립 질의별 top 결과, 실제 CID/RID, source hash, rank, lane, 선택 여부와 이유를 남긴다. 검색된 카드가 아니라 **허용되는 전체 소스 의미가 보존된 선택**을 평가한다. 후보가 검색되어도 소유자나 잠긴 속성을 바꾸면 채택 실패다.

일반 통근자에 코트 후보가 노출되는 것 자체는 실패가 아니다. 그 요청에 무기·감시 의도·성적 협박을 자동으로 부여하는 것이 실패다. 한영 차이와 직역/자연어 차이를 별도로 보고한다. 독립 holdout은 외부 작성·동결 전까지 PENDING이다.

## 6. 이미지 검증

[PIXEL-PLAN.md](PIXEL-PLAN.md)의 초기 12개 장면을 baseline/stage 한 쌍씩 비교하는 24장 계획을 사용한다. 현재 이미지 호출은 0이다. 실제 실행 시 각 요청의 독립 core/locks와 선택 소스, 최종 prompt 및 runtime receipt를 고정한다. 단순히 stage 프롬프트를 더 길게 만든 조건과 비교하지 않는다.

모든 핵심 접점이 한 프레임에 읽혀야 한다. 일부만 보이면 partial_is_fail, 가리거나 너무 작아 판단할 수 없으면 UNOBSERVABLE_NOT_PASS다. 차단된 결과는 BLOCKED_UNSCORED로 보존한다. 반복이 필요하면 새 비교로 분리하고 최초 실패를 유지한다. 생성 모델의 동일 seed나 비결정성이 통제되지 않으면 원인 효과로 단정하지 않는다.

## 7. 단계별 완료 판정과 복구

연구 → source registration → source qualification → staging search → 실제 선택/프롬프트 반영 → 정확한 요청 전송 → 저장 이미지의 gate → 사용자 수용을 각각 기록한다. 앞 단계의 PASS를 뒤 단계로 복사하지 않는다.

마지막 활성화 전에 검증된 설치본을 --no-activate 등 지원되는 별도 경로로 확인하고, 그 뒤에만 기본 선택을 전환한다. 이전 sealed generation과 config를 복구 가능하게 보존한다. 실패 시 이전 선택으로 돌아가되 실패 자료는 삭제하지 않는다.

버전 관리가 후속으로 요청되면 explicit allowlist로 이 변경만 stage한다. 기존 dirty/untracked 파일과 runtime 실험을 포함하지 않는다. commit, push, 배포, 사용자 수용은 별도 상태다. 현재는 어느 것도 수행하지 않았다.

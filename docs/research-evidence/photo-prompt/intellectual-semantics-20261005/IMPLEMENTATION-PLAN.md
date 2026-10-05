# 시각 의미·후보팩 데이터 반영 계획

상태: **PLANNED_NOT_IMPLEMENTED**. 140개 어휘 결정을 완료하고 78개 보강 단위를 준비했다. 원본 대화·외부 근거·기존 데이터와 초안을 연결했으며, 활성 assets·index·generator·tests는 이 요청에서 변경하지 않는다.

## 목표와 완료 정의

목표는 요청된 지적 인상·탐구 활동이 정확한 actor–자료–도구 관계로 표현되고, 적합한 후보가 후보팩에 실제로 노출되며, 채택 시 본래 의미·손 역할·인원·옷·시점·텍스트를 보존하는 것이다. 명시되지 않은 지능·신분·정신 건강·성적 지향·동의·유죄·시간 전환을 판정하는 분류기는 만들지 않는다.

구현 완료에는 authored 데이터의 구조 검증뿐 아니라 **필요 프로파일 노출, 후보 선택 또는 정당한 거절, 효과 보존, required 관계가 남은 최종 프롬프트, 원본 이미지 all-of 판정**이 필요하다. 연구 패키지의 무결성 PASS는 구현이나 이미지 PASS가 아니다.

## P0. 구현 시작점과 중복·소유 결정

**입력:** [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json), [AUTHORING-INVENTORY.json](AUTHORING-INVENTORY.json), [TERM-DECISIONS.json](TERM-DECISIONS.json).

1. 기존 HEAD·authored 해시·등록 manifests와 현재 체크아웃을 비교한다. 다른 작업의 변경이 있으므로 원래 해시로 덮어쓰지 않는다. 구현은 필요하면 별도 worktree에서 수행하고 사용자 작업을 보존한다.
2. 60개 재사용 후보 ID와 7개 프로파일을 `(file,slot,id)` 단위로 재확인한다. 배열 순서에 의존하지 않는다. 같은 의미를 다른 ID로 중복 생성하지 않는다.
3. `pv_steepled_fingers`, `pv_interlaced_fingers`, `pv_chin_support`, `pv_book_read`, `ae_lip_press/purse/pucker`, portrait 원자, `rembrandt_face_light_pattern`은 재사용 우선이다.
4. [ADOPTION-MAP.json](ADOPTION-MAP.json)의 각 단위를 **reuse / extend-existing / new-atomic / new-bundle / context-only / defer**로 확정한다. 제안된 파일 위치도 owner 의미에 맞게 확정한다.
5. 사전의 추상 형용사, 40/57/59/82의 시간 개념, sapiosexual의 비시각 정체성, 밝은 학구풍의 저작 연출명은 하드 외양 프로파일과 분리한다.

**산출물:** 채택 ID·현재 owner·기존 meaning 비교·추가 근거·전체 effects가 있는 결정 표. 새 activity owner가 필요한 이유와 기존 owner에 남길 항목도 명시한다.

**종료 조건:** 140개 모두 분류되어 있고 기존 ID와 의도치 않은 긍정 별칭 충돌이 없다. ‘라벨 22/140’ 또는 ‘exact profile 0/140’을 갭 수량으로 쓰지 않는다.

## P1. 기존 원자 보강과 충돌 교정

**우선 항목:** 턱 지지 변형·전완 지지·뒷손목 접촉, 페이지 고정·페이지 기부, pen hover/contact, 안경 상태·브리지 접촉, 단일 눈썹·입술 형상, camera height/direction/crop 분리.

| 작업 | 주 owner / 재사용 | 실제 변경 방향 | 필요한 검증 |
|---|---|---|---|
| 턱·뺨·전완 지지 | pose vocabulary, `pv_chin_support` | 넓은 원자는 유지하고 구체 laterality·contact 변형을 별도 컴포넌트/프로파일로 결속 | R014–R022, H01 |
| 읽기·페이지·펜 | `pv_book_read`, activity owner 검토 | page margin, corner pinch, root attachment, hover/contact를 별도 relation 상태로 정의 | R023–R025, H02–H03 |
| 안경 | accessory 원자 재사용 + activity interaction | worn/removed 상태·프레임 보존·bridge contact·eyes above rim을 분리 | R026–R028, H04 |
| 얼굴 | acting expression | exact/paraphrase 보강이 필요할 때만 범위 좁게 추가. 기존 purse/pucker/press를 합치지 않음 | R035–R041 |
| 방향·크롭·초점 | portrait + 현재 camera/focus 원자 | three-quarter angle/length, profile document/view, deep-space/focus를 별도 뜻으로 유지 | R042–R054, H13 |
| 조명·반사 | 기존 light/background 프로파일 | 실물/반사/투과 소유, 광원–조사 면, 필수 문서 가독성 연결 | R053–R056, H14 |

**필드 원칙:** positive definition·components·paraphrases에 실제 형태와 정확한 뜻을 둔다. 지능·직업·정체성 추론 금지, 대비 사례, 오케스트레이션 지시는 별도 claim limit/contrast 필드다. 단순히 `not`를 지워 긍정 문장으로 만들지 않는다. 예를 들어 pen hover의 ‘비접촉’은 실제 긍정 의미이고, ‘필기는 요청하지 않았다’는 requester negation이다.

**종료 조건:** 기존 뜻·guard·효과를 보존한 재사용과 narrow refinement가 구별되고, laterality·actor 소유·contact 상태가 실행 계약에서 표현된다. required 접점을 구체 구성요소 모두로 풀 수 없다면 하드 프로파일을 만들지 않는다.

## P2. 문서·기록·도구의 관계 원자

새 활동 묶음에 앞서 다음 공통 원자를 구축한다.

- `ia_annotation_anchor`, `ia_correction_anchor`: 원문 행–표지–주석/대체어의 대응.
- `ia_comparison_matrix`: 같은 criterion·서로 다른 object column·지정 difference cell.
- `ia_structured_board`: 소수 노드의 전제–중간–결론과 화살표 endpoint.
- `ia_revision_sequence`: 같은 문단의 소수 버전과 변경 note.
- `ia_reference_link`, `ia_deictic_reference`, `ia_gaze_reference`: 손·눈·표지의 대상 anchor.
- `ia_ruler_measure`, `ia_caliper_measure`, `ia_magnifier_target`: 도구마다 다른 접점·배치.

**저장 후보:** `photo_prompt_intellectual_activity_extension.json`. 기존 everyday/pose/실물·도구 owner가 같은 뜻을 이미 가진 경우 그 stable ID를 먼저 활용한다. 새 registry가 필요하면 대응 `photo_prompt_visual_obligations_intellectual_activity.json`을 만들되, 명시된 작업의 비대체적 관계에 해당하는 좁은 프로파일만 required 활성화를 허용한다.

**자료 fixture:** 짧은 문단 A, 비교표 A/B, x+3=7→x=4, 원자료 A=(2,3), 식별자 E1 등을 별도 저작한다. 과도한 작은 글자나 복잡한 도식을 첫 검증 대상으로 삼지 않는다. 일반 분위기의 자료와 exact text 요구를 분리한다.

**종료 조건:** 최소 relation unit마다 source/target 소유자, 접촉·참조의 대상, 관련 텍스트 요구, 모든 영향 차원을 선언한다. 필수 anchor의 가독성·크롭·가림도 소유 의미의 일부로 검토한다.

## P3. 첫 활동 묶음: 정독·교정·대조·디버깅·분석·동료 검토

첫 구현은 여섯 대표 묶음으로 한정한다.

1. **정독:** 기존 `pv_book_read` + page support + gaze/source line + anchored annotation.
2. **판본 대조:** corresponding passage A/B + difference note + 정확한 pointer target.
3. **교정/유도:** left/right hand roles + page support + pen contact + 짧은 검증 식 또는 수정 문구.
4. **디버깅:** 같은 filename/line의 code/traceback + 지정 조사 상태 + 입력 손.
5. **데이터 분석:** 동일 관측의 source row/plot point + 축/단위 + pointer target.
6. **동료 검토:** 요청된 두 actor + draft/comment anchor + writer/reviewer 소유 + 현재 gaze/pen 상태.

**조합 방식:** 묶음 라벨 하나로 세부 의무를 숨기지 않는다. authored component에 후보의 stable ID와 실제 relation을 연결하고, 선택 후 손 역할·문서 target을 core binding에 맞게 확정한다. 추가 인물은 묶음 후보의 권한이 아니다.

**종료 조건:** R058–R070의 채택된 사례에서 expected IDs가 candidate pack에 실제로 노출되는지 기록한다. 옵션이 부적합하면 이유 있는 거절이 유효하다. 사용자 명시 required 관계를 충족하지 않은 후보팩은 렌더 전에 fail closed로 보고한다.

## P4. 나머지 활동과 문화·성인·허구 변형

P3의 동일 자료·손 역할이 안정된 뒤 실험·현장 측정·도면/모형·체스/바둑·작품·악보·번역·설명·야간·자연 스케치로 확장한다. 도구별 물리 기하, 기보 합법성, 악보·번역 의미, 역사 복식은 각각 검증 가능한 fixture와 추가 1차 근거를 갖춘 항목만 정확성 의무를 주장한다.

다크 아카데미아·밝은 학구풍·긱 시크는 setting/style과 기본 활동을 분리한다. 긱 시크 프레임은 accessory 의미로 처리하며 성인 매력 축을 자동 추가하지 않는다. 명시 성인의 오피스 사이렌·독서 의상·플러팅에는 기존 contextual appeal의 권한·축·잠금 계약을 적용한다.

위험 흔적·mastermind·심문·허구 실험·전쟁 상황실·증거 검토·감금·고전 누드는 명시 event/role/medium과 실제 접촉·자료 관계를 따로 보유한다. 단어만으로 범죄·정신질환·현재 전쟁·실제 지향·누드를 자동 추가하지 않는다.

**종료 조건:** 같은 활동의 기본·문화·성인·허구 변형에서 actor count, identity, hand ownership, document anchor, crop, wardrobe lock을 모두 보존한다. 비시각 정체성이나 시간 개념을 픽셀 라벨로 승격하지 않는다.

## P5. 데이터 계약·등록·파생 인덱스

현재 구현 경로는 core freeze 후 retrieval → visual profile resolution → concepts/obligations → immutable candidate pack/v6다. [retrieval-contract](../../../../skills/photo-prompt-image-generator/references/retrieval-contract.md), [hybrid augmentation contract](../../../../skills/photo-prompt-image-generator/references/hybrid-augmentation-contract.md)를 구현 시작 시 현재 버전으로 재확인한다.

**실제 대상:**

- 기존 authored owner 파일 또는 검토된 새 activity extension/registry.
- `prompt_generator.py`의 `RESEARCH_EXTENSION_FILENAMES`, `VISUAL_OBLIGATION_EXTENSION_FILENAMES` 등록은 새 파일이 실제로 필요할 때만 변경.
- 기존 `photo_candidate_semantics.py`, `visual_profile_contracts.py`, `photo_contracts.py`로 structure·effects·scope 검증.
- `build_semantic_index.py`, `build_visual_profile_index.py`로 **병합된 authored sources**에서 파생 인덱스 재생성.

이 주제 전용 정규식·키워드 라우터나 두 번째 의미 저장소는 계획하지 않는다. 새 관계가 현재 generic 계약으로 표현되지 않으면 계약의 일반적 표현력을 먼저 검토하고 별도 변경 사유·호환성 검증을 남긴다. 연구 초안의 `proposed_relations.predicate`를 현재 enum이라고 가장하지 않는다.

`affected_dimensions`만 열렸다고 partial property lock과 호환되는 것은 아니다. 실제 `dimension / target / property`를 source-grounded actor·document·tool에 결속하고, 후보가 바꾸는 모든 실제 효과를 신고한다. 예를 들어 안경을 낮추는 over-glasses 변형은 expression뿐 아니라 eyewear 위치/착용 효과가 있으며, 읽는 문서가 보이게 카메라를 바꾸면 framing/camera 효과도 있다. 효과를 축소하여 잠금을 우회하지 않는다.

원자·묶음의 `existing_slot_context_extensions`는 실제 현재 schema가 허용하는 문맥 보강에만 쓴다. 기존 후보의 내용을 교체하거나 guards·effects를 제거하는 수단으로 쓰지 않는다. embedding cache는 input bytes·provider/model·차원 메타데이터가 호환될 때만 재사용한다. 생성된 index는 ours/theirs 선택으로 충돌을 해소하지 않는다.

**종료 조건:** 구조·소유·효과 검증 통과, 기존 의미 변경 없음, raw contrast·claim limit이 positive prototype에 섞이지 않음, resolver가 새 authored 내용을 실제 사용, source/index freshness 증거 확보. 후보 78개를 동시에 노출하는 목표는 없다. 현 계약의 같은 slot 후보 수·전체 노출 cap과 선택적 조합을 따른다.

## P6. 실행 검증·이미지 비교·채택 보고

**자동 검증:** [REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 82개 프로브를 채택 stable ID에 바인딩하여 실행 가능한 테스트로 전환한다. 단순 동의어 치환으로 테스트 수를 부풀리지 않는다. sense collision, negation, context, contact, laterality, count, full effect, property lock, temporal unsupported를 실제 assertion으로 검증한다.

관련 기존 검증군은 `test_photo_candidate_semantics.py`, `test_photo_visual_profile_retrieval.py`, `test_photo_semantic_index.py`, `test_photo_retrieval_runtime_improvement.py`, `test_photo_pose_vocabulary_semantics.py`, `test_photo_acting_expression_data.py`, `test_photo_portrait_composition_semantics.py`, `test_photo_lighting_visual_semantics.py`, `test_photo_realistic_background_semantics.py`, `test_photo_adult_appeal_visual_semantics.py`, `test_photo_violence_crime_visual_semantics.py`다. 실제 수정 owner에 해당하는 군과 공통 계약 검증을 수행하고, 실패는 baseline과 비교해 새 실패/기존 실패를 구분한다. 현재 패키지에서 이 테스트들을 실행했다는 뜻은 아니다.

**첫 픽셀 파일럿:** H01/H02/H03/H06/H08/H09/H12와 H15의 세 스타일을 대상으로 baseline/enriched 각 3회 독립 반복을 제안한다. 총 **10개 구체 요청 × 2개 arm × 3회 = 60개 이미지**다. 생성 도구가 seed를 제공하지 않으면 독립 반복으로 기록한다. 두 arm은 같은 provider/model·크기·요청·스타일·기본 core를 사용하고, 실험 arm에서 데이터 증분만 적용한다. 요청은 자연어로 표현하며 runtime ID·프로파일명을 넣어 검색을 유도하지 않는다. 최종 prompt의 차이도 저장한다.

**실행 절차:** generator skill의 pre-core 접근 경계를 유지한다. baseline과 독립 core를 확정·동결한 뒤 assets와 candidate pack을 조회한다. agent의 visual priority는 advisory이며 사용자 hard 요구를 새로 만들지 않는다. 비교가 이미지 도구에 전달된 prompt까지 도달했는지 별도 기록한다.

**보고 지표:**

| 단계 | 분모·증거 | 완료 판단 |
|---|---|---|
| 데이터 | 채택된 행·source·relations·effects | 누락·중복·dangling reference 없음 |
| retrieval/profile | 문맥·잠금상 eligible한 요청 | expected stable IDs의 실제 노출. required와 advisory 분모 분리 |
| 선택 | 노출된 후보와 composer 기록 | 필요한 관계 채택 또는 부적합 이유 있는 optional 거절 |
| 의도 보존 | 채택 후보의 전체 effects와 core locks | 비요청 인물·소유·옷·시점·텍스트·event 변화 0 |
| 최종 prompt | 실행 도구에 전달한 원문·해시 | required 지지·접촉·참조 관계 보존 |
| native pixels | 원본 이미지별 16개 all-of 묶음 중 적용 항목 | 모든 required 관찰 절 충족. 보이지 않음·읽히지 않음·불확실은 통과 불가 |
| 사용자 수용 | 결과·한계·실패 이미지의 검토 | 요청된 의미의 보존 여부 별도 확인 |

생성 차단·도구 실패·부분 성공을 분모에서 빼지 않는다. 차단은 내용/도구 상태와 이미지 평가 불가를 따로 기록한다. 개선 평균만으로 전체 의미의 구현을 선언하지 않으며 작은 파일럿의 범위를 명시한다. 이미 통과한 체크는 새 변경·실패·미해결 위험이 없으면 반복 확장하지 않는다.

## 실행 순서와 반영 중단 기준

순서는 **P0 → P1 → P2 → P3 → P5의 등록/재빌드/프로브 → 첫 P6 파일럿 → P4 확장 → 남은 P6**다. P1–P4 변경은 owner별 작은 증분으로 나누고 각 증분에서 재빌드와 필요한 체크를 수행한다.

원래 뜻을 교체해야 하거나, 필요한 property scope가 불명확하거나, 정확한 actor/document/tool binding이 없거나, required 관계가 pack·최종 prompt·픽셀 중 어느 한 층에서 빠지면 그 항목의 채택을 보류한다. 나머지 독립 항목의 작업은 계속할 수 있다. 문서에서 source를 읽은 것, 구조 테스트를 통과한 것, 이미지 일부 요소가 맞는 것을 전체 성공으로 합치지 않는다.

최종 구현 보고에는 채택/재사용/보류 ID, authored 변경, 인덱스 freshness, 프로브 결과, 후보팩 노출·선택, 원본 픽셀 판정, 미검증 경계, commit/push/PR 상태를 따로 남긴다. 이 연구 요청에서 commit·push·publish는 수행하지 않는다.

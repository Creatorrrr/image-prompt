# 시각 의미·후보팩 반영 계획

2026-10-05 KST. 이 계획은 [리서치 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/RESEARCH.md)와 [120항목 대응표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/CATALOGUE.md)를 실제 작성 자산으로 옮기는 순서다. **이번 작업에서는 이 계획을 실행하거나 활성 자산을 수정하지 않았다.**

## 1. 반영 목표와 유지할 계약

목표는 유혹 관련 단어가 더 많이 검색되는 것뿐 아니라, 요청된 눈·입·손·지지·시점·빛이 **정확한 소유자와 변경 범위로 노출되고 선택될 수 있는 것**이다. 넓은 분위기어가 상세 포즈·체형·의상·상대 인물을 강제하는 규칙은 추가하지 않는다.

유지할 계약:

- 현재 `photo-candidate-pack/v6`와 64개 후보 상한을 유지한다. 데이터 보강을 위해 슬롯·랭킹·상한을 재설계하지 않는다.
- 최초 해석/authorial core 확정은 후보팩·registry·index 검색 전에 수행한다. 이후 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → 요청별 의무/개념 후보/clarification → 불변 pack 순서를 유지한다.
- 사용자 정의, 부정, 고정 인물/시점/옷/소품, 열린 차원과 속성 잠금을 먼저 적용한다.
- `candidate_only` 묶음은 선택 대안이다. 프로필 활성화는 독립적인 요청 근거에 따라야 한다. 묶음·검색 점수·순위가 하드 의무를 만들지 않는다.
- ID로 작성 데이터·노출·선택·프롬프트·픽셀을 연결한다. 배열 첫 번째 항목을 의미적 기대값으로 사용하지 않는다.
- 출처 URL·논문 제목·조사 일자·연구 한계는 연구 폴더에 둔다. 임베딩용 긍정 텍스트에 부정 예시·검증 명령·메타데이터를 섞지 않는다.

## 2. P0 — 의미와 변경 범위를 먼저 확정

### 2.1 정의/별칭 경계

1. `pv_asymmetric_mouth`의 `Smirk` 별칭을 검토한다. 형태적 비대칭은 유지하고, 자기만족/장난의 의미는 별도 문맥 후보로 남긴다. exact alias 삭제가 다른 기존 요청에 미치는 영향도 함께 비교한다.
2. `pv_half_lidded`의 넓은 정의를 유지한다. 스퀸치·윗눈꺼풀 중심 변형은 더 좁은 의미로 구분한다.
3. 신체의 dropped shoulder와 의복 봉제선을 분리한다. 양방향 문맥/부정 사례를 만든다.
4. 자기 어깨 돌아보기와 다른 사람 어깨 전경의 OTS, 몸 3/4 방향과 3/4 shot, reverse chair와 straddle을 분리한다.
5. 15개 해석어는 선택 대안만 제공한다. 9개 시간 항목은 현재 정지 상태를 전체 시간 의미와 분리한다.

### 2.2 owner/target/property 매핑

각 후보를 다음 표로 확정한다. 이는 구현 전 필수 검토표이며 새 런타임 스키마가 아니다.

| 항목 | 확정할 내용 | 미확정일 때 |
|---|---|---|
| owner | 주체/상대/거울 반사/카메라/광원의 실제 core ID | 후보를 채택하지 않음 |
| 부위 | 어느 손·눈·입술·볼·어깨인지, actor-left/right와 화면 좌우 | 무지정이면 임의 좌우를 만들지 않음 |
| object/target | 자기 부위, 기존 옷/장식, 기존 상대, 지지면, 렌즈 | 관계 후보가 새 객체를 만들지 않음 |
| changed dimension | expression/pose/appearance/lighting/camera/composition 등 실제 변화의 합 | 효과가 넓으면 잠금에 보수적으로 거절 |
| changed property | 실제 잠금의 부모/자식 경로와 겹치는 정확 속성 | 텍스트 이름만 새로 써서 잠금을 우회하지 않음 |
| prerequisite | 이미 존재해야 하는 라펠/펜던트/상대/모발 배치 | 산문 조건만 믿고 적용하지 않음 |
| observability | 크롭, 거리, 초점, 가림으로 보이는 필수 요소 | `UNOBSERVABLE`;전체 PASS 아님 |

`contact_point`의 슬롯 기본 차원만으로 자기 손 접촉의 pose 변화가 전부 포착되지는 않는다. `gaze_target` 등 기본 차원이 비어 있는 슬롯도 있다. 기존 policy를 확인해 실제 효과를 명시한다. appearance를 바꾸는 hair tuck/fabric pinch는 손 자세만으로 선언해서 의복/모발 잠금을 빠져나가면 안 된다.

초안에 쓰인 `hair`, `garment`, `eyes.light_reflection`, `face.illumination_pattern`, 카메라/scene의 제안 경로를 실제 고정 core와 대조한다. 기존 `face.expression` 같은 넓은 부모 효과가 일부 표정 잠금과 충돌하면 그대로 거절한다. 세분된 경로를 추가하는 경우 실제 resolver/lock 검사를 함께 검증해야 한다. 지원되지 않으면 상위 효과를 보존한다.

**P0 완료 조건:** 120항목의 해석/형태/시간 분류, 소유 좌표, 주요 혼동 경계가 리뷰되고, 설치할 각 후보의 실제 대상·속성·실행 조건이 확인된다. 불명확한 항목은 선택 후보 또는 연구 제안 상태로 남긴다.

## 3. P1 — 기존 ID와 소유 파일을 먼저 보강

22개 기존 후보, 14개 기존 프로필 보강안이 출발점이다. 정확한 기존 필드와 제안 patch는 [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/CANDIDATE-DRAFTS.json), [프로필 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/PROFILE-DRAFTS.json)에 있다. patch를 자동 합집합으로 적용하지 않는다. 충돌 설명·별칭은 최종 의미 하나로 편집하고 기존 가드는 유지한다.

| 대상 | 기본 소유 파일 | 주요 보강 |
|---|---|---|
| `ae_squinch`, `ae_lip_bite`, `ae_sultry_variant`, `ae_coquettish_variant`, `ae_smolder_attraction` | [acting expression extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_acting_expression_extension.json) | 눈꺼풀/치아-입술의 경계, 실제 소유, 기존 adult/attraction 가드, 비유혹 문맥 |
| `ae_profile_squinch` | [acting expression obligations](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_acting_expression.json) | 열린 눈·아래 경계·윗눈꺼풀 중심 대체 실패, 원본 얼굴 게이트 |
| `pv_half_lidded`, `pv_asymmetric_mouth`, `pv_parted_lips`, `pv_shoulder_lower`, `pv_chin_support`, `pv_collarbone_touch`, `pv_lapel_grip` | [pose vocabulary extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json) | 넓은 의미 보존, lip/shoulder 좌표, touch/grip/support, 손·접촉 효과 |
| chin support / reverse chair / straddle 프로필 | [pose vocabulary obligations](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_pose_vocabulary.json) | hover 경계, 의자 방향/다리 배열, 지지 접점 |
| `reaching_toward_camera`, `tucking_hair_behind_ear`, `playful_smirk` | [tags](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) | 레거시 필드 보강, 팔/모발 소유, 형태와 태도 구분 |
| `ctx_c126` | [contextual appeal extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_contextual_appeal_extension.json) | 작업 집중 원래 의미·행동 보존, 입술 접점 명확화 |
| `sff_pro_l01/l05/l07/l08` | [fashion lighting source](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_sensual_fetish_fashion_extension.json) | split/loop/short/broad 단위, 투영 면 좌표, affected_properties 검토 |
| `lit_clean_vertical_catchlight_pair` | [lighting extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_lighting_extension.json) | 두 반사점이라는 좁은 의미와 눈/광원 소유·효과 |
| `pc_pc17_component_2`, OTS 구성 후보/프로필 | [portrait composition extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_portrait_composition_extension.json), [obligations](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_portrait_composition.json) | 전경 shoulder의 다른 actor 소유, 초점/시점 실제 target |
| contrapposto·languid·기존 주요 조명 프로필 | [base obligations](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json) | 원래 안정된 정의 유지, 가시성·시간·short/broad의 별도 축 |
| tongue/lip boundary | [slang obligations](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_slang_visual.json) | 기존 혀/입 경계 재사용, 실제 접점과 이동 미검증 |

파일별 위치는 작성 시점 소유 목록이다. 구현 전에 중복 ID나 진행 중인 변경을 다시 확인한다. 같은 후보가 여러 소유 파일에서 정의되면 현재 loader 합성 규칙을 확인해 최종 유효 record를 판정한다.

현재 일부 legacy 후보 안의 `research_source_urls`, `research_origin_id`, `research_confusions`는 유지보수 지침의 연구/런타임 분리와 맞지 않는 부분이다. 이번 대상 record에서 필요한 출처·반례를 연구 폴더로 옮기고 런타임에는 긍정 의미와 지원되는 제외/문맥 필드만 남기는 방안을 검토한다. 다른 미관련 record 전체를 함께 정리하지 않는다.

**P1 완료 조건:** 기존 의미·가드·ID를 보존한 최종 필드가 있고, owner/effects와 혼동 회귀가 통과한다. 이 단계에서 이미 필요한 관계를 모두 표현할 수 있으면 신규 record 수를 줄인다.

## 4. P2 — 빈 세부 형태만 추가하고 선택 묶음으로 연결

14개 신규 후보 제안은 다음과 같다. ID는 제안 ID이며 활성 데이터에 아직 없다.

| 원 번호 | 후보 제안 | 설치 전 핵심 조건 |
|---|---|---|
| 18 | `se_lash_occluded_upward_gaze` | 눈 방향·턱 pitch·속눈썹;기존 bashful direct와 중복 검토 |
| 19 | `se_upper_lid_dominant_half_lid` | 넓은 half-lidded를 보존한 좁은 하위 의미 |
| 30 | `se_eye_visible_through_own_hair` | 같은 주체 모발/눈;모발 잠금;가시 시선 |
| 71 | `se_edge_on_hand_to_camera` | 실제 손 평면;손 크기 고정 |
| 72 | `se_two_hands_different_heights` | 같은 두 손/팔 소유;몸통 기준 높이 |
| 73 | `se_cheek_fingertip_light_touch` | 자기 볼 손끝 접점;넓은 얼굴 만짐과 구분 |
| 74 | `se_hand_hover_below_chin` | visible gap;지지 프로필과 반대 조건 |
| 76 | `se_one_hand_behind_head` | 한 손만;반대 손 잠금 |
| 78 | `se_lapel_fingertip_touch` | 이미 있는 라펠;집음 없음 |
| 79 | `se_small_garment_fold_pinch` | 손끝 사이 원단;의복 연결/노출/잠금 보존 |
| 80 | `se_existing_pendant_fingertip_hold` | 이미 있는 장식 본체/체인/손 소유 |
| 119 | `se_cornea_catchlight_without_wetness` | 눈 표면 반사;젖음/두 점 조건 없음 |
| 28 | `se_gaze_at_existing_partner_lips_state` | 기존 상대 입;현재 상태만, 순서 아님 |
| 81 | `se_beckon_shaped_finger_static_state` | 굽힌 현재 손 상태만;반복/초대 완료 아님 |

신규 제안은 기존 owners 안에서 같은 형태를 추가하거나, 해당 owner의 하위 문맥으로 통합한다. 눈/입은 acting/neutral expression 계열, 팔/손/접촉은 pose vocabulary, 순수 반사는 lighting, 가림/시점은 portrait composition 소유를 우선 검토한다. 모든 제안을 별도 `seduction` 확장 파일에 복제하지 않는다. 새 파일이 정말 필요할 때만 기존 확장 manifest에 등록한다.

처음 12개 형태에는 좁은 프로필 template이 있다. 실제 core 전제 검사와 소유/속성 매핑을 완성한 항목만 선택해 설치한다. 상대 입 시선 상태와 beckon 모양은 상대/의도/시간과 섞이기 쉬워 우선 선택 후보로 두고 넓은 원 용어의 exact 하드 alias로 등록하지 않는다.

선택형 묶음 10개는 다음 용도다.

- 위 시선+작은 닫힌 미소+기존 라펠 접촉.
- 옆 시선+비대칭 입+부드러운 빛.
- 스퀸치+작은 눈 표면 반사.
- 가장자리 좌석+뒤쪽 손 지지+손가락 이완.
- 턱 아래 hover 손+닫힌 미소+CU.
- 한 손 뒤통수+목 축+직접 시선.
- 자기 어깨 돌아보기+MCU+Rembrandt.
- 기존 상대 어깨 OTS+주체 얼굴 초점.
- short 면 방향+loop 패턴.
- 기존 펜던트 hold+닫힌 미소+부드러운 빛.

각 묶음은 독립적으로 채택된 요소만 작동해야 한다. 가장자리 앉기와 뒤쪽 손 지지가 물리적으로 동시에 가능한지, 주체/손이 같은 소유인지, 얼굴 조명 pattern이 돌아본 자세와 일치하는지 확인한다. 호환되지 않으면 별도 대안으로 남긴다. broad mood 하나로 묶음 전체를 요구하지 않는다.

**P2 완료 조건:** 중복 없는 최종 후보/프로필 목록과 stable IDs, 적절한 source owner, 긍정 검색 텍스트, 실제 가드/효과 매핑, optional bundle 동작이 확인된다. 제안 수량 자체는 완료 기준이 아니다.

## 5. P3 — 인덱스·의미 회귀·후보팩 검증

### 5.1 구현 전후 baseline

구현 시 별도 체크아웃 또는 적절한 작업 공간을 사용한다. 주 작업 공간의 진행 중인 변경을 기록하고 해당 작성 자산/테스트만 다룬다. 기존 전체 테스트가 실패한다면 baseline failure ID를 기록하고, 이번 변경으로 새로 생긴 실패와 구분한다. 불관련 fixture나 역사적 픽셀 evidence를 재작성해 통과시키지 않는다.

### 5.2 파생 자산 재생성

작성 자산을 먼저 병합하고 기존 도구로 시각 프로필 인덱스와 semantic index/BM25F 관련 결과를 재생성한다.

- [build_visual_profile_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py)
- [build_semantic_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_semantic_index.py)
- [validate_photo_prompt_dictionary.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py)

실행 옵션은 구현 시 해당 CLI의 현재 도움말/유지보수 지침을 확인한다. 생성 인덱스를 수동 편집하지 않는다. 벡터 캐시는 텍스트·provider·model·dimensions 등 호환 메타데이터가 일치하는 경우만 재사용한다. 의미/embedding text가 바뀐 항목의 옛 벡터를 무조건 보존하지 않는다. 이번 연구 단계에서는 재생성/embedding 호출을 하지 않았다.

### 5.3 의미·계약 회귀

기존 테스트군 중 관련 범위를 확장한다.

- [acting expression](/Users/chasoik/Projects/image-prompt/tests/test_photo_acting_expression_data.py), [neutral alternatives](/Users/chasoik/Projects/image-prompt/tests/test_photo_neutral_expression_alternatives.py).
- [pose vocabulary](/Users/chasoik/Projects/image-prompt/tests/test_photo_pose_vocabulary_semantics.py), [pose visual semantics](/Users/chasoik/Projects/image-prompt/tests/test_photo_pose_visual_semantics.py).
- [portrait composition](/Users/chasoik/Projects/image-prompt/tests/test_photo_portrait_composition_semantics.py), [lighting visual semantics](/Users/chasoik/Projects/image-prompt/tests/test_photo_lighting_visual_semantics.py).
- [visual obligations](/Users/chasoik/Projects/image-prompt/tests/test_photo_visual_obligations.py), [authorial core v6](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core_v6.py).

[검증 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/REGRESSION-PLAN.json)은 **120개 검토 프로브와 45개 경계 사례**다. 120개 프로브를 120개 완성된 실행 테스트로 간주하지 않는다. 프로브별 요청과 기대 ID/관계를 정교화한 뒤 필요한 실행 회귀를 작성한다. 45개는 36개 교차 경계+9개 시간 항목이다.

특히 다음은 실제 계약 회귀로 확인한다.

1. 정확 문구, 문맥 없는 broad label, 부정, 인물/물체 의미, 사용자 정의, 새 한/영 holdout 표현.
2. 성인 끌림 가드 보존과 일반 표정의 중립 문맥;외형만으로 끌림을 자동 활성화하지 않음.
3. actor/target 좌우, 자기/상대, 직접/반사, camera roll/head roll, face yaw/projected lighting side.
4. 열린 차원·부분 속성 잠금·출력 제외가 후보와 프로필을 일관되게 제한함.
5. 가림/크롭/초점이 의무를 숨기면 미관찰/충돌을 표시하고 core를 몰래 바꾸지 않음.
6. 새 record와 optional bundle의 stable ID 노출, 후보 선택, 의무 승격 근거를 따로 확인함.
7. temporal label을 정지 상태의 exact hard profile로 잘못 승격하지 않음.

### 5.4 요청별 후보팩 확인

최초 core 해시, 적용된 작성 자산 해시, eligibility, pack hash, candidate key, profile ID, 선택 이유, 프롬프트의 구성요소 증거를 기록한다. 후보가 파일에 있는 것만으로 pack 성공이 아니다. 후보팩에 노출되어도 선택되지 않았다면 반영된 픽셀 효과로 귀속하지 않는다.

슬롯 기본 차원이나 문자열 점수가 아닌 실제 owner/effects 검사를 통과해야 한다. `candidate_slots`에 stable ID를 연결하고 같은 ID의 슬롯 모호성을 제거한다. 기존 64개 상한에서 새 데이터가 필요한 좁은 의미를 노출하는지, 관련 없는 후보가 좁은 슬롯을 점유하는지 확인한다. 이 결과에서 병목이 드러날 때만 별도 런타임 변경안을 만든다.

**P3 완료 조건:** 작성/파생 자산이 일치하고 관련 baseline 대비 새 실패가 없다. 경계 회귀와 pack 노출/선택/의무 근거가 기록된다. 여기까지는 이미지 품질 PASS가 아니다.

## 6. P4 — 원본 픽셀에서 최종 형태와 관계 확인

[픽셀 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/seduction-expression-20261004/PIXEL-QUALIFICATION-PLAN.json)의 8개 장면군을 사용한다. 눈꺼풀, 손날/손 접촉, 한 손 뒤통수, 라펠/원단/장식 접점, 전신 지지, 자기/상대 어깨, 조명 pattern/면 방향, 순수 반사점/국소 광역이다.

장면군 안의 변형은 실행 전에 별도 하위 사례로 나눈다. 예를 들어 라펠 touch와 fabric pinch와 pendant hold를 한 이미지에 모두 넣지 않는다. 스퀸치와 윗눈꺼풀 변형, 단독 돌아보기와 두인물 OTS도 구분한다. **8개 장면군은 8장 생성 예산을 뜻하지 않는다.** 구현 완료 후 정확한 하위 사례/arm 수와 모델/options를 확정한다.

각 하위 사례는 같은 요청/core/crop/options에서 현재 데이터와 반영 데이터 arms를 비교한다. 임의의 성공 이미지 선별이나 자동 재시도로 결과를 대체하지 않는다. 데이터·pack·선택·프롬프트·원본 파일과 해시를 모두 보관한다. 생성 변동 때문에 두 이미지의 차이만으로 인과를 단정하지 않고, 해당 데이터의 실제 노출/채택 증거도 요구한다.

판정은 원본 픽셀 기준이다.

- actor/target의 정확 소유, 손가락/팔/목/다리 연결, 선택 접점/간격, 그림자 연결/분리, 반사점 위치, 크롭·잠금 보존을 각각 검사한다.
- 필수 구성요소가 하나라도 실패하면 전체 장면은 실패한다: `partial_is_fail`.
- 가려짐·작은 크기·흐림으로 필수 관계를 못 읽으면 `UNOBSERVABLE`;전체 PASS로 계산하지 않는다.
- 원본을 읽기 위해 확대 표시할 수 있으나, 새 픽셀을 생성하는 보정/업스케일 결과를 원본 증거로 쓰지 않는다.
- 시간 항목 전체는 비디오/순서 프레임에서 검사한다. 정지형태의 성공을 전체 시간 의미 성공으로 올리지 않는다.

**P4 완료 조건:** 설치 대상으로 채택한 의미의 노출/선택/프롬프트/원본 픽셀 연결과 모든 요구 게이트가 기록된다. 미노출·미선택·미관찰을 성공 숫자에서 제외한다. 사용자 수용은 별도 상태로 남긴다.

## 7. 배치와 중단/복구 기준

| 배치 | 범위 | 권장 선행/출구 |
|---|---|---|
| A | 의미 경계+기존 22개 후보/14개 프로필 검토 | P0 매핑, 핵심 경계 회귀;기존 정의 보존 |
| B | 검토에서 살아남은 신규 형태 후보/좁은 프로필 | 중복 제거, 실제 가드/target/property, 좁은 holdout |
| C | 10개 중 호환 가능한 optional 묶음 | 각 구성의 독립 적용/잠금/선택 검사 |
| D | 파생 인덱스·팩·원본 픽셀 검증 | 작성 자산 확정, 기록된 baseline과 source hashes |

데이터만으로 충분한 곳은 런타임 변경을 하지 않는다. 실제 필요한 entity/context 검사가 현재 계약에서 표현되지 않으면 해당 후보를 선택형 또는 보류로 남기고 좁은 런타임 제안을 별도로 검토한다. 의미 오라우팅, 잠금 침범, 객체 추가, broad label의 전체 recipe 강제, baseline 대비 새 실패가 발생하면 그 배치를 되돌리고 작성 자산에서 파생 결과를 다시 생성한다.

되돌림 단위는 검토된 작성 record/테스트와 그로부터 재생성한 결과다. 다른 작업의 자산·인덱스·연구 폴더를 함께 reset하지 않는다. 커밋/푸시/PR은 별도 구현 작업의 범위에서 결정하며 이번 연구는 발행하지 않았다.

## 8. 완료 보고에 포함할 숫자

구현 후 보고에서는 설치된 record 수, 중복으로 재사용한 수, 구조 검증, 의미/계약 회귀, 후보 노출/선택, 프롬프트 증거, 원본 픽셀, 사용자 수용을 분리한다. 현재 보고 가능한 숫자는 **120항목 조사, 39출처, 157기존 후보·17프로필 대응, 36후보 보강 제안, 26프로필 보강 제안, 10선택 묶음, 45경계 회귀 제안, 8픽셀 장면군**이다. 활성 반영·런타임 회귀·이미지 생성은 각각 0건이다.

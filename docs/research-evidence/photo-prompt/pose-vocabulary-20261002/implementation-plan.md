# 시각 의미 데이터·후보팩 반영 계획

2026-10-02 · 계획 상태: 연구 완료, 런타임 반영·렌더 검증 전

## 1. 반영 원칙과 작업 순서

원문 398개 행을 그대로 398개 후보로 등록하지 않는다. 이번 초안의 **236개 관찰 정의 + 77개 행별 분해 + 문맥/보류 항목**을 기준으로 기존 후보를 재사용하고 누락된 관계를 추가한다. 신규 48개 프로파일 제안도 한 번에 전부 하드 활성화하지 않는다. 정의·변형·출처·범위 검토를 마친 항목부터 연결하며, 픽셀 검증 결과는 별도로 남긴다.

작업 단위는 요청마다 **하나의 고정된 코어와 하나의 통합 후보팩**이다. 지지 자세, 손, 시선, 접촉과 상대 관계를 같은 장면 안에서 연결한다. 용어마다 독립 팩을 만들고 서로 다른 코어·인원·의상을 합치는 방식은 사용하지 않는다.

우선순위는 단어의 유명세나 성적 장르 여부가 아니라 **혼동 위험, 관찰 가능성, 현행 데이터 재사용, 출처 확실성**으로 정한다.

| 단계 | 주요 작업 | 완료 조건 |
|---|---|---|
| 0. 의미 확정 | 기존 후보/프로파일 재사용, 반대 값 분리, 보류 변형 확정, 소유자·속성 범위 검토 | 모든 승격 항목의 정확 정의·반례·출처 역할·필수 영역·고정 속성이 기록됨 |
| 1. P0 지지·접촉 | 무릎/좌석/다리 교차/눕기/손 지지/발 접촉과 기존 조형 3종 보강 | 좁은 데이터·정책·팩 회귀 통과, 선택되지 않은 프로파일 비활성, 관찰 충돌 감지 |
| 2. P1 손·전문 자세·상대 | 손 기호와 눈, 발레, 두 사람 접촉/지지, 선택한 요가·NPC 변형 | 명칭/좌표계/소유자/단계의 구분과 범위 제한이 팩·프롬프트까지 유지 |
| 3. P2 문맥·별칭 | 날짜/공동체/작품/학파 정보를 포함한 별칭 연결, 장르 메타데이터, 남은 공연·요가 검토 | 미확정 별칭은 자동 활성화되지 않으며 정확 변형만 요청 범위에서 연결 |
| 4. 원본 이미지 자격 검증 | 같은 코어의 비교 실험, 원본 접촉·관절·손가락·소유자 검토 | 필수 게이트 전부 관찰 가능하고 PASS인 범위만 이미지 검증 완료로 기록 |

## 2. 단계 0: 중복 제거와 스키마 조정

### 2.1 기존 데이터 재사용

다음 20개 재사용/확장 대상은 현재 병합 데이터에서 존재를 확인했다. 초안의 슬롯과 현재 슬롯이 다르면 이동을 자동 적용하지 말고 대상·속성 소유를 먼저 조정한다.

| 초안 의미 | 현행 대상 | 작업 |
|---|---|---|
| 콘트라포스토 | `contrapposto_full_body` + `contrapposto_weight_shift` | 별칭·하중 관찰·가림 반례 보강 |
| 세르펜티나타 | `figura_serpentinata_full_body` + `figura_serpentinata_spiral_pose` | 축 회전과 평면 S곡선 경계 |
| 트리방가 | `tribhanga_three_bend_full_body` + `tribhanga_three_bend_pose` | 세 교대 굴곡의 공동 관찰 |
| S/C곡선 | `editorial_s_curve_pose`, `single_arc_c_curve_pose` | 하중·회전과 독립된 투영 형상 |
| 중립·엇갈린 발·발목 교차 | `neutral_standing_pose`, `staggered_leg_depth_separation`, `crossed_ankles_narrow_base` | 발 위치·지지 역할과 키워드 연결 |
| 좌면 가장자리 | `perched_edge_sit_grounded_support` | 좌면/발의 가시 영역과 armrest 변형 경계 |
| 발끝 뻗기 | `lower_limb_plantarflexed_line` | heel lift / pointe와 비동의어 |
| 팔꿈치 기대기 | `propped_elbow_recline_support` | 손/전완/팔꿈치의 접촉 역할 |
| 흉곽–골반·머리 방향 | `thorax_pelvis_opposed_azimuth`, `head_shoulder_opposition` | 카메라 방향·머리·시선 분리 |
| 손목·머리 위 팔 | `relaxed_wrist_offset_line`, `arms_raised_overhead` | 손가락과 손 위치는 별도 |
| 보행 | `walking_mid_stride_pose` | 지지/공중 단계와 head-turn 결합 |
| 휴대폰·안경 | `holding_phone_visible`, `hand_adjusting_sunglasses` | 소품 유형·손 접촉 대상의 변형 검토 |
| 뒤로 굽힌 자유 다리 | `single_support_backward_flexed_free_leg` | 이미 존재하는 역학을 재사용 |
| 손끝 비지지 접촉 | `fingertip_contact_visible_target_non_support` | `contact_point` 유지, 터치와 하중 구분 |

이 밖에 정면/측면/후면/3/4 몸 방향, 손 주머니, 머리 넘기기, 무릎 올린 앉기 등은 [77개 분해 설계](row-decompositions.tsv)에 대상과 수정할 범위를 적었다. 목록의 후보를 실제 별칭으로 묶기 전에 지지면·관절·접촉 역할이 같은지 확인한다. “유사한 예”로 표시한 항목은 변환이 필요한 참고이며 동의어가 아니다.

### 2.2 현재 계약에 맞게 조정할 필드

`candidate-data.proposed.json`과 `visual-profiles.proposed.json`은 **연구용 스키마**다. 그대로 assets에 복사하면 안 된다.

- 런타임 후보는 현재의 `id/ko/en/weight/tags/for_any/aliases/keywords/embedding_text/concept_units/relations/affected_dimensions/affected_properties` 형식으로 조정한다.
- 원장·출처·보류 상태·상세 좌표계·관찰 영역은 유지보수 데이터에 두고, 지원되는 런타임 키만 확장에 넣는다. 초안의 `typed_assertions`는 의미 설계이며 현행 계약이 이미 직접 실행한다고 주장하지 않는다.
- `relations`의 현재 필수 키는 `id/type/subject/object`다. 초안의 `actor_1` 등을 실제 코어 엔티티에 바인딩한 후 이 형식으로 내린다.
- 초안의 속성명은 설계 값이다. 현재 property contract의 target/property 소유와 허용된 수정 범위에 맞춰 검증한다. 소유자가 해소되지 않으면 채택 가능 상태로 만들지 않는다.
- `contact_point`는 현재 `relationship`, `gaze_engagement`는 `expression`, `relational_action`은 `action`을 기본 소유한다. 복합 후보에는 실제 변경 차원과 속성을 개별 기록한다. 빈 차원인 `gaze_target`에 후보를 넣고 자동 채택 가능하다고 가정하지 않는다.
- `core_assertion_discovery`는 구체적인 units와 속성 범위를 가진 후보에만 제한적으로 적용한다. `open`, `wide`, `pose`, `heart`, `attitude` 같은 단어로 코어의 다른 속성을 바꾸지 않게 한다.
- 기존 `body_framing.forward_torso_lean_close_crop`의 지원 단서 보존은 프레이밍 의미다. 몸통 기울기 후보와 연결하되 고정된 크롭 변경을 자동 허용하지 않는다.

## 3. P0: 먼저 반영할 구체적 의미

첫 묶음은 기존 조형 3종과 다음 16개 정밀 의미를 중심으로 잡는다.

1. `pv_tall_kneel`, `pv_heel_sit`, `pv_half_kneel` — 골반 높이와 무릎/발 접지.
2. `pv_squat_grounded`, `pv_toe_squat`, `pv_quadruped` — 발/뒤꿈치/손/무릎 지지.
3. `pv_reverse_chair`, `pv_chair_straddle` — 좌면 상대 방향과 다리의 양쪽 배치.
4. `pv_figure_four`, `pv_knee_over_knee`, `pv_ankle_cross_seated` — 교차 높이와 접촉 대상.
5. `pv_supine`, `pv_prone`, `pv_side_lying` — 몸통의 어느 면이 지지되는지.
6. `pv_chin_support`, `pv_fingertip_touch` — 지지와 비지지 접촉.

기존 족저굴곡, 뒤쪽 자유 다리, 팔꿈치 지지의 후보는 새 ID로 중복 추가하지 않고 함께 검토한다. `kneeling_soft_pose`의 covered/non-suggestive 문구는 기존 스타일링 문맥으로 보존할 수 있지만 높은 무릎과 낮은 무릎의 구별을 대신하지 못한다. 중립 역학의 필수 정의와 스타일링 문맥을 분리한다.

필요한 지원 부위가 크롭 밖이면 해당 후보의 의미가 검증되지 않는다는 사실을 팩의 관찰 충돌로 남긴다. 코어가 head-and-shoulders를 고정했다면 하체 지지를 보이도록 자동으로 전신 크롭으로 바꾸지 않는다. 현재 계약으로 표현 가능한 가시성 메타데이터를 먼저 쓰고, 표현되지 않는 경우에 한해 범용 observability 판정의 최소 변경을 설계한다.

통과 기준은 정확 기하가 문장으로 노출되는지, 가까운 오답이 대체 채택되지 않는지, `affected_properties`와 고정 속성이 팩→선택→채택→컴포저 단계에서 보존되는지다. 픽셀 판정 전에는 이미지 검증 완료로 표시하지 않는다.

## 4. P1/P2: 순차 확장 범위

### 손·시선

V/더블 V/얼굴 근처 V, 작은 손가락 하트/두 손 하트/팔 하트, 깍지/손끝 맞댐/합장, 손바닥 위/아래를 먼저 구분한다. Finger/Hand heart와 gyaru V는 성인 중립 예시의 손가락·엄지·손바닥 원본을 조정한 후 정확 게이트를 확정한다. 눈 방향과 head turn은 다른 속성이며 Squinch는 근접 눈꺼풀 원본이 필요하다. Cheek/Cat heart, Smize/Fish gape는 부정확한 별칭 활성화로 출시하지 않는다.

### 전문 자세와 두 사람

Arabesque/Attitude, Retiré/Passé, Tendu, Demi-pointe/En pointe, Croisé/Effacé부터 구분한다. 정적 위치와 동작 단계의 프로파일을 분리하고 학파·관찰자·동작 다리를 기록한다. 두 사람은 손잡기/머리–어깨/정면·뒤 포옹부터 시작하고, 가로 안기/업기/딥은 여러 지지와 가려진 팔 소유의 검증을 추가한다.

요가 28종의 후보를 유지하되 `individual_source_check_required` 17개는 개별 페이지·교육 관행 확인을 완료한다. Cow/Gomukhasana, Natarajasana, Boat/Naukasana 충돌을 전역 별칭으로 풀지 않는다. NPC 8종은 부문·참조 변형을 고정하고 원본 자세 예를 붙인다. 이름만 존재하는 공식 규정으로 손·발 형상까지 검증했다고 처리하지 않는다.

### 문맥과 별칭

Model digitals/Polaroids는 촬영 목적과 세트 구성으로 기존 `capture_context` 후보를 재사용한다. 카탈로그·룩북·뷰티·장르명은 단독 지지 자세를 고정하지 않는다. OOTD/candid는 촬영 문맥으로 남긴다. 부두아/그라비아 별칭의 중립 기하는 기존 포즈 원자와 연결하고 의상·노출·성적 톤 효과를 추가하지 않는다.

도상은 특정 작품·수인 변형을 원장에 기록한다. Voguing/팬댄스/결박·역할 연출은 공연·작가의 직접 설명과 선택 순간을 확보한 뒤 소품 접촉·지지·가림으로 내린다. 광범위한 양식명을 하나의 팔/골반 형태로 정하지 않는다.

## 5. 파일별 반영 위치

아래 파일명 중 `pose_vocabulary` 두 개는 **신규 파일 제안**이다. 현재 존재하거나 로드되는 파일로 오해하면 안 된다.

| 위치 | 예정 작업 |
|---|---|
| `skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json` | 검토한 신규 후보와 기존 슬롯 문맥 확장; 지원되는 키만 사용 |
| `.../assets/photo_prompt_visual_obligations_pose_vocabulary.json` | 승인된 정확 의미·활성화·required fields·render gates; 기존 3개와 중복 금지 |
| `.../assets/photo_prompt_tags.json` | 의미 정책/라우팅의 필요한 연결만 검토; 다른 포즈/장르 가중치 일괄 변경 금지 |
| `.../scripts/prompt_generator.py` | 두 확장 로더 등록 및 현재 경로로 표현 안 되는 최소 연결에 한해 변경 |
| `.../scripts/photo_candidate_semantics.py` | 기존 validator/bundle projection/property scope 사용; 새 의미 레지스트리를 코드에 중복 작성하지 않음 |
| `.../scripts/photo_embodiment.py` | 기존 소유자·reach·support·contact 판단 재사용; 새 관계를 지원하지 못한 경우만 최소 확장 검토 |
| `.../scripts/visual_profile_contracts.py` | 기존 요청 전용·부정·사용자 정의 우선 계약 재사용 |
| `.../scripts/build_semantic_index.py` | 실제 승격한 소스만 반영하여 source hash를 갱신 |
| `.../scripts/build_visual_profile_index.py` | 승격한 프로파일과 source hash에 맞춰 생성 |
| `docs/research-evidence/photo-prompt/research_evidence.jsonl` 및 유지보수 원장 | 연구·출처·변형 확인 상태 기록; 승인된 픽셀 증거가 없는 항목을 approved 이미지 사례로 추가하지 않음 |
| `tests/test_photo_pose_visual_semantics.py` | 명명 포즈·혼동·부분 충족·가림 사례를 실제 계약에 연결 |
| `tests/test_photo_candidate_semantics.py` | 후보 범위, relations, 소유자, 속성 채택과 비활성 프로파일 검증 |
| `tests/test_photo_visual_profile_retrieval.py` | 정확 이름/부정/비인체 동음이의/사용자 정의와 검색 회귀 |
| `tests/test_photo_authorial_direction_scope.py`, `tests/test_photo_embodiment.py` | 고정 코어, 인원·의상·크롭 유지와 접촉/지지 연속성 |

현행 팩 기본 계약은 `photo-candidate-pack/v6`이며 소스상 총 후보 상한은 64, core slot 상한은 4, support slot 상한은 2다. 236개 초안을 한 요청에 모두 노출하는 계획이 아니다. 기존 한도 안에서 핵심 포즈 의미와 지원 접촉을 같이 보여줄 수 있는지 점검하고, 실제 누락 증거 없이 상한을 넓히지 않는다. 기존 `pose_framing_system`에 contact/partner/expression 지원을 연결할 경우에도 팩 크기·관찰 충돌·다른 주제 라우팅의 회귀를 함께 확인한다.

## 6. 평가와 렌더 계획

### 6.1 먼저 실행할 저비용 검증

1. 런타임 스키마, 참조 ID, 중복/순환 canonical 연결, source hash, property target·dimension 검증.
2. 원문 정확 이름, 반대 값, 부정, 동음이의, 사용자 정의를 실제 활성화 경로에 연결.
3. 한 요청으로 생성한 팩에서 노출 ID/순위/정의/지원 관계/범위를 기록. 노출과 선택과 채택을 따로 판정.
4. 채택된 관계가 컴포저의 구체 문장으로 남는지 확인. 표시용 별칭만 늘어난 경우 통과시키지 않음.
5. 고정된 인원·의상·신체 비율·얼굴/머리 참고 범위·장소·빛·카메라·크롭·성적 톤의 변경 회귀 점검.

현재의 five-arm fixture는 기존 포즈 평가의 기술 계약을 참고하는 자료다. 이번 224개 사례는 연구 입력 초안이며 validator에 넣기만 하면 실행된 테스트가 되는 형식은 아니다. 각 기대 결과를 실제 API의 활성화/노출/속성/판정 결과에 연결해 의미 있는 회귀로 만든다.

### 6.2 원본 이미지 비교의 인과 분리

처음에는 아래 8개 진단 장면을 골라 **4개 조건 × 장면 8개 = 32회 이미지 호출**을 계획한다. 이는 미래 예산 단위이며 이번 작업에서 실행하거나 비용을 지출한 호출이 아니다.

- 높은 무릎과 낮은 무릎 앉기.
- Figure-four와 무릎 위 교차.
- 거꾸로 앉기와 스트래들.
- 손끝 접촉과 턱 지지.
- 발끝 뻗기와 발 앞부분/포앵트 지지.
- V와 손가락 하트의 손가락 소유.
- Arabesque와 Attitude의 동작 무릎.
- 한 인물의 거울 셀피와 두 인물 손잡기 소유자.

8개 각각에서 실제로 요청할 목표와 고정된 반례를 먼저 명시한다. 대상에 두 뜻을 동시에 요구하지 않는다.

| 비교 조건 | 의미 프로파일 | 후보 데이터 | 확인할 효과 |
|---|---|---|---|
| A | 현재 | 현재 | 기준 상태 |
| B | 보강 | 현재 | 정의·하드 의미의 효과 |
| C | 현재 | 보강 | 후보 노출·선택·채택의 효과 |
| D | 보강 | 보강 | 두 데이터의 결합과 충돌 |

각 조건은 같은 요청 의도·코어·인원·성인 여부·의상·배경·빛·카메라·허용한 포즈 속성을 사용한다. 프롬프트/negative 바이트, core/pack/control/selection/review의 해시, 이미지 모델·버전·지원되는 파라미터, 호출과 원본 파일을 보존한다. seed가 지원되고 의미가 보장되는 경우만 통제값으로 쓰며 픽셀 결정성을 가정하지 않는다. 비교를 시작하기 전 네 조건을 고정한다.

8장면×1회의 초기 결과는 진단 표본이다. 전체 236개 후보 또는 51개 프로파일의 성공률로 일반화하지 않는다. 재현성 문제가 있거나 실패 원인을 분리해야 할 때 해당 장면만 반복하고, 원인이 확인되면 영향을 받은 게이트를 재검증한다. 단순 반복 호출로 정의 오류를 덮지 않는다.

### 6.3 원본 게이트와 종료 조건

- 큰 배치와 실루엣은 썸네일에서 확인하고, 손가락 수·손목/팔 연결·무릎/발 접촉·눈꺼풀·소유자는 원본 해상도에서 확인한다.
- 필수 게이트가 모두 관찰 가능하며 PASS인 장면만 성공이다. 일부 맞음은 실패로 집계한다.
- 가림/프레임 밖은 `UNOBSERVABLE`로 남겨 성공에서 제외한다. 이를 해부학 오류나 특정 모델의 첫 원인으로 단정하지 않는다.
- 요청 코어가 필요한 영역을 가리면 충돌을 보고한다. 관찰용 별도 프레임은 분리된 허용이 있을 때만 만들고 원래 조건의 성공으로 합치지 않는다.
- 호출 차단/도구 실패는 attempt 상태다. 생성된 이미지의 포즈 품질 실패와 분리한다.
- 수정은 해당 실패 관계/포즈/가림 속성에 제한한다. 다른 고정 속성이 달라지면 비교 조건에서 탈락시킨다.
- 원본 게이트 통과 후에도 사용자 수용은 별도 상태다. `research_ready`, `runtime_connected`, `pack_exposed`, `adopted`, `prompt_verified`, `pixel_qualified`, `user_accepted`를 한 PASS로 합치지 않는다.

## 7. 보류 항목을 닫는 방법

| 남은 항목 | 확보할 증거 | 승격 조건 |
|---|---|---|
| Cheek/Cat heart, Smize/Fish, M/여표 별칭 | 날짜·공동체가 확인되는 직접 정의와 서로 구별되는 성인 원본 예시 | 손/눈/무릎/발·대상·지지의 정확 변형을 기록하고 가까운 반례로 구별 가능 |
| 개별 요가 17종 | 교육기관의 개별 정의, 명명 충돌과 지지 변형 | 선택 관행의 기하와 보조도구 조건이 확정됨 |
| 복잡한 발레/수인/도상 | 학파 또는 작품이 명시된 원본, 관찰자 방향 | 학교/작품의 변형과 좌우·손·발을 검증 가능 |
| NPC 변형 | 동일 부문·변형의 실제 비교 사진 | 이름 외 팔/손/다리 구성의 근거가 있음 |
| Voguing·공연·역할·서스펜션 | 실무자/작가의 설명, 한 단계의 원본과 실제 지지 | 양식·시퀀스와 정지 프레임을 구분하고 소유자/지지/가림을 기록 가능 |

최종 완료는 모든 단어를 하드 포즈로 등록하는 것이 아니다. 각 원문 행이 **검증된 자세·변형, 적절한 문맥 메타데이터, 또는 이유가 있는 미확정 항목**으로 추적 가능하고, 반영한 범위의 실제 팩/속성/프롬프트/원본 픽셀 증거가 따로 존재해야 한다.

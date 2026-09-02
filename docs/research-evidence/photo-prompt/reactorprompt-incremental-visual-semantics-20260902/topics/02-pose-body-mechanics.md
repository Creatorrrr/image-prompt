# 02. 포즈·신체 역학: 지지, 하중 경로, 동작 단계, 접촉

## 결론

이 증분 코퍼스는 `contrapposto`, `figura serpentinata`, `tribhanga` 같은 새 명명 포즈를 exact 프로필로 더 추가해야 한다는 근거보다, **일상 포즈에서 지지점·비지지 사지·접촉 역할·프레이밍 가능성을 함께 전달하는 구조가 부족하다**는 근거를 준다. 현재 exact 프로필인 `contrapposto_weight_shift`, `figura_serpentinata_spiral_pose`, `tribhanga_three_bend_pose`는 구조적 의무와 혼동 경계가 이미 구체적이다. 이번 범위에서는 이들을 유지한다.

권고는 다음 네 가지다.

1. `body_pose`에 broad/advisory 후보 `single_support_backward_flexed_free_leg`를 추가한다.
2. `body_orientation`에 close crop에서도 하중을 주장하지 않는 `forward_torso_lean_close_crop`을 추가한다.
3. 손 모양과 접촉을 분리한다. 새 `fingertip_contact_visible_target_non_support`는 `hand_pose`가 아니라 기존 `contact_point` 슬롯이 소유하고, 포즈 의미 정책이 `contact_point`를 라우팅하도록 한다.
4. 후보마다 `pose_mechanics.observability`를 두고, 필요한 신체·접촉면이 프레임 밖이면 하중 후보를 선택하거나 성공으로 채점하지 않는 일반 가드를 추가한다. 현재 여섯 ID만 나열한 close-up 충돌 규칙의 사각지대를 메우는 목적이다.

이 문서는 **research/design 산출물**이다. 런타임 자산, 생성 인덱스, 테스트, 렌더 요청은 변경하지 않았다. 제안은 구현·렌더 성공이나 사용자 판단을 의미하지 않는다.

## 범위와 증거 경계

- 기준 리비전: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 고정 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 매니페스트 SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, ID 1565–2746
- 프롬프트 조사: 924개 전수 lexical scan. 아래 집계는 서로 배타적이지 않고, 의미 라벨이 아니라 후보 발굴용 문자열 신호다.
- 픽셀 조사: 실제 파일 32장, 16개 게시물. 8개 주제 양성 게시물과 인접 ID 대조 8개를 짝지어, 초·중·후반 ID 구간을 포함했다.
- 픽셀과 프롬프트는 독립 증거다. 프롬프트에 문장이 있어도 픽셀 성공이 아니며, 필요한 부위가 잘리면 `UNSCORED`이지 품질 0이나 실패 원인의 확정이 아니다.
- 이미지에서 보이는 접촉·관절·지지면만 기록했다. 정체성, 동일인 여부, 보호 특성, 건강·체력·체중·가치·매력, 관계·감정·의도는 추론하지 않았다.

## 전체 프롬프트 스캔

아래 정규식은 소문자화한 비어 있지 않은 프롬프트에 적용했다. 수치는 중복 허용이다.

| 신호군 | 핵심 매칭 표현 | 게시물 수 | 해석 한계 |
|---|---|---:|---|
| 명시적 하중 경로 | `most weight`, `support leg`, `free leg`, `one leg planted`, `feet planted`, `balanced on uneven` 등 | 19 | 문장에 하중이 있어도 발·지면이 프레임 밖이면 픽셀 검증 불가 |
| 비대칭 다리 기하 | `one leg lifted/raised/bent/extended`, `crossed ankles`, `staggered stance` 등 | 15 | 굽힌 무릎, 발목 교차, 공중의 free foot은 서로 대체 불가 |
| 흉곽·골반·어깨 관계 | `torso turn/twist/lean`, `shoulder drop/different depths`, `hip/pelvis shift`, `S-curve` 등 | 62 | 카메라 롤, 원근, 의복·머리카락 윤곽이 신체 평면처럼 보일 수 있음 |
| 좌석·표면 지지 그래프 | `sitting/seated/perched`, `lean against/on`, 손·팔꿈치·등의 표면 접촉 등 | 81 | `sitting`만으로 골반·발·손 중 무엇이 지지하는지 정해지지 않음 |
| 이동 단계 | `mid-step/stride`, `walking/running/stepping`, `stance/swing/rear/trailing leg`, `crouching/kneeling/jumping` 등 | 59 | 여러 행동을 `or`로 열거하면 한 프레임의 단계가 결정되지 않음 |
| 손–신체/표면 접촉 | 손·손끝·팔꿈치의 `rest/brace/touch/press/hold/grip` | 69 | 접촉과 하중 지지는 다르며, 가까이 있음은 접촉도 아님 |
| 전신 관찰 가능성 | `full-body/full length`, `head-to-feet`, `both feet`, `uncropped feet`, `boots to head` | 90 | 표현만 있고 실제 픽셀에서 잘릴 수 있음 |
| close crop | `close-up/close portrait`, `head-and-shoulders`, `crown-to-chest`, `mid-thigh upward` 등 | 160 | 하체 하중 후보와 구조적으로 충돌할 수 있음 |

정제한 명명 용어 집계에서는 `contrapposto`가 3건이었다. ID 2004와 2699는 양성, ID 2475는 명시적 부정(`no contrapposto`)이다. `figura serpentinata`와 `tribhanga`는 0건이었다. `S-curve` 계열 16건 중 15건은 신체/포즈 문맥이고 1건(ID 2548)은 머리카락 웨이브만 가리키는 lexical false positive였다. `fashion pose|editorial pose` 같은 일반 표현은 9건으로, 자체로는 지지 기하를 정하지 못한다.

가장 직접적인 프레이밍 충돌은 ID 2743, 2745, 2378, 2379, 2173이다. 이 다섯 프롬프트는 하중/지지 표현을 포함하지만 close crop이고 전신 가시성 표현은 없다. 이는 빈도보다 **관찰 가능성 메타데이터**가 우선해야 함을 보여준다.

## 픽셀 표본과 관찰

선정은 주제 양성 ID와 가장 가까운 사용 가능한 인접 ID를 대조로 묶은 목적 표본이다. 대조는 모든 포즈 차원의 완전한 음성을 뜻하지 않는다. 각 게시물의 `_01`, `_02` 두 실제 이미지를 보았다.

| 짝 | 역할·ID | 프롬프트 증거 | 픽셀 증거 `_01` / `_02` |
|---:|---|---|---|
| 1 | 양성 1583 | 전신, 손은 허리, 한 다리 들기 | 두 장 모두 공중 free foot이 없다. `_01`은 좁은 교차/근접 지지, `_02`는 넓은 양발 지지. 명시한 다리 들기 0/2 |
| 1 | 대조 1584 | 전신, 한 손 허리, 서 있기 | 명시적 다리 들기 없이도 발목 교차 또는 비대칭 무릎이 나타난다. 일반 비대칭은 공중 free foot의 대체물이 아님 |
| 2 | 양성 1724 | 접이식 의자에 앉기, 모자 잡기 | 둘 다 좌석·등받이 접촉이 보이나 한 장은 교차/들린 다리, 다른 장은 다른 발 배치. `sitting`만으로 지지 그래프가 고정되지 않음 |
| 2 | 대조 1725 | 돌 테이블에 앉기 | 두 장 모두 프롬프트에 없던 뒤쪽 양손 브레이스와 교차 다리를 더한다. 좌석 종류만으로 손/발 지지를 예측할 수 없음 |
| 3 | 양성 1883 | 흉곽 비틀기, 어깨 하강, 골반 각도, 팔 대각선, S-curve | 하체가 잘려 하중 경로는 미관찰. 보이는 곡선의 상당 부분은 팔·의복·크롭으로도 설명 가능 |
| 3 | 대조 1884 | 전신, 달리기/회전/과일 따기/웅크리기 등 복수 행동 | `_01`은 지지 발과 공중 trailing foot이 명확. `_02`는 보행처럼 읽히지만 한 발/다리가 일부 가려짐. 복수 분기 문장이 단계 변이를 남김 |
| 4 | 양성 2101 | 한 다리 planted, 반대 다리 뒤로 굽혀 발 들기, 전신 | 두 장 모두 지지 발, 뒤로 굽힌 무릎, 공중 free foot이 썸네일에서도 분리된다. 가장 깨끗한 양성 |
| 4 | 대조 2102 | 가까운 고각 셀피, 상체 전방 기울기 | 다리·발·지지면이 프레임 밖. 상체 기울기는 관찰 가능하지만 하중은 채점 불가 |
| 5 | 양성 2173 | 카운터 기대기, 한 손 접촉, 한쪽 다리 하중, 다리 교차, mid-thigh crop | 손–카운터 접촉은 보이지만 발·지면은 없다. 접촉 성공이 다리 하중 성공을 증명하지 않음 |
| 5 | 대조 2174 | 손은 난간, 오른쪽 하중, 어깨·골반 약간 비틀기, 무릎 아래까지 | 손–난간/의복 접촉은 보이지만 발이 없어 하중은 채점 불가 |
| 6 | 양성 2378 | mid-thigh 셀피, 한쪽 hip에 weight shift | 휴대전화 그립과 골반 비대칭은 보이지만 발·지면이 없다. 하중은 `UNSCORED` |
| 6 | 대조 2377 | 얼굴 중심 extreme close-up | 하중·지지·하지 기하는 프레임 밖 |
| 7 | 양성 2607 | 불균일 지면, 한 손 주머니, 다른 손끝이 보이는 대상에 접촉, boots-to-head | 두 장 모두 부츠–지면과 손끝–대상 접촉이 보인다. 손끝 접촉은 touch-only이며 관계·감정·신뢰의 픽셀 증거로 사용하지 않음 |
| 7 | 대조 2608 | 야간 상반신 close portrait | 발·지지면·표면 접촉이 없다 |
| 8 | 양성 2743 | `paused mid-step`, rear-leg weight, 그러나 crown-to-mid-chest crop | 두 장 모두 상반신 초상. step과 rear-leg weight는 프레임 밖이라 검증 불가. 프롬프트 내부의 강한 의무 충돌 |
| 8 | 대조 2744 | 낮은 카메라 위로 상체 전방 기울기, 손은 프레임 밖 | 두 장 모두 원근과 어깨 깊이로 상체 접근/기울기는 보이나, 지지·하중은 보이지 않는다. 낮은 시점이 전신 기울기를 대체하면 안 됨 |

엄격한 발–지면/좌석–골반 지지 사슬을 채점할 수 있었던 것은 13/32장이다: 1583-01/02, 1584-01/02, 1724-01/02, 1725-01/02, 1884-01, 2101-01/02, 2607-01/02. 나머지 19장은 이 축에서 `UNSCORED`다. 그중 일부는 상체 방향 또는 손 접촉처럼 다른 축에서는 채점 가능하다.

## 프롬프트–픽셀 정렬과 분기

1. **정렬 양성:** ID 2101은 전신 가시성, planted foot, 뒤로 굽힌 free leg, 발의 공중 간격을 함께 지정했고 두 장 모두 첫눈에 읽혔다.
2. **명시 문장만의 실패:** ID 1583은 `one leg lifted`를 썼지만 두 장 모두 양발 접촉/교차로 치환됐다. 후보 텍스트 존재를 픽셀 PASS로 쓸 수 없다.
3. **크롭으로 인한 비채점:** ID 2743은 `mid-step`과 rear-leg weight를 쓰면서 crown-to-mid-chest를 요구했다. 같은 요청 안에서 검증 가능성을 제거했다.
4. **접촉 ≠ 지지:** ID 2173/2174의 손–표면 접촉은 보이지만 손이 장식적 touch인지 안정화인지 하중 지지인지 구별할 하중 경로가 없다.
5. **`sitting`의 과소결정:** ID 1724/1725는 좌석 접촉 외의 손·발 지지 구성이 이미지마다 바뀐다.
6. **복수 행동의 과소결정:** ID 1884처럼 여러 행동을 나열하면 stance/swing/turning 중 무엇을 고정할지 불분명하다.
7. **무프롬프트 비대칭:** ID 1584는 구체적 하지 기하 없이도 비대칭을 만든다. 그러므로 `asymmetry`나 `S-curve`만으로 single-support 성공을 채점하면 false positive가 난다.
8. **카메라 혼동:** ID 2744는 low angle과 가까운 원근으로 상체 전방 접근이 강해진다. `body_orientation`은 채점할 수 있어도 하체 하중을 상속하면 안 된다.

## 현재 자산의 커버리지와 겹침

검토한 소스 자산은 `.agents/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`과 `.agents/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`이다. 생성물인 `photo_prompt_visual_profile_index.json`, `photo_prompt_semantic_index.json`과 shard는 원본 편집 대상이 아니다.

### 이미 강한 영역

- `contrapposto_weight_shift`: loaded support leg, relaxed free leg, 골반–어깨 counter-tilt, 전신 가시성, generic shift/잘린 발/S-curve를 명시적으로 거부한다.
- `figura_serpentinata_spiral_pose`: 지지/자유 다리에서 시작하는 골반–흉곽–어깨–팔–머리의 3차원 반대 방향 연쇄를 요구한다.
- `tribhanga_three_bend_pose`: 머리, 중앙 골반, 굽힌 무릎의 교대 굴곡을 요구하고 의상·도상·손동작을 분리한다.
- 후보층에는 `walking_mid_stride_pose`, `pelvic_obliquity_single_support`, `staggered_leg_depth_separation`, `crossed_ankles_narrow_base`, `perched_edge_sit_grounded_support`, `propped_elbow_recline_support`, `controlled_three_quarter_weight_shift`처럼 이미 관찰 가능한 기하가 있는 항목이 있다.

### 약한 영역과 소유권

| 의미 | 단일 소유자 | 현 상태 | 권고 |
|---|---|---|---|
| 발·골반·좌석을 잇는 지지/하중 그래프 | `body_pose` | 일부 새 후보는 강하지만 legacy 후보가 `natural weight shift` 정도로 모호 | `pose_mechanics.primary_supports/free_segments/observability`로 보강 |
| 흉곽·골반·머리의 방향/평면 | `body_orientation` | `thorax_pelvis_opposed_azimuth` 등은 강함 | close crop 전방 기울기를 별도 후보로 추가; 하중을 주장하지 않음 |
| 손가락 배열·손목 각도 | `hand_pose` | `hand_on_railing`, `hand_on_table_edge`가 대상만 말하고 역할은 없음 | 손 모양만 소유; 접촉 여부/역할을 소유하지 않음 |
| 접촉 상태·접촉 대상·하중 역할 | `contact_point` | 슬롯은 존재하지만 악기/관계/마법 중심이며 포즈 정책에 라우팅되지 않음 | 일반 인체–표면 접촉 후보 추가, `pose-framing-system-semantic-policy-v1`에 라우팅 |
| 행동/대상 정체 | `action`, `prop`, 필요 시 `relational_action` | 접촉 후보가 의미까지 삼키기 쉬움 | 접촉은 보이는 effector–target 관계만, 행동 의미는 해당 슬롯이 소유 |
| gaze 대상 | `gaze_target`/`gaze_engagement` | 포즈와 함께 쓰일 수 있음 | 시선은 접촉·관계를 증명하지 않음 |

`turning_back_over_shoulder_pose`는 `body_pose`의 동작/단계와 `looking_back_over_shoulder_orientation`의 방향이 겹친다. 호환 ID는 유지하되 방향은 후자, 정지/보행/회전 단계는 `body_pose` 또는 `action`이 소유하도록 라우팅 우선순위를 낮추는 편이 낫다.

현재 hard 규칙 `closeup_shot_scale_vs_full_body_pose`는 `contrapposto_full_body`, `power_stance_feet_apart`, `walking_mid_stride_pose`, `stepping_into_frame_pose`, `jumping_motion_pose`, `editorial_s_curve_pose` 여섯 ID만 막는다. `relaxed_standing_weight_shift`, `half_turn_weight_shift_pose`, `pelvic_obliquity_single_support`, `staggered_leg_depth_separation`, `crossed_ankles_narrow_base`, `perched_edge_sit_grounded_support`, `controlled_three_quarter_weight_shift`는 같은 관찰성 문제가 있어도 누락된다. ID 나열을 계속 늘리기보다 후보 메타데이터에 의한 일반 가드가 필요하다.

## 제안 의미 모델

아래는 `photo_prompt_tags.json`의 후보에 붙이고 후보 팩/작성 프롬프트까지 전달해야 하는 원본 메타데이터다. 저장만 하고 프롬프트에 작동시키지 않으면 개선이 아니다.

```json
{
  "pose_mechanics": {
    "phase": "static_hold | locomotor_transition | seated_support | upper_body_orientation",
    "primary_supports": [
      {
        "body_role": "support_foot | pelvis | forearm | back",
        "target_role": "ground | seat | rail | wall",
        "contact_role": "load_bearing | stabilizing"
      }
    ],
    "secondary_supports": [],
    "free_segments": [
      {"body_role": "free_foot", "contact_state": "clearance"}
    ],
    "segment_relations": [
      "pelvis_thorax_azimuth",
      "pelvis_shoulder_counter_tilt",
      "head_shoulder_opposition"
    ],
    "gesture_contacts": [
      {
        "effector": "hand | fingertips | forearm",
        "target_role": "visible_target",
        "contact_role": "touch_only | manipulating | stabilizing | load_bearing"
      }
    ],
    "observability": {
      "required_visible_regions": [],
      "incompatible_shot_scale_facets": []
    },
    "reject_substitutes": []
  }
}
```

좌우는 기본값으로 고정하지 않고 `support/free`, `near/far`, `subject-relative` 역할을 쓴다. 고정 left/right가 필요한 명시 요청만 요청층에서 결합한다.

## 후보 데이터 제안

모두 **broad/advisory 후보**다. 코퍼스 빈도는 기본 선택 권한이 아니며, 새 exact visual-obligation 프로필을 정당화하지 않는다.

### 1. 새 `body_pose`: `single_support_backward_flexed_free_leg`

- 레이어: `photo_prompt_tags.json` → `slots.body_pose`
- `en`: `single-support standing pose with the opposite knee flexed and free foot lifted behind`
- `ko`: `한쪽 발로 지지하고 반대 무릎을 굽혀 발을 뒤로 든 정지 포즈`
- `weight`: `0.60` 제안, 회귀 후 조정
- `embedding_text`: `full-body static pose with one planted support foot under the pelvis, the opposite knee flexed backward and the free foot clearly off the ground behind, with both feet, ankles and the ground contact visible`
- aliases: `one leg planted other bent backward`, `heel lifted behind`, `뒤로 한 발 들기`
- `phase`: `static_hold`
- primary support: `support_foot -> ground, load_bearing`
- free segment: `free_foot, clearance`
- required regions: `pelvis`, `both_knees`, `both_ankles`, `both_feet`, `ground_contact`
- incompatible facets: `shot_scale:close_up`, `shot_scale:extreme_close`, `shot_scale:medium_close`
- reject: `walking_stride`, `jump_or_both_feet_airborne`, `crossed_ankles`, `both_feet_planted`, `seated_knee_up`, `cropped_feet`

### 2. 새 `body_orientation`: `forward_torso_lean_close_crop`

- 레이어: `photo_prompt_tags.json` → `slots.body_orientation`
- `en`: `upper torso leaning toward the camera with coherent shoulder depth`
- `ko`: `어깨 깊이와 목 연결이 읽히는 상체 전방 기울기`
- `weight`: `0.56` 제안
- `embedding_text`: `close or medium portrait where the thorax visibly inclines toward the camera, one shoulder advances in depth and the neck-head chain remains coherent; lower-body support is outside the claim and remains unscored`
- `phase`: `upper_body_orientation`
- required regions: `head_neck_connection`, `both_shoulders`, `upper_thorax`
- reject: `low_camera_only`, `camera_roll_only`, `wide_angle_face_enlargement`, `shoulder_crop_hiding_depth`
- 중요한 부정: `support/load-bearing lower body is not inferred`

### 3. 새 `contact_point`: `fingertip_contact_visible_target_non_support`

- 레이어: `photo_prompt_tags.json` → `slots.contact_point`; `pose-framing-system-semantic-policy-v1`의 steering/routed slots에 `contact_point` 추가
- `en`: `fingertips visibly touching a target without bearing body weight`
- `ko`: `신체 하중을 받지 않고 보이는 대상에 손끝만 닿는 접촉`
- `weight`: `0.54` 제안
- `embedding_text`: `a continuous shoulder-elbow-wrist-hand path ends in fingertips visibly touching a readable target region, with a contact patch or occlusion cue and no body weight transferred through the hand`
- contact role: `touch_only`
- required regions: `arm_path_or_clear_wrist_hand_path`, `fingertips`, `target_contact_region`
- reject: `hovering_near_target`, `target_hidden`, `interpenetration`, `load_bearing_brace`, `disembodied_or_cropped_hand`
- 대상의 종/정체와 행동의 서사는 `prop`/`action`/`relational_action`이 소유한다. 이 후보는 관계·감정·동의·신뢰를 표현하지 않는다.

### 4. 기존 후보 보강

새 ID를 중복 생성하지 않고 다음 후보의 `embedding_text`와 `pose_mechanics`를 강화한다.

| 후보 | 반드시 추가할 관찰 요소 | 혼동 음성 |
|---|---|---|
| `relaxed_standing_weight_shift` | 한 planted support foot, 골반의 지지 쪽 이동, 반대 무릎/발의 이완 상태, 양발·지면 가시성 | cropped hip pop, camera roll, 의복 주름만 |
| `half_turn_weight_shift_pose` | 지지 발과 골반 방향, 흉곽의 half-turn, 목–머리 연속성 | over-shoulder gaze만, 발이 잘린 상반신 회전 |
| `leaning_on_railing_pose` | 발/골반의 기본 지지와 손·전완–난간의 stabilizing 또는 load-bearing 역할을 명시 | 손만 얹고 몸은 직립, 난간 근처 손, 배경 난간 |
| `seated_sideways_chair_pose` | pelvis–seat 접촉, 두 무릎 방향, 최소 한 발 또는 손의 보조 지지 | 의자 옆 서 있기, 좌석이 가려진 crop, 부유하는 골반 |
| `one_knee_raised_seated_pose` | 좌석/바닥 지지, raised knee와 반대쪽 지지 사지 분리 | standing knee lift, crossed legs, 잘린 좌석 |
| `candid_adjusting_balance_pose` | 순간 phase 하나, planted/clearing foot, 이동 방향 | generic blur, hair/fabric motion, 여러 행동 `or` 나열 |
| `turning_back_over_shoulder_pose` | `body_pose`에서는 정지/보행/회전 phase만 유지 | gaze/orientation을 중복 소유 |

## 렌더 게이트

각 게이트는 썸네일 첫 읽기와 native-size 구조 검사를 분리한다. 엄격 사례는 `partial_is_fail`이고, 필수 부위가 애초에 프레임 밖이면 해당 축은 `UNSCORED` 또는 fixture 수준의 observability fail이다.

| 유형 | 썸네일 게이트 | native-size 게이트 |
|---|---|---|
| 정지 single support | planted foot와 뒤쪽 공중 free foot, 굽힌 무릎이 서로 분리되어 즉시 읽힘 | 발목·무릎 연결, 발–지면 접촉 그림자, 두 발의 병합/관통 없음 |
| 표면 지지 | 지지 표면, 신체 축, 주 지지점이 한눈에 함께 보임 | 손바닥/전완/골반 contact patch와 표면 원근이 일치, 틈/관통 없음 |
| touch-only 접촉 | 손/손끝 경로와 대상이 동시에 보이며 접촉인지 근접인지 구별됨 | 손끝–대상 경계의 occlusion/contact shadow가 자연스럽고 하중 지지로 변질되지 않음 |
| close forward lean | 흉곽 경사, 양 어깨 깊이, 머리–목 관계가 읽힘 | 렌즈 원근과 신체 연결이 일관; 하지 하중은 채점하지 않음 |
| locomotor phase | stance/swing 다리와 몸통 방향이 하나의 단계로 읽힘 | 발 clearance/contact shadow, 무릎·발목 연결, 이동 방향 일관 |
| seated support | pelvis–seat와 적어도 하나의 발/손 보조 지지가 함께 읽힘 | 좌석 접촉 가장자리, 관절 연결, 표면과 신체의 관통/부유 없음 |

## 회귀·홀드아웃 설계

### 프롬프트/후보 회귀

1. `full-body contrapposto ...`는 기존 `contrapposto_weight_shift`를 exact 활성화하고 새 일반 single-support가 이를 대체하지 않는다.
2. `full body, one foot planted, opposite knee bent backward, heel clearly off the ground behind`는 `single_support_backward_flexed_free_leg`를 선택하고 walking/jump/crossed-ankles를 배제한다.
3. `walking mid-stride with stance and swing leg`는 `walking_mid_stride_pose`를 선택하고 정지 single-support를 배제한다.
4. `hand lightly rests on railing, body upright, both feet grounded`는 `hand_on_railing` + touch-only contact를 허용하되 `leaning_on_railing_pose`는 배제한다.
5. `forearm bears part of the upper torso load on a railing, both feet grounded`는 `leaning_on_railing_pose`와 load-bearing contact를 선택한다.
6. sideways chair 요청은 pelvis–seat, 무릎 방향, 발 지지를 작성 프롬프트에 모두 남긴다.
7. close portrait + low camera + forward lean은 `forward_torso_lean_close_crop`을 허용하되 lower-body load 후보를 hard reject한다.
8. fingertips touch visible target는 `fingertip_contact_visible_target_non_support`를 선택하고 `hovering` 및 load-bearing brace를 배제한다.
9. Dutch tilt, 의복/머리카락 S 윤곽만 있는 요청은 body support 후보를 활성화하지 않는다.
10. `one leg lifted`가 있어도 결과 픽셀에서 양발 planted면 strict pixel FAIL이다.

### 코퍼스 홀드아웃

- ID 2699: 명시적 contrapposto 양성
- ID 2710: 전신 S-curve, 한쪽 하중, 반대 다리 교차가 함께 있는 혼동 사례
- ID 2534: 안장 + 한 planted foot + 페달 쪽 raised foot + 손–핸들/바구니의 다중 지지 그래프
- ID 2637: crouch + 손–포장 접촉의 stabilizing 사례
- ID 2004: contrapposto이지만 3/4 crop인 프레이밍 음성
- ID 2175: top-down, reclined full-body twist로 카메라/지지 소유권을 분리할 사례

이 여섯 개는 이번 픽셀 표본에 포함하지 않았으며 미래 prompt regression 홀드아웃으로 남긴다. 미래 픽셀 검증은 입력·모델·설정·참조 역할을 arm별로 고정하고, arm당 기록된 생성 1회, 교차-arm 입력 없음, 썸네일/native 별도 채점을 지켜야 한다. 이번 연구에서는 새 이미지를 생성하지 않았다.

## 가설과 반증 조건

| 가설 | 현재 근거 | 반증 조건 |
|---|---|---|
| 표현 격차: 일반 접촉 후보가 역할과 관찰성을 전달하지 못한다 | 2173/2174에서 손 접촉은 보이나 load role은 불명; `contact_point`가 포즈 정책에 미라우팅 | 현 컴파일러가 모든 홀드아웃에서 contact role, target, required region을 후보 팩과 작성 프롬프트에 이미 보존함을 증명 |
| 프롬프트 상호작용: 하중 후보와 close crop이 충돌한다 | 5개 명시 충돌 ID, 2743 픽셀에서 완전 비관찰 | ID 열거 없이 일반 메타데이터 가드가 다섯 요청 모두 하체 하중 후보를 거부함을 증명 |
| 넓은 라벨 치환: `one leg lifted`/S-curve가 양발 planted/팔·의복 곡선으로 치환된다 | 1583 0/2, 1883의 잘린 하체·팔/의복 윤곽 | exact mechanics를 고정한 matched 반복 렌더에서 해당 치환이 재현되지 않고 모든 strict gate가 지속 통과 |
| 복수 행동 분기는 단일 프레임 phase를 과소결정한다 | 1884 두 장의 phase/가시성 차이 | 컴파일러가 한 phase를 결정해 작성 프롬프트에 남기고, 고정 반복에서 같은 phase가 유지됨 |

## 선행 검증과 이번 결정의 경계

기존 `tests/test_photo_pose_visual_semantics.py`, `tests/fixtures/photo_prompt/pose_semantics_five_arm_cases_v1.jsonl`, `artifacts/photo-runs/20260831-pose-semantics-five-arm-v1/RESULTS.md`에는 명명 포즈와 후보 조합의 이전 검증이 있다. 당시 다섯 arm 중 3개, 원자 게이트 25개 중 20개가 통과했고, crossed-ankle 및 elbow–torso negative-space 일부가 실패했다. 이는 “프롬프트/후보 존재 ≠ 픽셀 성공”이라는 경계와 이번 보강 방향을 지지하지만, 이번 ReactorPrompt 32장 관찰을 대신하지 않는다.

따라서 이번 결정은 다음과 같다.

- bounded status: **`proposed`**
- 새 exact visual-obligation 프로필: **추가하지 않음**
- broad/advisory 후보: **3개 제안**
- legacy 후보 의미 보강: **7개 제안**
- 일반 프레이밍 가드와 `contact_point` 라우팅: **설계 제안**
- 런타임/인덱스/테스트/렌더: **미구현·미검증**
- 사용자 픽셀 판단: **수행하지 않음**

## 근거 자료와 재현 명령

### 로컬 근거

- 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 프롬프트 원문: `generated/reactorprompt-export-20260902-incremental/prompts/`
- 이미지 원본: `generated/reactorprompt-export-20260902-incremental/images/`
- 현재 의무 레지스트리: `.agents/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`
- 현재 후보/정책: `.agents/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`
- 승인 연구 레지스트리: `docs/research-evidence/photo-prompt/research_evidence.jsonl`, 관련 ID `body_semantics_getty_contrapposto`, `body_semantics_camera_perspective_shape`, `pose_semantics_nga_figura_serpentinata`, `pose_semantics_met_tribhanga_three_bend`, `pose_semantics_pelvis_rotation_planes`, `pose_semantics_thorax_pelvis_counterrotation`

재현 명령:

```sh
shasum -a 256 generated/reactorprompt-export-20260902-incremental/manifest.json
jq '{posts:length, nonempty_prompts: map(select(.prompt_missing == false and (.prompt|type)=="string" and (.prompt|length)>0))|length, images:[.[].images[]]|length, min_id:(map(.id)|min), max_id:(map(.id)|max)}' generated/reactorprompt-export-20260902-incremental/manifest.json
jq -r '.[] | select(.prompt_missing == false and (.prompt|type)=="string") | [.id, (.prompt|ascii_downcase)] | @tsv' generated/reactorprompt-export-20260902-incremental/manifest.json
jq '.coherence_rules | .. | objects | select((.id? // .rule_id? // "")=="closeup_shot_scale_vs_full_body_pose")' .agents/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json
```

집계 정규식 전문은 위 “전체 프롬프트 스캔” 표의 표현군을 `jq test(...)`에 적용했다. 원시 `weight`, `contact`, `support` 단어 수는 의복·물체·카메라 문맥의 오탐이 많아 최종 수치에서 제외했다.

### 픽셀 표본 파일

```text
1583_DY02Fg5Gkf7_01.jpg  1583_DY02Fg5Gkf7_02.jpg
1584_DY019udGojz_01.jpg  1584_DY019udGojz_02.jpg
1724_DZARzqpGkZm_01.jpg  1724_DZARzqpGkZm_02.jpg
1725_DZARlyAGkPp_01.jpg  1725_DZARlyAGkPp_02.jpg
1883_DZpgpC_GigD_01.jpg  1883_DZpgpC_GigD_02.jpg
1884_DZpfEKMmjLG_01.jpg  1884_DZpfEKMmjLG_02.jpg
2101_DaeuqxKmsFW_01.jpg  2101_DaeuqxKmsFW_02.jpg
2102_DaffrQFGkl8_01.jpg  2102_DaffrQFGkl8_02.jpg
2173_Da2QMtqGkoh_01.jpg  2173_Da2QMtqGkoh_02.jpg
2174_Da2apsbmj9t_01.jpg  2174_Da2apsbmj9t_02.jpg
2377_Dbu7E11mmut_01.jpg  2377_Dbu7E11mmut_02.jpg
2378_Dbu6pEtGhPQ_01.jpg  2378_Dbu6pEtGhPQ_02.jpg
2607_Dcdxfusmvwe_01.jpg  2607_Dcdxfusmvwe_02.jpg
2608_DcdzbCUmrdO_01.jpg  2608_DcdzbCUmrdO_02.jpg
2743_Dcxz9FZGh4u_01.jpg  2743_Dcxz9FZGh4u_02.jpg
2744_Dcx0mrdmn5__01.jpg 2744_Dcx0mrdmn5__02.jpg
```

모두 `generated/reactorprompt-export-20260902-incremental/images/` 아래이며, 파일별 SHA-256과 원본 URL은 매니페스트에 보존되어 있다.

### 외부/승인 출처

- National Gallery of Art, *Michelangelo's David-Apollo*: https://www.nga.gov/content/dam/ngaweb/research/gallery-archives/PressReleases/2012-2010/2012/14A11_74061_20121212.pdf
- The Metropolitan Museum of Art, *Divine Images in Stone and Bronze*: https://resources.metmuseum.org/resources/metpublications/pdf/Divine_Images_in_Stone_and_Bronze_The_Metropolitan_Museum_Journal_v_4_1971.pdf
- Pelvis/trunk plane review: https://pmc.ncbi.nlm.nih.gov/articles/PMC5545133/
- Thorax/pelvis coordination study: https://pmc.ncbi.nlm.nih.gov/articles/PMC9974329/
- Foot plantar/contact mechanics source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6301851/
- Base-of-support review: https://pmc.ncbi.nlm.nih.gov/articles/PMC10440942/
- CVPR 2020, hand contact state/target region 분리: https://openaccess.thecvf.com/content_CVPR_2020/html/Shan_Understanding_Human_Hands_in_Contact_at_Internet_Scale_CVPR_2020_paper.html

이 출처들은 관찰 가능한 지지점, 신체 평면, 손의 contact state/target 분리만 추상화하는 데 썼다. 임상 각도, 안정성·건강 판정, 미적 가치, 관계·의도를 일반화하지 않았다.

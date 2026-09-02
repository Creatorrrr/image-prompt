# 주제 13 — 서사적 사건 시점, 인과 비트, 미완 전환, 가시적 결과

## 결론 요약

**상태: `proposed` (research-only, 미구현).**

새 코퍼스는 `decisive moment`를 새 정확 프로필로 추가해야 한다는 근거보다, 이미 존재하는 정확 프로필과 넓은 품질 축 사이의 **저강도 사건 단계 후보 및 검증 공백**을 더 강하게 보여준다.

- 정확 소유층에는 이미 `peak_action_event_phase`가 있다. 이 프로필은 `화면 안 원인 -> 방향성 궤적 -> 아직 끝나지 않은 즉시 결과`를 요구하고, 속도선·모션 블러·완료된 사후 상태를 대체물로 거부한다. 같은 의미의 정확 프로필을 새로 만들지 않는다.
- 넓은 advisory 소유층에는 `photographic_craft.dimensions[id=decisive_moment]`가 있다. 그러나 실제 새 코퍼스에서는 `mid-step`, `just after`, `about to` 같은 말이 있어도 크롭 때문에 해당 단계가 보이지 않거나, 프레임 밖 호출자·과거 사건·숨은 의도만 문장으로 주장하는 경우가 있었다.
- 보강 우선순위는 다음 세 가지다.
  1. `narrative_phase` 후보에 **접촉 직전, 접촉 시작, 유체 이송 중, 해제 후 계속되는 궤적, 가시적 수습, 가라앉는 여파** 같은 관찰 가능한 일반 단계를 추가한다.
  2. `decisive_moment` 품질 축에 **크롭 안 증거, 원인 소유자, 궤적 소유자, 결과/흔적, 블러 소유자**를 분리하는 게이트를 추가한다.
  3. `친구가 이름을 불렀다`, `말다툼 직후`, `고백 직전`처럼 단일 프레임에서 확인할 수 없는 서사 원인은 검색 힌트로만 두고, 픽셀 판정은 머리·몸의 상반된 방향, 접촉/이격, 물질 상태 같은 가시적 관계로 제한한다.

이번 연구는 새 코퍼스의 924개 비어 있지 않은 프롬프트를 전수 스캔했고, 16개 게시물의 실제 이미지 29개를 직접 검토했다. 29개는 코퍼스 전체 4,908개 이미지의 빈도 표본이 아니며, 이 보고서의 픽셀 관찰은 해당 표본에만 적용된다. 이미지 생성, 런타임 파일 수정, 인덱스 재생성, 새 렌더 자격 판정, 사용자 선호 판정은 수행하지 않았다.

## 1. 범위와 표본 방법

### 1.1 고정 입력

- 매니페스트: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 매니페스트 SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 전체 범위: 게시물 1,182개, 이미지 4,908개, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, 프롬프트 누락 258개, ID 1565–2746
- 비교 기준: `skills/photo-prompt-image-generator`의 지정 기준 리비전 `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 비교 시 생성 인덱스가 아니라 authored source인 `photo_prompt_visual_obligations.json`, `photo_prompt_tags.json`, `photo_prompt_quality_layers.json`을 보았다.

### 1.2 프롬프트 전수 스캔

924개 프롬프트 각각에 대해 대소문자 무시 정규식으로 다음 비상호배타적 신호를 집계했다. 이 수치는 **프롬프트 문구 후보 수**이지 이미지 구현 빈도가 아니다.

| 휴리스틱 | 포함한 대표 표현 | 일치 게시물 |
|---|---|---:|
| `phase_boundary` | `decisive moment`, `capture the instant`, `just before/after`, `immediately before/after`, `about to`, `mid-step/stride/flight`, `caught/frozen mid-*` | 17 |
| `boundary_state_words` | `unfinished`, `in progress`, `ongoing`, `transitioning` | 6 |
| `motion_render` | `motion blur`, `panning`, `fast shutter`, `frozen motion`, `shutter drag`, `action shot` | 33 |
| `physical_trajectory` | `airborne`, `droplet`, `spray`, `splash`, `spilling`, `pouring`, `falling`, `scattering`, `billowing`, `trailing`, `water streams` | 187 |
| `visible_consequence` | `footprints`, `ripples`, `residue`, `debris`, `damp/soaked`, `water stain`, `wet surface`, `torn/cracked`, `released hand`, `half-used/open` | 89 |
| `action_phase` | `reaching`, `releasing`, `catching`, `walking/striding`, `turning`, `pulling`, `stirring/cooking`, `scooping` 등 | 127 |
| `cause_response` | `after hearing`, `after a friend called`, 물질 이동과 결과를 `as ...`로 직접 연결한 좁은 패턴 | 5 |
| `static_near_control` | `posed`, `motionless`, `studio/formal portrait`, `fashion pose` 등 | 86 |

주요 교집합은 다음과 같다.

- `phase_boundary + action_phase`: 10개
- `phase_boundary + physical_trajectory`: 7개
- `phase_boundary + visible_consequence`: 6개
- `phase_boundary + physical_trajectory + action_phase`: 5개
- `action_phase + (physical_trajectory 또는 visible_consequence)`: 43개
- 두 축 이상을 결합한 구조 후보 집합: 49개

휴리스틱은 의도적으로 advisory다. 예를 들어 `unfinished` 6개 중 여러 건은 옷의 raw hem이나 헤어 스타일 상태였고, `motion blur`는 열차 밖 배경이나 보행자에게만 속할 수 있었다. 반대로 ID 2081의 `strides`/`scatters`, ID 2469의 `scoop`, ID 2572의 조리 동작처럼 어형이 규칙에 없어서 강한 시각 사례가 누락되기도 했다. 따라서 49개를 고품질 사건 이미지 수라고 해석하지 않는다.

### 1.3 픽셀 표본

의도 표본으로 12개 양성 후보 게시물과 4개 근접대조 게시물을 선택했다. 초반·중반·후반 ID를 모두 포함하고, 각 게시물에서 가능한 경우 첫 두 이미지를 사용했다.

- 양성 후보: 1819, 1843, 1933, 2081, 2301, 2469, 2566, 2567, 2572, 2578, 2638, 2743
- 근접대조: 1820, 1917, 2273, 2637
- 합계: **16개 게시물, 실제 이미지 29개**
- 모든 29개를 썸네일 비교로 확인하고, 핵심 양성/음성 8개(1819-01, 2081-01, 2469-01, 2567-01, 2572-01, 2743-01, 2273-01, 2637-01)는 원본 크기로 재검토했다.

이 표본은 의미 경계와 실패 양상을 찾기 위한 의도 표본이다. `29/4,908`의 비율을 코퍼스 빈도로 일반화하지 않는다.

## 2. 프롬프트 측 발견

### 2.1 단계 단어는 드물고, 물질/행동 단서는 분산되어 있다

정밀한 단계 경계 표현은 17/924였지만, 궤적 단서는 187/924, 행동 단계 단서는 127/924였다. 즉 코퍼스의 시간성은 `decisive moment`라는 이름보다 다음처럼 분산된 문장 조각으로 더 자주 나타났다.

- 신체 단계: `mid-step`, `walking`, `turning`, `reaching`, `scooping`
- 물질 궤적: 물방울, 물줄기, 꽃잎, 머리카락, 연기, 먼지
- 결과 상태: 젖은 천, 흐트러진 물체, 표면 물결, 반쯤 쓴 물건
- 촬영 표면: 빠른 셔터, 플래시 동결, 모션 블러, 패닝

따라서 검색과 후보 구성은 `phase word` 하나가 아니라 최소 두 개의 독립 신호를 결합해야 한다. 다만 두 축 일치도 hard evidence가 아니며, 정확 프로필 승격에는 기존 `peak_action_event_phase`의 네 그룹 증거가 필요하다.

### 2.2 문장에 적힌 원인과 화면에서 확인 가능한 원인은 다르다

- ID 1843, 1933, 2566은 `친구/누군가가 이름을 불러 돌아본다`고 쓴다. 프롬프트상 원인은 명시적이지만, 호출자·음향·동일 관계는 단일 이미지에서 확인할 수 없다.
- 화면에서 판정할 수 있는 것은 `다리/몸통은 이동 방향을 유지하고, 머리·눈·머리카락은 카메라 쪽으로 회전한다`는 **이중 방향 관계**다.
- 그러므로 `called-name response`는 authored story로 보존할 수 있어도, 후보팩의 픽셀 게이트는 `locomotion_counterturn_midphase`처럼 관찰 가능한 이름을 가져야 한다.

### 2.3 `unfinished`와 `motion blur`는 사건 단계의 충분조건이 아니다

- `unfinished`는 ID 2273의 세팅 중 헤어처럼 물질 상태를 나타낼 수 있지만, 도구·손·접점·다음 단계가 없으면 포착된 전환이 아니다.
- ID 1917은 열차 밖 배경의 흐림이 있지만 주 피사체는 고정된 수면 포즈다.
- ID 2637은 보행자 배경 블러가 풍부하지만 주 피사체는 완결된 정면 패션 포즈다.

촬영 효과는 `capture_medium/motion`의 소유다. 사건 의미는 별도로 actor/source, phase, trajectory, target state 또는 consequence를 가져야 한다.

### 2.4 조용한 임계 장면은 peak action과 다른 후보가 필요하다

ID 2567의 식사 직전 장면은 빠른 움직임이 없지만, `손을 모은 자세 + 수평 젓가락 + 손대지 않은 그릇 + 그릇을 향한 시선`이 다음 동작 직전임을 만든다. ID 2572의 조리 장면도 완성된 음식 포즈가 아니라 `불 위 팬 + 손잡이를 잡은 손 + 주걱과 달걀의 관계`로 active process를 읽게 한다.

이들은 `peak_action_event_phase`를 억지로 활성화할 사례가 아니라, `preparation`, `pause`, `active_process`, `contact_state`를 결합한 advisory 후보의 근거다.

## 3. 픽셀 측 관찰

### 3.1 양성 후보 22개 이미지

| 게시물 / 이미지 | 프롬프트가 주장한 단계 | 픽셀 관찰 | 정렬 판정 |
|---|---|---|---|
| 1819 / 01–02 | 물을 쏟은 직후 수건에 손을 뻗음 | 넓은 젖은 천 경계와 손에 잡힌/닿는 수건이 함께 보인다. 쏟는 원인은 이미 지나갔지만 결과와 수습은 동시 가시적이다. | `aftermath + repair` 강함; spill 원인은 미확인 |
| 1843 / 01–02 | 호출 뒤 돌아보는 `mid-step` | 보행 다리와 팔 스윙, 머리 회전은 보이나 호출자는 없다. | visible counter-turn 강함; 호출 인과는 미확인 |
| 1933 / 01–02 | 해변을 걷다가 이름을 듣고 돌아봄 | 근접 크롭, 얼굴을 가로지르는 머리카락과 돌아본 머리는 보이나 발걸음·발자국은 프레임 밖이다. | 부분 정렬; 보행 단계와 원인은 미확인 |
| 2081 / 01–02 | 큰 보폭, 돌아봄, 꽃잎이 공중에 흩어짐 | 양다리 사이 큰 비대칭, 손의 꽃다발, 공중에 분리된 꽃잎이 같은 프레임에 보인다. | 강한 trajectory/consequence; 바람 원인은 부분적 |
| 2301 / 01 | 바다에 들어가기 직전, 가방에서 반쯤 쓴 선크림에 손을 뻗음 | 가방을 향한 시선·손·선크림 준비 상태가 보인다. 바다 입수라는 다음 사건은 환경 문맥에 의존한다. | preparation 강함; 미래 입수는 미확인 |
| 2469 / 01–02 | 두 손으로 물을 떠 올려 물줄기와 방울을 떨어뜨림 | 손 사이 source, 끊어지거나 이어진 수류, 공중 물방울, 수면 반응이 한 화면에 연결된다. | 강한 `source -> transfer -> receiver` |
| 2566 / 01–02 | 걷다가 호출 직후 시선만 돌림 | 전신 보행, 발 접지 차이, 몸통 진행과 카메라 쪽 머리/시선이 동시에 보인다. | locomotion counter-turn 강함; 호출 원인은 미확인 |
| 2567 / 01–02 | 먹기 직전 | 모은 손, 수평 젓가락, 손대지 않은 라멘, 그릇을 향한 시선이 중앙 삼각형을 만든다. | 조용한 pre-use threshold 강함 |
| 2572 / 01–02 | 달걀 조리 중 | 불 위 팬, 팬 손잡이 그립, 달걀 근처의 주걱이 보인다. 빠른 변화보다 지속 공정 단계다. | active process 강함; decisive peak는 아님 |
| 2578 / 01 | 용의 `mid-flight` | 날개·몸·꼬리의 비스듬한 방향은 읽히지만 접촉 해제나 새 결과는 없다. | 비행 상태는 보임; 사건 비트는 약함 |
| 2638 / 01–02 | 교차로를 `mid-stride`, 머리를 뒤로 돌림 | 보폭, 한쪽 발의 전진, 몸통과 머리의 방향 차이, 뒤로 흐르는 머리카락이 보인다. | locomotion counter-turn 강함 |
| 2743 / 01–02 | `paused mid-step` | crown-to-mid-chest 크롭이라 다리·발·접지·보폭이 모두 보이지 않는다. 정면에 가까운 완성 초상으로 읽힌다. | **실패 대조:** 문구는 있으나 단계 증거가 크롭 밖 |

### 3.2 근접대조 7개 이미지

| 게시물 / 이미지 | 왜 가까운 대조인가 | 픽셀 경계 |
|---|---|---|
| 1820 / 01 | 상자 안을 찾는다고 서술한 굽힌 자세 | 상자와 몸의 접촉은 보이지만 무엇을 찾는지, 직전/다음 단계는 확인할 수 없다. active pose이지 decisive beat의 충분조건은 아니다. |
| 1917 / 01–02 | 열차 배경 모션 블러 | 흐림은 열차 밖 환경에 속하고 주 피사체는 고정된 수면 자세다. `blur != subject event`. |
| 2273 / 01–02 | `unfinished backstage hairstyling` | 핀과 롤이 과정 상태를 암시하지만 도구·손·접촉/해제·가시적 다음 단계가 없다. `unfinished state != captured transition`. |
| 2637 / 01–02 | 움직이는 보행자와 젖은 거리 속 패션 포즈 | 배경은 움직이지만 주 피사체는 정면 응시·중앙 crouch·완결된 손 배치다. `dynamic context != subject event`. |

### 3.3 픽셀에서 반복된 구분

표본 안에서 사건 단계가 가장 잘 읽힌 경우는 다음 중 둘 이상이 같은 주 피사체/물질에 묶였다.

1. **phase geometry** — air gap, 접촉 시작, 하중/접지 차이, 해제된 손, 보폭, counter-rotation
2. **owned trajectory** — 꽃잎·물·머리카락·도구·팔다리의 한 방향 이동
3. **target state or consequence** — 젖은 천, 수면 반응, 손대지 않은 그릇, 조리 중 표면, 흐트러진 물체
4. **crop inclusion** — 위 증거가 설명이 아니라 실제 프레임 안에 있음

반대로 추상 감정, 보이지 않는 호출자, 단순 모션 블러, 공중 입자, `unfinished`라는 상태 말, 역동적 배경만으로는 사건 단계가 안정적으로 읽히지 않았다.

## 4. 프롬프트/픽셀 정렬과 분기

### 4.1 정렬

- 1819: 결과(젖은 천)와 수습(수건 접촉)이 한 프레임에 공존한다.
- 2081: 보행 위상과 공중 꽃잎이 분리되어도 같은 꽃다발/동작과 연결된다.
- 2469: source hands, falling water, receiver surface가 연속적이다.
- 2567: 다음 행동 직전임을 손·도구·대상 상태가 함께 만든다.
- 2638: 전진 보행과 머리 counter-turn이 다른 벡터로 동시에 보인다.

### 4.2 발산

- 1843/1933/2566: 화면은 회전 반응을 지원하지만 `친구가 이름을 불렀다`는 원인을 증명하지 않는다.
- 2743: `mid-step`은 프롬프트에 있으나 해당 신체 부위가 완전히 크롭 밖이다.
- 1917/2637: 블러는 있으나 주 피사체 사건 단계의 소유자가 아니다.
- 2273: 공정 중 상태는 있으나 그 상태가 바뀌는 찰나는 없다.
- 2578: 비행이라는 지속 상태는 보이지만 cause–consequence 관계는 약하다.

이 발산은 prompt-level PASS와 pixel-level PASS를 분리해야 한다는 근거다. 또한 픽셀 판정에서 실제 관계, 숨은 의도, 감정, 성격을 추론하지 않는다.

## 5. 기존 데이터 중복과 정확한 소유층

### 5.1 이미 있는 정확 프로필 — 중복 생성 금지

기준 리비전의 `photo_prompt_visual_obligations.json`에는 `peak_action_event_phase`가 이미 있다.

- 정확 활성어: `peak-action event-phase relation`, `decisive unfinished-action composition`, `결정적 행동 단계 관계`, `원인 동작 결과 동시 구도`
- 필수 그룹: `action_cause`, `action_trajectory`, `action_consequence`, `action_boundary`
- 혼동 대조: posed anticipation, completed aftermath, speed lines, motion blur without cause
- 게이트: thumbnail 원인, both 궤적, both 미완 결과, native 이전/이후/속도그래픽 대체 거부

`tests/test_photo_visual_obligations.py`에도 정확 활성과 `settled pose with decorative speed lines` 음성 회귀가 있다. 따라서 새 exact 프로필 `decisive_moment_v2`나 동의어 복제본은 만들지 않는다.

### 5.2 넓은 품질 소유층

`photo_prompt_quality_layers.json`에는 다음이 이미 있다.

- `quality_profiles.documentary.prompt_focus`: `decisive moment`
- `photographic_craft.dimensions[id=decisive_moment]`
  - 기본: transition, hesitation, aftermath, micro-event
  - refinement: `human_or_animal_transition`, `observer_timing`, `still_life_aftertouch`, `process_phase_transition`
- 인접 축: `shot_intent`, `frame_hierarchy`, `environment_consequence`

일반적인 “프레임이 완결 포즈가 아니라 특정 찰나처럼 읽히는가”는 여기가 소유한다. 다만 현재 문구는 크롭 안 증거, 원인/궤적/결과의 소유자, 블러 소유자를 직접 강제하지 않으므로 아래의 cross-cutting gate를 추가할 후보가 된다.

### 5.3 후보/패싯 소유층

`photo_prompt_tags.json`과 생성기의 facet vocabulary에는 이미 다음 축이 있다.

- 후보 슬롯: `action`, `narrative_phase`, `motion`, `contact_point`, `aftermath_trace`, `ambient_particle`
- facet: `event_phase`, `movement_type`, `movement_phase`, `contact_state`, `material_response`, `process_stage`
- `composition` 슬롯의 `peak_action_event_phase` 후보는 exact profile과 연결되어 있다.

공백은 새 슬롯 자체보다 **관찰 가능한 저강도 사건 후보가 이 facet들을 한 소유 관계로 묶지 못한다는 점**이다. 일부 기존 `narrative_phase` 항목은 `before_confession`, `after_argument`, `after_secret_revealed`처럼 이야기 이름을 먼저 제시한다. 이들은 직접 요청된 authored story는 될 수 있지만, 단일 프레임의 hard pixel fact가 되어서는 안 된다.

### 5.4 인접 주제와의 경계

- 손/도구/물체의 정확 접점 및 해부학: 주제 7(소품 상호작용) 소유
- 보행, 하중, 몸통/머리 counter-rotation의 해부학: 주제 2(포즈) 소유
- 셔터, 블러, 플래시 동결: 주제 3/12(카메라·캡처 매체) 소유
- 얼굴·시선의 미세 판독: 주제 9 소유
- 이 보고서의 소유는 위 신호를 **하나의 시간 단계 및 인과 범위로 연결하는 관계**다.

## 6. 제안하는 의미 구성요소와 혼동 경계

### 6.1 공통 advisory 중간표현

품질 축 또는 candidate pack의 내부 기록으로 다음 필드를 제안한다. 단독 태그가 아니라 한 사건의 소유 관계로 함께 저장해야 한다.

```json
{
  "event_owner": "subject|hand|tool|object|fluid|environmental_source",
  "event_phase": "preparation|initiation|active_process|handoff|release|aftermath|settling",
  "contact_state": "clearance_no_contact|surface_or_medium_contact|equipment_contact|flight_or_separation|post_contact_release",
  "trajectory_owner": "same visible entity or material as event_owner, or null",
  "trajectory_direction": "source-relative visible direction, or null",
  "target_state": "unchanged|beginning_to_change|changed_unsettled|settled",
  "visible_consequence": "one literal in-frame effect, or null",
  "residual_trace": "one literal in-frame residue, or null",
  "crop_evidence": ["literal anchors that remain inside the selected frame"],
  "temporal_claim_scope": "single_frame_observable|authored_but_not_pixel_verifiable",
  "capture_motion_owner": "subject|object|background|camera|none"
}
```

규칙:

- `single_frame_observable`은 event owner와 phase evidence가 프레임 안에 있을 때만 허용한다.
- 보이지 않는 호출자, 대화, 실제 관계, 의도, 감정은 `authored_but_not_pixel_verifiable`로 남긴다.
- `capture_motion_owner=background|camera`는 주 피사체 event evidence로 승격하지 않는다.
- `target_state=changed_unsettled`은 exact `peak_action_event_phase`의 consequence를 지원할 수 있지만, 나머지 exact 그룹을 대신하지 않는다.

### 6.2 혼동 음성

| 제안 의미 | 반드시 거부할 대체물 |
|---|---|
| 접촉 직전 | 가리키는 포즈, 정지한 손, 대상 없는 손짓, 이미 접촉한 상태 |
| locomotion counter-turn | 상체만 보이는 portrait, 완결된 정면 패션 포즈, 머리와 몸이 같은 방향인 보행 |
| 유체 이송 중 | 표면이 젖어 있기만 함, 장식 물방울, source/receiver 없는 공중 입자 |
| 해제 후 궤적 | 계속 꽉 쥔 손, 물체가 정지함, 속도선만 있음 |
| 수습 단계 | 결과 흔적 없는 수건/도구 포즈, generic housekeeping, 표정만 있는 당황 |
| 가라앉는 여파 | 오래된 정적 손상, 장식 먼지/연기, 원인이 없는 배경 블러 |
| quiet pre-use threshold | 이미 사용 중이거나 완료된 대상, 대상이 프레임 밖, 손·도구·시선이 서로 다른 목표를 향함 |

## 7. 후보팩/데이터 제안

아래 항목은 모두 `photo_prompt_tags.json -> slots.narrative_phase`의 **advisory 후보**로 제안한다. BM25F/embedding 검색이 후보를 제시할 수 있으나, baseline event를 바꾸거나 hard visual obligation을 만들 수 없다. 수치 weight는 검색 calibration 후 결정하며, 코퍼스 빈도로 기본값을 정하지 않는다.

### 7.1 제안 후보와 정확 필드

| `id` | `en` / 핵심 관찰 | 권장 `facets` | 주요 alias/keyword |
|---|---|---|---|
| `precontact_readiness_visible_gap` | one actor/tool aligned to a visible target with a small air gap before contact | `event_phase:[preparation]`, `movement_phase:[readiness,initiation]`, `contact_state:[clearance_no_contact]` | `pre-contact gap`, `contact about to begin`, `접촉 직전 이격` |
| `locomotion_counterturn_midphase` | feet/body continue one travel vector while head, gaze, or hair visibly counter-rotates | `event_phase:[active_process]`, `movement_type:[locomotion]`, `movement_phase:[propulsion_release]`, `contact_state:[surface_or_medium_contact]` | `mid-stride head turn`, `walking counter-rotation`, `보행 중 머리 회전` |
| `source_to_receiver_liquid_transfer_midphase` | visible source, continuous or separated liquid trajectory, and receiving-surface response coexist | `event_phase:[active_process]`, `movement_type:[fluid_flow]`, `movement_phase:[flight_transfer]`, `material_response:[particle_or_fluid_displacement]` | `liquid transfer`, `suspended stream`, `source receiver water path` |
| `tool_contact_active_process_phase` | hand/tool contact, working target, and not-yet-finished material state remain visible | `event_phase:[active_process]`, `movement_type:[fine_motor]`, `contact_state:[equipment_contact]` | `active tool contact`, `work in progress`, `도구 접촉 공정 중` |
| `postcontact_release_continuing_trajectory` | hand/tool has separated while the object, limb, fluid, or fabric continues along one direction | `event_phase:[active_process]`, `movement_phase:[propulsion_release,flight_transfer]`, `contact_state:[post_contact_release,flight_or_separation]` | `release follow-through`, `released but still moving`, `해제 후 진행` |
| `visible_mishap_repair_phase` | harmless visible residue/displacement and a concrete restoring action share the frame, without personality/emotion inference | `event_phase:[recovery]`, `movement_type:[fine_motor]`, `contact_state:[surface_or_medium_contact,equipment_contact]` | `visible cleanup`, `minor repair action`, `결과 흔적 수습` |
| `untouched_target_preuse_threshold` | ready hand/tool/ritual geometry and an unchanged target show the instant before use begins | `event_phase:[preparation,pause]`, `movement_phase:[readiness]`, `contact_state:[clearance_no_contact]` | `before first use`, `untouched target`, `사용 직전` |
| `settling_aftereffect_trace_phase` | changed target plus residual motion/trace remains after contact has ended but before the scene fully settles | `event_phase:[aftermath]`, `movement_phase:[deceleration_stabilization]`, `contact_state:[post_contact_release]` | `settling aftermath`, `residual trajectory`, `가라앉는 여파` |

각 후보의 실제 entry에는 현재 스키마에 맞춰 다음 필드를 채운다.

```json
{
  "id": "<above id>",
  "ko": "<observable Korean description>",
  "en": "<observable English description>",
  "weight": "CALIBRATION_REQUIRED",
  "tags": ["event_phase", "observable_timing", "narrative_safe"],
  "aliases": ["<bounded aliases>"],
  "keywords": ["<owner>", "<phase>", "<consequence or gap>"],
  "embedding_text": "<actor/source + phase/contact + target state + consequence; no hidden intent>",
  "facets": {"event_phase": ["..."], "movement_type": ["..."], "movement_phase": ["..."], "contact_state": ["..."]}
}
```

`weight` 문자열은 설계 표기이며 런타임에 그대로 넣는 값이 아니다. 적용 시 별도 retrieval calibration으로 숫자를 정해야 한다.

### 7.2 exact/advisory 분리

**Exact/hard lane**

- 기존 `peak_action_event_phase`를 그대로 소유자로 사용한다.
- hard 활성은 exact term 또는 네 component group을 모두 갖춘 직접 증거에 한정한다.
- 이 코퍼스만으로 새 exact profile을 승격하지 않는다.
- `mid-step`, `just after`, `motion blur`, `unfinished` 한 단어는 hard 활성 근거가 아니다.

**Advisory lane**

- 위 여덟 후보는 BM25F/embedding 및 quality refinement에서만 사용한다.
- 후보는 frozen authorial core의 event를 바꾸거나, 보이지 않는 원인을 추가하거나, 새 관계/감정을 만들 수 없다.
- composer는 모든 후보를 거부할 수 있다.
- 검색 빈도나 이 보고서의 픽셀 표본은 global default 권한이 아니다.

### 7.3 품질 층 보강 제안

`photo_prompt_quality_layers.json -> photographic_craft.dimensions[id=decisive_moment]`에 다음 refinement를 제안한다.

1. `crop_owned_phase_evidence`
   - principle: 주장한 event phase의 신체/도구/대상 증거가 실제 crop 안에 있어야 한다.
   - hard negative: crown-to-chest portrait에 `mid-step`만 쓰기.
2. `visible_cause_scope`
   - principle: 프레임 밖 호출·대화·의도는 authored cause일 수 있지만 pixel cause로 점수화하지 않는다.
3. `motion_owner_separation`
   - principle: subject/object motion, background motion, camera shake를 분리한다.
   - hard negative: 움직이는 배경/셔터 효과만으로 subject decisive moment 판정.
4. `quiet_threshold_legibility`
   - principle: 고속 동작이 없어도 ready geometry + unchanged target + next-step boundary가 보이면 조용한 pre-use phase로 읽을 수 있다.

## 8. 썸네일/원본 렌더 게이트

이 게이트는 향후 구현·렌더 평가용 제안이며, 이번 연구에서 새 렌더로 실행하지 않았다.

### 8.1 Thumbnail gates

1. **Phase first-read:** 프롬프트 없이 `접촉 전 / 접촉 시작 / 진행 중 / 해제 / 직후 / 가라앉는 중` 중 하나를 말할 수 있고, 그 단계의 owner를 가리킬 수 있어야 한다.
2. **Crop inclusion:** 사건을 설명하는 최소 두 anchor가 프레임 안에 있어야 한다. `mid-step`이면 보폭/접지/다리 위상 중 최소 하나가 실제로 보여야 한다.
3. **Direction:** 궤적이 필요한 후보는 source-relative 한 방향이 읽혀야 한다. 무작위 공중 입자는 실패다.
4. **Target/consequence:** peak-action exact는 원인·궤적·미완 결과가 모두 읽혀야 한다. quiet threshold는 ready geometry와 unchanged target가 함께 읽혀야 한다.
5. **No story inference:** 보이지 않는 호출자, 실제 관계, 숨은 의도, 감정 상태를 알아야만 통과할 수 있으면 실패다.

### 8.2 Native gates

1. 접촉 또는 air gap이 손가락·도구·대상 표면에서 해부학적/물리적으로 일관된다.
2. 물·꽃잎·천·머리카락·도구의 궤적이 source와 결과에 연결되며, 복제되거나 무작위로 떠 있지 않다.
3. motion blur 방향이 실제 움직이는 owner에 속한다. 배경 블러와 카메라 흔들림을 주 피사체 궤적으로 오인하지 않는다.
4. `released`를 주장하면 손/도구와 대상 사이 이격이 있고, 계속 `gripping`한 상태는 실패다.
5. target state가 `unchanged`, `beginning_to_change`, `changed_unsettled`, `settled` 중 주장한 단계와 일치한다.
6. 손, 발, 관절, 도구, 대상 형태가 사건을 설명할 수 있을 만큼 온전하다. 해부학/물체 오류가 단계 판독을 만들면 실패다.

모든 필수 게이트는 `partial_is_fail`로 평가하고, 배달되지 않은 렌더는 `UNSCORED`다. 프롬프트 PASS는 픽셀 PASS가 아니다.

## 9. 회귀 및 홀드아웃 테스트

### 9.1 정적/패키지 회귀

1. **기존 exact 유지**
   - positive: direct exact term + visible cause + directional trajectory + unfinished consequence + boundary evidence -> `peak_action_event_phase` hard match.
   - hard negative: settled fashion pose + speed lines; background motion blur; completed aftermath -> hard match 없음.
2. **단일 단어 과활성 방지**
   - `unfinished hem`, `transitioning background gradient`, `after rain`, `during winter`, `mid-thigh crop` -> 사건 exact profile 비활성.
3. **크롭 호환성**
   - positive: full-body mid-stride + visible contact difference + counter-turned head.
   - negative: crown-to-chest portrait에 `paused mid-step`; audit warning 또는 해당 단계 문구 제거 요구.
4. **원인 범위**
   - `after a friend called her name`에서 호출자가 프레임 밖이면 authored cause는 보존하되 pixel evidence에는 `locomotion_counterturn`만 남긴다.
5. **블러 소유권**
   - sleeping passenger + blurred exterior -> subject event facet 없음.
   - moving subject + sharp face + limb/hair trajectory blur -> subject/object owner로만 facet 부여.
6. **retrieval causal pairs**
   - `water held in cupped hands falling to sea`는 `source_to_receiver_liquid_transfer_midphase`를 surface wetness, rain, damp clothing보다 위에 둔다.
   - `unfinished pinned hairstyle`는 process-state 후보를 반환할 수 있지만 captured-transition 후보를 반환하지 않는다.
   - `pre-meal joined hands and untouched bowl`는 quiet pre-use를 반환하고 peak action exact를 반환하지 않는다.

### 9.2 향후 픽셀 회귀 팔

동일 모델/설정/비율을 고정하고 각 팔의 프롬프트를 독립 동결해야 한다. 아래는 제안일 뿐 이번 연구에서는 생성하지 않았다.

| family | positive | hard negative |
|---|---|---|
| liquid transfer | 손/용기 source, 공중 수류, receiver surface response | 젖은 표면만 있고 source/trajectory 없음 |
| locomotion counter-turn | 전진 보행 접지와 머리/시선 counter-rotation | 상반신 portrait, 완결된 정면 포즈 |
| quiet pre-use | ready hands/tool, untouched target, target-directed gaze | 이미 사용 중이거나 대상이 crop 밖 |
| repair after visible mishap | 결과 흔적과 복구 동작 동시 가시 | 수건/도구를 든 정적 포즈, 흔적 없음 |
| release/follow-through | contact separation + continuing trajectory | 계속 쥔 손 + 속도선 |
| settling aftermath | changed target + residual trace + ended contact | 오래된 손상 또는 장식 입자만 있음 |

### 9.3 unrelated held-outs

- 산업: 컨베이어 이송 지점에서 물체가 한 지지면을 떠나 다음 지지면에 막 닿는 순간
- 자연: 새가 수면 착지 직전 날개·발·수면 사이 air gap을 유지하는 순간
- 음식: 소스가 용기에서 접시로 흐르고 첫 표면 변형이 시작되는 순간
- 보존/수리: 도구가 손상 경계에 닿기 직전이고 기준 표면이 함께 보이는 순간
- 무인 장면: 넘어간 물체, 진행 중인 유체, 가라앉는 잔류 흔적만으로 phase가 읽히는 장면

사람이 있는 경우에도 실제 관계, 성격, 의도, 감정, 직업을 픽셀에서 추론하지 않는다.

## 10. 한계와 bounded decision

### 한계

- 픽셀은 의도 표본 29개만 검토했으며 전체 4,908개 빈도를 말하지 않는다.
- 동일 게시물의 이미지들은 유사한 생성 조건을 공유할 수 있어 독립 표본이 아니다.
- 프롬프트 휴리스틱은 어형과 문맥에 민감하다. 49개 구조 후보는 후보 회수용이며 품질 점수가 아니다.
- 새 이미지 생성이나 metadata-blind 독립 평가를 하지 않았다.
- 기존 렌더 fixture의 과거 PASS는 현재 새 코퍼스나 새 제안의 render qualification이 아니다.
- 사용자 미감/선호 판단은 수집되지 않았다.
- 기준 파일은 고정 리비전과 연구 brief의 SHA를 사용해 비교했으며, 작업 중 변할 수 있는 생성 인덱스는 authored evidence로 사용하지 않았다.

### 결정

**`proposed`.**

- 새 exact profile 추가: **reject** — 기존 `peak_action_event_phase`와 중복된다.
- 기존 exact profile의 보존 및 새 hard-negative/crop 회귀 추가: **proposed**.
- 여덟 generic `narrative_phase` advisory 후보, facet binding, blur/crop/causal-scope 품질 refinement: **proposed**.
- 런타임 편집, 인덱스 재생성, 테스트 변경, 렌더 생성, promote: **not performed / unscored**.

## 11. 증거 부록

### 11.1 검토한 이미지 경로

모든 경로의 기준 디렉터리는 `generated/reactorprompt-export-20260902-incremental/`이다.

```text
images/1819_DZZ9ypimina_01.jpg
images/1819_DZZ9ypimina_02.jpg
images/1843_DZkV504mmU3_01.jpg
images/1843_DZkV504mmU3_02.jpg
images/1933_DZ3wPRtGsTh_01.jpg
images/1933_DZ3wPRtGsTh_02.jpg
images/2081_DaX79JTGik4_01.jpg
images/2081_DaX79JTGik4_02.jpg
images/2301_DbcqPDeGqPp_01.jpg
images/2469_DcAdphPGmSJ_01.jpg
images/2469_DcAdphPGmSJ_02.jpg
images/2566_DcQ20r-mp-i_01.jpg
images/2566_DcQ20r-mp-i_02.jpg
images/2567_DcQ2DmbGmJ_01.jpg
images/2567_DcQ2DmbGmJ_02.jpg
images/2572_DcVdWWGmo6Q_01.jpg
images/2572_DcVdWWGmo6Q_02.jpg
images/2578_DcV-QRQGmAZ_01.jpg
images/2638_DcfQhjRmv-R_01.jpg
images/2638_DcfQhjRmv-R_02.jpg
images/2743_Dcxz9FZGh4u_01.jpg
images/2743_Dcxz9FZGh4u_02.jpg
images/1820_DZZ9U24mnke_01.jpg
images/1917_DZxUAYkmuwx_01.jpg
images/1917_DZxUAYkmuwx_02.jpg
images/2273_DbK14xomlc2_01.jpg
images/2273_DbK14xomlc2_02.jpg
images/2637_DcfQm3DmoSa_01.jpg
images/2637_DcfQm3DmoSa_02.jpg
```

### 11.2 재현 명령

프롬프트 분모:

```bash
jq '[.[] | select(.prompt_missing == false)] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json
```

기준 소유층 확인:

```bash
git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json \
  | jq '.profiles[] | select(.id == "peak_action_event_phase")'

jq '.. | objects | select(.id? == "decisive_moment")' \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json

jq '{narrative_phase:(.slots.narrative_phase|length), aftermath_trace:(.slots.aftermath_trace|length), motion:(.slots.motion|length), contact_point:(.slots.contact_point|length)}' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json
```

휴리스틱 구현은 Python `re.I|re.S`로 924개 레코드의 `prompt`에 적용했다. 핵심 phase pattern은 다음처럼 좁게 제한했다.

```text
decisive moment | exact moment | capture(d) the instant |
just before/after | immediately before/after | about to |
caught/frozen mid-(motion|step|stride|turn|swing|jump|fall|flight|action...) |
mid-(air|motion|step|stride|turn|swing|jump|fall|flight|action...)
```

`during`은 `during winter` 같은 시간/장소 문맥 오탐이 많아 precise phase count에서 제외했다. 모든 category는 비상호배타적으로 집계했다.

### 11.3 외부의 권위 있는 참고 자료

- [International Center of Photography — Henri Cartier-Bresson: The Decisive Moment](https://www.icp.org/exhibitions/henri-cartier-bresson-decisive-moment): 사진 자체의 고유한 서사 형식과 출판 제목의 역사적 맥락을 설명한다. 여기서 `decisive moment`를 하나의 고정된 물리 분류표로 보지 않고, 화면 조직과 순간의 결합이라는 넓은 품질 축으로 유지한 근거로 사용했다.
- [Nikon — Capturing or Freezing Motion in Photos](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/capturing-or-freezing-motion-in-photos): 셔터 속도가 움직임을 정지하거나 흐리게 기록한다는 촬영 메커니즘을 설명한다. 이 자료는 `motion blur/freeze`를 사건 의미 자체가 아니라 별도 capture rendering 축으로 분리한 근거로 사용했다.

이 외의 핵심 결론은 새 ReactorPrompt 프롬프트/픽셀과 현재 저장소 authored source의 비교에서 도출했다.

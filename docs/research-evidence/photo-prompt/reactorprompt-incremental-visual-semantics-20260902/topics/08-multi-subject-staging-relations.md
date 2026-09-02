# 08. 다중 피사체 스테이징·시선·근접성·가림·공유 표적·관계 토폴로지

## 결론

**결정: `proposed`**

ReactorPrompt 증분 코퍼스는 `couple`, `friends`, `siblings`, `chemistry` 같은 관계 라벨을 더 추가할 근거보다, 다음처럼 **프레임 안에서 관찰 가능한 관계 그래프**를 별도로 소유할 근거를 제공한다.

```text
동일 프레임/패널 구분
-> 행위자 수·가시성·전경/배경 역할
-> 머리·몸통·손의 방향과 소유자
-> 상대 인물/제3의 표적/카메라 중 시선 도착점
-> 거리·접촉·가림·공통 접근 공간
-> 표적을 향한 행위와 상대의 관찰 가능한 반응
```

프롬프트가 있는 924개 기록을 전수 스캔했다. 고정밀 다중 인물·군중·부분 동반자 쿼리의 합집합은 20개 게시물이었고, 관계 라벨은 35개, 문자 그대로의 `eye contact`는 27개, 프레임 밖 촬영자 관계는 13개였다. 그러나 `eye contact` 대부분은 카메라 응시였고, 관계 라벨 상당수는 프레임 밖 촬영자나 서사 설정이었다. 저장된 **23개 게시물 43장**을 직접 검사한 결과도 나란히 카메라를 보는 두 인물, 같은 방향을 보는 인물과 동물, 배경 군중, 한 사람의 여러 패널이 상호 시선·공유 과업·집단 관계로 잘못 읽힐 수 있음을 보였다.

따라서 포괄 관계어는 검색·후보 힌트로만 두고, 정확한 하드 의미는 `행위자-행위-표적-반응-소유권`을 모두 명시한 좁은 요청에서만 활성화해야 한다. 이 문서는 연구·설계 결과이며 런타임 자산, 색인, 테스트, 생성 이미지에는 변경을 가하지 않았다. 제안 후보의 런타임 동작, 렌더 자격, 요청자 판단은 모두 미검증이다.

## 범위와 표본 방법

### 고정 근거와 증거층

- 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 범위: 게시물 1,182개, 저장 이미지 4,908장, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, 프롬프트 누락 258개, 게시물 ID 1565–2746
- 런타임 비교 기준: Git revision `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- authored source 비교 기준 SHA는 공용 연구 브리프의 동결값을 사용했다. 작업 트리의 다른 에이전트 변경은 근거로 섞지 않았다.
- 증거층은 다음처럼 분리했다.
  - **프롬프트 관찰:** 924개 본문 전수 텍스트 스캔
  - **코퍼스 픽셀 관찰:** 저장된 23개 게시물 43장의 직접 시각 검토
  - **패키지 관찰:** 동결 revision의 후보·캐릭터 반응·visual obligation·계약 파일
  - **외부 연구 근거:** 공동 주의, 집단 공간 구성, 문화권별 선호 거리의 1차 논문
  - **생성 픽셀/사용자 판단:** 없음

프롬프트의 관계 라벨은 픽셀 증거로 취급하지 않았고, 픽셀에서 보이는 접촉이나 방향도 실제 관계, 동일 인물 여부, 정체성, 감정, 동의, 성격의 증거로 확장하지 않았다.

### 프롬프트 전수 스캔

`prompt.strip()`이 비어 있지 않은 924개를 모두 읽고, 다음 고정밀 축을 대소문자 무시 정규식으로 탐색했다.

1. 수가 적힌 다중 출연진: `two|three|four|five|several|multiple|both` 뒤에 `people|women|men|subjects|friends|colleagues|dancers...`
2. 명시적 쌍 또는 부분 출연진: `portrait of a couple`, `second adult companion`, `only ... companion is visible`, `hand and partial arm of another person`, `part of a man's face` 등
3. 양성 군중·배경 출연진: `among passengers`, `crowd behind`, `people in the background` 등. `no crowd`, `no people in the background`는 제외했다.
4. 관계 라벨, 시선 벡터, 근접/접촉, 부분 가시성, 프레임 밖 촬영자, 단일 인물 배제, 다중 패널/시트는 서로 겹치는 별도 쿼리로 집계했다.

이 수치는 문법 파서나 의미 정답이 아니라 **프롬프트 측 탐색 증거**다. 특히 `eye contact`, `friends`, `group`, `four views`는 각각 상호 시선, 실제 관계, 상호작용 집단, 네 명의 동시 출연을 뜻하지 않는다.

### 픽셀 표본

고정밀 합집합 20개 중 초기·중기·후기 ID, 쌍·군중·부분 인물·다중 패널을 모두 포함하도록 표집했다. 여기에 관계 라벨은 있지만 프레임 안 동반자가 없는 경우, 일반 시장 군중, 인물과 동물의 카메라 공동 응시를 대조군으로 추가했다. 대체로 게시물당 `_01`, `_02` 두 장을 열었고 이미지가 한 장뿐인 1852, 2048, 2449는 한 장을 검사해 총 **23개 게시물 43장**이 되었다.

표본은 일반적 쌍과 군중뿐 아니라 다음 혼동 조건을 의도적으로 포함한다.

- 나란히 카메라를 보는 두 인물
- 상대를 보는 쌍과 제3의 표적을 함께 보는 쌍
- 얼굴이 없는 손·팔·몸통만 들어온 동반자
- 전경 인물이 배경 인물을 부분 가리는 깊이 구성
- 무작위 배경 군중과 공통 표적 주변의 집단
- 프레임 밖 친구/동반자 시점
- 동일 인물의 콜라주·회전 시트
- 프롬프트가 같지만 픽셀이 다른 중복 본문

43장 표본의 비율을 4,908장 전체 빈도로 일반화하지 않는다.

## 프롬프트 측 발견과 계수

### 고정밀 다중 피사체 합집합

| 탐색 축 | 프롬프트 수 | 게시물 ID | 해석 경계 |
|---|---:|---|---|
| 수가 적힌 출연진 | 6 | 1857, 1858, 2145, 2472, 2475, 2641 | 2472·2475는 같은 인물의 패널/뷰이며 동시 출연진이 아님 |
| 명시적 쌍 또는 부분 출연진 | 8 | 2233, 2236, 2339, 2346, 2349, 2449, 2551, 2556 | 프레임 밖 촬영자와 부분 신체가 섞임 |
| 양성 군중 또는 배경 출연진 | 6 | 1838, 1846, 1852, 2048, 2355, 2667 | 배경 맥락과 상호작용 집단은 다름 |
| 고정밀 합집합 | **20** | 위 세 행의 합집합 | 중복 없음 |

### 겹치는 보조 축

| 보조 축 | 프롬프트 수 | 관찰된 문제 |
|---|---:|---|
| 폭넓은 관계 라벨 | 35 | `friend`, `couple`, `siblings`, `family`, `colleagues`, `companion`은 시각적 공존이나 실제 관계를 보장하지 않음 |
| 문자 그대로 `eye contact` | 27 | 대부분 렌즈/카메라 응시이며 A↔B 상호 시선과 구별되지 않음 |
| 고정밀 관계 시선 벡터 | 6 | 1857, 1858, 2240, 2339, 2551, 2556; 같은 방향, 카메라, 상대, 프레임 밖 대상이 혼재 |
| 프레임 안 근접·접촉 | 6 | 2145, 2236, 2240, 2339, 2551, 2556 |
| 인물 간 부분 가시성·가림 | 4 | 2233, 2236, 2551, 2641 |
| 프레임 밖 촬영자 관계 | 13 | 1847, 1891, 1912, 2251, 2301, 2449, 2568, 2572, 2705, 2706, 2711, 2712, 2731 |
| 단일 인물 배제 | 26 | `only person`, `one model only`, `no other people` 등; 다중 후보의 음성 경계 |
| 다중 패널·콜라주·캐릭터 시트 | 29 | 같은 인물의 반복 뷰가 인물 수로 오인될 수 있음 |

고정밀 20개 프롬프트를 수동 검토했을 때, **서로 다른 두 참여자가 같은 프레임에서 보이는 외부 물체를 각기 다른 역할로 다루는 명시적 사례는 2233의 케이크 전달과 2556의 모니터/키보드 과업 정도로 제한적**이었다. 이는 코퍼스 빈도 주장이 아니라, 이 쿼리와 수동 판정에서 관계 라벨보다 `누가 무엇을 향해 어떤 행위를 하는가`가 드물게 적힌다는 관찰이다.

### 프롬프트에서 분리해야 할 네 가지 시선

```text
상호 시선       A -> B, B -> A
공유 제3 표적   A -> T, B -> T
평행 카메라 응시 A -> lens, B -> lens
독립 시선       A -> T1, B -> T2
```

`both looking`, `eye contact`, `facing the same direction`만으로 어느 토폴로지인지 정하면 안 된다. 목표 노드와 방향 주체가 없는 표현은 advisory retrieval만 허용해야 한다.

## 픽셀 측 관찰과 표본 ID

아래 표는 저장된 픽셀에서 **보이는 배치와 행동만** 기술한다. 프롬프트의 `couple`, `friend`, `brother`, `boyfriend` 같은 라벨은 실제 관계 판정에 사용하지 않았다.

| 게시물 | 검사 이미지 | 관찰 가능한 공간·행동 관계 | 혼동 또는 결손 |
|---|---|---|---|
| 1838 | 01, 02 | 전경 성인 한 명을 배경 승객과 겹침이 둘러싸 밀도·깊이를 형성 | 군중 맥락은 보이나 특정 두 사람의 공유 표적·상호 시선은 없음 |
| 1843 | 01, 02 | 거리 전경 성인 한 명, 배경 통행인 | 프롬프트의 친구 연락/촬영 설정은 동반자 픽셀 증거가 아님 |
| 1846 | 01, 02 | 주 인물, 가까운 부분 인물, 배경 군중. 01은 인접 인물의 얼굴 방향과 잔이 주 인물 쪽으로 모임 | 보이는 상호작용은 말할 수 있으나 실제 친분은 판정할 수 없음 |
| 1852 | 01 | 여러 인물이 같은 큰 방향으로 정렬된 집단 질량 | 개별 쌍의 시선·반응은 해상도와 밀도 때문에 읽히지 않음 |
| 1857 | 01, 02 | 한 장은 비어 있거나 물체 중심으로 읽히며 두 피사체가 안정적으로 공존하지 않음 | `both facing same direction`의 출연진·관계 의무가 픽셀에서 유지되지 않음 |
| 1858 | 01, 02 | 인물과 고양이의 측면 방향이 대체로 평행 | 공통 방향은 보이나 상호 시선이나 공유 과업은 아님 |
| 2048 | 01 | 보트의 단일 전경 인물과 멀리 있는 사람/보트 | 환경 맥락이지 같은 활동 집단이라고 단정할 수 없음 |
| 2145 | 01, 02 | 두 성인이 가깝고 대칭적으로 나란히 서며 둘 다 카메라를 향함 | co-portrait는 읽히지만 A↔B 시선·상호 행동이나 실제 관계는 보이지 않음 |
| 2219 | 01, 02 | 시장의 주 인물 한 명과 가능한 배경 통행인 | 장면 인구 밀도 대조군; focused group가 아님 |
| 2233 | 01, 02 | 다른 사람의 손·팔이 케이크를 들고 들어오고 주 인물의 머리·눈이 케이크로 향함 | 얼굴 없는 참여자도 소유권·표적이 이어지면 관계 그래프가 읽힘. 고아 손이나 카메라 응시는 음성 |
| 2236 | 01, 02 | 전경의 잘린 성인 몸이 배경 성인을 부분 가리며 깊이와 근접성이 생김 | 두 사람의 시선은 서로보다 카메라/옆 방향에 가까워, 가림만으로 관계를 만들 수 없음 |
| 2240 | 01, 02 | 인물과 고양이의 얼굴이 가깝고 둘 다 카메라 쪽을 향함 | 공유 렌즈 표적은 가능하나 상호 주체성·친밀 관계의 증거는 아님 |
| 2339 | 01, 02 | 얼굴을 마주한 두 성인, 위/아래로 맞물리는 눈·머리 방향, 목/턱 부근 직접 접촉 | 상호 방향·접촉은 보인다. 로맨스, 감정, 동의는 픽셀에서 확정하지 않음 |
| 2346 | 01, 02 | 한 사람의 아침 식사 장면 | 2349와 프롬프트가 바이트 단위로 같지만 요청된 두 얼굴 접촉은 없음 |
| 2349 | 01, 02 | 실루엣 두 인물의 입맞춤, 팔/허리 접촉, 기울어진 자세 | 보이는 접촉만 양성. 실제 관계나 동의 판정에는 사용하지 않음 |
| 2355 | 01, 02 | 에스컬레이터 전경 한 명과 먼 배경 사람 | 배경 군중은 관계 집단을 대신하지 않음 |
| 2449 | 01 | 방/문가의 한 인물 | 프롬프트의 동반자 카메라 시점은 프레임 밖 캡처 관계이며 두 인물 스테이징이 아님 |
| 2472 | 01, 02 | 2×2 콜라주에 한 인물의 여러 뷰가 반복 | 네 명의 동시 출연이 아님. 패널 간 얼굴 일관성도 별도 문제 |
| 2475 | 01, 02 | 한 인물의 정면·측면·후면 회전 시트 | 반복 뷰를 다중 피사체 관계로 계수하면 안 됨 |
| 2551 | 01, 02 | 잘린 동반자 몸통과 한 팔/손이 주 인물의 윗팔에 연결되고, 주 인물 머리는 프레임 밖 동반자를 향함 | 얼굴이 없어도 연결된 팔·접촉점·시선으로 그래프가 읽힘. 신체 소유권이 핵심 |
| 2556 | 01, 02 | 방/참조/회전 시트에 가까운 합성 이미지 | 프롬프트의 상세한 두 인물 모니터·키보드 상호작용이 정지 이미지에 보존되지 않음 |
| 2641 | 01, 02 | 골목의 전경/배경 두 성인, 큰 크기·깊이 분리, 둘 다 카메라 쪽에 가까운 방향 | 공간 공존은 보이지만 상호 표적·행위는 없음 |
| 2667 | 01, 02 | 체육관 전경 한 명과 작은 배경 사람들 | 일반 배경 맥락이며 관계 집단이 아님 |

표본에서 반복된 가장 중요한 경계는 다음과 같다.

- **근접성은 관계가 아니다.** 2145와 2236은 가까워도 상호 시선·공유 행동이 없다.
- **가림은 깊이 증거이지 관계 증거가 아니다.** 2236과 2641은 앞뒤 순서를 만들지만 상대를 향한 행동은 별도다.
- **카메라는 하나의 표적이다.** 2145와 2240처럼 두 피사체가 렌즈를 보는 것은 A↔B가 아니라 A→lens, B→lens다.
- **부분 신체도 행위자가 될 수 있다.** 2233과 2551은 연결된 팔, 접촉점, 표적, 상대의 방향이 함께 있을 때만 읽힌다.
- **패널 수는 출연진 수가 아니다.** 2472와 2475는 같은 프레임의 사회적 관계가 아니라 매체 구성이다.
- **군중은 focused group가 아니다.** 1838, 2048, 2219, 2355, 2667의 배경 사람들은 특정 공통 표적 접근이나 상호 반응을 보장하지 않는다.

## 프롬프트/픽셀 정렬과 발산

### 정렬이 강한 조건

1. **행위자와 표적이 모두 보일 때:** 2233의 손-케이크-받는 인물 방향은 두 얼굴이 없어도 관계가 읽혔다.
2. **방향이 신체 여러 부위에서 일치할 때:** 2339는 눈만이 아니라 머리, 얼굴 평면, 몸의 거리, 접촉점이 함께 두 인물 사이로 모였다.
3. **부분 크롭의 소유자가 연결될 때:** 2551은 팔이 몸통에서 접촉점까지 이어져 프레임 밖 인물의 위치가 제한된다.
4. **공간 역할이 분리될 때:** 전경 주 인물, 중경 두 번째 인물, 배경 군중을 각기 다른 actor role로 기록하면 단순 count보다 안정적이다.

### 발산과 데이터 위험

- **동일 프롬프트, 다른 픽셀:** 2346과 2349의 프롬프트 SHA-256은 모두 `2331d121b83b3b30ef910b680c9143a4c5ef8227a78d8c3868bcd4563110f6ad`이다. 텍스트는 두 얼굴의 입맞춤을 요청하지만 2346은 한 사람의 아침 장면, 2349는 두 사람의 접촉 장면이다. 검증된 연결 정보 없이 이 두 쌍을 학습·게이트 정답으로 쓰면 안 된다.
- **상세 시퀀스가 정지 이미지에 없음:** 2556은 공유 모니터/키보드, 행위 교대, 반응까지 프롬프트에 있지만 표본 픽셀은 관계 시퀀스를 보여주지 않는다.
- **라벨만 남고 상대가 없음:** 1843·2449의 친구/동반자 촬영 설정은 프레임 밖 캡처 관계일 뿐 co-present dyad가 아니다.
- **출연진 결손:** 1857은 `both`와 같은 방향을 말하지만 두 주체가 안정적으로 보이지 않는다.
- **장면 밀도 과잉 대체:** 배경 사람 수를 늘리는 것으로 상호작용 집단을 대신할 수 없다.

따라서 corpus text-image pair는 `prompt present`만으로 양성 fixture가 되지 않는다. 최소한 원본 픽셀, 파일 SHA, 게시물 ID, 프롬프트 SHA, 사람이 확인한 relation graph를 함께 고정해야 한다.

## 기존 데이터 중복과 소유층

### 이미 있는 강점

동결 revision의 `photo_prompt_character_moe_extension.json`에는 `relationship_blocking` family와 두 preset이 이미 있다.

- `character_relationship_chemistry_scene`
  - `shared_focus`
  - `complementary_action`
  - `reciprocal_response`
- `character_pose_proxemics_scene`
  - `support_or_weight_point`
  - `distance_relative_to_task`
  - `orientation_or_shared_target`

같은 family에 연결된 runtime node는 17개이며, 그중 `dyad_shared_gaze_target`, `dyad_mutual_orientation_blocking`, `relationship_complementary_handoff`, `relationship_group_access_arc`, `relationship_mutual_gaze_release`, `relationship_shared_focus_blocking`, `pose_gesture_proxemics`는 이 연구와 직접 겹친다. 특히 다음 정의는 유지할 가치가 있다.

- 공유 초점: 두 참여자의 머리·몸통·도달 공간이 하나의 보이는 표적에 맞는다.
- handoff: 한쪽이 물체를 내밀거나 놓고, 다른 손이 충돌 없이 그 물체에 정렬된다.
- group access arc: 집단이 초점 물체에 접근 가능한 열린 호를 만든다.
- mutual gaze release: 짧은 상호 시선이 공유 표적이나 과업으로 해소된다.

`photo_prompt_scene_expression_character_moe.json`에도 관계 chemistry, pose/proxemics, 얼굴/시선 인상, quiet care, ensemble, companion reciprocity의 관련 route family 6개와 family당 4개 blueprint가 있다. `only an adult friend's hand entering frame`, ensemble focus handoff, companion signal/response/task agency도 이미 존재한다.

`photo_prompt_visual_obligations.json`의 좁은 exact/hard profile도 다음과 같이 상당하다.

- 표적 반응을 요구하는 `target_directed_seductive_display`, `playful_flirtation_interaction`
- 대치·개입·유대 관계인 `formal_biwu_reciprocal_salute_standoff`, `wuxia_bamboo_forest_aerial_duel`, `xia_protective_intervention_event`, `familiar_practitioner_reciprocal_bond`
- 소유 물체·전승·동반자 시점인 `other_owned_object_covetous_approach`, `local_legend_site_transmission`, `companion_viewpoint_everyday_candid`
- 집단 관계인 `adult_multi_interest_harem_ensemble_relation`, `adult_central_target_romantic_rivalry_event`, `overhead_social_snapshot_relation`

이들은 좁은 요청에 대해 `all-of` 게이트와 대체 불가 조건을 이미 소유한다. 새 제안은 이 장르·관계별 하드 프로필을 복제하지 않는다.

### 구조적 공백

현재 데이터에는 주제 중립적인 typed `relation_graph`가 없다. 다음 정보가 자연어 정의나 개별 profile에 흩어져 있다.

- actor ID와 정확한 수
- `full | partial | off_frame | background_context` 가시성
- 동일 프레임인지, 패널/시퀀스인지
- primary/secondary/context 역할과 depth layer
- gaze target이 상대, 제3의 물체, 렌즈 중 무엇인지
- 접촉하는 사지와 접촉 대상의 소유자
- crop에서 들어온 신체의 연속성
- occlusion 순서와 최소 보존 landmark
- 군중 맥락과 focused group의 차이
- 실제 관계·감정·동의로 넘어가지 않는 inference ceiling

### 권장 소유 경계

- **authorial core / composition contract:** actor 수, same-frame 여부, 주/부/맥락 역할, depth/occlusion order, 관계 그래프의 필수 edge. 프롬프트 본문이 정확히 요구한 관계는 core가 소유해야 한다.
- **character mechanism candidate pack:** 시선·몸 방향·거리·접촉·handoff·group access의 관찰 가능한 실현 후보. 열린 차원만 보완하며 core 관계를 바꾸지 않는다.
- **visual obligation exact profile:** `actor-action-target-response`가 좁게 명시된 요청만 하드 활성화한다. BM25F/embedding hit는 advisory이며 hard route가 아니다.
- **capture/viewpoint layer:** 프레임 밖 친구·동반자 촬영자, POV, 카메라 보유자. co-present actor count와 분리한다.
- **media/layout layer:** collage, contact sheet, turnaround, sequence. panel count와 actor count를 분리한다.
- **quality layer:** 일반적인 신체 연속성, 충돌 없는 접촉, 시선의 물리 가능성. 특정 관계나 거리 규범을 기본값으로 넣지 않는다.

## 제안 시각 의미 성분과 혼동 경계

| 성분 | 관찰 가능한 양성 | 혼동 음성 | 권장 소유층 | 검토 게이트 |
|---|---|---|---|---|
| 1. actor cardinality | 동일 프레임의 서로 분리된 신체/실루엣 수 | 같은 인물의 패널·거울·포스터·사진 | core `actors`, media layer | 썸네일에서 수와 주/부 역할이 즉시 읽힘 |
| 2. frame mode | `single_scene`, `multi_panel`, `sequence` | 콜라주의 칸 수를 사람 수로 계산 | core/media | 패널 경계와 시간 단계가 actor graph와 분리 |
| 3. visibility/crop ownership | full/partial/off-frame/context, 연결된 몸통-사지-접촉점 | 고아 손, 융합 몸, 어느 인물 손인지 불명 | core + character candidate | 원본에서 사지 연속성과 소유자가 하나로 결정됨 |
| 4. depth/occlusion order | A가 B의 특정 윤곽을 가리고도 B의 필수 landmark가 남음 | 겹침만 있음, 얼굴 병합, 두 번째 인물 소실 | composition | 썸네일의 앞뒤 순서와 원본의 경계가 일치 |
| 5. mutual gaze | A 눈/머리→B 얼굴, B 눈/머리→A 얼굴 | 둘 다 렌즈, 같은 방향, 한쪽만 상대를 봄 | character mechanism; exact request만 hard | 양쪽 벡터가 물리적으로 교차하고 각 주체가 구별됨 |
| 6. shared third target | A→T와 B→T, T가 보이고 두 몸의 도달/반응이 맞음 | 둘 다 카메라, 서로 다른 물체, 표적이 프레임 밖 | character mechanism | actor-action-target가 썸네일, 손/눈 정렬이 원본에서 유지 |
| 7. parallel lens gaze | A→lens, B→lens | mutual gaze/chemistry로 오인 | capture/composition guard | 카메라 축을 명시적 target node로 기록 |
| 8. body orientation | 머리뿐 아니라 몸통·발·도달 공간이 상대/표적과 호환 | 얼굴만 돌고 몸은 불가능한 방향, 단순 나란히 서기 | pose/proxemics | 머리-몸통-손의 큰 방향이 서로 모순되지 않음 |
| 9. task-relative distance | 과업·접촉·표적 도달에 맞는 상대 거리 | 고정 cm 밴드, 가까움=친밀함 | character mechanism/quality | 과업 수행 가능성으로 평가, 문화/관계 추론 금지 |
| 10. contact ownership | source limb, target body/object site, 연결, 압력/반응 단서 | 떠 있는 손, 관통, 불명확한 소유자, 근접만 있음 | character mechanism; 좁은 hard profile | 원본에서 손가락·사지 연결, 접촉점, 상대 반응 확인 |
| 11. handoff topology | giver hand→object←receiver hand, 이동 방향과 비충돌 정렬 | 같은 물체 없이 두 손만 가까움, 서로 다른 물체 | 기존 handoff node 확장 | 물체가 두 역할 사이의 한 표적으로 유지 |
| 12. focused-group access | 여러 몸이 하나의 가시 표적 주위 열린 접근 공간을 공유 | 줄, 무작위 군중, 배경 인파, 닫힌 벽 형태 | 기존 group access arc | 초점 물체와 참여자별 접근/방향이 모두 읽힘 |
| 13. context crowd | 작은 배경 인물, 겹침, 밀도·장소 규모 | focused group나 상호 관계로 과해석 | composition/context | primary actor와 context actor를 별도 계층으로 유지 |
| 14. response/consequence | 표적 이동, 받는 손, 몸의 회피/따라감 등 상대 행위의 결과 | 정적인 포즈 두 개, 라벨만 chemistry | visual obligation/character response | 원인 행위와 관찰 가능한 결과가 같은 프레임/고정 phase에 공존 |
| 15. inference ceiling | `visible_contact`, `shared_target`, `mutual_orientation`까지만 기록 | 실제 연애·친분·혈연·동의·감정·정체성 판정 | schema policy | 사람이 검토해도 비시각 주장 필드가 생성되지 않음 |

외부 연구는 이 분해를 제한적으로 뒷받침한다. Scaife와 Bruner의 공동 시선 연구는 한 사람의 시선이 다른 관찰자를 환경의 위치로 유도할 수 있음을 보였지만, 이것이 성인의 실제 관계나 내적 상태를 증명하지는 않는다. Setti 등의 still-image F-formation 연구는 위치와 몸 방향, 모두가 접근할 수 있는 공통 공간을 이용해 대화 집단을 모델링한다. 이는 거리 하나보다 orientation과 shared access를 써야 한다는 근거이지 실제 친분의 증거가 아니다. Sorokowska 등의 42개국 연구는 선호 대인 거리가 문화·성별·나이 등과 함께 달라짐을 보고하므로, 보편적인 고정 cm 임계값을 런타임 게이트로 두면 안 된다.

## 후보팩/데이터 제안

### 1. 주제 중립 `relation_graph` 계약

제안 위치: authorial core가 소유하고 composition contract가 검증하는 구조화 레코드. 후보팩은 비어 있는 edge의 시각적 실현만 제안한다.

```json
{
  "relation_graph": {
    "frame_mode": "single_scene",
    "same_frame_required": true,
    "actors": [
      {
        "actor_id": "A",
        "visibility": "full",
        "crop_anchor": "none",
        "depth_layer": "foreground",
        "visual_role": "primary"
      },
      {
        "actor_id": "B",
        "visibility": "partial",
        "crop_anchor": "arm_hand",
        "depth_layer": "foreground",
        "visual_role": "secondary"
      }
    ],
    "referents": [
      {"target_id": "T1", "visible": true, "owner_actor_id": "B"}
    ],
    "edges": [
      {
        "source_id": "B",
        "relation_type": "presents_or_handoffs",
        "target_id": "T1",
        "source_body_part": "connected_hand",
        "phase": "offer"
      },
      {
        "source_id": "A",
        "relation_type": "gaze_to_referent",
        "target_id": "T1",
        "observable_response": "head_and_eye_orientation"
      }
    ],
    "occlusion_order": ["B.arm_hand", "T1", "A"],
    "inference_ceiling": "visible_spatial_and_behavior_relation_only"
  }
}
```

필수 필드:

- `frame_mode`, `same_frame_required`
- `actors[].actor_id`, `visibility`, `depth_layer`, `visual_role`
- 부분 신체일 때 `crop_anchor`와 `connected_to_actor_id`
- `referents[].target_id`, `visible`, `owner_actor_id`
- `edges[].source_id`, `relation_type`, `target_id`, `phase`
- 접촉일 때 `source_body_part`, `target_site`, `continuity_required`
- `occlusion_order`, `minimum_visible_landmarks`
- `inference_ceiling`

### 2. advisory character candidate node

제안 위치: `photo_prompt_character_moe_extension.json`의 `relationship_blocking` family. 다음은 새 라벨이 아니라 기존 relation mechanism의 빠진 typed variant다.

- `dyad_mutual_gaze_topology`
- `dyad_shared_third_target`
- `parallel_camera_gaze_not_reciprocity` — 양성 후보가 아니라 충돌/대체 방지 guard
- `cropped_companion_limb_ownership`
- `foreground_background_actor_separation`
- `crowd_context_without_pairwise_relation`
- `focused_group_common_access_space`
- `same_frame_relation_not_panel_multiplicity` — media/layout guard

각 candidate 레코드는 최소한 다음을 가져야 한다.

```json
{
  "id": "dyad_shared_third_target",
  "family_ids": ["relationship_blocking"],
  "requires": {
    "actor_count": 2,
    "same_frame": true,
    "visible_target_count": 1,
    "gaze_edges": ["A->T1", "B->T1"]
  },
  "confusion_negatives": [
    "A->lens and B->lens",
    "A->T1 and B->T2",
    "target absent or fully hidden",
    "multi-panel repetition"
  ],
  "claim_boundary": "Do not infer actual relationship, emotion, consent, or identity."
}
```

### 3. 좁은 exact visual-obligation profile 후보

제안 위치: `photo_prompt_visual_obligations.json`. broad `friend`, `couple`, `family`, `chemistry`, `eye contact`만으로는 활성화하지 않는다. 정확한 명시가 있을 때만 다음 profile을 검토한다.

1. `cropped_companion_visible_contact_relation`
   - 필수: 부분 참여자의 연결된 사지, 명확한 접촉점, 상대의 호환 가능한 방향/반응, 한 명의 소유자로 결정 가능한 신체
   - 거부: floating hand, ambiguous owner, 접촉 없이 근접, 두 번째 인물이 완전히 소실
2. `foreground_background_two_actor_occlusion_relation`
   - 필수: 두 actor, 지정 depth order, 필요한 landmark, 명확한 occlusion edge, 요청된 시선/행위 edge
   - 거부: face merge, background actor erased, 겹침만 있고 관계 edge 없음
3. `two_adult_shared_target_handoff`
   - 필수: 두 성인 외관 actor, 하나의 보이는 물체, giver action, receiver alignment/response, 비충돌 hand ownership
   - 거부: 서로 다른 물체, 카메라 공동 응시, 정적인 손 두 개, 물체 소유 불명
4. `focused_group_shared_access_formation`
   - 필수: 정확한 참여자 수 또는 허용 범위, 하나의 보이는 focal target, 각 참여자의 orientation/access, primary group와 context crowd 분리
   - 거부: queue, random crowd, 모두 렌즈만 봄, focal target 없음

모든 hard profile은 기존처럼 **all-of**다. 하나라도 빠지면 `partial_is_fail`이며, crop이나 해상도 때문에 판단할 수 없으면 `UNSCORED`다. `UNSCORED`는 품질 0도 PASS도 아니다.

### 4. scene blueprint와 provenance

제안 위치: `photo_prompt_scene_expression_character_moe.json`에는 장르 중립의 held-out blueprint만 추가한다. 동기를 준 ReactorPrompt 장면 문구를 기본 prompt fragment로 복사하지 않는다.

- 부분 팔이 하나의 물체를 내밀고, 주 인물은 물체를 보는 단일 프레임
- 앞뒤 두 인물이 겹치지만 각 얼굴/몸 방향이 분리되는 장면
- 두 참여자가 같은 작업 표면을 공유하되 카메라는 보지 않는 장면
- 작은 집단이 공통 물체 주위에 열린 접근 호를 만드는 장면

모든 fixture는 `corpus_post_id`, `corpus_image_sha256`, `prompt_sha256`, `human_verified_relation_graph`, `review_scale`, `review_status`를 보존해야 한다. 2346/2349처럼 텍스트 중복과 픽셀 불일치가 있으면 `pair_alignment: rejected`로 남긴다.

## 썸네일·원본 게이트

### 썸네일 게이트

- 요청된 actor 수와 primary/secondary/context 역할이 첫눈에 분리된다.
- `single_scene` 관계는 그리드·콜라주·turnaround로 대체되지 않는다.
- 상호 시선 또는 공유 표적은 큰 머리/몸 방향과 표적 위치로 먼저 읽힌다.
- 전경/배경 실루엣과 occlusion order가 병합 없이 읽힌다.
- 배경 군중이 focused group를 대체하지 않는다.
- 잘린 동반자는 최소한 연결된 신체 진입점과 관계 행위를 유지한다.

### 원본 게이트

- 눈·머리·몸통 벡터가 물리적으로 가능한 하나의 도착점을 가리킨다.
- 사지의 시작점, 관절, 손가락, 접촉점이 한 actor 소유로 이어진다.
- handoff 물체가 giver와 receiver 사이에서 하나의 물체로 유지되고 손이 충돌하지 않는다.
- secondary actor의 `minimum_visible_landmarks`가 crop/가림 뒤에도 남는다.
- occlusion edge와 깊이 순서가 머리카락·팔·의상 경계에서 일관된다.
- 표적의 owner와 각 actor의 반응이 프롬프트 phase에 맞는다.
- 입맞춤·포옹 같은 접촉도 `visible_contact`까지만 점수화하며 실제 관계·감정·동의는 채점하지 않는다.

### 공통 판정

`actor + action + target + observable response/consequence` 중 hard profile이 요구한 항목은 같은 평가 이미지에 모두 공존해야 한다. 한 장면에 관계를 모두 담으라는 요청이 아니고 명시적 sequence라면 phase별 그래프를 따로 평가하되, 다른 phase의 성공으로 실패한 phase를 보충하지 않는다.

## 회귀 및 held-out 테스트

| 테스트 | 양성 조건 | hard negative / 거부 대체 |
|---|---|---|
| 부분 케이크 전달 | 연결된 donor 팔·손, 같은 케이크, recipient 머리/눈이 케이크로 향함 | 떠 있는 케이크, 고아 손, recipient가 카메라만 봄 |
| 전경/배경 dyad | 명확한 두 actor와 depth order, 필요한 얼굴/몸 landmark, 요청된 관계 edge | 얼굴 병합, 배경 actor 소실, 단순 겹침 |
| 공유 도구 handoff | 서로 다른 actor 손, 하나의 도구, 주는/받는 phase 정렬 | 각자 다른 도구, 정적인 공동 소유, 손 충돌 |
| 상호 시선 | A→B와 B→A가 눈·머리 방향에서 함께 성립 | 나란히 렌즈 응시, 같은 방향 보기, 한쪽만 응시 |
| 공유 제3 표적 | 보이는 T, A→T와 B→T, 도달/반응 호환 | T 없음, 카메라 co-gaze, 서로 다른 T |
| 인물+동물 카메라 co-gaze | capture target node로만 기록 | reciprocal companion agency 또는 실제 유대의 양성으로 사용 |
| 시장/열차 군중 | context crowd와 primary actor 분리 | focused group/관계 chemistry로 활성화 |
| focused group | 보이는 공통 물체, 참여자별 방향, 열린 접근 공간 | 줄, 무작위 근접 인파, 배경 extras |
| 4패널 동일 인물 | `multi_panel`, actor count 1 | actor count 4, social group |
| turnaround sheet | `multi_panel/reference`, actor count 1 | same-frame dyad/group |
| 프레임 밖 친구 촬영 | capture/viewpoint relation | co-present dyad count 또는 상호 시선 |
| 잘린 동반자 접촉 | 몸통-사지-접촉점이 이어지고 주 인물 방향이 호환 | orphan limb, 소유자 불명, 융합 신체 |
| 입맞춤/포옹 | 보이는 접촉·상대 방향만 양성 | 실제 관계, 동의, 감정, 정체성 판정 |
| 중복 프롬프트 불일치 | 검증된 이미지별 relation graph 사용 | 2346과 2349를 같은 양성 text-image pair로 자동 채택 |
| 출연진 결손 | 요청한 모든 actor와 edge가 존재 | `both`가 있으나 한 주체만 보임 |

구현 전 최소 회귀 세트는 위 15개 개념당 양성 1개와 hard negative 2개 이상을 가져야 한다. 썸네일 PASS와 원본 PASS를 별도로 기록하고, 자동 audit PASS를 픽셀 PASS나 요청자 승인으로 보고하지 않는다.

## 한계와 제한된 결정

- 픽셀 표본은 목적 표집한 43장/23개 게시물이며 전체 4,908장의 빈도 추정이 아니다.
- 정규식 계수는 prompt-side retrieval 증거다. 자연어 부정, 은유, 장면 밖 인물, 패널 구성을 완전하게 해석하지 않는다.
- 일부 이미지의 눈동자 방향은 해상도·측면광·가림 때문에 정확히 판단하기 어렵다. 그런 경우 `UNSCORED`가 맞다.
- 정지 이미지는 짧은 상호 시선 후 공유 과업으로 넘어가는 시간 관계나 handoff의 이전/이후를 한 장에서 모두 증명하지 못할 수 있다. 명시적 sequence는 phase별로 검토해야 한다.
- 외부 연구는 공동 시선, 공통 접근 공간, 거리의 문화 차이를 설명하는 기전 근거일 뿐 이 코퍼스의 실제 관계나 생성 성공률을 입증하지 않는다.
- 2346/2349 불일치는 코퍼스의 모든 prompt-image 연결이 틀렸다는 뜻이 아니라, **연결 검증 없는 자동 양성화가 안전하지 않다**는 반례다.
- 이 보고서는 candidate schema와 gate를 제안했을 뿐 authored asset, generated index, test fixture, 독립 렌더 arm을 만들지 않았다.

따라서 현재의 제한된 결정은 `proposed`다. 다음 단계는 (1) 주제 중립 relation graph의 authored schema 검토, (2) motivating corpus와 분리된 held-out fixture 작성, (3) 자동 source/contract audit, (4) 독립 입력의 렌더 arm, (5) thumbnail/native all-of 검토, (6) 별도 요청자 판단 순서여야 한다. 이 단계가 끝나기 전에는 “후보팩 강화 완료”나 “픽셀 검증 완료”라고 말할 수 없다.

## 증거 부록

### 검사 이미지 경로

모든 경로는 `generated/reactorprompt-export-20260902-incremental/` 아래다.

- `images/1838_DZkYO76Goxn_01.jpg`, `images/1838_DZkYO76Goxn_02.jpg`
- `images/1843_DZkV504mmU3_01.jpg`, `images/1843_DZkV504mmU3_02.jpg`
- `images/1846_DZkUuWqmup1_01.jpg`, `images/1846_DZkUuWqmup1_02.jpg`
- `images/1852_DZkOvc2gcs__01.jpg`
- `images/1857_DZnAmOrmuVf_01.jpg`, `images/1857_DZnAmOrmuVf_02.jpg`
- `images/1858_DZm0W_Tmu3p_01.jpg`, `images/1858_DZm0W_Tmu3p_02.jpg`
- `images/2048_DaQI2joGmCJ_01.jpg`
- `images/2145_DarleXXmn2D_01.jpg`, `images/2145_DarleXXmn2D_02.jpg`
- `images/2219_DbA9vnSmtpk_01.jpg`, `images/2219_DbA9vnSmtpk_02.jpg`
- `images/2233_DbDFirWGuGm_01.jpg`, `images/2233_DbDFirWGuGm_02.jpg`
- `images/2236_DbDDsQumrpD_01.jpg`, `images/2236_DbDDsQumrpD_02.jpg`
- `images/2240_DbDCe6TmjL5_01.jpg`, `images/2240_DbDCe6TmjL5_02.jpg`
- `images/2339_DbnJalMGnLD_01.jpg`, `images/2339_DbnJalMGnLD_02.jpg`
- `images/2346_DbnJkdLGoDJ_01.jpg`, `images/2346_DbnJkdLGoDJ_02.jpg`
- `images/2349_DbnJfpqmg1c_01.jpg`, `images/2349_DbnJfpqmg1c_02.jpg`
- `images/2355_DbqQWmsGpVs_01.jpg`, `images/2355_DbqQWmsGpVs_02.jpg`
- `images/2449_Db8aJ56AaJf_01.jpg`
- `images/2472_DcAYVf7GoaA_01.jpg`, `images/2472_DcAYVf7GoaA_02.jpg`
- `images/2475_DcAWsihGtqN_01.jpg`, `images/2475_DcAWsihGtqN_02.jpg`
- `images/2551_DcQw4XvmhZT_01.jpg`, `images/2551_DcQw4XvmhZT_02.jpg`
- `images/2556_DcQElb4Gjy8_01.jpg`, `images/2556_DcQElb4Gjy8_02.jpg`
- `images/2641_DcfQR7cmhdc_01.jpg`, `images/2641_DcfQR7cmhdc_02.jpg`
- `images/2667_Dclm00YGh8L_01.jpg`, `images/2667_Dclm00YGh8L_02.jpg`

### 재현 명령

```bash
jq '[.[] | select((.prompt // "") | gsub("\\s"; "") | length > 0)] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq -r '.[] | select(.id | IN(1838,1843,1846,1852,1857,1858,2048,2145,2219,2233,2236,2240,2339,2346,2349,2355,2449,2472,2475,2551,2556,2641,2667)) | .id as $id | .images[:2][] | [$id,.local_file] | @tsv' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq -r '.[] | select(.id == 2346 or .id == 2349) | [.id,.prompt] | @tsv' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json \
  | jq -r '.presets[] | select((.family // "") == "relationship_blocking") | .id'

git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json \
  | jq -r '.character_mechanism_graph.runtime_nodes[] | select((.family_ids // []) | index("relationship_blocking")) | .id'

git show 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json \
  | jq -r '.. | objects | .id? // empty' \
  | rg 'relationship|reciprocal|companion|harem|rivalry|social_snapshot|shared|target'
```

전수 계수는 위 manifest를 읽는 고정 정규식 스크립트로 수행했고, 원문을 수정하지 않았다. `IN(...)` 명령은 검사한 경로를 재열거하는 용도이며 시각 판정을 자동 재현하지 않는다.

### 외부 1차 근거

- Scaife, M. & Bruner, J. S. (1975), *The capacity for joint visual attention in the infant*, Nature. [DOI](https://doi.org/10.1038/253265a0)
- Setti, F. et al. (2015), *F-Formation Detection: Individuating Free-Standing Conversational Groups in Images*, PLOS ONE. [DOI](https://doi.org/10.1371/journal.pone.0123783)
- Sorokowska, A. et al. (2017), *Preferred Interpersonal Distances: A Global Comparison*, Journal of Cross-Cultural Psychology. [DOI](https://doi.org/10.1177/0022022117698039)

### 변경 경계

- 새로 작성한 파일: 이 보고서 하나
- 변경하지 않은 것: `skills/photo-prompt-image-generator`의 authored asset, generated index, script, test, fixture, runtime behavior
- 생성하지 않은 것: 새 이미지, 렌더 ledger, 픽셀 자격 결과, 사용자 승인

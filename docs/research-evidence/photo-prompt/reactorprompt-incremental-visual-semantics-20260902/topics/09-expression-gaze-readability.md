# Topic 09 — 표정·시선·머리 방향·미세 긴장·썸네일 가독성

status: proposed

## 상태와 결론

- 결정: **proposed**
- 모드: 연구/설계 전용. 런타임 자산, 생성 인덱스, 테스트, 스킬 문서는 수정하지 않았다.
- 대상: ReactorPrompt 증분 코퍼스의 비어 있지 않은 프롬프트 **924개 전수**와, early/middle/late에 분산한 **18개 게시물의 실제 이미지 36장**.
- 픽셀 검토: 36장을 동일한 240×320 타일의 썸네일 조건에서 전수 비교했고, 그중 9개 게시물의 18장은 원본 해상도로 다시 확인했다. 두 해상도 판정은 합치지 않았다.
- 핵심 결론: 현재 데이터에는 맥락에 묶인 표정 의무와 다양한 표정·시선 태그가 이미 많다. 부족한 것은 “감정” 동의어가 아니라 **머리 자세, 눈 방향, 눈꺼풀·눈썹·입·턱의 보이는 동작, 가림, 대상 관계, 출력 크기별 가독성**을 한 소유권 아래 구조화하는 계약이다.
- 정확한 맥락형 표정 요청은 기존 visual-obligation이 계속 소유해야 한다. 일반적인 얼굴 동작은 새 advisory IR이 소유하고, 요청된 얼굴 단서가 실제 출력 크기에서 살아남는지는 조건부 quality refinement가 소유하는 편이 맞다.
- 재사용 가능한 좁은 hard profile은 **머리와 눈의 반대 방향 관계** 하나만 제안한다. “자신감”, “반항적”, “성가신 듯한”, “알 수 없는 표정” 같은 총체적·숨은 상태 라벨은 하드 의무가 아니다.
- 이 연구는 기존 코퍼스의 출처 픽셀을 관찰한 것이다. 제안 후보의 독립 생성 적합성, 런타임 동작, 사용자 판단은 모두 **UNSCORED**다.

## 1. 범위와 안전 경계

### 1.1 동결 입력

- manifest: generated/reactorprompt-export-20260902-incremental/manifest.json
- manifest SHA-256: 0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732
- 원시 gallery SHA-256: 35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f
- 번역 자료 SHA-256: d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586
- 범위: 게시물 1,182개, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, ID 1565–2746.
- 연구 brief가 지정한 기준 스킬 revision: 8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab
- 협업 작업 트리의 동시 변경과 섞이지 않도록 기존 authored source는 git show HEAD:path로 읽었다.
  - photo_prompt_visual_obligations.json: 64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc
  - photo_prompt_tags.json: 5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00
  - photo_prompt_quality_layers.json: 99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f
  - photo_prompt_visual_profile_index.json: 4d674dc00cfa05897f837a7b53410d18766edb8556b1378190523e6e4d1b6626

generated visual-profile index는 파생물로만 대조했다. 의미 소유권의 근거는 authored obligation/tag/quality source다.

### 1.2 관찰 경계

이 보고서는 각 이미지를 서로 독립적인 픽셀 결과로 보았다. 다음은 관찰하거나 추론하지 않았다.

- 사람의 정체성, 동일인 여부, 생체 인식 정보
- 보호 특성, 건강, 매력, 성격, 직업, 민족·국적·소속
- 실제 감정, 숨은 의도, 관계의 진위

기록한 것은 보이는 머리 방향, 눈의 방향, 눈꺼풀·눈썹·입·턱의 모양, 손이나 머리카락·안경·그림자의 가림, 보이는 행동, 대상과의 화면상 관계뿐이다. 프롬프트가 “rebellious”, “annoyed”, “calm and unreadable” 같은 라벨을 쓰더라도 픽셀에서 그 상태를 판정하지 않았다.

## 2. 연구 방법

### 2.1 프롬프트 924개 전수 스캔

모든 비어 있지 않은 본문을 소문자화하고, 표현 라벨과 관찰 가능한 구성 요소를 분리한 정규식 계열로 전수 계수했다. 게시물 수와 중복을 제거한 본문 수를 함께 기록했다.

- expression descriptor: smile, pout, calm, tense, confident, pensive, annoyed 등 얼굴 상태를 서술하는 어휘
- gaze/eyeline: gaze, eye contact, looking toward/away/down/up, side-eye, eyeline 등
- head orientation: front, three-quarter, profile, head turned, head return 등
- local action: brow, eyelid, narrowed/widened eye, lip corner, parted/pressed lip, teeth, jaw, nostril 등
- visibility/occlusion: face dominant, eye visible, hair/hand/glasses/shadow across face 등
- thumbnail/first-read: thumbnail, scroll-stop, first read, small-size 등

이 계수는 문맥 분류기가 아니라 **프롬프트 어휘의 휴리스틱 감사**다. 부정문, 비교문, 다중 패널이 포함될 수 있고, 출현했다고 픽셀 실현을 뜻하지 않는다.

### 2.2 픽셀 표본

- 구간: early 1565–1958, middle 1959–2352, late 2353–2746.
- 각 구간에서 6개 게시물을 골라 총 18개 게시물로 고정했다.
- 각 게시물에서 manifest 순서상 다운로드에 성공한 첫 두 이미지를 사용했다.
- 양성만 모으지 않고 다음 근접 대조를 포함했다.
  - 직접 시선 대 렌즈 밖 시선
  - 머리 회전 대 눈 회전
  - 얼굴이 큰 프레임 대 전신 프레임
  - 한 채널만 보이는 의도적 가림 대 눈 전체를 막는 가림
  - 실제 국소 동작 대 추상 라벨만 강한 문장
  - 얼굴 선명도 대 요청 eyeline의 정확성
- 36장 모두 썸네일에서 검토했다. 1580, 1591, 1650, 1785, 1798, 1897, 2212, 2244, 2273의 18장은 원본 해상도에서도 검토했다.
- 목적 표본이므로 성공률을 4,908장 전체에 외삽하지 않는다. 원본 확대를 하지 않은 18장에 대해서는 미세 눈꺼풀·입꼬리 판정을 썸네일 수준으로 제한했다.

## 3. 프롬프트 증거

### 3.1 축별 출현량

| 휴리스틱 축 | 게시물 | 고유 본문 | 해석 경계 |
|---|---:|---:|---|
| expression descriptor | 650 | 643 | 추상 상태 라벨과 문자 그대로의 표정 동작이 혼재 |
| gaze or eyeline | 561 | 549 | 카메라, 대상, 화면 밖, 아래·위 방향 포함 |
| direct camera gaze | 96 | 92 | 렌즈 접촉만 세며 관계·의도는 세지 않음 |
| off-axis gaze | 66 | 65 | looking away, side-eye, past lens 등 |
| head orientation | 138 | 137 | 정면, 3/4, 프로필, 회전 포함 |
| head tilt or chin | 43 | 43 | pitch와 roll이 혼재할 수 있음 |
| profile or three-quarter | 66 | 65 | 얼굴 방위 문구 |
| lip or mouth action | 25 | 25 | 벌림, 다묾, 입꼬리, 치아 등 |
| brow or lid action | 36 | 35 | 눈썹·눈꺼풀의 국소 동작 |
| jaw, teeth, or nostril action | 10 | 10 | 희소한 하부 얼굴 동작 |
| face or eye visibility | 132 | 130 | 보이게 함, 강조, 부분 가림 포함 |
| thumbnail or first-read | 16 | 16 | 출력 크기나 최초 읽힘의 직접 언급 |
| face occlusion control | 18 | 18 | 머리카락, 손, 안경, 그림자 등 |
| opposed head–eye relation | 22 | 22 | 머리와 눈의 진행 방향이 다른 문구 |

중요한 결합과 누락:

| 결합/누락 | 게시물 |
|---|---:|
| expression + gaze | 422 |
| gaze + head orientation | 103 |
| gaze + lip/mouth action | 19 |
| head orientation + lip/mouth action | 7 |
| face visibility + thumbnail/first-read | 11 |
| occlusion + visibility | 4 |
| direct gaze + off-axis gaze | 4 |
| descriptor가 있으나 gaze/head/local action이 없음 | 194 |

마지막 194개는 핵심 설계 간극이다. 총체적 라벨이 많아도 어떤 눈·입·머리 단서가 보여야 하는지는 비어 있을 수 있다. 이 경우 라벨을 강한 profile로 승격하면 생성기와 평가자가 서로 다른 얼굴 모양을 “성공”으로 셀 위험이 있다.

### 3.2 ID 구간별 분포

| 구간 | 비어 있지 않은 프롬프트 | expression | gaze | direct | off-axis | head | local action union | visibility | thumbnail | occlusion | opposed head–eye |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| early | 382 | 243 | 178 | 32 | 11 | 15 | 8 | 16 | 1 | 2 | 0 |
| middle | 285 | 199 | 204 | 30 | 27 | 47 | 17 | 40 | 3 | 5 | 6 |
| late | 257 | 208 | 179 | 34 | 28 | 76 | 38 | 76 | 12 | 11 | 16 |

후반부로 갈수록 머리 자세, 국소 얼굴 동작, 가림, 썸네일 언어가 더 자주 명시된다. 이는 작성 양식의 변화일 수 있으므로 품질 향상이나 사용 선호의 변화로 해석하지 않는다.

## 4. 픽셀 증거

아래 “정렬”은 프롬프트의 문자 그대로인 보이는 구성 요소와의 정렬이다. 감정·의도 판정이 아니다.

| 구간 / ID | 프롬프트의 관찰 가능 주장 | 두 이미지에서 실제로 보인 것 | 썸네일 / 원본 판정 |
|---|---|---|---|
| early / 1580 | 몸·머리는 비껴가고 눈은 카메라 쪽으로 돌아옴, 한쪽 입꼬리 | 머리/몸과 눈 방향의 반대 관계는 작은 얼굴에서도 읽힘. 한쪽 입꼬리는 중립 또는 약간 벌어진 입과 구분하기 어려움 | 관계 정렬 / 입 동작 불충분 |
| early / 1591 | 직접 시선, 작고 차분한 미소 | 두 장 모두 직접 시선. 01은 작은 미소, 02는 더 중립적이고 약간 벌어진 입 | 시선 정렬 / 입 동작 변이 |
| early / 1650 | 전신 장면에서 직접 시선, pout가 focal point | 직접 시선은 남지만 입 모양은 썸네일에서 거의 중립. 원본에서도 pout를 명확히 분리하기 어려움 | 크기 때문에 주 표정 불충분 |
| early / 1785 | 얼굴 중심, 직접 시선, 중립에 가까운 입 | 얼굴·눈·입의 기하가 선명함. “calm and unreadable”은 별도 픽셀 사건으로 검증할 수 없음 | 구성 요소 정렬 / 총체 라벨 UNSCORED |
| early / 1798 | 손이 관자·볼 근처, 한쪽 눈을 더 좁힘, 입술 벌어짐·치아 | 손-얼굴 접촉, 눈꺼풀 비대칭, 입 벌림이 썸네일과 원본에서 함께 읽힘 | 강한 다중 채널 양성 |
| early / 1897 | 머리카락·그림자로 상부 얼굴을 숨기고 입술·턱을 밝힘 | 눈 방향과 전체 얼굴 동작은 판정 불가. 하부 얼굴 윤곽과 입 채널은 읽힘 | 채널별 가림 양성 |
| middle / 2212 | 머리·눈은 화면 밖, 입술 벌어짐, 얼굴/머리에 동작 흐림 | off-axis 머리·눈과 벌어진 입은 보이지만 두 장 모두 얼굴은 비교적 선명해 요청한 motion blur는 약함 | 방향 정렬 / 타이밍 발산 |
| middle / 2244 | 머리를 뒤로 기울이고 얼굴은 선명, 눈은 카메라에서 벗어남 | 머리 pitch는 분명. 적어도 한 장은 눈이 렌즈 근처를 향해 “away”와 구분이 약하고, 동작 흐림도 약함 | 머리 정렬 / eyeline 불충분 |
| middle / 2273 | 얼굴 중심의 강한 side-eye | 두 장 모두 머리 방향과 분리된 측면 눈 방향이 썸네일·원본에서 유지됨 | 강한 눈 방향 양성 |
| middle / 2283 | 어깨 너머 머리 되돌림, 측면 시선, 작은 미소 | 머리 되돌림과 눈의 측면 관계, 작은 입꼬리 변화가 썸네일에서 읽힘 | 관계 정렬 / 미세 의미는 판정 안 함 |
| middle / 2296 | 고개를 낮추고 렌즈 밖 아래를 봄, 닫힌 입 | 머리 pitch, 아래·측면 눈 방향, 닫힌 입이 함께 읽힘 | 조합 정렬 |
| middle / 2322 | 3/4, 턱 들기, 큰 얼굴 그림자, 시선은 약간 카메라 밖 | 3/4와 턱 들기·그림자는 명확. 한 장의 시선은 렌즈 근처로 보여 “약간 밖”을 분리하기 어려움 | 머리 정렬 / 미세 eyeline 불충분 |
| late / 2541 | 이완된 눈썹, 좁아진 눈, 볼 상승, 작은 미소, 벌어진 입 | 01은 미소 성분이 더 강하고 02는 중립에 가까움. 요청한 모든 성분이 두 장에서 함께 고정되지는 않음 | 채널 공변 불충분 |
| late / 2583 | 70–80도 프로필, 한쪽 보이는 눈은 렌즈로 돌아옴 | 두 장 모두 프로필과 눈의 복귀가 작은 크기에서도 분리됨. 눈이 머리카락에 완전히 가려지지 않음 | 강한 머리–눈 반대 관계 양성 |
| late / 2585 | 선글라스로 눈을 가리고 얼굴·입·포도 행동을 보임 | 안경이 눈 전체를 덮어 gaze는 판정 불가. 입, 얼굴 윤곽, 포도와의 접촉은 남음 | gaze 음성 / 다른 채널 양성 |
| late / 2654 | 머리카락이 눈·볼을 가로지르고 머리는 관찰자 쪽, 시선은 렌즈 근처/밖 | 머리 방향은 읽히지만 가는 머리카락과 작은 눈 영역 때문에 near-lens와 past-lens를 구분하기 어려움 | 가림 근접 대조 |
| late / 2707 | 얼굴 중심, 손에 볼·턱을 받침, 직접 시선, 닫힌 입 | 얼굴-손 접촉, 직접 시선, 닫힌 입이 썸네일에서 즉시 읽힘 | 강한 first-read 양성 |
| late / 2741 | 머리 기울임, 반쯤 내려온 눈꺼풀, 카메라 쪽으로 올려봄, 부드럽게 닫힌 입 | 두 장에서 literal component가 함께 보이며 02가 더 강함 | 다중 채널 정렬 |

### 4.1 프롬프트–픽셀 정렬에서 반복된 패턴

1. **방향 관계는 작은 크기에서도 비교적 강했다.** 1580과 2583의 머리–눈 반대 관계, 2273의 side-eye, 2296의 아래 시선은 개별 “감정” 라벨보다 먼저 읽혔다.
2. **얼굴 크기만으로 미세 입 동작이 보장되지 않았다.** 1650은 프롬프트가 pout를 focal point라 불렀지만 전신 프레임에서 그 동작이 썸네일에 남지 않았다.
3. **선명한 얼굴과 정확한 eyeline은 다른 게이트다.** 2244와 2322는 얼굴·머리 자세가 읽혀도 “카메라에서 약간 벗어남”을 안정적으로 판정하기 어려웠다.
4. **가림은 얼굴 전체 PASS/FAIL이 아니다.** 1897에서는 눈 채널은 막혔지만 입·턱 채널은 의도적으로 살아 있었다. 2585에서는 선글라스가 gaze 평가를 막아도 입·대상 행동은 남았다.
5. **국소 채널은 함께 존재해야 한다.** 2541처럼 눈·볼·입의 여러 동작을 요청했어도 생성 쌍에서 일부만 변하면 총체적 라벨로 이를 덮어서는 안 된다.
6. **추상 라벨은 픽셀 성공 기준이 아니었다.** “rebellious”, “annoyed”, “unreadable”은 보이는 동작을 설명하는 출처 문구일 수 있지만, 그 상태 자체를 이미지에서 판정하지 않았다.

## 5. 외부 메커니즘 근거

- [OpenFace 2.0: Facial Behavior Analysis Toolkit](https://par.nsf.gov/servlets/purl/10099458)은 얼굴 landmark, 머리 자세, 눈 방향, Facial Action Unit을 서로 다른 출력으로 다룬다. 이 보고서는 특정 이미지의 상태를 자동 판정하는 데 이 논문을 쓰지 않고, **head pose / gaze / local facial action을 한 라벨로 합치지 말아야 한다**는 구조적 근거로만 사용한다.
- [Gaze360: Physically Unconstrained Gaze Estimation in the Wild](https://openaccess.thecvf.com/content_ICCV_2019/html/Kellnhofer_Gaze360_Physically_Unconstrained_Gaze_Estimation_in_the_Wild_ICCV_2019_paper.html)은 넓은 머리 자세와 거리에서 gaze를 다루며 추정 불확실성을 별도 출력한다. 이 보고서는 이를 **머리 방향과 눈 방향을 분리하고, 가림·해상도 때문에 방향이 불명확할 때 UNSCORED를 허용해야 한다**는 근거로 사용한다.

외부 자료는 안정적인 관찰 축의 근거다. ReactorPrompt 이미지가 실제 얼굴 분석 시스템으로 측정되었거나, 프롬프트 라벨의 심리적 의미가 인증되었다는 증거가 아니다.

## 6. 기존 authored source와 소유권 대조

### 6.1 기존 visual obligations가 이미 소유하는 의미

| 기존 profile | 기존 소유권 | 이번 제안이 빼앗지 않는 이유 |
|---|---|---|
| achievement_reward_smile | 성공 결과, 대칭적 미소, 결과물 쪽 주의, 성공 뒤 행동·결과 | 일반 smile tag가 아니라 보이는 성공 사건 전체가 계약 |
| affiliative_reassurance_smile | 걱정하는 상대, 절제된 미소, 지원 행동, 상대 반응 | 실제 감정 추론이 아니라 화면 안 상호작용 사슬이 소유 |
| decision_uncertainty_display | 두 선택지, 한 개의 물리적으로 가능한 eyeline/머리·도구 비교, 눈썹·입 긴장, 멈춘 행동, 미해결 상태 | face-only “confused”나 분할 gaze를 이미 음성으로 거부 |
| embarrassment_repair_display | 작은 실수, gaze break/얼굴 단서, 수리 행동, 상대 반응 | 눈을 피하는 얼굴 하나만으로 통과하지 않음 |
| verified_safety_relief | 앞선 위험, 안전 확인, 확인 대상 eyeline, 여러 긴장 완화 채널, 후속 결과 | 단순 이완 얼굴과 구별하는 맥락형 계약 |
| target_directed_seductive_display | 동일한 보이는 성인 대상, 대상 지향 동작, 후속 반응 | 직접 시선·벌어진 입만으로 숨은 의도를 주장하지 않음 |
| playful_flirtation_interaction | 대상·행동·결과가 묶인 상호작용 | 일반적인 미소나 카메라 시선의 소유자가 아님 |
| look_motion_room_direction_relation | gaze/이동 방향 앞의 화면 여유 | 얼굴 방향 자체보다 composition 공간을 소유 |
| intentional_face_occluded_mood_portrait | 정체성 영역의 의도적 가림, 장면·행동이 전달하는 분위기 | 우연한 crop/실패한 focus나 모든 gaze 가독성의 소유자가 아님 |
| primary_secondary_figure_ground_hierarchy | 첫 읽힘의 주·보조 계층 | 일반 계층만 소유하며 얼굴 채널의 정확성은 소유하지 않음 |

따라서 새 “emotion profile” 묶음을 만들 이유가 없다. exact context-bound 요청은 위 프로필로 라우팅하고, 일반 얼굴 동작은 아래 IR에 남긴다.

### 6.2 현재 tag/candidate source의 겹침과 간극

동결 photo_prompt_tags.json은 111개 slot을 가지며 관련 축은 다음과 같다.

| 현재 slot | 엔트리 수 | 재사용할 강점 | 간극 |
|---|---:|---|---|
| expression | 89 | 입·눈의 일부 literal component가 이미 있음 | confident, pensive, skeptical, warm/cold 같은 총체·숨은 상태 라벨이 동작과 혼재 |
| gaze_target | 23 | 카메라, 대상, 손, 물체 같은 target이 비교적 구체적 | avoiding, doubt 같은 의도 단어가 target geometry와 섞임 |
| gaze_engagement | 14 | lens, past-lens, off-frame, object, reflection, returned gaze 등 | 머리 자세와의 물리 관계·불확실성 필드가 없음 |
| body_orientation | 14 | head_shoulder_opposition 같은 방향 후보 | 머리 yaw/pitch/roll, 눈 방향, 어깨 방향의 독립 소유권이 없음 |
| emotional_contradiction | 10 | 서로 다른 보이는 채널을 조합할 가능성 | abstract label끼리의 조합이면 픽셀 게이트가 모호 |
| platform_framing | 11 | crop-safe 얼굴 배치와 thumbnail-safe placement | 얼굴이 프레임에 있다는 것과 눈·입 단서가 읽힌다는 것을 구분하지 않음 |

expression 안의 small_asymmetric_closed_lip_target_smile처럼 “한쪽 입꼬리, 닫힌 입, 대상”을 적는 후보는 좋은 선례다. 반대로 confident_direct_gaze, looking_away_pensive, skeptical_side_eye 같은 이름은 검색 alias로 남길 수 있어도 의미 소유자는 literal component여야 한다.

### 6.3 현재 quality layer

동결 photo_prompt_quality_layers.json의 5개 축은 shot_intent, light_provenance, frame_hierarchy, decisive_moment, environment_consequence다.

- frame_hierarchy / close_focus_priority는 얼굴의 우선순위와 선명도에 재사용할 수 있다.
- decisive_moment는 눈 깜박임 직전, 입술이 막 벌어지는 순간처럼 **요청된 전환 단계**의 타이밍을 보조할 수 있다.
- shot_intent는 왜 얼굴 채널이 주 읽힘인지 설명할 수 있다.
- 그러나 어느 얼굴 채널이 잠겼고, 작은 출력에서 살아남았는지, 눈 가림 때문에 gaze만 UNSCORED인지에 대한 소유자는 없다.
- viral_thumbnail_clarity 같은 후보는 화면 전체의 주제 명료도이지 얼굴 action channel의 정확성 계약이 아니다.

따라서 의미 IR은 candidate layer, exact 관계는 visual obligation, 출력 가독성은 quality refinement가 각각 소유해야 한다.

## 7. 제안: observable components

### 7.1 canonical advisory IR

새 단일 소유 후보를 photo-facial-display/v1로 제안한다. 아래는 설계 필드이며 구현은 하지 않았다.

    {
      "schema": "photo-facial-display/v1",
      "source": {
        "kind": "request_exact|reference_observation|candidate_advisory|authorial_choice",
        "literal_evidence": [],
        "confidence": "high|medium|low",
        "priority": "P0|P1|P2"
      },
      "head_pose": {
        "yaw": "front|three_quarter_left|three_quarter_right|profile_left|profile_right|away|unspecified",
        "pitch": "up|level|down|unspecified",
        "roll": "left|level|right|unspecified",
        "shoulder_relation": "aligned|counter_rotated|independent|unspecified"
      },
      "eye_direction": {
        "mode": "lens|visible_target|off_frame|past_lens|down|up|left|right|unscored",
        "target_id": null,
        "target_visible": false,
        "visible_eye_count": 0,
        "direction_confidence": "high|medium|low|unscored"
      },
      "head_eye_relation": {
        "mode": "aligned|eye_return_against_head|head_return_eyes_elsewhere|independent|unscored",
        "single_plausible_eyeline": true
      },
      "facial_actions": {
        "brow": [],
        "upper_lid": [],
        "lower_lid": [],
        "mouth": [],
        "cheek": [],
        "jaw": [],
        "nostril": []
      },
      "occlusion": [
        {
          "channel": "left_eye|right_eye|brows|mouth|jaw|whole_face",
          "occluder": "hair|hand|glasses|shadow|crop|object",
          "coverage": "partial|full",
          "required_channel_preserved": true
        }
      ],
      "context_binding": {
        "visible_trigger_id": null,
        "target_id": null,
        "action_id": null,
        "visible_consequence_id": null
      },
      "readability": {
        "priority": "primary|supporting|incidental",
        "thumbnail_carriers": [],
        "native_only_channels": [],
        "unscored_channels": []
      },
      "invariants": [],
      "flexible_fields": []
    }

핵심 규칙:

1. head_pose와 eye_direction을 별도 필드로 잠근다. “profile”은 gaze가 아니고 “side-eye”는 머리 profile이 아니다.
2. 대상이 보이면 target_id를 사용하고, 화면 밖이면 단일 방향 벡터와 confidence를 남긴다. 실제 의도는 기록하지 않는다.
3. facial_actions는 해부학적 진단이 아니라 **보이는 상대 변화**만 기록한다. 예: 한쪽 입꼬리 상승, 입술 닫힘/벌어짐, 눈꺼풀 aperture 감소, 눈썹 안쪽 접근.
4. occlusion은 얼굴 전체 boolean이 아니라 채널별로 기록한다.
5. 총체적 의미가 맥락 의무라면 visible trigger → target/result → face action → gaze/attention → hand/body action → immediate consequence 사슬을 기존 profile에 연결한다.
6. 썸네일 carrier는 1–2개의 크고 구별되는 동작만 지정한다. 모든 미세 동작을 썸네일에서 요구하지 않는다.
7. source/provenance/confidence/P0–P2가 없는 검색 발견은 advisory를 넘지 않는다.

### 7.2 좁은 신규 hard profile

profile id 제안: **head_eye_counterorientation_relation**

정확한 요청이 “머리/코축은 한 방향으로 돌아가 있으나, 보이는 눈은 하나의 명시 대상 또는 렌즈로 되돌아온다”와 동등할 때만 활성화한다.

필수 구성 요소:

1. 머리 yaw가 정면이 아닌 방향으로 충분히 읽힌다.
2. 적어도 하나의 가리지 않은 눈에서 iris/sclera 관계가 하나의 target을 향한다.
3. 머리 방향과 눈 방향이 화면에서 서로 구분되고 반대 관계가 first-read에 남는다.
4. 목·어깨 연결과 눈의 방향이 물리적으로 연속적이다.
5. 대상이 카메라가 아니면 visible target 또는 단일 off-frame vector를 지정한다.

혼동 음성:

- 정면 머리 + 직접 카메라 시선
- 머리와 눈이 같은 방향으로 정렬된 profile
- 머리는 정면인데 눈만 옆으로 간 일반 side-eye
- 선글라스·완전한 머리카락·깊은 그림자로 iris 방향을 볼 수 없음
- crop 때문에 코축이나 눈 방향 중 하나가 사라짐
- 서로 다른 두 대상을 동시에 본다는 분할 gaze

1580과 2583은 이 관계의 corpus positive이고, 2273은 eye-only side-eye 근접 대조, 2585는 occlusion 음성이다. 이 사례는 제안의 근거이지 새 profile의 생성 적합성 PASS가 아니다.

## 8. confusion negatives

| 혼동 | 거부 기준 |
|---|---|
| descriptor-only 얼굴 | calm, confident, annoyed, rebellious 같은 라벨만 있고 literal action이 없으면 hard gate로 승격하지 않음 |
| direct gaze = 관계/의도 | 렌즈 방향은 target geometry일 뿐 유혹, 신뢰, 공격성, 친밀감의 증거가 아님 |
| head turned = eyes turned | 코축과 iris 방향을 각각 판정. 하나로 다른 하나를 대체하지 않음 |
| profile = side-eye | profile은 머리 yaw, side-eye는 눈 방향. 둘은 함께 또는 따로 존재할 수 있음 |
| face sharp = eyeline correct | 얼굴 선명도와 렌즈/렌즈 밖/대상 방향은 별도 gate |
| close crop = thumbnail expression | 프레임에서 얼굴이 커도 작은 입꼬리·눈꺼풀 차이가 다운스케일에서 사라질 수 있음 |
| makeup/light = local tension | 아이라인, 속눈썹, 주름 그림자, 립글로스를 눈꺼풀 긴장·입꼬리 상승으로 세지 않음 |
| perspective asymmetry = action asymmetry | 3/4 자세나 한쪽 가림 때문에 커 보이는 눈·입꼬리를 국소 동작으로 자동 판정하지 않음 |
| hair/glasses = mood | 가림은 가림 채널만 설명한다. 숨은 분위기나 의도를 증명하지 않음 |
| endpoint = transition tension | 이미 닫힌 입/고정된 시선만으로 “막 말하려는 순간” 같은 전환을 통과시키지 않음 |
| one channel = composite affect | smile 하나, gaze break 하나로 기존 context-bound profile을 통과시키지 않음 |
| pair consistency = same person | 생성 쌍의 구성 요소 변이만 비교하며 동일인 여부를 추론하지 않음 |

## 9. owning layer와 candidate routing

| 입력 의미 | canonical owner | hard activation | quality 보조 |
|---|---|---|---|
| exact context-bound affect | 기존 visual obligation | 해당 profile의 모든 trigger/target/action/consequence가 잠길 때 | decisive_moment, environment_consequence |
| exact head–eye counterorientation | 신규 head_eye_counterorientation_relation | 문자 그대로의 반대 방향 관계 요청일 때만 | frame_hierarchy |
| generic expression/gaze/head pose | photo-facial-display/v1 advisory IR | 없음 | 요청 priority가 primary일 때만 facial_display_readability |
| 시선 앞의 화면 여유 | 기존 look_motion_room_direction_relation | 구도 문구가 exact일 때 | frame_hierarchy |
| 의도적인 얼굴 정체성 영역 가림 | 기존 intentional_face_occluded_mood_portrait | 기존 exact phrase 계약 | light_provenance, frame_hierarchy |
| 단순 crop-safe 얼굴 배치 | 기존 platform_framing 후보 | 없음 | frame_hierarchy |

### 9.1 조건부 quality refinement

이름 제안: **facial_display_readability**

항상 켜지는 미용 품질 점수가 아니다. photo-facial-display/v1에서 priority가 primary이고 하나 이상의 얼굴 채널이 P0/P1로 잠긴 경우에만 활성화한다.

- head direction과 eye direction의 분리 가능성
- 필요한 iris, lid, brow, mouth, jaw 채널의 가시성
- occluder가 필수 채널을 지우지 않는지
- 요청 출력 크기에서 지정한 carrier가 먼저 읽히는지
- 머리/눈/입/손-얼굴 접촉이 서로 모순 없이 공존하는지

보이는 얼굴 생김새의 매력, 정상성, 건강, “좋은 표정”을 평가하지 않는다.

## 10. thumbnail / native gates

### 10.1 공통 gate

1. exact 요청에서 잠긴 모든 P0 구성 요소가 장면 안에 존재한다.
2. 머리 pose, 눈 방향, 얼굴 action, 대상, 가림의 owner가 서로 충돌하지 않는다.
3. 대상 관계가 의미의 일부라면 target과 즉시 보이는 action/consequence가 함께 존재한다.
4. 판정 불가능한 채널은 0점이 아니라 UNSCORED다. P0 채널이 UNSCORED면 partial_is_fail로 해당 arm을 실패 처리한다.

### 10.2 thumbnail gate

검토 기준은 출력용 다운스케일에서 적용하며, 이번 240×320 타일을 보편적 픽셀 임계값으로 만들지 않는다.

- primary face가 주 장면 요소와 경쟁하지 않고 첫 읽힘에 들어온다.
- 머리 방향과 주 eyeline이 서로 다른 경우 두 방향을 구분할 수 있다.
- 지정한 thumbnail carrier 1–2개가 makeup, shadow, hair, compression과 구분된다.
- contextual profile이면 얼굴만 확대해 읽는 것이 아니라 trigger/target/action/consequence의 최소 관계도 첫 읽힘에 남는다.
- 필수 눈 채널이 완전히 가려지면 gaze는 FAIL 또는 UNSCORED이며, 다른 입·턱 채널의 성공으로 대체하지 않는다.
- 얼굴이 작은 전신 구도에서는 입꼬리·눈꺼풀 같은 native-only micro action을 억지로 PASS시키지 않는다.

### 10.3 native gate

- head yaw/pitch/roll을 어깨·카메라 roll과 분리할 수 있다.
- 보이는 iris 방향이 한 target과 물리적으로 일관되고, 서로 다른 방향으로 찢어지거나 교차하지 않는다.
- 요청된 brow/lid/mouth/cheek/jaw 구성 요소가 같은 프레임에서 함께 존재한다.
- 좌우 비대칭은 자세·가림·조명만으로 설명되는 false positive가 아니다.
- hair/hand/glasses/shadow/crop의 channel별 coverage가 IR과 일치한다.
- 눈·눈꺼풀·입술·치아·턱선이 뒤틀리거나 중복되지 않는다.
- micro tension이 요청되면 닫힘/벌어짐, 압박/이완, 비대칭 같은 실제 국소 기하가 보여야 하며 총체 라벨로 대체하지 않는다.

### 10.4 보류한 수치

얼굴 점유율, iris 최소 픽셀, 입꼬리 변위 같은 보편 수치는 이번 표본만으로 고정하지 않는다. 소스별 크롭과 출력 플랫폼이 달라 과적합 위험이 크다. 구현 전 독립 render arm에서 source-relative threshold를 교정해야 한다.

## 11. regression과 held-out 설계

### 11.1 최소 인과쌍

한 번에 한 축만 바꾸고 seed/reference/composition/나머지 문구를 고정한다.

| pair | 양성 | 근접 음성 | 판정 목적 |
|---|---|---|---|
| A | 직접 렌즈 시선 | 렌즈 바로 옆 past-lens | face sharpness와 eyeline 분리 |
| B | 3/4 머리 + 렌즈로 돌아온 눈 | 머리와 눈이 같은 방향 | head–eye counterorientation |
| C | 정면 머리 + side-eye | profile 머리 + 정렬된 눈 | profile과 side-eye 분리 |
| D | 닫힌 입 + 한쪽 입꼬리 상승 | 대칭적 닫힌 입, 립글로스만 강함 | mouth action과 재질/조명 분리 |
| E | 눈썹 안쪽 접근 + 입술 압박 | 아이메이크업·그림자만 강함 | local tension false positive |
| F | 같은 구성 요소의 얼굴 중심 프레임 | 같은 구성 요소의 전신 프레임 | thumbnail carrier 생존 |
| G | 머리카락이 한쪽 눈만 부분 가림 | 불투명 안경이 두 눈을 전부 가림 | channel별 occlusion/UNSCORED |
| H | 기존 uncertainty profile의 두 선택지·단일 eyeline·paused action | 한 물체만 보는 face-only “confused” | 기존 context owner 회귀 |
| I | 손이 볼·턱을 실제 지지 | 손이 얼굴 가까이에 떠 있음 | face–hand contact와 pose 대체 방지 |

각 arm은 독립 생성하고 다른 arm의 이미지를 입력으로 쓰지 않는다. 실패 수리는 실패한 보이는 관계만 수정한다.

### 11.2 corpus regression anchors

- positive: 1580, 2583 — 머리–눈 반대 방향
- near control: 2273 — 정면/약한 머리 회전에서 eye-only side-eye
- multi-channel positive: 1798, 2741
- thumbnail scale failure: 1650
- occlusion split: 1897, 2585, 2654
- sharp face but eyeline ambiguity: 2244, 2322
- strong first-read contact/action: 2707
- component co-variation check: 2541

이 ID들은 향후 생성 결과의 참조 입력이 아니라 **판정 예시와 회귀 문장 설계용 anchor**다.

### 11.3 held-out

- 한국어·영어의 짧은 literal 요청을 각각 동결한다.
- 훈련/설계 표본에 없던 머리 방향, 대상 위치, 한쪽 눈 가림을 조합한다.
- exact profile 문구를 쓰지 않은 generic portrait를 음성으로 둔다.
- 얼굴이 작지만 head–eye 관계는 큰 경우와, 얼굴은 크지만 micro action이 약한 경우를 교차한다.
- visible target, off-frame target, lens target을 각각 별도 holdout으로 둔다.
- 남은 906개 게시물 중 설계 표본과 ID가 겹치지 않는 사례를 사용하며, 구현자는 성공 사례를 보고 threshold를 사후 조정하지 않는다.

### 11.4 판정 기록

각 arm은 다음을 분리 기록한다.

- request/profile activation과 prompt bytes
- candidate IR/source/provenance/P0–P2
- 생성 요청·이미지·hash lineage
- thumbnail gate
- native gate
- context-bound relation gate
- 채널별 PASS / FAIL / UNSCORED
- user judgment

prompt/static PASS는 pixel PASS가 아니고, pixel PASS는 user acceptance가 아니다. partial은 PASS가 아니다.

## 12. 표본 이미지 경로

각 행의 두 파일을 모두 썸네일 검토했다. 별표 행은 두 파일 모두 원본 해상도로도 확인했다.

| 구간 / ID | 이미지 01 | 이미지 02 |
|---|---|---|
| early / 1580* | generated/reactorprompt-export-20260902-incremental/images/1580_DY02aeqmtgo_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1580_DY02aeqmtgo_02.jpg |
| early / 1591* | generated/reactorprompt-export-20260902-incremental/images/1591_DY11gvrmtgI_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1591_DY11gvrmtgI_02.jpg |
| early / 1650* | generated/reactorprompt-export-20260902-incremental/images/1650_DY9ZkxOmshC_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1650_DY9ZkxOmshC_02.jpg |
| early / 1785* | generated/reactorprompt-export-20260902-incremental/images/1785_DZO_iW7GlGC_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1785_DZO_iW7GlGC_02.jpg |
| early / 1798* | generated/reactorprompt-export-20260902-incremental/images/1798_DZRO8dGGqRH_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1798_DZRO8dGGqRH_02.jpg |
| early / 1897* | generated/reactorprompt-export-20260902-incremental/images/1897_DZsDnRbGvza_01.jpg | generated/reactorprompt-export-20260902-incremental/images/1897_DZsDnRbGvza_02.jpg |
| middle / 2212* | generated/reactorprompt-export-20260902-incremental/images/2212_Da9dP5SGvog_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2212_Da9dP5SGvog_02.jpg |
| middle / 2244* | generated/reactorprompt-export-20260902-incremental/images/2244_DbDCIUSml3P_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2244_DbDCIUSml3P_02.jpg |
| middle / 2273* | generated/reactorprompt-export-20260902-incremental/images/2273_DbK14xomlc2_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2273_DbK14xomlc2_02.jpg |
| middle / 2283 | generated/reactorprompt-export-20260902-incremental/images/2283_DbVoQrhmtq3_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2283_DbVoQrhmtq3_02.jpg |
| middle / 2296 | generated/reactorprompt-export-20260902-incremental/images/2296_DbcvK4WGsb7_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2296_DbcvK4WGsb7_02.jpg |
| middle / 2322 | generated/reactorprompt-export-20260902-incremental/images/2322_DbiaJ10mlbb_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2322_DbiaJ10mlbb_02.jpg |
| late / 2541 | generated/reactorprompt-export-20260902-incremental/images/2541_DcQwsUwmmNB_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2541_DcQwsUwmmNB_02.jpg |
| late / 2583 | generated/reactorprompt-export-20260902-incremental/images/2583_DcYfB0umqav_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2583_DcYfB0umqav_02.jpg |
| late / 2585 | generated/reactorprompt-export-20260902-incremental/images/2585_DcYiSCFmnX1_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2585_DcYiSCFmnX1_02.jpg |
| late / 2654 | generated/reactorprompt-export-20260902-incremental/images/2654_DciZLkTmqFP_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2654_DciZLkTmqFP_02.jpg |
| late / 2707 | generated/reactorprompt-export-20260902-incremental/images/2707_DcqC17IGtsA_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2707_DcqC17IGtsA_02.jpg |
| late / 2741 | generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_01.jpg | generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_02.jpg |

## 13. 재현과 검증 메모

전수 스캔의 모집단은 manifest에서 prompt를 trim했을 때 비어 있지 않은 행으로 만들었다. 중복 본문은 별도로 정규화해 고유 수를 기록했다. 이미지 표본은 manifest의 downloaded image path를 사용했으며, 각 ID에서 첫 두 성공 파일을 고정했다.

검증할 항목:

1. manifest 1,182 / non-empty 924 / unique prompt 904가 재현되는가.
2. 위 36개 이미지 경로가 모두 존재하는가.
3. 표본 ID가 early 6, middle 6, late 6으로 분산되는가.
4. report status가 proposed인가.
5. prompt evidence와 pixel evidence가 별도 절인가.
6. 대상 보고서 외 runtime/index/test/다른 report를 이 작업이 수정하지 않았는가.

## 14. bounded decision

**proposed, not implemented.**

다음 구현 단계가 승인된다면 순서는 다음과 같다.

1. photo-facial-display/v1 advisory IR과 source/provenance/P0–P2 schema를 작성한다.
2. 기존 expression/gaze/body-orientation tag를 새 IR에 매핑하되 추상 라벨은 alias로만 남긴다.
3. 정확한 head–eye 반대 방향 요청만 좁은 visual obligation으로 추가한다.
4. primary face 요청에서만 facial_display_readability quality refinement를 켠다.
5. frozen causal pairs와 held-out set으로 prompt/static을 먼저 감사한다.
6. 독립 생성 arm에서 thumbnail/native/context gate를 각각 채점한다.
7. 부분 정렬은 실패로 남기고 user judgment를 별도 기록한다.

이 보고서 자체는 런타임 적합성, 렌더 성공, 사용자 수용을 증명하지 않는다.

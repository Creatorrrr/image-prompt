# 포즈 용어의 시각 의미·후보팩 데이터 보강 리서치

2026-10-02 · 기준 리비전 `0e5cc0d1968d5cfe83d1b63e9cfa198724ea9463`

## 결론과 산출물의 상태

보강의 중심은 **포즈 이름을 늘리는 일과 함께, 같은 이름이 요구하는 관절·지지·접촉·시점 관계를 명시하는 것**이다. 원문에 등장하는 단어들을 하나의 동의어 풀로 넣으면 `높은 무릎 꿇기 ↔ 뒤꿈치 앉기`, `발끝 뻗기 ↔ 포앵트 지지`, `손끝 접촉 ↔ 턱 지지`, `팔짱 ↔ 상대와 팔짱`이 섞인다. 손·발·상대 인물이 늘어날수록 소유자와 접촉 대상도 의미 데이터의 일부가 되어야 한다.

참조 대화 [포즈 용어 조사](https://chatgpt.com/c/6abf0e48-7010-83ee-8bbf-7764bcfe2150)의 1–17절 표를 **398개 원문 행, 26개 용어군**으로 전사했다. 요가의 11개 묶음 행에 들어 있는 **28개 개별 이름**을 별도 자식 항목으로 풀어 총 **426개 주석 레코드**를 만들었다. 이는 고유한 정식 용어 426개라는 뜻이 아니다. 반복, 반대 값의 묶음, 별칭, 장르명과 촬영 관행이 포함된다. 18절의 분류 축 14개, 조합 예시 6개, 서두의 분류 예시 3개는 용어 수에서 제외했다.

외부 출처는 42개 레코드로 관리한다. 본문을 읽은 항목 34개, 검색 도구가 반환한 해당 발행자 본문을 읽은 항목 7개, 접근 실패로 남긴 참고 단서 1개다. 박물관·무용단·요가 교육기관·포토그래퍼·공식 대회 규정과 날짜가 있는 매체 사용례를 구분했다. 매체의 별칭 사용은 정식 해부학적 정의나 2026년 유행의 증거가 아니다.

작성한 초안은 다음과 같다.

| 산출물 | 규모 | 의미 |
|---|---:|---|
| [용어 카탈로그](keyword-catalog.json) | 398개 원문 행 + 28개 요가 자식 | 각 행의 처리 방향, 현행 문자열 단서, 후보 초안 연결, 확인할 항목 |
| [후보 데이터 초안](candidate-data.proposed.json) | 236개 | 구성요소, 혼동 경계, 소유자, 속성 범위, 관찰 가능성, 출처 |
| [행별 분해 설계](row-decompositions.tsv) | 77개 | 단순 별칭 매칭으로 처리되지 않는 행의 구체적 해석·재사용 대상 |
| [프로파일 초안](visual-profiles.proposed.json) | 51개 | 기존 3개 재검토 + 신규 48개 제안; 모두 원본 픽셀 판정 미검증 |
| [평가 사례 초안](evaluation-cases.proposed.jsonl) | 224개 | 정의 양성·가까운 오답·일부 충족·가림·활성화/범위 사례 |
| [현행 데이터 감사](current-data-audit.json) | 74개 소스 해시 | 확장 병합 기준 수량, 실제 후보, 정책, 재사용 대상 |

후보 236개 중 정의 정리 109개, 기존 프로파일 재사용 3개, 프로젝트 관찰 정의 60개다. 나머지 64개에는 변형 선택, 원본 참고 이미지 조정, 개별 요가 출처 확인, 별칭 또는 동작 단계 확인이 필요하다. 앞의 172개도 렌더 성공으로 승인된 후보를 뜻하지 않는다. 이번 작업은 **리서치와 반영 설계**이며 런타임 자산·인덱스·생성 결과는 변경하지 않았다.

초안의 별칭은 검색 단서다. 전역 동의어 또는 즉시 하드 활성화 목록이 아니다. Barbie feet의 맨발 조건, Chin V의 턱 대상, T-Rex의 손목 이외 팔·손가락 변형, self-covering의 가림 물체처럼 이름별 추가 조건을 `conditional_alias_constraints`에 기록했다. 프로파일 승격 때 기본 구성요소와 이 조건을 함께 조정해야 한다.

## 1. 현재 데이터의 실제 범위

`prompt_generator.load_json()`으로 기본 태그와 등록된 확장을 병합했고, `load_visual_obligation_registry()`로 프로파일 확장을 병합했다. 기본 JSON만 세면 보강량과 중복 여부를 잘못 판단한다.

| 슬롯 | 기본 파일 | 확장 병합 후 | 확인한 보강 문제 |
|---|---:|---:|---|
| `body_pose` | 43 | 86 | 지지 형태·무릎 높이·좌면 위치를 더 세분해야 함 |
| `body_orientation` | 14 | 26 | 몸의 방향, 관절 회전, 머리 방향과 카메라 방향의 분리 |
| `hand_pose` | 21 | 25 | 손 위치 외에 손가락 구성·손바닥 방향·손 개수 필요 |
| `contact_point` | 24 | 44 | 접촉·잡기·겉으로 보이는 지지·가림의 역할 구분 |
| `gaze_target` | 23 | 34 | 대상은 있지만 슬롯 차원 매핑은 빈 배열 |
| `gaze_engagement` | 14 | 17 | 현재 소유 차원은 `expression` |
| `expression` | 89 | 102 | 일반 표정과 특정 눈·입 별칭의 경계 |
| `relational_action` | 37 | 54 | 기본 소유 차원은 `action`; 자세·접촉 효과는 개별 명시 필요 |
| `action` | 516 | 963 | 행동이 많아도 정확한 자세·단계·접촉이 보장되지는 않음 |

기본 프로파일은 333개, 병합 후 전체 프로파일은 1,385개다. 이 전체 수를 포즈 프로파일 수로 부르면 안 된다. 이번 조형 용어의 기존 핵심 프로파일 `contrapposto_weight_shift`, `figura_serpentinata_spiral_pose`, `tribhanga_three_bend_pose`를 확인했으며 새 이름으로 중복 작성할 이유가 없다.

기존 후보를 재사용할 수 있는 예는 `three_quarter_body_turn`, `clean_side_profile_orientation`, `back_view_orientation`, `perched_edge_sit_grounded_support`, `lower_limb_plantarflexed_line`, `propped_elbow_recline_support`다. 9월 연구에서 제안됐던 `single_support_backward_flexed_free_leg`, `fingertip_contact_visible_target_non_support`, `forward_torso_lean_close_crop`도 현재 병합 데이터에 존재한다. 마지막 항목의 현재 슬롯은 **`body_framing`**이므로 옛 연구 문서의 제안 슬롯만 보고 옮기면 안 된다.

반면 관련 슬롯의 `ko/en/aliases/keywords/embedding_text`에서 `arabesque`, `bambi`, `barbie feet`, `finger heart`, `figure-four`, `tall kneeling`, `supine`, `prone`, `gyaru`, `squinch`, `abhaya`, `warrior`, `passé`의 문자열은 발견하지 못했다. 이것은 **명칭 연결의 단서**다. 동일 기하가 다른 문장으로 존재하지 않는다는 증거나 실제 검색 실패율은 아니다.

또한 현행 `pose_framing_system` 라우팅은 `body_pose`, `shot_scale`, `hand_pose`, `body_orientation`, `gaze_engagement`, `camera_direction`, `composition`, `subject_framing` 중심이다. `contact_point`, 상대 관계와 표정의 세부 후보를 추가하기만 해서는 관련 팩에 노출된다고 단정할 수 없다. 반영 시 라우팅·슬롯 적용 가능성·팩 내부 예산을 함께 검증해야 한다.

## 2. 의미 데이터가 가져야 할 관찰 구조

다음은 출처의 표준 스키마가 아니라 이 프로젝트에 맞춘 설계 제안이다. 기존 18절 분류 축을 실행 가능한 관계로 바꾼다.

| 축 | 기록할 값·관계 | 구분해야 할 오류 |
|---|---|---|
| 몸의 기본 지지 | 서기/앉기/무릎/눕기/공중; 골반·발·무릎·손·전완·등의 접촉 | 앉은 골반이 좌면과 떨어짐, 공중 단계에 발이 붙음 |
| 소유자 | `actor_1`, `actor_2`, 몸의 좌우, 반사상 | 상대 손이 자기 손이 됨, 반사상 때문에 인원 수 증가 |
| 관절과 분절 | 관절 이름·굴곡/신전·회전; 흉곽/골반의 서로 다른 방향 | 몸 전체 방향과 관절 회전을 혼동 |
| 접촉 대상·역할 | 몸 부위/소품/지지면/상대; 근접/접촉/그립/겉보기 지지/가림 | 가까운 손을 접촉으로, 손끝 터치를 하중 지지로 판정 |
| 좌표계 | 배우 몸 기준, 지면 기준, 카메라 기준, 이미지 기준 | 왼팔과 화면 왼쪽, 몸 회전과 카메라 롤을 혼동 |
| 관찰 가능성 | 필요한 관절·손가락·지지면·깊이 단서, 가림 원인 | 크롭 밖의 발이나 가려진 팔꿈치를 상상하여 성공 처리 |
| 시간 단계 | 지지/이륙/공중/착지, 잡고 있음/놓음/받음, 선택한 회전 순간 | 정지 사진 한 장으로 전체 동작·속도를 확정 |
| 변경 범위 | `affected_dimensions` + `affected_properties` + 고정된 코어 속성 | 포즈 선택이 의상·신체 비율·관계·성적 톤까지 바꿈 |

해부학적 굴곡·신전이나 족저굴곡은 **어떤 관절의 움직임인가**가 먼저다. 화면에서 팔이 짧게 보이는 것은 카메라와 깊이 관계일 수 있으며 뼈 길이를 바꾸라는 요구가 아니다. [OpenStax의 움직임 분류](https://openstax.org/books/anatomy-and-physiology-2e/pages/9-5-types-of-body-movements), [Adobe의 손·앉기 촬영 설명](https://www.adobe.com/creativecloud/photography/discover/sitting-poses-and-hand-poses.html)

한 사진에서 실제 하중·힘을 측정할 수는 없다. 여기의 지지 판정은 바닥·좌면 접촉, 연결된 팔·다리, 중심 배치와 변형처럼 **보이는 지지 단서가 요청된 자세와 양립하는지**를 확인한다. 가려진 하중 분포나 건강·유연성은 추론하지 않는다. 손 위치와 손목 각도도 따로 기록해야 한다. [Neil van Niekerk의 손목·손 예시](https://neilvn.com/tangents/posing-tip-check-wrists-hands/)

## 3. 26개 용어군별 보강 방향

아래 출처 ID는 [출처 원장](sources.json)의 직접 링크와 연결된다. 후보 수는 여러 군에 함께 연결되는 항목이 있어 서로 더하면 236을 넘는다. 상세한 영문 관찰 조건과 대체 거부 조건은 [후보 원본](candidate-atoms.tsv), 각 원문 행의 연결은 [카탈로그](keyword-catalog.json)에 있다.

| 군 · 원문 행 / 연결 후보 | 핵심 보강과 혼동 경계 | 출처 |
|---|---|---|
| F01 조형 · 16 / 9 | 하중 대항, 축 나선, 세 교대 굴곡, 투영 S/C곡선을 각각 보존. 동세선·제스처 드로잉은 작업/조형 설명; 손짓과 구분 | S01–03, S36–37 |
| F02 서기 · 18 / 10 | 발의 좌우 폭과 앞뒤 간격, 지지 다리와 자유 다리, 골반 이동과 기울기, 발 벽 접촉을 별도 축으로 | S04–05, S07 |
| F03 좌석 · 21 / 15 | 좌면 가장자리/안쪽, 의자 상대 방향, 다리 교차 높이, 골반·팔꿈치·발 지지를 구분. 거꾸로 앉기와 스트래들은 독립 속성 | S05, S07 |
| F04 바닥·무릎 · 16 / 12 | 정강이 교차/양발 허벅지 접촉/W, 높은 무릎/뒤꿈치 앉기/한 무릎, 스쿼트/뒤꿈치 든 스쿼트/네 점 지지 | S04–05, S29 |
| F05 눕기 · 17 / 12 | 등을 댐/앞면을 댐/옆면을 댐이 기본. 전완 지지, 무릎 굴곡, 발 들기, 벽 접촉과 프레임 대각선을 독립 결합 | S06, S29 |
| F06 몸통 · 16 / 11 | 관절·분절 이름을 붙여 굴곡/신전·전인/후인·거상/하강·골반 전후 경사를 분리. 몸매나 카메라 롤로 판정하지 않음 | S04 |
| F07 팔 · 15 / 8 | 팔 개수, 어깨–팔꿈치–손목 사슬, 뒤/위 배치, 반대 팔꿈치/팔 접촉, 엄지만 걸기와 손 전체 넣기 구분 | S07–08 |
| F08 손 · 22 / 19 | 턱/볼/관자/이마/목/쇄골 위치, 손목과 손가락 형상, 포갬/깍지/손끝 맞댐, 터치/그립/지지를 분리 | S07–08 |
| F09 다리·발 · 14 / 12 | 무릎과 발의 간격, 다리 교차 높이, 발 yaw와 발목 굴곡, 발끝/뒤꿈치 접촉, 앞뒤/좌우 스플릿을 분리 | S04, S23 |
| F10 머리·시선 · 14 / 13 | 머리 roll/yaw/pitch/전방 이동, 흉곽 대비 방향, 동공 방향, 눈 틈을 별도 기록. 카메라 높이는 머리 자세가 아님 | S07, S09 |
| F11 표정 · 17 / 10 | 입술 틈·돌출, 치아, 입꼬리 비대칭, 볼·눈썹·눈꺼풀을 관찰 단위로. Smize/Squinch/Fish/Sparrow는 동일 별칭으로 합치지 않음 | S09–10, S16 |
| F12 손·팔 기호 · 22 / 16 | V의 두 손가락, 엄지, 손바닥 방향; 작은 손가락 하트/두 손 하트/팔 하트; 접촉과 얼굴 앞 배치를 분리 | S07, S11 |
| F13 매체 별칭 · 12 / 9 | 이름→문서화된 변형→관찰 기하의 연결을 보존. 역사적 유행 날짜, 사용 공동체, 대체 가능한 변형을 기록 | S11–16, S38 |
| F14 지지물·소품 · 16 / 11 | 벽/난간/탁자의 지지와 컵/책/폰/안경/천의 그립·접촉을 분리. 소품 존재만으로 상호작용 판정 금지 | S07 |
| F15 움직임 · 15 / 9 | 보행 접지, 달리기 공중, 점프, 피벗, 던짐/받음, 머리·천의 반응을 한 순간으로 정의. 블러만으로 성공 금지 | S36 |
| F16 모델·패션 · 16 / 1 | 디지털·이커머스·룩북·뷰티는 촬영 목적. 각진/긴/접힌 조형은 선택한 관절 관계로 구체화; 촬영 매체나 신체 비율 자동 변경 금지 | S18, S36 |
| F17 두 사람·그룹 · 27 / 20 | 인원·상대 방향·손/팔/이마/머리 접촉·업기/안기의 지지·높이/원형 배치를 소유자 관계로. 관계·감정은 별도 요청 | S19 |
| F18 도상 · 12 / 6 | 특정 작품의 Thinker/푸디카/유희좌와 지정 수인을 정의. 누드·오달리스크·드로잉·롱 포즈는 각각 노출/장르/작업/시간 정보 | S03, S20–22 |
| F19 발레 · 15 / 16 | 지지/동작 다리, 발 접촉, 무릎 상태, 관찰자 방향과 학파 변형. 정적 위치와 이동 과정은 별도 | S23–26, S39–42 |
| F20 보깅·공연 · 10 / 2 | 공연 양식과 특정 요소를 구분. 솔로 딥과 파트너 딥, 패션 catwalk와 ballroom catwalk, 정지 freeze와 전체 동작을 분리 | S27 |
| F21 요가 · 11 묶음 / 28 | 개별 이름마다 손/발/무릎/골반/등의 지지와 필수 접촉을 기록. 같은 이름의 다른 자세, 학파와 보조도구 변형을 보존 | S28–31 |
| F22 보디빌딩 · 9 / 8 | NPC의 필수 8종과 quarter-turn 비교를 분리. front/back/side와 팔 위치를 정하고 근육량을 바꾸는 후보가 되지 않게 | S32 |
| F23 장르 · 9 / 0 | Glamour/Pin-up/Boudoir/Gravure 등은 장르·연출 문맥으로 보존. 고유한 뼈대 자세를 정의하지 않으므로 단독 하드 게이트를 만들지 않음 | S06 |
| F24 화보 배치 · 17 / 13 | 무릎·앉기·엎드림·돌아보기·팔·아치의 중립 기하를 재사용. 지지와 시점을 추가하며 의상/노출/성적 톤은 따로 | S06–07 |
| F25 별칭·가림 · 11 / 8 | M/여표는 특정 참조 변형이 필요. 손/팔/시트/로브/옷자락의 소유자·접촉·가림 영역을 기록; 자동 탈의 금지 | S06, S21, S33–34 |
| F26 벌레스크·역할 · 10 / 2 | 부채·장갑과 손의 연결, 가림/드러냄의 선택 순간, 골반 동작과 지지 상태를 분리. 결박 양식/역할명만으로 접촉·의도·지지를 확정하지 않음 | S35, S27 |

## 4. 우선 해결할 혼동 경계

### 조형·지지·좌석

| 비교 | 꼭 남길 차이 | 필요한 가시 영역 |
|---|---|---|
| Contrapposto / S-curve | 전자는 지지/자유 다리와 대항 기울기; 후자는 투영 곡선 | 발·무릎·골반·어깨 |
| Serpentinata / 일반 torso twist | 하체–흉곽–머리/팔의 나선 연결과 깊이 | 상하체 방향·겹침·실루엣 |
| Tribhanga / hip pop | 머리–중간–하체의 세 교대 굴곡 | 세 영역을 동시에 비교할 프레임 |
| Tall kneeling / heel-sitting | 골반이 뒤꿈치에서 높은가, 낮게 앉았는가 | 무릎·정강이·뒤꿈치·골반 |
| Half-kneeling / lunge | 한 무릎의 실제 지면 접촉 | 양다리와 지면 |
| Squat / toe squat / kneeling | 발 또는 무릎 지지, 뒤꿈치 접촉 | 무릎·발·지면 |
| Reverse-chair / chair-straddle | 의자 방향과 두 다리의 좌면 양쪽 배치 | 등받이·좌면·골반·양다리 |
| Knee-over-knee / figure-four / ankle-cross | 허벅지 교차, 발목–반대 허벅지 접촉, 낮은 발목 교차 | 양 무릎·발목·발 |
| Prone / supine / side-lying | 어느 몸통 면이 지지면을 향하는가 | 몸통과 지지면의 방향 |
| Quadruped / plank / downward dog | 무릎 접지 여부, 몸통선과 골반 높이 | 손·무릎·발·몸통 |

조형 용어의 정의는 [Getty의 contrapposto 설명](https://www.getty.edu/news/why-contrapposto-pose-statue-art-David-example-greek-roman/), [National Gallery의 serpentinata 정의](https://www.nationalgallery.org.uk/paintings/glossary/figura-serpentinata), [Met의 도상 설명](https://www.metmuseum.org/essays/recognizing-the-gods)을 기준으로 비교했다. 한 박물관이 특정 문맥에서 비슷하다고 설명해도 프로젝트의 모든 후보를 동의어로 합치는 근거는 되지 않는다.

[Getty AAT 통제어휘](https://www.getty.edu/vow/AATFullDisplay?find=&logic=null&note=&subjectid=300067391)는 contrapposto의 관련 항목에서 serpentinata와 tribhanga를 구별되는 개념으로 명시한다. 세 이름을 하나의 검색 동의어로 묶기보다 연결된 비교 개념으로 유지하는 근거다.

좌석 후보는 “앉기” 외에 **좌면 위치·다리 관계·손 접촉**이 있어야 구별된다. 기존 가장자리 지지 후보는 재사용하고 부족한 교차 형태와 의자 방향을 붙이는 방식이 적절하다. [Adorama의 앉기 예시](https://www.adorama.com/alc/sitting-poses/)

### 손·시선·상대 접촉

`hand_touching_face`의 폭넓은 표현을 유지하되 턱·볼·관자·이마의 정밀 후보를 연결한다. “턱 괴기”에는 턱–손 접촉 외에 손을 받치는 팔꿈치·전완의 지지가 필요하고, 손끝 비지지 접촉은 몸의 하중을 다른 곳에 남긴다. [Adobe의 손 접촉 설명](https://www.adobe.com/creativecloud/photography/discover/sitting-poses-and-hand-poses.html)

시선은 눈의 방향이고, 머리 방향은 얼굴의 yaw/pitch/roll이다. 얼굴이 정면이어도 동공은 옆을 볼 수 있다. 눈을 가리는 손과 눈 방향 프로파일을 함께 요구하면 관찰 충돌이 발생한다. 이를 자동 눈 방향 통과나 자동 손 이동으로 처리하지 말고 고정 코어와 충돌로 기록한다.

두 사람 손잡기는 `actor_1.hand ↔ actor_2.hand`이며, 자기 깍지는 `actor_1.left_hand ↔ actor_1.right_hand`다. 뒤에서 안기, 업기, 가로 안기에는 여러 몸의 지지와 팔 소유를 동시에 판정해야 한다. 손/얼굴의 단순 근접은 실제 접촉을 대신하지 못한다. [Adobe의 두 사람 포즈 설명](https://www.adobe.com/creativecloud/photography/discover/engagement-photo-poses.html)

## 5. 발레·요가·보디빌딩의 정확한 분해

발레는 **관절 형태 + 지지 발 + 관찰자 + 선택 단계**의 조합이다.

- Arabesque는 뒤쪽 동작 다리가 곧고 Attitude는 들어 올린 동작 다리의 무릎이 굽는다. 팔 위치, 높이와 전후 방향의 학파 변형은 따로 선택한다. [Ballet Jörgen A 사전](https://www.jorgendance.ca/ballet-vocabulary/ballet-terms-a/)
- Retiré는 굽힌 다리의 발이 지지 다리 무릎 부근에 있는 위치이고, Passé는 지나가는 동작이다. 일반 수업에서 이름이 혼용될 수 있으므로 사용자의 정의를 우선하며, 한 정지 프레임은 전체 이동 과정의 증거가 아니다. [Jörgen R](https://www.jorgendance.ca/ballet-vocabulary/ballet-terms-r/), [Jörgen P](https://www.jorgendance.ca/ballet-vocabulary/ballet-terms-p/)
- Tendu의 동작 발끝은 바닥 접촉을 유지하는 형태로 게이트를 제안한다. 공개 설명에서 발이 바닥을 떠나는 Glissé와 대비한 해석이며, 수업 영상을 검토한 것은 아니다. Développé는 펼치는 동작의 선택 단계와 종점을 기록한다. [ENB Tendu 설명](https://watch.ballet.org.uk/videos/ballet-vocab-battement-tendu), [ENB Développé 설명](https://watch.ballet.org.uk/step-into-summer-july-beginner/videos/ballet-vocab-developpe)
- Croisé/Effacé는 관찰자에게 교차/열림으로 읽히는 관계다. 몸 각도 하나나 발목 교차만으로 대신하지 않는다. Épaulement와 Port de bras도 학파·위치·팔 변형이 필요하다. [Jörgen E](https://www.jorgendance.ca/ballet-vocabulary/ballet-terms-e/)
- Pointed foot는 발목의 선, demi-pointe는 앞발 볼의 지지, en pointe는 선택한 포앵트 슈즈 끝의 지지다. 신발 존재나 까치발만으로 포앵트를 통과시키지 않는다. Grand jeté는 선택한 공중 단계와 앞뒤 다리 확장을 함께 판정한다. [Atlanta Ballet](https://www.atlantaballet.com/resources/ballet-terms-and-positions)

요가 28종은 아래 11개 묶음으로 정리했다. 표의 기하는 프로젝트의 관찰 정의이며, 세부 지침·건강 효과·개인의 가동 범위에 관한 조언은 포함하지 않는다. 17개 초안은 개별 출처 재확인이 필요하고 그 상태를 데이터에 표시했다.

| 원문 묶음 | 개별 이름 | 판정의 중심 |
|---|---|---|
| 서기·균형 | Tadasana, Vrksasana, Utkatasana | 양발 직립 / 한 발과 반대 다리 접촉 / 좌면 없는 무릎 굴곡 |
| 전사 | Warrior I, II, III | 앞향 몸통·위팔 / 옆향 몸통·수평팔 / 한 발 지지와 들어 올린 뒤 다리 |
| 삼각형·측면 | Trikonasana, Utthita Parsvakonasana | 앞 무릎이 펴진 측굴 / 굽힌 앞 무릎과 옆 몸통–팔의 사선 |
| 다리·팔 균형 | Garudasana, Natarajasana | 교차/감긴 팔·다리 / 한 발 지지와 뒤 발–손 접촉 |
| 바닥 앉기 | Sukhasana, Padmasana, Baddha Konasana | 정강이 교차 / 양발–반대 허벅지 / 발바닥끼리 접촉 |
| 전굴·휴식 | Balasana, Paschimottanasana | 낮은 무릎 지지의 접힌 몸통 / 앉아 앞으로 뻗은 다리와 몸통 |
| 등 젖히기 | Bhujangasana, Ustrasana, Dhanurasana | 엎드린 아래 몸통 / 높은 무릎 지지 / 엎드린 몸과 손–발목 연결 |
| 누운 곡선 | Setu Bandha Sarvangasana, Urdhva Dhanurasana | 어깨/등·발 지지 / 손·발 지지와 들린 몸통 |
| 네 점 지지 | Marjaryasana, Bitilasana, Downward Facing Dog | 손·무릎과 등 위 곡선 / 손·무릎과 등 아래 곡선 / 손·발과 높은 골반 |
| 코어·팔 균형 | Navasana, Plank, Crow, Crane | 좌골 지지 V / 팔·발끝 지지 / 굽힌 팔 / 더 편 팔의 균형 |
| 바로 눕기 | Savasana | 등과 팔다리의 지지; 이름으로 실제 사망·무반응을 추론하지 않음 |

요가의 이름 충돌은 실제 출처 대조에서 확인했다. [Art of Living 목록](https://www.artofliving.org/us-en/yoga/poses/yoga-poses)은 `Gomukhasana`를 Cow Pose로도 부르고, 누운 몸통 비틀기에 `Natarajasana`를 사용한다. 반면 [YogaRenew의 Natarajasana](https://www.yogarenewteachertraining.com/yoga-poses/dancer-pose/)는 선 상태의 다리–손 접촉을 가진 Dancer다. 따라서 `Cow`나 산스크리트 이름만 복사해 전역 별칭으로 삼으면 안 된다. Boat의 좌골 지지 Navasana와 누운 Naukasana 계열도 개별 정의를 대조한 후 분리해야 한다.

Crow/Crane은 [Yoga Journal의 설명](https://www.yogajournal.com/poses/crane-pose/?scope=anon)에서 Kakasana의 굽힌 팔과 Bakasana의 더 편 팔로 구별한다. 이 구별을 선택한 교육 관행으로 기록하고 학파 차이를 남긴다. [측각 설명](https://www.yogajournal.com/practice/extended-side-angle-explainer/?scope=anon)은 뒤 발부터 옆 몸통과 위 팔로 이어지는 사선을 확인하는 데 도움이 된다.

보디빌딩에서는 [NPC 공식 규정](https://npcnewsonline.com/official-bodybuilding-rules/)에 Front/Back Double Biceps, Front/Back Lat Spread, Side Chest, Side Triceps, Abdominals and Thighs, Most Muscular 8종이 열거돼 있다. Quarter turns는 비교 절차와 연결된다. 이름의 존재는 공식 규정으로 확인했지만, 정확한 그립·다리 변형의 게이트에는 종목/부문을 고정한 원본 예시가 추가로 필요하다. 포즈 후보는 근육량·체격 변경 효과를 갖지 않는다.

## 6. 별칭·SNS·성인 화보 용어의 출처와 제한

| 용어 | 확인한 근거와 잠정 기하 | 반영 제한 |
|---|---|---|
| Bambi | [ELLE 2017](https://www.elle.com/beauty/a44609/what-is-bambi-pose/)의 낮은 무릎/뒤꿈치 쪽 앉기 사용 | tall kneeling과 분리; 이름으로 의상·노출을 바꾸지 않음 |
| Barbie feet | [Cosmopolitan 2018](https://www.cosmopolitan.com/tw/fashion/what-to-wear/g22110985/barbie-feet-instagram-style-2018/)의 맨발 뒤꿈치 들기 | 발목·접지 역할과 맨발 조건을 구분; high heels나 pointe와 다름 |
| Gyaru peace | [Vogue Korea 2022](https://www.vogue.co.kr/2022/04/20/%ED%95%AB%ED%95%9C-%EB%B8%8C%EC%9D%B4/)의 카메라 쪽 V 변형 | 손바닥 방향과 단축이 필요; 세대·국적을 포즈 속성으로 넣지 않음 |
| Squinch | [Peter Hurley](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos)의 눈 틈 조절 설명 | 아래/위 눈꺼풀의 보이는 관계를 근접 원본으로 조정; 자신감 추론 금지 |
| Smize | [Glamour 2012](https://www.glamour.com/story/post-24-2012-11)의 eye-smile 사용 | 단일 필수 눈꺼풀 형태가 아직 확정되지 않아 정확 게이트 보류 |
| T-Rex hands | [Huda Beauty 2016](https://hudabeauty.com/us/en_US/blog-hb-love-how-to-slay-in-every-selfie-with-t-rex-hands-33160.html)의 사용자/실무자 표현 | 손목 각도·손가락·얼굴 대비 위치를 참조 변형별로 확인 |
| Migraine/Headache | [Vogue 2018](https://www.vogue.com/article/biggest-beauty-trends-face-tuning-botox-bars-cbd-instagram-cazzie-david)의 이마 손 배치 별칭 | 한 손/두 손·관자/이마를 구분; 실제 질환을 의미하지 않음 |
| Toothache/虫歯 | [ORICON 2020](https://www.oricon.co.jp/news/2166634/full/)의 포즈 이름 사용 | 별칭 존재와 정확 손–볼 기하는 다른 증거; 실제 치통을 추론하지 않음 |
| Fish/Sparrow/Hair twirl | [Glamour 2015](https://www.glamour.com/story/fish-gape-flattering-selfie-tricks)의 사용 | 입술 틈·치아·눈·머리 움직임이 일부 중첩; 단순 동의어화 보류. 머리 회전과 손가락으로 머리카락 감기는 다른 변형 |
| Finger/Hand/Cheek/Cat heart | 원문과 관찰 가능한 손가락/팔 구성으로 초안 작성 | 손 개수·엄지/검지 접촉·뺨 대상 확인. Cheek/Cat은 직접 참조 부족으로 정확 별칭 활성화 보류 |
| 女豹のポーズ | [ORICON 사진 캡션](https://www.oricon.co.jp/news/2145372/photo/1/)의 어휘 사용 | 사진 픽셀을 검토한 것은 아님. 지지점·몸통 곡선·시선의 참조 변형 필요 |
| M字開脚 | [ORICON 2023](https://www.oricon.co.jp/news/2280908/full/)의 어휘 사용 | 좌면/무릎/발 위치가 없으면 wide stance나 split과 구별 불가; 정확 참조 보류 |

Glamour/Boudoir/Gravure/Pin-up 같은 장르와 “무릎 앉기·뒤돌아보기·가림” 같은 기하는 서로 다른 정보다. [Nikon의 부두아 촬영 설명](https://www.nikonusa.com/learn-and-explore/c/ideas-and-inspiration/a-peek-inside-the-boudoir-ready-on-the-set-go-with-cherie-steinberg)을 바탕으로 장르·빛·프레임·스타일링과 몸 배치를 분리했다. 같은 무릎 앉기 기하는 일상 사진과 성인 화보에 모두 연결할 수 있다. 이 연구는 기존 성적 톤/의상 제어값을 바꾸지 않는다.

손·전완·시트·로브 가림은 `owner → covering object → covered target` 관계로 작성한다. `Venus pudica`는 특정 서기 도상이고, 모든 hand bra나 self-covering의 동의어가 아니다. [Met의 특정 푸디카 작품](https://www.metmuseum.org/art/collection/search/329841), [NGA의 Thinker 관찰 설명](https://www.nga.gov/artworks/1005-thinker-le-penseur), [Princeton의 royal ease 작품](https://artmuseum.princeton.edu/art/collections/objects/23888)처럼 작품별 팔·다리 연결을 보존한다.

보깅은 [Smithsonian의 역사 설명](https://nmaahc.si.edu/explore/stories/brief-history-voguing)에 있는 공연·공동체 맥락을 유지하고 특정 정지 포즈로 환원하지 않는다. [Soho School의 Fan Dance](https://sohoschoolofburlesque.co.uk/fan-dance)도 이동·표현·안무를 포함한다. 부채 가림과 장갑 가장자리 그립은 한 프레임의 관계로 초안화했지만, Duckwalk/Spins and dips/Bump and grind/Tease and reveal/결박·서스펜션의 정확 형태에는 공연자·작가의 정의와 선택 단계가 더 필요하다. 로프 체결법이나 수행 지침을 의미 데이터로 가져오지 않는다.

## 7. 검증 설계와 성공 판단

평가는 다음 층을 따로 기록한다.

1. **원장 완전성**: 원문 행을 빠뜨리지 않고 반복·메타데이터·보류 상태까지 기록했는가.
2. **정의·출처 적합성**: 출처가 공식 이름, 사용례, 관찰 기하 중 무엇을 지지하는가. 정의와 프로젝트 게이트를 구분했는가.
3. **런타임 연결**: 올바른 슬롯·활성화·속성 범위·프로파일 관계가 연결됐는가.
4. **팩 노출·선택·채택**: 후보가 노출됐는지, 선택됐는지, 코어와 고정 속성에 맞게 채택됐는지 각각 확인했는가.
5. **프롬프트 표현**: 필요한 관계가 구체적 문장으로 남았는가.
6. **이미지 원본**: 지지·관절·손가락·접촉·소유자가 실제로 보이는가.
7. **사용자 판단**: 사용자가 의도한 포즈와 표현으로 받아들였는가.

데이터 존재, 검색 유사도, 후보 ID 선택, 프롬프트 점검은 6–7층의 성공을 대신하지 않는다. 이번 결과는 1–2층의 연구 및 이후 검증 설계다. 실제 후보팩 생성, 인덱스 재생성, 이미지 호출, 생성 이미지의 원본 픽셀 검토는 수행하지 않았다.

224개 사례는 프로파일별 정의 양성/첫 혼동 대상/필수 요소 하나 누락/필수 영역 하나 가림의 204개와 활성화·범위 20개로 구성했다. 아직 생산 테스트로 연결되거나 이미지로 실행된 사례는 아니다. `arabesque ornament`, `V-neck`, 머리카락의 S곡선, 3/4 길이 크롭, 부정문, 사용자 정의, 한 인물의 반사상, Cow/Dancer 이름 충돌을 별도 포함했다.

픽셀 판정은 큰 배치에 대한 썸네일 검토와 손가락·관절·실제 접촉의 원본 해상도 검토를 나눈다. **모든 필수 게이트가 관찰 가능하며 PASS여야 성공**이다. 일부만 맞으면 `partial_is_fail`이고, 프레임 밖/가림은 `UNOBSERVABLE`로 남겨 성공에서 제외한다. 이는 관찰 불가를 곧바로 해부학 오류나 생성 원인으로 단정한다는 뜻이 아니다. 선택한 행동의 전체 과정은 시퀀스 증거가 있을 때만 평가한다.

## 8. 추가 확인이 필요한 범위

- Cheek/Cat heart와 Smize/Fish gape 등 10개 원문 항목은 정확 이름–기하 연결을 보류했다. 이유와 다음 확인 항목을 카탈로그에 기록했다.
- 요가 17개 후보는 개별 정의 페이지와 명명 관행을 재확인해야 한다. 목록에 이름이 있다는 사실을 개별 동작의 완전한 근거로 올리지 않았다.
- 근접 눈꺼풀, 복잡한 손 하트, ballet viewer 관계, NPC 그립 변형, 도상 작품의 세부와 가로 안기의 지지에는 원본 참고 픽셀의 조정이 필요하다.
- ABT 사전 접근 실패는 Atlanta Ballet/Jörgen으로 대체했다. 원문의 Newsis cheek-heart 사진은 접근 실패로 남겼고 해당 사진을 검증했다고 주장하지 않는다.
- 출처 참고 이미지를 다운로드하거나 픽셀 정답으로 승인하지 않았다. 생성 이미지도 없다. 등록된 후보 수와 게이트 초안 수를 포즈 정확도 향상 수치로 사용할 수 없다.

실제 반영 순서, 파일별 책임과 단계별 통과 기준은 [반영 계획](implementation-plan.md)에 정리했다.

# 40개 시각 문법 보강 제안

2026-10-07 · 연구 및 반영 계획용. 운영 데이터, 생성 프롬프트, 완성 후보팩이 아니다.

기존 ID는 검토할 원본 또는 비교 앵커다. 나열된 ID 전체가 새 표현과 동의어이거나 한꺼번에 채택되어야 한다는 뜻이 아니다. 원문 사전의 우선도나 사용 이력도 생성 효과의 검증값으로 취급하지 않았다.

| ID | 우선도 | 반영 경로 | 제안 |
|---|---|---|---|
| G01 | P1 | authoring_guidance | 매체와 촬영 태도의 일관성 |
| G02 | P0 | relation_bundle_trial | 장르를 서로 다른 시각적 운반체에 배정 |
| G03 | P0 | relation_bundle_trial | 평범한 장소와 낭만적 의상의 대비 |
| G04 | P1 | authoring_guidance | 정서어를 상황과 관찰 단서로 연결 |
| G05 | P0 | enrich_existing | 유지되는 태도와 작게 새는 반응의 동시 대비 |
| G06 | P1 | authoring_guidance | 개성 있는 작은 동작의 사용 범위 |
| G07 | P0 | new_relation_trial | 웃음이 풀리는 중간 표정 |
| G08 | P1 | reuse_and_qualify | 닫힌 입과 눌린 입술의 구별 |
| G09 | P0 | enrich_existing | 관객 위치를 실제 촬영 공간에 연결 |
| G10 | P1 | relation_bundle_trial | 상호 주의의 두 끝점 |
| G11 | P0 | reuse_and_qualify | 지지 다리와 이완 다리의 역할 |
| G12 | P1 | enrich_existing | 동작 사이의 한 단계 선택 |
| G13 | P0 | new_relation_trial | 연필·종이·흔적의 인과 연결 |
| G14 | P0 | new_relation_trial | 가방을 놓는 순간의 지지 이전 |
| G15 | P1 | reuse_and_qualify | 두 손이 같은 컵을 감싸는 구조 |
| G16 | P0 | reuse_and_qualify | 넓은 여백과 피사체 경계 |
| G17 | P0 | reuse_and_qualify | 한 강조점과 저채도 배경의 범위 |
| G18 | P0 | relation_bundle_trial | 얼굴·손·장소 단서의 공동 가독성 |
| G19 | P1 | new_relation_trial | 평면 인쇄물과 입체 전경의 분리 |
| G20 | P1 | authoring_guidance | 요청된 크롭 안에서 접촉을 읽히게 하기 |
| G21 | P1 | enrich_existing | 광원의 모양과 가장자리 반응 |
| G22 | P1 | reuse_and_qualify | 혼합광의 색을 수신 표면에 배정 |
| G23 | P0 | relation_bundle_trial | 직접 플래시와 실내 주변광의 서로 다른 역할 |
| G24 | P0 | semantic_boundary_review | 광학 흔적의 발생 위치 구별 |
| G25 | P1 | enrich_existing | 입자와 움직임 흔적을 핵심 증거와 분리 |
| G26 | P1 | reuse_and_qualify | 검정 바닥과 하이라이트 계조의 독립 제어 |
| G27 | P1 | enrich_existing | 팔레트 이름을 색의 소유자와 면적으로 번역 |
| G28 | P0 | relation_bundle_trial | 같은 빛 아래 서로 다른 재질 반응 |
| G29 | P1 | new_material_trial | 실크 섬유와 faille 직조의 분리 |
| G30 | P1 | new_relation_trial | 리본에서 절개선으로 이어지는 조형 연결 |
| G31 | P1 | reuse_and_qualify | 잔머리의 뿌리·바람·역광 연결 |
| G32 | P1 | enrich_existing | 피부 결·고유색·조명색의 분리 |
| G33 | P1 | enrich_existing | 생활 흔적을 장면의 행동과 묶기 |
| G34 | P0 | new_relation_trial | 물 접촉점과 표면 변화의 원인 연결 |
| G35 | P1 | relation_bundle_trial | 바람에 반응하는 여러 운반체의 정합성 |
| G36 | P1 | enrich_existing | 시간 정지 연출의 정지 구역과 예외 |
| G37 | P0 | new_relation_trial | 흑연선에서 실과 꽃으로 이어지는 입체 경계 |
| G38 | P1 | enrich_existing | 실제 축소 크기와 미니어처처럼 보이는 초점 효과 |
| G39 | P2 | defer_medium_route | 종이 바탕과 수채 워시·흑연의 물성 |
| G40 | P2 | defer_medium_route | 선·명암 덩어리·경계·디테일의 위계 |

## G01 · 매체와 촬영 태도의 일관성

**경로:** authoring_guidance · P1 · 효과 검증 전 trial

**씨앗:** K001 `candid snapshot photograph` / K011 `unpolished phone flash photo` / K015 `intimate personal snapshot` / K018 `watercolor and graphite illustration`

**보여야 할 구성:**

- capture register visible in framing and light
- scene content consistent with the chosen medium

**관계:** the chosen capture register governs the same frame

**소유자:** declared frame and medium

**함께 검토할 변경 범위:** style / camera; content additions require separately open scope

**긍정 요청 예:** 폰 플래시 스냅으로 평소 공간의 한 순간을 담아줘.

**혼동 반례:** 스튜디오 광고 사진인데 모든 불완전 스냅 효과를 자동으로 붙인다.

**기존 원본·비교 앵커:**

- 후보 `slot:medium:street_snapshot` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · street snapshot

**해석·검증 한계:**

- documentary나 RAW는 실제 촬영 이력의 증거가 아니다.
- 순수 수채 요청을 사진 프롬프트로 바꾸지 않는다.

**관련 근거:** [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field) / [Nikon — The Basics of Flash Photography](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G02 · 장르를 서로 다른 시각적 운반체에 배정

**경로:** relation_bundle_trial · P0 · 효과 검증 전 trial

**씨앗:** K022 `ethereal gothic` / K025 `gothic sci-fi aesthetic` / K037 `architectural couture`

**보여야 할 구성:**

- existing architectural forms retain their structure
- a separate existing vista carries the second genre
- material and light join both regions

**관계:** each genre has a separately declared carrier within one scene

**소유자:** existing architecture / vista / garment

**함께 검토할 변경 범위:** concept / setting / style / lighting; all declared carrier changes must be open

**긍정 요청 예:** 무너진 성당 아치 너머로 행성의 지평선이 보이는 장면.

**혼동 반례:** 고딕이라는 말만으로 뿔·왕관·날개와 우주선을 추가한다.

**기존 원본·비교 앵커:**

- 후보 `slot:aesthetic_trend:ethereal_dream_aesthetic` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · ethereal dreamlike styling

**해석·검증 한계:**

- 두 장르라는 숫자는 창작 출발점이며 사용자 요구를 제한하지 않는다.
- ethereal 한 단어를 고딕 구조의 hard trigger로 쓰지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [MoMA — Surrealism and Dreams](https://www.moma.org/collection/terms/surrealism/surrealism-and-dreams)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G03 · 평범한 장소와 낭만적 의상의 대비

**경로:** relation_bundle_trial · P0 · 효과 검증 전 trial

**씨앗:** K036 `romantic clothing in a mundane fluorescent setting` / K419 `ordinary convenience-store fluorescents`

**보여야 할 구성:**

- declared everyday setting remains identifiable
- declared garment retains its distinct construction
- shared illumination touches both

**관계:** the existing garment contrasts with the existing place while sharing one light environment

**소유자:** frozen garment and location

**함께 검토할 변경 범위:** setting / appearance / lighting; cannot introduce an outfit or place through a lighting-only effect

**긍정 요청 예:** 낭만적인 드레스를 입은 인물이 평범한 형광등 편의점에 서 있다.

**혼동 반례:** 빛만 보강하는 후보가 새 드레스와 편의점을 함께 만든다.

**기존 원본·비교 앵커:**

- 후보 `slot:location:old_laundromat_fluorescent` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · old fluorescent laundromat

**해석·검증 한계:**

- 대비가 계층·신분·성격의 사실을 의미하지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Nikon — The Basics of Flash Photography](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography) / [ARRI — Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G04 · 정서어를 상황과 관찰 단서로 연결

**경로:** authoring_guidance · P1 · 효과 검증 전 trial

**씨앗:** K041 `serene melancholy` / K048 `bittersweet nostalgia` / K054 `quiet after tears`

**보여야 할 구성:**

- request-led quiet or active bodily state
- one scene-bound trace or directed attention
- space and light serving the same moment

**관계:** context connects the selected affect reading to visible scene evidence

**소유자:** frozen actor and established circumstances

**함께 검토할 변경 범위:** expression / pose / composition / lighting only where open

**긍정 요청 예:** 울음이 지난 뒤 조용히 창가에 앉아 있는 여운.

**혼동 반례:** 푸른 색보정만으로 우울증이나 실제 슬픔을 판정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:mood:domestic_melancholy` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · domestic melancholy

**해석·검증 한계:**

- 정서를 증명하는 얼굴 모양 한 가지를 정의하지 않는다.
- 눈물·비·소품을 모든 우울 요청에 기본 삽입하지 않는다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G05 · 유지되는 태도와 작게 새는 반응의 동시 대비

**경로:** enrich_existing · P0 · 효과 검증 전 trial

**씨앗:** K065 `curiosity beneath composure` / K066 `embarrassment beneath defiance` / K068 `a smile she is trying not to show`

**보여야 할 구성:**

- one declared baseline posture remains
- one local facial or gaze change stays small
- same actor owns both configurations

**관계:** the same actor retains one attitude while a separate local channel changes

**소유자:** main actor; counterpart only if established

**함께 검토할 변경 범위:** expression / pose / relationship; may not create a counterpart or relationship

**긍정 요청 예:** 평정은 유지하지만 입술을 누르고 옆으로 시선이 새는 순간.

**혼동 반례:** 작은 옆눈질만으로 츤데레나 사랑을 확정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:expression:jaw_set_embarrassment` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · jaw-set embarrassment
- 후보 `slot:intent_state:guarded_royal_composure` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · guarded royal composure

**해석·검증 한계:**

- character_response는 해당 요청 의미가 있을 때만 사용한다.
- tsundere·kuudere 그래프의 존재가 현재 요청을 재분류하지 않는다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G06 · 개성 있는 작은 동작의 사용 범위

**경로:** authoring_guidance · P1 · 효과 검증 전 trial

**씨앗:** K074 `presence rather than overt beauty` / K079 `one specific person, not a generic idealized model` / K080 `a habitual gesture caught unnoticed`

**보여야 할 구성:**

- one specific visible gesture
- gesture connected to a current object or task

**관계:** a present gesture gives particularity without inventing a biography

**소유자:** declared actor

**함께 검토할 변경 범위:** action / pose; preserve appearance locks

**긍정 요청 예:** 생각에 잠긴 채 책 모서리를 엄지로 가만히 잡고 있는 모습.

**혼동 반례:** 한 장의 손동작으로 오랜 습관·지능·성격을 사실로 저장한다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- habitual은 사용자가 설정한 연출 맥락일 수 있다.
- 이미지 검증은 현재 손과 대상의 관계까지만 한다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G07 · 웃음이 풀리는 중간 표정

**경로:** new_relation_trial · P0 · 효과 검증 전 trial

**씨앗:** K089 `eyes naturally closed from laughing` / K090 `a real uncontrollable laugh` / K100 `mouth at rest after a brief laugh`

**보여야 할 구성:**

- mouth has relaxed from its widest laugh
- eye region retains a smile-like configuration
- shoulders or hands retain a scene-compatible residual gesture

**관계:** local face channels occupy different visible relaxation states in one actor

**소유자:** same actor face and body

**함께 검토할 변경 범위:** expression / pose; prior event and timing remain interpretation

**긍정 요청 예:** 웃음이 잦아들며 입은 풀렸지만 눈가에는 웃음이 남아 있다.

**혼동 반례:** 단순히 눈을 감은 명상 표정을 웃음 직후의 증거로 채택한다.

**기존 원본·비교 앵커:**

- 후보 `slot:expression:candid_laugh` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · a candid laugh
- 후보 `slot:expression:pv_eyes_closed` · [photo_prompt_pose_vocabulary_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json) · both eyelid openings close; both eye regions remain visible; mouth expression is independently selected

**해석·검증 한계:**

- 실제 시간차나 웃음 원인을 한 장에서 입증하지 않는다.
- 새 hard alias로 웃는 얼굴 일반을 잡지 않는다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G08 · 닫힌 입과 눌린 입술의 구별

**경로:** reuse_and_qualify · P1 · 효과 검증 전 trial

**씨앗:** K084 `softly parted lips` / K085 `neutral mouth corners` / K097 `lips pressed closed`

**보여야 할 구성:**

- upper and lower lip edges meet
- lip margins visibly compress along the closed seam

**관계:** both margins press against each other on the same face

**소유자:** declared actor lips

**함께 검토할 변경 범위:** expression / face.expression

**긍정 요청 예:** 윗입술과 아랫입술을 꾹 눌러 닫은 표정.

**혼동 반례:** 그냥 다문 입이나 앞으로 내민 입술을 압박된 입술과 동의어로 등록한다.

**기존 원본·비교 앵커:**

- 후보 `slot:expression:ae_lip_press` · [photo_prompt_acting_expression_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_acting_expression_extension.json) · upper and lower lips meet along a fully closed seam; the lip margins look compressed together
- 프로필 `ae_profile_lip_press` · [photo_prompt_visual_obligations_acting_expression.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_acting_expression.json)

**해석·검증 한계:**

- 닫힘만 보이는 표현에는 압박 hard duty를 추가하지 않는다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G09 · 관객 위치를 실제 촬영 공간에 연결

**경로:** enrich_existing · P0 · 효과 검증 전 trial

**씨앗:** K108 `photographed by a friend sitting across from her` / K109 `conversational distance` / K120 `the camera occupies a meaningful position`

**보여야 할 구성:**

- viewpoint has a stated location relative to the actor
- distance and crop retain the current interaction
- gaze direction agrees with the viewpoint or off-frame target

**관계:** camera position belongs to the declared interaction geometry

**소유자:** camera / actor / established target

**함께 검토할 변경 범위:** camera / composition / relationship; each affected relation must be open

**긍정 요청 예:** 맞은편에 앉은 사람이 찍은 듯한 대화 거리의 초상.

**혼동 반례:** 카메라 거리만으로 실제 친구 관계나 동의를 사실로 판정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:capture_context:off_camera_companion_everyday_capture` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · nearby off-camera companion viewpoint during one adult subject's concrete everyday task
- 후보 `slot:viewer_position:viewer_as_confidant` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · viewer leaned in as a trusted confidant
- 프로필 `companion_viewpoint_everyday_candid` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- viewer role는 연출 맥락이다.
- 친구 시점 후보 때문에 두 번째 인물을 화면에 추가하지 않는다.

**관련 근거:** [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field) / [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G10 · 상호 주의의 두 끝점

**경로:** relation_bundle_trial · P1 · 효과 검증 전 trial

**씨앗:** K111 `attention fixed on someone outside the frame` / K112 `gaze following the fingertip` / K118 `mutual attention without a posed smile`

**보여야 할 구성:**

- each established participant has a readable gaze or orientation
- one declared shared target or reciprocal target is identifiable
- attention endpoints remain distinct

**관계:** each participant directs attention toward the declared counterpart or shared target

**소유자:** two established actors or actor and established object

**함께 검토할 변경 범위:** gaze / relationship / pose; cannot increase subject count

**긍정 요청 예:** 두 사람이 테이블 위 같은 편지를 바라보며 잠시 말이 없다.

**혼동 반례:** 평범한 공동 주의를 검색 결과의 돌봄·성취·종교 의식으로 바꾼다.

**기존 원본·비교 앵커:**

- 후보 `slot:relational_action:two_people_sitting_without_words` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · two people sitting face to face without words

**해석·검증 한계:**

- 상호 주의가 호감이나 애정의 진위를 증명하지 않는다.

**관련 근거:** [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G11 · 지지 다리와 이완 다리의 역할

**경로:** reuse_and_qualify · P0 · 효과 검증 전 trial

**씨앗:** K128 `weight distributed naturally onto one leg` / K136 `shoulders level above an asymmetrical stance` / K139 `a readable support leg`

**보여야 할 구성:**

- one leg has the principal support contact
- the other leg has a different relaxed or light-contact role
- pelvis and torso connect above that support

**관계:** body configuration responds to the declared support leg

**소유자:** same actor body and floor

**함께 검토할 변경 범위:** pose / body.support_and_configuration; camera changes need separate open scope

**긍정 요청 예:** 한 다리에 체중을 싣고 다른 다리는 힘을 빼고 선 모습.

**혼동 반례:** 모든 한쪽 다리 지지를 전신 크롭·정해진 골반각의 contrapposto로 강제한다.

**기존 원본·비교 앵커:**

- 후보 `slot:body_pose:pv_single_support` · [photo_prompt_pose_vocabulary_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_pose_vocabulary_extension.json) · one planted leg supplies the principal visible support; the free leg has a different relaxed or lightly contacting role; the pelvis and torso remain connected over the support base
- 후보 `slot:body_pose:contrapposto_full_body` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · full-body contrapposto with one loaded support leg, one relaxed free leg, and opposed pelvis-shoulder tilt
- 프로필 `contrapposto_weight_shift` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- 단순 지지 관계와 고전 contrapposto의 전체 구성을 구별한다.

**관련 근거:** [The Met — Rodin and contrapposto](https://www.metmuseum.org/art/collection/search/207693)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G12 · 동작 사이의 한 단계 선택

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K140 `a pause between two movements` / K156 `a half-finished gesture` / K157 `just after turning toward a sound`

**보여야 할 구성:**

- one action phase is chosen
- contact or remaining gap matches that phase
- any residual trace is physically compatible

**관계:** the present actor-target relation agrees with one selected phase

**소유자:** declared actor and target

**함께 검토할 변경 범위:** action / pose / relationship; complete simultaneous changes reviewed together

**긍정 요청 예:** 손이 대상에 닿기 바로 전의 작은 틈을 남겨줘.

**혼동 반례:** 접촉 전의 틈과 완전한 접촉과 놓은 뒤의 궤적을 동시에 의무화한다.

**기존 원본·비교 앵커:**

- 후보 `slot:narrative_phase:precontact_readiness_visible_gap` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · pre-contact readiness with an explicit visible gap between actor and target
- 후보 `slot:narrative_phase:locomotion_counterturn_midphase` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · mid-locomotion counterturn with travel direction and torso rotation simultaneously readable
- 후보 `slot:narrative_phase:settling_aftereffect_trace_phase` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · settling aftereffect phase with a visible residual trace and diminishing motion

**해석·검증 한계:**

- 단계 라벨이 이전·다음 사건을 픽셀로 입증하지 않는다.

**관련 근거:** [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G13 · 연필·종이·흔적의 인과 연결

**경로:** new_relation_trial · P0 · 효과 검증 전 trial

**씨앗:** K146 `a pencil touching the page` / K405 `annotated research papers`

**보여야 할 구성:**

- held pencil tip contacts the declared paper
- support keeps the page and tool relation plausible
- a local mark begins at the contact region

**관계:** the held tool contacts one supported page and leaves a compatible local trace

**소유자:** actor hand / pencil / paper

**함께 검토할 변경 범위:** action / pose / setting / text only if requested; do not add legible words

**긍정 요청 예:** 연필 끝이 종이에 닿아 짧은 선을 막 긋는 순간.

**혼동 반례:** 연필 눈썹이나 종이를 잡는 손을 연필의 종이 접촉과 같은 후보로 취급한다.

**기존 원본·비교 앵커:**

- 후보 `slot:narrative_phase:tool_contact_active_process_phase` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · active process phase with coherent tool-target contact and an immediate trace
- 후보 `slot:hand_pose:ia_page_hold` · [photo_prompt_intellectual_activity_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_intellectual_activity_extension.json) · palm or thumb contacts a declared page margin; page remains attached to the open book; book rests on a stated support; requested passage remains unobscured

**해석·검증 한계:**

- ia_page_hold는 종이 지지 비교 대상이며 연필 접촉과 동의어가 아니다.

**관련 근거:** [The Met — Graphite](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-graphite) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G14 · 가방을 놓는 순간의 지지 이전

**경로:** new_relation_trial · P0 · 효과 검증 전 trial

**씨앗:** K152 `the weight of a bag leaving her hand` / K156 `a half-finished gesture`

**보여야 할 구성:**

- hand and handle relation shows release
- bag has a declared continuing path or new support
- arm and shoulder remain connected to the releasing actor

**관계:** the bag support changes from the hand toward a visible path or established surface

**소유자:** actor hand / bag / established support

**함께 검토할 변경 범위:** action / pose / setting; no new destination or prop through pose-only adoption

**긍정 요청 예:** 가방을 바닥에 내려놓으며 손이 손잡이에서 떨어지는 순간.

**혼동 반례:** 떠 있는 가방과 손의 분리를 해부학적 연결 없이 성공 처리한다.

**기존 원본·비교 앵커:**

- 후보 `slot:narrative_phase:postcontact_release_continuing_trajectory` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · post-contact release with a continuing actor or object trajectory

**해석·검증 한계:**

- 무게 감소나 피로·안도의 감정은 연출 해석으로 남긴다.

**관련 근거:** [The Met — Rodin and contrapposto](https://www.metmuseum.org/art/collection/search/207693) / [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G15 · 두 손이 같은 컵을 감싸는 구조

**경로:** reuse_and_qualify · P1 · 효과 검증 전 trial

**씨앗:** K143 `holding a warm teacup` / K145 `both hands wrapped around a cup` / K160 `contact shadows at the fingers`

**보여야 할 구성:**

- two hands belong to one declared actor
- both hands contact one cup body
- wrists continue into the same actor arms

**관계:** both owned hands wrap around the same cup

**소유자:** actor hands and cup

**함께 검토할 변경 범위:** pose / contact; steam and warmth require separate established meaning

**긍정 요청 예:** 양손으로 하나의 컵을 감싼 모습.

**혼동 반례:** 증기 없는 컵 잡기 요청에 뜨거운 음료·추위·감정까지 자동으로 강제한다.

**기존 원본·비교 앵커:**

- 후보 `slot:contact_point:cv_two_hand_cup` · [photo_prompt_cute_visual_forms_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_cute_visual_forms_extension.json) · both of the actor's hands curve around the same cup body; fingers from each hand visibly contact that cup surface; both wrists connect the cradling hands to the same actor
- 후보 `slot:action:ctx_warm_cup_hold` · [photo_prompt_contextual_appeal_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_contextual_appeal_extension.json) · both hands surround a cup with a faint visible wisp of steam
- 프로필 `cv_profile_two_hand_cup` · [photo_prompt_visual_obligations_cute_visual_forms.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_cute_visual_forms.json)

**해석·검증 한계:**

- 온기·냄새·컵의 실제 온도는 손 접촉만으로 증명하지 않는다.

**관련 근거:** [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G16 · 넓은 여백과 피사체 경계

**경로:** reuse_and_qualify · P0 · 효과 검증 전 trial

**씨앗:** K161 `large negative space` / K163 `dark lateral margins` / K173 `do not make the subject fill the entire frame`

**보여야 할 구성:**

- one contiguous low-detail field
- subject contour separates from that field
- requested surroundings remain present where needed

**관계:** a bounded empty or quiet field supports the subject without erasing required context

**소유자:** frame / subject contour / background

**함께 검토할 변경 범위:** composition / layout; crop changes require camera scope

**긍정 요청 예:** 인물 옆에 넓고 단순한 여백을 남기되 장소가 읽히게 해줘.

**혼동 반례:** 일반 배경 여백을 허벅지나 팔 안쪽의 몸으로 둘러싸인 틈 프로필로 활성화한다.

**기존 원본·비교 앵커:**

- 후보 `slot:composition:subject_field_negative_space_relation` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · clear subject-to-field relation using one large low-detail negative-space region

**해석·검증 한계:**

- negative space 일반과 body-bounded negative space를 구별한다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G17 · 한 강조점과 저채도 배경의 범위

**경로:** reuse_and_qualify · P0 · 효과 검증 전 trial

**씨앗:** K177 `one signature accent` / K294 `one saturated accent in a muted field` / K302 `black × ivory × a single scarlet accent`

**보여야 할 구성:**

- declared focal owner carries stronger chroma
- surrounding field retains quieter distinct colors
- accent extent and multiplicity are bounded

**관계:** one declared accent remains separate from its quieter field

**소유자:** named accent owner and bounded color scope

**함께 검토할 변경 범위:** color / surface.local_color; no new red objects or red lighting

**긍정 요청 예:** 저채도 공간에서 한 개의 붉은 리본만 강조해줘.

**혼동 반례:** 붉은 리본에 붉은 꽃·귀걸이·램프까지 더해도 single accent라고 처리한다.

**기존 원본·비교 앵커:**

- 후보 `slot:color:cr_candidate_vivid_on_muted` · [photo_prompt_color_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_color_relations_extension.json) · the named focal region has visibly stronger chroma than its surrounding field; the surrounding field retains faint readable hues and separate material tones
- 프로필 `cr_vivid_on_muted` · [photo_prompt_visual_obligations_color_relations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_color_relations.json)
- 프로필 `cr_achromatic_accent` · [photo_prompt_visual_obligations_color_relations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_color_relations.json)

**해석·검증 한계:**

- muted는 achromatic과 다르다.
- 빛이나 반사 속 같은 강조색을 독립 개체 개수와 구분한다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [Huang et al. — T2I-CompBench++ (v3, 2025)](https://arxiv.org/abs/2307.06350v3)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G18 · 얼굴·손·장소 단서의 공동 가독성

**경로:** relation_bundle_trial · P0 · 효과 검증 전 trial

**씨앗:** K187 `face, hands, and one setting cue remain readable` / K188 `moderate depth of field` / K198 `subject sharpest, background still recognizable`

**보여야 할 구성:**

- face retains required expression detail
- hand-target contact remains interpretable
- one established setting cue remains recognizable

**관계:** focus and depth preserve all declared evidence regions together

**소유자:** camera focus / face / hand-target / setting cue

**함께 검토할 변경 범위:** camera / optical.focus; pose or prop movement needs separately open effect

**긍정 요청 예:** 얼굴과 컵을 감싼 손, 기차 창틀이 함께 읽히는 초상.

**혼동 반례:** 극도로 얕은 심도가 손 접촉이나 기차 단서를 지워도 배경 흐림만으로 개선이라 한다.

**기존 원본·비교 앵커:**

- 후보 `slot:focus:rb_readable_environment_focus_candidate` · [photo_prompt_realistic_background_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_realistic_background_extension.json) · The selected subject plane remains crisp; the middle-distance environmental forms remain recognizable; the farther background loses fine detail consistently with its depth.
- 프로필 `rb_readable_environment_focus` · [photo_prompt_visual_obligations_realistic_background.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_realistic_background.json)

**해석·검증 한계:**

- 세 지역을 항상 선명하게 만드는 기본값이 아니다.
- 요청된 가림·흐림을 임의로 해제하지 않는다.

**관련 근거:** [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field) / [Hu et al. — TIFA](https://arxiv.org/abs/2303.11897) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G19 · 평면 인쇄물과 입체 전경의 분리

**경로:** new_relation_trial · P1 · 효과 검증 전 trial

**씨앗:** K020 `photographic subject against a printed illustration` / K200 `flat printed background, dimensional foreground` / K458 `real subject × oversized illustrated backdrop`

**보여야 할 구성:**

- background mark lies on a visible flat support
- foreground form has occlusion or cast-shadow depth
- shared light does not erase the plane distinction

**관계:** dimensional foreground occupies space in front of the declared flat printed support

**소유자:** printed support and established foreground

**함께 검토할 변경 범위:** composition / material / lighting; subject identity remains locked

**긍정 요청 예:** 실제 인물 앞뒤의 인쇄 포스터가 종이 평면으로 읽히게 해줘.

**혼동 반례:** 배경 그림의 인물을 새 실제 인물로 늘리거나 전경을 납작한 인쇄물로 바꾼다.

**기존 원본·비교 앵커:**

- 후보 `slot:surface_material:pe_pencil_print` · [photo_prompt_editing_effects_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json) · pencil linework on a depicted paper artifact

**해석·검증 한계:**

- 보이는 층 구분과 실제 촬영·합성 이력을 구별한다.

**관련 근거:** [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [PBRT 4e — Diffuse Reflection](https://www.pbr-book.org/4ed/Reflection_Models/Diffuse_Reflection) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G20 · 요청된 크롭 안에서 접촉을 읽히게 하기

**경로:** authoring_guidance · P1 · 효과 검증 전 trial

**씨앗:** K219 `the contact point remains within the frame` / K220 `no invented anatomy outside the crop` / K215 `a close foreground hand as a scale anchor`

**보여야 할 구성:**

- requested frame boundary retained
- consequential contact lies in view when required
- visible articulation connects the owned parts

**관계:** crop preserves evidence for the requested contact without inventing off-frame anatomy

**소유자:** camera crop and acting body chain

**함께 검토할 변경 범위:** camera / composition; cannot widen a locked crop

**긍정 요청 예:** 주어진 허리 위 크롭에서 컵과 두 손이 모두 보이게 해줘.

**혼동 반례:** 검증하기 쉽다는 이유로 고정된 클로즈업을 전신으로 넓힌다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- 프레임 밖 지지는 설명할 수 있으나 픽셀 통과 증거로 쓰지 않는다.

**관련 근거:** [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G21 · 광원의 모양과 가장자리 반응

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K228 `narrow silver-white hair rim` / K235 `a narrow vertical golden backlight` / K236 `light catching only the fabric edges`

**보여야 할 구성:**

- declared narrow source occupies a stated region
- subject occludes the source where they overlap
- selected hair or cloth edges respond to that source

**관계:** source shape, overlap and edge response share a coherent spatial arrangement

**소유자:** light aperture / subject / named edge

**함께 검토할 변경 범위:** lighting / source.shape / surface.illumination; no new architecture through light-only change

**긍정 요청 예:** 뒤의 좁은 금빛 수직 광원이 머리 가장자리만 잡는다.

**혼동 반례:** 수직 틈새 광원을 따뜻한 낮은 해와 동의어로 등록한다.

**기존 원본·비교 앵커:**

- 후보 `slot:light_shape:egr_occluded_vertical_emissive_slit` · [photo_prompt_ethereal_gothic_scene_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_ethereal_gothic_scene_extension.json) · a narrow vertically extended luminous aperture lies behind the subject; the subject silhouette occludes the aperture wherever they overlap; the remaining visible aperture segments belong to the same aligned opening

**해석·검증 한계:**

- 따뜻한 색만으로 역광이나 실제 광원 모양을 입증하지 않는다.

**관련 근거:** [Nikon — The Basics of Flash Photography](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography) / [ARRI — Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G22 · 혼합광의 색을 수신 표면에 배정

**경로:** reuse_and_qualify · P1 · 효과 검증 전 trial

**씨앗:** K227 `warm reflected light on cool skin` / K248 `cool blue window light × warm amber lamps` / K298 `slightly uneven white balance`

**보여야 할 구성:**

- at least two declared light source regions
- each source illuminates a distinct receiver region
- shared surfaces have compatible transitions

**관계:** cool and warm light zones follow their declared sources and receivers

**소유자:** existing sources and illuminated surfaces

**함께 검토할 변경 범위:** lighting / surface.illumination; grading-only is a separate operation

**긍정 요청 예:** 창 쪽 소매는 차갑고 램프 쪽 탁자는 따뜻하게 빛난다.

**혼동 반례:** 전면 파랑-주황 색보정만으로 서로 다른 광원 관계를 충족한다.

**기존 원본·비교 앵커:**

- 프로필 `mixed_illuminant_white_balance_relation` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)
- 프로필 `rb_mixed_source_zones` · [photo_prompt_visual_obligations_realistic_background.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_realistic_background.json)

**해석·검증 한계:**

- 피부의 고유색을 조명색 변화와 혼동하지 않는다.

**관련 근거:** [Nikon — The Basics of Flash Photography](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography) / [ARRI — Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf) / [PBRT — Surface Reflection](https://www.pbr-book.org/3ed-2018/Color_and_Radiometry/Surface_Reflection)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G23 · 직접 플래시와 실내 주변광의 서로 다른 역할

**경로:** relation_bundle_trial · P0 · 효과 검증 전 trial

**씨앗:** K241 `direct on-camera smartphone flash` / K242 `warm tungsten light mixed with flash` / K243 `underexposed background behind a flash-lit subject`

**보여야 할 구성:**

- near actor has frontal flash response
- established practical lights retain warm background regions
- distance separates near exposure from the background

**관계:** flash illuminates the near actor while existing practicals preserve ambient context

**소유자:** flash / actor / established interior lights

**함께 검토할 변경 범위:** lighting / camera; cannot change candid event or create studio setup

**긍정 요청 예:** 따뜻한 실내등이 남아 있는 밤의 정면 플래시 스냅.

**혼동 반례:** 완벽한 다중 스튜디오광을 같은 장면에 기본으로 추가한다.

**기존 원본·비교 앵커:**

- 후보 `slot:light_type:tungsten_practical` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · warm tungsten practical light
- 프로필 `mixed_illuminant_white_balance_relation` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- 직접광을 피해야 한다는 일반 조언을 이 요청에 적용하지 않는다.
- 폰으로 실제 찍었다는 이력을 입증하지 않는다.

**관련 근거:** [Nikon — The Basics of Flash Photography](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-basics-of-flash-photography) / [ARRI — Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G24 · 광학 흔적의 발생 위치 구별

**경로:** semantic_boundary_review · P0 · 효과 검증 전 trial

**씨앗:** K261 `gentle lens bloom` / K262 `subtle halation` / K270 `irregular light-leak softness` / K271 `foreground condensation` / K272 `fingerprints and rain droplets on the lens`

**보여야 할 구성:**

- artifact has a declared carrier plane
- local bright-edge spread is separate from atmospheric volume
- face and contact evidence survive the chosen artifact

**관계:** lens or glass marks and highlight spread occupy their respective carrier layers

**소유자:** lens/glass plane or image capture response

**함께 검토할 변경 범위:** camera / lens artifact / tone response; atmospheric additions need setting scope

**긍정 요청 예:** 렌즈 앞 물방울만 흐리게 보이고 얼굴은 읽히는 사진.

**혼동 반례:** 김·안개·필름 할레이션·diffusion bloom을 모두 같은 뜻의 후보로 저장한다.

**기존 원본·비교 앵커:**

- 후보 `slot:lens_artifact:water_droplets_on_lens` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · water droplets on the lens
- 후보 `slot:lens_artifact:rain_streaks_on_glass` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · rain streaks on glass or lens
- 프로필 `diffusion_filter_highlight_halation` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- 현재 diffusion_filter_highlight_halation 명칭과 정의는 필름 현상과 구분해 검토한다.
- 픽셀 모양이 실제 필름이나 필터 사용을 증명하지 않는다.

**관련 근거:** [Kodak — VISION Color Print Film 2383/3383 technical information](https://www.kodak.com/content/products-brochures/motion-picture/KODAK-VISION-Color-Print-Film-2383-3383-technical-information.pdf) / [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field) / [PBRT 4e — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G25 · 입자와 움직임 흔적을 핵심 증거와 분리

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K263 `fine film grain` / K264 `subtle organic grain` / K273 `slight softness and minor motion blur` / K275 `moderate high-ISO noise` / K280 `restrained optical imperfections`

**보여야 할 구성:**

- image-plane grain stays distinct from object texture
- blur is localized to the declared movement or depth
- required small regions retain usable detail

**관계:** capture traces remain subordinate to declared evidence regions

**소유자:** image response / moving region / focus plane

**함께 검토할 변경 범위:** camera / image finish; do not erase required anatomy or material evidence

**긍정 요청 예:** 미세한 입자는 남기고 손의 접촉과 천의 결은 읽히게.

**혼동 반례:** 입자를 원단 무늬로 넣거나 모든 눈·손을 흔들림으로 지운다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- 필름 입자·센서 노이즈·종이 결을 매체에 맞춰 구별한다.

**관련 근거:** [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) / [Kodak — VISION Color Print Film 2383/3383 technical information](https://www.kodak.com/content/products-brochures/motion-picture/KODAK-VISION-Color-Print-Film-2383-3383-technical-information.pdf) / [Adobe — Control depth of field](https://www.adobe.com/learn/photoshop/web/use-aperture-to-control-depth-of-field)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G26 · 검정 바닥과 하이라이트 계조의 독립 제어

**경로:** reuse_and_qualify · P1 · 효과 검증 전 trial

**씨앗:** K282 `lifted matte blacks` / K284 `smooth highlight rolloff` / K296 `deep blacks with readable fabric folds`

**보여야 할 구성:**

- shadow floor follows one selected grade
- dark cloth retains requested fold information
- bright regions approach white with the selected shoulder

**관계:** tone response preserves the chosen shadow and bright-region evidence

**소유자:** image tone response / existing cloth and highlights

**함께 검토할 변경 범위:** color / image.color_grading; material finish is a separate effect

**긍정 요청 예:** 깊은 검정 의상의 주름과 밝은 천의 계조가 함께 남는다.

**혼동 반례:** 모든 검정을 띄우라는 지시와 깊은 검정 유지 지시를 같은 영역에 겹친다.

**기존 원본·비교 앵커:**

- 후보 `slot:color_grading:pe_faded_black_floor` · [photo_prompt_editing_effects_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json) · faded image tones with lifted blacks and reduced chroma
- 후보 `slot:color_grading:lit_noir_deep_detailed_black_finish` · [photo_prompt_lighting_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_lighting_extension.json) · deep detailed blacks with protected selective whites
- 후보 `slot:color_grading:lit_golden_protected_warm_rolloff` · [photo_prompt_lighting_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_lighting_extension.json) · warm finish with protected highlight rolloff
- 프로필 `highlight_rolloff_tone_response` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)
- 프로필 `egr_profile_low_key_lifted_black_floor` · [photo_prompt_visual_obligations_ethereal_gothic_scene.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_ethereal_gothic_scene.json)

**해석·검증 한계:**

- lifted blacks와 deep blacks는 목표 영역·곡선 선택을 명확히 한다.
- smooth가 무조건 좋은 마감이라는 주장으로 쓰지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Kodak — VISION Color Print Film 2383/3383 technical information](https://www.kodak.com/content/products-brochures/motion-picture/KODAK-VISION-Color-Print-Film-2383-3383-technical-information.pdf) / [Hu et al. — TIFA](https://arxiv.org/abs/2303.11897)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G27 · 팔레트 이름을 색의 소유자와 면적으로 번역

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K301 `charcoal × warm gold × ivory blossoms` / K302 `black × ivory × a single scarlet accent` / K308 `deep teal × oatmeal × wood brown` / K311 `blue-gray × cool white × traffic-light red` / K316 `cream × burgundy-brown × tungsten amber`

**보여야 할 구성:**

- dominant existing surface owns the main color
- secondary existing surface owns another color
- accent is confined to its named carrier

**관계:** local colors stay on their declared carriers with a clear hierarchy

**소유자:** declared surfaces / trim / light carriers

**함께 검토할 변경 범위:** color / surface.local_color / wardrobe.color / background.local_color

**긍정 요청 예:** 검정 의상과 아이보리 배경 사이에서 빨간 리본 하나가 작게 강조된다.

**혼동 반례:** 색 조합만으로 특정 민족·기분·지능을 판정하거나 코발트 후보를 빨강과 동의어로 만든다.

**기존 원본·비교 앵커:**

- 후보 `slot:color:pal_app_neutral_cobalt_accent` · [photo_prompt_palette_applications_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_palette_applications_extension.json) · one small cobalt-blue object stands apart from a larger off-white and graphite neutral field; the cobalt color remains confined to that object
- 프로필 `cr_achromatic_accent` · [photo_prompt_visual_obligations_color_relations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_color_relations.json)

**해석·검증 한계:**

- 기존 코발트 팔레트는 바인딩 구조의 비교 대상이며 빨강 팔레트와 동의어가 아니다.
- 20개 조합을 모두 새 hard profile로 복제하지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [Huang et al. — T2I-CompBench++ (v3, 2025)](https://arxiv.org/abs/2307.06350v3)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G28 · 같은 빛 아래 서로 다른 재질 반응

**경로:** relation_bundle_trial · P0 · 효과 검증 전 trial

**씨앗:** K321 `black silk satin` / K333 `matte fabric against polished metal` / K335 `natural folds and fabric weight` / K340 `material-specific highlights`

**보여야 할 구성:**

- matte fabric retains diffuse texture
- polished metal has bounded view-dependent highlights
- folds and edges preserve each surface identity

**관계:** two declared material owners respond differently to the same illumination

**소유자:** existing cloth / metal / light

**함께 검토할 변경 범위:** material / surface.reflectance; lighting or garment changes require open scope

**긍정 요청 예:** 무광 원단과 닦인 금속 장식이 같은 빛을 서로 다르게 받는다.

**혼동 반례:** 모든 표면을 glossy로 만들거나 한복 재해석 프로필의 복장 전체를 가져온다.

**기존 원본·비교 앵커:**

- 프로필 `satin_directional_luster_drape_surface` · [photo_prompt_visual_obligations_reactorprompt.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_reactorprompt.json)
- 프로필 `pa_bounded_metal_trim` · [photo_prompt_visual_obligations_palette_applications.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_palette_applications.json)

**해석·검증 한계:**

- 반사 모델은 시각 설계를 돕지만 실제 성분 검사로 쓰지 않는다.

**관련 근거:** [PBRT 4e — Diffuse Reflection](https://www.pbr-book.org/4ed/Reflection_Models/Diffuse_Reflection) / [PBRT 4e — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission) / [PBRT — Surface Reflection](https://www.pbr-book.org/3ed-2018/Color_and_Radiometry/Surface_Reflection) / [MFA CAMEO — Satin](https://cameo.mfa.org/wiki/Satin)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G29 · 실크 섬유와 faille 직조의 분리

**경로:** new_material_trial · P1 · 효과 검증 전 trial

**씨앗:** K323 `ivory silk faille` / K324 `graphite silk` / K339 `crisp cotton against heavy wool`

**보여야 할 구성:**

- fine crosswise ribs lie on one cloth surface
- ribs continue across the declared fold structure
- declared color remains local to that cloth

**관계:** weave texture follows the same continuous garment surface

**소유자:** existing garment cloth

**함께 검토할 변경 범위:** material / wardrobe.material and surface.texture; color and silhouette stay separate

**긍정 요청 예:** 아이보리 실크 faille의 가로 잔골이 주름을 따라 읽히는 옷.

**혼동 반례:** 실크·새틴·faille를 동의어로 만들거나 광택만으로 faille를 통과시킨다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- 원단 용어가 특정 피부 노출·재단·신체 형태를 요구하지 않는다.
- 섬유 성분의 실제 진위는 렌더에서 입증하지 않는다.

**관련 근거:** [MFA CAMEO — Satin](https://cameo.mfa.org/wiki/Satin) / [MFA CAMEO — Faille](https://cameo.mfa.org/wiki/Faille) / [MFA CAMEO — Silk](https://cameo.mfa.org/wiki/Silk)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G30 · 리본에서 절개선으로 이어지는 조형 연결

**경로:** new_relation_trial · P1 · 효과 검증 전 trial

**씨앗:** K343 `one sculptural couture bow` / K344 `a ribbon tail continuing into a bodice seam` / K360 `a motif expressed through line, not literal costume`

**보여야 할 구성:**

- declared ribbon tail has an attachment origin
- tail direction reaches the declared bodice seam
- seam continues in the same garment rather than on skin

**관계:** one visible motif continues from ribbon structure into an existing garment seam

**소유자:** ribbon / seam / same garment

**함께 검토할 변경 범위:** appearance / wardrobe.details; geometry changes must be open

**긍정 요청 예:** 리본 끝의 선이 같은 의상의 절개선으로 자연스럽게 이어진다.

**혼동 반례:** 머리 리본의 매달림이나 cut-on sleeve를 의상 절개선 연결과 동의어로 처리한다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- 미적 선의 연속과 실제 부품 부착을 각각 기록한다.
- 신체에 새로운 선·상처·구멍을 만들지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G31 · 잔머리의 뿌리·바람·역광 연결

**경로:** reuse_and_qualify · P1 · 효과 검증 전 trial

**씨앗:** K363 `fine flyaways caught in backlight` / K376 `hair gently moved by a draft` / K377 `wet strands against the temples` / K380 `hair ornaments following the main silhouette`

**보여야 할 구성:**

- fine hairs connect to the declared roots or tie
- strand displacement agrees with an established local cause
- backlight response follows the actual strand edges

**관계:** owned strands respond to an established breeze or movement and source direction

**소유자:** actor hair / established air or action / light

**함께 검토할 변경 범위:** appearance / hair.style; weather and lighting need independent scope

**긍정 요청 예:** 역광 속 잔머리는 머리카락에서 이어지고 기존 바람에 조금 움직인다.

**혼동 반례:** 머리카락을 공중 장식으로 떼거나 머리 잠금 때문에 가려진 가닥을 통과로 기록한다.

**기존 원본·비교 앵커:**

- 후보 `slot:hair_style:pr_hair_strand_owner_and_cause_candidate` · [photo_prompt_photorealism_elements_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_photorealism_elements_extension.json) · Keep a few flyaway hairs attached to the hairline, with their direction explained by the scene's motion or air.
- 프로필 `pr_hair_strand_owner_and_cause` · [photo_prompt_visual_obligations_photorealism_elements.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_photorealism_elements.json)

**해석·검증 한계:**

- 바람 없는 고정 장면에는 바람을 새로 넣지 않는다.

**관련 근거:** [ARRI — Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf) / [PBRT 4e — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G32 · 피부 결·고유색·조명색의 분리

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K381 `natural skin texture` / K384 `subtle natural skin-tone variation` / K387 `natural facial asymmetry` / K399 `skin affected by the light color` / K400 `preserve identity without beauty smoothing`

**보여야 할 구성:**

- declared skin texture remains locally visible
- incident color follows the lighting zone
- identity-defining structure remains unchanged where locked

**관계:** illumination varies over the same skin surface without redefining its local identity

**소유자:** actor skin / light receiver region

**함께 검토할 변경 범위:** appearance / skin.texture and lighting / surface.illumination; local skin color separately locked

**긍정 요청 예:** 피부 고유색은 유지하면서 창빛이 닿는 면만 차갑게 보인다.

**혼동 반례:** 조명색을 피부색 변경으로 저장하거나 눈밑 그림자로 질병·피로를 확정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:skin_finish:skin_microtexture_local_light_response` · [photo_prompt_reactorprompt_visual_relations_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_reactorprompt_visual_relations_extension.json) · skin microtexture retained through local diffuse and specular light response
- 후보 `slot:complexion_coverage:sheer_complexion_texture_preservation` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · sheer complexion correction preserving pores, fine texture, and local natural color variation
- 프로필 `sheer_complexion_texture_preservation` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- 솜털·모공·잡티를 모든 초상의 의무로 추가하지 않는다.
- 일러스트 얼굴에 실사 피부 결을 강제하지 않는다.

**관련 근거:** [PBRT — Surface Reflection](https://www.pbr-book.org/3ed-2018/Color_and_Radiometry/Surface_Reflection) / [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G33 · 생활 흔적을 장면의 행동과 묶기

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K405 `annotated research papers` / K406 `worn vintage leather sofa` / K408 `a lived-in interior` / K409 `wrinkled white bedding` / K420 `one unmistakable cue of the place`

**보여야 할 구성:**

- one established setting cue is readable
- one trace belongs to a current task or surface
- supporting objects remain subordinate

**관계:** trace and present action share the same established place

**소유자:** existing room / object / actor task

**함께 검토할 변경 범위:** setting / props / action only when open

**긍정 요청 예:** 펴둔 책과 손이 멈춘 자리가 함께 읽히는 조용한 방.

**혼동 반례:** lived-in을 무조건 잡동사니 가득한 방으로 바꾸거나 논문으로 천재성을 판정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:location:lived_in_studio_room` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · a lived-in small studio room
- 후보 `slot:space_condition:lived_in_clutter` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · lived-in clutter with everyday objects left naturally around the space

**해석·검증 한계:**

- 흔적이 실제 과거 사건을 증명하지 않는다.
- 요청에 없는 물건을 늘려 생활감 목표를 채우지 않는다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Barrett et al. — Emotional Expressions Reconsidered (2019)](https://pmc.ncbi.nlm.nih.gov/articles/6640856/) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G34 · 물 접촉점과 표면 변화의 원인 연결

**경로:** new_relation_trial · P0 · 효과 검증 전 trial

**씨앗:** K428 `irregular wet patches` / K429 `beads of water clinging to lashes` / K430 `rain-darkened stone` / K431 `subtle ripples around a touching hand` / K439 `realistic surface tension`

**보여야 할 구성:**

- declared hand or object contacts the water surface
- a localized ripple or meniscus belongs to that contact
- wet and dry regions remain separate on the same receiver

**관계:** water response starts at the declared contact rather than at an unrelated source

**소유자:** actor part / water surface / same material receiver

**함께 검토할 변경 범위:** relationship / water_contact, material / moisture, pose where needed

**긍정 요청 예:** 손끝이 수면에 닿은 지점에서만 작은 잔물결이 퍼진다.

**혼동 반례:** 말소리의 초현실 잔물결이나 일반 하천을 손 접촉과 같은 뜻으로 처리한다.

**기존 원본·비교 앵커:**

- 직접 연결한 ID 없음. 신규 의미의 필요성과 인접 기존 데이터부터 재검토한다.

**해석·검증 한계:**

- 비·습기·수중 상태를 서로 대신 쓰지 않는다.
- 물리적 원인의 설명과 픽셀의 접촉 확인을 구별한다.

**관련 근거:** [PBRT 4e — Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G35 · 바람에 반응하는 여러 운반체의 정합성

**경로:** relation_bundle_trial · P1 · 효과 검증 전 trial

**씨앗:** K155 `a ribbon tail caught in the wind` / K432 `flowing fabric motion` / K440 `one consistent wind direction`

**보여야 할 구성:**

- hair and cloth remain attached to their owners
- their local displacement agrees with the stated airflow
- mass and support allow different curvature and delay

**관계:** several established carriers respond compatibly to one declared local airflow

**소유자:** hair / cloth / air in existing scene

**함께 검토할 변경 범위:** appearance / pose / atmosphere; no new wind through a hair-only effect

**긍정 요청 예:** 같은 옆바람을 받는 머리와 리본이 각 재질에 맞게 휘어진다.

**혼동 반례:** 모든 가닥을 완전히 평행하게 만들거나 자세 움직임을 바람과 동일시한다.

**기존 원본·비교 앵커:**

- 후보 `slot:hair_style:pr_hair_strand_owner_and_cause_candidate` · [photo_prompt_photorealism_elements_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_photorealism_elements_extension.json) · Keep a few flyaway hairs attached to the hairline, with their direction explained by the scene's motion or air.
- 후보 `slot:motion:mep_garment_movement_candidate` · [photo_prompt_model_editorial_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_model_editorial_extension.json) · one readable step or turn provides the movement phase; the attached fabric trails or folds in a direction compatible with that movement; the support or airborne state remains consistent with the chosen phase
- 프로필 `pr_hair_strand_owner_and_cause` · [photo_prompt_visual_obligations_photorealism_elements.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_photorealism_elements.json)
- 프로필 `mep_garment_movement` · [photo_prompt_visual_obligations_model_editorial.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_model_editorial.json)

**해석·검증 한계:**

- 난류·관성·무게를 고려해 일치와 복제를 구별한다.

**관련 근거:** [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G36 · 시간 정지 연출의 정지 구역과 예외

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K040 `time freeze surrealism` / K441 `raindrops suspended in midair` / K442 `single raindrop floating upward` / K443 `stopped car splash` / K444 `birds frozen in air` / K459 `a single impossible rule in a believable world`

**보여야 할 구성:**

- ordinary scene retains its established geometry
- selected drops or splash have suspended configurations
- any allowed exception has a separately bounded owner

**관계:** the declared rule governs one selected domain while its explicit exception stays separate

**소유자:** declared world region / suspended elements / exception

**함께 검토할 변경 범위:** concept / action / atmosphere / composition; requester rule has authority

**긍정 요청 예:** 빗방울이 멈춘 교차로에서 방울 하나만 위로 떠오르는 연출.

**혼동 반례:** 빠른 셔터로 찍힌 물보라만 보고 실제 시간이 정지했다고 통과한다.

**기존 원본·비교 앵커:**

- 프로필 `diegetic_reality_invariant_failure` · [photo_prompt_visual_obligations.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json)

**해석·검증 한계:**

- 실제 시간 정지를 정지 픽셀로 증명하지 않는다.
- 규칙 하나는 설계 선택이며 여러 규칙을 요청한 사용자에게 강제하지 않는다.

**관련 근거:** [MoMA — Surrealism and Dreams](https://www.moma.org/collection/terms/surrealism/surrealism-and-dreams) / [Adobe — Motion blur](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G37 · 흑연선에서 실과 꽃으로 이어지는 입체 경계

**경로:** new_relation_trial · P0 · 효과 검증 전 trial

**씨앗:** K039 `sketch-to-reality transition` / K446 `graphite lines becoming real thread` / K447 `lace becoming stems and three-dimensional roses` / K448 `some flowers remain unfinished drawings` / K460 `visible transition instead of a decorative effect`

**보여야 할 구성:**

- drawn line lies flat on declared paper
- one intermediate raised thread joins that line
- a connected lace or stem region becomes visibly dimensional

**관계:** source mark, intermediate material and target form share a continuous owned boundary

**소유자:** paper mark / attached thread / declared emerging form

**함께 검토할 변경 범위:** material / junction, composition / depth; subject or anatomy changes need explicit scope

**긍정 요청 예:** 종이 위 연필선이 실제 실로 솟아 같은 꽃의 줄기로 이어지는 경계.

**혼동 반례:** 실제 꽃을 그림 옆에 놓거나 전체 그림을 한 번에 실물로 바꾼 결과를 전환 경계라고 한다.

**기존 원본·비교 앵커:**

- 후보 `slot:transition_stage:contiguous_source_target_mid_metamorphosis` · [photo_prompt_imaginal_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_imaginal_extension.json) · a mid-metamorphosis stage continuously connecting readable source and target forms
- 후보 `slot:surface_material:pe_pencil_print` · [photo_prompt_editing_effects_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json) · pencil linework on a depicted paper artifact

**해석·검증 한계:**

- 일부 평면 흔적을 남기는 것은 이 비교 사례의 요구이지 모든 변신의 의무가 아니다.

**관련 근거:** [The Met — Graphite](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-graphite) / [The Met — Watercolor](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-watercolor) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [Cho et al. — Davidsonian Scene Graph](https://google.github.io/dsg/)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G38 · 실제 축소 크기와 미니어처처럼 보이는 초점 효과

**경로:** enrich_existing · P1 · 효과 검증 전 trial

**씨앗:** K215 `a close foreground hand as a scale anchor` / K450 `consistent miniature scale` / K451 `an artist's hand as a scale reference` / K452 `toy-scale miniature city` / K453 `strong tilt-shift effect` / K454 `center focus band`

**보여야 할 구성:**

- declared familiar anchor shares a readable depth relation
- relative dimensions agree across objects
- focus effect is separate from geometric scale

**관계:** object scale is constrained by an established anchor rather than by blur alone

**소유자:** scale anchor / miniature / common support plane

**함께 검토할 변경 범위:** body_geometry / scale or composition / depth; lens / focus is separate

**긍정 요청 예:** 실제 손 옆의 작은 종이 위 도시가 일관된 크기로 보이게.

**혼동 반례:** tilt-shift 흐림 띠가 있다는 이유만으로 도시가 실제 장난감 크기라 판정한다.

**기존 원본·비교 앵커:**

- 후보 `slot:scale_relation:canonical_size_anchor_relation` · [photo_prompt_research_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_research_extension.json) · a familiar same-plane object providing a canonical size anchor without forced perspective
- 후보 `slot:subject:miniature_city_scene` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · a city scene made to look miniature by tilt-shift optics

**해석·검증 한계:**

- 미니어처 인상과 물리적 축소 의미를 구별한다.
- 기준물 추가는 setting/prop 범위가 열려 있을 때만 가능하다.

**관련 근거:** [Nikon — The PC Lens Advantage](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/the-pc-lens-advantage-what-you-see-is-what-youll-get) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [Ghosh et al. — GenEval](https://arxiv.org/abs/2310.11513)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G39 · 종이 바탕과 수채 워시·흑연의 물성

**경로:** defer_medium_route · P2 · 효과 검증 전 trial

**씨앗:** K018 `watercolor and graphite illustration` / K461 `visible pencil strokes` / K462 `watercolor washes` / K463 `paper texture` / K467 `large white paper areas` / K476 `translucent watercolor bleed` / K477 `dry-brush texture`

**보여야 할 구성:**

- paper substrate remains distinct from the image plane
- transparent wash lets paper contribute to value
- graphite marks and dry-brush gaps have medium-specific surfaces

**관계:** drawing marks and washes remain on their declared paper support

**소유자:** physical paper artwork or separately selected illustration output

**함께 검토할 변경 범위:** material / surface.texture for photographed artifact; pure illustration needs its own medium route

**긍정 요청 예:** 하얀 종이 여백과 연필선이 남는 수채 초상.

**혼동 반례:** 수채 요청을 실사 DSLR 얼굴로 만들고 종이 입자만 후처리로 덮는다.

**기존 원본·비교 앵커:**

- 후보 `slot:surface_material:pe_pencil_print` · [photo_prompt_editing_effects_extension.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_editing_effects_extension.json) · pencil linework on a depicted paper artifact

**해석·검증 한계:**

- photo corpus에는 촬영된 종이 작품의 표면으로 제한해 사용할 수 있다.
- 순수 일러스트를 photo medium으로 자동 등록하지 않는다.

**관련 근거:** [The Met — Watercolor](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-watercolor) / [The Met — Graphite](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-graphite) / [PBRT 4e — Diffuse Reflection](https://www.pbr-book.org/4ed/Reflection_Models/Diffuse_Reflection)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

## G40 · 선·명암 덩어리·경계·디테일의 위계

**경로:** defer_medium_route · P2 · 효과 검증 전 trial

**씨앗:** K472 `tapered linework` / K473 `hard and soft edge hierarchy` / K474 `selective detail concentration` / K475 `simple value masses beneath rich ornament` / K479 `detailed focal area with a suggestive background` / K480 `rich surface detail without silhouette clutter`

**보여야 할 구성:**

- primary silhouette remains legible at small scale
- selected focal area has denser edges and detail
- secondary regions preserve larger value masses

**관계:** detail concentration supports the primary shape rather than replacing its hierarchy

**소유자:** declared focal area / silhouette / support field

**함께 검토할 변경 범위:** composition for shared hierarchy; linework and painted surfaces require illustration scope

**긍정 요청 예:** 장식은 풍부하지만 작은 크기에서도 실루엣과 얼굴 중심이 읽히는 2D 그림.

**혼동 반례:** 모든 면에 같은 잔선을 넣거나 피부 디테일과 셀 채색을 자동 병합한다.

**기존 원본·비교 앵커:**

- 후보 `slot:composition:primary_secondary_figure_ground_hierarchy` · [photo_prompt_tags.json](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json) · primary figure, subordinate support, and background separated by a clear hierarchy of boundaries and contrast

**해석·검증 한계:**

- 단순 명암과 적은 정보가 모든 미감의 정답은 아니다.
- 사진의 위계는 재사용하되 붓질·선 처리 의미는 별도 보존한다.

**관련 근거:** [Getty — Principles of Design](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html) / [Getty — Vocabulary for Describing an Artwork](https://www.getty.edu/education/k-12-learning/describe-listen-draw/vocabulary-for-describing-an-artwork/) / [The Met — Watercolor](https://www.metmuseum.org/perspectives/materials-and-techniques-drawing-watercolor)

근거는 용어·물리·평가 설계의 참고다. 위 조합의 미감 향상은 이번 연구자의 가설이며 해당 출처가 생성 효과를 검증한 것은 아니다.

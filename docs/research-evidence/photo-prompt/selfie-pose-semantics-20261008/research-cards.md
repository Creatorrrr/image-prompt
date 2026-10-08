# 셀카 포즈 상세 연구 카드

2026-10-08 KST · 180개 원문 행을 각각 하나의 연구 카드로 보존했다. 관찰 문장과 관계는 설계 제안이며 운영 등록·이미지 심사는 아직 실행하지 않았다.

출처는 명칭 또는 촬영 원리를 지지한다. 아래 프레이밍·소유·후보 설계 전부를 각 기사에서 확인했다는 뜻이 아니다.


## 1. 표정 중심 셀카

### 001. 옅은 미소 / Soft smile

- 의미·혼동 경계: 입꼬리의 작은 상승과 입 닫힘을 분리한다. 눈웃음이나 행복이라는 내면을 자동으로 요구하지 않는다.
- 관찰 구성: main_subject.face: closed lips meet along one seam / main_subject.face: both mouth corners rise slightly / main_subject.face: lower jaw keeps a neutral position beneath closed lips
- 방향 관계: main_subject.face.mouth_corners → rise_beside → main_subject.face.closed_lips; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 입술선·양 입꼬리를 같은 얼굴 크롭에 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 002. 치아가 보이는 미소 / Teeth smile

- 의미·혼동 경계: 치아 노출량과 웃음 크기는 별개다. 입을 크게 벌린 놀람과 구분한다.
- 관찰 구성: main_subject.face: teeth appear between parted smiling lips / main_subject.face: mouth corners rise on both sides / main_subject.face: cheeks lift beside the same mouth
- 방향 관계: main_subject.face.teeth → visible_between → main_subject.face.lips; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈과 입을 함께 담고 치아가 흐림에 묻히지 않게 한다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 003. 웃음이 터지는 순간 / Laughing selfie

- 의미·혼동 경계: 웃음의 한 시점은 표현할 수 있으나 정지 사진에서 자발성이나 직전 대사를 증명하지 않는다.
- 관찰 구성: main_subject.face: raised cheeks accompany an open smile / main_subject.face: eyes narrow without becoming hidden / main_subject.head: head remains connected above the shoulders during the selected laugh phase
- 방향 관계: main_subject.face.cheeks → rise_beside → main_subject.face.open_smile; main_subject.face → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 움직인 머리가 잘리지 않도록 여백을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 004. 눈웃음 / Smize

- 의미·혼동 경계: 기존 ae_smize는 입꼬리 상승을 포함한다. 입 중립형을 동의어만 추가해 덮어쓰지 않는다.
- 관찰 구성: main_subject.face: cheek and outer eye regions rise gently / main_subject.face: both eyes stay open through softened apertures / main_subject.face: lips remain neutral or only minimally curved in this proposed eye smile variant
- 방향 관계: main_subject.face.eye_apertures → narrow_with → main_subject.face.cheek_rise; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈꺼풀과 입술을 함께 보이게 해 변형을 판별한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 005. 스퀸치 / Squinch

- 의미·혼동 경계: 아래 눈꺼풀 중심의 조작이다. 양 눈꺼풀을 세게 닫는 스퀸트·찡그림과 구분한다.
- 관찰 구성: main_subject.face: lower eyelid margins lift toward the irises / main_subject.face: upper eyelids remain comparatively steady / main_subject.face: both eyes remain visibly open
- 방향 관계: main_subject.face.lower_eyelids → approach → main_subject.face.irises; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 아래 눈꺼풀 경계가 원본 크기에서 읽혀야 한다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 006. 젠지 파우트 / Gen Z pout

- 의미·혼동 경계: 2026년 보도되는 이름이지만 세대·성격·심리 진단이 아니다. 윗입술만의 절대 규칙이나 멍한 시선 강제는 피한다.
- 관찰 구성: main_subject.face: upper lip projects slightly in a small pout / main_subject.face: lower lip is less strongly projected than an exaggerated kiss face / main_subject.face: eyes and mouth corners retain a comparatively unaccented contour
- 방향 관계: main_subject.face.upper_lip → projects_more_than → main_subject.face.lower_lip; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 윗입술·아랫입술·눈이 함께 보이는 얼굴 크롭을 쓴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/), [S05 — Vogue Japan — Gen Z Pout](https://www.vogue.co.jp/article/2026-trends-gen-z-pout-wbg), [S06 — 경향신문 — Z세대 셀카 표정 공식](https://www.khan.co.kr/article/202608220915001/amp)

### 007. 덕페이스 / Duck face

- 의미·혼동 경계: 입술 돌출과 작은 입 벌림은 다르다. 큰 눈이나 장난기는 별도 선택이다.
- 관찰 구성: main_subject.face: lips project forward in a pronounced rounded contour / main_subject.face: mouth corners gather toward the center / main_subject.face: upper and lower lips belong to one coherent mouth
- 방향 관계: main_subject.face.lips → project_forward_from → main_subject.face.plane; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 입술 돌출이 보이는 정면 또는 약한 사선 크롭을 쓴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 008. 입술 살짝 벌리기 / Fish gape·Parted lips

- 의미·혼동 경계: fish gape의 역사적 명칭과 일반 parted lips를 구분해 기록한다. 입술 틈만으로 관능·놀람을 확정하지 않는다.
- 관찰 구성: main_subject.face: upper and lower lips leave a narrow visible gap / main_subject.face: jaw is only slightly lowered / main_subject.face: lip projection is independent of the opening
- 방향 관계: main_subject.face.upper_lip → separated_by_small_gap_from → main_subject.face.lower_lip; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈·코·입의 관계와 작은 입술 틈을 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 009. 한쪽 입꼬리 미소 / Smirk

- 의미·혼동 경계: 비대칭 입꼬리와 얼굴 회전을 구분한다. 자신감·악의·성적 의도는 요청 문맥에 둔다.
- 관찰 구성: main_subject.face: one mouth corner rises more than the other / main_subject.face: opposite mouth corner remains comparatively level / main_subject.face: facial yaw does not alone account for the asymmetry
- 방향 관계: main_subject.face.mouth_corner_a → higher_than → main_subject.face.mouth_corner_b; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 양 입꼬리를 가리지 않고 비교할 수 있어야 한다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)

### 010. 찡긋 웃기 / Scrunched smile

- 의미·혼동 경계: 양 눈의 좁아짐과 한쪽 눈만 감는 윙크를 혼합하지 않는다.
- 관찰 구성: main_subject.face: nose bridge shows a small scrunch / main_subject.face: mouth corners rise into a smile / main_subject.face: eyes narrow while the nose and mouth remain visible
- 방향 관계: main_subject.face.nose_scrunch → co_occurs_with → main_subject.face.smile; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 코·눈·입이 모두 읽히는 가까운 얼굴 프레임을 쓴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S03 — Peter Hurley — The Squinch](https://peterhurley.com/blog/squinch-single-easiest-tip-looking-confident-photos), [S04 — Paul Ekman Group — Facial Action Coding System](https://www.paulekman.com/facial-action-coding-system/)


## 2. 머리 방향·시선 중심 셀카

### 011. 렌즈 정면 응시 / Direct gaze

- 의미·혼동 경계: 화면 속 자기 눈 응시와 촬영 렌즈 응시는 다르다. 얼굴 정면만으로 눈맞춤을 판정하지 않는다.
- 관찰 구성: main_subject.face: eye axes point toward the active camera lens / main_subject.head: face direction is separately readable / camera: the active lens target is distinct from the preview screen
- 방향 관계: main_subject.face.eye_axes → point_toward → camera.active_lens; main_subject.face → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈동자를 충분히 남긴다. 픽셀만으로 미세한 렌즈·화면 차이가 불분명하면 판정 보류한다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 012. 사선 얼굴 / Three-quarter face

- 의미·혼동 경계: 얼굴 사선 방향과 3/4 길이 크롭을 구분한다. 20–40도는 원문 촬영 시작점이며 고정 정의가 아니다.
- 관찰 구성: main_subject.head: face turns in yaw relative to the camera / main_subject.face: both eyes remain visible with unequal cheek widths / main_subject.body: torso direction remains independently specified
- 방향 관계: main_subject.head.face_yaw → differs_from → main_subject.body.torso_yaw; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 양 눈·코·양 볼 윤곽이 읽히는 얼굴 크롭을 쓴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 013. 옆얼굴 / Profile

- 의미·혼동 경계: 일부 반대편 눈이 보이는 사선 얼굴과 구분한다. 한쪽 얼굴만 보인다고 인물 수를 추가하지 않는다.
- 관찰 구성: main_subject.head: face turns sideways relative to the camera / main_subject.face: forehead nose lips and chin create a lateral contour / main_subject.body: neck remains continuous with the turned torso or head
- 방향 관계: main_subject.face.profile_contour → faces_laterally_to → camera; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 이마부터 턱까지 측면 윤곽과 시선 쪽 여백을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 014. 고개 기울이기 / Head tilt

- 의미·혼동 경계: 카메라 롤·몸 전체 기울기·어깨 으쓱을 고개 기울임으로 대체하지 않는다.
- 관찰 구성: main_subject.head: head rolls sideways relative to the thorax / main_subject.body: shoulder line remains an independent reference / main_subject.neck: neck joins the rolled head to the shoulders
- 방향 관계: main_subject.head.roll → differs_from → main_subject.body.thorax_roll; main_subject.head → belongs_to → main_subject; main_subject.body → belongs_to → main_subject; main_subject.neck → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 얼굴과 양 어깨선 또는 목의 기준선을 함께 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 015. 턱을 내리고 올려다보기 / Chin down, eyes up

- 의미·혼동 경계: 카메라가 높다는 사실만으로 턱 내림과 눈 올림을 추정하지 않는다.
- 관찰 구성: main_subject.head: chin pitches downward relative to the thorax / main_subject.face: eye axes turn upward relative to the face / main_subject.neck: chin neck and shoulders remain connected
- 방향 관계: main_subject.face.eye_axes → look_above → main_subject.head.face_forward_axis; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.neck → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈동자·턱·목을 한 프레임에 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 016. 턱을 들고 내려다보기 / Chin up, eyes down

- 의미·혼동 경계: 낮은 카메라와 턱을 든 자세는 독립 축이다. 콧속 확대가 정의가 아니다.
- 관찰 구성: main_subject.head: chin pitches upward relative to the thorax / main_subject.face: eye axes turn downward relative to the face / main_subject.neck: jaw and neck retain readable continuity
- 방향 관계: main_subject.face.eye_axes → look_below → main_subject.head.face_forward_axis; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.neck → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 턱·목·눈의 방향이 함께 읽히도록 약한 각도를 선택한다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 017. 옆으로 시선 빼기 / Look-away

- 의미·혼동 경계: 눈만 이동하는 변형과 고개까지 돌리는 변형을 따로 기록한다. 무관심·진짜 캔디드의 증거가 아니다.
- 관찰 구성: main_subject.face: eye axes point laterally away from the lens / main_subject.head: face yaw stays independently readable / scene_target: the selected off camera target has a declared direction
- 방향 관계: main_subject.face.eye_axes → point_away_from → camera.active_lens; main_subject.face → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈과 코 방향을 비교할 수 있게 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 018. 아래 보기 / Downward gaze

- 의미·혼동 경계: 아래 시선·턱 내림·감은 눈을 동일시하지 않는다.
- 관찰 구성: main_subject.face: irises point toward a lower declared target / main_subject.head: head pitch is separately specified / scene_target: the lower target remains outside or inside the selected frame as requested
- 방향 관계: main_subject.face.eye_axes → point_toward → declared_lower_target; main_subject.face → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈꺼풀·눈동자와 요청된 손 또는 소품을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 019. 눈 감기 / Eyes closed

- 의미·혼동 경계: 자는 중·죽음·평온 같은 상태는 눈 감김으로 확정하지 않는다.
- 관찰 구성: main_subject.face: both eyelid seams close gently / main_subject.face: brows retain an independently selected shape / main_subject.face: mouth expression remains independent of eye closure
- 방향 관계: main_subject.face.upper_eyelid_margins → meet → main_subject.face.lower_eyelid_margins; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 양 눈꺼풀 닫힘을 확인할 수 있는 얼굴 크롭을 쓴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)

### 020. 윙크 / Wink

- 의미·혼동 경계: 한쪽 눈의 폐쇄와 양 눈의 좁아짐을 분리한다. 어느 눈인지 지정되면 인물 기준 좌우를 보존한다.
- 관찰 구성: main_subject.face: one eyelid seam is closed / main_subject.face: the opposite eye remains open / main_subject.face: both eye positions belong to the same face
- 방향 관계: main_subject.face.closed_eye_a → contrasts_with → main_subject.face.open_eye_b; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 감은 눈을 손·머리카락으로 가리지 않는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S16 — Nikon — Look Good in Pictures](https://www.nikonusa.com/press-room/nikons-how-to-series-look-go)


## 3. 볼·턱에 손을 대는 셀카

### 021. 볼 콕 / Cheek poke

- 의미·혼동 경계: 접촉형·눌림형은 별도 강도다. 검지가 닿기만 하는 후보에 피부 함몰을 강제하지 않는다.
- 관찰 구성: main_subject.hand: one index fingertip touches the selected cheek / main_subject.face: the contact lies below the eye beside the mouth / main_subject.arm: the touching hand continues through its own wrist and forearm
- 방향 관계: main_subject.hand.index_tip → touches → main_subject.face.cheek; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 검지 끝과 볼의 접점·손목을 같은 프레임에 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 022. 손바닥에 볼 기대기 / Palm-on-cheek

- 의미·혼동 경계: 단순 접촉과 하중을 받는 배치를 분리한다. 탁자 받침이 없다면 실제 지지력의 측정은 주장하지 않는다.
- 관찰 구성: main_subject.hand: one palm cups the side of the cheek / main_subject.face: cheek rests against the same palm surface / main_subject.arm: fingers and forearm form a continuous support configuration
- 방향 관계: main_subject.hand.palm → supports_configuration → main_subject.face.cheek; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 볼·손바닥·손목을 보이고 하중형은 팔꿈치 받침도 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 023. 한 주먹 턱받침 / Fist under chin

- 의미·혼동 경계: 턱 아래의 열린 손바닥과 구분한다. 지지와 장식적 접촉은 문맥으로 구별한다.
- 관찰 구성: main_subject.hand: loosely folded knuckles sit below the chin / main_subject.face: chin contacts the stated knuckle area / main_subject.arm: wrist and elbow belong to the same support arm
- 방향 관계: main_subject.face.chin → rests_on → main_subject.hand.knuckles; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 턱·주먹·손목을 담고 지지형은 팔꿈치 지지면도 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 024. 콩순이식 양 주먹 / Double-fist cheek pose

- 의미·혼동 경계: 주먹형과 펼친 손가락의 꽃받침형을 구분한다. 이름은 2022년 보도 맥락이며 어린 인물을 강제하지 않는다.
- 관찰 구성: main_subject.hands: two separate fists sit below the cheeks / main_subject.face: face remains centered between the fists / main_subject.arms: each fist connects to a different wrist and arm
- 방향 관계: main_subject.hands → lie_below → main_subject.face.cheeks; main_subject.hands → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 주먹 전체·얼굴·각 손목을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 025. 양손 꽃받침 / Flower pose

- 의미·혼동 경계: 실제 하중 지지와 얼굴을 둘러싼 장식형을 구분한다.
- 관찰 구성: main_subject.hands: two palms open upward beneath the chin / main_subject.hands: fingers fan outward on opposite sides / main_subject.arms: two wrists remain attached to distinct arms
- 방향 관계: main_subject.hands → frame_below → main_subject.face.chin; main_subject.hands → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 손바닥·손가락 끝·턱 아래 공간을 모두 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 026. 한 손 꽃받침 / Half flower

- 의미·혼동 경계: 양손 꽃받침을 한 손에서 두 손으로 늘리지 않는다. 손이 턱을 지지하는지는 별도로 기록한다.
- 관찰 구성: main_subject.hand: one open palm sits diagonally beneath the chin / main_subject.hand: fingers fan toward the opposite cheek / main_subject.arm: one wrist connects that palm to one forearm
- 방향 관계: main_subject.hand → frames_below → main_subject.face.chin; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손 전체와 턱의 간격 또는 접촉을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 027. 턱선 L자 / L-shaped jaw frame

- 의미·혼동 경계: 같은 엄지·검지 모양이어도 턱과의 배치가 다르다. 손가락 총으로 바꾸지 않는다.
- 관찰 구성: main_subject.hand: thumb lies beneath the chin / main_subject.hand: index finger extends beside the selected cheek / main_subject.hand: remaining digits fold on the same connected palm
- 방향 관계: main_subject.hand.thumb → lies_under → main_subject.face.chin; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 엄지·검지·턱의 세 접점 관계를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 028. 손등 턱받침 / Back-of-hand chin rest

- 의미·혼동 경계: 손등과 손바닥이 반대 면이라는 점을 보존한다.
- 관찰 구성: main_subject.hand: dorsum of the hand faces the chin underside / main_subject.face: chin contacts the stated hand dorsum / main_subject.arm: wrist continues without an impossible reversal
- 방향 관계: main_subject.face.chin → rests_on → main_subject.hand.dorsum; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손톱·관절 또는 손등 단서와 턱 접촉을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 029. 볼 살짝 집기 / Cheek pinch

- 의미·혼동 경계: 엄지·검지 두 접점이 필요하다. 볼 콕이나 입술 터치를 대체로 쓰지 않는다.
- 관찰 구성: main_subject.hand: thumb and index finger oppose on one cheek / main_subject.face: a small cheek fold lies between the two digit tips / main_subject.arm: both digit tips belong to one connected hand
- 방향 관계: main_subject.hand.thumb_and_index → pinch → main_subject.face.cheek; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 두 손가락 끝과 작은 피부 주름이 읽히는 가까운 크롭을 쓴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 030. 양손으로 볼 감싸기 / Double cheek cup

- 의미·혼동 경계: 볼 양옆 접촉과 턱 아래 꽃받침을 구분한다. 압박 정도는 열어 둔다.
- 관찰 구성: main_subject.hands: two palms cup opposite cheeks / main_subject.hands: fingers point upward beside the face / main_subject.arms: each palm connects to a separate arm
- 방향 관계: main_subject.hands → cup → main_subject.face.cheeks; main_subject.hands → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 볼·손가락·손목이 읽히게 한다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)


## 4. 눈·입 주변 손동작과 얼굴 가리기

### 031. 티렉스 손 / T-Rex hands

- 의미·혼동 경계: 2016년 이름으로 기록한다. 손톱 길이·매니큐어·새끼손가락 위치를 필수 외형으로 만들지 않는다.
- 관찰 구성: main_subject.hand: one hand displays loosely curled fingers near the face / main_subject.hand: hand dorsum and nails remain readable / main_subject.arm: wrist joins the hand beside the chin or cheek
- 방향 관계: main_subject.hand.curled_digits → lie_near → main_subject.face; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 얼굴 옆의 손가락 굽힘과 손등을 원본 크기로 확인한다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S08 — Teen Vogue — T-Rex Selfie Craze](https://www.teenvogue.com/story/t-rex-hands-selfie-craze)

### 032. 입술 끝 터치 / Fingertip-to-lip

- 의미·혼동 경계: 입술 외곽 접촉·세로 쉿·입 안 삽입은 서로 다른 동작이다.
- 관찰 구성: main_subject.hand: one fingertip touches the outer lower lip or corner / main_subject.face: the touched lip edge remains visible / main_subject.hand: finger remains outside the mouth in this variant
- 방향 관계: main_subject.hand.index_tip → touches_outside → main_subject.face.lip; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손가락 끝·입술 경계·눈을 함께 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 033. 쉿 포즈 / Shh pose

- 의미·혼동 경계: 접촉형과 작은 공기 틈형은 따로 보존한다. 진짜 침묵 강요의 뜻은 외형만으로 확정하지 않는다.
- 관찰 구성: main_subject.hand: one index finger stands vertically before the lips / main_subject.face: lips remain behind that finger / main_subject.arm: the upright digit connects to the same actor wrist
- 방향 관계: main_subject.hand.index → stands_vertical_before → main_subject.face.lips; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손가락의 세로 방향과 입술 위치를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 034. 얼굴 반 가리기 / Half-face hand cover

- 의미·혼동 경계: 손 가림·폰 가림·프레임 밖 크롭은 같은 반쪽 얼굴이 아니다.
- 관찰 구성: main_subject.hand: one upright palm occludes one lateral face half / main_subject.face: the opposite eye and cheek remain visible / main_subject.arm: the covering hand continues to the same actor arm
- 방향 관계: main_subject.hand → occludes → main_subject.face.lateral_half; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손 경계와 남은 한쪽 눈·코·입의 범위를 확인한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 035. 한쪽 눈 가리기 / One-eye cover

- 의미·혼동 경계: 눈 하나 가림과 얼굴 절반 전체 가림을 구분한다.
- 관찰 구성: main_subject.hand: one hand occludes only the selected eye region / main_subject.face: nose and mouth remain visible outside that hand / main_subject.arm: covering palm or dorsum retains wrist continuity
- 방향 관계: main_subject.hand → occludes → main_subject.face.selected_eye; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 가려지지 않은 눈·코·입과 손 가림 경계를 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 036. 손가락 사이로 보기 / Peek-through fingers

- 의미·혼동 경계: 손가락 사이 틈·손 표면의 눈 무늬·손 뒤 완전 가림을 구별한다.
- 관찰 구성: main_subject.hand: fingers separate in front of the face / main_subject.face: one eye is visible through a digit gap / main_subject.hand: the gap edges belong to the same foreground hand
- 방향 관계: main_subject.face.eye → appears_through → main_subject.hand.digit_gap; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손가락 틈의 눈에 초점을 맞추고 손목 연결을 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 037. 이마 짚기 / Facepalm

- 의미·혼동 경계: 이마 손바닥과 관자놀이 손끝을 구분한다. 두통·당황을 진단하지 않는다.
- 관찰 구성: main_subject.hand: palm contacts the forehead plane / main_subject.head: head pitch is separately readable / main_subject.arm: forearm rises to the forehead from the same shoulder
- 방향 관계: main_subject.hand.palm → touches → main_subject.face.forehead; main_subject.hand → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 이마 접촉·손바닥 면·팔 연결을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 038. 햇빛 가리기 / Hand visor

- 의미·혼동 경계: 차양과 경례의 손 각도·위치를 분리한다. 실제 햇빛 차단 효과는 광원과 그림자를 함께 봐야 한다.
- 관찰 구성: main_subject.hand: palm faces downward above the brow / main_subject.hand: extended fingers form a small horizontal visor / main_subject.face: eyes remain below the visor edge
- 방향 관계: main_subject.hand → lies_above → main_subject.face.brow; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손의 수평면·눈썹·눈과 실제 그림자를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 039. 관자놀이 터치 / Temple touch

- 의미·혼동 경계: headache pose는 얼굴을 당기는 변형이 있다. 일반 접촉에 당김·통증을 강제하지 않는다.
- 관찰 구성: main_subject.hand: two or three fingertips contact the temple / main_subject.face: temple lies lateral to the forehead and eye / main_subject.arm: bent elbow forms a continuous arm triangle
- 방향 관계: main_subject.hand.fingertips → touch → main_subject.face.temple; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 관자놀이 접점·손목·가능하면 팔꿈치를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S19 — ELLE — Headache Pose](https://www.elle.com/beauty/a21947206/what-is-headache-pose-instagram/)

### 040. 입 가리고 웃기 / Hand-over-mouth laugh

- 의미·혼동 경계: 입 가림만으로 웃음을 증명하지 않는다. 눈·볼의 움직임은 별도 표정 후보다.
- 관찰 구성: main_subject.hand: same actor hand occludes the mouth front / main_subject.face: cheeks lift and eyes narrow above that hand / main_subject.arm: covering fingers retain their own wrist and arm
- 방향 관계: main_subject.hand → occludes → main_subject.face.mouth; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손 가림과 눈·볼을 함께 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)


## 5. V·캐릭터형 손동작

### 041. 기본 브이 / Classic peace sign

- 의미·혼동 경계: V 목선·승리 의미·인물 연령을 자동으로 추가하지 않는다.
- 관찰 구성: main_subject.hand: index and middle fingers extend into a separated V / main_subject.hand: ring and little fingers fold beside the thumb / main_subject.hand: palm direction remains independently readable
- 방향 관계: main_subject.hand.index → diverges_from → main_subject.hand.middle; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 두 손가락 끝과 접힌 손가락·엄지를 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 042. 눈 옆 가로 브이 / Sideways eye V

- 의미·혼동 경계: 눈을 손가락으로 가리는 변형과 눈 옆 프레임형을 구분한다.
- 관찰 구성: main_subject.hand: index middle V rotates sideways / main_subject.face: outer eye corner lies beside or between the V tips / main_subject.hand: both fingertips remain clear of the eyeball
- 방향 관계: main_subject.hand.v_digits → frame_beside → main_subject.face.outer_eye; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: V 방향·눈꼬리·손목을 함께 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 043. 턱 아래 브이 / V under chin

- 의미·혼동 경계: 두 긴 손가락의 V와 엄지·검지의 L을 구분한다.
- 관찰 구성: main_subject.hand: index and middle fingers separate beneath the chin / main_subject.face: chin lies above the V opening / main_subject.arm: wrist connects the lower V to its own arm
- 방향 관계: main_subject.hand.v_digits → lie_below → main_subject.face.chin; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 턱·검지·중지 관계와 손목을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 044. 갸루피스 / Gyaru peace

- 의미·혼동 경계: 뒤집어 앞으로 뻗는 위치가 핵심이다. 갸루 메이크업·의상·국적을 강제하지 않는다.
- 관찰 구성: main_subject.hand: index middle V points downward and forward / main_subject.arm: gesture arm reaches toward the lens / main_subject.hand: the V remains one connected hand in front of the face
- 방향 관계: main_subject.hand → reaches_toward → camera.lens; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 아래를 향한 손끝·팔 깊이·얼굴을 함께 보인다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 045. 잔망루피식 정수리 브이 / Crown V

- 의미·혼동 경계: 정수리 한 V와 두 손의 토끼 귀는 다르다. 캐릭터 얼굴·분홍 피부를 추가하지 않는다.
- 관찰 구성: main_subject.hand: index middle V sits above the crown center / main_subject.head: crown lies immediately beneath the V base / main_subject.arm: the raised wrist belongs to the posing actor
- 방향 관계: main_subject.hand.v_digits → lie_above → main_subject.head.crown; main_subject.hand → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 정수리와 V 전체를 잘리지 않게 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 046. 토끼 귀 / Bunny ears

- 의미·혼동 경계: 원문의 두 손 자기 머리 변형과 타인 뒤 한 손 장난 변형을 별도 기록한다.
- 관찰 구성: main_subject.hands: two V shapes sit above opposite head sides / main_subject.head: head lies below the two separate V bases / main_subject.arms: each hand connects to a separate arm
- 방향 관계: main_subject.hands.v_pair → lie_above_opposite_sides_of → main_subject.head; main_subject.hands → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 V·정수리·두 손목을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 047. 높낮이 다른 더블 브이 / Asymmetric double V

- 의미·혼동 경계: 두 손 복제 오류와 높낮이 차이를 구분한다. 두 포즈 손은 폰 잡는 손과 겹칠 수 없다.
- 관찰 구성: main_subject.hands: each hand forms an index middle V / main_subject.hands: the two hands occupy different heights / main_subject.arms: two wrists remain assigned to separate arms
- 방향 관계: main_subject.hand_a → higher_than → main_subject.hand_b; main_subject.hands → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양손·팔의 소유와 상대 높이를 읽을 수 있게 한다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 048. 고양이 발 / Cat paw

- 의미·혼동 경계: 이름만으로 고양이 귀·동물 종·장갑을 추가하지 않는다.
- 관찰 구성: main_subject.hand: wrist flexes into the selected paw like angle / main_subject.hand: fingers curl loosely without a rigid fist / main_subject.arm: curled hand stays connected to its own forearm
- 방향 관계: main_subject.hand.curled_digits → continue_beyond → main_subject.hand.flexed_wrist; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 굽힌 손목·손가락·팔 연결을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 049. 경례 / Salute

- 의미·혼동 경계: 군대·계급·특정 국가의 경례 규칙은 요청 없이는 붙이지 않는다.
- 관찰 구성: main_subject.hand: straight grouped fingers lie near the forehead edge / main_subject.hand: palm orientation follows the specified salute variant / main_subject.arm: elbow bends outward from the same shoulder
- 방향 관계: main_subject.hand.grouped_fingers → lie_beside → main_subject.face.forehead_edge; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손끝·이마와 팔꿈치의 관계를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)

### 050. 샤카 / Shaka

- 의미·혼동 경계: 검지·새끼의 록 사인과 엄지·새끼의 샤카를 구별한다. 문화 의미를 보편적 사실로 만들지 않는다.
- 관찰 구성: main_subject.hand: thumb and little finger extend away from the palm / main_subject.hand: index middle and ring fingers remain folded / main_subject.arm: the same wrist supports both extended digits
- 방향 관계: main_subject.hand.thumb → diverges_from → main_subject.hand.little_finger; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 엄지·새끼·접힌 세 손가락을 확인한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S07 — CIVICNEWS — 갸루 피스·잔망루피 피스](https://www.civicnews.com/news/articleView.html?idxno=34000)


## 6. 하트·호감·교감 손동작

### 051. 손가락 하트 / Finger heart

- 의미·혼동 경계: 손가락 하트·집게·돈을 비비는 손동작을 위치와 실루엣으로 구분한다.
- 관찰 구성: main_subject.hand: thumb and index cross in a small two digit shape / main_subject.hand: the crossing has two distinct fingertips / main_subject.arm: both digits belong to one connected wrist
- 방향 관계: main_subject.hand.thumb → crosses → main_subject.hand.index; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 엄지·검지의 작은 교차를 원본 크기에서 읽히게 한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 052. 볼하트 / Cheek heart

- 의미·혼동 경계: 볼하트는 여러 변형이 있으므로 볼+손 곡선이라는 제안형을 먼저 명시한다.
- 관찰 구성: main_subject.hand: one curved hand forms a half heart beside the cheek / main_subject.face: cheek contour completes the adjacent rounded side / main_subject.arm: hand remains connected below the selected cheek
- 방향 관계: main_subject.hand.curve → frames_beside → main_subject.face.cheek; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손 곡선·볼·작은 사이 공간이 읽혀야 한다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 053. 양 볼하트 / Double cheek heart

- 의미·혼동 경계: 곡선 윤곽의 볼하트와 손바닥으로 볼을 감싸는 컵형을 구분한다.
- 관찰 구성: main_subject.hands: each hand curves beside a different cheek / main_subject.face: both cheek hand outlines remain distinct / main_subject.arms: two wrists belong to two separate arms
- 방향 관계: main_subject.hands.curve_pair → frame_opposite_sides_of → main_subject.face.cheeks; main_subject.hands → belongs_to → main_subject; main_subject.face → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양손 실루엣과 양 볼을 함께 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 054. 양손 하트 / Two-hand heart

- 의미·혼동 경계: 손끝을 맞댄 첨탑형과 하트의 음영 공간을 구별한다. 손끝 접촉과 작은 틈형을 분리한다.
- 관찰 구성: main_subject.hands: two curved finger groups create the upper heart sides / main_subject.hands: two thumbs form a lower meeting point / main_subject.hands: a heart shaped negative space remains between the hands
- 방향 관계: main_subject.hands → bound → heart_aperture; main_subject.hands → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양손 전체·하트 안 빈 공간·두 손목을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 055. 머리 위 큰 하트 / Overhead heart

- 의미·혼동 경계: 둥근 발레 팔 타원과 하트의 곡률·접점을 구분한다.
- 관찰 구성: main_subject.arms: both arms rise above the head in opposing curves / main_subject.hands: hands meet near the upper apex / main_subject.head: head stays inside or below the arm heart silhouette
- 방향 관계: main_subject.arms → bound_around → main_subject.head; main_subject.arms → belongs_to → main_subject; main_subject.hands → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 손끝·양 팔꿈치·머리를 한 프레임에 넣는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 056. 고양이 하트 / Cat heart

- 의미·혼동 경계: 원문은 귀를 세우는 손가락을 지정하지 않았다. 대표 용법의 손가락 배치는 후속 실물 예시 확인까지 보류하고, 이 외형안만 유지한다.
- 관찰 구성: main_subject.hands: two hands create a central heart shaped gap / main_subject.hands: two selected fingers create separate ear like peaks / main_subject.hands: heart gap and both peaks remain simultaneously visible
- 방향 관계: main_subject.hands.selected_ear_digits → form_peaks_above → heart_aperture; main_subject.hands → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 하트 빈 공간·두 귀 봉우리·손 소유를 원본으로 확인한다.
- 반영 판단: P0 · geometry_draft_name_activation_deferred
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S23 — 서울경제 — 원문 하트 포즈 참조](https://www.sedaily.com/article/13748013)

### 057. 상대를 기다리는 반쪽 하트 / Half-heart invitation

- 의미·혼동 경계: 실제로 상대를 기다린다는 의도는 사진에서 확정하지 않는다. 완성된 두 사람 하트와 구별한다.
- 관찰 구성: main_subject.hand: one hand forms one open curved heart half / composition: the unfilled half remains beside that hand / main_subject.body: one actor occupies the filled side of the frame
- 방향 관계: main_subject.hand.curve → bounds_half_of → open_heart_space; main_subject.hand → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 반쪽 손과 빈 공간을 함께 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 058. 눈을 둘러싼 작은 하트 / Heart eye frame

- 의미·혼동 경계: 눈에 닿는 배치·손가락 틈형·그래픽 하트를 혼합하지 않는다.
- 관찰 구성: main_subject.hands: two hands form a small heart shaped aperture / main_subject.face: one eye remains visible through that aperture / main_subject.hands: hands sit in front of the eye with an explicit gap
- 방향 관계: main_subject.face.eye → appears_through → heart_aperture; main_subject.hands → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 하트 안 눈동자·양손·반대 눈 또는 입 일부를 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 059. 엄지척 / Thumbs-up

- 의미·혼동 경계: 엄지와 중지의 위치를 구별한다. 동의·찬성 같은 사회적 해석은 문맥에 둔다.
- 관찰 구성: main_subject.hand: thumb extends upward away from the palm / main_subject.hand: four other fingers remain folded / main_subject.arm: thumb and folded digits connect to one wrist
- 방향 관계: main_subject.hand.thumb → points_up_from → main_subject.hand.folded_digit_base; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 엄지 뿌리·접힌 네 손가락을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)

### 060. 렌즈 가리키기 / Point-to-camera

- 의미·혼동 경계: 검지 방향이 렌즈에 향하는지 확인한다. 엄지 세움은 선택이며 손가락 총과 별도다.
- 관찰 구성: main_subject.hand: index finger extends along the camera depth direction / main_subject.hand: other fingers fold separately from the extended index / main_subject.arm: foreshortened finger and wrist remain connected
- 방향 관계: main_subject.hand.index → points_toward → camera.active_lens; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 검지 끝·손바닥·손목의 깊이 연결을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/)


## 7. 머리카락·옷·액세서리를 만지는 셀카

### 061. 귀 뒤로 머리 넘기기 / Hair tuck

- 의미·혼동 경계: 손이 머리 옆에 있다는 것만으로 귀 뒤 넘김을 인정하지 않는다.
- 관찰 구성: main_subject.hand: fingertips guide a small hair strand behind the ear / main_subject.hair: the same strand passes around the ear contour / main_subject.ear: ear and touching hand remain distinct
- 방향 관계: main_subject.hand.fingers → guide_behind → main_subject.ear; main_subject.hand → belongs_to → main_subject; main_subject.hair → belongs_to → main_subject; main_subject.ear → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 귀·가닥·손끝의 통과 관계를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 062. 머리 쓸어 넘기기 / Hair sweep

- 의미·혼동 경계: 한 장은 동작의 선택된 단계만 보여준다. 실제 움직임 이력을 확정하지 않는다.
- 관찰 구성: main_subject.hand: open fingers pass over the forehead hairline / main_subject.hair: hair strands lie behind or beneath those fingers / main_subject.arm: raised arm joins the sweeping hand
- 방향 관계: main_subject.hand.fingers → lie_over → main_subject.forehead.hairline; main_subject.hand → belongs_to → main_subject; main_subject.hair → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 헤어라인·손바닥·움직인 가닥을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 063. 포니테일 잡기 / Ponytail hold

- 의미·혼동 경계: 이미 요청된 포니테일만 사용한다. 이 후보가 머리 길이·헤어스타일을 변경해서는 안 된다.
- 관찰 구성: main_subject.hand: fingers grip the gathered ponytail length / main_subject.hair: the gathered hair remains rooted at the same head / main_subject.arm: gripping wrist remains attached to the actor arm
- 방향 관계: main_subject.hand → grips → main_subject.hair.ponytail; main_subject.hand → belongs_to → main_subject; main_subject.hair → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 묶인 뿌리와 손의 잡는 지점·연결 가닥을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 064. 머리 한 가닥 만지기 / Hair twirl

- 의미·혼동 경계: 가닥 만지기·손가락 감기·잡아당기기를 분리한다.
- 관찰 구성: main_subject.hand: a small hair strand curves around one fingertip / main_subject.hair: that strand continues to the same head hair / main_subject.hand: finger and strand remain separate silhouettes
- 방향 관계: main_subject.hair.strand → curves_around → main_subject.hand.finger; main_subject.hand → belongs_to → main_subject; main_subject.hair → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손끝 주변 가닥과 머리로 이어지는 경로를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 065. 셔츠 칼라 잡기 / Collar touch

- 의미·혼동 경계: 옷깃·쇄골·목 접촉은 서로 다른 대상이다. 셔츠를 새로 추가하지 않는다.
- 관찰 구성: main_subject.hand: fingertips contact one shirt collar edge / main_subject.wardrobe: collar edge remains part of the worn shirt / main_subject.arm: hand connects to its own wrist beside the neckline
- 방향 관계: main_subject.hand → touches → main_subject.wardrobe.collar; main_subject.hand → belongs_to → main_subject; main_subject.wardrobe → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손끝·칼라 경계·목의 분리를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 066. 재킷 라펠 잡기 / Lapel hold

- 의미·혼동 경계: 라펠 접촉이 재킷 전체 열기·벗기로 바뀌지 않게 한다.
- 관찰 구성: main_subject.hand: fingers pinch one lapel edge / main_subject.wardrobe: lapel fold responds locally to the grip / main_subject.arm: gripping hand continues from its own wrist
- 방향 관계: main_subject.hand → grips → main_subject.wardrobe.lapel; main_subject.hand → belongs_to → main_subject; main_subject.wardrobe → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손의 잡는 지점과 라펠 접힘을 보인다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 067. 소매에 손 숨기기 / Sweater paws

- 의미·혼동 경계: 가려진 손을 없는 손 또는 완전한 손 모양 증거로 세지 않는다. 소매 길이 변경은 의상 잠금과 별도 검토한다.
- 관찰 구성: main_subject.wardrobe: sleeve end covers most of the hand / main_subject.hand: selected fingertips remain beyond the sleeve opening / main_subject.arm: covered wrist continues inside the same sleeve
- 방향 관계: main_subject.wardrobe.sleeve → covers → main_subject.hand; main_subject.wardrobe → belongs_to → main_subject; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 소매 입구와 보이는 손끝·팔의 연결을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 068. 선글라스 내리기 / Sunglasses lowered

- 의미·혼동 경계: 선글라스 추가·안경 종류 변경은 금지된 잠금을 존중한다. 벗어 든 상태와 구별한다.
- 관찰 구성: main_subject.hand: fingers grip one frame rim or temple / main_subject.accessory: glasses sit lower on the nose than the eyes / main_subject.face: eyes appear above the lowered top rim
- 방향 관계: main_subject.hand → grips_and_lowers → main_subject.accessory.glasses; main_subject.hand → belongs_to → main_subject; main_subject.accessory → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 잡는 지점·코 위 프레임·노출된 눈을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 069. 안경 고쳐 쓰기 / Glasses adjustment

- 의미·혼동 경계: 프레임 접촉과 눈·관자놀이 접촉을 구분한다. 지적 능력의 단서로 사용하지 않는다.
- 관찰 구성: main_subject.hand: fingertip contacts the bridge or temple of existing glasses / main_subject.accessory: frame remains worn on the same face / main_subject.arm: touching digit belongs to one connected hand
- 방향 관계: main_subject.hand → touches → main_subject.accessory.glasses_frame; main_subject.hand → belongs_to → main_subject; main_subject.accessory → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 프레임 접점·손끝·눈 사이 간격을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 070. 모자 챙 잡기 / Cap-brim touch

- 의미·혼동 경계: 모자 추가나 챙 형태 변경을 자동으로 하지 않는다.
- 관찰 구성: main_subject.hand: fingers grip the edge of an existing cap brim / main_subject.accessory: brim continues to the cap worn on the head / main_subject.face: face visibility remains separate from the brim angle
- 방향 관계: main_subject.hand → grips → main_subject.accessory.cap_brim; main_subject.hand → belongs_to → main_subject; main_subject.accessory → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손끝·챙·모자의 연결과 얼굴 가림 범위를 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)


## 8. 기본 카메라 높이·크롭 변형

### 071. 눈높이 기본 셀카 / Eye-level selfie

- 의미·혼동 경계: 폰 중앙의 높이와 사용 렌즈 높이를 구분한다. 폰이 최종 셀카 화면 안에 보여야 하는 것은 아니다.
- 관찰 구성: camera: active lens lies approximately at the actor eye level / main_subject.arm: one capture arm extends toward the device / main_subject.face: face remains directed toward the selected lens or screen target
- 방향 관계: camera.lens → at_height_of → main_subject.face.eyes; main_subject.arm → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 직접 셀카는 촬영 팔·깊이 단서를 남기되 기기 전체 노출을 강제하지 않는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 072. 약한 하이앵글 / Slight high angle

- 의미·혼동 경계: 고개 숙임과 카메라 높이를 분리한다. 각도만으로 얼굴 작아짐을 보장하지 않는다.
- 관찰 구성: camera: lens lies slightly above eye level / main_subject.head: upper face plane has a mild downward view relation / background: scene perspective agrees with the higher camera
- 방향 관계: camera.lens → slightly_above → main_subject.face.eyes; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈·턱·어깨 및 필요한 공간 기준을 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 073. 팔을 올린 하이앵글 / Raised-arm selfie

- 의미·혼동 경계: 들어 올린 촬영 팔과 별도의 포즈 팔을 구분한다. 양손을 포즈에 쓰면 고정 촬영이 필요하다.
- 관찰 구성: main_subject.arm: capture arm rises above the head / camera: active lens points downward from that raised position / main_subject.head: face looks toward the declared upper lens target
- 방향 관계: main_subject.capture_arm → holds_above → camera; main_subject.arm → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 팔 진입점·얼굴·아래쪽 몸의 깊이 관계를 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 074. 정수리 위 탑다운 / Top-down portrait

- 의미·혼동 경계: 약한 하이앵글과 수직 탑다운은 다르다. 얼굴 정면 노출은 필수가 아니다.
- 관찰 구성: camera: optical axis points nearly vertically downward / main_subject.head: crown lies below the lens / support_surface: floor or seat plane spreads behind the actor from above
- 방향 관계: camera.lens → looks_down_on → main_subject.head.crown; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 정수리·어깨·지지면 배치를 포함한다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 075. 가슴 높이 로우앵글 / Chest-level low angle

- 의미·혼동 경계: 카메라 높이는 몸 기준으로 기록한다. 턱 들기·콧속 강조를 자동으로 요구하지 않는다.
- 관찰 구성: camera: lens lies below the actor eye level near chest height / main_subject.head: face is viewed from below along an upward optical axis / background: upper room or sky region occupies the upper frame
- 방향 관계: camera.lens → below → main_subject.face.eyes; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 목·턱과 배경의 수직 원근을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 076. 바닥 높이 셀프포트레이트 / Ground-level portrait

- 의미·혼동 경계: 인물이 쪼그린 자세와 카메라가 바닥에 있는 상태는 독립이다.
- 관찰 구성: camera: device rests close to the floor on a stable support / main_subject.body: actor rises above that low camera plane / support_surface: floor continues beneath both camera position and actor support
- 방향 관계: camera → rests_near → support_surface.floor; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 몸과 지면의 관계를 보여주는 넓은 구도를 쓴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 077. 기울어진 화면 / Dutch-angle selfie

- 의미·혼동 경계: 문틀·거울선 같은 수직 기준을 쓴다. 고개 기울기만으로 더치앵글을 인정하지 않는다.
- 관찰 구성: composition: normally vertical scene lines tilt together in the image / main_subject.body: body tilt remains independently readable / composition: image roll differs from head roll
- 방향 관계: setting.vertical_lines → tilt_relative_to → image.vertical_axis; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 배경의 기준선과 얼굴을 함께 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 078. 극근접 크롭 / Tight face crop

- 의미·혼동 경계: 적당한 거리 촬영 후 크롭과 렌즈에 얼굴을 가까이 둔 원근을 분리한다.
- 관찰 구성: composition: face occupies most of the image area / main_subject.face: selected forehead or chin edge lies outside the crop / camera: physical camera distance remains independently specified
- 방향 관계: image.crop → cuts_selected_edges_of → main_subject.face; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 요청된 눈·입 등 핵심 부위의 원본 해상도를 유지한다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 079. 반쪽 얼굴 크롭 / Half-face crop

- 의미·혼동 경계: 프레임 밖 얼굴과 손·폰 뒤 얼굴을 구별한다.
- 관찰 구성: composition: frame edge cuts through one side of the face / main_subject.face: remaining half is visible inside the image / composition: no hand or phone is required at the cut boundary
- 방향 관계: image.frame_edge → cuts_through → main_subject.face.lateral_half; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 프레임 경계가 얼굴을 자르는 위치를 명확히 보인다.
- 반영 판단: P0 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)

### 080. 배경을 크게 넣는 셀카 / Environmental selfie

- 의미·혼동 경계: 작은 인물만으로 셀프 촬영을 증명하지 않는다. 팔 길이를 넘는 거리는 고정 장치나 연장 장비 문맥이 필요하다.
- 관찰 구성: main_subject.body: actor occupies a comparatively small image region / setting: recognizable surrounding space occupies a broad area / main_subject.arm: capture mode remains consistent with the chosen camera distance
- 방향 관계: setting.projected_area → larger_than → main_subject.projected_area; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 인물·장소·촬영 방식의 공간 관계를 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion)


## 9. 0.5배 초광각·과장된 원근 셀카

### 081. 큰 머리·작은 몸 / Big-head overhead

- 의미·혼동 경계: 0.5배 숫자만으로 머리 확대를 요구하지 않는다. 해부학적 머리 크기 변경과 원근 효과를 분리한다.
- 관찰 구성: camera: lens sits nearer the head than the feet / main_subject.head: head projects larger relative to the distant body / main_subject.body: shoulders torso and feet remain one continuous actor
- 방향 관계: main_subject.head → nearer_than → main_subject.feet; main_subject.head → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 머리·몸·발의 비교가 가능한 넓은 탑다운 프레임을 쓴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 082. 긴 팔 대각선 / Long-arm diagonal

- 의미·혼동 경계: 긴 팔처럼 보이는 투영과 실제 팔 길이를 변경하는 것은 다르다.
- 관찰 구성: main_subject.arm: capture arm enters from a frame corner / main_subject.arm: forearm runs diagonally toward the actor / camera: near arm segments project larger than the distant shoulder
- 방향 관계: main_subject.capture_arm → projects_diagonally_from → image.corner; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 팔의 진입점·손목 또는 팔꿈치·어깨 연결을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 083. 손바닥 내밀기 / Reaching-hand perspective

- 의미·혼동 경계: 렌즈 앞으로 내민 손과 폰을 잡은 손의 역할을 분리한다. 큰 손은 원근이지 손 크기 변경이 아니다.
- 관찰 구성: main_subject.hand: free palm extends closer to the lens than the face / main_subject.hand: fingers spread on that foreground palm / main_subject.arm: wrist elbow and shoulder join the reaching hand
- 방향 관계: main_subject.free_hand → nearer_than → main_subject.face; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 전경 손과 뒤 얼굴이 겹치지 않게 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 084. 소품이 큰 전경 / Oversized foreground prop

- 의미·혼동 경계: 실제 거대 소품과 렌즈 앞 확대 소품을 구별한다. 소품 종류는 요청에 따른다.
- 관찰 구성: prop: held object lies nearer the lens than the face / main_subject.hand: fingers grip that same object / main_subject.face: face remains visible behind or beside the enlarged projection
- 방향 관계: prop → nearer_than → main_subject.face; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 소품 전체·잡는 접점·얼굴의 깊이 순서를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 085. 신발 전경 / Sneaker-forward selfie

- 의미·혼동 경계: 독립된 신발 소품·큰 발 해부학·서 있는 일반 전신과 구분한다.
- 관찰 구성: main_subject.foot: one worn shoe sits nearer the lens than the torso / main_subject.leg: near shoe remains connected through its own ankle and knee / main_subject.body: seated or supported torso stays farther behind
- 방향 관계: main_subject.foot.shoe → nearer_than → main_subject.face; main_subject.foot → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 신발·발목·다리·얼굴의 연결을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 086. 가장자리 과장 / Edge-stretch experiment

- 의미·혼동 경계: 가장자리 늘어짐·배럴 왜곡·어안 곡선을 동일시하지 않는다. 디지털 보정 여부는 별도다.
- 관찰 구성: main_subject.face: face or hand occupies an off axis image edge / composition: that edge region shows stretched projection relative to the central region / background: reference lines retain the chosen lens projection behavior
- 방향 관계: image.edge_object_projection → stretches_relative_to → image.center_object_projection; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 중앙 기준과 가장자리 물체를 비교할 수 있게 한다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 087. 무릎이 앞에 오는 구도 / Knee-forward perspective

- 의미·혼동 경계: 한 무릎 세운 자세와 가까운 카메라의 원근을 별도 조합한다.
- 관찰 구성: main_subject.knee: one bent knee lies nearer the camera than the face / main_subject.leg: thigh and lower leg continue from that knee / main_subject.face: face remains farther behind without total occlusion
- 방향 관계: main_subject.knee → nearer_than → main_subject.face; main_subject.knee → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 무릎·다리·얼굴의 깊이를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 088. 하늘 배경 올려찍기 / Sky-backed low angle

- 의미·혼동 경계: 하늘 배경만으로 로우앵글을 판정하지 않는다.
- 관찰 구성: camera: lens points upward from below the actor face / main_subject.body: actor leans or stands above the lens / setting: sky occupies the background behind head and shoulders
- 방향 관계: setting.sky → lies_behind → main_subject.head_and_shoulders; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 턱 아래 방향·어깨와 하늘의 배치를 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 089. 방 안에 작게 서기 / Tiny subject, big room

- 의미·혼동 경계: 작은 프레임 점유율을 실제 축소 인물·미니어처 방으로 바꾸지 않는다.
- 관찰 구성: main_subject.body: actor occupies a small part of the room image / setting: room corners and floor lines span a wide field / camera: camera position is distant from the actor
- 방향 관계: main_subject.projected_area → smaller_than → room.projected_area; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 인물 전신과 방의 모서리·바닥선을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)

### 090. 앞뒤 크기 대비 / Near–far duo

- 의미·혼동 경계: 두 사람의 실제 신체 크기나 인물 수를 바꾸지 않는다. 깊이와 겹침을 분리한다.
- 관찰 구성: main_subject.face: near actor face occupies a large projected region / partner_subject.body: far actor stands at a greater camera distance / composition: both actor silhouettes remain distinct without owner swapping
- 방향 관계: main_subject.face → nearer_than → partner_subject.body; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 가까운 얼굴·먼 인물 전신과 중간 공간을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S13 — Hootsuite — What is a 0.5 selfie?](https://blog.hootsuite.com/social-media-definitions/0-5-selfie/)


## 10. 상반신 거울 셀카

### 091. 얼굴 전체 가리기 / Face-covered mirror selfie

- 의미·혼동 경계: 얼굴 전체 가림을 얼굴 없는 인물이나 프레임 밖 크롭으로 대체하지 않는다.
- 관찰 구성: phone: held phone occludes the reflected eyes nose and mouth / main_subject.hand: one reflected hand visibly grips that phone / mirror: phone and actor occupy the same reflected room plane
- 방향 관계: phone → occludes → main_subject.face; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 폰의 가림 범위·손 접점·거울 기준을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 092. 얼굴 절반 가리기 / Half-face mirror selfie

- 의미·혼동 경계: 한쪽 눈·볼을 남기는 변형과 폰 위로 눈만 남기는 변형을 구분한다.
- 관찰 구성: phone: held phone covers one lateral reflected face region / main_subject.face: one eye and cheek remain visible beside the phone edge / mirror: hand phone and face share one coherent reflection
- 방향 관계: phone → occludes → main_subject.face.lateral_half; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 폰 경계·남은 눈·볼·손을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 093. 눈 하나만 드러내기 / One-eye reveal

- 의미·혼동 경계: 폰 위·폰 옆 두 변형을 분리한다. 손으로 눈 하나 가림과 반대의 가시성이다.
- 관찰 구성: phone: phone body occludes most of the reflected face / main_subject.face: one eye peeks above or beside one phone edge / main_subject.hand: grip keeps phone connected to the reflected actor
- 방향 관계: main_subject.face.eye → visible_beyond → phone.edge; main_subject.face → belongs_to → main_subject; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 노출된 눈과 폰 모서리의 관계를 원본으로 확인한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 094. 휴대폰을 턱 아래에 / Phone-below-chin

- 의미·혼동 경계: 폰이 가슴에 있다는 사실만으로 시선을 화면에 고정하지 않는다.
- 관찰 구성: phone: phone sits below the reflected chin / main_subject.face: whole face stays visible above the device / main_subject.hand: one reflected hand grips the phone near the upper chest
- 방향 관계: phone → lies_below → main_subject.face.chin; main_subject.face → belongs_to → main_subject; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 얼굴·턱·폰 윗변·손 접점을 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 095. 얼굴 옆에 휴대폰 / Side-phone mirror selfie

- 의미·혼동 경계: 옆에 둔 폰과 얼굴 일부를 가린 폰을 구분한다.
- 관찰 구성: phone: phone lies laterally beside the reflected cheek / main_subject.face: face contour remains visible apart from the phone / main_subject.hand: gripping hand holds the device in the same reflected space
- 방향 관계: phone → lies_beside → main_subject.face.cheek; main_subject.face → belongs_to → main_subject; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 얼굴과 폰 사이 간격·손 접점·거울 공간을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 096. 화면을 내려다보기 / Looking at the screen

- 의미·혼동 경계: 자기 거울 눈·거울 속 렌즈·실제 화면을 별도 대상으로 기록한다. 시선만으로 스마트폰 내용은 주장하지 않는다.
- 관찰 구성: main_subject.face: eye axes point toward the actual held screen / phone: screen target lies below or beside the face / mirror: reflected eyeline corresponds to the same physical screen target
- 방향 관계: main_subject.face.eyes → look_at → phone.screen; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 눈동자·폰 위치를 담되 화면 내용 노출은 요구하지 않는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 097. 거울 속 렌즈 보기 / Lens-reflection gaze

- 의미·혼동 경계: 거울 속 자기 눈을 보는 것과 구분한다. 인물 기준 좌우와 화면 기준 좌우를 별도 기록한다.
- 관찰 구성: main_subject.face: eyes point toward the reflected active lens position / phone: active lens sits on the reflected phone back / mirror: eye lens relation agrees within the physical reflection
- 방향 관계: main_subject.face.eyes → look_at → phone.reflected_lens; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 눈·폰의 렌즈 위치를 담고 미세한 시선 차이는 판정 보류할 수 있다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 098. 거울 한쪽으로 치우치기 / Off-center mirror

- 의미·혼동 경계: 한쪽 배치와 우연한 몸 절단을 구분한다. 1/3은 제안값이지 필수 수치가 아니다.
- 관찰 구성: main_subject.body: reflection occupies one lateral part of the mirror / mirror: central mirror area remains partly empty / setting: reflected room fills the retained negative space
- 방향 관계: main_subject.reflection → lies_lateral_to → mirror.center; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 거울 경계·인물 실루엣·빈 공간을 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 099. 두 거울로 다른 면 보이기 / Double reflection

- 의미·혼동 경계: 반사 두 개를 두 사람으로 세지 않는다. 재귀 반사·합성·다중 노출은 별도 방식이다.
- 관찰 구성: mirror_pair: two distinct mirror planes have different orientations / main_subject.body: same actor appears in consistent views across both planes / phone: device and hand relationships remain compatible with the selected reflection paths
- 방향 관계: mirror_pair → reflect → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 두 물리 거울 경계와 각 반사의 대응 단서를 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 100. 상의 디테일 크롭 / Upper-outfit detail

- 의미·혼동 경계: 목걸이·칼라·소매 중 요청된 대상만 선택한다. 얼굴을 억지로 추가하지 않는다.
- 관찰 구성: composition: crop isolates the declared upper garment region / main_subject.wardrobe: collar necklace or sleeve details remain inside the crop / main_subject.face: face may lie wholly outside that chosen frame
- 방향 관계: image.crop → isolates → main_subject.upper_wardrobe; main_subject.wardrobe → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 의상 상세와 크롭 끝선을 명확히 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S11 — Apple Support — Take a selfie with your iPhone camera](https://support.apple.com/en-gb/guide/iphone/iph1b88429a6/ios), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)


## 11. 서서 찍는 전신 거울 셀카

### 101. 한쪽 다리에 체중 싣기 / Weight shift

- 의미·혼동 경계: 사진은 하중 수치를 측정하지 않는다. 뒤·앞 또는 인물 좌우 지지 다리를 명시한다.
- 관찰 구성: main_subject.leg: one leg has the principal visible support configuration / main_subject.leg: opposite knee stays comparatively relaxed / main_subject.body: pelvis and torso remain connected over the support base
- 방향 관계: main_subject.principal_support_leg → supports_configuration_of → main_subject.pelvis; main_subject.leg → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 골반·양 무릎·발바닥을 한 프레임에 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 102. 한 발 앞으로 / Staggered stance

- 의미·혼동 경계: 앞발 이동과 큰 런지 굴곡을 구분한다.
- 관찰 구성: main_subject.feet: one foot lies ahead of the other on the ground / main_subject.leg: rear leg retains the selected support role / main_subject.body: pelvis stays connected above the two leg paths
- 방향 관계: main_subject.foot_a → anterior_to → main_subject.foot_b; main_subject.feet → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 머리부터 양발과 바닥 접촉까지 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 103. 발목 교차 / Crossed ankles

- 의미·혼동 경계: 무릎 교차·정강이 교차와 구분한다.
- 관찰 구성: main_subject.legs: lower legs cross near the ankles / main_subject.feet: each foot continues from its own crossed shin / main_subject.body: standing base remains independently readable
- 방향 관계: main_subject.lower_leg_a → crosses_at_ankle → main_subject.lower_leg_b; main_subject.legs → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 교차점·양 발목·바닥 접촉을 담는다.
- 반영 판단: P0 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 104. 넓은 삼각형 / Triangle stance

- 의미·혼동 경계: The Triangle은 특정 가이드의 명칭이며 넓은 모든 자세의 표준 이름은 아니다.
- 관찰 구성: main_subject.feet: feet spread beyond a narrow hip width base / main_subject.leg: one foot stands slightly ahead of the other / main_subject.body: torso connects above the wide triangular base
- 방향 관계: main_subject.foot_a → laterally_separated_from → main_subject.foot_b; main_subject.feet → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 양발·골반·몸통과 거울의 기준선을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 105. 느슨한 S라인 / The Lean

- 의미·혼동 경계: 골반 측면 이동·요추 신전·카메라 롤을 구분한다. 특정 성적 분위기를 자동으로 추가하지 않는다.
- 관찰 구성: main_subject.feet: feet align in a close fore aft arrangement / main_subject.body: rear hip shifts laterally / main_subject.body: upper torso counterbalances above the shifted pelvis
- 방향 관계: main_subject.pelvis → laterally_offset_from → main_subject.shoulder_midpoint; main_subject.feet → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 어깨·골반·양발을 함께 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 106. 팔꿈치·무릎 각 만들기 / The Hook

- 의미·혼동 경계: The Hook은 가이드 용법으로 기록한다. 관절 각도 효과를 실제 몸통 길이 증가로 쓰지 않는다.
- 관찰 구성: main_subject.arm: free elbow projects away from the torso / main_subject.leg: one knee bends in the selected direction / main_subject.body: arm torso negative space remains visible
- 방향 관계: main_subject.elbow → separated_by_gap_from → main_subject.torso; main_subject.arm → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 팔꿈치·무릎·몸통 사이 빈 공간을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 107. 한쪽 뒤꿈치 들기 / Heel-lift stance

- 의미·혼동 경계: 뒤꿈치만 듦·발 전체 공중·발끝 포앵트를 구분한다.
- 관찰 구성: main_subject.foot: one heel clears the ground / main_subject.foot: same forefoot remains in ground contact / main_subject.leg: opposite leg retains the principal support configuration
- 방향 관계: main_subject.heel → clears → support_surface.floor; main_subject.foot → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 뒤꿈치 아래 틈·앞발 접점·반대 다리를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 108. 벽 기대기 / Wall lean

- 의미·혼동 경계: 벽 근처에 서 있음과 실제 벽 접촉을 구분한다.
- 관찰 구성: main_subject.body: selected shoulder or back contacts the wall / main_subject.feet: feet retain a visible ground base / wall: wall plane remains distinct from the actor silhouette
- 방향 관계: main_subject.shoulder_or_back → contacts → wall.plane; main_subject.body → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 접점·벽 수직선·양발을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 109. 옆모습 옷핏 / Side-profile outfit

- 의미·혼동 경계: 얼굴만 옆으로 돌린 것과 몸 옆면을 보이는 것을 구분한다.
- 관찰 구성: main_subject.body: torso turns nearly side on to the mirror / main_subject.wardrobe: garment side seam and depth contour remain visible / main_subject.arm: free arm does not fully occlude the garment side
- 방향 관계: main_subject.torso.side → faces → mirror.plane; main_subject.body → belongs_to → main_subject; main_subject.wardrobe → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 의상 옆선·몸통·다리 실루엣을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)

### 110. 뒤돌아 어깨 너머 보기 / Over-the-shoulder back view

- 의미·혼동 경계: 머리 회전과 몸통 회전을 분리한다. 목의 불가능한 회전을 만들지 않는다.
- 관찰 구성: main_subject.body: back and one lateral torso side face the mirror / main_subject.head: head turns over the selected shoulder / phone: phone remains beside the shoulder with one coherent grip
- 방향 관계: main_subject.torso.back → faces → mirror.plane; main_subject.body → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 등판·어깨·얼굴 일부·폰을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S14 — Emilia Petrarca / Anna Z. Gray — Mirror Selfie Like a Pro](https://emiliapetrarca.substack.com/p/how-to-take-a-mirror-selfie-like)


## 12. 앉기·쪼그리기 거울 셀카

### 111. 바닥에 편하게 다리 접기 / Cross-legged floor sit

- 의미·혼동 경계: 양발을 반대 허벅지에 올린 로터스를 자동으로 추가하지 않는다.
- 관찰 구성: main_subject.body: pelvis contacts the floor / main_subject.legs: folded shins cross in front of the pelvis / main_subject.feet: each foot connects to its own lower leg
- 방향 관계: main_subject.shin_a → crosses_before_pelvis_with → main_subject.shin_b; main_subject.body → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 골반 지지·무릎·발의 연결을 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 112. 양 무릎 높이 다르게 / Uneven-knee sit

- 의미·혼동 경계: 높낮이 차이와 카메라 기울기를 구분한다.
- 관찰 구성: main_subject.body: pelvis rests on the floor / main_subject.knees: two bent knees occupy different heights / main_subject.legs: each shin continues from its own knee toward its foot
- 방향 관계: main_subject.knee_a → higher_than → main_subject.knee_b; main_subject.body → belongs_to → main_subject; main_subject.knees → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 양 무릎·골반·발 경로를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 113. 한 무릎 세우기 / One-knee-up sit

- 의미·혼동 경계: 골반 지지 앉기와 한 무릎 지면 지지 하프니일을 구분한다.
- 관찰 구성: main_subject.body: pelvis rests on the floor or seat / main_subject.leg: one knee rises above the opposite folded leg / main_subject.arm: free forearm rests on the raised knee when selected
- 방향 관계: main_subject.knee_a → rises_above → main_subject.folded_leg_b; main_subject.body → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 골반·양 다리·팔꿈치 접점을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 114. 다리 대각선 뻗기 / Diagonal leg extension

- 의미·혼동 경계: 다리의 화면 대각선과 카메라 롤·벌린 스플릿을 구분한다.
- 관찰 구성: main_subject.body: pelvis remains seated on a visible support / main_subject.legs: selected legs extend along an image diagonal / main_subject.feet: each foot remains attached beyond its own knee
- 방향 관계: main_subject.legs → extend_diagonally_from → main_subject.pelvis; main_subject.body → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 요청된 발끝까지 담거나 크롭 한계를 명시한다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 115. 정면 쪼그려 앉기 / Front squat mirror

- 의미·혼동 경계: 스쿼트·바닥 앉기·무릎 꿇기를 지지점으로 구별한다.
- 관찰 구성: main_subject.legs: hips and knees flex into a low squat / main_subject.feet: two feet provide the grounded base / main_subject.body: pelvis stays above rather than on the floor
- 방향 관계: main_subject.feet → support_low_squat_configuration_of → main_subject.pelvis; main_subject.legs → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 양발·무릎·골반 아래 틈을 담는다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 116. 옆으로 쪼그려 앉기 / Side crouch

- 의미·혼동 경계: 사선 방향은 자세와 별도 축이다.
- 관찰 구성: main_subject.legs: knees flex into a low crouched support / main_subject.body: torso and knees face the selected oblique direction / main_subject.feet: feet remain the specified ground contacts
- 방향 관계: main_subject.bent_knees → lie_below_oblique → main_subject.torso; main_subject.legs → belongs_to → main_subject; main_subject.body → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 발·무릎·몸통의 단계적 배치를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 117. 의자 앞쪽에 앉기 / Chair-edge sit

- 의미·혼동 경계: 의자에 앉았다는 정보만으로 좌면 앞쪽 위치를 인정하지 않는다.
- 관찰 구성: main_subject.body: pelvis contacts the front region of the chair seat / chair: seat edge remains visible beside the thighs / main_subject.feet: feet retain independently stated support
- 방향 관계: main_subject.pelvis → rests_on → chair.seat_front; main_subject.body → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 좌면 접점·앞쪽 끝선·양 다리를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 118. 의자에서 다리 꼬기 / Seated leg cross

- 의미·혼동 경계: 무릎 위 교차·발목 위 교차·4자 앉기를 분리한다.
- 관찰 구성: main_subject.body: pelvis remains on the chair seat / main_subject.legs: one thigh crosses over the other near the knees / main_subject.feet: lower legs continue to their own feet
- 방향 관계: main_subject.thigh_a → crosses_above → main_subject.thigh_b; main_subject.body → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 골반·교차 무릎·양 정강이·발을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 119. 의자 뒤로 앉기 / Reverse-chair sit

- 의미·혼동 경계: 의자 방향 반전과 다리를 좌면 양쪽에 두는 스트래들을 동일시하지 않는다.
- 관찰 구성: main_subject.body: torso faces the chair backrest / main_subject.body: pelvis remains on the seat / main_subject.arms: forearms rest over the front facing backrest when selected
- 방향 관계: main_subject.torso → faces → chair.backrest; main_subject.body → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 등받이·좌면·몸 방향·각 다리를 담는다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 120. 소파 앞 바닥에 기대기 / Floor lean against sofa

- 의미·혼동 경계: 소파 좌면 앉기와 바닥 앉기+등 접촉을 구분한다.
- 관찰 구성: main_subject.body: pelvis rests on the floor in front of the sofa / main_subject.body: back contacts the sofa front or seat edge / main_subject.leg: one knee rises beside the supported torso
- 방향 관계: main_subject.back → contacts → sofa.front; main_subject.body → belongs_to → main_subject; main_subject.leg → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 바닥 골반 접점·소파 접점·다리를 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)


## 13. 누운 자세·휴식형 셀프포트레이트

### 121. 바로 누운 얼굴 셀카 / Supine selfie

- 의미·혼동 경계: 높은 카메라만으로 누운 자세를 인정하지 않는다.
- 관찰 구성: main_subject.body: back of torso rests on a support surface / main_subject.head: face points upward toward the chosen camera / main_subject.arm: one capture arm holds the camera above the face when handheld
- 방향 관계: main_subject.torso.back → rests_on → support_surface; main_subject.body → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 베개·지지면·목·얼굴의 눕는 관계를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 122. 옆으로 누워 베개 기대기 / Side-lying pillow pose

- 의미·혼동 경계: 엎드린 몸에서 고개만 옆으로 돌린 것과 구분한다.
- 관찰 구성: main_subject.body: lateral torso rests on the support surface / main_subject.head: head contacts a pillow beside that torso / main_subject.neck: head remains joined to the side oriented shoulders
- 방향 관계: main_subject.torso.side → rests_on → support_surface; main_subject.body → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.neck → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 옆면 지지·베개 접점·목 연결을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 123. 엎드려 팔꿈치 받치기 / Prone forearm support

- 의미·혼동 경계: 턱받침만으로 엎드림을 인정하지 않는다.
- 관찰 구성: main_subject.body: lower anterior torso remains on the surface / main_subject.arms: forearms support the chest from in front / main_subject.elbows: two elbows connect to separate shoulders
- 방향 관계: main_subject.forearms → contact_in_front_of → prone_supported_torso; main_subject.body → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject; main_subject.elbows → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 몸 앞면 지지와 양 전완·팔꿈치를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 124. 소파에 비스듬히 기대기 / Sofa recline

- 의미·혼동 경계: 등·옆면 지지를 선택해 기록한다. 소파라는 장소만으로 눕는 자세를 만들지 않는다.
- 관찰 구성: main_subject.body: side or back rests diagonally against the sofa / main_subject.arm: one arm contacts the cushion or armrest / main_subject.legs: leg paths remain distinct along the recline
- 방향 관계: main_subject.torso → reclines_against → sofa.support_surface; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 지지점·몸 대각선·다리를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 125. 침대 가장자리에 앉기 / Bed-edge portrait

- 의미·혼동 경계: 침대·성적 분위기·옷 수준은 서로 다른 축이다.
- 관찰 구성: main_subject.body: pelvis contacts the mattress near its edge / bed: edge runs beside the thighs rather than behind the whole body / main_subject.legs: legs descend or extend from the supported pelvis
- 방향 관계: main_subject.pelvis → rests_on → bed.mattress_edge; main_subject.body → belongs_to → main_subject; main_subject.legs → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 매트리스 끝선·좌면 접점·다리를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 126. 한 팔을 머리 뒤로 / Arm-behind-head recline

- 의미·혼동 경계: 양손 머리 뒤 기존 후보를 한 팔 요청에 그대로 적용하지 않는다.
- 관찰 구성: main_subject.arm: one bent arm reaches behind the head / main_subject.head: head rests beside or over that arm / main_subject.body: torso remains supported in the selected recline
- 방향 관계: main_subject.arm → reaches_behind → main_subject.head; main_subject.arm → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 머리·팔꿈치·어깨와 지지면을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 127. 무릎 끌어안기 / Curled-up self-hug

- 의미·혼동 경계: 팔 소유와 무릎 접촉을 명시한다. 내면의 불안·취약함을 자동 추론하지 않는다.
- 관찰 구성: main_subject.knees: bent knees approach the torso / main_subject.arms: arms wrap the selected knees / main_subject.body: pelvis or side retains visible support
- 방향 관계: main_subject.arms → wrap → main_subject.bent_knees; main_subject.knees → belongs_to → main_subject; main_subject.arms → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 얼굴·양팔·무릎·지지점을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 128. 담요 감싸기 / Blanket wrap

- 의미·혼동 경계: 재질·덮는 범위는 요청에 따른다. 연구가 의상이나 노출의 숨은 기본값을 추가하지 않는다.
- 관찰 구성: blanket: fabric wraps around the selected shoulder and torso region / main_subject.hand: one hand holds the visible blanket edge / main_subject.face: face remains above the selected fabric boundary
- 방향 관계: blanket → wraps → main_subject.shoulders_and_torso; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 담요 가장자리·잡는 손·얼굴을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 129. 엎드려 발을 뒤로 올리기 / Bent-leg prone pose

- 의미·혼동 경계: 발만 보이는 것으로 엎드림을 판정하지 않는다.
- 관찰 구성: main_subject.body: torso and thighs rest prone on the support / main_subject.knees: knees bend to lift the lower legs backward / main_subject.feet: feet clear the support behind the torso
- 방향 관계: main_subject.feet → clear_surface_behind → main_subject.prone_torso; main_subject.body → belongs_to → main_subject; main_subject.knees → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 얼굴·몸 앞면 지지·양 무릎·뒤쪽 발을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 130. 밤비 포즈 / Bambi pose

- 의미·혼동 경계: 기존 bare bambi hard activation 금지를 유지한다. 원문의 낮은 무릎 앉기 안을 pv_heel_sit로 검토하되 이름과 전체 포즈의 동등성을 확정하지 않는다.
- 관찰 구성: main_subject.knees: knees and shins rest on the support surface / main_subject.body: pelvis lowers toward the heels above folded shins / main_subject.feet: foot placement remains separately specified
- 방향 관계: main_subject.pelvis → lowers_toward → main_subject.heels; main_subject.knees → belongs_to → main_subject; main_subject.body → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 무릎·정강이·골반·뒤꿈치를 남긴다.
- 반영 판단: P0 · reuse_heel_sit_geometry_bambi_name_deferred
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography), [S20 — ELLE — What is Bambi Pose?](https://www.elle.com/beauty/a44609/what-is-bambi-pose/)


## 14. 일상 행동·소품을 이용한 셀카

### 131. 컵 너머 바라보기 / Over-the-cup selfie

- 의미·혼동 경계: 입 근처 컵·입술 접촉·실제 마시는 단계는 다르다.
- 관찰 구성: main_subject.hand: fingers grip the cup body or handle / cup: rim sits below the visible eyes near the mouth / main_subject.face: eyes look over the rim toward the selected target
- 방향 관계: cup.rim → lies_below → main_subject.face.eyes; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 컵 테두리·손 잡는 접점·눈을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 132. 음식 들어 보이기 / Food-in-hand selfie

- 의미·혼동 경계: 음식 보여주기와 입·도구 접촉을 분리한다. 음식 종류를 새로 선택하는 것은 별도 슬롯이다.
- 관찰 구성: main_subject.hand: hand holds the requested food or utensil / prop: food remains beside rather than wholly over the face / main_subject.face: face and prop occupy separate readable regions
- 방향 관계: main_subject.hand → holds → requested_food_or_utensil; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 음식·손·얼굴의 관계를 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 133. 책으로 얼굴 일부 가리기 / Book-frame portrait

- 의미·혼동 경계: 책을 들고 있다는 사실이 읽기·지능의 증거는 아니다. 한 손형·두 손형을 분리한다.
- 관찰 구성: main_subject.hands: hands grip the open book edges / book: book occludes the selected lower or lateral face region / main_subject.face: one or both eyes remain beyond the book boundary
- 방향 관계: book → occludes → main_subject.face.selected_region; main_subject.hands → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 책을 한 손으로 잡는 변형과 두 손으로 잡는 변형을 먼저 선택한다. 두 손을 쓰면 동일 인물의 촬영 손은 남지 않는다.
- 가시성: 책 가장자리·잡는 손·남은 얼굴을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 134. 꽃 향기 맡기 / Flower-to-face

- 의미·혼동 경계: 향기나 실제 후각 경험은 사진으로 증명하지 않는다. 코 옆 위치와 동작 단계만 기록한다.
- 관찰 구성: main_subject.hand: hand grips the flower stem / flower: flower head lies below the nose or beside the cheek / main_subject.face: nose or eyes orient toward the flower
- 방향 관계: flower.head → lies_below → main_subject.face.nose; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 줄기·잡는 손·꽃·코의 거리를 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 135. 메이크업 수정 중 / Makeup touch-up

- 의미·혼동 경계: 립·브러시·퍼프마다 대상·접촉 면이 다르므로 세 후보로 분리한다. 화장 상태 변경은 외형 잠금과 별도다.
- 관찰 구성: main_subject.hand: hand grips the selected cosmetic tool / tool: tool tip contacts its declared face target / main_subject.face: the target lip cheek or brow remains distinct from the tool
- 방향 관계: tool.tip → contacts → main_subject.face.declared_target; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 도구 끝·얼굴 접점·잡는 손을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 136. 양치 중 셀카 / Toothbrush selfie

- 의미·혼동 경계: 입가에 든 칫솔과 치아 접촉 양치 단계를 분리한다. 거품은 선택이다.
- 관찰 구성: main_subject.hand: hand grips the toothbrush handle / toothbrush: brush head sits at the actor mouth / main_subject.face: mouth and brush contact remain anatomically coherent
- 방향 관계: toothbrush.head → contacts_or_approaches → main_subject.face.mouth; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 칫솔 머리·입·손잡이·손을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 137. 한 걸음 움직이는 셀프포트레이트 / Walking-step portrait

- 의미·혼동 경계: 정지 한 장은 걷기 전체 궤적·속도를 입증하지 않는다.
- 관찰 구성: main_subject.legs: one leg advances in the selected step phase / main_subject.foot: foot contact or clearance matches that phase / main_subject.body: torso remains supported above the leg paths
- 방향 관계: main_subject.advancing_leg → lies_anterior_to → main_subject.support_leg; main_subject.legs → belongs_to → main_subject; main_subject.foot → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 양발·무릎·몸통의 단계 관계를 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 138. 머리카락이 흩날리는 순간 / Wind-in-hair

- 의미·혼동 경계: 바람의 원인·세기·동작 이력은 기록 문맥이다. 흐림만으로 바람을 판정하지 않는다.
- 관찰 구성: main_subject.hair: strands deflect laterally from their roots / main_subject.head: hair remains attached to the same head / main_subject.face: selected eyes and mouth remain visible between strands
- 방향 관계: main_subject.hair.strands → deflect_laterally_from → main_subject.hair.roots; main_subject.hair → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 가닥 뿌리·흩날림 방향·얼굴을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 139. 돌아보는 중간 / Mid-turn portrait

- 의미·혼동 경계: 돌아봄의 한 단계와 실제 회전 이력을 구분한다.
- 관찰 구성: main_subject.body: torso faces an oblique direction / main_subject.head: head turns toward the selected camera target / main_subject.hair: hair and shoulders retain the selected intermediate configuration
- 방향 관계: main_subject.head.yaw → differs_from → main_subject.shoulder_yaw; main_subject.body → belongs_to → main_subject; main_subject.head → belongs_to → main_subject; main_subject.hair → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 머리·어깨·몸통의 서로 다른 방향을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 140. 주차한 차 안 창가 셀카 / Parked-car window selfie

- 의미·혼동 경계: 운전 중/정차 여부는 외형만으로 확정하지 않는다. 주차 맥락은 명시된 장면이며 브랜드·개인정보는 필수 요소가 아니다.
- 관찰 구성: main_subject.body: actor sits inside a vehicle cabin / window: side window lies beside the actor face / camera: capture device faces the actor within the declared parked scene
- 방향 관계: vehicle.side_window → lies_beside → main_subject.face; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 차창·좌석·얼굴·빛 방향을 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)


## 15. 두 사람·그룹·포토부스 셀카

### 141. 얼굴 나란히 / Same-plane duo

- 의미·혼동 경계: 같은 평면은 완전히 같은 얼굴 크기·실제 친밀도의 요구가 아니다.
- 관찰 구성: main_subject.face: first face occupies a similar depth to the second / partner_subject.face: second face remains separately visible / composition: two face sizes and overlap agree with the selected camera position
- 방향 관계: main_subject.face → at_similar_depth_to → partner_subject.face; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 두 얼굴·어깨 연결과 겹침을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 142. 머리 기대기 / Head lean

- 의미·혼동 경계: 누가 누구에게 기대는지 방향을 기록한다.
- 관찰 구성: main_subject.head: first head contacts the partner shoulder or head side / partner_subject.body: receiving shoulder or head remains distinct / main_subject.neck: leaning head stays attached to its own neck
- 방향 관계: main_subject.head → rests_on → partner_subject.shoulder; main_subject.head → belongs_to → main_subject; main_subject.neck → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 두 얼굴·접점·각 목의 소유를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 143. 함께 만드는 하트 / Shared heart

- 의미·혼동 경계: 각자 한 손씩이면 다른 손으로 폰을 잡을 수 있다. 원문의 고정 카메라 권고를 양손 불가능의 일반 규칙으로 쓰지 않는다.
- 관찰 구성: main_subject.hand: one actor hand forms one heart half / partner_subject.hand: another actor hand forms the other half / hands_pair: two owned halves meet around one heart shaped gap
- 방향 관계: main_subject.hand → meets → partner_subject.hand; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 두 사람 각자 한 손의 하트라면 참가자 한 명의 다른 손으로 폰 촬영이 가능하다.
- 가시성: 하트 접점·양손 손목·두 인물 얼굴을 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 144. 뒤에서 감싸기 / Back-hug portrait

- 의미·혼동 경계: 앞사람 손과 뒤사람 팔을 바꾸지 않는다. 관계·동의·성적 분위기는 포옹 외형으로 확정하지 않는다.
- 관찰 구성: partner_subject.body: one actor stands behind the other / partner_subject.arms: rear actor arms wrap the front actor torso / main_subject.face: front and rear faces remain laterally distinct
- 방향 관계: partner_subject.arms → wrap → main_subject.torso; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 두 얼굴·각 팔 소유·감싸는 접촉을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 145. 위에서 모이는 원형 / Overhead group circle

- 의미·혼동 경계: 인물 수를 요청대로 고정한다. 원형 배치와 같은 크기 얼굴은 독립이다.
- 관찰 구성: actor_group: requested faces gather below one upper camera / camera: lens points downward toward the group center / actor_group: each face remains distinct around that center
- 방향 관계: requested_actor_group.faces → gather_below → camera
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 모든 얼굴·정수리·프레임 끝 여백을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 146. 높낮이 삼각형 / Staggered group triangle

- 의미·혼동 경계: 각 인물 높이와 지지점을 따로 기록한다.
- 관찰 구성: actor_group: requested heads occupy distinct heights / actor_group: head positions form the selected triangle silhouette / actor_group: each actor retains a separate grounded or seated support
- 방향 관계: requested_actor_group.heads → form_height_triangle_in → image
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 모든 얼굴과 각 지지 자세가 확인될 범위를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 147. 앞뒤 거울 그룹 / Layered mirror group

- 의미·혼동 경계: 실제 여러 사람과 한 사람의 재귀 반사를 구분한다. 기존 단일 성인 거울 프로필의 인물 수 가정을 확대하지 않는다.
- 관찰 구성: main_subject.hand: front actor grips the capture phone in the reflection / actor_group: other reflected faces appear at separate rear positions / mirror: all reflections share a coherent physical mirror space
- 방향 관계: mirror → reflects → requested_actor_group; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 거울 경계·촬영자 손·모든 얼굴을 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 148. 네 컷 표정 변화 / Four-cut sequence

- 의미·혼동 경계: 한 장의 표정 네 개나 복제 인물로 대체하지 않는다. format·count와 컷별 소유를 검토한다.
- 관찰 구성: composition: four distinct panels preserve the declared actor identity / main_subject.face: facial or hand configurations differ by panel / composition: similar framing links the ordered panels
- 방향 관계: four_panels → preserve_identity_of → declared_actor; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 각 컷의 얼굴·손·패널 경계를 별도로 심사한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 149. 같은 표정·한 명만 다른 표정 / Reaction contrast

- 의미·혼동 경계: 한 사람만 다른 표정을 갖는 분포를 보존한다. 집단 감정·사회 관계를 추론하지 않는다.
- 관찰 구성: actor_group: most requested faces keep one common configuration / designated_actor.face: one designated face shows the contrasting expression / actor_group: each face remains connected to its own body
- 방향 관계: designated_actor.expression → differs_from → actor_group.expression
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 모든 얼굴을 표정 비교 가능한 크기로 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)

### 150. 반려동물 눈높이 / Pet-level selfie

- 의미·혼동 경계: 동물 종·인물 수·실제 반려 관계를 후보가 새로 추가하지 않는다.
- 관찰 구성: main_subject.body: human lowers beside the already requested animal / animal_subject.head: animal eyes lie near the human face height / camera: lens height follows the declared animal eye plane
- 방향 관계: main_subject.face → at_height_of → animal_subject.face; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 사람·동물 얼굴과 각각의 몸 연결을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors)


## 16. 성인 패션·부두아·관능적 셀카

### 151. 오프숄더 어깨선 / Off-shoulder portrait

- 의미·혼동 경계: 오프숄더 의상과 어깨 방향을 별도 슬롯으로 조합한다. 옷·노출을 후보가 변경하지 않는다.
- 관찰 구성: main_subject.wardrobe: existing off shoulder neckline reveals the selected shoulder / main_subject.body: that shoulder turns slightly toward the lens / main_subject.head: neck and face continue from the shoulder line
- 방향 관계: main_subject.shoulder → lies_above → existing_off_shoulder_neckline; main_subject.wardrobe → belongs_to → main_subject; main_subject.body → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 의상 가장자리·어깨·목·얼굴을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 152. 등 라인·백리스 / Open-back portrait

- 의미·혼동 경계: 백리스 형태와 몸 회전·머리카락 치우기를 구분한다.
- 관찰 구성: main_subject.body: back faces the selected camera direction / main_subject.wardrobe: existing garment opening exposes the stated back region / main_subject.head: head turns with a coherent neck and shoulder relation
- 방향 관계: existing_garment.back_opening → frames → main_subject.back; main_subject.body → belongs_to → main_subject; main_subject.wardrobe → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 등판·의상 경계·어깨·얼굴 일부를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 153. 쇄골 주변 손동작 / Collarbone touch

- 의미·혼동 경계: 쇄골 접촉·목 움켜쥠·목걸이 잡기를 다른 관계로 둔다.
- 관찰 구성: main_subject.hand: fingertips touch the upper chest near the clavicle / main_subject.body: clavicle or neckline landmarks locate the touch / main_subject.arm: hand connects to its own wrist below the neck
- 방향 관계: main_subject.hand → touches → main_subject.clavicle; main_subject.hand → belongs_to → main_subject; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 쇄골 기준·손끝 접점·목의 여유를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 154. 뒤태 셀카 / Belfie

- 의미·혼동 경계: belfie는 뒤태 중심 명칭이다. 특정 노출·의상·몸매·한 자세를 강제하지 않는다.
- 관찰 구성: main_subject.body: rear torso hip and leg contours face the selected view / composition: rear lower body occupies the chosen dominant frame region / camera: capture mode remains consistent with mirror or fixed self portrait
- 방향 관계: main_subject.rear_body_region → dominates → selected_crop; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 등·허리·골반·다리의 연결과 요청된 촬영 방식을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography), [S26 — SELF — Belfie example](https://www.self.com/story/lea-michele-jlo-selfie)

### 155. 옆선과 체중 이동 / Side-curve pose

- 의미·혼동 경계: 곡선 포즈와 실제 신체 곡률·체형을 구별한다.
- 관찰 구성: main_subject.body: pelvis shifts over one supported leg / main_subject.body: shoulder and hip directions differ coherently / main_subject.arm: near arm leaves a visible gap beside the waist
- 방향 관계: main_subject.pelvis → offset_over → main_subject.support_leg; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 어깨·허리·골반·양발을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 156. 팔을 올린 스트레치 / Arms-up stretch

- 의미·혼동 경계: 손목 교차형과 머리 뒤형을 하나의 필수 자세로 합치지 않는다.
- 관찰 구성: main_subject.arms: both arms rise above the head / main_subject.hands: wrists cross or hands rest behind the head in separately chosen variants / main_subject.body: shoulders and torso remain continuous below the raised arms
- 방향 관계: main_subject.arms → rise_above → main_subject.head; main_subject.arms → belongs_to → main_subject; main_subject.hands → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 손끝부터 양 팔꿈치·몸통까지 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 157. 로브·타월 랩 / Robe or towel-wrap portrait

- 의미·혼동 경계: 로브·타월 재료와 여밈 구조를 분리한다. 덮는 범위를 연구 기본값으로 변경하지 않는다.
- 관찰 구성: main_subject.wardrobe: existing robe or towel wraps the specified torso region / main_subject.hand: one hand grips the wrap edge / main_subject.body: coverage boundary remains the declared one
- 방향 관계: main_subject.hand → grips → existing_robe_or_towel_edge; main_subject.wardrobe → belongs_to → main_subject; main_subject.hand → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 직물 겹침·손 잡는 접점·선택된 얼굴 범위를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 158. 란제리·수영복 패션 리클라인 / Lingerie or swimwear recline

- 의미·혼동 경계: 란제리·수영복을 한 의상으로 합치지 않는다. 성인 패션 맥락을 보존하며 지지 자세 자체는 장르 중립이다.
- 관찰 구성: main_subject.body: side torso reclines on a declared surface / main_subject.arm: one arm supports the upper body / main_subject.knees: two knees occupy separately stated positions
- 방향 관계: main_subject.arm → supports_configuration_of → main_subject.reclining_torso; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject; main_subject.knees → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 의상·팔 지지점·양 무릎·몸 연결을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 159. 창가 옆선 실루엣 / Window-side silhouette

- 의미·혼동 경계: 역광 실루엣·단순 암부·옆창 얼굴 조명을 구별한다.
- 관찰 구성: window: bright background source lies behind the side oriented actor / main_subject.body: body side contour remains darker than that background / main_subject.arm: arm torso gap creates readable negative space
- 방향 관계: bright_window → lies_behind → main_subject.side_silhouette; main_subject.body → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 창 또는 광원 위치와 몸 윤곽·팔 틈을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)

### 160. 아랫입술 가볍게 물기 / Subtle lip-bite portrait

- 의미·혼동 경계: 입술 벌림·입술 말아 넣기·아랫입술 물기를 구분한다. 의도·관능은 요청 문맥으로 둔다.
- 관찰 구성: main_subject.face: upper teeth contact the lower lip / main_subject.face: the bitten lower lip retains a coherent small fold / main_subject.face: eye target remains independently specified
- 방향 관계: main_subject.face.upper_teeth → contact → main_subject.face.lower_lip; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 치아·아랫입술 접점과 눈을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S09 — Neil van Niekerk — Pose the hands, asymmetry](https://neilvn.com/tangents/posing-tips-pose-hands-asymmetry/), [S10 — Lara Jade — Self portrait photography](https://www.larajadeeducation.com/blogposts/top-tips-for-self-portrait-photography)


## 17. 반항·도발·코믹·액션 연출

### 161. 팔짱 낀 정면 / Crossed-arm stance

- 의미·혼동 경계: 팔 교차·손 깍지·손목 교차를 분리한다. 방어적 성격을 자동 추론하지 않는다.
- 관찰 구성: main_subject.arms: two forearms cross before the torso / main_subject.hands: each hand belongs to its own crossed arm / main_subject.body: shoulders retain a separate relaxed or chosen height
- 방향 관계: main_subject.forearm_a → crosses_before_torso_with → main_subject.forearm_b; main_subject.arms → belongs_to → main_subject; main_subject.hands → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 팔꿈치·전완·손 소유를 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 162. 주머니 손·넓은 자세 / Hands-in-pocket stance

- 의미·혼동 경계: 폰 잡는 손과 주머니 손을 겹치게 하지 않는다. 엄지만 걸기와 손 전체 넣기를 분리한다.
- 관찰 구성: main_subject.hand: selected free hand enters an existing pocket opening / main_subject.wardrobe: pocket edge remains visible around the hand / main_subject.feet: feet retain the separately requested stance
- 방향 관계: main_subject.free_hand → enters → existing_pocket_opening; main_subject.hand → belongs_to → main_subject; main_subject.wardrobe → belongs_to → main_subject; main_subject.feet → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 포켓 입구·손목과 요청된 양발을 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 163. 근육 포즈 / Double-biceps pose

- 의미·혼동 경계: 근육을 보여주는 포즈와 실제 근육량·체형을 구별한다.
- 관찰 구성: main_subject.arms: both upper arms rise laterally / main_subject.elbows: both elbows bend with forearms raised / main_subject.hands: two fists remain connected beyond their own elbows
- 방향 관계: main_subject.forearms → rise_above → main_subject.bent_elbows; main_subject.arms → belongs_to → main_subject; main_subject.elbows → belongs_to → main_subject; main_subject.hands → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 양 어깨·팔꿈치·주먹을 모두 담는다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 164. 복서 가드 / Boxer guard

- 의미·혼동 경계: 가드 자세를 실제 타격·부상·폭력 사건으로 확장하지 않는다.
- 관찰 구성: main_subject.hands: two fists stand before the face sides / main_subject.elbows: elbows stay nearer the torso than the fists / main_subject.face: eyes remain visible between the guard hands
- 방향 관계: main_subject.fists → lie_before_opposite_sides_of → main_subject.face; main_subject.hands → belongs_to → main_subject; main_subject.elbows → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 한 인물의 양손이 포즈에 점유된다. 같은 손으로 폰을 쥐게 하지 않는다. 장치가 화면에 반드시 보여야 하는 것은 아니다.
- 가시성: 주먹·눈·팔꿈치·몸통을 남긴다.
- 반영 판단: P1 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 165. 주먹을 앞으로 멈추기 / Foreshortened punch pose

- 의미·혼동 경계: 정지 주먹의 단축 원근과 실제 타격·접촉·결과를 구별한다.
- 관찰 구성: main_subject.hand: one fist lies closer to the lens than the face / main_subject.arm: arm extends in depth from the same shoulder / main_subject.hand: other hand stays in its separately declared position
- 방향 관계: main_subject.fist → nearer_than → main_subject.face; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 주먹·전완·어깨·얼굴의 깊이 순서를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 166. 손가락 총 / Finger-gun pose

- 의미·혼동 경계: 빈손 모양을 실제 총·총격·자해 행위로 바꾸지 않는다.
- 관찰 구성: main_subject.hand: index finger extends in the selected direction / main_subject.hand: thumb rises away from the folded digits / main_subject.arm: empty hand remains attached to one wrist
- 방향 관계: main_subject.hand.index → extends_beside_raised → main_subject.hand.thumb; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 검지·엄지·접힌 손가락과 손목을 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 167. 가운데손가락 제스처 / Middle-finger pose

- 의미·혼동 경계: 중지 소유와 양옆 접힌 손가락을 확인한다. 욕설 대상이나 폭력 의도는 별도 문맥이다.
- 관찰 구성: main_subject.hand: middle finger extends from the central palm / main_subject.hand: other fingers fold distinctly around its base / main_subject.arm: gesture hand connects to the actor own wrist
- 방향 관계: main_subject.hand.middle_finger → extends_between → main_subject.hand.folded_neighbor_digits; main_subject.hand → belongs_to → main_subject; main_subject.arm → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 손 전체가 판별 가능한 크기로 보이게 한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 168. 록 핸드사인 / Rock horns

- 의미·혼동 경계: 엄지·새끼의 샤카 및 엄지까지 펴는 ILY형과 구별한다. 음악 취향·종교 해석을 자동 추가하지 않는다.
- 관찰 구성: main_subject.hand: index and little fingers extend / main_subject.hand: middle and ring fingers remain folded / main_subject.hand: thumb remains in the selected folded or restraining position
- 방향 관계: main_subject.hand.index_and_little → extend_beside → main_subject.hand.folded_middle_and_ring; main_subject.hand → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 펴고 접힌 손가락 네 개와 엄지 위치를 확인한다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 169. 으르렁·분노 연기 / Snarl portrait

- 의미·혼동 경계: 분노 연출과 실제 감정·폭력 의도를 분리한다. 눈썹·윗입술·치아를 별도 조합한다.
- 관찰 구성: main_subject.face: brow inner ends draw together / main_subject.face: one or both upper lip regions lift / main_subject.face: teeth become partly visible beneath the raised lip
- 방향 관계: main_subject.face.upper_lip → lifts_to_expose → main_subject.face.teeth; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈썹·코·윗입술·치아를 담는다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)

### 170. 공포·빌런 응시 / Horror or villain stare

- 의미·혼동 경계: 공포·빌런은 장르·역할 맥락이다. 흉터·무기·폭력·정체성을 자동 추가하지 않는다.
- 관찰 구성: main_subject.head: chin pitches slightly downward / main_subject.face: eyes point toward the declared lens target / lighting: selected partial illumination leaves the requested eyes readable
- 방향 관계: main_subject.face.eye_axes → point_toward → camera.active_lens; main_subject.head → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 눈·턱·선택된 손과 조명 경계를 남긴다.
- 반영 판단: P1 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S17 — Nikon — Retro ’90s action portraiture](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/how-to-photograph-retro-90s-magazine-action-portraiture)


## 18. 빛·반사·흔들림을 활용하는 셀카

### 171. 창 정면의 부드러운 셀카 / Window-facing portrait

- 의미·혼동 경계: 창 존재·창 방향·광원의 겉보기 크기·그림자 부드러움을 분리한다.
- 관찰 구성: window: broad window source faces the actor front / main_subject.face: face planes show soft light shadow transitions / main_subject.body: body orientation remains independent of the source direction
- 방향 관계: window.source → illuminates_front_of → main_subject.face; main_subject.face → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 얼굴 명암과 창 방향을 평가할 단서를 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 172. 옆창 사선광 / Side-window portrait

- 의미·혼동 경계: 얼굴 사선 방향과 광원 사선 방향을 동일시하지 않는다.
- 관찰 구성: window: window lies laterally beside the actor / main_subject.face: window facing face planes are brighter than opposite planes / main_subject.head: face turn remains independent of the source placement
- 방향 관계: window.source → illuminates_side_of → main_subject.face; main_subject.face → belongs_to → main_subject; main_subject.head → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 양 얼굴 면과 그림자 전이를 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 173. 반쪽 조명 / Split-light portrait

- 의미·혼동 경계: 조명 반쪽·손 가림 반쪽·크롭 반쪽을 구별한다. 어두운 눈의 가시성은 별도다.
- 관찰 구성: light_source: dominant source lies to one side of the face / main_subject.face: one face half is brighter than the other / main_subject.face: the light boundary runs near the central face plane
- 방향 관계: main_subject.face.lit_half → brighter_than → main_subject.face.shadow_half; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 밝은 면·어두운 면·명암 경계를 남긴다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 174. 머리카락 역광 / Backlit hair portrait

- 의미·혼동 경계: 밝은 헤어 윤곽·머리 색·전경 조명은 별도다.
- 관찰 구성: light_source: source lies behind or rear oblique to the actor / main_subject.hair: hair edges receive bright rim or transmitted light / main_subject.face: face exposure is independently selected
- 방향 관계: rear_light_source → illuminates_edges_of → main_subject.hair; main_subject.hair → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 머리 가장자리 빛과 광원 방향·얼굴을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 175. 플래시 거울 셀카 / Flash mirror selfie

- 의미·혼동 경계: 거울 정반사 번쩍임·얼굴 직광·렌즈 플레어·센서 블룸을 구분한다. 점 하나만으로 플래시 원인을 확정하지 않는다.
- 관찰 구성: phone: visible or reflected device flash lies in the mirror scene / mirror: specular flash reflection occupies a declared image region / main_subject.face: face lies beside or partly behind that reflection as requested
- 방향 관계: mirror → reflects → phone.flash; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 물리 거울·폰 그립·가림·시선 경로가 일관되어야 한다. 양손 포즈와 결합 시 촬영 장치를 별도 지지한다.
- 가시성: 폰·거울 기준·플래시 반사 위치와 얼굴을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 176. 움직임이 남는 셀카 / Motion-blur self-portrait

- 의미·혼동 경계: 국소 피사체 움직임·전체 카메라 흔들림·초점 흐림·합성 복제를 별도 변형으로 둔다.
- 관찰 구성: main_subject.hand: selected moving region shows a directional trail / setting: stationary reference edges remain comparatively clear in the local blur variant / main_subject.body: actor anatomy remains continuous beneath the selected blur
- 방향 관계: main_subject.moving_region_trail → contrasts_with → stationary_scene_edges; main_subject.hand → belongs_to → main_subject; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 선명한 기준과 흐린 부위를 같은 프레임에 남긴다.
- 반영 판단: P0 · compose_existing_components
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 177. 블라인드·창틀 그림자 / Patterned-shadow portrait

- 의미·혼동 경계: 투영 그림자·화장 줄무늬·직물 줄무늬를 구분한다.
- 관찰 구성: shadow_pattern: parallel shadow bands cross the selected face or body region / main_subject.body: bands conform to the receiving body surface / window_occluder: a declared blind or frame blocks the incident light
- 방향 관계: window_occluder → casts_bands_on → main_subject.receiving_surface; main_subject.body → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 줄무늬의 명암 전이·표면 굴곡·빛 방향을 담는다.
- 반영 판단: P1 · literal_research_then_inventory_review
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 178. 작은 손거울 속 얼굴 / Hand-mirror portrait

- 의미·혼동 경계: 실제 손거울·폰 화면·얼굴 사진·다른 사람을 구분한다.
- 관찰 구성: main_subject.hand: hand grips a bounded small mirror / mirror: mirror plane contains a partial reflection of the same face / main_subject.face: real and reflected face regions obey the selected viewing geometry
- 방향 관계: hand_mirror → reflects → main_subject.face; main_subject.hand → belongs_to → main_subject; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 거울 경계·손잡이 접점·반사 얼굴과 실제 얼굴의 대응을 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 179. 유리창 반사 겹치기 / Window-reflection portrait

- 의미·혼동 경계: 유리의 반사+투과·두 거울 반사·소프트웨어 다중 노출은 다르다.
- 관찰 구성: window: one glass plane transmits the exterior scene / main_subject.face: same actor reflection overlays that transmitted scene / composition: reflection and exterior retain distinct depth and brightness cues
- 방향 관계: glass_plane → overlays_reflection_on → transmitted_exterior; main_subject.face → belongs_to → main_subject
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 유리 경계·겹친 얼굴·창밖 장면을 함께 담는다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)

### 180. 그림자 셀프포트레이트 / Shadow self-portrait

- 의미·혼동 경계: 그림자 자체와 역광의 실제 인물 실루엣을 구분한다. 그림자의 크기를 인물 신체 크기로 읽지 않는다.
- 관찰 구성: light_source: source projects the actor shadow onto a receiving plane / shadow: connected head torso and limb silhouette appears on that plane / support_surface: wall or floor retains a visible shadow receiving surface
- 방향 관계: light_source → casts_shadow_on → support_surface
- 촬영·손 역할: 포즈에 쓰는 손·소품을 잡는 손·지지 손·폰을 잡는 손을 인물별로 배정한다. 손 하나의 겸용은 실제 동일 접점에서 가능한 경우만 허용한다.
- 가시성: 그림자 윤곽·받는 면·빛 방향의 단서를 남긴다.
- 반영 판단: P0 · new_or_specialized_draft
- 출처 범위: [S25 — 셀카 포즈 조사 — 사용자 지정 ChatGPT 대화](https://chatgpt.com/c/6ac663d1-765c-83ee-b316-9e5c0d03db8c), [S01 — Canon — 8 tips for stunning self-portraits](https://www.canon-europe.com/get-inspired/tips-and-techniques/self-portrait-tips/), [S02 — Canon Australia — Distortion](https://www.canon.com.au/get-inspired/glossary/distortion), [S12 — OpenStax — Image Formation by Mirrors](https://openstax.org/books/college-physics-ap-courses-2e/pages/25-7-image-formation-by-mirrors), [S18 — Canon EOS R8 Manual — Panning Mode](https://cam.start.canon/en/C013/manual/html/UG-02_BasicShooting_0110.html)


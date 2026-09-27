# 인물 사진 구도: 시각 의미·후보팩 보강 리서치

조사일: 2026-09-27. 참조 대화: 「인물 사진 구도 조사」(6ab8c04c-6820-83ee-9d4c-6b4241474930).

## 1. 결론과 산출물의 범위

가장 필요한 보강은 구도 이름의 추가보다 **인물·카메라·몸·시선·전경·반사면·초점·프레임 사이의 관계를 분리하고, 같은 사진에서 그 관계가 함께 보이는지 판정하는 데이터**이다. 원 대화의 30개 구도, 재사용할 12개 구성 원리, 5개 촬영 표현, 3개 사진 묶음을 총 50개 연구 레코드로 정리했다. 25개 출처는 열람 방식과 확인 범위를 함께 기록했다.

이번 결과는 연구와 적용 가능한 초안이다. 런타임 사전·레지스트리·인덱스·생성기는 변경하지 않았다. 연구 폴더 안의 `.proposed.json`은 현재 컴파일러에 대조하는 검토용 데이터이며 자동 로딩되지 않는다. 기존 Y2K 변경, 미완료 인덱스 파일, 다른 출력은 보존한다. 실제 이미지 생성·픽셀 통과·사용자 매력 판단·후보팩 효과는 이 턴의 검증 범위가 아니다.

| 파일 | 용도 |
|---|---|
| `source-conversation.json` | 조사한 원 대화의 조회 스냅샷; 이전 인용 마커는 새 출처로 취급하지 않음 |
| `sources.json` | 출처별 URL·확인일·사실 범위·열람 제한 |
| `concept-catalog.json` | 50개 개념의 구성요소·소유자·차원·혼동 경계·적용안 |
| `coverage-audit.json` | 현재 합쳐진 데이터의 개수·기존 ID 대조·입력 파일 SHA-256 |
| `candidate-extension.proposed.json` | 42개 단일사진 개념의 관계 후보와 선택 번들 초안 |
| `visual-profiles.proposed.json` | 기존 개념만으로 부족한 16개 관계의 좁은 의무 초안 |
| `candidate-source-map.json` | 후보와 출처의 유지보수 연결; 런타임에 출처 URL을 노출하지 않음 |
| `keyword-coverage.csv` | 한국어·영어 키워드별 범위와 재사용 여부 |
| `regression-cases.jsonl` | 개발용 정의·넓은 라벨·한국어 설명·반례·변이 사례 |
| `qualification-plan.json` | 이후 독립 렌더와 동일 이미지 픽셀 검증 계획 |
| `verification.json` | 실제 실행한 구조·좁은 활성화·번들 경계 검사 결과 |

## 2. 출처가 말하는 사실과 이번 설계 제안을 구분한다

촬영 범위가 얼굴·행동·환경의 비중을 바꾸고, 눈 초점과 단순한 배경이 얼굴 전달에 도움이 된다는 점은 촬영 자료에서 확인했다. 몸과 머리의 방향을 분리하는 예시도 확인된다. [Canon 프레이밍](https://asia.canon/en/support/8200023500), [Nikon 눈 초점](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [Nikon 몸과 머리 방향](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits).

전경 흐림, 거울, 프리즘, 고보, 움직임 궤적은 서로 다른 공간·광학 원리를 가진다. 프리즘은 굴절·색 분산 등, 고보는 광원 패턴, 움직임 흐림은 노출 시간 중 위치 변화에 관한 자료를 바탕으로 분리했다. [Adobe 프리즘](https://www.adobe.com/creativecloud/photography/technique/prism.html), [Westcott 고보](https://westcottu.com/creating-a-sense-of-environment-with-the-optical-spot-by-lindsay-adler), [Adobe 모션 블러](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html).

평면거울의 얼굴상은 거울 뒤의 가상상에 해당한다. 카메라에서 거울을 거쳐 인물까지의 광학 경로와 표면까지 거리를 분리해야 한다. 단순 정면 배치에서는 경로를 `카메라→거울 + 거울→인물`로 이해할 수 있으며, 비스듬한 배치는 실제 반사 광선을 기준으로 판단한다. 따라서 거울 테두리·얼룩 초점과 반사 얼굴 초점은 같은 조건이 아니다. 곡면 거울에는 이 평면거울 모델을 그대로 적용하지 않는다. [OpenStax 평면거울](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors).

다음은 이번 목적을 위한 자체 설계 판단이다: 얼굴이 중요한 요청에는 살아남아야 할 표정 영역을 선언하고, 강한 장치의 범위를 제한하며, 장치와 주인공의 우선순위를 함께 검토한다. 이는 모든 인물사진에 눈맞춤·양쪽 눈·예쁜 얼굴·단순 배경을 강제하는 규칙이 아니다. 옆얼굴·눈 감음·완전 얼굴 가림·의도적 흐림·작은 환경 인물을 명시한 요청은 그대로 보존한다. 특정 카메라 수치·얼굴 면적 비율·기울기 각도를 보편적 통과 기준으로 만들 근거는 확보하지 못했다.

## 3. 용어를 분해할 최소 의미 축

`출력 범위 → 촬영 범위 → 카메라 높이/피치/롤 → 얼굴 방향 → 몸통 방향 → 눈의 목표 → 몸의 지지 → 행동/순간 → 전경 소유자 → 반사면 종류 → 초점 소유자 → 가림 범위 → 배경 위계 → 후처리/질감`

| 혼동하기 쉬운 표현 | 별도로 보존할 의미 |
|---|---|
| three-quarter view / three-quarter-length | 얼굴·몸의 방향 / 몸을 포함하는 길이. 단독 three-quarter가 핵심이면 먼저 의미를 확인 |
| own over-the-shoulder glance / OTS shot | 본인의 몸과 고개 회전 / 타인의 어깨와 주인공 사이 카메라 관계 |
| diagonal body / Dutch roll | 몸의 축 / 장면 기준선의 공통 기울기 |
| negative space / looking room / headroom / move room | 저정보 영역 / 시선 벡터 앞 / 머리 위 / 이동 벡터 앞 |
| foreground bokeh / background bokeh / motion blur | 가까운 물체의 초점 이탈 / 먼 배경의 초점 이탈 / 노출 중 움직임 |
| mirror / window glass / prism | 반사 가상상 / 투과와 반사의 중첩 / 굴절·분산·반사 효과 |
| candid / off-camera gaze / mid-action | 촬영 방식 / 눈의 방향 / 화면에서 보이는 사건 단계 |
| photo dump / diptych / triptych / sequence | 선택·게시 묶음 / 두 이미지 / 세 이미지 / 명시적 시간 순서 |

이 분리는 원 대화에 명시된 혼동 경계를 보존한 것이다. 영상 OTS와 Dutch angle의 구조는 정지사진에 필요한 공간 관계만 사용했다. [Adobe OTS](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html), [Adobe Dutch angle](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html).

## 4. 현재 저장소 데이터와 보강 경계

조회 시 합쳐진 데이터는 **8,230개 후보 항목·407개 번들·944개 시각 프로필**이다. 이 숫자는 전체 사전의 크기이며 인물 구도 30개가 충분히 검증되었다는 수치가 아니다. 각 파일의 해시를 `coverage-audit.json`에 고정했다.

재사용 우선 영역은 `look_motion_room_direction_relation`, `subject_field_negative_space_relation`, `frame_within_frame_boundary_relation`, `companion_viewpoint_everyday_candid`, `mep_in_between`, `mep_graphic_pose`, `mep_gaze_target`, `mep_environment_relation`, `pr_environmental_portrait_subject_place`, `pr_casual_crop_subject_legibility`, `rb_glass_reflection_transmission`이다.

다만 기존 계약에는 추가 조건이 있다. 동행자 프로필은 생활 행동과 반응, 프레임 속 프레임은 세 면의 둘레, overhead 프로필은 가까운 위쪽 시점과 바닥·원근 등의 증거를 요구한다. 맞은편 테이블·창틀 한쪽·앉은 고각을 요청했다고 이 모든 조건을 자동 강제하면 원래 의미가 바뀐다. 미러 셀피는 휴대폰과 손의 접촉까지 요구하므로 일반 거울 인물사진에 쓰면 안 된다. 가시 얼굴을 가리는 기존 감성 사진 계약도 기본 얼굴 우선 목표에 무조건 섞지 않는다.

신규 관계 초안은 어깨–머리 분리, 맞은편 테이블 위계, 앉은 삼각 점, 지지된 몸 대각선, 자기 팔의 얼굴 프레이밍, 렌즈 쪽 전달, 타인의 어깨·손 소유자, 전경 흐림 틈, 유리 투과 얼굴과 외부 반사, 거울 속 주 얼굴, 손거울의 얼굴 범위, 국소 프리즘, 대칭 배경과 비대칭 포즈, 정지 인물과 주변 궤적, 카메라 롤의 16개이다. 모두 넓은 이름이 아니라 요청 근거가 있는 구성요소의 전체 결합에서만 하드가 되는 초안이다.

기존 항목을 확장·재사용할 수 있는 곳도 관계 후보 초안에 포함했다. 따라서 아래 초안의 총 항목 수를 실제 신규 항목으로 그대로 추가할 수량으로 해석하면 안 된다. 채택 전에 같은 소유자·관계의 기존 원자를 합치고 ID는 유지하는 중복 제거 검토가 필요하다.

## 5. 원 대화의 30개 구도와 12개 추가 원리

아래 구성요소와 통과 조건은 출처 문장의 번역·보편적 미학 정의가 아니라 자체 데이터 설계이다. 출처는 해당 기법의 기초 원리만 지지한다. 장면 예시는 개발용으로 작성했고 실제 렌더 통과 사례가 아니다.

### PC01. 눈높이의 가까운 상반신

검색어: `eye-level close portrait`, `head-and-shoulders portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | main subject / framing | the frame includes the face and shoulders at a readable portrait scale |
| c2 · `camera_height` | camera relative to main subject / camera | the viewpoint meets the subject near the visible eye line |
| c3 · `focus` | visible face / camera | the visible eye and expression-bearing facial landmarks remain resolved |
| c4 · `composition` | face and background / composition | a simpler surrounding field separates the face and shoulder contour |

혼동 경계: 얼굴만 확대했다고 눈높이가 증명되지는 않는다. / 가슴 위 프레이밍과 정면 얼굴 방향은 별개다.

현재 근거: `head_and_shoulders_crop`, `eye_level_observer`, `eye_focus`. 적용안: `reuse_atoms` · P0.

개발 사례: 얼굴과 어깨가 보이고 눈높이에서 촬영한 성인 인물. 반례: 같은 크롭이지만 정수리를 크게 내려다보는 사진.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S02: Canon EOS R6 V: Portrait](https://cam.start.canon/en/C023/manual/html/UG-03_ShootingStill_0050.html), [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits).

### PC02. 몸은 사선, 얼굴은 카메라 쪽

검색어: `angled shoulders facing camera`, `three-quarter body angle`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_orientation` | main torso / pose | the torso and shoulder plane turn obliquely to the camera |
| c2 · `body_orientation` | head relative to torso / pose | the head turns back toward the camera relative to the torso |
| c3 · `gaze_engagement` | main eyes and lens / expression | the visible eyes address the lens while the shoulders remain oblique |
| c4 · `composition` | head neck and torso / body_geometry | neck and shoulder connections remain continuous through the turn |

혼동 경계: three-quarter-length는 촬영 범위이다. / 얼굴과 몸이 함께 측면으로 향하는 사진은 다르다.

현재 근거: `three_quarter_body_turn`, `head_shoulder_opposition`, `direct_camera_aware`. 적용안: `new_joint_relation` · P0.

개발 사례: 어깨는 비스듬하지만 머리와 눈은 렌즈를 향한 성인. 반례: 무릎 위로 찍었을 뿐 얼굴과 어깨가 모두 정면.

기초 원리 출처: [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits), [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits).

### PC03. 맞은편 테이블 구도

검색어: `across-the-table portrait`, `table companion perspective`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | table and camera and seated subject / composition | a near table edge separates the camera position from the seated subject |
| c2 · `subject_framing` | main face and table / framing | the subject face remains above the near table plane at readable scale |
| c3 · `hand_pose` | subject hands and table / pose, action | the subject hands rest or act on the visible tabletop with plausible contact |
| c4 · `composition` | table objects and face / composition | table objects occupy supporting regions around the primary face |

혼동 경계: 카페 배경만 있거나 탑다운 음식 사진인 경우 / 실제 연애 관계·친밀한 성격의 증거로 사용

현재 근거: `companion_viewpoint_everyday_candid`, `hand_on_table_edge`. 적용안: `new_joint_relation` · P0.

개발 사례: 맞은편 좌석에서 컵 옆 손과 얼굴을 함께 담은 성인. 반례: 높은 탑다운 시점에서 음식이 중심이고 얼굴은 프레임 밖.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PC04. 가까운 동행자의 시점

검색어: `companion perspective`, `close handheld portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `camera_direction` | camera and daily activity / camera | the view occupies a plausible nearby companion position beside a daily activity |
| c2 · `action` | subject hand and activity object / action | one concrete hand activity remains legible in the near setting |
| c3 · `gaze_engagement` | subject response and camera holder / expression, action | one glance or gesture addresses the nearby camera holder |
| c4 · `composition` | main face and environment / composition, framing | the face stays readable within the nearby environmental frame |

혼동 경계: 셀피와 카메라 밖 동행자 촬영은 다르다. / 소품 없는 인플루언서 포즈만으로 생활 행동을 증명하지 않는다.

현재 근거: `companion_viewpoint_everyday_candid`, `off_camera_companion_everyday_capture`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 동행자 좌석에서 일상 동작과 렌즈 쪽 짧은 반응을 담은 성인. 반례: 팔 길이 전면카메라 셀피.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S10: Adobe: Candid photography](https://www.adobe.com/creativecloud/photography/type/candid-photography.html).

### PC05. 어깨 너머로 돌아보기

검색어: `looking back over the shoulder`, `over-the-shoulder glance`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_orientation` | main torso / pose | the main subject torso faces partly away from the camera |
| c2 · `body_orientation` | main head and own shoulder / pose | the same subject head turns back across the near shoulder |
| c3 · `composition` | main face and own shoulder / composition | the turned face remains readable beyond its own near shoulder |
| c4 · `body_pose` | main body chain / body_geometry | the head neck and torso retain a plausible connected turning range |

혼동 경계: 타인의 어깨 너머로 찍는 OTS와 혼동 / 몸 전체를 카메라 쪽으로 돌린 정면 사진

현재 근거: `turning_back_over_shoulder_pose`, `looking_back_over_shoulder_orientation`. 적용안: `extend_existing_atoms` · P1.

개발 사례: 등이 일부 보이고 본인의 어깨 너머로 돌아보는 성인. 반례: 다른 사람의 어깨만 전경에 있고 주인공은 정면.

기초 원리 출처: [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits).

### PC06. 옆얼굴과 시선 앞 여백

검색어: `profile with looking room`, `side-profile portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_orientation` | main face / pose | the visible nose lip and chin form a readable side-face contour |
| c2 · `gaze_target` | visible eye and head / expression | the visible eye and head establish one sideward direction |
| c3 · `composition` | gaze vector and image field / composition | usable open space extends ahead of the stated gaze direction |
| c4 · `subject_framing` | profile face / framing | the profile landmarks remain large enough to inspect in the final frame |

혼동 경계: 여백이 시선 뒤에 있으면 looking room과 다르다. / 옆을 보는 눈과 완전 옆얼굴은 별개다.

현재 근거: `mep_casting_profile`, `look_motion_room_direction_relation`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 옆얼굴이 화면 오른쪽을 보며 그 앞에 넓은 공간이 남음. 반례: 옆얼굴 앞은 잘리고 뒷머리 뒤쪽에만 여백이 있음.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S07: Adobe: Negative space photography](https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html).

### PC07. 무릎 위의 약한 로우앵글

검색어: `knee-up subtle low angle`, `three-quarter-length portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | main body and crop edges / framing | the frame runs from the head to the explicitly chosen region above the knees |
| c2 · `camera_height` | camera and main face / camera | the viewpoint lies modestly below the face with upward spatial cues |
| c3 · `body_pose` | main torso and legs / body_geometry | the torso and legs retain coherent near-to-far proportions |
| c4 · `composition` | main face and body / composition | the face remains a readable focal region within the larger body frame |

혼동 경계: 극단적인 지면 시점·벌레 시점은 약한 로우앵글이 아니다. / 3/4 얼굴 방향과 knee-up은 별도 축이다.

현재 근거: `knee_up_framing`. 적용안: `extend_existing_atoms` · P1.

개발 사례: 무릎 조금 위에서 잘리고 약하게 올려다보는 성인 인물. 반례: 지면에서 신발이 크게 돌출되고 얼굴이 아주 작음.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S14: Ward et al.: Nasal distortion in short-distance photographs](https://pubmed.ncbi.nlm.nih.gov/29494735/).

### PC08. 한쪽 다리에 무게를 둔 비대칭 전신

검색어: `weight-shift pose`, `asymmetrical standing pose`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | main body / framing | the full frame preserves the head and both feet |
| c2 · `body_pose` | main support and free leg / pose | one support leg carries the stance while the other remains relatively relaxed |
| c3 · `body_orientation` | shoulders and pelvis / pose | shoulder and pelvis alignment vary with the visible weight shift |
| c4 · `contact_point` | support foot and ground / body_geometry | the supporting foot establishes a plausible ground contact path |

혼동 경계: S커브·골반 과장·비대칭 의상만으로 하중 분담을 증명하지 않는다. / 일반 웨이트 시프트를 고전 콘트라포스토와 동일시하지 않는다.

현재 근거: `relaxed_standing_weight_shift`, `contrapposto_full_body`, `mep_poised_support`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 한 발이 지지하고 반대 무릎이 이완된 전신 성인. 반례: 양발 지지는 같고 의상만 비대칭.

기초 원리 출처: [S18: National Galleries of Scotland: Contrapposto](https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto).

### PC09. 앉아서 만드는 삼각형

검색어: `seated triangular composition`, `triangular pose grouping`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_pose` | subject and seat / pose | the subject sits on a visible supporting surface |
| c2 · `composition` | face elbow and knee / composition | the face elbow and knee define three separated triangle vertices |
| c3 · `body_pose` | subject limb joints / body_geometry | the visible arm and leg joints connect plausibly between those vertices |
| c4 · `subject_framing` | nominated body regions / framing | the frame preserves all three nominated vertices and their spacing |

혼동 경계: 삼각 무늬나 세 인물의 배치가 대체하지 않는다. / 신체 내부 여백의 삼각형과 세 점의 배치는 다르다.

현재 근거: `mep_graphic_pose`, `body_bounded_negative_space`. 적용안: `new_joint_relation` · P1.

개발 사례: 앉은 성인의 얼굴·팔꿈치·세운 무릎 세 점이 삼각 배치. 반례: 팔과 허리 사이만 삼각형이고 무릎은 잘림.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S18: National Galleries of Scotland: Contrapposto](https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto).

### PC10. 몸이 가로지르는 대각선

검색어: `diagonal reclining portrait`, `diagonal body axis`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_pose` | torso and support / pose | a seat sofa or wall visibly supports the reclining torso |
| c2 · `composition` | main torso axis / composition | the shoulder-to-pelvis body axis crosses the image diagonally |
| c3 · `camera_direction` | camera and environmental lines / camera | stable environmental reference lines retain the intended level camera roll |
| c4 · `composition` | main face and body axis / composition | the face remains readable near one end of the diagonal body path |

혼동 경계: 더치 앵글은 몸이 아니라 카메라 회전이다. / 지지 없이 공중에 누운 형상은 실패한다.

현재 근거: `propped_elbow_recline_support`. 적용안: `new_joint_relation` · P1.

개발 사례: 소파에 지지된 몸만 대각선이고 창틀은 수직인 성인. 반례: 몸은 수직인데 카메라 전체가 기울어짐.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S09: Adobe: Dutch angle shot](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html).

### PC11. 앉은 인물을 위에서 가까이 보기

검색어: `high-angle seated portrait`, `close elevated observer`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_pose` | subject and seat / pose | the subject is visibly seated on a supporting surface |
| c2 · `camera_height` | camera and seated face / camera | the camera looks downward from a nearby position above the seated face |
| c3 · `gaze_engagement` | main face and elevated lens / expression | the raised face or visible eye direction connects toward that camera |
| c4 · `composition` | subject body and camera / composition | head torso and near limbs follow one coherent downward perspective |

혼동 경계: 가까운 고각과 수직 탑다운·드론은 다르다. / 앉았다는 이유로 자동 overhead 프로필을 강제하지 않는다.

현재 근거: `overhead_social_snapshot_relation`, `floor_high_angle_direction`. 적용안: `extend_existing_atoms` · P1.

개발 사례: 의자에 앉아 고개를 들어 가까운 위쪽 카메라를 보는 성인. 반례: 드론 거리의 작은 인물이 바닥만 바라봄.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S14: Ward et al.: Nasal distortion in short-distance photographs](https://pubmed.ncbi.nlm.nih.gov/29494735/).

### PC12. 팔과 손으로 얼굴 주위 공간 만들기

검색어: `arm framing`, `hands framing the face`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `hand_pose` | subject own hand and face / pose | the subject own arm or hand arcs around the face perimeter |
| c2 · `composition` | face and body-made opening / composition | the face lies within a readable opening formed by that arm or hand |
| c3 · `body_pose` | main arm joint chain / body_geometry | the wrist elbow and shoulder connect plausibly through the framing gesture |
| c4 · `focus` | main face / camera | the requested expression-bearing facial region remains readable through the opening |

혼동 경계: 눈을 막는 손과 얼굴 주변의 프레이밍은 별개다. / 화면 밖 타인의 손을 주인공의 손으로 혼동하지 않는다.

현재 근거: `arms_raised_overhead`, `mep_graphic_pose`, `body_bounded_negative_space`. 적용안: `new_joint_relation` · P1.

개발 사례: 자기 팔이 얼굴 둘레에 아치를 만들고 눈은 열린 공간에 있음. 반례: 두 손바닥이 눈과 표정을 완전히 덮음.

기초 원리 출처: [S25: Canon SNAPSHOT: Techniques from professional models](https://snapshot.asia.canon/en/article/3-flattering-techniques-to-learn-from-professional-models), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques).

### PC13. 포즈 사이의 순간

검색어: `in-between moment`, `mid-gesture portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `action` | main subject and action / action | one nominated body or hand action remains visibly underway |
| c2 · `motion` | main action-bearing region / timing | a displaced limb hair group or cloth edge indicates the unfinished phase |
| c3 · `body_pose` | main body support / pose | the rest of the stance supports the same action phase |
| c4 · `composition` | face and action / composition | the facial reaction remains legible beside the incomplete gesture |

혼동 경계: 고정된 옆시선만으로 중간 순간을 증명하지 않는다. / 실제 비연출·진심·성격을 픽셀에서 확정하지 않는다.

현재 근거: `mep_in_between`, `camera_acknowledged_observer_frame`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 옷깃을 고쳐 잡는 중 손과 옷 가장자리가 이동한 성인. 반례: 옆을 본 정지 포즈에 candid라는 이름만 붙음.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S10: Adobe: Candid photography](https://www.adobe.com/creativecloud/photography/type/candid-photography.html).

### PC14. 비스듬히 걸어 들어오기

검색어: `walking portrait`, `diagonal movement`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `action` | main walker / action, timing | one subject step establishes a readable walking phase |
| c2 · `composition` | walker path and frame / composition | the walking path runs obliquely across the image plane |
| c3 · `body_pose` | main feet and attached cloth / pose | feet support and fabric displacement agree with the same step |
| c4 · `subject_framing` | main face / framing | the moving face remains readable within the chosen mid-distance frame |

혼동 경계: 기울어진 카메라가 보행 방향을 대체하지 않는다. / 걷는 포즈·실제 이동 궤적·장노출은 별개다.

현재 근거: `mep_garment_movement`, `stepping_into_frame_pose`. 적용안: `extend_existing_atoms` · P1.

개발 사례: 성인 인물이 화면을 사선으로 지나며 한 걸음의 지지가 보임. 반례: 양발 정지인데 난간만 사선.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S17: Adobe: Motion blur photography](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html).

### PC15. 활동 중심 환경 인물

검색어: `environmental portrait`, `activity-based portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `action` | subject and task element / action | the subject contacts or attends to one task-relevant scene element |
| c2 · `composition` | task and contextual fixture / composition | a contextual fixture explains where the activity takes place |
| c3 · `subject_framing` | main face and hands / framing | the frame retains the face and task-bearing hand action together |
| c4 · `composition` | main subject and environment / composition | the environment supports the activity while the subject remains readable |

혼동 경계: 공간만 넓고 행동이 없는 원경과 다르다. / 도구 소유만으로 취향·직업·숙련을 확정하지 않는다.

현재 근거: `pr_environmental_portrait_subject_place`, `mep_environment_relation`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 작업대에서 손의 작업과 얼굴·관련 도구가 같은 화면에 있음. 반례: 풍경 속 아주 작은 인물에게 직업 라벨만 부여.

기초 원리 출처: [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques), [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PC16. 카메라 쪽으로 건네기

검색어: `offering gesture`, `reaching toward camera`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `hand_pose` | subject hand and camera / pose, action | the subject attached hand extends toward the camera position |
| c2 · `contact_point` | subject hand and offered object / action | the offered object follows the visible subject hand contact |
| c3 · `composition` | near object and main face / composition | the offered hand or object occupies a nearer plane than the face |
| c4 · `composition` | offered object and main face / composition | the near object leaves the requested facial expression region readable |

혼동 경계: 카메라를 잡은 셀피 팔과 구분한다. / 프레임 밖 관객의 손을 주인공의 팔로 연결하지 않는다.

현재 근거: `reaching_toward_camera`, `hands_foreground_face_behind`. 적용안: `new_joint_relation` · P0.

개발 사례: 자기 팔로 작은 물건을 렌즈 쪽에 내밀고 뒤 얼굴이 보이는 성인. 반례: 누구의 손인지 불명확하거나 물건이 얼굴 전체를 덮음.

기초 원리 출처: [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PC17. 타인의 어깨 너머 주인공

검색어: `over-the-shoulder shot`, `OTS portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `partner_framing` | secondary companion shoulder / relationship, composition | another person shoulder forms a partial near-plane silhouette |
| c2 · `composition` | camera secondary shoulder and main face / camera, composition | the camera observes the main face beyond that secondary shoulder |
| c3 · `gaze_target` | main response and secondary companion / expression, relationship | the main response relates to the companion position indicated by the near shoulder |
| c4 · `focus` | main face and secondary shoulder / camera | the main face receives the requested focus priority over the foreground shoulder |

혼동 경계: 주인공 자신의 돌아보는 어깨가 아니다. / 어깨가 아니라 의자·소품 전경인 경우는 별도이다.

현재 근거: `over_partner_shoulder_subject_face`, `over_the_shoulder_dialogue`. 적용안: `new_joint_relation` · P0.

개발 사례: 화면 왼쪽 타인의 흐린 어깨 너머로 성인 주인공 얼굴이 선명. 반례: 주인공이 본인 어깨 너머로 돌아보기만 함.

기초 원리 출처: [S08: Adobe: Over the shoulder shot](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html).

### PC18. 타인의 손만 보이는 상호작용

검색어: `cropped companion interaction`, `companion hands-only portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `partner_framing` | secondary companion hand / relationship, framing | a secondary person hand enters from a traceable frame edge |
| c2 · `contact_point` | secondary hand and nominated target / action | that hand contacts or transfers the specified garment or small object |
| c3 · `action` | main subject and companion contact / action, expression | the main subject reaction relates to the same visible contact or transfer |
| c4 · `composition` | secondary hand and main face / composition | the secondary hand stays subordinate while the main face remains readable |

혼동 경계: 떠 있는 손·주인공의 세 번째 팔·자기 옷깃 조정과 구분한다. / 손만 등장했다고 연인·친구·동의를 추론하지 않는다.

현재 근거: `mep_fitting_adjustment`. 적용안: `new_joint_relation` · P1.

개발 사례: 가장자리에서 들어온 타인 손이 옷깃을 정리하고 성인 주인공이 반응. 반례: 주인공 자신의 손이 옷깃을 만짐.

기초 원리 출처: [S08: Adobe: Over the shoulder shot](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html), [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PC19. 흐릿한 전경 사이 얼굴

검색어: `foreground framing`, `foreground bokeh portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | near object and frame edge / composition | a scene-owned near object occupies a peripheral foreground region |
| c2 · `focus` | near object and main face / camera | that near object remains softer than the resolved main face |
| c3 · `composition` | foreground opening and main face / composition | a clear opening through the foreground reveals the intended face region |
| c4 · `composition` | three scene planes / composition | overlap and softness separate foreground subject and farther setting |

혼동 경계: 배경 보케만 있는 사진·디지털 비네팅과 구분한다. / 부드러움이 눈·표정을 덮으면 목적에 실패한다.

현재 근거: `botanical_editorial_portrait_context`, `rb_foreground_occlusion`. 적용안: `new_joint_relation` · P0.

개발 사례: 흐린 전경 잎이 양쪽 가장자리에 있고 성인 얼굴은 빈 틈에서 선명. 반례: 얼굴은 선명하지만 보케가 배경에만 있음.

기초 원리 출처: [S06: Canon SNAPSHOT: Easy Pretty Portraits](https://snapshot.asia.canon/en/article/easy-pretty-portraits-3-quick-convenient-camera-techniques), [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits).

### PC20. 문·창문 속 인물

검색어: `frame within a frame`, `doorway portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | scene opening and main subject / composition | a physical scene boundary forms an opening around the primary subject |
| c2 · `composition` | opening boundary / composition | readable boundary thickness or overlap establishes a near plane |
| c3 · `subject_framing` | main face and opening / framing | the main face stays readable inside the opening |
| c4 · `composition` | opening edges and frame / composition | the intended opening enclosure is preserved within the final crop |

혼동 경계: 디지털 테두리·비네팅·배경에 그린 아치와 구분한다. / 기존 hard 프로필은 최소 세 면의 경계를 요구하므로 한쪽 창틀만 요청하면 강제하지 않는다.

현재 근거: `frame_within_frame_boundary_relation`, `architectural_threshold_frame_depth_relation`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 실제 문틀의 세 면과 깊이가 성인 얼굴 주변을 감싸는 사진. 반례: 사진 파일에 테두리만 추가.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S06: Canon SNAPSHOT: Easy Pretty Portraits](https://snapshot.asia.canon/en/article/easy-pretty-portraits-3-quick-convenient-camera-techniques).

### PC21. 유리 너머 얼굴과 도시 반사

검색어: `through-glass portrait`, `window reflection portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | glass plane / composition | a visible pane edge or frame locates the glass plane between camera and subject |
| c2 · `composition` | transmitted main face / composition | the subject face is seen through the pane in the transmitted scene |
| c3 · `reflection_logic` | reflected exterior scene and glass / composition | a restrained exterior reflection overlays a distinct region of the pane |
| c4 · `focus` | transmitted face and reflection / camera | the transmitted expression-bearing face remains readable through the layered pane |

혼동 경계: 평면거울 속 얼굴·이중노출·비닐 필름 흐림과 구분한다. / 창문 반사만으로 도시 위치·특정 장소를 확정하지 않는다.

현재 근거: `rb_glass_reflection_transmission`, `pr_reflection_scene_binding_candidate`. 적용안: `new_joint_relation` · P0.

개발 사례: 창틀 너머 성인 얼굴과 약한 거리 반사가 분리돼 읽힘. 반례: 불투명 거울에 얼굴 하나만 반사됨.

기초 원리 출처: [S12: Adobe: Reflection photography](https://www.adobe.com/nz/creativecloud/photography/discover/reflection-photography.html), [S13: OpenStax: Images formed by plane mirrors](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors).

### PC22. 거울 속 얼굴이 주인공

검색어: `mirror-led portrait`, `reflected face as main subject`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `reflection_logic` | mirror and reflected face / composition | a physical mirror boundary contains a reflected face in one coherent view |
| c2 · `composition` | reflected main face / composition | the reflected face receives the primary visual emphasis |
| c3 · `body_orientation` | direct body and reflected body / pose, composition | a partial direct body view corresponds plausibly to that reflection |
| c4 · `focus` | reflected face / camera | the reflected eye or expression region remains resolved within the visible mirror boundary |

혼동 경계: 거울 셀피는 휴대폰의 주체·접촉·반사까지 요구하는 다른 계약이다. / 유령·지연 반사·이중 자아 라우트가 섞이면 실패한다.

현재 근거: `faithful_reflection`, `pr_reflection_scene_binding_candidate`. 적용안: `new_joint_relation` · P0.

개발 사례: 실제 뒷어깨와 거울 속 성인 얼굴이 같은 순간에 대응함. 반례: 거울 테두리만 선명하고 반사 얼굴은 흐림.

기초 원리 출처: [S12: Adobe: Reflection photography](https://www.adobe.com/nz/creativecloud/photography/discover/reflection-photography.html), [S13: OpenStax: Images formed by plane mirrors](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors).

### PC23. 작은 손거울 안의 얼굴

검색어: `handheld mirror portrait`, `selective face reflection`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `contact_point` | hand and small mirror / action | a visible hand supports one small mirror at plausible contact points |
| c2 · `reflection_logic` | small mirror and reflected face / composition | the mirror boundary encloses the selected reflected face region |
| c3 · `composition` | reflected face and image scale / framing | the reflected expression remains readable at the mirror image scale |
| c4 · `focus` | reflected face and direct scene / camera | the reflected face and direct surroundings retain a coherent focus hierarchy |

혼동 경계: 손거울이 보여도 얼굴 반사가 없으면 실패한다. / 눈 한 조각만 요청한 경우 표정 전체를 요구하지 않는다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `new_joint_relation` · P0.

개발 사례: 손이 잡은 작은 거울 안에 표정이 읽히는 성인 얼굴이 담김. 반례: 손거울 밖 직접 얼굴만 보이고 거울 안은 하늘.

기초 원리 출처: [S12: Adobe: Reflection photography](https://www.adobe.com/nz/creativecloud/photography/discover/reflection-photography.html), [S13: OpenStax: Images formed by plane mirrors](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors), [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PC24. 가장자리 프리즘·굴절

검색어: `edge refraction portrait`, `prism edge effect`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `lens_artifact` | peripheral optical effect / camera | a localized peripheral region shows refracted displacement or spectral separation |
| c2 · `composition` | optical region and frame / composition | the optical effect remains near a chosen image edge |
| c3 · `focus` | central main face / camera | the central requested facial features remain coherent and resolved |
| c4 · `composition` | edge effect and scene owner / composition | the shifted edge detail remains connected to the same scene or light source |

혼동 경계: 얼굴 전체 분해·무지개 조명만 있는 사진·원인 없는 복제와 구분한다. / 굴절 결과는 관찰 가능하지만 실제 프리즘 장비 사용은 메타데이터이다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `new_joint_relation` · P1.

개발 사례: 한쪽 가장자리만 굴절되고 성인 얼굴 중심은 선명. 반례: 얼굴 전부가 여러 조각으로 반복됨.

기초 원리 출처: [S11: Adobe / Sam Hurd: Prism photography](https://www.adobe.com/creativecloud/photography/technique/prism.html).

### PC25. 가장자리 타이트 크롭

검색어: `off-center close-up`, `tight face crop`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | main face and crop edge / framing | the face occupies a close portrait scale near one image edge |
| c2 · `composition` | main face and frame center / composition | the face focal point lies visibly away from the geometric center |
| c3 · `focus` | main face / camera | the explicitly requested eye and expression region remains resolved |
| c4 · `subject_framing` | nominated facial region / framing | the crop preserves the requested diagnostic facial region |

혼동 경계: 의도적 두상 크롭과 요청한 눈·입을 잘라버린 크롭은 다르다. / 프로필·눈 감음 요청에 양쪽 눈 가시성을 일괄 적용하지 않는다.

현재 근거: `pr_casual_crop_subject_legibility`, `beauty_tight_face_crop`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 머리 위는 일부 잘리지만 성인 눈과 입이 읽히며 중심에서 벗어남. 반례: 요청한 눈이 화면 밖으로 잘림.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits).

### PC26. 여백을 바라보는 인물

검색어: `negative-space portrait`, `looking room`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `gaze_target` | main head and gaze / expression | one visible head or gaze vector points toward a nominated side |
| c2 · `composition` | gaze and open field / composition | a contiguous low-detail field extends ahead of that vector |
| c3 · `subject_framing` | main face / framing | the subject facial signal remains readable at the final display size |
| c4 · `composition` | subject contour and field / composition | the subject outline separates from the simple field |

혼동 경계: negative space·headroom·look room·move room은 서로 다른 측정이다. / 시선 앞 공간이 있어도 복잡한 간판으로 가득하면 저정보 여백과 다르다.

현재 근거: `look_motion_room_direction_relation`, `subject_field_negative_space_relation`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 성인이 향한 쪽에 단순한 벽 여백이 있고 얼굴이 읽힘. 반례: 뒷머리 뒤쪽에만 여백.

기초 원리 출처: [S07: Adobe: Negative space photography](https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html).

### PC27. 대칭 공간 속 비대칭 인물

검색어: `symmetrical setting asymmetrical pose`, `axial portrait contrast`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | architecture axis and paired elements / composition | architectural pairs form a readable symmetry axis in the scene |
| c2 · `body_pose` | main subject pose / pose | the main subject limb or head arrangement departs visibly from that symmetry |
| c3 · `composition` | architecture and pose / composition | the two spatial roles remain simultaneously readable in one frame |
| c4 · `composition` | main face and architecture / composition | the face retains focal priority within the paired architecture |

혼동 경계: 단순 중앙 배치는 배경 대칭을 증명하지 않는다. / 인물까지 좌우 완전 복제인 경우는 다른 구도이다.

현재 근거: `centered_symmetric`, `mep_graphic_pose`. 적용안: `new_joint_relation` · P1.

개발 사례: 대칭 복도 중앙에서 성인 한쪽 팔과 고개만 비대칭. 반례: 비대칭 배경에서 인물만 중앙에 둠.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques).

### PC28. 빛·그림자의 면 분할

검색어: `graphic shadows`, `gobo portrait`, `shadow framing`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `lighting` | light pattern and receiving surface / lighting | a coherent patterned light and shadow region crosses a visible scene surface |
| c2 · `light_shape` | light pattern and surface material / lighting | the pattern defines graphic areas distinct from permanent material markings |
| c3 · `composition` | pattern and main face / composition | the pattern boundary organizes the image around the main face |
| c4 · `focus` | main face / camera | the requested facial expression survives the patterned illumination |

혼동 경계: 의복 프린트·피부 무늬·벽지와 광원 패턴을 혼동하지 않는다. / 프레임 밖 광원인 경우 장비 사용 증명보다 패턴 결과만 판정한다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `optional_relation_candidate` · P1.

개발 사례: 벽과 어깨에 창 그림자가 이어지고 성인 표정은 읽힘. 반례: 얼굴의 무늬가 조명과 무관한 타투.

기초 원리 출처: [S16: Westcott / Lindsay Adler: Environmental gobos](https://westcottu.com/creating-a-sense-of-environment-with-the-optical-spot-by-lindsay-adler).

### PC29. 정지 인물과 움직이는 주변

검색어: `still subject motion contrast`, `sharp stationary portrait with trails`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_pose` | main subject and support / pose | the primary subject keeps a readable stationary support and pose |
| c2 · `focus` | main face / camera | the requested facial region remains comparatively resolved |
| c3 · `motion` | moving peripheral element / timing, camera | a separate moving peripheral element leaves a directional exposure trail |
| c4 · `composition` | trail owner and main subject / composition | the trail and sharp subject occupy coherently related scene planes |

혼동 경계: 보케 원·얕은 심도·렌즈 흔들림만으로 모션 궤적을 증명하지 않는다. / 주인공을 추적하는 패닝과 정지 인물 대비는 다른 계약이다.

현재 근거: `panning_subject_tracking_motion_relation`, `rear_curtain_flash_motion_trace`. 적용안: `new_joint_relation` · P0.

개발 사례: 선명한 정지 성인 옆으로 이동하는 빛이 방향 궤적을 남김. 반례: 배경은 흐리지만 모든 빛 점이 동그란 보케.

기초 원리 출처: [S17: Adobe: Motion blur photography](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html).

### PC30. 프레임을 기울이기

검색어: `Dutch angle`, `Dutch tilt`, `canted angle`, `camera roll`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `camera_direction` | camera and reference lines / camera | the camera roll rotates a stable scene reference relative to the image axes |
| c2 · `composition` | scene reference lines / composition | multiple normally level scene lines share a coherent tilt direction |
| c3 · `body_pose` | main support and tilted scene / pose | the subject stance remains plausible in the tilted scene coordinates |
| c4 · `subject_framing` | main face and crop / framing | the nominated facial region remains readable after the rotated crop |

혼동 경계: 몸 자체 대각선·경사진 지면·우연히 비스듬한 물체와 구분한다. / 더치 앵글을 캔디드 촬영의 동의어로 사용하지 않는다.

현재 근거: `dutch_tilt_direction`, `dutch_angle_tension`. 적용안: `new_joint_relation` · P1.

개발 사례: 창틀과 수평 난간이 함께 기울어진 프레임의 성인 인물. 반례: 창틀은 수직인데 인물 몸만 기대어 사선.

기초 원리 출처: [S09: Adobe: Dutch angle shot](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html).

### PX01. 촬영 범위와 얼굴 방향의 분리

검색어: `shot scale versus facial orientation`, `three-quarter ambiguity`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | main crop / framing | the crop endpoint explicitly describes the included body extent |
| c2 · `body_orientation` | main face / pose | the facial direction is specified independently of that crop endpoint |
| c3 · `composition` | crop and facial direction / composition | the visible result simultaneously preserves the two requested axes |

혼동 경계: three-quarter 단독 표현은 길이인지 방향인지 불명확하다. / 새 후보가 원래 요청의 모호성을 사후에 대신 해석하지 않는다.

현재 근거: `knee_up_framing`, `restrained_three_quarter_face_depth_read`. 적용안: `reuse_atoms` · P0.

개발 사례: 무릎 위 프레이밍이며 얼굴은 비스듬히 보임. 반례: 3/4라는 단어만으로 얼굴·몸 방향을 모두 고정.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits).

### PX02. 머리 위 여백

검색어: `headroom`, `top frame clearance`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | head contour and top frame / composition | a nominated top margin separates the head contour from the upper frame edge |
| c2 · `subject_framing` | face and crop / framing | the same frame preserves the requested facial region and shot scale |
| c3 · `composition` | top margin and lateral field / composition | the top margin remains independent of lateral gaze space |

혼동 경계: headroom은 시선 앞 여백이 아니다. / 타이트 크롭 요청이면 머리 위 여백을 강제하지 않는다.

현재 근거: `head_and_shoulders_crop`. 적용안: `optional_relation_candidate` · P1.

개발 사례: 머리 위 공간은 작고 시선 앞 공간은 넓음. 반례: 머리 위 여백을 주기 위해 요청한 상반신 범위를 원경으로 바꿈.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500).

### PX03. 주인공의 첫 읽기 위계

검색어: `subject visual hierarchy`, `face priority`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | main face and distractors / composition | the intended face is separable from competing bright or high-detail regions |
| c2 · `focus` | main face / camera | the intended facial signal resolves at the nominated output display size |
| c3 · `composition` | props and main face / composition | supporting props preserve their role relative to the main face |

혼동 경계: 호감·매력 점수와 가시성은 다른 지표다. / 도구가 주인공인 제품 사진에 얼굴 우선 원칙을 강제하지 않는다.

현재 근거: `face_hands_prop_visibility_budget`. 적용안: `reuse_atoms` · P0.

개발 사례: 작은 썸네일에서도 성인 얼굴이 읽히고 밝은 소품이 가리지 않음. 반례: 얼굴은 네이티브 확대에서만 보이고 간판이 화면을 지배.

기초 원리 출처: [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques).

### PX04. 초점의 소유자

검색어: `focus ownership`, `visible eye focus`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `focus` | nominated face surface / camera | the nominated direct or reflected facial region receives the focus priority |
| c2 · `composition` | scene planes and focus owner / composition | the foreground and background softness agree with that selected owner |
| c3 · `subject_framing` | focused feature / framing | the focused feature is large enough for the intended review scale |

혼동 경계: 거울 테두리의 선명함은 반사된 눈의 선명함이 아니다. / 포커스 스태킹·스플릿 디옵터는 단일 초점 이행과 다른 선택이다.

현재 근거: `eye_focus`, `shallow_depth_focus_falloff_relation`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 거울 테두리는 부드럽고 안의 성인 눈이 선명. 반례: 거울 테두리만 날카롭고 반사된 얼굴이 흐림.

기초 원리 출처: [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [S13: OpenStax: Images formed by plane mirrors](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors).

### PX05. 가림의 소유자와 범위

검색어: `occlusion owner`, `partial occlusion`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | occluder owner / composition | the nominated occluder has a traceable scene or body owner |
| c2 · `composition` | occluder and target region / composition | the occluder overlaps only the requested image region |
| c3 · `composition` | surviving diagnostic region / composition | the requested surviving facial or action evidence remains exposed |

혼동 경계: 친밀감·몰래 촬영·얼굴 숨김을 같은 상태로 합치지 않는다. / 전체 얼굴 노출보다 특정 남길 영역을 요청 기준으로 쓴다.

현재 근거: `rb_foreground_occlusion`, `intentional_face_occluded_mood_portrait`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 커튼이 한쪽 어깨만 가리고 표정은 보이는 성인. 반례: 커튼이 요청한 눈까지 막음.

기초 원리 출처: [S06: Canon SNAPSHOT: Easy Pretty Portraits](https://snapshot.asia.canon/en/article/easy-pretty-portraits-3-quick-convenient-camera-techniques), [S08: Adobe: Over the shoulder shot](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html).

### PX06. 손의 소유자와 접촉

검색어: `hand ownership`, `contact continuity`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `contact_point` | hand and owner / body_geometry | each visible hand connects to a plausible subject or entering frame-edge owner |
| c2 · `contact_point` | hand and object / action | the nominated hand contacts the object at a traceable grip or support point |
| c3 · `composition` | contact region / composition | the contact remains visible at the required final review scale |

혼동 경계: 새 팔 생성·떠 있는 소품·손가락 수만 맞는 경우 / 피사체 수 한 명과 타인 손의 존재는 충돌할 수 있으므로 count와 relationship에 요청 근거 필요

현재 근거: `pr_object_contact_shadow_support`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 자기 팔이 이어진 손으로 손거울 테두리를 지지함. 반례: 손은 보이지만 팔·가장자리 소유자가 없고 거울이 떠 있음.

기초 원리 출처: [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/).

### PX07. 얼굴 비례와 카메라 거리

검색어: `camera-distance perspective`, `near-field facial perspective`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `camera_direction` | camera and face depth / camera | the camera viewpoint defines a coherent near-to-far relation across the face |
| c2 · `composition` | near and farther facial regions / composition | near facial or hand regions change scale coherently with the chosen distance |
| c3 · `subject_framing` | crop and camera position / framing | the intended crop is preserved independently of the perspective choice |

혼동 경계: 초점거리 숫자만으로 원근 비례를 증명하지 않는다. / 초광각 셀피 요청을 무조건 자연 비례 사진으로 치환하지 않는다.

현재 근거: `wide_angle_near_field_perspective`, `distortion_controlled_portrait_perspective`. 적용안: `reuse_scoped_profile` · P0.

개발 사례: 같은 크롭이라도 가까운 시점의 코·손과 먼 시점의 비례를 구분. 반례: 24mm 라벨만 있고 원근 단서가 없음.

기초 원리 출처: [S14: Ward et al.: Nasal distortion in short-distance photographs](https://pubmed.ncbi.nlm.nih.gov/29494735/).

### PX08. 몸 대각선과 카메라 롤의 분리

검색어: `body diagonal versus camera roll`, `diagonal versus canted`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | main body axis / composition | the body axis is measured against the image frame |
| c2 · `camera_direction` | camera and scene lines / camera | camera roll is evaluated through independent stable scene lines |
| c3 · `composition` | body and scene angle axes / composition | the two angle relations remain independently describable in the same image |

혼동 경계: 자세 변경을 카메라 변경으로 교정하지 않는다. / 배경 기준선이 없으면 카메라 롤 판정은 unscorable이다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `optional_relation_candidate` · P0.

개발 사례: 소파의 성인 몸은 대각선이고 창틀은 수직. 반례: 인물만 사선인데 Dutch angle이라고 판정.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S09: Adobe: Dutch angle shot](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html).

### PX09. 배경 선과 윤곽의 접선 분리

검색어: `background tangency`, `contour separation`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | background line and subject contour / composition | the nominated background line remains separable from the subject contour |
| c2 · `composition` | hair shoulders and background / composition | the hair and shoulder edges retain a readable depth boundary |
| c3 · `subject_framing` | subject contour in final crop / framing | the separation survives the final crop and display size |

혼동 경계: 인물 머리에서 자라는 전봇대·어깨에 붙은 난간 / 모든 겹침을 금지하는 규칙으로 확장하지 않는다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `optional_relation_candidate` · P1.

개발 사례: 머리 옆 간판 지지대가 떨어져 보임. 반례: 지지대가 정수리 윤곽과 이어짐.

기초 원리 출처: [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits), [S05: Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques).

### PX10. 팔·몸 사이 여백의 형상

검색어: `body-bounded negative space`, `arm-torso aperture`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `body_pose` | main body contours / pose | connected body contours bound one readable opening |
| c2 · `composition` | body opening and background / composition | the opening contains continuous scene background |
| c3 · `subject_framing` | opening boundary / framing | all nominated contour boundaries remain visible in the crop |

혼동 경계: 앉은 삼각형의 세 점 배치와 다르다. / 의상 무늬·배경 삼각형이 대체하지 않는다.

현재 근거: `body_bounded_negative_space`, `mep_graphic_pose`. 적용안: `reuse_scoped_profile` · P1.

개발 사례: 굽힌 팔과 허리 사이에 배경이 보이는 삼각 틈. 반례: 셔츠에 그려진 삼각형.

기초 원리 출처: [S18: National Galleries of Scotland: Contrapposto](https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto).

### PX11. 얼굴로 수렴하는 장면 선

검색어: `leading lines to face`, `scene-owned directional line`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `composition` | scene line / composition | a scene-owned line has a traceable beginning and continuation |
| c2 · `composition` | scene line and target face / composition | its visible direction leads toward the nominated subject region |
| c3 · `composition` | line and face hierarchy / composition | the line remains subordinate to the target facial signal |

혼동 경계: 사선이라는 이유만으로 유도선이 되지 않는다. / 얼굴을 가로지르는 강한 선은 집중을 분산할 수 있다.

현재 근거: 전용 관계는 신규 초안 또는 선택 후보로 검토. 적용안: `optional_relation_candidate` · P1.

개발 사례: 테이블 가장자리와 난간이 성인 얼굴 근처로 이어짐. 반례: 강한 선이 얼굴 반대쪽 화면 밖으로 흐름.

기초 원리 출처: [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits), [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500).

### PX12. 원본 구도와 게시 크롭

검색어: `output crop preservation`, `display-scale portrait`.

| 구성요소 | 소유자 / 적용 차원 | 관찰할 관계 |
|---|---|---|
| c1 · `subject_framing` | face action and output crop / framing, format | the nominated facial and action regions remain inside the declared output crop |
| c2 · `composition` | selected device and crop / composition | the selected optical or framing device remains visible after that crop |
| c3 · `focus` | required feature and display / camera | the required feature remains legible at the nominated display scale |

혼동 경계: SNS 비율을 모든 플랫폼의 영구 규격으로 고정하지 않는다. / 미리보기 재크롭을 검증하지 않고 최종 게시 성공이라고 보고하지 않는다.

현재 근거: `face_hands_prop_visibility_budget`. 적용안: `reuse_atoms` · P0.

개발 사례: 세로 크롭 후에도 손거울 테두리와 성인 눈이 남음. 반례: 크롭이 거울 테두리를 잘라 일반 얼굴 사진으로 바뀜.

기초 원리 출처: [S01: Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500), [S04: Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits).

## 6. SNS 표현과 여러 장의 구성은 별도 범위로 둔다

### PS01. 포토덤프·꾸민 듯 안 꾸민 듯한 스냅

검색어: photo dump, curated candid. 범위: `capture_style`.

보이는 요소: one frame depicts a specific interrupted everyday action; one restrained crop or gesture irregularity remains visible; the chosen portrait signal remains readable despite that irregularity.

경계: 느슨한 외관과 실제 무편집·무연출은 다르다. / 여러 장의 묶음이라는 의미를 한 장 안의 콜라주로 치환하지 않는다.

출처와 범위: [S23: Vogue: What is in an Instagram photo dump?](https://www.vogue.com/article/instagram-photo-dump-generation-z), [S10: Adobe: Candid photography](https://www.adobe.com/creativecloud/photography/type/candid-photography.html).

### PS02. 디카·직광 플래시 스냅

검색어: digicam aesthetic, direct-flash snapshot. 범위: `capture_style`.

보이는 요소: a near-axis flash-like source creates direct highlights and scene-owned cast shadows; one nominated low-resolution or compression texture remains locally visible; the intended facial expression remains legible through the chosen texture.

경계: 직광 플래시·노이즈·JPEG는 독립 조건이며 CCD 장비를 픽셀에서 확정하지 않는다. / Y2K 의상·2000년대 시대·디카를 자동 동의어로 묶지 않는다.

출처와 범위: [S03: Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits), [S02: Canon EOS R6 V: Portrait](https://cam.start.canon/en/C023/manual/html/UG-03_ShootingStill_0050.html).

### PS03. 0.5 셀피·초광각 셀피

검색어: 0.5 selfie, ultrawide selfie. 범위: `capture_style`.

보이는 요소: a close self-held camera viewpoint produces a wide surrounding field; near and farther body regions show coherent close-range scale differences; the requested face region remains recognizable within that wide field.

경계: .5x는 카메라 선택 메타데이터이고 0.5 셀피는 촬영 관행이다. / 후면·화면 비확인·손의 위치를 라벨만으로 일괄 강제하지 않는다.

출처와 범위: [S21: Apple: Ultra Wide camera / macro guide](https://support.apple.com/en-sa/guide/iphone/iphfaacf2eb0/ios), [S14: Ward et al.: Nasal distortion in short-distance photographs](https://pubmed.ncbi.nlm.nih.gov/29494735/).

### PS04. 관계·반응 중심 인물

검색어: relational portrait, interaction-led portrait. 범위: `capture_style`.

보이는 요소: one visible gesture or response relates to a specific interaction target; the frame preserves evidence of that same target or its position; the subject reaction remains readable within the interaction frame.

경계: 진정성·성격·실제 관계는 단일 픽셀의 확정 사실이 아니다. / 기쁨·대화·호감을 모든 인물에게 기본 주입하지 않는다.

출처와 범위: [S19: Adobe: 2026 Creative Trends Forecast](https://business.adobe.com/resources/creative-trends-report.html), [S20: Adobe: Connectioneering in the AI era](https://business.adobe.com/uk/blog/connectioneering-creative-trend-human-connection-ai-era), [S08: Adobe: Over the shoulder shot](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html).

### PS05. 생활 도구를 이용한 시각 실험

검색어: creative portrait, everyday optical device. 범위: `capture_style`.

보이는 요소: one nominated scene-owned device changes a visible spatial relation; the subject action or visible placement relates coherently to that device; the requested portrait signal survives the optical intervention.

경계: creative·cinematic·editorial은 특정 시각 의무가 아니다. / 새로움 점수와 장비·인물의 매력은 서로 다른 평가다.

출처와 범위: [S11: Adobe / Sam Hurd: Prism photography](https://www.adobe.com/creativecloud/photography/technique/prism.html), [S15: Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/), [S24: Canon SNAPSHOT: Creative portraitures](https://snapshot.asia.canon/vn/en/article/3-creative-ways-to-shoot-portraitures).

### PM01. 딥틱

검색어: diptych, paired portraits. 범위: `multi_image`.

보이는 요소: two independently readable images form one explicitly ordered pair; a declared visual attribute links the paired images; a declared change distinguishes their portrait roles.

경계: 두 사람 투샷과 두 이미지의 쌍은 다르다. / 기본 single-image 생성에 두 패널을 몰래 추가하지 않는다.

출처와 범위: [S22: Julieanne Kost: Pairing diptychs and triptychs](https://jkost.com/blog/2015/06).

### PM02. 트립틱

검색어: triptych, three-image portrait set. 범위: `multi_image`.

보이는 요소: three independently readable images form one nominated group; a declared color shape or light relation connects all three; each image contributes a distinct declared portrait function.

경계: 세 사람 단체사진과 세 이미지의 그룹은 다르다. / 같은 시드·외형 연속성이 자동 보장되지 않는다.

출처와 범위: [S22: Julieanne Kost: Pairing diptychs and triptychs](https://jkost.com/blog/2015/06).

### PM03. 시간 순서 인물 시퀀스

검색어: portrait sequence, temporal portrait progression. 범위: `multi_image`.

보이는 요소: separate images have an explicit ordered sequence; one declared event phase changes between the ordered frames; declared appearance and setting anchors maintain permitted continuity.

경계: 단일 중간 순간은 시간 순서를 증명하지 않는다. / 인물의 진짜 감정 변화·성격을 사진의 순서만으로 확정하지 않는다.

출처와 범위: [S22: Julieanne Kost: Pairing diptychs and triptychs](https://jkost.com/blog/2015/06), [S10: Adobe: Candid photography](https://www.adobe.com/creativecloud/photography/type/candid-photography.html).

Adobe의 2026 자료와 2026-09-16 해설은 관계·일상·감정 전달을 강조한다. 이는 산업 전망이며 특정 인물 구도의 SNS 인기 순위·조회수·전환 효과를 측정한 자료가 아니다. 포토덤프 자료는 2022년 문화 해설이다. 디카·0.5 셀피는 이 연구에서 시각 표현과 촬영 메타데이터를 나눠 기록했으며 2026 상승 추세를 별도 주장하지 않는다. [Adobe 2026 전망](https://business.adobe.com/resources/creative-trends-report.html), [Adobe 9월 해설](https://business.adobe.com/uk/blog/connectioneering-creative-trend-human-connection-ai-era), [Vogue 포토덤프](https://www.vogue.com/article/instagram-photo-dump-generation-z).

## 7. 후보팩용 데이터 설계와 채택 규칙

초안은 **156개 원자 후보, 42개 선택 번들, 16개 관계 프로필**을 포함한다. 기본 컨텍스트는 human portrait이지만 연구 예시의 성인 지정은 고정 캐스팅·나이·성별·외형 기본값으로 이식하지 않았다. 새로운 장면·인물·소품을 자동 추가하는 프리셋은 만들지 않았다.

후보는 `concept_units`를 짧은 관계 단위로 보존하고 `relations`에서 소유자와 대상, `affected_dimensions`에서 변경 차원을 선언한다. 얼굴·몸·카메라·표정·초점을 하나의 무차별 구도 태그로 합치지 않는다. 타인의 어깨나 손을 선택하려면 `relationship`과 관련 `composition/framing` 차원이 열려 있고 요청한 인원 조건과도 맞아야 한다. 닫힌 pose/camera/relationship을 번들이 열어서는 안 된다.

번들의 `associated_profile_ids`는 연구 연관 정보이다. 선택된 번들이 독립 요청 근거 없이 프로필을 자동 하드 활성화하지 않는다. 반면 시각 개념을 명시적으로 opt-in하여 그 의무를 선택한 경우에는 해당 계약의 모든 구성요소와 render gate를 인계해야 한다. 번들 선택과 프로필 opt-in은 서로 다른 행동이다. 선택하지 않은 후보는 의무가 아니며 모든 후보를 거절해도 된다.

프로필의 exact trigger는 구성요소의 전체 결합만 사용한다. `mirror portrait`, `candid`, `Dutch angle`, `pretty`, `three-quarter` 등 단독 라벨을 곧바로 새 하드 프로필로 만들지 않는다. 한국어 자연 설명과 가까운 표현은 선택 후보의 검색 회수 대상이다. 이 초안의 영어 전체 정의는 컴파일·변이 검증용이며 실사용자의 발화 문장을 exact alias로 박아 넣는 방식으로 일반화할 계획이 아니다.

`source_ids`, URL, 시대 유행 근거, 후보–출처 맵은 유지보수 파일에만 둔다. 런타임 후보의 embedding text·concept units·최종 프롬프트에 연구 제목·검색 과정·출처 문장을 복사하지 않는다. 초안의 부정 경계는 평가·후보 거절을 위한 데이터이며 positive prompt에 포괄적인 금지문으로 주입하지 않는다.

### 원자 후보의 추가 개선이 필요한 부분

각 원자는 의미를 보존하는 일차 분해안이며 아직 독립 후보 노출률을 검증하지 않았다. 단일 구성요소가 너무 일반적이면 번들 키워드 회수와 실제 선택이 떨어질 수 있다. 전체 의미를 문장 템플릿 하나로 만들기보다 `전경 위치–얼굴 틈–초점 소유자`, `거울 경계–반사 얼굴–직접 몸 대응` 같은 필수 공동 관계를 번들의 구성요소와 relation evidence로 묶어야 한다. 가벼운 유사도 히트가 없는 관계를 대신 증명하게 두지 않는다.

## 8. 검증 사례와 이후 픽셀 시험

개발용 사례는 총 252개이다. 각 개념의 영어 전체 정의·넓은 영어 라벨·한국어 설명·한국어 혼동 반례, 신규 프로필의 부정·일부 구성요소 변이, 20개 요청 우선 경계 사례를 포함한다. 한국어 사례는 데이터와 같이 작성했으므로 독립 holdout이나 임베딩 일반화 성공으로 부르지 않는다. 이번 실행 결과는 `verification.json`에 있는 검사만 유효하다.

이후 단계는 다음 순서로 진행한다.

1. 30개 구도의 요청 의미·반례·평가 기준을 런타임 데이터와 독립적으로 동결한다. 12개 원리는 재사용 검사에 포함한다.
2. 기존 원자와 신규 관계를 중복 제거하고, 관계별 source/component/profile/bundle을 확인한다.
3. 임베딩·BM25F 인덱스를 실제 채택된 소스에서 갱신하고 해시·정확 경로·의미 재표현·인접 반례를 검사한다. 이 연구에서는 인덱스를 갱신하지 않았다.
4. 후보 노출과 작가 선택을 별도로 기록한다. 노출되지 않은 목표가 프롬프트나 이미지에서 나타났다고 후보팩 효과라고 해석하지 않는다.
5. 관계별 서로 다른 세 장면과 독립 두 시도로 적합 범위를 시험한다. 예산과 표본 수는 실제 실행 전 결정한다. 같은 코어를 동결한 baseline/후보 선택 조건을 비교하되 시드만 같다고 모든 조건이 동일하다고 가정하지 않는다.
6. 전체 썸네일에서 주인공·구도 장치의 첫 읽기를 보고, 네이티브 크롭에서 손 접촉·눈 초점·반사 대응·몸의 지지·세부 가림을 판정한다. 적용되는 모든 hard gate가 같은 이미지에서 통과해야 장면 통과이다.
7. 가시성·초점·물리 관계의 통과와 사용자가 느끼는 매력·친밀감·흥미를 분리한다. 사용자 수락을 받기 전 대표 구도로 승격하지 않는다.

특히 실패를 예상하고 대비할 대상은 전경이 눈을 덮는 경우, 손거울이 너무 작아 얼굴을 읽을 수 없는 경우, 유리 투과와 거울 반사가 혼합되는 경우, 타인의 손이 주인공의 추가 팔로 이어지는 경우, 단순 보케를 움직임 궤적으로 오인하는 경우, 기울어진 몸을 더치 앵글로 판정하는 경우이다. 실패·가림·판정 불가를 평균 점수로 상쇄하지 않는다.

## 9. 적용 우선순위

P0은 원 대화의 주된 얼굴 전달 목표와 혼동 위험을 해결하는 순서이다: 촬영 범위/방향 분리 → 얼굴·손·초점 소유자 → 맞은편 테이블과 방향 분리 → 전경 틈 → 유리/거울/손거울 분리 → 타인의 어깨/손 → 여백과 모션 대비. 이는 인기순위나 필수 추천 템플릿이 아니다.

P1은 몸과 배경의 그래픽 관계, 자세 지지, 국소 광학 변주이다. P2는 유행 표현의 날짜·근거 갱신과 다중 이미지 시리즈 계약이다. 한 장의 사진만 요청하면 다중 이미지 모드는 후보 노출에서 제외한다.

현재 research-only 결과에 대해 완료라고 말할 수 있는 것은 출처 회수, 용어 분해, 현재 사전 대조, 적용 초안 작성과 실행된 구조 검사이다. 검색 노출, 임베딩 일반화, 실제 후보팩 전달, 이미지 의미 성공, 사용자 매력 판단은 별도의 미검증 상태로 남긴다.

## 10. 출처 기록과 제한

| ID | 자료 | 확인 범위 | 제한 |
|---|---|---|---|
| S01 | [Canon: Shooting a balanced portrait](https://asia.canon/en/support/8200023500) | 촬영 범위별로 얼굴·행동·환경이 차지하는 비중이 달라진다. · `page_read` | 용어 사용의 한 사례이며 무릎 위·가슴 위의 모든 명칭을 국제 표준으로 고정하지 않는다. |
| S02 | [Canon EOS R6 V: Portrait](https://cam.start.canon/en/C023/manual/html/UG-03_ShootingStill_0050.html) | 얼굴과 눈에 초점을 두고 주변을 단순화하며 연속 촬영으로 표정·자세 변화를 포착한다. · `page_read` | 특정 기종 기능 설명을 모든 장비나 생성 이미지의 EXIF 증명으로 확장하지 않는다. |
| S03 | [Nikon: Take Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/take-better-portraits) | 어깨와 머리 방향을 분리하고 배경의 돌출 선과 복잡성을 점검한다. · `page_read` | 원문의 신체를 날씬하게 만든다는 가치 판단은 채택하지 않는다. |
| S04 | [Nikon: Quick Tips for Taking Better Portraits](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits) | 중앙에서 벗어난 얼굴도 눈에 초점을 유지해야 한다. · `page_read` | 눈 초점은 표정 전달 목표의 기준이며 눈 감은 사진이나 흐림을 요청한 사진을 부정하지 않는다. |
| S05 | [Canon Canada / Nicole Ashley: Portrait tips](https://www.canon.ca/en/Articles/2024/portrait-photography-tips-and-techniques) | 자세를 고정하기보다 머리·옷·발의 작은 동작을 관찰하고 배경을 보조 역할로 둔다. · `page_read` | 행동이 자연스러워 보인다고 실제 성격·진심·촬영 경위를 증명하지 않는다. |
| S06 | [Canon SNAPSHOT: Easy Pretty Portraits](https://snapshot.asia.canon/en/article/easy-pretty-portraits-3-quick-convenient-camera-techniques) | 흐린 전경과 배경 사이에 피사체를 놓는 방식은 얼굴 방향으로 시선을 유도할 수 있다. · `search_excerpt_only_open_403` | 본문 열람이 403으로 제한되어 검색에 노출된 전경 흐림·가림 관련 설명만 사용한다. |
| S07 | [Adobe: Negative space photography](https://www.adobe.com/creativecloud/photography/type/negative-space-photography.html) | 여백은 피사체와 주변의 관계이며 얕은 심도와 함께 사용할 수 있다. · `page_read` | 자료의 여백 비율 조언을 모든 인물사진의 필수 수치로 채택하지 않는다. |
| S08 | [Adobe: Over the shoulder shot](https://www.adobe.com/sg/creativecloud/video/production/cinematography/camera-shots-and-angles/over-the-shoulder-shot.html) | 가까운 인물의 어깨·머리 일부 너머로 다른 인물을 보는 층화 구도이다. · `page_read` | 영상 기법을 정지사진의 공간 관계에 한정해서 전용하며 장면 전환·역숏은 별도이다. |
| S09 | [Adobe: Dutch angle shot](https://www.adobe.com/au/creativecloud/video/production/cinematography/camera-shots-and-angles/dutch-angle-shot.html) | 카메라의 롤 회전으로 장면의 수평·수직 기준선이 기울어진다. · `page_read` | 자료의 x축·candid angle 표기는 채택하지 않고 roll / canted angle로 기록한다. 긴장 연출은 제안이지 인물의 정신 상태 증명이 아니다. |
| S10 | [Adobe: Candid photography](https://www.adobe.com/creativecloud/photography/type/candid-photography.html) | 포즈를 지시한 사진과 진행 중인 생활 사건을 관찰한 사진의 촬영 접근이 다르다. · `page_read` | 카메라를 보지 않음만으로 비연출·무인지·동의를 판단하지 않는다. |
| S11 | [Adobe / Sam Hurd: Prism photography](https://www.adobe.com/creativecloud/photography/technique/prism.html) | 프리즘은 굴절·반사·색 분산을 만들며 인물 촬영의 기본 구성을 먼저 확보한다. · `page_read` | 가장자리만 쓰기와 얼굴 중심 보존은 이번 목적의 설계 제안이지 모든 프리즘 사진의 정의가 아니다. |
| S12 | [Adobe: Reflection photography](https://www.adobe.com/nz/creativecloud/photography/discover/reflection-photography.html) | 물·유리·거울의 반사는 카메라 높이와 위치에 따라 포함 범위가 달라진다. · `page_read` | 유리 투과와 평면거울 반사, 물 표면 반사를 하나의 프로필로 합치지 않는다. |
| S13 | [OpenStax: Images formed by plane mirrors](https://openstax.org/books/university-physics-volume-3/pages/2-1-images-formed-by-plane-mirrors) | 평면거울의 가상상은 거울 뒤에 위치하며 거울에서 물체까지 거리와 상까지 거리가 같다. · `page_read` | 거울 표면에 초점이 맞으면 반사된 얼굴도 자동으로 선명하다는 설명은 채택하지 않는다. 곡면·프리즘은 별도 광학이다. |
| S14 | [Ward et al.: Nasal distortion in short-distance photographs](https://pubmed.ncbi.nlm.nih.gov/29494735/) | 카메라 거리 변화가 얼굴의 원근 비례에 영향을 주는 수학 모델을 제시한다. · `pubmed_abstract_read_pmc_fulltext_unavailable` | PubMed 초록은 확인했고 PMC 본문은 접근 확인 화면으로 제한되었다. 특정 왜곡 비율·미용 판단·진단은 사용하지 않는다. |
| S15 | [Canon Creator Lab / Nina Collins: Creative portrait photography](https://www.canoncreatorlab.ca/insights/creative-portrait-photography/) | 생활 소품은 인물에게 구체적인 상호작용을 부여하고 작은 움직임으로 사진을 변주할 수 있다. · `page_read` | 특정 소품·시대·인물 외형을 구도 계약의 의무로 만들지 않는다. |
| S16 | [Westcott / Lindsay Adler: Environmental gobos](https://westcottu.com/creating-a-sense-of-environment-with-the-optical-spot-by-lindsay-adler) | 고보는 빛이 통과하는 패턴을 만들며 투사 패턴의 경계를 선명하거나 부드럽게 조절할 수 있다. · `page_read` | 원인 장비가 화면 밖이면 특정 고보 장비의 실제 사용을 픽셀만으로 증명하지 않는다. |
| S17 | [Adobe: Motion blur photography](https://www.adobe.com/creativecloud/photography/technique/motion-blur.html) | 노출 중 움직임과 셔터 시간이 궤적을 만들며 고정 카메라와 패닝은 다른 촬영 관계이다. · `page_read` | 흐린 배경만으로 움직임 흐림·패닝·장노출을 판정하지 않는다. |
| S18 | [National Galleries of Scotland: Contrapposto](https://www.nationalgalleries.org/art-and-artists/glossary-terms/contrapposto) | 한 다리에 하중을 싣는 자세와 골반·몸의 대응 관계를 설명한다. · `page_read` | 일반 비대칭 자세 전부를 콘트라포스토로 하드 활성화하지 않는다. |
| S19 | [Adobe: 2026 Creative Trends Forecast](https://business.adobe.com/resources/creative-trends-report.html) | 2026 전망은 감각·연결·장난스러운 실험·지역성을 제시한다. · `page_read` | SNS 인물 구도별 인기 순위나 성과 측정 자료가 아니다. |
| S20 | [Adobe: Connectioneering in the AI era](https://business.adobe.com/uk/blog/connectioneering-creative-trend-human-connection-ai-era) | 일상 상호작용과 공유된 경험을 중심으로 한 시각 이야기 방향을 설명한다. · `page_read` | 업계 자기 전망이며 사진의 진실성·보편적 호감·매출 효과를 보증하지 않는다. |
| S21 | [Apple: Ultra Wide camera / macro guide](https://support.apple.com/en-sa/guide/iphone/iphfaacf2eb0/ios) | 지원 기종에서는 .5x를 선택해 Ultra Wide 카메라로 전환할 수 있다. · `page_read` | 이 문서는 매크로 사용 설명이다. 0.5 셀피의 인기·필수 후면 촬영·모든 기종 지원을 뒷받침하지 않는다. |
| S22 | [Julieanne Kost: Pairing diptychs and triptychs](https://jkost.com/blog/2015/06) | 색·형태·선·빛과 분위기를 이용해 여러 사진의 관계를 연결한다. · `search_excerpt_only_open_406` | 정지사진 한 장의 구도와 사진 간 배치·순서를 구분하며 검색에서 확인한 설명 범위를 넘지 않는다. |
| S23 | [Vogue: What is in an Instagram photo dump?](https://www.vogue.com/article/instagram-photo-dump-generation-z) | 포토덤프의 느슨한 외관도 선택·편집된 결과일 수 있다는 문화적 해설이다. · `page_read` | 2022년 기사이며 2026년 인기 데이터로 사용하지 않는다. |
| S24 | [Canon SNAPSHOT: Creative portraitures](https://snapshot.asia.canon/vn/en/article/3-creative-ways-to-shoot-portraitures) | 반사·소품·선의 대비를 통한 인물 구도 사례를 소개한다. · `search_excerpt_only_open_403` | 검색에 표시된 2026년 업데이트 표기는 유행의 시작일·실험 검증일이 아니다. |
| S25 | [Canon SNAPSHOT: Techniques from professional models](https://snapshot.asia.canon/en/article/3-flattering-techniques-to-learn-from-professional-models) | 손을 얼굴 주변에 배치하는 포즈 사례를 소개한다. · `search_excerpt_only_open_403` | 작은 얼굴·매력의 보편적 이상은 채택하지 않는다. 손 프레이밍의 형상 기준은 자체 제안이다. |

참조 대화에 등장한 Rosie Lugg·Eletrico 관련 원문 URL은 조회된 대화에서 복원되지 않았고 이번 검색에서도 해당 Canon 원문을 확인하지 못했다. 이 이름들을 신규 기술 계약이나 유행 근거로 사용하지 않았다. Nina Collins 자료는 Canon Creator Lab 원문에서 확인했다. 일부 Canon SNAPSHOT와 Julieanne Kost 원문은 검색 발췌만 확인했으므로 위와 같이 열람 범위를 제한했다. 외부 참고 이미지의 픽셀·라이선스·데이터셋 수집 가능성은 이번에 조사·승인된 범위가 아니며 이미지를 수집하거나 학습 데이터라고 부르지 않았다.

## 11. 실제 실행한 초안 검증

`python3 docs/research-evidence/photo-prompt/portrait-composition-20260927/verify_research.py`로 다음을 실행했다.

- 개념 50개·출처 25개·개발 사례 252개의 ID와 상호 참조를 확인했고 기존 ID 참조 74건을 현재 소스에서 대조했다.
- 관계 프로필 16개가 기존 컴파일러에서 64개 소유자 지정 gate로 컴파일되었다.
- 원자 후보 156개와 번들 42개가 실제 확장 병합 함수를 이용한 메모리 내 검사에 통과했다.
- 신규 프로필 범위에서 정의·넓은 라벨·부정·일부 구성요소 사례 132건과 추가 라벨·단일 구성요소 217건의 좁은 활성화를 검사했다.
- 정상 번들 42건, 구성요소가 빠진 번들의 거절 156건, 닫힌 차원 때문에 거절되는 번들 131건, 중복 evidence field의 거절 16건을 확인했다.
- 검증 전후에 스냅샷 대상 런타임 파일의 해시가 같았다. 검증기는 연구 폴더의 verification.json만 기록한다.

이는 252개의 렌더 테스트 통과나 전체 저장소 회귀 통과를 의미하지 않는다. 한국어 후보 회수·임베딩 일반화, 반례 픽셀 50건, 요청 우선 설계 사례 20건은 실행하지 않았다. 실제 후보팩 전달·선택·최종 프롬프트 감사·렌더 요청 감사·이미지 의미 검증·사용자 판단도 수행하지 않았다. 현재 판정은 **연구 초안의 실행된 구조 검사 통과**이다.

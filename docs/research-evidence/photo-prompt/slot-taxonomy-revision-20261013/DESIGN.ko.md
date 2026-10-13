# 슬롯 체계 정비 0단계: 확정 설계

기준은 `39e1b3a8`의 18,250개 후보·12,020개 연결·112개 슬롯이다. 이전 감사와 사용자가 지정한 [이미지 특징 요소 정리](chatgpt-conversation://6ab3a1f1-fca8-83ee-8782-b4218ae0da39)의 전체 45개 분류를 대조했다. 참고 대화는 분류 범위의 참고 자료이며 운영 지시나 이미지에서 원인을 추론하는 규칙이 아니다.

목표는 **136개의 평면 역할 태그**다. 원래 역할 106개를 유지·정제·개명하고 30개를 추가한다. 후보 본문을 슬롯 아래로 복사하지 않는다. 한 canonical 후보와 역할은 다대다 관계이고 각 역할은 공통 positive 풀 전체를 독립 BM25F·임베딩으로 검색한다.

## 의미 계약

[TARGET-CATALOG.json](TARGET-CATALOG.json)은 운영 전환에 사용할 확정 명세다. 각 역할에 영어·한국어 설명, 대상 소유 범위, 의미 차원, 직접/맥락 구분, 구체 속성 경로, 의미 증거 단어, 포함·제외 설명, 이웃 역할, frozen core focus 필드, 제시 우선순위를 둔다. [SLOT-DECISIONS.json](SLOT-DECISIONS.json)은 기존 112개 전부의 유지·개명·분해·통합 결정을 기록한다.

property_prefixes는 후보의 실제 effect property와 비교하는 범위다. evidence_terms는 후보 의미를 대조하는 보조 자료다. 차원만 같거나 단어 하나가 겹친다는 이유로 의미 적합성 완료를 선언하지 않는다. 직접 역할의 긍정 판정에는 명시적 소유 속성 근거와 의미 근거가 함께 필요하다. 근거가 빈 후보는 검토 필요로 제시할 수 있지만 검증된 역할로 표시하지 않는다. 직접 속성과 명백히 다른 효과를 가진 후보는 역할 부적합으로 구별한다. 맥락 역할은 실제 배경·목적·해석이 선언된 범위에서만 활용하며 시각 사실로 확대하지 않는다.

lighting·makeup_style·wardrobe_style은 완결된 복합 구성이라는 독립 의미가 있을 때 유지한다. 세부 역할이 있다는 이유만으로 상위 태그를 자동 생성하지 않는다. 표시용 family는 운영 검색 노드나 제시 예산을 갖지 않는다.

## 통합·분해와 일반화

- material → surface_material. source 조건과 유리/잔해의 서로 다른 물건 소유자를 유지한다.
- body_framing → subject_framing. partner_framing → subject_framing 및 필요한 composition 관계. 성인·부위·참여자 수·연속성 조건을 보존한다.
- distance_narrative → 실제 간격·장벽은 proxemics, 관계·몸 방향을 표현한 부분은 해당 역할. 거리에서 마음을 자동 추론하지 않는다.
- quality → image_detail·skin_finish·image_artifact·color_grading·staging_degree 등의 구체 역할. frame_anchor_medium → 배치·포함 범위·광학·입자·반사 등의 실제 역할 또는 제약 계약.
- duty_prop_state → prop_state, transition_stage → transformation_stage, emotional_contradiction → character_contrast, person_origin → declared_person_background 등으로 일반화하거나 맥락을 명시한다.
- motion → physical_motion을 기본 역할로 정제하고, 기록된 궤적은 motion_rendering, 카메라 움직임·지지는 camera_movement로 분리한다.
- attire_context는 전통·역할·의례 복식의 맥락이며 전통 복식을 코스프레로 바꾸지 않는다. adult_presentation_context와 fetish_styling은 선택된 표현 맥락이며 연령 조건·가죽 소재·동의 판단과 구별한다.

통합에서 후보 ID·본문·출처를 유지한다. 같은 후보·목표 슬롯 관계가 겹치면 한 binding만 소유하도록 참조를 재연결한다. 폐지 슬롯을 운영 alias로 두지 않는다. provenance의 역사 슬롯 이름은 출처로 보존하며 운영 소비자와 구별한다.

## 추가 역할과 참고 범위

추가 30개는 background_element, environment_detail, season, historical_period, calendar_context, subject_count, age_presentation, gender_presentation, skin_tone, body_hair, garment_fit, garment_state, wardrobe_layering, light_quality, light_color, exposure, camera_distance, depth_of_field, spatial_depth, motion_rendering, camera_movement, image_artifact, image_detail, staging_degree, visual_hierarchy, visual_density, offscreen_context, narrative_clue, visible_text, shadow_relation이다.

[REFERENCE-COVERAGE.json](REFERENCE-COVERAGE.json)은 참고 대화의 45개 분류를 목표 역할과 모두 대응한다. “이미지 품질/Texture”라는 분류 안의 JPEG·grain·flare·피부 질감은 소유 공간별로 분리한다. “사진 매체” 안의 DSLR·스마트폰·다큐·화보도 장치·매체·목적·장르로 구별한다. “현실감”이나 “불완전성”은 여러 속성의 검토 범위이며 이를 또 하나의 만능 슬롯으로 만들지 않는다.

젖은 우산·빈 컵·낡은 신발은 관찰되는 현재 상태다. 비·식사 완료·오래 걸었다는 해석은 선언된 narrative_clue 맥락으로 다루며 자동 사실이 아니다. 성별 표현과 연령 표현도 실제 정체성·정확한 나이를 이미지에서 추정하는 역할이 아니다. offscreen_context는 기존 행위자와 요청 의미를 보존하며 새 사람·차량·소리를 임의로 추가하지 않는다.

새 역할에는 후보를 억지로 생성하거나 다른 슬롯의 본문을 복제하지 않는다. 이번 이관에서 실제로 표현한 역할에 연결할 수 있지만 전체 18,250개에 신규 다중 태그를 심사하는 일은 후속 4~8단계다.

## native 계약과 조건 분리

2단계에서 corpus·catalog·binding 계약을 새 native 버전으로 전환한다. 후보 자체의 조건은 canonical 후보 한 곳에서 소유하고 역할 조건은 binding에서 소유한다. 새 binding의 빈 조건이 후보 조건을 덮을 수 없게 한다. 후보 효과 역시 canonical 후보 한 곳에서 소유한다. 현재 모든 12,020개 binding 효과가 후보 효과와 같다는 사실을 먼저 확인했으므로 중복 효과 사본을 제거할 수 있다.

필수 for_any/for_all·필수 문맥·제외 조건은 후보에서 먼저 검사한다. 주체·성인·소유자 같은 필수 범위와 공통 슬롯의 분야 선호를 구별한다. 다른 역할의 binding 조건을 무관한 요청 역할에 그대로 전파하지 않는다. bundle에서 선언한 member 역할의 적용 조건과 intrinsic 조건은 모두 보존한다. body/age/actor count 관련 양성·음성 회귀를 통해 조건 우회를 검증한다.

역할 명세가 실제 query specification에 들어가고 영어·한국어 focus가 동일한 경계를 표현하게 한다. focus 투영·우선순위는 catalog에서 읽으며 새 역할을 추가할 때 숨은 상수 목록도 따로 수정하는 구조를 정리한다. 같은 이름의 core.camera.capture_mode나 사진 action 필드는 슬롯 ID와 구별한다.

운영 원본을 변경하는 2·3단계는 각각 인덱스·closure·native publication 검증을 끝내고 커밋한다. 텍스트가 동일한 벡터만 엄격한 recipe/model/hash 조건에서 재사용한다. 옛 질의 hash를 새 명세의 결과로 바꾸지 않고 새 context와 실제 query embedding을 만든다.

## 경계 검증 항목

| 양성 역할 | 혼동 음성 | 구별 기준 |
|---|---|---|
| 지정 모발 영역의 색 | 흰 의복 커프 | 같은 appearance라도 carrier/property가 다름 |
| 수신 표면 대비 입사 방향 | 얼룩 빛무늬 | source direction과 footprint shape 분리 |
| 물리 직조·표면 조직 | JPEG·영상 grain·공중 먼지 | 표면, 이미지 면, 광학 경로, 공기 공간 분리 |
| 카메라 거리 | waist-up shot scale | 물리 거리와 투영된 포함 범위 분리 |
| 초점면 선택 | 얕은 심도 | plane priority와 sharp depth extent 분리 |
| 조명 강도 | clipping·bloom | incident level과 recorded image state 분리 |
| 바람에 움직이는 천 | 천의 기록된 blur | 물리 상태와 image rendering 분리 |
| 명시된 행사 | 일반 검사·준비 단계 | occasion과 procedure/narrative phase 분리 |
| 게시 캡션 맥락 | 간판 글자 | 사진 밖 publication과 frame 안 text 분리 |
| 참가자 두 명 framing | 단일 주체 framing | 대상 목록과 participant count 보존 |
| 젖은 우산 | 비가 왔다는 확정 사실 | 관찰 상태와 서사 해석 분리 |
| 의복 소재·부착 구조 | 자동 fetish 의미 | 명시된 표현 맥락 필요 |

위 항목 외에도 모든 catalog 행의 includes/excludes/neighbors로 후보 중심 판단 기준을 제공한다. 코드 회귀·실제 hybrid 검색·exact full-scan oracle·필요 shard 읽기를 검증하되 이를 전체 후보 의미 품질이나 이미지 픽셀 평가로 보고하지 않는다.

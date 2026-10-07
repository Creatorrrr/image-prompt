# 시각 의미 카드 초안

상태: PROPOSED_NOT_INTEGRATED · 2026-10-07

이 문서는 출처 사실을 바탕으로 작성한 시각 연출 제안이다. 모든 카드가 운영 프로파일 한 개에 대응하는 것은 아니다. 계열 카드 안의 대안은 따로 좁혀 작성한다. 분위기 문맥과 보류 카드는 hard obligation으로 승격하지 않는다. 숨겨진 요소는 미관찰이며, 일부만 보이는 결과는 해당 카드의 전체 통과가 아니다.

## EG01 · 고요한 고딕의 선택형 문맥

- 처리: CONTEXT_ONLY · P0 · 후보 슬롯 제안: `genre`
- 소유자: `whole_request`
- 관찰 요소: The portrait retains the requested photographic medium. / Dark fabric, pale blossoms and bounded warm ornament may support the stated mood without replacing the frozen scene.
- 관계: mood_label → contextualizes → selected_scene_components
- 혼동 경계: gothic automatically adds graves, blood, heavy makeup or a cathedral / ethereal automatically makes a transparent ghost
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A01 · The Met — Symbolism](https://www.metmuseum.org/essays/symbolism), [R08 · PromptHero — gothic woman portrait prompt](https://prompthero.com/prompt/c04e50ca393), [R09 · NanoPrompts — AI Gothic and Dark Art Prompts Guide](https://nanoprompts.net/pt/articles/ai-gothic-dark-art/), [R10 · Morphic — Witchcore portrait AI Images](https://morphic.com/br/resources/images/witchcore-portrait-image)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG02 · 평온한 우울의 관찰 가능한 연출

- 처리: CONTEXT_ONLY · P0 · 후보 슬롯 제안: `expression`
- 소유자: `subject.face`, `subject.shoulders`, `scene`
- 관찰 요소: Visible brows and mouth remain relatively relaxed. / A composed posture and restrained scene accents support the requested quiet mood.
- 관계: face_configuration → belongs_to → subject; scene_accents → support → requested_mood
- 혼동 경계: automatic tears, frowning or collapse / a facial configuration proves the person's real emotional state
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A01 · The Met — Symbolism](https://www.metmuseum.org/essays/symbolism), [R06 · Bella Kotak — The sun dances and the moon kisses](https://www.bellakotakphotography.com/blog/moon-kisses), [R07 · Kirsty Mitchell — Wonderland](https://www.kirstymitchell.art/wonderland/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG03 · 상징주의의 사진적 차용

- 처리: CONTEXT_ONLY · P1 · 후보 슬롯 제안: `aesthetic_trend`
- 소유자: `background.panel`, `scene.flowers`
- 관찰 요소: Selected flowers and ornament carry an authored symbolic role. / The requested skin, hair and fabric remain photographic surfaces.
- 관계: symbolic_motif → carried_by → declared_scene_object
- 혼동 경계: style label replaces the entire image with an oil painting / a flower has one universal psychological meaning
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A01 · The Met — Symbolism](https://www.metmuseum.org/essays/symbolism)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG04 · 물체 프레임에 이어지는 식물 곡선

- 처리: REUSE · P1 · 후보 슬롯 제안: `prop`
- 소유자: `artifact.frame`, `artifact.ornament`
- 관찰 요소: Long stem-like curves continue into the declared object frame. / Adjacent floral lines follow the same flowing structure.
- 관계: stem_curve → continues_into → artifact.frame
- 혼동 경계: unrelated background vine is evidence for the artifact / all S curves imply Art Nouveau authenticity
- 기존 ID: `orn_gd54`, `orn_profile_gd54`
- 근거: [A02 · V&A — The Whiplash](https://www.vam.ac.uk/articles/the-whiplash/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG05 · 금박 화면의 식물·여백 배치

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `background.screen`, `screen.painted_motifs`, `optional_scene.branch`
- 관찰 요소: A bounded gold-ground panel carries painted floral or branch motifs. / Unpainted gold intervals remain visible between those motif groups; actual scene branches retain separate owners.
- 관계: painted_floral_motifs → lie_on → gold_ground_panel; physical_branch → is_separate_from → painted_branch_motif
- 혼동 경계: dense gilded wallpaper across the entire room / a screen motif changes the subject's ethnicity or historical identity
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R12 · The Met — Rinpa Painting Style](https://www.metmuseum.org/essays/rinpa-painting-style), [A03 · Tokyo Fuji Art Museum — Folding Screen with Design of Plum Tree](https://www.fujibi.or.jp/en/collection/artwork/03580/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG06 · 의식적인 초상 프레이밍

- 처리: CONTEXT_ONLY · P1 · 후보 슬롯 제안: `composition`
- 소유자: `background.frame`, `subject`
- 관찰 요소: A distinct enclosing frame surrounds a readable portrait region. / Its central opening remains separate from surrounding ornament.
- 관계: background.frame → surrounds → subject_portrait_region
- 혼동 경계: religious affiliation or halo inferred from a formal frame / the frame covers the requested face
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R13 · Belvedere — Judith](https://sammlung.belvedere.at/objects/3492/judith), [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG07 · 위협·졸음과 분리한 낮은 윗눈꺼풀

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `expression`
- 소유자: `subject.eyes`, `subject.brows`, `subject.mouth`
- 관찰 요소: The upper eyelid margins cover part of the visible irises. / Visible brow and mouth regions remain relaxed rather than snarling or grinning.
- 관계: upper_lid_margin → partly_occludes → same_eye_iris
- 혼동 경계: menacing distant gaze substituted for neutral lowering / closed eyes or sleep substituted for visible irises
- 기존 ID: `half_lidded_menacing_distant_gaze`, `sleepy_half_lidded_eyes`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG08 · 머리 회전과 구분한 위쪽 시선

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `expression`
- 소유자: `subject.eyes`, `camera_axis`
- 관찰 요소: Both visible eye regions address the same declared off-camera direction. / The gaze direction is defined separately from head yaw and pitch.
- 관계: eye_direction → points_toward → declared_off_camera_target; head_orientation → is_separate_from → eye_direction
- 혼동 경계: chin lifting alone counts as upward gaze / each eye points to a different target
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L07 · Nikon — What Is Focal Length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners), [L08 · Canon — Depth of Field](https://files.canon-europe.com/files/webcontent/rf-lens-world/knowledge/depth-of-field/index.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG09 · 얼굴·몸통 방향의 축 분리

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `body_orientation`
- 소유자: `subject.head`, `subject.neck`, `subject.torso`, `camera_axis`
- 관찰 요소: Head yaw, pitch and roll are separately declared relative to the camera. / The neck connects continuously to a separately oriented shoulder plane.
- 관계: head → connected_by → subject.neck; head_yaw → measured_relative_to → camera_axis; torso_yaw → measured_relative_to → camera_axis
- 혼동 경계: three-quarter profile conflated with a three-quarter-length crop / head yaw is added twice as camera angle and relative neck turn
- 기존 ID: `pc_pc02_owner_relation`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L07 · Nikon — What Is Focal Length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners), [L08 · Canon — Depth of Field](https://files.canon-europe.com/files/webcontent/rf-lens-world/knowledge/depth-of-field/index.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG10 · 작은 입술 간격과 이완

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `expression`
- 소유자: `subject.upper_lip`, `subject.lower_lip`
- 관찰 요소: The upper and lower lip margins remain separate along a small readable gap. / Mouth corners stay relaxed without a wide open mouth.
- 관계: upper_lip_margin → separated_from → lower_lip_margin
- 혼동 경계: a pout or a broad open mouth / an exact millimeter measurement inferred from uncalibrated pixels
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG11 · 감은 눈의 별도 상태

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `eye_detail`
- 소유자: `subject.eyes`, `subject.posture`
- 관찰 요소: Both selected eye apertures are closed. / The head and shoulders retain the declared composed support.
- 관계: closed_lid_edges → cover → eye_apertures
- 혼동 경계: half-lidded irises count as closed eyes / sleep, illness or unconsciousness inferred
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG12 · 눈꺼풀 덮임 형태와 일시 자세

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `eye_detail`
- 소유자: `subject.upper_lid_fold`, `subject.upper_lid_margin`
- 관찰 요소: An explicitly requested upper-lid fold lies over part of the eyelid surface. / The movable lid margin's position remains independently declared.
- 관계: upper_lid_fold → overlies → upper_lid_surface; lid_fold_shape → is_separate_from → lid_aperture_state
- 혼동 경계: all lowered lids are hooded eyelid anatomy / fixed ethnicity or health inferred from eyelid form
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG13 · 좁은 중앙 수직축의 흉상

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `composition`
- 소유자: `image.frame`, `subject.bust`, `background.vertical_element`
- 관찰 요소: The declared bust crop leaves a readable face and neck. / The selected vertical background element is aligned with the frame's central region.
- 관계: bust_crop → bounded_by → image.frame; background.vertical_element → aligned_with → frame_vertical_axis
- 혼동 경계: a full-body crop substitutes for a bust / the subject must be perfectly mirrored to be centered
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L07 · Nikon — What Is Focal Length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners), [L08 · Canon — Depth of Field](https://files.canon-europe.com/files/webcontent/rf-lens-world/knowledge/depth-of-field/index.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG14 · 꽃가지 아치와 얼굴 여백

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `composition`
- 소유자: `scene.branches`, `subject.face`
- 관찰 요소: Attached woody branch paths curve around the portrait region. / Branch groups leave the requested facial features readable through their opening.
- 관계: flowers → attached_to → scene.branches; branch_arcs → bracket → subject.face
- 혼동 경계: a floating decorative flower border / a wreath attached to the head when scene framing was requested
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R01 · Kew POWO — Prunus mume](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:730000-1/general-information), [R06 · Bella Kotak — The sun dances and the moon kisses](https://www.bellakotakphotography.com/blog/moon-kisses), [R07 · Kirsty Mitchell — Wonderland](https://www.kirstymitchell.art/wonderland/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG15 · 좌우의 어두운 여백

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `composition`
- 소유자: `image.left_margin`, `image.right_margin`, `subject`
- 관찰 요소: Low-detail dark intervals remain beside the portrait. / Those intervals separate the primary face from peripheral ornament.
- 관계: dark_intervals → separate → portrait_and_ornament
- 혼동 경계: a black vignette counts as scene negative space in every case / background uniformly loses all material detail
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG16 · 비대칭 꽃군의 균형

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `composition`
- 소유자: `scene.left_flower_group`, `scene.right_flower_group`, `subject`
- 관찰 요소: Two selected floral groups retain unequal extents or heights. / Their distribution leaves the face as the declared focal region.
- 관계: left_flower_group → differs_in_extent_from → right_flower_group
- 혼동 경계: equal mirrored flower groups / a specific numerical balance ratio is universal
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R12 · The Met — Rinpa Painting Style](https://www.metmuseum.org/essays/rinpa-painting-style), [A03 · Tokyo Fuji Art Museum — Folding Screen with Design of Plum Tree](https://www.fujibi.or.jp/en/collection/artwork/03580/), [R06 · Bella Kotak — The sun dances and the moon kisses](https://www.bellakotakphotography.com/blog/moon-kisses), [R07 · Kirsty Mitchell — Wonderland](https://www.kirstymitchell.art/wonderland/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG17 · 얼굴·레이스·꽃의 초점 평면

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `focus`
- 소유자: `subject.near_eye`, `scene.foreground`, `scene.background_flowers`
- 관찰 요소: The selected near eye stays readable at its focus plane. / A separate farther flower plane is visibly softer without duplicating physical flowers.
- 관계: background_flowers → farther_from_camera_than → subject.near_eye; foreground_plane → is_separate_from → eye_focus_plane
- 혼동 경계: all foreground lace and eyes are guaranteed equally sharp at any distance / bokeh light discs substitute for blurred botanical forms / pe_background_bokeh is a related light-disc alternative, not an equivalent botanical-defocus profile.
- 기존 ID: `pc_pc19_owner_relation`
- 근거: [L07 · Nikon — What Is Focal Length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners), [L08 · Canon — Depth of Field](https://files.canon-europe.com/files/webcontent/rf-lens-world/knowledge/depth-of-field/index.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG18 · 목덜미의 낮은 번

- 처리: ENRICH_EXISTING · P0 · 후보 슬롯 제안: `hair_style`
- 소유자: `subject.hair`, `subject.nape`
- 관찰 요소: Gathered hair forms a compact coiled mass near the nape. / The bun connects to the same subject's gathered hair rather than floating above the head.
- 관계: bun_mass → located_near → subject.nape; gathered_hair → continues_into → bun_mass
- 혼동 경계: a high topknot / a detached ornamental flower is mistaken for the bun
- 기존 ID: `low_bun_hair`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG19 · 눈썹 높이의 일자 앞머리

- 처리: ENRICH_EXISTING · P0 · 후보 슬롯 제안: `hair_style`
- 소유자: `subject.front_hair`, `subject.forehead`, `subject.brows`
- 관찰 요소: The front hair descends over the forehead to a blunt transverse edge. / The edge lies at the explicitly selected brow-relative height.
- 관계: front_hair → overlies → subject.forehead; fringe_edge → located_relative_to → subject.brows
- 혼동 경계: a bob haircut is added because a blunt fringe was selected / eyes covered when brow-level ends were requested
- 기존 ID: `ca_blunt_fringe`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG20 · 옆머리 가닥과 리본 분리

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `hair_style`
- 소유자: `subject.side_hair`, `subject.cheek`
- 관찰 요소: Narrow hair strands descend beside the cheek from traceable hair roots. / Those strands retain hair-like filament edges distinct from flat ribbons.
- 관계: side_hair_strands → descend_beside → subject.cheek
- 혼동 경계: flat fabric ribbons count as hair tendrils / strands emerge from cheeks or shoulders
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG21 · 헤어 매듭에 연결된 긴 리본

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `hair_style`
- 소유자: `subject.hair_tie`, `hair_tie.ribbon_ends`
- 관찰 요소: Flat fabric ribbon ends continue from a readable hair fastening. / The same ribbon ends hang beside the subject with coherent gravity.
- 관계: ribbon_ends → continue_from → subject.hair_tie
- 혼동 경계: unattached strips floating in the background / a tie adds a braid or twin tails automatically
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG22 · 검은 머리의 절제된 윤기

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `hair_color`
- 소유자: `subject.hair`, `acting_light`
- 관찰 요소: The hair mass retains a dark local color. / Selected strands carry restrained light bands while individual hair edges remain readable.
- 관계: light_band → follows → hair_surface_orientation
- 혼동 경계: wet clumping inferred solely from shine / lacquered plastic mass substitutes for readable hair
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG23 · 피부의 매트감과 실제 질감

- 처리: REUSE · P0 · 후보 슬롯 제안: `makeup_style`
- 소유자: `subject.skin`, `facial_light`
- 관찰 요소: Selected skin regions keep fine nonuniform surface detail. / Specular highlights remain restrained without removing the facial form.
- 관계: fine_texture → lies_on → subject.skin; light_gradient → models → facial_form
- 혼동 경계: plastic smoothing / all pale skin becomes uniformly white or medically interpreted
- 기존 ID: `pe_texture_preserving_tone_evening_relation`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG24 · 차가운 피부 기조와 따뜻한 반사

- 처리: ENRICH_EXISTING · P1 · 후보 슬롯 제안: `color`
- 소유자: `subject.skin`, `warm_light`, `background`
- 관찰 요소: The face retains its selected relatively cool base tendency. / Warm reflected or contour light affects bounded source-facing skin regions.
- 관계: warm_light → illuminates → source_facing_skin; skin_local_color → is_separate_from → light_color
- 혼동 경계: a global orange skin tint / warm skin makeup is confused with light reflected from a gold surface
- 기존 ID: `cr_cool_subject`, `cr_colored_rim`
- 근거: [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG25 · 눈 화장·볼 색의 국소 범위

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `makeup_style`
- 소유자: `subject.eyelid_cosmetics`, `subject.cheeks`
- 관찰 요소: Selected muted cosmetic pigment remains in its declared eyelid or cheek region. / The transition stays soft while the natural skin boundary remains readable.
- 관계: cosmetic_pigment → bounded_within → declared_face_region
- 혼동 경계: background mauve washes across all skin / heavy dark makeup added from the gothic label
- 기존 ID: `smoky_eye_diffused_gradient`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG26 · 입술의 낮은 채도와 새틴·매트 마감

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `lip_finish`
- 소유자: `subject.lips`
- 관찰 요소: The selected rose or berry pigment stays inside the declared lip region. / A chosen restrained finish remains distinguishable from wet mirror-like gloss.
- 관계: lip_pigment → bounded_within → subject.lips
- 혼동 경계: parted lips infer desire or intent / matte lip pigment removes the natural lip structure
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG27 · 높은 칼라와 레이스 가장자리

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `garment_detail`
- 소유자: `subject.blouse_collar`, `subject.neck`, `collar.lace`
- 관찰 요소: A standing collar forms a garment boundary around the lower neck. / Its lace pattern and selected scalloped edge remain attached to the collar.
- 관계: standing_collar → surrounds → lower_neck; lace_edge → attached_to → collar
- 혼동 경계: all Victorian clothing must have the same high collar / a neck tattoo or jewelry substitutes for the collar
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A04 · The Met — Death Becomes Her labels](https://libmma.contentdm.oclc.org/digital/api/collection/p16028coll12/id/18303/download), [A11 · The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342), [A05 · LACMA — Design Dispatch Exploring Lace](https://unframed.lacma.org/2008/10/23/design-dispatch-exploring-lace)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG28 · 비치는 천과 지정된 하층

- 처리: REUSE · P0 · 후보 슬롯 제안: `surface_material`
- 소유자: `subject.outer_cloth`, `subject.declared_underlayer`
- 관찰 요소: Open cells or translucent cloth remain physically present through edges and folds. / Only the explicitly declared lower layer is visible through the outer textile.
- 관계: outer_cloth → lies_in_front_of → declared_underlayer; transmission → passes_through → outer_cloth
- 혼동 경계: sheer automatically removes lining or adds body exposure / flat black floral print on opaque fabric substitutes for open lace
- 기존 ID: `sheer_garment_optical_layering`, `clothing_ct079_v1`
- 근거: [A05 · LACMA — Design Dispatch Exploring Lace](https://unframed.lacma.org/2008/10/23/design-dispatch-exploring-lace), [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG29 · 상복 자료의 쿠튀르 차용

- 처리: CONTEXT_ONLY · P1 · 후보 슬롯 제안: `costume_style`
- 소유자: `declared_garment`, `optional_scene_context`
- 관찰 요소: Selected dark textiles can reference historically documented mourning clothing. / Historical staging, wearer circumstance and period fidelity remain separately specified.
- 관계: historical_reference → informs → selected_textile_choices
- 혼동 경계: a black dress proves bereavement / Victorian, Edwardian and all mourning stages are merged
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A04 · The Met — Death Becomes Her labels](https://libmma.contentdm.oclc.org/digital/api/collection/p16028coll12/id/18303/download), [A11 · The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG30 · 어깨에 붙은 꽃 코르사주

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `garment_detail`
- 소유자: `subject.right_shoulder_garment`, `corsage`
- 관찰 요소: A compact floral group is attached to the selected garment shoulder. / Its petal or fabric shapes stay localized at that attachment.
- 관계: corsage → attached_to → declared_shoulder_garment
- 혼동 경계: right in camera coordinates silently swaps the wearer's right / flowers float beside the shoulder or cover the whole torso
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG31 · 천 장미와 식물 꽃의 구별

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `garment_detail`
- 소유자: `garment.fabric_rosette`, `scene.living_flower`
- 관찰 요소: A selected garment rosette is formed by gathered or folded fabric. / A separate living flower retains its own botanical stem and petal owner.
- 관계: folded_fabric → forms → garment.fabric_rosette; living_flower → attached_to → botanical_stem
- 혼동 경계: fabric flowers grow from skin / all corsage flowers are automatically living plants
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG32 · 샹티이형 망 바탕과 꽃 모티프

- 처리: REUSE · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.lace_net`, `lace.floral_motifs`
- 관찰 요소: Fine floral motifs attach to a continuous open net ground. / The small net cells remain readable between larger motifs.
- 관계: floral_motif → attached_to → continuous_net_ground
- 혼동 경계: guipure bars without a continuous ground net / a particular manufacturing process or fiber inferred from appearance
- 기존 ID: `orn_gd31`, `orn_profile_gd31`
- 근거: [A05 · LACMA — Design Dispatch Exploring Lace](https://unframed.lacma.org/2008/10/23/design-dispatch-exploring-lace)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG33 · 튈의 미세한 열린 망

- 처리: REUSE · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.tulle_panel`
- 관찰 요소: Fine threads form a repeated network of actual open cells. / The mesh panel retains an attached edge, seam or fold.
- 관계: threads → bound → open_cells; panel_edge → belongs_to → garment.tulle_panel
- 혼동 경계: dense floral lace automatically appears / opaque polka dots substitute for mesh holes
- 기존 ID: `clt_ct090_v2`, `clothing_ct090_v2`
- 근거: [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG34 · 튈 위에 잡힌 미세 주름

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `garment_detail`
- 소유자: `garment.tulle_panel`, `panel.pleats`
- 관찰 요소: Narrow repeated pleat folds traverse a selected tulle panel. / The same panel retains a distinguishable fine mesh surface.
- 관계: pleat_ridges → formed_in → same_tulle_panel
- 혼동 경계: woven corded silk ribs substitute for pleat folds / a pleated skirt appears when a blouse panel was selected
- 기존 ID: `clothing_ct090_v2`
- 근거: [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon), [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG35 · 각진 주름을 유지하는 얇은 오간자

- 처리: REUSE · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.sheer_panel`
- 관찰 요소: A light transparent or translucent panel holds relatively crisp folds. / The panel's attached seams and edges remain visible.
- 관계: angular_folds → belong_to → garment.sheer_panel
- 혼동 경계: soft fluid chiffon drape / fiber identity or exact weave inferred from a distant view
- 기존 ID: `clothing_ct091_v1`
- 근거: [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG36 · 작은 유동 주름의 시폰

- 처리: REUSE · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.translucent_panel`
- 관찰 요소: A soft translucent cloth drops into small flowing folds. / The hanging cloth has a traceable garment attachment.
- 관계: fluid_folds → hang_from → declared_garment_attachment
- 혼동 경계: crisp self-supporting organza folds / fog or transparent glass replaces the cloth
- 기존 ID: `clothing_ct091_v2`
- 근거: [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG37 · 낮은 광택의 크레이프 표면

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.crape_like_panel`
- 관찰 요소: The selected dark cloth has a low-sheen finely irregular surface. / Its folds remain fabric forms with restrained highlights.
- 관계: surface_texture → lies_on → garment.crape_like_panel
- 혼동 경계: glossy satin / black color alone proves historical mourning crape
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A04 · The Met — Death Becomes Her labels](https://libmma.contentdm.oclc.org/digital/api/collection/p16028coll12/id/18303/download), [A11 · The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342), [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG38 · 골이 있는 실크형 표면

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.ribbed_panel`
- 관찰 요소: Fine parallel surface ribs follow one cloth panel. / Broader cloth folds remain separate from the fine rib spacing.
- 관계: fine_ribs → lie_on → garment.ribbed_panel
- 혼동 경계: garment pleats substituted for woven-looking ribs / fiber authenticity inferred from visible ribs
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A04 · The Met — Death Becomes Her labels](https://libmma.contentdm.oclc.org/digital/api/collection/p16028coll12/id/18303/download), [A11 · The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342), [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG39 · 벨벳 결·크러시·데보레의 경계

- 처리: REUSE · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `garment.velvet_panel`
- 관찰 요소: Dense short pile shows fold-dependent sheen. / Crushed-pile variation or transparent patterned regions are separately requested variants.
- 관계: pile_sheen → varies_with → cloth_fold_orientation
- 혼동 경계: all velvet must be crushed or burnout / fur or sharp patent reflections replace short velvet pile
- 기존 ID: `clt_ct089_v2`, `clothing_ct089_v2`
- 근거: [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG40 · 식물 자수와 부착 구조

- 처리: REUSE · P1 · 후보 슬롯 제안: `garment_detail`
- 소유자: `garment.ground_cloth`, `garment.embroidery`
- 관찰 요소: Raised thread paths form selected botanical motifs above the ground cloth. / Visible anchor stitches or edge relief connect the motif to the same carrier.
- 관계: raised_threads → attached_to → garment.ground_cloth
- 혼동 경계: flat floral ink print / thread relief is evidence of metal filigree
- 기존 ID: `orn_gd33`, `orn_profile_gd33`, `orn_gd34`, `orn_profile_gd34`
- 근거: [A05 · LACMA — Design Dispatch Exploring Lace](https://unframed.lacma.org/2008/10/23/design-dispatch-exploring-lace), [A06 · Textile Research Centre — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [A07 · Getty AAT — Organza 300310123](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [A08 · MFA CAMEO — Chiffon](https://cameo.mfa.org/wiki/Chiffon)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG41 · 잎 적은 목질 가지의 매화

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `prop`
- 소유자: `scene.mume_branch`, `branch.flowers`
- 관찰 요소: Small pale flowers attach at intervals along a woody branch. / The selected flowering branch is leafless or sparsely leafed rather than a leafy bouquet.
- 관계: small_flowers → attached_to → same_woody_branch
- 혼동 경계: large magnolia cups / a fixed five-petal count imposed on every cultivar
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R01 · Kew POWO — Prunus mume](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:730000-1/general-information)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG42 · 동백의 큰 꽃과 광택 잎

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.camellia_branch`, `branch.flowers`, `branch.leaves`
- 관찰 요소: Selected larger flowers remain connected to a branching stem. / Broad glossy leaves retain their own leaf boundaries on the same branch.
- 관계: flowers → borne_on → camellia_branch; leaves → attached_to → camellia_branch
- 혼동 경계: small blossoms on a leafless mume twig / flower petal count fixed across all cultivars
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R02 · RHS — Camellia japonica](https://www.rhs.org.uk/plants/2845/camellia-japonica/details)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG43 · 목련의 큰 꽃 구조

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.magnolia_flower`, `flower.branch`
- 관찰 요소: A selected magnolia variant has relatively large distinct floral segments. / The cup, bowl or star form is chosen explicitly for that variant.
- 관계: large_flower → attached_to → declared_branch
- 혼동 경계: all magnolia forms merged into one petal count / tiny repeated plum blossoms
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R03 · RHS — How to grow magnolias](https://www.rhs.org.uk/plants/magnolia/growing-guide)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG44 · 처진 종 모양 꽃열

- 처리: DEFER_SOURCE_CONFIRMATION · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.flower_stalk`, `stalk.bell_flowers`
- 관찰 요소: Small bell-like flowers hang down along the selected flower stalk. / The selected flower mouths retain a downward orientation.
- 관계: bell_flowers → hang_from → same_stalk
- 혼동 경계: upright lily trumpets / botanical species qualified from a search snippet alone
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R05 · Woodland Trust — Lily of the valley](https://www.woodlandtrust.org.uk/trees-woods-and-wildlife/plants/wild-flowers/lily-of-the-valley/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG45 · 붉은 기운이 남은 어두운 장미

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.rose`, `rose.petals`
- 관찰 요소: Layered rose petals preserve a dark red or purple tendency in illuminated regions. / The selected near-black petals retain distinguishable folds.
- 관계: petal_layers → form → same_rose_bloom
- 혼동 경계: uniform dead black blob / natural black pigmentation or frost inferred from the color label
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R04 · RHS — Rosa Black Prince](https://www.rhs.org.uk/plants/47875/rosa-black-prince-hp/details)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG46 · 작은 꽃의 성긴 가지 무리

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.fine_flower_spray`
- 관찰 요소: Fine branching stems carry many small separated flowers. / Open intervals remain between the tiny flower groups.
- 관계: tiny_flowers → attached_to → fine_branching_stems
- 혼동 경계: a dense hydrangea head / purple hue automatically proves dyeing or a natural species-wide color
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R11 · RHS — Cut flowers growing and selection](https://www.rhs.org.uk/plants/for-places/cut-flowers-growing), [R06 · Bella Kotak — The sun dances and the moon kisses](https://www.bellakotakphotography.com/blog/moon-kisses), [R07 · Kirsty Mitchell — Wonderland](https://www.kirstymitchell.art/wonderland/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG47 · 고사리 잎과 장식 잎

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.frond`, `artifact.leaf_motif`
- 관찰 요소: An explicitly selected frond has repeated smaller leaf divisions along its central axis. / A decorative leaf motif remains attached to its separately declared artifact.
- 관계: leaf_divisions → arranged_along → frond_axis; decorative_leaf → attached_to → artifact
- 혼동 경계: golden artifact leaves are living fern fronds / a botanical species inferred from generic ornament
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG48 · 서리·이슬·말린 꽃잎의 독립 상태

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `texture`
- 소유자: `declared_flower.petals`, `petal_surface_detail`
- 관찰 요소: The explicitly selected surface state has localized crystals, droplets or dry curled edges. / That state stays on the same named petal owner.
- 관계: surface_state → bounded_on → declared_petals
- 혼동 경계: near-black automatically means dried or frost-covered / glitter substitutes for ice; grains substitute for droplets
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG49 · 국소 필리그리의 선재·틈

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `wearable_accessory`
- 소유자: `declared_jewelry`, `jewelry.wire_paths`
- 관찰 요소: Fine curved members form a bounded jewelry motif. / Background or a separately declared backing remains distinguishable between those members.
- 관계: wire_paths → bound → local_open_intervals
- 혼동 경계: printed golden curls / a ring, choker or religious emblem added automatically
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG50 · 구슬·진주의 반복 부품

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `wearable_accessory`
- 소유자: `declared_accessory`, `accessory.beads`
- 관찰 요소: Small separate bead-like elements form the requested string or local embroidery. / Each bead retains a boundary distinct from the carrier.
- 관계: beads → attached_to → declared_accessory_carrier
- 혼동 경계: white image grain counts as seed pearls / jet-style implies verified jet material
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A04 · The Met — Death Becomes Her labels](https://libmma.contentdm.oclc.org/digital/api/collection/p16028coll12/id/18303/download), [A11 · The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342), [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG51 · 받침 안의 카메오형 부조

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `wearable_accessory`
- 소유자: `declared_accessory.mount`, `accessory.relief`
- 관찰 요소: A bounded relief form projects above a contrasting field. / Its mounting border remains distinct from the same relief.
- 관계: relief_form → raised_above → accessory_field; mounting_border → surrounds → relief_field
- 혼동 경계: painted face icon substitutes for raised relief / a skull or cross introduced without request
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG52 · 황동·은·청동의 세월 표면

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `surface_material`
- 소유자: `declared_metal_object.surface`
- 관찰 요소: Uneven dulling or selected patina remains bounded on the metal surface. / Material highlights follow object geometry rather than becoming light sources.
- 관계: surface_variation → bounded_on → metal_object
- 혼동 경계: gold color proves brass alloy / all old metals have the same green corrosion
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A12 · CCI — Caring for Metal Objects](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG53 · 빛을 받는 금박형 패널

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `surface_material`
- 소유자: `background.panel`, `panel.metallic_leaf_surface`, `acting_light`
- 관찰 요소: A bounded panel has subtly uneven reflective leaf-like surface patches. / The surface response follows illumination while the panel boundary remains readable.
- 관계: reflective_leaf_surface → lies_on → background.panel; light → reflected_by → panel.surface
- 혼동 경계: yellow emitted light counts as a gold-leaf material / gold material proves a particular fabrication technique or provenance
- 기존 ID: `tarnished_gold_leaf_surface`
- 근거: [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG54 · 구획과 이음이 있는 금빛 모자이크

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `surface_material`
- 소유자: `background.panel`, `panel.tesserae`
- 관찰 요소: Small adjacent pieces retain repeated tile boundaries on the panel. / Light response may vary between pieces without merging them into one smooth sheet.
- 관계: tesserae → adjacent_within → same_panel_boundary
- 혼동 경계: reptile scales inferred from mosaic scale texture / continuous cracked gold leaf counts as separate tiles
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A10 · French Ministry of Culture — Making Tesserae](https://archeologie.culture.gouv.fr/mosquee-omeyyades/en/making-tesserae)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG55 · 선택 부위의 금박 벗겨짐

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `texture`
- 소유자: `panel.leaf_layer`, `panel.substrate`
- 관찰 요소: Irregular losses interrupt selected parts of the reflective layer. / A distinguishable lower substrate remains inside the loss boundaries.
- 관계: leaf_layer_loss → reveals → same_panel_substrate
- 혼동 경계: gold-colored dust floats off every surface / entire room becomes abandoned because one panel is weathered
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG56 · 식물 형태를 한 금빛 장식 부재

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `prop`
- 소유자: `artifact.branch_shaped_member`
- 관찰 요소: A branch-shaped object retains a solid artifact boundary. / Its metallic surface response stays on that same member.
- 관계: metallic_surface → bounded_on → branch_shaped_artifact
- 혼동 경계: gold lighting transforms a living twig into metal / living plant growth inferred from a leaf-shaped artifact
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [A09 · V&A — A Guide to Metalworking Techniques](https://www.vam.ac.uk/articles/metalworking-techniques), [A02 · V&A — The Whiplash](https://www.vam.ac.uk/articles/the-whiplash/)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG57 · 차콜 배경과 어두운 재질

- 처리: ENRICH_EXISTING · P0 · 후보 슬롯 제안: `location`
- 소유자: `background.backdrop`, `subject.outline`
- 관찰 요소: The chosen background remains predominantly dark with restrained local material information. / Small lightness or material differences keep the subject boundary readable.
- 관계: subject_contour → separated_from → dark_backdrop
- 혼동 경계: all dark backgrounds are seamless paper / a pure black clipping region erases required contour detail
- 기존 ID: `cr_dark_on_dark`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG58 · 얕은 벽감의 공간 구조

- 처리: DEFER_DOMAIN_REVIEW · P1 · 후보 슬롯 제안: `location`
- 소유자: `background.niche`, `niche.opening`
- 관찰 요소: A bounded recessed region has a readable front opening and interior depth. / Selected ornament belongs to the opening rather than filling unrelated walls.
- 관계: niche_interior → recedes_behind → opening_plane
- 혼동 경계: a whole cathedral appears from the word niche / religious affiliation inferred from an architectural alcove
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG59 · 경계가 있는 타원 거울

- 처리: REUSE · P1 · 후보 슬롯 제안: `prop`
- 소유자: `scene.mirror`, `subject.reflected_face`
- 관찰 요소: The mirror has a distinct physical boundary. / Any selected reflection remains geometrically related to the same subject and scene.
- 관계: reflection → contained_within → mirror_boundary
- 혼동 경계: another person's face appears without a mirror owner / mirror introduced by antique mood alone
- 기존 ID: `pc_pc22_owner_relation`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG60 · 인물 뒤 가려지는 세로 발광 틈

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `light_shape`
- 소유자: `background.emissive_slit`, `subject.silhouette`, `background.panel`
- 관찰 요소: A narrow vertically extended luminous aperture lies behind the subject. / The subject occludes that aperture where their silhouettes overlap; visible segments belong to the same aligned opening.
- 관계: emissive_slit → behind → subject; subject.silhouette → occludes → overlapping_slit_region; slit_opening → bounded_by → background.panel
- 혼동 경계: unbroken stripe drawn over the face / golden rim without any visible selected aperture / a visible aperture guarantees wraparound light on every contour
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L02 · Aputure — Spotlight Max Operating Instructions](https://help.aputure.com/en/spotlight-max-operating-instructions), [L03 · Profoto — Softbox Strip](https://www.profoto.com/us/en/products/light-shaping-tools/softboxes/profoto-softbox-strip)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG61 · 선택된 턱·목·머리 윤곽의 역광

- 처리: REUSE · P0 · 후보 슬롯 제안: `light_direction`
- 소유자: `rear_source`, `subject.hair_edge`, `subject.neck_edge`, `subject.jaw_edge`
- 관찰 요소: A selected rear light contribution reaches source-facing contour segments. / The warmer rim remains distinct from the front-lit face interior.
- 관계: rear_source → illuminates → source_facing_contours; front_fill → illuminates → face_interior
- 혼동 경계: all silhouette boundaries glow equally / outline painted on the image plane independent of source
- 기존 ID: `pe_rear_rim`, `cr_colored_rim`
- 근거: [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L02 · Aputure — Spotlight Max Operating Instructions](https://help.aputure.com/en/spotlight-max-operating-instructions), [L03 · Profoto — Softbox Strip](https://www.profoto.com/us/en/products/light-shaping-tools/softboxes/profoto-softbox-strip)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG62 · 입체감을 남긴 부드러운 정면 보조광

- 처리: REUSE · P0 · 후보 슬롯 제안: `light_type`
- 소유자: `front_fill_source`, `subject.face`
- 관찰 요소: The acting frontal or near-frontal source produces broad shadow-edge transitions. / Facial form retains gradual light differences without specular clipping.
- 관계: front_fill_source → illuminates → face_front_planes
- 혼동 경계: completely flat uniform face color / out-of-focus eyes substitute for a soft source
- 기존 ID: `soft_light_shadow_edge_relation`
- 근거: [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG63 · 로우키 조명과 검정 톤 바닥 분리

- 처리: NEW_SIBLING · P0 · 후보 슬롯 제안: `lighting`
- 소유자: `scene.light_distribution`, `image_plane.dark_tones`
- 관찰 요소: The scene's selected dark regions dominate the composition. / The output black floor is a separately selected tonal property.
- 관계: scene_illumination → is_separate_from → output_black_floor
- 혼동 경계: low key always crushes blacks / lifted blacks add a bright physical fill lamp
- 기존 ID: `pe_lifted_black_floor_relation`
- 근거: [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html), [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG64 · 따뜻한 배경과 상대적으로 차가운 얼굴

- 처리: REUSE · P1 · 후보 슬롯 제안: `color`
- 소유자: `background.region`, `subject.face`, `source_contributions`
- 관찰 요소: Selected background regions retain a warmer tendency than the face interior. / Light color footprints follow surfaces and occlusion instead of globally recoloring the face.
- 관계: background_color_role → warmer_than → face_interior_role; source_footprint → follows → receiving_surface
- 혼동 경계: all skin becomes blue / skin tone prescribed from ethnicity rather than the frozen request
- 기존 ID: `cr_cool_subject`, `cr_two_color_lights`
- 근거: [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG65 · 확산·초점 흐림·필름 할레이션의 분리

- 처리: ENRICH_EXISTING · P0 · 후보 슬롯 제안: `quality`
- 소유자: `image_plane.highlight_neighborhood`, `subject.focus_plane`
- 관찰 요소: A selected diffusion variant softens specified contrast or highlight transitions. / Focus-plane eye or textile detail stays readable; a halo is required only for a separately selected halo-producing variant.
- 관계: diffusion_effect → bounded_to → selected_picture_regions; focus_state → is_separate_from → highlight_spread
- 혼동 경계: all diffusion must create a red halo / global blur, thick fog or flare ghosts count as restrained diffusion
- 기존 ID: `pe_neutral_diffusion`, `diffusion_filter_highlight_halation`, `pe_local_bloom_relation`
- 근거: [L04 · Tiffen — Diffusion Guide](https://tiffen.com/pages/diffusion-guide), [L05 · Tiffen — Hazed and Confused](https://tiffen.com/blogs/imagemaker/hazed-confused)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG66 · 클리핑과 공간 번짐을 구분한 롤오프

- 처리: REUSE · P0 · 후보 슬롯 제안: `color_grading`
- 소유자: `image_plane.highlight_tones`, `subject.highlight_form`
- 관찰 요소: Bright image tones approach the selected upper range gradually. / Important bright facial or cloth form retains readable internal variation.
- 관계: tone_response → preserves → highlight_form
- 혼동 경계: a spatial luminous halo automatically counts as tonal roll-off / exposure metadata inferred from rendered pixels
- 기존 ID: `pe_gentle_rolloff`, `highlight_rolloff_tone_response`
- 근거: [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG67 · 물체 표면과 구분한 고운 그레인

- 처리: REUSE · P1 · 후보 슬롯 제안: `grain_profile`
- 소유자: `image_plane`, `subject.material_detail`
- 관찰 요소: Fine irregular picture-plane grain remains visible in selected tonal regions. / The grain does not replace pores, lace threads or physical dust.
- 관계: grain → overlays → image_plane_tones; material_detail → is_separate_from → grain
- 혼동 경계: grain becomes skin damage or glitter / digital colored noise automatically proves film capture
- 기존 ID: `pe_fine_midtonal_grain`, `pe_fine_midtonal_grain_relation`
- 근거: [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG68 · 검정 바닥 상승과 옷의 세부

- 처리: REUSE · P0 · 후보 슬롯 제안: `color_grading`
- 소유자: `image_plane.dark_tones`, `garment.dark_detail`
- 관찰 요소: The selected darkest output tones sit above an absolute black floor. / Adjacent dark cloth or hair details remain distinguishable.
- 관계: output_black_floor → belongs_to → image_plane; dark_detail → retained_within → selected_dark_regions
- 혼동 경계: crushed dark regions or a gray physical cloth substitute / a software slider direction is prescribed without a verified editor contract
- 기존 ID: `pe_lifted_black_floor`, `pe_lifted_black_floor_relation`
- 근거: [L06 · Adobe — Lightroom Classic Image Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG69 · 색 이름과 팔레트의 소유자 배정

- 처리: ENRICH_EXISTING · P0 · 후보 슬롯 제안: `color`
- 소유자: `garment`, `background.panel`, `scene.flowers`, `skin`, `light`
- 관찰 요소: Each selected color role belongs to a named existing surface or light owner. / The hue families remain locally distinguishable while the requested overall chroma stays restrained.
- 관계: named_palette_role → bounded_on → declared_owner; local_material_color → is_separate_from → illumination_color
- 혼동 경계: three color words wash every region equally / antique gold is a fixed universal HEX value / a named palette necessarily adds new objects
- 기존 ID: `cr_low_chroma`, `cr_dark_on_dark`
- 근거: [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917), [L01 · ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [L09 · broncolor — Water Reflections for Portrait Photography](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

## EG70 · 공기층·입자·정적의 독립 범위

- 처리: NEW_SIBLING · P1 · 후보 슬롯 제안: `ambient_particle`
- 소유자: `scene.atmosphere`, `declared_particles`, `subject`, `ribbons`
- 관찰 요소: Selected haze or particles occupy declared scene regions with readable depth. / A static-pose or calm-air option is separate from the presence of smoke, mist or suspended petals.
- 관계: atmosphere → occupies → declared_scene_volume; particle_visibility → depends_on → local_light_and_depth
- 혼동 경계: fine film grain becomes dust motes / ethereal adds a dense smoke veil over the eyes / stillness proves a literal stop of time
- 기존 ID: 없음 또는 추가 도메인 확인 필요
- 근거: [R06 · Bella Kotak — The sun dances and the moon kisses](https://www.bellakotakphotography.com/blog/moon-kisses), [R07 · Kirsty Mitchell — Wonderland](https://www.kirstymitchell.art/wonderland/), [R00 · 참조 대화의 사용자 원본 프롬프트와 회수 키워드](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)
- 출처 적용 범위: 외부 사실은 SOURCES의 짧은 주장까지다. 위 구성·소유·관계·후보 표현은 연구자의 제안이다.
- 채택·픽셀 기준: 명시적으로 선택한 변형의 모든 구성요소를 같은 소유자에 구현한다. 문맥 라벨만으로 활성화하지 않는다. 원본 픽셀에서 가림·부분 충족·소유자 이동은 통과로 계산하지 않는다.

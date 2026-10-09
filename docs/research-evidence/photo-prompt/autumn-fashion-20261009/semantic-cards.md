# 가을 패션 상세 의미 카드

113개 의미군과 129개 가시 구현 초안. 카드 안의 여러 이름·문장은 독립 선택지이며 동시에 필요한 조건 목록이 아니다.
정의는 원문과 공개 근거를 대조한 연구자의 종합이다. 출처가 용어의 모든 현대 변형·별칭을 각각 검증했다는 뜻은 아니다.
관찰 구성·후보 문장·혼동 검사·속성 경로는 반영 설계다. 구조 검사 성공이 라이브 검색이나 이미지 성공을 증명하지 않는다.

## AFR001 — 클래식·프레피·아이비·트래드

- 원문 범위: 클래식 / 프레피 / 아이비 스타일 / 트래드
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: 네 이름은 역사·스타일 범위가 겹친다. 프레피의 학교·스포츠 레퍼토리와 Ivy의 버튼다운·자연스러운 테일러링을 선택된 의복 조합으로 구체화한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 셔츠 칼라 끝을 고정하는 작은 단추; 니트나 재킷 바깥으로 보이는 같은 셔츠 칼라; 테일러드 옷과 캐주얼 하의의 조합
- 혼동 경계: 아동·학교 신분을 자동 추가하지 않는다; 모든 classic이 Ivy는 아니다; 칼라 단추와 앞여밈 단추는 다르다
- 주장 한계: 학력·국적·경제 계층은 옷으로 확인할 수 없다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.details.tailoring_front
- 현 후보 이웃(표현 대조, 의미 보증 아님): adult_gugak_instrument_performer, buzz_cut, chrh_hair_topology_chignon, classic_elegant, classic_mustache, classic_tapered_wing_liner, dark_academia_tweed_outfit, framer_restorer_role_model, gugak_instrument_rehearsal_room, opening_hybrid_veranda_architecture_2, paper_umbrella_prop, penny_loafers
- 현 프로필 이웃(표현 대조): chrh_rel_hair_topology_chignon, opening_hybrid_veranda_architecture

**독립 구현 1:** An Oxford button-down shirt collar projects above the V-neck of the same wearer's sweater vest.

관계: `shirt collar` → `same wearer's sweater-vest neckline` (project_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/)

## AFR002 — 다크·라이트 아카데미아

- 원문 범위: 다크 아카데미아 / 라이트 아카데미아
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: dark/light는 선택한 팔레트와 빈티지 테일러링 해석이다. 각각 짙은 갈색·차콜과 크림·베이지 예시를 제공하되 구조를 서로 바꾸지 않는다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 의복별 명시된 색; 같은 재킷의 체크 및 라펠; 이너 목선과 겉옷의 분리
- 혼동 경계: 검정 옷 전체를 gothic으로 합치지 않는다; 도서관·책·학생 역할은 별도 선택이다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.color, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): brass_candlestick_prop, dark_academia, dark_academia_book_stack, dark_academia_reader, dark_academia_still_life, dark_academia_study_tabletop, dark_academia_tweed_outfit, light_academia_aesthetic, light_academia_knit_layers, oak_library_dark_academia
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** A charcoal checked blazer frames the oatmeal roll-neck sweater worn beneath it.

관계: `charcoal blazer front` → `same wearer's oatmeal sweater` (frame_outer_layer, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S11: Saint + Sofia — Trending Dark Academia](https://saintandsofia.com/blogs/style/trending-dark-academia), [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/)

## AFR003 — 절제된 스타일과 지위 담론

- 원문 범위: 콰이어트 럭셔리 / 올드머니 룩 / 미니멀리즘 / 프렌치 시크
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: quiet luxury와 old-money는 사회적 이미지의 이름, minimalism은 장식·색·선의 절제, French chic는 느슨한 스타일 관습이다. 무로고·간결한 선은 구현 가능하나 값비싼 소재나 부는 픽셀 사실이 아니다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 간결한 여밈과 선; 선택한 제한 팔레트; 로고 유무가 읽히는 실제 옷 표면
- 혼동 경계: 가격·브랜드·부의 보편 지표로 쓰지 않는다; 프랑스인 정체성·파리 배경을 묶지 않는다
- 주장 한계: 섬유 등급·가격·계층·국적은 외형으로 인증하지 않는다.
- 부분 속성 제안: wardrobe.color, wardrobe.details.tailoring_front
- 현 후보 이웃(표현 대조, 의미 보증 아님): architectural_material_luxury_aesthetic, greige_camel_cream_quiet_palette, old_money_aesthetic, old_money_tailored_layers, quiet_diffuse_material_gallery_lighting, quiet_luxury_aesthetic, stone_wood_brass_precision_junction_surface
- 현 프로필 이웃(표현 대조): low_brand_prominence_material_luxury

**독립 구현 1:** The coat's uninterrupted front panels hang beside a narrow concealed closure.

관계: `coat front panels` → `same coat's concealed center closure` (flank, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S15: Vogue — Quiet Luxury Is Extending Beyond the Runways](https://www.vogue.com/article/quiet-luxury-interiors-trend), [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/)

## AFR004 — 헤리티지·컨트리·이퀘스트리언

- 원문 범위: 헤리티지 / 컨트리 룩 / 이퀘스트리언
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: heritage는 전통 디자인의 계보, country는 전원복 레퍼토리, equestrian은 승마복에서 가져온 형태다. 왁스 표면·칼라·좁은 하의·높은 부츠를 각각 선택한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 겉옷의 큰 포켓과 다른 칼라 표면; 부츠 입구와 바짓단의 포함 관계; 동일 의복의 질감 차이
- 혼동 경계: 말·총·농장 노동·상류층을 자동 추가하지 않는다; 라이딩 부츠와 cowboy 앞코·굽은 구분한다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.utility_pocket_closure, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): archive_reinterpretation_material_study, archive_sample_new_iteration_pair, building_reinforced_travel_case_frame, comparing_archive_sample_with_new_iteration, equestrian_dust_arena, equestrian_rider, gugak_instrument_rehearsal_room, heritage_reinterpretation_luxury_aesthetic, heritage_restoration_lab, heritage_restorer_role_model, heritage_travel_case_workshop, heritage_travel_object_luxury_aesthetic
- 현 프로필 이웃(표현 대조): heritage_travel_object_construction, pa_crossing_lines_same_carrier

**독립 구현 1:** The narrow trouser legs enter the tops of the same wearer's tall riding boots.

관계: `trouser leg ends` → `same wearer's riding-boot shafts` (enter, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S02: Barbour — Men's Jacket Style Guide](https://au.barbour.com/pages/mens-wax-jacket-styles-quick-guide), [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/)

## AFR005 — 워크웨어·유틸리티·밀리터리

- 원문 범위: 워크웨어 / 유틸리티 / 밀리터리
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: workwear는 작업복 외형의 계보, utility는 기능형 디테일, military-inspired는 군복 요소의 차용이다. 포켓·견장·조절끈을 대상별로 분해한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 앞판 위 덧댄 패치 포켓; 포켓 플랩과 여밈; 같은 의복의 허리 조절부
- 혼동 경계: 많은 포켓이 군복 신분의 증거는 아니다; 위장무늬는 표면 패턴이다; 도구·무기·전투를 자동 추가하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.utility_pocket_closure
- 현 후보 이웃(표현 대조, 의미 보증 아님): cargo_utility_tank_set, chef_temperature_ticket_hygiene_check, clinical_nursing_scrub_duty_system, clt_ct028_v1, emt_high_visibility_transport_uniform, humanoid_labor_robot, indigenous_futurisms_world_landcare_location, khaki_utility_coded, military_dress_uniform_costume, mine_workwear_hidden_silk_lining, miner_workwear_hard_hat, photographer_utility_vest_costume
- 현 프로필 이웃(표현 대조): clinical_nursing_duty_system, clothing_ct028_v1, emergency_medical_transport_system, police_public_safety_duty_system, uniform_utility_pockets_beside_closure, y2kr_cargo_capri, y2kr_cargo_mini

**독립 구현 1:** Large patch pockets are stitched onto the lower front panels of the same chore jacket.

관계: `large patch pockets` → `same chore jacket's front panels` (attached_to, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S02: Barbour — Men's Jacket Style Guide](https://au.barbour.com/pages/mens-wax-jacket-styles-quick-guide), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR006 — 고프코어

- 원문 범위: 고프코어
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: 아웃도어 장비의 기능형 외형을 일상복으로 사용하는 스타일 사용례다. 셸·플리스·트레일 신발은 선택 가능한 개별 운반체다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 지퍼 달린 셸 앞판; 이너 플리스의 파일 표면; 실제 신발 밑창 외곽
- 혼동 경계: 등산 행동·배경·방수 성능을 함께 인증하지 않는다; normcore·athleisure를 동의어로 만들지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): gorpcore_aesthetic
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** An open shell jacket reveals the fleece collar of the same wearer's inner layer.

관계: `open shell front` → `same wearer's fleece collar` (reveal_inner_layer, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S12: Salomon — Normcore Fashion](https://www.salomon.com/en-gb/sg/a/normcore-fashion)

## AFR007 — 보헤미안과 웨스턴

- 원문 범위: 보헤미안 / 보호 / 웨스턴
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: boho는 느슨한 형태·자수·문양·프린지의 가변 조합이고 western은 스냅·요크·부츠 등 특정 디자인 계보다. 프린지 하나로 둘을 동일 판정하지 않는다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 같은 재킷 요크 아래 달린 술; 스냅 앞여밈; 선택한 신발 앞코·샤프트 스티치
- 혼동 경계: 민족·원주민 정체성을 임의 부여하지 않는다; 스웨이드가 모든 western의 필수 소재는 아니다
- 주장 한계: 해당 구체 프린지 후보는 연구자 제안이며 시대·민족 복식 인증이 아니다.
- 부분 속성 제안: wardrobe.details.tassel_fringe_braid, wardrobe.details.hardware
- 현 후보 이웃(표현 대조, 의미 보증 아님): ability_academy_practical_exam_action, bt_overload_dependency_location, bt_overload_rating_prop, character_affection_distance_spectrum_scene_action, ctx_c022, ctx_c158, des_covetous_owner_response_cue, final_fitting_function_check_phase, firefighter_turnout_ppe_system, gaowu_surface_material, heritage_travel_object_luxury_aesthetic, hr_exorcism_contested_threshold
- 현 프로필 이웃(표현 대조): armed_conflict_protected_status_breach, daguerreotype_reflective_cased_plate_object, firefighter_protective_response_system, genocidal_group_destruction_campaign, heritage_travel_object_construction, hvr_profile_exorcism_contested_threshold, hvr_profile_hospital_protection_gap, hvr_profile_safe_boundary_failure, hvr_profile_talisman_bridge_seam, jianghu_inn_identity_standoff, korean_afterlife_guide_escort, maritime_safety_coast_guard_role

**독립 구현 1:** Separate suede fringe strips hang from the seam across the jacket's back yoke.

관계: `suede fringe strips` → `same jacket's back-yoke seam` (hang_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR008 — 바이커·그런지·펑크

- 원문 범위: 바이커 / 그런지 / 펑크
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: biker는 모토 디자인, grunge는 헐렁한 겹침·체크·마모, punk는 스트랩·지퍼·타탄 등의 역사적 디자인 맥락이다. 반항 성격을 픽셀 속성으로 저장하지 않는다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 재킷 앞판을 가로지르는 사선 지퍼; 같은 옷의 금속 부품; 의복에 속한 마모 경계
- 혼동 경계: 검정 가죽이 모두 punk는 아니다; 바이크 탑승·폭력·결박·실제 빈곤을 추정하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.hardware, wardrobe.details.wardrobe_straps
- 현 후보 이웃(표현 대조, 의미 보증 아님): adult_diy_punk_venue_collective, adult_goth_scene_participant, assembling_goth_scene_style_for_venue, biker_short_thigh_knee_landmark, goth_postpunk_self_styling, nineties_grunge_editorial, punk_band_vocalist, punk_rococopunk_maintenance_handoff_prop, punk_rococopunk_mechanism_prop, punk_rococopunk_world_core, sff_extra_xa050, sff_extra_xa051
- 현 프로필 이웃(표현 대조): cycling_bib_shorts_strap_pad_continuity, exercise_dress_integrated_short_liner, y2kr_moto_bag, y2kr_moto_jacket

**독립 구현 1:** The metal zipper runs diagonally across the front of the leather moto jacket.

관계: `metal zipper` → `same moto jacket's front` (cross_diagonally, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S05: Schott NYC — 618 Perfecto](https://www.schottnyc.com/products/618-classic-perfecto-steerhide-leather-motorcycle-jacket), [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

## AFR009 — 고스와 다크 로맨틱

- 원문 범위: 고스 / 고딕 / 다크 로맨틱
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: 검정·벨벳·레이스 계열에 여러 하위 스타일이 있다. dark romantic은 꽃·드레이프·리본 등의 어두운 로맨틱 해석으로, gothic 건축과 다른 대상이다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 의복에 속한 레이스 패턴; 같은 옷의 어두운 색면; 벨벳과 레이스의 층 구분
- 혼동 경계: 공포·종교·십자가·장례 장면은 이름만으로 추가하지 않는다; 검정 의상은 고스의 충분조건이 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.material, wardrobe.color, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): adult_goth_scene_participant, catlike_narrow_eye_shape, cool_dusty_rose_bean_lip, dark_intimate_gothic_tension, dark_spaghetti_strap_top, deep_burgundy_wine_hair, goth_postpunk_self_styling, gothic_candle_studio, gothic_dark_makeup, gothic_doll_cosplayer, gothic_doll_lace_dress, gothic_doll_still_pose
- 현 프로필 이웃(표현 대조): decadent_languor_environment, hvr_profile_gothic_past_present, orn_profile_gd51, pf_brick_castle, pf_venetian_arcade, y2kr_blackletter, y2kr_goth_motif, y2kr_goth_palette

**독립 구현 1:** A black lace blouse shows its floral openwork above a burgundy velvet waistband.

관계: `blouse floral lace` → `same wearer's velvet waistband` (sit_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR010 — 발레코어와 코케트

- 원문 범위: 발레코어 / 코케트
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: balletcore는 무용복에서 차용한 wrap·타이츠·워머·플랫, coquette는 리본·레이스·작은 꽃의 스타일 사용례다. 공유 요소가 있어도 같은 계열로 합치지 않는다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 랩 상의 앞판의 사선 교차; 같은 의복에 붙은 리본; 발레 플랫과 워머의 분리
- 혼동 경계: 실제 무용 능력·연령·성격·유혹 의도를 주장하지 않는다; 리본·레이스만으로 고정 연령을 추가하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.details.wardrobe_trim
- 현 후보 이웃(표현 대조, 의미 보증 아님): balletcore_aesthetic, coquette_aesthetic, coquette_balletcore_flatlay, coquette_tea_table_flatlay, hair_ribbon_bow, satin_ribbon_flatlay_prop
- 현 프로필 이웃(표현 대조): playful_flirtation_interaction

**독립 구현 1:** The cardigan's two front panels cross diagonally and tie at the same wearer's waist.

관계: `wrap-cardigan front panels` → `same wearer's waist` (cross_and_tie, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S10: Museum at FIT — Ballerina: Fashion's Modern Muse](https://exhibitions.fitnyc.edu/ballerina/), [S13: Vogue — The Coquette Trend Is Still Thriving for Spring](https://www.vogue.com/article/coquette-trend-spring-selena-gomez-kendall-jenner)

## AFR011 — Y2K와 가을 레이어

- 원문 범위: Y2K
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: 시대 이미지와 low-rise·cropped·gloss 등의 선택지를 분리한다. cyber futurism과 McBling·일상복 변형은 기존 Y2K 원본을 먼저 재사용한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 상의 밑단과 하의 허리선; 명시한 표면 광택; 같은 착용자의 의복 층
- 혼동 경계: 2000년대라는 말만으로 배꼽·노출·로고를 강제하지 않는다; McBling·cyber를 동의어로 합치지 않는다
- 주장 한계: Y2K의 하위 시대 범위는 기존 독립 연구와 대조 후 승격한다. S14·S16은 시대 규격 전체의 근거가 아니다.
- 부분 속성 제안: wardrobe.length.hem_landmark, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): adult_y2k_revival_stylist, beaded_phone_charm_prop, capri_cropped_windbreaker, contemporary_heisei_y2k_layers, cyber_y2k_aesthetic, kpop_glossy_y2k_stagewear, kpop_y2k_album_world, kpop_y2k_pastel_chrome, lit_direct_flash_camera_axis, lit_direct_flash_crisp_close_shadow, lit_direct_flash_glossy_snapshot_finish, lit_direct_flash_near_far_drop
- 현 프로필 이웃(표현 대조): y2kr_cyber_palette, y2kr_goth_motif, y2kr_pop_palette, y2kr_rave_palette, y2kr_sport_palette, y2kr_warm_denim_palette

**독립 구현 1:** The cropped cardigan hem ends above the waistband of the same wearer's low-rise jeans.

관계: `cropped cardigan hem` → `same wearer's jeans waistband` (end_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S14: Vogue — When It Comes to the Office Siren Trend](https://www.vogue.com/article/office-siren-girlhood-trend-patriarchy), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR012 — 오피스 사이렌

- 원문 범위: 오피스 사이렌
- 우선순위 / 유형: P2 / style_family
- 뜻과 축: 유행어의 직장복 해석이다. 펜슬 형태·셔츠 여밈 상태·안경을 각각 선택하고, 노출·밀착·직업을 한 묶음으로 강제하지 않는다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 같은 셔츠의 앞여밈; 펜슬 스커트 외곽; 실제 선택된 안경테
- 혼동 경계: 직장·오피스·불편한 자세·깊은 열림을 자동 추가하지 않는다; Bayonetta 안경과 캐릭터 cosplay는 별개다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.tailoring_front, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): office_look_not_siren_guard, office_siren_aesthetic
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The fitted button-front shirt enters the waistband of the same wearer's pencil skirt.

관계: `shirt lower front` → `same wearer's pencil-skirt waistband` (enter, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S14: Vogue — When It Comes to the Office Siren Trend](https://www.vogue.com/article/office-siren-girlhood-trend-patriarchy)

## AFR013 — 란제리 드레싱

- 원문 범위: 란제리 드레싱
- 우선순위 / 유형: P1 / style_family
- 뜻과 축: 속옷에서 유래한 의복 형태를 눈에 보이는 겉의 구성 요소로 사용하는 맥락이다. 슬립·캐미솔·코르셋의 실제 패널과 겉옷 관계로 구체화한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 슬립의 독립 어깨끈; 겉카디건과 이너의 다른 경계; 같은 드레스의 바깥 몸판
- 혼동 경계: 속옷 형상은 실제 속옷 역할·노출·행위와 동일하지 않다; 모든 새틴 드레스가 slip은 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.details.corset_bustier
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The open cardigan's front edges frame a separate satin camisole beneath it.

관계: `open cardigan edges` → `same wearer's separate camisole` (frame, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR014 — 트렌치 부품

- 원문 범위: 트렌치코트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 전통형 trench의 벨트·겹여밈·견장·덮개를 독립 부품으로 모델링한다. 선택한 변형에서만 함께 요구한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 같은 코트의 두 앞판 겹침; 벨트의 허리 경로; 견장 또는 스톰 덮개의 부착 위치
- 혼동 경계: 탐정 역할·총기·체크 안감·모든 부품을 자동 추가하지 않는다; 맥·더블 코트와 구분한다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.trench_components
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct009_v1, detective_trench_coat_costume
- 현 프로필 이웃(표현 대조): clothing_ct009_v1

**독립 구현 1:** The trench coat belt passes through side loops and closes across the overlapping front panels.

관계: `same trench coat's belt` → `side loops and overlapping coat front` (pass_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S01: Burberry — The History of the Trench Coat](https://int.burberry.com/c/burberry-world/heritage/trench-coat/)

## AFR015 — 맥과 발마칸

- 원문 범위: 맥 코트 / 발마칸 코트
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: Mac은 간결한 레인코트 계열 표현, Balmacaan은 래글런과 간결한 앞판을 가진 overcoat 계열이다. 소재·길이·실루엣은 별도 결정한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 칼라에서 겨드랑이 쪽으로 이어지는 래글런 연결선; 단순한 앞여밈; 동일 코트의 넓은 몸판
- 혼동 경계: Mac을 브랜드·Macintosh 컴퓨터와 혼동하지 않는다; raglan=큰 소매·어깨 노출이 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.structure.sleeve_attachment, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The coat's raglan seams run from the collar base toward the underarm on each side.

관계: `same coat's raglan seams` → `collar base and underarm regions` (connect, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S04: Mackintosh — Guide to Wool Coats](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats)

## AFR016 — 피코트와 더플

- 원문 범위: 피코트 / 더플코트
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: 피코트는 비교적 짧은 겹여밈과 큰 라펠, 전통 더플은 후드·토글-루프라는 다른 연결 구조다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 피코트 앞판 겹침과 두 단추열; 더플 앞판의 막대 토글과 대응 루프; 같은 코트의 후드
- 혼동 경계: 두 디자인을 동시에 요구하지 않는다; 토글을 일반 단추나 zip으로 바꾸지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.tailoring_front, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Each bar-shaped toggle passes through its paired loop across the duffle coat's front opening.

관계: `duffle-coat toggles` → `paired loops across the same front opening` (pass_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The peacoat's wide lapels sit above two visible rows of buttons on overlapping front panels.

관계: `peacoat lapels` → `same peacoat's paired button rows` (sit_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S04: Mackintosh — Guide to Wool Coats](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats), [S03: Gloverall — History of the Duffle Coat](https://www.gloverall.com/blogs/journal/history-of-the-duffle-coat-origins-heritage)

## AFR017 — 랩·로브 코트

- 원문 범위: 랩 코트 / 로브 코트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: wrap은 앞판 겹침 방식, robe는 느슨한 가운형 몸판 해석이다. 벨트와 몸판은 같은 코트 소유자에 결속한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 사선 또는 비스듬히 겹친 앞판; 허리를 둘러 묶인 벨트; 매듭에서 양옆으로 모이는 직물
- 혼동 경계: 벨트가 있다고 모든 코트가 wrap은 아니다; 랩 상의와 coat를 혼동하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.panel.structure, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The robe coat's front panels overlap beneath a belt tied around the same coat's waist.

관계: `robe-coat front panels` → `same coat's tied waist belt` (overlap_beneath, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S04: Mackintosh — Guide to Wool Coats](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR018 — 코쿤과 더스터

- 원문 범위: 코쿤 코트 / 더스터
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: cocoon은 몸통 볼륨에서 밑단으로 좁아지는 외곽, duster는 긴 가벼운 겉옷의 제품·역사 표현이다. 볼륨과 길이는 독립 축이다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 몸통 최대 폭과 아래 좁아지는 코쿤 경계; 더스터의 긴 수직 밑단; 같은 옷의 처지는 앞판
- 혼동 경계: 긴 코트를 cocoon으로 합치지 않는다; 청소 도구 duster와 다른 대상이다
- 주장 한계: duster의 역사적 소재·용도 전체는 별도 확인 대상이다. 현재 카드의 외형은 선택된 길이·무게감 제안이다.
- 부분 속성 제안: wardrobe.silhouette.torso_outline, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The coat's rounded torso outline narrows toward the hem below the hips.

관계: `same cocoon coat's torso outline` → `hem below the hips` (narrow_toward, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S04: Mackintosh — Guide to Wool Coats](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats), [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

## AFR019 — 케이프와 판초

- 원문 범위: 케이프 / 판초
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: cape는 어깨에서 떨어지는 소매 없는 덮개, poncho는 중앙 목 구멍으로 통과해 몸을 둘러싸는 구성이다. 열린 앞판과 목 개구부를 실제 변형별로 검토한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 어깨에서 이어지는 큰 한 겹; 팔의 통과 또는 노출 위치; 선택된 중앙 목 개구부
- 혼동 경계: cloak·cape·poncho 명칭만으로 특정 문화·잠금장치를 결정하지 않는다; 앞이 닫힌 cape와 slit poncho 변형을 배제하지 않는다
- 주장 한계: cape/poncho 일반 구조는 원문·기존 데이터에 근거한 작업 정의이며, 모든 변형의 독립 출처 확인 완료를 뜻하지 않는다.
- 부분 속성 제안: wardrobe.details.cape_cloak_poncho
- 현 후보 이웃(표현 대조, 의미 보증 아님): andean_poncho_panel_system, ccx_cc26_02, clt_ct011_v1, clt_ct011_v2, poncho_central_neck_front_back_panels, unif_hood_belt_cape_layers
- 현 프로필 이웃(표현 대조): andean_poncho_central_opening_panel_system, clothing_ct011_v1, clothing_ct011_v2, costume_ccx_cc26_02, uniform_hood_belt_cape_layers

**독립 구현 1:** The poncho panel extends from a central neck opening over both shoulders toward the hanging hem.

관계: `poncho panel` → `central neck opening and both shoulders` (extend_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR020 — 블레이저의 독립 구조 축

- 원문 범위: 블레이저 / 싱글브레스티드 / 더블브레스티드 / 오버사이즈 블레이저 / 크롭 재킷 / 트위드 재킷
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: blazer 종류, single/double 여밈, oversized 여유, cropped 길이, tweed 표면은 함께 성립하는 독립 축이다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 앞판 겹침 폭과 단추 배열; 어깨·몸판의 여유; 밑단의 신체 기준점; 표면 실 혼합
- 혼동 경계: tweed=노칼라·장식 단추가 아니다; 큰 어깨=허리 여유 전체가 아니다; 두 단추열만으로 잠김 상태를 인증하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.tailoring_front, wardrobe.length.hem_landmark, wardrobe.material.visible_weave
- 현 후보 이웃(표현 대조, 의미 보증 아님): athletic_shorts_oversized_blazer, clean_blazer_trousers, clt_ct012_v2, coordinated_school_uniform_system, dark_academia_tweed_outfit, fit_ff04_v1_candidate, jacket_lapel_settle_action, oversized_top_tiny_bottom, school_uniform_component_inspection, school_uniform_consistent_trim_system, sculpted_power_shoulders, sport_luxe_fandom
- 현 프로필 이웃(표현 대조): clothing_ct012_v2, fit_ff04_v1, school_uniform_institutional_system, underwear_as_outerwear_layer_system, y2kr_crop_low

**독립 구현 1:** The cropped blazer's hem ends at the same wearer's waist while its broad front panels overlap.

관계: `cropped blazer hem` → `same wearer's waist` (end_at, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S04: Mackintosh — Guide to Wool Coats](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats), [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S32: Johnstons of Elgin — International Tweed Day](https://discover.johnstonsofelgin.com/our-story/international-tweed-day)

## AFR021 — 모토 재킷의 비대칭 여밈

- 원문 범위: 라이더 / 모토 재킷
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 사선 지퍼·스냅 라펠·벨트 등의 선택된 모토 변형이다. 현대 최소형에는 벨트가 생략될 수 있다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 같은 앞판의 사선 지퍼 경로; 라펠 부착점; 선택된 금속 지퍼 끝
- 혼동 경계: 가죽 종류가 moto 구조를 대신하지 않는다; 바이크·안전성은 별도 사실이다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.hardware, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): biker_short_thigh_knee_landmark, black_leather_rider_outfit, motorcycle_rider_model, y2kr_moto_jacket
- 현 프로필 이웃(표현 대조): cycling_bib_shorts_strap_pad_continuity, exercise_dress_integrated_short_liner, y2kr_moto_jacket

**독립 구현 1:** The moto jacket's asymmetrical zipper joins the offset edges of its front panels.

관계: `asymmetrical moto zipper` → `same jacket's offset front edges` (join, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S05: Schott NYC — 618 Perfecto](https://www.schottnyc.com/products/618-classic-perfecto-steerhide-leather-motorcycle-jacket)

## AFR022 — 보머와 바시티

- 원문 범위: 보머 재킷 / 바시티 재킷
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: bomber는 짧은 몸판·모이는 커프스와 밑단 계열, varsity는 문자·배색·스냅·줄무늬 리브의 가변 스포츠 디자인 계열이다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 몸판을 모으는 시보리 밑단; 커프스의 수축; 선택된 몸판-소매 배색 및 스냅
- 혼동 경계: 학교 소속·학생·운동선수 역할을 추가하지 않는다; 리브 밑단 하나로 두 이름을 동의어로 만들지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.bomber_finish, wardrobe.color
- 현 후보 이웃(표현 대조, 의미 보증 아님): casual_bomber_jacket_miniskirt
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The bomber jacket's fuller body gathers into a narrower ribbed waistband.

관계: `bomber jacket body` → `same jacket's ribbed waistband` (gather_into, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR023 — 해링턴

- 원문 범위: 해링턴 재킷
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: G9 계열의 짧은 지퍼 재킷과 dog-ear 칼라·리브 마감·뒷요크를 분해한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 두 칼라 끝의 세우는 잠금; 리브 커프스와 밑단; 선택된 뒷면 요크
- 혼동 경계: bomber와 공유하는 리브만으로 동일 판정하지 않는다; Fraser Tartan은 브랜드 예시다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.bomber_finish, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The Harrington jacket's two collar tabs meet above its front zipper.

관계: `Harrington collar tabs` → `same jacket's front zipper` (meet_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S06: Baracuta — What is a Harrington jacket?](https://support.baracuta.com/en-US/what-is-a-harrington-jacket-327293)

## AFR024 — 트러커 버전

- 원문 범위: 트러커 재킷
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: Type I·II·III에 따라 포켓과 절개가 다르다. 양쪽 포켓 후보는 선택된 Type II 변형으로 한정한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 같은 앞판의 덮개 포켓; 세로 주름 또는 절개; 단추 앞여밈
- 혼동 경계: 데님 소재가 trucker 구조를 보장하지 않는다; 한 포켓 역사형을 오류라고 하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.utility_pocket_closure, wardrobe.surface.denim_chambray
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Two flap chest pockets sit beside the Type II jacket's button-front opening.

관계: `Type II jacket chest pockets` → `same jacket's button-front opening` (flank, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S07: Levi's — Type II Selvedge Trucker Jacket](https://www.levi.com/US/en_US/clothing/men/outerwear/type-ii-selvedge-trucker-jacket/p/A76320014)

## AFR025 — 셔킷·초어·반·필드

- 원문 범위: 셔킷 / 초어 재킷 / 반 재킷 / 필드 / 사파리 재킷
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: 셔킷은 셔츠형 칼라·여밈의 두꺼운 덧옷, chore는 박스형 패치 포켓, barn은 야외복 레퍼토리, field/safari는 다포켓과 허리 조절 계열이다. 제품명 중첩을 인정한다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 칼라와 여밈의 셔츠형 구조; 앞판에 덧댄 포켓; 선택된 이질 소재 칼라; 허리 조절 연결
- 혼동 경계: barn을 말 barn·농장 배경으로 바꾸지 않는다; field를 군사·사파리 여행으로 자동 확대하지 않는다; 포켓 수는 변형별로 지정한다
- 주장 한계: 셔킷·초어·반·field 일반 사양은 명칭만으로 완전 인증되지 않는다. 포켓·칼라별 제품 출처를 승격 때 보완한다.
- 부분 속성 제안: wardrobe.details.utility_pocket_closure, wardrobe.details.wardrobe_structure
- 현 후보 이웃(표현 대조, 의미 보증 아님): 85mm, actioncam_ultrawide, aeolian_dune_crosswind_location, aeolian_dune_field_subject, agricultural_field_robot, asymmetric_counterbalance_relation, aurora_borealis_field, balanced_contour_highlight_dimension, black_hole_emission_ring_measurement_prop, bt_phase_driving_action, bt_phase_nucleation_aesthetic, character_companion_reciprocity_scene_subject
- 현 프로필 이웃(표현 대조): asymmetric_counterbalance_relation, auroral_arc_curtain_atmosphere, backlit_silhouette_mass_relation, balayage_ribbon_color_placement, bloodstain_observation_documentation, blue_hour_ambient_practical_balance, contour_highlight_cosmetic_sculpting, cr_accented_analogous, cr_chromatic_subject, cr_color_blocks, cr_dark_on_dark, cr_high_chroma

**독립 구현 1:** The barn jacket's ribbed corduroy collar rests above its smooth cotton front panels.

관계: `barn-jacket corduroy collar` → `same jacket's cotton front panels` (rest_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S02: Barbour — Men's Jacket Style Guide](https://au.barbour.com/pages/mens-wax-jacket-styles-quick-guide), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR026 — 퀼팅과 왁스드

- 원문 범위: 퀼팅 재킷 / 왁스드 재킷
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: quilting은 겉·속층을 고정하는 봉제 패턴, waxing은 표면 처리다. 같은 옷에 둘이 함께 존재할 수 있다.
- 소유자: 같은 명시된 착용자의 해당 의복·부위·레이어에 결속한다. 일반 의복 구조가 연령·신분·성별을 변경하거나 자동 지정하지 않는다.
- 관찰 단서: 반복 봉제선과 구획별 부피; 빛에 따른 선택된 코튼 표면의 완만한 반사; 부품의 같은 의복 소유
- 혼동 경계: 마름모 프린트를 퀼팅 봉제로 통과시키지 않는다; 광택만으로 왁스·방수 성능을 증명하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.material.visible_weave, wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Diamond stitching divides the jacket's padded front into repeated shallow raised cells.

관계: `diamond quilt stitching` → `same jacket's padded front cells` (divide, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S02: Barbour — Men's Jacket Style Guide](https://au.barbour.com/pages/mens-wax-jacket-styles-quick-guide)

## AFR027 — 풀오버·카디건·기장

- 원문 범위: 풀오버 / 카디건 / 크롭 카디건 / 롱라인 카디건
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: pullover의 통과형 몸판, cardigan의 전체 앞여밈, cropped/longline의 밑단 기준점은 별도 축이다. 카디건의 현재 열림 상태를 의복 종류와 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 니트 앞판을 나누는 연속 여밈; 선택한 단추 잠김; 밑단과 허리·힙 기준점
- 혼동 경계: 크롭이라는 이름으로 복부·배꼽을 강제하지 않는다; 잠긴 카디건을 pullover로 합치지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.cardigan_opening, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): adjusting_collar, cardigan_pilling_detail, clt_ct006_v1, clt_ct006_v2, coordinated_school_uniform_system, knit_cardigan_jeans, librarian_cardigan_formal, lightweight_open_knit_layer_surface, school_uniform_component_inspection, school_uniform_consistent_trim_system, sky_blue_ribbed_cardigan_sweatpants, tank_lightweight_summer_layer_wide_trouser_ensemble
- 현 프로필 이웃(표현 대조): clothing_ct006_v1, clothing_ct006_v2, underwear_as_outerwear_layer_system, y2kr_crop_cardigan

**독립 구현 1:** The cropped cardigan's buttoned front ends at the waistband of the same wearer's skirt.

관계: `cropped cardigan hem` → `same wearer's skirt waistband` (end_at, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR028 — 트윈세트·베스트·민소매 니트

- 원문 범위: 트윈세트 / 스웨터 베스트 / 슬리브리스 니트
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: twinset은 맞춘 이너와 카디건 두 벌의 관계, sweater vest는 소매 없는 니트 운반체, sleeveless knit은 넓은 종류다. 같은 색 한 벌을 twinset으로 판정하지 않는다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 두 니트의 독립 목선과 앞판; 색·표면의 맞춤 관계; 암홀과 이너 소매의 층 구분
- 혼동 경계: 니트 베스트가 항상 셔츠 위에 있다는 뜻은 아니다; 민소매와 겨드랑이 피부 가시성은 별개다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.material, wardrobe.color
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The open knit cardigan reveals a separate sleeveless knit top in the same color and stitch texture.

관계: `open cardigan` → `same wearer's separate matching knit top` (reveal_matching_layer, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR029 — 폴로·하프집·헨리

- 원문 범위: 폴로 니트 / 하프집 니트 / 헨리넥
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: polo는 칼라·짧은 플래킷, half-zip은 짧은 지퍼, Henley는 칼라 없는 짧은 단추 플래킷이다. 개방 깊이는 현재 착용 상태다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 명시된 칼라 유무; 앞여밈의 길이와 부품; 지퍼 또는 단추의 끝점
- 혼동 경계: 같은 짧은 여밈을 모든 이름의 동의어로 합치지 않는다; 열림만으로 노출 부위를 결정하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.henley_placket, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct001_v1
- 현 프로필 이웃(표현 대조): clothing_ct001_v1

**독립 구현 1:** A short row of buttons descends from the Henley top's collarless round neck.

관계: `Henley button placket` → `same top's collarless round neck` (descend_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR030 — 랩 니트와 타이프런트

- 원문 범위: 랩 니트 / 타이프런트 톱
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: wrap은 앞판이 겹쳐 교차하는 구성, tie-front는 앞에서 묶는 여밈이다. 매듭은 별도 위치를 가지며 겹침 또는 열린 간격을 만들 수 있다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 앞판 교차 방향; 실제 끈 끝과 매듭; 매듭 주변의 겹침·열린 공간
- 혼동 경계: 앞 매듭이 모든 wrap을 증명하지 않는다; 매듭 위치가 배꼽이나 가슴 노출을 보장하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.panel.structure, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): y2kr_tie_front, y2kr_wrap_knit
- 현 프로필 이웃(표현 대조): y2kr_tie_front, y2kr_wrap_knit

**독립 구현 1:** The knit top's two front ties meet in a knot between its lower front edges.

관계: `same knit top's front ties` → `knot between its lower front edges` (meet_in, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR031 — 볼레로와 슈러그

- 원문 범위: 볼레로 / 슈러그
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: bolero는 짧은 덧재킷, shrug는 어깨·팔·윗등에 집중하는 덧옷 계열이다. 상품명의 중첩과 몸판의 실제 면적을 함께 기록한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 짧은 덧옷 밑단; 독립 이너 몸판; 양 소매와 어깨 연결
- 혼동 경계: 짧은 카디건과 무조건 동의어로 합치지 않는다; 덧옷의 짧음을 이너 노출로 자동 해석하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): lightweight_open_knit_layer_surface, pv_shoulder_raise, tank_lightweight_summer_layer_wide_trouser_ensemble, y2kr_bolero, y2kr_shrug
- 현 프로필 이웃(표현 대조): y2kr_bolero, y2kr_shrug

**독립 구현 1:** The shrug covers the shoulders and arms above a separate full-length camisole body.

관계: `same wearer's shrug` → `shoulders and arms above the separate camisole` (cover_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR032 — 캐미솔·브라렛·밴도·보디슈트

- 원문 범위: 캐미솔 / 브라렛 / 밴도 / 튜브톱 / 보디슈트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: cami는 가는 끈 상의, bralette는 브라 유래 구조, bandeau/tube는 끈 없는 띠형 또는 관형, bodysuit는 위·아래가 이어진 한 벌이다. 컵·길이·역할은 별도 축이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 독립 스트랩 또는 끈 없는 윗경계; 컵 및 몸판; 상의가 하의에 들어가는 경계
- 혼동 경계: strapless=짧은 밴도가 아니다; 상의가 매끈하게 들어간 사진만으로 숨은 bodysuit 하부를 인증하지 않는다; 브라렛 이름만으로 지지력을 정하지 않는다
- 주장 한계: 보디슈트의 숨은 하부·기능은 명세에 보존하고 가시성 검사와 분리한다.
- 부분 속성 제안: wardrobe.structure.strap_attachment, wardrobe.details.corset_bustier
- 현 후보 이웃(표현 대조, 의미 보증 아님): athletic_unitard_continuous_one_piece, camisole_slip_over_shirt_layer, chrh_hair_color_state_hair_bikini_structure, clt_ct004_v1, clt_ct004_v2, clt_ct155_v1, exercise_dress_outer_skirt_inner_shorts, lace_trim_camisole_wide_denim_ensemble, pfe_neck_foundation_candidate, sff_extra_xa047, sff_extra_xa058, sw_candidate_bandeau
- 현 프로필 이웃(표현 대조): clothing_ct004_v1, clothing_ct004_v2, clothing_ct155_v1, lace_trim_attached_edge, pfe_neck_foundation, sw_bandeau, underwear_as_outerwear_layer_system, unitard_upper_crotch_leg_continuity, y2kr_bandeau, y2kr_bodysuit, y2kr_cami, y2kr_lace_cami

**독립 구현 1:** Two thin camisole straps connect the front neckline to the same garment's back edge.

관계: `camisole shoulder straps` → `same camisole's front and back neckline edges` (connect, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types)

## AFR033 — 플란넬 셔츠와 푸시보

- 원문 범위: 플란넬 셔츠 / 푸시보 블라우스
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: flannel은 기모 표면, shirt는 의복 구조, pussy-bow는 목에서 묶는 길고 넓은 타이다. 체크 패턴과 플란넬 가공을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 셔츠 표면의 낮은 보풀; 목 부근의 리본 두 루프와 끝; 같은 블라우스에 이어진 타이
- 혼동 경계: check=flannel이 아니다; 독립 스카프와 부착된 bow는 별개다; 이름의 다른 언어 뜻은 의복 구성 근거가 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.material, wardrobe.accessories.neck_wear_position
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The blouse's long neck ties form two bow loops just below its collar.

관계: `same blouse's neck ties` → `bow loops below its collar` (form, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR034 — 크루·터틀·모크·퍼널

- 원문 범위: 크루넥 / 터틀넥 / 롤넥 / 모크넥 / 퍼널넥
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: crew는 얕은 원형, turtle/roll은 높고 접는 칼라, mock은 짧은 서는 칼라, funnel은 더 넓게 솟는 목 둘레 해석이다. 높이·접힘·넓이를 실제 경계로 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 목 밑 또는 목 위 끝점; 접힌 겹선의 유무; 목과 칼라 사이 간격
- 혼동 경계: 목을 덮는다고 모두 turtle이 아니다; 높은 목선과 bodycon은 독립이다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.neckline
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct039_v2, pv_head_tilt
- 현 프로필 이웃(표현 대조): clothing_ct039_v2, cv_profile_head_tilt

**독립 구현 1:** The roll-neck collar rises along the neck and folds back over itself at the upper edge.

관계: `roll-neck upper edge` → `same collar's standing neck band` (fold_over, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The short mock-neck band stands around the base of the neck with a single upper edge.

관계: `mock-neck band` → `same wearer's neck base` (stand_around, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR035 — 보트·스쿱·스퀘어

- 원문 범위: 보트넥 / 바토넥 / 스쿱넥 / U넥 / 스퀘어넥
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 넓고 얕은 횡곡선, 깊게 내려간 U곡선, 직선 옆과 바닥을 가진 사각 경계가 다르다. 폭과 깊이를 별도 값으로 기록한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 동일 상의의 좌우 경계; 중앙 최저점; 바닥의 곡선 또는 직선
- 혼동 경계: 보트의 넓이가 off-shoulder를 뜻하지 않는다; 깊이만으로 cleavage를 확정하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.neckline
- 현 후보 이웃(표현 대조, 의미 보증 아님): boat_deck_shoes, clt_ct035_v1, clt_ct035_v2, coast_guard_rescue_boat_deck, coast_guard_rescue_line_lifebuoy_radio_set, coast_guard_rescue_line_recovery, dockside_sailorcore, former_service_residue_prop, mythic_flood_preservation_aesthetic, sw_candidate_scoop, sw_candidate_square
- 현 프로필 이웃(표현 대조): clothing_ct035_v1, clothing_ct035_v2, ghost_ship_former_vessel_breach, maritime_safety_coast_guard_role, mythic_flood_preservation_vessel, sw_scoop, sw_square, water_rel_w036

**독립 구현 1:** The square neckline has two near-vertical sides joined by a straight lower edge.

관계: `same top's square-neck sides` → `straight lower neckline edge` (join, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types)

## AFR036 — V와 플런징

- 원문 범위: V넥 / 플런징 네크라인
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: V는 중앙으로 모이는 경계 형태, plunging은 상대적으로 깊게 내려가는 범위 표현이다. 실제 몸 기준점과 이너 경계를 함께 정한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 두 사선이 만나는 점; 그 점의 명시된 신체 기준; 아래 이너 또는 피부 상태
- 혼동 경계: V와 plunge는 깊이가 고정되지 않는다; 몸의 골·배꼽 가시성을 이름으로 추가하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.neckline, wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): sw_candidate_plunge
- 현 프로필 이웃(표현 대조): sw_plunge

**독립 구현 1:** The neckline's two diagonal edges meet at a low point on the same top's center front.

관계: `V-neck diagonal edges` → `same top's low center-front point` (converge_at, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types)

## AFR037 — 스위트하트·카울·서플리스

- 원문 범위: 스위트하트넥 / 카울넥 / 서플리스넥
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: sweetheart는 두 볼록 곡선과 중앙 골, cowl은 늘어진 직물 주름, surplice는 사선 앞판 겹침이다. 셋이 만든 낮은 목선을 서로 대체하지 않는다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 두 목선 곡선 또는 처진 U주름 또는 앞판 사선 교차; 해당 상의의 실제 경계; 겹침의 위아래 층
- 혼동 경계: cowl을 단순 깊은 U로 합치지 않는다; surplice를 항상 실제 wrap 잠금이라고 확정하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.neckline, wardrobe.panel.folds
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct037_v1, pfe_cowl_candidate, sw_candidate_sweetheart
- 현 프로필 이웃(표현 대조): clothing_ct037_v1, pfe_cowl, sw_sweetheart

**독립 구현 1:** Loose satin folds hang between the two sides of the same camisole's cowl neckline.

관계: `camisole cowl folds` → `same neckline's left and right edges` (hang_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Two rounded upper edges dip together at the center of the sweetheart neckline.

관계: `sweetheart neckline arcs` → `same neckline's center notch` (dip_together, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S20: Seamwork — How to Sew Bias-Cut Garments](https://www.seamwork.com/sewing-tutorials/how-to-sew-bias-cut-garments)

## AFR038 — 오프·원·콜드 숄더

- 원문 범위: 오프숄더 / 바르도넥 / 원숄더 / 콜드숄더
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: off는 양쪽 어깨 아래 경계, one는 비대칭 한쪽 지지, cold는 어깨 부분만 열린 구조다. 한쪽을 내려 입은 착용 상태와 설계 비대칭도 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 양쪽 또는 한쪽 어깨의 실제 피부 경계; 남은 소매·스트랩; 열린 창의 위치
- 혼동 경계: drop shoulder 봉제선은 노출이 아니다; 어깨를 덮은 코트가 있으면 몸 가시성을 별도 판정한다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.neckline, wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): black_backpack_one_shoulder, clt_ct038_v1, clt_ct038_v2, clt_ct131_v1, clt_ct142_v2, cold_shoulder_cutout_sleeve_bridge, cold_shoulder_knit_top_midi_skirt, pfe_one_shoulder_candidate, pv_head_tilt, pv_shoulder_forward, pv_shoulder_lower, sf_151_base
- 현 프로필 이웃(표현 대조): clothing_ct131_v1, clothing_ct142_v2, pfe_one_shoulder, sf_profile_151_base, sw_offshoulder, sw_oneshoulder, uniform_shoulder_draped_empty_sleeve, y2kr_mini_shoulder, y2kr_one_shoulder

**독립 구현 1:** The cold-shoulder top keeps its neckline and sleeves while rounded openings expose each shoulder cap.

관계: `cold-shoulder openings` → `same wearer's shoulder caps` (expose_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The off-shoulder knit's upper edge passes below both shoulder caps.

관계: `off-shoulder knit upper edge` → `same wearer's left and right shoulder caps` (pass_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S18: Sherri Hill — What Is a Halter Dress?](https://www.sherrihill.com/blogs/news/what-is-a-halter-dress)

## AFR039 — 홀터·스트랩리스·키홀·일루전

- 원문 범위: 홀터넥 / 스트랩리스 / 키홀 네크라인 / 일루전 네크라인
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: halter는 목 뒤의 연결, strapless는 어깨끈 없음, keyhole은 경계 안의 개구부, illusion은 비치는 실제 원단층이다. 지지 경로·구멍·투과성을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 목 뒤 연결 또는 어깨 위 지지 없는 윗선; 키홀의 둘레; illusion 원단의 경계와 미세 망
- 혼동 경계: halter=깊은 V·오픈백이 아니다; 투명 원단을 맨살 구멍으로 대체하지 않는다; strapless=일자 윗선만은 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.structure.strap_attachment, wardrobe.material.transmission, wardrobe.neckline
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct004_v2, pfe_halter_candidate, pfe_illusion_panel_candidate, sw_candidate_halter, sw_candidate_strapless, y2kr_bandeau, y2kr_tube_dress, y2kr_tube_top
- 현 프로필 이웃(표현 대조): clothing_ct004_v2, pfe_halter, pfe_illusion_panel, racerback_sports_bra_strap_convergence, sw_halter, sw_strapless, y2kr_bandeau, y2kr_tube_dress, y2kr_tube_top

**독립 구현 1:** A fine mesh panel bridges the dress's sweetheart bodice edge and its high neckline.

관계: `illusion mesh panel` → `same dress's bodice edge and high neckline` (bridge, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The halter top's straps converge behind the same wearer's neck.

관계: `halter-top straps` → `same wearer's nape` (converge, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S18: Sherri Hill — What Is a Halter Dress?](https://www.sherrihill.com/blogs/news/what-is-a-halter-dress)

## AFR040 — 밀착도와 여유

- 원문 범위: 피티드 / 슬림핏 / 바디콘 / 바디스키밍
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: fitted는 맞춘 재단, slim은 적은 여유, bodycon은 곡선을 따른 밀착, skimming은 접촉 사이 가볍게 흐르는 표면 해석이다. 신체를 바꾸는 속성이 아니다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 같은 몸 부위와 의복 경계; 국소 접촉·떨어짐; 접촉 사이의 처짐
- 혼동 경계: 밀착과 직접 노출은 다르다; slim 수치를 사진에서 역산하지 않는다; 기존 fit 변형을 재사용한다
- 주장 한계: 신축성·압력·치수·건강·편안함은 픽셀만으로 판정하지 않는다.
- 부분 속성 제안: wardrobe.fit.contact_distribution, wardrobe.drape
- 현 후보 이웃(표현 대조, 의미 보증 아님): ao_dai_long_tunic_trouser_system, ao_dai_side_openings_over_trousers, athletic_unitard_continuous_one_piece, bias_cut_body_skimming_drape, biker_short_thigh_knee_landmark, body_con_second_skin, brief_lined_running_short_inner_brief, building_reinforced_travel_case_frame, capri_legging_mid_calf_landmark, ccx_cc08_01, ccx_cc23_01, clt_ct005_v2
- 현 프로필 이웃(표현 대조): active_skort_outer_skirt_inner_shorts, bespoke_tailoring_individual_pattern, clothing_ct005_v2, clothing_ct023_v2, costume_ccx_cc08_01, costume_ccx_cc23_01, cycling_bib_shorts_strap_pad_continuity, exercise_dress_integrated_short_liner, fit_ff07_v2, fit_ff47_v2, fit_ff61_v1, golem_constructed_material_agency

**독립 구현 1:** The opaque knit dress follows the torso curves while remaining a continuous fabric surface.

관계: `opaque knit dress surface` → `same wearer's torso curves` (follow, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S20: Seamwork — How to Sew Bias-Cut Garments](https://www.seamwork.com/sewing-tutorials/how-to-sew-bias-cut-garments)

## AFR041 — 아워글라스·신칭·핏앤플레어

- 원문 범위: 아워글라스 실루엣 / 웨이스트 신칭 / 핏앤플레어
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: hourglass는 의복 외곽의 상하 볼륨과 좁은 중간, cinching은 허리를 모으는 방식, fit-and-flare는 위쪽 맞음과 아래 퍼짐이다. 결과 외곽과 원인 구조를 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 같은 옷의 허리 최소 폭; 위·아래 폭 대비; 벨트·패널·끈의 모이는 곳
- 혼동 경계: 몸 비율을 변경하거나 특정 성별 체형을 강제하지 않는다; 신칭 벨트와 hourglass 결과는 동일 의무가 아니다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.silhouette.torso_outline, wardrobe.panel.structure
- 현 후보 이웃(표현 대조, 의미 보증 아님): bottom_hourglass_relation, natural_hourglass_relation, top_hourglass_relation
- 현 프로필 이웃(표현 대조): one_piece_dress_construction, soft_full_figure_volume

**독립 구현 1:** The jacket's waist belt gathers its front fabric between broader shoulder and hip outlines.

관계: `same jacket's waist belt` → `front fabric between broader shoulder and hip outlines` (gather, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR042 — 보디스·코르셋·뷔스티에

- 원문 범위: 보디스 / 코르셋 톱 / 뷔스티에 / 오버버스트 코르셋 / 언더버스트 코르셋
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: bodice는 상체 몸판, corset/bustier는 제품에서 중첩되기도 하는 패널·컵·보강 구조, over/underbust는 위 경계 위치다. 실제 지지와 외형 차용을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 같은 의복의 상부 경계; 컵을 포함하거나 그 아래 시작하는 패널; 별도 이너와 코르셋의 층
- 혼동 경계: underbust=underboob이 아니다; 보닝·컵·레이스업을 제품명 하나로 전부 강제하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.corset_bustier, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): appearance_h028, ccx_cc08_01, ccx_cc08_02, ccx_cc10_03, clt_ct001_v1, clt_ct004_v2, clt_ct005_v1, clt_ct005_v2, clt_ct019_v2, clt_ct023_v1, clt_ct023_v2, clt_ct031_v1
- 현 프로필 이웃(표현 대조): appearance_rel_h028, bifurcated_one_piece_jumpsuit, clothing_ct001_v1, clothing_ct004_v2, clothing_ct005_v1, clothing_ct005_v2, clothing_ct019_v2, clothing_ct023_v2, clothing_ct031_v1, clothing_ct031_v2, clothing_ct036_v1, clothing_ct036_v2

**독립 구현 1:** The underbust corset's upper edge sits below the bust over a separate continuous blouse.

관계: `underbust-corset upper edge` → `same wearer's bust over the separate blouse` (sit_below_over, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR043 — 컵·와이어·보닝

- 원문 범위: 컵 디테일 / 언더와이어 / 보닝
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 컵의 패널 경계, underwire의 컵 하단 지지, boning의 몸판 지지는 서로 다르다. 봉제 채널은 외형 근거이고 숨은 삽입물 재질은 명세 사실이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 컵 패널의 곡선 경계; 컵 아래 곡선 채널; 몸판 위 세로 채널
- 혼동 경계: 컵이 있다고 wire가 있는 것은 아니다; 채널을 보고 강도·재질·지지력을 인증하지 않는다
- 주장 한계: 내부 지지대의 존재·재질·강도는 보이는 단면이나 제품 명세 없이 이미지 PASS로 만들지 않는다.
- 부분 속성 제안: wardrobe.details.bra_wire_boning, wardrobe.construction.boning
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct023_v1, clt_ct072_v1, clt_ct072_v2, orn_gd40, sff_pro_c15, sff_pro_c16, sff_pro_e19, y2kr_corset_top
- 현 프로필 이웃(표현 대조): clothing_ct023_v1, clothing_ct072_v1, clothing_ct072_v2, couture_atelier_individual_construction, y2kr_corset_top

**독립 구현 1:** Curved cup seams sit above separate vertical channels on the same structured bodice.

관계: `bodice cup seams` → `same bodice's vertical channels` (sit_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR044 — 다트와 프린세스 심

- 원문 범위: 다트 / 프린세스 심
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: dart는 접어 봉제한 쐐기와 끝점, princess seam은 패널 사이에 길게 이어지는 곡선 연결선이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 다트가 끝나는 지점; 패널 두 장 사이의 연속선; 같은 몸판의 가슴-허리 구역
- 혼동 경계: dart 눈 움직임·무기와 의복을 분리한다; princess 캐릭터·복식 스타일과 심 구조는 다르다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.princess_dart, wardrobe.structure.panel_connection
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct031_v1, clt_ct031_v2, eyes_dart_to_partner_then_away, sff_pro_c01
- 현 프로필 이웃(표현 대조): clothing_ct031_v1, clothing_ct031_v2

**독립 구현 1:** The dress's curved panel seams continue from the upper torso down through its waist.

관계: `same dress's princess panel seams` → `upper torso and waist` (continue_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S23: Mood Sewciety — 9 Types of Sewing Darts](https://blog.moodfabrics.com/all-about-darts/), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR045 — 엠파이어와 페플럼

- 원문 범위: 엠파이어 웨이스트 / 페플럼
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: empire는 높은 절개선의 위치, peplum은 허리 부근에 별도로 퍼지는 짧은 패널이다. 전체 dress flare와 다른 층이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 가슴 아래 위치의 이음선; 허리에서 덧대어 퍼진 짧은 층; 아래 본몸판과의 독립 경계
- 혼동 경계: 높은 하의 허리선과 empire 드레스 절개는 다른 소유자다; 짧은 러플 모두를 peplum으로 합치지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.peplum, wardrobe.panel.structure
- 현 후보 이웃(표현 대조, 의미 보증 아님): architectural_peplum, clt_ct005_v1, hw_empire_raised_waist_1, hw_empire_raised_waist_2
- 현 프로필 이웃(표현 대조): clothing_ct005_v1, hw_empire_raised_waist

**독립 구현 1:** A short flared peplum panel projects from the bodice waist above the fitted skirt.

관계: `peplum panel` → `same dress's waist above its skirt` (project_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR046 — 바이어스와 드레이프

- 원문 범위: 바이어스 컷 / 드레이프
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: bias는 결에 대한 재단 방향, drape는 직물의 보이는 낙하·접힘 상태다. 재단 방식이 요청되면 명세를 보존하되 그 자체의 픽셀 인증은 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 직물이 닿는 지점; 접촉 사이 늘어진 곡선; 밑단의 비강제 흐름
- 혼동 경계: drape=루칭·bodycon이 아니다; 유연한 흐름만으로 45도 재단을 확정하지 않는다
- 주장 한계: 정확 재단각·결 방향이 숨겨지면 명세 확인 대상으로 남긴다.
- 부분 속성 제안: wardrobe.drape, wardrobe.panel.folds
- 현 후보 이웃(표현 대조, 의미 보증 아님): andean_poncho_panel_system, animated_inanimate_helper, basted_toile_dress_form_prop, bias_cut_body_skimming_drape, ccx_cc41_01, ccx_cc41_02, cheekbone_to_temple_blush_drape, chrh_hair_color_state_hair_body_overlap, clt_ct011_v2, clt_ct037_v1, clt_ct077_v1, clt_ct091_v1
- 현 프로필 이웃(표현 대조): andean_poncho_central_opening_panel_system, cheekbone_temple_blush_drape, chrh_rel_hair_color_state_hair_body_overlap, clothing_ct011_v2, clothing_ct037_v1, clothing_ct077_v1, clothing_ct142_v1, costume_ccx_cc41_01, costume_ccx_cc41_02, couture_atelier_individual_construction, fit_ff31_v1, fit_ff38_v1

**독립 구현 1:** The skirt's soft fabric hangs in curved folds between the waist attachment and its free hem.

관계: `same skirt's soft folds` → `waist attachment and free hem` (hang_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S20: Seamwork — How to Sew Bias-Cut Garments](https://www.seamwork.com/sewing-tutorials/how-to-sew-bias-cut-garments), [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

## AFR047 — 루칭·셔링·스모킹

- 원문 범위: 루칭 / 셔링 / 스모킹
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: ruching은 국소적으로 모은 주름, shirring은 여러 봉제 행, smocking은 주름을 연결하는 장식 고정 계열이다. 탄성 shirring과 자수 smocking의 혼용을 기록한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 주름의 모임 방향; 반복 봉제 행; 선택된 주름 사이 연결 자수
- 혼동 경계: 아무 주름을 셋 모두의 증거로 쓰지 않는다; 탄성·수축률은 정지 사진에서 확정하지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.gathers_shirring_smock
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct064_v1, clt_ct064_v2, harem_gathered_waist_ankle_cuff, leggings_center_back_scrunch_channel, pfe_ruching_candidate, sw_candidate_ruched, sw_candidate_shirred, sw_candidate_smocked, y2kr_ruched_top
- 현 프로필 이웃(표현 대조): balloon_curved_leg_tapered_hem, clothing_ct064_v2, gathered_ankle_voluminous_trouser, pfe_ruching, sw_ruched, sw_shirred, sw_smocked, y2kr_ruched_top

**독립 구현 1:** Parallel stitched rows gather the same blouse's waist panel into small repeated folds.

관계: `parallel shirring rows` → `same blouse's waist panel` (gather, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Decorative stitches connect adjacent small pleats across the same blouse's smocked panel.

관계: `smocking decorative stitches` → `adjacent pleats on the same blouse panel` (connect, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S21: Tilly and the Buttons — How to Sew Shirring](https://tillyandthebuttons.com/blogs/sewing/how-to-sew-shirring), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR048 — 민소매와 암홀 범위

- 원문 범위: 슬리브리스 / 스파게티 스트랩 / 딥 암홀 / 드롭 암홀 / 컷어웨이 숄더
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: 소매 유무·끈 폭·암홀 아래점·어깨 전면 경계는 독립 축이다. deep/drop은 개구부 범위와 lowered sleeve 형태가 중첩되는 제품 표현이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 암홀 경계와 겨드랑이 기준; 얇은 끈이 연결하는 앞뒤; 이너의 같은 구역 커버리지
- 혼동 경계: 민소매가 겨드랑이 전체 가시성을 보장하지 않는다; 팔 자세·겉코트가 가리면 관찰 불가다; deep armhole과 sideboob는 별개다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.coverage.opening_location, wardrobe.structure.strap_attachment
- 현 후보 이웃(표현 대조, 의미 보증 아님): cold_shoulder_cutout_sleeve_bridge, dark_spaghetti_strap_top, sff_extra_xa045, sw_candidate_jane, unif_sleeveless_robe_over_inner_sleeves, y2kr_crop_tank, y2kr_denim_vest, y2kr_rib_tank
- 현 프로필 이웃(표현 대조): cold_shoulder_cutout_topology, sw_jane, uniform_sleeveless_robe_over_inner_sleeves, y2kr_crop_tank, y2kr_denim_vest, y2kr_rib_tank

**독립 구현 1:** The sleeveless top's armhole edge curves below the same wearer's underarm beside a visible inner layer.

관계: `top armhole edge` → `same wearer's underarm beside the inner layer` (curve_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S18: Sherri Hill — What Is a Halter Dress?](https://www.sherrihill.com/blogs/news/what-is-a-halter-dress), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR049 — 등 개방과 끈 토폴로지

- 원문 범위: 레이서백 / 오픈백 / 백리스 / 로백 / 크로스백
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: racerback은 중앙 합류, crossback은 교차, low-back은 낮은 뒷윗선, open/backless는 열린 등판 범위다. 전체 빈 면적과 끈 그래프는 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 선택된 뒷면 목선; 끈이 만나는 점 또는 X교차; 같은 의복에 연결된 끈 끝
- 혼동 경계: 뒤를 못 보는 정면 이미지로 등 구조 PASS를 주지 않는다; Y와 X를 합치지 않는다; 겉옷·머리 가림을 기록한다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.structure.back_strap_connection, wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): backless_loafers, clt_ct124_v1, court_skort_racerback_top_ensemble, crossback_strap_intersection, fit_ff20_v2_candidate, fit_ff52_v1_candidate, fit_ff52_v2_candidate, pfe_back_face_candidate, pfe_hair_clearance_candidate, racerback_strap_yoke_convergence, running_split_short_racerback_tank_ensemble, selective_open_back_stable_front_coverage
- 현 프로필 이웃(표현 대조): clothing_ct124_v1, fit_ff20_v2, fit_ff52_v1, fit_ff52_v2, pfe_back_face, racerback_sports_bra_strap_convergence, sw_crossback, sw_scoopback

**독립 구현 1:** Two back straps cross in an X between the same top's shoulder attachments and opposite lower back edges.

관계: `same top's back straps` → `opposite lower-back attachment points` (cross, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The top's shoulder straps converge into one central band between the shoulder blades.

관계: `same top's shoulder straps` → `central back band` (converge_into, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S18: Sherri Hill — What Is a Halter Dress?](https://www.sherrihill.com/blogs/news/what-is-a-halter-dress), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR050 — 사이드 오픈과 위치별 컷아웃

- 원문 범위: 사이드 오픈 / 웨이스트 컷아웃 / 버스트 컷아웃 / 언더버스트 컷아웃
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: open-sided는 옆판이 열리는 구성, cut-out은 특정 몸 부위의 창이다. waist/bust/underbust는 창의 위치이며 내부는 피부·이너·다른 원단일 수 있다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 같은 의복의 개구부 둘레; 창과 몸 기준점; 창 안의 실제 피부 또는 이너
- 혼동 경계: underbust opening이 가슴 아래 피부를 보장하지 않는다; 검정 프린트를 열린 구멍으로 판정하지 않는다; 허리와 bust 개구부를 바꾸지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): hw_dangui_open_sides_1, hw_dangui_open_sides_2, hw_dangui_open_sides_3, pfe_cutout_candidate, sw_candidate_cutout
- 현 프로필 이웃(표현 대조): hw_dangui_open_sides, pfe_cutout, sw_cutout

**독립 구현 1:** The knit dress has bounded openings at each side of the same wearer's waist.

관계: `knit-dress cutout edges` → `same wearer's left and right waist regions` (bound_at, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR051 — 사이드붑과 언더붑의 실제 상태

- 원문 범위: 사이드붑 / 언더붑
- 우선순위 / 유형: P1 / visible_state
- 뜻과 축: sideboob는 가슴 측면, underboob는 아래쪽 일부가 실제 보이는 상태 표현이다. 옷 종류·끈 위치·underbust 코르셋과 다른 관찰 대상이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 측면 또는 아래의 지정된 피부 구역; 그 구역을 노출시키는 의복 경계; 해당 구역의 이너·겉옷 가림
- 혼동 경계: 깊은 암홀만으로 측면 가시성을 확정하지 않는다; underbust cutout이 상복부만 보이면 underboob가 아니다
- 주장 한계: 기존 pfe_lateral_chest와 pfe_lower_chest의 정의·범위부터 대조한다. S17·S16은 모든 인터넷 별칭의 독립 사전 인증이 아니다.
- 부분 속성 제안: wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): pfe_lateral_chest_candidate, pfe_lower_chest_candidate
- 현 프로필 이웃(표현 대조): pfe_lateral_chest, pfe_lower_chest

**독립 구현 1:** A narrow outer-bust skin region is visible beside the adult wearer's deeply lowered armhole edge.

관계: `adult wearer's outer-bust skin region` → `same top's lowered armhole edge` (visible_beside, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** A narrow lower-bust skin region is visible directly below the adult wearer's top hem.

관계: `adult wearer's lower-bust skin region` → `same top's hem` (visible_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR052 — 미드리프와 배꼽

- 원문 범위: 미드리프 베어링 / 네이블 베어링
- 우선순위 / 유형: P0 / visible_state
- 뜻과 축: midriff는 상하의 사이 복부 가시 구간, navel-baring은 배꼽이라는 특정 기준점의 실제 가시 상태다. crop·low-rise를 각각 독립 조건으로 유지한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 상의 하단 경계; 하의 상단 경계; 두 경계 사이 지정 복부·배꼽; 가림 여부
- 혼동 경계: 복부가 보여도 배꼽은 가려질 수 있다; 크롭+하이웨이스트가 겹치면 빈 간격이 없다
- 주장 한계: 픽셀에서 배꼽 기준점이 안 보이면 navel 가시성은 통과하지 않는다. 몸 비율을 변경하지 않는다.
- 부분 속성 제안: wardrobe.coverage.opening_location, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): pfe_navel_candidate
- 현 프로필 이웃(표현 대조): pfe_navel

**독립 구현 1:** The top hem and trouser waistband leave a visible strip of upper abdomen while the navel remains below the waistband.

관계: `same wearer's top hem and trouser waistband` → `upper-abdomen strip` (leave_gap, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The same adult wearer's navel is visible in the gap between the top hem and low trouser waistband.

관계: `adult wearer's navel` → `same wearer's top hem and trouser waistband` (visible_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types)

## AFR053 — 시어와 직접 개방

- 원문 범위: 시어 / 시스루
- 우선순위 / 유형: P0 / material_state
- 뜻과 축: sheer는 실제 원단을 통과해 밑의 피부·이너가 읽히는 성질이다. 원단 없는 창과 별개이며 소재 이름만으로 투과성을 결정하지 않는다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어에 결속한다. 성인 초상 노출 의미는 기존 범위 조건을 보존한다.
- 관찰 단서: 앞의 원단 경계·망 또는 주름; 뒤의 피부·이너 윤곽; 빛과 중첩 층
- 혼동 경계: 베이지 불투명 천을 맨살로 오인하지 않는다; 얇음·빛 반사만으로 sheer PASS를 주지 않는다
- 주장 한계: 명칭만으로 이너·노출·체형·치수·제작 이력을 확정하지 않는다.
- 부분 속성 제안: wardrobe.material.transmission, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): barong_tagalog_untucked_formal_shirt, chrh_hair_cut_see_through_bangs, clt_ct079_v1, clt_ct091_v1, ethereal_sheer_layering, fit_ff49_v2_candidate, mesh_sheer_layering, pfe_hosiery_sheer_candidate, pfe_mesh_skin_candidate, sff_extra_xa001, sff_extra_xa021, sff_pro_e01
- 현 프로필 이웃(표현 대조): chrh_rel_hair_cut_see_through_bangs, clothing_ct079_v1, clothing_ct091_v1, fit_ff49_v2, no_makeup_makeup_layering, pfe_hosiery_sheer, pfe_mesh_skin, restrained_polished_natural_makeup_balance, sheer_garment_optical_layering, sw_mesh, y2kr_sheer_nylon, y2kr_sheer_top

**독립 구현 1:** The sheer blouse's fine weave overlays the sharply bounded camisole neckline beneath it.

관계: `sheer blouse weave` → `same wearer's inner camisole neckline` (overlay, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S33: FALKE — Tights Styling](https://www.falke.com/us_en/journal/tights-styling/), [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types)

## AFR054 — 스커트 길이 기준

- 원문 범위: 미니스커트 / 마이크로미니 / 미디 / 맥시
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: mini/micro/midi/maxi는 신체에 대한 밑단 위치 범주다. 기장 cm·촬영 시점·착용자 비례가 없으면 보편 수치 경계를 만들지 않는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 같은 스커트 밑단; 무릎·종아리·발목 기준; 타이츠·부츠의 가림 층
- 혼동 경계: 미니=맨살 허벅지가 아니다; 맥시=얕은 트임이 아니다; 포트레이트 크롭에서 밑단을 못 보면 기장 미확인
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct076_v1, clt_ct076_v2, cold_shoulder_knit_top_midi_skirt, cropped_wide_leg_culotte_geometry, culotte_button_front_blouse, culotte_inseam_leg_separation, electronic_control_separation_light, electronic_instrument_signal_studio, midi_controller_external_sound_action, midi_controller_external_sound_chain_prop, midi_controller_touch_and_output_relation, midi_controller_touch_signal_pose
- 현 프로필 이웃(표현 대조): clothing_ct076_v1, culotte_cropped_wide_leg_topology, midi_controller_external_sound_source, pfe_mini_outer_leg, theremin_dual_antenna_noncontact, y2kr_micro_mini

**독립 구현 1:** The midi skirt's hem falls below the knee and above the same wearer's ankle.

관계: `midi skirt hem` → `same wearer's knee and ankle` (fall_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR055 — 펜슬과 A라인

- 원문 범위: 펜슬 스커트 / A라인
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: pencil은 몸을 따라 좁게 떨어지는 외곽, A-line은 허리에서 아래로 넓어지는 외곽이다. 길이·핏·플리츠·슬릿과 함께 성립한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 허리와 힙의 의복 경계; 밑단 폭; 폭의 증가 또는 좁은 낙하
- 혼동 경계: 좁은 허리를 몸 수정으로 만들지 않는다; 두 이름을 미니·미디 길이와 합치지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.silhouette.torso_outline, wardrobe.panel.structure
- 현 후보 이웃(표현 대조, 의미 보증 아님): business_blouse_pencil_skirt, chrh_hair_cut_a_line, ctx_c135, exercise_dress_integrated_liner_ensemble, ia_go_review, one_piece_a_line_dress, water_w139
- 현 프로필 이웃(표현 대조): chrh_rel_hair_cut_a_line, hogarth_waving_line_of_beauty, ia_profile_go_review, irreversible_threshold_crossing_consequence, one_piece_dress_construction, water_rel_w139

**독립 구현 1:** The skirt's side edges widen progressively from its waistband toward the hem.

관계: `A-line skirt side edges` → `same skirt's waistband and hem` (widen_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR056 — 플리츠 토폴로지

- 원문 범위: 플리츠 스커트 / 나이프 플리츠 / 박스 플리츠 / 아코디언 플리츠
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: pleated는 접힘 계열, knife는 반복 단방향, box는 양쪽 대칭 접힘과 평평한 면, accordion은 촘촘한 지그재그 계열이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 접힘 방향; 평평한 면과 모서리; 반복 주기와 펼쳐지는 부분
- 혼동 경계: 단순 gathered 잔주름을 knife로 합치지 않는다; knife·box·accordion을 한 이미지에 전부 의무화하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.pleat_topology
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct063_v1, clt_ct063_v2, hw_francaise_free_back_1
- 현 프로필 이웃(표현 대조): clothing_ct063_v1, clothing_ct063_v2, hw_francaise_free_back

**독립 구현 1:** The skirt's knife pleats overlap in one repeated direction below the waistband.

관계: `same skirt's knife pleats` → `waistband-to-hem sequence` (overlap_in_direction, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Opposing folds frame each broad flat face of the skirt's box pleats.

관계: `opposing box-pleat folds` → `same skirt's flat pleat faces` (frame, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S21: Tilly and the Buttons — How to Sew Shirring](https://tillyandthebuttons.com/blogs/sewing/how-to-sew-shirring)

## AFR057 — 랩과 킬트풍

- 원문 범위: 랩 스커트 / 킬트 / 킬트풍 스커트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: wrap은 겹쳐 감싸는 구조, kilt는 역사적 복식 및 특정 구성 계열이다. kilt-inspired 상품의 타탄·버클·플리츠는 각기 다른 축이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 같은 스커트 앞판 겹침; 선택한 옆 잠금; 뒤 또는 옆의 주름
- 혼동 경계: 타탄만으로 정통 kilt 인증을 주지 않는다; 랩을 중앙 슬릿으로 바꾸지 않는다; 스코틀랜드 정체성은 별도다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.panel.structure, wardrobe.details.pleat_topology
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct018_v1, kilt_flat_apron_side_back_pleats, scottish_kilt_pleated_wrap_system, simple_top_wrap_skirt_ensemble, wrap_skirt_diagonal_overlap_closure
- 현 프로필 이웃(표현 대조): clothing_ct018_v1

**독립 구현 1:** The skirt's outer front panel overlaps the inner panel and fastens at the same skirt's side waist.

관계: `outer wrap-skirt panel` → `inner panel and side-waist closure` (overlap_and_fasten, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S08: Museum at FIT — Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/)

## AFR058 — 단·버블·비대칭 밑단

- 원문 범위: 티어드 스커트 / 버블 스커트 / 비대칭 밑단 / 하이로 밑단 / 핸커치프 헴
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: tiered는 가로 단 연결, bubble은 안쪽으로 모인 부풀음, asymmetric는 불균일, high-low는 앞뒤 등 특정 길이 차, handkerchief는 여러 뾰족한 낙하이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 가로 단 이음선; 안으로 돌아 모이는 밑단; 앞뒤 높이; 여러 끝점
- 혼동 경계: 물결 주름을 단층 구조로 인증하지 않는다; 임의 비대칭과 여러 모서리 헴을 같은 구조로 합치지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.skirt_layering, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): asymmetrical_hemline, clt_ct018_v2, clt_ct062_v1, clt_ct062_v2, y2kr_handkerchief_hem, y2kr_tiered
- 현 프로필 이웃(표현 대조): clothing_ct018_v2, y2kr_handkerchief_hem, y2kr_tiered

**독립 구현 1:** The skirt's inflated lower panel turns inward and gathers into its shorter inner hem.

관계: `bubble-skirt lower panel` → `same skirt's gathered inner hem` (turn_inward, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S20: Seamwork — How to Sew Bias-Cut Garments](https://www.seamwork.com/sewing-tutorials/how-to-sew-bias-cut-garments)

## AFR059 — 니트·스웨터·터틀 드레스

- 원문 범위: 니트 드레스 / 스웨터 드레스 / 터틀넥 드레스
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: knit은 편직 원단, sweater는 상의 유래의 실루엣 표현, turtleneck은 칼라 구조다. fitted 또는 loose, mini 또는 midi가 별도로 적용된다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 드레스 표면의 코; 선택한 칼라 접힘; 길이가 이어진 동일 몸판
- 혼동 경계: 모든 knit가 굵은 sweater는 아니다; 터틀넥은 bodycon·노출 정도를 결정하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.material.visible_weave, wardrobe.neckline, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The continuous rib-knit dress body extends from its folded neck band to a mid-calf hem.

관계: `same rib-knit dress body` → `folded neck band and mid-calf hem` (extend, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

## AFR060 — 원피스의 기본 구조 계열

- 원문 범위: 슬립 드레스 / 랩 드레스 / 블레이저 드레스 / 셔츠 드레스 / 피나포어 드레스 / 시스 드레스
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: slip은 끈·간결한 몸판, wrap은 겹침, blazer는 재킷 여밈, shirt는 칼라·플래킷, pinafore는 덧입는 민소매, sheath는 좁은 외곽 계열이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 각 의상 고유 목선·앞판; 같은 드레스의 치마로 이어지는 경계; 피나포어 아래 별도 이너
- 혼동 경계: 현대 상품명 중첩을 인정한다; 긴 셔츠라고 모두 dress는 아니다; 모든 sheath가 강한 밀착은 아니다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.wardrobe_structure, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct020_v1, clt_ct020_v2, deconstructed_mummy_wrap_dress, dropwaist_satin_slip_dress, nineties_slip_dress_layered, one_piece_shirt_dress, one_piece_wrap_dress, pale_yellow_gauze_slip_dress, y2kr_slip
- 현 프로필 이웃(표현 대조): clothing_ct020_v1, one_piece_dress_construction, y2kr_slip

**독립 구현 1:** A separate blouse collar and sleeves emerge from beneath the sleeveless pinafore dress.

관계: `inner blouse collar and sleeves` → `same wearer's pinafore neckline and armholes` (emerge_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR061 — 슬릿의 위치·깊이와 벤트

- 원문 범위: 사이드 슬릿 / 프런트 슬릿 / 더블 슬릿 / 싸이하이 슬릿 / 벤트
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: side/front/double는 위치와 수, thigh-high는 위 끝의 몸 기준, vent는 겹침형 이동 여유 구성이다. 치마 전체 길이와 분리한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 트임 위 끝과 밑단; 각 트임의 둘레; 겹쳐 남은 vent 플랩; 그 안의 실제 타이츠 또는 피부
- 혼동 경계: 긴 치마=다리 전체 가림은 아니다; 깊은 슬릿=보이는 허벅지가 아니다; 열린 앞판 틈을 슬릿 두 개로 세지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.hem_slit_vent, wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct061_v1, clt_ct061_v2, clt_ct140_v2, fire_f070, hydrothermal_altered_ground_mineral_crust_surface, hydrothermal_vent_alteration_relation, hydrothermal_vent_field_location, localized_hydrothermal_steam, pfe_slit_candidate, sff_pro_g07, soil_e044, vent_plume_altered_ground_frame
- 현 프로필 이웃(표현 대조): clothing_ct061_v1, clothing_ct061_v2, clothing_ct140_v2, face_pareidolia_embedded_nonface_pattern, fire_rel_f070, pfe_slit, soil_rel_e044, water_rel_w062, water_rel_w088

**독립 구현 1:** The maxi skirt's side slit opens from a point on the thigh down to the same skirt's ankle-length hem.

관계: `maxi-skirt side-slit edges` → `thigh-height endpoint and ankle-length hem` (open_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The skirt's back vent keeps one lower panel overlapping the other beneath the vent endpoint.

관계: `back-vent outer panel` → `same skirt's inner panel below the vent endpoint` (overlap, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR062 — 스트레이트·와이드·팔라초

- 원문 범위: 스트레이트 / 와이드 레그 / 팔라초
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: straight는 비교적 곧은 다리 외곽, wide는 전반적인 폭, palazzo는 매우 넓고 유연하게 흐르는 팬츠 표현이다. 허리선과 길이는 별도다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 힙 아래부터 이어지는 폭; 무릎과 밑단 관계; 실제 두 바지 다리 사이 분기
- 혼동 경계: 전부 바닥 길이·하이웨이스트로 고정하지 않는다; 넓은 천을 스커트로 오인하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.trouser_leg_shape, wardrobe.drape
- 현 후보 이웃(표현 대조, 의미 보증 아님): crop_top_wide_pants, cropped_wide_leg_culotte_geometry, flare_legging_knee_to_hem_expansion, palazzo_full_length_wide_leg_geometry, straight_black_hair_with_bangs, wide_leg_long_line, wrap_front_blouse_straight_trousers
- 현 프로필 이웃(표현 대조): culotte_cropped_wide_leg_topology

**독립 구현 1:** Two broad palazzo trouser legs separate below the crotch and hang in independent vertical folds.

관계: `same palazzo trouser legs` → `crotch and independent lower folds` (separate_and_hang, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR063 — 테이퍼와 배럴

- 원문 범위: 테이퍼드 / 배럴
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: tapered는 아래로 좁아지는 폭 분포, barrel은 허벅지·무릎의 바깥 볼록함과 밑단 수축이다. balloon과의 명칭 중첩은 기존 fit 의미로 대조한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 양쪽 다리 외곽 최대 폭; 무릎 부근 곡선; 좁아지는 밑단
- 혼동 경계: 발목만 좁다고 모두 barrel은 아니다; 착용자 다리 굽힘과 바지 곡선을 분리한다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.silhouette.outer_leg_curve, wardrobe.fit.hem_taper
- 현 후보 이웃(표현 대조, 의미 보증 아님): balloon_convex_leg_tapered_hem_silhouette, balloon_leg_curve_tapered_hem, chrh_hair_cut_feathered_ends, classic_tapered_wing_liner, clt_ct031_v2, fire_f012, fit_ff12_v2_candidate, fit_ff26_v1_candidate, fitted_top_balloon_trouser_ensemble, mg_tapered_stroke, punk_clockpunk_mechanism_prop, salwar_kameez_tunic_trouser_scarf_system
- 현 프로필 이웃(표현 대조): balloon_curved_leg_tapered_hem, ca_pointed_ear_panels, cheekbone_temple_blush_drape, cjk_seed_face_relation, clothing_ct031_v2, fire_rel_f012, fit_ff12_v2, fit_ff26_v1, mg_tapered_stroke_relation, restrained_polished_natural_makeup_balance, sca_h05, soil_rel_e065

**독립 구현 1:** The trouser legs bow outward around the knees before narrowing toward the ankle hems.

관계: `same barrel trouser legs` → `knee-level volume and ankle hems` (curve_then_narrow, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR064 — 부츠컷·플레어·시가렛

- 원문 범위: 부츠컷 / 플레어 / 시가렛 팬츠
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: bootcut은 무릎 아래 완만한 퍼짐, flare는 더 뚜렷한 퍼짐 계열, cigarette는 가늘고 비교적 곧은 외곽이다. 브랜드별 경계 차이를 유지한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 허벅지·무릎의 비교 폭; 아래 퍼짐 시작점; 밑단 폭
- 혼동 경계: bootcut에 실제 부츠를 자동 추가하지 않는다; cigarette 흡연 소품과 다른 대상이다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.flared_trouser_hem, wardrobe.details.trouser_leg_shape
- 현 후보 이웃(표현 대조, 의미 보증 아님): alto_tenor_saxophone_reed_keywork_prop, anamorphic_horizontal_flare, circular_sun_flare, clt_ct005_v1, clt_ct013_v2, clt_ct048_v1, clt_ct065_v2, fire_f108, fire_f126, fit_ff15_v2_candidate, flare_legging_knee_to_hem_expansion, modern_piston_trumpet_prop
- 현 프로필 이웃(표현 대조): alto_tenor_saxophone_reed_conical_body, ca_flared_lower_form, clothing_ct005_v1, clothing_ct013_v2, clothing_ct048_v1, clothing_ct065_v2, diffusion_filter_highlight_halation, fire_rel_f108, fire_rel_f126, fire_rel_f131, fire_rel_f132, fire_rel_f133

**독립 구현 1:** The close-fitting trouser legs widen gradually below the knees toward their bootcut hems.

관계: `same trouser legs` → `knee points and bootcut hems` (widen_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR065 — 퀼로트와 밑위 축

- 원문 범위: 퀼로트 / 하이웨이스트 / 미드라이즈 / 로라이즈
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: culottes는 짧고 넓은 두 바지 다리, rise는 허리밴드 위치다. 시각 기준점과 패턴상의 crotch-to-waist 치수를 혼동하지 않는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 두 다리 분기; 허리밴드의 실제 신체 위치; 위 상의의 겹침
- 혼동 경계: 스커트 같은 외형만으로 두 다리를 인증하지 않는다; low-rise=배꼽 가시가 아니다; 하이웨이스트와 high-leg는 별개다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.length.hem_landmark, wardrobe.details.trouser_leg_shape
- 현 후보 이웃(표현 대조, 의미 보증 아님): culotte_button_front_blouse, high_rise_waist_navel_relation, palazzo_full_length_wide_leg_geometry, sff_extra_xa016, sff_pro_e24, sw_candidate_midlowrise, y2kr_crop_low, y2kr_low_cargo, y2kr_low_rise, y2kr_ultra_low
- 현 프로필 이웃(표현 대조): culotte_cropped_wide_leg_topology, longline_sports_bra_extended_underband, sw_midlowrise, y2kr_crop_low, y2kr_low_cargo, y2kr_low_rise, y2kr_ultra_low

**독립 구현 1:** The culottes divide into two wide legs with hems ending around the same wearer's mid-calf.

관계: `same culottes` → `two wide mid-calf trouser legs` (divide_into, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR066 — 쇼츠 길이와 스코트

- 원문 범위: 테일러드 쇼츠 / 핫팬츠 / 마이크로 쇼츠 / 버뮤다 쇼츠 / 스코트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: tailored는 여밈·주름의 정돈, hot/micro는 매우 짧은 범주, Bermuda는 무릎 부근 기장, skort는 스커트 외형과 쇼츠 결합이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 선택한 쇼츠의 두 다리 밑단; 허리 주름·포켓; 스커트 앞판 뒤의 별도 쇼츠
- 혼동 경계: micro의 보편 cm를 만들지 않는다; 숨은 쇼츠가 안 보이면 skort 결합은 미확인; 짧은 하의=하의 없음이 아니다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.length.hem_landmark, wardrobe.details.skirt_layering
- 현 후보 이웃(표현 대조, 의미 보증 아님): bermuda_two_knee_length_short_hems, biker_short_thigh_knee_landmark, casual_capri_below_knee_clear_ankle_gap, court_skort_racerback_top_ensemble, fitted_top_bermuda_slim_belt_ensemble, micro_short_proportion, skort_outer_panel_inner_shorts
- 현 프로필 이웃(표현 대조): active_skort_outer_skirt_inner_shorts, capri_trouser_below_knee_clear_ankle_gap, exercise_dress_integrated_short_liner, two_in_one_running_shorts_dual_layer

**독립 구현 1:** The skort's wrap-like front panel overlaps a separately visible pair of shorts beneath it.

관계: `skort front skirt panel` → `same garment's visible shorts layer` (overlap, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR067 — 레깅스와 스티럽

- 원문 범위: 레깅스 / 스티럽 팬츠
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: leggings는 밀착한 신축성 하의, stirrup은 발 아래로 거는 실제 고리 구조다. 소재와 고리는 별도다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 다리 의복의 연속 경계; 발 아래 스트랩 경로; 밑단과 스트랩 연결
- 혼동 경계: 밀착만으로 압박 기능을 인증하지 않는다; 발 아래 고리가 안 보이면 stirrup은 관찰 불가
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.trouser_leg_shape, wardrobe.structure.strap_attachment
- 현 후보 이웃(표현 대조, 의미 보증 아님): athletic_unitard_continuous_one_piece, capri_legging_mid_calf_landmark, fit_ff53_v1_candidate, flare_legging_knee_to_hem_expansion, leggings_absent_center_front_seam, leggings_center_back_scrunch_channel, leggings_crossover_front_waistband, leggings_v_back_waistband, seven_eighth_legging_ankle_landmark, stirrup_legging_underfoot_loop, studio_bra_tank_seven_eighth_legging_ensemble, sw_candidate_leggings
- 현 프로필 이웃(표현 대조): fit_ff53_v1, stirrup_leggings_underfoot_loop, sw_leggings, two_in_one_running_shorts_dual_layer, unitard_upper_crotch_leg_continuity

**독립 구현 1:** Each stirrup strap connects the trouser hem edges beneath the same wearer's foot.

관계: `stirrup trouser straps` → `same wearer's feet and trouser hem edges` (connect_beneath, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S19: Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

## AFR068 — 동물성 섬유의 출처 메타데이터

- 원문 범위: 울 / 메리노 울 / 램스울 / 캐시미어 / 모헤어 / 앙고라 / 알파카
- 우선순위 / 유형: P1 / metadata
- 뜻과 축: 울·품종·어린 양·염소 속털·Angora goat mohair·rabbit angora·alpaca의 출처 의미를 보존한다. 사진 구현은 보풀 길이·코 크기·광택·두께 등 별도 선택 속성으로 작성한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 선택된 의복 표면의 보풀 길이; 편직코 크기; 선택한 표면 반사
- 혼동 경계: 보풀=모헤어·앙고라·캐시미어 성분 인증이 아니다; cashmere=camel 색이 아니다; mohair goat와 angora rabbit을 합치지 않는다
- 주장 한계: 상품 명세·섬유 라벨·시험 정보 없이 픽셀로 동물 기원·품종·함량·마이크론·촉감·가격을 판정하지 않는다.
- 부분 속성 제안: wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): fine_wool_cashmere_matte_pile_surface, needle_felt_fiber_texture, needle_felt_wool_prop, tartan_wool_twill_sett_surface
- 현 프로필 이웃(표현 대조): low_brand_prominence_material_luxury, qipao_standing_collar_diagonal_closure_system

이 카드는 명세/용어 메타데이터다. 숨은 기원·수치·가격을 픽셀 프로필로 자동 승격하지 않는다.

출처: [S28: Woolmark — What is Merino wool?](https://www.woolmark.com/en-hk/fibre/what-is-merino-wool/), [S29: Mohair South Africa — The Fibre](https://www.mohair.co.za/natural-fibre), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR069 — 트위드·부클레·플란넬·코듀로이

- 원문 범위: 트위드 / 부클레 / 플란넬 / 코듀로이
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: tweed는 직물 계열, bouclé는 루프성 실·표면, flannel은 기모, corduroy는 반복 파일 골이다. 체크와 원산지는 별도다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 혼합 실·루프 표면; 낮은 기모; 평행 골의 간격·입체감
- 혼동 경계: tweed=하운즈투스가 아니다; flannel=check가 아니다; corduroy 골과 rib 니트 코는 다르다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.material.visible_weave, wardrobe.pattern
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct089_v1, clt_ct089_v2, dark_academia_tweed_outfit, sff_pro_t10
- 현 프로필 이웃(표현 대조): clothing_ct089_v1

**독립 구현 1:** Raised corduroy wales run vertically along the skirt's fabric surface.

관계: `corduroy pile wales` → `same skirt's vertical fabric surface` (run_along, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Small yarn loops rise from the same jacket's bouclé fabric surface.

관계: `bouclé yarn loops` → `same jacket's fabric surface` (rise_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S32: Johnstons of Elgin — International Tweed Day](https://discover.johnstonsofelgin.com/our-story/international-tweed-day), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR070 — 개버딘·능직·데님·저지·폰테

- 원문 범위: 개버딘 / 트윌 / 능직 / 데님 / 저지 / 폰테
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: gabardine은 치밀한 능직 계열, twill은 사선 교차 조직, denim은 특정 능직 계열, jersey와 ponte는 니트 계열이다. 색·섬유·두께와 조직을 분리한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 가까이 읽히는 사선 조직; 니트 코 또는 표면; 데님 워싱 경계
- 혼동 경계: 파란색=denim이 아니다; 매끈함=ponte가 아니다; 정지 표면만으로 double-knit·신축률을 인증하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.material.visible_weave, wardrobe.surface.denim_chambray
- 현 후보 이웃(표현 대조, 의미 보증 아님): blokecore_aesthetic, clt_ct026_v1, clt_ct026_v2, clt_ct084_v1, clt_ct084_v2, clt_ct086_v1, clt_ct086_v2, clt_ct087_v1, clt_ct087_v2, clt_ct098_v1, contemporary_heisei_y2k_layers, cropped_tank_denim_casual
- 현 프로필 이웃(표현 대조): clothing_ct026_v1, clothing_ct026_v2, clothing_ct084_v1, clothing_ct086_v1, clothing_ct098_v1, y2kr_cropped_denim_jacket, y2kr_denim_bag, y2kr_denim_dress, y2kr_denim_jacket, y2kr_denim_mini, y2kr_denim_vest, y2kr_flare_yoga

**독립 구현 1:** Fine diagonal twill ridges cross the same coat's compact fabric surface.

관계: `fine twill ridges` → `same coat's compact fabric surface` (cross, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S01: Burberry — The History of the Trench Coat](https://int.burberry.com/c/burberry-world/heritage/trench-coat/)

## AFR071 — 벨벳과 벨루어

- 원문 범위: 벨벳 / 벨루어
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 촘촘한 짧은 파일의 깊은 명암 외형이 겹친다. woven velvet와 knit velour 등의 제조 차이는 명세 축이고 픽셀은 파일 방향·광택을 읽는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 짧은 파일 표면; 접힌 천의 서로 다른 명암; 방향에 따른 반사
- 혼동 경계: 짙은 단색만으로 velvet 통과시키지 않는다; 파일 외형만으로 knit/woven 기반을 확정하지 않는다
- 주장 한계: velvet_pile 경로는 제안이며 현 계약과 재검토한다. 재료 기반은 명세를 보존한다.
- 부분 속성 제안: wardrobe.material, wardrobe.surface.velvet_pile
- 현 후보 이웃(표현 대조, 의미 보증 아님): baroque_gilded_chiaroscuro_lighting, baroque_opulent_luxury_aesthetic, broken_luxury_core, ccx_cc31_01, ccx_cc31_02, cervid_velvet_antler_bud_ear_root, clt_ct089_v1, clt_ct089_v2, crown_on_cushion_prop, ctx_pile_turn, faded_luxury_after_event_trace, gilded_marble_velvet_opulence_surface
- 현 프로필 이웃(표현 대조): clothing_ct089_v2, costume_ccx_cc31_01, decadent_languor_environment, private_client_service_interaction, y2kr_velour, y2kr_velour_hoodie, y2kr_velour_pants

**독립 구현 1:** The skirt's short pile changes brightness across neighboring fabric folds.

관계: `same skirt's short pile` → `neighboring fabric folds` (change_across, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR072 — 새틴과 실크

- 원문 범위: 새틴 / 실크
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: satin은 긴 float를 가진 조직 또는 직물, silk는 섬유 기원이다. silk satin과 synthetic satin이 모두 가능하므로 alias로 합치지 않는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 매끄러운 직물의 연속 하이라이트; 접힘에서 넓어지고 좁아지는 반사; 동일 의복의 흐름
- 혼동 경계: 새틴 광택=실크 성분 인증이 아니다; 하이라이트만으로 조직 전체를 확정하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.satin_sateen, wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): business_blouse_pencil_skirt, celestial_silk_ribbon_robe, clt_ct085_v1, clt_ct085_v2, commoner_disguise_over_silk, coquette_balletcore_flatlay, couture_internal_support_and_drape_layers, draping_and_hand_finishing_couture_layers, dropwaist_satin_slip_dress, fine_silk_ribbon_texture, five_color_silk_strip_prop, fluid_satin_luster_drape_surface
- 현 프로필 이웃(표현 대조): clothing_ct085_v1, decadent_languor_environment, gradient_lip_center_distribution, qipao_standing_collar_diagonal_closure_system, restrained_polished_natural_makeup_balance, satin_directional_luster_drape_surface, self_possessed_sensual_presence, sw_finish, y2kr_satin

**독립 구현 1:** Broad satin highlights follow the curved folds on the same slip dress.

관계: `satin specular highlights` → `same slip dress's curved folds` (follow, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR073 — 레이스·메시·튈

- 원문 범위: 레이스 / 메시 / 튈
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: lace는 무늬와 구멍의 장식망, mesh는 망 구조, tulle은 가는 망 계열이다. 구멍·패턴·중첩·이너를 실제 운반체에 결속한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 레이스 무늬의 열린 셀; 균일 메시 눈; 밑 이너의 경계; 여러 튈 층
- 혼동 경계: 구멍 프린트가 실제 openwork는 아니다; mesh=피부 직접 노출은 아니다; 가죽 레이스업의 lace와 분리한다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.mesh_tulle_lace, wardrobe.material.transmission
- 현 후보 이웃(표현 대조, 의미 보증 아님): appearance_h013, athletic_mesh_open_structure, basted_toile_dress_form_prop, bat_shadow_lace_prop, body_mapped_circular_knit_zones, ccx_cc26_02, ccx_cc27_01, charred_paper_edge, clt_ct055_v2, clt_ct090_v1, clt_ct090_v2, clt_ct152_v1
- 현 프로필 이웃(표현 대조): appearance_rel_h013, clothing_ct055_v2, clothing_ct090_v1, clothing_ct090_v2, clothing_ct152_v1, costume_ccx_cc26_02, costume_ccx_cc27_01, cycling_bib_shorts_strap_pad_continuity, egr_profile_high_collar_lace_structure, egr_profile_micropleated_tulle_panel, electric_faraday_mesh_enclosure_relation, fit_ff44_v2

**독립 구현 1:** The floral lace openings reveal the contrasting camisole fabric directly underneath.

관계: `blouse floral-lace openings` → `same wearer's contrasting camisole` (reveal_underlayer, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR074 — 시폰과 오간자

- 원문 범위: 시폰 / 오간자
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 둘 다 얇고 투과성 있는 직물 변형이 가능하지만 chiffon은 유연한 낙하, organza는 비교적 서는 형태를 만드는 예가 많다. 사진 구현은 직접 낙하·볼륨을 지정한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 끝이 처지는 얇은 패널; 선택한 부풀어 선 패널; 빛 아래 보이는 이너
- 혼동 경계: 투과성만으로 둘을 구별하지 않는다; 실크 기원을 자동 인증하지 않는다; 뻣뻣함 물성값은 픽셀 단서와 별개다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.chiffon_organza_taffeta, wardrobe.drape
- 현 후보 이웃(표현 대조, 의미 보증 아님): sff_extra_xa002, sff_pro_y07, sheer_organza_chiffon_transmission
- 현 프로필 이웃(표현 대조): sheer_garment_optical_layering

**독립 구현 1:** The translucent organza sleeve holds a rounded volume above its gathered cuff.

관계: `organza sleeve shell` → `same sleeve's gathered cuff` (hold_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR075 — 가죽 외형·스웨이드·페이턴트·인조

- 원문 범위: 스무스 레더 / 스웨이드 / 페이턴트 레더 / 인조가죽
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: smooth는 매끄러운 면, suede는 짧은 nap, patent는 강한 코팅 반사, faux는 재료 모방이라는 기원이다. 외형과 실제 피혁·폴리머 성분을 분리한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 매끄러운 넓은 반사; 짧은 털결의 매트 명암; 강한 하이라이트 경계
- 혼동 경계: 반사만으로 가죽·PU·PVC를 인증하지 않는다; 인조가죽이 항상 특정 광택을 갖는 것은 아니다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.leather_suede_pvc
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct080_v1, clt_ct080_v2, sff_pro_f08, suede_nap_texture, tall_suede_boots, y2kr_patent, y2kr_patent_garment
- 현 프로필 이웃(표현 대조): clothing_ct080_v1, y2kr_patent

**독립 구현 1:** Bright, sharply edged highlights curve across the patent-finish boot shaft.

관계: `patent-finish highlights` → `same boot's shaft` (curve_across, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The suede jacket's short nap creates soft tonal changes across its folded sleeves.

관계: `suede-jacket short nap` → `same jacket's sleeve folds` (change_across, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S30: Dr. Martens — Patent Lamper Leather](https://www.drmartens.com/us/en/materials/patent-leather), [S31: UGG — Information on UGG and Our Brand](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig)

## AFR076 — 시어링·셰르파·페이크 퍼

- 원문 범위: 시어링 / 셰르파 / 페이크 퍼
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: shearling은 털이 붙은 양가죽, sherpa는 양털 같은 파일 직물 제품 계열, faux fur는 털 외형의 모방 재료다. 외형의 부풀음과 기원을 분리한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 칼라·커프스 파일과 매끄러운 몸판; 선택한 파일 뭉치 크기; 보이는 소재 접합 경계
- 혼동 경계: 양털 같은 외형만으로 animal hide를 인증하지 않는다; sherpa와 shearling은 동의어가 아니다; 털=겨울·성별 고정이 아니다; shearling fleece라는 상품 수식어에는 폴리에스터 제품도 있으므로 제품명과 소재 기원을 분리한다.
- 주장 한계: 한 장 외형으로 실제/인조 기원을 판정하지 않는다. sherpa 세부 사양은 제품별 명세 확인 대상이다.
- 부분 속성 제안: wardrobe.material, wardrobe.details.wardrobe_trim
- 현 후보 이웃(표현 대조, 의미 보증 아님): ccx_cc17_01, ccx_cc22_02, mob_wife_aesthetic, y2kr_faux_fur, y2kr_faux_fur_garment, y2kr_fur_trim
- 현 프로필 이웃(표현 대조): costume_ccx_cc17_01, costume_ccx_cc22_02, y2kr_faux_fur, y2kr_fur_trim

**독립 구현 1:** The jacket's dense fleece-like collar forms a separate textured border above its smooth outer panels.

관계: `fleece-like collar` → `same jacket's smooth outer panels` (form_border, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S31: UGG — Information on UGG and Our Brand](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S42: Patagonia — Retro Pile Fleece](https://www.patagonia.com/product/mens-retro-pile-fleece-pullover/22695.html)

## AFR077 — 리브·피셔맨·와플

- 원문 범위: 리브 / 골지 / 피셔맨 리브 / 와플 니트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: rib는 반복 골, fisherman은 부풀고 두터운 리브 변형, waffle은 작은 사각 요철 배열이다. 종류·치수·신축성과 분리한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 세로 또는 선택된 골 방향; 오목·볼록의 반복; 골과 주변 의복 곡면
- 혼동 경계: 바지 corduroy 파일과 knit rib를 합치지 않는다; 파일 브러싱이 코 구조를 대신하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.jersey_rib_interlock, wardrobe.material.visible_weave
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct010_v1, clt_ct087_v1, clt_ct087_v2, ctx_rib_flatten, pf_rib_vault_chapel_composition, pf_rib_vault_chapel_location, rib_knit_stretch_recovery_surface, ribbed_knit_body_boundary_surface, ribbed_knit_texture, sff_pro_t15, sky_blue_ribbed_cardigan_sweatpants, sw_candidate_rib
- 현 프로필 이웃(표현 대조): clothing_ct010_v1, clothing_ct087_v1, pf_rib_vault_chapel, sw_rib, vg_faille_crossgrain_ribs_profile, y2kr_rib_tank

**독립 구현 1:** Alternating raised knit ribs follow the same top's vertical torso surface.

관계: `same top's raised knit ribs` → `vertical torso fabric surface` (follow, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR078 — 케이블과 아란

- 원문 범위: 케이블 니트 / 아란 니트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: cable은 실 띠의 교차·꼬임 외형, Aran은 케이블·다이아몬드·복합 조직 계열이다. 아란 이름만으로 모든 전통 무늬를 의무화하지 않는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 교차하는 입체 띠; 배경 코의 다른 질감; 선택한 복합 무늬 구획
- 혼동 경계: 인쇄된 밧줄 그림과 실제 니트 교차를 분리한다; Cable=Aran 원산지 인증이 아니다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.details.cable_knit
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct008_v1, clt_ct008_v2
- 현 프로필 이웃(표현 대조): clothing_ct008_v1

**독립 구현 1:** Raised cable columns cross over one another against the sweater's flatter knit background.

관계: `same sweater's cable columns` → `flatter knit background` (cross_over, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR079 — 포인텔과 오픈 니트

- 원문 범위: 포인텔 / 오픈 니트
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: pointelle은 작은 규칙적 eyelet의 니트 표현, open knit는 성긴 코 사이 틈이라는 더 넓은 성질이다. 제작 방법과 투과·밑층을 따로 적는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 작은 규칙 eyelet; 구멍 사이의 실제 코; 아래 독립 이너 경계
- 혼동 경계: pointelle=lace 직물이 아니다; 성긴 knit가 전신 투명 의무를 만들지 않는다; 구멍만으로 소재 기원·기법을 인증하지 않는다
- 주장 한계: pointelle의 모든 상품 별칭과 제작 방식은 독립 재확인 필요. S24·S25는 니트 계열 범위 근거이며 해당 eyelet 후보는 작업 정의를 따른다.
- 부분 속성 제안: wardrobe.material.visible_weave, wardrobe.material.transmission
- 현 후보 이웃(표현 대조, 의미 보증 아님): lightweight_open_knit_layer_surface, sff_pro_y04
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Small ordered eyelets repeat between the cardigan's knitted stitches above a separate camisole.

관계: `cardigan eyelets` → `same cardigan's knit stitches above the camisole` (repeat_between, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S25: Rowan — General Information: Knitting With Colour](https://knitrowan.com/general-information)

## AFR080 — 청키와 파인게이지

- 원문 범위: 청키 니트 / 파인게이지 니트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 굵은 실·큰 코와 작은 코·매끈한 면이라는 가시 외형을 비교한다. 게이지 수치와 두께는 관련 있어도 동일 값은 아니다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 프레임에서 분해 가능한 편직코; 실 지름의 상대 외관; 같은 옷의 코 간격
- 혼동 경계: 얇아 보인다고 숫자 gauge를 확정하지 않는다; fine=캐시미어, chunky=울 성분으로 합치지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.material.visible_weave
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Large individual knit loops remain distinct along the same sweater's sleeve and cuff.

관계: `same sweater's large knit loops` → `sleeve and cuff surfaces` (remain_distinct, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary)

## AFR081 — 브러시드와 퍼지

- 원문 범위: 브러시드 니트 / 퍼지 니트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: brushed는 표면을 일으킨 가공, fuzzy는 보송한 외형의 묘사어다. 보풀 halo를 가시 속성으로 저장하고 가공 과정은 명세로 구분한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 의복 경계 밖 잔털; 표면 코 위의 낮은 보풀; 배경과 분리되는 섬유 윤곽
- 혼동 경계: 소프트포커스·낮은 해상도를 털결로 통과시키지 않는다; fuzzy=mohair가 아니다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Fine protruding fibers soften the outline of the same knit sleeve.

관계: `knit sleeve surface fibers` → `same sleeve's outer fabric boundary` (protrude_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S29: Mohair South Africa — The Fibre](https://www.mohair.co.za/natural-fibre)

## AFR082 — 멜란지·헤더와 말드

- 원문 범위: 멜란지 / 헤더 / 말드
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 미세 혼합색 표면과 두 색 실이 꼬여 보이는 외형을 구분한다. 원사 제조 과정과 혼합색 이미지 현상은 같은 증거가 아니다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 미세한 색점 또는 혼합 실; 선택된 두 색 나선 형태; 균일 조명 아래 의복 표면
- 혼동 경계: 노이즈·색수차·그림자를 실 혼합으로 판정하지 않는다; 원사 twist 방식은 근접·명세 근거가 필요하다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.color, wardrobe.material.visible_weave
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Two contrasting yarn colors spiral together within the sweater's visible marled stitches.

관계: `two yarn colors` → `same sweater's visible marled stitches` (spiral_together, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR083 — 인타르시아·자카드·페어아일

- 원문 범위: 인타르시아 / 자카드 / 페어아일
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: intarsia의 국소 색면과 Fair Isle의 반복 stranded 구성, jacquard의 조직 무늬를 구분한다. 전면 색무늬만으로 숨은 실 경로를 인증하지 않는다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 큰 색면 또는 작은 수평 반복 띠; 색 경계의 코; 선택한 직물의 조직 무늬
- 혼동 경계: 프린트=조직색 무늬가 아니다; Fair Isle 스타일과 실제 제작 기법은 다른 증거 층이다; Johnstons Intarsia 문구를 정의로 채택하지 않는다
- 주장 한계: 뒷면 float·기계·제작 이력은 별도 명세 또는 뒷면 자료로 검증한다.
- 부분 속성 제안: wardrobe.surface.jacquard_dobby, wardrobe.material.visible_weave
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct088_v1, clt_ct088_v2, layered_style_textile_surface, sff_pro_t09, sw_candidate_jacquard
- 현 프로필 이웃(표현 대조): clothing_ct088_v2, sw_jacquard

**독립 구현 1:** Small repeated color motifs form horizontal bands across the same sweater's knitted front.

관계: `knit color motifs` → `same sweater's front` (form_bands, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** A broad contrasting color block follows the actual stitch grid of the same pullover's front.

관계: `pullover color-block edge` → `same pullover's stitch grid` (follow, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S25: Rowan — General Information: Knitting With Colour](https://knitrowan.com/general-information), [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR084 — 체크·마름모·능직 문양

- 원문 범위: 아가일 / 타탄 / 글렌 체크 / 하운즈투스 / 헤링본 / 윈도페인 / 핀스트라이프
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: argyle은 다이아와 교차선, tartan은 다색 띠 교차, glen은 작은 격자의 큰 반복, houndstooth는 깨진 격자, herringbone은 사선 교대, windowpane은 큰 얇은 격자, pinstripe는 가는 반복선이다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 무늬의 최소 단위; 큰 반복과 가는 선; 실제 의복 표면의 방향
- 혼동 경계: 체크나 색 하나로 모든 종류를 동의어로 합치지 않는다; herringbone 인쇄와 능직 실 구조를 구분한다; 원산지·가문은 별도
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.check_patterns, wardrobe.surface.houndstooth_polka, wardrobe.pattern
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct084_v1, clt_ct084_v2, clt_ct094_v2, clt_ct095_v1, clt_ct095_v2, kilt_flat_apron_side_back_pleats, lowrider_paint_trim_hydraulic_and_upholstery_details, scottish_kilt_pleated_wrap_system, sff_pro_t06, sff_pro_x03, tartan_sett_twill_texture, tartan_wool_twill_sett_surface
- 현 프로필 이웃(표현 대조): clothing_ct084_v2, clothing_ct094_v2, clothing_ct095_v1

**독립 구현 1:** Alternating diagonal bands meet in repeated V-shaped herringbone lines across the coat.

관계: `coat diagonal pattern bands` → `same coat's repeated V-shaped pattern` (meet_in, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Fine diagonal lines cross the knitted diamond shapes on the same argyle vest.

관계: `fine argyle diagonal lines` → `same vest's knitted diamonds` (cross, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S32: Johnstons of Elgin — International Tweed Day](https://discover.johnstonsofelgin.com/our-story/international-tweed-day), [S26: CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

## AFR085 — 꽃·페이즐리·동물·위장

- 원문 범위: 다크 플로럴 / 페이즐리 / 레오퍼드 / 카무플라주
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: dark floral은 팔레트와 꽃무늬, paisley는 굽은 물방울 곡선, leopard는 반점 모티프, camouflage는 불규칙 색면이다. 실제 자연물과 프린트를 구분한다.
- 소유자: 같은 착용자의 선택된 의복 또는 두 명시된 의복에 결속한다.
- 관찰 단서: 의복 표면의 해당 반복 모티프; 바탕색과 무늬 경계; 같은 천의 주름에 따라 이어지는 패턴
- 혼동 경계: 실제 표범·꽃·군인·위장 성능을 추가하지 않는다; dark floral을 검정만으로 판정하지 않는다
- 주장 한계: 치수·숨은 구조·섬유 성분·제작 과정은 외관과 별도 명세 사실로 보존한다.
- 부분 속성 제안: wardrobe.surface.floral_paisley_animal, wardrobe.pattern
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct096_v1, clt_ct096_v2, military_field_uniform_system, y2kr_camouflage, y2kr_leopard_print
- 현 프로필 이웃(표현 대조): clothing_ct096_v1, military_uniform_duty_system, y2kr_camouflage, y2kr_leopard_print

**독립 구현 1:** Curved paisley motifs continue across the folds of the same printed blouse.

관계: `paisley print motifs` → `same blouse's fabric folds` (continue_across, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR086 — 소매의 연결선과 볼륨

- 원문 범위: 드롭숄더 / 래글런 소매 / 돌먼 / 배트윙 소매 / 퍼프 소매 / 비숍 소매 / 벨 소매
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: drop은 낮은 연결선, raglan은 목-암홀 사선, dolman/batwing은 큰 몸판-소매 연결, puff는 모인 둥근 볼륨, bishop는 긴 볼륨과 손목 수축, bell은 끝의 퍼짐이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 연결선 양 끝; 소매 최대 폭 위치; 커프스 또는 끝의 수축·퍼짐
- 혼동 경계: 어깨 선 위치와 맨살 노출은 다르다; bishop와 bell 끝모양을 합치지 않는다; 소매 볼륨을 착용자 팔 형태로 바꾸지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.structure.sleeve_attachment, wardrobe.silhouette.sleeve_flare, wardrobe.sleeves.bishop_bell_balloon
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct044_v1, clt_ct044_v2, clt_ct045_v1, clt_ct045_v2, clt_ct046_v2, clt_ct047_v1, clt_ct047_v2, fit_ff15_v2_candidate, oversized_design_ease_relation, sff_pro_c25, y2kr_oversize_tee
- 현 프로필 이웃(표현 대조): clothing_ct044_v2, clothing_ct045_v1, clothing_ct046_v2, clothing_ct047_v1, clothing_ct047_v2, fit_ff15_v2, y2kr_oversize_tee

**독립 구현 1:** The dropped sleeve seam sits below the same wearer's shoulder point while fabric covers the shoulder.

관계: `same shirt's sleeve seam` → `same wearer's covered shoulder point` (sit_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The full bishop sleeve gathers into a narrow cuff at the same wearer's wrist.

관계: `bishop-sleeve volume` → `same sleeve's narrow wrist cuff` (gather_into, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S23: Mood Sewciety — 9 Types of Sewing Darts](https://blog.moodfabrics.com/all-about-darts/)

## AFR087 — 소매 길이·트임·썸홀

- 원문 범위: 익스트라 롱 슬리브 / 슬릿 슬리브 / 썸홀
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: extra-long은 손 기준을 넘는 밑단, slit는 소매 개방, thumbhole은 실제 엄지가 통과하는 커프스 구멍이다. 손가락·의복 소유를 유지한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 손등과 커프스 끝; 트임의 위 끝과 아래 끝; 커프스를 통과한 엄지
- 혼동 경계: 구멍을 보고 엄지 위치를 임의 이동하지 않는다; 소매 트임과 깊은 암홀은 다른 부위다; 몸 일부가 프레임 밖이면 관찰 불가
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.length.sleeve, wardrobe.structure.cuff_edge
- 현 후보 이웃(표현 대조, 의미 보증 아님): thumbhole_cuff_hand_opening
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The same wearer's thumb passes through the cuff opening while the extended sleeve covers the back of the hand.

관계: `same wearer's thumb` → `same sleeve's cuff opening` (pass_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR088 — 칼라와 라펠

- 원문 범위: 피터팬 칼라 / 노치드 라펠 / 피크드 라펠 / 숄칼라
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: Peter Pan은 둥근 끝의 칼라, notch는 칼라-라펠 홈, peak는 위를 향한 끝, shawl은 꺾임 없는 곡선 계열이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 칼라 끝과 앞판; 라펠 모서리 방향; 홈 또는 연속 곡선
- 혼동 경계: 피터팬 캐릭터를 추가하지 않는다; 숄 액세서리와 shawl collar 연결 구조를 분리한다; 둘레 곡선만으로 소재를 추정하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.stand_peterpan_sailor, wardrobe.details.tailoring_front
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct041_v1
- 현 프로필 이웃(표현 대조): clothing_ct041_v1

**독립 구현 1:** A visible notch separates the jacket's collar edge from the upper end of its lapel.

관계: `same jacket's collar notch` → `collar edge and upper lapel end` (separate, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR089 — 프릴·프린지·레이스업

- 원문 범위: 프릴 / 러플 / 프린지 / 레이스업
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: ruffle은 모은 파도형 가장자리, fringe는 독립적으로 매달린 술, lace-up은 구멍·고리를 통과해 연결하는 끈이다. 장식과 여밈 역할은 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 붙은 가장자리와 물결; 술의 부착선·자유 끝; 대응 아일릿과 끈 교차 경로
- 혼동 경계: 레이스 천을 lace-up 끈으로 합치지 않는다; 끈이 장식이면 여밈 성능을 주장하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.ruffle_flounce, wardrobe.details.tassel_fringe_braid, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): akihabara_maid_cafe_uniform, chrh_hair_color_state_colored_bangs, chrh_hair_cut_blunt_bangs, chrh_hair_cut_bottleneck_bangs, chrh_hair_cut_full_bangs, chrh_hair_cut_micro_bangs, chrh_hair_cut_see_through_bangs, chrh_hair_cut_side_swept_bangs, chrh_hair_cut_supp_french_bob, chrh_hair_cut_wispy_bangs, chromatic_fringe_edges, clt_ct065_v1
- 현 프로필 이웃(표현 대조): ca_blunt_fringe, chrh_rel_hair_color_state_colored_bangs, chrh_rel_hair_cut_blunt_bangs, chrh_rel_hair_cut_full_bangs, chrh_rel_hair_cut_see_through_bangs, chrh_rel_hair_cut_side_swept_bangs, chrh_rel_hair_cut_supp_french_bob, chrh_rel_hair_cut_wispy_bangs, clothing_ct043_v1, clothing_ct065_v1, clothing_ct068_v2, egr_profile_brow_level_blunt_fringe

**독립 구현 1:** A cord alternates through paired eyelets on the two edges of the same bodice's front opening.

관계: `lace-up cord` → `paired eyelets on the same bodice edges` (alternate_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

## AFR090 — 마모와 로 에지

- 원문 범위: 디스트레스드 / 로 에지
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: distressed는 마모·찢김·색바램 외형, raw edge는 접어 마감하지 않은 절단 경계다. 손상 상태와 실제 발생 원인·사용 이력을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 의복 내부 찢김 경계; 끝에서 나온 실; 선택한 색바램 위치
- 혼동 경계: 올풀린 밑단을 폭력·가난·사고 증거로 쓰지 않는다; 인물 피부 상처와 의복 손상은 다른 운반체다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.wardrobe_trim
- 현 후보 이웃(표현 대조, 의미 보증 아님): basted_toile_balance_and_fit_lines
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** Loose yarn ends project from the cut edge of the same denim skirt's hem.

관계: `denim-skirt loose yarn ends` → `same skirt's cut hem edge` (project_from, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR091 — 스터드·체인·본디지풍 스트랩

- 원문 범위: 스터드 / 체인 디테일 / 본디지 스트랩
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: stud는 부착된 반복 금속 장식, chain은 연결 고리, bondage-inspired는 복식 스트랩 디자인 계보다. 각 부품의 부착·연결·자유 끝을 기록한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 의복에 고정된 작은 금속 부품; 체인의 연속 고리와 부착점; 스트랩의 양끝 고정
- 혼동 경계: 실제 결박·자유 제한·폭력·관계·동의를 옷에서 추정하지 않는다; 허공에 뜬 끈이나 신체를 관통한 장식은 실패다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.sequins_beads_studs, wardrobe.details.wardrobe_straps
- 현 후보 이웃(표현 대조, 의미 보증 아님): clt_ct069_v1, clt_ct069_v2, clt_ct108_v2, fit_ff44_v1_candidate, orn_gd24, orn_gd40, orn_gd57, simple_pearl_studs, small_studded_dailywear_accessory, y2kr_studs
- 현 프로필 이웃(표현 대조): button_down_collar_fastening, clothing_ct023_v2, clothing_ct108_v2, fit_ff44_v1, orn_profile_gd24, orn_profile_gd40, y2kr_studs

**독립 구현 1:** A detachable strap runs between two metal rings attached to the same trouser waistband.

관계: `fashion strap` → `two rings on the same trouser waistband` (connect, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR092 — 가을 색 이름과 소유자

- 원문 범위: 카멜 / 오트밀 / 에크루 / 아이보리 / 토프 / 그레이지 / 초콜릿 브라운 / 에스프레소 / 코냑 / 토바코 / 러스트 / 테라코타 / 번트 오렌지 / 머스터드 / 오커 / 버건디 / 옥스블러드 / 플럼 / 오버진 / 올리브 / 포레스트 그린 / 차콜 / 네이비
- 우선순위 / 유형: P2 / metadata
- 뜻과 축: 색명은 가변적인 색영역 접근어다. warm light tan·light mixed grey beige·deep red brown 같은 가시 색 설명을 함께 저장하고, 선택되면 코트·상의 등 운반체를 고정한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 명시된 의복의 밝기·색상·채도; 같은 조명에서 의복 간 대비; 비슷한 색명 사이 불확실 범위
- 혼동 경계: 색 이름을 무조건 동일 HEX로 만들지 않는다; camel을 섬유·동물, espresso를 음료, rust를 실제 부식으로 혼동하지 않는다; 가을=갈색 고정이 아니다
- 주장 한계: 색 코드는 사용자·제품 스와치가 제공한 경우에만 해당 문맥의 정확값으로 보존한다. 사진 화이트밸런스와 재료 반사 때문에 맥락 없는 절대색 인증은 피한다.
- 부분 속성 제안: wardrobe.color
- 현 후보 이웃(표현 대조, 의미 보증 아님): black_cherry_palette, business_blouse_pencil_skirt, casual_bomber_jacket_miniskirt, colored_mascara_accent, deconstructed_mummy_wrap_dress, deep_burgundy_wine_hair, e_waste_robot_graveyard, egr_charcoal_backdrop_dark_material, egr_palette_s301, egr_palette_s302, egr_palette_s307, egr_palette_s308
- 현 프로필 이웃(표현 대조): egr_profile_charcoal_backdrop_dark_material, fire_rel_f003, fire_rel_f051, fire_rel_f090, fire_rel_f110, hvr_profile_corrosion_used_touch_zone, hvr_profile_palette_mold_ward, pa_bands_same_carrier, pa_bounded_metal_trim, pa_dark_oxblood_bone_owners, pa_food_container_color_owners, pa_local_color_under_separate_lights

이 카드는 명세/용어 메타데이터다. 숨은 기원·수치·가격을 픽셀 프로필로 자동 승격하지 않는다.

출처: [S37: Ralph Lauren — Winter Style Notes: Tonal Dress](https://www.ralphlauren.com/rlmag/ralph-lauren-tone-on-tone.html), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR093 — 부츠의 높이 기준

- 원문 범위: 앵클부츠 / 니하이 부츠 / 오버니 부츠 / 싸이하이 부츠
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: ankle/knee/over-knee/thigh는 입구의 신체 기준점이다. 굽·재질·밀착과 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 부츠 입구와 발목·무릎·허벅지; 같은 다리에서 스커트 밑단; 사이에 남는 타이츠 또는 피부
- 혼동 경계: over-knee와 thigh-high는 중첩될 수 있다; 부츠+미니가 맨살 간격을 보장하지 않는다
- 주장 한계: shaft_height 경로는 새 부분 속성 제안이다. 현 계약 검토 없이 runtime 경로라고 단정하지 않는다.
- 부분 속성 제안: wardrobe.length.hem_landmark, wardrobe.footwear.shaft_height
- 현 후보 이웃(표현 대조, 의미 보증 아님): fishnet_thigh_high_boots, pointed_ankle_boots, street_jacket_boots, y2kr_knee_boots
- 현 프로필 이웃(표현 대조): y2kr_knee_boots

**독립 구현 1:** The boot shaft ends just below the same wearer's knee, beneath the skirt hem.

관계: `boot shaft upper edge` → `same wearer's knee beneath the skirt hem` (end_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S36: Dr. Martens — 2976 Virginia Chelsea Boots](https://www.drmartens.com/us/en/2976-virginia-leather-chelsea-boots-nero/p/30698001), [S35: Crockett and Jones — Style Guide](https://www.crockettandjones.com/pages/style-guide)

## AFR094 — 첼시·컴뱃·모토·라이딩·웨스턴·삭스

- 원문 범위: 첼시부츠 / 컴뱃부츠 / 바이커 / 모토 부츠 / 라이딩 부츠 / 웨스턴 / 카우보이 부츠 / 삭스부츠
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: Chelsea는 탄성 옆판, combat은 끈 여밈 계열, moto는 버클·스트랩, riding은 높은 간결한 shaft, western은 곡선 입구·스티치·굽·앞코, sock는 부드러운 밀착 upper의 제품 표현이다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 옆 탄성 패널 또는 실제 끈 경로; 선택된 버클·샤프트·앞코; 발과 신발의 경계
- 혼동 경계: 실제 군인·라이더·승마·카우보이 역할을 추가하지 않는다; 높은 검정 부츠만으로 이름들을 확정하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.footwear.backless_vs_strapped, wardrobe.footwear.shaft_height
- 현 후보 이웃(표현 대조, 의미 보증 아님): biker_short_thigh_knee_landmark, jianghu_frontier_inn_hall, mortality_agent_intervention, ri_five_buddha_families_readable_composition, western_cowboy_boots, western_death_personification_agent, western_frontier_outfit, western_frontier_station, western_frontier_world, y2kr_western_belt
- 현 프로필 이웃(표현 대조): cycling_bib_shorts_strap_pad_continuity, exercise_dress_integrated_short_liner, jianghu_inn_identity_standoff, korean_afterlife_guide_escort, western_death_personification, y2kr_western_belt

**독립 구현 1:** An elastic side gusset joins the Chelsea boot's front and rear upper panels.

관계: `Chelsea boot side gusset` → `same boot's front and rear upper panels` (join, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S36: Dr. Martens — 2976 Virginia Chelsea Boots](https://www.drmartens.com/us/en/2976-virginia-leather-chelsea-boots-nero/p/30698001), [S35: Crockett and Jones — Style Guide](https://www.crockettandjones.com/pages/style-guide), [S05: Schott NYC — 618 Perfecto](https://www.schottnyc.com/products/618-classic-perfecto-steerhide-leather-motorcycle-jacket)

## AFR095 — 로퍼·메리제인·발레 플랫·옥스퍼드/더비

- 원문 범위: 로퍼 / 메리제인 / 발레 플랫 / 옥스퍼드 / 더비
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: loafer는 끈 없는 구두 계열, Mary Jane은 발등 가로 스트랩, ballet flat은 낮은 발레 유래 외형, Oxford/Derby는 quarter-vamp 연결이 다르다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 발등 스트랩의 실제 부착; 구두 끈의 facings; vamp 위·아래로 연결된 구조
- 혼동 경계: 바닥 굽 높이만으로 끈 구조를 대체하지 않는다; Oxford 셔츠·대학과 신발을 분리한다; 별칭 Oxford/Derby를 synonym 한 쌍으로 합치지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.footwear.oxford_derby_brogue, wardrobe.footwear.backless_vs_strapped
- 현 후보 이웃(표현 대조, 의미 보증 아님): backless_loafers, ballet_flat_sneakers, block_heel_pumps, boat_deck_shoes, chunky_dad_sneakers, clt_ct083_v1, clt_ct083_v2, clt_ct122_v1, clt_ct122_v2, clt_ct123_v1, clt_ct123_v2, clt_ct124_v1
- 현 프로필 이웃(표현 대조): clothing_ct083_v2, clothing_ct122_v1, clothing_ct122_v2, clothing_ct123_v2, y2kr_ballet_flats

**독립 구현 1:** The Derby shoe's eyelet facings are stitched over the same shoe's vamp.

관계: `Derby eyelet facings` → `same shoe's vamp` (stitched_over, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The Mary Jane strap crosses the same wearer's instep and attaches to both sides of the shoe.

관계: `Mary Jane strap` → `same shoe's two sides across the instep` (cross_and_attach, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S35: Crockett and Jones — Style Guide](https://www.crockettandjones.com/pages/style-guide), [S10: Museum at FIT — Ballerina: Fashion's Modern Muse](https://exhibitions.fitnyc.edu/ballerina/)

## AFR096 — 굽과 밑창 축

- 원문 범위: 키튼힐 / 블록힐 / 플랫폼 / 러그솔
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: kitten은 비교적 낮고 가는 굽, block은 넓은 굽, platform은 앞 발바닥 아래 높이, lug는 깊은 요철 패턴이다. 전체 신발 종류와 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 뒤꿈치 굽 폭과 높이; 앞 밑창의 높이; 실제로 보이는 굵은 돌기
- 혼동 경계: 뒤 굽이 높다고 platform은 아니다; 밑창 바닥을 못 보면 lug 패턴은 미확인; 신발 명칭만으로 수치 cm를 고정하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.footwear.heel_platform_wedge
- 현 후보 이웃(표현 대조, 의미 보증 아님): active_rail_driver_cab, blank_lower_third_safe_area, block_heel_pumps, carousel_crop_safe_series_frame, center_safe_subject_frame, clt_ct130_v1, clt_ct130_v2, contemporary_heisei_y2k_layers, demoscene_world_restore_location, ed_bus_stop_ready_candidate, ed_subway_exit_candidate, ep_transit_boundary_waiting_orientation
- 현 프로필 이웃(표현 대조): clothing_ct130_v1, early_2000s_compact_digicam_social_repost, ed_subway_exit, fire_rel_f096, formal_biwu_reciprocal_salute_standoff, opening_rail_platform_departure, pf_gun_battery, rail_driver_operation, rail_platform_dispatch_operation, y2kr_platform_boots, y2kr_platform_flip, y2kr_platform_sandal

**독립 구현 1:** A raised platform supports the front of the shoe separately from its broad rear heel.

관계: `front platform sole` → `same shoe's forefoot separate from the rear heel` (support, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S35: Crockett and Jones — Style Guide](https://www.crockettandjones.com/pages/style-guide), [S36: Dr. Martens — 2976 Virginia Chelsea Boots](https://www.drmartens.com/us/en/2976-virginia-leather-chelsea-boots-nero/p/30698001)

## AFR097 — 타이츠·스타킹·삭스·워머

- 원문 범위: 타이츠 / 팬티호즈 / 스타킹 / 싸이하이 스타킹 / 홀드업 / 스테이업 / 니삭스 / 오버니 삭스 / 레그워머 / 암워머
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: tights/pantyhose는 허리부터 연결된 구조, stocking은 다리별 별도 구조, hold-up은 상단 자가 고정 계열, socks는 양말, warmers는 덧입는 관형이다. 국내 stocking의 넓은 용례와 구별한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 다리별 상단 밴드; 선택된 허리 연결; 워머의 위아래 두 자유 경계; 팔·다리 운반체
- 혼동 경계: 상의가 허리를 가리면 tights/stocking 차이는 명세로 남는다; 발 포함 여부와 투과성은 별도; 실리콘 고정력은 사진으로 인증하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.accessories.sock_stocking_tights, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): capri_legging_mid_calf_landmark, clt_ct025_v1, clt_ct107_v1, clt_ct107_v2, fishnet_thigh_high_boots, pfe_garter_path_candidate, pfe_hosiery_backline_candidate, pfe_hosiery_opaque_candidate, pfe_hosiery_sheen_candidate, pfe_hosiery_sheer_candidate, pfe_lace_welt_candidate, pfe_plain_welt_candidate
- 현 프로필 이웃(표현 대조): clothing_ct025_v1, clothing_ct107_v1, clothing_ct107_v2, pfe_garter_path, pfe_hosiery_backline, pfe_hosiery_opaque, pfe_hosiery_sheen, pfe_hosiery_sheer, pfe_thigh_skin_band, stirrup_leggings_underfoot_loop, sw_leggings, y2kr_legwarmers

**독립 구현 1:** The leg warmer forms a separate knitted tube around the ankle above the same wearer's shoe.

관계: `separate leg-warmer tube` → `same wearer's ankle above the shoe` (surround, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S33: FALKE — Tights Styling](https://www.falke.com/us_en/journal/tights-styling/), [S34: Wolford — Our Tights Guide](https://www.wolford.com/en-ca/our-tights-guide.html)

## AFR098 — 호저리의 투과·광택·무늬

- 원문 범위: 시어 타이츠 / 오페이크 타이츠 / 매트 타이츠 / 글로시 타이츠 / 피시넷 / 레이스 타이츠 / 백심
- 우선순위 / 유형: P0 / variant_family
- 뜻과 축: sheer/opaque, matte/gloss, fishnet/lace/back-seam은 별도 축이다. 연속 원단층의 가시 피부, 표면 반사, 열린 망눈, 장식선으로 각각 구현한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 다리 위 별도 원단층; 망눈 또는 무늬; 피부가 비치는 범위; 뒤쪽 세로선
- 혼동 경계: 백심은 실제 seam 또는 seam-look 변형이 있다; matte=opaque가 아니다; fishnet 마름모를 argyle 색무늬와 합치지 않는다; DEN을 투명도 값으로 쓰지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.accessories.sock_stocking_tights, wardrobe.material.transmission
- 현 후보 이웃(표현 대조, 의미 보증 아님): fishnet_thigh_high_boots, pfe_hosiery_backline_candidate, pfe_hosiery_opaque_candidate, pfe_hosiery_sheer_candidate, sff_extra_xa047, sff_extra_xa048
- 현 프로필 이웃(표현 대조): pfe_hosiery_backline, pfe_hosiery_opaque, pfe_hosiery_sheer

**독립 구현 1:** The sheer tights remain a continuous dark layer while the same leg's skin tone shows through.

관계: `sheer-tights fabric` → `same wearer's leg skin tone` (overlay_transparently, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** Diamond-shaped fishnet openings repeat over the same wearer's legs.

관계: `fishnet mesh openings` → `same wearer's legs` (repeat_over, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S33: FALKE — Tights Styling](https://www.falke.com/us_en/journal/tights-styling/), [S34: Wolford — Our Tights Guide](https://www.wolford.com/en-ca/our-tights-guide.html), [S27: CottonWorks — Denier](https://cottonworks.com/encyclopedia-item/denier/)

## AFR099 — 가터벨트의 연결

- 원문 범위: 가터벨트
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: 허리·골반 지지대에서 내려오는 끈이 같은 stocking 상단 band에 붙는 구조다. 몸통 하네스와 다른 끝점을 가진다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 허리 지지대; 아래로 이어진 연속 스트랩; 같은 스타킹 상단에 연결된 클립
- 혼동 경계: 끈만 보이고 stocking 끝점이 없으면 연결 PASS가 아니다; hold-up self-support와 별도; 벨트·끈·타이츠를 한 원단으로 합치지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.garter_suspender
- 현 후보 이웃(표현 대조, 의미 보증 아님): pfe_garter_path_candidate
- 현 프로필 이웃(표현 대조): pfe_garter_path

**독립 구현 1:** A garter strap descends from the waist belt and clips onto the upper band of the same stocking.

관계: `garter-belt strap` → `waist belt and same stocking's upper band` (connect, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR100 — 베레모·뉴스보이·비니

- 원문 범위: 베레모 / 뉴스보이 캡 / 비니
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: beret은 납작한 둥근 crown, newsboy는 작은 챙과 다분할 부풀음, beanie는 머리에 붙는 니트 cap이다. 소재·로고·머리카락과 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 납작한 crown 또는 봉제 구획; 챙의 존재; 니트 코와 머리의 접촉
- 혼동 경계: beret=프랑스 배경·국적이 아니다; 둥근 모자를 모두 뉴스보이로 합치지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.accessories.headwear
- 현 후보 이웃(표현 대조, 의미 보증 아님): beanie, beret
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The newsboy cap's segmented crown bulges above its short curved brim.

관계: `newsboy-cap crown` → `same cap's short curved brim` (bulge_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/)

## AFR101 — 스카프·머플러·스톨

- 원문 범위: 스카프 / 머플러 / 스톨
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: scarf와 국내 muffler는 폭·보온성 용례가 겹치며 stole은 어깨를 감쌀 넓고 긴 천의 표현이다. 현재 놓인 경로를 의복 종류와 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 목 또는 어깨를 둘러싼 천 경로; 동일 천의 자유 끝; 겉옷 위·아래 층
- 혼동 경계: shawl collar와 독립 액세서리는 다른 연결; 스톨에 fur 소재·formal 행사를 자동 추가하지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.accessories.neck_wear_position, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): andean_poncho_panel_system, bandana_scarf_neck, clear_jelly_bag_charm_system, clt_ct104_v1, clt_ct104_v2, ctx_borrowed_scarf_return, ctx_scarf_offer_refusal, handknit_scarf_prop, mexican_rebozo_shawl_wrap_system, narrow_lace_scarf_openwork_strip, neutral_base_single_lemon_accent, rebozo_long_shawl_route_and_fringe
- 현 프로필 이웃(표현 대조): clothing_ct104_v2, uniform_neck_scarf_separate_hair_ornament, wrap_front_overlap_closure, wrap_skirt_overlap_closure, y2kr_bandana, y2kr_headscarf, y2kr_scarf_belt, y2kr_scarf_top, y2kr_skinny_scarf

**독립 구현 1:** The wide stole crosses the shoulders over the coat and hangs in two separate ends.

관계: `same stole` → `shoulders over the coat and two free ends` (cross_and_hang, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR102 — 벨트·코르셋 벨트·체인·하네스

- 원문 범위: 와이드 벨트 / 코르셋 벨트 / 체인 벨트 / 패션 하네스
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: wide는 폭, corset belt는 넓은 몸판·레이스업의 허리 장식, chain belt는 금속 고리 경로, harness는 몸통·어깨 스트랩 그래프다. 실제 보강·역할은 별도다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 같은 옷 위 벨트 경로; 버클 또는 고리 연결; 하네스의 스트랩 교차와 몸통 끝점
- 혼동 경계: belt를 body corset으로 합치지 않는다; 하네스가 안전 장비·실제 결박을 뜻하지 않는다; 피부를 관통하는 스트랩은 실패다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.wardrobe_straps, wardrobe.details.hardware, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): natural_hourglass_relation, y2kr_chain_belt, y2kr_wide_belt
- 현 프로필 이웃(표현 대조): y2kr_chain_belt, y2kr_wide_belt

**독립 구현 1:** The fashion harness straps cross over the shirt and join the same waist strap at two side rings.

관계: `fashion-harness upper straps` → `same harness's waist strap at two side rings` (join, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S09: V&A — Vivienne Westwood: punk, new romantic and beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

## AFR103 — 초커·핑거리스·리본

- 원문 범위: 초커 / 핑거리스 글러브 / 리본 타이
- 우선순위 / 유형: P1 / variant_family
- 뜻과 축: choker는 목 가까운 짧은 목걸이, fingerless는 손가락 끝의 열린 장갑, ribbon tie는 선택된 위치에 묶은 끈이다. 형태와 의미 역할을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 목 둘레의 별도 장신구; 장갑 경계에서 나온 손가락 끝; 리본의 부착 또는 매듭 위치
- 혼동 경계: 목 장신구를 collar 또는 결박으로 합치지 않는다; 장갑이 손 피부에 녹아들면 실패다; 리본은 목·머리·옷 중 소유자를 지정한다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.accessories.glove_mitten, wardrobe.accessories.neck_wear_position
- 현 후보 이웃(표현 대조, 의미 보증 아님): adjusting_choker_gloves, choker_gloves_high_heels, clt_ct106_v1, ctx_c019, royal_crest_choker, ruby_cameo_choker_prop, sff_extra_xa040, vel_open_ring_choker_mount, y2kr_ribbon_tie, y2kr_stone_choker, y2kr_tattoo_choker
- 현 프로필 이웃(표현 대조): clothing_ct106_v1, vel_open_ring_choker_mount_profile, y2kr_ribbon_tie, y2kr_stone_choker, y2kr_tattoo_choker

**독립 구현 1:** The fingerless glove ends below the same wearer's exposed fingertips.

관계: `fingerless-glove finger edges` → `same wearer's fingertips` (end_below, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S22: Mood Sewciety — Ultimate List of Sewing Terms](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR104 — 레이어·질감·기장·볼륨 대비

- 원문 범위: 레이어링 / 텍스처 믹스 / 길이 대비 / 볼륨 대비
- 우선순위 / 유형: P0 / relation_family
- 뜻과 축: layering은 둘 이상의 별도 의복 순서, texture mix는 서로 다른 운반체 표면, length/volume contrast는 명시된 두 의복의 상대 관계다. 선택된 대비만 활성화한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 두 의복의 독립 경계; 목선·소매·밑단에서 드러난 이너; 서로 다른 표면; 같은 프레임의 길이·폭
- 혼동 경계: 긴 코트가 이너를 완전히 가리면 대비는 관찰 불가다; 상의 부피를 몸 크기로 바꾸지 않는다; 배경·빛·렌즈까지 같은 스타일로 묶지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.material, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): adult_decora_maker_wearer, advanced_clever_layering, architectural_peplum, arms_crossed_stance, asymmetrical_flatlay_layering, asymmetrical_hemline, back_to_waist_curve, balloon_convex_leg_tapered_hem_silhouette, bermuda_two_knee_length_short_hems, biker_short_thigh_knee_landmark, black_leather_harness_style, bm_abdominal_projection
- 현 프로필 이웃(표현 대조): adult_everyday_controlled_reveal_moment, pfe_volume_contrast, west_african_grand_boubou_volume_system, y2kr_long_short_layer, y2kr_tiny_big, y2kr_visible_layers

**독립 구현 1:** The long coat's open front reveals the same wearer's shorter skirt hem above the knees.

관계: `long coat's open front` → `same wearer's shorter skirt hem` (reveal, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

**독립 구현 2:** The broad blazer panels stand away from the fitted knit top worn beneath them.

관계: `broad blazer panels` → `same wearer's fitted inner knit` (stand_away, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html), [S37: Ralph Lauren — Winter Style Notes: Tonal Dress](https://www.ralphlauren.com/rlmag/ralph-lauren-tone-on-tone.html)

## AFR105 — 토널과 모노크롬

- 원문 범위: 토널 드레싱 / 모노크롬
- 우선순위 / 유형: P1 / relation_family
- 뜻과 축: tonal은 같은 색계의 밝기·재질 변화, monochrome은 단일 색 중심이라는 넓은 표현이다. black-and-white photographic monochrome과 의복 palette를 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 같은 조명에서 의복별 색 관계; 밝기·표면 차이; 명시된 두 의복
- 혼동 경계: 토널이라는 말로 사진 전체를 흑백 처리하지 않는다; 톤 차이가 곧 다른 hue라는 뜻은 아니다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.color, wardrobe.material
- 현 후보 이웃(표현 대조, 의미 보증 아님): lit_noir_monochrome_or_restrained_palette, monochrome_diffused_lid_wash, muted_monochrome_cheek_wash, pe_daguerreotype_plate, pe_platinum_print_paper, pe_wet_plate_artifact
- 현 프로필 이웃(표현 대조): autochrome_glass_transparency_color_screen

**독립 구현 1:** The camel coat and darker brown knit keep related hues while their distinct surfaces remain visible.

관계: `same wearer's camel coat` → `darker brown knit underlayer` (share_hue_family, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S37: Ralph Lauren — Winter Style Notes: Tonal Dress](https://www.ralphlauren.com/rlmag/ralph-lauren-tone-on-tone.html)

## AFR106 — 벨티드와 프런트 턱

- 원문 범위: 벨티드 스타일링 / 프런트 턱 / 프렌치 턱
- 우선순위 / 유형: P0 / relation_family
- 뜻과 축: belted는 겉옷 위 벨트의 허리 경로, front tuck는 상의 앞부분만 허리밴드 안으로 들어가는 현재 착용 상태다. 의복 패턴과 원산지가 아니다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 벨트가 누르는 같은 코트 직물; 앞상의-허리밴드 포함; 옆·뒤의 자유 밑단
- 혼동 경계: 셔츠 전체 턱인과 부분 tuck을 합치지 않는다; 국적·스타일 성격을 추가하지 않는다; 겉벨트와 바지 내부 벨트는 다른 레이어다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.details.top_layer_relation
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The shirt's front hem enters the trouser waistband while its side and back hems hang outside.

관계: `same shirt's front hem` → `trouser waistband with free side and back hems` (enter_partially, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S39: MasterClass — How to Pull Off the Perfect French Tuck](https://www.masterclass.com/articles/how-to-pull-off-the-perfect-french-tuck), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR107 — 원버튼 카디건의 현재 상태

- 원문 범위: 원버튼 카디건 스타일링
- 우선순위 / 유형: P0 / visible_state
- 뜻과 축: 단추 하나를 고른 잠김 상태다. 잠긴 지점 위·아래의 열림 방향, 이너·피부를 별도 관계로 작성하며 새 카디건 종류로 만들지 않는다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 잠긴 한 단추와 맞물린 두 앞판; 그 아래 벌어진 경계; 사이의 명시된 이너 또는 피부
- 혼동 경계: one-button 구조 제품과 현재 하나 잠김을 합치지 않는다; 열림=배꼽·가슴 노출이 아니다; 단추 하나가 프레임 밖이면 미확인
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.cardigan_opening, wardrobe.structure.front_fastener
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** One fastened cardigan button joins the front edges; below it, the edges diverge over a separate camisole.

관계: `same cardigan's one fastened button and front edges` → `lower opening over the separate camisole` (join_then_diverge, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S24: Johnstons of Elgin — Knitwear and Cashmere Glossary](https://johnstonsofelgin.com/pages/glossary), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR108 — 시어 레이어링의 투과 대상

- 원문 범위: 시어 레이어링
- 우선순위 / 유형: P0 / relation_family
- 뜻과 축: 앞의 비치는 원단과 뒤의 선택된 이너·피부의 두 운반체를 결속한다. 투과 대상·범위가 명시되어야 한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 앞 원단의 망과 주름; 뒤 이너의 선명한 경계; 겹친 곳의 중첩 변화
- 혼동 경계: sheer라는 단어만으로 피부 노출을 추가하지 않는다; ethereal이라는 분위기는 실제 두 층 관계를 대신하지 못한다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.material.transmission, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): ethereal_sheer_layering
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The sheer blouse's fine mesh lies in front of the separate camisole, whose neckline remains readable through it.

관계: `sheer blouse mesh` → `same wearer's separate camisole neckline` (overlay, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S33: FALKE — Tights Styling](https://www.falke.com/us_en/journal/tights-styling/), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR109 — 란제리를 보이는 의복으로 착용

- 원문 범위: 란제리 애즈 아우터웨어
- 우선순위 / 유형: P1 / relation_family
- 뜻과 축: 속옷 유래 형태를 외부에서 보이는 의복 요소로 사용하는 선택된 층 관계다. lingerie dressing 스타일군과 해당 실제 착용 상태를 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 겉재킷과 별도 bralette/cami; 눈에 읽히는 이너 경계; 주체의 같은 몸통 소유
- 혼동 경계: 이너를 잘라 노출을 늘리는 변형과 동등하지 않다; 속옷 유래=실제 속옷만 착용한 상태가 아니다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.details.corset_bustier
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The open blazer exposes the complete upper edge of a separate lace camisole worn as a visible layer.

관계: `same wearer's open blazer` → `separate visible lace camisole upper edge` (reveal, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR110 — 하의실종과 노팬츠 룩

- 원문 범위: 하의실종 스타일링 / 노팬츠 룩
- 우선순위 / 유형: P0 / visible_state
- 뜻과 축: 하의실종은 긴 상의가 짧은 하의를 가리는 가시 연출, no-pants look는 전통 팬츠 대신 짧은 하의 등을 보이는 패션 이름이다. 하의 존재·종류·가림을 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 긴 상의 밑단; 선택된 짧은 하의의 경계 또는 명세; 타이츠·다리·부츠 층
- 혼동 경계: 짧은 하의가 안 보여도 없음으로 판정하지 않는다; 두 유행어를 완전 동의어로 합치지 않는다; 누락된 의복을 임의 삭제하지 않는다
- 주장 한계: 이 후보는 숨은 쇼츠의 관찰 가능한 연구 변형이다. 완전 가려진 원 요청을 이 변형으로 강제 바꾸면 안 된다;완전 가림은 존재 명세와 이미지 관찰 불가를 분리한다.
- 부분 속성 제안: wardrobe.details.layer_order, wardrobe.length.hem_landmark
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The long sweater hem covers most of the separate shorts while a short edge of their fabric remains visible below it.

관계: `long sweater hem` → `same wearer's separate shorts with a visible lower edge` (cover_most, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html), [S16: Metropolitan Museum of Art — Infra-Apparel](https://resources.metmuseum.org/resources/metpublications/pdf/Infra_Apparel.pdf)

## AFR111 — 피카부의 대상 관계

- 원문 범위: 피카부 디테일
- 우선순위 / 유형: P1 / relation_family
- 뜻과 축: 개구부·겹침의 벌어짐을 통해 다른 층이 일부 보이는 표현이다. 무엇이 보이는지와 어떤 옷의 틈인지 정한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 개구부 둘레; 그 안의 다른 피부·이너·레이스; 전후 레이어
- 혼동 경계: cut-out·sheer·unbuttoned를 자동 동의어로 합치지 않는다; 보이는 대상을 지정하지 않은 감성어만으로 PASS를 주지 않는다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.coverage.opening_location, wardrobe.details.layer_order
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** A small lace underlayer is visible through the bounded opening in the same blouse's upper front.

관계: `separate lace underlayer` → `same blouse's bounded upper-front opening` (visible_through, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S17: Sherri Hill — Neckline Types](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [S38: Ralph Lauren — Layer Up](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html)

## AFR112 — 데콜테와 클리비지의 본문 보충

- 원문 범위: 데콜테 / 클리비지
- 우선순위 / 유형: P1 / supplemental_visible_state
- 뜻과 축: décolletage는 낮은 의복 윗경계 및 거기서 보이는 어깨·윗가슴 영역의 용례, cleavage는 양 가슴 사이 보이는 좁은 공간이라는 별도 뜻이다. 다른 분열·세포분열 의미를 분리한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 상의 윗경계; 쇄골·윗가슴 영역; 명시된 경우 중앙 좁은 공간
- 혼동 경계: 쇄골 가시성을 cleavage로 합치지 않는다; 깊은 목선이라도 이너·직물이 가릴 수 있다
- 주장 한계: 명칭만으로 성분·성능·신분·현재 가시 상태를 확정하지 않는다.
- 부분 속성 제안: wardrobe.coverage.opening_location
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

**독립 구현 1:** The adult wearer's collarbones and upper chest remain visible above the blouse's broad neckline.

관계: `adult wearer's collarbones and upper chest` → `same blouse's broad neckline` (visible_above, 유형명은 초안).
필수 검토: 선택된 구현의 같은 소유자·두 끝점·정확 관계·실제로 주장한 가시 단서를 확인한다. 형제 변형의 단서를 all-of로 추가하지 않는다. 보이지 않거나 일부만 맞으면 활성 의무를 통과시키지 않는다.

출처: [S40: Cambridge Dictionary — Décolletage](https://dictionary.cambridge.org/us/dictionary/english/decolletage), [S41: Cambridge Dictionary — Cleavage](https://dictionary.cambridge.org/us/dictionary/english/cleavage)

## AFR113 — 데니어의 본문 보충

- 원문 범위: 데니어 / DEN
- 우선순위 / 유형: P0 / supplemental_metadata
- 뜻과 축: DEN은 9,000m당 질량의 선밀도이며 투명도·GSM·빛 투과율이 아니다. 브랜드의 opaque 경계는 제품군과 색·구조·신장 조건의 설명으로 기록한다.
- 소유자: 같은 착용자의 명시된 의복·부위·레이어 또는 명시된 의복 쌍에 결속한다.
- 관찰 단서: 별도 시어/불투명 패널 속성; 실제 입은 타이츠 층; 피부 투과 관찰
- 혼동 경계: 40DEN=특정 투명도 보편 규칙으로 만들지 않는다; 실 굵기값과 의복 기장·광택을 합치지 않는다
- 주장 한계: 정확 DEN은 명세로 보존한다. 같은 값의 제품도 외관이 다를 수 있어 이미지로 선밀도 수치를 인증하지 않는다.
- 부분 속성 제안: wardrobe.material.transmission
- 현 후보 이웃(표현 대조, 의미 보증 아님): 해당 씨앗 표현의 이웃 없음
- 현 프로필 이웃(표현 대조): 해당 씨앗 표현의 이웃 없음

이 카드는 명세/용어 메타데이터다. 숨은 기원·수치·가격을 픽셀 프로필로 자동 승격하지 않는다.

출처: [S27: CottonWorks — Denier](https://cottonworks.com/encyclopedia-item/denier/), [S33: FALKE — Tights Styling](https://www.falke.com/us_en/journal/tights-styling/), [S34: Wolford — Our Tights Guide](https://www.wolford.com/en-ca/our-tights-guide.html)


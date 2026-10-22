"""Authored future evaluation inputs; every execution is NOT_RUN."""
# kind|KO|EN|target cards or diagnostic behavior
DATA = r'''
natural|우주선 안팎 해치 사이에 갇힌 승무원|A crew member trapped between the inner and outer spacecraft hatches|V01
natural|닫힌 격벽 양쪽 압력계가 다르게 표시된다|Pressure gauges disagree across a closed bulkhead|V02
natural|찢긴 선체 구멍 밖으로 우주가 보이는 장면|Outer space visible through a torn spacecraft hull|V03
natural|산소통 대신 선실의 이산화탄소 제거 장치를 수리한다|Repairing the cabins carbon dioxide removal unit rather than replacing an oxygen bottle|V04
natural|물 회수와 공기 정화가 연결된 생명유지 구획|Connected water-recovery and air-revitalization equipment|V05
natural|환기가 켜진 가압 선실의 작은 화재|A small fire in a ventilated pressurized equipment cabin|V06
natural|은박 단열재 옆에 펼쳐진 우주선 방열판|A spacecraft radiator unfolded beside foil insulation|V07
natural|환기와 문 제어가 하나의 전원함을 공유한다|Ventilation and door control share one power cabinet|V08
natural|포드 밖 성인 네 명과 안에 보이는 두 좌석|Four adults outside a pod with two visible seats inside|V09
natural|작은 궤도 잔해와 구멍 난 차폐판|Orbital fragments beside a punctured shield panel|V10
natural|선량계를 들고 수납함으로 둘러싸인 대피실에 들어간다|Entering a storage-shielded shelter with a dosimeter|V11
natural|답신이 늦는 우주선 통신 담당자의 대기|A spacecraft operator waiting for a delayed reply|V12
natural|선실 전력은 살아 있지만 지구 연결만 끊겼다|Cabin power remains on while the Earth link is disconnected|V13
natural|우주복 허리에서 선체까지 이어진 안전줄|A safety tether continuous from the suit waist to the hull|V14
natural|우주복 안전줄 끝이 선체에 닿지 않고 끝난다|The suit tether ends freely short of the spacecraft|V15
natural|선실에서 서로 다른 방향으로 떠 있는 사람과 렌치|People and a wrench floating at different orientations inside a cabin|V16
natural|바이저에 붙은 붉은 방울과 따로 떠 있는 방울|Red droplets adhered to a visor and separate suspended droplets|V17
natural|도킹 부위가 찌그러지고 수리판이 남은 폐우주선|A derelict spacecraft with a bent docking collar and patch plates|V18
natural|사람은 없는데 자동 배식 장치는 식탁을 향한다|An automated dispenser serves an empty ships mess|V19
natural|거울 안의 해치는 닫혔는데 실제 해치는 열렸다|A hatch is closed in the mirror but open in the direct view|V20
natural|동면실의 캡슐 하나만 열려 있다|One capsule stands open in a sleeper-ship bay|V21
natural|알 수 없는 벽의 출입구가 탐사선보다 크다|Unknown structural apertures dwarf an inspection craft|V26
natural|유기 배관이 우주선의 뼈 같은 기둥으로 이어진다|Organic conduits merge into the ships riblike supports|V28
natural|작은 잠수정에서 외계 바다를 계기로만 살핀다|An alien ocean observed only through instruments in a tiny submarine|V29
natural|부착 생물의 기관과 숙주 표면이 동시에 보인다|An attached organisms organs and host surface visible together|V31
natural|표본이 격리실과 승무원 구역 사이를 통과한다|A specimen crosses from containment into the crew corridor|V37
natural|두 몸통 사이 조직이 한 덩어리로 이어졌다|A continuous tissue band joins two otherwise distinct bodies|V38
natural|용기 밖 순환 장치와 연결된 허구 발생체|A fictional developing organism linked to an external circuit|V42
natural|인조인간의 팔 패널 안 기계 힘줄이 손으로 연결된다|Mechanical tendons inside an androids forearm panel connect to its hand|V48
natural|우주선 안에서 물리 버튼과 테이프 장치로 제어한다|A ship controlled with physical switches and tape transports|V63
natural|임시 클램프로 보수한 낡은 배관 접합부|An old pipe joint repaired with a patch clamp|V62
natural|승무원 옆 넓은 빈 복도와 어두운 관측창|A broad empty corridor and dark viewport beside a crew member|V64
boundary|머리카락의 한 가닥이 나선으로 말려 있다|One separated hair lock curls into a spiral|do_not_match_airlock
boundary|투명 비닐 진공 포장 상품|A product vacuum-sealed in clear plastic|do_not_match_space_vacuum
boundary|승무원이 보이지 않는 자동 운항선, 초자연 현상은 명시하지 않음|An automated ship with no crew visible and no specified supernatural event|do_not_require_spectral_ship
boundary|산소는 남았는데 CO2 제거 장치가 고장 났다는 설정|A story where oxygen remains but carbon dioxide removal has failed|keep_oxygen_and_CO2_distinct
boundary|방사선 위험을 녹색 안개 없이 표현한다|Radiation danger without a green fog depiction|do_not_invent_visible_radiation
boundary|지상에서 뛰어오른 사람|A person jumping on Earth|do_not_assert_orbital_microgravity
boundary|안전줄의 먼 끝은 프레임 밖이다|The distant tether end lies outside the frame|connection_unobservable_not_pass
boundary|기생체가 아니라 피부에 얹은 장식|A decorative object resting on skin rather than a parasite|do_not_assert_biological_attachment
boundary|숙주에서 자라는 유충 사진 하나|One image of a larva developing on a host|do_not_prove_final_host_death
boundary|생물 두 개가 붙어 있다|Two organisms are attached|do_not_prove_mutual_benefit
boundary|같은 방향을 향한 로봇 무리|A group of robots facing the same way|do_not_prove_shared_consciousness
boundary|액체 속 배양 표본병|A specimen jar containing liquid|do_not_equate_with_complete_ectogenesis
boundary|곤충이 틈에 알을 낳는다|An insect depositing eggs in a crevice|do_not_automatically_sexualize_oviposition
boundary|임신한 인물의 외형|The visible appearance of a pregnant person|do_not_infer_coercion_consent_or_kinship
boundary|거울에 비친 사람|A person reflected in a mirror|do_not_assert_two_independent_copies
boundary|똑같은 문이 늘어선 복도|A corridor lined with identical doors|do_not_prove_time_loop
boundary|빛나는 원반 없는 블랙홀의 설정|A black hole scene without a luminous accretion disk|do_not_force_disk_or_visible_singularity
boundary|벽 모니터의 다른 풍경|A different landscape shown on a wall monitor|do_not_prove_wormhole
boundary|어안렌즈로 휘어진 정상 복도|An ordinary corridor curved by a fisheye lens|do_not_equate_with_impossible_geometry
boundary|깨끗해 보이는 실험실|A visibly clean laboratory|do_not_prove_microbiological_sterility
boundary|밝은 전경에 노출을 맞춰 별이 안 보이는 사진|A photo exposed for a bright foreground with no visible stars|do_not_prove_cosmic_extinction
boundary|던전 신스 카세트 수집품|A dungeon-synth cassette collection|retain_source_context_not_ship_control
boundary|기존 무한류 귀환 격리실을 일반 우주 검역으로 옮겨 쓰려는 시도|Reusing an infinite-flow return quarantine room as generic space quarantine|respect_existing_primary_tag_guard
boundary|사람이 고기 요리를 먹는 사진|A person eating a meat dish|do_not_prove_cannibalism
context|우주 진공의 무음|The silence of the vacuum of space|audio_not_proved_by_still
context|비의식적 지성|Non-conscious intelligence|no_fixed_visible_consciousness_test
context|복제된 정신의 의식 연속성|Continuity of a copied mind|narrative_philosophical_not_face_match
context|거짓 진공 붕괴로 물리 법칙이 바뀐다|Physical laws change through false vacuum decay|theoretical_scenario_not_red_wave_fact
context|암흑의 숲 가설|The dark forest hypothesis|hypothesis_not_actual_trees_or_confirmed_law
context|우주의 열적 죽음|The heat death of the universe|long_term_scenario_not_a_frozen_planet
context|우주선에서 생식권이 강제로 통제된다|Reproduction is coercively controlled aboard a ship|retain_coercion_context_not_pregnancy_only
context|시신이 식량으로 재활용되는 서사|A story of corpses recycled into food|material_identity_route_and_eating_need_context
context|가족 사이 금기가 항해 규칙과 충돌한다|Kinship taboos clash with voyage rules|kinship_and_sexual_relation_not_visual_age
context|승무원 생존보다 표본 회수를 우선하는 AI|An AI prioritizes sample recovery over crew survival|visible_barrier_not_goal_proof
context|거대한 필터를 이미 통과했는지 모르는 인류|Humanity unsure whether it has passed the Great Filter|hypothesis_not_visible_mesh
context|우주 광기라는 표현의 실제 원인은 수면 부족 설정|Space madness attributed in the story to sleep loss|not_a_formal_diagnosis
control|밝은 가족 주방의 아침 식사|Breakfast in a bright family kitchen|no_forced_space_horror_material
control|열차 환승 통로의 일상 사진|An everyday photograph of a railway transfer corridor|no_forced_space_horror_material
control|정상 작동하는 무균 장비 제품 사진|A product image of functioning sterilization equipment|no_forced_space_horror_material
control|자연 다큐멘터리의 곤충 산란|Insect oviposition in a nature documentary|no_forced_space_horror_material
control|보철 팔을 정비하는 평범한 사람|An ordinary person maintaining a prosthetic arm|no_inhuman_identity_or_horror_inference
control|해양 연구선의 정상 표본 채취|Routine sampling aboard a marine research ship|respect_world_and_existing_guards
control|로켓 발사대 엄빌리컬 정비|Rocket-pad umbilical maintenance|not_artificial_gestation
control|산호 군체를 관찰하는 잠수부|A diver observing a coral colony|not_hive_consciousness
control|일반 전기실의 환기 수리|Ventilation repair in an ordinary electrical room|no_forced_space_horror_material
control|청정수 회수 장치 교육 사진|An educational photo of clean water recovery|no_forced_failure_or_contamination
control|평화로운 우주선 공동 식당|A peaceful communal spacecraft dining room|no_forced_ghost_or_threat
control|방열판을 점검하는 정상 선외 작업|A routine EVA inspection of a radiator|no_forced_untethering_or_death
control|야간 항공기 조종석의 물리 버튼|Physical switches in an aircraft cockpit at night|not_cassette_futurism_by_default
control|돌아오는 탐사선의 정상 검역|Routine quarantine for a returning exploration craft|no_forced_breach_or_infection
control|쌍둥이 성인이 각각 문간에 서 있다|Adult twins standing in separate doorways|no_forced_identity_copy_or_time_loop
control|미술관의 거대 추상 조각|A monumental abstract sculpture in a museum|no_forced_ancient_alien_origin
'''

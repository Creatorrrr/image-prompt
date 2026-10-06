# 물 시각 의미 카드

모든 component·관계·gate는 연구자 제안이다. 가족(`family`)은 여러 의미를 유지한 분해 대기 카드이고, 맥락(`context`)은 외관만으로 확정할 수 없는 의미다. `visual`만 후보 초안을 만들며 그 초안도 hard activation·property·owner 검증 전이다.

## W001 · 물의 성분·출처·용도 구분 · P1

원 대화: 담수 — Freshwater, 해수 — Seawater, 기수 — Brackish water, 염수 — Saline water, 고농도 염수 — Brine, 지표수 — Surface water, 지하수 — Groundwater, 용천수·샘물, 빗물·우수, 융설수·빙하융수, 광천수 — Mineral water, 증류수 — Distilled water, 음용수 — Potable water, 폐수·하수. 경로: `context` → `situation_context`.

관찰 명세:

- a water sample in its stated collection context
- the specified source vessel or water body
- a visible sampling or treatment context when requested

관계: `water_sample → comes_from → specified_source`.

오인 경계: 담수·해수·기수·증류·음용·폐수는 다른 분류 축이다. 색·광택·투명도만으로 성분·안전성·출처를 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W002 · 샘의 출수점과 이어지는 물길 · P1

원 대화: 용천수·샘물, 샘·용천 — Spring. 경로: `visual` → `location`.

관찰 명세:

- water emerging from a bounded ground opening
- a connected shallow channel
- damp substrate adjoining the outlet

관계: `spring_outlet → feeds → connected_channel`.

오인 경계: 지하수 전체를 동굴 호수로 바꾸지 않는다. 배관 출구와 자연 샘은 원인이 다르다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W003 · 빗물·융설수의 공급 맥락 · P2

원 대화: 빗물·우수, 융설수·빙하융수. 경로: `family` → `location`.

관찰 명세:

- a visible rain runoff outlet or melting snow edge
- a connected downstream wet path
- source material adjoining the water path

관계: `source_edge → supplies → water_path`.

오인 경계: 비·눈·빙하의 출처는 별도 변형이다. 맑은 개울만으로 융설 기원을 주장하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W004 · 방울 맺힘과 젖음성의 외관 · P0

원 대화: 표면장력 — Surface tension, 응집력 — Cohesion, 젖음성 — Wettability, 친수성·소수성, 방울 맺힘 — Beading. 경로: `visual` → `surface_material`.

관찰 명세:

- separate rounded liquid caps on the selected surface
- curved contact boundaries
- surface texture visible between droplets

관계: `droplets → rest_on → selected_surface`.

오인 경계: 둥근 방울 외관은 소수성의 정량 판정이 아니다. 기포·보석·땀의 발생 원인을 자동 치환하지 않는다.

관련 근거: [USGS Surface Tension and Water](https://www.usgs.gov/water-science-school/science/surface-tension-and-water), [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W005 · 물과 고체의 부착 경계 · P1

원 대화: 부착력 — Adhesion. 경로: `visual` → `surface_material`.

관찰 명세:

- liquid contacting the selected solid edge
- a connected wet contact patch
- a hanging drop joined to that edge

관계: `liquid_contact → attaches_to → solid_edge`.

오인 경계: 부착력은 보이지 않는 힘이다. 접촉 형상을 표현하며 모든 재료에 같은 젖음 각도를 강제하지 않는다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W006 · 다공성 재료의 물 번짐 · P0

원 대화: 모세관 현상 — Capillary action. 경로: `visual` → `surface_material`.

관찰 명세:

- a connected damp front within the paper or cloth
- visible fibers continuing across wet and dry regions
- a darker wetted region linked to the liquid contact

관계: `liquid_contact → feeds → damp_front`; `damp_front → occupies → porous_material`.

오인 경계: 번짐과 표면 유동을 구분한다. 상승 속도·흡수량은 단일 사진에서 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary), [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W007 · 용기 벽의 메니스커스 · P0

원 대화: 메니스커스 — Meniscus. 경로: `visual` → `surface_material`.

관찰 명세:

- a curved liquid edge at the inner vessel wall
- a continuous central liquid level
- the same vessel wall meeting that curved edge

관계: `liquid_surface → meets → inner_vessel_wall`.

오인 경계: 물–유리의 전형적 오목 경계를 다룬다. 볼록 메니스커스·젤·렌즈와 등가가 아니다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W008 · 물체의 잠긴 부분과 부유 지지 · P0

원 대화: 부력 — Buoyancy, 부유·뜨기 — Floating. 경로: `visual` → `body_pose`.

관찰 명세:

- one continuous object crossing the water surface
- its displaced submerged volume
- a coherent floating orientation relative to the surface

관계: `water_surface → intersects → floating_object`.

오인 경계: 뜨는 자세는 부력·밀도 수치를 증명하지 않는다. 사람의 지지·호흡 자세는 별도로 검토한다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W009 · 점성의 맥락과 흐름 인상 · P2

원 대화: 점성 — Viscosity. 경로: `context` → `situation_context`.

관찰 명세:

- the requested liquid in its identified context
- a continuous stream or stretched liquid bridge
- a visible flow shape at the stated scale

관계: `liquid_bridge → connects → source_and_receiver`.

오인 경계: 느린 흐름이나 긴 줄기만으로 점성을 측정하지 않는다. 물을 자동으로 시럽처럼 만들지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W010 · 수압의 비가시적 성질 · P2

원 대화: 수압 — Water pressure. 경로: `context` → `situation_context`.

관찰 명세:

- a specified underwater setting
- a pressure instrument only when requested
- a readable physical context for depth

관계: `instrument → measures → water_pressure`.

오인 경계: 수압 자체를 광선·기포·찌그러진 인체로 대신하지 않는다. 수치와 깊이의 증거는 별도다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W011 · 경도와 광물 침전의 차이 · P1

원 대화: 경수·연수 — Hard / soft water, 석회질 물때 — Limescale. 경로: `context` → `situation_context`.

관찰 명세:

- a stated hard water context
- a mineral deposit on a wetted fixture
- a visible deposit boundary on the fixture

관계: `mineral_deposit → covers → fixture_surface`.

오인 경계: 경수·연수는 촉감·맑기 분류가 아니다. 침전물 외관만으로 경도나 조성을 확정하지 않는다.

관련 근거: [USGS Hardness of Water](https://www.usgs.gov/water-science-school/science/hardness-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W012 · 탁도·염분·용존산소 분리 · P0

원 대화: 탁도 — Turbidity, 염분 — Salinity, 용존산소 — Dissolved oxygen. 경로: `context` → `situation_context`.

관찰 명세:

- visible suspended particles when turbidity is specified
- reduced contrast through the water path
- a measurement context for dissolved properties

관계: `particles → scatter → transmitted_light`.

오인 경계: 탁도는 산란 외관, 염분·용존산소는 성분이다. 기포가 용존산소의 직접 영상 증거가 아니다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary), [USGS Hardness of Water](https://www.usgs.gov/water-science-school/science/hardness-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W013 · 수증기·증발·증산의 비가시성 · P0

원 대화: 수증기 — Water vapor, 증발 — Evaporation, 증산 — Transpiration. 경로: `context` → `situation_context`.

관찰 명세:

- a stated phase change context
- a visible liquid surface or plant carrier
- condensed droplets only in the requested visible plume

관계: `phase_change → occurs_at → specified_carrier`.

오인 경계: 기체 수증기를 흰 연기로 그리지 않는다. 증발·증산의 속도와 원인은 외관만으로 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W014 · 차가운 표면의 결로 · P0

원 대화: 응결·응축 — Condensation, 결로. 경로: `visual` → `surface_material`.

관찰 명세:

- small droplets attached to the specified cold surface
- merging droplets on that same surface
- a clear separation from liquid inside the vessel

관계: `condensed_droplets → cover → outer_cold_surface`.

오인 경계: 유리 밖 결로와 안쪽 물·창밖 비를 구분한다. 온도·습도 수치를 픽셀로 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W015 · 비의 낙하·충돌·젖은 결과 · P1

원 대화: 강수 — Precipitation, 이슬비·가랑비, 소나기. 경로: `visual` → `weather`.

관찰 명세:

- airborne rain streaks at the chosen exposure
- contact splashes on the ground
- a connected wet ground region

관계: `rain_drops → strike → ground_surface`.

오인 경계: 이슬비와 소나기의 물방울 크기·밀도는 선택 변형이다. 긴 노출선만으로 강수량을 측정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W016 · 침투와 지표 유출 · P1

원 대화: 침투 — Infiltration, 지표 유출 — Runoff. 경로: `family` → `aftermath_trace`.

관찰 명세:

- a water path entering porous ground or crossing its surface
- a connected wet soil boundary
- a source area linked to the path

관계: `water_path → contacts → soil_boundary`.

오인 경계: 침투와 유출은 다른 경로다. 한 표면 흔적만으로 지하 경로를 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W017 · 이슬의 표면 부착 · P1

원 대화: 이슬 — Dew. 경로: `visual` → `surface_material`.

관찰 명세:

- small droplets on a leaf edge or web strand
- the supporting surface remains continuous
- localized highlights within each droplet

관계: `dew_droplets → rest_on → leaf_or_web`.

오인 경계: 비에 젖은 표면·분무·결로와 외관이 겹친다. 발생 시각·기상 원인은 요청 맥락에 유지한다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W018 · 안개·해무·물안개의 깊이 차폐 · P1

원 대화: 안개 — Fog, 해무 — Sea fog, 물안개. 경로: `visual` → `ambient_particle`.

관찰 명세:

- a low suspended haze near the ground or water
- distant objects losing contrast
- nearer edges remaining more legible

관계: `droplet_haze → obscures → distant_objects`.

오인 경계: 흰 수증기·연기와 동의어로 쓰지 않는다. 해무라는 출처는 연안 맥락과 함께 유지한다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W019 · 독립 물방울 형상 · P1

원 대화: 물방울 — Droplet. 경로: `visual` → `texture`.

관찰 명세:

- one bounded water droplet
- curved transparent volume
- background distortion through that volume

관계: `droplet_volume → refracts → background_detail`.

오인 경계: 모든 방울을 눈물 모양으로 고정하지 않는다. 카메라 bokeh·기포·보석은 별도다.

관련 근거: [USGS Surface Tension and Water](https://www.usgs.gov/water-science-school/science/surface-tension-and-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W020 · 표면을 덮는 얇은 수막 · P0

원 대화: 수막 — Water film. 경로: `visual` → `surface_material`.

관찰 명세:

- a continuous thin wet layer
- localized reflections across that layer
- underlying material detail still visible

관계: `water_film → covers → selected_surface`.

오인 경계: 독립 방울과 수막은 다른 상태다. 수막이 소재 자체를 유리나 금속으로 바꾸지 않는다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W021 · 연속 물줄기와 분사 출구 · P0

원 대화: 물줄기 — Jet / stream. 경로: `visual` → `action`.

관찰 명세:

- a continuous liquid column
- a visible source opening
- a coherent landing or receiving region

관계: `outlet → emits → water_column`; `water_column → contacts → receiver`.

오인 경계: 물줄기의 출구·접촉점을 연결한다. 분리된 방울만으로 연속 분사를 대신하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W022 · 표면을 따르는 가는 물길 · P0

원 대화: 실개울 같은 흐름 — Rivulet. 경로: `visual` → `aftermath_trace`.

관찰 명세:

- a narrow connected liquid path
- branching or merging within the selected surface
- a downstream pool or drop when visible

관계: `rivulet → travels_over → selected_surface`.

오인 경계: 물의 경로를 소유 표면에 묶는다. 피부의 눈물 자국과 벽의 누수 흔적은 별도 변형이다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W023 · 출구에 붙은 낙수와 떨어진 방울 · P1

원 대화: 낙수·물방울 떨어짐 — Dripping. 경로: `visual` → `action`.

관찰 명세:

- a hanging drop at the outlet edge
- a separated drop below it
- a receiver aligned with the fall path

관계: `outlet_edge → releases → falling_drop`.

오인 경계: 한 프레임의 배치는 낙수 주기나 반복 동작의 증거가 아니다.

관련 근거: [USGS Surface Tension and Water](https://www.usgs.gov/water-science-school/science/surface-tension-and-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W024 · 충돌에서 생긴 비말·물보라 · P0

원 대화: 비말 — Spray droplets, 물보라 — Spray. 경로: `visual` → `ambient_particle`.

관찰 명세:

- airborne droplets near a visible collision zone
- a coherent spray fan
- the same wave or outlet continuing into that zone

관계: `collision_zone → launches → airborne_spray`.

오인 경계: 안개·눈·입자 먼지로 대신하지 않는다. 물보라가 생긴 원인과 방향을 같은 장면에 묶는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W025 · 물체–수면 충돌 스플래시 · P0

원 대화: 스플래시 — Splash. 경로: `visual` → `action`.

관찰 명세:

- an object meeting the liquid surface
- a raised liquid sheet at that contact
- detached drops beyond the sheet

관계: `impacting_object → contacts → water_surface`; `contact_zone → raises → splash_sheet`.

오인 경계: 충돌점 없는 장식 비말은 사건 증거가 아니다. 소리는 정지 사진으로 증명하지 않는다.

관련 근거: [USGS Surface Tension and Water](https://www.usgs.gov/water-science-school/science/surface-tension-and-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W026 · 크라운 스플래시의 솟은 테두리 · P0

원 대화: 크라운 스플래시 — Crown splash. 경로: `visual` → `texture`.

관찰 명세:

- a circular rising liquid rim around an impact center
- short spikes on that rim
- detached droplets aligned around the rim

관계: `impact_center → surrounded_by → raised_liquid_rim`.

오인 경계: 왕관 소품·꽃잎·분수와 구분한다. 형성 조건과 순간 시점은 별도이며 모든 낙수의 기본값이 아니다.

관련 근거: [USGS Surface Tension and Water](https://www.usgs.gov/water-science-school/science/surface-tension-and-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W027 · 수중 기포의 경계와 투과 · P0

원 대화: 기포 — Bubble. 경로: `visual` → `ambient_particle`.

관찰 명세:

- bounded gas pockets inside the water
- bright curved rims
- water and background continuing around the pockets

관계: `gas_pockets → contained_in → water_body`.

오인 경계: 물방울은 액체가 공기 중에 있는 경우다. 기포 수만으로 산소량·호흡 행위·생물발광을 추정하지 않는다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W028 · 작은 기포가 모인 포말층 · P0

원 대화: 포말·거품 — Foam / froth. 경로: `visual` → `texture`.

관찰 명세:

- many small bubbles packed into a patch
- irregular foam edges
- liquid visible beside the foam patch

관계: `foam_patch → floats_on → water_surface`.

오인 경계: 포말·기포 하나·먼지층을 구분한다. 흰 거품이 곧 오염은 아니다.

관련 근거: [NOAA What is sea foam](https://oceanservice.noaa.gov/facts/seafoam.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W029 · 파문과 회전 흐름 분리 · P0

원 대화: 동심원 파문, 소용돌이 — Vortex / whirlpool. 경로: `family` → `motion`.

관찰 명세:

- concentric ridges around a disturbance or curved streamlines around a rotation center
- one coherent water surface
- floating tracers only when requested

관계: `water_ridges → organize_around → specified_center`.

오인 경계: 방사형 파문과 회전 유동은 별도 형태다. 회전은 언제나 아래로 빨려드는 깔때기를 뜻하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W030 · 풍파의 수면 능선 · P1

원 대화: 파랑 — Waves, 풍랑 — Wind waves. 경로: `visual` → `texture`.

관찰 명세:

- multiple surface crests
- varying crest spacing at the chosen scale
- a coherent horizon and local wave field

관계: `wave_crests → occupy → water_surface`.

오인 경계: 파동과 물 전체의 이동을 혼동하지 않는다. 바람 세기는 사진으로 정량 확정하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W031 · 너울의 연속 능선 · P1

원 대화: 너울 — Swell. 경로: `visual` → `texture`.

관찰 명세:

- long rounded wave crests
- relatively repeated crest spacing
- a coherent wave field extending across the scene

관계: `swell_crests → extend_across → water_surface`.

오인 경계: 현지 강풍·폭풍을 자동 추가하지 않는다. 발생 위치·주기는 장면 밖 맥락이다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W032 · 쇄파와 백파의 접힘·포말 · P0

원 대화: 쇄파 — Breaking wave, 백파 — Whitecap. 경로: `visual` → `action`.

관찰 명세:

- a crest losing its upright shape
- a falling lip of water
- foam joined to the breaking crest

관계: `wave_lip → falls_into → foam_zone`.

오인 경계: 수면의 흰 빛 반짝임과 백파를 구분한다. 포말의 원인이 같은 파도에 연결되어야 한다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html), [NOAA What is sea foam](https://oceanservice.noaa.gov/facts/seafoam.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W033 · 배럴 파도의 빈 터널 · P0

원 대화: 배럴·튜브 — Barrel / tube. 경로: `visual` → `texture`.

관찰 명세:

- a curling wave lip
- a readable hollow interior
- a continuous wave face meeting the breaking base

관계: `curling_lip → encloses → hollow_wave_interior`.

오인 경계: 고체 유리 터널·평범한 둥근 파도와 다르다. 내부 공간을 거품이 완전히 덮으면 미관찰이다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W034 · 해변 위로 퍼지는 처오름 · P0

원 대화: 처오름 흐름 — Swash. 경로: `visual` → `action`.

관찰 명세:

- a thin sheet extending up the beach
- an advancing foam edge
- wet sand contiguous with the sheet

관계: `swash_sheet → spreads_over → beach_surface`.

오인 경계: 동작 방향은 한 프레임의 추론이다. 되흐름과 서로 동의어로 저장하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W035 · 해변에서 바다로 이어지는 되흐름 · P0

원 대화: 되흐름 — Backwash. 경로: `visual` → `action`.

관찰 명세:

- a thin retreating sheet over sloped sand
- small seaward channels
- a connected receiving sea surface

관계: `backwash_channels → connect_to → sea_surface`.

오인 경계: 모든 되흐름을 위험한 이안류로 바꾸지 않는다. 방향 증거가 약하면 정지 수막으로만 평가한다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W036 · 이동체 뒤의 항적파 · P0

원 대화: 항적파 — Wake. 경로: `visual` → `motion`.

관찰 명세:

- one moving hull or object
- wake ridges joined behind it
- a trailing disturbed surface distinct from ambient waves

관계: `moving_hull → leaves → wake_ridges`.

오인 경계: 항적의 소유자는 같은 선박이다. 배 앞·무관한 물결·일반 포말로 대신하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W037 · 조석·극점·사리·조금·조류 구분 · P1

원 대화: 조석 — Tides, 만조·간조, 밀물·썰물, 사리·조금, 조류 — Tidal current. 경로: `context` → `situation_context`.

관찰 명세:

- a stated tidal stage
- a waterline against a fixed shore reference
- exposed or submerged shore features at that stage

관계: `current_waterline → relates_to → fixed_shore_reference`.

오인 경계: 만조·간조 극점과 조차·주기는 시간·계측 문제다. 한 프레임이 사리·조금이나 조류 방향을 증명하지 않는다.

관련 근거: [NOAA What are tides](https://oceanservice.noaa.gov/facts/tides.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W038 · 해류·용승·침강·세이시의 맥락 · P2

원 대화: 해류 — Ocean current, 용승 — Upwelling, 침강 — Downwelling, 세이시 — Seiche. 경로: `context` → `situation_context`.

관찰 명세:

- a stated flow mechanism
- a visible surface tracer when requested
- instruments or a diagram only in the specified context

관계: `flow_observation → relates_to → stated_mechanism`.

오인 경계: 일반 물결·깊은 파란색을 용승이나 침강의 직접 영상 증거로 쓰지 않는다. 세이시는 시간적 진동이다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary), [NOAA What are tides](https://oceanservice.noaa.gov/facts/tides.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W039 · 해빙·유빙·정착빙의 위치 관계 · P1

원 대화: 해빙 — Sea ice, 유빙 — Drift ice, 정착빙 — Fast ice. 경로: `family` → `location`.

관찰 명세:

- flat ice sheets or floes at the water surface
- water gaps between ice regions
- a shore attachment when fast ice is specified

관계: `ice_region → meets → water_or_shore_boundary`.

오인 경계: 해빙 기원과 이동 상태는 별도 축이다. 한 프레임은 drift 속도나 정착의 지속성을 증명하지 않는다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W040 · 빙산의 수면 교차 부피 · P1

원 대화: 빙산 — Iceberg. 경로: `visual` → `subject`.

관찰 명세:

- a distinct large ice body
- a coherent waterline crossing its lower region
- irregular exposed faces and connected submerged form when visible

관계: `water_surface → intersects → iceberg_body`.

오인 경계: 크기 비율을 고정하지 않는다. 해빙 판·산·빙하벽은 같은 객체가 아니다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W041 · 빙하와 빙붕의 육지 연결 · P1

원 대화: 빙하 — Glacier, 빙붕 — Ice shelf. 경로: `family` → `location`.

관찰 명세:

- a continuous large ice mass
- crevasses or coherent ice faces
- a land connection or floating shelf front appropriate to the specified variant

관계: `ice_mass → connects_to → specified_land_or_shelf`.

오인 경계: 빙하·빙붕의 지지 방식과 기원을 보존한다. 떠 있는 파편만으로 둘을 대신하지 않는다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W042 · 팬케이크 아이스의 원반과 융기 테두리 · P0

원 대화: 팬케이크 아이스 — Pancake ice. 경로: `visual` → `texture`.

관찰 명세:

- multiple flat rounded ice discs
- raised perimeter rims
- liquid water between neighboring discs

관계: `raised_rim → bounds → ice_disc`.

오인 경계: 음식 팬케이크·비누 거품·일반 유빙과 다르다. 테두리와 원반의 동일 객체 관계를 확인한다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W043 · 표면의 서리 결정 · P1

원 대화: 서리 — Frost. 경로: `visual` → `surface_material`.

관찰 명세:

- small branching ice crystals on the selected surface
- a readable supporting material
- localized crystalline edges

관계: `frost_crystals → attached_to → selected_surface`.

오인 경계: 액체 이슬·분무·먼지와 다르다. 서리 발생 온도와 과정은 별도 증거다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W044 · 끝을 따라 길어진 고드름 · P1

원 대화: 고드름 — Icicle. 경로: `visual` → `prop`.

관찰 명세:

- a connected tapered ice body
- attachment to an overhead edge
- a lower pointed or melting tip

관계: `icicle → hangs_from → overhead_edge`.

오인 경계: 유리 장식·물줄기와 구분한다. 성장 기간이나 낙하 위험을 외관으로 확정하지 않는다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W045 · 얼음 입자와 액체의 슬러시 · P1

원 대화: 슬러시·빙수상 혼합물 — Slush. 경로: `visual` → `surface_material`.

관찰 명세:

- small irregular ice or snow particles
- liquid water between them
- a connected granular wet mixture

관계: `ice_particles → mixed_with → liquid_water`.

오인 경계: 한 덩어리 얼음·눈밭·흰 거품과 다르다. 음료나 식품 맥락은 요청에 있을 때만 추가한다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W046 · 윤슬·물비늘의 수면 반짝임 · P0

원 대화: 윤슬, 물비늘. 경로: `visual` → `light_shape`.

관찰 명세:

- small specular glints on wave facets
- a coherent sun or moon lighting direction
- glitter distributed across the water surface

관계: `light_source → reflects_from → wave_facets`.

오인 경계: 카우스틱·수중 발광·뿌린 glitter와 다르다. 물비늘의 비유가 실제 비늘을 추가하지 않는다.

관련 근거: [국립국어원 윤슬 답변](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=320787&searchCondition=&searchKeyword=), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W047 · 실물 소유자가 연결된 수면 반영 · P0

원 대화: 반영 — Reflection, 반영 중심 구도 — 묘사 표현. 경로: `visual` → `reflection_logic`.

관찰 명세:

- one visible reflected object
- its inverted or rippled surface image
- geometric continuity between object and water plane

관계: `visible_object → reflected_in → water_surface`.

오인 경계: 거울 반영과 굴절된 수중 실물을 구분한다. 반영 속 별도 인물은 요청된 초현실 변형이어야 한다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W048 · 수면 경계에서 꺾여 보이는 실물 · P0

원 대화: 굴절 — Refraction. 경로: `visual` → `texture`.

관찰 명세:

- one object continuing through the waterline
- an apparent displacement below the interface
- the same object's material continuing on both sides

관계: `water_interface → refracts → continuous_object`.

오인 경계: 실제 부러짐·추가 팔다리·복제 객체로 굴절을 표현하지 않는다. 시점에 따라 변위가 달라진다.

관련 근거: [OpenStax Total Internal Reflection](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W049 · 수면 굴절이 수중 수광면에 만든 카우스틱 · P0

원 대화: 카우스틱 — Caustics. 경로: `visual` → `light_shape`.

관찰 명세:

- a rippled transparent water surface
- concentrated bright curves on a submerged receiver
- receiver texture visible between the light curves

관계: `light_source → passes_through → water_surface`; `water_surface → concentrates_on → submerged_receiver`.

오인 경계: 수면 반짝임·발광·피부 문신·페인트와 다르다. 빛의 주인과 수광면을 같은 물 공간에 묶는다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission), [OpenStax Total Internal Reflection](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W050 · 수중 위보기의 스넬의 창 · P0

원 대화: 스넬의 창 — Snell’s window. 경로: `visual` → `composition`.

관찰 명세:

- an underwater upward viewpoint
- a bounded view of the above-water scene
- surrounding surface regions reflecting the underwater scene

관계: `water_surface → transmits → above_water_scene`; `outer_surface_region → reflects → underwater_scene`.

오인 경계: 둥근 잠수창·어안 렌즈·구멍이 아니다. 평탄 수면·굴절률로부터 도출한 광학 명세이며 특정 카메라 구도를 모든 수중 사진에 강제하지 않는다.

관련 근거: [OpenStax Total Internal Reflection](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W051 · 입자에서 드러나는 수중 광선 · P0

원 대화: 수중 광선·빛기둥. 경로: `visual` → `lighting`.

관찰 명세:

- a coherent light entry direction
- illuminated suspended particles along a shaft
- a gradual contrast loss with water path

관계: `light_source → illuminates → suspended_particles`.

오인 경계: 공기 중 먼지의 ray를 그대로 복사하지 않는다. 맑기·깊이·광원 크기에 따라 가시성이 다르다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission), [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W052 · 조명과 연결된 수중 후방산란 · P0

원 대화: 후방산란 — Backscatter. 경로: `visual` → `lens_artifact`.

관찰 명세:

- small bright particles within the camera lighting path
- foreground scatter over a more distant subject
- a coherent underwater medium

관계: `camera_light → illuminates → foreground_particles`.

오인 경계: 소나 음향 backscatter·마린 스노·기포와 같은 의미가 아니다. 입자 종류와 침강 방향은 추가 증거가 필요하다.

관련 근거: [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W053 · 물 경로 길이에 따른 색·대비 변화 · P0

원 대화: 청색화·색 소실. 경로: `visual` → `color_grading`.

관찰 명세:

- near and far objects at distinct water path lengths
- progressive contrast loss
- a coherent illuminant affecting their colors

관계: `water_path → attenuates → object_signal`.

오인 경계: 모든 수중을 파란 단색 필터로 만들지 않는다. 탁도·조명·거리·카메라 보정이 함께 관여하며 수심을 단정하지 않는다.

관련 근거: [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W054 · 생물 또는 교란 경로에 묶인 발광 · P0

원 대화: 생물발광 — Bioluminescence. 경로: `visual` → `lighting`.

관찰 명세:

- light localized to specified organisms or their disturbed trail
- darker surrounding water
- continuity between organism and emitting region

관계: `organism_or_trail → emits → localized_light`.

오인 경계: 카우스틱·반사·형광과 구분한다. 모든 해파리나 야간 물을 발광시키지 않는다.

관련 근거: [NOAA What is bioluminescence](https://oceanservice.noaa.gov/facts/biolum.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W055 · 외부 여기광과 연결된 생물형광 · P0

원 대화: 생물형광 — Biofluorescence. 경로: `visual` → `lighting`.

관찰 명세:

- a specified excitation light context
- a distinct emitted color on the organism
- adjacent nonfluorescent surfaces under the same light

관계: `excitation_light → reaches → organism`; `organism → re_emits → fluorescent_light`.

오인 경계: 생물발광·빗해파리 무지갯빛과 다르다. 관측 필터·빛 조건이 없는 색만으로 형광을 확정하지 않는다.

관련 근거: [NOAA What is bioluminescence](https://oceanservice.noaa.gov/facts/biolum.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W056 · 수면의 얇은 유막과 색 띠 · P1

원 대화: 무지갯빛 유막, 기름 유출·유막. 경로: `visual` → `surface_material`.

관찰 명세:

- a thin bounded film on the water
- irregular iridescent bands
- the same surface visible outside the film

관계: `thin_film → covers → water_surface`.

오인 경계: 색 띠는 얇은 막의 광학 표현이다. 석유 종류·독성·유출 원인은 외관만으로 증명하지 않는다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W057 · 하천·개울의 연속 수로 · P1

원 대화: 강·하천 — River / stream, 개울·시내 — Brook / creek, 유수역 — Lotic water, 물길·물굽이. 경로: `visual` → `location`.

관찰 명세:

- a connected channel between banks
- a coherent upstream to downstream path
- bed material visible at the requested clarity

관계: `channel → bounded_by → river_banks`.

오인 경계: 강·개울의 규모 경계를 보편 수치로 고정하지 않는다. 실제 흐름 방향은 추가 단서가 필요하다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W058 · 호수·연못·웅덩이·정수역의 공간 · P1

원 대화: 정수역 — Lentic water, 호수 — Lake, 연못 — Pond, 웅덩이 — Pool / puddle. 경로: `family` → `location`.

관찰 명세:

- a water body enclosed by the appropriate land boundary
- a coherent surface plane
- an edge appropriate to the requested scale

관계: `water_body → bounded_by → land_edge`.

오인 경계: 정수역은 정수 처리수가 아니다. 호수·연못·웅덩이의 규모와 지속성은 별도 변형으로 유지한다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W059 · 습지의 수문·초본·수목·이탄 구분 · P1

원 대화: 습지 — Wetland, 초본 습지 — Marsh, 수목 습지 — Swamp, 이탄습지 — Peatland / bog. 경로: `family` → `location`.

관찰 명세:

- shallow water or saturated soil
- vegetation grounded in that wet substrate
- a continuous wetter to drier transition

관계: `wet_substrate → supports → wetland_vegetation`.

오인 경계: marsh·swamp·bog는 등가 별칭이 아니다. 이탄·화학 상태·장기 수문 조건은 사진만으로 단정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W060 · 저수지의 저장 공간과 구조물 · P2

원 대화: 저수지 — Reservoir. 경로: `visual` → `location`.

관찰 명세:

- a bounded impounded water body
- a dam or managed edge when requested
- a coherent water level against that structure

관계: `storage_structure → bounds → water_body`.

오인 경계: 호수의 외관만으로 인공 저장 목적을 증명하지 않는다. 시설·관리 맥락을 요청에 맞춘다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W061 · 온천 출수와 응결된 안개 · P1

원 대화: 온천·간헐천. 경로: `visual` → `location`.

관찰 명세:

- a bounded spring pool or outlet
- visible condensed mist near the water
- mineral or wet rock edges when specified

관계: `spring_outlet → feeds → pool`.

오인 경계: 뜨거운 물의 정확한 온도나 광천 성분은 보이지 않는다. 안개를 기체 수증기 자체로 기록하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W062 · 간헐천의 지면 분출 연결 · P1

원 대화: 온천·간헐천. 경로: `visual` → `action`.

관찰 명세:

- a jet connected to a ground vent
- droplets around the jet
- a wet surrounding basin

관계: `ground_vent → emits → water_jet`.

오인 경계: 주기적 간헐성은 시간 증거다. 분수 배관·폭포와 분출 기원을 혼동하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W063 · 발원지·유역·분수계의 공간 맥락 · P2

원 대화: 발원지 — Headwaters / source, 유역 — Drainage basin, 분수계 — Watershed divide. 경로: `context` → `situation_context`.

관찰 명세:

- a stated source or drainage context
- connected visible channels
- a ridge or map only when requested

관계: `drainage_paths → converge_on → common_outlet`.

오인 경계: 발원점·지하 공급·유역 전체를 한 사진의 작은 샘으로 대신하지 않는다. 분수계는 분수 시설이 아니다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W064 · 지류가 본류로 만나는 합류부 · P0

원 대화: 지류 — Tributary, 합류부 — Confluence. 경로: `visual` → `location`.

관찰 명세:

- two connected incoming channels
- one joined downstream channel
- a coherent bank junction

관계: `tributary_channel → joins → main_channel`.

오인 경계: 물 색 차이는 선택형이며 필수 조건이 아니다. 색 경계만으로 염분·유속을 확정하지 않는다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W065 · 얕은 하상 위의 여울 · P1

원 대화: 여울 — Riffle. 경로: `visual` → `location`.

관찰 명세:

- shallow bed elements under the surface
- small broken ripples
- a connected channel through that bed

관계: `shallow_bed → modulates → surface_ripples`.

오인 경계: 깊은 파도·큰 폭포와 다르다. 유속·수심 수치와 위험도는 별도다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W066 · 하천 소와 급류의 다른 하상 · P1

원 대화: 소 — Pool, 급류 — Rapids. 경로: `family` → `location`.

관찰 명세:

- a stated pool or rapid reach
- the corresponding smooth or broken surface
- a continuous river corridor

관계: `river_reach → contains → specified_surface_state`.

오인 경계: 느린 깊은 소와 거친 급류를 한 동의어 후보로 합치지 않는다. 상대 깊이·흐름은 맥락이다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W067 · 폭포의 낙차·낙수·폭포소 · P0

원 대화: 폭포·폭포소. 경로: `visual` → `location`.

관찰 명세:

- a water sheet crossing a visible drop edge
- continuous falling water
- a receiving plunge pool and contact spray

관계: `drop_edge → releases → falling_sheet`; `falling_sheet → strikes → plunge_pool`.

오인 경계: 낙수만으로 폭포소의 존재·깊이를 주장하지 않는다. 양쪽이 요청되면 연결 전체가 필수다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W068 · 곡류의 하도와 안쪽 퇴적부 · P1

원 대화: 곡류 — Meander. 경로: `visual` → `location`.

관찰 명세:

- one winding channel
- continuous opposite banks
- an inner bend depositional surface when requested

관계: `winding_channel → bounded_by → continuous_banks`.

오인 경계: 뱀 형상·임의 리본을 추가하지 않는다. 퇴적 위치는 지정된 하도와 연결한다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W069 · 본류와 분리된 우각호 · P0

원 대화: 우각호 — Oxbow lake. 경로: `visual` → `location`.

관찰 명세:

- a curved isolated water body
- nearby continuous river channel
- land separating the old bend from that channel

관계: `land_barrier → separates → old_bend_and_current_channel`.

오인 경계: U자 연못만으로 형성 역사를 확정하지 않는다. 공간 형태와 곡류 절단의 지질 해석을 분리한다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W070 · 사주 사이 갈라지고 합치는 망상하천 · P0

원 대화: 망상하천 — Braided river. 경로: `visual` → `location`.

관찰 명세:

- multiple shallow channel branches
- sediment bars between branches
- visible downstream reconnections

관계: `channel_branches → split_and_rejoin → around_sediment_bars`.

오인 경계: 삼각주의 바다 방류 분기·운하망과 구분한다. 분기만 있고 재합류가 없으면 명세를 일부만 만족한다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W071 · 하천과 연속된 범람원 · P1

원 대화: 범람원 — Floodplain. 경로: `visual` → `location`.

관찰 명세:

- an active river channel
- an adjacent broad low surface
- recent deposition only when specified

관계: `floodplain_surface → adjoins → active_channel`.

오인 경계: 현재 침수와 과거 범람원을 혼동하지 않는다. 지형 외관만으로 재현 주기를 확정하지 않는다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W072 · 하중도·사주의 물 경계 · P1

원 대화: 사주·하중도. 경로: `family` → `location`.

관찰 명세:

- an exposed sediment surface
- water dividing around it or bounding its edge
- coherent grain or vegetation cover

관계: `channel_water → bounds → sediment_body`.

오인 경계: 사주·섬·암반은 구분한다. 물에 둘러싸인 정도와 퇴적물 기원을 별도로 기록한다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W073 · 삼각주 지형과 하구 수역 구분 · P0

원 대화: 삼각주 — Delta, 하구 — Estuary / river mouth. 경로: `family` → `location`.

관찰 명세:

- a river connected to a receiving water body
- sedimentary branching only for a delta variant
- shoreline continuity around the mouth

관계: `river_channel → enters → receiving_water_body`.

오인 경계: 하구가 항상 삼각주는 아니며 하구가 항상 기수인 것도 아니다. 분기·퇴적·염분은 각각 다른 조건이다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm), [NOAA What is an estuary](https://oceanservice.noaa.gov/facts/estuary.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W074 · 해안선·만·해협·곶의 육수 경계 · P2

원 대화: 해안선 — Coastline, 만 — Bay / gulf, 해협 — Strait, 곶 — Cape / headland. 경로: `family` → `location`.

관찰 명세:

- a continuous land water boundary
- the requested indentation passage or protrusion
- a view retaining the relevant land endpoints

관계: `land_boundary → shapes → specified_coastal_space`.

오인 경계: 만·해협·곶은 다른 topology다. 이 가족 카드는 별칭 통합용 후보가 아니며 개별 분해 후 채택한다.

관련 근거: [NPS High Relief Shorelines](https://www.nps.gov/articles/high-relief-erosional-shorelines.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W075 · 외해와 부분 분리된 석호 · P1

원 대화: 석호 — Lagoon. 경로: `visual` → `location`.

관찰 명세:

- a shallow inner water body
- a barrier separating it from outer water
- a limited connection when present

관계: `barrier → separates → inner_and_outer_water`.

오인 경계: 호수·하구와 단순 등가가 아니다. 산호 또는 모래 장벽은 명시된 변형을 따른다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W076 · 해안에서 뻗은 사취 · P1

원 대화: 사취 — Spit. 경로: `visual` → `location`.

관찰 명세:

- a narrow sediment projection
- one landward attachment
- water along the extended edges

관계: `sediment_spit → extends_from → shore_attachment`.

오인 경계: 섬–육지 연결 사주와 다르다. 임의 다리나 양쪽 연결을 추가하지 않는다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W077 · 섬을 잇는 육계사주 · P1

원 대화: 육계사주 — Tombolo. 경로: `visual` → `location`.

관찰 명세:

- a sediment neck joining two land masses
- water on both sides of the neck
- continuous exposed material along the connection

관계: `sediment_neck → connects → two_land_masses`.

오인 경계: 사취·교량·파도선과 다르다. 양쪽 endpoint와 퇴적 재료가 필요하다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W078 · 외해와 안쪽 수역을 나누는 장벽섬 · P1

원 대화: 장벽섬 — Barrier island. 경로: `visual` → `location`.

관찰 명세:

- an elongated island near the mainland
- outer sea on one side
- an inner water gap between island and mainland

관계: `barrier_island → separates → outer_sea_and_inner_water`.

오인 경계: 본토에 붙은 사취와 다르다. 항공 시점은 선택형이며 사용자 시점을 바꾸어 의무를 피하지 않는다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W079 · 사빈·자갈해변·갯벌의 퇴적 표면 · P1

원 대화: 사빈·자갈해변, 갯벌 — Tidal flat. 경로: `family` → `surface_material`.

관찰 명세:

- the requested grain scale or muddy flat
- a coherent wet dry edge
- tidal channels only in the specified flat

관계: `water_edge → meets → specified_sediment_surface`.

오인 경계: 모래·자갈·펄을 같은 질감으로 합치지 않는다. 갯벌은 조석·평탄 지형 맥락이 필요하다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W080 · 현재 수면과 연속된 조간대 대상 · P0

원 대화: 조간대 — Intertidal zone. 경로: `visual` → `location`.

관찰 명세:

- upper drier shore bands
- lower wetter attached life bands
- the current waterline adjoining the low band

관계: `shore_bands → ordered_above → current_waterline`.

오인 경계: 색칠한 줄무늬·젖은 돌 하나로 대체하지 않는다. 생물 종이나 정확한 조위는 외관만으로 확정하지 않는다.

관련 근거: [NOAA What are tides](https://oceanservice.noaa.gov/facts/tides.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W081 · 퇴조 뒤 암반 틈의 조수웅덩이 · P1

원 대화: 조수웅덩이 — Tide pool. 경로: `visual` → `location`.

관찰 명세:

- a water pocket within coastal rock
- exposed surrounding shore
- attached coastal organisms only when requested

관계: `rock_boundary → contains → water_pocket`.

오인 경계: 일반 웅덩이와 구분하되 간조의 시간적 발생 원인은 별도 맥락이다.

관련 근거: [NOAA What are tides](https://oceanservice.noaa.gov/facts/tides.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W082 · 해식절벽·동굴·관통 아치 · P1

원 대화: 해식절벽, 해식동굴·해식아치. 경로: `family` → `location`.

관찰 명세:

- a coastal rock face
- the requested recess or through opening
- sea water contacting the rock base

관계: `sea_water → contacts → coastal_rock_base`.

오인 경계: 동굴의 recess와 아치의 through opening을 나눈다. 파랑 침식 과정은 단일 외관의 확정 사실이 아니다.

관련 근거: [NPS High Relief Shorelines](https://www.nps.gov/articles/high-relief-erosional-shorelines.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W083 · 본토에서 떨어진 시스택 · P1

원 대화: 시스택 — Sea stack. 경로: `visual` → `subject`.

관찰 명세:

- an isolated rock pillar
- water separating it from the shore
- a coherent rock base at the water boundary

관계: `water_gap → separates → rock_pillar_and_shore`.

오인 경계: 빙산·등대·아치 기둥과 다르다. 높이와 침식 연대를 고정하지 않는다.

관련 근거: [NPS High Relief Shorelines](https://www.nps.gov/articles/high-relief-erosional-shorelines.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W084 · 피오르와 리아스의 형성 구분 · P2

원 대화: 피오르·리아스. 경로: `context` → `situation_context`.

관찰 명세:

- a stated drowned valley context
- coastal inlets following that valley
- a view retaining the valley boundaries

관계: `sea_water → occupies → specified_valley`.

오인 경계: 빙하곡과 하곡의 기원을 분리한다. 높은 절벽이 곧 피오르라는 자동 activation을 만들지 않는다.

관련 근거: [NPS High Relief Shorelines](https://www.nps.gov/articles/high-relief-erosional-shorelines.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W085 · 수주·표영·저서·광층의 공간 맥락 · P1

원 대화: 수주 — Water column, 표영 환경 — Pelagic, 저서 환경 — Benthic, 유광층, 박광층·황혼대 — Twilight zone, 무광층 — Aphotic zone. 경로: `context` → `situation_context`.

관찰 명세:

- a specified water column or bottom context
- a coherent light path
- visible bottom only in the requested benthic variant

관계: `water_column → extends_between → surface_and_bottom`.

오인 경계: 유광·박광·무광의 깊이를 고정하지 않는다. 푸른 그라데이션이 광합성 가능 여부를 증명하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary), [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W086 · 수온약층과 염분약층 · P1

원 대화: 수온약층 — Thermocline, 염분약층 — Halocline. 경로: `context` → `situation_context`.

관찰 명세:

- a stated temperature or salinity layer context
- a measurement reference when requested
- optical distortion only in a separately specified gradient

관계: `measurement → describes → specified_water_layer`.

오인 경계: 수온 변화와 염분 변화는 다른 변수다. 흐린 띠만으로 어느 층인지 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W087 · 대륙붕·사면·평원·해구·해산 · P2

원 대화: 대륙붕 — Continental shelf, 대륙사면 — Continental slope, 심해평원 — Abyssal plain, 해구 — Ocean trench, 해산 — Seamount. 경로: `context` → `situation_context`.

관찰 명세:

- the requested seafloor shape at the chosen scale
- coherent bottom relief
- a water body around that relief

관계: `seafloor_relief → occupies → specified_water_body`.

오인 경계: 완만한 면·급경사·좁은 골·고립 산을 구분한다. 실수심·지질 기원은 계측 또는 요청 맥락이다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W088 · 열수 굴뚝과 입자 분출 · P0

원 대화: 열수분출공 — Hydrothermal vent, 블랙 스모커 — Black smoker. 경로: `visual` → `subject`.

관찰 명세:

- a seafloor chimney or vent opening
- a particle laden plume joined to the opening
- surrounding water distinct from the plume

관계: `vent_opening → emits → particle_plume`.

오인 경계: 블랙 스모커는 불 연기·수중 화재가 아니다. 온도·광물 조성은 요청 맥락 또는 계측에 둔다.

관련 근거: [NOAA What is a hydrothermal vent](https://oceanservice.noaa.gov/facts/vents.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W089 · 해저 함몰부의 염수호 경계 · P0

원 대화: 염수호 — Brine pool. 경로: `visual` → `location`.

관찰 명세:

- a pool boundary within a seafloor depression
- surrounding seawater above that pool
- a continuous interface at the depressed floor

관계: `dense_pool → occupies → seafloor_depression`.

오인 경계: 대기 중 호수·수면 구멍으로 대신하지 않는다. 외관은 density와 독성의 직접 증거가 아니다.

관련 근거: [NOAA Brine Pool expedition observation](https://oceanexplorer.noaa.gov/multimedia/daily-image-media-20200917/). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W090 · 수주 속 마린 스노 입자 · P0

원 대화: 마린 스노 — Marine snow. 경로: `visual` → `ambient_particle`.

관찰 명세:

- irregular pale suspended aggregates
- separation between particle sizes
- a coherent deep water background

관계: `particle_aggregates → suspended_in → water_column`.

오인 경계: 얼음 눈·모든 기포·광학 잡광과 다르다. 침강 속도와 유기물 성분을 정지 사진으로 확정하지 않는다.

관련 근거: [NOAA What is marine snow](https://oceanservice.noaa.gov/facts/marinesnow.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W091 · 산호 군체와 암초 공간 · P1

원 대화: 산호초 — Coral reef. 경로: `visual` → `subject`.

관찰 명세:

- connected skeletal colony forms
- polyps only at sufficient scale
- water occupying spaces between colony branches

관계: `coral_colony → attached_to → reef_substrate`.

오인 경계: 산호를 해조 잎으로 바꾸지 않는다. 백색 골격이 곧 사망·백화라는 판정을 자동 활성화하지 않는다.

관련 근거: [NOAA Are corals animals or plants](https://oceanservice.noaa.gov/facts/coral.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W092 · 고정 부위·줄기·엽체가 이어지는 켈프 · P0

원 대화: 켈프 숲 — Kelp forest. 경로: `visual` → `subject`.

관찰 명세:

- a substrate attachment
- continuous stipes leading to broad blades
- coherent underwater blade orientations

관계: `holdfast → anchors → stipes`; `stipes → connect_to → blades`.

오인 경계: 육상 나무·잘피의 뿌리와 동일시하지 않는다. 기낭은 종·요청 변형이 있을 때만 추가한다.

관련 근거: [NOAA What is a kelp forest](https://oceanservice.noaa.gov/facts/kelp.html), [Smithsonian Seagrass and Seagrass Beds](https://ocean.si.edu/ocean-life/plants-algae/seagrass-and-seagrass-beds). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W093 · 바닥에 뿌리내린 해초지 · P0

원 대화: 해초지 — Seagrass meadow. 경로: `visual` → `subject`.

관찰 명세:

- leaf blades arising from the seafloor
- a connected rooted meadow
- open water between individual blades

관계: `rooted_base → supports → leaf_blades`.

오인 경계: 잘피류는 해조류와 다른 식물이다. 잘라 떠다니는 해조 다발로 바꾸지 않는다.

관련 근거: [Smithsonian Seagrass and Seagrass Beds](https://ocean.si.edu/ocean-life/plants-algae/seagrass-and-seagrass-beds). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W094 · 물–노출 뿌리–수간–수관 맹그로브 · P0

원 대화: 맹그로브 — Mangrove. 경로: `visual` → `location`.

관찰 명세:

- tidal water among exposed roots
- connected trunks above those roots
- canopy extending above the trunks

관계: `exposed_roots → connect_to → trunks`; `trunks → support → canopy`.

오인 경계: 종별 지주근·호흡근을 무조건 함께 붙이지 않는다. 수중 켈프 숲·일반 육상 숲과 구분한다.

관련 근거: [NOAA What is a mangrove forest](https://oceanservice.noaa.gov/facts/mangroves.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W095 · 염습지와 갈대밭의 맥락 · P1

원 대화: 염습지 — Salt marsh, 갈대밭. 경로: `family` → `location`.

관찰 명세:

- rooted grass or reed stems
- wet sediment beneath them
- connected water channels when specified

관계: `wet_sediment → supports → specified_stems`.

오인 경계: 염분·종은 맥락이다. 갈대밭을 항상 해안 염습지로 바꾸지 않는다.

관련 근거: [NOAA What is a mangrove forest](https://oceanservice.noaa.gov/facts/mangroves.html), [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W096 · 수면 아래 침수식물 · P1

원 대화: 침수식물. 경로: `visual` → `subject`.

관찰 명세:

- leaves and stems below the waterline
- a coherent submerged attachment context
- light and water around the plant

관계: `water_surface → lies_above → submerged_plant`.

오인 경계: 침수식물·침수된 육상 나무·해조류의 분류는 별도다. 바닥 고정 여부를 요청에 맞춘다.

관련 근거: [Smithsonian Seagrass and Seagrass Beds](https://ocean.si.edu/ocean-life/plants-algae/seagrass-and-seagrass-beds). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W097 · 부엽식물과 부유식물의 고정 여부 · P0

원 대화: 부엽식물, 부유식물. 경로: `family` → `subject`.

관찰 명세:

- leaf surfaces floating at the waterline
- stems or roots appropriate to the specified variant
- water visible between leaves

관계: `floating_leaf → connected_to → specified_support_system`.

오인 경계: 바닥에 뿌리둔 부엽과 자유 부유는 다른 관계다. 가족 카드 자체를 한 강한 후보로 채택하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W098 · 바닥 뿌리와 수상 줄기의 정수식물 · P0

원 대화: 정수식물 — Emergent plant. 경로: `visual` → `subject`.

관찰 명세:

- a rooted base under shallow water
- stems crossing the water surface
- leaves above the same surface

관계: `rooted_base → supports → emergent_stems`.

오인 경계: 정수식물은 정수장·수질 개선 식물이라는 뜻이 아니다. 수면 위아래의 같은 줄기 연결이 필요하다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W099 · 플랑크톤·유영·저서 생물의 생활 위치 · P1

원 대화: 플랑크톤 — Plankton, 식물플랑크톤·동물플랑크톤, 유영생물 — Nekton, 저서생물 — Benthos. 경로: `context` → `situation_context`.

관찰 명세:

- the specified organism in the water column or bottom setting
- a visible scale context when requested
- water and substrate belonging to that setting

관계: `organism → occupies → specified_ecological_space`.

오인 경계: 플랑크톤은 작은 크기의 동의어가 아니다. 능동 유영 능력·영양 방식·생활사는 한 프레임으로 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W100 · 종형 해파리와 연결된 부속지 · P1

원 대화: 해파리 — Jellyfish. 경로: `visual` → `subject`.

관찰 명세:

- a continuous gelatinous bell
- tentacles or oral arms joined to the appropriate bell regions
- water visible through transparent portions

관계: `bell_body → connects_to → specified_appendages`.

오인 경계: 촉수와 구완을 종별로 구분한다. 모든 해파리가 완전 투명하거나 발광한다는 기본값을 만들지 않는다.

관련 근거: [Smithsonian Jellyfish and Comb Jellies](https://ocean.si.edu/ocean-life/invertebrates/jellyfish-and-comb-jellies). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W101 · 빗해파리 몸과 빗살판 열 · P0

원 대화: 빗해파리 — Comb jelly. 경로: `visual` → `subject`.

관찰 명세:

- a gelatinous body
- longitudinal comb rows on that same body
- localized rainbow highlights along those rows

관계: `comb_rows → follow → same_gelatinous_body`.

오인 경계: 무지갯빛 빗살판을 발광 LED·일반 해파리 촉수로 바꾸지 않는다. 여덟 열의 전부가 안 보이면 필요한 관찰 수를 프레이밍에 맞춰 판정한다.

관련 근거: [Smithsonian Jellyfish and Comb Jellies](https://ocean.si.edu/ocean-life/invertebrates/jellyfish-and-comb-jellies). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W102 · 기질에 붙은 말미잘·폴립 · P1

원 대화: 말미잘 — Sea anemone, 산호 폴립 — Coral polyp. 경로: `family` → `subject`.

관찰 명세:

- a attached body base
- tentacles around a visible oral region
- a consistent connection to substrate or colony

관계: `tentacle_ring → surrounds → oral_region`.

오인 경계: 말미잘과 군체 속 산호 폴립의 규모·기질은 다르다. 꽃잎 모양이 실제 식물을 뜻하지 않는다.

관련 근거: [Smithsonian Jellyfish and Comb Jellies](https://ocean.si.edu/ocean-life/invertebrates/jellyfish-and-comb-jellies), [NOAA Are corals animals or plants](https://oceanservice.noaa.gov/facts/coral.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W103 · 문어의 몸·팔·빨판 연결 · P0

원 대화: 문어 — Octopus. 경로: `visual` → `subject`.

관찰 명세:

- a continuous mantle and arm base
- the specified visible arms joined to that base
- suction cups following the arm surfaces

관계: `arm_base → connects_to → octopus_arms`; `arm_surface → carries → suction_cups`.

오인 경계: 팔을 분리된 뱀·장식 줄로 바꾸지 않는다. 가려진 팔까지 억지로 보여 주거나 모든 컵의 종별 배열을 고정하지 않는다.

관련 근거: [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W104 · 오징어 팔과 긴 촉완의 차이 · P0

원 대화: 오징어 — Squid. 경로: `visual` → `subject`.

관찰 명세:

- an elongated mantle
- shorter arms around the head
- two longer tentacles with distinct terminal regions when visible

관계: `head_region → connects_to → arms_and_tentacles`.

오인 경계: 여덟 팔과 두 촉완을 열 개 동일 팔로 합치지 않는다. 촉완이 가려지면 전체 topology의 PASS를 주장하지 않는다.

관련 근거: [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W105 · 갑오징어의 넓은 몸과 지느러미 가장자리 · P1

원 대화: 갑오징어 — Cuttlefish. 경로: `visual` → `subject`.

관찰 명세:

- a broad flattened mantle
- a fin margin along the mantle sides
- connected arms at the head region

관계: `fin_margin → follows → mantle_edge`.

오인 경계: 오징어의 긴 원추형 몸과 자동 등가로 저장하지 않는다. W자 동공은 충분한 원본 해상도가 있을 때만 평가한다.

관련 근거: [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W106 · 앵무조개의 외부 나선 껍데기 · P1

원 대화: 앵무조개 — Nautilus. 경로: `visual` → `subject`.

관찰 명세:

- an external coiled shell
- a body opening at its end
- multiple appendages emerging from the same opening

관계: `shell_aperture → contains → body_and_appendages`.

오인 경계: 내부 방은 절단 표본 변형에만 보인다. 살아 있는 외부 껍데기를 투명 단면으로 바꾸지 않는다.

관련 근거: [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W107 · 가오리의 몸과 펼친 가슴지느러미 · P1

원 대화: 가오리 — Ray. 경로: `visual` → `subject`.

관찰 명세:

- a broad flattened disc
- pectoral fins continuous with that body
- a connected tail where the selected species has one

관계: `pectoral_fins → continuous_with → ray_body`.

오인 경계: 새 날개·천 망토로 바꾸지 않는다. 꼬리 가시·종·독성을 모든 가오리의 기본값으로 쓰지 않는다.

관련 근거: [Smithsonian Shark Cousins Skates and Rays](https://ocean.si.edu/ocean-life/sharks-rays/shark-cousins-skates-and-rays). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W108 · 해마의 목·주둥이·감긴 꼬리 · P2

원 대화: 해마 — Seahorse. 경로: `visual` → `subject`.

관찰 명세:

- an upright curved body
- an elongated snout
- a tail curling around the specified support when requested

관계: `seahorse_tail → wraps_around → specified_support`.

오인 경계: 원 대화 외형을 보존한 초안이다. 꼬리 지지·종별 형태는 공개 1차 자료 추가 대조 전 hard profile로 승격하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W109 · 갑각·집게·더듬이의 종별 소유 · P2

원 대화: 갑각·집게·더듬이. 경로: `family` → `subject`.

관찰 명세:

- a specified crustacean body
- jointed appendages joined to that body
- claws and antennae only in the chosen anatomy

관계: `appendages → attached_to → specified_crustacean_body`.

오인 경계: 게·새우의 팔다리 수와 체절을 한 구조로 합치지 않는다. 종별 근거 추가 후 좁은 후보로 나눈다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W110 · 아가미·지느러미·비늘·촉수·빨판 · P2

원 대화: 아가미·지느러미·비늘, 촉수·빨판. 경로: `family` → `species_marker`.

관찰 명세:

- the selected animal's body region
- connected anatomical structures on that region
- material detail belonging to the same animal

관계: `anatomical_structure → belongs_to → specified_animal_region`.

오인 경계: 물고기 아가미·두족류 빨판·촉수를 사람이나 다른 종에 자동 부착하지 않는다. 신체 소유와 종별 topology를 먼저 결정한다.

관련 근거: [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives), [Smithsonian Shark Cousins Skates and Rays](https://ocean.si.edu/ocean-life/sharks-rays/shark-cousins-skates-and-rays). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W111 · 어군의 개체와 집단 배열 · P1

원 대화: 어군 — School / shoal. 경로: `visual` → `subject`.

관찰 명세:

- multiple separately bounded fish bodies
- a coherent collective arrangement
- water gaps between the individuals

관계: `fish_individuals → form → group_arrangement`.

오인 경계: school과 shoal의 행동적 구분은 정지 인상만으로 확정하지 않는다. 종·개체 수는 명시된 요청을 따른다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W112 · 진주와 진주층의 표면 광택 · P1

원 대화: 진주 — Pearl, 진주층·자개 — Nacre / mother-of-pearl. 경로: `family` → `surface_material`.

관찰 명세:

- a pearl body or nacre shell region
- layered luster on that specific carrier
- curved highlights following the surface

관계: `luster → belongs_to → pearl_or_nacre_carrier`.

오인 경계: 보석 구와 조개 표면층은 별도다. 진주는 반드시 구형·백색이 아니며 반짝임이 발광을 뜻하지 않는다.

관련 근거: [GIA Pearl Description](https://www.gia.edu/pearl-description). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W113 · 조개껍데기와 산호 골격의 구조 · P2

원 대화: 조개껍데기 — Seashell, 산호 골격. 경로: `family` → `prop`.

관찰 명세:

- a specified shell or skeletal carrier
- continuous ridges chambers or branches of that variant
- a coherent material surface

관계: `structural_pattern → belongs_to → specified_skeletal_carrier`.

오인 경계: 부채·나선·가지·뇌 주름은 다른 변형이다. 산호색이나 나선만으로 재료 기원을 확정하지 않는다.

관련 근거: [NOAA Are corals animals or plants](https://oceanservice.noaa.gov/facts/coral.html), [Smithsonian Cephalopods Octopus Squid Cuttlefish and Nautilus](https://ocean.si.edu/ocean-life/invertebrates/octopuses-squids-and-relatives). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W114 · 유목과 바다유리의 풍화 흔적 · P2

원 대화: 유목 — Driftwood, 바다유리 — Sea glass. 경로: `family` → `surface_material`.

관찰 명세:

- a worn wood grain or frosted glass surface
- rounded exposed edges
- coherent weathering on that material

관계: `weathered_edge → bounds → specified_material`.

오인 경계: 나무와 유리는 원자 후보를 나눠야 한다. 원 대화의 해양 기원은 별도 조사 전 외관으로 증명하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W115 · 젖은 자갈·실트·펄의 입도 · P1

원 대화: 몽돌·물에 닳은 자갈, 실트 — Silt, 진흙·펄 — Mud. 경로: `family` → `surface_material`.

관찰 명세:

- a specified coarse or fine sediment surface
- wet material contiguous with water
- the requested grain detail at adequate scale

관계: `water_contact → wets → sediment_surface`.

오인 경계: 입도·젖음·원형 마모는 별개 축이다. 젖어서 어두운 돌이 유기물이나 오염이 되지 않는다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W116 · 해안의 표착물 띠 · P1

원 대화: 표착물 — Wrack / strandline material. 경로: `visual` → `aftermath_trace`.

관찰 명세:

- an irregular line of deposited material
- seaweed or branches only when specified
- a continuous shoreline context

관계: `deposited_material → forms → shoreline_band`.

오인 경계: 표착물 조성과 마지막 조위를 외관만으로 확정하지 않는다. 장식 배열과 퇴적 흔적을 구분한다.

관련 근거: [NPS Sandy Coast Landforms](https://home.nps.gov/articles/sandy-coast-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W117 · 물 접촉 기질의 생물막 · P1

원 대화: 물때·생물막 — Biofilm. 경로: `visual` → `surface_material`.

관찰 명세:

- a thin attached film on the specified substrate
- a coherent wet boundary
- substrate texture continuing below the film

관계: `attached_film → covers → wet_substrate`.

오인 경계: 광물 scale·녹·녹조를 같은 물때로 합치지 않는다. 미생물 종류·건강 위험은 별도다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W118 · 광물 침전과 금속 부식의 흔적 · P1

원 대화: 석회질 물때 — Limescale, 녹·부식 흔적. 경로: `family` → `aftermath_trace`.

관찰 명세:

- the requested mineral crust or corrosion patch
- a trace linked to water contact
- carrier material visible beside the trace

관계: `water_contact_trace → lies_on → specified_carrier`.

오인 경계: 흰 침전과 붉은 녹은 다른 재료 변화다. 한 후보가 양쪽을 자동 혼합하지 않는다.

관련 근거: [USGS Hardness of Water](https://www.usgs.gov/water-science-school/science/hardness-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W119 · 물얼룩·침수선의 높이와 경로 · P0

원 대화: 물얼룩·침수선. 경로: `visual` → `aftermath_trace`.

관찰 명세:

- a continuous stain or sediment line
- a readable wall or object surface
- a localized boundary consistent with the specified water trace

관계: `water_trace → marks → carrier_surface`.

오인 경계: 현재 수면·과거 침수 흔적·광택 줄을 구분한다. 과거 사건 날짜와 원인은 별도 맥락이다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W120 · 마른 진흙의 다각형 건열 · P1

원 대화: 건열 — Mud cracks. 경로: `visual` → `surface_material`.

관찰 명세:

- connected polygonal cracks
- dried sediment plates between cracks
- a coherent drying surface

관계: `crack_network → bounds → dried_sediment_plates`.

오인 경계: 젖은 물결·시멘트 이음새·파충류 비늘로 치환하지 않는다. 물이 없어진 흔적도 물 연구 범위에 포함한다.

관련 근거: [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W121 · 물과 마른 표면의 국소 변화 · P0

원 대화: 몽돌·물에 닳은 자갈, 젖은 발자국·손자국. 경로: `visual` → `aftermath_trace`.

관찰 명세:

- adjacent wet and dry regions of the same material
- a bounded transferred wet mark
- coherent reflections only in the wet region

관계: `wet_mark → interrupts → same_material_surface`.

오인 경계: 광택만으로 재료를 바꾸지 않는다. 같은 돌·바닥의 국소 상태 변화와 다른 물체를 비교하지 않는다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W122 · 염전의 물·얕은 구획·소금 흔적 · P1

원 대화: 천일염, 염전. 경로: `visual` → `location`.

관찰 명세:

- shallow bounded evaporation pans
- coherent embankment divisions
- salt deposits only in the specified drying region

관계: `embankments → divide → evaporation_pans`.

오인 경계: 물색만으로 염분을 확정하지 않는다. 눈밭이나 얼음으로 소금 퇴적을 대체하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W123 · 염수 절임과 식용 해조의 맥락 · P2

원 대화: 염수 절임 — Brining, 식용 해조류. 경로: `family` → `situation_context`.

관찰 명세:

- the specified food carrier
- a liquid brining vessel or harvested seaweed arrangement
- visible processing context only when requested

관계: `food_carrier → placed_in → specified_processing_context`.

오인 경계: 재료의 식용성·염도·보존 안전성은 외관 판정이 아니다. 해조의 얇은 막·띠·갈래를 따로 유지한다.

관련 근거: [FAO A Guide to the Seaweed Industry](https://www.fao.org/4/Y4765E/y4765e00.htm), [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W124 · 한천·카라기난·알긴산의 재료 명칭 · P1

원 대화: 한천 — Agar, 카라기난 — Carrageenan, 알긴산·알지네이트 — Alginate. 경로: `context` → `situation_context`.

관찰 명세:

- a stated hydrocolloid material context
- the requested gel or powder form
- a source or laboratory reference only when specified

관계: `material_sample → identified_by → stated_context`.

오인 경계: 같은 투명 겔 외관에서 세 물질을 구분할 수 없다. 원료·조성·성능을 픽셀 의무로 저장하지 않는다.

관련 근거: [FAO A Guide to the Seaweed Industry](https://www.fao.org/4/Y4765E/y4765e00.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W125 · 양식·담수화·수력·냉각수 시스템 · P2

원 대화: 양식 — Aquaculture, 해수담수화 — Desalination, 수력발전, 냉각수. 경로: `family` → `situation_context`.

관찰 명세:

- a specified aquatic or industrial facility
- connected water handling structures
- visible operation traces belonging to that facility

관계: `facility_component → handles → specified_water_flow`.

오인 경계: 생산 목적과 흐름 연결을 나누고 각 시스템의 후보를 개별 작성한다. 무관한 배관이 기능을 증명하지 않는다.

관련 근거: [FAO A Guide to the Seaweed Industry](https://www.fao.org/4/Y4765E/y4765e00.htm), [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W126 · 얼음 조각의 조형·기포·녹음 · P1

원 대화: 얼음 조각 — Ice sculpture. 경로: `visual` → `subject`.

관찰 명세:

- a shaped continuous ice body
- trapped bubbles or surface frost only in the chosen variant
- melt droplets joined to its lower edges

관계: `melt_droplets → attached_to → ice_sculpture_edge`.

오인 경계: 유리·수정·일반 빙산과 다르다. 재료 온도·작품 내력은 외관으로 확정하지 않는다.

관련 근거: [NSIDC Science of Sea Ice](https://nsidc.org/learn/parts-cryosphere/sea-ice/science-sea-ice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W127 · 수조·수영장의 물과 구조 경계 · P1

원 대화: 수조·아쿠아리움 — Tank / aquarium, 수영장 — Swimming pool. 경로: `family` → `location`.

관찰 명세:

- a bounded water volume
- tank wall or pool coping
- coherent floor and wall connections

관계: `container_walls → bound → water_volume`.

오인 경계: 수조·수영장·아쿠아리움 전시 시설은 다른 규모와 기능이다. 물속 장면에 모두 자동 추가하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W128 · 인피니티 풀의 넘침 가장자리 · P0

원 대화: 인피니티 풀 — Infinity pool. 경로: `visual` → `location`.

관찰 명세:

- a pool water plane meeting a vanishing edge
- a coherent outer vista
- a spill edge retaining physical continuity

관계: `pool_plane → meets → overflow_edge`.

오인 경계: 수영장 벽이 통째로 사라지는 생성 오류와 구분한다. 실제 수평선과 풀 수면은 같은 객체가 아니다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W129 · 반사 연못의 실물–반영 대응 · P1

원 대화: 반사 연못 — Reflecting pool. 경로: `visual` → `location`.

관찰 명세:

- a relatively still bounded pool
- an identified object above the pool
- a corresponding surface reflection

관계: `identified_object → reflected_in → reflecting_pool`.

오인 경계: 잔잔함은 음용성·정수 처리의 증거가 아니다. 연못 종류와 reflection 메커니즘을 따로 저장한다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W130 · 분수와 벽천의 물 경로 · P1

원 대화: 분수 — Fountain, 벽천·워터월 — Water wall. 경로: `family` → `action`.

관찰 명세:

- a visible nozzle or wall source
- a continuous free jet or wall attached sheet
- a linked receiving basin

관계: `water_source → feeds → specified_jet_or_wall_sheet`.

오인 경계: 공중 분사와 벽 부착은 다른 관계다. 후보 가족을 선택하면 모든 시설을 동시에 추가하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W131 · 노천탕의 수면·가장자리·외부 공간 · P1

원 대화: 노천탕. 경로: `visual` → `location`.

관찰 명세:

- a bounded bathing pool
- open outdoor context above it
- continuous wet coping at the pool edge

관계: `bathing_pool → opens_to → outdoor_space`.

오인 경계: 노천탕이 누드·성적 행위·특정 문화 복장을 자동 의미하지 않는다. 온도와 몸의 노출은 별도 요청 축이다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W132 · 수로·수로교·운하의 구조 연결 · P1

원 대화: 수로 — Channel / aqueduct, 수로교, 운하 — Canal. 경로: `family` → `location`.

관찰 명세:

- a continuous water channel
- supporting structure appropriate to the variant
- connected banks or bridge endpoints

관계: `channel_structure → supports → continuous_water_path`.

오인 경계: 수로교의 상부 물길과 선박 운하의 규모·용도를 나눠야 한다. 마른 도로교로 치환하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W133 · 댐·보·수문·갑문의 물 조절 · P1

원 대화: 댐·보, 수문 — Sluice gate, 갑문 — Navigation lock. 경로: `family` → `prop`.

관찰 명세:

- a specified barrier or gate
- coherent upstream and downstream water regions
- a lock chamber only in the navigation variant

관계: `gate_or_barrier → separates → water_regions`.

오인 경계: 수문과 갑문은 같은 문이 아니다. 수위 변화·작동 방향은 시간적 증거 또는 요청 맥락이다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W134 · 취수구·방류구의 입출구 방향 · P0

원 대화: 취수구·방류구. 경로: `family` → `prop`.

관찰 명세:

- a bounded pipe or opening
- a water path joined to that opening
- a visible source or receiving region

관계: `opening → connects_to → specified_water_path`.

오인 경계: 입구·출구는 같은 외관일 수 있다. 맥락 없는 파이프에 유동 방향을 단정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W135 · 저류·정수·하수처리의 시설 맥락 · P2

원 대화: 저류조·저류지, 정수장·하수처리장. 경로: `family` → `situation_context`.

관찰 명세:

- the stated water handling facility
- connected basins or channels
- operation context only when requested

관계: `connected_basins → belong_to → specified_facility`.

오인 경계: 저류와 처리 기능을 구분한다. 물의 맑기만으로 정수장·하수처리장이나 처리 완료를 확정하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W136 · 항구·부두·잔교의 접안 공간 · P1

원 대화: 항구 — Harbor, 부두 — Quay / wharf, 잔교 — Pier. 경로: `family` → `location`.

관찰 명세:

- a coherent vessel water access
- a quay edge or pier structure
- support continuity between land and water structure

관계: `shore_structure → adjoins → vessel_water_space`.

오인 경계: 잔교의 양옆 물과 부두의 접안 edge를 구분한다. 배가 있다는 사실만으로 항구 기능 전체를 증명하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W137 · 방파제와 등대의 연안 배치 · P2

원 대화: 방파제 — Breakwater, 등대 — Lighthouse. 경로: `family` → `location`.

관찰 명세:

- a specified breakwater or lighthouse structure
- a coherent coastline context
- protected water or light source only in the chosen variant

관계: `coastal_structure → placed_at → specified_shore_context`.

오인 경계: 파랑 차폐와 항로 표시 기능은 다르다. 등대 빛으로 모든 바다를 비추거나 방파제를 아치로 바꾸지 않는다.

관련 근거: [NPS High Relief Shorelines](https://www.nps.gov/articles/high-relief-erosional-shorelines.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W138 · 부표의 수면 교차와 계류 · P0

원 대화: 부표 — Buoy. 경로: `visual` → `prop`.

관찰 명세:

- one continuous buoy body crossing the surface
- coherent floating orientation
- a mooring attachment only when requested

관계: `water_surface → intersects → buoy_body`.

오인 경계: 부표의 색·표지 규정·항로 의미는 지역 자료가 있어야 한다. 이 초안은 외형 관계만 다룬다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W139 · 닻·계류줄의 선박 연결 · P0

원 대화: 닻 — Anchor, 계류줄 — Mooring line. 경로: `visual` → `prop`.

관찰 명세:

- a line attached to the selected vessel point
- a continuous line path
- a corresponding anchor or shore attachment

관계: `mooring_line → connects → vessel_and_attachment`.

오인 경계: 끝점 없는 rope는 고정 관계를 증명하지 않는다. 장력·닻의 실제 고정은 영상 밖 사실일 수 있다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W140 · 선체·갑판·선수·선미·현창·돛 장치 · P1

원 대화: 선체 — Hull, 갑판 — Deck, 선수·선미 — Bow / stern, 현창 — Porthole, 돛대·돛·리깅. 경로: `family` → `prop`.

관찰 명세:

- one coherent vessel body
- selected deck window or rigging parts connected to that body
- consistent front and rear orientation

관계: `vessel_parts → belong_to → same_vessel`.

오인 경계: 앞·뒤와 부품 소유를 나눈다. 원 대화의 구조 어휘를 바탕으로 하되 선종별 상세는 1차 자료 대조 후 좁은 후보로 옮긴다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W141 · 물 빠진 건선거와 드러난 선저 · P1

원 대화: 건선거 — Dry dock. 경로: `visual` → `location`.

관찰 명세:

- a ship supported within a dock basin
- exposed lower hull
- a coherent drained basin floor

관계: `dock_supports → carry → exposed_hull`.

오인 경계: 빈 수영장·떠 있는 배·평범한 부두와 다르다. 작업 종류는 요청에 있을 때만 추가한다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W142 · 어망·통발·작살·구명 장비 구분 · P1

원 대화: 어망·통발·작살, 구명부환·구명뗏목. 경로: `family` → `prop`.

관찰 명세:

- the specified net trap spear ring or raft
- connected functional parts of that device
- contact with water or person only when requested

관계: `device_parts → belong_to → specified_device`.

오인 경계: 포획구·부유구·대피구는 다른 물체다. 작살 사용법·포획 방법·구조 실행 절차를 후보에 넣지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W143 · 수영 추진과 떠 있는 정지 자세 · P0

원 대화: 수영 — Swimming, 부유·뜨기 — Floating. 경로: `family` → `body_pose`.

관찰 명세:

- one continuous body in water
- a requested stroke or floating support arrangement
- coherent water contact at limbs and torso

관계: `body_parts → contact → water_medium`.

오인 경계: 정지 부유와 능동 수영은 별도 동작이다. 호흡·관절·균형은 pre-core embodiment 검토에서 결정한다.

관련 근거: [PADI Scuba Certification FAQ](https://www.padi.com/help/scuba-certification-faq). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W144 · 수면 스노클의 공기 중 끝과 입 연결 · P0

원 대화: 스노클링 — Snorkeling. 경로: `visual` → `wearable_accessory`.

관찰 명세:

- a mask on the specified face
- a snorkel joined near the mouth
- its upper opening above the surface in the surface breathing variant

관계: `snorkel → connects_to → mouth`; `snorkel_opening → above → waterline`.

오인 경계: 스노클·스쿠버 레귤레이터·숨참기를 혼동하지 않는다. 물속 숨참기 순간의 별도 변형은 수면 호흡 카드와 분리한다.

관련 근거: [PADI Scuba Certification FAQ](https://www.padi.com/help/scuba-certification-faq). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W145 · 프리다이빙의 수중 몸과 숨참기 맥락 · P0

원 대화: 프리다이빙 — Freediving. 경로: `visual` → `body_pose`.

관찰 명세:

- a specified diver continuously submerged
- a coherent descending or gliding posture
- equipment limited to the requested freediving variant

관계: `diver_body → contained_in → water_medium`.

오인 경계: 외관만으로 숨참기 시간을 증명하지 않는다. 장비 없는 수중 누드나 익수와 동일 의미로 합치지 않는다.

관련 근거: [UNESCO Culture of Jeju Haenyeo](https://ich.unesco.org/en/RL/culture-of-jeju-haenyeo-women-divers-01068). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W146 · 스쿠버의 실린더–호스–입·BCD 연결 · P0

원 대화: 스쿠버다이빙 — Scuba diving, 레귤레이터 — Regulator, 부력조절기 — BCD. 경로: `visual` → `wearable_accessory`.

관찰 명세:

- a secured cylinder and buoyancy device
- a continuous regulator hose
- a mouthpiece belonging to that same diver

관계: `cylinder → feeds → regulator_hose`; `regulator_hose → connects_to → diver_mouth`.

오인 경계: 일반 기포나 등가방만으로 스쿠버를 증명하지 않는다. 실제 압력·산소 농도·성능은 외관 검증이 아니다.

관련 근거: [PADI Scuba Certification FAQ](https://www.padi.com/help/scuba-certification-faq). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W147 · 서핑의 보드·몸 지지·파도면 · P1

원 대화: 서핑 — Surfing. 경로: `visual` → `action`.

관찰 명세:

- a connected surfboard beneath the rider
- visible foot or body support on that board
- the same board contacting a wave face

관계: `rider → supported_by → surfboard`; `surfboard → contacts → wave_face`.

오인 경계: 파도 옆에 떠 있는 보드와 실제 지지 관계를 나눈다. 임의 손잡이·스키 바인딩을 추가하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W148 · 카약·카누의 배와 노 접촉 · P1

원 대화: 카약·카누. 경로: `family` → `prop`.

관찰 명세:

- the requested hull shape
- a seated or kneeling paddler grounded in that hull
- paddle blade contacting water at the selected stroke

관계: `paddler → holds → paddle`; `paddle_blade → contacts → water`.

오인 경계: 배 종류·노날 수·좌석을 개별 변형으로 나눈다. 두 종류를 하나의 후보로 합치지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W149 · 웨트슈트와 드라이슈트의 옷 구조 · P0

원 대화: 웨트슈트 — Wetsuit, 드라이슈트 — Drysuit. 경로: `family` → `wardrobe_style`.

관찰 명세:

- continuous torso and limb panels
- a readable garment entry
- wrist and neck seals only in the dry suit variant

관계: `garment_panels → join_at → specified_seams`.

오인 경계: 밀착복이 곧 웨트슈트는 아니다. 방수·보온·소재·착용자 체형은 별도이며 요청된 길이를 유지한다.

관련 근거: [PADI Scuba Certification FAQ](https://www.padi.com/help/scuba-certification-faq), [PADI Dry Suits](https://www.padi.com/gear/dry-suits). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W150 · 오리발과 발의 연결 · P0

원 대화: 핀·오리발 — Fins. 경로: `visual` → `wearable_accessory`.

관찰 명세:

- a foot pocket around the specified foot
- a continuous fin blade
- the same limb connected to the pocket

관계: `fin_pocket → attached_to → diver_foot`.

오인 경계: 핀을 독립 물고기 지느러미로 바꾸지 않는다. 보이지 않는 발·뒤집힌 pocket은 연결 PASS가 아니다.

관련 근거: [PADI Scuba Certification FAQ](https://www.padi.com/help/scuba-certification-faq). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W151 · 물질·테왁·망사리의 작업 연결 · P0

원 대화: 물질, 테왁, 망사리. 경로: `visual` → `prop`.

관찰 명세:

- a floating tewak body at the surface
- a net collection bag attached to that body
- the specified diver contacting or working beside it

관계: `net_bag → attached_to → tewak_float`; `diver → contacts → tewak_float`.

오인 경계: 현대 foam과 박 소장품을 판본 변형으로 둔다. 일반 스쿠버 실린더·표류 부표와 구분하며 직업·나이는 외관으로 단정하지 않는다.

관련 근거: [국립해양박물관 테왁망사리](https://www.mmk.or.kr/?folder=collection&idx=53&page=view), [UNESCO Culture of Jeju Haenyeo](https://ich.unesco.org/en/RL/culture-of-jeju-haenyeo-women-divers-01068). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W152 · 몸을 가르는 하나의 수면 경계 · P0

원 대화: 잠김 — Immersion / submersion, 반쯤 잠긴. 경로: `visual` → `body_pose`.

관찰 명세:

- one continuous body across the waterline
- coherent submerged and exposed regions
- surface contact at the specified body height

관계: `water_surface → intersects → specified_body_region`.

오인 경계: 수면이 목·가슴·허리 어디를 가르는지 요청을 따른다. 새 팔다리·절단·복제 몸으로 굴절을 표현하지 않는다.

관련 근거: [OpenStax Total Internal Reflection](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W153 · 떠오름·가라앉음의 순간 맥락 · P1

원 대화: 떠오름·가라앉음. 경로: `context` → `action`.

관찰 명세:

- one submerged object
- a stated vertical motion context
- a visible trail or displaced water only when requested

관계: `motion_context → belongs_to → submerged_object`.

오인 경계: 기포 방향·자세만으로 실제 속도·부력 부호·익사를 확정하지 않는다. 시간적 뜻은 요청 맥락에 유지한다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W154 · 손·용기·피부 사이 물 옮김 · P0

원 대화: 물장구, 물을 끼얹기, 헹굼. 경로: `family` → `relational_action`.

관찰 명세:

- a specified hand or vessel carrying water
- a connected transfer path
- water meeting the named receiving body or object

관계: `water_source → transfers_to → named_receiver`.

오인 경계: 물장구·끼얹기·헹굼을 별도 동작으로 분해한다. 손의 소유·물 흐름·접촉점이 모두 필요하다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W155 · 피부 방울과 피부 위 물줄기 · P0

원 대화: 물방울이 맺힌 피부, 물줄기가 흐르는 피부. 경로: `family` → `skin_condition`.

관찰 명세:

- bounded drops or a connected rivulet on the specified skin region
- skin texture continuing between wet regions
- localized moisture highlights

관계: `water_on_skin → belongs_to → specified_skin_region`.

오인 경계: 눈물·땀·빗물·바닷물의 원인을 광택만으로 확정하지 않는다. 피부·의복·유리의 물방울은 다른 소유다.

관련 근거: [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W156 · 공기 중 젖어 뭉친 머리 · P0

원 대화: 젖어 뭉친 머리카락. 경로: `visual` → `hair_style`.

관찰 명세:

- reduced airy volume
- several visible damp strand bundles
- local contact with the face neck or garment

관계: `damp_bundles → belong_to → subject_hair`; `damp_bundles → adhere_to → nearby_surface`.

오인 경계: dry gloss·gel slick back만으로 대신하지 않는다. 현재 wet_damp_clumped_hair_state의 뜻과 guard를 보존한다.

관련 근거: [Bico et al Elastocapillary Coalescence in Wet Hair Nature 2004](https://www.nature.com/articles/432690a), [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W157 · 물속에서 떠 펼쳐진 머리 · P0

원 대화: 수중에서 퍼진 머리카락. 경로: `visual` → `hair_style`.

관찰 명세:

- hair joined to the specified scalp
- separated strands spreading within water
- a coherent buoyant or current aligned arrangement

관계: `hair_strands → connected_to → subject_scalp`; `hair_strands → suspended_in → water_medium`.

오인 경계: 공기 중 중력·축 처짐 의무를 그대로 적용하지 않는다. 수중에서도 모든 가닥이 균일한 부채가 되는 것은 아니다.

관련 근거: [Bico et al Elastocapillary Coalescence in Wet Hair Nature 2004](https://www.nature.com/articles/432690a). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W158 · 땀과 눈물의 발생 맥락 · P1

원 대화: 땀방울, 눈물 자국. 경로: `family` → `skin_condition`.

관찰 명세:

- droplets on the specified skin or a wet track from an eye region
- a continuous carrier surface
- source context preserved in the request

관계: `wet_track → originates_at → specified_source_region`.

오인 경계: 동일 외관이 땀·물·눈물일 수 있다. 눈물은 그려진 뺨 선이나 눈 화장 번짐과 다르고 감정 진단을 뜻하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W159 · 수건과 몸의 접촉·감싸는 겹침 · P1

원 대화: 수건으로 감싼. 경로: `visual` → `garment_detail`.

관찰 명세:

- a continuous towel surface
- overlap around the specified body region
- fabric texture and contact at its edge

관계: `towel_layer → wraps → specified_body_region`.

오인 경계: 요청되지 않은 피복 기본값으로 사용하지 않는다. 감싼 수건과 닦는 동작은 다른 변형이다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W160 · 웨트룩과 미술사 웨트 드레이퍼리 · P0

원 대화: 웨트룩 — Wet look, 웨트 드레이퍼리 — Wet drapery. 경로: `family` → `situation_context`.

관찰 명세:

- the chosen wet looking carrier
- folds or strand groups on that carrier
- coherent material continuity

관계: `wet_looking_form → belongs_to → specified_carrier`.

오인 경계: 실제 물의 존재·밀착 주름·성적 맥락은 서로 다른 축이다. dry statue의 wet drapery에 액체 물을 자동 추가하지 않는다.

관련 근거: [Met Classical Art and Modern Dress](https://www.metmuseum.org/essays/classical-art-and-modern-dress), [Bico et al Elastocapillary Coalescence in Wet Hair Nature 2004](https://www.nature.com/articles/432690a). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W161 · 젖은 천의 밀착·늘어짐·봉제선 · P0

원 대화: 밀착하는 젖은 천 — Clinging fabric, 웨트 티셔츠 — Wet T-shirt. 경로: `visual` → `garment_detail`.

관찰 명세:

- cloth contacting the specified body or object
- connected folds around that contact
- seams and hem identifying the same garment

관계: `cloth_layer → contacts → specified_underlying_surface`.

오인 경계: 밀착을 투명·라텍스·임의 체형 변경과 동일시하지 않는다. T셔츠 종류와 노출 범위는 요청을 유지한다.

관련 근거: [Met Classical Art and Modern Dress](https://www.metmuseum.org/essays/classical-art-and-modern-dress), [USGS Adhesion and Cohesion of Water](https://www.usgs.gov/water-science-school/science/adhesion-and-cohesion-water). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W162 · 젖은 직물의 투과 변형 · P0

원 대화: 젖은 시스루 — Wet transparency. 경로: `visual` → `surface_material`.

관찰 명세:

- readable fibers seams and folds
- partial transmission through the selected cloth patch
- underlying requested surface aligned behind that patch

관계: `cloth_patch → transmits → requested_underlying_surface`.

오인 경계: 젖음은 자동 투명화 조건이 아니다. 소재·두께·조명을 따르고 요청된 불투명·피복 lock을 변경하지 않는다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W163 · 나체 수영·목욕·수중 누드의 분리 · P1

원 대화: 스키니 디핑 — Skinny dipping, 목욕 누드·수중 누드. 경로: `context` → `situation_context`.

관찰 명세:

- the explicitly requested exposed body regions
- coherent water contact
- a stated swimming bathing or art context

관계: `body_exposure → belongs_to → explicit_request`.

오인 경계: 나체는 자동 성행위·유혹·동의·관계를 뜻하지 않는다. 표현을 조사 목록에 보존하며 외관 의무는 요청자 지정과 적용 정책을 따른다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W164 · 샤워·목욕의 물 공급과 접촉 · P0

원 대화: 샤워 장면·목욕 장면. 경로: `family` → `action`.

관찰 명세:

- a requested shower source or bathing basin
- water joined to the specified contact region
- coherent wet surface traces

관계: `water_source → contacts → specified_bathing_region`.

오인 경계: 젖은 피부만으로 씻는 동작을 증명하지 않는다. 증기·수건·유리·노출은 별도 선택 요소다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W165 · 아쿠아필리아·WAM의 문맥별 의미 · P1

원 대화: 아쿠아필리아 — Aquaphilia, 웨트 앤드 메시 — Wet and messy, WAM. 경로: `context` → `situation_context`.

관찰 명세:

- the specified water or messy material context
- a visible material transition on its carrier
- requested expressive tone separately grounded

관계: `material_transition → affects → specified_carrier`.

오인 경계: 물 애호·전시 제목·성적 관심은 별도 용례다. WAM은 해당 당사자 정의에서 물만 있는 wetlook과 다른 messy를 나눈다. 재료가 욕망·동의·빈도의 증거는 아니다.

관련 근거: [Hat Rock Contemporary Aquaphilia exhibition](https://hatrockcontemporary.com.au/exhibitions/18-aquaphilia/works/), [UMD Site Theme](https://umd.net/termsofservice). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W166 · 정상 경계를 넘은 홍수·범람·침수 · P0

원 대화: 홍수 — Flood, 범람, 돌발홍수 — Flash flood, 침수. 경로: `visual` → `location`.

관찰 명세:

- water beyond the usual channel or inside a specified space
- coherent waterline against fixed structures
- displaced objects only when requested

관계: `flood_water → occupies → normally_dry_space`.

오인 경계: 돌발성·발생 원인은 시간적 맥락이다. 보통 강·실내 수영장과 다르고 피해자를 자동 추가하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary), [NPS River Systems and Fluvial Landforms](https://www.nps.gov/subjects/geology/fluvial-landforms.htm). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W167 · 폭풍해일과 지진해일의 기원 분리 · P1

원 대화: 폭풍해일 — Storm surge, 지진해일 — Tsunami. 경로: `context` → `situation_context`.

관찰 명세:

- a stated surge or tsunami event context
- coherent coastal inundation when requested
- structures sharing one waterline

관계: `event_water → inundates → specified_coast`.

오인 경계: 같은 침수 외관에서 기압·바람·해저 변위를 식별할 수 없다. 파도 벽·배럴을 필수 정의로 고정하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W168 · 주변 파도와 비교하는 이상고파 · P1

원 대화: 이상고파·괴물파도 — Rogue wave. 경로: `context` → `situation_context`.

관찰 명세:

- one unusually large wave in a stated comparison context
- neighboring wave scale references
- a coherent water field

관계: `large_wave → compared_with → neighboring_waves`.

오인 경계: 큰 파도 하나만으로 rogue wave의 정량 기준을 충족했다고 주장하지 않는다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W169 · 쇄파대 사이 바다로 빠지는 이안류 · P0

원 대화: 이안류 — Rip current. 경로: `visual` → `motion`.

관찰 명세:

- a narrow seaward flow corridor
- adjacent breaking wave regions
- surface foam or sediment aligned along that corridor

관계: `surface_tracers → follow → seaward_corridor`.

오인 경계: 이안류는 아래로 빨아들이는 소용돌이가 아니다. 표면 단서는 진단·유속 수치의 증거가 아니며 지역 관측 맥락을 유지한다.

관련 근거: [NOAA What is a rip current](https://oceanservice.noaa.gov/facts/ripcurrent.html), [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W170 · 부영양화·HAB·빈산소의 관찰 한계 · P0

원 대화: 부영양화 — Eutrophication, 적조·유해조류 대발생 — HAB, 빈산소 수역·데드존 — Dead zone. 경로: `context` → `situation_context`.

관찰 명세:

- a stated bloom or oxygen measurement context
- visible discoloration only when specified
- sampling evidence or affected ecosystem only in the request

관계: `measurement_context → describes → water_condition`.

오인 경계: 녹색·붉은 물·물고기 부재만으로 영양물질·독성·산소량을 단정하지 않는다. 용어별 변수를 분리한다.

관련 근거: [NOAA What is a red tide](https://oceanservice.noaa.gov/facts/redtide.html), [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W171 · 작은 플라스틱의 재질·크기 증거 · P1

원 대화: 미세플라스틱. 경로: `visual` → `ambient_particle`.

관찰 명세:

- small distinct fragments in a sample context
- a relevant size reference
- a coherent water or sediment carrier

관계: `small_fragments → contained_in → sample_carrier`.

오인 경계: 작은 빛 점이나 기포를 미세플라스틱으로 단정하지 않는다. 크기·재료 식별 없는 장면은 외형 제안만이다.

관련 근거: [NOAA What are microplastics](https://oceanservice.noaa.gov/facts/microplastics.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W172 · 유실 어구와 생물 얽힘 구분 · P1

원 대화: 유령어구·유령어업 — Ghost gear / fishing. 경로: `visual` → `prop`.

관찰 명세:

- a coherent abandoned gear structure in the specified water context
- connected net strands
- an entanglement contact only when requested

관계: `net_strands → contact → specified_organism_or_substrate`.

오인 경계: 유령어구와 실제 포획 지속은 다른 상태다. 얽힘을 장식적인 망사로 대체하지 않으며 종별 상해를 자동 추가하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W173 · 익수·호흡장애·사망의 의미 분리 · P0

원 대화: 익수·익사. 경로: `context` → `situation_context`.

관찰 명세:

- a stated water incident context
- specified immersion geometry
- visible rescue or aftermath only when requested

관계: `immersion_context → relates_to → specified_incident`.

오인 경계: 수중 자세·기포·무표정만으로 호흡장애나 사망을 진단하지 않는다. 익수 과정과 익사 결과를 분리한다.

관련 근거: [WHO Drowning](https://www.who.int/news-room/fact-sheets/detail/drowning). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W174 · 난파·침몰·전복·표류·좌초의 상태 · P1

원 대화: 난파 — Shipwreck, 침몰 — Sinking, 전복 — Capsizing, 표류 — Drifting / adrift, 좌초 — Grounding. 경로: `family` → `situation_context`.

관찰 명세:

- one coherent vessel
- its specified orientation or seabed contact
- water and damage only in the chosen state

관계: `vessel → occupies → specified_navigation_state`.

오인 경계: 침몰은 깊이 이동, 전복은 자세, 좌초는 하상 접촉, 표류는 제어 맥락이다. 빈 배나 안개를 유령선 의미로 승격하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W175 · 수몰 인공물과 침수 실내의 연속 구조 · P0

원 대화: 수몰 — Submergence, 침수된 실내·수중 폐허. 경로: `visual` → `location`.

관찰 명세:

- recognizable connected room or structural elements
- water crossing or surrounding them
- a coherent floor wall or doorway system

관계: `water_body → occupies → connected_built_space`.

오인 경계: 폐허·물이 없는 어두운 방·일반 수족관과 구분한다. history·사망·초자연 의미를 자동 추가하지 않는다.

관련 근거: [USGS Water Science Glossary](https://www.usgs.gov/water-science-school/science/water-science-glossary). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W176 · 수장·물고문의 문맥과 기록 · P2

원 대화: 수장 — Burial at sea / water burial, 물고문. 경로: `context` → `situation_context`.

관찰 명세:

- the stated memorial or violation documentation context
- requested visible water contact only
- participants and objects limited to the described scene

관계: `stated_context → governs → visible_scene`.

오인 경계: 장례 의미와 폭력 의미를 구분한다. 실행 방법·질식 조건·피해 통제법을 작성하지 않고 의미 연구와 비실행적 장면 맥락에 보존한다.

관련 근거: [OHCHR Istanbul Protocol 2022](https://www.ohchr.org/sites/default/files/documents/publications/2022-06-29/Istanbul-Protocol_Rev2_EN.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W177 · 수중 혈액·색 물질 확산 · P1

원 대화: 수중 혈흔·혈액의 확산. 경로: `visual` → `surface_material`.

관찰 명세:

- a bounded colored release source when requested
- diluted branching wisps in the same water
- progressive transparency away from the source

관계: `colored_material → diffuses_into → water_medium`.

오인 경계: 혈액·염료·잉크는 색만으로 구별하지 않는다. 깊은 물의 색 흡수와 조명을 고려하며 붉은 불투명 연기로 고정하지 않는다.

관련 근거: [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission), [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W178 · 심해·수몰 인공물 공포의 맥락 · P1

원 대화: 심해 공포 — Thalassophobia, 수몰 인공물 공포 — Submechanophobia. 경로: `context` → `situation_context`.

관찰 명세:

- the specified vast or submerged artificial setting
- a visible scale contrast
- uncertain distance or bounded visibility when chosen

관계: `viewer_context → relates_to → specified_space`.

오인 경계: 공포 효과·당사자 용어·임상 진단은 다른 층이다. 사람 얼굴이나 어두운 바다만으로 질환·개인 감정을 확정하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W179 · 수면 아래 정체불명 실루엣 · P1

원 대화: 수면 아래 실루엣. 경로: `visual` → `subject`.

관찰 명세:

- a bounded submerged dark form
- a coherent occluding water layer
- a scale or distance relation to visible surroundings

관계: `water_layer → obscures → submerged_form`.

오인 경계: 정체불명은 추가 해부학을 확정하지 않는다. 반영·거대 그림자·실제 수중 실물을 구분한다.

관련 근거: [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W180 · 용왕·용궁·물귀신의 provenance · P2

원 대화: 용왕, 용궁, 물귀신. 경로: `context` → `situation_context`.

관찰 명세:

- the requester specified mythic setting
- requested visible architectural or figure features
- a coherent relation to water

관계: `mythic_context → governs → specified_design`.

오인 경계: 존재 이름이 고정 복장·나이·인종·노출·성격을 결정하지 않는다. 지역 설화와 창작 제안을 나누며 공식 전형 외형으로 주장하지 않는다.

관련 근거: [한국민족문화대백과사전 용신신앙](https://encykorea.aks.ac.kr/Article/E0039556). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W181 · 용왕제·풍어제·기우제의 의례 맥락 · P2

원 대화: 용왕제, 풍어제, 기우제. 경로: `context` → `situation_context`.

관찰 명세:

- a stated cultural or ritual context
- visible participants or objects actually specified
- water or weather relation grounded in that context

관계: `ritual_context → relates_to → specified_water_or_weather`.

오인 경계: 세 의례의 목적·지역·판본을 구분한다. 사진의 물·제단만으로 실제 의례·신앙·효험을 확정하지 않는다.

관련 근거: [한국민족문화대백과사전 용신신앙](https://encykorea.aks.ac.kr/Article/E0039556), [UNESCO Culture of Jeju Haenyeo](https://ich.unesco.org/en/RL/culture-of-jeju-haenyeo-women-divers-01068). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W182 · 인간 상체와 물고기 하체의 인어 연결 · P1

원 대화: 인어 — Mermaid / merman. 경로: `visual` → `subject`.

관찰 명세:

- a specified human upper torso
- a continuous transition into a fish like lower body
- coherent lower body fins in the chosen design

관계: `upper_torso → joins → fish_like_lower_body`.

오인 경계: 자동 여성·미성년·누드·성적 관계·특정 지느러미 수를 만들지 않는다. 인어와 초기 세이렌의 해부를 나눈다.

관련 근거: [Royal Museums Greenwich What is a Mermaid](https://www.rmg.co.uk/stories/art-culture/what-mermaid). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W183 · 초기 그리스 세이렌의 여성–새 혼성 · P1

원 대화: 세이렌 — Siren. 경로: `visual` → `subject`.

관찰 명세:

- the explicitly chosen human and bird components
- coherent attachment between them
- feathered or wing structures belonging to the same figure

관계: `human_component → joins → bird_component`.

오인 경계: 노래는 정지 사진 증거가 아니다. 현대 인어형 해석은 별도 판본이며 물고기 꼬리를 자동 붙이지 않는다.

관련 근거: [Royal Museums Greenwich What is a Mermaid](https://www.rmg.co.uk/stories/art-culture/what-mermaid). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W184 · 세례·성수의 의례적 뜻 · P2

원 대화: 세례 — Baptism, 성수 — Holy water. 경로: `context` → `situation_context`.

관찰 명세:

- a specified water ritual context
- the requested vessel or body contact
- participants actually grounded in the request

관계: `ritual_water → contacts → specified_target`.

오인 경계: 종교 의미는 색·광택·물방울로 증명할 수 없다. 종파·침수·붓기·뿌림을 별도 지정 없이 한 장면에 합치지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W185 · 정화·탄생·경계·기억·심연·이중상의 상징 · P2

원 대화: 정화의 물 — 상징 해석, 탄생의 물 — 상징 해석, 경계의 강 — 상징 해석, 망각·기억의 물 — 상징 해석, 심연 — Abyss, 수면의 이중상 — 상징 해석. 경로: `context` → `situation_context`.

관찰 명세:

- an explicitly chosen symbolic relationship
- visible water and its named counterpart
- a coherent scene carrying that relationship

관계: `water_motif → related_to → specified_counterpart`.

오인 경계: 상징은 연구자 또는 요청자 해석이다. 건강·죄·탄생·기억·불안의 사실 판정이나 모든 장면의 고정 레시피가 아니다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W186 · 찰랑·출렁·일렁·넘실의 시각 번역 · P0

원 대화: 찰랑거리다, 출렁거리다, 일렁이다, 넘실거리다. 경로: `family` → `motion`.

관찰 명세:

- the requested scale of surface ridges
- a coherent edge or reflected form being displaced
- local wave height relative to nearby objects

관계: `wave_surface → displaces → edge_or_reflection`.

오인 경계: 한국어 크기·리듬 인상은 strict 물리 수치가 아니다. 용기·넓은 수면·반영 등 문맥을 보고 별도 표현으로 옮긴다.

관련 근거: [국립국어원 윤슬 답변](https://www.korean.go.kr/front/onlineQna/onlineQnaView.do?mn_id=216&pageIndex=1&qna_seq=320787&searchCondition=&searchKeyword=), [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W187 · 졸졸·콸콸·퐁당·첨벙·찰박의 소리 · P1

원 대화: 졸졸, 콸콸, 퐁당, 첨벙, 찰박·철벅. 경로: `context` → `situation_context`.

관찰 명세:

- the specified narrow flow strong flow or impact action
- a connected source and receiver
- visible splash or shallow contact when requested

관계: `requested_action → contacts → named_receiver`.

오인 경계: 사진은 음량·음색·반복 리듬을 증명하지 않는다. 의성어는 요청의 행동·규모를 해석하는 맥락이며 소리 사실을 pixel gate로 만들지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W188 · 수면 물결무늬의 능선·광암 · P1

원 대화: 물결무늬. 경로: `visual` → `texture`.

관찰 명세:

- repeated curved surface ridges
- alternating reflection bands on those ridges
- a coherent underlying water plane

관계: `reflection_bands → follow → wave_ridges`.

오인 경계: 인쇄된 옷 무늬·모래 ripple·카우스틱은 다른 소유 표면과 메커니즘이다.

관련 근거: [NOAA Waves Currents Tutorial](https://oceanservice.noaa.gov/education/tutorial_currents/03coastal1.html), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W189 · 갯내·물비린내의 감각 맥락 · P2

원 대화: 갯내·물비린내. 경로: `context` → `situation_context`.

관찰 명세:

- the stated coastal or waterside setting
- material sources only when requested
- visible environmental context preserved

관계: `sensory_context → belongs_to → specified_setting`.

오인 경계: 냄새는 한 프레임에서 관찰되지 않는다. 순수 물 자체의 보편 냄새·오염·부패·질병을 자동 부여하지 않는다.

근거 상태: 원 대화의 의미·연구자 외형 제안. 추가 공개 1차 자료 대조가 필요하다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W190 · 한 프레임의 오버언더 수면 연속성 · P0

원 대화: 오버언더·스플릿 샷 — Over-under / split shot. 경로: `visual` → `composition`.

관찰 명세:

- an air scene and underwater scene in one frame
- one coherent waterline dividing them
- continuous shared objects where they cross that line

관계: `waterline → separates → air_and_water_views`; `shared_object → continues_across → waterline`.

오인 경계: 두 사진 콜라주·거울 대칭·두 개의 수면으로 대체하지 않는다. 사용자 crop을 바꿔 의무를 피하지 않는다.

관련 근거: [DivePhotoGuide Over-Unders in Temperate Waters](https://www.divephotoguide.com/underwater-photography-techniques/article/over-unders-temperate-waters/), [OpenStax Total Internal Reflection](https://openstax.org/books/university-physics-volume-3/pages/1-4-total-internal-reflection). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W191 · 수면 높이 시점의 전경과 수평선 · P1

원 대화: 수면 높이 시점 — 묘사 표현. 경로: `visual` → `camera_height`.

관찰 명세:

- a camera viewpoint near the surface
- water ridges prominent in the foreground
- a coherent distant water plane

관계: `near_surface_viewpoint → looks_across → water_plane`.

오인 경계: 장비를 프레임에 추가하는 뜻이 아니다. 낮은 시점·부분 잠긴 렌즈·수중 위보기는 다른 변형이다.

관련 근거: [DivePhotoGuide Over-Unders in Temperate Waters](https://www.divephotoguide.com/underwater-photography-techniques/article/over-unders-temperate-waters/). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

## W192 · 밝은 수면 앞의 수중 실루엣 · P1

원 대화: 수중 역광 실루엣 — 묘사 표현. 경로: `visual` → `lighting`.

관찰 명세:

- a submerged subject contour
- brighter surface light behind it
- coherent water attenuation between camera and subject

관계: `surface_light → backlights → submerged_subject`.

오인 경계: 검은 그림자·수면 반영과 구분한다. 윤곽만 남는 사진은 요청된 얼굴·장비 세부의 관찰 PASS를 만들지 않는다.

관련 근거: [Akkaynak and Treibitz A Revised Underwater Image Formation Model CVPR 2018](https://csms.haifa.ac.il/profiles/tTreibitz/webfiles/revised-underwater-image.pdf), [PBRT Specular Reflection and Transmission](https://pbr-book.org/3ed-2018/Reflection_Models/Specular_Reflection_and_Transmission). 외형 투영과 source의 사실 주장은 구분한다.

후보·원본 픽셀 상태: `PROPOSED_NOT_RUN`.

# 불 관련 시각 의미 카드

각 카드의 외형은 출처의 현상 경계 위에 설계한 선택적 실현이다. 용어 전체에 강제하지 않는다.
맥락 카드에는 픽셀 gate를 만들지 않는다. 출처 수준은 SOURCES.json에 따로 표시했다.

## 불과 연소

### F001 심지에 붙은 촛불과 용융 왁스

분류: observable. 연결 용어: 양초 · 심지 · 화염 · 확산 화염.

- wick: a dark wick centered beneath the flame
- flame: a continuous luminous envelope attached above that wick
- wax_pool: a shallow liquid wax pool within the solid candle

관계: wick → anchors → flame; wax_pool → surrounds → wick.

경계: 촛불은 심지만 타는 현상이 아니며 모든 불을 이 형태로 고정하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html), [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/).

### F002 장작 표면에서 솟는 화염

분류: observable. 연결 용어: 불 · 불길 · 유염연소 · 장작 · 모닥불 · 화원.

- fuel_surface: recognizable wood surfaces beneath the fire
- flame: several continuous flame tongues attached to those surfaces
- air_gap: open gaps between the wood and flame tips

관계: fuel_surface → anchors → flame.

경계: 독립 발광 입자·용암·그을린 장작만으로 현재 화염을 대신하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F003 화염 없이 달아오른 잉걸불

분류: observable. 연결 용어: 불씨 · 잔불 · 잉걸불 · 숯불 · 검붉은 잔광.

- fuel_piece: a solid irregular charred fuel fragment
- glowing_patch: a red luminous patch within that same fragment
- cool_surface: a dark surface adjoining the luminous patch

관계: glowing_patch → belongs_to → fuel_piece.

경계: 불씨는 발화의 비유이기도 하다. 고체 발광을 공중의 화염 덩어리로 바꾸지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F004 화원에서 분리된 작은 불티

분류: observable. 연결 용어: 불꽃 · 불티 · Spark · Burning particle.

- source: a visible emitting fire or hot work point
- burning_particle: small separate luminous particles near that source
- air_gap: dark air separating the particles from continuous flame

관계: source → emits → burning_particle.

경계: 불꽃의 Flame/Spark 다의성을 보존한다. 렌즈 고스트·먼지·보케는 입자 증거가 아니다.

근거: [S07 NWCG Firebrand](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/firebrand-82), [S32 ACS Omega Customizing the Appearance of Sparks](https://pubs.acs.org/doi/10.1021/acsomega.2c03081).

### F005 조각 형태가 남은 비화물

분류: observable. 연결 용어: 비화물 · Firebrand.

- fuel_fragment: a recognizable irregular glowing fuel fragment
- air_gap: air separating the fragment from its original fuel bed
- source: a distinct source fire or charred fuel bed

관계: source → releases → fuel_fragment.

경계: 비화물 존재만으로 다른 장소에 착화한 비화를 확정하지 않는다.

근거: [S07 NWCG Firebrand](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/firebrand-82).

### F006 다공성 연료 표면의 훈소

분류: observable. 연결 용어: 훈소 · 표면연소 · Smoldering · 지중화.

- porous_fuel: a dark porous solid surface
- localized_glow: a small glow within the same porous material
- smoke_wisp: a thin smoke wisp leaving that material

관계: porous_fuel → emits → smoke_wisp; localized_glow → belongs_to → porous_fuel.

경계: 훈소에 발광·연기를 항상 요구하지 않는다. 이것은 보이는 훈소의 한 선택적 실현이다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F007 점화원의 접촉과 붙기 시작한 가장자리

분류: observable. 연결 용어: 발화 · 점화 · 착화 · 불쏘시개 · 부싯깃.

- ignition_source: a small flame held against one fuel edge
- fuel_edge: a newly luminous patch on that same edge
- unburned_fuel: recognizable unburned material adjoining the patch

관계: ignition_source → contacts → fuel_edge.

경계: 순간 장면은 자연발화·자동발화의 원인이나 성공 시간을 증명하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F008 꺼진 촛불의 심지와 연기

분류: observable. 연결 용어: 소염 · Flame extinction · 잔열.

- candle_wick: a dark wick above a visible candle
- smoke_wisp: a narrow wisp rooted at that wick
- wax_pool: a liquid or cooling wax pool around the wick

관계: candle_wick → emits → smoke_wisp.

경계: 연기가 있거나 불꽃이 보이지 않는 것만으로 완전 소화·안전 상태를 판정하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F009 열분해·산화 반응의 비가시적 구분

분류: context. 연결 용어: 연소 · 열분해 · 완전연소 · 불완전연소 · 연쇄반응 · 화학발광.

열분해는 열에 의한 분해이며 연소와 비동치다. 화학종·반응 완결·연쇄반응은 단일 사진으로 확정하지 않는다.

경계: 검은 연기는 모든 불완전연소의 필요충분 조건이 아니다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S02 NIST Pyrolysis](https://www.nist.gov/glossary-term/30146).

### F010 점화 원인과 재발화의 시간 경계

분류: context. 연결 용어: 인화 · 자연발화 · 자동발화 · 재발화 · 발화.

외부 점화원 유무·내부 발열·재발화는 시간 순서와 계측 또는 사건 문맥이 필요하다.

경계: 지금 타는 불 한 장을 재발화나 방화의 증거로 삼지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S02 NIST Pyrolysis](https://www.nist.gov/glossary-term/30146).

## 화염 구조

### F011 버너 출구에 붙은 청색 원뿔

분류: observable. 연결 용어: 예혼합 화염 · 청색 화염 · 화염 기부.

- burner: a bounded metal burner outlet
- inner_cone: a small blue conical region immediately above the outlet
- outer_envelope: a larger flame envelope around the inner cone

관계: burner → anchors → inner_cone; outer_envelope → surrounds → inner_cone.

경계: 청색 원뿔 외형만으로 혼합 방식·연료·온도를 확정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

### F012 매끄러운 화염 외피

분류: observable. 연결 용어: 층류 화염 · Laminar flame.

- flame_base: one continuous flame base on the declared source
- flame_envelope: a smooth tapered luminous boundary
- background: clear dark space outside that boundary

관계: flame_envelope → attaches_to → flame_base.

경계: 매끄러운 정지 외형은 유동의 층류 상태를 계측한 증거가 아니다.

근거: [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/), [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

### F013 불규칙하게 접힌 화염 경계

분류: observable. 연결 용어: 난류 화염 · 혀 모양 불길 · 갈라진 불꽃.

- flame_base: a shared flame base on one fuel region
- flame_envelope: uneven lobes and branching tips above that base
- air_gaps: dark gaps between adjacent luminous lobes

관계: flame_envelope → attaches_to → flame_base.

경계: 모든 갈라진 불꽃을 난류라고 판정하거나 별개의 광원으로 복제하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/).

### F014 분사 출구와 이어진 제트 화염

분류: observable. 연결 용어: 제트 화염 · 화염 분출 · Flame jet.

- nozzle: a visible bounded discharge opening
- flame_jet: a continuous elongated flame issuing from that opening
- jet_axis: the flame aligned with the outlet direction

관계: nozzle → emits → flame_jet.

경계: 무기·산업 버너·요리 토치를 이름만으로 교환하지 않는다. 재료·용도는 요청 문맥이다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S30 IWM First World War gallery large print guide](https://www.iwm.org.uk/sites/default/files/files/2023-10/first_world_war_large_print_guide.pdf).

### F015 액적을 둘러싼 실험 화염

분류: observable. 연결 용어: 액적 화염 · Droplet flame.

- fuel_droplet: a small central liquid droplet in a declared experiment
- flame_shell: a luminous envelope surrounding the same droplet
- apparatus: a coherent enclosing experimental chamber

관계: flame_shell → surrounds → fuel_droplet.

경계: 물방울·마법 구체·용암 방울로 바꾸지 않는다. 모든 액적 화염이 구형이라는 의무는 없다.

근거: [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

### F016 미소중력 실험의 구형 화염

분류: observable. 연결 용어: 미소중력 화염 · Microgravity flame.

- fuel_region: a bounded central experimental fuel region
- flame_shell: a near spherical luminous shell around that region
- chamber: a consistent enclosed observation chamber

관계: flame_shell → surrounds → fuel_region.

경계: 우주 진공에서 산소 없이 타는 불이라는 설정을 자동 추가하지 않는다.

근거: [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/), [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

### F017 냉염의 계측과 낮은 가시성

분류: context. 연결 용어: 냉염 · Cool flame.

냉염은 특정 저온 연소다. NASA의 일부 실험에서는 빛이 희미해 실시간 육안 영상에서 확인할 수 없었고 계측으로 검출했다.

경계: 차가워서 만져도 되는 불·얼음 불꽃·선명한 청색 구체를 정식 정의로 쓰지 않는다.

근거: [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

### F018 화염면·반응대·혼합의 계측 경계

분류: context. 연결 용어: 화염면 · 반응대 · 확산 화염 · 부력 화염.

반응 영역·부력 영향·연료와 산화제의 혼합 경로는 서로 다른 설명 축이다. 정지 외피는 연구자의 선택적 투영이다.

경계: 반응대를 네온 선으로 강제하거나 색으로 혼합 방식을 단정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/), [S04 NASA Cool Flames](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

## 화염 형상

### F019 리본처럼 얇게 펼쳐진 화염

분류: observable. 연결 용어: 리본 같은 불길 · Ribbon-like flame.

- flame_sheet: a thin elongated luminous sheet
- curved_edge: a curved edge continuous with that sheet
- source: one declared fuel or fictional emission source

관계: source → emits → flame_sheet.

경계: 묘사 표현이다. 천 리본이나 고체 발광 띠로 의미를 대체하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F020 세로로 솟는 화염 기둥

분류: observable. 연결 용어: 화염 기둥 · Column of flame · 창끝 같은 불꽃.

- source: a bounded source at the column base
- flame_column: a tall connected luminous fire column
- upper_boundary: a narrowing irregular upper flame boundary

관계: source → anchors → flame_column.

경계: 기둥만으로 화염 회오리의 회전을 증명하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/).

### F021 가로로 이어지는 화염 장벽

분류: observable. 연결 용어: 화염 장벽 · Wall of fire.

- fuel_line: an extended declared fuel or fictional source line
- flame_front: a laterally continuous row of attached flames
- depth_boundary: one coherent foreground and background across the front

관계: fuel_line → anchors → flame_front.

경계: 산불 화선·폭발·불투명한 고체 벽은 서로 다른 실현이다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F022 줄을 이루는 화염 커튼

분류: observable. 연결 용어: 화염 커튼 · Curtain of fire.

- source_array: multiple bounded sources arranged along one line
- flame_array: thin neighboring flame sheets above those sources
- gaps: legible spacing between the individual source positions

관계: source_array → emits → flame_array.

경계: 이것은 선택 가능한 배열이다. 모든 화염 장벽에 장치 배열을 강요하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F023 원형으로 연결된 판타지 불길

분류: creative. 연결 용어: 불의 고리 · Ring of fire.

- fire_ring: a continuous circular arrangement of flame tongues
- interior: an open interior bounded by the same ring
- carrier: a declared ground path or fictional source supporting the ring

관계: fire_ring → bounds → interior.

경계: 판타지 제안이다. 금속 도상 후광·환태평양 지진대·실제 숲불의 동의어가 아니다.

근거: [S29 The Met Shiva as Lord of Dance 39328](https://www.metmuseum.org/art/collection/search/39328).

### F024 머리 위 공간에 놓인 불꽃 왕관

분류: creative. 연결 용어: 불꽃 왕관 · Crown of flames.

- head: one declared head with its silhouette intact
- flame_crown: a crown shaped flame arrangement above that head
- gap: a readable spatial gap or explicitly requested contact boundary

관계: flame_crown → above → head.

경계: 왕관 형태는 머리카락 연소·화상·폭력을 자동 의미하지 않는다.

근거: [S29 The Met Shiva as Lord of Dance 39328](https://www.metmuseum.org/art/collection/search/39328).

### F025 여러 출구에서 솟는 화염 분수

분류: observable. 연결 용어: 화염 분수 · Fountain of flame.

- source_cluster: several declared upward emission openings
- flame_branches: separate rising flames rooted at those openings
- shared_base: a coherent common base beneath the branches

관계: source_cluster → emits → flame_branches.

경계: 불티 분수·용암 분수와 구별하며 장치 제작·점화 절차는 데이터에 넣지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F026 아래로 흘러내리는 불티 배열

분류: observable. 연결 용어: 불꽃 폭포 · Cascade of sparks.

- source_edge: a declared elevated hot work or display edge
- spark_field: many separate luminous particle marks below the edge
- downward_paths: curved downward particle paths in the selected exposure

관계: source_edge → emits → spark_field.

경계: 연속 액체·화염막으로 바꾸지 않는다. 사진의 노출시간과 입자 운동은 별개로 기록한다.

근거: [S32 ACS Omega Customizing the Appearance of Sparks](https://pubs.acs.org/doi/10.1021/acsomega.2c03081).

### F027 펄럭임·일렁임·맥동의 시간 경계

분류: context. 연결 용어: 펄럭이는 불꽃 · 일렁이는 불길 · 맥동하는 화염 · 폭발적으로 치솟는 불.

정지 장면에서는 한 시점의 접힌 경계만 관찰한다. 반복·밝기 변화·급격한 확대는 영상이나 사건 맥락이 필요하다.

경계: 같은 불꽃을 여러 위치에 복제해 시간 변화의 사실 증거라고 하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S03 NASA Why NASA is studying flames in space](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/).

### F028 표면을 따라 뻗은 불길

분류: observable. 연결 용어: 핥듯 번지는 불 · Licking flames.

- fuel_surface: a recognizable selected surface
- flame_tip: a connected flame tip close to that surface
- contact_region: one localized source or contact region feeding the tip

관계: flame_tip → follows → fuel_surface.

경계: 표면 접근만으로 이동 방향·연소 확산 속도를 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F029 대상을 휘감는 판타지 불길

분류: creative. 연결 용어: 휘감는 불길 · 나선형 화염 · Coiling flames.

- target: one recognizable declared target
- flame_curve: a coherent flame curve wrapping around that target
- depth_order: legible front and rear segments around the same target

관계: flame_curve → wraps_around → target.

경계: 창작 형상이다. 감긴 형태만으로 실제 와류·화재 원인을 선언하지 않는다.

근거: [S08 NWCG Fire whirl](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/fire-whirl-86).

### F030 입자 운동과 노출에 의한 불티 궤적

분류: observable. 연결 용어: 불티의 꼬리 · Spark trail · 불티의 소용돌이.

- source: one declared moving luminous particle source
- image_plane: curved bright particle traces across the captured image
- scene_edges: recognizable scene edges separate from the particle traces

관계: image_plane → records → source.

경계: 같은 궤적은 단순 운동 표현일 수 있다. 회전 방향·노출시간은 픽셀만으로 확정하지 않는다.

근거: [S32 ACS Omega Customizing the Appearance of Sparks](https://pubs.acs.org/doi/10.1021/acsomega.2c03081), [S25 Nikon Bright Idea Adding Star Power](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-idea-adding-star-power).

## 색과 불빛

### F031 고체 내부의 적열과 어두운 표면

분류: observable. 연결 용어: 적열 · Red heat · 백열.

- heated_solid: one continuous solid object
- luminous_region: a red luminous region within that object's boundaries
- cool_region: a darker connected region of the same object

관계: luminous_region → belongs_to → heated_solid.

경계: 반사된 붉은빛·빨간 페인트와 구별하며 정확한 온도를 산출하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F032 밝게 발광하는 고체의 외피

분류: observable. 연결 용어: 백열 · White heat · Incandescence.

- heated_solid: a solid body retaining a readable outline
- luminous_region: a very bright pale luminous region within that body
- edge_detail: some coherent edge detail adjoining the bright region

관계: luminous_region → belongs_to → heated_solid.

경계: 센서 포화의 흰 영역·흰색 물체·LED를 자동 백열 고체로 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F033 청색 화염의 색과 화원

분류: observable. 연결 용어: 청색 화염 · 청백색 화염.

- flame: a continuous blue tinted flame envelope
- source: a declared fuel or burner supporting its base
- scene: a coherent surrounding scene outside the flame

관계: source → anchors → flame.

경계: 청색이 모든 화염에서 더 높은 온도·완전연소·동일 연료를 뜻하지 않는다.

근거: [S06 RSC Flame colours](https://edu.rsc.org/resources/flame-colours-a-demonstration/760.article), [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F034 황금·주홍·진홍 화염의 영역

분류: observable. 연결 용어: 황금빛 화염 · 주홍색 불길 · 진홍색 불길 · 발광 그을음.

- flame: a continuous yellow orange or red flame region
- source: a declared source at its base
- luminous_boundary: an irregular luminous boundary distinct from solid surfaces

관계: source → anchors → flame.

경계: 색 이름은 묘사다. 그을음량·온도·유독성을 색으로 계측하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html), [S06 RSC Flame colours](https://edu.rsc.org/resources/flame-colours-a-demonstration/760.article).

### F035 녹색 또는 보라색 화염

분류: observable. 연결 용어: 녹색 화염 · 보라색 화염 · 불꽃반응.

- flame: a continuous green or violet luminous flame region
- source: a declared experimental or fictional source
- color_scope: the hue localized to that flame rather than the whole image

관계: source → anchors → flame.

경계: 실제 발광색과 마법 색을 맥락으로 구별한다. 화학종·실험 제조법은 픽셀에서 도출하지 않는다.

근거: [S06 RSC Flame colours](https://edu.rsc.org/resources/flame-colours-a-demonstration/760.article).

### F036 구리색으로 묘사한 화염

분류: observable. 연결 용어: 구리빛 불꽃 · Copper-colored flame.

- flame: a continuous reddish bronze tinted flame
- source: a coherent source beneath the flame
- receiver: surrounding surfaces with their own material colors

관계: source → emits → flame.

경계: 구리색 묘사는 구리 화합물의 녹색 계열 불꽃반응과 동의어가 아니다.

근거: [S06 RSC Flame colours](https://edu.rsc.org/resources/flame-colours-a-demonstration/760.article).

### F037 불빛이 닿는 수광면

분류: observable. 연결 용어: 불빛 · 화광 · 호박빛 불빛 · Firelight.

- fire_source: one declared luminous fire source
- receiver_surface: warm illumination on the face or surface turned toward that fire
- shadow_side: a darker region on the surface turned away from it

관계: fire_source → illuminates → receiver_surface.

경계: 주황색 소재·전역 색보정·표면 자체 발광으로 광원–수광면 관계를 대신하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F038 화면 밖 화원에서 오는 불빛

분류: observable. 연결 용어: 불빛 · Fire glow.

- receiver_surface: a selected surface illuminated from one declared direction
- shadow_boundary: a coherent transition to the surface's unlit side
- offscreen_source: fire light attributed to a declared offscreen source

관계: offscreen_source → illuminates → receiver_surface.

경계: 화원은 화면 밖에 있을 수 있다. 불빛 요청만으로 보이는 화염을 강제로 추가하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F039 수면에 반사된 화염

분류: observable. 연결 용어: 불빛 · Fire reflection.

- fire_source: one declared fire above or beside the water
- water_surface: a coherent reflective water plane
- reflection: a broken elongated reflection aligned with that same fire

관계: water_surface → reflects → fire_source.

경계: 수중 발광·수면 위 별도 화염·중복 화원으로 반사를 대체하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F040 불빛과 사물 그림자의 연결

분류: observable. 연결 용어: 불빛 · 복사열 · Fire shadow.

- fire_source: one declared fire light source
- occluding_object: an object between the light and a receiving wall
- shadow: a shadow on that wall consistent with the source and object

관계: occluding_object → blocks → fire_source; occluding_object → casts_shadow_on → receiving_wall.

경계: 빛의 가시적 그림자는 복사열의 수치·피부 가열을 증명하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

## 열과 공기

### F041 열원 위 공기를 통과한 배경 왜곡

분류: observable. 연결 용어: 열 아지랑이 · Heat shimmer.

- heat_source: a declared hot surface or fire
- background_edge: a background edge seen through air just above that source
- distortion: localized waviness of that background edge

관계: heated_air_path → distorts → background_edge.

경계: 전역 블러·연기·렌즈 고스트·실제 물체 변형과 구별한다.

근거: [S36 OpenStax Physics Refraction](https://openstax.org/books/physics/pages/16-2-refraction).

### F042 상승 흐름을 보여 주는 입자와 연기

분류: observable. 연결 용어: 상승기류 · 화재 플룸 · 대류 · 열풍.

- source: a bounded fire at the plume base
- plume: a continuous rising column rooted at that source
- tracers: smoke or particles arranged within the same plume

관계: source → emits → plume; plume → carries → tracers.

경계: 방향 표현은 선택된 순간의 외형이다. 속도·대류 열유속은 별도 계측이다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S10 Bureau of Meteorology How fires make thunderstorms](https://www.bom.gov.au/resources/learn-and-explore/fire-weather-knowledge-centre/how-fires-make-thunderstorms).

### F043 열·온도·열유속·열방출률의 분리

분류: context. 연결 용어: 열기 · 복사열 · 전도 · 대류 · 열유속 · 열방출률 · 잔열 · 열복사.

열방출률은 에너지 방출의 시간 변화율, 열유속은 면적당 열전달률이며 온도와 다르다. 열이나 잔열 자체에 보편적인 가시 형상이 없다.

경계: 커다란 불·붉은 피부·주황색 조명으로 정확한 값이나 안전성을 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S38 NIST Heat Release Rate](https://www.nist.gov/publications/heat-release-rate-single-most-important-variable-fire-hazard).

### F044 불소리·냄새·향미의 비가시성

분류: context. 연결 용어: 타닥거림 · 우르릉거리는 불 · 쉭 하는 소리 · 매캐함 · 그을린 냄새 · 불향 · 훈연향 · 그을린 풍미.

소리·냄새·맛은 사진으로 직접 측정하지 않는다. 그 경험의 원인인 연료·도구·표면 상태나 사람의 반응을 선택적으로 표현한다.

경계: 반응 표정은 독성·청력·통증·향미 품질의 사실 증거가 아니다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr), [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html).

## 연기와 잔류물

### F045 화원과 연결된 연기 기둥

분류: observable. 연결 용어: 연기 · 연기 기둥 · Smoke column.

- source: one declared emitting material or fire
- smoke_plume: a coherent plume rooted at that source
- background: background detail partly obscured behind the plume

관계: source → emits → smoke_plume.

경계: 연기는 한 물질이 아니다. 플룸을 공장 증기·안개와 자동 동의어로 묶지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr), [S10 Bureau of Meteorology How fires make thunderstorms](https://www.bom.gov.au/resources/learn-and-explore/fire-weather-knowledge-centre/how-fires-make-thunderstorms).

### F046 빛을 가리는 검은 연기

분류: observable. 연결 용어: 검은 연기 · 흑연 · Black smoke.

- source: a declared smoke emission source
- smoke_plume: dark suspended rolling smoke forms above that source
- occluded_background: background detail reduced behind the smoke

관계: smoke_plume → obscures → occluded_background.

경계: 흑연은 graphite 동음어가 있다. 검은색만으로 연료·독성·방화 여부를 확정하지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F047 희게 산란하는 연기 외관

분류: observable. 연결 용어: 흰 연기 · White smoke.

- source: a declared combustion related source
- smoke_plume: pale suspended plume forms attached to that source
- background: background edges fading through the pale plume

관계: source → emits → smoke_plume.

경계: 흰 연기·물안개·응결 플룸은 원인이 다를 수 있으며 무해함의 증거가 아니다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F048 천장 아래 쌓인 연기층

분류: observable. 연결 용어: 연기층 · Smoke layer.

- ceiling: a readable room ceiling
- smoke_layer: a denser smoke region beneath that ceiling
- lower_region: a more legible lower room below the smoke boundary

관계: smoke_layer → below → ceiling.

경계: 정지 경계만으로 산소 농도·백드래프트 직전·대피 가능성을 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F049 원경 대비를 낮추는 연무

분류: observable. 연결 용어: 연무 · 연기 장막 · Smoke haze.

- near_objects: nearby objects retaining relatively clear edges
- distant_objects: distant objects with reduced contrast
- haze: a coherent suspended veil along the view path

관계: haze → obscures → distant_objects.

경계: 연무·안개·렌즈 베일의 공간적 소유를 구별한다. 대기질 수치를 외관으로 산출하지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F050 공중에 떠 있는 재 조각

분류: observable. 연결 용어: 비산재 · 재 구름 · Fly ash.

- source: a declared residue or ash emission region
- ash_particle: small irregular pale or dark flakes in the air
- air_gap: visible air separating the flakes from solid deposits

관계: source → releases → ash_particle.

경계: 재·불티·눈·꽃가루는 단일 흰 점만으로 구별되지 않는다. 기원을 맥락으로 유지한다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F051 바닥에 남은 느슨한 재

분류: observable. 연결 용어: 재 · Ash · 연소 잔류물.

- residue_bed: a loose pale granular or flaky deposit
- support_surface: the ground or tray supporting that deposit
- char_fragment: recognizable dark fuel fragments within the residue

관계: residue_bed → rests_on → support_surface.

경계: 재는 항상 순수 무기물·흰색만이 아니다. 화산재·눈·먼지의 자동 동의어가 아니다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F052 수광면에 붙은 검댕

분류: observable. 연결 용어: 그을음 · 검댕 · 그을음 자국 · Soot staining.

- deposit_surface: one readable wall or object surface
- soot_patch: a dark matte deposit adhering to that surface
- clean_edge: a boundary between the deposit and a cleaner area

관계: soot_patch → adheres_to → deposit_surface.

경계: 공중 연기·재·검은 도색·피부색을 표면 그을음으로 판정하지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F053 고체 형태가 남은 탄화물

분류: observable. 연결 용어: 탄화물 · Char · 연소 잔류물.

- charred_material: a blackened solid retaining part of the original form
- fracture: porous fracture or cracks within that solid
- residue: loose fragments adjoining the same piece

관계: charred_material → retains_form_of → original_material.

경계: 재의 느슨한 분말과 구별한다. 탄화만으로 현재 타는 상태를 의무화하지 않는다.

근거: [S02 NIST Pyrolysis](https://www.nist.gov/glossary-term/30146), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F054 어두운 끈적한 침착 외관

분류: observable. 연결 용어: 타르 · Tar.

- deposit_surface: a declared cooled surface
- dark_deposit: a dark viscous looking coating on that surface
- runnel: a thick coherent runnel within the coating

관계: dark_deposit → coats → deposit_surface.

경계: 색·광택만으로 타르의 화학 조성을 확정하지 않는다. 소스가 확인되지 않으면 점성 침착 외관으로 기록한다.

근거: [S02 NIST Pyrolysis](https://www.nist.gov/glossary-term/30146), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F055 무색 기체와 입자 크기의 관측 한계

분류: context. 연결 용어: 일산화탄소 · 초미세먼지 · PM₂.₅ · 연소 억제.

일산화탄소·입경·농도·독성은 가시 연기의 색과 독립된 계측 정보다. 수치·분자·입경 표기는 요청된 교육 도식에만 별도 연결한다.

경계: 일산화탄소를 검은 연기 덩어리로 그리거나 연기 부재를 안전 판정으로 삼지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

## 재료 손상

### F056 열로 갈색으로 변한 표면

분류: observable. 연결 용어: 그을림 · 눋기 · Scorching.

- selected_surface: a readable cloth paper or wood surface
- scorched_patch: a localized brown darkened patch
- unaltered_area: an adjoining area retaining the material's original texture

관계: scorched_patch → belongs_to → selected_surface.

경계: 그을림·그을음 침착·완전 탄화는 같은 변화가 아니다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F057 말리고 사라진 종이 가장자리

분류: observable. 연결 용어: 탄 종이 가장자리 · Burnt paper edges.

- paper_sheet: one coherent thin sheet of paper
- charred_edge: an irregular dark curled perimeter
- missing_patch: a small absent section contiguous with that edge

관계: charred_edge → bounds → paper_sheet.

경계: 종이 전체를 숯 덩어리로 바꾸거나 손상만으로 사건 원인을 단정하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F058 다각형 균열이 생긴 탄화목

분류: observable. 연결 용어: 악어가죽 같은 탄화 균열 · Alligator-like char.

- charred_wood: a recognizable wood surface
- crack_network: polygonal cracks within the charred layer
- char_blocks: raised dark blocks separated by those cracks

관계: crack_network → divides → charred_wood.

경계: 균열 크기·광택만으로 촉진제·급속 화재·방화를 판단하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F059 짧게 그슬린 털 끝

분류: observable. 연결 용어: 그슬림 · Singeing.

- selected_hair: hair or fur owned by one declared subject
- singed_tips: localized curled or shortened tips
- intact_strands: adjoining strands retaining their original structure

관계: singed_tips → belong_to → selected_hair.

경계: 전신 화상·타인의 머리·모든 털 제거로 확대하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F060 열로 둥글어진 용융 모서리

분류: observable. 연결 용어: 용융 · 녹아내린 모서리 · Melting.

- heated_object: one recognizable selected object
- softened_edge: a drooping rounded edge continuous with that object
- cooled_runnel: a solidified flow attached to the same edge

관계: softened_edge → belongs_to → heated_object.

경계: 녹·오염·탄화와 다르며 소재가 요청되지 않으면 모든 물체를 플라스틱으로 바꾸지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf), [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

### F061 열 이력을 맥락으로 둔 휜 판재

분류: observable. 연결 용어: 열변형 · 뒤틀림 · Warping.

- selected_plate: one continuous plate or frame
- warped_region: a bent or twisted segment within that plate
- connection: the segment connected to unchanged parts of the same object

관계: warped_region → belongs_to → selected_plate.

경계: 휨 외형만으로 열·하중·충돌 중 원인을 확정하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf), [S15 NIST Fire-Affected Concrete](https://www.nist.gov/programs-projects/investigation-fire-affected-concretes-residual-properties-and-link-petrographic).

### F062 도장층의 부풀음

분류: observable. 연결 용어: 표면 부풀음 · Blistering.

- coated_surface: one readable painted or coated substrate
- blisters: small raised pockets within the coating
- intact_coating: intact coating adjoining the raised areas

관계: blisters → belong_to → coated_surface.

경계: 피부 수포·기포·소결 입자와 구별하며 화재만을 유일 원인으로 강제하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F063 층이 들뜬 코팅과 기판

분류: observable. 연결 용어: 박리 · Delamination · Peeling.

- substrate: one continuous underlying substrate
- detached_layer: a thin surface layer lifting from it
- exposed_area: an area of the same substrate revealed beneath the lifted layer

관계: detached_layer → separates_from → substrate.

경계: 콘크리트 조각 박락·가루 재·그을음과 동의어로 쓰지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F064 콘크리트 표면의 박락

분류: observable. 연결 용어: 박락 · Spalling.

- concrete_element: one recognizable concrete element
- missing_surface: a rough recessed region where surface material is missing
- fragments: compatible broken surface fragments near that element

관계: fragments → separate_from → concrete_element.

경계: 표면 손상만으로 정확한 온도·구조 안전·보수 가능성을 판정하지 않는다.

근거: [S15 NIST Fire-Affected Concrete](https://www.nist.gov/programs-projects/investigation-fire-affected-concretes-residual-properties-and-link-petrographic).

### F065 화재로 손상된 건물 외관

분류: observable. 연결 용어: 화재 흔적 · 불에 그을린 폐허 · 대화재.

- damaged_structure: one legible building or room structure
- charred_surfaces: blackened surfaces attached to that structure
- debris: damaged remnants spatially connected to the same structure

관계: debris → belongs_to → damaged_structure.

경계: 손상 패턴은 조사 단서다. 단일 이미지가 발화점·방화·사망을 증명하지 않는다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F066 소결·유리화의 미시구조 경계

분류: context. 연결 용어: 소결 · 유리화 · Sintering · Vitrification.

입자 결합·유리질 형성은 공정·미시구조를 포함하는 명칭이다. 매끈한 표면만으로 확정하지 않는다.

경계: 성형·용융·서냉·결정화와 동치로 저장하지 않는다. 전용 재료학 추가 조사 후 승격한다.

근거: [S17 Corning Museum Annealing](https://allaboutglass.cmog.org/definition/annealing), [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

## 화재 사건

### F067 구획 안 연료에 붙은 화재

분류: observable. 연결 용어: 화재 · 구조물 화재 · 구획 화재 · 환기 지배 화재 · 연료 지배 화재.

- room: one coherent enclosed room with readable openings
- burning_fuel: recognizable burning furniture or fuel within that room
- smoke: smoke spatially connected to the same fire

관계: burning_fuel → inside → room; burning_fuel → emits → smoke.

경계: 화염·개구부 외형은 환기 지배·연료 지배를 계측한 사실이 아니다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S12 NIST Backdraft](https://www.nist.gov/glossary-term/18991), [S13 NIST Defining Flashover for Fire Hazard Calculations](https://www.nist.gov/publications/defining-flashover-fire-hazard-calculations).

### F068 액체 표면 위 화염

분류: observable. 연결 용어: 유류 화재 · Flammable-liquid fire.

- liquid_pool: a declared liquid fuel surface in a bounded region
- flame: a continuous flame attached above that surface
- pool_boundary: a readable perimeter supporting the flame base

관계: liquid_pool → anchors → flame.

경계: 단일 외관으로 액체 종류·누출 경로·발화 원인을 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S39 RSC Flames in the kitchen](https://edu.rsc.org/download?ac=509309).

### F069 전기·금속 화재의 원인 경계

분류: context. 연결 용어: 전기 화재 · 금속 화재 · 지하 화재 · 대화재.

전기·금속·지하라는 말은 에너지원·연료·장소를 각각 소유한다. 원인이 확인된 문맥과 관찰된 화염·손상을 연결한다.

경계: 밝은 흰 빛은 금속 화재의 진단이 아니고 전선 근처 불은 누전의 증거가 아니다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F070 배터리 셀의 배출구와 플룸

분류: observable. 연결 용어: 배터리 열폭주 · Battery thermal runaway.

- battery_cell: a recognizable declared cell or battery enclosure
- vent: a localized visible outlet on that enclosure
- vent_plume: a plume rooted at the same outlet

관계: vent → belongs_to → battery_cell; vent → emits → vent_plume.

경계: 가스 배출·점화·셀 파열은 별개다. 필수 화염·폭발·한 가지 가스색을 강요하지 않는다.

근거: [S33 FAA Hazard Analysis for Various Lithium Batteries](https://www.fire.tc.faa.gov/pdf/TC-16-17.pdf).

### F071 구획 밖으로 드러난 화구 외관

분류: observable. 연결 용어: 화구 · Fireball · 화염 분출.

- source_region: one declared combustion event region
- flame_envelope: a rounded expanding looking luminous envelope
- surrounding_space: scene space surrounding the same event

관계: source_region → emits → flame_envelope.

경계: 팽창은 순간 외형의 묘사다. 태양·유성 화구·폭굉의 증거로 사용하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S34 NIST Deflagration](https://www.nist.gov/glossary-term/21671).

### F072 플래시오버·백드래프트의 사건 분리

분류: context. 연결 용어: 플래시오버 · 백드래프트 · 화염 확산.

플래시오버는 구획 내 광범위한 연소로 전환되는 단계다. 백드래프트는 산소 부족 생성물과 갑작스러운 공기 유입을 포함한다. 정지 화염에 사건 이름을 확정하지 않는다.

경계: 문 밖 불꽃만으로 백드래프트라고 판정하거나 둘을 단일 폭발 후보로 합치지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S12 NIST Backdraft](https://www.nist.gov/glossary-term/18991), [S13 NIST Defining Flashover for Fire Hazard Calculations](https://www.nist.gov/publications/defining-flashover-fire-hazard-calculations).

### F073 전파 속도와 역화의 비가시적 조건

분류: context. 연결 용어: 폭연 · 폭굉 · 분진폭발 · 역화.

폭연·폭굉의 전파 속도와 역화의 상류 진행은 시간·매질 정보가 필요하다. 이번 데이터는 그 이름을 기하 형태와 분리한다.

경계: 큰 화구·충격파처럼 보이는 고리만으로 폭굉을 선언하지 않는다. 폭굉 전문 자료는 추가 조사 대상으로 둔다.

근거: [S34 NIST Deflagration](https://www.nist.gov/glossary-term/21671), [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

## 소방과 방호

### F074 같은 연료로 향하는 소화 물줄기

분류: observable. 연결 용어: 소화 · 진화 · 진압 · 냉각 · Fire suppression.

- nozzle: one readable suppression nozzle
- water_stream: a coherent water stream from that nozzle
- target_fuel: the declared burning material where the stream lands

관계: nozzle → emits → water_stream; water_stream → contacts → target_fuel.

경계: 물줄기가 보인다고 진화 완료·적합한 소화법·안전성을 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S31 NFPA Truth About Home Fire Sprinklers](https://content.nfpa.org/-/media/project/storefront/catalog/files/fire-sprinkler-initiative/sprinkler-myths-and-facts.pdf?rev=9ffa003adce542e0965df177266424ce).

### F075 열에 반응한 개별 스프링클러 헤드

분류: observable. 연결 용어: 스프링클러 · Fire sprinkler.

- sprinkler_head: one active ceiling mounted sprinkler head
- spray: a spray pattern rooted at that same head
- nearby_heads: other visible heads retaining their own inactive state

관계: sprinkler_head → emits → spray.

경계: 연기만으로 모든 헤드가 한꺼번에 켜지는 전형을 기본값으로 만들지 않는다.

근거: [S31 NFPA Truth About Home Fire Sprinklers](https://content.nfpa.org/-/media/project/storefront/catalog/files/fire-sprinkler-initiative/sprinkler-myths-and-facts.pdf?rev=9ffa003adce542e0965df177266424ce).

### F076 감지기·소화기·방화문의 객체 구별

분류: context. 연결 용어: 연기감지기 · 소화기 · 방화문 · 방화구획 · 내화 · 난연 · 불연 · 질식소화.

감지·소화 도구·구획·재료 성능을 별도 객체와 속성으로 둔다. 장치의 존재는 작동·등급·법적 적합성의 픽셀 증거가 아니다.

경계: 방화문 외관만으로 내화 시간을 추정하거나 소화기를 모든 화재에 동일하게 연결하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S31 NFPA Truth About Home Fire Sprinklers](https://content.nfpa.org/-/media/project/storefront/catalog/files/fire-sprinkler-initiative/sprinkler-myths-and-facts.pdf?rev=9ffa003adce542e0965df177266424ce).

### F077 보호복과 장비를 갖춘 소방 인물

분류: observable. 연결 용어: 방화복 · Firefighter protective clothing · 열화상 카메라.

- firefighter: one identifiable firefighter in declared protective clothing
- equipment: a declared held tool owned by that firefighter
- action_target: the same visible fire or inspection target addressed by the tool

관계: firefighter → holds → equipment; equipment → directed_at → action_target.

경계: 소방 의복만으로 안전 확보·직업 자격·열화상 측정을 완료했다고 하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F078 연료를 끊는 방화선의 공간 구조

분류: observable. 연결 용어: 방화선 · 연료 제거 · Firebreak.

- fuel_bed: a declared vegetation fuel area
- bare_corridor: a connected strip with visibly reduced fuel
- opposite_fuel: vegetation on the other side of that same corridor

관계: bare_corridor → separates → fuel_bed.

경계: 맨땅 경계는 소화 성공·확산 차단을 증명하지 않는다. 도로와 동치 별칭이 아니다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

## 산불과 생태

### F079 풀과 낮은 연료에 붙은 지표화

분류: observable. 연결 용어: 산불 · 들불 · 지표화 · 화선.

- surface_fuel: recognizable grass litter or low vegetation
- flame_front: flames attached to that lower fuel layer
- canopy: a distinguishable upper vegetation layer if present

관계: flame_front → burns_at → surface_fuel.

경계: 모든 산불을 수관까지 타는 불로 확대하지 않는다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F080 나무 수관에 놓인 화염

분류: observable. 연결 용어: 수관화 · Crown fire.

- tree_canopy: recognizable tree crowns above trunks
- canopy_flames: flames physically rooted within those crowns
- lower_layer: a distinct lower vegetation and trunk region

관계: canopy_flames → burns_at → tree_canopy.

경계: 한 나무의 횃불화·수관화의 전파 분류·지표화 의존성은 사건 맥락으로 별도 기록한다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F081 이탄·지중 연료의 국소 연기

분류: observable. 연결 용어: 지중화 · 이탄 화재 · Ground fire · Peat fire.

- organic_ground: a declared organic ground or peat surface
- smoke_outlet: a localized smoke outlet in that surface
- char_patch: a dark affected region adjoining the outlet

관계: organic_ground → emits → smoke_outlet.

경계: 지하 연소의 깊이·지속 시간은 표면 연기만으로 확정하지 않는다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm), [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F082 낮은 연료와 수관을 잇는 사다리 연료

분류: observable. 연결 용어: 사다리 연료 · Ladder fuels.

- low_fuel: a low fuel layer around a tree
- intermediate_fuel: shrubs or branches bridging the vertical gap
- canopy: the same tree's higher crown above the bridge

관계: intermediate_fuel → connects → low_fuel; intermediate_fuel → connects → canopy.

경계: 세로 연결이 핵심이다. 사다리 도구나 연속 불기둥을 반드시 추가하지 않는다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F083 본 화선과 떨어진 비화점

분류: observable. 연결 용어: 비화 · 비화점 · Spotting · Spot fire.

- main_fire: a declared main fire front
- unburned_gap: unburned space separating two fire regions
- secondary_fire: a smaller active fire beyond that gap

관계: unburned_gap → separates → main_fire; unburned_gap → separates → secondary_fire.

경계: 두 불의 외형만으로 실제 비화 인과를 확정하지 않는다. 사건 문맥이 인과를 소유한다.

근거: [S07 NWCG Firebrand](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/firebrand-82), [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F084 회전축을 가진 화염 회오리 외관

분류: observable. 연결 용어: 화염 회오리 · Fire whirl.

- base_fire: a coherent source fire at ground level
- vortex_column: a narrowing or spiraling column above that source
- entrained_material: smoke or fragments arranged around the column axis

관계: base_fire → feeds → vortex_column; vortex_column → carries → entrained_material.

경계: 일반 불기둥·토네이도·소용돌이 불티 배열을 같은 현상으로 판정하지 않는다.

근거: [S08 NWCG Fire whirl](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/fire-whirl-86).

### F085 연기 플룸 위 응결된 화재 구름

분류: observable. 연결 용어: 화재적운 · 화재적란운 · Pyrocumulus · Pyrocumulonimbus.

- fire_plume: a smoke plume rooted at a large declared fire
- cloud_base: a condensate cloud forming above the plume
- cloud_top: a coherent towering upper cloud connected to that base

관계: fire_plume → rises_into → cloud_base; cloud_base → supports → cloud_top.

경계: 모든 큰 검은 연기·모든 구름이 화재적란운은 아니다. 번개·성층권 도달을 필수화하지 않는다.

근거: [S10 Bureau of Meteorology How fires make thunderstorms](https://www.bom.gov.au/resources/learn-and-explore/fire-weather-knowledge-centre/how-fires-make-thunderstorms).

### F086 화재 뒤 식생과 탄화 흔적의 공존

분류: observable. 연결 용어: 화재 후 재생 · Post-fire regeneration.

- charred_stem: a charred tree or stem rooted in the landscape
- new_growth: new green growth rooted near that same burned area
- substrate: the shared ground supporting both states

관계: charred_stem → shares_ground_with → new_growth.

경계: 초록 식생 한 장이 특정 적응·종자 발아 기작·회복 기간을 증명하지 않는다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F087 나이테에 남은 화재 흉터의 외관

분류: observable. 연결 용어: 화재 흔적 나이테 · Fire scar.

- cross_section: one readable wood cross section
- growth_rings: concentric growth ring structure
- scar: a localized disrupted region within those rings

관계: scar → interrupts → growth_rings.

경계: 사진만으로 발생 연도·빈도·원인을 확정하지 않는다. 실제 시료의 해석 맥락을 보존한다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm).

### F088 연료 수분·화재 체제·계획소각의 맥락

분류: context. 연결 용어: 화재 기상 · 연료 수분 · 화재 체제 · 화재 적응 · 계획소각.

수분·빈도·계절·관리 목적은 다른 축이다. 계획소각도 외형만으로 자연 산불과 구별되지 않을 수 있다.

경계: 건조한 풀 외관이 수분 함량·법적 승인·통제 상태를 증명하지 않는다.

근거: [S09 NWCG FI-210 Glossary](https://training.nwcg.gov/pre-courses/FI210/html/nifc___full_main_p206.htm), [S10 Bureau of Meteorology How fires make thunderstorms](https://www.bom.gov.au/resources/learn-and-explore/fire-weather-knowledge-centre/how-fires-make-thunderstorms).

## 연료와 생활

### F089 장작 더미와 가는 불쏘시개의 크기 차이

분류: observable. 연결 용어: 장작 · 땔감 · 불쏘시개 · 부싯깃.

- firewood: recognizable larger wood pieces
- kindling: thinner twigs or splints beside those pieces
- support: one coherent storage or fire preparation surface

관계: kindling → beside → firewood.

경계: 형태 차이는 용도 후보를 돕는다. 모든 재료가 실제 점화됐거나 젖지 않았다고 하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F090 화로 안 숯과 발광 부위

분류: observable. 연결 용어: 숯 · 숯불 · 화로 · Brazier.

- brazier: a bounded open heat holding vessel
- charcoal: irregular charcoal pieces inside that vessel
- glow: localized red glow within the same charcoal bed

관계: brazier → contains → charcoal; glow → belongs_to → charcoal.

경계: 숯불은 큰 화염을 반드시 동반하지 않는다. 숯·석탄·코크스의 화학 동치를 만들지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F091 연료 종류와 재료 식별의 경계

분류: context. 연결 용어: 석탄 · 코크스 · Charcoal · Coal · Coke.

연료 종류는 재료·생산 과정·요청 맥락으로 유지한다. 검고 다공성이라는 외관만으로 종류를 확정하지 않는다.

경계: 검은 연료 덩어리를 전부 숯으로 통합하거나 생산 이력을 픽셀로 판정하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S02 NIST Pyrolysis](https://www.nist.gov/glossary-term/30146).

### F092 촛농의 흘러내림과 굳은 층

분류: observable. 연결 용어: 촛농 · Melted candle wax · 촛대.

- candle: one recognizable wax candle
- wax_runnel: a continuous wax runnel down its side
- wax_deposit: a thicker wax deposit at the runnel's lower end

관계: wax_runnel → belongs_to → candle; wax_runnel → feeds → wax_deposit.

경계: 액체 왁스·굳은 왁스·원래 양초 표면을 구별하며 온도를 외관으로 확정하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F093 등잔의 용기와 심지

분류: observable. 연결 용어: 등잔 · Oil lamp.

- oil_lamp: a bounded fuel holding lamp body
- wick: a wick emerging from its spout or opening
- flame: a small flame attached to that same wick

관계: oil_lamp → supports → wick; wick → anchors → flame.

경계: 전구·촛대·램프워킹 장치와 다르다. 역사적 유종·시대는 전용 출처가 필요하다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F094 손잡이 위 연료가 타는 횃불

분류: observable. 연결 용어: 횃불 · Torch.

- torch: one graspable shaft or declared torch body
- fuel_head: a bounded burning head at its upper end
- flame: flames attached to that head

관계: torch → supports → fuel_head; fuel_head → anchors → flame.

경계: 토치 공구·성화·의례 횃불의 용도를 자동 혼합하지 않는다.

근거: [S37 IOC Olympic Torch Relay Reference](https://library.olympics.com/default/digitalCollection/DigitalCollectionInlineDownloadHandler.ashx?_cb=20201210144919&documentId=171885&parentDocumentId=171884).

### F095 벽난로 화구와 장작·굴뚝

분류: observable. 연결 용어: 벽난로 · 굴뚝 · Fireplace · Chimney.

- hearth_opening: a readable bounded fireplace opening
- fuel_bed: burning or glowing fuel inside that opening
- flue_direction: a coherent upper cavity or chimney path above the fuel

관계: hearth_opening → contains → fuel_bed.

경계: 굴뚝 존재가 배출 정상·무연·실내 안전을 증명하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F096 한국 전통 부엌의 아궁이와 솥

분류: observable. 연결 용어: 아궁이 · 부뚜막 · Firebox.

- firebox: a low fuel opening in a hearth platform
- platform: a continuous raised cooking platform around that opening
- pot: a cooking vessel seated above the same heating cavity

관계: platform → contains → firebox; firebox → below → pot.

경계: 화로·서양 벽난로와 다른 공간 연결이다. 모든 한국 부엌을 한 시대의 형태로 고정하지 않는다.

근거: [S35 National Folk Museum 한국인은 밥심으로 산다](https://webzine.nfm.go.kr/2016/02/29/한국인은-밥심으로-산다/).

### F097 풀무 출구와 화덕의 연결

분류: observable. 연결 용어: 풀무 · Bellows · 대장간 화덕.

- bellows: a recognizable bellows body
- outlet: a nozzle connected to that body
- forge: the same fire bed toward which the outlet is directed

관계: bellows → connected_to → outlet; outlet → directed_at → forge.

경계: 별도 인물·다른 화덕으로 출구를 옮기지 않는다. 모든 단조 장면에 풀무를 필수화하지 않는다.

근거: [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

### F098 부지깽이 끝이 닿는 같은 연료

분류: observable. 연결 용어: 부지깽이 · Fire poker.

- fire_poker: one continuous long handled fire tool
- contact_tip: its visible tip inside the declared fire bed
- fuel_piece: the same fuel piece being contacted by that tip

관계: fire_poker → contacts → fuel_piece.

경계: 도구 소유자와 접촉 대상이 같은 프레임에서 읽혀야 한다. 검이나 지팡이로 치환하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F099 부싯돌 접촉점에서 나온 불티

분류: observable. 연결 용어: 부싯돌 · Fire-striking stone.

- striking_pair: two declared striking objects held together
- contact_point: one readable meeting point between them
- sparks: small luminous particles localized at that point

관계: contact_point → emits → sparks.

경계: 부싯돌만 손에 든 장면은 점화 성공 증거가 아니다. 제조·재료 조합 지침은 포함하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html), [S32 ACS Omega Customizing the Appearance of Sparks](https://pubs.acs.org/doi/10.1021/acsomega.2c03081).

## 공예와 산업

### F100 가마 입구와 안쪽 작업물

분류: observable. 연결 용어: 가마 · 노 · 용광로 · 소성.

- chamber: one bounded kiln or furnace interior
- opening: a visible opening into that same chamber
- workpiece: a declared workpiece or charge inside it

관계: chamber → contains → workpiece.

경계: 가마·제철로·서냉로의 공정 목적과 온도는 별도 문맥이며 동일 장비로 합치지 않는다.

근거: [S16 Corning Museum Flameworking](https://glassmaking.cmog.org/flameworking), [S17 Corning Museum Annealing](https://allaboutglass.cmog.org/definition/annealing).

### F101 도가니에서 주형으로 이어지는 쇳물

분류: observable. 연결 용어: 도가니 · 쇳물 · 주조 · 슬래그.

- crucible: a bounded vessel holding declared molten metal
- pour_stream: a coherent liquid stream from its lip
- mold: the same receiving mold beneath the stream

관계: crucible → emits → pour_stream; pour_stream → enters → mold.

경계: 발광·유동은 화염의 증거가 아니다. 금속 종류·슬래그 조성은 외형으로 확정하지 않는다.

근거: [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

### F102 망치·모루·가열 금속의 단조 접촉

분류: observable. 연결 용어: 단조 · Forging · 대장간 화덕.

- workpiece: a continuous heated metal piece resting on an anvil
- hammer: a hammer aligned with one region of that piece
- contact_region: a readable same piece impact region

관계: hammer → contacts → workpiece; workpiece → rests_on → anvil.

경계: 장식용 망치·독립 불꽃·주조 붓기와 다르다. 불티는 모든 단조에 필수가 아니다.

근거: [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

### F103 담금질·뜨임·풀림의 공정 경계

분류: context. 연결 용어: 담금질 · 뜨임 · 풀림 · Quenching · Tempering · Annealing.

가열·냉각 이력과 재료 성질의 차이는 공정 맥락으로 둔다. 이번에 확인한 유리 서냉 정의를 모든 금속 열처리의 정의로 확대하지 않는다.

경계: 수조·증기 한 장으로 담금질을 확정하지 않는다. 금속 열처리 전용 출처 확인 뒤 추가 승격한다.

근거: [S17 Corning Museum Annealing](https://allaboutglass.cmog.org/definition/annealing), [S18 V&A Guide to metalworking techniques](https://www.vam.ac.uk/articles/metalworking-techniques).

### F104 용접 접점과 용융 풀·불티

분류: observable. 연결 용어: 용접 · 용접 불꽃 · Welding sparks.

- tool: a declared welding tool directed at a metal joint
- joint: a localized bright work region on that same joint
- sparks: separate luminous particles leaving the work region when requested

관계: tool → directed_at → joint; joint → emits → sparks.

경계: 아크광·가스 화염·고체 불티를 한 물질로 합치지 않는다. 공정별 발생 여부는 전용 출처 확인이 필요하다.

근거: [S32 ACS Omega Customizing the Appearance of Sparks](https://pubs.acs.org/doi/10.1021/acsomega.2c03081), [S42 TWI What is Arc Welding](https://www.twi-global.com/technical-knowledge/faqs/what-is-arc-welding).

### F105 블로파이프 끝의 유리 덩어리

분류: observable. 연결 용어: 유리 불기 · Glassblowing.

- blowpipe: one continuous pipe held by the glassworker
- glass_gather: a hot glass gather attached to its far end
- tool_contact: a declared shaping tool contacting that same gather if present

관계: glass_gather → attached_to → blowpipe.

경계: 용융 유리와 화염을 구별하며 관 끝과 유리 덩어리를 분리하지 않는다.

근거: [S41 Corning Museum Glass Dictionary Blowing](https://allaboutglass.cmog.org/glass-dictionary/b).

### F106 토치 앞에서 가공하는 유리 막대

분류: observable. 연결 용어: 램프워킹 · Lampworking · Flameworking.

- torch: a declared fixed flame source
- glass_rod: a continuous glass rod directed into the flame region
- softened_region: a localized softened section of the same rod

관계: torch → heats → glass_rod.

경계: 유리 불기·유리 서냉과 다른 장면이다. 별도 유리를 공중에 복제하지 않는다.

근거: [S16 Corning Museum Flameworking](https://glassmaking.cmog.org/flameworking).

### F107 나무 표면과 열 펜의 낙화 흔적

분류: observable. 연결 용어: 낙화 · Pyrography.

- wood_surface: one readable wood grain surface
- heated_tip: a declared hot drawing tip meeting that surface
- dark_mark: a localized dark line adjoining that same tip

관계: heated_tip → contacts → wood_surface; dark_mark → belongs_to → wood_surface.

경계: 검은 잉크·음각·전체 탄화와 다른 선택적 실현이다. 제작 공정은 추가 전문 출처 대상이다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F108 가스 플레어 스택 끝의 화염

분류: observable. 연결 용어: 가스 플레어링 · Gas flaring.

- stack: one readable elevated industrial stack
- tip: a bounded outlet at its upper end
- flame: a flame physically attached to that tip

관계: stack → supports → tip; tip → emits → flame.

경계: 태양 플레어·렌즈 플레어·비상 신호탄과 다른 소유자다. 굴뚝 사고로 자동 해석하지 않는다.

근거: [S40 EPA AP-42 Industrial Flares](https://www.epa.gov/sites/default/files/2020-10/documents/13.5_industrial_flares.pdf).

### F109 화염 연마와 소재 변화의 한계

분류: context. 연결 용어: 화염 연마 · Flame polishing.

토치 근처 표면과 최종 매끄러움은 보일 수 있으나 전후 변화·정확한 연마 공정은 시간 맥락이 필요하다.

경계: 모든 매끄러운 유리를 화염 연마로 분류하지 않는다. 전문 공정 출처를 추가 확인한다.

근거: [S16 Corning Museum Flameworking](https://glassmaking.cmog.org/flameworking), [S17 Corning Museum Annealing](https://allaboutglass.cmog.org/definition/annealing).

## 요리와 향미

### F110 열원 위 식재료와 석쇠

분류: observable. 연결 용어: 직화 · 숯불구이 · 장작구이 · 그릴링 · 로스팅.

- heat_source: a declared charcoal wood or flame heat source
- grate: a coherent cooking support above that source
- food: recognizable food resting on that support

관계: heat_source → below → grate; food → rests_on → grate.

경계: 구이·로스팅 방식은 문맥이다. 모든 구이에 큰 화염이나 동일한 줄무늬를 필수화하지 않는다.

근거: [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html), [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F111 갈변된 음식 표면

분류: observable. 연결 용어: 시어링 · 토스팅 · 마이야르 반응.

- food: one recognizable food piece
- browned_patch: a brown surface region on that same food
- interior_or_adjacent: an adjoining lighter or otherwise distinct region of the food

관계: browned_patch → belongs_to → food.

경계: 갈색 외형만으로 마이야르·캐러멜화·소스·탄화 중 기작을 확정하지 않는다.

근거: [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html).

### F112 갈변과 구별되는 검게 탄 부위

분류: observable. 연결 용어: 차링 · Charring · 그을린 풍미.

- food: one readable food piece
- char_patch: a localized blackened rough region
- uncharred_patch: recognizable adjacent food texture on the same piece

관계: char_patch → belongs_to → food.

경계: 검은 양념·김·검은 식재료와 구별한다. 쓴맛이나 안전성을 픽셀로 판정하지 않는다.

근거: [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F113 음식과 연결된 훈연 맥락

분류: observable. 연결 용어: 훈연 · Smoking · 훈연향.

- food: recognizable food within a declared smoking setting
- smoke_path: smoke passing through the same food space
- smoke_source: a coherent source feeding that smoke path

관계: smoke_source → emits → smoke_path; smoke_path → passes_by → food.

경계: 연기 존재만으로 보존·향미·숙성·익힘 완료를 주장하지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr), [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html).

### F114 팬 위 증기에서 일어나는 플람베

분류: observable. 연결 용어: 플람베 · Flambé.

- pan: a readable cooking pan
- food_region: food or sauce in that same pan
- flame: a flame envelope immediately above the pan contents

관계: flame → above → food_region; food_region → inside → pan.

경계: 음식 고체 자체 연소·토치 화염·주방 전체 화재로 바꾸지 않는다.

근거: [S39 RSC Flames in the kitchen](https://edu.rsc.org/download?ac=509309).

### F115 토치 끝과 음식 표면의 마감 부위

분류: observable. 연결 용어: 토치 마감 · Torch finishing.

- torch: a handheld culinary torch
- flame_tip: a short flame aligned toward one food patch
- browned_patch: the same food patch beneath that flame tip

관계: torch → emits → flame_tip; flame_tip → directed_at → browned_patch.

경계: 도구 방향과 목표 부위의 소유를 유지한다. 피부·다른 음식에 화염을 이전하지 않는다.

근거: [S39 RSC Flames in the kitchen](https://edu.rsc.org/download?ac=509309), [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F116 솥바닥 형태가 남은 누룽지

분류: observable. 연결 용어: 누룽지 · Scorched rice.

- rice_grains: recognizable cooked rice grains
- crust: a connected browned rice layer
- pot_shape: a curvature or edge corresponding to the declared pot base

관계: crust → made_of → rice_grains.

경계: 검은 재·일반 크래커와 구별하며 누룽지를 완전 탄화의 동의어로 쓰지 않는다.

근거: [S35 National Folk Museum 한국인은 밥심으로 산다](https://webzine.nfm.go.kr/2016/02/29/한국인은-밥심으로-산다/), [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html).

### F117 반응·향미·웍헤이의 의미 경계

분류: context. 연결 용어: 마이야르 반응 · 캐러멜화 · 불향 · 웍헤이.

마이야르·캐러멜화는 다른 반응 축이다. 불향·웍헤이는 여러 감각과 조리 맥락을 포괄할 수 있으며 단일 표면 무늬가 아니다.

경계: 팬에서 화염이 솟는 장면을 웍헤이의 필요충분 조건으로 등록하지 않는다. 전문 향미 자료 추가 조사 대상이다.

근거: [S19 ACS Tasty Culinary Chemistry](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html), [S39 RSC Flames in the kitchen](https://edu.rsc.org/download?ac=509309).

## 태양과 우주기상

### F118 관측 방식이 명시된 태양 원반

분류: observable. 연결 용어: 태양 · 항성 · 태양 원반 · 태양 가장자리.

- solar_disk: one coherent circular solar disk
- limb: a bounded edge enclosing that same disk
- observation: a declared visible light solar observation context

관계: limb → bounds → solar_disk.

경계: 태양은 핵융합 별이다. 지상의 장작 화염·공중 화구와 동치로 저장하지 않는다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/).

### F119 광구의 쌀알무늬

분류: observable. 연결 용어: 광구 · 쌀알무늬 · Granulation.

- photosphere: a declared resolved photospheric surface
- granules: a cellular pattern of brighter surface patches
- intergranular_lanes: darker lanes between those patches

관계: intergranular_lanes → separate → granules.

경계: 픽셀 해상도·관측 대역이 필요하다. 일반 주황색 피부·대륙 표면·노이즈로 대신하지 않는다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/).

### F120 흑점의 어두운 중심과 주변부

분류: observable. 연결 용어: 흑점 · Sunspot.

- photosphere: a resolved brighter photospheric surface
- umbra: a dark localized sunspot core
- penumbra: a structured less dark region adjoining that core

관계: penumbra → surrounds → umbra.

경계: 모든 흑점에 같은 주변부를 필수화하지 않는다. 이 카드는 주변부가 보이는 흑점의 선택적 실현이다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/), [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/).

### F121 백반의 국소 밝은 광구 영역

분류: observable. 연결 용어: 백반 · Facula.

- photosphere: a declared visible light photospheric region
- bright_patch: a localized bright surface patch
- surroundings: adjacent photospheric texture bounding that patch

관계: bright_patch → belongs_to → photosphere.

경계: 플레어·렌즈 고스트·화염색으로 대신하지 않는다. 식별에는 관측 맥락을 유지한다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/).

### F122 관측 영역과 대역별 태양 대기

분류: context. 연결 용어: 채층 · 전이영역 · 코로나 · Chromosphere · Corona.

광구·채층·전이영역·코로나는 다른 층이다. 일식·필터·EUV 등 관측 맥락과 교재 단면도를 분리한다.

경계: 태양 원반을 확대했다고 내부 핵·모든 대기층이 동시에 보인다고 하지 않는다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/), [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/), [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

### F123 태양 가장자리 밖 홍염

분류: observable. 연결 용어: 홍염 · 분출 홍염 · Solar prominence.

- solar_limb: a coherent solar limb edge
- prominence: a looped or arching plasma structure extending beyond that edge
- attachment: legible contact regions between the structure and the solar limb

관계: prominence → extends_from → solar_limb.

경계: 홍염은 모든 태양 플레어의 동의어가 아니다. 분출·지속 시간은 한 장으로 확정하지 않는다.

근거: [S21 NASA What is a solar prominence](https://www.nasa.gov/image-article/what-solar-prominence/), [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

### F124 태양 원반 위 어두운 필라멘트

분류: observable. 연결 용어: 필라멘트 · Solar filament.

- solar_disk: a coherent observed solar disk
- filament: an elongated dark structure against the brighter disk
- continuity: a readable continuous filament path within that disk

관계: filament → against → solar_disk.

경계: 홍염과 관측 배경의 차이를 보존한다. 렌즈·의복·전구 필라멘트와 동음어다.

근거: [S21 NASA What is a solar prominence](https://www.nasa.gov/image-article/what-solar-prominence/).

### F125 같은 태양 표면을 잇는 코로나 루프

분류: observable. 연결 용어: 코로나 루프 · 코로나 아케이드.

- solar_surface: a declared observed solar region
- loop: a curved luminous plasma structure above that region
- footpoints: two coherent footpoint regions on the same solar surface

관계: loop → connects → footpoints.

경계: 자기장 선 자체가 가시광 철사로 보인다고 하지 않는다. 지상 불의 고리와 다른 소유다.

근거: [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/), [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

### F126 활동 영역의 국소 밝은 플레어 외관

분류: observable. 연결 용어: 태양 플레어 · Solar flare.

- solar_disk: a declared solar observation
- active_region: a localized active region within that disk
- brightening: a concentrated bright emission patch in that same region

관계: brightening → belongs_to → active_region.

경계: 단일 밝은 점이 시간적 에너지 폭발을 확정하지 않는다. 파장·영상 배색·시점을 맥락으로 둔다.

근거: [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/), [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

### F127 코로나그래프의 넓은 CME 전면

분류: observable. 연결 용어: 코로나 질량 방출 · CME.

- occulting_disk: an opaque observing disk masking the solar center
- outer_corona: a faint outer corona around that registered center
- ejection_front: a broad asymmetric plasma front beyond the disk

관계: occulting_disk → masks → solar_center; ejection_front → within → outer_corona.

경계: 이것은 코로나그래프 실현이다. 모든 CME 요청에 원반 차폐를 정의상 강요하지 않는다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/), [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/).

### F128 EUV 영상의 어두운 코로나 구멍

분류: observable. 연결 용어: 코로나 구멍 · Coronal hole.

- solar_disk: a declared EUV solar image
- dark_region: a broad lower brightness coronal region
- surroundings: brighter observed corona surrounding that region

관계: dark_region → belongs_to → corona_observation.

경계: 태양 표면의 실제 구멍·흑점·검은 물체로 바꾸지 않는다.

근거: [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/), [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

### F129 태양 내부·자기장·태양풍의 비가시적 경계

분류: context. 연결 용어: 핵융합 · 플라스마 · 태양 핵 · 복사층 · 대류층 · 자기 재연결 · 태양풍.

내부 층·핵반응·자기 연결·지속적인 입자 흐름은 계측·이론·교육 도식의 정보다. 사진형 후보와 단면도 후보를 분리한다.

경계: 빨간 화염·마법 선·굴뚝 연기를 관측 사실로 쓰지 않는다.

근거: [S20 NASA Sun Facts](https://science.nasa.gov/sun/facts/), [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/).

### F130 EUV 파장에 배정된 태양 영상색

분류: observable. 연결 용어: 태양 · 청색 화염 · 녹색 화염 · 보라색 화염.

- solar_image: one declared solar observation image
- channel: a declared EUV channel for that image
- color_table: a consistent assigned display color across the same channel

관계: color_table → maps → channel.

경계: SDO의 배색을 육안 태양색·화학 불꽃색·보편적 온도색으로 취급하지 않는다.

근거: [S23 NASA Slices of the Sun](https://science.nasa.gov/resource/slices-of-the-sun/).

## 카메라 광학

### F131 광원 방향으로 번지는 베일형 플레어

분류: observable. 연결 용어: 렌즈 플레어 · Veiling glare · Flare.

- light_source: one declared bright source entering the camera path
- image_plane: a luminous veil across the captured image toward that source
- scene_detail: reduced contrast in detail behind the veil

관계: light_source → causes_artifact_on → image_plane.

경계: 공간의 실제 연무·화염막·전역 주황색 색보정과 다르다.

근거: [S24 ZEISS Reduction of reflections for camera lenses](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-about-the-reduction-of-reflections-for-camera-lenses.pdf).

### F132 광원과 정렬된 분리 플레어 고스트

분류: observable. 연결 용어: 고스트 플레어 · Ghost images · 렌즈 플레어.

- light_source: one declared bright optical source
- ghost_shapes: separate translucent optical shapes aligned with that source
- scene: physical scene objects continuing behind those shapes

관계: ghost_shapes → overlay → image_plane; ghost_shapes → aligned_with → light_source.

경계: 불티·행성·독립 광원·물방울로 공간 객체화하지 않는다.

근거: [S24 ZEISS Reduction of reflections for camera lenses](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-about-the-reduction-of-reflections-for-camera-lenses.pdf).

### F133 광원 중심을 지나는 수평 플레어

분류: observable. 연결 용어: 아나모픽 플레어 · Horizontal flare streak.

- light_source: one declared bright optical source
- streak: a thin horizontal luminous line through that source
- scene_edges: other scene edges remaining coherent around the streak

관계: streak → passes_through → light_source.

경계: 수평 줄 하나가 렌즈 종류·실제 빛 기둥·화염 제트를 증명하지 않는다. 기존 후보를 우선 재사용한다.

근거: [S24 ZEISS Reduction of reflections for camera lenses](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-about-the-reduction-of-reflections-for-camera-lenses.pdf).

### F134 점광원 중심의 회절 별모양

분류: observable. 연결 용어: 선스타 · Sunstar · Starburst.

- point_source: a small bright source in the frame
- rays: several narrow luminous rays centered on it
- scene: a coherent physical scene behind the optical rays

관계: rays → centered_on → point_source.

경계: 광선은 태양 플레어·불티·폭발이 아니다. 모든 태양 사진에 회절별을 필수화하지 않는다.

근거: [S25 Nikon Bright Idea Adding Star Power](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-idea-adding-star-power).

### F135 할레이션·블룸·포화의 소유 경계

분류: context. 연결 용어: 할레이션 · Halation · Bloom · Highlight clipping.

필름층 산란·디지털 블룸·포화·렌즈 내부 반사는 발생 경로가 다르다. 이번에는 기존 editing 데이터와 용어를 재검토하며 신규 정의 승격은 보류한다.

경계: 광원 주변의 모든 빛 번짐을 렌즈 플레어라고 분류하지 않는다.

근거: [S24 ZEISS Reduction of reflections for camera lenses](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-about-the-reduction-of-reflections-for-camera-lenses.pdf), [S25 Nikon Bright Idea Adding Star Power](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-idea-adding-star-power).

## 불처럼 보이는 비연소 현상

### F136 용암의 액체 발광과 식은 외피

분류: observable. 연결 용어: 용암 · Lava · 불꽃 폭포.

- lava_flow: a connected declared molten rock flow
- crust: a darker solidifying crust on that flow
- luminous_gaps: red orange luminous gaps within the same crust

관계: crust → covers → lava_flow.

경계: 용암은 용융 암석이다. 주황색 발광만으로 화학적 연소 화염을 추가하지 않는다.

근거: [S27 USGS Lava is not fire](https://www.usgs.gov/news/volcano-watch-lavas-not-fire).

### F137 하늘을 가르는 밝은 유성 화구

분류: observable. 연결 용어: 유성 화구 · Bolide · Fireball.

- sky: one coherent atmospheric sky
- bright_head: a localized bright meteor event head
- trail: a luminous trail linked to the same head

관계: trail → connected_to → bright_head.

경계: 보케·태양 원반·공중 연료 폭발·매달린 신호탄과 다르다. 단일 이미지가 물체 조성을 확정하지 않는다.

근거: [S28 NASA Looking for Lightning Finding Fireballs](https://science.nasa.gov/earth/earth-observatory/looking-for-lightning-finding-fireballs-149381/).

### F138 뾰족한 구조물 끝의 세인트엘모 방전

분류: observable. 연결 용어: 세인트엘모의 불 · St. Elmo's fire.

- pointed_structure: a readable mast or other pointed object
- discharge_glow: a localized blue violet glow at its tip
- object_body: the intact structure beneath that glow

관계: discharge_glow → at_tip_of → pointed_structure.

경계: 대기 전기 방전이다. 연료가 타는 불·낙뢰 줄기·손상된 구조물로 자동 해석하지 않는다.

근거: [S26 NOAA Weird Ocean Phenomena](https://oceanservice.noaa.gov/ocean/weird-ocean-weather.html).

### F139 하늘의 오로라 커튼

분류: observable. 연결 용어: 오로라 · Aurora · 태양풍.

- night_sky: one coherent night sky above a horizon
- auroral_bands: extended luminous bands or curtains within that sky
- stars: background star points distinguishable from the bands

관계: auroral_bands → within → upper_atmosphere.

경계: 태양풍 자체의 가시 사진·지상 화염 커튼·대기 화재로 저장하지 않는다.

근거: [S22 NASA Heliophysics Vocabulary](https://science.nasa.gov/heliophysics/resources/vocabulary/).

## 문화와 판타지

### F140 Nataraja 조각의 불 도상 후광

분류: observable. 연결 용어: 불의 고리 · Agni · 불의 후광.

- sculpture: a declared Nataraja sculpture
- halo: a physical circular halo with flame shaped projections
- held_flame: the distinct flame motif held in the sculpture's hand

관계: halo → surrounds → sculpture; held_flame → held_by → sculpture.

경계: 금속 도상과 실제 연소를 구별한다. 단일 소장품의 의미를 모든 불 의례에 일반화하지 않는다.

근거: [S29 The Met Shiva as Lord of Dance 39328](https://www.metmuseum.org/art/collection/search/39328).

### F141 의례 맥락에 놓인 촛불 배열

분류: observable. 연결 용어: 봉헌초 · Votive candle · 성화 · 의례의 불.

- candle_array: several recognizable candles in a declared ritual setting
- flames: small flames rooted at their own wicks
- support: a coherent tray or altar surface supporting the candles

관계: support → supports → candle_array.

경계: 촛불 배열만으로 종교·동의·효험을 판정하지 않는다. 의례 판본별 출처 검토가 별도로 필요하다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html), [S29 The Met Shiva as Lord of Dance 39328](https://www.metmuseum.org/art/collection/search/39328).

### F142 향 끝의 연기와 소유 관계

분류: observable. 연결 용어: 향 · Incense · 훈소.

- incense_stick: a declared thin incense stick or cone
- tip: a localized dark or glowing emitting tip
- smoke_wisp: a narrow wisp connected to that same tip

관계: tip → belongs_to → incense_stick; tip → emits → smoke_wisp.

경계: 연기·형태 제안이다. 특정 신앙·향 성분·감각 효과·의례 절차를 외형에 넣지 않는다.

근거: [S11 NIST Smoke Production and Properties](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

### F143 두 횃불 사이 성화 전달

분류: observable. 연결 용어: 성화 · 성화 봉송 · Olympic flame.

- first_torch: one torch owned by an identifiable bearer
- second_torch: a second torch owned by the other bearer
- transfer_region: a coherent flame contact region between their heads

관계: first_torch → contacts → second_torch.

경계: 두 사람·두 도구의 소유를 보존한다. 실제 대회 판본·고대 연속성·브랜드를 임의 추가하지 않는다.

근거: [S37 IOC Olympic Torch Relay Reference](https://library.olympics.com/default/digitalCollection/DigitalCollectionInlineDownloadHandler.ashx?_cb=20201210144919&documentId=171885&parentDocumentId=171884).

### F144 몸의 형상이 화염으로 구성된 정령

분류: creative. 연결 용어: 불의 정령 · Fire elemental.

- body_silhouette: one readable declared creature silhouette
- flame_structure: connected flame forms composing that body
- scene_contact: a coherent ground or spatial relation for the creature

관계: flame_structure → composes → fictional_body.

경계: 창작 제안이다. 모든 불을 인물로 의인화하거나 특정 신화의 정식 외형으로 주장하지 않는다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.

### F145 불과 새 형상이 연결된 창작 불사조

분류: creative. 연결 용어: 불사조 · Phoenix.

- bird_body: one readable fictional bird body
- wings: paired wings connected to that same body
- flame_edges: declared flame forms integrated with its wing or tail edges

관계: wings → connected_to → bird_body; flame_edges → belong_to → fictional_bird.

경계: 보편적인 정전·역사적 판본을 주장하지 않는 창작 제안이다. 재생 서사는 단일 사진의 사실이 아니다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.

### F146 용의 입에서 이어지는 불길

분류: creative. 연결 용어: 화염 브레스 · Dragon breath.

- dragon: one readable declared dragon
- mouth: a coherent mouth opening on that dragon
- fire_jet: a connected flame jet issuing from the same opening

관계: mouth → belongs_to → dragon; mouth → emits → fire_jet.

경계: 머리 앞의 별도 화원·코의 불·분리된 레이저로 대상–출구 관계를 대체하지 않는다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.

### F147 지면 위 작은 판타지 도깨비불

분류: creative. 연결 용어: 도깨비불 · Will-o'-the-wisp · Ghost fire.

- ground: a declared ground or marsh setting
- small_lights: small separate floating luminous forms
- air_gap: a readable gap between lights and the ground

관계: small_lights → above → ground.

경계: 창작 외관이다. 자연 발생 원인·인 성분·실제 영혼·지역 민속 판본을 확정하지 않는다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.

## 신체와 재료 접촉

### F148 열원 가까이에 놓인 손의 위치 관계

분류: observable. 연결 용어: 불 쬐기 · Warming hands · 열기.

- heat_source: one declared heat source
- hands: hands owned by the same identifiable person
- gap: a visible separation between the hands and source

관계: hands → near → heat_source.

경계: 가까움은 실제 체감 온도·안전 거리·통증의 증거가 아니다. 접촉·화상을 자동 추가하지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

### F149 촛농이 놓인 피부 표면

분류: observable. 연결 용어: 촛농 · Wax play · 촛농 플레이.

- skin_patch: one explicitly selected skin region of a declared subject
- wax_deposit: a bounded wax deposit resting on that region
- contact_edge: a clear contact boundary between wax and the same skin

관계: wax_deposit → rests_on → selected_skin_patch.

경계: 촛농 접촉·성적 맥락·동의·통증·상해는 별개다. 왁스의 온도나 시술 안전성을 외형으로 확정하지 않는다.

근거: [S05 ACS Shining a Light on Candles](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

### F150 그을리고 구멍 난 의복의 같은 부위

분류: observable. 연결 용어: 불에 탄 옷 · Burned clothing · 탄화.

- garment: one declared garment owned by its wearer
- burned_edge: a localized blackened curled fabric edge
- opening: a missing fabric patch contiguous with that edge

관계: burned_edge → belongs_to → selected_garment_patch.

경계: 의복 손상을 추가 노출·신체 손상·성적 의미로 확대하지 않는다. opacity·coverage lock도 별도로 존중한다.

근거: [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

### F151 피부 손상과 임상·감각 판단의 경계

분류: context. 연결 용어: 화상 · 피부 수포 · 화상 흉터 · Burn · Scald.

피부의 색·수포·흉터 등 묘사는 요청 문맥에 보존하되 깊이·원인·발생 시점·통증·치료 상태를 사진으로 진단하지 않는다.

경계: 검댕을 화상으로, 그슬린 털을 깊은 피부 손상으로 바꾸지 않는다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics).

## 폭력 맥락

### F152 역사적 화염방사기의 도구–분사 연결

분류: observable. 연결 용어: 화염방사기 · Flamethrower · 소이 무기.

- carrier: an identifiable bearer of a declared historical flame tool
- nozzle: a discharge tool connected to its declared fuel pack
- fire_jet: a continuous flame issuing from that nozzle

관계: carrier → holds → nozzle; nozzle → emits → fire_jet.

경계: 역사적 객체 외형 제안이다. 제작·성능·사용 전술은 후보 데이터에 넣지 않는다.

근거: [S30 IWM First World War gallery large print guide](https://www.iwm.org.uk/sites/default/files/files/2023-10/first_world_war_large_print_guide.pdf).

### F153 요청된 대상 표면에 붙은 화염

분류: observable. 연결 용어: 불타는 신체 · Burning body · 화형.

- target: one identifiable explicitly requested target
- carrier_surface: the declared burning surface on that same target
- flame: flames visibly attached to that surface

관계: carrier_surface → belongs_to → target; carrier_surface → anchors → flame.

경계: 인물의 존재만으로 피해·화형을 활성화하지 않는다. 사망·통증·고의·가해자는 별도 요청 또는 사건 맥락이다.

근거: [S01 NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [S14 NIST OSAC Strengthening Fire and Explosion Investigation 2021](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf).

## 비유와 동기

### F154 분노·욕망·유혹·몰입의 불 비유

분류: context. 연결 용어: 불기 · 화세 · 맹화 · 열화 · 화마 · 불타는 사랑 · 불타는 욕망 · 불꽃 튀는 · 불같은 분노.

비유는 감정·갈등·끌림·몰입을 문맥으로 보존한다. 감정을 실현할 행위·관계·결과를 독립적으로 저술하며 물리적 불을 자동 추가하지 않는다.

경계: 강렬한 시선·붉은 조명만으로 성적 관심·동의·폭력 의도·진단을 확정하지 않는다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.

### F155 불에 대한 성적 관심과 방화 동기의 경계

분류: context. 연결 용어: Pyrophilia · 불 페티시 · 방화 · Arson.

불에 대한 성적 관심·방화 행위·방화 동기·임상 진단은 같은 의미가 아니다. 표현된 내용은 유지하고 정신 상태를 외관에서 추론하지 않는다.

경계: 불 주변 인물·흥분 표정·대형 화재를 동기·동의·진단의 사실 근거로 저장하지 않는다.

근거 수준: 연구자의 창작 제안 또는 문맥 분리 원칙. 특정 역사·과학·임상 정의의 검증으로 주장하지 않는다.


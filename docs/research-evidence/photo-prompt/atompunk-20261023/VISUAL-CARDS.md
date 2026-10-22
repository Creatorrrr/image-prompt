# 상세 시각 의미 카드

가시 실현은 연구자가 저술한 제안이다. 출처는 용어 또는 인접 맥락만 뒷받침하며 전체 장면의 고증·품질을 승인하지 않는다.

표의 성분과 방향 관계는 선택된 분기 전체의 검토 항목이다. 일부가 가려지면 부분 또는 관찰 불가이며 전체 통과가 아니다.

## E01 — A020

still / P0 / 역할 제안: prop, object_structure

두꺼운 정비 플랜지가 있는 밀폐 원통 용기에서 단열 배관이 뻗고 옆 랙에 바늘 계기가 모여 있다.

성분: vessel = A closed cylindrical vessel with heavy service flanges; pipe = Several insulated pipes terminating at the vessel; gauge = A separate rack of needle gauges

관계: pipe → terminates_at → vessel; gauge → beside → vessel

혼동 경계: 냉각탑은 원자로 그 자체가 아님; 일반 보일러와 외관 중첩

주장 한계: 이것은 저술한 외부 설비 제안;핵분열 작동·노심 형상·정확한 차폐 두께를 픽셀로 확정하지 않음

근거: [S02](https://www.eisenhowerlibrary.gov/research/online-documents/atoms-peace) (body_excerpt), [S05](https://www.energy.gov/ne/articles/cherenkov-radiation-explained) (body_excerpt)

## E02 — A022

proxy / P0 / 역할 제안: prop, object_structure

방사형 방열핀이 반복된 소형 전원통과 탐사 계측기가 양끝이 보이는 케이블로 연결된다.

성분: generator = A compact cylindrical power unit with repeated radial cooling fins; probe = A separate exploration instrument; cable = A visible cable with both ends exposed

관계: cable → joins → generator; cable → joins → probe

혼동 경계: RTG와 연쇄반응 원자로; 배터리와 냉각용 터빈

주장 한계: 핀의 외형만으로 동위원소·전력·연료를 입증하지 않음;선택한 RTG 실물 판본은 후속 확인

근거: [S04](https://science.nasa.gov/planetary-science/programs/radioisotope-power-systems/power-radioisotope-thermoelectric-generators/) (body_excerpt)

## E03 — A023

versioned / P1 / 역할 제안: prop, object_structure

전방에 객실이 있고 후방 동력부가 큰 낮고 긴 콘셉트카 축소모형이 전시대에 놓여 있다.

성분: model = A long low concept-car scale model with its cabin forward; rear = A bulky rear power-module housing behind the cabin; plinth = A museum display plinth

관계: model → rests_on → plinth; rear → behind_cabin_of → model

혼동 경계: 주행 가능한 핵자동차와 1958 3/8 모형; 현재 양산차

주장 한계: 유물 설명으로 모형 여부 확인;정확한 차체 윤곽·색·치수의 재현 승인은 원본 사진 확인 후

근거: [S06](https://www.thehenryford.org/collections/explore/artifact/278186) (body_and_object_metadata)

## E04 — A024

proxy / P1 / 역할 제안: prop, location

큰 단일 벨형 엔진이 시험 지지대 안에 고정되고 굵은 공급관이 엔진까지 이어진다.

성분: engine = A large single-bell engine mounted inside a test support frame; feed = Broad insulated feed pipes; console = A remote bank of physical control instruments; frame = A sturdy open engine-test support frame

관계: feed → terminates_at → engine; engine → inside → frame

혼동 경계: 핵열 추진과 핵펄스 추진; 유인우주선 Orion

주장 한계: 장면은 연구자가 제안한 시험 설비;내부 반응·연료·성능의 물리적 검증 아님

근거: [S07](https://www.nasa.gov/rocket-systems-area-nuclear-rockets/) (indexed_body_excerpt)

## E05 — A027, A028

still / P0 / 역할 제안: prop, relational_action

바늘 눈금이 있는 휴대 상자형 계측기와 분리형 프로브가 케이블로 연결되고 프로브는 밀폐 표본 가까이에 놓인다.

성분: meter = A portable box meter with a needle dial; probe = A separate handheld detector probe; cable = A flexible cable; sample = A sealed specimen container

관계: cable → joins → meter; cable → joins → probe; probe → held_near → sample

혼동 경계: 계수기와 개인 선량계; 계기 전체를 방사선 검출기로 단정

주장 한계: 수치·클릭음·검출 핵종·누적 피폭량은 외관만으로 확정하지 않음

근거: [S11](https://www.nrc.gov/facilities-safety/radiation-protection/radiation-and-its-health-effects/detecting-radiation) (indexed_body_excerpt)

## E06 — A028

proxy / P0 / 역할 제안: wearable_accessory, prop_placement

평범한 작업복의 성인 기술자 가슴에 작은 직사각형 모니터링 배지가 고정되어 있다.

성분: worker = An adult technician in plain workwear; badge = A small rectangular monitoring badge clipped at the chest

관계: badge → clipped_to_chest_of → worker

혼동 경계: 선량계 배지와 계수기 프로브; 신분증

주장 한계: 배지는 소품 외형의 제안;누적 선량·직업적 권한·안전성을 판정하지 않음

근거: [S12](https://remm.hhs.gov/radiation-dosimeters-dose-monitoring-worker-safety.htm) (indexed_excerpt)

## E07 — A029

still / P0 / 역할 제안: prop, ambient_particle

어두운 바닥과 투명 벽의 작은 상자 안쪽 낮은 층에 가늘고 불규칙한 흰 응결 궤적이 측면광을 받는다.

성분: chamber = A clear-sided chamber with a dark floor; tracks = Fine pale irregular condensation trails near the floor; lamp = A low side lamp

관계: tracks → inside → chamber; lamp → illuminates → tracks

혼동 경계: 안개상자와 거품상자; 공기 중 광선·별무늬

주장 한계: 입자 자체·핵종·궤적의 시간 변화를 사진으로 확정하지 않음

근거: [S10](https://www.iop.org/explore-physics/physics-around-you/understanding-surroundings/cloud-chamber) (body_and_indexed_excerpt)

## E08 — A030

still / P0 / 역할 제안: lighting, reflection_logic

깊은 투명 수조의 잠긴 구조물 가까이 청자색 빛이 국소적으로 모이고 수면 일부에 푸른 반사가 생긴다.

성분: pool = A deep clear-water pool with visible submerged structures; glow = A localized blue-violet glow underwater; reflection = A blue reflection along the adjacent water surface

관계: glow → below_water_surface_of → pool; reflection → on_surface_of → pool

혼동 경계: 방사성 물질 전체의 녹색 광채; 수조 위 안개·네온 조명

주장 한계: 색과 매질 배치를 평가;실제 방사선 현상·선량을 판정하지 않음

근거: [S05](https://www.energy.gov/ne/articles/cherenkov-radiation-explained) (body_excerpt)

## E09 — A031

versioned / P1 / 역할 제안: prop, prop_placement

열린 교육용 실험 키트 케이스의 칸마다 작은 계측기와 닫힌 표본병이 나뉘어 담겨 있다.

성분: case = An open compartmented educational kit case; instruments = Small boxed measuring instruments; vials = Closed specimen vials

관계: instruments → inside → case; vials → inside → case

혼동 경계: 현대 과학완구와 Gilbert 원자력 실험 세트; 실제 안전성

주장 한계: 정확한 구성품은 판본별 원본 확인 필요;방사성 내용물·안전성·아동 사용 적합성을 주장하지 않음

근거: [S49](https://www.energy.gov/lm/articles/holiday-toy-shopping-during-1950s-looked-bit-different-during-2020s) (indexed_body_excerpt)

## S01 — A033

versioned / P0 / 역할 제안: prop, object_structure

광택 구형 위성 몸체에서 네 개의 긴 채찍형 안테나가 뒤쪽으로 뻗는다.

성분: body = A polished spherical satellite body; antennas = Four long whip antennae trailing back from the body

관계: antennas → attached_to → body

혼동 경계: 다방향 전구 샹들리에; 인공위성처럼 보이는 임의 구체

주장 한계: 네 안테나 전체와 부착부를 확인;모형과 궤도 위 실물의 장소는 별도로 선언

근거: [S13](https://airandspace.si.edu/stories/editorial/sputnik-and-space-age) (indexed_body_excerpt)

## S02 — A034, A043

proxy / P1 / 역할 제안: wardrobe_style, garment_detail

성인 착용자의 몸을 감싼 두꺼운 수트에 관절 주름과 단단한 원형 목링, 소매에 이어지는 두꺼운 장갑이 보인다.

성분: wearer = An adult wearer; garment = A bulky enclosed suit with visible joint folds; collar = A rigid circular neck ring; gloves = Thick gloves joined to the sleeves

관계: garment → worn_by → wearer; collar → part_of → garment; gloves → join_sleeves_of → garment

혼동 경계: 은색 패션 수트와 기능성 압력복; 소련 우주복의 모든 판본

주장 한계: 국적·실제 우주비행 경력·특정 비행복 판본은 패치나 외형만으로 확정하지 않음

근거: [S24](https://journal.sciencemuseum.ac.uk/article/cosmonauts-birth-of-an-exhibition/) (body_excerpt)

## S03 — A006, A007, A008, A035

still / P0 / 역할 제안: prop, object_structure

뾰족하고 매끈한 로켓 아래쪽에 큰 후퇴형 핀이 붙고 넓은 핀 끝이 착륙면을 딛는다.

성분: rocket = A pointed smooth rocket body; fins = Large swept fins on the lower body; feet = The broad ends of the fins at a landing surface; ground = A flat landing surface

관계: fins → attached_to_lower_body_of → rocket; feet → touch → ground

혼동 경계: 현대 발사체·미사일·고딕 성당; 모든 raypunk가 핵동력이라는 추론

주장 한계: 이는 복고 SF 조형 제안;실제 추진·우주항행·정확한 공학적 적합성을 주장하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt), [S43](https://11bitstudios.com/games/the-invincible/) (publisher_synopsis)

## S04 — A036

still / P0 / 역할 제안: prop, object_structure

납작하고 넓은 원반형 기체의 중앙에 돔이 솟고 가장자리 아래로 짧은 착륙 다리가 내려온다.

성분: craft = A broad shallow disc-shaped craft; dome = A raised central dome; legs = Short landing legs below the rim

관계: dome → above_center_of → craft; legs → under → craft

혼동 경계: 비행접시와 접시형 건축; 접시 실루엣만으로 외계인 존재 판정

주장 한계: 비행·기원·탑승 종족은 외형만으로 확정하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt)

## S05 — A037

still / P1 / 역할 제안: prop, spatial_depth

닫힌 객실의 소형 이동체가 상층 발코니 착륙장 바로 위에 있고 바닥과 기체 사이의 공기 틈이 보인다.

성분: car = A compact enclosed passenger vehicle; pad = A landing pad on an upper-level balcony; gap = A clearly visible air gap below the vehicle

관계: car → above → pad; gap → between_car_and → pad

혼동 경계: 바퀴 달린 주차 차량; 원근 착시로 생긴 틈

주장 한계: 현재 공중 배치만 평가;부상 원리·비행속도·시간 전후를 확정하지 않음

근거: [S43](https://11bitstudios.com/games/the-invincible/) (publisher_synopsis)

## S06 — A038

proxy / P1 / 역할 제안: wearable_accessory, anatomical_connection

성인 조종사 등에 소형 프레임이 두 어깨끈과 허리띠로 고정되고 하단에 두 노즐이 아래를 향한다.

성분: wearer = An adult pilot; frame = A compact back-mounted flight frame; straps = Two shoulder straps and a waist belt; nozzles = Paired downward-pointing nozzles

관계: frame → strapped_to_back_of → wearer; straps → join → frame; nozzles → under → frame

혼동 경계: 등짐·스쿠버 탱크; 허공에 떠 있는 분리 장비

주장 한계: 실제 Bell 판본·추력·연료는 후속 자료 검증;단일 사진으로 지속 비행을 입증하지 않음

근거: [S24](https://journal.sciencemuseum.ac.uk/article/cosmonauts-birth-of-an-exhibition/) (body_excerpt)

## S07 — A039

still / P0 / 역할 제안: location, object_structure

분화구가 있는 메마른 지형 위 투명 거주 돔을 통해 낮은 생활 건물이 보인다.

성분: terrain = A barren cratered landscape; dome = A transparent habitation dome on the terrain; habitat = Low occupied structures visible through the dome

관계: habitat → inside → dome; dome → on → terrain

혼동 경계: 지오데식 골격과 기밀 압력돔; 지구 온실

주장 한계: 실제 달·기압·생명유지 성능은 외관만으로 확정하지 않음;실내외 광학 경계가 필요

근거: [S14](https://www.nasa.gov/reference/international-space-station/) (indexed_body_excerpt)

## S08 — A040, A041

still / P0 / 역할 제안: object_structure, spatial_depth

끊기지 않은 토러스형 거주 고리와 중앙 축 허브가 여러 방사형 연결부로 이어진다.

성분: ring = A continuous toroidal outer habitation ring; hub = A central axial hub; spokes = Several spokes joining the hub to the ring

관계: spokes → join → hub; spokes → join → ring

혼동 경계: 현재 ISS·평면 도넛 장식; 인공중력 발생기

주장 한계: 구조만 정지사진 평가;회전·인공중력은 연속 자료 또는 별도 허구 설정 필요

근거: [S14](https://www.nasa.gov/reference/international-space-station/) (indexed_body_excerpt)

## S09 — A042

still / P0 / 역할 제안: wearable_accessory, reflection_logic

성인 인물의 얼굴을 둥근 투명 셸이 감싸고 목의 단단한 밀폐링에 이어지며 셸 표면에 곡선 반사가 남는다.

성분: wearer = An adult figure with a visible face; helmet = A clear rounded helmet shell; ring = A firm neck seal ring; highlight = A curved highlight on the shell; face = The face of the same wearer

관계: face → inside → helmet; helmet → joined_to → ring; ring → around_neck_of → wearer

혼동 경계: 유리 볼을 든 인물·일반 고글; 헬멧 앞면의 불투명 얼굴 합성

주장 한계: 밀폐 성능·산소 공급은 증명되지 않음;얼굴·셸·목링이 같은 소유 관계여야 함

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## S10 — A044

still / P0 / 역할 제안: prop, object_structure

부푼 몸체 아래 손잡이가 붙고 동심 링이 반복된 점감형 총열 끝에 발사부가 구별된다.

성분: handle = A short grip attached to a bulbous weapon body; barrel = A tapered barrel with repeated concentric rings; tip = A distinct forward emitter; body = A bulbous weapon body

관계: barrel → attached_to → body; tip → at_front_of → barrel; handle → under → body

혼동 경계: 현대 총기·레이저 실험기; 핵에너지 무기라는 단정

주장 한계: 빔 효과는 별도 선택;분해·살상·원인·실제 무기 작동을 사진으로 증명하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt)

## S11 — A045

still / P1 / 역할 제안: surreal_physics_detail, reflection_logic

가장자리가 읽히는 반투명 곡면 바깥에는 파편이 있고 안쪽 표면은 흐트러지지 않은 상태다.

성분: barrier = A curved translucent boundary with a visible rim; outside = Airborne fragments outside the boundary; inside = An undisturbed interior surface

관계: outside → outside → barrier; inside → inside → barrier

혼동 경계: 유리 돔·발광 테두리; 전후 효과를 한 장에 몰아넣음

주장 한계: 현재의 분리 배치만 평가;보호 원리·충돌 사건·시간 인과는 별도 증거

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt)

## M01 — A046

still / P0 / 역할 제안: prop, object_structure

투명 전자관 안에 어두운 전극판과 작은 따뜻한 필라멘트가 있고 핀 베이스가 소켓에 꽂혀 있다.

성분: tube = A clear glass electronic tube; plates = Dark internal electrode plates; filament = A small warm filament at the base; socket = A pinned base seated in a socket

관계: plates → inside → tube; filament → inside → tube; socket → under → tube

혼동 경계: 닉시 숫자관·단순 전구; 모든 관 전체가 강하게 빛나는 연출

주장 한계: 선택한 관 형상만;증폭·발열·계산 방식은 외관만으로 확정하지 않음

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M02 — A047

proxy / P1 / 역할 제안: prop, object_structure

작은 밀폐 부품 밑면의 가는 리드가 성긴 초기 전자기판에 이어진다.

성분: package = A small sealed electronic package; leads = Thin leads emerging from its base; board = A sparse early electronic board

관계: leads → join → board; package → above → board

혼동 경계: 초기 점접촉 실험물과 후대 트랜지스터 패키지; 현대 IC

주장 한계: 1947 기록은 존재 시점의 근거;이 외형 제안의 연대·반도체 내부 기능은 판본 확인 전 미확정

근거: [S16](https://www.computerhistory.org/siliconengine/invention-of-the-point-contact-transistor/) (body_heading_and_indexed_metadata)

## M03 — A048, A050

still / P0 / 역할 제안: location, prop

높은 장비 캐비닛이 평행 통로를 만들고 물리적 패치·표시 패널 옆에 성인 운영자가 서 있다.

성분: cabinets = Tall equipment cabinets forming parallel aisles; operator = An adult operator beside the cabinets; panels = Physical patch and indicator panels

관계: panels → on → cabinets; operator → beside → cabinets

혼동 경계: 서버랙·단일 콘솔; 전자두뇌라는 이름으로 실제 지능 추론

주장 한계: 방 규모·사람 대비 크기만 평가;연산 방식·의식·통제 권한은 별도 문맥

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M04 — A049

proxy / P0 / 역할 제안: prop, object_structure

물리 계산 패널에 짧은 패치 케이블이 여러 소켓을 잇고 눈금 다이얼이 줄지어 있다.

성분: panel = A physical computing panel; patches = Many short cables joining labelled sockets; knobs = Rows of calibrated dials

관계: patches → join_sockets_on → panel; knobs → on → panel

혼동 경계: 다이얼 외관과 연속량 아날로그 계산; MONIAC와 전자 아날로그 장치

주장 한계: 패치형 장치는 한 실현 분기;모든 아날로그 계산기를 이 모습으로 통일하지 않음

근거: [S17](https://blog.sciencemuseum.org.uk/back-to-the-future-of-computing/) (indexed_body_excerpt)

## M05 — A051

still / P0 / 역할 제안: prop, object_structure

두꺼운 둥근 베젤과 깊은 캐비닛 안쪽에 볼록한 화면이 있고 아래에 작은 물리 조작부가 있다.

성분: screen = A convex display face recessed in a deep cabinet; bezel = A thick rounded frame; knobs = Small physical controls below the display; cabinet = A deep equipment cabinet

관계: screen → inside → bezel; bezel → part_of → cabinet; knobs → below → screen

혼동 경계: 얇은 평판·CRT와 동의어인 아날로그 컴퓨터

주장 한계: 내부 전자총·실제 화면 주사 방식은 이미지로 확인되지 않음

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M06 — A052

still / P0 / 역할 제안: prop, visible_text

계측기 화면의 가는 직교 눈금 위에 연속 파형이 보이고 옆에는 스케일 조작부가 있다.

성분: screen = A dark instrument screen; grid = A fine rectangular graticule; trace = A continuous pale waveform; knobs = Physical scale controls beside the screen

관계: trace → over → grid; grid → on → screen; knobs → beside → screen

혼동 경계: 레이더의 원형 스윕·TV 영상; 파형만으로 생체신호 판정

주장 한계: 오실로스코프 외형 제안;파형의 출처·주파수·진단은 판독 자료 없이 미확정

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M07 — A053

still / P0 / 역할 제안: prop, object_structure

투명 표시관 안쪽에 숫자 모양 전극들이 깊이 방향으로 겹치고 그중 한 숫자만 주황빛으로 켜진다.

성분: tube = A clear glass display envelope; digits = Several superimposed shaped numeral electrodes; lit = One orange-lit numeral

관계: digits → inside → tube; lit → one_of → digits

혼동 경계: 7세그먼트·LED·진공관 필라멘트; 겹친 숫자를 동시 발광시킴

주장 한계: 가스 종류·온도는 외형 판정 대상 아님;원본 수준에서 전극 층과 켜진 숫자를 함께 확인

근거: [S18](https://www.evilmadscientist.com/2007/nixie-tube-take-apart/) (firsthand_disassembly_excerpt)

## M08 — A054

still / P0 / 역할 제안: prop, surface_pattern

단단한 직사각형 카드에 작은 직사각형 구멍들이 행과 열의 격자에 맞춰 뚫려 있다.

성분: card = A stiff rectangular data card; holes = Small rectangular holes aligned in discrete rows and columns

관계: holes → pierce → card

혼동 경계: 키펀치 천공과 인쇄 점·장식 구멍

주장 한계: 실제 데이터·신원·명령 내용은 구멍 배열만으로 확정하지 않음;정확한 카드 규격은 별도

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M09 — A055

still / P0 / 역할 제안: prop, object_structure

한 장비 전면의 두 노출 릴 사이에 테이프가 중앙 헤드 블록을 거쳐 이어진다.

성분: left_reel = An exposed tape reel on the left of one equipment face; right_reel = A second exposed tape reel on the right of the same face; tape = A visible tape path; heads = A central tape-head block

관계: tape → runs_from → left_reel; tape → passes → heads; tape → runs_to → right_reel

혼동 경계: 오디오·컴퓨터 테이프; 자기테이프 릴과 카세트

주장 한계: 기록 매체·회전·데이터 처리 내용은 외형만으로 확정하지 않음

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M10 — A056, A057

still / P0 / 역할 제안: location, prop

경사진 조작대의 원형 표적 화면 옆에 토글과 바늘 계기가 모이고 성인 운영자가 앉아 있다.

성분: console = A sloped physical control desk; display = A circular plotting display with marks; switches = Grouped toggles and needle gauges; operator = An adult seated at the console

관계: display → on → console; switches → on → console; operator → seated_at → console

혼동 경계: 레이더 원형 표시와 오실로스코프 파형; 일반 CRT와 SAGE 전체

주장 한계: SAGE 특정 판본·실제 표적·명령의 유효성은 별도 확인;상대 위치와 장치 구분만 평가

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt)

## M11 — A059, A060

still / P0 / 역할 제안: relational_action, contact_point

관절 팔을 가진 서비스 로봇의 집게가 수평 쟁반 가장자리를 잡고 쟁반이 컵을 받친다.

성분: robot = A service robot with one jointed arm; tray = A horizontal serving tray; cup = A cup supported by the tray; hand = A robot gripper contacting the tray edge

관계: hand → part_of → robot; hand → contacts → tray; cup → rests_on → tray

혼동 경계: 가사 능력·지능과 구체적인 접촉; 허공의 컵·주인 없는 손

주장 한계: 한 순간의 지지 관계만 평가;서보 피드백·성공한 연속 작업은 입증하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt)

## M12 — A061, A062

still / P1 / 역할 제안: anatomical_connection, body_form

성인 형태 인공 인물의 한쪽 팔뚝 덮개가 열리고 같은 덮개 안에 관절과 배선이 보인다.

성분: figure = An adult-shaped artificial figure; cover = An opened nonbiological forearm cover; mechanism = Visible joints and cable runs under the same cover

관계: cover → part_of_forearm_of → figure; mechanism → inside → cover

혼동 경계: 로봇·안드로이드·생물과 기계가 결합한 사이보그

주장 한계: 인간형 외형은 인격·성별 정체성·생물학적 결합의 증거가 아님;사이보그는 별도 조직 접점 필요

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt)

## B01 — A064, A067, A068

still / P0 / 역할 제안: location, object_structure

뒤로 물러난 지지선보다 넓은 지붕이 날카롭게 치켜올라 돌출되고 낮은 유리벽 실내 옆에 높은 도로 간판이 선다.

성분: roof = A broad sharply upswept roof; support = A set-back support line; glass = A low glass-walled public room; sign = A tall roadside sign

관계: roof → projects_beyond → support; glass → below → roof; sign → beside → glass

혼동 경계: 일반 미드센추리 장식·단순 네온; 캔틸레버와 위로 휜 형상

주장 한계: 겉보기 돌출은 구조 검증이 아님;구기 라벨만으로 간판·지붕 전체를 자동 추가하지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt), [S20](https://www.laconservancy.org/learn/historic-places/panns-coffee-shop/) (indexed_body_excerpt)

## B02 — A069

still / P0 / 역할 제안: object_structure, location

서로 마주한 두 지붕면이 양쪽 높은 끝에서 같은 낮은 중앙 골짜기로 내려온다.

성분: left = One roof plane descending toward a central valley; right = An opposing roof plane descending toward the same valley; valley = A clearly lower central roof trough

관계: left → meets_at → valley; right → meets_at → valley

혼동 경계: 중앙이 높은 박공지붕; 한쪽만 올라간 shed roof

주장 한계: 현재 보이는 단면 관계만 평가;가려진 구조를 일반 구기 지붕으로 대체 통과시키지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt)

## B03 — A070

still / P1 / 역할 제안: object_structure, location

평면 판을 반복해서 접은 듯한 지붕에 곧은 마루선과 골선이 번갈아 이어진다.

성분: roof = A roof formed by repeated angular planar folds; ridges = Alternating straight ridge and valley lines

관계: ridges → part_of → roof

혼동 경계: 주름 커튼·곡면 셸; V자 지붕 하나와 반복 절판

주장 한계: 구조적 강성·설계자·특정 건물은 별도 확인;형태 실현 제안

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt)

## B04 — A071

still / P0 / 역할 제안: object_structure, location

반구형 돔 표면을 곧은 삼각 지지대가 나누고 삼각형들이 공통 접점에서 이어진다.

성분: dome = A hemispherical dome frame; triangles = Repeated straight triangular struts; nodes = Visible shared junctions

관계: triangles → form_surface_of → dome; nodes → join → triangles

혼동 경계: 매끈한 기밀 돔·임의 유리구; 삼각 골격과 공기 밀폐

주장 한계: 삼각 골격과 접합의 가시 구조만 평가;특정 건물·자재·밀폐·구조적 안전성은 별도 원전과 검증 필요

근거: [S51](https://www.bfi.org/about-fuller/geodesic-domes/) (body_excerpt)

## B05 — A072

still / P1 / 역할 제안: location, object_structure

넓은 원형 공공 실내가 가는 중앙 지지부 위에 있고 연속된 원반 테두리가 바깥으로 돌출된다.

성분: building = A wide circular public room; stem = A narrow central support; rim = A continuous overhanging disc rim

관계: building → above → stem; rim → around → building

혼동 경계: 비행체·UFO와 고정 건축; 모든 원형 건물의 구기 판정

주장 한계: 지상 고정·실내 접근 관계는 별도 장면에서 명시;특정 건물 복원 아님

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt)

## B06 — A073, A102

still / P0 / 역할 제안: location, spatial_depth

공공 전시관 안의 축소 미래도시 모형 주위로 관람 난간과 방문객이 둘러선다.

성분: pavilion = A public exhibition pavilion; model = A miniature future-city model inside the pavilion; visitors = Visitors gathered around a viewing rail

관계: model → inside → pavilion; visitors → outside_rail_around → model

혼동 경계: 실제 미래도시와 전시 모형; 소비 유토피아의 실현

주장 한계: 모형과 사람의 크기 관계만;정치적 약속의 진실·관람자의 믿음은 판정하지 않음

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S23](https://zimmerli.rutgers.edu/node/332) (body_excerpt)

## B07 — A074

still / P0 / 역할 제안: location, object_structure

짧은 열차 몸체가 하나의 고가 가이드빔을 걸쳐 타고 빔 아래에는 띄엄띄엄 지지 기둥이 선다.

성분: train = A short train body; beam = A single elevated guide beam; supports = Spaced pylons under the beam

관계: train → straddles → beam; beam → above → supports

혼동 경계: 두 레일 열차·공중에 분리된 차량; 현수형 모노레일

주장 한계: 걸침형 분기만 저술;현수형은 별도 분기;이동·구동 원리는 정지사진으로 증명하지 않음

근거: [S14](https://www.nasa.gov/reference/international-space-station/) (indexed_body_excerpt)

## B08 — A075, A152, A153, A154

still / P0 / 역할 제안: location, space_condition

조용한 한 도로를 따라 낮은 단층집이 반복되고 각 현관 앞 잔디와 붙박이 차고가 보인다.

성분: houses = Repeated low single-storey houses; lawns = Shallow lawns leading to each entrance; garages = Attached garages; road = A shared quiet street

관계: houses → along → road; lawns → in_front_of → houses; garages → attached_to → houses

혼동 경계: 반복 주택과 자발적 동조·핵가족·성 역할; 원자력의 핵과 핵가족

주장 한계: 외형 반복만 평가;거주자의 관계·성별 역할·정치적 복종·일탈 배제는 문맥층

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt), [S37](https://www.archives.gov/education/lessons/fallout-docs) (body_and_captions)

## B09 — A013, A076

proxy / P0 / 역할 제안: location, background_element

넓은 공공 광장 가장자리에 반복 구조 베이의 기념비적 홀이 서고 벽에 로켓·우주비행사 부조가 크게 놓인다.

성분: plaza = A broad public plaza; hall = A monumental public hall with repeated structural bays; relief = A large rocket-and-cosmonaut decorative relief

관계: hall → borders → plaza; relief → on_wall_of → hall

혼동 경계: 미국식 다이너·무조건 붉은 별·모든 소비에트 모더니즘의 단일 양식

주장 한계: 지역·연대·구체 건축의 판본은 추가 원전 필요;부조는 창작 제안이며 실제 정치적 소속의 증거 아님

근거: [S23](https://zimmerli.rutgers.edu/node/332) (body_excerpt), [S24](https://journal.sciencemuseum.ac.uk/article/cosmonauts-birth-of-an-exhibition/) (body_excerpt)

## B10 — A063, A065

proxy / P1 / 역할 제안: location, object_structure

낮고 긴 건물에서 유리 코너가 매끈하게 둥글고 수평 몰딩 띠가 입면을 길게 따른다.

성분: building = A low long building; corner = A smoothly rounded glazed corner; bands = Long horizontal trim bands

관계: corner → part_of → building; bands → along_facade_of → building

혼동 경계: 스트림라인 모던과 구기의 상승선; 아르데코의 모든 분기

주장 한계: 시대·양식은 형상만으로 확정하지 않음;특정 건축의 역사적 복원 전 자료 보강

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt), [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## F01 — A077

still / P0 / 역할 제안: surface_pattern, object_structure

가운데 장식 점 둘레로 여러 타원 궤도가 교차하고 작은 점들이 궤도 위에 붙는다.

성분: center = A central decorative dot; orbits = Several crossing elliptical loops; beads = Small dots placed on the loops

관계: orbits → cross_around → center; beads → on → orbits

혼동 경계: 실제 원자 모형·위성·방사형 별; 양자 상태의 사실 묘사

주장 한계: 과학 상징 장식만 평가;물리학적 정확성·에너지원의 증거 아님

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## F02 — A078

still / P0 / 역할 제안: object_structure, surface_pattern

작은 중앙 시계판에서 길고 짧은 뾰족한 선이 같은 평면으로 방사된다.

성분: center = A small central clock face; rays = Long and short tapered rays radiating in the same plane

관계: rays → radiate_from → center

혼동 경계: 입체 전구 스푸트니크 조명; 태양 그림 자체

주장 한계: 시계의 형상만;1950년대 진품·제조사·디자이너는 별도 증거

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## F03 — A079

still / P0 / 역할 제안: prop, object_structure

작은 구형 조명 허브에서 여러 방향으로 단단한 막대가 뻗고 각 끝에 전구가 달린다.

성분: core = A small spherical lamp hub; rods = Rigid rods extending in many directions; bulbs = Bulbs at the rod tips

관계: rods → attached_to → core; bulbs → at_tips_of → rods

혼동 경계: 실제 스푸트니크 네 안테나; 평면 선버스트 시계

주장 한계: 전구·막대·허브 전체 연결이 필요;이름으로 실제 위성 구조를 강제하지 않음

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## F04 — A080, A081, A082

still / P1 / 역할 제안: object_structure, prop

비대칭의 둥근 로브가 있는 상판 한쪽에 뚜렷한 오목 홈이 있고 가는 다리가 상판을 받친다.

성분: top = An asymmetrical table top with rounded lobes; notch = One distinct inward concave notch; legs = Slender supporting legs

관계: notch → cut_into_edge_of → top; legs → support → top

혼동 경계: 강낭콩형의 안쪽 홈과 꺾인 부메랑형; 모든 유기형을 동의어 처리

주장 한계: 이 카드는 강낭콩형 한 분기;부메랑형은 각진 굽힘을 별도 저술하고 혼합 채택하지 않음

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## F05 — A083, A087, A088

still / P0 / 역할 제안: surface_material, color

둥근 가전 케이스의 상부 민트 패널과 하부 크림 패널 사이를 좁고 거울처럼 밝은 몰딩이 가른다.

성분: appliance = A rounded appliance casing; upper = A pale mint upper panel; lower = A cream lower panel; trim = A narrow mirror-bright strip between the panels

관계: upper → part_of → appliance; lower → part_of → appliance; trim → below → upper; trim → above → lower

혼동 경계: 전체 장면 색과 물체 투톤; 크롬 합금·에나멜 화학 조성

주장 한계: 색의 소유자와 표면 반사만 평가;실제 크롬·도료 종류는 확정하지 않음

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt), [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt)

## F06 — A084

proxy / P0 / 역할 제안: surface_material, object_structure

평평한 카운터의 얇은 무늬 표면과 층진 단면이 보이고 둥근 금속 띠가 테두리를 따라간다.

성분: counter = A flat counter slab; skin = A thin patterned top skin; edge = A visible layered edge; band = A separate rounded metal edge band

관계: skin → on_top_of → counter; edge → part_of → counter; band → along_edge_of → counter

혼동 경계: Formica 상표와 일반 장식 적층판; 대리석·통짜 수지

주장 한계: 제조사·수지·층별 화학 조성은 외형만으로 증명하지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt), [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt)

## F07 — A085, A086

proxy / P1 / 역할 제안: surface_material, object_structure

매끈한 한 덩어리 곡면 의자 셸의 테두리가 연속되고 아래에는 별도의 가는 지지대가 있다.

성분: shell = A smooth one-piece curved chair shell; lip = A continuous rolled-looking perimeter; supports = Separate narrow supports under the shell

관계: lip → around → shell; supports → under → shell

혼동 경계: 성형 플라스틱·유리섬유·합판; 매끈함을 재료 조성 증거로 사용

주장 한계: 성형처럼 보이는 형상만;섬유·제조 공정은 확인 자료 없으면 proxy로 유지

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt), [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## F08 — A089, A090

still / P0 / 역할 제안: prop, object_structure

낮고 긴 차체 뒤에 한 쌍의 테일핀이 솟고 객실 위를 둥근 투명 캐노피가 감싼다.

성분: car = A long low car body; fins = Paired raised tailfins at the rear; canopy = A rounded clear cabin canopy

관계: fins → at_rear_of → car; canopy → above_cabin_of → car

혼동 경계: 테일핀과 실제 비행날개; 풍선형 유리와 고정 캐노피

주장 한계: 여기서는 한 가상 차체의 조형;실제 모델·연대·핵동력·비행 능력 아님

근거: [S06](https://www.thehenryford.org/collections/explore/artifact/278186) (body_and_object_metadata), [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt)

## L01 — A091

still / P0 / 역할 제안: location, prop_placement

긴 서비스 카운터 앞에 기둥형 의자가 일정 간격으로 놓이고 외벽 쪽 부스 좌석과 카운터 뒤 커피포트가 보인다.

성분: counter = A long service counter; stools = Evenly spaced pedestal stools; booths = Booth seats against the outer wall; pot = A coffee pot behind the counter; wall = An outer wall of the room

관계: stools → in_front_of → counter; booths → beside → wall; pot → behind → counter

혼동 경계: 다이너 실내·구기 외관·드라이브인 이용 방식

주장 한계: 음식 종류·노동 관계·미국 전체의 필수 실내를 뜻하지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt), [S20](https://www.laconservancy.org/learn/historic-places/panns-coffee-shop/) (indexed_body_excerpt)

## L02 — A092

still / P1 / 역할 제안: location, relational_action

주차된 자동차의 열린 옆창 가장자리에서 쟁반이 지지되고 성인 서버가 차 밖에 서 있다.

성분: car = A parked car with an open side window; tray = A tray supported at the window edge; server = An adult server standing outside

관계: tray → supported_at_window_of → car; server → outside → car

혼동 경계: 드라이브인 식당과 자동차극장; 드라이브스루

주장 한계: 자동차극장은 별도 스크린·주차열 분기;세 형식을 한 후보로 묶지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt)

## L03 — A093, A094

still / P1 / 역할 제안: location, background_element

외부 출입 객실이 낮게 줄서고 문 앞 주차띠 옆에 독립 간판 기둥이 솟아 글자 윤곽의 발광 튜브가 보인다.

성분: rooms = A low row of exterior-entry rooms; parking = A parking strip directly outside the doors; pylon = A tall freestanding sign frame; tubes = Visible luminous tubing along the sign letters

관계: parking → in_front_of → rooms; tubes → on → pylon; pylon → beside → parking

혼동 경계: 네온은 광원·파일런은 지지 형식; 모든 파일런이 네온인 것은 아님

주장 한계: 선택한 야간 간판 분기만;가스 성분·실제 영업·여행자의 관계는 확정하지 않음

근거: [S19](https://www.laconservancy.org/learn/historic-places/johnies-coffee-shop/) (body_excerpt)

## L04 — A095

still / P1 / 역할 제안: prop, object_structure

독립 음악 캐비닛 앞에 물리 선곡 버튼과 투명 전시창이 있고 곡선 장식 조명이 창을 둘러싼다.

성분: cabinet = A freestanding music cabinet; selector = A bank of physical song-selection buttons; window = A clear display window; lighting = Curved decorative light strips

관계: selector → on → cabinet; window → on_front_of → cabinet; lighting → around → window

혼동 경계: 주크박스와 가정용 하이파이; 실제 재생 음악

주장 한계: 재생·코인 작동은 정지사진에서 미검증;전면 판본은 후속 확인

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt)

## L05 — A096

still / P0 / 역할 제안: prop, prop_placement

칸이 나뉜 식사 트레이에 음식이 분리되어 있고 낮은 접이식 테이블 맞은편에는 TV가 놓인다.

성분: tray = A compartmented meal tray; food = Separate food portions in the compartments; table = A low folding table; tv = A television facing the table

관계: food → inside → tray; tray → on → table; tv → faces → table

혼동 경계: 도시락·기내식; 혼자 먹는 것과 외로움·가족 관계

주장 한계: 가시 배치만;냉동·조리 공정·시청 시간·감정은 확정하지 않음

근거: [S27](https://americanhistory.si.edu/explore/exhibitions/food/online/new-and-improved/help-home-cook/no-work-no-dishes) (indexed_body_excerpt)

## L06 — A097, A098

still / P0 / 역할 제안: location, relational_action

붙박이 주방 카운터 끝에 버튼 패널이 있고 열린 배식 해치의 받침 위에 준비된 접시가 놓인다.

성분: kitchen = A compact fitted kitchen; panel = A button panel at a counter edge; hatch = An open serving hatch; plate = A prepared plate supported on the hatch ledge

관계: panel → on → kitchen; plate → on → hatch; hatch → part_of → kitchen

혼동 경계: 자동화의 표시와 실제 자동 조리; 새 가전의 나열

주장 한계: 버튼 입력부터 조리 완료까지의 시간 인과는 한 장으로 증명하지 않음;관계는 저술 제안

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt)

## L07 — A099, A132

still / P1 / 역할 제안: location, prop_placement

낮은 오디오 캐비닛 상단에 레코드플레이어가 들어가고 양옆에 스피커 캐비닛, 옆에는 작은 음료 바가 놓인다.

성분: cabinet = A low audio cabinet; record = A record player recessed in its top; speakers = Two spatially separated speaker cabinets; bar = A small drinks counter

관계: record → inside → cabinet; speakers → to_either_side_of → cabinet; bar → beside → cabinet

혼동 경계: 독신 남성·성적 자유·부유함을 인테리어로 추론; 스피커 두 대와 실제 스테레오

주장 한계: 시각적인 음향 설비만;소리·주민 관계·주거 권한은 문맥층

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S27](https://americanhistory.si.edu/explore/exhibitions/food/online/new-and-improved/help-home-cook/no-work-no-dishes) (indexed_body_excerpt)

## L08 — A101, A102

still / P0 / 역할 제안: background_element, visible_text

밝은 홍보 포스터의 인쇄 테두리 안에서 웃는 그림 마스코트가 가전 제품 그림 옆에 배치된다.

성분: poster = A bright promotional poster; mascot = A smiling drawn mascot within its printed border; product = A rendered appliance beside the mascot

관계: mascot → printed_on → poster; product → printed_on → poster

혼동 경계: 인쇄 캐릭터와 장면 속 실물 로봇; 행복 광고와 실제 행복

주장 한계: 정확한 문구는 별도 text gate;홍보 주장·인물 믿음·기업 도덕성을 판정하지 않음

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt)

## W01 — A104

still / P0 / 역할 제안: wardrobe_style, silhouette_proportion

성인 착용자의 재킷 허리가 뚜렷하게 잘록하고 종아리 길이 풍성한 치마의 밑단이 넓게 퍼진다.

성분: wearer = An adult wearer; jacket = A fitted jacket with a sharply defined waist; skirt = A full calf-length skirt; hem = A broad outward skirt hem

관계: jacket → worn_by → wearer; skirt → worn_by → wearer; hem → part_of → skirt

혼동 경계: 뉴 룩과 직선 시프트·펜슬; 체형 자체의 변경

주장 한계: 의복 구조·실루엣만;신체 비율·계층·가정적 역할을 추론하거나 자동 변경하지 않음

근거: [S26](https://www.vam.ac.uk/articles/the-golden-age-of-couture) (indexed_body_excerpt)

## W02 — A105

still / P1 / 역할 제안: garment_fit, garment_detail

성인 착용자의 골반선을 따라 좁게 내려오는 치마가 무릎 가까이 끝나고 뒤쪽에 작은 보행 트임이 보인다.

성분: wearer = An adult wearer; skirt = A narrow skirt following the hips; hem = A hem close to the knees; vent = A small visible back walking vent

관계: skirt → worn_by → wearer; vent → part_of → skirt; hem → part_of → skirt

혼동 경계: 연필 모양 장식·플레어 치마; 직업·성적 성격

주장 한계: 형상과 선택한 트임 분기만;보이지 않는 뒷부분을 정면 사진으로 통과시키지 않음

근거: [S26](https://www.vam.ac.uk/articles/the-golden-age-of-couture) (indexed_body_excerpt)

## W03 — A106, A107

proxy / P1 / 역할 제안: garment_detail, silhouette_proportion

지지 구조가 있는 상의에 뾰족한 한 쌍의 컵이 형성되고 각 컵 둘레에 동심 봉제선이 보인다.

성분: garment = A supported upper garment; cups = Paired pointed cup structures; seams = Concentric stitched lines around each cup

관계: cups → part_of → garment; seams → on → cups

혼동 경계: 원뿔형 의복 지지 구조와 실제 신체 해부; 니트만으로 속옷 확정

주장 한계: 소장품 설명으로 원뿔형 컵과 원형 봉제의 근거를 확인;정확한 유물 판본 복원은 원본 픽셀 검토 전 미확정;속옷 구조를 실제 신체 비율로 바꾸지 않음

근거: [S26](https://www.vam.ac.uk/articles/the-golden-age-of-couture) (indexed_body_excerpt), [S50](https://web.prm.ox.ac.uk/bodyarts/index.php/permanent-body-arts/reshaping-and-piercing/150-reshaping-breasts.html) (body_and_object_metadata)

## W04 — A108, A109, A112

still / P0 / 역할 제안: wardrobe_style, garment_detail

성인 착용자의 짧은 직선 드레스에 각진 절개선과 흰색·은색 패널, 단정한 기하학적 밑단이 보인다.

성분: wearer = An adult wearer; dress = A short straight dress with angular seams; panels = Contrasting white and silver panels; edge = A clean geometrical hem

관계: dress → worn_by → wearer; panels → part_of → dress; edge → part_of → dress

혼동 경계: 미니는 길이·시프트는 구조; 모든 미니가 A라인·모든 mod가 우주복

주장 한계: 나이·직업·인공 재료 종류는 외형만으로 확정하지 않음;실제 디자이너 판본 복원 아님

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## W05 — A110

still / P0 / 역할 제안: footwear, garment_detail

성인 착용자의 양발에 매끈한 흰 부츠가 맞춰지고 낮고 넓은 굽과 간결한 원통형 샤프트가 보인다.

성분: wearer = An adult wearer; boots = A matching pair of smooth white boots; heels = Low broad heels; shafts = Close cylindrical shafts

관계: boots → worn_on_feet_of → wearer; heels → part_of → boots; shafts → part_of → boots

혼동 경계: 1960s 모든 부츠와 특정 고고 부츠; 무조건 무릎 길이

주장 한계: 발목·종아리·무릎 길이는 별도 분기;가려진 양발·굽을 완전 통과시키지 않음

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## W06 — A111, A125

proxy / P0 / 역할 제안: surface_material, garment_detail

성인 착용자의 광택 비닐처럼 보이는 겉옷 주름을 따라 밝은 반사가 꺾이고 앞 여밈이 보인다.

성분: wearer = An adult wearer; garment = A glossy close-fitting vinyl-like outer garment; folds = Sharp bright reflections bending at garment folds; closure = A visible front fastening

관계: garment → worn_by → wearer; folds → on → garment; closure → part_of → garment

혼동 경계: 금속성 직물·PVC·라텍스; 광택과 성적 취향·페티시

주장 한계: 재료 조성·성적 흥분·동의는 시각 판정 불가;성적 강조는 현재 사용자 설정이 별도 결정

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## W07 — A113

still / P1 / 역할 제안: wardrobe_style, object_structure

성인 착용자의 몸통에서 바지 다리까지 한 벌로 이어지는 의복에 앞 지퍼와 패치 주머니가 보인다.

성분: wearer = An adult wearer; suit = A one-piece garment with continuous torso and trouser legs; zip = A visible front zip; pockets = Functional patch pockets

관계: suit → worn_by → wearer; zip → part_of → suit; pockets → on → suit

혼동 경계: 상하 세트와 점프슈트; 유니섹스와 실제 성별·역할

주장 한계: 유니섹스는 설계·판매 문맥;성별 정체성·소속·직업은 의복만으로 확정하지 않음

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## W08 — A114

still / P1 / 역할 제안: hair_style, object_structure

성인 인물의 정수리 위로 높고 둥근 머리 볼륨이 솟고 옆머리가 위쪽 덩어리로 이어진다.

성분: head = An adult subject's head; hair = A tall rounded hair mass above the crown; sides = Swept-up side hair flowing into the upper mass

관계: hair → above_crown_of → head; sides → join → hair

혼동 경계: 비하이브와 일반 부푼 웨이브; 장식 헬멧

주장 한계: 형상 제안의 시대적 인접 근거;정확한 기원·고증은 헤어 소장품 추가 확인

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)

## V01 — A115, A116, A117

proxy / P1 / 역할 제안: presentation_style, background_element

옷을 입고 포즈를 취한 성인의 글래머 초상 인쇄물이 종이 테두리와 고정핀을 드러내며 벽에 걸린다.

성분: print = A printed adult glamour portrait; figure = A clothed adult posed for the portrait; border = A visible paper border and mounting pins; wall = A workshop wall

관계: figure → depicted_in → print; print → pinned_to → wall

혼동 경계: 핀업 매체·여성형 cheesecake·남성형 beefcake의 구분; 디저트 키워드

주장 한계: 해당 인물은 종이 속 묘사;성적 지향·동의·실제 근육량·매력 평가는 확정하지 않음

근거: [S28](https://special.library.unlv.edu/node/58463) (collection_metadata), [S29](https://thelibrarydistrict.org/blogs/post/miss-atomic-bomb-icon-of-the-atomic-age/) (indexed_curatorial_excerpt)

## V02 — A119

still / P1 / 역할 제안: wardrobe_style, garment_detail

성인 착용자에게 수영복 상의와 하의가 따로 놓이고 그 사이 허리 부분이 드러난다.

성분: wearer = An adult wearer; top = A separate two-piece swimwear top; bottom = A separate swimwear bottom; gap = Visible midriff between both garments

관계: top → worn_by → wearer; bottom → worn_by → wearer; gap → below → top; gap → above → bottom

혼동 경계: 비키니 환초·핵실험과 의복; 원피스 수영복

주장 한계: 명명의 정확한 역사·모든 비키니 형태는 별도 패션 원전 과제;성적 의미를 자동 추가하지 않음

근거: [S29](https://thelibrarydistrict.org/blogs/post/miss-atomic-bomb-icon-of-the-atomic-age/) (indexed_curatorial_excerpt)

## V03 — A120

versioned / P1 / 역할 제안: garment_detail, background_element

성인 홍보 인물이 입은 원피스 수영복 앞면에 솜처럼 보이는 버섯구름 장식이 부착된다.

성분: figure = An adult promotional figure; swimsuit = A one-piece swimsuit; ornament = A cotton-like mushroom-cloud applique on the front

관계: swimsuit → worn_by → figure; ornament → attached_to_front_of → swimsuit

혼동 경계: 비키니와 원피스; 실제 폭발과 부착 장식; 정식 대회 우승자라는 단정

주장 한계: 역사적 인물의 신원 재현 없이 구조 연구;1957 사진과 목록의 넓은 연대 범위를 구분

근거: [S28](https://special.library.unlv.edu/node/58463) (collection_metadata), [S29](https://thelibrarydistrict.org/blogs/post/miss-atomic-bomb-icon-of-the-atomic-age/) (indexed_curatorial_excerpt)

## V04 — A121, A122, A140

proxy / P1 / 역할 제안: presentation_style, wardrobe_style

성인 무대 인물의 각진 금속성 의상 뒤로 조형된 인공 행성 배경과 장식 무대등이 드러난다.

성분: performer = An adult stage performer; costume = An angular metallic-looking costume; set = A visibly artificial sculpted planetary backdrop; lights = Decorative stage lights

관계: costume → worn_by → performer; performer → in_front_of → set; lights → around → set

혼동 경계: 쇼걸과 벌레스크; 캠프와 단순 노출; 성적 유혹을 여성 우주인의 본질로 만들기

주장 한계: 공연의 외형 제안만;성적 행위·욕망·장르 전체의 캠프 효과를 자동 확정하지 않음

근거: [S30](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion) (body_excerpt), [S31](https://www.viennale.at/en/films/barbarella) (body_excerpt)

## V05 — A126

context / P1 / 역할 제안: adult_presentation_context

BDSM 도상은 패션 차용·합의된 성인 실천·강압 장면을 구별하는 문맥으로 남긴다.

성분: 

관계: 

혼동 경계: 목걸이·손목 장식만으로 BDSM·동의·학대를 확정

주장 한계: 당사자 단체 문헌으로 동의의 개념을 확인;개별 관계의 합의·권력 관계는 사진의 하드 시각 의무나 법적 판단으로 만들지 않음

근거: [S30](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion) (body_excerpt), [S53](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement-summary.pdf) (pdf_text_excerpt)

## G01 — A133

proxy / P1 / 역할 제안: prop, hand_pose

목재 전자악기 캐비닛의 수직 막대와 수평 루프 안테나 근처에 성인 연주자의 손이 접촉 없이 놓인다.

성분: instrument = A wooden electronic-instrument cabinet; rod = A vertical rod antenna; loop = A separate horizontal loop antenna; hands = An adult player's hands held clear of the antennae

관계: rod → attached_to → instrument; loop → attached_to → instrument; hands → near_without_touching → instrument

혼동 경계: 테레민과 전자키보드; 모든 SF 음향이 테레민이라는 단정

주장 한계: 소리·실제 제어 원리는 정지사진에서 미검증;1929 소장품 형상은 추가 픽셀 확인 필요

근거: [S48](https://collection.sciencemuseumgroup.org.uk/objects/co8593059) (indexed_object_metadata)

## G02 — A135, A136, A138

still / P1 / 역할 제안: medium, background_element

테두리가 보이는 펄프풍 인쇄 장면 안에 핀 로켓과 큰눈 괴물이 그려지고 별도 캡션 칸이 나뉜다.

성분: poster = A pulp-style printed scene inside a visible frame; rocket = A painted finned rocket; monster = A painted large-eyed creature; caption = A separate printed caption block

관계: rocket → depicted_in → poster; monster → depicted_in → poster; caption → printed_on → poster

혼동 경계: 실물 장면과 그림 속 인물; 뉴스영화·공공 교육영화의 시간 형식

주장 한계: 이는 펄프 삽화 한 분기;영화 편집·내레이션·정확한 문구는 별도 증거와 매체 선택 필요

근거: [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt)

## R01 — A150, A151

still / P0 / 역할 제안: location, relational_action

유인 관제 부스 안에는 두꺼운 모니터가 모이고 차단대 밖 대기열 앞에서 천공카드가 리더 위치에 놓인다.

성분: booth = A staffed control booth; monitors = Several deep physical monitors; queue = A short queue behind a barrier; card = A punched card held at a reader; reader = A physical punched-card reader

관계: monitors → inside → booth; queue → outside → booth; card → at → reader

혼동 경계: 출입 절차와 충성심 검사·감시국가의 확정; 카드와 실제 사상

주장 한계: 구체적인 검사 배치만;국가 규모 감시·정치적 충성·실제 정보 수집은 문맥층

근거: [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt), [S34](https://www.loc.gov/exhibits/hope-for-america/a-climate-of-fear.html) (body_excerpt)

## R02 — A149, A151

still / P0 / 역할 제안: narrative_clue, prop_placement

닫힌 출입문 옆 카드 리더와 문 위 기업 로고판 뒤로 반복 주거동이 보인다.

성분: gate = A closed access gate; reader = A card reader at the gate; sign = A company-logo placard; housing = Repeated housing visible beyond the gate

관계: reader → beside → gate; sign → on → gate; housing → beyond → gate

혼동 경계: 공장 출입구와 기업 소유 도시; 신분과 전력 공급의 실제 결합

주장 한계: 기업 온정주의·시민권·고용 관계는 장면만으로 확정하지 않음;로고는 창작이며 특정 기업 아님

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S36](https://www.archives.gov/milestone-documents/president-dwight-d-eisenhowers-farewell-address) (primary_document_page)

## R03 — A161, A163

still / P0 / 역할 제안: location, prop_placement

낮게 둘러싸인 지하실 안에 겹침 침상과 밀폐 식품·물통 선반, 작은 물리 라디오가 놓인다.

성분: room = A low enclosed basement room; bunks = Stacked sleeping bunks; shelves = Shelves of sealed food cans and water containers; radio = A small physical radio

관계: bunks → inside → room; shelves → inside → room; radio → on → shelves

혼동 경계: 대피소와 군사 지휘벙커; 비축물과 실제 생존 기간

주장 한계: 낙진 차폐·식품 안전·충분한 기간은 입증하지 않음;대피소 표식 문구는 별도 확인

근거: [S37](https://www.archives.gov/education/lessons/fallout-docs) (body_and_captions)

## R04 — A162

still / P1 / 역할 제안: body_pose, contact_point

성인 훈련 참가자가 튼튼한 책상 아래 웅크리고 두 팔로 낮춘 머리를 가린다.

성분: adult = An adult drill participant; desk = A sturdy table; head = The participant's lowered head; arms = The participant's arms over the head

관계: adult → crouches_under → desk; arms → cover → head

혼동 경계: 민방위 동작과 실제 핵폭발에서의 안전 보증; 시대의 필수 아동 인물

주장 한계: 성인 시연 분기;훈련의 가시 동작만;보호 효과·지침의 현재 적합성은 판단하지 않음

근거: [S37](https://www.archives.gov/education/lessons/fallout-docs) (body_and_captions)

## R05 — A164, A165

proxy / P0 / 역할 제안: atmospheric_medium, object_structure

넓고 소용돌이치는 구름 머리가 더 좁은 수직 기둥 위로 퍼지고 낮은 먼지층이 바닥에 펼쳐진다.

성분: cloud = A broad turbulent cloud cap; stem = A narrower rising vertical cloud column; base = A low spreading dust layer

관계: cloud → above → stem; stem → above → base

혼동 경계: 버섯구름은 핵폭발만의 형상이 아님; 방사성 낙진과 일반 먼지

주장 한계: 핵기원·방사능·폭발 종류·피폭량을 형상에서 확정하지 않음

근거: [S37](https://www.archives.gov/education/lessons/fallout-docs) (body_and_captions)

## R06 — A166, A167

proxy / P0 / 역할 제안: location, scale_relation

사람 없는 모형 주거도로의 가구 있는 시험 주택 안에 딱딱한 인체형 시험물이 있고 떨어진 곳에는 계측 스테이션이 놓인다.

성분: street = A deserted mock residential street; house = A furnished test-house facade; figures = Rigid human-shaped test figures; instruments = Measurement stations set back from the house

관계: figures → inside → house; instruments → beside → street; house → along → street

혼동 경계: 실제 거주자·피해 시신과 시험 인형; 일반 교외 빈집

주장 한계: 구체 인형 판본은 사진 원본 확인 전 proxy;실험 수행·피해·안전은 장면으로 확정하지 않음

근거: [S37](https://www.archives.gov/education/lessons/fallout-docs) (body_and_captions)

## R07 — A172

still / P0 / 역할 제안: location, aftermath_trace

쇠락한 미래 전시관 옆 고가 궤도가 끊기고 건물에는 빛바랜 명랑한 홍보판, 기단에는 자란 식물이 보인다.

성분: pavilion = A deteriorated future-exhibition pavilion; track = A broken elevated guideway; sign = A faded cheerful promotional panel; plants = Vegetation encroaching at the base

관계: track → beside → pavilion; sign → on → pavilion; plants → at_base_of → pavilion

혼동 경계: 폐허와 실제 핵전쟁 원인; 모든 atompunk를 Fallout 폐허로 통일

주장 한계: 현재의 손상·식생만 평가;시간 길이·핵 오염·사람의 죽음은 확정하지 않음

근거: [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt), [S47](https://gear.bethesda.net/products/fallout-essential-tin-sign-set) (indexed_rightsholder_product_copy)

## H01 — A173, A174, A175

still / P1 / 역할 제안: location, object_structure

유리 격벽 너머 실험실 작업대에는 닫힌 기기가 놓이고 바깥 복도와 통제 출입문이 공간을 나눈다.

성분: lab = A separated laboratory behind a glazed partition; bench = A workbench with closed instruments; corridor = A corridor outside the partition; door = A controlled entry door

관계: bench → inside → lab; corridor → outside → lab; door → in_boundary_of → lab

혼동 경계: 비밀 연구소와 일반 연구시설; 과학자 외모와 비윤리성

주장 한계: 인간 실험·비동의·정신질환은 시각 fact가 아님;일반 공간 후보만 제안

근거: [S41](https://ehss.energy.gov/ohre/roadmap/whitehouse/exesum.html) (body_excerpt)

## H02 — A176, A177

still / P0 / 역할 제안: scale_relation, species_marker

하나의 거대한 두발 생물이 다리 근처 도시 건물보다 높이 솟고 아래에는 거리의 규모 기준이 보인다.

성분: creature = A single enormous bipedal creature; buildings = Several city buildings near its legs; street = An inhabited-scale street below

관계: creature → towers_over → buildings; buildings → along → street

혼동 경계: 원근상의 가까운 작은 모형과 거대 생물; 모든 괴수의 핵기원

주장 한계: 도시 대비 크기 관계만;실제 방사선 원인·고유 IP 외형·실제 사망을 추가하지 않음

근거: [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## H03 — A178

still / P0 / 역할 제안: species_marker, scale_relation

세 몸마디와 여섯 다리, 한 쌍 더듬이를 가진 하나의 거대 곤충 옆에 작은 보통 차량이 놓인다.

성분: insect = A single giant six-legged insect; body = Three distinct body segments; antennae = A pair of antennae; vehicle = A small ordinary vehicle beside it

관계: body → part_of → insect; antennae → on_head_of → insect; insect → larger_than → vehicle

혼동 경계: 거미는 곤충이 아님; 개미·벌·거미의 몸 구조 혼합

주장 한계: 소스의 거미 포함 서술은 원 분류의 오류 가능성으로 남김;거미형은 여덟 다리 별도 branch

근거: [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## H04 — A179, A180, A189

still / P1 / 역할 제안: body_form, anatomical_connection

가상의 성인 크기 생물에 의도된 여분 팔이 붙고 팔 뿌리의 연속 조직 접점이 드러난다.

성분: creature = A fictional adult-sized creature; arm = A deliberately extra arm; join = A continuous visible tissue junction at the extra arm root

관계: arm → attached_to → creature; join → at_root_of → arm

혼동 경계: 실제 피폭 피해·장애와 SF 돌연변이; 생성기의 실수 팔다리

주장 한계: 사용자가 선택한 가상 신체 구조만;유전·피폭 원인·진단·배척의 역사를 외형에서 추론하지 않음

근거: [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## H05 — A181

still / P1 / 역할 제안: species_marker, body_form

비인간 가상 생물의 과장되어 돌출된 두 눈이 짧은 지지 구조를 통해 몸에 이어진다.

성분: creature = A fictional nonhuman creature; eyes = Two exaggerated protruding eyes; stalks = Short structures supporting the eyes

관계: eyes → on → stalks; stalks → part_of → creature

혼동 경계: BEM을 실제 곤충 분류로 취급; 돌출 눈과 악의·정신질환

주장 한계: 펄프 도상 제안;생물학적 종·정치적 적대·공격 의도는 판정하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt), [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## H06 — A184

still / P1 / 역할 제안: prop, anatomical_connection

밀폐 투명 전시 용기 속에 뇌 모양 인공 표본이 맑은 액체에 잠기고 뚜껑의 밀폐 포트로 리드가 지나간다.

성분: vessel = A transparent sealed display vessel; specimen = A stylized brain-shaped artificial specimen; fluid = Clear liquid around the specimen; leads = Visible leads crossing a sealed lid port

관계: specimen → inside → vessel; fluid → inside → vessel; leads → pass_through_lid_of → vessel

혼동 경계: 실제 살아 있는 뇌·의식·신원; 용기 밖 공중 전선

주장 한계: 외형 연구 분기;생명·의식·실험 동의·표본 출처는 확정하지 않음

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt), [S41](https://ehss.energy.gov/ohre/roadmap/whitehouse/exesum.html) (body_excerpt)

## X01 — A001, A002, A003, A004, A005, A006, A007, A008, A009, A010, A011, A012, A013, A014, A032

context / P0 / 역할 제안: genre, world, historical_period

장르·시대·문화 경로를 보존하고 선택한 공간·장치·의복의 구체 형태로 내려간다.

성분: 

관계: 

혼동 경계: 장르 이름과 외형 의무; strictly pre-digital을 디지털 컴퓨터 부재로 읽기

주장 한계: 단일 연대·미국식 소품·녹색 빛·파국·정치 신념을 라벨로 강제하지 않음

근거: [S01](https://www.wired.com/2008/12/here-comes-atom/) (body_excerpt), [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt), [S16](https://www.computerhistory.org/siliconengine/invention-of-the-point-contact-transistor/) (body_heading_and_indexed_metadata), [S24](https://journal.sciencemuseum.ac.uk/article/cosmonauts-birth-of-an-exhibition/) (body_excerpt), [S43](https://11bitstudios.com/games/the-invincible/) (publisher_synopsis)

## X02 — A015, A016, A017, A018, A019, A021, A025, A026

context / P0 / 역할 제안: world, narrative_clue

에너지 약속·정책·핵반응·허구 소형화는 문맥층에 두고 선택한 설비 또는 전시 도해의 가시 구조만 따로 저술한다.

성분: 

관계: 

혼동 경계: 핵분열·핵융합·RTG·핵열·핵펄스·현대 Orion을 서로 대체

주장 한계: 평면 도해는 사진과 다른 매체;소스 S08 미확보로 Orion 판본은 defer;무료 전력·소형화의 달성을 주장하지 않음

근거: [S02](https://www.eisenhowerlibrary.gov/research/online-documents/atoms-peace) (body_excerpt), [S03](https://www.nrc.gov/education-regulatory-research/history-101/too-cheap-to-meter-a-history-of-the-phrase) (indexed_excerpt_body_403), [S04](https://science.nasa.gov/planetary-science/programs/radioisotope-power-systems/power-radioisotope-thermoelectric-generators/) (body_excerpt), [S07](https://www.nasa.gov/rocket-systems-area-nuclear-rockets/) (indexed_body_excerpt), [S08](https://airandspace.si.edu/collection-objects/propulsion-test-vehicle-project-orion/nasm_A19721008000) (access_failed_403), [S09](https://www.energy.gov/lm/plowsharevela-uniformweapons-related-program-sites) (body_excerpt)

## X03 — A041, A050, A058, A059

context / P0 / 역할 제안: world, procedure_step

회전·피드백·전자두뇌·자동제어의 원리와 현재 보이는 장치 배치를 분리한다.

성분: 

관계: 

혼동 경계: 서보 관절의 외형과 실제 피드백; 원환 구조와 실제 인공중력

주장 한계: 작동·지능·제어 인과는 정지사진 하드 gate로 만들지 않음;시간 자료가 필요

근거: [S14](https://www.nasa.gov/reference/international-space-station/) (indexed_body_excerpt), [S15](https://www.computerhistory.org/revolution/real-time-computing/6/122) (body_excerpt), [S17](https://blog.sciencemuseum.org.uk/back-to-the-future-of-computing/) (indexed_body_excerpt)

## X04 — A066, A100, A139, A140

context / P1 / 역할 제안: aesthetic_trend, presentation_style

대중소비 미학·키치·캠프·서구의 티키 차용은 비평 문맥으로 두고 구체 형상과 역사 범위를 따로 기록한다.

성분: 

관계: 

혼동 경계: 티키 소비 이미지와 실제 태평양 지역 문화; 키치와 캠프; 1986 용어와 당대 명칭

주장 한계: 실제 문화·민족·취향·비평 효과를 소품에서 확정하지 않음;Tiki는 차용을 다룬 행사 소개까지 확인했고 지역별 진품 판본은 추가 조사

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt), [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S23](https://zimmerli.rutgers.edu/node/332) (body_excerpt), [S30](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion) (body_excerpt), [S52](https://www.docomomo-us.org/event/mission-for-modernism-tiki-bars-kitsch-or-cultural-appropriation) (indexed_event_description_page_header_followup_timeout)

## X05 — A118, A123, A124, A127, A128, A155

context / P1 / 역할 제안: adult_presentation_context, narrative_clue

성인 문화·인공 연인·대상화·성적 해방의 개념은 보존하고 의상·인공 신체·그림 속 인물과 비가시 관계를 나눈다.

성분: 

관계: 

혼동 경계: Bombshell 인물 호칭과 폭탄; 인간형 로봇과 인격·연애·성적 의도

주장 한계: 성인 외형·의상만으로 욕망·동의·관계·정체성을 확정하거나 장르 라벨로 성적 표현을 활성화하지 않음

근거: [S30](https://www.metmuseum.org/exhibitions/listings/2019/camp-notes-on-fashion) (body_excerpt), [S31](https://www.viennale.at/en/films/barbarella) (body_excerpt)

## X06 — A129, A130, A131, A132, A134, A135, A136, A137, A138

audio_temporal / P1 / 역할 제안: medium, presentation_style

음향·뉴스영화·교육영화·B급 제작과 정지화면의 설비·인쇄·세트를 분리한다.

성분: 

관계: 

혼동 경계: 하이파이 장치와 고음질; 스테레오 공간감과 스피커 수; 음향과 화면 색

주장 한계: 오디오·편집·성우·영화 전체 경험은 정지사진 픽셀로 점수화하지 않음

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt), [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt), [S48](https://collection.sciencemuseumgroup.org.uk/objects/co8593059) (indexed_object_metadata)

## X07 — A141, A142, A143, A144, A145, A146, A147, A148

context / P0 / 역할 제안: world, narrative_clue

냉전·블랙리스트·라벤더 공포·군산복합체는 문서와 서사 맥락으로 남긴다.

성분: 

관계: 

혼동 경계: 붉은 색과 공산주의; 외모와 성적 지향; 대기열과 정치적 숙청

주장 한계: 실제 소속·정치 성향·피해자 신원·직업 배제는 외형으로 확정하지 않음;문서 내용은 별도 출처와 읽기 증거

근거: [S34](https://www.loc.gov/exhibits/hope-for-america/a-climate-of-fear.html) (body_excerpt), [S35](https://www.archives.gov/research/lgbt/federal-employment) (body_excerpt), [S36](https://www.archives.gov/milestone-documents/president-dwight-d-eisenhowers-farewell-address) (primary_document_page)

## X08 — A149, A150, A151, A152, A153, A154

context / P0 / 역할 제안: world, social_cue

제도·가족·성 역할의 서사 문맥과 문·카드·반복 주택 같은 가시 배치를 구분한다.

성분: 

관계: 

혼동 경계: 핵가족의 nuclear와 원자력; 정돈된 거리와 자발적 동조

주장 한계: 성별·혈연·동의·기업 소유·시민권을 소품으로 확정하지 않음

근거: [S22](https://cranbrookartmuseum.org/2014/03/10/cranbrook-and-the-american-look/) (body_excerpt), [S34](https://www.loc.gov/exhibits/hope-for-america/a-climate-of-fear.html) (body_excerpt), [S35](https://www.archives.gov/research/lgbt/federal-employment) (body_excerpt), [S36](https://www.archives.gov/milestone-documents/president-dwight-d-eisenhowers-farewell-address) (primary_document_page)

## X09 — A156, A157, A158, A159, A160

context / P0 / 역할 제안: world, narrative_clue

군비경쟁·핵 억지·상호확증파괴·벼랑 끝 전술·최후 장치는 전략과 허구 설정으로 보존한다.

성분: 

관계: 

혼동 경계: 원탁·대형 지도·버섯구름과 전략의 실증; MAD의 일반 형용사 의미

주장 한계: 단일 사진으로 보복 능력·정치적 의도·전 지구 파괴 가능성을 판정하지 않음

근거: [S02](https://www.eisenhowerlibrary.gov/research/online-documents/atoms-peace) (body_excerpt), [S36](https://www.archives.gov/milestone-documents/president-dwight-d-eisenhowers-farewell-address) (primary_document_page), [S45](https://www.sonypicturesmuseum.com/collection/film/625/dr-strangelove.html) (indexed_licensor_synopsis)

## X10 — A164, A168, A169, A170, A171

context / P0 / 역할 제안: narrative_clue, world

오염·건강 피해·주변화·기후 원인은 외형에 환원하지 않고 출처 문맥과 현재 상태를 분리한다.

성분: 

관계: 

혼동 경계: 방사선 질환과 창백함; Downwinders와 괴물; 눈·먼지와 핵겨울

주장 한계: 진단·피폭·원주민 정체성·오염·기후 인과는 픽셀 판정 금지;핵겨울 연구의 후대 연대를 보존

근거: [S38](https://www.nps.gov/mapr/learn/historyculture/downwinders.htm) (body_excerpt), [S39](https://www.epa.gov/navajo-nation-uranium-cleanup/section-32-33-mines) (indexed_body_excerpt), [S40](https://ntrs.nasa.gov/citations/19840033254) (abstract_metadata)

## X11 — A173, A175, A179, A180, A183, A185, A186, A187, A188

context / P0 / 역할 제안: narrative_clue, world

비윤리 실험·신체 대체·정신 지배·우생학·성적 감금·강압은 권력·의도·동의 문제의 연구 문맥으로 보존한다.

성분: 

관계: 

혼동 경계: 흰 가운과 광기; 구속 외형과 성적 강압; 피폭 피해와 즉각적 괴수화

주장 한계: 어떤 항목도 선정성·폭력성 때문에 조사에서 삭제하지 않음;비동의·성적 폭력은 생성 장면 초안으로 변환하지 않음

근거: [S41](https://ehss.energy.gov/ohre/roadmap/whitehouse/exesum.html) (body_excerpt), [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## X12 — A182, A189, A190, A191

context / P1 / 역할 제안: narrative_clue, aftermath_trace

침공·바디 호러·고어·로봇 반란은 사건 문맥;현재 가시 구조·손상·거리·접촉은 별도 선택한다.

성분: 

관계: 

혼동 경계: 기계의 정지와 반란; 붉은 자국과 피·살상 원인; 비인간과 악의

주장 한계: 인과·실제 사망·권리·의도는 한 장으로 확정하지 않음;고어 상세 해부는 기존 전문 자료와 의미 검토 뒤 후속

근거: [S32](https://www.loc.gov/static/programs/national-film-preservation-board/documents/forbidden_planet.pdf) (pdf_text_excerpt), [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt), [S42](https://www.janusfilms.com/films/1856) (licensor_synopsis)

## L09 — A103

proxy / P1 / 역할 제안: location, background_element

공공 전망 테라스의 성인 방문객들이 난간에서 먼 사막 지평선을 바라본다.

성분: deck = A public observation terrace; viewers = Adult visitors at a railing; horizon = A distant desert horizon

관계: viewers → on → deck; viewers → face → horizon

혼동 경계: 원자력 관광과 일반 전망대; 오락의 외형과 실제 핵실험 관람

주장 한계: 역사적 관광 맥락은 출처로만 연결;픽셀은 관람 장소만 보여주며 실제 폭발·안전·관광객의 태도를 입증하지 않음

근거: [S29](https://thelibrarydistrict.org/blogs/post/miss-atomic-bomb-icon-of-the-atomic-age/) (indexed_curatorial_excerpt), [S33](https://www.loc.gov/static/programs/national-film-preservation-board/documents/AtomicCafe.pdf) (pdf_text_excerpt)

## F09 — A080

still / P1 / 역할 제안: object_structure, surface_pattern

두 개의 점감형 팔이 넓고 각진 굽힘에서 만나는 비대칭 부메랑형 장식이 보인다.

성분: shape = An asymmetrical bent decorative shape; arms = Two tapering arms meeting at one broad angled bend

관계: arms → part_of → shape

혼동 경계: 오목 홈이 있는 강낭콩형; 모든 유기형의 동의어

주장 한계: 형태만 평가;실제 투척 도구·특정 문화의 진품으로 판정하지 않음

근거: [S21](https://ahf.nuclearmuseum.org/ahf/history/atomic-age-design/) (body_excerpt)

## W09 — A111

proxy / P1 / 역할 제안: surface_material, garment_detail

금속처럼 보이는 직물 의상에 부드러운 천 주름이 생기고 고운 직조 표면에서 반사가 잘게 끊긴다.

성분: garment = A metallic-looking woven garment; folds = Soft fabric folds; weave = A fine visible woven surface catching broken reflections

관계: folds → part_of → garment; weave → on → garment

혼동 경계: 광택 비닐 시트·딱딱한 판금; 금속성 반사와 섬유 조성

주장 한계: 금속사·코팅·섬유 비율은 외형으로 확정하지 않음;직조가 가려지면 부분 판정

근거: [S25](https://www.vam.ac.uk/articles/an-introduction-to-1960s-fashion) (body_excerpt)


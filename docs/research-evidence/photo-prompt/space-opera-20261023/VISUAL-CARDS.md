# 시각 의미 카드 72개

모든 장면은 선택형 저술안이다. sources.json의 출처는 정의·제약·작품 맥락만 지지하며, 구성·재료·상태·표시값의 정확한 픽셀 사실을 승인하지 않는다. `NOT_RUN`, `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 유지한다.

## V01 · 격납고가 구분되는 대형 함체

쐐기형 선체 배면에 움푹 들어간 격납고가 있고 작은 셔틀이 조명 켜진 개구부 안에 놓인다.

A wedge-shaped hull has a recessed belly hangar; a small shuttle sits inside its illuminated opening.

- 소유자/성분: hull: large wedge hull; hangar: recessed belly hangar; shuttle: small shuttle
- 방향 관계: hangar → part_of → hull; shuttle → inside → hangar
- 혼동: 삼각형 전투기·선체 표면에 그린 사각형
- 주장 한계: 형상만으로 전함 등급·제국 소속·정확한 크기를 단정하지 않는다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V02 · 모함과 탑재기의 척도

훨씬 큰 모함 선체의 서로 다른 열린 격납 구획에 소형 기체들이 놓인다.

Several small craft occupy separate open bays along one much larger carrier hull.

- 소유자/성분: carrier: large carrier hull; bays: separate open bays; craft: small craft
- 방향 관계: bays → part_of → carrier; craft → inside → bays
- 혼동: 항공모함 위에 우주 배경만 추가·같은 크기 배들
- 주장 한계: 항모 기능을 암시하되 실제 탑재량·출격 순서는 별도 근거다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V03 · 외부 컨테이너 화물선

작은 기밀 승무원 모듈 뒤 열린 척추형 프레임에 화물 컨테이너가 고정된다.

Cargo containers sit in an open spine-frame behind a small pressurized crew module.

- 소유자/성분: crew: small pressure module; frame: open longitudinal frame; cargo: cargo containers
- 방향 관계: frame → behind → crew; cargo → secured_to → frame
- 혼동: 여객선 창문·무장 함체와 화물 기능 혼동
- 주장 한계: 독립 무역상·합법 거래 여부는 외형으로 결정되지 않는다.
- 제안 슬롯: object_structure, prop_state; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V04 · 탐사선의 분리된 계측 붐

작은 탐사선 선체에 긴 센서 붐이 달리고 추진기 군과 거리를 둔다.

A compact survey hull carries a long sensor boom separated from its thruster cluster.

- 소유자/성분: hull: survey hull; boom: sensor boom; thrusters: thruster cluster
- 방향 관계: boom → attached_to → hull; thrusters → attached_to → hull; boom → separated_from → thrusters
- 혼동: 장식 안테나·우주전함 자동 변환
- 주장 한계: 탐사 목적·감도·자기 간섭 제거 성능은 사진으로 입증하지 않는다.
- 제안 슬롯: object_structure; 잠정 판단: new
- 출처: [T01](sources.json); [T02](sources.json); [T04](sources.json); [M06](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V05 · 세대우주선의 공동 재배구역

선내 재배장이 공동 생활 갑판으로 이어지고 서로 다른 연령대의 사람들이 식용 작물 화단을 돌본다.

A shipboard garden opens onto shared living decks where people of different ages tend food beds.

- 소유자/성분: garden: shipboard garden; decks: shared living decks; people: mixed-age residents; beds: food beds
- 방향 관계: garden → opens_onto → decks; people → tend → beds; beds → inside → garden
- 혼동: 캡슐 몇 개로 세대선 표현·우주 온실 하나
- 주장 한계: 여러 세대의 실제 계승·여행 기간·출산 정책은 서사로 유지한다.
- 제안 슬롯: location, relational_action; 잠정 판단: refine
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V06 · 개별 캡슐이 있는 동면실

닫힌 투명 덮개 캡슐마다 누운 성인이 있고 개별 서비스 배관이 연결된다.

Closed transparent-lidded pods contain reclining adults, each with a separate service line.

- 소유자/성분: pods: closed individual pods; adults: reclining adults; lines: separate service lines
- 방향 관계: adults → inside → pods; lines → connected_to → pods
- 혼동: 영안실·구속 감금실·열린 침대
- 주장 한계: 동면·저체온·생존·의식·동의는 외형으로 확정하지 않는다.
- 제안 슬롯: object_structure, body_pose; 잠정 판단: refine
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V07 · 이동 세계의 내부 시가지

주거 밀집 구역이 큰 정비 리브를 가진 함체 외피 아래 굽어 이어진다.

A dense residential district curves beneath an enclosing ship hull with large maintenance ribs.

- 소유자/성분: district: residential district; hull: enclosing ship hull; ribs: maintenance ribs
- 방향 관계: hull → encloses → district; ribs → part_of → hull
- 혼동: 행성도시·보통 우주정거장·평면 도시 콜라주
- 주장 한계: 이동 중임·자급률·인구는 별도 정보다.
- 제안 슬롯: location, spatial_depth; 잠정 판단: new
- 출처: [T05](sources.json); [T06](sources.json); [T08](sources.json); [T15](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V08 · 생체막과 기계 골조의 생체함

경계가 있는 반투명 막이 리브형 선체 골조를 감싸고 기계식 도킹 클램프가 가장자리를 잡는다.

A bounded translucent membrane wraps a ribbed hull frame while mechanical docking clamps grip its rim.

- 소유자/성분: membrane: translucent outer membrane; frame: ribbed hull frame; clamps: mechanical docking clamps
- 방향 관계: membrane → wraps → frame; clamps → grip → frame
- 혼동: 촉수 우주선 한 단어·살아 있는 갑옷
- 주장 한계: 생명·통증·재생·의식은 소재 닮음으로 입증되지 않는다.
- 제안 슬롯: surface_material, anatomical_connection; 잠정 판단: refine
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V09 · 창이 있는 함교와 내부 정보실

창이 있는 조종 갑판과 콘솔이 둘러싼 내부 전술실이 격벽 문으로 구분된다.

A windowed piloting deck is separated by a bulkhead doorway from an interior tactical room lined with consoles.

- 소유자/성분: bridge: windowed piloting deck; cic: interior tactical room; door: bulkhead doorway; consoles: tactical consoles
- 방향 관계: door → between → bridge; door → between → cic; consoles → inside → cic
- 혼동: 우주 창문이 모든 전투정보실의 필수 조건
- 주장 한계: 함교와 CIC의 배치는 선택안이며 보편 설계가 아니다.
- 제안 슬롯: location, object_structure; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V10 · 안전줄 양 끝이 보이는 선외 작업

압력복 작업자가 선체 레일을 잡고 연속된 안전줄이 복장의 하네스와 별도 선체 고정점을 연결한다.

A suited worker grips a hull rail; a continuous tether joins the suit harness to a separate hull anchor.

- 소유자/성분: worker: suited worker; harness: suit harness; tether: continuous tether; anchor: hull anchor; rail: hull rail
- 방향 관계: harness → worn_by → worker; tether → joins → harness; tether → joins → anchor; worker → grips → rail
- 혼동: 한쪽 끝만 보이는 줄·스쿠버 호스·패션 비행복
- 주장 한계: 밀폐 성능·산소 잔량·실제 연결 강도·궤도는 입증하지 않는다.
- 제안 슬롯: contact_point, wearable_accessory; 잠정 판단: refine
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V11 · 두 경계를 갖는 에어록

짧은 방이 닫힌 안쪽 해치와 선체 외부로 열린 바깥 해치 사이에 놓인다.

A short chamber lies between a closed inner hatch and an outer hatch opening toward the hull exterior.

- 소유자/성분: chamber: short transition chamber; inner: inner hatch; outer: outer hatch; exterior: hull exterior
- 방향 관계: inner → bounds → chamber; outer → bounds → chamber; outer → opens_onto → exterior
- 혼동: 엘리베이터·문 두 개 달린 복도·hair lock
- 주장 한계: 압력 전이·인터록·절차 성공을 현재 문 상태로 단정하지 않는다.
- 제안 슬롯: location, object_structure; 잠정 판단: reuse
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V12 · 이온 추진기와 전력 공급의 관계

짐벌에 달린 이온 추진기가 우주선 본체 뒤에 있고 넓은 태양전지 배열이 본체 양옆으로 펼쳐진다.

A gimbaled ion thruster is mounted at a spacecraft bus rear; broad solar arrays extend from the bus sides.

- 소유자/성분: bus: spacecraft bus; thruster: gimbaled ion thruster; arrays: solar arrays
- 방향 관계: thruster → mounted_on → bus; arrays → extend_from → bus
- 혼동: 거대 파란 화염·전력 패널과 방열판 동일시
- 주장 한계: 분사광은 노출 조건에 좌우되며 추력·FTL·가속 성능을 뜻하지 않는다.
- 제안 슬롯: object_structure; 잠정 판단: new
- 출처: [T01](sources.json); [T02](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V13 · 돛의 장력 구조

얇은 반사 돛이 작은 중심 우주선에서 뻗은 네 긴 붐 사이에 펼쳐진다.

A thin reflective sail spans four long booms extending from a compact central spacecraft.

- 소유자/성분: sail: thin reflective sail; booms: four long booms; bus: central spacecraft
- 방향 관계: sail → spans → booms; booms → extend_from → bus
- 혼동: 연소 엔진 불꽃·파라솔·단단한 태양전지 날개
- 주장 한계: 광압 가속·전력 생산·정확한 전개 성공은 별도 검증이다.
- 제안 슬롯: object_structure, surface_material; 잠정 판단: new
- 출처: [T04](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V14 · 방열판의 배관과 뿌리

밝은 방열판이 호일 단열 서비스 모듈 옆으로 뻗고 보이는 배관이 패널 뿌리까지 이어진다.

A pale radiator panel extends beside a foil-wrapped service module; a visible pipe reaches the panel root.

- 소유자/성분: panel: pale radiator panel; module: foil-wrapped service module; pipe: visible heat-transfer pipe
- 방향 관계: panel → extends_from → module; pipe → joins → module; pipe → joins → panel
- 혼동: 태양전지 셀·비행기 날개·대기 속 냉각 핀
- 주장 한계: 관측은 연결 구조까지이며 방열량·온도는 계측이 필요하다.
- 제안 슬롯: object_structure, surface_material; 잠정 판단: reuse
- 출처: [T03](sources.json); [M04](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V15 · 관문의 구멍과 함선 통과 방향

함선이 고정된 큰 고리의 빈 개구부를 향하고 선체와 고리 골조는 분리되어 있다.

A ship points through the empty aperture of a large anchored ring; its hull remains separate from the ring frame.

- 소유자/성분: ship: approaching ship; ring: anchored gate ring; aperture: empty central aperture
- 방향 관계: aperture → inside → ring; ship → points_toward → aperture
- 혼동: 자유 부유 토러스 거주지·함선 자체 링 엔진
- 주장 한계: 선택형 허구 관문이며 실제 웜홀·순간이동·도착지는 입증하지 않는다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [T13](sources.json); [C05](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V16 · 초공간의 작품별 선택 표현

작은 함선 한 척을 파란 발광 터널이 둘러싸며 빛줄기가 실루엣 뒤로 모인다.

One small ship is framed by a blue luminous tunnel whose streaks converge behind its silhouette.

- 소유자/성분: ship: small ship; tunnel: blue luminous tunnel; streaks: converging streaks
- 방향 관계: tunnel → surrounds → ship; streaks → part_of → tunnel
- 혼동: 워프·점프·웜홀을 하나의 필수 파란 터널로 통합
- 주장 한계: 공식 사례에서 착안한 선택 표현이며 모든 FTL의 정의가 아니다.
- 제안 슬롯: space_condition, lighting; 잠정 판단: new
- 출처: [T13](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V17 · 광통신 터미널의 조준축

우주선의 광학 터미널이 별도 삽입 화면에 표시된 먼 지상 수신소를 향한다.

An optical terminal on a spacecraft points toward a distant ground dish shown in a separate inset.

- 소유자/성분: terminal: spacecraft optical terminal; spacecraft: spacecraft; inset: ground-station inset
- 방향 관계: terminal → mounted_on → spacecraft; terminal → points_toward → inset
- 혼동: 진공에서 항상 선명한 광선·즉시 응답 앤서블
- 주장 한계: 삽입 화면은 설명 도해이며 실제 링크·빛의 지연 시간을 증명하지 않는다.
- 제안 슬롯: object_structure, composition; 잠정 판단: new
- 출처: [T01](sources.json); [T02](sources.json); [T04](sources.json); [M06](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V18 · 성도 테이블과 항로의 소유자

장교가 테이블에 귀속된 성도에서 표시된 두 성계를 연결하는 한 항로를 가리킨다.

An officer points to one route connecting two marked systems on a table-bound star map.

- 소유자/성분: officer: officer; map: table-bound star map; route: single connecting route; systems: two marked systems
- 방향 관계: route → connects → systems; route → displayed_on → map; officer → points_to → route
- 혼동: 관객 전용 HUD·막연한 별 배경·광년을 시간으로 오독
- 주장 한계: 지도상 거리·항행 가능·위험 회피·통제권의 진실은 별도다.
- 제안 슬롯: prop, relational_action; 잠정 판단: new
- 출처: [M02](sources.json); [M03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V19 · 중앙이 빈 토러스 거주지

외부 시점에서 두꺼운 거주 토러스가 스포크로 중심 허브에 연결되고 허브 주위 공간이 비어 있다.

An external view shows a thick inhabited torus connected by spokes to a central hub, leaving open space around the hub.

- 소유자/성분: torus: inhabited torus; spokes: radial spokes; hub: central hub; void: open central space
- 방향 관계: spokes → join → torus; spokes → join → hub; void → inside → torus
- 혼동: 다이슨 구·행성 둘레의 링·평면 원판
- 주장 한계: 형태는 회전 속도·중력값·거주 적합성의 증거가 아니다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [T05](sources.json); [T06](sources.json); [T08](sources.json); [T15](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V20 · 실린더의 마주 보는 내부 지면

긴 원통 거주지 안에서 식생 지면이 양옆으로 올라가 보이는 중심축 건너 머리 위까지 이어진다.

Inside a long cylindrical habitat, planted ground curves upward on both sides and continues overhead across the visible axis.

- 소유자/성분: ground: curving inhabited inner ground; axis: visible longitudinal axis; buildings: ground-mounted buildings
- 방향 관계: ground → curves_around → axis; buildings → supported_by → ground
- 혼동: 한 평면에 선 도시·원통 터널 천장에 가짜 도시 무늬
- 주장 한계: 원근·지지 방향을 판정하고 실제 회전·가속은 별도다.
- 제안 슬롯: location, spatial_depth; 잠정 판단: new
- 출처: [T05](sources.json); [T06](sources.json); [T08](sources.json); [T15](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V21 · 항성을 둘러싼 띠 세계

거대한 띠 고리가 중심 항성을 두르고 가까운 구간에는 높은 가장자리 벽 사이의 거주 내면이 보인다.

A vast ribbon-like ring surrounds a central star; a nearer segment reveals an inhabited inner surface bounded by raised rim walls.

- 소유자/성분: ring: vast ribbon ring; star: central star; surface: inhabited inner surface; rims: raised rim walls
- 방향 관계: ring → surrounds → star; surface → part_of → ring; rims → bound → surface
- 혼동: 작은 스탠퍼드 토러스·행성 고리·다이슨 군집
- 주장 한계: 허구의 척도와 도해를 명시하며 안정성·실제 공전은 주장하지 않는다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: defer
- 출처: [T06](sources.json); [M10](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.
- 채택 전 공백: Ringworld 원전/공식 디자인의 띠·벽·항성 관계를 본문으로 확인해야 한다. M10은 발췌인 hosted concordance다.

## V22 · 분리된 다이슨 군집

서로 분리된 수집 위성들이 실루엣 사이 틈을 남긴 채 항성을 두르고 항성 일부가 노출된다.

Many distinct collector satellites encircle a star with clear gaps between their silhouettes, leaving the star partly exposed.

- 소유자/성분: satellites: separate collector satellites; star: partly exposed star; gaps: clear gaps
- 방향 관계: satellites → surround → star; gaps → separate → satellites
- 혼동: 매끈한 고체 껍질·소행성대·링월드
- 주장 한계: 에너지 포획률·공전 안정성·문명 등급을 단정하지 않는다.
- 제안 슬롯: object_structure; 잠정 판단: new
- 출처: [T08](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V23 · 돔의 압력 경계와 출입실

투명 돔이 건물과 식생 지면을 감싸고 작은 이중문 전이실이 아래 가장자리에 있다.

A clear dome encloses buildings and planted ground; a small two-door vestibule interrupts its lower rim.

- 소유자/성분: dome: clear dome; buildings: interior buildings; ground: planted ground; vestibule: two-door vestibule
- 방향 관계: dome → encloses → buildings; dome → encloses → ground; vestibule → part_of → dome
- 혼동: 유리 온실 하나·대기 전체 테라포밍 완료
- 주장 한계: 기밀·산소·폐쇄 순환 완성·외부 독성은 별도 정보다.
- 제안 슬롯: location, object_structure; 잠정 판단: new
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V24 · 미완성 선체와 조선소 골조

미완성 함체가 더 큰 열린 갠트리 안에 있고 서비스 암이 드러난 선체 구역으로 뻗는다.

An incomplete ship hull sits within a larger open gantry, with service arms reaching exposed hull sections.

- 소유자/성분: hull: incomplete ship hull; gantry: larger open gantry; arms: service arms
- 방향 관계: hull → inside → gantry; arms → attached_to → gantry; arms → reach_toward → hull
- 혼동: 완성 함선과 장식 고리·격납고와 건조 설비 혼동
- 주장 한계: 건조 과정·궤도·작업 성공을 정지 구조로 입증하지 않는다.
- 제안 슬롯: location, object_structure; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V25 · 레일과 코일의 구조 비교

설명 절개도에서 평행 도전 레일 두 개가 있는 총열과 반복 코일에 둘러싸인 별도 총열이 나란히 놓인다.

A labeled cutaway pairs a barrel with two parallel conducting rails and a separate barrel surrounded by repeated coils.

- 소유자/성분: rails: two parallel rails; barrel_a: rail barrel; coils: repeated coils; barrel_b: coil barrel
- 방향 관계: rails → line → barrel_a; coils → surround → barrel_b
- 혼동: 그냥 미래 총·레이저 빔과 구조 동일시
- 주장 한계: 구조 설명 도해이며 실제 작동·탄속·제작 가능성을 보증하지 않는다.
- 제안 슬롯: object_structure; 잠정 판단: defer
- 출처: [M09](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.
- 채택 전 공백: M09는 레일건만 지지한다. 코일건 원전 공학 자료를 확보하기 전 두 구조 비교 채택을 보류한다.

## V26 · 함체와 방어 포탑의 조준

함체의 작은 추적 포탑이 선체 실루엣 밖의 접근 미사일을 향한다.

A small tracking turret on a hull points toward an incoming missile drawn outside the hull silhouette.

- 소유자/성분: turret: small tracking turret; hull: protected hull; missile: incoming missile
- 방향 관계: turret → mounted_on → hull; turret → aims_at → missile
- 혼동: 대함 주포·명중 없는 화려한 빔 폭포
- 주장 한계: 방어 성공·표적 속도·자동 추적은 시간·계측 문제다.
- 제안 슬롯: relational_action, object_structure; 잠정 판단: new
- 출처: [T11](sources.json); [T12](sources.json); [M09](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V27 · 방어막과 선체를 분리한 접점

굽은 반투명 경계가 함체와 떨어져 있고 국소 발광 충돌점이 경계 표면에 놓인다.

A curved translucent barrier stands apart from the hull; a localized luminous impact sits on the barrier surface.

- 소유자/성분: barrier: curved translucent barrier; hull: protected hull; impact: localized luminous contact
- 방향 관계: barrier → separated_from → hull; impact → on_surface_of → barrier
- 혼동: 선체 자체 발광·렌즈 플레어·성운
- 주장 한계: 허구 방어막의 선택 도상이며 방호 성능·에너지량은 주장하지 않는다.
- 제안 슬롯: space_condition, contact_point; 잠정 판단: new
- 출처: [T11](sources.json); [T12](sources.json); [M09](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V28 · 승선 통로 양쪽의 함체

밀폐 승선관이 서로 다른 두 선체의 해치를 연결하고 압력복 인물들이 관 안에 있다.

An enclosed boarding tube joins two separate hull hatches while suited figures move within the tube.

- 소유자/성분: tube: enclosed boarding tube; hatch_a: first hull hatch; hatch_b: second hull hatch; figures: suited figures
- 방향 관계: tube → joins → hatch_a; tube → joins → hatch_b; figures → inside → tube
- 혼동: 단순 도킹·떠 있는 인물·상대 선박 소유자 혼동
- 주장 한계: 적대 강습·허가 여부·전투 결과는 외형이 아닌 맥락이다.
- 제안 슬롯: anatomical_connection, location; 잠정 판단: new
- 출처: [T11](sources.json); [T14](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V29 · 통행 통제와 기다리는 화물선

화물선들이 별도 순찰함과 검문소가 지키는 좁은 통행 구역 밖에 대기한다.

Cargo ships wait outside a narrow transit corridor watched by separate patrol ships and a checkpoint station.

- 소유자/성분: cargo: waiting cargo ships; corridor: transit corridor; patrol: patrol ships; station: checkpoint station
- 방향 관계: cargo → outside → corridor; patrol → flank → corridor; station → beside → corridor
- 혼동: 일반 교통 대기·함대전만으로 경제 봉쇄 단정
- 주장 한계: 봉쇄의 법적 성격·의도·지속 기간·기아 인과는 추가 서사다.
- 제안 슬롯: composition, situation_context; 잠정 판단: new
- 출처: [C02](sources.json); [C04](sources.json); [C06](sources.json); [C08](sources.json); [C14](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V30 · 분열된 행성의 파편 경계

허구 행성이 밝게 드러난 내부 주위로 분리된 큰 곡면 파편들로 갈라져 있다.

A fictional planet is split into large separated curved fragments around a bright exposed interior.

- 소유자/성분: planet: fictional planet; fragments: separated curved fragments; interior: bright exposed interior
- 방향 관계: fragments → surround → interior; interior → between → fragments
- 혼동: 행성 멸균·지표 유리화·엑스테르미나투스 하나로 통합
- 주장 한계: 현재 허구 파편 형태만 보이며 무기·원인·모든 생명 사망은 입증하지 않는다.
- 제안 슬롯: object_structure, aftermath_trace; 잠정 판단: new
- 출처: [T11](sources.json); [T12](sources.json); [M09](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V31 · 유리질 표면과 대피선의 대비

검은 유리질 지면이 손상 도시 쪽으로 이어지고 작은 대피선이 온전한 착륙장 위에 있다.

Dark glass-like terrain runs toward a damaged city while a small evacuation craft stands on an intact landing pad.

- 소유자/성분: terrain: glass-like terrain; city: damaged city; craft: evacuation craft; pad: intact landing pad
- 방향 관계: terrain → extends_toward → city; craft → supported_by → pad
- 혼동: 행성 폭발·화산 흑요석·멸균 완료
- 주장 한계: 유리화 원인·학살 의도·행성 전체 범위·무생물 상태는 단정하지 않는다.
- 제안 슬롯: surface_material, aftermath_trace; 잠정 판단: defer
- 출처: [C18](sources.json); [T12](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.
- 채택 전 공백: 지표 유리화의 작품별 피해 범위와 원인을 공식 원전에서 확인해야 한다. C18은 Exterminatus 명령이지 glassing 기전이 아니다.

## V32 · 서로 다른 대기 구획의 외교

서로 다른 형태의 두 사절이 투명 밀폐 칸막이 양쪽에서 마주 보고 각 구획에 별도 대기 서비스 연결부가 있다.

Two differently shaped delegates face each other across a transparent sealed partition, each with its own atmosphere-service fittings.

- 소유자/성분: delegate_a: first delegate; delegate_b: second delegate; partition: sealed transparent partition; fittings: separate service fittings
- 방향 관계: partition → separates → delegate_a; partition → separates → delegate_b; fittings → serve → delegate_a; fittings → serve → delegate_b
- 혼동: 방역실·종족 분리 차별을 환경 필요와 동일시
- 주장 한계: 실제 외계 생화학·최초 접촉·필수 분리 여부는 설정이다.
- 제안 슬롯: location, relational_action; 잠정 판단: new
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V33 · 화자 사이에 귀속된 번역 장치

두 화자가 사이의 탁상 번역 장치를 향하고 장치에는 구분된 입력·출력 표시가 있다.

Two speakers address a tabletop translation device between them, with distinct input and output indicators.

- 소유자/성분: speaker_a: first speaker; speaker_b: second speaker; device: tabletop translation device; indicators: input-output indicators
- 방향 관계: device → between → speaker_a; device → between → speaker_b; indicators → part_of → device
- 혼동: 목걸이 장식·텔레파시·번역 자막과 극중 장치 혼동
- 주장 한계: 번역 정확성·의도 이해·협상 성공은 사진으로 판단하지 않는다.
- 제안 슬롯: prop, relational_action; 잠정 판단: new
- 출처: [C03](sources.json); [C05](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V34 · 비인간형 사절의 도달 범위

방사형 몸의 사절이 두 관절 사지로 낮은 공용 탁자에 토큰을 놓고 맞은편에 인간 사절이 있다.

A radial-bodied delegate uses two articulated limbs to place a token on a low shared table opposite a human envoy.

- 소유자/성분: alien: radial-bodied delegate; limbs: two articulated limbs; token: token; table: low shared table; human: human envoy
- 방향 관계: limbs → part_of → alien; limbs → contact → token; token → on → table; human → opposite → alien
- 혼동: 인간 몸에 촉수 장식·잡을 수 없는 손과 탁자 높이
- 주장 한계: 외형은 사피언스·의식·언어·성별 체계를 입증하지 않는다.
- 제안 슬롯: body_form, contact_point; 잠정 판단: new
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V35 · 숙주와 부착체의 별도 소유자

작은 부착 생물이 큰 숙주의 경계 있는 피부 접점과 맞닿으며 두 몸의 윤곽이 구분된다.

A small attached organism meets a larger host at a bounded skin interface; both body outlines remain distinguishable.

- 소유자/성분: host: larger host; organism: small attached organism; interface: bounded skin interface
- 방향 관계: interface → part_of → host; organism → attached_to → interface
- 혼동: 장신구·문신·피부 융합·공생과 기생 단정
- 주장 한계: 상리 이익·피해·의지 통제·동의·종속 방향은 별도다.
- 제안 슬롯: anatomical_connection; 잠정 판단: refine
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V36 · 여러 몸과 하나의 통신 허브

서로 구분되는 몸들이 보이는 선으로 하나의 중심 통신 허브에 연결되고 각 몸에 별도 접속점이 있다.

Several distinct bodies connect by visible lines to one central communication hub; each body has a separate endpoint.

- 소유자/성분: bodies: distinct bodies; lines: separate visible lines; hub: communication hub
- 방향 관계: lines → join → bodies; lines → join → hub
- 혼동: 무리 정렬·공유 의식·한 자아·다수 자아 합성을 혼동
- 주장 한계: 보이는 것은 연결 토폴로지이며 인격 수·군체 정신은 문맥으로 남긴다.
- 제안 슬롯: anatomical_connection, relational_action; 잠정 판단: refine
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V37 · 안드로이드의 기계 내부

성인 형태 안드로이드의 한쪽 전완 패널이 열려 온전한 인공 외피 아래 기계 구동부가 보인다.

An adult-shaped android has one open forearm panel revealing mechanical actuators beneath an intact synthetic outer shell.

- 소유자/성분: android: adult-shaped android; panel: open forearm panel; actuators: mechanical actuators; shell: synthetic outer shell
- 방향 관계: panel → part_of → android; actuators → beneath → shell; shell → part_of → android
- 혼동: 사람 보철·갑옷·빨간 눈으로 악의·성적 서비스 판정
- 주장 한계: 기계 구조는 의식·시민권·자율성·성적 목적을 입증하지 않는다.
- 제안 슬롯: body_region, object_structure; 잠정 판단: refine
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V38 · 살아 있는 피부와 임플란트 경계

기계 전완이 살아 있는 듯한 상완 피부와 보이는 접점에서 만나고 별도 외부 서비스 포트가 있다.

A mechanical forearm meets living-looking upper-arm skin at a visible interface, with a separate external service port.

- 소유자/성분: forearm: mechanical forearm; skin: upper-arm skin; interface: visible body-machine interface; port: external service port
- 방향 관계: interface → joins → forearm; interface → joins → skin; port → part_of → forearm
- 혼동: 전신 로봇·장갑 소매·기계 손 소유자 바뀜
- 주장 한계: 생체 조직의 실제 생존·수술 이력·자발적 개조는 입증하지 않는다.
- 제안 슬롯: anatomical_connection, body_region; 잠정 판단: refine
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V39 · 함선과 연결된 지휘 인터페이스

인간 지휘관이 함선 전체 상태 화면을 보고 화면의 도식에서 여러 구획이 하나의 핵심 노드에 연결된다.

A human commander faces a ship-wide status display whose diagram links several compartments to one core node.

- 소유자/성분: commander: human commander; display: ship-wide status display; compartments: displayed compartments; node: displayed core node
- 방향 관계: compartments → linked_to → node; node → displayed_on → display; commander → faces → display
- 혼동: 빨간 카메라·얼굴 홀로그램만으로 인격화
- 주장 한계: 함선의 자아·지휘권·도덕성·Minds 정전은 도식과 별도다.
- 제안 슬롯: prop, visible_text; 잠정 판단: new
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V40 · 독립 단말 앞의 닮은 두 성인

닮은 두 성인이 서로 다른 단말 앞에 서고 각 단말에는 서로 다르게 표시된 개인 기록이 있다.

Two similar-looking adults stand at separate terminals showing different labeled personal logs.

- 소유자/성분: adult_a: first adult; adult_b: second adult; terminal_a: first terminal; terminal_b: second terminal
- 방향 관계: adult_a → uses → terminal_a; adult_b → uses → terminal_b; adult_a → separate_from → adult_b
- 혼동: 쌍둥이·한 사람 거울상·복제와 기억 복사 동일시
- 주장 한계: 현재 분리된 몸과 묘사된 기록만 보이며 정신 분기·혈연은 입증하지 않는다.
- 제안 슬롯: relational_action, prop; 잠정 판단: context
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V41 · 몸의 환경 적응과 외부 장비의 구분

수생 적응 허구 성인에게 목 아가미 주름과 물갈퀴 손가락이 보이고 옆에 사용하지 않는 호흡 장비가 있다.

An aquatic-adapted fictional adult has visible neck gill folds and webbed fingers while standing beside unused breathing equipment.

- 소유자/성분: adult: aquatic-adapted adult; gills: neck gill folds; fingers: webbed fingers; gear: unused breathing gear
- 방향 관계: gills → part_of → adult; fingers → part_of → adult; gear → beside → adult
- 혼동: 스쿠버 장비·행성을 바꾸는 테라포밍·물고기 장식
- 주장 한계: 형태 선택안이며 실제 호흡·유전 개조·유전성은 별도다.
- 제안 슬롯: body_form, body_region; 잠정 판단: new
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V42 · 몸 밖의 발생 용기

밀폐 투명 발생 용기 안에 웅크린 생물 형태 하나가 있고 튜브는 용기 벽에 연결된다.

A sealed transparent developmental vessel contains one curled biological form with a tube attached to the vessel wall.

- 소유자/성분: vessel: sealed developmental vessel; form: curled biological form; tube: service tube; wall: vessel wall
- 방향 관계: vessel → encloses → form; tube → attached_to → wall; wall → part_of → vessel
- 혼동: 인체 내부 임신·표본 병·가슴이나 성적 신체 자동 추가
- 주장 한계: 인간 완전 체외 임신의 실현·생존·발달 단계·친권·강제성은 주장하지 않는다.
- 제안 슬롯: object_structure, anatomical_connection; 잠정 판단: defer
- 출처: [M07](sources.json); [M08](sources.json); [C19](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.
- 채택 전 공백: M07 본문 접근 실패·M08 발췌만 확보. 동물의 부분 발생 지원과 인간 완전 체외 임신을 구분한 원전 재검토가 필요하다.

## V43 · 권좌와 기념비적 축선

단일 높은 좌석이 긴 대칭 홀의 끝에 있고 작은 수행원들이 가문별 깃발 아래 서 있다.

A single raised seat terminates a long symmetrical hall; small attendants stand below house-specific banners.

- 소유자/성분: seat: single raised seat; hall: long symmetrical hall; attendants: small attendants; banners: house-specific banners
- 방향 관계: seat → at_end_of → hall; attendants → below → seat; banners → inside → hall
- 혼동: 검정색·악역·특정 현실 정권 표식으로 자동 치환
- 주장 한계: 위계적 공간 선택안이며 제국·정통성·선악은 확정하지 않는다.
- 제안 슬롯: location, composition; 잠정 판단: new
- 출처: [C02](sources.json); [C04](sources.json); [C06](sources.json); [C08](sources.json); [C14](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V44 · 대표석이 분리된 의회 공간

원형 회의장에서 사절들이 같은 높이의 책상에 앉고 각 책상에 서로 다른 지역 문장이 있다.

Delegates occupy equal-height desks in a circular chamber, each desk bearing a distinct local emblem.

- 소유자/성분: delegates: delegates; desks: equal-height desks; chamber: circular chamber; emblems: distinct local emblems
- 방향 관계: delegates → seated_at → desks; emblems → attached_to → desks; desks → inside → chamber
- 혼동: 원형 배치만으로 민주주의·평등 시민권 판정
- 주장 한계: 대표성·투표권·연방과 국가연합 구분은 제도 정보다.
- 제안 슬롯: composition, location; 잠정 판단: new
- 출처: [C02](sources.json); [C04](sources.json); [C06](sources.json); [C08](sources.json); [C14](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V45 · 가문 인장 교환의 의례

두 성인 대표가 서로 다른 가문 깃발 아래 탁자를 사이에 두고 봉인 상자를 교환한다.

Two adult representatives exchange sealed cases across a table beneath separate family banners.

- 소유자/성분: a: first adult representative; b: second adult representative; cases: sealed cases; table: exchange table; banners: separate family banners
- 방향 관계: a → offers → cases; b → receives → cases; table → between → a; table → between → b
- 혼동: 결혼·인질·외교 협정을 물건 교환만으로 확정
- 주장 한계: 혼인·혈연·자유 의사·왕조 동맹은 서사상 명시해야 한다.
- 제안 슬롯: relational_action, prop; 잠정 판단: new
- 출처: [C02](sources.json); [C04](sources.json); [C06](sources.json); [C08](sources.json); [C14](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V46 · 통행과 자원 접근의 병목

하나의 통제 부스가 화물 대기열과 유일하게 열린 관문 사이에 있고 장벽 뒤에 별도 연료 탱크가 있다.

One control booth sits between a cargo queue and a single open gate, with separate fuel tanks behind the barrier.

- 소유자/성분: booth: control booth; queue: cargo queue; gate: single open gate; tanks: fuel tanks; barrier: access barrier
- 방향 관계: booth → between → queue; booth → between → gate; tanks → behind → barrier
- 혼동: 자원 독점 전체를 금고 하나·스파이스 특정 재료로 자동화
- 주장 한계: 통제 장면은 독점 범위·정당성·통행료의 실제 효력을 입증하지 않는다.
- 제안 슬롯: location, relational_action; 잠정 판단: new
- 출처: [C08](sources.json); [C13](sources.json); [C11](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V47 · 세관 장벽과 화물의 접근

검사관이 검문 장벽 한쪽에서 봉인 화물 상자를 검사하고 소유자는 반대편에 기다린다.

An inspector examines a sealed cargo case on one side of a checkpoint barrier while its owner waits on the other.

- 소유자/성분: inspector: inspector; case: sealed cargo case; barrier: checkpoint barrier; owner: cargo owner
- 방향 관계: inspector → examines → case; barrier → separates → inspector; barrier → separates → owner
- 혼동: 상자·어두운 조명만으로 밀수나 범죄 단정
- 주장 한계: 금지 품목·불법성·소유권의 진실은 문맥이고 표시는 묘사된 주장이다.
- 제안 슬롯: relational_action, prop; 잠정 판단: new
- 출처: [C08](sources.json); [C13](sources.json); [C11](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V48 · 민간 대피선의 승선 배려

승무원이 개인 가방을 든 민간인의 붐비는 소형 수송선 승선을 돕고 옆에는 보급품이 쌓여 있다.

A crew member helps a civilian carrying a personal bag onto a crowded small transport, beside stacked supplies.

- 소유자/성분: crew: crew helper; civilian: civilian with bag; transport: small transport; supplies: stacked supplies
- 방향 관계: crew → supports → civilian; civilian → boards → transport; supplies → beside → transport
- 혼동: 군사 상륙·여객 대기·난민 법적 지위 단정
- 주장 한계: 피난 원인·추방·친족·국적·난민 지위는 외형과 구별한다.
- 제안 슬롯: relational_action, location; 잠정 판단: new
- 출처: [C13](sources.json); [C14](sources.json); [C15](sources.json); [C18](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V49 · 정비 행위와 제의 장치의 병치

로브를 입은 기술자들이 열린 기계 옆에서 공구를 들고 별도 의식 램프와 표장이 작은 제단 선반에 있다.

Robed technicians hold tools beside an opened machine while a separate ritual lamp and emblem stand on a small shrine shelf.

- 소유자/성분: technicians: robed technicians; tools: tools; machine: opened machine; shrine: small shrine shelf; lamp: ritual lamp
- 방향 관계: technicians → hold → tools; tools → beside → machine; lamp → on → shrine
- 혼동: 향·로브만으로 종교·수리 성공·마법 원인 단정
- 주장 한계: 선택적 의례 단서는 신앙·효능·허구 능력을 자동 입증하지 않는다.
- 제안 슬롯: prop, relational_action; 잠정 판단: new
- 출처: [C20](sources.json); [C08](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V50 · 유물과 관찰자의 척도

작은 조사대가 층진 암석에 일부 박힌 거대한 풍화 기하 물체 앞에 서 있다.

A small survey team stands before a huge weathered geometric object partly embedded in layered rock.

- 소유자/성분: team: small survey team; object: weathered geometric object; rock: layered rock
- 방향 관계: object → embedded_in → rock; team → faces → object
- 혼동: 거대함만으로 고대 문명·BDO·외계 기원 확정
- 주장 한계: 연대·제작자·멸망 원인·금지 지식은 별도 출처가 필요하다.
- 제안 슬롯: spatial_depth, aftermath_trace; 잠정 판단: new
- 출처: [T05](sources.json); [T06](sources.json); [T08](sources.json); [T15](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V51 · 출입 제어와 신체 결정의 문맥

성인이 의료 출입문 옆에 서고 방 밖의 별도 담당자가 접근 콘솔을 조작한다.

An adult stands beside a medical doorway whose access console is controlled by a separate official outside the room.

- 소유자/성분: adult: adult patient; door: medical doorway; console: access console; official: separate official
- 방향 관계: adult → beside → door; official → operates → console; console → beside → door
- 혼동: 의료 장비·구속·침묵만으로 강제성 또는 동의 판정
- 주장 한계: 출입 관계만 관찰 가능하다. 강제·생식 정책·동의 부재는 명시 서사로 보존한다.
- 제안 슬롯: situation_context; 잠정 판단: context
- 출처: [C19](sources.json); [C17](sources.json); [M08](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V52 · 두 성인의 독립된 신경 연결

명시적으로 성인인 두 파트너가 떨어져 앉고 각자의 머리 인터페이스가 공용 콘솔에 연결되며 두 사람의 손은 자유롭다.

Two explicitly adult partners sit apart with separate head interfaces linked to a shared console; both hands remain free.

- 소유자/성분: a: first adult partner; b: second adult partner; interfaces: separate head interfaces; console: shared console
- 방향 관계: interfaces → worn_by → a; interfaces → worn_by → b; interfaces → connected_to → console
- 혼동: 전선이 동의·쾌락·강제 조종의 증거라는 단정
- 주장 한계: 동의·사랑·감각 공유 성공·페로몬 강제성은 외형으로 판정하지 않는다.
- 제안 슬롯: anatomical_connection, relational_action; 잠정 판단: new
- 출처: [C19](sources.json); [C17](sources.json); [M08](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V53 · 여러 성인의 공동생활

명시적으로 성인인 여러 거주자가 선내 식사를 나누고 구분된 좌석과 개인 소지품 사이에서 음식을 건넨다.

Several explicitly adult residents share a shipboard meal, passing food between distinct seats and personal belongings.

- 소유자/성분: adults: adult residents; food: shared food; table: shipboard table; belongings: personal belongings
- 방향 관계: adults → seated_at → table; food → passed_between → adults; belongings → beside → table
- 혼동: 식사만으로 다자혼·하렘·혈연·성적 관계 단정
- 주장 한계: 공동생활 외의 관계·동의·혈연·혼인은 서사 정보다.
- 제안 슬롯: relational_action, location; 잠정 판단: new
- 출처: [C15](sources.json); [C03](sources.json); [C13](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V54 · 펄프 의상과 압력복의 환경 분리

명시적으로 성인인 공연자가 밀폐 거주지 안에서 오리지널 금속성 투피스 무대 의상을 입고 별도의 압력복이 보관함에 걸려 있다.

An explicitly adult performer wears an original metallic two-piece stage costume inside a sealed habitat; a separate pressure suit hangs in a locker.

- 소유자/성분: performer: adult performer; costume: metallic two-piece stage costume; habitat: sealed habitat; suit: separate pressure suit; locker: locker
- 방향 관계: costume → worn_by → performer; performer → inside → habitat; suit → inside → locker
- 혼동: 노출 의상을 진공 방호복·성노예·동의·특정 인물 의상으로 자동화
- 주장 한계: 복식·실내 위치만 관찰 가능하며 성적 서비스·강제성·방호 성능은 별도다.
- 제안 슬롯: wardrobe_style, location; 잠정 판단: new
- 출처: [M05](sources.json); [C01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V55 · 사용 부위에 집중된 수선 흔적

함선 해치의 손잡이에는 마모 광택, 걸쇠에는 벗겨진 도색, 옆에는 색이 다른 수리판이 있다.

A ship hatch has polished wear on its handle, chipped paint at the latch, and a mismatched repair plate beside it.

- 소유자/성분: hatch: ship hatch; handle: handle; latch: latch; plate: mismatched repair plate
- 방향 관계: handle → part_of → hatch; latch → part_of → hatch; plate → beside → latch
- 혼동: 모든 면에 무작위 녹·고어·퇴폐로 장르 단정
- 주장 한계: 현재 마모만 보이며 특정 과거 사건·정비 기간은 입증하지 않는다.
- 제안 슬롯: surface_material, aftermath_trace; 잠정 판단: refine
- 출처: [M01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V56 · 물리 매체가 있는 선내 단말

두꺼운 CRT 단말 아래 물리 스위치가 있고 분리 가능한 데이터 카트리지가 표시된 슬롯에 일부 꽂혀 있다.

A thick CRT terminal sits above physical switches; a removable data cartridge is partly inserted in a labeled slot.

- 소유자/성분: crt: thick CRT terminal; switches: physical switches; cartridge: removable cartridge; slot: data slot
- 방향 관계: switches → below → crt; cartridge → inserted_in → slot; slot → part_of → crt
- 혼동: 카세트 음악 컬렉션·아날로그 호러·실제 시대 확정
- 주장 한계: 미래의 물성 선택안이며 저주·고장·기록 진위는 별도다.
- 제안 슬롯: prop, object_structure; 잠정 판단: refine
- 출처: [M02](sources.json); [M03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V57 · 계층별 표면 디테일과 척도

큰 선체 패널 안에 더 작은 출입 해치와 그보다 작은 정비 부속이 있고 작은 작업자가 일관된 척도를 제공한다.

A large hull plate contains a smaller access hatch and still smaller service fittings; a tiny worker provides a consistent scale cue.

- 소유자/성분: plate: large hull plate; hatch: smaller access hatch; fittings: small service fittings; worker: tiny worker
- 방향 관계: hatch → part_of → plate; fittings → attached_to → plate; worker → beside → hatch
- 혼동: 무작위 노이즈·평면 텍스처·모든 부품이 같은 크기
- 주장 한계: 시각 계층은 제작 방식·실제 기능·정확한 크기의 증거가 아니다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [M01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V58 · 장치에 귀속되는 입체 표시

투명 도식 층들이 물리 탁상 방출기 위에 있고 조작자가 가장 가까운 층을 직접 바라본다.

Transparent diagram layers rise above a physical tabletop emitter while an operator looks directly at the nearest layer.

- 소유자/성분: layers: transparent diagram layers; emitter: tabletop emitter; operator: operator
- 방향 관계: layers → above → emitter; operator → looks_at → layers
- 혼동: 관객용 HUD·의상 홀로그래픽 광택·무근거 공중 화면
- 주장 한계: 극중 표시의 선택 도상이며 현실 공중 투사 기술·정보의 진실은 입증하지 않는다.
- 제안 슬롯: prop, relational_action; 잠정 판단: new
- 출처: [M02](sources.json); [M03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V59 · 착용자에 묶인 계급장과 문장

성인 장교의 같은 튜닉에 어깨 계급장과 별도 가문 문장이 있고 두 부착점이 보인다.

An adult officer wears a shoulder rank tab and a separate family crest on the same tunic, with both attachment points visible.

- 소유자/성분: officer: adult officer; tunic: ceremonial tunic; rank: shoulder rank tab; crest: family crest
- 방향 관계: tunic → worn_by → officer; rank → attached_to → tunic; crest → attached_to → tunic
- 혼동: 가문 문장과 군 계급 동일시·타인의 훈장이 전이
- 주장 한계: 표시가 주장하는 소속은 관찰되지만 진짜 권한·세습·충성은 별도다.
- 제안 슬롯: wardrobe_style, wearable_accessory; 잠정 판단: new
- 출처: [C02](sources.json); [C04](sources.json); [C06](sources.json); [C08](sources.json); [C14](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V60 · 압력 선체에 결합된 고딕 구조

버팀벽 같은 리브가 밀폐 선체 외부를 따라가고 실내 첨두 아치가 압력 해치를 둘러싼다.

Buttress-like ribs follow the outside of a sealed ship hull, while a pointed interior arch frames a pressure hatch.

- 소유자/성분: hull: sealed ship hull; ribs: buttress-like ribs; arch: pointed interior arch; hatch: pressure hatch
- 방향 관계: ribs → attached_to → hull; arch → frames → hatch
- 혼동: 교회를 우주 배경에 붙이기·고딕 장르에 고어 강제
- 주장 한계: 선택 조합이며 실제 구조 강도·종교·그림다크는 입증하지 않는다.
- 제안 슬롯: location, object_structure; 잠정 판단: new
- 출처: [M01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V61 · 변경 시장의 생존 물자 교환

상인이 수선된 착륙항 좌판에서 물 카트리지를 교환하고 옆에는 먼지 묻은 소형 화물선이 있다.

A trader exchanges a water cartridge at a patched landing-port stall beside a small dusty cargo craft.

- 소유자/성분: trader: trader; cartridge: water cartridge; stall: patched landing-port stall; craft: small cargo craft
- 방향 관계: trader → exchanges → cartridge; cartridge → at → stall; craft → beside → stall
- 혼동: 카우보이 모자만으로 우주 서부극·사막 필수화
- 주장 한계: 물자·교역의 현재 관계만 보이며 변경 통치·빈곤·범죄는 서사다.
- 제안 슬롯: relational_action, location; 잠정 판단: new
- 출처: [C08](sources.json); [C13](sources.json); [C11](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V62 · 수리 작업으로 이어지는 승무원 관계

승무원 둘이 떼어낸 패널을 함께 받치고 셋째가 열린 함선 배관 옆에서 맞는 공구를 건넨다.

Two crew members support a removed panel together while a third offers the matching tool beside an open ship conduit.

- 소유자/성분: crew: two supporting crew; panel: removed panel; third: third crew member; tool: matching tool; conduit: open ship conduit
- 방향 관계: crew → support → panel; third → offers → tool; panel → beside → conduit
- 혼동: 단체 포즈·유사가족을 혈연·연애로 자동화
- 주장 한계: 협력은 보이지만 장기 유대·선택한 가족·도덕성은 별도다.
- 제안 슬롯: relational_action, contact_point; 잠정 판단: new
- 출처: [C15](sources.json); [C03](sources.json); [C13](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V63 · 행성 변경과 몸 변경의 비교 도해

분할 개념도에서 행성 둘레 환경 처리기와 별도 프레임의 적응형 인간 몸을 대비한다.

A split concept diagram contrasts environmental processors around a planet with a separately framed adapted human body.

- 소유자/성분: planet: planet; processors: environmental processors; body: adapted human body; divider: diagram divider
- 방향 관계: processors → surround → planet; divider → separates → planet; divider → separates → body
- 혼동: 같은 녹색 행성으로 두 개념 통합·변화 완료 오인
- 주장 한계: 저술한 비교 도해이며 시간 변화·실현 가능·생존 적합성은 입증하지 않는다.
- 제안 슬롯: composition, object_structure; 잠정 판단: new
- 출처: [T09](sources.json); [T10](sources.json); [C03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V64 · 공유 기록과 개별 접근 지점

분리된 두 독자가 기록 보관함을 향하고 각자 표시된 단말이 같은 저장 노드에 연결된다.

Two separate readers face an archive cabinet; each uses an individually labeled terminal linked to the same storage node.

- 소유자/성분: readers: two separate readers; terminals: individual terminals; storage: shared storage node; cabinet: archive cabinet
- 방향 관계: readers → use → terminals; terminals → linked_to → storage; storage → inside → cabinet
- 혼동: 접속 수와 인격 수 동일시·저장이 의식 지속의 증거
- 주장 한계: 접속 구조만 보이며 기억 소유·동일 의식·편집 이력·사후 생존은 별도다.
- 제안 슬롯: anatomical_connection, prop; 잠정 판단: new
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V65 · 보급의 양 끝과 인수인계

지원 셔틀이 봉인 보급 컨테이너를 열린 화물선 구획으로 옮기고 인수자가 표시선 뒤에서 기다린다.

A service shuttle transfers sealed supply containers toward an open freighter bay while receivers wait behind a marked line.

- 소유자/성분: shuttle: service shuttle; containers: sealed supply containers; bay: freighter bay; receivers: receivers; line: marked line
- 방향 관계: containers → between → shuttle; containers → between → bay; receivers → behind → line
- 혼동: 화려한 전투만으로 군수 지원·무한 탄약
- 주장 한계: 전달 방향과 현재 배치만 보이며 보급량·작전 지속성은 별도다.
- 제안 슬롯: relational_action, location; 잠정 판단: new
- 출처: [C13](sources.json); [C14](sources.json); [C15](sources.json); [C18](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V66 · 부유체와 손잡이의 미세중력 단서

선실 안에서 방울과 줄에 매인 공구가 서로 다른 높이에 떠 있고 승무원이 벽 레일을 잡는다.

Inside a cabin, loose droplets and a tethered tool float at different heights while a crew member holds a wall rail.

- 소유자/성분: droplets: loose droplets; tool: tethered tool; crew: crew member; rail: wall rail; cabin: crew cabin
- 방향 관계: crew → grips → rail; tool → inside → cabin; droplets → inside → cabin
- 혼동: 수중·점프·중력 소멸·관성 완충장치 효능 판정
- 주장 한계: 부유 표현의 선택안이며 실제 미세중력·가속·궤도는 계측이 필요하다.
- 제안 슬롯: space_condition, contact_point; 잠정 판단: refine
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V67 · 메시아 도상과 군중의 시선

고립된 성인 한 명이 투사된 상징 문양 아래 서고 군중은 별도 낮은 단상에서 문양을 바라본다.

A solitary adult stands below a projected symbolic emblem while a crowd faces the emblem from a separate lower platform.

- 소유자/성분: adult: solitary adult; emblem: projected symbolic emblem; crowd: crowd; platform: lower platform
- 방향 관계: emblem → above → adult; crowd → faces → emblem; crowd → on → platform
- 혼동: 빛나는 후광이 예언·신성·선택된 자의 진실
- 주장 한계: 현재 시선·배치만 보이며 믿음·조작·능력·구원은 서사다.
- 제안 슬롯: composition, lighting; 잠정 판단: new
- 출처: [C20](sources.json); [C08](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V68 · 행성 도시의 연속성

밀집 도시 블록이 굽은 행성 가장자리를 따라 이어지고 별도 삽입 화면은 경계 있는 자급형 탑 단지를 강조한다.

Dense city blocks wrap across a curved planetary limb, with one bounded self-contained tower complex highlighted in an inset.

- 소유자/성분: blocks: planet-spanning city blocks; limb: curved planetary limb; complex: bounded tower complex; inset: detail inset
- 방향 관계: blocks → cover → limb; complex → shown_in → inset
- 혼동: 한 거대 도시가 행성 전체·아콜로지 자급을 증명
- 주장 한계: 행성도시의 저술된 축척 도해이며 실제 전면 피복·자급률은 주장하지 않는다.
- 제안 슬롯: location, spatial_depth; 잠정 판단: new
- 출처: [T05](sources.json); [T06](sources.json); [T08](sources.json); [T15](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V69 · 제작 흔적과 완성 외형의 구별

작업대 위 미완성 오리지널 우주선 모형 옆에 부품 런너와 분리된 완성 모형이 있다.

A workshop table holds an unfinished original spacecraft miniature beside donor sprues and a separately placed completed model.

- 소유자/성분: table: workshop table; unfinished: unfinished original miniature; sprues: donor sprues; finished: completed model
- 방향 관계: unfinished → on → table; sprues → beside → unfinished; finished → separate_from → unfinished
- 혼동: 완성 기계 표면만 보고 킷배싱 제작 과정 확정
- 주장 한계: 현재 작업대 구성은 보이지만 실제 제작 이력·시간 순서는 추가 기록이다.
- 제안 슬롯: prop, object_structure; 잠정 판단: new
- 출처: [M01](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V70 · 독립된 예비 추진기와 열 경로

오리지널 함선의 긴 후방 엔진부가 구조 척추로 승무원 모듈과 떨어지고 양옆에는 구분된 방열판이 있다.

An original ship has a long aft engine assembly separated from crew modules by a structural spine and flanked by distinct radiator panels.

- 소유자/성분: engine: aft engine assembly; spine: structural spine; crew: crew modules; radiators: separate radiator panels
- 방향 관계: spine → between → engine; spine → between → crew; radiators → beside → spine
- 혼동: 길고 밝은 엔진이 핵융합·반물질·FTL을 증명
- 주장 한계: 선택한 공학적 외형이며 에너지원·방사선 차폐·추력·실현성을 보증하지 않는다.
- 제안 슬롯: object_structure, spatial_depth; 잠정 판단: new
- 출처: [T01](sources.json); [T02](sources.json); [T04](sources.json); [M06](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V71 · 의식의 합성과 몸의 분산을 구분한 도해

삼분할 도해에서 다대일 연결·일대다 연결·끊어진 두 복사본을 각기 경계 있는 표시로 구분한다.

A three-panel diagram separates many-to-one links, one-to-many links, and two disconnected copies, each with its own bounded label.

- 소유자/성분: many: many input nodes; one: single output node; fan: one-to-many network; copies: two disconnected nodes; panels: three bounded panels
- 방향 관계: many → converge_on → one; fan → separate_from → copies; copies → shown_in → panels
- 혼동: 군체·분산 자아·정신 분기를 하나의 발광 군집으로 통합
- 주장 한계: 도해의 연결 토폴로지만 보이며 실제 의식·자아·연속성은 비가시 설정이다.
- 제안 슬롯: composition, object_structure; 잠정 판단: context
- 출처: [C07](sources.json); [C09](sources.json); [C10](sources.json); [C11](sources.json); [C16](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

## V72 · 생명유지의 서로 다른 기능 경로

산소 생성·이산화탄소 제거·물 회수의 별도 표시 모듈들이 구분된 서비스 선으로 승무원 선실에 연결된다.

Separate labeled modules for oxygen generation, carbon-dioxide removal, and water recovery connect to a crew cabin through distinct service lines.

- 소유자/성분: oxygen: oxygen module; carbon: carbon-dioxide module; water: water-recovery module; cabin: crew cabin; lines: distinct service lines
- 방향 관계: lines → connect → oxygen; lines → connect → carbon; lines → connect → water; lines → connect → cabin
- 혼동: 산소 장치 하나로 완전 순환·공기 재활용·식량 자급 확정
- 주장 한계: 계통 설명 도해이며 회수율·생존시간·완전 폐쇄계는 측정과 설계 근거가 필요하다.
- 제안 슬롯: object_structure, anatomical_connection; 잠정 판단: reuse
- 출처: [M04](sources.json); [M05](sources.json); [T03](sources.json). 위 정확한 장면은 저술안.
- 필수 검토: 모든 관계의 양 끝·개수·재료·접점을 같은 프레임에서 확인. 가림·부분 구현은 통과 불가.

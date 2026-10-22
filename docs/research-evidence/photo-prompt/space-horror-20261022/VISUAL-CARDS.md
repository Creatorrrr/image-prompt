# 시각 의미 카드 64개

출처가 지원하는 정의·작품별 해석과 저술한 장면 기하를 구분한다. 모든 관계 gate의 실제 이미지 검토는 NOT_RUN이다. V41·V47·V61은 문맥 단서 카드로 보존하고 양성 후보 초안에서 보류했다.

## V01 두 해치 사이의 압력 전이실

- 원문: 15, 36, 37; 관찰: still; 우선순위: P0.
- EN: A suited crew member stands in a short chamber bounded by an inner hatch and a separate outer hatch; the outer hatch opens onto the spacecraft exterior.
- KO: 압력복을 입은 승무원이 안쪽 해치와 별도의 바깥 해치로 구획된 짧은 방 안에 서 있고, 바깥 해치 너머로 선체 외부가 보인다.
- 구성 소유자: crew: suited crew member; chamber: short transition chamber; inner: inner hatch; outer: outer hatch; exterior: spacecraft exterior.
- 방향 관계: inner → bounds → chamber; outer → bounds → chamber; crew → inside → chamber; outer → opens_onto → exterior.
- 혼동 경계: 한 문짜리 창고·엘리베이터·통로 두 문.
- 주장 한계: 압력 전이 절차·문 인터록·밀폐 성능은 별도 근거가 필요하다.
- 제안 슬롯: location, object_structure, space_condition; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/), [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V02 서로 다른 구획의 압력 표시

- 원문: 16, 17, 18, 19, 20, 27; 관찰: proxy; 우선순위: P0.
- EN: Two pressure gauges flank a closed hatch, with visibly different needle positions; a technician braces a gloved hand on the hatch frame.
- KO: 닫힌 해치 양쪽의 압력계 바늘 위치가 서로 다르고 기술자가 장갑 낀 손을 해치 프레임에 댄다.
- 구성 소유자: left: left pressure gauge; right: right pressure gauge; hatch: closed pressure hatch; tech: technician; frame: hatch frame.
- 방향 관계: left → flanks → hatch; right → flanks → hatch; tech → touches → frame.
- 혼동 경계: 두 계기 장식·산소 농도계와 압력계 혼동.
- 주장 한계: 바늘 차이는 계기 표현이며 감압 속도·산소 분압·CO2 농도나 질병을 입증하지 않는다.
- 제안 슬롯: prop_state, visible_text, contact_point; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/), [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V03 선체 관통부와 외부 시야

- 원문: 16, 25, 38; 관찰: still; 우선순위: P0.
- EN: A ragged opening crosses the spacecraft hull, exposing black exterior space; loose insulation fragments are suspended near the torn edge inside the compartment.
- KO: 찢긴 선체 가장자리 안쪽에 단열재 조각이 떠 있고 선체를 관통한 구멍 너머로 검은 외부 공간이 보인다.
- 구성 소유자: hull: spacecraft shell; opening: ragged through-hole; exterior: black exterior space; fragments: loose insulation fragments; edge: torn hull edge.
- 방향 관계: opening → pierces → hull; opening → reveals → exterior; fragments → adjacent_to → edge.
- 혼동 경계: 어두운 도장·창문·벽의 얕은 파손.
- 주장 한계: 관통 외형은 보이지만 감압률·구멍 원인·밖으로 빨려가는 시간 경과는 미확정이다.
- 제안 슬롯: object_structure, aftermath_trace, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/), [S04](https://www.esa.int/Space_Safety/Space_Debris/Space_Debris_FAQ_Frequently_asked_questions).

## V04 CO2 제거 장치의 분리된 유로

- 원문: 18, 33, 34; 관찰: still; 우선순위: P0.
- EN: An opened air-treatment rack contains a removable cartridge; a hose from the cabin duct ends at a detached coupling beside that cartridge.
- KO: 열린 공기 처리 랙의 탈착식 카트리지 옆에 선실 덕트에서 온 호스의 분리된 커플링이 놓여 있다.
- 구성 소유자: rack: air-treatment rack; cartridge: removable cartridge; hose: cabin-duct hose; coupling: detached hose end.
- 방향 관계: cartridge → inside → rack; hose → ends_at → coupling; coupling → beside → cartridge.
- 혼동 경계: 휴대 산소통·산소 생성기·장식 배관.
- 주장 한계: 장치 종류는 설정·라벨 지원이 필요하며 CO2 제거 성능과 실제 중독은 외형으로 확정하지 않는다.
- 제안 슬롯: prop, object_structure, contact_point; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/).

## V05 연결된 재생 생명유지 계통

- 원문: 33, 35, 42; 관찰: still; 우선순위: P0.
- EN: A water recovery tank, an air-treatment rack and an oxygen unit occupy separate bays; distinct pipe runs connect each unit to a common service panel.
- KO: 물 회수 탱크·공기 처리 랙·산소 장치가 별도 구획에 있고 각각의 배관이 공통 서비스 패널로 이어진다.
- 구성 소유자: water: water-recovery tank; air: air-treatment rack; oxygen: oxygen unit; panel: common service panel; pipes: distinct pipe runs.
- 방향 관계: pipes → connects → water; pipes → connects → air; pipes → connects → oxygen; pipes → terminates_at → panel.
- 혼동 경계: 산소통 여러 개·배관 무작위 겹침.
- 주장 한계: 재생률·완전 폐쇄순환·고장 전파 순서는 배관의 존재만으로 입증되지 않는다.
- 제안 슬롯: object_structure, environment_detail; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/).

## V06 환기 흐름 쪽으로 기운 선내 화염

- 원문: 39; 관찰: proxy; 우선순위: P0.
- EN: Inside a pressurized equipment bay, a small flame extends from a cable enclosure toward a nearby ventilation grille; a crew member reaches for a wall extinguisher.
- KO: 가압 장비실의 케이블 함에서 작은 불꽃이 인근 환기 그릴 쪽으로 뻗고 승무원이 벽의 소화기로 손을 뻗는다.
- 구성 소유자: flame: small cable-enclosure flame; box: cable enclosure; grille: ventilation grille; crew: crew member; extinguisher: wall extinguisher.
- 방향 관계: flame → emerges_from → box; flame → oriented_toward → grille; crew → reaches_toward → extinguisher.
- 혼동 경계: 진공 속 불길·모든 선내 불이 구형이라는 단정.
- 주장 한계: 환기 영향은 선택한 시뮬레이션 조건이다. 정지 영상은 유동장이나 연소 물리를 측정하지 않는다.
- 제안 슬롯: physical_motion, environment_detail, action; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S07](https://www.nasa.gov/image-article/candle-flame-1g-vs-microgravity/), [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/).

## V07 라디에이터와 단열 담요의 분리

- 원문: 40; 관찰: still; 우선순위: P0.
- EN: A pale radiator panel extends from the service module beside a foil-wrapped equipment housing; a visible pipe joins the module to the panel root.
- KO: 호일 단열재를 두른 장비 함 옆으로 밝은 라디에이터 패널이 펼쳐지고 배관이 모듈에서 패널 뿌리로 이어진다.
- 구성 소유자: panel: pale radiator panel; module: service module; blanket: foil insulation; housing: equipment housing; pipe: thermal pipe.
- 방향 관계: panel → extends_from → module; blanket → wraps → housing; pipe → joins → panel.
- 혼동 경계: 태양전지판·호일 자체를 방열판으로 간주.
- 주장 한계: 내부 온도·방열 성능·과열 원인은 표면색으로 판단하지 않는다.
- 제안 슬롯: object_structure, surface_material, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S05](https://www.esa.int/Enabling_Support/Space_Engineering_Technology/Thermal_Control).

## V08 공통 전원함을 공유하는 두 계통

- 원문: 41, 42, 43; 관찰: proxy; 우선순위: P0.
- EN: Separate ventilation and hatch-control cables converge at one open power cabinet; beyond it one corridor segment is dark while the adjacent emergency strip is lit.
- KO: 환기와 해치 제어 케이블이 열린 전원함 하나에 모이고, 그 너머 통로의 한 구간은 어둡고 인접 비상등 띠는 켜져 있다.
- 구성 소유자: vent: ventilation cable; door: hatch-control cable; cabinet: common power cabinet; corridor: dark corridor segment; strip: lit emergency strip.
- 방향 관계: vent → terminates_at → cabinet; door → terminates_at → cabinet; strip → adjacent_to → corridor.
- 혼동 경계: 장식 전선·단순한 저조도 사진.
- 주장 한계: 전원 의존·단일 고장점·연쇄 순서는 도면이나 시계열이 있어야 검증된다.
- 제안 슬롯: environment_detail, lighting, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S02](https://www.nasa.gov/reference/environmental-control-and-life-support-systems-eclss/).

## V09 탈출 포드 입구와 한정된 좌석

- 원문: 46, 115; 관찰: still; 우선순위: P0.
- EN: Four suited adults cluster outside an escape pod whose open doorway reveals two separate restraint seats.
- KO: 압력복을 입은 성인 네 명이 탈출 포드 앞에 모여 있고 열린 출입구 안으로 구속 벨트 좌석 두 개가 보인다.
- 구성 소유자: crew: four suited adults; pod: escape pod; door: open doorway; seats: two visible restraint seats.
- 방향 관계: crew → outside → pod; door → reveals → seats; seats → inside → pod.
- 혼동 경계: 일부 좌석이 가려진 여객선·한 사람이 겹친 군중.
- 주장 한계: 보이는 좌석 수만을 주장한다. 전체 정원·누가 구조될지·자동 선별을 확정하지 않는다.
- 제안 슬롯: subject_count, proxemics, object_structure; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S11](https://sf-encyclopedia.com/entry/horror_in_sf).

## V10 충돌 파편과 손상된 궤도 구조물

- 원문: 25, 26; 관찰: still; 우선순위: P0.
- EN: An orbital module has a punctured shield panel; separate irregular fragments are spread across the same exterior view.
- KO: 궤도 모듈의 차폐 패널에 구멍이 나 있고 같은 외부 시야에 불규칙한 파편들이 서로 떨어져 있다.
- 구성 소유자: module: orbital module; shield: punctured shield panel; fragments: separate irregular fragments.
- 방향 관계: shield → part_of → module; fragments → distributed_near → module.
- 혼동 경계: 별무리·정상 위성 편대·모든 궤도의 즉시 폭발.
- 주장 한계: MMOD의 기원·충돌 속도·케슬러의 연쇄 전개는 정지 화면으로 검증하지 않는다.
- 제안 슬롯: background_element, aftermath_trace; 실제 binding 승인 아님.
- gate: 관계 2개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S04](https://www.esa.int/Space_Safety/Space_Debris/Space_Debris_FAQ_Frequently_asked_questions).

## V11 차폐 구획으로 이어진 좁은 통로

- 원문: 23, 24; 관찰: proxy; 우선순위: P0.
- EN: A crew member carries a dosimeter toward a small inner shelter surrounded by dense storage lockers; the outer work bay remains behind the closing hatch.
- KO: 승무원이 선량계를 들고 조밀한 수납함으로 둘러싸인 작은 안쪽 대피실로 향하고, 닫히는 해치 뒤에는 외부 작업 구획이 남아 있다.
- 구성 소유자: crew: crew member; meter: dosimeter; shelter: inner shelter; lockers: dense storage lockers; hatch: separating hatch; bay: outer work bay.
- 방향 관계: crew → holds → meter; lockers → surrounds → shelter; hatch → separates → bay.
- 혼동 경계: 녹색 안개·방사능 괴물·공포 표정만 있는 인물.
- 주장 한계: 방사선은 보이지 않는다. 대피 배치는 위험 대응의 단서이며 노출량·태양 입자 사건을 입증하지 않는다.
- 제안 슬롯: location, prop, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S01](https://www.nasa.gov/hrp/hazards/), [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V12 송신·수신 시각을 분리한 통신석

- 원문: 29, 125; 관찰: proxy; 우선순위: P0.
- EN: A communications terminal displays separate sent and received timestamp fields beside a waiting operator, with the two fields readable together.
- KO: 대기 중인 통신 담당자 옆 단말에 송신 시각과 수신 시각 칸이 분리되어 있고 두 칸이 함께 읽힌다.
- 구성 소유자: terminal: communications terminal; sent: sent timestamp field; received: received timestamp field; operator: waiting operator.
- 방향 관계: sent → displayed_on → terminal; received → displayed_on → terminal; operator → beside → terminal.
- 혼동 경계: 다운로드 진행 막대·시간대가 다른 시계.
- 주장 한계: 화면 숫자는 가공된 표지다. 실제 신호 이동 시간·동기화·왕복 지연은 별도 기록이 필요하다.
- 제안 슬롯: visible_text, prop, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S06](https://www.nasa.gov/missions/tech-demonstration/space-communications-7-things-you-need-to-know/).

## V13 전원은 남고 링크가 끊긴 단말

- 원문: 30, 43; 관찰: proxy; 우선순위: P0.
- EN: A powered communications console shows a disconnected-link symbol while neighboring cabin indicators remain illuminated.
- KO: 통신 콘솔의 전원은 켜져 있으나 연결 끊김 기호가 보이고 옆 선실 표시등들도 켜져 있다.
- 구성 소유자: console: powered communications console; symbol: disconnected-link symbol; indicators: lit cabin indicators.
- 방향 관계: symbol → displayed_on → console; indicators → adjacent_to → console.
- 혼동 경계: 전체 정전·검은 모니터·일부러 꺼둔 화면.
- 주장 한계: 두절 원인·예정 시간·상대 생존·AI의 고의는 판정하지 않는다.
- 제안 슬롯: prop_state, visible_text, lighting; 실제 binding 승인 아님.
- gate: 관계 2개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S06](https://www.nasa.gov/missions/tech-demonstration/space-communications-7-things-you-need-to-know/).

## V14 선체에 연결된 안전줄

- 원문: 31, 32; 관찰: still; 우선순위: P0.
- EN: An adult EVA technician wears a closed pressure suit and life-support backpack; one continuous tether joins the suit waist fitting to a spacecraft rail.
- KO: 성인 선외 기술자가 밀폐 압력복과 생명유지 배낭을 착용하고, 끊기지 않은 안전줄이 허리 연결부에서 선체 레일까지 이어진다.
- 구성 소유자: worker: adult suited EVA technician; pack: life-support backpack; tether: continuous tether; waist: suit waist fitting; rail: spacecraft rail.
- 방향 관계: pack → attached_to → worker; tether → joins → waist; tether → joins → rail.
- 혼동 경계: 줄이 화면 밖에서 끝남·케이블을 잡은 손만 보임.
- 주장 한계: 현재 연결만 증명한다. 구조 보장·줄 장력·과거의 이탈 여부는 미확정이다.
- 제안 슬롯: wearable_accessory, contact_point, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V15 우주복 끝에서 끊긴 연결

- 원문: 32; 관찰: proxy; 우선순위: P0.
- EN: A suited astronaut is separated from the hull by an empty gap; a short tether fixed to the waist ends in a visibly free carabiner inside that gap.
- KO: 우주복 인물과 선체 사이에 빈 간격이 있고 허리에 고정된 짧은 줄 끝의 카라비너가 그 간격 안에서 자유롭게 끝난다.
- 구성 소유자: astronaut: suited astronaut; hull: spacecraft hull; tether: waist-attached short tether; clip: free carabiner; gap: empty intervening space.
- 방향 관계: tether → attached_to → astronaut; tether → ends_at → clip; gap → separates → hull; clip → inside → gap.
- 혼동 경계: 카라비너가 선체에 실제로 연결됨·유영 중 정상 작업.
- 주장 한계: 해당 줄의 미연결만 가시적이다. 모든 추진수단의 부재·멀어지는 속도·구조 불가를 입증하지 않는다.
- 제안 슬롯: anatomical_connection, proxemics, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V16 공통 아래쪽이 없는 선실

- 원문: 21, 22; 관찰: still; 우선순위: P0.
- EN: Inside a station module, two crew members and loose tools occupy different orientations; one gloved hand holds a rail while a separate wrench has no visible support.
- KO: 정거장 모듈 안에서 승무원 두 명과 공구가 다른 방향을 향하고 한 장갑 손은 레일을 잡지만 별도 렌치는 지지 없이 떠 있다.
- 구성 소유자: crew: two crew members; tools: loose tools; hand: one crew members gloved hand; rail: module rail; wrench: separate unsupported wrench.
- 방향 관계: hand → belongs_to → crew; hand → grips → rail; wrench → separated_from → rail; tools → different_orientation_from → crew.
- 혼동 경계: 점프·수중 촬영·전원 선 자세로 바닥에 섬.
- 주장 한계: 현재 부유 외형을 다룬다. 중력 자체가 없다는 주장은 하지 않으며 실제 지남력 상실은 심리·계측 영역이다.
- 제안 슬롯: body_orientation, physical_motion, contact_point; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S01](https://www.nasa.gov/hrp/hazards/), [S03](https://www.nasa.gov/reference/11-0-spacesuits-vol-2/).

## V17 무중량을 암시하는 붉은 액체 방울

- 원문: 21, 176; 관찰: proxy; 우선순위: P0.
- EN: Separate red liquid droplets hang between a damaged glove and a transparent visor; several droplets adhere to the visor while others remain visibly detached.
- KO: 손상된 장갑과 투명 바이저 사이에 붉은 액체 방울들이 떨어져 떠 있고 일부는 바이저에 붙지만 나머지는 떨어져 있다.
- 구성 소유자: free: detached red liquid droplets; adhered: red droplets attached to visor; glove: damaged glove; visor: transparent visor.
- 방향 관계: free → in_gap_adjacent_to → glove; free → separated_from → visor; adhered → adheres_to → visor; glove → separated_from → visor.
- 혼동 경계: 빗방울·모든 액체가 완벽한 공·피 색만으로 인간의 죽음 단정.
- 주장 한계: 붉은 액체는 허구의 선택 재료다. 혈액의 성분·누구의 것인지·부상 원인은 외형만으로 입증되지 않는다.
- 제안 슬롯: liquid_inclusion, surface_moisture, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S31](https://ntrs.nasa.gov/api/citations/19930004376/downloads/19930004376.pdf), [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare).

## V18 폐우주선 외피와 작동 흔적

- 원문: 47, 174; 관찰: still; 우선순위: P0.
- EN: A dark spacecraft carries a bent docking collar and multiple external patch plates; a small inspection light reveals the worn hull around the collar.
- KO: 어두운 우주선에 휜 도킹 칼라와 여러 외부 보수판이 있고 작은 점검등이 칼라 주변의 닳은 선체를 비춘다.
- 구성 소유자: ship: spacecraft; collar: bent docking collar; patches: external patch plates; light: inspection light.
- 방향 관계: collar → attached_to → ship; patches → covers → ship; light → illuminates → collar.
- 혼동 경계: 일반 건물 폐허·정상 우주선 야경.
- 주장 한계: 폐기 이력·승무원 부재·고장 기간은 외관만으로 확정하지 않는다.
- 제안 슬롯: object_structure, space_condition, aftermath_trace; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V19 사람 없이 돌아가는 식사 설비

- 원문: 48, 177, 179; 관찰: proxy; 우선순위: P0.
- EN: An empty ship mess contains filled cups beneath a mechanical dispenser arm; the arm is extended over one empty chair beside a laid place setting.
- KO: 빈 우주선 식당의 기계 배식 팔 아래에 채워진 컵이 있고, 팔은 차려진 식사 자리 옆 빈 의자 위로 뻗어 있다.
- 구성 소유자: mess: ship mess; arm: mechanical dispenser arm; cups: filled cups; chair: empty chair; setting: laid place setting.
- 방향 관계: arm → above → cups; chair → beside → setting; arm → extends_over → chair.
- 혼동 경계: 유령 실루엣 자동 추가·수상 유령선.
- 주장 한계: 한 구역의 부재와 자동화 단서다. 배 전체가 무인인지 실종·사망했는지 알 수 없다.
- 제안 슬롯: narrative_clue, prop_placement, offscreen_context; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films).

## V20 선실과 거울의 불일치

- 원문: 49, 106, 170; 관찰: still; 우선순위: P1.
- EN: A crew member stands before a fixed mirror; the reflected corridor contains a closed hatch where the directly visible corridor contains an open doorway, with both doorframes in view.
- KO: 승무원 앞 고정 거울 속 복도에는 닫힌 해치가 있지만 직접 보이는 복도에는 열린 문이 있고 두 문틀이 함께 보인다.
- 구성 소유자: crew: crew member; mirror: fixed mirror; real: direct corridor doorway; image: reflected corridor hatch.
- 방향 관계: crew → faces → mirror; image → visible_in → mirror; image → differs_from → real.
- 혼동 경계: 각도가 다른 별도 문·거울 속 영상 화면.
- 주장 한계: 불일치는 저술한 초현실 표현이다. 유령·환각·편집·실제 물리 위반 중 원인은 미확정이다.
- 제안 슬롯: reflection_logic, reality_anchor, surreal_concept; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films).

## V21 동면열의 빈 캡슐 하나

- 원문: 51, 112; 관찰: still; 우선순위: P0.
- EN: A row of closed stasis capsules contains one open capsule with displaced restraints; a suited adult stands beside that open capsule.
- KO: 닫힌 동면 캡슐 열에 구속 벨트가 흐트러진 열린 캡슐 하나가 있고 그 옆에 우주복 성인이 서 있다.
- 구성 소유자: closed: row of closed capsules; open: one open capsule; restraints: displaced restraints; adult: suited adult.
- 방향 관계: restraints → inside → open; adult → beside → open; open → adjacent_to → closed.
- 혼동 경계: 의료 침대·캡슐 수만으로 승무원 사망.
- 주장 한계: 동면 상태·각성 시점·기억 위조·안쪽 사람의 의식은 입증하지 않는다.
- 제안 슬롯: location, prop_state, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S13](https://sf-encyclopedia.com/entry/generation_starships), [S09](https://www.nasa.gov/hrp/hazard-isolation-and-confinement/).

## V22 세대별 생활 흔적이 겹친 주거 구획

- 원문: 50, 93, 95, 155; 관찰: proxy; 우선순위: P1.
- EN: A ship habitat combines a repaired domestic table, successive height marks on one door jamb and several differently worn family photographs fixed to the wall.
- KO: 우주선 거주 구획의 수리한 식탁 옆 한 문설주에 여러 키 눈금이 있고 벽에는 마모 정도가 다른 가족사진들이 붙어 있다.
- 구성 소유자: table: repaired domestic table; jamb: door jamb; marks: successive height marks; photos: family photographs; wall: habitat wall.
- 방향 관계: marks → on → jamb; photos → attached_to → wall; table → beside → jamb.
- 혼동 경계: 일반 가족 주거·사진 속 인물을 실제 승무원과 동일시.
- 주장 한계: 세대 항해·혈연·출산 명령·근친 관계·정확한 연대는 외형만으로 입증되지 않는다.
- 제안 슬롯: narrative_clue, environment_detail; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S13](https://sf-encyclopedia.com/entry/generation_starships), [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos).

## V23 식사가 남은 무인 식민지

- 원문: 52, 179; 관찰: proxy; 우선순위: P1.
- EN: Inside a planetary habitat, half-finished meals remain on a common table beside empty work chairs; a sealed window shows the surrounding barren terrain.
- KO: 행성 거주지의 공용 식탁에 먹다 남긴 식사가 있고 작업 의자들은 비어 있으며 밀폐창 밖으로 황량한 지표가 보인다.
- 구성 소유자: meals: half-finished meals; table: common table; chairs: empty work chairs; window: sealed habitat window; terrain: barren terrain.
- 방향 관계: meals → on → table; chairs → beside → table; window → reveals → terrain.
- 혼동 경계: 정상 점심시간 뒤 빈 방·행성 전체 절멸.
- 주장 한계: 중단된 생활을 암시할 뿐 실종의 원인·기간·전 인구의 부재를 확정하지 않는다.
- 제안 슬롯: location, narrative_clue, prop_placement; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V24 외부 환경과 떨어진 연구기지

- 원문: 53, 101; 관찰: still; 우선순위: P1.
- EN: A small research habitat sits alone on an exposed rocky ridge; its narrow enclosed access tube ends at a single exterior hatch.
- KO: 작은 연구 거주동이 드러난 암석 능선 위에 홀로 있고 좁은 밀폐 접근 통로가 외부 해치 하나에서 끝난다.
- 구성 소유자: habitat: small research habitat; ridge: rocky ridge; tube: enclosed access tube; hatch: single exterior hatch.
- 방향 관계: habitat → on → ridge; tube → joins → habitat; tube → ends_at → hatch.
- 혼동 경계: 산악 산장·프레임 밖 다른 기지를 없다고 단정.
- 주장 한계: 관찰 시야의 고립만 가시적이며 구조 거리·인구·지원 불가를 확정하지 않는다.
- 제안 슬롯: location, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S01](https://www.nasa.gov/hrp/hazards/), [S09](https://www.nasa.gov/hrp/hazard-isolation-and-confinement/).

## V25 굴착면 안의 이질적 층

- 원문: 54, 164; 관찰: still; 우선순위: P1.
- EN: A mining drill faces an exposed rock cut inside a pressure tunnel; a smooth patterned slab interrupts the rough mineral layers directly ahead of the bit.
- KO: 가압 갱도 안 채굴 드릴 앞의 거친 광물 절단면 사이로 매끄럽고 무늬 있는 판층이 드릴 비트 정면에 드러난다.
- 구성 소유자: drill: mining drill; cut: exposed rock cut; slab: patterned smooth slab; layers: rough mineral layers; bit: drill bit.
- 방향 관계: slab → interrupts → layers; bit → faces → slab; layers → part_of → cut.
- 혼동 경계: 장식 벽·자연 무늬를 외계 문명으로 단정.
- 주장 한계: 인공 기원·봉인·저주·착취·발견 전 역사는 판정하지 않는다.
- 제안 슬롯: environment_detail, object_structure, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S14](https://sf-encyclopedia.com/entry/big_dumb_objects), [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V26 작은 탐사선과 거대 구조물의 동시 척도

- 원문: 55, 169; 관찰: still; 우선순위: P0.
- EN: A small inspection craft passes close to an enormous artificial-looking ribbed structure; repeated access apertures remain much larger than the craft in the same continuous view.
- KO: 작은 점검선 옆 거대한 인공물 같은 리브 구조가 이어지고 반복된 출입구들은 같은 연속 시야에서 점검선보다 훨씬 크게 보인다.
- 구성 소유자: craft: small inspection craft; structure: enormous ribbed structure; apertures: repeated large apertures.
- 방향 관계: craft → adjacent_to → structure; apertures → part_of → structure; apertures → larger_than → craft.
- 혼동 경계: 멀리 있는 물체의 원근 크기·작은 모형.
- 주장 한계: 확정 치수·제작 종·목적·무지성·관객의 공포 반응은 크기 비교만으로 입증되지 않는다.
- 제안 슬롯: scale_relation, spatial_depth, object_structure; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S14](https://sf-encyclopedia.com/entry/big_dumb_objects), [S26](https://www.nationalgalleries.org/art-and-artists/glossary-terms/sublime).

## V27 서로 다른 흔적층의 외계 유적

- 원문: 56, 154, 155; 관찰: proxy; 우선순위: P1.
- EN: An excavated structure exposes three superimposed wall surfaces bearing different repeated marks; a modern survey rod rests against the nearest layer.
- KO: 발굴 구조물의 겹친 벽 표면 세 층마다 다른 반복 무늬가 있고 가장 가까운 층에 현대 측량봉이 기대 있다.
- 구성 소유자: layers: three superimposed wall surfaces; marks: different repeated marks; rod: modern survey rod; structure: excavated structure.
- 방향 관계: layers → part_of → structure; marks → on → layers; rod → against → layers.
- 혼동 경계: 한 문명의 재도장·지질 줄무늬.
- 주장 한계: 문명 수·연대·멸망 순서·경고의 번역은 별도 고고학·서사 증거가 필요하다.
- 제안 슬롯: surface_pattern, narrative_clue, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S14](https://sf-encyclopedia.com/entry/big_dumb_objects), [S28](https://www.seti.org/research/seti-101/fermi-paradox/).

## V28 선체 부재로 이어지는 생체 조직

- 원문: 57, 175; 관찰: still; 우선순위: P0.
- EN: Rib-like structural arches support a ship passage; fleshy conduits merge into the arches at visible seams while a metal handrail remains separate.
- KO: 갈비뼈 같은 구조 아치가 선내 통로를 받치고 살 같은 도관이 이음부에서 아치로 이어지며 금속 손잡이는 분리되어 있다.
- 구성 소유자: arches: rib-like load-bearing arches; passage: ship passage; conduits: fleshy conduits; seams: visible merging seams; rail: separate metal handrail.
- 방향 관계: arches → supports → passage; conduits → merges_into → arches; seams → at → arches; rail → separate_from → conduits.
- 혼동 경계: 벽에 붙인 덩굴·내장 소품·일반 호스.
- 주장 한계: 형태 통합만 가시적이다. 생명·신경·소화·승객의 생물학적 편익을 확정하지 않는다.
- 제안 슬롯: anatomical_connection, object_structure, surface_material; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare), [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films).

## V29 관측창 없이 외계 바다를 읽는 잠수정

- 원문: 58, 63; 관찰: still; 우선순위: P1.
- EN: A cramped submersible cabin has an opaque forward bulkhead, a sonar display and a small external-camera print; the pilot faces the instruments rather than a front window.
- KO: 비좁은 잠수정 선실의 정면 격벽은 불투명하고 소나 화면과 작은 외부 카메라 인쇄물이 있으며 조종사는 앞창 대신 계기를 본다.
- 구성 소유자: cabin: cramped submarine cabin; bulkhead: opaque forward bulkhead; sonar: sonar display; print: small camera print; pilot: pilot.
- 방향 관계: bulkhead → bounds → cabin; pilot → faces → sonar; print → beside → sonar.
- 혼동 경계: 넓은 창으로 괴물을 보는 잠수정·우주복 내부.
- 주장 한계: Iron Lung에서 얻은 관측 제약의 선택형 변주다. 바다의 성분·행성·지성은 계기만으로 증명되지 않는다.
- 제안 슬롯: apparatus_pov, location, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S25](https://store.steampowered.com/app/1846170/Iron_Lung/).

## V30 인간형 축이 없는 외계 몸

- 원문: 60, 61, 63, 64; 관찰: still; 우선순위: P1.
- EN: A fictional organism spreads five unequal lobes around a porous central body; no distinct humanlike face, paired arms or upright torso organizes its silhouette.
- KO: 허구 생물의 다공성 중심 몸 주위로 크기가 다른 다섯 엽이 퍼져 있고 실루엣은 인간형 얼굴·한 쌍의 팔·직립 몸통을 중심으로 구성되지 않는다.
- 구성 소유자: body: porous central body; lobes: five unequal lobes; silhouette: whole organism contour.
- 방향 관계: lobes → radiates_from → body; silhouette → bounds → body.
- 혼동 경계: 촉수 달린 인간·외모로 지능과 비의식성 단정.
- 주장 한계: 비인간형 외형은 지능·의식 부재·화학·극한 내성의 증거가 아니다.
- 제안 슬롯: body_form, silhouette_proportion, species_marker; 실제 binding 승인 아님.
- gate: 관계 2개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S24](https://www.rifters.com/blindsight/BS_main.htm).

## V31 숙주 외피와 부착 생물의 접점

- 원문: 73, 75, 77; 관찰: proxy; 우선순위: P0.
- EN: A distinct small organism grips a bounded area of a larger fictional host; its attachment organs remain continuous with its own body at the host surface.
- KO: 작은 별도 생물이 큰 허구 숙주의 한정된 표면을 붙잡고 부착 기관이 작은 생물 몸에서 숙주 표면까지 연속해서 보인다.
- 구성 소유자: host: larger fictional host; organism: small attached organism; organs: organisms attachment organs; surface: bounded host surface.
- 방향 관계: organs → belongs_to → organism; organs → contacts → surface; surface → part_of → host.
- 혼동 경계: 장식 장신구·주인의 추가 팔다리.
- 주장 한계: 부착 관계와 두 몸만 보인다. 영양 이동·피해·공생 편익·감염은 미확정이다.
- 제안 슬롯: anatomical_connection, contact_point; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S15](https://learn.genetics.utah.edu/content/symbiosis/examples/), [S16](https://entomology.mgcafe.uky.edu/ef018).

## V32 같은 숙주 경계에서 나온 외부 개체

- 원문: 74, 82; 관찰: proxy; 우선순위: P1.
- EN: A small fictional larval form projects through one split in a larger hosts outer casing; the split edge and emerging body remain visible together.
- KO: 큰 숙주의 외피 틈 하나에서 작은 허구 유충형 몸이 밖으로 나오고 갈라진 가장자리와 나온 몸이 함께 보인다.
- 구성 소유자: host: larger fictional host; casing: host outer casing; split: single casing split; larva: small emerging larval form.
- 방향 관계: casing → part_of → host; split → pierces → casing; larva → emerges_through → split.
- 혼동 경계: 알에서 부화·외부 기생체를 얹음.
- 주장 한계: 포식기생의 숙주 최종 사망·발달 기간·살아 있음은 한 장으로 입증되지 않는다.
- 제안 슬롯: transformation_stage, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S16](https://entomology.mgcafe.uky.edu/ef018).

## V33 두 생물의 서로 다른 연결부

- 원문: 75, 80; 관찰: proxy; 우선순위: P1.
- EN: Two distinct fictional organisms are joined by a transparent tubular bridge; the bridge enters a separate visible port on each body.
- KO: 서로 다른 허구 생물 두 몸을 투명 관형 연결부가 잇고 각 몸의 별도 접속구로 들어간다.
- 구성 소유자: first: first organism; second: second organism; bridge: transparent tubular bridge; port1: first body port; port2: second body port.
- 방향 관계: port1 → belongs_to → first; port2 → belongs_to → second; bridge → enters → port1; bridge → enters → port2.
- 혼동 경계: 같은 몸의 팔다리·단순 접촉.
- 주장 한계: 상호 이익·피해·통제권·동화를 자동 판정하지 않는다. Symbiosis를 mutualism과 동일시하지 않는다.
- 제안 슬롯: anatomical_connection, relational_action; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S15](https://learn.genetics.utah.edu/content/symbiosis/examples/).

## V34 덕트에서 선실로 이어지는 만연

- 원문: 76; 관찰: still; 우선순위: P0.
- EN: Small egglike clusters occupy a ventilation duct and continue across the grille onto an adjacent cabin wall.
- KO: 작은 알 같은 덩어리들이 환기 덕트 안을 차지하고 그릴을 지나 인접 선실 벽까지 이어진다.
- 구성 소유자: clusters: small egglike clusters; duct: ventilation duct; grille: duct grille; wall: adjacent cabin wall.
- 방향 관계: clusters → inside → duct; clusters → crosses → grille; clusters → on → wall.
- 혼동 경계: 장식 리벳·곰팡이 얼룩·감염자를 뜻하는 군중.
- 주장 한계: 퍼진 외형을 다룬다. 생물 종·성장 속도·인간 감염성은 미확정이다.
- 제안 슬롯: environment_detail, surface_pattern; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S16](https://entomology.mgcafe.uky.edu/ef018), [S08](https://planetaryprotection.jpl.nasa.gov/mission-implementation).

## V35 지구 장비에서 외부 토양으로 향한 접점

- 원문: 78; 관찰: proxy; 우선순위: P0.
- EN: A landers sampling arm extends from its equipment bay into untouched-looking terrain; a visibly soiled tool tip contacts the local soil.
- KO: 착륙선 장비실에서 뻗은 채취 팔의 눈에 띄게 묻은 도구 끝이 현지 토양에 닿는다.
- 구성 소유자: lander: lander equipment bay; arm: sampling arm; tip: soiled tool tip; soil: local soil.
- 방향 관계: arm → extends_from → lander; tip → part_of → arm; tip → contacts → soil.
- 혼동 경계: 귀환 표본·토양 더러움만으로 지구 미생물 확정.
- 주장 한계: 전방 경로를 표현한 허구 배치다. 생물 기원·전달·살균 실패는 별도 검증이 필요하다.
- 제안 슬롯: contact_point, procedure_step; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S08](https://planetaryprotection.jpl.nasa.gov/mission-implementation).

## V36 귀환 캡슐과 안쪽 봉쇄선

- 원문: 78, 79; 관찰: proxy; 우선순위: P0.
- EN: A return-sample capsule sits within a transparent isolator; the capsule, sealed glove ports and the outer clean laboratory remain separately visible.
- KO: 귀환 표본 캡슐이 투명 아이솔레이터 안에 있고 캡슐·밀폐 장갑 포트·바깥 청정 실험실이 분리되어 보인다.
- 구성 소유자: capsule: return-sample capsule; isolator: transparent containment box; ports: sealed glove ports; lab: outer laboratory.
- 방향 관계: capsule → inside → isolator; ports → part_of → isolator; isolator → inside → lab.
- 혼동 경계: 전방 오염 장면·맨손 표본 취급.
- 주장 한계: 역방향 오염 관리의 맥락이다. 실제 외계 위험·오염 발생·완벽한 무균은 배치로 증명되지 않는다.
- 제안 슬롯: object_structure, prop_placement; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S08](https://planetaryprotection.jpl.nasa.gov/mission-implementation).

## V37 표본 용기가 격리선을 넘는 순간

- 원문: 79; 관찰: still; 우선순위: P0.
- EN: A gloved arm carries a closed specimen container through an open isolation hatch toward an unsealed crew corridor; both sides of the hatch are visible.
- KO: 장갑 낀 팔이 닫힌 표본 용기를 열린 격리 해치로 통과시켜 밀폐되지 않은 승무원 복도 쪽으로 옮기며 해치 양쪽이 함께 보인다.
- 구성 소유자: arm: gloved carriers arm; container: closed specimen container; hatch: open isolation hatch; corridor: crew corridor; chamber: isolation chamber.
- 방향 관계: arm → holds → container; container → crosses → hatch; hatch → separates → chamber; corridor → outside → chamber.
- 혼동 경계: 격리실 안에서 든 용기·문만 열림.
- 주장 한계: 경계 통과만 가시적이다. 규정 위반·누출·질병 전파·비동의는 별도 맥락이다.
- 제안 슬롯: relational_action, contact_point, procedure_step; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S08](https://planetaryprotection.jpl.nasa.gov/mission-implementation).

## V38 두 몸의 경계가 합쳐진 접합

- 원문: 80, 83; 관찰: still; 우선순위: P1.
- EN: Two fictional bodies retain separate heads and limbs but share one continuous band of tissue between their torsos; the join has no intervening gap.
- KO: 허구 몸 두 개의 머리와 팔다리는 분리되어 있지만 몸통 사이 조직 띠가 틈 없이 하나로 이어진다.
- 구성 소유자: first: first fictional body; second: second fictional body; join: continuous tissue band; torso1: first torso; torso2: second torso.
- 방향 관계: torso1 → belongs_to → first; torso2 → belongs_to → second; join → merges_into → torso1; join → merges_into → torso2.
- 혼동 경계: 포옹·몸 겹침·별도 끈으로 묶임.
- 주장 한계: 관계는 조직 연속성이다. 생존·의식 수·수술·동의·정체성 상실은 미확정이다.
- 제안 슬롯: body_form, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare).

## V39 외피와 새 형태가 함께 드러난 단계

- 원문: 66, 81, 82; 관찰: still; 우선순위: P1.
- EN: A fictional figure has one intact outer shell region and one peeled-back region revealing differently structured limbs beneath; the layer boundary stays visible.
- KO: 허구 인물의 외피 일부는 온전하고 일부는 벗겨져 다른 구조의 팔다리가 아래에서 드러나며 층 경계가 보인다.
- 구성 소유자: figure: fictional figure; shell: partly intact outer shell; edge: peeled-back boundary; limbs: different limbs beneath shell.
- 방향 관계: shell → part_of → figure; edge → borders → shell; limbs → beneath → shell.
- 혼동 경계: 의상 탈의·다른 몸을 겹침.
- 주장 한계: 현재 이중 층만 보인다. 돌연변이 유전 원인·변신 능력·실제 시간 변화는 시퀀스가 필요하다.
- 제안 슬롯: transformation_stage, material_thickness; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare).

## V40 의료 덮개 밖으로 뻗은 손

- 원문: 85; 관찰: proxy; 우선순위: P1.
- EN: A covered fictional body lies on a supported medical platform; one articulated hand extends beyond the cover and grips the platform edge.
- KO: 지지된 의료대 위의 덮인 허구 몸에서 관절 있는 손 하나가 덮개 밖으로 나와 의료대 가장자리를 잡는다.
- 구성 소유자: body: covered fictional body; platform: supported medical platform; cover: opaque cover; hand: articulated hand; edge: platform edge.
- 방향 관계: body → on → platform; hand → belongs_to → body; hand → extends_beyond → cover; hand → grips → edge.
- 혼동 경계: 잠든 환자·시신 이동 노동.
- 주장 한계: 손의 자세만 보인다. 이전 사망·재생·타 생물의 조종은 설정과 시간 증거가 필요하다.
- 제안 슬롯: hand_pose, contact_point, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare).

## V41 표본화된 몸과 실험 장치의 관계

- 원문: 86, 161; 관찰: proxy; 우선순위: P1.
- EN: A fictional adult lies on a laboratory platform beneath a suspended examination instrument; a second operator watches from behind a separate observation pane.
- KO: 허구 성인이 실험대에 누워 있고 머리 위에는 검사 장치가 매달려 있으며 다른 조작자는 별도 관찰창 뒤에서 지켜본다.
- 구성 소유자: adult: fictional adult; platform: laboratory platform; instrument: suspended examination device; operator: separate operator; pane: observation pane.
- 방향 관계: adult → on → platform; instrument → above → adult; pane → separates → operator.
- 혼동 경계: 일반 의료 검사·살아 있음·비동의 자동 판정.
- 주장 한계: 생체 해부·살아 있음·가해 목적·비동의는 이 배치만으로 확정하지 않는다. 핵심 행위를 대체한 증거로 사용할 수 없다.
- 제안 슬롯: participant_role, prop_placement, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos).

## V42 인공 발생 용기와 외부 순환

- 원문: 94; 관찰: still; 우선순위: P1.
- EN: A transparent fictional gestation chamber encloses a curled nonhuman developing form in liquid; a cord-like line joins that form to a separate external circuit.
- KO: 투명한 허구 발생 용기 안 액체에 웅크린 비인간 발달체가 있고 끈 같은 연결선이 그 몸에서 별도 외부 순환 계통으로 이어진다.
- 구성 소유자: chamber: fictional gestation chamber; form: curled nonhuman developing form; liquid: chamber liquid; line: cord-like connection; circuit: external circuit.
- 방향 관계: chamber → encloses → form; liquid → surrounds → form; line → joins → form; line → joins → circuit.
- 혼동 경계: 표본병·동면 캡슐·인간 완전 체외 발생 달성.
- 주장 한계: 연구의 실제 양 실험과 이 SF 장면을 구분한다. 생식 원인·소유권·인간 적용·완전 발생을 주장하지 않는다.
- 제안 슬롯: object_structure, anatomical_connection, liquid_inclusion; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S17](https://www.nature.com/articles/ncomms15112).

## V43 산란 기관과 알의 비성적 접점

- 원문: 90; 관찰: still; 우선순위: P1.
- EN: A fictional insectlike creature bends a narrow terminal organ toward a crevice; one egg rests at the organ tip above an existing small clutch.
- KO: 허구 곤충형 생물이 가느다란 말단 기관을 틈 쪽으로 굽히고, 기관 끝에 알 하나가 기존 작은 알 무더기 위에 놓여 있다.
- 구성 소유자: creature: fictional insectlike creature; organ: terminal oviposition-like organ; egg: one egg; clutch: small clutch; crevice: substrate crevice.
- 방향 관계: organ → belongs_to → creature; egg → at_tip_of → organ; egg → above → clutch; clutch → inside → crevice.
- 혼동 경계: 성적 관통으로 자동 해석·알과 기관의 단절.
- 주장 한계: 산란 외형의 선택형 허구다. 생물학적 성공·수정·성폭력·숙주 종은 이 형상으로 판단하지 않는다.
- 제안 슬롯: anatomical_connection, contact_point, transformation_stage; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S16](https://entomology.mgcafe.uky.edu/ef018).

## V44 숙주막 안의 별도 몸 실루엣

- 원문: 87, 88, 89; 관찰: proxy; 우선순위: P1.
- EN: A translucent patch on a fictional hosts flank encloses a distinct curled inner silhouette; intact host surface surrounds the patch.
- KO: 허구 숙주 옆구리의 반투명 막 안으로 별도 웅크린 몸 실루엣이 보이고 온전한 숙주 표면이 그 막을 둘러싼다.
- 구성 소유자: host: fictional host; patch: translucent flank patch; inner: curled inner silhouette; surface: intact surrounding host surface.
- 방향 관계: patch → part_of → host; patch → encloses → inner; surface → surrounds → patch.
- 혼동 경계: 평범한 임신·문신·배양 용기.
- 주장 한계: 임신·기생·수정 원인·성별·동의는 외형만으로 확정하지 않는다. 강제 임신의 의미를 이 후보 하나로 대체하지 않는다.
- 제안 슬롯: body_form, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos), [S16](https://entomology.mgcafe.uky.edu/ef018).

## V45 유기 개구부의 상징적 이빨

- 원문: 97, 98; 관찰: still; 우선순위: P1.
- EN: A fictional organic doorway has paired fleshy folds around a central opening and inward-facing toothlike ridges along its rim; a metal floor stops at the threshold.
- KO: 허구 유기 출입구의 중앙 개구부를 쌍을 이룬 살 같은 주름이 둘러싸고 안쪽을 향한 이빨 같은 융기가 가장자리에 있으며 금속 바닥은 문턱에서 끝난다.
- 구성 소유자: opening: organic doorway opening; folds: paired fleshy folds; teeth: inward-facing toothlike ridges; rim: opening rim; floor: metal floor.
- 방향 관계: folds → surrounds → opening; teeth → along → rim; rim → bounds → opening; floor → ends_at → rim.
- 혼동 경계: 일반 입·원형 문·실제 생식기관이라고 단정.
- 주장 한계: vagina dentata의 추상화 가능성을 검토하는 저술이다. 성적 기관·공격·동의·작가 의도는 단정하지 않는다. 원전 도상 검증은 추가 과제다.
- 제안 슬롯: object_structure, surface_material, surreal_concept; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S29](https://www.routledge.com/link/link/p/book/9780367209452), [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films).

## V46 선체막에서 나오는 별도 소형 몸

- 원문: 57, 91; 관찰: still; 우선순위: P1.
- EN: A small fictional body protrudes through a split membrane integrated into the ship wall; the membrane edge and the emerging body have separate contours.
- KO: 선체 벽과 통합된 막이 갈라진 곳에서 작은 허구 몸이 나오며 막 가장자리와 나온 몸의 윤곽이 구분된다.
- 구성 소유자: wall: ship wall; membrane: integrated wall membrane; split: membrane split; body: small emerging body.
- 방향 관계: membrane → integrated_into → wall; split → part_of → membrane; body → emerges_through → split.
- 혼동 경계: 깨진 유리창·벽에 붙인 조각.
- 주장 한계: 출산·번식·모체 정체·고통·동의는 따로 정한 서사다.
- 제안 슬롯: transformation_stage, anatomical_connection; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films), [S20](https://www.ea.com/able/news/inside-dead-space-2-new-necromorph-nightmare).

## V47 생식 통제의 문서와 접근권 단서

- 원문: 92, 93, 159, 165; 관찰: proxy; 우선순위: P1.
- EN: An adult holds a rejected access card before a locked medical hatch; beside it a terminal carries distinct allocation and authorization fields.
- KO: 성인이 잠긴 의료 해치 앞에 거부된 출입 카드를 들고 있고 옆 단말에는 할당과 승인 칸이 나뉘어 있다.
- 구성 소유자: adult: adult cardholder; card: rejected access card; hatch: locked medical hatch; terminal: authorization terminal; fields: allocation and authorization fields.
- 방향 관계: adult → holds → card; card → before → terminal; fields → displayed_on → terminal; terminal → beside → hatch.
- 혼동 경계: 일반 예약 실패·복지 배분·임신 외형으로 강압 판정.
- 주장 한계: 생식 강압·우생학·비동의·기업 정책은 독립 서사·문서 맥락이 필요하다. 이 단서만으로 의미 완료를 선언하지 않는다.
- 제안 슬롯: visible_text, social_cue, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos), [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V48 인조인간의 열린 외피와 작동 부품

- 원문: 116, 117, 118; 관찰: still; 우선순위: P0.
- EN: A humanlike synthetic has a bounded service panel open at the forearm, revealing mechanical tendons continuous with the visible hand.
- KO: 인간형 합성체의 팔뚝에 한정된 정비 패널이 열려 있고 그 안 기계 힘줄이 보이는 손으로 이어진다.
- 구성 소유자: synthetic: humanlike synthetic; forearm: forearm casing; panel: open service panel; tendons: mechanical tendons; hand: visible hand.
- 방향 관계: forearm → belongs_to → synthetic; panel → part_of → forearm; tendons → inside → panel; tendons → continuous_with → hand.
- 혼동 경계: 보철 사용자 전체를 비인간·악으로 간주.
- 주장 한계: 합성 외형은 의식·충성·불쾌감·타인의 실제 정체의 증거가 아니다.
- 제안 슬롯: anatomical_connection, object_structure; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S19](https://spectrum.ieee.org/the-uncanny-valley), [S24](https://www.rifters.com/blindsight/BS_main.htm).

## V49 화물 쪽과 승무원 쪽으로 갈린 차단

- 원문: 113, 114, 115, 160; 관찰: proxy; 우선순위: P1.
- EN: A sealed hatch separates an adult crew member from a protected cargo bay; a control arm holds the hatch latch while the cargo remains behind a second transparent barrier.
- KO: 닫힌 해치가 성인 승무원과 보호된 화물실을 나누고 제어 팔이 해치 걸쇠를 잡으며 화물은 두 번째 투명 차단막 뒤에 남아 있다.
- 구성 소유자: crew: adult crew member; hatch: sealed hatch; arm: control arm; latch: hatch latch; cargo: protected cargo; barrier: second transparent barrier.
- 방향 관계: hatch → separates → crew; arm → holds → latch; latch → part_of → hatch; cargo → behind → barrier.
- 혼동 경계: 일반 검역·승무원의 명령·기업 악의 추정.
- 주장 한계: 가시적인 차단 관계다. AI 목표·고의·배신·인간 희생 결정은 설정과 사건 증거가 필요하다.
- 제안 슬롯: relational_action, narrative_clue, contact_point; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [S22](https://www.bfi.org.uk/lists/10-great-lovecraftian-horror-films).

## V50 분리된 몸 두 개의 닮음

- 원문: 65, 108, 119, 120; 관찰: still; 우선순위: P1.
- EN: Two separately supported adult figures share closely matching faces and suits; each stands in a different doorway with distinct uninterrupted body contours.
- KO: 얼굴과 우주복이 매우 닮은 성인 둘이 다른 문간에 각각 서 있고 두 몸의 끊기지 않은 윤곽과 지지가 분리되어 보인다.
- 구성 소유자: first: first adult figure; second: second adult figure; door1: first doorway; door2: second doorway.
- 방향 관계: first → inside → door1; second → inside → door2; first → resembles → second.
- 혼동 경계: 거울·장노출·쌍둥이를 무조건 복제라고 단정.
- 주장 한계: 닮음과 두 몸만 보인다. 동일 인물·복제·기억·의식 연속성·시간선은 미확정이다.
- 제안 슬롯: subject_count, reflection_logic, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S19](https://spectrum.ieee.org/the-uncanny-valley), [S24](https://www.rifters.com/blindsight/BS_main.htm).

## V51 닫힌 동면 용기 안 열린 눈

- 원문: 112, 121; 관찰: proxy; 우선순위: P1.
- EN: An adult face with open eyes is visible behind a sealed capsule window; both hands rest inside the capsule below a separate exterior release handle.
- KO: 밀폐 캡슐 창 뒤 성인 얼굴의 눈이 떠 있고 두 손은 용기 안에 놓이며 해제 손잡이는 바깥에 분리되어 있다.
- 구성 소유자: adult: adult capsule occupant; window: sealed capsule window; hands: occupants hands; handle: exterior release handle; capsule: capsule enclosure.
- 방향 관계: window → reveals → adult; hands → inside → capsule; handle → outside → capsule.
- 혼동 경계: 깨어 있는 환자·포스터·의식과 눈뜸 동일시.
- 주장 한계: 눈뜸·접근 불가 외형이다. 의식·시간 지각·마비·고통·디지털 영생을 입증하지 않는다.
- 제안 슬롯: eye_detail, object_structure, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S09](https://www.nasa.gov/hrp/hazard-isolation-and-confinement/), [S13](https://sf-encyclopedia.com/entry/generation_starships).

## V52 비콘 발신기와 수신 화면

- 원문: 125, 126, 132; 관찰: proxy; 우선순위: P1.
- EN: A small beacon is wired to a playback unit inside an abandoned relay room; a separate receiver screen shows an incoming distress-call icon.
- KO: 버려진 중계실의 작은 비콘이 재생 장치에 배선되어 있고 별도 수신기 화면에는 들어오는 조난 호출 기호가 보인다.
- 구성 소유자: beacon: small wired beacon; player: playback unit; receiver: separate receiver; icon: distress-call icon; room: abandoned relay room.
- 방향 관계: beacon → wired_to → player; icon → displayed_on → receiver; beacon → inside → room.
- 혼동 경계: 정상 반복 조난 송신·방송 장비.
- 주장 한계: 재생과 수신의 인과·속임수·악의·발신자 정체는 별도 검증이 필요하다.
- 제안 슬롯: prop, anatomical_connection, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S06](https://www.nasa.gov/missions/tech-demonstration/space-communications-7-things-you-need-to-know/), [S18](https://nickbostrom.com/information-hazards.pdf).

## V53 가려진 신호 화면과 사람의 반응

- 원문: 127, 128, 129, 130, 131; 관찰: proxy; 우선순위: P1.
- EN: A researcher faces a partially occluded symbol display while a second person turns away and covers their eyes; the screen and both sightlines remain distinct.
- KO: 연구원 하나는 일부가 가려진 기호 화면을 향하고 다른 사람은 몸을 돌려 눈을 가리며 화면과 두 시선 방향은 구분된다.
- 구성 소유자: reader: first researcher; other: second person; screen: partly occluded symbol display; hands: second persons hands; eyes: second persons eyes.
- 방향 관계: reader → faces → screen; other → turns_away_from → screen; hands → belongs_to → other; hands → covers → eyes.
- 혼동 경계: 고장 화면·일반 눈부심·도마뱀 바실리스크.
- 주장 한계: 정보 위해·인지 효과·전염·진실성·인과는 표정·기호로 입증되지 않는다. 허구 매개체의 선택형 배치다.
- 제안 슬롯: gaze_target, relational_action, offscreen_context; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S18](https://nickbostrom.com/information-hazards.pdf).

## V54 같은 원문과 다른 두 번역

- 원문: 134, 8; 관찰: proxy; 우선순위: P1.
- EN: A translation desk places one alien-script panel between two separate output displays with different line arrangements; the analyst compares both outputs.
- KO: 번역 책상에서 외계 문자 패널 하나 양쪽에 줄 배열이 다른 출력 화면 두 개가 있고 분석가가 둘을 비교한다.
- 구성 소유자: source: one alien-script panel; left: first output display; right: second output display; analyst: analyst.
- 방향 관계: source → between → left; source → between → right; analyst → faces → left; right → differs_from → left.
- 혼동 경계: 단순 다른 언어 번역·위치가 다른 동일 화면.
- 주장 한계: 번역 정확도·명령 수용·인지재해·악의는 별도 언어·서사 근거가 필요하다.
- 제안 슬롯: visible_text, prop_placement, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S18](https://nickbostrom.com/information-hazards.pdf), [S24](https://www.rifters.com/blindsight/BS_main.htm).

## V55 강착 원반이 있는 블랙홀의 선택형 시각화

- 원문: 135, 138, 169; 관찰: proxy; 우선순위: P0.
- EN: A dark central shadow is bordered by a bright accretion disk; a bent image of the far disk segment arches above the shadow, with a small craft at the foreground edge.
- KO: 어두운 중심 그림자 둘레에 밝은 강착 원반이 있고 먼 원반 부분의 휜 상이 그림자 위로 솟으며 전경 가장자리에 작은 탐사선이 있다.
- 구성 소유자: shadow: dark central shadow; disk: bright accretion disk; lensed: bent far-disk image; craft: small foreground craft.
- 방향 관계: disk → surrounds → shadow; lensed → represents → disk; craft → foreground_to → shadow.
- 혼동 경계: 눈에 보이는 특이점·검은 구슬 표면·모든 블랙홀에 원반.
- 주장 한계: 시각화한 원반·렌즈상·그림자의 구분이다. 지평선 자체·특이점 관측·안전 거리·실측은 미입증이다.
- 제안 슬롯: reality_anchor, scale_relation, light_shape; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S10](https://science.nasa.gov/universe/black-holes/anatomy/).

## V56 길게 늘어난 선체 부품 사이의 연속성

- 원문: 136; 관찰: proxy; 우선순위: P1.
- EN: A fictional spacecraft has a stretched central truss connecting its still-recognizable nose and engine section; the connector remains continuous across the elongated gap.
- KO: 허구 우주선의 식별 가능한 기수와 엔진 사이를 길게 늘어난 중앙 트러스가 끊기지 않고 잇는다.
- 구성 소유자: nose: spacecraft nose; engine: engine section; truss: stretched continuous truss; craft: fictional spacecraft.
- 방향 관계: nose → part_of → craft; engine → part_of → craft; truss → joins → nose; truss → joins → engine.
- 혼동 경계: 긴 설계의 우주선·단순 모션 블러.
- 주장 한계: 조석력의 허구적 외형 제안이다. 실제 힘·늘어나는 과정·블랙홀 질량·물리 정확도를 입증하지 않는다.
- 제안 슬롯: surreal_physics_detail, object_structure; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S10](https://science.nasa.gov/universe/black-holes/anatomy/).

## V57 한 시야에서 이어지는 모순된 통로

- 원문: 145; 관찰: still; 우선순위: P1.
- EN: A clearly fictional corridor turns back through a doorway whose continuous floor edge rejoins the first corridor at an incompatible angle; both junctions remain unobscured.
- KO: 명시적 허구 복도가 문간을 지나 되돌아와 첫 복도에 맞지 않는 각도로 재접속하며 연속 바닥선과 두 접합부가 가려지지 않는다.
- 구성 소유자: first: first corridor; return: return corridor; door: connecting doorway; edge: continuous floor edge; junctions: two visible junctions.
- 방향 관계: return → rejoins → first; door → connects → return; edge → continues_through → door; junctions → belongs_to → edge.
- 혼동 경계: 어안 왜곡·곡면 건축·가려진 연결·비유클리드 수학 전체.
- 주장 한계: 의도된 투영 모순이지 실제 공간의 측정 증거가 아니다. 내부가 외부보다 크다는 주장에는 추가 시점·도면이 필요하다.
- 제안 슬롯: surreal_concept, reflection_logic, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S12](https://sf-encyclopedia.com/entry/gothic_sf).

## V58 경계가 있는 다른 공간의 삽입

- 원문: 140, 141, 142, 146; 관찰: still; 우선순위: P1.
- EN: A bounded opening in a ship wall reveals a landscape with a different horizon direction; the ordinary wall and its floor continue visibly around the opening.
- KO: 선내 벽의 경계 있는 구멍 안으로 다른 수평선 방향의 풍경이 보이고 평범한 벽과 바닥은 그 구멍 주위로 이어진다.
- 구성 소유자: wall: ship wall; opening: bounded opening; landscape: other landscape; floor: ordinary ship floor.
- 방향 관계: opening → inside → wall; opening → reveals → landscape; floor → continues_around → opening.
- 혼동 경계: 모니터·그림·정상 창·실제 웜홀 관측.
- 주장 한계: 차원·FTL·도약 오류·연결의 물리 실재는 허구 설정이다. 출발·도착 시각은 별도 증거다.
- 제안 슬롯: surreal_concept, reality_anchor, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S12](https://sf-encyclopedia.com/entry/gothic_sf), [S10](https://science.nasa.gov/universe/black-holes/anatomy/).

## V59 부분 조립 탐사기와 별도 완성 개체

- 원문: 124, 152, 153; 관찰: proxy; 우선순위: P1.
- EN: A robotic fabrication arm holds a half-built probe beside one complete probe of the same visible design; feedstock plates sit in a separate rack.
- KO: 로봇 제작 팔이 같은 외형의 완성 탐사기 하나 옆에서 반쯤 조립된 탐사기를 잡고 있고 원재료 판들은 별도 랙에 있다.
- 구성 소유자: arm: robotic fabrication arm; partial: half-built probe; complete: complete matching probe; feedstock: raw plates; rack: separate material rack.
- 방향 관계: arm → holds → partial; partial → resembles → complete; feedstock → inside → rack.
- 혼동 경계: 일반 제조공장·동일 군집을 복제로 단정.
- 주장 한계: 자기복제·자원 전환·절멸 명령·그레이 구의 증식은 작동·시간·목표 근거가 필요하다.
- 제안 슬롯: object_structure, procedure_step, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S28](https://www.seti.org/research/seti-101/fermi-paradox/).

## V60 산소 공급 접근권의 시각적 비대칭

- 원문: 159, 160, 163, 164, 165; 관찰: proxy; 우선순위: P1.
- EN: A worker stands outside a locked supply cage while a supervisor holds the only visible key near an oxygen-cylinder valve inside the cage.
- KO: 노동자는 잠긴 공급 철망 밖에 있고 감독자는 철망 안 산소통 밸브 근처에서 유일하게 보이는 열쇠를 쥐고 있다.
- 구성 소유자: worker: worker; supervisor: supervisor; key: only visible key; cage: locked supply cage; oxygen: oxygen cylinder; valve: cylinder valve.
- 방향 관계: worker → outside → cage; supervisor → holds → key; oxygen → inside → cage; valve → part_of → oxygen.
- 혼동 경계: 정상 안전관리·연료통·표정으로 가해 의도 단정.
- 주장 한계: 접근 비대칭의 단서다. 독점·살인·식민주의·강압·조직의 법적 권한은 독립 맥락이 필요하다.
- 제안 슬롯: social_cue, proxemics, narrative_clue; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos).

## V61 사람 유해와 처리 설비의 분리

- 원문: 166, 167, 168; 관찰: proxy; 우선순위: P1.
- EN: An anonymous fictional covered human-shaped body rests on a trolley beside a closed resource-processing hatch; a separate food tray remains on the opposite side of the room.
- KO: 덮인 익명 허구 인체 형태가 운반대 위 닫힌 자원 처리 해치 옆에 있고 음식 쟁반은 방 반대편에 분리되어 있다.
- 구성 소유자: body: covered fictional human-shaped body; trolley: support trolley; hatch: closed processing hatch; tray: separate food tray; room: processing room.
- 방향 관계: body → on → trolley; trolley → beside → hatch; tray → opposite_to → hatch.
- 혼동 경계: 일반 영안실·고기를 먹는 행위만으로 식인.
- 주장 한계: 사망·종·처리 경로·섭식 대상·제의 목적을 입증하지 않는다. 식인·시신 재활용의 완료 증거로 사용할 수 없다.
- 제안 슬롯: narrative_clue, prop_placement, participant_role; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [S23](https://www.bfi.org.uk/sight-and-sound/reviews/high-life-review-claire-denis-probes-outer-reaches-human-taboos).

## V62 배관의 임시 수리와 노후 표면

- 원문: 173, 174; 관찰: still; 우선순위: P0.
- EN: Exposed pipes run over chipped wall paint; a patch clamp and a fresh gasket interrupt one corroded pipe joint while neighboring joints remain worn.
- KO: 벗겨진 벽 도장 위 노출 배관의 부식 접합부 하나에 보수 클램프와 새 개스킷이 있고 주변 접합부는 닳아 있다.
- 구성 소유자: pipes: exposed pipes; wall: chipped painted wall; joint: corroded joint; clamp: patch clamp; gasket: fresh gasket.
- 방향 관계: pipes → over → wall; clamp → covers → joint; gasket → inside → joint.
- 혼동 경계: 산업 양식 자체를 쇠락으로 간주·무작위 녹 텍스처.
- 주장 한계: 노후와 보수 대비만 보인다. 정비 실패·누수 성분·기업 과실·오랜 시간은 미확정이다.
- 제안 슬롯: texture, aftermath_trace, object_structure; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V63 CRT·테이프·물리 조작계의 기능 배치

- 원문: 173, 180; 관찰: still; 우선순위: P0.
- EN: A curved CRT monitor sits above a tape transport and a bank of physical toggle switches; a crew members hand rests on one switch rather than a floating hologram.
- KO: 곡면 CRT 아래 테이프 구동부와 물리 토글 스위치 열이 있고 승무원 손은 홀로그램 대신 스위치 하나 위에 놓인다.
- 구성 소유자: crt: curved CRT monitor; tape: tape transport; switches: physical toggle-switch bank; hand: crew members hand.
- 방향 관계: crt → above → tape; switches → beside → tape; hand → contacts → switches.
- 혼동 경계: 카세트 음악 컬렉션·VHS 노이즈만·출판 형식을 기술 양식과 동일시.
- 주장 한계: Cassette Futurism의 저술한 외형 조합이다. 정보 지연·정확한 시대·실제 발견 영상 여부는 미확정이다.
- 제안 슬롯: prop, object_structure, contact_point; 실제 binding 승인 아님.
- gate: 관계 3개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver).

## V64 인물 옆을 차지한 큰 어두운 빈 구역

- 원문: 169, 171, 172, 177, 178, 179, 180; 관찰: still; 우선순위: P1.
- EN: A lone crew member occupies one edge of the frame beside a lit doorway; a long empty corridor and a broad unlit viewport occupy the remaining space without a visible creature.
- KO: 승무원 한 명이 켜진 문간 옆 화면 가장자리에 있고 긴 빈 복도와 넓고 어두운 관측창이 나머지를 차지하며 보이는 생물은 없다.
- 구성 소유자: crew: lone crew member; door: lit doorway; corridor: long empty corridor; viewport: broad unlit viewport; frame: image frame.
- 방향 관계: crew → beside → door; corridor → extends_from → door; viewport → adjacent_to → corridor; crew → at_edge_of → frame.
- 혼동 경계: 단순 노출 부족·괴물을 반드시 채움·부재를 전체 세계로 확장.
- 주장 한계: 음향·무음·화면 밖 생물의 실제 존재·관객 감정·시간 반복은 정지 화면으로 입증되지 않는다.
- 제안 슬롯: composition, offscreen_context, spatial_depth; 실제 binding 승인 아님.
- gate: 관계 4개를 같은 이미지에서 판독. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`; 원인/서사 진위는 별도.
- 출처: [S21](https://www.bfi.org.uk/features/alien-40-ridley-scott-sigourney-weaver), [S27](https://repeaterbooks.com/product/the-weird-and-the-eerie/), [S30](https://thequietus.com/culture/books/mark-fisher-weird-eerie-kubrick-tarkovsky-nolan-review/).

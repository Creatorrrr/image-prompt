# 신화 요소 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-01
- 대상: `photo-prompt-image-generator`
- 입력: 참조 대화 「신화 요소 조사」의 38개 분류와 834개 키워드 항목
- 구현 범위: 한 장의 이미지에서 구성요소와 관계를 반증할 수 있는 10개 신화 모티프, 모티프별 6개 슬롯 후보, 좁은 정확 구문의 시각 의무
- 비구현 범위: 이미지 생성, 렌더 픽셀 합격 판정, 사용자 미감 판정, 종교적 진위나 의례 효능 판정, 신화 전체를 하나의 외형으로 고정하는 규칙

## 1. 결론

참조 대화의 목록은 검색용 어휘집으로는 넓고 유용하지만, 그 항목을 그대로 하드 시각 규칙으로 만들면 세 가지 오류가 생긴다.

1. `myth`, `pantheon`, `underworld`, `fate`, `flood`, `world tree` 같은 넓은 말이 특정 문화의 한 외형으로 고정된다.
2. 사건 이름이 소품이나 분위기로 축약된다. 예를 들어 운명의 실은 붉은 실, 카타바시스는 동굴, 대홍수는 비 오는 배, 신격화는 빛나는 인물로 대체되기 쉽다.
3. 서로 다른 전승의 인물·도상·의례가 한 장면에 혼합되고, 그 결과를 역사적·종교적 사실처럼 보이게 한다.

따라서 이번 확장은 다음 두 층만 구현한다.

- **하드 시각 계약**: 좁은 정확 구문이 들어왔을 때만 활성화하며, 행위자·대상·관계·전환·결과의 다섯 독립 증거를 모두 요구한다.
- **자문형 후보팩**: 각 모티프를 `aesthetic_trend`, `subject`, `action`, `location`, `prop`, `composition`의 여섯 슬롯으로 분해한다. 의미 검색은 후보 제안일 뿐 하드 활성화가 아니다.

결과적으로 10개 프로필과 60개 후보를 추가했다. 넓은 문화명·신명·장르명·상징어는 후보 검색에 남기고 단독으로는 의무를 만들지 않는다.

## 2. 선별 기준

참조 대화의 38개 분류 가운데 아래 조건을 모두 만족하는 모티프를 우선했다.

1. 이름을 제거해도 한 장면에서 관찰 가능한 구조가 남는다.
2. 최소 다섯 개의 독립 구성요소 또는 관계를 정의할 수 있다.
3. 가장 가까운 실패 대체물을 구체적으로 열거할 수 있다.
4. 박물관·학술기관·문화기관의 자료로 핵심 관계와 변이 경계를 확인할 수 있다.
5. 특정 문화의 고유 전승을 일반 비교 모티프와 분리할 수 있다.

선별 결과는 창세 3개, 우주 구조 1개, 운명 1개, 신적 지위 전환 1개, 저승 하강 1개, 사후 심판 1개, 대홍수 보존 1개, 질서 수립 전투 1개다.

## 3. 공통 시각 의미 모델

각 계약은 다음 고정 질문에 답해야 한다.

| 차원 | 질문 | 단독으로 부족한 대체물 |
|---|---|---|
| 행위자 | 누가 사건을 시작하거나 겪는가? | 의상, 이름표, 신화적 분위기 |
| 대상·영역 | 무엇이 변하거나 연결되는가? | 상징 소품 하나, 일반 배경 |
| 관계 | 행위자와 대상이 어떻게 물리적으로 이어지는가? | 나란히 배치, 시선만 공유 |
| 전환 | 이전 상태에서 이후 상태로 무엇이 달라지는가? | 완성 상태만 제시, 추상 발광 |
| 결과 | 그 변화 때문에 주변에 무엇이 새로 생기는가? | 무관한 효과, 장식적 파편 |

하나라도 빠지면 `partial = fail`이다. 문구가 존재한다는 사실은 프롬프트 검증일 뿐 렌더 픽셀 합격이 아니다.

## 4. 구현한 10개 모티프

### 4.1 Earth-diver: 회수된 흙이 최초의 땅이 되는 인과

Oxford Academic의 창세신화 개관은 earth-diver, cosmic egg, world-parents를 서로 다른 반복 유형으로 구분한다. earth-diver 유형에서 보존할 시각 핵심은 원초의 물, 잠수 행위자, 아래에서 가져온 적은 양의 흙, 수면 귀환, 같은 흙에서 시작되는 최초의 땅이다.

- 프로필: `earth_diver_first_land_creation`
- 필수 증거: 육지 없는 물 / 잠수자 하나 / 회수된 흙덩이 / 수면으로의 귀환 / 동일 물질에서 퍼지는 첫 땅
- 실패 대체물: 평범한 동물 수영, 보물 든 잠수자, 기존 해안의 진흙, 회수 과정 없는 완성 섬
- 문화 경계: 북미·시베리아·남아시아 등 개별 전승의 동물종·창조자·장소를 일반 계약이 대신하지 않는다. 이름이 붙은 변형은 해당 전승의 출처와 사용자 정의를 우선한다.

### 4.2 Cosmic egg: 알의 자체 물질이 세계 질서로 이어지는 전환

같은 비교 창세 자료는 cosmic egg를 별도 유형으로 다룬다. 단순한 알 상징이 아니라 하나의 닫힌 원초 알, 내부 세계 가능성, 갈라지는 경계, 껍질·내부와 새 우주 구조의 물질 연속성, 새로 정렬된 세계 층이 필요하다.

- 프로필: `cosmic_egg_world_emergence`
- 필수 증거: 원초 알 하나 / 경계 안의 내부 / 원인으로 읽히는 파열 / 알-우주 물질 연속성 / 새 세계 층
- 실패 대체물: 장식 알, 보통 새 부화, 깨진 껍질 뒤의 별도 행성, 알과 무관한 우주 폭발
- 변이 경계: 알에서 무엇이 나오고 껍질이 어떤 세계 부분이 되는지는 전승마다 다르므로 기본 계약은 특정 인물·색·도상을 강제하지 않는다.

### 4.3 World-parent separation: 접촉한 하늘과 땅의 분리로 생기는 빛

뉴질랜드 문화유산 자료 Te Ara의 Ranginui와 Papatūānuku 항목은 맞닿은 하늘 아버지와 땅 어머니가 자식 Tāne에 의해 분리되고 빛과 공간이 열리는 마오리 전승을 보여준다. 이 자료에서 일반화하는 것은 `접촉 → 능동 분리 → 새 간격 → 빛/세계 공간`의 관계뿐이다.

- 프로필: `world_parent_separation_creation`
- 필수 증거: 구분되지만 맞닿은 두 부모 / 눌린 초기 공간 / 능동 분리자·힘 / 같은 두 존재 사이의 증가 간격 / 그 틈의 첫 빛
- 실패 대체물: 멀리 선 거인 둘, 평범한 지평선, 분리 없는 포옹, 부모 없는 빛줄기
- 문화 경계: generic 후보가 Ranginui, Papatūānuku, Tāne의 고유 이름·계보·형상을 다른 전승에 이식하지 않는다. 마오리 변형을 요청하면 Te Ara와 해당 문화 문맥이 우선한다.

### 4.4 Axis mundi: 한 중심축의 삼계 경계 통과

The Metropolitan Museum of Art의 Maya `Deity face pendant` 자료는 세계축을 저승에 뿌리를 두고 하늘에 가지를 뻗는 큰 나무로 설명하고, `Earflare Set` 자료는 세계의 중심을 영역 사이의 이동·전환 지점으로 설명한다. 일반 계약은 특정 Maya 도상을 복제하지 않고, 하나의 중심축과 서로 다른 아래·가운데·위 영역, 두 경계 통과, 전 높이의 연속 연결만 추출한다.

- 프로필: `axis_mundi_three_realm_connection`
- 필수 증거: 중심축 하나 / 구별되는 삼계 / 하부 경계 통과 / 상부 경계 통과 / 한 경로의 연속성
- 실패 대체물: 거대한 장식 나무, 한 풍경의 탑, 분리된 세 패널, 경계를 잇지 않는 산
- 적용 경계: `axis mundi`, `world tree`, `sacred mountain` 단독어는 전승별 변이가 커 하드 활성화하지 않는다.

### 4.5 Moirai: 하나의 생명실에 대한 세 역할

The Met의 Three Fates 자료는 Clotho, Lachesis, Atropos를 생명실을 잣고, 길이를 배정·측정하고, 자르는 역할로 구분한다. 시각 계약은 여성 세 명이나 실 소품이 아니라 한 실 위에 분리된 세 행동이 동시에 연결되는가를 본다.

- 프로필: `moirai_fate_thread_life_allocation`
- 필수 증거: 서로 다른 세 운명신 / 실의 시작을 잣는 역할 / 같은 실을 재는 역할 / 같은 실의 끝을 자르는 역할 / 세 행동을 잇는 한 생명실
- 실패 대체물: 무관한 실을 든 세 인물, 가위 든 재봉사 한 명, 측정 없는 끊어진 실, 일반적인 붉은 인연실
- 문화 경계: 이 계약은 그리스 Moirai 요청에 한정한다. Norse Norns나 다른 운명 존재를 자동으로 동일한 세 도구·역할로 바꾸지 않는다.

### 4.6 Apotheosis: 같은 필멸자가 신적 질서에 수용되는 지위 전환

British Museum의 Apotheosis of Homer 부조는 Homer의 지속된 인물성, 관을 씌우는 행위, 신격화된 배치와 주변 인물군을 한 장면에 결합한다. 여기서 추출하는 것은 특정 부조 구도나 인물 복제가 아니라 `필멸자 표식 → 경계 횡단 → 신적 질서의 영접·수여 → 새 지위`다.

- 프로필: `mythic_apotheosis_mortal_divine_transition`
- 필수 증거: 같은 필멸자 / 이전 지위의 표식 / 필멸-신적 경계 / 신적 집단의 능동 영접·수여 / 새로 부여된 표지나 자리
- 실패 대체물: 떠오르는 빛나는 인물, 신을 숭배하는 인간, 보통 왕의 대관식, 다른 신으로 인물 교체
- 적용 경계: `apotheosis` 단독어는 미술사·정치·비유 문맥에서도 쓰이므로 좁은 장면 구문만 하드 활성화한다.

### 4.7 Katabasis: 살아 있는 방문자의 방향성 있는 저승 하강

Getty의 고대 저승 자료와 Orpheus 관련 테라코타 자료는 살아 있는 영웅이 목적을 가지고 저승으로 내려가는 katabasis 사례를 제공한다. 하강은 어두운 장소가 아니라 살아 있는 출발자, 인간 세계의 뒤쪽 단서, 경계 통과의 방향, 저승 목적지, 방문 목적의 결합이다.

- 프로필: `katabasis_living_underworld_descent`
- 필수 증거: 살아 있는 방문자 / 뒤에 남은 인간 세계 / 아래로 향하는 문·계단·강 경계 / 구별되는 저승 / 회수물·안내 표식·임무 목적
- 실패 대체물: 보통 동굴 탐험, 시신 매장, 죽은 영혼의 psychopomp 호송, 방향 없는 어두운 여행
- 분리 경계: 기존 `korean_afterlife_guide_escort`처럼 죽은 이를 안내하는 관계와 의도적으로 분리한다. 살아 있는 방문자와 죽은 이의 호송은 다른 계약이다.

### 4.8 Egyptian weighing of the heart: 심장-깃털 저울과 판결의 역할 체계

British Museum의 Papyrus of Ani와 Greenfield Papyrus 기록은 죽은 이의 심장을 Ma'at의 깃털과 견주는 저울, Anubis의 관여, Thoth의 기록, Ammit 또는 Osiris와 연결된 결과를 보여준다.

- 프로필: `egyptian_heart_weighing_judgment`
- 필수 증거: 죽은 피심판자 / 심장 대 Ma'at 깃털의 양팔저울 / 저울을 다루는 Anubis / 결과를 기록하는 Thoth / Ammit 또는 Osiris가 만드는 결과
- 실패 대체물: 정의의 저울, 저울 없는 Anubis, 장식용 심장·깃털, 그리스와 이집트 판결자의 혼합
- 문화 경계: 이 프로필은 고대 이집트의 이름 붙은 장면에만 사용한다. 일반 `afterlife judgment`나 다른 문화의 심판을 이 구성으로 고정하지 않는다. 박물관 파피루스의 인물 배치·선·색·상형문자를 복제하지 않는다.

### 4.9 Great Flood: 봉인된 보존 선박과 살아남음의 결과

British Museum의 Flood Tablet은 배의 준비, 가족과 살아 있는 것·물자의 탑승, 문을 닫고 봉인함, 홍수, 물의 진정과 정박, 새의 방출을 포함하는 서사 증거를 제공한다. 한 장에서는 전체 시간을 그대로 증명할 수 없으므로 준비·보존·재난·생존 결과를 압축하되 서로 연결해야 한다.

- 프로필: `mythic_flood_preservation_vessel`
- 필수 증거: 목적 제작 선박 / 선택된 생명·씨앗·물자 / 봉인·보호 구조 / 육지 표식을 삼킨 세계 규모 물 / 물러남·착지·새 방출 같은 생존 결과
- 실패 대체물: 폭풍 속 어선, 피난선, 배 옆의 동물, 고요한 물 위의 빈 방주
- 변이 경계: Gilgamesh의 Flood Tablet은 근거 사례이지 모든 대홍수 전승의 공통 세부를 대표하지 않는다. 특정 전승 요청 시 선박 형태·탑승자·동물·착지 장소를 해당 출처에 맞춘다.

### 4.10 Chaoskampf / Combat Myth: 전투의 패배 결과가 우주 질서가 되는가

ORACC의 Marduk와 Tiamat 자료는 바빌로니아 전승에서 영웅과 원초 바다 존재의 전투 및 그 뒤의 우주 질서 수립을 확인할 수 있는 전문 학술 자료다. 다만 St Andrews 연구는 `Chaoskampf`가 광범위한 문헌을 하나의 가정된 틀로 묶을 위험이 있는 논쟁적 비교 용어임을 지적하며 `Combat Myth` 같은 더 제한적인 표현을 검토한다.

- 프로필: `chaoskampf_cosmogonic_ordering`
- 필수 증거: 전승에 묶인 챔피언 / 구별되는 원초 혼돈의 적 / 읽히는 전투 접촉 / 적의 패배·분할 전환 / 그 결과 생긴 경계·세계 물질·안정된 영역
- 실패 대체물: 일반 드래곤 전투, 이미 죽은 괴물, 투기장 결투, 전투와 무관한 우주 배경
- 용어 경계: `Chaoskampf`는 편의적 비교 레이블로만 취급한다. Marduk–Tiamat 같은 이름 붙은 변형을 다른 문화에 덮어씌우지 않으며, 단순한 폭풍신·뱀·용 전투는 우주 질서 결과가 없으면 실패한다.

## 5. 후보팩 설계

각 모티프는 여섯 슬롯에 정확히 한 후보씩 추가되어 총 60개다.

| 프로필 | aesthetic_trend | subject | action | location | prop | composition |
|---|---|---|---|---|---|---|
| earth diver | `earth_diver_creation_aesthetic` | `earth_diver_creation_subject` | `earth_diver_retrieve_first_earth_action` | `primordial_ocean_without_land_location` | `earth_diver_first_mud_clod_prop` | `earth_diver_surface_return_composition` |
| cosmic egg | `cosmic_egg_creation_aesthetic` | `cosmic_egg_creation_subject` | `cosmic_egg_world_hatching_action` | `primordial_void_egg_location` | `cosmic_egg_shell_world_transition_prop` | `cosmic_egg_rupture_composition` |
| world parents | `world_parent_separation_aesthetic` | `world_parent_separation_subject` | `world_parent_forced_apart_action` | `compressed_sky_earth_location` | `first_light_gap_prop` | `world_parent_vertical_separation_composition` |
| axis mundi | `axis_mundi_connection_aesthetic` | `axis_mundi_three_realm_subject` | `axis_mundi_realm_crossing_action` | `three_realm_vertical_location` | `axis_boundary_transition_prop` | `axis_mundi_full_height_composition` |
| Moirai | `moirai_fate_thread_aesthetic` | `moirai_three_role_subject` | `moirai_spin_measure_cut_action` | `fate_overlook_workplace_location` | `continuous_mortal_life_thread_prop` | `moirai_role_thread_composition` |
| apotheosis | `mythic_apotheosis_aesthetic` | `apotheosis_same_mortal_subject` | `apotheosis_divine_investiture_action` | `mortal_divine_threshold_location` | `mortal_token_divine_regalia_prop` | `apotheosis_continuity_composition` |
| katabasis | `katabasis_underworld_aesthetic` | `katabasis_living_traveler_subject` | `katabasis_threshold_descent_action` | `living_to_underworld_gate_location` | `katabasis_objective_token_prop` | `katabasis_directional_composition` |
| Egyptian judgment | `egyptian_heart_weighing_aesthetic` | `egyptian_judgment_ensemble_subject` | `anubis_heart_balance_action` | `egyptian_hall_of_judgment_location` | `heart_feather_balance_prop` | `egyptian_judgment_register_composition` |
| great flood | `mythic_flood_preservation_aesthetic` | `mythic_flood_vessel_subject` | `mythic_flood_seal_preserve_action` | `world_covering_deluge_location` | `preserved_lineage_cargo_prop` | `mythic_flood_vessel_world_composition` |
| Chaoskampf | `chaoskampf_combat_myth_aesthetic` | `chaoskampf_champion_adversary_subject` | `chaoskampf_defeat_order_action` | `primordial_sea_combat_location` | `chaoskampf_order_boundary_prop` | `chaoskampf_combat_consequence_composition` |

모든 후보는 `id`, 한·영 표현, 가중치, 태그, 별칭, 키워드, `embedding_text`를 가진다. 가중치는 후보 우선순위일 뿐 사실성 점수나 하드 활성화 임계값이 아니다.

## 6. 하드 활성화와 자문 검색의 경계

### 하드 활성화하는 좁은 구문 예

- `earth-diver creation myth`
- `cosmic egg creation myth`
- `world-parent separation myth`
- `mythic axis mundi`
- `Moirai life thread`
- `mythic apotheosis of a mortal`
- `mythic katabasis into the underworld`
- `Egyptian weighing of the heart`
- `great flood myth preservation vessel`
- `Chaoskampf cosmogonic combat`

### 단독으로 하드 활성화하지 않는 말

- `myth`, `mythology`, `folklore`, `legend`, `pantheon`
- `creation`, `cosmogony`, `world tree`, `sacred mountain`, `axis mundi`
- `fate`, `destiny`, `thread`, `apotheosis`, `katabasis`, `underworld`
- `Anubis`, `Thoth`, `Osiris`, `Moirai`, `flood`, `ark`, `dragon`, `chaos`, `order`
- 특정 문화명, 종교명, 신명, 민족명만 있는 요청

직접 정확 구문은 하드 계약을 만든다. BM25F·임베딩 유사도는 후보를 제안할 수 있지만 구성요소 증거가 없는 새 하드 의무를 만들 수 없다.

## 7. 문화·안전·재사용 경계

- 박물관 유물과 필사본은 관계를 이해하는 근거이지 복제할 레이아웃 템플릿이 아니다. 원본 선, 색, 장식, 상형문자, 인물 배치, 손상 흔적을 복제하지 않는다.
- 살아 있는 전통과 신성한 인물·의례는 장식적 혼합 재료로 취급하지 않는다. 이름 붙은 전승은 해당 문화 출처와 사용자의 구체적 정의를 우선한다.
- 의례·주문·희생·장례의 실제 수행법, 읽을 수 있는 신성 문구, 초자연적 효능 주장은 후보에 넣지 않는다.
- 외형만으로 종교, 민족, 국적, 도덕성, 영적 상태, 사후 운명, 신적 정체성을 추론하지 않는다.
- 비교 유형은 검색과 시각 구조 분석을 위한 추상화다. 역사적 전파 관계나 보편 원형의 증명이 아니다.

## 8. 검증 설계

### 8.1 구조·패키지 검증

- 확장 JSON과 시각 의무 레지스트리가 파싱되어야 한다.
- 여섯 슬롯에 모티프별 한 후보, 총 60개가 있어야 한다.
- 10개 프로필은 각각 구성요소 그룹 5개, 근거 필드 5개, 렌더 게이트 5개, 실패 대체물 5개 이상을 가져야 한다.
- 모든 후보 ID, 프로필 ID, 렌더 게이트 ID는 중복되지 않아야 한다.
- 연구 근거 행은 후보와 프로필을 역참조해야 한다.

### 8.2 프롬프트 동작 검증

- 좁은 정확 구문 10개가 각각 하나의 의도된 프로필만 활성화해야 한다.
- 광범위한 단독어와 인접 개념은 새 프로필을 활성화하지 않아야 한다.
- `katabasis`는 죽은 이의 안내 계약과, `Moirai`는 일반 fate/thread와, `Chaoskampf`는 일반 dragon fight와 분리되어야 한다.
- 의미 인덱스에는 60개 후보가 모두 들어가되 의미 검색 결과만으로 하드 시각 의무를 만들지 않아야 한다.

### 8.3 아직 주장하지 않는 증거층

- **패키지 PASS**: 파일·스키마·인덱스가 일관된다는 뜻이다.
- **프롬프트 PASS**: 정확 구문·부정 대조·의무 구성요소가 텍스트 경로에서 맞는다는 뜻이다.
- **렌더 UNTESTED**: 실제 생성 이미지가 다섯 게이트를 모두 만족하는지는 이번 작업에서 검증하지 않는다.
- **사용자 판단 UNSCORED**: 문화적 적합성, 미감, 선호는 사용자가 별도로 판단해야 한다.

## 9. 출처

1. Oxford Academic, *Creation Myths* chapter: https://academic.oup.com/book/44435/chapter-abstract/377431577
2. Kokugakuin University, Kojiki creation-type commentary: https://kojiki.kokugakuin.ac.jp/kojiki/%E5%A4%A9%E5%9C%B0%E5%88%9D%E7%99%BA/
3. Te Ara, *Ranginui and Papatūānuku*: https://teara.govt.nz/en/artwork/2426/ranginui-and-papatuanuku
4. The Metropolitan Museum of Art, Maya axis-mundi records: https://www.metmuseum.org/art/collection/search/319873 and https://www.metmuseum.org/art/collection/search/317430
5. The Metropolitan Museum of Art, *The Three Fates*: https://www.metmuseum.org/art/collection/search/373996
6. British Museum, *The Apotheosis of Homer*: https://www.britishmuseum.org/collection/object/G_1819-0812-1
7. Getty, ancient terracotta and Underworld materials: https://www.getty.edu/publications/terracottas/catalogue/2/ and https://www.getty.edu/art/exhibitions/ancient_underworld/inner.html
8. British Museum, Papyrus of Ani weighing scene: https://www.britishmuseum.org/collection/object/Y_EA10470-3
9. British Museum, Greenfield Papyrus weighing scene: https://www.britishmuseum.org/collection/object/Y_EA10554-80
10. British Museum, Flood Tablet: https://www.britishmuseum.org/collection/object/W_K-3375
11. ORACC, Marduk and Tiamat: https://oracc.museum.upenn.edu/amgg/listofdeities/marduk/index.html and https://oracc.museum.upenn.edu/amgg/Listofdeities/Tiamat/index.html
12. ORACC, technical terms: https://oracc.museum.upenn.edu/cams/akno/technicalterms/index.html
13. University of St Andrews research repository, terminology critique of Chaoskampf: https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/33626/Thesis-Clayton-Mills-complete-version.pdf?isAllowed=y&sequence=5

## 10. 판정

현재 판정은 `implemented / prompt-behavior`다. 집중 검증에서 10개 정확 라우팅, 광범위 단독어·인접 대체물 부정 대조, 60개 후보의 런타임 병합, 연구 근거 결합이 모두 통과했다. 이미지 생성과 픽셀 판정은 이번 범위 밖이므로 `promote`나 렌더 품질 개선을 주장하지 않는다. 기존 전체 회귀 묶음은 34개 테스트가 통과했지만, 신화 프로필과 무관한 `clinical_nursing_duty_system`이 기존 yandere fixture의 간호사 문구에도 함께 활성화되어 6건이 실패했다. 동일 입력을 HEAD 레지스트리와 현재 레지스트리에 각각 적용했을 때 결과가 같았으므로 이번 신화 확장의 회귀로 분류하지 않는다.

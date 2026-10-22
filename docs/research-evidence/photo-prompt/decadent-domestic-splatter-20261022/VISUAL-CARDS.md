# 시각 의미 카드

모든 배열·장면은 새로 저술한 선택안이다. 출처가 같은 모양의 장면을 묘사했다는 뜻이 아니다. 관계별 gate와 소유자는 JSON에 보존한다. 프록시는 서사 의미 자체의 통과 증거가 아니며 H 카드는 긍정 시각 초안을 만들지 않는다.

## 호사·인공성·쇠락

### A01 금박 손실과 드러난 바탕

- 모드/우선순위: still / P0; 제안 역할: surface_material, prop_state
- 한글: 금박 액자의 한정된 박락 부위에서 밑바탕이 드러나고 남은 금빛 면과 경계가 이어진다.
- English: A bounded loss in a gilded frame exposes its ground beside the continuous surviving gold-colored surface.
- 소유자: {"frame": "gilded frame", "loss": "bounded leaf loss", "ground": "exposed ground"}
- 관계: loss → within → frame; ground → visible_at → loss
- 혼동: 금 전체가 녹슨 철처럼 표현됨
- 주장 한계: 금박 손실의 외관이다. 순금의 부식·가문 몰락·정확한 연대는 증명하지 않는다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S43 Canadian Conservation Institute: Caring for metal objects](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)

### A02 은기 홈과 돌출부의 다른 표면

- 모드/우선순위: still / P0; 제안 역할: surface_material, texture
- 한글: 은빛 쟁반의 어두운 오목 홈과 밝은 돌출 가장자리가 같은 물건 안에서 구분된다.
- English: Dark recessed grooves and a bright raised rim remain distinguishable on the same silver-colored tray.
- 소유자: {"tray": "silver-colored tray", "groove": "dark recessed groove", "ridge": "bright raised rim"}
- 관계: groove → part_of → tray; ridge → part_of → tray; groove → adjacent_to → ridge
- 혼동: 검은 그림자만 존재, 금과 은의 성질 혼동
- 주장 한계: 재료 성분·황화 반응·손질 이력은 확인하지 않는다. 순금 녹과 혼합하지 않는다.
- 출처: [S43 Canadian Conservation Institute: Caring for metal objects](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)

### A03 파일이 닳은 벨벳 팔걸이

- 모드/우선순위: still / P1; 제안 역할: surface_material, prop_state
- 한글: 벨벳 의자의 팔걸이에 눌려 납작해진 파일 구역이 주변의 두툼한 파일과 맞닿아 있다.
- English: A flattened pile patch on a velvet chair armrest borders the surrounding plush pile.
- 소유자: {"chair": "upholstered chair", "arm": "velvet armrest", "patch": "flattened pile patch"}
- 관계: arm → part_of → chair; patch → within → arm
- 혼동: 피부 상처, 그림자만으로 마모 판정
- 주장 한계: 현재 표면의 차이만 보인다. 누가 얼마나 앉았는지·권태·질병은 별도다.
- 출처: [S27 Met: Renaissance Velvet Textiles](https://www.metmuseum.org/essays/renaissance-velvet-textiles)

### A04 정렬된 방과 뒤의 낡은 벽면

- 모드/우선순위: still / P1; 제안 역할: spatial_depth, environment_detail
- 한글: 정돈된 앞방에서 정렬된 열린 문들을 따라 뒤쪽 방의 벗겨진 벽면이 보인다.
- English: Aligned open doorways connect a tidy formal front room to a farther room with a peeling wall surface.
- 소유자: {"near": "near formal room", "doors": "aligned open doorways", "far": "far room", "wall": "peeling wall surface"}
- 관계: doors → connect → near; doors → lead_to → far; wall → part_of → far
- 혼동: 포스터 속 문, 서로 무관한 방을 몽타주
- 주장 한계: 이어지는 시선과 표면만 확인한다. 집 전체의 쇠락·숨은 범죄는 입증되지 않는다.
- 출처: [S25 Met: Visitors to Versailles](https://www.metmuseum.org/ko/press-releases/visitors-to-versailles-2018-exhibitions)

### A05 화려한 틈 안의 먼지

- 모드/우선순위: still / P1; 제안 역할: texture, prop_state
- 한글: 장식 조각의 깊은 홈에 무광의 먼지가 남고 돌출된 가장자리에는 하이라이트가 이어진다.
- English: Dull dust remains inside the deep recesses of an ornate carving while highlights follow its raised edges.
- 소유자: {"ornament": "ornate carved ornament", "recess": "carved recess", "dust": "dull dust deposit"}
- 관계: recess → part_of → ornament; dust → inside → recess
- 혼동: 먼지와 금속 변색을 동일시
- 주장 한계: 물리적 침착과 빛의 차이다. 방치 기간·신분·청결 습관을 확정하지 않는다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S43 Canadian Conservation Institute: Caring for metal objects](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)

### A06 축 늘어진 손과 손대지 않은 잔

- 모드/우선순위: proxy / P1; 제안 역할: hand_pose, prop_placement
- 한글: 앉은 성인의 힘 빠진 손이 의자 팔걸이에 놓이고 바로 옆에 잔 하나가 놓여 있다.
- English: A seated adult's relaxed hand rests on a chair arm beside a single glass.
- 소유자: {"person": "seated adult", "hand": "relaxed hand", "glass": "untouched-looking glass", "arm": "chair arm"}
- 관계: hand → belongs_to → person; hand → rests_on → arm; glass → beside → arm
- 혼동: 음주·중독·우울 진단으로 비약
- 주장 한계: 손의 자세·물건 위치는 보인다. 앙뉘·스플린·약물·내면 상태는 해석이다.
- 출처: [S03 Cambridge: Decadence](https://www.cambridge.org/core/journals/victorian-literature-and-culture/article/decadence/2621A4931E82EFF8948DCCE2DB7A3423)

### A07 생화 장식의 두 상태

- 모드/우선순위: still / P1; 제안 역할: prop_state, composition
- 한글: 한 화병 안에 곧은 줄기와 처진 줄기가 함께 있고 그 아래 떨어진 꽃잎이 놓인다.
- English: Upright and drooping stems share one vase, with fallen petals below it.
- 소유자: {"vase": "vase", "fresh": "upright fresh-looking stem", "wilted": "drooping stem", "petals": "fallen petals"}
- 관계: fresh → inside → vase; wilted → inside → vase; petals → below → vase
- 혼동: 한 꽃의 시계열이라고 단정, 몸의 부패로 전환
- 주장 한계: 현재 식물 상태의 병치다. 식물종·원인·관계 변화·경과 시간은 별도다.
- 출처: [S29 National Gallery: Treck, Vanitas Still Life](https://www.nationalgallery.org.uk/paintings/jan-jansz-treck-vanitas-still-life)

### A08 정돈된 얼굴과 풀린 실내 장식

- 모드/우선순위: proxy / P1; 제안 역할: character_contrast, environment_detail
- 한글: 단정히 꾸민 성인이 거울 곁에 있고 옆 벽의 장식 천 한쪽이 풀려 늘어진다.
- English: A carefully groomed adult stands beside a bounded mirror while one edge of the adjacent wall fabric hangs loose.
- 소유자: {"adult": "carefully groomed adult", "mirror": "bounded mirror", "wall": "wall beside mirror", "fabric": "loosened wall fabric"}
- 관계: adult → beside → mirror; fabric → hangs_from → wall; wall → beside → mirror
- 혼동: 외모로 도덕·질병 판정
- 주장 한계: 외양과 방의 상태를 대비한다. 댄디즘·죄책감·통제 욕망은 외형이 증명하지 않는다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S03 Cambridge: Decadence](https://www.cambridge.org/core/journals/victorian-literature-and-culture/article/decadence/2621A4931E82EFF8948DCCE2DB7A3423)

### A09 서로 다른 방의 인공 조명 구획

- 모드/우선순위: still / P1; 제안 역할: light_color, space_condition
- 한글: 앞방의 차가운 빛과 열린 문 너머의 따뜻한 빛이 문틀에서 구분된다.
- English: Cool illumination in the front room meets warm illumination beyond an open doorway at the doorframe.
- 소유자: {"room": "room", "door": "open doorway", "near": "cool illumination zone", "far": "warm illumination zone"}
- 관계: near → inside → room; far → visible_through → door; door → part_of → room
- 혼동: 색만으로 지알로·악의·초자연 확정
- 주장 한계: 빛 구획의 선택안이다. 지알로에 특정 색이 필수라는 뜻이 아니다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S07 BFI: 10 great neo-giallo films](https://www.bfi.org.uk/lists/10-great-neo-giallo-films)

### A10 미니어처 전시와 사람 크기의 공간

- 모드/우선순위: proxy / P1; 제안 역할: scale_relation, composition
- 한글: 격식 있는 방의 작은 진열함 안에 미니어처들이 정렬되고 성인 거주자가 함 곁에 선다.
- English: Miniature objects are aligned inside a small display case in a formal room, with an adult resident beside it.
- 소유자: {"adult": "adult resident", "case": "small display case", "objects": "arranged miniature objects", "room": "formal room"}
- 관계: objects → inside → case; case → inside → room; adult → beside → case
- 혼동: 인물 자체가 소유물·인형이라고 확정
- 주장 한계: 크기·정렬·거리는 보인다. 대상화·수집 강박·재산권은 해석으로 남는다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### A11 바로크의 통합된 극적 공간

- 모드/우선순위: still / P1; 제안 역할: composition, light_direction
- 한글: 건축 벽감 안 조각의 굽이치는 옷 주름을 한 방향의 빛이 강조한다.
- English: Directional light emphasizes twisting sculpted drapery on a figure within an architectural niche.
- 소유자: {"niche": "architectural niche", "sculpture": "sculpture", "drape": "sculpted drapery", "light": "directional light patch"}
- 관계: sculpture → inside → niche; drape → part_of → sculpture; light → falls_on → sculpture
- 혼동: 금빛 물건 하나를 바로크 전체로 판정
- 주장 한계: 조각·건축·빛의 저술한 결합이다. 역사적 정본·연대·관객 감정을 보증하지 않는다.
- 출처: [S46 Rijksmuseum: Baroque](https://www.rijksmuseum.nl/en/collection/node/Baroque--7ce3f58e9fcb4702b31ff783fb88c963)

### A12 로코코의 비대칭 로카유 패널

- 모드/우선순위: still / P1; 제안 역할: surface_pattern, object_structure
- 한글: 밝은 패널 안에 조개와 곡선을 닮은 장식이 비대칭으로 이어진다.
- English: Asymmetric shell-like scrolls run across a pale panel bounded by its outer edge.
- 소유자: {"panel": "pale panel", "scroll": "asymmetric shell-like scroll", "edge": "panel edge"}
- 관계: scroll → within → panel; edge → bounds → panel
- 혼동: 바로크·아르누보를 같은 선무늬로 합침
- 주장 한계: 선·비대칭·색의 선택안이다. 모든 로코코에 같은 색이나 조개를 강제하지 않는다.
- 출처: [S22 Rijksmuseum: Rococo](https://www.rijksmuseum.nl/en/collection/node/Rococo--c40f1414283f45da861eeb4103b94d73)

### A13 아르누보의 줄기형 구조와 장식

- 모드/우선순위: still / P1; 제안 역할: object_structure, surface_pattern
- 한글: 난간의 줄기처럼 굽은 구조선과 실제 연결부가 하나의 장식 형태를 이룬다.
- English: Stem-like structural lines and visible joints form an integrated ornament in a railing.
- 소유자: {"rail": "railing", "stem": "stem-like structural line", "joint": "visible joint"}
- 관계: stem → part_of → rail; joint → connects_to → stem
- 혼동: 덩굴 그림·실제 혈관·괴물 촉수
- 주장 한계: 구조와 장식 통합의 제안이다. 생물·인체·성적 의미·특정 건축가 정본은 별도다.
- 출처: [S21 V&A: Art Nouveau - an international style](https://www.vam.ac.uk/articles/art-nouveau-an-international-style)

## 접근·자율성·노동 동선

### B01 양쪽 손과 한 개의 열쇠

- 모드/우선순위: proxy / P0; 제안 역할: relational_action, prop_placement
- 한글: 한 성인의 손이 열쇠 하나를 쥐고 다른 성인의 펼친 손 위쪽에 두고 있다.
- English: One adult's hand holds a single key above another adult's open hand.
- 소유자: {"holder": "adult holder", "hand": "holder hand", "other": "another adult open hand", "key": "single key"}
- 관계: hand → belongs_to → holder; hand → holds → key; key → above → other
- 혼동: 두 사람 모두 같은 열쇠를 쥠, 부양자를 가해자로 자동 지정
- 주장 한계: 소지와 손의 위치만 보인다. 거부·통제의 반복·소유권·관계는 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B02 몸이 가로지르는 출입선

- 모드/우선순위: still / P0; 제안 역할: proxemics, space_condition
- 한글: 성인 한 명이 열린 문 폭을 가로질러 서 있고 다른 성인이 문을 향해 선다.
- English: An adult stands across the width of an open doorway while another adult faces the opening.
- 소유자: {"adult": "blocking adult", "door": "open doorway", "other": "other adult", "floor": "visible crossing line"}
- 관계: adult → stands_across → door; other → faces → door; floor → crosses → door
- 혼동: 단순 옆에 선 몸, 문 바깥 출구가 보이지 않음
- 주장 한계: 현재 통행 배치다. 감금·위협·동의·도망 의도는 정지 화면만으로 확정하지 않는다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B03 경계 양쪽의 잠금장치

- 모드/우선순위: still / P0; 제안 역할: object_structure, space_condition
- 한글: 문 가까운 쪽 표면에 달린 빗장이 문틀 받이에 걸쳐 들어가 있다.
- English: A surface bolt mounted on the near face of a door extends into its receiver on the doorframe.
- 소유자: {"door": "door", "bolt": "surface bolt", "frame": "doorframe", "side": "visible near face"}
- 관계: bolt → mounted_on → door; bolt → extends_into → frame; side → part_of → door
- 혼동: 열쇠구멍만으로 잠김 판정, 반대편 구조 발명
- 주장 한계: 부품의 위치와 맞물림이다. 내부 사람·실제 잠김·탈출 불가능성·푸른 수염 서사는 별도다.
- 출처: [S05 Ellen Ledoux: Was there ever a Female Gothic?](https://www.nature.com/articles/palcomms201742), [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B04 돈을 덮는 손과 열린 지갑

- 모드/우선순위: proxy / P0; 제안 역할: relational_action, contact_point
- 한글: 열린 지갑 속 지폐를 한 성인의 손이 덮고 다른 성인의 손이 지갑 옆에 머문다.
- English: One adult's hand covers banknotes inside an open wallet while another adult's hand remains beside it.
- 소유자: {"holder": "adult hand", "money": "banknotes", "wallet": "open wallet", "other": "other adult hand"}
- 관계: holder → covers → money; money → inside → wallet; other → beside → wallet
- 혼동: 돈을 주는 순간을 강탈로 판정
- 주장 한계: 접촉과 접근 배치다. 경제적 학대·재산권·의존의 반복은 다른 증거가 필요하다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B05 같은 문서와 서로 다른 접근

- 모드/우선순위: proxy / P1; 제안 역할: relational_action, prop_placement
- 한글: 유리 앞면의 함 안에 문서 한 장이 놓이고 한 성인은 바깥에서, 다른 성인은 열린 함 곁에서 문서를 본다.
- English: A single document lies in a glass-front case, seen by one adult outside it and another beside its open section.
- 소유자: {"document": "single document", "case": "glass-front case", "adult": "adult outside case", "holder": "adult beside open case"}
- 관계: document → inside → case; adult → outside → case; holder → beside → case
- 혼동: 그림 속 문서, 글을 읽지 않고 유언으로 확정
- 주장 한계: 문서·구획·접근의 차이다. 상속 효력·강제 결혼·법적 소유는 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B06 전화기 사이의 분리된 손

- 모드/우선순위: proxy / P1; 제안 역할: contact_point, relational_action
- 한글: 한 손이 탁자 위 전화기를 들고 다른 성인의 펼친 손은 전화기와 떨어져 있다.
- English: One hand holds a phone above a table while another adult's open hand remains separate from it.
- 소유자: {"phone": "single phone", "hand": "holding hand", "other": "other open hand", "table": "table"}
- 관계: hand → holds → phone; phone → above → table; other → separate_from → phone
- 혼동: 다른 전화기를 목표 기기로 오인
- 주장 한계: 현재 소지와 거리다. 압수·연락 차단·계정 권한·강요는 입증하지 않는다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B07 다른 방에 연결된 호출 벨

- 모드/우선순위: still / P1; 제안 역할: object_structure, environment_detail
- 한글: 벽의 호출 손잡이에서 이어진 줄이 서비스 구역 벽의 벨까지 연속해 보인다.
- English: A continuous visible wire runs from a wall bell pull to a bell mounted in the service area.
- 소유자: {"pull": "bell pull", "wire": "visible wire run", "bell": "service bell", "wall": "service area wall"}
- 관계: pull → connects_to → wire; wire → leads_to → bell; bell → mounted_on → wall
- 혼동: 선이 끊기거나 다른 벨에 연결
- 주장 한계: 연결 구조의 저술안이다. 실제 소리·명령·복종·역사적 정본 배선은 확정하지 않는다.
- 출처: [S26 National Trust: Country house communication](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages)

### B08 격식 방과 보조 계단의 갈림

- 모드/우선순위: still / P1; 제안 역할: spatial_depth, location
- 한글: 한 계단참에서 격식 있는 방의 문과 좁은 보조 계단이 벽을 사이에 두고 갈라진다.
- English: A formal room doorway and a narrow service stair diverge from one landing on opposite sides of a partition.
- 소유자: {"landing": "landing", "formal": "formal room door", "stair": "narrow service stair", "partition": "partition wall"}
- 관계: formal → opens_from → landing; stair → rises_from → landing; partition → separates → formal; partition → separates → stair
- 혼동: 서로 다른 집을 합성, 복식으로 하인 지정
- 주장 한계: 동선 분리는 보인다. 사회적 신분·공모·노동 조건을 외형만으로 판정하지 않는다.
- 출처: [S26 National Trust: Country house communication](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages), [S42 National Trust: Servants rooms](https://www.nationaltrust.org.uk/discover/history/what-were-georgian-and-victorian-servants-rooms-like)

### B09 유리 온실의 출입 경계

- 모드/우선순위: proxy / P1; 제안 역할: space_condition, object_structure
- 한글: 유리 온실 안의 성인과 출입문 위 빗장이 한 화면에 보인다.
- English: An adult inside a glass greenhouse and a latch on its entry door are visible in the same frame.
- 소유자: {"greenhouse": "glass enclosure", "door": "enclosure door", "latch": "visible latch", "adult": "adult inside"}
- 관계: door → part_of → greenhouse; latch → on → door; adult → inside → greenhouse
- 혼동: 식물 보존을 인물 감금으로 자동 해석
- 주장 한계: 배치와 장치다. 실제 잠김·열쇠 소유·황금 새장·가학성은 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible), [S21 V&A: Art Nouveau - an international style](https://www.vam.ac.uk/articles/art-nouveau-an-international-style)

### B10 두 사람이 서로 다른 문고리를 잡음

- 모드/우선순위: still / P1; 제안 역할: relational_action, contact_point
- 한글: 같은 문의 가까운 문고리와 먼 문고리를 서로 다른 성인의 손이 각각 잡고 있다.
- English: Different adults' hands grip the near and far handles of the same door.
- 소유자: {"door": "single door", "handle1": "near handle", "handle2": "far handle", "hand1": "first adult hand", "hand2": "second adult hand"}
- 관계: handle1 → part_of → door; handle2 → part_of → door; hand1 → grips → handle1; hand2 → grips → handle2
- 혼동: 손 합쳐짐, 두 문, 가려진 손을 확인했다고 판정
- 주장 한계: 동시 접점만 확인한다. 힘의 승패·허가·탈출·과거 패턴은 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### B11 사적 화장 공간과 침실의 문턱

- 모드/우선순위: proxy / P1; 제안 역할: space_condition, prop_placement
- 한글: 화장 거울을 둔 탁자가 문 곁에 있고 문 너머 침대는 별도 공간에 놓인다.
- English: A dressing table with its mirror stands beside a doorway, with a bed in the separate space beyond.
- 소유자: {"table": "dressing table", "mirror": "table mirror", "door": "doorway", "bed": "bed beyond doorway"}
- 관계: mirror → on → table; table → beside → door; bed → visible_through → door
- 혼동: 부두아르를 항상 침실·성행위 방으로 고정
- 주장 한계: 부두아르·침실을 연결한 저술안이다. 혼인·성별·역사적 용도·누가 살았는지는 별도다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S05 Ellen Ledoux: Was there ever a Female Gothic?](https://www.nature.com/articles/palcomms201742)

### B12 욕실 거울과 세면대의 대응

- 모드/우선순위: still / P1; 제안 역할: reflection_logic, object_structure
- 한글: 세면대 위 거울 안에 같은 수도꼭지의 대응 반사가 보인다.
- English: A bounded mirror above a washbasin contains the corresponding reflection of the same tap.
- 소유자: {"basin": "washbasin", "mirror": "bounded mirror", "tap": "tap", "reflection": "corresponding tap reflection"}
- 관계: tap → part_of → basin; mirror → above → basin; reflection → inside → mirror; reflection → corresponds_to → tap
- 혼동: 다른 수도꼭지 복제·유리 뒤 실제 방
- 주장 한계: 공간·반사 대응만 확인한다. 노출·성적 맥락·신체 흔적·살해는 추가하지 않는다.
- 출처: [S12 Freud Museum: The Uncanny](https://www.freud.org.uk/2019/09/18/the-uncanny/)

### B13 저장 선반과 밀폐 용기

- 모드/우선순위: still / P1; 제안 역할: object_structure, prop_placement
- 한글: 저장실 선반 위 닫힌 식품 용기와 붙은 표식이 각각 구분된다.
- English: Closed food-storage jars and their attached labels remain distinct on shelving in a storage room.
- 소유자: {"room": "storage room", "shelf": "food-storage shelf", "jar": "closed jar", "label": "separate jar label"}
- 관계: shelf → inside → room; jar → on → shelf; label → on → jar
- 혼동: 보관 내용물을 인육·독·장기로 확정
- 주장 한계: 저장·구획의 일반적 제안이다. 내용물·유통기한·식인·범죄를 입증하지 않는다.
- 출처: [S26 National Trust: Country house communication](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### B14 경사진 지붕 아래 다락의 상자

- 모드/우선순위: still / P1; 제안 역할: location, spatial_depth
- 한글: 경사진 지붕 안쪽 아래의 다락 바닥에 닫힌 보관 상자가 놓인다.
- English: A closed storage box rests on an attic floor beneath the sloping underside of the roof.
- 소유자: {"roof": "sloping roof underside", "room": "attic room", "box": "closed storage box", "floor": "attic floor"}
- 관계: roof → above → room; box → on → floor; floor → part_of → room
- 혼동: 상자 속 인물·광기·감금을 자동 발명
- 주장 한계: 위치·기하만 보인다. 방의 역사·버려진 사람·수용 내용은 별도다.
- 출처: [S42 National Trust: Servants rooms](https://www.nationaltrust.org.uk/discover/history/what-were-georgian-and-victorian-servants-rooms-like)

## 시선·감시·기록의 차이

### C01 직접 시선과 거울 속 대상

- 모드/우선순위: still / P0; 제안 역할: reflection_logic, gaze_target
- 한글: 성인 관찰자가 경계가 분명한 거울을 보고, 거울 안에 다른 성인과 대응하는 반사가 보인다.
- English: An adult observer looks toward a bounded mirror containing the corresponding reflection of another adult.
- 소유자: {"observer": "adult observer", "mirror": "bounded mirror", "target": "another adult", "reflection": "target reflection"}
- 관계: observer → looks_toward → mirror; reflection → inside → mirror; reflection → corresponds_to → target
- 혼동: 거울 밖 복제 인물, 반사 안의 다른 사람
- 주장 한계: 시선과 반사 대응이다. 몰래 관찰·불륜·관음적 흥분은 다른 주장이다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S12 Freud Museum: The Uncanny](https://www.freud.org.uk/2019/09/18/the-uncanny/)

### C02 열쇠구멍이 한정하는 시야

- 모드/우선순위: still / P0; 제안 역할: viewer_position, composition
- 한글: 물리적 문의 열쇠구멍 안쪽 가장자리가 방의 일부 시야를 둘러싼다.
- English: The inner edge of a physical door keyhole bounds a partial view of the room beyond.
- 소유자: {"door": "door panel", "hole": "physical keyhole", "view": "partial room view", "edge": "hole inner edge"}
- 관계: hole → within → door; view → visible_through → hole; edge → bounds → view
- 혼동: 의복 키홀, 장식 비네트, 구멍 안에 문 전체
- 주장 한계: 시점의 저술안이다. 실제 사생활 침해·행위자의 성적 의도는 확정하지 않는다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo)

### C03 기록 화면과 같은 출입문

- 모드/우선순위: still / P0; 제안 역할: apparatus_pov, reflection_logic
- 한글: 모니터 화면에 실제 출입문의 구별 가능한 표식이 같은 배치로 보인다.
- English: A monitor image depicts the same physical doorway with its distinguishing marker in the same arrangement.
- 소유자: {"monitor": "monitor", "screen": "bounded screen image", "door": "physical door", "mark": "door marker"}
- 관계: screen → inside → monitor; screen → depicts → door; mark → on → door
- 혼동: TV 속 다른 방, 화면을 창으로 오인
- 주장 한계: 화면 대응만 확인한다. 실시간·녹화·접근 권한·비밀 감시는 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### C04 가려진 목격과 보이는 단편

- 모드/우선순위: still / P0; 제안 역할: composition, narrative_clue
- 한글: 성인 목격자가 가리개 너머 사건의 단편을 보고 그 범위에 검은 장갑 낀 손이 보인다.
- English: An adult witness faces an event fragment beyond a partial screen, with a black-gloved hand within the visible fragment.
- 소유자: {"witness": "adult witness", "screen": "partial screen", "fragment": "visible event fragment", "hand": "black-gloved hand"}
- 관계: screen → occludes → fragment; witness → faces → fragment; hand → within → fragment
- 혼동: 장갑만 보고 살인자 확정, 보이지 않는 행위를 발명
- 주장 한계: 단편만 채점한다. 완전 사건·가해자·기억 오류·장르 확정은 하지 않는다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S07 BFI: 10 great neo-giallo films](https://www.bfi.org.uk/lists/10-great-neo-giallo-films)

### C05 가족사진의 실제 빈자리와 찢김

- 모드/우선순위: proxy / P1; 제안 역할: narrative_clue, prop_state
- 한글: 액자 속 사진 종이 일부가 찢겨 빠져 있고 종이의 실제 절단 가장자리가 보인다.
- English: A bounded area of a framed photograph is missing, with the torn paper edge visibly surrounding the gap.
- 소유자: {"photo": "single family photograph", "tear": "bounded tear", "frame": "photo frame", "gap": "missing paper area"}
- 관계: photo → inside → frame; tear → within → photo; gap → bounded_by → tear
- 혼동: 얼굴을 가린 반사, 종이 대신 실제 인체 누락
- 주장 한계: 종이 손상이다. 친족·학살·누가 지웠는지·부재자의 사망은 별도다.
- 출처: [S05 Ellen Ledoux: Was there ever a Female Gothic?](https://www.nature.com/articles/palcomms201742)

### C06 서로 다른 기명 표식의 두 소품

- 모드/우선순위: proxy / P1; 제안 역할: narrative_clue, visible_text
- 한글: 나란한 개인 소품 두 개에 서로 다른 이름 표식이 붙어 있다.
- English: Two adjacent personal objects carry visibly different name labels.
- 소유자: {"case": "personal case", "tag1": "first name label", "object": "separate personal object", "tag2": "second name label"}
- 관계: tag1 → attached_to → case; tag2 → attached_to → object; object → beside → case
- 혼동: 판독 불가 문자를 다른 이름이라고 채점
- 주장 한계: 표시 내용만 확인한다. 불륜·이중생활·사람의 신원·소유 관계는 별도다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender)

### C07 고용인의 시선과 열려 있는 틈

- 모드/우선순위: proxy / P1; 제안 역할: gaze_target, space_condition
- 한글: 쟁반을 든 성인이 열린 문틈 쪽을 향하고 그 틈 너머로 방 일부가 보인다.
- English: An adult holding a serving tray faces an open door gap that reveals part of a room.
- 소유자: {"worker": "adult carrying tray", "tray": "serving tray", "gap": "open door gap", "room": "room beyond"}
- 관계: worker → holds → tray; worker → faces → gap; gap → reveals → room
- 혼동: 옷만으로 고용인·증언·충성도 확정
- 주장 한계: 행동과 시선의 선택안이다. 실제 목격 내용·기억·증언의 신빙성·공모는 별도다.
- 출처: [S26 National Trust: Country house communication](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages), [S42 National Trust: Servants rooms](https://www.nationaltrust.org.uk/discover/history/what-were-georgian-and-victorian-servants-rooms-like)

### C08 지워진 선과 남은 계보 표식

- 모드/우선순위: proxy / P1; 제안 역할: visible_text, narrative_clue
- 한글: 탁자 위 허구 관계도에 연결선을 지운 흔적과 남은 이름 표식이 함께 보인다.
- English: A fictional chart on a table shows an erased connecting line beside remaining name labels.
- 소유자: {"chart": "fictional chart", "line": "erased connecting line", "label": "remaining labels", "table": "table"}
- 관계: line → within → chart; label → within → chart; chart → on → table
- 혼동: 단순 장식 선, 실제 혈연 검사 결과로 취급
- 주장 한계: 그림의 표기와 손상이다. 혈통·친자·근친 성관계·상속 진위는 입증하지 않는다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### C09 여닫은 서랍과 빈 윤곽 자리

- 모드/우선순위: proxy / P1; 제안 역할: prop_state, narrative_clue
- 한글: 열린 서랍의 안감에 물건 모양의 빈 홈이 있고 성인의 손이 서랍에 닿아 있다.
- English: An open drawer contains an empty object-shaped recess in its lining, with an adult hand touching the drawer.
- 소유자: {"drawer": "open drawer", "lining": "shaped lining", "recess": "empty object-shaped recess", "hand": "adult hand"}
- 관계: lining → inside → drawer; recess → within → lining; hand → touches → drawer
- 혼동: 물건이 가려진 것을 부재로 채점
- 주장 한계: 빈 홈의 현재 상태다. 도난·누가 가져갔는지·원래 소유자·범죄 이력은 별도다.
- 출처: [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### C10 기록판과 조작 손의 분리

- 모드/우선순위: proxy / P1; 제안 역할: contact_point, prop_placement
- 한글: 성인의 손에 들린 연필 끝이 종이 기록의 현재 보이는 기입란에 닿아 있다.
- English: A pencil held by an adult hand touches a visible entry on a paper record.
- 소유자: {"record": "paper record", "hand": "adult hand", "pencil": "pencil", "entry": "current visible entry"}
- 관계: hand → holds → pencil; pencil → touches → entry; entry → within → record
- 혼동: 작성 행위 자체를 위조·가스라이팅으로 판정
- 주장 한계: 접촉·기입 위치다. 수정의 전후·기만·다른 사람의 현실 판단 변화는 별도다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible), [S17 Jennifer Freyd: DARVO](https://www.jjfreyd.com/darvo/)

## 직물·표면·몸의 분리

### D01 새틴 광택이 따르는 동일 천의 주름

- 모드/우선순위: still / P0; 제안 역할: surface_material, material_mechanics
- 한글: 새틴처럼 보이는 한 천 조각의 주름을 따라 연속된 하이라이트 띠가 흐른다.
- English: A continuous highlight band follows a fold in one satin-like cloth panel.
- 소유자: {"panel": "satin-like cloth panel", "fold": "fold in panel", "highlight": "continuous highlight band"}
- 관계: fold → part_of → panel; highlight → follows → fold
- 혼동: 플라스틱 피부, 실크 원료 확정
- 주장 한계: 보이는 직조 유사 반응이다. 섬유 성분·촉감·페티시 의미는 별도다.
- 출처: [S23 Met: Robe a la francaise, 1999.41a,b](https://www.metmuseum.org/art/collection/search/82495), [S24 Met: Rescuing the Goddess textile conservation](https://www.metmuseum.org/perspectives/tibetan-thangka-textile-conservation)

### D02 다마스크의 평평한 무늬 반전

- 모드/우선순위: still / P0; 제안 역할: surface_pattern, surface_material
- 한글: 연속된 천 위의 평평한 무늬와 바탕이 반사 차이로 나뉘고 같은 주름이 무늬를 가로지른다.
- English: A flat woven-looking motif and its ground differ in reflection on continuous cloth, with the same fold crossing the motif.
- 소유자: {"cloth": "continuous cloth", "motif": "flat woven-looking motif", "ground": "contrasting ground", "fold": "cloth fold"}
- 관계: motif → within → cloth; ground → within → cloth; fold → crosses → motif
- 혼동: 튀어나온 자수·인쇄로만 표현
- 주장 한계: 광택·평면·연속성을 본다. 현미경 없이 실제 직조·재료·연대를 보증하지 않는다.
- 출처: [S23 Met: Robe a la francaise, 1999.41a,b](https://www.metmuseum.org/art/collection/search/82495)

### D03 브로케이드의 바탕과 장식 실

- 모드/우선순위: still / P1; 제안 역할: surface_pattern, material_form
- 한글: 바탕 천 위로 약간 도드라진 직조형 무늬가 있고 그 무늬 안에 금속처럼 반사하는 장식 실이 이어진다.
- English: A slightly raised woven-looking motif sits on a base textile, with metallic-looking ornamental threads running through it.
- 소유자: {"cloth": "base textile", "motif": "raised woven-looking motif", "thread": "metallic-looking ornamental thread"}
- 관계: motif → on → cloth; thread → within → motif
- 혼동: 다마스크 전체를 금실 자수로 오인
- 주장 한계: 외관의 제안이다. 모든 브로케이드가 금속사·돌출 무늬인 것은 아니며 성분은 별도다.
- 출처: [S24 Met: Rescuing the Goddess textile conservation](https://www.metmuseum.org/perspectives/tibetan-thangka-textile-conservation)

### D04 레이스 구멍과 뒤의 피부 구분

- 모드/우선순위: still / P1; 제안 역할: garment_detail, wardrobe_layering
- 한글: 레이스 패널의 구멍 사이로 착용자의 피부가 보이고 패널 가장자리가 연속해 이어진다.
- English: The wearer's skin is visible through bounded openings in a lace panel with a continuous outer edge.
- 소유자: {"lace": "lace panel", "opening": "bounded lace opening", "skin": "wearer skin", "edge": "panel border"}
- 관계: opening → within → lace; skin → visible_through → opening; edge → bounds → lace
- 혼동: 구멍을 상처로, 레이스를 문신으로 오인
- 주장 한계: 피부와 별도 천의 경계다. 노출 욕망·성적 동의·장례/혼례 역할은 별도다.
- 출처: [S23 Met: Robe a la francaise, 1999.41a,b](https://www.metmuseum.org/art/collection/search/82495), [S41 V&A: Art Nouveau and the erotic](https://www.vam.ac.uk/articles/art-nouveau-and-the-erotic/)

### D05 금속사와 피부 표면의 분리

- 모드/우선순위: still / P1; 제안 역할: contact_point, wearable_accessory
- 한글: 성인 착용자의 손목 피부와 브로케이드 소매의 가장자리가 구분되고 장식 실은 천 안에 남는다.
- English: An adult wearer's wrist skin is distinct from the edge of a brocade sleeve, with ornamental threads remaining inside the textile.
- 소유자: {"adult": "adult wearer", "sleeve": "brocade sleeve", "wrist": "wrist skin", "thread": "ornamental thread"}
- 관계: sleeve → on → adult; wrist → belongs_to → adult; thread → within → sleeve
- 혼동: 실이 피부에 관통, 장식이 생체 구조로 융합
- 주장 한계: 의복·신체의 분리만 확인한다. 페티시·결박·상해는 자동 추가하지 않는다.
- 출처: [S24 Met: Rescuing the Goddess textile conservation](https://www.metmuseum.org/perspectives/tibetan-thangka-textile-conservation), [S41 V&A: Art Nouveau and the erotic](https://www.vam.ac.uk/articles/art-nouveau-and-the-erotic/)

### D06 손상된 천과 온전한 아래 표면

- 모드/우선순위: still / P0; 제안 역할: garment_state, anatomical_connection
- 한글: 의복의 찢어진 천 가장자리에 섬유가 풀려 있고 아래에는 연속된 피부가 보인다.
- English: Frayed fibers border a tear in a garment, with continuous skin visible underneath.
- 소유자: {"garment": "garment", "tear": "torn textile region", "fibers": "frayed edge", "skin": "continuous underlying skin"}
- 관계: tear → within → garment; fibers → border → tear; skin → visible_through → tear
- 혼동: 천 찢김을 박피·상처로 채점
- 주장 한계: 천 손상과 인체 상태를 분리한다. 숨은 상처·폭행 경위는 추가하지 않는다.
- 출처: [S27 Met: Renaissance Velvet Textiles](https://www.metmuseum.org/essays/renaissance-velvet-textiles), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### D07 장갑 낀 손이 별도 장갑을 만짐

- 모드/우선순위: proxy / P1; 제안 역할: hand_pose, contact_point
- 한글: 장갑 낀 성인의 손이 탁자 위 빈 장갑에 닿고 빈 손목 구멍이 보인다.
- English: A gloved adult hand touches a separate empty glove on a table, with its open cuff visible.
- 소유자: {"hand": "gloved adult hand", "glove": "separate empty glove", "table": "table", "opening": "empty glove cuff"}
- 관계: hand → touches → glove; glove → on → table; opening → part_of → glove
- 혼동: 떨어진 실제 손, 장갑 두 개가 한 신체로 연결
- 주장 한계: 물건의 접촉이다. 성적 집착·사망·절단·특정 장르를 확정하지 않는다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S41 V&A: Art Nouveau and the erotic](https://www.vam.ac.uk/articles/art-nouveau-and-the-erotic/)

### D08 향수병과 분무의 실제 방향

- 모드/우선순위: proxy / P1; 제안 역할: sensory_cue, physical_motion
- 한글: 성인의 손이 향수병을 들고 노즐에서 가는 분무가 뻗어 나온다.
- English: An adult hand holds a perfume bottle with a fine visible spray extending from its nozzle.
- 소유자: {"bottle": "perfume bottle", "nozzle": "nozzle", "mist": "visible fine spray", "hand": "adult hand"}
- 관계: nozzle → part_of → bottle; mist → extends_from → nozzle; hand → holds → bottle
- 혼동: 향·기억·시체 은폐를 눈에 보인다고 채점
- 주장 한계: 분무의 방향·입자는 보인다. 냄새·성분·회상·무언가를 가린다는 목적은 별도다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S41 V&A: Art Nouveau and the erotic](https://www.vam.ac.uk/articles/art-nouveau-and-the-erotic/)

### D09 도자기 인형의 관절과 유약

- 모드/우선순위: still / P1; 제안 역할: object_structure, surface_material
- 한글: 진열 받침 위 인형에 제작된 관절과 도자기처럼 광택 나는 표면이 보인다.
- English: A doll on a display stand has a manufactured joint and a porcelain-like glazed surface.
- 소유자: {"doll": "porcelain-like doll", "joint": "manufactured joint", "glaze": "glazed surface", "stand": "display stand"}
- 관계: joint → part_of → doll; glaze → covers → doll; doll → on → stand
- 혼동: 실제 사람 피부 균열·마비·대상화로 진단
- 주장 한계: 제작물의 형태다. 소재 성분·살아 있음·배우자 정체·폭력은 별도다.
- 출처: [S12 Freud Museum: The Uncanny](https://www.freud.org.uk/2019/09/18/the-uncanny/), [S35 Met: Michael Henry Spang Ecorche](https://www.metmuseum.org/art/collection/search/195365)

### D10 첨두 창과 유리 조각의 구조

- 모드/우선순위: still / P1; 제안 역할: object_structure, light_shape
- 한글: 벽 속 첨두형 창에 색유리 조각이 구분되고 그 사이 납선처럼 보이는 띠가 이어진다.
- English: A pointed window within a wall contains distinct colored panes separated by leading-like strips.
- 소유자: {"window": "pointed window", "glass": "separate colored panes", "lead": "leading strips", "wall": "wall"}
- 관계: glass → inside → window; lead → between → glass; window → within → wall
- 혼동: 네온 그림을 실제 창으로, 고딕 원형과 부흥 연대 혼동
- 주장 한계: 형태만 검토한다. 교파·시대·가문 정통성·초자연은 별도다.
- 출처: [S28 V&A: Stained glass, Gothic Revival and beyond](https://www.vam.ac.uk/articles/stained-glass-gothic-revival-and-beyond/)

## 만찬·의례·노출 강도

### E01 주인의 위치와 비어 있는 자리

- 모드/우선순위: proxy / P1; 제안 역할: composition, participant_role
- 한글: 식탁 끝 의자와 옆의 빈 의자가 서로 떨어져 있고 각 자리의 식기가 보인다.
- English: A head chair and a separate empty side chair stand at a dining table with visible place settings.
- 소유자: {"table": "dining table", "head": "head chair", "empty": "empty side chair", "settings": "place settings"}
- 관계: head → at_end_of → table; empty → beside → table; settings → on → table
- 혼동: 빈자리만으로 추방·살해·상속인 확정
- 주장 한계: 좌석·식기의 배치다. 가족관계·배제의 의도·누가 권력자인지는 별도다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S15 Mikhail Bakhtin: Rabelais and His World, new translation](https://mitpress.mit.edu/9780262553131/rabelais-and-his-world/)

### E02 접시 건너편에서 멈춘 손

- 모드/우선순위: proxy / P1; 제안 역할: relational_action, contact_point
- 한글: 공용 접시 위로 뻗은 성인의 손과 맞은편 성인의 손이 접시 테두리를 사이에 두고 보인다.
- English: An adult hand reaching above a shared dish faces another adult hand across its rim.
- 소유자: {"dish": "shared dish", "hand1": "reaching adult hand", "hand2": "other adult hand", "rim": "dish rim"}
- 관계: hand1 → above → dish; hand2 → across_from → hand1; rim → part_of → dish
- 혼동: 같은 손의 복제, 음식 통제·동의 확정
- 주장 한계: 손·접시의 거리다. 금식 강요·위계·욕망·공모는 맥락이다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible)

### E03 찢긴 냅킨과 분리된 붉은 액체

- 모드/우선순위: still / P1; 제안 역할: aftermath_trace, prop_state
- 한글: 탁자 위 냅킨이 찢겨 있고 옆에는 냅킨과 구분되는 붉은 액체가 고여 있다.
- English: A torn cloth napkin lies on a table beside a distinct pool of red liquid.
- 소유자: {"napkin": "cloth napkin", "tear": "napkin tear", "liquid": "red liquid", "table": "table"}
- 관계: tear → within → napkin; napkin → on → table; liquid → beside → napkin
- 혼동: 피부 손상·피·고어를 색만으로 확정
- 주장 한계: 천 손상과 액체 외관이다. 실제 혈액·싸움·사망·인과는 별도다.
- 출처: [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### E04 가려진 접시와 옆의 메뉴

- 모드/우선순위: proxy / P1; 제안 역할: prop_placement, narrative_clue
- 한글: 덮개가 접시 내용을 가리고 메뉴 카드가 덮개 옆에 놓여 있다.
- English: A closed cloche hides a plate's contents, with a menu card beside it on the table.
- 소유자: {"cloche": "closed cloche", "plate": "covered plate", "card": "menu card", "table": "table"}
- 관계: cloche → covers → plate; card → beside → cloche; plate → on → table
- 혼동: 보이지 않는 인육·독·원재료 발명
- 주장 한계: 가림은 내용물의 미확정 상태다. 식인·독살·금기 음식을 채점하지 않는다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### E05 과일의 껍질과 드러난 연한 부분

- 모드/우선순위: still / P1; 제안 역할: prop_state, texture
- 한글: 접시 위 과일의 갈라진 껍질 사이로 무르게 보이는 과육이 드러난다.
- English: Soft-looking fruit flesh is visible through a split in the skin of fruit on a plate.
- 소유자: {"fruit": "overripe-looking fruit", "skin": "split fruit skin", "flesh": "exposed soft-looking fruit flesh", "plate": "plate"}
- 관계: skin → part_of → fruit; flesh → visible_through → skin; fruit → on → plate
- 혼동: 실제 인체 살·장기로 변환
- 주장 한계: 과일 외관만 확인한다. 안전성·부패 미생물·인체 괴사를 진단하지 않는다.
- 출처: [S29 National Gallery: Treck, Vanitas Still Life](https://www.nationalgallery.org.uk/paintings/jan-jansz-treck-vanitas-still-life)

### E06 식탁보 아래 보이는 신체 흔적의 경계

- 모드/우선순위: proxy / P1; 제안 역할: aftermath_trace, composition
- 한글: 식탁보가 내려온 가장자리 아래 바닥에 선언된 허구의 상해 흔적 일부가 보인다.
- English: Part of a declared fictional injury trace is visible on the floor below the hanging edge of a tablecloth.
- 소유자: {"table": "table", "cloth": "tablecloth", "trace": "declared fictional injury trace", "floor": "floor"}
- 관계: cloth → hangs_from → table; trace → visible_below → cloth; trace → on → floor
- 혼동: 천의 얼룩과 신체 흔적 혼합, 가려진 부분을 완성
- 주장 한계: 드러난 범위만 검토한다. 부분 단서가 완전한 스플래터 관계나 전체 사건을 충족하지 않는다.
- 출처: [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### E07 의례상과 가정 식탁의 분리

- 모드/우선순위: proxy / P1; 제안 역할: space_condition, prop_placement
- 한글: 닫힌 의례 용기를 둔 상과 식탁 사이에 구획용 가리개가 서 있다.
- English: A partition separates a table holding a closed ceremonial vessel from a dining table.
- 소유자: {"ritual": "ritual display table", "meal": "dining table", "partition": "partition", "vessel": "closed ceremonial vessel"}
- 관계: partition → between → ritual; partition → between → meal; vessel → on → ritual
- 혼동: 용기를 인체·제물·식인 재료로 확정
- 주장 한계: 구획과 기물이다. 희생·살해·종교·신성모독은 별도 문맥이다.
- 출처: [S15 Mikhail Bakhtin: Rabelais and His World, new translation](https://mitpress.mit.edu/9780262553131/rabelais-and-his-world/), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### E08 관객과 무대 위의 분장 흔적

- 모드/우선순위: still / P1; 제안 역할: capture_context, composition
- 한글: 무대 위 성인 연기자에게 상해 분장이 보이고 무대 경계 밖 관객석 일부가 보인다.
- English: An adult performer on a theatrical stage wears visible injury prosthetics, with part of the audience outside the stage boundary.
- 소유자: {"stage": "theatrical stage", "actor": "adult stage performer", "prosthetic": "visible injury prosthetic", "audience": "audience edge"}
- 관계: actor → on → stage; prosthetic → on → actor; audience → outside → stage
- 혼동: 무대 피를 실제 범죄로, 공연 맥락 없는 실제 상해와 혼합
- 주장 한계: 공연과 분장으로 명시된 실현안이다. 모든 스플래터를 분장으로 대체하는 규칙은 아니다.
- 출처: [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1)

## 신체 결과·경계·현재 단계

### F01 분리 신체의 실제 끝점과 간격

- 모드/우선순위: still / P0; 제안 역할: anatomical_connection, body_form
- 한글: 선언된 허구 인체와 대응하는 분리 신체 부분의 양쪽 끝점 및 사이 간격이 보인다.
- English: Both endpoints and the intervening gap are visible between a declared fictional anatomical body and its matching separated part.
- 소유자: {"body": "declared fictional anatomical body", "part": "matching separated body part", "end1": "visible body endpoint", "end2": "visible part endpoint"}
- 관계: end1 → part_of → body; end2 → part_of → part; part → separate_from → body
- 혼동: 가림·크롭·의수 분해를 실제 신체 분리로 채점
- 주장 한계: 분리 결과의 형태를 보존한다. 절단 방법·가해자·행위 시간·죽음은 별도다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F02 들린 피부층과 같은 몸의 아래 표면

- 모드/우선순위: still / P1; 제안 역할: anatomical_connection, body_region
- 한글: 선언된 허구 신체의 들린 피부층과 그 아래 표면이 같은 몸의 이어진 경계에서 보인다.
- English: A lifted skin layer and underlying surface remain linked at a visible boundary on the same declared fictional body.
- 소유자: {"body": "declared fictional anatomical carrier", "layer": "lifted skin layer", "under": "underlying body surface", "edge": "connected layer edge"}
- 관계: layer → part_of → body; edge → joins → layer; edge → joins → under
- 혼동: 옷·밀랍 덮개를 피부층으로 오인
- 주장 한계: 피부층의 결과 구조다. 박피 과정·목적·고통·생사를 추정하지 않는다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F03 빈 공동과 분리된 대응 내부 구조

- 모드/우선순위: still / P0; 제안 역할: anatomical_connection, object_structure
- 한글: 허구 신체의 열린 공동과 밖에 놓인 선언된 내부 구조가 분리된 경계로 보인다.
- English: A visible cavity in a fictional anatomical carrier is separated from a declared internal structure outside it.
- 소유자: {"body": "declared fictional anatomical carrier", "cavity": "visible body cavity", "structure": "declared removed internal structure", "gap": "visible separation"}
- 관계: cavity → within → body; structure → outside → cavity; gap → between → structure; gap → between → body
- 혼동: 탈장·연결된 돌출을 적출로 채점, 음식과 장기 혼동
- 주장 한계: 내부/외부 및 연결 상태다. 시술·폭력 방법·원인·생명 상태는 별도다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F04 닫힌 몸과 바깥 기관의 연속 연결

- 모드/우선순위: still / P1; 제안 역할: anatomical_connection, body_form
- 한글: 허구 신체의 한정된 구멍에서 바깥 기관 형태까지 연속된 조직 연결부가 보인다.
- English: A continuous tissue bridge joins a fictional body at a bounded opening to an externalized organ form.
- 소유자: {"body": "declared fictional body", "opening": "bounded opening", "organ": "externalized organ form", "bridge": "continuous tissue bridge"}
- 관계: opening → within → body; bridge → connects → body; bridge → connects → organ
- 혼동: 외부에 있다는 이유로 적출·분리와 동일시
- 주장 한계: 연결된 외부화다. F03의 분리 결과와 다른 선택안이며 둘을 동시에 요구하지 않는다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F05 괴사 문맥과 색 변화의 분리

- 모드/우선순위: proxy / P1; 제안 역할: skin_condition, body_marking
- 한글: 선언된 허구의 살아 있는 몸에서 국소 변색 구역과 인접 피부의 경계가 보인다.
- English: A localized altered region and its boundary with adjacent skin are visible on a declared fictional living body.
- 소유자: {"body": "declared fictional living body", "region": "localized altered region", "boundary": "boundary to adjacent skin"}
- 관계: region → part_of → body; boundary → bounds → region
- 혼동: 검은 피부·분장을 괴사로 진단
- 주장 한계: 괴사라는 명시 문맥을 보존하되 픽셀은 외관만 판정한다. 조직 사망·원인·감염은 진단 불가.
- 출처: [S44 MedlinePlus: Necrosis](https://www.medlineplus.gov/ency/article/002266.htm)

### F06 부패한 유기물과 변색 표면

- 모드/우선순위: proxy / P1; 제안 역할: prop_state, surface_material
- 한글: 허구의 유기 잔해가 받침 위에 있고 같은 잔해 표면에 변색과 형태가 무너진 구역이 보인다.
- English: Declared fictional organic remains rest on a support with localized discoloration and a collapsed surface region.
- 소유자: {"remains": "declared fictional organic remains", "patch": "discolored patch", "collapse": "collapsed surface region", "support": "support surface"}
- 관계: patch → within → remains; collapse → within → remains; remains → on → support
- 혼동: 녹슨 금속·과일·살아 있는 사람을 동일 상태로 취급
- 주장 한계: 외형과 선언 문맥을 나눈다. 사망 시간·세균·냄새·사망 원인·모독 의도는 별도다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films), [S44 MedlinePlus: Necrosis](https://www.medlineplus.gov/ency/article/002266.htm)

### F07 생물 부착부와 별도 숙주

- 모드/우선순위: still / P1; 제안 역할: anatomical_connection, species_marker
- 한글: 별개인 허구 생물과 숙주의 접합 경계가 연결된 상태로 보인다.
- English: A distinct fictional organism and host meet at a visible attachment boundary.
- 소유자: {"host": "declared fictional host", "organism": "separate fictional organism", "attachment": "visible attachment boundary"}
- 관계: attachment → joins → organism; attachment → joins → host
- 혼동: 옷 장식·장신구·단순 동행을 기생으로 판정
- 주장 한계: 접합의 실현안이다. 기생의 영양 의존·피해·종·질환·지능은 외형만으로 확정하지 않는다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F08 두 몸이 만나는 연속된 공통 조직

- 모드/우선순위: still / P0; 제안 역할: anatomical_connection, subject_count
- 한글: 구분 가능한 두 허구 몸 사이에 공통 조직이 연속해 이어지고 한 사지의 소유자가 추적된다.
- English: Continuous shared tissue joins two distinguishable fictional bodies, with one limb traceable to its owner.
- 소유자: {"body1": "first fictional body", "body2": "second fictional body", "bridge": "continuous shared tissue", "limb": "traceable limb"}
- 관계: bridge → joins → body1; bridge → joins → body2; limb → belongs_to → body1
- 혼동: 포옹·겹침·이상 손을 융합 통과로 채점
- 주장 한계: 물리적 융합이다. 가족의 enmeshment·동의·감정·동일 인격을 뜻하지 않는다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F09 한 몸의 명시된 변형 경계

- 모드/우선순위: still / P1; 제안 역할: transformation_stage, body_form
- 한글: 하나의 허구 몸에 원래 형태 구역과 바뀐 형태 구역이 연속된 이행부로 이어진다.
- English: Retained and changed anatomical regions belong to one fictional body and meet through a continuous transition.
- 소유자: {"body": "single fictional body", "old": "retained anatomical region", "new": "changed anatomical region", "transition": "continuous transition"}
- 관계: old → part_of → body; new → part_of → body; transition → joins → old; transition → joins → new
- 혼동: 두 인물을 합침, 전후 이미지를 동시에 한 몸으로 착각
- 주장 한계: 현재 단계의 형상이다. 실제 변화의 전후·속도·원인·자발성은 시퀀스가 필요하다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### F10 부착된 분장과 선언된 실제 몸의 차이

- 모드/우선순위: still / P1; 제안 역할: skin_condition, capture_context
- 한글: 성인 연기자의 상해 분장 부품과 실제 피부 사이에 부착 이음선이 보인다.
- English: A visible attachment seam separates an injury prosthetic from an adult performer's skin.
- 소유자: {"performer": "adult performer", "appliance": "prosthetic injury appliance", "seam": "visible appliance seam", "skin": "performer skin"}
- 관계: appliance → attached_to → performer; seam → bounds → appliance; skin → beside → seam
- 혼동: 실제 상해를 전부 가짜라고 분류
- 주장 한계: 분장 부품의 구체적 경계다. 요청의 실제 허구 신체 손상 F01~F04를 대신 충족하지 않는다.
- 출처: [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

## 수집·애도·해부 모형

### G01 모발을 넣은 기명 브로치

- 모드/우선순위: still / P0; 제안 역할: object_structure, wearable_accessory
- 한글: 브로치의 투명 덮개 아래 땋은 모발이 있고 같은 물건에 판독 가능한 기명 추모 문구가 있다.
- English: Plaited hair lies beneath a brooch's transparent cover, with a readable named memorial inscription on the same object.
- 소유자: {"brooch": "brooch", "glass": "crystal cover", "hair": "plaited hair lock", "inscription": "readable memorial inscription"}
- 관계: hair → under → glass; glass → part_of → brooch; inscription → on → brooch
- 혼동: 그림 모발·장식 실, 글을 읽지 않고 애도 확정
- 주장 한계: 물건 표기와 모발 형태다. 기증자·실제 사망·합의·사용자의 감정은 별도다.
- 출처: [S30 Met: Tiffany Brooch, 2000.556](https://www.metmuseum.org/art/collection/search/16805)

### G02 모발 장신구의 비애도 대조

- 모드/우선순위: still / P0; 제안 역할: object_structure, wearable_accessory
- 한글: 열린 로켓 안에 땋은 모발이 있고 경첩과 체인이 물건에 연결돼 있다.
- English: An open locket contains braided hair, with its hinge and chain visibly attached.
- 소유자: {"locket": "open locket", "hair": "braided hair", "hinge": "hinge", "chain": "chain"}
- 관계: hair → inside → locket; hinge → part_of → locket; chain → attached_to → locket
- 혼동: 모발을 보자 사망·네크로필리아 자동 부여
- 주장 한계: 살아 있는 사람의 선물일 수도 있다. 애도·성적 의미·특정 인물의 소유를 확정하지 않는다.
- 출처: [S30 Met: Tiffany Brooch, 2000.556](https://www.metmuseum.org/art/collection/search/16805)

### G03 그려진 눈 미니어처

- 모드/우선순위: still / P1; 제안 역할: object_structure, image_detail
- 한글: 장신구 틀 안의 평평한 회화면에 눈 하나가 그려져 있다.
- English: A single eye is painted on a flat miniature surface inside a jeweled setting.
- 소유자: {"jewel": "jewel setting", "miniature": "painted eye miniature", "surface": "flat painted support", "frame": "decorative rim"}
- 관계: miniature → on → surface; surface → inside → jewel; frame → bounds → miniature
- 혼동: 실제 적출 눈·카메라 렌즈
- 주장 한계: 회화와 세팅의 관계다. 눈의 주인·실제 감시·성적 시선은 별도다.
- 출처: [S31 Met: Eye brooch](https://www.metmuseum.org/art/collection/search/825835)

### G04 분류 칸이 나뉜 진기품 캐비닛

- 모드/우선순위: still / P0; 제안 역할: object_structure, prop_placement
- 한글: 진열장의 서로 다른 칸에 자연 조개·공예품·과학 도구가 구분돼 놓인다.
- English: A natural shell, a crafted object and a scientific instrument occupy separate cells of one display cabinet.
- 소유자: {"cabinet": "display cabinet", "shell": "natural shell", "craft": "crafted object", "instrument": "scientific instrument", "cells": "separate cells"}
- 관계: shell → inside → cells; craft → inside → cells; instrument → inside → cells; cells → part_of → cabinet
- 혼동: 잡동사니를 모든 수집 범주의 완전 충족으로 셈
- 주장 한계: 자연/제작/도구의 저술한 병치다. 정본 구성·소유권·식민 수탈·강박은 별도 근거다.
- 출처: [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### G05 열린 서랍과 안의 분류표

- 모드/우선순위: still / P1; 제안 역할: object_structure, visible_text
- 한글: 캐비닛의 열린 서랍 안에서 작은 물건과 그 곁의 분류표가 구분된다.
- English: A small object and a separate classification tag are visible inside an open cabinet drawer.
- 소유자: {"cabinet": "cabinet", "drawer": "open drawer", "tag": "classification tag", "object": "small object"}
- 관계: drawer → part_of → cabinet; tag → inside → drawer; object → beside → tag
- 혼동: 라벨이 실제 재료·사람 신원을 인증
- 주장 한계: 분류하는 행위의 흔적이다. 표기 진위·이전 닫힘·비밀·소유권은 입증하지 않는다.
- 출처: [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### G06 해부학적 비너스의 밀랍 경계

- 모드/우선순위: still / P0; 제안 역할: object_structure, surface_material
- 한글: 목재·유리 진열함 안의 여성형 밀랍 해부 모형에 내부 모형 구조가 보이고 분리 가능한 앞면 패널은 옆에 놓인다.
- English: A female-form wax anatomical model inside a wood-and-glass case shows internal model forms beside its removable anterior panel.
- 소유자: {"model": "female-form wax anatomical model", "panel": "removable anterior panel", "interior": "model internal forms", "case": "wood_and_glass case"}
- 관계: panel → beside → model; interior → within → model; model → inside → case
- 혼동: 실제 피해자·수술 장면·성적 대상화로 자동 전환
- 주장 한계: 교육용 모형의 저술안이다. 모든 Venus의 동일 디자인·제작자·기관 전부를 주장하지 않는다.
- 출처: [S33 UniFI: Cere anatomiche, La Specola](https://www.sma.unifi.it/vp-167-anatomia-umana.html), [S34 Italian cultural heritage: Venere 0900444945](https://catalogo.beniculturali.it/detail/HistoricOrArtisticProperty/0900444945)

### G07 에코르셰 청동상과 받침

- 모드/우선순위: still / P0; 제안 역할: object_structure, surface_material
- 한글: 청동 해부학 조각의 근육 부조와 별도의 대리석처럼 보이는 받침이 보인다.
- English: Modeled muscle relief belongs to a bronze anatomical figure standing on a separate marble-like base.
- 소유자: {"figure": "bronze anatomical figure", "muscles": "modeled muscle relief", "base": "marble-like base"}
- 관계: muscles → part_of → figure; figure → on → base
- 혼동: 실제 박피된 인물, 과학 도면을 살아 있는 몸으로 채점
- 주장 한계: 조각 매체를 보존한다. 실제 손상·죽음·특정 역사 작품의 복제품을 뜻하지 않는다.
- 출처: [S35 Met: Michael Henry Spang Ecorche](https://www.metmuseum.org/art/collection/search/195365), [S36 Met: Ecorche - The Backs of Two Seated Figures](https://www.metmuseum.org/art/collection/search/355650)

### G08 피부 장정의 출처 카드와 책

- 모드/우선순위: proxy / P0; 제안 역할: prop_placement, visible_text
- 한글: 책 장정과 별도의 출처 설명 카드가 같은 진열함 안에 보인다.
- English: A book binding and a separate provenance card are visible inside the same display case.
- 소유자: {"book": "bound book", "card": "explicit provenance card", "case": "display case", "binding": "book binding"}
- 관계: binding → part_of → book; book → inside → case; card → beside → book
- 혼동: 가죽 질감만으로 인간 피부·희생자 신원 확정
- 주장 한계: 표기/외형과 인간 유래의 실제 검사를 분리한다. 이 초안은 인피라는 재료를 시각적으로 인증하지 않는다.
- 출처: [S37 Harvard Library: Human-skin binding FAQ](https://ask.library.harvard.edu/faq/82429)

### G09 시체상 무덤의 조각·수의·기단

- 모드/우선순위: still / P0; 제안 역할: object_structure, prop_placement
- 한글: 돌 기단 위의 시체상 조각에 수의 형태와 연속된 석재 표면이 보인다.
- English: A carved cadaver effigy on a stone plinth has a carved shroud and a continuous stone surface.
- 소유자: {"effigy": "carved cadaver effigy", "shroud": "carved shroud", "plinth": "stone plinth", "surface": "stone surface"}
- 관계: shroud → part_of → effigy; surface → covers → effigy; effigy → on → plinth
- 혼동: 진짜 시신·모든 무덤에 이중상 강제
- 주장 한계: 원 대화의 용어를 소장기관·연구로 보완한 제안이다. 실제 매장자·사망·죄책감은 별도다.
- 출처: [S38 V&A Conservation Journal45: English Cadaver Tomb](https://www.vam.ac.uk/__data/assets/pdf_file/0005/177215/17132_file.pdf), [S39 Michael Rimmer: Silver and Guilt](https://www.tandfonline.com/doi/abs/10.1080/00681288.2019.1642013)

### G10 바니타스의 사치품과 시간 도상

- 모드/우선순위: proxy / P0; 제안 역할: composition, prop_placement
- 한글: 장신구·모래시계·해골 형태가 같은 정물 받침 위에서 서로 구분된다.
- English: An ornamental jewel, an hourglass and a skull form remain distinct on the same still-life surface.
- 소유자: {"jewel": "ornamental jewel", "hourglass": "hourglass", "skull": "skull form", "surface": "shared surface"}
- 관계: jewel → on → surface; hourglass → on → surface; skull → on → surface
- 혼동: 해골 하나=바니타스 전체, 보석과 뼈 융합
- 주장 한계: 도상 병치의 선택안이다. 실제 죽음·시간 경과·관객의 허무감은 입증하지 않는다.
- 출처: [S29 National Gallery: Treck, Vanitas Still Life](https://www.nationalgallery.org.uk/paintings/jan-jansz-treck-vanitas-still-life)

### G11 메멘토 모리의 단독 유품

- 모드/우선순위: proxy / P1; 제안 역할: prop_state, prop_placement
- 한글: 열린 유품함 안에 기념 물건 하나와 별도의 추모 표식이 놓여 있다.
- English: A single memorial object and a separate memorial label rest inside an open keepsake box.
- 소유자: {"object": "single memorial object", "box": "open keepsake box", "label": "separate memorial label"}
- 관계: object → inside → box; label → beside → object
- 혼동: 바니타스에 필요한 모든 사물 자동 추가
- 주장 한계: 물건·표기만 검토한다. 사망·정체·원인·집착·성적 욕망은 별도다.
- 출처: [S29 National Gallery: Treck, Vanitas Still Life](https://www.nationalgallery.org.uk/paintings/jan-jansz-treck-vanitas-still-life), [S30 Met: Tiffany Brooch, 2000.556](https://www.metmuseum.org/art/collection/search/16805)

### G12 가문 초상화와 현 인물의 거리

- 모드/우선순위: proxy / P1; 제안 역할: composition, scale_relation
- 한글: 벽의 초상화 액자 아래에 현재의 성인이 떨어져 서 있다.
- English: A present adult stands apart below a framed portrait on the wall.
- 소유자: {"portrait": "framed portrait", "adult": "current adult", "frame": "portrait frame", "wall": "wall"}
- 관계: portrait → inside → frame; frame → on → wall; adult → below → portrait
- 혼동: 닮음만으로 혈연·전 배우자·환생 확정
- 주장 한계: 배치와 그림의 인물만 보인다. 가문 정통성·관계·공포·유산은 문맥이다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S05 Ellen Ledoux: Was there ever a Female Gothic?](https://www.nature.com/articles/palcomms201742)

### G13 빈 진열대와 살아 있는 인물의 분리

- 모드/우선순위: proxy / P1; 제안 역할: composition, space_condition
- 한글: 빈 진열대가 있는 유리함 밖에 성인이 서 있고 함의 경계가 인물과 구분된다.
- English: An adult stands outside a glass case containing an empty display stand, with the case boundary distinct from the person.
- 소유자: {"stand": "empty display stand", "glass": "glass case", "adult": "adult outside", "boundary": "case boundary"}
- 관계: stand → inside → glass; adult → outside → glass; boundary → bounds → glass
- 혼동: 성인을 전시된 물건·시신으로 자동 취급
- 주장 한계: 거리와 경계다. 인격의 소유·수집 계획·강제·성적 대상화는 외형으로 확정하지 않는다.
- 출처: [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### G14 가보를 건네는 동일 물건의 접점

- 모드/우선순위: still / P1; 제안 역할: relational_action, contact_point
- 한글: 성인 한 명의 손이 받친 물건 하나를 다른 성인의 손이 같은 접점에서 만진다.
- English: One adult hand supports a single heirloom-like object while another adult hand touches that same object.
- 소유자: {"object": "single heirloom-like object", "hand1": "first adult hand", "hand2": "second adult hand"}
- 관계: hand1 → supports → object; hand2 → touches → object
- 혼동: 두 물건·세 손·공중 부양, 소유권 이전 자동 인증
- 주장 한계: 동일 물건의 접촉만 보인다. 가보라는 이력·증여·상속 법률효력·동의는 별도다.
- 출처: [S30 Met: Tiffany Brooch, 2000.556](https://www.metmuseum.org/art/collection/search/16805), [S32 Met: Collecting for the Kunstkammer](https://www.metmuseum.org/essays/collecting-for-the-kunstkammer)

### G15 성유물함의 용기와 별도 내부

- 모드/우선순위: still / P1; 제안 역할: object_structure, prop_placement
- 한글: 성유물함 형태의 용기에 뒤쪽 출입문이 있고 열린 문을 통해 빈 내부 구획이 보인다.
- English: A reliquary-like container has a rear access door opening toward a visible empty interior compartment.
- 소유자: {"container": "reliquary-like container", "door": "rear access door", "interior": "visible empty compartment"}
- 관계: door → part_of → container; interior → inside → container; door → opens_toward → interior
- 혼동: 용기만 보고 유골·성인 신원·실제 신성 확정
- 주장 한계: 용기/내용물의 구분이다. 성유물함에는 비신체 유물도 있을 수 있고 닫힌 내부는 미확정이다.
- 출처: [S47 Philadelphia Museum: Reliquary Chasse](https://www.philamuseum.org/objects/51954)

## 비평·권력·금기·비가시 주장

### H01 세 장르의 서로 다른 기능

- 모드/우선순위: context / P2; 제안 역할: genre, world
- 한글: 미학·관계 서사·신체 표현·역사적 장르 계보를 독립 축으로 보존한다.
- English: Preserve aesthetic direction, relationship narrative, bodily depiction and historical genre lineage as distinct contextual axes.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 네온·검은 장갑·피·저택이 모든 장르를 대체
- 주장 한계: 장르명은 모든 카드의 하드 활성화가 아니다. 장르 서술 자체도 단일 도상으로 검증되지 않는다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S03 Cambridge: Decadence](https://www.cambridge.org/core/journals/victorian-literature-and-culture/article/decadence/2621A4931E82EFF8948DCCE2DB7A3423), [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1), [S09 BFI: Pleasures and pains of the flesh](https://www.bfi.org.uk/features/pleasures-pain-new-french-extremity), [S10 Miriam Silverberg: Erotic Grotesque Nonsense sample](https://content.ucpress.edu/pages/8868/8868.ch01.pdf), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### H02 퇴폐·권태·질병 관심의 해석

- 모드/우선순위: context / P2; 제안 역할: mood, concept_tension
- 한글: 유미주의·세기말·상징주의·앙뉘·스플린·댄디즘을 서로 구분해 해석한다.
- English: Keep aestheticism, fin de siecle, symbolism, ennui, spleen and dandyism distinct in interpretation.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 나른한 얼굴을 우울증·도착·부도덕으로 진단
- 주장 한계: 개별 용어 전부를 이번에 독립 사전 대조하지 않았다. 역사·내면·감각은 외형에 고정하지 않는다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S03 Cambridge: Decadence](https://www.cambridge.org/core/journals/victorian-literature-and-culture/article/decadence/2621A4931E82EFF8948DCCE2DB7A3423), [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013)

### H03 비체·언캐니·그로테스크의 비평

- 모드/우선순위: context / P2; 제안 역할: concept_tension, offscreen_context
- 한글: 비체·언캐니·마카브르·그로테스크·몸 장르를 비평적 읽기로 보존한다.
- English: Preserve abjection, the uncanny, the macabre, the grotesque and body genres as critical readings.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 피·기괴함 하나로 이론 전체 통과
- 주장 한계: 비평 틀·관객 반응·종교 위반은 단일 픽셀 분류가 아니다. Williams 본문 논증은 미검증.
- 출처: [S11 Julia Kristeva: Powers of Horror](https://cup.columbia.edu/book/powers-of-horror/9780231214575/), [S12 Freud Museum: The Uncanny](https://www.freud.org.uk/2019/09/18/the-uncanny/), [S13 Barbara Creed: The Monstrous-Feminine, second edition](https://www.routledge.com/link/link/p/book/9780367209452), [S14 Linda Williams: Film Bodies: Gender, Genre, and Excess](https://online.ucpress.edu/fq/article-abstract/44/4/2/39822/Film-Bodies-Gender-Genre-and-Excess?redirectedFrom=fulltext), [S15 Mikhail Bakhtin: Rabelais and His World, new translation](https://mitpress.mit.edu/9780262553131/rabelais-and-his-world/)

### H04 강압적 통제의 반복과 영향

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, situation_context
- 한글: 출입·돈·연락 제한의 반복과 상대 자율성에 미치는 영향을 서사 증거로 분리한다.
- English: Keep the repeated restriction of access, money or communication and its effect on autonomy as narrative evidence.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 열쇠 소지·부유함·함께 있음만으로 학대 확정
- 주장 한계: 현재 배치와 지속 행동 패턴은 다른 증거다. 법률적 유죄·진단·피해자 신원을 추정하지 않는다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible), [S19 WHO: Violence against women](https://www.who.int/health-topics/violence-against-women/)

### H05 가스라이팅과 DARVO의 다른 순서

- 모드/우선순위: context / P2; 제안 역할: narrative_core, offscreen_context
- 한글: 현실 판단의 조작과 부인·공격·역할 역전의 대응 순서를 구분한다.
- English: Distinguish manipulation of reality judgment from the deny-attack-role-reversal response sequence.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 반박·부인·어두운 조명 하나를 두 개념으로 채점
- 주장 한계: 발화·전후 증거가 필요하다. DARVO의 사용 자체도 과거 행위의 유죄 증거는 아니다.
- 출처: [S16 Home Office: Controlling or coercive behaviour guidance](https://www.gov.uk/government/publications/controlling-or-coercive-behaviour-statutory-guidance-framework/controlling-or-coercive-behaviour-statutory-guidance-framework-accessible), [S17 Jennifer Freyd: DARVO](https://www.jjfreyd.com/darvo/)

### H06 혈연·상속·결혼·가족의 비밀

- 모드/우선순위: context / P2; 제안 역할: narrative_core, declared_person_background
- 한글: 불륜·혈통·상속·푸른 수염·전 배우자·대물림을 서로 다른 서사 전제로 유지한다.
- English: Keep infidelity, lineage, inheritance, Bluebeard, the absent first spouse and intergenerational repetition as distinct narrative premises.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 가족사진·열쇠·초상화·닮음이 사건 전부를 인증
- 주장 한계: 친족·사망·혼인 효력·의도·반복은 개별 근거가 필요하다. 원전 작품 상세 비교는 후속.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S05 Ellen Ledoux: Was there ever a Female Gothic?](https://www.nature.com/articles/palcomms201742)

### H07 욕망·페티시·관음·임상 명칭

- 모드/우선순위: context / P2; 제안 역할: adult_presentation_context, offscreen_context
- 한글: 욕망의 표현·사물의 성적 의미·사생활 시선·가학/피학이라는 문학적 용법을 구분한다.
- English: Distinguish erotic expression, erotic significance of objects, private-looking viewpoints and literary uses of sadism and masochism.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 실크·장갑·노출·통증만으로 성적 진단
- 주장 한계: 성적 정체성·임상 진단·동의·쾌감은 외형으로 확정할 수 없다. 노화·장애를 공포의 근거로 삼지 않는다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S41 V&A: Art Nouveau and the erotic](https://www.vam.ac.uk/articles/art-nouveau-and-the-erotic/)

### H08 합의된 BDSM과 강압의 구분

- 모드/우선순위: context / P2; 제안 역할: adult_presentation_context, offscreen_context
- 한글: 합의된 권력 교환과 성적 강압·파트너 성폭력을 별개 의미로 보존한다.
- English: Keep consensual power exchange distinct from sexual coercion and intimate-partner sexual violence.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 부부·웃음·계약서·구속 소품만으로 동의나 학대 인증
- 주장 한계: 사전 의사·지속 동의·철회·비동의의 근거가 각각 필요하다. 복식·도구로 대체할 수 없다.
- 출처: [S18 NCSF: Statement on Consent](https://ncsfreedom.org/wp-content/uploads/2019/12/Consent-Counts-Statement.pdf), [S19 WHO: Violence against women](https://www.who.int/health-topics/violence-against-women/)

### H09 재생산 강압과 신체 자율성

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, situation_context
- 한글: 피임·임신·출산 결정권과 그것을 제한하는 강압을 구분해 보존한다.
- English: Retain reproductive decisions and coercive interference with them as separate claims.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 배 크기·후계자 문서·의료 소품으로 강제 확정
- 주장 한계: 생식 상태·강압·인과는 외형으로 진단하지 않는다. 손상·성폭력의 행위 절차를 저술하지 않는다.
- 출처: [S19 WHO: Violence against women](https://www.who.int/health-topics/violence-against-women/), [S20 WHO: Clinical handbook, Part 5](https://www.afro.who.int/sites/default/files/2020-06/Clinical%20Handook%20for%20Women%20Web%20final%20signed_0.pdf)

### H10 근친 금기와 가족 내 성적 학대

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, declared_person_background
- 한글: 근친이라는 친족/성관계 범주와 가족 권력을 이용한 성적 침해를 구분한다.
- English: Keep incest as a kinship-and-sexual-relation category distinct from intrafamilial sexual abuse.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 닮음·가족사진·같은 방을 성행위·피해의 증거로 취급
- 주장 한계: 중립적 연구 의미를 보존한다. 이미지에는 친족·행위·동의·나이를 새로 발명하지 않는다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S19 WHO: Violence against women](https://www.who.int/health-topics/violence-against-women/)

### H11 시체성애와 애도·죽음 도상의 구분

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, adult_presentation_context
- 한글: 시체를 향한 성적 욕망을 애도·마카브르 취향·모형 전시와 구분한다.
- English: Distinguish sexual desire directed toward a corpse from mourning, macabre imagery and anatomical-model display.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 로켓·잠든 사람·시체상 조각을 시체성애로 판정
- 주장 한계: 생사·성적 의도·행위는 별도 근거다. 맥락 기록은 성적 시각 후보나 생성 지시가 아니다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S30 Met: Tiffany Brooch, 2000.556](https://www.metmuseum.org/art/collection/search/16805), [S38 V&A Conservation Journal45: English Cadaver Tomb](https://www.vam.ac.uk/__data/assets/pdf_file/0005/177215/17132_file.pdf)

### H12 식인·자기 식인·성적 식인의 주장

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, narrative_core
- 한글: 식인의 재료·섭식자·대상 종/동일인과 성적 의미를 각각 분리한다.
- English: Separate the material, eater, species or self-relation and erotic interpretation of cannibalism.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 붉은 수프·고기·입맞춤만으로 식인이나 성적 식인 확정
- 주장 한계: 서사에서 명시된 의미는 보존하지만 일반 음식 후보가 그 의미를 충족했다고 채점하지 않는다.
- 출처: [S09 BFI: Pleasures and pains of the flesh](https://www.bfi.org.uk/features/pleasures-pain-new-french-extremity), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### H13 흡혈의 행위와 에로틱 해석

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, adult_presentation_context
- 한글: 혈액 섭취·행위자·대상·접촉과 성적 해석을 별개 주장으로 보존한다.
- English: Preserve blood consumption, actor, target, contact and erotic interpretation as separate claims.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 두 점의 상흔·송곳니·목의 손길만으로 흡혈·쾌감 확정
- 주장 한계: 상흔 외관은 종·도구·인물·성적 의도의 식별 증거가 아니다. NIST 자료는 흡혈귀 정의 출처가 아니다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S45 NIST: CSAFE Bitemark Thinkshop Report](https://nvlpubs.nist.gov/nistpubs/ir/2022/NIST.IR.8352sup1.pdf)

### H14 집단 성적 의례·수간·동물성애

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, adult_presentation_context
- 한글: 집단 의례의 성적 맥락, 동물과의 성행위, 동물을 향한 성적 관심을 구별하는 중립 용어 기록을 둔다.
- English: Keep neutral contextual records distinguishing sexual group ritual, sexual acts involving animals and sexual interest directed toward animals.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 동물·가면·군중·종간 돌봄을 성적 행위로 자동 변환
- 주장 한계: 원 대화의 뜻을 누락하지 않지만 성적 행위의 시각 레시피는 만들지 않는다. S04는 역사적 담론 범위만 지원한다.
- 출처: [S04 Cambridge: The Sexual Psychology of Decadence](https://doi.org/10.1017/9781108550826.013), [S10 Miriam Silverberg: Erotic Grotesque Nonsense sample](https://content.ucpress.edu/pages/8868/8868.ch01.pdf)

### H15 고문·가족 살해·의례적 희생

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, narrative_core
- 한글: 의도적 고통·가족관계와 사망·의례의 목적을 각각 증거가 필요한 사건 범주로 유지한다.
- English: Retain intentional suffering, family relationship and death, and ritual purpose as separately evidenced event claims.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 감금 소품·쓰러진 사람·제단만으로 사건 범주 확정
- 주장 한계: 손상 결과와 행위 방법·사망·가해 의도·관계·종교 목적을 구분한다.
- 출처: [S08 Exeter Press: Grand-Guignol - The French Theatre of Horror](https://www.exeterpress.co.uk/products/grand-guignol-1), [S19 WHO: Violence against women](https://www.who.int/health-topics/violence-against-women/), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

### H16 고어의 정도·의학 상태·감각 반응

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, concept_tension
- 한글: 고어 표현, 물리적 손상·변형, 괴사 진단, visceral 반응을 서로 다른 축으로 기록한다.
- English: Record gore depiction, physical damage or transformation, necrosis diagnosis and visceral response on separate axes.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: visceral은 반드시 내장, 검은 부분은 반드시 괴사
- 주장 한계: 직접 형태를 F 카드로 평가하되 진단·감각·관객 반응은 픽셀 통과로 만들지 않는다.
- 출처: [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films), [S44 MedlinePlus: Necrosis](https://www.medlineplus.gov/ency/article/002266.htm)

### H17 인피 장정의 물질 확인과 출처

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, publication_caption_context
- 한글: 인간 피부라는 재료 주장과 검사·기증자·보관 이력·동의를 별도로 기록한다.
- English: Separate the human-skin material claim from testing, donor identity, custodial history and consent.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 가죽 무늬·책 옆 설명문만으로 인간 유래 인증
- 주장 한계: 2026년 FAQ는 신원과 정확한 경위를 미확정으로 둔다. 재료 검사는 시각 게이트가 아니다.
- 출처: [S37 Harvard Library: Human-skin binding FAQ](https://ask.library.harvard.edu/faq/82429)

### H18 한 장에서 확인 불가한 감각·시간

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, sensory_cue
- 한글: 향·음성·맛·기억·반복·반전·관객 반응은 필요한 다른 매체 증거와 연결한다.
- English: Tie scent, voice, taste, memory, repetition, reversal and audience response to the additional evidence they require.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 분무·입 벌림·흐릿함·사진 한 장으로 감각/시퀀스 확정
- 주장 한계: 정지 상태의 시각적 단서는 유지한다. 관찰 불가를 통과로 바꾸지 않는다.
- 출처: [S01 Julia Crouch: Genre bender](https://juliacrouch.co.uk/blog/genre-bender), [S12 Freud Museum: The Uncanny](https://www.freud.org.uk/2019/09/18/the-uncanny/), [S14 Linda Williams: Film Bodies: Gender, Genre, and Excess](https://online.ucpress.edu/fq/article-abstract/44/4/2/39822/Film-Bodies-Gender-Genre-and-Excess?redirectedFrom=fulltext)

### H19 방의 기능·위치·매장 용도의 구분

- 모드/우선순위: context / P2; 제안 역할: location, offscreen_context
- 한글: 부두아르·침실·살롱·다락·저장 지하실·납골/매장 공간의 기능과 위치를 구분한다.
- English: Distinguish boudoir, bedroom, salon, attic, storage cellar and burial crypt by function and location.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 지하실을 모두 납골당, 화장방을 모두 침실로 치환
- 주장 한계: 가시 기하와 역사적 용도는 별도다. 이 목록의 모든 방 이름을 독립 건축 사전으로 검증한 것은 아니다.
- 출처: [S25 Met: Visitors to Versailles](https://www.metmuseum.org/ko/press-releases/visitors-to-versailles-2018-exhibitions), [S26 National Trust: Country house communication](https://www.nationaltrust.org.uk/discover/history/art-collections/country-house-communication-through-the-ages), [S38 V&A Conservation Journal45: English Cadaver Tomb](https://www.vam.ac.uk/__data/assets/pdf_file/0005/177215/17132_file.pdf), [S42 National Trust: Servants rooms](https://www.nationaltrust.org.uk/discover/history/what-were-georgian-and-victorian-servants-rooms-like)

### H20 서사 정보·시간·불가능 범행

- 모드/우선순위: context / P2; 제안 역할: narrative_core, offscreen_context
- 한글: 화자 신뢰성·초점화·다중 시점·시간 순서·단서 재해석·폐쇄집단/밀실 수수께끼를 구분한다.
- English: Distinguish narrator reliability, focalization, multiple perspectives, temporal ordering, clue reinterpretation and closed-circle or locked-room mystery.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 카메라 POV=화자, 잠긴 방=밀실 미스터리, 흐림=불신 화자
- 주장 한계: 서사 담화·정보 차이·시간·접근 조건의 추가 증거가 필요하다. 열 용어 모두의 독립 사전 대조는 아니다.
- 출처: [S50 Dan Shen: Unreliability](https://www-archiv.fdm.uni-hamburg.de/lhn/node/66.html), [S51 Burkhard Niederhoff: Focalization](https://www-archiv.fdm.uni-hamburg.de/lhn/node/18.html)

### H21 정지 이미지·음향·공감각·시간

- 모드/우선순위: context / P2; 제안 역할: offscreen_context, sensory_cue
- 한글: 활인화의 지속·공감각·폴리·대위법적 음향·화면 밖 소리와 블랙코미디의 효과를 따로 기록한다.
- English: Record tableau duration, synaesthesia, Foley, contrapuntal sound, off-screen sound and black-comedy effect separately.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 열린 입=소리, 분무=향, 정지 포즈=지속, 웃는 얼굴=블랙코미디
- 주장 한계: 오디오/시퀀스/감상 맥락을 픽셀로 인증하지 않는다. BFI 폴리 교육 자료는 대위법 전체의 정의 출처가 아니다.
- 출처: [S02 V&A: The Cult of Beauty](https://www.vam.ac.uk/__data/assets/pdf_file/0005/179519/vanda-cultofbeauty.pdf), [S52 Met: The Dawn of Photography](https://www.metmuseum.org/exhibitions/listings/2003/french-daguerreotypes), [S53 BFI: Moving Images in the Classroom](https://www.screen.scot/binaries/content/assets/screen-scot/film-education/frameworks-and-guides/bfi-education-moving-image-in-the-classroom-1.pdf)

### H22 창작 조합명과 참고 작품의 지위

- 모드/우선순위: context / P2; 제안 역할: genre, offscreen_context
- 한글: 원 대화의 조합 표현 8개는 제안명이며 작품 8개는 서로 다른 접점의 참고작으로 보존한다.
- English: Keep the eight coined combination expressions distinct from the eight reference works and their different points of contact.
- 소유자: {}
- 관계: 문맥 전용; 시각 관계 없음
- 혼동: 제안명을 정식 장르·작품 전체를 모든 조합의 전형으로 승격
- 주장 한계: 시놉시스·초안·비평 열람과 전체 영화/프레임 관찰은 다르다. 정본 디자인·캐릭터·장면을 복제하는 후보가 아니다.
- 출처: [S54 Miramax: The Cook, The Thief, His Wife and Her Lover](https://www.miramax.com/movie/the-cook-the-thief-his-wife-her-lover/), [S55 Clive Barker official: Hellraiser](https://www.clivebarker.info/hellraiser.html), [S56 BFI Sight and Sound: Crimson Peak](https://www.bfi.org.uk/sight-and-sound/reviews/film-week-crimson-peak), [S57 BFI Player: Society](https://player.bfi.org.uk/subscription/film/watch-society-1989-online), [S58 Searchlight Pictures Press: Ready or Not](https://press.searchlightpictures.com/ready-or-not), [S59 BFI Southbank: The Handmaiden](https://bfidatadigipres.github.io/big%20screen%20classics/2022/02/04/handmaiden/), [S60 Busan International Film Festival archive: A Tale of Two Sisters](https://biff.kr/eng/html/archive/arc_history_view.asp?kind=history&m_idx=8053&pyear=2003), [S61 BFI: 10 great erotic horror films](https://www.bfi.org.uk/lists/10-great-erotic-horror-films)

## 명암·재현·구도·기록 매체

### I01 형태를 모델링하는 명암

- 모드/우선순위: still / P1; 제안 역할: light_direction, light_quality
- 한글: 둥근 물체의 밝은 면과 그늘 면 사이에 이어지는 명암 변화가 형태를 드러낸다.
- English: A continuous tonal transition between the lit and shaded sides models the volume of a rounded object.
- 소유자: {"object": "rounded object", "bright": "lit side", "shadow": "shaded side", "transition": "tonal transition"}
- 관계: bright → part_of → object; shadow → part_of → object; transition → between → bright; transition → between → shadow
- 혼동: 명암만 있으면 넓은 암흑이 필수라고 판정
- 주장 한계: 키아로스쿠로의 선택안이다. 공간 전체가 어두워야 한다는 조건은 없다.
- 출처: [S48 National Gallery: Chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro)

### I02 지배적 어둠 안의 손과 얼굴

- 모드/우선순위: still / P1; 제안 역할: exposure, light_shape
- 한글: 대부분 어두운 방 안에서 같은 성인의 얼굴과 손 일부가 선택적으로 밝게 보인다.
- English: Selected parts of the same adult's face and hand are bright within a predominantly dark room.
- 소유자: {"person": "adult person", "face": "lit face", "hand": "lit hand", "room": "predominantly dark room"}
- 관계: face → belongs_to → person; hand → belongs_to → person; person → inside → room
- 혼동: 검은 옷만 있음·손 소유자 불명
- 주장 한계: 선택적 밝음과 어두운 면적의 관계다. 가려진 필수 접촉을 통과로 만들지 않는다.
- 출처: [S49 National Gallery: Tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism)

### I03 활인화의 인물과 재현 이미지

- 모드/우선순위: proxy / P1; 제안 역할: composition, staging_degree
- 한글: 정적인 자세의 성인 집단과 별도 참고 이미지에서 대응하는 인물 배치가 보인다.
- English: A posed adult group and a separate reference image show a corresponding arrangement of figures.
- 소유자: {"people": "posed adult group", "reference": "separate reference image", "arrangement": "matching visible arrangement"}
- 관계: people → reproduce → arrangement; arrangement → depicted_in → reference
- 혼동: 마네킹·실제 시신·일반 가족사진을 모두 활인화로 판정
- 주장 한계: 현재 배치 대응이다. 오래 정지한 시간·역사 작품의 정확한 재현·연기 의도는 별도다.
- 출처: [S52 Met: The Dawn of Photography](https://www.metmuseum.org/exhibitions/listings/2003/french-daguerreotypes)

### I04 내부 프레임과 바깥 프레임

- 모드/우선순위: still / P1; 제안 역할: composition, subject_framing
- 한글: 바깥 이미지 경계 안의 실제 문틀이나 창틀이 성인 인물을 한 번 더 둘러싼다.
- English: A physical doorway or window frame inside the outer image boundary surrounds an adult subject.
- 소유자: {"frame": "physical inner frame", "subject": "adult subject", "image": "outer image boundary"}
- 관계: frame → surrounds → subject; frame → inside → image
- 혼동: 거울 반사·감금·도피 불가를 자동 추가
- 주장 한계: 구도의 경계다. 안 보이는 방·출구·시선의 의미는 발명하지 않는다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S51 Burkhard Niederhoff: Focalization](https://www-archiv.fdm.uni-hamburg.de/lhn/node/18.html)

### I05 편지 원문과 기록 매체의 분리

- 모드/우선순위: proxy / P1; 제안 역할: visible_text, prop_placement
- 한글: 성인의 손에 든 한 편지에 판독 가능한 한 줄이 있고 편지는 필기면 위에 놓인다.
- English: An adult hand holds a single letter bearing one legible line above a writing surface.
- 소유자: {"letter": "single letter", "hand": "adult hand", "line": "legible line", "surface": "writing surface"}
- 관계: line → within → letter; hand → holds → letter; letter → above → surface
- 혼동: 텍스트 존재만으로 서간체 서사 전체·진실 인증
- 주장 한계: 기록의 매체·표기다. 화자·시퀀스·위조·진위는 별도 증거가 필요하다.
- 출처: [S50 Dan Shen: Unreliability](https://www-archiv.fdm.uni-hamburg.de/lhn/node/66.html), [S51 Burkhard Niederhoff: Focalization](https://www-archiv.fdm.uni-hamburg.de/lhn/node/18.html)

### I06 식탁·시선·노출 결과의 초점 위계

- 모드/우선순위: still / P1; 제안 역할: visual_hierarchy, composition
- 한글: 식탁 곁의 선언된 허구 신체 결과를 성인이 바라보고 같은 가시 영역 안에 둘 다 놓인다.
- English: An adult faces a declared fictional bodily result beside a dining table, with both within one shared visible area.
- 소유자: {"table": "dining table", "adult": "adult observer", "result": "declared fictional bodily result", "view": "shared visible area"}
- 관계: adult → faces → result; result → beside → table; view → contains → adult; view → contains → result
- 혼동: 무관한 장식들을 늘림·정작 결과 접점을 가림
- 주장 한계: 미장센/세트피스의 관계 저술안이다. 실제 전체 사건·서사적 절정·관객 반응은 단일 컷으로 인증하지 않는다.
- 출처: [S06 BFI: Where to begin with giallo](https://www.bfi.org.uk/features/where-begin-giallo), [S40 BFI: 10 great body horror films](https://www.bfi.org.uk/lists/10-great-body-horror-films)

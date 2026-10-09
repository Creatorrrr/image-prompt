# 봄 패션 시각 의미 상세 카드

가족 수준 의미 카드와 선택형 후보 초안이다. 각 후보를 실행 데이터로 승격하기 전에 개별 그래프·적용 속성·조건·필수 시각 요소를 확정한다. 한 카드의 모든 대안은 동시에 필수가 아니다. 출처는 원장에 적힌 좁은 주장만 뒷받침하며, 관찰 관계와 검증 설계는 이번 연구의 제안이다.

## SF001 라운드·크루 목선

둥근 윗선의 깊이와 폭은 연속 변수다. 원문의 Round/Crew 병기를 무조건 동의어로 고정하지 않는다.

원문 연결: `SPT01-01` 라운드넥·크루넥 — Round / Crew neck

관찰 구성: `top_A.neckline`, `wearer_A.neck_base`

관계 설계: `top_A.neckline → curves_below → wearer_A.neck_base`

혼동 경계: 크루보다 깊은 라운드도 있다. 이름만으로 쇄골 가림을 확정하지 않는다.

관찰 조건: 직물의 둥근 연속 경계와 목 기준점이 동시에 읽힘

적용 속성 제안: `wardrobe.neckline.contour`, `wardrobe.neckline.depth` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `bundle:mg_round_cap_bundle`, `bundle:mg_round_join_bundle`, `bundle:ri_lucy_plate_eyes`, `profile:appearance_rel_h048`, `profile:ca_back_tubes`

후보 초안:

- `SPR_DRAFT_SF001_01` (SPT01-01): The top has a shallow rounded neckline close to the base of the same wearer's neck.

## SF002 넓은 목선·보트넥

가로 폭과 얕은 중앙 깊이를 분리한다. wide는 폭 설명이고 boat는 외곽 형태다.

원문 연결: `SPT01-02` 와이드넥† — Wide neckline, `SPT01-03` 보트넥·바토넥 — Boat / Bateau neck

관찰 구성: `top_A.neckline`, `wearer_A.clavicle_span`

관계 설계: `top_A.neckline → spans_across → wearer_A.clavicle_span`

혼동 경계: 넓은 V도 wide다. 보트넥을 오프숄더로 바꾸지 않는다.

관찰 조건: 양끝·중앙 깊이·어깨 위 직물의 연속성을 함께 확인

적용 속성 제안: `wardrobe.neckline.width`, `wardrobe.neckline.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:clothing_ct035_v2`, `slot:garment_detail:clt_ct035_v2`, `profile:ghost_ship_former_vessel_breach`, `profile:maritime_safety_coast_guard_role`, `profile:mythic_flood_preservation_vessel`

후보 초안:

- `SPR_DRAFT_SF002_01` (SPT01-02): The top neckline opens widely across the collarbone area.
- `SPR_DRAFT_SF002_02` (SPT01-03): The top has a broad, shallow neckline with an almost horizontal central edge.

## SF003 스쿠프·U 목선

곡선 가장자리의 가로 폭과 세로 깊이를 저장한다. U와 scoop의 유통 경계는 가변이다.

원문 연결: `SPT01-04` 스쿠프넥 — Scoop neck, `SPT01-05` 유넥 — U-neck

관찰 구성: `top_A.neckline`, `wearer_A.upper_chest`

관계 설계: `top_A.neckline → bounds_rounded_opening_over → wearer_A.upper_chest`

혼동 경계: 보이는 경계 없이 가슴 크기나 피부 그림자를 목선 모양으로 대신하지 않는다.

관찰 조건: 목선 전체의 곡률·양쪽 가장자리·바닥이 읽힘

적용 속성 제안: `wardrobe.neckline.contour`, `wardrobe.neckline.depth` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:clothing_ct034_v2`, `profile:sw_scoop`, `slot:garment_detail:clt_ct034_v2`, `slot:garment_detail:sw_candidate_scoop`

후보 초안:

- `SPR_DRAFT_SF003_01` (SPT01-04): A broad rounded neckline dips below the collarbones on the same top.
- `SPR_DRAFT_SF003_02` (SPT01-05): The same top has a vertically extended U-shaped neckline.

## SF004 스퀘어 목선

가로 바닥과 좌우 옆변이 만나는 모서리가 핵심이다. 직각의 정확한 각도는 별도 명세다.

원문 연결: `SPT01-06` 스퀘어넥 — Square neck

관찰 구성: `top_A.neckline_base`, `top_A.neckline_sides`

관계 설계: `top_A.neckline_base → meets_corners_of → top_A.neckline_sides`

혼동 경계: 어깨끈·쇄골 노출·밀착핏을 자동 추가하지 않는다.

관찰 조건: 동일 개구부의 바닥과 양쪽 모서리가 식별됨

적용 속성 제안: `wardrobe.neckline.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:sw_square`, `slot:garment_detail:clt_ct035_v1`, `slot:garment_detail:sw_candidate_square`, `profile:clothing_ct035_v1`

후보 초안:

- `SPR_DRAFT_SF004_01` (SPT01-06): The top neckline has a straight horizontal base joined to two upright side edges.

## SF005 V·깊은 V·플런징

V의 수렴 모양과 내려가는 깊이는 별도다. plunging에 국제 공통 깊이 수치를 붙이지 않는다.

원문 연결: `SPT01-07` 브이넥 — V-neck, `SPT01-08` 딥 브이넥·플런징 — Deep V / Plunging neckline

관찰 구성: `top_A.left_neckline_edge`, `top_A.right_neckline_edge`, `top_A.neckline_low_point`

관계 설계: `top_A.left_neckline_edge → converges_with → top_A.right_neckline_edge`

혼동 경계: 깊은 V가 가슴골을 보장하지 않는다. 플런지 브라와 겉옷 목선을 분리한다.

관찰 조건: 양 경계·수렴점과 지정한 신체 기준점이 보임

적용 속성 제안: `wardrobe.neckline.contour`, `wardrobe.neckline.depth` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:sw_plunge`, `slot:garment_detail:sw_candidate_plunge`

후보 초안:

- `SPR_DRAFT_SF005_01` (SPT01-07): Two neckline edges converge to a V-shaped point on the top front.
- `SPR_DRAFT_SF005_02` (SPT01-08): The V-shaped neckline extends low along the center of the same torso.

## SF006 서플리스 목선

서로 다른 앞판의 사선 겹침으로 V를 만든다. 실제 랩 여밈은 추가 조건이다.

원문 연결: `SPT01-09` 서플리스넥 — Surplice neckline

관찰 구성: `top_A.left_front_panel`, `top_A.right_front_panel`

관계 설계: `top_A.left_front_panel → overlaps_diagonally → top_A.right_front_panel`

혼동 경계: 일반 V 재단·트위스트·봉제된 포 랩의 기능을 구분한다.

관찰 조건: 사선 가장자리와 아래로 이어지는 같은 앞판의 층 순서 확인

적용 속성 제안: `wardrobe.front.overlap`, `wardrobe.neckline.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Faux Wrap Skirt](https://www.seamwork.com/sewing-patterns/pattern-hacks-how-to-draft-a-faux-wrap-skirt)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF006_01` (SPT01-09): Two separate front panels overlap diagonally across the top front, forming a V neckline.

## SF007 스위트하트·수평 윗선

두 볼록 곡선과 중앙 오목점 또는 거의 수평인 경계를 선택한다. 끈 유무는 독립이다.

원문 연결: `SPT01-10` 스위트하트넥 — Sweetheart neckline, `SPT01-11` 스트레이트 어크로스 — Straight-across neckline

관찰 구성: `bodice_A.top_edge`, `bodice_A.center_dip`

관계 설계: `bodice_A.top_edge → forms_two_arcs_meeting_at → bodice_A.center_dip`

혼동 경계: 스트랩리스와 스위트하트를 동의어로 합치지 않는다. 컵 봉제는 별도다.

관찰 조건: 윗선 양쪽 곡선 또는 수평 경계가 같은 몸판에 속함

적용 속성 제안: `wardrobe.neckline.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Jovani — Strapless Dress Necklines Compared](https://www.jovani.com/blog/formal-events/strapless-dress/)

기존 검토 이웃: `profile:sw_sweetheart`, `slot:garment_detail:sw_candidate_sweetheart`

후보 초안:

- `SPR_DRAFT_SF007_01` (SPT01-10): Two rounded arcs on the bodice upper edge meet in a shallow central dip.
- `SPR_DRAFT_SF007_02` (SPT01-11): The bodice upper edge runs nearly straight across the upper chest.

## SF008 카울 목선

목 또는 앞가슴에 붙은 원단이 중력 방향으로 늘어지며 접힌다. 위치·처짐 깊이를 구체화한다.

원문 연결: `SPT01-12` 카울넥 — Cowl neck

관찰 구성: `top_A.draped_front`, `top_A.neckline_attachment`

관계 설계: `top_A.draped_front → hangs_from → top_A.neckline_attachment`

혼동 경계: 목걸이·머플러·장식 러플·쇄골 그림자와 다르다.

관찰 조건: 주름이 해당 목선에 이어지는 부착부와 처짐 바닥을 확인

적용 속성 제안: `wardrobe.neckline.drape` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Claudette Cowl Neck Dress](https://www.seamwork.com/pdf-sewing-patterns/claudette-cowl-neck-dress), [V&A — Madeleine Vionnet](https://www.vam.ac.uk/articles/madeleine-vionnet-an-introduction)

기존 검토 이웃: `profile:pfe_cowl`, `slot:garment_detail:clt_ct037_v1`, `slot:garment_detail:pfe_cowl_candidate`, `profile:clothing_ct037_v1`

후보 초안:

- `SPR_DRAFT_SF008_01` (SPT01-12): The same neckline fabric hangs into a soft U-shaped fold across the top front.

## SF009 오프숄더·바르도

양쪽 어깨 아래로 내려간 동일 옷의 윗선과 연결된 소매를 본다. 접힌 밴드는 선택 변형이다.

원문 연결: `SPT01-13` 오프숄더 — Off-the-shoulder, `SPT01-14` 바르도넥 — Bardot neckline

관찰 구성: `top_A.upper_edge`, `wearer_A.shoulders`, `top_A.sleeves`

관계 설계: `top_A.upper_edge → lies_below → wearer_A.shoulders`

혼동 경계: 목선이 넓은 것과 어깨 아래로 내려간 것은 다르다. Bardot에 밴드 필수를 강제하지 않는다.

관찰 조건: 양쪽 어깨 기준점·같은 직물 윗선·소매 접속이 읽힘

적용 속성 제안: `wardrobe.shoulder.coverage`, `wardrobe.neckline.fold` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Corsets, Crinolines and Bustles](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

기존 검토 이웃: `profile:sf_profile_151_base`, `profile:sw_offshoulder`, `slot:body_orientation:sf_151_base`, `slot:garment_detail:clt_ct038_v1`, `slot:garment_detail:clt_ct038_v2`

후보 초안:

- `SPR_DRAFT_SF009_01` (SPT01-13): The top upper edge runs below both shoulders and continues into the sleeves.
- `SPR_DRAFT_SF009_02` (SPT01-14): A folded fabric band follows the top edge below both shoulders.

## SF010 원숄더·콜드숄더

한쪽 지지 연결과 어깨에 둘러싸인 개구부는 다른 위상이다. 좌우 소유자를 보존한다.

원문 연결: `SPT01-15` 원숄더 — One-shoulder, `SPT01-16` 콜드숄더 — Cold-shoulder

관찰 구성: `top_A.left_shoulder_connection`, `top_A.shoulder_window`, `wearer_A.shoulder`

관계 설계: `top_A.shoulder_window → is_bounded_by → top_A.remaining_fabric`

혼동 경계: 원숄더를 한쪽 소매가 없는 옷으로 고정하지 않는다. 콜드숄더와 오프숄더를 구분한다.

관찰 조건: 선택된 한쪽 연결 또는 개구부 주변 잔여 직물이 보여야 함

적용 속성 제안: `wardrobe.shoulder.support_topology`, `wardrobe.shoulder.opening` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:pfe_one_shoulder`, `profile:sw_oneshoulder`, `slot:garment_detail:pfe_one_shoulder_candidate`, `slot:garment_detail:sw_candidate_oneshoulder`, `bundle:clothing_b_sari_continuity`

후보 초안:

- `SPR_DRAFT_SF010_01` (SPT01-15): The top crosses the left shoulder while its upper edge leaves the right shoulder open.
- `SPR_DRAFT_SF010_02` (SPT01-16): A bounded opening in the sleeve exposes the shoulder while fabric still crosses above it.

## SF011 홀터 연결

상의 앞의 끈 또는 원단이 목 뒤 쪽으로 이어지는 경로다. 앞가슴 높이와 등 개방은 별도다.

원문 연결: `SPT01-17` 홀터넥 — Halter neck

관찰 구성: `top_A.neck_strap`, `top_A.front_panel`, `wearer_A.neck_back`

관계 설계: `top_A.neck_strap → connects_front_to → wearer_A.neck_back`

혼동 경계: 레이서백·높은 목선만으로 홀터가 되지 않는다.

관찰 조건: 앞판 부착부와 목 옆으로 이어지는 끈 경로; 뒤 가림이면 완전 연결은 미관찰

적용 속성 제안: `wardrobe.strap.route` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — All About Necklines](https://blog.moodfabrics.com/all-about-necklines/)

기존 검토 이웃: `profile:pfe_halter`, `profile:sw_halter`, `slot:garment_detail:pfe_halter_candidate`, `slot:garment_detail:sw_candidate_halter`, `profile:racerback_sports_bra_strap_convergence`

후보 초안:

- `SPR_DRAFT_SF011_01` (SPT01-17): The top front connects to straps that pass around the back of the same neck.

## SF012 키홀·일루전 패널

실제 빈 개구부와 투명한 직물 패널은 다른 구성이다. 일루전에는 피부색이 아닌 망사도 가능하다.

원문 연결: `SPT01-18` 키홀넥 — Keyhole neckline, `SPT01-19` 일루전 넥라인 — Illusion neckline

관찰 구성: `top_A.keyhole_edge`, `top_A.illusion_panel`, `top_A.opaque_bodice`

관계 설계: `top_A.illusion_panel → joins_to → top_A.opaque_bodice`

혼동 경계: 원문 skin-tone은 흔한 변형이며 보편 필수가 아니다. 피부색 안감·맨살·실제 구멍을 구분한다.

관찰 조건: 키홀의 둘레 또는 망사의 조직과 봉합 경계가 읽힘

적용 속성 제안: `wardrobe.opening.topology`, `wardrobe.layer.connection` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `profile:pfe_illusion_panel`, `slot:garment_detail:pfe_illusion_panel_candidate`

후보 초안:

- `SPR_DRAFT_SF012_01` (SPT01-18): A small bounded opening sits below the neckline on the same top.
- `SPR_DRAFT_SF012_02` (SPT01-19): A sheer mesh panel visibly joins the opaque bodice across the upper neckline.

## SF013 스트랩리스 지지 배치

그 옷의 어깨끈이 없는 구성과 다른 옷의 끈을 분리한다. 숨은 내부 지지력을 추론하지 않는다.

원문 연결: `SPT01-20` 스트랩리스 — Strapless

관찰 구성: `top_A.upper_bodice`, `wearer_A.shoulder_paths`

관계 설계: `top_A.upper_bodice → has_no_visible_strap_across → wearer_A.shoulder_paths`

혼동 경계: 목걸이·안쪽 브라 끈은 다른 소유자다. 정면만으로 숨은 끈 부재를 확증하지 않는다.

관찰 조건: 요청된 관찰 방향에서 양 어깨와 앞뒤 연결 경로가 충분히 읽힘

적용 속성 제안: `wardrobe.strap.presence` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Jovani — Strapless Dress Necklines Compared](https://www.jovani.com/blog/formal-events/strapless-dress/), [Bravissimo — Moulded and Padded T-Shirt Bras](https://www.bravissimo.com/tshirt-bras-for-big-boobs/)

기존 검토 이웃: `profile:sw_strapless`, `profile:y2kr_bandeau`, `profile:y2kr_tube_dress`, `slot:garment_detail:sw_candidate_strapless`, `slot:wardrobe_style:y2kr_bandeau`

후보 초안:

- `SPR_DRAFT_SF013_01` (SPT01-20): The top upper edge spans the torso with both shoulder paths free of straps belonging to that top.

## SF014 민소매·탱크·캐미솔

소매 부재, 어깨 연결폭, 의복 길이와 내장 레이어를 독립 변수로 둔다.

원문 연결: `SPT02-01` 슬리브리스 — Sleeveless, `SPT02-02` 탱크 톱 — Tank top, `SPT02-03` 캐미솔·캐미 — Camisole / Cami

관찰 구성: `top_A.armhole`, `top_A.shoulder_bridge`, `top_A.hem`

관계 설계: `top_A.shoulder_bridge → joins → top_A.front_and_back`

혼동 경계: 캐미솔이라고 짧거나 비치거나 내장 브라가 있다고 확정하지 않는다.

관찰 조건: 어깨 연결과 소매 부착부가 보임; 몸판 아래층은 별도 선언

적용 속성 제안: `wardrobe.sleeve.presence`, `wardrobe.strap.width` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Paradise Patterns — Sommar Camisole](https://paradisepatterns.com/products/sommar-camisole-pdf-sewing-pattern-with-built-in-bralette-low-support-thin-straps-cropped-or-hip-length-sizes-bust-28-58-reversible)

기존 검토 이웃: `bundle:uniform_layered_contrast_robe`, `profile:cold_shoulder_cutout_topology`, `profile:sw_jane`, `profile:uniform_sleeveless_robe_over_inner_sleeves`, `profile:y2kr_crop_tank`

후보 초안:

- `SPR_DRAFT_SF014_01` (SPT02-02): The tank front and back are joined by broad fabric bridges over the shoulders.
- `SPR_DRAFT_SF014_02` (SPT02-03): The camisole front and back connect through narrow shoulder straps.
- `SPR_DRAFT_SF014_03` (SPT02-01): The sleeveless top has finished armhole edges without attached sleeves.

## SF015 가는·넓은 어깨끈

폭과 부착 위치는 개별 속성이다. 가는 끈이라는 이름에 고정 mm를 붙이지 않는다.

원문 연결: `SPT02-04` 스파게티 스트랩 — Spaghetti straps, `SPT02-05` 와이드 스트랩 — Wide straps

관찰 구성: `top_A.shoulder_straps`, `top_A.front_anchor`, `top_A.back_anchor`

관계 설계: `top_A.shoulder_straps → connect → top_A.front_anchor_and_back_anchor`

혼동 경계: 몸 위에 그린 선·목걸이·다른 옷의 끈과 구별한다.

관찰 조건: 각 끈의 폭과 같은 옷의 부착 양끝이 읽힘

적용 속성 제안: `wardrobe.strap.width`, `wardrobe.strap.attachment` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Paradise Patterns — Sommar Camisole](https://paradisepatterns.com/products/sommar-camisole-pdf-sewing-pattern-with-built-in-bralette-low-support-thin-straps-cropped-or-hip-length-sizes-bust-28-58-reversible)

기존 검토 이웃: `slot:wardrobe_style:dark_spaghetti_strap_top`

후보 초안:

- `SPR_DRAFT_SF015_01` (SPT02-04): Two narrow straps run from the top front over the shoulders to the back.
- `SPR_DRAFT_SF015_02` (SPT02-05): Wide fabric straps span the shoulders and join the same top front and back.

## SF016 레이서백·크로스백

등 위 중앙으로 모이는 접속과 X 교차를 다른 변형으로 둔다. 교차가 접합점인지는 별도다.

원문 연결: `SPT02-06` 레이서백 — Racerback, `SPT02-15` 크로스백 — Cross-back

관찰 구성: `top_A.back_straps`, `top_A.central_back_panel`

관계 설계: `top_A.back_straps → converge_into → top_A.central_back_panel`

혼동 경계: 끈이 평행인 등과 다르다. 앞면 포즈만으로 뒤 구조를 PASS 처리하지 않는다.

관찰 조건: 뒤 또는 읽히는 3/4 방향에서 두 경로·접속·교차 확인

적용 속성 제안: `wardrobe.back.strap_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Oner Active — PrecisionMove Drop Armhole Vest](https://uk.oneractive.com/products/precisionmove-drop-armhole-tank-top-white), [Bravissimo — Moulded and Padded T-Shirt Bras](https://www.bravissimo.com/tshirt-bras-for-big-boobs/)

기존 검토 이웃: `profile:fit_ff52_v1`, `profile:racerback_sports_bra_strap_convergence`, `slot:garment_detail:fit_ff52_v1_candidate`, `slot:garment_detail:racerback_strap_yoke_convergence`, `slot:wardrobe_style:court_skort_racerback_top_ensemble`

후보 초안:

- `SPR_DRAFT_SF016_01` (SPT02-06): The top back narrows to a central racerback bridge between the shoulder blades.
- `SPR_DRAFT_SF016_02` (SPT02-15): Two straps belonging to the top cross visibly in an X over the back.

## SF017 컷어웨이·드롭·깊은 암홀

안으로 들어가는 앞 어깨 경계와 아래로 내려가는 암홀 끝점을 다른 축으로 둔다.

원문 연결: `SPT02-07` 컷어웨이 암홀 — Cutaway armholes, `SPT02-08` 드롭 암홀 — Drop armhole, `SPT02-09` 딥 암홀·로 암홀 — Deep / Low armhole

관찰 구성: `top_A.armhole_front`, `top_A.armhole_low_point`, `wearer_A.armpit`

관계 설계: `top_A.armhole_low_point → lies_below → wearer_A.armpit`

혼동 경계: 드롭 숄더는 소매 연결선 위치다. 큰 암홀이 옆가슴 노출을 보장하지 않는다.

관찰 조건: 암홀 둘레·아래 끝점과 옆판 및 아래층이 동시에 보임

적용 속성 제안: `wardrobe.armhole.contour`, `wardrobe.armhole.depth` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Oner Active — PrecisionMove Drop Armhole Vest](https://uk.oneractive.com/products/precisionmove-drop-armhole-tank-top-white)

기존 검토 이웃: `bundle:pe_bundle_parallel_scene_deep_focus`, `profile:chiaroscuro_form_modeling_relation`, `profile:clothing_ct045_v1`, `profile:cumulonimbus_tower_anvil_precipitation_outflow`, `profile:hw_francaise_free_back`

후보 초안:

- `SPR_DRAFT_SF017_01` (SPT02-07): The armhole front curves inward toward the neck, leaving the front shoulder uncovered.
- `SPR_DRAFT_SF017_02` (SPT02-08, SPT02-09): The tank armhole extends well below the same wearer's armpit.

## SF018 머슬 탱크·오픈사이드

제품 통칭과 열린 옆판의 실제 형태를 분리한다. 연결부가 남는 위치를 지정한다.

원문 연결: `SPT02-10` 머슬 탱크† — Muscle tank, `SPT02-11` 오픈사이드† — Open-side top

관찰 구성: `top_A.side_edges`, `top_A.remaining_side_connections`

관계 설계: `top_A.side_edges → leave_space_between → top_A.remaining_side_connections`

혼동 경계: 모든 muscle tank가 큰 암홀인 것은 아니다. 운동 능력과 몸 근육을 추가하지 않는다.

관찰 조건: 연속 피부 노출인지 아래층 의복인지 및 잔여 연결부 확인

적용 속성 제안: `wardrobe.side.opening` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Oner Active — PrecisionMove Drop Armhole Vest](https://uk.oneractive.com/products/precisionmove-drop-armhole-tank-top-white)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF018_01` (SPT02-11): The top side is open between its upper shoulder connection and the lower side tie.
- `SPR_DRAFT_SF018_02` (SPT02-10): A loose cropped muscle-style tank has broad open armholes and a continuous front.

## SF019 옆·뒤 묶음

묶음 위치와 두 끈의 시작점·교차·매듭을 구체화한다. 조절 기능과 장식 리본은 독립이다.

원문 연결: `SPT02-12` 타이사이드 — Tie-side, `SPT02-16` 타이백 — Tie-back

관찰 구성: `top_A.tie_ends`, `top_A.knot`, `top_A.side_or_back_edges`

관계 설계: `top_A.tie_ends → meet_in → top_A.knot`

혼동 경계: 고정된 bow 장식을 여밈 기능으로 추정하지 않는다.

관찰 조건: 옷에 붙은 양끝과 실제 매듭 경로가 보임

적용 속성 제안: `wardrobe.closure.tie_location`, `wardrobe.closure.connection` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:sw_tieside`, `slot:garment_detail:sw_candidate_tieside`, `profile:sw_tieback`, `slot:garment_detail:sw_candidate_tieback`

후보 초안:

- `SPR_DRAFT_SF019_01` (SPT02-12): Two tie ends attached to the top side edges meet in a visible side knot.
- `SPR_DRAFT_SF019_02` (SPT02-16): The top back edges connect through two ties knotted at the center back.

## SF020 오픈백·로백

뒤판이 비워진 영역과 낮아진 뒤 윗선의 범위를 저장한다. 고정 비율은 없다.

원문 연결: `SPT02-13` 오픈백·백리스 — Open-back / Backless, `SPT02-14` 로백 — Low-back

관찰 구성: `top_A.back_opening`, `top_A.back_upper_edge`, `wearer_A.back`

관계 설계: `top_A.back_upper_edge → bounds_open_region_on → wearer_A.back`

혼동 경계: 앞면 깊은 목선·망사 뒤판·가려진 등과 구분한다.

관찰 조건: 등 경계와 연결 직물, 아래층 유무가 읽히는 후면 관찰 필요

적용 속성 제안: `wardrobe.back.coverage` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:pfe_back_face`, `slot:subject_framing:pfe_back_face_candidate`, `profile:clothing_ct124_v1`, `slot:footwear:backless_loafers`, `slot:footwear:clt_ct124_v1`

후보 초안:

- `SPR_DRAFT_SF020_01` (SPT02-13): The top has an open back region framed by connected fabric edges.
- `SPR_DRAFT_SF020_02` (SPT02-14): The top back upper edge sits low across the back while the lower panel remains continuous.

## SF021 캡·플러터 소매

어깨 끝의 짧은 덮음과 부착부에서 자유 끝으로 퍼지는 소매를 구분한다.

원문 연결: `SPT02-17` 캡 슬리브 — Cap sleeves, `SPT02-18` 플러터 슬리브 — Flutter sleeves

관찰 구성: `top_A.sleeve_attachment`, `top_A.sleeve_free_edge`

관계 설계: `top_A.sleeve_free_edge → fans_out_from → top_A.sleeve_attachment`

혼동 경계: 플러터 소매가 자세 변화 없이 반드시 겨드랑이를 드러내는 것은 아니다.

관찰 조건: 부착선·소매 끝·팔의 상대 경계가 동시에 식별됨

적용 속성 제안: `wardrobe.sleeve.length`, `wardrobe.sleeve.volume` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Tilly and the Buttons — Dominique Pattern Hacks](https://tillyandthebuttons.com/blogs/sewing/dominique-pattern-hacks)

기존 검토 이웃: `profile:clothing_ct048_v1`, `slot:garment_detail:clt_ct048_v1`

후보 초안:

- `SPR_DRAFT_SF021_01` (SPT02-17): A short cap sleeve covers just the shoulder tip on the blouse.
- `SPR_DRAFT_SF021_02` (SPT02-18): The blouse sleeve flares from its attachment into a loose rippling free edge.

## SF022 뷔스티에·코르셋 톱

컵·몸판·채널·여밈을 선택적으로 기술한다. 이름만으로 기능적 조임과 보닝 모두를 강제하지 않는다.

원문 연결: `SPT03-01` 뷔스티에 — Bustier, `SPT03-02` 코르셋 톱 — Corset top

관찰 구성: `top_A.cup_panels`, `top_A.torso_panels`, `top_A.channels`

관계 설계: `top_A.cup_panels → join_to → top_A.torso_panels`

혼동 경계: 부드러운 패션 톱과 역사적 보정 코르셋을 구별한다. 큰 가슴을 새로 추가하지 않는다.

관찰 조건: 컵·몸판 경계 또는 선택한 채널·여밈이 같은 의복에 속함

적용 속성 제안: `wardrobe.bodice.panel_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Natalie Rolt — Elina Bustier](https://www.natalierolt.com/products/elina-bustier), [The Met — Yohji Yamamoto Bustier](https://www.metmuseum.org/art/collection/search/693847), [V&A — Corsets, Crinolines and Bustles](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

기존 검토 이웃: `slot:fetish_styling:corset_bustier_layered`, `profile:clothing_ct023_v1`, `profile:clothing_ct023_v2`, `profile:y2kr_bustier`, `slot:garment_detail:sff_extra_xa056`

후보 초안:

- `SPR_DRAFT_SF022_01` (SPT03-01): The bustier has distinct curved cup panels joined to a longer fitted torso panel.
- `SPR_DRAFT_SF022_02` (SPT03-02): The corset-style top has visible vertical channels and a constructed front closure.

## SF023 언더버스트 코르셋

상단 경계가 가슴 아래에 놓이는 별도 의복이다. 가슴 아래 피부 노출의 이름과 다르다.

원문 연결: `SPT03-03` 언더버스트 코르셋 — Underbust corset

관찰 구성: `corset_A.top_edge`, `inner_top_A`, `wearer_A.underbust`

관계 설계: `corset_A.top_edge → lies_below → wearer_A.underbust`

혼동 경계: underboob·underbust seam·underbust cutout과 동의어가 아니다.

관찰 조건: 코르셋 상단·아래층의 연속·옷끼리의 겹침 순서 확인

적용 속성 제안: `wardrobe.corset.coverage`, `wardrobe.layer.order` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Corsets, Crinolines and Bustles](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF023_01` (SPT03-03): A separate corset begins below the bust and wraps over the continuous inner blouse at the waist.

## SF024 브라 톱·브라렛

컵·밴드·끈·레이스의 조합이며 제품 변형이 넓다. bralette를 무조건 무와이어로 정의하지 않는다.

원문 연결: `SPT03-04` 브라 톱 — Bra top, `SPT03-05` 브라렛 — Bralette

관찰 구성: `bra_top_A.cups`, `bra_top_A.band`, `bra_top_A.straps`

관계 설계: `bra_top_A.cups → attach_to → bra_top_A.band`

혼동 경계: 스포츠형·삼각형·와이어·패딩은 별도 옵션이며 자동 all-of 대상이 아니다.

관찰 조건: 선택한 패널·밴드·끈의 연결; 성능은 외형과 분리

적용 속성 제안: `wardrobe.bra.panel_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Bravissimo — Moulded and Padded T-Shirt Bras](https://www.bravissimo.com/tshirt-bras-for-big-boobs/)

기존 검토 이웃: `slot:garment_detail:visible_bralette_tailored_blazer_layer`, `profile:pfe_neck_foundation`, `profile:underwear_as_outerwear_layer_system`, `slot:garment_detail:pfe_neck_foundation_candidate`

후보 초안:

- `SPR_DRAFT_SF024_01` (SPT03-04): The bra-style top has two visible cup regions joined to a short torso band.
- `SPR_DRAFT_SF024_02` (SPT03-05): The bralette has soft triangular panels joined to a narrow lower band.

## SF025 밴도·튜브 톱

몸통을 두르는 윗부분의 형태와 전체 길이를 분리한다. 브랜드마다 길이 경계가 다르다.

원문 연결: `SPT03-06` 밴도 — Bandeau, `SPT03-07` 튜브 톱 — Tube top

관찰 구성: `top_A.torso_band`, `top_A.hem`

관계 설계: `top_A.torso_band → encircles → wearer_A.torso`

혼동 경계: 윗선 모양·와이어·노출 정도를 이름에서 추론하지 않는다.

관찰 조건: 같은 원통 몸판의 윗선과 밑단 범위를 확인

적용 속성 제안: `wardrobe.bodice.length`, `wardrobe.strap.presence` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `bundle:sw_bundle_convertible_bandeau`, `bundle:sw_variant_bandeau`, `profile:sw_bandeau`, `profile:y2kr_bandeau`, `slot:garment_detail:sw_candidate_bandeau`

후보 초안:

- `SPR_DRAFT_SF025_01` (SPT03-06): A short strapless fabric band wraps continuously around the torso.
- `SPR_DRAFT_SF025_02` (SPT03-07): A strapless tube top extends from the upper torso down to the waist.

## SF026 컵 재단·언더와이어

컵의 봉제 외곽과 내부 와이어 명세를 구별한다. 보이는 케이싱이 실제 금속을 입증하지 않는다.

원문 연결: `SPT03-08` 컵드 톱 — Cupped top, `SPT03-09` 언더와이어 — Underwire

관찰 구성: `top_A.cup_edges`, `top_A.under_cup_channel`

관계 설계: `top_A.under_cup_channel → follows_lower_edge_of → top_A.cup_edges`

혼동 경계: 주름·가슴 윤곽·패딩과 다르다. 와이어 성분과 압박은 픽셀 게이트에서 제외한다.

관찰 조건: 컵의 하단과 곡선 채널이 같은 컵에 이어짐

적용 속성 제안: `wardrobe.cup.seaming`, `wardrobe.cup.visible_casing` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Natalie Rolt — Elina Bustier](https://www.natalierolt.com/products/elina-bustier), [Bravissimo — Moulded and Padded T-Shirt Bras](https://www.bravissimo.com/tshirt-bras-for-big-boobs/)

기존 검토 이웃: `profile:clothing_ct072_v1`, `profile:fit_ff40_v2`, `slot:garment_detail:clt_ct072_v1`

후보 초안:

- `SPR_DRAFT_SF026_01` (SPT03-08): Separate curved cup seams shape the top front above a continuous lower bodice.
- `SPR_DRAFT_SF026_02` (SPT03-09): A curved casing follows the lower edge of each cup on the top.

## SF027 패딩·몰디드 컵

패딩의 추가 층과 성형 공정은 독립 명세다. 보이는 외관은 매끈한 곡면 등으로 별도 저장한다.

원문 연결: `SPT03-10` 패디드·몰디드 컵 — Padded / Molded cups

관찰 구성: `bra_A.cup_surface`, `bra_A.visible_inner_layer`

관계 설계: `bra_A.visible_inner_layer → lies_inside → bra_A.cup_surface`

혼동 경계: 매끈한 컵이 패딩·몰딩 공정·지지 성능을 자동 입증하지 않는다.

관찰 조건: 표면 게이트만 가능; 패딩·성형 공정 자체는 내부 또는 제품 명세로 검증

적용 속성 제안: `wardrobe.cup.surface`, `metadata.cup.padding`, `metadata.cup.molding` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Bravissimo — Moulded and Padded T-Shirt Bras](https://www.bravissimo.com/tshirt-bras-for-big-boobs/)

기존 검토 이웃: `profile:appearance_rel_h014`, `profile:sv_padded_garment_contour`, `profile:wearable_protective_armor_system`, `profile:y2kr_skate_shoes`, `slot:footwear:y2kr_skate_shoes`

후보 초안:

- `SPR_DRAFT_SF027_01` (SPT03-10): The selected cup has a smooth continuous outer surface without a visible central seam.

## SF028 보닝·채널

몸판의 세로 케이싱과 내부 지지재를 분리한다. 채널의 위치·끝점을 관찰한다.

원문 연결: `SPT03-11` 보닝 — Boning

관찰 구성: `top_A.vertical_channels`, `top_A.bodice_panels`

관계 설계: `top_A.vertical_channels → run_along → top_A.bodice_panels`

혼동 경계: 페인팅된 줄·골지 조직·프린세스 심과 다르다. 채널만으로 내부 지지재 강도를 판단하지 않는다.

관찰 조건: 동일 몸판의 채널 양옆과 시작·끝 위치가 읽힘

적용 속성 제안: `wardrobe.bodice.visible_channels` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Natalie Rolt — Elina Bustier](https://www.natalierolt.com/products/elina-bustier), [V&A — Corsets, Crinolines and Bustles](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

기존 검토 이웃: `profile:clothing_ct023_v1`, `profile:clothing_ct072_v1`, `profile:clothing_ct072_v2`, `profile:orn_profile_gd40`, `profile:y2kr_corset_top`

후보 초안:

- `SPR_DRAFT_SF028_01` (SPT03-11): Several narrow vertical casings run along the fitted bodice panels.

## SF029 버스트 다트·프린세스 심

수렴해 끝나는 봉제와 여러 패널을 길게 잇는 절개를 다른 위상으로 둔다.

원문 연결: `SPT03-12` 버스트 다트 — Bust darts, `SPT03-13` 프린세스 심 — Princess seams

관찰 구성: `top_A.dart_tip`, `top_A.dart_legs`, `top_A.princess_seam`

관계 설계: `top_A.dart_legs → converge_at → top_A.dart_tip`

혼동 경계: 세로 직선 장식·주름·몸 피부선과 구분한다.

관찰 조건: 다트의 끝 또는 절개의 이어짐과 소유 패널을 확인

적용 속성 제안: `wardrobe.bodice.shaping_seams` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Darts Into Princess Seams](https://www.seamwork.com/sewing-patterns/pattern-hack-turn-darts-into-princess-seams)

기존 검토 이웃: `profile:clothing_ct031_v1`, `slot:garment_detail:clt_ct031_v1`, `slot:garment_detail:clt_ct031_v2`

후보 초안:

- `SPR_DRAFT_SF029_01` (SPT03-12): A short stitched dart narrows from the blouse side seam to a tip near the bust.
- `SPR_DRAFT_SF029_02` (SPT03-13): A curved princess seam runs continuously through the bust area toward the waist.

## SF030 언더버스트 심

가슴 아래의 몸판 연결선이다. 밑단·코르셋 상단·빈 구멍과 다르다.

원문 연결: `SPT03-14` 언더버스트 심 — Underbust seam

관찰 구성: `top_A.underbust_seam`, `top_A.upper_panel`, `top_A.lower_panel`

관계 설계: `top_A.underbust_seam → joins → top_A.upper_and_lower_panels`

혼동 경계: 엠파이어는 전체 치마 시작 위치까지의 관계다. 가슴 아래 절개라고 피부가 보이는 것은 아니다.

관찰 조건: 동일 원단 패널 사이의 연결선과 아래 연속 몸판 확인

적용 속성 제안: `wardrobe.bodice.seam_height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Darts Into Princess Seams](https://www.seamwork.com/sewing-patterns/pattern-hack-turn-darts-into-princess-seams), [Natalie Rolt — Elina Bustier](https://www.natalierolt.com/products/elina-bustier)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF030_01` (SPT03-14): A continuous seam joins the upper and lower bodice directly beneath the bust.

## SF031 가슴 루칭·트위스트

주름의 수렴 고정점과 원단의 꼬인 교차를 구분한다. 한국어 셔링은 구조 문맥으로 해석한다.

원문 연결: `SPT03-15` 셔링 버스트·트위스트 프런트 — Ruched bust / Twist-front

관찰 구성: `top_A.bust_folds`, `top_A.gather_anchor`, `top_A.twist_crossing`

관계 설계: `top_A.bust_folds → converge_at → top_A.gather_anchor`

혼동 경계: 루칭·셔링·스모킹을 하나의 고무실 속성으로 합치지 않는다.

관찰 조건: 모음 지점 또는 실제 원단 교차가 보이고 몸 그림자와 분리됨

적용 속성 제안: `wardrobe.bust.folds`, `wardrobe.front.twist` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — A Guide to Shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering)

기존 검토 이웃: `profile:sw_twist`, `slot:garment_detail:sw_candidate_twist`

후보 초안:

- `SPR_DRAFT_SF031_01` (SPT03-15): Small folds on the top front converge into a center-bust seam.
- `SPR_DRAFT_SF031_02` (SPT03-15): Two front fabric sections twist around a visible central crossing.

## SF032 크롭·마이크로 크롭·미드리프

상의 길이와 상의-하의 사이의 보이는 피부 범위를 따로 저장한다. 모든 크롭이 배꼽을 드러내지 않는다.

원문 연결: `SPT04-01` 크롭 톱 — Crop top, `SPT04-02` 마이크로 크롭† — Micro-crop top, `SPT04-03` 미드리프 바링† — Midriff-baring

관찰 구성: `top_A.hem`, `bottom_A.waistband`, `wearer_A.navel`

관계 설계: `top_A.hem → lies_above → bottom_A.waistband`

혼동 경계: top crop과 영상 crop을 구별한다. 길이만으로 가슴 아래 피부 노출을 자동 추가하지 않는다.

관찰 조건: 상의 밑단·하의 허리단·요청된 기준점과 아래층을 함께 확인

적용 속성 제안: `wardrobe.top.hem_height`, `wardrobe.coverage.midriff_gap` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Paradise Patterns — Sommar Camisole](https://paradisepatterns.com/products/sommar-camisole-pdf-sewing-pattern-with-built-in-bralette-low-support-thin-straps-cropped-or-hip-length-sizes-bust-28-58-reversible), [British Vogue — Skin Reveal](https://www.vogue.co.uk/fashion/article/skin-reveal-trend)

기존 검토 이웃: `profile:pfe_midriff`, `slot:garment_detail:pfe_midriff_candidate`, `slot:wardrobe_style:crop_top_wide_pants`, `profile:clothing_crop_top_waist_hem`, `profile:sw_sporttop`

후보 초안:

- `SPR_DRAFT_SF032_01` (SPT04-01): The short top hem sits just above the high waistband with a narrow gap between the garments.
- `SPR_DRAFT_SF032_02` (SPT04-02): The top hem ends high on the torso, leaving a larger gap above the waistband.
- `SPR_DRAFT_SF032_03` (SPT04-03): The same top hem and trouser waistband leave a visible midriff gap between them.

## SF033 앞 여밈·매듭

앞판 끝이 묶이는 여밈과 봉제된 장식 매듭을 분리한다. 매듭 아래 빈 공간은 선택 사항이다.

원문 연결: `SPT04-04` 타이프런트 — Tie-front, `SPT04-05` 노트프런트 — Knot-front

관찰 구성: `top_A.front_ends`, `top_A.front_knot`

관계 설계: `top_A.front_ends → meet_in → top_A.front_knot`

혼동 경계: 노트 장식에 실제 풀리는 여밈 기능을 붙이지 않는다.

관찰 조건: 양끝의 출발 앞판·매듭·남은 몸판의 연속 확인

적용 속성 제안: `wardrobe.front.knot`, `wardrobe.closure.function_metadata` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Wynn Tie-Front Crop](https://www.seamwork.com/pdf-sewing-patterns/wynn-tie-front-bolero)

기존 검토 이웃: `profile:y2kr_tie_front`, `slot:garment_detail:y2kr_tie_front`

후보 초안:

- `SPR_DRAFT_SF033_01` (SPT04-04): Two fabric ends from the top front tie together in a visible knot.
- `SPR_DRAFT_SF033_02` (SPT04-05): A fixed fabric knot gathers the continuous top front at its center.

## SF034 스플릿·스카프·핸드커치프

앞의 분리된 가장자리, 묶인 직물 몸판, 뾰족한 밑단을 독립적으로 분해한다.

원문 연결: `SPT04-06` 스플릿 프런트† — Split-front, `SPT04-07` 스카프 톱·반다나 톱 — Scarf / Bandana top, `SPT04-08` 핸드커치프 톱 — Handkerchief top

관찰 구성: `top_A.split_edges`, `top_A.pointed_hem`, `top_A.tie_anchor`

관계 설계: `top_A.pointed_hem → extends_below → top_A.side_hem`

혼동 경계: 삼각 밑단이 반드시 스카프 재활용·백리스·짧은 길이를 뜻하지 않는다.

관찰 조건: 틈의 시작점 또는 밑단의 상대 높이; 제작 이력은 별도

적용 속성 제안: `wardrobe.front.split`, `wardrobe.hem.asymmetry` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:clothing_ct104_v2`, `profile:uniform_neck_scarf_separate_hair_ornament`, `profile:wrap_front_overlap_closure`, `profile:wrap_skirt_overlap_closure`, `profile:y2kr_bandana`

후보 초안:

- `SPR_DRAFT_SF034_01` (SPT04-06): The top front lower edges separate into an open split below the closure.
- `SPR_DRAFT_SF034_02` (SPT04-08): The top hem falls to a distinct central point lower than its side edges.
- `SPR_DRAFT_SF034_03` (SPT04-07): A scarf-like triangular fabric panel wraps across the torso and ties at the back.

## SF035 허리·옆·배꼽 컷아웃

개구부의 위치·개수·주변 연결과 아래층을 기록한다. 원단이 비워져도 피부가 보인다는 보장은 없다.

원문 연결: `SPT04-09` 웨이스트 컷아웃 — Waist cutout, `SPT04-10` 사이드 컷아웃 — Side cutout, `SPT04-11` 네이블 컷아웃† — Navel cutout

관찰 구성: `dress_A.waist_opening`, `dress_A.remaining_bridges`, `inner_A`

관계 설계: `dress_A.waist_opening → is_bounded_by → dress_A.remaining_fabric`

혼동 경계: 투명 패널·피부색 안감·단순 크롭의 열린 밑단과 다르다.

관찰 조건: 둘레와 잔여 연결, 구멍 뒤에 보이는 표면의 소유자 확인

적용 속성 제안: `wardrobe.cutout.location`, `wardrobe.cutout.topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Skin Reveal](https://www.vogue.co.uk/fashion/article/skin-reveal-trend)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF035_01` (SPT04-09): A bounded opening interrupts the dress fabric at the waist while connected fabric remains above and below.
- `SPR_DRAFT_SF035_02` (SPT04-11): The dress has a bounded opening positioned around the navel area.
- `SPR_DRAFT_SF035_03` (SPT04-10): A bounded opening lies at the side waist of the dress with continuous fabric above and below.

## SF036 O링 연결

서로 분리된 패널 또는 끈의 양끝이 같은 고리를 통과하거나 부착된다. 단순 고리 프린트와 다르다.

원문 연결: `SPT04-12` 링 링크·O링 디테일 — Ring-linked / O-ring detail

관찰 구성: `top_A.left_tab`, `top_A.right_tab`, `ring_A`

관계 설계: `top_A.left_tab → joins_via_ring_to → top_A.right_tab`

혼동 경계: 고리 장식만으로 구조 연결·조임 기능·복부 노출을 판단하지 않는다.

관찰 조건: 같은 고리와 두 탭의 부착부·주변 빈 공간이 읽힘

적용 속성 제안: `wardrobe.hardware.connection` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Skin Reveal](https://www.vogue.co.uk/fashion/article/skin-reveal-trend)

기존 검토 이웃: `slot:fetish_styling:sff_pro_e05`

후보 초안:

- `SPR_DRAFT_SF036_01` (SPT04-12): Two separate fabric tabs attach to opposite sides of the same visible ring.

## SF037 미드리프 플로싱

의복에 연결된 가는 끈이 복부를 감는 경로다. 체인 장신구와 소유자를 구분한다.

원문 연결: `SPT04-13` 미드리프 플로싱† — Midriff flossing

관찰 구성: `top_A.waist_ties`, `top_A.tie_anchor`, `wearer_A.waist`

관계 설계: `top_A.waist_ties → wrap_around → wearer_A.waist`

혼동 경계: body chain·허리벨트·신체 구속 행위를 자동 추가하지 않는다.

관찰 조건: 의복 부착점·몸 앞과 옆의 이어짐·매듭이 식별됨

적용 속성 제안: `wardrobe.tie.route` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Skin Reveal](https://www.vogue.co.uk/fashion/article/skin-reveal-trend)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF037_01` (SPT04-13): Thin ties attached to the top wrap around the exposed waist and meet at a side knot.

## SF038 로·하이라이즈

하의 허리단을 같은 신체 기준점에 결속한다. 배꼽 노출은 상의와 레이어를 포함한 결과다.

원문 연결: `SPT04-14` 로라이즈 — Low-rise, `SPT04-15` 하이라이즈 — High-rise

관찰 구성: `bottom_A.waistband`, `wearer_A.navel`, `wearer_A.natural_waist`

관계 설계: `bottom_A.waistband → lies_below → wearer_A.navel`

혼동 경계: 몸 치수 변경·다리 길이 변경·노출량을 수치로 추정하지 않는다.

관찰 조건: 허리단과 해당 몸 기준점 또는 명시한 다른 기준선이 함께 보임

적용 속성 제안: `wardrobe.bottom.waistband_height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

기존 검토 이웃: `bundle:y2kr_bundle_pop_denim`, `profile:sw_midlowrise`, `profile:y2kr_crop_low`, `profile:y2kr_low_cargo`, `profile:y2kr_low_rise`

후보 초안:

- `SPR_DRAFT_SF038_01` (SPT04-14): The trouser waistband sits below the same wearer's navel.
- `SPR_DRAFT_SF038_02` (SPT04-15): The trouser waistband rises above the same wearer's navel.

## SF039 사이드붑·언더붑

옆 또는 아래 가슴의 피부가 해당 옷 경계 밖에 보이는 결과다. 구조·포즈·아래층과 연결해서 해석한다.

원문 연결: `SPT04-16` 사이드붑† — Sideboob, `SPT04-17` 언더붑† — Underboob

관찰 구성: `adult_wearer_A.skin_region`, `top_A.coverage_edge`

관계 설계: `top_A.coverage_edge → bounds_visible_region_of → adult_wearer_A.skin_region`

혼동 경계: 큰 암홀·언더버스트 코르셋·절개·그림자만으로 해당 노출을 확정하지 않는다. 원문 명칭은 유지한다.

관찰 조건: 성인 문맥과 정확한 피부 위치·같은 의복 경계·아래층 상태가 모두 읽혀야 함

적용 속성 제안: `wardrobe.coverage.side_breast`, `wardrobe.coverage.lower_breast` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Vogue Korea — 언더붑 스타일링](https://www.vogue.co.kr/2022/05/18/%EC%85%80%EB%9F%BD%EC%9D%98-%EC%96%B8%EB%8D%94%EB%B6%91-%EC%8A%A4%ED%83%80%EC%9D%BC%EB%A7%81/)

기존 검토 이웃: `profile:pfe_lateral_chest`, `slot:garment_detail:pfe_lateral_chest_candidate`, `profile:pfe_lower_chest`, `slot:garment_detail:pfe_lower_chest_candidate`

후보 초안:

- `SPR_DRAFT_SF039_01` (SPT04-16): The side edge of the adult subject's top leaves a small lateral breast region visible.
- `SPR_DRAFT_SF039_02` (SPT04-17): The lower edge of the adult subject's top leaves a small underside breast region visible.

## SF040 미니·미디·맥시 길이

무릎·종아리·발목과 밑단의 상대 위치를 저장한다. 고정 센티미터 기준과 브랜드 공통 micro 경계는 없다.

원문 연결: `SPT05-01` 미니스커트 — Miniskirt, `SPT05-02` 마이크로 미니 — Micro-mini, `SPT05-03` 미디스커트 — Midi skirt, `SPT05-04` 맥시스커트 — Maxi skirt

관찰 구성: `skirt_A.hem`, `wearer_A.knees`, `wearer_A.ankles`

관계 설계: `skirt_A.hem → lies_relative_to → wearer_A.leg_landmarks`

혼동 경계: 긴 길이와 피부 가림은 다른 축이다. 신체 비율을 바꾸지 않는다.

관찰 조건: 밑단과 두 다리 기준점이 보이며 구도 크롭이면 미관찰

적용 속성 제안: `wardrobe.skirt.hem_height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — Skirt Silhouettes](https://blog.moodfabrics.com/all-about-skirt-silhouettes/)

기존 검토 이웃: `slot:wardrobe_style:casual_bomber_jacket_miniskirt`, `profile:pfe_mini_outer_leg`, `profile:y2kr_micro_mini`, `slot:garment_detail:y2kr_micro_mini`, `slot:subject_framing:pfe_mini_outer_leg_candidate`

후보 초안:

- `SPR_DRAFT_SF040_01` (SPT05-01): The skirt hem ends above the same wearer's knees.
- `SPR_DRAFT_SF040_02` (SPT05-03): The skirt hem falls below the knees and above the ankles.
- `SPR_DRAFT_SF040_03` (SPT05-04): The skirt hem reaches near the ankles.
- `SPR_DRAFT_SF040_04` (SPT05-02): A very short skirt hem ends high along the thighs of the adult wearer.

## SF041 슬릿 위치·높이·개수

분리된 직물 경계의 시작점·양변·위치와 수를 저장한다. 하이스릿은 전체 길이와 독립이다.

원문 연결: `SPT05-05` 하이 슬릿 — High slit, `SPT05-06` 사이드 슬릿 — Side slit, `SPT05-07` 프런트 슬릿 — Front slit, `SPT05-08` 더블 슬릿 — Double slit

관찰 구성: `skirt_A.slit_edges`, `skirt_A.slit_upper_endpoint`, `wearer_A.thigh`

관계 설계: `skirt_A.slit_edges → separate_below → skirt_A.slit_upper_endpoint`

혼동 경계: 접힌 주름·랩 앞판·찢김·인쇄된 검은 선과 구분한다.

관찰 조건: 선택된 위치·수·시작점과 양변, 아래층 또는 다리가 읽힘

적용 속성 제안: `wardrobe.skirt.slit_location`, `wardrobe.skirt.slit_height`, `wardrobe.skirt.slit_count` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Faux Wrap Skirt](https://www.seamwork.com/sewing-patterns/pattern-hacks-how-to-draft-a-faux-wrap-skirt)

기존 검토 이웃: `profile:pfe_slit`, `slot:garment_detail:pfe_slit_candidate`, `bundle:hw_dangui_open_sides`, `profile:clothing_ct061_v1`, `profile:clothing_ct140_v2`

후보 초안:

- `SPR_DRAFT_SF041_01` (SPT05-05): A slit in the long skirt begins high along the thigh while the surrounding skirt stays continuous.
- `SPR_DRAFT_SF041_02` (SPT05-06): A single slit opens along the skirt side.
- `SPR_DRAFT_SF041_03` (SPT05-08): Two distinct slits open in the same skirt.
- `SPR_DRAFT_SF041_04` (SPT05-07): A slit opens along the front center of the same skirt.

## SF042 랩·사롱 스커트

겹치는 앞판과 허리의 고정점·매듭을 저장한다. 걸을 때 벌어짐은 정지 사진의 보편 필수가 아니다.

원문 연결: `SPT05-09` 랩 스커트 — Wrap skirt, `SPT05-10` 사롱 스커트 — Sarong skirt

관찰 구성: `skirt_A.outer_front_panel`, `skirt_A.inner_front_panel`, `skirt_A.waist_knot`

관계 설계: `skirt_A.outer_front_panel → overlaps → skirt_A.inner_front_panel`

혼동 경계: 앞판 사선이 곧 슬릿이 아니다. 실제 조절 가능한 여밈과 고정 포 랩을 분리한다.

관찰 조건: 두 판의 가장자리·층 순서·고정 또는 매듭의 출발점 확인

적용 속성 제안: `wardrobe.skirt.overlap`, `wardrobe.skirt.closure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Faux Wrap Skirt](https://www.seamwork.com/sewing-patterns/pattern-hacks-how-to-draft-a-faux-wrap-skirt)

기존 검토 이웃: `profile:clothing_ct018_v1`, `profile:wrap_skirt_overlap_closure`, `slot:wardrobe_style:clt_ct018_v1`, `slot:wardrobe_style:simple_top_wrap_skirt_ensemble`, `slot:garment_detail:wrap_skirt_diagonal_overlap_closure`

후보 초안:

- `SPR_DRAFT_SF042_01` (SPT05-09): One front skirt panel crosses over the other and attaches at the waist.
- `SPR_DRAFT_SF042_02` (SPT05-10): The sarong-style skirt wraps around the hips and ties in a visible side knot.

## SF043 비대칭·하이로 밑단

앞뒤 또는 좌우 높이 차이를 개별 변형으로 기록한다. 비대칭 모두가 앞짧뒤길인 것은 아니다.

원문 연결: `SPT05-11` 비대칭·하이로 헴 — Asymmetric / High-low hem

관찰 구성: `skirt_A.front_hem`, `skirt_A.back_hem`

관계 설계: `skirt_A.front_hem → lies_above → skirt_A.back_hem`

혼동 경계: 카메라 투시·포즈로 생긴 차이와 의복 재단 차이를 구별한다.

관찰 조건: 같은 옷의 앞뒤 또는 선택된 좌우 가장자리가 둘 다 읽힘

적용 속성 제안: `wardrobe.hem.height_distribution` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — Skirt Silhouettes](https://blog.moodfabrics.com/all-about-skirt-silhouettes/)

기존 검토 이웃: `profile:aeolian_dune_stoss_crest_slipface_transport`, `profile:asymmetric_counterbalance_relation`, `profile:black_hole_shadow_reconstruction`, `profile:chrh_rel_hair_cut_asymmetric_bob`, `profile:cme_coronagraph_snapshot`

후보 초안:

- `SPR_DRAFT_SF043_01` (SPT05-11): The skirt front hem is shorter than the back hem on the same garment.

## SF044 플리츠 미니·펜슬

주름 구조와 좁은 치마 폭은 다른 변수다. 한 옷에 동시에 성립할 수 있다.

원문 연결: `SPT05-12` 플리츠 미니 — Pleated mini, `SPT05-13` 펜슬 스커트 — Pencil skirt

관찰 구성: `skirt_A.pleat_folds`, `skirt_A.outer_contour`

관계 설계: `skirt_A.pleat_folds → repeat_along → skirt_A.waist_to_hem`

혼동 경계: 플리츠 때문에 길이·슬릿·학교 역할을 자동 추가하지 않는다.

관찰 조건: 접힘 반복 또는 같은 몸 기준점에 따른 외곽 폭 확인

적용 속성 제안: `wardrobe.skirt.pleats`, `wardrobe.skirt.width_distribution` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering)

기존 검토 이웃: `profile:y2kr_pleated_mini`, `slot:garment_detail:y2kr_pleated_mini`, `slot:wardrobe_style:business_blouse_pencil_skirt`, `slot:wardrobe_style:ctx_c135`

후보 초안:

- `SPR_DRAFT_SF044_01` (SPT05-12): Repeated folded pleats run from the waist toward the short skirt hem.
- `SPR_DRAFT_SF044_02` (SPT05-13): The skirt stays narrow along the hips and thighs before ending near the knees.

## SF045 버블·튤립 스커트

둥근 외곽의 부피와 말아 들어간 밑단 또는 겹친 꽃잎형 앞판을 구분한다.

원문 연결: `SPT05-14` 버블 스커트 — Bubble skirt, `SPT05-15` 튤립 스커트 — Tulip skirt

관찰 구성: `skirt_A.puffed_shell`, `skirt_A.turned_hem`, `skirt_A.overlap_panels`

관계 설계: `skirt_A.puffed_shell → curves_into → skirt_A.turned_hem`

혼동 경계: 둥근 골반 신체를 새로 만들지 않는다. 넓은 A라인만으로 버블이 아니다.

관찰 조건: 부피 전환과 실제 밑단 또는 겹친 두 앞판의 경계 확인

적용 속성 제안: `wardrobe.skirt.volume`, `wardrobe.skirt.hem_construction` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — Skirt Silhouettes](https://blog.moodfabrics.com/all-about-skirt-silhouettes/), [Mood — Erica Bubble Skirt Pattern](https://blog.moodfabrics.com/the-erica-skirt-free-sewing-pattern/)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF045_01` (SPT05-14): The skirt shell balloons outward then turns inward at its gathered hem.
- `SPR_DRAFT_SF045_02` (SPT05-15): Two curved front skirt panels overlap like petals toward the hem.

## SF046 스코트

겉 치마판과 안쪽 두 바짓단은 서로 다른 층·분기다. 정면 외관만으로 내부 쇼츠가 증명되지 않는다.

원문 연결: `SPT05-16` 스코트 — Skort

관찰 구성: `skort_A.skirt_panel`, `skort_A.inner_shorts`, `skort_A.leg_branches`

관계 설계: `skort_A.skirt_panel → overlies → skort_A.inner_shorts`

혼동 경계: 치마+별도 속바지와 일체형 여부는 제품 명세가 필요하다.

관찰 조건: 치마판과 두 쇼츠 개구부가 동일 하의에 결속됨; 안이 안 보이면 명세만 유지

적용 속성 제안: `wardrobe.bottom.layer_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Jalie — LOULOUXE Sporty Skort](https://jalie.com/products/loulouxe-sport-skort-sewing-pattern)

기존 검토 이웃: `profile:active_skort_outer_skirt_inner_shorts`, `slot:garment_detail:skort_outer_panel_inner_shorts`, `slot:wardrobe_style:court_skort_racerback_top_ensemble`, `profile:costume_ccx_cc22_01`, `profile:costume_ccx_cc22_02`

후보 초안:

- `SPR_DRAFT_SF046_01` (SPT05-16): A skirt panel overlaps the front while two separate shorts hems remain visible beneath it.

## SF047 짧은 쇼츠·컷오프

두 다리 분기와 끝점·밑단 가공을 저장한다. hot pants와 micro의 수치 경계는 가변이다.

원문 연결: `SPT05-17` 핫팬츠·쇼트 쇼츠 — Hot pants / Short shorts, `SPT05-18` 마이크로 쇼츠† — Micro shorts, `SPT05-19` 데님 컷오프 — Denim cutoffs

관찰 구성: `shorts_A.left_hem`, `shorts_A.right_hem`, `shorts_A.frayed_edge`

관계 설계: `shorts_A.frayed_edge → follows → shorts_A.leg_hems`

혼동 경계: 프레이드는 보이는 상태이며 실제 바지를 잘라 만든 이력을 증명하지 않는다.

관찰 조건: 두 바지 개구부·끝점 또는 올풀림이 원단 경계에 붙음

적용 속성 제안: `wardrobe.shorts.length`, `wardrobe.hem.finish` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `slot:silhouette_proportion:biker_short_thigh_knee_landmark`, `slot:silhouette_proportion:micro_short_proportion`

후보 초안:

- `SPR_DRAFT_SF047_01` (SPT05-17): Two short trouser legs end high on the thighs.
- `SPR_DRAFT_SF047_02` (SPT05-19): The denim shorts have uneven frayed threads along both cut-looking hems.
- `SPR_DRAFT_SF047_03` (SPT05-18): Very short trouser legs end near the top of each thigh.

## SF048 돌핀·바이커 쇼츠

옆으로 올라가는 곡선 끝단과 허벅지를 따르는 밀착은 별도다. 대비 파이핑은 선택 변형이다.

원문 연결: `SPT05-20` 돌핀 쇼츠 — Dolphin shorts, `SPT05-21` 바이커 쇼츠 — Biker shorts

관찰 구성: `shorts_A.side_hem`, `shorts_A.front_hem`, `shorts_A.thigh_panel`

관계 설계: `shorts_A.side_hem → curves_above → shorts_A.front_hem`

혼동 경계: 운동복이라는 이름으로 운동 능력·압박 성능을 붙이지 않는다.

관찰 조건: 끝단의 상대 높이 또는 두 다리의 직물 접촉과 연속성 확인

적용 속성 제안: `wardrobe.shorts.hem_contour`, `wardrobe.shorts.fit` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

기존 검토 이웃: `slot:silhouette_proportion:biker_short_thigh_knee_landmark`, `profile:cycling_bib_shorts_strap_pad_continuity`, `profile:exercise_dress_integrated_short_liner`

후보 초안:

- `SPR_DRAFT_SF048_01` (SPT05-20): The shorts hems curve upward at the sides with a distinct bound edge.
- `SPR_DRAFT_SF048_02` (SPT05-21): The shorts fabric follows both thighs closely to mid-thigh.

## SF049 버뮤다·카프리·퀼로트

길이의 몸 기준점과 두 다리의 폭·분기를 나눈다. 스커트처럼 보여도 다리 분기는 유지한다.

원문 연결: `SPT05-22` 버뮤다 쇼츠 — Bermuda shorts, `SPT05-23` 카프리 팬츠 — Capri pants, `SPT05-24` 퀼로트 — Culottes

관찰 구성: `pants_A.leg_hems`, `wearer_A.knees`, `pants_A.leg_branch`

관계 설계: `pants_A.leg_hems → lie_relative_to → wearer_A.leg_landmarks`

혼동 경계: 카프리·퀼로트에 국제 공통 길이와 고정 폭을 강제하지 않는다.

관찰 조건: 하의 분기·두 밑단·요청된 몸 기준점 확인

적용 속성 제안: `wardrobe.pants.length`, `wardrobe.pants.leg_width` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `slot:wardrobe_style:fitted_top_bermuda_slim_belt_ensemble`, `profile:capri_trouser_below_knee_clear_ankle_gap`, `slot:silhouette_proportion:bermuda_two_knee_length_short_hems`, `slot:silhouette_proportion:casual_capri_below_knee_clear_ankle_gap`, `slot:wardrobe_style:capri_cropped_windbreaker`

후보 초안:

- `SPR_DRAFT_SF049_01` (SPT05-22): The shorts end near the knees.
- `SPR_DRAFT_SF049_02` (SPT05-23): The trousers end around the calf area.
- `SPR_DRAFT_SF049_03` (SPT05-24): Two wide trouser legs flare separately from the same lower-body garment.

## SF050 밀착·스키밍·밴디지

몸과 직물의 지역 접촉·떨어짐을 저장한다. 밴디지는 띠 구성의 외형이고 압박 성능은 별도다.

원문 연결: `SPT06-01` 피티드 — Fitted, `SPT06-02` 슬림핏 — Slim fit, `SPT06-03` 보디콘 — Bodycon, `SPT06-04` 스킨타이트 — Skin-tight, `SPT06-05` 보디 스키밍 — Body-skimming, `SPT06-06` 밴디지 드레스 — Bandage dress

관찰 구성: `dress_A.surface`, `wearer_A.torso`, `dress_A.band_panels`

관계 설계: `dress_A.surface → follows_contour_of → wearer_A.torso`

혼동 경계: 밀착=노출·신축률·압박력·몸 수치 변경이 아니다.

관찰 조건: 해당 옷의 부위별 접촉과 주름·띠 경계를 구분; 기능은 미채점

적용 속성 제안: `wardrobe.fit.local_contact`, `wardrobe.bodice.band_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [The Met — Extreme Beauty: The Body Transformed](https://www.metmuseum.org/press-releases/extreme-beauty-the-body-transformed-2001-exhibitions)

기존 검토 이웃: `profile:clothing_ct005_v2`, `profile:y2kr_baby_tee`, `slot:wardrobe_style:clt_ct005_v2`, `slot:wardrobe_style:contemporary_heisei_y2k_layers`, `slot:wardrobe_style:fitted_tank_capri_low_profile_flat_ensemble`

후보 초안:

- `SPR_DRAFT_SF050_01` (SPT06-01, SPT06-02): The garment follows the torso with limited visible space at the waist.
- `SPR_DRAFT_SF050_02` (SPT06-03, SPT06-04): The dress fabric closely follows the bust, waist and hip contours.
- `SPR_DRAFT_SF050_03` (SPT06-05): The dress skims the torso with small soft folds rather than a taut surface.
- `SPR_DRAFT_SF050_04` (SPT06-06): Broad band-like panels form repeated horizontal divisions across the fitted dress.

## SF051 아워글라스·허리 조임

옷 외곽의 상대 폭과 벨트·끈·절개 등 수축 장치를 분리한다.

원문 연결: `SPT06-07` 아워글라스 — Hourglass silhouette, `SPT06-08` 신치드 웨이스트 — Cinched waist

관찰 구성: `dress_A.waist_contour`, `dress_A.upper_and_hip_contours`, `belt_A`

관계 설계: `dress_A.waist_contour → is_narrower_than → dress_A.upper_and_hip_contours`

혼동 경계: 몸 자체 치수·과장된 가슴·힙 증가를 추가하지 않는다.

관찰 조건: 동일 의복 외곽 폭과 선택된 조임 장치가 읽힘

적용 속성 제안: `wardrobe.silhouette.width_distribution`, `wardrobe.waist.gathering` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [The Met — Extreme Beauty: The Body Transformed](https://www.metmuseum.org/press-releases/extreme-beauty-the-body-transformed-2001-exhibitions)

기존 검토 이웃: `profile:bottom_hourglass_silhouette_relation`, `profile:hourglass_silhouette_relation`, `profile:soft_full_figure_volume`, `profile:top_hourglass_silhouette_relation`, `slot:silhouette_proportion:bottom_hourglass_relation`

후보 초안:

- `SPR_DRAFT_SF051_01` (SPT06-07): The garment silhouette narrows at the waist between fuller upper and hip regions.
- `SPR_DRAFT_SF051_02` (SPT06-08): A belt gathers the same dress fabric inward at the natural waist.

## SF052 A라인·핏앤플레어

폭이 밑단 쪽으로 늘어나는 것과 맞는 몸판-퍼지는 치마의 전환은 독립이다.

원문 연결: `SPT06-09` A라인 — A-line, `SPT06-10` 핏앤플레어 — Fit-and-flare

관찰 구성: `dress_A.bodice`, `dress_A.waist_join`, `dress_A.skirt`

관계 설계: `dress_A.skirt → widens_below → dress_A.waist_join`

혼동 경계: 허리 조임이 없는 A라인도 가능하다. 상체 밀착을 자동 추가하지 않는다.

관찰 조건: 퍼짐 시작점과 위아래 폭의 관계 확인

적용 속성 제안: `wardrobe.silhouette.flare_start`, `wardrobe.silhouette.width_distribution` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [The Met — Extreme Beauty: The Body Transformed](https://www.metmuseum.org/press-releases/extreme-beauty-the-body-transformed-2001-exhibitions)

기존 검토 이웃: `profile:chrh_rel_hair_cut_a_line`, `slot:hair_style:chrh_hair_cut_a_line`, `slot:wardrobe_style:one_piece_a_line_dress`, `bundle:chrh_bundle_chrh_hair_cut_a_line`, `profile:hogarth_waving_line_of_beauty`

후보 초안:

- `SPR_DRAFT_SF052_01` (SPT06-09): The skirt widens gradually from its upper edge toward the hem.
- `SPR_DRAFT_SF052_02` (SPT06-10): A fitted bodice joins a skirt that flares outward below the waist.

## SF053 시스·컬럼·머메이드

몸을 따라가는 정도와 하부 퍼짐 시작점이 핵심이다. 브랜드 명칭보다 실제 외곽을 저장한다.

원문 연결: `SPT06-11` 시스·컬럼 — Sheath / Column, `SPT06-12` 머메이드 — Mermaid

관찰 구성: `dress_A.hip_region`, `dress_A.lower_flare`, `dress_A.outer_contour`

관계 설계: `dress_A.lower_flare → widens_below → dress_A.narrow_upper_skirt`

혼동 경계: mermaid 신화 캐릭터·물고기 꼬리를 의복에 넣지 않는다. 퍼짐 위치는 선택된 변형일 뿐이다.

관찰 조건: 몸판·힙·퍼짐 시작점·밑단 전체가 읽힘

적용 속성 제안: `wardrobe.silhouette.flare_start`, `wardrobe.silhouette.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [The Met — Extreme Beauty: The Body Transformed](https://www.metmuseum.org/press-releases/extreme-beauty-the-body-transformed-2001-exhibitions)

기존 검토 이웃: `bundle:intellectual_ia_comparison_matrix`, `profile:architectural_threshold_frame_depth_relation`, `profile:electric_constricted_arc_bridge_relation`, `profile:electric_tesla_coil_terminal_streamers_relation`, `profile:electric_welding_arc_and_spatter_relation`

후보 초안:

- `SPR_DRAFT_SF053_01` (SPT06-11): The dress falls in a nearly straight vertical outline along the torso and legs.
- `SPR_DRAFT_SF053_02` (SPT06-12): The dress follows the hips and upper legs, then flares outward below the knees.

## SF054 엠파이어·드롭 웨이스트

몸 기준선에 대한 의복의 치마 연결선 위치다. 가슴 아래 봉제 모두가 엠파이어는 아니다.

원문 연결: `SPT06-13` 엠파이어 웨이스트 — Empire waist, `SPT06-14` 드롭 웨이스트 — Drop waist

관찰 구성: `dress_A.skirt_join`, `wearer_A.underbust`, `wearer_A.natural_waist`

관계 설계: `dress_A.skirt_join → lies_relative_to → wearer_A.natural_waist`

혼동 경계: 높은 바지 허리선과 드레스 치마 시작선을 혼동하지 않는다.

관찰 조건: 연결선과 치마 시작, 같은 몸의 기준점 확인

적용 속성 제안: `wardrobe.waist_seam.height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Jovani — Empire Waist Dress](https://www.jovani.com/blog/fashion-and-style-tips/empire-waist-dress/)

기존 검토 이웃: `profile:hw_empire_raised_waist`, `slot:garment_detail:hw_empire_raised_waist_1`, `slot:garment_detail:hw_empire_raised_waist_2`, `profile:hw_drop_waist_1920`, `slot:costume_style:hw_drop_waist_1920_2`

후보 초안:

- `SPR_DRAFT_SF054_01` (SPT06-13): The skirt joins the bodice directly below the bust and falls from that raised seam.
- `SPR_DRAFT_SF054_02` (SPT06-14): The skirt joins the long bodice below the natural waist.

## SF055 페플럼·오버사이즈·박시

허리 부착 짧은 퍼짐, 지역 여유, 직선 외곽은 별도 변수다.

원문 연결: `SPT06-15` 페플럼 — Peplum, `SPT06-16` 오버사이즈·박시핏 — Oversized / Boxy fit

관찰 구성: `top_A.waist_flounce`, `top_A.body_panels`, `wearer_A.waist`

관계 설계: `top_A.waist_flounce → attaches_at → top_A.waist_edge`

혼동 경계: 모든 오버사이즈가 박시하지 않다. 페플럼이 몸 골반의 볼륨을 증명하지 않는다.

관찰 조건: 부착선·자유 끝 또는 동일 옷의 공간과 외곽을 확인

적용 속성 제안: `wardrobe.peplum.connection`, `wardrobe.fit.local_ease`, `wardrobe.silhouette.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Tilly and the Buttons — Dominique Pattern Hacks](https://tillyandthebuttons.com/blogs/sewing/dominique-pattern-hacks)

기존 검토 이웃: `profile:clothing_ct005_v1`, `slot:silhouette_proportion:architectural_peplum`, `slot:wardrobe_style:clt_ct005_v1`, `profile:clothing_ct005_v2`, `slot:wardrobe_style:clt_ct005_v2`

후보 초안:

- `SPR_DRAFT_SF055_01` (SPT06-15): A short flared fabric extension attaches around the top waist.
- `SPR_DRAFT_SF055_02` (SPT06-16): The top side panels fall in a broad straight outline with visible space beside the torso.

## SF056 파인 게이지·골지

작은 루프의 밀도와 세로 융기 골은 서로 다른 편직 속성이다. 둘이 함께 가능하다.

원문 연결: `SPT07-01` 파인 게이지 니트 — Fine-gauge knit, `SPT07-02` 리브 니트·골지 — Rib knit

관찰 구성: `knit_top_A.loops`, `knit_top_A.ribs`

관계 설계: `knit_top_A.ribs → repeat_along → knit_top_A.vertical_surface`

혼동 경계: 잔주름·스트라이프 프린트가 골지는 아니다. fine gauge를 고정 게이지 수치로 추정하지 않는다.

관찰 조건: 같은 원단 면에서 루프 또는 골의 입체 반복이 원본 해상도로 식별됨

적용 속성 제안: `wardrobe.textile.loop_scale`, `wardrobe.textile.rib_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: `profile:clothing_ct087_v1`, `slot:surface_material:clt_ct087_v1`, `slot:surface_material:rib_knit_stretch_recovery_surface`, `slot:surface_material:sff_pro_t15`

후보 초안:

- `SPR_DRAFT_SF056_01` (SPT07-01): The knit top surface shows small closely spaced loops.
- `SPR_DRAFT_SF056_02` (SPT07-02): Raised vertical ribs repeat across the same knit top.

## SF057 포인텔·오픈워크

바탕 편직 안의 반복 작은 구멍과 더 넓은 열린 조직을 구분한다. 아래층은 별도다.

원문 연결: `SPT07-03` 포인텔 니트 — Pointelle knit, `SPT07-04` 오픈워크 니트 — Openwork knit

관찰 구성: `knit_top_A.open_loops`, `knit_top_A.solid_loop_field`, `inner_A`

관계 설계: `knit_top_A.open_loops → repeat_within → knit_top_A.solid_loop_field`

혼동 경계: 물방울 프린트·레이스·촬영 노이즈와 다르다. 포인텔=맨살 노출이라는 의무를 만들지 않는다.

관찰 조건: 구멍 경계가 실의 연결로 이루어지고 아래층의 표면과 구분됨

적용 속성 제안: `wardrobe.textile.openwork_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF057_01` (SPT07-03): Small eyelet-like holes repeat in a geometric pattern within the knitted top surface.
- `SPR_DRAFT_SF057_02` (SPT07-04): Larger open stitches leave visible gaps between the yarn paths.

## SF058 크로셰 모티프

코바늘 공정 명세와 루프·모티프의 보이는 연결을 구분한다. 제작 방식 자체를 사진으로 단정하지 않는다.

원문 연결: `SPT07-05` 크로셰 톱 — Crochet top

관찰 구성: `top_A.loop_motifs`, `top_A.motif_joins`

관계 설계: `top_A.loop_motifs → connect_through → top_A.motif_joins`

혼동 경계: 일반 니트·자수 꽃·레이스 문양·크로셰처럼 보이는 기계 생산물의 제작 이력을 구분한다.

관찰 조건: 실 경로와 모티프 사이 실제 연결을 원본 해상도로 확인

적용 속성 제안: `wardrobe.textile.motif_connection`, `metadata.textile.process` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF058_01` (SPT07-05): Looped floral motifs on the top are joined by open yarn bridges.

## SF059 카디건·크롭·랩

앞의 열린 여밈과 몸판 길이 및 교차 여밈을 별도로 저장한다.

원문 연결: `SPT07-06` 카디건 — Cardigan, `SPT07-07` 크롭 카디건 — Cropped cardigan, `SPT07-08` 랩 카디건 — Wrap cardigan

관찰 구성: `cardigan_A.front_edges`, `cardigan_A.hem`, `cardigan_A.wrap_tie`

관계 설계: `cardigan_A.front_edges → separate_at → cardigan_A.open_placket`

혼동 경계: 카디건 이름만으로 열린 상태·배꼽 노출·안쪽 브라를 추가하지 않는다.

관찰 조건: 각 변형의 여밈 가장자리·밑단·매듭을 해당 카디건에 결속

적용 속성 제안: `wardrobe.cardigan.closure`, `wardrobe.cardigan.length` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: `profile:y2kr_crop_cardigan`, `slot:costume_style:librarian_cardigan_formal`, `slot:garment_detail:cardigan_pilling_detail`, `slot:hand_pose:adjusting_collar`, `slot:wardrobe_style:knit_cardigan_jeans`

후보 초안:

- `SPR_DRAFT_SF059_01` (SPT07-06): The cardigan has separate front edges with visible button and buttonhole bands.
- `SPR_DRAFT_SF059_02` (SPT07-07): The cardigan hem ends near the waist.
- `SPR_DRAFT_SF059_03` (SPT07-08): The cardigan front panels cross and tie at the waist.

## SF060 트윈세트

안쪽 톱과 카디건은 두 개의 의복이다. 색·원단을 공유하되 완전히 합치지 않는다.

원문 연결: `SPT07-09` 트윈세트 — Twinset

관찰 구성: `inner_knit_A`, `cardigan_A`

관계 설계: `cardigan_A → is_layered_over → inner_knit_A`

혼동 경계: 한 벌처럼 인쇄된 레이어·서로 다른 셔츠 세트를 동일 소재라고 추론하지 않는다.

관찰 조건: 두 옷의 경계·층 순서·선택된 색/조직 대응이 읽힘

적용 속성 제안: `wardrobe.layer.order`, `wardrobe.layer.matching_surface` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF060_01` (SPT07-09): A separate knit top sits beneath a cardigan with a matching visible knit texture and color.

## SF061 볼레로·슈러그

짧은 겉몸판과 어깨·팔 중심의 덮음 범위를 저장한다. 유통 명칭 경계는 가변이다.

원문 연결: `SPT07-10` 볼레로 — Bolero, `SPT07-11` 슈러그 — Shrug

관찰 구성: `outer_A.shoulder_cover`, `outer_A.body_hem`, `inner_top_A`

관계 설계: `outer_A.shoulder_cover → overlies → inner_top_A.shoulder_region`

혼동 경계: 짧은 옷이라고 크롭 톱·카디건과 같은 형태가 아니다.

관찰 조건: 겉옷과 안쪽 옷 경계, 어깨 연결·몸판 유무 확인

적용 속성 제안: `wardrobe.outer.coverage_topology`, `wardrobe.layer.order` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `profile:y2kr_bolero`, `slot:surface_material:lightweight_open_knit_layer_surface`, `slot:wardrobe_style:tank_lightweight_summer_layer_wide_trouser_ensemble`, `slot:wardrobe_style:y2kr_bolero`, `profile:y2kr_shrug`

후보 초안:

- `SPR_DRAFT_SF061_01` (SPT07-10): A short bolero body ends above the waist and frames the separate inner top.
- `SPR_DRAFT_SF061_02` (SPT07-11): The shrug covers the shoulders and arms with only a small back connecting panel.

## SF062 베스트·폴로·베이비 티·헨리

소매 유무·칼라·부분 플래킷·몸판 길이는 각각 독립 구조다. baby tee는 성인 의복 문맥의 이름이다.

원문 연결: `SPT07-12` 니트 베스트 — Knit vest, `SPT07-13` 폴로 니트 — Polo knit, `SPT07-14` 베이비 티† — Baby tee, `SPT07-15` 헨리 톱 — Henley top

관찰 구성: `top_A.collar`, `top_A.short_placket`, `top_A.armhole`, `top_A.hem`

관계 설계: `top_A.short_placket → ends_within → top_A.front_bodice`

혼동 경계: 유아 의복·전면 셔츠 플래킷·레이어 역할과 구별한다.

관찰 조건: 선택된 구조의 끝점과 소유 몸판, 성인 문맥 확인

적용 속성 제안: `wardrobe.collar.presence`, `wardrobe.placket.extent`, `wardrobe.top.length` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: `bundle:y2kr_bundle_pop_denim`, `profile:y2kr_baby_tee`, `profile:y2kr_graphic_baby`, `slot:garment_detail:y2kr_graphic_baby`, `slot:wardrobe_style:y2kr_baby_tee`

후보 초안:

- `SPR_DRAFT_SF062_01` (SPT07-13): A knitted collar joins a short button placket on the polo top.
- `SPR_DRAFT_SF062_02` (SPT07-15): The collarless top has a short button placket ending partway down the front.
- `SPR_DRAFT_SF062_03` (SPT07-14): A fitted short-sleeve tee ends high at the waist on the adult wearer.
- `SPR_DRAFT_SF062_04` (SPT07-12): A sleeveless knit vest has finished armholes and a continuous knitted body.

## SF063 피전트·퍼프 블라우스

모은 목둘레·넉넉한 몸판·풍성한 소매를 독립 분량으로 둔다. 원문 명칭은 선택 범주다.

원문 연결: `SPT07-16` 피전트 블라우스 — Peasant blouse, `SPT07-17` 퍼프 슬리브 블라우스 — Puff-sleeve blouse

관찰 구성: `blouse_A.gathered_neck`, `blouse_A.sleeve_volume`, `blouse_A.cuff`

관계 설계: `blouse_A.sleeve_volume → expands_between → blouse_A.attachment_and_cuff`

혼동 경계: 농촌 배경·민족·직업·아이 연령을 의복에서 추론하지 않는다.

관찰 조건: 실제 모음 고정점과 같은 소매의 부피 위치가 읽힘

적용 속성 제안: `wardrobe.blouse.gathers`, `wardrobe.sleeve.volume_distribution` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering)

기존 검토 이웃: `profile:y2kr_peasant`, `slot:wardrobe_style:y2kr_peasant`

후보 초안:

- `SPR_DRAFT_SF063_01` (SPT07-16): The blouse neck edge gathers into a loose body with softly full sleeves.
- `SPR_DRAFT_SF063_02` (SPT07-17): Fabric gathers at the sleeve head to form a rounded puff above the upper arm.

## SF064 시어 셔츠의 층

셔츠 조직 너머 보이는 표면이 피부인지 안쪽 의복인지 결속한다. 셔츠 몸판과 아래층은 독립이다.

원문 연결: `SPT07-18` 시어 셔츠 — Sheer shirt

관찰 구성: `shirt_A.sheer_surface`, `inner_top_A.edge`, `shirt_A.placket`

관계 설계: `shirt_A.sheer_surface → overlies → inner_top_A`

혼동 경계: 투명도만으로 브라리스나 피부 노출을 확정하지 않는다.

관찰 조건: 겉 셔츠 조직·아래층 경계·가림 순서가 함께 식별됨

적용 속성 제안: `wardrobe.layer.transmission`, `wardrobe.layer.order` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF064_01` (SPT07-18): The sheer shirt texture remains visible over the solid inner top, whose upper edge shows through it.

## SF065 선드레스·티 드레스

사용 상황·역사적 분위기의 유통 범주다. 소매·길이·무늬는 각각 선택해야 한다.

원문 연결: `SPT08-01` 선드레스 — Sundress, `SPT08-02` 티 드레스 — Tea dress

관찰 구성: `dress_A.bodice`, `dress_A.skirt`, `dress_A.straps`

관계 설계: `dress_A.skirt → joins_to → dress_A.bodice`

혼동 경계: 선드레스=가는 끈·민소매만, tea=꽃무늬·단일 길이만으로 정의하지 않는다.

관찰 조건: 요청된 실제 옷 구성만 검사; 편안함·기온·계절 성능은 미채점

적용 속성 제안: `wardrobe.dress.structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Amber Tiered Dress](https://www.seamwork.com/pdf-sewing-patterns/amber-tiered-dirndl-dress)

기존 검토 이웃: `profile:appearance_rel_h027`, `slot:garment_detail:appearance_h027`

후보 초안:

- `SPR_DRAFT_SF065_01` (SPT08-01): A lightweight dress has broad shoulder straps and a gathered skirt.
- `SPR_DRAFT_SF065_02` (SPT08-02): A day dress combines a shaped waist with a softly falling skirt.

## SF066 슬립·캐미 드레스

얇은 끈과 드레스 몸판의 연결, 표면 광택과 처짐을 독립 변수로 둔다.

원문 연결: `SPT08-03` 슬립 드레스 — Slip dress, `SPT08-04` 캐미 드레스 — Cami dress

관찰 구성: `dress_A.thin_straps`, `dress_A.bodice`, `dress_A.skirt`

관계 설계: `dress_A.thin_straps → attach_to → dress_A.bodice`

혼동 경계: slip=실크·바이어스·시어를 모두 강제하지 않는다. 속옷 착용 여부도 별도다.

관찰 조건: 끈의 부착 양끝·몸판 연속·선택된 표면이 읽힘

적용 속성 제안: `wardrobe.dress.strap_connection`, `wardrobe.textile.drape` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Madeleine Vionnet](https://www.vam.ac.uk/articles/madeleine-vionnet-an-introduction), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: `slot:wardrobe_style:dropwaist_satin_slip_dress`, `slot:wardrobe_style:nineties_slip_dress_layered`, `slot:wardrobe_style:pale_yellow_gauze_slip_dress`, `profile:y2kr_slip`, `slot:wardrobe_style:y2kr_slip`

후보 초안:

- `SPR_DRAFT_SF066_01` (SPT08-03): Thin straps attach to a softly draped dress bodice with a continuous skirt.
- `SPR_DRAFT_SF066_02` (SPT08-04): A camisole-style dress has narrow shoulder straps and a more structured continuous body.

## SF067 랩·포 랩 드레스

겹친 앞판과 실제 여밈 경로를 구분한다. 포 랩은 고정된 겹침의 한 변형이다.

원문 연결: `SPT08-05` 랩 드레스 — Wrap dress, `SPT08-06` 포 랩 — Faux-wrap dress

관찰 구성: `dress_A.crossed_front`, `dress_A.waist_anchor`, `dress_A.fixed_join`

관계 설계: `dress_A.crossed_front → attaches_at → dress_A.waist_anchor`

혼동 경계: 겹침의 외관만으로 풀리는 여밈·조절 가능·벌어짐을 확증하지 않는다.

관찰 조건: 외부 겹침은 관찰; 숨은 여밈 기능은 명세 또는 상세 관찰 필요

적용 속성 제안: `wardrobe.front.overlap`, `wardrobe.closure.topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Faux Wrap Skirt](https://www.seamwork.com/sewing-patterns/pattern-hacks-how-to-draft-a-faux-wrap-skirt)

기존 검토 이웃: `profile:clothing_ct020_v1`, `slot:costume_style:deconstructed_mummy_wrap_dress`, `slot:wardrobe_style:clt_ct020_v1`, `slot:wardrobe_style:one_piece_wrap_dress`, `profile:one_piece_dress_construction`

후보 초안:

- `SPR_DRAFT_SF067_01` (SPT08-05): The dress front panel wraps diagonally across the torso and ties at the waist.
- `SPR_DRAFT_SF067_02` (SPT08-06): Overlapping dress front panels meet a fixed visible join at the waist.

## SF068 셔츠·스목·베이비돌 드레스

칼라와 전면 플래킷, 넉넉한 폭, 높은 몸판-치마 연결 위치를 각각 분리한다.

원문 연결: `SPT08-07` 셔츠 드레스 — Shirt dress, `SPT08-08` 스목 드레스 — Smock dress, `SPT08-09` 베이비돌 드레스 — Babydoll dress

관찰 구성: `dress_A.collar`, `dress_A.full_placket`, `dress_A.high_skirt_join`

관계 설계: `dress_A.skirt → starts_below → dress_A.high_skirt_join`

혼동 경계: babydoll은 성인 의복 이름이며 아이 연령·속옷·짧은 길이 고정 규격을 추가하지 않는다.

관찰 조건: 선택한 칼라/여밈·폭 분포·높은 연결선과 치마의 소유 확인

적용 속성 제안: `wardrobe.dress.placket`, `wardrobe.dress.width_distribution`, `wardrobe.skirt.join_height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Amber Tiered Dress](https://www.seamwork.com/pdf-sewing-patterns/amber-tiered-dirndl-dress)

기존 검토 이웃: `slot:wardrobe_style:clt_ct020_v1`, `slot:wardrobe_style:clt_ct020_v2`, `slot:wardrobe_style:one_piece_shirt_dress`

후보 초안:

- `SPR_DRAFT_SF068_01` (SPT08-07): A shirt collar joins a button placket extending down the dress front.
- `SPR_DRAFT_SF068_02` (SPT08-08): The dress body falls loosely from the shoulders with little waist narrowing.
- `SPR_DRAFT_SF068_03` (SPT08-09): A short full skirt begins at a high seam below the bust.

## SF069 뷔스티에·니트 드레스

상의 몸판 구조와 치마 연결, 편직 재질을 다른 축으로 둔다. 니트 드레스의 핏은 다양하다.

원문 연결: `SPT08-10` 뷔스티에 드레스 — Bustier dress, `SPT08-11` 니트 드레스 — Knit dress

관찰 구성: `dress_A.cup_bodice`, `dress_A.skirt_join`, `dress_A.knit_surface`

관계 설계: `dress_A.cup_bodice → joins_to → dress_A.skirt`

혼동 경계: 브라 톱+별도 스커트가 원피스처럼 보여도 연결 여부는 별도 확인한다.

관찰 조건: 같은 의복의 연결선 또는 조직의 연속 확인

적용 속성 제안: `wardrobe.dress.panel_connection`, `wardrobe.textile.knit_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Natalie Rolt — Elina Bustier](https://www.natalierolt.com/products/elina-bustier), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF069_01` (SPT08-10): A cup-seamed bodice joins a continuous skirt at the waist.
- `SPR_DRAFT_SF069_02` (SPT08-11): The dress surface shows knitted loops along both the torso and skirt.

## SF070 티어드·블레이저 드레스

가로 치마 층 연결과 라펠·재킷형 앞여밈의 연장을 별도로 저장한다.

원문 연결: `SPT08-12` 티어드 드레스 — Tiered dress, `SPT08-13` 블레이저 드레스 — Blazer dress

관찰 구성: `dress_A.skirt_tiers`, `dress_A.tier_joins`, `dress_A.lapels`

관계 설계: `dress_A.skirt_tiers → join_along → dress_A.tier_joins`

혼동 경계: 층 주름과 별도 옷 레이어를 혼동하지 않는다. 재킷 길이만으로 드레스를 확정하지 않는다.

관찰 조건: 각 치마층의 부착선 또는 라펠부터 밑단까지 같은 몸판의 연속 확인

적용 속성 제안: `wardrobe.dress.tier_connections`, `wardrobe.dress.front_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering), [Burberry — Cropped Mayfair Trench Jacket](https://us.burberry.com/cropped-tropical-gabardine-mayfair-trench-jacket-p81264701), [Seamwork — Amber Tiered Dress](https://www.seamwork.com/pdf-sewing-patterns/amber-tiered-dirndl-dress)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF070_01` (SPT08-12): Several gathered skirt tiers join along horizontal seams.
- `SPR_DRAFT_SF070_02` (SPT08-13): Lapels and a double-breasted front continue into a dress-length body.

## SF071 피나포어·에이프런·케이프

겹쳐 입는 앞판·끈과 어깨에서 내려오는 바깥 원단의 연결을 기록한다. 명칭은 겹칠 수 있다.

원문 연결: `SPT08-14` 피나포어 드레스 — Pinafore dress, `SPT08-15` 에이프런 드레스 — Apron dress, `SPT08-16` 케이프 드레스 — Cape dress

관찰 구성: `outer_dress_A.front_panel`, `outer_dress_A.straps`, `dress_A.cape_panel`, `inner_top_A`

관계 설계: `outer_dress_A.front_panel → overlies → inner_top_A`

혼동 경계: 앞치마를 입었다고 특정 직업·순종·배경을 붙이지 않는다.

관찰 조건: 어깨 부착·몸판 범위·소매와 케이프 및 안쪽 옷의 다른 경계 확인

적용 속성 제안: `wardrobe.layer.order`, `wardrobe.dress.overpanel_connection` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `slot:costume_style:akihabara_maid_cafe_uniform`, `slot:costume_style:dirndl_bodice_blouse_skirt_apron_system`

후보 초안:

- `SPR_DRAFT_SF071_01` (SPT08-14, SPT08-15): An apron-style dress front connects to shoulder straps over a separate blouse.
- `SPR_DRAFT_SF071_02` (SPT08-16): A cape panel attaches at the dress shoulders and hangs outside the sleeves.

## SF072 트렌치·크롭·맥 코트

여밈·라펠·뒤 플랩·견장·길이·벨트는 개별 옵션이다. 트렌치 모두에 같은 세트를 강제하지 않는다.

원문 연결: `SPT09-01` 트렌치코트 — Trench coat, `SPT09-02` 크롭 트렌치 — Cropped trench, `SPT09-03` 맥 코트 — Mac coat

관찰 구성: `coat_A.front_panels`, `coat_A.epaulettes`, `coat_A.back_flap`, `coat_A.hem`

관계 설계: `coat_A.back_flap → overlies → coat_A.back_panel`

혼동 경계: 짧은 트렌치에 반드시 허리벨트가 있는 것은 아니다. 방수·방풍 성능은 명세다.

관찰 조건: 선택한 실제 플랩·견장·여밈과 밑단을 같은 겉옷에 결속

적용 속성 제안: `wardrobe.coat.front_structure`, `wardrobe.coat.details`, `wardrobe.coat.length` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Burberry — Cropped Mayfair Trench Jacket](https://us.burberry.com/cropped-tropical-gabardine-mayfair-trench-jacket-p81264701)

기존 검토 이웃: `profile:clothing_ct009_v1`, `slot:costume_style:detective_trench_coat_costume`, `slot:wardrobe_style:clt_ct009_v1`

후보 초안:

- `SPR_DRAFT_SF072_01` (SPT09-01): A double-breasted coat has a separate back storm flap and shoulder tabs.
- `SPR_DRAFT_SF072_02` (SPT09-02): The trench-style jacket retains its front overlap and shoulder tabs above a short hem.
- `SPR_DRAFT_SF072_03` (SPT09-03): A simple raincoat front closes with a clean placket and minimal exterior detail.

## SF073 블레이저의 외부와 내부

어깨 외곽·라펠·길이를 관찰하되 내부 패드·심지·캔버스는 별도 명세로 둔다.

원문 연결: `SPT09-04` 테일러드 블레이저 — Tailored blazer, `SPT09-05` 언스트럭처드 블레이저 — Unstructured blazer, `SPT09-06` 크롭 블레이저 — Cropped blazer

관찰 구성: `blazer_A.lapels`, `blazer_A.shoulder_contour`, `blazer_A.hem`

관계 설계: `blazer_A.lapels → continue_from → blazer_A.front_edges`

혼동 경계: 부드러운 외관이 unlined·unpadded·unstructured를 모두 증명하지 않는다.

관찰 조건: 외부 라펠·어깨·길이만 검사; 숨은 구성은 외부 사진으로 PASS하지 않음

적용 속성 제안: `wardrobe.blazer.contour`, `wardrobe.outer.length`, `metadata.tailoring.internal_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Understanding Ease](https://www.seamwork.com/sewing-tutorials/understanding-ease)

기존 검토 이웃: `slot:garment_detail:visible_bralette_tailored_blazer_layer`, `profile:underwear_as_outerwear_layer_system`, `slot:silhouette_proportion:sculpted_power_shoulders`

후보 초안:

- `SPR_DRAFT_SF073_01` (SPT09-04): The blazer lapels frame an open front with a defined shoulder outline.
- `SPR_DRAFT_SF073_02` (SPT09-05): The blazer falls in soft shoulder folds.
- `SPR_DRAFT_SF073_03` (SPT09-06): The blazer hem ends near the waist above the separate inner top hem.

## SF074 표면·재킷 포켓 구조

트위드는 원단 범주, 트러커·초어·유틸리티는 몸판·포켓 구성이다. 같은 축으로 합치지 않는다.

원문 연결: `SPT09-07` 트위드 재킷 — Tweed jacket, `SPT09-08` 데님·트러커 재킷 — Denim / Trucker jacket, `SPT09-09` 초어·반 재킷 — Chore / Barn jacket, `SPT09-10` 사파리·유틸리티 재킷 — Safari / Utility jacket

관찰 구성: `jacket_A.surface`, `jacket_A.chest_pockets`, `jacket_A.patch_pockets`

관계 설계: `jacket_A.patch_pockets → attach_to → jacket_A.front_panel`

혼동 경계: chore/barn·safari/utility 명칭의 유통 경계는 가변이다. 군인·농부 정체성을 붙이지 않는다.

관찰 조건: 포켓의 붙은 모서리·입구·몸판과 조직이 구분됨

적용 속성 제안: `wardrobe.jacket.pocket_topology`, `wardrobe.textile.surface` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Burberry — Cropped Mayfair Trench Jacket](https://us.burberry.com/cropped-tropical-gabardine-mayfair-trench-jacket-p81264701)

기존 검토 이웃: `slot:costume_style:dark_academia_tweed_outfit`, `slot:wardrobe_style:dark_academia_tweed_outfit`, `bundle:y2kr_bundle_pop_denim`, `profile:clothing_ct086_v1`, `profile:clothing_ct086_v2`

후보 초안:

- `SPR_DRAFT_SF074_01` (SPT09-08): The short denim jacket has two chest pockets and visible front panel seams.
- `SPR_DRAFT_SF074_02` (SPT09-09): The jacket front carries several large patch pockets.
- `SPR_DRAFT_SF074_03` (SPT09-10): Multiple flap pockets and a belt are attached to the utility jacket.
- `SPR_DRAFT_SF074_04` (SPT09-07): The jacket has an irregular textured yarn surface with visible interlacing.

## SF075 블루종·아노락·셔킷·더스터

모아진 끝단, 부분 여밈, 셔츠형 구성, 긴 겉옷 길이를 분해한다. blouson은 bomber보다 넓은 범주다.

원문 연결: `SPT09-11` 보머·블루종 — Bomber / Blouson, `SPT09-12` 윈드브레이커 — Windbreaker, `SPT09-13` 아노락 — Anorak, `SPT09-14` 셔킷 — Shacket, `SPT09-15` 더스터 — Duster

관찰 구성: `jacket_A.gathered_hem`, `jacket_A.body`, `outer_A.partial_placket`, `outer_A.long_hem`

관계 설계: `jacket_A.gathered_hem → draws_in → jacket_A.body`

혼동 경계: 보머의 모든 군용 디테일을 블루종에 강제하지 않는다. 방풍·두께·보온성은 외형으로 확정하지 않는다.

관찰 조건: 선택된 끝단 모음·플래킷 끝점·안팎 길이 차이 확인

적용 속성 제안: `wardrobe.outer.hem_gathering`, `wardrobe.placket.extent`, `wardrobe.layer.length_relation` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:clothing_ct010_v1`, `profile:clothing_ct010_v2`, `profile:sw_tankini`, `slot:wardrobe_style:casual_bomber_jacket_miniskirt`, `slot:wardrobe_style:clt_ct010_v2`

후보 초안:

- `SPR_DRAFT_SF075_01` (SPT09-11): The jacket body billows slightly above a gathered waist hem and cuffs.
- `SPR_DRAFT_SF075_02` (SPT09-13): A hooded outer top has a front opening that stops partway down the body.
- `SPR_DRAFT_SF075_03` (SPT09-15): A lightweight outer layer hangs long below the inner outfit.
- `SPR_DRAFT_SF075_04` (SPT09-12): A light outer jacket has a continuous thin-looking shell and an attached hood.
- `SPR_DRAFT_SF075_05` (SPT09-14): A shirt-like outer layer has a collar, front button placket and patch chest pockets.

## SF076 섬유 성분과 보이는 단서

코튼·리넨·실크·레이온/비스코스는 성분 명세다. 슬럽·광택·주름은 그 자체의 보이는 속성으로 별도 둔다.

원문 연결: `SPT10-01` 코튼 — Cotton, `SPT10-02` 리넨 — Linen, `SPT10-03` 실크 — Silk, `SPT10-04` 레이온·비스코스 — Rayon / Viscose

관찰 구성: `fabric_A.surface`, `fabric_A.composition_spec`

관계 설계: `fabric_A.composition_spec → describes_material_of → fabric_A`

혼동 경계: 광택으로 실크, 슬럽으로 리넨, 부드러움으로 레이온을 확증하지 않는다.

관찰 조건: 성분 자체는 제품 명세·시험 근거 필요; 사진에서 성분 게이트는 미채점

적용 속성 제안: `metadata.textile.fiber_composition` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `profile:hw_lingerie_daydress`, `slot:costume_style:hw_lingerie_daydress_1`, `slot:costume_style:opaque_white_bandage_couture_costume`, `slot:garment_detail:matte_white_bandage_weave`, `slot:garment_detail:opaque_cotton_gauze_wrap_layers`

후보 초안:

- 요청 명세로만 유지하며 정지 이미지 hard 의무를 만들지 않음.

## SF077 얇은 평직·샴브레이

조직·두께·비침과 실 색 배치를 독립적으로 저장한다. 샴브레이와 데님은 같은 청색이어도 조직이 다르다.

원문 연결: `SPT10-05` 포플린 — Poplin, `SPT10-06` 론 — Lawn, `SPT10-07` 보일 — Voile, `SPT10-08` 샴브레이 — Chambray

관찰 구성: `fabric_A.warp`, `fabric_A.weft`, `fabric_A.surface`

관계 설계: `fabric_A.warp → interlaces_with → fabric_A.weft`

혼동 경계: 포플린·론·보일의 모든 상업적 변형을 사진으로 확정하지 않는다. 청색=데님은 아니다.

관찰 조건: 확대에서 실제 실 교차 또는 선택된 투과 외관만 관찰

적용 속성 제안: `wardrobe.textile.visible_weave`, `wardrobe.layer.transmission` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `slot:surface_material:woven_poplin_crisp_fold_surface`, `slot:wardrobe_style:button_down_poplin_shirt_tailored_trousers`, `profile:pf_parterre_axis`, `slot:aesthetic_trend:wetland_hydrology_mosaic_aesthetic`, `slot:location:pf_parterre_axis_location`

후보 초안:

- `SPR_DRAFT_SF077_01` (SPT10-08): The fabric shows differently colored warp and weft crossing in a fine plain-weave surface.
- `SPR_DRAFT_SF077_02` (SPT10-07): A thin woven outer layer softly transmits the color of the inner garment.
- `SPR_DRAFT_SF077_03` (SPT10-05): The shirt cloth has a fine close plain-weave surface.
- `SPR_DRAFT_SF077_04` (SPT10-06): The lightweight blouse cloth shows a very fine even woven surface.

## SF078 시어서커 요철

낮은 면과 반복된 볼록 띠의 표면 차이를 저장한다. 줄무늬 색은 별도다.

원문 연결: `SPT10-09` 시어서커 — Seersucker

관찰 구성: `fabric_A.puckered_strips`, `fabric_A.flatter_strips`

관계 설계: `fabric_A.puckered_strips → alternate_with → fabric_A.flatter_strips`

혼동 경계: 프린트 줄무늬·세탁 주름·봉제 퍼커링을 동일 의미로 합치지 않는다.

관찰 조건: 반복된 높이 차이와 같은 원단 면의 연속을 확인

적용 속성 제안: `wardrobe.textile.relief_pattern` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF078_01` (SPT10-09): Raised puckered strips alternate with flatter strips across the same fabric.

## SF079 시폰·조젯·오간자

투과와 유연한 작은 주름, 잔입자 표면, 형태를 유지하는 얇은 부피를 별도 변형으로 둔다.

원문 연결: `SPT10-10` 시폰 — Chiffon, `SPT10-11` 조젯 — Georgette, `SPT10-12` 오간자 — Organza

관찰 구성: `fabric_A.folds`, `fabric_A.surface`, `fabric_A.free_edge`

관계 설계: `fabric_A.folds → hang_from → fabric_A.attachment`

혼동 경계: 같이 비쳐도 처짐·강성은 다르다. 정확한 섬유·GSM·혼방과 촉감은 사진이 입증하지 않는다.

관찰 조건: 선택된 직물 표면·접힘·부피와 아래층 관계가 함께 읽힘

적용 속성 제안: `wardrobe.textile.fold_scale`, `wardrobe.textile.surface`, `wardrobe.textile.volume` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `profile:clothing_ct091_v1`, `profile:clothing_ct091_v2`, `profile:sheer_garment_optical_layering`, `slot:garment_detail:sff_extra_xa002`, `slot:surface_material:sheer_organza_chiffon_transmission`

후보 초안:

- `SPR_DRAFT_SF079_01` (SPT10-10): The thin translucent fabric falls in small soft folds.
- `SPR_DRAFT_SF079_02` (SPT10-11): The translucent fabric has a fine pebbled matte surface.
- `SPR_DRAFT_SF079_03` (SPT10-12): The thin translucent sleeve holds a rounded volume with crisp folds.

## SF080 튤·레이스·메시

망상 조직의 구멍, 실 문양, 규칙 격자를 구분한다. 피부가 아닌 안감이 밑에 있을 수 있다.

원문 연결: `SPT10-13` 튤 — Tulle, `SPT10-14` 레이스 — Lace, `SPT10-15` 메시 — Mesh

관찰 구성: `fabric_A.mesh_cells`, `fabric_A.thread_motifs`, `lining_A`

관계 설계: `fabric_A.mesh_cells → repeat_across → fabric_A`

혼동 경계: 작은 구멍이 모두 lace·tulle·crochet은 아니다. 셔츠와 피부 조직을 혼동하지 않는다.

관찰 조건: 실 경계·구멍 형태·모티프와 아래층이 원본 해상도에서 읽힘

적용 속성 제안: `wardrobe.textile.open_space_pattern`, `wardrobe.layer.order` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `bundle:costume_b18`, `bundle:egr_arrangement_lace_tulle_layers`, `bundle:egr_micropleated_tulle_panel_bundle`, `profile:clothing_ct090_v1`, `profile:clothing_ct090_v2`

후보 초안:

- `SPR_DRAFT_SF080_01` (SPT10-13): A fine net layer has small repeated mesh cells.
- `SPR_DRAFT_SF080_02` (SPT10-14): Thread motifs form distinct patterned areas separated by open spaces.
- `SPR_DRAFT_SF080_03` (SPT10-15): A regular mesh grid remains visible over the solid lining.

## SF081 새틴·크레이프·저지

조직과 표면 반사·입자·루프를 분리한다. 저지는 편직이고 새틴은 조직 명칭이다.

원문 연결: `SPT10-16` 새틴 — Satin, `SPT10-17` 크레이프 — Crêpe, `SPT10-18` 저지 — Jersey

관찰 구성: `fabric_A.highlights`, `fabric_A.pebbled_surface`, `fabric_A.knit_loops`

관계 설계: `fabric_A.highlights → follow_folds_on → fabric_A`

혼동 경계: 크레이프를 모두 시어로, 새틴을 모두 실크로, 저지를 모두 특정 섬유로 고정하지 않는다.

관찰 조건: 선택된 표면 증거와 실제 직물 경계 확인; 조직 진위는 해상도에 따라 보류

적용 속성 제안: `wardrobe.textile.reflectance`, `wardrobe.textile.surface_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `profile:clothing_ct085_v1`, `profile:clothing_ct085_v2`, `profile:gradient_lip_center_distribution`, `profile:restrained_polished_natural_makeup_balance`, `profile:satin_directional_luster_drape_surface`

후보 초안:

- `SPR_DRAFT_SF081_01` (SPT10-16): Broad soft highlights follow the smooth fabric folds.
- `SPR_DRAFT_SF081_02` (SPT10-17): The cloth surface has a fine irregular pebbled texture.
- `SPR_DRAFT_SF081_03` (SPT10-18): Small knit loops continue across the jersey garment.

## SF082 시어·시스루·세미시어

투과 외관의 정도와 아래층 표면을 묶는다. 명칭은 섬유나 직조 방식 자체가 아니다.

원문 연결: `SPT10-19` 시어 — Sheer, `SPT10-20` 시스루 — See-through, `SPT10-21` 세미시어 — Semi-sheer

관찰 구성: `outer_A.surface`, `inner_A.boundary`

관계 설계: `outer_A.surface → transmits_outline_of → inner_A.boundary`

혼동 경계: 흰 안감·피부색 직물·어두운 그림자가 실제 피부 노출을 뜻하지 않는다.

관찰 조건: 겉 조직과 아래층을 분리해 확인; 조명·겹수·색 변경에 대한 반례 포함

적용 속성 제안: `wardrobe.layer.transmission` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood Fabrics — Fabric Dictionary](https://www.moodfabrics.com/pages/fabric-dictionary)

기존 검토 이웃: `bundle:clothing_b_linen_sheer_layers`, `bundle:fit_ff49_v2_bundle`, `profile:clothing_ct079_v1`, `profile:clothing_ct079_v2`, `profile:clothing_ct091_v1`

후보 초안:

- `SPR_DRAFT_SF082_01` (SPT10-19, SPT10-20): The outer fabric texture stays visible while the inner garment edge shows through it.
- `SPR_DRAFT_SF082_02` (SPT10-21): The outer fabric softly transmits the inner garment color without revealing a sharp inner boundary.

## SF083 드레이프·바이어스

보이는 접힘과 중력 방향, 숨은 실 방향·재단 공정을 분리한다.

원문 연결: `SPT10-22` 드레이프 — Drape, `SPT10-23` 바이어스 컷 — Bias cut

관찰 구성: `fabric_A.folds`, `fabric_A.anchor`, `fabric_A.grain_spec`

관계 설계: `fabric_A.folds → hang_from → fabric_A.anchor`

혼동 경계: 드레이프가 곧 바이어스 재단·실크 성분·특정 탄성이라는 증거는 아니다.

관찰 조건: 고정점·처짐·받치는 몸 또는 바닥의 관계만 관찰; 공정은 별도 명세

적용 속성 제안: `wardrobe.textile.drape`, `metadata.textile.cut_orientation` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Madeleine Vionnet](https://www.vam.ac.uk/articles/madeleine-vionnet-an-introduction)

기존 검토 이웃: `profile:clothing_ct011_v2`, `profile:clothing_ct077_v1`, `profile:nivi_sari_continuous_pleat_pallu_system`, `profile:pfe_cowl`, `slot:action:one_piece_drape_turnaround`

후보 초안:

- `SPR_DRAFT_SF083_01` (SPT10-22): Long soft folds descend from the fabric attachment and settle along the torso.

## SF084 매트·글로시 표면

반사의 폭·세기·배치와 촬영 조명을 분리한다. 소재 이름이나 품질을 자동 결정하지 않는다.

원문 연결: `SPT10-24` 매트·글로시 — Matte / Glossy

관찰 구성: `fabric_A.surface`, `light_A.highlight_footprint`

관계 설계: `light_A.highlight_footprint → appears_on → fabric_A.surface`

혼동 경계: 강한 조명 때문에 생긴 반사와 직물 표면 성질의 증거를 구분한다.

관찰 조건: 비교 시 조명·각도를 고정하고 같은 직물 면에서 반사 변화를 확인

적용 속성 제안: `wardrobe.textile.reflectance` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/)

기존 검토 이웃: `profile:soft_light_shadow_edge_relation`, `profile:soil_rel_e009`, `profile:soil_rel_e096`, `slot:lighting:multi_material_same_source_response`, `slot:lip_finish:high_shine_glossy_lip`

후보 초안:

- `SPR_DRAFT_SF084_01` (SPT10-24): A broad luminous highlight follows the curved fabric surface.
- `SPR_DRAFT_SF084_02` (SPT10-24): The same fabric surface shows subdued diffuse shading without a sharp bright highlight.

## SF085 번아웃·데보레

한 원단 면에서 더 빽빽한 문양과 비치는 바탕이 이어지는 외관이다. 화학 제거 공정은 명세다.

원문 연결: `SPT10-25` 번아웃·데보레 — Burnout / Dévoré

관찰 구성: `fabric_A.dense_motif`, `fabric_A.sheer_ground`

관계 설계: `fabric_A.dense_motif → continues_within → fabric_A.sheer_ground`

혼동 경계: 프린트·아플리케·진짜 개구부와 구분한다. 외관만으로 섬유 제거 이력을 확정하지 않는다.

관찰 조건: 같은 바탕의 연속성·문양의 두께/밀도·투과 차이가 읽힘

적용 속성 제안: `wardrobe.textile.density_pattern`, `metadata.textile.finish_process` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Mood — Burnout Fabrics](https://www.moodfabrics.com/collections/burnout-lasercut-drapery-fabrics)

기존 검토 이웃: `slot:mood:burnout_reset`, `slot:texture:sff_pro_f03`

후보 초안:

- `SPR_DRAFT_SF085_01` (SPT10-25): Dense raised motifs alternate with translucent ground areas on the same fabric panel.

## SF086 개더·루칭·셔링·스모킹

모음 고정점, 장식 주름, 반복 봉제 줄, 장식 스티치의 연결을 다른 구조로 저장한다.

원문 연결: `SPT11-01` 개더 — Gathers, `SPT11-02` 루칭 — Ruching, `SPT11-03` 셔링 — Shirring, `SPT11-04` 스모킹 — Smocking

관찰 구성: `fabric_A.folds`, `fabric_A.anchor_seam`, `fabric_A.stitch_rows`, `fabric_A.embroidery_bridges`

관계 설계: `fabric_A.folds → converge_at → fabric_A.anchor_seam`

혼동 경계: 한국어 셔링이라는 이름에 고무실을 자동 강제하지 않는다. 일반 주름이 스모킹은 아니다.

관찰 조건: 각 선택 변형의 고정점·봉제 줄 또는 장식 스티치가 실제 직물에 연결됨

적용 속성 제안: `wardrobe.folds.anchor_topology`, `wardrobe.stitching.row_pattern` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — A Guide to Shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering)

기존 검토 이웃: `bundle:costume_b26`, `bundle:fit_ff22_v1_bundle`, `bundle:fit_ff37_v2_bundle`, `bundle:hw_chemise_gown_sash`, `profile:appearance_rel_h106`

후보 초안:

- `SPR_DRAFT_SF086_01` (SPT11-01): Small folds converge into a single attachment seam.
- `SPR_DRAFT_SF086_02` (SPT11-02): Decorative folds gather across a selected part of the bodice.
- `SPR_DRAFT_SF086_03` (SPT11-03): Several parallel stitched rows gather the fabric into a repeated narrow band.
- `SPR_DRAFT_SF086_04` (SPT11-04): Decorative stitches link the peaks of gathered folds into a geometric pattern.

## SF087 플리츠 방향과 반복

접힌 방향·반복 폭·맞닿는 두 방향과 펼쳐지는 구조를 저장한다. 주름 가족 전체가 all-of 의무가 아니다.

원문 연결: `SPT11-05` 플리츠 — Pleats, `SPT11-06` 나이프 플리츠 — Knife pleats, `SPT11-07` 박스 플리츠 — Box pleats, `SPT11-08` 아코디언 플리츠 — Accordion pleats

관찰 구성: `skirt_A.fold_edges`, `skirt_A.fold_faces`

관계 설계: `skirt_A.fold_edges → repeat_along → skirt_A.surface`

혼동 경계: 프린트 줄·골지·자연 구김과 구별한다. 실제 열가공 공정을 사진으로 확정하지 않는다.

관찰 조건: 선택된 접힘 방향과 직물 면이 원본 해상도에서 읽힘

적용 속성 제안: `wardrobe.pleats.direction`, `wardrobe.pleats.repeat_scale` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:clothing_ct063_v1`, `profile:sw_pleats`, `slot:garment_detail:clt_ct063_v1`, `slot:garment_detail:pleat_fold_ridge_valley_geometry`, `slot:garment_detail:sw_candidate_pleats`

후보 초안:

- `SPR_DRAFT_SF087_01` (SPT11-06): Parallel pleats lie repeatedly toward the same side.
- `SPR_DRAFT_SF087_02` (SPT11-07): Two opposing folds meet around a broad central pleat face.
- `SPR_DRAFT_SF087_03` (SPT11-08): Narrow repeated pleats fan open toward the skirt hem.
- `SPR_DRAFT_SF087_04` (SPT11-05): Repeated folded sections give the skirt alternating raised edges and recessed faces.

## SF088 핀턱

좁게 접어 봉제한 돌출 선을 저장한다. 원단을 나눠 잇는 절개·인쇄 선과 다르다.

원문 연결: `SPT11-09` 핀턱 — Pintucks

관찰 구성: `blouse_A.narrow_tucks`, `blouse_A.stitch_lines`

관계 설계: `blouse_A.narrow_tucks → follow → blouse_A.stitch_lines`

혼동 경계: 다트의 수렴 끝점·프린세스 절개·레이스 띠를 핀턱으로 부르지 않는다.

관찰 조건: 접힌 작은 능선과 봉제 및 원단의 연속성 확인

적용 속성 제안: `wardrobe.tucks.visible_structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Darts Into Princess Seams](https://www.seamwork.com/sewing-patterns/pattern-hack-turn-darts-into-princess-seams)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF088_01` (SPT11-09): Several very narrow stitched tucks rise along the blouse front.

## SF089 러플·플라운스

부착 경계의 모음과 자유 가장자리의 물결을 구분한다. 기법과 외관이 항상 사진에서 완전히 구분되지는 않는다.

원문 연결: `SPT11-10` 러플·프릴 — Ruffles / Frills, `SPT11-11` 플라운스 — Flounce

관찰 구성: `trim_A.attachment_edge`, `trim_A.free_edge`, `garment_A.base_fabric`

관계 설계: `trim_A.attachment_edge → attaches_to → garment_A.base_fabric`

혼동 경계: 러플·플라운스의 외관이 겹치면 재단 공정을 확증하지 않는다. 소매 부피와도 별도다.

관찰 조건: 고정 경계와 자유 경계를 각각 관찰하고 같은 장식 조각에 결속

적용 속성 제안: `wardrobe.trim.attachment`, `wardrobe.trim.free_edge_contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Seamwork — Create Perfect Gathers](https://www.seamwork.com/sewing-tutorials/gathering), [Tilly and the Buttons — Dominique Pattern Hacks](https://tillyandthebuttons.com/blogs/sewing/dominique-pattern-hacks)

기존 검토 이웃: `slot:costume_absorption_guard:lace_frill_not_fur_guard`, `profile:clothing_ct005_v2`, `profile:clothing_ct065_v2`, `slot:garment_detail:clt_ct065_v2`, `slot:wardrobe_style:clt_ct005_v2`

후보 초안:

- `SPR_DRAFT_SF089_01` (SPT11-10): A gathered fabric strip attaches along one edge while its free edge ripples outward.
- `SPR_DRAFT_SF089_02` (SPT11-11): A curved fabric flounce joins the garment along a smooth attachment edge and widens into waves.

## SF090 레이스 트림·아이렛·스캘럽

붙인 띠·자수 구멍·반복 곡선 끝단을 독립 속성으로 둔다. 금속 아일릿과 자수 아이렛은 다른 문맥이다.

원문 연결: `SPT11-12` 레이스 트림 — Lace trim, `SPT11-13` 아이렛·브로드리 앙글레즈 — Eyelet / Broderie anglaise, `SPT11-14` 스캘럽 에지 — Scalloped edge

관찰 구성: `trim_A.lace_strip`, `fabric_A.embroidered_holes`, `garment_A.scalloped_edge`

관계 설계: `trim_A.lace_strip → attaches_along → garment_A.edge`

혼동 경계: 인쇄된 구멍·단순 투명도·금속 고리를 브로드리 앙글레즈로 대체하지 않는다.

관찰 조건: 원본에서 봉합 경계·구멍 둘레 스티치·선택된 곡선 끝단 확인

적용 속성 제안: `wardrobe.trim.connection`, `wardrobe.embroidery.hole_border`, `wardrobe.edge.contour` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:lace_trim_attached_edge`, `slot:garment_detail:lace_trim_edge`, `slot:wardrobe_style:lace_trim_camisole_wide_denim_ensemble`, `slot:wardrobe_style:lace_trim_tee_satin_skirt`, `profile:y2kr_lace_cami`

후보 초안:

- `SPR_DRAFT_SF090_01` (SPT11-12): A separate lace strip attaches along the garment hem.
- `SPR_DRAFT_SF090_02` (SPT11-13): Small cut-looking holes are surrounded by visible embroidery stitches.
- `SPR_DRAFT_SF090_03` (SPT11-14): The fabric edge repeats in rounded scallops.

## SF091 아플리케·로제트·리본

별도 조각의 부착, 말린 직물의 입체 꽃, 끈의 매듭과 고리를 구분한다. 위치는 반드시 소유자를 가진다.

원문 연결: `SPT11-15` 아플리케 — Appliqué, `SPT11-16` 로제트 — Rosette, `SPT11-17` 보 디테일 — Bow detail

관찰 구성: `applique_A.cut_edge`, `rosette_A.rolled_folds`, `bow_A.loops`, `garment_A.anchor`

관계 설계: `bow_A.loops → join_at → bow_A.knot`

혼동 경계: 꽃 프린트·진짜 꽃·다른 옷의 리본·장식 bow와 기능적 tie를 구분한다.

관찰 조건: 별도 경계 또는 접힘/매듭과 해당 의복 부착점이 식별됨

적용 속성 제안: `wardrobe.ornament.attachment`, `wardrobe.ornament.structure` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Coquette for Spring](https://www.vogue.co.uk/article/kendall-jenner-selena-gomez-coquette-girl-trend)

기존 검토 이웃: `profile:clothing_ct067_v1`, `slot:garment_detail:clt_ct067_v1`, `slot:garment_detail:metiers_art_embroidery_attachment_detail`, `slot:garment_detail:orn_gd35`, `slot:garment_detail:sff_pro_e14`

후보 초안:

- `SPR_DRAFT_SF091_01` (SPT11-15): A separate fabric motif is attached with visible edges over the base cloth.
- `SPR_DRAFT_SF091_02` (SPT11-16): Rolled fabric folds form a small raised rosette attached to the neckline.
- `SPR_DRAFT_SF091_03` (SPT11-17): Two ribbon loops meet at a knot attached to the same garment front.

## SF092 레이스업 경로

교차 끈·통과 고리/구멍·서로 마주한 패널을 연결한다. 실제 조절 성능은 별도다.

원문 연결: `SPT11-18` 레이스업 — Lace-up

관찰 구성: `lace_A`, `garment_A.left_eyelets`, `garment_A.right_eyelets`

관계 설계: `lace_A → threads_between → garment_A.opposing_eyelets`

혼동 경계: lace fabric·금속 프린트·다른 옷의 선을 lace-up으로 혼동하지 않는다.

관찰 조건: 끈의 반복 통과와 두 패널에 속한 고리들을 원본에서 확인

적용 속성 제안: `wardrobe.closure.lace_route` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Vivienne Westwood: Punk and Beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

기존 검토 이웃: `profile:sw_laceup`, `slot:garment_detail:sw_candidate_laceup`, `bundle:clothing_b_derby_tongue`, `profile:clothing_ct055_v1`, `profile:clothing_ct055_v2`

후보 초안:

- `SPR_DRAFT_SF092_01` (SPT11-18): A single lace crosses alternately through two opposing rows of eyelets on the garment.

## SF093 술·파이핑·금속 부품

연속 자유 술, 묶음 태슬, 봉제선을 따라가는 띠와 고정 금속을 별도 연결로 둔다.

원문 연결: `SPT11-19` 프린지·태슬 — Fringe / Tassel, `SPT11-20` 파이핑 — Piping, `SPT11-21` 스터드·아일릿·체인 — Studs / Eyelets / Chains

관찰 구성: `trim_A.free_strands`, `trim_A.anchor_edge`, `piping_A`, `hardware_A`

관계 설계: `trim_A.free_strands → hang_from → trim_A.anchor_edge`

혼동 경계: 프린지와 태슬, 자수 아이렛과 금속 아일릿, 체인 액세서리와 옷 부품의 소유자를 분리한다.

관찰 조건: 선택된 끝점·고정점·실제 부품 경계가 같은 물체에 속함

적용 속성 제안: `wardrobe.trim.endpoint_topology`, `wardrobe.hardware.attachment` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Vivienne Westwood: Punk and Beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

기존 검토 이웃: `profile:clothing_ct068_v2`, `slot:garment_detail:orn_gd38`, `profile:clothing_ct068_v1`, `profile:orn_profile_gd38`, `slot:fetish_styling:sff_pro_e07`

후보 초안:

- `SPR_DRAFT_SF093_01` (SPT11-19): Separate fringe strands hang continuously from the garment edge.
- `SPR_DRAFT_SF093_02` (SPT11-19): A bundle of strands hangs from one tied tassel head.
- `SPR_DRAFT_SF093_03` (SPT11-20): A narrow raised piping follows the garment seam.
- `SPR_DRAFT_SF093_04` (SPT11-21): Metal studs attach individually to the belt surface.

## SF094 로맨틱·페미닌·코케트

넓은 미적 문맥을 구체 아이템·표면·장식의 선택형 조합으로 푼다. 성별·성격·나이는 외형 결과가 아니다.

원문 연결: `SPT12-01` 로맨틱 — Romantic, `SPT12-02` 페미닌 — Feminine, `SPT12-03` 코케트 — Coquette

관찰 구성: `blouse_A.lace_edge`, `bow_A`, `skirt_A.soft_folds`

관계 설계: `bow_A → attaches_at → blouse_A.neckline`

혼동 경계: 리본 하나가 스타일 전체를 확증하지 않는다. 코케트에 성적 행동·어린 연령을 붙이지 않는다.

관찰 조건: 선택된 소유 장식만 검사; 스타일 명칭의 전체 증명은 사용자 문맥과 분리

적용 속성 제안: `wardrobe.ornament.attachment`, `wardrobe.skirt.folds` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Coquette for Spring](https://www.vogue.co.uk/article/kendall-jenner-selena-gomez-coquette-girl-trend), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `slot:aesthetic_trend:sff_pro_x02`, `slot:aesthetic_trend:vamp_romantic`, `slot:mood:romantic_decay_mood`, `slot:narrative_core:romantic_decay_core`, `slot:subject:adult_new_romantic_club_participant`

후보 초안:

- `SPR_DRAFT_SF094_01` (SPT12-03): A small ribbon bow attaches at the blouse neckline beside a narrow lace edge.
- `SPR_DRAFT_SF094_02` (SPT12-01): A floral skirt falls in soft gathered folds beneath the separate top.
- `SPR_DRAFT_SF094_03` (SPT12-02): The outfit combines a shaped waist with a softly flowing skirt and a small attached ornament.

## SF095 발레코어

랩 상의·신발·니트 토시 등 발레 유래 요소를 독립 옵션으로 둔다. 실제 발레 능력과 무대는 자동 추가하지 않는다.

원문 연결: `SPT12-04` 발레코어 — Balletcore

관찰 구성: `wrap_top_A`, `legwarmers_A`, `flat_shoes_A`

관계 설계: `legwarmers_A → wrap_around → wearer_A.lower_legs`

혼동 경계: 발레 플랫과 포인트 슈즈는 다르다. 발레코어가 토슈즈·튤·레오타드 모두의 의무는 아니다.

관찰 조건: 선택한 아이템과 실제 몸 부위의 접속만 확인

적용 속성 제안: `wardrobe.layer.item_combination` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `slot:aesthetic_trend:balletcore_aesthetic`, `slot:aesthetic_trend:coquette_balletcore_flatlay`

후보 초안:

- `SPR_DRAFT_SF095_01` (SPT12-04): A wrap knit top is paired with separate leg warmers and low flat shoes.

## SF096 코티지·프레리·보헤미안

전원 연상·높은 목선과 긴 층 치마·느슨한 장식 조합을 다른 문맥으로 둔다.

원문 연결: `SPT12-05` 코티지코어 — Cottagecore, `SPT12-06` 프레리 — Prairie style, `SPT12-07` 보헤미안·보호 — Bohemian / Boho

관찰 구성: `dress_A.puff_sleeves`, `dress_A.tiered_skirt`, `vest_A.open_motifs`

관계 설계: `vest_A → layers_over → dress_A`

혼동 경계: 꽃무늬 하나가 cottagecore 전체를 확증하지 않는다. 농촌 거주·민족·농부 정체성을 붙이지 않는다.

관찰 조건: 선택된 아이템 구성이 읽힘; 시대·생활방식은 픽셀 게이트가 아님

적용 속성 제안: `wardrobe.layer.item_combination` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `slot:aesthetic_trend:cottagecore_aesthetic`, `slot:world:cottagecore`, `bundle:y2kr_bundle_boho_layers`, `profile:y2kr_boho_palette`, `slot:color:y2kr_boho_palette`

후보 초안:

- `SPR_DRAFT_SF096_01` (SPT12-05): A small floral dress combines puff sleeves with an apron-like front panel.
- `SPR_DRAFT_SF096_02` (SPT12-06): A high-neck dress has full sleeves and a long tiered skirt.
- `SPR_DRAFT_SF096_03` (SPT12-07): A loose outfit combines an open-motif vest with separate embroidered trim.

## SF097 프레피·아이비·테니스코어

셔츠·폴로·블레이저·플리츠 등 선택형 아이템 문맥이다. 아이비의 모든 시대를 동일 규격으로 저장하지 않는다.

원문 연결: `SPT12-08` 프레피 — Preppy, `SPT12-09` 아이비 — Ivy style, `SPT12-10` 테니스코어 — Tenniscore

관찰 구성: `polo_A`, `pleated_skirt_A`, `blazer_A`, `loafers_A`

관계 설계: `blazer_A → layers_over → polo_A`

혼동 경계: 학교 재학·테니스 실력·사회 계층·유니폼 역할을 자동 확정하지 않는다.

관찰 조건: 선택된 옷 소유자·층 순서·주름과 신발 구조만 검사

적용 속성 제안: `wardrobe.layer.item_combination` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Ralph Lauren — Mad for Madras](https://www.ralphlauren.com/rlmag/ralph-lauren-mad-for-madras.html)

기존 검토 이웃: `slot:costume_style:dark_academia_tweed_outfit`, `slot:wardrobe_style:dark_academia_tweed_outfit`, `slot:footwear:penny_loafers`

후보 초안:

- `SPR_DRAFT_SF097_01` (SPT12-08): A polo top is paired with a pleated skirt and loafers.
- `SPR_DRAFT_SF097_02` (SPT12-09): An open blazer layers over an Oxford-style shirt and straight trousers.
- `SPR_DRAFT_SF097_03` (SPT12-10): A polo top is paired with a short pleated skirt and separate sports socks.

## SF098 애슬레저·스포티·캐주얼 시크

서로 다른 용도의 아이템이 같은 착용자에 결합되는 관계다. 문맥 이름이 특정 몸·운동 능력을 뜻하지 않는다.

원문 연결: `SPT12-11` 애슬레저 — Athleisure, `SPT12-12` 스포티 시크 — Sporty chic, `SPT12-13` 캐주얼 시크 — Casual chic

관찰 구성: `sport_top_A`, `jacket_A`, `jeans_A`

관계 설계: `jacket_A → layers_over → sport_top_A`

혼동 경계: 한 아이템을 스타일 전체의 정의로 고정하지 않는다. 퍼포먼스·기능성은 명세다.

관찰 조건: 선택된 아이템과 안팎 경계만 검사

적용 속성 제안: `wardrobe.layer.item_combination` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Oner Active — PrecisionMove Drop Armhole Vest](https://uk.oneractive.com/products/precisionmove-drop-armhole-tank-top-white)

기존 검토 이웃: `slot:action:adult_stretching_pose`, `slot:wardrobe_style:gym_athleisure_mirror_fit`

후보 초안:

- `SPR_DRAFT_SF098_01` (SPT12-11): A sports-style top is paired with leggings and low sneakers.
- `SPR_DRAFT_SF098_02` (SPT12-12): An open blazer layers over a sports top and wide trousers.
- `SPR_DRAFT_SF098_03` (SPT12-13): A simple tee and jeans are paired with a shaped jacket.

## SF099 프렌치·미니멀·럭셔리·해안 문맥

통칭을 아이템·색 수·장식 양·표면으로 구체화한다. 코스털과 노티컬은 서로 겹칠 수 있지만 동의어가 아니다.

원문 연결: `SPT12-14` 프렌치 시크† — French chic, `SPT12-15` 미니멀 — Minimal, `SPT12-16` 콰이어트 럭셔리† — Quiet luxury, `SPT12-17` 코스털·노티컬 — Coastal / Nautical

관찰 구성: `top_A`, `trousers_A`, `flat_shoes_A`, `outfit_A.visible_palette`

관계 설계: `top_A → shares_palette_family_with → trousers_A`

혼동 경계: 국적·거주지·실제 가격·경제력·섬유 진위·항해 능력을 외관으로 증명하지 않는다.

관찰 조건: 요청된 구체 요소만 확인; quiet luxury의 진짜 고급품 여부는 미채점

적용 속성 제안: `wardrobe.palette.relationship`, `wardrobe.surface.logo_presence` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `slot:aesthetic_trend:genz_clean_minimal`, `slot:body_marking:ankle_minimal_tattoo`, `slot:composition:negative_space`, `slot:location:minimal_korean_living_room`, `slot:makeup_style:wet_lash_minimal_makeup`

후보 초안:

- `SPR_DRAFT_SF099_01` (SPT12-14): A horizontal-striped top is paired with straight denim and flat shoes.
- `SPR_DRAFT_SF099_02` (SPT12-15, SPT12-16): A logo-free jacket and trousers share a restrained neutral palette.
- `SPR_DRAFT_SF099_03` (SPT12-17): A navy-and-light striped top is paired with light trousers.

## SF100 Y2K 문맥

시대·하위 스타일을 보존하고 로라이즈·짧은 상의·금속 등은 개별 옵션으로 둔다.

원문 연결: `SPT12-18` Y2K — Y2K style

관찰 구성: `top_A.hem`, `jeans_A.waistband`, `bag_A.short_strap`

관계 설계: `top_A.hem → lies_above → jeans_A.waistband`

혼동 경계: Y2K futurism·McBling·Cyber Y2K를 같은 세트로 합치지 않는다. 2000년대 전체가 로라이즈 의무는 아니다.

관찰 조건: 선택된 길이·허리단·가방 경로만 검사; 시대 자체는 문맥 메타데이터

적용 속성 제안: `wardrobe.layer.item_combination` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `bundle:direct_flash_y2k_snapshot`, `profile:y2kr_cyber_palette`, `profile:y2kr_goth_motif`, `profile:y2kr_pop_palette`, `profile:y2kr_rave_palette`

후보 초안:

- `SPR_DRAFT_SF100_01` (SPT12-18): A short fitted top is paired with low-waisted jeans and a small short-strap shoulder bag.

## SF101 란제리·고스·펑크·페티시 유래

레이스·슬립·코르셋·스트랩·버클을 소유 물체별로 둔다. 스타일 이름과 실제 행위를 분리한다.

원문 연결: `SPT12-19` 란제리 룩 — Lingerie dressing, `SPT12-20` 소프트 고스† — Soft goth, `SPT12-21` 펑크·록 시크 — Punk / Rock chic, `SPT12-22` 페티시 인스파이어드 — Fetish-inspired fashion

관찰 구성: `bustier_A`, `shirt_A`, `harness_A.straps`, `belt_A.buckle`

관계 설계: `harness_A.straps → lie_over → shirt_A.surface`

혼동 경계: 원문의 불편하거나 성적 뉘앙스가 있는 명칭도 삭제하지 않는다. 행위·노출·구속 상태를 자동 의무화하지 않는다.

관찰 조건: 선택한 의복·하드웨어·장신구 경계와 연결을 확인

적용 속성 제안: `wardrobe.layer.order`, `wardrobe.accessory.strap_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Vivienne Westwood: Punk and Beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: `slot:action:assembling_goth_scene_style_for_venue`, `slot:action:folding_zines_and_setting_up_diy_punk_show`, `slot:action:punk_world_system_action`, `slot:aesthetic_trend:sff_pro_x01`, `slot:location:punk_world_system_location`

후보 초안:

- `SPR_DRAFT_SF101_01` (SPT12-19): A lace-trimmed slip dress is worn beneath a separate cardigan.
- `SPR_DRAFT_SF101_02` (SPT12-20): A dark lace blouse is paired with a structured dark skirt.
- `SPR_DRAFT_SF101_03` (SPT12-21): A belt with attached metal studs crosses a short pleated skirt.
- `SPR_DRAFT_SF101_04` (SPT12-22): A separate fashion harness lies over the continuous blouse, with its straps connected at a buckle.

## SF102 글래머러스·여리핏·청순글램

유통 인상 표현을 광택·장식·여유·목선의 명시된 조합으로 풀고 단일 체형을 뜻하지 않게 한다.

원문 연결: `SPT12-23` 글래머러스 — Glamorous, `SPT12-24` 여리핏·청순글램†

관찰 구성: `top_A.neckline`, `top_A.soft_folds`, `ornament_A`

관계 설계: `ornament_A → attaches_to → top_A`

혼동 경계: 가슴·허리 치수를 키우거나 줄이고 나이·순결·매력을 픽셀 사실로 부여하지 않는다.

관찰 조건: 인상 이름은 선택권을 열어두며 구체 요청된 직물 관계만 검사

적용 속성 제안: `wardrobe.neckline.width`, `wardrobe.textile.drape`, `wardrobe.ornament.attachment` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [The Met — Extreme Beauty: The Body Transformed](https://www.metmuseum.org/press-releases/extreme-beauty-the-body-transformed-2001-exhibitions)

기존 검토 이웃: `profile:curvilinear_figure_relation`, `slot:mood:glamorous_backstage`

후보 초안:

- `SPR_DRAFT_SF102_01` (SPT12-23): A softly reflective dress carries a small attached ornament near the neckline.
- `SPR_DRAFT_SF102_02` (SPT12-24): The top has a wide neckline and soft fabric folds along the sleeves.

## SF103 색 이름·파스텔

색 명칭은 견본과 문맥을 갖는 가변 범주다. 여러 색이 병기된 원문 행은 하나의 강제 색으로 합치지 않는다.

원문 연결: `SPT13-01` 파스텔 — Pastel, `SPT13-02` 버터 옐로 — Butter yellow, `SPT13-03` 파우더 핑크 — Powder pink, `SPT13-04` 블러시 핑크 — Blush pink, `SPT13-05` 피치 — Peach, `SPT13-06` 라일락·라벤더 — Lilac / Lavender, `SPT13-07` 스카이 블루 — Sky blue, `SPT13-08` 아이시 블루 — Icy blue, `SPT13-09` 민트 — Mint, `SPT13-10` 세이지 — Sage, `SPT13-11` 아이보리·에크루 — Ivory / Ecru, `SPT13-12` 베이지·그레이지 — Beige / Greige, `SPT13-13` 체리 레드 — Cherry red

관찰 구성: `garment_A.color_field`, `reference_swatch_A`

관계 설계: `garment_A.color_field → corresponds_to → reference_swatch_A`

혼동 경계: blush는 피부 화장, sage는 식물 등 다의성이 있다. 임의 RGB와 전역 화이트밸런스를 변경하지 않는다.

관찰 조건: 선택한 의복 면의 색과 조명·견본 기준; 이름만으로 색차 수치를 PASS하지 않음

적용 속성 제안: `wardrobe.palette.local_color` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Colour Trends Summer 2025](https://www.vogue.co.uk/article/summer-colour-trends-2025)

기존 검토 이웃: `profile:y2kr_pop_palette`, `slot:color:hanbok_pastel_seasonal`, `slot:color:kpop_y2k_pastel_chrome`, `slot:color:matte_pastel_editorial`, `slot:color:pastel`

후보 초안:

- `SPR_DRAFT_SF103_01` (SPT13-02): A pale warm yellow colors the selected cardigan.
- `SPR_DRAFT_SF103_02` (SPT13-08): A very pale cool blue colors the selected blouse.
- `SPR_DRAFT_SF103_03` (SPT13-10): A muted gray-green colors the selected trousers.
- `SPR_DRAFT_SF103_04` (SPT13-13): A small bag provides a saturated red accent.
- `SPR_DRAFT_SF103_05` (SPT13-01): The selected garment uses a light, softly saturated color.
- `SPR_DRAFT_SF103_06` (SPT13-03): A pale soft pink colors the selected top.
- `SPR_DRAFT_SF103_07` (SPT13-04): A pale warm pink with a muted beige undertone colors the selected blouse.
- `SPR_DRAFT_SF103_08` (SPT13-05): A soft pink-orange colors the selected skirt.
- `SPR_DRAFT_SF103_09` (SPT13-06): A pale violet colors the selected cardigan.
- `SPR_DRAFT_SF103_10` (SPT13-07): A light clear blue colors the selected shirt.
- `SPR_DRAFT_SF103_11` (SPT13-09): A light blue-green colors the selected top.
- `SPR_DRAFT_SF103_12` (SPT13-11): A warm off-white colors the selected skirt.
- `SPR_DRAFT_SF103_13` (SPT13-12): A light muted beige-gray colors the selected trousers.

## SF104 모노크로매틱·토널·컬러 블로킹

색 관계의 양 끝은 실제 의복 또는 같은 의복의 패널이다. 전역 필터와 구분한다.

원문 연결: `SPT13-14` 모노크로매틱 — Monochromatic, `SPT13-15` 토널 드레싱 — Tonal dressing, `SPT13-16` 컬러 블로킹 — Colour blocking

관찰 구성: `top_A.color`, `bottom_A.color`, `garment_A.panel_colors`

관계 설계: `top_A.color → shares_hue_family_with → bottom_A.color`

혼동 경계: 토널과 단일색을 같은 hard 의미로 고정하지 않는다. background까지 자동 변색하지 않는다.

관찰 조건: 옷마다 색 소유자와 두 색의 관계 또는 패널 경계가 읽힘

적용 속성 제안: `wardrobe.palette.item_relationship`, `wardrobe.palette.panel_layout` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Colour Trends Summer 2025](https://www.vogue.co.uk/article/summer-colour-trends-2025)

기존 검토 이웃: `bundle:cr_variant_monochromatic`, `profile:cr_monochromatic`, `slot:color:cr_candidate_monochromatic`, `profile:cr_color_blocks`, `slot:color:cr_candidate_color_blocks`

후보 초안:

- `SPR_DRAFT_SF104_01` (SPT13-14): The top and trousers use different lightness levels of the same blue family.
- `SPR_DRAFT_SF104_02` (SPT13-15): The blouse and skirt use closely related muted warm tones.
- `SPR_DRAFT_SF104_03` (SPT13-16): Large distinct color panels meet along visible garment seams.

## SF105 디츠이·보태니컬·수채 꽃무늬

모티프 구성·크기·밀도·윤곽의 선명도를 분리한다. 꽃무늬는 실제 배경 꽃을 추가하지 않는다.

원문 연결: `SPT13-17` 디츠이 플로럴 — Ditsy floral, `SPT13-18` 보태니컬 프린트 — Botanical print, `SPT13-19` 워터컬러 플로럴 — Watercolour floral

관찰 구성: `dress_A.print_motifs`, `dress_A.garment_field`

관계 설계: `dress_A.print_motifs → repeat_over → dress_A.garment_field`

혼동 경계: floral=embroidered=lace가 아니다. 실제 크기 수치는 견본이나 몸 기준 명세 필요하다.

관찰 조건: 주름을 따라 이어지는 인쇄면·선택한 모티프/밀도/윤곽 확인

적용 속성 제안: `wardrobe.print.motif`, `wardrobe.print.scale`, `wardrobe.print.edge_quality` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Printed Dresses 2026](https://www.vogue.co.uk/article/printed-dress-trend-summer-2026)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF105_01` (SPT13-17): Tiny floral motifs repeat densely across the dress fabric.
- `SPR_DRAFT_SF105_02` (SPT13-18): Leaves, stems and flowers form larger botanical motifs on the same fabric.
- `SPR_DRAFT_SF105_03` (SPT13-19): Soft-edged floral color patches form a watercolor-like print on the dress.

## SF106 깅엄·줄·점·투알·페이즐리

반복 모티프의 윤곽·방향·겹침을 저장한다. 소재 공정·특정 민족·항해 역할은 별도다.

원문 연결: `SPT13-20` 깅엄 — Gingham, `SPT13-21` 브르통 스트라이프 — Breton stripes, `SPT13-22` 폴카 도트 — Polka dots, `SPT13-23` 투알 드 주이 — Toile de Jouy, `SPT13-24` 페이즐리 — Paisley

관찰 구성: `garment_A.pattern_motifs`, `garment_A.fold_surface`

관계 설계: `garment_A.pattern_motifs → continue_across → garment_A.fold_surface`

혼동 경계: gingham 외관과 실제 yarn-dyed 공정은 다르다. 투알을 보편적인 단일 파랑, 페이즐리를 민족 정체성으로 고정하지 않는다.

관찰 조건: 모티프가 해당 원단 주름·경계에 따라 연결되고 벽/배경 무늬와 분리됨

적용 속성 제안: `wardrobe.print.repeat_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Printed Dresses 2026](https://www.vogue.co.uk/article/printed-dress-trend-summer-2026)

기존 검토 이웃: `profile:clothing_ct095_v2`, `slot:surface_material:clt_ct095_v2`, `profile:clothing_ct096_v1`, `slot:surface_material:clt_ct096_v1`, `profile:clothing_ct096_v2`

후보 초안:

- `SPR_DRAFT_SF106_01` (SPT13-20): Even-width horizontal and vertical bands cross into a small repeating check pattern.
- `SPR_DRAFT_SF106_02` (SPT13-21): Repeated horizontal light and dark stripes follow the top fabric.
- `SPR_DRAFT_SF106_03` (SPT13-22): Round dots repeat across the garment.
- `SPR_DRAFT_SF106_04` (SPT13-23): Small line-drawn landscape scenes repeat across the fabric.
- `SPR_DRAFT_SF106_05` (SPT13-24): Curved teardrop motifs with hooked tips repeat across the fabric.

## SF107 플랫·메리제인·슬링백·뮬·굽

발등과 뒤꿈치 연결 및 갑피·굽·밑창을 독립적으로 저장한다. 메리제인과 슬링백이 함께 가능한 변형도 있다.

원문 연결: `SPT14-01` 발레 플랫 — Ballet flats, `SPT14-02` 메리제인 — Mary Janes, `SPT14-03` 슬링백 — Slingbacks, `SPT14-04` 뮬 — Mules, `SPT14-05` 로퍼 — Loafers, `SPT14-06` 키튼 힐 — Kitten heels, `SPT14-07` 에스파드리유 — Espadrilles

관찰 구성: `shoe_A.instep_strap`, `shoe_A.heel_strap`, `shoe_A.heel`, `shoe_A.upper`

관계 설계: `shoe_A.instep_strap → connects_across → wearer_A.instep`

혼동 경계: 발레 플랫=포인트 슈즈가 아니다. kitten은 굽 속성이다. 뮬의 열린 앞코 여부와 밑창 섬유 진위는 별도다.

관찰 조건: 선택한 발등/뒤꿈치 부착 양끝과 실제 신발; 로프 성분·착화감은 미채점

적용 속성 제안: `wardrobe.shoe.strap_route`, `wardrobe.shoe.heel_shape`, `wardrobe.shoe.sole_surface` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Steve Madden — Shoe Glossary](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction), [British Vogue — TikTok Aesthetics of 2023](https://www.vogue.co.uk/article/tiktok-aesthetics-2023)

기존 검토 이웃: `slot:footwear:low_profile_ballet_flat_topology`, `bundle:y2kr_bundle_ballet_neighbor`, `profile:y2kr_ballet_flats`, `slot:footwear:ballet_flat_sneakers`, `slot:footwear:y2kr_ballet_flats`

후보 초안:

- `SPR_DRAFT_SF107_01` (SPT14-01): A low flat shoe encloses the forefoot with a small bow at the vamp.
- `SPR_DRAFT_SF107_02` (SPT14-02): A strap crosses the instep and attaches to both sides of the same shoe.
- `SPR_DRAFT_SF107_03` (SPT14-03): A strap passes behind the heel and joins both sides of the shoe.
- `SPR_DRAFT_SF107_04` (SPT14-04): The shoe leaves the rear heel open without a rear strap.
- `SPR_DRAFT_SF107_05` (SPT14-06): A short slender heel supports the rear of the shoe.
- `SPR_DRAFT_SF107_06` (SPT14-07): A rope-like braided layer runs around the shoe sole.
- `SPR_DRAFT_SF107_07` (SPT14-05): A low slip-on shoe has a continuous vamp without a crossing lace closure.

## SF108 샌들·발목끈·메시·낮은 스니커즈·부츠

끈의 몸 부위, 갑피 조직, 신발 부피, 샤프트 높이를 각각 선택한다.

원문 연결: `SPT14-08` 스트래피 샌들 — Strappy sandals, `SPT14-09` 앵클 스트랩 — Ankle strap, `SPT14-10` 메시 슈즈 — Mesh shoes, `SPT14-11` 로프로파일 스니커즈 — Low-profile sneakers, `SPT14-12` 앵클부츠 — Ankle boots

관찰 구성: `shoe_A.ankle_strap`, `shoe_A.mesh_upper`, `shoe_A.sole`, `boot_A.shaft`

관계 설계: `shoe_A.ankle_strap → encircles → wearer_A.ankle`

혼동 경계: 끈만 보인다고 해당 신발의 연결이 완전한 것은 아니다. 메시와 fishnet의 크기 경계는 명세로 둔다.

관찰 조건: 끈 양끝·갑피-밑창 접속·같은 발 기준점이 읽힘

적용 속성 제안: `wardrobe.shoe.strap_route`, `wardrobe.shoe.upper_structure`, `wardrobe.shoe.shaft_height` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [Steve Madden — Shoe Glossary](https://www.stevemadden.com/pages/glossary-of-shoe-types-materials-and-construction)

기존 검토 이웃: `slot:footwear:strappy_flat_sandals`, `profile:clothing_ct125_v2`, `slot:footwear:clt_ct125_v2`, `slot:footwear:slim_low_profile_sneakers`, `slot:footwear:pointed_ankle_boots`

후보 초안:

- `SPR_DRAFT_SF108_01` (SPT14-08, SPT14-09): Several connected straps cross the foot while a separate strap circles the ankle.
- `SPR_DRAFT_SF108_02` (SPT14-10): A visible mesh upper spans the foot above the shoe sole.
- `SPR_DRAFT_SF108_03` (SPT14-11): The sneaker has a low thin-looking sole and a narrow upper profile.
- `SPR_DRAFT_SF108_04` (SPT14-12): The boot shaft ends around the ankle.

## SF109 양말 길이·타이츠·피시넷·토시

끝점과 무릎·허벅지 기준, 망상 조직과 아래층, 발을 덮는지 여부를 나눈다.

원문 연결: `SPT14-13` 니하이 삭스 — Knee-high socks, `SPT14-14` 오버니·사이하이 — Over-the-knee / Thigh-high, `SPT14-15` 시어 타이츠 — Sheer tights, `SPT14-16` 피시넷 — Fishnets, `SPT14-17` 레그워머 — Leg warmers

관찰 구성: `sock_A.top_edge`, `tights_A.mesh`, `legwarmer_A.open_ends`, `wearer_A.knee`

관계 설계: `sock_A.top_edge → lies_relative_to → wearer_A.knee`

혼동 경계: 맨다리·피부색 안감·불투명 타이츠를 구분한다. denier·섬유·가터 지지 기능은 사진에서 확증하지 않는다.

관찰 조건: 길이 기준점과 실/망상 조직 및 실제 의복 끝단이 보임

적용 속성 제안: `wardrobe.hosiery.hem_height`, `wardrobe.hosiery.surface`, `wardrobe.legwarmer.coverage` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: `profile:pfe_slit`, `slot:fetish_styling:fishnet_thigh_high_boots`, `slot:garment_detail:pfe_slit_candidate`, `profile:pfe_hosiery_sheer`, `slot:texture:pfe_hosiery_sheer_candidate`

후보 초안:

- `SPR_DRAFT_SF109_01` (SPT14-13): The sock top ends just below the knee.
- `SPR_DRAFT_SF109_02` (SPT14-14): The stocking top reaches above the knee.
- `SPR_DRAFT_SF109_03` (SPT14-15): A thin continuous hosiery layer softly transmits the leg color.
- `SPR_DRAFT_SF109_04` (SPT14-16): A distinct net pattern wraps around the leg.
- `SPR_DRAFT_SF109_05` (SPT14-17): A separate knit tube gathers around the calf with the foot left uncovered.

## SF110 머리 리본·머리띠·스카프

부착·묶음 위치와 물체를 유지한다. 같은 리본이라는 이름으로 옷과 머리의 소유자를 공유하지 않는다.

원문 연결: `SPT14-18` 헤어 보·헤드밴드 — Hair bow / Headband, `SPT14-19` 실크 스카프 — Silk scarf

관찰 구성: `hair_bow_A`, `headband_A`, `scarf_A`, `wearer_A.head`

관계 설계: `hair_bow_A → attaches_to → wearer_A.hair`

혼동 경계: 실크는 성분 명세이며 광택이나 얇음으로 진위를 판정하지 않는다.

관찰 조건: 머리/목의 실제 경로·부착 또는 매듭과 옷의 리본이 구분됨

적용 속성 제안: `appearance.accessory.attachment`, `metadata.accessory.fiber` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Coquette for Spring](https://www.vogue.co.uk/article/kendall-jenner-selena-gomez-coquette-girl-trend)

기존 검토 이웃: `profile:clothing_ct101_v2`, `profile:clothing_ct102_v1`, `slot:hair_style:long_black_twin_tails`, `slot:wearable_accessory:clt_ct101_v2`, `slot:wearable_accessory:clt_ct102_v1`

후보 초안:

- `SPR_DRAFT_SF110_01` (SPT14-18): A separate ribbon bow is visibly secured in the hair.
- `SPR_DRAFT_SF110_02` (SPT14-18): A curved headband crosses the top of the head.
- `SPR_DRAFT_SF110_03` (SPT14-19): A thin scarf wraps around the neck and ties in a small knot.

## SF111 라피아 외관·작은 숄더백

식물 섬유 성분과 엮임 외관, 가방 부피와 짧은 스트랩을 분리한다.

원문 연결: `SPT14-20` 라피아 백 — Raffia bag, `SPT14-21` 미니 숄더백 — Mini shoulder bag

관찰 구성: `bag_A.woven_body`, `bag_A.short_strap`, `bag_A.anchors`

관계 설계: `bag_A.short_strap → joins → bag_A.two_anchors`

혼동 경계: raffia와 유사 재료의 외관을 구별해 명세 보류한다. 몸 겨드랑이 노출을 자동 추가하지 않는다.

관찰 조건: 가방 면·입구·스트랩 두 앵커와 해당 어깨의 관계 확인

적용 속성 제안: `wardrobe.bag.surface`, `wardrobe.bag.strap_length` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5)

기존 검토 이웃: `profile:y2kr_mini_shoulder`, `slot:wearable_accessory:y2kr_mini_shoulder`

후보 초안:

- `SPR_DRAFT_SF111_01` (SPT14-20): Broad straw-like strands interlace across the bag surface.
- `SPR_DRAFT_SF111_02` (SPT14-21): A small bag hangs close below the shoulder from a short strap attached at both bag ends.

## SF112 체인·하네스·가터 연결

장신구와 옷은 다른 소유자다. 체인 링크·스트랩·버클과 스타킹 클립의 실제 연결을 둔다.

원문 연결: `SPT14-22` 보디 체인·웨이스트 체인 — Body / Waist chain, `SPT14-23` 패션 하네스 — Fashion harness, `SPT14-24` 가터 디테일 — Garter details

관찰 구성: `chain_A.links`, `harness_A.straps`, `garter_A.clip`, `stocking_A.top_band`

관계 설계: `garter_A.clip → attaches_to → stocking_A.top_band`

혼동 경계: 장식 가터와 실제 지지 연결은 다르다. 이미지에서 구속·동의·성적 행위를 추론하지 않는다.

관찰 조건: 각 물체의 실제 링크/부착 양끝이 모두 읽힘

적용 속성 제안: `wardrobe.accessory.connection_topology` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [V&A — Vivienne Westwood: Punk and Beyond](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)

기존 검토 이웃: `profile:clothing_ct113_v2`, `profile:y2kr_body_chain`, `slot:wearable_accessory:clt_ct113_v2`, `slot:wearable_accessory:y2kr_body_chain`, `bundle:chrh_bundle_chrh_hair_color_state_hair_body_overlap`

후보 초안:

- `SPR_DRAFT_SF112_01` (SPT14-22): Linked metal segments form a separate chain around the waist over the outfit.
- `SPR_DRAFT_SF112_02` (SPT14-23): A separate harness crosses the blouse with connected straps and one visible buckle.
- `SPR_DRAFT_SF112_03` (SPT14-24): A garter strap ends in a visible clip attached to the stocking top band.
- `SPR_DRAFT_SF112_04` (SPT14-24): A separate decorative band circles the thigh without a stocking clip.

## SF113 겹침·투과·피카부

겉옷-안쪽 옷-피부를 별도 노드로 두고 구멍 또는 투과 경로를 지정한다.

원문 연결: `SPT15-01` 레이어링 — Layering, `SPT15-02` 시어 레이어링 — Sheer layering, `SPT15-03` 피카부 — Peekaboo

관찰 구성: `outer_A`, `inner_A`, `wearer_A.skin`, `outer_A.opening`

관계 설계: `outer_A → overlies → inner_A`

혼동 경계: peekaboo는 피부와 속옷 모두 가능하다. 이름만으로 노출을 확대하지 않는다.

관찰 조건: 어느 표면을 보게 하는지 소유자와 실제 외부 경계를 확인

적용 속성 제안: `wardrobe.layer.order`, `wardrobe.layer.revealed_surface` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: `slot:composition:window_reflection_layering`, `slot:procedure_step:prepare_style_participate_step`, `slot:silhouette_proportion:advanced_clever_layering`, `slot:silhouette_proportion:skirt_over_pants_layering`, `profile:adult_everyday_controlled_reveal_moment`

후보 초안:

- `SPR_DRAFT_SF113_01` (SPT15-01): The outer cardigan frames the separate inner top with both garment edges visible.
- `SPR_DRAFT_SF113_02` (SPT15-02): The sheer outer shirt transmits the solid inner top while retaining its own texture.
- `SPR_DRAFT_SF113_03` (SPT15-03): An opening in the outer garment reveals the separate inner garment beneath it.

## SF114 언더웨어 애즈 아우터웨어·보이는 브라

속옷 유래 형태와 현재 겉에서 보이는 아래층을 분리한다. 의도는 요청 문맥이지 사진의 심리 사실이 아니다.

원문 연결: `SPT15-04` 언더웨어 애즈 아우터웨어 — Underwear as outerwear, `SPT15-05` 익스포즈드 브라† — Exposed bra styling

관찰 구성: `bra_A.upper_edge`, `outer_A.open_front`, `bra_A.straps`

관계 설계: `outer_A.open_front → reveals → bra_A.upper_edge`

혼동 경계: 란제리풍 원피스가 실제 브라를 입었다는 증거는 아니다. 노출이 항상 맨살인 것도 아니다.

관찰 조건: 같은 브라/속옷 유래 의복의 경계와 바깥옷 가림 순서 확인

적용 속성 제안: `wardrobe.layer.revealed_garment` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: `profile:underwear_as_outerwear_layer_system`

후보 초안:

- `SPR_DRAFT_SF114_01` (SPT15-05): The open jacket frames a separate bra-style top whose upper edge and straps remain visible.
- `SPR_DRAFT_SF114_02` (SPT15-04): A lingerie-style slip is worn as the visible dress beneath an open outer layer.

## SF115 브라리스의 숨은 상태

브라 부재는 착용 명세다. 겉옷이 불투명하거나 내부가 가려지면 사진에서 확인할 수 없다.

원문 연결: `SPT15-06` 브라리스† — Braless styling

관찰 구성: `outfit_A.bra_presence_spec`, `outer_A`

관계 설계: `outfit_A.bra_presence_spec → constrains_hidden_layer_of → outer_A`

혼동 경계: 보이지 않는 끈·매끈한 표면·노브라 느낌·피부 윤곽을 실제 부재로 확증하지 않는다. 요청 문맥은 삭제하지 않는다.

관찰 조건: 명시적 요청/착용 명세로 보존; 내부 부재는 정지 외부 사진에서 UNOBSERVABLE

적용 속성 제안: `metadata.layer.bra_presence` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- 요청 명세로만 유지하며 정지 이미지 hard 의무를 만들지 않음.

## SF116 네이키드 드레싱·노팬츠 문맥

피부색 안감·투명층·컷아웃·긴 상의와 짧은 하의 등 선택된 실제 조합으로 푼다.

원문 연결: `SPT15-07` 네이키드 드레싱† — Naked dressing, `SPT15-08` 노팬츠 룩† — No-pants look

관찰 구성: `dress_A.sheer_layer`, `lining_A`, `long_top_A`, `shorts_A`

관계 설계: `long_top_A → overlies → shorts_A`

혼동 경계: 원문 이름을 없애지 않지만 실제 무의복·숨은 쇼츠 부재를 자동 결론으로 만들지 않는다.

관찰 조건: 선택된 안감 경계 또는 긴 상의-하의 경계가 보임; 가려진 부재는 미채점

적용 속성 제안: `wardrobe.layer.order`, `wardrobe.layer.coverage_relation` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Edie Sedgwick No-Pants Look](https://www.vogue.co.uk/fashion/article/edie-sedgwick-no-pants-fashion-trend)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF116_01` (SPT15-07): A sheer dress layer lies over a continuous skin-tone lining.
- `SPR_DRAFT_SF116_02` (SPT15-08): A long top overlaps the short lower garment so its hem is only slightly visible.

## SF117 열린 카디건·폴드오버

현재 여밈 상태와 접힌 가장자리를 저장한다. 완전히 열림·일부 단추 잠금·접힌 허리단은 다른 변형이다.

원문 연결: `SPT15-09` 오픈 카디건 스타일링† — Open-cardigan styling, `SPT15-10` 턴다운·폴드오버 — Fold-over styling

관찰 구성: `cardigan_A.placket_edges`, `cardigan_A.fastened_button`, `garment_A.folded_edge`

관계 설계: `cardigan_A.placket_edges → separate_below → cardigan_A.fastened_button`

혼동 경계: 원단 자체 밴드·카울 접힘·열린 모든 단추 상태를 한 의미로 고정하지 않는다.

관찰 조건: 같은 여밈의 고정점과 분리된 양변 또는 접힘의 이중 직물 경계 확인

적용 속성 제안: `wardrobe.closure.current_state`, `wardrobe.edge.fold_state` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [British Vogue — Lingerie Dressing](https://www.vogue.co.uk/fashion/article/lingerie-dressing-trend-ss23)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF117_01` (SPT15-09): One upper cardigan button is fastened while the front edges separate below it.
- `SPR_DRAFT_SF117_02` (SPT15-10): The garment upper edge folds outward into a continuous doubled band.

## SF118 질감·길이·부피의 대비

대비의 양 끝은 같은 착용자의 구체 의복이다. 체형·배경·촬영 스타일로 전파하지 않는다.

원문 연결: `SPT15-11` 텍스처 믹스 — Texture mixing, `SPT15-12` 프로포션 플레이† — Proportion play

관찰 구성: `top_A.surface`, `skirt_A.surface`, `top_A.hem`, `bottom_A.volume`

관계 설계: `top_A.surface → contrasts_with → skirt_A.surface`

혼동 경계: 텍스처 믹스는 섬유 진위의 비교가 아니다. proportion play는 실제 몸 비율 변경이 아니다.

관찰 조건: 양 의복의 경계와 서로 다른 선택된 속성이 동시에 읽힘

적용 속성 제안: `wardrobe.layer.surface_relationship`, `wardrobe.layer.proportion_relationship` (실제 경로 검증 전)

출처: [봄 패션 용어 조사](https://chatgpt.com/c/6ac7dd42-01f0-83ee-b2e1-92d1775f13d5), [CottonWorks — Basic Woven Fabric Designs](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [CottonWorks — Knit Basics](https://cottonworks.com/learning-hub/knitting/knit-basics/)

기존 검토 이웃: 같은 긍정 표현 이웃 없음; 의미 자체의 부재를 입증하지 않음

후보 초안:

- `SPR_DRAFT_SF118_01` (SPT15-11): A matte knit top sits above a smooth softly reflective skirt.
- `SPR_DRAFT_SF118_02` (SPT15-12): A short fitted top is paired with long wide trouser legs.


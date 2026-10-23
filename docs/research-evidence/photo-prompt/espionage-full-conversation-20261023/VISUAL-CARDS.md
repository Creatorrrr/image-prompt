# 새 시각 의미 카드 42개

각 카드는 하나의 완결된 한영 제안이며 native_approval=false다. 모든 접점과 소유자, 물리 매체/묘사 이미지 경계는 함께 유지한다. 아래 게이트는 실제 이미지로 별도 검증해야 한다.

## espfull_worn_lapel — 외투 라펠 마모 경계

A coat lapel has a scuffed pale patch beside an intact darker area, both on the same continuous cloth panel.

한 외투의 이어진 라펠 천에 옅게 닳은 부분과 손상되지 않은 짙은 부분이 나란히 보인다.

관계: coat.lapel → has_patch → coat.scuff; coat.scuff → borders → coat.intact_cloth

관찰 게이트: 같은 천의 마모·정상 경계

혼동 경계: 실제 착용 연수; 임무 이력

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_3fa7a99327a157d3963d2d8727067013

## espfull_weathered_hem — 외투 밑단 표면 침착

A coat hem bears a matte dusty band with irregular edges above a cleaner strip of the same fabric.

외투 밑단의 같은 천 위에서 불규칙한 가장자리의 무광 먼지 띠와 더 깨끗한 띠가 구분된다.

관계: coat.hem → carries → dust.band; dust.band → borders → coat.clean_strip

관찰 게이트: 먼지 띠와 같은 천 경계

혼동 경계: 환경 노출 원인·기간

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_8c487d89b0b75ad0917c777fae26ff34

## espfull_creased_sleeve — 소매 구김 능선

One cloth sleeve shows three angular creases, each with a raised ridge and an adjacent shadowed trough on the same sleeve panel.

하나의 천 소매에 각진 주름 세 개가 있고 각 주름의 솟은 능선과 인접한 그늘 골이 같은 소매 면에 보인다.

관계: sleeve.panel → contains → crease.ridges; crease.ridges → adjoin → crease.troughs

관찰 게이트: 능선·골 연속; 같은 소매

혼동 경계: 밤샘·이동 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_2962679f867e5d40829315f5c1488850

## espfull_frayed_cuff — 소맷부리 해짐 연결

Loose individual fibres extend directly from the unravelled edge of one cloth cuff, with the intact sleeve weave visible beside the edge.

헐어진 천 소맷부리 끝에서 낱실이 직접 이어져 나오고 그 옆에는 온전한 소매 직조가 보인다.

관계: cuff.edge → remains_connected_to → loose.fibres; cuff.edge → borders → sleeve.intact_weave

관찰 게이트: 낱실 뿌리와 커프 연결; 온전한 직조 경계

혼동 경계: 찢어진 구멍; 별도 실뭉치

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_7afc6f2c0fd25373acaef2f16c6ef922

## espfull_torn_coat — 겉옷 찢김의 두 가장자리

An opaque outer coat has a small tear with two separated ragged cloth edges; an intact opaque lining remains visible through the opening.

불투명 겉외투의 작은 찢김에서 거친 천 가장자리 둘이 벌어지고 그 틈으로 온전한 불투명 안감이 보인다.

관계: coat.edge_a → separated_from → coat.edge_b; coat.opening → reveals → lining.opaque_cloth

관찰 게이트: 둘로 나뉜 천 가장자리; 안감과 겉감 분리

혼동 경계: 피부 손상; 사건 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_d5edfac258ee57d097318c5437b07269

## espfull_wet_coat — 젖은 외투와 방울

One opaque coat panel has a darker wet patch beside drier cloth, with distinct water droplets resting on the darker patch and a hanging damp hem.

하나의 불투명 외투 면에서 마른 천 옆에 짙은 젖은 부분이 있고 그 위의 물방울과 아래로 처진 축축한 밑단이 보인다.

관계: coat.wet_patch → borders → coat.dry_cloth; droplets → rest_on → coat.wet_patch; coat.hem → hangs_below → coat.wet_patch

관찰 게이트: 같은 천 젖음·마름 경계; 독립 방울; 불투명 천

혼동 경계: 비 원인; 원래 광택 소재; 투명 의복

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_e3281d2c6a3b50b89861fb35f5562be6

## espfull_grime_seam — 가방 솔기의 때

A bag has dark matte residue gathered inside its seam recess, while the adjoining raised leather-like edge is cleaner.

가방 솔기의 움푹한 곳에 짙은 무광 잔여물이 모이고 인접한 가죽처럼 보이는 솟은 가장자리는 더 깨끗하다.

관계: bag.seam_recess → contains → residue; bag.raised_edge → borders → bag.seam_recess

관찰 게이트: 홈·솟은 부분·침착 구분

혼동 경계: 물질 화학; 오염 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_d8785048a5025e93b3bc4941df06dcfe

## espfull_skin_beads — 피부의 습한 반사

Small moisture beads sit on a person’s temple above the cheek, with separate specular points on the beads and visible skin between them.

인물의 관자놀이와 볼 위쪽에 작은 수분 방울이 있고 방울마다 반사점과 그 사이 피부가 구분된다.

관계: moisture.beads → rest_on → person.temple; skin.gaps → separate → moisture.beads

관찰 게이트: 방울과 피부 분리

혼동 경계: 땀의 화학적 증명; 긴장·운동·공포

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F05

후보: cand_5428bd31f718509aa5ed96737e2e97f6

## espfull_smudged_liner — 아이라인 번짐 경계

A person’s lower eyelid has a dark cosmetic line whose edge feathers into a soft grey smear on the adjacent cheek, while the eye remains separate.

인물의 아래 눈꺼풀을 따른 짙은 화장선의 가장자리가 옆 볼의 옅은 회색 번짐으로 퍼지고 눈 자체와 구분된다.

관계: cosmetic.line → along → person.lower_eyelid; cosmetic.smear → extends_from → cosmetic.line

관찰 게이트: 눈·화장선·번짐 분리

혼동 경계: 울음·비·마찰 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F05

후보: cand_963e48ea66c4553886dd4ae534a7a08b

## espfull_casualty_swatch — 상해 분장 표본

A small stage-makeup swatch beside a brush shows a violet bruise-like oval and a thin painted red scratch on artificial skin material.

붓 옆 작은 무대 분장 표본의 인조 피부 재료에 보라색 멍처럼 보이는 타원과 가늘게 그린 붉은 긁힘이 보인다.

관계: swatch.artificial_skin → carries → painted.oval; swatch.artificial_skin → carries → painted.line; brush → beside → swatch

관찰 게이트: 표본·붓·그린 자국

혼동 경계: 실제 상해; 심문·고문·상해 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F05

후보: cand_a7847a8c92c5559f8001e7ed0b6b2e07

## espfull_redbrown_stain — 옷 위 적갈색 얼룩

An opaque shirt has an irregular red-brown stain across its cloth weave, with the clean cloth and the stain boundary visible together.

불투명 셔츠의 직조 위에 불규칙한 적갈색 얼룩이 있고 깨끗한 천과 얼룩 경계가 함께 보인다.

관계: shirt.weave → carries → redbrown.stain; redbrown.stain → borders → shirt.clean_cloth

관찰 게이트: 천 위 얼룩 경계

혼동 경계: 혈액 성분; 피의 주인; 폭력·시점

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F01

후보: cand_89188f30b580502986aac1ff11a20429

## espfull_scar_surface — 피부의 선형 표면 차이

A narrow pale raised line crosses a small area of visible skin, with its edge relief and surrounding uninterrupted skin readable together.

드러난 피부의 작은 부분에 옅고 가늘게 솟은 선이 가로지르고 그 가장자리 높낮이와 주변의 이어진 피부가 함께 보인다.

관계: pale.raised_line → crosses → skin.patch; pale.raised_line → borders → skin.uninterrupted_surface

관찰 게이트: 선의 높낮이·피부 경계

혼동 경계: 치유 이력; 흉터 원인·나이

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F05

후보: cand_120874426c18573ba6a6ebafca7bf64e

## espfull_continuity_pair — 의상 연속성 비교 기록

Two separate printed continuity photographs lie side by side; each depicts a coat with one crescent tear at the left cuff and a dark patch below the same lapel, with corresponding positions visible in both prints.

분리된 의상 연속성 기록 사진 두 장이 나란히 놓이고 각 인쇄 이미지의 외투 왼 소맷부리에 초승달 모양 찢김 하나와 같은 라펠 아래 짙은 자국이 있어 두 사진의 대응 위치를 비교할 수 있다.

관계: print_a.depicted_cuff → has → print_a.crescent_tear; print_b.depicted_cuff → has → print_b.crescent_tear; print_a.depicted_lapel → above → print_a.dark_patch; print_b.depicted_lapel → above → print_b.dark_patch

관찰 게이트: 독립 사진 두 장; 각 사진 속 대응 위치

혼동 경계: 실제 동일 인물; 촬영 시각·서사 시간 연속성

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F02

후보: cand_6396b6ee1b755ae0b7cc09d0a03dc120

## espfull_blocking_triangle — 인물 배치의 삼각 관계

Three people occupy separate points around a table: one seated at its near edge and two standing beyond opposite corners, with open space between each body.

탁자 가까운 가장자리에 앉은 한 사람과 먼쪽 두 모서리 뒤에 선 두 사람이 분리된 세 위치를 차지하고 각 몸 사이에 빈 공간이 보인다.

관계: person_a → seated_at → table.near_edge; person_b → stands_beyond → table.far_left; person_c → stands_beyond → table.far_right

관찰 게이트: 세 몸·탁자·사이 공간

혼동 경계: 움직임 순서; 권력·동의

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_56395d10386d545c8c4f6d2b729b99ce

## espfull_full_frame — 전신 프레임

One standing person is framed from the complete top of the head to both shoe soles, with visible margins above the head and below the shoes.

서 있는 한 사람이 머리 맨 위부터 양쪽 신발 바닥까지 화면에 들어오고 머리 위와 신발 아래 여백이 보인다.

관계: image.frame → contains → person.head_top; image.frame → contains → person.shoe_soles

관찰 게이트: 머리·양발·상하 여백

혼동 경계: 허벅지 크롭; 클로즈업

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_3b636dd51cfa5222b7dab469d60b6f93

## espfull_cowboy_frame — 허벅지 중간 크롭

One person fills a vertical frame from the top of the head down to mid-thigh; both hands and the waist are inside the frame, and the lower frame edge cuts across the thighs above the knees.

세로 화면이 한 인물의 머리 위부터 허벅지 중간까지 담고 양손과 허리가 화면 안에 있으며 아래 테두리가 무릎 위 허벅지를 가로지른다.

관계: image.lower_edge → crosses → person.mid_thigh; image.frame → contains → person.hands_and_waist

관찰 게이트: 머리부터 허벅지 중간; 양손·허리; 무릎 위 크롭

혼동 경계: 전신; 무릎 아래 크롭; 포즈 용어

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F03

후보: cand_20da5e42e8c45f63b9ae873ad95e31e8

## espfull_insert_watch — 손목시계 인서트

A close insert fills the frame with one wristwatch and its supporting wrist; the dial, strap joins and skin boundary remain sharp while the distant background is soft.

클로즈 인서트 화면을 손목시계 하나와 이를 받치는 손목이 채우고 시계판·줄 연결·피부 경계는 선명하며 먼 배경은 흐리다.

관계: watch.strap → wraps → person.wrist; image.frame → closely_contains → watch.dial_and_joins

관찰 게이트: 시계·손목 접점; 실제 작은 범위 크롭

혼동 경계: 시계형 카메라 기능; 중요 단서라는 진실

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_c2baa7df9e1250e99ba661461b30008d

## espfull_ots_frame — 어깨 너머 두 인물 구도

The near person’s shoulder and side of the head occupy one foreground edge; beyond that shoulder a separate person’s face and upper torso are in focus.

가까운 인물의 어깨와 머리 옆면이 전경 한쪽 가장자리를 차지하고 그 어깨 너머 별도 인물의 얼굴과 상체에 초점이 맞는다.

관계: person_near.shoulder → foreground_of → person_far.face; image.focus → on → person_far.face_and_torso

관찰 게이트: 전경 어깨·다른 사람 얼굴 분리

혼동 경계: 한 배우의 뒤돌아보기; 화면 속 사진

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F04

후보: cand_2b248a9939235decbf28f84148ca34e0

## espfull_pov_hands — 관찰자 손을 포함한 시점 프레임

Two hands enter from the lower image edge holding an open folder toward a doorway ahead, while the hand owner’s head and torso remain outside the frame.

화면 아래 가장자리에서 나온 두 손이 열린 폴더를 앞쪽 출입구를 향해 들고 손 주인의 머리와 몸통은 화면 밖에 있다.

관계: hands → enter_from → image.lower_edge; hands → hold → folder; folder → foreground_of → doorway

관찰 게이트: 아래서 들어온 손·폴더·앞 출입구

혼동 경계: 실제 관찰자 신원; 유일한 주관적 진실

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_fdc4b1d7ed4357a0b64c3f72487de8f8

## espfull_door_occlusion — 전경 문틀의 부분 가림

A near dark door jamb overlaps one outer edge of a person farther inside the room; the person’s face and both hands remain visible beyond the jamb.

가까운 어두운 문설주가 방 안쪽 인물의 바깥 가장자리 일부를 가리며 문설주 너머 얼굴과 양손은 보인다.

관계: door.jamb → occludes → person.outer_edge; person.face_and_hands → visible_beyond → door.jamb

관찰 게이트: 문틀·몸의 앞뒤 겹침; 얼굴·양손 유지

혼동 경계: 그림자 띠; 관찰자의 실제 은신

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_0f3c4f0dfaa05526919cfd644e1f353e

## espfull_window_frame — 창 속 인물의 내부 프레임

A rectangular window frame surrounds a person across a courtyard, with all four window borders visible inside the outer image frame and courtyard depth between them.

직사각 창틀이 안뜰 건너 인물을 둘러싸고 바깥 화면 안에 창의 네 변과 사이 안뜰 깊이가 보인다.

관계: window.four_borders → surround → person; courtyard.depth → between → window_and_person

관찰 게이트: 내부 네 변·외부 화면 분리; 사이 깊이

혼동 경계: 단순 인물 크롭; 관찰·고립 의도

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_7971d5ee67805339b40d2f17dbe7da20

## espfull_silhouette_frame — 어두운 외곽과 밝은 배경

A person’s head, coat and arms form a nearly featureless dark shape against a brighter doorway, with a clear continuous outer contour and no readable facial detail.

더 밝은 출입구 앞에서 인물의 머리·외투·팔이 내부 세부가 거의 없는 어두운 형태를 이루고 얼굴 세부 대신 이어진 바깥 윤곽이 선명하다.

관계: person.dark_contour → against → doorway.bright_field; person.face → has → unreadable_internal_detail

관찰 게이트: 밝은 배경·연속 외곽; 내부 세부 억제

혼동 경계: 얼굴 신원 유지 테스트와 동시 강제

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_fc790ca8bae35a089f5b5e1a06373ad0

## espfull_dutch_frame — 화면 자체의 기울기

The image frame remains rectangular while the room’s door uprights and horizon line are visibly tilted together relative to its vertical and horizontal edges.

화면은 직사각형이고 방의 문 수직선과 수평선이 화면의 수직·수평 테두리에 대해 함께 기울어 있다.

관계: room.door_uprights → tilted_relative_to → image.vertical_edge; room.horizon → tilted_relative_to → image.horizontal_edge

관찰 게이트: 두 환경 축과 화면 축 비교

혼동 경계: 배우 고개 기울임; 진단·불안 원인

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_241d54705fca513b8cd9e0d9093e9407

## espfull_lowkey_face — 명암이 분리된 로키

One side of a person’s face and one hand are selectively lit, while the opposite face side and most of the room remain dark but distinct from the lit contours.

인물 얼굴 한쪽과 손 하나에 선택적으로 빛이 닿고 반대쪽 얼굴과 방 대부분은 어둡되 밝은 윤곽과 구분된다.

관계: light → illuminates → person.face_side_and_hand; person.opposite_side → darker_than → person.lit_side

관찰 게이트: 선택적 명부·암부 비교

혼동 경계: 전체 노출 부족; 선악·의도

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_23b9ee1962385293beecf506f842bfa3

## espfull_rim_outline — 머리·외투 가장자리 림

A narrow rear-side light traces the outer hair edge and coat shoulder, separating those edges from a darker background while the central cloth remains dimmer.

뒤 옆쪽의 가는 빛이 머리카락 바깥 가장자리와 외투 어깨를 따라 어두운 배경과 분리하며 천 중앙은 더 어둡다.

관계: rear_side_light → traces → hair.outer_edge; rear_side_light → traces → coat.shoulder_edge; edge_light → separates_from → dark.background

관찰 게이트: 외곽 빛·배경 분리; 중앙보다 밝은 가장자리

혼동 경계: 정면 전체 조명; 헤일로 물체

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_c637e68bb8f65ea0924b882f656762f7

## espfull_dossier_spread — 도시어의 문서·사진 소유자

An open dossier lies on a table with a clipped portrait print on the left page and separate typed sheets on the right; the portrait remains bounded by its own paper edges.

탁자 위 열린 도시어 왼쪽 장에는 클립으로 고정한 인물 사진 인쇄물이, 오른쪽에는 별도 타자 문서가 있고 인물 이미지는 사진 종이의 경계 안에 있다.

관계: dossier.left_page → supports → portrait.print; portrait.depicted_person → bounded_by → portrait.paper_edges; dossier.right_page → supports → typed.sheets

관찰 게이트: 폴더·인쇄물·묘사된 인물 분리

혼동 경계: 문서 진위; 실제 신분·행위 증명

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_270c16ca489f58df9554164848457ee5

## espfull_film_strip — 문서 축소 필름의 물리 표면

A narrow translucent film strip rests across a light panel, with several rectangular document-like frames separated along the strip and a loose coil at one end.

가는 반투명 필름 띠가 라이트 패널 위에 놓이고 띠를 따라 문서처럼 보이는 직사각 프레임들이 분리되어 있으며 한쪽 끝은 느슨하게 감겨 있다.

관계: film.strip → rests_on → light.panel; document_like.frames → bounded_inside → film.strip; film.end → forms → loose.coil

관찰 게이트: 필름 띠·프레임 경계·코일

혼동 경계: 기록 해상도·실제 내용; 정확한 역사적 규격

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_4976b0b189b0522d90131975aaa99c87

## espfull_mini_camera — 작은 카메라의 크기 비교

A miniature camera body with a round lens and visible shutter button rests beside an adult-sized gloved hand, the camera and hand separate and fully visible.

원형 렌즈와 셔터 버튼이 보이는 초소형 카메라 본체가 성인 크기의 장갑 낀 손 옆에 놓이고 카메라와 손이 분리되어 모두 보인다.

관계: camera.lens → attached_to → camera.body; camera.body → beside → gloved.hand

관찰 게이트: 렌즈·본체·버튼; 손과 크기 비교

혼동 경계: 정확한 박물관 복제; 숨김 성공·실제 촬영

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_ee7865c9b1875b37ad3c1f5d7118eda6

## espfull_open_container — 일상 용기와 드러난 내부

An ordinary-looking pen case lies open on a table, its detached cover beside a clearly bounded inner compartment containing a folded paper.

평범해 보이는 펜 케이스가 탁자 위에 열려 있고 분리된 덮개 옆 경계가 분명한 내부 칸에 접힌 종이가 있다.

관계: case.compartment → contains → folded.paper; case.cover → separated_from → case.body

관찰 게이트: 열린 내부 칸·종이·덮개

혼동 경계: 탐지 회피 성능; 역사적 동전 장치와 동일성

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_1d8213ca005b54db8e14fb5faaa7a684

## espfull_disguise_tray — 분장 도구와 본래 인물 분리

A wig on a stand, a makeup palette and a small brush occupy separate places on a dressing table; the wig is not attached to any person.

분장대 위의 가발 스탠드·화장 팔레트·작은 붓이 분리된 자리에 있고 가발은 인물에 붙어 있지 않다.

관계: wig → rests_on → stand; palette → beside → brush; stand → rests_on → dressing.table

관찰 게이트: 가발·도구·사람 구분

혼동 경계: 실제 잠입 신분; 말투·습관 변화

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. F08

후보: cand_06f8e08965905d7aa04c841b59a06a7e

## espfull_consular_desk — 영사 창구의 물리 구획

A public counter stands before a glass partition with a document slot, and an open passport rests on the visitor side beneath the slot.

공공 창구 뒤 유리 칸막이에 문서 투입구가 있고 그 아래 방문자 쪽 창구 위에 열린 여권이 놓인다.

관계: glass.partition → has → document.slot; passport → rests_on → counter.visitor_side

관찰 게이트: 유리·투입구·문서·방향

혼동 경계: 기관 소속; 외교 면책·허가

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_ff994adf6cf3593e8c7b51a832523a63

## espfull_hotel_threshold — 호텔 문턱과 복도 구분

An open guest-room door separates a softly lit room from a longer corridor; the door latch, threshold and a small travel bag just inside the room are visible together.

열린 객실 문이 은은한 방과 긴 복도를 나누고 문 래치·문턱·방 안쪽 작은 여행가방이 함께 보인다.

관계: door.threshold → separates → room_and_corridor; travel.bag → rests_inside → room.threshold

관찰 게이트: 문·문턱·양쪽 공간·가방

혼동 경계: 익명성; 만남의 사적 의도

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_855dfdbcd7d7530f87da8a9401a3e32d

## espfull_checkpoint_documents — 검문 창구의 문서 접점

At a checkpoint booth a person’s hand holds one passport flat on the counter under a clear partition opening, while a second person stands on the opposite side.

검문 부스 창구의 투명 칸막이 입구 아래 한 인물의 손이 여권 하나를 평평하게 놓고 반대편에는 별도 인물이 서 있다.

관계: person_a.hand → holds → passport; passport → on → counter; partition.opening → between → person_a_and_person_b

관찰 게이트: 두 인물·손·여권·칸막이 분리

혼동 경계: 진짜 신원; 국경 통과 성공

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_11276ad03e5c51b1bd20fb00ba7811ba

## espfull_monitor_room — 화면 속 사람과 관찰실 구분

An observer sits before two monitors in a control room; each monitor contains a bounded image of a different corridor, while the observer and desk remain outside both screen images.

관찰실에서 한 관찰자가 모니터 두 대 앞에 앉고 각 화면에는 다른 복도의 경계 있는 이미지가 들어 있으며 관찰자와 책상은 두 화면 이미지 밖에 있다.

관계: monitor_a.screen → contains_image_of → corridor_a; monitor_b.screen → contains_image_of → corridor_b; observer → sits_outside → screen_images

관찰 게이트: 화면 두 개·이미지·실제 방 경계

혼동 경계: 실시간 감청; 관찰 대상 정체·소리

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_0aeb74d23e175e16b9f212e418966cb2

## espfull_social_table — 사교 모임의 공간 관계

Three people in ordinary evening clothes stand around a small table, each holding a separate glass, with a clear gap between their bodies.

평범한 저녁 외출복을 입은 세 사람이 작은 탁자 둘레에 서서 각각 다른 잔을 들고 몸 사이에는 분명한 간격이 있다.

관계: person_a.hand → holds → glass_a; person_b.hand → holds → glass_b; person_c.hand → holds → glass_c

관찰 게이트: 각 손·잔·몸 소유자 분리

혼동 경계: 공작 가담; 성적 동의·유혹; 대화 내용

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_ba05991576725c7f9bd167fb5bd35854

## espfull_mirror_boundary — 거울 속 모습의 소유 경계

A person stands beside a rectangular mirror; the reflected face is contained within the mirror border and aligns with the physical person’s head position outside that border.

한 인물이 직사각 거울 옆에 서 있고 반사된 얼굴은 거울 테두리 안에 있으며 테두리 밖 실제 인물의 머리 위치와 대응한다.

관계: mirror.reflected_face → bounded_by → mirror.border; mirror.reflected_face → corresponds_to → person.physical_head

관찰 게이트: 실제 인물·거울·반사면 경계

혼동 경계: 두 인격; 이중간첩; 다른 실재 인물

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_fc82573c504b5172b0eb48f03a249561

## espfull_narrow_view — 문틈 안의 먼 화면

Two near door edges form a narrow vertical opening through which a distant desk and one hand on its folder are visible, with the near edges softly out of focus.

가까운 문 가장자리 둘이 만든 세로로 좁은 틈 너머 먼 책상과 폴더 위 손 하나가 보이고 가까운 문 가장자리는 약하게 흐리다.

관계: door.edges → bound → narrow.opening; opening → reveals → distant.desk_and_hand

관찰 게이트: 양쪽 문 경계·틈·먼 손

혼동 경계: 실제 망원 초점거리; 불법 감시·의도

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_ed9892c9ecdc5e5f8a2524b826a4af89

## espfull_office_piles — 형광등 사무실의 서류 더미

A grey office desk holds three uneven paper stacks beneath a visible fluorescent ceiling fixture, with separate folder edges and a plain chair beside the desk.

회색 사무실 책상 위 고르지 않은 서류 더미 세 개가 보이는 천장 형광등 아래 놓이고 폴더 가장자리와 책상 옆 단순한 의자가 구분된다.

관계: paper.stacks → rest_on → desk; fluorescent.fixture → above → desk; chair → beside → desk

관찰 게이트: 서류 더미·조명기구·책상

혼동 경계: 관료적 소진·직책

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_080f1722c5bc59e68c34fa62cbfcace3

## espfull_sealed_case — 맥거핀의 닫힌 용기 표면

A closed hard case with two latched catches rests alone on a table; its interior contents are not visible.

잠금 걸쇠 두 개가 닫힌 하드 케이스가 탁자에 홀로 놓이고 내부 내용물은 보이지 않는다.

관계: case.catch_a → latched_to → case.body; case.catch_b → latched_to → case.body; case → rests_on → table

관찰 게이트: 닫힌 케이스·걸쇠; 내부 비가시

혼동 경계: 서사적 중요성; 실제 비밀 내용

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_2ef601e36d8054b7b380b08373b11e33

## espfull_annotated_print — 붉은 표시와 인쇄물

One printed photograph has a red circle drawn on its paper around a small depicted doorway, with the circle staying on the print rather than in the surrounding room.

인쇄 사진 속 작은 출입구 둘레에 종이 위 붉은 원이 그려져 있고 원은 주변 실제 방이 아니라 인쇄물 표면에 있다.

관계: red.circle → drawn_on → print.paper; red.circle → surrounds → print.depicted_doorway

관찰 게이트: 종이 경계·종이 위 원·묘사된 문

혼동 경계: 단서의 진실·거짓; 범인·레드헤링 역할

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_1a587797a414553889df510ec046eabc

## espfull_contact_sheet_window — 콘택트시트·관찰자·실제 창 분리

An observer holds a contact sheet beside an open dossier near a window; the sheet contains a grid of small photographs, while a separate courtyard lies beyond the real window and outside every printed image.

한 관찰자가 창 근처 열린 도시어 옆에서 콘택트시트를 들고 시트에는 작은 사진 격자가 있으며 별도 안뜰은 실제 창 너머에 있고 모든 인쇄 이미지 밖에 있다.

관계: observer.hands → hold → contact.sheet; contact.sheet → contains → printed.photo_grid; courtyard → beyond → real.window; dossier → beside → contact.sheet

관찰 게이트: 손·시트·격자; 실제 창·안뜰·인쇄물 분리

혼동 경계: 같은 사건·인물; 실시간 화면; 인쇄 이미지를 실제 공간으로 이동

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_4fa643ed03535151b29bfd2d0f46a441

## espfull_broken_seal — 끊어진 봉인 연결

An envelope has two torn halves of one paper seal attached to opposite flap edges, with a visible gap between the matching torn boundaries.

봉투의 마주한 덮개 가장자리에 한 종이 봉인의 찢어진 두 조각이 붙어 있고 대응하는 찢김 경계 사이에 틈이 보인다.

관계: seal.half_a → attached_to → envelope.flap_a; seal.half_b → attached_to → envelope.flap_b; seal.torn_edges → separated_by → gap

관찰 게이트: 봉투·봉인 두 조각·틈

혼동 경계: 누가 언제 열었는지; 정보 유출 성공

출처 범위: Listed sources support only the named bounded convention or professional context. Unlisted proposals are authored testable visual constructions, not source-established facts or verified plates. 

후보: cand_15388d8a730b5eaab0fb787270e822d8


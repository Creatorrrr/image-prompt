# 시각 의미 상세 카드

2026-10-06 KST. 120개 연구 단위이며 활성 profile/후보 수가 아니다. 각 카드의 영어·한국어 형태는 고유명사를 제거한 연구자 작성 명세다. 출처는 연결된 특정 사실만 확인하며 전체 형태·모든 참조 행을 자동 보증하지 않는다.

RESEARCH_DRAFT_NOT_RUNTIME_SCHEMA. 색·길이·동작·연령·몸 형태·원인·기능은 명시적으로 선택된 범위에만 적용한다.

## H001 기본 긴 로브

어깨에서 소매 달린 넉넉한 겉옷이 무릎 아래로 이어지고 옷자락과 다리 윤곽은 구별된다.

one loose sleeve-bearing outer garment descends from the shoulders; its torso cloth continues below the knees; the garment outline stays separate from the wearer's legs.

- 관찰 요소: one loose sleeve-bearing outer garment descends from the shoulders / its torso cloth continues below the knees / the garment outline stays separate from the wearer's legs
- 소유·관계: [{"id": "h001_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one loose sleeve-bearing outer garment descends from the shoulders", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h001_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its torso cloth continues below the knees", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h001_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the garment outline stays separate from the wearer's legs", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Robe is not automatically an open-front film uniform, a cape without sleeves, or a belted bathrobe.
- 출처 상태: TEXT_SUPPORTED; [S01](https://www.harrypotter.com/writing-by-jk-rowling/clothing)
- 기존 profile: costume_ccx_cc12_01, clothing_ct024_v1; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Existing profiles require an open vest/belt or wrap closure; neither may be imposed on plain robes.
- 참조 행: ref_001, ref_009, ref_031
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H002 셔츠·넥타이·니트·로브의 층

같은 착용자의 칼라 셔츠 위에 넥타이와 별도 니트가 있고 긴 로브가 그 바깥을 감싼다.

a collared shirt is the inner layer; a tie crosses that shirt beneath a separate knit neckline; an outer robe frames those inner layers on the same wearer.

- 관찰 요소: a collared shirt is the inner layer / a tie crosses that shirt beneath a separate knit neckline / an outer robe frames those inner layers on the same wearer
- 소유·관계: [{"id": "h002_r1", "subject": "shirt", "type": "inside", "object": "knit", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h002_r2", "subject": "tie", "type": "in_front_of", "object": "shirt", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h002_r3", "subject": "tie", "type": "passes_below", "object": "knit_neckline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h002_r4", "subject": "knit", "type": "inside", "object": "outer_robe", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A coat printed with shirt/tie graphics does not establish four separate layers; components on different people do not complete the relation.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S06](https://fashionista.com/2017/06/jany-temime-harry-potter-costume-designer-interview), [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257)
- 기존 profile: costume_ccx_cc02_02, costume_ccx_cc12_01; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Layer topology is invariant; shirt colour, tie motif, skirt/trousers and exact knit type remain separate optional choices.
- 참조 행: ref_002, ref_017, ref_031, ref_067, ref_109, ref_115, ref_120, ref_121
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H003 검정 겉감 안쪽의 유색 후드 면

후드가 로브 목둘레에 이어지고 접힌 가장자리 양쪽에 서로 다른 색의 안팎 면이 보인다.

one fabric hood joins the same outer robe neckline; the hood's inside surface contrasts with its outside; an opened fold exposes both surfaces with one continuous edge.

- 관찰 요소: one fabric hood joins the same outer robe neckline / the hood's inside surface contrasts with its outside / an opened fold exposes both surfaces with one continuous edge
- 소유·관계: [{"id": "h003_r1", "subject": "hood", "type": "attached_at", "object": "robe_neckline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h003_r2", "subject": "inside_colour", "type": "on", "object": "hood_inside", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h003_r3", "subject": "fold_edge", "type": "separates", "object": "hood_inside_and_outside", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A coloured scarf, background, separate cap or light spill is not hood lining.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S06](https://fashionista.com/2017/06/jany-temime-harry-potter-costume-designer-interview), [S25](https://x.com/masoq095/status/2105042738517295257)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Colour placement is scene-specific; third-film creator wording and one fan image do not determine every early-film hood.
- 참조 행: ref_007, ref_115
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H004 넥타이 표면의 사선 줄

묶인 넥타이의 긴 면 안에 서로 다른 색 띠가 비스듬히 반복된다.

a knot joins the narrow upper and wide lower tie portions; alternating colour bands cross that same tie diagonally; the band pattern remains inside the tie perimeter.

- 관찰 요소: a knot joins the narrow upper and wide lower tie portions / alternating colour bands cross that same tie diagonally / the band pattern remains inside the tie perimeter
- 소유·관계: [{"id": "h004_r1", "subject": "diagonal_bands", "type": "bounded_by", "object": "tie_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h004_r2", "subject": "tie_knot", "type": "continuous_with", "object": "tie_blade", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Diagonal stripes on the robe or background cannot satisfy a tie pattern; a ribbon bow is a separate structure.
- 출처 상태: PIXELS_AND_PRODUCT_SCOPE; [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257), [S33](https://harrypottershop.co.uk/products/ravenclaw-house-tie)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_CONTEXT_REVIEW — Keep stripe width/order and selected palette open unless requested; replica navy/silver is product scope.
- 참조 행: ref_002, ref_003, ref_004, ref_005, ref_006, ref_115, ref_120
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H005 니트 목선·소매끝의 가는 배색

니트의 목선이나 소매 끝을 가는 색 띠가 따라가며 몸판 바탕과 분리된다.

a knit garment has a readable neck or cuff edge; a narrow contrasting band follows that same edge; the broad knit body retains its distinct ground colour.

- 관찰 요소: a knit garment has a readable neck or cuff edge / a narrow contrasting band follows that same edge / the broad knit body retains its distinct ground colour
- 소유·관계: [{"id": "h005_r1", "subject": "contrast_band", "type": "follows", "object": "knit_neck_or_cuff_edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A necklace, shirt collar, isolated patch or overall coloured jumper is not an edge-following trim.
- 출처 상태: SAMPLE_PIXELS; [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257)
- 기존 profile: clothing_ct066_v2; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Existing neckline binding isn't necessarily knit-in trim; construction must remain separate from appearance.
- 참조 행: ref_002, ref_003, ref_004, ref_005, ref_115
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H006 로브 가슴의 작은 문장 패치

가슴의 지정한 옷 패널에 몸판보다 작은 문장 테두리가 놓이고 피부와 분리된다.

a bounded emblem occupies one selected chest panel; the emblem scale is smaller than the torso panel; its contour stays within that declared garment surface.

- 관찰 요소: a bounded emblem occupies one selected chest panel / the emblem scale is smaller than the torso panel / its contour stays within that declared garment surface
- 소유·관계: [{"id": "h006_r1", "subject": "small_emblem", "type": "localized_on", "object": "selected_garment_chest_panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A freestanding crest, skin tattoo, printed background or generic large bird does not prove a chest badge.
- 출처 상태: SAMPLE_AND_REPLICA_SCOPE; [S25](https://x.com/masoq095/status/2105042738517295257), [S33](https://harrypottershop.co.uk/products/ravenclaw-house-tie)
- 기존 profile: clothing_ct067_v1; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Patch, embroidery and print are manufacturing alternatives; house membership and values are not inferred.
- 참조 행: ref_002, ref_003, ref_004, ref_005, ref_006, ref_014, ref_017, ref_115
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H007 기숙사 배색의 판본 선택

같은 옷의 지정한 면에 선택된 두 색을 배치하고 다른 판본의 두 색은 대안으로 남긴다.

one selected palette belongs to specified garment regions; a different palette remains an alternative version; the version label does not add anatomy or personality.

- 관찰 요소: one selected palette belongs to specified garment regions / a different palette remains an alternative version / the version label does not add anatomy or personality
- 소유·관계: [{"id": "h007_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one selected palette belongs to specified garment regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h007_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a different palette remains an alternative version", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h007_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the version label does not add anatomy or personality", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Blue/bronze book canon and navy/silver shop design must not be merged into one compulsory palette; green doesn't mean villain.
- 출처 상태: VERSION_CONTEXT; [S02](https://www.harrypotter.com/writing-by-jk-rowling/colours), [S33](https://harrypottershop.co.uk/products/ravenclaw-house-tie), [S34](https://www.harrypotter.com/house/ravenclaw)
- 기존 profile: cr_restricted_subject; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Store four house/book palettes and filmed/product colourways in version metadata; no character-name hard alias.
- 참조 행: ref_003, ref_004, ref_005, ref_006, ref_120
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H008 크라운과 챙이 분리되는 뾰족모자

가늘어지는 모자 몸체가 둘레의 챙에서 솟고 머리 위의 별도 물체로 얹힌다.

a tapered crown rises from the hat base; one brim surrounds that crown base; the hat rests as a separate object above the head.

- 관찰 요소: a tapered crown rises from the hat base / one brim surrounds that crown base / the hat rests as a separate object above the head
- 소유·관계: [{"id": "h008_r1", "subject": "tapered_crown", "type": "rises_from", "object": "brim", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h008_r2", "subject": "brim", "type": "encircles", "object": "crown_base", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h008_r3", "subject": "hat", "type": "rests_above", "object": "wearer_head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Animal horns or a triangular hairstyle are not hat parts; pointed crown alone doesn't prove a brim.
- 출처 상태: TEXT_SUPPORTED; [S01](https://www.harrypotter.com/writing-by-jk-rowling/clothing), [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: costume_ccx_cc11_01; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Preserve existing broad-brim selected relation; soft collapse and narrow millinery brim are sibling variants.
- 참조 행: ref_008, ref_019, ref_136
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H009 팔꿈치 위에서 끝나는 어깨 망토

어깨 덮개가 팔꿈치 위에서 끝나고 그 아래에 별도 옷의 몸판과 팔이 이어진다.

one short outer cloth covers the shoulders; its lower edge ends above the elbows; a separate lower garment continues below that edge.

- 관찰 요소: one short outer cloth covers the shoulders / its lower edge ends above the elbows / a separate lower garment continues below that edge
- 소유·관계: [{"id": "h009_r1", "subject": "capelet", "type": "covers", "object": "wearer_shoulders", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h009_r2", "subject": "capelet_hem", "type": "ends_above", "object": "wearer_elbows", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h009_r3", "subject": "lower_garment", "type": "continues_below", "object": "capelet_hem", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A long cloak, extended collar or built-in sleeve doesn't automatically satisfy a separate capelet.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct011_v1; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Do not broaden shoulder-supported full cape into a fixed capelet length.
- 참조 행: ref_010, ref_045
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H010 긴 코트와 내부 정장의 수직선

긴 코트의 옷깃 안쪽에 별도 셔츠나 조끼가 보이고 겉층의 옷자락이 더 아래로 내려간다.

a tailored outer coat has its own lapels or upright collar; a separate shirt or vest remains visible inside; the coat hem continues below the inner jacket or waistline.

- 관찰 요소: a tailored outer coat has its own lapels or upright collar / a separate shirt or vest remains visible inside / the coat hem continues below the inner jacket or waistline
- 소유·관계: [{"id": "h010_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a tailored outer coat has its own lapels or upright collar", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h010_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate shirt or vest remains visible inside", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h010_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the coat hem continues below the inner jacket or waistline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Long coat, open robe and tailcoat are not interchangeable; black tie colour isn't proof of a bow tie.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S17](https://www.harrypotter.com/news/exclusive-eddie-redmayne-interview-on-newt-scamanders-coat), [S18](https://www.harrypotter.com/news/the-touch-of-glamour-in-colin-farrell-fantastic-beasts-costume), [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers)
- 기존 profile: costume_ccx_cc02_02, costume_ccx_cc12_01; 기존 후보: 없음
- 제안 처리: REUSE_OR_BUNDLE — Stage, school suit and formal ball cases keep separate hem/closure/neckwear alternatives.
- 참조 행: ref_009, ref_049, ref_066, ref_068, ref_102, ref_106, ref_124
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H011 목둘레의 세운 칼라와 앞여밈

목 아래를 세운 깃이 둘러싸고 넓게 눕는 라펠과 분리되며 앞여밈이 아래로 이어진다.

an upright collar encircles the neck base; the collar edge stands raised around the neck; a separate front closure descends from that collar.

- 관찰 요소: an upright collar encircles the neck base / the collar edge stands raised around the neck / a separate front closure descends from that collar
- 소유·관계: [{"id": "h011_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "an upright collar encircles the neck base", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h011_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the collar edge stands raised around the neck", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h011_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate front closure descends from that collar", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: High neckline alone doesn't prove a standing collar; qipao or religious identity must not be inferred.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S18](https://www.harrypotter.com/news/the-touch-of-glamour-in-colin-farrell-fantastic-beasts-costume), [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape), [S40](https://www.harrypotter.com/features/first-and-last-appearance-of-our-favourite-harry-potter-characters)
- 기존 profile: costume_ccx_cc04_01; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Button count, tight fit, black colour and particular character costume need separate selection.
- 참조 행: ref_019, ref_020, ref_028, ref_048, ref_068, ref_108, ref_124, ref_135
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H012 목에 감아 앞에서 접은 넓은 천

넓은 천이 목을 두른 뒤 가슴 위에서 접히거나 묶이고 셔츠와 다른 끝부분이 보인다.

a broad cloth band wraps the neck; the same cloth folds or knots at the upper chest; wider fabric ends remain distinct from the shirt front.

- 관찰 요소: a broad cloth band wraps the neck / the same cloth folds or knots at the upper chest / wider fabric ends remain distinct from the shirt front
- 소유·관계: [{"id": "h012_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a broad cloth band wraps the neck", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h012_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the same cloth folds or knots at the upper chest", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h012_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "wider fabric ends remain distinct from the shirt front", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A slim tie, bow tie or unattached vertical jabot is not this wrap-and-fold relation.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct104_v2; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Existing narrow scarf lacks broad cravat geometry; colour and exact historical period are optional.
- 참조 행: ref_026, ref_136
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H013 목 아래로 겹쳐 내려오는 레이스 자보

깃 아래 장식이 여러 주름으로 가슴 위에 내려오며 목을 둘러싸는 띠와 구별된다.

a lace or light cloth ornament starts below the collar; several projecting folds descend over the upper chest; its free edges stay separate from a circumferential neck band.

- 관찰 요소: a lace or light cloth ornament starts below the collar / several projecting folds descend over the upper chest / its free edges stay separate from a circumferential neck band
- 소유·관계: [{"id": "h013_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a lace or light cloth ornament starts below the collar", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h013_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "several projecting folds descend over the upper chest", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h013_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its free edges stay separate from a circumferential neck band", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A circular ruff, scarf knot, tie or sleeve lace cannot substitute for front-hanging jabot.
- 출처 상태: TEXT_AND_GLOSSARY; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S29](https://resources.metmuseum.org/resources/metpublications/pdf/Man_and_the_Horse_an_illustrated_history_of_equestrian_apparel.pdf)
- 기존 profile: clothing_ct043_v1; 기존 후보: 없음
- 제안 처리: NEW_OR_SIBLING — Do not map circular ruff to jabot; exact fastening and film lace subtype remain unverified.
- 참조 행: ref_009, ref_050, ref_137
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H014 누빔 조끼 위의 문장 장식

조끼 표면에 봉제선으로 나뉜 볼륨 칸과 작은 문장이 함께 있고 망토와 별도 층이다.

repeated seam-bounded padded cells occupy a vest panel; a separate crest motif lies on that same panel; the vest remains inside or under an outer cloak.

- 관찰 요소: repeated seam-bounded padded cells occupy a vest panel / a separate crest motif lies on that same panel / the vest remains inside or under an outer cloak
- 소유·관계: [{"id": "h014_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "repeated seam-bounded padded cells occupy a vest panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h014_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate crest motif lies on that same panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h014_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the vest remains inside or under an outer cloak", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A printed diamond pattern doesn't prove padded quilting; crest on another person's coat isn't the vest motif.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Source identifies the duelling ensemble; stitched cell scale and crest outline need a closer still before exact canon use.
- 참조 행: ref_027
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H015 망토 가장자리에 매달린 술

망토 둘레의 부착선 밖으로 실이나 끈 끝이 각각 늘어진다.

separate thread or cord ends attach along a cloak edge; the attachment line follows that same cloth perimeter; individual ends hang free beyond the cloth edge.

- 관찰 요소: separate thread or cord ends attach along a cloak edge / the attachment line follows that same cloth perimeter / individual ends hang free beyond the cloth edge
- 소유·관계: [{"id": "h015_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "separate thread or cord ends attach along a cloak edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h015_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the attachment line follows that same cloth perimeter", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h015_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "individual ends hang free beyond the cloth edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Printed fringe, feathers elsewhere or tears without an attachment row are not tassels/fringe.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct068_v2, orn_profile_gd38; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — A few tassel bundles and a continuous fringe row are alternatives, not automatically equal.
- 참조 행: ref_027, ref_147
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H016 한 손에만 착용한 장갑

지정한 한 손은 장갑 안에 있고 다른 손은 그 장갑 밖이며 첫 손목에 커프 경계가 보인다.

one selected hand lies inside a separate glove; the other hand remains outside that glove; the glove boundary ends at its own cuff on the first wrist.

- 관찰 요소: one selected hand lies inside a separate glove / the other hand remains outside that glove / the glove boundary ends at its own cuff on the first wrist
- 소유·관계: [{"id": "h016_r1", "subject": "glove", "type": "encloses", "object": "selected_hand", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h016_r2", "subject": "other_hand", "type": "outside", "object": "glove", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h016_r3", "subject": "glove_cuff", "type": "terminates_at", "object": "selected_wrist", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: One visible gloved hand with the other hidden cannot prove one-glove-only cardinality.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct106_v1; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Fingerless gloves aren't the default; wearer-relative left/right must be explicit only when requested.
- 참조 행: ref_027
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H017 큰 주머니의 두꺼운 외투

두꺼운 외투의 몸판에 큰 주머니가 붙고 소매와 옷자락의 두께가 구별된다.

a bulky overcoat encloses the torso; large bounded pockets attach to that same coat; the hem and sleeve fabric retain substantial visible thickness.

- 관찰 요소: a bulky overcoat encloses the torso / large bounded pockets attach to that same coat / the hem and sleeve fabric retain substantial visible thickness
- 소유·관계: [{"id": "h017_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a bulky overcoat encloses the torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h017_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "large bounded pockets attach to that same coat", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h017_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the hem and sleeve fabric retain substantial visible thickness", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Actual animal hide is not established by the word moleskin; cotton moleskin and fictional overcoat identity are separate.
- 출처 상태: SEED_LEAD; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: clothing_ct058_v1; 기존 후보: 없음
- 제안 처리: HOLD_SOURCE_AND_REUSE — Hagrid's exact overcoat fabric isn't verified by this publisher page. Generic pocket construction is reusable.
- 참조 행: ref_021
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H018 해짐·색바램·얼룩의 국소 배치

옷 끝의 풀린 실, 천 안쪽의 바랜 면, 접힌 곳의 얼룩을 같은 옷에 각각 배치한다.

frayed thread ends remain on an actual garment edge; faded patches remain inside the same cloth surface; creases or dirt occupy local folds within a traceable garment outline.

- 관찰 요소: frayed thread ends remain on an actual garment edge / faded patches remain inside the same cloth surface / creases or dirt occupy local folds within a traceable garment outline
- 소유·관계: [{"id": "h018_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "frayed thread ends remain on an actual garment edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h018_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "faded patches remain inside the same cloth surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h018_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "creases or dirt occupy local folds within a traceable garment outline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Distress isn't a torn body, a printed grunge background, or proof of poverty, imprisonment or age.
- 출처 상태: SAMPLE_AND_SOURCE_LEAD; [S41](https://www.wbstudiotour.co.uk/wp-content/uploads/2020/06/at-home-costume-distressing-activity-sheet-1.pdf), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_RELATION_WITH_SOURCE_HOLD — Separate reversible cloth state from biography; source PDF details need acquisition before exact process claims.
- 참조 행: ref_036, ref_037, ref_038, ref_069, ref_126, ref_147, ref_148
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H019 가로·세로 줄무늬가 남는 낡은 죄수복

낡은 옷의 줄무늬가 마모된 끝에서도 남고 몸·겉외투와 분리된다.

alternating bands lie on a loose garment panel; worn edges interrupt but don't replace those bands; the garment remains separate from the body and outer coat.

- 관찰 요소: alternating bands lie on a loose garment panel / worn edges interrupt but don't replace those bands / the garment remains separate from the body and outer coat
- 소유·관계: [{"id": "h019_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "alternating bands lie on a loose garment panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h019_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "worn edges interrupt but don't replace those bands", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h019_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the garment remains separate from the body and outer coat", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Striped shirt alone does not establish prison history, a particular inmate or authentic uniform period.
- 출처 상태: SEED_LEAD; [S41](https://www.wbstudiotour.co.uk/wp-content/uploads/2020/06/at-home-costume-distressing-activity-sheet-1.pdf)
- 기존 profile: clothing_ct093_v1; 기존 후보: 없음
- 제안 처리: HOLD_SOURCE_OR_GENERIC — Sirius film garment direction/colour needs a versioned still; generic stripes stay advisory.
- 참조 행: ref_037
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H020 초기 넓고 두꺼운 경기 로브

두꺼운 경기 겉옷의 넓은 옷자락과 별도 보호구가 구분된다.

a broad outer robe extends around the athlete; its thick cloth creates a large free hem; separate protective accessories remain outside or beneath that robe.

- 관찰 요소: a broad outer robe extends around the athlete / its thick cloth creates a large free hem / separate protective accessories remain outside or beneath that robe
- 소유·관계: [{"id": "h020_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a broad outer robe extends around the athlete", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h020_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its thick cloth creates a large free hem", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h020_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "separate protective accessories remain outside or beneath that robe", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Thin later kit, ordinary black schoolwear or hem motion without a robe isn't the early design.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OPTIONAL_VARIANT — Early film label is provenance; a static frame does not prove flight or wind movement.
- 참조 행: ref_011
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H021 가벼운 경기복과 등판 이름·번호

가벼운 경기복의 등판에 글자나 숫자가 놓이고 보호구 윤곽은 분리된다.

a lighter sports garment has a readable back panel; letters or digits remain on that same back panel; armour or pads retain separate contours.

- 관찰 요소: a lighter sports garment has a readable back panel / letters or digits remain on that same back panel / armour or pads retain separate contours
- 소유·관계: [{"id": "h021_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a lighter sports garment has a readable back panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h021_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "letters or digits remain on that same back panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h021_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "armour or pads retain separate contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Front crest or background lettering cannot satisfy a back number; an unseen back isn't evidence.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OPTIONAL_VARIANT — Name/number is version-specific and requires back visibility; don't require it in frontal-only prompts.
- 참조 행: ref_012
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H022 운동복 위의 관절 보호대

지정한 팔꿈치·무릎·정강이에 별도 보호 패널이 놓이고 띠나 경계가 같은 보호대에 속한다.

a separate pad covers the selected elbow knee or shin; straps or bounded panels belong to that same pad; the pad follows the contour of its declared limb segment.

- 관찰 요소: a separate pad covers the selected elbow knee or shin / straps or bounded panels belong to that same pad / the pad follows the contour of its declared limb segment
- 소유·관계: [{"id": "h022_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate pad covers the selected elbow knee or shin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h022_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "straps or bounded panels belong to that same pad", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h022_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the pad follows the contour of its declared limb segment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Helmet, clothing print or a pad on another limb doesn't establish the selected joint protection.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/)
- 기존 profile: costume_ccx_cc13_02; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Keep helmet, chest padding, leather appearance and sport function independent unless selected.
- 참조 행: ref_013, ref_077
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H023 손뜨개 니트의 큰 한 글자

니트의 얽힌 실 표면 안에 가슴 중앙의 큰 한 글자가 놓인다.

interlocked yarn loops form the knit garment surface; one large letter occupies its central chest panel; the letter contour is bounded by the knitted chest surface.

- 관찰 요소: interlocked yarn loops form the knit garment surface / one large letter occupies its central chest panel / the letter contour is bounded by the knitted chest surface
- 소유·관계: [{"id": "h023_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "interlocked yarn loops form the knit garment surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h023_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one large letter occupies its central chest panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h023_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the letter contour is bounded by the knitted chest surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A logo backdrop, necklace letter or non-letter emblem is not a chest monogram; print vs knit-in construction remains distinct.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_CONTEXT_REVIEW — Request must select legible character if exact text matters; don't force R/H on generic winter knit.
- 참조 행: ref_024
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H024 길이가 다른 천 단의 치마 층

치마의 가로 천 단이 위아래로 겹치고 같은 허리 지지부에서 이어진다.

two or more separate horizontal cloth edges cross the skirt; upper layers overlap lower layers; all layers remain connected to the same skirt support.

- 관찰 요소: two or more separate horizontal cloth edges cross the skirt / upper layers overlap lower layers / all layers remain connected to the same skirt support
- 소유·관계: [{"id": "h024_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "two or more separate horizontal cloth edges cross the skirt", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h024_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "upper layers overlap lower layers", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h024_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "all layers remain connected to the same skirt support", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Vertical pleats, painted horizontal stripes or several unrelated skirts aren't tiered layering.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct018_v2; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Exact tier count, colour gradient, long hem and chiffon are separate choices.
- 참조 행: ref_051, ref_143
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H025 얇은 천의 겹침과 색 농도

얇은 천 두 면의 끝이 따로 보이고 겹친 부분의 빛 투과가 한 겹보다 줄어든다.

a thin flowing panel has a complete fabric edge; an overlapping panel remains separately traceable; the overlap transmits less light than one unlayered panel.

- 관찰 요소: a thin flowing panel has a complete fabric edge / an overlapping panel remains separately traceable / the overlap transmits less light than one unlayered panel
- 소유·관계: [{"id": "h025_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a thin flowing panel has a complete fabric edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h025_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "an overlapping panel remains separately traceable", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h025_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the overlap transmits less light than one unlayered panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Glow, fog or darker painted stripes don't prove layered translucent cloth; transparency doesn't prove exposure or erotic intention.
- 출처 상태: TEXT_SUPPORTED; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct091_v2; 기존 후보: sheer_organza_chiffon_transmission
- 제안 처리: REUSE_OR_MODIFIER — Fiber chemistry is sourced only for documented film costumes; generic material appearance remains visual.
- 참조 행: ref_051, ref_140
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H026 예복 색과 재단의 판본 분기

선택한 예복의 색·목선·치마 형태를 같은 판본 안에 유지하고 다른 판본은 대안으로 남긴다.

one selected gown retains its stated colour field; its selected skirt and neckline stay within that version; another adaptation remains an alternative rather than an extra layer.

- 관찰 요소: one selected gown retains its stated colour field / its selected skirt and neckline stay within that version / another adaptation remains an alternative rather than an extra layer
- 소유·관계: [{"id": "h026_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one selected gown retains its stated colour field", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h026_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its selected skirt and neckline stay within that version", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h026_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "another adaptation remains an alternative rather than an extra layer", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Periwinkle/pink, white/plain vs black bird motif and lilac/red are different cases; source only confirms some pairs.
- 출처 상태: VERSION_CONTEXT; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Hermione wedding lilac/red and bridesmaid palettes remain seed leads until primary verification.
- 참조 행: ref_050, ref_051, ref_078, ref_079, ref_080, ref_081, ref_082, ref_084
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H027 짧은 파티 드레스의 밖으로 뻗는 세 층

짧은 드레스의 세 천 단이 몸에서 바깥으로 뻗고 각각의 끝 윤곽을 유지한다.

three distinct skirt tiers belong to one short dress; each tier edge projects outward from the body; the tiers retain separate free contours above the knees.

- 관찰 요소: three distinct skirt tiers belong to one short dress / each tier edge projects outward from the body / the tiers retain separate free contours above the knees
- 소유·관계: [{"id": "h027_r1", "subject": "three_tiers", "type": "part_of", "object": "same_short_dress", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h027_r2", "subject": "tier_edges", "type": "project_from", "object": "wearer_body", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h027_r3", "subject": "each_tier", "type": "retains", "object": "separate_free_edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Three painted bands or a generic long tiered gown aren't three-dimensional short tiers.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S43](https://contentful.harrypotter.com/usf1vwtuqyxm/4i0wa5BOBWYACKeQyUyaSo/ba0a6c04fa6c7cb2c2cf59eeadd0ba39/LunaLovegood_WB_F6_LunaLovegoodSlugClubChristmasPartyWithSanguiniAndEldredWorple_Still_080615_Port.jpg?fm=jpg&q=75&w=914)
- 기존 profile: clothing_ct018_v2; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — The still confirms short flared silhouette; metallic shine and star earrings aren't part of tier topology.
- 참조 행: ref_074
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H028 두 새 문양이 만드는 하트 윤곽

몸판의 새 문양 두 개가 안쪽으로 마주 굽어 하나의 하트 윤곽을 만들고 옷 표면에 남는다.

two separate bird motifs occupy the same bodice; their inward-facing curves jointly outline a heart; both motifs remain bounded by that same garment surface.

- 관찰 요소: two separate bird motifs occupy the same bodice / their inward-facing curves jointly outline a heart / both motifs remain bounded by that same garment surface
- 소유·관계: [{"id": "h028_r1", "subject": "bird_motif_a", "type": "on", "object": "same_bodice", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h028_r2", "subject": "bird_motif_b", "type": "on", "object": "same_bodice", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h028_r3", "subject": "inward_curves", "type": "jointly_outline", "object": "heart", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Two independent birds, a printed heart without birds, or biological wings attached to the wearer don't complete the relation.
- 출처 상태: TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: clothing_ct067_v1; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Source names phoenixes, not swans. Pattern geometry doesn't prove applique technique or immortality.
- 참조 행: ref_079
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H029 세로 잔주름 위의 비대칭 잎 장식

드레스의 세로 잔주름 위에 한쪽 어깨·목선의 잎 모양 장식을 국소 배치한다.

fine folds run vertically down the gown; a bounded leaf-shaped ornament lies at one shoulder or neckline; the ornament attaches at one explicitly selected local point.

- 관찰 요소: fine folds run vertically down the gown / a bounded leaf-shaped ornament lies at one shoulder or neckline / the ornament attaches at one explicitly selected local point
- 소유·관계: [{"id": "h029_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "fine folds run vertically down the gown", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h029_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a bounded leaf-shaped ornament lies at one shoulder or neckline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h029_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the ornament attaches at one explicitly selected local point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A leaf-print fabric, two symmetrical straps or ordinary drape wrinkles aren't a confirmed asymmetric ornament.
- 출처 상태: SEED_LEAD; [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct063_v1, clothing_ct067_v1; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Fleur ball exact attachment, leaf count and pleat construction need an original still; generic morphology can be researched.
- 참조 행: ref_046
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H030 옷 가장자리의 레이스와 몸판 분리

지정한 옷 끝·패널의 실 조직에 구멍이 있고 옆의 불투명 몸판은 별도 경계를 유지한다.

openwork lace occupies a bounded garment edge or panel; lace openings are formed by thread structure; an adjacent opaque garment panel retains its own contour.

- 관찰 요소: openwork lace occupies a bounded garment edge or panel / lace openings are formed by thread structure / an adjacent opaque garment panel retains its own contour
- 소유·관계: [{"id": "h030_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "openwork lace occupies a bounded garment edge or panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h030_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "lace openings are formed by thread structure", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h030_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "an adjacent opaque garment panel retains its own contour", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Printed flowers, random tears or actual injured skin aren't lace; distressed lace isn't default uncovered skin.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct090_v2; 기존 후보: 없음
- 제안 처리: REUSE_OR_SIBLING — Mesh ground, bar-linked lace and lace-trim placement remain different selected structures.
- 참조 행: ref_052, ref_064, ref_137
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H031 코르셋 패널과 별도 여밈

몸통을 감싸는 패널의 세로선과 그 옷 가장자리를 잇는 여밈을 구분한다.

separate fitted panels enclose the torso; reinforcement or seam channels run along those panels; the closure joins declared edges of that same garment.

- 관찰 요소: separate fitted panels enclose the torso / reinforcement or seam channels run along those panels / the closure joins declared edges of that same garment
- 소유·관계: [{"id": "h031_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "separate fitted panels enclose the torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h031_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "reinforcement or seam channels run along those panels", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h031_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the closure joins declared edges of that same garment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A fitted dress alone doesn't prove a separate corset, a busk or lacing; back lacing can't be invented from a front photo.
- 출처 상태: GENERIC_TECHNICAL; [S27](https://www.vam.ac.uk/articles/a-z-opus-anglicanum), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: costume_ccx_cc26_01, orn_profile_gd40; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Bellatrix exact construction remains a film-case acquisition lead. Preserve garment subtype and existing adult guards where present.
- 참조 행: ref_064, ref_146
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H032 의상 전체 조합의 선택 가능 묶음

선택한 옷 요소만 같은 착용자의 층·색 관계로 묶고 선택하지 않은 요소는 대안으로 남긴다.

several selected garment atoms share one wearer; their layering and colour relations are explicitly chosen; unselected atoms remain optional across alternative ensembles.

- 관찰 요소: several selected garment atoms share one wearer / their layering and colour relations are explicitly chosen / unselected atoms remain optional across alternative ensembles
- 소유·관계: [{"id": "h032_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "several selected garment atoms share one wearer", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h032_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "their layering and colour relations are explicitly chosen", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h032_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "unselected atoms remain optional across alternative ensembles", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A bundle hit cannot lock every component; male/female presentation doesn't select trousers, skirt, hair length or makeup.
- 출처 상태: OPTIONAL_DESIGN; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S17](https://www.harrypotter.com/news/exclusive-eddie-redmayne-interview-on-newt-scamanders-coat), [S18](https://www.harrypotter.com/news/the-touch-of-glamour-in-colin-farrell-fantastic-beasts-costume), [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: BUNDLE_ONLY — Prototype bundles are blue capelet set, school layering, formal coat/vest, adult black dress. Effects must be the union of actually adopted components.
- 참조 행: ref_045, ref_048, ref_049, ref_067, ref_068, ref_102, ref_106, ref_115, ref_120, ref_121, ref_124, ref_125
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H033 세운 깃 재킷·가슴 띠·한쪽 털 덮개

세운 깃의 재킷 위로 가슴을 가로지르는 띠가 있고 한쪽 어깨의 털 덮개가 분리된다.

an upright-collar jacket remains the torso garment; a distinct diagonal strap crosses its chest; a separate fur-like shoulder cover occupies one selected side.

- 관찰 요소: an upright-collar jacket remains the torso garment / a distinct diagonal strap crosses its chest / a separate fur-like shoulder cover occupies one selected side
- 소유·관계: [{"id": "h033_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "an upright-collar jacket remains the torso garment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h033_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a distinct diagonal strap crosses its chest", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h033_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate fur-like shoulder cover occupies one selected side", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A sash printed on the jacket, full symmetric fur collar or different wearers' parts aren't the same ensemble.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: costume_ccx_cc04_01; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Tonks' military coat is text-supported; Krum's exact red strap/fur ensemble still needs a source still.
- 참조 행: ref_048, ref_063
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H034 분홍 재킷·스커트와 작은 리본

분홍 계열 재킷과 치마를 분리하고 작은 리본을 목선·소품의 지정 부위에 한정한다.

a tailored jacket sits above a separate skirt; a small bow remains local to a selected collar or accessory; both garments keep the chosen pink colour family.

- 관찰 요소: a tailored jacket sits above a separate skirt / a small bow remains local to a selected collar or accessory / both garments keep the chosen pink colour family
- 소유·관계: [{"id": "h034_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a tailored jacket sits above a separate skirt", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h034_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a small bow remains local to a selected collar or accessory", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h034_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "both garments keep the chosen pink colour family", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Pink garment colour isn't authority, cruelty, femininity or a compulsory bow everywhere.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S39](https://www.harrypotter.com/features/colour-coordinating-the-wizarding-world)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: BUNDLE_REVIEW — Pink progression is source-supported; exact handbag, cut and ribbon need scene-level corroboration.
- 참조 행: ref_059
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H035 여러 시점 사이의 분홍 강도 변화

여러 시점의 같은 의상 계열을 비교하여 조명 차이를 통제한 뒤 분홍 강도의 차이를 판단한다.

the same costume family appears in multiple frames; pink chroma differs across matched garments; lighting and exposure differences are controlled before attributing design change.

- 관찰 요소: the same costume family appears in multiple frames / pink chroma differs across matched garments / lighting and exposure differences are controlled before attributing design change
- 소유·관계: [{"id": "h035_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the same costume family appears in multiple frames", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h035_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "pink chroma differs across matched garments", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h035_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "lighting and exposure differences are controlled before attributing design change", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: One saturated-pink still can't prove increasing power or progressive colour change.
- 출처 상태: TEMPORAL_ONLY; [S39](https://www.harrypotter.com/features/colour-coordinating-the-wizarding-world)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: TEMPORAL_ONLY — Keep only a selected pink state in still-image candidates; sequence narrative remains outside still hard obligations.
- 참조 행: ref_060
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H036 길고 매끈하게 내려오는 생머리

머리카락이 두피에서 어깨 아래로 이어지고 큰 굴곡 없이 정돈된 방향을 유지한다.

hair strands continue from the visible scalp region; the length descends past a selected shoulder landmark; most strands follow a coherent low-curvature direction.

- 관찰 요소: hair strands continue from the visible scalp region / the length descends past a selected shoulder landmark / most strands follow a coherent low-curvature direction
- 소유·관계: [{"id": "h036_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "hair strands continue from the visible scalp region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h036_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the length descends past a selected shoulder landmark", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h036_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "most strands follow a coherent low-curvature direction", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Long pale hair isn't female identity, TS, pure blood or mandatory platinum chemistry; a wig isn't biology without declared representation.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films), [S21](https://www.harrypotter.com/features/five-differences-between-the-younger-draco-malfoy-and-the-draco-we-see-in-cursed-child), [S24](https://x.com/redteneri/status/2102398387194626330), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: blonde_long_hair
- 제안 처리: MODIFIER_REVIEW — Existing long-blonde candidate combines colour/length; prefer independent texture/length so locks are respected.
- 참조 행: ref_028, ref_061, ref_108, ref_114, ref_121, ref_131
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H037 짧은 머리끝의 불규칙한 방향

짧은 머리의 뿌리에서 이어진 여러 끝이 서로 다른 방향으로 들린다.

short hair retains visible scalp-to-tip continuity; several tips point in different directions; the irregularity remains local to the short hair mass.

- 관찰 요소: short hair retains visible scalp-to-tip continuity / several tips point in different directions / the irregularity remains local to the short hair mass
- 소유·관계: [{"id": "h037_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "short hair retains visible scalp-to-tip continuity", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h037_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "several tips point in different directions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h037_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the irregularity remains local to the short hair mass", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Large uniform curls, long tangled hair or general image grain aren't short tousled spikes.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_FORM — Black colour, thin face, scar and eye colour remain separate atoms; tousled does not require wet hair.
- 참조 행: ref_014, ref_134
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H038 전체 부피와 잔머리가 퍼지는 머리

머리 전체의 큰 부피 밖으로 가는 잔머리가 퍼지고 한 가닥의 늘어짐과 구분된다.

one hair mass extends broadly beyond the head outline; fine flyaway strands project at its perimeter; the broad volume is distributed across the scalp hair mass.

- 관찰 요소: one hair mass extends broadly beyond the head outline / fine flyaway strands project at its perimeter / the broad volume is distributed across the scalp hair mass
- 소유·관계: [{"id": "h038_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one hair mass extends broadly beyond the head outline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h038_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "fine flyaway strands project at its perimeter", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h038_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the broad volume is distributed across the scalp hair mass", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A bushy animal tail, a smooth large wig or a few short spikes doesn't establish bushy scalp hair.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: ca_bushy_tail; 기존 후보: 없음
- 제안 처리: NEW_CARRIER_SIBLING — Do not reuse nonhuman tail ownership for scalp hair; volume and wave pitch are separate.
- 참조 행: ref_015, ref_132
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H039 장발과 거친 수염의 독립된 경계

머리 옆에서 내려오는 장발과 턱·볼에서 시작하는 수염의 뿌리를 구별한다.

long head hair descends beside the face; coarse beard hair starts from jaw and chin regions; both masses remain distinguishable at their origins.

- 관찰 요소: long head hair descends beside the face / coarse beard hair starts from jaw and chin regions / both masses remain distinguishable at their origins
- 소유·관계: [{"id": "h039_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "long head hair descends beside the face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h039_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "coarse beard hair starts from jaw and chin regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h039_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "both masses remain distinguishable at their origins", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A neck fur ruff or one wig covering the face isn't a biological beard; body size doesn't establish hair texture.
- 출처 상태: SEED_LEAD; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: ca_body_fur_ruff; 기존 후보: full_beard
- 제안 처리: REUSE_AND_CASE_HOLD — Keep generic beard candidate; Hagrid exact hair/body bundle requires first-film source qualification.
- 참조 행: ref_021
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H040 이마에서 뒤로 눕힌 머리 방향

이마의 머리 경계에서 가닥이 두피 뒤쪽으로 누워 이어지며 젖음·묶임과는 구별된다.

front hair starts at the forehead hairline; the strands sweep backward over the scalp; separated visible strands retain a consistent backward surface direction.

- 관찰 요소: front hair starts at the forehead hairline / the strands sweep backward over the scalp / separated visible strands retain a consistent backward surface direction
- 소유·관계: [{"id": "h040_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "front hair starts at the forehead hairline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h040_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the strands sweep backward over the scalp", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h040_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "separated visible strands retain a consistent backward surface direction", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Wet-look is not intrinsic to slick-back; a ponytail alone doesn't prove the front is slicked back.
- 출처 상태: PARTIAL_TEXT_AND_PIXELS; [S21](https://www.harrypotter.com/features/five-differences-between-the-younger-draco-malfoy-and-the-draco-we-see-in-cursed-child), [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: 없음; 기존 후보: slicked_back_wet
- 제안 처리: SIBLING_REVIEW — Current wet-look candidate should retain wet meaning; add dry swept-back sibling instead of weakening it.
- 참조 행: ref_017, ref_124, ref_130
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H041 큰 물결 머리와 작은 나선 컬 구분

긴 가닥이 넓은 굴곡을 번갈아 만들고 작은 나선 컬과 분리된다.

long hair follows alternating broad curves; each curve spans a larger section than a tight ringlet; the waves remain continuous with their scalp roots.

- 관찰 요소: long hair follows alternating broad curves / each curve spans a larger section than a tight ringlet / the waves remain continuous with their scalp roots
- 소유·관계: [{"id": "h041_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "long hair follows alternating broad curves", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h041_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each curve spans a larger section than a tight ringlet", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h041_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the waves remain continuous with their scalp roots", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Bushy volume, ringlet loops and short hair disorder are not equivalent wave geometries.
- 출처 상태: PARTIAL_TEXT_AND_PIXELS; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_EXISTING_CANDIDATE_REVIEW — Actor/year/colour and a neat updo are separate; a film hair example isn't the universal character hairstyle.
- 참조 행: ref_015, ref_026, ref_051, ref_066, ref_069, ref_081
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H042 가닥별 굵은 나선 컬

분리된 머리 묶음이 반복 나선을 만들며 얼굴 옆으로 이어진다.

a separated hair section follows repeated spiral turns; the turns retain a continuous strand path; several continuous spiral sections descend beside the face.

- 관찰 요소: a separated hair section follows repeated spiral turns / the turns retain a continuous strand path / several continuous spiral sections descend beside the face
- 소유·관계: [{"id": "h042_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separated hair section follows repeated spiral turns", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h042_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the turns retain a continuous strand path", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h042_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "several continuous spiral sections descend beside the face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Flat S-waves, artificial jewellery spirals or loop braids are not ringlets.
- 출처 상태: DESIGN_PROPOSAL; [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: ca_coiled_head_elements; 기존 후보: 없음
- 제안 처리: NEW_FORM — Ringlet villainess interpretation is a proposed design, not verified default Female Draco canon.
- 참조 행: ref_123, ref_133
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H043 머리색 두 영역의 위치 관계

같은 머리의 지정한 윗부분·앞쪽과 얼굴 옆·아래쪽에 다른 밝기의 면을 배치한다.

a dark hair region occupies the selected crown or front roll; a lighter region occupies selected face-side or lower sections; the boundary stays within one connected hairstyle.

- 관찰 요소: a dark hair region occupies the selected crown or front roll / a lighter region occupies selected face-side or lower sections / the boundary stays within one connected hairstyle
- 소유·관계: [{"id": "h043_r1", "subject": "dark_region", "type": "on", "object": "selected_crown_or_front_roll", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h043_r2", "subject": "light_region", "type": "on", "object": "selected_side_or_lower_hair", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h043_r3", "subject": "both_regions", "type": "part_of", "object": "one_hairstyle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Lighting-only contrast, dark roots, left/right half split and face-framing highlights are different placements.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films), [S42](https://contentful.harrypotter.com/usf1vwtuqyxm/5zu7yWx27uKEquuAeMSKOe/87198c6433e31cdef347f1bae4b8a63a/NarcissaMalfoy_WB_F6_NarcissaMalfoyFullbody_Promo_080615_Port.jpg?fm=jpg&q=75&w=914)
- 기존 profile: 없음; 기존 후보: faded_blonde_rooted_hair
- 제안 처리: NEW_PLACEMENT_OR_MODIFIER — Observed promo has dark crown/front roll with lighter sides/lower sections; back unseen. Do not universalize seed's dark-back description.
- 참조 행: ref_070, ref_119
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H044 짧고 삐친 유색 머리

짧은 머리의 솟은 끝에 선택한 색이 놓이고 외투색·조명과 분리된다.

short scalp hair forms separate upward tips; a selected colour occupies those hair strands; hair colour remains separate from coat colour or lighting.

- 관찰 요소: short scalp hair forms separate upward tips / a selected colour occupies those hair strands / hair colour remains separate from coat colour or lighting
- 소유·관계: [{"id": "h044_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "short scalp hair forms separate upward tips", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h044_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a selected colour occupies those hair strands", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h044_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "hair colour remains separate from coat colour or lighting", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Purple coat, scene wash or a smooth bob isn't spiky coloured hair; colour doesn't establish magic transformation.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_ATOM_BUNDLE — Tonks violet/pink states stay alternative versions; film red coat is separate.
- 참조 행: ref_063
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H045 뒤로 모은 번과 긴 머리의 연결

머리 가닥이 뒤·위의 한 지점으로 모여 작은 감긴 덩어리를 만든다.

hair strands gather toward a rear or upper tie point; the gathered bundle coils into a compact bun; the bun remains continuous with the same scalp hair.

- 관찰 요소: hair strands gather toward a rear or upper tie point / the gathered bundle coils into a compact bun / the bun remains continuous with the same scalp hair
- 소유·관계: [{"id": "h045_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "hair strands gather toward a rear or upper tie point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h045_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the gathered bundle coils into a compact bun", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h045_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the bun remains continuous with the same scalp hair", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A detached hat, bilateral tails or simply swept-back hair doesn't establish a connected bun.
- 출처 상태: TEXT_SUPPORTED; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: bilateral_twin_tail_gather; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Single bun vs two scalp ties remains distinct; neatness and hair colour aren't anatomy.
- 참조 행: ref_019, ref_046, ref_051
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H046 길게 내려오는 흰 수염

턱과 아래 볼에서 시작한 밝은 수염이 선택한 가슴 높이 아래로 이어진다.

beard hair begins at chin and lower cheeks; the same beard extends below the chest landmark when selected; light hair retains separable strand edges.

- 관찰 요소: beard hair begins at chin and lower cheeks / the same beard extends below the chest landmark when selected / light hair retains separable strand edges
- 소유·관계: [{"id": "h046_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "beard hair begins at chin and lower cheeks", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h046_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the same beard extends below the chest landmark when selected", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h046_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "light hair retains separable strand edges", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: White scarf, robe trim or a neck ruff isn't a beard; long beard doesn't imply age, wisdom or rank.
- 출처 상태: TEXT_SUPPORTED; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: 없음; 기존 후보: full_beard
- 제안 처리: REUSE_OR_MODIFIER — Waist length and exact white/silver shade are version choices; early ornate vs late muted robes remain separate.
- 참조 행: ref_018, ref_071
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H047 입 양쪽으로 퍼지는 큰 콧수염

윗입술 위의 굵은 털이 입 양쪽으로 내려가거나 퍼지고 턱수염과 구별된다.

facial hair starts above the upper lip; thick ends extend down or sideways beside the mouth; the upper-lip attachment and extended ends remain continuously traceable.

- 관찰 요소: facial hair starts above the upper lip / thick ends extend down or sideways beside the mouth / the upper-lip attachment and extended ends remain continuously traceable
- 소유·관계: [{"id": "h047_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "facial hair starts above the upper lip", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h047_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "thick ends extend down or sideways beside the mouth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h047_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the upper-lip attachment and extended ends remain continuously traceable", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A full beard, tusks or lip shadow isn't a walrus-style moustache.
- 출처 상태: SEED_LEAD; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Slughorn book silver moustache/green eyes and missing film moustache need an exact primary book citation.
- 참조 행: ref_073
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H048 가는 원형 안경테와 코 다리

두 눈 위치의 원형 테가 콧등의 다리와 관자쪽 다리로 이어진다.

two circular rims enclose separate eye-region lenses; a bridge joins those rims across the nose; temple arms remain connected to that same frame.

- 관찰 요소: two circular rims enclose separate eye-region lenses / a bridge joins those rims across the nose / temple arms remain connected to that same frame
- 소유·관계: [{"id": "h048_r1", "subject": "left_rim", "type": "encloses", "object": "left_eye_region_lens", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h048_r2", "subject": "right_rim", "type": "encloses", "object": "right_eye_region_lens", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h048_r3", "subject": "nose_bridge", "type": "joins", "object": "same_two_rims", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Iris outlines, a single monocle, round earring or two detached circles aren't connected spectacles.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: ca_spectacle_frame; 기존 후보: wireframe_round_glasses
- 제안 처리: REUSE_OR_SHAPE_MODIFIER — Reuse general frame topology and existing round-glasses candidate; do not make every glasses request circular.
- 참조 행: ref_014, ref_030
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H049 반달형 렌즈 테의 낮은 윗선

렌즈 아래에는 곡선 테가 있고 위에는 낮고 평평한 선이 있으며 두 테가 코 다리로 연결된다.

each lens rim has a lower curved arc; its upper edge is lower and flatter than a full circle; the two half-rims connect through one nose bridge.

- 관찰 요소: each lens rim has a lower curved arc / its upper edge is lower and flatter than a full circle / the two half-rims connect through one nose bridge
- 소유·관계: [{"id": "h049_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each lens rim has a lower curved arc", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h049_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its upper edge is lower and flatter than a full circle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h049_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the two half-rims connect through one nose bridge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Tiny oval glasses or full circular frames aren't half-moon geometry.
- 출처 상태: TEXT_SUPPORTED; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: ca_spectacle_frame; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Frame topology reused; selected half-moon shape new or modifier. Wearer intellect isn't evidence.
- 참조 행: ref_018
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H050 안경 렌즈 안에서만 커지는 눈

테가 있는 렌즈 안에서만 눈이 주변 얼굴보다 크게 보인다.

the same eye region is seen through a bounded lens; the lens changes apparent eye scale relative to adjacent face; the magnified appearance stays inside the lens perimeter.

- 관찰 요소: the same eye region is seen through a bounded lens / the lens changes apparent eye scale relative to adjacent face / the magnified appearance stays inside the lens perimeter
- 소유·관계: [{"id": "h050_r1", "subject": "lens", "type": "bounds", "object": "magnified_eye_projection", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h050_r2", "subject": "adjacent_face", "type": "outside", "object": "lens_boundary", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Globally enlarged anime eyes, physical buphthalmos or a prosthetic eye isn't lens magnification.
- 출처 상태: TEXT_SUPPORTED; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers)
- 기존 profile: ca_spectacle_frame; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Trelawney exact optical magnitude/temple thickness require a close still; never diagnose health from pixels.
- 참조 행: ref_039
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H051 피부 표면에 분산된 작은 주근깨 점

지정한 얼굴 피부에 작고 경계가 있는 불규칙·둥근 색점이 분산된다.

many small pigment-like dots occupy selected skin regions; each dot retains a small bounded irregular or rounded contour; their distribution follows the surface of one declared face.

- 관찰 요소: many small pigment-like dots occupy selected skin regions / each dot retains a small bounded irregular or rounded contour / their distribution follows the surface of one declared face
- 소유·관계: [{"id": "h051_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "many small pigment-like dots occupy selected skin regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h051_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each dot retains a small bounded irregular or rounded contour", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h051_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "their distribution follows the surface of one declared face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Grain, acne lesions, drawn star stickers or stains elsewhere aren't this selected pattern; red hair does not require freckles. Pixels alone cannot establish natural pigment versus painted dots.
- 출처 상태: SEED_LEAD; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_ATOM_REVIEW — Ron's precise source appearance is a lead; natural origin needs declared context and source evidence. Generic visible-dot morphology makes no ethnicity or health claim.
- 참조 행: ref_016
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H052 상대적으로 큰 앞니

같은 입에서 윗앞니의 폭·돌출을 옆 치아와 비교해 드러낸다.

upper central incisors belong to the visible mouth; their width or projection differs relative to neighbouring teeth; the comparison remains within the same dentition.

- 관찰 요소: upper central incisors belong to the visible mouth / their width or projection differs relative to neighbouring teeth / the comparison remains within the same dentition
- 소유·관계: [{"id": "h052_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "upper central incisors belong to the visible mouth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h052_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "their width or projection differs relative to neighbouring teeth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h052_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the comparison remains within the same dentition", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Fangs, open-mouth darkness or lower teeth alone aren't enlarged upper incisors.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: OWNER_SLOT_REVIEW — eye_detail is not a valid final owner for teeth; use existing facial/anatomical carrier or hold instead of forcing this suggested slot.
- 참조 행: ref_015
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H053 곡선으로 돌출하는 코

코가 얼굴에서 이어져 돌출하고 콧등의 옆선이 볼록한 곡선을 만든다.

one nose projects continuously from the face; its bridge profile has a clear convex curve; the nose tip remains separate from a mask projection.

- 관찰 요소: one nose projects continuously from the face / its bridge profile has a clear convex curve / the nose tip remains separate from a mask projection
- 소유·관계: [{"id": "h053_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one nose projects continuously from the face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h053_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "its bridge profile has a clear convex curve", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h053_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the nose tip remains separate from a mask projection", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A separate mask nose, a snake slit or strong shadow isn't a hooked biological nose.
- 출처 상태: TEXT_SUPPORTED; [S30](https://www.harrypotter.com/features/harry-potter-whos-who-professors-edition-dumbledore-mcgonagall-snape)
- 기존 profile: ca_projecting_face_mask; 기존 후보: 없음
- 제안 처리: NEW_CARRIER_SIBLING — No ancestry or villain trait inferred. Film actor face and book descriptor remain separate.
- 참조 행: ref_020, ref_088
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H054 좁아지는 턱끝과 얼굴 윤곽

볼·아래턱 윤곽이 턱끝으로 좁아지며 얼굴 축 안에서 비교된다.

cheek contours narrow toward the lower jaw; the jaw converges into a relatively narrow chin; the declared breadth comparison uses one stated view of that face.

- 관찰 요소: cheek contours narrow toward the lower jaw / the jaw converges into a relatively narrow chin / the declared breadth comparison uses one stated view of that face
- 소유·관계: [{"id": "h054_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "cheek contours narrow toward the lower jaw", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h054_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the jaw converges into a relatively narrow chin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h054_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the declared breadth comparison uses one stated view of that face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A turned head or wide-angle distortion doesn't establish a permanently pointed face.
- 출처 상태: TEXT_SUPPORTED; [S40](https://www.harrypotter.com/features/first-and-last-appearance-of-our-favourite-harry-potter-characters)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: REUSE_EXISTING_FACE_REVIEW — Do not add a character-specific genetic facial type; perspective and bony structure require distinct evidence.
- 참조 행: ref_017, ref_028, ref_068, ref_088, ref_120
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H055 눈색은 홍채 안의 독립 속성

동공 주위의 홍채 경계 안에 선택한 색을 한정하고 양쪽 눈의 소유를 유지한다.

a bounded iris surrounds a distinct pupil; the selected iris colour stays inside that boundary; left and right eye regions retain their own ownership.

- 관찰 요소: a bounded iris surrounds a distinct pupil / the selected iris colour stays inside that boundary / left and right eye regions retain their own ownership
- 소유·관계: [{"id": "h055_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a bounded iris surrounds a distinct pupil", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h055_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the selected iris colour stays inside that boundary", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h055_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "left and right eye regions retain their own ownership", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Eye colour does not mean house colour, magic, purity, a person's identity or hair colour.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films), [S24](https://x.com/redteneri/status/2102398387194626330), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: sca_f05_central; 기존 후보: 없음
- 제안 처리: MODIFIER_REVIEW — Harry book green/film blue and fan gray/green/blue are version-specific; central heterochromia is not ordinary iris colour.
- 참조 행: ref_014, ref_017, ref_060, ref_119, ref_120
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H056 주변 기준과 비교하는 체구·키

같은 공간의 사람·책상 같은 기준과 연결된 몸을 비교하고 발의 지지면을 확인한다.

a declared body remains one connected figure; a shared-plane person or object gives a scale reference; feet and support surfaces clarify the relative height.

- 관찰 요소: a declared body remains one connected figure / a shared-plane person or object gives a scale reference / feet and support surfaces clarify the relative height
- 소유·관계: [{"id": "h056_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a declared body remains one connected figure", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h056_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a shared-plane person or object gives a scale reference", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h056_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "feet and support surfaces clarify the relative height", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Low camera angle or foreground placement alone doesn't prove giant/small stature; race and health are not inferred.
- 출처 상태: SEED_LEAD; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: OWNER_AND_GEOMETRY_REVIEW — Filius/Maxime/Hagrid case scale requires versioned body/scene evidence; do not copy prop-model dimensions into creature anatomy.
- 참조 행: ref_021, ref_023, ref_047
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H057 피로·수척함과 복식 상태 분리

얼굴의 드러난 윤곽, 옷의 여유·주름, 자세를 각각 기록한다.

selected facial planes have stronger visible contours; clothes show local slack or wrinkles; pose and clothing traces are described independently from mental state.

- 관찰 요소: selected facial planes have stronger visible contours / clothes show local slack or wrinkles / pose and clothing traces are described independently from mental state
- 소유·관계: [{"id": "h057_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "selected facial planes have stronger visible contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h057_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "clothes show local slack or wrinkles", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h057_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "pose and clothing traces are described independently from mental state", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Hollow-looking cheeks, disordered clothes or under-eye shadow don't prove fatigue, illness, captivity or guilt.
- 출처 상태: SEED_LEAD; [S41](https://www.wbstudiotour.co.uk/wp-content/uploads/2020/06/at-home-costume-distressing-activity-sheet-1.pdf)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Require explicit requested visual axes rather than one 'exhausted prisoner' keyword-to-body obligation.
- 참조 행: ref_037, ref_038, ref_069, ref_071, ref_126
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H058 피부 위의 짧고 각진 번개형 선

이마의 지정한 피부에 짧은 선이 여러 번 각지게 꺾이고 그 선 주변만 색·높이가 달라진다.

a narrow line remains on a selected forehead skin region; several angular bends form one connected short path; skin relief or colour differs locally along that path.

- 관찰 요소: a narrow line remains on a selected forehead skin region / several angular bends form one connected short path / skin relief or colour differs locally along that path
- 소유·관계: [{"id": "h058_r1", "subject": "angular_scar_path", "type": "localized_on", "object": "forehead_skin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h058_r2", "subject": "successive_bends", "type": "continuous_with", "object": "same_path", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A smooth scratch, rune, hair strand or crossing scar network isn't the same path; book centre/side position cannot be invented.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: ca_irregular_scar_lines; 기존 후보: bm_scar_surface
- 제안 처리: SIBLING_REVIEW — Existing intersecting-scar profile requires crossings; a nonintersecting lightning path must not inherit them.
- 참조 행: ref_014, ref_092
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H059 얼굴 흉터의 국소 경로와 높이

같은 피부의 불규칙한 선에 국소 색·높이 차이가 이어진다.

irregular narrow lines lie on one selected skin region; local colour or relief follows those line paths; the paths remain separate from a fabric seam or drawn cosmetic mark.

- 관찰 요소: irregular narrow lines lie on one selected skin region / local colour or relief follows those line paths / the paths remain separate from a fabric seam or drawn cosmetic mark
- 소유·관계: [{"id": "h059_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "irregular narrow lines lie on one selected skin region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h059_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "local colour or relief follows those line paths", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h059_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the paths remain separate from a fabric seam or drawn cosmetic mark", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A face contour, makeup streak, blood drip or coat seam isn't healed scar form; injury cause isn't visual proof.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S12](https://www.harrypotter.com/writing-by-jk-rowling/illness-and-disability), [S36](https://www.harrypotter.com/features/harry-potter-101-dark-magical-objects)
- 기존 profile: ca_irregular_scar_lines; 기존 후보: bm_scar_surface
- 제안 처리: REUSE_OR_SUBTYPE — Crossing number and healed/fresh state are explicitly selected; don't demand intersections for every scar.
- 참조 행: ref_055, ref_094
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H060 한 손의 검은 변색·줄어든 부피

같은 팔에 이어진 한 손의 피부만 어둡고 작게 쭈그러져 비교 부위와 다르다.

one hand remains anatomically connected to its own forearm; local dark discolouration stays on that hand; creased shrunken surface differs from the unaffected comparison region.

- 관찰 요소: one hand remains anatomically connected to its own forearm / local dark discolouration stays on that hand / creased shrunken surface differs from the unaffected comparison region
- 소유·관계: [{"id": "h060_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one hand remains anatomically connected to its own forearm", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h060_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "local dark discolouration stays on that hand", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h060_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "creased shrunken surface differs from the unaffected comparison region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A black glove, broad skin tone, mud or a shadow doesn't establish withered/discoloured hand; curse cause is contextual.
- 출처 상태: SEED_LEAD; [S36](https://www.harrypotter.com/features/harry-potter-101-dark-magical-objects)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Dumbledore case needs scene/source confirmation; retain horror morphology without health diagnosis.
- 참조 행: ref_072, ref_097
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H061 한 눈 자리의 인공 구체와 고정부

한쪽 눈 자리에 인공 눈의 홍채·외곽과 고정부가 같은 연결로 놓인다.

one artificial eye occupies a selected orbital region; the eye has its own bounded iris and housing; a bounded mount or interface joins that same artificial eye.

- 관찰 요소: one artificial eye occupies a selected orbital region / the eye has its own bounded iris and housing / a bounded mount or interface joins that same artificial eye
- 소유·관계: [{"id": "h061_r1", "subject": "artificial_eye", "type": "occupies", "object": "selected_orbit", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h061_r2", "subject": "housing", "type": "supports", "object": "same_artificial_eye", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h061_r3", "subject": "ordinary_other_eye", "type": "separate_from", "object": "replacement", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Blue iris alone, glasses, an eyepatch or a mechanical eye mounted on a door isn't an orbital replacement.
- 출처 상태: TEXT_SUPPORTED; [S11](https://www.harrypotter.com/fact-file/objects/mad-eye-moodys-eye), [S12](https://www.harrypotter.com/writing-by-jk-rowling/illness-and-disability)
- 기존 profile: sca_x04; 기존 후보: 없음
- 제안 처리: NEW_CARRIER_RELATION — Film strap/side location must be checked from a still; 360-degree motion/vision needs temporal evidence.
- 참조 행: ref_055, ref_095
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H062 몸 끝점과 소켓에서 이어지는 의족

남은 다리 끝에 연결부가 맞닿고 그 지점에서 보철 구간이 지지면 쪽으로 이어진다.

a residual leg ends at a declared body boundary; an interface meets that same residual endpoint; one prosthetic segment continues from the interface toward support.

- 관찰 요소: a residual leg ends at a declared body boundary / an interface meets that same residual endpoint / one prosthetic segment continues from the interface toward support
- 소유·관계: [{"id": "h062_r1", "subject": "socket", "type": "meets", "object": "same_residual_limb_endpoint", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h062_r2", "subject": "prosthetic_segment", "type": "continues_from", "object": "socket", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h062_r3", "subject": "segment", "type": "reaches_toward", "object": "support_plane", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A wooden staff, stiff boot or detached leg-shaped object isn't a connected limb replacement.
- 출처 상태: TEXT_SUPPORTED; [S12](https://www.harrypotter.com/writing-by-jk-rowling/illness-and-disability)
- 기존 profile: bm_prosthetic_connection; 기존 후보: 없음
- 제안 처리: REUSE_WITH_GUARDS — Existing profile explicitly requires an adult subject. Preserve that guard and do not impose modern hardware on fictional wood without evidence.
- 참조 행: ref_055
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H063 팔에 이어진 금속성 대체 손

같은 팔 끝에 손 모양 대체물이 이어지고 그 손의 손가락과 금속성 반사 면이 구별된다.

a hand-shaped replacement connects to one forearm endpoint; fingers articulate as parts of that same replacement; metal-like reflections remain on the replacement surface.

- 관찰 요소: a hand-shaped replacement connects to one forearm endpoint / fingers articulate as parts of that same replacement / metal-like reflections remain on the replacement surface
- 소유·관계: [{"id": "h063_r1", "subject": "replacement_hand", "type": "continues_from", "object": "same_forearm_endpoint", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h063_r2", "subject": "replacement_fingers", "type": "part_of", "object": "replacement_hand", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h063_r3", "subject": "metal_like_reflection", "type": "on", "object": "replacement_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Metal glove over an intact hand, independent severed-hand prop or another actor's hand isn't replacement anatomy.
- 출처 상태: TEXT_SUPPORTED; [S36](https://www.harrypotter.com/features/harry-potter-101-dark-magical-objects)
- 기존 profile: bm_prosthetic_connection; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Do not force a visible socket or ordinary human biology on magic replacement; static shine doesn't establish silver chemistry or powers.
- 참조 행: ref_058, ref_096
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H064 낮은 코 돌출과 두 가는 콧구멍

얼굴의 코 돌출을 낮추고 가는 콧구멍 두 개를 같은 머리의 면 안에 유지한다.

the facial surface has greatly reduced nose projection; two narrow nostril openings remain on that same face; the nostril region remains continuous with the declared facial surface.

- 관찰 요소: the facial surface has greatly reduced nose projection / two narrow nostril openings remain on that same face / the nostril region remains continuous with the declared facial surface
- 소유·관계: [{"id": "h064_r1", "subject": "nostril_openings", "type": "on", "object": "same_flattened_facial_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h064_r2", "subject": "altered_nose_region", "type": "continuous_with", "object": "head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Ordinary nose shadow, reptile mask or slit pupils aren't slit nostrils; all snake-like faces don't require red eyes.
- 출처 상태: TEXT_SUPPORTED; [S09](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/)
- 기존 profile: ca_projecting_face_mask; 기존 후보: 없음
- 제안 처리: NEW_CARRIER_RELATION — Book red eyes vs film face needs a separate exact eye source; film production dots/contacts are not body details.
- 참조 행: ref_056, ref_098
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H065 팔 피부의 해골·입에서 나온 뱀 문양

지정한 아래팔 피부의 해골 입에서 뱀의 선이 나오고 두 부분이 같은 피부 문양이다.

a skull motif remains on a selected forearm surface; a serpent path emerges from the skull mouth; both motif parts share that same skin carrier.

- 관찰 요소: a skull motif remains on a selected forearm surface / a serpent path emerges from the skull mouth / both motif parts share that same skin carrier
- 소유·관계: [{"id": "h065_r1", "subject": "skull_motif", "type": "on", "object": "forearm_skin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h065_r2", "subject": "serpent_path", "type": "emerges_from", "object": "skull_mouth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h065_r3", "subject": "serpent_path", "type": "on", "object": "same_forearm_skin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Sky sign, jewellery, actual snake or decal on a sleeve isn't forearm marking; owner and surface must be explicit.
- 출처 상태: TEXT_SUPPORTED; [S10](https://www.harrypotter.com/fact-file/magical-miscellany/the-dark-mark)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_TOPOLOGY — Tattoo-like representation doesn't establish membership, cause, touch activation or real-world ideology.
- 참조 행: ref_093
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H066 몸 내부를 통해 보이는 배경

인물의 윤곽이 유지되면서 몸 안쪽을 통해 뒤의 배경이 읽히고 옷·몸의 투명도를 같은 방식으로 처리한다.

a complete declared figure contour remains readable; background features remain visible through its interior; body and clothing opacity are consistently represented across the selected region.

- 관찰 요소: a complete declared figure contour remains readable / background features remain visible through its interior / body and clothing opacity are consistently represented across the selected region
- 소유·관계: [{"id": "h066_r1", "subject": "background_features", "type": "visible_through", "object": "figure_interior", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h066_r2", "subject": "figure_contour", "type": "bounds", "object": "same_translucent_region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Desaturation, white clothes, fog around a solid body or projected light alone isn't transparency.
- 출처 상태: TEXT_SUPPORTED; [S44](https://www.harrypotter.com/features/the-shrewd-skills-of-severus-snape)
- 기존 profile: human_ghost_identity_breach; 기존 후보: translucent_spirit_glow_surface
- 제안 처리: SIBLING_SCOPE_REVIEW — Former life, death and ghost identity need contextual evidence; do not weaken existing ghost-identity meaning into an effect.
- 참조 행: ref_030, ref_099
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H067 후드 속 얼굴 가림과 지면 위 간격

후드가 머리를 가리고 긴 천이 이어지며 부유를 선택한 경우 가장 아래 윤곽과 지면 사이에 틈이 보인다.

a hood covers the declared head region; long cloth continues below that hood; a visible gap separates the figure's lowest body or cloth from the support plane when floating is selected.

- 관찰 요소: a hood covers the declared head region / long cloth continues below that hood / a visible gap separates the figure's lowest body or cloth from the support plane when floating is selected
- 소유·관계: [{"id": "h067_r1", "subject": "hood", "type": "covers", "object": "head_region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h067_r2", "subject": "long_cloth", "type": "continues_from", "object": "hood", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h067_r3", "subject": "lowest_figure_contour", "type": "separated_from", "object": "support_plane_if_floating_selected", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A standing hooded person, feet cropped out or blowing cloth without support-plane evidence doesn't prove hovering.
- 출처 상태: TEXT_SUPPORTED; [S15](https://www.harrypotter.com/fact-file/creatures/dementor)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_BUNDLE — Concealment and hovering are separate obligations; 'Dementor' doesn't authorize soul-harm event or all physical details automatically.
- 참조 행: ref_042
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H068 긴 사지·마른 몸통의 늑대형 변형체

지정한 비인간 머리의 주둥이와 같은 마른 몸통에 이어진 긴 관절 사지를 구분한다.

one declared nonhuman head has a projecting muzzle; long articulated limbs attach to the same narrow torso; sparse fur or exposed joints stay on that body model.

- 관찰 요소: one declared nonhuman head has a projecting muzzle / long articulated limbs attach to the same narrow torso / sparse fur or exposed joints stay on that body model
- 소유·관계: [{"id": "h068_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one declared nonhuman head has a projecting muzzle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h068_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "long articulated limbs attach to the same narrow torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h068_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "sparse fur or exposed joints stay on that body model", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A furry quadruped wolf, an independent costume head or human thinness alone isn't this film-specific creature form.
- 출처 상태: SEED_LEAD; [S09](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Lupin film sparse-fur design still needs a primary image/creator source; no real illness/danger inference.
- 참조 행: ref_043, ref_100
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H069 인간 얼굴 위의 생물학적 고양이 변형

변형된 얼굴의 털 면·주둥이 수염·머리에 이어진 귀를 구분한다.

a declared transformed face carries continuous fur-bearing regions; whiskers emerge from its muzzle region; ear bases join the declared fur-bearing head surface.

- 관찰 요소: a declared transformed face carries continuous fur-bearing regions / whiskers emerge from its muzzle region / ear bases join the declared fur-bearing head surface
- 소유·관계: [{"id": "h069_r1", "subject": "whiskers", "type": "emerge_from", "object": "transformed_muzzle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h069_r2", "subject": "ears", "type": "join", "object": "transformed_head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h069_r3", "subject": "fur", "type": "continuous_with", "object": "transformed_face_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Headband cat ears, painted whiskers or an external mask remain costume/decoration; they don't prove bodily transformation.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S37](https://www.harrypotter.com/features/when-magic-in-harry-potter-goes-really-wrong)
- 기존 profile: ca_pointed_ear_panels; 기존 후보: ca_cap_projections
- 제안 처리: NEW_WITH_MEDIUM_GUARD — Grey film fur and black book cat descriptions remain version leads; no magical mechanism inferred from still pixels.
- 참조 행: ref_032
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H070 옆으로 길게 뻗은 뾰족귀

같은 머리 양쪽의 귀가 옆으로 길게 뻗어 끝이 좁아지고 각 귀 안에 안쪽 면이 있다.

two ear structures extend laterally from the same head; each ear narrows toward an outer tip; inner panels remain enclosed by their own ear contours.

- 관찰 요소: two ear structures extend laterally from the same head / each ear narrows toward an outer tip / inner panels remain enclosed by their own ear contours
- 소유·관계: [{"id": "h070_r1", "subject": "two_ear_bases", "type": "connected_to", "object": "same_nonhuman_head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h070_r2", "subject": "inner_panels", "type": "inside", "object": "their_own_ear_contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Cap points, horns, separate mask ears or unrelated actors' ears don't complete nonhuman ear ownership.
- 출처 상태: TEXT_SUPPORTED; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/)
- 기존 profile: ca_elongated_side_ears, ca_pointed_ear_panels; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Dobby and goblins differ in eye/nose/jaw proportions; don't collapse them into one generic small 'elf' preset.
- 참조 행: ref_029, ref_088, ref_089
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H071 인간 상체와 말 하체의 연속 접합

인간 머리·상체가 한 접합점에서 말 몸통으로 이어지고 아래에는 네 말 다리와 꼬리가 있다.

a human head and torso remain above one junction; an equine torso continues from that same junction; four horse legs and an equine tail belong to the lower body.

- 관찰 요소: a human head and torso remain above one junction / an equine torso continues from that same junction / four horse legs and an equine tail belong to the lower body
- 소유·관계: [{"id": "h071_r1", "subject": "human_torso", "type": "joined_at", "object": "equine_torso_junction", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h071_r2", "subject": "four_horse_legs", "type": "part_of", "object": "equine_lower_body", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h071_r3", "subject": "equine_tail", "type": "connected_to", "object": "same_hindquarters", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A rider on a horse, two overlapping bodies or a statue with intentionally truncated limbs isn't necessarily this complete form.
- 출처 상태: TEXT_SUPPORTED_WITH_CITATION_LIMIT; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers)
- 기존 profile: ri_centaur_rimmer_form, ri_centaur_nessos_human_knees; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Do not broaden sculpture-specific truncation/kneeling profiles; exact source-book citation needs correction.
- 참조 행: ref_025
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H072 맹금류 앞부분·날개와 말 뒤부분

같은 몸에 조류 머리·발톱 앞다리·날개 두 개가 붙고 말의 뒤몸통·뒷다리·꼬리로 이어진다.

an avian head and taloned forequarters belong to one torso; paired feathered wings join that torso; equine hindquarters legs and tail continue from the same body.

- 관찰 요소: an avian head and taloned forequarters belong to one torso / paired feathered wings join that torso / equine hindquarters legs and tail continue from the same body
- 소유·관계: [{"id": "h072_r1", "subject": "avian_forequarters", "type": "joined_to", "object": "same_hybrid_torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h072_r2", "subject": "paired_wings", "type": "connected_to", "object": "torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h072_r3", "subject": "equine_hindquarters", "type": "continuous_with", "object": "same_hybrid_torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Lion rear is griffin, all-horse legs with wings is Pegasus, rider/horse overlap isn't a hybrid junction.
- 출처 상태: TEXT_SUPPORTED; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/), [S46](https://www.harrypotter.com/features/every-time-draco-malfoy-was-just-too-draco)
- 기존 profile: hippogriff_eagle_horse_topology; 기존 후보: 없음
- 제안 처리: REUSE_WITH_EFFECT_MAPPING — Existing profile lacks explicit affected-property mapping; adoption needs reviewed owner/effect mapping instead of a cloned keyword profile.
- 참조 행: ref_044
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H073 비늘 몸통·턱·송곳니의 거대 뱀

비늘 몸통이 같은 뱀 머리와 이어지고 턱의 송곳니·주변 크기 기준을 구분한다.

one long scaled torso remains continuous with a snake head; fangs emerge from the declared jaw; a shared-plane scale reference establishes the chosen giant size.

- 관찰 요소: one long scaled torso remains continuous with a snake head / fangs emerge from the declared jaw / a shared-plane scale reference establishes the chosen giant size
- 소유·관계: [{"id": "h073_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one long scaled torso remains continuous with a snake head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h073_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "fangs emerge from the declared jaw", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h073_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a shared-plane scale reference establishes the chosen giant size", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Dragon limbs, teeth on a mask, isolated fang or forced perspective alone isn't a giant serpent.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S09](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: SOURCE_AND_OWNER_REVIEW — Basilisk exact eye/scale/fang dimensions require source still; petrifying gaze is not an eye colour.
- 참조 행: ref_033
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H074 몸통에 이어진 거미의 여덟 다리

한 거미 몸통에 연결된 여덟 관절 다리와 같은 몸 표면의 털·눈 무리를 구분한다.

one arachnid body has eight connected articulated legs; the legs extend from the same body regions; hair and eye groups remain on that creature surface.

- 관찰 요소: one arachnid body has eight connected articulated legs / the legs extend from the same body regions / hair and eye groups remain on that creature surface
- 소유·관계: [{"id": "h074_r1", "subject": "eight_legs", "type": "connected_to", "object": "same_arachnid_body", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h074_r2", "subject": "hair", "type": "on", "object": "same_creature_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Eight visible tips without complete attachment may include duplicates; puppet operating rods aren't anatomical legs.
- 출처 상태: TEXT_SUPPORTED; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_EXISTING_MORPHOLOGY_REVIEW — Animatronic leg-span numbers are production-object measurements, not a universal fictional scale.
- 참조 행: ref_034
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H075 부분·전체 얼굴 가면의 판본별 범위

별도 가면이 얼굴의 선택된 범위를 덮고 테두리·선택한 눈 구멍이 같은 가면에 속한다.

one separate mask covers a selected face region; its perimeter is traceable against the head; selected eye apertures are bounded holes in that same mask.

- 관찰 요소: one separate mask covers a selected face region / its perimeter is traceable against the head / selected eye apertures are bounded holes in that same mask
- 소유·관계: [{"id": "h075_r1", "subject": "mask", "type": "separate_from", "object": "face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h075_r2", "subject": "apertures", "type": "through", "object": "same_mask", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h075_r3", "subject": "mask_perimeter", "type": "bounds", "object": "selected_face_coverage", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: An actual altered face, lower-face scarf or hood shadow isn't a separate mask; partial and whole coverage are alternatives.
- 출처 상태: TEXT_SUPPORTED; [S07](https://www.harrypotter.com/features/death-eater-masks-and-costumes)
- 기존 profile: ca_projecting_face_mask; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — Fourth-film partial vs fifth-film full coverage; mouth apertures belong only to explicitly chosen variants. Do not force generic projecting mask nose or full coverage.
- 참조 행: ref_057, ref_101
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H076 금속 같은 가면의 새김·구멍 구별

반사되는 가면 표면 위의 새김선과 실제 눈 구멍을 구별한다.

incised ornament remains on one mask surface; solid reflective ground persists between motif lines; actual eye apertures remain distinct from engraved grooves.

- 관찰 요소: incised ornament remains on one mask surface / solid reflective ground persists between motif lines / actual eye apertures remain distinct from engraved grooves
- 소유·관계: [{"id": "h076_r1", "subject": "incisions", "type": "on", "object": "mask_solid_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h076_r2", "subject": "eye_apertures", "type": "through", "object": "mask", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h076_r3", "subject": "solid_ground", "type": "between", "object": "incised_motif_lines", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Black painted motifs aren't necessarily holes; reflective mask isn't necessarily solid silver; matching clothing motif doesn't merge owners.
- 출처 상태: TEXT_SUPPORTED; [S07](https://www.harrypotter.com/features/death-eater-masks-and-costumes)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Retain per-mask individual pattern and costume embroidery as related separate carriers.
- 참조 행: ref_057, ref_101
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H077 중앙 모래시계·둘레 고리·목걸이

작은 모래시계가 장식 중앙에 있고 별도 고리가 이를 둘러싸며 같은 장식에 목걸이 줄이 연결된다.

a small hourglass remains at the centre of a pendant; separate ring structures encircle that hourglass; a chain attaches to the same pendant above the chest.

- 관찰 요소: a small hourglass remains at the centre of a pendant / separate ring structures encircle that hourglass / a chain attaches to the same pendant above the chest
- 소유·관계: [{"id": "h077_r1", "subject": "hourglass", "type": "inside", "object": "pendant_centre", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h077_r2", "subject": "rings", "type": "encircle", "object": "hourglass", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h077_r3", "subject": "chain", "type": "attached_to", "object": "same_pendant", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Clock dial, ordinary ring necklace or background hourglass doesn't satisfy the central pendant structure.
- 출처 상태: TEXT_AND_REPLICA_SCOPE; [S13](https://www.harrypotter.com/fact-file/objects/time-turner), [S14](https://noblecollection.com/Item--i-PRP-HP-7017)
- 기존 profile: clothing_ct109_v2; 기존 후보: 없음
- 제안 처리: NEW_PROP_MODIFIER — Do not force replica ring count, gold purity or contradictory size; motion/time function stays outside still gates.
- 참조 행: ref_040
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H078 코르크 조각을 꿴 목걸이

서로 다른 코르크 마개 윤곽을 하나의 끈이 지지하고 그 끈이 목걸이 고리를 만든다.

several cork-like plugs have distinct contours; one cord passes through or holds those same pieces; the cord forms a wearable neck loop.

- 관찰 요소: several cork-like plugs have distinct contours / one cord passes through or holds those same pieces / the cord forms a wearable neck loop
- 소유·관계: [{"id": "h078_r1", "subject": "cord", "type": "holds", "object": "several_cork_plugs", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h078_r2", "subject": "cord", "type": "forms", "object": "neck_loop", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Bottle caps, beads of unknown material or corks on a table don't establish a worn cork necklace.
- 출처 상태: TEXT_SUPPORTED; [S16](https://www.harrypotter.com/features/luna-lovegoods-eight-wackiest-moments)
- 기존 profile: clothing_ct109_v2; 기존 후보: 없음
- 제안 처리: NEW_RELATION — Official editorial sometimes loosely calls them caps; preserve plug vs cap boundary from the selected source/image.
- 참조 행: ref_062
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H079 잎 달린 작은 뿌리열매 드롭 귀걸이

귀의 부착점 아래에 작은 뿌리열매 모양이 매달리고 그 위의 잎 장식이 같은 귀걸이에 속한다.

a small root-fruit-shaped ornament hangs below an ear attachment; a distinct leaf-like top belongs to that ornament; the pendant connects through a distinct jewellery attachment.

- 관찰 요소: a small root-fruit-shaped ornament hangs below an ear attachment / a distinct leaf-like top belongs to that ornament / the pendant connects through a distinct jewellery attachment
- 소유·관계: [{"id": "h079_r1", "subject": "root_fruit_pendant", "type": "hangs_from", "object": "ear_attachment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h079_r2", "subject": "leaf_like_top", "type": "part_of", "object": "same_ornament", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Actual radish held in hand, tattoo or pendant necklace isn't ear-mounted; fictional plant identity is provenance.
- 출처 상태: TEXT_SUPPORTED; [S16](https://www.harrypotter.com/features/luna-lovegoods-eight-wackiest-moments), [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_MODIFIER — Exact orange/red shape and leaf number need enlarged source pixels before canon-detail qualification.
- 참조 행: ref_062
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H080 별 형태가 매달린 귀걸이

완전한 별 모양 장식이 귀 부착점에서 매달리고 머리카락·배경 별과 분리된다.

a star-shaped ornament has a complete pointed contour; it hangs from a declared ear attachment; the ear jewellery remains separate from hair and background stars.

- 관찰 요소: a star-shaped ornament has a complete pointed contour / it hangs from a declared ear attachment / the ear jewellery remains separate from hair and background stars
- 소유·관계: [{"id": "h080_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a star-shaped ornament has a complete pointed contour", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h080_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "it hangs from a declared ear attachment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h080_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the ear jewellery remains separate from hair and background stars", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Sparkle glints alone don't prove a star outline; earrings hidden behind hair are unobservable.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S43](https://contentful.harrypotter.com/usf1vwtuqyxm/4i0wa5BOBWYACKeQyUyaSo/ba0a6c04fa6c7cb2c2cf59eeadd0ba39/LunaLovegood_WB_F6_LunaLovegoodSlugClubChristmasPartyWithSanguiniAndEldredWorple_Still_080615_Port.jpg?fm=jpg&q=75&w=914)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_EXISTING_ORNAMENT_REVIEW — Star earrings belong to the party variant; don't require them in all Luna-related looks.
- 참조 행: ref_074
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H081 넓은 장식 안경과 다른 렌즈색

장식적인 넓은 안경테 안에 색이 구분되는 두 렌즈가 있고 코 다리로 연결된다.

a broad decorated frame surrounds two lenses; the lenses retain distinct selected colour regions; a bridge connects them over the nose.

- 관찰 요소: a broad decorated frame surrounds two lenses / the lenses retain distinct selected colour regions / a bridge connects them over the nose
- 소유·관계: [{"id": "h081_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a broad decorated frame surrounds two lenses", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h081_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the lenses retain distinct selected colour regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h081_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a bridge connects them over the nose", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A full face mask, skin-painted motif or global colour grade isn't a pair of decorated coloured lenses.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S16](https://www.harrypotter.com/features/luna-lovegoods-eight-wackiest-moments)
- 기존 profile: ca_spectacle_frame, y2kr_colored_frame; 기존 후보: 없음
- 제안 처리: MODIFIER_REVIEW — Paper vs plastic vs product material and exact lens pattern need versioned object evidence; invisible-creature vision is not visual form.
- 참조 행: ref_075
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H082 머리 위의 큰 사자 모형 모자

인간 머리 위의 별도 사자 얼굴 모형 둘레에 갈기가 있고 착용자의 머리와 지지 경계가 구별된다.

a separate lion-face object rests above a human head; a mane surrounds that object's face; the wearer head remains underneath with a distinct support boundary.

- 관찰 요소: a separate lion-face object rests above a human head / a mane surrounds that object's face / the wearer head remains underneath with a distinct support boundary
- 소유·관계: [{"id": "h082_r1", "subject": "lion_head_object", "type": "rests_above", "object": "human_head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h082_r2", "subject": "mane", "type": "surrounds", "object": "object_face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h082_r3", "subject": "wearer_head", "type": "distinct_from", "object": "hat_object", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Biological lion head, animal-face mask covering the wearer or a lion beside the person isn't a top-mounted hat.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S16](https://www.harrypotter.com/features/luna-lovegoods-eight-wackiest-moments)
- 기존 profile: ca_animal_head_mask; 기존 후보: 없음
- 제안 처리: NEW_CARRIER_SIBLING — Head-covering mask and above-head sculpture differ; roar needs temporal/audio evidence.
- 참조 행: ref_076
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H083 작은 비즈 주머니의 입구·손잡이

작은 주머니의 입구와 표면 구슬을 구분하고 손잡이·조임끈이 같은 가방에 이어진다.

a small flexible pouch has a bounded mouth; bead-like elements occupy that pouch surface; a handle or drawcord attaches to the same pouch edge.

- 관찰 요소: a small flexible pouch has a bounded mouth / bead-like elements occupy that pouch surface / a handle or drawcord attaches to the same pouch edge
- 소유·관계: [{"id": "h083_r1", "subject": "beads", "type": "on", "object": "pouch_surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h083_r2", "subject": "handle_or_drawcord", "type": "attached_to", "object": "same_pouch", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h083_r3", "subject": "pouch_mouth", "type": "bounds", "object": "pouch_opening", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A necklace, beaded clothing panel or unbounded decorative cluster isn't a pouch; unlimited capacity is not visible.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S38](https://www.harrypotter.com/features/10-of-the-most-useful-objects-from-the-wizarding-world)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: PROP_OWNER_REVIEW — Hand contact and garment attachment are optional separate relations. Exact clasp/cord form still needs image evidence.
- 참조 행: ref_085
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H084 안경테의 보석 장식과 렌즈

보석 같은 작은 장식이 안경테에 붙고 렌즈·코 다리는 별도 구조로 남는다.

small stone-like ornaments attach to a spectacle frame; the frame retains separate eye lenses and a bridge; the ornament attachments stay within the spectacle frame boundary.

- 관찰 요소: small stone-like ornaments attach to a spectacle frame / the frame retains separate eye lenses and a bridge / the ornament attachments stay within the spectacle frame boundary
- 소유·관계: [{"id": "h084_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "small stone-like ornaments attach to a spectacle frame", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h084_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the frame retains separate eye lenses and a bridge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h084_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the ornament attachments stay within the spectacle frame boundary", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Eye makeup crystals, ordinary glare or earrings aren't frame-mounted stones.
- 출처 상태: SEED_LEAD; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers)
- 기존 profile: ca_spectacle_frame; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Rita book vs film frame/colour/nail/fabric variants require exact sources; generic frame adornment can be drafted.
- 참조 행: ref_053, ref_054
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H085 성인 무대판의 긴 뒤묶음

머리카락이 뒤의 한 묶임점에서 긴 꼬리로 이어지고 수염·칼라는 독립 선택이다.

scalp hair gathers toward one rear fastening point; a long single tail continues from that point; a separate facial-hair or collar state remains optional.

- 관찰 요소: scalp hair gathers toward one rear fastening point / a long single tail continues from that point / a separate facial-hair or collar state remains optional
- 소유·관계: [{"id": "h085_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "scalp hair gathers toward one rear fastening point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h085_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a long single tail continues from that point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h085_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate facial-hair or collar state remains optional", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Loose long hair, twin tails or a female reinterpretation aren't a confirmed single ponytail.
- 출처 상태: TEXT_SUPPORTED; [S20](https://www.harrypotter.com/news/cursed-child-first-look-at-malfoys-in-character), [S21](https://www.harrypotter.com/features/five-differences-between-the-younger-draco-malfoy-and-the-draco-we-see-in-cursed-child)
- 기존 profile: bilateral_twin_tail_gather; 기존 후보: 없음
- 제안 처리: SIBLING_REVIEW — 2016 promo loose/position details and later stage ponytail can be different case observations; don't flatten cast/production history.
- 참조 행: ref_108
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H086 손·지팡이·지팡이 손잡이의 접촉

한 손이 잡은 손잡이에서 별도의 가는 막대가 끝까지 이어지고 손가락과 물체 경계가 유지된다.

one hand visibly encloses a bounded handle; the same handle continues into one separate narrow shaft; the shaft remains outside the hand and continuous to its tip.

- 관찰 요소: one hand visibly encloses a bounded handle / the same handle continues into one separate narrow shaft / the shaft remains outside the hand and continuous to its tip
- 소유·관계: [{"id": "h086_r1", "subject": "same_hand_fingers", "type": "in_contact_with", "object": "prop_handle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h086_r2", "subject": "handle", "type": "continuous_with", "object": "shaft", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h086_r3", "subject": "shaft", "type": "continuous_to", "object": "prop_tip", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Floating wand, merged finger-shaft, another person's grip or production rubber material isn't this handle relation.
- 출처 상태: TEXT_SUPPORTED; [S35](https://www.harrypotter.com/features/designing-harry-potter-wands)
- 기존 profile: costume_ccx_cc36_01, costume_ccx_cc36_02; 기존 후보: 없음
- 제안 처리: REUSE_WITH_PROP_OWNER — Wand-in-cane extraction, hidden blades and magical effect need separate selected relations/evidence.
- 참조 행: ref_028, ref_055, ref_058
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H087 귓불에 연결된 고리 귀걸이

완전한 고리 윤곽이 지정한 귀에 이어지고 목걸이·머리 고리와 분리된다.

one closed ring retains its full curved contour; an attachment joins it to the declared ear; the ring remains separate from neck chains and hair loops.

- 관찰 요소: one closed ring retains its full curved contour / an attachment joins it to the declared ear / the ring remains separate from neck chains and hair loops
- 소유·관계: [{"id": "h087_r1", "subject": "ring", "type": "connected_to", "object": "declared_ear", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h087_r2", "subject": "closed_ring_contour", "type": "separate_from", "object": "hair_loops", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A black crescent shadow, hair curl or unconnected background ring isn't a hoop earring.
- 출처 상태: SAMPLE_PIXELS; [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: REUSE_OR_NEW_ORNAMENT — This source shows dark hoops; material, exact cardinality and all-fanart universality are not implied.
- 참조 행: ref_118
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H088 서로 다른 목걸이·팔찌·반지의 겹침

여러 줄·고리 장식의 윤곽을 구분하고 각각 목·손목·손가락의 지정 부위에 연결한다.

several distinct chains or bracelets keep separate contours; each attaches to its declared neck wrist or finger carrier; each overlapping ornament retains a separately traceable carrier attachment.

- 관찰 요소: several distinct chains or bracelets keep separate contours / each attaches to its declared neck wrist or finger carrier / each overlapping ornament retains a separately traceable carrier attachment
- 소유·관계: [{"id": "h088_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "several distinct chains or bracelets keep separate contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h088_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each attaches to its declared neck wrist or finger carrier", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h088_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each overlapping ornament retains a separately traceable carrier attachment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Background beads, fused fingers or one embossed print isn't multiple independently worn jewellery.
- 출처 상태: PARTIAL_TEXT_AND_PIXELS; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers), [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: OWNER_SPECIFIC_REVIEW — Trelawney bangles, Maxime opal and fan dark nails are different axes; nail colour is not jewellery.
- 참조 행: ref_039, ref_047, ref_118
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H089 느슨한 천 코트와 정장 내부층

천 코트 몸판에 여유가 있고 안의 셔츠·조끼와 겉옷의 옷자락·깃이 분리된다.

a fabric overcoat leaves visible ease around the torso; shirt or vest layers remain separate inside; the outer hem and lapel shape follow the selected coat version.

- 관찰 요소: a fabric overcoat leaves visible ease around the torso / shirt or vest layers remain separate inside / the outer hem and lapel shape follow the selected coat version
- 소유·관계: [{"id": "h089_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a fabric overcoat leaves visible ease around the torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h089_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "shirt or vest layers remain separate inside", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h089_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the outer hem and lapel shape follow the selected coat version", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Loose coat isn't uniform wizard robe or proof of occupation; soft rosy colour doesn't establish personality.
- 출처 상태: TEXT_SUPPORTED; [S17](https://www.harrypotter.com/news/exclusive-eddie-redmayne-interview-on-newt-scamanders-coat), [S19](https://www.harrypotter.com/news/fantastic-beasts-dressing-tina-and-queenie-goldstein)
- 기존 profile: costume_ccx_cc02_02; 기존 후보: 없음
- 제안 처리: REUSE_OR_MODIFIER — Queenie exact peach/pink ombre coat and Tina huge collar are seed leads; Newt petrol hue is separately sourced.
- 참조 행: ref_102, ref_103, ref_104
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H090 각진 어깨의 긴 코트·검백 테두리

긴 코트의 어깨 외곽과 솔기·라펠을 따라가는 대비 테두리를 구분한다.

a long coat has emphasized shoulder contours; contrasting edging follows its selected seam or lapel boundaries; the soft cloth remains separate from boots and skin.

- 관찰 요소: a long coat has emphasized shoulder contours / contrasting edging follows its selected seam or lapel boundaries / the soft cloth remains separate from boots and skin
- 소유·관계: [{"id": "h090_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a long coat has emphasized shoulder contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h090_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "contrasting edging follows its selected seam or lapel boundaries", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h090_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the soft cloth remains separate from boots and skin", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Physical wetness, plastic armour or overall black-and-white image grade isn't cashmere/Lurex coat appearance.
- 출처 상태: TEXT_SUPPORTED; [S18](https://www.harrypotter.com/news/the-touch-of-glamour-in-colin-farrell-fantastic-beasts-costume)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: NEW_OR_ATOM_BUNDLE — Exact case material is creator-supported; generic sheen cannot establish fiber chemistry.
- 참조 행: ref_105
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H091 TS·팬작품 제목·캐릭터명

팬 해석·작품명을 문맥으로 기록하고 보이는 머리·옷·몸·표정은 따로 선택한다.

a named fan interpretation establishes a declared creative version; visible traits are independently chosen within that version; names do not identify sex-change events or body geometry.

- 관찰 요소: a named fan interpretation establishes a declared creative version / visible traits are independently chosen within that version / names do not identify sex-change events or body geometry
- 소유·관계: [{"id": "h091_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a named fan interpretation establishes a declared creative version", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h091_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "visible traits are independently chosen within that version", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h091_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "names do not identify sex-change events or body geometry", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: TS label, Karina, adult stage long hair and an outfit swap are not one canonical visual preset.
- 출처 상태: CONTEXT_ONLY; [S22](https://novelpia.com/novel/3291), [S23](https://knowyourmeme.com/memes/malfoid-female-draco-malfoy), [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — No title/name in positive retrieval; gender/age/transition history aren't inferred from visible clothing. No Novelpia-to-X lineage evidence.
- 참조 행: ref_110, ref_111, ref_112, ref_113
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H092 변장·착의 변환과 신체 변형 구분

한 장면의 얼굴·옷은 현재 모습만 증명하며 변장·보가트·몸 변형은 별도 문맥과 연속성으로 기록한다.

an observed face and costume establish only the shown appearance; a declared story context can identify disguise or imitation; body change requires its own continuity or explicit request.

- 관찰 요소: an observed face and costume establish only the shown appearance / a declared story context can identify disguise or imitation / body change requires its own continuity or explicit request
- 소유·관계: [{"id": "h092_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "an observed face and costume establish only the shown appearance", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h092_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a declared story context can identify disguise or imitation", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h092_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "body change requires its own continuity or explicit request", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Boggart imitation is not real Snape's body changing sex; Polyjuice identity isn't proved from a copied face alone.
- 출처 상태: CONTEXT_ONLY; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers), [S32](https://www.harrypotter.com/features/unsung-heroes-augusta-longbottom), [S37](https://www.harrypotter.com/features/when-magic-in-harry-potter-goes-really-wrong)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Keep showing a costume, altered anatomy, a disguise target and actual person identity as separate evidence layers.
- 참조 행: ref_041, ref_086, ref_087
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H093 내려온 눈꺼풀과 비대칭 입꼬리

같은 얼굴에서 윗눈꺼풀이 홍채 일부를 덮고 한쪽 입꼬리가 더 올라간다.

upper eyelids partly overlap the irises; one mouth corner rises more than the other; both actions belong to one declared face at the same moment.

- 관찰 요소: upper eyelids partly overlap the irises / one mouth corner rises more than the other / both actions belong to one declared face at the same moment
- 소유·관계: [{"id": "h093_r1", "subject": "upper_lids", "type": "overlap", "object": "their_irises", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h093_r2", "subject": "one_mouth_corner", "type": "higher_than", "object": "other_corner", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h093_r3", "subject": "eye_and_mouth_actions", "type": "co_owned_by", "object": "same_face", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Neutral face, head tilt or separate characters' expressions don't complete this conjunction; no arrogance or desire is proved.
- 출처 상태: SAMPLE_PIXELS; [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257)
- 기존 profile: sca_f03; 기존 후보: playful_smirk
- 제안 처리: NEW_OR_CONJUNCTION — Existing playful-smirk candidates add interpretation; maintain a neutral facial-action description and optional contextual reading.
- 참조 행: ref_116, ref_128, ref_129
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H094 팔짱·턱 높이·머리 기울기의 독립 축

같은 몸 앞의 두 팔 교차를 확인하고 손의 소유와 머리 기울기·턱 높이는 별도로 고른다.

two forearms cross in front of the same torso; hands or sleeve ends retain their own connected owners; the head tilt and chin height are separately selected.

- 관찰 요소: two forearms cross in front of the same torso / hands or sleeve ends retain their own connected owners / the head tilt and chin height are separately selected
- 소유·관계: [{"id": "h094_r1", "subject": "two_forearms", "type": "cross_in_front_of", "object": "same_torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h094_r2", "subject": "each_hand", "type": "continuous_with", "object": "its_own_forearm", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: One hand holding the opposite elbow isn't necessarily arms crossed; pose doesn't establish noble rank or rivalry.
- 출처 상태: SAMPLE_PIXELS; [S25](https://x.com/masoq095/status/2105042738517295257), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: POSE_OWNER_REVIEW — Artist sample includes different poses; don't encode all three as compulsory expression of TS or villainess.
- 참조 행: ref_117, ref_126, ref_127
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H095 두 인물의 마주보기·시선·소품 소유

두 인물의 몸·손·시선 목표와 책·지팡이의 소유를 분리한다.

two distinct figures keep separate body and hand ownership; each selected gaze has a declared target; a wand or book remains attached to the correct holder.

- 관찰 요소: two distinct figures keep separate body and hand ownership / each selected gaze has a declared target / a wand or book remains attached to the correct holder
- 소유·관계: [{"id": "h095_r1", "subject": "each_prop", "type": "held_by", "object": "declared_holder", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h095_r2", "subject": "each_gaze", "type": "directed_at", "object": "declared_target", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h095_r3", "subject": "participant_a", "type": "separate_from", "object": "participant_b", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: One frontal figure or gaze toward the camera isn't interpersonal competition; disagreement/romance isn't inferred from pose.
- 출처 상태: DESIGN_PROPOSAL; [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_AND_OWNER_REVIEW — Competition is an authored situation; static visual cues support a chosen reading but do not prove actual emotion/history.
- 참조 행: ref_127
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H096 직조 문양의 브로케이드 표면

천 바탕과 다른 문양 실의 높이·광택을 구분하고 별도 덧댄 천과 분리한다.

a pattern yarn lies above or through a distinct cloth ground; the motif retains bounded repeated contours; the weave-related relief remains separate from sewn-on fabric pieces.

- 관찰 요소: a pattern yarn lies above or through a distinct cloth ground / the motif retains bounded repeated contours / the weave-related relief remains separate from sewn-on fabric pieces
- 소유·관계: [{"id": "h096_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a pattern yarn lies above or through a distinct cloth ground", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h096_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the motif retains bounded repeated contours", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h096_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the weave-related relief remains separate from sewn-on fabric pieces", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Print, embroidery, applique and jacquard as a general process aren't automatically brocade.
- 출처 상태: GENERIC_TECHNICAL; [S27](https://www.vam.ac.uk/articles/a-z-opus-anglicanum), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: 없음; 기존 후보: brocade_raised_supplementary_weft_surface
- 제안 처리: REUSE_CANDIDATE — Exact fiber/process needs material documentation; candidate shape doesn't prove production history.
- 참조 행: ref_018, ref_107, ref_138
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H097 빛 방향에 따라 달라지는 벨벳 기모

짧은 기모가 천 면을 덮고 주름 방향에 따라 광택이 달라져 매끈한 가죽과 구별된다.

a dense short nap covers a bounded cloth panel; adjacent folds show direction-dependent sheen changes; the soft surface remains distinguishable from smooth leather glare.

- 관찰 요소: a dense short nap covers a bounded cloth panel / adjacent folds show direction-dependent sheen changes / the soft surface remains distinguishable from smooth leather glare
- 소유·관계: [{"id": "h097_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a dense short nap covers a bounded cloth panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h097_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "adjacent folds show direction-dependent sheen changes", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h097_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the soft surface remains distinguishable from smooth leather glare", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Uniform plastic gloss, background darkness or long animal fur isn't velvet nap.
- 출처 상태: TEXT_AND_GENERIC; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct089_v2; 기존 후보: velvet_fabric_surface
- 제안 처리: REUSE_WITH_EFFECT_SCOPE — Existing profile uses appearance wardrobe.surface scope; align final effects with actual owner instead of changing scope by label.
- 참조 행: ref_066, ref_107, ref_125, ref_139
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H098 시폰형 얇은 흐름과 가장자리

얇은 천의 끝과 작은 흐르는 주름·겹침 면을 구분한다.

a thin cloth panel has a complete edge; small fluid folds continue across that panel; the thin panel edges remain traceable across overlapping folds.

- 관찰 요소: a thin cloth panel has a complete edge / small fluid folds continue across that panel / the thin panel edges remain traceable across overlapping folds
- 소유·관계: [{"id": "h098_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a thin cloth panel has a complete edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h098_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "small fluid folds continue across that panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h098_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the thin panel edges remain traceable across overlapping folds", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Tulle cell network, rigid organza or mist isn't automatically chiffon; a photo alone doesn't prove silk.
- 출처 상태: TEXT_AND_GENERIC; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct091_v2; 기존 후보: sheer_organza_chiffon_transmission
- 제안 처리: REUSE_OR_MATERIAL_SIBLING — Documented Hermione silk/chiffon remains source-specific; generic candidate should not impose chemistry.
- 참조 행: ref_140
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H099 튈의 실제 망사 셀과 겹침

가는 실이 실제 열린 셀을 이루고 각 망사 층의 끝과 겹침을 구별한다.

fine threads enclose repeated open cells; a complete mesh layer has its own outer edge; overlapping layers each retain a separately traceable mesh network.

- 관찰 요소: fine threads enclose repeated open cells / a complete mesh layer has its own outer edge / overlapping layers each retain a separately traceable mesh network
- 소유·관계: [{"id": "h099_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "fine threads enclose repeated open cells", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h099_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a complete mesh layer has its own outer edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h099_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "overlapping layers each retain a separately traceable mesh network", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Painted dots, opaque lace print or fog isn't tulle mesh; rigid support and short tutu aren't universal.
- 출처 상태: TEXT_AND_GENERIC; [S05](https://www.harrypotter.com/features/hogwarts-haute-couture-greatest-fashion-moments-from-the-films), [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct090_v2, costume_ccx_cc27_01; 기존 후보: 없음
- 제안 처리: REUSE_WITH_SUBTYPE_GUARDS — Existing tutu layers start below waist; don't force that carrier/short spread on a wedding gown.
- 참조 행: ref_079, ref_141
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H100 주름의 능선·골·접히는 방향

같은 천의 능선·골이 패널을 따라 반복되고 방향·폭을 선택한다.

fabric repeatedly folds into ridges and valleys; the folds run continuously along the selected panel; their direction and width remain explicitly chosen.

- 관찰 요소: fabric repeatedly folds into ridges and valleys / the folds run continuously along the selected panel / their direction and width remain explicitly chosen
- 소유·관계: [{"id": "h100_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "fabric repeatedly folds into ridges and valleys", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h100_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the folds run continuously along the selected panel", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h100_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "their direction and width remain explicitly chosen", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Printed stripes, fine weave ribs or random wrinkles aren't set pleat topology; knife and inverted box folds remain siblings.
- 출처 상태: GENERIC_TECHNICAL; [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct063_v1, clothing_ct063_v2; 기존 후보: pleat_fold_ridge_valley_geometry
- 제안 처리: REUSE_SELECTED_SUBTYPE — Generic label pleating doesn't automatically activate knife pleats; specific form requires request evidence.
- 참조 행: ref_046, ref_077, ref_142
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H101 한쪽은 붙고 다른 끝은 자유로운 러플

주름 잡은 띠의 한쪽은 지정한 옷 끝에 붙고 반대쪽은 물결치는 자유 끝으로 남는다.

one edge of a gathered strip attaches to a garment; the opposite edge remains free and wave-shaped; the attachment stays on the selected sleeve neckline or skirt carrier.

- 관찰 요소: one edge of a gathered strip attaches to a garment / the opposite edge remains free and wave-shaped / the attachment stays on the selected sleeve neckline or skirt carrier
- 소유·관계: [{"id": "h101_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one edge of a gathered strip attaches to a garment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h101_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the opposite edge remains free and wave-shaped", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h101_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the attachment stays on the selected sleeve neckline or skirt carrier", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Smooth circular flounce, tier join, random crumple or lace texture alone isn't gathered ruffle.
- 출처 상태: GENERIC_TECHNICAL; [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct065_v1, clothing_ct065_v2; 기존 후보: 없음
- 제안 처리: REUSE_OR_CARRIER_SIBLING — Current sleeve ruffle and skirt flounce are distinct; owner changes require sibling/context review.
- 참조 행: ref_081, ref_082, ref_144
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H102 바탕 천 위에 덧붙인 별도 문양 천

별도 모양 천의 테두리가 바탕 천 위에 보이고 봉제를 선택한 경우 연결 실을 확인한다.

a shaped fabric piece lies over a distinct ground cloth; its complete border remains readable against that ground; a declared sewn attachment joins the two when stitching is specified.

- 관찰 요소: a shaped fabric piece lies over a distinct ground cloth / its complete border remains readable against that ground / a declared sewn attachment joins the two when stitching is specified
- 소유·관계: [{"id": "h102_r1", "subject": "shaped_fabric_piece", "type": "over", "object": "ground_cloth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h102_r2", "subject": "specified_stitching", "type": "joins", "object": "piece_to_ground_if_requested", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Print, weave or stitched outline without a separate fabric piece isn't applique; a movie motif doesn't prove construction.
- 출처 상태: GENERIC_TECHNICAL; [S27](https://www.vam.ac.uk/articles/a-z-opus-anglicanum)
- 기존 profile: clothing_ct067_v1, costume_ccx_cc42_02; 기존 후보: 없음
- 제안 처리: REUSE_WITH_CARRIER_SCOPE — Don't cite generic applique definition as proof that Fleur's actual black motifs used applique.
- 참조 행: ref_079, ref_145
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H103 두 줄의 구멍을 가로지르는 끈 여밈

같은 옷의 양쪽 구멍 줄 사이로 끈이 교차하며 각 구멍을 통과한다.

paired garment edges contain two eyelet rows; one cord repeatedly crosses between those rows; the cord enters the declared eyelets on the same garment.

- 관찰 요소: paired garment edges contain two eyelet rows / one cord repeatedly crosses between those rows / the cord enters the declared eyelets on the same garment
- 소유·관계: [{"id": "h103_r1", "subject": "cord", "type": "crosses_between", "object": "paired_eyelet_rows", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h103_r2", "subject": "cord", "type": "passes_through", "object": "declared_eyelets", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h103_r3", "subject": "both_rows", "type": "part_of", "object": "same_garment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A printed cross pattern, studs/loops busk, braid or independent neck ribbon isn't functional lacing topology.
- 출처 상태: GENERIC_TECHNICAL; [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: clothing_ct055_v1, costume_ccx_cc26_02; 기존 후보: 없음
- 제안 처리: REUSE_WITH_LOCATION_GUARDS — Generic lacing vs corset back lacing are separate; don't invent hidden rear lacing from a front still.
- 참조 행: ref_064, ref_146
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H104 마모 원인보다 보이는 옷 상태

지정한 천의 끝 섬유·국소 색바램·얼룩을 각각 보이는 상태로 기록한다.

worn fibers remain attached to a selected edge; local fading remains on that same textile; separate stains occupy bounded cloth regions.

- 관찰 요소: worn fibers remain attached to a selected edge / local fading remains on that same textile / separate stains occupy bounded cloth regions
- 소유·관계: [{"id": "h104_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "worn fibers remain attached to a selected edge", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h104_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "local fading remains on that same textile", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h104_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "separate stains occupy bounded cloth regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Environmental history, distress-making method or social class isn't established by weathered appearance.
- 출처 상태: SOURCE_LEAD; [S41](https://www.wbstudiotour.co.uk/wp-content/uploads/2020/06/at-home-costume-distressing-activity-sheet-1.pdf)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: HOLD_PROCESS_REUSE_FORM — Distinct edge damage, fading and stains should be independently optional; verify source PDF before procedural claims.
- 참조 행: ref_147, ref_148
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H105 지정한 소유자 안에서의 비대칭

같은 소유자의 좌우에서 지정한 속성만 다르게 두고 다른 속성은 독립적으로 유지한다.

a named left-side property differs from its right-side counterpart; both sides belong to the same declared carrier; other property axes remain unchanged unless selected.

- 관찰 요소: a named left-side property differs from its right-side counterpart / both sides belong to the same declared carrier / other property axes remain unchanged unless selected
- 소유·관계: [{"id": "h105_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a named left-side property differs from its right-side counterpart", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h105_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "both sides belong to the same declared carrier", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h105_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "other property axes remain unchanged unless selected", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Hair-region asymmetry, facial action, garment hem and composition balance are different property/owner relations.
- 출처 상태: CONTEXT_ONLY; [S42](https://contentful.harrypotter.com/usf1vwtuqyxm/5zu7yWx27uKEquuAeMSKOe/87198c6433e31cdef347f1bae4b8a63a/NarcissaMalfoy_WB_F6_NarcissaMalfoyFullbody_Promo_080615_Port.jpg?fm=jpg&q=75&w=914), [S24](https://x.com/redteneri/status/2102398387194626330)
- 기존 profile: asymmetric_counterbalance_relation; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Don't use global composition-balance profile for local face/hair asymmetry; choose an exact owner/property first.
- 참조 행: ref_149, ref_070, ref_046, ref_116
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H106 묶임점에 붙는 작은 머리 리본

머리 묶임점에 별도 리본 매듭이 이어지고 리본 끝이 머리와 분리된다.

hair strands gather at a declared tie point; a separate ribbon knot joins that same point; two ribbon tails remain outside the hair bundle.

- 관찰 요소: hair strands gather at a declared tie point / a separate ribbon knot joins that same point / two ribbon tails remain outside the hair bundle
- 소유·관계: [{"id": "h106_r1", "subject": "hair", "type": "gathers_at", "object": "tie_point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h106_r2", "subject": "ribbon_knot", "type": "attached_at", "object": "same_tie_point", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h106_r3", "subject": "ribbon_tails", "type": "separate_from", "object": "hair_bundle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Neck tie, green lining, ear hoop or independent ribbon elsewhere isn't a hair fastening.
- 출처 상태: DESIGN_PROPOSAL; [S24](https://x.com/redteneri/status/2102398387194626330), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: uniform_neck_scarf_separate_hair_ornament; 기존 후보: 없음
- 제안 처리: OPTIONAL_DESIGN_ONLY — Green ribbon/ringlets are a proposed villainess design direction, not a default seen in the three inspected artist samples.
- 참조 행: ref_122, ref_123, ref_118
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H107 성인 후일담의 복식·소품 판본

선택한 성인 재단에 익숙한 색을 남기고 반지·타이핀은 별도 소품으로 둔다.

selected adult tailoring replaces the chosen schoolwear; familiar palette remains on specified garment regions; ring and tie pin are separate bounded accessories when selected.

- 관찰 요소: selected adult tailoring replaces the chosen schoolwear / familiar palette remains on specified garment regions / ring and tie pin are separate bounded accessories when selected
- 소유·관계: [{"id": "h107_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "selected adult tailoring replaces the chosen schoolwear", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h107_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "familiar palette remains on specified garment regions", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h107_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "ring and tie pin are separate bounded accessories when selected", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Book receding hair, film inherited accessories and stage ponytail aren't one combined age-change anatomy.
- 출처 상태: VERSION_CONTEXT; [S04](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/costumes/), [S40](https://www.harrypotter.com/features/first-and-last-appearance-of-our-favourite-harry-potter-characters)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: CONTEXT_ONLY — Adult depiction must come from explicit source/request context; no universal ageing amount or family status from accessories.
- 참조 행: ref_090, ref_091
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H108 손톱 면 안의 어두운 색

지정한 손가락 끝의 손톱 판 안에만 어두운 색을 놓고 손의 연결을 유지한다.

a nail plate occupies the end of a declared finger; dark colour stays inside that nail boundary; the same finger remains connected to its own hand.

- 관찰 요소: a nail plate occupies the end of a declared finger / dark colour stays inside that nail boundary / the same finger remains connected to its own hand
- 소유·관계: [{"id": "h108_r1", "subject": "dark_colour", "type": "inside", "object": "nail_plate_boundary", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h108_r2", "subject": "nail_plate", "type": "on", "object": "same_connected_finger", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Dark fingertips, injury, rings or gloves aren't nail polish; one fanart doesn't establish all-fan costume canon.
- 출처 상태: SAMPLE_PIXELS; [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: OWNER_SLOT_REVIEW — Review current nail carrier/slot before adoption; don't force face-makeup ownership or a sexual/health interpretation.
- 참조 행: ref_118
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H109 머리에 감긴 터번과 어깨 드레이프

같은 머리에 천 띠가 겹쳐 감기고 어깨로 내려오는 끝과의 연결·분리를 확인한다.

overlapping fabric bands wrap around one declared head; a separate free cloth end descends toward the shoulder; the head wrap and hanging cloth retain a readable connection or declared separation.

- 관찰 요소: overlapping fabric bands wrap around one declared head / a separate free cloth end descends toward the shoulder / the head wrap and hanging cloth retain a readable connection or declared separation
- 소유·관계: [{"id": "h109_r1", "subject": "overlapping_bands", "type": "wrap", "object": "declared_head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h109_r2", "subject": "free_end", "type": "descends_toward", "object": "shoulder", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Hair volume, religion, nationality or a loose neck scarf cannot be inferred from a head wrap; fictional purple colour isn't universal.
- 출처 상태: SEED_LEAD; [S01](https://www.harrypotter.com/writing-by-jk-rowling/clothing)
- 기존 profile: ri_dastar_scope; 기존 후보: 없음
- 제안 처리: CULTURAL_SCOPE_AND_SOURCE_HOLD — Quirrell's turban/drape colour and construction need a film still. Don't broaden a Dastar-specific identity to all turbans.
- 참조 행: ref_022
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H110 정돈된 가르마와 정상 코의 학생형

가르마에서 정돈된 머리 방향을 보이고 코의 돌출은 머리와 별도 속성으로 둔다.

a visible part line divides the front hair; the strands follow a tidy direction from that line; ordinary nose projection remains independent from the selected hairstyle.

- 관찰 요소: a visible part line divides the front hair / the strands follow a tidy direction from that line / ordinary nose projection remains independent from the selected hairstyle
- 소유·관계: [{"id": "h110_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a visible part line divides the front hair", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h110_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the strands follow a tidy direction from that line", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h110_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "ordinary nose projection remains independent from the selected hairstyle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Young/older character label doesn't automatically exchange human nose for slit nostrils; hairstyle cannot prove secret identity.
- 출처 상태: SEED_LEAD; [S09](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: GENERIC_FORM_CASE_HOLD — Young Tom Riddle exact hair/year/face source is pending. Use as a version contrast lead, not a character-name activation.
- 참조 행: ref_031
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H111 지퍼 후드와 일상복의 겹침

앞지퍼 후드의 목선·후드 연결을 확인하고 안의 셔츠와 바지는 별도 층으로 둔다.

a zipper runs along the hooded upper garment's front opening; the hood joins its own neckline; a separate inner shirt and trousers retain independent edges when selected.

- 관찰 요소: a zipper runs along the hooded upper garment's front opening / the hood joins its own neckline / a separate inner shirt and trousers retain independent edges when selected
- 소유·관계: [{"id": "h111_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a zipper runs along the hooded upper garment's front opening", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h111_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the hood joins its own neckline", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h111_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate inner shirt and trousers retain independent edges when selected", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: An open robe, a hood worn on another layer or painted zipper doesn't establish this hooded top.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S06](https://fashionista.com/2017/06/jany-temime-harry-potter-costume-designer-interview), [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: clothing_ct007_v1, clothing_ct007_v2; 기존 후보: 없음
- 제안 처리: REUSE_OR_BUNDLE — Third-film casual direction is creator-supported; Hermione's exact pink shade and trouser cut remain scene-level leads.
- 참조 행: ref_035, ref_036
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H112 넓은 소매 구멍·큰 천 몸판·별도 하의

어깨에서 내려오는 큰 천 몸판의 넓은 소매 구멍과 안쪽·아래의 헐렁한 바지를 구분한다.

a very broad outer cloth body descends from the shoulders; large sleeve openings belong to that same garment; a separate loose trouser layer remains inside or below it.

- 관찰 요소: a very broad outer cloth body descends from the shoulders / large sleeve openings belong to that same garment / a separate loose trouser layer remains inside or below it
- 소유·관계: [{"id": "h112_r1", "subject": "broad_sleeve_openings", "type": "part_of", "object": "large_outer_cloth_body", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h112_r2", "subject": "loose_trousers", "type": "inside_or_below", "object": "same_outer_garment", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A generic cape, poncho, skin colour or ornate cap doesn't establish a named African garment or nationality.
- 출처 상태: TEXT_SUPPORTED; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films)
- 기존 profile: west_african_grand_boubou_volume_system; 기존 후보: 없음
- 제안 처리: REUSE_WITH_CULTURAL_PROVENANCE — Kingsley creator interview explicitly cites Agbada and Kota trousers. Keep source names in provenance and preserve actual form boundaries.
- 참조 행: ref_065
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H113 큰 불투명 색석의 목·귀 장신구

별도 받침의 큰 색석과 목·귀 부착점, 돌 안의 색면을 구분한다.

one stone-like element sits inside its own metal-like mount; the mount attaches to a selected neck or ear carrier; surface colour patches remain within that stone.

- 관찰 요소: one stone-like element sits inside its own metal-like mount / the mount attaches to a selected neck or ear carrier / surface colour patches remain within that stone
- 소유·관계: [{"id": "h113_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "one stone-like element sits inside its own metal-like mount", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h113_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the mount attaches to a selected neck or ear carrier", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h113_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "surface colour patches remain within that stone", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Iridescent lighting, a painted cloth motif or a white pearl doesn't establish opal chemistry, wealth or class.
- 출처 상태: SEED_LEAD; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/)
- 기존 profile: clothing_ct111_v2; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Madame Maxime opal material and precise mounting are source leads; halo setting is not mandatory.
- 참조 행: ref_047
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H114 긴 코트 전면의 원·소용돌이 문양

긴 코트의 천 패널 안에서 원·소용돌이 문양이 반복되며 옷 몸판과 솔기 경계를 유지한다.

repeated curved motifs occupy one long coat surface; the motifs remain bounded by its actual cloth panels; the coat body and garment seams remain readable underneath.

- 관찰 요소: repeated curved motifs occupy one long coat surface / the motifs remain bounded by its actual cloth panels / the coat body and garment seams remain readable underneath
- 소유·관계: [{"id": "h114_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "repeated curved motifs occupy one long coat surface", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h114_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the motifs remain bounded by its actual cloth panels", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h114_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the coat body and garment seams remain readable underneath", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: A background gold pattern, actual smoke or global swirl effect isn't coat-surface ornament.
- 출처 상태: SEED_LEAD; [S28](https://www.metmuseum.org/exhibitions/listings/2016/manus-x-machina/exhibition-galleries)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: HOLD_EXACT_CASE — Xenophilius film gold/mustard fabric and pattern repeat require an original still; a generic motif is a researcher proposal.
- 참조 행: ref_083
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H115 단순 주머니형 천옷의 머리·팔 구멍

단순한 천 몸판의 머리·팔 구멍 경계를 보이고 비인간 몸통 위의 별도 덮개로 둔다.

a simple cloth body hangs from the selected shoulder region; a head opening and arm openings remain actual cloth boundaries; the cloth stays a separate covering over the declared nonhuman torso.

- 관찰 요소: a simple cloth body hangs from the selected shoulder region / a head opening and arm openings remain actual cloth boundaries / the cloth stays a separate covering over the declared nonhuman torso
- 소유·관계: [{"id": "h115_r1", "subject": "head_and_arm_openings", "type": "bounded_by", "object": "same_simple_cloth", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h115_r2", "subject": "cloth_body", "type": "separate_covering_on", "object": "nonhuman_torso", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: A skin membrane, ordinary tailored robe or actual bedding pillowcase alone isn't a worn simple tunic; cloth doesn't define species.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/), [S09](https://www.wbstudiotour.co.uk/press-office/wbstl-press-pack/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: SOURCE_AND_NONHUMAN_OWNER_REVIEW — Dobby pillowcase exact colour and seam construction not verified by production-method pages; source leads retained.
- 참조 행: ref_029
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H116 양쪽의 작은 머리 묶음과 안경

같은 머리의 양쪽 묶임점과 이어진 두 묶음을 보이고 안경은 별도 구조로 남긴다.

two visible hair gathering points belong to one head; each point leads into a distinct side bundle; a separate spectacle frame remains outside those bundles.

- 관찰 요소: two visible hair gathering points belong to one head / each point leads into a distinct side bundle / a separate spectacle frame remains outside those bundles
- 소유·관계: [{"id": "h116_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "two visible hair gathering points belong to one head", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h116_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "each point leads into a distinct side bundle", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h116_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate spectacle frame remains outside those bundles", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Loose sidelocks, one rear ponytail or knots on a bonnet don't establish two scalp-attached bundles.
- 출처 상태: SEED_LEAD; [S31](https://www.harrypotter.com/features/the-top-five-most-fashionable-hogwarts-teachers)
- 기존 profile: bilateral_twin_tail_gather; 기존 후보: 없음
- 제안 처리: REUSE_WITH_CASE_HOLD — Myrtle's exact hair style/era/ghost schoolwear needs film image evidence; lens shape isn't inferred from two tails.
- 참조 행: ref_030
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H117 손톱·깃펜·가방의 소유 분리

손톱색은 같은 손에 한정하고 깃펜·가방은 실제 잡는 손과 연결하며 소품색을 옷색과 분리한다.

selected nail colour stays on one declared hand; a separate quill or bag is held by its actual fingers; object surface colour remains independent from nails and clothes.

- 관찰 요소: selected nail colour stays on one declared hand / a separate quill or bag is held by its actual fingers / object surface colour remains independent from nails and clothes
- 소유·관계: [{"id": "h117_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "selected nail colour stays on one declared hand", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h117_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "a separate quill or bag is held by its actual fingers", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h117_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "object surface colour remains independent from nails and clothes", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: Acid-green quill colour doesn't prove green clothing or nails; reporter role and writing function require separate context.
- 출처 상태: PARTIAL_TEXT_SUPPORTED; [S45](https://www.harrypotter.com/features/ranked-wizarding-fashion-icons-web), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: costume_ccx_cc36_01; 기존 후보: 없음
- 제안 처리: OWNER_SLOT_AND_SOURCE_HOLD — Rita canonical acid-green quill, crocodile bag and nails require dedicated source verification; do not adopt by colour association.
- 참조 행: ref_053, ref_054, ref_118
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H118 눈 고정부 띠와 별도 얼굴 피부

머리를 따라간 띠가 인공 눈의 고정부에 이어지고 띠·눈·피부 경계가 분리된다.

a strap path runs along a declared head region; the strap joins the selected artificial eye housing; skin remains distinct from the strap and eye boundary.

- 관찰 요소: a strap path runs along a declared head region / the strap joins the selected artificial eye housing / skin remains distinct from the strap and eye boundary
- 소유·관계: [{"id": "h118_r1", "subject": "strap", "type": "joins", "object": "artificial_eye_housing", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h118_r2", "subject": "strap", "type": "follows", "object": "selected_head_region", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h118_r3", "subject": "skin", "type": "separate_from", "object": "strap", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: An eyepatch strap, headband or glasses arm isn't an artificial-eye mount; exact side isn't inferred.
- 출처 상태: SEED_LEAD; [S11](https://www.harrypotter.com/fact-file/objects/mad-eye-moodys-eye)
- 기존 profile: sca_x04; 기존 후보: 없음
- 제안 처리: HOLD_FILM_MOUNT — Magic eye text confirms iris/device, but film strap/side path still needs original source pixels.
- 참조 행: ref_055, ref_095
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H119 군집 안의 개체별 얼굴·가면 차이

여러 인물의 머리·가면 소유를 나누고 코·귀·턱·문양의 국소 차이를 유지한다.

several separate heads or masks retain their own owners; each selected nose ear chin or pattern differs locally; each owner retains separate feature contours beneath shared costume choices.

- 관찰 요소: several separate heads or masks retain their own owners / each selected nose ear chin or pattern differs locally / each owner retains separate feature contours beneath shared costume choices
- 소유·관계: [{"id": "h119_r1", "subject": "each_head_or_mask", "type": "owned_by", "object": "its_participant", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}, {"id": "h119_r2", "subject": "individual_features", "type": "separate_across", "object": "participants", "owner_binding": "same_declared_owner_unless_explicit_scene_participants"}]
- 오인 경계: Repeating one cloned face or mixing one actor's ear with another's jaw doesn't prove individual designs.
- 출처 상태: TEXT_SUPPORTED; [S07](https://www.harrypotter.com/features/death-eater-masks-and-costumes), [S08](https://www.wbstudiotour.co.uk/the-experience/explore-the-tour/creature-effects/)
- 기존 profile: 없음; 기존 후보: 없음
- 제안 처리: MULTI_OWNER_REVIEW — Goblins use anatomical/prosthetic face variation; masked humans use object-pattern variation. Keep species, manufacture and representation distinct.
- 참조 행: ref_089, ref_101
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.

## H120 노란 기가 약한 밝은 머리색

밝은 색을 머리 가닥 안에 한정하고 따뜻한 금색과 비교해 노란 기가 적도록 선택한다.

light colour occupies bounded hair strands; the selected pale hue has low yellow saturation; the selected hue remains localized to the bounded hair strands.

- 관찰 요소: light colour occupies bounded hair strands / the selected pale hue has low yellow saturation / the selected hue remains localized to the bounded hair strands
- 소유·관계: [{"id": "h120_r1", "subject": "component_1", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "light colour occupies bounded hair strands", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h120_r2", "subject": "component_2", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the selected pale hue has low yellow saturation", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}, {"id": "h120_r3", "subject": "component_3", "type": "co_owned_by", "object": "declared_carrier", "predicate_en": "the selected hue remains localized to the bounded hair strands", "owner_binding": "same_declared_owner_unless_explicit_scene_participants", "endpoint_mapping_status": "REVIEW_REQUIRED"}]
- 오인 경계: White balance, silver wig chemistry, grey ageing hair and warm blonde are separate; hair colour doesn't determine sex or ancestry.
- 출처 상태: TEXT_AND_SAMPLE_PIXELS; [S03](https://www.harrypotter.com/features/harry-potter-book-character-descriptions-versus-how-they-looked-in-the-films), [S24](https://x.com/redteneri/status/2102398387194626330), [S25](https://x.com/masoq095/status/2105042738517295257), [S26](https://x.com/grizz056/status/1766771258178613565)
- 기존 profile: 없음; 기존 후보: silver_blonde_gothic_hair
- 제안 처리: SIBLING_OR_COLOUR_MODIFIER — Current silver-blonde Gothic candidate adds style context; neutral cool pale blonde should preserve colour locks without Gothic genre.
- 참조 행: ref_017, ref_028, ref_061, ref_108, ref_114, ref_119, ref_120, ref_121, ref_124, ref_125
- 이미지 판정: 선택한 관계를 모두 원본 픽셀에서 확인. 부분 통과는 실패, 필수 부위 가림은 UNOBSERVABLE_NOT_PASS.


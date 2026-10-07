# Semantic cards — 60 reviewed research proposals

All cards are researcher-authored design proposals. They are not live assets, mandatory meanings, or tested image effects.

## VEL-001 — 관능·친밀감·위험감의 별도 의미 축

- Keywords: K001, K002, K003, K004
- Kind / priority: authoring_guidance / P1
- Owner: resolved adult appeal intent and declared scene
- Slots: mood, expression, atmosphere
- Observable proposition: The authored scene resolves attraction, private familiarity, and perceived danger separately; concrete carriers realize only the meaning actually selected.
- Components: requested appeal direction; declared context; specific present carriers
- Relations: 
- Confusions: sultry label as facial geometry; intimate distance as consent; danger label as actual assault
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf), [R10](https://radar.gsa.ac.uk/5735/)
- Adoption note: 원래 연령 미확인 S09는 관찰 자료로 유지한다. 추상 의도는 형태 원자가 아니며 현행 sensual/fetish controls의 뜻과 값을 변경하지 않는다.

## VEL-002 — 밀착 핏과 신체 형상의 분리

- Keywords: K005, K008, K009, K013, K014
- Kind / priority: reuse_extend / P1
- Owner: declared garment on the same subject
- Slots: garment_detail, wardrobe_style, silhouette_proportion
- Observable proposition: A fitted garment follows the declared torso contour; waist shaping belongs to its seams and outer boundary while the wearer's prescribed body proportions remain intact.
- Components: continuous garment edges; visible fitted waist boundary; seams or tension folds on that garment
- Relations: garment → follows → declared torso; waist seams → shape → same garment boundary
- Confusions: body reshaping to simulate fit; unrequested corset; tight fit as transparency
- Existing IDs to review: pfe_opaque_fit, pfe_skimming
- Research sources: [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- Adoption note: 기존 fitted/opaque/skimming 후보의 효과 범위를 비교한다. 핏·체형·노출을 같은 효과로 확장하지 않는다.

## VEL-003 — 슬릿의 높이·경계·의상 정체성

- Keywords: K006, K007
- Kind / priority: reuse_extend / P0
- Owner: one selected dress and one continuous leg
- Slots: garment_detail, costume_style
- Observable proposition: Two finished edges form a side opening in the same dress; the selected leg is visible through that opening while the dress's remaining panel and hem remain continuous.
- Components: two finished slit edges; same garment panel and hem; one anatomically continuous leg
- Relations: slit edges → bound → visible opening; leg → appears through → same dress opening
- Confusions: a torn panel instead of a constructed slit; two disconnected legs; generic China dress forced into a canonical qipao
- Existing IDs to review: pfe_slit, slot:garment_detail:pfe_slit_candidate
- Research sources: [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- Adoption note: 재사용 기존 pfe_slit. 민소매·차이나 드레스만으로 칼라·사선 여밈·전통 판본 전체를 추가하지 않는다. 높이는 원 요청의 부위 관계로 묶는다.

## VEL-004 — 코르셋형 절개선과 코르셋 시스템

- Keywords: K010, K015
- Kind / priority: new_relation_trial / P1
- Owner: selected vest or bodice panel
- Slots: garment_detail, wardrobe_style
- Observable proposition: Curved vertical seams divide a fitted vest's torso panels and remain visibly joined to those panels; a seam pattern alone does not introduce lacing, boning, underwear, or restraint.
- Components: curved panel seams; continuous adjoining cloth panels; declared vest silhouette
- Relations: curved seams → join → torso panels
- Confusions: painted stripes; bra cup seams replacing torso panels; automatic lacing or boning
- Existing IDs to review: slot:fetish_styling:corset_bustier_layered, slot:wardrobe_style:y2kr_bustier
- Research sources: [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [R09](https://www.vam.ac.uk/museumofsavagebeauty/mcq/coiled-corset/)
- Adoption note: 기존 layered corset/bustier 후보는 다른 의복·효과일 수 있다. 단순 동의어 추가 전에 새 garment_detail 원자로 비교한다.

## VEL-005 — 볼륨과 내부 패드의 관측 한계

- Keywords: K011, K012
- Kind / priority: claim_guard / P1
- Owner: declared garment region and hidden construction
- Slots: garment_detail, silhouette_proportion
- Observable proposition: Visible garment volume may be described at a named region, but a concealed integrated pad is an authored construction premise rather than a pixel-observable internal structure.
- Components: named volume owner; outer contour; visible pad boundary only if naturally exposed
- Relations: 
- Confusions: volume without an owner; body enlargement as padding; claiming a hidden pad passed pixel inspection
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- Adoption note: 안 보이는 패드를 검증하기 위해 의상을 벗기거나 절개하지 않는다. 내부 제작 조건과 겉 실루엣의 증거를 분리한다.

## VEL-006 — 라텍스풍 반사·핏·검정의 소유

- Keywords: K016, K018, K019, K020
- Kind / priority: reuse_extend / P1
- Owner: selected garment surface
- Slots: surface_material, garment_detail
- Observable proposition: The selected black garment retains continuous edges and local reflective bands that curve with its folds; fit, base color, and specular response are separate owned properties.
- Components: bounded garment surface; fold-following specular bands; dark base planes retaining material detail
- Relations: highlight → lies on → garment fold; base color → belongs to → same garment
- Confusions: black acrylic furniture instead of clothing; global bloom instead of surface sheen; latex as an automatic sexual role
- Existing IDs to review: hvr_profile_fetish_material_owner, slot:fetish_styling:glossy_latex_look
- Research sources: [R10](https://radar.gsa.ac.uk/5735/), [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R12](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory)
- Adoption note: 현행 latex/leather 혼합 프로필의 전제·추가 여밈 요구를 확인한다. 재료 원자만 필요한 요청에 새 여밈이나 fetish 문맥을 필수로 넣지 않는다.

## VEL-007 — 무광 가죽·금속·노후 표면의 대비

- Keywords: K017, K021, K022, K023
- Kind / priority: reuse_extend / P1
- Owner: two declared garment or armor surfaces
- Slots: surface_material, texture
- Observable proposition: The declared leather-like panel has restrained surface sheen, while its adjacent metal ornament has separately bounded reflections and visible localized wear.
- Components: two separate material owners; restrained cloth or leather-like sheen; bounded metal highlight and wear
- Relations: metal ornament → attaches to → declared panel
- Confusions: global dirt over the person; all surfaces with the same gloss; patina as bodily injury
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R12](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory)
- Adoption note: leather-like는 외관 비교로 유지한다. 피부·머리 청결을 바꾸지 않고 장식 금속의 마모만 지정한다.

## VEL-008 — 새틴의 방향성 광택과 실크 섬유

- Keywords: K024, K026
- Kind / priority: reuse_extend / P0
- Owner: same satin-like garment
- Slots: surface_material, garment_detail
- Observable proposition: A continuous satin-like garment carries broad smooth luster along its fold curvature while seams and darker planes retain surface continuity.
- Components: continuous satin-like surface; fold direction; broad luster; seam and dark-plane continuity
- Relations: luster → follows → same garment folds
- Confusions: silk as a synonym of every satin; wet skin shine replacing fabric luster; glare obscuring seam continuity
- Existing IDs to review: satin_directional_luster_drape_surface, slot:surface_material:satin_directional_luster_drape_surface, slot:surface_material:y2kr_satin
- Research sources: [R06](https://cameo.mfa.org/wiki/Satin), [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)
- Adoption note: 이미 충분한 기존 의미를 재사용한다. satin/ silk 병기 표현은 섬유와 직조의 두 축으로 연구표에서 분해하되 원문을 고치지 않는다.

## VEL-009 — 레이스 트림의 부착선·빈 셀·자유 가장자리

- Keywords: K025
- Kind / priority: reuse_extend / P0
- Owner: lace band and separate base garment
- Slots: garment_detail, surface_material
- Observable proposition: A narrow openwork lace band is attached along an edge of the base garment, with a readable join and a distinct free edge.
- Components: narrow lace band; real openwork cells; attachment line; free lace edge
- Relations: lace band → joins along → base garment edge
- Confusions: printed lace graphics; all-over lace replacing trim; detached lace accessory
- Existing IDs to review: lace_trim_attached_edge, slot:garment_detail:lace_trim_edge
- Research sources: [R07](https://underpinningsmuseum.com/museum-collections/julia-silk-satin-lace-applique-slip-by-carine-gilson/)
- Adoption note: 기존 프로필의 원자·gate를 보존한다. 불투명 바탕은 원래 선택된 후보가 요구할 때만 적용하며 일반 lace trim의 새 기본값으로 만들지 않는다.

## VEL-010 — 목선 모양·깊이·보이는 부위

- Keywords: K027, K028, K031, K034
- Kind / priority: reuse_extend / P0
- Owner: adult subject, neckline edge and selected body region
- Slots: garment_detail, body_framing
- Observable proposition: The declared neckline edge has a readable shape and depth relative to the torso; the requested visible body region is continuous with that edge.
- Components: neckline boundary; shape and torso reference; requested visible region
- Relations: neckline → bounds → selected exposed region
- Confusions: low neckline automatically meaning cleavage; chest highlight replacing an opening; cropped neckline claimed as verified
- Existing IDs to review: decolletage_neckline_exposure, pfe_cleavage
- Research sources: [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [R19](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html)
- Adoption note: decolletage와 cleavage 기존 프로필의 의미 차이를 유지한다. square/low/cleavage를 하나의 alias로 묶지 않고 성인 문맥과 요청 부위를 각각 확인한다.

## VEL-011 — 가는 어깨끈의 폭과 연결

- Keywords: K029, K033
- Kind / priority: reuse_extend / P1
- Owner: selected dress strap
- Slots: garment_detail, wardrobe_style
- Observable proposition: A narrow shoulder strap runs continuously from the selected garment front over the shoulder to its declared rear attachment.
- Components: narrow strap width; shoulder crossing; front and rear garment attachment
- Relations: strap → connects → same garment front and rear
- Confusions: bag strap instead of garment strap; floating thin line; thinness as automatic undressing
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R07](https://underpinningsmuseum.com/museum-collections/julia-silk-satin-lace-applique-slip-by-carine-gilson/)
- Adoption note: spaghetti/thin strap은 폭 축이다. 비대칭 흘러내림·오프숄더·목걸이와 분리한다.

## VEL-012 — 한쪽 어깨끈의 이탈 위치

- Keywords: K030
- Kind / priority: new_relation_trial / P0
- Owner: one garment-owned strap and its shoulder
- Slots: garment_detail
- Observable proposition: One attached shoulder strap lies below its own shoulder crest; its front and rear garment connections remain traceable while the opposite side keeps its independently declared state.
- Components: selected side ownership; strap below shoulder crest; garment attachment continuity; opposite side state
- Relations: selected strap → lies below → same-side shoulder crest; strap ends → remain attached to → same garment
- Confusions: designed one-shoulder garment; bag strap; both straps falling; additional unrequested exposure
- Existing IDs to review: pfe_one_shoulder, slot:garment_detail:y2kr_bra_straps
- Research sources: [R07](https://underpinningsmuseum.com/museum-collections/julia-silk-satin-lace-applique-slip-by-carine-gilson/), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 설계된 one-shoulder와 상태 변형을 구별하는 별도 관계 후보 trial. 정지 프레임에서 실제 흘러내린 시간·원인은 입증하지 않는다.

## VEL-013 — 슬립 형식과 속옷·겉옷 용도

- Keywords: K032
- Kind / priority: context_guard / P1
- Owner: selected slip-like garment system
- Slots: wardrobe_style, costume_style
- Observable proposition: A slip-like dress is represented through its selected straps, drape, and trim; actual undergarment use, outerwear layering, and erotic intent remain separately resolved context.
- Components: garment silhouette; selected strap and trim; declared layering context
- Relations: 
- Confusions: lingerie-inspired as nakedness; adding a tee or lining by default; underwear label as sexual activity
- Existing IDs to review: underwear_as_outerwear_layer_system, slot:wardrobe_style:dropwaist_satin_slip_dress
- Research sources: [R07](https://underpinningsmuseum.com/museum-collections/julia-silk-satin-lace-applique-slip-by-carine-gilson/), [R08](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)
- Adoption note: 기존 underwear-as-outerwear는 레이어가 요청된 경우에만 선택한다. 일반 슬립 의상에 새 가림/노출 조건을 덧붙이지 않는다.

## VEL-014 — 젖음·광택·투과의 독립 축

- Keywords: K035, K037, K038, K042
- Kind / priority: new_relation_trial / P0
- Owner: declared cloth region
- Slots: garment_detail, surface_material
- Observable proposition: Moisture belongs to one bounded cloth region; sheen and selected partial transmission are represented independently while the same fabric's edges remain continuous.
- Components: bounded wet region; cloth edge continuity; separate reflection evidence; separate transmission evidence if selected
- Relations: moisture → belongs to → cloth region; transmitted underlying contour → is visible through → selected cloth region
- Confusions: wet automatically becoming see-through; surface glare as transmission; dry sheer cloth as proof of wetness; unrequested change to exposed anatomy
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R12](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory), [R20](https://ora.ox.ac.uk/objects/uuid%3Abce39250-7534-457d-8342-343b77088615)
- Adoption note: wet 상태만으로 transparency 후보를 채택하지 않는다. 젖음과 투과를 결합한 원문에서는 두 속성을 각각 bind한다. 실제 직물 투과율·젖음의 인과는 미검증.

## VEL-015 — 젖은 원단의 접촉·장력·주름

- Keywords: K036
- Kind / priority: new_relation_trial / P0
- Owner: selected garment and same subject region
- Slots: garment_detail, contact_point
- Observable proposition: The selected garment adheres locally to its declared body region; nearby cloth tension and folds connect that contact to traceable garment edges.
- Components: local cloth-body contact; connected tension folds; garment edge continuity
- Relations: garment patch → contacts → declared body region; folds → continue from → same contact boundary
- Confusions: body deformation; static-cling synonym without moisture context; uniform vacuum wrapping; transparency inferred from adherence
- Existing IDs to review: slot:garment_detail:static_cling_fabric
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability), [R20](https://ora.ox.ac.uk/objects/uuid%3Abce39250-7534-457d-8342-343b77088615)
- Adoption note: 기존 static-cling은 원인·문맥이 다를 수 있다. 밀착·젖음·투과를 별도로 선택하고 몸 자체의 비율을 바꾸지 않는다.

## VEL-016 — 젖은 머리 가닥의 무게와 접촉

- Keywords: K039
- Kind / priority: reuse_extend / P0
- Owner: same subject hair and face or neck
- Slots: hair_style, contact_point
- Observable proposition: Damp hair forms traceable strand bundles with local adherence to the declared skin region; roots and the contact path stay visible.
- Components: root-to-strand continuity; wet bundle state; declared skin contact
- Relations: wet strands → adhere to → same subject cheek or neck
- Confusions: dry slick hairstyle; oily shine only; strands crossing into another owner
- Existing IDs to review: wet_damp_clumped_hair_state, slot:hair_style:hr_wet_hair_skin_contact
- Research sources: [R20](https://ora.ox.ac.uk/objects/uuid%3Abce39250-7534-457d-8342-343b77088615)
- Adoption note: 기존 wet_damp 프로필과 접촉 후보를 재사용. 과거 샤워 사실이나 인물의 성적 상태를 뜻으로 추가하지 않는다.

## VEL-017 — 피부 물방울과 하이라이트의 위치

- Keywords: K040
- Kind / priority: reuse_extend / P1
- Owner: selected visible skin patch
- Slots: skin_condition, skin_finish, light_direction
- Observable proposition: Discrete droplets or bounded moisture on a selected skin patch carry light-consistent highlights without transferring that wetness to neighboring fabric or the whole body.
- Components: skin patch owner; droplet boundary or bounded moisture; coherent local highlight
- Relations: droplet highlight → lies on → selected skin patch
- Confusions: plastic skin; glitter or makeup as water; whole-body wetness inferred from one spot
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R14](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)
- Adoption note: 피부 물기·뷰티 메이크업·장면 광택을 분리한다. 원래 청결 조건이나 의복 상태를 덮지 않는다.

## VEL-018 — 거울 김·물방울과 샤워 서사

- Keywords: K041, K043
- Kind / priority: new_relation_trial / P1
- Owner: mirror or glass surface and visible room
- Slots: reflection_logic, surface_material
- Observable proposition: Condensation and discrete droplets occupy the mirror plane; visible reflection remains continuous in the unoccluded region while moisture does not migrate to the lens or the reflected person.
- Components: mirror plane; bounded condensation; discrete surface droplets; unoccluded reflection continuity
- Relations: condensation → occupies → mirror plane
- Confusions: lens fog; opaque white paint; wet hair as proof of a completed shower
- Existing IDs to review: rb_glass_reflection_transmission
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R13](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits)
- Adoption note: just-out-of-shower는 상황 해석이며 시간 증거가 아니다. mirror plane/카메라 렌즈/공기 안개를 따로 기록한다.

## VEL-019 — 긴 장갑의 길이와 끝단

- Keywords: K044, K045
- Kind / priority: reuse_extend / P1
- Owner: selected glove on one arm
- Slots: wearable_accessory, garment_detail
- Observable proposition: The glove continuously covers the selected hand and forearm; its upper edge sits above the same arm's elbow with the declared gloss.
- Components: hand-to-forearm glove continuity; same elbow reference; upper cuff edge; local gloss
- Relations: glove cuff → lies above → same arm elbow
- Confusions: long sleeve mistaken for a glove; floating cuff; black glove as aggression or fetish intent
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)
- Adoption note: above the elbows를 독립 mood 대신 소유된 길이 관계로 묶고 좌우 장갑 상태를 혼동하지 않는다.

## VEL-020 — 초커·O링·넥 아머의 다른 구조

- Keywords: K046, K047, K048
- Kind / priority: new_relation_trial / P0
- Owner: neck band, front ornament and neck armor as separately selected objects
- Slots: wearable_accessory, garment_detail
- Observable proposition: A close neck band retains a continuous fastening path; a selected front ring attaches to that band and remains distinct from any separately chosen protective neck piece.
- Components: neck-band continuity; front ornament attachment; ring contour; separate armor ownership
- Relations: front ring → attaches to → neck band
- Confusions: bag ring; detached floating ring; neck armor forced into jewelry; ring interpreted as restraint
- Existing IDs to review: slot:wearable_accessory:y2kr_tattoo_choker, slot:wearable_accessory:royal_crest_choker
- Research sources: [R09](https://www.vam.ac.uk/museumofsavagebeauty/mcq/coiled-corset/), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 검정 밴드·금속 링·neck armor의 원자 조합. 장식 착용만으로 실제 움직임 제한이나 성적 역할을 추가하지 않는다.

## VEL-021 — 스트랩·체인의 연결점과 처짐

- Keywords: K049, K050, K053
- Kind / priority: new_relation_trial / P0
- Owner: declared garment attachments and hanging chain
- Slots: wearable_accessory, garment_detail
- Observable proposition: A narrow strap connects at declared garment points; the decorative chain hangs between or from its own attachment points with a coherent downward curve.
- Components: declared attachment points; continuous strap; continuous chain links; downward drape
- Relations: chain → hangs from → declared garment attachment; buckle → joins → selected strap segments
- Confusions: floating chain; chain connecting unrelated bodies; taut restraint replacing loose decoration; accessory becoming a skin cut
- Existing IDs to review: slot:wearable_accessory:y2kr_chain_strap, slot:wearable_accessory:unif_lapel_chain_separate_inner_neck
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 가방·라펠 전용 기존 관계를 일반 의상에 바로 동의어 확장하지 않는다. 다른 owner면 새 variant가 필요하다.

## VEL-022 — 부분 보호 장식과 실제 보호 기능

- Keywords: K051
- Kind / priority: claim_guard / P2
- Owner: selected ornament or armor patch
- Slots: garment_detail, costume_style
- Observable proposition: A bounded protective-looking ornament overlaps only the declared garment or body region; unobserved protective performance remains outside the visual claim.
- Components: bounded plate or ornament; declared attachment; selected coverage region
- Relations: ornament → overlaps → selected region
- Confusions: complete armor added from one patch; proof of protection; extra straps invented to force fit
- Existing IDs to review: wearable_protective_armor_system
- Research sources: [R09](https://www.vam.ac.uk/museumofsavagebeauty/mcq/coiled-corset/), [R16](https://www.metmuseum.org/art/collection/search/35728)
- Adoption note: 부분적 의상 장식과 완전 armor-system의 필수 구조를 구별한다.

## VEL-023 — 느슨한 가죽 넥타이의 매듭 상태

- Keywords: K052
- Kind / priority: reuse_extend / P1
- Owner: same subject tie and shirt collar
- Slots: wearable_accessory, garment_detail
- Observable proposition: The selected leather-like tie knot sits below its collar reference with a traceable loop and a gravity-following hanging blade.
- Components: collar reference; lowered knot; continuous loop; hanging tie blade
- Relations: tie knot → lies below → same collar
- Confusions: scarf or strap substitute; necktie as choking device; exposure expansion
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 격식의 느슨함은 창작 해석이다. 끈의 해부학적 연결을 구체화하고 목을 제한하는 뜻으로 바꾸지 않는다.

## VEL-024 — 누운 신체와 침구 눌림의 접촉

- Keywords: K054, K055, K057
- Kind / priority: new_relation_trial / P0
- Owner: one body and its supporting bedding
- Slots: body_pose, contact_point
- Observable proposition: The reclining subject has readable torso and limb support; the bedding depresses at the same contact region and adjacent folds respond locally to that load.
- Components: declared reclining support; same body-bedding contact; localized depression; connected bedding folds
- Relations: body contact region → depresses → same bedding patch
- Confusions: bed dent away from the body; body levitation; global wrinkling as contact; bedroom as sexual activity
- Existing IDs to review: pv_profile_supine, pv_profile_side_lying
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 원래 relaxed limb 위치를 유지한다. 침구 패턴/장식 대신 접촉 부위와 국소 변형을 보강하며 체중 수치·실제 수면 상태를 추정하지 않는다.

## VEL-025 — 거울 시선과 세면대의 공간 관계

- Keywords: K058, K059, K061
- Kind / priority: reuse_extend / P0
- Owner: subject, mirror plane and sink if present
- Slots: gaze_target, reflection_logic, body_pose, location
- Observable proposition: The subject's visible gaze is directed toward their reflected face; the mirror plane and reflection align with the body's actual position beside the declared sink.
- Components: subject gaze target; mirror plane; same subject reflection; sink/body support if selected
- Relations: subject eyes → look toward → own reflected face; reflection → corresponds to → same subject
- Confusions: camera gaze substituting for mirror gaze; second person in the mirror; adding a sink to an unrelated portrait
- Existing IDs to review: rb_glass_reflection_transmission
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 기존 건축 유리 프로필은 반사면 근거일 뿐 인물 reflection 의무를 자동 충족하지 않는다. 새 directed gaze 관계를 부분 trial.

## VEL-026 — 손으로 젖은 머리를 쓸어 넘기는 접촉

- Keywords: K060
- Kind / priority: new_relation_trial / P1
- Owner: same subject hand and hair
- Slots: hand_pose, action, contact_point
- Observable proposition: The raised hand reaches the subject's own damp hair; fingertips and strand bundles share a visible contact region while arm continuity and torso balance remain intact.
- Components: same arm and hand owner; fingertip/hair contact; hair bundle continuity; body support
- Relations: own fingertips → contact → own wet hair
- Confusions: hand near hair without required contact; another person's hand; detached strands
- Existing IDs to review: slot:hair_style:hr_wet_hair_skin_contact
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 일반 hand-in-hair와 실제 접촉 선택을 구별한다. 근처/통과/정리 중 표현의 확정 의미는 original context로 결정한다.

## VEL-027 — 무릎 꿇기·손바닥 위·봉헌의 층

- Keywords: K062, K063, K064
- Kind / priority: reuse_extend / P0
- Owner: declared kneeling actor and hand targets
- Slots: body_pose, hand_pose, relational_action
- Observable proposition: The selected kneeling configuration keeps knees, feet and pelvis support readable; the declared palms face upward and hold a selected cupped shape without an invented coercing actor.
- Components: selected knee and foot support; pelvis continuity; palms-up orientation; declared target if present
- Relations: knees → contact → declared support; palms → face → upward direction
- Confusions: kneeling as automatic submission; new controller or deity added from the pose; prayer label as proof of personal belief
- Existing IDs to review: pv_profile_tall_kneel, pv_profile_heel_sit, pv_profile_half_kneel
- Research sources: [R15](https://www.metmuseum.org/art/collection/search/546745), [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 자세 geometry 재사용. 원문 기도·봉헌은 관계/상황으로 보존하며 새로운 종교 도상이나 성적 역할을 기본으로 만들지 않는다.

## VEL-028 — 시선·눈꺼풀·차분함과 내면 추론

- Keywords: K056, K065, K066, K067, K068, K069, K070, K072
- Kind / priority: reuse_extend / P1
- Owner: one subject face and declared gaze target
- Slots: expression, gaze_engagement, gaze_target
- Observable proposition: Visible eyelid aperture and pupil direction are recorded on the same face; a calm or dreamy reading is contextual authoring intent rather than proof of a unique internal state.
- Components: visible eyes; declared pupil target; eyelid aperture; same face ownership
- Relations: eyes → aim toward → declared target
- Confusions: eyelid relaxation as desire; camera gaze as consent; pensive as psychiatric diagnosis
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf)
- Adoption note: 기존 세부 표정 프로필의 geometry를 조합하되 감정어를 hard morphology의 동의어로 넣지 않는다. 잠들기 전·우연성은 순간 서사다.

## VEL-029 — 작은 입술 틈과 측정 한계

- Keywords: K071
- Kind / priority: reuse_extend / P1
- Owner: same face upper and lower lip
- Slots: expression
- Observable proposition: The upper and lower lips remain near each other with a small visible central gap; jaw opening and lip shape retain the requested expression.
- Components: upper lip boundary; lower lip boundary; small central gap; independently constrained jaw
- Relations: upper and lower lips → bound → small central opening
- Confusions: wide jaw drop; pout replacing lip parting; unscaled pixel gap certified as 1–2 mm
- Existing IDs to review: ae_profile_lip_press, ae_profile_lip_tighten
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf)
- Adoption note: 닫힌 lip_press/lip_tighten을 선택해 열린 입술을 대체하지 않는다. 1–2mm는 original authored scale intent이며 참조 눈금 없는 사진에서 mm PASS 판정하지 않는다.

## VEL-030 — 1인칭 높이·방향과 관계의 분리

- Keywords: K073, K074, K075, K077, K078, K080, K081, K082
- Kind / priority: new_relation_trial / P0
- Owner: declared camera and subject; POV body only if given
- Slots: viewer_position, camera_height, camera_direction, composition
- Observable proposition: A first-person camera occupies its declared height beside the support surface and looks upward toward the subject; relative height does not itself introduce body contact or control.
- Components: camera height reference; camera view direction; subject position; declared POV body region when necessary
- Relations: camera → lies below → subject face; camera optical axis → points toward → subject face
- Confusions: low angle as physical restraint; POV without a declared body interpreted as chest contact; close framing as consent
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R13](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: floor/stone reference와camera방향을 분리해 owner bind. 원문 제압의 별도 contact 의미는 VEL-041에서 다룬다.

## VEL-031 — 필수 얼굴·관계 단서의 초점 가독성

- Keywords: K076, K079
- Kind / priority: reuse_extend / P0
- Owner: frame, focus planes and required evidence owners
- Slots: focus, subject_framing, composition
- Observable proposition: The selected face remains in focus while each independently required contact or garment boundary is readable at its own depth; shallow depth is a selected treatment rather than permission to erase required evidence.
- Components: face focus; required relationship visibility; chosen depth hierarchy
- Relations: focus region → includes → required visible evidence when co-realized
- Confusions: sharp face but hidden required contact; numerical aperture as proof of focus; changing requester blur to satisfy a test
- Existing IDs to review: pfe_face_garment
- Research sources: [R13](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits)
- Adoption note: 시각 의무 all-of 조합을 검토. 사용자가 의도한 가림·흐림은 보존하고 그 관계는 UNOBSERVABLE로 남긴다.

## VEL-032 — 무기 개수·소유자·장비의 형태

- Keywords: K083, K084, K085, K086, K087, K088, K089, K090, K091, K092, K093, K094
- Kind / priority: reuse_extend / P1
- Owner: declared carrier and separately counted equipment
- Slots: prop, wearable_accessory, costume_style, footwear
- Observable proposition: Each declared weapon remains one continuous object with its own carrier or mounting; tactical footwear and armor retain separate object identities without proving an attack.
- Components: declared object count; continuous object body; carrier or mount ownership; separate footwear or armor
- Relations: weapon → belongs to → declared carrier
- Confusions: one weapon duplicated across hands; equipment silhouette as attack; oversized firearm as actual damage
- Existing IDs to review: slot:prop:real_holstered_service_pistol
- Research sources: [R16](https://www.metmuseum.org/art/collection/search/35728), [R01](https://arxiv.org/abs/2310.11513)
- Adoption note: 총잡이·전술 소재는 역할/외형이다. 관측된 원문 장비와 공격 행동을 분리하고 실제 작동·전술 방법의 데이터로 확장하지 않는다.

## VEL-033 — 홀스터 안의 무기 상태

- Keywords: K087
- Kind / priority: reuse_extend / P0
- Owner: one sidearm and its worn holster
- Slots: prop, action, wearable_accessory
- Observable proposition: One sidearm is seated in its visible holster attached to the declared carrier; it is not simultaneously held in a hand or directed at a target.
- Components: one holster opening; weapon seated inside; carrier attachment; independently declared hand state
- Relations: sidearm → is seated in → same carrier holster
- Confusions: held weapon substituted for holstered state; holster without the requested object; new aiming target
- Existing IDs to review: slot:prop:real_holstered_service_pistol, slot:action:carrying_holstered_real_sidearm
- Research sources: [R16](https://www.metmuseum.org/art/collection/search/35728), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 기존 재질/형태 후보 재사용. no aiming 표현을 자동 semantic negative로 넣는 대신 선택 상태와 frozen meaning 충돌 검증으로 처리한다.

## VEL-034 — 발도·양손 소지·일반 소지의 상태

- Keywords: K095, K098, K099, K102
- Kind / priority: new_relation_trial / P0
- Owner: declared hand, weapon and sheath if selected
- Slots: action, hand_pose, contact_point, prop
- Observable proposition: The selected held object has a readable hand contact and continuous geometry; a partial draw retains the same object partly inside its declared sheath while dual holding keeps two distinct hand-object pairings.
- Components: hand-object ownership; required contact; selected sheath overlap; distinct bilateral pairing if selected
- Relations: declared hand → contacts → same selected object; partly drawn object → overlaps → own sheath opening
- Confusions: drawing a picture as weapon drawing; two hands holding one object instead of two objects; fully exposed object replacing partial draw; changing prop state into attack
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R16](https://www.metmuseum.org/art/collection/search/35728), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 범용 held/sheathed/transitional-contact contract를 우선 활용한다. 화기 작동법·검술 순서를 설계하지 않고 프레임에서 보이는 상태만 모델링한다.

## VEL-035 — 조준의 방향·대상과 발사의 차이

- Keywords: K096, K100, K101, K103
- Kind / priority: new_relation_trial / P0
- Owner: declared actor, carried prop and target if specified
- Slots: action, relational_action, body_pose
- Observable proposition: The declared prop's orientation is directed toward its specified target or off-frame direction; actor support and the prop's held contact remain readable without introducing a discharge or injury.
- Components: held-object continuity; declared direction; target ownership if present; actor support
- Relations: prop orientation → points toward → declared target or direction
- Confusions: aiming as firing; new victim invented from preparation; combat stance as contact damage
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 준비·자세·조준을 서로 다른 상태로 둔다. off-frame 대상은 새 인물로 채우지 않는다. 연령·피해 정도·무기 종류는 원 요청 소유다.

## VEL-036 — 재장전 등 시간 동사의 정지 증거

- Keywords: K097
- Kind / priority: claim_guard / P2
- Owner: declared prop and its visible state
- Slots: action, hand_pose, prop
- Observable proposition: A named temporal action is supported only by its authored present-frame hand-object configuration; duration, mechanical cycle completion and unseen operations require separate temporal evidence.
- Components: selected present-frame state; declared object continuity; visible contact if requested
- Relations: 
- Confusions: a completed process inferred from holding; arbitrary mechanism added for a verb; instructions for real firearm operation
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R18](https://www.bfi.org.uk/sight-and-sound/features/alfred-hitchcock-my-own-methods), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 원문 동사는 보존하되 공개 후보에 조작 순서/구동 레시피를 만들지 않는다. 새 의미 동의어 이전에 구체적 요청 문맥을 확보하는 hold.

## VEL-037 — 등 뒤 기계 무장의 장착 소유

- Keywords: K089, K091, K092
- Kind / priority: new_relation_trial / P1
- Owner: fictional mounted equipment and carrier
- Slots: prop, wearable_accessory, costume_style
- Observable proposition: A fictional back-mounted unit connects to its declared carrier through a readable mount; the unit's silhouette and the human body's support remain separately traceable.
- Components: unit silhouette; visible mount; carrier continuity; separate body contour
- Relations: equipment mount → connects → declared back carrier
- Confusions: floating machine; extra anatomical limb; real weapon engineering inferred from fictional shape
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R16](https://www.metmuseum.org/art/collection/search/35728), [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 미래형·기계식은 허구 외형의 한정 variant이다. 몸을 장비 부품으로 바꾸거나 유혈을 수반하는 새 행동을 추가하지 않는다.

## VEL-038 — 마법 시전·방어막·충돌의 대상 관계

- Keywords: K104, K105, K106, K107, K108, K109
- Kind / priority: new_relation_trial / P0
- Owner: declared fictional actors, effect origin and barrier
- Slots: action, relational_action, surreal_physics_detail
- Observable proposition: A fictional effect has a visible declared origin, a directed path and a localized encounter with the selected barrier; defensive actor and casting actor retain distinct roles if both are present.
- Components: declared origin; effect path; barrier surface; localized encounter; actor role ownership
- Relations: effect path → encounters → declared barrier region
- Confusions: floating glow with no origin or target; attacker and defender swapped; barrier impact becomes bodily injury; outstretched arm as proof of casting
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R01](https://arxiv.org/abs/2310.11513)
- Adoption note: 판타지 효과는 창작 설계이며 물리 현상의 과학적 정의가 아니다. 한 팔 확장과 실제 시전은 같은 alias로 묶지 않는다.

## VEL-039 — 충돌 불꽃·입자·파편의 발생 위치

- Keywords: K109, K110, K111, K112
- Kind / priority: new_relation_trial / P0
- Owner: effect contact zone and separate material fragments
- Slots: ambient_particle, motion, aftermath_trace
- Observable proposition: Light sparks and material fragments occupy a bounded encounter region; each selected fragment remains distinct from the figure's body and from global image-plane grain.
- Components: bounded collision region; local luminous particles; material fragment identities; figure continuity
- Relations: sparks or fragments → originate near → declared encounter zone
- Confusions: uniform sparkle overlay; blood instead of sparks; body parts instead of stone debris; dust as film grain
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R14](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)
- Adoption note: 반짝이는 입자·암석 파편·피부 피해의 owner를 분리한다. 사건 인과는 작성된 허구 상황의 의미이며 실제 발생 증명으로 보고하지 않는다.

## VEL-040 — 망토 운동과 움직임 원인의 범위

- Keywords: K113
- Kind / priority: reuse_extend / P1
- Owner: same actor and attached cloak
- Slots: garment_detail, motion
- Observable proposition: The actor's cloak remains attached to its declared collar or shoulder points; trailing folds extend behind that actor with a coherent present pose.
- Components: cloak attachment; same actor ownership; trailing folds; present motion direction
- Relations: cloak folds → trail behind → same actor
- Confusions: cloak detaches; wind direction treated as universal parallelism; robe motion as injury or attack
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 의복 움직임을 바람·회전·질주 등 하나의 자동 원인에 묶지 않는다. 선택된 장면의 cause와 부착 토폴로지를 함께 검토한다.

## VEL-041 — 가까움·접촉·움직임 제한의 구분

- Keywords: K114, K115, K118
- Kind / priority: new_relation_trial / P0
- Owner: nonsexual declared actors and their contact regions
- Slots: relational_action, contact_point, body_pose
- Observable proposition: Where nonsexual physical restraint is explicitly requested, the acting limb has a readable contact with the declared target region, the target has a supporting surface, and the authored restriction is kept distinct from mere spatial overlap.
- Components: two distinct actor owners; specified target region; readable contact boundary; target supporting surface
- Relations: acting limb → contacts → declared target region; target body → rests on → declared support
- Confusions: low camera angle as restraint; occlusion mistaken for contact; comforting embrace as force; sexual framing introduced into source school context
- Existing IDs to review: interpersonal_physical_assault_event
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: S15의 학생 맥락은 비성적 분석으로만 유지한다. adult-assault 프로필은 성인·원치 않는 힘·결과의 추가 전제를 가져 자동 재사용하지 않는다. 압력의 크기나 원치 않음은 픽셀만으로 인증하지 않는다.

## VEL-042 — 지지 다리·체중 문장·지속 시간의 한계

- Keywords: K116, K117, K119, K120
- Kind / priority: claim_guard / P0
- Owner: acting subject support limb and declared target support
- Slots: body_pose, contact_point, viewer_position
- Observable proposition: A planted support limb and continuous torso-limb geometry are visibly checked; steady pressure and the proportion of carried weight remain authored premises without measured force or temporal evidence.
- Components: planted support foot; same leg continuity; torso connection; target support if declared
- Relations: support foot → contacts → declared floor
- Confusions: floating support foot; limb belonging to wrong actor; one frame proving steady duration; force magnitude inferred from silhouette
- Existing IDs to review: contrapposto_weight_shift, pv_profile_half_kneel
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: neutral support 모델을 제압/폭력 의미로 확대하지 않는다. POV beneath와 실제 압력은 별개이며 support checks만 이미지 의무로 둔다.

## VEL-043 — 비접촉 질책과 문턱 대립

- Keywords: K121, K122, K124, K125, K126, K127, K128, K130, K131, K132
- Kind / priority: new_relation_trial / P0
- Owner: declared speaker, listener, hands/faces and threshold
- Slots: relational_action, gaze_target, proxemics, hand_pose
- Observable proposition: The declared speaker and listener occupy distinct positions around the selected threshold; the specified hand-to-face interval remains visibly open and their gaze targets remain owned.
- Components: two actor positions; declared threshold if present; visible hand-face gap; separate gaze targets
- Relations: speaker hand → remains separated from → listener face; actor positions → relate across → declared threshold
- Confusions: rebuke as a strike; wounded disbelief as a skin wound; new sexual relation; adult actor substituted into historical age-15 source
- Existing IDs to review: slot:action:ctx_listen_and_leave_room
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: K128 wounded는 문맥상 정서 표현이다. 성인 listener 후보는 원 source 연령과 같지 않으므로 기능적 gap 관계만 참고한다. 원문 비성적 언쟁의 나이를 바꾸지 않는다.

## VEL-044 — 비아냥·미완 발언의 서사층

- Keywords: K123, K129
- Kind / priority: authoring_guidance / P1
- Owner: speaker-listener relationship and present response
- Slots: expression, relational_action, narrative_phase
- Observable proposition: The scene may author an interrupted verbal exchange through present mouth, gesture and target attention; an unseen exact insult or elapsed dialogue is not a visual atom.
- Components: present mouth or gesture state; declared listener; response target
- Relations: 
- Confusions: fixed mouth shape proving an exact insult; adding subtitles without request; unfinished speech as assault
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf), [R18](https://www.bfi.org.uk/sight-and-sound/features/alfred-hitchcock-my-own-methods)
- Adoption note: 대사·시간 사실을 still-image gate로 만들지 않는다. 필요하면 기존 typed character-response assertion에서 baseline-trigger-response-consequence를 요청 근거로 구성하며 새 토픽 router를 만들지 않는다.

## VEL-045 — 전투 후 환경 파손과 인물 피해의 분리

- Keywords: K133, K134, K135, K136, K139, K140, K141, K142, K143, K144
- Kind / priority: new_relation_trial / P0
- Owner: declared room/city surfaces and debris
- Slots: space_condition, aftermath_trace, ambient_particle, location
- Observable proposition: Damaged furniture or architecture retains identifiable broken boundaries and nearby owned debris; dust or smoke remains localized while the figure's separately declared skin, hair and clothing states stay intact.
- Components: named broken object; break boundary; same-object debris; localized air trace; independent figure state
- Relations: debris → corresponds to → declared damaged object
- Confusions: ruin as proof of a recent fight; damaged room as wounded body; dark smoke as a specific cause; dangerous role as actual perpetration
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R18](https://www.bfi.org.uk/sight-and-sound/features/alfred-hitchcock-my-own-methods)
- Adoption note: 전투 직후는 source 서사이고 흔적은 현재 관찰 축이다. 파손 owner·손상 정도·인물 청결을 별도로 bind. 새 혈흔은 추가하지 않는다.

## VEL-046 — 내린 검·장갑 벗기기의 현재 상태

- Keywords: K137, K138
- Kind / priority: new_relation_trial / P1
- Owner: same actor hand, sword and glove
- Slots: action, hand_pose, prop, wearable_accessory
- Observable proposition: The same actor holds the sword in its declared lowered orientation; an independently selected glove-removal state keeps glove edge, own hand contact and garment ownership continuous.
- Components: sword hand contact; lowered orientation; glove edge; same actor ownership
- Relations: sword → is held by → declared hand; glove edge → is grasped by → same actor hand when selected
- Confusions: lowered sword as proof of completed attack; extra blood on blade; unrequested undressing; glove replaced by a detached hand
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R16](https://www.metmuseum.org/art/collection/search/35728), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 완료·천천히는 시간 전제다. 현재 물건 상태와 손 접촉을 구체화하고 사건 결과를 확대하지 않는다.

## VEL-047 — 혈흔·묻음과 신체 훼손의 다른 정도

- Keywords: K145, K146, K149, K154, K155
- Kind / priority: new_relation_trial / P0
- Owner: declared fictional stain substrate or body region
- Slots: aftermath_trace, skin_condition, prop
- Observable proposition: A specifically requested fictional blood mark remains localized on its declared substrate or body region; a stained object does not introduce tissue disruption, an extra victim, or a perpetrator.
- Components: declared substrate; bounded mark distribution; body-region ownership if selected; preserved unrelated body continuity
- Relations: stain → lies on → declared substrate
- Confusions: red light or paint as blood; minor smear becomes gore; blood-stained knife as perpetrator identity; unrequested additional victim
- Existing IDs to review: bloodstain_observation_documentation, hvr_profile_gore_localized_tissue
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 현행 forensic 프로필은 척도·기록 절차가 추가되고 gore 후보는 조직/신체 훼손을 포함한다. 단순 smear의 동등 후보가 아니므로 별도 비노골적 trace 원자 trial이 필요하다. 생물학적 진위·원인·책임 추정은 제외한다.

## VEL-048 — 멍·찰과상·표면 오염의 소유

- Keywords: K147, K148, K150, K153
- Kind / priority: new_relation_trial / P1
- Owner: specified fictional skin region and independent dirt
- Slots: skin_condition, aftermath_trace
- Observable proposition: The specified skin region has bounded discoloration or a superficial mark while its larger anatomical continuity remains readable; grime and surface scratches are separately owned appearances.
- Components: named skin region; bounded discoloration or surface mark; anatomical continuity; independent dirt owner
- Relations: selected mark → lies on → specified skin region
- Confusions: makeup as proven injury; smeared dirt as an open wound; automatic severe tissue loss; appearance as clinical diagnosis
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 피부 표면 표현의 연구용 외관 정의만 작성한다. 피부색·화장과 반례를 짝지으며 병변 진단·부상 정도의 의학적 판정 데이터를 만들지 않는다.

## VEL-049 — 붕대 같은 천·치료·상징의 구분

- Keywords: K151, K213
- Kind / priority: context_guard / P0
- Owner: wrap textile, chosen covered region and source narrative
- Slots: garment_detail, wearable_accessory
- Observable proposition: A bandage-like wrap has visible textile edges, crossings and attachment on the declared region; medical treatment, memory symbolism and dress construction remain separate meanings.
- Components: wrap textile boundary; layer crossings; declared region attachment
- Relations: wrap layer → overlaps → previous textile layer
- Confusions: every wrap as proof of a wound; memory motif as true memory; bandage dress as injury; unrequested exposed wound
- Existing IDs to review: slot:garment_detail:opaque_cotton_gauze_wrap_layers, slot:garment_detail:crisscross_linen_bandage_wrapping
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 기존 wrap 원자 재사용. 치료/패션/상징 문맥은 서로 equivalent paraphrase로 등록하지 않는다.

## VEL-050 — 의복 손상과 신체 연속성·노출 보존

- Keywords: K152
- Kind / priority: new_relation_trial / P0
- Owner: selected damaged garment and underlying subject
- Slots: garment_detail, aftermath_trace
- Observable proposition: Damage belongs to the selected garment edge or panel; separated fragments retain garment identity and the subject's body continuity and requester-prescribed visible regions remain unchanged.
- Components: garment damage owner; fragment textile identity; body continuity; prescribed coverage/exposure preserved
- Relations: detached cloth fragments → derive from → declared garment panel
- Confusions: cloth fragments as flesh; new injury; automatic new body exposure; wear on a prop transferred to skin
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: K152의 worn/damaged는 owner가 선행해야 한다. K152는 S11 설명문의 비성적 피해 맥락에 있고, 의복 파편 사례는 참조 대화 6절의 별도 본문 보충 사례이다. 후자는 원본 JSON의 19 source ID에 대응 근거가 없어 새 ID나 나이를 발명하지 않으며 성적 variant의 씨앗으로 사용하지 않는다.

## VEL-051 — 일어나기·기기·버티기의 지지 관계

- Keywords: K158, K159, K160, K164
- Kind / priority: new_relation_trial / P0
- Owner: same actor limbs, torso and support surface
- Slots: body_pose, action, hand_pose, contact_point
- Observable proposition: The selected actor transfers support through readable palm or knee contact and a coherent torso-limb chain; a rising configuration remains distinct from static kneeling or crawling.
- Components: specified support limbs; readable contact points; torso-limb continuity; selected action state
- Relations: own palm or knee → supports → same actor on declared surface
- Confusions: floating hands; extra limbs; kneeling as proof of surrender; rising posture as sexual arousal
- Existing IDs to review: pv_profile_quadruped, pv_profile_half_kneel, pv_profile_seated_palm_brace
- Research sources: [R17](https://openstax.org/books/college-physics-2e/pages/9-3-stability)
- Adoption note: 기존 quadruped/half-kneel/seated brace는 서로 대체할 수 없다. support transition의 추가 관계를 new trial로 검토한다.

## VEL-052 — 눈물·소진·숨참과 맥락

- Keywords: K156, K157, K161, K162, K163, K166, K167, K168
- Kind / priority: authoring_guidance / P1
- Owner: declared actor response and current surroundings
- Slots: expression, intent_state, action
- Observable proposition: Visible tears, posture, and present response may serve the requested fatigue or pain narrative; the same facial movement does not certify physiological state, surrender, or sexual emotion.
- Components: present tear or posture cue; declared response context; owned action target
- Relations: 
- Confusions: parted lips as sexual emotion; fatigue as surrender; clinical diagnosis from posture; pain intensified to gratify sexual framing
- Existing IDs to review: ae_profile_held_tears_lips
- Research sources: [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf)
- Adoption note: 관찰 형태와 소진·고통·항복의 해석을 구별한다. 원문 설명문의 비성적 부상/생존 의미를 보존한다.

## VEL-053 — 패배 화면 텍스트와 사건의 구분

- Keywords: K165
- Kind / priority: context_guard / P2
- Owner: explicitly requested diegetic text surface
- Slots: prop, composition
- Observable proposition: If requested, a bounded display or text surface contains the specified label; the label's presence is verified separately from the actor's actual outcome.
- Components: declared text surface; requested text string; placement and legibility
- Relations: label → appears on → declared display
- Confusions: defeated pose creating unrequested text; label as proof of actual defeat; extra symbols added as evidence
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R01](https://arxiv.org/abs/2310.11513)
- Adoption note: 敗北는 original 화면 텍스트다. 기본 negative/runtime 장식으로 늘리지 않으며 글자 정확도와 사건 의미를 따로 평가한다.

## VEL-054 — 유리 밀착·반사·굴절의 같은 평면

- Keywords: K169, K173
- Kind / priority: new_relation_trial / P0
- Owner: declared body region and glass plane
- Slots: contact_point, reflection_logic, surface_material
- Observable proposition: The selected body region meets the declared glass plane at a readable boundary; reflection and transmission remain attached to that same plane and distinct from body geometry.
- Components: glass plane reference; specified contact boundary; same-plane reflection/transmission; body continuity
- Relations: declared body patch → contacts → glass plane
- Confusions: overlap as contact; reflection as a second trapped person; lens distortion as body injury; cold palette as physical temperature
- Existing IDs to review: rb_glass_reflection_transmission
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R04](https://visualgenome.org/api/v0/api_endpoint_reference)
- Adoption note: 접촉·광학 효과·밀폐 관계를 따로 채택한다. 유리면 근처 자세만으로 압력이나 강제 감금을 증명하지 않는다.

## VEL-055 — 밀폐처럼 보이는 공간과 실제 감금

- Keywords: K170, K171, K172, K174
- Kind / priority: context_guard / P1
- Owner: visible chamber boundaries, subject and declared exit
- Slots: location, space_condition, body_pose
- Observable proposition: A bounded chamber has readable wall, glass or exit boundaries around the subject; actual confinement, breathlessness and temporal suspension are separate authored or unobservable premises.
- Components: interior/exterior boundary; declared exit state if visible; subject spatial position
- Relations: subject → lies inside → declared chamber
- Confusions: aquarium look as actual drowning; closed-looking room as forced captivity; suspended pose as measured elapsed time
- Existing IDs to review: slot:location:hr_sealed_habitat_external_limit
- Research sources: [R11](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [R18](https://www.bfi.org.uk/sight-and-sound/features/alfred-hitchcock-my-own-methods)
- Adoption note: 기존 sealed-habitat는 hostile exterior와 internal anomaly라는 추가 조건이 있으므로 generic chamber에 자동 채택하지 않는다.

## VEL-056 — 안개 숲·가지·이빨 웃음의 형태

- Keywords: K175, K176, K177, K178
- Kind / priority: reuse_extend / P2
- Owner: declared forest surfaces and fictional mouth
- Slots: location, atmosphere, expression
- Observable proposition: Fog occupies scene depth among traceable branches; a separately selected fictional mouth reveals its own sharp teeth without turning the environment or smile into an attack event.
- Components: scene-depth fog; owned branch silhouette; selected mouth and teeth; separate figure identity
- Relations: fog → occupies → declared scene depth; teeth → belong to → selected fictional mouth
- Confusions: horror label as mandatory blood; image-plane blur as fog; sharp teeth as actual assault; branch becoming a limb
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R14](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)
- Adoption note: forest/environment와 mouth geometry를 분리한다. ordinary smile·sharp teeth·위협 intent를 같은 hard alias로 합치지 않는다.

## VEL-057 — 일반 사진 연출의 소재·광원·증거 층

- Keywords: K179, K180, K181, K182, K183, K184, K185, K186, K187, K188
- Kind / priority: reuse_extend / P1
- Owner: declared image plane, surfaces, lights and interactions
- Slots: medium, lighting, light_direction, color_grading, grain_profile, surface_material, contact_point
- Observable proposition: Directional lights illuminate separately named surfaces; wet pavement reflects its environment, grain belongs to the image plane, and required body/object contact retains its own geometric evidence.
- Components: named light receivers; bounded pavement reflection; image-plane grain; independent interaction support
- Relations: source light → illuminates → declared receiver; pavement → reflects → declared scene; grain → occupies → image plane
- Confusions: cinematic as violence; caution tape as proven crime; grain as airborne dust; blue moonlight and warm candles as one local color
- Existing IDs to review: highlight_rolloff_tone_response, rb_glass_reflection_transmission
- Research sources: [R13](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits), [R14](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [R19](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html)
- Adoption note: 일반 품질·매체·빛은 기존 사전을 재사용한다. 위험 테이프·피부 질감만으로 사건/선정성 수위를 분류하지 않는다.

## VEL-058 — 선정성 관련 부정문의 범위 보존

- Keywords: K189, K190, K191, K192, K193, K194, K195, K196, K197, K198, K199
- Kind / priority: negative_firewall_plan / P0
- Owner: active requester spans and selected exclusions
- Slots: expression, garment_detail, body_pose
- Observable proposition: Negative source expressions retain their exclusion scope; a term appearing in a negative list cannot become positive candidate text, a new requirement, or an inferred invitation.
- Components: source polarity; exact active span; excluded meaning; positive remainder
- Relations: 
- Confusions: nudity in negative list used as a positive; rather-than scope inverted; global default covering inferred from one historical negative
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R02](https://arxiv.org/abs/2501.09425), [R03](https://arxiv.org/abs/2610.03084)
- Adoption note: 연구표와 회귀 fixture에만 negative 원문을 둔다. 현재 요청의 source-grounded exclusions와 explicit meaning을 보존하며 역사적 배제를 모든 미래 요청의 기본값으로 복제하지 않는다.

## VEL-059 — 잔혹성 배제와 해부학 오류 방지의 분리

- Keywords: K200, K201, K202, K203, K204, K205, K206, K207, K208
- Kind / priority: negative_firewall_plan / P0
- Owner: active exclusion scope and photographic defect controls
- Slots: action, skin_condition, aftermath_trace
- Observable proposition: No-blood or no-gore spans remain semantic exclusions when requester-grounded, while broken-wrist or dislocated-shoulder items in a defect list remain geometry repair constraints rather than desired injuries.
- Components: source polarity; semantic exclusion owner; defect list provenance; unchanged positive action
- Relations: 
- Confusions: no gore cancels all action; blood negation produces blood; defect term becomes injury evidence; Chinese negation stripped
- Existing IDs to review: no equivalent existing ID established
- Research sources: [R02](https://arxiv.org/abs/2501.09425), [R03](https://arxiv.org/abs/2610.03084)
- Adoption note: 不要血腥/不要殺戮場面를 부정 의미 그대로 해석한다. 사건 제외와 좁은 photographic-defect vocabulary를 동일 칸에 넣지 않는다.

## VEL-060 — 가림·얼굴 동일성·색·연령의 독립 보존

- Keywords: K209, K210, K211, K212, K213, K214, K215, K216, K217
- Kind / priority: context_guard / P0
- Owner: declared garment coverage, face identity, color carrier and source age
- Slots: garment_detail, subject_framing, ambient_particle, light_type
- Observable proposition: Requester-prescribed coverage and facial identity remain preserved; red code particles and a crimson machine light retain their own carriers, while adult status remains a subject condition rather than an appeal score.
- Components: coverage boundary; declared face invariants; red particle or machine-light ownership; source age provenance
- Relations: crimson light → comes from → declared machine; code particles → remain distinct from → stains on a substrate
- Confusions: red as blood; face lock as sensuality; adult as evidence of consent; age inferred from appearance; covering altered for a retrieval candidate
- Existing IDs to review: slot:light_type:status_led_glow, slot:ambient_particle:egr_localized_suspended_particles
- Research sources: [R04](https://visualgenome.org/api/v0/api_endpoint_reference), [R05](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf)
- Adoption note: K209/210 가림은 해당 원문 조건으로만 유지한다. FACE LOCKED는 기존 identity/control 경로를 사용하며 후보팩에 새 외모/연령 라우터를 만들지 않는다.


"""Authored proposals with local owners. IDs below are research IDs, never CIDs/RIDs."""
CARDS=[]
def visual(cid,title,ko,en,owners,edges,confusion,limit,slots,sources,existing='',adoption='refine',priority='P1',mode='still'):
    CARDS.append(dict(card_id=cid,title_ko=title,mode=mode,proposal_ko=ko,proposal_en=en,
        owners=dict(x.split('=',1) for x in owners.split(';')),
        relations=[dict(zip(('from','predicate','to'),x.split('>'))) for x in edges.split(';')],
        confusion_boundary_ko=confusion,claim_limit_ko=limit,proposed_slots=slots.split(','),
        source_refs=sources.split(','),existing_card_refs=existing.split(',') if existing else [],
        adoption=adoption,priority=priority,canonical_status='optional_authored_realization; source supports motif or definition, not this complete staging',
        activation='post_core_explicit_selection_or_exact_request_only; broad_label_is_advisory',
        evidence_policy={'unobservable':'UNOBSERVABLE_NOT_PASS','whole_case':'partial_is_fail'},native_approval=False))
def context(cid,title,meaning,confusion,limit,sources,existing='',adoption='context',mode='context'):
    CARDS.append(dict(card_id=cid,title_ko=title,mode=mode,meaning_ko=meaning,
        confusion_boundary_ko=confusion,claim_limit_ko=limit,source_refs=sources.split(','),
        existing_card_refs=existing.split(',') if existing else [],adoption=adoption,priority='P0',
        owners={},relations=[],proposed_slots=[],candidate_eligible=False,
        activation='interpretive_context_only; never_hard_visual_from_label',native_approval=False))

visual('R01','같은 바닥에서 비교되는 규모',
 '작은 성인 조사자와 훨씬 큰 석문이 같은 평탄한 바닥에 닿고, 조사자의 전신과 문 상단이 함께 보인다.',
 'A small adult investigator and a much taller stone doorway meet the same level floor; the entire investigator and the doorway’s upper edge remain visible together.',
 'observer=adult investigator;portal=large stone doorway;floor=shared level contact plane',
 'observer>stands_on>floor;portal>rises_from>floor',
 '광각 근접 소품·원근차를 실제 규모 차로 판정','절대 치수·우주적 중요성·공포 감정은 별개다.',
 'scale_relation,composition','S01,S43','C001,C178','reuse','P0')
visual('R02','인간과 다른 곳을 향하는 거대 존재',
 '거대한 생물의 머리와 눈 방향은 수면의 먹이 무리를 향하고, 작은 배는 옆의 같은 수면에 떠 있다.',
 'The visible head and eye of a giant organism are directed toward a shoal at the water surface; a small boat floats beside it on the same continuous surface.',
 'organism=large organism;eye=visible eye;shoal=surface shoal;boat=small vessel;water=shared water surface',
 'eye>part_of>organism;eye>directed_toward>shoal;boat>floats_on>water;organism>intersects>water',
 '눈 방향 불명·시선만으로 마음 읽기','가시 방향은 무관심·포식 의도·인간을 못 봄의 증명이 아니다. 이 먹이 장면은 창작이다.',
 'gaze_target,scale_relation,situation_context','S01,S06','C003','refine','P0')
visual('R03','유적과 덮인 지층의 경계',
 '절개된 지층 아래에서 조각 벽의 윗면이 드러나고, 여러 수평 퇴적층이 그 위를 연속해서 덮는다.',
 'The upper edge of a carved wall is exposed beneath a cut bank; several continuous horizontal sediment layers lie over the wall, with their contact boundary visible.',
 'wall=carved wall;bank=cut sediment bank;layers=visible horizontal layers',
 'layers>part_of>bank;layers>overlie>wall',
 '표면 흙먼지·장식 줄무늬를 층서로 판정','덮임 관계만 보인다. 수억 년·인류 이전·퇴적 순서의 과학 판정은 별도다.',
 'aftermath_trace,location','S04,S20','C061','refine','P0','proxy')
visual('R04','우물 주변 황폐 경계',
 '석조 우물 주변의 회색 가루 지대가 잎 없는 나무를 둘러싸고, 그 바깥에 푸른 초목이 남아 있어 경계가 읽힌다.',
 'A patch of grey dust surrounds a stone well and leafless trees; green vegetation remains outside the patch, making the edge between the two areas readable.',
 'well=stone well;patch=grey dusty ground;trees=leafless trees;growth=green outer vegetation',
 'patch>surrounds>well;trees>rooted_in>patch;growth>borders>patch',
 '화재·가뭄·계절 변화와 외계 오염을 혼동','외계 원인·독성·냄새·생물 사망은 배치로 확정되지 않는다.',
 'aftermath_trace,location,space_condition','S05','C086','refine','P0','proxy')
visual('R05','관측 장치와 관측 범위',
 '투명 관측판 안쪽에만 반투명 생물 윤곽이 보이고, 판 밖으로 이어지는 같은 벽과 탁자는 정상적으로 정렬된다.',
 'Translucent organism contours appear only within a transparent observation panel; the same wall and tabletop align continuously across the panel’s boundary.',
 'panel=transparent observation panel;contours=organism-like contours;wall=shared background wall;table=shared tabletop',
 'contours>visible_within>panel;wall>continues_across>panel;table>continues_across>panel',
 '판에 붙인 스티커·모니터 영상·반사와 투과를 혼동','추가 감각·생물 실재·광학 작동은 창작 설정이다.',
 'apparatus_pov,reality_anchor,object_structure','S44','C105','refine','P1','proxy')
visual('R06','서로 다른 매체의 대응 형상',
 '점토 부조와 종이 스케치가 탁자 위에 따로 놓이고, 갈라진 머리 윤곽과 비대칭 세 돌기가 두 매체에서 대응한다.',
 'A clay relief and a separate paper sketch lie on a table; a split head outline and three asymmetrically placed projections correspond across both representations.',
 'relief=clay representation;sketch=paper representation;table=shared support',
 'relief>rests_on>table;sketch>rests_on>table;sketch>corresponds_in_landmarks_to>relief',
 '두 물건을 하나로 융합·대충 닮은 장식','동일 꿈·전파·기록의 독립성·진위를 입증하지 않는다. 세 돌기는 저술한 비교 표식이다.',
 'prop_placement,narrative_clue,object_structure','S03','C116','new','P0','proxy')
visual('R07','발견된 원고와 보관 흔적',
 '펼쳐진 손글씨 원고 한쪽 아래가 열린 보관 상자 안에 남아 있고, 종이가 상자의 앞 테두리를 넘어 탁자로 이어진다.',
 'Part of an unfolded handwritten manuscript remains inside an open storage box; the sheet crosses its front rim and extends onto the table.',
 'sheet=handwritten manuscript;box=open storage box;table=outer support',
 'sheet>partly_inside>box;sheet>crosses_rim_of>box;sheet>rests_on>table',
 '일반 편지를 금서·죽은 저자의 기록으로 판정','발견 경위·저자의 실종·금지 지식은 문맥이다.',
 'prop_placement,visible_text','S03,S15','C135','refine','P1','proxy')
visual('R08','회화와 사진의 국소 대응',
 '벽의 회화와 탁자의 사진이 같은 웅크린 형상과 갈라진 돌기둥을 보여주며, 사진의 종이 가장자리와 회화의 액자가 따로 보인다.',
 'A framed painting on a wall and a paper photograph on a table show the same crouched figure beside a split stone pillar; the frame and the photograph’s paper edges remain distinct.',
 'painting=framed image;photograph=paper photograph;wall=painting support;table=photo support',
 'painting>mounted_on>wall;photograph>rests_on>table;photograph>shares_landmarks_with>painting',
 '사진 속 생물을 방 안 실물로 합침','사진은 위조 여부·실재·괴물 종을 입증하지 않는다. 정확한 포즈는 창작 비교 표식이다.',
 'prop_placement,narrative_clue','S12','C116','new','P0','proxy')
visual('R09','같은 사건 식별자의 기록 불일치',
 '같은 짧은 사건 번호가 있는 두 장의 기록에 서로 다른 날짜가 읽히고, 두 종이의 테두리가 분리된다.',
 'Two separate records carry the same short event identifier but different legible dates; each sheet has its own visible border.',
 'record_a=first paper record;record_b=second paper record;id_a=first identifier;id_b=second identifier;date_a=first date;date_b=different second date',
 'id_a>printed_on>record_a;id_b>printed_on>record_b;date_a>printed_on>record_a;date_b>printed_on>record_b;id_a>matches>id_b',
 '읽히지 않는 글자를 정확한 모순으로 판정','시간 여행·누락 기억·기록의 거짓말을 증명하지 않는다. 텍스트가 작으면 미판정이다.',
 'visible_text,narrative_clue,object_structure','S08','C174','refine','P0','proxy')
visual('R10','필적 견본과 낡은 기록의 비교',
 '작은 카드와 낡은 문서에 같은 짧은 서명이 있고, 동일한 꺾인 획과 긴 아래꼬리가 읽힐 크기로 나란히 놓인다.',
 'A small reference card and an aged document lie side by side, each bearing the same short signature with a matching angular stroke and long descender, large enough to compare.',
 'card=reference card;document=aged document;signature_a=card signature;signature_b=document signature',
 'signature_a>ink_on>card;signature_b>ink_on>document;signature_a>matches_stroke_landmarks_of>signature_b',
 '유사 글꼴을 동일인 필적으로 판정','저자 동일성·기억·연대·정신 교환은 별도 검증이다.',
 'visible_text,narrative_clue','S08','C118','new','P1','proxy')
visual('R11','두 잠자리와 독립된 꿈 스케치',
 '떨어진 두 침대 옆 탁자에 각각 스케치가 놓이며, 두 종이에 같은 세 갈래 탑 윤곽이 보인다.',
 'Two separated beds each have a bedside table holding a sketch; both sheets show the same three-pronged tower outline, with each bed–table–sheet grouping distinct.',
 'bed_a=first bed;bed_b=second bed;table_a=first bedside table;table_b=second bedside table;sketch_a=first sketch;sketch_b=second sketch',
 'table_a>beside>bed_a;table_b>beside>bed_b;sketch_a>rests_on>table_a;sketch_b>rests_on>table_b;sketch_a>shares_outline_with>sketch_b',
 '한 그림의 복사본을 독립적인 꿈으로 판정','수면·동일 꿈·접촉·전염은 이미지 밖 문맥이다.',
 'prop_placement,narrative_clue,proxemics','S03','C118','new','P2','proxy')
visual('R12','항구의 생활 동선과 폐쇄된 바다 경계',
 '좁은 선착장이 쇠락한 창고 사이 골목 끝의 수면으로 이어지고, 문이 닫힌 건물과 계류된 작은 배가 함께 보인다.',
 'A narrow quay continues from an alley between weathered warehouses to the water; closed building doors and a moored small boat remain visible in the same view.',
 'quay=narrow quay;alley=warehouse alley;water=harbor water;boat=moored boat;warehouse=weathered warehouse',
 'quay>continues_from>alley;quay>borders>water;boat>moored_beside>quay;warehouse>bounds>alley',
 '빈 항구=사악한 공동체·가난=퇴화','지명·경제 상태·주민의 도덕·혈통은 외형에서 판정하지 않는다.',
 'location,space_condition','S07,S21','C133','refine','P2','proxy')
visual('R13','황금빛 꿈의 도시',
 '높은 난간 너머로 붉은 지붕과 대리석 아치 다리가 햇빛 아래 보이며, 가까운 난간과 먼 도시가 분리된다.',
 'Beyond a high balustrade, red roofs and veined marble arched bridges catch warm sunlight; the near railing remains distinct from the distant city.',
 'railing=near balustrade;city=distant roofed city;bridges=marble arched bridges',
 'railing>foreground_of>city;bridges>span_gaps_within>city',
 '꿈=안개 낀 검은 폐허로 고정','꿈의 실재·향기·잃은 기억은 보이지 않는다.',
 'location,composition,surface_material','S11','C134','new','P2')
visual('R14','카르코사 도상의 선택',
 '호수 지평선 위에 두 밝은 원반이 따로 있고, 그 위의 밝은 하늘에는 작고 검은 별꼴 표식이 놓인다.',
 'Two separate bright discs sit above a lake horizon; small dark star-shaped marks appear against the brighter sky above them.',
 'lake=water body;horizon=lake horizon;disc_a=first bright disc;disc_b=second bright disc;marks=dark star-shaped sky marks;sky=bright sky',
 'horizon>bounds>lake;disc_a>above>horizon;disc_b>above>horizon;marks>against>sky',
 '검은 별=블랙홀·천문학 사실','체임버스의 시적 모티프를 위한 선택 구성이다. 정확한 지형·천체 물리는 주장하지 않는다.',
 'world,location,reality_anchor','S27','C151','refine','P2','versioned')
visual('R15','사람과 맞지 않는 낮은 통로',
 '성인 조사자가 엎드린 자세로 낮은 돌 통로에 들어가며, 등 위 천장과 손 앞 바닥 사이 간격이 함께 보인다.',
 'An adult investigator lies prone at a low stone passage entrance; the ceiling above their back and the floor under their extended hands remain visible together.',
 'person=adult investigator;passage=low stone passage;ceiling=upper passage boundary;floor=lower passage boundary',
 'person>partly_inside>passage;ceiling>above_back_of>person;person>lies_on>floor',
 '단순 지하실을 비인간 건설자로 확정','몸 비례 차이는 시각 제안이다. 건설자 종족·도시 연대는 판정하지 않는다.',
 'scale_relation,location,body_pose','S20','C077','new','P1')
visual('R16','얼음 아래 유적의 노출',
 '갈라진 얼음벽의 투명한 층 안에 조각 벽 일부가 들어 있고, 벽의 아래쪽은 얼음 틈 바닥으로 드러난다.',
 'Part of a carved wall lies within a translucent layer of fractured ice; its lower section emerges onto the floor of the ice cleft, with the ice–stone boundary exposed.',
 'wall=carved stone wall;ice=fractured translucent ice;cleft=ice opening',
 'wall>partly_embedded_in>ice;wall>emerges_into>cleft',
 '바위 옆 눈더미를 봉인된 고대 유적으로 판정','빙하 연대·봉인 기간·소생은 별도다.',
 'location,surface_material,object_structure','S04','C061','new','P1','proxy')
visual('R17','수몰 건축의 매질',
 '잠긴 석주 위로 연속 수면이 보이고, 석주 앞을 지나는 부유 입자와 기포가 물속 깊이 관계를 만든다.',
 'Submerged stone columns stand below a continuous visible water surface; suspended particles and bubbles pass in front of the columns, establishing the intervening water medium.',
 'columns=submerged stone columns;surface=water surface;particles=waterborne particles;bubbles=water bubbles',
 'columns>below>surface;particles>in_front_of>columns;bubbles>in_front_of>columns',
 '안개·건조 폐허의 청록 보정을 수중으로 판정','침몰 원인·깊이·르뤼에 지명은 입증하지 않는다.',
 'location,space_condition,lighting','S03','C076','reuse','P0')
visual('R18','단일 거석과 조립된 거석의 구분',
 '이 구성에서는 큰 석문 양옆에 개별 돌 블록의 접합선이 드러나고, 작은 측정 막대가 문턱에 놓인다.',
 'This realization shows individual block seams on both sides of a large stone doorway, with a small measuring rod lying at the threshold.',
 'portal=block-built portal;seams=visible block joints;rod=measuring rod;threshold=doorway base',
 'seams>divide_blocks_of>portal;rod>rests_on>threshold',
 'cyclopean=반드시 이음새 없는 단일 석체','거석 축조의 선택형이다. 돌의 절대 크기·문명·시대를 원문에서 일반화하지 않는다.',
 'object_structure,scale_relation,location','S03,S04','C164','reuse','P0')
visual('R19','네 접속점이 모두 보이는 계단 루프',
 '네 구간의 계단과 네 모퉁이 연결부가 하나의 닫힌 고리로 보이고, 일관된 국소 오름 방향이 시작점으로 돌아온다.',
 'Four stair flights and all four corner junctions form one visible closed loop; their locally consistent ascending direction returns to the starting junction.',
 'flight_a=first flight;flight_b=second flight;flight_c=third flight;flight_d=fourth flight',
 'flight_a>ascending_join_to>flight_b;flight_b>ascending_join_to>flight_c;flight_c>ascending_join_to>flight_d;flight_d>ascending_join_to>flight_a',
 '접속부 가림·일반 나선계단·기울어진 카메라','허구의 불가능한 도형이다. 비유클리드 기하의 수학적 정의와 다르다.',
 'surreal_physics_detail,object_structure,space_condition','S03,S33','C162','reuse','P0')
visual('R20','창문 안쪽의 다른 외부',
 '방 안의 창틀과 유리 가장자리가 보이고, 창 내부에는 별 없는 검은 영역이 있지만 창 옆의 열린 문으로는 밝은 도시 지붕이 보인다.',
 'A room has a clearly framed window showing a starless dark field; beside it, an open doorway reveals bright city roofs, with both architectural boundaries visible.',
 'window=framed window;dark_field=window view;door=open doorway;roofs=bright exterior roofs;room=shared interior',
 'dark_field>framed_by>window;roofs>seen_through>door;window>part_of>room;door>part_of>room',
 '커튼·불투명 유리·노출차를 차원으로 단정','외부 실재·차원 이동·음악의 보호 효능은 문맥이다. 문과 창 비교는 저술한 실현이다.',
 'reality_anchor,location,space_condition','S13','C080','new','P1','proxy')
visual('R21','벽 경계를 넘는 연속 형상',
 '생물의 한 부속지가 온전한 벽의 평평한 면에서 끊김 없이 돌출하고, 벽의 줄눈은 접점 주변에서 계속 보인다.',
 'One organism appendage projects continuously from an intact flat wall surface; the wall’s masonry joints remain visible around the junction.',
 'appendage=continuous protruding appendage;wall=intact masonry wall;joints=wall joints',
 'appendage>emerges_from_surface_of>wall;joints>continue_around>appendage',
 '벽 구멍·부착 조각·겹침을 차원 통과로 판정','벽 통과와 고차원성의 작동 원인은 설정이다. 가시 접점만 판정한다.',
 'anatomical_connection,surreal_physics_detail','S10','C068','new','P1','proxy')
visual('R22','크툴루 우상의 소유자별 외형',
 '받침 위에 앉은 작은 조각상은 촉수성 머리와 비늘 몸을 가지며, 길고 좁은 날개가 등에서 좌우로 이어진다.',
 'A small seated statuette on a pedestal has a tentacled head and scaly body; long narrow wings extend from the back on both sides, with their roots visible.',
 'idol=small seated statuette;head=tentacled idol head;body=scaly idol torso;wings=long narrow idol wings;pedestal=statue support',
 'head>part_of>idol;body>part_of>idol;wings>attached_to_back_of>body;idol>rests_on>pedestal',
 '부조의 rudimentary wings를 이 우상에 전사','원전의 우상 묘사 대상을 선택한다. 본체의 실제 해부학·색·크기를 확정하지 않는다.',
 'subject,species_marker,prop,anatomical_connection','S03','C119','refine','P0','versioned')
visual('R23','부조의 얕은 돌출',
 '평평한 점토판에서 촉수 머리와 비늘 몸 형상이 얕게 솟고, 몸 뒤 작은 날개 자국은 판 표면에 붙어 있다.',
 'A tentacled head and scaly body rise in shallow relief from a flat clay tablet; rudimentary wing forms behind the body remain continuous with the tablet surface.',
 'tablet=flat clay tablet;figure=shallow raised figure;wings=rudimentary relief wings',
 'figure>raised_from>tablet;wings>part_of>figure;wings>continuous_with_surface_of>tablet',
 '우상·실물·평면 그림을 같은 대상으로 합침','원전 부조의 범위다. 물질색·정확한 날개 수·본체 비례는 별도 선택이다.',
 'prop,object_structure,surface_material','S03','C119','new','P0','versioned')
visual('R24','엘더 싱의 오중 몸통',
 '자유롭게 선 표본의 통 모양 몸통에 다섯 세로 능선이 둘레를 이루고, 위쪽의 오각 별 모양 기관과 목 접점이 보인다.',
 'A freestanding specimen has a barrel-like torso with five longitudinal ridges around its circumference and a five-pointed upper organ joined by a visible neck.',
 'specimen=freestanding organism;torso=five-ridged barrel torso;head=five-pointed upper organ;neck=visible neck',
 'torso>part_of>specimen;head>connected_via>neck;neck>joins>torso',
 '불가사리 얼굴만으로 전체 오중 해부학 PASS','둘레 전체 능선이 가려지면 총 다섯 개는 미판정이다. 모든 말단의 정본 재현을 주장하지 않는다.',
 'body_form,species_marker,anatomical_connection','S04','C120,C170','refine','P0','versioned')
visual('R25','분기 팔의 국소 연결',
 '엘더 싱 몸통 능선의 한 줄기 팔이 다섯 가는 가지로 갈라지며, 몸통 부착점과 그 분기점이 같은 근접 시야에 보인다.',
 'One stalk attached to a ridge of an Elder Thing torso divides into five slender branches; the torso attachment and that first branching junction remain visible in the same close view.',
 'torso=local torso ridge;stalk=single proximal stalk;branches=five first-order branches',
 'stalk>attached_to>torso;branches>branch_from>stalk',
 '떨어진 촉수·뒤의 가지를 같은 접점으로 합침','국소 1차 분기만 선택했다. 원전의 전신 5×5×5 기관 수 검증이 아니다.',
 'anatomical_connection,body_region','S04','C120','new','P1','versioned')
visual('R26','쇼고스 덩어리와 표면의 눈',
 '젤 같은 한 덩어리가 바닥에 퍼지고, 서로 다른 크기의 눈 같은 기관이 그 연속 표면에 박혀 있으며 돌출부의 뿌리가 덩어리로 이어진다.',
 'One gelatinous mass spreads across the floor; differently sized eye-like organs sit within its continuous surface, and projecting lobes remain rooted in the same mass.',
 'mass=continuous gelatinous body;eyes=surface eye-like organs;lobes=projecting lobes;floor=support',
 'eyes>embedded_in>mass;lobes>continuous_with>mass;mass>spreads_on>floor',
 '여러 슬라임 생물·무늬·공중 눈','임시 생성·지능·복종·재생은 시퀀스나 설정이다.',
 'body_form,texture,anatomical_connection','S04','C121','refine','P0','versioned')
visual('R27','미고의 서로 다른 부위',
 '갑각 유사 몸통에 여러 관절 다리와 한 쌍의 등 막날개가 붙고, 머리 위치의 타원체에는 짧은 안테나가 조밀하게 솟는다.',
 'A crustacean-like torso bears multiple jointed limbs and one pair of dorsal membranous wings; a convoluted ellipsoid at the head position carries many short antennae.',
 'torso=crustacean-like torso;limbs=jointed limbs;wings=pair of dorsal membranous wings;head=convoluted ellipsoid;antennae=short projections',
 'limbs>attached_to>torso;wings>attached_to_back_of>torso;head>joined_to>torso;antennae>grow_from>head',
 '버섯갓·인간 머리·등지느러미와 날개 혼합','이 작품의 선택 외형이다. fungoid라는 명칭이 버섯 자실체를 요구하지 않는다.',
 'species_marker,anatomical_connection','S06','C122','reuse','P0','versioned')
visual('R28','딥 원의 허구적 이종 표지',
 '허구 생물의 회색빛 몸에 비늘 영역이 있고, 목 양쪽 아가미 같은 틈과 손가락 사이 막이 각 부위에 따로 보인다.',
 'A fictional greyish organism has scaled body areas, gill-like slits at both sides of the neck, and membranes between the fingers, with each feature attached to its own body region.',
 'organism=fictional nonhuman organism;scales=body scale areas;gills=neck slits;hands=hands;webs=interdigital membranes',
 'scales>on>organism;gills>on_neck_of>organism;hands>part_of>organism;webs>between_fingers_of>hands',
 '현실 인종 얼굴·눈 모양을 종족 판정에 사용','허구 형태만 다룬다. 인간의 혈통·인격·유전 진단은 불가하다.',
 'species_marker,body_region','S07','C123','refine','P0','versioned')
visual('R29','이스 종족 점유 몸의 말단 기능 분리',
 '원뿔 몸 꼭대기의 네 자루 중 두 개는 집게, 하나는 깔때기 묶음, 하나는 둥근 기관으로 끝나며 네 뿌리가 따로 보인다.',
 'Four stalks rise from the apex of a conical body: two end in pincers, one in a cluster of funnel-like forms, and one in a rounded organ; all four stalk roots remain distinguishable.',
 'body=conical body;claw_a=first pincer stalk;claw_b=second pincer stalk;funnels=funnel-ended stalk;head=rounded-organ stalk',
 'claw_a>rooted_in_apex_of>body;claw_b>rooted_in_apex_of>body;funnels>rooted_in_apex_of>body;head>rooted_in_apex_of>body',
 '네 개 머리·네 집게·인간형으로 치환','정신 교환·종족의 모든 시대 형태는 주장하지 않는다.',
 'body_form,species_marker,anatomical_connection','S08','C124','refine','P0','versioned')
visual('R30','밝게 드러난 무안면 머리',
 '뿔 두 개가 달린 매끈한 머리 앞면 전체가 측면광 아래 드러나고, 목과 날개 뿌리가 같은 몸으로 이어진다.',
 'The entire smooth front of a two-horned head is visible under side lighting; the neck and membranous wing roots connect to the same body.',
 'head=smooth two-horned head;neck=neck;body=single body;wings=membranous wings',
 'head>joined_via>neck;neck>joins>body;wings>attached_to_back_of>body',
 '가면·등 돌린 얼굴·검게 가린 얼굴','무안면 국소 외형만 검증한다. 정확한 전신 나이트건트 재현이나 납치 기능은 별도다.',
 'species_marker,body_region,lighting','S11','C125,C171','refine','P0','versioned')
visual('R31','니알라토텝의 시연자 장면',
 '한 성인 시연자가 유리·금속 장치 옆에 서 있고, 떨어진 관중들이 시연자와 장치를 향한다.',
 'One adult demonstrator stands beside an apparatus made of glass and metal; a separate audience faces the demonstrator and the apparatus.',
 'demonstrator=adult presenter;device=glass and metal apparatus;audience=separate audience',
 'demonstrator>beside>device;audience>faces>demonstrator;audience>faces>device',
 '피부색·파라오 복장으로 모든 화신 동일화','이 단편의 시연 관계를 고른다. 모든 화신·신격 여부·군중의 실제 감정은 확정하지 않는다.',
 'participant_role,prop_placement,relational_action','S19','C126','reuse','P1','versioned')
visual('R32','소환 분말의 표면 윤곽',
 '분말이 공기 중의 굽은 몸 윤곽 일부에 붙어 있고, 뒤의 언덕은 윤곽 바깥에서 연속해서 보인다.',
 'A coating of powder marks part of a curved body contour in the air; the hillside behind it remains continuous outside that contour.',
 'powder=visible powder coating;contour=partially outlined form;hill=background hillside',
 'powder>coats>contour;hill>behind>contour',
 '먼지 구름·연기·전체 불가시 생물의 완전 관찰','일부 윤곽만 관찰한다. 전체 기관 수·원래의 불가시성·의식의 효능은 불확정이다.',
 'texture,subject_framing,reality_anchor','S09','','new','P2','versioned')
visual('R33','균사체와 버섯갓을 분리한 표면',
 '가는 실들이 갈라져 바닥 틈을 건너 한 망을 이루고, 몇 가닥은 물체 밑면과 직접 이어진다.',
 'Fine branching filaments form a connected network across floor cracks; several strands join directly to the underside of an object.',
 'filaments=branching filament network;floor=floor with cracks;object=local object',
 'filaments>cross_cracks_in>floor;filaments>join_underside_of>object',
 '뿌리·거미줄·버섯갓과 무조건 동일시','균류 동정·감염·먹이 관계·성장 속도는 입증하지 않는다.',
 'texture,anatomical_connection','S35','C159','reuse','P0')
visual('R34','비늘과 주름의 분리',
 '생물의 한 부위에는 겹치는 판형 비늘이, 인접한 부위에는 연속 피부의 깊은 주름이 있고 둘 사이 경계가 보인다.',
 'One body region has overlapping plate-like scales; an adjacent region has deep folds in continuous skin, with their boundary visible.',
 'body=organism body;scales=overlapping plates;folds=continuous skin folds;boundary=transition boundary',
 'scales>cover_region_of>body;folds>cover_adjacent_region_of>body;boundary>separates>scales;boundary>separates>folds',
 'rugose와 squamous를 동의어로 처리','판형과 주름만 구분한다. 부패·나이·종은 함의하지 않는다.',
 'texture,surface_material,body_region','S36,S37','C011,C012,C158','refine','P0')
visual('R35','촉수의 뿌리·중간·자유 말단',
 '흡반 없는 유연한 부속지 한 가닥이 몸에서 시작해 빈 공간으로 휘고, 몸 접점부터 자유 말단까지 가리지 않고 보인다.',
 'One flexible suckerless appendage begins at the body and curves into open space; its body junction, continuous middle, and free tip remain unobscured.',
 'body=organism torso;appendage=one flexible suckerless appendage;tip=free distal tip',
 'appendage>attached_to>body;tip>distal_part_of>appendage',
 '떠 있는 관·뿌리 가림·촉수=붙잡기·성적 접촉','흡반 없음과 자유 말단은 이번 선택 조건이다. tentacular의 사전 뜻 전체가 아니다.',
 'anatomical_connection,body_form','S34','C156,C180','refine','P0')
visual('R36','젤 표면과 내부 가시성',
 '반투명 덩어리 앞쪽 표면의 하이라이트와 그 뒤의 흐릿한 내부 입자가 따로 보이며, 바닥에 닿은 외곽이 눌려 퍼진다.',
 'A translucent mass shows a near-surface highlight separate from blurred internal particles; its outline flattens and spreads where it meets the floor.',
 'mass=translucent mass;highlight=near surface highlight;particles=internal particles;floor=contact plane',
 'highlight>on_surface_of>mass;particles>inside>mass;mass>flattens_against>floor',
 '유리 조각·발광 구체·반사 입자를 내부 구조로 판정','점성 수치·살아 있음·원형질 구성은 정지 영상으로 입증되지 않는다.',
 'surface_material,texture,contact_point','S04','C013,C024','refine','P1')
visual('R37','한 몸 안의 변형 경계',
 '성인 허구 인물의 한 팔에 정상 피부와 비늘 영역이 연속해서 이어지고, 팔꿈치와 손은 같은 팔에 붙어 있다.',
 'One arm of a fictional adult has ordinary skin transitioning continuously into a scaled region; the elbow and hand belong to that same connected arm.',
 'adult=fictional adult;arm=single arm;skin=ordinary skin region;scales=scaled region;hand=connected hand',
 'arm>part_of>adult;skin>covers_region_of>arm;scales>covers_adjacent_region_of>arm;hand>attached_to>arm',
 '장갑·의상·옆 사람 팔·유전 진단','현재의 혼합 형태만 보인다. 과거 변신·혈통·퇴화·자발성은 불확정이다.',
 'transformation_stage,anatomical_connection,body_region','S07','C028','refine','P0','proxy')
visual('R38','함께 있는 생물의 돌봄 접점',
 '성인이 작은 비인간 생물이 놓인 그릇을 두 손으로 받치고, 생물의 몸과 그릇 사이 지지 접점이 보인다.',
 'An adult supports a bowl with both hands while a small nonhuman organism rests inside it; hand–bowl and organism–bowl support contacts are visible.',
 'adult=adult carer;hands=both hands;bowl=support vessel;organism=small nonhuman organism',
 'hands>part_of>adult;hands>support>bowl;organism>rests_inside>bowl',
 '관계가 가까우면 기생·강압 또는 상호 공생으로 확정','돌봄으로 읽을 수 있는 배치다. 상호 이익·동의·종족 관계는 설정으로 보존한다.',
 'relational_action,contact_point,situation_context','S32','','new','P2','proxy')
visual('R39','뇌 원통의 원전 금속 외관',
 '닫힌 금속 원통 앞의 소켓 세 개가 삼각 배열을 이루고, 두 소켓에서 나온 선이 각각 별도 장치 단자까지 이어진다.',
 'A closed metal cylinder has three front sockets in a triangular arrangement; cables from two sockets run continuously to terminals on two separate devices, with all four cable endpoints visible.',
 'cylinder=closed metal cylinder;sockets=three front sockets;cable_a=first cable;cable_b=second cable;device_a=first external device;device_b=second external device',
 'sockets>mounted_on>cylinder;cable_a>connects_socket_on>cylinder;cable_a>terminates_on>device_a;cable_b>connects_socket_on>cylinder;cable_b>terminates_on>device_b',
 '반사광을 내부 뇌로 판정·유리병으로 자동 치환','원전의 외부 장치 배치다. 뇌·의식·장치 기능·전송은 외형에서 보이지 않는다.',
 'prop,object_structure,contact_point','S06','C104,C169','refine','P0','versioned')
visual('R40','투명 뇌 용기의 창작 변형',
 '투명 용기 안의 액체에 뇌 같은 물체가 떠 있고, 용기 벽과 내부 물체 사이 간격 및 벽을 통과하는 두 단자가 보인다.',
 'A brain-like object sits in liquid inside a transparent vessel; a visible gap separates it from the vessel wall, and two terminals pass through the wall.',
 'vessel=transparent vessel;object=brain-like internal object;liquid=inner liquid;terminals=two wall feedthroughs',
 'object>inside>vessel;object>immersed_in>liquid;terminals>pass_through_wall_of>vessel',
 '금속 원통 정본·살아 있는 의식으로 판정','원전 정본이 아닌 creative_variant다. 인간 뇌 동정·생존·동의는 미입증이다.',
 'prop,object_structure,surface_material','S06','C103','refine','P1','creative_variant')
visual('R41','기록 속 해부와 현재 표본의 분리',
 '덮개 아래 놓인 허구 성인 표본의 한 팔만 노출되고, 옆의 해부 도식은 종이 테두리 안에 남는다.',
 'A covered fictional adult specimen has one exposed arm; a separate anatomical diagram beside it stays within the edges of its paper sheet.',
 'specimen=covered fictional adult specimen;arm=exposed arm;cover=opaque body covering;diagram=paper anatomical diagram',
 'arm>part_of>specimen;cover>covers_rest_of>specimen;diagram>beside>specimen',
 '도식 장기를 실물 노출로 합침','표본의 죽음·인체 실험의 동의·외계 연구 목적은 문맥이다.',
 'prop_placement,body_region,narrative_clue','S04,S18','','new','P1','proxy')
visual('R42','분리 신체와 절단면 위치',
 '허구 성인 마네킹 같은 몸체와 분리된 팔이 작업대 위에 간격을 두고 놓이며, 양쪽 끝면은 서로 가리지 않는다.',
 'A fictional adult mannequin-like torso and a detached arm lie apart on a worktable; their two end surfaces remain unobscured and distinct.',
 'torso=fictional adult mannequin-like torso;arm=detached arm;table=worktable',
 'torso>rests_on>table;arm>rests_on>table;arm>separated_from>torso',
 '몸에 붙은 팔·의상 소매·가려진 접점','분리 상태의 창작 실현이다. 실제 절단 행위·사망·통증은 판정하지 않는다.',
 'aftermath_trace,object_structure','S18','C043','refine','P1')
visual('R43','무덤 경계와 들어 올린 부장품',
 '열린 석관 안의 뼈 옆에서 작은 장신구가 들어 올려지고, 장갑 낀 손과 장신구의 접촉이 석관 테두리 위에서 보인다.',
 'A gloved hand lifts a small ornament above the rim of an open stone coffin; bones remain inside, and the hand–ornament contact is visible.',
 'coffin=open stone coffin;bones=contained bones;hand=gloved hand;ornament=small ornament',
 'bones>inside>coffin;hand>holds>ornament;ornament>above_rim_of>coffin',
 '고고학 발굴=도굴·시체 훼손','소유권·허가·시신 정체·의도를 외형으로 판정하지 않는다.',
 'relational_action,prop_placement,contact_point','S45','C048','new','P1','proxy')
visual('R44','유골의 공간 분포',
 '지하 통로의 낮은 돌 칸막이 뒤에 뼈들이 쌓이고, 앞쪽 바닥은 비어 있어 칸막이와 축적 경계가 보인다.',
 'Bones accumulate behind low stone partitions in an underground passage while the foreground floor remains clear, exposing the boundary of the accumulation.',
 'bones=bone accumulation;partitions=low stone dividers;passage=underground passage;floor=clear foreground floor',
 'bones>behind>partitions;partitions>within>passage;floor>foreground_of>bones',
 '뼈=식인·인간 가축·동일 가문','종·사육·섭식·역사는 골격 외관만으로 확정되지 않는다.',
 'location,aftermath_trace','S17','C048','refine','P1','proxy')
visual('R45','유체 흔적의 소유와 색',
 '선택한 황금빛 액체가 허구 생물의 피부 틈에서 아래 받침으로 한 줄 이어지고, 표면 반사와 액체 경계가 분리된다.',
 'A chosen gold-colored fluid forms a continuous trail from a fissure in a fictional organism’s surface to a support below, with the fluid boundary distinct from reflected highlights.',
 'organism=fictional organism;fissure=surface fissure;fluid=chosen gold-colored fluid;support=lower support',
 'fissure>on>organism;fluid>extends_from>fissure;fluid>reaches>support',
 'ichor=항상 검은 점액·금색 반사를 체액으로 판정','황금색은 저술 선택이다. 신의 피·독성·생존 상태는 단어와 외형에서 입증하지 않는다.',
 'color,surface_material,aftermath_trace','S38','','new','P0','proxy')
visual('R46','원고의 서로 다른 언어 층',
 '두꺼운 책의 펼친 면에 한 문자 체계의 본문과 다른 체계의 짧은 여백 주석이 분리되어 있고, 둘 다 같은 종이에 속한다.',
 'An open thick book has a main text in one script and short marginal annotations in a visibly different script, both belonging to the same paper page.',
 'book=open volume;page=single paper page;main=main script block;annotation=marginal script',
 'page>part_of>book;main>ink_on>page;annotation>ink_on>page;annotation>beside>main',
 '아라비아어 비슷한 글자를 알 아지프 정본으로 판정','문자 외형은 언어·정확한 번역·가공 저자의 필적을 입증하지 않는다.',
 'visible_text,prop,object_structure','S15,S24','C135','refine','P1','proxy')
visual('R47','금서 판본과 서지 라벨',
 '서로 다른 두 책의 앞에 작은 서지 카드가 따로 있고, 카드의 짧은 언어 표기와 각 책의 연결이 놓인 위치로 분명하다.',
 'Two distinct books each have a separate small bibliographic card directly in front; the short language labels are legible and each card’s association with its own book is unambiguous.',
 'book_a=first book;book_b=second book;card_a=first bibliographic card;card_b=second bibliographic card',
 'card_a>in_front_of>book_a;card_b>in_front_of>book_b',
 '다른 표지색=다른 번역·라벨=역사적 진본','판본 표기는 설정이다. 실제 고대 문헌·실존 소장본으로 주장하지 않는다.',
 'visible_text,prop_placement,narrative_clue','S15,S24','','new','P2','proxy')
visual('R48','빛나는 부등다면체와 상자',
 '붉은 줄이 있는 거의 검은 다면체 돌의 중간을 금속 띠가 감싸고, 일곱 수평 지지대가 띠에서 열린 상자 안쪽 벽까지 이어져 돌을 바닥에서 띄운다.',
 'A metal band surrounds the middle of a nearly black, red-striated polyhedral stone; seven horizontal supports join the band to the inner walls of an open box, suspending the stone above the bottom.',
 'stone=nearly black red-striated irregular polyhedron;band=central metal band;supports=seven horizontal supports;box=open box;bottom=box bottom',
 'band>surrounds_middle_of>stone;supports>join>band;supports>terminate_on_inner_walls_of>box;bottom>part_of>box;stone>suspended_above>bottom',
 '이름에서 정확한 면 수 추론·돌=상자','원전의 구조 일부를 선택한다. 일곱 지지대의 양끝이 가려지면 수량 전체는 미판정이다. 예지·발광 효능·정확한 면 수는 주장하지 않는다.',
 'prop,object_structure,surface_material','S14','','new','P0','versioned')
visual('R49','가지형 표식의 판본 분리',
 '종이 위 하나의 세로 선에서 짧은 사선들이 가지처럼 갈라지며, 같은 종이의 넓은 여백이 표식 둘레에 남는다.',
 'Short diagonal strokes branch from a single vertical stroke on paper, with open margins surrounding this one branch-like mark.',
 'paper=plain paper;stem=single vertical ink stroke;branches=short diagonal ink strokes',
 'stem>ink_on>paper;branches>branch_from>stem',
 '가지형을 별 안의 눈·정확한 획수 정본으로 치환','편지 도상의 설명에 따른 연구용 도식이다. 원본 도판의 정밀 복제·주술 효능을 주장하지 않는다.',
 'prop,visible_text,object_structure','S26','','new','P0','versioned')
visual('R50','황색 표식의 검은 장신구',
 '검은 오닉스 같은 잠금 장신구의 금색 선 문양이 표면에 박혀 있고, 장신구가 외투 천에 고정된 경계가 보인다.',
 'Gold-colored linework is inlaid on a black onyx-like clasp; the boundary where the clasp is fastened to a coat remains visible.',
 'ornament=black onyx-like clasp;lines=gold-colored inlaid lines;coat=coat fabric',
 'lines>inlaid_on>ornament;ornament>fastened_to>coat',
 '후대 삼지 표식을 체임버스 정본으로 확정','선의 정확한 도안은 저술 선택이다. 하스터 정체·소유자의 교단·인지 위험은 판정하지 않는다.',
 'prop,object_structure,surface_material','S27','C131','refine','P0','versioned')
visual('R51','은열쇠와 상자의 접점',
 '은빛 열쇠가 열린 조각 목제 상자 안쪽의 작은 홈에 놓이고, 금속 반사와 목재 무늬가 분리된다.',
 'A silver-colored key rests in a shallow recess inside an open carved wooden box; its metallic reflections remain distinct from the wood grain.',
 'key=silver-colored key;box=carved wooden box;recess=inner shallow support',
 'key>rests_in>recess;recess>part_of>box',
 '은색=순은·열쇠=문 작동','열쇠 세부와 받침 홈은 선택형이다. 꿈 접근·시간 여행·재료 분석은 별도다.',
 'prop,prop_placement,surface_material','S22','','new','P1','versioned')
visual('R52','문양과 소환의 인과 분리',
 '바닥 선으로 된 닫힌 원의 바깥에 성인 참가자들이 서 있고, 원 안 중앙에는 작은 물체 하나가 놓인다.',
 'Adults stand outside a closed line circle drawn on the floor; one small object rests at the circle’s center, with the line and the object distinct.',
 'adults=adult participants;circle=closed floor line;object=central object;floor=support floor',
 'adults>outside>circle;circle>drawn_on>floor;object>at_center_of>circle',
 '집합 배치=소환 성공·모든 원전 의례 필수 마법진','정확한 원형 배치는 저술 제안이다. 소환·신앙·자발성은 판정하지 않는다.',
 'prop_placement,proxemics,object_structure','S03,S21','C098,C173','refine','P0','proxy')
visual('R53','영창 행위와 오디오 분리',
 '성인 참가자들이 각자 손에 든 종이를 향해 입을 벌리고 있으며, 종이와 얼굴이 따로 읽힌다.',
 'Adult participants hold separate sheets toward their faces with mouths open; each face and its own sheet remain distinguishable.',
 'participants=adult participants;mouths=visible mouths;sheets=individual held sheets',
 'mouths>part_of>participants;participants>hold>sheets',
 '벌린 입=특정 언어·음량·음정·사악한 영창','말하는 듯한 자세만 보인다. 주문 내용·소환 효능·집단 의도는 문맥이다.',
 'expression,relational_action,prop_placement','S03','C112','new','P1','proxy')
visual('R54','제단과 성인 신체의 위치',
 '완전히 옷 입은 허구 성인이 낮은 석대 위에 누워 있고, 다른 성인 둘은 석대 끝에서 떨어져 서 있다.',
 'A fully clothed fictional adult lies on a low stone platform; two other adults stand apart from its ends, leaving the prone body and platform boundaries visible.',
 'prone=clothed fictional adult;platform=low stone platform;others=two standing adults',
 'prone>lies_on>platform;others>stand_apart_from>platform',
 '누운 사람=인신공희·제단=죽음·참여=동의','의례적 희생과 강압은 설정이다. 자발성·사망·거래·가해 행위는 미입증이다.',
 'prop_placement,proxemics,situation_context','S03','C045','refine','P1','proxy')
visual('R55','의례적 나체의 비성적 문맥',
 '비노골적인 뒷모습의 성인 한 명이 돌 문턱 앞에 서 있고, 접은 예복은 옆 받침 위에 놓여 있다.',
 'One adult is seen non-explicitly from behind, standing before a stone threshold; a folded ceremonial robe rests on a separate support beside the adult.',
 'adult=adult seen from behind;threshold=stone threshold;robe=folded ceremonial robe;support=separate robe support',
 'adult>stands_before>threshold;robe>rests_on>support;support>beside>adult',
 '나체=성적 의례·동의·바카날','성인·나체와 의례 문맥은 분리한다. 선정성·성행위·강압은 자동 추가하지 않는다.',
 'adult_presentation_context,prop_placement,composition','S03','C054','refine','P2','proxy')
visual('R56','천체 도식과 실제 하늘의 대응',
 '관측대의 성도판에 표시된 세 점과 창 너머 하늘의 세 밝은 점이 같은 꺾인 배열로 보이며, 판 테두리와 창틀은 분리된다.',
 'A star chart on an observatory desk and three bright points beyond a framed window share the same bent arrangement; the chart border remains separate from the window frame.',
 'chart=star chart;chart_points=three drawn points;window=framed window;sky_points=three distant bright points',
 'chart_points>drawn_on>chart;sky_points>seen_through>window;chart_points>correspond_in_layout_to>sky_points',
 '별 배열=귀환 시간표·천문학적 정확도','천체 정렬과 존재 각성의 인과는 서사다. 세 점 배열은 저술한 비교 기준이다.',
 'prop_placement,narrative_clue,visible_text','S03','C065','refine','P1','proxy')
visual('R57','휴면처럼 보이는 몸과 석실',
 '거대한 생물 한 몸이 석실 바닥의 홈에 기대 있고, 배의 윤곽과 몸에 닿는 홈 가장자리가 함께 보인다.',
 'One immense organism rests against a recess in a stone chamber floor; its ventral outline and the recess edges supporting it remain visible together.',
 'organism=resting immense organism;recess=stone floor recess;chamber=stone chamber',
 'organism>rests_in>recess;recess>within>chamber',
 '정지 자세=수면·죽음·불사','휴면의 시각적 대안이다. 생존 상태·꿈·귀환 조건은 미입증이다.',
 'body_pose,location,scale_relation','S03','','new','P2','proxy')

context('K01','장르·철학·설정망의 독립','러브크래프트적 공포·코스믹 호러는 표현 양식, 코스미시즘은 관점, 크툴루 신화는 공유 설정망으로 구분한다. 허무주의·인간중심주의 해체는 별도 해석축이다.','horror라는 단어가 촉수·녹색·우주 배경·잔혹성을 자동 강제','넓은 장르는 검색 문맥이며 단독 시각 의무를 만들지 않는다.','S01,S02,S28','C004,C010')
context('K02','미지·불가지·명명의 한계','정보 부족과 인간 인식의 원리적 한계를 구분한다. 지식이 위험해지는 서사도 별개다.','보이지 않는 것=불가지·기하 모순=인식 붕괴','부분 공개·가림은 선택 실현이며 불가지성을 증명하지 않는다.','S01,S02','C006,C027,C177')
context('K03','정신·기억·정체성의 서사층','집착·기억 공백·정신 교환·정체성 해체·광기 묘사는 각각 사건과 해석을 요구한다.','특정 표정·장애·눈동자·인종=광기 또는 비인간 정체','의학 진단과 내면·기억·의식 소유는 정지 사진에서 판정하지 않는다.','S08,S16,S29','C118')
context('K04','서술 기법은 프레임 수와 다르다','서간체·액자서사·지연 폭로·부정적 묘사·제한 시점·회복 없는 생존은 정보 제시 방법이다.','여러 액자=액자서사·검은 실루엣=부정적 묘사·표정=믿을 수 없는 화자','문서 소품은 선택 실현이다. 순서·화자의 신뢰·관객의 발견은 단일 정지 화면으로 검증할 수 없다.','S01,S03,S12','C139',mode='sequence')
context('K05','심층 시간·미래·주기의 구분','심층 시간·인류 이전 문명·인류 이후 미래·우주 주기·별의 때를 각각 기간·역사·조건 문맥으로 보존한다.','낡음=수억 년·폐허=인류 멸종·성도=각성','층서·폐허·성도는 기간과 인과의 대리 단서다.','S03,S04,S08','C061,C067')
context('K06','실제 비유클리드와 허구 불가능 공간','비유클리드 기하, 고차원 설정, 지각 혼란, 불가능 도형, 원근 왜곡을 따로 기록한다.','초광각·더치 앵글·나선계단=수학적 비유클리드','수학은 별도 검증이며 장르 단어가 고정 계단·포털을 요구하지 않는다.','S03,S10,S33','C070,C138,C148')
context('K07','가공 지명의 선택형 외관','아컴·대학·인스머스·던위치·킹스포트·르뤼에·드림랜드·렝·유고스는 작품별 장소다.','모든 장소를 하나의 고정 지도·고딕 양식·어두운 항구로 합침','지명만으로 주민 외모·종교·계급·도덕·실제 위경도를 만들지 않는다.','S03,S06,S07,S09,S11,S21','C133,C134')
context('K08','신격 분류의 판본','Great Old Ones·Outer Gods·Elder Gods·Other Gods와 생물 종족 Elder Things는 서로 다른 텍스트 층이다.','엘더 싱=엘더 갓·모든 Old Ones=같은 분류','러브크래프트·후대 소설·Chaosium 판본을 명시하고 작품의 모호성을 보존한다.','S04,S11,S28','C130')
context('K09','아자토스·요그 소토스의 비고정 외형','원전의 우주적 명칭과 시적 이미지·문턱 관계를 유지하되 얼굴·구체 수·꿈 우주 등식을 고정하지 않는다.','아자토스가 깨어나면 우주 소멸=원전 확정','명칭의 정본 생물 해부학은 보류한다. 작품의 해당 구절과 후대 버전을 더 확보해야 한다.','S09,S25','C127,C128',adoption='defer',mode='versioned_context')
context('K10','슈브 니구라스·다곤·히드라의 외관','이름·칭호·교단 관계와 실제 등장 몸을 분리한다.','검은 염소=원전 정본 신체·Mother Hydra=그리스 다두 뱀','명시되지 않은 해부학은 신규 정본 후보로 만들지 않는다.','S07,S09,S28','C129,C149',adoption='defer',mode='versioned_context')
context('K11','노덴스·차토구아·하스터·황색의 왕','노덴스의 작품별 역할, Smith 계열 차토구아, 비어스·체임버스·후대 하스터와 왕을 분리한다.','하스터=왕·노덴스=모든 판본의 선신·모든 이름이 러브크래프트 창작','차토구아 원작과 비어스 원문은 이번에 직접 검토하지 않았다. 이름 계보 전체는 보류하고 조사 과제로 남긴다.','S11,S26,S27,S28','C152',adoption='defer',mode='versioned_context')
context('K12','금서의 가공 서지와 미검증 책들','네크로노미콘의 저자·번역·가상 연혁과 실제 원전·시판 모작을 분리한다. 다른 마도서는 저자·최초 작품·판본 별도 확인 대상이다.','Book of Eibon·De Vermis·Unaussprechlichen Kulten을 같은 책의 별칭으로 합침','에이본의 서·벌레의 신비·이름 없는 제의·프나코틱 사본의 독립 원작 서지를 이번에 전부 검증하지 않았다.','S15,S24','C135',adoption='defer')
context('K13','가공 언어·문양·효능 분리','Aklo의 원문 언급, 표면 선 문양, 발음 가능한 주문, 관객의 인지 위험은 서로 다른 자료다.','아무 룬=아클로·표식 복제=소환·Yellow Sign=Elder Sign','문자 정확성·독해·주술 효과는 이미지 형태와 독립적으로 검증한다.','S09,S14,S26,S27','','context')
context('K14','의례의 행위와 소속','교단·다곤 교단·별의 지혜 교단·호명·소환·영창·희생 거래·종말론을 역할과 인과 문맥으로 보존한다.','두건·원·종교 의상=악한 소속·소환 성공·동의','특정 현실 종교나 민족을 허구적 교단 표지로 사용하지 않는다.','S03,S07,S14,S21','C097,C173')
context('K15','신체 변형과 원인·역사의 독립','바디 호러·비체·변신·격세유전·퇴화·인공생명·재생명화·사령술·부패는 모양과 원인·서사가 다르다.','혼합 몸=열등·질병·악의·비인간 인격','유전·진단·살아 있음·죽음·초자연 효능은 현재 외관에서 판정하지 않는다. 원전의 인종주의·우생학적 관점을 중립 분류로 복제하지 않는다.','S04,S07,S18,S32,S42','C040,C041,C049')
context('K16','섭식 대상·유골·사육의 구분','식인·시체 섭식·인간 가축·해부 표본·도굴·시신 훼손은 대상과 행위, 허가·역사가 다르다.','구울·뼈·이빨=식인 확인·표본=비동의','섭식 대상 동정·죽음·과거 소유·강압은 추가 증거가 필요하다.','S12,S17,S18','C047')
context('K17','생식·친족·동의의 독립','생식 공포·이종 생식·혼종·생식 강요·근친상간·근친교배·괴물적 탄생은 서로 다른 주장이다.','이종 특징=성폭력·가족 관계=근친상간·임신=동의','성적 행위·친족·동의·가해자·혈통은 몸 외형으로 증명되지 않는다. 던위치의 미기재 사건을 사실로 만들지 않는다.','S07,S09','C052,C053')
context('K18','성적 금기의 비가시 주장','시체성애·성폭력·촉수 에로티카·Cthulhurotica·에로틱 호러는 문학·후대 장르 문맥으로 구분해 보존한다.','촉수=성행위·나체=비동의·시체 곁 사람=시체성애','용어 연구와 이미지 제작 자격은 별개다. 성폭력·시체와의 성행위는 해석 문맥으로 보존하며 해당 행위의 시각 후보는 작성하지 않는다.','S23,S32','C051,C053',adoption='context')
context('K19','괴물적 여성성과 비판적 재해석','여성 몸·모성·출산의 공포 재현을 분석하는 관점과 퀴어·페미니즘 재서술을 문맥으로 보존한다.','여성=괴물·혼종=타락·정체성만으로 외형 강제','Barbara Creed 원저·Project LC.RC 논문·개별 현대 소설 전문은 이번에 읽지 않았다. 정의 확정과 작품별 시각화를 보류한다.','S32,S42','','defer')
context('K20','묘사 형용사는 원인과 다르다','eldritch·ineffable·unspeakable·unnamable·blasphemous와 태고·지하·암흑 어휘는 문체와 해석 문맥이다.','eldritch=초록 촉수·antediluvian=실제 지질 시대·blasphemous=특정 종교 악성','구체 장면을 골라야 하며 어휘만으로 색·해부학·도덕을 강제하지 않는다. 모든 어휘의 독립 사전 항목을 이번에 검증한 것은 아니다.','S01,S02,S41','C009')
context('K21','소리·냄새의 독립 채널','fetid·mephitic는 후각/대기 문맥, gibbering·ululation은 소리다. charnel·sepulchral은 장소·분위기와 소리의 중의성이 있다.','안개=악취·벌린 입=울부짖음·황록 기체=독성','정지 영상은 소리·냄새·독성·정확한 감정의 PASS 근거가 아니다.','S13,S39,S40','C095,C112',mode='audio_or_olfactory')
context('K22','가변성과 동작의 시간축','protean·metamorphosis·reanimation·disintegration은 변화의 서사를 포함할 수 있다. 한 프레임의 혼합 경계와 시간 변화 증거는 다르다.','흐릿함=변신·정지 몸=부활·겔=살아 있는 원형질','시퀀스 비교나 영상으로 따로 계획한다. 정지 후보는 선택한 현재 형태만 책임진다.','S04,S07,S18','C041,C113,C176',mode='sequence')
context('K23','SAN과 실제 정신 건강','SAN·Sanity Loss는 RPG 수치와 게임 규칙이다.','창백함·기괴한 눈=이성 상실 수치','수치는 읽을 수 있는 UI/문서의 그래픽으로만 선택 가능하다. 실제 질환·회복력은 외관에서 평가하지 않는다.','S29','','context')
context('K24','인지재해·정보재해의 후대 용례','SCP에서 쓰는 인지·정보 위험을 원전의 금지 지식과 비교하되 동일 개념으로 합치지 않는다.','책 읽기+놀람=위험 전파·모든 금서=인지재해','지각·전파·위험의 인과는 설정이다. 그림 자체에 실제 위험 효능을 부여하지 않는다.','S30','C117')
context('K25','현대 위어드·생태·공생의 확장','Ecohorror·Posthuman Horror·New Weird·pastiche·critical rewriting·symbiosis는 다른 분석축이다.','뉴 위어드=러브크래프트 복사·공생=항상 기생·괴물은 항상 적대','현대 작품 전문의 독립 조사와 개념 정의는 추가 과제다. R38은 원전 사실이 아닌 저술한 돌봄 대안이다.','S05,S32','','context')
context('K26','비행 폴립·구울의 형태와 서사','비행 폴립의 부분 물질성·소리·바람과 구울의 식시·인간과의 관계는 서로 다른 서사와 감각이다.','유령=폴립·구울=항상 살아 있는 인간 공격·날개 유무를 이름에서 도출','원전의 해당 생물 전 묘사를 이번에 정밀 대조하지 않았다. 정본 전신 후보는 보류하며 유골 배치만 선택 가능하다.','S08,S11,S12','','defer',mode='versioned_context')
context('K27','생물 유사 형용사와 생물학적 동정','batrachian·ichthyoid·fungoid는 닮음의 언어다. amorphous·gelatinous·protoplasmic은 모양·질감·생물학 용례가 다르다.','두꺼비 닮음=실제 양서류·겔=살아 있는 원형질·균류=독성','형태·질감의 선택 실현은 R28/R33/R36으로 분리하고, 진짜 종·세포 구성·물성을 확정하지 않는다. 전 어휘의 사전 독립 검증은 미완료다.','S04,S06,S07,S35','C013,C020')

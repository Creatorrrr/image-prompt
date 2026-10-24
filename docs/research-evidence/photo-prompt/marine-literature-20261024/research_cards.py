"""Authored research proposals; never imported by the operating candidate loader."""
CARDS = []


def add(key, label, seeds, slots, owners, relations, en, ko, boundary,
        sources='S00', mode='still', priority='P0'):
    """Three bilingual visible propositions, explicit nodes, directed endpoints."""
    nodes = [dict(zip(('id', 'description'), n.split(':', 1))) for n in owners.split('|')]
    edges = [dict(zip(('subject', 'predicate', 'object'), r.split('>'))) for r in relations.split('|')]
    ec, kc = en.split(';'), ko.split(';')
    assert len(ec) == len(kc) == 3, key
    CARDS.append(dict(
        id=key, label=label, seed_terms=seeds.split('|'), planned_slots=slots.split('|'),
        owners=nodes, relations=edges, mode=mode, priority=priority,
        source_ids=sources.split('|'), source_scope='authored visual proposal; sources support only the indicated term or boundary, not the complete scene',
        components=[{'id': f'{key}-G{i+1}', 'en': e.strip(), 'ko': k.strip(),
                     'required': True, 'render_gate': f'Inspect {e.strip()} together with the other two groups in the same image or declared panel.'}
                    for i, (e, k) in enumerate(zip(ec, kc))],
        proposal_en='; '.join(s.strip() for s in ec)+'.',
        proposal_ko='; '.join(s.strip() for s in kc)+'.',
        confusion_boundary=boundary, claim_limits=[
            'Visible pose, clothing or a label does not establish identity, military service, rank, sexual orientation, consent, intent, diagnosis, chemical composition, chronology or real events.',
            'Broad genre and character names are context only. Adopt this realization explicitly; preserve requester-owned people, counts, clothing, medium and exclusions.',
            'All selected groups and their endpoints must be observable together. UNOBSERVABLE_NOT_PASS; partial_is_fail; BLOCKED_UNSCORED when no pixels return.'
        ], runtime_registered=False, native_pixel_status='NOT_RUN'))


# Clothing and attachments: material, wearer, layer and local colour remain separate.
add('V001','각진 군용 팔각모','팔각모','wearable_accessory|object_structure',
    'person:adult wearer|cap:short-brimmed faceted cap|crown:polygonal crown|brim:projecting brim',
    'person>wears>cap|crown>part_of>cap|brim>projects_from>cap',
    'a stiff polygonal crown has distinct angled side panels;a short brim projects from the front of the same cap;the cap rests on the adult wearer’s head',
    '단단한 다각형 모체의 옆면이 각진 패널로 나뉜다;같은 모자의 앞쪽에서 짧은 챙이 돌출된다;모자가 성인 착용자의 머리에 놓인다',
    '야구모자·베레모·긴 챙의 조교모와 구분. 단일 시점에서 뒤쪽까지 여덟 각 모두 확인했다고 주장하지 않는다.', 'S00|S09|S10')
add('V002','가슴 천 위의 적색 이름표','빨간 명찰','garment_detail|visible_text',
    'person:wearer|shirt:upper garment|patch:red rectangular cloth patch|letters:optional declared text',
    'person>wears>shirt|patch>attached_to>shirt|letters>printed_on>patch',
    'a horizontal red rectangular patch lies on the upper garment’s chest;the patch border remains distinct from the surrounding cloth;any requested name is confined to that patch',
    '상의 가슴의 가로로 긴 직사각형 패치가 붉다;패치 테두리가 주변 천과 구분된다;요청된 이름 글자는 그 패치 안에만 놓인다',
    '이름표와 계급장·부대 마크·국기 구분. 실제 소속·실명은 확정하지 않으며 정확한 한글은 별도 게이트다.', 'S00|S09')
add('V003','피부 위에 놓인 별도 패치','맨상체의 명찰','prop_placement|body_marking',
    'person:adult actor|skin:uncovered upper chest|patch:separate red surface patch',
    'skin>part_of>person|patch>rests_on>skin',
    'an adult actor’s upper chest is uncovered;a separate red rectangular patch rests against that chest;its complete border distinguishes it from skin and any nearby cloth',
    '성인 인물의 윗가슴이 옷에 덮이지 않는다;별도 붉은 직사각형 패치가 그 가슴 표면에 놓인다;패치의 온전한 테두리가 피부와 주변 천을 구분한다',
    '옷 위 명찰과 다른 대안. 침습 부착·상처·피어싱을 추정하지 않는다. 팬덤 필수 설정으로 주장하지 않는다.')
add('V004','매트한 편상 전투화 외형','세무워커·쎄무워커','footwear|surface_material',
    'person:adult wearer|boots:pair of ankle-height lace-up boots|soles:thick outsoles',
    'person>wears>boots|soles>part_of>boots',
    'ankle-height boots enclose the wearer’s feet;laces cross through opposing rows of eyelets;matte short-nap uppers meet visibly thick outsoles',
    '발목 높이의 부츠가 착용자의 발을 감싼다;마주 보는 아일릿 줄 사이로 끈이 교차한다;짧은 결의 매트한 갑피가 두꺼운 밑창과 이어진다',
    '패션용 무릎 높이 스웨이드 부츠와 구분. 표면만으로 가죽 화학·보급 규격·정확한 시대를 확정하지 않는다.', 'S00|S09')
add('V005','전투복의 국소 위장무늬','위장무늬 전투복','wardrobe_style|surface_pattern',
    'person:adult wearer|jacket:long-sleeve jacket|trousers:matching trousers|pattern:camouflage patches',
    'person>wears>jacket|person>wears>trousers|pattern>on>jacket|pattern>on>trousers',
    'a long-sleeve jacket and trousers cover the adult wearer;irregular contrasting patches follow the cloth folds;pockets and seams remain readable beneath the pattern',
    '긴소매 상의와 바지가 성인 착용자를 덮는다;대비되는 불규칙 얼룩이 천의 주름을 따라 이어진다;무늬 속에서도 주머니와 솔기가 읽힌다',
    '일반 얼룩 위장과 특정 한국군 세대의 디지털 패턴을 구분. 시대·부대는 별도 참조 필요.', 'S00|S09')
add('V006','온전한 활동복','활동복|정상적으로 갖춰 입은 활동복','wardrobe_layering|wardrobe_style',
    'person:adult wearer|top:athletic top|pants:athletic pants',
    'person>wears>top|person>wears>pants',
    'an athletic top covers the adult wearer’s torso;athletic trousers cover both legs;the upper hem and waistband make the clothing layers distinct',
    '운동용 상의가 성인 착용자의 몸통을 덮는다;운동용 바지가 양다리를 덮는다;상의 밑단과 허리선으로 옷의 층이 구분된다',
    '상대적 평범함의 한 대안이며 황룡의 유일한 고정 복장으로 잠그지 않는다.')
add('V007','목걸이형 식별표','군번줄','wearable_accessory|contact_point',
    'person:adult wearer|chain:neck chain|tags:two flat plates',
    'chain>around>person|tags>suspended_from>chain',
    'a chain curves around the adult wearer’s neck;two small flat plates hang from the same chain;the chain-to-plate connection is visible against the chest',
    '체인이 성인 착용자의 목 둘레를 지난다;작은 평판 두 개가 같은 체인에 매달린다;가슴 앞에서 체인과 판의 연결점이 보인다',
    '일반 목걸이와 구분하되 실제 군번·국적·신분은 추정하지 않는다.')
add('V008','붉은 삼각 하의 선택형','각개빤쓰·각개빤스','wardrobe_style|garment_fit',
    'person:adult wearer|briefs:opaque red briefs|waistband:upper band|leg_openings:two leg openings',
    'person>wears>briefs|waistband>part_of>briefs|leg_openings>part_of>briefs',
    'opaque red briefs cover the adult wearer’s pelvis;a continuous waistband encloses the waist;two high-cut leg openings remain distinct from the cloth',
    '불투명 붉은 삼각 하의가 성인 착용자의 골반을 덮는다;연속된 허리 밴드가 허리 둘레를 감싼다;양쪽 높게 파인 다리 구멍이 천과 구분된다',
    '사각·반바지형과 상호 배타적 선택형. 성적 동작·지향·동의는 부여하지 않는다.', 'S00|S03')
add('V009','붉은 사각 하의 선택형','각개빤쓰·각개빤스','wardrobe_style|garment_fit',
    'person:adult wearer|shorts:opaque red boxer shorts|hems:two short leg hems',
    'person>wears>shorts|hems>part_of>shorts',
    'opaque red boxer shorts cover the adult wearer’s pelvis;two short fabric legs extend below the crotch;each leg has a separate hem around the upper thigh',
    '불투명 붉은 사각 하의가 성인 착용자의 골반을 덮는다;가랑이 아래로 짧은 천 다리 두 개가 내려온다;양쪽 허벅지 위에 각각 별도 밑단이 있다',
    '삼각 팬티와 구분. 이 형태·색을 모든 인물에 자동 적용하지 않는다.', 'S00|S03')
add('V010','모자와 하의의 최소 복장 조합','팔각모＋각개빤쓰','wardrobe_layering|wearable_accessory',
    'person:adult actor|cap:faceted short-brimmed cap|shorts:opaque red shorts|torso:uncovered torso',
    'person>wears>cap|person>wears>shorts|torso>part_of>person',
    'a faceted short-brimmed cap sits on the adult actor’s head;opaque red shorts cover the pelvis;the torso between the shorts and neck is uncovered',
    '각진 짧은 챙 모자가 성인 인물의 머리에 놓인다;불투명 붉은 짧은 하의가 골반을 덮는다;하의와 목 사이의 몸통은 옷에 덮이지 않는다',
    '완결된 선택형 조합이며 모자·하의·맨상체를 개별 후보에서 무단 묶지 않는다.', 'S00|S03')
add('V011','맨상체 경계','맨상체·상탈','wardrobe_layering|body_region',
    'person:adult actor|torso:upper torso|lower_garment:opaque lower garment',
    'torso>part_of>person|person>wears>lower_garment',
    'the adult actor’s chest and abdomen are uncovered;an opaque lower garment begins at the waist;no shirt panel crosses the exposed torso',
    '성인 인물의 가슴과 배가 옷에 덮이지 않는다;불투명 하의가 허리에서 시작된다;노출된 몸통을 가로지르는 상의 천이 없다',
    '노출 상태는 성적 상황·공격성·가혹행위의 증거가 아니다.')
add('V012','귀에 연결된 작은 링','신체 피어싱','wearable_accessory|contact_point',
    'person:adult actor|ear:visible earlobe|ring:small metal-coloured hoop',
    'ear>part_of>person|ring>passes_at>ear',
    'one earlobe is visible on the adult actor;a small metal-coloured hoop meets that earlobe;the loop is distinguishable from hair and detached background marks',
    '성인 인물의 한쪽 귓불이 보인다;작은 금속색 링이 그 귓불에 연결된다;고리가 머리카락과 배경의 떨어진 자국에서 구분된다',
    '개인 선택형 장식. 가슴 등 다른 부위 피어싱이나 집단 필수 표식으로 확장하지 않는다.')
add('V013','하체 군장만 남은 복장','전투복 바지와 군화','wardrobe_style|footwear',
    'person:adult wearer|trousers:combat-style trousers|boots:lace-up boots',
    'person>wears>trousers|person>wears>boots|trousers>overlap>boots',
    'combat-style trousers cover both legs;lace-up boots enclose both feet;the trouser hems overlap the tops of the same boots',
    '전투복 형태의 바지가 양다리를 덮는다;끈이 있는 군화 형태 부츠가 두 발을 감싼다;바지 밑단이 같은 부츠의 위쪽과 겹친다',
    '상체 옷·머리·소속은 이 하체 대안이 결정하지 않는다.')
add('V014','일상 공구와 제복의 조합','군복과 비군사적 소품의 혼합','prop|contact_point',
    'person:adult wearer|uniform:buttoned utility clothing|wrench:adjustable wrench|hand:actor hand',
    'person>wears>uniform|hand>part_of>person|hand>grips>wrench',
    'an adult wears buttoned utility clothing;one hand grips the shaft of an adjustable wrench;the wrench’s open jaw remains clear of the hand',
    '성인이 단추 달린 작업복 형태 옷을 입는다;한 손이 몽키스패너의 자루를 쥔다;공구의 벌어진 턱은 손에 가려지지 않는다',
    '의복과 도구 소유 관계. 무기 사용·폭력 결과·특정 직업을 추정하지 않는다.', 'S00|S14')

# Body, face and hair. Named-character routes stay versioned, never canonical.
add('V015','과장된 어깨·흉곽·상완','비현실적인 근육량|거대한 상체','body_form|silhouette_proportion',
    'person:adult fictional figure|shoulders:broad shoulders|arms:thick upper arms|torso:large ribcage',
    'shoulders>part_of>person|arms>part_of>person|torso>part_of>person',
    'the adult figure’s shoulders extend broadly beyond the head;thick upper arms remain connected to those shoulders;the enlarged ribcage tapers into the same figure’s waist',
    '성인 인물의 어깨가 머리 바깥으로 크게 넓어진다;굵은 상완이 그 어깨와 이어진다;커진 흉곽이 같은 인물의 허리로 좁아진다',
    '근육량·강함·지능·가해자 지위는 같은 변수가 아니다. 단순 전경 확대와 구분.', 'S00|S04')
add('V016','짧고 굵은 목','짧고 굵은 목','silhouette_proportion|anatomical_connection',
    'person:adult figure|head:head|neck:short broad neck|shoulders:shoulder line',
    'head>connected_via>neck|neck>joins>shoulders|shoulders>part_of>person',
    'a short broad neck connects the head to the shoulders;the jaw remains separate from the shoulder line;both sides of the neck are visible above the collar area',
    '짧고 굵은 목이 머리와 어깨를 잇는다;턱은 어깨선과 구분된다;옷깃 부근 위로 목 양옆이 보인다',
    '목이 가려진 구도·고개 숙임을 짧은 목의 증거로 통과시키지 않는다.')
add('V017','작은 머리와 큰 몸통','작은 머리와 큰 몸의 대비','silhouette_proportion|scale_relation',
    'person:single adult fictional figure|head:head|torso:large torso',
    'head>part_of>person|torso>part_of>person|head>smaller_relative_to>torso',
    'one adult figure has a head small relative to its torso;the neck visibly joins that head and torso;the full shoulder width and head appear in the same depth plane',
    '한 성인 인물의 머리가 몸통에 비해 작다;목이 그 머리와 몸통을 눈에 보이게 잇는다;어깨 전체 폭과 머리가 같은 깊이 평면에 보인다',
    '아동화·별도 인물의 머리·광각의 가까운 손 확대와 구분.')
add('V018','모자챙이 드리운 얼굴 암부','모자챙 아래 얼굴 그림자|얼굴의 암부 처리','shadow_relation|light_shape',
    'person:adult figure|cap:cap|brim:cap brim|face:upper face|shadow:cast shadow',
    'person>wears>cap|brim>part_of>cap|shadow>cast_from>brim|shadow>falls_on>face',
    'a cap brim projects above the same adult figure’s eyes;a dark band follows below that brim across the upper face;the lower face remains more legible than the shaded area',
    '모자챙이 같은 성인 인물의 눈 위로 돌출된다;그 챙 아래의 어두운 띠가 얼굴 위쪽을 가로지른다;얼굴 아래쪽은 암부보다 더 읽힌다',
    '검은 피부색·검은 페이스페인트·얼굴 전체 실루엣과 구분. 황근출의 단일 얼굴로 고정하지 않는다.', 'S00|S04')
add('V019','암부 속 눈과 치아 선택형','눈과 치아만 드러나는 얼굴','light_shape|facial_geometry',
    'face:single adult face|eyes:eye highlights|teeth:visible teeth|shadow:dark face area',
    'eyes>part_of>face|teeth>part_of>face|shadow>covers>face',
    'one adult face is largely rendered in dark tones;small eye highlights remain inside its eye region;a separate row of teeth appears inside that face’s mouth',
    '한 성인 얼굴이 대체로 어두운 톤으로 처리된다;작은 눈 하이라이트가 눈 영역 안에 남는다;별도 치아 줄이 같은 얼굴의 입 안에 보인다',
    '발광 눈·독립된 공중 치아·초자연적 종족은 자동 추가하지 않는다. 그림체 선택형이다.')
add('V020','짧은 옆머리와 남긴 윗머리','상륙돌격형 두발·돌격머리','hair_style',
    'person:adult figure|sides:short side hair|top:longer top hair|scalp:head surface',
    'sides>on>scalp|top>on>scalp|scalp>part_of>person',
    'the adult figure’s side hair is clipped short;the top retains a visibly longer strip of hair;the transition between the side and top regions is readable',
    '성인 인물의 옆머리가 짧게 정리된다;정수리에는 더 긴 머리 부분이 남는다;옆머리와 윗머리의 길이 전환이 읽힌다',
    '단일 표준 규격·모히칸·전원 삭발과 구분. 실제 군 규정 준수는 별도 확인.', 'S00|S09')
add('V021','중앙 모히칸 능선','모히칸형 머리','hair_style',
    'head:adult head|ridge:central hair ridge|sides:short side regions',
    'ridge>on>head|sides>flank>ridge',
    'a narrow hair ridge follows the centre of an adult head;both side regions are substantially shorter;the ridge rises above the side silhouette',
    '좁은 머리 능선이 성인 머리의 중앙을 따른다;양옆 부분은 상당히 짧다;능선이 옆쪽 윤곽보다 위로 솟는다',
    '무모칠의 모든 판본 또는 실제 해병 두발 규격이라고 주장하지 않는다.')
add('V022','머리를 감싼 검은 두건','검은 두건','wearable_accessory|wardrobe_layering',
    'person:adult figure|cloth:black head cloth|knot:rear knot',
    'cloth>wraps>person|knot>part_of>cloth',
    'black cloth wraps around the adult figure’s crown;a tied knot with short ends appears behind the head;the face remains uncovered below the cloth edge',
    '검은 천이 성인 인물의 머리 위쪽을 감싼다;머리 뒤에 짧은 끝이 남은 매듭이 보인다;천 가장자리 아래로 얼굴은 가려지지 않는다',
    '복면·바라클라바와 구분. 도둑·견쌍섭 정체성은 모자만으로 확정하지 않는다.')
add('V023','모니터 머리의 기계 신체','기계 머리·사이보그 몸체|1q2w3e4r!','body_form|anatomical_connection',
    'figure:fictional mechanical figure|monitor:box monitor head|neck:mechanical neck joint|body:mechanical torso',
    'monitor>connected_via>neck|neck>joins>body|body>part_of>figure',
    'a box-shaped monitor occupies the figure’s head position;a visible mechanical neck joint supports that monitor;segmented torso panels connect below the same joint',
    '상자형 모니터가 인물의 머리 위치를 차지한다;보이는 기계 목 관절이 그 모니터를 받친다;같은 관절 아래로 분절된 몸통 패널이 이어진다',
    '손에 든 모니터·뒤쪽 화면·헬멧과 구분. 통신 능력·인격·공식 디자인은 미확정.', 'S00', priority='P1')
add('V024','보통 체형과 거구의 비교','평범한 성인 남성 체형|황룡','scale_relation|character_contrast',
    'a:ordinary adult male figure|b:exaggerated adult male figure|floor:shared floor',
    'a>stands_on>floor|b>stands_on>floor|a>narrower_than>b',
    'two adult male figures stand on the same visible floor plane;one has ordinary torso proportions while the other has exaggerated shoulders;their heads and feet remain simultaneously visible for comparison',
    '두 성인 남성 인물이 같은 보이는 바닥 평면에 선다;한 명은 보통 몸통 비례이고 다른 한 명은 과장된 어깨를 갖는다;비교할 두 사람의 머리와 발이 동시에 보인다',
    '작은 인물을 아동으로 만들지 않는다. 보통 체형은 도덕적 정상성·피해 이력의 증거가 아니다.', 'S00|S03')
add('V025','붉은 괴물 형태의 표면','붉은 괴물형 변신|쾌흥태','body_form|color',
    'figure:fictional adult creature form|body:red body surface|limbs:enlarged limbs',
    'body>part_of>figure|limbs>connected_to>body',
    'a fictional adult figure has an enlarged creature-like torso;its body surface is locally red rather than lit by an all-red scene;large limbs remain joined to that torso',
    '허구의 성인 인물이 커진 괴물형 몸통을 갖는다;전체 장면의 적색 조명 대신 몸 표면 자체가 국소적으로 붉다;큰 팔다리가 그 몸통과 이어진다',
    '정지 형태는 변신 과정·힘·분노를 증명하지 않는다. 해당 인물의 판본 선택은 별도.', 'S00', priority='P1')
add('V026','길어진 말 형태 얼굴','말처럼 길어진 얼굴|말딸필','facial_geometry|species_marker',
    'figure:fictional adult character|head:head|muzzle:elongated muzzle|neck:neck',
    'muzzle>part_of>head|head>connected_via>neck|neck>part_of>figure',
    'an elongated muzzle projects from a fictional adult character’s face;the eye region remains behind the muzzle;the head connects continuously to the same character’s neck',
    '허구 성인 캐릭터의 얼굴에서 긴 주둥이가 돌출된다;눈 영역은 주둥이 뒤쪽에 남는다;머리가 같은 캐릭터의 목과 연속되어 이어진다',
    '렌즈 왜곡·말 가면·기록자 역할과 구분. 말딸필의 모든 판본으로 고정하지 않는다.', 'S00', priority='P1')

# Expressions: shape is observable; inner state and judgement remain contextual.
add('V027','턱을 치켜든 얼굴','턱을 치켜든 표정','body_orientation|gaze_direction',
    'person:adult actor|head:head|chin:chin|torso:torso', 'head>part_of>person|chin>part_of>head|head>tilts_up_relative_to>torso',
    'the adult actor’s chin lifts above its neutral position;the underside of the jaw becomes visible;the torso stays sufficiently upright to distinguish the head tilt',
    '성인 인물의 턱이 중립 위치보다 올라간다;턱 아래 면이 보인다;몸통은 머리 기울임과 구분될 만큼 수직으로 남는다',
    '권위·우월감·낮은 카메라 위치를 턱 각도만으로 확정하지 않는다.')
add('V028','힘을 준 근엄한 얼굴','과도하게 근엄한 표정','expression',
    'face:adult face|brows:brows|mouth:closed mouth', 'brows>part_of>face|mouth>part_of>face',
    'both brows draw down toward the centre of the adult face;the lips form a firm closed line;the jaw contour remains visibly set',
    '성인 얼굴의 양 눈썹이 중앙 쪽으로 내려간다;입술이 단단히 닫힌 선을 이룬다;턱 윤곽은 힘이 들어간 형태로 보인다',
    '표정 형태는 명령·처벌·성격·실제 분노의 판정이 아니다.')
add('V029','입꼬리만 오른 미소','입꼬리만 올라간 미소','expression',
    'face:adult face|mouth:mouth|eyes:eyes', 'mouth>part_of>face|eyes>part_of>face',
    'the corners of the adult face’s mouth turn upward;the lips remain mostly closed;the eye region does not expand into a matching broad grin',
    '성인 얼굴의 입 양끝이 위로 향한다;입술은 대체로 닫혀 있다;눈 영역은 크게 웃는 형태로 함께 넓어지지 않는다',
    '친절·기만·위협 의도·동의는 이 국소 미소에서 추론하지 않는다.')
add('V030','치아를 드러낸 웃음','이를 드러낸 웃음','expression',
    'face:adult face|mouth:open mouth|teeth:teeth', 'mouth>part_of>face|teeth>inside>mouth',
    'the adult face’s mouth stretches into a wide grin;teeth remain visible inside the mouth boundary;the raised cheek contours belong to that same face',
    '성인 얼굴의 입이 넓게 웃는 형태로 벌어진다;입 경계 안에 치아가 보인다;올라간 볼 윤곽이 같은 얼굴에 속한다',
    '공격성·광기·성적 의미는 별도 문맥. 공중 치아나 다른 인물의 입을 허용하지 않는다.')
add('V031','크게 뜬 눈과 굳은 입','눈을 크게 뜬 경직','expression|eye_detail',
    'face:adult face|eyes:eyes|mouth:mouth', 'eyes>part_of>face|mouth>part_of>face',
    'both eyes open wide on one adult face;the upper eyelids reveal more of the irises;the mouth remains a small closed or narrowly parted shape',
    '한 성인 얼굴의 두 눈이 크게 뜨인다;윗눈꺼풀이 홍채를 더 드러낸다;입은 작게 닫히거나 좁게 벌어진 형태로 남는다',
    '공포·놀람·명령 이해 여부는 표정만으로 확정하지 않는다.')
add('V032','이마 땀방울과 닫힌 입','식은땀과 굳은 입','surface_moisture|expression',
    'face:adult face|drops:small forehead droplets|mouth:closed mouth', 'drops>on>face|mouth>part_of>face',
    'small droplets sit on the adult actor’s forehead;each droplet is separate from hair and drawn background marks;the same face’s lips remain pressed together',
    '작은 물방울이 성인 인물의 이마에 놓인다;각 방울이 머리카락과 배경 기호에서 구분된다;같은 얼굴의 입술은 눌러 닫힌다',
    '물방울은 차가움·공포·병·악취 원인을 입증하지 않는다.')
add('V033','반쯤 감긴 눈과 중립 입','반쯤 감긴 눈·무표정','expression|eye_detail',
    'face:adult face|eyes:eyes|mouth:mouth', 'eyes>part_of>face|mouth>part_of>face',
    'the adult face’s upper lids cover roughly half the visible eye openings;the mouth forms a neutral near-horizontal line;the cheeks remain comparatively relaxed',
    '성인 얼굴의 윗눈꺼풀이 눈 틈을 대략 반쯤 덮는다;입은 중립적인 거의 수평선을 이룬다;볼은 비교적 이완되어 있다',
    '체념·냉소·지능·피로 진단·황룡의 정체성은 미확정.')
add('V034','만화 눈물의 과장','눈물과 비명의 과장|따흐흑|따흐앙·따흐아앙','expression|image_detail',
    'face:drawn adult face|tears:drawn tear streams|mouth:open drawn mouth', 'tears>start_at>face|mouth>part_of>face',
    'drawn tear streams extend from both eyes of an adult face;the streams stay distinct from the face outline;an exaggerated open mouth occupies the lower face',
    '그려진 눈물 줄기가 성인 얼굴의 양쪽 눈에서 내려온다;눈물 줄기가 얼굴 외곽선과 구분된다;과장되게 벌어진 입이 얼굴 아래쪽에 놓인다',
    '만화 기호 선택형. 울음 소리·고통·성적 행위는 그림만으로 확정하지 않는다.', 'S00', mode='graphic', priority='P1')

# Poses and directed multi-person relations.
add('V035','차렷의 신체 정렬','차렷|아쎄이의 신고','body_pose',
    'person:adult actor|arms:arms|legs:legs|floor:floor', 'arms>part_of>person|legs>part_of>person|person>stands_on>floor',
    'an adult actor stands with the torso upright;both arms remain straight alongside the torso;the legs and feet are held close together on the floor',
    '성인 인물이 몸통을 곧게 세워 선다;두 팔이 몸통 양옆에 곧게 내려온다;다리와 발이 바닥 위에서 서로 가깝게 모인다',
    '정지 형태만 정의하며 실제 군 규정·복종·군번·긴장 감정은 확정하지 않는다.')
add('V036','손과 이마가 연결되는 경례','경례','hand_pose|contact_point',
    'person:adult actor|arm:raised arm|hand:raised hand|temple:temple region',
    'arm>part_of>person|hand>connected_to>arm|hand>beside>temple',
    'one adult actor’s bent arm rises from its own shoulder;straight grouped fingers approach the same actor’s temple;the wrist and hand orientation remain visible at the salute endpoint',
    '한 성인 인물의 굽힌 팔이 자기 어깨에서 올라온다;펴서 모은 손가락이 같은 인물의 관자 부근으로 간다;경례 끝점에서 손목과 손 방향이 보인다',
    '눈가리개·햇빛 가림·타인 이마 접촉과 구분. 특정 국가 규칙은 별도 참조 필요.')
add('V037','같은 방향으로 도열','도열|집단 반복 구도','composition|subject_count',
    'group:declared adult group|line:shared alignment|floor:shared ground', 'group>aligned_along>line|group>stands_on>floor',
    'the declared number of adults stand in an orderly row;their feet share a visible ground alignment;their torsos face the same selected direction',
    '지정된 수의 성인이 질서 있는 줄로 선다;발들이 보이는 바닥 기준선을 공유한다;몸통들이 같은 지정 방향을 향한다',
    '복제 얼굴·인원수 증식·병역 신분 자동 추가를 금한다.')
add('V038','자기 팔짱','팔짱 낀 자세','hand_pose|body_pose',
    'person:adult actor|left_arm:left arm|right_arm:right arm|torso:torso',
    'left_arm>part_of>person|right_arm>part_of>person|left_arm>crosses_over>right_arm|left_arm>in_front_of>torso',
    'both adult actor’s arms bend across their own chest;the forearms cross in front of the torso;each hand remains connected to the correct arm at the opposing upper-arm region',
    '성인 인물의 두 팔이 자기 가슴 앞으로 굽혀진다;두 전완이 몸통 앞에서 교차한다;각 손이 맞은편 상완 부근에서 올바른 팔과 연결된다',
    '두 사람의 팔짱·수갑·손바꿈·복종이나 선임 지위와 구분.')
add('V039','등 뒤로 모은 두 손','뒷짐','hand_pose|body_pose',
    'person:adult actor|arms:two arms|hands:two hands|back:back of torso',
    'arms>part_of>person|hands>connected_to>arms|hands>behind>back',
    'both arms continue behind the adult actor’s torso;both hands gather behind the lower back;the chosen rear view reveals the actual hand-to-hand relation',
    '두 팔이 성인 인물의 몸통 뒤로 이어진다;두 손이 허리 뒤쪽에 모인다;선택된 후면 시점이 실제 두 손의 관계를 드러낸다',
    '정면에서 손이 안 보이는 것만으로 깍지·구속·손의 개수를 통과시키지 않는다.')
add('V040','허리 양쪽에 손','허리에 손을 얹은 자세','hand_pose|contact_point',
    'person:adult actor|hands:two hands|waist:waist|elbows:two elbows', 'hands>part_of>person|hands>contact>waist|elbows>part_of>person',
    'each adult actor’s hand rests on its own side of the waist;both elbows project outward;wrists and forearms visibly connect to the same torso',
    '성인 인물의 각 손이 자기 허리 양옆에 놓인다;양쪽 팔꿈치가 바깥으로 나온다;손목과 전완이 같은 몸통에 이어져 보인다',
    '자신감·허세·성적 의미는 별도. 타인 허리를 잡는 관계로 바꾸지 않는다.')
add('V041','흉곽을 앞으로 편 자세','가슴을 내미는 자세','body_pose|body_orientation',
    'person:adult actor|ribcage:ribcage|shoulders:shoulders|pelvis:pelvis', 'ribcage>part_of>person|shoulders>part_of>person|pelvis>part_of>person',
    'the adult actor’s ribcage projects forward of the pelvis;both shoulders draw backward relative to the chest;the head and waist remain connected in a continuous body outline',
    '성인 인물의 흉곽이 골반보다 앞으로 나온다;양어깨가 가슴에 비해 뒤로 놓인다;머리와 허리가 연속된 몸 윤곽으로 이어진다',
    '과장된 근육량과 자세 변화를 구분. 자부심·용맹을 형태로 확정하지 않는다.')
add('V042','한 인물이 다른 인물을 내려다봄','턱을 들고 내려다보기','gaze_target|scale_relation',
    'a:adult observer|b:adult target|eyes:observer eyes|head:observer head', 'eyes>part_of>a|head>part_of>a|eyes>directed_toward>b',
    'adult A’s eye level sits above adult B’s face;A’s head and visible eye direction angle toward B;both faces appear in the same frame with separate ownership',
    '성인 A의 눈높이가 성인 B의 얼굴보다 높다;A의 머리와 보이는 눈 방향이 B를 향한다;두 얼굴이 별도 소유자로 같은 화면에 보인다',
    '카메라 내려다보기와 구분. 계급·동의·경멸은 시선만으로 판정하지 않는다.')
add('V043','대상을 향한 손가락','손가락질','hand_pose|gaze_target',
    'a:adult pointer|hand:pointing hand|finger:index finger|target:declared target', 'hand>part_of>a|finger>part_of>hand|finger>points_toward>target',
    'one adult’s index finger extends from a visible hand;the remaining fingers fold toward the palm;the finger’s axis points toward a separate declared target in the same frame',
    '한 성인의 검지가 보이는 손에서 뻗는다;나머지 손가락은 손바닥 쪽으로 접힌다;검지 축이 같은 화면의 별도 지정 대상을 향한다',
    '명령·비난·유죄는 미확정. 손의 소유자와 지목 대상 바꾸기는 실패다.')
add('V044','상대 쪽으로 기울인 상체','상체를 앞으로 내밀기','body_orientation|proxemics',
    'a:adult actor|b:adult target|torso:actor torso|hips:actor hips', 'torso>part_of>a|hips>part_of>a|torso>leans_toward>b',
    'adult A’s torso tilts forward relative to A’s hips;A’s head moves into the space toward adult B;both actors remain separate with a visible gap between their bodies',
    '성인 A의 몸통이 자기 골반에 비해 앞으로 기운다;A의 머리가 성인 B 쪽 공간으로 나간다;두 인물은 몸 사이의 보이는 간격을 유지한다',
    '접촉·위협 의도·동의를 자동 추정하지 않는다. 두 인물이 합쳐지면 실패.')
add('V045','넓게 앉은 다리','다리를 벌리고 앉기','body_pose|contact_point',
    'person:clothed adult actor|seat:seat|hips:hips|knees:two knees|feet:feet|floor:floor',
    'hips>part_of>person|hips>supported_by>seat|knees>part_of>person|feet>part_of>person|feet>toward>floor',
    'a clothed adult’s hips rest on a visible seat;the knees spread laterally wider than the hips;both lower legs remain connected and extend toward the floor',
    '옷을 입은 성인의 골반이 보이는 좌석에 놓인다;양 무릎이 골반보다 좌우로 넓게 벌어진다;두 종아리는 연결을 유지하며 바닥 쪽으로 뻗는다',
    '권위·성적 제안·자발성은 추정하지 않는다. 발은 바닥으로 향하며 좌석 위 발 관계를 요구하지 않는다.')
add('V046','문 개구부를 가로지른 인물','문간을 가로막고 서기|황근출의 등장','proxemics|composition',
    'person:adult actor|doorway:door opening|frame:door frame|passage:visible passage',
    'person>within>doorway|frame>bounds>doorway|person>occludes>passage',
    'an adult actor stands within a visible door frame;the shoulders occupy much of the opening’s width;the body overlaps the visible passage behind it',
    '성인 인물이 보이는 문틀 안에 선다;어깨가 개구부 폭의 큰 부분을 차지한다;몸이 뒤쪽 보이는 통로를 가린다',
    '단일 프레임은 실제 감금·출구 부재·통행 방해 의도를 증명하지 않는다.')
add('V047','굳은 어깨와 팔','얼어붙은 자세','body_pose',
    'person:adult actor|shoulders:shoulders|arms:arms|hands:hands', 'shoulders>part_of>person|arms>part_of>person|hands>connected_to>arms',
    'an adult actor’s shoulders are raised and held close;the arms remain stiff beside the torso;both hands show a fixed open or curled configuration',
    '성인 인물의 어깨가 올라가 몸 가까이 모인다;팔이 몸통 옆에서 뻣뻣한 형태로 남는다;양손이 고정된 펼침 또는 굽힘 모양을 보인다',
    '정지 이미지는 움직이지 않은 시간·공포·신경 상태를 증명하지 않는다.')
add('V048','뒤쪽에 놓인 발의 순간','뒷걸음질','body_pose|physical_motion',
    'person:adult actor|front_foot:forward foot|rear_foot:rear foot|target:front-facing target',
    'front_foot>part_of>person|rear_foot>part_of>person|person>faces>target',
    'an adult actor’s face and torso remain oriented toward a front target;one foot extends behind the body;the front knee bends while the rear foot approaches the ground',
    '성인 인물의 얼굴과 몸통은 앞쪽 대상을 향한다;한 발이 몸 뒤쪽으로 뻗는다;뒤 발이 바닥 쪽으로 가는 동안 앞 무릎은 굽혀진다',
    '정지형 자세는 실제 후진 이동을 확정하지 않는다. 이동 방향은 연속 장면이나 명시된 만화 기호 필요.', mode='proxy')
add('V049','몸을 작게 모은 자세','몸을 움츠리기','body_pose',
    'person:adult actor|shoulders:shoulders|arms:arms|torso:torso', 'shoulders>part_of>person|arms>part_of>person|torso>part_of>person',
    'the adult actor’s shoulders round forward;both arms draw close to the torso;the head lowers into the space between the shoulders',
    '성인 인물의 어깨가 앞으로 말린다;두 팔이 몸통 가까이 모인다;머리가 어깨 사이 공간으로 내려온다',
    '추위·공포·굴욕·부상·동의는 포즈만으로 확정하지 않는다.')
add('V050','손바닥을 보이는 거리 두기','손바닥을 보이며 물러서기','hand_pose|proxemics',
    'a:adult actor|palms:actor palms|b:other adult|torso:actor torso',
    'palms>part_of>a|torso>part_of>a|palms>faces_toward>b',
    'adult A holds open palms toward adult B;A’s elbows bend between hands and shoulders;A’s torso leans away while a gap remains between the adults',
    '성인 A가 펼친 손바닥을 성인 B 쪽으로 보인다;A의 팔꿈치가 손과 어깨 사이에서 굽혀진다;A의 몸통이 멀어지는 방향으로 기울며 두 성인 사이에 간격이 남는다',
    '거절의 시각 대리표현이나 실제 동의 상태를 확정하는 게이트로 사용하지 않는다.', mode='proxy')
add('V051','바닥에 낮게 앉은 자세','주저앉기','body_pose|contact_point',
    'person:adult actor|hips:hips|legs:legs|floor:floor', 'hips>part_of>person|legs>part_of>person|hips>rests_on>floor',
    'an adult actor’s hips rest on the floor;both knees bend near the body;the torso stays visibly above the grounded hips',
    '성인 인물의 골반이 바닥에 놓인다;양 무릎이 몸 가까이 굽혀진다;몸통은 바닥의 골반 위로 보인다',
    '붕괴 과정·실신·패배·부상 원인은 정지 자세로 확정하지 않는다.')
add('V052','자기 머리를 감싼 두 손','머리를 감싸기','hand_pose|contact_point',
    'person:adult actor|hands:two hands|head:head|arms:two arms',
    'hands>part_of>person|arms>part_of>person|hands>contact>head',
    'both hands meet the sides or top of the same adult actor’s head;each wrist connects to its own forearm;the elbows remain separated around the head',
    '두 손이 같은 성인 인물의 머리 옆면 또는 위에 닿는다;각 손목이 자기 전완과 이어진다;양팔꿈치가 머리 주변에서 떨어져 있다',
    '고통·혼란·정신질환·강요는 미확정. 다른 사람 손으로 치환하지 않는다.')
add('V053','옷을 입고 엎드린 절 자세','해병 도게자','body_pose|contact_point',
    'person:fully clothed adult actor|hands:hands|knees:knees|head:head|floor:floor',
    'hands>part_of>person|knees>part_of>person|hands>on>floor|knees>on>floor|head>near>floor',
    'a fully clothed adult kneels with both knees on the floor;both hands rest on the floor ahead of the knees;the lowered head approaches the floor between the hands',
    '온전히 옷을 입은 성인의 양 무릎이 바닥에 닿는다;두 손이 무릎 앞의 바닥에 놓인다;낮춘 머리가 두 손 사이의 바닥 쪽으로 간다',
    '일반 절 자세의 제한된 대안. 원문의 노출·성적 가혹행위 판본 의미는 문맥에 따로 보존하며 동일 재현이라 하지 않는다.', 'S00|S08', priority='P1')
add('V054','엎드려뻗친 지지점','엎드려뻗쳐','body_pose|contact_point',
    'person:clothed adult actor|palms:palms|toes:toes|torso:torso|floor:floor',
    'palms>part_of>person|toes>part_of>person|palms>supports_on>floor|toes>supports_on>floor|torso>part_of>person',
    'a clothed adult’s palms and toes contact the floor;both arms support the torso above the floor;the trunk extends between the shoulders and feet without merging into the ground',
    '옷을 입은 성인의 손바닥과 발끝이 바닥에 닿는다;양팔이 몸통을 바닥 위에서 지지한다;몸통이 어깨와 발 사이로 뻗으며 바닥과 합쳐지지 않는다',
    '운동·훈련·가혹행위는 같은 포즈를 공유한다. 강제성은 별도 문맥이다.')
add('V055','앞으로 기운 달리기 순간','돌격','body_pose|physical_motion',
    'person:adult runner|torso:torso|legs:legs|arms:arms', 'torso>part_of>person|legs>part_of>person|arms>part_of>person',
    'the adult runner’s torso leans toward the selected travel side;one knee rises as the opposite leg extends behind;the arms counterbalance with correct shoulder ownership',
    '성인 주자의 몸통이 지정된 진행 쪽으로 기운다;한 무릎이 올라가고 반대 다리는 뒤로 뻗는다;두 팔이 올바른 어깨 소유를 유지하며 균형을 잡는다',
    '공격 목적·실제 속도·도착 지점을 정지 자세만으로 확정하지 않는다.', mode='proxy')
add('V056','위협에서 멀어지는 달리기 구도','역돌격|역돌격·리버스 돌격|빤스런','physical_motion|proxemics',
    'runner:adult runner|threat:declared scene obstacle|ground:shared ground|head:runner head',
    'runner>on>ground|threat>on>ground|head>part_of>runner|runner>oriented_away_from>threat',
    'an adult runner’s torso and leading leg orient away from a separate obstacle;the obstacle remains visible behind the runner;the runner’s head turns partly back toward that obstacle',
    '성인 주자의 몸통과 앞다리가 별도 장애물에서 멀어지는 쪽을 향한다;장애물이 주자의 뒤쪽에 보인다;주자의 머리는 그 장애물 쪽으로 일부 돌아간다',
    '후퇴의 정지 대리형. 자막의 용맹 주장·실제 공포·실제 이동 방향을 이미지 형태와 혼동하지 않는다.', 'S00|S03', mode='proxy')
add('V057','같은 쪽으로 흩어지는 집단','집단 도주','composition|physical_motion',
    'group:declared adult runners|obstacle:separate obstacle|ground:shared ground',
    'group>on>ground|obstacle>on>ground|group>oriented_away_from>obstacle',
    'the declared adult group occupies separated running poses;their leading legs orient toward the same side of the frame;a separate obstacle remains behind the group on the shared ground',
    '지정된 성인 집단이 떨어진 달리기 자세를 취한다;앞다리들이 화면의 같은 쪽을 향한다;별도 장애물이 공유 바닥 위 집단 뒤에 남는다',
    '집단 감정·도주 원인·이전의 위세는 별도. 같은 얼굴 복제와 인원수 변경 금지.', mode='proxy')
add('V058','집단과 한 명의 다른 반응','한 명만 다른 반응|황룡의 반론','composition|character_contrast',
    'group:declared adult group|outlier:one adult outlier|hands:group raised hands|face:outlier face',
    'hands>part_of>group|face>part_of>outlier|outlier>beside>group',
    'a declared adult group holds matching raised-arm poses;one separate adult keeps both arms lowered;the outlier’s visible face has a neutral mouth beside the group',
    '지정된 성인 집단이 같은 팔 들기 자세를 취한다;별도 성인 한 명은 두 팔을 내린다;집단 옆의 다른 인물 얼굴은 중립적인 입을 보인다',
    '정상인·도덕성·정체성·반대 의사를 몸짓만으로 단정하지 않는다.')

# Settings, vehicles and tools: topology and carrier identity matter.
add('V059','컨테이너 적층 성채','해병성채|녹슨 철판·컨테이너 적층|해병성채 전경','object_structure|environment_detail',
    'stack:fictional container stack|upper:upper container|lower:lower container|seams:horizontal tier seams',
    'upper>above>lower|upper>part_of>stack|lower>part_of>stack|seams>on>stack',
    'rectangular ribbed containers form a tall fictional stack;horizontal seams separate the visible tiers;door and window openings remain distinct from the corrugated walls',
    '직사각형 골판 컨테이너가 높은 허구의 적층을 이룬다;수평 이음새가 보이는 층을 나눈다;문과 창 개구부가 골판 벽에서 구분된다',
    '실제 포항 군부대 건축·구조 안전성·정확한 층수는 미확정.', 'S00|S03', priority='P1')
add('V060','17층을 셀 수 있는 입면','17층 컨테이너','object_structure|subject_count',
    'stack:fictional container tower|tiers:seventeen tiers|base:visible base|roof:visible roof',
    'tiers>part_of>stack|base>bottom_of>stack|roof>top_of>stack',
    'the full base-to-roof elevation of a fictional container tower fits the frame;seventeen separate horizontal tiers can be counted;each tier has a distinct boundary across the tower face',
    '허구 컨테이너 탑의 바닥부터 지붕까지 입면이 화면 안에 들어온다;분리된 수평 층 열일곱 개를 셀 수 있다;각 층은 탑 정면을 가로지르는 구분 경계를 갖는다',
    '높아 보임·17 자막만으로 통과 불가. 가려진 층은 UNOBSERVABLE. 구조 고증 주장 아님.', 'S00|S03', priority='P1')
add('V061','반복 침상과 관물함','내무반·생활관|반복되는 침상·관물함|체스터','environment_detail|object_structure',
    'room:barracks-like room|beds:repeated bunks|lockers:upright storage lockers|aisle:central aisle',
    'beds>inside>room|lockers>inside>room|aisle>between>beds',
    'repeated beds line a barracks-like room;upright storage lockers stand beside the bed positions;a continuous aisle separates the bed rows',
    '반복 침상이 병영 형태 방에 늘어선다;침상 위치 옆에 세로 관물함이 선다;연속된 통로가 침상 줄 사이를 나눈다',
    '수용소·실제 부대·강제 거주를 공간만으로 확정하지 않는다. 체스터는 별도 책상으로 오역하지 않는다.', 'S00|S05')
add('V062','취사 공간과 식사 공간','주계·주계장','environment_detail|prop_placement',
    'room:fictional mess area|pots:large cooking pots|counter:serving counter|tables:dining tables',
    'pots>behind>counter|tables>in_front_of>counter|counter>inside>room',
    'large cooking pots stand behind a serving counter;dining tables occupy the opposite side;the counter separates preparation and eating areas within one room',
    '큰 조리 냄비들이 배식대 뒤에 놓인다;식탁들이 반대쪽을 차지한다;배식대가 같은 방의 준비 구역과 식사 구역을 나눈다',
    '주계=인육 조리라는 자동 연상 금지. 주계장이라는 호칭의 직책·장소 문맥은 따로 결정.', 'S00|S05')
add('V063','세 번째 칸의 문자 표식','화장실 3사로','visible_text|environment_detail',
    'room:fictional restroom|stalls:three adjacent stalls|third:third stall|label:declared numeral 3',
    'stalls>inside>room|third>member_of>stalls|label>on>third',
    'three restroom stall fronts appear side by side;the third stall carries the numeral 3;its partition and door remain distinct from the neighbouring stalls',
    '화장실 칸 전면 세 개가 나란히 보인다;세 번째 칸에 숫자 3이 놓인다;그 칸의 칸막이와 문이 이웃 칸에서 구분된다',
    '부활·리스폰은 이 공간에서 보이지 않는다. 문자와 칸 수는 별도 필수 게이트.', 'S00', priority='P1')
add('V064','문패가 있는 빈 방','전우애실','visible_text|prop_placement',
    'room:empty fictional room|door:room door|sign:door sign|text:declared room label',
    'door>opens_to>room|sign>on>door|text>on>sign',
    'a door opens into an empty fictional room;a rectangular sign is attached to that door;only the explicitly requested room label appears within the sign',
    '문이 비어 있는 허구의 방으로 열린다;직사각형 문패가 그 문에 붙어 있다;문패 안에는 명시적으로 요청된 방 이름만 놓인다',
    '문패는 내부 행위·동의·성폭력을 입증하지 않는다. 원래 성적 가혹행위 문맥은 별도 보존.', 'S00', priority='P2')
add('V065','오염처럼 보이는 하천 표면','해병천|해병청정수','surface_pattern|liquid_inclusion',
    'river:fictional watercourse|water:opaque water|debris:floating debris|bank:visible bank',
    'water>inside>river|debris>floats_on>water|bank>bounds>river',
    'opaque water fills a fictional channel;small floating debris lies on its surface;visible banks delimit the same watercourse',
    '불투명 물이 허구의 수로를 채운다;작은 부유 잔해가 그 표면에 놓인다;보이는 둑이 같은 하천의 경계를 이룬다',
    '독성·수질·악취·음용 가능성·실제 포항 하천은 표면만으로 판정하지 않는다.', 'S00|S03', mode='proxy', priority='P1')
add('V066','기괴한 생물과 수목의 동산','해병동산','environment_detail|species_marker',
    'garden:fictional garden|plants:ordinary plants|creature:one declared fictional creature|ground:shared ground',
    'plants>inside>garden|creature>inside>garden|creature>on>ground',
    'ordinary plants occupy a fictional garden;one explicitly declared creature stands among them;both the creature and plants connect to the same visible ground',
    '일반 식물들이 허구의 동산을 채운다;명시적으로 지정한 괴물 한 마리가 그 사이에 선다;괴물과 식물 모두 같은 보이는 바닥과 이어진다',
    '장르 이름만으로 타 작품 괴물·성적 의미·폭력을 추가하지 않는다.', 'S00', priority='P2')
add('V067','붉은 구형 승합차 외형','오도봉고|무톤듀오의 외출','prop|object_structure',
    'van:fictional red minibus|cabin:passenger cabin|windows:side windows|wheels:wheels',
    'cabin>part_of>van|windows>on>cabin|wheels>supports>van',
    'a boxy red vehicle has an enclosed passenger cabin;several side windows continue behind the front seats;visible wheels support the same body above the ground',
    '각진 붉은 차량이 닫힌 승객실을 갖는다;여러 옆창이 앞좌석 뒤로 이어진다;보이는 바퀴들이 같은 차체를 바닥 위에서 받친다',
    '봉고 트럭·화물 밴·구체적 연식과 구분. 제조사 역사 자료는 오도봉고의 색·기능을 입증하지 않는다.', 'S00|S08|S11', priority='P1')
add('V068','앞좌석의 운전자와 옆 인물','무모칠|톤톤정|무톤듀오','contact_point|subject_count',
    'driver:adult driver|passenger:adult passenger|wheel:steering wheel|seats:front seats|van:van interior',
    'driver>in>seats|passenger>in>seats|driver>holds>wheel|seats>inside>van',
    'two separate adults occupy the vehicle’s front seats;the driver’s hands contact the steering wheel;the passenger remains in a distinct seat beside the driver',
    '서로 다른 성인 두 명이 차량 앞좌석에 앉는다;운전자의 손이 운전대에 닿는다;동승자는 운전자 옆의 별도 좌석에 남는다',
    '고정 인물의 체형·커플 여부·납치 임무는 역할만으로 확정하지 않는다.', 'S00|S03', priority='P1')
add('V069','차실 안팎의 공간 모순','무한 수용 차량','surreal_physics_detail|spatial_depth',
    'van:fictional cutaway van|outer:bounded outer shell|interior:long interior corridor|seats:repeated seats',
    'outer>part_of>van|interior>inside>outer|seats>within>interior',
    'a cutaway shows the complete bounded shell of a fictional van;a long interior corridor extends visibly beyond the shell’s apparent depth;repeated seat rows remain inside the depicted corridor',
    '단면에서 허구 차량의 온전한 외곽이 보인다;긴 내부 복도가 외곽의 겉보기 깊이를 넘어 뻗는다;반복 좌석 줄이 그려진 복도 안에 남는다',
    '무한은 유한 픽셀로 증명 불가. 큰 버스·사람 과밀·별도 건물을 차실로 오인하지 않는다.', 'S00', mode='proxy', priority='P2')
add('V070','화물 적재함이 열린 트럭','각개트럭','prop|object_structure',
    'truck:fictional utility truck|cab:front cab|bed:open rear bed|wheels:wheels',
    'cab>part_of>truck|bed>behind>cab|wheels>supports>truck',
    'a fictional utility truck has a separate front cab;an open cargo bed extends behind the cab;the cab and bed share one wheel-supported chassis',
    '허구의 작업용 트럭에 별도 앞 운전실이 있다;운전실 뒤로 열린 화물 적재함이 이어진다;운전실과 적재함이 바퀴가 받치는 한 차대를 공유한다',
    '차량 이름의 고정 차종·빨간 색·탑승 인원을 추정하지 않는다. 승합차와 구분.', 'S00', priority='P1')
add('V071','조절식 스패너의 턱과 나사','몽키스패너','prop|object_structure',
    'tool:adjustable wrench|fixed:fixed jaw|moving:movable jaw|screw:adjusting screw|handle:handle',
    'fixed>part_of>tool|moving>opposes>fixed|screw>adjacent_to>moving|handle>part_of>tool',
    'an open wrench head has one fixed jaw and one opposing sliding jaw;an adjusting screw sits below the movable jaw;a long handle continues from that same head',
    '벌어진 스패너 머리에 고정 턱과 맞은편 이동 턱이 있다;이동 턱 아래에 조절 나사가 놓인다;같은 머리에서 긴 손잡이가 이어진다',
    '파이프렌치·펜치·폐구형 렌치와 구분. 공구는 폭력의 증거가 아니다.', 'S00|S14')
add('V072','칸 나눈 금속색 식판','츄라이·츄레이','prop|object_structure',
    'tray:meal tray|compartments:recessed compartments|rim:continuous outer rim|surface:metal-coloured surface',
    'compartments>part_of>tray|rim>bounds>tray|surface>on>tray',
    'a shallow metal-coloured tray has multiple recessed compartments;raised dividers separate the compartments;a continuous outer rim encloses the same tray',
    '얕은 금속색 식판에 여러 오목한 칸이 있다;솟은 분리벽이 칸들을 나눈다;연속된 바깥 테두리가 같은 식판을 감싼다',
    '식판과 식기 세척 행위 구분. TV 디너 후보의 텔레비전·탁자·음식을 무단 제거해 재사용하지 않는다.', 'S00|S05')
add('V073','작은 금속 관물함','체스터','prop|object_structure',
    'locker:upright storage unit|door:front door|shelves:interior shelves|handle:door handle',
    'door>part_of>locker|shelves>inside>locker|handle>on>door',
    'an upright rectangular storage unit has a front door;a visible handle attaches to that door;open access reveals shelves inside the same unit',
    '세로 직사각형 수납함에 앞문이 있다;보이는 손잡이가 그 문에 붙는다;열린 부분으로 같은 수납함 안의 선반이 보인다',
    '체스터필드 소파·서랍장·특정 실존 인물 이름과 구분.', 'S00|S05')
add('V074','음식 이름과 내용물의 분리','해병푸드|해병짜장|해병맥주|해병수육|해병탕수육|해병특식|해병젤리|해병햄버거','prop_placement|visible_text',
    'table:fictional display table|vessel:opaque covered vessel|card:menu card|text:declared menu title',
    'vessel>on>table|card>beside>vessel|text>on>card',
    'a covered opaque vessel stands on a fictional display table;a separate menu card sits beside that vessel;only the explicitly requested menu title appears on the card',
    '덮인 불투명 용기가 허구의 전시 탁자에 놓인다;별도 메뉴 카드가 그 용기 옆에 선다;카드에는 명시적으로 요청된 메뉴 이름만 보인다',
    '비노출 문맥 전달 대안일 뿐 원래 배설물·인육·체액 설정의 시각 재현이나 입증이 아니다. 용기 내용물은 UNKNOWN.', 'S00|S03|S06|S07', mode='proxy', priority='P2')

# Framing, lighting and visible graphic marks.
add('V075','아래에서 올려다보는 시점','로우앵글 — Low angle','composition|camera_direction',
    'camera:declared camera viewpoint|subject:adult subject|jaw:subject underside|background:vertical background edges',
    'camera>below>subject|jaw>part_of>subject|background>behind>subject',
    'the framing looks upward toward an adult subject;the underside of the jaw or nearby overhead surfaces is visible;background verticals recede upward behind the subject',
    '화면이 성인 대상을 향해 위로 올려다본다;턱 아래나 주변 위쪽 면이 보인다;배경의 수직선이 대상 뒤에서 위로 멀어진다',
    '인물의 아래 시선·키·권력과 카메라 방향 구분. 정확한 카메라 높이는 별도.', 'S00|S12')
add('V076','위에서 내려다보는 시점','하이앵글 — High angle','composition|camera_direction',
    'camera:declared camera viewpoint|subject:adult subject|ground:ground plane', 'camera>above>subject|subject>on>ground',
    'the framing looks downward toward an adult subject;the top planes of the head and shoulders are visible;the ground spreads behind and around the subject',
    '화면이 성인 대상을 향해 아래로 내려다본다;머리와 어깨의 윗면이 보인다;바닥이 대상 뒤와 주변으로 펼쳐진다',
    '고립·나약함·어린 나이를 자동 부여하지 않는다.', 'S00|S12')
add('V077','두 성인의 같은 평면 크기 대비','극단적인 크기 대비','scale_relation|composition',
    'a:large adult figure|b:smaller adult figure|floor:shared reference plane',
    'a>stands_on>floor|b>stands_on>floor|a>larger_than>b',
    'two adults stand at comparable depth on one floor;one adult’s head-to-foot silhouette is much larger;shared floor marks make their scale comparison readable',
    '두 성인이 같은 바닥의 비슷한 깊이에 선다;한 성인의 머리부터 발까지 윤곽이 훨씬 크다;공유 바닥 표식으로 크기 비교가 읽힌다',
    '같은 평면 체격 대비와 원근에 의한 화면 크기 차이를 구분. 작은 인물도 성인.', 'S00|S12')
add('V078','뒤쪽 빛과 어두운 실루엣','역광 실루엣','lighting|light_direction',
    'figure:adult figure|opening:bright opening|outline:figure contour|interior:dark figure interior',
    'opening>behind>figure|outline>bounds>figure|interior>inside>outline',
    'a bright opening lies behind an adult figure;the figure’s outer contour separates from that opening;the interior of the figure remains substantially darker',
    '밝은 개구부가 성인 인물의 뒤에 놓인다;인물의 바깥 윤곽이 그 개구부에서 분리된다;인물 내부는 상당히 더 어둡게 남는다',
    '이 실루엣으로 가려진 눈·명찰·손 연결을 통과시키지 않는다. 공포 감정은 미확정.')
add('V079','중앙 인물과 좌우 대칭','정면 대칭 구도','composition|visual_hierarchy',
    'centre:central adult|left:left adult group|right:right adult group|axis:frame centre axis',
    'centre>on>axis|left>left_of>centre|right>right_of>centre',
    'one adult occupies the frame’s centre axis;declared adults flank the centre on the left and right;the flanking silhouettes form a visibly balanced frontal arrangement',
    '한 성인이 화면 중심축을 차지한다;지정된 성인들이 중앙의 좌우에 놓인다;양옆 윤곽이 정면에서 시각적으로 균형을 이룬다',
    '사열·선전·숭배·군 계급은 구도만으로 확정하지 않는다.')
add('V080','한 사람을 둘러싼 배치','중앙의 고립된 한 사람','proxemics|composition',
    'centre:one adult|group:declared surrounding adults|floor:shared ground',
    'centre>on>floor|group>surrounds>centre|group>on>floor',
    'one adult occupies an open central floor area;other declared adults stand around that area;visible gaps preserve the central figure’s complete outline',
    '성인 한 명이 열린 중앙 바닥을 차지한다;지정된 다른 성인들이 그 공간 주변에 선다;보이는 간격이 중앙 인물의 온전한 윤곽을 남긴다',
    '사회적 배제·기수열외·감금·강압은 배치만으로 입증하지 않는다.')
add('V081','가까운 손을 키운 원근','과장 원근법','composition|spatial_depth',
    'person:adult figure|hand:foreground hand|arm:connecting arm|torso:background torso',
    'hand>part_of>person|hand>connected_via>arm|arm>joins>torso|hand>nearer_than>torso',
    'one adult’s hand fills the foreground;the connected forearm recedes toward that adult’s smaller torso;overlap and size change make the depth order readable',
    '한 성인의 손이 전경을 채운다;이어진 전완이 같은 성인의 더 작은 몸통 쪽으로 멀어진다;겹침과 크기 변화로 깊이 순서가 읽힌다',
    '거대 신체 변형·다른 소유자의 손·렌즈 초점거리 단정과 구분.', 'S00|S12')
add('V082','한 대상에 모이는 집중선','집중선','image_detail|visual_hierarchy',
    'panel:comic panel|lines:radial ink lines|target:declared focal figure',
    'lines>on>panel|target>depicted_in>panel|lines>converges_toward>target',
    'radial ink lines occupy the comic panel’s outer area;their axes converge toward one declared focal figure;the focal figure remains separate from the drawn lines',
    '방사형 먹선이 만화 칸의 바깥쪽을 차지한다;선의 축이 지정된 초점 인물 하나로 모인다;초점 인물은 그려진 선과 분리되어 남는다',
    '실제 광선·빗줄기·총격과 구분. 사진 매체에 자동 추가하지 않는다.', 'S00|S13', mode='graphic', priority='P1')
add('V083','평행한 속도선','속도선','image_detail|motion_rendering',
    'panel:comic panel|lines:parallel ink strokes|runner:drawn adult runner',
    'lines>on>panel|runner>depicted_in>panel|lines>behind>runner',
    'parallel ink strokes run across a comic panel;the strokes remain separate from the drawn adult runner;their shared direction differs from radial focus lines',
    '평행 먹선이 만화 칸을 가로지른다;선들은 그려진 성인 주자와 분리된다;선들의 공통 방향은 방사형 집중선과 다르다',
    '선은 이동을 나타내는 기호이며 실측 속도·방향의 시간적 입증이 아니다.', 'S00|S13', mode='graphic', priority='P1')
add('V084','인물 옆의 큰 효과 문자','거대한 효과음|“악!”|톤!·톤톤!','visible_text|image_detail',
    'panel:comic panel|letters:declared lettering|figure:drawn adult figure',
    'letters>on>panel|figure>depicted_in>panel|letters>beside>figure',
    'large declared lettering sits beside a drawn adult figure;its strokes remain readable apart from the figure outline;the lettering occupies more height than the figure’s head',
    '큰 지정 문자가 그려진 성인 인물 옆에 놓인다;글자 획은 인물 윤곽과 별도로 읽힌다;문자 높이가 인물 머리보다 크다',
    '문자의 존재는 실제 소리·성량의 증거가 아니다. 정확한 한글 게이트 별도.', 'S00|S15', mode='graphic', priority='P1')
add('V085','굵은 먹선과 해칭','먹선과 거친 명암','medium|image_detail',
    'panel:drawn panel|figure:drawn adult figure|contour:thick contour strokes|hatching:shadow hatching',
    'contour>bounds>figure|hatching>on>figure|figure>depicted_in>panel',
    'thick dark strokes outline a drawn adult figure;short hatching strokes build selected shadow areas;white intervals remain between the separate ink marks',
    '굵고 어두운 획이 그려진 성인 인물의 윤곽을 이룬다;짧은 해칭 획이 선택된 암부를 만든다;분리된 먹선 사이에 흰 간격이 남는다',
    '사진 노이즈·검은 피부·실제 상처와 구분. 특정 작가 화풍으로 잠그지 않는다.', 'S00|S13', mode='graphic', priority='P1')
add('V086','별도 테두리 안의 반응 얼굴','반응 컷','format|composition',
    'page:comic page|main:main panel|inset:separate reaction panel|face:drawn adult face',
    'main>part_of>page|inset>part_of>page|face>depicted_in>inset',
    'a comic page contains a main panel;a separate bordered inset contains one adult face;the inset border separates that face from the main panel’s physical space',
    '만화 페이지에 본 장면 칸이 있다;별도 테두리의 삽입 칸에 성인 얼굴 하나가 들어간다;삽입 칸 테두리가 그 얼굴과 본 장면의 물리 공간을 나눈다',
    '실제 장면에 추가 머리를 만들지 않는다. 전후 순서·심리 원인은 정지 칸만으로 입증 불가.', 'S00|S15', mode='graphic', priority='P1')
add('V087','물체에 국한된 붉은 포인트','붉은색의 반복|붉은색 포인트','color|visual_hierarchy',
    'patch:red cloth patch|shorts:red opaque shorts|van:red vehicle body|scene:neutral surrounding scene',
    'patch>within>scene|shorts>within>scene|van>within>scene',
    'a cloth patch has a red local surface;separate opaque shorts and a vehicle body repeat that red;the surrounding scene retains visibly non-red colours',
    '천 패치의 국소 표면이 붉다;별도 불투명 하의와 차량 차체가 그 붉음을 반복한다;주변 장면은 눈에 띄는 비적색 색을 유지한다',
    '적색 조명·전체 색보정·혈흔·집단 필수색과 구분. 세 물건이 함께 요청된 경우만 채택.')
add('V088','냄새를 나타내는 만화 곡선','냄새선·탁한 연무','sensory_cue|image_detail',
    'panel:comic panel|object:declared odour-source proxy|lines:wavy drawn lines|figure:adult reacting figure',
    'lines>above>object|lines>on>panel|figure>depicted_in>panel',
    'wavy drawn lines rise above a declared object in a comic panel;the lines remain graphic marks rather than physical vapour;a separate adult figure holds a hand near the nose',
    '물결 모양의 그린 선이 만화 칸의 지정 물체 위로 오른다;선은 물리 증기 대신 그래픽 기호로 남는다;별도 성인 인물이 코 가까이에 손을 둔다',
    '실제 냄새·독성·오염 원인·화학 성분은 확정하지 않는다. 연무와 기호를 다른 선택형으로 둔다.', 'S00|S03', mode='graphic', priority='P1')
add('V089','탁한 공기층','냄새선·탁한 연무','atmospheric_medium|spatial_depth',
    'space:fictional room|haze:diffuse haze|near:near object|far:far object',
    'haze>inside>space|near>nearer_than>far|haze>between>near',
    'a diffuse haze fills a fictional room;farther objects have softer lower-contrast edges;near objects retain more distinct contours in front of the haze',
    '퍼진 연무가 허구의 방을 채운다;더 먼 물체의 경계는 부드럽고 대비가 낮다;가까운 물체는 연무 앞에서 더 뚜렷한 윤곽을 유지한다',
    '연무는 악취·유독가스·특정 물질의 증거가 아니다. 만화 냄새선과 상호 대체하지 않는다.', mode='proxy', priority='P1')
add('V090','표어판의 운반체와 글자','군대식 표어판','visible_text|prop_placement',
    'wall:fictional wall|board:rectangular signboard|text:declared slogan',
    'board>attached_to>wall|text>on>board',
    'a rectangular signboard attaches to a fictional wall;declared slogan text stays within that board’s boundary;the board and letters remain separate from people in front',
    '직사각형 표어판이 허구의 벽에 붙는다;지정 표어 글자는 그 판의 경계 안에 남는다;판과 글자는 앞쪽 인물에서 구분된다',
    '글자는 실제 규정·기관 승인·등장인물의 믿음을 입증하지 않는다.', mode='still', priority='P1')
add('V091','모순 날씨의 분리된 구역','과장된 날씨','weather|space_condition',
    'scene:fictional scene|left:left snow-covered ground|right:right heat-shimmer area|divider:visible boundary',
    'left>part_of>scene|right>part_of>scene|divider>between>left',
    'one fictional frame shows snow on the left ground;the right ground has drawn heat-shimmer distortion;a visible boundary keeps the two selected weather zones distinct',
    '한 허구 화면의 왼쪽 바닥에 눈이 있다;오른쪽 바닥에는 그려진 열기 왜곡이 있다;보이는 경계가 선택된 두 날씨 구역을 나눈다',
    '작가가 만든 초현실 대안이며 기후·온도·계절의 측정값이 아니다. 장르명만으로 강제하지 않는다.', 'S00|S03', mode='graphic', priority='P2')
add('V092','문장과 장면의 반어 대조','가치전도|반어|완곡어법|자진입대·자원입대|대민지원','visible_text|concept_tension',
    'page:comic page|caption:declared positive caption|scene:separate depicted fictional scene|border:caption border',
    'caption>inside>border|scene>depicted_in>page|caption>above>scene',
    'a bordered positive caption sits above a fictional scene;the depicted adults occupy a separate scene area;the caption’s typography remains distinct from the depicted physical objects',
    '테두리 있는 긍정 자막이 허구 장면 위에 놓인다;그려진 성인들은 별도의 장면 영역을 차지한다;자막의 글자가 그려진 물리 물체와 구분된다',
    '반어의 구체적 서사·강요는 명시된 대화·순서에 달린다. 자진입대라는 문구만으로 자발성을 통과시키지 않는다.', 'S00|S03|S07', mode='graphic', priority='P2')

# Sequence-only records are diagnostic plans, deliberately excluded from still-image drafts.
add('T001','도열에서 역돌격으로 전환','역돌격 장면|역돌격·리버스 돌격','narrative_phase|physical_motion',
    'page:declared ordered sequence|first:first panel|second:second panel|group:declared adult group',
    'first>before>second|group>depicted_in>first|group>depicted_in>second',
    'the first panel shows a declared adult group in formation;the next panel shows corresponding adults running away from the same obstacle;panel boundaries and reading order are explicit',
    '첫 칸은 지정된 성인 집단의 도열을 보여 준다;다음 칸은 대응하는 성인들이 같은 장애물에서 멀어지는 달리기 형태를 보여 준다;칸 경계와 읽는 순서가 명시된다',
    '한 정지 이미지의 뒷모습만으로 앞선 위세·후퇴를 입증하지 않는다. 실제 동일인·시간 경과는 별도.', 'S00|S03', mode='sequence', priority='P2')
add('T002','부활과 동일인 주장 경계','부활·리스폰|빨알라·해병천국','narrative_phase|offscreen_context',
    'sequence:ordered fictional sequence|first:first panel|next:next panel|figure:declared recurring figure',
    'first>before>next|figure>depicted_in>first|figure>depicted_in>next',
    'the first panel marks a declared figure as absent;the next panel depicts the declared figure present;separate panel boundaries preserve the proposed order',
    '첫 칸은 지정 인물이 부재함을 표시한다;다음 칸은 지정 인물이 있음을 그린다;분리된 칸 경계가 제안된 순서를 유지한다',
    '부재→재등장은 실제 죽음·생명·부활의 증명이 아니다. 표기된 서사 주장으로만 보존.', 'S00|S03', mode='sequence', priority='P2')
add('T003','일상에서 밈으로의 전환','해병드리프트','narrative_phase|narrative_core',
    'sequence:ordered fictional sequence|first:ordinary opening panel|next:meme-reveal panel|motif:selected reveal motif',
    'first>before>next|motif>depicted_in>next',
    'an opening panel presents an ordinary declared situation;a later panel introduces one explicitly selected meme motif;panel boundaries preserve the reveal as a later authored event',
    '도입 칸이 명시된 일상 상황을 보여 준다;뒤의 칸이 명시적으로 선택된 밈 표식 하나를 도입한다;칸 경계가 그 공개를 뒤의 창작 사건으로 유지한다',
    '한 장의 군인 그림=드리프트 아님. 일반 장르 요청에 반전이나 밈 표식을 주입하지 않는다.', 'S00', mode='sequence', priority='P2')
add('T004','간단히 끝나는 회의의 순서','마라톤 회의','narrative_phase|visible_text',
    'sequence:ordered fictional sequence|first:opening meeting panel|next:closing panel|caption:declared time caption',
    'first>before>next|caption>on>next',
    'the first panel shows adults seated around a meeting table;the next panel shows the meeting table abandoned;a declared short-time caption belongs only to the closing panel',
    '첫 칸은 회의 탁자 둘레에 앉은 성인들을 보여 준다;다음 칸은 사람들이 떠난 회의 탁자를 보여 준다;명시된 짧은 시간 자막은 마무리 칸에만 속한다',
    '회의라는 그림만으로 회의 길이·비합리성·결론을 확정하지 않는다.', 'S00', mode='sequence', priority='P2')

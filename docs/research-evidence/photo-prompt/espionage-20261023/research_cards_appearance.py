from research_cards import group

group("two_person_blocking", "S08,S16,S23", "body_pose,relational_action,contact_point,gaze_target",
      "Arrangement cannot establish allegiance, consent, romance, blackmail, restraint purpose, injury cause or authority.", r"""
face_to_face|마주 선 두 사람|Two separate torsos face each other across an unoccupied gap.|별도의 두 몸통이 빈 간격을 두고 서로 마주한다.|A.torso>faces>B.torso|두 몸 경계;방향과 간격|이미 접촉;대립의 원인
side_by_side|나란한 두 사람|Two people stand next to each other facing the same direction.|두 사람이 옆에 서서 같은 방향을 향한다.|A>beside>B;A.torso>parallel_to>B.torso|두 몸 경계;각자의 방향|연인·동료 신분;시선 방향 강제
back_to_back|등을 맞댄 두 사람|Two people face opposite ways with upper backs in visible contact.|두 사람이 반대 방향을 향하고 등 윗부분이 서로 닿는다.|A.upper_back>contacts>B.upper_back|등의 접점;반대 몸 방향|떨어진 포스터 합성;공동 충성
whisper_proximity|귓가 가까운 입|One person's mouth is close to another person's ear with a visible gap.|한 사람 입이 상대 귀 가까이에 있고 작은 틈이 보인다.|A.mouth>near>B.ear|입과 귀의 다른 소유자;간격|입맞춤;실제 말·동의
other_tie|상대 타이를 정리하는 손|One person pinches another person's tie knot below that person's collar.|한 사람이 상대 칼라 아래 넥타이 매듭을 집는다.|A.hand>pinches>B.tie.knot;B.tie.knot>below>B.collar|행위자의 손;상대의 매듭|자기 타이;배려나 지배
ballroom_hold|춤의 두 접점|Two adults join one pair of hands while another hand rests on the partner's upper back.|성인 두 사람이 한 쌍의 손을 맞잡고 다른 손은 상대 등 윗부분에 놓인다.|A.hand1>joins>B.hand1;A.hand2>contacts>B.upper_back|맞잡은 두 손;등 접촉과 팔 연속성|중복 팔;연애·비밀 거래
divergent_gazes|가까운 몸과 다른 시선|Two people stand close while looking at two different visible points.|두 사람 몸은 가깝고 각자는 서로 다른 보이는 지점을 바라본다.|A>near>B;A.gaze>toward>target1;B.gaze>toward>target2|몸 간격;다른 두 시선 종점|불충·배신;같은 대상 응시
seated_standing|앉고 선 높이 차이|A seated person faces a standing person across a table.|앉은 사람이 탁자 건너 선 사람을 마주한다.|A.pelvis>supported_by>chair;B.feet>supported_by>floor|각자 지지면;탁자와 높이|심문 확정;직급 자동 지정
threshold_standoff|문을 사이에 둔 두 사람|Two people face each other from opposite sides of a doorway.|두 사람이 출입구 반대쪽에서 서로 마주한다.|A>on_side1_of>doorframe;B>on_side2_of>doorframe;A.torso>faces>B.torso|문틀 경계;인물의 반대쪽 위치|출구 봉쇄 성공;이전 감금
supported_walk|다른 몸에 체중을 기대기|One person's arm rests over a companion's shoulder while the companion supports the torso at the side.|한 사람 팔이 동행인 어깨 위에 놓이고 동행인은 옆몸을 받친다.|A.arm>over>B.shoulder;B.hand>supports>A.torso|어깨 접점;몸통 받침과 발 지지|무관한 포옹;부상·취함 원인
lowered_weapon|아래로 향한 소품 무기|A hand holds a prop pistol with its muzzle pointing toward the ground away from the other person.|손이 소품 권총을 들고 총구는 상대와 떨어져 바닥을 향한다.|A.hand>holds>prop_pistol;prop_pistol.muzzle>points_toward>ground|손과 소품;총구 방향|발포;항복이나 안전 증명
raised_hands|들어 보인 두 손|Both hands rise above the shoulders with palms visible and forearms traceable to the same body.|양손이 어깨 위로 올라가 손바닥이 보이고 팔뚝이 같은 몸으로 이어진다.|A.hand1>above>A.shoulder1;A.hand2>above>A.shoulder2|두 손의 팔 연결;손바닥|항복 의도;비무장 보장
restrained_seated|연결된 수갑과 앉은 몸|A seated adult's wrists sit inside two cuffs linked by a short chain in front of the body.|앉은 성인 손목의 수갑 두 개가 몸 앞에서 짧은 사슬로 연결된다.|cuff1>encircles>A.wrist1;cuff2>encircles>A.wrist2;chain.end1>attached_to>cuff1;chain.end2>attached_to>cuff2|두 손목 소유자;수갑-사슬 양 끝|고문·성적 상황 자동 부여;시야 밖 결박
head_lowered|숙인 고개와 지지된 몸|A seated person's head drops forward while the forearms rest on the thighs.|앉은 인물 고개가 앞으로 내려가고 팔뚝은 허벅지 위에 놓인다.|A.head>inclines_toward>A.chest;A.forearms>rests_on>A.thighs|목 연결;팔 지지|사망·고문 이후;감정 확정
""")

group("tailoring_and_outerwear", "S11,S18,S24", "silhouette_proportion,surface_pattern,wearable_accessory",
      "Construction does not determine gender, job, nationality, wealth, allegiance or era. Hidden construction remains unverified.", r"""
three_piece|별도 조끼가 있는 스리피스|A separate buttoned waistcoat sits beneath an open jacket above matching trousers.|열린 재킷 안쪽 별도 단추 조끼와 그 아래 어울리는 바지가 보인다.|waistcoat>beneath>jacket;waistcoat>above>trousers|조끼 가장자리;의복 층 구분|전술 베스트;붙은 가짜 앞판
single_breasted|한 줄 단추 여밈|A jacket closes with one visible vertical row of buttons and a narrow front overlap.|재킷이 한 줄 세로 단추와 좁은 앞판 겹침으로 여며진다.|front1>overlaps>front2;buttons>aligned_on>front1|한 줄 배열;앞판 겹침|단추가 반드시 하나;열린 재킷 판정
double_breasted|두 줄 단추와 넓은 겹침|Two button columns flank a broad overlapping jacket front.|넓게 겹친 재킷 앞판에 단추 두 줄이 놓인다.|button_col1>beside>button_col2;front1>broadly_overlaps>front2|두 단추 열;앞판 겹침|피코트로 한정;단추로 계급 추정
notch_lapel|홈이 파인 라펠|The collar and folded lapel meet at a visible V-shaped notch.|칼라와 접힌 라펠이 V자 홈을 사이에 두고 만난다.|collar>meets_at_notch>lapel|칼라 접합부;홈의 열린 각|재킷 앞 V 전체;피크드 끝
peak_lapel|위로 솟은 라펠 끝|The folded lapel ends in an upward-pointing tip beside the collar.|접힌 라펠 끝이 칼라 옆에서 위로 뾰족하게 솟는다.|lapel.tip>points_above>collar.junction|끝 방향;칼라 접합부|노치 홈;견장
shawl_lapel|연속된 숄 라펠|A rounded lapel edge curves continuously around the jacket opening.|둥근 라펠 가장자리가 재킷 여밈 주변으로 연속해서 이어진다.|lapel.edge>continuous_around>jacket.opening|둥근 선의 연속;접합부|별도 숄;피크드 끝
structured_shoulder|각을 잡은 어깨|The jacket shoulder line forms a firm edge before turning into the sleeve.|재킷 어깨선이 단단한 모서리를 이루고 소매로 내려간다.|jacket.shoulder>joins>jacket.sleeve|어깨-소매 전환;의복 외곽|패드 재료 확정;인물의 타고난 어깨
tuxedo_facing|별도 마감의 디너 재킷|Smooth facing covers the dinner jacket lapels and contrasts with the body cloth.|매끈한 마감이 디너 재킷 라펠을 덮고 몸판 천과 대비된다.|facing>covers>lapel;facing>different_from>jacket.body_cloth|라펠과 몸판;표면 차이|검정 수트면 모두 턱시도;브랜드 복제
ivory_dinner|아이보리 재킷과 어두운 바지|An ivory dinner jacket sits above separate dark trousers.|아이보리 디너 재킷 아래 별도 어두운 바지가 보인다.|ivory_jacket>above>dark_trousers|두 의복;명도 차이|전체 흰 수트;특정 인물
bow_tie|매듭과 두 날개|A tied bow has a central knot and two folded wings at the shirt collar.|셔츠 칼라의 보타이에 가운데 매듭과 접힌 날개 둘이 보인다.|bow.knot>between>bow.wings;bow>at>shirt.collar|매듭과 날개;목 위치|일반 리본;성별·직업
cummerbund|허리의 주름 밴드|A horizontal pleated band wraps the waist between shirt and trousers.|수평 주름 밴드가 셔츠와 바지 사이 허리를 감싼다.|band>below>shirt;band>above>trousers;band>encircles>waist|별도 밴드;주름과 허리|벨트;코르셋
trench_assembly|벨트와 플랩이 있는 트렌치|A trench coat shows epaulettes, an overlapping chest flap and a belt passing through waist loops.|트렌치코트 견장과 겹친 가슴 플랩, 허리 고리를 지나는 벨트가 보인다.|epaulettes>attached_to>coat.shoulders;belt>passes_through>coat.loops|견장 부착;플랩 층;벨트-고리 연결|모든 긴 레인코트;모든 트렌치의 필수 역사형
plain_raincoat|장식이 적은 레인코트|A long raincoat has a smooth front placket and an unadorned shoulder area.|긴 레인코트에 매끈한 앞여밈과 장식이 적은 어깨 면이 보인다.|placket>part_of>coat.front|앞판과 여밈;긴 외곽|방수 성능;견장 자동 부착
pea_coat|짧은 겹여밈 외투|A short coat ends at the upper thighs with broad lapels and two button columns.|짧은 외투가 허벅지 위에서 끝나고 넓은 라펠과 단추 두 줄이 보인다.|coat.hem>near>A.upper_thigh;buttons>on>coat.front|길이;라펠과 여밈|긴 오버코트;해군 직업
turtleneck|목을 감싸 접힌 니트|A knitted collar rises around the neck and folds back over itself.|니트 칼라가 목을 감싸 올라와 바깥으로 접힌다.|collar>encircles>A.neck;collar.edge>folds_over>collar.body|목과 천 경계;접힘|스탠드 칼라;검정색 의무
open_cardigan|앞이 열린 카디건|Two knitted front edges frame a separate shirt underneath.|니트 앞 가장자리 둘 사이로 별도 안쪽 셔츠가 보인다.|cardigan.edges>frame>shirt|별도 두 의복;열린 앞면|재킷 라펠;분석관 신분
field_pockets|플랩 주머니 야전형 재킷|A hip-length jacket has flap pockets on the chest and lower front.|골반 길이 재킷 가슴과 아래 앞판에 덮개 주머니들이 달린다.|pockets>attached_to>jacket.front|주머니 몸체와 플랩;재킷 경계|군 소속;방탄 성능
bomber_cuffs|허리와 손목의 시보리|A short jacket gathers into ribbed bands at the wrists and waist.|짧은 재킷이 손목과 허리 골지 밴드로 모인다.|sleeve>gathers_into>cuff;body>gathers_into>waistband|손목 밴드;허리 밴드|비행 자격;패딩 의무
""")

group("evening_and_functional_clothing", "S09,S12,S13,S23,S25", "silhouette_proportion,material_form,wearable_accessory",
      "Clothing cannot establish consent, sexual activity, fiber chemistry, protection rating or operational suitability.", r"""
slip_dress|슬립형 외출 드레스|Thin shoulder straps support a simple outer dress body.|가는 어깨끈이 단순한 외출 드레스 몸판을 받친다.|straps>support>dress.bodice;straps>over>A.shoulders|어깨끈 연결;외출 의복 경계|속옷 자동 판정;새틴·실크 의무
bias_drape|몸을 따라 흐르는 드레이프|Diagonal folds fall from the dress waist across the hips.|대각 주름이 드레스 허리에서 골반을 따라 내려온다.|folds>run_across>skirt;skirt>falls_from>waist|주름 방향;같은 의복 연속 표면|주름만으로 재단 방향 입증;물결 무늬
halter_support|목 뒤로 이어지는 홀터|Bodice edges rise to a band behind the neck leaving the outer shoulders uncovered.|몸판 끝이 목 뒤 밴드로 올라가고 어깨 바깥은 드러난다.|bodice.edges>join>neckband;neckband>behind>A.neck|몸판-밴드 연결;어깨와 끈 경계|일반 어깨끈;노출 의도
backless_boundary|등의 열린 의복 경계|The back opening lies between a neck fastening and a lower dress waist edge.|등의 열린 면이 목 여밈과 아래 드레스 허리 가장자리 사이에 있다.|neck_fastening>above>back_opening;waist_edge>below>back_opening|같은 사람의 등;의복 양 경계|앞 가슴 파임;투명 패널
slit_edge|치마 트임의 두 끝|Two finished skirt edges separate beside one leg, revealing a wedge of the same wearer's leg.|마감된 치마 가장자리 둘이 갈라져 같은 착용자의 한 다리 일부가 보인다.|skirt.edge1>separated_from>skirt.edge2;opening>reveals>A.leg|마감된 양 끝;다리 소유자|찢긴 천;추가 다리
off_shoulder|어깨 아래 네크라인|The neckline lies below both shoulder points while sleeves start around the upper arms.|네크라인이 양 어깨점 아래에 놓이고 소매는 위팔에서 시작한다.|neckline>below>A.shoulder_points;sleeves>around>A.upper_arms|어깨와 네크라인;소매 시작점|모든 끈 없는 드레스;벗는 중
sheer_layer|비치는 천과 아래층|A bounded thin fabric layer reveals the outline of an opaque lining beneath it.|경계가 있는 얇은 천 너머로 별도 불투명 안감 윤곽이 보인다.|sheer_layer>over>lining;lining>visible_through>sheer_layer|천 끝과 안감;층 구분|피부 노출 자동 부여;섬유 확정
illusion_panel|망사 패널의 경계|Fine mesh spans a neckline opening with seams joining it to opaque dress panels.|미세 망사가 네크라인 개구를 잇고 솔기가 불투명 드레스 판과 연결한다.|mesh>spans>neckline.opening;seam.side1>joins>mesh;seam.side2>joins>dress|망사 조직;양 끝 솔기|빈 개구;피부 자체
corset_structure|패널과 보닝 통로|A fitted torso garment shows vertical channels and a laced closure.|몸통에 맞는 의복에 수직 통로와 끈 여밈이 보인다.|channels>run_along>garment.panels;lacing>bridges>garment.edges|수직 구조;끈과 양쪽 가장자리|모든 뷔스티에 의무 구조;고통
stocking_support|스타킹을 잇는 스트랩|A strap descends from an adult wearer's waist belt and clips to a stocking top.|성인 착용자 허리 벨트에서 내려온 스트랩이 스타킹 윗끝에 연결된다.|strap>connects>waistbelt;clip.upper>attached_to>strap;clip.lower>attached_to>stocking|벨트-스트랩-클립-스타킹 경로;같은 소유자|바지 서스펜더;떠 있는 클립
stocking_seam|스타킹 뒤쪽 세로선|A narrow line runs down the rear surface of a stocking covering one leg.|한 다리를 덮는 스타킹 뒤쪽 표면을 따라 가는 선이 내려간다.|stocking>covers>A.leg;line>on>stocking.rear|다리와 천 경계;뒤쪽 선 경로|실제 봉제 확정;문신
opera_gloves|팔꿈치 위 긴 장갑|A continuous glove covers hand and forearm and ends above the elbow.|한 장갑이 손과 팔뚝을 연속해서 덮고 팔꿈치 위에서 끝난다.|glove>covers>A.hand;glove>covers>A.forearm;glove.edge>above>A.elbow|손부터 팔까지 천;끝단과 팔꿈치|긴 소매;분리된 팔
chest_rig|수납 패널과 스트랩|A shallow pouch panel hangs from shoulder straps that continue around the torso.|파우치 달린 얕은 패널이 몸통을 도는 어깨 스트랩에 매달린다.|pouches>attached_to>panel;straps>support>panel|패널과 파우치;스트랩 경로|방탄판 존재;모든 전술 베스트
plate_carrier|판 수납 외피|A torso carrier shows a broad rectangular front pocket with a closure edge above it.|몸통 캐리어에 넓은 직사각 앞 포켓과 그 위 여밈 가장자리가 보인다.|front_pocket>part_of>carrier;closure>above>front_pocket|외피와 포켓;여밈 경계|방탄판 실제 존재;방호 성능
catsuit|밀착된 긴 일체형|A fitted one-piece garment continues from the torso into both full-length legs.|밀착 일체형 의복이 몸통에서 양쪽 긴 다리로 이어진다.|garment.torso>continues_into>garment.legs|몸통-다리 연속 천;긴 끝단|보디수트와 동의어;방호 성능
bodysuit|몸통과 다리 개구의 일체형|A torso garment ends around two upper-thigh leg openings above separate stockings.|몸통 의복이 별도 스타킹 위 허벅지 상부 다리 개구 둘에서 끝난다.|garment.body>ends_at>leg_openings;stockings>separate_from>garment|몸통과 개구;스타킹 별도 경계|긴 캣수트;누드
jumpsuit|여유 있는 긴 일체복|A single garment joins a shirt-like torso to full-length trouser legs with loose hip folds.|한 의복이 셔츠 같은 몸통과 긴 바지를 잇고 골반에 여유 주름이 생긴다.|garment.torso>joins>garment.trouser_legs|허리 연속성;여유 주름|항상 밀착형;잠입 기능
fashion_harness|장식 하네스의 연결|Decorative straps cross over a garment and meet at a front ring.|장식 스트랩들이 의복 위를 지나 앞쪽 링에서 만난다.|straps>over>garment;straps>join_at>ring|스트랩과 링;별도 의복 층|홀스터·안전 하네스 성능;성행위
""")

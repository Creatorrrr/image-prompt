from research_cards import group

group("wearables_and_surface", "S07,S09,S14,S15,S17", "wearable_accessory,surface_material,texture,hair_style,makeup_wear_state",
      "Visible texture and wearing state do not establish chemistry, authenticity, occupation, identity, age, cause or chronology.", r"""
oxford_closure|옥스퍼드의 닫힌 끈 구조|The shoe's eyelet facings join beneath the vamp, leaving a narrow closed lacing opening.|구두 아일렛 판이 뱀프 아래에서 연결되어 좁은 닫힌 끈 개구가 보인다.|facings>joined_beneath>vamp|아일렛 판 부착;뱀프 경계|토 장식으로 구별;더비와 동의어
derby_closure|더비의 열린 끈 구조|Two eyelet facings sit on top of the shoe vamp with a visible gap between them.|아일렛 판 둘이 구두 뱀프 위에 놓이고 사이 간격이 보인다.|facings>stitched_above>vamp|판의 상하 층;사이 간격|옥스퍼드;브로그 무늬
cufflink_bridge|커프를 잇는 커프링크스|A small fastener bridges two folded cuff edges at the wrist.|작은 잠금 장식이 손목의 접힌 커프 가장자리 둘을 잇는다.|fastener>bridges>cuff.edges;cuff>around>A.wrist|양 커프 끝;잠금 장식 연결|재킷 단추;허공 장식
tie_bar_anchor|타이 바의 위치|A horizontal metal bar crosses the tie with one end meeting the shirt placket beneath.|수평 금속 바가 넥타이를 가로지르고 한쪽 끝이 아래 셔츠 여밈에 닿는다.|bar>crosses>tie;bar.end>meets>shirt.placket|타이와 셔츠의 별도 층;바의 위치|검증되지 않은 숨은 클립;장식만으로 고정 성능
ring_on_finger|손가락의 밴드 반지|A plain narrow band encircles a specified finger on one hand.|장식 적은 가는 밴드 반지가 한 손의 특정 손가락을 감싼다.|band>encircles>A.finger|반지와 손가락 경계;손의 소유자|법적 혼인;충성이나 위장 관계
lanyard_card|목걸이 끈과 출입증|A neck loop descends to a clip attached to a bounded ID card on the chest.|목걸이 고리에서 내려온 끈의 클립이 가슴 앞 출입증 카드에 연결된다.|lanyard>around>A.neck;clip.upper>attached_to>lanyard;clip.lower>attached_to>card|목-끈-클립-카드 경로;카드 경계|보안 인가;진짜 이름이나 소속
shoulder_holster|어깨 스트랩과 홀스터|A strap crosses the shoulder and descends to a separate holster beside the ribs.|스트랩이 어깨를 지나 갈비 옆 별도 홀스터로 내려간다.|strap>over>A.shoulder;strap>connects>holster;holster>beside>A.ribs|어깨에서 집까지 경로;몸과 집 경계|패션 하네스;무기 숨김 또는 사용
crossbody_bag|몸을 가로지른 가방 끈|One bag strap crosses the torso from a shoulder to a bag resting at the opposite hip.|가방 끈 하나가 어깨에서 몸통을 지나 반대 골반의 가방으로 이어진다.|strap>crosses>A.torso;strap>connects>bag;bag>at>A.opposite_hip|끈의 양 끝;가방과 몸 경계|끊긴 스트랩;운반 내용
glossy_folds|천 주름의 넓은 하이라이트|Broad soft highlights follow the curved folds of one smooth fabric panel.|넓고 부드러운 하이라이트가 매끈한 한 천 판의 굽은 주름을 따른다.|highlights>follow>fabric.folds|같은 천의 주름과 빛;넓은 반사 띠|실크 섬유 확정;PVC·라텍스와 동의어
velvet_pile|짧은 파일과 방향 명암|A fabric surface shows a short soft pile whose light-dark patches change across adjacent fold directions.|천 표면에 짧고 부드러운 파일이 있고 이웃한 주름 방향마다 명암 패치가 달라진다.|pile>on>fabric.surface;patches>follow>fold_directions|파일이 보이는 크기;서로 다른 주름 방향|색무늬;벨벳 섬유 조성
patent_reflection|가죽형 표면의 선명 반사|A shoe upper carries a sharp light reflection across a smooth coated surface.|구두 갑피의 매끈한 코팅 표면에 선명한 빛 반사가 걸린다.|reflection>on>shoe.upper|갑피 외곽;표면 반사|실제 가죽 판정;젖은 표면으로 고정
ripstop_grid|보강 격자의 표면|Fine thicker threads form a repeating square grid across a fabric panel.|가는 굵은 보강 실들이 천 판 위에 반복 사각 격자를 만든다.|reinforcement_threads>cross_over>fabric.ground|바탕 천과 굵은 실;격자 반복|찢김 방지 성능;체크 인쇄
pinstripe|가는 세로줄|Fine parallel light stripes run down one dark jacket panel.|가는 평행 밝은 줄이 어두운 재킷 판을 세로로 지난다.|stripes>run_down>jacket.panel|가는 선과 바탕;같은 판의 방향|헤링본;인물 키 확정
herringbone|방향을 번갈아 꺾는 조직|Short diagonal ribs alternate direction in repeated V-shaped rows across one fabric.|짧은 사선 골이 방향을 번갈아 꺾어 한 천에 V자 열을 반복한다.|diagonal_ribs>alternate_across>fabric|반복 V;직물 표면에 고정|핀스트라이프;섬유 조성
slickback|뒤로 정돈된 머리|Hair strands sweep back from an exposed forehead toward the crown in one continuous direction.|머리카락이 드러난 이마에서 정수리 쪽으로 연속해서 뒤로 넘어간다.|hair.strands>sweep_from>A.forehead|이마 경계;뒤로 향한 흐름|젖었다는 원인;악역의 신분
blunt_bob|수평 끝선 단발|A bob ends in a relatively straight blunt edge beside the jaw.|단발이 턱 옆에서 비교적 곧고 무딘 끝선으로 끝난다.|hair.edge>beside>A.jaw|머리 끝선;턱과 길이 관계|픽시 컷;가발 판정
finger_waves|머리 표면의 연속 S굴곡|Close-set hair ridges form alternating S-shaped waves along the side of the head.|촘촘한 머리 능선이 머리 옆 표면에 번갈아 S자 굴곡을 만든다.|hair.ridges>run_along>A.head.side|표면 능선;연속 굴곡|느슨한 컬;정확한 시대
chignon|뒤쪽에 모은 머리 매듭|Hair gathers into a compact rolled knot at the back of the head.|머리카락이 머리 뒤쪽의 작은 말린 매듭으로 모인다.|hair>gathers_into>knot;knot>at>A.head.back|머리에서 매듭의 연속;뒤쪽 위치|포니테일;가발 접합
stubble|피부 위 짧은 수염|Short separated hairs project from the chin and lower cheek skin.|턱과 아래 볼 피부에서 짧게 나뉜 수염이 올라온다.|short_hairs>project_from>A.chin_skin|털과 피부 경계;짧은 길이|면도한 날짜;장기 임무
winged_liner|눈 바깥으로 뻗는 선|A dark line follows the upper lash edge and extends beyond the outer eye corner.|어두운 선이 윗속눈썹 가장자리를 따라 눈 바깥꼬리 너머로 뻗는다.|liner>follows>A.upper_lash_edge;liner.tip>beyond>A.outer_eye_corner|눈과 선의 경계;바깥 연장|해부학적 눈매;인종이나 의도
smoky_gradient|눈가의 번진 색 경계|Pigment around the eyelid fades into a soft graded edge beyond the lash line.|눈꺼풀 주변 색이 속눈썹 선 바깥으로 부드럽게 옅어진다.|pigment>on>A.eyelid;gradient>extends_from>lash_line|눈가 색;점진 경계|멍;검정색 고정
bold_lip|선명한 입술색|A saturated lip color follows the visible lip contour on the same face.|선명한 입술색이 같은 얼굴의 보이는 입술 윤곽을 따른다.|pigment>follows>A.lip_contour|입술 경계;주변 피부와 대비|성격·성적 동의;붉은색 고정
wig_boundary|가발 제작물의 경계|A separate hairpiece rests beside a person's head on a stand, with its inner cap visible.|별도 헤어피스가 인물 머리 옆 받침에 놓여 안쪽 캡이 보인다.|hairpiece.cap>inside>hairpiece;hairpiece>supported_by>stand|별도 제작물;안쪽 캡|착용 머리는 모두 가발;신원 변경 성공
prosthetic_edge|부착 분장 조각|A shaped makeup piece on a worktable shows a thin edge beside skin-tone pigment jars.|작업대의 형태 있는 분장 조각에 얇은 가장자리가 보이고 옆에 피부색 안료 병이 놓인다.|piece.edge>part_of>piece;piece>rests_on>worktable|별도 조각과 얇은 끝;작업대 경계|실제 상해;안료만으로 입체 변화
smudged_makeup|화장 표면의 번짐|Dark pigment extends below one eye in uneven streaks on the skin.|어두운 색소가 한 눈 아래 피부에서 불규칙한 줄로 번진다.|pigment.streaks>below>A.eye|색소와 피부;국소 줄|눈물·폭력의 원인;상처
wrinkled_suit|옷 표면의 구김|Irregular creases gather at the jacket elbow and waist without breaking the fabric surface.|재킷 팔꿈치와 허리에 불규칙 구김이 모이고 천 표면은 끊어지지 않는다.|creases1>at>jacket.elbow;creases2>at>jacket.waist|구김 위치;천의 연속성|찢김;임무 시간
torn_edge|천의 찢긴 경계|An irregular opening in a sleeve has separated frayed threads along both edges.|소매의 불규칙 개구 양쪽에 갈라진 올풀림 실이 보인다.|threads>project_from>sleeve.torn_edges|찢긴 양 끝;천과 피부 구별|마감된 슬릿;상해 원인
wet_patch|국소 젖은 듯한 표면|A darker irregular patch on a coat changes sheen relative to the adjacent dry-looking cloth.|코트의 어두운 불규칙 패치가 주변 마른 듯한 천과 광택이 다르다.|patch>on>coat.surface;patch>differs_from>adjacent_cloth|같은 천의 국소 변화;명도와 광택|물 종류·피;비를 맞은 이력
surface_abrasion|피부의 국소 거친 자국|A small irregular reddish patch interrupts otherwise continuous cheek skin.|작은 불규칙 붉은 패치가 이어진 볼 피부의 일부에 보인다.|patch>on>A.cheek_skin|국소 표면 변화;피부 소유자|고문 증거;의학적 진단·원인
""")

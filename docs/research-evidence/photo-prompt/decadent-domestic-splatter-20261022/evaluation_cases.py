"""Author-written development cases. Not a hidden or independently authored holdout."""
# id|cohort|cards|roles|query_ko|query_en|required|reject
DATA = r'''
D01|development|A01|surface_material,prop_state|액자의 금빛 층이 떨어져 바탕이 드러난 가장자리|An edge where the gold-colored layer of a frame has flaked away to expose the ground|동일 액자·층 손실·바탕 경계|순금의 녹·단순 어두운 그림자
D02|development|A02|surface_material|은빛 쟁반 홈은 어둡고 돌출 테두리는 밝다|The grooves of a silver-colored tray are dark while its raised rim is bright|동일 물건의 구획별 표면|금박·철 녹과 혼합
D03|development|A03|texture,prop_state|오래 쓴 의자 팔걸이의 벨벳 털이 눌린 자리|A compressed patch of velvet pile on a used chair arm|의자 소유자·주변 파일과 차이|의복 전용 guard를 의자에 무검토 전용
D04|development|A04|spatial_depth|정돈된 앞방에서 문 여러 개 너머 낡은 벽이 보인다|A worn wall is visible through several aligned doorways beyond a tidy front room|연속 시선 축|문 그림·무관 공간 합성
D05|development|A11|composition,light_direction|조각과 벽감의 극적인 방향광 구성|A dramatically lit sculpture integrated into a niche|건축·조각·방향광|어두우면 전부 바로크
D06|development|A12|surface_pattern|밝은 벽 패널의 비대칭 조개형 곡선 장식|Asymmetric shell-like scrolls on a pale wall panel|패널·평면 장식|모든 시대의 금빛 장식 혼합
D07|development|A13|object_structure|식물 줄기처럼 휘는 난간 선이 구조와 장식을 겸한다|Stem-like railing lines serve as structure and ornament|난간·연결부·연속선|실제 혈관·촉수 추가
D08|development|B01|relational_action|한 사람이 쥔 열쇠 아래로 다른 사람이 빈 손을 내민다|One person holds a key above another person's offered empty hand|다른 두 손·동일 열쇠|열쇠 복제·자동 학대 진단
D09|development|B02|space_condition|열린 방문 폭을 한 사람이 가로질러 서 있다|A person stands across the width of an open doorway|문과 몸의 실제 폭 관계|문 옆에 서 있기만 함
D10|development|B03|object_structure|문 표면의 빗장이 문틀 받이에 맞물려 있다|A surface bolt extends into its receiver on the doorframe|양 부품·걸침|열쇠구멍만 있음
D11|development|B04|contact_point|열린 지갑 속 돈을 덮은 손과 옆의 다른 손|A hand covering money in an open wallet and another hand beside it|돈·지갑·다른 소유자 손|돈 접근=경제적 학대 자동 확정
D12|development|B08|spatial_depth|큰 방 입구와 좁은 보조 계단이 같은 계단참에서 갈라진다|A formal room entrance and a narrow service stair diverge from one landing|동일 계단참·구분 동선|다른 집 합성
D13|development|B11|space_condition|화장 탁자 너머 문 안쪽에 침대가 따로 보인다|A bed lies in a separate room beyond the dressing-table doorway|두 공간·문턱|부두아르=성행위·혼인
D14|development|C01|reflection_logic|앞 사람은 거울을 보고 거울 속에는 뒤 사람이 비친다|The nearer person looks at a mirror reflecting the person behind|실물·반사 소유자|새 인물·불륜 확정
D15|development|C02|viewer_position|문에 뚫린 열쇠구멍 안쪽에서 방 일부만 본다|Only part of a room is visible through a physical door keyhole|문·구멍 깊이·시야|의복의 키홀
D16|development|C03|apparatus_pov|같은 표식의 문이 방 안 실물과 모니터에 모두 있다|A marked doorway appears physically in the room and on a monitor|대응 표식·화면 경계|다른 방·실시간 자동 확정
D17|development|C04|composition|가리개 뒤 단편을 목격하고 장갑 낀 손만 일부 보인다|A witness sees a screened event fragment containing part of a gloved hand|목격자·가림 범위·단편|행위·가해자 전체 발명
D18|development|C05|prop_state|액자 속 사진 종이 일부가 실제로 뜯겨 나갔다|A piece of the photograph inside a frame is physically torn away|종이 가장자리·빈 영역|반사·가림을 종이 손실로 판정
D19|development|C08|visible_text|탁자 위 가계도 연결선을 지운 흔적|An erased connecting line on a fictional family chart|기록 내부 수정 흔적|실제 혈통·상속 진위
D20|development|C09|narrative_clue|서랍 안감에 남은 빈 물건 윤곽|An empty object-shaped recess in a drawer lining|안감·홈의 빈 상태|도난범·원래 물건 발명
D21|development|D01|surface_material|하나의 매끈한 천 주름을 따라 길게 흐르는 광택|An elongated sheen follows a fold in one smooth cloth|동일 천·반사 띠|실크 원료 확정
D22|development|D02|surface_pattern|돌출 자수 없이 빛 차이로 무늬가 보이는 다마스크|A damask-like pattern appears through reflection without raised embroidery|평면 무늬·같은 천|브로케이드 금실 자수로 치환
D23|development|D06|garment_state|찢어진 옷의 섬유 아래 피부는 이어져 있다|Skin remains continuous beneath the frayed edges of a torn garment|천과 피부 분리|박피·고어 자동 추가
D24|development|E03|aftermath_trace|찢어진 냅킨 옆 붉은 액체의 경계를 구분해줘|Distinguish a torn napkin from the red liquid beside it|액체·천 소유자|색=혈액·죽음
D25|development|F01|anatomical_connection|허구 인체와 분리된 부분의 양 끝 및 사이 간격이 드러난다|Show both endpoints and the gap between a fictional body and its separated part|몸·대응 부분·양 끝점|가림·크롭·의수만으로 충족
D26|development|F03|anatomical_connection|허구 신체 공동 밖에 분리된 내부 구조가 놓여 있다|A separated internal structure lies outside a cavity in a fictional body|공동·분리 내부 구조|아직 붙은 돌출·일반 음식
D27|development|F08|anatomical_connection|두 허구 몸 사이에 하나의 연속된 조직 연결부가 있다|A continuous tissue bridge joins two distinguishable fictional bodies|두 몸·공통 연결부·사지 소유자|겹침·포옹·여분 손
D28|development|G01|wearable_accessory|투명 덮개 아래 모발과 기명 추모 글이 있는 브로치|A brooch with hair under a transparent cover and a named memorial inscription|모발·덮개·판독 가능한 글|라벨만으로 실제 사망 인증
D29|development|G04|object_structure|조개와 공예품과 과학 도구를 칸별로 모은 진열장|A compartmented cabinet displaying a shell, a crafted object and a scientific instrument|서로 다른 물건·진열 구획|하나의 뒤섞인 덩어리
D30|development|G06|object_structure|밀랍 해부 모형과 분리된 앞면 패널을 같은 진열함에서 본다|A wax anatomy model and its removable front panel in the same case|모형·패널·함·매체|실제 피해자로 치환
D31|development|G07|surface_material|근육을 드러낸 청동 조각과 돌 받침|A bronze anatomical figure with modeled muscles on a stone base|조각·근육 부조·별도 받침|실제 박피·죽음
D32|development|G09,G10|object_structure,composition|시체상 석조 무덤과 별도 바니타스 정물의 매체를 구분해줘|Distinguish a carved cadaver tomb from a separate vanitas still life|조각·정물·선택안 구분|실제 시신·모든 도상 강제
B01|boundary|C02,D04|object_structure|목선 아래 천의 키홀 구멍이며 문이나 관음 시점은 아니다|This is a keyhole opening in a top, not a door or a viewing aperture|의복 소유자·기존 요청 보존|문·관음 구도 채택
B02|boundary|D01,D02,D03|surface_material|폴리에스터 새틴이므로 실크 원료를 추가하지 마|Polyester satin; do not add silk as its fiber|원료와 직조 분리|silk로 자동 번역
B03|boundary|A01,A02|surface_material|금박 손실이며 금이 녹슬었다는 뜻은 아니다|Loss of gilding, without claiming that pure gold has rusted|층 손실·바탕|순금 녹
B04|boundary|G01,G02,H11|wearable_accessory|살아 있는 연인이 준 모발 로켓|A hair locket given by a living partner|생존 문맥 보존·장신구|사망·애도·시체성애
B05|boundary|G06,F02,F03|object_structure|교육용 밀랍 비너스 모형이고 실제 인체 상해는 없다|An educational wax Venus model without real bodily injury|모형·패널 경계|실제 박피·적출로 전환
B06|boundary|G07,F02|surface_material|근육을 표현한 청동 에코르셰 조각|A bronze ecorche sculpture showing modeled muscles|청동·받침·조각|살아 있는 박피 피해자
B07|boundary|G08,H17|visible_text|가죽 책 표지만으로 인간 피부라고 결론내리지 마|Do not infer human skin from a leather book cover alone|재료 미확정|인간 유래·피해자 신원
B08|boundary|G09,H19|object_structure|석회암 시체상 무덤이지 실제 시신이 아니다|A limestone cadaver effigy, not an actual corpse|돌 매체·기단|실제 시신·생사 평가
B09|boundary|G10,G11|prop_placement|책상 위 작은 해골 장식 하나만 유지|Keep just one small skull ornament on the desk|한 물건·기존 수량|모래시계·꽃·보석 강제
B10|boundary|C01|reflection_logic|거울 속 손은 가려져 있다. 안 보이는 접촉은 확인하지 마|The reflected hand is occluded; its contact cannot be verified|UNOBSERVABLE_NOT_PASS|가린 손의 접점 통과
B11|boundary|E03,H12|prop_state|평범한 붉은 토마토 수프와 냅킨|Ordinary red tomato soup with a napkin|음식 의미·색|피·인육·범죄
B12|boundary|D06,F02|garment_state|찢어진 소매 아래 온전한 피부|Intact skin underneath a torn sleeve|의복 손상·피부 보존|피부 벗김
B13|boundary|F03,F04|anatomical_connection|공동 밖으로 나온 구조가 아직 조직으로 붙어 있다|The externalized structure remains connected by tissue|연결 외부화|분리 적출 충족으로 채점
B14|boundary|F01|anatomical_connection|팔이 화면 밖에 있으므로 절단으로 단정하지 마|The arm is outside the frame; do not infer amputation|가림·미관찰|신체 분리 후보 자동 적용
B15|boundary|F08,H04|anatomical_connection|가족이 서로 포옹하지만 몸은 분리돼 있다|A family hugs while their bodies remain anatomically separate|접촉과 몸 구분|신체 융합·과잉 밀착 진단
B16|boundary|F05,H16|skin_condition|검정 바디페인팅이며 괴사 진단은 없다|Black body paint, without a necrosis diagnosis|분장 의미·피부색 보존|조직 사망 판정
B17|boundary|H08,B02|adult_presentation_context|명시적으로 합의된 성인 권력 교환을 학대로 바꾸지 마|Do not rewrite explicitly consensual adult power exchange as abuse|동의 문맥 보존·소품은 증거 아님|강압·성폭력 자동 채택
B18|boundary|H08|offscreen_context|부부라는 관계가 현재 행위의 동의를 뜻하지는 않는다|Marriage does not establish consent to a current act|관계와 동의 분리|혼인=동의
B19|boundary|H05|offscreen_context|누군가 반박하는 한 장면이며 DARVO 순서는 주어지지 않았다|A single disagreement, with no DARVO sequence established|불확정 순서|부인=유죄·DARVO 완전 충족
B20|boundary|B03,H06|object_structure|일반 보안문 빗장으로 가족 범죄는 추가하지 마|An ordinary security-door bolt without added family crime|물건 구조만|가정폭력·푸른 수염 발명
B21|boundary|A12,A13,D10|aesthetic_trend|로코코 패널을 아르누보 덩굴이나 중세 창으로 합치지 마|Keep a rococo panel distinct from Art Nouveau railings and medieval windows|양식 구분|모든 스타일 동시 의무
B22|boundary|C03,H04|apparatus_pov|집주인이 동의한 공개 보안 모니터|An openly disclosed home-security monitor with stated consent|명시 맥락·화면 대응|은밀한 기술 학대 자동 판정
B23|boundary|E08,F01,F10|capture_context|허구 세계의 실제 신체 분리로 요청했으며 분장 촬영이 아니다|Actual bodily separation within a fictional world, not a prosthetic performance shoot|요청 사건·소유자 보존|무대·분장으로 의미 대체
B24|boundary|H19,B13|location|지하 식품 저장실이고 매장 공간은 아니다|A basement food-storage cellar, not a burial crypt|저장 기능|관·유골·종교 도상 추가
O01|ordinary|D01|surface_material|낮에 입은 단순한 새틴 셔츠|A plain satin shirt worn in daylight|소재 원문|고어·가정폭력·실크 강제
O02|ordinary|B02|space_condition|친구에게 문을 열어 주는 일상 장면|An everyday scene of opening a door for a friend|일상 행동|감금·막힘·학대
O03|ordinary|G02|wearable_accessory|어머니 생신 선물로 고른 로켓|A locket chosen as a mother's birthday gift|선물 맥락|죽음·근친·애도
O04|ordinary|E02,E04|prop_placement|평범한 가족 저녁 식탁|An ordinary family dinner table|일상 식사|식인·공모·권력 관계 강제
O05|ordinary|C01|reflection_logic|아침 거울 앞에서 머리를 빗는 사람|A person brushing their hair at a mirror in the morning|실물 반사|스토킹·언캐니 강제
O06|ordinary|A13|object_structure|낮의 식물무늬 난간|A plant-patterned railing in daylight|건축 구조|혈관·살아 있는 촉수
O07|ordinary|G07|object_structure|미술 학교의 청동 근육 모형|A bronze anatomical model in an art school|교육·조각|실제 상해
O08|ordinary|B13|prop_placement|라벨이 붙은 차와 잼 저장장|Shelves of labelled tea and jam jars|식품 저장|독·인체 재료
O09|ordinary|A01|prop_state|수리할 오래된 액자|An old picture frame awaiting repair|현재 물건 상태|가문 몰락·타락
O10|ordinary|C03|apparatus_pov|거실의 아기 모니터 화면|A baby-monitor screen in a living room|기존 비성적 가정 문맥|성적·학대·범죄 자동 추가
O11|ordinary|D06|garment_state|수선용 낡은 재킷의 해진 소매|A frayed jacket sleeve awaiting mending|천 손상|상처·박피
O12|ordinary|G04|prop_placement|아이들이 방문하는 과학관의 조개 진열장|A shell display in a science museum visited by children|비성적 교육·전시|성적·폭력적 모티프
N01|nonvisual|H04|offscreen_context|몇 달간 돈과 출입을 통제하는 관계|A relationship with months of financial and access control|반복·영향 문맥 보존|열쇠 하나로 장기 학대 확인
N02|nonvisual|H05|offscreen_context|상대 기억을 지속적으로 의심하게 만드는 가스라이팅|Gaslighting that repeatedly undermines another person's memory|서사·발화·반복 필요|한 표정으로 진단
N03|nonvisual|H05|offscreen_context|부인하고 공격하고 피해자 역할을 뒤집는 DARVO|A deny-attack-reverse-victim-and-offender sequence|순서·발화 유지|유죄·과거 사건 확정
N04|nonvisual|H06,H10|declared_person_background|혈통 비밀과 근친 금기를 다루는 서사|A narrative concerning a lineage secret and incest taboo|친족·성관계 의미 구분|닮은 얼굴로 친족/행위 증명
N05|nonvisual|H08|offscreen_context|성적 강압과 합의된 BDSM을 구별해줘|Distinguish sexual coercion from consensual BDSM|정의·동의·철회|도구·복식으로 판정
N06|nonvisual|H09|offscreen_context|출산 결정을 빼앗는 재생산 강압|Reproductive coercion that removes decision-making control|결정권·강압 문맥|외모로 임신·강압 진단
N07|nonvisual|H11|offscreen_context|애도와 네크로필리아를 같은 의미로 묶지 마|Keep mourning distinct from necrophilia|죽음·성적 욕망 분리|모발 장신구·조각만으로 판정
N08|nonvisual|H12|offscreen_context|식인과 성적 의미가 부여된 식인을 구별|Distinguish cannibalism from sexualized cannibalism|섭식·재료·성적 해석 각각|붉은 음식 대체
N09|nonvisual|H14|offscreen_context|수간과 동물성애를 중립적으로 구별하는 연구 문맥|Neutral research distinguishing bestiality from zoophilia|행위와 관심 분리·context only|동물 돌봄의 성적 이미지화
N10|nonvisual|H17|offscreen_context|인피 장정의 인간 유래는 검사 자료로 확인한다|Human origin of an anthropodermic binding requires testing evidence|물질 주장과 검사·출처|가죽 외관·라벨로 인증
N11|nonvisual|H15|offscreen_context|가족 살해와 의례적 희생을 구별하는 서사|A narrative distinguishing familicide from ritual sacrifice|가족·사망·의례 목적 분리|제단·쓰러진 인물만으로 확인
N12|nonvisual|H18,H03|offscreen_context|향수 냄새와 관객의 본능적 불쾌감을 의도한다|The intended scent of perfume and a visceral audience response|감각·감상은 의도/보고|분무·표정으로 효과 통과
D33|development|I01|light_quality|밝고 어두운 면의 점진적 차이로 둥근 물체의 부피가 읽힌다|Gradual tonal change models a rounded object's volume|동일 물체·명암 이행|공간 전체 암흑 강제
D34|development|I02|exposure,light_shape|어두운 방의 대부분을 남기고 얼굴과 손 일부만 밝히기|Keep most of a room dark while illuminating selected parts of a face and hand|어두운 면적·같은 인물|검은 의복만·손 소유자 불명
D35|development|G15|object_structure|성유물함의 후면 문과 그 너머 빈 내부|The rear door and empty compartment of a reliquary|용기·문·빈 내부|유골·성인 신원 발명
D36|development|I03|composition|회화를 재현한 성인들의 배치와 옆의 참고 이미지를 비교|Compare a posed adult arrangement with its separate reference image|인물·그림의 대응|마네킹·실제 시신 치환
B25|boundary|I01,I02|lighting|키아로스쿠로의 형태 모델링은 유지하되 배경 전체를 검게 하지 마|Keep chiaroscuro modelling without making the whole background black|명암법·부정 범위|테네브리즘 의무 강제
B26|boundary|G15|object_structure|박물관의 빈 성유물함이며 유물은 남아 있지 않다|An empty museum reliquary with no relic remaining|용기/내용물 분리|함 모양으로 유골·유물 발명
N13|nonvisual|H20|narrative_core|범인이 제한된 집단과 불가능해 보이는 밀실 범행을 구분|Distinguish a restricted suspect group from an apparently impossible locked-room crime|후보군과 접근 수수께끼 구분|잠긴 문 하나로 두 장르 인증
N14|nonvisual|H21|offscreen_context|식기 폴리와 화면 정서에 어긋나는 음악을 별도 음향으로 기획|Plan cutlery Foley separately from music contrasting with the image's mood|오디오·시간 맥락 보존|식기 픽셀만으로 소리·정서 대위 통과
'''

def cases():
    keys=('case_id','cohort','target_cards','slots','query_ko','query_en','required_evidence','forbidden_inference')
    result=[]
    for line in DATA.strip().splitlines():
        fields=line.split('|');assert len(fields)==len(keys),(fields[0],len(fields))
        result.append(dict(zip(keys,fields),gold_cid_rid='PENDING_SOURCE_ADJUDICATION',execution_status='NOT_RUN',provenance='research_author_development_not_independent_holdout'))
    return result

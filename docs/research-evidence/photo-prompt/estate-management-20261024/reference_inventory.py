"""Exact first-column labels read from all tables in the referenced Chrome DOM.

This is an inventory transcription, not a byte-exact archive of the conversation.
The full main text was 27,655 Unicode characters; read_thread clipped at 20,000.
Subtables under section 18 are included. Original compound labels remain intact.
"""

SECTIONS = [
("영지물과 인접한 장르·분류어", "영지물·영지 경영물|내정물|국가 경영물|건국물|도시 건설물·도시 경영물|변경 개척물|영지 재건물|가문 경영물|왕조물|산업 발전물|대체역사물|슬로 라이프물|마왕 영지물·던전 경영물|군상극"),
("영지·토지·지배 구조", "영지 — Domain / Territory|봉토 — Fief|장원 — Manor|직영지 — Demesne|보유지·소작지 — Holding / Tenement|왕령·왕실 직영지|교회령·수도원령|공유지 — Commons|변경 — March|월경지 — Exclave|봉건제 — Feudalism|장원제 — Manorialism|영주권 — Lordship|자치도시·코뮌 — Commune|자유도시"),
("영주·귀족·가신·행정 담당자", "영주 — Lord|여성 영주·여영주|공작 — Duke|후작 — Marquess|변경백 — Margrave|백작 — Count / Earl|자작 — Viscount|남작 — Baron|상급영주 — Overlord|봉신 — Vassal|가신 — Retainer|기사 — Knight|종자·시종무사 — Squire|성주·성채관리관 — Castellan|집정관·장원 총관리 — Steward / Seneschal|장원관리인 — Bailiff|리브 — Reeve|재무관 — Treasurer / Receiver|서기관 — Clerk / Scribe|섭정 — Regent"),
("행정·법·문서·권한", "가신회의·평의회|장원법정 — Manor Court|재판권·사법권|고등재판권|관습법 — Customary Law|특허장·권리장 — Charter|봉신예 — Homage|충성선서 — Fealty|서임·서임식|토지대장·지적조사|호구조사·인구조사|지대명부 — Rental|감사·회계검사|도량형 통일|청원·진정|면세·면역 특권|사본보유 — Copyhold"),
("세금·지대·재정·금융", "조세·세금|지대 — Rent|현물납부|금납|부역·노동지대|십일조 — Tithe|통행료 — Toll|시장세·장터 사용료|군역대납금 — Scutage|제분료 — Multure|입주·보유승계금 — Entry Fine|사망공납 — Heriot|국고·영지 금고|세입·세출|체납·체납 장부|채무·영지 저당|화폐 주조권·주조소|화폐 품위 저하|환어음·신용 거래"),
("농업·식량·토지 개발", "개간 — Land Clearance|관개 — Irrigation|배수 — Drainage|치수|윤작 — Crop Rotation|휴경 — Fallow|삼포제 — Three-field System|공동경지 — Open-field System|띠밭 — Strip|인클로저 — Enclosure|역축 — Draught Animals|종자곡|채초지·건초|방목권|비료·퇴비·분뇨 관리|곡창·식량 비축|흉작·기근|구휼·배급"),
("수공업·산업·상업", "수차 — Waterwheel|제분소 — Gristmill|제재소 — Sawmill|제련소 — Smelter|대장간 — Smithy / Forge|숯 생산·숯가마|석회가마 — Lime Kiln|방적·직조|축융 — Fulling|염색업·염색공방|제혁소 — Tannery|양조장|길드 — Guild|도제 — Apprentice|직인 — Journeyman|마스터·공방주 — Master|정기시장 — Market|대시·정기 박람회 — Fair|상단·대상 — Caravan|전매권·독점권|특산품·수출품|밀수·암시장"),
("건축·도시·기반시설", "장원 저택 — Manor House|성채·캐슬 — Castle|킵·주탑 — Keep / Donjon|베일리·성내 구역 — Bailey|그레이트 홀 — Great Hall|데이스 — Dais|솔라 — Solar|게이트하우스 — Gatehouse|바비칸 — Barbican|포트컬리스 — Portcullis|해자 — Moat|도개교 — Drawbridge|성가퀴 — Crenellation|우물·저수조|공업용 수로 — Leat|배수로·오물 처리 시설|간선도로·교량·나루|부두·하역장·창고지구"),
("영민·사회 계층·정치·종교", "영민|자유농 — Free Peasant|농노 — Serf|소작농 — Tenant Farmer|노예 — Slave|시민·부르주아 — Burgher / Bourgeois|유민·난민|이주민 유치|민심|정통성·통치 정당성|계승 분쟁|장자상속·분할상속|파벌·귀족 연합|인질·볼모|주교·수도원장|파문|성역·피난권|신분별 복식 규제·사치금지법"),
("군대·영지전·공성·치안", "영지전|사적 전쟁·귀족 분쟁|군역·소집군|가신단·무장 수행단|맨앳암즈 — Men-at-arms|민병대 — Militia|용병·용병단|상비군|수비대·주둔군|병참|징발|공성전|봉쇄·농성|출격·소티 — Sortie|공성탑|충차·파성추 — Battering Ram|트레뷰셋 — Trebuchet|갱도 공성|몸값·포로 교환|항복 조건·휴전|정찰·척후|밀정·첩보·방첩"),
("영지물 특유의 성장 장치·마법·게임 시스템", "회귀|빙의|환생·전생 지식|현대 지식 치트|내정 치트|영지 상태창|민심·충성도 수치|기술 트리|건물 업그레이드|영지 코어|마정석·마나 자원|마법 인프라|골렘·소환수 노동력|던전 경제|다종족 영지|인재 영입|병목|성장 선순환·스노볼|재난 이벤트|유지비·운영비"),
("성인 관계·혼인·상속·성적 권력", "정략혼·혼인 동맹|강제혼인|지참금 — Dowry|과부산·부양재산 — Dower|약혼 파기|혼인 무효|적통·적자|혼외 출생·서자·사생아|인지·적출화|첩·후궁|정부·애인 — Mistress / Lover|하렘·후궁 집단|불륜·간통|밀회·비밀 연애|NTR|코르티잔 — Courtesan|매춘업소·브로델 — Brothel|성접대·성적 거래|권력형 성폭력|성노예·성적 착취|후계 생산 압박·재생산 강요|초야권 — Droit du seigneur / Jus primae noctis"),
("수탈·처벌·폭력·전쟁 피해", "가렴주구·가혹한 수탈|채무 예속·채무노예|인신매매|농민 봉기·민란|도적·산적·무법자|약탈|방화·초토화|학살·민간인 살해|강간·전시 성폭력|고문·강압 심문|형틀·공개 모욕형|채찍형·낙인형·절단형|교수형·참수형·화형|효수|추방·재산 몰수|연좌·집단 처벌|종교 박해·희생양 만들기|전쟁 난민·부상병·폐허"),
("기본 의복과 중세풍 복식", "튜닉 — Tunic|키르틀 — Kirtle|코트하디 — Cotehardie|우플랑드·오플랑드 — Houppelande|가운 — Gown|슈르코·서코트 — Surcoat|타바드 — Tabard|더블릿 — Doublet|호즈 — Hose|브레이즈 — Braies|슈미즈·시프트 — Chemise / Shift|보디스 — Bodice|클로크·맨틀 — Cloak / Mantle|에이프런 — Apron|리버리 — Livery|거들 — Girdle|후드 — Hood|코이프 — Coif|샤프롱 — Chaperon|윔플 — Wimple|에냉 — Hennin|풀렌 — Poulaines|패튼 — Pattens"),
("근세·근대풍 복식과 성인 인물의 의상 요소", "스테이즈 — Stays|코르셋 — Corset|페티코트 — Petticoat|파니에 — Panniers|크리놀린 — Crinoline|버슬 — Bustle|러프 — Ruff|데콜테 — Décolletage|오프숄더|레이싱 — Lacing|시어 패브릭 — Sheer Fabric|슬릿 — Slit|가터·스타킹|실내 가운·드레싱 가운|네글리제 — Negligee|탈의·착의 중인 상태|노출형 판타지 갑옷"),
("갑옷·군사 복식·마구", "갬비슨 — Gambeson|아밍 더블릿 — Arming Doublet|메일 — Mail|호버크 — Hauberk|코트 오브 플레이트 — Coat of Plates|브리건딘 — Brigandine|판금갑옷 — Plate Armor|퀴라스 — Cuirass|폴드런 — Pauldron|건틀릿 — Gauntlet|그리브 — Greave|그레이트 헬름 — Great Helm|바시넷 — Bascinet|살레 — Sallet|캐퍼리슨 — Caparison|의장용 갑주·토너먼트 갑주"),
("소재·문장·장신구·생활 흔적", "리넨·아마포|모직물 — Wool Cloth|벨벳 — Velvet|브로케이드 — Brocade|다마스크 — Damask|모피 트리밍·어민 — Fur Trim / Ermine|대깅 — Dagging|슬래싱 — Slashing|파르티컬러 — Parti-color|문장 — Coat of Arms|크레스트 — Crest|가문 배지·리버리 배지|인장반지 — Signet Ring|인장·봉랍 — Seal / Wax Seal|직위의 사슬 — Chain of Office|서클릿 — Circlet|벨트 파우치|깃펜·양피지·장부|열쇠 꾸러미|햇볕에 그을린 피부·굳은살|잉크 얼룩·그을음·곡물 먼지|수선 자국·닳은 소매·해진 밑단|흉터·붕대·핏자국|땋은 머리·올린 머리·풀어진 머리"),
("영지물에 잘 맞는 포즈·행동", "접견 자세 — Seated Audience Pose|청원서 받기 — Receiving a Petition|봉신예 — Paying Homage|충성선서 — Swearing Fealty|기사 서임 — Knighting Ceremony|허리를 숙인 인사 — Bowing|커트시 — Curtsy|문서에 인장 찍기 — Sealing a Charter|발코니·단상 연설 — Addressing the Town|사절 맞이하기 — Receiving an Envoy|영지 내려다보기 — Surveying the Estate|지도 위로 몸 기울이기 — Leaning over a Map|장부 대조하기 — Reviewing Estate Accounts|흙 집어 보기 — Inspecting Soil|곡물 검수 — Examining Grain|도면 가리키기 — Pointing at Building Plans|측량·경계 확인 — Surveying Land Boundaries|수로 점검 — Inspecting an Irrigation Channel|수확 자세 — Harvesting|대장장이 작업 — Smithing at an Anvil|짐 운반·수레 밀기 — Hauling Supplies|빵·식량 나눠주기 — Distributing Rations|기마 순찰 — Mounted Patrol|투구를 옆구리에 든 자세|건틀릿 벗기 — Removing a Gauntlet|성벽 경계 — Watching from the Battlements|무기 내려놓고 항복하기|부상자 곁에 무릎 꿇기|어깨 너머로 돌아보기|귀 가까이 속삭이기|시종이 옷의 여밈을 돕기|창가·난롯가의 사적 휴식"),
("동아시아풍 영지물에 추가할 용어", "식읍|녹읍|수조권|다이묘|번 — Han|석고 — Kokudaka|검지 — Kenchi|검지장|조카마치·성하도시"),
("의상·포즈·공간을 묶은 영지물 장면 조합", "가난한 변경 영주의 첫 시찰|유능한 여성 영주의 재정 개혁|대규모 관개공사|부유한 상업도시의 영주|봉신의 충성 의례|포위된 성의 마지막 회의|정략혼 연회와 비밀 협상|성인 인물의 사적인 착의 장면|폭정에 대한 공개 청원|전쟁 후 영지 재건"),
]

# 군대물·밀리터리물 시각 의미·후보 데이터 강화 리서치

조사일: 2026-10-24 KST. 범위: [군대물 용어 조사](https://chatgpt.com/c/6adb70a2-a2f8-83ec-ac21-6ec6a88f3c9d)의 전체 사용자 메시지와 응답. 이 문서는 **연구와 후속 반영 계획**이며 운영 데이터 등록·검색 교체·이미지 생성 결과가 아니다.

## 조사 결론

기존의 ‘군인·군복·무기’ 수준 후보를 늘리는 것만으로는 부족하다. 이번 확장의 단위는 **국가·시대·조직 문맥**, **의복과 장구의 독립 구조**, **사람·장비·공간 사이의 관계**, **보이는 외형과 증명되지 않는 주장**이다. 동일한 ‘군인’ 요청에서 전투·생활·정비·의례·귀환·성인 패션이 모두 열려 있어야 한다. 요청하지 않은 전투, 무기, 계급, 성적 의미를 기본값으로 덧붙이면 범위가 오히려 좁아진다.

원문 24개 표의 **393행**을 순서대로 보존했고, 연구용 **104개 한영 시각 대안**과 **52개 문맥 구분**을 작성했다. 출처는 40개이며, 관련 본문·검색 발췌·소장품 메타데이터·접근 실패를 구분했다. 모든 393개 정의를 독립 출처로 완전 재검증했다는 뜻은 아니다. 특정 군복·장비의 도판과 한국군 현행 복제는 추가 확인 대상이다. 정확한 건수는 [research-counts.json](research-counts.json)에 있다.

## 참조 대화의 복원 범위

`read_thread`는 1개 대화 turn, `hasMore:false`, `nextCursor:null`을 반환했지만 응답 item 자체가 `truncated:true`여서 10절 군장 중간까지만 전달했다. 페이지 커서의 완료는 본문 완전성을 보장하지 않았다. 로그인된 Chrome에서 원래 URL을 열어 사용자 요청과 1~16절, 15-2절의 성폭력·MST·Nazisploitation, 마지막 조합 예시와 맺음말까지 확인했다.

- [conversation.browser.txt](conversation.browser.txt): 브라우저에서 읽은 전체 렌더링 텍스트. 사이트의 탐색·부가 UI 문구가 일부 포함될 수 있다.
- [conversation-tables.json](conversation-tables.json): 24개 표, 헤더 제외 393행, 표별 순서와 원래 셀을 유지한 추출본.
- [conversation-links.json](conversation-links.json): 응답에 실제로 표시된 외부 링크. `+1/+2` 인용 UI의 숨은 추가 출처를 전부 복원했다고 주장하지 않는다.
- [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md): 각 행의 부분 시각 대안·문맥·추가 표본 보류 경로.

원문에 포함된 폭력·성적 주제도 보존했다. 이 대화는 키워드 조사 자료이며 현재 사용자의 이미지 요청·생성 승인이나 모든 공식 정의의 권위로 취급하지 않는다.

## 1. 장르·역할·서사와 보이는 외형을 나눈다

군대물은 병영 안의 생활을, 전쟁물은 민간인을 포함한 전쟁의 결과를 중심에 둘 수 있다. BFI의 영화 비평에서도 전쟁 배경 안에 로맨스 등 다른 서사 접근이 함께 나타난다. 따라서 장르명 하나를 무장한 인물·전투 장면의 자동 trigger로 쓰지 않는 편이 적절하다. 이 설계 판단은 비평 자료와 원문 범위를 바탕으로 한 연구자의 추론이다. [BFI](https://www.bfi.org.uk/lists/10-great-first-world-war-films)

군사 SF는 거대한 병기만이 아니라 복무·제도·정치·윤리를 포함한다. 미래 병기의 외형과 작품의 군사적 가치관은 별개다. 연구 카드는 보급 컨테이너와 문, 병기 모티브와 신체를 분리해 보여주는 선택지를 두고, 군국주의 지지·전쟁 원인·군사적 성과는 문맥으로 남긴다. [SFE: Military SF](https://sf-encyclopedia.com/entry/military_sf)

신병·베테랑·엄격한 교관·냉소적인 실무자·출세 지향 상관은 서로 다른 경험·동기 서술이다. 흉터·나이 든 얼굴·찢긴 옷·찡그린 표정을 각 유형의 고정 외형으로 삼으면 다양성을 잃는다. V02·V06·V47·V59·V66은 특정 순간의 행동·표면·관계만 제안한다. 첫 전투·최후의 저항·명령과 양심·피로스의 승리·영웅 만들기·기록 조작은 별도 맥락과 시간적 증거가 필요하다.

## 2. 국가·시대·군종·병과·계급·보직을 독립 축으로 둔다

한국 계급 명칭은 군인사법 제3조의 시행 표시를 확인했다. 하지만 그 명칭이 계급장 모양·착용 위치·중대장 같은 보직을 정하지는 않는다. 구체 인물의 계급과 보직, 가상 설정인지 실제 제식인지 따로 적어야 한다. 국가별 등가표와 정확한 표장은 후속 도판 검토가 필요하다. [군인사법 제3조](https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1032035873)

호주전쟁기념관의 편제표는 시대·병과에 따라 단위 구성과 지휘관·인원이 달라지는 사례를 보여준다. 분대·소대·중대라는 말에 보편 인원수를 넣는 방식은 피한다. 임무부대도 하나의 고정된 규모로 시각화하지 않는다. [Australian War Memorial: Structure](https://www.awm.gov.au/learn/understanding-military-structure/army/structure)

현역·예비역·보충역은 병역상 신분이다. 생활관·점호·급식·휴가·말년의 실제 모습과 운영을 해당 신분표에서 추론할 수는 없다. 한국 병영의 시기별·부대별 생활 사진은 P1 추가 조사로 남긴다. V01~V10은 한국군의 공식 재현이 아니라 가능한 생활 장면 초안이다. [병무청 병역이행안내](https://www.mma.go.kr/contents.do?mc=usr0000041)

부대 표장에는 조직 역사·지역·전통이 담길 수 있다. 같은 별·날개·해골·왕관이 항상 같은 계급·자격을 의미하지 않는다. 정규군·민병대·PMC·법적 용병의 구분도 장비 혼용이나 국적처럼 보이는 외형으로 결정하면 안 된다. [National Army Museum: Regimental badges](https://www.nam.ac.uk/explore/regimental-badges), [ICRC: PMSCs](https://www.icrc.org/en/law-and-policy/private-military-and-security-companies)

## 3. 군복은 명칭보다 구조와 쓰임을 정확하게 연결한다

미 육군 안내는 ACU와 IHWCU라는 군복에 OCP라는 무늬가 쓰인다고 구분한다. ‘디지털’, ‘우드랜드’, ‘카키’, ‘OD’, ‘OCP’, ‘ACU’는 각각 패턴 형식·일반 환경 표현·색채어·특정 무늬·옷 체계 등 다른 범주의 값이다. 한국어 카키를 짙은 녹색 하나로 고정하거나 각진 무늬를 OCP와 등치하지 않는다. [US Army uniforms](https://www.army.mil/uniforms/)

전투복·근무복·정복·의장복·만찬복·작업복·비행복은 용도별 갈래를 유지한다. V13~V19는 주머니·칼라·지퍼·장식끈·하네스·의복 층을 다룬다. 한 후보에 모든 용도의 복장을 섞거나, 의장 장식끈을 실전 장구로 전용하지 않는다. 정확한 국가별 명칭 대응은 검토 대상이다.

역사복은 아래처럼 형태를 나누되 고증 승격을 분리한다.

| 대상 | 이번 시각 구분 | 후속 확인 |
|---|---|---|
| 트렌치코트 | 견장·겹친 플랩·허리 고리와 벨트 | 연식·군·민간 변형·정확한 표본 |
| Battle Dress | 짧은 상의와 높은 허리 비율 | 판형·주머니·여밈의 해당 연식 |
| 펠리스·돌먼 | 별도 덧재킷과 안쪽 재킷을 구분 | 끈 고정점·소매·안감·착용 방향 |
| 그레이트코트·스모크·봄버 | 길이·부피·여밈·밑단으로 분해 | 직물·모델·시기별 사례 |
| 퍼티·각반 | 감은 천의 나선과 별도 패널형 여밈 | 군·시대별 표본 |
| 샤코·버스비 | 같은 모자로 합치지 않음 | 높이·털·전면판·시기별 도판 |

박물관 자료는 군복에서 민간 패션으로의 이동과 후사르 펠리스의 어깨걸침 사례를 뒷받침한다. 이것이 현재 모든 트렌치·코트·제복의 공식 형태를 정하는 것은 아니다. [Army fashion statements](https://www.nam.ac.uk/explore/armys-been-responsible-many-fashion-statements), [Cavalry roles](https://www.nam.ac.uk/explore/cavalry-roles), [샤코 표장 소장품](https://collection.nam.ac.uk/detail.php?acc=1959-01-12-1)

길리 슈트는 프린트 무늬만으로 이루어진 옷과 구별해야 한다. 특정 박물관 표본은 바탕 의복에 다른 천을 더해 형태를 흐리는 구조를 설명한다. V97은 바탕층과 추가 섬유의 시각 관계만 제안하며 실제 은폐 능력·저격수 신분·무기를 추가하지 않는다. [Nationaal Militair Museum, 129332](https://collectie.nmm.nl/nl/collectie/detail/445775/)

## 4. 군장·방호구는 수납·하중·장착·성능을 분해한다

영국군 Virtus STV 설명에는 방호재 없이 휴대구로 쓰는 구성, 소프트아머, 판 수납구, 복합 방호 구성이 구별되어 있다. ‘파우치가 많은 조끼 = 방탄복’ 또는 ‘닫힌 캐리어 = 판이 들어 있음’이라는 변환은 성립하지 않는다. V30은 벗어 놓은 열린 수납구에서 판이 보이는 한 상태이고 V31은 얇은 휴대 패널의 외형이다. 어느 것도 실제 방호 성능의 시각적 증명은 아니다. [British Army: Combat body armour](https://www.army.mod.uk/learn-and-explore/equipment/personal-equipment/combat-body-armour/)

MOLLE 체계, PALS의 부착 격자, 파우치 뒤 끈의 실제 결합, 웹빙 하중 경로는 각각 V32~V34로 분리했다. 고정된 파우치 내용물이나 모든 레이저 컷 구조를 같은 방식으로 추가하지 않는다. 배낭 끈·허리벨트·슬링 두 끝·홀스터·음용관은 V08·V35~V37에서 실제 소유자와 연결을 명시한다. [US Army 역사 조사 PDF](https://history.army.mil/html/museums/uniforms/survey_uwa.pdf), [US Army MOLLE FAQ](https://cpeground.army.mil/Resources/Frequently-Asked-Questions/)

센서의 물리 장착, 보는 사람, 표시 화면, 화면 속 대상, 실제 환경도 별도 소유자다. 광증폭과 열영상의 융합 장치가 존재하므로 NVG·열영상을 항상 별개 기계나 녹색·흑백의 고정 쌍으로 나누지 않는다. V39와 V40은 같은 장치의 올림/내림 대안이며 동시에 합치지 않는다. V41의 화면 속 인체상은 실물 인물·정확한 온도·실제 적의 존재를 증명하지 않는다. [PEO Soldier Technology Compendium 2025](https://www.peosoldier.army.mil/Portals/53/Documents/soldier_systems/2025_PEO_Soldier_Technology_Compendium_Print.pdf)

## 5. 포즈 후보는 손·몸·물체의 연결을 완결한다

V49~V69를 독립 포즈 태그의 모음으로 축소하지 않는다. 경례의 팔은 같은 인물의 어깨로 이어져야 하고, 쌍안경은 두 손·두 접안부·같은 눈과 연결되어야 한다. 무전은 수화기·손·귀/입과 본체로 이어지는 케이블을 구분한다. 지도를 보는 인원은 같은 지점으로 시선과 손이 모여야 한다. 이러한 구도는 연구자가 작성한 실현이며 공식 제식·교신 성공·고의의 입증은 아니다.

해치 장면은 허리가 차량 내부로 이어지고 팔과 테두리의 지지가 보여야 한다. 조종석은 골반·좌석·하네스·무릎·계기판 사이에 공간이 필요하다. 부축은 두 사람의 팔과 손을 분리하고, 들것 운반은 같은 프레임 양끝·각 손잡이·누운 몸의 지지를 함께 읽어야 한다. 유품과 포옹은 물체 소유·팔의 주인·발 지지를 확인하되 가족·연애·사망·동의의 문맥을 만들지 않는다.

미 육군 TC 3-21.5는 무기별·동작별로 제식을 나눈다. 이번에는 목차와 관련 발췌를 확인했으므로 어깨총·받들어총의 정확한 손·총 위치는 **보류**한다. 나라·시대·무기를 지정해 해당 도판을 검토한 뒤 별도 대안으로 추가해야 한다. [TC 3-21.5, May 2021](https://www.usarcent.army.mil/Portals/1/Documents/regs/TC%203-21.5%20Drill%20and%20Ceremonies%20May%202021.pdf)

## 6. 장비와 공간의 실루엣은 기능·임무의 증명이 아니다

LoC의 총기 역사 개론은 기관단총과 돌격소총 등을 구분하지만 길이·조준경 하나로 소총·카빈·DMR·저격소총 전체를 구분하는 표준은 아니다. 원문 용어를 모두 보존하면서 모델별 도판·구조 조사는 다음 단계로 둔다. 장전·운용 순서나 전술 수행법은 이 시각 데이터의 조사 대상이 아니다. [Library of Congress](https://guides.loc.gov/submachine-gun-to-the-assault-rifle)

차량의 궤도·포탑·포신·승하차부·하부 형상은 볼 수 있어도 전차/자주포, APC/IFV의 역할과 내부 능력을 단정할 수 없다. V98~V100은 경사판 연결·포탑 지지·높은 차체라는 부분 실현이다. 특정 MRAP의 설명을 모든 차종의 방호 성능으로 일반화하지 않는다. [US Army 훈련 장비 표](https://home.army.mil/liggett/5715/3746/4738/ATFP_EA-FNSI_2016.pdf), [MRAP 사례](https://www.army.mil/article/73139/unit_trains_with_armys_newest_trucks)

공격·정찰·수송 헬기는 임무·설계의 다른 범주다. UAS는 기체만이 아니라 관련 운용 장비를 포함한다. 한 기체를 보았다고 무장·자율성·조종자의 적대 의도를 부여하지 않는다. 함정의 격벽·출입구·갑판과 항공기 cockpit의 경계도 유지한다. [US Army Aviation](https://www.army.mil/article-amp/227276/we_are_10th_cab_an_introduction_to_the_10th_combat_aviation_brigade), [FAA UAS](https://www.faa.gov/faq/what-unmanned-aircraft-system-uas), [미 해군 용어집](https://www.history.navy.mil/content/history/museums/nmusn/education/educational-resources/ships-to-the-sea-1/nautical-vocabulary-list.html)

CAS는 낮게 나는 기체의 이름이 아니며, MEDEVAC·CASEVAC도 헬기의 종류가 아니다. 항공지원의 아군·표적 관계, 지정 의료능력, 이송 중 돌봄 등은 물체 외형과 다른 수준이다. 브리핑·디브리핑·AAR도 지도 앞 모습만으로 구분되지 않는다. 실제 음성·시점·역할은 문맥에 남긴다. [RCAF doctrine glossary](https://www.canada.ca/en/air-force/corporate/policies-standards/royal-canadian-air-force-doctrine/ad-b-ga-403-000-fp-001-glossary.html), [JTS 용어 논의](https://jts.health.mil/assets/docs/cosccc/2019-13-Nov-CoSCCC-CoERCCC-Minutes.pdf)

## 7. 폭력·트라우마·성적 소재의 범위를 빠뜨리지 않는다

393행에는 고어·신체 훼손·헤이징·고문·포로 학대·약탈·학살·소년병·성폭력·MST·군사 성노예제·Nazisploitation이 그대로 있다. 문맥 경로는 주제 삭제가 아니다. 특히 고어는 피·신체 손상을 직접 보여주는 표현 양식을 포함하므로 붉은 얼룩이나 찢긴 옷으로 그 요청 전체를 대체하지 않는다. V103·V104는 **그보다 좁은** 물질·의복 상태의 대안이다.

KIA/WIA/MIA/POW 같은 지위, 사건의 주체·고의·피해, 국제범죄의 요건은 분리한다. 수갑·폐허·사망한 듯한 몸이 실제 POW 신분·전쟁범죄·집단살해의 모든 요건을 증명하지 않는다. 소년병 관련 개념은 전투 외 동원도 포함한다. [ICRC Rules of war](https://www.icrc.org/en/document/FAQ-rules-of-war-ihl), [UN 범죄 개념](https://www.un.org/en/genocide-prevention/definition), [UNICEF](https://www.unicef.org/protection/children-recruited-by-armed-forces)

셸 쇼크·전투 피로·PTSD는 역사가 다르고, 도덕적 손상과 MST는 각각 PTSD의 동의어가 아니다. 멍한 응시·흉터·의족·숙인 고개는 해당 진단·경험의 고정 시각 표지가 될 수 없다. 소리·먹먹함·정적도 단일 정지사진에서는 실제 청각 사실이 아니라 표현·문맥 경로로 남겨야 한다. [VA PTSD history](https://www.ptsd.va.gov/understand/what/history_ptsd.asp), [VA Moral injury](https://www.ptsd.va.gov/understand/related/moral_injury_ptsd.asp), [VA MST](https://ptsd.va.gov/understand/types/sexual_trauma_military.asp)

성인 밀리터리 시크·핀업·군복 페티시·권위의 에로티시즘·택티컬 메이드·비키니 아머는 실제 군복·방호·군인 신분과 분리한다. 크롭트 재킷·미니 치마·가터·장식 하네스·광택 제복·어깨 코트·젖은 의복은 착의 상태·연결·표면별 선택지를 만든다. 특정 후보의 내의나 피부 노출 상태를 모든 ‘오픈 재킷’·‘젖은 옷’ 요청의 기본값으로 옮기지 않는다.

노즈아트는 기체 표면에 그린 이미지이며 핀업만을 뜻하지 않는다. 곡면·패널선·그림 경계가 읽혀야 하고, 그림 속 인물은 실제 옆에 선 인원수와 구분해야 한다. [National WWII Museum](https://www.nationalww2museum.org/war/articles/decoding-wwii-plane-nose-art), [142nd Wing 상어입 노즈아트](https://www.142wg.ang.af.mil/News/Article-Display/Article/2703590/about-that-shark-mouth-on-the-151-jet/)

전우애·BL/GL·로맨스·제도상 fraternization·성적 강압·CRSV·성노예제는 한 묶음의 positive 후보가 될 수 없다. 2014년 미 육군의 관계 설명은 비성적 친교도 포함할 수 있음을 보여주지만 현행 모든 군의 규정은 아니다. 성적 폭력은 합의된 성인 패션의 속성이 아니다. [US Army historical explanation](https://www.army.mil/article/138222/Army_updates_reg_defining_inappropriate_relationships), [ICRC conflict-related sexual violence](https://www.icrc.org/en/document/five-things-know-about-sexual-violence-conflict-zones)

## 기존 데이터와 연결하는 판단

작업 트리의 manifest closure를 직접 읽어 후보 21,883개·binding 16,698개를 조사했다. 군장·보호구 표적 어휘는 en/ko/definition/aliases의 지정 검색에서 0건이었지만 **의미상 데이터 부재나 설치 검색 실패를 입증하지는 않는다.** 조회 범위·검색어·모듈 해시와 인접 후보 47개 원문은 [corpus-audit.json](corpus-audit.json), [existing-source-snapshots.json](existing-source-snapshots.json)에 있다.

| 기존 후보 | 확인한 문제 또는 재사용 범위 | 제안 |
|---|---|---|
| `cand_25e0f45f02b25ac8a853eb63b8f0fa0f` 군인 역할 모델 | ‘일관된 군복’이라는 요약이며 세부 장구·역할을 완결하지 않음 | 넓은 subject 후보로 유지, 세부 구조는 별도 대안 |
| `cand_59849d02f9cc501bb453ac8d42a8ede7` 경례 | EN은 손가락·변형별 손바닥·팔꿈치를 서술하나 KO는 ‘경례’ 한 단어 | 전체 한영 의미·조건·effects를 대조해 보완; V49를 그대로 덮어쓰지 않음 |
| `cand_7c21122f9000531c8cc8f8ad22e90b35` aircraft flight deck | 항공기 조종실 문맥인데 ‘비행갑판’이라는 별칭이 있음 | 항공모함 갑판 경로와 혼동 평가 후 문맥 한정 |
| `cand_5ccf05cc8bd152caaf61d576b37698b8` 트렌치 | 견장·플랩·고리를 지나는 벨트라는 완결 문장 | V20 신규 중복 작성에 앞서 전체 재사용 검토 |
| `cand_47e5157aab435869be9c51ce7e3dbb01` 바퀴 들것 | 구급대원 2명·바퀴·매트리스·양끝 손잡이 포함 | 바퀴 들것에만 검토, V67 천 들것 운반과 합치지 않음 |
| `cand_64518d7eba7b55768ec9a1fde733d428` 인쇄 핀업 | 종이 테두리·핀·정비실 벽의 인쇄 초상 | V83 항공기 곡면 그림으로 변형해 같은 CID를 재사용하지 않음 |
| `cand_2b1148c925bf55e5aa7a69c44caaa389` 가터 연결 | 같은 가터 클립과 스타킹 윗밴드의 접점 | 전체 조건과 부분 property lock 검토 후 기존 연결 대안 재사용 |

이것은 읽은 소스에 대한 예비 판단이다. native qualification·검색 rank·실제 채택의 승인은 아니다. 특히 V20은 기존 소스와 상당히 겹치므로 신규 CID가 필요한 사례로 세지 않는다.

## 남은 불확실성과 실행 경계

한국군 현행 복제·계급장 전체 도판, 국가·연식별 제식, 샤코·버스비·돌먼·브리치즈, 소프트아머 단면, 총검·박격포·곡사포·탄약/탄창/클립 등 구체 표본, 함종과 항공기 모델별 구조는 후속 조사 대상이다. 403을 받은 출처는 [SOURCES.md](SOURCES.md)에 그대로 남겼다. 문헌 명칭을 확인한 것과 도판을 본 것을 혼용하지 않았다.

시각 대안은 충분한 초기 설계 재료지만 운영 데이터에는 바로 import할 수 없다. 실제 조건·효과·소유자·현재 catalog 적합성과 한영 의미를 검토하고 등록, 설치 검색, 채택된 전체 문장의 프롬프트 반영, 저장 픽셀을 각각 확인해야 한다. [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)에 순서·완료 조건·검증·복구를 적었다.

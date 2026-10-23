"""Rebuild research-only artifacts. Never imports or changes runtime data."""
from pathlib import Path
import collections
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent

def save(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

# Source notes are bounded paraphrases. Scene geometry below is authored research,
# not a description of a source photograph and not official drill/medical advice.
SOURCE_TEXT = '''
S01|Army Uniforms and Grooming Guide|US Army|https://www.army.mil/uniforms/|body_reviewed|ACU는 군복 체계이고 OCP는 무늬다. 근무·전투·의례 복장과 표장 배치를 구분한다.|미군 안내의 한 시점이며 한국군·역사군복의 규정으로 전용하지 않는다.
S02|군인사법 제3조|국가법령정보센터|https://www.law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lsJoLnkSeq=1032035873|official_search_excerpt|2026-10-02 시행 표시와 병·부사관·준사관·장교의 계급 명칭을 확인했다.|계급장 도판·복제·보직 배정은 이 조문만으로 확인되지 않는다.
S03|병역이행안내 개요|병무청|https://www.mma.go.kr/contents.do?mc=usr0000041|official_search_excerpt|현역·예비역·보충역 등은 제도상 신분이며 옷차림이나 현재 직업과 일대일 대응하지 않는다.|생활관 배치·전투식량·휴가의 실제 운영에 대한 출처는 아니다.
S04|Structure|Australian War Memorial|https://www.awm.gov.au/learn/understanding-military-structure/army/structure|body_reviewed|호주군 자료 안에서도 시대와 병과에 따라 편제와 인원 구성이 다르다.|분대·중대의 보편 인원수나 한국군 계급 대응표를 만들지 않는다.
S05|Regimental badges|National Army Museum|https://www.nam.ac.uk/explore/regimental-badges|body_reviewed|부대 표장은 조직의 전통·지역·역사와 연결되며 계급과 다른 정보를 전한다.|별·날개·해골의 의미를 모양만으로 고정하지 않는다.
S06|Army fashion statements|National Army Museum|https://www.nam.ac.uk/explore/armys-been-responsible-many-fashion-statements|body_reviewed|트렌치코트와 Battle Dress의 형태가 민간 패션으로 옮겨 갔으며 장식과 기능은 달라질 수 있다.|민간 패션의 재단이 실제 군복 규정·실용성을 보장하지 않는다.
S07|Cavalry roles|National Army Museum|https://www.nam.ac.uk/explore/cavalry-roles|body_reviewed|후사르 펠리스는 털 가장자리를 가진 짧은 덧재킷이며 어깨에 걸치고 끈으로 고정하는 사례가 있다.|현대 코트 어깨걸침과 같은 의복으로 합치지 않는다.
S08|Pelisse, 3rd Zieten Hussars, pre-1914|National Army Museum collection|https://collection.nam.ac.uk/detail.php?acc=1960-01-3-4|catalogue_text_only|특정 소장품의 명칭·소속·시기와 accession 1960-01-3-4를 확인했다.|안감·여밈·착용 방향의 도판 픽셀 검토는 하지 않았다.
S09|Combat body armour|British Army|https://www.army.mod.uk/learn-and-explore/equipment/personal-equipment/combat-body-armour/|body_reviewed|Virtus STV는 휴대구·소프트아머·판 수납구·복합방호 구성으로 달라질 수 있다. 외형만으로 내부 방호재를 확정할 수 없다.|제품별 방호 성능·정확한 현행 크기 수·착용 적합성은 이 연구에서 평가하지 않는다.
S10|Survey of US Army Uniforms, Weapons and Accoutrements|US Army Center of Military History|https://history.army.mil/html/museums/uniforms/survey_uwa.pdf|official_search_excerpt|MOLLE 체계와 그 장비에 쓰인 PALS 부착 격자를 구분하는 역사 자료다.|전 페이지 도판 검토나 최신 모든 레이저 컷 방식의 표준 검증은 미실행이다.
S11|Frequently Asked Questions: MOLLE|US Army acquisition office|https://cpeground.army.mil/Resources/Frequently-Asked-Questions/|official_search_excerpt|MOLLE는 조끼·배낭·파우치 등을 임무에 맞게 구성하는 모듈식 휴대 장비 체계다.|파우치 수량이나 내용물·방호재의 실제 존재를 자동 부여하지 않는다.
S12|From the Submachine Gun to the Assault Rifle|Library of Congress|https://guides.loc.gov/submachine-gun-to-the-assault-rifle|body_reviewed|기관단총·돌격소총의 역사와 설계 분류는 구분된다.|특정 모델의 식별·작동·장전법은 이 개론의 확인 범위를 넘는다.
S13|TC 3-21.5 Drill and Ceremonies, May 2021|US Army|https://www.usarcent.army.mil/Portals/1/Documents/regs/TC%203-21.5%20Drill%20and%20Ceremonies%20May%202021.pdf|official_search_excerpt|차렷·쉬어·경례·행진과 M4 계열 무기 제식의 분리된 항목을 확인했다.|국가·무기별 각 동작의 도판·손 방향은 추가 검토까지 보류한다.
S14|Nautical Vocabulary List|Naval History and Heritage Command|https://www.history.navy.mil/content/history/museums/nmusn/education/educational-resources/ships-to-the-sea-1/nautical-vocabulary-list.html|official_search_excerpt|갑판·격벽·침상·식당 등 함정 공간의 용어는 구조와 용도에 연결된다.|함종별 구획·잠수함 내부와 민항기 flight deck을 동일시하지 않는다.
S15|Letters from the First World War: The trenches|UK National Archives|https://www.nationalarchives.gov.uk/education/teaching-resources/letters-from-the-first-world-war-the-trenches-part-one/|search_excerpt_body_403|편지 사료의 검색 발췌에서 우천·노출·통신병의 생활 경험을 확인했다.|전체 본문은 403. 한국 병영생활 또는 모든 참호 배치의 근거로 확대하지 않는다.
S16|Canadian Forces Aerospace Shape Doctrine Glossary|Royal Canadian Air Force|https://www.canada.ca/en/air-force/corporate/policies-standards/royal-canadian-air-force-doctrine/ad-b-ga-403-000-fp-001-glossary.html|body_reviewed|CAS의 close는 아군과 가까운 표적에 대한 긴밀한 임무 통합을 뜻한다. ISR은 수집·처리·전달을 연결한다.|저공비행이나 화면 속 표적 아이콘만으로 임무를 증명하지 않는다.
S17|CoSCCC / CoERCCC Minutes, Nov 2019|Joint Trauma System|https://jts.health.mil/assets/docs/cosccc/2019-13-Nov-CoSCCC-CoERCCC-Minutes.pdf|official_search_excerpt|의료 전용·지정 능력과 이송 중 의료지원에 관한 MEDEVAC/CASEVAC 용어 차이를 기록한다.|체계·국가별 용어 차이가 있어 헬기나 적십자 모양만으로 분류하지 않는다.
S18|What is an unmanned aircraft system?|FAA|https://www.faa.gov/faq/what-unmanned-aircraft-system-uas|official_search_excerpt|UAS는 무인 항공기와 운용에 필요한 장비를 함께 포함한다.|자율성·무장·추적 대상·운용자의 적대 의도는 기체 외형에 없다.
S19|Fused Night Vision, Technology Compendium 2025|PEO Soldier|https://www.peosoldier.army.mil/Portals/53/Documents/soldier_systems/2025_PEO_Soldier_Technology_Compendium_Print.pdf|official_search_excerpt|열영상과 광증폭 센서를 결합하는 장치도 있어 둘을 항상 배타적인 장치로 나누면 틀린다.|녹색 화면을 모든 NVG의 공통 외형으로 강제하지 않는다. 전체 도판은 보류다.
S20|FAQ: Rules of war|ICRC|https://www.icrc.org/en/document/FAQ-rules-of-war-ihl|body_reviewed|민간인 보호와 고문·부당대우 금지 등을 다룬다. 보이는 행위와 법적 책임 판단은 다르다.|사진 하나로 분쟁 유형·신분·고의·위법성 전체를 확정하지 않는다.
S21|Definitions of Genocide and Related Crimes|United Nations|https://www.un.org/en/genocide-prevention/definition|official_search_excerpt_body_403|전쟁범죄·인도에 반한 죄·집단살해는 서로 다른 맥락과 요건을 갖는다.|본문 재조회는 403. 법적 판단을 위한 전체 요건표나 현행 법률 자문으로 쓰지 않는다.
S22|Children recruited by armed forces or armed groups|UNICEF|https://www.unicef.org/protection/children-recruited-by-armed-forces|body_reviewed|아동 동원에는 전투뿐 아니라 운반·취사·연락 등의 역할도 포함된다.|작은 체격이나 짧은 머리만으로 나이·강제동원을 판정하지 않는다.
S23|History of PTSD in Veterans|VA National Center for PTSD|https://www.ptsd.va.gov/understand/what/history_ptsd.asp|body_reviewed|셸 쇼크·전투 피로·현대 PTSD에는 개념과 진단 역사의 차이가 있다.|멍한 시선이나 흉터를 임상 진단으로 치환하지 않는다.
S24|Moral Injury and PTSD|VA National Center for PTSD|https://www.ptsd.va.gov/understand/related/moral_injury_ptsd.asp|official_search_excerpt|도덕적 손상은 PTSD와 겹칠 수 있으나 그 자체가 진단명은 아니다.|죄책감·신념·사건 경험은 얼굴 표정으로 증명되지 않는다.
S25|Military Sexual Trauma|VA National Center for PTSD|https://ptsd.va.gov/understand/types/sexual_trauma_military.asp|official_search_excerpt|MST는 군 복무 중 성폭행·성희롱 경험에 관한 VA 용어이며 진단명이 아니다.|피해 경험·성별·진단을 특정 외형에 연결하지 않는다.
S26|Army updates reg defining inappropriate relationships, 2014|US Army|https://www.army.mil/article/138222/Army_updates_reg_defining_inappropriate_relationships|body_reviewed_historical|친교·거래 등 성적이지 않은 관계도 지휘·공정성 문제와 연결될 수 있다.|2014년 설명이다. 현행 전 세계의 연애 금지 규정으로 사용하지 않는다.
S27|Five things to know about sexual violence in conflict zones|ICRC|https://www.icrc.org/en/document/five-things-know-about-sexual-violence-conflict-zones|body_reviewed|성폭력은 폭력·착취의 범주이며 피해자의 외형이나 성별로 발생을 판정할 수 없다.|동의된 성인 패션·로맨스와 성적 강압을 같은 positive 후보로 묶지 않는다.
S28|Private military and security companies|ICRC|https://www.icrc.org/en/law-and-policy/private-military-and-security-companies|official_search_excerpt|기업 직원의 지위는 역할과 행위에 따라 달라지며 법적 용병 정의와 단순 동의어가 아니다.|패치 없음·혼합 장비·외국인 외형이 법적 신분을 증명하지 않는다.
S29|10 great First World War films|BFI / Matthew Thrift|https://www.bfi.org.uk/lists/10-great-first-world-war-films|body_reviewed_critical|전쟁영화에는 로맨스·풍자·법정 등 여러 서사 접근이 함께 나타난다.|공식 장르 온톨로지나 모든 작품에 필요한 시각 요소의 목록은 아니다.
S30|Military SF|The Encyclopedia of Science Fiction|https://sf-encyclopedia.com/entry/military_sf|body_reviewed_critical|군사 SF의 역사와 정치·복무 제도는 병기 외형만으로 요약되지 않는다.|전문 비평·참고자료이며 군사 기술의 1차 규정으로 사용하지 않는다.
S31|Decoding WWII Plane Nose Art|National WWII Museum|https://www.nationalww2museum.org/war/articles/decoding-wwii-plane-nose-art|body_reviewed_critical|기체에 그려진 개별 그림·이름·상징은 국가 표장과 다른 시각문화 층이다.|박물관의 역사 해설이며 특정 모델·역사 그림의 재현 허가나 실물 인물을 증명하지 않는다.
S32|Order No 150 X: SS Arlanza, Starboard|Imperial War Museums|https://www.iwm.org.uk/collections/item/object/27409|catalogue_search_metadata|역사 선박의 대즐 위장 관련 도판 기록을 확인했다.|도판 픽셀·실제 위장 효율·원색을 검토하지 않았다.
S33|Nazisploitation! The Nazi Image in Low-Brow Cinema and Culture|Bloomsbury|https://www.bloomsbury.com/uk/nazisploitation-9781441199652/|reference_link_body_403|참조 대화에 있는 연구서 서지 포인터를 보존했다.|이번 본문 접근 403. 이 출처만으로 새 세부 의미·도상을 확정하지 않는다.
S34|About that Shark mouth on the 151 Jet, 2021|142nd Wing History Office|https://www.142wg.ang.af.mil/News/Article-Display/Article/2703590/about-that-shark-mouth-on-the-151-jet/|official_search_excerpt|항공기 상어입 그림이라는 비핀업 노즈아트의 구체적인 사례가 있다.|그림의 실제 색·치수·모델별 배치는 도판 확인 전 보류한다.
S35|Special Operations|US Army recruiting|https://www.goarmy.com/careers-and-jobs/specialty-careers/special-ops|body_reviewed|Special Operations 안에 Rangers와 Special Forces 등 서로 다른 조직 경로가 있다.|홍보 사이트이며 모든 국가의 특수부대 편제·복장을 대표하지 않는다.
S36|Fort Hunter Liggett Army Total Force Training Integration EA, 2016|US Army|https://home.army.mil/liggett/5715/3746/4738/ATFP_EA-FNSI_2016.pdf|official_search_excerpt|훈련 장비 표가 Abrams·Bradley·M109를 전차·전투차량·자주곡사포로 구분한다.|유형별 역할의 근거이며 전 페이지 외형 도판·모든 Bradley 변형의 탑승 구조를 확인한 것은 아니다.
S37|10th Combat Aviation Brigade introduction, 2019|US Army|https://www.army.mil/article-amp/227276/we_are_10th_cab_an_introduction_to_the_10th_combat_aviation_brigade|official_search_excerpt|공격·정찰, 중형 수송, 중량 수송 헬기라는 서로 다른 역할 경로를 구분한다.|공격헬기와 수송헬기의 모든 운용·무장·크기 기준을 보편화하지 않는다.
S38|Unit trains with Army's newest trucks, 2012|US Army|https://www.army.mil/article/73139/unit_trains_with_armys_newest_trucks|official_search_excerpt_historical|MRAP의 두 변형과 높아진 V형 하부 구조라는 사례 설명을 확인했다.|외형은 내폭 성능·생존·모든 MRAP 공통 치수를 증명하지 않는다.
S39|Shako plate, 13th Light Dragoons, 1855-1861|National Army Museum collection|https://collection.nam.ac.uk/detail.php?acc=1959-01-12-1|catalogue_search_metadata|동일 연대 안에서도 시기에 따라 샤코에서 버스비로 바뀐 기록이 있다.|두 모자 종류를 같은 털모자 또는 같은 부대로 고정하지 않는다. 정확한 도판은 보류다.
S40|Ghillie suit, object 129332|Nationaal Militair Museum|https://collectie.nmm.nl/nl/collectie/detail/445775/|catalogue_search_metadata|바탕 옷에 다른 천 조각을 더해 윤곽을 흐리는 구체적 소장품 설명이 있다.|식물·망·천의 시각 층을 프린트 무늬와 구분하되 은폐 성능과 모든 길리 슈트 구성을 일반화하지 않는다.
'''

sources=[]
for line in SOURCE_TEXT.strip().splitlines():
    sid,title,publisher,url,access,support,limit=line.split('|')
    sources.append(dict(id=sid,title=title,publisher=publisher,url=url,access=access,
                        accessed_date_kst='2026-10-24',bounded_support_ko=support,limitations_ko=limit))
save('sources.json',sources)

# Each row: ID, title, complete KO, complete EN, explicit graph triples,
# observable checks, confusion boundary, proposed roles, source IDs.
CARD_TEXT = '''
V01|생활관의 개인 구역|서로 마주 보는 침상 두 줄 사이에 통로가 있고 각 침상 머리맡에 별도 관물대와 접힌 담요가 놓인다.|Two rows of bunks face an open aisle, with a separate locker and folded blanket at each bunk's head.|bunks>face>aisle;locker>beside>bunk|침상 반복;통로 연속;개별 수납|신병·선후임·특정 국가의 생활규정은 이 배치로 증명하지 않는다.|location,spatial_depth|S03
V02|점호의 줄과 보고자|줄을 맞춘 인원 앞에서 한 사람이 명부판을 들고 서 있으며 앞줄 사람들의 얼굴이 그 사람을 향한다.|A person holding a roster board stands before aligned rows of personnel whose front-row faces turn toward that person.|roster>held_by>reporter;front_row>faces>reporter|명부 지지 손;앞줄과 보고자 분리;얼굴 방향|보이는 명단은 출석 사실이나 전원의 소속을 증명하지 않는다.|relational_action,gaze_target|S13
V03|불침번의 빛 구역|침상 옆 통로에 선 사람의 작은 손전등이 바닥 한 구역을 비추고 뒤쪽 침상에는 누운 사람들이 있다.|A standing person in the bunk aisle directs a small flashlight onto a patch of floor while people lie in bunks behind them.|flashlight>held_by>sentry;sentry>stands_in>aisle;beam>falls_on>floor|손전등 주인;바닥의 빛;침상과 통로|수면 여부·시간·불침번 명령은 문맥이며 얼굴을 향한 탐조로 바꾸지 않는다.|lighting,location|S03
V04|급식의 전달 접점|급식대 뒤의 손이 국자를 배식판의 한 칸 위에 들고 있고 식사자의 두 손은 배식판 양쪽을 지지한다.|A hand behind the serving counter holds a ladle over one compartment of a tray supported at both sides by the diner's hands.|server.hand>holds>ladle;diner.hands>support>tray;ladle>above>tray.compartment|두 사람의 손 소유;국자와 칸;배식판 수평 지지|군 급식이라는 제도·짬밥의 경력 의미와 음식 외형을 합치지 않는다.|contact_point,relational_action|S03
V05|보급 상자의 인계|트럭 적재함 끝의 사람이 상자 아래를 받치고 지상의 다른 사람이 같은 상자의 양옆을 잡는다.|A person at a truck's cargo edge supports the underside of a crate while another person on the ground grips the same crate's sides.|person_a.hands>support>crate.bottom;person_b.hands>grip>crate.sides;crate>between>people|같은 상자;양쪽 손;높이와 지지|운송 중과 인계 완료를 동시에 주장하지 않으며 내용물은 외부 형태로 확정하지 않는다.|relational_action,contact_point|S11
V06|정비 공구와 열린 패널|작업복 차림의 사람이 차량의 열린 측면 패널 앞에 무릎을 대고 같은 손의 렌치를 노출된 고정구에 댄다.|A person in coveralls kneels beside an open vehicle side panel, bringing a wrench in one hand against an exposed fastener.|maintainer.hand>holds>wrench;wrench>contacts>fastener;panel>open_on>vehicle|렌치의 손;공구와 고정구 접점;열린 패널|정비 성공·고장 원인·실제 장비 모델은 주장하지 않는다.|contact_point,prop_state|S11
V07|편지와 사진의 매체 경계|앉은 사람의 한 손이 접힌 편지를 펼쳐 들고 탁자 위의 작은 가족사진에는 종이 테두리가 보인다.|A seated person holds an unfolded letter in one hand, while a small family photograph on the table retains a visible paper border.|hand>holds>letter;photo>rests_on>table;depicted_people>inside>photo|편지 소유;사진 테두리;실물과 사진 인물 분리|가족관계·귀환 약속·유품의 이력은 별도 문맥이다.|prop_state,background_element|S15
V08|배낭 행군의 하중|두 어깨끈이 배낭 상부에서 같은 사람의 양어깨를 지나며 허리벨트가 허리를 감싸고 상체는 약간 앞으로 기운다.|Two shoulder straps run from a rucksack over the same person's shoulders, a waist belt encircles the waist, and the torso inclines slightly forward.|rucksack.straps>over>wearer.shoulders;belt>around>wearer.waist;rucksack>behind>torso|끈 연속;벨트와 허리;배낭 무게 방향|실제 질량·피로·규정상 완전군장 구성을 확정하지 않는다.|body_pose,wearable_accessory|S09,S11
V09|PX의 작은 소비|제복 차림 두 사람이 매대 앞에 서 있고 한 사람이 포장 간식을 들어 다른 사람 쪽으로 내민다.|Two uniformed people stand by a shop counter as one extends a wrapped snack toward the other.|giver.hand>holds>snack;snack>toward>receiver;people>beside>counter|간식 주인;수신자 방향;매대|특정 매장 상표·국가·계급 관계·공짜 제공 여부는 문맥이다.|location,relational_action|S03
V10|근무 교대의 기록|책상 앞의 두 사람 중 한 사람이 펼친 기록부의 같은 줄을 짚고 다른 사람은 그 지점을 내려다본다.|At a desk, one of two people points to a line in an open logbook while the other looks down at that same point.|finger>points_to>logbook.line;receiver.gaze>toward>logbook.line|같은 줄;손 소유;서로 다른 인물|당직 인수인계 완료·기록의 진실은 증명하지 않는다.|gaze_target,contact_point|S03
V11|방한복의 중첩|패딩 외투의 후드가 목둘레를 감싸고 장갑 낀 손목 위로 소매가 겹치며 바지 밑단이 부츠 윗부분을 덮는다.|A padded coat's hood surrounds the neck, sleeves overlap gloved wrists, and trouser hems cover the boot tops.|hood>around>neck;sleeve>overlaps>glove.cuff;trousers>cover>boot.top|목·손목 층;부츠 경계;볼륨|보온 성능·국가·혹한기 훈련 여부를 옷의 두께만으로 확정하지 않는다.|garment_detail,material|S01
V12|우의의 빗물|판초의 넓은 면이 어깨와 배낭 위를 덮고 가장자리에서 떨어지는 물방울이 젖은 바닥과 이어진다.|A broad poncho covers the shoulders and rucksack, with droplets falling from its edge onto wet ground.|poncho>covers>shoulders;poncho>covers>rucksack;droplets>from>poncho.edge|배낭 덮임;우의 가장자리;낙수|방수 등급·저체온·성적 의도는 시각 사실이 아니다.|garment_detail,material|S15
V13|전투복의 외형|무늬가 있는 상의와 바지에 바깥 주머니와 여밈선이 보이고 군장 끈은 상의 바깥을 지난다.|A patterned jacket and trousers show external pockets and closure seams, with equipment straps passing over the jacket.|straps>over>jacket;pockets>part_of>uniform|상의·바지;외부 주머니;군장 층|특정 무늬·군복 체계·군종은 별도 지정한다.|wardrobe_style,garment_detail|S01
V14|근무복의 셔츠와 재킷|라펠 재킷 안에 셔츠 칼라와 넥타이가 보이고 바지에는 세로 주름선이 이어진다.|A shirt collar and tie remain visible inside a lapelled jacket above trousers with vertical creases.|tie>over>shirt;jacket>over>shirt|칼라 층;넥타이;바지선|의례복·만찬복·특정 계급을 이 세 부품만으로 단정하지 않는다.|wardrobe_style,garment_detail|S01
V15|의장 장식의 소유자|흰 장갑을 낀 사람의 어깨에서 장식끈이 가슴 앞을 돌아 같은 재킷의 부착점으로 이어진다.|A decorative cord runs from a white-gloved person's shoulder across the chest to an attachment point on that same jacket.|cord>attached_to>jacket.shoulder;cord>ends_at>jacket.chest|같은 재킷;끈의 양 끝;흰 장갑|견식의 자격·계급·군종은 따로 검토한다.|garment_detail,wearable_accessory|S05
V16|작업복의 일체형 경계|넉넉한 원피스 작업복의 앞 지퍼선이 목 아래에서 허리까지 이어지고 무릎과 소매에 기름 얼룩이 남아 있다.|A loose one-piece coverall has a front zipper running from below the neck to the waist, with oil marks on knees and sleeves.|zipper>part_of>coverall;stains>on>coverall|한 벌의 연결;지퍼 연속;얼룩 위치|얼룩은 직급·경험·실제 정비 이력을 증명하지 않는다.|wardrobe_style,material|S01
V17|비행복과 별도 하네스|원피스 비행복 바깥으로 두 어깨 하네스가 내려와 허리의 버클에 이어지고 비행복 지퍼는 그 안쪽에 남는다.|Two shoulder harness straps pass over a one-piece flight suit toward a waist buckle, while the suit zipper remains beneath them.|harness>over>flight_suit;straps>connect_to>buckle|옷과 하네스 분리;버클 연결;지퍼 층|낙하산·사출좌석 결합 여부는 특정 표본 검토까지 주장하지 않는다.|garment_detail,wearable_accessory|S01,S19
V18|컴뱃 셔츠와 휴대구|상의의 몸통은 단색이고 양 소매는 위장무늬이며 그 위에 별도 장비 휴대 조끼가 놓인다.|A shirt has a plain torso and patterned sleeves beneath a separate equipment-carrying vest.|vest>over>shirt;pattern>on>sleeves|몸통과 소매;조끼 별도 경계;목선|재질·난연성·방호판의 존재를 확정하지 않는다.|garment_detail,wardrobe_style|S01,S09
V19|체육복과 놓인 군화|헐렁한 운동복 차림의 사람이 침상 끝에 앉아 있고 바닥에는 벗어 둔 군화 한 켤레가 있다.|A person in loose athletic clothes sits at a bunk edge beside a pair of removed combat boots on the floor.|person>seated_on>bunk;boots>rest_on>floor|앉은 지지;신발 한 켤레;옷과 신발 분리|비전투 생활을 표현하는 대안이며 휴가·말년 신분은 별도 문맥이다.|wardrobe_style,body_pose|S03
V20|트렌치코트의 구성|트렌치코트의 어깨 견장과 겹친 가슴 플랩이 보이고 허리벨트는 같은 코트의 고리를 지난다.|A trench coat shows shoulder epaulettes and an overlapping chest flap, with its belt passing through loops on the same coat.|belt>through>coat.loops;flap>part_of>coat|견장;겹친 플랩;벨트 고리|기존 완결 후보 재사용 검토 대상이며 군인·첩보원 정체성을 만들지 않는다.|garment_detail,wardrobe_style|S06
V21|배틀드레스의 비율|허리에서 끝나는 짧은 재킷 아래로 높은 허리선의 바지가 이어지며 재킷의 주머니와 여밈이 보인다.|A short jacket ends at the waist above high-waisted trousers, with visible jacket pockets and front fastening.|jacket.hem>at>waist;trousers.waist>below>jacket|짧은 상의;높은 허리;여밈|정확한 연식·국가의 Battle Dress 표본은 별도 도판 검토가 필요하다.|wardrobe_style,garment_detail|S06
V22|펠리스 어깨걸침|털 가장자리가 있는 짧은 덧재킷이 한쪽 어깨에 걸리고 끈이 앞가슴을 지나 반대편 고정점에 이어진다.|A short fur-edged overjacket hangs over one shoulder, with a cord crossing the upper chest to an attachment point.|pelisse>hangs_over>shoulder;cord>connects>attachment|짧은 덧재킷;털 경계;지지 끈|돌먼과 같은 옷으로 합치지 않으며 정확한 역사 착장·방향은 보류한다.|garment_detail,wearable_accessory|S07,S08
V23|긴 외투의 무게|두꺼운 긴 외투의 밑단이 무릎 아래로 내려오고 옷의 무게가 큰 세로 주름으로 모인다.|A heavy long coat falls below the knees, its weight gathering into broad vertical folds.|coat.hem>below>knees;folds>on>coat|외투 길이;큰 주름;몸과 외투 경계|울 조성·그레이트코트 연식은 외형만으로 확정하지 않는다.|wardrobe_style,material|S06
V24|각반과 천 퍼티의 차이|왼쪽 표본에는 종아리를 감은 천 띠의 겹친 나선이 있고 오른쪽 표본에는 별도 여밈을 가진 한 장의 각반이 있다.|The left specimen has overlapping spirals of cloth around the calf, while the right specimen has a single gaiter panel with a separate closure.|puttee>spirals_around>calf;gaiter>closes_around>other_calf|두 표본 분리;나선;패널 여밈|비교 표본 모드이며 한 인물의 양쪽 다리에 다른 역사 장구를 자동 조합하지 않는다.|object_structure,garment_detail|S10
V25|접힌 군모와 챙 군모|탁자 왼쪽의 군모는 납작하게 접힌 두 면을 보이고 오른쪽 군모에는 앞으로 돌출한 챙이 있다.|A cap on the left of a table shows two flat folded sides, while another cap on the right has a projecting front peak.|cap_a>left_of>cap_b;peak>part_of>cap_b|별도 모자;접힌 면;앞챙|사이드 캡·정모의 구체적 제식과 소속은 별도 검토한다.|object_structure,prop_state|S01
V26|베레모와 별도 표장|부드러운 챙 없는 모자가 머리에 놓이고 앞옆 면에는 천과 구분되는 작은 금속 표장이 붙는다.|A soft brimless cap rests on the head with a small metal badge distinct from the fabric on its front side.|cap>on>head;badge>attached_to>cap|챙 없음;모자 지지;표장 경계|베레모 색과 badge로 전 세계의 병과·정치적 충성을 통일하지 않는다.|wearable_accessory,garment_detail|S05
V27|계급 표지와 부대표장의 분리|재킷 어깨에는 작은 서열 표지가 있고 소매에는 별도 부대 표장이 있어 두 표지가 서로 다른 면을 차지한다.|A jacket has a small rank marker on the shoulder and a separate unit patch on the sleeve, occupying different surfaces.|rank_marker>on>shoulder;unit_patch>on>sleeve|두 표지 분리;부착 면;크기|가상 배치 대안이며 실제 계급명·표장 모양·복제 규정은 지정된 국가와 시점의 도판이 필요하다.|garment_detail,prop_placement|S01,S02,S05
V28|훈장과 약장의 구분|별도 두 재킷 표본 중 하나에는 리본 아래 금속 메달이 매달리고 다른 하나에는 짧은 직사각형 약장 줄만 붙는다.|Of two separate jacket specimens, one carries metal medals below ribbons, while the other carries short rectangular ribbon bars.|medals>hang_below>ribbons;ribbon_bars>on>other_jacket|표본 경계;매달린 금속;직사각형 약장|훈공·전과·특정 수훈 자격은 시각 사실이 아니다.|garment_detail,object_structure|S01
V29|인식표의 고리|한 손이 금속 식별판 두 장을 들고 같은 체인의 고리가 손가락 사이로 늘어진다.|One hand holds two metal identification plates as loops of the same chain hang between the fingers.|hand>holds>plates;chain>through>plates|두 판;체인 연속;손 소유|글씨를 읽지 못하면 개인 신원·사망·유품의 출처를 주장하지 않는다.|hand_pose,prop_state|S10
V30|열린 캐리어의 판|몸에서 벗겨 탁자에 놓은 캐리어의 상부 수납구가 열려 있고 단단한 판의 윗부분이 같은 수납구 밖으로 나온다.|A carrier removed from the body lies on a table with its upper pocket open and the top of a rigid plate projecting from that same pocket.|plate>inside>carrier.pocket;carrier>rests_on>table|수납구와 판의 연속;판 두께;탁자 지지|착용 중인 닫힌 캐리어의 내부를 투시하지 않으며 방호 등급은 증명하지 않는다.|object_structure,prop_state|S09
V31|얇은 리그와 의복 층|작은 전면 파우치들을 지닌 얇은 패널이 어깨끈과 옆끈으로 몸통 위에 고정되고 셔츠가 가장자리 밖으로 보인다.|A thin panel with front pouches is held over the torso by shoulder and side straps, leaving the shirt visible beyond its edges.|straps>support>panel;panel>over>shirt;pouches>attached_to>panel|패널 경계;끈 연속;별도 셔츠|체스트 리그의 시각 대안이며 방호재 없음 자체를 닫힌 외형만으로 증명하지 않는다.|wearable_accessory,object_structure|S09,S11
V32|PALS의 사다리 격자|평평한 천 표본에 가로 웨빙 줄과 일정한 수직 봉제선이 반복되어 작은 통과 구간들을 만든다.|Horizontal webbing rows and repeated vertical stitches create small passage segments on a flat fabric specimen.|stitches>divide>webbing;webbing>on>fabric|가로 줄;세로 봉제;통과 구간|MOLLE 전체 체계와 동일시하지 않는다. 레이저 컷 별도 방식은 다른 표본이다.|object_structure,material|S10
V33|파우치와 부착면|패널 앞면의 파우치 뒤 끈이 같은 패널의 격자 구간을 지나며 파우치의 위쪽 입구는 닫혀 있다.|A pouch's rear straps pass through grid segments on the same front panel while the pouch's upper opening remains closed.|pouch.straps>through>panel.grid;pouch>attached_to>panel|뒤 끈 경로;같은 패널;입구 상태|격자만 보인다고 파우치 연결·탄창·의료품을 새로 추정하지 않는다.|object_structure,contact_point|S10,S11
V34|웹빙의 하중 경로|양어깨에서 내려온 끈이 허리 장구 벨트에 닿고 여러 수납구가 같은 벨트에서 매달린다.|Straps descend from both shoulders to an equipment belt, with several pouches hanging from that same belt.|straps>connect_to>belt;pouches>hang_from>belt|어깨에서 허리;벨트 연속;수납구 지지|장식용 패션 하네스나 신체 구속 장치로 바꾸지 않는다.|wearable_accessory,object_structure|S10,S11
V35|총기 슬링의 두 끝|한 소총이 몸 앞에 비스듬히 놓이고 슬링은 같은 소총의 앞뒤 부착점에서 어깨를 돌아 이어진다.|A rifle lies diagonally before the torso, its sling running from front and rear attachment points on that same rifle around the shoulder.|sling>attached_to>rifle.front;sling>attached_to>rifle.rear;sling>over>shoulder|같은 총;두 끝;어깨 지지|소총을 새로 추가하는 효과가 있으며 슬링만 필요한 요청에 무기 전체를 강제하지 않는다.|wearable_accessory,object_structure|S10,S12
V36|홀스터와 장구 벨트|허리 벨트 바깥쪽에 단단한 수납구가 고정되고 권총 손잡이 일부가 같은 수납구 위로 드러난다.|A rigid holster is attached outside a waist belt, with part of a pistol grip visible above that same holster.|holster>attached_to>belt;pistol>inside>holster|벨트 연결;수납구 입구;손잡이|권총의 장전 상태·사용 권한·공격 의도는 외형에 없다.|wearable_accessory,prop_state|S10,S12
V37|음용관의 연결|배낭 위쪽에서 나온 가는 관이 같은 사람의 어깨끈을 따라 내려오고 끝의 마우스피스가 가슴 앞 클립에 걸린다.|A narrow tube emerges from the upper rucksack, follows the same person's shoulder strap, and ends in a mouthpiece clipped at the chest.|tube>from>rucksack;tube>along>strap;mouthpiece>clipped_to>chest_clip|관 시작;어깨 경로;마우스피스 끝|산소·수액관과 합치지 않으며 물의 존재·청결을 주장하지 않는다.|object_structure,wearable_accessory|S11
V38|헤드셋의 마이크 끝|헤드밴드가 같은 사람의 양 귀컵을 연결하고 한 귀컵에서 나온 붐 마이크가 입 옆에서 끝난다.|A headband connects the ear cups on the same person's head, and a boom microphone extends from one cup to a point beside the mouth.|headband>connects>ear_cups;mic>from>ear_cup;mic.tip>beside>mouth|같은 머리;붐 시작과 끝;입과 거리|실제 교신·청력보호·소음 차단 성능은 보장하지 않는다.|wearable_accessory,object_structure|S11
V39|들어 올린 야시경|헬멧 앞의 마운트에서 짧은 팔이 올라가 광학 장치를 이마 위에 지지하고 착용자의 눈은 아래에 드러난다.|A short arm rises from the helmet's front mount to support an optical device above the forehead, leaving the wearer's eyes visible below.|mount>attached_to>helmet;arm>supports>device;device>above>eyes|마운트;지지 팔;눈과 장치 위치|NVG 작동·열영상 기능·임무의 은밀함은 외형만으로 확정하지 않는다.|wearable_accessory,prop_state|S09,S19
V40|눈앞으로 내린 야시경|헬멧 마운트에 연결된 광학 장치가 눈앞으로 내려오고 연결 팔은 헬멧과 장치 사이를 잇는다.|An optical device is lowered before the eyes from a helmet mount, its connecting arm spanning helmet and device.|arm>connects>helmet_mount;device>before>eyes|같은 장치;눈앞 위치;마운트 연결|올림 상태와 동시 채택하지 않으며 녹색 발광을 눈·현실 공간에 자동 추가하지 않는다.|wearable_accessory,prop_state|S09,S19
V41|열영상 화면의 경계|휴대형 장치의 작은 화면 안에 명암이 다른 인체 모양이 표시되고 화면 밖의 실제 풍경은 다른 색조로 남는다.|A handheld device's small screen contains a high-contrast human-shaped image, while the actual landscape outside the screen retains different tones.|depicted_shape>inside>screen;screen>part_of>device|장치 테두리;화면 안 인체상;실물 경계|화면의 인물과 실물의 신원·온도·적대성·센서 정확도는 증명하지 않는다.|prop_state,presentation_style|S19
V42|방독면과 필터|고무 재질 얼굴 덮개가 코와 입을 가리고 둥근 필터가 같은 마스크 측면에 결합되며 머리끈이 뒤쪽으로 이어진다.|A rubber-like facepiece covers nose and mouth, with a round filter joined to its side and head straps extending behind the head.|filter>attached_to>mask;mask>covers>nose_mouth;straps>around>head|필터 접합;얼굴 덮임;머리끈|밀착·필터 수명·실제 오염·위험 종류는 추가 문맥이다.|wearable_accessory,object_structure|S10
V43|무릎 보호대의 소유자|단단한 보호판이 같은 사람의 굽힌 무릎 앞에 놓이고 두 끈이 다리 뒤로 돌아 고정된다.|A rigid pad lies over the front of the same person's bent knee, with two straps running behind the leg.|pad>over>knee;straps>around>leg|무릎 소유;판과 옷 층;끈 경로|의복 일체형과 외부 스트랩형을 동시에 주장하지 않는다.|wearable_accessory,garment_detail|S10
V44|고글과 별도 헬멧|고글의 두 렌즈가 눈앞에 있고 고무 밴드가 머리 뒤를 감싸며 헬멧 가장자리는 그 위에 남는다.|Two goggle lenses sit before the eyes, their elastic band wrapping behind the head beneath the helmet edge.|goggles>before>eyes;band>around>head;helmet>above>goggles|렌즈;밴드 연속;헬멧 층|방탄 인증·시력·눈빛을 가려도 정확한 시선 판독이 된다고 주장하지 않는다.|wearable_accessory,object_structure|S09
V45|설상 덧옷의 열린 부분|흰 덧옷이 몸통과 팔을 덮고 열린 목둘레와 소매 끝에 안쪽 유색 의복이 보인다.|A white overgarment covers torso and arms, with colored inner clothing visible at the open neck and sleeve ends.|white_layer>over>inner_clothes|흰 겉층;목 경계;손목 경계|설상 위장 효율·겨울 훈련·특정 위장 체계를 증명하지 않는다.|wardrobe_style,garment_detail|S01
V46|위장무늬 비교 표본|한 천 표본에는 작은 각진 반점이 반복되고 다른 표본에는 더 큰 곡선형 얼룩이 있어 두 무늬가 분리된다.|One fabric specimen repeats small angular patches while another has larger curved blotches, keeping the patterns separate.|pattern_a>on>fabric_a;pattern_b>on>fabric_b|별도 표본;각진 반점;곡선 얼룩|디지털이라는 이름만으로 특정 국가·적외선 성능·OCP를 지정하지 않는다.|material,object_structure|S01
V47|먼지와 마모의 위치|부츠 밑창과 바지 밑단에는 마른 흙이 붙고 재킷 팔꿈치의 돌출부에는 옅은 마모가 남는다.|Dry earth clings to boot soles and trouser hems, with pale wear on the projecting elbows of the jacket.|earth>on>boot_soles;wear>on>jacket.elbows|마모 부위;의복과 피부 구분;표면|전투 경험·가난·베테랑·손상의 원인을 외형으로 단정하지 않는다.|material,garment_detail|S15
V48|헬멧과 묶은 머리|뒤로 낮게 묶은 머리가 헬멧 뒷가장자리 아래에 놓이고 턱끈은 귀 아래에서 턱 쪽으로 이어진다.|Hair tied low at the back lies below the helmet's rear edge, while the chin strap runs beneath the ears toward the chin.|hair>below>helmet.edge;chinstrap>under>ears|머리·헬멧 경계;끈 경로;턱 접점|모든 군인의 머리를 삭발로 통일하지 않으며 현행 군별 허용 규정은 별도 검토한다.|hair_style,wearable_accessory|S01
V49|거수경례의 연결|펴서 모은 오른손 손가락이 이마 옆에 놓이고 손목·팔꿈치·같은 어깨가 연결되며 왼손은 몸 옆에 남는다.|Straight grouped fingers of the right hand lie beside the forehead, with wrist and elbow connected to the same shoulder while the left hand remains at the side.|right_hand>near>forehead;elbow>belongs_to>same_arm;left_hand>beside>torso|손 소유;팔의 연속;반대 손|특정 손바닥 방향·군종식 경례는 지정된 도판 확인 전 고정하지 않는다.|hand_pose,body_pose|S13
V50|차렷의 정렬|선 인물의 양발 뒤꿈치가 가까이 있고 두 팔이 몸 옆으로 내려오며 몸통은 수직으로 정렬된다.|A standing person's heels are close together, both arms hang beside the body, and the torso aligns vertically.|feet>support>body;arms>beside>torso|발과 바닥;팔 위치;몸통 축|엄밀한 국가별 발 각도·손가락 모양·정신 상태를 이 일반 대안에 넣지 않는다.|body_pose|S13
V51|쉬어 자세의 손 위치|선 인물의 두 발이 떨어져 있고 두 손은 허리 뒤 같은 높이에서 포개지며 양 팔꿈치가 바깥으로 굽는다.|A standing person's feet are apart, both hands overlap behind the waist at one level, and both elbows bend outward.|hands>behind>waist;feet>apart_on>ground|두 손 소유;허리 뒤;발 지지|정확한 parade rest 변형·복종 감정은 별도 문맥이다.|body_pose,hand_pose|S13
V52|줄 맞춘 행진의 순간|평행한 두 줄의 인원에서 앞줄 사람들의 같은 쪽 발이 앞으로 나와 있고 옆 사람 사이 간격이 이어진다.|In two parallel files, front-row people extend the same-side foot forward while intervals continue between adjacent people.|person_a>beside>person_b;files>parallel_to>each_other|줄 연속;발의 순간;간격|모든 팔다리를 동기화된 움직임으로 증명하거나 행진 전체 순서를 한 프레임에 넣지 않는다.|body_pose,composition|S13
V53|낮게 둔 소총의 외형|소총을 몸 앞에서 두 손으로 지지하고 총구는 시선보다 아래를 향하며 총열과 손가락이 분리되어 보인다.|Two hands support a rifle before the body, its muzzle directed below the line of sight with barrel and fingers separately visible.|hands>support>rifle;muzzle>below>gaze_axis|총구 방향;두 손 소유;총의 연속|작전 수행·사격 준비 절차·안전 인증을 설명하는 카드가 아니다.|body_pose,prop_state|S12
V54|견착의 접점|같은 소총의 개머리판이 어깨 앞에 닿고 한 손은 앞쪽을 받치며 얼굴의 시선이 소총 길이 방향을 따른다.|The butt of one rifle contacts the front of the shoulder, one hand supports its fore-end, and the face looks along the rifle's length.|rifle.butt>contacts>shoulder;hand>supports>foreend;gaze>along>rifle|견착 접점;같은 총;시선 축|발사·명중·적의 존재·실제 조작법을 부여하지 않는다.|contact_point,gaze_target|S12
V55|한쪽 무릎과 반대 발|한 무릎은 지면에 닿고 반대쪽 발바닥이 앞쪽 바닥을 지지하며 몸통은 두 지지점 위에 놓인다.|One knee touches the ground while the opposite foot supports the body in front, with the torso above those supports.|knee>contacts>ground;opposite_foot>supports>body|무릎 소유;반대 발;균형|관측·돌봄·복종·부상 중 어느 사건인지 자세만으로 정하지 않는다.|body_pose,contact_point|S13
V56|엎드린 관찰의 지지|인물의 배와 허벅지가 지면에 가깝고 두 팔꿈치가 앞쪽 바닥을 받치며 머리는 낮게 들린다.|A person's abdomen and thighs remain close to the ground, both elbows support the front of the body, and the head is held low.|elbows>support>torso;abdomen>near>ground|몸·지면;양 팔꿈치;목 연결|은폐 성공·저격수 자격·전투 상황은 문맥이다.|body_pose,contact_point|S13
V57|쌍안경의 손과 눈|두 손이 같은 쌍안경의 양쪽 몸통을 잡고 접안부 두 개가 같은 인물의 눈앞에 놓인다.|Both hands grip the two barrels of one binocular, with its paired eyepieces positioned before the same person's eyes.|hands>grip>binocular;eyepieces>before>eyes|같은 장치;두 접안부;손 소유|대상의 정체·거리·관찰 성과는 별도 문맥이다.|hand_pose,gaze_target|S16
V58|무전 수화기의 연결|한 손이 수화기를 귀와 입 사이에 대고 꼬인 케이블이 같은 수화기에서 허리의 무전 본체로 이어진다.|One hand holds a handset between ear and mouth, with a coiled cable running from that same handset to a radio body at the waist.|hand>holds>handset;cable>connects>handset;cable>connects>radio|손;수화기 양끝 위치;케이블 양끝|교신 성공·발화 내용·Roger/Wilco는 정지영상으로 증명하지 않는다.|hand_pose,object_structure|S16
V59|지도의 같은 지점을 보는 사람들|탁자 위 펼친 지도의 한 지점을 한 사람이 짚고 반대편 두 사람의 얼굴이 그 지점을 향한다.|One person points to a spot on a map spread over a table as two people opposite direct their faces toward that same spot.|finger>points_to>map.spot;faces>toward>map.spot;map>on>table|한 지점;세 사람 분리;지도 지지|지도 기호가 실제 전황·명령·합동 작전을 증명하지 않는다.|gaze_target,relational_action|S16
V60|해치와 상체의 연속|차량 상부의 열린 원형 해치 안에서 인물의 허리가 이어지고 양팔은 해치 가장자리 위에 놓인다.|A person's waist continues into an open circular hatch atop a vehicle, with both arms resting on its rim.|waist>inside>hatch;arms>rest_on>hatch.rim|상하체 연속;해치 테두리;팔 지지|차량 모델·승무원 직책·전투 능력은 해치만으로 확정하지 않는다.|body_pose,contact_point|S04
V61|조종석의 좌석과 하네스|인물의 골반이 조종석 좌석에 놓이고 어깨끈이 가슴 앞을 지나며 계기판은 무릎 앞에 따로 놓인다.|A person's pelvis rests in a cockpit seat, shoulder straps cross the chest, and an instrument panel stands separately before the knees.|seat>supports>pelvis;straps>over>chest;panel>before>knees|좌석 지지;끈;계기판 공간|정확한 항공기·사출좌석·비행 중 상태·조종 자격은 별도 표본과 문맥이다.|body_pose,location|S01
V62|차량 아래 정비의 공간|고정 지지대 위에 놓인 차량 아래에서 사람이 낮은 이동판에 누워 위로 손을 뻗고 바퀴는 몸 옆에 떨어져 보인다.|Beneath a vehicle on fixed stands, a person lies on a low creeper and reaches upward, with a wheel visibly clear of the body.|stands>support>vehicle;creeper>supports>person;hand>toward>underside|차량 지지대;몸 공간;뻗는 팔|보이는 지지는 실제 작업 안전성·수리 절차의 인증이 아니다.|body_pose,contact_point|S11
V63|초소와 대기 인물|작은 초소 출입구 옆에 선 사람이 한 손으로 난간을 잡고 앞쪽 도로를 바라본다.|A person stands beside a small guard-post entrance, holding a rail with one hand and facing the road ahead.|hand>holds>rail;person>beside>entrance;face>toward>road|난간 접점;출입구;도로 방향|민간인을 적으로 부여하거나 모든 초소에 사격을 추가하지 않는다.|location,gaze_target|S20
V64|벽에 기대앉은 휴식|인물의 등이 벽에 닿고 엉덩이가 바닥을 지지하며 헬멧은 무릎 옆 바닥에 놓인다.|A person's back rests against a wall, hips are supported by the ground, and a helmet lies beside the knees.|back>against>wall;hips>on>ground;helmet>beside>knees|벽 접촉;골반 지지;헬멧 별도|패배·정신질환·사망을 축 처진 자세로 단정하지 않는다.|body_pose,prop_placement|S23
V65|옆구리의 헬멧|굽힌 팔뚝과 옆구리 사이에 헬멧이 끼워지고 손은 헬멧 아래 가장자리를 받친다.|A helmet is tucked between a bent forearm and the side of the torso, with the hand supporting its lower edge.|helmet>between>forearm_torso;hand>supports>helmet.rim|같은 팔;측면 공간;손 지지|헬멧을 머리에도 동시에 씌우지 않으며 계급·감정은 별도 문맥이다.|hand_pose,prop_state|S01
V66|전우 부축의 두 주인|기댄 사람의 한 팔이 돕는 사람의 양어깨 쪽으로 놓이고 돕는 사람의 손은 상대 허리를 감싸며 두 사람 발이 바닥에 남는다.|One person's arm rests across the helper's shoulders, the helper's hand supports that person's waist, and both retain foot contact with the ground.|person_a.arm>over>helper.shoulders;helper.hand>supports>person_a.waist;feet>on>ground|팔 소유;허리 손;발과 체중|부상·동의·전우 관계·이송 성공은 이 접점만으로 증명하지 않는다.|relational_action,contact_point|S17
V67|들것 양끝의 같은 프레임|두 운반자의 손이 같은 들것의 앞뒤 손잡이를 잡고 누운 사람의 몸이 그 들것 천 위에 길게 지지된다.|Two carriers grip the front and rear handles of one stretcher, with a reclining person's body supported along its fabric.|carrier_a.hand>grips>front_handle;carrier_b.hand>grips>rear_handle;fabric>supports>patient|같은 프레임;앞뒤 접점;몸 지지|바퀴 들것과 도수 운반용을 합치지 않는다. MEDEVAC·의료 능력은 문맥이다.|relational_action,contact_point|S17
V68|유품을 든 고개|한 사람이 작은 금속 표지를 양손 안에 받치고 고개를 숙여 그 손 쪽으로 얼굴을 향한다.|A person cups a small metal token in both hands and bows the head toward those hands.|hands>support>token;face>toward>hands|표지 소유;손·얼굴 방향;몸 지지|물건이 실제 유품인지·사망·슬픔의 원인을 판정하지 않는다.|hand_pose,gaze_target|S23
V69|재회 포옹의 팔 연결|군복 차림 사람과 사복 차림 사람이 마주 안고 각자의 팔이 상대 등으로 이어지며 양쪽 발은 현관 바닥을 딛는다.|A uniformed person and a civilian-dressed person embrace face to face, their arms continuing around each other's backs while both stand on an entry floor.|person_a.arms>around>person_b.back;person_b.arms>around>person_a.back;feet>on>floor|두 팔 소유;등 접점;발 지지|가족·연인·합의·귀환 이력은 요청 문맥으로만 확정한다.|relational_action,contact_point|S26
V70|지휘실의 실물과 화면|두 사람이 탁자 앞에 서고 벽 화면의 지도 테두리는 실물 탁자와 구분되며 한 사람 손은 탁자 지도를 짚는다.|Two people stand at a table, a wall display's map border remains distinct from the physical table, and one hand points to the table map.|hand>points_to>physical_map;display_map>inside>screen|화면 테두리;실물 지도;손 대상|C2·ISR·전황·데이터 신뢰·지휘권을 화면 장식으로 증명하지 않는다.|location,presentation_style|S16
V71|참호의 통로와 낮은 몸|흙벽 사이 좁은 통로 바닥에 판자가 이어지고 인물의 어깨가 흙벽 상단보다 낮게 놓인다.|Planks run along a narrow passage between earthen walls, with a person's shoulders below the wall tops.|planks>on>passage.floor;shoulders>below>earth_wall.top|통로;판자;벽 높이|국가·전쟁 연도·정확한 진지 설계·적 위치를 단정하지 않는다.|location,spatial_depth|S15
V72|벙커의 출입 경계|두꺼운 벽의 낮은 입구 안쪽에 인물이 있고 좁은 개구를 통한 바깥 빛이 바닥에 떨어진다.|A person stands inside a low entrance through a thick wall, while exterior light falls through the narrow opening onto the floor.|person>inside>bunker;light>through>opening|벽 두께;안팎;출입 공간|방호 성능·봉쇄·감금·초자연적 원인을 형태만으로 확정하지 않는다.|location,lighting|S20
V73|함정 통로와 격벽|좁은 금속 통로 양쪽에 격벽이 이어지고 한 격벽의 출입구 아래에 높은 문턱이 보인다.|Bulkheads line a narrow metal passage, with a raised sill beneath a doorway in one bulkhead.|doorway>through>bulkhead;sill>below>doorway|격벽;출입구;문턱|수밀 성능·잠항 중 여부·특정 잠수함 내부는 따로 검토한다.|location,object_structure|S14
V74|함교의 전방 시야|여러 전방 창 아래 조종·항해 콘솔이 있고 인물은 콘솔 뒤에서 창밖 수평선을 바라본다.|Navigation consoles sit below forward windows, and a person behind them faces the horizon outside.|consoles>below>windows;person>behind>consoles;gaze>toward>horizon|창;콘솔;수평선|함장 계급·자동 항해·군함 종류는 문맥이며 항공기 flight deck과 합치지 않는다.|location,gaze_target|S14
V75|격납고의 열린 동선|큰 격납고 안의 항공기 옆에 낮은 정비 발판과 공구함이 있고 인물 통로가 기체 아래와 분리된다.|Beside an aircraft in a large hangar stand a low maintenance platform and tool chest, leaving a personnel aisle clear of the underside.|platform>beside>aircraft;aisle>clear_of>underside|기체 규모;발판;통로|기종·정비 성공·출격 예정은 별도 문맥이다.|location,spatial_depth|S31
V76|검문소의 상호 위치|차단봉 양쪽에 제복 인물과 민간복 인물이 마주 서며 민간복 인물 손의 서류가 두 사람 사이에 놓인다.|A uniformed person and a civilian-dressed person face each other across a barrier, with a document held between them by the civilian-dressed person.|barrier>between>people;document>held_by>civilian;faces>toward>each_other|차단봉;서류 주인;상호 얼굴|의심·범죄·적대성·통과 허가·정체를 외형에서 새로 부여하지 않는다.|location,relational_action|S20
V77|야전 진료 구역|천막 안에 들것 두 개가 떨어져 놓이고 의료 가방과 작업등은 한 들것 옆 공간에 있다.|Two stretchers are spaced apart inside a tent, with a medical bag and task light beside one of them.|stretchers>separated_in>tent;bag>beside>stretcher|두 들것;빈 간격;가방·등|의료 자격·실제 치료·위생·진단은 물건으로 증명하지 않는다.|location,prop_placement|S17
V78|추모비의 사람과 빈 공간|추모비 앞에 한 사람이 서서 꽃을 들고 있고 사람과 비석 사이에 비어 있는 바닥이 남는다.|A person holding flowers stands before a memorial stone with an open strip of ground between person and stone.|hand>holds>flowers;ground>between>person_stone|꽃 주인;비석;거리|실제 사망자·군 경력·유족·도덕적 손상은 문맥이다.|location,proxemics|S23
V79|정렬된 의례 구도|인물 줄이 화면 중앙 축을 기준으로 좌우에 나뉘고 가운데 통로가 멀리까지 이어진다.|Rows of people divide on either side of the frame's central axis, with a central aisle receding into the distance.|rows>on_sides_of>central_axis;aisle>between>rows|대칭 축;통로;반복|국가 권력·선전 지지·집단의 의도는 구도 자체와 다르다.|composition,spatial_depth|S29
V80|계기판 빛의 얼굴|어두운 조종석에서 계기판이 내는 작은 빛이 앉은 인물의 턱과 볼 아래쪽을 비춘다.|In a dark cockpit, small instrument lights illuminate the lower cheek and chin of a seated person.|light>from>instruments;light>falls_on>lower_face|광원;얼굴 부위;좌석|조종 능력·불안·경보·비행 상태는 조명만으로 확정하지 않는다.|lighting|S01
V81|진흙 표면과 얼굴의 분리|얼굴 옆과 옷깃에 마른 흙 자국이 남고 눈가와 입의 피부 경계는 그대로 읽힌다.|Dried earth marks the side of a face and clothing collar while the skin boundaries around eye and mouth remain readable.|earth>on>face;earth>on>collar|피부·옷 경계;흙;눈과 입|피부색·민족·부상·전투 경험과 흙을 혼동하지 않는다.|material,face_detail|S15
V82|방향이 먼 시선|앉은 인물의 얼굴이 앞을 향하지만 눈의 시선축은 가까운 손 안의 물건을 향하지 않고 그 너머로 이어진다.|A seated person's face points forward, but the eye axis passes beyond rather than toward the object in nearby hands.|gaze>past>near_object|눈의 판독;대상 거리;얼굴 방향|천 야드 응시의 가능한 외형이며 PTSD·무감정·의식 상태는 진단하지 않는다.|gaze_target,facial_expression|S23
V83|노즈아트의 곡면 경계|항공기 코의 곡면 위에 그려진 인물 그림이 패널선과 함께 휘어지고 실제 정비 인물은 그 곁 바닥에 선다.|A painted figure curves with the aircraft nose and its panel lines, while a real maintainer stands on the floor beside it.|painted_figure>on>aircraft.nose;panel_lines>across>paint;maintainer>beside>aircraft|곡면;패널선;그림·실물 분리|그림 속 인물은 실물 인물 수에 합산하지 않으며 모델·미술가·연대는 따로 검토한다.|presentation_style,object_structure|S31
V84|비핀업 노즈아트|항공기 코의 양쪽에 상어입 모양의 이빨 그림이 도장면 위로 이어지고 기체의 금속 패널 경계가 보인다.|A shark-mouth tooth motif extends across the painted sides of an aircraft nose while metal panel boundaries remain visible.|shark_motif>painted_on>aircraft.nose|그림 면;이빨 모티브;기체 경계|노즈아트를 성적 그림의 동의어로 만들지 않는다. 정확한 기체 표본은 보류다.|object_structure,presentation_style|S34
V85|성인 밀리터리 패션|성인 모델이 짧은 견장 재킷과 높은 허리선의 치마를 입고 별도 군모를 한 손에 든다.|An adult model wears a cropped epaulette jacket and high-waisted skirt, holding a separate military-style cap in one hand.|jacket>over>torso;hand>holds>cap|짧은 재킷;치마;모자 손 지지|패션 대안이며 실제 군복·군인 신분·동의·계급을 증명하지 않는다.|wardrobe_style,hand_pose|S06
V86|열린 재킷과 안쪽 의복|성인 인물의 재킷 앞이 열리고 안쪽 상의의 앞면이 그 틈으로 드러나며 양 라펠이 바깥으로 떨어진다.|An adult person's jacket is open, revealing an inner top through the gap as both lapels fall outward.|jacket>open_over>inner_top|여밈 상태;옷 층;라펠|이 대안의 안쪽 상의는 명시적 구성이다. 열린 재킷 일반어에 내의·노출·성적 의도를 강제하지 않는다.|garment_detail,wardrobe_style|S06
V87|가터의 실제 접점|성인 모델의 가터 끈 끝 클립이 같은 다리 스타킹의 윗밴드를 잡고 끈은 허리 쪽의 의복으로 이어진다.|A garter strap's end clip grips the top band of a stocking on the same adult model's leg, with the strap continuing toward a waist garment.|clip>grips>stocking.band;strap>connects>clip;strap>toward>waist_garment|같은 다리;클립;상부 끈|독립 허벅지 밴드·군장 하중끈과 다르며 성적 동의는 별도 문맥이다.|wearable_accessory,contact_point|S06
V88|패션 하네스의 구조|성인 모델의 재킷 바깥으로 가는 장식끈이 몸통을 두르고 가슴의 작은 링에서 만나며 파우치는 달리지 않는다.|Thin decorative straps encircle an adult model's jacketed torso and meet at a small chest ring, without attached pouches.|straps>over>jacket;straps>meet_at>ring|옷 바깥;링 연결;장식끈 경로|여기서 파우치 없음은 이 대안의 명시적 구성일 뿐 모든 패션 하네스의 정의가 아니다. 군장·구속으로 전용하지 않는다.|wearable_accessory,object_structure|S06
V89|장화와 바지의 경계|성인 모델의 긴 부츠 윗선이 허벅지에 놓이고 바지나 치마의 밑단과 구분되며 굽이 바닥을 지지한다.|An adult model's tall boot top lies at the thigh, distinct from a trouser or skirt hem, with the heel supporting the foot on the floor.|boot.top>at>thigh;heel>on>floor|부츠 윗선;의복 경계;굽 지지|전투화·방호구 성능·성적 역할은 외형과 다른 문맥이다.|wearable_accessory,garment_detail|S06
V90|광택 제복 소재|성인 모델의 몸에 맞는 가상 제복에서 넓은 반사광이 굽은 소매와 몸통을 따라 이어지고 봉제선은 따로 읽힌다.|Broad highlights follow the curved sleeves and torso of an adult model's fitted fictional uniform, with seams remaining distinct.|highlights>on>uniform;seams>part_of>uniform|반사광;봉제;몸과 옷|광택만으로 라텍스·가죽·실제 군 제식·성적 행위를 확정하지 않는다.|material,wardrobe_style|S06
V91|어깨 코트의 지지|성인 인물의 코트 양 어깨 부분이 몸의 어깨에 걸리고 빈 소매는 양옆으로 늘어지며 두 팔은 소매 밖에 남는다.|A coat rests on an adult person's shoulders, its empty sleeves hanging at the sides while both arms remain outside them.|coat>rests_on>shoulders;arms>outside>coat.sleeves|빈 소매;어깨 지지;팔 소유|펠리스·군인 권한·우월한 성격과 동일시하지 않는다.|garment_detail,body_pose|S06,S07
V92|젖은 의복의 표면|성인 인물의 셔츠에서 젖어 어두워진 구역이 마른 구역과 나뉘고 소매 끝에 작은 물방울이 맺힌다.|An adult person's shirt shows darker wet patches beside dry areas, with small droplets at the sleeve ends.|wet_patch>on>shirt;droplets>on>sleeve.edge|젖음 경계;물방울;옷 소유|젖은 옷만으로 투명화·노출·질병·성적 초대를 추가하지 않는다.|material,garment_detail|S06
V93|의족과 지지면|바지를 걷은 사람의 한쪽 무릎 아래에 의족 연결부가 드러나고 같은 의족 발이 바닥을 딛는다.|Below one knee of a person with a raised trouser hem, a prosthetic connection is visible and that prosthetic foot contacts the floor.|prosthesis>below>knee;prosthetic_foot>on>floor|신체와 장치;발·바닥;바지 경계|절단 원인·전쟁 경력·재활 성과·능력 전체를 신체 차이로 단정하지 않는다.|body_detail,contact_point|S20
V94|붕대와 외부 옷의 경계|한 인물의 팔뚝을 감싼 붕대가 소매 아래에서 드러나고 붕대 끝은 같은 감김 위에 고정된다.|A bandage around one person's forearm emerges below the sleeve, with its end secured over the same wrapping.|bandage>around>forearm;bandage.end>on>wrapping|팔 소유;감김 연속;소매 경계|출혈 정도·진단·전상·치료 성공·고어를 자동 추가하지 않는다.|body_detail,garment_detail|S17
V95|가상 군사 SF의 보급|가상 제복 인물 두 명이 밀폐문 앞에서 같은 물자 컨테이너를 밀고 문틀의 조명은 사람과 구분된다.|Two people in fictional uniforms push one supply container before a sealed door, with frame lights distinct from their bodies.|hands>push>container;container>before>door|같은 컨테이너;손 접점;문 경계|압력·우주·자원 부족·전쟁 윤리·봉쇄는 문과 제복만으로 증명하지 않는다.|relational_action,location|S30
V96|병기 의인화의 장착 경계|성인 가상 캐릭터의 등 하네스에 소형 함선 모티브 장식이 달리고 실제 팔과 장식의 포신 모양이 분리되어 보인다.|A miniature ship-motif ornament is attached to an adult fictional character's back harness, with real arms visibly distinct from decorative barrel shapes.|ornament>attached_to>harness;harness>on>character.back|장착 지지;팔·장식 구분;모티브 크기|실제 함선 운용·정체·모든 밀리터리 모에의 성인성이나 성적 성격을 정의하지 않는다.|object_structure,wearable_accessory|S30
V97|길리 슈트의 추가 섬유|기본 상의 바깥에 불규칙한 천 조각과 섬유가 매달려 어깨 윤곽을 끊고 일부 틈으로 바탕 옷이 보인다.|Irregular cloth strips and fibers hang outside a base jacket, breaking its shoulder outline while gaps reveal the underlying garment.|fibers>attached_to>base_jacket;strips>outside>shoulders|바탕층;추가 섬유;윤곽 분절|프린트 위장과 다르며 실제 은폐·저격수 자격·무기 추가를 뜻하지 않는다.|garment_detail,material|S40
V98|장갑차의 열린 승하차 경계|궤도 차량 뒤의 열린 출입구와 경사판이 이어지고 한 인물의 발은 경사판 위에 다른 발은 차량 안에 놓인다.|An open rear doorway on a tracked vehicle meets a ramp, with one person's foot on the ramp and the other inside the vehicle.|ramp>meets>rear_doorway;foot_a>on>ramp;foot_b>inside>vehicle|같은 출입구;발 소유;내외 공간|APC·IFV·지휘차를 이 구조 하나로 구분하지 않는다. 특정 모델의 동선은 도판 확인이 필요하다.|object_structure,contact_point|S36
V99|포탑과 궤도 차체|낮은 궤도 차체 위에 회전 포탑 형태가 놓이고 긴 포신 하나가 포탑 앞쪽으로 이어진다.|A low tracked hull supports a turret form, with one long barrel continuing from its front.|turret>on>tracked_hull;barrel>from>turret|포신 연속;포탑 지지;궤도|전차·자주포의 역할·정확한 기종은 실루엣 하나로 확정하지 않는다.|object_structure|S36
V100|높은 차량과 하부 형상|바퀴 차량의 객실이 바퀴 위로 높이 놓이고 아래에서 본 차체 바닥은 가운데 능선을 가진 양쪽 경사면으로 읽힌다.|A wheeled vehicle's cabin sits high above the wheels, while the underside reads as two sloping surfaces meeting at a central ridge.|cabin>above>wheels;underside.slopes>meet_at>ridge|객실 높이;하부 관찰각;두 경사면|MRAP 관련 외형 대안이며 실제 내폭 성능·생존·현재 운용 국가를 주장하지 않는다.|object_structure,spatial_depth|S38
V101|수송헬기 객실의 크기|헬기의 넓은 옆문 안쪽에 나란한 좌석들이 보이고 문 앞 인물은 객실 바닥보다 아래 발판에 선다.|Rows of seats are visible inside a helicopter's broad side doorway, with a person standing on a step below the cabin floor.|seats>inside>cabin;step>below>cabin.floor;person>on>step|문·좌석;바닥 높이;발판 지지|모든 수송헬기가 같은 문·좌석을 쓰지 않으며 MEDEVAC·상륙·공중강습을 자동 부여하지 않는다.|location,object_structure|S37
V102|비성적 구금 접점|옷을 입은 인물의 두 손목에 별도 금속 고리가 놓이고 짧은 사슬이 두 고리 사이를 잇는다.|Separate metal cuffs surround a clothed person's wrists, joined by a short chain between the two cuffs.|cuff_a>around>wrist_a;cuff_b>around>wrist_b;chain>joins>cuffs|같은 인물 손목;두 고리;사슬 연속|이 외형은 구금·포로의 법적 지위·학대·죄·동의·성적 의미를 증명하지 않는다.|wearable_accessory,contact_point|S20
V103|옷의 찢김과 피부 경계|소매 천의 찢어진 두 가장자리가 벌어져 안쪽 팔 피부가 보이고 천 조각은 같은 소매에 이어져 있다.|Two torn edges of a sleeve separate to reveal the arm beneath, while the loose cloth remains connected to that same sleeve.|torn_edges>part_of>sleeve;skin>beneath>sleeve_gap|찢김 끝;같은 소매;피부 층|옷 손상과 신체 훼손·전상·공격 원인을 합치지 않는다.|garment_detail,material|S20
V104|피의 색 묘사와 물질 주장|소매의 일부에 짙은 붉은 얼룩이 있고 가장자리의 번짐이 마른 천 위에 남아 있다.|A dark red stain marks part of a sleeve, with feathered edges against dry cloth.|red_stain>on>sleeve;feathered_edge>part_of>stain|옷 소유;얼룩 경계;붉은 색|붉은색만으로 혈액·폭력·출혈·사망을 증명하지 않는다. 명시적 혈액 요청은 물질 의미를 별도로 유지해야 한다.|material,garment_detail|S20
'''

cards=[]
for line in CARD_TEXT.strip().splitlines():
    cid,title,ko,en,graph,gates,boundary,slots,sids=line.split('|')
    triples=[dict(zip(['from','relation','to'],g.split('>'))) for g in graph.split(';')]
    cards.append(dict(id=cid,title_ko=title,positive_ko=ko,positive_en=en,
        owner_nodes=sorted({x[k] for x in triples for k in ['from','to']}),relations=triples,
        observable_gates=gates.split(';'),confusion_boundary_ko=boundary,
        suggested_slots=slots.split(','),source_ids=sids.split(','),
        source_support_scope='Bounded definitions and confusion boundaries only; all scene geometry is independently authored.',
        mode='authored_research_option',runtime_importable=False,native_approval=False,
        readiness='requires_whole_source_review_and_current_schema_mapping',
        activation='optional_post_core_only',whole_case_policy='partial_is_fail',
        unobservable_policy='UNOBSERVABLE_NOT_PASS'))
save('semantic-cards.json',cards)

# Resolve proposal names against the actual current catalog; these are still
# research suggestions, never automatically approved runtime bindings.
for card in cards:
    mapping={'material':'surface_material','facial_expression':'expression',
             'face_detail':'skin_condition','body_detail':'object_structure'}
    card['suggested_slots']=[mapping.get(s,s) for s in card['suggested_slots']]
    if card['id'] in ['V32','V46','V104']:
        card['suggested_slots']=[('surface_pattern' if s=='surface_material' else s) for s in card['suggested_slots']]
    if card['id']=='V92':
        card['suggested_slots']=['surface_moisture','garment_detail']
    if card['id']=='V94':
        card['suggested_slots']=['wearable_accessory','garment_detail']
save('semantic-cards.json',cards)

CONTEXT_TEXT='''
C01|군대물·밀리터리물·전쟁물|제도 안의 생활, 군사 기술·조직, 전쟁의 수행·사회적 결과라는 서로 다른 중심축이다. 군복 하나를 모두의 충분조건으로 삼지 않는다.|S29,S30
C02|전기물 戰記物·傳記物|전쟁 경과 서사와 인물 생애 서사는 다른 뜻이다. 연대기·작품 맥락을 이름만으로 확정하지 않는다.|S29
C03|병영 코미디·캐치-22|관료제의 모순·인과·반복이 문맥이다. 우스운 표정 하나로 규칙의 순환을 증명하지 않는다.|S29,S30
C04|군사 SF·군사 판타지·대체역사|기술·마법·역사 분기가 세계 설정이다. 미래 군복·함선·장식은 가능한 외형이며 군국주의 지지나 역사 분기를 증명하지 않는다.|S30
C05|밀리터리 모에·병기 의인화|귀여운 군사 캐릭터와 병기의 인격화는 다른 설계 방식이다. 성적 표현·실제 무기 운용·인물의 나이를 자동 부여하지 않는다.|S30
C06|군종·병과·계급·보직|육해공의 조직, 전문 분야, 서열, 맡은 직무를 독립 값으로 둔다. 계급장이 함장 보직이나 지휘권을 증명하지 않는다.|S02,S04
C07|장교·부사관·병·준사관|국가별 신분 체계가 다르다. 영어 enlisted를 한국의 병만으로 제한하거나 warrant officer를 모든 국가의 준위와 완전히 등치하지 않는다.|S02,S04
C08|분대·소대·중대·임무부대|군·시대·병과에 따라 편제와 규모가 달라진다. 임무부대는 고정 수량이 아니며 한 사진의 인원수로 단위를 확정하지 않는다.|S04
C09|정규군·비정규군·민병대·PMC·용병|법·조직·고용·행위의 서로 다른 축이다. 혼합 복장·외국인 외모·무표장으로 법적 용병을 정의하지 않는다.|S20,S28
C10|SOF·Special Forces|포괄적 특수작전 조직과 미 육군의 고유 조직명은 다르다. 검은 군복·해골 패치가 소속이나 자격을 증명하지 않는다.|S35
C11|신병·베테랑·선임·후임·말년|입대·근무 순서·남은 기간·경험은 시간 정보다. 얼굴 나이·흉터·머리 길이를 대리 정답으로 쓰지 않는다.|S03,S23
C12|군기·똥군기·고문관·폐급|규율·부당한 위계에 대한 비판·비하 표현을 나눈다. 비하어를 실제 장애·질환·능력의 시각 분류로 만들지 않는다.|S03
C13|전우애·결속·BL·GL·로맨스|공동 임무·조직 소속감·연애 관계는 다르다. 같은 성별의 포옹이나 부축을 연애·성적 관계의 자동 증거로 만들지 않는다.|S26
C14|입영·자대배치·전역·제대·현역·예비역·보충역|이동 사건·복무 종료·제도상 신분을 나눈다. 전역을 모든 의무 종료나 민간복 착용과 등치하지 않는다.|S03
C15|유격훈련·게릴라전|한국 군대의 통상 훈련 명칭과 전쟁 방식은 다르다. 장애물·훈련복만으로 실제 비정규전을 부여하지 않는다.|S03,S16
C16|전투식량·MRE·짬밥|야외용 식량의 넓은 범주, 특정 식량 체계 이름, 식사·경력을 비유하는 속어를 나눈다. 포장 모양과 경험을 합치지 않는다.|S03
C17|전략·작전·전술·전구·전역|목표·연결 활동·개별 운용·공간·연속 경과는 다른 수준이다. 지도와 전투복이 그 수준을 정하지 않는다. 전역 campaign과 복무 전역도 나눈다.|S16
C18|합동·연합·제병협동|군종·국가·병과의 협력 축이 다르다. 다양한 패치·차량이 사진에 같이 있다는 것만으로 실제 협력 체계를 증명하지 않는다.|S04,S16
C19|전장의 안개·기동전·소모전·피로스의 승리|정보 부족·작전 접근·손실 누적·결과 판단은 문맥·시간에 걸친 주장이다. 연기·안개·폐허·지친 표정에 자동 등치하지 않는다.|S16,S29
C20|ISR·C2·C4ISR·EW|정보 흐름·지휘권·체계 구성·전자기 활동은 화면 장식과 다르다. 센서·화면·안테나만 보이면 기능은 보류한다.|S16
C21|CAS·공중우세·화력지원·제압사격|임무·표적·아군 관계·효과는 외형 이상이다. 낮게 나는 기체·섬광·연기만으로 임무 성공이나 행위 억제를 증명하지 않는다.|S16
C22|MEDEVAC·CASEVAC|플랫폼 실루엣이 아닌 전용·지정 의료 능력과 지원 체계에 관한 구분이다. 지상 이송도 가능하며 의무후송은 헬기 이름이 아니다.|S17
C23|브리핑·디브리핑·AAR|임무 전 설명·사후 보고·개선을 위한 검토는 비슷한 지도 장면으로 나타날 수 있으나 시간·목적이 다르다.|S16
C24|콜사인·Roger·Wilco·Over·Out|식별명·수신·이행 의사·응답 기대·교신 종료의 차이를 남긴다. 무전기 든 정지사진은 소리·발화 의미를 증명하지 않는다. 세부 절차어의 현행 원문 확인은 보류다.|S16
C25|소총·돌격소총·카빈·SMG·기관총·DMR·저격소총|범주는 외형뿐 아니라 탄약·작동·역할·역사에 걸친다. 길이·조준경 하나로 분류하지 않는다. 각 특정 모델 도판이 필요하다.|S12
C26|전차·자주포·APC·IFV·MRAP|차체·포탑·궤도·승하차부·하부 형상을 볼 수 있지만 역할·내부·방호가 유형을 가르는 경우가 있다. 실루엣만의 보편 판별기를 만들지 않는다.|S36,S38
C27|UAV·UAS·드론·자율성|기체와 관련 운용 체계, 원격조종과 자율성은 독립이다. 기체를 보았다고 통제 링크·무장·공격 의도를 발명하지 않는다.|S18
C28|로켓·미사일·레이더·소나|추진·유도·탐지 원리와 임무가 형상과 다른 차원이다. 모든 로켓 무유도·모든 화면 실제 탐지로 단정하지 않는다. 구체 분류 출처 보강이 필요하다.|S16
C29|ACU·OCP·디지털·카키·OD|군복 체계·특정 무늬·무늬 형식·색 이름을 나눈다. 정확한 색좌표·위장 성능·국가를 이름만으로 고정하지 않는다.|S01
C30|바디아머·캐리어·리그·소프트아머·하드아머|휴대 구조와 숨은 방호재를 나눈다. 캐리어 안의 판은 열려 보이는 실현으로만 시각 확인하고 성능은 별도 문맥으로 둔다.|S09
C31|MOLLE·PALS·레이저 컷|체계와 부착 격자·제조 방식을 나눈다. 한 가로 줄에서 전체 체계·파우치의 실제 결합을 추정하지 않는다.|S10,S11
C32|NVG·열영상·융합 장치|광증폭·열영상·융합 기술을 단순히 녹색/흑백으로 나누지 않는다. 장치·보는 사람·표시 화면·실제 풍경을 구분한다.|S19
C33|경례·받들어총·어깨총|나라·시대·무기·행사별 제식이 다르다. 일반 자세와 실제 공식 동작을 나누고 확인한 변형만 별도 대안으로 등록한다.|S13
C34|계급장·부대표장·훈장·약장·자격장|서열·소속·수훈·약식 표시·자격은 다른 정보다. 비슷한 별·날개·장식끈으로 계급·자격을 일률적으로 정하지 않는다.|S01,S05
C35|핸드헬드·그레인·낮은 채도·기록성|촬영 방식·영상 표면·역사적 진실은 다르다. 한 프레임의 블러와 저채도가 실제 종군 기록·연대를 증명하지 않는다.|S29
C36|무전 잡음·포성·먹먹함·정적|청각과 시간에 관한 의미는 시각 대리표현만으로 성립하지 않는다. 자막·만화 효과는 별도 매체 경계를 가진 표현이다.|S29
C37|KIA·WIA·MIA·POW|행정상 사상·실종 분류와 법적 구금 지위다. 누운 몸·붕대·빈 침상·수갑은 가능한 단서일 뿐 해당 지위 전체의 증거가 아니다.|S20,S21
C38|Friendly fire·Fragging|아군 피해와 의도적 내부 공격은 주체 관계·고의·사건 원인이 다르다. 같은 군복 두 사람이 보이는 장면에 원인과 고의를 자동 부여하지 않는다.|S20
C39|고어·신체 훼손·전투 손상|피·내부 조직·신체 손상을 직접 보이는 표현 양식, 실제 신체의 손상, 옷·기계의 손상을 구분한다. 붉은 얼룩·찢긴 옷·의수만으로 그 전체를 대체하거나 요구 의미를 지우지 않는다.|S20
C40|헤이징·괴롭힘·고문·포로 학대|서열 명분·반복 관계·심각한 고통의 행위·구금 상태의 침해는 다른 사건 범주다. 피해자·가해자·행위·상황은 문맥과 실제 접점으로 분리한다.|S20
C41|약탈·민간인 학살·전쟁범죄·인도에 반한 죄·집단살해|재산 침탈·살해 사건과 국제범죄의 요건을 나눈다. 집단·고의·규모·분쟁 연계·맥락을 폐허 사진 하나에서 판정하지 않는다.|S20,S21
C42|소년병·아동 동원|전투 외 역할도 포함한다. 아동의 신체 외형은 연령과 강제동원 이력을 증명하지 않으며 성인 패션의 후보와 합치지 않는다.|S22
C43|비인간화·War porn|표현 방식·비평적 판단이다. 무기·폭발·고어가 있다는 한 사실만으로 작가 의도나 작품 전체의 정치적 성격을 확정하지 않는다.|S29
C44|Shell shock·Combat fatigue·PTSD|역사적 표현·급성 스트레스·임상 진단이 서로 다르다. 천 야드 응시·흉터·군복은 진단 표지가 아니다.|S23
C45|도덕적 손상·생존자 죄책감·귀환 소외|개인 가치·상실·사회 복귀의 문맥이다. 고개 숙임·빈자리·의족을 각 개념의 고정 외형으로 만들지 않는다.|S24
C46|군복 페티시·권위의 에로티시즘·밀리터리 시크|성적 의미 부여·비평 관점·패션 차용은 다르다. 제복·광택·부츠·명령 자세 자체가 특정 성적 의도·행동·동의를 증명하지 않는다.|S06
C47|핀업·노즈아트·택티컬 메이드·비키니 아머|성인 매력 이미지·기체 그림·허구 결합 의상·판타지 방호 디자인을 나눈다. 노즈아트는 실물 인물도 필수 성적 이미지도 아니며 실용 방호와 다르다.|S06,S31,S34
C48|샤워·탈의·젖은 옷|사건·착의 상태·표면 상태는 다르다. 젖음을 투명화·노출·성적 접근에 자동 연결하지 않으며 특정 대안의 내의를 모든 요청에 강제하지 않는다.|S06
C49|Fraternization·상관부하 로맨스|제도상 부적절한 관계와 서사상 연애는 별개다. 규정은 시점·군에 따라 다르며 동성/이성 관계·성적 여부를 단순 금지로 통일하지 않는다.|S26
C50|기지촌·전시 성매매·성적 강압·CRSV·군사 성노예제|공간·경제·상업적 성관계와 강압·폭력·강제 착취 체계를 나눈다. 동의된 성인 코스튬 후보에 이 문맥을 기본 부착하지 않는다.|S27
C51|MST|군 복무 중 특정 성폭행·성희롱 경험을 가리키는 VA 용어다. PTSD·현재 증상·외형·성별과 동의어가 아니다.|S25
C52|Nazisploitation|역사적 나치 이미지의 착취영화·문화 비평 범주 포인터를 보존한다. 출판사 본문 접근이 막혀 세부 도상·성적 장면 처방은 이번에 검증하지 않았다.|S33
'''
contexts=[]
for line in CONTEXT_TEXT.strip().splitlines():
    cid,terms,boundary,sids=line.split('|')
    contexts.append(dict(id=cid,terms=terms,boundary_ko=boundary,source_ids=sids.split(','),
                         positive_visual_eligible=False,runtime_importable=False,native_approval=False,
                         evidence_status='bounded_research_context_not_runtime_definition'))
save('context-distinctions.json',contexts)
context_lines=['# 문맥·유사 개념 구분 52개','',
    '외형으로 증명할 수 없는 부분과 비평·법·진단·시간의 범위를 보존한다. 폭력·성적 주제도 누락하지 않았다. 일부 개념은 직접 보이는 표현 양식을 포함하지만 특정 부분 시각 대안이 그 전체 의미를 대체하지 않는다. 아래 설명은 범위 설계이며 모두가 독립적인 공식 정의 검증을 마친 항목은 아니다.','']
for c in contexts:
    context_lines += [f"## {c['id']} · {c['terms']}",'',c['boundary_ko'],'','출처: '+', '.join(c['source_ids']),'']
(ROOT/'CONTEXT-DISTINCTIONS.md').write_text('\n'.join(context_lines)+'\n')

TABLE_NAMES=['1. 장르','2. 인물·서사','3-1. 조직·신분','3-2. 한국 계급','3-3. 부대 단위','4. 병과·직무','5. 병영생활','6-1. 전쟁 개념','6-2. 지원·무전','7. 장비 분류','8-1. 기능복','8-2. 역사·실루엣','9. 군모·표장','10. 군장','11-1. 색·위장·표면','11-2. 머리·신체','12. 포즈','13-1. 공간','13-2. 시청각','14. 폭력·지위','14. 심리','15-1. 성인 외형','15-2. 관계·성폭력','16. 조합']

# A route identifies a usable component option, never an equivalence or trigger.
# Context rows may still link illustrative component cards. Unreviewed concrete
# weapon types and legal/clinical labels remain explicit rather than disappearing.
ROW_ROUTES = {
 0:'V01 V13 V76 V71 V79 V53 V01 V09 V02 V38 V70 V70 V74 V73 V61 V60 V05 V59 V72 V69 V76 V78 V79 V95 V96 V95 V42 V69 V96 V96',
 1:'V02 V47 V49 V66 V59 V06 V66 V67 V64 V71 V66 V76 V10 V70 V78 V69 V07 V63 V05 V27',
 2:'- - V27 V59 V70 V59 V70 V14 V13 V13 V13 V13 V06',
 3:'V27 V27 V27 V27 V27 V27',
 4:'V52 V52 V52 V52 V52 V52 V52 V52 V52 V52',
 5:'V53 V05 V60 V60 V59 V06 V58 V70 V05 V06 V77 V94 V76 V78 V57 V56 V54 - V38 V61 V73 V74 V07',
 6:'V02 V02 V01 V01 V10 V01 V02 V10 V03 V63 V08 V11 V55 V08 V09 V69 V09 V04 V04 V19 V50 - V13',
 7:'V70 V59 V53 V71 V70 V70 V70 V70 V60 V60 V71 V71 V76 V55 V71 V17 V61 V74 V72 V64',
 8:'V70 V70 V70 V41 V59 V53 V61 V61 V05 V76 V67 V67 V59 V59 V10 V58 V58 V58 V58 V58',
 9:'V54 V54 V53 V53 V54 V54 V54 V36 - - - - - V99 V98 V98 V100 V41 V41 - V61 V101 V75 V74 V73 V70 V73 -',
10:'V13 V14 V14 V14 V15 V16 V17 V18 V19 V11 V12 V97',
11:'V14 V13 V85 V12 V23 V20 V21 - V22 - V13 V14 V24 V08',
12:'V26 V25 V25 V25 V25 - - V39 V27 V27 V27 V27 V28 V28 V27 V15 V15 V29',
13:'V30 V30 V30 - V31 V34 V33 V32 V33 V36 V35 V34 V08 V37 V43 V44 V38 V39,V40 V41 V42',
14:'V13 V21 V08 V46 V46 V45 V46 V46 V13 - V47 V47',
15:'V48 V48 V48 V48 V81 V81 V81 - V94 V93',
16:'V50 V51 V49 - - V52 V53 V54 V55 V56 V57 V58 V59 V60 V61 V62 V63 V08 V64 V65 V66 V67 V68 V69',
17:'V79 V01 V71 V72 V05 V70 V75 V74 V73 V77 V76 V78',
18:'V82 V82 V64 V79 V64 V60 V71 V01 V80 V72 V47 - - -',
19:'V78 V94 V07 V102 V94 - V104 V103 V64 V64 V72 V102 V05 V78 V76 V76 V78 - V76 V60',
20:'V82 V64 V82 V68 V68 V69',
21:'V85 V91 V85 V85 V83 V85 V86 V85 V89 V87 V90 V88 V90 - V96 V91 - V92',
22:'V69 V69 V07 V69 V69 - - - - - -',
23:'V01 V71 V38 V60 V73 V69 V95 V85 V42'
}

TABLE_SOURCES = {0:'S29,S30',1:'S29,S23',2:'S02,S04,S28',3:'S02',4:'S04',5:'S04,S16,S35',6:'S03,S15',7:'S16,S20',8:'S16,S17',9:'S12,S18,S36,S37,S38',10:'S01,S09,S40',11:'S06,S07,S08',12:'S01,S05,S39',13:'S09,S10,S11,S19',14:'S01,S32',15:'S01,S23',16:'S13,S17',17:'S14,S15,S20',18:'S23,S29',19:'S20,S21,S22',20:'S23,S24',21:'S06,S31',22:'S25,S26,S27',23:'S29,S30'}

TABLE_LIMITS = {
0:'장르·비평 명칭이다. 연결된 시각 대안은 가능한 한 요소일 뿐 필요충분 정의나 요청 없는 전투·로맨스 추가 규칙이 아니다.',
1:'성격·전우 관계·동기·경험·시간 경과는 문맥이다. 장면의 물리적 접점과 별도로 보존한다.',
2:'군종·병과·계급·보직·고용형태·법적 신분은 독립 속성이다. 외모·장구·표장의 간단한 모양으로 확정하지 않는다.',
3:'한국 계급 명칭은 S02로 확인했다. 정확한 계급장·복제 위치·국가 간 등가관계는 별도 도판이 필요하다.',
4:'단위 명칭에서 인원·장비·지휘관 계급을 보편적으로 고정하지 않는다. V52는 정렬의 부분 예시다.',
5:'직무는 상황 문맥이다. 장비를 가진 인물이라고 그 직무·숙련·국가·자격을 증명하지 않는다.',
6:'한국 생활·속어의 시대·부대 차이를 남긴다. 병역 신분 출처가 점호·휴가·생활관의 실제 운영 전체를 입증하지 않는다.',
7:'전략·작전·전술·교리·역사적 경과는 정지영상의 배치와 다르다. 전투 수행법이 아닌 시각 구분 범위다.',
8:'정보 체계·교신·항공지원·후송의 기능은 장치 실루엣이나 화면 아이콘으로 증명되지 않는다.',
9:'유형의 이름·기능과 실제 특정 모델의 외형 식별을 분리한다. 연결은 일반 소총·차량·화면 등 부분 대안이며 유형 동의어가 아니다.',
10:'군복의 용도·소재·국가·연식을 분리한다. 단순 재단으로 공식 제식·보호 성능·성적 성격을 확정하지 않는다.',
11:'역사 의복은 시대·군대·개별 표본을 고정한 도판 검토가 필요하다. 장면 초안은 고증 확인을 대신하지 않는다.',
12:'표장 의미와 부착물 형태를 분리한다. 모자 종류별 도판·국가별 복제 확인이 필요한 항목을 보류한다.',
13:'착용자·의복·끈·수납물·부착면·센서·화면을 분리한다. 숨은 내부·방호 성능·작동을 외형에서 추정하지 않는다.',
14:'색·무늬·군복 체계·표면 상태는 독립이다. 표본·조명 없는 색 이름으로 정확한 색좌표나 위장 성능을 정하지 않는다.',
15:'외형과 신체 차이를 경력·질환·도덕·성별에 연결하지 않는다. 헤어 이름의 정확한 재단은 추가 표본이 필요하다.',
16:'동작의 소유자·관절·접점·지지면과 가시성을 검토한다. 국가별 제식 세부와 전술·치료 수행법을 일반 시각 대안에 섞지 않는다.',
17:'공간의 벽·바닥·출입·인물 관계를 다룬다. 특정 기지·함정·기관·방호 성능·감금 원인은 별도 문맥이다.',
18:'촬영·표정·소리·진단을 구분한다. 정지사진에 실제 시간·음향·정신 상태를 부여하지 않는다.',
19:'사건·피해·행위·표현 양식·행정 지위·국제법적 요건을 분리한다. 구체적인 폭력 표현은 요청의 범위와 별도 생성 정책을 따른다.',
20:'역사 표현·임상 진단·도덕적 손상·감정 서사를 동일한 표정 후보에 병합하지 않는다.',
21:'성인 패션·허구 디자인·그림 속 인물·실제 군복을 분리한다. 명칭만으로 특정 노출·동의·실제 기능을 더하지 않는다.',
22:'성인 관계의 동의·권력·제도와 폭력·착취 경험을 분리한다. BL·GL·전우애를 외형·강압의 동의어로 만들지 않는다.',
23:'원문 저자의 창작 조합 예시다. 결합 전제와 구성 요소 전체를 선택적으로 검토하며 장르 정의·기본 처방으로 승격하지 않는다.'}

tables=json.loads((ROOT/'conversation-tables.json').read_text())
atlas=[]
global_i=0
for table in tables:
    ti=table['table']; rows=table['rows'][1:]; routes=ROW_ROUTES[ti].split()
    assert len(routes)==len(rows),(ti,len(routes),len(rows))
    for ri,(row,route) in enumerate(zip(rows,routes),1):
        global_i+=1
        context=ti in [0,1,2,3,4,5,6,7,8,19,20,22,23]
        held=route=='-'
        mode='context_only' if context else ('defer_specific_visual' if held else 'component_option')
        if ti==18 and ri in [12,13,14]:
            mode='context_only'
            context=True
            held=False
        sids=TABLE_SOURCES[ti].split(',')
        atlas.append(dict(id=f'K{global_i:03}',table_index=ti,row_index=ri,section=TABLE_NAMES[ti],
            term=row[0],source_cells=row,conversation_definition_ko=row[1],
            mode=mode,component_card_ids=[] if route=='-' else route.split(','),
            component_route_is_equivalence=False,source_ids=sids,
            source_support_scope='Section-level contextual support only. Not independent verification of every definition or visual component.',
            integration_decision='context' if context else ('defer' if held else 'compare_reuse_or_author_bounded_option'),
            claim_limit_ko=TABLE_LIMITS[ti],native_approval=False,runtime_importable=False))
assert global_i==393
TABLE_CONTEXTS={0:['C01','C02','C03','C04','C05'],1:['C03','C11','C13','C19'],2:['C06','C09'],3:['C07'],4:['C08'],5:['C06','C10','C22','C25'],6:['C11','C12','C14','C15','C16'],7:['C17','C18','C19'],8:['C20','C21','C22','C23','C24'],9:['C25','C26','C27','C28'],10:['C29','C30'],11:['C29','C34'],12:['C34'],13:['C30','C31','C32'],14:['C29'],15:['C11','C44'],16:['C33','C22','C13'],17:['C20','C26'],18:['C35','C36','C44'],19:['C37','C38','C39','C40','C41','C42','C43'],20:['C44','C45'],21:['C46','C47','C48'],22:['C49','C50','C51','C52'],23:['C01','C04','C47']}
GAP_NOTES={
 'K174':'총검과 특정 총의 결합부·도검 단독 표본을 분리해 같은 무기와의 실제 부착 경로를 확인한다.',
 'K175':'손으로 던지는 종류와 발사기용 유탄의 형상·실제 표본을 분리한다. 공통 구형 소품으로 일반화하지 않는다.',
 'K176':'특정 박격포의 포신·지지·바닥 구조를 도판으로 검토한다. 구경·운용 동작을 임의로 추가하지 않는다.',
 'K177':'특정 곡사포의 정적인 포신·포가·차륜 또는 차체를 검토한다. 사격 성능·운용 절차는 시각 후보에 넣지 않는다.',
 'K178':'견인식·자주식의 운송 구조와 실제 포 표본을 각각 검토한다. V99 실루엣을 전차/자주포 공통 정답으로 쓰지 않는다.',
 'K185':'추진·유도 개념과 실제 형상을 구분할 개별 표본이 필요하다. 로켓=무유도·미사일=특정 날개 형상으로 고정하지 않는다.',
 'K193':'탄약 개체·탄창 용기·장전 보조 클립을 별개 물체 표본으로 확인한다. 부품과 전체를 한 물건으로 합치지 않는다.',
 'K213':'돌먼의 몸에 맞는 재단·가슴 장식·별도 덧재킷과의 경계를 특정 소장품 도판에서 확인한다.',
 'K215':'브리치즈의 허벅지·무릎·종아리와 부츠 경계를 시기별 표본에서 확인한다. 모든 승마 바지를 같은 형태로 고정하지 않는다.',
 'K225':'S39의 서지 정보 외에 샤코 전체 모자의 높이·챙·전면판·장식을 실제 도판에서 확인한다.',
 'K226':'버스비 전체 표본과 베어스킨·샤코의 차이를 실제 도판에서 확인한다. 털 표면만으로 분류하지 않는다.',
 'K241':'유연한 방호재가 별도 표본·열린 수납부·단면에서 어떻게 드러나는지 확인한다. 착용 외형만으로 내부를 확정하지 않는다.',
 'K267':'S32의 대즐 도판을 실제로 보고 선박 곡면·패턴·표시 면을 검토한다. 도판 표색과 실제 역사 색·위장 효율을 나눈다.',
 'K277':'치유된 피부 흔적의 범위·위치·소유자를 비진단적 표현으로 검토한다. 전쟁·폭력·경력·성격의 증거로 삼지 않는다.',
 'K283':'지정 국가·시대·무기의 어깨총 도판에서 같은 총과 손·어깨의 접점을 확인한다.',
 'K284':'지정 국가·시대·무기의 받들어총 도판에서 총 방향·두 손·몸의 상대 위치를 확인한다.',
 'K369':'허구 디자인의 가려진 부위·장식과 장착을 명시한 선택 대안을 작성한다. 실제 방호 성능·추가 성적 행위를 부여하지 않는다.',
 'K372':'샤워·목욕·탈의는 서로 다른 사건이다. 시점·착의·행동 범위를 정한 개별 실현이 필요하며 임의의 노출·가림 상태를 기본값으로 만들지 않는다.'}
gaps=[]
for row in atlas:
    row['section_context_ids']=TABLE_CONTEXTS[row['table_index']]
    row['component_route_scope']='Possible component or illustrative scene only; never the whole compound term, a synonym, or a mandatory trigger.'
    if row['mode']=='defer_specific_visual':
        assert row['id'] in GAP_NOTES,row['id']
        row['next_research_ko']=GAP_NOTES[row['id']]
        gaps.append({'keyword_id':row['id'],'term':row['term'],'next_research_ko':GAP_NOTES[row['id']],
                     'defer_reason':'specific_scope_or_specimen_review_pending','term_is_preserved':True})
save('remaining-research.json',gaps)
save('keyword-atlas.json',atlas)

def md_escape(value):
    return str(value).replace('|','\\|').replace('\n',' ')

atlas_lines=['# 원문 전체 키워드 대응표','',
    '원문 24개 표의 393행을 순서대로 보존했다. 표 안의 복합어는 행을 먼저 유지하며, 한 행의 부분 시각 카드가 그 복합어 전체의 동의어가 되는 것은 아니다. `context_only`는 삭제가 아니라 비가시 의미를 보존하는 경로다. `defer_specific_visual`은 특정 표본·접점 검토가 남은 항목이다. 모든 출처는 절 수준의 근거이며 원문 정의 전체를 재검증했다고 뜻하지 않는다.','']
for ti in range(24):
    atlas_lines += [f'## {TABLE_NAMES[ti]}','','| ID | 원문 용어 | 경로 | 부분 시각 카드 |','|---|---|---|---|']
    for row in atlas:
        if row['table_index']==ti:
            atlas_lines.append('| '+' | '.join(map(md_escape,[row['id'],row['term'],row['mode'],', '.join(row['component_card_ids']) or '보류']))+' |')
    atlas_lines += ['',TABLE_LIMITS[ti],'']
(ROOT/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas_lines)+'\n')

lines=[f'# 시각 의미와 후보 초안 {len(cards)}개','',
    '각 항목은 연구용 완결 시각 대안이다. 실제 후보 CID/RID, effects, intrinsic conditions, native proof는 아직 만들지 않았다. `suggested_slots`는 구현 때 현행 catalog와 대조할 제안이며 승인된 binding이 아니다. 각 출처는 한정된 용어 구분을 뒷받침하고 아래 구도·행동은 독립적으로 작성했다. 실제 도판·신체 모델·원문 전체 조건 검토는 다음 단계다.','']
for c in cards:
    lines += [f"## {c['id']} · {c['title_ko']}",'',c['positive_ko'],'',c['positive_en'],'',
        '- 관계: '+'; '.join(f"{r['from']} → {r['relation']} → {r['to']}" for r in c['relations']),
        '- 화면 확인: '+ '; '.join(c['observable_gates']),
        '- 구분·한계: '+c['confusion_boundary_ko'],
        '- 제안 role: '+', '.join(c['suggested_slots'])+' / 출처: '+', '.join(c['source_ids']),'']
(ROOT/'VISUAL-CARDS.md').write_text('\n'.join(lines)+'\n')

source_lines=['# 출처와 확인 범위','',
    '조회일: 2026-10-24 KST. `body_reviewed`도 문서 전체·모든 그림을 완독했다는 뜻은 아니며 관련 본문을 검토했다는 뜻이다. 검색 발췌만 확인한 출처, 역사 설명, 본문 403, 도판 미확인은 따로 표시했다. 현재 세부 역사 군복과 한국군 복제 도판·장비별 외형 식별은 미완료다.','']
for s in sources:
    source_lines += [f"## {s['id']} · {s['title']}",'',f"[{s['publisher']}]({s['url']}) · {s['access']}",'',s['bounded_support_ko'],'',s['limitations_ko'],'']
(ROOT/'SOURCES.md').write_text('\n'.join(source_lines)+'\n')

counts=collections.Counter(x['mode'] for x in atlas)
save('research-counts.json',{'conversation_table_count':len(tables),'conversation_row_count':len(atlas),
    'keyword_route_modes':dict(counts),'visual_card_count':len(cards),'context_distinction_count':len(contexts),'source_count':len(sources),
    'source_access_modes':dict(collections.Counter(x['access'] for x in sources)),
    'image_calls':0,'runtime_source_writes':0,'registration':'not_started',
    'retrieval_evaluation':'not_run','pixel_evaluation':'not_run','user_acceptance':'not_requested'})
print(json.dumps(json.loads((ROOT/'research-counts.json').read_text()),ensure_ascii=False,indent=2))

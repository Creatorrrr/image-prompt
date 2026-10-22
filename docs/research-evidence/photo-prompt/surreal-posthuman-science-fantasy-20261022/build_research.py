"""Offline research authoring only. Does not import or register operating candidates."""
from pathlib import Path
import csv, hashlib, json, re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def dump(name, value):
    (HERE/name).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

SOURCE_ROWS = '''S01|Centre Pompidou: Surrealist art|https://mediation.centrepompidou.fr/education/ressources/ENS-surrealistart-EN/ENS-surrealistart-EN.htm|museum_educational_body|Origins and artist entries; follow-up glossary request timed out|꿈·욕망·자동기술·이질적 병치의 역사적 연결|개별 무늬가 실제 자동기술로 제작됐다는 증거는 아님
S02|The Met: Surrealism|https://www.metmuseum.org/essays/surrealism|museum_essay_body|Essay body, especially technique and desire paragraphs 125-143|데칼코마니·그라타주, 욕망·폭력·정밀한 환영적 공간|현대 후보의 구체적 접점이나 작가의 의도를 대신 증명하지 않음
S03|MoMA: Surrealist Strategies|https://www.moma.org/collection/terms/surrealism/surrealist-strategies|search_index_and_navigation|Search excerpt; current opened body was navigation and article index|자동기술·발견 오브제라는 조사 경로|현재 열린 페이지 본문에서 역사 해설 전문은 확인하지 못함
S04|Mori: The Uncanny Valley, authorized translation|https://spectrum.ieee.org/the-uncanny-valley|primary_essay_body|Authorized translation, affinity hypothesis and movement discussion|인간 유사성과 친화감의 비선형 관계를 제안한 가설|특정 형태를 모든 관객이 무서워한다는 보편 법칙은 아님
S05|Braidotti: Posthuman Critical Theory|https://rosibraidotti.com/wp-content/uploads/2019/08/369.-Posthuman-Critical-Theory-1.pdf|primary_search_abstract_only|Author-hosted PDF opened but no extractable lines; indexed abstract read|포스트휴먼과 탈인간중심주의의 만남을 다룬다는 원전 위치|13쪽 전문을 읽지 않았으며 개별 철학 용어의 완전 검증 아님
S06|Haraway: Staying with the Trouble|https://www.dukeupress.edu/staying-with-the-trouble|publisher_description_toc|Publisher description and chapter list, especially ch.3-5|공동 생성·공생발생·친족 만들기를 연결하는 연구 틀|책 전체나 개별 사례를 직접 읽었다는 뜻 아님
S07|Clark and Chalmers: The Extended Mind|https://www.consc.net/papers/extended.html|primary_paper_body|Sections 1-3 and coupling examples|도구와 환경이 인지 체계에 참여하는 주장|외부 케이블이나 저장소가 의식의 이동·생존을 입증하지 않음
S08|SFE: Science Fantasy|https://sf-encyclopedia.com/entry/science_fantasy|editor_authored_reference_body|Definition and ingredient discussion, lines 23-30|경계가 느슨하며 마법·신·특정 소재가 필수는 아님|색·장치·복장 묶음을 장르의 필요충분조건으로 만들지 않음
S09|SFE: Technofantasy|https://sf-encyclopedia.com/entry/technofantasy|editor_authored_reference_body|Definition and examples, lines 23-29|기술 외피를 가진 본질적으로 판타지적인 서사|과학적 정당화가 강한 합리화된 판타지와 구분
S10|SFE: Science and Sorcery|https://sf-encyclopedia.com/entry/science_and_sorcery|editor_authored_reference_body|Definition and world-crossing distinctions, lines 23-27|과학과 판타지 설정의 병치·교차|포털 하나나 마법 단독이 이 범주를 증명하지 않음
S11|SFE: Psionics|https://sf-encyclopedia.com/entry/psionics|editor_authored_reference_body|Definition and historical pseudoscience caveat, lines 23-26|정신 능력과 전자 장치의 SF 어휘|실증된 공학 기술로 등록하지 않음
S12|SFE: Upload|https://sf-encyclopedia.com/entry/upload|search_index_only|Indexed definition read; direct open returned HTTP 429|인격의 소프트웨어 복사·전이라는 SF 용법|업로딩 성공·동일 인격의 생존을 증명하지 않음
S13|Partridge et al.: Extra-uterine premature lamb support|https://www.nature.com/articles/ncomms15112|primary_paper_body|2017 abstract and introduction, lines 59-88|양 태아의 제한된 체외 생리 지원 실험|완전한 인간 체외 임신의 구현·최신 임상 현황을 주장하지 않음
S14|National Academies: Human Genome Editing glossary|https://www.ncbi.nlm.nih.gov/books/NBK447273/|search_index_only|Indexed chimera definition; direct open showed browser check|상이한 유전적 개체에서 온 세포로 구성된 키메라 정의|동물 머리의 외형 혼합을 유전적 키메라로 판정하지 않음
S15|Bordenstein and Theis: Holobionts and Hologenomes|https://pmc.ncbi.nlm.nih.gov/articles/PMC4540581/|search_index_only|Indexed paper passages; direct body blocked by browser check|숙주와 연관 미생물을 함께 보는 틀|공동 의식·완벽한 협력·단일 선택 단위의 보편 합의로 확대하지 않음
S16|Harrington: Women, Monstrosity and Horror Film|https://www.routledge.com/Women-Monstrosity-and-Horror-Film-Gynaehorror-1st-Edition/Harrington/p/book/9781315546568|publisher_search_description|Publisher indexed description; direct open inaccessible|기네호러가 성·생식과 생애의 넓은 범위를 다루는 비평어임|임신 장면만으로 축약하거나 책 전체를 읽었다고 하지 않음
S17|Creed: The Monstrous-Feminine|https://www.routledge.com/The-Monstrous-Feminine-Film-Feminism-Psychoanalysis/Creed/p/book/9781003006756|publisher_search_description|Publisher indexed description; direct open inaccessible|여성성의 괴물화와 비체를 분석하는 비평 틀|여성·생식·젠더 비순응 자체를 괴물 속성으로 만들지 않음
S18|Laboria Cuboniks: Xenofeminism|https://laboriacuboniks.net/manifesto/xenofeminism-a-politics-for-alienation/|primary_manifesto_body|Sections 0x00-0x04, 0x0E-0x10|자연·기술·젠더·권력의 관계에 대한 선언|기술이 자동으로 해방적이라는 규칙이나 외형 분류가 아님
S19|John Pier: Metalepsis|https://www-archiv.fdm.uni-hamburg.de/lhn/node/51.html|scholarly_reference_body|Definition and explication, lines 43-62|서사 층위의 경계 침범과 단순 재현·중첩의 구별|작은 모형이 있는 것만으로 서사 경계 침범이 확정되지 않음
S20|Arcosanti: What is Arcology|https://arcosanti.org/vision/what-is-arcology/|originating_institution_body|Definition and design principles|건축·생태·농업·공용 공간의 통합|거대한 건물이나 식물 덩굴만으로 아콜로지라 판정하지 않음
S21|National Gallery: The Ambassadors|https://www.nationalgallery.org.uk/paintings/hans-holbein-the-younger-the-ambassadors|museum_collection_body|About the work, lines 99-106|관찰 각도에 따라 해골로 읽히는 왜상의 사례|단일 정면 이미지로 각도 변화에 따른 검증을 완료할 수 없음
S22|Ebb Software interview: Scorn|https://www.unrealengine.com/developer-interviews/creating-the-unreal-dystopian-surrealism-and-biomechanical-horrors-of-scorn|primary_creator_interview|Design, interface, augmentation and sound, lines 34-58|세계의 기능 원리를 신체·무기·퍼즐 인터페이스에 일관되게 적용|작품의 특정 디자인을 복사하거나 모든 바이오메커니컬을 Scorn이라 부르지 않음
S23|Tippett Studio: MAD GOD|https://www.tippett.com/portfolio/mad-god/|creator_studio_description|Studio project body, lines 26-35|실물 세트·피규어·환경을 제작한 어두운 초현실 세계|영화 전체나 개별 장면의 의도를 직접 검증한 것은 아님
S24|Kodansha: BLAME!|https://kodansha.us/series/blame/|publisher_synopsis|Series synopsis, lines 28-33|인간의 규모를 넘어선 도시와 유전자·네트워크 접근의 서사|건물 사진만으로 특정 유전자·역사·접근 권한을 입증하지 않음
S25|Macmillan: Borne|https://us.macmillan.com/books/9780374714925/borne/|publisher_synopsis_and_excerpt|Opening excerpt and Book Details synopsis|생명공학 폐허에서 돌봄·인격·위험이 얽힘|초안의 생물 형태는 독립 저술이며 정본 Borne의 복원이 아님
S26|Penguin Random House: Perdido Street Station|https://www.penguinrandomhouse.com/books/114262/perdido-street-station-by-china-mieville/|publisher_synopsis|Book Description and About sections|과학·마술·도시의 혼성 세계를 조사하는 작품 근거|책 전체의 사회 제도를 이번에 모두 검증하지 않음
S27|GKIDS: Angel's Egg|https://gkids.com/films/angels-egg/|distributor_metadata_only|Current opened body was home-video/store details|작품·배급 페이지의 존재 확인|상징·신학 해석·장면의 근거로 이 페이지를 사용하지 않음
S28|NHGRI: Cloning Fact Sheet|https://www.genome.gov/about-genomics/fact-sheets/Cloning-Fact-Sheet|originating_institution_body|Definitions and cloning types, lines 8-35|유전적 복사와 여러 클로닝 절차의 구별|닮은 외형·쌍둥이·기억 동일성을 서로 대체하지 않음
S29|Mbembe: Necropolitics|https://dukeupress.edu/necropolitics|publisher_description_toc|Publisher description and book contents|생존·죽음에 대한 정치적 권력의 분석을 위한 원전 경로|배급대·폐허·구속구의 외형만으로 죽음정치를 확정하지 않음
S30|Freud Museum: The Uncanny|https://www.freud.org.uk/2019/09/18/the-uncanny/|museum_essay_body|Researcher essay body, lines 11-48; comments excluded|친숙함의 낯설어짐·분신·반복의 역사적 맥락|관객 반응은 경험에 좌우되며 Freud 원전 전문을 읽은 것은 아님
S31|Jeff VanderMeer: Working Definition of New Weird|https://www.jeffvandermeer.com/blog/2007/09/27/working-definition-of-new-weird|primary_author_definition|Author's working definition, lines 5-7|도시·이차세계·현실 사회의 복잡성과 SF·판타지·공포의 혼합|장르의 유일한 정의나 촉수·의상·건물의 표준 도감이 아님
S32|Matthew Brehmer: Visualizing the Weird and the Eerie|https://arxiv.org/html/2309.01763v1|primary_design_essay_secondary_fisher_interpretation|Essay abstract and sections 1-3|불확실한 존재·부재·행위 주체를 시각화에 응용하는 저자의 제안|사진 관객에 대한 실험 결과나 Fisher 원전 직접 확인은 아님
S33|HR Giger Museum: HR Giger biography|https://www.hrgigermuseum.com/hr-giger|artist_museum_body|Selected design chronology read; focused follow-up fetch timed out|작가의 영화·가구·공간 디자인 활동을 조사하는 경로|생체역학 정의·실제 공생·모든 유기적 기계의 표준 형태를 증명하지 않음'''

sources=[]
for line in SOURCE_ROWS.splitlines():
    sid,title,url,kind,scope,support,limit=line.split('|')
    sources.append(dict(source_id=sid,title=title,url=url,evidence_kind=kind,read_scope=scope,
                        supports_ko=support,limit_ko=limit,reviewed_date_kst='2026-10-22',
                        geometry_support='No candidate geometry is quoted from this source.'))
dump('sources.json',{'schema':'research-sources/v1','sources':sources})

# Fields: ID | title | KO positive | EN positive | owners key:description;... | edges from>predicate>to;... | slots | confusion | nonvisual claim limit.
CARD_ROWS = '''A01|도자기로 굳은 커튼|창틀의 커튼은 접힌 도자기 판으로 이루어지고, 상단 고리가 봉을 감싼다.|A window curtain consists of folded porcelain plates, with its upper rings encircling a rod.|curtain:folded porcelain curtain;ring:upper curtain rings;rod:curtain rod|ring>part_of>curtain;ring>encircles>rod|surface_material,object_structure|천을 닮은 인쇄 무늬|재질 전이의 외형만 보이며 실제 변환 과정은 확인되지 않는다.
A02|가지로 갈라지는 열쇠|금속 열쇠의 날은 하나의 줄기에서 잎 달린 두 가지로 이어진다.|The blade of a metal key continues from one stem into two leafy branches.|key:metal key;stem:key blade stem;branches:two leafy branches|stem>part_of>key;branches>continues_from>stem|object_structure,material_form|열쇠 옆에 놓인 잎|식물 성장·연금술 작동은 입증되지 않는다.
A03|사슬이 된 물줄기|주전자 주둥이와 그 아래 컵 사이의 물줄기는 중간에서 투명한 사슬 고리로 이어진다.|A stream between a teapot spout and the cup below continues into transparent chain links at its midpoint.|spout:teapot spout;stream:stream;links:transparent chain links;cup:cup below|stream>starts_at>spout;stream>continues_into>links;links>ends_above>cup|material_form,object_structure|물이 반짝여 고리처럼 보임|중력·유체의 실제 규칙이나 시간적 변신은 입증되지 않는다.
A04|접힌 바다의 문턱|열린 문 안의 파도 표면이 문턱에서 수직으로 접혀 방 바닥까지 이어진다.|A wave surface inside an open doorway folds vertically at the threshold and continues onto the room floor.|door:open doorway;wave:wave surface;threshold:door threshold;floor:room floor|wave>visible_inside>door;wave>folds_at>threshold;wave>continues_onto>floor|environment_detail,material_form|바다 사진이 붙은 문|공간 연결의 환영이며 포켓 우주 존재는 확정되지 않는다.
A05|붙박이 손잡이의 작은 지형|서랍의 금속 손잡이 안쪽에 계단식 지형이 연속해서 솟아 있다.|A stepped terrain rises continuously inside the metal handle of a drawer.|drawer:drawer;handle:metal drawer handle;terrain:stepped miniature terrain|handle>attached_to>drawer;terrain>rises_inside>handle|object_structure,scale_relation|서랍 앞에 놓인 별도 모형|내부 주민이나 독립 우주의 존재를 뜻하지 않는다.
A06|종이 무늬와 그림자 생물|탁자의 찢긴 종이 가장자리와 그 그림자가 합쳐져 한 마리 새의 윤곽을 이룬다.|A torn paper edge on a table and its cast shadow together form the outline of one bird.|paper:torn paper;shadow:paper cast shadow;bird:combined bird outline;table:table|paper>rests_on>table;shadow>cast_by>paper;paper>contributes_to>bird;shadow>contributes_to>bird|surface_pattern,reflection_logic|옆에 실제 새를 추가함|새의 생명이나 관객의 무의식 상태를 입증하지 않는다.
B01|얼굴로 읽히는 기둥열|정면의 기둥 두 개와 가운데 아치의 빈 공간이 하나의 얼굴 윤곽도 이루며, 개별 기둥의 밑동은 보인다.|Two frontal columns and the void of the central arch also form one face outline, while the separate column bases remain visible.|columns:two columns;arch:central arch void;face:combined face outline;bases:column bases|bases>part_of>columns;columns>contributes_to>face;arch>contributes_to>face|object_structure,spatial_depth|건축 앞에 거대한 얼굴을 따로 둠|하나의 형상에 두 해석이 있어야 하며 도시의 의식은 판단하지 않는다.
B02|손과 반사의 다른 자세|거울 앞 인물의 오른손은 펴져 있지만 같은 손의 거울상은 주먹을 쥔 모습이며 거울 테두리가 모두 보인다.|A person's right hand is open before a mirror, but its reflection forms a fist, and the entire mirror frame is visible.|hand:person right hand;reflection:reflection of that right hand;mirror:framed mirror|reflection>reflection_of>hand;reflection>visible_in>mirror|reflection_logic,hand_pose|서로 다른 두 사람의 손|한 장면의 불일치이며 시간 지연·빙의 원인은 판단하지 않는다.
B03|사람과 새 그림자|바닥에 선 인물의 두 발에서 시작한 하나의 그림자가 날개를 편 새 윤곽으로 이어진다.|One shadow starts at both feet of a standing person and extends into the outline of a spread-winged bird.|person:standing person;feet:both feet;shadow:single bird-shaped shadow;floor:floor|feet>part_of>person;feet>touches>floor;shadow>starts_at>feet|reflection_logic,contact_point|옆 새가 드리운 별도 그림자|영혼·도플갱어·주술 효과를 증명하지 않는다.
B04|비스듬히 맞물린 왜상|비스듬한 시점에서 서로 떨어진 세 돌판의 길쭉한 칠 자국이 한 눈 모양으로 정렬된다.|From an oblique viewpoint, elongated painted marks on three separate stone slabs align into one eye shape.|slabs:three separate stone slabs;marks:elongated painted marks;eye:aligned eye shape|marks>painted_on>slabs;marks>align_as>eye|surface_pattern,viewer_position|정면의 보통 눈 그림|한 시점의 정렬만 검사할 수 있다. 각도 의존성은 별도 시점 비교가 필요하다.
B05|손바닥과 거대 문고리|성인 손바닥이 거대한 문고리의 일부에 닿고, 손가락과 문고리의 접점이 함께 보인다.|An adult palm touches a small part of an enormous door handle, with fingers and the handle contact visible together.|hand:adult palm and fingers;handle:enormous door handle|hand>touches>handle|scale_relation,contact_point|원근으로 크게 보이는 전경 소품|실제 거리·동일 평면 근거 없이 물리적 치수 비율은 확정하지 않는다.
B06|바닥과 어긋난 투명 판|투명 판을 통과해 보이는 타일 줄 하나가 판 가장자리에서 옆으로 어긋나며, 나머지 바닥 줄은 곧게 이어진다.|One tile line viewed through a transparent panel shifts sideways at the panel edge, while the surrounding floor lines continue straight.|panel:transparent panel;line:viewed tile line;edge:panel edge;floor:surrounding tile floor|edge>part_of>panel;line>part_of>floor;line>visible_through>panel;line>offset_at>edge|reflection_logic,spatial_depth|보통 굴절이나 깨진 타일|관측 가능한 어긋남이며 비유클리드 기하학의 수학적 증명은 아니다.
C01|팔과 기록함의 연결|성인 인물의 오른팔 바깥 소켓에서 나온 케이블이 열린 기록함의 단자까지 끊김 없이 이어진다.|A cable runs continuously from a socket on the outside of an adult person's right forearm to a terminal in an open archive case.|person:adult person;arm:right forearm;socket:outer forearm socket;cable:cable;terminal:archive case terminal|arm>part_of>person;socket>attached_to>arm;cable>starts_at>socket;cable>ends_at>terminal|anatomical_connection,contact_point|옷 위에 얹은 연결되지 않은 전선|데이터·기억·영혼 전송과 자발성은 외형으로 판정하지 않는다.
C02|금속과 피부의 연속 이음|같은 허구적 인물의 손목에서 피부 가장자리와 금속 외피가 하나의 둘레 이음선으로 만난다.|At one wrist of the same fictional person, the skin edge and metal shell meet along one continuous encircling seam.|person:fictional person;wrist:one wrist;skin:skin edge;shell:metal shell;seam:encircling seam|wrist>part_of>person;skin>meets_at>seam;shell>meets_at>seam;seam>encircles>wrist|anatomical_connection,surface_material|위에 걸친 팔찌|인체 진단·증강 성공·기계 인격을 입증하지 않는다.
C03|등판과 천장 릴|입은 외투의 등판 구멍을 통과한 관이 그 착용자의 등 소켓과 천장 릴 사이를 잇고, 구멍 둘레와 양끝이 보인다.|A tube passes through a hole in a worn coat's back panel and connects its wearer's back socket to a ceiling reel, with the hole rim and both ends visible.|wearer:coat wearer;coat:worn coat;hole:back panel hole;socket:wearer back socket;tube:tube;reel:ceiling reel|coat>worn_by>wearer;socket>part_of>wearer;hole>part_of>coat;tube>passes_through>hole;tube>connects>socket;tube>connects>reel|anatomical_connection,object_structure|관이 외투 표면에서 끝남|착용자와 의복의 소유를 구분하며 생명 유지·구속 여부를 단정하지 않는다.
C04|인공 손과 잠금부|성인 인물의 인공 손끝이 열린 기계 잠금부의 두 홈에 각각 닿아 있다.|An adult person's artificial fingertips touch the two grooves of an open mechanical lock.|person:adult person;hand:artificial hand;tips:artificial fingertips;grooves:two lock grooves|hand>part_of>person;tips>part_of>hand;tips>touches>grooves|contact_point,relational_action|손이 잠금부 앞에서 떠 있음|기계 제어 성공·권한·사이오닉스를 확인하지 않는다.
C05|뼈 형태 지지대와 외부 주머니|허구적 인물의 몸통 바깥에 뼈 형태 지지대가 있고, 투명한 주머니가 그 지지대의 두 고리에 매달려 있다.|A bone-shaped support sits outside a fictional person's torso, and a transparent pouch hangs from two rings on that support.|person:fictional person;torso:person torso;support:external bone-shaped support;rings:two support rings;pouch:transparent pouch|torso>part_of>person;support>outside>torso;rings>part_of>support;pouch>hangs_from>rings|object_structure,anatomical_connection|장기를 노출한 몸으로 오인|주머니를 실제 장기·생식기·임신으로 판정하지 않는다.
C06|분리된 인공 팔의 받침|몸에 연결되지 않은 인공 팔이 두 받침 위에 놓이고, 열린 팔꿈치 결합부와 받침 접점이 보인다.|An artificial arm detached from any body rests on two supports, with its open elbow coupling and support contacts visible.|arm:detached artificial arm;coupling:open elbow coupling;supports:two supports|coupling>part_of>arm;arm>rests_on>supports|object_structure,prop_placement|인간의 절단된 팔과 혼동|인공 팔 분리는 인간 신체 절단의 의미를 충족하지 않는다.
D01|머리 장치와 서랍 배열|인물의 머리 장치에서 나온 선 하나가 벽 서랍 배열의 한 열린 칸까지 이어진다.|One lead from a person's head device runs to one open compartment in an array of wall drawers.|person:person;device:head device;lead:single lead;compartment:one open wall drawer|device>worn_by>person;lead>starts_at>device;lead>ends_at>compartment|anatomical_connection,environment_detail|머리 뒤 배경 선의 우연한 겹침|확장된 마음의 창작적 비유이며 기억 저장은 별도 설정이다.
D02|한 선을 공유하는 두 단말|서로 떨어진 두 단말의 포트가 하나의 Y자 케이블 양 갈래에 각각 연결된다.|The ports of two separate terminals connect to the two branches of one Y-shaped cable.|terminals:two separate terminals;ports:terminal ports;cable:single Y-shaped cable|ports>part_of>terminals;cable>connects>ports|object_structure,contact_point|두 선이 화면 밖에서 끊김|정보 공유·군체 의식·동일 인격을 입증하지 않는다.
D03|복수 몸 앞의 같은 초상|외형이 다른 두 인공 몸 앞에 같은 얼굴 초상 카드가 하나씩 놓인다.|One identical face portrait card stands before each of two artificial bodies with different exteriors.|bodies:two artificial bodies;cards:two identical face portrait cards|cards>placed_before>bodies|body_form,prop_placement|한 몸을 두 번 찍은 합성|인격 분기·같은 사람·복제 유전자를 입증하지 않는다.
D04|필기장과 조작 손|성인 인물은 펼친 필기장의 그림을 한 손가락으로 짚고 다른 손으로 옆 장치의 같은 모양 다이얼을 잡는다.|An adult points to a diagram in an open notebook with one finger and grips a matching-shaped dial on a nearby device with the other hand.|person:adult person;finger:pointing finger;notebook:open notebook diagram;hand:other hand;dial:matching-shaped device dial|finger>part_of>person;hand>part_of>person;finger>points_at>notebook;hand>grips>dial|relational_action,contact_point|필기장이 소품으로만 놓임|실제 인지의 구성 요소인지 단순 참고인지 픽셀로 확정하지 않는다.
D05|서로 다른 몸의 교환 받침|서로 다른 두 인공 외피가 각기 열린 받침 위에 있고 두 받침 사이에 빈 운반 트레이가 놓인다.|Two different artificial shells sit on separate open cradles, with an empty carrying tray between them.|shells:two artificial shells;cradles:two open cradles;tray:empty carrying tray|shells>rests_on>cradles;tray>between>cradles|body_form,prop_placement|기억이 몸을 옮기는 장면으로 단정|실제로 교환이 일어났는지·자아가 이동했는지 판정하지 않는다.
D06|연결된 합창 좌석|원형으로 배치된 빈 좌석 각각의 등판에서 선이 나와 중앙 금속 원판에 닿는다.|A lead from the back of each empty seat in a circle reaches one central metal disk.|seats:circle of empty seats;backs:seat backs;leads:seat leads;disk:central metal disk|backs>part_of>seats;leads>starts_at>backs;leads>ends_at>disk|environment_detail,object_structure|그냥 원형 좌석|좌석 수는 구현 시 선언해야 하며 집단 의식·음악·의례는 추가 맥락이다.
E01|기둥과 이어진 뿌리 지지|벽의 굵은 뿌리 두 갈래가 하나의 기둥 하부와 바닥 틈에 각각 이어진다.|Two thick wall roots continue to the base of one column and into a floor crack.|wall:wall;roots:two thick roots;column:column base;crack:floor crack|roots>emerges_from>wall;roots>continues_to>column;roots>enters>crack|environment_detail,anatomical_connection|기둥 표면의 뿌리 무늬|실제 하중 지지·공생 이득·건물의 생명 여부는 판단하지 않는다.
E02|살 같은 벽 밸브|유기적 주름의 벽 한가운데 금속 밸브가 박혀 있고 주름이 밸브 테두리까지 연속된다.|A metal valve is set in a wall of organic folds that continue to the valve rim.|wall:organically folded wall;valve:metal valve;folds:wall folds;rim:valve rim|folds>part_of>wall;valve>embedded_in>wall;folds>continues_to>rim|environment_detail,surface_material|살색 도료를 칠한 평면 벽|바이오모픽 외형과 실제 살아 있는 건축은 구분한다.
E03|막과 덕트의 접합|반투명 주름막의 가장자리가 환기 덕트의 원형 프레임 안쪽에 고정되어 있다.|The edge of a translucent pleated membrane is fixed inside the circular frame of a ventilation duct.|membrane:translucent pleated membrane;edge:membrane edge;frame:circular duct frame;duct:ventilation duct|edge>part_of>membrane;frame>part_of>duct;edge>fixed_inside>frame|object_structure,environment_detail|덕트 앞에 떠 있는 천|호흡·섭식·포식 기능은 외형으로 확인되지 않는다.
E04|균사와 천 소매의 경계|성인이 입은 천 소매 끝에서 흰 섬유 같은 균사 덩어리가 자라난 듯 손등 위로 이어지며 경계가 보인다.|A white fibrous mycelium-like mass continues from the cuff of an adult's worn cloth sleeve onto the back of the hand, with the boundary visible.|adult:adult wearer;sleeve:worn sleeve;cuff:sleeve cuff;mass:mycelium-like fibrous mass;hand:back of hand|sleeve>worn_by>adult;cuff>part_of>sleeve;mass>continues_from>cuff;mass>extends_onto>hand;hand>part_of>adult|anatomical_connection,texture|장갑이나 레이스를 균류로 확정|미생물 종·감염·공생·유전적 결합은 확인되지 않는다.
E05|생체 벽의 수선 패치|성인 정비사의 손이 유기적 주름 벽의 패치 가장자리를 누르고 패치 둘레의 고정점이 보인다.|An adult maintainer's hand presses the edge of a patch on an organically folded wall, with its surrounding fasteners visible.|maintainer:adult maintainer;hand:maintainer hand;wall:organic folded wall;patch:wall patch;fasteners:patch fasteners|hand>part_of>maintainer;hand>presses>patch;patch>attached_to>wall;fasteners>surrounds>patch|relational_action,contact_point|건축 수선을 치료 행위로 확정|치유·고통·건물의 감각은 서사 설정이다.
E06|온실과 순환관|계단식 재배대 아래에서 나온 투명 관이 같은 온실의 높은 물통으로 이어진다.|A transparent pipe from beneath stepped growing beds runs to an elevated water tank in the same greenhouse.|beds:stepped growing beds;pipe:transparent pipe;tank:elevated water tank;greenhouse:shared greenhouse|beds>inside>greenhouse;tank>inside>greenhouse;pipe>starts_beneath>beds;pipe>ends_at>tank|environment_detail,object_structure|식물이 있는 큰 건물|자원 자립·완전 순환·아콜로지 도시 전체를 입증하지 않는다.
F01|무릎 자세와 크랭크|성인 작업자가 기계 앞 한쪽 무릎을 바닥에 대고 손으로 노출된 크랭크를 잡는다.|An adult worker kneels on one knee before a machine and grips its exposed crank.|worker:adult worker;knee:one knee;floor:floor;hand:worker hand;crank:machine crank|knee>part_of>worker;hand>part_of>worker;knee>touches>floor;hand>grips>crank|body_pose,contact_point|기도가 기계를 작동시킨다고 단정|의례·기도·기적의 인과는 추가 설정이다.
F02|봉헌물과 기계 슬롯|작은 금속 토큰이 기계 받침의 홈에 절반 끼워져 있고 성인의 두 손가락이 바깥쪽 가장자리를 잡는다.|A small metal token is half inserted into a groove in a machine pedestal, and two adult fingers grip its outer edge.|token:small metal token;groove:pedestal groove;fingers:two adult fingers;edge:outer token edge|token>inserted_into>groove;edge>part_of>token;fingers>grips>edge|contact_point,prop_placement|성물·결제·희생을 외형으로 확정|봉헌의 의미·대가·효과는 별도 맥락이다.
F03|도선과 문자판|금속 도선이 문자 모양 홈을 따라 구부러져 있고 양끝이 같은 판의 두 단자에 고정된다.|A metal wire bends along character-shaped grooves, with both ends fastened to two terminals on the same plate.|wire:metal wire;grooves:character-shaped grooves;plate:single plate;terminals:two plate terminals|grooves>part_of>plate;terminals>part_of>plate;wire>follows>grooves;wire>ends_at>terminals|surface_pattern,object_structure|발광 문자만 추가함|실제 주문·암호·문화권 문자·회로 작동은 입증하지 않는다.
F04|종과 연결된 케이블|매달린 종의 추 끝에 케이블이 연결되고 케이블 반대쪽 끝이 벽 장치에 들어간다.|A cable attaches to the tip of a hanging bell's clapper and enters a wall device at its other end.|bell:hanging bell;clapper:bell clapper;cable:cable;device:wall device|clapper>part_of>bell;cable>starts_at>clapper;cable>ends_at>device|object_structure,contact_point|케이블이 종 바깥에서 끝남|소리·정신 동조·신의 응답은 정지 이미지로 확인하지 않는다.
F05|성물함과 평형추|뚜껑 열린 작은 함이 한쪽 접시에 놓이고, 반대쪽 추와 이어진 줄이 도르래를 지난다.|A small open box rests on one pan, while a cord passes over a pulley to a weight on the opposite side.|box:small open box;pan:one pan;cord:cord;pulley:pulley;weight:opposite weight|box>rests_on>pan;cord>connects>pan;cord>passes_over>pulley;cord>connects>weight|object_structure,prop_placement|신성한 무게를 측정한다고 단정|성물·영혼·가치·기적의 실재는 별도 의미다.
F06|액체와 감긴 코일|유리 용기 바깥에 구리 코일이 감기고, 안쪽 액면과 바깥 코일이 동시에 보인다.|A copper coil wraps around a glass vessel, with both the inner liquid surface and outer coil visible.|vessel:glass vessel;coil:copper coil;liquid:inner liquid surface|coil>wraps_around>vessel;liquid>inside>vessel|surface_material,object_structure|진짜 연금술 변환이나 생명 제조로 단정|재료 배치만 입증되며 실험 절차·화학·연금술의 성공은 아니다.
G01|광물 속의 작은 도시|반투명 광물 덩어리 안에 작은 건물 윤곽과 가로가 보이고 광물의 외곽도 함께 보인다.|Small building outlines and streets are visible inside a translucent mineral mass, whose outer contour is also visible.|mineral:translucent mineral mass;buildings:small building outlines;streets:small streets|buildings>visible_inside>mineral;streets>visible_inside>mineral|scale_relation,environment_detail|광물 표면에 비친 도시|내부 생명·별도 우주·차원은 외형만으로 확정하지 않는다.
G02|기계 외피 속 거주 발판|거대한 열린 기계 외피의 안쪽 벽에 작은 거주 발판들이 붙어 있고 발판 난간이 보인다.|Small habitation platforms attach to the inner wall of a vast open machine casing, with their railings visible.|casing:vast open machine casing;wall:inner casing wall;platforms:small habitation platforms;railings:platform railings|wall>part_of>casing;platforms>attached_to>wall;railings>part_of>platforms|environment_detail,scale_relation|배경에 놓인 별개 도시|문명의 연대·기계신·피난 강요를 입증하지 않는다.
G03|작업자와 기둥의 크기|성인 작업자가 거대한 기둥 밑동 옆 같은 바닥에 서 있으며 발과 밑동 접지가 모두 보인다.|An adult worker stands beside the base of a vast column on the same floor, with the feet and column ground contact both visible.|worker:adult worker;feet:worker feet;column:vast column;base:column base;floor:shared floor|feet>part_of>worker;base>part_of>column;feet>touches>floor;base>touches>floor|scale_relation,spatial_depth|전경 원근만으로 압도를 만듦|초원미래·멸망·특정 작품의 공간을 자동 추론하지 않는다.
G04|겹겹의 제어 창|큰 제어실 창 너머에 더 작은 제어실 창이 같은 중심축으로 겹쳐 보인다.|A smaller control-room window is visible through a larger control-room window on the same central axis.|outer:large control-room window;inner:smaller control-room window|inner>visible_through>outer|spatial_depth,environment_detail|창문 반사만으로 중첩을 오인|포함 관계만 보이며 창조자·상위 시뮬레이션은 확정하지 않는다.
G05|지구 모양 구체와 뿌리|육지 무늬가 있는 구체 아래에서 굵은 뿌리 묶음이 뻗어 받침 구멍을 통과한다.|Thick roots extend beneath a land-patterned sphere and pass through a hole in its stand.|sphere:land-patterned sphere;roots:thick root bundle;stand:stand;hole:stand hole|roots>extends_from>sphere;hole>part_of>stand;roots>passes_through>hole|object_structure,anatomical_connection|실제 살아 있는 행성으로 단정|행성의 크기·생명·의식·천체 궤도는 입증하지 않는다.
G06|빛과 작은 작업대|어두운 홀의 작은 작업대 위로 거대한 원형 장치의 빛이 떨어지며 둘의 위치가 보인다.|Light from a vast circular device falls onto a small workbench in a dark hall, with both positions visible.|device:vast circular device;light:device light;bench:small workbench;hall:dark hall|light>emitted_by>device;light>falls_on>bench;bench>inside>hall|lighting,scale_relation|광륜을 신성의 증거로 판정|누미노스는 관객 경험이며 신성·숭배 여부는 별도 설정이다.
H01|방 안의 같은 방 모형|탁자 위 열린 방 모형에는 실제 방과 같은 창·탁자 배치가 보이고, 모형과 실제 창이 함께 프레임에 있다.|An open room model on a table repeats the real room's window and table arrangement, with the model and real window in the same frame.|room:real room;window:real window;table:real table;model:open room model;mini:miniature window and table|window>part_of>room;table>inside>room;model>rests_on>table;mini>inside>model|object_structure,prop_placement|임의의 미니어처|재현의 중첩은 보이지만 메타렙시스·무한 반복은 입증하지 않는다.
H02|초상과 빈 얼굴 자리|인물이 든 액자 안에는 같은 옷의 인물이 보이지만 얼굴 자리만 빈 종이로 남아 있다.|A framed portrait held by a person shows a figure in matching clothes, but the face area remains blank paper.|person:person;frame:held portrait frame;portrait:figure in matching clothes;blank:blank paper face area|frame>held_by>person;portrait>inside>frame;blank>part_of>portrait|narrative_clue,prop_placement|가려진 얼굴을 기억 삭제로 확정|기억 삭제·가족 관계·사진 변화의 시간 순서는 판단하지 않는다.
H03|서로 다른 마모의 두 장치|동일한 외형의 장치 두 개가 나란히 놓이고 한쪽 외피에만 녹과 벗겨진 도료가 있다.|Two devices with identical shapes sit side by side, with rust and peeling paint on only one shell.|devices:two identically shaped devices;shell:one device shell;rust:rust and peeling paint|shell>part_of>devices;rust>on>shell|texture,prop_placement|녹을 시간 여행의 흔적으로 확정|연대·과거와 미래의 동일 물체 여부는 서사 정보다.
H04|문 너머의 같은 창 배치|열린 문 너머 방의 창과 의자 배치가 문 앞 방의 배치와 일치하고 양쪽 방 경계가 보인다.|The window and chair arrangement beyond an open doorway matches that of the near room, with both room boundaries visible.|door:open doorway;near:near room;far:far room;layout:matching window and chair arrangements|far>visible_through>door;layout>occurs_in>near;layout>occurs_in>far|environment_detail,spatial_depth|비슷한 방을 실제 동일 방으로 확정|공간 루프·무한 복도·재귀 악몽의 반복 경험은 미확인이다.
H05|거울 둘 사이의 반복|서로 마주 보는 두 거울 사이에서 동일한 작은 등불의 상이 여러 크기로 반복되고 거울 테두리도 보인다.|Between two facing mirrors, the same small lamp repeats at several sizes, with both mirror frames visible.|mirrors:two facing mirrors;lamp:small lamp;images:repeated lamp images|images>reflection_of>lamp;images>visible_in>mirrors|reflection_logic,spatial_depth|미니 램프 여러 개를 따로 배치함|유한한 가시 반복이며 실제 무한성이나 시간 루프가 아니다.
H06|겹쳐 남은 벽 글자|벽의 벗겨진 상층 도료 아래에서 이전 글자의 일부가 보이고 새 글자는 상층에 남아 있다.|Parts of older lettering show beneath a peeled upper paint layer on a wall, while newer letters remain on the upper layer.|wall:wall;upper:peeled upper paint;old:older letter fragments;new:newer letters|upper>on>wall;old>visible_beneath>upper;new>on>upper|surface_pattern,texture|새 글자와 낡은 글자를 한 평면에 인쇄함|겹친 흔적은 보이지만 실제 연대·문자 의미·문명의 수는 입증하지 않는다.
I01|다른 조직의 허구적 접합|허구 생물의 비늘 부위와 매끈한 외피 부위가 하나의 몸통 접합에서 연속된다.|A fictional creature's scaled region and smooth shell region continue through one junction on the same torso.|creature:fictional creature;torso:single torso;scaled:scaled region;smooth:smooth shell region;junction:torso junction|torso>part_of>creature;scaled>continues_through>junction;smooth>continues_through>junction|anatomical_connection,body_form|두 생물이 겹쳐 서 있음|유전적 키메라·교잡·공생발생의 실제 기전은 판정하지 않는다.
I02|세 부품 조립 마네킹|마네킹의 머리·몸통·다리가 서로 다른 재료이며 목과 허리의 연결부가 보인다.|A mannequin has a head, torso and legs made of different materials, with neck and waist joints visible.|mannequin:mannequin;head:head;torso:torso;legs:legs;neck:neck joint;waist:waist joint|head>part_of>mannequin;torso>part_of>mannequin;legs>part_of>mannequin;neck>joins>head;neck>joins>torso;waist>joins>torso;waist>joins>legs|body_form,surface_material|단지 색이 다른 의상|엑스퀴지트 코프스 제작 절차·인간의 수는 입증하지 않는다.
I03|내벽에 붙은 녹색 막|투명한 허구 생물 외피의 안쪽 벽에 녹색 막이 붙고 바깥 외곽과 막 경계가 함께 보인다.|A green film adheres to the inner wall of a transparent fictional creature's shell, with both the outer contour and film boundary visible.|creature:fictional creature;shell:transparent shell;wall:inner shell wall;film:green inner film|shell>part_of>creature;wall>part_of>shell;film>adheres_to>wall|anatomical_connection,surface_material|빛 반사나 바깥 이끼|조류·세균의 종, 상호 이득, 홀로바이온트의 진화 단위는 입증하지 않는다.
I04|몸들과 공유 막|두 허구 생물의 외피가 가운데 한 막의 서로 반대쪽 가장자리와 각각 이어진다.|The shells of two fictional creatures each continue into opposite edges of one central membrane.|left:first fictional creature shell;right:second fictional creature shell;membrane:single central membrane;edge1:first edge;edge2:opposite edge|edge1>part_of>membrane;edge2>part_of>membrane;left>continues_into>edge1;right>continues_into>edge2|anatomical_connection,relational_action|장식 천이 두 몸 앞에 겹침|두 개체의 의식·동의·공생의 득실은 별도 설정이다.
I05|종자 모양 장치와 관|종자 모양 허구 장치의 하단 관이 흙 담긴 상자의 구멍으로 들어간다.|A lower tube on a seed-shaped fictional device enters a hole in a soil-filled box.|device:seed-shaped fictional device;tube:lower tube;box:soil-filled box;hole:box hole|tube>part_of>device;hole>part_of>box;tube>enters>hole|object_structure,environment_detail|식물 모양 기계로 생명공학을 확정|유전자 조작·생식·실제 발아는 보이지 않는다.
I06|배양 용기와 외부 순환|액체가 든 닫힌 투명 주머니의 두 관이 외부 순환 장치에 연결되고, 주머니 전체가 보인다.|Two tubes from a closed transparent fluid pouch connect to an external circulation device, with the entire pouch visible.|pouch:closed transparent fluid pouch;tubes:two pouch tubes;device:external circulation device|tubes>starts_at>pouch;tubes>ends_at>device|object_structure,contact_point|용기를 완전한 인간 인공자궁으로 확정|태아·임신 단계·인간 임상 적용·생리 기능을 외형만으로 확인하지 않는다.
J01|닫힌 이음 주변의 흉터|성인 인물 팔의 닫힌 원형 이음 둘레에 희미한 흉터 자국이 있고 외부 장치가 가장자리에 붙어 있다.|Faint scar marks surround a closed circular seam on an adult person's arm, with an external device attached at the edge.|person:adult person;arm:person arm;seam:closed circular seam;scar:surrounding scar marks;device:edge device|arm>part_of>person;seam>on>arm;scar>surrounds>seam;device>attached_to>seam|body_marking,anatomical_connection|도색 무늬를 실제 상처로 확정|통증·수술 경위·강제 개조는 별도 정보다.
J02|열린 형틀과 몸|허구 인물의 몸 주변에 열린 두 금속 형틀이 놓여 있고 몸과 형틀 사이 틈이 보인다.|Two open metal mold halves lie around a fictional person's body, with visible gaps between the body and molds.|person:fictional person;body:person body;molds:two open metal mold halves;gaps:body-mold gaps|body>part_of>person;gaps>between>body;gaps>between>molds|body_pose,object_structure|형틀만으로 구속·가해 의도를 확정|자발성·강제·탈출 가능성·피해를 외형으로 단정하지 않는다.
J03|넘친 점액과 용기|열린 용기 테두리에서 점성 물질 한 줄기가 바깥 바닥까지 이어지고 재료의 시작점이 보인다.|One strand of viscous material extends from an open vessel rim to the floor outside, with its origin visible.|vessel:open vessel;rim:vessel rim;strand:viscous strand;floor:outside floor|rim>part_of>vessel;strand>starts_at>rim;strand>ends_on>floor|material_mechanics,texture|반짝이는 표면만으로 점성을 판정|체액·혈액·부패·질병이라고 확정하지 않는다.
J04|분리된 해부 모형|비성적 해부 전시 모형의 두 분리 부품이 받침 위에 놓이고, 평평한 모형 결합면이 보인다.|Two separated parts of a nonsexual anatomical display model rest on a stand, with their flat model coupling surfaces visible.|model:nonsexual anatomical display model;parts:two separated model parts;surfaces:flat model couplings;stand:stand|parts>part_of>model;surfaces>part_of>parts;parts>rests_on>stand|object_structure,prop_placement|실제 훼손된 인체나 생체 해부로 치환|모형은 실제 인체 훼손 용어를 충족하지 않는다. 실제 묘사를 채택하려면 별도 완전 source가 필요하다.
J05|비어 있는 벗은 외피|속이 빈 허구 생물 외피가 갈라진 등 이음과 열린 바닥을 드러내고 받침에 서 있다.|A hollow fictional creature shell stands on a support, exposing a split back seam and open base.|shell:hollow fictional creature shell;seam:split back seam;base:open shell base;support:support|seam>part_of>shell;base>part_of>shell;shell>stands_on>support|body_form,object_structure|외피를 곧바로 시체로 분류|탈피·죽음·박피 행위·정체성 이탈은 별도 설정이다.
J06|천과 금속 가시의 걸림|성인 인물의 소매 천 일부가 벽 금속 가시에 걸려 당겨지고, 피부와 가시 사이에는 틈이 보인다.|Part of an adult's sleeve catches on a metal wall spike and pulls taut, with a gap visible between skin and spike.|person:adult person;sleeve:worn sleeve;spike:metal wall spike;skin:person skin;gap:skin-spike gap|sleeve>worn_by>person;sleeve>catches_on>spike;gap>between>skin;gap>between>spike|contact_point,material_mechanics|옷의 손상을 신체 손상으로 치환|부상·고어·공포 경험을 자동 추가하지 않는다.
K01|서로 다른 손의 접촉|두 성인의 손바닥이 서로 맞닿고 한쪽 금속 손가락과 다른 쪽 피부 손가락의 접점이 보인다.|Two adults' palms touch, with contact visible between one person's metal fingers and the other's skin fingers.|adult1:first adult;adult2:second adult;hand1:metal hand;hand2:skin hand|hand1>part_of>adult1;hand2>part_of>adult2;hand1>touches>hand2|contact_point,relational_action|가까운 두 손이 실제로 닿지 않음|친밀성·욕망·합의·혼인 관계는 별도 정보다.
K02|같은 외피의 접합을 살피는 두 사람|한 성인이 다른 성인이 착용한 인공 외피의 손목 이음선을 손끝으로 가리키며 두 손과 이음선이 보인다.|One adult points a fingertip at the wrist seam of an artificial shell worn by another adult, with both hands and the seam visible.|adult1:pointing adult;adult2:wearing adult;finger:first adult fingertip;shell:second adult worn shell;seam:shell wrist seam|finger>part_of>adult1;shell>worn_by>adult2;seam>part_of>shell;finger>points_at>seam|relational_action,anatomical_connection|타인의 접점을 내 몸의 접점으로 오인|동의·검사 권한·사랑을 외형에서 추론하지 않는다.
K03|장갑 표면을 누르는 손끝|한 성인의 손끝이 다른 성인이 낀 긴 장갑의 광택 표면을 눌러 작은 주름을 만든다.|One adult's fingertip presses the glossy surface of a long glove worn by another adult, forming a small crease.|adult1:first adult;adult2:second adult;finger:first adult fingertip;glove:second adult long glove;crease:small glove crease|finger>part_of>adult1;glove>worn_by>adult2;finger>presses>glove;crease>on>glove|texture,contact_point|광택 장갑만으로 페티시·성행위를 판정|성적 의미·합의 여부·성별은 명시 문맥을 보존한다.
K04|외형이 다른 두 교체 외피|성인 인물이 외형이 다른 두 인공 외피 사이에 서 있고 각 외피의 열린 장착 테두리가 보인다.|An adult stands between two artificial shells with different exteriors, with each open mounting rim visible.|adult:adult person;shells:two artificial shells;rims:open shell mounting rims|adult>between>shells;rims>part_of>shells|body_form,prop_placement|외형 대안을 성정체성·성징 변경으로 확정|형태 선택권·생물학적 성·임신·정체성은 외형과 구별한다.
K05|함께 잡은 인터페이스 원판|두 성인이 하나의 금속 인터페이스 원판 양쪽 가장자리를 각각 잡고 각 손의 접점이 보인다.|Two adults each grip opposite edges of one metal interface disk, with both hand contacts visible.|adult1:first adult;adult2:second adult;hand1:first adult hand;hand2:second adult hand;disk:single metal interface disk|hand1>part_of>adult1;hand2>part_of>adult2;hand1>grips>disk;hand2>grips>disk|contact_point,relational_action|두 원판을 겹쳐 한 개로 보이게 함|분산된 동의·기억 융합·관계 성립은 보이는 접촉과 별개다.
K06|비인간 외피를 수선하는 손|성인이 비인간 형태 동반자의 외피 패치를 손으로 받치고, 패치와 외피 경계가 함께 보인다.|An adult supports a patch on a nonhuman-shaped companion's shell with a hand, with the patch-shell boundary visible.|adult:adult person;hand:adult hand;companion:nonhuman-shaped companion;shell:companion shell;patch:shell patch|hand>part_of>adult;shell>part_of>companion;patch>attached_to>shell;hand>supports>patch|relational_action,contact_point|비인간 외형을 성적 대상·동물 종으로 단정|돌봄의 행동 제안이며 친족·연애·인격성의 증명이 아니다.
L01|배급 토큰과 단자|줄 서 있는 성인의 손에서 금속 토큰이 단자 앞 접시로 건네지고 손·토큰·접시가 함께 보인다.|A metal token is passed from a queued adult's hand toward a dish before a terminal, with hand, token and dish visible together.|adult:queued adult;hand:adult hand;token:metal token;dish:terminal dish|hand>part_of>adult;hand>holds>token;token>above>dish|relational_action,prop_placement|단자와 줄만으로 생명정치를 확정|무엇을 배급하는지·차별·통제·합법성은 서사 정보다.
L02|인공 부품의 상품 진열|여러 인공 손 부품이 진열대의 분리 칸에 놓이고 각 부품의 커넥터가 보인다.|Several artificial hand components sit in separate display compartments, with their connectors visible.|hands:artificial hand components;compartments:display compartments;connectors:hand connectors|hands>inside>compartments;connectors>part_of>hands|object_structure,prop_placement|인공 부품을 실제 거래되는 인간 장기로 판정|판매·임대·기업 소유·신체 착취는 별도 맥락이다.
L03|기계 몸의 평범한 노동|성인 인공 신체 작업자의 손이 재봉틀 옆 천을 잡고 천은 바늘판 위에 놓인다.|An adult artificial-bodied worker holds cloth beside a sewing machine, with the cloth resting on its needle plate.|worker:adult artificial-bodied worker;hand:worker hand;cloth:cloth;plate:machine needle plate|hand>part_of>worker;hand>holds>cloth;cloth>rests_on>plate|relational_action,contact_point|기계 몸이면 곧바로 노예 노동으로 분류|지위·강요·감정·계약 관계는 별도 정보다.
L04|손바닥과 출입판|성인 인물 손바닥이 출입판의 오목한 자리에 맞닿고 문과 판이 같은 벽에 보인다.|An adult palm touches a recess in an access panel, with the panel and door visible on the same wall.|adult:adult person;palm:adult palm;panel:access panel;recess:panel recess;door:door;wall:shared wall|palm>part_of>adult;recess>part_of>panel;palm>touches>recess;panel>on>wall;door>on>wall|contact_point,environment_detail|접촉만으로 유전자 인증 성공을 판정|유전자·권리·접근 허용·거부 여부를 입증하지 않는다.
L05|다른 사람에게 건네는 기록함|한 성인이 작은 기록함 바닥을 받치고 다른 성인이 그 손잡이를 잡으며 두 손 접점이 보인다.|One adult supports the base of a small archive case while another grips its handle, with both hand contacts visible.|adult1:first adult;adult2:second adult;hand1:first hand;hand2:second hand;case:small archive case;handle:case handle|hand1>part_of>adult1;hand2>part_of>adult2;handle>part_of>case;hand1>supports>case;hand2>grips>handle|relational_action,contact_point|같은 함을 잡는 것을 기억 상속으로 확정|내용물·기억 소유·가족 관계·거래 성립은 서사 정보다.
L06|남은 이음과 일상 수선|성인 인물이 인공 무릎 외피의 나사를 작은 공구로 조이며 무릎·공구 끝·나사 접점이 보인다.|An adult tightens a screw on an artificial knee shell with a small tool, with knee, tool tip and screw contact visible.|adult:adult person;knee:artificial knee shell;screw:knee shell screw;tool:small tool;tip:tool tip|knee>part_of>adult;screw>part_of>knee;tip>part_of>tool;tip>touches>screw|contact_point,relational_action|정비를 수술·자해로 바꿈|치료·수리 성공·자율성·경제적 강제는 별도 정보다.'''

FAMILIES={
'A':('사물의 전이와 이질적 병치',['S01','S02']),
'B':('이중 이미지와 지각 불일치',['S01','S04','S21','S30']),
'C':('신체와 장치의 소유·접합',['S22','S33']),
'D':('인지·기억을 위한 외부 구조',['S07','S12']),
'E':('유기적 건축과 돌봄',['S06','S20','S22']),
'F':('의례 형식과 기계 인터페이스',['S08','S09','S10','S11']),
'G':('인간 너머의 규모와 포함 세계',['S08','S24']),
'H':('재귀·기록·시간의 흔적',['S19','S02']),
'I':('복합 생물과 조립 구조',['S13','S14','S15','S28']),
'J':('신체의 경계와 물질 흔적',['S02','S22']),
'K':('친밀성·외형 선택·돌봄',['S06','S16','S17','S18']),
'L':('몸과 기억을 둘러싼 일상 제도',['S18','S25','S26','S29','S31'])}

catalog=json.loads((ASSETS/'photo_candidate_slot_catalog.json').read_text())['slot_catalog']
cards=[]
for line in CARD_ROWS.splitlines():
    cid,title,ko,en,owners,edges,slots,confusion,limit=line.split('|')
    owners=dict(x.split(':',1) for x in owners.split(';'))
    relations=[dict(zip(['from','predicate','to'],x.split('>'))) for x in edges.split(';')]
    slots=slots.split(',')
    cards.append(dict(card_id=cid,family=FAMILIES[cid[0]][0],title_ko=title,
        proposal_ko=ko,proposal_en=en,owners=owners,directed_relations=relations,
        proposed_slots=slots,role_descriptors={s:{k:catalog[s][k] for k in ['semantic_role','dimensions','property_prefixes']} for s in slots},
        source_ids=FAMILIES[cid[0]][1],source_support='Conceptual background or analogy only; all concrete geometry independently authored.',
        observability='visible_arrangement_only',nearest_confusion_ko=confusion,claim_limit_ko=limit,
        priority='P0' if cid[1:] in ['01','02'] else 'P1',
        adoption_mode='optional_complete_realization',activation='Explicit compatible selection after independent core freeze; no genre-triggered obligation.',
        component_gates=[dict(gate_id=f'{cid}-O-{owner}',owner=owner,requirement_en=description,partial_is_fail=True,status='NOT_RUN') for owner,description in owners.items()],
        whole_positive_meaning_gate=dict(proposal_en=en,proposal_ko=ko,all_properties_required=True,status='NOT_RUN',limit='Relations alone do not cover every material, count, pose or qualifier. All explicit positive clauses remain required.'),
        render_gates=[dict(gate_id=f'{cid}-R{i+1}',relation=r,both_endpoints_required=True,partial_is_fail=True,status='NOT_RUN') for i,r in enumerate(relations)],
        native_approval=False,pixel_status='NOT_RUN',language_review='authored bilingual draft; independent bilingual review pending'))
dump('semantic-cards.json',{'schema':'surreal-posthuman-research-cards/v1','cards':cards})
dump('candidate-drafts.json',{'schema':'research-only-candidate-proposals/v1',
    'not_loader_input':True,'not_registered':True,'proposals':[
    {**c,'candidate_id':None,'realization_id':None,'source_module':None,
     'decision':'review_reuse_refine_new_context_or_defer','conditions_effects_native_proof':'UNAUTHORED_PENDING_FULL_SOURCE_REVIEW'} for c in cards]})

GROUP_ROUTES={
'중심축':('contextual_genre',['A','B','C','D','E','F','G','H','I','J','K','L'],['S01','S05','S08']),
'꿈과 연상':('historical_method_or_experience',['A','B','H'],['S01','S02']),
'형태와 오브제':('art_method_or_motif',['A','B','I'],['S01','S02']),
'초현실 공포':('critical_experience_or_motif',['B','G','H','J'],['S04','S22']),
'인간 중심주의':('philosophical_context',['D','E','K','L'],['S05','S06']),
'몸과 인지':('philosophical_or_cognitive_context',['C','D','E'],['S07','S05']),
'정신과 인격':('fiction_science_and_identity',['C','D','L'],['S07','S12','S28']),
'종과 생식':('biology_or_speculative_motif',['E','I','K'],['S13','S14','S15','S28','S06']),
'기술과 마법':('historical_critical_or_setting',['F','G'],['S08','S09','S10','S11']),
'신과 우주':('religious_or_speculative_context',['F','G'],['S08']),
'공간과 감각':('spatial_material_or_crossmodal',['A','B','E','G','H'],['S20','S21','S22']),
'신체 공포와 폭력':('depiction_action_and_genre_distinct',['C','I','J'],['S02','S22']),
'욕망과 매혹':('desire_and_critical_context',['K','J'],['S02','S16','S17']),
'성 생식 동의':('sex_reproduction_and_autonomy_context',['K','I','L'],['S13','S16','S17','S18']),
'서사 기법':('genre_or_narrative_operation',['H','L','A'],['S19','S08','S26']),
'권력과 일상':('political_and_social_context',['L','D','K'],['S18','S29'])}

BOUNDARIES={
'Surrealism':'역사적 운동·창작 방법·보이는 효과를 구분. 기괴한 사물 하나는 운동 소속의 증거가 아니다.',
'Dream Logic':'감정과 연상의 인과는 서사 관계. 공간 변형의 한 순간을 보여도 꿈의 논리 전체를 입증하지 않는다.',
'Psychic Automatism':'결과 무늬와 제작 방법은 다르다. 질감만으로 자동기술 과정을 역추정하지 않는다.',
'Frottage':'표면 위 종이를 문지르는 절차와 결과 텍스처를 분리. 사진 매체를 종이 그림으로 자동 교체하지 않는다.',
'Decalcomania':'눌렀다 떼는 전사 기법. 반드시 좌우대칭이라는 제한을 추가하지 않는다.',
'Assemblage / Agencement':'미술 조립과 철학적 배치를 별도 sense로 유지하며 전자의 오브제 조건을 후자에 강제하지 않는다.',
'The Uncanny':'친숙함과 낯섦의 관계를 설계하되 관객의 불안 경험을 픽셀 fact로 선언하지 않는다.',
'Uncanny Valley':'모리의 가설을 보편 감정 규칙으로 등록하지 않는다. 움직임 효과는 단일 정지 화면에서 검증할 수 없다.',
'The Weird':'피셔의 특정 비평 틀을 사용하려면 원전별 sense와 근거를 보강. 현재 이번 소스 목록에는 그 책 전문 검증이 없다.',
'The Eerie':'행위 주체의 부재·존재에 대한 질문. 단순 빈 복도를 자동 이리로 승인하지 않는다. 피셔 원전 추가 검토 필요.',
'Body without Organs':'장기를 제거한 신체라는 문자적 source로 바꾸지 않는다. 철학 원전 재검토가 필요한 문맥 항목이다.',
'Extended Mind':'외부 도구의 지속적 결합에 대한 논제. 저장 장치·케이블이 실제 의식 전송을 보증하지 않는다.',
'Distributed Cognition':'여러 도구와 사람의 인지 처리 분석이며 단일 군체 의식과 동일하지 않다.',
'Mind Uploading':'복사·실행·원래 인격의 생존은 별도 주장. 연결 장치만으로 어느 것도 증명하지 않는다.',
'Cloning':'유전적 복사와 외형 유사·심리 연속성을 구분한다.',
'Chimera':'유전적 세포 계통의 혼합과 미술적 합성 생물의 외형을 다른 sense로 보존한다.',
'Hybrid':'교잡 계통과 범용 혼성 미학을 분리. 키메라·이식·공생과 같은 뜻으로 합치지 않는다.',
'Holobiont':'숙주와 미생물의 연합을 공동 의식이나 무조건적 상호 이득으로 바꾸지 않는다.',
'Ectogenesis / Ectogestation':'2017 양 태아 지원 실험은 완전한 인간 체외 임신의 구현 증거가 아니다. 이번 연구는 최신 임상 상태 조사도 아니다.',
'Parthenogenesis':'인간에게 적용한 모티프는 가상 설정. 외형으로 생식 기전을 판정하지 않는다.',
'Science Fantasy':'특정 신·주문·룬·금속·색의 묶음을 필수 profile로 만들지 않는다.',
'Technofantasy':'기술의 외형과 과학적 설명을 구분한다. 합리화된 판타지와 동의어가 아니다.',
'Psionics':'SF 어휘이며 입증된 정신 공학 분야라는 사실로 등록하지 않는다.',
'Homunculus':'연금술 인공 인간과 신경과학 신체 지도는 다른 sense다.',
'Golem':'유대 전승의 구체적 맥락을 일반 로봇·석상과 합치지 않는다. 원전별 보강 전에는 설정 문맥 검토 대상이다.',
'Noosphere':'정신권 사상과 실제 공동 정신 공간은 구분한다.',
'Numinous':'신성 앞의 매혹·압도는 경험·해석. 큰 광원과 신성의 실재는 다르다.',
'Non-Euclidean Space':'실제 비유클리드 기하학은 모순된 공간과 다르다. 불가능한 건축의 느슨한 장르적 사용을 분리한다.',
'Arcology':'건축·생태·자원·생활의 통합. 규모가 크거나 녹색 식물이 있다는 것만으로 성립하지 않는다.',
'Biomechanical':'미학적 유기체-기계 접합과 실제 생체역학 연구를 구분한다.',
'Biomorphic':'유기체를 닮은 형태이며 실제 생명·생체 조직이라는 뜻은 아니다.',
'Anamorphosis':'각도 의존성 확인에는 비교 시점이 필요. 단일 컷은 해당 시점의 정렬만 통과 가능하다.',
'Acousmatic Sound':'음원을 보이지 않게 들려주는 소리. 정지 사진에서 소리의 존재를 PASS 처리하지 않는다.',
'Synesthetic Imagery':'감각 간 비유를 가시 요소로 제안할 수 있지만 냄새·촉감·청각 경험 자체는 사진으로 입증하지 않는다.',
'Gore':'시각적 신체 손상·혈액의 묘사 강도와 바디 호러의 정체성·통제 상실을 별도 축으로 둔다.',
'Dismemberment':'실제 인체 분리·인공 부품·해부 모형·회화적 분절은 서로 다른 source다. 모형을 실제 사건의 대체 합격으로 쓰지 않는다.',
'Flaying':'피부 제거 모티프. 빈 외피·의상 탈착·탈피를 같은 뜻으로 승인하지 않는다.',
'Evisceration':'장기 제거 행위·결과·전시 모형을 구분하며 단순 열린 기계 함으로 충족 처리하지 않는다.',
'Vivisection':'살아 있음과 실험 행위라는 추가 맥락이 필요. 해부 도구·해부 모형만으로 확정하지 않는다.',
'Cannibalism':'인간 신체와 섭취 관계 및 동종 여부가 의미 조건. 식사·육류만으로 채택하지 않는다. 기억 계승은 창작 확장이다.',
'Autocannibalism':'섭취자와 섭취 대상의 동일 소유자 관계가 필요. 타인의 신체 섭취와 다른 모티프다.',
'Fetishism':'성적 의미·인류학적 물신·상품물신을 분리. 광택 재료·특정 부위만으로 성적 맥락을 자동 부여하지 않는다.',
'BDSM':'합의된 성인 권력 교환 맥락과 비동의적 폭력을 혼합하지 않는다. 구속구 외형은 합의 증거가 아니다.',
'Xenophilia':'낯선 것에 대한 호감은 비성적 용법도 있다. 비인간 외형만으로 성적 의미를 추가하지 않는다.',
'Androgyny':'외형 표현·생물학적 성·성정체성을 분리하며 젠더 비순응을 공포 속성으로 만들지 않는다.',
'Gynaehorror':'여성의 성·생식과 생애 전반을 다루는 비평 범주이며 임신 공포만으로 축약하지 않는다.',
'The Monstrous-Feminine':'여성이 괴물이라는 본질 규칙이 아니라 문화적 괴물화의 분석 개념이다.',
'Incest Taboo':'친족과 규범의 맥락. 비슷한 얼굴·성인 둘의 근접·기억 상속은 혈연 관계의 증거가 아니다.',
'Necrophilia':'죽은 신체를 향한 성적 욕망의 개념. 창백함·수면·인형·부활 전승을 동일 의미로 바꾸지 않는다.',
'Sexual Violence':'동의·신체 자율성 침해 맥락을 별도로 보존. 자세·복장·접촉만으로 법적·서사적 사건을 확정하지 않는다.',
'Distributed Consent':'이 대화의 설정어. 실제 법·임상 표준처럼 제시하지 않는다. 여러 몸·인격의 의사를 외형에서 추정하지 않는다.',
'Metalepsis':'서사 층위의 침범은 단순 그림 속 그림·작은 방·포털과 다르다.',
'Mise en abyme':'내부 재현과 전체의 구조적 대응을 검토. 작은 모형 존재만으로 무한 재귀·층위 침범을 확정하지 않는다.',
'Information Hazard':'정보가 위험을 만들거나 가능하게 한다는 개념과 읽으면 변신하는 초자연 설정을 구분한다.',
'Necropolitics':'죽음·생존 조건의 권력을 분석하는 개념. 폐허·검문·공장 외형만으로 제도를 확정하지 않는다.',
'Xenofeminism':'기술·자연·젠더 권력의 정치적 선언. 외형 스타일·외계 종·특정 성징의 시각 태그가 아니다.'}

DIRECT={'Surrealism':['S01','S02'],'Decalcomania':['S02'],'Uncanny Valley':['S04'],
        'Extended Mind':['S07'],'Science Fantasy':['S08'],'Technofantasy':['S09'],
        'Science and Sorcery':['S10'],'Psionics':['S11'],'Cloning':['S28'],
        'Arcology':['S20'],'Anamorphosis':['S21'],'Metalepsis':['S19'],
        'Xenofeminism':['S18'],'Gynaehorror':['S16'],'The Monstrous-Feminine':['S17'],
        'Holobiont':['S15'],'Chimera':['S14'],'Ectogenesis / Ectogestation':['S13'],
        'Mind Uploading':['S12'],'Necropolitics':['S29'],'Sympoiesis':['S06'],
        'The Uncanny / Unheimlich':['S30'],'Doppelgänger':['S30'],'New Weird':['S31'],
        'Biomechanical':['S22']}

prefix=(HERE/'REFERENCE-PREFIX.md').read_text()
old_defs={m.group(1):m.group(2).strip() for m in re.finditer(r'\| \*\*(.*?)\*\* \| (.*?) \|',prefix)}
TAIL_DEFS={
'Eroticism':'욕망·육체·친밀성·금기를 감각과 상징으로 탐구하는 영역.',
'Erotic Horror':'성적 욕망과 공포가 서사의 중심에서 얽히는 계열.',
'Fetishism':'특정 대상·재료·부위에 욕망이 집중되는 용법. 인류학·경제 비평 용법은 별도다.',
'L’amour fou':'이성적 계산과 사회 관습을 넘어서는 사랑과 욕망을 탐구하는 초현실주의 표현.',
'Jouissance':'라캉 이론에서 편안한 쾌락을 넘어 고통·실패의 반복과 얽히는 향유.',
'Eros / Death Drive':'정신분석에서 결합·생명·지속과 파괴·해체·반복의 관계를 설명하는 틀.',
'Sadism / Masochism':'고통·굴욕·지배·복종과 쾌락의 관계를 다루는 용어. 합의 여부는 별도다.',
'BDSM':'합의된 성인 사이의 속박·권력 교환·사도마조히즘 등을 포괄하는 용어.',
'Monstrous Intimacy':'비인간적 외형·존재 방식과 맺는 친밀한 관계의 비평·설정 표현.',
'Xenophilia':'낯선 것과 이질적인 것에 대한 호감·매혹. 모든 용법이 성적인 것은 아니다.',
'Androgyny':'남성적·여성적으로 읽히는 특징을 함께 가지거나 구분을 흐리는 외형적 표현.',
'Sexual Metamorphosis':'성적 신체 특징·생식 구조가 변하는 창작 모티프.',
'Reproductive Horror':'임신·출산·생식 능력·혈통·생식 통제를 중심으로 하는 공포.',
'Gynaehorror':'에린 해링턴의 여성 신체·성·생식과 생애 전반의 공포영화 분석 용어.',
'The Monstrous-Feminine':'바버라 크리드의 여성성·성·생식에 대한 문화적 불안과 괴물화의 분석 틀.',
'Reproductive Coercion':'타인이 개인의 생식 선택·지속·중단 등에 통제나 강요를 가하는 문제.',
'Incest Taboo':'가까운 친족 사이 성적 관계를 둘러싼 금기·규범.',
'Necrophilia':'죽은 신체를 향한 성적 욕망을 가리키는 개념.',
'Sexual Violence':'동의와 신체 자율성을 침해하는 성적 강제와 폭력.',
'Distributed Consent':'다중 몸·다중 인격의 동의를 어떻게 성립시킬지 묻는 이 대화의 설정어.',
'New Weird':'SF·판타지·공포와 기괴한 도시·사회·생태를 결합하는 문학적 경향.',
'Slipstream':'주류·장르 문학의 경계를 넘으며 현실감을 교란하는 비평적 명칭.',
'Biopunk':'생명공학·신체 개조·생물학적 통제·불평등을 다루는 SF 경향.',
'Scientific Romance':'초기 영국 SF 등의 사변적·철학적 이야기 계보를 가리키는 역사적 명칭.',
'Novum':'수빈의 SF 이론에서 작품 세계를 현실과 근본적으로 다르게 만드는 새로운 요소.',
'Cognitive Estrangement':'낯선 세계를 통해 현실 제도와 인식을 새롭게 보게 하는 SF 이론 개념.',
'Conceptual Breakthrough':'세계 이해의 틀 자체가 바뀌는 발견과 전환.',
'Literalized Metaphor':'비유 표현을 작품 세계의 실제 현상으로 구현하는 기법.',
'Unreliable Narrator':'서술자의 정보·해석·평가를 그대로 신뢰할 수 없게 하는 구성.',
'Mise en abyme':'작품 내부의 재현이 작품 전체의 구조나 사건을 되비추는 구성.',
'Metalepsis':'이야기를 말하는 층위와 말해지는 층위 등의 경계를 침범하는 구성.',
'Information Hazard':'정보의 획득·전달이 해를 일으키거나 가능하게 하는 위험.',
'Biopolitics / Biopower':'신체·인구·출생·건강과 삶을 관리·규범화하는 권력의 분석 틀.',
'Necropolitics':'집단을 죽음·소모·생존 조건 박탈에 노출시키는 권력의 분석 틀.',
'Dehumanization':'사람·집단의 인격과 도덕적 지위를 부정하거나 약화하는 과정.',
'Speciesism':'종 소속에 따라 이익과 도덕적 지위를 부당하게 차등 취급하는 태도.',
'Commodification of the Body':'신체·조직·능력을 판매와 교환의 대상으로 다루는 문제.',
'Memory Economy':'기억을 거래·상속·과세하는 자원으로 삼는 창작 설정어.',
'Xenofeminism':'기술·자연·젠더와 권력을 재검토하며 해방의 가능성을 모색하는 사상.'}

seeds=[];group=None
for line in (HERE/'seed-labels.txt').read_text().splitlines():
    if not line or line.startswith('#'):continue
    if line.startswith('['):group=line[1:-1];continue
    label=line; ko,_,en=label.partition(' — ')
    if not en:en=ko
    canonical=re.sub(r', .*','',en)
    kind,families,refs=GROUP_ROUTES[group]
    direct=DIRECT.get(canonical,[])
    seeds.append(dict(seed_id=f'K{len(seeds)+1:03}',group=group,label=label,ko=ko,en=canonical,
        definition_ko=old_defs.get(label,TAIL_DEFS.get(canonical,'')),
        definition_origin='prior conversation lead, not independently verified in every case',
        term_status='setting_or_motif_explicitly_marked' if any(s in label for s in ['설정어','모티프','사변적','SF 설정']) else kind,
        direct_source_ids=direct,family_background_source_ids=refs,
        evidence_status='direct_reference_scoped' if direct else 'family_background_only_term_specific_verification_pending',
        candidate_family_routes=families,
        candidate_route_limit='Possible illustrative neighborhoods only; no card asserts the full term and no automatic activation.',
        route='context_first_then_optional_visual_analogy',
        confusion_boundary_ko=BOUNDARIES.get(canonical,BOUNDARIES.get(canonical.split(' / ')[0],'개념의 성립 조건과 외형적 비유를 구분한다. 해당 용어의 원전·문맥을 추가 대조한 뒤 선택한다.')),
        automatic_visual_obligations=[],native_approval=False))
dump('keyword-register.json',{'schema':'research-keyword-register/v1','reference_conversation_id':'6ad98716-5014-83ee-b7a8-856a91f6e97c','keywords':seeds})
lines=['# 키워드별 의미·경로·혼동 경계','',
       '정의는 원 대화의 조사 출발점과 후반부 요약을 보존했다. 개별 정의 전체가 독립 검증되었다는 뜻은 아니다. 직접 자료도 sources.json의 실제 열람 범위를 따른다. 가족군 경로는 선택적 예시 이웃이며 해당 개념 전체를 가시적으로 충족하는 카드 목록이 아니다.','']
for group in GROUP_ROUTES:
    lines += ['## '+group,'','| ID·용어 | 정의 출발점 | 구분·반영 경계 | 자료 범위 |','|---|---|---|---|']
    for k in seeds:
        if k['group']!=group:continue
        refs=', '.join(k['direct_source_ids']) if k['direct_source_ids'] else '개별 검증 보강 필요'
        lines.append(f"| {k['seed_id']} {k['label']} | {k['definition_ko']} | {k['confusion_boundary_ko']} | {refs} |")
    lines.append('')
(HERE/'KEYWORD-MAP.md').write_text('\n'.join(lines)+'\n')
atlas=['# 가시 후보 초안 72개','', '모든 장면은 독립 저술한 연구안이다. 출처는 배경·유추이며 정본 디자인의 인용이 아니다. native facts, guard/effect, CID/RID, 역할 승인과 픽셀 검증은 아직 없다.','']
for f,(title,_) in FAMILIES.items():
    atlas += ['## '+f+' '+title,'','| ID·제목 | 한영 긍정 장면 | 혼동·한계 |','|---|---|---|']
    for c in cards:
        if not c['card_id'].startswith(f):continue
        atlas.append(f"| {c['card_id']} {c['title_ko']} | {c['proposal_ko']} / {c['proposal_en']} | {c['nearest_confusion_ko']} — {c['claim_limit_ko']} |")
    atlas.append('')
(HERE/'CANDIDATE-ATLAS.md').write_text('\n'.join(atlas)+'\n')
with (HERE/'seed-keywords.tsv').open('w') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['seed_id','group','label','term_status','evidence_status'])
    for k in seeds:w.writerow([k[x] for x in ['seed_id','group','label','term_status','evidence_status']])

CONTEXTS=[
('X01','원본 자아의 생존','복사·전송·실행·동일성은 각각 다른 주장. 케이블과 닮은 몸은 생존의 증거가 아니다.',['S07','S12']),
('X02','군체 의식과 군집지능','동기화된 자세·공유 선·같은 화면은 하나의 의식이나 실제 인지 처리를 입증하지 않는다.',['S07','S15']),
('X03','기관 없는 신체와 리좀','신체 조직화·관계의 철학을 실제 장기 제거·덩굴 장식으로 축소하지 않는다. 원전 보강 필요.',['S05']),
('X04','생식 방식과 권리','완전 체외 임신·단성생식·복제·키메라를 분리. 외형과 권한·선택권을 혼합하지 않는다.',['S13','S14','S28']),
('X05','초자연의 실제 작동','문자·회로·기도 자세·광원은 주문·기적·신성의 효과를 입증하지 않는다.',['S08','S09','S10','S11']),
('X06','소리와 감각','아쿠스마틱 소리·냄새·촉감·공감각 경험 자체는 정지 이미지에서 미검증.',['S22']),
('X07','역사와 시간','녹·층위·폐허·겹친 초상은 실제 연대·이전 문명·시간 여행을 확정하지 않는다.',['S02','S24']),
('X08','꿈과 관객의 공포','꿈 작업·응축·전치·누미노스·언캐니는 개념 또는 경험. 신체 외형만으로 정신 상태를 진단하지 않는다.',['S01','S04']),
('X09','욕망과 페티시 의미','에로티시즘·주이상스·죽음 충동·페티시 의미는 비평·욕망 맥락. 광택·재질·노출만으로 자동 부여하지 않는다.',['S02']),
('X10','성인 관계의 동의','BDSM·분산된 동의·사디즘/마조히즘은 합의·역할·주체를 개별 검토. 자세만으로 합의나 강제를 확정하지 않는다.',['S18']),
('X11','친족 금기와 죽음의 경계','근친 금기·시체 성애 용어를 연구에 보존하되 혈연·죽음·성적 욕망을 외형에 덧씌우지 않는다. 원전별 추가 검증 필요.',['S16','S17']),
('X12','생식 통제와 괴물화 비평','생식 강요·성적 폭력·괴물적 여성성은 권력·동의·문화적 구성 맥락. 특정 성·젠더·임신을 공포 태그로 만들지 않는다.',['S16','S17','S18']),
('X13','신체 훼손의 사건과 매체','절단·박피·적출·생체 해부·식인·자가 식인은 행위·결과·소유자·생사 조건이 다르다. 모형과 실제 사건의 대체 합격을 금지한다.',['S02','S22']),
('X14','제도와 상품화','배급·수선·전시·근무의 가시 장면과 생명정치·죽음정치·소유권·종차별의 제도 설명을 분리한다.',['S18','S29']),
('X15','서사 층위와 정보위험','그림 속 그림·문·읽는 자세만으로 메타렙시스·시뮬레이션·정보위험이 성립하지 않는다.',['S19']),
('X16','비인간 친족과 자율성','함께 사는 구조와 돌봄을 제안하되 인격·친족·진화적 이득·형태적 자유를 외형에서 증명하지 않는다.',['S06','S25'])]
dump('context-records.json',{'schema':'research-context-only/v1','records':[dict(context_id=i,title_ko=t,meaning_limit_ko=l,source_ids=s,source_scope='background only; individual concepts may require further primary reading',positive_visual_effects=[],native_approval=False) for i,t,l,s in CONTEXTS]})

# Cases are development material authored with the cards, not independent holdout results.
cases=[]
for c in cards:
    cases.append(dict(case_id='DEV-'+c['card_id'],cohort='development',query_ko=c['proposal_ko'],query_en=c['proposal_en'],expected=c['card_id']+': all directed relations; no narrative inference',status='NOT_RUN'))
controls=[
('boundary','기관 없는 신체라는 철학을 설명하는 개념 사진','A conceptual photo about the philosophical body without organs','Do not add organ removal'),
('boundary','세포 계통이 다른 키메라와 혼성 조형의 차이','Difference between cellular chimerism and hybrid-looking sculpture','Do not infer genetics from appearance'),
('boundary','기억 업로딩 장치의 케이블 연결','Cable connections on a fictional memory-upload device','Only connections; no successful survival claim'),
('boundary','비유클리드 기하학과 불가능한 계단의 차이','Distinguish non-Euclidean geometry from impossible stairs','No mathematical identity inferred'),
('boundary','창백한 인공 인물의 초상','Portrait of a pale artificial figure','Do not infer corpse or necrophilia'),
('boundary','장갑의 광택 표면과 손끝 접촉','A fingertip touching a glossy glove','Do not add fetish context or consent'),
('boundary','해부 전시 모형의 분리 부품','Separated parts of an anatomical display model','Do not substitute actual human injury'),
('boundary','단자와 연결된 원형 좌석','Circular seats connected to a terminal','Do not claim hive consciousness'),
('boundary','구속 도구가 놓인 비어 있는 작업실','Empty workshop containing restraint equipment','No BDSM or violence inference'),
('boundary','커다란 건물 앞의 녹색 덩굴','Green vines before a huge building','No arcology or living building inference'),
('boundary','방 안에 같은 방의 모형이 있는 사진','Photo of a room with a model of that room','No metalepsis from nesting alone'),
('boundary','다른 종 두 존재가 같은 그릇을 보는 장면','Two beings of different species looking at the same bowl','No genetic hybrid or kinship inferred'),
('boundary','양 태아의 체외 지원 연구를 참고한 허구 용기','Fictional vessel informed by extra-uterine lamb-support research','No completed human ectogenesis claim'),
('boundary','소매가 금속 가시에 걸린 성인','Adult with a sleeve caught on a metal spike','No skin penetration or injury added'),
('boundary','인공 몸 둘 앞에 같은 초상 카드','Identical portrait cards before two artificial bodies','No same person or cloning claim'),
('boundary','마법과 기술이 공존하는 정물','Still life in a world with magic and technology','No mandatory runes deity or ritual'),
('ordinary','평범한 다실의 주전자와 컵','Teapot and cup in an ordinary tearoom','No material transformation'),
('ordinary','일반 재봉 작업 사진','Ordinary sewing work photo','No biomechanical body'),
('ordinary','온실 재배대와 급수관','Greenhouse beds and water pipes','No living architecture'),
('ordinary','인공 손 부품 제품 사진','Product photo of an artificial hand part','No gore or actual human hand'),
('ordinary','복도 출입판과 문','Corridor access panel and door','No genetic segregation'),
('ordinary','종과 케이블의 박물관 전시','Museum exhibit of a bell and cable','No audible sound claim'),
('ordinary','비성적 성인 두 사람의 손 접촉','Nonsexual palm contact between two adults','No erotic escalation'),
('ordinary','낡은 벽 위 겹친 도료','Layered paint on an old wall','No vanished civilization'),
('ordinary','미니어처 도시 제품 사진','Product photo of a miniature city','No inhabited pocket universe'),
('ordinary','거울 앞 손을 편 인물','Person with an open hand before a mirror','Reflection keeps matching pose'),
('ordinary','평범한 인공 무릎 정비','Ordinary artificial-knee maintenance','No surgery or coercion'),
('ordinary','흰 종이 위 나무 무늬 문지르기','Rubbing wood texture onto white paper','Technique does not change photographic medium'),
('nonvisual','여러 몸의 동의는 모두 성립했다','All embodied selves have consented','Keep explicit context; never prove consent from pixels'),
('nonvisual','같은 자아가 업로드 후 생존한다','The same self survives uploading','Context only'),
('nonvisual','이 행성은 실제로 의식이 있다','This planet is conscious','Context only'),
('nonvisual','어떤 목소리가 벽 뒤에서 들린다','A voice is heard behind the wall','Sound not visually verifiable'),
('nonvisual','이 문장을 읽으면 신체가 바뀐다','Reading this sentence changes the body','Causal sequence not established by static frame'),
('nonvisual','두 인물은 유전적으로 복제 관계다','The two figures are genetic clones','No appearance-only proof'),
('nonvisual','이 사회는 기억을 상속하고 과세한다','This society inherits and taxes memories','Institution needs narrative context'),
('nonvisual','이 둘은 친족이며 금기를 논의한다','These two are kin discussing a taboo','Kinship not derived from likeness'),
('nonvisual','이 인물은 생식 통제를 거부한다','This character refuses reproductive control','Autonomy and refusal require context'),
('nonvisual','이 구조물은 수백만 년 전에 만들어졌다','This structure was built millions of years ago','Age not proven by weathering'),
('nonvisual','신이 의례에 실제로 응답한다','A deity truly responds to the ritual','No efficacy from light or gesture'),
('nonvisual','이 신체 변화는 자발적이며 즐겁다','This bodily change is voluntary and joyful','No coercion or pathology added')]
for n,(cohort,ko,en,expected) in enumerate(controls,1):cases.append(dict(case_id=f'C{n:02}',cohort=cohort,query_ko=ko,query_en=en,expected=expected,status='NOT_RUN'))
with (HERE/'EVALUATION-CASES.tsv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=list(cases[0]),delimiter='\t');w.writeheader();w.writerows(cases)
dump('COUNTS.json',dict(keywords=len(seeds),sources=len(sources),visual_drafts=len(cards),context_records=len(CONTEXTS),direct_reference_keywords=sum(bool(k['direct_source_ids']) for k in seeds),evaluation_cases=len(cases),bilingual_queries=len(cases)*2,planned_pixel_groups=12,planned_pixel_arms=3,planned_images=36,all_evaluations='NOT_RUN'))
print(json.dumps(json.loads((HERE/'COUNTS.json').read_text()),ensure_ascii=False))

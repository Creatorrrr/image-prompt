"""Build only this non-operating research package; no API or index writes."""
import csv
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]


def write_json(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


# Source notes are paraphrases. Staging below is independently authored and is
# not asserted to be an attested historical practice or an exhaustive variant.
SOURCE_ROWS = '''
S01|BFI / Adam Scovell: Where to begin with folk horror|https://www.bfi.org.uk/features/where-begin-with-folk-horror|body_read|풍경·고립·공동체의 신념·사건을 연결하는 장르 분석.|영국 영화 중심의 비평 틀이며 모든 지역·작품의 필수 공식이 아니다.
S02|Dawn Keetley: Introduction: Defining Folk Horror|https://www.revenantjournal.com/contents/introduction-defining-folk-horror-2/|body_read|장르의 역사와 민속의 기능, 영미 중심 정의의 범위를 논한다.|특정 영화의 설정을 실제 민속의 보편 사실로 옮길 수 없다.
S03|University Press of Colorado: The Folkloresque|https://www.upcolorado.com/utah-state-university-press/the-folkloresque|publisher_description_read|대중문화가 민속의 테마·캐릭터·이미지를 재창작하는 개념.|책 전체 독서가 아니며 창작 전통의 실제 연원을 증명하지 않는다.
S04|BFI: 10 great urban wyrd films|https://www.bfi.org.uk/lists/10-great-urban-wyrd-films|body_read|도시 공간의 층위와 기이함·부재를 영화 사례로 설명한다.|도시 또는 빈 공간 자체는 포크 호러 판정 근거가 아니다.
S05|OpenStax: Rituals of Transition and Conformity|https://openstax.org/books/introduction-anthropology/pages/13-4-rituals-of-transition-and-conformity|section_read|의례의 공유된 형식과 통과의례·경계 상태를 설명한다.|문턱 사진 한 장으로 사회적 신분 변화의 완료를 증명할 수 없다.
S06|National Trust: Hollow way, Easthope Wood|https://heritagerecords.nationaltrust.org.uk/HBSMR/MonRecord.aspx?skin=printerfriendly&uid=MNA141529|record_read|주변 땅보다 낮게 패인 실제 통행로의 깊이·폭과 용도를 기록한다.|개별 유적의 치수를 모든 holloway의 규격으로 쓰지 않는다.
S07|Visit Lindisfarne: Travel|https://visitlindisfarne.com/travel/|search_excerpt_read|섬으로 연결되는 도로는 썰물 때 건널 수 있는 조수 통로다.|현재 통행시간 안내나 실제 탈출 불가 상태를 조사한 자료가 아니다.
S08|English Heritage: Prehistoric Landscapes|https://www.english-heritage.org.uk/learn/story-of-england/prehistory/landscape/|relevant_passage_read|거석·봉분·선사 경계들이 풍경 속에서 서로 연결되고 중첩된다.|모든 거석이 희생 제단이거나 모든 인공 둔덕이 무덤인 것은 아니다.
S09|Historic England: St Winefride Holy Well, 1018702|https://historicengland.org.uk/listing/the-list/list-entry/1018702/|record_partial_read|성스러운 우물의 지정유산 기록과 장소 식별을 확인한다.|내부 전체 구조나 모든 치유 우물의 공통 형태까지 검증하지 않았다.
S10|National Museum of Ireland: May Day / Bealtaine|https://source.museum.ie/en-IE/Collections-Research/Folklife-Collections/Folklife-Collections-List-(1)/Religion-and-Calendar-Customs/May-Day|relevant_passage_read|장식한 May Bush, Maypole, 꽃과 리본 등 지역 세시풍속을 구별한다.|수확제·하지·메이데이·영화의 축제를 하나의 의례로 합치지 않는다.
S11|National Museum of Ireland: Cailleach / Last Sheaf|https://www.museum.ie/getmedia/cb38ad68-b0fe-45d8-b249-4a6eabd0076e/Cailleach.pdf|pdf_pages_1_2_text_read|마지막 곡식단을 엮어 수확을 기념하며 지역에 따라 활용이 달랐다.|사람 모양 인형이나 저주용 도구가 반드시 되는 것은 아니다. 원본 도판의 픽셀 검토는 안 했다.
S12|National Museum of Ireland: Ghost turnips and Samhain|https://source.museum.ie/en-IE/News/2023/Ghost-turnips%2C-pucas%2C-fortune-telling-and-evil-abd|search_excerpt_read|순무등·가면·점복 같은 박물관이 소개하는 할로윈 관습.|현대 호박등이나 모든 고대 사와인 의례의 동일성을 증명하지 않는다.
S13|Museum Wales: Mari Lwyd, F91.50|https://museum.wales/collections/online/object/cba385d3-1410-317d-b2af-0b763168523a/Mari-Lwyd/|record_and_search_body_read|말 두개골·장대·흰 천·리본을 갖춘 소장품과 성탄기 방문 풍속.|소장품의 탁구공 눈이나 장식을 모든 지역·시대의 필수로 고정하지 않는다.
S14|Historic England: What Are Witches' Marks?|https://historicengland.org.uk/whats-new/features/discovering-witches-marks/what-are-witches-marks|body_read|출입구·창·벽난로 주변 목재·돌에 새긴 방어 표식과 육엽문.|일부 표식의 기능은 논쟁 중이며 장인의 습작·장식 가능성도 남는다.
S15|MOLA: Witch bottles concealed and revealed|https://www.mola.org.uk/discoveries/research-projects/witch-bottles-concealed-and-revealed|body_and_search_excerpt_read|병 안의 핀·못 등의 내용물과 숨겨진 위치를 조사하는 연구.|밀봉된 불투명 병의 외관 사진으로 내용물이나 액체 성분을 확인할 수 없다.
S16|Museum of Witchcraft and Magic: Poppet 2089|https://museumofwitchcraftandmagic.co.uk/object/poppet-doll-3/|search_excerpt_read|천으로 된 인형과 옷·허리 끈을 기록한 현대 주술 보조물 사례.|모든 인형이 저주·피해·특정인의 머리카락을 뜻하지 않는다.
S17|Pitt Rivers Museum: Dorset hag stone|https://england.prm.ox.ac.uk/englishness-Dorset-hag-stone.html|relevant_passage_read|자연 구멍을 가진 돌과 지역의 액막이 믿음을 연결한다.|인공 구멍 장신구와 구별하며 구멍을 통해 초자연 존재가 보인다는 효과는 미입증이다.
S18|Cornell Library: Devils and Familiars|https://exhibits.library.cornell.edu/witchcraft/feature/devils-and-familiars|relevant_passage_read|사바트·음란한 집회·작은 동물 사역령을 묘사한 역사적 상상과 삽화.|박해자들의 혐의와 도상이 실제 의례·초자연 능력의 사실 증거가 아니다.
S19|English Heritage: Eight Witchcraft Myths|https://www.english-heritage.org.uk/learn/histories/eight-witchcraft-myths|page_partial_read|마녀술과 역사적 박해를 통속적 이미지와 구분할 참조 자료.|처형 방식·성별·시대별 보편 수치의 확인에는 사용하지 않았다.
S20|Library of Congress: The Green Man, Pagan or Not?|https://blogs.loc.gov/folklife/2023/11/the-green-man-pagan-or-not/|relevant_passages_read|잎사귀 얼굴과 이교 연속성 해석을 둘러싼 학술 논쟁을 검토한다.|조각의 존재가 중세의 비밀 이교 공동체나 특정 신의 실재를 증명하지 않는다.
S21|Rosslyn Chapel: Green Man|https://www.rosslynchapel.com/highlights/green-man/|body_read|건축 조각의 얼굴·입에서 뻗는 식물 형상을 확인한다.|해당 기관의 상징 설명을 모든 foliate head의 유일한 의미로 쓰지 않는다.
S22|Historic Environment Scotland: Supernatural Creatures|https://blog.historicenvironment.scot/2018/10/supernatural-creatures-scottish-folklore/|body_read|켈피의 말·인간형, 브라우니의 집안일·답례 관계와 지역 채록으로 연결한다.|한 형태를 전승 전체의 표준으로 고정하지 않으며 위협은 이야기 속 주장이다.
S23|Historic Environment Scotland: Orkney folktales, The Outrun|https://blog.historicenvironment.scot/2024/09/orkney-folktales-the-outrun/|search_excerpt_read|지역별 셀키 아내 이야기와 가죽을 빼앗는 판본을 소개한다.|가죽 외관만으로 변신·혼인·자유 박탈을 입증할 수 없다.
S24|Alfie Howard: Windigo Violence and Resistance|https://eprints.whiterose.ac.uk/id/eprint/212554/1/genealogy-08-00050.pdf|pdf_abstract_and_section_2_read|굶주림·겨울·탐욕의 서사와 현대 비원주민 매체의 사슴뿔 외형을 구분한다.|학술 리뷰이며 각 공동체의 원전·당사자 해석을 대신하지 않는다. 기본 괴물 외형 확정은 보류한다.
S25|Library of Congress: La Llorona, Introduction|https://blogs.loc.gov/folklife/2021/10/la-llorona-an-introduction-to-the-weeping-woman/|variants_passage_read|울음·물가·자녀 상실뿐 아니라 다양하게 달라지는 지역 판본을 소개한다.|흰옷·익사·두 아이·살해 동기를 일괄 필수화하지 않는다.
S26|CulturEd Philippines: Aswang|https://philippineculturaleducation.com.ph/aswang/|body_read|아스왕의 여러 유형 중 몸이 분리되어 상체가 나는 마나낭갈을 구분한다.|지역 간 차이를 보존하고 임신부·아동 공격이나 특정 외형을 자동 추가하지 않는다.
S27|National Museum of Ireland: Kingship and Sacrifice|https://source.museum.ie/en-IE/Museums/Archaeology/Exhibitions/Kingship-and-Sacrifice|body_read|이탄습지 시신과 왕권·희생의 연결을 전시의 해석 이론으로 명시한다.|모든 습지 시신의 사인·신분·의례 목적을 동일하게 확정하지 않는다.
S28|Historic England: The Living Dead, Wharram Percy|https://historicengland.org.uk/whats-new/news/archaeological-evidence-living-dead-in-mediaeval-england/|relevant_passage_read|특정 유골의 절단 흔적과 귀환 방지 해석, 식인 가설과의 차이를 설명한다.|비정상 매장 형태만으로 범죄·식인·뱀파이어의 실재를 판정할 수 없다.
S29|Whitby Museum: Hand of Glory|https://whitbymuseum.org.uk/hand-of-glory/|body_read|전승 속 손 촛대와 손가락 점화는 서로 다른 판본이며 소장 손에는 탄 흔적이 없다.|민담의 준비 절차·마술 효능을 실제 사실로 쓰지 않는다.
S30|Metropolitan Museum: Bronze phallic amulet, 60.117.7|https://www.metmuseum.org/art/collection/search/255092|object_record_read|로마 청동 생식기·손짓 부적의 액막이 용도를 설명한다.|성기 도상이 성행위·풍요 의례·성적 착취를 뜻하는 것은 아니다.
S31|Cambridge University Press: Myth of Sacred Prostitution|https://www.cambridge.org/core/books/myth-of-sacred-prostitution-in-antiquity/61198555C0E969D82AC0B8900F7D99E7|publisher_search_description_read|성전 매춘의 통속적 제도상을 부정하는 Stephanie Budin의 논지를 확인한다.|책·반론 전체를 읽지 않았으므로 역사적 합의가 완전히 확정됐다고 단정하지 않는다.
S32|University of Chicago Press: The Lord's First Night|https://press.uchicago.edu/ucp/books/book/chicago/L/bo3629910.html|publisher_description_read|초야권의 역사적 증거를 비판하는 Alain Boureau의 책 소개.|본문 전체 검토가 아니며 실제 성폭력의 부재를 주장하지 않는다.
S33|한국민족문화대백과사전: 금줄|https://encykorea.aks.ac.kr/Article/E0008002|definition_and_content_read|왼 새끼줄, 문기둥 사이 또는 신성한 대상의 경계, 지역별 부착물 차이.|출산·성별·가족관계·모든 부착물의 동시 사용을 시각으로 추정하지 않는다.
S34|한국민족문화대백과사전: 장승|https://encykorea.aks.ac.kr/Article/E0048619|definition_and_captions_read|사람 얼굴을 새긴 나무·돌 기둥과 마을 입구·길가의 기능.|모든 장승을 동일 표정·짝·명문·악령으로 고정하지 않는다.
S35|한국민족문화대백과사전: 솟대|https://encykorea.aks.ac.kr/Article/E0030608|definition_and_captions_read|마을 성역·경계의 신목과 새를 얹은 기둥의 자료를 확인한다.|새의 종류·수·방향은 지역·표본 확인 뒤 지정한다.
S36|한국민족문화대백과사전: 서낭당|https://encykorea.aks.ac.kr/Article/E0027672|definition_and_content_read|마을 어귀·고갯마루의 돌무더기, 신목, 천, 당집 등 여러 형태.|단일 건축형이나 일본 신사 외형을 기본값으로 쓰지 않는다.
S37|한국민족문화대백과사전: 굿|https://encykorea.aks.ac.kr/Article/E0006765|definition_and_captions_read|신을 청하고 대접하고 보내는 의례이며 목적과 지역 형식이 다양하다.|복식·악기 한 개로 강신·퇴마·종교적 진위를 단정하지 않는다.
S38|한국민족문화대백과사전: 씻김굿|https://encykorea.aks.ac.kr/Article/E0034204|ritual_subsections_read|무명 매듭 고풀이, 망자 상징물, 긴 무명 길닦음을 서로 구별한다.|지역·연행자별 차이와 상징물을 보존하며 실제 시신을 기본값으로 바꾸지 않는다.
S39|한국민족문화대백과사전: 동티|https://encykorea.aks.ac.kr/Article/E0016838|page_partial_read|금기를 어긴 뒤 재앙으로 설명되는 민속 개념의 참조 항목.|원인·질병·신령의 노여움의 사실 증거로 사용하지 않는다.
S40|Kokugakuin University: Shimenawa|https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9616|body_read|신성·청정한 공간을 구획하는 짚줄과 느슨한 짚, 선택적인 시데.|시데·장소·방향·굵기 조건을 모든 시메나와에 보편화하지 않는다.
S41|Kokugakuin University: Yorishiro|https://d-museum.kokugakuin.ac.jp/eos/detail/?id=9657|body_read|나무·돌·의례 도구·사람 등 신령이 내리는 매개라는 개념.|요리시로와 부정을 대리하는 가타시로를 같은 기능으로 합치지 않는다.
S42|UNESCO: Raiho-shin, 01271|https://ich.unesco.org/en/RL/raiho-shin-ritual-visits-of-deities-in-masks-and-costumes-01271|element_body_and_captions_read|가면·의상의 방문자, 집주인의 식사 환대, 지역별 역할·절차 차이.|무서운 외양을 악령·폭력·살인 의례로 해석하지 않는다.
S43|BGSU Libraries: Baba Yaga resources|https://libguides.bgsu.edu/fairytales/baba-yaga|bibliographic_search_excerpt_read|재화·변형·판본을 찾기 위한 도서관의 자료 안내.|특정 오두막·절구·악행의 완전한 원전 확인으로 사용하지 않는다.
'''.strip()


# id | seed numbers | family | Korean title | English visible realization |
# Korean visible realization | directed owner graph | distinguishing test |
# confusion boundary | claim limit | source ids | priority
VISUAL_ROWS = '''
L01|17|land|움푹 패인 옛길|A narrow footpath lies below both earth banks, with exposed roots crossing the bank faces.|좁은 보행로가 양쪽 흙둑보다 낮고 둑의 옆면에 뿌리가 드러나 있다.|path>below>banks;roots>on>banks|노면과 양옆 지표면 높이차 동시 확인|평지 숲길·터널|길의 연대·사용 목적은 사진만으로 확정 불가|S06|P0
L02|18|land|교차로의 선택|Three dirt paths meet beside one marker; a visitor stands at their junction.|세 흙길이 표식 옆에서 만나고 방문자 하나가 그 교점에 서 있다.|paths>meet_at>junction;visitor>stands_at>junction;marker>beside>junction|실제로 이어진 세 갈래와 선택 지점|갈라짐 없는 길·표식만 있는 들판|운명·계약·길의 반복은 정지 화면 미입증|S01|P1
L03|19,44|land|문턱의 양쪽|A raised wooden sill separates a lit interior from the dark exterior; a bowl rests outside the sill.|솟은 나무 문턱이 밝은 실내와 어두운 바깥을 나누고 그릇은 문턱 바깥에 놓여 있다.|sill>separates>interior;sill>separates>exterior;bowl>outside>sill|안과 밖·문턱·그릇의 위치 구분|출입구 없는 벽·안쪽 그릇|초대 여부·접근 금지의 초자연 효과 미입증|S05|P0
L04|20|land|잠긴 조수 통로|A road from the near shore continues under shallow seawater toward a visible island; marker posts trace the submerged route.|가까운 해안의 도로가 얕은 바닷물 아래로 이어져 보이는 섬을 향하고 표지 말뚝이 잠긴 노선을 잇는다.|road>connects>shore;road>toward>island;water>covers>road;posts>trace>road|육지·잠긴 연결 구간·섬을 한 화면에서 확인|호수에 끝난 길·일반 다리|현재 밀물 진행·안전한 통행시간·탈출 불가는 미입증|S07|P0
L05|16,44|land|숲의 금지 경계|A rough timber gate interrupts the only visible opening in a dense tree line; an adult remains on the path outside it.|거친 나무문이 빽빽한 숲 가장자리의 보이는 유일한 틈을 막고 성인은 그 밖의 길에 남아 있다.|gate>blocks>opening;opening>within>tree_line;adult>outside>gate|경계와 실제 통로의 차단 관계|아무 숲·떠 있는 문|실제 성림의 특정 문화·전능한 금지 효력 미입증|S01|P0
L06|21|land|환상열석의 공간|Weathered standing stones form a readable ring with an open central ground.|풍화된 입석들이 원형을 이루고 가운데 열린 지면이 읽힌다.|stones>encircle>central_ground|돌의 독립성과 원의 배치|아무 바위더미·절벽|제단·매장·희생·천문 기능은 별도 근거|S08|P0
L07|22|land|봉분과 통로|A low grass-covered mound has a stone-lined opening at its base and a path ending at that opening.|잔디 덮인 낮은 봉분 밑에 돌로 두른 입구가 있고 길이 그 입구까지 이어진다.|opening>at_base>mound;path>ends_at>opening|융기 구조와 드러난 입구의 연결|평지 묘비·일반 언덕|모든 봉분에 입구가 있는 것은 아닌 선택형 실현|S08|P1
L08|23,49|land|우물가의 봉헌 배치|A stone-lined water source has small votive objects placed on a dry ledge beside the water.|돌로 두른 수원 곁의 마른 턱에 작은 봉헌물들이 놓여 있다.|ledge>beside>water_source;objects>rest_on>ledge|수원·마른 턱·물건이 분리되어 보임|단순 욕조·물속 쓰레기|물의 치유력·물건의 진짜 의례 목적은 문맥|S09|P1
L09|24|land|이탄 절단면|Dark peat layers are exposed in a cut bank above a waterlogged hollow.|물이 고인 움푹한 지형 위 절단면에 검은 이탄층이 드러난다.|peat_layers>exposed_in>bank;bank>above>waterlogged_hollow|젖은 절단면의 겹과 지면 관계|마른 모래사막·아무 안개|이탄의 성분·연대는 외형만으로 확정 불가|S27|P1
L10|24|land|갈대 저습지|Tall reeds surround open channels of shallow standing water.|키 큰 갈대가 얕게 고인 물길을 둘러싼다.|reeds>surround>water_channels|식생과 열린 물길|건조 황야·깊은 바다|fen의 수문·생태학적 분류는 사진 단독 미입증|S01|P1
L11|24|land|열린 황야|Low scrub covers exposed rolling ground beneath an uninterrupted horizon.|낮은 관목이 탁 트인 기복 지형을 덮고 수평선이 막힘없이 이어진다.|scrub>covers>rolling_ground;horizon>above>rolling_ground|낮은 식생·열린 지형|수직 숲·이탄 채굴 단면|moor의 생태학적 정확성·고립된 사회는 문맥|S01|P1
L12|25|land|작물 손상의 비교|A strip of blackened drooping stalks borders upright green crop rows in the same field.|같은 밭의 검게 처진 줄기 띠가 곧게 선 녹색 작물 줄과 맞닿아 있다.|damaged_strip>borders>green_rows;damaged_strip>within>field;green_rows>within>field|손상 줄과 비교 줄이 함께 보임|수확 후 빈 밭·저주라고만 적은 장면|병원체·흉작 원인·마을 재난은 미입증|S02|P0
L13|26|land|겹친 땅의 기록|An excavation edge reveals an older stone wall beneath the cut end of a modern paved road.|발굴 가장자리에 현대 포장도로의 잘린 끝 아래 오래된 돌벽이 드러난다.|stone_wall>below>road;excavation_edge>exposes>stone_wall|현대 구조와 하부 석축의 층위|같은 높이의 폐허 두 개|종교·민족·정확한 연대는 판독 불가|S08|P0
L14|7,150|land|도시 밑의 흔적|A tiled station wall opens onto exposed older masonry behind its broken surface.|타일을 붙인 역 벽의 깨진 표면 뒤로 더 오래돼 보이는 석축이 노출된다.|tiles>cover>wall;break>exposes>masonry;masonry>behind>tiles|현대 마감과 드러난 하부 재료|중세 성채 전체·일반 지하철|실제 과거 사건·초자연 행위성은 미입증|S04|P1
O01|58,55|object|마지막 곡식단|A small bound sheaf with intact grain heads hangs above an emptied harvest table.|이삭이 붙은 작은 곡식단을 묶어 비워진 수확 작업대 위에 걸어 놓았다.|binding>holds>sheaf;sheaf>above>table|이삭과 줄기를 묶은 실제 재료|옥수수 알·저주 인형|마지막 수확물·다음 해 파종은 서사 정보|S11|P0
O02|57,54|object|메이폴의 연결|Ribbons descend from the top of one tall pole into the separate hands of adult dancers around it.|성인 춤꾼들이 한 높은 기둥 둘레에서 꼭대기에 연결된 리본을 각각 손에 잡고 있다.|ribbons>attached_to>pole_top;hands>hold>ribbons;dancers>around>pole|꼭대기에서 각 손까지 이어지는 연결|공중 리본·화관만 쓴 인물|불·희생·성적 행위를 의례명으로 추가하지 않음|S10|P0
O03|54|object|메이 부시|A cut leafy branch outside a house carries tied ribbons and cloth strips.|집 밖에 세운 잎 달린 가지에 리본과 천 조각을 묶어 두었다.|ribbons>tied_to>branch;cloth>tied_to>branch;branch>outside>house|가지의 지지와 부착물|메이폴·크리스마스트리|특정 지역 판본의 선택형이며 모든 벨테인의 공통 외형 아님|S10|P1
O04|53,85|object|순무등|A hollowed turnip with cut eye and mouth openings contains a small light on a windowsill.|눈과 입 구멍을 낸 속 빈 순무 안에 작은 불빛이 있고 창턱에 놓여 있다.|light>inside>turnip;openings>cut_into>turnip;turnip>on>windowsill|순무 외피·파낸 구멍·내부 광원|호박등·늪의 떠 있는 불빛|잭오랜턴의 여러 뜻과 도깨비불을 구분|S12|P1
O05|59,60|object|가면 방문극의 문전|Masked adult performers with visibly tied costume pieces wait outside a household doorway.|가면을 쓴 성인 연희자들이 매어 붙인 의상 조각을 드러낸 채 집 문밖에 서 있다.|masks>worn_by>performers;costume_parts>tied_to>performers;performers>outside>doorway|사람이 착용한 가면과 실제 문전의 관계|괴물의 자연 피부·모든 가면을 동일 행사로 분류|노래·연극 대사·지역 의례명은 별도 원전 확인|S13,S42|P1
O06|61|object|마리 루어드의 운반 구조|A horse-skull figure is fixed to a pole beneath trailing ribbons; a white cloth falls from behind the skull around its carrier.|말 두개골 형상을 장대에 고정하고 리본을 늘어뜨렸으며 두개골 뒤에서 흰 천이 내려와 운반자를 감싼다.|skull>fixed_to>pole;ribbons>attached_to>skull;cloth>falls_from>skull;cloth>around>carrier;carrier>supports>pole|두개골·장대 연결·천의 부착과 운반 관계|인체에 붙은 해골 머리·사슴뿔 괴물|문화 풍속의 물체 구조를 지키며 살해·괴물 실재는 추가하지 않음|S13|P0
O07|62|object|비어 있는 의례 형상|An oversized human-shaped wicker framework stands upright with its hollow interior visible through the weave.|사람 모양의 커다란 버들가지 틀이 서 있고 엮은 틈 너머로 빈 내부가 보인다.|weave>forms>human_shape;openings>reveal>hollow_interior|사람 형상·엮인 구조·빈 내부|시신·조각상 속 사람 자동 추가|위커 맨의 역사적 희생 관습은 이 물체로 입증되지 않음|S01,S03|P0
O08|71,45|object|천 주술 인형|A hand-stitched cloth figure has a red cord tied around its own waist.|손바느질한 천 인형의 허리에 빨간 끈을 묶어 놓았다.|stitches>join>cloth_figure;cord>around>figure_waist|인형 자체의 재료·봉합·허리 끈|사람의 실제 몸·자동 바늘 저주|치유·보조·사랑·해악의 목적은 분기 문맥|S16|P0
O09|72,50|object|숨겨진 방어병의 외관|A stoppered ceramic bottle rests in a shallow recess beneath a lifted hearth slab.|마개를 막은 도기병이 들어 올린 화덕 판석 아래 얕은 홈에 놓여 있다.|stopper>closes>bottle;bottle>inside>recess;slab>above>recess|병의 외관과 은닉 위치|일반 진열병·안 보이는 내부의 시각 PASS|병 내부의 못·소변·머리카락은 보이지 않음|S15|P0
O10|72,46|object|방어병 내용물의 별도 전시|An opened bottle sits beside a tray holding bent pins and a small lock of hair, each separate from the bottle.|열어 둔 병 옆 쟁반에 구부린 핀들과 작은 머리카락 다발을 병과 분리해 놓았다.|tray>beside>bottle;pins>on>tray;hair>on>tray|열린 병과 분리된 내용물의 가시 관계|불투명 병을 투시·액체 성분 판정|출토 진위·원래 소유자·유래는 서사. 밀봉 branch와 동시 적용 금지|S15|P0
O11|73,50|object|출입구의 육엽문|A small six-lobed compass-drawn design is scratched into the timber jamb beside a doorway.|문 옆 나무 문설주에 컴퍼스로 그린 듯한 여섯 잎무늬가 작게 새겨져 있다.|design>incised_in>jamb;jamb>beside>doorway|여섯 잎의 기하와 건축 표면의 위치|피부 낙인·오각별·발광 마법진|방어 의도는 해석이며 표식만으로 마녀의 존재나 효능 미입증|S14|P0
O12|75|object|해그 스톤|A naturally rounded stone hangs from a cord passing through its irregular opening.|자연스럽게 둥근 돌의 불규칙한 구멍에 끈을 통과시켜 매달았다.|cord>passes_through>stone_opening;opening>within>stone|돌 재료·관통 구멍·끈의 통과|금속 펜던트·막힌 홈|구멍의 자연 형성·보호 능력은 픽셀만으로 확정 불가|S17|P1
O13|70|object|마도서의 물체성|A worn bound book lies open with hand-drawn diagrams on its paper pages.|낡은 제본 책을 펼쳐 종이 면 위의 손으로 그린 도형이 보인다.|pages>part_of>book;diagrams>on>pages|책·페이지·도형의 부착 관계|떠 있는 홀로그램·실제 언어 판독 자동 PASS|주술 효능·저자·판독 불가 텍스트의 내용은 미입증|S18|P1
O14|68|object|사역령을 암시하는 동물 관계|A small cat rests beside an adult's open working book while the adult looks toward the same animal.|작은 고양이가 성인의 펼친 작업 책 옆에 있고 성인은 그 동물을 바라본다.|cat>beside>book;adult>looks_at>cat|동물·사람·시선 대상의 관계|고양이만 있으면 마녀·동물 자동 변형|사역 계약·초자연 능력은 문맥에만 둠|S18|P1
O15|86|object|잎사귀 얼굴 조각|A carved stone face has vine forms emerging from the mouth and curling around both cheeks.|돌에 새긴 얼굴의 입에서 덩굴 형상이 나와 양 볼 둘레로 휘어진다.|vines>emerge_from>mouth;vines>around>cheeks;face>carved_in>stone|입·덩굴의 연속성과 석재 표면|살아 있는 숲의 신·잎 왕관만 있는 얼굴|그린맨 도상과 단일한 이교 신·신앙 연속성을 분리|S20,S21|P0
O16|87|object|뿔 달린 의례 가면|A horned mask is visibly strapped onto an adult performer's head.|뿔 달린 가면을 성인 연희자의 머리에 끈으로 매어 놓았다.|horns>part_of>mask;straps>attach>mask;mask>worn_by>performer|가면·부착 끈·착용자의 분리|자연 뿔 해부·웬디고 기본 외형|단일 뿔 신·현대 종교·악마를 동일시하지 않음|S18,S03|P1
O17|49,51|object|바치는 물건과 수용처|An adult's open palms extend a small wrapped object toward a low stone ledge.|성인의 편 손바닥이 작은 포장물을 낮은 돌턱 쪽으로 내민다.|palms>support>offering;palms>toward>ledge|손·물건·수용처의 분리와 방향|빈 손·상대 몸을 물건으로 치환|봉헌 의도·서약·응답·대가는 문맥|S08,S05|P1
O18|108,50|object|생식기 도상의 부적|A small bronze amulet bearing a phallic form hangs from a suspension loop.|남근 형상이 있는 작은 청동 부적을 매다는 고리에 걸어 놓았다.|phallic_form>part_of>amulet;loop>supports>amulet|청동 물체·도상·고리|실제 성행위·실라나기그와 동의어 처리|이 로마 사례는 액막이 물체이며 성적 의례의 증거 아님|S30|P1
R01|27,28|relation|공동체 원 바깥의 방문자|A lone adult visitor stands outside a loose circle of adults at the end of a narrow field path.|들판의 좁은 길 끝에서 성인 방문자 하나가 성인들의 성긴 원 바깥에 서 있다.|visitor>outside>adult_circle;path>ends_at>adult_circle|방문자와 집단·길·원 바깥 위치|기존 동일 실현을 새 CID로 복제|혈통·신앙·공모는 미입증. 기존 완전 소스 우선 비교|S01|P0
R02|30|relation|환대와 막힌 출구|A host offers a filled bowl while another adult stands across the open exit behind the guest.|주인이 그릇을 내미는 동안 다른 성인이 손님 뒤의 열린 출구를 가로막고 서 있다.|host>offers>bowl;blocker>across>exit;exit>behind>guest|제공과 출구 차단이 함께 보임|친절한 식사만·닫힌 문만|감금·동의·모든 주민의 의도는 한 장으로 확정 불가|S01,S02|P0
R03|31,33,97|relation|지목받는 한 사람|Several adults point toward one separated adult while leaving a clear gap around that person.|여러 성인이 떨어져 선 성인 하나를 가리키고 그 사람 둘레에는 빈 간격이 남아 있다.|group>points_at>isolated_adult;gap>around>isolated_adult|손끝·시선·지목 대상이 일치|집단 사진·민족 외형으로 악역 지정|유죄·마녀·공모·비난의 정당성은 문맥|S18,S02|P0
R04|36|relation|제비뽑기의 순간|One adult hand lifts a marked folded slip from a box held by another adult.|한 성인의 손이 다른 성인이 든 상자에서 표시된 접힌 쪽지를 들어 올린다.|holder>holds>box;hand>lifts>slip;slip>from>box|두 소유자·손·상자·쪽지의 연속 관계|떠 있는 제비·결과 숫자 판독만 의존|살해·공정성·피선정자의 운명은 서사|S02|P0
R05|31,145,147|relation|집단의 같은 방향|Adults seated along both sides of a table turn their heads toward the same doorway while one visitor remains facing forward.|탁자 양편에 앉은 성인들이 같은 문 쪽으로 고개를 돌리지만 방문자 하나는 정면을 향한다.|group>oriented_to>doorway;visitor>faces>forward;group>beside>table|집단 방향과 한 사람의 차이|모두 카메라 응시·임의 다중 시선|동시 동작·합창·암묵적 합의는 미입증|S05|P0
R06|147,29|relation|사람과 물건의 의례 배치|Equal bowls form a ring around a central empty stool; adult participants stand outside the bowls.|같은 그릇들이 빈 의자 둘레에 원을 이루고 성인 참여자들은 그릇 바깥에 서 있다.|bowls>encircle>stool;participants>outside>bowls|중심·그릇 원·바깥 사람의 순서|사람과 그릇의 위치 뒤바뀜|배치가 잔혹한 도덕·제물·종교를 직접 입증하지 않음|S05|P1
R07|6,11,148|relation|아름다운 들판의 차단|In bright sun, flowering field rows lead to adults standing shoulder to shoulder across a narrow exit path.|밝은 햇볕 아래 꽃 핀 밭고랑이 좁은 출구 길을 어깨를 맞대고 가로막은 성인들에게 이어진다.|field_rows>lead_to>exit_path;adults>block>exit_path|밝은 들판과 구체적인 차단 행위 공존|그냥 아름다운 축제·어두움 자동 추가|두려움·누미노제·범죄 의도는 별도 평가|S01,S02|P0
R08|9,10,37|relation|빈자리와 남은 흔적|A used plate and a pulled-back chair interrupt an otherwise evenly set table with no person at that place.|고르게 차린 식탁의 한 자리만 사용한 접시와 뒤로 빠진 의자가 있고 그 자리에 사람은 없다.|plate>at>place;chair>pulled_from>place;place>within>table_setting|반복 배치 속 빈자리와 사용 흔적|빈 방 전체·인물 자동 추가|실종·죽음·유령·시간 경과는 미입증|S04|P1
R09|38,12|relation|통과 직전|An adult with one foot raised stands before a cloth-hung entrance while two adults wait on the far side.|한 발을 든 성인이 천을 건 입구 앞에 있고 다른 성인 둘이 반대편에 기다린다.|entrant>before>entrance;cloth>hangs_at>entrance;receivers>beyond>entrance|이쪽·경계·저쪽의 구분|이미 통과한 자세·천이 몸을 자름|입문·신분 변화·강제성은 문맥|S05|P1
R10|32,34,35|relation|계보와 규칙의 물체 단서|An older ledger with branching ink lines lies beside a newer family photograph on the same desk.|가지친 잉크 선이 있는 오래된 장부와 더 새로워 보이는 가족사진이 같은 책상 위에 놓여 있다.|ledger>on>desk;photograph>on>desk;lines>on>ledger|두 기록 매체와 도식의 가시 대조|텍스트만으로 저주 증명·실제 친족 추정|관습법·조상의 빚·유전·혈연은 판독되지 않으면 미입증|S03|P1
V01|98|body|습지에서 드러난 보존 신체|A darkened preserved human hand and forearm emerge from an exposed peat layer, with the remaining extent hidden in earth.|검게 변한 보존 인체의 손과 팔뚝이 노출된 이탄층에서 드러나고 나머지는 흙에 가려져 있다.|hand>continuous_with>forearm;forearm>emerges_from>peat|손·팔의 연결과 이탄 접점|완전 신체가 보인다는 주장·미라 장식|사망 원인·왕권·희생·전신 보존 여부 미입증|S27|P0
V02|99|body|귀환 방지로 해석되는 배치|An excavated grave contains prone skeletal remains with a heavy stone resting above the upper back.|발굴 무덤에 엎드린 유골이 있고 등 위쪽에 무거운 돌이 놓여 있다.|remains>inside>grave;stone>above>upper_back|발굴 범위·몸의 방향·돌의 위치|모든 특이 매장을 동일 의례로 단정|특정 사례를 본뜬 허구 배치. 실제 Wharram Percy의 동일 양식 주장 아님|S28|P1
V03|100|body|영광의 손의 한 판본|A dried hand-shaped object supports one candle between its fingers on a stand.|마른 손 모양 물체의 손가락 사이에 초 하나를 받쳐 받침대 위에 놓았다.|candle>between>fingers;fingers>part_of>hand_object;hand_object>on>stand|손 형상·독립된 초·지지 관계|손가락 모두가 타는 다른 판본과 합침|전승의 선택형 도상이며 소장품의 원래 사용·실제 인체 재료 미입증|S29|P1
V04|90,91,92|body|봉헌물과 붉은 액체|A shallow bowl containing dark red liquid rests on a low support while adults face it from a distance.|검붉은 액체를 담은 얕은 그릇을 낮은 받침에 놓고 성인들이 거리를 두고 그쪽을 향한다.|liquid>inside>bowl;bowl>on>support;adults>face>bowl|액체·용기·참여자의 거리|붉은색만으로 인간 피·살해 증명|혈액·종·소유자·의례 효능은 시각 미입증; 명시된 맥락은 따로 보존|S02,S27|P1
V05|93|body|벽 속 인체 형상의 은닉|A broken wall reveals a wrapped adult-sized human-shaped bundle inside its narrow cavity.|깨진 벽의 좁은 공동 안에 성인 크기의 사람 모양으로 감싼 꾸러미가 드러난다.|bundle>inside>wall_cavity;break>reveals>bundle|벽 두께·공동·꾸러미 범위|시신이라고 단정·기초 희생과 동의어|사람·생사·살해·건축 목적은 명시 맥락에 한정|S03|P1
V06|95,96,97|body|강제의 물리적 단서|An adult's two wrists are bound together by a visible cord while a separate adult holds the free end.|성인의 두 손목이 보이는 끈으로 함께 묶여 있고 다른 성인이 끈의 끝을 잡고 있다.|cord>binds>wrists;wrists>part_of>bound_adult;holder>holds>free_end;free_end>part_of>cord|양 손목·매듭·끈 끝과 타인의 손|손가락 끈·공중 매듭|동의·무죄·재판·형벌·성폭력은 단독 이미지로 확정 불가|S18|P1
V07|103,104,105,110|body|성인 나체와 의례 문맥의 분리|A nude adult seen from behind stands in a shallow stone bathing basin, with a folded robe on the dry rim.|뒤에서 본 나체 성인이 얕은 돌 목욕 분지에 서 있고 마른 가장자리에 접은 겉옷이 놓여 있다.|adult>inside>basin;robe>on>rim;rim>part_of>basin|나체 성인·분지·분리된 겉옷이 읽힘|옷 입은 인물을 나체라고 판정·나체를 성행위로 승격|성인 나체는 직접 외형이지만 의례·입문·성혼·동의·풍요는 문맥. 특정 관습 재현 아님|S05,S18|P1
K01|127|korea|한국 금줄의 구조|A left-twisted straw rope spans two wooden gateposts; charcoal pieces and short pine sprigs are tucked into the same rope.|왼쪽으로 꼰 새끼줄이 두 나무 문기둥을 잇고 같은 줄에 숯 조각과 짧은 솔가지를 끼워 놓았다.|rope>connects>gateposts;charcoal>tucked_into>rope;pine>tucked_into>rope|양끝·꼬임·두 종류 부착물의 연결|일본 시데·발광 마법진·고추 필수화|선택한 재료 판본이며 출생·성별·모든 지역의 공통형 미입증|S33|P0
K02|123|korea|서낭당의 누석과 신목|A roughly conical stone pile stands at a village path junction beside a mature tree bearing tied cloth strips.|마을 길목의 대략 원뿔형 돌무더기 옆에 천 조각을 묶은 큰 나무가 서 있다.|pile>beside>tree;cloth>tied_to>tree;pile>at>path_junction|누석·나무·부착 천·길목의 관계|일본 도리이·하나의 돌탑을 모든 서낭당으로 고정|다양한 서낭당 중 한 형식이며 실재 수호신·동티 미입증|S36|P0
K03|125|korea|장승의 기둥과 얼굴|A weathered wooden post beside a village road has a carved human-like face near its top.|마을길 옆 풍화된 나무 기둥 위쪽에 사람 같은 얼굴이 새겨져 있다.|face>carved_in>post;post>beside>road|얼굴과 같은 통나무 기둥의 연속성|솟대·자연 사람·서양 토템 기둥으로 일괄 치환|짝·명문·표정·재료는 별도 판본 조건|S34|P0
K04|126|korea|솟대의 새와 장대|A carved bird figure is fixed to the top of a long wooden pole at a village edge.|마을 가장자리의 긴 나무 장대 꼭대기에 조각한 새 형상을 고정했다.|bird_figure>fixed_to>pole_top;pole>at>village_edge|새 형상·꼭대기 접점·장대 전체|날아가는 새·장승 얼굴·십자가|새 종·수·방위·마을의 실제 풍요는 미입증|S35|P0
K05|124,127|korea|당산나무의 보호 경계|A broad old tree stands within a straw-rope boundary whose ends are tied to separate posts.|굵은 오래된 나무가 짚줄 경계 안에 있고 줄 양끝은 서로 다른 기둥에 묶여 있다.|rope>encloses>tree;rope_ends>tied_to>posts|나무·줄의 범위·양끝의 지지|나무에 감은 줄과 무조건 같은 branch|이 배치는 저술한 선택안이며 특정 마을의 당산제 재현 아님|S36,S33|P0
K06|118,120|korea|굿의 연행과 상차림|An adult ritual performer faces a prepared offering table while a separate seated musician holds a drum at the side.|성인 의례 연행자가 차린 제상 쪽을 향하고 옆의 별도 앉은 악사가 북을 들고 있다.|performer>faces>offering_table;musician>beside>performer;musician>holds>drum|연행자·악사·북·제상의 소유 분리|모든 굿을 퇴마·비명·중국 도사 복식으로 처리|지역·복식·거리·공수·강신 여부는 별도 확인|S37|P0
K07|122|korea|고풀이의 매듭|An adult performer holds a long plain cotton strip with a visibly loosened knot between two hands.|성인 연행자가 두 손 사이에 풀려 느슨해진 매듭이 보이는 긴 무명천을 들고 있다.|hands>hold>cotton_strip;knot>within>cotton_strip;knot>between>hands|무명·두 손·실제 매듭의 접점|오색 끈 기본값·시간적 완전 해소 PASS|망자의 한·정화·실제 풀리는 연속 과정은 미입증|S38|P0
K08|122|korea|씻김의 망자 상징물|A rolled mat enclosing clothing forms an upright body-like bundle with a bowl placed at its top.|옷을 감싼 돗자리를 세워 몸통 같은 꾸러미를 만들고 그 위에 주발을 올렸다.|mat>encloses>clothing;mat>forms>upright_bundle;bowl>on_top>bundle|돗자리·옷·주발이 이루는 상징 구조|실제 노출 시신·일본 종이 인형|지역 제차의 일부이며 상징물 전체·씻김 효능을 자동 충족하지 않음|S38|P0
K09|122|korea|길닦음의 긴 무명|A small symbolic spirit object rests on a long white cotton strip stretched across an open floor.|작은 넋 상징물이 열린 바닥에 길게 편 흰 무명천 위에 놓여 있다.|spirit_object>on>cotton_strip;cotton_strip>across>floor|상징물과 지지 천·길게 이어진 공간|시신 이동·극락 도달을 시각 사실화|사용된 판본의 의미는 문맥이며 사후 세계의 실재 미입증|S38|P1
J01|135|japan|시메나와와 시데의 선택형|A thick braided straw rope is tied around a tree trunk, with folded white paper streamers hanging from the same rope.|굵게 꼰 짚줄을 나무 몸통 둘레에 묶고 같은 줄에 접은 흰 종이 시데를 매달았다.|rope>around>tree;paper_streamers>hang_from>rope|줄·시데·나무의 부착|한국 금줄의 숯·고추와 동의어|시데는 선택한 branch의 조건이며 모든 시메나와의 필수 아님|S40|P0
J02|134|japan|매개로 지정한 나무|An uncarved standing tree is marked by a small prepared ritual emblem at its base.|조각하지 않은 나무 밑에 마련한 작은 의례 표식을 두었다.|emblem>at_base>tree|자연물과 의례 표식의 구분|가타시로의 대속 기능·나무 자동 인간화|요리시로라는 기능은 선언된 문맥; 신의 실제 강림 미입증|S41|P1
J03|133|japan|내방신의 방문과 환대|Adults wearing frightening masks and straw costumes stand at a household entrance as the host presents a meal tray.|무서운 가면과 짚 의상을 입은 성인들이 집 입구에 서 있고 집주인은 음식 쟁반을 내민다.|masks>worn_by>visitors;costumes>worn_by>visitors;visitors>at>entrance;host>offers>meal_tray|착용자·문전·집주인·음식 방향|악령의 습격·살인 교단·모든 내방신의 짚 의상 필수화|나마하게에서 영감 받은 선택형; 각 지역 실제 재현은 추가 원전 필요|S42|P0
E01|80|entity|켈피의 말형 변주|A wet horse-shaped figure stands at the bank of a dark pool, with waterweed caught in its mane.|젖은 말 형상의 존재가 어두운 웅덩이 가장자리에 서 있고 갈기에 수초가 걸려 있다.|figure>at_bank>pool;waterweed>caught_in>mane;mane>part_of>figure|말형·물가·갈기와 수초|말과 인간형을 동시에 합침·자동 납치|외형은 선택적 창작 실현; 수초의 전승상 인간형 단서를 말형으로 옮긴 저술임|S22|P1
E02|81,113|entity|셀키의 가죽 소유 관계|An adult stands on a rocky shore while another adult holds a separate sealskin beyond the first adult's reach.|바위 해안의 성인 하나가 손을 뻗고 다른 성인이 그 손이 닿지 않는 곳에서 분리된 물범 가죽을 들고 있다.|holder>holds>sealskin;sealskin>beyond_reach>reaching_adult;adults>on>shore|두 성인·별개 가죽·도달 거리|인어 꼬리·동물과 성행위 자동 추가|변신·혼인·납치·동의는 맥락에 한정|S23|P1
E03|82|entity|브라우니의 답례 배치|A small humanoid figure stands beside a worked flour sack; a separate bowl of food rests on the nearby floor.|작은 사람형 존재가 작업한 밀가루 자루 옆에 서 있고 가까운 바닥에 음식 그릇이 따로 놓여 있다.|figure>beside>sack;bowl>on>floor;bowl>near>figure|일감·소형 존재·답례물의 분리|할로윈 악마·보수 계약 확정|야간 노동 완료·답례 규칙 위반의 결과는 서사|S22|P1
E04|140|entity|라 요로나의 한 연출|An adult woman with a shawl stands alone beside a riverbank, one hand covering her face.|숄을 두른 성인 여성이 강가에 홀로 서서 한 손으로 얼굴을 가리고 있다.|woman>beside>river;shawl>worn_by>woman;hand>covers>face|물가·숄·가린 얼굴|흰 드레스·두 아이·살해를 보편 필수화|선택한 연출은 정체성·울음 소리·자녀 죽음을 증명하지 않음|S25|P1
E05|142|entity|마나낭갈의 분리 범위|A winged adult upper-body figure hovers above a separately standing lower-body form, with a clear gap between the two forms.|날개 달린 성인 상반신 형상이 따로 선 하반신 형상 위에 떠 있고 두 형태 사이에 분명한 틈이 보인다.|wings>part_of>upper_body;upper_body>above>lower_body;gap>separates>upper_body;gap>separates>lower_body|상·하체 양쪽과 분리 간격 동시 확인|보통 날개 인간·허리 가림·모든 아스왕이 동일|초자연 정체는 판본 문맥; 피해자·임신·포식은 자동 추가하지 않음|S26|P1
F01|148,6|form|대낮의 구체적 위협|Hard midday shadows fall across a flower-covered table as an adult hand slides its only exit latch shut.|꽃으로 덮인 탁자에 한낮의 단단한 그림자가 드리우고 성인의 손이 유일하게 보이는 출구 빗장을 닫고 있다.|shadows>across>table;flowers>on>table;hand>moves>latch;latch>on>exit|한낮 조명과 구체적 출구의 빗장|꽃만 있는 축제·밤 분위기로 치환|닫는 시간 진행·동기·전체 탈출 불가 미입증|S01,S02|P0
F02|146|form|민속적 제작 흔적|Uneven hand stitches join patched cloth around a rough wooden frame, with straw ends caught at the joins.|거친 나무틀 둘레의 덧댄 천을 고르지 않은 손바느질로 잇고 접합부에 짚 끝이 끼어 있다.|stitches>join>cloth_patches;cloth>around>frame;straw>caught_at>joins|생활 재료·접합·사용 흔적|낡은 물건이면 고대·모든 문화의 동일 재료|연대·진품·민족·의례 목적을 재료에서 추정하지 않음|S13,S16|P0
F03|150,10|form|기록물 사이의 반복|Two paper photographs and a field notebook lie side by side, with the same simple geometric mark visible in both photographs and on the notebook sketch.|종이 사진 두 장과 현장수첩을 나란히 놓고 두 사진 및 수첩 스케치에 같은 간단한 기하 표식이 보인다.|photos>beside>notebook;mark>on>photo_one;mark>on>photo_two;mark>on>notebook|세 매체에서 표식의 실제 대응|설명 글만·판독 못 하는 얼굴 동일성|사진 연대·동일 인물·저주·기록 진위는 미입증|S03,S04|P0
F04|143,144,145,149|form|민속 채록의 물체|A fieldworker holds a small recorder toward a seated adult storyteller, with an open notebook on the worker's lap.|조사자가 앉은 성인 구술자 쪽으로 작은 녹음기를 내밀고 자기 무릎에는 펼친 수첩을 둔다.|worker>holds>recorder;recorder>toward>storyteller;notebook>on>worker_lap|기기·화자·수첩의 소유와 방향|녹음기만으로 특정 노래 내용 증명|음성·가사·선창과 응답의 시간적 순서는 미입증|S03|P1
'''.strip()

CONTEXT_ROWS = '''
X01|1,2,5,6,7|장르와 민속의 범위|장소·전승·공동체·금기를 해석하되 장르 이름으로 모든 형상을 강제하지 않는다.|S01,S02
X02|3,4|민속풍 재창작과 만들어진 전통|창작 설정·현대 재구성과 실제 기록을 구분하고 각각의 시기와 저술 주체를 기록한다.|S03
X03|8,9,10,11|낯섦·부재·과거의 잔향·매혹|관객의 감정과 비평적 해석은 장면의 개별 증거와 분리한다. 오래된 테이프가 곧 hauntology의 성립은 아니다.|S04
X04|12,37,38,52,53,54,55,56,57,58,59,60,61,62|경계·순환·세시 달력|계절·절기·지역·의례 단계는 각각 기록한다. 꽃·불·추수·가면을 모두 한 축제에 합치지 않는다.|S05,S10,S11,S12,S13
X05|13,14,15,26|땅의 행위성과 장소의 영|지하·뿌리·층위는 가시 단서이고 땅의 요구·고의·영적 실재는 서사적 명제다.|S01,S08
X06|27,28,29,30,31,32,33,34,35,36,51|공동체의 권력과 계약|차단·지목·선정·교환을 구체화하되 법·혈통·공모·저주·계약의 효력은 외형으로 확정하지 않는다.|S01,S02
X07|39,40,41,42,43,44,49,50|신앙과 금기|애니미즘·토테미즘·조상 제의·이교·혼합을 서로 다른 개념으로 보존한다. 공동체 전체를 살인 집단으로 자동 해석하지 않는다.|S02,S18,S37,S42
X08|45,46,47,48,64,65,66,68,69,70,71,72,73,75|주술의 대상과 관계|닮음·접촉·점복·전조·방어·해악은 다른 관계다. 머리카락·인형·핀의 소유·분리·접촉을 보되 효능·의도는 문맥이다.|S14,S15,S16,S17,S18
X09|67,74,106,114,115|박해 혐의와 성적 도상|사바트·악마의 낙인·성교 혐의는 사료의 주장 주체를 표시한다. 의례적 난교와 초자연 방문을 실제 확인 관습으로 승격하지 않는다.|S18,S19
X10|76,77,78,79,83,84,85,87,88,89,139|전승 존재의 판본|이름만으로 유아 바꿔치기·예고 울음·사냥 행렬·검은 개의 정체·야마우바의 행동을 확정하지 않는다. 원전이 약한 존재별 외형 신규 후보는 후순위다.|S22,S43
X11|63,90,91,92,93,94,95,96,97,98,99,100,101,102|죽음·희생·식인·신체 훼손|생사·재료·피해·사인·시신 처리·희생 목적을 분리한다. 유골 변형·붉은 액체·상차림만으로 살해·식인·인신공양을 추정하지 않는다.|S18,S27,S28,S29
X12|103,104,105,107,108,109,110,111,112,113|성·생식·혼인·통제|성인 나체·성기 도상·성행위·풍요·임신·강요·족내혼·근친을 별도 필드와 문맥으로 남긴다. 명시 요청을 누락하거나 다른 의미로 은폐하지 않는다.|S30,S18
X13|116,117|논쟁적 성 관습의 역사|성전 매춘과 초야권은 검토한 연구자의 주장·시대·범위를 표기하고 통속적 보편 제도로 확정하지 않는다.|S31,S32
X14|118,119,120,121,128,129,130,131|한국 무속의 직능·공수·부정·동티|강신·직능 계승·신병의 민속 해석·공수·천도·손님신의 질병 의미는 의상·표정만으로 입증되지 않는다. 손님굿을 일반 방문자 장면과 합치지 않는다.|S37,S38,S39
X15|132,134,136,137,138|일본 민속의 기능과 오염 개념|마레비토·요리시로·가타시로·게가레·하라에·원령·타타리·츠키모노의 기능을 구분한다. 같은 종이·나무 외형이 같은 기능의 증거는 아니다.|S41,S42
X16|143,144,145|음성·가사·응답의 한계|입 모양·녹음기·집단 배치와 실제 음성·노랫말·차례를 분리한다. 연속음·선창 후 응답은 스틸 이미지에서 검증할 수 없다.|S05
X17|149,150|전설의 행동화와 기록 진위|현장 방문·문서·녹음은 가시적일 수 있으나 전설을 믿어 따라 했는지·기록이 진짜인지는 별도 근거다.|S03
X18|141|웬디고의 현대 외형과 원전|뿔·사슴 해골을 전통 기본값으로 만들지 않는다. 특정 원전·공동체·현대 매체를 지정하고 확정하지 못한 외형 후보는 보류한다.|S24
X19|80,81,82,86,140,142|이름과 외형의 대응 한계|선택한 켈피·셀키·브라우니·그린맨·라 요로나·마나낭갈 연출은 한 판본 또는 저술한 표현이다. 이름과 가시 형상의 일대일 대응을 요구하지 않는다.|S20,S22,S23,S25,S26
'''.strip()


def build():
    sources = []
    for line in SOURCE_ROWS.splitlines():
        sid, title, url, access, supports, limit = line.split('|')
        sources.append(dict(id=sid, title=title, url=url, access=access,
                            supports=supports, limit=limit, accessed_on='2026-10-22',
                            media_pixel_inspection=False))
    cards = []
    for line in VISUAL_ROWS.splitlines():
        cid, seeds, family, title, en, ko, relations, test, confusion, limit, refs, priority = line.split('|')
        graph = []
        for relation in relations.split(';'):
            source, predicate, target = relation.split('>')
            graph.append(dict(source=source, predicate=predicate, target=target))
        owners = sorted({x[k] for x in graph for k in ('source', 'target')})
        cards.append(dict(id=cid, family=family, title_ko=title,
            seed_numbers=[int(x) for x in seeds.split(',')], priority=priority,
            evidence_mode='observable_realization', phrase_en=en, phrase_ko=ko,
            owners=owners, relations=graph, distinguishing_observation=test,
            confusion_boundaries=confusion.split('·'), claim_limit=limit,
            source_refs=refs.split(','), source_support_scope='Definition/object/critical distinction only; exact scene is an authored proposal.',
            historical_status='authored_optional_realization_not_attested_practice',
            gates=[dict(id=cid+'-G1', requirement=test, scope='all declared distinguishing components together'),
                   dict(id=cid+'-G2', requirement='각 관계의 양 끝·소유·부착·범위가 같은 원본 화면에서 식별됨', scope='actual selected relation graph')],
            missing_evidence='UNOBSERVABLE_NOT_PASS', partial_is_fail=True,
            adoption='reuse_review_first' if cid=='R01' else 'compare_existing_then_refine_or_new',
            native_qualification='NOT_RUN', registration='NOT_IN_OPERATING_MANIFEST'))
    for line in CONTEXT_ROWS.splitlines():
        cid, seeds, title, limit, refs = line.split('|')
        cards.append(dict(id=cid, family='context', title_ko=title,
            seed_numbers=[int(x) for x in seeds.split(',')], priority='P0_boundary',
            evidence_mode='context_only', claim_limit=limit, owners=[], relations=[],
            source_refs=refs.split(','), gates=[], positive_candidate_allowed=False,
            source_support_scope='Family-level boundary only; every term is not independently verified.',
            adoption='context_or_defer_term_by_term', registration='NOT_IN_OPERATING_MANIFEST'))
    seeds = json.loads((ROOT/'seed-keywords.json').read_text())['terms']
    routes = []
    for seed in seeds:
        title=seed['title']; parts=title.split(' — ',1)
        matching=[c for c in cards if seed['number'] in c['seed_numbers']]
        routes.append(dict(seed_number=seed['number'], title=title,
            terms_ko=parts[0].split('·'), terms_en=[x.strip() for x in parts[1].split('/')] if len(parts)==2 else [],
            card_refs=[c['id'] for c in matching],
            routing='optional_visual_plus_context' if any(c['evidence_mode']=='observable_realization' for c in matching) else 'context_or_defer',
            qualification='RESEARCH_ROUTE_ONLY',
            fact_check='family_level_source; term-specific original source required before cultural/historical claim'))
    drafts=[]
    catalog=json.loads((REPO/'skills/photo-prompt-image-generator/assets/photo_candidate_slot_catalog.json').read_text())['slot_catalog']
    roles={'land':['location','background_element'],'object':['prop','surface_material'], 'relation':['composition','relational_action'],
           'body':['body_pose','prop'],'korea':['prop','location'],'japan':['prop','location'],
           'entity':['subject'],'form':['composition','lighting']}
    for c in cards:
        if c['evidence_mode']!='observable_realization': continue
        proposed=roles[c['family']]
        drafts.append(dict(id='draft_'+c['id'], card_ref=c['id'], phrase_en=c['phrase_en'], phrase_ko=c['phrase_ko'],
            owners=c['owners'], relations=c['relations'], hard_components=c['distinguishing_observation'],
            render_gates=c['gates'], claim_limit=c['claim_limit'], source_refs=c['source_refs'],
            proposed_roles=[r for r in proposed if r in catalog],
            unresolved_role_names=[r for r in proposed if r not in catalog],
            role_approval='NOT_REVIEWED; family role suggestions cannot approve full-source effects',
            conditional_policy='complete one selected realization; no union with alternative branches',
            frozen_core_rule='post-core optional; preserve requester meaning and all locks',
            intrinsic_effect_review='NOT_RUN; derive all actual owner/count/appearance/setting/action effects before adoption',
            native_source_units='NOT_AUTHORED', cid=None, rid=None, status='RESEARCH_DRAFT_ONLY'))
    write_json('sources.json',dict(schema='folk-horror-sources/v1',sources=sources))
    write_json('semantic-cards.json',dict(schema='folk-horror-semantic-research/v1',cards=cards))
    write_json('keyword-routes.json',dict(schema='folk-horror-keyword-routes/v1',routes=routes))
    write_json('candidate-drafts.json',dict(schema='folk-horror-candidate-drafts/v1',drafts=drafts))
    with (ROOT/'SOURCES.tsv').open('w') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(['id','title','url','access','supports','limit'])
        for s in sources:w.writerow([s[k] for k in ('id','title','url','access','supports','limit')])
    atlas=['# 150개 원 대화 항목의 반영 경로','', '분류와 연결은 연구 제안이다. route는 실제 검색 실행이나 native 의미 승인이 아니다.','', '| 번호 | 원 대화 항목 | 경로 | 카드 |','|---|---|---|---|']
    for r in routes: atlas.append(f"| {r['seed_number']} | {r['title']} | {r['routing']} | {', '.join(r['card_refs'])} |")
    (ROOT/'KEYWORD-ATLAS.md').write_text('\n'.join(atlas)+'\n')
    lines=['# 관측 가능한 시각 의미와 문맥 카드','', '아래 장면은 출처가 확인한 단서에서 저술한 선택형 실현이다. 각 항목은 전체 전승의 표준 외형이 아니다.','']
    for c in cards:
        lines += [f"## {c['id']} {c['title_ko']}", '', f"원 항목: {', '.join(map(str,c['seed_numbers']))} / {c['evidence_mode']} / {c['priority']}", '']
        if c['evidence_mode']=='observable_realization':
            lines += [c['phrase_ko'], '', c['phrase_en'], '', '관계: '+'; '.join(f"{r['source']} → {r['predicate']} → {r['target']}" for r in c['relations']), '', '확인: '+c['distinguishing_observation'], '', '혼동: '+' / '.join(c['confusion_boundaries']), '']
        lines += ['주장 한계: '+c['claim_limit'], '', '출처: '+', '.join(f"[{s}]("+next(x['url'] for x in sources if x['id']==s)+')' for s in c['source_refs']), '']
    (ROOT/'VISUAL-CARDS.md').write_text('\n'.join(lines))
    print(json.dumps(dict(seeds=len(seeds),routes=len(routes),sources=len(sources),cards=len(cards),visual_drafts=len(drafts),context_cards=len(cards)-len(drafts)),ensure_ascii=False))


if __name__=='__main__':
    build()

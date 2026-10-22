"""Write authored research evaluation cases, without executing retrieval."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
# set | ids | Korean request | English request | expected judgment
ROWS = '''
development|L01|양쪽 흙둑보다 낮은 옛길과 드러난 뿌리가 보이게 해줘.|Show a sunken footpath below both earth banks with exposed roots.|낮은 노면과 양 둑의 높이차가 있는 complete source
development|L04|섬으로 가는 길 일부가 얕은 바닷물 아래 잠긴 모습을 육지부터 보여줘.|Show the road from the mainland toward an island with a section submerged in shallow seawater.|섬·육지·연결 노선·잠긴 구간을 함께 보이는 실현
development|R02|주인은 밥그릇을 내밀고 다른 주민은 손님 뒤의 출구를 막고 있어.|The host offers a meal bowl while another villager blocks the exit behind the guest.|제공자·손님·차단자의 소유와 역할 유지
development|R04|성인 한 명이 든 상자에서 다른 성인이 표시된 제비를 들어 올리는 순간.|One adult lifts a marked slip from a box held by a second adult.|두 성인·상자·손·쪽지의 접점 보존
development|O06|마리 루어드의 말 두개골 형상과 장대와 흰 천이 어떻게 연결됐는지 보이게.|Make the horse-skull figure, pole and white cloth connections of a Mari Lwyd readable.|운반 물체 구조. 해골 머리 인체로 치환 금지
development|O09|화덕 돌판 아래 숨긴 밀봉 도기 방어병의 겉모습.|The exterior of a stoppered ceramic protective bottle concealed below a hearth slab.|은닉 외관만. 내부 내용물 가시 주장 금지
development|O10|열린 방어병 옆 쟁반에 구부린 핀과 머리카락을 따로 전시해줘.|Display an opened protective bottle beside bent pins and hair on a separate tray.|밀봉 branch와 합치지 않는 개봉 전시
development|O11|문설주 나무에 긁어 새긴 작은 육엽 방어 표식.|A small six-lobed protective mark scratched into a timber door jamb.|여섯 잎과 건축 표면의 위치
development|K01|양 문기둥을 잇는 왼 새끼 금줄에 숯과 솔가지를 끼운 모습.|A left-twisted Korean straw boundary rope spans two gateposts with charcoal and pine tucked into it.|시데 자동 추가 없이 재료·양끝·부착 유지
development|K02|마을 고갯길의 돌무더기와 천 조각 묶인 신목으로 된 서낭당.|A village pass shrine with a stone pile beside a tree carrying tied cloth strips.|해당 서낭당 형식만. 도리이 자동 추가 금지
development|K03|길가 통나무 기둥 위쪽에 사람 얼굴을 새긴 장승.|A jangseung beside a road with a human-like face carved into the upper part of a wooden post.|같은 기둥과 새긴 얼굴. 새 조각과 구별
development|K04|마을 끝 긴 장대 꼭대기에 새 조각을 고정한 솟대.|A sotdae at a village edge with a carved bird fixed to a tall pole.|새와 장대의 실제 접점. 생물 새와 구별
development|K06|굿 연행자와 옆에서 북을 든 별도 악사, 앞의 제상.|A gut performer faces an offering table with a separate drum-holding musician beside them.|세 주체의 소유·역할. 지역 외형은 별도 검토
development|K07|성인 연행자의 양손 사이 긴 무명천 매듭이 느슨하게 풀린 모습.|An adult performer holds a long cotton strip with a loosened knot between both hands.|천·매듭·손의 실제 연결
development|K08|씻김굿의 망자 상징물로 옷을 감싼 돗자리 위에 주발을 올려줘.|Show a spirit effigy for ssitgim-gut formed from clothing rolled in a mat with a bowl on top.|상징 구조. 실제 시신으로 바꾸지 않음
development|J01|나무 몸통에 감은 시메나와에서 흰 종이 시데가 내려오게.|A shimenawa around a tree trunk has folded white shide hanging from the same rope.|나무·줄·시데 부착, 금줄 부착물과 구별
development|J03|짚 의상과 무서운 가면을 쓴 성인 방문자에게 집주인이 음식을 내미는 장면.|The host offers food to adult visitors wearing straw costumes and frightening masks.|가면 착용자와 환대 관계. 악령 공격으로 전환 금지
development|O15|돌에 새긴 얼굴의 입에서 나온 덩굴이 양 볼을 감싸게.|On a carved stone face, vines emerge from the mouth and curl around both cheeks.|석재 얼굴·입·덩굴의 연속 관계
development|O01|이삭이 남은 마지막 곡식단을 묶어 수확 작업대 위에 걸어줘.|Hang a bound last sheaf with intact grain heads above a harvest table.|실제 곡식 재료. 사람 인형 필수화 금지
development|O02|기둥 꼭대기 리본이 둘레 성인 춤꾼의 손까지 이어지는 메이폴.|Maypole ribbons connect the pole top to the hands of adult dancers around it.|각 리본의 양끝과 소유자
development|V01|노출된 이탄층에서 보존된 손과 팔뚝만 드러나고 나머지는 흙에 가려져 있어.|A preserved hand and forearm emerge from peat while the rest remains hidden in earth.|보이는 범위만. 전신·사인·희생 주장 금지
development|E02|해안의 한 성인이 손을 뻗고 다른 성인이 물범 가죽을 손이 닿지 않게 들고 있어.|One adult reaches on a shore while another holds a sealskin out of reach.|두 성인·분리 가죽·거리 관계
development|E05|날개 달린 성인 상반신과 아래에 남은 하반신의 분리 틈이 모두 보이게.|Show a winged adult upper body and the separate lower body below with their gap visible.|모든 분리 범위 가시. 날개만으로 PASS 금지
development|F03|사진 두 장과 조사수첩 세 군데에 같은 단순 표식이 반복되게.|Repeat the same simple mark in two photographs and a field notebook.|세 매체의 실제 표식 대응
boundary|O11,X09|건물의 마녀 방어 표식과 사람 피부의 악마 낙인을 구분해줘.|Distinguish building protection marks from an alleged devil's mark on a person's skin.|물체 표면과 신체 혐의를 같은 후보로 합치지 않음
boundary|K01,J01|한국 금줄을 원하고 일본 종이 시데는 넣지 말아줘.|Use a Korean geumjul without Japanese shide paper streamers.|같은 경계 역할만으로 문화 부착물 오염 금지
boundary|O07,X11|안이 비어 있는 버들가지 사람 형상이고 안에 사람은 없어.|The human-shaped wicker framework is empty with no person inside.|effigy를 인신공양 또는 내부 인물로 자동 확장 금지
boundary|O09,O10|불투명한 병을 밀봉한 채로 안의 핀이 보였다고 판정하지 마.|Do not claim the pins are visible inside an opaque sealed bottle.|UNOBSERVABLE_NOT_PASS. 개봉을 임의 추가하지 않음
boundary|E02,X19|셀키 가죽 이야기이며 인어 꼬리를 붙이지 마.|This is a selkie-skin story; do not add a mermaid tail.|명시된 존재·가죽과 해부 의미 보존
boundary|O14,X08|책 옆 고양이는 평범한 반려동물이며 마법 계약은 없어.|The cat beside the book is an ordinary pet with no magical pact.|동물의 동반과 사역 계약을 분리
boundary|L08,X07|우물의 형태만 보여주고 치유가 일어났다고 결론내리지 마.|Show the well's form without concluding that healing occurred.|장소 외형과 효능 분리
boundary|V04,X11|붉은 액체가 담긴 그릇이지만 피인지는 알려지지 않았어.|A bowl contains red liquid whose identity as blood is unknown.|색으로 성분·소유자·살해 추론 금지
boundary|V01,X11|습지 시신이 있다는 사실만으로 왕의 희생이라고 판단하지 마.|A bog body alone does not establish a sacrificed king.|관측·신분·사인·목적 구분
boundary|R03,X06|한 사람을 모두 가리켜도 그 사람이 유죄라고 단정하지 마.|People pointing at one person does not establish that person's guilt.|지목과 법적·도덕적 사실 구분
boundary|X18,O16|웬디고라는 이름만으로 사슴뿔과 사슴 해골을 기본값으로 넣지 마.|Do not default to deer antlers or a deer skull from the name windigo alone.|현대 매체 외형의 전통 원형 승격 금지
boundary|V07,X12|성인 나체를 보여주는 것과 성행위·성적 입문 의식은 다른 의미야.|Adult nudity, sexual activity and sexual initiation are distinct meanings.|노출과 행위·의도·의례의 자동 합침 금지
boundary|X12|족내혼이라고 했지만 가까운 친족의 성관계를 말한 것은 아니야.|Endogamy here does not mean sexual relations between close relatives.|집단 내부 혼인과 근친 의미 구분
boundary|J03,X15|내방신은 무서운 가면을 쓰지만 복을 비는 방문 의례야.|The masked visiting deities look frightening within a good-fortune visitation ritual.|악령·폭력·살인 관계 자동 추가 금지
boundary|O15,X19|잎사귀 얼굴 조각으로 중세 비밀 이교 집단의 실재를 증명하지 마.|A foliate-head carving does not prove a secret medieval pagan community.|도상과 역사적 연속성 분리
boundary|X09,X13|박해 문헌의 마녀 사바트 혐의를 확인된 실제 관습으로 적지 마.|Do not turn witch-sabbath allegations in persecution records into established practice.|사료의 주장과 실재·기능 분리
ordinary_control|L01|평평하고 넓은 숲길의 평범한 산책 사진.|An ordinary walk along a broad level woodland path.|패인 길·금기·의례 자동 추가 금지
ordinary_control|O02|성인들이 리본 메이폴 주변에서 즐겁게 춤추는 풍경.|Adults happily dance around a ribbon maypole.|희생·감금·주술적 위협 자동 추가 금지
ordinary_control|L12|건강한 녹색 작물이 자라는 농부의 일상.|A farmer's daily work beside healthy green crops.|흉작·저주 자동 추가 금지
ordinary_control|F02|현대 매장에서 짚색 가방을 진열한 제품 사진.|A product display of a straw-colored bag in a modern shop.|색상을 실제 짚 재료·의례로 승격 금지
ordinary_control|L14|출근길 지하철역에서 기다리는 성인들.|Adults wait in a subway station on their commute.|발굴·폐허·도시 주술 자동 추가 금지
ordinary_control|K04|바위 해안에서 실제 새를 관찰하는 사진.|A wildlife photograph of real birds on a rocky shore.|새 조각·솟대·신령 자동 추가 금지
ordinary_control|O09|주방 선반에 있는 밀봉 도기병의 상품 사진.|A product photograph of a sealed ceramic bottle on a kitchen shelf.|은닉 방어병·내용물·주술 자동 추가 금지
ordinary_control|O13|손으로 그린 식물 그림이 있는 평범한 펼친 책.|An ordinary open book with hand-drawn botanical diagrams.|마도서·해악·악마 자동 추가 금지
nonvisual_control|X16|한 장의 사진으로 선창 뒤에 모두가 응답하는 정확한 소리와 순서를 증명할 수 있나.|Can a single photograph prove the exact sound and sequence of a call followed by a group response?|음성·시간 순서는 검증 불가로 기록
nonvisual_control|X04|의례가 수백 년간 매년 반복되었다는 것을 사진 한 장의 사실로 확정하지 마.|Do not establish centuries of annual ritual repetition as a fact from one photograph.|순환 시간·연대·빈도를 픽셀 사실로 승격 금지
nonvisual_control|X08|머리카락을 인형에 붙였다는 모습이 실제 접촉 주술의 성공을 증명하지는 않아.|Hair attached to a doll does not establish that contagious magic succeeded.|부착 관계와 효능 구분
nonvisual_control|X12|표정이나 옷차림만으로 혼인·성적 동의·혈연을 확정하지 마.|Do not establish marriage, sexual consent or kinship from expression or clothing alone.|동의·관계·신분의 근거 한계 유지
'''.strip()

with (ROOT/'EVALUATION-CASES.tsv').open('w') as f:
    w=csv.writer(f,delimiter='\t');w.writerow(['id','set','card_refs','query_ko','query_en','expected_judgment','execution_status'])
    for n,line in enumerate(ROWS.splitlines(),1):
        kind,cards,ko,en,expect=line.split('|')
        w.writerow([f'FH{n:03}',kind,cards,ko,en,expect,'NOT_RUN'])
print('Authored cases:',len(ROWS.splitlines()),'Bilingual queries:',len(ROWS.splitlines())*2)

"""Compile hand-authored research proposals. Never writes distributable assets."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OWNER = "the request-supported costume wearer"

# These are research abstractions, not confirmed specifications of every named version.
# id | family | ko | subject | directed relation | object | evidence 1 | evidence 2
# | source IDs | disposition | reuse IDs | nearest misleading substitute
ATOM_ROWS = r"""
U01|joseon|몸판과 소매의 배색 경계|the robe body|separate_from|the contrasting sleeves|The body is one continuous color area below the armhole.|A different sleeve color begins at the selected armhole or sleeve boundary.|S03|supported_relation||동다리의 모든 연대를 한 배색으로 고정한 긴 코트
U02|joseon|소매 없는 전복이 안쪽 소매 위에 겹침|the sleeveless outer robe|layered_over|the inner long-sleeved robe|The outer robe has open armholes rather than its own sleeves.|The inner sleeves emerge through those armholes and belong to the same wearer.|S02|supported_relation||소매 달린 겉두루마기 또는 식재료 전복
U03|joseon|철릭의 상의와 주름 하의가 허리에서 연결됨|the robe upper body|connected_to|the pleated lower robe at the waist|A visible waist join separates the upper body from the lower folds.|The pleated lower cloth continues from that same join.|S01|supported_relation||독립된 치마를 코트 아래에 입은 조합
U04|joseon|선택된 철릭 소매의 탈착 경계|the detachable sleeve|connected_to|the upper robe attachment edge|The selected sleeve has its own attachment edge.|A fastening or separation boundary is visible at that edge rather than only a decorative seam.|S01|supported_relation||모든 철릭에 탈착 소매를 부과하거나 숨은 여밈을 보였다고 판정
U05|cavalry|가슴 브레이드의 양끝이 같은 재킷에 붙음|the repeated chest braids|attached_to|the same jacket front|Each selected braid has visible front attachment points.|The braid crosses between those points on the same jacket.|S04|reuse_existing|ccx_cc05_02,costume_ccx_cc05_02|공중에 떠 있는 끈 또는 옆 사람의 견장 끈
U06|cavalry|어깨에 걸친 펠리스의 빈 소매와 고정끈|the fur-edged short coat|draped_over|one shoulder of the inner-jacket wearer|A separate short coat rests on one shoulder above the inner jacket.|Its hanging sleeve is unoccupied and the support cord belongs to the coat.|S04|supported_relation||양팔을 모두 끼운 모피 재킷이나 어깨 위 모피 스톨
U07|cavalry|차프카의 각진 윗판과 별도 챙|the four-cornered cap top|connected_to|the lower cap body above its brim|The top has a distinct four-corner outline.|A separate lower body and brim remain below the angular top.|S05|supported_relation||원통 샤코나 단순 사각 학사모
U08|cavalry|플라스트론 앞판이 튜닉 몸판 안에 놓임|the contrasting chest plastron|attached_to|the front of the selected tunic|A bounded chest panel belongs to the tunic front.|The panel edge remains inside the body rather than becoming a separate vest.|S05|needs_primary_verification||출처가 확인되지 않은 연대 배색을 모든 창기병에 적용
U09|cavalry|주아브 재킷에 붙은 가짜 조끼 앞판|the false vest panel|attached_to|the short jacket|The vest-like front panel is joined to the jacket construction.|Its boundary does not establish an independently worn inner waistcoat.|S06|supported_relation||별도 조끼를 필수로 추가한 삼중 겹침
U10|cavalry|넓은 바지통이 발목의 좁은 경계로 모임|the full trouser legs|gathered_into|the narrow lower-leg boundary|Each leg has visible excess width above the lower leg.|That same cloth narrows toward the selected ankle or gaiter boundary.|S06|needs_primary_verification||넓은 치마 한 장 또는 모든 주아브복의 발목 주름 강제
U11|guards|높은 모피 모자가 머리 위에 독립된 부피를 가짐|the tall fur-textured cap|worn_by|the tunic wearer|The cap has a tall continuous outer volume above the head.|Its lower edge sits on the same wearer rather than merging with hair.|S60|supported_relation||검은 머리카락을 베어스킨으로 판정하거나 모든 연대에 깃털 추가
U12|guards|킬트 앞의 스포런이 허리에서 별도로 매달림|the sporran pouch|suspended_from|the waist belt in front of the kilt|A distinct pouch has its own outline in front of the kilt.|A belt or chain supports it at the same wearer's waist.|S05|needs_primary_verification||타탄 주름치마만으로 특정 하이랜드 연대와 스포런을 확정
U13|military|짧은 야전 상의 밑단이 별도 하의 허리에 닿음|the short field blouse hem|meets|the separate trouser waist|The upper garment ends at a visible hem near the waist.|Separate trousers continue beneath that hem.|S07|needs_primary_verification||일체형 커버올 또는 모든 시대 야전복의 공통 재단으로 확대
U14|military|선택된 역사 표식의 부착 위치와 바탕 면|the requested historical insignia|attached_to|its specified garment or cap carrier|The requested emblem has a bounded visible shape.|Its placement is tied to the selected sleeve band, collar tab or cap rather than floating nearby.|S08,S09|supported_relation||검은 제복만으로 SS를 추론하거나 요청된 유물 표식을 임의의 판타지 문양으로 바꿈
U15|military|AGSU의 코트·셔츠·하의 배색이 각 부품에 귀속됨|the green service coat|layered_over|the tan shirt above taupe trousers|The green outer coat remains distinct from the tan shirt at its opening.|The trousers form a separate taupe lower garment on the same wearer.|S11|supported_relation||상의·셔츠·하의를 모두 같은 녹색으로 칠한 군복
U16|military|청색 정복 외피와 흰 셔츠의 경계|the blue service coat|layered_over|the white shirt|The blue coat has its own lapel or front opening.|The white shirt is visible within that opening rather than recoloring the coat.|S12|supported_relation||ASU와 AGSU의 색을 혼합하거나 모든 바지에 금색 줄을 강제
U17|military|전투복 여밈과 몸판 주머니가 별도 기능 면을 이룸|the utility pockets|attached_to|the jacket body beside its front closure|The front closure follows the jacket's center axis.|The selected pocket openings lie on the body and do not become printed camouflage shapes.|S13|supported_relation||카모 무늬만으로 주머니·여밈·계급·성능이 충족됐다고 판정
U18|military|같은 재단 위에 놓인 선택 위장 무늬|the selected camouflage shapes|distributed_across|the garment panels|Pattern areas lie within cloth panels and continue across the selected seams.|Their scale and colors follow one chosen pattern version.|S10,S13|needs_primary_verification||ACU 재단과 OCP 무늬를 한 동의어로 취급하거나 봄·가을 양면을 동시에 표시
U19|sailor|세일러 칼라가 어깨에서 직사각 등판으로 이어짐|the sailor collar|continues_onto|the upper back panel|The collar spreads across both shoulders of one wearer.|Its rear portion has a distinct broad panel rather than a narrow shirt collar.|S56,S61|reuse_existing|ccx_cc03_01,costume_ccx_cc03_01,clothing_ct041_v2|V넥 리본만으로 세일러 칼라를 충족하거나 군인·학생 신분 자동 부여
U20|sailor|1859 청색 프록의 깃·커프스가 몸판과 같은 계열임|the collar and cuffs|share_color_with|the blue frock body|The visible collar is blue without the earlier white applied collar.|The visible cuff edges remain blue rather than added white cuffs.|S56|supported_relation||1841의 흰 덧깃을 1859 이후 기본형에도 필수로 유지
U21|sailor|바지통이 무릎 아래에서 넓어지는 하단 윤곽|the lower trouser legs|widen_toward|their separate hems|Each trouser leg remains a separate tube below the knee.|Its hem is wider than the selected knee region.|S56|supported_relation||모든 수병복·교복에 벨보텀을 강제하거나 긴 치마로 대체
U22|sailor|노퍽 재킷의 세로 주름을 가로 벨트가 감쌈|the coat waist belt|crosses_over|the vertical coat pleats|Visible pleat lines descend along the selected coat panels.|A separate belt encircles that same coat at waist level.|S57|supported_relation||1917 여성 사무병복을 짧은 세일러 미니드레스로 바꿈
U23|flight|직물 일체형 비행복의 앞지퍼와 별도 지퍼 주머니|the front zipper|runs_along|the fabric coverall body|A single fabric body continues from torso into separate trouser legs.|The main zipper is distinct from selected pocket zippers on that body.|S15|supported_relation||항공 조종사 셔츠·바지 또는 헬멧 연결 압력복과 합침
U24|flight|조종사 셔츠 견장과 흉장 표식의 위치 분리|the shirt shoulder tabs|attached_to|the shoulders above a separate chest badge|The tabs sit on the selected shirt's shoulders.|A requested wing badge occupies the chest independently of the shoulder tabs.|S18|needs_primary_verification|ccx_cc05_01,costume_ccx_cc05_01|항공사·계급 확인 없이 네 줄 견장·흰 모자·윙 배지를 필수화
U25|flight|헬멧 경계가 압력복 몸체의 목 연결부에 닿음|the integrated helmet edge|connected_to|the suit neck assembly|The helmet and visor have visible enclosing boundaries around the head.|The lower helmet boundary meets the suit's neck assembly rather than a simple open shirt collar.|S17|supported_relation|ccx_cc13_01,ccx_cc13_02|청색 NASA 훈련복이라는 이유로 압력복 헬멧을 추가하거나 보호 성능을 픽셀로 입증
U26|court|스위스 갈라복의 세 배색이 한 외피의 분할 면에 놓임|the selected colored garment sections|belong_to|the same gala garment|Red, yellow and blue areas remain assigned to the selected garment sections.|Their borders follow one wearer's garment rather than a background flag.|S19|needs_primary_verification||배경의 삼색만으로 갈라복을 충족하거나 모든 소매 재단을 추정
U27|court|흉갑이 직물 갈라복과 목 러프 바깥에 겹침|the ceremonial breastplate|layered_over|the cloth uniform below its ruff|The metal breastplate has an independent outer edge over cloth.|A separate ruff encircles the neck above that breastplate.|S19|supported_relation|clothing_ct043_v1,ccx_cc13_02|러프와 흉갑을 갈라복 모든 근무 버전에 강제
U28|court|군악 역할의 황흑 배색을 갈라 삼색과 구분|the yellow-and-black garment areas|belong_to|the selected drummer variant|The selected garment carries a yellow-and-black scheme.|The ordinary red-yellow-blue gala scheme is not mixed into that same selected variant.|S20|supported_relation||고수의 배색을 근위대 전원의 기본복으로 사용
U29|court|긴 뒤자락 코트 안에 독립된 조끼 앞섶이 남음|the waistcoat front|visible_inside|the open short-front long-back coat|The outer coat has a distinct short front and longer rear tails.|A separate waistcoat front remains inside its lapels.|S35,S58|reuse_existing|ccx_cc02_01,ccx_cc02_02,costume_ccx_cc02_02|영국·네덜란드의 다른 의례·시대를 모두 같은 색의 연미복으로 병합
U30|court|무릎바지 끝의 여밈과 아래 스타킹이 분리됨|the knee-breeches hem|meets|the separate stocking below it|The trouser ends stop near the knee with their own closure edge.|Separate stockings continue beneath that edge.|S35|needs_primary_verification||현대 긴 바지로 대체하거나 특정 궁정의 노란 바지를 미확인 상태로 확정
U31|police|튜닉과 헬멧의 시대 조합을 초기 톱햇과 분리|the domed helmet|worn_with|the selected later tunic|The headwear has a domed helmet outline rather than a tall flat-topped hat.|The outer garment is a tunic rather than the earlier tailcoat.|S22|supported_relation||1829 초기 코트에 후대 헬멧을 시간 구분 없이 결합
U32|police|레드서지 상의 아래 바지 바깥선의 노란 줄|the yellow trouser stripe|runs_along|the outside seam below the red coat|The red coat remains a distinct upper garment.|A yellow stripe follows the outer trouser leg on the same wearer.|S23|supported_relation||모든 캐나다 경찰 일상복에 적색 상의·스테트슨을 강제
U33|police|보호조끼 외곽이 셔츠 몸판과 팔을 남김|the protective vest|layered_over|the shirt torso|The vest has a separate torso outline and armholes.|The shirt sleeves remain visible outside those vest armholes.|S22|needs_primary_verification||짙은 셔츠만으로 조끼를 충족하거나 실제 방탄 성능을 추론
U34|fire|재킷에 부착된 반사 띠와 바탕 직물의 경계|the reflective bands|attached_to|the turnout jacket panels|The selected bands have bounded sewn placement on the jacket.|Their optical response differs from the surrounding cloth when lighting makes it observable.|S25|reuse_existing|clothing_ct028_v1|노란 도색을 무조건 반사체로 판정하거나 특정 제품 배색을 모든 소방복에 확대
U35|fire|소방서 근무복과 방화 외피를 별도 선택으로 다룸|the selected turnout outer garment|layered_over|the station garment when requested|The protective outer layer has an independent enclosing edge.|Any visible station garment remains beneath it rather than replacing that outer layer.|S25|needs_primary_verification||소방관이라는 직업만으로 방화복·공기호흡기·진압 동작 추가
U36|prison|가로 줄무늬가 상하 의복 면에 귀속됨|the alternating stripe bands|distributed_across|the selected prison-costume garment|Stripe boundaries run across actual garment panels.|The selected palette and stripe direction remain consistent for that version.|S26|design_only||줄무늬가 모든 실제 교정복의 규칙이거나 그 옷이 유죄를 뜻한다고 추론
U37|prison|일체형 복장의 상체 여밈이 바지 부분으로 이어짐|the coverall upper body|continues_into|the trouser section of the same garment|A continuous garment body crosses the waist.|A separate front closure belongs to that body rather than an independent jacket.|S27|supported_relation||드라마 소품의 주황색을 실제 전 세계 수용복 규정으로 일반화
U38|prison|단색 교정복 상의 밑단과 별도 하의 허리|the plain sweatshirt hem|separate_from|the trouser waistband|The upper garment has its own ending hem.|Separate trousers begin beneath it in the selected plain palette.|S26|supported_relation||주황 일체형·흑백 줄무늬만 교정복 후보로 허용
U39|medical|간호 원피스 바깥 앞치마와 별도 깃·커프스|the apron panel|layered_over|the nurse-dress body|The apron has its own edge over the underlying dress.|The dress collar or cuffs remain separate garment details.|S28|reuse_existing|ccx_cc01_01,ccx_cc01_02,ccx_cc01_03|박물관 합성 전시복을 한 벌의 원본으로 선언하거나 모자를 모든 간호복에 강제
U40|medical|스크럽 상의와 바지의 별도 허리 경계|the scrub top hem|separate_from|the scrub trouser waist|A loose top ends at its own hem.|The trousers remain an independent lower garment rather than a white fitted dress.|S29|supported_relation||간호사라는 역할만으로 치료·환자·차트를 추가
U41|medical|열린 백의가 안쪽 일상복을 둘러쌈|the lab-coat opening|reveals|the independent inner garment|The coat front has two separate edges around the torso.|An inner garment remains visible between them without being recolored into the coat.|S30|design_only||흰 긴 코트만으로 의사·연구자 신분이나 장갑을 추론
U42|medical|후드와 직물 커버올 몸체의 연결 경계|the fabric hood|connected_to|the selected coverall neck|The hood is fabric continuous with or attached at the coverall neck.|Its face opening remains a distinct edge rather than an enclosing rigid helmet.|S30|supported_relation||후드만으로 기밀 밀봉·생물학적 보호 성능이 검증됐다고 판정
U43|medical|수술모와 마스크가 각각 머리와 얼굴에 귀속됨|the surgical mask|worn_by|the selected wearer below a separate cap|The mask has its own border and support on the face.|A separate cap contains the head hair region and does not merge into the mask.|S29|design_only||눈가리개를 수술 마스크로 대체하거나 모든 의료복에 마스크 강제
U44|airline|의복 앞섶의 단일 단추열과 이중 단추열 분리|the selected button row|attached_to|one garment front configuration|Buttons occupy one selected single-row or double-row configuration.|The overlapping front edge follows that chosen configuration.|S31|supported_relation||JAL의 다른 시대·일반/책임자 앞섶을 한 의복에 혼합
U45|airline|1970 JAL의 앞벨트와 별도 뒤지퍼|the red waist belt|encircles|the dress with a separate rear zipper|A red belt forms an independent waist band over the dress.|The selected closure is on the back rather than an invented front button row.|S31|supported_relation||가슴 금색 단추가 있는 다른 시대 JAL 재킷을 자동 추가
U46|airline|모자 없는 선택 버전에서 머리 위 독립 모자 외피를 배제|the visible head silhouette|remains_separate_from|any unrequested hat shell|The full selected head region is observable.|No independent hat crown or brim is imposed on that region for this selected no-hat variant.|S31|supported_relation||1996 JAL 버전에 이전 시대 보울 모자를 자동 추가하거나 가린 머리를 모자 없음의 증거로 사용
U47|airline|승무원 스카프의 상승한 끝과 별도 머리 장식|the raised scarf end|extends_from|the neck accessory below the separate hair ornament|The scarf originates from the neck and has its own projecting end.|The separate hair ornament belongs to the hair rather than continuing from that scarf.|S32|supported_relation||목 스카프를 머리 장식으로 연결하거나 2019 설명을 2026 현행 규정으로 선언
U48|airline|사롱 위에 겹친 케바야 블라우스|the kebaya blouse|layered_over|the wrapped sarong|The upper blouse has its own lower edge.|A wrapped sarong continues below that edge on the same wearer.|S33|reuse_existing|clothing_ct141_v2|배색만으로 블레이저를 케바야로 판정하거나 모든 SQ 버전에 케로상 세 개를 강제
U49|airline|계급별 색은 선택 의복 면에만 매핑|the selected rank color|belongs_to|the version-specific uniform garment|One chosen garment palette is assigned to its actual cloth panels.|It is not copied onto skin, background or unrelated accessories.|S33|needs_primary_verification||네 색의 존재 확인을 색-직급의 정확한 대응표 확인으로 확대
U50|airline|같은 재킷의 스커트형과 바지형을 대안으로 유지|the selected jacket|worn_with|one selected skirt or trouser alternative|The upper jacket remains the common selected garment.|Exactly the requested lower garment type is present for that wearer.|S32|supported_relation||한 사람에게 스커트와 바지를 두 버전의 필수 조합으로 겹침
U51|service|벨홉의 짧은 재킷과 독립된 모자|the short service jacket|worn_with|the separate pillbox-like cap|The jacket ends at its own selected short hem.|The cap has a bounded crown independent from the jacket collar.|S34|needs_primary_verification||리버리·궁정·호텔의 같은 색 재킷을 모두 벨홉으로 명명
U52|service|앞치마 가슴판·허리띠·치마 패널의 귀속|the apron bib and lower panel|connected_to|their own waist band over the dress|The selected apron bib has its own upper support.|Its lower panel and band remain outside a separately bounded dress.|S59,S62|reuse_existing|ccx_cc01_01,ccx_cc01_02,ccx_cc01_03|허리 앞치마를 가슴판 앞치마의 증거로 쓰거나 앞치마에 실제 가사 역할 강제
U53|service|조리복의 겹친 앞섶과 이중 단추열|the chef-jacket overlapping front|closed_by|two selected button rows|The front panels overlap as one jacket construction.|The button rows are attached to that front rather than a printed pattern.|S36,S37|supported_relation||조리복을 무조건 흰색으로 한정하거나 특정 유물 색을 모든 조리사에 부여
U54|service|버니 머리 장식이 의복 착용자의 머리에 붙음|the artificial ears|attached_to|the headpiece of the leotard wearer|The ear shapes have their own manufactured outlines.|Their base belongs to a headpiece worn by the same garment wearer.|S38,S39|reuse_existing|ccx_cc17_01,ccx_cc17_02|인간을 토끼 종으로 바꾸거나 옷만으로 성적 행위·관계·신체 비율을 부과
U55|service|흰 칼라·커프스가 검은 원피스 몸판에 붙음|the white collar and cuffs|attached_to|the black dress neckline and sleeve ends|The white collar follows the dress neckline with its own edge.|The white cuffs lie at the actual sleeve ends of that same dress.|S59|supported_relation||무릎 길이 실제 사용인복을 무조건 긴 치마·흰 앞치마로 교체
U56|school|입식깃과 중앙 앞섶이 같은 가쿠란 상의를 이룸|the standing collar|connected_to|the central-front jacket closure|The collar rises from the jacket neckline.|The central closure belongs to the same structured jacket body.|S40,S61|needs_primary_verification||상표·학교 확인 없이 모든 가쿠란의 단추 수·금속 색을 확정
U57|school|세일러 선이 칼라 가장자리의 윤곽을 따름|the selected collar lines|follow|the sailor-collar edge|Each line stays within the collar panel near its edge.|The number and spacing follow the chosen school or version rather than a universal count.|S61|supported_relation|clothing_ct041_v2,ccx_cc03_01|선이 배경이나 리본에만 있거나 모든 학교에 세 줄을 강제
U58|school|민소매 점퍼스커트 아래 블라우스 소매가 나옴|the sleeveless jumper dress|layered_over|the separate blouse|The outer dress has its own open armholes.|The inner blouse sleeves emerge from those openings on the same wearer.|S40|needs_primary_verification||소매가 붙은 원피스를 점퍼스커트 겹침으로 판정
U59|school|개조 교복의 상의 길이와 하의 폭을 각각 조절|the modified jacket hem|sits_relative_to|the selected trouser waist|The jacket's hem has a chosen long or short position relative to the waist.|The lower garment keeps its separately chosen wide or ordinary leg outline.|S40|supported_relation||초란과 탄란을 동시에 적용하거나 넓은 바지에서 비행·폭력 성향 추론
U60|academic|가운과 독립된 학위 모자를 같은 착용자에 귀속|the academic headwear|worn_by|the gown wearer|The selected cap has its own crown or top shape above the head.|The gown remains a separate shoulder-supported outer garment on the same wearer.|S41|supported_relation||모든 학위·기관에 사각모·탐모·후드를 동시에 강제
U61|religion|수단의 긴 몸판과 중앙 앞섶|the central front closure|runs_along|the long cassock body|The garment body descends continuously below the waist.|A selected front closure belongs to that body rather than an outer stole.|S43|needs_primary_verification||사제의 교단·계급별 단추 수·색을 확인 없이 고정
U62|religion|수도복 튜닉과 별도 후드·허리끈|the waist cord|encircles|the habit tunic below its separate hood|The tunic has a continuous torso and lower cloth body.|A separate cord gathers its waist while the hood or capuche retains its own edge.|S43,S44|supported_relation||모든 프란치스코회에 갈색·세 매듭을 부과하거나 수련자와 서원자를 합침
U63|religion|수녀 베일과 머리 둘레 흰 층을 분리|the outer veil|layered_over|the selected inner headcloth|The outer veil has its own descending edge.|A separately bounded inner headcloth remains visible where requested.|S44|needs_primary_verification||모든 수도회 수녀복을 흑백 한 형태로 고정하거나 신앙·성격을 추론
U64|religion|직사각 가사의 안쪽 패치와 바깥 테두리|the rectangular inner patchwork|enclosed_by|the outer kesa border|Interior cloth blocks form a bounded rectangular field.|A separate border surrounds that field rather than a random all-over print.|S42|supported_relation||모든 가사에 동일 열 수·색·주름을 부과하거나 입는 방식 없이 신분 확정
U65|religion|흰 상의·붉은 하카마 위 선택된 치하야 겉옷|the selected chihaya outer layer|layered_over|the white upper garment above red hakama|The white upper garment and red lower garment remain separate pieces.|When chihaya is selected, it has its own outer edge above those pieces.|S45|supported_relation||일반 미코복에도 춤용 겉옷을 항상 추가하거나 성인·미성년 나이를 의복으로 판정
U66|fiction_trek|부서색 상의와 검은 하의의 TOS 계열 배치|the selected department-color top|worn_with|the separate dark lower garment|The chosen color belongs to the top body.|The lower garment retains a separate dark region without importing another show's yoke.|S46|supported_relation||Star Trek 모든 판본의 가슴·어깨·깃 색을 한 기본 제복으로 병합
U67|fiction_trek|TNG 초기 일체형과 후기 별도 상하의 경계|the chosen TNG upper body|meets|its version-specific lower construction|The selected early or later construction has one defined waist boundary.|The alternative version's waist treatment is not added to that same garment.|S46|needs_primary_verification||이름만으로 초기·후기 재단을 동시 부과하거나 성별로 바지 종류를 고정
U68|fiction_trek|회색 어깨 요크 아래 검은 몸판과 별도 부서색 목층|the grey shoulder yoke|attached_to|the black body above the separate color neck layer|The selected upper yoke is grey and belongs to the black outer body.|A separate colored neck layer remains visible within the opening.|S46,S48|supported_relation||초기 DS9의 부서색 어깨와 후기의 회색 어깨를 서로 바꿈
U69|fiction_trek|적갈색 앞섶과 별도 사슬·속목층|the selected lapel chain|attached_to|the maroon outer lapel above the inner neck layer|The chain has its own attachment on the selected outer lapel.|The raised undershirt neckline remains an independent inner layer.|S47|supported_relation||허가 복제품의 소재를 원본 촬영복의 정확한 소재로 확정
U70|fiction_trek|Enterprise 작업복 어깨의 얇은 부서색 영역|the narrow department trim|attached_to|the work-style suit shoulder|The suit is one chosen work-style outer garment.|The selected department color stays in a narrow shoulder area rather than recoloring the whole torso.|S46|supported_relation||NASA 비행복에 해당 작품의 표식을 자동 이식
U71|fiction_sw|흰 장갑판 사이 검은 보디글러브 관절층|the armor plates|layered_over|the black body glove at the joints|Armor pieces have separate hard-looking outer edges.|Black cloth remains visible between selected plate edges at the joints.|S49,S50|supported_relation|ccx_cc13_02,ccx_cc13_03,ccx_cc15_01,ccx_cc15_02|흰 로봇 몸체로 바꾸거나 복장만으로 총·전투 동작을 자동 추가
U72|fiction_sw|스노트루퍼 후드·벨트 아래 케이프가 별도 층임|the hood and belt-supported cape|layered_over|the selected insulated suit|A separate hood surrounds the head region.|A cape edge continues below its belt support rather than becoming rear armor plates.|S51|supported_relation||일반 스톰트루퍼·스카우트·퍼스트 오더에 같은 후드와 케이프를 부과
U73|fiction_sw|선택 헬멧의 눈·입·하단 면을 판본별로 유지|the selected helmet face planes|belong_to|one edition-specific helmet shell|Eye and mouth openings occupy the selected helmet face.|Their connecting planes and lower outline remain one chosen edition.|S49,S50|needs_primary_verification|ccx_cc13_01|Phase I·II·제국·퍼스트 오더의 얼굴 면을 기억만으로 혼합
U74|fiction_nier|2B 눈가리개와 독립된 높은 깃·가슴 개구부|the eye covering|worn_by|the selected 2B-version wearer above the garment opening|The eye covering has a visible edge across the eye region.|The high garment neckline and selected chest opening remain separate below it.|S52,S53|observed_crop_only|ccx_cc28_02|관찰하지 않은 치마 밑단·부츠까지 검증했다고 하거나 게임·애니 판본을 합침
U75|fiction_hp|퀴디치 로브와 훈련복·경기 보호대의 판본 분리|the selected sports outer garment|worn_with|its requested training or match equipment|One chosen robe or tracksuit construction is visible.|Protective pads or a helmet appear only for the selected match configuration.|S54|supported_relation||혼혈 왕자의 훈련복에 경기용 보호대를 항상 얹거나 초기 두 영화의 무거운 로브를 유지
U76|fiction_hp|보바통의 푸른 의복과 독립된 뾰족 모자|the pointed blue hat|worn_by|the selected blue-costume wearer|The hat has its own pointed crown above the head.|The selected blue garment remains a separate cloth body beneath it.|S54|supported_relation||다른 마법학교의 검은 로브를 보바통의 대표 의복으로 대체
U77|fiction_handmaid|흰 날개형 머리 가리개와 적색 외피의 분리|the white winged head covering|worn_with|the selected red outer garment|The head covering has independent lateral projecting edges.|The red outer garment belongs to the same wearer below that covering.|S55|needs_primary_verification||적색만으로 시녀 신분·갈색 이모복·청록 아내복을 혼합하거나 신체 통제를 자동 장면화
U78|transformation|장교 모티프 외피와 코르셋 구조선의 소유 분리|the corset channels|belong_to|the corset beneath optional jacket motifs|Vertical channels continue within the corset's own outline.|Any selected braid or shoulder motif attaches to a separate outer garment or its declared carrier.|S04|reuse_existing|ccx_cc26_01,ccx_cc26_02,ccx_cc05_01,ccx_cc05_02|직업 이름에서 실제 군 계급·무기·신체 비율을 추론
U79|transformation|무대 의복의 선택된 짧은 밑단과 바디수트 경계|the selected short hem or leg opening|belongs_to|the stage garment|The chosen ending edge belongs to the garment itself.|The visible leg region remains the wearer anatomy rather than added cloth panels.|S59|design_only||미니·성인 무대복을 실제 간호·경찰 규정으로 선언하거나 신체 크기를 임의 변경
U80|transformation|광택 하이라이트가 제복 표면의 주름을 따름|the specular highlight|follows|the selected garment surface|The highlight lies on the garment's curved or folded surface.|Its path changes with those visible folds rather than emitting light at every seam.|S38|design_only||광택만으로 라텍스·가죽·내구성·성적 취향을 확정
U81|transformation|헤짐과 수선 패치의 위치를 같은 의복에 묶음|the repair patch and frayed edge|belong_to|the selected garment region|The patch has its own sewn boundary on the chosen panel.|Fraying stays localized to the requested edge and does not become body injury.|S10|reuse_existing|ccx_cc32_01,ccx_cc32_02|오래된 군복에서 사망·부상·피해자·가해자를 자동 추가
U82|transformation|발광 패널 경계와 비발광 직물 관절층 분리|the luminous panel edges|separate_from|the unlit fabric joint gaps|The selected panel border carries a visible light source or glow.|The cloth gaps between panels remain a different unlit material region.|S49|reuse_existing|ccx_cc35_01,ccx_cc35_02,ccx_cc13_03|SF 제복이라는 이름만으로 전신 네온·로봇 종·보안 임무를 자동 추가
U83|transformation|명시적으로 든 소품과 종교 의복의 소유 분리|the explicitly requested handheld prop|held_by|the selected garment wearer|The requested prop has a separate handle and outer silhouette.|The same wearer's hand visibly grips it without changing the garment into a weapon.|S43|reuse_existing|ccx_cc36_01,ccx_cc36_02|수도복만으로 무기·전투·폭력을 추가하거나 의복을 곧바로 실제 신앙으로 판정
"""

SCOPES = {
    "supported_relation": "출처가 지지하는 범위의 관계 초안. 기관·연대의 전체 복장 검증이나 런타임 검증은 아니다.",
    "reuse_existing": "동등한 기존 관계를 우선 재사용한다. 명명된 역사·작품 버전의 사실성은 별도 확인한다.",
    "needs_primary_verification": "형태 가설과 검증 대상을 제안한다. 기관·시대·판본 프로필의 확정 근거로 사용하지 않는다.",
    "design_only": "요청에 따라 선택할 수 있는 시각적 변형 설계다. 역사·규정·직업의 사실 주장으로 승격하지 않는다.",
    "observed_crop_only": "공식 화면에서 관찰한 크롭의 요소만 지지한다. 화면 밖 구조와 다른 매체 판본은 미확인이다.",
}

def write_json(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")

def atom_rows():
    rows = []
    for line in ATOM_ROWS.strip().splitlines():
        aid, family, ko, subject, predicate, obj, c1, c2, sources, status, reuse, confusion = line.split("|")
        slot = "wearable_accessory" if aid in {"U07", "U11", "U12", "U14", "U24", "U43", "U54", "U60", "U73", "U76", "U77"} else "garment_detail"
        if aid in {"U18", "U80"}: slot = "surface_material"
        if aid == "U83": slot = "prop"
        en = f"{subject} {predicate.replace('_', ' ')} {obj}"
        region = "prop" if slot == "prop" else "wardrobe"
        components = []
        for i, phrase in enumerate((c1, c2), 1):
            components.append({
                "id": f"{aid}_c{i}", "owner": OWNER, "carrier": subject if i == 1 else obj,
                "observable_evidence": phrase,
                "prompt_evidence_field_proposal": f"uniform_{aid.lower()}_component_{i}_phrase",
                "native_gate_proposal": {"id": f"uniform_{aid.lower()}_native_{i}", "review_scale": "native",
                    "pass_condition": phrase + " The carrier must belong to the declared wearer.",
                    "fail_condition_ko": confusion,
                    "occluded": "UNOBSERVABLE", "partial_is_fail": True},
            })
        rows.append({
            "id": aid, "family": family, "label_ko": ko, "relation_en": en,
            "proposal_status": status, "status_scope_ko": SCOPES[status],
            "owner_scope": OWNER,
            "relations_proposal": [{"id": f"{aid}_owner", "type": "declared_owner_scope", "subject": subject, "object": OWNER},
                {"id": f"{aid}_assertion", "type": predicate, "subject": subject, "object": obj}],
            "components": components, "source_ids": sources.split(","),
            "source_binding_ko": "출처 연결은 조사 근거 또는 반례의 위치다. 두 영문 증거 문장은 연구자의 형태 추상화이며 원문 인용·완제품 규격이 아니다.",
            "reuse_existing_ids": reuse.split(",") if reuse else [],
            "confusion_boundaries_ko": [confusion, "복장 선택은 직업 동작·연령·신체·동기·신념·소품 추가를 자동 허용하지 않는다."],
            "candidate_slot_proposal": slot, "affected_dimensions_proposal": ["appearance"],
            "affected_properties_research": [{"dimension": "appearance", "target": "request_supported_owner",
                "property": f"{region}.{subject.replace(' ', '_')}.{predicate}", "runtime_key_status": "unvalidated_mapping"}],
            "activation_plan": {"candidate_only_until_selected": True,
                "exact_relation_terms_proposal": [ko, en], "bare_role_alias_hard_activation": False,
                "approximate_discovery": "advisory_only", "named_version_requires_independent_verification": True},
            "claim_limits_ko": ["원자료에서 확인하지 않은 구조·재질·계급·연대·성능은 보충 추론하지 않는다.",
                "속성 경로와 관계 type은 현행 검증기를 거쳐 매핑해야 하며 이 연구 키를 그대로 배포하지 않는다."],
        })
    return rows

# Every reference row gets a traceable assessment and an implementation target.
# start-end | proposed atoms | sources | reviewed delta or unresolved claim
CATALOGUE_ROWS = r"""
1-3|U01|S03|흥완군 유물의 배색은 확인했으나 18~20세기 연대별 색 변화 전체는 확인하지 못했다. 연도 alias는 보류하고 실제 소매 경계만 후보화한다.
4|U01,U02|S02,S03|민소매 덧옷과 안쪽 소매의 소유를 분리한다. 원 대화의 짙은 자색 등 모든 배색은 유물 단위로 더 확인한다.
5-6|U03,U04|S01|허리 접합·주름을 핵심으로 둔다. 계급·역할별 색과 탈착 소매는 해당 버전에서만 선택한다.
7|U03|S01|황색 군악 역할이라는 대응은 이번 근거로 확정하지 못했다. 철릭 구조와 황색 선택을 분리한다.
8|U05|S04|기존 가슴 브레이드 관계를 우선 재사용한다. 돌만의 정확한 줄 수·매듭·연대는 개별 유물의 추가 확인 대상이다.
9|U05,U06|S04|어깨에 걸친 별도 모피 테두리 코트는 지지된다. 확인한 박물관 사례는 c1848이며 원 대화의 c1820과 동일하지 않다.
10|U05,U06|S04|펠리스의 구조와 영국 의용기병의 적색·은색 배색을 분리한다. 후자의 연대·소속 유물은 미확인이다.
11|U09,U10|S06|1863~66 Keystone Zouaves 유물은 가짜 조끼가 붙은 재킷이다. 독립된 조끼를 공통 필수로 두지 않는다.
12|U11|S60|적색 튜닉·베어스킨은 공식 근거가 있다. 단추 묶음·깃털은 연대별이며 Scots Guards의 예를 전원에 확대하지 않는다.
13|U12|S05|킬트·스포런·연대별 상의에 대한 직접 유물 확인이 남았다. 창기병 자료는 스포런의 확인 근거가 아니다.
14|U07,U08|S05|차프카의 각진 윗판은 확인했다. 플라스트론·바지 줄의 정확한 색은 해당 연대 사례를 추가 확인한다.
15|U13|S07|1940 블라우스의 소재·소매 표식은 유물 근거가 있다. 짧은 상의와 하의 접합은 전체 착장 확인 후 확정한다.
16|U14|S08|검은 외피와 표식 부착을 분리한다. 역사복 명시 요청은 중립적으로 모델링하되 검정 패션만으로 조직을 추론하지 않는다. 정확한 1932 도입 주장은 추가 확인한다.
17|U14|S09|야전 회색·깃/어깨 표식을 유물별로 기록한다. 검색 본문은 읽었지만 상세 페이지 열기는 실패했다.
18|U18,U81|S10|M42 양면 계절 무늬와 앞끈·허리·손목·위장 부착띠를 구분한다. 모든 SS 스모크의 공통 무늬로 일반화하지 않는다.
19|U15|S11|AGSU의 부품별 배색을 보존한다. 의복 설명과 2026 착용 규정 준수는 다른 검증이다.
20|U16|S12|청색 외피·흰 셔츠를 분리한다. 금색 하의 브레이드는 계급에 조건화한다.
21|U17,U18|S13|ACU 재단과 OCP 무늬를 독립 축으로 둔다. 난연성·보호 능력은 정지 이미지로 확인하지 않는다.
22|U19,U21|S14|1817 하계복 기록을 출발점으로 삼되 셔츠·바지·모자 세부의 유물/도판 확인이 더 필요하다.
23|U19|S56|1859 흰 덧깃·커프스 제거 기록은 이전 대비를 지지한다. 1841 전체 프록 구조·재단은 별도 확인한다.
24|U19,U20|S56|흰 덧깃·커프스가 사라진 청색 프록으로 비교한다. 후대 파이핑까지 없다고 확장하지 않는다.
25|U19,U57|S56|1866의 파이핑 줄 수는 당시 역할과 연결된다. 세 줄을 모든 시대 수병과 학교 교복의 공통 규칙으로 만들지 않는다.
26|U17|S14|데님 작업복의 정확한 초기 연도·주머니·상의 구성은 추가 확인이 필요하다. 사병 정복과 작업복을 별도 버전으로 남긴다.
27|U22|S57|노퍽 코트·벨트·긴 스커트 규정과 실제 착용을 구분한다. 변개 No.15는 1917 또는 1918의 날짜 불확실성을 보존한다.
28|U16|S14,S56|1973 재킷·넥타이 개편의 본문을 이번 반환 자료에서 충분히 확보하지 못했다. 해당 이름의 hard activation은 보류한다.
29|U23|S15|K-2B의 회녹색 직물 일체형·지퍼 주머니 사례를 확인했다. 모든 녹색 비행복의 주머니 수로 고정하지 않는다.
30|U23|S15|일체형 구조와 사막색 팔레트를 분리한다. 사막색의 모델·시대·포켓 배치는 추가 확인한다.
31|U23,U25|S16,S17|청색 훈련복과 청색 압력복은 헬멧·목 연결 구조가 다르다. 색상만으로 후보를 합치지 않는다.
32|U23,U24|S18|초기 가죽 비행사복의 헬멧·고글·재킷은 별도 소장 유물이 필요하다. 후대 민항 모자 자료를 직접 근거로 사용하지 않는다.
33|U16,U24|S18|민항의 해군풍 계열은 확인되지만 확인 유물은 Northwest 모자다. Pan Am 흰 모자·정확한 계급 줄 수는 보류한다.
34|U24|S18|셔츠 견장·윙 배지·항공사 계급 줄 수를 별도 후보로 둔다. 견장의 수만으로 모든 항공사의 직급을 역추론하지 않는다.
35|U26|S19|삼색 갈라복은 공식 자료에 있다. 색 경계가 어떤 재단 면에 놓이는지는 전·후면 도판을 더 확인한다.
36|U26,U27|S19|갑옷·러프·모리온을 의례별 추가 요소로 둔다. 모든 갈라복에 갑옷을 강제하지 않는다.
37|U26|S19|청색 훈련복을 삼색 갈라복과 별도 선택으로 유지한다. 야간 근무 전체 규정은 추가 확인한다.
38|U28|S20|군악 고수의 황흑과 장교 적색 벨벳을 일반 삼색과 구분한다.
39|U29|S21|2025년 대표복 도입 자체는 확인했다. 검은 더블 앞섶·소매·장식의 전체 형상은 공식 이미지 검증이 남았다.
40|U29,U30|S35|합스부르크 풋맨/마부 사례를 구조 비교에 사용한다. 18세기 전체 유럽 가사직의 공통 규격으로 확대하지 않는다.
41|U29,U30|S34,S58|왕실 리버리는 역할·행사별로 다르다. 1887 도판은 수채 채색 사진이며 현대 대례 배색 전체는 별도 확인한다.
42|U29|S34,S58|준의례라는 용도와 적색 코트·검은 바지의 정확한 조합을 나눈다. 해당 전체 조합의 1차 자료 확인은 남았다.
43|U29|S34|일상 검정 코트·적색 조끼의 구체 조합은 이번 본문만으로 확정하지 못했다. 연미복의 층 관계만 재사용한다.
44|U29,U30|S34|네덜란드 청·적·황 배색의 직접 궁정 자료를 찾지 못했다. 영국·오스트리아 근거를 대신 적용하지 않는다.
45|U31|S22|초기 톱햇·테일코트와 1863 이후 헬멧·튜닉의 교체를 구분한다.
46|U31|S22|헬멧·튜닉의 시대 조합을 유지한다. 런던의 변천을 다른 나라 경찰 전체의 순서로 확대하지 않는다.
47|U33|S22|셔츠 위 조끼의 구조 가설은 제안하되 최신 Met 모델의 실제 전·후면 근거 확보가 필요하다.
48|U32|S23|레드서지와 바지 노란 줄을 확인했다. 모자·부츠는 역사 변화를 보존하고 일상 근무복과 합치지 않는다.
49|U33|S24|2026년 4월 30일 개편 기사 메타데이터만 확인했다. 원문 리다이렉트로 형상·현행 지급을 확인하지 못했으므로 네이비 디자인을 확정하지 않는다.
50|U29|S25|홍콩 소방 의례복의 기관 1차 자료는 남았다. 미국 제품 브로슈어로 홍콩 정복을 입증할 수 없다.
51|U35|S25|서내 근무복과 방화복을 분리한다. 특정 소방서의 색·표식·장비는 해당 기관 확인 뒤 추가한다.
52|U34,U35|S25|CDC가 제공한 제조사 자료의 탠색·반사띠는 특정 제품 사례다. 모든 현행 방화복이나 보호 성능의 보증으로 쓰지 않는다.
53|U36|S26|흑백 줄무늬는 요청된 외형의 설계로 남긴다. 실제 교정복이 항상 줄무늬라는 근거는 없으며 회색 분리형 유물이 반례다.
54|U37|S27|확인한 주황 일체형은 Luke Cage 촬영 소품이다. 실제 교정 규정이라고 출처를 바꾸지 않는다.
55|U38|S26|회색 스웨트셔츠·바지의 실제 소장 사례를 확인해 단색 분리형을 독립 후보로 둔다.
56|U39|S28|앞치마·깃·커프스·모자를 부품별로 나눈다. 박물관도 이 전시 구성을 여러 간호복의 합성이라고 명시한다.
57|U39,U40|S28,S29|흰 원피스와 현대 분리형을 합치지 않는다. c1910 NMHM 구성은 복제품이므로 원본 유물로 기록하지 않는다.
58|U39|S28|후기 개방 목둘레의 정확한 연도·국가·목 형태는 추가 확인한다. 일반 간호 역할에서 그 형상을 강제하지 않는다.
59|U40|S29|튜닉+바지와 스크럽 구조를 비교하되 기관별 튜닉 여밈·색 구분은 추가 확인한다.
60|U40|S29|현대 스크럽의 상하 분리 관계를 후보화한다. 환자·모니터·활력 징후 동작은 별도 요청이다.
61|U40,U43|S29|수술모·마스크·스크럽은 분리 소유와 개별 선택을 유지한다. 특정 수술실 착용 규정은 추가 확인한다.
62|U40|S29|대학 간호학생의 청색 지정복은 해당 대학 자료가 필요하다. 일반 간호사·성인 모델에게 학생 나이를 부과하지 않는다.
63|U41|S30|백의의 겉/속옷 관계를 설계한다. 보호복 제조사의 커버올 자료는 모든 실험실 백의의 직접 출처가 아니다.
64|U23,U42|S15,S30|직물 일체형·여밈을 재사용하되 보일러수트 모델별 깃·포켓·부착 장화는 별도 확인한다.
65|U42|S30|제조사 모델별 후드·손목·발덮개를 구분한다. 몸을 덮는 외형은 밀봉·방호 능력의 증거가 아니다.
66-68|U44|S31|JAL 공식 변천표와 해당 기간을 연결했다. 그 기간의 여밈·모자·색을 하나의 조합 단위로 보존한다.
69|U45|S31|이 버전은 앞의 적색 벨트와 뒤지퍼를 분리한다. 앞단추 재킷 시대의 특징을 가져오지 않는다.
70|U44|S31|1977 계열은 여섯 금색 단추의 원피스와 바디셔츠를 구분한다. 원피스를 다른 시대의 재킷·스커트 조합으로 바꾸지 않는다.
71|U44|S31|1988 계열의 이중 앞섶과 속블라우스·모자를 보존한다. 버전 사이 단추열 혼합은 실패다.
72|U44,U46|S31|1996 일반·책임자의 코트 차이를 나누고 모자 폐지 정보를 보존한다. 모자 없음 판정은 머리 영역이 보이는 경우에만 가능하다.
73|U44,U47|S32|1991 계열과 2005 도입 계열을 분리한다. 2019 공식 회고를 2026 현행 복제 규정으로 부르지 않는다.
74-75|U47,U50|S32|스커트와 바지는 대안 하의다. 스카프와 머리 장식은 각각 목·머리에 귀속한다.
76-79|U48,U49|S33|사롱 케바야와 네 색의 존재는 확인했다. 이 페이지는 네 색-직급 대응을 모두 설명하지 않아 원 대화의 순서대로 직급표를 확정하지 않는다.
80|U51|S34|벨홉의 실제 호텔별 재킷·모자 자료는 추가 확보 대상이다. 왕실 리버리 자료를 호텔의 실제 규정으로 쓰지 않는다.
81|U52,U55|S59,S62|c1925 실제 사용인복은 무릎 길이·흰 칼라/커프스다. 긴 검정 원피스·흰 앞치마를 모든 실제 사용인복에 강제하지 않는다.
82|U52,U79|S59|프렌치 메이드의 짧은 치마·레이스는 선택된 무대 변형으로 모델링한다. 실제 가사직의 공통 사실로 승격하지 않는다.
83|U53|S36|흰 이중 앞섶 재킷·토크·앞치마 유물의 부품을 구분한다. 조리 동작은 별도 요청이다.
84|U53|S37|붉은 재킷 유물이 흰색만 필수라는 가정을 반박한다. 원 대화의 검정 버전 자체는 추가 제조사/기관 자료가 필요하다.
85|U54,U79|S38,S39|레오타드와 독립 머리 장식을 유물 단위로 분리한다. 카탈로그 소재와 광택의 픽셀 관찰은 다른 증거다.
86|U03,U65|S40|학교 하카마 역사는 확인했지만 미코의 홍백 배색·철릭의 허리 접합을 학교 하카마에 복사하지 않는다.
87|U56|S40,S61|쓰메에리 계열의 존재와 학교별 규칙을 확인했다. 특정 단추 수는 개별 학교/유물로 더 확인한다.
88-89|U19,U57|S40,S61|동·하복의 팔 길이·색은 학교별이다. 공통 칼라 관계를 재사용하면서 원 대화의 한 배색을 전 학교에 고정하지 않는다.
90|U58|S40|점퍼스커트 계열의 존재는 확인했다. 블라우스와 외피 연결은 모델 전·후면 이미지로 확정한다.
91-93|U44,U50|S40|블레이저화·체크·색 변화는 변천표의 추세다. 학교마다 실제 시행 연도가 같다고 해석하지 않는다.
94-96|U59,U79|S40|초란·탄란·본탄·긴 치마는 개조 착용 축으로 보존한다. 의복 변형에서 품행·범죄·폭력 동기를 추론하지 않는다.
97|U60|S41|Oxford는 가운과 사각모 또는 부드러운 모자를 구분한다. 학위·행사·기관에 맞춰 조건화한다.
98|U60|S41|둥근 탐모의 특정 기관/학위 자료는 추가 필요하다. Oxford의 soft cap과 모든 tam을 동의어로 합치지 않는다.
99|U61|S43|가톨릭 수단의 계급별 색·단추·앞섶에 직접 교회/박물관 출처를 더 확보한다. 수도복 자료로 수단 규격을 대신하지 않는다.
100|U62|S43,S44|검정 수도복의 정확한 수도회 버전은 추가 확인한다. 갈색·회색 사례가 있으므로 색 하나로 수도회를 역추론하지 않는다.
101|U62|S43,S44|갈색과 회색 프란치스코회 사례, 수련자/서원자 매듭 차이를 확인한다. 세 매듭은 전원 공통이 아니다.
102|U63|S44|수녀복의 베일·머리층을 제안하지만 흑백의 특정 수도회 원본 도판 확인이 남았다.
103|U64|S42|가사의 테두리와 패치워크를 구분한다. 특정 유물의 패치 열 수를 모든 가사 규칙으로 만들지 않는다.
104-105|U65|S45|기본 홍백과 춤의 치하야 추가를 분리한다. 실제 의례·신앙·나이는 의복만으로 부여하지 않는다.
106|U66|S46|파일럿에서 TOS로의 넥라인·색 변화가 언급되지만 초기 터틀넥의 전체 전·후면 판본 확인은 남았다.
107-108|U66,U79|S46|TOS 계열의 부서색·검은 하의/원피스 대안을 분리한다. 의복 성별 규칙을 모든 요청 대상에게 자동 강제하지 않는다.
109|U66|S46|Motion Picture 중성색 계열은 공식 회고에 있으나 전체 조합·하위 변형의 상세 도판 확인은 남았다.
110|U69|S47|적갈색·사슬·속목층의 근거는 공식 소개된 허가 복제품이다. 원 촬영복 소재 검증과 분리한다.
111-112|U67|S46|TNG 초기/후기 구분을 유지하되 재단의 정확한 허리 경계·전후면 도판을 더 확인한다.
113|U68|S46|초기 DS9/Voyager의 부서색 어깨와 후기 회색 어깨를 대조하는 별도 버전으로 남긴다. 이 항목에 후기 회색 요크를 직접 붙이지 않는다.
114|U68|S46,S48|회색 어깨·검은 몸판·부서색 목층을 따로 귀속한다. 허가 복제품의 선택 조끼를 전원 필수로 만들지 않는다.
115|U70|S46|Enterprise 작업복과 어깨 부서색을 구분한다. 현실 NASA 훈련복과 작품 표식을 합치지 않는다.
116|U66|S46|2009의 미세 델타 질감은 이번 1차 텍스트만으로 재확인하지 못했다. 확대 도판 관찰 후 소재 후보를 추가한다.
117|U44|S46|Into Darkness의 회색 정복은 원 대화 주장으로 남긴다. 공식 제작 자료나 실제 의상 도판 확보 후 판본 프로필을 만든다.
118-119|U71,U73|S49|검은 보디글러브 위 장갑판은 지지된다. Phase I/II의 얼굴 구조·부대 채색은 판본별 확대 도판이 필요하다.
120|U71,U73|S50|흰 장갑 계열을 분해한다. 무기·사격·제국의 행동은 의복만으로 요구하지 않는다.
121|U71,U72|S51|후드·벨트 아래 케이프·절연복을 일반 병사판과 분리한다. 설정상 성능은 시각 관계와 구분한다.
122-123|U71,U73|S50|스카우트·퍼스트 오더의 헬멧과 경장갑 차이는 전·후면 공식 도판 추가 확인이 남았다. 일반 스톰트루퍼 판형을 복제하지 않는다.
124|U74|S52,S53|공식 애니 화면에서 눈가리개·높은 깃·가슴 개구부·상체를 관찰했다. 크롭 밖 치마/부츠와 게임판은 미확인이다.
125-127|U74|S53|9S·사령관·오퍼레이터의 별도 캐릭터 존재는 확인했다. 이들의 전체 의복은 로스터 텍스트로 검증되지 않으며 2B 크롭 관찰을 전이하지 않는다.
128|U76|S54|영화 의상의 푸른색과 모자를 공식 제작 소개에 연결한다. 텍스트만으로 전체 치마 구조를 확정하지 않는다.
129-130|U75|S54|초기 두 영화의 무거운 로브와 후기 가벼운 스포츠 외피를 분리한다. 등에 이름·번호가 있는 후기 요소를 초기판에 복사하지 않는다.
131|U75|S54|훈련 트랙수트와 경기의 팔꿈치·무릎 보호대·헬멧은 서로 다른 선택이다. 모든 훈련복에 경기 보호대를 강제하지 않는다.
132-133|U77|S55|디자이너 인터뷰 색인에서 적색 시녀·청록 아내와 날개·케이프 주제를 확인했다. 영상 시청·전후면 이미지 검증은 남았다.
134|U77|S55|갈색 Aunt의 정확한 앞섶·케이프·모자는 해당 공식 이미지/인터뷰 구간을 추가 확인한다. 색인 존재만으로 전체 의상을 승인하지 않는다.
135|U05,U29|S04,S58|군악대 모티프의 장식 연결을 재사용한다. 무대 디자인의 계급·직업·행진 동작은 별도 선택이다.
136|U05,U78|S04|장식끈/견장과 코르셋의 지지·여밈을 각각 자기 의복에 귀속한다. 특정 실제 군복 규정이라고 명명하지 않는다.
137-138|U79|S59|바디수트·미니는 선택된 무대 의복의 외곽 변화다. 실제 경찰·간호 규정과 연령·신체 비율을 추론하지 않는다.
139|U52,U78|S59|앞치마는 기존 메이드 관계, 코르셋은 기존 구조선을 각각 재사용한다. 한 장식 패널이 두 의복의 증거를 동시에 대신하지 않는다.
140|U19,U57,U79|S56,S61|성인 무대용 세일러 모티프를 독립 변형으로 둔다. 실제 수병·학교 신분이나 모든 군복 부품을 자동 추가하지 않는다.
141|U80|S38|광택의 표면 증거를 설계한다. 유물의 소재 기재를 모든 광택 제복에 확대하지 않는다.
142|U62,U83|S43|종교복과 명시 소품은 다른 선택이다. 무장 요청이 있을 때만 기존 손-소품 관계를 사용한다.
143|U39,U81|S28|간호복의 바탕 구조와 의복 얼룩·헤짐은 분리한다. 호러 이름만으로 신체 손상·피해 서사를 추가하지 않는다.
144|U17,U81|S07,S10|헤짐·수선은 선택한 군복의 특정 면에 제한한다. 시대·부대 표식은 손상과 독립 축이다.
145|U33,U82|S49|보안 제복·발광 패널·직물 관절은 선택된 디자인 관계다. 현실 직업의 실제 장비나 로봇 종으로 바꾸지 않는다.
"""

BUNDLE_ROWS = r"""
UB01|전복과 배색 안쪽 옷|U01,U02|동다리 연대·배색은 유물 확인 뒤 선택
UB02|철릭 허리 접합과 선택 소매|U03,U04|탈착 소매는 확인된 버전에서만 선택
UB03|어깨에 걸친 펠리스와 가슴 브레이드|U05,U06|어깨 걸침과 양팔 착용은 대안
UB04|창기병 모자와 선택 앞판|U07,U08|연대별 앞판 배색 검증이 남음
UB05|주아브 가짜 조끼와 넓은 하의|U09,U10|별도 조끼형과 가짜 조끼형은 대안
UB06|근위 모자와 연대별 상의|U11,U14|표식·단추·깃털은 연대별 선택
UB07|정복 배색과 별도 표식|U15,U16,U14|AGSU와 ASU는 서로 배타적인 대안
UB08|야전 재단과 선택 위장 무늬|U17,U18|재단과 패턴을 독립 선택하고 양면 계절은 대안
UB09|수병 칼라와 시대별 하의|U19,U20,U21|1859 무장식 깃과 후대 파이핑은 대안
UB10|직물 비행복과 헬멧 압력복 비교|U23,U25|일반 훈련복과 압력복은 대안이며 동시 필수 아님
UB11|스위스 갈라 의례 변형|U26,U27,U28|군악 배색과 일반 갈라 배색은 대안; 갑옷은 별도 선택
UB12|궁정 리버리의 코트·조끼·무릎바지|U29,U30|국가·행사·역할별 배색은 확인된 것만 사용
UB13|경찰 외피·조끼·역사 버전|U31,U32,U33|런던 초기/후기, RCMP, 현대 조끼는 대안
UB14|서내 근무복과 방화 외피|U34,U35|보호 장비와 실제 진압 행동은 별도 요청
UB15|교정복 외형의 세 대안|U36,U37,U38|줄무늬·일체형·단색 분리형은 대안
UB16|의료복 원피스·분리형·수술 액세서리|U39,U40,U43|원피스와 스크럽은 대안; 모자/마스크는 선택
UB17|후드 일체형과 열린 백의|U41,U42|백의와 보호 커버올은 대안이며 성능을 주장하지 않음
UB18|JAL 앞섶·벨트·머리wear 시대 비교|U44,U45,U46|시대별 모자와 여밈을 대안으로 보존
UB19|대한항공 스카프·머리 장식·하의 대안|U47,U50|스커트/바지는 한 착용자의 대안
UB20|SQ 케바야 구조와 선택 색|U48,U49|직급별 대응 확인 전 색은 선택 팔레트로만 사용
UB21|사용인 앞치마와 흑백 칼라|U52,U55|실제 유물과 짧은 무대 변형은 대안
UB22|버니의 레오타드·머리 장식|U54,U79|의복과 인공 귀를 분리하고 생물학적 귀로 대체 금지
UB23|교복 칼라·겹침·개조 대안|U19,U56,U57,U58,U59|학교·시대·동하복별 대안이며 연령을 부과하지 않음
UB24|수도복·가사·미코의 별도 계통|U61,U62,U63,U64,U65|종교 계통은 대안이며 모든 요소를 한 착장에 합치지 않음
UB25|Star Trek 판본별 색·요크·목층|U66,U67,U68,U69,U70|시리즈/판본/직무 버전은 배타적 대안
UB26|Star Wars 판본별 장갑·헬멧·후드|U71,U72,U73|부대·임무·판본별 대안이며 무기는 독립 요청
UB27|NieR 캐릭터별 의복 관찰 대기|U74|2B 크롭에서 다른 캐릭터·게임판·전신으로 증거 전이 금지
UB28|마법학교/퀴디치의 판본과 용도|U75,U76|학교 교복·훈련·경기와 초기/후기 영화는 대안
UB29|시녀·아내·Aunt 복장의 계층 대안|U77|인터뷰 영상 및 공식 전후면 이미지 확인 전 보류
UB30|성인 무대·광택·호러·사이버 선택 변형|U78,U79,U80,U81,U82,U83|각 변형은 독립 선택; 성적 행동·신체손상·전투는 자동 추가 금지
"""

def run():
    atoms = atom_rows()
    write_json("relation-proposals.json", {"schema": "uniform-costume-relations-research/v1", "runtime_ready": False,
        "policy_ko": "관계·소유·혼동 경계·렌더 게이트의 연구 초안. 배포 전 중복 확인과 현행 스키마 매핑을 수행한다.",
        "status_counts": dict(Counter(a["proposal_status"] for a in atoms)), "atoms": atoms})
    inventory = json.loads((HERE / "keyword-inventory.json").read_text())
    assessment = {}
    for line in CATALOGUE_ROWS.strip().splitlines():
        ran, aa, ss, note = line.split("|")
        ends = ran.split("-"); start = int(ends[0]); end = int(ends[-1])
        for n in range(start, end + 1):
            if n in assessment: raise ValueError(f"duplicate reference assessment {n}")
            assessment[n] = {"proposed_atom_ids": aa.split(","), "source_ids": ss.split(","), "research_delta_ko": note}
    annotated = []
    for n, row in enumerate(inventory, 1):
        if n not in assessment: raise ValueError(f"missing reference assessment {n}")
        annotated.append({**row, **assessment[n], "verification_scope": "component_or_comparison_only_not_full_ensemble",
            "named_version_hard_activation_ready": False,
            "version_axes_to_preserve": ["country_or_institution", "era_or_release", "duty_or_event", "rank_or_role", "season", "medium_or_edition", "construction_variant"],
            "version_policy_ko": "확인된 축만 채운다. 원 대화 이름·연도는 탐색 키이며 정답인 런타임 별칭으로 자동 승인하지 않는다."})
    write_json("keyword-assessments.json", {"schema": "uniform-costume-keyword-assessments-research/v1", "rows": annotated})
    bundles = []
    for line in BUNDLE_ROWS.strip().splitlines():
        bid, ko, aa, condition = line.split("|")
        bundles.append({"id": bid, "label_ko": ko, "research_atom_pool": aa.split(","),
            "pool_semantics": "research_comparison_pool_not_all_of_bundle", "candidate_only": True,
            "same_frame_owner": OWNER,
            "selection_condition_ko": condition,
            "activation_ko": "지원되는 단일 버전에서 요청된 관계만 선택한다. 풀의 모든 atom을 required_group으로 직렬화하지 않는다.",
            "runtime_bundle_status": "needs_version_split_and_concrete_candidate_id_mapping"})
    write_json("bundle-proposals.json", {"schema": "uniform-costume-bundle-planning-research/v1", "runtime_ready": False, "bundles": bundles})
    source_map = {s["id"]: s for s in json.loads((HERE / "sources.json").read_text())["sources"]}
    lines = ["# 제복 코스튬 145개 키워드 조사 대조표", "", "원 대화의 설명은 검증 대상이다. 이 표의 출처는 해당 행 전체의 승인 표시가 아니며, ‘추가 조사·반영 판단’에 적힌 범위만 지지한다.", "",
        "모든 행의 named-version hard activation은 아직 승인하지 않았다. 부분 구조의 근거 확보와 완전한 착장 검증을 구분한다.", ""]
    last = None
    for row in annotated:
        if row["section"] != last:
            last = row["section"]
            lines += [f"## {last}", "", "| ID | 원 대화 키워드 | 추가 조사·반영 판단 | 관계 초안 | 근거·반례 위치 |", "|---|---|---|---|---|"]
        links = ", ".join(f"[{sid}]({source_map[sid]['url']})" for sid in row["source_ids"])
        note = row["research_delta_ko"].replace("|", "\\|")
        lines.append(f"| {row['id']} | {row['label_ko']} | {note} | {', '.join(row['proposed_atom_ids'])} | {links} |")
    lines += ["", "원 대화의 원래 형태 설명은 [keyword-inventory.json](keyword-inventory.json), 출처의 직접 확인 수준과 한계는 [sources.json](sources.json)에 보존했다.", ""]
    (HERE / "keyword-catalogue.md").write_text("\n".join(lines))
    lines = ["# 시각 관계 보강 초안", "", "83개는 추가 런타임 레코드 수가 아니다. 기존 관계 재사용·근거 있는 관계 초안·검증 대기·선택 디자인을 합친 연구 백로그다.", "",
        "상태·소유·구성 요소·속성 매핑 제안은 [relation-proposals.json](relation-proposals.json), 비교 풀은 [bundle-proposals.json](bundle-proposals.json)에 있다. 속성 경로와 관계 type의 런타임 적합성은 미검증이다.", ""]
    for atom in atoms:
        links = ", ".join(f"[{sid}]({source_map[sid]['url']})" for sid in atom["source_ids"])
        lines += [f"## {atom['id']} — {atom['label_ko']}", "", f"상태: `{atom['proposal_status']}`. {atom['status_scope_ko']}", "",
            f"- 소유: `{OWNER}`; 후보 슬롯 제안: `{atom['candidate_slot_proposal']}`.",
            f"- 방향 관계: `{atom['relation_en']}`.",
            f"- 관찰 1: {atom['components'][0]['observable_evidence']}",
            f"- 관찰 2: {atom['components'][1]['observable_evidence']}",
            f"- 혼동 경계: {atom['confusion_boundaries_ko'][0]}",
            f"- 재사용 우선 ID: {', '.join(atom['reuse_existing_ids']) or '동등 항목 추가 대조 후 결정'}.",
            f"- 근거/반례 탐색 위치: {links}. 원문 인용이나 전체 형상 승인 표시가 아니다.", ""]
    (HERE / "relation-proposals.md").write_text("\n".join(lines))
    print(json.dumps({"assessments": len(annotated), "atoms": len(atoms), "comparison_pools": len(bundles), "statuses": dict(Counter(a['proposal_status'] for a in atoms))}, ensure_ascii=False))

if __name__ == "__main__":
    run()

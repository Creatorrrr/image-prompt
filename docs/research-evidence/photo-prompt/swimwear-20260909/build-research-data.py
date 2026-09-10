"""Build isolated research drafts and a lexical baseline; never writes runtime assets."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ASSETS = ROOT / 'skills/photo-prompt-image-generator/assets'

def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

source_rows = '''
rei|https://www.rei.com/learn/expert-advice/swimsuits.html|REI active swimwear guide|opened|수영 의복 종류·끈·안감·기능 구분|판매자 가이드이며 성능 시험 또는 모든 용어의 표준이 아님
speedo|https://speedo.com.au/explore-swimwear-guides/blog-find-your-fit.html|Speedo women's fit guide|opened|다리선과 등판 디자인을 분리; 상표별 등판 명칭|상표 명칭을 보편적 구조명으로 강제하지 않음
seafolly_tops|https://us.seafolly.com/collections/bikini-tops|Seafolly bikini tops|opened|triangle·longline·underwire·halter bandeau 등의 판매 분류|카탈로그 명칭은 변동 가능하며 사진 픽셀은 미검토
seafolly_bandeau|https://us.seafolly.com/products/lotus-bandeau-halter-bikini-top-j40759-teal|Lotus Bandeau Halter Bikini Top|opened|bandeau와 halter가 결합된 실제 상품명|모든 bandeau에 끈이 있다는 뜻이 아님
seafolly_bottoms|https://au.seafolly.com/collections/bikini-bottoms?page=2|Seafolly bikini bottoms|search_excerpt|high waisted·high cut·hipster·tie side·Brazilian·boyleg 분류|검색 발췌 확인; 개별 제품 뒷면 실측 없음
seafolly_brazilian|https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut|Seafolly Brazilian cut|opened|Brazilian을 cheeky cut으로 설명하며 다양한 허리선과 결합|보편적인 coverage 순서·백분율을 입증하지 않음
ripcurl|https://www.ripcurl.com/pages/womens-wetsuit-guide|Rip Curl women's wetsuit guide|opened|입구 지퍼 방식·길이 변형·neoprene 대체 소재 존재|보온 성능과 화학 조성은 사진으로 증명 불가
ripcurl_jane|https://www.ripcurl.com.au/blogs/products/the-best-wetsuits-for-spring|Rip Curl spring wetsuits|search_excerpt|Long Jane의 긴 다리와 민소매 조합|브랜드별 상품 예시이며 여성 정체성의 시각 판정 아님
blueseventy|https://www.blueseventy.com/blogs/updates/what-is-a-swimskin-and-how-is-it-different-from-a-wetsuit|Blueseventy swimskin explanation|opened|swimskin은 얇은 경기용 레이어; wetsuit과 소재·기능 구분|해당 브랜드 설명; 경기 규칙·속도 개선을 이번 조사에서 검증하지 않음
hunza|https://www.hunzag.com/pages/care-instructions|Hunza G care and Original Crinkle|opened|브랜드 crinkle 소재 명칭과 신축 관련 설명|특정 조직 또는 모든 체형의 핏을 일반화하지 않음
mood|https://blog.moodfabrics.com/naxos-swim-suit-free-sewing-pattern/|Mood Naxos swimsuit sewing pattern|opened|겉감과 self-lining을 함께 봉제하는 수영복 제작 사례|한 패턴이 모든 수영복 구조를 정의하지 않음
mood_tricot|https://www.moodfabrics.com/products/nude-4-way-stretch-swimwear-tricot-306790|Mood swimwear tricot|search_excerpt|swimwear tricot와 four-way stretch의 상품 사용|신축·혼용률을 픽셀에서 추정하지 않음
seamwork|https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring|Seamwork guide to shirring|opened|평행 봉제열의 elastic shirring과 장식 스티치 smocking 구별|무신축 셔링 등 전체 섬유 용어를 포괄하는 표준 아님
fashionpedia|https://arxiv.org/abs/2004.12276|Fashionpedia ontology paper|opened|의복·부품·국소 속성 분리 설계의 근거|수영복 전용 어휘집도 이미지 생성 품질 검증도 아님
met_1920|https://www.metmuseum.org/art/collection/search/91762|The Met bathing suit 1979.124.4|opened|1920년대 미국 wool 수영복 소장품 기록|그 시대 전체의 유일한 형태·소재가 아님; 이미지 미관찰
met_1964|https://www.metmuseum.org/art/collection/search/81814|The Met Rudi Gernreich 1964|opened|1964 monokini의 역사적 의미|현대 cut-out one-piece와 동일어로 병합하지 않음
roxy_monokini|https://www.roxy.com/blogs/expert-guides/swimsuits-for-rectangle-body-shape?page=2|ROXY monokini retail usage|search_excerpt|cut-out sides monokini라는 현대 판매 용례|체형 조언은 데이터에 반영하지 않음
bloch|https://us.blochworld.com/collections/the-bloch-collection/products/mens-tank-unitard-black|BLOCH tank unitard|search_excerpt|민소매와 발목 위까지 이어지는 다리의 unitard 사례|여성용 제품 표준으로 전용하지 않고 sleeve와 leg 독립성만 참고
maritime|https://www.sea.museum/en/society-and-water|Australian National Maritime Museum society and water|search_excerpt|1910s two-piece부터 현대까지 소장품별 연구 경로|소장품 개별 페이지·픽셀 확인 전 시대별 형태 단정 금지
vam|https://www.vam.ac.uk/blog/caring-for-our-collections/the-twelve-days-of-christmas-at-clothworkers-seven-swimming-costumes|V&A seven swimming costumes|search_excerpt_open_403|박물관 수영복 사례 연구의 후속 경로|본문 open 403; 구체적 역사 주장에는 사용하지 않음
cotton|https://www.cottoninc.com/quality-products/textile-resources/textile-encyclopedia/|Cotton Incorporated textile encyclopedia|search_excerpt|텍스타일 용어 후속 확인 경로|개별 rib·terry·seersucker 정의 미열람; 후보의 세부 조직은 설계 가설
'''
sources = []
for line in source_rows.strip().splitlines():
    sid, url, title, access, supports, limits = line.split('|')
    sources.append(dict(id=sid, url=url, title=title, access=access, supports=supports, limits=limits, accessed_at='2026-09-09', pixel_inspected=False))
write('sources.json', sources)

# The following literal visual contracts are original research proposals, not quotations.
# Source IDs support terminology/category boundaries, not every proposed gate.
rows = '''
onepiece|one-piece swimsuit;원피스 수영복;maillot|garment_topology|상체 패널이 몸통을 지나 하의와 한 의복으로 연결됨|드레스 밑단·분리형 상하의·점프수트 바지통으로 대체|front_three_quarter|rei
bikini|bikini;비키니;two-piece swimwear|garment_topology|독립된 수영 상의와 하의의 두 의복 경계|색이 같다는 이유로 일체형 처리|front_three_quarter|rei,seafolly_tops
tankini|tankini;탱키니;blouson tankini;flared tankini|garment_topology|몸통을 덮는 상의의 자유 밑단과 별도 하의|하복부가 가려졌다고 원피스로 단정|hem_detail|rei
swimdress|swim dress;스윔드레스;skirted swimsuit|garment_topology|수영복 본체 위로 이어지는 치마 패널과 독립된 치마 밑단|일반 비치 드레스·별도 sarong과 혼동|hem_detail|rei
legsuit|legsuit;leg suit;레그수트|garment_topology|몸통과 짧은 두 바지통이 연결된 수영 의복|긴소매만 추가하고 다리 구조 누락|front_full|rei
triangle|triangle bikini;트라이앵글 비키니|top_shape|상의 좌우에 구별되는 삼각 패널과 그 꼭짓점 연결|목끈만 있고 삼각 패널은 사라짐|front|seafolly_tops
string| string bikini;스트링 비키니;side-string|strap_width|폭이 좁은 끈의 출발점과 연결 또는 매듭 위치|무조건 삼각 컵·특정 하의 커버리지로 고정|detail|seafolly_tops
bandeau|bandeau;반두;밴듀|top_shape|가로 밴드형 상의 전면을 유지|bandeau를 모든 끈 없음과 동일시|front|seafolly_bandeau
strapless|strapless;스트랩리스|strap_topology|어깨 또는 목으로 올라가는 지지끈 없는 선택형|장식끈과 숨은 끈의 존재를 정면만으로 확정|front_and_back|seafolly_bandeau
halter|halter;홀터넥;halter neck|strap_topology|상의에서 올라오는 끈이 목 뒤로 이어지는 경로|등 중앙 X자 경로로 대체|three_quarter_back|rei,seafolly_bandeau
bralette|bralette bikini;브라렛 비키니|top_shape|선택한 패널 형태와 언더밴드를 먼저 명시|편안함·무와이어를 외관만으로 단정|front|seafolly_tops
balconette|balconette;발코넷;demi-cup;데미컵|top_shape|선택한 낮은 컵 윗선·컵 분할·스트랩 부착점|두 판매 용어를 단일 정확 규격으로 고정|front_detail|seafolly_tops
underwire|underwire;언더와이어;와이어 비키니|internal_structure|외부에 보이는 컵 아래 곡선 채널만 시각 증거로 기록|와이어 실물·지지력을 착용 사진에서 증명|cup_detail|rei
longline|longline bikini;롱라인 비키니|top_length|컵 아래 언더밴드가 아래쪽으로 연장됨|탱키니의 몸통 길이와 자동 동일화|front|seafolly_tops
sporttop|sport bikini top;crop-top bikini;tank bikini|top_shape|선택된 크롭 길이·넓은 어깨끈·전면 패널 구조|스포츠브라와 동일 실루엣만으로 용도 증명|front|rei
scoop|scoop neck;스쿱넥|neckline|전면 윗선이 완만한 U자 곡선을 이룸|등 파임과 같은 필드로 저장|front|speedo
square|square neck;스퀘어넥|neckline|전면 윗선의 수평부와 양쪽 모서리|U자 윗선으로 대체|front|seafolly_tops
sweetheart|sweetheart neckline;스위트하트|neckline|좌우 둥근 윗선이 중앙의 얕은 골에서 만남|단순 깊은 V로 대체|front|seafolly_tops
plunge|plunge;deep V-neck;플런지|neckline|깊이와 종료 지점을 명시한 전면 V 개구부|허리 컷아웃을 대신 추가|front|rei
highneck|high-neck;하이넥|neckline|전면 윗선이 목 기저 가까이 올라옴|긴소매나 등 전체 덮기를 자동 추가|front|speedo
oneshoulder|one-shoulder;원숄더|strap_topology|착용자 기준 한쪽 어깨에만 연결되는 구조|카메라 좌우 반전·가려진 반대 끈|front_and_back|seafolly_tops
offshoulder|off-shoulder;오프숄더|sleeve_attachment|양 어깨 아래 팔 위쪽을 지나는 선택된 소매 또는 밴드|원숄더로 대체|front|seafolly_tops
racerback|racerback;레이서백|back_topology|견갑 사이 중앙으로 모이는 등판 또는 끈 구조|교차만 하는 X자 두 끈으로 대체|back|speedo,rei
crossback|crossback;X-back;크로스백|back_topology|독립된 두 끈이 등을 가로질러 X 교차 후 부착점에 연결|중앙 단일 판으로 합쳐짐|back|speedo,rei
scoopback|scoop back;U-back;low back;로우백|back_opening|등의 U형 경계와 파임 종료 위치를 선택해 표시|앞 네크라인 깊이로 대체|back|speedo
vback|V-back;브이백|back_opening|V가 개구부인지 끈 경로인지 먼저 특정|V 개구부와 V형 끈을 무조건 같은 구조로 처리|back|speedo
laceup|lace-up back;레이스업;corset lacing|closure|두 경계의 여러 연결점을 오가며 조이는 반복 끈 경로|단일 X 끈·장식 bow만 추가|back_detail|speedo
tieback|tie-back;타이백|closure|등의 두 끈 끝이 실제 매듭에서 만남|지퍼·끈 없는 장식 매듭으로 대체|back_detail|speedo
keyhole|keyhole back;키홀;cut-out back|opening|등의 특정 위치에 경계가 닫힌 개구부|등 전체 파임과 동일화|back|speedo
straps|spaghetti straps;wide straps;double straps;adjustable straps|strap_detail|폭·개수·길이조절 슬라이더를 각각 선택 기록|이중 끈을 교차끈으로 변경·슬라이더 위치 유실|detail|rei
highrise|high-waisted;high-rise;하이웨이스트;하이라이즈|waist_height|하의 윗선이 착용자의 허리 부근에 놓임|다리 개구부 높이도 함께 변경|front|seafolly_bottoms,seafolly_brazilian
midlowrise|mid-rise;low-rise;로우라이즈|waist_height|하의 윗선의 위치를 중간 또는 낮은 위치로 명시|커버리지 감소·끈 하의로 자동 치환|front|seafolly_bottoms
highleg|high-leg;high-cut;하이레그;하이컷|leg_opening|다리 개구부 옆 경계가 위로 올라가는 절개|높은 허리선만으로 충족|front_three_quarter|speedo,seafolly_bottoms
boyleg|boyleg;boyshort;보이레그;보이쇼츠|leg_length|짧은 두 바지통의 하단이 허벅지 위쪽을 가로지름|브리프 다리 구멍만 넓게 만듦|front_three_quarter|seafolly_bottoms
coverage|full coverage;classic;moderate;cheeky;Brazilian;thong|rear_coverage|후면 패널 경계의 폭과 위치를 선택한 참조에 상대적으로 명시|판매 명칭의 엄격한 공통 순서·국적·체형 추론|back|seafolly_brazilian
tieside|tie-side bottom;타이사이드|side_closure|좌우 하의 측면 패널 끝이 끈 매듭에서 연결|별도 장식 리본·무조건 low-rise|side_detail|seafolly_bottoms
vfront|V-front;V-cut bottom;브이컷 하의|waist_shape|전면 허리선 중앙이 V로 내려감|다리 절개 high-leg와 동일화|front|seafolly_brazilian
foldover|fold-over waist;접어내린 허리밴드|waist_detail|허리밴드가 겉으로 접혀 두 겹 가장자리 형성|프린트 띠·독립 벨트로 대체|front_detail|seafolly_bottoms
skirtbottom|swim skirt;skirted bottom;스윔스커트|lower_layer|별도 수영 하의에 붙은 치마와 그 밑단|swim dress 전체와 동일시|hem_detail|rei
rashguard|rashguard;rash vest;래시가드;surf shirt|garment_topology|독립 상의의 밑단·소매 길이·선택한 여밈|긴소매만으로 wetsuit을 판정|front_full|rei
surfsuit|surf suit;서프수트;long-sleeve swimsuit|garment_topology|소매와 수영 하의가 몸통에 연결된 일체형 변형|분리형 rashguard·필수 neoprene으로 치환|front_full|ripcurl,rei
wetsuit|wetsuit;웨트수트;fullsuit;steamer|garment_topology|선택된 팔다리 길이·분할 패널·입구 경로·두께감|검은 catsuit·모든 제품의 neoprene 조성 단정|front_and_back|ripcurl
springsuit|springsuit;spring suit;shorty|limb_coverage|소매 길이와 다리 길이를 별개 값으로 지정|모든 springsuit을 반팔 반바지로 고정|front_full|ripcurl
jane|Long Jane;Short Jane|limb_coverage|민소매 몸통과 선택한 긴 또는 짧은 바지통|민소매면 다리도 짧다고 추론|front_full|ripcurl_jane
swimskin|swimskin;swim skin|garment_function|선택된 얇은 경기용 겉레이어의 봉제선·밑단·여밈|wetsuit 또는 dive skin 동의어 병합|front_and_back|blueseventy
leggings|swim tights;swim leggings;수영 레깅스;jammers|leg_length|별도 하의의 허리밴드와 선택된 무릎 또는 발목 길이|두 길이를 동의어 취급·자전거 패드 추가|front_full|rei
boardshorts|boardshorts;보드쇼츠;swim shorts|garment_topology|별도 직선 바지통·선택한 밑위·여밈·밑단|타이트 jammer 또는 일반 속옷으로 치환|front_full|rei
bodysuit|bodysuit;바디수트;leotard;레오타드|adjacent_garment|지정된 의복 용도와 외부 경계를 따로 보존|수영장 배경만으로 수영복 판정|front_and_back|bloch,rei
unitard|unitard;유니타드;catsuit;캣수트|adjacent_garment|몸통과 다리의 연속성·다리 길이·소매를 따로 지정|팔 길이만으로 유니타드 정의·수영 성능 추론|front_full|bloch
wrapcover|sarong;pareo;파레오;사롱;beach wrap|outer_layer|독립 천이 허리를 감싸며 겹침·매듭·자유 밑단을 만듦|수영복에 붙은 치마로 합침·착용자 문화 정체성 추론|front_three_quarter|rei
coverup|kaftan;caftan;beach tunic;kimono cover-up;robe-style cover-up|outer_layer|수영복 바깥 별도 의복의 앞섶·소매·밑단 경계|상업 kimono 명칭만으로 전통 기모노 구조 부여|front_full|rei
beachshirt|beach shirt;linen shirt;cover-up dress;beach pants;palazzo pants|outer_layer|선택한 겉옷의 고유 여밈·밑단·실루엣 보존|수영복 자체 구조로 흡수|front_full|rei
rib|ribbed;골지|surface_topography|규칙적인 평행 돌출 능선과 골의 국소 음영|평면 줄무늬로 대체|macro|hunza,cotton
crinkle|crinkle;크링클;seersucker|surface_topography|선택된 잔요철의 반복 간격과 조직 영역|봉제열 셔링·수평 큰 주름과 혼동|macro|hunza,cotton
terry|terry cloth;테리;타월지|surface_topography|선택된 루프 또는 파일 표면의 세밀한 경계|땀방울·보풀·매끈한 무광면으로 대체|macro|cotton
jacquard|jacquard;자카드|surface_pattern|실 또는 편직 구조와 연동된 무늬의 국소 변화 가설|프린트와 원거리에서 확실히 구분 가능하다고 단정|macro|cotton
crochet|crochet;크로셰;lace overlay|layered_surface|실 고리 무늬의 겉층과 선택한 별도 안감의 경계|무조건 무안감·물에 못 들어가는 옷으로 판정|macro_and_hem|mood
mesh|mesh panel;메시;sheer panel;power mesh|panel_optics|패널 위치·구멍 조직·뒤층·안감 유무를 지정|열린 컷아웃으로 대체·내부 power mesh를 노출 패널화|detail|mood,rei
finish|matte technical;glossy stretch;satin-look;metallic;Lurex|surface_finish|매트 확산·넓은 광택·금속성 반사·점상 반짝임 중 선택|광택 하나로 실크·라텍스·젖음 확정|detail|hunza,mood_tricot
ruched|ruching;루싱;gathering;개더|fabric_manipulation|선택된 솔기나 끈 위치로 모이는 주름 방향과 종료점|원단 전체 crinkle로 대체|detail|seamwork
shirred|shirring;셔링;elastic shirring|fabric_manipulation|여러 평행 봉제열 사이로 잔주름이 모임|보이는 봉제열 없이 crinkle만 추가|detail|seamwork
smocked|smocking;스모킹|fabric_manipulation|선택된 주름과 장식 스티치의 규칙적 연결|기계 elastic shirring과 항상 동일시|macro|seamwork
pleats|pleats;플리츠|fabric_manipulation|방향이 일정한 접힌 주름 능선과 겹침|잡아모은 무작위 잔주름으로 대체|detail|seamwork
ruffle|ruffle;frill;flounce;tiered ruffle|edge_volume|고정 가장자리와 떨어져 물결치는 자유 가장자리|scallop 절개선만으로 충족|detail|seafolly_tops
scallop|scalloped edge;스캘럽;picot trim|edge_shape|반복 둥근 가장자리 또는 작은 고리 장식 중 선택|프릴의 자유 천 층과 혼동|detail|seafolly_tops
piping|contrast piping;binding;contrast trim|edge_construction|솔기 속 돌출 선·가장자리 감싼 띠·단순 대비 띠를 구별|모두 평면 색칠로 구현|macro|mood
cutout|cut-out;컷아웃;waist cut-out|opening|위치가 특정된 열린 공간의 폐쇄 경계와 남은 연결 패널|살색 천·메시 삽입으로 대체|front_three_quarter|roxy_monokini
wrapfront|wrap-front;랩프런트|panel_overlap|앞판이 비스듬히 포개지며 겹침 가장자리가 이어짐|그려진 사선·중앙 꼬임으로 대체|front|seafolly_tops
twist|twist-front;knot-front;트위스트;매듭 앞판|panel_connection|중앙의 실제 꼬임 또는 매듭으로 양쪽 천이 수렴|O-ring 또는 인쇄 무늬로 대체|front_detail|seafolly_tops
ring|O-ring;ring connector;링 연결|hardware|두 천 또는 끈이 같은 링의 서로 다른 쪽에 물리적으로 연결|신체 위에 떠 있는 장신구|detail|seafolly_tops
belt|belted;buckle;벨트;버클|hardware|허리를 지나는 별도 띠와 선택한 버클 연결|프린트 허리띠·몸통 절개선으로 대체|front_detail|seafolly_tops
zip|zip-front;back zip;chest zip;지퍼 수영복|closure|지퍼 이빨선·슬라이더·끝점이 특정한 입구 위치에 있음|앞 세로 지퍼와 가슴 가로 입구 혼동|detail|ripcurl
print|polka dots;gingham;nautical stripes;floral;animal print;checkerboard;ombre;tie-dye;toile|surface_pattern|무늬 요소·규모·간격·방향·색 전이를 독립 기록|무늬만으로 촬영 연도·섬유·민족 추정|front_detail|fashionpedia
wet|wet fabric;water droplets;beaded water;젖은 수영복|surface_state|원단 위 물방울과 젖음 경계를 광택 반사와 별개로 지정|젖음에서 자동 투명화·라텍스화·chlorine 성분 추론|detail|rei
internal|molded cups;soft cups;removable pads;shelf bra;boning;fully lined;double-lined|hidden_metadata|제품 명세 또는 안쪽이 보이는 상품컷에서만 내부 구조 판정|정면 착용샷으로 탈착성·안감 겹수 확인|inside_product_only|rei,mood
performance|UPF;chlorine-resistant;quick-drying;four-way stretch;shape retention;anti-pilling;compression;tummy-control|performance_metadata|명세로 유지하고 필요 시 보이는 패널 구성만 따로 기술|성능 수치·편안함·체형 교정의 픽셀 PASS|not_pixel_scoreable|rei
fibers|nylon;polyamide;polyester;elastane;spandex;Lycra;neoprene|material_metadata|소재 명세와 실제 표면 관찰을 분리|원료에서 광택·안감·신축률·정확 혼용률을 생성|not_pixel_scoreable|mood_tricot,ripcurl
era|bathing costume;1910s;1920s;1930s;1940s;1950s;1960s;1970s;1980s;1990s;Y2K|historical_context|소장품 단위 연대·구조·소재를 함께 선택|시대별 한 가지 룩을 사실로 고정·사진 연대 추정|reference_specific|met_1920,met_1964,maritime
monokini|monokini;모노키니|ambiguous_label|역사적 1964 의미와 현대 연결형 컷아웃 용례를 먼저 구분|현대 상품 요청에 역사적 노출 형태를 자동 도입|context_required|met_1964,roxy_monokini
mood|resort chic;Riviera;pin-up;mermaidcore;scuba-inspired;quiet luxury;coquette;bohemian|optional_style|사용자가 선택한 색·배치·형태 조합의 제안|의복 형태·신체·소득·국적·브랜드를 강제|scene|fashionpedia
accessories|swim cap;goggles;sun hat;sunglasses;body chain;beach tote;towel;surfboard;snorkel;fins|optional_prop|물건별 착용·잡음·놓임 관계와 가림 영역|장신구를 수영복 구조로 흡수·소품만으로 종목 확정|scene|rei
environment|poolside;infinity pool;beach;lagoon;cabana;yacht deck;underwater studio|optional_location|배경의 물 표면·건축·지면 관계를 선택|수영복만으로 해변 강제·배경만으로 의복 종류 판정|scene|rei
'''
matrix=[]
for line in rows.strip().splitlines():
    sid, terms, axis, evidence, confusion, view, src = line.split('|')
    matrix.append(dict(id='sw_'+sid, terms=[t.strip() for t in terms.split(';')], axis=axis,
        proposed_visible_evidence=evidence, confusion_boundary=confusion, required_view=view,
        source_ids=src.split(','), status='proposed_not_runtime_bound',
        evidence_status='source_terminology_plus_authored_visual_hypothesis',
        source_support_scope='Referenced sources support terminology or category boundaries; the literal gate is authored and untested.'))
write('keyword-matrix.json',matrix)
md=['# 수영복 키워드 → 시각 의미 설계표','', '상세 문맥·한계는 research-report.md와 sources.json 참조. 각 행은 구현 전 설계안이며 공식 사전 정의나 검증 완료 프로파일이 아니다.','', '| ID / 관련어 | 독립 축 | 관찰할 관계 | 혼동 경계 | 필요한 시점 |','|---|---|---|---|---|']
for r in matrix: md.append('| '+ ' | '.join([r['id']+' / '+', '.join(r['terms']),r['axis'],r['proposed_visible_evidence'],r['confusion_boundary'],r['required_view']])+' |')
(HERE/'keyword-matrix.md').write_text('\n'.join(md)+'\n')

byid={r['id']:r for r in matrix}
bundle_rows='''
continuous_maillot|연속 몸통 원피스|onepiece,scoop|상체에서 하의로 이어지는 한 의복의 연결을 우선 읽는다
separate_triangle|분리형 삼각 패널 비키니|bikini,triangle,string|상하 분리와 두 삼각 패널을 보존하되 하의 컷은 열어둔다
convertible_bandeau|홀터를 결합한 가로 밴드 상의|bikini,bandeau,halter|가로 밴드 몸체와 목 뒤 끈 경로가 동시에 읽힌다
tankini_hem|탱키니의 독립 밑단|tankini|몸통을 덮어도 자유 밑단이 별도 하의와 구별된다
swimdress_hem|치마가 결합된 수영복|swimdress|본체와 치마의 연결 및 치마 밑단을 구별한다
longline_square|스퀘어넥 롱라인 상의|bikini,longline,square|사각 윗선과 연장된 언더밴드를 동시에 보존한다
highrise_classic|높은 허리선과 독립 다리선|bikini,highrise|허리선만 높이며 다리 절개와 후면 폭은 별도 선택한다
highleg_lowback|하이레그 로우백 원피스|onepiece,highleg,scoopback|다리선과 등 파임을 독립적으로 읽을 수 있는 시점을 선택한다
crossback_training|등 뒤 X자 수영 끈|onepiece,crossback|두 끈의 교차와 네 부착 방향을 추적한다
racerback_training|중앙으로 모이는 등판|onepiece,racerback|중앙 등판 연결이 독립 X끈과 구별된다
boyleg_legsuit|짧은 두 바지통 일체형|legsuit,boyleg|몸통과 두 짧은 바지통의 연속성이 보인다
tieside_vfront|측면 매듭과 V 허리선|bikini,tieside,vfront|측면 실제 연결과 전면 허리선 모양을 구별한다
rashguard_separates|래시가드와 별도 쇼츠|rashguard,boardshorts|상의 밑단과 별도 하의 허리 경계가 유지된다
surf_integrated|긴소매 일체형 서프웨어|surfsuit,zip|소매에서 몸통과 하의까지 이어지며 앞 지퍼가 실제 여밈으로 읽힌다
jane_panels|민소매 긴다리 웨트수트|wetsuit,jane|팔과 다리 길이를 독립 선택하고 패널 연결을 보존한다
swimskin_layer|얇은 경기용 겉레이어|swimskin|겉레이어의 여밈과 밑단을 표현하며 성능은 명세로 남긴다
sarong_layer|수영복 위 독립 랩|onepiece,wrapcover|안쪽 수영복과 바깥 랩의 겹침·매듭·자유 밑단이 구별된다
crochet_lined|안감을 가진 크로셰 표면|bikini,crochet|열린 실 무늬 뒤에 안감이 있는 선택형을 보존한다
ring_cutout|링이 연결하는 컷아웃|onepiece,cutout,ring|열린 공간과 남은 연결부 및 링 부착점이 물리적으로 맞는다
ruched_front|솔기로 모이는 주름|onepiece,ruched|원단 조직과 별개로 지정한 솔기로 주름이 수렴한다
shirred_panel|봉제열 셔링 패널|onepiece,shirred|평행 봉제열과 사이의 잔주름이 같이 보인다
rib_surface|골지 표면|onepiece,rib|평행 능선의 입체성이 프린트 줄무늬와 구별된다
wet_matte|물방울이 있는 매트 수영복|onepiece,wet|국소 물방울과 원단 바탕의 매트 표면을 구분한다
asymmetric_wrap|비대칭 랩 원피스|onepiece,oneshoulder,wrapfront|한 어깨 연결과 앞판의 겹침 경로를 함께 보존한다
'''
bundles=[]
for line in bundle_rows.strip().splitlines():
    sid,title,ids,proposition=line.split('|')
    refs=['sw_'+x for x in ids.split(',')]
    bundles.append(dict(id='sw_bundle_'+sid,title_ko=title,primary_visual_proposition=proposition,
        component_ids=refs, candidate_ids=['sw_candidate_'+x[3:] for x in refs],
        adoption='optional', profile_activation='independent_request_evidence_only',
        affected_dimensions=['appearance'],
        source_ids=sorted({s for x in refs for s in byid[x]['source_ids']}),
        confusion_boundaries=[byid[x]['confusion_boundary'] for x in refs],
        required_views=sorted({byid[x]['required_view'] for x in refs}),
        open_dimensions=['palette','location','lighting','subject_identity','body_shape','expression'],
        establishment='proposed_unrendered', runtime_preset_id=None))
candidate_ids=sorted({c for b in bundles for c in b['candidate_ids']})
candidates=[]
for cid in candidate_ids:
    comp=byid['sw_'+cid.removeprefix('sw_candidate_')]
    candidates.append(dict(id=cid,proposed_slot='wardrobe_style',component_id=comp['id'],
        literal_proposal_ko=comp['proposed_visible_evidence'],owner='selected_swim_garment',
        affected_dimensions=['appearance'],source_ids=comp['source_ids'],
        status='research_only_requires_runtime_schema_translation'))
write('candidate-drafts.json',dict(schema_version='swimwear-research-draft/v1',decision='proposed',
    runtime_compatible=False, candidate_count=len(candidates),bundle_count=len(bundles),
    activation_policy=dict(exact_structural_request='eligible_only_after_context_negation_and_intent_review',broad_swimwear='optional_families',semantic_only='advisory',metadata='not_pixel_scoreable'),
    candidates=candidates,bundles=bundles))

# Read only census over source top-level JSONs, excluding generated indexes.
terms=['swimwear','swimsuit','bikini','tankini','maillot','rashguard','wetsuit','수영복','비키니','래시가드','수영','high-leg','high-waisted']
rx=re.compile('|'.join(re.escape(x) for x in terms),re.I)
coverage=[]
def walk(obj, path=''):
    if isinstance(obj,dict):
        fields={k:obj[k] for k in ('id','ko','en','aliases','activation') if k in obj}
        if fields and rx.search(json.dumps(fields,ensure_ascii=False)):
            yield dict(json_pointer=path,id=obj.get('id'),fields=fields)
        for k,v in obj.items(): yield from walk(v,path+'/'+str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj): yield from walk(v,path+'/'+str(i))
for p in sorted(ASSETS.glob('*.json')):
    if 'index' in p.name: continue
    raw=p.read_bytes()
    coverage.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest(),hits=list(walk(json.loads(raw)))))
write('local-coverage.json',dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
    scope='top-level assets JSON except generated indexes; only id/ko/en/aliases/activation; lexical evidence, not routing or rendered evaluation',terms=terms,files=coverage))

pairs='''
rise_leg|하이웨이스트 비키니, 보통 다리선|로우라이즈 비키니, 하이레그|허리선과 다리선만 각각 변경; 한 축에서 다른 축 추론 금지
bandeau_straps|홀터 끈이 있는 반두 상의|어깨끈 없는 반두 상의|가로 밴드 형태 유지; neck strap만 변경
triangle_string|넓은 스트랩 삼각 비키니|가는 스트랩 삼각 비키니|삼각 패널 유지; 끈 폭만 변경
back_topology|중앙 등판 레이서백|독립 X끈 크로스백|등 뒤 연결 위상 구분
neck_back|얕은 스쿱넥, 낮은 등 파임|깊은 V네크라인, 높은 등판|앞뒤 개구부 소유권 분리
tankini_onepiece|하의를 덮는 긴 탱키니 상의|배 부분 연속 패널 원피스|밑단과 의복 연결을 판정; 피부 노출 유무로 판정 금지
skirt_wrap|치마가 붙은 일체형 수영복|원피스 위 별도 사롱|치마 부착과 독립 매듭·겹침 구분
cutout_mesh|허리의 열린 컷아웃|동일 위치의 메시 삽입|공간과 구멍 조직의 차이
rib_stripe|골지 단색 원단|매끈한 줄무늬 프린트|입체 능선과 평면 무늬 구분
shirring_crinkle|평행 봉제열 셔링|원단 전체 크링클|봉제열 존재와 국소 주름 수렴 구분
wet_gloss|마른 광택 원단|젖은 매트 원단의 물방울|젖음과 바탕 광택 분리; 투명화 금지
zip_entry|앞 중앙 세로 지퍼|가슴 입구 지퍼|지퍼 위치와 경로 보존
rash_surf|긴소매 래시가드와 하의|긴소매 일체형 서프수트|분리 밑단과 일체 연결 구분
jane_spring|민소매 긴다리 웨트수트|긴소매 짧은다리 스프링수트|팔·다리 길이 독립
coverage_rise|같은 뒷면 폭의 하이웨이스트|같은 뒷면 폭의 로우라이즈|뒤 패널 경계를 유지하며 허리선만 변경
layer_lining|안감 있는 크로셰 수영복|동일 겉감의 독립 크로셰 커버업|의복 종류·레이어·안감을 서로 구별
hardware|앞판을 연결하는 링|앞판 위 별도 원형 장신구|두 천 부착점 존재와 장식 분리
metadata|탈착 패드가 있는 수영복 정면|탈착 패드가 없는 동일 외관|정면으로 탈착성 판정 불가; unobservable
negation|하이레그가 아닌 원피스 수영복|하이레그 원피스 수영복|부정어 처리; high-leg substring 강제 활성화 금지
polysemy|비키니 아머 캐릭터|비키니 수영복 상품|갑옷 문맥과 수영복 문맥 혼선 방지
onepiece_word|원피스 드레스|원피스 수영복|기존 드레스 배제 조건 유지
monokini_context|현대 컷아웃 모노키니 상품|1964 Gernreich 소장품 설명|역사·현대 의미 병합 금지
'''
cases=[]
for line in pairs.strip().splitlines():
    cid,a,b,expected=line.split('|')
    cases.append(dict(id='sw_pair_'+cid,a=a,b=b,expected=expected,status='specified_not_executed'))
write('verification-plan.json',dict(decision='proposed',pairs=cases,
    holdouts=['긴소매 레오타드','니트 스카프의 골지','매트한 비옷 위 빗방울','전통 복식 사롱','래시가드 없는 패들보드 장면','밴듀가 아닌 반두 지명 문맥'],
    experiments=['A: independently frozen authorial core with no candidate pack','B: same core plus baseline pack from recorded commit','C: same core plus proposed implemented data'],
    match_conditions=['same request and intent lock','same model version and aspect ratio','same reference handling and attempt budget','freeze prompt bytes per arm','repeated runs if stochastic render improvement is claimed'],
    required_measurements=['retrieved candidate IDs','exposed new IDs','adopted IDs and literal clauses','source intent lock SHA256','request audit','delivery outcome','per-gate pixels','user judgment'],
    success='All requested structural gates and unrelated holdouts pass; new-data contribution requires exposed and adopted IDs with their relations visible.',
    stop='Any axis coupling, unsupported hard activation, missing critical gate or zero exposure/adoption prevents promotion; fix the earliest supported failing stage.',
    pixel_rules=dict(partial_is_fail=True,occluded_requested_gate='not_pass',hidden_performance='not_pixel_scoreable',generation_blocked='unscored',not_requested_back='do_not_force_camera'),
    execution_status='No runtime routing tests or renders performed in this research task'))

assert len({s['id'] for s in sources})==len(sources)
assert len(byid)==len(matrix)
assert all(set(r['source_ids']) <= {s['id'] for s in sources} for r in matrix)
assert all(set(b['candidate_ids']) <= set(candidate_ids) for b in bundles)
assert all(set(b['component_ids']) <= set(byid) for b in bundles)
write('artifact-check.json',dict(status='pass',checks=['unique IDs','source references resolve','candidate and component references resolve','JSON roundtrip'],
    source_count=len(sources),matrix_rows=len(matrix),candidate_count=len(candidates),bundle_count=len(bundles),contrast_pairs=len(cases),
    source_files_scanned=len(coverage),source_files_with_lexical_hits=sum(bool(x['hits']) for x in coverage),
    not_proven=['runtime compatibility','routing behavior','visual source inspection','render improvement','user preference']))
for p in HERE.glob('*.json'): json.loads(p.read_text())
print((HERE/'artifact-check.json').read_text())

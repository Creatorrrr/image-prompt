"""Primary-source supplements found while reviewing the first research draft.

Source support is deliberately narrower than the researcher's proposed nodes,
sentences and framing. No source describes every alias in a card.
"""

def enrich(cards, sources, source, variant):
    source("S48", "Free People scarves and bandanas", "https://www.freepeople.com/scarves/", "fashion_brand", "page_text",
           "브랜드가 큰 사각 스카프를 top/halter로, 작은 천을 headband/머리/가방에 묶는 용례를 설명.",
           "한 장의 스카프 실현 근거이며 모든 bandana 판매 톱의 여밈·실제 원료를 고정하지 않는다.")
    source("S49", "Christopher Esber Bandana Scarf Tie Top", "https://christopheresber.com.au/products/bandana-scarf-tie-top-indigo-bandana-print", "fashion_designer", "page_text",
           "one-shoulder scarf neckline, neck hardware, pointed hem, open back/self-tie의 한 상품 구성.",
           "bandana top이 모두 strapless 삼각형 천이 아님; silk·brass·프린트는 상품별 명세다.")
    source("S50", "Simplicity S3238 vest top and shorts", "https://simplicity.com/simplicity/pds3238", "pattern_maker", "page_text",
           "끈·앞단추·tie detail의 vest top을 tank 위에 또는 단독 착용; shorts에는 앞주름·side pockets·back darts.",
           "vest가 반드시 겉레이어인 것은 아님; 숨은 lining은 외관에서 인증하지 않는다.")
    source("S51", "McCall M8583 bubble-hem skirt", "https://simplicity.com/mccalls/pdm8583", "pattern_maker", "page_text",
           "natural waist에 놓인 lined/flared skirt, bubble gathered hem, 길이 변형과 bias drape 옵션.",
           "bubble 부피·밑단 모임과 길이·허리 높이는 독립; 사진에서 숨은 lining 연결을 자동 추정하지 않는다.")
    source("S52", "Seamwork Sloan sheath dress", "https://www.seamwork.com/pdf-sewing-patterns/sloan-puff-sleeve-dress", "pattern_maker", "page_text",
           "fitted sheath에 darts/tuck, center-front slit, high round neck, bubble sleeves가 조합된 패턴.",
           "sheath의 몸 가까운 재단 근거; 모든 sheath에 동일 소매·슬릿·네크라인을 요구하지 않는다.")
    source("S53", "Melissa adult jelly-shoe collection", "https://www.shopmelissa.com/collections/adult-shoes?page=17", "footwear_manufacturer", "search_snippet_plus_related_page_text",
           "adult jelly-shoe 판매 분류에 Opaque Blue라는 색 명세가 있음; 같은 컬렉션 첫 페이지는 Clear Black도 표시.",
           "page 17 Opaque Blue는 검색 발췌, 첫 페이지는 본문 확인. jelly라는 이름만으로 모든 색의 optical transmission을 고정하지 않는다. 제품 이미지의 광학 검증은 미실시.")
    source("S54", "Rothy's Max Square Ballerina Clover Mesh", "https://rothys.com/products/womens-max-square-ballerina-clover-mesh", "footwear_manufacturer", "page_text",
           "mesh upper와 solid knit toe, V-shaped vamp, 별도 outsole이 한 신발에 공존.",
           "mesh flat이 전 영역 투과를 요구하지 않는다. 재생 원료·착화감·washability는 픽셀 판단이 아니다.")
    source("S55", "Smithsonian NMAfA anklet 99-26-4", "https://africa.si.edu/collection/object/nmafa_99-26-4", "museum", "search_snippet_open_failed",
           "anklet 소장품에 raffia/cowrie shells/glass beads를 별도 재료로 기재.",
           "직접 열기 500 오류; 카탈로그 명칭·재료 발췌만 근거. 이 역사적 물품의 문화 정체성이나 형태를 모든 현대 anklet에 강제하지 않는다.")
    source("S56", "LOEWE baskets and raffia bags", "https://www.loewe.com/usa/en/women/bags/baskets", "fashion_designer", "page_text",
           "basket 가족에 raffia, straw, rattan, iraca palm이 있고 tote/shoulder/crossbody/bucket/hobo 형태가 함께 존재.",
           "basket 구조와 raffia 원료는 동의어가 아니며 제품 가격·생산지·진품을 시각 후보에 전이하지 않는다.")
    source("S57", "Jennifer Zeuner Lala Body Chain", "https://jenniferzeuner.com/products/lala-body-chain", "jewelry_designer", "page_text",
           "목과 허리를 감싼 체인이 가슴에서 연결되는 실제 장신구 상품 구성.",
           "연결 경로만 재사용; 해당 합금·도금·무게·착용자 심리나 복장까지 의무화하지 않는다.")
    source("S58", "Swimsuits For All swimdress with attached shorts", "https://www.swimsuitsforall.com/products/swimdress-with-attached-swim-shorts/1065683.html", "swimwear_brand", "page_text",
           "A-line swimdress와 attached swim shorts를 하나의 제품에 결합.",
           "skirt 외형에서 숨은 shorts를 인증하지 않는다; shaping/anti-chafing 홍보는 픽셀 의미로 옮기지 않는다.")
    source("S59", "Nike Miler brief-lined running shorts", "https://www.nike.com/gb/t/miler-dri-fit-12-5cm-brief-lined-running-shorts-P2UpNPGN/IF2060-382", "sportswear_manufacturer", "page_text",
           "달리기용 여유 있는 하의에 built-in brief, elastic waistband/drawstring, hem vents를 결합한 사례.",
           "숨은 brief·support·흡한 성능은 외관 증거와 분리; 이 상품이 남성용이라고 모든 running shorts의 인물 성별을 고정하지 않는다.")
    source("S60", "Lands' End relaxed rash-guard swim tee", "https://www.landsend.com/products/womens-long-sleeve-relaxed-upf-50-rash-guard/id_246954", "swimwear_brand", "search_snippet_plus_partial_page_text",
           "long-sleeve relaxed rash guard라는 제품명과 swimsuit 위 착용을 설명하는 검색 발췌.",
           "페이지 본문은 제품명·판매 UI만 확인되고 Product Details 탭의 상세 설명은 회수되지 않음. UPF/성능은 명세이며 픽셀 인증이 아니다.")
    source("S61", "Billabong women's swim and board shorts", "https://www.billabong.com/collections/womens-swim-boardshorts", "surfwear_manufacturer", "page_text",
           "swim/board shorts를 함께 분류하고 느슨한 boardshorts·짧은 inseam·boardshort skirt 변형이 공존.",
           "두 판매명을 필수 상호 배타 구조로 만들지 않는다. water use와 quick-dry 설명은 실제 물·젖음·성능의 생성 의무가 아니다.")
    source("S62", "Nike Ace visor", "https://www.nike.com/t/ace-dri-fit-visor-NHd8Qj", "sportswear_manufacturer", "page_text",
           "unstructured visor, 낮은 depth, sweatband, hook-and-loop 뒤 여밈이라는 제품 구성.",
           "visor라는 물품 용례의 근거. 열린 crown의 연결 그래프는 연구자의 관찰 설계이며 제품 이미지를 따로 픽셀 판독하지 않았다. sweat-wicking/재생 원료는 명세다.")
    source("S63", "Seamwork Brom shirt dress", "https://www.seamwork.com/pdf-sewing-patterns/brom-pleated-sleeve-shirt-dress", "pattern_maker", "page_text",
           "stand collar/button-front placket, dart로 맞춘 bodice, A-line skirt, box/knife pleat의 서로 다른 소매 위치.",
           "shirt dress가 항상 loose/straight라는 가정의 반례; 해당 소매 장식까지 모든 shirtdress에 고정하지 않는다.")
    source("S64", "Seamwork Freesia empire-waist bias dress", "https://www.seamwork.com/pdf-sewing-patterns/freesia-empire-waist-bias-dress", "pattern_maker", "page_text",
           "straight-grain bodice와 bias skirt를 나누고 underbust gathers·keyhole·empire waist·body-skimming fit을 결합.",
           "bias cut은 의복 전체의 일률적 grain 방향이 아닐 수 있음; empire가 반드시 전부 loose인 것도 아니다.")
    source("S65", "Seamwork Georgia shift dress", "https://www.seamwork.com/pdf-sewing-patterns/georgia-easy-woven-shift-dress", "pattern_maker", "page_text",
           "plenty of ease인 woven shift와 slight empire waist, short sleeves, no closures가 공존하는 패턴.",
           "shift/empire 판매 분류를 무조건 배타적으로 만들지 않는다; 각 변형의 actual ease/절개 위치를 선택해야 한다.")
    source("S66", "Seamwork Brooklyn half-circle skirt", "https://www.seamwork.com/pdf-sewing-patterns/brooklyn-full-skirt", "pattern_maker", "page_text",
           "half-circle 재단, front box pleat, natural waist, full hem이 같은 패턴에 공존.",
           "퍼진 외형만으로 정확한 원형 재단을 증명하지 않는다; pleated와 circle도 배타 판매명이 아니다.")
    source("S67", "Lacoste polo construction", "https://www.lacoste.com/us/lacoste-polos.html", "clothing_manufacturer", "page_text",
           "칼라·짧은 button placket과 여러 fit/sleeve length, concealed buttons가 함께 있는 polo 군.",
           "두 단추·반소매·악어 로고·원료를 모든 polo의 필수 픽셀 의무로 만들지 않는다.")
    source("S68", "Reyn Spooner Old School Reyn's aloha shirt", "https://www.reynspooner.com/collections/lei-day-favorites/products/old-school-reyns", "clothing_manufacturer", "page_text",
           "큰 monstera 모티프의 aloha shirt에 button-front/pullover/tailored 변형과 print-matched pocket이 존재.",
           "aloha 명칭과 특정 프린트·소매·여밈·원료를 분리; 착용자 문화 정체성과 장소는 의복 라벨에서 추론하지 않는다.")

    by_id = {c["id"]: c for c in cards}
    # Replace weakly related references with direct product/pattern evidence.
    refs = {
        6: ["S48", "S49"], 15: ["S68", "S32"], 16: ["S67", "S07"],
        17: ["S50", "S01"], 57: ["S63", "S05", "S07"],
        58: ["S52", "S65", "S63", "S02"], 59: ["S64", "S65", "S28"],
        63: ["S66", "S02"], 67: ["S51", "S02"],
        69: ["S50", "S30"], 71: ["S59", "S02", "S09"],
        87: ["S60", "S12", "S11"], 88: ["S61", "S30"],
        89: ["S58", "S61"], 114: ["S53", "S54", "S07"],
        115: ["S62", "S11"], 116: ["S56", "S48"], 117: ["S55"],
        118: ["S57", "S35"]
    }
    for num, source_ids in refs.items():
        by_id[f"SF{num:03d}"]["source_ids"] = source_ids
    by_id["SF042"]["source_ids"].append("S64")
    by_id["SF005"]["variants"][0]["relation"]["subject"] = "the halter upper bands"
    by_id["SF066"]["source_ids"] = ["S01", "S51"]
    by_id["SF058"]["confusion_boundary"] += " 실제 shift 패턴에도 slight empire waist가 있어 분류명을 배타적인 구조 계약으로 취급하지 않는다."
    by_id["SF059"]["confusion_boundary"] += " empire waist와 body-skimming fit은 실제 패턴에서 공존한다."
    by_id["SF063"]["confusion_boundary"] += " half-circle 재단과 front box pleat도 동시 성립한다."
    by_id["SF006"]["variants"].append(variant(
        "the one-shoulder scarf panel", "secures_at", "the neck connector of the same top",
        "a scarf panel wraps over one shoulder and secures at a neck connector; its pointed lower hem remains separate from its tied open back"))
    by_id["SF114"]["meaning_ko"] = "성형된 jelly-shoe 갑피와 망눈을 가진 mesh-flat 갑피를 나누고 각 부위의 광학 투과는 독립적으로 기록한다."
    by_id["SF114"]["confusion_boundary"] += " jelly 이름만으로 투과를 의무화하지 않으며 mesh upper와 opaque knit toe도 공존한다."
    by_id["SF114"]["variants"].append(variant(
        "the opaque molded shoe upper", "joins", "the same low shoe sole",
        "an opaque molded upper joins the low sole; its solid panels retain distinct edges around the foot opening"))

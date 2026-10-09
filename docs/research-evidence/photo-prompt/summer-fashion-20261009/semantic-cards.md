# 여름 패션 상세 시각 의미 카드

각 카드는 가족 단위 연구 기록이다. 같은 카드의 variant는 독립 선택형이며 모두 동시에 요구하지 않는다.
출처는 정의/문맥의 근거, 연결 그래프와 영문 관찰 문장은 연구자의 반영 제안이다. runtime-ready 데이터가 아니다.

## SF001 · 베이식 티와 베이비 티

씨앗: 베이식 티셔츠 — Basic T-shirt, 베이비 티 — Baby tee

의미: 베이식은 장식 수준, baby tee는 짧고 비교적 가까운 몸판·소매의 판매 형태다.

소유자: same T-shirt. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: baby는 착용자 나이가 아니며 크롭 길이·배꼽 노출과 필연적으로 결합하지 않는다.

관찰 조건: 상체 앞면에서 소매 끝·몸판 밑단·여유를 함께 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: the T-shirt has short fitted sleeves; its compact body ends at the upper hip
  관계: the T-shirt sleeve hem → ends_near → the upper arm.

## SF002 · 크롭·마이크로 크롭 길이

씨앗: 크롭톱 — Crop top, 마이크로 크롭톱 — Micro-crop top

의미: 일반 상의보다 짧은 밑단의 상대 위치이며 micro는 비표준 강화 표현이다.

소유자: same top hem relative to torso. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 밑단, 하의 윗선, 배꼽 위치는 세 개의 기준선이다; 노출을 자동 추론하지 않는다.

관찰 조건: 상의 밑단과 허리 주변이 가려지지 않는 앞면.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: pfe_midriff_candidate.

출처: [Free People Prairie Field milkmaid top](https://www.freepeople.com/shop/prairie-field-top/), [Vogue Alexander Wang spring 2025](https://www.vogue.com/fashion-shows/spring-2025-ready-to-wear/alexander-wang).

- 독립 변형 1: the cropped top ends above the trouser waistband; a narrow band of abdomen separates the two garment edges
  관계: the top hem → ends_above → the trouser waistband.

- 독립 변형 2: the short top ends at the lower ribcage; a separate high waistband rises close to that hem
  관계: the top hem → ends_at → the lower ribcage.

## SF003 · 탱크·골지 탱크·캐미솔

씨앗: 탱크톱 — Tank top, 리브드 탱크 — Ribbed tank, 캐미솔·캐미 톱 — Camisole / Cami top

의미: 민소매 탱크의 어깨 연결과 가는 끈 캐미솔을 구분하고 rib는 별도 표면 축이다.

소유자: same top shoulder connections. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap` (proposed_family_requires_schema_and_effect_review).

혼동 경계: tank/cami 끈 폭의 판매 경계는 겹친다; 광택·레이스·피부 노출은 별도.

관찰 조건: 어깨 연결부·암홀·원단 골을 각각 식별.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: broad fabric bands join the tank front and back over the shoulders; its armholes have finished edges
  관계: the tank shoulder band → connects → the front and back bodice.

- 독립 변형 2: two narrow straps join the camisole front and back; the light bodice hangs from those straps
  관계: the camisole strap → connects → the front and back upper edges.

## SF004 · 튜브·반도·스트랩리스

씨앗: 튜브톱 — Tube top, 반도·밴도 톱 — Bandeau top

의미: 수평 몸통 밴드와 어깨 연결 없는 구조, 그리고 몸판 길이를 독립적으로 기술한다.

소유자: same strapless top. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 반도 밴드 형태에 탈착 스트랩이 있는 제품도 있어 bandeau=strapless 완전 동의어는 아니다.

관찰 조건: 앞·어깨·옆면, 탈착 연결 고리는 별도 가까운 시점.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_bandeau, y2kr_bandeau.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the strapless top has a horizontal upper edge across the torso; its continuous bodice extends to the waist
  관계: the strapless top upper edge → runs_across → the upper torso.

## SF005 · 홀터·하이넥 홀터

씨앗: 홀터톱 — Halter top, 하이넥 홀터 — High-neck halter, 홀터 드레스 — Halter dress

의미: 목 뒤 연결 경로와 앞쪽 덮는 높이를 분리한다.

소유자: same halter top or dress. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap` (proposed_family_requires_schema_and_effect_review).

혼동 경계: halter는 깊은 V·백리스·삼각컵·짧은 길이의 동의어가 아니다.

관찰 조건: 목 뒤 연결까지 보이는 사선 시점; 앞목 높이는 앞면에서.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct038_v1.

출처: [Burda 5891 halter top](https://simplicity.com/burda-style/bur5891), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the halter front panel rises to the base of the neck; its upper bands join behind the neck
  관계: the halter upper bands → joins_at → the back of the neck.

- 독립 변형 2: two bands rise from the open front neckline; they tie together behind the neck
  관계: the halter straps → join_at → the back of the neck.

## SF006 · 스카프·반다나 톱

씨앗: 스카프 톱·반다나 톱 — Scarf / Bandana top

의미: 평면 천의 겹침·묶음과 삼각형 밑단이 특징인 하나의 실현 방식이다.

소유자: same tied scarf top. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure.front_fastener_state` (existing_candidate_property_family).

혼동 경계: 실제 스카프를 묶은 구조와 완성된 패턴 의복을 분리; paisley는 필수 아님.

관찰 조건: 앞의 삼각 밑단과 실제 묶임 위치를 연결해 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Free People scarves and bandanas](https://www.freepeople.com/scarves/), [Christopher Esber Bandana Scarf Tie Top](https://christopheresber.com.au/products/bandana-scarf-tie-top-indigo-bandana-print).

- 독립 변형 1: a folded scarf wraps around the torso; its lower corner points downward and its side corners meet in a back knot
  관계: the scarf corners → tie_at → the back of the same torso.

- 독립 변형 2: a scarf panel wraps over one shoulder and secures at a neck connector; its pointed lower hem remains separate from its tied open back
  관계: the one-shoulder scarf panel → secures_at → the neck connector of the same top.

## SF007 · 브라톱·브라렛

씨앗: 브라톱 — Bra top, 브라렛 — Bralette

의미: 짧은 상의의 컵·밴드·끈 형태와 부드러운 브라렛을 선택형으로 표현한다.

소유자: same short bust-covering top. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: bra top이 스포츠 기능·와이어·란제리 문맥을 모두 요구하지 않는다.

관찰 조건: 가슴 위 가장자리와 밑가슴 밴드를 볼 수 있어야 한다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you), [Wacoal normal vs push-up bra](https://www.wacoalindia.com/blogs/stories/understanding-the-difference-between-a-normal-bra-and-a-push-up-bra).

- 독립 변형 1: the short top has two fabric cup sections; both join a continuous underbust band
  관계: the short top cups → join → the underbust band.

## SF008 · 랩 여밈과 서플리스 목둘레

씨앗: 랩톱 — Wrap top, 서플리스넥 — Surplice neckline, 랩 드레스 — Wrap dress, 랩 스커트 — Wrap skirt

의미: 사선 앞판 겹침은 네크라인 관계이고 실제 wrap은 여밈 관계까지 필요하다.

소유자: same crossed front bodice. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.front_fastener_state` (existing_candidate_property_family).

혼동 경계: 끈 장식이나 V선만으로 풀리는 랩을 확정하지 않는다. pullover mock-wrap과 side-zipper를 별도 변형으로 유지.

관찰 조건: 겹침의 자유 가장자리와 고정·매듭 양 끝을 확인한다.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct018_v1.

출처: [Seamwork Posie surplice dress](https://www.seamwork.com/pdf-sewing-patterns/posie-surplice-wrap-dress), [Butterick B5764 mock wrap](https://simplicity.com/butterick/pdb5764).

- 독립 변형 1: one dress front panel overlaps the other diagonally; its free edge meets a waist tie
  관계: the outer front panel → overlaps → the inner front panel of the same dress.

- 독립 변형 2: two front bodice panels cross into a V neckline; their lower edges join the same fixed waist seam
  관계: the two front bodice panels → cross_above → the fixed waist seam.

## SF009 · 타이프런트·타이백

씨앗: 타이프런트 톱 — Tie-front top, 타이백 — Tie-back

의미: 묶음이 놓인 방향과 실제로 연결하는 패널을 지정한다.

소유자: same top closure. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.front_fastener_state` (existing_candidate_property_family).

혼동 경계: 앞 매듭이 복부 틈을 반드시 만들지는 않으며 tie-back이 백리스와 같지는 않다.

관찰 조건: 매듭·끈 출발점·양 패널 끝을 한 시점에서 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Burda 5891 halter top](https://simplicity.com/burda-style/bur5891), [Free People Prairie Field milkmaid top](https://www.freepeople.com/shop/prairie-field-top/).

- 독립 변형 1: two front fabric ends meet in a knot; each end remains attached to its own side of the bodice
  관계: the two front fabric ends → join_in → a knot on the same top.

- 독립 변형 2: two back straps meet in a visible knot; their ends connect to the left and right bodice edges
  관계: the two back straps → join_in → a knot across the same back opening.

## SF010 · 밀크메이드·피전트

씨앗: 밀크메이드 톱 — Milkmaid top, 피전트 블라우스 — Peasant blouse

의미: 연상군을 컵 주변 모음·목둘레 모음·소매 볼륨·자수 등 선택 요소로 해체한다.

소유자: same blouse selected construction. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: milkmaid에 퍼프·면·컵·스퀘어넥을 모두 의무화하지 않는다; peasant도 같은 템플릿 아님.

관찰 조건: 선택한 주름 출발점과 소매/몸판의 연결이 보이는 상체.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Burda 6502 peasant blouses](https://simplicity.com/burda-style/bur6502), [Free People Prairie Field milkmaid top](https://www.freepeople.com/shop/prairie-field-top/).

- 독립 변형 1: small gathers shape the blouse bust above a horizontal seam; flutter sleeves extend from the shoulder openings
  관계: the blouse bust gathers → converge_toward → the lower bodice seam.

- 독립 변형 2: fine gathers run around the blouse neckline; the loose bodice hangs below the gathered opening
  관계: the blouse neckline gathers → radiate_into → the loose front bodice.

## SF011 · 스모크 톱·셔링·스모킹

씨앗: 스모크 톱 — Smocked top, 셔링 — Shirring, 스모킹 — Smocking

의미: 평행 봉제 줄의 모음과 주름 위 장식 자수를 구분한다.

소유자: same garment gathered area. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: retail smocked가 실제 탄성 셔링일 수 있다; 늘어남 성능은 정지 사진으로 확정하지 않는다.

관찰 조건: 봉제 줄 또는 장식 자수가 식별되는 근접면.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct064_v1, clt_ct064_v2.

출처: [Seamwork guide to shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring).

- 독립 변형 1: parallel stitched rows gather the blouse waist panel; small folds repeat between the rows
  관계: parallel stitch rows → gather → the same blouse waist panel.

- 독립 변형 2: decorative stitches bridge adjacent gathered folds; the repeated stitching forms a small geometric pattern
  관계: decorative crossing stitches → bridge → the gathered folds of the same panel.

## SF012 · 크로셰·크로셰 톱·커버업

씨앗: 크로셰 톱 — Crochet top, 크로셰 커버업 — Crochet cover-up, 크로셰 — Crochet

의미: 코바늘 고리·모티프와 조직 틈을 표현하되 의복 역할은 별도로 둔다.

소유자: same crocheted garment layer. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.visible_weave` (existing_candidate_property_family).

혼동 경계: crochet는 섬유 종류가 아니며 촘촘한 crochet도 가능; 모든 crochet가 비치지는 않는다.

관찰 조건: 원래 저장 해상도에서 고리·틈을 식별; 아래층도 함께 보이는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seafolly resort cover ups](https://us.seafolly.com/collections/kaftans-cover-ups).

- 독립 변형 1: interlinked yarn loops form the top surface; small openings separate the looped motifs
  관계: the crochet loops → form → the same top surface.

## SF013 · 시어·시어 셔츠·세미시어

씨앗: 시어 셔츠 — Sheer shirt, 시어·시스루 — Sheer / See-through, 세미시어 — Semi-sheer

의미: 연속된 원단을 통한 광학 투과를 의복 안쪽 층에 연결한다.

소유자: same outer fabric and inner layer. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.transmission` (existing_candidate_property_family).

혼동 경계: 같은 색 속옷은 피부와 다르며 시어를 구멍·나체로 대체하지 않는다.

관찰 조건: 외곽 원단 경계, 겹수, 아래층의 연속성이 보이는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

- 독립 변형 1: the sheer shirt remains a continuous outer fabric layer; the opaque camisole is visible through it
  관계: the sheer shirt fabric → transmits_the_outline_of → the opaque camisole underneath.

- 독립 변형 2: the inner garment is visible through a single sheer panel; its outline becomes weaker where two panels overlap
  관계: the overlapping sheer panels → reduce_visibility_of → the inner garment.

## SF014 · 캠프·쿠반칼라

씨앗: 캠프칼라 셔츠 — Camp-collar shirt, 쿠반칼라 셔츠 — Cuban-collar shirt

의미: 목 주변에 평평하게 펼쳐지는 convertible 칼라와 열린 앞선을 기술한다.

소유자: same shirt collar. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 칼라가 tropical print·반소매·특정 국적을 요구하지 않는다.

관찰 조건: 칼라의 접힌 끝과 앞여밈 연결이 보이는 정면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork Negroni camp shirt](https://www.seamwork.com/pdf-sewing-patterns/negroni-vintage-camp-shirt).

- 독립 변형 1: the open collar folds flat against the upper chest; its points sit on either side of the front opening
  관계: the open shirt collar → lies_flat_against → the same upper chest.

## SF015 · 알로하 셔츠·트로피컬 프린트

씨앗: 알로하·하와이안 셔츠 — Aloha / Hawaiian shirt, 트로피컬 프린트 — Tropical print

의미: 열대 식물 등의 무늬 모티프와 셔츠 기본 구조를 분리한다.

소유자: same shirt printed surface. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.pattern` (existing_candidate_property_family).

혼동 경계: 모든 camp collar가 Hawaiian은 아니며 착용자 민족·해변 배경은 필수 아님.

관찰 조건: 큰 잎·꽃의 반복이 원단을 따라 이어지는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Reyn Spooner Old School Reyn's aloha shirt](https://www.reynspooner.com/collections/lei-day-favorites/products/old-school-reyns), [Liberty print collections](https://www.libertylondon.com/uk/features/craft/about-liberty-fabrics-collections.html).

- 독립 변형 1: large tropical leaf motifs repeat across the shirt panels; the print follows the fabric folds
  관계: tropical leaf motifs → repeat_across → the same shirt panels.

## SF016 · 폴로 칼라와 짧은 플래킷

씨앗: 폴로셔츠 — Polo shirt

의미: 접힌 칼라와 목에서 몸판 중간까지만 내려오는 짧은 단추선.

소유자: same polo shirt. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 폴로 경기 장면이나 전체 셔츠형 단추 여밈이 아니다.

관찰 조건: 칼라와 부분 플래킷 끝이 함께 보이는 정면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Lacoste polo construction](https://www.lacoste.com/us/lacoste-polos.html), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: a folded collar surrounds the polo neckline; a short button placket ends within the front bodice
  관계: the button placket → ends_within → the polo front bodice.

## SF017 · 베스트·웨이스트코트 단독 상의

씨앗: 베스트 톱·웨이스트코트 톱 — Waistcoat worn as a top

의미: 앞단추·V선·조끼 몸판을 상의로 읽는 착장 방식.

소유자: same sleeveless vest. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 속에 셔츠가 있어야 하는 의무도, 맨몸 단독 착장의 자동 의무도 없다.

관찰 조건: 소매 없는 연결과 앞여밈, 이너 여부는 실제로 보이는 부분만.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S3238 vest top and shorts](https://simplicity.com/simplicity/pds3238), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: the sleeveless vest fronts meet along a central button row; shaped side panels narrow toward the waist
  관계: the vest front edges → meet_at → the central button row.

## SF018 · 크루넥

씨앗: 크루넥 — Crew neck

의미: 목 아래를 비교적 높게 둥글게 감싸는 선.

소유자: same top neckline. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: high neck나 터틀넥 높이·필수 바디콘과 합치지 않는다.

관찰 조건: 목의 기준점과 원단 윗선이 드러난 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the rounded neckline sits near the base of the neck; the front fabric covers the upper chest
  관계: the rounded top neckline → sits_near → the base of the neck.

## SF019 · 스쿠프·딥 스쿠프

씨앗: 스쿠프넥·유넥 — Scoop / U-neck, 딥 스쿠프넥 — Deep scoop neck

의미: 목 파임의 둥근 곡선과 깊이를 분리하여 기록한다.

소유자: same top neckline. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: U곡선, 넓은 폭, 깊은 파임은 관련 있지만 서로 동일하지 않다.

관찰 조건: 정면, 가장자리의 연속된 곡선과 내려가는 위치.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the neckline forms a broad rounded U; its lowest curve sits below the collarbones
  관계: the scoop neckline → curves_below → the collarbones.

## SF020 · V와 플런징

씨앗: 브이넥 — V-neck, 플런징 네크라인 — Plunging neckline

의미: 중앙 V 형상과 깊은 파임을 다른 속성으로 둔다.

소유자: same top central neckline. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: plunge의 판매 설명이 V에 치우치더라도 특정 비V의 깊은 파임 문맥을 소거하지 않는다; cleavage 별도.

관찰 조건: 파임 양쪽 경계와 최저점이 식별되는 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you).

- 독립 변형 1: two sloping neckline edges meet at a central front point; the point lies below the upper chest
  관계: the two sloping neckline edges → meet_at → a central front point.

## SF021 · 스퀘어넥

씨앗: 스퀘어넥 — Square neck

의미: 가로 하단과 양쪽 직선에 가까운 측면으로 둘러싼 선.

소유자: same bodice neckline. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 쇄골 노출은 깊이·폭에 달림; 둥근 sweetheart나 bandeau의 직선만으로 대체 못함.

관찰 조건: 정면, 모서리가 실제 원단 가장자리여야 함.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Free People Prairie Field milkmaid top](https://www.freepeople.com/shop/prairie-field-top/).

- 독립 변형 1: near-vertical neckline sides meet a horizontal lower edge; both corners are visible on the same bodice
  관계: the neckline side edges → join → the horizontal lower neckline edge.

## SF022 · 스위트하트

씨앗: 스위트하트넥 — Sweetheart neckline

의미: 두 윗곡선과 가운데 내려간 접점의 관계.

소유자: same bodice upper edge. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 하트 프린트·가슴골·푸시업과 다른 구조.

관찰 조건: 컵 윗선 전체와 중앙 접점이 보이는 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: two rounded upper edges meet at a central dip; the same fabric bodice continues below them
  관계: the two rounded upper edges → meet_at → the central neckline dip.

## SF023 · 스트레이트어크로스

씨앗: 스트레이트어크로스 — Straight-across neckline

의미: 몸통 앞쪽을 수평으로 가로지르는 윗선.

소유자: same top upper edge. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 어깨끈·컵 형태·밑단 길이는 별도다.

관찰 조건: 수평 윗선과 어깨 연결이 확인되는 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit).

- 독립 변형 1: a straight upper edge extends across the front bodice; narrow shoulder straps attach at its outer ends
  관계: the straight upper edge → extends_across → the same front bodice.

## SF024 · 보트·바토넥

씨앗: 보트넥·바토넥 — Boat / Bateau neck

의미: 얕고 좌우로 넓은 목 파임과 어깨 쪽 끝점.

소유자: same top neckline. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.neckline` (existing_candidate_property_family).

혼동 경계: 넓음이 deep scoop이나 어깨 아래로 내려간 off-shoulder와 같지 않다.

관찰 조건: 양쪽 어깨까지 들어오는 정면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the shallow neckline extends toward both shoulder tops; the fabric still covers the outer shoulders
  관계: the boat neckline → extends_toward → both shoulder tops.

## SF025 · 카울·드레이프

씨앗: 카울넥 — Cowl neck, 드레이프 — Draping

의미: 여분의 원단이 늘어져 생기는 앞목 주름과 중력 방향.

소유자: same hanging neckline fabric. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.material.drape` (existing_candidate_property_family).

혼동 경계: cowl은 단순 U컷·주름 프린트·별도 목걸이가 아니며 깊이는 선택.

관찰 조건: 드레이프 가장자리와 원단 연속이 읽히는 근접 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: loose neckline fabric hangs between its shoulder attachments; curved folds descend across the front
  관계: the loose neckline fabric → hangs_between → its two shoulder attachments.

## SF026 · 오프숄더·바르도

씨앗: 오프숄더·바르도넥 — Off-shoulder / Bardot neckline

의미: 윗선이 양쪽 실제 어깨 아래로 내려간 상태.

소유자: same top upper edge and sleeves. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.shoulder` (existing_candidate_property_family).

혼동 경계: drop shoulder 봉제선·cold-shoulder 개구부와 분리; 원단을 내린 착용 상태도 별도.

관찰 조건: 양쪽 어깨와 소매 시작점이 같이 보이는 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the upper garment edge sits below both shoulder tops; the sleeves begin around the upper arms
  관계: the upper garment edge → sits_below → both shoulder tops.

## SF027 · 원숄더·비대칭 목둘레

씨앗: 원숄더 — One-shoulder, 어시메트릭 네크라인 — Asymmetric neckline

의미: 원숄더는 한 어깨의 연결, asymmetry는 더 넓은 좌우 불균형 범주.

소유자: same bodice shoulder attachment. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.shoulder` (existing_candidate_property_family).

혼동 경계: 화면 왼쪽과 착용자 왼쪽을 혼동하지 않는다; 모든 비대칭이 원숄더는 아님.

관찰 조건: 어깨 양쪽과 같은 의복의 대각선을 확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the bodice rises to the wearer's right shoulder; its opposite upper edge ends below the left shoulder
  관계: the bodice upper edge → rises_to → the wearer's right shoulder attachment.

## SF028 · 콜드숄더

씨앗: 콜드숄더 — Cold-shoulder

의미: 어깨의 개구부 위로 연결부가 남고 그 아래에 소매가 이어지는 구조.

소유자: same sleeve shoulder bridge. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.shoulder` (existing_candidate_property_family).

혼동 경계: off-shoulder 전체 이동과 다른 개구부 토폴로지.

관찰 조건: 어깨의 남은 브리지와 개구부 아래 소매 연결이 보임.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: cold_shoulder_cutout_sleeve_bridge.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: a fabric bridge remains over the shoulder opening; the sleeve continues below the exposed shoulder
  관계: the shoulder bridge → spans_above → the sleeve shoulder opening.

## SF029 · 키홀·프런트 컷아웃

씨앗: 키홀넥 — Keyhole neckline, 프런트 컷아웃 — Front cutout

의미: 키홀은 위쪽이 연결된 작은 개구부, front cutout은 위치 범주다.

소유자: same front bodice opening. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: 목 파임의 열린 가장자리·망사 투과·찢김 프린트로 대체하지 않는다.

관찰 조건: 개구부 둘레의 연속된 경계와 위의 연결부.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Cupshe Monokini / Cut Out](https://www.cupshe.com/collections/monokini-cut-out).

- 독립 변형 1: a small enclosed keyhole opens below the neckline; a fabric band bridges its upper edge
  관계: the top neckline band → bridges_above → the enclosed keyhole opening.

## SF030 · 일루전·누드 일루전

씨앗: 일루전 네크라인 — Illusion neckline, 누드 일루전 — Nude illusion

의미: 얇은 패널이 실제로 연결하는 경계와 피부색에 가까운 색을 별도로 기술한다.

소유자: same sheer support panel. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.material.transmission` (existing_candidate_property_family).

혼동 경계: nude는 색·착장·나체 다의어; 같은 피부색의 불투명 원단도 가능.

관찰 조건: 망사 가장자리·봉제·겹침이 확인되는 해상도; 피부색은 해당 착용자 기준.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

- 독립 변형 1: a fine sheer panel connects the bodice edge to the shoulder seam; its faint boundary remains visible
  관계: the sheer support panel → connects → the bodice edge to the shoulder seam.

- 독립 변형 2: the fabric surface is close in color to the wearer's skin; a seam and folded fabric edge establish the garment layer
  관계: the fabric surface color → resembles → the wearer's local skin tone.

## SF031 · 슬리브리스·캡 슬리브

씨앗: 슬리브리스 — Sleeveless, 캡 슬리브 — Cap sleeve

의미: 소매 없음과 어깨끝만 덮는 짧은 소매의 차이.

소유자: same top arm opening. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.sleeve` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 슬리브리스는 암홀 깊이·겨드랑이 가시성·노출 면적을 자동 결정하지 않는다.

관찰 조건: 어깨끝·암홀 경계가 함께 보이는 앞/사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the finished armhole edge surrounds the arm opening; the bodice has no projecting sleeve
  관계: the sleeveless armhole edge → surrounds → the same arm opening.

- 독립 변형 2: a small cap sleeve extends over the shoulder tip; its lower edge ends above the upper arm
  관계: the cap sleeve edge → extends_over → the shoulder tip.

## SF032 · 플러터·퍼프 소매

씨앗: 플러터 슬리브 — Flutter sleeve, 퍼프 슬리브 — Puff sleeve

의미: 플러터의 자유 하단 퍼짐과 퍼프의 모음으로 생긴 부피를 구분한다.

소유자: same sleeve volume. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.sleeve` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 겹치는 flutter/puff cap 변형을 허용; 바람·움직임·좁은 허리를 필수화하지 않는다.

관찰 조건: 부착선·소매 하단과 부피를 동시에 봄.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Burda 6502 peasant blouses](https://simplicity.com/burda-style/bur6502), [Free People Prairie Field milkmaid top](https://www.freepeople.com/shop/prairie-field-top/).

- 독립 변형 1: the flutter sleeve has a loose flared lower edge; its fabric hangs away from the upper arm
  관계: the flutter sleeve free edge → flares_away_from → the upper arm.

- 독립 변형 2: the sleeve fabric bulges between the shoulder seam and a gathered cuff; small folds converge at both boundaries
  관계: the gathered sleeve fabric → bulges_between → its shoulder seam and gathered cuff.

## SF033 · 래글런·드롭숄더 연결선

씨앗: 래글런 슬리브 — Raglan sleeve, 드롭숄더 — Drop shoulder

의미: 겨드랑이-목 사선 연결과 실제 어깨보다 아래의 연결선 위치를 독립적으로 둔다.

소유자: same top sleeve-to-bodice seam. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.fit.shoulder.seam_position` (existing_candidate_property_family).

혼동 경계: 노출·수치·어깨 너비·소매 길이는 다른 축; 원단무늬만 사선인 것은 raglan 아님.

관찰 조건: 봉제선의 실제 양 끝점과 신체 어깨 기준점을 확인.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: fit_ff09_v1_candidate.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the sleeve seam runs diagonally from the underarm to the neckline; the sleeve and bodice meet along that seam
  관계: the raglan sleeve seam → runs_from → the underarm to the neckline.

- 독립 변형 2: the shoulder seam lies below the wearer's shoulder tip; the sleeve begins down the upper arm
  관계: the shoulder seam → lies_below → the wearer's shoulder tip.

## SF034 · 딥 암홀·머슬 탱크

씨앗: 딥 암홀·드롭 암홀 — Deep / Dropped armhole, 머슬 탱크 — Muscle tank

의미: 암홀 아래끝이 몸통 옆으로 내려가는 위치와 민소매 기본 형태를 나눈다.

소유자: same armhole lower boundary. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: muscle tank가 항상 deep armhole는 아니며 팔을 올린 것만으로 넓은 암홀을 증명 못함.

관찰 조건: 팔이 옆면 경계를 가리지 않는 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the armhole lower edge descends below the underarm crease; the side opening exposes a narrow strip of torso
  관계: the armhole lower edge → descends_below → the underarm crease.

## SF035 · 레이서백·크로스백

씨앗: 레이서백 — Racerback, 크로스백 — Cross-back

의미: 중앙 합류와 X 교차는 다른 연결 그래프다.

소유자: same back strap network. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.back_strap_connection` (existing_candidate_property_family).

혼동 경계: 교차 그림·멀티끈·목걸이·다른 의복의 끈을 같은 스트랩으로 합치지 않는다.

관찰 조건: 뒤면에서 모든 연결 끝점과 교차/합류 지점을 확인.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: fit_ff52_v1_candidate, fit_ff52_v2_candidate, crossback_strap_intersection.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Burda 5891 halter top](https://simplicity.com/burda-style/bur5891).

- 독립 변형 1: two upper back straps converge into one central band; the band joins the lower back panel
  관계: the two upper back straps → converge_into → one central back band.

- 독립 변형 2: two back straps cross at the center of the back; each continues to an opposite lower bodice attachment
  관계: the two back straps → cross_at → the center of the same back.

## SF036 · 오픈백·백리스·로백

씨앗: 오픈백 — Open-back, 백리스 — Backless, 로백 — Low-back

의미: 뒤판 개구부·적은 뒤판·낮은 뒤쪽 윗선을 구분한다.

소유자: same back bodice boundary. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: 앞면 높은 덮임과 공존 가능; hair occlusion은 등을 가리는 의복 커버리지와 다름.

관찰 조건: 뒤판 경계를 머리카락·팔이 가리지 않는 뒤 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Burda 5891 halter top](https://simplicity.com/burda-style/bur5891), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: the back garment edge sits below the shoulder blades; the front bodice remains high at the neck
  관계: the back upper garment edge → sits_below → the shoulder blades.

## SF037 · 오픈사이드·허리·사이드 컷아웃

씨앗: 오픈사이드 — Open-side, 컷아웃 — Cutout, 웨이스트 컷아웃 — Waist cutout, 사이드 컷아웃 — Side cutout, 컷아웃 드레스 — Cutout dress

의미: 완전히 둘러싼 구멍과 옆 가장자리까지 열린 틈의 경계를 구분한다.

소유자: same garment side opening. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: waist와 side는 위치에 따라 중첩 가능; cutout은 단순 시어·분리 의복 간 공백이 아님.

관찰 조건: 열린 부위의 위·아래 연결과 둘레를 확인.

처리: P0 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Cupshe Monokini / Cut Out](https://www.cupshe.com/collections/monokini-cut-out), [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

- 독립 변형 1: a skin window is enclosed within the bodice side; continuous fabric remains above and below the opening
  관계: the side cutout perimeter → surrounds → a waist skin window within the same bodice.

- 독립 변형 2: the garment side is open between its upper and lower panels; a narrow band connects those panels
  관계: the top and bottom side edges → join_through → a narrow connecting band.

## SF038 · 피티드·바디스키밍

씨앗: 피티드 — Fitted, 바디스키밍 — Body-skimming

의미: 재단된 가까운 핏과 윤곽을 가볍게 따르는 직물의 국소 접촉·여유.

소유자: same garment local contact. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 새 체형을 생성하지 않으며 tight/압박/정확 치수는 별도.

관찰 조건: 몸통의 옷 경계·접촉 구간·처지는 구간이 보이는 사선.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: pfe_skimming_candidate.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the fabric lightly follows the torso; small loose spans hang between its contact areas
  관계: the body-skimming fabric → hangs_between → its local torso contact areas.

## SF039 · 바디콘·스킨타이트

씨앗: 바디콘 — Bodycon, 스킨타이트 — Skin-tight

의미: 몸통과 하체 윤곽 가까이 따라가는 의복의 여유 상태.

소유자: same opaque fitted garment. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 붙음은 비침·피부 노출·가슴/힙 확대가 아니며 stretch 섬유 조성은 미확인.

관찰 조건: 불투명 원단의 경계와 주름 상태를 확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [LYCRA quality FAQ](https://one.lycra.com/en/lycra-frequently-asked-questions/quality-lycra).

- 독립 변형 1: opaque close-fitting fabric follows the torso and hip contour; the garment edge remains continuous across the covered areas
  관계: the close-fitting fabric → follows → the torso and hip contour.

## SF040 · 밴디지 스타일

씨앗: 밴디지 스타일 — Bandage style

의미: 띠 같은 패널이 몸통 주위를 감싸는 시각적 구조.

소유자: same banded garment panels. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 진짜 압박·의료 붕대·로프 결박·무조건 가로줄 프린트로 합치지 않는다.

관찰 조건: 패널 부착 경계·겹침과 질감이 식별되는 근접면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: broad fabric bands wrap around the bodice; their joined edges form visible horizontal panel boundaries
  관계: the broad fabric bands → join_along → their edges around the same bodice.

## SF041 · 허리 강조·아워글라스·핏앤플레어

씨앗: 웨이스트 디파인드 — Waist-defined, 아워글라스 실루엣 — Hourglass silhouette, 핏앤플레어 — Fit-and-flare

의미: 의복 허리의 좁음, 상하부 폭 대비, 하부 퍼짐 시작을 따로 기술한다.

소유자: same garment waist and skirt. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit.waist_suppression` (existing_candidate_property_family).

혼동 경계: hourglass 의복을 신체 형태 변경으로 해석하지 않는다; 모든 허리강조가 flare 아님.

관찰 조건: 의복 허리와 상하부 폭을 한 시점에서 봄.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Seamwork Posie surplice dress](https://www.seamwork.com/pdf-sewing-patterns/posie-surplice-wrap-dress).

- 독립 변형 1: the bodice narrows at the garment waist; the skirt panels flare outward below that seam
  관계: the skirt panels → flare_below → the fitted garment waist.

## SF042 · 바이어스 컷

씨앗: 바이어스 컷 — Bias cut

의미: 재단 방향은 명세로, 몸을 따라 사선으로 흐르는 처짐은 관찰로 나눈다.

소유자: same garment drape and grain specification. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.material.drape` (existing_candidate_property_family).

혼동 경계: 45도는 true bias 정의이지 사진의 주름각 측정치 아님; 새틴·silk·bodycon과 독립.

관찰 조건: 직물 결이 보이지 않으면 drape만 관찰하고 제작 방식은 NOT_OBSERVABLE.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: bias_cut_body_skimming_drape.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Seamwork Freesia empire-waist bias dress](https://www.seamwork.com/pdf-sewing-patterns/freesia-empire-waist-bias-dress).

- 독립 변형 1: soft oblique folds settle around the hips; the skirt fabric falls in a continuous fluid sheet
  관계: the hanging skirt fabric → forms → oblique soft folds around the hips.

## SF043 · 릴랙스드·박시·오버사이즈

씨앗: 릴랙스드 핏 — Relaxed fit, 박시 핏 — Boxy fit, 오버사이즈 — Oversized

의미: 편한 여유, 직선 몸판, 확장된 품·어깨·길이는 서로 다른 속성이다.

소유자: same garment ease distribution. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: boxy가 항상 oversized는 아니며 긴 길이만으로 전부 과대 사이즈라 확정 못함.

관찰 조건: 옷과 몸의 간격·어깨선·밑단을 함께 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Seamwork Negroni camp shirt](https://www.seamwork.com/pdf-sewing-patterns/negroni-vintage-camp-shirt).

- 독립 변형 1: the boxy shirt side edges descend to a straight hem; the bodice remains roomy through the waist
  관계: the boxy shirt side edges → descend_without_narrowing_to → the straight lower hem.

## SF044 · 뷔스티에·코르셋·오버/언더버스트

씨앗: 뷔스티에 — Bustier, 코르셋 톱 — Corset top, 오버버스트 코르셋 — Overbust corset, 언더버스트 코르셋 — Underbust corset

의미: 컵을 포함한 몸통 구조와 가슴 아래에서 시작하는 경계를 분리한다.

소유자: same structured garment upper boundary. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: fashion corset 표면이 실제 압박·waist training을 입증하지 않는다; underbust는 다른 상의 층 필요할 수 있음.

관찰 조건: 실제 윗선과 이너의 층 순서·패널 경계를 볼 수 있어야 한다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Simplicity S3118 corset and skort](https://simplicity.com/simplicity/pds3118).

- 독립 변형 1: the structured outer garment begins below the bust; the blouse continues above its upper edge
  관계: the underbust outer garment edge → starts_below → the bust of the inner blouse.

- 독립 변형 2: the overbust bodice panels continue from the cup area into the waist; visible seams divide the shaped panels
  관계: the overbust bodice panels → continue_from → the cup area into the garment waist.

## SF045 · 발코네트·데미 컵

씨앗: 발코네트 — Balconette, 데미컵 — Demi cup

의미: 컵 윗선의 방향·깊이와 넓게 떨어진 끈의 상대 배치를 기록한다.

소유자: same cup top and strap attachment. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.cup_edge` (existing_candidate_property_family).

혼동 경계: 브랜드가 두 이름을 함께 사용하므로 고정 컵 면적 %나 배타적 종류로 저장하지 않는다.

관찰 조건: 컵 윗선 양쪽과 중앙·끈 부착점이 보이는 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you).

- 독립 변형 1: the cup upper edges run nearly horizontally; the shoulder straps attach near the outer cup sides
  관계: the cup upper edges → run_nearly_horizontally_between → the outer strap attachments.

## SF046 · 플런지 컵 중앙선

씨앗: 플런지 브라·컵 — Plunge bra / cup

의미: 낮은 중앙 연결부와 두 컵의 안쪽 경계.

소유자: same bra or swim top center. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.cup_edge` (existing_candidate_property_family).

혼동 경계: plunge bra의 형태와 deep V dress의 겉목 파임을 하나의 의복으로 합치지 않는다.

관찰 조건: 컵 사이의 연결과 이너/겉옷을 구분할 앞면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you), [Wacoal normal vs push-up bra](https://www.wacoalindia.com/blogs/stories/understanding-the-difference-between-a-normal-bra-and-a-push-up-bra).

- 독립 변형 1: the cup inner edges descend toward a low central connector; each cup remains joined to the same underbust band
  관계: the two cup inner edges → meet_at → a low central connector.

## SF047 · 푸시업·언더와이어·몰디드 컵

씨앗: 푸시업 — Push-up, 언더와이어 — Underwire, 몰디드 컵 — Molded cup

의미: 패드 위치·컵하부 보강·성형 구조는 독립 설계 속성이다.

소유자: same cup internal specification. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 표면의 매끈함은 실제 wire/pad/열성형 공정 증거가 아니다; 몸 수정 후보로 전환하지 않는다.

관찰 조건: 숨은 속성은 명세로 보존; 원단 외곽·보강 채널을 보여주는 경우만 별도 후보화.

처리: P1 / preserve_specification_no_automatic_pixel_candidate. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you), [Wacoal normal vs push-up bra](https://www.wacoalindia.com/blogs/stories/understanding-the-difference-between-a-normal-bra-and-a-push-up-bra).

명세/물품 유형을 보존하되 이번에는 자동 픽셀 후보를 만들지 않는다. 별도 관찰 가능한 물품 시점이 필요한 경우 후속 승격에서 작성한다.

## SF048 · 보닝·프린세스 심·다트·언더버스트 심

씨앗: 보닝 — Boning, 프린세스 심 — Princess seam, 다트 — Dart, 언더버스트 심 — Underbust seam

의미: 보강재·패널 연결선·쐐기 접힘·가슴아래 절개는 다른 기능과 외형이다.

소유자: same bodice seam or casing. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 보닝 채널을 보강재 존재로, 절개선을 피부 노출로, princess를 왕족으로 읽지 않는다.

관찰 조건: 연결선의 시작/끝·원단 양쪽 이어짐·입체 fold apex를 확인.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct031_v1.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: two stitched dart legs converge at one bodice point; the surrounding fabric forms a shallow shaped fold
  관계: the dart fold legs → converge_at → one point in the same bodice.

- 독립 변형 2: a curved vertical seam joins two shaped bodice panels; it continues from the upper chest toward the waist
  관계: the curved vertical seam → joins → two shaped panels of the same bodice.

## SF049 · 데콜테와 클리비지

씨앗: 데콜테 — Décolletage, 클리비지 — Cleavage

의미: 목 아래·쇄골·가슴 윗부분의 영역과 가슴 사이 중앙 골 가시성을 구별한다.

소유자: same wearer and garment upper opening. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.upper_edge` (existing_candidate_property_family).

혼동 경계: 네크라인 이름이나 컵 모양만으로 cleavage를 확정하지 않는다.

관찰 조건: 요청된 해당 부위가 실제 시점·원단·머리카락에 가려지지 않아야 한다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines), [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you).

- 독립 변형 1: the garment edge sits below the collarbones; the exposed collarbone area remains unobstructed
  관계: the garment upper edge → leaves_visible → the collarbone area.

- 독립 변형 2: the central neckline opening reveals the groove between the adult wearer's breasts; the garment panels retain visible inner edges beside that opening
  관계: the central garment neckline opening → reveals → the groove between the same adult wearer's breasts.

## SF050 · 사이드붑·언더붑

씨앗: 사이드붑 — Sideboob, 언더붑 — Underboob

의미: 가슴 옆 경계와 아랫경계의 가시성은 위치가 다른 관찰 상태다.

소유자: same adult wearer boundary and garment edge. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: 깊은 암홀·micro crop·underbust seam이 해당 노출을 필수로 만들지 않는다; 슬랭은 의복 종류 아님.

관찰 조건: 해당 경계와 이를 덮는 가장자리의 관계가 직접 보여야 함; 선정 여부와 사실 판정은 별도.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: pfe_lateral_chest_candidate, pfe_lower_chest_candidate.

출처: [Vogue Alexander Wang spring 2025](https://www.vogue.com/fashion-shows/spring-2025-ready-to-wear/alexander-wang), [MasterClass neckline guide](https://www.masterclass.com/articles/guide-to-necklines).

- 독립 변형 1: a bounded outer breast contour is visible beside the adult bodice arm opening; the same opaque bodice covers the central breast surface
  관계: the same adult bodice side edge → leaves_visible → a bounded outer breast contour.

- 독립 변형 2: a bounded lower breast contour is visible below the adult top edge; the upper breast surface remains covered by the same opaque top
  관계: the same adult top lower edge → sits_above → a bounded lower breast contour.

## SF051 · 미드리프와 배꼽 가시성

씨앗: 미드리프 베어링 — Midriff-baring, 네이블 베어링 — Navel-baring

의미: 복부의 연속된 틈과 그 틈 안에 실제 배꼽이 보이는 상태를 별개로 둔다.

소유자: same top hem, lower waistband and wearer. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: cropped/high-rise/low-rise 각 이름은 배꼽의 실제 가시성을 보증하지 않는다.

관찰 조건: 상하의 기준선과 배꼽이 한 시점에 식별됨.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: pfe_midriff_candidate.

출처: [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Seafolly high-leg high-waist bottom](https://sg.seafolly.com/products/jetset-lure-high-leg-high-waist-bikini-bottom-j30196-black).

- 독립 변형 1: the top hem ends above the navel; the lower waistband sits below it, leaving the navel visible between the garment edges
  관계: the exposed abdomen gap → contains → the visible navel.

- 독립 변형 2: a narrow abdomen strip appears below the top hem; the waistband covers the navel beneath that strip
  관계: the exposed abdomen gap → lies_above → the covered navel.

## SF052 · 슬릿·사이하이·슬릿 스커트

씨앗: 슬릿 — Slit, 사이하이 슬릿 — Thigh-high slit, 슬릿 스커트 — Slit skirt

의미: 밑단에서 이어진 트임·상단 높이·시점에 따른 실제 벌어짐을 분리한다.

소유자: same skirt slit and hem. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: 긴 skirt와 thigh-high slit은 공존; 트임 높음이 다리 노출을 항상 보증하지 않는다.

관찰 조건: 밑단·트임 상단과 다리가 보이는 전체/사선; 닫힌 겹침이면 가시성은 미확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seamwork Posie surplice dress](https://www.seamwork.com/pdf-sewing-patterns/posie-surplice-wrap-dress).

- 독립 변형 1: two skirt edges separate below a slit apex at the upper thigh; the same long hem continues on both sides
  관계: the skirt slit edges → separate_below → a slit apex at the upper thigh.

## SF053 · 오픈워크의 구멍과 투과

씨앗: 오픈워크 — Openwork

의미: 실제 실 사이 개구부와 연속 원단을 통한 투과를 분리한다.

소유자: same openwork outer layer and inner layer. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.transmission` (existing_candidate_property_family).

혼동 경계: mesh/lace/crochet=나체가 아님; lining이 조직 구멍 뒤를 덮을 수 있다.

관찰 조건: 구멍·실·아래층 경계를 원해상도에서 확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: openwork holes reveal an opaque inner layer; the surrounding yarn forms the outer garment surface
  관계: the openwork holes → reveal → the opaque inner layer.

## SF054 · 언라인드·브라리스

씨앗: 언라인드 — Unlined, 브라리스 — Braless

의미: 안감 없음과 브라 미착용은 층 구성/착용 상태 명세이며 외관과 독립적이다.

소유자: same hidden clothing layers. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: 불투명 겉옷·스트랩 부재·자연스러운 윤곽은 미착용의 증거가 아니다.

관찰 조건: 확인 가능한 단면·열린 안쪽이 없으면 비시각 메타데이터로 유지.

처리: P0 / preserve_specification_no_automatic_pixel_candidate. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Wacoal normal vs push-up bra](https://www.wacoalindia.com/blogs/stories/understanding-the-difference-between-a-normal-bra-and-a-push-up-bra), [CAKES grippy circles](https://cakesbody.com/products/grippy-cakes-circles), [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

명세/물품 유형을 보존하되 이번에는 자동 픽셀 후보를 만들지 않는다. 별도 관찰 가능한 물품 시점이 필요한 경우 후속 승격에서 작성한다.

## SF055 · 비저블 란제리·웨일테일·네이키드 드레싱

씨앗: 비저블 란제리 — Visible lingerie, 웨일테일 — Whale tail, 네이키드 드레싱 — Naked dressing

의미: 별도 이너의 보이는 가장자리/끈과 넓은 착장 인상을 분리한다.

소유자: same inner garment and outer garment. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: naked dressing은 실제 나체가 필수 아님; whale tail의 끈을 겉옷 허리띠나 동물 꼬리로 대체 못함.

관찰 조건: 층별 소유자와 이너의 계속되는 경계, 뒤쪽이면 뒤면 확인.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: y2kr_whale_tail.

출처: [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/), [Vogue whale-tail outfit](https://www.vogue.com/article/teyana-taylor-aughties-trend-whale-tail).

- 독립 변형 1: the inner underwear back straps rise above the low trouser waistband; the straps join into a visible Y at the back
  관계: the inner underwear back straps → rise_above → the outer trouser waistband.

## SF056 · 국소 니플 커버·패스티

씨앗: 니플 커버·패스티 — Nipple covers / Pasties

의미: 브라와 별도의 국소 덮개 제품 유형; 모양·색·부착 방식은 제품별로 다름.

소유자: same independent coverage accessory. 제안 슬롯: `wearable_accessory`. 속성 가족: `wardrobe.coverage` (existing_candidate_property_family).

혼동 경계: braless와 양립 가능; 숨은 커버를 피부·겉옷 윤곽만으로 판정하지 않는다.

관찰 조건: 물품을 따로 볼 수 있는 제품 시점 또는 확실한 층 경계; 접착 성능은 관찰 불가.

처리: P1 / preserve_specification_no_automatic_pixel_candidate. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [CAKES grippy circles](https://cakesbody.com/products/grippy-cakes-circles).

명세/물품 유형을 보존하되 이번에는 자동 픽셀 후보를 만들지 않는다. 별도 관찰 가능한 물품 시점이 필요한 경우 후속 승격에서 작성한다.

## SF057 · 선드레스·슬립·셔츠·티셔츠 드레스

씨앗: 선드레스 — Sundress, 슬립 드레스 — Slip dress, 셔츠 드레스 — Shirt dress, 티셔츠 드레스 — T-shirt dress

의미: 계절 용도, 얇은 끈 몸판, 셔츠 디테일, 길어진 티 구조를 별개로 둔다.

소유자: same dress base structure. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: sundress가 모두 mini·노출·floral인 것은 아님; slip=새틴·속옷 착용도 아님.

관찰 조건: 상체 연결과 드레스 밑단을 볼 수 있는 전신/중거리.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork Brom shirt dress](https://www.seamwork.com/pdf-sewing-patterns/brom-pleated-sleeve-shirt-dress), [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: narrow straps support a softly hanging dress bodice; the fabric continues into a simple skirt
  관계: the narrow dress straps → support → the softly hanging dress bodice.

- 독립 변형 2: a folded collar frames the shirt dress neck; the front button row continues down toward the skirt
  관계: the shirt dress front → continues_along → a button row toward its skirt hem.

## SF058 · 시스·시프트·A라인

씨앗: 시스 드레스 — Sheath dress, 시프트 드레스 — Shift dress, 에이라인 드레스 — A-line dress

의미: 몸 가까운 재단, 어깨에서 직선으로 떨어짐, 아래로 폭 증가를 나눈다.

소유자: same dress waist and hem width. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: sheath=skin-tight는 아님; A-line의 시작점과 waist fit은 선택. 실제 shift 패턴에도 slight empire waist가 있어 분류명을 배타적인 구조 계약으로 취급하지 않는다.

관찰 조건: 어깨·허리·밑단 폭을 한 시점에서 읽음.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork Sloan sheath dress](https://www.seamwork.com/pdf-sewing-patterns/sloan-puff-sleeve-dress), [Seamwork Georgia shift dress](https://www.seamwork.com/pdf-sewing-patterns/georgia-easy-woven-shift-dress), [Seamwork Brom shirt dress](https://www.seamwork.com/pdf-sewing-patterns/brom-pleated-sleeve-shirt-dress), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the dress side edges fall nearly straight from the shoulders; the waist has visible ease
  관계: the shift dress side edges → fall_from → the shoulders toward a nearly straight hem.

- 독립 변형 2: the dress side edges widen toward the lower hem; the skirt forms a clear A-shaped outline
  관계: the dress side edges → widen_toward → the lower hem.

## SF059 · 베이비돌·엠파이어·드롭웨이스트

씨앗: 베이비돌 드레스 — Babydoll dress, 엠파이어 웨이스트 — Empire waist, 드롭웨이스트 — Drop waist

의미: babydoll의 형태군과 높은/낮은 허리 절개 위치를 독립적으로 둔다.

소유자: same dress seam landmark. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.details.waistline_position` (existing_candidate_property_family).

혼동 경계: babydoll은 아동 나이 요청이 아니고 empire=임신·체형 변경 아님; 정확 기준점 지정 필요. empire waist와 body-skimming fit은 실제 패턴에서 공존한다.

관찰 조건: 가슴아래·자연허리·골반과 절개선을 함께 확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork Freesia empire-waist bias dress](https://www.seamwork.com/pdf-sewing-patterns/freesia-empire-waist-bias-dress), [Seamwork Georgia shift dress](https://www.seamwork.com/pdf-sewing-patterns/georgia-easy-woven-shift-dress), [Butterick B5764 mock wrap](https://simplicity.com/butterick/pdb5764).

- 독립 변형 1: the skirt attaches just below the bust; loose fabric descends from the raised seam
  관계: the dress skirt seam → sits_just_below → the bust.

- 독립 변형 2: the bodice extends below the natural waist; the skirt attaches at a lower seam near the hips
  관계: the dress skirt seam → sits_below → the natural waist.

## SF060 · 티어드 드레스

씨앗: 티어드 드레스 — Tiered dress

의미: 가로 층 연결과 각 층의 폭/모음.

소유자: same connected skirt tiers. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 러플 덧장식·실제 속치마 층과 서로 다른 구조; 전부 한꺼번에 요구하지 않는다.

관찰 조건: 각 가로 연결선과 위아래 원단 연속이 읽히는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: successive skirt tiers join at horizontal seams; each lower tier has more gathered width than the one above
  관계: successive skirt tiers → join_at → horizontal gathered seams.

## SF061 · 롬퍼·점프슈트·보디수트

씨앗: 롬퍼·플레이수트 — Romper / Playsuit, 점프슈트 — Jumpsuit, 보디수트 — Bodysuit

의미: 상체와 하체의 의복 연속성, 다리통 길이, 보디수트의 아래 연결을 구분한다.

소유자: same connected upper and divided lower garment. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: bodysuit가 swimsuit·속옷·wetness와 같은 의미 아님; 숨은 가랑이 연결은 픽셀 증거가 부족할 수 있음.

관찰 조건: 롬퍼/점프수트는 연결 몸판과 두 다리통을 함께; 가려진 bodysuit 연결은 미확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [McCall M8454 romper](https://simplicity.com/mccalls/m8454), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: the bodice continues into two separate short leg sections; one continuous garment seam joins the waist
  관계: the romper bodice → continues_into → two separate short leg sections.

## SF062 · 미니·마이크로·미디·맥시 길이

씨앗: 미니스커트 — Mini skirt, 마이크로 미니 — Micro mini, 미디스커트 — Midi skirt, 맥시스커트 — Maxi skirt

의미: 밑단을 무릎·종아리·발목 같은 기준점에 상대적으로 기록한다.

소유자: same skirt hem relative to legs. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 판매명이 통일된 cm 경계는 아님; 사진 crop으로 잘린 다리를 skirt 길이로 판정 못함.

관찰 조건: 실제 밑단과 대응 신체 기준점이 함께 보임.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134), [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between).

- 독립 변형 1: the skirt hem ends between the knee and ankle; a clear lower-leg gap remains above the footwear
  관계: the midi skirt hem → ends_between → the knee and ankle.

- 독립 변형 2: the skirt hem ends above the knee; the lower garment edge remains visible across the front
  관계: the mini skirt hem → ends_above → the knee.

## SF063 · 펜슬·서클·스케이터

씨앗: 펜슬스커트 — Pencil skirt, 서클스커트 — Circle skirt, 스케이터 스커트 — Skater skirt

의미: 좁고 가까운 하부 윤곽과 허리에서 넓게 퍼지는 형태를 나눈다.

소유자: same skirt local width distribution. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: circle는 패턴 재단 의미도 있음; 풍성한 사진만으로 정확한 원형 패턴 공정은 미확인. half-circle 재단과 front box pleat도 동시 성립한다.

관찰 조건: 허리·힙·밑단 폭과 옷의 경계를 함께 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork Brooklyn half-circle skirt](https://www.seamwork.com/pdf-sewing-patterns/brooklyn-full-skirt), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the skirt follows the hips toward a narrow hem; its side edges remain close below the hip
  관계: the skirt fabric → follows → the hip toward a narrow hem.

- 독립 변형 2: the short skirt panels flare from a fitted waistband; the broad hem forms loose curved folds
  관계: the short skirt panels → flare_from → the fitted waistband.

## SF064 · 플리츠·플리츠 스커트

씨앗: 플리츠 스커트 — Pleated skirt, 플리츠 — Pleats

의미: 반복 접힘의 ridge/valley, 방향, 폭과 고정 구간.

소유자: same repeated folded fabric. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 주름 프린트·잔잔한 구김·셔링 모음은 다른 표면; box/knife를 동의어 병합하지 않는다.

관찰 조건: 접힌 외곽과 음영·실제 겹침이 해상도에서 보여야 함.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Simplicity S3118 corset and skort](https://simplicity.com/simplicity/pds3118).

- 독립 변형 1: repeated pleat ridges alternate with recessed valleys; the folds continue from the skirt upper edge toward the hem
  관계: the repeated pleat ridges → alternate_with → recessed fold valleys.

## SF065 · 사롱·파레오·랩 스커트

씨앗: 사롱 스커트 — Sarong skirt, 파레오 — Pareo / Pareu, 사롱 — Sarong

의미: 몸에 둘러 입은 천의 겹침·매듭과 용도; sarong/pareo 문화 명칭은 기록 유지.

소유자: same wrapping cloth. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure.front_fastener_state` (existing_candidate_property_family).

혼동 경계: 현대 beach 용법의 유사성이 역사적 복식 전체의 동일성을 뜻하지 않는다; 단순 skirt 프린트가 아님.

관찰 조건: 겹친 천의 끝점과 실제 묶음·밑단을 확인.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_wrapcover.

출처: [Seafolly resort cover ups](https://us.seafolly.com/collections/kaftans-cover-ups), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: one sheet of cloth wraps around the hips; its two ends meet in a side waist knot
  관계: the wrapped cloth ends → meet_at → a side waist knot.

## SF066 · 하이로·비대칭 스커트

씨앗: 하이로 스커트 — High-low skirt, 어시메트릭 스커트 — Asymmetric skirt

의미: 앞뒤 길이 차이와 더 넓은 비대칭 범주.

소유자: same skirt hem positions. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 원근·옷을 들어올린 상태를 재단된 비대칭으로 오인하지 않는다.

관찰 조건: 앞뒤 또는 좌우의 실제 밑단을 구분할 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [McCall M8583 bubble-hem skirt](https://simplicity.com/mccalls/pdm8583).

- 독립 변형 1: the front skirt hem ends above the back hem; both lengths belong to the same continuous skirt
  관계: the front skirt hem → ends_above → the back hem of the same skirt.

## SF067 · 버블·머메이드 스커트

씨앗: 버블 스커트 — Bubble skirt, 머메이드 스커트 — Mermaid skirt

의미: 안으로 모인 밑단의 풍선 부피와 힙/허벅지 아래 퍼짐을 구분한다.

소유자: same lower skirt boundary. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.silhouette` (proposed_family_requires_schema_and_effect_review).

혼동 경계: mermaid skirt가 꼬리·물속 인물·mermaidcore를 뜻하지 않는다; flare onset을 구체화.

관찰 조건: 수축 밑단 또는 퍼짐 시작점과 같은 skirt 원단 연결.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [McCall M8583 bubble-hem skirt](https://simplicity.com/mccalls/pdm8583), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the skirt swells above a gathered lower edge; the hem turns inward beneath that volume
  관계: the gathered lower skirt edge → turns_inward_under → the rounded skirt volume.

- 독립 변형 2: the skirt follows the hips and upper thighs; its lower panels flare outward below that fitted section
  관계: the lower skirt → flares_below → the fitted upper-thigh section.

## SF068 · 핫팬츠·조츠·데님 컷오프

씨앗: 핫팬츠·쇼트쇼츠 — Hot pants / Short shorts, 데님 컷오프 — Denim cutoffs, 조츠 — Jorts

의미: 아주 짧은 다리통, 데님 원단, 잘라낸 듯 올풀림 마감은 독립 축.

소유자: same shorts length and raw edge. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: jorts의 긴 버전도 있음; denim이나 cutoff가 반드시 hot pants를 뜻하지 않는다.

관찰 조건: 양 다리 밑단과 올풀림을 읽을 가까운 전신.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: the denim shorts have short frayed edge threads; both separate leg hems remain visible
  관계: the denim shorts hems → have → short frayed edge threads.

## SF069 · 버뮤다·테일러드 쇼츠

씨앗: 버뮤다 쇼츠 — Bermuda shorts, 테일러드 쇼츠 — Tailored shorts

의미: 무릎 부근 길이와 허리밴드·다트·앞주름 등의 재단 구조를 분리한다.

소유자: same shorts hem and tailoring. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: tailored가 long/baggy 또는 남성 정체성과 동일하지 않다.

관찰 조건: 무릎과 두 밑단, 허리의 실제 봉제선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S3238 vest top and shorts](https://simplicity.com/simplicity/pds3238), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: two shorts hems end near the knees; a shaped waistband joins the separate leg panels
  관계: the shorts hems → end_near → the knees.

## SF070 · 박서·블루머 쇼츠

씨앗: 박서 쇼츠 — Boxer shorts, 블루머 쇼츠 — Bloomer shorts

의미: 고무줄 허리의 느슨한 다리통과 다리입구를 모은 부푼 형태.

소유자: same shorts waistband and leg openings. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: boxer 판매명은 속옷 착용을 보증하지 않는다; bloomers도 아동 나이를 의미하지 않는다.

관찰 조건: 허리와 양 다리입구 경계가 보이는 전체 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: each shorts leg has puffed fabric above a gathered opening; the two lower openings remain separate
  관계: the gathered shorts leg openings → hold_below → the puffed leg fabric.

## SF071 · 바이커·러닝 쇼츠

씨앗: 바이커 쇼츠 — Biker shorts, 러닝 쇼츠 — Running shorts

의미: 가까운 신축형 다리통과 여유 있는 달리기형 형태를 분리한다.

소유자: same short leg fit. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 러닝의 성능·실제 운동 행동·체형·근육량을 자동 생성하지 않는다.

관찰 조건: 다리통의 여유·옆트임·길이가 보이는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Nike Miler brief-lined running shorts](https://www.nike.com/gb/t/miler-dri-fit-12-5cm-brief-lined-running-shorts-P2UpNPGN/IF2060-382), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease), [LYCRA quality FAQ](https://one.lycra.com/en/lycra-frequently-asked-questions/quality-lycra).

- 독립 변형 1: the close-fitting shorts follow the upper thighs; their two hems end around mid-thigh
  관계: the close-fitting short leg fabric → follows → the upper-thigh contour.

## SF072 · 카고 쇼츠 주머니

씨앗: 카고 쇼츠 — Cargo shorts

의미: 허벅지 옆의 외부 덧주머니와 덮개 연결.

소유자: same shorts patch pockets. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: cargo가 군인·무기·폭력 상황·특정 색을 필수로 요구하지 않는다.

관찰 조건: 덧주머니 부착선과 덮개를 식별하는 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: a large patch pocket attaches to the outer thigh panel; a flap covers its upper opening
  관계: the side patch pocket → attaches_to → the outer thigh panel of the shorts.

## SF073 · 스코트·큐롯

씨앗: 스코트 — Skort, 퀼로트·큐롯 — Culottes

의미: skort는 스커트와 바지의 결합, culottes는 넓은 분리 다리통이다.

소유자: same visible skirt layer or divided trousers. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 앞의 skirt 같은 윤곽만으로 안쪽 shorts를 단정하지 않는다.

관찰 조건: 분리 다리통이나 바지/앞덮개 층 경계를 보여주는 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S3118 corset and skort](https://simplicity.com/simplicity/pds3118), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134), [McCall M8454 romper](https://simplicity.com/mccalls/m8454).

- 독립 변형 1: a skirt-like front panel overlaps attached shorts; the separate shorts hems remain visible at the side
  관계: the skirt-like front panel → overlaps → the attached shorts.

- 독립 변형 2: two wide trouser legs separate below the shared waist; each has its own broad lower hem
  관계: the wide trouser legs → separate_below → the shared waist and crotch area.

## SF074 · 카프리·페달푸셔

씨앗: 카프리 팬츠 — Capri pants, 페달푸셔 — Pedal pushers

의미: 종아리/무릎아래 상대 밑단과 판매명 중첩을 함께 기록한다.

소유자: same trouser leg hem. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.length` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 고정 cm·필수 slim·얇은 다리·모든 cropped trousers와 합치지 않는다.

관찰 조건: 무릎·발목·밑단 기준이 모두 보임.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: the trouser hems end below the knees; clear ankle gaps separate the hems from the shoes
  관계: the cropped trouser hems → end_below → the knees above clear ankle gaps.

## SF075 · 팔라초·와이드 레그

씨앗: 팔라초 팬츠 — Palazzo pants, 와이드 레그 팬츠 — Wide-leg pants

의미: 넓은 다리통과 허리 아래부터 유연하게 퍼지는 팔라초 실현을 나눈다.

소유자: same trousers width and drape. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 넓음이 반드시 얇고 부드러운 섬유·긴 길이를 뜻하지 않는다.

관찰 조건: 양 다리통, 허리/힙에서의 퍼짐, 처짐을 함께.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134), [Seamwork understanding ease](https://www.seamwork.com/sewing-tutorials/understanding-ease).

- 독립 변형 1: broad trouser legs fall from the waistband in soft folds; their separate hems remain wide
  관계: the broad trouser legs → fall_from → the same waistband in soft folds.

## SF076 · 드로스트링 팬츠

씨앗: 드로스트링 팬츠 — Drawstring pants

의미: 끈이 통과하는 케이싱과 출입구·매듭의 관계.

소유자: same waistband cord and casing. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap_fastener` (existing_candidate_property_family).

혼동 경계: 허리에 놓인 장식 리본·belt와 달리 실제 끈 경로가 필요; 소재·허리 높이는 독립.

관찰 조건: 끈 출발 구멍과 매듭·케이싱 경계.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: a drawcord emerges from two waistband openings; its ends meet in a front waist knot
  관계: the waist drawcord → emerges_from → the waistband casing.

## SF077 · 하이·미드·로라이즈

씨앗: 하이라이즈·하이웨이스트 — High-rise / High-waisted, 미드라이즈 — Mid-rise, 로라이즈 — Low-rise

의미: 허리선 높이는 배꼽·자연허리·골반 기준 관계로, rise 측정은 별도 명세로 둔다.

소유자: same waistband relative to wearer landmarks. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.fit.waistband_landmark` (existing_candidate_property_family).

혼동 경계: high waist는 high-leg·허리 잘록함·배꼽 노출의 동의어가 아니다.

관찰 조건: 밴드 윗선과 대응 신체 기준점이 보여야 한다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seafolly high-leg high-waist bottom](https://sg.seafolly.com/products/jetset-lure-high-leg-high-waist-bikini-bottom-j30196-black).

- 독립 변형 1: the waistband upper edge sits above the navel; the two leg openings remain independently positioned
  관계: the waistband upper edge → sits_above → the navel.

- 독립 변형 2: the waistband upper edge sits below the navel; the upper abdomen remains visible above it
  관계: the waistband upper edge → sits_below → the navel.

## SF078 · 비키니·삼각 패널·스트링

씨앗: 비키니 — Bikini, 트라이앵글 비키니 — Triangle bikini, 스트링 비키니 — String bikini

의미: 분리 구성, 컵 패널 형상, 얇은 연결 끈은 조합 가능한 독립 속성.

소유자: same swim top and separate bottom. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: triangle이 반드시 string은 아니며 bikini가 최소 커버리지·해변 배경을 뜻하지 않는다.

관찰 조건: 두 패널 형상·지지 연결과 상하 분리 경계.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_triangle.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: two triangular swim panels form the top; each upper point joins its own supporting strap
  관계: each triangular swim panel upper point → joins → its supporting strap.

- 독립 변형 2: thin side strings extend from the swim top panels; their ends tie together across the back
  관계: the swim top side strings → tie_to → the same top back strings.

## SF079 · 반도·홀터·롱라인·언더와이어 비키니

씨앗: 반도 비키니 — Bandeau bikini, 홀터 비키니 — Halter bikini, 언더와이어 비키니 — Underwire bikini, 롱라인 비키니 톱 — Longline bikini top

의미: 수평 패널·목 뒤 연결·밑가슴 아래 연장·보강 명세를 분리한다.

소유자: same swim top selected axes. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap` (proposed_family_requires_schema_and_effect_review).

혼동 경계: 반도+halter 공존 가능; wire는 내부 명세여서 컵 아래 선만으로 확정 못함.

관찰 조건: 선택한 패널 경계와 목/밴드 연결이 보이는 시점.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_bandeau.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Wacoal balconette vs demi](https://www.wacoalindia.com/blogs/stories/balconette-vs-demi-cup-choosing-the-right-style-for-you).

- 독립 변형 1: a horizontal swim top band wraps the chest; halter straps rise from its outer edges toward the neck
  관계: the horizontal swim top band → joins → the halter straps at its outer edges.

- 독립 변형 2: the lower swim top band extends below the cup bases; a separate bottom remains below the top hem
  관계: the swim top lower band → extends_below → the cup bases.

## SF080 · 탱키니·원피스 수영복

씨앗: 탱키니 — Tankini, 원피스 수영복 — One-piece swimsuit

의미: 긴 분리 상의의 밑단과 하나로 이어진 몸통-하의 구조.

소유자: same swim garment connectedness. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 탱키니 겹침이 이어진 원피스처럼 보일 수 있으므로 가려진 경계는 미확인.

관찰 조건: 상의 밑단·독립 하의 윗선 또는 연결 몸통의 연속성을 확인.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_tankini, sw_candidate_onepiece.

출처: [Seafolly tankini](https://us.seafolly.com/blogs/sf-world/what-is-a-tankini), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: the long swim top has its own finished hem; that hem overlaps a separate swim bottom waistband
  관계: the tankini top hem → overlaps → the separate swim bottom waistband.

- 독립 변형 2: the swimsuit bodice continues through the waist into its lower brief section; two leg openings belong to the same garment
  관계: the swimsuit bodice → continues_into → the connected lower brief section.

## SF081 · 모노키니 역사·현대 의미

씨앗: 모노키니 — Monokini

의미: 1964 역사형과 현대 컷아웃 원피스 판매 범주를 문맥으로 분리한다.

소유자: same explicitly selected swimsuit design. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 한 단어만으로 topless 역사형을 현대 수영복에 추가하지 않는다; 새 선택형도 보편 정의 아님.

관찰 조건: 현대형은 상하 연결과 컷아웃; 역사형은 명시적인 시대/디자인 요구가 필요.

처리: P0 / split_historical_and_modern_context_before_reuse. 기존 검토 ID: sff_extra_xa005.

출처: [Cupshe Monokini / Cut Out](https://www.cupshe.com/collections/monokini-cut-out), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: a narrow torso panel connects the upper and lower swimsuit sections; side cutouts open on both sides of that connector
  관계: the narrow torso panel → connects → the upper and lower swimsuit sections.

## SF082 · 플런지·백리스 수영복

씨앗: 플런지 원피스 — Plunge one-piece, 백리스 수영복 — Backless swimsuit

의미: 앞의 낮은 파임과 뒤의 넓은 개방은 각각 다른 면의 속성이다.

소유자: same swimsuit front and back boundaries. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.opening_location` (existing_candidate_property_family).

혼동 경계: 한쪽 면만 본 사진으로 반대면의 커버리지를 확정하지 않는다.

관찰 조건: 앞/뒤 따로 보거나 실제 양면 관계가 보이는 사선; 반사 속 소유자도 구별.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: the swimsuit back edge ends below the shoulder blade area; the front panel remains high across the upper chest
  관계: the swimsuit back edge → ends_below → the shoulder blade area.

## SF083 · 하이레그와 높은/낮은 허리선

씨앗: 하이레그·하이컷 — High-leg / High-cut, 하이웨이스트 비키니 — High-waisted bikini, 로라이즈 비키니 — Low-rise bikini

의미: 다리 입구 윗선과 허리 밴드 높이를 별도 기준선으로 기록한다.

소유자: same swim bottom waistband and leg openings. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.leg_opening` (existing_candidate_property_family).

혼동 경계: high-leg+high-waist 공존; high cut의 leg 문맥과 deep neck cut을 분리한다.

관찰 조건: 허리 밴드·다리 입구·골반 기준이 같은 하의에 있어야 함.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_highleg.

출처: [Seafolly high-leg high-waist bottom](https://sg.seafolly.com/products/jetset-lure-high-leg-high-waist-bikini-bottom-j30196-black), [FIT history of women's swimwear](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/).

- 독립 변형 1: the swim bottom waistband sits high on the torso; its leg opening edges independently rise toward the lateral hips
  관계: the leg opening upper edges → rise_toward → the lateral hips beneath a high waistband.

## SF084 · 타이사이드 수영복

씨앗: 타이사이드 — Tie-side

의미: 하의 앞뒤 패널이 옆의 끈 묶음으로 연결되는 경로.

소유자: same swim bottom side closure. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap_fastener` (existing_candidate_property_family).

혼동 경계: 일방·양방 위치를 선택; string 상의와 다른 owner이며 무조건 low-rise 아님.

관찰 조건: 하의 앞뒤 패널에서 매듭으로 이어지는 실제 끝점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Seafolly Brazilian bikini cut](https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut).

- 독립 변형 1: the swim bottom front and back ties meet in a side hip knot; each tie remains attached to its own fabric panel
  관계: the swim bottom front and back ties → meet_in → a side hip knot.

## SF085 · 치키·브라질리언·통·지스트링

씨앗: 치키 — Cheeky, 브라질리언 컷 — Brazilian cut, 통 — Thong, 지스트링 — G-string

의미: 뒤판 폭·하단 좁아짐·끈형 연결은 실제 보이는 형태로 기술한다.

소유자: same swim bottom rear panel. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.coverage.rear_panel` (existing_candidate_property_family).

혼동 경계: 브랜드별 면적 %를 보편화하지 않으며 Brazilian은 착용자 국적 아님; thong footwear 별도.

관찰 조건: 뒤판 양쪽 경계와 폭이 보이는 뒤면; 앞면만으론 미확인.

처리: P0 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly Brazilian bikini cut](https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut), [Havaianas sandals vs flip-flops](https://www.havaianas.com/blogs/news/sandals-vs-flip-flops-what-s-the-difference).

- 독립 변형 1: the swim rear panel narrows toward its lower center; both outer rear garment edges remain visible
  관계: the swim rear panel → narrows_between → the two outer rear garment edges.

- 독립 변형 2: a narrow rear connector joins the waistband to the lower swim panel; the same garment endpoints remain visible
  관계: the narrow rear connector → joins → the waistband to the lower swim panel.

## SF086 · 마이크로 비키니·보이쇼츠 하의

씨앗: 마이크로 비키니·마이크로키니 — Micro bikini / Microkini, 보이쇼츠 수영복 — Boyshort swim bottoms

의미: 작은 패널 면적이라는 비표준 범주와 짧은 다리통 형태를 분리한다.

소유자: same swim panel area and leg sections. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.coverage.leg_opening` (existing_candidate_property_family).

혼동 경계: micro는 정확 cm·몸 확대·필수 특정 부위 노출이 아님; boyshort는 남성/아동 정체성 아님.

관찰 조건: 실제 패널 경계와 다리입구를 확인; 면적은 정량 인증하지 않음.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Seafolly Brazilian bikini cut](https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut).

- 독립 변형 1: the swim bottom extends below the hip crease; two short leg sections end in separate horizontal hems
  관계: the boyshort lower edges → extend_below → the hip crease as two short legs.

- 독립 변형 2: small swim panels connect through thin supporting straps; each panel retains a distinct fabric perimeter
  관계: the small swim panels → connect_through → thin supporting straps around the same torso.

## SF087 · 래시가드·서프수트

씨앗: 래시가드 — Rash guard, 서프수트 — Surf suit

의미: 독립 소매 상의의 밑단과 일체형 몸통/하의 연결을 나눈다.

소유자: same separate or connected swim garment. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 긴소매=UPF 인증·실제 서핑·방수·neoprene·wetness는 아님.

관찰 조건: 소매, 독립 밑단 또는 하부 연결이 보이는 전체 시점.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Lands' End relaxed rash-guard swim tee](https://www.landsend.com/products/womens-long-sleeve-relaxed-upf-50-rash-guard/id_246954), [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit), [Skin Cancer Foundation clothing UPF](https://www.skincancer.org/skin-cancer-prevention/sun-protection/sun-protective-clothing/).

- 독립 변형 1: the sleeved swim top ends at its own hem; a separate swim bottom begins below that edge
  관계: the rashguard torso → ends_at → its own hem above the separate bottom.

- 독립 변형 2: the long-sleeved torso continues into the lower swim section; the same garment has two leg openings
  관계: the surf suit torso → continues_into → the connected lower swim section.

## SF088 · 스윔쇼츠·보드쇼츠

씨앗: 스윔쇼츠 — Swim shorts, 보드쇼츠 — Board shorts

의미: 수영 용도의 바지통 형상과 여유·여밈을 표현한다.

소유자: same loose swim shorts. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.fit` (proposed_family_requires_schema_and_effect_review).

혼동 경계: board shorts가 전부 무릎길이·내장 liner·특정 섬유·남성을 뜻하지 않는다.

관찰 조건: 분리된 양 다리통과 허리·밑단 관계.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Billabong women's swim and board shorts](https://www.billabong.com/collections/womens-swim-boardshorts), [Simplicity S8134 culottes trousers shorts](https://simplicity.com/simplicity/pds8134).

- 독립 변형 1: loose shorts legs hang below the swim waistband; both separate hems have visible ease around the thighs
  관계: the loose shorts legs → hang_below → the swim waistband.

## SF089 · 스윔스커트·스윔드레스

씨앗: 스윔스커트 — Swim skirt, 스윔드레스 — Swim dress

의미: 수영복 하의에 연결된 skirt 덮개와 상체까지 이어진 dress 외관을 나눈다.

소유자: same skirt overlay and swim layer. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: 일반 sundress나 분리 sarong을 연결 수영복으로 오인하지 않는다.

관찰 조건: skirt와 하부 swim layer의 실제 이어짐/분리 경계를 볼 수 있어야 함.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Swimsuits For All swimdress with attached shorts](https://www.swimsuitsforall.com/products/swimdress-with-attached-swim-shorts/1065683.html), [Billabong women's swim and board shorts](https://www.billabong.com/collections/womens-swim-boardshorts).

- 독립 변형 1: a short skirt overlay attaches to the swim bottom waistband; the connected lower swim layer remains visible beneath it
  관계: the short skirt overlay → attaches_to → the same swim bottom waistband.

## SF090 · 부르키니의 층 구성

씨앗: 부르키니 — Burkini / Burqini

의미: 머리·소매·몸통·다리 덮개와 부착/분리 경로를 선택형으로 기록한다.

소유자: same covered swim ensemble. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: 3-piece·헐렁함·특정 종교·국적·연령·UPF를 자동 부여하지 않는다.

관찰 조건: 후드/머리덮개 연결·상의 밑단·바지 경계를 전체 시점에서 본다.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Ahiida Sportz-Fit Burqini](https://ahiida.com/product/sz-ultramarine-black-spliced/).

- 독립 변형 1: the head covering connects to the long-sleeved upper garment; separate full-length swim trousers continue below the top
  관계: the swim head covering → connects_to → the long-sleeved upper garment.

## SF091 · 커버업·카프탄·튜닉·비치 셔츠·로브

씨앗: 커버업 — Cover-up, 카프탄·카프탄 드레스 — Kaftan / Caftan, 튜닉 — Tunic, 비치 셔츠 — Beach shirt, 비치 로브 — Beach robe

의미: 커버업은 용도이며 몸판 길이·앞여밈·소매·밑단이 실제 형태다.

소유자: same outer garment over swimwear. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: kaftan의 문화 복식 전체를 beach loose dress로 축소하지 않는다; sheer/wet 자동 추가 없음.

관찰 조건: 겉층 가장자리와 안쪽 수영복이 같은 착용자에게 연결됨.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: sw_candidate_coverup.

출처: [Seafolly resort cover ups](https://us.seafolly.com/collections/kaftans-cover-ups), [Ahiida Sportz-Fit Burqini](https://ahiida.com/product/sz-ultramarine-black-spliced/).

- 독립 변형 1: open outer shirt panels frame the swimsuit underneath; the shirt has its own collar and finished hem
  관계: the open outer shirt panels → frame → the swimsuit underneath.

- 독립 변형 2: a loose tunic hem hangs over the separate swim bottom; its broad body falls from the shoulders
  관계: the loose tunic hem → hangs_over → the separate swim bottom.

## SF092 · 섬유·브랜드·조성

씨앗: 코튼·면 — Cotton, 리넨·린넨 — Linen, 레이온·비스코스 — Rayon / Viscose, 라이오셀 — Lyocell, 모달 — Modal, 텐셀 — TENCEL™, 엘라스테인·스판덱스 — Elastane / Spandex, 나일론·폴리에스터 — Nylon / Polyester

의미: cotton/linen은 섬유, rayon/viscose/modal/lyocell은 재생 셀룰로오스 계열, TENCEL은 브랜드; nylon/polyester/elastane은 별도 조성 축이다.

소유자: same textile material specification. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material` (existing_candidate_property_family).

혼동 경계: 브랜드와 일반 섬유를 합치지 않는다; 같은 섬유가 다양한 weave/knit/finish에 사용됨. 사진은 정확 혼방·브랜드·친환경 성능을 입증하지 못한다.

관찰 조건: 비시각 명세로 보존; 필요한 표면·처짐·투과만 별도 가시 후보에서 선택.

처리: P1 / preserve_specification_no_automatic_pixel_candidate. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [Lenzing TENCEL brand portfolio](https://www.lenzing.com/products/brands/tenceltm/), [LYCRA quality FAQ](https://one.lycra.com/en/lycra-frequently-asked-questions/quality-lycra), [REI breathable fabrics](https://www.rei.com/learn/expert-advice/how-to-pick-the-most-breathable-fabrics.html), [Fashion Fabrics Club fabric glossary](https://fashionfabricsclub.com/pages/fabric-glossary).

명세/물품 유형을 보존하되 이번에는 자동 픽셀 후보를 만들지 않는다. 별도 관찰 가능한 물품 시점이 필요한 경우 후속 승격에서 작성한다.

## SF093 · 포플린·론·보일·거즈·더블거즈·시어서커

씨앗: 포플린 — Poplin, 론 — Lawn, 보일 — Voile, 거즈 — Gauze, 더블 거즈 — Double gauze, 시어서커 — Seersucker

의미: 미세하고 비교적 매끈한 원단, 성긴 원단, 겹친 거즈와 반복 puckering을 분리한다.

소유자: same light fabric structure. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.visible_weave` (existing_candidate_property_family).

혼동 경계: 가벼움=투명함 아님; seersucker의 반복 요철을 무작위 착용 구김이나 shirring 봉제 줄로 대체하지 않는다.

관찰 조건: 매끈함/구멍/겹수/요철 각각 적절한 근접 해상도; 숨은 double layer는 미확인.

처리: P0 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [Seamwork guide to shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring).

- 독립 변형 1: small raised puckered bands alternate with flatter woven bands; the pattern repeats across the same fabric
  관계: the seersucker raised bands → alternate_with → flatter woven bands.

- 독립 변형 2: a fine voile layer hangs in light folds; a faint inner garment outline is visible through the continuous weave
  관계: the fine voile layer → transmits → a faint inner garment outline.

## SF094 · 샴브레이·데님

씨앗: 샴브레이 — Chambray, 데님 — Denim

의미: 평직의 색실 혼합과 데님의 능직 사선 표면을 나눈다.

소유자: same woven fabric surface. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.visible_weave` (existing_candidate_property_family).

혼동 경계: 파란 색 하나로 denim을 확정하지 않으며 chambray를 모든 denim과 동일시하지 않는다.

관찰 조건: 실 방향이 분해되는 원해상도 근접면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between).

- 독립 변형 1: fine diagonal yarn ridges cross the denim surface; the ridges continue through the fabric folds
  관계: the visible diagonal yarn ridges → cross → the denim fabric surface.

## SF095 · 시폰·조젯·오간자

씨앗: 시폰 — Chiffon, 조젯 — Georgette, 오간자 — Organza

의미: 가볍게 흐르는 투과면, 잔 크레이프 표면, 얇지만 형태를 지탱하는 부피의 차이를 다룬다.

소유자: same sheer fabric drape. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.drape` (existing_candidate_property_family).

혼동 경계: 세 판매명을 전부 동일한 흐르는 silk로 병합하지 않는다; 섬유 조성·정확 weave는 별도.

관찰 조건: 처짐과 실제 주름 면·비침을 비교할 근접 사선.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Fashion Fabrics Club fabric glossary](https://fashionfabricsclub.com/pages/fabric-glossary).

- 독립 변형 1: thin translucent folds hold away from the garment underneath; sharp fold edges maintain a light structured volume
  관계: the thin organza folds → hold_away_from → the covered garment underneath.

## SF096 · 새틴 조직과 광택

씨앗: 새틴 — Satin

의미: 조직 이름과 매끈한 광택의 시각 표현을 나눈다.

소유자: same fabric face. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material` (existing_candidate_property_family).

혼동 경계: satin=실크·젖음·vinyl이 아니며 광택만으로 새틴 조직을 확정하지 않는다. satin/sateen 용어 경계는 기술 문헌과 현대 판매 문맥마다 달라 별도 provenance가 필요하다.

관찰 조건: 연속 하이라이트와 접힘 변화; exact weave는 근접 결 증거가 별도로 필요.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Fashion Fabrics Club fabric glossary](https://fashionfabricsclub.com/pages/fabric-glossary), [Mood polyester charmeuse](https://www.moodfabrics.com/collections/polyester-charmeuse-fashion-fabrics?limit=90).

- 독립 변형 1: the smooth fabric face carries broad highlights; the highlights change gently across the soft folds
  관계: the smooth fabric face → carries → broad highlights along the folds.

## SF097 · 저지·리브·테리

씨앗: 저지 — Jersey, 리브·골지 — Rib knit, 테리 — Terry

의미: 편직 고리면, 반복 골, 표면 pile loop를 각각 기록한다.

소유자: same knitted surface. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.visible_weave` (existing_candidate_property_family).

혼동 경계: rib의 줄무늬와 인쇄 stripe는 다르고 terry가 반드시 젖은 수건은 아니다.

관찰 조건: 골·고리가 분해되는 근접 해상도.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: raised knit columns alternate with recessed columns; the vertical rib texture follows the same top folds
  관계: the rib knit raised columns → alternate_with → recessed knitted columns.

- 독립 변형 2: small pile loops project from the fabric face; their repeated looped texture remains visible in the light
  관계: small pile loops → project_from → the same terry fabric face.

## SF098 · 메시·튤·레이스·아일렛·브로드리·오픈니트

씨앗: 메시 드레스 — Mesh dress, 메시 — Mesh, 튤 — Tulle, 레이스 — Lace, 아일렛 — Eyelet, 브로드리 앙글레즈 — Broderie anglaise, 오픈 니트 — Open knit

의미: 규칙 망눈, 장식 고리무늬, 바탕천에 자수 마감 구멍, 성긴 knit를 독립 형태로 둔다.

소유자: same perforated or openwork material. 제안 슬롯: `surface_material`. 속성 가족: `wardrobe.material.visible_weave` (existing_candidate_property_family).

혼동 경계: eyelet은 hardware 고리도 될 수 있어 문맥 구분; tulle의 layer volume와 한겹 transmission은 별도.

관찰 조건: 실·바탕천·구멍·마감 경계가 원해상도에서 구별돼야 함.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: broderie_anglaise_eyelet.

출처: [Seamwork cotton fabric guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Fashion Fabrics Club fabric glossary](https://fashionfabricsclub.com/pages/fabric-glossary).

- 독립 변형 1: embroidered edges surround small holes in a woven base cloth; intact fabric separates the openings
  관계: the embroidered hole edges → surround → small openings in the woven base cloth.

- 독립 변형 2: fine net threads enclose repeated openings; an opaque inner garment remains behind the net layer
  관계: fine net threads → enclose → repeated mesh openings.

## SF099 · 개더·루싱

씨앗: 개더 — Gather, 루싱 — Ruching

의미: 긴 원단의 모음과 국소 장식 주름이 어느 봉제/끈으로 모이는지 지정한다.

소유자: same locally gathered garment panel. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 제조사 glossary에서 ruching을 gathering으로 설명하므로 억지 배타 범주로 만들지 않는다; 무작위 wrinkles와 다름.

관찰 조건: 모이는 시작/끝, 실제 봉제선과 주름 방향.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seamwork guide to shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring).

- 독립 변형 1: small bodice folds converge into a side gathering seam; the surrounding fabric remains part of the same panel
  관계: small bodice folds → converge_into → the same side gathering seam.

## SF100 · 러플·프릴·플라운스

씨앗: 러플·프릴 — Ruffle / Frill, 플라운스 — Flounce

의미: 부착선에 모음이 있는 장식과 모음 없이 하단 폭이 커지는 곡선 재단의 차이.

소유자: same attached trim edge. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: 판매명 flounce가 넓은 ruffle 가족에 속할 수 있음; 두 구조를 한 번에 의무화하지 않는다.

관찰 조건: 부착선의 gathers 여부와 free edge 폭을 확인.

처리: P1 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct065_v1, clt_ct065_v2.

출처: [Threads geometric flounces](https://www.threadsmagazine.com/2020/02/19/how-to-sew-geometric-flounces), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: small gathers run along the trim attachment edge; its loose outer edge ripples below the neckline seam
  관계: the gathered trim attachment edge → joins → the same neckline seam.

- 독립 변형 2: a smooth flounce edge joins the skirt seam; its wider free edge falls in curved waves below it
  관계: the smooth flounce attachment edge → joins → the same skirt seam.

## SF101 · 프린지·태슬·스캘럽

씨앗: 프린지 — Fringe, 태슬 — Tassel, 스캘럽 에지 — Scalloped edge

의미: 여러 늘어진 가닥, 묶인 술, 반복 곡선 가장자리의 형태를 나눈다.

소유자: same garment edge ornament. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure` (existing_candidate_property_family).

혼동 경계: fringe는 머리 앞머리 다의어, scallop은 조개 생물과 분리한다.

관찰 조건: 가닥 부착점·묶임·실제 원단 끝을 근접 확인.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [V&A paisley and India](https://www.vam.ac.uk/dundee/articles/a-long-way-from-home-the-paisley-pattern-and-india).

- 독립 변형 1: separate fringe strands hang from the garment hem; their upper ends attach along the finished edge
  관계: the fringe strands → hang_from → the same garment hem.

- 독립 변형 2: repeated rounded fabric lobes form the hem edge; each curve belongs to the continuous garment fabric
  관계: the repeated rounded fabric lobes → form → the same scalloped hem edge.

## SF102 · 레이스업·멀티스트랩·링·매듭

씨앗: 레이스업 — Lace-up, 멀티스트랩·스트래피 — Multi-strap / Strappy, 링 디테일 — Ring detail, 노티드 디테일 — Knotted detail

의미: 끈 통과 구멍·교차 경로·고리 연결·실제 매듭은 다른 그래프다.

소유자: same garment connection hardware. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.structure.strap_fastener` (existing_candidate_property_family).

혼동 경계: lace fabric과 lace-up, 주얼리 ring과 garment connector를 구별. metal이 실제 폭력/구속을 요구하지 않는다.

관찰 조건: 모든 연결 끝점과 끈 owner가 보이는 근접면.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know), [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit).

- 독립 변형 1: one cord passes through opposing eyelet rows; crossed cord spans join the two garment edges
  관계: the garment lacing cord → passes_through → opposing rows of eyelets.

- 독립 변형 2: a connector ring joins two fabric strap ends; both fabric ends visibly loop around that ring
  관계: the connector ring → joins → two fabric strap ends of the same garment.

## SF103 · 디스트레스드·스터드

씨앗: 디스트레스드 — Distressed, 스터드 — Studs

의미: 의도적으로 해진 듯한 경계와 부착된 금속 장식을 관찰한다.

소유자: same garment surface treatment. 제안 슬롯: `garment_detail`. 속성 가족: `wardrobe.material` (existing_candidate_property_family).

혼동 경계: 프린트 찢김·원단 구멍·실제 부상·폭력 맥락을 분리; studs가 spikes나 무기와 같지 않다.

관찰 조건: 해진 섬유끝 또는 stud 부착점이 보이는 원해상도.

처리: P1 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [V&A Vivienne Westwood](https://www.vam.ac.uk/collections/vivienne-westwood), [Threads sewing glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

- 독립 변형 1: frayed threads project from the fabric opening; intact woven cloth borders the worn edge
  관계: the frayed edge threads → project_from → a worn fabric opening.

- 독립 변형 2: small studs attach along the garment edge; their raised metal-like heads cast short local shadows
  관계: small studs → attach_along → the garment edge.

## SF104 · 깅엄·브르통/마린 줄무늬

씨앗: 깅엄 — Gingham, 브르통·마린 스트라이프 — Breton / Nautical stripe

의미: 교차 격자와 수평 stripe의 반복 주기·방향을 나눈다.

소유자: same garment repeating pattern. 제안 슬롯: `color`. 속성 가족: `wardrobe.pattern` (existing_candidate_property_family).

혼동 경계: 체크가 모두 gingham 아님; Breton의 과거 줄 수를 현대 모든 의복에 강제하지 않는다.

관찰 조건: 직물 주름 따라 왜곡되는 무늬의 반복을 확인.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Saint James Breton shirt history](https://us.saint-james.com/pages/our-history), [Liberty print collections](https://www.libertylondon.com/uk/features/craft/about-liberty-fabrics-collections.html).

- 독립 변형 1: small crossing bands form a repeated two-color check; the checks continue across the fabric folds
  관계: the small crossing bands → form → a repeated two-color check on the same fabric.

- 독립 변형 2: horizontal contrasting bands repeat across the shirt torso; the bands bend with the garment folds
  관계: horizontal contrasting bands → repeat_across → the same shirt torso.

## SF105 · 꽃 크기·식물·열대·페이즐리·도트

씨앗: 디치 플로럴 — Ditsy floral, 라지 스케일 플로럴 — Large-scale floral, 보태니컬 프린트 — Botanical print, 페이즐리 — Paisley, 폴카도트 — Polka dots

의미: 모티프 종류, 크기, 밀도와 반복 방향을 각각 기록한다.

소유자: same fabric motif field. 제안 슬롯: `color`. 속성 가족: `wardrobe.pattern` (existing_candidate_property_family).

혼동 경계: floral과 botanical 중첩 허용; tropical이 실제 tropical location을 추가하지 않음; paisley 문화와 착용자 출신을 분리.

관찰 조건: 꽃/잎 형태와 원단 기준 반복 규모가 식별되어야 함.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Liberty print collections](https://www.libertylondon.com/uk/features/craft/about-liberty-fabrics-collections.html), [V&A paisley and India](https://www.vam.ac.uk/dundee/articles/a-long-way-from-home-the-paisley-pattern-and-india), [Fashion Fabrics Club fabric glossary](https://fashionfabricsclub.com/pages/fabric-glossary).

- 독립 변형 1: tiny floral motifs repeat densely across the garment panels; each motif stays small relative to the bodice width
  관계: tiny floral motifs → repeat_densely_across → the same garment panels.

- 독립 변형 2: large leaf motifs span broad areas of the garment panels; the repeat remains tied to the fabric surface
  관계: large leaf motifs → span → broad areas of the same garment panels.

## SF106 · 타이다이·색면·모노크롬·파스텔·네온·메탈릭

씨앗: 타이다이 — Tie-dye, 컬러블로킹 — Color blocking, 모노크롬 — Monochrome, 파스텔 — Pastel, 네온 — Neon, 메탈릭 — Metallic

의미: 불규칙 번짐, 경계 분명한 색면, 유사색 구성, 명도/채도, 반사는 독립 축이다.

소유자: same garment color and finish. 제안 슬롯: `color`. 속성 가족: `wardrobe.color` (existing_candidate_property_family).

혼동 경계: tie-dye 제조 이력·neon 실제 발광·metallic 실제 금속 원료를 이미지로 확정하지 않는다.

관찰 조건: 색면 경계·명도·반사 위치를 확인하고 white balance 영향을 기록.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Liberty print collections](https://www.libertylondon.com/uk/features/craft/about-liberty-fabrics-collections.html), [Cotton Incorporated textile weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf).

- 독립 변형 1: two contrasting color fields meet at a clear garment boundary; each field remains continuous within its panel
  관계: two contrasting color fields → meet_at → a clear boundary on the same garment.

- 독립 변형 2: soft irregular color patches spread across the fabric surface; blurred color transitions follow the cloth folds
  관계: soft irregular color patches → spread_across → the same fabric surface.

## SF107 · 리조트·비치·마린·코스털 그랜드마더

씨앗: 리조트웨어 — Resortwear, 비치웨어 — Beachwear, 노티컬·마린 룩 — Nautical / Marine look, 코스털 그랜드마더 — Coastal grandmother

의미: 용도와 비공식 연상군은 의복의 구조·색·레이어 후보를 묶는 문맥이다.

소유자: same optional outfit components. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: grandmother는 나이·혈연이 아니며 resort/nautical이 해변·요트·계층을 강제하지 않는다.

관찰 조건: 선택된 옷의 요소만 확인; 장소·연령·생활습관은 독립 요청.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Seafolly resort cover ups](https://us.seafolly.com/collections/kaftans-cover-ups), [Saint James Breton shirt history](https://us.saint-james.com/pages/our-history), [Bazaar A-Z microtrends](https://www.harpersbazaar.com/fashion/trends/a65784060/a-z-micro-trends-defined/).

- 독립 변형 1: a light roomy shirt layers over a simple sleeveless top; straight trousers continue below the shirt hem
  관계: the light outer shirt → layers_over → the simple sleeveless top.

## SF108 · 보호·코티지·코케트·발레코어

씨앗: 보호·보헤미안 — Boho / Bohemian, 코티지코어 — Cottagecore, 코케트 — Coquette, 발레코어 — Balletcore

의미: 자수·작은 무늬·리본·랩 형태 등 선택한 단서를 조합한다.

소유자: same selected outfit adornments. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: style label이 나이·성적 의도·전원 장소·전부 pink/puff인 all-of 묶음을 만들지 않는다.

관찰 조건: 실제로 선택한 장식의 의복 부착과 층 연결만 확인.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Burda 6502 peasant blouses](https://simplicity.com/burda-style/bur6502), [Vogue aesthetics of 2023](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [Bazaar A-Z microtrends](https://www.harpersbazaar.com/fashion/trends/a65784060/a-z-micro-trends-defined/).

- 독립 변형 1: small ribbon bows attach at the blouse neckline; a soft wrap skirt overlaps at the waist
  관계: small ribbon bows → attach_at → the same blouse neckline.

## SF109 · Y2K·머메이드코어·코스털 카우걸·토마토 걸

씨앗: Y2K, 머메이드코어 — Mermaidcore, 코스털 카우걸 — Coastal cowgirl, 토마토 걸 — Tomato girl

의미: 시대 연상·물빛 표면·웨스턴 혼합·여름 색채는 별개 스타일 문맥이다.

소유자: same optional fashion realization. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: Y2K=whale tail 필수 아님; mermaidcore=꼬리 아님; cowgirl 직업·tomato 실제 식물·girl 나이를 추론하지 않는다.

관찰 조건: 선택한 신발/허리띠/색/장식만 이미지에서 확인.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Vogue aesthetics of 2023](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [Vogue tomato girl summer](https://www.vogue.com/article/kendall-jenner-model-tomato-girl-summer-trend), [Bazaar A-Z microtrends](https://www.harpersbazaar.com/fashion/trends/a65784060/a-z-micro-trends-defined/).

- 독립 변형 1: a western belt sits over the light dress waist; cowboy-style boots remain separate footwear below the hem
  관계: the western belt → sits_over → the waist of the light summer dress.

- 독립 변형 2: pearl-like embellishments attach to sea-colored fabric; soft iridescent highlights follow the garment folds
  관계: the pearl-like embellishments → attach_to → the sea-colored fabric surface.

## SF110 · 테니스·애슬레저·고프·블록코어

씨앗: 테니스코어 — Tenniscore, 애슬레저 — Athleisure, 고프코어 — Gorpcore, 블록코어 — Blokecore

의미: 스포츠 의복의 외형·야외 장비·축구 저지 활용을 일상 옷과 조합한 용도군.

소유자: same sports-inspired outfit. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: 실제 운동·팀 소속·성별·기능 성능·야외 배경을 이름만으로 강제하지 않는다.

관찰 조건: selected polo/pleated/skort/jersey/utility 등의 실제 형태만.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Bazaar A-Z microtrends](https://www.harpersbazaar.com/fashion/trends/a65784060/a-z-micro-trends-defined/), [Seafolly fit guide](https://us.seafolly.com/blogs/sf-world/your-guide-to-find-the-perfect-fit).

- 독립 변형 1: the sports jersey has a loose short-sleeved body; its hem rests above a separate denim waistband
  관계: the sports jersey hem → rests_above → the separate denim waistband.

## SF111 · 콰이어트 럭셔리·란제리 드레싱·서머 고스·펑크

씨앗: 콰이어트 럭셔리 — Quiet luxury, 란제리 드레싱 — Lingerie dressing, 서머 고스 — Summer goth, 펑크 룩 — Punk look

의미: 로고 절제·이너 유래 구조·검정 가벼운 레이어·재조합이라는 선택 문맥.

소유자: same selected visible style treatment. 제안 슬롯: `wardrobe_style`. 속성 가족: `wardrobe.layers` (existing_candidate_property_family).

혼동 경계: quiet luxury가 실제 가격·재력·브랜드 보증을 뜻하지 않는다. black·mesh·chain은 공격성·강요·폭력 증거 아님.

관찰 조건: 선택한 재단·표면·레이어를 관찰; 심리·경제 상태는 평가하지 않음.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [V&A Vivienne Westwood](https://www.vam.ac.uk/collections/vivienne-westwood), [Vogue aesthetics of 2023](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [Bazaar sheer clothing](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

- 독립 변형 1: a black openwork layer lies over an opaque inner dress; the airy outer holes reveal the covered inner layer
  관계: the black openwork layer → lies_over → the same opaque inner dress.

## SF112 · 슬라이드·통·스트래피·피셔맨 샌들

씨앗: 슬라이드 — Slides, 플립플롭·통 샌들 — Flip-flops / Thong sandals, 스트래피 샌들 — Strappy sandals, 피셔맨 샌들 — Fisherman sandals

의미: 발등 band, toe-post Y, 여러 가는끈, cage형 교차띠의 실제 연결을 분리한다.

소유자: same shoe strap network. 제안 슬롯: `footwear`. 속성 가족: `wardrobe.footwear.sandal_strap_paths` (existing_candidate_property_family).

혼동 경계: thong은 여기서 속옷이 아님; fisherman이 직업·낚시 장면을 만들지 않는다.

관찰 조건: 발가락 사이 기둥·발등 띠·밑창 연결을 각각 확인.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: fisherman_sandals.

출처: [Havaianas sandals vs flip-flops](https://www.havaianas.com/blogs/news/sandals-vs-flip-flops-what-s-the-difference), [Camper Brutus fisherman sandals](https://www.camper.com/en_US/men/shoes/brutus/camper-brutus_sandal-K100778-006).

- 독립 변형 1: a Y-shaped sandal strap passes between the first and second toes; its side ends join the same sole
  관계: the Y-shaped sandal strap → passes_between → the first and second toes.

- 독립 변형 2: interlaced sandal bands span the instep; their ends attach along both sides of the sole
  관계: the interlaced sandal bands → span → the same foot instep.

## SF113 · 에스파드리유·웨지·플랫폼·뮬·스포츠 샌들

씨앗: 에스파드리유 — Espadrilles, 웨지 — Wedge, 플랫폼 샌들 — Platform sandals, 뮬 — Mules, 스포츠 샌들 — Sport sandals

의미: 밑창 둘레 질감, 연결된 쐐기 굽, 앞발 포함 높이, 뒤꿈치 개방, 조절끈은 조합 축이다.

소유자: same shoe sole and heel topology. 제안 슬롯: `footwear`. 속성 가족: `wardrobe.footwear.backless_vs_strapped` (existing_candidate_property_family).

혼동 경계: wedge+platform 공존 가능; mule의 앞코는 열리거나 닫힘; rope질감이 황마 인증은 아님.

관찰 조건: 옆면에서 앞발과 뒤꿈치 높이, 밑창·뒤끈을 확인.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Castañer espadrille atelier](https://castaner.com/en-gr/pages/atelier), [Havaianas sandals vs flip-flops](https://www.havaianas.com/blogs/news/sandals-vs-flip-flops-what-s-the-difference).

- 독립 변형 1: the sole forms one continuous wedge between forefoot and heel; braided rope-like bands wrap its outer edge
  관계: the wedge sole → forms_one_continuous_mass_between → the forefoot and heel.

- 독립 변형 2: the shoe has an open back around the heel; the covered forefoot rests on a low sole
  관계: the open shoe back → leaves_unenclosed → the heel.

## SF114 · 젤리 슈즈·메시 플랫

씨앗: 젤리 슈즈 — Jelly shoes, 메시 플랫 — Mesh flats

의미: 성형된 jelly-shoe 갑피와 망눈을 가진 mesh-flat 갑피를 나누고 각 부위의 광학 투과는 독립적으로 기록한다.

소유자: same shoe upper optical surface. 제안 슬롯: `footwear`. 속성 가족: `wardrobe.material.transmission` (existing_candidate_property_family).

혼동 경계: 젤리 질감은 젤리 음식·젖음 아님; mesh 구멍을 투명 고체로 대체하지 않는다. jelly 이름만으로 투과를 의무화하지 않으며 mesh upper와 opaque knit toe도 공존한다.

관찰 조건: 갑피 가장자리·망눈·밑창의 연결이 보이는 근접면.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Melissa adult jelly-shoe collection](https://www.shopmelissa.com/collections/adult-shoes?page=17), [Rothy's Max Square Ballerina Clover Mesh](https://rothys.com/products/womens-max-square-ballerina-clover-mesh), [CottonWorks single and double knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/).

- 독립 변형 1: a molded translucent upper joins a low sole; the covered foot is faintly visible through the solid upper
  관계: the molded translucent upper → joins → the same low shoe sole.

- 독립 변형 2: a fine mesh upper covers the foot; repeated net openings remain visible above the flat sole
  관계: the fine mesh upper → covers → the foot above the same flat sole.

- 독립 변형 3: an opaque molded upper joins the low sole; its solid panels retain distinct edges around the foot opening
  관계: the opaque molded shoe upper → joins → the same low shoe sole.

## SF115 · 스트로 햇·버킷·바이저

씨앗: 스트로 햇 — Straw hat, 버킷햇 — Bucket hat, 바이저 — Visor

의미: 짜임 소재, 아래로 내려간 둘레챙, 머리윗부분 열린 visor는 별개 축.

소유자: same headwear crown and brim. 제안 슬롯: `wearable_accessory`. 속성 가족: `wardrobe.accessories` (existing_candidate_property_family).

혼동 경계: straw가 반드시 wide-brim은 아니며 visor가 full crown/UPF/스포츠 행동을 뜻하지 않는다.

관찰 조건: 챙·크라운의 실제 연결과 머리윗부분 덮임.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Nike Ace visor](https://www.nike.com/t/ace-dri-fit-visor-NHd8Qj), [Skin Cancer Foundation clothing UPF](https://www.skincancer.org/skin-cancer-prevention/sun-protection/sun-protective-clothing/).

- 독립 변형 1: the visor brim projects from a head band; the top of the head remains uncovered
  관계: the visor brim → projects_from → a head band below an open crown.

## SF116 · 라피아·바스켓 백·헤드스카프

씨앗: 라피아 백 — Raffia bag, 바스켓 백 — Basket bag, 헤드스카프 — Headscarf

의미: 원료 명칭·바구니 구조와 머리에 둘러 묶은 천을 분리한다.

소유자: same bag structure or separate head wrap. 제안 슬롯: `wearable_accessory`. 속성 가족: `wardrobe.accessories` (existing_candidate_property_family).

혼동 경계: raffia-like synthetic 가능; basket은 원료 아님; headscarf가 religion·nationality를 결정하지 않는다.

관찰 조건: 가방 짜임·handle 연결 또는 머리 천의 knot/끝점.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [LOEWE baskets and raffia bags](https://www.loewe.com/usa/en/women/bags/baskets), [Free People scarves and bandanas](https://www.freepeople.com/scarves/).

- 독립 변형 1: woven handles join a basket-like bag body; crossing strips form the bag surface
  관계: the woven bag handles → join → the same basket-like bag body.

- 독립 변형 2: a cloth scarf wraps around the head; its two ends tie at the back
  관계: the headscarf ends → tie_at → the back of the same head.

## SF117 · 셸·비즈 주얼리·앵클릿

씨앗: 셸 주얼리 — Shell jewelry, 비디드 주얼리 — Beaded jewelry, 앵클릿 — Anklet

의미: 조개 모티프, 구슬 연결, 발목 위치는 소재·형태·착용위치라는 다른 축이다.

소유자: same wearable ornament. 제안 슬롯: `wearable_accessory`. 속성 가족: `wardrobe.accessories` (existing_candidate_property_family).

혼동 경계: shell/pearl 외형은 생물 재료·진품 인증이 아니고 anklet은 body chain 전체와 다름.

관찰 조건: 구슬과 끈·chain 연결 또는 발목 둘레 부착이 식별됨.

처리: P2 / review_equivalents_then_add_or_extend_visible_variant. 기존 검토 ID: 행별 lexical neighbor를 검토한 뒤 결정.

출처: [Smithsonian NMAfA anklet 99-26-4](https://africa.si.edu/collection/object/nmafa_99-26-4).

- 독립 변형 1: a fine chain encircles the ankle above the shoe; small connected beads follow its curve
  관계: the anklet chain → encircles → the same ankle above the shoe.

## SF118 · 웨이스트·벨리·보디 체인

씨앗: 웨이스트 체인·벨리 체인 — Waist / Belly chain, 보디 체인 — Body chain

의미: 허리 둘레 체인과 목/가슴/허리/등 연결망의 경로를 별개로 다룬다.

소유자: same chain ornament network on wearer. 제안 슬롯: `wearable_accessory`. 속성 가족: `wardrobe.accessories` (existing_candidate_property_family).

혼동 경계: 장신구 chain이 의복 지지끈·body pose·결박 관계로 바뀌지 않도록 owner를 둔다.

관찰 조건: 체인 연결·경로·겉옷 앞뒤 층 순서가 보이는 시점.

처리: P0 / reuse_meaning_review_relation_and_effect_scope. 기존 검토 ID: clt_ct113_v2.

출처: [Jennifer Zeuner Lala Body Chain](https://jenniferzeuner.com/products/lala-body-chain), [V&A Vivienne Westwood](https://www.vam.ac.uk/collections/vivienne-westwood).

- 독립 변형 1: a fine waist chain encircles the abdomen; it remains separate from the lower waistband
  관계: the waist chain → encircles → the abdomen above the lower waistband.

- 독립 변형 2: a center ornament chain connects the neck chain to the waist chain; all three chains belong to the same body accessory
  관계: the ornament center chain → connects → the neck chain to the waist chain.

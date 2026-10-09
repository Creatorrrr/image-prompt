# 여름 패션: 시각 의미·후보 데이터 강화 리서치와 반영 계획

2026-10-09 KST. 기준 대화: [여름 패션 용어 조사](chatgpt-conversation://6ac7dd4a-cb28-83e8-9f3a-29b08702b631).

여름 패션은 **의복 종류, 연결 구조, 핏, 길이, 개구부 위치, 앞뒤 커버리지, 원단 투과, 층 순서, 장식·무늬, 착장 스타일**을 조합하는 데이터로 강화하는 것이 적합하다. 핵심은 이름을 늘리는 것보다 **같은 의복의 어느 부분이 무엇과 연결되고, 어떤 경계 사이에서 무엇이 실제로 보이는지**를 표현하는 것이다. 크롭·홀터·하이레그·시어는 서로 다른 속성이므로 하나의 노출 정도 축으로 합치면 원문의 구분을 잃는다. 이 분해는 원문과 제작자·기관·브랜드의 설명을 바탕으로 한 연구 설계다. [Seamwork의 랩형 몸판](https://www.seamwork.com/pdf-sewing-patterns/posie-surplice-wrap-dress), [Seafolly의 수영복 구성](https://us.seafolly.com/blogs/sf-world/what-is-a-tankini).

조사 결과는 **원문 용어 299행, 공개 출처 68개, 의미 카드 118개, 후보 문장 초안 166개**다. 구현을 위한 비교 사례 57개, 정상 동시 조합 16개, 변경 반례 15개, 이미지 검증 묶음 18개도 작성했다. 166개는 신규 런타임 엔트리 수가 아니다. 이미 있는 의미의 재사용, 관계·효과 범위 보강, 새 가시 변형 검토를 위한 선택형 초안이다.

## 1. 범위와 원문 확보

참조 대화는 17절로 구성된다. 1~15절의 24개 용어 표에 299행이 있고, 16절에는 신체 부위별 연결 15개, 17절에는 조합 예시 7개가 있다. 행 안의 여러 한국어·영어 별칭은 중복 집계하지 않았다.

read_thread의 assistant 본문은 20,000자에서 잘렸다. 공식 ChatGPT 브라우저의 실제 제목·본문·표를 추가 확인해 전체 용어 행을 확보했다. [씨앗 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/seed-terms.txt)은 완전한 표의 용어 라벨 목록이고, [API 스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/reference-api-snapshot.json)은 일부 본문이다. 둘을 완전한 원문 아카이브라고 혼동하지 않는다. [신체 부위·원문 조합과 취득 한계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/reference-cross-links.json)에 취득 범위를 기록했다.

가슴·몸매 강조, 쇄골·겨드랑이·복부·배꼽·허벅지·등·골반·엉덩이 커버리지, 란제리·수영복·국소 커버 제품을 포함했다. sideboob, underboob, whale tail, braless, micro bikini도 조사 대상에 남겼다. 패션의 체인·스터드·찢김은 의복 형태로 조사하고, 별도 폭력 사건이나 관계를 만들어 넣지 않는다.

| 산출물 | 읽을 수 있는 내용 |
|---|---|
| [상세 의미 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/semantic-cards.md) | 118개 가족의 정의, owner, 관계, 혼동 경계, 관찰 조건, 독립 변형, 출처 |
| [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/candidate-proposals.json) | 166개 관찰 문장, 구체적인 관계 양 끝점, 속성 가족, 채택 조건, 계획 상태의 gate |
| [용어별 반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/term-plan.csv) | 299행 전부의 의미 카드, 처리 방향, 우선순위, 관련 가족 초안, 현재 이웃과 출처 |
| [현재 긍정 필드 이웃](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/term-inventory.json) | 공식 tokenizer를 이용한 후보·프로필의 토큰 이웃 목록 |
| [출처 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/source-ledger.json) | 68개 URL, 확인한 사실 범위, 접근 수준, 일반화 한계 |
| [반영 단계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/implementation-plan.json) | 도메인별 원본 소유, 승격 순서, 인덱스·검색·픽셀 증거 요구 |
| [회귀·이미지 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/regression-plan.json) | 혼동 비교, 정상 조합, 의도적 결함 변경, 필요한 관찰 시점 |

각 카드의 연결 그래프·영문 문장·프레이밍은 연구자가 작성한 실현 제안이다. 출처가 카드의 모든 변형을 그대로 정의했다는 뜻이 아니다. 299행의 모든 별칭을 각각 독립 출처로 재검증했다는 주장도 하지 않는다. 용어 행에서 연결한 related_family_draft_ids는 **검토할 가족 인벤토리**이며 직접 동의어 매핑이 아니다. 개별 용어와 개별 변형의 동등성·적합성은 구현 W0에서 확정한다.

## 2. 현재 저장소와 실제 보강 지점

2026-10-09 **03:43:00~03:43:13 KST**, HEAD `f081ac7305210def8348cc76d3a8f9f48393b4de`의 작업 트리를 공식 원본 로더로 읽었다. 기존 미커밋 변경이 포함된 조사 기준이다. 원본 assets와 scripts 165개를 로드 전후 해시로 비교했고 이 구간의 변경은 없었다. runtime snapshot provider, publisher, embedding, 이미지 호출은 실행하지 않았다. [조사 기준과 해시](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/current-source-audit.json).

| 집계 단위 | 현재 조사 수량 |
|---|---:|
| 슬롯 | 114 |
| 로드된 슬롯 후보 | 11,188 |
| 컴파일된 시각 프로필 | 2,977 |
| 후보 번들 | 1,347 |
| 원문 행 중 후보 긍정 필드 토큰 이웃이 있는 행 | 198 / 299 |
| 프로필 긍정 필드 토큰 이웃이 있는 행 | 169 / 299 |
| 둘 중 하나에 토큰 이웃이 있는 행 | 203 / 299 |

이 집계는 검색 정확도나 데이터 완성도 점수가 아니다. tokenizer는 단어의 경계를 지키지만 여러 토큰이 떨어진 위치에 있어도 이웃으로 잡을 수 있다. 따라서 96행의 표현이 검색되지 않은 것이 곧 의미 누락은 아니며, 203행에 이웃이 있는 것이 곧 같은 의미라는 뜻도 아니다. 실제 임베딩 회수·후보 노출·선택·이미지의 증거는 별도다.

특히 body chain 행에는 의복 장신구뿐 아니라 몸 포즈·손 접촉 관련 이웃도 나온다. 소유자와 slot, 관계를 붙여 검토해야 하는 이유다. drop shoulder는 정확한 라벨 이웃에 없더라도 `fit_ff09_v1_candidate`의 어깨끝-소매 연결 관계가 이미 있어, 별도의 원본 발췌로 확인했다. [추가 검토 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/additional-reviewed-records.json).

| 기존 도메인 원본 | 후보 수 | concept_units / relations / affected_properties |
|---|---:|---|
| 수영복 | 65 | 65 / 0 / 0 |
| 패션 핏 | 114 | 114 / 114 / 114 |
| 의복 구조 | 174 | 174 / 174 / 174 |
| 직물 표면 | 38 | 38 / 38 / 38 |

수영복에는 연결을 잘 설명하는 concept_units가 이미 있으나, 조사한 슬롯 후보에는 명시적 relations와 세부 effect 범위가 없다. 이런 **여러 끝점을 가진 의복 관계**부터 보강하는 편이 효과적이다. 단일 질감 후보에 관계 수를 무조건 늘리자는 제안은 아니다.

| 씨앗과 실제 이웃 | 판단과 계획 |
|---|---|
| `sw_candidate_triangle` | 두 삼각 패널과 꼭짓점 지지 연결을 재사용. string은 별도 관계 |
| `sw_candidate_bandeau` | 수평 밴드의 위·아래 경계를 재사용. strapless/halter를 따로 보존 |
| `sw_candidate_tankini`, `sw_candidate_onepiece` | 독립 밑단·하의 vs 연결 몸통·두 다리입구를 명시적 그래프로 보강 |
| `sw_candidate_highleg` | 다리입구와 waistline 구분을 유지하며 세부 effect 범위 추가 |
| `fit_ff52_v1_candidate`, `fit_ff52_v2_candidate` | 이미 Y 합류와 X 교차를 구분. 중복 후보보다 다국어 표현·부정·가림 회귀를 우선 |
| `cold_shoulder_cutout_sleeve_bridge` | 좋은 경계 설명을 bridge/개구부/남은 소매의 구조와 관찰 의무로 강화 |
| `pfe_midriff_candidate` | 피부 띠 자체는 있음. 배꼽 가시성까지 같은 뜻으로 묶지 않음 |
| `pfe_lateral_chest_candidate`, `pfe_lower_chest_candidate` | 성인 의복의 옆·아래 가슴 경계를 재사용하고 해당 owner와 국소 effect를 보존 |
| `y2kr_whale_tail` | 이너끈이 별도 낮은 허리선 위로 나오는 관계가 있음. 이너/겉옷의 층 owner와 뒤 연결 보강 |
| `clt_ct031_v1`, `clt_ct064_v1/v2`, `clt_ct065_v1/v2` | 다트/프린세스 심, 셔링/스모킹, 러플/플라운스의 기존 구조 재사용 |
| `broderie_anglaise_eyelet`, `fisherman_sandals` | 이름 수준의 이웃에 실제 자수 구멍·케이지 끈 연결을 보강할 가치 |
| `clt_ct113_v2` | 목-허리 체인 관계 재사용. 장신구를 pose나 옷의 지지끈과 혼합하지 않음 |
| `sff_extra_xa005` | 현재 `topless monokini` 역사형. 현대 cutout one-piece 씨앗과 의미 동등하지 않음 |
| high-neck halter / milkmaid top / seersucker | 이 조사에서 해당 표현의 긍정 토큰 이웃 없음. 기존 유사 구조를 확인한 뒤 필요한 변형만 추가 |

## 3. 원문 용어를 분해할 독립 축

| 축 | 저장할 관찰 관계 | 자동으로 붙이면 안 되는 의미 |
|---|---|---|
| 기본 의복 | top/dress/divided legs, 상하 분리·연결 | 계절 장소, 성별·연령, 신체 변경 |
| 어깨·끈·소매 | 붙는 끝점, 합류·교차, sleeve bridge, seam의 위치 | 깊은 앞목 파임·백리스·특정 소매 길이 |
| 네크라인 | 위 가장자리의 shape·폭·깊이·중앙 접점 | 가슴골 가시성·푸시업·원료 |
| 핏·실루엣 | 옷과 몸의 접촉·여유, 허리/하부의 폭 관계 | 신체 가슴·힙·허리 크기 변경, 압력 수치 |
| 길이·rise | 실제 밑단·waistband와 몸 기준점 | 배꼽 노출, high-leg, 정확 cm |
| 개구부·coverage | 둘러싼 구멍·open edge·slit apex, 면별 coverage | 투명 원단, 다른 의복 사이 공백, 반대면 구조 |
| 광학 투과 | outer fabric → visible inner layer → skin | 원단 구멍, nakedness, braless |
| 원료·조직·가공 | 조성 명세와 관찰 가능한 weave/knit/relief 분리 | UPF·성능·브랜드·제조공정 픽셀 인증 |
| 장식·무늬 | 부착점, 모티프 크기·반복, 색면, 반사 | 실제 부상·폭력·직업·문화 정체성 |
| 착장 스타일 | 선택 가능한 의복·색·질감 조합 | 고정 복장 묶음, 장소·나이·성격·계층 |

같은 성인 인물의 같은 옷에 특정 스타일·부위 관계를 덧붙이는 연구다. 의복에서 비롯된 hourglass/bodycon 강조를 body_geometry 변형으로 바꾸지 않는다. 특정 스타일명의 어원이 여성·girl·grandmother를 포함해도 그 이름만으로 나이·가족관계를 바꾸지 않는다.

## 4. 상세 조사에서 중요한 경계

### 네크라인과 연결 구조

크루·스쿠프·V·스퀘어·스위트하트·보트·카울은 각각 원단 가장자리의 높이/곡선/접점/처짐으로 설명할 수 있다. 그런데 가슴골은 가장자리 이름과 별개로 실제 가슴 사이 중앙 영역이 보이는 상태다. 넓은 보트넥이 반드시 어깨 아래에 놓이는 것도 아니다. SF018~SF030은 shape·position·coverage를 따로 둔다. [MasterClass](https://www.masterclass.com/articles/guide-to-necklines).

홀터는 목 뒤로 이어지는 연결 경로를 먼저 표현한다. 앞을 높게 덮는 SF005 v1과 낮은 앞 파임을 가진 v2는 독립 변형이다. 긴소매/짧은소매가 모두 있는 실제 camp-collar 패턴처럼, 칼라나 끈 형태가 소매 길이를 고정하지 않는다. [Burda 5891](https://simplicity.com/burda-style/bur5891), [Seamwork Negroni](https://www.seamwork.com/pdf-sewing-patterns/negroni-vintage-camp-shirt).

스카프 톱도 모두 같은 삼각 strapless 천이 아니다. 실제 Bandana Scarf Tie Top에는 한쪽 어깨를 두른 천, 목의 connector, 뾰족한 밑단, 뒤 tie가 함께 있다. SF006은 단순 back knot 실현과 이 연결 실현을 독립 후보로 둔다. [Christopher Esber 상품 구조](https://christopheresber.com.au/products/bandana-scarf-tie-top-indigo-bandana-print). polo 역시 판매군 안에서 칼라·짧은 placket은 유지하되 단추 숨김·소매 길이·fit이 다를 수 있다. [Lacoste의 여러 polo 구조](https://www.lacoste.com/us/lacoste-polos.html).

off-shoulder는 전체 윗선이 어깨 아래, cold-shoulder는 어깨 위 bridge와 아래 소매가 남는 구조다. drop shoulder는 소매를 붙이는 봉제선이 어깨끝 바깥에 있는 구조다. 같은 bare shoulder 인상으로 묶으면 정작 원단 연결을 잃는다. SF026·SF028·SF033은 어깨 기준과 원단/소매의 실제 끝점을 검사하도록 설계했다.

### 밀크메이드·피전트·셔링

milkmaid 상품명에 ruched bust, flutter sleeves, square neck, semi-sheer, smocked back을 결합한 사례가 있다. 퍼프소매와 면 소재를 보편 필수로 고정하면 이 사례부터 설명하지 못한다. SF010은 style name을 선택 가능한 visible construction으로 다루고, SF011은 주름을 모으는 줄과 장식 자수를 따로 기록한다. [Free People Prairie Field](https://www.freepeople.com/shop/prairie-field-top/).

Seamwork는 탄성실 셔링과 자수 스모킹을 구별하지만 제품명에서는 두 이름이 섞일 수 있다. Threads의 glossary는 ruching을 gathering 계열로 설명한다. 따라서 판매명을 무조건 배타적인 세 범주로 만들기보다 **봉제 줄·주름 연결·장식 stitches·해당 의복 부위**를 저장한다. [Seamwork shirring](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring), [Threads glossary](https://www.threadsmagazine.com/project-guides/learn-to-sew/sewing-terms-to-know).

러플/프릴과 플라운스도 넓은 장식 가족에서 중첩될 수 있다. 한쪽 변형은 부착선의 개더, 다른 변형은 부착선에 모음 없이 아래로 증가하는 폭이 구별점이다. SF100의 두 변형을 하나의 all-of 계약으로 합치지 않는다. [Threads geometric flounces](https://www.threadsmagazine.com/2020/02/19/how-to-sew-geometric-flounces).

### 복부·배꼽·가슴·등의 가시성

배꼽을 보이게 하는 관계는 **상의 밑단 → 배꼽 → 하의 윗선** 세 기준점이 필요하다. 복부의 얇은 띠가 보이면서 배꼽이 가려진 SF051 v2도 유지한다. crop/high-rise/low-rise 라벨에서 가시성 결과를 대신 판정하지 않는다.

sideboob와 underboob는 성인 의복 가장자리 옆/아래에 가슴 경계가 보이는 관찰 상태다. deep armhole·underbust seam·micro-crop은 이 상태의 동의어가 아니다. SF050은 옆·아랫경계를 각각 후보로 작성했고, 기존 PFE의 성인 대상·불투명 중앙 덮임·의복 소유 관계를 재사용하도록 계획했다. 아주 짧은 half-shirt와 underboob 표현을 함께 쓰는 런웨이 사례는 한 실현의 근거이며 모든 micro-crop의 정의는 아니다. [Alexander Wang spring 2025 관찰](https://www.vogue.com/fashion-shows/spring-2025-ready-to-wear/alexander-wang).

앞 high-neck과 뒤 low-back은 함께 성립할 수 있다. 앞쪽 사진으로 뒤판을, 뒤쪽 사진으로 앞 컵·목 파임을 자동 추론하지 않는다. hair/팔/프레임이 가린 부분은 옷이 덮은 것으로도, 노출된 것으로도 추정하지 않는다.

### 비침·구멍·층과 숨은 상태

시어는 연속된 원단을 통한 투과, mesh/openwork는 실제 조직 사이의 구멍, cutout은 의복 원단 영역을 비운 개구부다. 같은 색의 불투명 이너가 비치면 보이는 것은 이너 원단이다. **outer garment와 inner garment를 따로 소유시키고 투과의 대상까지 연결**해야 피부 노출로 잘못 강화되지 않는다. [Bazaar의 시어 착장](https://www.harpersbazaar.com/fashion/trends/a43532183/how-to-wear-sheer-clothes/).

unlined와 braless는 숨은 층/착용 상태의 명세다. 어깨끈이 없거나 원단이 매끈해 보이는 것만으로 실제 브라 미착용을 증명하지 않는다. 니플 커버도 독립 국소 제품으로 기록하되, 피부 위에 보이지 않는 커버의 존재·부착·성능을 외관만으로 추정하지 않는다. adhesive/non-adhesive 구분은 실제 제품군에서도 존재한다. SF047·SF054·SF056·SF092는 이런 명세를 보존하며 자동 픽셀 후보를 만들지 않은 카드다. [CAKES 제품](https://cakesbody.com/products/grippy-cakes-circles).

### 수영복의 조합 축과 모노키니

triangle은 패널 모양, string은 연결 끈, bandeau는 수평 밴드, halter는 목 뒤 경로, longline은 컵 아래 길이다. high-leg는 다리 입구, high-waist는 허리선, cheeky/Brazilian/thong은 뒤판의 폭·커버리지에 관계한다. 분리형 bikini와 긴 tankini, 연결된 one-piece도 토폴로지가 다르다. [Seafolly tankini](https://us.seafolly.com/blogs/sf-world/what-is-a-tankini), [Seafolly Brazilian](https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut).

같은 제품 제목에 high leg와 high waist가 같이 있어 두 축의 공존이 확인된다. 다만 해당 Singapore 페이지의 직접 열기는 실패했으므로 제목 확인 이상의 치수·이미지 판단은 하지 않았다. [상품 제목 근거](https://sg.seafolly.com/products/jetset-lure-high-leg-high-waist-bikini-bottom-j30196-black).

원문에서 지적한 monokini 다의성은 현재 데이터와 비교했을 때 특히 중요하다. FIT의 1964 Gernreich 역사형과 Cupshe의 현대 Monokini/Cut Out 판매 범주는 다르다. 현재 이웃 `sff_extra_xa005`는 역사형의 topless 의미를 갖고 있다. 이것은 **잘못된 의미 전이 가능성을 검사할 근거**이지 실제 런타임이 잘못된 이미지를 생성했다는 증거는 아니다. SF081은 두 문맥을 보존하고 broad label만으로 어느 쪽도 hard 활성화하지 않도록 우선 계획했다. [FIT swimwear history](https://fashionhistory.fitnyc.edu/a-history-of-womens-swimwear/), [Cupshe 현대 분류](https://www.cupshe.com/collections/monokini-cut-out).

burkini도 머리·상의·바지를 반드시 세 개의 분리 물품으로 고정하면 실제 2-piece/attached Hijood 제품을 설명하지 못한다. SF090은 연결 방식을 선택 변형으로 두고 종교·국적·성능은 생성하지 않는다. [Ahiida 제품](https://ahiida.com/product/sz-ultramarine-black-spliced/).

swimdress에는 실제로 attached swim shorts를 가진 제품이 있다. 뒤·옆·밑단에서 연결 하의가 보이지 않는 한 skirt 외곽만으로 내부 구조를 픽셀 확인했다고 하지 않는다. boardshort/skirt 같은 혼합 제품도 있어 swim/board 판매명을 배타적인 다리통 구조로 고정하지 않는다. [Swimsuits For All의 연결 하의](https://www.swimsuitsforall.com/products/swimdress-with-attached-swim-shorts/1065683.html), [Billabong의 swim/boardshort군](https://www.billabong.com/collections/womens-swim-boardshorts).

### 드레스·스커트의 재단과 실루엣

shirt dress는 칼라·placket 관계이고 반드시 boxy한 silhouette는 아니다. 실제 Brom에는 몸판 darts와 A-line skirt가 있다. shift와 empire도 항상 배타적이지 않으며 Georgia는 두 이름을 함께 쓰고, Freesia는 empire waist와 body-skimming fit을 결합한다. SF057~SF059는 판매명보다 실제 여유와 skirt seam의 기준점으로 선택하도록 설계했다. [Brom](https://www.seamwork.com/pdf-sewing-patterns/brom-pleated-sleeve-shirt-dress), [Georgia](https://www.seamwork.com/pdf-sewing-patterns/georgia-easy-woven-shift-dress), [Freesia](https://www.seamwork.com/pdf-sewing-patterns/freesia-empire-waist-bias-dress).

half-circle과 pleated도 함께 성립한다. Brooklyn의 front box pleat와 half-circle 재단을 하나의 배타 taxonomy로 만들지 않는다. bubble은 밑단이 모여 만든 부피 관계이며 natural waist/length는 별도다. 원형 재단·숨은 lining·제작 방법은 실제 외곽과 다른 증거를 요구한다. [Brooklyn](https://www.seamwork.com/pdf-sewing-patterns/brooklyn-full-skirt), [McCall M8583](https://simplicity.com/mccalls/pdm8583).

### 원료·조직·표면·성능

섬유 이름과 조직은 분리한다. TENCEL은 제조사의 브랜드이며 현재 공식 포트폴리오는 Lyocell, Modal, Lyocell Filament를 포함한다. 원문의 lyocell/modal 설명에 filament를 보완했다. elastane/spandex도 일반 섬유 종류이고 LYCRA는 브랜드다. [Lenzing](https://www.lenzing.com/products/brands/tenceltm/), [LYCRA FAQ](https://one.lycra.com/en/lycra-frequently-asked-questions/quality-lycra).

새틴은 조직·원단 용어의 사용 범위도 조심해야 한다. Cotton Incorporated 문헌은 silk satin과 다른 섬유의 sateen이라는 구분 및 지역 차이를 설명하고, 현대 공급사는 polyester를 satin weave로 짠 charmeuse를 명시한다. 한 정의를 전세계 판매명 표준으로 강제하지 않고 **섬유 조성, weave, 표면 광택을 별도 정보**로 유지한다. [Cotton Incorporated weaving](https://cottonworks.com/wp-content/uploads/2018/01/Weaving_booklet-for_web.pdf), [Mood polyester charmeuse](https://www.moodfabrics.com/collections/polyester-charmeuse-fashion-fabrics?limit=90).

seersucker의 반복 puckering은 착용 구김이나 봉제 셔링으로 바꾸지 않는다. rib의 실제 골과 인쇄 stripe, eyelet의 바탕천·자수 구멍과 metal grommet, mesh의 망눈과 투명 고체, terry pile loop와 젖은 수건을 구별한다. SF093~SF098은 전체 사진과 native 근접면에서 확인할 표면 관계를 분리했다. [Seamwork cotton guide](https://www.seamwork.com/fabric-guides/a-guide-to-cotton-fabrics-for-garment-sewing-from-lawn-to-denim-and-everything-in-between), [CottonWorks knits](https://cottonworks.com/learning-hub/knitting/single-and-double-knits/), [직물 공급사 glossary](https://fashionfabricsclub.com/pages/fabric-glossary).

통기성·흡한·속건·UPF는 서로 다른 성능 명세다. 가벼운 외형·늘어남·투과 사진을 성능 수치나 인증으로 승격하지 않는다. 요청에 해당 정보가 있으면 명세로 유지하고 관찰 가능한 표면/처짐과 분리한다. [REI 원단 요인](https://www.rei.com/learn/expert-advice/how-to-pick-the-most-breathable-fabrics.html), [UPF의 의미](https://www.skincancer.org/skin-cancer-prevention/sun-protection/sun-protective-clothing/).

### 스타일·패턴·신발·장신구

-core/-girl 계열은 중첩되는 사용 명칭으로 저장한다. 무조건 새 top/dress profile을 하나씩 만드는 것보다 선택한 옷의 visible cues를 여러 방식으로 조합하는 후보가 유용하다. 2023 회고와 2025 이후 편집 사용 자료를 2026 현재 인기 순위처럼 쓰지 않았다. [Vogue의 명칭 사용](https://www.vogue.com/article/core-aesthetic-microtrends-2023), [Bazaar의 microtrend 용례](https://www.harpersbazaar.com/fashion/trends/a65784060/a-z-micro-trends-defined/).

신발의 thong은 발가락 사이 Y-strap이다. slide의 발등 band와 구분하며 속옷 owner로 옮기지 않는다. wedge/forefoot platform/heel openness는 동시에 조합할 수 있는 다른 축이다. SF112~SF114는 실제 끈 끝점·밑창·발의 관계를 후보화한다. [Havaianas](https://www.havaianas.com/blogs/news/sandals-vs-flip-flops-what-s-the-difference), [Castañer 제작](https://castaner.com/en-gr/pages/atelier).

mesh flat도 갑피 전체가 동일하게 비치는 것은 아니다. Rothy's의 제품 설명에는 mesh upper와 solid knit toe가 공존한다. Melissa의 jelly 판매군에는 검색 발췌에서 Opaque Blue가 확인되어, jelly라는 이름만으로 투과를 hard로 켜지 않도록 반례를 추가했다. 후자는 컬렉션 명세 근거이며 상품 이미지 광학 검증은 아니다. [Rothy's 부위별 갑피](https://rothys.com/products/womens-max-square-ballerina-clover-mesh), [Melissa 판매 분류](https://www.shopmelissa.com/collections/adult-shoes?page=17).

raffia는 원료 명칭, basket은 구성 가족이다. 실제 basket군에도 raffia/rattan/iraca palm 등과 여러 가방 형태가 있으므로 SF116에서 원료와 body/handle 연결을 따로 둔다. [LOEWE basket군](https://www.loewe.com/usa/en/women/bags/baskets).

waist chain과 neck-to-waist body chain은 다른 장신구 그래프다. 같은 accessory의 endpoint를 지키고 top straps, pose, 결박 관계로 바꾸지 않는다. 스터드·찢김·체인의 펑크 문맥은 유지하되 실제 폭력을 추론하지 않는다. [V&A Westwood](https://www.vam.ac.uk/collections/vivienne-westwood).

목과 허리를 감싼 체인이 가슴에서 연결되는 장신구 상품을 추가 확인해 SF118의 endpoint 제안 근거를 보완했다. 합금·도금·무게·가격이나 착용자의 심리는 그 연결 그래프에 넣지 않는다. [Jennifer Zeuner Lala Body Chain](https://jenniferzeuner.com/products/lala-body-chain).

## 5. 데이터 반영 방법

현재 모델의 public surfaces인 concept_units, directed relations, slot candidates, optional bundles를 유지한다. 계절별 파일 하나에 299행을 복제하기보다 **의미를 소유하는 도메인 원본**을 먼저 확장한다.

| 표면 | 우선 반영할 내용 |
|---|---|
| 수영복 extension/profile | 상하 연결·위/아래 band·neck/back strap·waist/leg/rear의 별도 owner 관계 |
| 의복 구조 extension/profile | shoulder bridge, free vs fixed wrap, slit apex, seam 끝점, dart와 panel의 실제 연결 |
| 패션 핏 extension/profile | 국소 여유·의복 폭·seam 위치의 재사용; body geometry 변경 금지 |
| 초상·커버리지 extension/profile | 중앙/옆/아래 가슴, 복부/배꼽, 앞/뒤 가시성의 국소 범위 |
| 직물 표면 extension/profile | 실제 weave/knit/relief/투과 대상, 광택과 원료 분리 |
| 장신구·신발 원본 | ring/lacing/chain owner, toe-post/cage/heel/sole의 끝점 |
| Y2K 및 기존 스타일 후보 | whale tail·baby tee·bandeau 표현 보강; 스타일 묶음은 optional |

제안의 최소 단위는 “어떤 owner의 A가 B와 R 관계에 있다”이다. 예를 들어 SF035의 같은 top에서 two straps → converge into → central band와 two straps → cross at → center of back는 독립 변형이다. 선택한 변형의 각 구성 문장과 관계를 literal evidence로 증명하고, 해당 프로필을 채택했다면 모든 gate를 일반 composed/render contract로 전달한다.

현재 초안은 payload_draft와 연구 metadata를 분리했다. payload 안에는 원문 bulk 어휘, source URL, 출처 제목, 연구 카드·점수·인기 라벨을 넣지 않았다. 하지만 **complete per-variant effect 검토는 남아 있다**. 초안의 속성 가족만 보고 그대로 등록하면 안 된다. 현재 후보에 같은 path가 있는지와 실제 schema 허용 여부도 다른 문제다. wardrobe.fit/length/silhouette/structure.sleeve/structure.strap의 가족 표현은 후속 작업에서 정확한 leaf와 영향 범위를 확정한다.

문장에 여러 open dimensions가 바뀌는 경우에는 모든 영향을 기록한다. 예를 들어 새 dress base를 고르는 후보가 소재 drape·hem·strap까지 고정한다면 이 효과를 appearance 한 가족으로 숨기지 않는다. 옷의 구조를 잠근 요청에 신발/무늬만 열려 있으면 해당 옷 후보는 거절할 수 있어야 한다.

현재 299행의 처리 원장은 다음과 같다. 이 수량은 최종 새 엔트리 수나 구현 완료 수가 아니다.

| 연구 처리 방향 | 원문 행 |
|---|---:|
| 기존 의미 동등성을 검토한 뒤 필요한 가시 변형만 추가/확장 | 216 |
| 확인한 기존 후보의 의미 재사용·관계/effect 검토 | 68 |
| 숨은 구조·착용 상태·섬유/물품 유형의 명세 보존, 자동 픽셀 후보 없음 | 14 |
| 역사/현대 문맥 분리 후 재사용 | 1 |

## 6. 구현 순서와 완료 조건

**W0 — 현재 원본 재확인과 동등성 판정.** 원본·manifest·현재 branch/hash를 새 작업 시점에 다시 확인한다. 299행과 166초안에서 기존 ID 재사용, 문구 확장, 관계 보강, 신규 변형, 비시각 명세를 확정한다. 모노키니·thong·eyelet·fringe·style/identity 다의성을 먼저 다룬다. 이 단계에서 실제 승격할 엔트리 수가 정해진다.

**W1 — 핵심 경계.** 우선순위는 crop/navel, halter/front/back, cold/off/drop shoulder, Y/X strap, layer/transmission/cutout, monokini, high-leg/high-rise, rear coverage, seersucker, eyelet, footwear/chain이다. 정상 조합을 허용하면서 adjacent profile이나 잘못된 owner가 hard로 켜지는지 확인할 paired cases를 작성한다.

**W2 — 원본 관계·프로필.** 기존 도메인 extension과 corresponding profile을 먼저 보강한다. concrete garment/component nodes, 단일 directed relation, 독립 variant, 전체 affected-properties를 확정한다. broad label·approximate hit가 requester hard authority를 만들지 않도록 한다. 출처와 limitations는 연구 evidence area에 둔다.

**W3 — 표면·장신구·스타일.** 표면 원자, 신발 끈·밑창, 장신구 연결을 보강하고 스타일은 선택형 조합을 늘린다. 모든 milkmaid/core 스타일에 동일 배경·노출·몸매를 강제하지 않는다. 새 summer extension은 현 도메인 소유 체계보다 운영/검색 이득이 확인되는 경우에만 검토한다.

**W4 — 파생 데이터와 publication.** 필요한 원본만 수정하고 source_manifest 및 maintenance_ref를 유지한다. semantic/BM25F와 visual-profile index를 다시 만든다. 같은 provider/model/dimensions와 전체 embedding 입력 text가 동일한 벡터만 재사용하고 새/변경 text의 batch size는 1로 유지한다. dictionary/registry stale hash와 current runtime revision을 검증한다. historical pack·baseline을 새 결과로 덮어쓰지 않는다. [현재 유지보수 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md).

**W5 — 실제 검색·채택·구성 회귀.** label/한국어·영어 paraphrase/부정/homonym/다중 owner를 별도로 시험한다. 각 요청에서 core를 독립 작성·freeze한 다음 retrieval을 실행하고, 원하는 관계가 회수되고 adjacent 의미로 오염되지 않는지 확인한다. optional candidate 선택 여부, literal component/relation evidence, bundle members와 효과 잠금, composed binding과 runtime receipt를 분리 검증한다.

**W6 — 이미지와 사용자 선호.** 이미지 검증이 요청될 때 선택한 검증 묶음과 범위를 확정하고 실제 생성한다. 원본 이미지와 native crops에서 모든 hard gate를 확인한다. 가림·프레임 밖·작은 해상도·한 component 성공은 전체 PASS가 아니다. 미학적 선호와 사용자의 수락은 instruction fidelity와 별도 증거다.

## 7. 회귀와 이미지 검증 설계

57개 비교는 서로 다른 meaning을 구별하는 요청이다. 전세계 판매 용어를 배타적 taxonomy로 만들기 위한 표가 아니다. 16개 정상 조합에는 high-waist+high-leg, bandeau+halter, high-neck+low-back, crop+가려진 배꼽, openwork+opaque inner, maxi+thigh slit, wedge+platform, shift+empire waist, mesh upper+solid toe가 포함된다.

15개 변경 반례는 owner 이동, 이너/겉층 바꾸기, endpoint 누락, 대안 합치기, source leak, property 잠금 위반, body edit, hidden property PASS, thumbnail-only PASS, 가림을 PASS로 처리, negation hard leak, similarity hard 승격, stale pack, sibling activation, partial-as-full을 다룬다.

| 이미지 묶음의 목적 | 필요한 증거 |
|---|---|
| 배꼽·crop·rise | top hem, waistband, navel 세 기준점 |
| high-neck halter·back opening | 앞 덮임과 목 뒤 join; 뒤판은 실제로 보이는 시점 |
| off/cold/drop shoulder | 신체 shoulder와 원단 윗선·bridge·seam의 관계 |
| racer/X back | 같은 top의 모든 strap endpoint와 합류/교차 |
| sheer·mesh·illusion·cutout | 연속 outer fabric 또는 실제 구멍, inner owner, layer 순서 |
| slit·길이·skort·romper | 실제 밑단/트임 apex/분리 다리통/연결 이너 |
| cup·dart·seam | 실제 외곽·봉제 연결; 숨은 wire/pad의 성능은 평가하지 않음 |
| swim coverage | waistband·leg opening·rear panel을 별도로 보여주는 시점 |
| surface relief | 전체 원본과 native crop에서 실제 loop/gather/embroidered hole |
| footwear·chain | toe-post/cage/heel/sole 또는 neck/waist chain의 모든 연결 끝점 |
| style | 선택된 의복 단서 fidelity; identity·장소·선호는 별도 |

이 표와 18개 pixel group은 계획이다. 해당 시점의 source·core·pack·selected gates를 고정한 실제 실험은 아직 없다.

## 8. 이번에 검증한 범위

연구 산출물 생성과 무결성 검증은 통과했다. 299행 매핑, 118개 카드, 166개 고유 초안, 68개 출처 참조, 기존 검토 ID, 관계 양 끝점, CSV/JSON 일치, source URL의 payload 분리, 효과에 identity/body_geometry가 들어가지 않는 것을 검사했다. [연구 무결성 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/research-validation.json).

이 검증은 연구 파일의 구조·참조 무결성을 증명한다. 의미 동등성 최종 판정, runtime dictionary/profile 등록, 인덱스 재생성, live retrieval, composition, 이미지·moderation·사용자 acceptance는 이번 결과에 포함하지 않는다. 임베딩 호출과 이미지 호출은 0회다.

연구 원본은 새 문서와 이 조사 폴더에 작성했다. 기존 미커밋 원본·테스트를 복원하거나 stage하지 않았다. [종료 보존 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/final-preservation.json)와 [산출물 검증·해시 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/summer-fashion-20261009/final-validation.json)에 최종 상태를 기록한다.

# 가을 패션 시각 의미·후보 데이터 상세 리서치와 반영 계획

2026-10-09 KST. 기준 대화: [가을 패션 용어 조사](chatgpt-conversation://6ac7dd53-2098-83ee-8a3c-84c3a250f650).

가을 패션 데이터는 **의복 종류, 구조, 부위별 핏, 기장, 소재·조직, 표면, 현재 착용 상태, 레이어 순서, 실제 가시 영역**으로 분해해 강화하는 것이 적절하다. 스타일 이름은 이 축들을 선택하는 문맥이고, 구체적인 옷·피부·배경을 모두 강제하는 규격이 아니다. 특히 “몸을 따른다”, “피부가 직접 보인다”, “원단 너머로 이너가 비친다”는 서로 다른 관계다. 이 분해는 패턴 제작사의 여유량 설명, 의복 디자이너의 목선 구분, 제조사의 직물·코디 설명을 대조한 연구 설계다. [Seamwork](https://www.seamwork.com/sewing-tutorials/understanding-ease), [Sherri Hill](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [Ralph Lauren](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html).

원문 용어 표 **347행**, 부위별 역검색 **10행**, 코디 예시 **12행**을 읽었다. 이를 **113개 상세 의미 카드, 129개 후보 문장 초안, 42개 출처 원장, 의미 비교 56쌍, 변형 반례 12개, 이미지 검사 12묶음**으로 정리했다. 113개 중 111개는 표의 의미군이고, 2개는 본문에 등장한 데콜테·클리비지와 DEN의 보충 카드다. 한 행 안의 별칭을 여러 용어로 중복 집계하지 않았다.

이번 산출물은 리서치와 반영 설계다. **129개 초안은 실제 신규 런타임 엔트리 수가 아니다.** 기존 의미 재사용, 표현 보강, 독립 변형, 명세 메타데이터를 검토하기 위한 예시다. 원본 등록·색인 재생성·라이브 검색·이미지 생성은 후속 적용 단계이며 이번에는 실행하지 않았다.

**확인 가능한 산출물**

| 산출물 | 내용 |
|---|---|
| [상세 의미 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/semantic-cards.md) | 113개 의미군의 뜻·관찰 단서·소유자·혼동 경계·주장 한계·기존 이웃·출처 |
| [용어별 반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/term-plan.csv) | 원문 347행 모두의 카드·우선순위·처리 방향·현재 후보/프로필 이웃 |
| [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/candidate-proposals.json) | 129개 독립 가시 문장, 구체 관계의 양 끝점, 적용 전제, 속성 범위 검토 입력 |
| [반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/implementation-plan.json) | 기존 원본별 재사용 방향, 7개 적용 파동, 파생 색인·런타임·검증 기준 |
| [회귀·이미지 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/regression-plan.json) | 56개 최소 비교, 12개 변형 반례, 12개 이미지 검사 묶음 |
| [원문 코디·역검색](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/source-outfit-examples.json) | 12개 코디를 유지보수 평가 요청으로 보존하고 10개 부위 목표를 관찰 조건으로 연결 |
| [출처 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/sources.json) / [보충 출처](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/supplemental-sources.json) | 자료의 권위 종류·접근 수준·확인한 사실·일반화 한계 |

**원문과 근거의 확보 범위**

`read_thread`의 응답은 20,000자에서 잘렸다. 공식 ChatGPT 화면의 렌더된 표를 추가로 읽어 17절, 표 27개를 확인했다. 표 1~15절의 첫 열을 [씨앗 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/seed-terms.txt)에 전사했다. [대화 캡처](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/source-conversation.json)의 API 본문은 잘린 상태이며, 전체 본문 복사본이라고 표현하지 않는다. 전체 용어 목록과 후반부 정의·코디 관계는 렌더된 화면에서 확인했다.

42개 출처에는 제조사·디자이너·패턴 개발자·산업 기관·박물관·출판사 사전과 스타일 사용례 기사가 포함된다. 직조·선밀도·제작 구조의 사실에는 제작·산업 자료를, 복식사의 디자인에는 기관·소장품 해설을, 인터넷 스타일 이름에는 해당 시기의 사용례를 사용했다. Vogue의 office siren·coquette·quiet luxury 기사는 **스타일 담론의 사용례**이고, 2026년 현재 유행 순위나 보편 복식 규격을 확증하지 않는다.

출처의 제품 사양과 연구자가 설계한 가시 문장·관계·픽셀 검사 조건은 다르다. 347개 행의 모든 별칭과 현대 변형을 각각 독립된 1차 자료로 정의했다는 뜻도 아니다. 예를 들어 barn/shacket의 상품명 중첩, pointelle의 제품별 구멍·조직, duster의 역사 변형은 승격할 정확한 레코드의 제품·패턴 근거를 추가 확인해야 한다. 이 조건은 각 카드와 용어별 대조표에 남겼다.

**현재 저장소와 대조한 기준**

2026-10-09 **03:39:32~03:39:47 KST**에 현 작업 트리의 공식 로더로 원본을 읽었다. HEAD는 `f081ac7305210def8348cc76d3a8f9f48393b4de`이고, 기존 미커밋 원본 변경이 포함된다. 이 구간의 원본·관련 코드·색인 매니페스트 SHA-256과 mode는 바뀌지 않았다. 원본을 로드한 조사이고 전체 검사기·런타임 dispatch·임베딩 검색을 실행한 결과는 아니다. [기준 스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/source-snapshot.json).

| 집계 | 확인 수량 |
|---|---:|
| 후보 슬롯 | 114 |
| 로드된 슬롯 후보 | 11,188 |
| 로더의 의미 문서 | 11,224 |
| 컴파일된 시각 프로필 | 2,977 |
| 후보 번들 | 1,347 |
| 등록 후보 원본 / 시각 프로필 원본 | 67 / 49 |
| 씨앗 표현이 후보의 긍정 필드에 있는 행 | 219 |
| 씨앗 표현이 프로필의 긍정 필드에 있는 행 | 171 |
| 둘 중 한 곳에 표현이 있는 행 | 220 |

남은 127행은 **표현 대조에서 이웃을 찾지 못한 행**이다. 같은 형태가 다른 문장으로 저장되어 있을 수 있으므로 곧바로 의미 누락 127개라고 계산하지 않는다. 반대로 표현이 있어도 다른 운반체나 변형일 수 있다. 현재 `오프숄더` 표현 대조에는 실제 의미가 halter인 `clt_ct038_v1`과 양쪽 어깨 아래 목선인 `clt_ct038_v2`가 함께 잡힌다. 긍정 필드의 언급을 실제 정의와 대조해야 하는 이유다. [현 레코드 발췌](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/current-positive-records.json).

**저장해야 할 독립 축**

| 축 | 표현 예 | 저장할 단서와 소유자 |
|---|---|---|
| 스타일 문맥 | Ivy, academia, gorpcore, coquette | 가변 의복 레퍼토리와 문맥. 인물의 신분·성격은 별도 |
| 의복 운반체 | coat, cardigan, dress, stocking | 같은 착용자의 어떤 의복 인스턴스인지 |
| 패널·소매·끈 구조 | raglan, corset, racerback | 연결선·개구부·스트랩의 양 끝과 토폴로지 |
| 여밈 디자인 | single/double, toggle, lace-up | 앞판·부품·루프·고리의 실제 연결 |
| 현재 착용 상태 | one-button, front tuck | 잠긴 부품·들어간 앞밑단·자유로운 옆/뒤밑단 |
| 핏·외곽 | fitted, bodycon, cocoon, barrel | 옷의 국소 접촉·거리·최대 폭·수축 |
| 길이·기준점 | cropped, midi, knee-high | 밑단·부츠 입구와 같은 인물의 기준 부위 |
| 소재 명세 | cashmere, silk, shearling, DEN | 출처 있는 기원·함량·수치. 별도 명세 사실 |
| 조직·표면 | rib, corduroy, satin, pointelle | 코·파일·실 방향·구멍·반사의 가시 단서 |
| 색·문양 | camel, tartan, paisley | 색을 가진 의복·반복 모티프·방향·크기 |
| 레이어 관계 | outer coat → inner knit | 둘 이상의 독립 경계와 위/아래 순서 |
| 커버리지 | cutout, sheer, navel visible | 원단 경계·이너 유무·실제로 보이는 지정 부위 |
| 관찰 조건 | back view, hem visible | 해당 끝점이 읽히는 시점·규모·가림 상태 |

이 축들은 상호 배타적인 옵션 목록이 아니다. “초콜릿 색, 파인게이지 리브, 피티드, 모크넥, 슬리브리스, 크롭 길이”는 한 상의에 함께 적용할 수 있다. 그 상의가 배꼽을 드러내는지는 하의 허리선과 이너·겉옷·촬영 범위를 따로 확인해야 한다.

**조사에서 중요한 의미 경계**

`드롭숄더`, `래글런`, `오프숄더`는 서로 다른 속성이다. 드롭은 소매 연결선이 어깨 기준점보다 낮은 구조이고, 래글런은 목선에서 암홀 쪽으로 이어지는 사선 연결이다. 오프숄더는 의복 윗경계가 양쪽 어깨 아래에 있는 변형이다. 큰 니트를 하나 넣고 세 의미를 모두 충족했다고 처리하면 연결 구조와 실제 피부 개방을 잃는다. 기존 `clt_ct044_v1/v2`와 `clt_ct038_v2`를 재사용하면서 운반체와 끝점의 표현을 보강할 수 있다. [목선 제작사 설명](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [봉제 용어](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/).

`크롭`, `로라이즈`, `미드리프`, `네이블`도 한 의미가 아니다. 상의 밑단과 하의 허리선이 겹치면 크롭이어도 복부 간격이 없다. 복부의 위쪽만 보여도 배꼽은 허리밴드 아래에 남을 수 있다. 배꼽이 요구되는 경우에는 같은 인물의 배꼽 기준점, 상의 밑단, 하의 윗선이 모두 읽혀야 한다. 기존 `pfe_navel`은 실제 배꼽과 인쇄점·피어싱·천 그림자의 구분을 이미 가진다. 이를 crop라는 넓은 별칭으로 확장하지 않는다.

`민소매`, `딥 암홀`, `사이드붑`은 종류·개구부·가시 상태다. 민소매여도 팔과 겉코트가 겨드랑이를 가릴 수 있다. 깊은 암홀 안에 이너가 남아 있으면 가슴 측면이 직접 보인다는 결론도 성립하지 않는다. `언더버스트 코르셋`은 의복의 상부 경계이고, `언더붑`은 아래쪽 피부 구역의 실제 상태다. 언더버스트 컷아웃이 상복부만 보여 주는 변형도 구분한다. 이 용어들을 연구 목록에서 제거하지 않고 `pfe_lateral_chest`, `pfe_lower_chest`와 의복 구조 의미를 각각 대조한다.

`데콜테`는 낮은 옷의 윗경계 및 거기서 드러나는 어깨·윗가슴을 가리키는 용례가 있다. `클리비지`의 신체 의미는 양 가슴 사이의 좁은 공간이다. 넓은 목선과 쇄골 가시성을 가슴골 가시성으로 바꾸지 않는다. cleavage의 의견 분열·세포분열 뜻도 별도 문맥으로 유지한다. [Cambridge décolletage](https://dictionary.cambridge.org/us/dictionary/english/decolletage), [Cambridge cleavage](https://dictionary.cambridge.org/us/dictionary/english/cleavage).

`홀터`, `스트랩리스`, `키홀`, `일루전`에서는 지지 경로와 빈 공간, 존재하는 원단층을 분리한다. 홀터는 목 뒤로 이어지는 끈·천의 구조이고, 높은 앞목선도 가능하다. 스트랩리스는 어깨끈의 부재이며 sweetheart나 일자 윗선 등 여러 변형이 가능하다. 일루전은 비치는 실제 원단이 있으므로 맨살 구멍으로 대체하면 의미가 바뀐다. [Sherri Hill 목선](https://www.sherrihill.com/blogs/news/style-guide-neckline-types), [홀터 변형](https://www.sherrihill.com/blogs/news/what-is-a-halter-dress).

`시어`에서는 앞 원단과 투과 대상의 두 소유자를 적어야 한다. 예를 들어 “시어 블라우스의 미세 망 뒤로 같은 인물의 캐미솔 목선이 보인다”는 이너 가시성 후보다. 여기서 캐미솔을 삭제해 피부를 더 보이게 만들면 동등한 표현 보강이 아니다. 원단 없는 cutout과 원단을 통과하는 sheer도 서로 다른 방식이다.

`트렌치`, `맥`, `발마칸`, `피코트`, `더플`은 코트라는 공통 운반체 아래 여러 부품·실루엣을 가진다. Burberry의 heritage trench는 벨트·견장·개버딘 등의 전통형을 설명하고, Mackintosh는 발마칸을 래글런과 간결한 앞판으로 설명한다. Gloverall의 더플은 토글-루프와 후드가 핵심이다. 특정 제품의 안감·길이·버클·모든 부품을 가족 이름 하나의 보편 의무로 만들지 않는다. [Burberry](https://int.burberry.com/c/burberry-world/heritage/trench-coat/), [Mackintosh](https://www.mackintosh.com/en-jp/blogs/guides/the-mackintosh-guide-to-wool-coats), [Gloverall](https://www.gloverall.com/blogs/journal/history-of-the-duffle-coat-origins-heritage).

`보머`와 `해링턴`은 짧은 몸판과 리브가 겹치지만 칼라·요크의 정의가 같지 않다. Baracuta의 G9는 dog-ear 칼라와 umbrella back yoke를 구체적으로 설명한다. `트러커`도 Type I의 한 포켓과 Type II의 두 포켓처럼 버전을 보존해야 한다. 데님 소재나 짧은 길이 하나가 이 구조들을 대신하지 못한다. [Baracuta](https://support.baracuta.com/en-US/what-is-a-harrington-jacket-327293), [Levi's Type II](https://www.levi.com/US/en_US/clothing/men/outerwear/type-ii-selvedge-trucker-jacket/p/A76320014).

`트윈세트`는 맞춘 두 니트의 관계이고, `원버튼 카디건 스타일링`은 현재 잠김 상태다. 전자는 서로 다른 앞판·목선과 맞춤 색·조직이 필요하고, 후자는 잠긴 단추 하나, 아래 벌어지는 두 경계, 그 사이에 보이는 이너 또는 피부가 필요하다. 단추 하나가 있는 재킷 디자인과 하나만 잠근 카디건을 합치지 않는다. 카디건·플래킷의 제작 용어와 실제 레이어 코디를 대조한 관찰 설계다. [Johnstons](https://johnstonsofelgin.com/pages/glossary), [Ralph Lauren](https://www.ralphlauren.com/rlmag/ralph-lauren-womens-layer-up.html).

`루칭`, `셔링`, `스모킹`, `플리츠`는 주름을 만든 모임·접힘·고정 방식이 다르다. 탄성실 셔링은 여러 봉제 행이 직물을 모으는 제작 방식이고, 자수 스모킹은 주름 사이의 장식 고정이 다르다. 이름의 판매 현장 혼용은 남기되 같은 사진의 아무 잔주름을 모든 기법의 증거로 사용하지 않는다. 나이프·박스·아코디언도 독립 변형이며 하나를 선택할 때 나머지 둘이 의무가 되지 않는다. [Tilly and the Buttons](https://tillyandthebuttons.com/blogs/sewing/how-to-sew-shirring), [Mood](https://blog.moodfabrics.com/moods-ultimate-list-of-sewing-terms-to-know/).

`미니·맥시·슬릿·부츠·타이츠`는 같은 다리에서 여러 경계를 만든다. 맥시 길이에 높은 슬릿이 있으면 다리 일부가 보일 수 있고, 미니라도 불투명 타이츠가 있으면 피부가 직접 보이지 않는다. 미니 밑단과 부츠 입구 사이의 구역은 피부일 수도, 타이츠일 수도 있다. 다리 가시성을 의복 길이의 부작용으로 추정하지 않고 구역의 실제 내용을 검사한다. [FALKE](https://www.falke.com/us_en/journal/tights-styling/), [Wolford](https://www.wolford.com/en-ca/our-tights-guide.html).

`DEN`은 9,000m당 질량을 나타내는 선밀도 단위다. 투명도·광택·GSM 측정값이 아니다. FALKE와 Wolford의 상품 가이드에는 다른 DEN 범위의 시어/불투명 설명이 있으므로, 브랜드별 범위를 세계 공통의 “40DEN이면 반드시 불투명” 규칙으로 저장하지 않는다. 숫자는 명세로 남기고 투과성과 표면 반사를 가시 속성으로 따로 적는다. [CottonWorks Denier](https://cottonworks.com/encyclopedia-item/denier/), [FALKE](https://www.falke.com/us_en/journal/tights-styling/), [Wolford](https://www.wolford.com/en-ca/our-tights-guide.html).

`울·캐시미어·모헤어·실크`는 섬유 기원이고, `리브·능직·새틴·포인텔`은 다른 조직·표면 범주다. 같은 옷에 여러 이름이 함께 적용될 수 있다. Satin의 매끄러운 반사는 silk 함량의 증거가 아니고, 보송한 표면도 cashmere·mohair·angora 함량의 인증이 아니다. Mohair의 Angora goat와 rabbit angora를 혼동하지 않는다. [CottonWorks 조직](https://cottonworks.com/learning-hub/weaving/basic-woven-fabric-designs/), [Woolmark](https://www.woolmark.com/en-hk/fibre/what-is-merino-wool/), [Mohair South Africa](https://www.mohair.co.za/natural-fibre).

`시어링`과 `셰르파`는 외형과 기원 모두를 봐야 한다. UGG의 twinface sheepskin은 shearling 면과 suede 면을 설명하지만, Patagonia는 “shearling fleece”라는 수식어를 100% recycled polyester 제품에 사용한다. 상품 수식어가 양가죽 기원의 인증이 되지 않는 실제 예다. 고리·파일·털 길이·매끄러운 몸판과의 경계는 가시 후보로 쓰고 재료 기원은 명세로 유지한다. [UGG](https://www.ugg.com/ca/help-center.html?a=Information-on-UGG%28r%29-and-Our-Brand---id--J6cPk4gJT4aqfLYPB4K1ig), [Patagonia](https://www.patagonia.com/product/mens-retro-pile-fleece-pullover/22695.html).

공식 용어집도 항목별로 검토했다. 열린 Johnstons 페이지의 `Intarsia` 항목에는 가벼운 실·ply 설명이 들어 있어 인타르시아 정의 근거로 채택하지 않았다. Rowan은 색면별 실을 연결하는 인타르시아와 반복색의 뒤 float를 가진 Fair Isle를 별도로 설명한다. 정면 색무늬만으로 숨은 뒷면 제작법을 확정하지 않고, 코와 색면 경계의 가시 구현을 분리한다. Rowan 직접 열기는 독일어 페이지로 리다이렉트되어 영어 검색 제공 본문을 확인한 범위로 기록했다. [Johnstons](https://johnstonsofelgin.com/pages/glossary), [Rowan](https://knitrowan.com/general-information).

`Ivy`, `quiet luxury`, `old-money`, `office siren`, `balletcore`, `coquette`에서는 스타일 문맥과 신분·행동·노출을 나눈다. FIT의 Ivy 전시는 역사적 의복 레퍼토리를 보여 주지만 착용자의 학교·자산을 판정하지 않는다. 현대 office siren 사용례도 실제 직업이나 회사 규정을 증명하지 않는다. 발레 유래 구두·랩 상의를 선택했다고 무용 동작·발레리나 역할이 필수가 되지는 않는다. [FIT Ivy Style](https://sites.fitnyc.edu/depts/museum/Ivy_Style/), [FIT Ballerina](https://exhibitions.fitnyc.edu/ballerina/), [Vogue office siren](https://www.vogue.com/article/office-siren-girlhood-trend-patriarchy).

펑크·본디지풍 스트랩은 복식사 맥락과 실제 사건을 함께 조사하되 혼동하지 않는다. V&A는 Westwood의 특정 trousers·스트랩·지퍼·찢김을 역사적 디자인으로 설명한다. 연구 데이터에는 의복 부착점·끈 경로·자유 끝을 남기고, 실제 구속·폭력·행위를 착용한 옷에서 추론하지 않는다. 요청이 실제 사건을 별도로 명시하면 그 의미는 의복 스타일과 다른 관계로 보존해야 한다. [V&A](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond).

**기존 ID를 어떻게 재사용할지**

| 연구 범위 | 현재 확인한 의미 | 반영 판단 |
|---|---|---|
| trench | `clt_ct009_v1`, `clothing_ct009_v1` | 견장·허리벨트 변형을 재사용. 전체 trench 가족의 다른 부품을 자동 의무로 추가하지 않음 |
| raglan / drop | `clt_ct044_v1/v2`, `clothing_ct044_v2` | 연결선 의미 재사용. 목선 깊이·어깨 노출과 다른 표현임을 대조 |
| halter / off-shoulder | `clt_ct038_v1/v2` | 실제 정의는 각각 목 뒤 연결 / 양 어깨 아래 경계. 씨앗 표현 이웃만으로 같은 뜻으로 합치지 않음 |
| navel | `pfe_navel_candidate`, `pfe_navel` | 실제 배꼽 기준점·연속 피부·상하의 경계의 기존 계약 재사용 |
| sideboob / underboob | `pfe_lateral_chest_*`, `pfe_lower_chest_*` | 실제 가시 상태를 재사용. 암홀·underbust 구조 별칭을 무조건 추가하지 않음 |
| garter | `pfe_garter_path_candidate`, `pfe_garter_path` | 허리 지지→연속 끈→같은 stocking welt/clip의 끝점 보존 |
| bias/drape | `bias_cut_body_skimming_drape` | 현재 문장은 넓고 명시적 관계·부분 속성이 없음. 제조 명세와 가시 drape 후보를 분리할 가치 |
| sheer layering | `ethereal_sheer_layering` | 현재는 분위기 표현이며 명시적 관계·부분 속성이 없음. 앞 원단과 투과 대상의 독립 관계를 추가할 가치 |
| Oxford / Derby | `clt_ct122_v1/v2`, `clothing_ct122_v1/v2` | vamp 위/아래 facings 연결을 재사용. Oxford 셔츠 문맥과 구분 |
| Balmacaan·Duffle·Harrington | 해당 씨앗 표현의 직접 이웃이 없음 | 기존 raglan·closure·hood·bomber 의미와 동등성 검토 후 남은 구조만 추가 |
| twinset·one-button·pointelle | 해당 씨앗 표현의 직접 이웃이 없음 | 두 의복 matching / 현재 잠김 / 규칙 eyelet의 관계를 확인해 보강 |
| 하의실종·no-pants | 해당 씨앗 표현의 직접 이웃이 없음 | 하의 존재·종류·가림을 따로 모델링. 숨은 하의를 삭제하는 표현 보강은 허용하지 않음 |

표의 `*_`는 연구에서 관련 후보·프로필 쌍을 묶어 표시한 것이다. 적용 대상은 대조표·현 레코드의 실제 개별 ID로 확정한다. 신규 의미를 기존 label에 붙이기 전에 **소유자·관찰 부위·레이어·전제·전체 효과**가 동등한지 판정한다. 다른 구체 대상이나 효과라면 별도 후보가 필요하다.

**우선순위와 반영 수량의 의미**

| 우선순위 | 원문 행 | 우선 작업 |
|---|---:|---|
| P0 | 100 | 앞뒤/상하 경계, 이너 투과, 잠김·턱인 상태, 관찰 불가 조건, 핵심 구조 혼동 |
| P1 | 199 | 개별 의복·소재·조직·문양과 기존 핏/구조의 상세 의미 재사용 |
| P2 | 48 | 가변 스타일군·색 접근 표현. 고정 신분·장면·복식 레시피를 만들지 않음 |

347행의 처리 방향은 “기존 이웃의 동등성 검토 후 재사용·보강” 202행, “동등 구조 확인 후 필요한 독립 변형만 추가” 118행, “명세와 가시 프록시 분리” 27행이다. 섬유 7행과 색 20행이 마지막 범주다. 118행은 신규 후보 추가 확정 수가 아니다. 현재 표현을 못 찾은 행을 구조 의미로 다시 찾는 단계가 먼저다.

**후보를 반영하는 단위의 예**

원버튼 카디건 가족 전체를 하나의 hard profile로 바꾸지 않고, 선택된 구체 상태를 한 문장으로 작성한다.

> One fastened cardigan button joins the front edges; below it, the edges diverge over a separate camisole.

이 문장의 운반체는 같은 인물의 카디건과 별도 캐미솔이다. 관계는 `잠긴 단추 → 두 앞판 연결`, `그 아래 앞판 → 벌어짐`, `앞판 뒤 → 같은 캐미솔`이다. 변경 범위에는 카디건 여밈 상태와 실제 레이어가 들어간다. 이너가 없다는 잠금이 있다면 이 후보는 전체 의미가 맞지 않는다. 문장에 있는 캐미솔만 지우고 동일 후보를 채택했다고 기록하지 않는다.

후보 source에는 자연스러운 `concept_units`와 구체 노드의 `relations`, 정확한 `affected_dimensions`·`affected_properties`를 작성한다. 카드의 속성 목록은 **가족 범위의 검토 입력**이므로 그대로 모든 변형에 복사하지 않는다. 소재·색·의복 추가 등 문장의 암묵 효과까지 확정해야 한다. 현재 발췌 원본에서 확인하지 못한 `wardrobe.footwear.shaft_height`, `wardrobe.surface.velvet_pile` 같은 경로는 제안이고, 현 부분 속성 잠금 계약과 먼저 대조한다. `wardrobe.fit.contact_distribution`도 선택된 발췌 이웃만으로 가용 범위를 판단하지 않는다.

프로필은 실제 선택된 한 변형의 정의상 필요한 구성 요소에 한정한다. 한 요소에 한 의무면 `authored_components/v1`, 여러 요소가 하나의 공동 관계 의무를 이루면 `v2`를 검토한다. 소유 원본에 파생 `render_gates`·`required_evidence_fields` 등을 수동 작성하지 않는다. 모든 활성 구성·관계의 근거와 원본 이미지 검사 조건은 컴파일·구성·픽셀 단계에서 각각 결속한다.

**적용 순서**

| 파동 | 변경 내용 | 완료 조건 |
|---|---|---|
| W0 | 최신 원본·dirty 작업 재확인, 용어별 동등성·추가 근거 검토 | 실제 재사용 ID·새 변형·명세 항목이 구분된 대조표 |
| W1 | 레이어·커버리지·현재 잠김·턱인·소유자 관계 | crop/mini/sheer/halter 이름만으로 unsupported visibility가 생기지 않음 |
| W2 | 가을 겉옷·트윈세트·토글·규칙 eyelet·주름 구조 | 기존 구조 재사용 후 남은 독립 변형만 추가 |
| W3 | 소재·조직·표면·문양·색과 명세 분리 | DEN·섬유 기원·숨은 제작법을 픽셀 프록시로 인증하지 않음 |
| W4 | 스타일군·한국어/영어 긍정 표현·선택 후보 보강 | 반례·출처·한계가 긍정 색인에 유입되지 않고 스타일은 가변 선택으로 유지 |
| W5 | 정식 source 등록·두 색인·BM25F·런타임 세대 | 원본·dictionary·registry·index 해시와 receipt 결속 일치 |
| W6 | 변경 범위별 회귀, 요청된 경우 이미지 검사 | 데이터·노출·선택·문장·런타임·픽셀·사용자 판단을 별도로 기록 |

원본은 현재 clothing structure, fashion fit, portrait exposure, material/style 계열부터 재사용한다. 의미가 다른 잔여 데이터가 충분할 때만 `photo_prompt_autumn_fashion_extension.json`과 대응 시각 원본을 별도로 만든다. 등록은 `photo_prompt_source_manifest.json` 한곳을 통해 한다. 후보 로더의 파일 목록·생성기·precore·creative controls·SKILL.md에 키워드별 규칙을 추가할 필요는 이번 연구에서 확인되지 않았다.

동등한 aliases·keywords만 추가해도 dictionary/registry 해시가 바뀌면 정식 semantic/BM25F/visual 색인을 갱신한다. 벡터 재사용은 전체 입력 텍스트·provider·model·dimensions·entry key가 같은 경우에 한정한다. 기존 dirty 원본을 무심코 다른 checkout으로 이동하거나 덮어쓰지 않고, 구현 시작 시 최신 증거로 분리된 작업 범위를 정한다. 런타임 세대가 source pending이거나 불일치하면 오래된 세대를 최신 결과인 것처럼 사용하지 않는다.

**검증은 무엇을 입증해야 하는가**

56개 비교는 단어를 다시 출력하는 시험이 아니다. 예를 들어 “드롭숄더”와 “오프숄더”의 코어 의미가 달라야 하고, “크롭+높은 하의 겹침”에는 배꼽 hard obligation이 생기면 안 된다. “셰르파”와 “shearling fleece”에서 보풀만으로 양가죽 출처를 확정하지 않아야 한다. 독립적으로 작성·동결한 요청을 기준으로 실제 후보 정의, 적격성, 프로필 활성화, 선택·거부, 최종 문장의 보존을 각각 검사한다.

12개 변형 반례는 소유자 바꾸기, 관계 끝점 누락, 관계 역방향, alias의 범위 확장, 대안의 all-of화, 스타일의 hard 승격, 운반체 변경을 통한 속성 잠금 우회, 반례의 긍정 색인, stale index, pack/receipt 교체, 숨은 부위 PASS, 숫자/기원의 프록시 인증을 포함한다. 새 데이터 때문에 넓은 주제 로직을 만드는 방식으로 통과시키지 않는다.

적용 후에는 dictionary validator, visual index check와 현재의 fashion fit·portrait exposure·visual obligations·visual retrieval·core retrieval·candidate semantics·BM25F·prepack isolation 테스트를 변경 범위에 맞게 실행한다. 여러 등록 원본·컴파일 계약·광범위 코퍼스를 바꾸면 전체 suite까지 확장한다. 이 연구 산출물에는 실제 적용되지 않은 후속 실행을 PASS로 적지 않았다.

12개 이미지 검사 묶음은 각 비교를 별도 요청과 원본 V6 pack·receipt에 결속한다. 같은 prompt에 키워드만 교체한 결과가 의미 비교의 독립성을 자동 보장하지 않는다. 실제 저장된 원본 해상도 이미지에서 소유자, 두 끝점, 구조, 경계의 내용, 활성된 모든 구성 요소를 검사한다. 필요한 feature가 프레임 밖·가림·너무 작음·부분 충족이면 그 hard gate는 통과하지 않는다. 제공자가 이미지를 만들지 못한 경우에는 픽셀 검사를 unscored로 남긴다.

원문 코디 12개는 유지보수 평가 요청으로 보존했다. 코드에서 키워드별 기본 레시피로 검색·주입하는 데이터는 아니다. 특히 다음 세 코디는 의상 명칭만으로 제목의 가시 효과를 보장하지 않는다.

| 원문 예 | 관찰해야 할 관계 |
|---|---|
| 슬리브리스 모크넥 + 열린 롱 코트 | 팔 자세와 코트 소매가 겨드랑이·어깨를 가리는지. sleeveless만으로 겨드랑이 가시성 PASS 불가 |
| 로백 니트 + 어깨에 걸친 울 코트 | 코트·머리·시점이 낮은 뒷목선과 열린 등을 가리는지. 정면 사진의 의복명만으로 등 구조 PASS 불가 |
| 싸이하이 슬릿 맥시 + 부츠 + 울 코트 | 같은 다리의 슬릿 위끝·겉코트·부츠·타이츠 때문에 실제 허벅지 구역이 보이는지 |

다섯 종류의 결과를 혼동하지 않는다. 연구 카드의 출처·구조 유효성, 실제 최신 원본의 색인·런타임 결속, 후보의 노출·선택, 최종 문장·런타임 요청의 의미 보존, 실제 픽셀과 전체 사진의 읽힘을 따로 기록한다. 사용자 선호·수용은 또 별도 결과다.

**현재 검증 상태**

[연구 구조 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/research-validation.json)는 원문 347행의 누락·중복 없는 카드 연결, 113개 카드·129개 초안의 ID, 출처 연결과 구체 관계의 기본 무결성을 확인했다. [보고서·계획 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/report-validation.json)는 파일 링크·실제 기존 경로·CSV/JSON·회귀 카드 참조를 확인한다. 이 결과는 구조 무결성이고 모든 현대 별칭의 사실 확증, 실제 검색 회귀, 이미지 품질을 증명하지 않는다.

이번 작업의 파일 쓰기 범위는 이 보고서와 `autumn-fashion-20261009` 연구 폴더다. 마지막 [원본 보존 대조](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/final-preservation.json)에 기준 스냅샷 이후 파일 해시·mode 변화와 기존 dirty 파일 상태를 기록한다. 적용·커밋·push 결과는 아직 없다. 후속 구현은 W0의 최신 원본 및 의미 동등성 검토에서 시작하면 된다.

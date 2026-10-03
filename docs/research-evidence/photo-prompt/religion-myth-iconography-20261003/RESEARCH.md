# 종교·신화 도상: 시각 의미와 후보팩 강화 리서치

조사일: 2026-10-03. 출발점: [종교 신화 시각자료 조사](chatgpt-conversation://6ac0522b-b354-83ec-a3ea-b51dd34dcd46). 운영 반영은 별도 작업이며, 이번 결과는 연구 데이터와 반영 설계다.

## 핵심 결론

데이터를 강화할 단위는 신·종교의 이름보다 **특정 변형에서 보이는 구성 요소, 그 요소의 소유자, 연결 관계와 사건 단계**다. 이름만 추가하면 팔 수, 지물의 손, 인간·동물 신체의 연결, 유물과 살아 있는 인물의 차이까지 잘못 고정하기 쉽다. 같은 이름에 여러 시대·지역의 도상이 있고, 서로 다른 이름이 비슷한 외형을 공유한다. 따라서 기존 의미 소유자를 먼저 비교하고, 동일 의미는 재사용하며, 다른 구조는 변형을 분리하는 방향을 권고한다.

참고 대화의 키워드 표 286행을 모두 보존하고, 박물관 소장품 기록·기관 해설·전문 연구·전통 내부의 공개 설명 111건을 검토 목록으로 만들었다. 이를 바탕으로 연구 단위 140개, 후보 초안 110개, 혼동·변형 관계 39쌍을 작성했다. 140개 중 30개는 서사·해석 또는 구체 도판이 더 필요한 맥락 단위다. **110개 초안도 원본 도판 대조와 운영 소유권 번역 전에는 채택할 수 없다.**

| 산출물 | 수량 | 의미와 한계 |
|---|---:|---|
| 참고 키워드 행 | 286 | 1–23절의 표 행. 22–23절의 중복 색인을 보존했으므로 고유 개념 286개라는 뜻은 아니다. 24절은 분류 방법이다. |
| 출처 기록 | 111 | 본문 반환 90, 검색 발췌만 20, 유효 본문 없음 1. 서로 독립적인 기관 111곳이나 검증 완료된 도판 111점이라는 뜻은 아니다. |
| 시각 의미 연구 단위 | 140 | 변형 범위·관찰 요소·소유 관계·혼동 경계·출처·후보 위치를 연결했다. |
| 후보 초안 / 맥락 단위 | 110 / 30 | 초안은 연구 전용 스키마. 맥락 단위에는 운영 후보를 만들지 않았다. |
| 키워드별 판단 | 130 / 62 / 94 | 각각 관찰 초안에 연결 / 맥락 연구에 연결 / 추가 출처 조사 필요. 행 단위 집계다. |
| 제안 회귀 사례 / 픽셀 판정 계획 | 387 / 110 | 모두 미실행. 회귀 387건은 후보당 3건, 변형 39건, 공통 계약 18건의 설계다. |

상세 내용은 [140개 단위 카탈로그](CATALOG.md), 추적은 [키워드별 판단](TERM-DECISIONS.json), 실행 순서는 [반영 계획](IMPLEMENTATION-PLAN.md)에 있다. 남은 94행도 [후속 조사 목록](FOLLOWUP-RESEARCH.md)에 개별 질문과 함께 연결했다.

## 현재 데이터와 실제 빈틈

현재 체크아웃을 읽기 전용으로 로드한 결과 슬롯 112개, 병합 후보 9,703개, 시각 의무 프로필 1,510개가 읽혔다. 신화 확장은 의미 묶음 10개·후보 60개, 전설 확장은 8개·48개다. 기존 묶음은 창세·운명·저승 하강·심장 계량·홍수·장소 전설처럼 **사건의 구조**를 주로 다룬다. 종교 도상 전용 확장 파일은 현재 로더 등록 목록에 없다. 이 수치는 [LIVE-AUDIT.json](LIVE-AUDIT.json)의 시점·Git SHA·입력 해시를 기준으로 한다.

286행의 표기를 기존 후보의 긍정 필드에서 검색했을 때 30행에 문자열 단서가 있었다. 이는 의미 충족률이 아니다. 예를 들어 `Attribute`는 일반 영어 용례에도 걸리며, 보석·복식·동물 후보에 관련 단어가 있어도 특정 도상의 손·개수·역할을 보장하지 않는다. 단어 적중은 현재 소유자를 찾는 단서로만 남겼다.

후보 초안의 우선 위치는 `composition` 24, `prop` 27, `location` 6, `action` 8, `anatomical_connection` 23, `relational_action` 7, `costume_style` 3, `body_orientation` 1, `wearable_accessory` 7, `garment_detail` 3, `surface_material` 1이다. 현재 정책에서 `prop`의 허용 차원은 빈 목록이다. 따라서 **지물·성물 27건은 속성 소유권이 해결될 때까지 묶음 채택을 보류**해야 한다. 다른 83건도 위치 제안일 뿐 실제 target/property 검증은 아직이다.

## 데이터 설계를 바꾸는 주요 발견

아래의 ‘반영’은 연구에 근거한 설계 판단이다. 기관 설명이 제시한 구성 요소를 원본 이미지에서 모두 직접 확인했다는 뜻은 아니다. 검색 발췌만 확보한 사례는 표에서 별도로 표시한다.

### 1. 같은 이름의 개수·형태를 단일 정의로 고정할 수 없다

| 조사 사례 | 확인한 차이 | 반영 |
|---|---|---|
| 차크라삼바라 | 네팔의 청색 12팔 결합형과 백색 1얼굴·2손 좌정형이 별도로 기록되어 있다. [Met 78190](https://www.metmuseum.org/art/collection/search/78190), [HAR 432](https://www.himalayanart.org/items/432) | 이름만으로 12팔·결합 상대·자세를 의무화하지 않는다. `chakra_blue12`, `chakra_white2`를 분리한다. |
| 헤바즈라 | 선정 자료는 8얼굴·16손과 손마다 든 해골잔을 구별한다. [HAR 90531](https://www.himalayanart.org/items/90531) | 얼굴·손의 개수와 소유된 잔을 별도 검증하고, 일반 얍윰 후보로 축약하지 않는다. |
| 두르가 | 참바 지역 12세기상은 8팔의 공격 장면이다. 캄보디아 900년대상은 4팔과 바퀴·소라·곤봉·흙덩이 지물을 가진다. [Met 74502](https://www.metmuseum.org/art/collection/search/74502), [Cleveland 1996.27](https://www.clevelandart.org/art/1996.27) | 팔 수와 지물만이 아니라 사건 단계도 분리한다. 두 변형을 하나의 ‘여신 전투’ 프리셋으로 합치지 않는다. |
| 가네샤 | 타밀 지역 12세기상은 코끼리 머리의 인간형 몸에 4팔, 밧줄·도끼·과자·부러진 엄니가 손별로 배치된다. [Met 37397](https://www.metmuseum.org/art/collection/search/37397) | 이 작품의 actor-relative 손을 기록한다. 일반 가네샤 요청에 모든 세부를 강제하지 않는다. |
| 나가 | 일곱 후드가 감긴 좌대로 중앙 불상을 받치는 단편과, 인간 상체·뱀 하체를 가진 다섯 나가가 얽힌 네팔 용기 손잡이는 다른 구조다. [Met 38451](https://www.metmuseum.org/art/collection/search/38451), [Met 39389](https://www.metmuseum.org/art/collection/search/39389) | ‘다섯 개체’와 ‘한 몸의 다섯 머리’를 구별한다. 단편의 없는 머리·팔다리는 원본 관찰로 추정하지 않는다. |

### 2. 지물의 존재보다 소유자·손·지지 관계가 중요하다

| 조사 사례 | 확인한 관계 | 반영 |
|---|---|---|
| 나타라자 | 선정 촐라상은 상단 오른손 북·상단 왼손 불, 오른손의 보호 제스처, 든 왼발을 가리키는 앞 왼팔, 아파스마라를 밟은 오른발을 연결한다. [Met 39328](https://www.metmuseum.org/art/collection/search/39328) | 화면 좌우와 인물 자신의 좌우를 구별한다. 북·불이 배경에 있거나 손이 바뀌면 의무 충족이 아니다. |
| 바즈라바라히 | HAR의 적색 변형은 오른손 곡도, 왼손 해골잔, 왼쪽 팔꿈치의 카트방가, 별도의 작은 멧돼지 머리를 설명한다. [HAR 94](https://www.himalayanart.org/items/94) | 몸 전체가 멧돼지 머리인 바라히와 자동 병합하지 않는다. 작은 머리의 위치 변형과 지물 소유를 보존한다. |
| 성 루치아·바르톨로메오 | 루치아의 눈은 접시에 든 지물이며, 바르톨로메오의 칼은 식별 지물이다. [National Gallery 루치아](https://www.nationalgallery.org.uk/paintings/carlo-crivelli-saint-lucy), [바르톨로메오](https://www.nationalgallery.org.uk/paintings/glossary/st-bartholomew) | 지물 요청에서 얼굴 훼손이나 박피 사건을 자동 추가하지 않는다. ‘눈–접시’와 ‘칼–보유자’ 관계를 보존한다. |
| 아가타 속성을 가진 초상 | 작품 제목 자체가 ‘성 아가타의 속성을 지닌 여인의 초상’이며, 성인의 실제 초상으로 단정되지 않는다. [National Gallery NG24](https://www.nationalgallery.org.uk/paintings/sebastiano-del-piombo-portrait-of-a-lady-with-the-attributes-of-saint-agatha) | 표현된 지물과 인물의 정체를 다른 필드로 둔다. 실제 참조 인물의 신앙·신분으로 전이하지 않는다. |
| 성유물함 | 남네덜란드 팔형 성유물함은 금속 외함과 두 창을 가진 용기다. [Met 471270](https://www.metmuseum.org/art/collection/search/471270) | ‘팔형 용기’와 ‘살아 있는 인체’의 타입을 분리한다. 가려진 내용물·진위·효능은 픽셀 판정 대상에서 제외한다. |

관계 이름만 넣고 양 끝 대상을 모호하게 두면 이 강화가 무효가 된다. 연구 관계의 `anubis`, `scale`, `actor_a.hand` 같은 엔티티는 실제 frozen core의 대상에 연결되어야 하며, 후보가 새로운 인물을 덧붙이는 근거가 되지 않는다.

### 3. 가까운 도상은 다르게 취급하되, 문헌에 기록된 혼합형을 허용해야 한다

호데게트리아의 가리키는 손과 엘레우사의 친밀한 얼굴 관계는 중요한 구별점이다. 그러나 Met의 13세기 이콘은 호데게트리아 변형으로 분류되면서 아이의 얼굴·몸 방향에 다른 관계가 섞여 있다. 전역적인 상호 배타 alias 규칙은 이 작품을 잘못 배제할 수 있다. **기본 구별 규칙과 자료로 특정한 혼합 변형을 함께 둬야 한다.** [Met 이콘 해설](https://www.metmuseum.org/essays/icons-and-iconoclasm-in-byzantium), [Met 831188](https://www.metmuseum.org/art/collection/search/831188)

미투나·마이투나·얍윰·아르다나리슈바라·레비스는 결합이라는 단어를 공유해도 구조가 다르다. 선정 미투나 부조는 두 연인의 포옹과 시선을 설명하고, 캄보디아 아르다나리슈바라는 시바·파르바티가 한 몸의 양쪽을 이룬다. 미투나라는 이름만으로 성교를 추가하거나, 한 몸의 양면을 두 머리 레비스로 바꿔서는 안 된다. 아르다나리슈바라 기록은 2023년 12월 반환된 작품이므로 현재 Met 소장이라고 표기하지 않는다. [Met 38141](https://www.metmuseum.org/art/collection/search/38141), [Met 39198](https://www.metmuseum.org/art/collection/search/39198)

피에타의 성인 그리스도–마리아 무릎 지지 관계와 성모 안식의 누운 마리아–그리스도가 든 영혼 표상은 인물 역할·크기·표현 타입이 다르다. 후자의 세부는 현재 검색 발췌 근거이며 원본 대조가 필요하다. [Met 피에타](https://www.metmuseum.org/art/collection/search/473331), [Smarthistory 장면 분류](https://smarthistory.org/the-lives-of-christ-and-the-virgin-in-byzantine-art/)

### 4. 기존 심장 계량 프로필을 재사용할 범위와 분리할 범위가 다르다

현재 `egyptian_heart_weighing_judgment`는 심판 대상, 심장–깃털 저울, 아누비스, 토트, 결과를 나타내는 암미트 또는 오시리스의 **5개 필수 그룹**을 가진다. 이 의미 소유자를 유지하며 아니 파피루스 관련 출처와 역할 구별을 보강하는 것이 우선이다.

그린필드 파피루스 기록에는 반대 접시에 단독 깃털 대신 깃털 머리 장식을 한 작은 마아트 상이 있는 변형이 제시된다. 이 경우 기존 `heart_feather_balance`의 의미를 몰래 넓히면 기존 계약이 무너진다. `heart_maat_figure`는 별도 변형 초안으로 두고, 요청이 이 변형을 지정했을 때 기존 일반 프로필과 충돌하지 않도록 현재 데이터 계약이 표현 가능한지 먼저 확인한다. 두 BM 기록은 이번 조사에서 검색 발췌만 확보했으므로 도판 검토 전 활성화를 보류한다. [BM EA10470-3](https://www.britishmuseum.org/collection/object/Y_EA10470-3), [BM EA10554-80](https://www.britishmuseum.org/collection/object/Y_EA10554-80)

### 5. 개수는 가지·개체·머리·수용 위치 중 무엇을 세는지 명시해야 한다

| 조사 사례 | 계수의 단위 | 반영 |
|---|---|---|
| 하누키아 | Wolpert 작품은 반원형의 여덟 심지 홀더와 별도의 작은 샤마시 용기다. [Jewish Museum 1527](https://collections.thejewishmuseum.org/collection/1527-hanukkah-lamp) | 9개의 점화 위치를 9개 가지로 번역하지 않는다. 7가지 메노라는 별도 소장품 조사 전 통합하지 않는다. |
| 켄타우로스 | 네소스의 초기 도상에는 사람 무릎이 남아 있고, 폴로스는 보통 기대하는 사람 복부 없이 인간 다리가 말 몸에 직접 연결되는 것으로 설명된다. [Met 248578](https://www.metmuseum.org/art/collection/search/248578), [Met 248101](https://www.metmuseum.org/art/collection/search/248101) | 일반형에 항상 말 다리 네 개를 강제하지 않는다. 작품이 설명하지 않은 총 다리 수는 추정하지 않는다. |
| 키마이라 | 사자 몸, 등에 난 염소 머리, 뱀 머리의 꼬리가 한 개체에 연결된다. [Getty 도상 레코드](https://www.getty.edu/cona/CONAIconographyRecord.aspx?iconid=901000661) | 세 동물을 나란히 놓은 구도나 막연한 혼합 생물과 구별한다. |
| 케르베로스 | CVA 검색 발췌에는 두 머리와 머리 위의 뱀 표지가 기술된다. 해당 도판·소장번호는 아직 미확정이다. [Met CVA 자료](https://resources.metmuseum.org/resources/metpublications/pdf/Attic_Black_Figured_Neck_Amphorae_Corpus_Vasorum_Antiquorum_Fascicule_4.pdf) | 두 머리 변형을 연구 보류 상태로 둔다. 세 머리 중 하나가 가려진 이미지와 구별해야 한다. |
| 슬레이프니르 | 자료는 한 말 몸에 여덟 다리를 가진 표상을 다룬다. [Historiska 그림 돌 자료](https://dev.vikingar.historiska.se/objects.php?e=no&l=en&showcase=772a155d-bfbc-4107-9ab3-2f61d275d838) | 두 마리 말의 겹침으로 대체할 수 없다. 요청상 필수 다리가 가리면 `UNOBSERVABLE`이며 통과가 아니다. |

### 6. 전통·지역·재료와 표현 매체를 보존해야 한다

| 사례 | 관찰 가능한 구별과 반영 |
|---|---|
| 그리스 세이렌 | 선정 자료의 인간–새 구조를 현대의 물고기 꼬리 인어와 구별한다. 그리스 스핑크스와 이집트 스핑크스도 한 후보로 합치지 않는다. [Getty 세이렌](https://www.getty.edu/publications/terracottas/catalogue/2/), [Met 그리스 스핑크스](https://www.metmuseum.org/art/collection/search/329999) |
| 부라크 | 골콘다 1660–80년 작품은 여성 얼굴과 여러 작은 동물로 구성된 몸을 가진 독립 표상이다. 일반 날개 말이나 모든 부라크의 정의로 고정하지 않는다. [Met 453334](https://www.metmuseum.org/art/collection/search/453334) |
| 이슬람 미술 | 종교 공간·세속 문맥의 인물 표현이 다르다. 이슬람이라는 이름만으로 인물 전체를 배제하는 규칙은 자료와 맞지 않는다. [Met Figural Representation](https://www.metmuseum.org/essays/figural-representation-in-islamic-art) |
| 도교 의례복 | 선정 청대 의례복의 해·금까마귀, 달·옥토끼, 두루미, 거북–뱀 자수는 **옷의 표면 요소**다. 착용자의 해부 구조나 모든 도교 복식의 필수 문양으로 옮기지 않는다. [Met 68508](https://www.metmuseum.org/art/collection/search/68508) |
| 한국 산신도·솟대 | 산신도의 노인·호랑이 일반형에는 여성·호랑이 없는 예외가 있다. 솟대의 세 가지·세 새는 특정 형태이지 모든 솟대의 정의가 아니다. [한국민족문화대백과 산신도](https://encykorea.aks.ac.kr/Article/E0026273), [솟대](https://encykorea.aks.ac.kr/Article/E0030608) |
| 마앙가카 은콘디 | 손을 허리에 둔 상, 몸의 금속물, 복부 약물 공간과 공동체적 역할을 구별한다. ‘주술 인형’이라는 이름으로 인간 상해나 임의의 저주 사건을 추가하지 않는다. [Met 320053](https://www.metmuseum.org/art/collection/search/320053) |
| 에궁군·드라포 | 소장 에궁군 **속옷 한 점**을 완전한 공연 의상으로 단정하지 않는다. 천·구슬·스팽글의 드라포와 바닥에 그린 베베는 매체가 다르다. [Met 315912](https://www.metmuseum.org/art/collection/search/315912), [Fowler 드라포](https://fowler.ucla.edu/exhibitions/saluting-vodou-spirits-haitian-flags-from-the-fowler-collection/) |
| 메소아메리카 공놀이 | 아차의 각진 홈은 요크와의 결합 단서이며 일반 손잡이 도끼와 다르다. 돌 장비의 의례용 복제품과 실제 경기 착용 장비를 구별하고, 공놀이 이름에서 패자 희생을 자동 추론하지 않는다. [Met 310474](https://www.metmuseum.org/art/collection/search/310474), [Met 공놀이 해설](https://www.metmuseum.org/essays/the-mesoamerican-ballgame) |
| 헤이 티키·응갈료드 | 특정 헤이 티키의 포우나무·파우아 눈과 서부 아넘랜드의 응갈료드 작품은 지역·작품 범위를 가진다. ‘태평양 티키’, ‘무지개 뱀’으로 평탄화하거나 모든 공동체의 보편 도상으로 확장하지 않는다. [Te Papa 56145](https://collections.tepapa.govt.nz/object/56145), [National Museum of Australia](https://www.nma.gov.au/exhibitions/old-masters/western-arnhem-land) |

### 7. 도표·문자는 장식 패턴과 다르고, 역사적 연대도 수정이 필요하다

레비스 자료에는 두 머리·한 몸의 1584년형과, 두 상체가 엉덩이에서 연결되고 세 다리·불사조가 결합된 15세기형이 구별된다. 특정 레비스 이름에 현대의 단일 실루엣을 강제해서는 안 된다. [Warburg 도상 비교](https://historycollections.blogs.sas.ac.uk/2025/10/22/warburg-afterlife-of-alchemy/)

실제로 회전층을 가진 볼벨과 인쇄된 립리 휠은 원형이라는 외형이 비슷해도 구조가 다르다. 고정된 동심원 도표를 기계식 볼벨로 변환하거나 한 장의 사진에서 회전 작동을 인증하지 않는다. [Getty 연금술 자료](https://www.getty.edu/research/exhibitions_events/exhibitions/alchemy/), [Science History Institute 립리 휠](https://digital.sciencehistory.org/works/0c483k14n)

원 대화의 바포메트 최초 도상 연도 ‘1856’은 수정해야 한다. Strube의 연구는 레비 그림의 첫 등장을 1854년 분책에 두고, 1855–56년 합본·후속 판본을 구별한다. 레비 전신 그림, 염소 머리 역오각별, 현대 동상은 같은 후보가 아니다. 제스처·문자 배치는 선정 판본 도판 대조 후 기록한다. [Strube 2016 논문](https://publikationen.uni-tuebingen.de/xmlui/bitstream/10900/141891/1/Strube_019.pdf)

스리 얀트라·세피로트·종자자는 원본의 선 연결·포함 관계·문자·방향을 확인해야 한다. ‘신비한 원형 문양’이라는 긍정 검색어만 늘리면 다른 도표와 섞인다. 이번에는 도표 초안과 맥락을 나눴으며, 정확한 도표 재현에 필요한 원본 노드·간선·문자 전사는 다음 조사 항목으로 남겼다. [National Library of Israel 도표 자료](https://blog.nli.org.il/en/djm_ilanot/)

## 공통 의미 데이터 모델

다음 축을 출처별 연구 레코드에 둔다. 모두 검색 점수나 인물의 실제 속성을 뜻하지 않는다.

| 축 | 기록할 내용 | 적용 예 |
|---|---|---|
| 변형 범위 | 지역·시기·제작자/전통·판본·소장번호·보존 상태 | 촐라 나타라자, 그린필드 계량형, 단편 나가상 |
| 표현 모드 | 유물 기록 / 요청에 따른 도상 재구성 / 도표·도해 / 공연·복식 | 성유물함 외함과 사람 팔, 가면과 연기자의 얼굴을 구별 |
| 개체·부분 타입 | 표현된 신·인물·동물, 개체 수, 머리·팔·다리 수, 재료 표면 | 몸 하나에 두 머리인지, 두 개체인지 |
| 지물 소유 | 지물–실제 core 대상–손·몸·받침의 연결 | 북·불의 손 바뀜, 눈–접시 |
| 연결 구조 | 붙음·감쌈·지지·포함·위아래·향함 | 키마이라의 등 머리·뱀 꼬리, 마리아 무릎 지지 |
| 사건 단계 | 정지 지물 / 행위 중 / 결과·흔적 | 칼 보유와 박피 사건, 전투와 이미 승리한 표상 |
| 도표 구조 | 노드·간선·중심·방향·층·문자의 정확한 관계 | 세피로트·얀트라·볼벨 |
| 혼동 경계 | 가장 가까운 다른 변형·매체·의미와 구별점 | 바라히/바즈라바라히, 메노라/하누키아 |
| 비시각 맥락 | 효능·신앙·서사·해석·출처의 불확실성 | 길상성, 보호 기능, 종교적 효능은 외형만으로 판정하지 않음 |

유물 기록 요청에서는 원래의 재료·매체·결손을 보존한다. 재구성 요청에서는 요청이 지정한 변형과 복원 범위를 core에 명시한다. 자료에 없는 얼굴·의상·행위는 후보가 완성하지 않는다. 사진 속 사람의 종교·민족·정체, 동의·욕망·의례의 효능은 도상이나 복식에서 추정하지 않는다.

## 의미 의무와 후보팩의 분리

**의무 활성화는 검증된 요청과 frozen core가 소유한다.** BM25F·임베딩은 후보 발견을 돕는 수준이다. 검색에서 나타났다는 이유, 후보를 골랐다는 이유, 출처 해설에 단어가 있다는 이유만으로 hard profile을 켜지 않는다. 일반 이름이 여러 변형을 가리키면 한 변형을 임의 확정하지 않는다.

110개 초안의 `affected_properties_draft`는 실제 운영 property라고 확인되지 않은 제안 경로다. target도 `<bind_actual_frozen_core_target>`로 남겨 실제 연결 전 사용을 막았다. 복합 관찰은 구도·동작·외형·몸 구조로 분해해야 한다. 예를 들어 나타라자 한 문장을 `action` 후보 하나에 넣고 북·불·팔 구조·구도 전체를 바꿀 권한을 주어서는 안 된다.

자료 설명·반례·신앙적 해석은 유지보수 근거에 보관한다. 긍정 검색 필드에는 해당 후보가 실제로 표현하는 표기만 둔다. 부정 문장, 이웃 변형, 연대 설명을 검색 필드에 복사하면 부정된 도상이 오히려 노출될 수 있다. 22–23절 색인 표기는 기존 단위로 연결하며 새로운 중복 의미 소유자를 만들지 않는다.

반영 순서는 **A: 소유 지물·복식·공간·구도 41건 → B: 복수 인물·신체 연결·변형 47건 → C: 복잡한 개수·도표·판본 22건**으로 제안한다. 각 단계에도 출처·소유권 보류 조건이 우선한다. `prop` 보류를 순서 번호만으로 해제하지 않는다. 전체 연구 단위를 실행 묶음으로 나눈 [BATCH-PLAN.json](BATCH-PLAN.json)에 구성원과 보류 사유를 기록했다.

## 검증 설계와 현재 증거의 범위

운영 검증은 입력 스키마·기존 소유권, 요청 활성화·부정어, 후보 노출·채택·잠금, 실제 생성 이미지, 사용자 수용을 각각 확인해야 한다. 연구 파일의 정합성 통과가 이 단계들의 통과를 대신하지 않는다.

픽셀 계획은 선정 변형의 필수 구성 요소와 관계를 **모두** 확인한다. 요청상 필수 요소가 일부만 보이면 `partial_is_fail`; 가림·해상도 때문에 판단할 수 없으면 `UNOBSERVABLE`이며 통과가 아니다. 원본 전체와 원본 해상도 부분을 함께 검토한다. 가려진 내용물·보이지 않는 손·도상 밖의 이야기, 실제 움직임, 신앙의 진위는 픽셀로 인증하지 않는다. 일반 요청에 없는 모든 변형 세부를 필수 의무로 확장하지도 않는다.

이번에 수행한 것은 참고 대화 수집, 출처 텍스트·검색 발췌 조사, 현재 로더 읽기, 연구 파일 교차 참조·스키마·로컬 링크 검증이다. 원본 도판 직접 대조, 운영 데이터 반영, 후보팩 실행, 제안 회귀 실행, 이미지 생성·네이티브 픽셀 판정, 사용자 수용 평가는 수행하지 않았다. 출처 접근 상태와 남은 검토는 [SOURCES.json](SOURCES.json), 현재 검증 결과는 [VALIDATION.json](VALIDATION.json)에 있다.

본문이 반환됐어도 기관 첫 화면·리디렉션·메타데이터만 온 기록이 있을 수 있다. `PAGE_TEXT_RETURNED`는 관련 모든 세부가 본문에서 검증됐다는 표시가 아니다. 원본 대화의 설명도 독립 근거가 아니며, 검색 발췌에만 있는 케르베로스·일부 BM 자료는 활성 데이터로 승격하기 전 정확한 객체와 도판을 다시 확인해야 한다.

## 파일 안내

- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md): 기존 계약에 맞춘 파일·소유권·활성화·검증·회복 순서.
- [CATALOG.md](CATALOG.md): 140개 단위별 관찰 요소·관계·혼동·출처.
- [SEMANTIC-UNITS.json](SEMANTIC-UNITS.json): 연구 의미 데이터. runtime 스키마가 아니다.
- [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json): 110개 후보 관찰 초안과 소유권·출처 보류.
- [VARIANT-RELATIONS.json](VARIANT-RELATIONS.json): 39쌍의 변형·혼동 경계. alias 병합표가 아니다.
- [REFERENCE-KEYWORDS.json](REFERENCE-KEYWORDS.json), [TERM-DECISIONS.json](TERM-DECISIONS.json): 원 대화 286행과 모든 행의 처리 판단.
- [FOLLOWUP-RESEARCH.md](FOLLOWUP-RESEARCH.md): 남은 94행의 구체 조사 질문과 맥락 62행 보강 범위.
- [SOURCES.json](SOURCES.json): 출처 111건의 URL·범위·접근 상태·증거 영수증.
- [BATCH-PLAN.json](BATCH-PLAN.json): 후보 초안 110건의 단계·실행 묶음·선행 조건.
- [REGRESSION-PROPOSALS.json](REGRESSION-PROPOSALS.json), [PIXEL-GATES.json](PIXEL-GATES.json): 미실행 검증 설계.
- [LIVE-AUDIT.json](LIVE-AUDIT.json), [VALIDATION.json](VALIDATION.json), [MANIFEST.json](MANIFEST.json): 현재 로더·입력 해시·연구 정합성·산출물 해시.


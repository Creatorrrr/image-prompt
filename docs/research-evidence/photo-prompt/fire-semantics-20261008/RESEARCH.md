# 불 관련 시각 의미·후보 데이터 강화 리서치

기준일: 2026-10-08, Asia/Seoul  
참조 대화: [불 관련 용어 조사](chatgpt-conversation://6ac643fe-2ae4-83e8-9fa1-319efc43d63e)  
작업 기준 checkout: main, `629bf4a88e1f1f524d177d67c09615a7fdb4f89d`

조사 중 별도 VEL 확장 커밋 `30fc97a8`과 작업 semantic index 변경이 관찰됐다. 작업 index는 새 커밋의 blob과도 다르며 작성 원인은 확인하지 않았다. 기존 authored asset JSON과 현재 검증용 Python 구현은 비교 범위에서 동일했고, 관찰된 Git·index 변경을 보존했다. [동시 변경 기록](LIVE-DRIFT-NOTE.md)에 최신성·보존 검증의 범위를 명시했다.

## 1. 조사 결과와 반영 방향

불을 한 가지 색이나 효과로 저장하면 연소 화염, 고체 잔불, 공중 입자, 표면 흔적, 조명, 태양 관측, 카메라 광학이 서로 섞인다. 이번 확장은 **무엇이 어디에 있고, 무엇에서 나와, 어떤 표면·매질·대상과 연결되는지**를 중심으로 설계했다.

20개 영역에 시각 의미 카드 155개를 작성했다. 그중 관찰 가능한 실현 124개와 창작 실현 7개를 후보 초안 131개로 만들고, 사진의 사실로 직접 확인할 수 없는 과정·감각·동기 등은 맥락 카드 24개로 보존했다. 관계 프로필은 현행 `authored_components/v2` 형태의 프로토타입 18개를 준비했다. 이 프로토타입에서 evidence field 54개와 gate 72개가 컴파일되는 것을 확인했다.

추가로 공동 채택 관계 7개, 회귀 비교·변이 사례 44쌍, 원본 픽셀 검증 사례 10개를 설계했다. 이 수치는 연구 산출물의 범위다. 등록·검색 성능·후보팩 노출·최종 프롬프트·이미지 품질을 검증한 수치가 아니다.

반영은 물리적 불·잔불·불티·불빛·연기·열손상을 먼저 진행하고, 기존 우주·카메라 데이터와 동치인 항목은 재사용한다. 문화·판타지·신체·폭력·관능·비유는 자체 맥락을 유지하되 일반 fire 토큰의 기본 장면에 섞지 않는다.

## 2. 참조 대화의 확인 범위

대화 도구로 user message와 assistant message를 읽었다. assistant 본문은 최대 20,000자 제한 때문에 16절의 “스피큘 —” 직전에 잘렸다. 1–15절과 16절의 완결된 표 행에서 **키워드 278개**를 확보했다. 원문과 잘린 위치는 [SOURCE-CONVERSATION.json](SOURCE-CONVERSATION.json), 실제 추출 행은 [SEED-INVENTORY.json](SEED-INVENTORY.json)에 보존했다.

조회된 278개 행은 모두 시각 카드 또는 맥락 카드에 연결했다. [SEED-COVERAGE.json](SEED-COVERAGE.json)은 이 누락 방지 기록이다. 각 행의 원 정의를 독립적으로 모두 검증했다는 뜻은 아니다. 여러 카드에 연결된 용어도 모두 동의어가 되는 것은 아니며, 배색·용암 등에 걸린 일부 연결은 혼동 경계를 설명하는 참조다.

대화 도입부가 언급한 광학·신화·의례·전쟁·신체·관능·비유 영역은 보충 조사로 확장했다. 해당 영역의 후반 세부 키워드를 원 대화에서 모두 가져왔다고 주장하지 않는다. 렌즈 플레어, 세인트엘모의 불, 오로라, 용암, 유성 화구, 도상 후광, 성화 전달, 촛농 접촉, 화염 무기, 감정의 불 비유 등이 이 보충 영역에 포함된다.

## 3. 근거 수준과 현재 데이터 상태

[NIST](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [NASA](https://science.nasa.gov/sun/facts/), NWCG, NOAA, 호주 기상청, ACS, RSC, 박물관, 광학·용접 기관 등 **1차 또는 기관 출처 42개**를 사용했다. [SOURCES.md](SOURCES.md)와 [SOURCES.json](SOURCES.json)에 URL, 확인일, 지원하는 주장, 접근 수준과 제한을 기록했다.

관련 본문·PDF 발췌를 읽은 출처는 22개, 저자 초록은 3개다. 나머지 17개는 공개 검색 문구와 페이지 정보 범위로 확인했다. 일부 RSC·NWCG·ZEISS·IWM·ACS 페이지는 403/405/502 또는 시간 초과로 전문 접근이 제한됐다. PDF의 앞부분만 반환된 자료도 관련 검색 문구 범위를 넘겨 해석하지 않았다. 따라서 “42개 전문 검토 완료”라고 보고하지 않는다.

출처가 직접 지원하는 것은 과학적 정의·현상 경계·특정 도구나 도상이다. 각 카드의 3개 구성요소, 프레이밍, owner 역할, 후보 문구, gate는 이 연구에서 설계한 시각적 투영이다. 과학적 개념마다 필수 3요소가 있다는 뜻도 아니고, 후보를 3요소로 복사해야 한다는 요구도 아니다.

현재 manifest에 등록된 candidate/profile 파일만 대상으로 관련 문자열을 조사했다. 결과는 후보 39개, 프로필 17개, 총 56개 lexical hit다. 우주·광학·펑크·상상·종교·의복 등으로 분산되어 있었다. 독립 fire 확장 파일은 없었다. 이 결과는 **어휘 탐색**이며 의미 동치·실제 검색 도달성·시각 품질의 판정은 아니다. 전체 결과는 [EXISTING-DATA-CATALOG.json](EXISTING-DATA-CATALOG.json)에 있다.

이미 확인한 재사용 대상은 다음과 같다.

|연구 카드|현재 원본 ID|검토 방향|
|---|---|---|
|F131 베일형 플레어|`pe_veiling_flare`|광원 쪽 대비 감소 의미를 유지하고 연구 provenance 연결|
|F132 분리형 고스트|`pe_aligned_ghosts`|광원 정렬·image-plane 소유가 동치인지 확인|
|F133 수평 플레어|`pe_horizontal_anamorphic_streak`|실제 장면의 선·화염 제트와 경계 보강|
|F127 CME|`coronal_mass_ejection_observation_subject`|coronagraph 판본과 다른 관측 판본을 구분|
|F135 빛 번짐 경계|`pe_local_bloom_relation` 등|기존 style/image-plane 효과와 lens 내부 반사의 차이 검토|

기존 후보의 “camera / image_plane / optical.lens_artifact” 경로는 직접 확인했다. 새 불·연기·재료·신체 target/property 제안은 consumer 연결 검증 전이다. 의미가 비슷하다는 이유만으로 새 경로를 유효한 runtime owner라고 간주하지 않는다.

## 4. 연소 화염·잔불·불티를 구별하는 기준

|대상|관찰해야 하는 형태와 관계|대표 혼동|
|---|---|---|
|화염 F001/F002|심지·연료 표면에 붙은 연속 발광 영역|떨어진 불티·그을린 연료·용암|
|잉걸불 F003|고체 조각 안 발광 부위와 연결된 어두운 표면|공중의 불꽃 덩어리·붉은 페인트|
|불티 F004|화원과 분리된 작은 발광 입자|렌즈 고스트·보케·반짝이는 먼지|
|비화물 F005|타거나 달아오른 연료 조각의 형태·이동 문맥|무조건 새 불이 붙었다는 사건|
|훈소 F006|선택된 다공성 연료와 국소 연기·발광의 연결|모든 훈소에 큰 화염·발광 필수화|
|열분해 F009|열에 의한 분해라는 과정 문맥|현재 화염·완전연소와 동치|
|점화 F007|점화원–같은 연료 가장자리의 접촉|자연발화·자동발화 원인 확정|

NIST는 열분해를 열에 의한 분해로 설명하고 연소에 선행할 수 있다고 구분한다. 촛불에서는 왁스가 심지를 통해 이동·기화하고 그을음 발광이 황색광에 기여한다. 이 근거를 물질–심지–화염의 연결로 투영했다. [NIST 열분해](https://www.nist.gov/glossary-term/30146), [ACS 촛불](https://inchemistry.acs.org/atomic-news/shining-light-on-candles.html).

F006과 F008의 선택적 실현에는 연기와 잔류물을 넣었지만, 훈소·소염이라는 말 전체에 같은 장면을 강제하지 않는다. 한 장의 사진은 완전 소화·잔열 부재·안전 상태를 확인해 주지 않는다.

## 5. 화염 구조·형상·시간을 서로 다른 축으로 저장

예혼합·확산은 혼합 경로, 층류·난류는 유동 상태, 부력·제트는 힘과 공급 경로의 구분이다. 청색 원뿔이나 매끄러운 외피는 유용한 외형 실현이지만 그것만으로 연료·혼합·온도를 확정하지 않는다. F011–F018에 이 경계를 기록했다.

지상 촛불의 길쭉한 형상에는 부력 대류가 관여한다. 미소중력 실험에서 구형 화염이 관찰되지만 “우주 진공에서 저절로 타는 불”의 근거가 아니다. [NASA 미소중력 화염](https://science.nasa.gov/biological-physical/resources/explainers-infographics/why-nasa-is-studying-flames-in-space/).

냉염은 특히 맥락 카드로 남긴다. NASA의 해당 실험에서는 빛이 희미해 실시간 영상에 보이지 않았고 계측으로 확인했다. 따라서 선명한 청색 구체·만져도 되는 불·얼음 불꽃을 냉염의 필수 형태로 등록하면 잘못된 지식이 된다. [NASA 냉염 연구](https://www.nasa.gov/missions/station/cool-flames-created-during-a-first-for-international-space-station-research/).

리본·기둥·장벽·커튼·고리·왕관은 형상과 배열의 표현이다. 펄럭임·맥동·급격한 확대는 시간적 상태다. 정지 외형에서 시간 변화 자체를 판정하지 않는다. 불티 궤적은 입자의 운동과 카메라 노출이 함께 관여할 수 있어 F030에서 capture 관계를 분리했다.

## 6. 색·불빛·열·카메라 효과의 소유 분리

불꽃색은 열뿐 아니라 발광 성분의 영향을 받는다. RSC의 불꽃반응 자료도 물질에 따라 다른 발광색을 다룬다. “청색이면 항상 더 뜨겁다”, “구리색이면 구리 성분이다” 같은 보편 규칙을 만들지 않는다. [RSC 불꽃색](https://edu.rsc.org/resources/flame-colours-a-demonstration/760.article).

|카드|소유와 관계|구현에서 피할 오류|
|---|---|---|
|F031/F032 적열·백열|같은 고체의 국소 발광|반사·페인트·센서 포화를 intrinsic emission으로 처리|
|F037 불빛|`fire_source → receiver_surface` 조명|피부색·소재색·전역 grade로 대체|
|F038 화면 밖 불빛|요청이 소유한 offscreen source와 보이는 수광면|보이지 않는 화원을 pixel gate로 요구|
|F039 불 반사|실제 화원–같은 수면의 반사|수중 불·별도 화원 복제|
|F041 열 아지랑이|열원 위 공기 경로–배경 경계 왜곡|전역 defocus·물체 변형·연기로 대체|
|F131/F132 플레어|카메라의 image plane와 광원|입자나 실제 장면 객체로 생성|
|F134 회절별|점광원 중심의 광학 광선|태양 플레어·폭발로 생성|

열방출률·열유속·온도는 각각 다른 양이다. 소리·냄새·맛·잔열은 보편적인 가시 형태가 없어 F043/F044에 맥락으로 보존했다. 열 아지랑이는 온도·밀도 차이에 의한 굴절 설명을 바탕으로 배경 경계의 국소 왜곡으로 투영한 제안이다. [NIST Fire Dynamics](https://www.nist.gov/el/fire-research-division-73300/firegov-fire-service/fire-dynamics), [OpenStax 굴절](https://openstax.org/books/physics/pages/16-2-refraction).

ZEISS는 내부 반사 고스트·베일·조리개 회절을 구별하고, Nikon은 밝은 점광원의 회절별을 설명한다. 렌즈 플레어를 단일 이미지 효과로 합치지 않는다. 필름 halation·디지털 bloom·포화에 대한 신규 전문 정의는 보류하고 기존 편집 효과와 별도 출처를 검토한다. [ZEISS 광학 자료](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-about-the-reduction-of-reflections-for-camera-lenses.pdf), [Nikon 회절별](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-idea-adding-star-power).

## 7. 연기·재·그을음·열손상은 매질과 재료로 구별

F045–F055는 공중 플룸, 상부 연기층, 원경 연무, 비산 입자, 바닥 재, 표면 검댕, 탄화 고체를 분리한다. 연기 색만으로 성분·독성·입경을 결정하지 않는다. 흑연/graphite, 필라멘트, 코로나 등의 동음어도 문맥으로 구분한다.

연기 문헌은 smoke에 기체까지 포함하는지 에어로졸만 다루는지 범위가 다를 수 있다. 이 차이를 연구 provenance에 보존하며 런타임에서는 요청된 가시 플룸·차폐·침착 형태를 표현한다. [NIST 연기 자료의 저자 초록](https://firedoc.nist.gov/article/k3cyXYQBWEcjUZEYH0wr).

F056–F066의 핵심은 **같은 재료의 변화 범위**다. 갈변, 탄화 균열, 종이 가장자리 손실, 털 끝 그슬림, 용융 모서리, 판재 휨, 코팅 부풀음, 박리, 콘크리트 박락을 한 “burned” 후보로 통합하지 않는다.

화재 패턴은 조사 단서이며 그 효과를 만든 물리적 원인 검토가 필요하다. 균열의 크기·그을음 자국 한 장으로 촉진제·방화·발화점을 확정하는 metadata를 만들지 않는다. 콘크리트의 외형 손상도 구조 안전·정확한 온도의 증거가 아니다. [NIST OSAC 조사 지침](https://www.nist.gov/system/files/documents/2021/07/28/Technical%20Guidance%20Document_Strengthening%20Fire%20and%20Explosion%20Investigation%20in%20the%20U.S._A%20Strategic%20Vision%20for%20Moving%20Forward_April%202021.pdf), [NIST 화재 콘크리트](https://www.nist.gov/programs-projects/investigation-fire-affected-concretes-residual-properties-and-link-petrographic).

## 8. 화재 사건·산불·방호의 시각 의미

플래시오버·백드래프트·역화·폭연·폭굉·재발화에는 시간·유동·산소·전파 속도 등이 관련된다. F072/F073은 사건 문맥으로 저장한다. 큰 화구나 문 밖 불꽃만으로 메커니즘을 진단하지 않는다. [NIST 백드래프트](https://www.nist.gov/glossary-term/18991), [NIST 플래시오버 초록](https://www.nist.gov/publications/defining-flashover-fire-hazard-calculations).

배터리 열폭주에서는 셀·배출구·플룸의 연결을 후보로 만들되 화염을 자동 요구하지 않는다. FAA의 시험에서도 가스 배출과 가스 점화 시험을 구별한다. [FAA 배터리 연구](https://www.fire.tc.faa.gov/pdf/TC-16-17.pdf).

산불은 낮은 연료층 F079, 수관 F080, 지중 유기물 F081, 세로 연결 연료 F082, 떨어진 비화점 F083, 회전 기둥 F084, 플룸 위 응결 구름 F085로 나눈다. 비화물·두 개의 불은 실제 비화 인과와 구별하고, 화재적란운에는 번개·성층권 도달을 보편 필수 요소로 만들지 않는다. [NWCG 비화물](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/firebrand-82), [NWCG 화염 회오리](https://www.nwcg.gov/publications/pms205/nwcg-glossary-of-wildland-fire-pms-205/fire-whirl-86), [호주 기상청 화재 구름](https://www.bom.gov.au/resources/learn-and-explore/fire-weather-knowledge-centre/how-fires-make-thunderstorms).

소화 도구는 같은 출구–분사–대상을 연결한다. 장비가 보이는 것과 실제 작동·소화 완료·재료 성능은 구별한다. 주거용 sprinkler는 열에 반응하고 헤드가 독립적으로 작동한다는 경계를 반영한다. 온도 수치는 PDF OCR 오독 때문에 이번 데이터에 옮기지 않았다. [NFPA sprinkler 자료](https://content.nfpa.org/-/media/project/storefront/catalog/files/fire-sprinkler-initiative/sprinkler-myths-and-facts.pdf?rev=9ffa003adce542e0965df177266424ce).

## 9. 생활·공예·산업·요리를 도구–재료 관계로 확장

생활 영역에는 심지–등잔, 횃불 머리–불길, 화로–숯, 벽난로–연료, 풀무 출구–화덕, 부지깽이 끝–같은 장작을 작성했다. 한국 전통 부엌 F096은 아궁이–부뚜막–같은 가열 공간 위 솥의 구조로 둔다. 역사·지역·재료 판본은 확인된 출처 범위에서 따로 묶는다. [국립민속박물관 부엌 맥락](https://webzine.nfm.go.kr/2016/02/29/한국인은-밥심으로-산다/).

산업 영역은 도가니–쇳물–주형, 망치–금속–모루, 블로파이프–끝의 유리, 토치–같은 유리 막대, 스택 끝–화염 등이다. molten metal·molten glass는 연소 화염과 다르다. 유리 서냉 정의를 금속의 담금질·뜨임·풀림에 그대로 확장하지 않는다. 금속 열처리·소결·유리화·낙화·화염 연마는 일부 전문 자료를 추가 확인할 필요가 있다. [V&A 금속 가공](https://www.vam.ac.uk/articles/metalworking-techniques), [Corning 유리 불기](https://allaboutglass.cmog.org/glass-dictionary/b), [Corning 서냉](https://allaboutglass.cmog.org/definition/annealing), [TWI 아크 용접](https://www.twi-global.com/technical-knowledge/faqs/what-is-arc-welding), [EPA 산업 플레어](https://www.epa.gov/sites/default/files/2020-10/documents/13.5_industrial_flares.pdf).

요리는 열원과 음식의 배치, 갈변 표면, 탄화 부위, 훈연 경로, 팬 위 플람베 화염, 토치 마감 부위를 분리한다. 마이야르와 캐러멜화는 서로 다른 반응이며 갈색 표면만으로 반응·향미·익힘 상태를 판정하지 않는다. 플람베는 팬 위 알코올 증기의 화염이라는 경계를 유지한다. [ACS 요리 화학](https://www.acs.org/acs-webinars/library/tasty-culinary-chemistry.html), [RSC 플람베](https://edu.rsc.org/download?ac=509309).

## 10. 태양·비연소 현상·광학을 불과 분리

태양은 핵융합 별이며 광구·채층·코로나는 같은 불꽃의 안팎 이름이 아니다. 흑점·백반·쌀알무늬에는 관측 대역·해상도가 필요하고, 내부 핵·자기장·태양풍은 일반 사진의 직접 픽셀 형태로 강제하지 않는다. [NASA 태양](https://science.nasa.gov/sun/facts/).

홍염/필라멘트는 태양 가장자리와 원반이라는 관측 배경 차이를 유지한다. 플레어의 복사 방출, CME의 물질 방출, 자기 루프 구조도 서로 다른 단위다. [NASA 홍염](https://www.nasa.gov/image-article/what-solar-prominence/), [NASA 현상 용어](https://science.nasa.gov/heliophysics/resources/vocabulary/).

NASA 용어 페이지에는 오래된 태양 주기 예측도 남아 있다. 이번에는 안정된 정의만 사용했다. SDO 배색은 EUV 파장에 배정된 색이라는 별도 observation metadata로 둔다. 이 배정은 사진 한 장만으로 복원할 수 없으므로 F130의 channel·color table을 native-visible component로 잘못 처리하지 않는다. [NASA SDO 배색](https://science.nasa.gov/resource/slices-of-the-sun/).

용암 F136은 용융 암석, 세인트엘모 F138은 대기 전기 방전, 유성 화구 F137은 대기 중 천체 사건이다. “불처럼 보인다”는 관계를 유지하되 연소 화염의 alias로 합치지 않는다. [USGS 용암](https://www.usgs.gov/news/volcano-watch-lavas-not-fire), [NOAA 세인트엘모](https://oceanservice.noaa.gov/ocean/weird-ocean-weather.html), [NASA 유성 화구](https://science.nasa.gov/earth/earth-observatory/looking-for-lightning-finding-fireballs-149381/).

## 11. 문화·판타지·폭력·관능·비유의 처리

문화 영역에서는 특정 Nataraja 조각의 금속 후광·손에 든 불 도상을 실제 화염과 구별한다. 성화 전달은 서로 다른 bearer–torch–head의 연결로 표현한다. 봉헌초·향은 시각적 배열·연기 후보와 종교·의례 판본을 분리한다. 이 연구는 특정 도상 하나를 모든 문화의 공통 불 의미로 주장하지 않는다. [Met Nataraja](https://www.metmuseum.org/art/collection/search/39328), [IOC 성화 맥락](https://library.olympics.com/default/digitalCollection/DigitalCollectionInlineDownloadHandler.ashx?_cb=20201210144919&documentId=171885&parentDocumentId=171884).

정령·불사조·용의 브레스·도깨비불은 별도 창작 제안이다. 원작·지역 민속·발생 화학의 정식 정의로 보고하지 않는다. 형상에서는 하나의 몸과 붙은 날개, 같은 입에서 나오는 불, 공간 앞뒤 연결을 우선한다.

화상·의복 손상·불타는 대상·화형·화염 무기·촛농 접촉·불에 대한 성적 관심도 조사 범위에 남겼다. **물리적 접촉, 의복 상태, 감각, 성적 의미, 동의, 동기, 임상 판단은 각각 다른 소유**다. 촛농 하나가 sexual tone을 만들거나 불 근처 인물이 방화 동기의 증거가 되지 않는다. 폭력 장면은 명시된 대상·표면·화염을 연결하며 피해 결과·사망·고의를 자동 작성하지 않는다.

F149의 wax–skin은 피부 material/relationship 제안이다. 일반 생일 양초나 손을 데우는 장면으로 해당 후보가 들어오면 문맥 불일치다. 기존 controls와 requester age·tone을 유지하며 연구 데이터에서 모든 인물에 literal adult 문구를 강제하지 않는다.

불타는 사랑·불꽃 튀는 관계·열화 같은 반응은 맥락 카드다. 요청이 실제 불을 요구하지 않았다면 감정의 actor–target–action–visible consequence를 독립적으로 저술할 수 있지만, 물리적 불이나 진단·성적 의도를 자동 활성화하지 않는다.

## 12. 실제 강화되는 데이터와 검증 경계

- [SEMANTIC-UNITS.json](SEMANTIC-UNITS.json): 카드 155개, 출처·구성요소·소유·관계·혼동 경계·효과 제안.
- [SEMANTIC-CARDS.md](SEMANTIC-CARDS.md): 모든 카드를 읽기 쉽게 풀어 쓴 문서.
- [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json): 슬롯·원자 문구·concept units·relations·affected properties 후보 131개.
- [PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json): 관계 중심 V2 프로토타입 18개.
- [BUNDLE-DRAFTS.json](BUNDLE-DRAFTS.json): 같은 소유자 아래 공동 채택을 검토할 묶음 7개.
- [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json): 재사용·신설·맥락 전용의 개별 반영 ledger.
- [REGRESSION-PLAN.json](REGRESSION-PLAN.json): 구분·반례·잠금 변이 사례 44쌍.
- [PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json): 통제 비교와 원본 픽셀 사례 10개.
- [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md): 실제 파일·단계·완료 조건을 명시한 반영 계획.

데이터 정합성과 현행 compiler의 제한된 형태 검증은 통과했다. 후보 131개의 슬롯·dimension/property 문법, 프로토타입 18개의 source shape·컴파일, gate 72개의 현재 프로필과 ID 비충돌을 확인했다. [VALIDATION.json](VALIDATION.json)에 미검증 항목을 함께 적었다.

runtime source/manifest/index 변경, 검색·activation 동작, 실제 owner resolution, 후보팩 노출, 프롬프트 audit, 이미지 생성, 사용자 수용은 이번 조사에서 실행하지 않았다. 리서치 자료는 이 폴더에만 있으며 배포되는 스킬의 source title·URL·bulk keyword·pre-core 지침에 복사하지 않는다.

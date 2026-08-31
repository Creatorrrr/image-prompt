# 펑크 계열 시각 의미·후보팩 강화 리서치

- 조사일: 2026-08-31
- 대상: `photo-prompt-image-generator`
- 계약: `photo-punk-visual-semantics/v1`
- 출발점: 선행 대화에서 추린 20개 `~punk` 키워드
- 목적: 장르명을 얇은 분위기 태그로 추가하지 않고, 사진 한 장에서 판별 가능한 작동 원리·물질·사회 관계·혼동 경계로 바꾼다.

## 결론

20개 이름을 같은 강도의 장르로 취급할 근거는 없다. 이번 확장은 다음 네 층으로 나눈다.

| 성립도 | 수 | 런타임 원칙 |
|---|---:|---|
| established genre | 5 | 정확 명칭 또는 명확한 장르 맥락에서 라우팅 가능 |
| established derivative | 4 | 모장르와 구분되는 시대·기술 기제가 있을 때 라우팅 가능 |
| emerging community genre | 1 | 커뮤니티 정의가 아직 유동적이므로 정확 명칭 요청에서만 활성화 |
| design shorthand | 10 | 독립 장르의 보편적 정전으로 주장하지 않고 정확 명칭 요청의 설계 계약으로만 사용 |

구현 단위는 이름 하나당 `world` 후보와 3개의 `prop` 후보 결합이다. `world`는 사회·환경·인프라의 작동 관계를, `prop`은 핵심 장치·고장 진단·정비 인계라는 서로 다른 장면에서 그 관계를 증명하는 물질적 운반체를 맡는다. 솔라펑크는 이미 더 강한 시민 제도 중심 프리셋이 있어 재사용했고, 나머지 19개는 신규 프리셋으로 만들었다.

## 20개 의미 계약

| 키워드 | 성립도 | 화면에서 성립시키는 핵심 | 대표 혼동 경계 |
|---|---|---|---|
| Cyberpunk | established genre | 접근 통제된 네트워크 권력 + 거리의 우회·수리 + 실제로 쓰이는 신체 인터페이스 | 네온·비·홀로그램만 있는 미래 도시, 사이버고스 클럽 패션 |
| Steampunk | established genre | 보일러·압력계·밸브 + 벨트·링키지의 동력 전달 + 사람이 쓰고 정비하는 19세기 대체 산업 | 빅토리아 의상에 장식용 톱니만 붙인 장면 |
| Dieselpunk | established genre | 연료 공급·내연기관 + 항공·대량 물류 + 배기열·진동·정비 노동 | 갈색 색보정, 군복, 리벳 표면만 있는 장면 |
| Decopunk | established derivative | 아르데코 기하와 스트림라인 외피 + 기능하는 시민·교통 기계 + 크롬·래커·검은 유리의 일관된 설계 체계 | 화려한 호텔 로비나 패션만 있는 장면 |
| Atompunk | established derivative | 1945–1965 원자력·초기 우주시대 인프라 + Googie 형태 + 낙관과 방사선·민방위 위험의 긴장 | 원자 아이콘·파스텔 복고만 있는 장면 |
| Raypunk | design shorthand | 펄프 우주 모험의 핀 로켓·돔·리브 하우징 + 과장된 아날로그 제어기의 실제 작동 | 일반 우주 오페라나 레이저총 소품 |
| Clockpunk | established derivative | 태엽·추·탈진기·캠·기어열 + 계산·자동인형의 인과적 운동 + 장인 제작 흔적 | 임의의 톱니 장식, 스팀 장치로 대체 |
| Teslapunk | design shorthand | AC 발전·변압·코일·도체·절연체 + 제어된 코로나 방전 + 하나의 전력망 | 원인 없는 번개 쇼, 스팀펑크의 청색 전기 효과 |
| Biopunk | established genre | 배양·조직 스캐폴드·유전 접근 통제 + 살아 있는 제작 공정 + 신체·제도적 결과 | 고어, 슬라임, 사이버 임플란트만 있는 장면 |
| Nanopunk | established derivative | 나노 스케일을 읽게 하는 계측 + 공급물·봉쇄 + 추적 가능한 거시적 전후 물성 변화 | 공중에 떠 있는 작은 로봇, 일반 홀로그램 UI |
| Solarpunk | established genre | 분산 재생에너지 + 공동체 소유·자원 배분 + 수리 가능한 기후 적응 인프라 | 식물벽·태양광 패널만 있는 고급 건축 |
| Lunarpunk | emerging community genre | 야간 생태 + 저에너지 길찾기·생물발광 재배 + 숨은 수리망·상호부조 | 보라색 달빛과 발광 식물만 있는 판타지 |
| Oceanpunk | design shorthand | 압력·어둠·부식·산소 순환 + 조류·파력 기계 + 해양 정착의 일상 정비 | 일반 잠수부나 수족관 장면 |
| Skypunk | design shorthand | 부력체·계류·도크·밸러스트 + 바람·기상 한계 + 화물·이동 교환 | 원인 없이 떠 있는 섬, 단순 비행선 배경 |
| Desertpunk | design shorthand | 깊은 그늘·열 방출 + 물 포집·배분 + 방진 기계·수리 문화 | 모래색 의상, 폐허, 오아시스 장식만 있는 장면 |
| Stonepunk | design shorthand | 석기·뼈·나무·생가죽·식물 섬유 + 레버·축·롤러·추·장력의 읽히는 하중 경로 | 동굴인 코스튬, 돌처럼 보이는 현대 기계 |
| Rococopunk | design shorthand | 18세기 볼륨·파스텔 실크·레이스·금박 비대칭 + 착용자가 해체·재봉한 DIY 펑크 변형 | 로코코 드레스에 기계를 붙인 장면, 일반 코스튬 |
| Magipunk | design shorthand | 마법 저장소·도관·계량기·접속부 + 공공 인프라·유지보수 + 불평등한 접근 | 주문 이펙트, 마법사 전투, 장식용 룬만 있는 장면 |
| Aetherpunk | design shorthand | 봉쇄된 에테르 매질 + 압력 용기·밸브·전도선·부력계 + 누출·수리·배급 | 설명 없는 빛나는 안개, 일반 마기테크 |
| Crystalpunk | design shorthand | 소켓형 광물 공진기 + 조율·냉각·파손·교체 주기 + 에너지 전달 경로 | 보석 장식, 수정 동굴, 특정 게임 세계의 외형 복제 |

## 출처에서 추출한 판별 원리

### 기술·권력 계열

[The Encyclopedia of Science Fiction의 Cyberpunk](https://sf-encyclopedia.com/entry/cyberpunk)는 사이버네틱스·정보망·신체 경계와 거리 수준의 소외를 함께 다룬다. 따라서 사이버펑크 후보는 `네온 도시`가 아니라 접근 통제, 재사용 인터페이스, 신체-기계 사용 행위를 한 프레임에 묶는다.

[Oxford Academic의 Biopunk 장](https://academic.oup.com/edited-volume/45763/chapter-abstract/398728780)은 유전공학·생명공학과 그 사회정치적 결과를 핵으로 둔다. 후보는 고어를 의무화하지 않고, 젖은 실험 공정에서 제도적 접근과 신체 결과로 이어지는 연결을 요구한다.

[SFE의 Nanotechnology](https://sf-encyclopedia.com/entry/nanotechnology)는 분자 규모 조립과 물성 변환을 다룬다. 분자 규모는 일반 사진에 직접 보이지 않으므로, 나노펑크는 계측 장비, 봉쇄, 공급물, 시편의 전후 상태로 간접 증명한다. 작은 로봇 떼는 기본 표현이 아니다.

### 레트로 기계·전기 계열

[SFE의 Steampunk](https://sf-encyclopedia.com/entry/steampunk)와 [Science Museum의 제작 문화 기록](https://blog.sciencemuseum.org.uk/steampunk-in-the-science-museum/)을 결합해 19세기 대체 기술과 실제 동력 전달을 분리하지 않았다. 황동·목재·다이얼은 운반체이며, 보일러에서 작업 결과까지 연결되지 않으면 실패다.

[SFE의 Dieselpunk](https://sf-encyclopedia.com/entry/dieselpunk)는 20세기 전반의 레트로퓨처와 수송·산업 계보를 지지한다. 디젤펑크 후보는 색보정이나 군복이 아니라 연료, 엔진, 물류, 열, 진동, 정비로 구별한다.

[Anglo Saxonica의 펑크 파생 장르 연구](https://revista-anglo-saxonica.org/articles/10.5334/as.23)는 clockpunk·atompunk·nanopunk 같은 파생 명칭이 더 큰 레트로퓨처 계보 안에서 분화된다는 근거로 사용했다. 다만 이 목록 자체를 모든 용어가 동등하게 확립됐다는 증거로 쓰지는 않았다.

[Cooper Hewitt의 Art Deco–Streamline 전환사](https://www.cooperhewitt.org/2013/10/02/design-revolutions-art-deco-to-streamline/)는 데코펑크의 역사적 형태·재료 기반을 제공한다. 아르데코 실내 장식만으로 끝내지 않고, 스트림라인 교통·시민 기계에 연결했다.

[Getty AAT의 Googie 정의](https://www.getty.edu/vow/AATFullDisplay?english=N&find=googie&logic=AND&note=&prev_page=1&subjectid=300265600)는 1950년대 우주시대·자동차 문화·강철·유리·네온·대담한 각형을 묶는다. 이는 아톰펑크와 레이펑크의 시대 운반체로만 사용했으며, 두 이름의 완전한 장르 정의로 확대하지 않았다.

[Met의 Making Marvels 전시 가이드](https://www.metmuseum.org/exhibitions/listings/2019/making-marvels-science-splendor/exhibition-guide)는 시계·자동인형·과학기구의 실제 기계 계보를 제공한다. 클락펑크 후보는 태엽·추·탈진기·캠을 선택 가능한 장식이 아니라 작동 사슬로 묶는다.

[Tesla Science Center의 Wardenclyffe 기록](https://teslasciencecenter.org/history/tower/)은 고주파·무선 전송·코일 시스템의 역사적 기반을 제공한다. 테슬라펑크는 독립 정전으로 과장하지 않고 정확 요청에만 코일·변압·절연·방전을 묶은 설계 축으로 활성화한다.

### 생태·환경 적응 계열

솔라펑크는 [Cambridge의 커뮤니티·분산 에너지 논의](https://doi.org/10.1017/9781009057868.013), [ISLE의 생태·정의 분석](https://academic.oup.com/isle/article/32/2/336/7289089?guestAccessKey=f95c4f4e-6c35-4328-9b10-3502d9df4284), [Philosophies의 목적지향적 희망 분석](https://www.mdpi.com/2409-9287/8/4/73)을 바탕으로 기존 시민 제도 중심 프리셋을 재사용한다. 녹색 표면보다 공동 소유, 자원 배분, 수리와 적응이 우선이다.

[Solarpunk Magazine의 Lunarpunk 정의](https://solarpunkmagazine.com/what-is-lunarpunk/)는 이 용어를 새롭고 덜 발달한 하위 장르로 직접 설명한다. 따라서 야간 색채만 복제하지 않고 저에너지 생태, 숨은 지식·수리망, 상호부조를 후보에 포함하되 정확 명칭 요청에만 연다.

Oceanpunk·Skypunk·Desertpunk는 독립 장르 근거 대신 각각 [NOAA의 해양 기술 제약](https://oceanexplorer.noaa.gov/explainers/technology/), [NASA의 비행선 기술 검토](https://ntrs.nasa.gov/api/citations/19760020076/downloads/19760020076.pdf), [미국 DOE의 고온건조 건물 사례](https://www7.eere.energy.gov/buildings/residential/exploredenh/explore-the-tour/casa-aguila)를 물리적 기제로 사용한다. 출처는 장르를 증명하지 않으며, 요청된 조어를 시각적으로 일관되게 구성하는 데만 쓰인다.

### 재료·패션·마기테크 계열

[Smithsonian Human Origins의 석기 자료](https://humanorigins.si.edu/evidence/behavior/stone-tools)는 박리·연마·자루 결합·복합 재료를 보여 준다. Stonepunk는 실제 역사 사회에 가상의 기계를 귀속하지 않고, 전금속 재료로 읽히는 하중 경로를 만드는 정확 요청용 구성이다.

[V&A의 Vivienne Westwood 연구](https://www.vam.ac.uk/articles/vivienne-westwood-punk-new-romantic-and-beyond)는 펑크의 DIY 해체와 역사 복식 재작업을 연결하는 근거다. 선행 목록의 `로코코 + 기계` 도식을 버리고, 로코코 실루엣을 착용자가 자르고 덧대고 다시 봉제한 구성으로 교정했다.

Magipunk와 Aetherpunk는 독립 장르를 확립할 강한 출처를 찾지 못했다. 그래서 넓은 동의어 검색이나 자동 추론을 허용하지 않는다. 사용자가 이름을 직접 말했을 때만 각각 `마법의 공공 인프라`, `봉쇄·수송 가능한 에테르 매질`이라는 원본 설계 계약으로 작동한다.

Crystalpunk는 [특정 RPG 샘플](https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/428660-sample.pdf)에서 실제 사용례를 확인했지만, 단일 제품은 보편 장르의 증거가 아니다. 제품의 설정명·진영·캐릭터·외형은 재사용하지 않고, 소켓·공진·냉각·파손·교체라는 일반 기제만 추상화했다.

## 후보팩 설계

신규 데이터는 다음처럼 구성한다.

- 시각 의미 계약 20개: 성립도, 활성화 방식, 핵심 명제, 3개 이상의 구성요소군, 3개 이상의 혼동 경계
- 프리셋 패밀리 4개: techno-social, retro-mechanical, ecological-speculative, constructed-shorthand
- 신규 프리셋 19개: 각 장르의 `world + prop`을 동시에 강제
- 신규 슬롯 후보 79개: 공통 `subject/action/location` 3개 + 장르별 `world` 19개 + `prop` 57개
- 장르별 소품 변형 3개: 핵심 장치, 작동 진단, 마모 부품의 교체·인계로 단일 고정 템플릿을 피함
- 기존 솔라펑크 후보 2개 재사용: 중복된 약한 프리셋을 만들지 않음
- EN/KO 정확 명칭 라우팅 20개: 사이버고스·DIY 펑크 음악·일반 친환경 건축 같은 이웃 개념과 분리

공통 인물 후보는 얼굴형, 체형, 민족성, 고정 의상을 지정하지 않는다. 세계의 핵심 시스템을 실제로 작동·정비·인계하는 성인 주민 또는 작업자로만 제한한다. 장르의 시각 의미는 인물의 외모가 아니라 시스템과 행위에서 나온다.

## 판정 경계

이 작업이 보장하는 것은 데이터 계약과 프롬프트 행동이다.

- 패키지 증거: JSON 구조, ID 유일성, 후보 참조 무결성
- 프롬프트 증거: 정확 EN/KO 라우팅, 세계 기제와 물질 운반체의 동시 선택, 이웃 개념 비활성화
- 렌더 증거: 이번 요청에서는 이미지를 생성하지 않았으므로 미평가
- 사용자 판단: 실제 취향·장르 설득력은 미평가

따라서 `후보팩에 들어갔다`는 사실을 `픽셀에서 장르가 성공했다`로 해석하면 안 된다. 향후 렌더 검증을 할 경우에도 장르명 인상 점수보다 각 계약의 보이는 기제와 혼동 경계를 항목별로 검사해야 한다.

## 검증 결과

- 펑크 전용 계약·라우팅·대체물·프롬프트 테스트: 7/7 통과
- 기존 월드빌딩 72개 홀드아웃과 렌더 수리 대표 회귀를 포함한 집중 묶음: 9/9 통과
- BM25F, 시각 의무, 시각 프로필 검색 회귀: 40/40 통과
- 후보팩 공용 커버리지 게이트: 6/6 통과
- 의미 인덱스: 6,910개 항목, 확장 프리셋·슬롯 누락 0
- 시각 프로필 인덱스: 82개 프로필, 정확 용어 483개
- 실제 `cyberpunk` semantic 후보팩: `punk_cyberpunk_world`로 단일 범위화되고 핵심 장치·진단·정비 인계 소품 3개가 모두 노출됨
- 전체 발견 테스트 첫 실행: 756개 중 31 실패·4 오류. 실행 도중 다른 작업의 시각 레지스트리와 인덱스가 어긋난 오류, 기존 골든·일러스트 고정 바이트 드리프트, 기존 근거 원장의 레거시 문구가 주원인이었다. 이번 확장과 직접 연결된 의미 항목 수 및 `facet orientation` 메타데이터 충돌은 수정하고 집중 재검증했다. 고정 골든·타 작업 근거 문구는 이 작업에서 갱신하지 않았다.

렌더 이미지는 생성하지 않았다. 따라서 위 통과는 패키지와 프롬프트 행동에 한정되며, 픽셀 충실도와 사용자 취향 판단은 미평가다.

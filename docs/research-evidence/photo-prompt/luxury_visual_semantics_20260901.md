# 럭셔리 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-01
- 입력 범위: 참조 대화 `럭셔리 용어 조사`의 17개 용어군과 25개 브랜드별 특징
- 적용 범위: `photo-prompt-image-generator`의 후보 사전, 개념 믹스인, 시각 의무, 근거 원장, 집중 회귀 테스트
- 비적용 범위: 실제 브랜드 로고·모노그램·제품 디자인 복제, 가격·희소성·진품·소유자 부·법적 지위의 픽셀 추론

## 결론

참조 대화의 브랜드별 특징을 런타임 브랜드 모사 지시로 넣지 않고, 서로 구분 가능한 12개 브랜드 중립 시각 문법으로 재구성했다.

1. 콰이어트 럭셔리
2. 컨스피큐어스 럭셔리
3. 장인 공정
4. 헤리티지 재해석
5. 헤리티지 트래블 오브제
6. 쿠튀르 아틀리에
7. 비스포크 테일러링
8. 건축적 소재 럭셔리
9. 바로크 오퓰런스
10. 하이 주얼리 크래프트
11. 파인 워치메이킹
12. 프라이빗 클라이언트 서비스

이 중 용어 의미가 최소 구성요소와 명확한 대체 불가 조건으로 고정되는 8개는 하드 시각 계약으로 등록했다. 장인 공정, 헤리티지 재해석, 건축적 소재, 바로크 오퓰런스는 현재 후보 문법과 믹스인으로만 강화했다. 이 네 축은 매체·시대·장소에 따른 변이가 커서 단일 픽셀 계약으로 고정하면 과잉 일반화될 가능성이 더 높다.

후보 사전에는 10개 슬롯에 걸쳐 75개 관련 후보 ID를 연결했다. 이 가운데 74개는 신규이고, 기존 `quiet_luxury_aesthetic` 1개는 넓고 모호한 단어 별칭을 제거하고 구성요소 중심으로 강화했다.

## 브랜드 조사에서 추출한 중립 문법

아래 브랜드명은 조사 입력의 특징을 군집화하기 위한 분석 라벨일 뿐이다. 생성 후보와 시각 계약에는 실제 브랜드명을 넣지 않았다.

| 조사 입력의 특징 군집 | 추출한 중립 시각 문법 | 런타임에서 보존할 관계 | 복제하지 않는 것 |
|---|---|---|---|
| Loro Piana, Bottega Veneta, Brunello Cucinelli의 절제·소재 중심 특징 | 콰이어트 럭셔리 | 낮은 표식 + 재료 표면 + 재단/형태 + 정밀 접합 | 인물의 부, 가격, 진품성, 특정 제품 |
| Louis Vuitton, Gucci, Fendi, Goyard의 표식·반복 코드 특징 | 컨스피큐어스 럭셔리 | 큰 오리지널 비문자 엠블럼 + 반복 기하 코드 + 하드웨어 + 물성 | 실제 로고, 브랜드명, 모노그램, 제품 실루엣 |
| Hermès, Loewe, Bottega Veneta, Moynat의 수작업 특징 | 장인 공정 | 재료 선택 → 특정 도구 접촉 → 구조 변화 → 검사 | 장인이 도구 옆에 서 있는 포즈, 완제품만 있는 장면 |
| Chanel, Dior, Burberry, Cartier 등의 아이콘·아카이브 갱신 특징 | 헤리티지 재해석 | 구형-신형 쌍에서 유지 요소 하나 + 변경 요소 하나 | 낡은 색감, 파티나, 연도 표기만으로 계보 주장 |
| Louis Vuitton, Goyard, Moynat, Rimowa의 여행 오브제 특징 | 헤리티지 트래블 오브제 | 보호 프레임 + 맞춤 피복 + 보강 코너 + 작동 하드웨어 + 수납 기능 | 모노그램 표면, 장식용 낡은 여행가방 |
| Chanel, Dior, Fendi의 아틀리에·쿠튀르 특징 | 쿠튀르 아틀리에 | 개별 토일 + 피팅/드레이핑 수정 + 내부 지지층 + 손부착 | 런웨이 드레스, 레드카펫 글래머, 법적 인증 추론 |
| bespoke, master cutter, fitting, aftercare 용어군 | 비스포크 테일러링 | 개인별 종이 패턴 + 베이스팅 피팅 + 손캔버스 + 기록/애프터케어 | MTM 재고 패턴, 단순 수선, 완성 수트 초상 |
| Prada, Delvaux, Rimowa, Audemars Piguet의 구조·정밀 소재 특징 | 건축적 소재 럭셔리 | 큰 재료 면 + 정밀 접합 + 섀도 갭 + 조각적 볼륨 + 반사 제어 | 빈 화이트 큐브, 고가 가구 라벨 |
| Bulgari, Fendi, Gucci의 로마·극적 장식 특징 | 바로크 오퓰런스 | 대리석·금박·거울·벨벳·곡선 장식의 다중 스케일 위계 | 무작위 금색 소품, 일반 호텔 로비, 왕관 하나 |
| Cartier, Van Cleef & Arpels, Bulgari, Tiffany의 보석 특징 | 하이 주얼리 크래프트 | 보석 매칭 + 세팅 접점 + 금속 지지구조 + 오리지널 통합 설계 | 느슨한 보석, 글리터, 캐럿·가격 주장 |
| Rolex, Patek Philippe, Audemars Piguet의 기계·마감 특징 | 파인 워치메이킹 | 연결된 무브먼트 + 시간 기능 + 차등 마감 + 조립/조정 | 흩어진 기어, 프린트 스켈레톤, 스마트워치, 지위 초상 |
| private appointment, clienteling, white-glove 용어군 | 프라이빗 클라이언트 서비스 | 상담 반응 + 소수 큐레이션 + 취급/피팅 + 애프터케어 | 대리석, 샴페인, 벨벳 로프, 빈 프라이빗 룸 |

## 픽셀로 다룰 수 있는 것과 없는 것

| 주장 | 픽셀 또는 프롬프트에서 다룰 수 있는 범위 | 추가 증거가 필요한 범위 |
|---|---|---|
| 브랜드 표식의 현저성 | 표식 크기, 반복 빈도, 배치, 대비 | 실제 브랜드 소유·진품·상표 권리 |
| 재료 외관 | 그레인, 파일, 직조, 광택, 주름, 접합부 | 섬유 직경, 원산지, 성분, 내구성, 가격 |
| 제작 공정 | 손과 특정 도구의 접촉, 조립 전후, 검사 동작 | 실제 작업 시간, 숙련 등급, 제작자 신원 |
| 개별 맞춤 | 개인별 패턴·토일·수정선이 같은 고객에 연결되는 장면 | 주문 기록, 서비스 계약, 실제 고객 이력 |
| 헤리티지 | 선언된 가상 아카이브-신형 쌍의 유지/변경 관계 | 실제 연도, 출처, 소유 계보, 문화 전승의 진위 |
| 쿠튀르 | 토일·드레이핑·내부 구조·손부착이 보이는 아틀리에 공정 | 법적·협회 인증, 컬렉션 일정, 하우스 자격 |
| 서비스 | 상담자-고객 반응, 소수 큐레이션, 피팅·관리 후속 | 만족도, 신뢰, 재구매, 고객 지위, 실제 사생활 보호 수준 |
| 럭셔리 가치 | 관찰 가능한 형태·재료·공정 관계 | 부, 희소성, 배타성, 사회적 지위, 객관적 품질, 사용자 선호 |

따라서 `luxury`, `럭셔리`, `명품`, `luxury brand` 같은 넓은 입력은 단일 후보팩이나 하드 시각 의무를 강제하지 않는다. 좁은 개념 용어가 들어왔을 때만 정확 라우팅한다.

## 8개 하드 시각 계약

### 1. `low_brand_prominence_material_luxury`

- 정확 활성어: `quiet luxury`, `discreet luxury`, `understated luxury`, `콰이어트 럭셔리`, `절제된 럭셔리`
- 필수 구성: 낮은 브랜드 표식, 특정 재료 표면, 재단 또는 형태 제어, 접합부 또는 하드웨어 정밀도
- 주요 대체 불가 조건: 베이지 미니멀리즘, 빈 방, 평범한 기본복, 부·가격 추론
- 후보 연결: `quiet_luxury_aesthetic`, 미세 울/캐시미어 파일, 풀그레인 가죽 변화, 석재-목재-브라스 접합, 저확산 소재 조명
- 픽셀 게이트: 표식 억제, 재료 구체성, 전체 형태의 핏, 근접 접합, 지위 추론 금지

### 2. `conspicuous_original_house_code_display`

- 정확 활성어: `conspicuous luxury`, `loud luxury`, `logomania styling`, `컨스피큐어스 럭셔리`
- 필수 구성: 오리지널 비문자 코드, 높은 현저성, 통제된 반복, 재료·오브제 구조 통합
- 주요 대체 불가 조건: 실제 로고·브랜드명·모노그램 복제, 임의 텍스트, 금색/검정 잡동사니
- 런타임 표현: 정의만 사용하며 `conspicuous luxury`, `loud luxury`, `logomania` 라벨을 최종 프롬프트에서 억제한다.
- 픽셀 게이트: 오리지널성, 첫인상 현저성, 반복 일관성, 심·하드웨어 통합, 상표/클러터 배제

### 3. `couture_atelier_individual_construction`

- 정확 활성어: `haute couture`, `couture atelier`, `metiers d'art couture`, `오트 쿠튀르`
- 필수 구성: 개별 토일/폼, 실시간 피팅·드레이핑, 내부 지지구조, 손부착·손마감
- 주요 대체 불가 조건: 완성 드레스만 있는 장면, 런웨이, 레드카펫, RTW 랙
- 경계: 렌더는 아틀리에 공정을 보일 수 있지만 Haute Couture 법적 자격을 증명하지 않는다.

### 4. `bespoke_tailoring_individual_pattern`

- 정확 활성어: `bespoke tailoring`, `bespoke suit craft`, `비스포크 테일러링`
- 필수 구성: 개인별 종이 패턴, 같은 고객의 베이스팅 피팅 수정, 손캔버스 내부, 기록/애프터케어
- 주요 대체 불가 조건: MTM 재고 패턴, 단순 수선, 기성복 핏, 완성 수트 초상
- 핵심 연결: 패턴과 피팅이 같은 고객에 대응해야 하며, 패턴 소유 관계가 장면에서 읽혀야 한다.

### 5. `heritage_travel_object_construction`

- 정확 활성어: `heritage travel luxury`, `trunk-maker aesthetic`, `heritage trunk luxury`
- 필수 구성: 단단한 보호 프레임, 장력 있게 맞춘 피복, 보강 하드웨어, 여행·보호 기능
- 주요 대체 불가 조건: 여행가방 실루엣만, 장식용 낡은 트렁크, 모노그램, 파티나
- 런타임 표현: 실제 하우스·헤리티지 라벨 대신 구조 정의만 사용한다.

### 6. `high_jewelry_setting_integration`

- 정확 활성어: `high jewelry`, `high jewellery`, `haute joaillerie`, `하이 주얼리`
- 필수 구성: 크기·색 매칭, 프롱/베젤/파베 접점, 금속 갤러리 지지, 오리지널 통합 구성
- 주요 대체 불가 조건: 느슨한 보석, 글리터, 코스튬 주얼리, 가격·캐럿 주장
- 촬영 문법: 제어된 스페큘러 하이라이트로 반짝임이 세팅 구조를 가리지 않게 한다.

### 7. `fine_watchmaking_mechanical_finishing`

- 정확 활성어: `fine watchmaking`, `haute horlogerie`, `파인 워치메이킹`
- 필수 구성: 연결된 기계식 무브먼트, 시간/조정 기능, 차등 마감, 조립·조정 작업점
- 주요 대체 불가 조건: 흩어진 장식 기어, 인쇄된 스켈레톤 무늬, 스마트워치, 지위 과시 초상
- 촬영 문법: 그레이징 라이트로 브러시 면, 폴리시 면, 앵글라주 모서리를 분리한다.

### 8. `private_client_service_interaction`

- 정확 활성어: `private client luxury`, `private appointment luxury`, `white-glove luxury service`
- 필수 구성: 상담자-고객 반응, 관련된 두세 선택지, 신중한 취급/피팅, 관리 후속
- 주요 대체 불가 조건: 빈 대리석 로비, 샴페인, 벨벳 로프, 프라이빗 룸, 판매원 포즈
- 런타임 표현: 서비스 라벨보다 관계 행동을 직접 기술하고 개인 정보 없는 애프터케어 기록만 사용한다.

## 후보 문법으로 유지한 4개 축

### 장인 공정

`craftsmanship_process_luxury_aesthetic`는 완제품 외관이 아니라 재료 선택, 특정 도구의 실제 접촉, 미완성-완성 구조 변화, 표면·기능 검사를 묶는다. 가죽 새들 스티치, 가죽 스트립 직조, 패턴 재단, 쿠튀르 드레이핑, 접합부 검사를 회전 가능한 액션 풀로 구성했다.

### 헤리티지 재해석

`heritage_reinterpretation_luxury_aesthetic`는 브랜드 없는 아카이브 샘플과 새 오리지널 버전을 쌍으로 둔다. 체결 논리·모티프·재료 관계 중 하나는 유지하고 실루엣·기능·표면 중 하나는 바꾼다. 파티나나 빈티지 컬러 그레이딩은 계보 증거가 아니다.

### 건축적 소재 럭셔리

`architectural_material_luxury_aesthetic`는 적은 수의 큰 재료 면, 정밀 접합, 섀도 갭, 조각적 볼륨, 제어된 반사를 결합한다. 공간 전체 면 위계와 접합부 근접 증거를 함께 요구하는 후보팩으로 구성했다.

### 바로크 오퓰런스

`baroque_opulent_luxury_aesthetic`는 대리석·금박 금속·거울·벨벳·곡선 장식·키아로스쿠로를 천장, 벽, 가구, 오브제의 여러 스케일에 반복한다. 금색의 양이 아니라 통합된 움직임과 위계가 핵심이다.

## 근거와 데이터 반영

| 근거 | 데이터에 반영한 추상 관계 | 반영하지 않은 주장 |
|---|---|---|
| [Journal of Marketing: Brand Prominence](https://journals.sagepub.com/doi/abs/10.1509/jmkg.74.4.015) | quiet/loud 표식 현저성 축 | 가격·부·품질 판정 |
| [FHCM: Our History](https://www.fhcm.paris/en/our-history), [FHCM Federation](https://www.fhcm.paris/en/federation-de-la-haute-couture-et-de-la-mode) | 개별 맞춤, 아틀리에 손작업, 원형 제작 | 법적 인증을 외관으로 추론 |
| [Savile Row Bespoke Association: Membership Requirements](https://www.savilerowbespoke.com/about-us/membership-requirements/) | 개인별 종이 패턴, master cutter, 손작업, 기록·애프터케어 | 작업 시간·회원 자격의 픽셀 판정 |
| [Hermès in the Making](https://www.hermes.com/us/en/content/340839-hermes-in-the-making-turkey/) | 클램프와 두 바늘 새들 스티치, 수리 연속성 | 브랜드 제품·장인 신원·진품성 |
| [Bottega Veneta: Intrecciato](https://www.bottegaveneta.com/en-us/men-collection-us/men-bags/intrecciato) | 가죽 스트립 교차, 재료·처리·직조 스케일 변이 | 고유 제품 비율·정확한 시그니처 패턴 |
| [Loro Piana: The Gift of Kings](https://mt.loropiana.com/en/our-world/the-gift-of-kings) | 무광 미세 파일, 부드러운 주름, 드레이프 | 섬유 직경·원산지·추적성·가치 |
| [Louis Vuitton: Trunks](https://us.louisvuitton.com/eng-us/stories/louis-vuitton-trunks) | 목재 패널 프레임, 피복, 금속 코너·잠금, 보호 기능 | 모노그램·잠금 디자인·브랜드 트렁크 복제 |
| [GIA: Guide to Ring Settings](https://4cs.gia.edu/en-us/blog/guide-to-ring-settings/) | 프롱·베젤·파베와 금속 지지구조 | 보석 종류·처리·가치·희소성 판정 |
| [FHH: Fine Watchmaking Manifesto](https://campaigns.hautehorlogerie.org/fhh/manifesto/manifesto-en.pdf) | 기계 기능, 손장식, 마감, 읽을 수 있는 시간 | 성능·정통성·시장 지위 판정 |
| [McKinsey: Human-centered luxury experiences](https://www.mckinsey.com/industries/retail/our-insights/when-ai-meets-desire-innovating-human-centered-luxury-experiences-in-the-agentic-age) | high-touch, discretion, pacing, clienteling, aftercare | 고객 만족·신뢰·VIP 지위의 외관 추론 |
| [V&A: The Baroque style](https://www.vam.ac.uk/articles/the-baroque-style) | 움직임·드라마·건축/장식 통합 | 특정 역사 공간·장식 프로그램 복제 |
| [MoMA: Ludwig Mies van der Rohe](https://www.moma.org/artists/7166) | 절제된 형식과 풍부한 재료·표면·텍스처 관계 | 특정 건물·가구 디자인 복제 |
| [UNESCO: Traditional craftsmanship](https://ich.unesco.org/en/traditional-craftsmanship-00057) | 완제품보다 기술·지식·전승 과정 강조 | 특정 공동체·전통 귀속을 외관으로 추론 |

각 근거는 `research_evidence.jsonl`에서 후보 ID와 시각 계약 또는 개념 믹스인에 연결했다. 하우스 공식 자료는 기술·구성 관계를 파악하는 데만 사용했고 비교 연구나 중립 표준처럼 취급하지 않았다.

## 후보팩 구조

| 슬롯 | 강화 수 | 역할 |
|---|---:|---|
| `aesthetic_trend` | 12 | 12개 문법의 의미 경계와 검색 문서 |
| `action` | 11 | 손도구 접촉, 피팅, 조립, 세팅, 검사, 상담 반응 |
| `capture_context` | 5 | 공정 다큐, 소재 매크로, 브랜드 중립 house-code, 프라이빗 서비스, 아카이브 비교 |
| `prop` | 10 | 패턴, 토일, 클램프, 코너 샘플, 세팅 트레이, 무브먼트, 애프터케어 기록 |
| `location` | 9 | 아틀리에·커팅룸·공방·세팅 벤치·워치 벤치·프라이빗 살롱 |
| `narrative_phase` | 6 | 원재료 선택부터 애프터케어까지의 공정 단계 |
| `surface_material` | 10 | 가죽·울·실크·직조·트래블 구조·금속·보석 세팅·바로크·건축 접합 |
| `garment_detail` | 4 | 토일 수정선, 손캔버스, 내부 지지층, 손자수 부착 |
| `color` | 4 | 절제·극적·주얼리·워치용 팔레트 |
| `lighting` | 4 | 소재 그레이징, 보석 스페큘러, 저확산 갤러리, 바로크 키아로스쿠로 |

후보 행에는 순위·점수 필드를 추가하지 않았다. 후보팩은 검색·회전 가능한 재료이며, 특정 브랜드나 미학을 항상 우선하도록 만들지 않는다.

## 라우팅·회귀 설계

집중 테스트는 다음을 분리해 확인한다.

1. 75개 관련 후보 ID가 기대 슬롯에 존재하고 검색 문서·별칭·키워드를 가진다.
2. 12개 좁은 용어는 정확한 믹스인 하나로 라우팅되고 최소 3개 슬롯의 소프트 앵커를 만든다.
3. `luxury`, `럭셔리`, `명품`, `luxury brand`는 어떤 믹스인이나 하드 시각 계약도 강제하지 않는다.
4. 믹스인은 얼굴·몸·출신·종족 슬롯을 소유하지 않는다.
5. 8개 시각 프로필은 각각 최소 4개 필수 구성군, 완전한 증거 필드, 고유한 픽셀 게이트 5개를 가진다.
6. 정확 용어는 기대 프로필 하나만 하드 활성화한다.
7. 베이지 미니멀리즘, 금색 호텔 로비, 완성 드레스, 재고 패턴 수트, 장식 여행가방, 느슨한 보석, 스마트워치, 빈 대리석 로비는 럭셔리 프로필을 하드 활성화하지 않는다.
8. 13개 근거 행은 승인 상태이고 실제 후보와 계약에 연결된다.

## 검증 경계

- 사전·라우팅 PASS: 후보 ID, 정확 믹스인, 정확 하드 프로필, 넓은 용어의 fail-closed 동작을 코드 수준에서 확인할 수 있다.
- 프롬프트 패키지 PASS: 생성 후보팩이 필요한 앵커와 시각 의무를 포함하는지 확인할 수 있다.
- 픽셀 PASS: 실제 생성 이미지에서 5개 게이트가 모두 보이는지 별도 렌더와 원본/썸네일 검수가 필요하다.
- 사용자 판단: “충분히 럭셔리하게 읽히는가”는 요청자 판단이며 자동 게이트와 분리한다.

이번 작업은 데이터와 프롬프트 계약 강화까지를 범위로 하며, 브랜드별 이미지 생성이나 픽셀 비교는 수행하지 않는다.

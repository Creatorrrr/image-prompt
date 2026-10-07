# vel 키워드 기반 시각 의미·후보팩 강화 리서치

작성일: 2026-10-07 (Asia/Seoul)  
참조: [프롬프트 분석 리스트 vel](https://chatgpt.com/c/6ac5bdb5-f8a4-83ee-adbd-170a43f642de)  
상태: 리서치와 반영 설계 완료. 실제 런타임 데이터 채택·인덱스 재생성·이미지 검증은 별도 단계.

**후속 보완:** 대화 뒤쪽의 217개 외형 분해와 465개 요소를 추가 대조한 [외형 요소 분해 리서치](appearance-decomposition-followup/RESEARCH.md)를 함께 적용한다. 층별 의복 가시성, 타월의 양손 지지·가림, 실제 접촉과 반사, 작은 입술 틈·치아, 붉은 발광의 소유 관계를 28개 추가 카드로 보강했다. 이 문서의 수치/검증은 초기 조사 기록으로 보존한다.

## 1. 결론과 조사 범위

이번 강화의 중심은 **노출·재료·접촉·사건 상태를 각 소유자에 연결하고, 가까운 다른 뜻이 장면을 바꾸지 않게 하는 것**이다. `wet`, `latex`, `kneeling`, `weapon`, `blood`의 목록을 늘리는 것만으로는 충분하지 않다. 예를 들어 원단이 젖었는지, 빛을 반사하는지, 밑의 형상이 비치는지, 몸에 접촉하는지는 서로 다른 시각 속성이다. 무기가 홀스터에 있는지, 손에 있는지, 대상을 향하는지, 사건 후 흔적이 보이는지도 각각 다르다.

참조 대화의 원본 분석 JSON을 브라우저의 파일 다운로드로 확보해 217행, 22분류, 19개 역사 자료 식별자를 확인했다. 원본 파일을 [SOURCE-KEYWORDS.json](SOURCE-KEYWORDS.json)에 보존했고 다운로드 경로·크기·SHA-256은 [영수증](SOURCE-DOWNLOAD-RECEIPT.json)에 기록했다.

| 원본 성격 | 행 수 | 이번 처리 |
|---|---:|---|
| 긍정 지시 | 100 | 요청 의미의 관찰 자료로 분해 |
| 이미지 연결 설명 | 97 | 실제 생성 입력이라는 주장 없이 외관·해석을 분리 |
| 부정 지시 | 20 | 배제 범위·해부학 오류 방지의 별도 검증 자료 |
| 전체 | 217 | 누락 없이 제안 카드에 연결 |

역사 자료의 원문·실제 생성 입력·SNS 게시물·원본 이미지를 다시 전수 확인하지는 않았다. 원본 사전의 연령 설명도 그대로 유지한 출처 주장이다. 이 연구는 특정 단어가 선정성·폭력성 또는 이미지 품질을 실제로 높였다는 인과 실험이 아니다.

217행을 60개 설계 카드로 연결했다. 의미가 중복되는 표현은 같은 카드로 연결하고, 서로 다른 속성은 한 표현에서 여러 카드로 분해했다.

| 제안 종류 | 수 | 반영 판단 |
|---|---:|---|
| 기존 의미 재사용·등가 표현 보완 | 22 | 새 항목보다 기존 의미·gate·접근 표현 유지 |
| 새 관계 후보 trial | 24 | 소유자·연결·단계·효과를 별도 검토 |
| 창작 지침 | 3 | 추상 의도를 고정된 얼굴·몸 형태로 만들지 않음 |
| 관측 한계 | 4 | 내부 패드·힘·시간·기능을 픽셀 사실로 인증하지 않음 |
| 문맥 구분 | 5 | 장식/구속, 천/치료, 밀폐/감금 등을 분리 |
| 부정문 검증 | 2 | 긍정 의미 역전과 수위 확대 방지 |

산출물은 [60개 상세 카드](SEMANTIC-CARDS.md), [217개 대조표](KEYWORD-CROSSWALK.md), [구조화 의미 단위](SEMANTIC-UNITS.json), [46개 후보 초안](CANDIDATE-DRAFTS.json), [12개 선택형 조합 메뉴](BUNDLE-DRAFTS.json), [반영 계획](IMPLEMENTATION-PLAN.md), [20개 외부 자료](SOURCES.md)다. 초안은 실제 런타임 스키마를 통과한 배포 데이터가 아니다.

## 2. 현재 저장소 대조 결과

검토한 작업 상태는 `main`, HEAD `4c9a0054473c4383ca5287ca3bf294b277e5c6e7`이며, 기존 변경을 포함한 **현재 authored 입력**을 실제 loader로 읽었다. Git에 미반영된 변경도 있는 스냅샷이므로 HEAD의 순수 내용과 같다고 주장하지 않는다. 이번 조사 파일은 독립 디렉터리에만 작성했다.

| 확인한 현재 데이터 | 수 |
|---|---:|
| source manifest의 authored source | 98 (candidate 58, visual_profile 40) |
| 슬롯 | 112 |
| 슬롯 후보 항목 | 10,500 |
| 전체 semantic document | 10,536 |
| 시각 프로필 | 2,290 |
| 기존 candidate bundle | 1,099 |

[현재 대조 결과](CURRENT-COVERAGE.json)는 런타임의 positive-field projection과 BM25F builder/ranker를 사용한 읽기 전용 진단이다. 원문 표현을 짧은 질의로 넣고 연구용 분류-슬롯 필터를 적용했다. query embedding, frozen-core applicability, 실제 후보팩 생성은 실행하지 않았다. 부정 지시 20개는 긍정 검색 질의에서 제외했다.

197개 긍정/설명 표현 중 정규화한 동일 구절이 candidate positive 필드에서 확인된 행은 14개, profile positive 필드는 12개, 합집합은 17개다. **나머지 180개가 의미 누락이라는 뜻은 아니다.** 기존 데이터는 다른 표현으로 같은 구조를 충분히 지원할 수 있다.

| 원본 표현 | 실제 확인한 기존 ID | 판단 |
|---|---|---|
| K007 슬릿 | `pfe_slit`, `pfe_slit_candidate` | 두 경계·같은 치마·한 다리 연속성 재사용 |
| K025 lace trim | `lace_trim_attached_edge`, `lace_trim_edge` | 부착선·빈 셀·자유 가장자리 재사용 |
| K026 satin texture | `satin_directional_luster_drape_surface`, `y2kr_satin` | 방향성 광택 구조 재사용 |
| K039 젖은 머리 | `wet_damp_clumped_hair_state`, `hr_wet_hair_skin_contact` | 젖음·뭉침·접촉 재사용 |
| K028 low neckline | `decolletage_neckline_exposure`, `pfe_cleavage` | 두 의미의 경계 유지; 동의어로 합치지 않음 |
| K087 holstered | `real_holstered_service_pistol`, `carrying_holstered_real_sidearm` | 실제 기존 소지 상태를 바탕으로 관계 보완 |
| K062 kneeling | `pv_profile_tall_kneel`, `pv_profile_heel_sit`, `pv_profile_half_kneel` | 각 지지 형태 유지; 역할 의미 자동 부여 금지 |

짧은 질의의 어휘 이웃에는 다른 뜻도 나타났다. `glossy black latex`에는 검정 아크릴 표면, `enclosed chamber`에는 리볼버 cylinder, `clinging to her body`에는 다른 문화의 접촉 도상, `struggling to rise`에는 눈썹·입꼬리의 상승이 가까이 나왔다. `blood smears`에는 신체 훼손을 함께 요구하는 기존 horror trace 후보가 나타났다.

이것은 **문맥 없는 연구 질의의 이웃**이다. 실제 frozen-core 검색 실패나 candidate-pack 오채택을 입증하지 않는다. 다만 이러한 이웃을 반례로 삼고, 원래 요청에 없는 owner·행동·피해 정도·문화 판본을 후보 선택으로 추가하지 않는 설계가 필요하다. 자세한 ID와 의미는 [현재 대조표 JSON](CURRENT-COVERAGE.json)에 남겼다.

## 3. 외부 리서치에서 얻은 설계 근거

### 3.1 형태·상황·해석·검증을 별도 층으로 둔다

Visual Genome의 scene graph는 객체 속성과 subject-predicate-object 관계를 구별한다. 이 구조를 참고해 후보를 **무엇의 어떤 부분이 무엇에 어떻게 연결되는가**로 기술한다. 장면 그래프가 실제 동의·의도·책임을 증명하는 것은 아니다. [Visual Genome API](https://visualgenome.org/api/v0/api_endpoint_reference)

GenEval은 객체의 공존·개수·위치·색 같은 구성을 별도 평가한다. 여기서 가져오는 것은 관계별 검증 설계이며, 논문에 나온 모델의 결과를 현행 모델의 성능으로 옮기지 않는다. [GenEval](https://arxiv.org/abs/2310.11513)

| 층 | 예 | 데이터에 두는 위치 |
|---|---|---|
| 관찰 형태 | 어깨끈이 같은 어깨 꼭대기 아래에 놓임 | concept unit / owned relation |
| 작성된 사건 의미 | 끈이 흘러내린 순간 | 요청 해석·행동/시간 문맥 |
| 내면·사회적 해석 | 유혹·복종·고통·명령 | 근거 있는 요청·관계 의미; 형태의 자동 동의어 아님 |
| 검증 | 연결점·소유자·노출 범위가 프레임에서 읽힘 | 선택된 증거·native gate |
| 관측 불가능한 사실 | 지속 압력·숨겨진 패드·실제 동의 | claim limit / 별도 증거 필요 |

### 3.2 관능성과 친밀감을 실제 운반체에 연결한다

직접적인 `섹시한`, `slightly sultry`는 의도·정서 방향이다. 이를 하나의 입술 모양이나 무릎 자세의 universal definition으로 만들면 비성적 뷰티 초상·기도·휴식과 충돌한다.

얼굴 운동과 감정 추론을 구별하는 연구는 맥락이 감정 해석에 영향을 줄 수 있음을 설명한다. 따라서 눈꺼풀의 이완·입술 틈은 관찰 형태로, 차분함·몽환성·애정·위협은 작성된 상황의 해석으로 둔다. 이 구분이 감정 표현을 제거한다는 뜻은 아니다. [Barrett 등의 수정본](https://affective-science.org/wp-content/uploads/2024/04/barrett-et-al-2019-emotional-expressions-reconsidered-challenges-to-inferring-emotion-from-human-facial-movements.pdf)

강화할 내용은 낮은 목선의 경계, 선택된 노출 부위, 몸에 맞는 재단, 카메라 거리, 시선의 대상, 사적인 공간에서의 구체적 행동이다. 현행 sensual/fetish의 의미·저장값은 이 연구에서 변경하지 않으며, 두 축을 서로 동의어나 상호 배타적 분류로 만들지 않는다. 노출·가림도 원 요청의 조건을 따른다.

### 3.3 핏·코르셋형 절개선·내부 구조를 분리한다

V&A는 역사적 코르셋의 지지 구조·보닝·여밈·실루엣 변화를 기록한다. 현대 패션 베스트의 코르셋형 절개선이 그 전체 구조를 포함한다는 뜻은 아니다. VEL-004는 몸통 패널을 연결하는 곡선 솔기만 다루고, 별도 lacing/boning/underwear 후보를 자동 추가하지 않는다. [V&A의 코르셋 자료](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear)

`볼륨`에는 부위·owner가 필요하다. 내부 패드가 가려져 있다면 겉 실루엣을 확인할 수 있을 뿐 내부 구조를 이미지 PASS로 인증할 수 없다. 패드를 보이게 하려고 요청에 없는 탈의·절개를 추가하지 않는다.

### 3.4 섬유·직조·마감·광학 작용을 분리한다

새틴은 직조 축이며 여러 섬유로 만들 수 있다. `satin/ silk`는 동일 분류의 동의어가 아니라 직조와 섬유를 섞은 표현이다. 기존 새틴 의미를 재사용하고 새 항목을 늘리지 않는다. [MFA CAMEO: Satin](https://cameo.mfa.org/wiki/Satin)

PBRT는 반사·투과와 미세 거칠기를 별도로 다룬다. 이를 광택·비침·무광·금속의 관찰 축을 나누는 데 사용한다. 사진의 광택으로 실제 섬유 성분이나 표면 거칠기 수치를 판정한다는 뜻은 아니다. [반사와 투과](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [거칠기](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory)

라텍스 패션 연구는 특정 디자이너·음악·하위문화와 재료의 관계를 다루는 제한된 자료다. 이를 모든 라텍스 착용자의 욕망·역할·동의로 일반화하지 않는다. [Glasgow School of Art의 학회 초록](https://radar.gsa.ac.uk/5735/)

### 3.5 젖음·밀착·투과를 독립 선택으로 만든다

젖은 원단은 moisture state, 몸에 붙는 원단은 contact/tension, 비치는 원단은 transmission, 물방울 하이라이트는 reflection이다. VEL-014/015는 같은 원단의 이 속성을 별도로 선언해 관계로 묶는 제안이다.

직물에 떨어지는 물방울의 젖음·퍼짐 연구도 직조·거칠기·젖음성 등 여러 요인을 다룬다. 이 논문은 의복의 투명화나 관능 효과를 측정하지 않는다. 따라서 `wet` 하나로 투과·노출을 자동 선택하는 근거로 쓰지 않는다. [Oxford 연구 기록](https://ora.ox.ac.uk/objects/uuid%3Abce39250-7534-457d-8342-343b77088615)

원단·피부·머리·거울·렌즈·공기의 물기는 서로 다른 owner다. 샤워 직후라는 시간 서사는 젖은 머리만으로 검증할 수 없다. 반대로 원 요청이 비침이나 특정 노출을 지정했다면 연구자의 선호로 새 안감·가림을 추가하지 않는다.

### 3.6 액세서리의 부착과 움직임 제한을 분리한다

초커는 목의 밴드, O링은 부착 장식, chain은 연결과 중력에 따른 처짐, glove는 손에서 팔로 이어지는 의복, neck armor는 별도 보호 장치다. 같은 단어가 패션·판타지·하위문화에 나타날 수 있어도 보이는 구조가 실제 기능을 인증하지는 않는다.

VEL-020/021은 링 윤곽·밴드 연결·체인의 attachment point를 강화한다. 장식 체인이 느슨한 상태라면 그 의미를 움직임 제한으로 바꾸지 않는다. 다른 owner를 가진 가방 strap·lapel chain의 기존 후보는 등가 표현인지 먼저 확인한다.

### 3.7 자세는 지지·접촉·거리로 읽는다

OpenStax는 무게중심과 지지 영역을 연결한다. 이 물리 개념은 지지 발·무릎·손·침구의 위치를 살피는 근거이며 실제 압력·체중 비율을 사진에서 측정하는 근거가 아니다. [OpenStax: Stability](https://openstax.org/books/college-physics-2e/pages/9-3-stability)

침구 눌림은 같은 몸의 접촉점과 국소 변형이 연결돼야 한다. 몸에서 떨어진 임의의 침대 주름은 대체 증거가 아니다. 무릎 꿇기는 kneel variant의 지지 구성을 확인하고, 봉헌은 선택된 손 방향·대상·상황을 별도로 둔다. 무릎 자세가 봉헌과 결합되는 소장품 사례도 있어 단일 역할로 분류할 수 없다. [The Met의 Kneeling and Offering 기록](https://www.metmuseum.org/art/collection/search/546745)

### 3.8 카메라 위치와 접촉·동의를 구별한다

1인칭 낮은 시점은 카메라의 높이와 방향이다. 상대가 관찰자보다 높은 위치에 있다는 사실은 가슴 접촉이나 제압을 포함하지 않는다. 제압이 명시된 경우에만 두 인물·접촉 부위·지지면을 따로 묶는다.

근접 초상이나 얕은 심도도 친밀감의 연출 수단이지만 실제 동의·욕망을 인증하지 않는다. 초점은 선택된 얼굴과 필수 관계가 읽히는지를 확인하는 수단이다. 숫자로 쓴 aperture만으로 검증하지 않는다. [Nikon의 초상 촬영·초점 자료](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/quick-tips-for-taking-better-portraits)

### 3.9 무장·준비·행동·결과를 분리한다

무기의 개수·형태·장착, holstered/held/partly drawn, 방향·대상, 발사/충돌의 발생, 파손/피해 결과는 별도 상태다. Met의 장비 기록도 갑옷·검·검 운반구를 서로 다른 물건으로 기록한다. [The Met 장비 기록](https://www.metmuseum.org/art/collection/search/35728)

이번 설계는 장면의 물건·접촉·상태를 모델링하며 실제 무기의 작동 순서나 전술 지침을 조사·추가하지 않는다. `drawing`, `reloading`, `preparing` 같은 시간 동사는 현재 프레임에서 어떤 상태를 보여주려는지 먼저 확정해야 한다. 보이지 않는 동작 완료나 지속 시간은 별도 증거가 필요하다.

### 3.10 마법 충돌·환경 파손·혈흔은 다른 owner를 가진다

마법 효과는 선택된 원점→경로→방어막/대상→국소 충돌 관계로 설계한다. 불꽃·광 입자·돌 파편은 각각 위치와 소재를 가진다. 이들은 몸의 훼손과 동일하지 않다.

공간의 파손은 이름 있는 가구·건물의 깨진 경계와 그 잔해가 연결돼야 한다. 폐허만으로 전투의 최근성·원인·가해자를 인증하지 않는다. 피부와 머리를 깨끗하게 유지하는 원문 조건은 환경 파손과 함께 유지할 수 있다.

혈흔은 substrate와 범위가 필요하다. 현재 forensic documentation 프로필은 측정·기록을 요구하고 일부 horror 후보는 신체 연속성의 훼손까지 포함한다. 단순 `blood smears`의 등가 후보로 채택하면 원 요청보다 강한 장면이나 다른 행위가 된다. VEL-047은 국소 흔적의 범위·신체 연속성을 따로 다루는 trial이다. 흔적의 생물학적 진위·의학적 상태·책임자는 이미지에서 단정하지 않는다.

### 3.11 갈등·소진·고통의 의미를 다른 장면으로 옮기지 않는다

`wounded disbelief`의 wounded는 해당 언쟁에서 정서적 표현이다. 부상 동의어로 넣지 않는다. 손을 들고 질책하지만 손과 얼굴 사이에 간격이 있는 장면에서는 그 간격 자체를 관계로 기록한다.

기어감·일어나려 함·땅을 짚음은 각기 다른 지지 상태다. 눈물·벌어진 입술·젖은 피부가 고통·소진 문맥에 있다면 그것을 성적 감정으로 바꾸지 않는다. 미완 발언·명령 내용·항복은 작성된 서사로 표현할 수 있지만 정지 사진만으로 언어 내용과 실제 내적 상태를 인증하지 않는다.

### 3.12 빛과 품질 표현의 강화는 사건 의미와 별도다

ARRI는 주광·보조광·분리광·배경광의 역할과 광질을 구별한다. 청색 달빛과 따뜻한 촛불은 각각 광원·수신면을 지정하고, 물체의 고유색·금속 반사·전체 색보정과 분리한다. [ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)

Getty는 강조를 크기·색·질감·형태·배치의 관계로 설명한다. 명암 대비·피부 질감·필름 그레인·주의 테이프는 장면 연출에 기여하지만 그 자체로 선정성·범죄·폭력의 증거가 아니다. 필름 그레인은 이미지 평면, 먼지·재는 장면의 깊이에 속한다. [Getty의 디자인 원리](https://www.getty.edu/education/teachers/building_lessons/formal_analysis2.html)

### 3.13 부정 조건의 준수를 긍정 조건과 따로 평가한다

NegBench는 부정 질의·부정 캡션을 별도 과제로 다룬다. 최근 NegT2IBench는 생성에서도 긍정 조건과 부정 조건의 수를 독립 변화시키는 설계를 제시한다. 후자는 2026-10-02 프리프린트이며 초록 범위에서 참고했다. 이 연구들의 수치를 현재 사용 모델의 실패율로 쓰지 않는다. [NegBench](https://arxiv.org/abs/2501.09425), [NegT2IBench](https://arxiv.org/abs/2610.03084)

`no blood`는 유혈 배제이지 action 전체 배제가 아니다. 부정 목록의 `lingerie`를 긍정 prototype에 넣지 않는다. `broken wrists`, `dislocated shoulders`는 해당 원문의 해부학 오류 방지 조건이며 원하는 피해가 아니다. 중국어 부정과 `rather than`의 범위도 보존한다.

역사적 부정 지시를 모든 미래 요청의 전역 기본값으로 복제하지 않는다. 현재 요청에 근거한 exclusion만 의미 권위를 가지며, 기존 intent-neutral photographic defect controls와 구별한다.

## 4. 22개 분류별 반영 지도

| 분류 | 중심 보강 | 제안 |
|---|---|---|
| 01 직접 분위기 | 관능·친밀·위험의 별도 의도와 운반체 | 001 |
| 02 몸에 맞는 실루엣 | 핏/체형/슬릿/절개선/숨겨진 패드 | 002–005 |
| 03 재질·촉각성 | 소재/직조/광택/무광/마모의 소유 | 006–009 |
| 04 목선·개방성 | 모양·깊이·부위·끈의 연결과 이탈 | 010–013 |
| 05 젖음 | moisture/contact/transmission과 owner | 014–018 |
| 06 액세서리 | 길이·링·연결점·처짐·매듭 | 019–023 |
| 07 사적 공간·자세 | 침구 접촉·거울 시선·자기 손·봉헌 | 024–028 |
| 08 표정 | 눈의 목표·눈꺼풀·작은 입술 틈 | 028–029 |
| 09 시점 | 카메라 높이/방향·필수 관계 가독성 | 030–031 |
| 10 장비 | 개수·장착·소유; 공격과 별도 | 032–033, 037 |
| 11 전투 동작 | 손-물건 접촉·부분 발도·방향·시간 한계 | 034–036 |
| 12 마법 충돌 | 원점·경로·막·국소 입자·망토 | 038–040 |
| 13 제압 | 비성적 contact/restriction/support 구분 | 041–042 |
| 14 언쟁 | 화자·청자·문턱·비접촉 간격·서사층 | 043–044 |
| 15 전투 후 흔적 | 사물 파손/공기 흔적/인물 상태 | 045–046 |
| 16 피해 흔적 | 국소 mark/멍/천/피해 정도와 owner | 047–050 |
| 17 소진·생존 | 지지 이전·고통 맥락·패배 화면 텍스트 | 051–053 |
| 18 밀폐·공포 | 유리 접촉·공간 경계·환경·치아 형태 | 054–056 |
| 19 일반 연출 | 광원-표면·grain/particle·증거 유지 | 057 |
| 20 선정 배제 | polarity/scope·역사 지시의 적용 경계 | 058 |
| 21 폭력 배제 | semantic exclusion/defect repair 분리 | 059 |
| 22 반례·보존 | coverage/identity/color/age의 별도 축 | 049, 060 |

숫자는 VEL 카드의 끝 번호다. 각 표현의 정확한 연결은 대조표에 있다. 원본 범주를 강도 점수나 안전 판정 enum으로 전환하지 않는다.

## 5. 반영 구조

키워드 한 행을 그대로 candidate 한 행으로 복사하지 않는다. 원본 K ID는 연구 provenance이고, 런타임의 의미 ID와 다르다. 연구 결과는 다음 경로로 채택한다.

1. 기존 의미와 owner·상태·효과가 같으면 등가 paraphrase와 명확한 component 표현만 보완한다.
2. 다른 물건·소유자·행동·상태이면 새 선택형 원자/관계를 작은 배치로 만든다.
3. 채택 후보의 실제 target/property와 영향 dimension을 현재 core에 맞게 바인딩한다.
4. 선택된 관계에 필요한 증거를 authored-components/v2와 기존 profile/compiler 계약으로 연결한다.
5. 추상 정서·시간·동의·기능은 형태의 positive prototype이나 hard gate로 옮기지 않는다.
6. 연구 URL·원문·출처 제목·대량 키워드는 배포 의미 데이터에 복사하지 않는다.
7. authored source를 ordered manifest에 등록한 뒤 semantic/visual-profile index를 다시 생성한다.

정상 후보팩 경로는 pre-core 독립 저작 → core 동결 → 슬롯 후보 검색 → visual-profile resolution → 선택적 해석/조합 → v6 후보팩이다. broad label, BM25F/embedding hit, bundle 연관은 새 hard duty를 만들지 않는다. 후보 때문에 core의 연령·노출·인물 수·정체성·행동·피해 정도를 고치지 않는다.

[반영 위치 대조 JSON](RUNTIME-MAPPING.json)은 기존 source와 제안 source를 명확히 구별한다. 새 source 두 쌍은 제안 이름이며 파일을 생성하거나 manifest에 등록하지 않았다. 현행 candidate-pack/v6의 공개 스키마를 새로 만들 필요는 없다.

## 6. 검증과 완료 경계

[회귀 계획](REGRESSION-PLAN.json)에 462개 개발 검증 사양을 작성했다. 이것은 실행된 테스트 결과가 아니다. 자연스러운 한국어/영어 paraphrase와 인접 의미의 holdout은 반영 직전에 개발 예시와 독립적으로 작성하고 바이트를 동결해야 한다.

[이미지 검증 계획](PIXEL-QUALIFICATION-PLAN.json)은 18개 대비군을 제안한다. 우선 여섯 군에서 2개 조건×3회 반복, 총 36장의 별도 실험을 계획했다. 현재 생성은 0회다. 각 실험은 같은 요청 의미·control·기본 장면을 유지하고 후보/관계 채택만 비교한다. seed가 노출되지 않는 provider라면 독립 반복으로 기록한다.

의복 연결·접촉점·간격·소유자·정도는 native pixels로 함께 확인한다. 선택한 필수 관계가 가려지면 `UNOBSERVABLE_NOT_PASS`, 생성이 차단되면 `BLOCKED_UNSCORED`다. 프롬프트/audit PASS, 실제 후보 노출, 선택, 이미지 기술 평가, 사용자 선호는 각각 별도 증거다. 연구 검증 PASS만으로 강화의 실효성이나 인과 효과를 보고하지 않는다.

원 source의 미성년·학생·연령 혼용 사례는 비성적 언쟁·액션·지지의 연구 자료로 유지한다. 그것을 성인으로 바꿔 성적 원본 재현을 만들지 않는다. 이후 독립적인 성인 패션 실험을 작성한다면 역사 자료 replay와 명확히 구별해야 한다.

원본 사전의 source count에 없는 의복 파편 사례는 참조 대화 6절의 본문 보충 사례다. VEL-050은 이를 별도 provenance로 남겼으며 존재하지 않는 source ID나 연령을 발명하지 않았다.

## 7. 결과 파일

- 읽기 시작: 이 문서와 [반영 계획](IMPLEMENTATION-PLAN.md)
- 표현별 추적: [217개 Markdown 대조표](KEYWORD-CROSSWALK.md), [CSV](KEYWORD-CROSSWALK.csv), [현재 어휘 이웃](CURRENT-COVERAGE.json)
- 제안 검토: [60개 상세 카드](SEMANTIC-CARDS.md), [원본 JSON](RESEARCH-PROPOSALS.json), [후보 초안](CANDIDATE-DRAFTS.json), [선택형 조합](BUNDLE-DRAFTS.json)
- 실행 설계: [실제 파일 매핑](RUNTIME-MAPPING.json), [회귀 사양](REGRESSION-PLAN.json), [native 검증 계획](PIXEL-QUALIFICATION-PLAN.json)
- 근거: [외부 자료](SOURCES.md), [현재 source snapshot](CURRENT-SOURCE-SNAPSHOT.json), [읽기 동안 hash 확인](AUDIT-SOURCE-HASHES.json), [연구 무결성 결과](VALIDATION.json)

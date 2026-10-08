# 패션 핏: 시각 의미·후보 데이터 강화 리서치와 반영 계획

2026-10-08 KST. 기준 대화: [패션 핏 용어 조사](chatgpt-conversation://6ac663bd-9f50-83e8-9f1d-d9cc4afbe32f).

핏 데이터는 **의복의 부위별 여유·접촉, 윤곽, 기준선, 패널 연결, 원단 거동, 커버리지, 현재 착용 상태**를 독립적으로 다루는 것이 효과적이다. 같은 바지에 slim·high-rise·bootcut·cropped가 함께 성립할 수 있으므로, 하나의 상호 배타적인 핏 목록으로 만들면 의미를 잃는다. 이 분해는 공식 제품 가이드의 지역별 핏·다리 형태 구분과 패턴 제작사의 여유량 설명을 바탕으로 한 연구 설계다. [Levi's 핏 가이드](https://www.levi.com/GB/en_GB/features/men-jeans-guide), [Seamwork 여유량 설명](https://www.seamwork.com/sewing-tutorials/understanding-ease).

이번 결과는 **21개 분류의 원문 용어 513개, 출처 41개, 상세 의미 카드 64개, 후보 문장 초안 119개, 혼동 비교 시나리오 38개**다. 119개는 실제 신규 엔트리 수가 아니다. 기존 의미 재사용, 동등한 표현 보강, 새 지역 관계, 기술 메타데이터를 구분한 설계 초안이며, 런타임 등록·인덱스 재생성·생성 실험은 이번 연구에서 실행하지 않았다.

## 1. 원문 확보와 근거의 범위

참조 대화의 API 본문은 20,000자에서 끊겼다. 공식 ChatGPT 화면의 렌더된 본문을 추가로 읽어 1~21절의 용어 표와 22절의 비교·조합 표를 확인했다. 원문은 용어 행 513개, 비교 행 14개, 조합 예시 행 6개로 구성된다. 한 행의 여러 별칭은 별개 용어로 중복 집계하지 않았다. [원문 용어 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/seed-terms.txt), [원문·기존 표현 대조 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/term-inventory.json).

41개 출처는 제작사·패턴 개발자·브랜드의 공식 설명, V&A의 소장 복식 해설, FIT의 기관 용어 연구, 출판사 사전이다. 기술적 원인은 제작사 자료를 우선하고, 역사적 외형은 시대·물체를 가진 기관 자료로 구분했다. FIT의 문헌 종합 자료를 새로운 실험 연구로 표현하지 않았다.

Coats·LYCRA 등의 직접 열기 오류, Cambridge의 403, Nike의 짧은 페이지 셸, Tommy의 지역 홈페이지 리다이렉트는 원장에 남겼다. 이 경우 공식 검색 제공 본문·발췌가 근거다. 원문 설명, 근거에 한정된 사실, 연구자가 제안한 구성 문장과 검증 설계는 서로 다르다. **513개의 모든 별칭을 각기 독립된 출처로 재검증했다는 뜻은 아니다.** 용어별 가족 매핑과 승격 전 확인 조건을 [반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/term-plan.csv)에 기록했다.

| 산출물 | 내용 |
|---|---|
| [상세 카드 64개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/semantic-cards.md) | 뜻, 의복 소유자, 변경 속성, 혼동 경계, 관찰 조건, 기존 ID, 출처, 후보 문장 |
| [후보 초안 119개](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/candidate-proposals.json) | 구성 요소, 관계의 두 끝점, 소유자 결속, 속성 범위, 선택 조건, 이미지 검사 조건 |
| [용어별 반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/term-plan.csv) | 513개 전부의 의미군·처리 방식·우선순위·출처·현재 긍정 필드 이웃 |
| [출처 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/sources.json) | 접근 수준, 확인한 범위, 일반화하면 안 되는 조건 |
| [회귀·이미지 검사 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/regression-plan.json) | 38개 비교, 10개 변경 공격, 12개 이미지 검증 묶음 |

## 2. 현재 저장소의 실제 기준

2026-10-08 **01:19:52~01:20:07 KST**에 현 작업 트리의 공식 로더로 원본을 로드했다. HEAD는 당시 `30fc97a84fb3c8a7863adf0b8b60010dce73b444`이며, 기존 미커밋 변경도 포함한다. 로드 전후 원본·관련 코드의 SHA-256과 mode를 비교했고 그 구간에 변경된 파일은 없었다. 전체 원본 검사기·인덱스 검사·라이브 dispatch를 실행한 것은 아니다. [기준 스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/source-snapshot.json).

| 집계 단위 | 확인 수량 |
|---|---:|
| 후보 슬롯 | 113 |
| 로드된 슬롯 후보 | 10,531 |
| 의미 검색 문서 | 10,567 |
| 컴파일된 시각 의미 프로필 | 2,321 |
| 컴파일된 후보 번들 | 1,117 |
| 등록 원본 확장 | 후보 60 / 시각 프로필 42 |
| 명시적 구성 요소가 있는 후보 | 3,157 |
| 명시적 관계가 있는 후보 | 2,418 |
| 명시적 부분 속성 범위가 있는 후보 | 1,808 |

이 수치는 데이터 품질 점수가 아니다. 단일 소재 후보와 여러 끝점을 가진 의상 관계 후보는 필요한 구조가 다르다. 이번에는 후자에서 뜻·소유·범위가 부족한 곳을 우선 조사했다.

513개 씨앗의 한국어·영어·행 내 별칭을 현재 코드의 긍정 검색 필드와 대조했다. 후보에 표현이 있는 씨앗은 238개, 프로필에 있는 씨앗은 197개, 합집합은 244개다. **남은 269개를 의미 누락이라고 계산할 수 없다.** 표면 문구가 없어도 같은 구조가 다른 말로 저장돼 있을 수 있다. 반대로 표현이 있어도 다른 대상·맥락일 수 있다. 임베딩, 실제 코어 검색, 후보 노출, 선택, 이미지 결과의 증거도 아니다.

### 기존 의미 재사용과 보강 지점

| 원문 씨앗 | 확인한 기존 항목 | 반영 판단 |
|---|---|---|
| body-skimming | `pfe_skimming_candidate`, `pfe_skimming`, `bias_cut_body_skimming_drape` | 접촉 사이 처짐은 이미 구체적. 성인 초상 범위와 일반 의복의 중립 의미를 구분 |
| boxy | `ctx_c150` | 재킷·바지·인물이 함께 묶인 장면형 후보. 몸통 윤곽만 쓰는 원자로 분리할 가치 |
| drop shoulder | `sff_pro_c24` | 연결선 요소가 있지만 효과 범위가 `wardrobe` 전체. 어깨·연결선의 부분 범위 보강 우선 |
| princess seam / dart | `clt_ct031_v1/v2`, `clothing_ct031_v1/v2` | 기존 패널 연결·다트 끝점 재사용. 공주 스타일·시선 dart 반례 추가 |
| raglan | `clt_ct044_v1/v2`, `clothing_ct044_v1` | 기존 연결선 재사용. 소매 길이·여유와 독립인 검색 표현 보강 |
| bishop / puff | `clt_ct047_v1`, `clt_ct046_v2` 및 대응 프로필 | 기존 커프스 모음·상부 부풀음 재사용. bell과 구별 |
| godet / pleat / shirring / smocking | `clt_ct030_*`, `clt_ct063_*`, `clt_ct064_*`, `sw_shirred`, `sw_smocked` | 의복 부위와 소재를 맞춰 재사용. 이름만 묶은 복제 프로필 불필요 |
| barrel leg | `balloon_leg_curve_tapered_hem`, `balloon_curved_leg_tapered_hem` | barrel 표현은 없지만 가까운 곡선·밑단 수축 의미 존재. 동등성 검토 후 표현 보강 또는 변형 분리 |
| high-leg | `sw_candidate_highleg`, `sw_highleg` | 허리선과 다리 가장자리 구분을 이미 지원. 소유자·속성 범위 보강 |
| racerback / cross-back | `racerback_sports_bra_strap_convergence`, `crossback_strap_intersection` | Y 합류와 X 교차의 끝점 보존. 후자의 구성 요소·관계 필드를 명시화할 가치 |
| pannier / bustle | `hw_lateral_pannier`, `hw_shelf_bustle` | 방향 관계 이미 지원. 역사 버전과 관찰 가능한 속성 유지 |
| curvy fit / cup gaping / waist gaping | 해당 정확 표현의 긍정 필드 이웃 없음 | 몸 수정 없이 의복의 지역 분량·국소 경계 관계를 추가하는 후보 우선 |
| negative ease / compression fit | 해당 정확 표현의 긍정 필드 이웃 없음 | 측정·설계 의미 먼저 보강. 밀착 사진을 압력·수치 증거로 승격하지 않음 |

`mermaid`에는 수중·신화 대상이, `tapered`에는 화장·붓 선 형태가, `dart`에는 눈 행동이 섞인다. `trouser break` 씨앗의 별칭에도 사건·패턴 중단이 이웃으로 잡혔다. 이는 문맥 없는 연구 질의의 혼동 신호다. 실제 runtime 오류가 확인됐다고 주장하지 않고, 의복 소유·부위·지역 효과를 가진 반례로 검사한다. [관련 기존 레코드 발췌](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/current-positive-records.json).

## 3. 조사에서 확인한 중요한 경계

### 3.1 여유는 지역 분포이며 밀착은 수치가 아니다

여유량은 대응하는 신체와 완성복 치수의 차이다. 착용 여유와 디자인 여유는 목적이 다르고, negative ease는 완성복이 더 작은 설계다. 같은 총 여유가 있어도 어깨·가슴·허리의 배분이 다르면 다른 외관을 만들 수 있다. 사진에서 저장할 단서는 직물 경계, 접촉 구역, 비접촉 구간과 처짐이다. **밀착·부드러운 주름만으로 -5cm나 신장률 30%를 확정하지 않는다.** [Seamwork](https://www.seamwork.com/sewing-tutorials/understanding-ease).

FF01·FF02는 수치 정의를 유지하면서 보이는 관계를 분리한다. 수치 요청 자체를 지우지 않고 명세로 보존하되, 측정 근거 없는 이미지 평가에서 수치 PASS를 주지 않는다.

### 3.2 커비핏은 옷의 분량 관계다

Madewell은 contoured waistband와 추가 힙·허벅지 여유를 Curvy의 특징으로 설명하고, 특정 허리-힙 차이 기준을 제시한다. 이 기준은 브랜드 소유의 기준이다. [Madewell](https://www.madewell.com/womens/denim/).

FF05의 관계는 `옷의 허리 구역 → 옷의 힙·허벅지 구역`이다. 기존 착용자의 허리·가슴·힙을 더 크게 또는 작게 만드는 후보가 아니다. `Athletic fit`도 지역 의복 분량으로 다루며 근육량을 새로 추가하지 않는다. `Curvy`라는 몸 의미와 `curvy-fit trousers`라는 의복 의미를 다른 소유자에 둔다.

### 3.3 실루엣 이름보다 퍼짐 시작점과 곡선이 안정적이다

Pronovias의 같은 페이지는 mermaid를 trumpet으로 부르기도 하면서, 별도 문단에서는 낮게 퍼지는 차이를 설명한다. 전 세계 공통의 한 경계로 저장하기 어렵다. [Pronovias Mermaid](https://www.pronovias.com/wedding-dresses/mermaid).

FF08은 `힙·허벅지를 따르는 직물 → 지정한 위치에서 퍼지는 하부 치마`를 저장한다. 무릎 또는 무릎 위가 요청·선택된 경우에만 그 위치를 검사한다. FF26도 “배럴”이라는 이름보다 양쪽 볼록한 외곽·최대 볼륨·매끈한 하부 수축을 저장하고 기존 balloon 의미와 먼저 대조한다.

H·I·X·Y 같은 문자 이름은 요청된 의복 윤곽을 찾는 접근 표현으로 유지한다. 이번 출처가 모든 문자 이름의 보편적인 독립 규격을 확증하는 것은 아니므로, 명칭만으로 몸 비율·길이·볼륨을 일괄 변경하지 않는다.

### 3.4 소매는 연결 구조·볼륨·끝단이 서로 다른 변수다

래글런·셋인은 연결선, 퍼프·지고는 볼륨 분포, 비숍·벨은 끝단의 모음·열림을 구별한다. 마리는 반복 결속과 사이 구간의 볼륨을 읽는다. 소매 길이·핏·재료는 별도로 선택한다. [Mood의 소매 연구](https://blog.moodfabrics.com/all-about-sleeves/), [FIT Gigot](https://fashionhistory.fitnyc.edu/gigot-sleeve/).

2026-10-01 발표된 Opal은 cut-on dolman의 몸판 연속성을 공식 제작 예로 보여준다. Oliver는 lantern이라는 실제 패턴 용어를 확인해 주지만, 특정 패널 연결을 hard 의미로 승격하려면 그 변형의 도해 확인이 더 필요하다. [Opal](https://www.seamwork.com/sewing-patterns/introducing-the-opal-sewing-pattern), [Oliver](https://www.seamwork.com/sewing-patterns/all-about-the-oliver-top).

### 3.5 안감·캔버스·패드·컵 성형은 독립 구성이다

Proper Cloth에는 패드가 없는 fully canvassed 변형도 있다. 따라서 unlined·unstructured·unpadded를 동의어로 처리할 수 없다. 외관의 부드러움만으로 내부 캔버스 비율을 검사하지 않는다. [Proper Cloth 구성 설명](https://propercloth.com/reference/jacket-construction-and-the-options-we-offer/).

Bravissimo는 moulded T-shirt bra에 padded와 non-padded가 모두 가능하고 wired bralette 변형도 있다고 설명한다. FF41은 컵 성형·패딩·와이어·커버리지를 분리한다. [Bravissimo 스타일 가이드](https://www.bravissimo.com/bra-style-guide/).

### 3.6 주름과 들뜸은 현재 상태이며 원인은 별도다

Tilly는 정상적인 바지에도 굽힘·동작 주름이 생긴다고 설명한다. Coats는 seam puckering에 장력·원단 구조·치수 변화·피드 등이 관여한다고 구분한다. Bravissimo는 컵 들뜸에 크기와 shape 문제 모두를 언급한다. [Tilly 바지 피팅](https://tillyandthebuttons.com/blogs/sewing/common-trouser-fitting-adjustments), [Coats](https://www.coats.com/en-us/info-hub/eliminating-seam-puckering/), [Bravissimo 피팅](https://www.bravissimo.com/bra-fitting-guide/).

FF42·FF56~58은 `특정 옷의 가장자리 → 그 옷과 몸 사이 틈`, `단추 고정점 → 모이는 직물`, `솔기 → 옆의 잔주름`처럼 저장한다. 사진 한 장에 자동 수선 지시·사이즈 부족·불편함·세탁 실패를 붙이지 않는다. riding up·recovery 같은 변화는 전후 또는 시퀀스 근거가 따로 있어야 한다.

### 3.7 커버리지·비침·윤곽·지지 성능을 분리한다

high-leg는 다리 개구부, high-waist는 허리 경계다. illusion panel은 연결된 얇은 직물이며 실제 빈 개구부와 다르다. 보이는 피부색은 피부·안감·안쪽 옷 중 어떤 표면인지 구분해야 한다. VPL은 겉감 위의 아래층 경계이며 직접 피부 노출과 같지 않다.

원문의 open-cup·cupless·open-crotch·sideboob·underboob·bulge·camel toe·wedgie 등을 삭제하지 않았다. 의복 구조·노출 위치·겉 윤곽·제품명·착용 상태의 차이를 그대로 유지한다. Cambridge는 camel toe의 속어 의미를, Levi's는 Wedgie가 제품명으로도 쓰인다는 것을 확인해 준다. 직접 열기의 제한과 별도 확인이 남은 속어는 원장에 표시했다. [Cambridge](https://dictionary.cambridge.org/us/dictionary/english/camel-toe), [Levi's Wedgie](https://www.levi.com/US/en_US/clothing/women/jeans/straight/wedgie-straight-womens-jeans/p/349640287).

compression·support·recovery·GSM·섬유 상표·UPF 같은 기술 조건은 단순한 밀착이나 비침에서 추정하지 않는다. LYCRA의 PCE도 제품 성능 시험 체계이며 보편 이미지 속성이 아니다. [Apostrophe 신축 측정](https://apostrophepatterns.com/pages/fabric-stretch), [LYCRA 성능 지표](https://one.lycra.com/en/business/news/made-measure-lycra-sport-performance-indexing).

### 3.8 역사적 볼륨은 지지 방향과 버전을 가진다

파니에는 좌우 확장, 버슬은 뒤 돌출, 크리놀린은 별도의 후프 받침을 가진다. bum roll과 bombast도 내부 받침·충전 방식이므로 착용자 신체 특징으로 대체하면 안 된다. 현대 steel-boned 코르셋 상품의 조건을 모든 역사적 stays에 강제하지 않는다. [V&A](https://www.vam.ac.uk/articles/corsets-crinolines-and-bustles-fashionable-victorian-underwear), [FIT Panniers](https://fashionhistory.fitnyc.edu/panniers/), [Bum Roll](https://fashionhistory.fitnyc.edu/bum-roll/), [Bombast](https://fashionhistory.fitnyc.edu/bombast-bombasted/).

## 4. 원문 21개 분류별 강화 지도

아래의 카드 번호는 위 상세 카드 파일과 연결된다. “반영”은 구현 예정 방향이며 현재 런타임 변경 완료를 뜻하지 않는다.

| 원문 분류 | 행 수 | 강화할 중심 | 카드 |
|---|---:|---|---|
| 1 기본 개념 | 16 | 치수·여유와 보이는 지역 관계를 분리 | FF01, 06, 38, 59, 64 |
| 2 밀착·여유 명칭 | 30 | 접촉 분포·분량·박시·체형 대응형 의복 비율 | FF02~05, 22, 24 |
| 3 전체 윤곽 | 20 | 폭 분포·부풀음·수축·퍼짐 위치 | FF06~08 |
| 4 어깨·암홀·소매 | 34 | 연결선·소매산·지역 볼륨·끝단 | FF09~16 |
| 5 목둘레·어깨 범위 | 24 | 가장자리 곡선·지지 연결·개구부 | FF17~20, 29 |
| 6 허리선·몸통 | 16 | 몸 기준선과 의복 연결선·수축 기구 | FF21~23 |
| 7 바지 치수·구조 | 18 | 허리단·다리 분기·측정선·요크 | FF23~24, 35, 59 |
| 8 바지 핏·윤곽 | 27 | 폭 변화·곡선·커프스·두 다리 연결 | FF24~27 |
| 9 스커트·드레스 | 19 | 접촉·패널·랩·삽입·받침 | FF28~29, 36~37, 60 |
| 10 길이·밑단 | 26 | 몸 기준점·신발·바닥과 끝단 관계 | FF30~31 |
| 11 재킷·내부 구성 | 21 | 전면 겹침·라펠·벤트와 숨은 구조 구분 | FF32~33, 59 |
| 12 패턴·봉제·주름 | 28 | 다트·패널·거싯·접힘 방향·모음 고정점 | FF34~37 |
| 13 소재 거동 | 28 | 처짐·강성과 측정·성분·이력 분리 | FF38~39, 49 |
| 14 브라 | 28 | 컵·밴드·고어·와이어·커버리지·현재 틈 | FF40~42 |
| 15 코르셋·보정복 | 24 | 패널·케이싱·여밈과 기술 치수 분리 | FF43~46 |
| 16 바디웨어·노출 | 33 | 연결 구조·다리 개구부·층·경계·외곽 | FF47~51, 62 |
| 17 운동복·기능 의상 | 18 | 끈 접속·솔기·관절 패널·조절 경로 | FF39, 52~55 |
| 18 피팅 문제 | 27 | 현재 틈·당김·잔주름·이동과 원인 분리 | FF42, 56~58 |
| 19 치수·제작·보정 | 35 | 체계·측정·공정과 요청된 결과 구분 | FF54, 59 |
| 20 역사·대체 패션 | 16 | 받침 방향·시대별 보디스·스트랩·절개 | FF60~62 |
| 21 한국어 인상 표현 | 25 | 의복·부위·거동에 따른 조건부 해석 | FF63 및 구체 관계 |
| 합계 | **513** | 모든 행에 반영 경로 있음 | 상세 CSV 참고 |

1차 분류는 시각 형태·상태 352개, 명세·공정 97개, 브랜드/가변 경계 26개, 시간·이력 6개, 명시적 맥락/제품명 7개, 한국어 문맥 표현 25개다. 각 행의 대표 처리 경로이지 상호 배타적인 자연 법칙이 아니다. 같은 용어의 관찰 가능한 변형과 숨은 기능이 함께 있을 수 있으며, 구현 때 개별 변형으로 다시 나눈다.

## 5. 데이터에 담을 구조

의미 정의는 하나의 기준으로 관리하되, **시각 의미 검색과 슬롯 후보 검색의 표면은 유지한다.** 의미 카드 한 개가 여러 후보 표현·프로필에 연결될 수 있고, 같은 후보도 여러 의미 조각을 실현할 수 있다. 이름·별칭을 모든 후보에 복제하는 방식보다, `의미 → 구성 요소 → 소유자·관계 → 선택형 후보 → 변경 범위 → 관찰 조건`의 연결을 보강한다.

| 층 | 저장할 내용 | 이번 설계 |
|---|---|---|
| 개념 정의 | 의복 종류·관찰 축·측정 의미·혼동 경계 | 카드 64개, 용어별 카드 연결 513행 |
| 구성 요소 | 패널·솔기·밴드·직물 경계·층·기준점 | 명사만 나열하지 않고 실제 보이는 부위를 선언 |
| 관계 | 주어·관계·목적어, 동일 의복·몸·층의 결속 | 가장자리와 틈, 두 스트랩과 앵커 등 양 끝점 유지 |
| 후보 표현 | 한 선택형 변형의 관찰 가능한 영어 문장 | 119개 초안, 기존 항목과 동등성 대조 후 채택 |
| 변경 범위 | 실제 바꾸는 의복의 부분 속성 | `wardrobe` 전체 대신 어깨 연결·다리 곡선·밑단 위치 등 |
| 문맥 조건 | 이미 선언된 의복·층·자세, 열려 있는 속성 | 다른 옷으로 전파하거나 고정된 신체·구도를 바꾸지 않음 |
| 관찰 조건 | 활성화한 구성 요소의 시각 증거와 게이트 | 가림·크롭으로 필요한 경계를 못 보면 미관찰 처리 |
| 근거 | 출처의 확인 범위·기존 ID·보류 사유 | 배포 스킬 밖의 연구 원장에 유지 |

### 5.1 후보 초안을 실행 데이터로 바꾸는 기준

이번 JSON의 `<bound_garment_id>`, 부위 대안, 가족 수준 관계 연산자는 설계용 자리표시자다. **현재 런타임에 그대로 넣을 수 없다.** 승격 때 선택된 변형의 구체 노드와 단일 관계로 바꾸고, 문장에 들어 있는 모든 효과를 다시 확인한다.

예를 들어 FF09 첫 문장은 셔츠 소매 연결선이 어깨 끝 바깥의 상완에 놓인다는 의미다.

- 구성 요소: 셔츠 몸판, 그 셔츠의 소매 연결선, 같은 착용자의 어깨 끝.
- 관계: `소매 연결선 → 어깨 끝보다 팔 쪽에 위치`, `소매 → 해당 연결선에 부착`.
- 변경 속성: 해당 셔츠의 `fit.shoulder.seam_position`과 `structure.sleeve_attachment`.
- 제외할 자동 효과: 착용자 어깨 폭, 다른 재킷, 의복 색, 소매 길이, 카메라, 나이·성격.
- 선택 조건: 셔츠가 이미 선언되어 있고 두 속성이 수정 가능하며, 문장이 요구하는 추가 길이·재료가 없는지 검토.
- 이미지 조건: 연결선과 어깨 기준이 같은 옷·착용자에서 읽힌다. 가려진 연결선을 이름만으로 PASS 처리하지 않는다.

기존 `sff_pro_c24`의 `wardrobe` 범위를 줄이는 것은 단순 별칭 추가와 다르다. 원본·기존 유지보수 기록을 보존하고, 완전한 효과 범위와 successor 기록으로 검증해야 한다. 기존 성인 초상 프로필도 유지하면서, 실제 중립 의복 범위가 필요한 경우 별도 변형을 검토한다.

### 5.2 조합은 각 구성 요소의 독립 선택을 유지한다

원문 조합 예시의 “크롭 박시 재킷 + 드롭 숄더 + 와이드 소매”에는 길이·몸통 윤곽·연결선·소매 폭이 있다. “하이 라이즈 + 여유 있는 허벅지 + 테이퍼드 + 발목 길이”도 허리 기준선·지역 여유·다리 폭 분포·밑단 기준점으로 나눈다.

FF64는 이 구성 요소들을 같은 의복에 연결하는 **선택형 번들**이다. 전부가 필수인 고정 장면을 새로 만드는 계획이 아니다. 고정된 발목 길이에 full-length 후보가 섞이면 제외하고, 장면에 바지가 두 벌 있으면 어느 바지의 속성인지 결속한 뒤 선택한다. 모든 후보에 투명도·노출·신체 비율 같은 추가 기본값을 넣지 않는다.

## 6. 반영 실행 계획

목표는 새 단어 수를 늘리는 것이 아니라, 요청된 핏의 **대상·지역 형태·관계가 검색과 구성에서 보존되고, 이미지에서는 관찰 가능한 경계를 구별하는 것**이다. 아래 단계와 완료 조건을 [구조화한 실행 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/implementation-plan.json)에도 기록한다.

### 단계 1 — 기존 의미와의 동등성·승격 범위 결정

카드 우선순위는 P0 30개, P1 28개, P2 6개다. P0는 부위 여유·커비핏·어깨 연결·다리 곡선·기준선·컵 상태·비침·문맥 혼동처럼 잘못 결합될 때 의미가 달라지는 축을 먼저 다룬다. P1은 패널·여밈·세부 볼륨·역사적 구조를 보강한다. P2는 구조 도해·속어별 근거가 더 필요하거나 대표 수요가 확인되지 않은 변형을 검토한다.

513행마다 다음 네 경로를 확정한다.

1. **기존 의미 재사용**: 소유자·지역 효과·관찰 조건까지 같으면 ID를 유지한다.
2. **동등한 표현 보강**: 뜻을 바꾸지 않는 문맥·별칭만 추가한다. raglan·princess seam·barrel/balloon 등이 후보이며, 명칭 유사성만으로 동등하다고 결정하지 않는다.
3. **새 변형 또는 좁은 범위 보강**: 의복 지역 관계가 없거나 기존 범위가 다를 때 작성한다. curvy-fit 지역 분량, 국소 들뜸, drop-shoulder 부분 효과가 우선이다.
4. **기술 명세·보류**: 수치·성분·촉감·공정·숨은 기능·변화 이력은 명세를 유지하고, 보이는 결과만 별도 변형으로 다룬다.

119개 초안은 검토 재료다. 중복을 제거한 최종 신규 수는 이 단계에서 결정한다. lantern의 특정 패널 도해, 한국어 인상 표현의 선택 문맥, bulge·wedgie 상태와 shelf-bra의 개별 변형처럼 가족 수준 출처만 있는 부분은 직접 자료를 확인한 후 승격한다. 의료·편안함·성능·치수 원인을 외관에서 역으로 추가하지 않는다.

**완료 조건:** 전 용어가 재사용 ID·보강 대상·신규 변형·명세 유지·근거 보류 중 하나 이상에 연결되고, 새로운 hard 의미에는 해당 변형을 직접 지지하는 근거와 혼동 반례가 있다.

### 단계 2 — 원본 확장과 프로필 작성

작성 후보 파일은 `assets/photo_prompt_fashion_fit_extension.json`과 `assets/photo_prompt_visual_obligations_fashion_fit.json`이다. 이는 이번에 만들어 등록한 파일이 아니라 후속 구현의 제안 경로다. 실제 작성 전에 당시 작업 트리와 등록 순서를 다시 확인하고, 기존 중복 파일과 충돌하면 좁은 기존 확장을 보강한다.

- 확장은 `assets/photo_prompt_source_manifest.json`에만 등록한다. 파일 종류·필수 여부·중복 없는 load order를 선언한다.
- 동등한 문맥 표현은 `existing_slot_context_extensions`를 검토한다. 뜻·소유자·효과가 달라지면 별도 변형으로 작성한다.
- 후보에는 필요한 `concept_units`, 구체 `relations`, 완전한 `affected_properties`를 작성한다. 길이·재료·커버리지·소매를 문장에 추가했다면 그 효과도 빠짐없이 선언한다.
- 프로필 원본은 `authored_components`로 작성한다. 단순 일대일 의무는 v1, 한 관계의 여러 구성 요소·증거가 함께 필요한 경우는 v2를 검토한다. 생성 필드와 모든 선택형 문장을 원본 hard all-of에 복사하지 않는다.
- 새 후보가 연령·신체·표정·성격·장면을 요청 없이 변경하지 않도록 한다. sensual 조건의 연령 정책은 기존 계약을 따른다.
- 기존 유지보수 기록을 덮어쓰지 않고, 바뀐 authored body hash와 변경 범위를 successor 기록에 연결한다.
- 출처 URL·원문 인용·용어 전체 목록·연구 과정은 연구 폴더에 둔다. 런타임 검색 텍스트에는 추상화한 시각 의미와 적절한 문맥만 넣는다.

**완료 조건:** 모든 등록·참조·소유자·부분 범위·동등성·변경 효과가 원본 검사에 통과한다. 다른 의복이나 몸까지 바꾸는 후보, 이미 고정된 속성을 넘는 후보는 제외된다.

### 단계 3 — 파생 인덱스와 런타임 세대 갱신

원본이 확정된 뒤 manifest 메타데이터, semantic/BM25F 문서, visual-profile registry와 인덱스를 같은 원본 기준으로 갱신한다. 다른 작업의 파생 샤드를 손으로 합치지 않는다.

호환 벡터 재사용은 entry·완전한 입력 텍스트·provider·model·dimensions가 일치하는 경우에 한한다. 새 텍스트는 실제로 임베딩이 필요하며 batch size 1의 기존 빌더 절차를 따른다. 문맥·별칭 수정도 해당 dictionary hash와 검색 문서에 영향을 주는지 확인한다. 프로필 registry 수정은 텍스트가 같아도 hash·인덱스 갱신이 필요하다.

현재 유지보수 계약의 `source_update`와 정식 빌더·publisher를 사용해 완성된 세대만 활성화한다. semantic·visual 인덱스가 아직 다른 원본을 가리키면 pending 상태이며, 파일이 존재한다는 이유로 최신 검색 성공이라고 처리하지 않는다. [현재 유지보수 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md).

**완료 조건:** 원본 검사, 양쪽 deep index 검사, source/registry hash와 실제 요청 receipt의 세대가 일치한다. 필요한 임베딩 호출과 재사용 수를 따로 기록한다.

### 단계 4 — 검색·선택·구성의 회귀 검증

후보 데이터를 읽기 전에 독립적인 요청·controls·frozen core를 작성한다. 한국어/영어의 38개 비교를 계획했으며, 최소 쌍은 한 핏 축만 바꾼다. skinny/slim, curvy-fit/curvy-body, princess-seam/princess-style, mermaid-dress/mermaid-character, Y/X straps, high-waist/high-leg, drop-shoulder/padded-shoulder 등이 포함된다.

우선 검증할 것은 단순 hit 수보다 다음 관계다.

1. 해당 의복과 문맥에서 올바른 후보가 공개 후보 표면에 나타난다.
2. 다른 의미의 이웃은 선택되지 않거나 문맥·고정 속성 guard로 제외된다.
3. 선택하지 않은 후보는 frozen core에 없던 hard 의무를 만들지 않는다.
4. 명시적으로 선택한 후보는 같은 의복의 해당 속성만 수정한다.
5. 구성 프롬프트와 audit에서 요청의 색·길이·층·몸·촬영 조건, 세대 receipt가 보존된다.

10개 변경 반례는 색·비침·소매 길이·다른 의복 소유자·몸 치수·퍼짐 위치·안감·Y/X·크롭 밖 경계·이름만의 hard 승격을 다룬다. 실제 public 경로의 노출·선택·구성 결과와 hard activation을 검사하고, 이번 긍정 필드 문자 일치를 그 증거로 대체하지 않는다.

관련 기존 테스트는 `test_photo_candidate_semantics.py`, `test_photo_core_retrieval.py`, `test_photo_visual_profile_retrieval.py`를 시작으로, casualwear·activewear·body_morphology·swimwear·costume_cosplay의 해당 모듈이다. 변경된 축의 invariant와 신규 반례를 추가해 `python -m unittest discover -s tests -p '<module>.py'` 방식으로 검증한다. 원본 dictionary와 visual index 검사는 단계 3 결과에 포함하고, 서로 다른 경로를 건드리거나 해결되지 않은 회귀가 있으면 범위를 넓힌다. 기존 historical fixture를 실패 뒤 새 기대값으로 덮어쓰지 않는다.

**완료 조건:** 정해진 비교·변경 반례와 영향받는 기존 회귀가 통과한다. 기존 실패가 있으면 동일 사례인지 따로 입증하며 전체 통과로 표현하지 않는다.

### 단계 5 — 생성 요청이 있을 때 이미지 검증

이번 작업에서는 생성하지 않았다. 후속 생성이 요청되면 12개 검증 묶음—국소 접촉, 지역 분량, 어깨 연결, 소매 끝단, 다리 곡선, 허리/다리 개구부, 밑단/신발 접촉, 비침 층, 컵 들뜸, 뒤 끈 연결, 여밈 끝점, 역사적 부피 방향—을 대표 실험으로 사용한다.

동일한 frozen request와 controls, 제공되는 경우 동일한 seed·생성 설정을 사용하고, 실제 전달 요청과 원본 이미지를 보존한다. 같은 seed도 동일한 픽셀을 보장한다고 가정하지 않는다. 선택된 변형의 게이트만 native pixels로 검사한다.

- 어깨 연결은 연결선과 어깨 기준, Y/X는 두 스트랩 경로와 부착점, 들뜸은 옷 경계와 틈을 같은 크롭에서 읽는다.
- 요청된 구도로 경계를 못 보면 `UNOBSERVABLE_NOT_PASS`다. 관찰을 위해 고정 구도를 자동으로 변경하지 않는다.
- 활성화한 관계 중 한 끝점만 보이면 `partial_is_fail`이다. 비활성 대안까지 모두 요구하지 않는다.
- 압력·신장률·섬유 성분·성능·이동 이력에는 정지 이미지 PASS를 주지 않는다.
- moderation 결과, 시각 의미 보존, 이미지 품질, 사용자 선호를 별도 기록한다.

**완료 조건:** 관찰 가능한 활성 의무가 모두 통과하고 비요청 변경이 없다. 미관찰·차단·부분 충족은 성공에 합산하지 않는다.

### 단계 6 — 결과에 따른 정식 승격

원본·인덱스·검색·구성·이미지·사용자 선호의 증거 수준을 별도 기록한다. 이미지 검증 전 데이터는 authored/retrieval 검증 수준으로만 보고하고, 대표 이미지 품질이나 사용자 수용 완료로 표현하지 않는다.

기존 의미를 충분히 강화하는 변형만 채택하고, 별칭 중복이나 원문 전수 등록을 성과 지표로 삼지 않는다. 구현이 요청되면 당시 concurrent 변경을 보존한 작업 범위에서 진행하며, 커밋·PR·푸시 등 전달 상태는 실제 수행한 단계로 기록한다.

**완료 조건:** 각 채택 항목에 원문 용어, 변형 의미, 작성 ID, provenance, 회귀와 가능한 이미지 증거가 이어지고, 미실행 수준·보류 이유가 명확하다.

## 7. 이번 결과의 검증 상태

| 검증 층 | 상태 |
|---|---|
| 참조 대화의 전체 용어 표 확보 | 완료: 513개 행, 비교 14개, 조합 6개 |
| 출처 조사 | 완료: 41개 접근 수준·확인 범위·한계 기록 |
| 현재 원본의 읽기 전용 로드 | 완료: 조사 당시 hash·mode 안정 구간 확보 |
| 용어 매핑·의미 카드·후보 초안 | 완료: 513행 / 64카드 / 119초안 |
| 반영 계획·회귀 설계 | 완료: 6단계 / 38비교 / 10변경 반례 / 12이미지 묶음 |
| 연구 산출물 참조·ID·집계 무결성 | PASS: 모든 용어 매핑·출처 참조·ID 집계·로컬 링크와 기존 ID 존재 확인 |
| 런타임 원본 통합·인덱스 갱신 | 미실행 |
| 실제 검색·선택·구성 회귀 | 미실행 |
| 이미지 생성·native pixels·사용자 선호 | 미실행 |

[연구 파일 무결성 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/research-validation.json), [문서·참조 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/report-validation.json), [기존 ID 존재 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/existing-id-verification.json), [종료 시점 파일 상태 비교](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/fashion-fit-20261008/final-preservation.json)를 제공한다.

이 작업의 쓰기 범위는 이 보고서와 새 연구 폴더다. 종료 비교에서는 로드 기준 파일 109개 중 108개가 내용·mode 동일했고, 등록 manifest와 별도로 기록한 두 인덱스에는 시작 이후 차이가 있었다. 이번 연구는 해당 파일을 수정·되돌림·stage하지 않았다. 차이는 시점 간 관찰이며 다른 동시 작업의 작성 주체를 증명하는 자료가 아니다. 따라서 위 집계는 명시한 조사 스냅샷 기준이고, 저장소 전체가 그대로였다고 가정하지 않는다.

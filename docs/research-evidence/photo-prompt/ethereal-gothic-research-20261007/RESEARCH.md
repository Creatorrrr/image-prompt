# 에테리얼 고딕 초상의 시각 의미·후보 데이터 강화 리서치

작성일: 2026-10-07 · 상태: 연구 및 반영 계획 작성 완료, 운영 반영 미실행

**이번에 가장 중요한 보강 대상은 고딕이라는 이름보다, 고요한 눈꺼풀 자세·중앙 발광 틈의 가림·꽃가지의 부착·금박과 광원의 구분이다.** 기존 자료가 이미 지원하는 레이스·튈·벨벳·확산·그레인·검정 톤은 재사용하고, 원본의 특별한 관계가 빠진 곳에 좁은 변형을 추가하는 방향이 적합하다.

이 문서는 참조 대화 [이미지 느낌 키워드 추출](chatgpt-conversation://6ac5054b-f064-83ec-bb20-f94cc770a917)의 원본 초상 프롬프트와 회수한 키워드에 기반한다. 사용자는 상세한 조사와 반영 계획을 요청했다. 연구 산출물만 작성했으며 운영 데이터·조회 로직·인덱스·이미지·Git 커밋을 변경하지 않았다.

## 1. 조사 입력과 증거의 범위

참조 대화는 18개 범주 360개 구문, 원형에 가까운 203개와 확장용 157개를 보고한다. 조회의 메시지당 20,000자 제한 때문에 이번에는 **350개**를 회수했다. 01~17 범주는 각 20개, 18 공기감 범주는 앞 10개다. 마지막 10개와 원 파일의 개별 A/B 표시는 회수하지 못했다. 18번 마지막 항목은 영어 `distant candle glow`를 확인했지만 한국어 설명 끝이 잘렸다. 누락 항목을 새로 지어내서 원문 항목으로 채우지 않았다.

[원 대화 발췌](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/REFERENCE-CONVERSATION.json), [350개 seed](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/SEED-KEYWORDS.json), [키워드별 검토 경로](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/KEYWORD-COVERAGE.json)에 입력을 보존했다. 이전 답변의 문구는 조사 대상이며 외부 사실·생성 성능·자동 실행 권한의 근거가 아니다.

증거를 다음과 같이 구분한다.

| 자료 | 이번 조사에서 확인한 범위 | 이 자료만으로 확인되지 않는 것 |
|---|---|---|
| 기관·제조사의 출처 35개 | 짧은 사실 의역, 의미 경계, 접근 상태 | 새 후보의 실제 생성 효과, 원본의 실제 영감 |
| 현재 저작 원본 98개 | 원문 레코드·ID·슬롯·정의와 관계 | 현재 실행 세대와 인덱스의 결합 검증 |
| 의미 카드·후보 초안 | 관찰 요소·소유자·관계·반례·반영 위치 제안 | 운영 스키마 적합성 전체와 조회 순위 |
| 프로토타입 3개 | 현재 컴파일러의 구성요소 투영 | hard activation, owner/property binding, 실제 후보팩 |
| 검증 계획 | 한·영 대비·부정·소유 경계 90개 설계 사례, 픽셀 6그룹 | 테스트 실행·렌더링·사용자 미적 수용 |

출처 35개는 동일한 근거 수준이 아니다. 기관 본문, 분담 연구자가 확인한 본문, 공식 검색 추출문, PDF 일부를 구분했다. 은방울꽃 본문은 403, 일부 기관 PDF·제품 페이지·심도 문서도 접근 제한이 있다. 제한 근거는 [출처 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/SOURCES.md)에 유지한다. 외부 프롬프트의 표현 존재와 촬영·역사 자료의 사실을 섞지 않는다.

## 2. 현재 데이터의 실제 상태

시작 작업 트리는 이미 여러 원본·테스트·파생 인덱스가 수정되어 있었다. 해당 상태를 [스냅샷](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/CHECKOUT-SNAPSHOT.json)에 기록했다. 매니페스트 등록 파일과 기본 파일을 직접 읽은 원문 규모는 후보 행 **10,440개**, 시각 의미 프로필 행 **2,249개**다. 컴파일된 운영 세대의 수량이나 의미 품질 점수로 해석하지 않는다.

350개 구문의 정규화한 전체 문구를 원문 레코드에서 문자 비교했을 때 11개에 일치가 있었고 339개에는 없었다. **339개가 의미적으로 누락됐다는 뜻은 아니다.** 새 문구가 기존의 더 구체적인 정의와 같은 뜻일 수 있다. 이 비교는 직접 표현의 재사용 가능성을 찾는 보조 자료이며 조회 실패율이 아니다. [원문 비교 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/EXISTING-DATA-AUDIT.json)를 남겼다.

| 영역 | 이번에 직접 확인한 기존 항목 | 반영 판단 |
|---|---|---|
| 반쯤 감긴 눈 | `half_lidded_menacing_distant_gaze`, `sleepy_half_lidded_eyes` | 위협·졸림을 유지한 기존 의미는 보존. 고요한 낮은 눈꺼풀 자세를 별도 변형으로 설계 |
| 낮은 번·일자 앞머리 | `low_bun_hair`, `ca_blunt_fringe` | 목덜미 부착·눈썹 상대 높이의 누락 여부를 검토하고 기존 ID 보강 |
| 아르누보 물체 프레임 | `orn_gd54`, `orn_profile_gd54` | 흐르는 곡선이 같은 물체 프레임으로 이어지는 구조 재사용 |
| 연속 망 바탕 꽃 레이스 | `orn_gd31`, `orn_profile_gd31` | 샹티이형 조직 재사용. 안감·모티프 굵은 윤곽은 좁은 보강 검토 |
| 튈·오간자형·시폰형·벨벳 | `clothing_ct090_v2`, `clothing_ct091_v1/v2`, `clothing_ct089_v2` | 망·각진 주름·유동 주름·짧은 결을 재사용 |
| 림·부드러운 광원 | `cr_colored_rim`, `soft_light_shadow_edge_relation`, `pe_rear_rim` | 기존 광원·받는 표면 관계 재사용. 중앙 슬릿과 가림은 별도 구조 |
| 확산·블룸·롤오프·그레인·검정 톤 | `pe_neutral_diffusion`, `pe_local_bloom_relation`, `highlight_rolloff_tone_response`, `pe_fine_midtonal_grain_relation`, `pe_lifted_black_floor_relation` | 기존 영상 효과 재사용. 서로 동의어로 통합하지 않음 |
| 배경 보케 | `pe_background_bokeh` | 작은 광원 원반의 후보다. 식물 가지의 일반적인 초점 흐림으로 재사용하지 않음 |
| 어두운 색·낮은 채도·국소 색 | `cr_dark_on_dark`, `cr_low_chroma` 및 팔레트 응용 확장 | 색 이름을 늘리기보다 기존 물체·광원별 역할을 보강 |

기존 고딕 장식 통합 보고서에는 세/네 로브 대체, 손 접촉 실패, 영어 간접 필리그리 검색 누락과 미완료 전체 회귀가 기록돼 있었다. 그 결과를 이번 초상의 성능으로 옮기지 않았다. 다만 **다른 물체의 맞는 모양을 지정 소유자의 증거로 대신하지 않기**, **선택하지 않은 데이터의 기여를 주장하지 않기**라는 검증 설계에 반영했다.

## 3. 추가 조사에서 얻은 주요 의미 경계

### 3.1. 미술 양식은 문맥, 관찰 형태는 선택 가능한 구체 요소

상징주의의 핵심 설명은 관념·감정의 표현이며 하나의 눈·꽃·조명 조합이 아니다. 따라서 `symbolist-inspired photographic portrait`는 사진의 피부와 직물 표현을 유지하면서 선택한 장식에 상징적 역할을 부여하는 **창작 제안**으로 다룬다. 원본의 실제 미술사적 영향으로 판정하지 않는다. [The Met — Symbolism](https://www.metmuseum.org/essays/symbolism)

아르누보의 유동적인 자연 곡선은 물체 프레임·머리 가닥·실제 가지 중 어디에 놓는지에 따라 다른 데이터다. 이번에는 이미 있는 물체 프레임의 줄기 곡선 항목을 재사용하고, 같은 단어를 인물의 헤어스타일에 강제 연결하지 않는다. [V&A — The Whiplash](https://www.vam.ac.uk/articles/the-whiplash/)

린파의 금빛 배경과 식물 모티프에서 차용할 수 있는 것은 배경 평면의 장식·여백이다. **패널에 그려진 가지**와 **촬영 공간의 실제 가지**를 구분해 소유·깊이·초점 계약을 다르게 작성한다. 사진 전체가 회화가 되거나 인물의 문화·시대 설정이 바뀌는 것은 별도 요청이다. [The Met — Rinpa Painting Style](https://www.metmuseum.org/essays/rinpa-painting-style)

벨베데레의 《유디트》에는 금박 매체와 반쯤 감긴 눈·살짝 벌어진 입술이 함께 등장한다. 이는 원형과 접점이 있는 참고 사례다. 작품의 서사·시선 해석·폭력·노출을 자동 차용하거나 원본의 영감이었다고 단정할 근거는 없다. [Belvedere — Judith](https://sammlung.belvedere.at/objects/3492/judith)

### 3.2. 낮은 눈꺼풀은 감정·시선·머리 각도와 별도 축

이번 원형에는 고요한 낮은 윗눈꺼풀, 카메라 밖 위쪽 시선, 이완된 눈썹과 작은 입술 간격이 결합된다. 그러나 `half-lidded` 하나는 위협·졸음·피곤함·유혹 중 어느 것도 반드시 뜻하지 않는다. 기존 위협적·졸린 후보를 지우지 않고, **윗눈꺼풀이 홍채를 일부 덮고 나머지 얼굴이 이완된 관찰형 sibling**을 제안한다.

`hooded`의 덮이는 피부 형태와 일시적인 눈꺼풀 낮춤도 구분한다. 머리의 yaw/pitch/roll, 몸통 회전, 실제 눈의 방향을 하나의 `three-quarter` 태그로 합치지 않는다. 이 구체 분해는 원본 요청에 대한 연구자의 설계이며 눈 형태로 나이·민족·건강·실제 감정을 판정하는 규칙이 아니다.

### 3.3. 검은 의상 안에서도 조직·주름·광택·층이 다르다

검은 레이스는 열린 망과 꽃 모티프, 튈은 미세 셀, 오간자형은 빳빳한 주름, 시폰형은 유동 주름이라는 서로 다른 관찰 근거를 가진다. 소재 이름 하나로 피부 노출을 추가하지 않고, 원단 외피와 사용자가 정한 안감의 순서를 유지한다. 섬유 종류는 보이는 표면만으로 인증하지 않는다. [LACMA — Lace](https://unframed.lacma.org/2008/10/23/design-dispatch-exploring-lace), [TRC — Tulle](https://www.trc-leiden.nl/trc-needles/materials/woven-and-interlocking-materials/tulle), [Getty — Organza](https://www.getty.edu/vow/AATFullDisplay?find=&logic=&note=&subjectid=300310123), [MFA — Chiffon](https://cameo.mfa.org/wiki/Chiffon)

상복 자료는 검정이라는 색 외에도 얇은 띠·플리츠·내부 지지와 표면의 대비를 보여준다. 현대 고딕 화보에 선택적으로 차용할 수 있지만 모든 빅토리안·에드워드 의상, 애도 단계, 실제 애도 상태를 같은 것으로 만들지 않는다. [The Met — Mourning Dress 1902–4](https://www.metmuseum.org/art/collection/search/106342)

### 3.4. 금박·금속 기재·모자이크·광원은 다른 소유자

금박은 기재 위의 얇은 표면층이고, 금빛 모자이크는 개별 조각의 경계가 있는 구조다. 황동·청동·은의 기재와 도금·파티나도 별개다. `golden`은 이 중 어느 것인지 요청에서 정해야 한다. 소재색·반사·자체 발광을 하나의 정의로 합치면 원본의 금박 패널이나 좁은 광원이 사라질 수 있다. [V&A — Metalworking](https://www.vam.ac.uk/articles/metalworking-techniques), [French Ministry of Culture — Tesserae](https://archeologie.culture.gouv.fr/mosquee-omeyyades/en/making-tesserae), [CCI — Metal Objects](https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/metal-objects.html)

### 3.5. 꽃 색보다 줄기·꽃 크기·잎·상태가 더 구체적이다

매화의 잎 적은 목질 가지, 동백의 광택 잎과 큰 꽃, 목련의 비교적 큰 꽃 형태는 같은 흰 꽃으로 취급하기 어렵다. `near-black rose`는 조명 아래 남는 짙은 붉은색·자주색을 가진 변형으로 제안한다. 서리·이슬·마른 상태는 별도 후보이며 어두운 색에서 자동 추론하지 않는다. [Kew — Prunus mume](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:730000-1/general-information), [RHS — Camellia](https://www.rhs.org.uk/plants/2845/camellia-japonica/details), [RHS — Magnolias](https://www.rhs.org.uk/plants/magnolia/growing-guide), [RHS — Black Prince](https://www.rhs.org.uk/plants/47875/rosa-black-prince-hp/details)

안개꽃의 보라색은 특히 일반화하지 않는다. RHS의 특정 종 절화 설명은 흰색이고, Bella Kotak은 현장의 분홍·보라 꽃을 기록했다. 둘의 관찰 범위가 다르므로 모든 보라색 안개꽃이 자연색 또는 염색이라는 규칙을 만들지 않는다. [RHS — Cut Flowers](https://www.rhs.org.uk/plants/for-places/cut-flowers-growing), [Bella Kotak — Moon Kisses](https://www.bellakotakphotography.com/blog/moon-kisses)

### 3.6. 중앙 세로광의 정체성은 가림·정렬·받는 표면의 관계다

화면에 보이는 좁은 배경 발광 틈과 길쭉한 광원 장비의 모양, 인물 윤곽에 나타나는 림은 별개의 속성이다. 인물 뒤에 있는 슬릿은 겹치는 부분에서 인물에 가려져야 한다. 슬릿이 얼굴 위로 관통하는 선으로 구현되면 실패다. 축 정렬만으로 머리·목·턱 전체에 균일한 림이 생긴다고 요구하지 않는다.

후방 윤곽광, 얼굴의 부드러운 보조광, 배경 조명은 각각 받는 표면을 지정한다. 원본의 금박 패널이 반사면인지 발광면인지도 먼저 선택한다. 여기의 슬릿 구성은 원본 요청을 구체화한 설계이며 제조사 자료가 해당 초상의 성공을 보장하는 것은 아니다. [ARRI Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf), [Aputure Spotlight](https://help.aputure.com/en/spotlight-max-operating-instructions), [broncolor Portrait Case](https://broncolor.swiss/news/how-to-create-water-reflections-for-portrait-photography)

### 3.7. 부드러운 광원·광학 확산·초점 흐림·블룸·톤을 분리한다

확산 필터마다 연화·대비 감소·번짐의 조합이 다르며 할레이션이 없는 연화도 있다. 그러므로 모든 `diffusion`에 광륜을 의무화하지 않는다. 부드러운 얼굴 그림자 경계, 선택 초점면의 읽힘, 밝은 경계 주변 번짐, 영상 톤의 롤오프, 실제 공간 안개는 각기 다른 증거다. [Tiffen Diffusion Guide](https://tiffen.com/pages/diffusion-guide), [Tiffen — Hazed and Confused](https://tiffen.com/blogs/imagemaker/hazed-confused)

`lifted blacks`는 물리적인 검은 옷이 회색 천으로 바뀌는 것과 다르다. 출력 영상의 어두운 톤과 세부 보존을 대상으로 삼는다. 로우키의 장면 밝기 분포·중간톤 대비·채도·검정 바닥을 독립 축으로 다룬다. 피부는 매트하면서 배경 금속은 선택적인 반사를 가질 수 있다. [Adobe Lightroom — Tone and Color](https://helpx.adobe.com/lightroom-classic/desktop/process-and-develop-photos/image-tone-color.html)

## 4. 18개 범주의 보강 계획

| 원 대화 범주 | 회수 | 연구 카드 | 구체 반영 방향 |
|---|---:|---|---|
| 01 장르·미술 방향 | 20 | EG01/03–06/29 | 양식 라벨은 문맥. 회화 모티프·프레임 곡선의 실제 소유자만 좁혀 선택 |
| 02 감정·정서 | 20 | EG02/70 | 이완된 얼굴·정돈된 자세·정적 공간의 조합. 실제 내면·눈물·병리 자동 추론 없음 |
| 03 시선·표정·자세 | 20 | EG07–12 | 눈꺼풀 덮임·눈 방향·머리 축·입술 간격 분리. hooded는 별도 확인 |
| 04 구도·촬영 언어 | 20 | EG13–17 | 중앙 흉상·가지 아치·좌우 여백·비대칭·초점 평면 |
| 05 헤어·머리 장식 | 20 | EG18–22 | 목덜미 번·앞머리 높이·머리 가닥·리본 부착·윤기 상태 |
| 06 피부·메이크업 | 20 | EG23–26 | 피부 국소 질감·빛 반사·화장 범위·입술 마감. 색 이름으로 피부 설정 변경 없음 |
| 07 의상 실루엣 | 20 | EG27–31 | 칼라 부착·하층·어깨 코르사주·천 장미. 긴 드레스/트레인은 현재 흉상으로 검증 불가 |
| 08 원단·표면 | 20 | EG32–40 | 레이스/튈/미세 주름/오간자/시폰/크레이프/실크 골/벨벳/자수 분리 |
| 09 꽃·식물 | 20 | EG41–48 | 가지 부착·잎·꽃 크기·꽃열·서리/이슬/마른 상태. 품종의 정확한 수량은 추가 확인 |
| 10 장신구·장식 | 20 | EG49–52 | 선재 틈·구슬·부조·기재/표면. 기존 장식 변형을 더 검토한 뒤 채택 |
| 11 금박·앤티크 표면 | 20 | EG53–56 | 반사층·타일 경계·표면 손실·금속 가지 |
| 12 배경·공간 | 20 | EG57–59 | 어두운 배경·얕은 벽감·경계 있는 거울. 개별 온실/회랑은 기존 공간 데이터와 대조 |
| 13 광원 위치·방향 | 20 | EG60–64 | 중앙 틈·가림·후방 윤곽·정면 보조·색 역할. 장비 형태는 별도 |
| 14 빛의 질·광학 | 20 | EG17/24/65–66 | 초점·그림자 경계·확산·광륜·반사·톤 전이 구분 |
| 15 색 이름 | 20 | EG52/69 | 고정 HEX나 금속 인증 대신 기존 소유자별 지역색·반사·광원색 |
| 16 색 조합 | 20 | EG69 + 팔레트 20안 | 주요 장·보조 표면/광원·작은 포인트의 역할 제안. 빈도 순위나 고정 면적 비율 없음 |
| 17 톤·그레인 | 20 | EG65–68 | 기존 효과 재사용. 물체 표면과 영상면의 차이를 검증 |
| 18 공기감·상징 연출 | 10 | EG03/48/70 | 실제 공간 입자·꽃잎 상태·상징적 정적 분리. 마지막 10개는 미회수 |

이 표와 키워드 파일의 연결은 **검토 목적지**이며 모든 구문의 정확한 의미가 이미 해결됐다는 표시가 아니다. floor-length gown, train, burnout velvet, 특정 장신구·식물 품종, 개별 공간 등은 그 변형의 범위·기존 항목·출처를 더 좁혀야 한다. 전체 360개를 동일 수의 필수 프로파일로 만드는 목표를 두지 않는다.

## 5. 후보 데이터를 어떤 형태로 강화할 것인가

70개 카드는 문맥·정의·관찰 관계를 정리한 연구 단위다. 운영 프로파일 수와 같지 않다. 처리 분류는 다음과 같다.

| 처리 | 카드 수 | 판단 |
|---|---:|---|
| 기존 의미 재사용 | 16 | 새 동의 프로파일을 만들지 않고 기존 후보·프로필 연결을 활용 |
| 기존 항목 보강 | 6 | 의미·ID를 유지하며 빠진 위치·범위·대조 표현을 추가 검토 |
| 새 좁은 변형 | 31 | 다른 형태·소유·관계를 가진 sibling으로 작성 |
| 문맥 전용 | 5 | 장르·정서·역사 차용. hard obligation으로 승격하지 않음 |
| 도메인 추가 검토 | 11 | 기존 머리/화장/장신구/공간 자료를 더 좁게 비교 |
| 출처 본문 확인 후 채택 | 1 | 은방울꽃 계열 제한 근거 보존 |

[의미 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/SEMANTIC-CARDS.md)는 관찰 요소·소유자·방향 관계·반례·기존 ID·출처·픽셀 판정을 담는다. [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/CANDIDATE-DRAFTS.json)은 **39개**이며 새 변형 33개, 보강 6개다. 꽃잎의 서리·이슬·건조 상태는 한 후보의 OR 조건으로 합치지 않고 세 후보로 분리했다. [조합 8안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/BUNDLE-DRAFTS.json)은 서로 독립적으로 선택하는 작은 묶음이다. [팔레트 역할 20안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/PALETTE-ROLE-DRAFTS.json)은 기존 색 소유자를 배정하는 제안이다.

모든 JSON은 연구 스키마다. `is_runtime_record=false` 또는 `PROPOSED_NOT_INTEGRATED`를 유지하며 운영 assets에 직접 복사하지 않는다. 가중치·rank·특정 광원 비율·카메라 거리·정확한 mm·HEX·API 모델을 새 후보의 기본값으로 만들지 않았다. 좁은 후보를 채택할 때만 해당 구성요소 전체를 같은 소유자에 구현한다.

예를 들어 중앙 슬릿의 새 후보는 다음 의미다.

> A narrow vertically extended luminous aperture lies behind the subject. The subject occludes the aperture where their silhouettes overlap; visible segments belong to the same aligned opening.

이는 연구자가 작성한 문구다. 일반 rim 후보나 전체 금빛 배경은 이 관계의 대체 증거가 아니다.

## 6. 원본 프롬프트의 충돌과 미확정점

| 원본 조합 | 아직 해결되지 않은 점 | 반영 전에 할 일 |
|---|---|---|
| 스튜디오 초상·조명 / negative `studio lighting` | 문자 그대로는 요구·금지 충돌 | 무엇을 배제하려는지 원 요청에서 해결. 자동 삭제·완화를 하지 않음 |
| shadowless fill / negative flat even skin lighting | 그림자 경계의 부드러움과 얼굴 전체 평면화가 섞임 | 선택 광원의 방향과 남길 얼굴 입체감을 명시 |
| `5500K-3200K` warm backlight | 한 광원 범위인지 복수 광원인지, white balance 기준 미정 | 색 역할·광원 수를 먼저 선언하고 불필요한 수치를 기본 후보에서 제거 |
| 85mm / 1.3m / 4:5 / mid-chest | 센서·크롭·거리 기준점과 인체 포함 범위 미정 | 불가능·적합을 단정하지 않고 구도와 촬영 설정을 분리 |
| 패널 0.2m / 가지 0.3–0.8m | 거리 기준점·앞뒤 방향·가림 경로 미정 | camera → subject → panel/source와 가지 평면을 선언 |
| 중앙 틈이 인물 뒤 / 빛선이 중앙에 보여야 함 | 피사체의 가림 때문에 연속선 가시성 보장 안 됨 | 실제 보일 상하 구간·틈 경계·림 받는 위치를 각각 판정 |
| 얕은 심도 / foreground lace sharp / 얼굴 선명 | 레이스와 눈의 평면이 다르면 동시에 선명함을 보장 못 함 | 선택 초점면과 거리·조리개·원본 판정 기준을 지정 |
| pitch black / lifted faded blacks | 물체 지역색과 출력 검정 톤이 섞임 | 검은 옷과 출력 톤 바닥을 별도 소유자에 귀속 |

85mm라는 이름으로 특정 구도를 자동 보장하지 않는다. [Nikon — Focal Length](https://www.nikon.co.uk/en_GB/learn-and-explore/magazine/tips-and-tricks/what-is-focal-length-in-photography-a-guide-for-beginners)

이 충돌을 해결하는 것은 데이터 조사와 별도의 요청별 해석 작업이다. 대체 숫자·네거티브를 조용히 바꾸지 않고, 실제 생성 작업에서 고정 요청·코어를 작성하기 전에 정리한다.

## 7. 실행 가능한 반영 순서와 완료 판정

[상세 반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/IMPLEMENTATION-PLAN.md)은 기준 원본 확인 → 재사용/변형 확정 → 저작 데이터 → 파생 인덱스 → 실제 후보팩 → 원본 픽셀 검증 순서로 구성했다. 코어를 고정하기 전에 데이터·후보팩을 읽고 원래 요청을 바꾸는 절차를 추가하지 않는다.

현재 코드의 순서는 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → visual obligations/concept candidates/clarification → 요청별 불변 v6 팩이다. 연구 자료를 후보팩과 동일하게 보거나 데이터의 관계를 런타임에서 이미 채택된 요구로 간주하지 않는다. [현재 생성 코드](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:10176)

[검증 설계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/EVALUATION-PLAN.json)은 언어 2개와 반례/통제 1개를 가진 30그룹, 총 90개 사례를 제안한다. 렌더링은 6개 경계 그룹의 초기 탐색 비교만 설계했다. 최대 12회라는 숫자는 미래 탐색 한도의 제안이며 이번에 실행하거나 비용을 승인한 것은 아니다. 변형의 의미가 달라지면 각 변형의 요청·코어를 따로 고정한다. 같은 코어라고 주장한 채 최종 프롬프트만 바꾸지 않는다.

새 데이터 효과를 주장하려면 실제 후보 노출, 채택, 추가·변경된 문구, 기존 코어의 보존과 원본 픽셀의 해당 요소를 연결해야 한다. 후보를 채택하지 않았거나 기본 프롬프트에 같은 요소가 이미 있었던 성공은 새 데이터의 기여로 계산하지 않는다. 탐색 비교 몇 장으로 일반적인 품질 향상이나 사용자 수용을 주장하지 않는다.

## 8. 이번에 실제 검증한 것

[연구 검증 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/VALIDATION.json)은 23개 확인을 기록한다. 22개는 PASS이며, 소스·ID 참조·슬롯·키워드 보존·연구 상태·컴파일러 투영과 보호 파일 해시를 포함한다.

**시작 시점의 운영 소스·스크립트 133개와 인덱스 매니페스트 2개는 동일했다.** 표정·금박 패널·슬릿 연구 프로토타입 3개에서 현재 `authored_components/v1` 컴파일러가 증거 필드와 렌더 기준을 투영하는 것을 확인했다. [프로토타입과 투영 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/ethereal-gothic-research-20261007/PROFILE-PROTOTYPES.json)

Git 상태의 완전 동일 비교 한 건은 FAIL이다. 조사 중 다른 작업 폴더에 `color-palette-main-merge-20261007/PRIMARY-BEFORE.json`, `data-quality-links-20261007/PRIMARY-BEFORE.json` 두 파일이 추가됐다. 기존 상태의 삭제·해시 변화는 관찰되지 않았지만 이 실패를 PASS로 덮어쓰지 않았다. 추가 파일은 이 연구에서 만들거나 수정한 산출물이 아니다.

운영 사전/인덱스 검사, 임베딩, 실제 후보팩 실행, 프롬프트 감사, 이미지 생성, 원본 픽셀 판정, 커밋·푸시는 미실행이다. 현재 완료된 제품은 출처와 검토 가능한 데이터 초안이 포함된 리서치 및 반영 계획이다.

# 수영복·인접 의복의 시각 의미와 후보팩 보강 리서치

작성: 2026-09-09 · 상태: **proposed / research only**

핵심 제안은 수영복 명칭을 대량으로 동의어 등록하는 것이 아니라 **의복의 연결 구조 → 부위별 절개와 끈 경로 → 표면·레이어 → 선택적 장면**으로 분해해 후보를 구성하는 것이다. 형태가 비슷한 의복과 겹치는 판매 용어가 많아, 명칭만 늘리면 회수율은 높아져도 서로 다른 구조를 같은 이미지로 만드는 문제가 남는다.

이번 결과는 82개 의미 설계 항목, 37개 재조합 후보 초안, 24개 선택형 묶음, 22개 대조 검증쌍이다. **82개 모두를 hard profile로 만들자는 제안이 아니다.** 기능 명세, 내부 구조, 모호한 판매 용어, 시대·무드는 서로 다른 처리 경로로 나눴다. 실제 런타임 데이터와 인덱스는 수정하지 않았고, 이미지 생성 또는 픽셀 검증도 수행하지 않았다.

## 1. 입력과 근거의 범위

참조 대화 **수영복 관련어 조사**의 전체 응답을 `read_thread`로 확인하고 [원문](referenced-conversation.md)에 보존했다. 그 대화는 21개 절의 키워드 목록과 조합 예시를 제공한다. 그 안의 이전 검색 citation 토큰은 현재 확인 가능한 출처로 간주하지 않았으며, 이번 조사에서 제조사·제작자·박물관·원 논문을 다시 확인했다.

- [sources.json](sources.json): 21개 출처의 URL, 열람 수준, 지지 범위와 한계. 검색 발췌만 확인한 자료와 본문을 연 자료를 구분했다. V&A 본문은 403으로 열리지 않아 후속 경로로만 남겼다.
- [keyword-matrix.md](keyword-matrix.md), [keyword-matrix.json](keyword-matrix.json): 용어를 관찰 가능한 축으로 변환한 82개 설계 단위.
- [candidate-drafts.json](candidate-drafts.json): 현재 스키마에 직접 로드하지 않는 후보·묶음 제안.
- [local-coverage.json](local-coverage.json): 현재 소스 파일 해시와 어휘 조사 결과.
- [verification-plan.json](verification-plan.json): 구현 후 확인할 대조쌍, 대조군과 중단 기준.

출처의 상품명·설명 확인과 실제 상품 이미지의 픽셀 관찰은 다르다. **이번에는 상품 사진과 소장품 이미지의 픽셀을 직접 판독하지 않았다.** 따라서 표의 구체적인 렌더 게이트는 출처 용어에 기초한 설계 가설이다. 원문의 모든 세부 키워드를 독립 출처로 검증했다고 주장하지 않는다. 복합어는 구성 축으로 분해했고, 세부 근거가 필요한 항목은 아래 P2와 보류 목록에 남겼다.

## 2. 현재 저장소에서 확인한 부족분과 재사용 지점

기준 커밋은 `b6e70b787c083bbd9c472488875a028d28fbd2a8`이다. 조사 시작 시 작업 트리는 깨끗했다. 생성 인덱스를 제외한 최상위 소스 JSON 38개에서 `id/ko/en/aliases/activation` 필드의 수영복 관련 어휘를 조사했다. 3개 파일에서 일치가 나왔지만 **문자열 출현과 전용 수영복 지원은 다르다**.

| 현재 지점 | 확인된 내용 | 보강 방향 |
|---|---|---|
| `photo_prompt_tags.json` | `pool_deck_swimwear_editorial`, `pool_deck_swim_editorial` | 장면·스타일 단서는 있으나 상의/하의/끈/절개 구조를 대신하지 못함 |
| 같은 파일 | `high_rise_waist_navel_relation` | 기존 허리선 관계 재사용 검토. 수영복 후보가 같은 의미를 새 ID로 중복 소유하지 않게 함 |
| `photo_prompt_visual_obligations.json` | `one_piece_dress_construction`이 원피스 수영복을 배제 | 기존 드레스 분기 유지하며 별도의 수영복 문맥 처리 |
| 같은 파일 | `wearable_protective_armor_system`, `commercial_appeal_revealing_armor` | bikini armor는 일반 비키니와 다른 문맥. 수영복 검색으로 갑옷을 잘못 활성화하면 안 됨 |
| 같은 파일 | `racerback_sports_bra_strap_convergence` | Y형 스포츠브라 변형은 재사용 가능한 구조 근거지만 모든 수영복 racerback에 그대로 강제하지 않음 |
| 같은 파일 | `sheer_garment_optical_layering` | 메시·레이스 겉층/안감 관계의 공통 모델 재사용 검토 |
| 같은 파일 | `active_skort_outer_skirt_inner_shorts` | 레이어 경계 평가 방법은 참고. 스윔드레스에 반드시 쇼츠가 있다고 전용하면 오류 |
| 로더·컴파일러 | visual extension 목록과 candidate extension 목록이 명시적으로 등록됨 | 파일 하나를 추가하는 것만으로 런타임이 바뀌지 않음 |

핵심 누락은 **수영복 가족별 연결 구조, 앞·뒤 절개의 독립성, 허리선/다리선/후면 폭의 독립성, 변형을 유지하는 후보 묶음**이다. 기존 범용 의복·레이어 의미는 일부 존재하므로 “수영복 관련 데이터가 전무하다”는 결론은 부정확하다. 어휘 조사에서 잡히지 않는 공통 의미도 별도로 소스에서 확인했다.

## 3. 원문에서 바로잡아야 할 의미 경계

### 3.1 High-rise, high-leg, rear coverage는 세 축이다

`high-waisted/high-rise`는 하의 윗선, `high-leg/high-cut`는 다리 구멍의 옆쪽 높이, `coverage`는 후면 패널이 덮는 범위다. Seafolly는 Brazilian 계열 안에서도 high-waisted, hipster, tie-side, V-cut을 구분한다. 따라서 높은 허리선에서 자동으로 높은 다리선 또는 좁은 후면 패널을 도출해서는 안 된다. [Seafolly의 실제 분류](https://us.seafolly.com/blogs/sf-world/dare-to-bare-the-brazilian-bikini-cut)

원문의 `Full → Classic → Moderate → Cheeky → Brazilian → Thong`은 보편적 표준 순서로 등록하지 않는다. 같은 브랜드도 Brazilian을 cheeky라는 말로 설명한다. 대신 요청 명칭을 보존하고, 선택된 후면 참조의 패널 경계와 상대 폭을 기록한다. 수치 기준을 만들려면 다양한 제품·체형·포즈를 포함한 별도 캘리브레이션이 필요하다. **브라질리언이라는 의복명으로 착용자 국적을 추론하지 않는다.**

### 3.2 Bandeau는 strapless와 동의어가 아니다

반두의 전면 밴드 모양과 지지끈 경로를 분리한다. 실제 상품명에 `Bandeau Halter`가 함께 쓰인다. 명시적인 strapless 요청에만 목·어깨 지지끈 없는 변형을 적용한다. 이 경계는 단순 명칭 확장이 오히려 이미지를 잘못 제한할 수 있는 직접적인 사례다. [Seafolly Lotus Bandeau Halter](https://us.seafolly.com/products/lotus-bandeau-halter-bikini-top-j40759-teal)

### 3.3 Triangle, string, halter도 서로 대체하지 않는다

Triangle은 패널 형태, string은 끈의 폭/연결, halter는 목 뒤 경로다. 삼각 상의에 넓은 끈도 가능하며, 홀터가 반드시 삼각 패널을 뜻하지 않는다. 후보는 `top_shape`, `strap_width`, `strap_path`를 별도 선택한다. 제조사 카탈로그는 이 용어들을 함께 사용하지만, 제안한 독립 필드는 이번 리서치의 설계 추론이다. [Seafolly 상의 카탈로그](https://us.seafolly.com/collections/bikini-tops)

### 3.4 Racerback와 crossback은 끝점과 연결 방식을 읽는다

등판 중앙으로 모이는 패널/요크와 두 끈이 교차하는 X 경로를 구분한다. `open back`은 더 넓은 개념이라 반드시 특정한 끈 경로를 의미하지 않는다. `V-back`도 V 모양 개구부인지 끈 배열인지 선택해야 한다. Speedo의 Medalist·Muscleback·Leaderback·Powerback 같은 상품군 이름은 보편적 위상 ID로 대체하지 않고 원래 브랜드 문맥을 보존한다. [Speedo 등판 가이드](https://speedo.com.au/explore-swimwear-guides/blog-find-your-fit.html)

정면에서 뒤 경로가 안 보이면 뒤 게이트 PASS를 줄 수 없다. 그렇다고 모든 수영복 사진을 뒷모습으로 바꾸지도 않는다. **요청한 구조를 증명할 프레임인가**를 별도로 판단해야 한다.

### 3.5 Tankini와 one-piece의 구분은 복부 노출량이 아니다

긴 상의가 하의를 덮는 탱키니에서는 피부 틈이 없어도 두 벌일 수 있다. 구분점은 독립적인 상의 밑단과 하의 경계다. 스윔드레스, 스커트형 하의, 별도 랩도 각각 본체와 연결된 치마 / 별도 하의의 치마 / 독립 천 레이어로 나눈다. REI의 스타일 분류를 참고하되 이 밑단 게이트는 이미지 평가를 위한 제안이다. [REI 수영복 가이드](https://www.rei.com/learn/expert-advice/swimsuits.html)

### 3.6 Wetsuit은 검은 밀착 의복이나 neoprene이라는 단어만으로 정의하지 않는다

팔다리 길이, 패널, 입구 경로를 지정하고 소재·두께·보온 기능은 명세로 둔다. 현행 Rip Curl 가이드는 neoprene 대체 소재도 소개한다. 모든 wetsuit의 화학 조성을 neoprene으로 단정하는 규칙은 부적절하다. Springsuit도 팔과 다리 길이를 각각 지정하며, Long Jane의 민소매·긴다리 조합을 일반화 가능한 반례로 삼는다. [Rip Curl 여성 가이드](https://www.ripcurl.com/pages/womens-wetsuit-guide), [Long Jane 용례](https://www.ripcurl.com.au/blogs/products/the-best-wetsuits-for-spring)

Swimskin은 얇은 경기용 레이어의 용어이며 wetsuit과 동의어가 아니다. `dive skin`까지 자동 병합하지 않는다. 실제 사용 적합성이나 경기 규칙은 이번 시각 의미 조사의 범위 밖이며, 이미지만으로 판정하지 않는다. [Blueseventy의 구분](https://www.blueseventy.com/blogs/updates/what-is-a-swimskin-and-how-is-it-different-from-a-wetsuit)

### 3.7 소재·표면·봉제 주름은 서로 다른 발생 원인이다

`nylon/polyamide`, `polyester`, `elastane/spandex`는 섬유 명세이며 `ribbed`, `crinkle`, `terry`는 표면/조직 명칭이다. 같은 섬유를 서로 다른 표면으로 만들 수 있으므로 섬유명에서 광택을 고정하지 않는다. `Lycra` 같은 상표 표기는 일반 섬유명과 별도 보존하고, 정확한 상표·혼용률 주장은 상품 명세가 있을 때만 사용한다.

Ruching은 특정 지점으로 모이는 주름, elastic shirring은 반복 봉제열 사이의 잔주름, smocking은 장식 스티치와 주름 연결로 구분하는 설계가 유용하다. 이 중 shirring/smocking의 제작 차이는 제작자가 직접 설명한다. 크링클 전체 표면을 셔링의 대체 증거로 삼지 않는다. [Seamwork 제작 설명](https://www.seamwork.com/sewing-tutorials/a-guide-to-elastic-shirring)

Hunza G의 Original Crinkle은 특정 브랜드의 소재 체계다. 이를 seersucker·rib·smocking과 하나의 동의어 집합으로 합치지 않는다. 다만 이번에는 조직 확대사진과 섬유 사전의 개별 항목을 확인하지 않았으므로 rib/crinkle/seersucker/terry/jacquard의 세부 자동 판정은 P2로 둔다. [Hunza G](https://www.hunzag.com/pages/care-instructions)

### 3.8 Crochet/mesh와 cut-out의 차이는 뒤층이다

열린 컷아웃에는 해당 위치를 메우는 천이 없고, 메시에는 구멍 조직이 있으며, 크로셰/레이스에는 실 무늬의 겉층이 있을 수 있다. 안감이 있는지 따로 정해야 한다. “크로셰=물에 들어갈 수 없음”, “메시=속이 전부 보임”을 규칙으로 만들지 않는다. 실제 수영복 제작에도 겉감과 안감이 분리된 구조가 있다. [Mood Naxos 제작 사례](https://blog.moodfabrics.com/naxos-swim-suit-free-sewing-pattern/)

### 3.9 역사·유행은 소장품과 선택형 스타일로 분리한다

원문의 시대별 목록은 영감용 출발점이다. 1920년대 전체를 sailor collar·bloomers·stockings로 고정하지 않는다. The Met에는 1920년대 wool 수영복의 개별 소장 기록이 있다. 시대 데이터는 소장품 ID와 연대·구조·소재를 묶어야 하며 한 사례에서 전체 시대의 복식을 일반화하지 않는다. [The Met 1979.124.4](https://www.metmuseum.org/art/collection/search/91762)

`monokini`는 원문에 없지만 이번 확장에서 중요한 다의어다. The Met의 1964 Gernreich 설명과 현대 ROXY의 cut-out sides 용례는 같은 시각 형태로 합칠 수 없다. 현대 모노키니 상품 요청에 역사적 형태를 자동 넣지 않는다. [The Met 1964](https://www.metmuseum.org/art/collection/search/81814), [ROXY 현대 용례](https://www.roxy.com/blogs/expert-guides/swimsuits-for-rectangle-body-shape?page=2)

`French Riviera`, `quiet luxury`, `Y2K`, `mermaidcore`는 국적·부·실제 연대·신체 조건을 뜻하는 hard profile이 아니다. 색과 패턴, 구조, 소품, 공간을 선택하는 옵션으로 남긴다. `kimono cover-up` 같은 소매업 용어만으로 전통 기모노의 구조나 착용자 정체성을 부여하지 않는다. sarong/pareo의 정확한 문화·기원 구분은 별도 소장품 근거를 확보하기 전 보류한다.

## 4. 제안하는 데이터 단위

의복 범주·부품·국소 속성의 분리는 Fashionpedia의 의류 온톨로지 설계와 방향이 맞는다. 하지만 해당 데이터셋을 수영복 용어 전체의 정답 사전으로 쓰지는 않는다. 아래 필드는 이 프로젝트에 적용하기 위한 제안이다. [Fashionpedia 원 논문](https://arxiv.org/abs/2004.12276)

| 층 | 저장할 값 | 시각 게이트 여부 |
|---|---|---|
| 의복 객체 | family, garment_count, 연결 패널, 독립 밑단 | 연결부가 보여야 판정 가능 |
| 부위 | neckline, strap endpoints/path, back opening, sleeves | 요청된 부위만 해당 시점에서 판정 |
| 하의 | waist height, waist shape, leg opening, leg length, rear panel coverage | 서로 독립; 후면은 후면 증거 필요 |
| 국소 구조 | seam, closure, ring attachments, knot, overlap, cut-out boundary | native 규모에서 물리 연결 확인 |
| 광학/텍스타일 | surface topography, finish, pattern, lining, wet state | 원료나 성능 판정과 분리 |
| 내부/성능 | pads, wire, lining count, UPF, drying, resistance | 명세/내부 제품컷; 일반 착용샷에서는 비채점 |
| 스타일/장면 | era inspiration, color, motif, accessory, location | 요청하지 않으면 선택적이며 의복 정의를 바꾸지 않음 |

각 행의 최소 요건은 **소유 의복 → 특정 부위 → 실제 연결/경계 → 혼동 대안 → 보이는 시점 → 출처와 한계**다. 이름 하나를 여러 표현으로 바꿔 쌓는 방식은 보강으로 세지 않는다.

`wearer_left/right`와 `image_left/right`도 구분한다. 거울·등 돌림·수중 굴절 때문에 같은 의복의 좌우를 잘못 바꿀 수 있다. 정면/후면/측면의 한 뷰로 판정 불가능한 항목은 `unobservable`로 기록한다. 이 상태는 요청된 필수 구조를 통과시킨다는 뜻이 아니다.

## 5. 충분한 보강을 위한 우선순위

### P0: 종류와 구조의 혼선부터 해결

1. One-piece / bikini / tankini / swimdress / legsuit / rashguard separates / integrated surf suit의 연결 구조.
2. Waist height / leg opening / rear coverage의 독립성.
3. Bandeau와 strapless, triangle과 string, racerback과 crossback의 비동의어 경계.
4. 원피스 드레스·bikini armor·레오타드·스포츠브라의 문맥 누출 방지.
5. 요청되지 않은 체형·노출량·배경을 후보 채택만으로 바꾸지 않는 intent 조건.

이 단계만으로도 “모든 수영복을 같은 검은 원피스나 삼각 비키니로 평탄화하는” 가설적 실패를 검사할 수 있다. 현재 렌더에서 그런 실패가 발생했다고 확인한 것은 아니다.

### P1: 부품과 레이어로 변형을 유지

Neckline, back opening, sleeve/leg length, tie/lace/zip closure, wrap/twist/ring, skirt/wrap layer를 추가한다. P0의 의복 연결과 서로 충돌하지 않아야 한다. `ring`은 물체 존재뿐 아니라 어떤 두 패널을 연결하는지, `wrap`은 대각선 무늬가 아닌 겹침 경계가 있는지 검사한다.

### P2: 확대 관찰이 필요한 표면과 비표준 판매명

Rib/crinkle/seersucker/terry/jacquard, piping/binding, balconette/demi/bralette, coverage 세부 라벨은 참조 이미지와 제조/패턴 근거를 더 확보한 뒤 승격한다. 현재 draft에는 필요 위치를 표현했지만 용어별 엄격 판별이 성립한다고 보지 않는다.

### P3: 역사·무드·소품 확장

원문의 시대별 목록과 리조트/서핑/로맨틱/미래 분위기는 선택형 묶음으로 확장한다. 배경·소품은 별도의 열린 차원일 때만 제안한다. 수영복 종류가 아직 흐려지는 단계에서 호텔·요트·선글라스를 늘리는 것은 핵심 데이터 개선이 아니다.

## 6. 후보팩의 실제 설계

24개 묶음은 하나의 완성 사진을 강제하는 프리셋이 아니다. 예를 들어 `sw_bundle_highrise_classic`은 높은 허리선만 명확히 하고 다리선·후면 폭을 열어두며, `sw_bundle_convertible_bandeau`는 가로 밴드와 목 뒤 끈이 공존할 수 있음을 제시한다. `sw_bundle_rashguard_separates`와 `sw_bundle_surf_integrated`는 소매가 같아도 다른 의복 수를 보존한다.

| 묶음군 | 제안 수 | 주요 목적 |
|---|---:|---|
| 기본 의복·상의 | 6 | 연속 원피스, 분리 삼각, 홀터 반두, 탱키니, 스윔드레스, 롱라인 |
| 하의·등판 | 6 | 높은 허리선, high-leg+low-back, X등판, 중앙 등판, boyleg, 측면 매듭 |
| 수상 스포츠 | 4 | 래시가드 분리형, 서프 일체형, Jane, swimskin |
| 레이어·표면·세부 | 8 | 랩, 안감 크로셰, 링 컷아웃, 루싱, 셔링, 골지, 젖은 매트, 비대칭 랩 |

**후보 채택은 프로파일 활성화 근거가 아니다.** 먼저 사용자 문맥에서 의미를 정하고, 이미 잠긴 차원은 후보가 덮어쓰지 않게 한다. BM25F/embedding hit는 발견을 돕는 advisory 신호로만 취급한다. 명시된 형태와 부품 관계가 요청에 있거나 독립적으로 확정된 경우에만 해당 의무를 적용한다.

후보 초안의 `proposed_slot=wardrobe_style`은 객체 단위 조사 편의상 임시 값이다. 구현 시 기존 `wardrobe_style`, `garment_detail`, `silhouette_proportion`, `texture` 중 의미 소유권이 맞는 슬롯으로 옮겨야 한다. 특히 기존 `high_rise_waist_navel_relation`은 재사용 여부를 먼저 결정한다. 세부 질감이 배경·피부·머리카락으로 번지지 않도록 `owner=selected_swim_garment` 관계를 실제 조합 문장에 보존해야 한다.

한국어 직역문은 구조 검토용 초안이다. 런타임 영어 문장은 짧은 literal relation으로 별도 작성하고, `source_ids/status/review_scale` 등의 관리 메타데이터를 이미지 프롬프트에 유출하지 않는다.

## 7. 후속 구현 시 파일 소유권

이번에는 아래 변경을 수행하지 않았다. 구현을 진행한다면 다음 순서가 적절하다.

1. `assets/photo_prompt_visual_obligations_swimwear.json`을 새 source extension으로 설계하되 기존 공통 계약과 중복되는 행을 먼저 제거한다. `authored_components`에서 match/evidence/instruction/render gate를 함께 소유한다.
2. `assets/photo_prompt_swimwear_extension.json`에 실제 슬롯 후보와 optional `visual_semantics` 묶음을 작성한다. 이번 연구용 JSON은 스키마가 다르므로 그대로 복사해 로드하지 않는다.
3. `scripts/prompt_generator.py`의 visual/candidate extension 등록 목록에 추가한다. `scripts/visual_profile_contracts.py`와 `scripts/photo_candidate_semantics.py`의 기존 컴파일 경로를 사용하며 별도 수영복 키워드 하드코딩은 피한다.
4. 인덱스·태그 등 파생 산출물은 현재 저장소 빌드 경로로 재생성한다. 관리 메타데이터의 소스 해시와 후보 ID 참조를 검사한다.
5. [verification-plan.json](verification-plan.json)의 대조쌍을 행동 테스트로 옮긴다. ID 존재 검사만으로 끝내지 않고 실제 요청에서 wrong activation, negation, axis coupling을 검사한다.

## 8. 비교 실험과 성공 기준

가설은 **의복 연결과 독립 축을 literal candidate로 전달하면, 같은 요청에서 구조 혼동이 줄어든다**이다. 용어 개수·후보팩 크기·테스트 개수 증가는 성공 지표가 아니다.

세 대조군을 사용한다. A는 후보팩 없는 독립 core, B는 기준 커밋 후보팩, C는 변경 후보팩이다. 공통 사용자 요청과 intent lock을 먼저 고정하고 각 군이 다른 군의 후보·최종 프롬프트를 보지 않게 한다. 같은 모델 버전·참조 방식·종횡비·시도 예산을 적용한다. 확률적 생성 개선을 주장하려면 군별 반복을 확보하고 프롬프트를 중간에 고쳐 같은 실험이라고 하지 않는다.

측정은 아래 단계별로 남긴다.

| 단계 | 확인할 증거 | 실패 시 해석 |
|---|---|---|
| 요청 해석 | 명시된 형태·부정·열린 차원 | 의미 입력/활성화 문제 |
| 후보 전달 | 새 ID가 실제 pack에 노출되었는지 | retrieval/pack 문제 |
| 채택 | 새 ID와 어느 literal clause가 채택되었는지 | composer/선택 문제 |
| 렌더 요청 | source intent SHA와 최종 prompt, audit | 전달 계약 문제 |
| 생성 | 이미지 파일/차단/오류 | 미전달이면 unscored |
| 픽셀 | 의복 연결, 특정 부위, 원단·레이어 관계 | 생성 반응/관찰 가능성 문제 |
| 사용자 판단 | 의도한 모습과 다양성이 실제로 좋아졌는지 | 기술 통과와 별도 판단 |

선택한 요청의 필수 구조 게이트는 모두 통과해야 한다. `partial_is_fail`을 유지하고, 안 보이는 뒤 끈을 정면 사진으로 통과시키지 않는다. 반대로 UPF·탈착성처럼 일반 픽셀에서 검증할 수 없는 것은 처음부터 픽셀 게이트로 만들지 않는다. **새 후보 노출/채택이 0이면 이미지가 좋아 보여도 데이터 효과로 결론 내릴 수 없다.**

최소 행동 대조는 22쌍이다. high-rise/high-leg, bandeau/strapless, triangle/string, racerback/X-back, 탱키니/원피스, 부착 치마/랩, cut-out/mesh, rib/stripe, shirring/crinkle, wet/gloss, 앞 지퍼/chest zip, rashguard/surf suit, 팔/다리 길이, metadata, 부정, 드레스·갑옷 다의어를 포함한다. 동의어만 바꾼 같은 사례를 holdout으로 세지 않는다.

중단 기준은 구조 축의 연쇄 변경, 사용자 잠금 침범, 무관한 기존 사례 회귀, 필수 시각 증거 누락이다. 이 중 하나라도 발생하면 최초 실패 단계를 고친다. 후보가 보이지 않는 상황에서 렌더 횟수만 늘리지 않는다.

## 9. 남은 근거 수집과 이번 완료 범위

전체 대화 키워드를 보존하고, 저장소 부족분을 확인하며, 핵심 혼동을 현재 1차 출처로 다시 검토하는 리서치는 완료했다. 기계 판독 초안은 ID 중복·출처 참조·후보 참조·JSON 문법을 검증했다. 이는 런타임 계약 검증이나 이미지 품질 검증을 뜻하지 않는다.

후속 이미지 코퍼스는 우선순위 P0의 혼동쌍마다 서로 다른 제품/브랜드의 정면·후면·측면을 확보하고, 확대가 필요한 P2에는 별도 디테일 사진을 배치하는 방식이 적절하다. 제품 전체 사진만으로 내부 와이어/패드·조직·뒷면 폭을 모두 판정하려 하지 않는다. 라이선스와 출처 URL·제품 ID·촬영 뷰를 기록한 뒤 관찰 가능한 항목만 레이블링한다. 이번에는 이 코퍼스를 수집하거나 픽셀 레이블링하지 않았다.

특히 추가 확인이 필요한 항목은 balconette/demi/bralette의 브랜드 간 차이, seersucker/rib/terry/jacquard 확대 조직, picot/piping/binding 제작 구조, swimdress의 내부 하의 변형, dive skin, 정확한 역사별 소장품, sarong/pareo의 문화별 구분이다. 이들을 근거가 확보된 P0 항목과 같은 신뢰도로 일괄 활성화하면 안 된다.

권장하는 다음 구현 단위는 **P0의 연결 구조·독립 축·다의어 경계부터 적용하고, 22개 행동 대조와 무관한 의복 holdout을 통과시킨 뒤 이미지 비교로 넘어가는 것**이다. P2/P3 확장은 해당 근거와 관찰 범위를 확보한 항목부터 진행한다.

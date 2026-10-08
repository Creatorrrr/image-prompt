# 쇼트컷·보브 보충 리서치 — 연구 초안

기준일: 2026-10-08 Asia/Seoul. 원본 `reference/keyword-inventory.tsv`의 ID와 한·영 표기를 그대로 연결했다. 신규 의미 카드 10개, 직접 열람한 일차 자료 URL 17개, 실행하지 않은 대조 설계 12개다. 같은 브랜드와 체인의 여러 페이지가 있으므로 URL 수를 독립 연구기관 수로 해석하지 않는다.

기존 `specialist-cuts.md`, `cuts-cards.json`, `cuts-sources.json`은 SHA-256이 그대로다. 이 보충의 결과는 새 연구 문서와 JSON 초안 세 파일에 한정한다. 런타임 데이터·코드·검색 인덱스·이미지 생성·기존 후보 ID 매핑을 수행하지 않았다. 출처 이미지의 픽셀과 영상도 검사하지 않았다.

## 직접 자료가 지지하는 핵심 경계

버즈의 고전형은 균일한 초단발에 가깝지만 L’Oréal은 페이드·디스커넥티드·크루 혼합을 함께 명명한다. 따라서 buzz/crew/fade를 전역 상호배타 레이블로 설정하면 직접 용례를 잃는다. 크루의 상부 길이 우세와 두상 윤곽은 Wahl의 직접 설명이 뒷받침하고, 플랫톱은 별도의 수평 deck이다. 높이와 측면 전이는 따로 선택한다. [L’Oréal 버즈 변형](https://www.lorealparisusa.com/beauty-magazine/hair-style/short-hairstyles/buzz-cut-styles-for-men), [Wahl 교육 PDF](https://wahlusa.com/media/wahl-home-haircutting.pdf), [CADMEN 플랫톱](https://academy.cadmen.ca/post/how-to-do-flat-top-haircut).

빅시의 bob/pixie 혼합은 두 브랜드가 일치한다. 길이 기준, curly styling 적합성, intro의 bob/lob 표현은 일치하지 않는다. 사진 한 장에서 grown-out pixie와 layered short bob 사이를 배타 분류하는 대신, 짧은 crown 층과 남긴 외곽을 후보 문구로 명시한다. [John Frieda 빅시](https://www.johnfrieda.com/en-uk/blog/hairstyles/bixie-cuts/), [L’Oréal 빅시](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/what-is-the-bixie-haircut).

투블럭은 조사한 Ash 직접 설명에서 귀 주변 짧은 side와 긴 upper의 연결 단절로 구분된다. 덮은 버전과 노출한 버전이 있으며 뒤의 gradual 刈り上げ와 공존한다. 한국 박준 공식 catalog도 투블럭을 가르마·쉼표·포마드·펌·염색과 분리하여 조합한다. side의 단절과 back의 blend를 같은 부위로 잘못 묶지 않는다. [Ash 練馬](https://nerima.ash-hair.com/posts/10878447/), [Ash 구분 설명](https://tsurugamine1.ash-hair.com/posts/39874753/), [Ash 직접 고객 사례](https://takatsu.ash-hair.com/posts/41758814), [박준 공식 투블럭 catalog](https://parkjun.com/park/bbs/board.php?bo_table=hair&cate=1&wr_1=%EB%82%A8%EC%9E%90&wr_2=%ED%88%AC%EB%B8%94%EB%9F%AD%EC%BB%B7&wr_3=&wr_4=).

프렌치 보브는 short bob contour 위에 fringe·part·layer·curl 변형을 허용한다. 페이지보이는 직접 자료가 중·장발의 smooth inward-curled styling까지 포함하고, modern pageboy는 완전한 outline 정의가 없다. 그래서 페이지보이의 단발·bowl·full fringe 고정 프로필은 hold로 둔다. [French bob 직접 정의](https://www.johnfrieda.com/en-uk/blog/hairstyles/french-bobs/), [Sam Villa 최신 교육 용례](https://www.samvilla.com/blogs/hair-tutorials/the-ultimate-fall-styling-guide-tools-and-techniques-for-seasonal-trends), [L’Oréal Pageboy 용례](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/1940s-hairstyles).

버터플라이는 짧은 face frame와 더 긴 보존 층의 관계를 남긴다. 한 브랜드는 octopus 별칭으로 소개하고 다른 브랜드는 구분하므로 exact alias는 hold이다. technical disconnected vs blended도 copy가 흔들리므로 결과의 층 위치만 의무로 둔다. 하드파트는 natural part와 대비되는 또렷한 exposed channel이며 내부 part path와 외곽 line-up을 분리한다. 도구 종류는 완성 사진의 판정에서 제외한다. [L’Oréal Butterfly](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/butterfly-haircut), [John Frieda Butterfly](https://www.johnfrieda.com/en-uk/blog/hairstyles/butterfly-cuts/), [Alfani 직접 Hard part 설명](https://www.alfanisbarbershop.com/blog/classic-side-part-guide).

## 반영 제안과 증거 수준

문헌 직접 정의·named case와 아래의 운영 정의를 구분했다. 최소사인, directed relation, camera, 양립 제약, 후보 영어, 대조 실험은 저자가 작성한 설계안이며 외부 교육 표준을 복사한 것이 아니다. 이름만으로 성별·연령·인종·국적·성격을 추가하지 않는다. cutting tool이나 시술 history는 영상·행위 증거가 필요하다. 연구 JSON은 runtime schema나 자동 merge manifest가 아니다.

제안 상태: 기존 의미 재사용 검토 5개, 의미·후보 구조 보강 4개, 명칭 자동 프로필 hold 1개. 실제 기존 후보 ID 대조와 중복 제거는 main executor가 수행한다.

| 원본 | 카드 | 보강/보류 중심 |
|---|---|---|
| H066 버즈컷 | `hair-cut-supp-buzz` | semantic_reuse_recommended |
| H067 크루컷 | `hair-cut-supp-crew` | semantic_reuse_recommended |
| H090 플랫톱 | `hair-cut-supp-flat_top` | semantic_reuse_recommended |
| H073 빅시컷 | `hair-cut-supp-bixie` | semantic_strengthening_proposal |
| H077 언더컷 | `hair-cut-supp-undercut` | semantic_reuse_recommended |
| H114 투블럭 | `hair-cut-supp-two_block` | semantic_strengthening_proposal |
| H101 프렌치 보브 | `hair-cut-supp-french_bob` | semantic_strengthening_proposal |
| H104 페이지보이 | `hair-cut-supp-pageboy` | hold_automatic_name_profile |
| H108 버터플라이컷 | `hair-cut-supp-butterfly` | semantic_strengthening_proposal |
| H092 하드 파트 | `hair-cut-supp-hard_part` | semantic_reuse_recommended |

## 카드 상세

### H066 버즈컷 / Buzz cut

`hair-cut-supp-buzz` · `hair.cut.short_family` · research draft

두피 가까이에 매우 짧은 모발을 남기는 커트군이다. 고전형은 대체로 균일하지만 직접 브랜드 용례에는 페이드·디스커넥션·크루 혼합형도 있다.

Owner/region: `subject.hair` → top, sides, back.

관찰 가능한 최소사인: 클래식 선택 시 상부·옆·뒤에 짧은 모발이 남고 길이 차가 작음; 두상 외곽을 따라가는 잔모 실루엣이 읽힘.

혼동 경계: 삭발이라는 동작·도구와 사진 속 남은 길이를 분리한다. smooth scalp는 클래식 잔모 버즈의 비교 조건이다. 상부가 길다고 buzz 계열을 무조건 배제하지 않는다. crew-buzz와 disconnected-buzz라는 혼합 용례가 있다. 가드 번호를 픽셀만으로 판정하지 않는다.

양립 가능: 선택적 fade/taper; hard_part; line_up; 색상·모질 다양성. 같은 부위의 모순: 같은 클래식 부위의 긴 보브 외곽; classic_uniform과 같은 영역의 큰 길이 단차 동시 의무.

필수 시야: three_quarter_plus_optional_rear — top, ear-side hair, nape if all-over claim. 정면의 두피만 보이는 crop는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-002`: 매우 짧은 고전형, 대체로 균일함, fade/disconnected/crew 혼합 명칭의 공존; `cuts-supp-src-001`: 자가 커트 절의 buzz 직접 이름 용례.

불확실성: uniform은 classic의 제약이지 전체 buzz 명칭의 유일한 정의가 아니다. 잔모는 색·조명·모밀도 때문에 안 보일 수 있다.

> a classic buzz cut with very short, near-even visible stubble following the head shape

classic/subtype를 먼저 고른다. 숫자 guard, 군인 설정, 성별, 두피 완전 노출을 덧붙이지 않는다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H067 크루컷 / Crew cut

`hair-cut-supp-crew` · `hair.cut.short_structure` · research draft

짧은 옆·뒤 위에 조금 더 길고 형태를 가진 상부를 남기는 쇼트컷이다. Wahl 교육 예에서는 상부의 길이가 변하며 두상 윤곽을 따른다.

Owner/region: `subject.hair` → top, sides, back.

관찰 가능한 최소사인: 매우 짧은 측면과 구분되는 짧은 상부 길이; 플랫톱의 수평 deck 없이 두상에 가까운 상부 윤곽.

혼동 경계: buzz를 완전 배제하는 taxonomy는 브랜드의 crew-buzz 용례와 충돌한다. 시저/프렌치 크롭을 앞머리 단서 없이 크루와 동일시하지 않는다. 픽시와 형태가 겹칠 수 있으므로 사진만으로 성별 또는 원래 커트 이름을 판별하지 않는다.

양립 가능: taper/fade 측면 선택; 작은 상부 질감; 앞쪽 약한 세움 또는 전방 흐름. 같은 부위의 모순: 동일 상부에 수평 플랫톱 deck 의무; 같은 선택 부위에 완전 동일 길이와 분명한 상부 우세 길이 동시 의무.

필수 시야: eye_level_three_quarter_and_side — top silhouette, side contrast. 상부가 가려진 모자 또는 overhead crop는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-001`: Crew 상부 길이 변화와 두상 윤곽; 옆·뒤 짧음; `cuts-supp-src-002`: 크루의 상부 우세 길이 및 buzz 혼합 용례.

불확실성: 상부를 반드시 앞으로 빗거나 특정 앞머리로 만들 필요는 없다. tutorial guard는 고정 기준이 아니다.

> a short crew cut, with closely cropped sides and back and a slightly longer top following the rounded head contour

flat-top 판별에는 상부 외곽을 함께 보인다. 앞머리 길이·방향은 별도로 선택한다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H090 플랫톱 / Flat top

`hair-cut-supp-flat_top` · `hair.cut.top_geometry` · research draft

세워진 상부 모발 끝이 평평한 수평 면을 만드는 커트 형태다. 면의 높이와 측면 테이퍼·페이드는 별개이며 긴 기술 플랫톱 용례도 있다.

Owner/region: `subject.hair` → top_deck, sides.

관찰 가능한 최소사인: 정면과 옆에서 상부 끝이 수평 deck로 읽힘; 단순 높은 볼륨이 아니라 연속된 평면 실루엣.

혼동 경계: crew의 두상 곡선을 수평 면으로 오인하지 않는다. high-top fade는 높이와 측면 전이까지 설명하는 이름이며 한 provider의 flat-top variant 용례만으로 전체 동일시하지 않는다. 세운 앞머리나 pompadour 한 덩어리는 전체 상부 수평 deck가 아니다. 사진은 comb/clipper-over-comb 도구·기법 증거가 아니다.

양립 가능: low/tall deck; 측면 taper 또는 fade; 각진 또는 약간 둥근 코너; 서 있을 수 있는 straight/coily 결과. 같은 부위의 모순: 같은 deck의 rounded/domed 외곽 의무; 동일 상부 전반의 내려앉은 긴 머리.

필수 시야: eye_level_front_and_side — deck across left-right, front-back top silhouette. 높은 카메라·기울어진 머리로 평면이 원근에 왜곡됨는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-003`: 수평 평면 정의, 높이와 측면 taper/fade 변주, 제한된 hi-top 호칭; `cuts-supp-src-004`: long technical flat top이라는 교육자의 직접 명명.

불확실성: 머리 밀도와 질감은 형태 유지에 영향을 줄 수 있으나 ethnicity나 natural texture를 이름에서 추론하지 않는다. hightop/box 관계는 source-specific이다.

> upright top hair forming a level horizontal flat-top deck, with the chosen side taper kept visible

평면·높이·측면 전이를 나눠 선택한다. high-top fade의 자동 동의어 확장은 보류한다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H073 빅시컷 / Bixie cut

`hair-cut-supp-bixie` · `hair.cut.hybrid_family` · research draft

픽시와 짧은 보브 요소를 결합해 상부·옆의 짧은 층과 보브처럼 남긴 외곽·얼굴 옆 길이가 함께 읽히는 혼합 명칭이다.

Owner/region: `subject.hair` → crown, sides, face_frame, perimeter.

관찰 가능한 최소사인: 짧은 상부층과 더 길게 남긴 외곽이 동시에 읽힘; close-cropped pixie와 대조할 때 길이 보존이 보임.

혼동 경계: 자란 픽시·레이어드 보브와 연속적으로 겹치므로 이미지 단독 배타 분류를 요구하지 않는다. 숏컷 전체나 Garçon을 bixie 동의어로 합치지 않는다. 곱슬 금지는 John Frieda의 styling caution과 L’Oréal의 curly variant가 충돌한다.

양립 가능: curly/wavy/straight variants; 앞머리 선택; centre/side part; tousled/sleek finish. 같은 부위의 모순: 같은 외곽의 잔모 수준 buzz와 bob-like perimeter 동시 의무; one_length_no_layers와 분명한 crown short layers 동시 의무.

필수 시야: front_three_quarter_with_side_or_rear — crown layers, side/perimeter ends, ear and jaw anchor. 머리 윗부분만 찍어 남긴 외곽이 없음는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-005`: 짧은 crown/side 층과 길게 남긴 face pieces; fringe/part 선택; `cuts-supp-src-006`: bob/pixie 혼합과 모질 변주; `cuts-supp-src-007`: 비교용 pixie의 짧은 옆·뒤와 상부층.

불확실성: 두 브랜드의 길이 표현이 다르고 정의 문장 내부에도 bob/lob 표현 흔들림이 있다. 고정 centimetre bin 없이 혼합 구조로 보강한다.

> a bixie combining short textured crown layers with a longer, softly layered bob-like perimeter around the face

원하는 남김 길이를 귀·턱 기준으로 추가 선택한다. choppy와 sleek를 함께 강제하지 않는다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H077 언더컷 / Undercut

`hair-cut-supp-undercut` · `hair.cut.regional_contrast` · research draft

지정된 하부 측면·뒤쪽에 매우 짧거나 면도한 영역을 두고 위에 더 긴 모발을 남기는 길이 대비 구조다. 전이의 연결·단절은 별도 속성이다.

Owner/region: `subject.hair` → selected_lower_sides_or_back, overlying_upper_hair, junction.

관찰 가능한 최소사인: 선택한 짧은 하부와 더 긴 상부가 함께 보임; 그 두 영역의 상대 길이가 읽힘.

혼동 경계: 일반 undercut 정의에 반드시 단절이 들어간다고 단정하지 않는다. disconnected는 junction 조건을 추가한다. 두블럭과 구조가 겹칠 수 있으나 모든 undercut이 한국/일본 two-block 호칭을 쓰는 것은 아니다. sidecut/nape undercut는 부위 후보로 설계할 수 있지만 이 보충조사에서 각 원어의 직접 정의는 확인하지 않았다. covered undercut는 감춰진 정면 crop으로 구조 판정을 못 한다.

양립 가능: bob/pixie/long upper hair; 선택 부위 한쪽·양쪽·nape; exposed/covered styling; 짧은 하부 안의 fade 가능. 같은 부위의 모순: 동일 선택 하부와 상부가 같은 길이; 보이지 않는 하부를 visible-pass로 인정.

필수 시야: side_or_rear_for_selected_region — selected short zone, upper section, junction. 긴 윗머리가 선택된 짧은 영역 전체를 덮는 상태는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-007`: 매우 짧은 sides/back와 더 긴 top라는 일반 undercut 용례; `cuts-supp-src-008`: 비교되는 side disconnection과 covered/exposed 표현.

불확실성: 범용 undercut과 disconnected two-block 사이의 정확한 번역 등가는 확정하지 않는다. 부위별 카드로 쪼개기 전 명칭 직접 증거가 필요하다.

> a clearly visible undercut in the chosen lower side region, with substantially longer upper hair above it

좌우는 subject 기준으로 저장한다. nape/side 범위, junction 연결, 감춤 여부를 사용자가 선택해야 한다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H114 투블럭 / Two-block cut

`hair-cut-supp-two_block` · `hair.cut.regional_convention` · research draft

조사한 일본 살롱 용례에서는 귀 주변 짧은 측면과 더 긴 상부를 연결하지 않아 두 길이 영역을 만든다. 한국 공식 카탈로그는 투블럭을 다양한 가르마·펌·앞머리와 조합한다.

Owner/region: `subject.hair` → ear_side_lower_block, upper_hair, side_junction, back_or_nape.

관찰 가능한 최소사인: 선택된 측면의 짧은 하부와 긴 상부가 함께 보임; 단절형 선택 시 그 side junction의 길이 단차가 읽힘.

혼동 경계: back의 blend가 있다고 side의 two-block 구조까지 배제하지 않는다. 내린 mushroom fringe나 centre part는 필수 요소가 아니다. two-block과 undercut의 겹침을 강제 차이로 만들지 않는다. Korean catalog 이름만으로 정확한 millimetre, 두부 전체 단절, 펌 도구 또는 일본 유래를 증명하지 않는다.

양립 가능: back kariage/taper/fade; covered/exposed upper hair; comma/parted/pomade styling; perm-like curls or straight styling. 같은 부위의 모순: 같은 선택 side junction의 fully_blended와 visible_disconnection 동시 의무; 최소 사인 판정 시 side를 완전히 가린 crop.

필수 시야: three_quarter_side_and_optional_rear — ear-side block, upper block, side junction. 정면 fringe만 보이는 crop는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-008`: 귀 주변 side disconnection과 덮음/노출 버전; 뒷머리 전이 공존; `cuts-supp-src-009`: 단차 vs 점진적 kariage 대비; `cuts-supp-src-010`: 상부 움직임과 뒷목 taper를 결합한 고객 직접 사례; `cuts-supp-src-011`: 한국 직접 명칭과 앞머리·가르마·펌·색상 조합의 비고정성.

불확실성: 구조 정의 증거는 특정 일본 살롱이며 한국 자료는 named-use 수준이다. 한 나라의 모든 살롱을 포괄하는 표준으로 확장하지 않는다.

> a two-block cut with short hair around the ears beneath a longer upper section, leaving a distinct side-length step; the back transition remains separately specified

일본 documented disconnection variant로 좁혀 선택한다. 한국 이름만 주어지면 upper 길이와 side 단차 강도를 확인·선택하고 앞머리는 별도 축으로 둔다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H101 프렌치 보브 / French bob

`hair-cut-supp-french_bob` · `hair.cut.bob_variant` · research draft

볼·턱 주변의 짧은 보브 외곽을 바탕으로 끝을 뭉툭하게 또는 부드럽게 질감 처리하는 명칭이다. 앞머리·가르마·곱슬과 약한 레이어의 변형이 허용된다.

Owner/region: `subject.hair` → main_side_perimeter, back_perimeter, fringe_if_selected.

관찰 가능한 최소사인: 얼굴·턱과 짧은 보브 외곽이 같은 프레임에 보임; 선택한 blunt/soft end treatment가 읽힘.

혼동 경계: blunt bob 전체를 French bob 동의어로 바꾸지 않는다. 풀 앞머리·마이크로뱅·흑발·직모·프랑스 국적은 필수 요소가 아니다. 레이어드·컬리 보브 축과 함께 성립 가능하며 one-length만 강제하면 직접 변형 용례를 잃는다. pageboy의 inward curl은 현재 끝 styling일 수 있어 독점 차이가 아니다.

양립 가능: optional full/wispy/curtain/no fringe; straight/wavy/curly texture; subtle layers; centre/side part. 같은 부위의 모순: 동일 주요 외곽의 긴 허리 길이; 같은 외곽에 extreme disconnected long-tail을 French bob 최소사인으로 대체.

필수 시야: front_or_three_quarter_plus_side — cheek/jaw/chin anchor, main bob ends, selected fringe. 끝선이 밖으로 잘린 얼굴 초근접 crop는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-012`: 길이 body anchors, optional fringe/part와 curly/textured variants; `cuts-supp-src-013`: jaw-length soft-layered French bob이라는 교육 브랜드의 직접 표현.

불확실성: 짧은 보브와 한 번의 사진만으로 이름 고유성을 입증하기 어렵다. 정확한 길이는 body anchor, 끝선과 fringe는 별도 선택한다.

> a short French bob ending around the jaw, with softly defined ends and the explicitly chosen fringe and natural texture

plain bob 기존 후보를 재사용하고 길이·끝선·fringe 선택을 보강한다. 프랑스풍 성격이나 국적을 넣지 않는다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H104 페이지보이 / Pageboy

`hair-cut-supp-pageboy` · `hair.cut_or_styling.historical_label` · research draft

출처별 범위가 다른 역사적 커트·스타일 명칭이다. 조사한 L’Oréal 직접 용례는 매끈한 모발과 안으로 말린 끝, 중·장발을 포함하며 Sam Villa는 modern pageboy의 매끈함과 움직임만 명명한다.

Owner/region: `subject.hair` → main_lengths, perimeter_ends.

관찰 가능한 최소사인: 선택된 source-specific inward-end 변형의 길이와 끝 말림이 보임; 명칭 독자성 판단은 이 사인만으로 통과시키지 않음.

혼동 경계: 짧은 턱 길이·uniform fringe·bowl/mushroom 형태를 이름만으로 강제하지 않는다. 단발 bob은 길이/외곽 축이고 inward end는 styling 축이라 동시에 성립 가능하다. 단순 인컬 사진이 pageboy의 역사적 고유 커트를 입증하지 않는다.

양립 가능: 선택된 bob 또는 medium/long length; 사용자가 선택한 fringe; smooth finish; inward end bend. 같은 부위의 모순: 같은 선택 끝선의 inward와 outward 방향 동시 의무; 고유 명칭 판정이 필요한 상황에서 인컬만으로 unique style ID 확정.

필수 시야: front_three_quarter_and_side — chosen length anchors, side/back inward end silhouette. 끝 말림이 가려진 상반신 crop는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-014`: 중·장발 smooth inward-curled pageboy 스타일 직접 용례; `cuts-supp-src-013`: modern pageboy 명칭과 smooth-with-movement 예.

불확실성: strict pageboy cut의 통일된 fringe·길이·outline에 대한 직접 교육 증거가 부족하다. 자동 cut profile 활성화는 hold.

> a smooth pageboy-inspired finish at the chosen length, with the visible perimeter ends curving inward

명칭 기반 자동 선택을 보류한다. 사용자가 source variant 또는 reference geometry를 고른 경우 관찰 가능한 길이·끝 방향만 제안한다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H108 버터플라이컷 / Butterfly cut

`hair-cut-supp-butterfly` · `hair.cut.layer_distribution` · research draft

짧은 얼굴 둘레 층과 전체 길이를 남기는 더 긴 층을 함께 배치하는 레이어 명칭이다. 얼굴 주변의 가벼운 부피와 흐름이 핵심이며 밖으로 말린 끝은 styling 선택이다.

Owner/region: `subject.hair` → face_frame, upper_layers, underlying_lengths.

관찰 가능한 최소사인: 얼굴 옆 짧은 끝과 더 아래로 남은 긴 층이 함께 보임; 선택한 부위에 부드러운 층 흐름이 읽힘.

혼동 경계: generic long layers와 완전 배타는 아니다. face-frame 집중이 약한 대조 예는 별도다. John Frieda의 octopus 별칭과 L’Oréal의 octopus 구분이 충돌하므로 exact synonym은 hold. 단절 vs blended라는 source copy 차이 때문에 salon-technique disconnection을 필수로 만들지 않는다. wolf의 짧고 choppy한 crown/뒤 긴 꼬리와 일부 겹칠 수 있어 방향·층 위치·남는 길이를 명시한다. feathered 결과는 razor·point-cutting 절차의 증거가 아니다.

양립 가능: short/medium/long selected length; straight/wavy/curly variant; curtain/side/no fringe; outward blowout or softer finish. 같은 부위의 모순: 같은 선택 face-frame 부위에 no_short_layers 의무; 모든 길이가 동일하면서 두 층 길이 대비 의무.

필수 시야: front_or_three_quarter_with_entire_selected_ends — face-frame ends, longer underlying ends, face and chosen length anchor. 가슴 아래만 찍거나 얼굴만 찍어 두 층 관계를 잃음는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-015`: short face-framing + longer retained layers; 여러 길이·질감과 optional fringe; wolf/octopus 차이 설명; `cuts-supp-src-016`: 두 길이의 층과 별칭 사용의 충돌 증거.

불확실성: 소스가 short butterfly까지 제시하므로 below-shoulder를 하드 의무화하지 않는다. octopus exact alias와 technical disconnection은 보류한다.

> a butterfly cut with shorter soft face-framing layers above retained longer lengths, creating airy movement around the face

선택한 face-frame 끝 anchor와 전체 길이를 함께 기록한다. blowout 방향은 커트와 다른 축이며 이름만으로 curl naturalness를 추론하지 않는다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

### H092 하드 파트 / Hard part

`hair-cut-supp-hard_part` · `hair.part.carved_line_appearance` · research draft

자연스럽게 모발을 갈라 만든 선과 구분하여, 지정된 가르마 경로에 좁고 또렷한 노출 채널을 내는 바버 용어다. 출처는 shaved/razored라 설명하지만 결과 사진은 도구 종류를 입증하지 않는다.

Owner/region: `subject.hair` → chosen_part_path, adjacent_hair.

관찰 가능한 최소사인: 한쪽 가르마 경로에 뚜렷한 좁은 노출 선이 보임; 선 옆 모발과의 잘 정의된 경계가 읽힘.

혼동 경계: 자연 scalp part 역시 노출될 수 있어 선의 경계·규칙성·인접 짧은 모발을 함께 본다. line-up은 외곽 hairline 정리이며 내부 part path와 다르다. 임의 decorative shaved stripe가 실제 가르마를 구분하지 않으면 hard part로 자동 합치지 않는다. 특정 면도기·trimmer를 사진으로 확정하지 않는다.

양립 가능: buzz/crew/top styling combinations; fade/taper; 선택적 side part; 선택적 line_up 외곽. 같은 부위의 모순: 같은 경로에 carved channel 없음과 visible sharp channel 의무; 가르마 위치를 보이지 않은 반대쪽에서 판정.

필수 시야: slightly_high_three_quarter_on_selected_part_side — entire chosen part channel, adjacent hair, front hairline if outer-vs-inner confusion. 반대편 측면 또는 채널을 긴머리가 덮음는 판정에 부적합하다.

출처별 지원: `cuts-supp-src-017`: soft natural part와 shaved/razored hard part의 직접 비교; `cuts-supp-src-002`: buzz+hard part 공존 및 폭 변주.

불확실성: 얇고 자연스러운 가르마와 강한 hard part 사이 모호성은 남는다. geometry gate로 관찰성을 확보하고 도구 절차 여부는 abstain.

> a narrow, sharply defined exposed hard-part channel along the chosen side part, clearly visible between the adjacent hair sections

subject-left/right와 경로를 선택한다. razor-cut/질병/흉터 또는 성격 의미를 부여하지 않는다.

Image gate: **not_run**. 선택한 최소사인을 모두 확인해야 하며 가림·crop·원근 문제는 unscorable이다. 고유 명칭, 시술 도구·과정 및 문화적 출신은 이 gate가 입증하지 않는다.

## 원본 25개 표기의 보충 범위와 hold

| 원본 ID | 정확한 원본 표기 | 이번 보충 상태 | 메모 |
|---|---|---|---|
| H065 | 삭발 / Shaved head | hold_not_independently_verified_in_supplement | 짧은 잔모 vs bare scalp의 시각 대조만 설계; shaved 도구·방식이나 명칭 고유성 직접 추가 검증 없음. |
| H066 | 버즈컷 / Buzz cut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H067 | 크루컷 / Crew cut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H068 | 아이비리그 컷 / Ivy League cut | hold_not_independently_verified_in_supplement | Ivy League 직접 교육 정의와 crew/side-part 경계는 이번 보충에서 검증하지 않음. |
| H069 | 시저컷 / Caesar cut | hold_not_independently_verified_in_supplement | Caesar의 별도 후보·프린지 경계는 이번 보충에서 직접 열람 검증하지 않음. |
| H070 | 프렌치 크롭 / French crop | hold_not_independently_verified_in_supplement | French crop의 crew/Caesar 경계 직접 증거는 이번 보충에서 확보하지 않음. |
| H071 | 텍스처드 크롭 / Textured crop | hold_not_independently_verified_in_supplement | Textured crop의 정의와 기법-결과 분리는 이번 보충에서 추가 검증하지 않음. |
| H072 | 픽시컷 / Pixie cut | source_grounded_boundary_only | 픽시 자체는 John Frieda 직접 정의로 빅시 대조에 사용; 기존 초기 카드 재사용을 main executor가 대조한다. |
| H073 | 빅시컷 / Bixie cut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H074 | 가르송컷 / Garçon cut | hold_not_independently_verified_in_supplement | Garçon을 pixie의 고정 동의어로 합치는 근거 없음; 원래 명칭 그대로 hold. |
| H075 | 보울컷 / Bowl cut | hold_not_independently_verified_in_supplement | Bowl의 페이지보이 전체 동의어화 직접 근거 없음; 기존 자료 검토는 main executor 소유. |
| H076 | 머시룸컷 / Mushroom cut | hold_not_independently_verified_in_supplement | 박준 catalog에 머쉬룸컷 명칭은 있으나 bowl/pageboy와 구조상 완전 동일함은 검증하지 않음. |
| H077 | 언더컷 / Undercut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H078 | 디스커넥티드 언더컷 / Disconnected undercut | property_boundary_translation_hold | disconnection을 junction 축으로 설명했지만 disconnected undercut 전체와 two-block의 정확한 번역 등가는 hold. |
| H079 | 사이드컷 / Sidecut | hold_not_independently_verified_in_supplement | 선택 side undercut 부위 확장은 설계안; Sidecut라는 원어의 직접 일차 정의는 미확보. |
| H080 | 네이프 언더컷 / Nape undercut | hold_not_independently_verified_in_supplement | 선택 nape undercut 부위 확장은 설계안; Nape undercut라는 원어의 직접 일차 정의는 미확보. |
| H090 | 플랫톱 / Flat top | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H091 | 하이톱 페이드 / High-top fade | source_specific_boundary_global_taxonomy_hold | CADMEN은 tall flat-top fade를 hi-top으로 명명; high-top fade의 모든 변형을 flat-top으로 합치는 전역 등가는 hold. |
| H092 | 하드 파트 / Hard part | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H101 | 프렌치 보브 / French bob | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H102 | 레이어드 보브 / Layered bob | source_grounded_axis_only | French bob의 soft/subtle layer 직접 용례를 사용; layered bob 전체의 독립 새 카드 추가는 하지 않음. |
| H103 | 컬리 보브 / Curly bob | source_grounded_axis_only | French bob의 curly variant 직접 용례를 사용; curly bob 전체의 독립 새 카드 추가는 하지 않음. |
| H104 | 페이지보이 / Pageboy | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H108 | 버터플라이컷 / Butterfly cut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |
| H114 | 투블럭 / Two-block cut | direct_card_target | 새 연구 카드 대상. 자동 반영 여부는 해당 card의 recommendation과 image gate를 따른다. |

## 대조 설계 12개 — 아직 실행하지 않음

같은 subject·광원·hair colour·density·배경·camera를 유지한다. 바뀌는 속성은 각 pair의 manipulated axis에 한정한다. name overlap과 visibility control은 결과를 강제로 다르게 만들어서는 안 된다. 이 문서의 prompt fixtures는 source 이미지 재현이나 native-pixel 성공 기록이 아니다.

| ID | 대조 | 조작 축 | 관찰 또는 abstention |
|---|---|---|---|
| `cuts-supp-pair-01` | 클래식 버즈 잔모 vs 매끈한 두피 | visible_stubble | 남은 잔모의 존재를 비교한다. 원래 삭발 도구와 동작은 판별하지 않는다. |
| `cuts-supp-pair-02` | 클래식 버즈 vs 크루의 상부 우세 길이 | relative_top_to_side_length | 상부가 측면보다 분명히 더 길어지는지만 비교한다. broad buzz family와 crew가 겹칠 수 있다. |
| `cuts-supp-pair-03` | 크루의 둥근 상부 vs 플랫톱 평면 | top_outline_geometry | 같은 eye-level 옆/정면에서 두상 곡선과 수평 deck를 구분한다. |
| `cuts-supp-pair-04` | 낮은 vs 높은 플랫톱 | deck_height | 둘 다 플랫톱이어야 한다. 높아졌다는 이유만으로 특정 문화·인종·high-top 전체 동일성을 만들지 않는다. |
| `cuts-supp-pair-05` | 픽시 vs 빅시의 외곽 길이 보존 | retained_side_and_face_perimeter | 남긴 외곽 길이 대비가 목적이다. 긴 pixie와 짧은 layered bob의 연속 영역에서는 unique name 판정은 abstain. |
| `cuts-supp-pair-06` | 보이는 언더컷 vs 가려진 언더컷 | upper_hair_occlusion | B는 커트 변화가 아니라 가림 변화다. B를 구조 실패로 단정하지 않고 unscorable로 둔다. |
| `cuts-supp-pair-07` | 측면 단절 투블럭 vs 측면 연결 테이퍼 | selected_side_junction_connection | 선택한 side junction 단차만 대조한다. 뒷목은 두 경우 모두 같은 gradual blend로 유지한다. |
| `cuts-supp-pair-08` | 언더컷 vs 투블럭 명칭의 겹침 | label_only_same_geometry | 문구 이름만 달라졌다면 같은 구조가 허용된다. 두 이름에 반드시 서로 다른 fringe·국적·전체 length를 생성하면 실패다. |
| `cuts-supp-pair-09` | 직모 vs 컬리 프렌치 보브 | texture_same_apparent_length | 둘 다 French bob으로 허용한다. apparent end anchor는 같게 유지하므로 curl shrinkage를 길이 차로 오인하지 않는다. |
| `cuts-supp-pair-10` | 보브 끝의 자연 낙하 vs 페이지보이 용례의 안쪽 말림 | end_bend_direction | 현재 끝 styling만 비교한다. B만으로 historical pageboy의 strict cut identity를 확정하지 않는다. |
| `cuts-supp-pair-11` | 일반 긴 층 vs 얼굴 둘레 집중 버터플라이 | face_frame_layer_distribution | overall length·광택·질감은 같게 두고 face-frame 끝 위치만 비교한다. 단절 기법 또는 octopus 동일성은 점수화하지 않는다. |
| `cuts-supp-pair-12` | 자연 가르마 vs 하드파트 채널 | part_channel_edge_morphology | 같은 위치에서 경계와 채널 규칙성을 비교한다. tiny part가 indistinguishable이면 abstain하며 도구 판별을 하지 않는다. |

## 일차 자료 목록

각 URL은 직접 열람한 publisher text/PDF이다. 아래 요약은 장문 인용이 아닌 조사자의 짧은 요약이다. 세부 unsupported claims와 locator는 `cuts-supplement-sources.json`에 있다.

| source ID | Publisher / 직접 문서 | 확인 범위 | 제한 |
|---|---|---|---|
| `cuts-supp-src-001` | [Wahl USA — Home Haircutting Made Simple](https://wahlusa.com/media/wahl-home-haircutting.pdf) | Crew: sides very short; top length varies and generally follows the head shape. Buzz is separately named in the self-cut example. | Older undated manual; guard examples are a specific tutorial, not universal numeric style thresholds. Tools and cutting order cannot be recovered from a finished photograph. |
| `cuts-supp-src-002` | [L’Oréal Paris USA — Just Shave It: 10 Buzz Cut Hairstyles For Men](https://www.lorealparisusa.com/beauty-magazine/hair-style/short-hairstyles/buzz-cut-styles-for-men) | Buzz usually has very short, approximately uniform length; this guide also names faded, disconnected, crew/buzz, line-up and hard-part combinations. Crew example keeps cropped top length over shorter back/sides. Hard-part examples vary width. | Source uses buzz as both a classic style and a broad family, so exclusivity with crew/fade/disconnection is not justified. Historical, face-shape and gender-marketing statements are not adopted. |
| `cuts-supp-src-003` | [CADMEN Barber Academy, Mississauga, Ontario — How to Do a Flat Top Haircut: The Technique for a Level Crown](https://academy.cadmen.ca/post/how-to-do-flat-top-haircut) | Flat top: upright top hair forms a level horizontal surface; side taper/fade and top height are separately variable. The FAQ names a tall flat-top fade as hi-top fade. | Private provider explicitly does not offer Ontario apprenticeship hours/qualification pathways. Its hi-top wording is one provider convention, not an exhaustive universal high-top taxonomy. Numeric height and maintenance advice not adopted. Source image is stock-linked and was not inspected. |
| `cuts-supp-src-004` | [MHD / Dale Ted Watkins — Step By Step Guide To Flat Top Haircut Video](https://myhairdressers.com/videos/long-technical-flat-top) | Educator labels a long technical flat top, supporting length variation within the named style. | Public overview read; paid video and step-by-step member content were not accessed. Listed techniques do not establish that a result photograph used those tools. |
| `cuts-supp-src-005` | [John Frieda UK — The Ultimate Guide to Bixie Cuts](https://www.johnfrieda.com/en-uk/blog/hairstyles/bixie-cuts/) | Bixie combines pixie and short bob, with shorter textured crown/side layers and longer face pieces. Fringe and parting variants are named. | Typical length overlaps bob territory. Curl styling cautions differ from L’Oréal; do not encode a curl incompatibility or exact length bin. Search title and dated body can differ. |
| `cuts-supp-src-006` | [L’Oréal Paris USA — The ’90s Bixie Haircut Is Back and Trendier Than Ever](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/what-is-the-bixie-haircut) | Bixie is a bob/pixie hybrid combining choppy voluminous layers with retained bob-like length; straight, wavy and curly versions are named. | Intro mentions lob-like length while the definition says shorter than bob: no fixed centimetre or anatomical limit adopted. Broad suitability is marketing, not a biological guarantee. |
| `cuts-supp-src-007` | [John Frieda UK — Our Favourite Short Haircuts for Women](https://www.johnfrieda.com/en-uk/blog/hairstyles/short-hairstyles-for-women/) | Pixie typically has cropped sides/back and longer top layers. Undercut keeps very short/shaved side/back regions beneath a longer top. Bob is a broad ear-to-shoulder family and can be straight or wavy. | General undercut definition does not explicitly require an unblended junction in every case. Gender framing, maintenance and face-shape suitability are not semantic obligations. |
| `cuts-supp-src-008` | [Ash 練馬店 / 鈴木拓斗 — メンズ必見ツーブロックの使い回し！](https://nerima.ash-hair.com/posts/10878447/) | In this salon convention, two-block shortens side hair near the ears without connecting it to longer upper hair. Covered and exposed versions are described; back taper can coexist. | One Japanese salon convention; no global definition, national origin or fixed length claimed. Product, chemical-safety and appearance-marketing text excluded. |
| `cuts-supp-src-009` | [HAIR MAKE Ash 鶴ヶ峰1号店 / 黄祥一 — 刈り上げとツーブロックの違いについて！](https://tsurugamine1.ash-hair.com/posts/39874753/) | Two-block has an upper/lower step, while the contrasted kariage has a gradual sloping transition. Several short-region length examples are offered. | Do not translate every 刈り上げ as skin fade. Millimetre examples vary and are not mandatory. Source text references photos; their pixels were not inspected. |
| `cuts-supp-src-010` | [Ash 高津店 / 但野 — お客様カルテ〖ツーブロ刈り上げショート〗](https://takatsu.ash-hair.com/posts/41758814) | A named two-block case combines short sides/back, movement on top and a shaped, tapering nape. | Single customer case does not require all two-blocks to have the same top styling, nape or length. Source image pixels not inspected. |
| `cuts-supp-src-011` | [박준뷰티랩 — BEAUTYLAB IT HAIR — 투블럭컷 filter](https://parkjun.com/park/bbs/board.php?bo_table=hair&cate=1&wr_1=%EB%82%A8%EC%9E%90&wr_2=%ED%88%AC%EB%B8%94%EB%9F%AD%EC%BB%B7&wr_3=&wr_4=) | Korean official catalog uses 투블럭컷 and 소프트투블럭컷 separately from parts, comma/pomade styling, perms and colours. Both short and medium-length cases are named. | Catalog names establish use and coexistence only; they do not define an exact length step or provide a formal Korean national standard. Linked videos/Naver posts and image pixels were not inspected. |
| `cuts-supp-src-012` | [John Frieda UK — Guide to French Bobs](https://www.johnfrieda.com/en-uk/blog/hairstyles/french-bobs/) | French bob is a short bob around cheekbone/jaw/chin with blunt or softly textured ends. Fringe, parting and straight/wavy/curly variants can vary. | Internal copy varies between one-length and subtle-layered versions; no mandatory fringe, single exact length or unique visual identity adopted. Parisian identity and nationality are not owner properties. |
| `cuts-supp-src-013` | [Sam Villa / Lori Barsamian — The Ultimate Fall Styling Guide: Tools and Techniques for Seasonal Trends](https://www.samvilla.com/blogs/hair-tutorials/the-ultimate-fall-styling-guide-tools-and-techniques-for-seasonal-trends) | French bob is described as jaw-length with soft layering; modern pageboy is named as sleek with movement. | Modern pageboy mention lacks a complete length/fringe/outline definition. Product suggestions do not prove the tool used in an image. Trend ranking is not adopted. |
| `cuts-supp-src-014` | [L’Oréal Paris USA — 13 Beautiful 1940s Hairstyles You Can Still Wear Today](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/1940s-hairstyles) | Here pageboy denotes smooth strands with inward-curled ends, including medium/long styling. | This broader historical styling usage cannot establish that every pageboy is a short bob or a bowl cut. English page first failed, then opened successfully via search reference; same brand language mirror also read. |
| `cuts-supp-src-015` | [L’Oréal Paris USA / Gillian Fuller — How To Make the Butterfly Cut Work for Your Hair Type and Texture](https://www.lorealparisusa.com/beauty-magazine/hair-style/hairstyle-trends/butterfly-haircut) | Butterfly combines shorter face-framing layers with retained longer layers and feathered movement. Short, medium and long variants are named; fringe is optional. This page distinguishes butterfly from wolf and octopus styles. | Copy describes layers as disconnected in one comparison and blended in another, so technical disconnection is not mandatory. Styling-dependent outward bends are not a proof of a cutting tool or natural wave. |
| `cuts-supp-src-016` | [John Frieda UK — The Ultimate Guide to Butterfly Cuts](https://www.johnfrieda.com/en-uk/blog/hairstyles/butterfly-cuts/) | Shorter face-framing layers plus longer retained lengths define the stated butterfly structure. The page also calls butterfly sometimes octopus. | The octopus-alias statement conflicts with L’Oréal’s explicit distinction. Treat it as search-use evidence, not equivalent semantic identity. |
| `cuts-supp-src-017` | [Alfani’s Barbershop, Denver / Artur Simonov — The Classic Side Part: Timeless Style Guide](https://www.alfanisbarbershop.com/blog/classic-side-part-guide) | Hard side part is explicitly contrasted with a natural soft part and described as a shaved/razored part line. | One shop’s styling convention; the finished visible channel cannot prove razor rather than trimmer. Profession, masculinity and formality claims are excluded. |

## 열람 한계와 다음 확인 항목

Wahl USA의 crew/guard HTML은 검색 본문을 볼 수 있었지만 direct open이 실패하여 채택 출처에 넣지 않았다. PDF 직접 자료로 대체했다. Pall Mall hard-part 자료는 header 이후 timeout이라 채택하지 않았다. nape undercut/sidecut/disconnected undercut 대상 검색에서 직접 정의가 확보되지 않았다는 사실은 명칭이 존재하지 않는다는 뜻이 아니다.

후속 검증은 기존 후보 중복 대조 → source-specific 선택 범위 확정 → 필요한 camera를 갖춘 native image 대조 → 결과·도구·명칭 증거 분리 순서다. 현재 source-text 열람과 구조적 JSON 검사까지 완료했고, 후보 활성화·retrieval 효과·이미지 픽셀·사용자 수락은 검증하지 않았다.

원본 세 파일의 보존 해시:

- `specialist-cuts.md`: `4d2dc1c14c028f3d546f3000d8571b5b315737dec7fad890dbd7753e372a1662`
- `cuts-cards.json`: `f674b9741db7f46769917d90d6714127c5c4e1ba7d8d367d71b9b327094b131a`
- `cuts-sources.json`: `7a619ed796a80d5a11bd1625f6dd14cdd54c2b865680a0d38c94db9e1feb3174`

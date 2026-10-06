# 100개 배색의 시각 의미 카드

2026-10-06 KST · 선택 가능한 설계 예시 · 활성 데이터/인덱스/이미지 검증 미실행

각 색의 owner는 하나의 가능한 적용 예시다. 조합 이름만으로 이 물체·재질·면적·장면을 요구하지 않는다. 출처는 맥락과 구조를 뒷받침하며, HEX·배치는 제안값이다.

전체 정의·효과 초안은 SEMANTIC-CARDS.json과 CANDIDATE-DRAFTS.json, 계산값은 SWATCH-METRICS.json에 있다.

## P001 흑백 그래픽

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 색채보다 윤곽·형태·여백을 주인공으로 만든다. 패션 에디토리얼, 타이포그래피, 건축적 구도에 적합하다. 백색을 넓히면 가벼워지고, 검정을 넓히면 극적이고 무거워진다.

**관찰할 관계:** The light field and dark contours retain separate readable surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F7F7F2|an off-white image field|큰 바탕 예시|0.974757 / 0.006602|
|#161616|black bounded contours|윤곽·경계|0.200193 / 0.0|

**오인 경계:** 저채도 파랑·세피아를 무채색으로 오인하거나 그림자 내부를 전부 뭉개는 실패

**연결:** M02, M04 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S18 Hygge Color Palette Ideas](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/hygge-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P002 웜 화이트·오트밀

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 비슷한 온도의 저채도색을 겹쳐 부드러운 생활감을 만든다. 니트·침구·밝은 목재·일상 사진에 적합하며, 색 차이보다 직물의 결을 보여주는 방식이 좋다.

**관찰할 관계:** Small tonal steps separate the warm wall, cloth and seams while weave remains visible.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F4EFE6|a warm-white existing wall|큰 바탕 예시|0.953541 / 0.013128|
|#D9CBB5|oatmeal-colored existing cloth|지지 영역|0.84769 / 0.033628|
|#9C8C7B|taupe existing seams|어두운 지지점|0.649562 / 0.031225|

**오인 경계:** 모든 중성색이 같은 밝기로 합쳐져 직물의 결과 경계가 사라짐

**연결:** M02 · P0

**맥락 출처:** [S18 Hygge Color Palette Ideas](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/hygge-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P003 차콜·그레이지

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 순수한 흑백 대비를 누그러뜨린 차분한 현대성. 날카로운 선은 유지하면서 차가운 사무실 같은 인상을 줄이고 싶을 때 사용한다.

**관찰할 관계:** Charcoal edges divide two lighter neutral surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#C8C0B4|a greige existing wall|큰 바탕 예시|0.810962 / 0.018857|
|#303235|a charcoal existing frame|어두운 지지점|0.316306 / 0.006025|
|#F3F1EA|an off-white existing panel|밝은 구별 영역|0.957756 / 0.009538|

**오인 경계:** 검정과 순백으로 과도하게 치환하거나 프레임색이 다른 물체로 이동함

**연결:** M02, M03 · P0

**맥락 출처:** [S18 Hygge Color Palette Ideas](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/hygge-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P004 카멜·초콜릿·크림

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 같은 갈색 계열을 밝기로 나누어 색은 적고 소재는 풍부한 화면을 만든다. 가죽·울·목재·가을 코트처럼 재질 중심의 컨셉에 적합하다.

**관찰할 관계:** Three warm brown-related regions remain distinct through tonal steps and existing texture.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F3E7D2|cream existing cloth|밝은 구별 영역|0.931919 / 0.030746|
|#C49665|camel-brown existing leather|중간 밝기|0.705458 / 0.085445|
|#493126|chocolate-brown existing wood|어두운 지지점|0.338307 / 0.039871|

**오인 경계:** 갈색 전역 필터로 천·가죽·목재의 국소색을 모두 같게 만듦

**연결:** M02, M05 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P005 콘크리트 모노크롬

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 채색보다 질량·표면·그림자가 읽히도록 한다. 산업 제품, 콘크리트 공간, 조형적인 인물 사진에 적합하다. 명도 차가 없으면 단순히 탁해지므로 면을 구분한다.

**관찰할 관계:** Gray planes separate through local shading and bounded dark recesses.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#D2D3CF|a light-gray existing concrete plane|밝은 구별 영역|0.864939 / 0.005542|
|#949792|a medium-gray existing concrete wall|중간 밝기|0.672407 / 0.008016|
|#282C2B|a charcoal existing recess|어두운 지지점|0.288767 / 0.00595|

**오인 경계:** 색만 회색이고 표면 깊이·경계가 사라지거나 필터로 콘크리트 재질을 주장함

**연결:** M02 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P006 안개색·슬레이트

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 청회색 안에서 밝기를 나누어 맑지만 눈부시지 않은 차분함을 설계한다. 유리·금속·흐린 날 풍경·정적인 제품 사진에 적합하다.

**관찰할 관계:** The pale field, slate object and deep-blue edge occupy distinct tonal regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E6EEF0|a pale mist-blue existing background|큰 바탕 예시|0.94365 / 0.008975|
|#8495A2|a slate-blue existing object|중간 밝기|0.660694 / 0.02748|
|#243B4A|a deep-blue existing edge|어두운 지지점|0.340131 / 0.039143|

**오인 경계:** 청회색 단색 틴트로 전역을 평평하게 만들어 유리·금속 경계를 없앰

**연결:** M02, M12 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S05 ICC Display calibration](https://www.color.org/displaycalibration/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P007 아이보리·머시룸·올리브

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 거의 중성색처럼 보이되 녹색 기운을 조금 남기는 절제된 자연성. 식물 컨셉을 강하게 드러내지 않고 흙과 잎의 단서만 넣고 싶을 때 좋다.

**관찰할 관계:** One bounded olive detail retains visible green amid larger neutral regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F1EDDF|an ivory existing field|큰 바탕 예시|0.945414 / 0.019061|
|#AAA08F|a mushroom-gray existing object|지지 영역|0.709508 / 0.026742|
|#505440|a dark-olive existing detail|작은 강조|0.436241 / 0.031952|

**오인 경계:** 큰 녹색 잎·식물을 추가해 절제된 색 선택을 보태니컬 장면으로 바꿈

**연결:** M03 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S18 Hygge Color Palette Ideas](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/hygge-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P008 뉴트럴 속 코발트 한 점

**계열:** 미니멀·뉴트럴: 색보다 형태와 재질을 보이게 하는 조합

**설계 의도:** 무채색에 가까운 화면에서 한 물체에만 시선을 집중한다. 작품·가방·의자·제품을 포인트로 삼는 구성에 적합하다. 코발트는 전체의 10% 이하부터 시도한다.

**관찰할 관계:** A single bounded cobalt object stands apart from the larger neutral field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F2F0E9|an off-white existing background|큰 바탕 예시|0.954749 / 0.009546|
|#323538|a graphite existing frame|어두운 지지점|0.327187 / 0.006741|
|#244BD8|one cobalt-blue existing object|작은 강조|0.48489 / 0.219122|

**오인 경계:** 코발트를 배경·피부·다른 소품 전체에 퍼뜨리거나 작은 강조를 큰 색면으로 바꿈

**연결:** M03, M12 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P009 검정·골드 — Black & Gold

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 어두운 바탕과 금속 반사의 차이로 장식의 존재감을 키운다. 주얼리·야간 행사·장식적인 패키지에 적합하다. 금색은 넓은 노란 면보다 가는 선과 금속 부품에 배치한다.

**관찰할 관계:** Warm gold reflection remains confined to the metal trim against the dark field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#121212|a black existing background|큰 바탕 예시|0.182204 / 0.0|
|#C3A45A|antique-gold existing metal trim|반사 강조|0.730805 / 0.100214|
|#F1E9D8|an ivory existing detail|밝은 구별 영역|0.935738 / 0.024181|

**오인 경계:** 넓은 노란 페인트 면으로 금속을 대체하거나 실제 금 성분을 단정함

**연결:** M01, M05 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P010 아이보리·샴페인

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 검정·금색의 무게를 걷어낸 밝고 의례적인 우아함. 초대장·웨딩·뷰티 촬영에 적합하다. 색 대비가 약하므로 엠보싱·주름·그림자로 형태를 보완한다.

**관찰할 관계:** The ivory field leads while champagne cloth and smaller gold fittings retain their own surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F5EFDF|an ivory existing surface|큰 바탕 예시|0.952496 / 0.022127|
|#DAC6A2|champagne-colored existing cloth|지지 영역|0.834109 / 0.053097|
|#B49355|small warm-gold existing fittings|반사 강조|0.680172 / 0.089694|

**오인 경계:** 9번의 검정 바탕 비율을 가져오거나 낮은 색 차이를 장식 추가로 덮음

**연결:** M01, M05 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P011 네이비·브라스

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 푸른 어둠과 따뜻한 금속을 대비시켜 차분함과 장식성을 함께 남긴다. 서재·호텔·클래식 제품에 적합하며, 황동은 프레임과 손잡이에 모은다.

**관찰할 관계:** Warm brass-colored reflections separate from the navy panel and cream cloth.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#172B49|a navy existing panel|큰 바탕 예시|0.288883 / 0.061097|
|#B89B5E|brass-colored existing hardware|반사 강조|0.702034 / 0.086706|
|#EEE7D9|cream existing cloth|밝은 구별 영역|0.929662 / 0.02015|

**오인 경계:** 황동색을 노란 조명으로 대체하거나 프레임·손잡이에 없는 부품을 추가함

**연결:** M05, M12 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P012 에메랄드·검정·골드

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 녹색을 깊고 짙게 잡아 잎보다 보석 같은 밀도를 강조한다. 벨벳·장식적 실내·주얼리에 적합하다. 부드러운 직물과 매끈한 금속의 차이를 함께 사용한다.

**관찰할 관계:** The deep-green textile remains distinct from the black ground and reflective gold fittings.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#155D47|an emerald existing textile|큰 바탕 예시|0.428944 / 0.078345|
|#17221E|a near-black existing ground|어두운 지지점|0.239956 / 0.017354|
|#C4A257|gold-colored existing fittings|반사 강조|0.727315 / 0.102266|

**오인 경계:** 벨벳·보석·잎을 서로 자동 대체하거나 녹색을 무조건 자연으로 해석함

**연결:** M05 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P013 버건디·아이보리·브라스

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 붉은색의 직접적인 자극을 어둡게 눌러 숙성된 분위기와 격식을 설계한다. 만찬·책 표지·클래식 의상·기념 패키지에 적합하다.

**관찰할 관계:** A light ivory region separates burgundy cloth from smaller warm metallic trim.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#692B39|burgundy existing cloth|큰 바탕 예시|0.380494 / 0.089767|
|#F1E5D0|an ivory existing surface|밝은 구별 영역|0.925866 / 0.030793|
|#AE8C50|brass-colored existing trim|반사 강조|0.658842 / 0.088428|

**오인 경계:** 버건디를 선명한 원색 빨강으로 만들거나 붉은색만으로 격식을 확정함

**연결:** M02, M05 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P014 오베르진·올드 골드

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 짙은 적보라와 누런 금속색의 차이로 성숙하고 장식적인 분위기를 만든다. 극장·향수·빈티지 살롱에 적합하다. 선명한 노랑보다 탁한 금색을 선택한다.

**관찰할 관계:** Muted warm metallic trim remains visible against the dark purple field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#432D46|an aubergine existing field|큰 바탕 예시|0.333536 / 0.051893|
|#B79755|old-gold existing trim|반사 강조|0.691447 / 0.093048|
|#E3D7C1|a parchment-colored existing surface|밝은 구별 영역|0.882967 / 0.032325|

**오인 경계:** 금속의 반사 대신 선명한 노랑 면을 쓰거나 보라색을 전역 조명으로 흘림

**연결:** M05 · P1

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P015 아이스 화이트·플래티넘

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 따뜻한 금색 대신 흰빛과 차가운 반사를 강조한다. 아르데코 패션의 화이트·크리스털·플래티넘 계열에서 착안한 주얼리·이브닝웨어용 조합이다.

**관찰할 관계:** Cool metallic reflection separates from the white field and darker steel-gray boundary.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F7F7F4|an ice-white existing field|큰 바탕 예시|0.975306 / 0.003964|
|#C3CBD0|silver-colored existing metal|반사 강조|0.837402 / 0.011238|
|#7D8992|a steel-gray existing edge|어두운 지지점|0.623291 / 0.019547|

**오인 경계:** 하얀 면과 은색 면이 합쳐지거나 회색 페인트를 플래티넘으로 판정함

**연결:** M02, M05 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P016 공작빛·골드

**계열:** 클래식·주얼리·장식: 어두운 바탕과 반사광의 대비

**설계 의도:** 휘슬러의 공작실 계열에서 착안했다. 청색과 녹색이 이어지는 바탕에 금빛 문양을 얹어 색의 깊이와 장식 밀도를 높인다.

**관찰할 관계:** The blue and green-teal regions stay distinct beneath bounded gold motifs.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#1E5964|a peacock-blue existing field|큰 바탕 예시|0.43105 / 0.062119|
|#3C786D|a green-teal existing surface|지지 영역|0.528918 / 0.065356|
|#C8AA61|gold-colored existing motifs|반사 강조|0.748937 / 0.098817|

**오인 경계:** 새·공작 깃털을 추가하거나 제안 팔레트를 공작실 원본 측정값으로 주장함

**연결:** M05, M07 · P1

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S09 Harmony in Blue and Gold: The Peacock Room](https://asia-archive.si.edu/object/F1904.61/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P017 네이비·화이트·레드

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 두 기본색으로 질서를 만들고 빨강을 작은 표식처럼 사용한다. 해안·마린 컨셉을 응용한 캐주얼 의상·여름 소품용. 흰 바탕, 남색 줄무늬, 작은 빨간 포인트로 역할을 나눈다.

**관찰할 관계:** Navy stripes repeat on white fabric while red remains a localized trim.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#18344C|navy existing stripes|반복 띠|0.315451 / 0.055033|
|#F5F4ED|white existing fabric|큰 바탕 예시|0.965992 / 0.009326|
|#C83B3B|a red existing trim|작은 강조|0.561146 / 0.178057|

**오인 경계:** 세 색의 균등 큰 면으로 줄무늬 관계를 지우거나 해안 장소를 강제함

**연결:** M07, M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P018 헤리티지 체크

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 버버리 체크의 색 관계에서 착안했다. 중성 바탕에 어두운 격자와 작은 붉은 선을 넣어 반복·전통·식별성을 설계한다. 색뿐 아니라 선의 굵기와 간격이 중요하다.

**관찰할 관계:** The colored line families cross on one beige carrier with distinct widths and spacing.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#C9AE8C|a beige existing checked surface|큰 바탕 예시|0.765736 / 0.055855|
|#242321|black existing grid lines|윤곽·경계|0.256472 / 0.003981|
|#F3EEE4|white existing grid lines|밝은 구별 영역|0.950265 / 0.014349|
|#A53533|thin red existing lines|작은 강조|0.493665 / 0.147912|

**오인 경계:** 색을 서로 다른 물체에 분산하거나 격자를 줄무늬로 치환함

**연결:** M07 · P1

**맥락 출처:** [S10 Burberry Check Card Case](https://int.burberry.com/check-card-case-p81163291)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P019 그린·레드 스트라이프

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 구찌의 녹색·빨강 스트라이프 사례에서 착안했다. 크림 바탕과 규칙적인 띠로 스포츠적 요소와 장식성을 결합한다. 큰 면보다 리본·띠·트리밍에 적합하다.

**관찰할 관계:** Green and red bands remain on the same ribbon-shaped region over the cream carrier.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#1E593E|green existing ribbon bands|반복 띠|0.417492 / 0.076417|
|#B33235|red existing ribbon bands|반복 띠|0.514949 / 0.165525|
|#F0E6D0|a cream existing carrier|큰 바탕 예시|0.927019 / 0.031121|

**오인 경계:** 띠 색을 전체 옷색으로 퍼뜨리거나 녹색·빨강만으로 실제 브랜드 소속을 확정함

**연결:** M07, M03 · P1

**맥락 출처:** [S11 Gucci luggage elastic Web band](https://www.gucci.com/ca/en/pr/women/travel-for-women/accessories-for-women/luggage-elastic-web-band-p-742436HAAC58980)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P020 아쿠아·화이트·실버

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 티파니의 브랜드색에서 착안했다. 밝은 청록, 흰 여백, 작은 금속 반사를 결합해 선물·보석·맑은 장식성을 설계한다.

**관찰할 관계:** Aqua packaging, white ribbon and small silver reflection occupy separate owners.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#81D0C5|an aqua existing package surface|큰 바탕 예시|0.80343 / 0.079757|
|#F8F8F2|a white existing ribbon|밝은 구별 영역|0.977477 / 0.007913|
|#BBC6CB|a silver-colored existing fitting|반사 강조|0.819556 / 0.014015|

**오인 경계:** 34번의 모래·바다 장면을 가져오거나 제안 아쿠아를 공식 Tiffany Blue로 주장함

**연결:** M05, M03 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S12 The Tiffany Blue Box](https://www.tiffany.com/world-of-tiffany/heritage/blue-box-story.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P021 오렌지·코코아·크림

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 에르메스의 오렌지 패키지에서 착안했다. 눈에 띄는 바탕을 갈색 선과 가죽색으로 정돈해 발랄함과 묵직함을 함께 남기는 응용이다.

**관찰할 관계:** The brown ribbon bounds the orange package against a light cream field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E87524|an orange existing package surface|큰 바탕 예시|0.684339 / 0.166418|
|#513A2B|a cocoa-brown existing ribbon|어두운 지지점|0.370148 / 0.040835|
|#F3E9D9|a cream existing ground|밝은 구별 영역|0.9376 / 0.023881|

**오인 경계:** 실제 상자 형태·공식 로고·진품을 색만으로 주장하거나 갈색을 가죽에 강제함

**연결:** M03 · P1

**맥락 출처:** [S13 Hermès Orange boxes FAQ](https://www.hermes.com/us/en/faq/products/orange-boxes/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P022 네이비·버건디·머스터드

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 어두운 두 색을 바탕으로 노랑을 작은 표식처럼 넣는 프레피풍 설계. 니트·타이·엠블럼·체크에 적합하다. 모든 색을 같은 폭으로 반복하지 않는 편이 좋다.

**관찰할 관계:** Unequal bounded bands retain a small mustard accent within darker cloth.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#26354B|navy existing cloth|큰 바탕 예시|0.32614 / 0.04417|
|#783744|burgundy existing woven bands|지지 영역|0.426525 / 0.091611|
|#B9994D|mustard existing trim|작은 강조|0.696517 / 0.102429|
|#EDE2CB|a cream existing insert|밝은 구별 영역|0.915456 / 0.032823|

**오인 경계:** 모든 색을 같은 굵기로 반복하거나 학교·신분·엠블럼을 새로 추가함

**연결:** M07, M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P023 인디고·토바코·에크루

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 차가운 청색 직물과 따뜻한 갈색 가죽을 나누어 소재가 읽히는 일상성을 만든다. 데님·작업복풍 패션·여행 스냅에 적합하다.

**관찰할 관계:** Indigo cloth, warm brown leather and light ecru remain separate local colors.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#244364|indigo existing denim|큰 바탕 예시|0.375344 / 0.067979|
|#A76D40|tobacco-brown existing leather|지지 영역|0.586983 / 0.09565|
|#E9DFC8|ecru existing cloth|밝은 구별 영역|0.905514 / 0.032515|

**오인 경계:** 데님을 파란 빛으로 대체하거나 모든 갈색을 목재로 바꿈

**연결:** M02, M05 · P1

**맥락 출처:** [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P024 검정·시그널 오렌지·실버

**계열:** 패션·브랜드에서 출발한 조합

**설계 의도:** 무거운 기본색 위에 선명한 색을 기능 표식처럼 사용하는 테크니컬 스포츠 설계. 오렌지는 지퍼·파이핑·장비 부품에 모아 기능과 연결한다.

**관찰할 관계:** Orange stays on the bounded functional trim while metal retains separate highlights.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#20252A|a black existing technical surface|큰 바탕 예시|0.261587 / 0.011864|
|#FF6937|signal-orange existing piping|작은 강조|0.702097 / 0.19382|
|#C7CED2|silver-colored existing fittings|반사 강조|0.847172 / 0.009497|

**오인 경계:** 주황 네온으로 변환하거나 기능색 때문에 지퍼·장비를 추가함

**연결:** M03, M05 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P025 세이지·크림·우드

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 잎·밝은 직물·나무를 각각 한 색으로 정리한 부드러운 보태니컬 컨셉. 식물 사진·생활용품·주거 공간에 적합하다. 녹색을 과하게 선명하게 만들지 않는다.

**관찰할 관계:** Muted foliage, light cloth and wood retain separate local colors.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#9EAE96|sage-colored existing foliage|지지 영역|0.731547 / 0.038336|
|#F0EADB|cream existing cloth|큰 바탕 예시|0.937679 / 0.02096|
|#A7815D|warm-brown existing wood|중간 밝기|0.631171 / 0.068731|

**오인 경계:** 세이지를 밝은 형광 녹색으로 바꾸거나 녹색 틴트로 모든 재료를 덮음

**연결:** M02, M13 · P1

**맥락 출처:** [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P026 올리브·카키·본

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 중저채도색으로 장식보다 실용성과 환경 적응성을 강조한다. 필드웨어·캠핑·탐험 컨셉에 적합하다. 밝은 색은 안감·셔츠·장비 라벨로 분리한다.

**관찰할 관계:** A light lining separates the two muted olive and khaki regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#596144|olive existing outer fabric|큰 바탕 예시|0.477364 / 0.045472|
|#A89F74|khaki existing equipment|중간 밝기|0.699341 / 0.059897|
|#E6DDC6|bone-colored existing lining|밝은 구별 영역|0.8986 / 0.032215|

**오인 경계:** 군인·전투·위장무늬를 색 조합만으로 추가하거나 밝은 안감을 숨김

**연결:** M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P027 테라코타·세이지·석회색

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 붉은 흙과 회녹색을 대비시키고 밝은 벽색으로 연결한다. 지중해풍 공간의 화분·정원·스투코 벽 관계를 응용한 배색이다.

**관찰할 관계:** The warm pottery and muted foliage remain separate against the pale wall.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#BC7056|terracotta-colored existing pottery|지지 영역|0.622584 / 0.104065|
|#889C7B|sage-colored existing foliage|지지 영역|0.66789 / 0.052584|
|#EEE3D0|a pale limestone-colored existing wall|큰 바탕 예시|0.919486 / 0.028009|

**오인 경계:** 같은 세 색을 천에 놓고 원래 화분·벽의 관계를 충족했다고 주장함

**연결:** M02 · P0

**맥락 출처:** [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P028 포레스트·월넛·리넨

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 잎 그늘·어두운 목재·밝은 직물을 대비시킨 숲속 은신처 컨셉. 숙소·독서 장면·자연 제품에 적합하다. 어두운 두 색 사이에 리넨을 끼운다.

**관찰할 관계:** Light cloth divides the two darker green and brown material regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#294F3D|forest-green existing foliage|큰 바탕 예시|0.393428 / 0.053769|
|#67472F|walnut-brown existing wood|어두운 지지점|0.427455 / 0.057185|
|#E5DBC7|linen-colored existing cloth|밝은 구별 영역|0.894057 / 0.028941|

**오인 경계:** 어두운 초록·갈색이 뭉치거나 색만으로 숲속 숙소를 확정함

**연결:** M02 · P1

**맥락 출처:** [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials), [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P029 모스·머스터드·러스트

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 녹색·노랑·주황을 모두 탁하게 눌러 같은 자연 소재군처럼 연결한다. 빈티지 야외복·식물 표본·거친 종이 패키지에 적합하다.

**관찰할 관계:** All three hue regions remain muted while their boundaries stay readable.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#68724B|moss-green existing cloth|큰 바탕 예시|0.533147 / 0.058712|
|#B6943C|muted mustard existing detail|지지 영역|0.68123 / 0.112939|
|#A25738|rust-colored existing surface|지지 영역|0.53931 / 0.108523|

**오인 경계:** 러스트색을 실제 부식으로 단정하거나 채도를 올려 현대 원색 스포츠로 바꿈

**연결:** M03 · P1

**맥락 출처:** [S21 Color Through the Decades: 1970s](https://www.sherwin-williams.com/painting-contractors/color-collections/color-through-the-decades/1970s)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P030 샌드·인디고·클레이

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 넓은 따뜻한 흙빛 속에 작은 청색을 넣어 시각적인 쉼표를 만든다. 건조한 지형·염색 직물·여행 컨셉에 적합하다. 남색은 천·문·소품에 집중한다.

**관찰할 관계:** A small indigo region interrupts the larger warm sand and clay fields.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#DDC7A4|a sand-colored existing field|큰 바탕 예시|0.839194 / 0.052906|
|#2D4267|a bounded indigo existing cloth|작은 강조|0.37985 / 0.069055|
|#B77C61|a clay-colored existing object|지지 영역|0.640278 / 0.083596|

**오인 경계:** 남색을 전체 배경으로 넓히거나 사막·여행 사건을 추가함

**연결:** M03, M12 · P1

**맥락 출처:** [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P031 유칼립투스·스톤·차콜

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 녹색의 생동감을 누르고 돌색과 연결한 차분한 자연성. 스파·욕실·무광 용기·우천 장면에 적합하며 물·유리의 반사를 보태기 좋다.

**관찰할 관계:** Muted green remains distinct from pale gray and dark boundaries.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#78978B|a muted eucalyptus-green existing surface|지지 영역|0.649199 / 0.039018|
|#C8CDC5|a stone-gray existing field|큰 바탕 예시|0.842138 / 0.012217|
|#343F3C|a charcoal existing edge|어두운 지지점|0.356641 / 0.015389|

**오인 경계:** 스파·치유 효과를 색으로 주장하거나 모든 면에 녹색 워시를 적용함

**연결:** M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P032 오프화이트·오크·먹색

**계열:** 자연·흙·식물: 색을 실제 소재와 연결하는 조합

**설계 의도:** 밝은 바탕·나무·가는 어두운 선을 분리하는 따뜻한 미니멀 설계. 수공예 소품과 단순한 공간에 적합하다. 먹색은 프레임과 윤곽에 제한한다.

**관찰할 관계:** Dark frames remain thin while the light field and warm wood lead.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F0E9DA|an off-white existing wall|큰 바탕 예시|0.935453 / 0.021341|
|#B89B72|oak-colored existing wood|중간 밝기|0.705577 / 0.065553|
|#30322C|thin ink-dark existing frames|윤곽·경계|0.313032 / 0.010818|

**오인 경계:** 먹색을 큰 면으로 확대하거나 색만으로 실제 오크 수종을 확정함

**연결:** M03 · P0

**맥락 출처:** [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials), [S18 Hygge Color Palette Ideas](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/hygge-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P033 코발트·화이트·테라코타

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 밝은 벽, 푸른 문·바다, 흙빛 바닥의 분리에서 착안한 또렷하고 건조한 휴양 컨셉. 강한 햇빛과 단순한 건축면에 적합하다.

**관찰할 관계:** Three architectural owners retain distinct blue, light and earth-colored surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#2855A3|a cobalt-blue existing door|지지 영역|0.461868 / 0.135722|
|#F5F0E3|a white existing wall|큰 바탕 예시|0.955493 / 0.018038|
|#C77D5D|a terracotta-colored existing floor|지지 영역|0.660614 / 0.10301|

**오인 경계:** 파랑을 하늘이나 의상으로 옮기거나 전통 지역 건축을 진위로 확정함

**연결:** M03, M12 · P0

**맥락 출처:** [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P034 아쿠아·모래·화이트

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 바다빛·모래빛·여백을 가볍게 연결한 공기감 있는 해안. 짙은 남색 마린룩보다 부드러운 휴식 장면에 적합하다.

**관찰할 관계:** The soft aqua, sand and light cloth regions remain distinct without a dark marine anchor.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#8BC9C3|an aqua existing water region|지지 영역|0.792147 / 0.064008|
|#DCC9A7|a sand-colored existing shore|지지 영역|0.842973 / 0.050189|
|#F7F4E9|a white existing cloth|밝은 구별 영역|0.966468 / 0.014888|

**오인 경계:** 20번의 포장·리본 배치를 가져오거나 같은 색상만으로 같은 컨셉이라고 판정함

**연결:** M02 · P0

**맥락 출처:** [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P035 코발트·레몬·오프화이트

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 차가운 진한 파랑과 밝은 노랑의 차이를 흰 바탕으로 완충한다. 레몬 소품·여름 의상·활기찬 제품에 적합하다.

**관찰할 관계:** A light field separates the vivid blue object and smaller yellow detail.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#2454C5|a cobalt-blue existing object|지지 영역|0.484859 / 0.184292|
|#F1D84B|a lemon-yellow existing detail|작은 강조|0.878564 / 0.156813|
|#F6F1DD|an off-white existing background|큰 바탕 예시|0.956706 / 0.026885|

**오인 경계:** 색상환을 선언하지 않고 수학적 보색이라 부르거나 레몬 과일을 추가함

**연결:** M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P036 피치·라벤더·페리윙클

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 따뜻한 낮에서 차가운 밤으로 넘어가는 시간의 흐름을 설계한다. 하늘·그라데이션·몽환적 배경에 적합하며 피치는 광원 근처에 둔다.

**관찰할 관계:** The three color regions connect smoothly along the declared sky path.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#ECA783|a peach existing upper sky region|공간 경로 끝점|0.786062 / 0.095419|
|#B79CCC|a lavender existing sky transition|전이 영역|0.732953 / 0.074145|
|#7E91BE|a periwinkle existing lower sky region|공간 경로 끝점|0.658672 / 0.070873|

**오인 경계:** 순서 없는 색 블록이나 명도 기반 후반 맵으로 공간 경로를 대체함

**연결:** M09 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S04 CSS Color Module Level 4](https://www.w3.org/TR/2026/CRD-css-color-4-20260930/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P037 벚꽃색·연두·아이보리

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 꽃과 새잎을 모두 연하게 잡아 개화·시작·가벼운 생명감을 표현한다. 봄 소품·피크닉·밝은 인물 촬영에 적합하다.

**관찰할 관계:** Pale pink petals and green leaves stay separate against the light neutral field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E8B4BC|pale blossom-pink existing petals|지지 영역|0.819098 / 0.061171|
|#B8C994|pale spring-green existing leaves|지지 영역|0.809544 / 0.073748|
|#F6EFDE|an ivory existing ground|큰 바탕 예시|0.953032 / 0.023703|

**오인 경계:** 분홍·녹색으로 계절이나 개화 시점을 확정하거나 새 꽃을 추가함

**연결:** M02, M13 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P038 러스트·머스터드·와인

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 따뜻한 세 색을 명도로 나누어 풍성하고 숙성된 가을을 설계한다. 니트·수확 장면·저녁 만찬에 적합하며 와인이 어두운 지지점이 된다.

**관찰할 관계:** The wine region provides a darker bounded anchor among warmer earth colors.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B65D36|a rust-colored existing surface|지지 영역|0.577413 / 0.126928|
|#C69E3D|a mustard existing object|중간 밝기|0.718356 / 0.122346|
|#693844|wine-colored existing cloth|어두운 지지점|0.405879 / 0.070826|

**오인 경계:** 가을·수확 사건을 자동 추가하거나 와인색을 실제 음료로 치환함

**연결:** M02 · P1

**맥락 출처:** [S21 Color Through the Decades: 1970s](https://www.sherwin-williams.com/painting-contractors/color-collections/color-through-the-decades/1970s)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P039 아이스 블루·네이비·실버

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 밝고 차가운 큰 면과 짙은 선으로 눈·얼음·겨울밤을 대비시킨다. 겨울 스포츠·주얼리·차가운 풍경에 적합하다.

**관찰할 관계:** The navy boundary keeps pale blue and silver reflection from merging.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#D8EAF1|an ice-blue existing field|큰 바탕 예시|0.925755 / 0.021385|
|#23354B|a navy existing edge|어두운 지지점|0.32404 / 0.045953|
|#A9B9C5|silver-colored existing metal|반사 강조|0.77719 / 0.024661|

**오인 경계:** 실버를 얼음으로 대체하거나 색만으로 겨울 스포츠 장면을 추가함

**연결:** M02, M05 · P1

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P040 포레스트·레드·골드·크림

**계열:** 해안·날씨·계절: 장소와 시간대를 암시하는 조합

**설계 의도:** 짙은 잎색에 붉은 장식과 따뜻한 반짝임을 얹는 겨울 축제 컨셉. 선물·리스·연말 식탁에 적합하다. 금색은 작은 반짝임으로 남긴다.

**관찰할 관계:** The red accent and small gold reflections remain bounded within darker green and cream regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#205340|forest-green existing foliage|큰 바탕 예시|0.4015 / 0.063981|
|#B73735|a red existing ornament|작은 강조|0.527059 / 0.164968|
|#C6A354|gold-colored existing detail|반사 강조|0.730965 / 0.106303|
|#F0E6CD|cream existing cloth|밝은 구별 영역|0.926283 / 0.034797|

**오인 경계:** 빨강·초록만으로 특정 축제·종교·날짜를 확정하거나 새 장식을 추가함

**연결:** M03, M05 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P041 로즈 쿼츠·세레니티

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 팬톤 2016년 두 색에서 착안했다. 따뜻한 분홍과 차가운 연파랑을 동등하게 놓아 부드러운 균형을 만든다. 당시 선정에는 관습적인 색 연상을 재고하려는 의도도 있었다.

**관찰할 관계:** The pink and blue surfaces stay distinct at similarly gentle chroma.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#EFC6CA|a soft rose-pink existing surface|지지 영역|0.86304 / 0.046871|
|#99ACD4|a soft blue existing surface|지지 영역|0.743808 / 0.061816|
|#F4F1EB|an off-white existing field|밝은 구별 영역|0.958802 / 0.008608|

**오인 경계:** 색을 성별·연령에 자동 배정하거나 제안 HEX를 공식 팬톤 값으로 삼음

**연결:** M02 · P0

**맥락 출처:** [S14 Pantone 2016 Rose Quartz and Serenity](https://www.pantone.com/eu/en-eu/articles/press-releases/pantone-reveals-color-of-the-year-for-2016-pantone-15-3919-serenity-and-pantone-13-1520-rose-quartz)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P042 라벤더·버터 옐로

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 보라와 노랑의 색 차이를 낮은 채도로 누그러뜨린 가벼운 장난스러움. 귀엽지만 지나치게 영아용처럼 보이지 않는 소품·패키지용 설계다.

**관찰할 관계:** Muted lavender and pale yellow remain separate across a light cream field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#BDA5D5|a lavender existing surface|지지 영역|0.758908 / 0.072335|
|#F0DF9E|a butter-yellow existing surface|지지 영역|0.902384 / 0.084949|
|#F7F0DD|a cream existing field|밝은 구별 영역|0.955533 / 0.026167|

**오인 경계:** 둘 다 옅다는 이유로 경계가 없어도 통과하거나 영아용 디자인을 강제함

**연결:** M02, M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S03 Color and emotion: hue, saturation, and brightness](https://pubmed.ncbi.nlm.nih.gov/28612080/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P043 민트·피치·밀크

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 차가운 잎빛과 따뜻한 과육빛을 고명도로 맞춰 신선함과 친근함을 함께 표현한다. 생활·뷰티 제품과 부드러운 무광 소재에 적합하다.

**관찰할 관계:** The cool and warm pale regions retain their local boundaries.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B6DBCA|a mint existing surface|지지 영역|0.85996 / 0.045483|
|#F0BEA5|a peach existing surface|지지 영역|0.839751 / 0.067116|
|#F8F1E5|a milk-colored existing field|밝은 구별 영역|0.960335 / 0.017601|

**오인 경계:** 실제 신선도·친근한 성격·위생을 색만으로 주장함

**연결:** M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S03 Color and emotion: hue, saturation, and brightness](https://pubmed.ncbi.nlm.nih.gov/28612080/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P044 더스티 로즈·토프

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 분홍의 채도를 줄이고 회갈색을 결합한 성숙한 로맨스. 꽃 장식·침실·차분한 인물 사진에 적합하며 주름과 직물의 결로 풍부함을 만든다.

**관찰할 관계:** Muted pink cloth remains separate from gray-brown and ivory surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#BE9398|dusty-rose existing cloth|지지 영역|0.704977 / 0.052245|
|#96877E|a taupe existing surface|중간 밝기|0.634181 / 0.022558|
|#F0E6D9|an ivory existing field|밝은 구별 영역|0.929302 / 0.020507|

**오인 경계:** 전역 분홍 필터로 회갈색을 지우거나 연령·로맨스를 확정함

**연결:** M02, M05 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P045 블러시·로즈·와인

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 분홍 계열 하나를 명도 세 층으로 나누는 단색조 설계. 밝은색이 많으면 부드럽고, 와인색이 많으면 성숙하고 무거워진다.

**관찰할 관계:** Three tonal tiers within the selected pink-red family remain readable.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F0CED0|a blush existing field|밝은 구별 영역|0.880647 / 0.038352|
|#C5798B|a rose-colored existing surface|중간 밝기|0.661958 / 0.097077|
|#703545|a wine-colored existing detail|어두운 지지점|0.41136 / 0.085105|

**오인 경계:** 모든 면을 같은 분홍으로 합치거나 어두운 색 비중을 고정함

**연결:** M01, M02 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P046 모브·블루그레이·실버

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 붉은 기운과 푸른 기운을 회색으로 감싸는 차가운 로맨스. 새벽·안개·새틴·조용한 감정 장면에 적합하다.

**관찰할 관계:** Gray-biased colored surfaces remain distinct from localized silver reflection.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B49BAC|mauve existing satin|지지 영역|0.71686 / 0.03765|
|#8D9EAD|a blue-gray existing field|지지 영역|0.690853 / 0.029351|
|#D0D6D9|silver-colored existing metal|반사 강조|0.872339 / 0.007756|

**오인 경계:** 새틴 광택과 금속 반사를 같은 물질로 판정하거나 차가운 감정을 의무화함

**연결:** M02, M05 · P1

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P047 피스타치오·로즈·바닐라

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 회녹색과 분홍의 대비를 노란 크림색으로 묶는 복고적 부드러움. 디저트·꽃·세라믹에 적합하며 지나친 사탕색을 피하기 쉽다.

**관찰할 관계:** The warm cream field connects two bounded muted hue regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B7C591|a pistachio-green existing surface|지지 영역|0.799519 / 0.071769|
|#D8A0AC|a muted rose existing surface|지지 영역|0.761781 / 0.068153|
|#F3E7C8|a vanilla-colored existing field|큰 바탕 예시|0.929512 / 0.042784|

**오인 경계:** 사탕처럼 과도하게 선명하게 만들거나 디저트·꽃을 무조건 추가함

**연결:** M02, M13 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P048 파스텔 캔디 믹스

**계열:** 파스텔·로맨스·뷰티: 부드럽지만 서로 다른 방향의 조합

**설계 의도:** 서로 다른 색의 밝기와 채도를 비슷하게 맞춰 가벼운 다채로움을 만든다. 놀이·팬시·판타지용. 색은 별도 블록으로 나누는 편이 의도가 명확하다.

**관찰할 관계:** Four bounded color blocks retain comparable soft chroma.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#EDBDD3|a pastel pink existing block|독립 색면|0.847133 / 0.061758|
|#C8BCE8|a pastel lavender existing block|독립 색면|0.819509 / 0.062335|
|#F3E7A5|a pale lemon existing block|독립 색면|0.922205 / 0.085022|
|#BCE0D0|a pastel mint existing block|독립 색면|0.876251 / 0.043732|

**오인 경계:** 네 색을 연속 그라데이션으로 합치거나 동일 명도·면적을 의무 수치로 만듦

**연결:** M02, M07 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P049 초콜릿·캐러멜·크림

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 원재료의 갈색과 유제품색을 연결하는 풍부한 디저트 컨셉. 진한 초콜릿, 구운 표면, 부드러운 크림을 각각 분리한다.

**관찰할 관계:** The three ingredient regions retain distinct brown and cream local colors.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#4F3029|an existing chocolate region|어두운 지지점|0.345166 / 0.047412|
|#C2874D|an existing caramel region|중간 밝기|0.670567 / 0.103973|
|#F2E2C4|an existing cream region|밝은 구별 영역|0.917912 / 0.043272|

**오인 경계:** 같은 팔레트를 가죽·목재에 적용하고 식품 재료가 충족됐다고 판정함

**연결:** M13, M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P050 에스프레소·코발트·크림

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 익숙한 커피색 사이에 차가운 파랑을 삽입해 전통 카페와 구별되는 현대성을 만든다. 파랑은 식품보다 컵·간판·그래픽에 배치한다.

**관찰할 관계:** Blue belongs to the cup while the beverage and cream keep separate food colors.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#372C27|an espresso-brown existing drink|어두운 지지점|0.30376 / 0.018559|
|#3A58C8|a cobalt-blue existing cup|작은 강조|0.504074 / 0.177545|
|#EFE5D2|an existing cream region|밝은 구별 영역|0.924738 / 0.027511|

**오인 경계:** 코발트를 식품 자체에 옮기거나 컵 없는 장면에 컵을 만들어 추가함

**연결:** M13, M03 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P051 토마토·바질·모차렐라

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 빨강·초록·크림색을 실제 재료와 연결한 신선한 조리 장면. 밝은 접시, 붉은 주재료, 작은 잎 무리로 역할을 나눈다.

**관찰할 관계:** Tomato, basil and mozzarella retain separate ingredient boundaries.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#D84A3C|an existing red tomato region|큰 바탕 예시|0.604084 / 0.180408|
|#438447|existing green basil leaves|작은 강조|0.554423 / 0.113829|
|#F3EFDE|an existing pale mozzarella region|밝은 구별 영역|0.950665 / 0.022877|

**오인 경계:** 빨강·초록·크림색만으로 원재료·맛·안전성을 확정함

**연결:** M13 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P052 말차·크림·팥색

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 녹색과 붉은 갈색을 서로 다른 재료로 읽히게 하는 차·제과 컨셉. 팥색을 작게 두어 녹색 주제가 흐려지지 않게 한다.

**관찰할 관계:** The smaller red-brown ingredient stays distinct from the larger green and cream regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#839957|an existing matcha-green region|큰 바탕 예시|0.649842 / 0.09419|
|#F0E5CC|an existing cream region|밝은 구별 영역|0.924068 / 0.035176|
|#824A51|an existing reddish-brown bean region|작은 강조|0.477304 / 0.076429|

**오인 경계:** 녹색으로 말차·건강효과를 단정하거나 팥색 면적을 주재료보다 크게 바꿈

**연결:** M13, M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P053 레드·옐로·크림

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 따뜻한 고채도색을 큰 블록으로 써 빠르게 읽히는 캐주얼 간식 컨셉을 만든다. 식욕 효과를 보장하는 조합이라기보다 시각적인 활기와 명확성이 목적이다.

**관찰할 관계:** The warm vivid panels remain bounded by a lighter package field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#DD3F32|a red existing package panel|독립 색면|0.599644 / 0.196883|
|#F3CA37|a yellow existing package panel|독립 색면|0.851071 / 0.159354|
|#FFF1CF|a cream existing package field|밝은 구별 영역|0.96057 / 0.046763|

**오인 경계:** 식욕·매출 효과를 단정하거나 포장을 식품 국소색으로 대체함

**연결:** M03, M07 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S03 Color and emotion: hue, saturation, and brightness](https://pubmed.ncbi.nlm.nih.gov/28612080/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P054 오렌지·레몬·라임

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 노랑을 연결색으로 사용해 감귤류의 산뜻한 원재료 단서를 만든다. 음료·여름 그래픽에 적합하다. 경계가 흐리면 흰 간격으로 분리한다.

**관찰할 관계:** Three existing citrus regions retain separate local hue boundaries.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F58C32|an existing orange-colored citrus region|지지 영역|0.739333 / 0.160532|
|#F0D848|an existing lemon-yellow citrus region|지지 영역|0.877439 / 0.158717|
|#9EBB44|an existing lime-green citrus region|지지 영역|0.746869 / 0.148122|

**오인 경계:** 세 과일을 새로 생성하거나 경계가 없는 음료색만으로 세 재료를 주장함

**연결:** M13, M07 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P055 베리·로즈·크림

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 진한 과즙에서 우유와 섞인 연한 색으로 이어지는 농도 차이를 표현한다. 베리 디저트·잼·립 제품에 적합하다.

**관찰할 관계:** Dark berry, mixed pink and light cream remain distinct visible regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#9B315C|an existing deep-berry region|어두운 지지점|0.482267 / 0.145697|
|#DA99B4|an existing rose-colored mixed region|중간 밝기|0.753751 / 0.084842|
|#F4E7D7|an existing cream region|밝은 구별 영역|0.93399 / 0.025596|

**오인 경계:** 색 농담만으로 실제 배합량·맛·농도를 측정했다고 주장함

**연결:** M13, M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P056 블루베리·버터·밀크

**계열:** 음식·원재료: 추상적인 심리보다 ‘무엇으로 만들었는지’를 전달하는 조합

**설계 의도:** 푸른 보라색 과실과 노란 구움색을 대비시켜 두 재료의 차이를 강조한다. 베이커리·브런치·패키지에 적합하다.

**관찰할 관계:** Blue-purple fruit remains separate from the yellow baked region and pale milk.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#4B4E8A|an existing blue-purple berry region|어두운 지지점|0.450375 / 0.097147|
|#E3C775|an existing butter-yellow baked region|중간 밝기|0.836035 / 0.106663|
|#F2EDDD|an existing milk-colored region|밝은 구별 영역|0.945683 / 0.021868|

**오인 경계:** 과일 표면과 구운 표면을 조명색으로 대체하거나 같은 대비로 원재료를 추정함

**연결:** M13, M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P057 삼원색·흑백 — De Stijl

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 데 스틸의 원색·직선·직각 구조에서 착안했다. 독립된 색면과 구조적 질서가 핵심이다. 백색은 큰 면, 검정은 경계, 원색은 크기가 다른 직사각형에 둔다.

**관찰할 관계:** Black orthogonal lines separate unequal primary-colored rectangular fields.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F5F2E8|a red existing rectangular field|독립 색면|0.960731 / 0.01363|
|#222222|a blue existing rectangular field|독립 색면|0.251965 / 0.0|
|#DA3B30|a yellow existing rectangular field|독립 색면|0.590541 / 0.197521|
|#F0CF38|black existing orthogonal lines|윤곽·경계|0.858231 / 0.161468|
|#2850A0|a white existing field|큰 바탕 예시|0.448586 / 0.137736|

**오인 경계:** 원색만 있고 직선·직각 관계가 없거나 De Stijl 전체를 이 한 도식으로 고정함

**연결:** M07 · P0

**맥락 출처:** [S16 MoMA Mondrian retrospective press release](https://www.moma.org/docs/press_archives/7380/releases/MOMA_1995_0060_46.pdf)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P058 레드·블랙·종이색

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 제한된 색 수와 큰 명도 차를 결합한 선언적 그래픽. 대각선·큰 제목·단순한 기하 도형을 사용하는 구성주의풍 응용 설계다.

**관찰할 관계:** The red graphic and black lines remain bounded on the paper carrier.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#C8332D|a red existing graphic shape|작은 강조|0.551654 / 0.186816|
|#232220|black existing graphic lines|윤곽·경계|0.252286 / 0.003997|
|#E8D9BA|a paper-colored existing carrier|큰 바탕 예시|0.889439 / 0.044323|

**오인 경계:** 구성주의 이름만으로 정치 선전·대각선·문구를 새로 추가함

**연결:** M07, M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P059 핑크·터쿼이즈·노랑·검정

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 유채색의 충돌을 검은 선과 패턴으로 묶는 멤피스풍 팝 설계. 장난스럽고 일부러 불균형한 화면에 적합하다. 점·지그재그·색면을 분리한다.

**관찰할 관계:** Distinct vivid shapes remain separated by bounded black pattern lines.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E88FA9|a pink existing shape|독립 색면|0.749107 / 0.111699|
|#49B8B2|a turquoise existing shape|독립 색면|0.717925 / 0.100407|
|#F2CE51|a yellow existing shape|독립 색면|0.85991 / 0.145812|
|#272527|black existing patterned lines|윤곽·경계|0.267412 / 0.004669|

**오인 경계:** 색 네 개만으로 Memphis를 확정하거나 점·지그재그를 다른 carrier로 옮김

**연결:** M07 · P1

**맥락 출처:** [S17 Memphis](https://designmuseum.org/memphis)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P060 아보카도·머스터드·번트 오렌지

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 따뜻한 복고 계열에서 착안했다. 선명한 원색 대신 누렇게 탁해진 색을 겹쳐 우드·코듀로이·기하 패턴의 재질감을 연결한다.

**관찰할 관계:** Muted warm-biased colored regions preserve their existing texture boundaries.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#788349|avocado-green existing cloth|큰 바탕 예시|0.586809 / 0.081914|
|#C5A144|a mustard existing surface|중간 밝기|0.724078 / 0.118335|
|#C5713E|a burnt-orange existing detail|지지 영역|0.632448 / 0.124841|
|#694C38|a brown existing wood region|어두운 지지점|0.442497 / 0.050139|

**오인 경계:** 색만으로 촬영 연대를 1970년대로 판정하거나 현대 원색으로 치환함

**연결:** M03, M05 · P1

**맥락 출처:** [S21 Color Through the Decades: 1970s](https://www.sherwin-williams.com/painting-contractors/color-collections/color-through-the-decades/1970s)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P061 터쿼이즈·코럴·크림

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 차가운 청록과 따뜻한 산호색을 크림으로 완충한 밝은 복고 공간. 둥근 가구·크롬·타일·다이너풍 장면에 적합하다.

**관찰할 관계:** Cream separates the turquoise and coral regions into readable surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#73BDB6|a turquoise existing surface|지지 영역|0.748023 / 0.074859|
|#E18A7B|a coral existing surface|지지 영역|0.720798 / 0.10952|
|#F3E6CC|a cream existing field|큰 바탕 예시|0.928492 / 0.03714|

**오인 경계:** 둥근 가구·크롬·다이너 장소를 배색 자체의 필수 의미로 만듦

**연결:** M03 · P1

**맥락 출처:** [S20 Midcentury Modern Color Palette](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/midcentury-modern-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P062 블루그레이·오커·월넛

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 미드센추리 계열의 목재와 색면 관계에서 착안했다. 차가운 저채도색과 따뜻한 목재의 균형이 목적이며, 가는 다리와 단순한 가구 형태에 적합하다.

**관찰할 관계:** Cool gray-blue, warm ochre and brown wood remain separate local color regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#7D9B9C|a blue-gray existing field|큰 바탕 예시|0.667092 / 0.033447|
|#C19A4D|an ochre existing object|지지 영역|0.706767 / 0.106094|
|#78513A|walnut-colored existing wood|어두운 지지점|0.472019 / 0.063097|
|#EDE4D4|an off-white existing insert|밝은 구별 영역|0.921659 / 0.023492|

**오인 경계:** 색으로 미드센추리 진품·연대·목종을 확정하거나 가는 다리를 추가함

**연결:** M02, M05 · P1

**맥락 출처:** [S20 Midcentury Modern Color Palette](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/midcentury-modern-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P063 그레이·일루미네이팅 옐로

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 팬톤 2021년 조합의 견고함과 희망이라는 의도에서 착안했다. 차분한 기반과 밝은 개입을 나눈다. 노랑을 넓히면 차분함보다 발랄함이 커진다.

**관찰할 관계:** A bounded yellow region interrupts the gray field at the declared hierarchy.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#999B9B|a gray existing field|큰 바탕 예시|0.687836 / 0.002321|
|#F4DF4A|a bright-yellow existing object|작은 강조|0.895372 / 0.162948|
|#F1F0E9|an off-white existing insert|밝은 구별 영역|0.953976 / 0.009355|

**오인 경계:** 노랑을 강제로 반 면적에 배치하거나 희망·강인함이 자동으로 입증된다고 함

**연결:** M03 · P0

**맥락 출처:** [S15 Pantone 2021 Ultimate Gray and Illuminating](https://www.pantone.com/na/en-us/articles/color-of-the-year/color-of-the-year-2021)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P064 핑크·블루·종이색

**계열:** 그래픽·레트로·아트: 색을 질서 또는 충돌의 도구로 사용하는 조합

**설계 의도:** 두 잉크 같은 강한 유채색과 따뜻한 종이색만 사용하는 간결한 인쇄물 컨셉. 진·포스터·독립출판에 적합하다. 겹침과 미세한 어긋남을 효과로 보탤 수 있다.

**관찰할 관계:** Two printed hue regions retain separate shapes on the paper carrier.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E94A91|a pink existing printed shape|인쇄색 영역|0.650502 / 0.203764|
|#3D59C7|a blue existing printed shape|인쇄색 영역|0.50674 / 0.174103|
|#F2E7D1|a paper-colored existing carrier|큰 바탕 예시|0.930857 / 0.031495|

**오인 경계:** 두 색만으로 리소 인쇄 공정을 확정하거나 어긋남·겹침을 항상 강제함

**연결:** M07 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P065 틸·오렌지 — Teal & Orange

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 차가운 배경과 따뜻한 피사체를 나누는 한난 대비 설계. 인물과 환경을 서로 다른 층으로 읽히게 한다. 피부를 균일한 주황색으로 칠하는 방식은 피한다.

**관찰할 관계:** The warm subject region stays separate from the cooler background without recoloring unrelated skin regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#246D78|a teal existing background|큰 바탕 예시|0.495083 / 0.072129|
|#DC9562|a restrained orange existing subject region|피사체 영역|0.729688 / 0.108771|
|#192D34|a charcoal existing recess|어두운 지지점|0.283391 / 0.028822|

**오인 경계:** 물체 배색을 두 색 광원이나 split toning으로 대체하고 피부를 균일 주황색으로 칠함

**연결:** M08, M12 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S26 Adobe Add a Split Tone Effect](https://helpx.adobe.com/premiere-elements/desktop/applying-special-effects/add-split-tone-effect.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P066 블루·앰버 혼합광

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 푸른 외부광과 따뜻한 실내등이 공존하는 빛의 출처가 있는 장면. 창가와 전구를 다른 방향에 두면 색의 대비가 공간 구조와 연결된다.

**관찰할 관계:** Two colored light contributions follow their declared receiving geometry and occlusion.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#304F7A|a blue-lit existing receiving surface|차가운 색광의 수신 영역|0.424598 / 0.080958|
|#D6A05B|an amber-lit existing receiving surface|따뜻한 색광의 수신 영역|0.742603 / 0.107672|
|#22262C|a charcoal existing shaded region|어두운 지지점|0.267125 / 0.012616|

**오인 경계:** 파란 벽·주황 옷 두 개만으로 혼합광이 증명됐다고 하거나 Kelvin만으로 색광 hue를 주장함

**연결:** M08, M10 · P0

**맥락 출처:** [S24 Rosco Filter Facts](https://us.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf), [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P067 매트릭스 계열 녹색·먹색

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 영화에서 가상현실을 불편하고 인공적으로 보이게 하려던 녹색 틴트에서 착안했다. 녹색이 항상 자연·치유를 뜻하지 않는 실제 사례다.

**관찰할 관계:** A restrained green bias recurs across the declared tonal scope while shading remains readable.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#6B8F59|an existing dark tonal region|어두운 지지점|0.608956 / 0.087992|
|#172019|an existing green-biased midtone region|공통 보정 경향|0.232098 / 0.018649|
|#D3D8C7|an existing pale tonal region|밝은 구별 영역|0.873685 / 0.02357|

**오인 경계:** 녹색 물체 몇 개만으로 전역 틴트를 충족하거나 영화 모든 버전의 같은 색을 주장함

**연결:** M11 · P0

**맥락 출처:** [S22 The Matrix: Welcome to the Machine](https://theasc.com/article/flashback-the-matrix-cinematography/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P068 호텔 핑크·퍼플·버건디

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 《그랜드 부다페스트 호텔》의 분홍·보라 계열에서 착안했다. 응용할 때는 밝은 건축면과 어두운 의상색을 분리해 장난감 같은 격식을 설계한다.

**관찰할 관계:** The brighter pink architecture stays separate from darker purple cloth and burgundy detail.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E6A2B3|a pink existing architectural surface|큰 바탕 예시|0.782109 / 0.083205|
|#805B8D|purple existing cloth|지지 영역|0.52899 / 0.087563|
|#8C3D54|a burgundy existing detail|어두운 지지점|0.471301 / 0.109875|

**오인 경계:** 특정 영화 시대·장면의 공식 팔레트를 확정하거나 호텔·유니폼을 새로 추가함

**연결:** M02, M12 · P2

**맥락 출처:** [S23 Lights, Camera, Color With Wes Anderson’s Colorist](https://www.sherwin-williams.com/architects-specifiers-designers/inspiration/stir/SW-ART-STIR-WES-ANDERSON)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P069 허니·올리브·크림

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 노란 빛으로 화면을 묶되 녹색을 남겨 단순 세피아와 구별하는 따뜻한 동화적 일상. 오래된 집·정원·햇빛 드는 방에 적합하다.

**관찰할 관계:** A warm grade leaves the bounded olive region recognizable.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#D5AA62|an existing honey-biased lit region|공통 보정 경향|0.762007 / 0.103438|
|#6D774A|an existing olive region|보존할 국소색|0.54918 / 0.066225|
|#EFE0BE|an existing cream region|밝은 구별 영역|0.910082 / 0.047676|

**오인 경계:** 전역 세피아로 녹색을 지우거나 동화적 느낌을 물리적 시간·장소로 고정함

**연결:** M11, M02 · P1

**맥락 출처:** [S26 Adobe Add a Split Tone Effect](https://helpx.adobe.com/premiere-elements/desktop/applying-special-effects/add-split-tone-effect.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P070 인디고·라벤더·피치

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 차가운 밤색 안에 작고 따뜻한 인물 영역을 남기는 부드러운 야간 감정. 고립감뿐 아니라 연결감도 표현하려는 인물 사진에 적합하다.

**관찰할 관계:** The smaller warm subject contribution remains spatially separate from the cool night field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#263D69|an indigo-lit existing background|차가운 색광의 수신 영역|0.364622 / 0.08161|
|#8C7CAB|a lavender-lit existing receiving region|전이 영역|0.618222 / 0.071939|
|#DDA68F|a peach-lit existing subject region|따뜻한 색광의 수신 영역|0.770685 / 0.072909|

**오인 경계:** 피치색 피부 전체를 도색하거나 연결감·고립감을 색으로 확정함

**연결:** M10, M12 · P1

**맥락 출처:** [S24 Rosco Filter Facts](https://us.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf), [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P071 샌드·시안·러스트

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 건조한 땅과 차가운 하늘을 나누고 녹슨색으로 시간의 흔적을 넣는 햇빛에 바랜 모험 컨셉. 사막·로드 무비풍 장면에 적합하다.

**관찰할 관계:** Warm ground and cool sky remain separate around the bounded rusty-colored surface.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#DAB981|a sand-colored existing ground|큰 바탕 예시|0.801581 / 0.082105|
|#68ABB6|a cyan existing sky|지지 영역|0.700635 / 0.069892|
|#9E5738|a rust-colored existing surface|작은 강조|0.533708 / 0.103915|

**오인 경계:** 색만으로 모험·방치 이력·실제 산화를 단정하거나 세 면을 후반 필터로 합침

**연결:** M12 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S19 Mediterranean Paint Colors](https://www.benjaminmoore.com/en-us/project-ideas-inspiration/design-style/mediterranean-color-palette-ideas)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P072 흑백·단일 레드

**계열:** 영화·사진·조명: 피사체와 공간을 색으로 분리하는 조합

**설계 의도:** 대부분의 색을 제거하고 하나의 물체만 붉게 남기는 서사적 단서 강조. 빨강을 5% 이하부터 시도하고, 무엇을 보아야 하는지 하나로 읽히게 한다.

**관찰할 관계:** The declared scope is achromatic except for the same bounded red owner.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#282828|an existing dark neutral region|무채색 영역|0.276848 / 0.0|
|#DADAD3|an existing light neutral region|무채색 영역|0.886403 / 0.009453|
|#C63435|one existing red object|같은 owner의 유채색 예외|0.550055 / 0.182994|

**오인 경계:** 다른 면에 유채색이 남거나 저채도 배색을 완전 무채색 예외 처리와 같게 판정함

**연결:** M04 · P0

**맥락 출처:** [S26 Adobe Add a Split Tone Effect](https://helpx.adobe.com/premiere-elements/desktop/applying-special-effects/add-split-tone-effect.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P073 시안·마젠타·블랙

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 밝은 두 광원을 어두운 공간에 분리해 인공적인 밤을 설계한다. 네온 간판·공연·게임 분위기에 적합하다. 반사면과 역광으로 빛의 출처를 보여준다.

**관찰할 관계:** Cyan and magenta light footprints remain spatially distinguishable in the dark scene.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#35D6DE|a cyan-lit existing receiving region|차가운 색광의 수신 영역|0.800928 / 0.126088|
|#E642BC|a magenta-lit existing receiving region|따뜻한 색광의 수신 영역|0.655329 / 0.233139|
|#14152A|an existing dark background|어두운 지지점|0.206734 / 0.041384|

**오인 경계:** 네온색 물체 두 개를 광원으로 판정하거나 반사·역광의 source를 뒤바꿈

**연결:** M08, M10 · P0

**맥락 출처:** [S24 Rosco Filter Facts](https://us.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf), [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P074 퍼플·핫핑크·선셋 오렌지

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 어두운 보라에서 따뜻한 지평선으로 밝아지는 신스웨이브풍 복고 미래. 전자음악·가상의 해질녘·긴 수평선에 적합하다.

**관찰할 관계:** Color moves along a declared sky-to-horizon path.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#2C1750|a dark-purple existing sky region|공간 경로 끝점|0.269356 / 0.099249|
|#E34A9B|a hot-pink existing sky region|전이 영역|0.644727 / 0.20314|
|#F3A45C|an orange existing horizon region|공간 경로 끝점|0.782347 / 0.12864|

**오인 경계:** 신스웨이브 이름만으로 격자·스포츠카·해를 추가하거나 색 순서를 역전함

**연결:** M09 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S04 CSS Color Module Level 4](https://www.w3.org/TR/2026/CRD-css-color-4-20260930/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P075 일렉트릭 블루·라임

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 차가운 고채도색과 밝은 황록색을 대비시켜 날카로운 기술·운동 이미지를 만든다. 라임은 버튼·테두리·기능 표식에 제한한다.

**관찰할 관계:** The lime region stays confined to the selected trim against blue and dark fields.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#3455E8|an electric-blue existing field|큰 바탕 예시|0.522801 / 0.224106|
|#D0ED45|lime existing functional trim|작은 강조|0.895725 / 0.187219|
|#202833|a charcoal existing ground|어두운 지지점|0.274117 / 0.023451|

**오인 경계:** 라임을 전역광으로 퍼뜨리거나 버튼·운동 장비를 자동 생성함

**연결:** M03 · P0

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P076 먹색·포스퍼 그린

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 어두운 바탕에 한 가지 발광색을 집중하는 터미널·센서·계기 컨셉. 정보가 어둠에서 떠오르는 모습이 목적이다.

**관찰할 관계:** Green luminous marks belong to the display and keep the surrounding field dark.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#111C17|a dark existing display field|큰 바탕 예시|0.213941 / 0.018667|
|#6DCB84|green existing luminous marks|발광면|0.765904 / 0.135799|
|#D6E0D5|pale existing display labels|밝은 구별 영역|0.896009 / 0.018288|

**오인 경계:** 녹색 페인트나 전역 틴트로 발광면을 대체하거나 임의 데이터·코드를 추가함

**연결:** M08 · P1

**맥락 출처:** [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P077 옐로·블랙·시안

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 주의 표식 같은 노랑·검정 구조에 차가운 발광색을 더한 산업형 사이버 컨셉. 노랑은 구조와 표식, 시안은 디지털 부분에 배정한다.

**관찰할 관계:** The yellow painted region remains distinct from cyan display emission.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#E8D33F|yellow existing structural paint|지지 영역|0.859424 / 0.16027|
|#1B2129|a black existing structure|어두운 지지점|0.245376 / 0.017665|
|#4BC6D4|a cyan existing display|발광면|0.764152 / 0.108725|

**오인 경계:** 노랑·검정을 실제 주의 표지로 확정하거나 시안 발광을 노란 반사에 덧씌움

**연결:** M08, M15 · P1

**맥락 출처:** [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq), [S33 OSHA 1910.145](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.145)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P078 실버·아이스 블루·화이트

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 금속과 반투명 플라스틱 같은 차가운 표면을 밝게 연결하는 크롬·Y2K풍 설계. 색뿐 아니라 반사와 투명도를 함께 지정한다.

**관찰할 관계:** Metal reflection and light-transmitting plastic stay on separate existing surfaces.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B7C1C9|silver-colored existing metal|반사 강조|0.805584 / 0.015817|
|#A3D5EB|ice-blue existing translucent plastic|투과 표면|0.845435 / 0.06023|
|#F4F8F9|a white existing ground|밝은 구별 영역|0.976389 / 0.004466|

**오인 경계:** 한 회색 면으로 금속·투명 플라스틱을 모두 대체하거나 Y2K 연대·재료 조성을 확정함

**연결:** M05 · P0

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P079 라벤더·블루·코럴 그라데이션

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 차가운 디지털색과 따뜻한 종착점을 부드럽게 연결하는 친근한 미래감. 네온보다 순한 배경용이며, 글자는 별도 단색 영역에 배치한다.

**관찰할 관계:** The ordered colors connect along the same declared background surface.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#BA9EEB|a lavender existing background zone|공간 경로 끝점|0.752268 / 0.112095|
|#729DE6|a blue existing background zone|전이 영역|0.695361 / 0.117921|
|#EEB0A1|a coral existing background zone|공간 경로 끝점|0.81093 / 0.076132|

**오인 경계:** Viridis 수치 맵이나 서로 떨어진 색 블록으로 연속 공간 경로를 대신함

**연결:** M09 · P0

**맥락 출처:** [S04 CSS Color Module Level 4](https://www.w3.org/TR/2026/CRD-css-color-4-20260930/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P080 네이비·민트·화이트

**계열:** 사이버·디지털·기술: 발광색과 어둠의 관계

**설계 의도:** 짙은 구조색과 밝은 기능색을 나누는 정돈되고 친근한 기술 이미지. 서비스·기기·설명 그래픽에 적합하다. 민트는 본문보다 강조 면에 사용한다.

**관찰할 관계:** Mint occupies bounded functional regions within a dark-and-light structure.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#173B52|navy existing structure|어두운 지지점|0.337568 / 0.057779|
|#70CDB4|mint existing functional regions|작은 강조|0.783583 / 0.0968|
|#EDF7F3|a white existing field|큰 바탕 예시|0.967539 / 0.0118|

**오인 경계:** 민트색만으로 정보 계층·접근성을 입증하거나 서비스 문구·UI를 새로 추가함

**연결:** M03, M15 · P1

**맥락 출처:** [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P081 블랙·옥스블러드·본

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 붉은색을 깊게 눌러 피·가죽·오래된 직물의 시각적 연상을 선택적으로 사용하는 어두운 로맨스. 고딕·극장·벨벳 의상에 적합하다.

**관찰할 관계:** Deep red cloth remains distinct within the dark field around the light detail.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#171418|a black existing field|큰 바탕 예시|0.196571 / 0.009168|
|#612A34|oxblood-colored existing cloth|지지 영역|0.364386 / 0.080354|
|#DDD1BB|a bone-colored existing detail|밝은 구별 영역|0.864532 / 0.032483|

**오인 경계:** 옥스블러드색을 실제 피·폭력·가죽 기원으로 단정함

**연결:** M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S08 Art Deco fashion](https://www.vam.ac.uk/articles/art-deco-fashion)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P082 블랙·바이올렛·실버

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 따뜻한 붉은색 대신 보라와 차가운 금속을 결합하는 비현실적이고 차가운 고딕. 사슬·반지·테두리에 밝기를 집중한다.

**관찰할 관계:** Cool metal reflection separates from the dark violet and black regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#18151F|a black existing field|큰 바탕 예시|0.204054 / 0.020106|
|#694B91|violet existing cloth|지지 영역|0.476792 / 0.112959|
|#BFC1CC|silver-colored existing trim|반사 강조|0.812686 / 0.015507|

**오인 경계:** 사슬·반지·고딕 건물을 팔레트의 필수 부품으로 추가함

**연결:** M05 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P083 플럼·포레스트·앤티크 골드

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 비슷하게 어두운 보석색을 가까이 놓고 낡은 금속으로 윤곽을 만드는 풍부하지만 밝지 않은 퇴폐성. 벨벳·유화·어두운 목재에 적합하다.

**관찰할 관계:** The two dark hue regions remain separate around smaller warm metallic edges.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#58354E|plum-colored existing cloth|지지 영역|0.38048 / 0.062472|
|#294C3D|a dark forest-green existing field|큰 바탕 예시|0.384962 / 0.048625|
|#AE8C52|antique-gold existing trim|반사 강조|0.65914 / 0.086505|

**오인 경계:** 금속 윤곽 없이 색이 뭉치거나 퇴폐·성격·도덕성을 자동 확정함

**연결:** M02, M05 · P1

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P084 페일 그린·더티 화이트

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 밝고 깨끗해야 할 공간에 탁한 녹색과 어두운 모서리를 넣는 미묘한 불편함. 고립된 시설·빈 복도·정적인 호러 장면용 설계다.

**관찰할 관계:** Muted-green local surfaces remain distinct from off-white surfaces and darker recesses.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#BBC6A4|a pale muted-green existing surface|국소 표면색|0.808958 / 0.04793|
|#E5E1D4|a dirty-white existing field|밝은 구별 영역|0.909321 / 0.017951|
|#7C857C|a gray existing recess|어두운 지지점|0.606469 / 0.01707|

**오인 경계:** 병·오염·정신 상태를 색만으로 단정하거나 국소 녹색을 전역 필터로 바꾸고 밝은 장면 전체를 검게 만듦

**연결:** M02 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P085 러스트·먹색·더티 크림

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 산화된 금속·잔해·먼지색을 나누어 시간과 방치를 시각화한다. 폐공장·낡은 기계·폐허에 적합하며 녹과 벗겨짐의 경계를 강조한다.

**관찰할 관계:** Rust-colored and pale deposit regions follow their existing bounded surface pattern.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#995A3F|a rust-colored existing weathered region|국소 표면색|0.533361 / 0.092276|
|#292E2C|an ink-dark existing surface|어두운 지지점|0.295524 / 0.007879|
|#D7CFB8|a dirty-cream existing deposit region|밝은 구별 영역|0.854793 / 0.032258|

**오인 경계:** 실제 녹·방치 기간·재해 이력을 색만으로 확정하거나 녹색을 피부에 옮김

**연결:** M05 · P1

**맥락 출처:** [S07 PBRT 4: Scattering from Layered Materials](https://pbr-book.org/4ed/Light_Transport_II_Volume_Rendering/Scattering_from_Layered_Materials)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P086 네이비·스모크·페일 블루

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 따뜻한 색을 억제해 푸른 회색의 거리감을 만드는 설계. 비 오는 도시·이별·고요한 밤에 적합하다. 감정은 표정과 공간 구성으로 완성한다.

**관찰할 관계:** Cool gray-blue tonal tiers retain bounded depth regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#273747|a navy existing background|큰 바탕 예시|0.329981 / 0.035449|
|#7E8C96|a smoke-gray existing surface|중간 밝기|0.632107 / 0.022178|
|#C3D1D8|a pale-blue existing detail|밝은 구별 영역|0.852134 / 0.01809|

**오인 경계:** 비·이별·외로움 사건을 필수로 만들거나 회청색을 전역 틴트로 합침

**연결:** M02, M12 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P087 블랙·애시드 그린·퍼플

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 어둠 위에서 낯선 황록색과 보라를 충돌시키는 허구의 독성·변이·금지구역 컨셉. 실제 독성 여부를 뜻하는 과학적 색 분류는 아니다.

**관찰할 관계:** The bright yellow-green accent remains bounded against black and purple.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#191B21|a black existing field|큰 바탕 예시|0.222677 / 0.012087|
|#C0D63B|an acid-green existing detail|작은 강조|0.832518 / 0.173221|
|#714691|a purple existing surface|지지 영역|0.47694 / 0.123996|

**오인 경계:** 색을 실제 독성·변이·금지구역의 과학적 판정으로 사용함

**연결:** M03 · P1

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S03 Color and emotion: hue, saturation, and brightness](https://pubmed.ncbi.nlm.nih.gov/28612080/)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P088 딥 레드·네이비·바이올렛

**계열:** 다크·고딕·불안·퇴폐: 아름다움 외의 감정도 의도적으로 설계하는 조합

**설계 의도:** 차가운 어둠 안으로 붉은 빛이 침입하는 네오누아르 조명 설계. 밤거리·갈등·긴장·어두운 관능에 적합하다. 두 광원을 공간적으로 분리한다.

**관찰할 관계:** The red light contribution remains spatially separate from the cooler dark field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#B23745|a red-lit existing receiving region|따뜻한 색광의 수신 영역|0.521338 / 0.158326|
|#1E2B4A|a navy-lit existing background|차가운 색광의 수신 영역|0.294062 / 0.059483|
|#665179|a violet-lit existing receiving region|전이 영역|0.472309 / 0.067782|

**오인 경계:** 빨간 물체로 적색광을 대체하거나 갈등·폭력·관능을 색만으로 확정함

**연결:** M08, M10 · P0

**맥락 출처:** [S24 Rosco Filter Facts](https://us.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf), [S25 ARRI Orbiter FAQ](https://www.arri.com/en/lighting/led-spotlights/orbiter/faq)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P089 오방색

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 방위·오행 등 문화적 질서를 가진 다섯 색 체계에서 착안했다. 현대적인 블록·띠·의상에 응용하되, 정확한 상징 배치는 해당 맥락에 맞춰 확인한다.

**관찰할 관계:** All five stated color families remain visible on the selected bands.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#28568B|a blue existing band|분리 색띠|0.448027 / 0.100902|
|#BA3C35|a red existing band|분리 색띠|0.537652 / 0.163323|
|#D6AF3E|a yellow existing band|분리 색띠|0.769055 / 0.134783|
|#F1E9D6|a white existing band|분리 색띠|0.935231 / 0.026638|
|#272926|a black existing band|분리 색띠|0.277775 / 0.006125|

**오인 경계:** 청을 단일 HEX로 고정하거나 임의 띠 순서를 방위·오행의 정당한 배치로 주장함

**연결:** M14, M07 · P2

**맥락 출처:** [S27 Korean Cultural Centre India: Obangsaek](https://www.korea.net/Events/Overseas/view?articleId=23083)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P090 단청 계열

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 다색의 반복과 층위에서 착안한 건축적 리듬. 녹색 바탕, 붉은 세부, 청색·황토색 층을 나누는 응용안이며 전통 단청의 정확한 복원색은 아니다.

**관찰할 관계:** The stated colors follow the existing layered architectural motif.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#568568|a green existing architectural painted ground|큰 바탕 예시|0.574274 / 0.068329|
|#C56347|a vermilion existing painted detail|지지 영역|0.610634 / 0.132189|
|#467FA0|a blue existing painted band|분리 색띠|0.571252 / 0.078764|
|#D0AA55|an ochre existing painted band|분리 색띠|0.755263 / 0.112777|
|#E8DFCA|a white existing painted boundary|밝은 구별 영역|0.905194 / 0.029684|

**오인 경계:** 다섯 색만으로 전통 단청·시대·복원색·안료를 인증하거나 건축 부재를 새로 추가함

**연결:** M14, M07 · P2

**맥락 출처:** [S28 전통 단청안료의 과학적 조사·분석](https://portal.nrich.go.kr/kor/originalUsrView.do?info_idx=8716&menuIdx=1046)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P091 청자빛·회백색·먹색

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 연한 회녹색을 넓게 두고 어두운 선을 제한해 유약의 깊이와 여백을 강조한다. 도자기·차·공예품에 적합하며 부드러운 반사광을 보탠다.

**관찰할 관계:** The pale green vessel keeps curved highlight shading and a bounded darker motif.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#A5BDB0|a celadon-green existing glazed vessel|큰 바탕 예시|0.776435 / 0.031988|
|#E9ECE3|a gray-white existing field|밝은 구별 영역|0.938305 / 0.012382|
|#38443E|an ink-dark existing motif|어두운 지지점|0.373839 / 0.018645|

**오인 경계:** 연한 초록 페인트를 유약 깊이로 판정하거나 실제 소성·화학 조성을 단정함

**연결:** M06, M02 · P0

**맥락 출처:** [S29 Goryeo Celadon](https://www.metmuseum.org/ko/essays/goryeo-celadon), [S32 Celadon Ewer and Basin: National Museum of Korea](https://www.museum.go.kr/ENG/contents/E0401000000.do?relicRecommendId=1818770&schM=view)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P092 청화백자 블루·화이트

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 백색 몸체와 코발트 문양의 관계를 응용한 여백과 선묘 중심의 배색. 색 수를 늘리기보다 푸른색의 농담과 문양 밀도로 변화를 만든다.

**관찰할 관계:** Blue motif regions remain on the same white ceramic owner.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F2F1E6|an existing white porcelain body|큰 바탕 예시|0.955911 / 0.014601|
|#28558B|an existing cobalt-blue painted motif|문양 선|0.445624 / 0.102008|
|#8DAACA|an existing pale-blue motif region|밝은 구별 영역|0.727431 / 0.056692|

**오인 경계:** 파란 옆 소품을 청화 문양으로 대신하거나 도자기를 두 색 조명으로 칠함

**연결:** M06, M07 · P0

**맥락 출처:** [S30 Blue-and-white Porcelain Jar](https://www.museum.go.kr/ENG/contents/E0401000000.do?relicRecommendId=519677&schM=view)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P093 옻칠풍 블랙·주홍·골드

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 검고 매끄러운 면, 붉은 내부, 작은 금빛 선을 대비시키는 의례적 공예 소품 설계. 특정 지역·시대의 전통 규범을 재현한 팔레트는 아니다.

**관찰할 관계:** The inner red surface and smaller gold motif remain distinct from the black exterior.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#211C1A|a black existing glossy outer surface|큰 바탕 예시|0.231492 / 0.008732|
|#C24B35|a vermilion existing inner surface|지지 영역|0.569026 / 0.1573|
|#BA9956|an existing gold-colored motif|반사 강조|0.698735 / 0.094401|

**오인 경계:** 안팎 색을 뒤집거나 모든 지역의 옻칠 규범·제작법으로 일반화함

**연결:** M05, M14 · P2

**맥락 출처:** [S06 PBRT 4: Specular Reflection and Transmission](https://www.pbr-book.org/4ed/Reflection_Models/Specular_Reflection_and_Transmission), [S31 Urushi conservation at the V&A](https://www.vam.ac.uk/blog/caring-for-our-collections/urushi-conservation-at-the-va)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P094 먹·한지·인주색

**계열:** 전통·공예: 문화적 체계와 제작 재료에서 출발하는 조합

**설계 의도:** 밝은 종이와 어두운 선 사이에서 작은 붉은 표식 하나가 서명과 마침표의 역할을 한다. 서예풍 그래픽·책·공예 패키지에 적합하다.

**관찰할 관계:** One red stamp-shaped region remains separate from dark marks on the same paper carrier.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#303330|existing ink-dark calligraphic marks|윤곽·경계|0.317048 / 0.006697|
|#E9DFC7|an existing warm paper carrier|큰 바탕 예시|0.905269 / 0.033746|
|#AE4539|an existing red stamp region|작은 강조|0.529753 / 0.140103|

**오인 경계:** 붉은 물체를 서명 표식으로 대신하거나 실제 문자의 뜻·서명 진위를 확정함

**연결:** M03, M14 · P2

**맥락 출처:** [S01 Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S27 Korean Cultural Centre India: Obangsaek](https://www.korea.net/Events/Overseas/view?articleId=23083)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P095 옐로·블랙 주의 대비

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 주의 표지의 노랑·검정 관계에서 착안했다. 감성보다 명도 차와 빠른 식별이 중심이다. 산업적 그래픽에 응용할 수 있지만 장식과 실제 표지는 구분한다.

**관찰할 관계:** The yellow field and black information region retain their declared sign roles.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#F0CB39|an existing yellow sign field|큰 바탕 예시|0.850282 / 0.158465|
|#222528|an existing black sign panel|윤곽·경계|0.262636 / 0.00712|

**오인 경계:** 장식용 줄무늬를 실제 경고로 판정하거나 한국·ISO·OSHA 준수를 같은 것으로 주장함

**연결:** M15 · P2

**맥락 출처:** [S33 OSHA 1910.145](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.145), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P096 레드·화이트·블랙 위험 대비

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 위험 표지의 색 관계에서 착안했다. 빨강은 경고 영역, 백색·검정은 읽는 정보 영역으로 역할을 분리한다.

**관찰할 관계:** The warning region stays distinct from the readable white and black information regions.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#CC3737|an existing red warning region|경고 패널|0.563535 / 0.186148|
|#F7F5EF|an existing white information field|밝은 구별 영역|0.970031 / 0.008232|
|#252525|existing black sign labels|윤곽·경계|0.26448 / 0.0|

**오인 경계:** 빨강을 모든 본문에 퍼뜨리거나 실제 문구·기호 없이 위험 표지를 인증함

**연결:** M15 · P2

**맥락 출처:** [S33 OSHA 1910.145](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.145), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P097 그린·화이트 안전 안내

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 안전 지시 표지의 녹색 패널·백색 글자 관계에서 착안했다. 안내의 종류를 일관되게 식별하는 것이 목적이며 문구와 기호를 함께 사용한다.

**관찰할 관계:** White lettering remains on the green panel while dark labels remain on the white field.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#27714F|an existing green instruction panel|안내 패널|0.493035 / 0.091675|
|#F5F7F0|an existing white sign field|큰 바탕 예시|0.972691 / 0.009466|
|#25332C|existing black sign labels|윤곽·경계|0.305936 / 0.022577|

**오인 경계:** 안전 지시 표지를 녹색 비상구·의무 표지 전체와 동일시하거나 법규 준수를 주장함

**연결:** M15 · P2

**맥락 출처:** [S33 OSHA 1910.145](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.145), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P098 블루·화이트·레드 발산형

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 중립 기준의 양쪽 방향을 다른 색으로 나타낸다. 증가·감소, 기준 대비 편차처럼 의미 있는 중앙값이 있을 때 적합하다. 빨강의 의미는 범례로 정의한다.

**관찰할 관계:** The two directional color regions flank the declared neutral reference in the labeled data view.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#2166AC|an existing blue negative-value region|기준의 음쪽|0.504641 / 0.130217|
|#F7F7F7|an existing white reference-value region|중앙 기준|0.976139 / 0.0|
|#B2182B|an existing red positive-value region|기준의 양쪽|0.491543 / 0.184997|

**오인 경계:** 임의 장식 면적이나 순위 없는 두 범주에 중앙값을 강제하고 범례 의미를 생략함

**연결:** M16 · P2

**맥락 출처:** [S34 Choosing Colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P099 블루·오렌지 범주형

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 순위 없는 두 범주를 구별하는 A/B 비교 설계. 색각 접근성이 자동으로 보장되는 것은 아니므로 선 종류·기호·직접 라벨을 병행한다.

**관찰할 관계:** Two labeled unordered categories retain separate marks without a numerical midpoint.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#287AB0|existing blue category-A marks|순위 없는 범주|0.556331 / 0.113844|
|#E58D3E|existing orange category-B marks|순위 없는 범주|0.72178 / 0.141056|
|#F0F0E8|an existing light chart field|큰 바탕 예시|0.952935 / 0.010608|

**오인 경계:** 파랑·주황만으로 접근성을 인증하거나 A/B 범주에 증가·감소 의미를 강제함

**연결:** M16 · P2

**맥락 출처:** [S34 Choosing Colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [S36 WCAG 2.2 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

## P100 보라·청록·노랑 — Viridis

**계열:** 기능·정보 전달: 감성보다 역할이 명확한 조합

**설계 의도:** 낮은 값부터 높은 값까지 이어지는 순차형 컬러맵의 대표 지점이다. 농도·강도·확률처럼 연속량의 크기에 적합하다. 장식용 면적 비율이 아니라 수치에 따라 매핑한다.

**관찰할 관계:** The declared scalar order links the five displayed color anchors to the labeled value order.

|색 기준|선택 가능한 owner|역할|평면 색칩 Oklab L / C|
|---|---|---|---|
|#440154|an existing lowest-value chart region|낮은 값 대표점|0.285018 / 0.136631|
|#3B528B|an existing lower-value chart region|중간 값 대표점|0.448418 / 0.097913|
|#21918C|an existing middle-value chart region|중간 값 대표점|0.596471 / 0.095069|
|#5EC962|an existing upper-value chart region|중간 값 대표점|0.748981 / 0.173011|
|#FDE725|an existing highest-value chart region|높은 값 대표점|0.917692 / 0.185864|

**오인 경계:** 다섯 색칩을 전체 연속 맵으로 보거나 수치 순서 없이 같은 면적의 장식 배색으로 사용함

**연결:** M16 · P2

**맥락 출처:** [S34 Choosing Colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html), [S35 WCAG 2.2 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

**채택 조건:** 실제 core의 같은 owner·속성으로 재결합하고 명시된 관계를 선택한 경우만 검증한다. 미선택 재질·새 물체·광원·감정을 추가할 권한은 없다.

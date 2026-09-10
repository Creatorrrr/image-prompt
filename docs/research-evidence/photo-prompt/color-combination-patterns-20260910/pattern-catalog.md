# 색 조합 패턴별 데이터 설계 부록

아래는 연구용 의미군과 시각 조건이다. 같은 행에 묶인 용어는 관련 변형이며 무조건 교환 가능한 exact alias가 아니다. 모든 게이트는 제안 상태이고 렌더 검증은 하지 않았다.

## ccp_monochromatic · 한 유채색군의 변주

용어: Monochromatic

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 이름 붙인 유채색 영역들이 한 색상군에 머묾 / 영역 사이 명도나 채도 단계는 구별됨.

혼동·대체 배제: 흑백만 있음 / 전역 색광 워시로 표면 구별이 사라짐.

영문 제어 초안: Keep the named chromatic regions within one hue family, with readable lightness or chroma variation.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_achromatic · 무채색 톤 구성

용어: Achromatic

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 대상 범위의 유채색이 제거됨 / 흑색·회색·백색 사이 톤과 재질이 구별됨.

혼동·대체 배제: 세피아 단색 / 저채도지만 색이 남는 장면.

영문 제어 초안: Render the specified scope without chromatic hues while retaining its tonal and material distinctions.

근거: [S03](https://cie.co.at/eilvterm/17-22-063), [S15](https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_analogous · 인접 색상군

용어: Analogous

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 주요 유채색 영역들이 같은 색상환의 연속된 이웃 구간에 놓임 / 각 영역은 다른 색상군으로 구별됨.

혼동·대체 배제: 한 색의 밝기 변화만 있음 / 멀리 떨어진 포인트를 필수로 추가.

영문 제어 초안: Keep the principal chromatic regions in neighboring hue families on the declared wheel.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_complementary · 대향 색상군

용어: Complementary, Complementary Contrast

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 두 주요 색상군의 영역 소유자가 구별됨 / 선택한 색상환에서 서로 대향함.

혼동·대체 배제: 두 색이 다르기만 함 / 한쪽 색은 조명 번짐뿐임.

영문 제어 초안: Assign the two named regions opposing hue families on the declared wheel, retaining each region's boundary.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_near_complementary · 보색 부근의 어긋남

용어: Near-Complementary

분류: `hue` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 두 영역은 넓은 색상 차를 유지함 / 한쪽이 선언된 보색 기준에서 약간 이동함.

혼동·대체 배제: 보색과 같은 프로필로 중복 집계 / 임의의 두 색.

영문 제어 초안: Offset one member of the declared opposing pair slightly while preserving a clear two-region hue contrast.

근거: [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_split_complementary · 기준색과 분할된 대향군

용어: Split Complementary

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 기준 영역 하나와 대향 쪽 두 색상군이 구별됨 / 대향 쪽 두 색의 벌어짐이 각각 보임.

혼동·대체 배제: 삼색 균등 간격으로 치환 / 보색 한쪽만 존재.

영문 제어 초안: Use one base hue family and two distinct families flanking its opposite on the declared wheel.

근거: [S07](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_triadic · 세 방향 색상군

용어: Triadic

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 세 주요 유채색군이 각각 영역에 귀속됨 / 선택한 색상환에서 세 방향 간격이 대체로 균등함.

혼동·대체 배제: 세 개 물체지만 색상군은 둘 / 분할 보색으로 대체.

영문 제어 초안: Place three distinguishable hue families approximately evenly around the declared wheel and assign each to a named region.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_tetradic · 두 보색쌍의 사색 관계

용어: Tetradic, Double Complementary, Rectangle Scheme

분류: `hue` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 네 색상군을 두 대향쌍으로 연결할 수 있음 / 각 색상군의 영역과 쌍 관계가 보존됨.

혼동·대체 배제: Adobe double split complementary와 무조건 동일시 / 네 색이기만 함.

영문 제어 초안: Assign four hue families as two opposing pairs, recording whether the requested geometry is rectangular or square.

근거: [S07](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_square · 정방형 사색 관계

용어: Square Scheme

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 네 주요 색상군이 구별됨 / 선택한 색상환의 네 방향 간격이 대체로 균등함.

혼동·대체 배제: 직사각형 사색을 같은 것으로 판정 / 세 색과 중성색 하나.

영문 제어 초안: Distribute four principal hue families approximately evenly around the declared wheel.

근거: [S07](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients), [S08](https://facelessuser.github.io/coloraide/harmonies/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_accented_analogous · 유사색 기반의 이탈 포인트

용어: Accented Analogous

분류: `hue` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 큰 기반 영역은 인접 색상군을 이룸 / 별도 작은 영역은 그 범위에서 떨어진 색상군임.

혼동·대체 배제: 기반부터 다색으로 분산 / 강조색이 기반만큼 큼.

영문 제어 초안: Use an analogous base field and a bounded accent outside that hue neighborhood.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S14](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_limited_palette · 제한된 색상 자원

용어: Limited Palette, Restricted Subject Palette, Restricted Background Palette

분류: `hue` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 제한할 피사체 또는 배경 범위가 지정됨 / 그 범위의 주된 색상군 수나 범위가 제한됨.

혼동·대체 배제: 무조건 단색으로 바꿈 / 화면 전체 제한을 피사체만으로 대체.

영문 제어 초안: Restrict the principal hue families within the named scope, leaving other scopes as requested.

근거: [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html), [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_polychromatic · 다색 구성

용어: Polychromatic

분류: `hue` / `advisory`. 후보 슬롯: `color`.

관찰 조건: 다수의 구별 가능한 색상군이 지정 범위에서 함께 읽힘 / 그 색들이 여러 실제 영역에 귀속됨.

혼동·대체 배제: 고채도 한 색 / 작은 노이즈를 색상군으로 집계.

영문 제어 초안: Allow multiple clearly distinct hue families across the specified regions without imposing a fixed harmony scheme.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_hue_contrast · 색상 차이 축

용어: Hue Contrast

분류: `hue` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 비교할 두 영역이 구별됨 / 명도나 채도만이 아닌 색상군 차이가 있음.

혼동·대체 배제: 명암만 강함 / 무조건 보색으로 확대.

영문 제어 초안: Keep a readable hue difference between the named regions independently of their lightness contrast.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S06](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_chroma_field · 전체 채도 수준

용어: High-Chroma Palette, Low-Chroma Palette, Muted Palette

분류: `chroma` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 조절할 범위가 명시됨 / 그 범위에 선명함 또는 억제된 색채감이 지속됨.

혼동·대체 배제: 밝기만 올림 / 암부로 묻어 색이 안 보임.

영문 제어 초안: Set the overall chroma level of the named field while retaining its requested hue and tonal structure.

근거: [S01](https://cie.co.at/eilvterm/17-22-073), [S02](https://cie.co.at/eilvterm/17-22-074). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_chroma_separation · 영역간 채도 대비

용어: Saturation / Chroma Contrast, Saturated Accent, Vivid-on-Muted, Muted-on-Vivid, Subject–Background Saturation Separation, Color Pop

분류: `chroma` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 비교 대상의 소유자가 분리됨 / 한쪽의 색채감이 다른 쪽보다 뚜렷이 강함.

혼동·대체 배제: 밝은 쪽을 고채도로 오인 / 배경도 함께 선명해짐.

영문 제어 초안: Give the named subject and environment a clear chroma hierarchy, in the requested direction.

근거: [S01](https://cie.co.at/eilvterm/17-22-073), [S02](https://cie.co.at/eilvterm/17-22-074), [S11](https://pubmed.ncbi.nlm.nih.gov/21264737/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_chroma_gradient · 채도의 순차 변화

용어: Chroma Gradient

분류: `chroma` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 변화의 공간 경로나 대상 순서가 있음 / 그 순서를 따라 채도 단계가 일관되게 변함.

혼동·대체 배제: 명도만 변함 / 랜덤한 색 점들의 나열.

영문 제어 초안: Vary chroma progressively along the specified path while holding the other requested color axes stable.

근거: [S02](https://cie.co.at/eilvterm/17-22-074), [S24](https://www.w3.org/TR/2026/CRD-css-color-4-20260908/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_chroma_distribution · 색상군별 채도 배분

용어: Uniform Saturation, Mixed Saturation, Soft-on-Soft

분류: `chroma` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 대상 색상군과 비교 기준이 지정됨 / 유사 채도 또는 차등 채도 배분이 여러 영역에서 확인됨.

혼동·대체 배제: HSV 수치가 같으면 지각도 동일하다고 단정 / soft를 흐림으로 대체.

영문 제어 초안: Distribute chroma consistently or unequally across the specified hue groups, preserving the requested tonal softness separately.

근거: [S01](https://cie.co.at/eilvterm/17-22-073), [S02](https://cie.co.at/eilvterm/17-22-074), [S03](https://cie.co.at/eilvterm/17-22-063). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_tonal_key · 명도 분포의 키

용어: High-Key Palette, Low-Key Palette, Mid-Key Palette

분류: `tone` / `reuse_existing`. 후보 슬롯: `color`.

관찰 조건: 밝은·어두운·중간 영역 중 요청한 범위가 화면 분포를 지배함 / 핵심 피사체의 필요한 계조는 남음.

혼동·대체 배제: 하이키를 클리핑으로 대체 / 로키를 전역 노출 부족으로 대체.

영문 제어 초안: Bias the image's tonal distribution toward the requested key while retaining the specified subject detail.

근거: [S15](https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

기존 데이터와의 경계: Existing low-key profile requires selective illumination, which is narrower than a dark tonal distribution. Reuse only for matching meaning; keep mid-key and distribution-only low-key separate.

## ccp_value_contrast · 영역간 명도 대비

용어: Light–Dark / Value Contrast, High-Value Contrast, Low-Value Contrast

분류: `tone` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 비교할 영역이 명확함 / 요청한 큰 또는 작은 밝고 어두움의 차이가 존재함.

혼동·대체 배제: 채도 차이만 있음 / 강한 그림자를 무조건 추가.

영문 제어 초안: Control the lightness difference between the named regions without changing their hue relationship unnecessarily.

근거: [S03](https://cie.co.at/eilvterm/17-22-063), [S15](https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_tonal_layering · 비슷한 톤의 층 구별

용어: Tonal Harmony, Tone-on-Tone, Dark-on-Dark, Light-on-Light

분류: `tone` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 비슷한 톤 또는 같은 색군의 영역이 겹치거나 이웃함 / 미세한 명도·색·질감 차이로 경계가 남음.

혼동·대체 배제: 검은 실루엣으로 합쳐짐 / 밝은 영역 전부 클리핑.

영문 제어 초안: Layer related tones while preserving small readable differences at the named boundaries.

근거: [S03](https://cie.co.at/eilvterm/17-22-063), [S15](https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_equiluminance · 등휘도와 근사 밝기 일치

용어: Isoluminant / Equiluminant Color

분류: `tone` / `measurement_only`. 후보 슬롯: `color`.

관찰 조건: 서로 다른 색상군을 비교할 영역이 정해짐 / 선언한 측정 색공간과 표시 조건에서 휘도 일치 여부를 확인함.

혼동·대체 배제: 같은 HSV V / 그레이스케일처럼 보인다는 주관적 판정만 있음.

영문 제어 초안: For a photographic approximation, use different hues with closely matched displayed luminance; reserve exact equiluminance for calibrated testing.

근거: [S13](https://opg.optica.org/abstract.cfm?uri=josaa-37-4-A35), [S24](https://www.w3.org/TR/2026/CRD-css-color-4-20260908/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_simultaneous_contrast · 동일 자극과 주변색의 상호작용

용어: Simultaneous Contrast

분류: `perception` / `measurement_only`. 후보 슬롯: `color`.

관찰 조건: 서로 다른 주변색 안의 비교 자극이 같은 표시색인지 확인됨 / 자극 차이와 구별된 주변 맥락 효과를 관찰 조건과 함께 평가함.

혼동·대체 배제: 두 자극 자체의 RGB가 다름 / 조명 차이로 실제 표면 표시색이 달라진 것을 지각 착시로 단정.

영문 제어 초안: Place matching displayed-color samples in different surrounds; evaluate the contextual perceptual effect separately from pixel equality.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S10](https://www.albersfoundation.org/alberses/teaching/interaction-of-color). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_role_hierarchy · 주조·보조·강조의 역할 위계

용어: Dominant–Secondary–Accent, Dominant Color, Supporting Color, Secondary Color, Accent Color, 60–30–10 Rule, Extension / Proportion Contrast

분류: `area` / `reuse_existing`. 후보 슬롯: `color`.

관찰 조건: 주조 영역이 가장 넓고 보조 영역이 구별됨 / 강조 영역의 면적과 위치가 두 기반 영역에 종속됨.

혼동·대체 배제: 모든 색면을 같은 비중으로 배치 / 색목록만 있고 영역 소유자가 없음.

영문 제어 초안: Keep a large dominant field, a smaller supporting region, and a bounded accent, with proportions specified only when requested.

근거: [S14](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_single_accent · 단일 강조 색상군

용어: Single Color Accent, Achromatic + Accent, Chromatic Accent

분류: `area` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 기반의 중성 또는 저채도 성격이 분명함 / 강조할 색상군과 소유자가 제한됨.

혼동·대체 배제: 중성 기반과 저채도 기반을 무조건 같게 봄 / 단일 색상군을 단일 물체로 강제.

영문 제어 초안: Confine the principal chromatic accent to the named owner against the requested neutral or restrained base.

근거: [S02](https://cie.co.at/eilvterm/17-22-074), [S14](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_isolated_accent · 공간적으로 고립된 포인트

용어: Isolated Accent

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 포인트 영역이 따로 식별됨 / 주변에 경쟁 색 덩어리 없이 분리 공간이 남음.

혼동·대체 배제: 포인트 주변에 같은 색이 붙어 큰 덩어리가 됨 / 무조건 중앙 배치.

영문 제어 초안: Separate the bounded accent from competing chromatic regions with a readable surrounding interval.

근거: [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/), [S14](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_micro_accent · 작지만 읽히는 포인트

용어: Micro Accent

분류: `area` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 강조 영역은 기반에 비해 작음 / 최종 출력과 썸네일 목표에서 요구한 표적은 식별 가능함.

혼동·대체 배제: 작아서 사라짐 / 큰 소품을 마이크로라 부름.

영문 제어 초안: Use a small localized chromatic accent that remains identifiable at the intended viewing size.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S14](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_accent_distribution · 강조색의 군집과 분산

용어: Accent Cluster, Scattered Accent, Clustered Color, Distributed Color

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 같은 역할의 색 요소들이 여러 개 있음 / 한정 영역 집중 또는 화면 분산이라는 요청한 배치가 보임.

혼동·대체 배제: 군집과 분산을 동시 의무화 / 색상 히스토그램만으로 판단.

영문 제어 초안: Place the accent elements in the requested cluster or dispersed arrangement, retaining each element's boundary.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_repetition · 분리된 소유자 사이 색 반복

용어: Repeated Accent, Color Echo, Color Repetition, Color Link

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 서로 떨어진 둘 이상의 영역이 구별됨 / 그 영역의 색상군이 시각적으로 연결됨.

혼동·대체 배제: 한 물체의 반사상만으로 별도 소유자 조건 충족 / 전역 워시.

영문 제어 초안: Repeat a recognizable hue family across distinct, separated scene elements.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_rhythm · 순서와 간격을 가진 반복

용어: Color Rhythm, Alternating Color

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 색 요소의 순서가 읽힘 / 반복 또는 교대 간격이 구도의 방향을 이룸.

혼동·대체 배제: 두 개 색 점만으로 리듬 보장 / 무작위 산포.

영문 제어 초안: Repeat or alternate the named color regions along a readable sequence with visible intervals.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_anchor · 색의 초점과 균형점

용어: Color Anchor, Chromatic Focal Point, Focal Color, Key Color, Highlight Color

분류: `attention` / `advisory`. 후보 슬롯: `color`.

관찰 조건: 의도한 시각 표적이 지정됨 / 그 표적의 색 대비가 주변과 구별됨.

혼동·대체 배제: highlight를 무조건 밝은 톤으로 해석 / 면적 최대인 색을 무조건 시선 초점으로 간주.

영문 제어 초안: Use the named region as the chromatic focal cue while preserving its intended relation to surrounding areas.

근거: [S11](https://pubmed.ncbi.nlm.nih.gov/21264737/), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_bridge · 두 색군 사이 연결 영역

용어: Color Bridge, Transitional Color

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 서로 다른 두 색군의 영역이 있음 / 중간 색조를 가진 제삼의 연결 영역 또는 연속 경로가 있음.

혼동·대체 배제: 배경 어디든 중간색 한 점 / 단순 두 색 혼합.

영문 제어 초안: Place a visible intermediate-color region between the two named palette regions.

근거: [S07](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients), [S05](https://www.cie.co.at/eilvterm/17-22-040). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_temperature_field · 따뜻한·차가운 색 지배

용어: Warm-Dominant, Cool-Dominant

분류: `temperature` / `advisory`. 후보 슬롯: `color`.

관찰 조건: 대상 범위의 상대적 한난 경향이 읽힘 / 요청한 중성 예외나 반대 영역이 있으면 보존됨.

혼동·대체 배제: 특정 켈빈을 픽셀에서 역산 / 웜을 무조건 주황색 워시로 만듦.

영문 제어 초안: Make the specified field relatively warm or cool while retaining any named neutral exceptions.

근거: [S04](https://cie.co.at/eilvterm/17-23-068), [S05](https://www.cie.co.at/eilvterm/17-22-040). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_temperature_separation · 소유자별 한난 분리

용어: Warm–Cool Contrast, Warm Subject / Cool Environment, Cool Subject / Warm Environment, Subject–Background Temperature Separation

분류: `temperature` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 피사체와 환경 등 비교 소유자가 구별됨 / 두 영역이 상대적으로 반대 한난 경향을 가짐.

혼동·대체 배제: 피부를 고정 주황색으로 만듦 / 전체 색조만 따뜻해짐.

영문 제어 초안: Separate the named owners by relative warm and cool color tendencies in the requested direction.

근거: [S04](https://cie.co.at/eilvterm/17-23-068), [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_depth_temperature · 깊이별 한난 배열

용어: Warm Foreground / Cool Background, Cool Foreground / Warm Background, Temperature Gradient

분류: `temperature` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 전후경 또는 공간 방향이 독립 단서로 읽힘 / 그 경로를 따라 요청한 한난 순서가 존재함.

혼동·대체 배제: 평면 위 두 색 띠를 깊이 증거로 대체 / 먼 곳은 항상 파랑으로 고정.

영문 제어 초안: Arrange the requested warm–cool order across independently readable spatial planes or a named spatial path.

근거: [S21](https://www.getty.edu/education/for_teachers/curricula/landscapes/background2.html), [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_mixed_illuminants · 혼합 광원의 색 관계

용어: Mixed Color Temperature

분류: `illumination` / `reuse_existing`. 후보 슬롯: `lighting`.

관찰 조건: 서로 다른 광원의 방향과 수광 영역이 구별됨 / 같은 재질 또는 중성 기준에서 두 조명 응답이 일관됨.

혼동·대체 배제: 명암 기반 split tone만 있음 / 전역 캐스트만 존재.

영문 제어 초안: Let distinct illuminants affect traceable receiving regions, with a declared white-balance anchor.

근거: [S04](https://cie.co.at/eilvterm/17-23-068), [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_tone_temperature · 명암 구간별 한난 배분

용어: Warm Highlight / Cool Shadow, Cool Highlight / Warm Shadow, Shadow Tint, Midtone Tint, Highlight Tint

분류: `grading` / `parameter_variant`. 후보 슬롯: `color_grading`.

관찰 조건: 하이라이트·중간톤·암부의 대상 구간이 선언됨 / 그 구간에 요청한 색 경향이 존재함.

혼동·대체 배제: 좌우 두 색 조명을 무조건 같은 의미로 처리 / 전역 단색 틴트.

영문 제어 초안: Give the specified tonal bands distinct color tendencies with controlled transitions and named protected regions.

근거: [S17](https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_multicolor_lighting · 여러 색광의 수광 관계

용어: Bi-Color Lighting, Dual-Tone Lighting, Two-Color Lighting, Tri-Color Lighting, RGB Lighting, Gel Contrast

분류: `illumination` / `new_narrow`. 후보 슬롯: `lighting`.

관찰 조건: 요청한 수의 색광 기여가 수광면에서 구별됨 / 빛의 방향·가림·겹침이 장면 표면과 연결됨.

혼동·대체 배제: 장비가 RGB라는 이유만으로 세 광원 판정 / 바이컬러 백색광 장비를 두 색 연출로 강제.

영문 제어 초안: Use separately traceable colored-light contributions on the specified receiving surfaces.

근거: [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices), [S04](https://cie.co.at/eilvterm/17-23-068). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_key_fill_color · 주광·보조광의 색 역할

용어: Colored Key + Neutral Fill, Neutral Key + Colored Fill

분류: `illumination` / `new_narrow`. 후보 슬롯: `lighting`.

관찰 조건: 주광과 보조광의 역할이 형상과 그림자에서 구별됨 / 각 역할에 색 또는 중성 특성이 요청대로 귀속됨.

혼동·대체 배제: 중성 피부라는 말만 있음 / 두 광원의 역할이 반대.

영문 제어 초안: Assign the requested color to the key or fill contribution while keeping the other contribution relatively neutral.

근거: [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_colored_rim · 윤곽에 귀속된 색광

용어: Colored Rim Light, Contrasting Rim Light

분류: `illumination` / `new_narrow`. 후보 슬롯: `lighting`.

관찰 조건: 피사체 윤곽 일부에 색광이 존재함 / 그 색광이 후방 또는 측후방 수광 형상과 일치함.

혼동·대체 배제: 후광 그래픽 / 배경색 경계를 림광으로 오인.

영문 제어 초안: Keep the colored light on source-facing contours, with its hue distinct from the key when requested.

근거: [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices), [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_wash · 범위를 가진 색광 워시

용어: Color Wash, Background Color Wash

분류: `illumination` / `parameter_variant`. 후보 슬롯: `lighting`.

관찰 조건: 워시를 받을 공간이나 배경이 지정됨 / 그 범위에 색광이 넓게 이어지면서 가림을 따름.

혼동·대체 배제: 배경 페인트색만 있음 / 배경 한정을 무시하고 얼굴까지 워시.

영문 제어 초안: Wash the named receiving area with colored illumination, preserving requested spill boundaries.

근거: [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_cross_color_light · 반대 방향의 서로 다른 색광

용어: Cross-Color Lighting, Color Separation Lighting

분류: `illumination` / `new_narrow`. 후보 슬롯: `lighting`.

관찰 조건: 분리된 방향 또는 수광 영역이 있음 / 그 영역별 다른 색광과 경계 전이가 읽힘.

혼동·대체 배제: 화면 위 색 필터 두 장 / 광원 방향 없는 착색.

영문 제어 초안: Let differently colored contributions arrive from distinct directions and follow the receiving forms and occlusions.

근거: [S16](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices), [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_figure_ground · 형태와 배경의 색 분리

용어: Subject–Background Color Separation, Figure–Ground Color Contrast, Neutral Field / Chromatic Subject, Chromatic Field / Neutral Subject, Character–Environment Palette Contrast

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 피사체 외곽과 배경이 독립 영역으로 구별됨 / 요청한 색 차이가 주요 외곽을 따라 유지됨.

혼동·대체 배제: 흐림만으로 분리 / 배경 일부 작은 색 점.

영문 제어 초안: Maintain the requested color contrast along the subject–background boundary.

근거: [S11](https://pubmed.ncbi.nlm.nih.gov/21264737/), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

기존 데이터와의 경계: Broad palette contrast permits multiple axes and hue families; do not force warm–cool separation or a single accent. Bind neutral/chromatic direction to the request.

## ccp_depth_palette · 공간 층별 팔레트

용어: Foreground–Midground–Background Palette, Layered Color Palette, Color Depth Separation

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 전경·중경·배경이 중첩·크기 등으로 구별됨 / 각 층의 색군 역할이 혼동되지 않음.

혼동·대체 배제: 색면 세 개만 있음 / 블러 단계만 존재.

영문 제어 초안: Assign distinct palette roles to independently readable foreground, middle, and background planes.

근거: [S21](https://www.getty.edu/education/for_teachers/curricula/landscapes/background2.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_atmospheric_color · 거리 증가에 따른 색·대비 변화

용어: Atmospheric Color Separation

분류: `spatial` / `reuse_or_parameter`. 후보 슬롯: `color`.

관찰 조건: 원근 거리 순서가 다른 단서로 확인됨 / 먼 영역의 색 강도와 명암 대비가 대기 조건에 맞게 약화됨.

혼동·대체 배제: 전역 뿌연 필터 / 모든 원경을 무조건 파랑으로 변경.

영문 제어 초안: Let distant planes lose chroma and local tonal contrast relative to nearer planes, consistent with the depicted atmosphere.

근거: [S21](https://www.getty.edu/education/for_teachers/curricula/landscapes/background2.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_framing · 색 영역의 둘러쌈

용어: Color Framing

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 중심 표적과 주변 색 영역이 구별됨 / 색 영역이 두 면 이상 또는 요청한 윤곽을 따라 표적을 감쌈.

혼동·대체 배제: 색 소품 하나가 근처에 있음 / 후반 테두리를 자동 추가.

영문 제어 초안: Use the specified colored scene regions to surround or bracket the focal subject.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_blocks · 넓고 분리된 색면

용어: Color Blocking, Large Color Fields

분류: `spatial` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 넓은 색면들이 각각 식별됨 / 색면 사이 경계가 구도에서 읽힘.

혼동·대체 배제: 잘게 쪼개진 다색 무늬 / 무조건 평면 포스터.

영문 제어 초안: Compose with large, clearly bounded color fields while retaining the requested photographic surface and depth cues.

근거: [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_split · 지정 방향의 색면 분할

용어: Split Color Composition, Diagonal Color Split

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 주요 색 영역들이 큰 구획으로 나뉨 / 경계의 위치나 대각 방향이 요청과 일치함.

혼동·대체 배제: split toning으로 치환 / 작은 대각 소품만 있음.

영문 제어 초안: Divide the main composition into the requested large color regions with a readable directional boundary.

근거: [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_bands · 수평·수직 색 띠

용어: Horizontal Color Bands, Vertical Color Bands

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 둘 이상의 길게 이어진 색 띠가 보임 / 띠의 방향과 순서가 명확함.

혼동·대체 배제: 줄무늬 의상만으로 전역 구도 충족 / 임의 색 점.

영문 제어 초안: Arrange the specified scope as ordered horizontal or vertical color bands.

근거: [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_radial_color · 방사·동심 배열

용어: Radial Color Arrangement, Concentric Color Structure

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 중심 또는 공통 축이 식별됨 / 방사 방향 또는 둘러싼 고리들의 색 순서가 보임.

혼동·대체 배제: 단순 중앙 포인트 / 원형 물체 하나.

영문 제어 초안: Arrange color regions as rays or nested surrounding zones around a visible shared center.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_spatial_gradient · 공간을 따른 연속 색 변화

용어: Gradient, Ombré

분류: `spatial` / `parameter_variant`. 후보 슬롯: `color`.

관찰 조건: 변화하는 물체나 공간 경로가 지정됨 / 그 경로에서 색상·명도·채도의 선언된 축이 연속적으로 변함.

혼동·대체 배제: Gradient Map과 동의어 처리 / 색 띠의 단절을 연속으로 판정.

영문 제어 초안: Change the specified color axis smoothly along the named surface or spatial path.

근거: [S07](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients), [S24](https://www.w3.org/TR/2026/CRD-css-color-4-20260908/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_zones · 영역별 색 구획

용어: Color Zoning

분류: `spatial` / `advisory`. 후보 슬롯: `color`.

관찰 조건: 둘 이상의 의미 있는 공간 구역이 있음 / 각 구역의 색 역할과 경계가 유지됨.

혼동·대체 배제: 아무 다색 장면 / 영역 소유자 없는 팔레트.

영문 제어 초안: Assign stable palette roles to the named spatial zones, preserving their boundaries.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_palette_complexity · 피사체·배경 색상군 복잡도 차

용어: Simple Background / Complex Subject Palette, Complex Background / Simple Subject Palette, Palette Density Contrast

분류: `complexity` / `new_narrow`. 후보 슬롯: `color`.

관찰 조건: 피사체와 배경의 평가 범위가 분리됨 / 한쪽의 유효 색상군 다양성이 다른 쪽보다 큼.

혼동·대체 배제: 채도 높은 한 색을 복잡하다고 간주 / 질감 노이즈만 증가.

영문 제어 초안: Use more distinct hue families in one named scope and fewer in the other, independently of texture detail.

근거: [S05](https://www.cie.co.at/eilvterm/17-22-040), [S12](https://pubmed.ncbi.nlm.nih.gov/22208128/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_split_toning · 두 톤 구간의 색조 분리

용어: Split Toning

분류: `grading` / `new_narrow`. 후보 슬롯: `color_grading`.

관찰 조건: 주로 암부와 밝은 톤에 다른 색 경향이 있음 / 색 변화가 화면 좌표보다 톤 구간에 결부됨.

혼동·대체 배제: 좌우 색광만 있음 / 전역 한 색 틴트.

영문 제어 초안: Apply different color tendencies to shadows and highlights with an explicit transition policy.

근거: [S17](https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_three_way_grade · 세 톤 구간의 독립 보정

용어: Three-Way Color Grading

분류: `grading` / `parameter_variant`. 후보 슬롯: `color_grading`.

관찰 조건: 암부·중간톤·하이라이트 처리 방향이 각각 지정됨 / 구간 전이가 연속적이고 보호 대상이 유지됨.

혼동·대체 배제: 색광 세 개 / 반드시 세 개 서로 다른 Hue로 강제.

영문 제어 초안: Control shadows, midtones, and highlights separately; the three controls need not introduce three different hues.

근거: [S17](https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_duotone · 제한 색조의 톤 재해석

용어: Duotone, Tritone

분류: `grading` / `new_narrow`. 후보 슬롯: `color_grading`.

관찰 조건: 제한된 색조가 여러 원래 표면의 명암 구조를 재해석함 / 잔존 원색과 계조의 허용 범위가 선언됨.

혼동·대체 배제: 두 색 의상 / 두 색 조명.

영문 제어 초안: Use a declared two- or three-color tonal remapping treatment, with the intended treatment of original surface hues made explicit.

근거: [S18](https://helpx.adobe.com/uk/photoshop/using/duotones.html), [S20](https://helpx.adobe.com/photoshop/using/applying-special-color-effects-images.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_selective_retention · 국소 색 보존·억제

용어: Selective Color, Partial Desaturation

분류: `grading` / `reuse_existing`. 후보 슬롯: `color_grading`.

관찰 조건: 남길 영역과 억제할 영역이 지정됨 / 경계·질감·동일 물체의 연결성이 유지됨.

혼동·대체 배제: 채도 높은 소품을 중성 배경에 둔 것만으로 편집 이력 단정 / Photoshop Selective Color 조정과 무조건 동의어.

영문 제어 초안: Retain chroma in the selected region while suppressing it elsewhere, with continuous shading and texture across the mask boundary.

근거: [S19](https://helpx.adobe.com/photoshop/using/mix-colors.html), [S25](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

기존 데이터와의 경계: Existing same-surface exception is narrower than keeping one entire object colored. Retain separate variants. Selective Color adjustment tool requires its own disambiguated interpretation.

## ccp_global_tint · 범위 전체의 공통 색 편향

용어: Global Tint, Color Cast Unification

분류: `grading` / `parameter_variant`. 후보 슬롯: `color_grading`.

관찰 조건: 전역 또는 지정 범위에 공통 색 편향이 있음 / 예외로 둔 중성 또는 제품 표면이 있으면 구별됨.

혼동·대체 배제: 한 색 물체만 많음 / 광원 원인을 단정.

영문 제어 초안: Apply a shared color bias within the declared scope, with explicit exceptions where requested.

근거: [S17](https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html), [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_gradient_mapping · 톤값을 색으로 대응

용어: Gradient Mapping

분류: `grading` / `new_narrow`. 후보 슬롯: `color_grading`.

관찰 조건: 회색조 기준과 색 정지점 대응이 지정됨 / 떨어진 영역도 같은 톤 조건에서 같은 매핑 체계를 따름.

혼동·대체 배제: 왼쪽에서 오른쪽으로만 바뀌는 배경 / 후반 도구 사용 이력을 픽셀만으로 확정.

영문 제어 초안: Map the declared tonal range to a specified sequence of color stops rather than to screen position.

근거: [S20](https://helpx.adobe.com/photoshop/using/applying-special-color-effects-images.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_cross_processed · 교차 현상풍 색·톤 관계

용어: Cross-Processed Palette

분류: `grading` / `advisory`. 후보 슬롯: `color_grading`.

관찰 조건: 어떤 색·톤 구간이 어떻게 이동하는지 지정됨 / 표면별 계조와 선택한 편향이 읽힘.

혼동·대체 배제: 녹색 캐스트 하나를 모든 교차 현상 표준으로 취급 / 생성 이미지로 실제 현상 이력 주장.

영문 제어 초안: Describe the requested channel or tonal color shifts explicitly, treating cross-processing as a look reference unless process metadata exists.

근거: [S23](https://www.lomography.com/school/what-is-cross-processing-fa-bne2kolj). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_discord · 의도한 색 불균형

용어: Color Discord, Clashing Colors, Chromatic Tension, Unequal Color Balance, Off-Balance Palette, Abrupt Color Contrast, Controlled Discord

분류: `attention` / `advisory`. 후보 슬롯: `color`.

관찰 조건: 기반 색 관계와 이탈 또는 급변 영역을 구별할 수 있음 / 이탈의 면적·위치·색 차이가 선언됨.

혼동·대체 배제: 불쾌함·긴장감의 보편적 발생을 보장 / 임의 다색 혼란.

영문 제어 초안: Introduce the specified hue, chroma, area, or spatial imbalance relative to an otherwise readable palette structure.

근거: [S10](https://www.albersfoundation.org/alberses/teaching/interaction-of-color), [S11](https://pubmed.ncbi.nlm.nih.gov/21264737/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_palette_continuity · 연속 장면의 색 관계 유지

용어: Palette Continuity

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 둘 이상의 순서 있는 프레임이 있음 / 소유자별 색 관계가 장면 변화에도 유지됨.

혼동·대체 배제: 단일 이미지로 연속성 통과 / 전체 평균 RGB만 일치.

영문 제어 초안: Maintain the declared owner-to-color relationships across the ordered frames.

근거: [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_palette_progression · 시간에 따른 색 변화

용어: Palette Progression, Color Arc

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 세 개 이상의 순서 있는 프레임 또는 시간 표본이 있음 / 지정 색 축의 변화 방향이 연속적으로 읽힘.

혼동·대체 배제: 한 장의 공간 그라디언트 / 사진 하나로 서사 변화 입증.

영문 제어 초안: Change the declared palette axis progressively across the ordered sequence.

근거: [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/), [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_palette_shift · 사건 전후 색 체계 전환

용어: Palette Shift

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 전환 전후 프레임과 사건 경계가 지정됨 / 그 경계에서 요청한 팔레트 관계가 바뀜.

혼동·대체 배제: 화이트밸런스 오류를 의도된 사건으로 추론 / 정지 사진 한 장.

영문 제어 초안: Change the declared palette relationship at the specified sequence boundary.

근거: [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/), [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_palette_inversion · 전후 색 역할 반전

용어: Palette Inversion

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 비교할 전후 프레임이 있음 / 같은 소유자들에 배정된 색 역할이 서로 뒤바뀜.

혼동·대체 배제: RGB 음화 반전 / 장면 사이 무관한 색 변화.

영문 제어 초안: Swap the declared owner-to-color roles between the before and after frames.

근거: [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/), [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_motif · 반복되는 색과 서사 대상

용어: Color Motif, Signature Color

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 동일한 서사 대상 또는 주제가 외부 맥락으로 지정됨 / 여러 프레임에서 그 대상과 색군의 결합이 반복됨.

혼동·대체 배제: 한 이미지의 포인트색으로 고유 시그니처나 감정 단정 / 국적·성격 추론.

영문 제어 초안: Repeat the declared color association with the specified narrative referent across the sequence.

근거: [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

## ccp_color_coding · 대상별 색 부호

용어: Color Coding

분류: `sequence` / `sequence_only`. 후보 슬롯: `None`.

관찰 조건: 둘 이상의 인물·장소·상황에 대응 규칙이 선언됨 / 각 대상이 해당 규칙에 맞는 색 관계를 반복 유지함.

혼동·대체 배제: 임의 색 옷으로 신분이나 역할 단정 / 명시한 대응표 없이 상징 주장.

영문 제어 초안: Maintain the explicitly declared color code for each named entity or setting.

근거: [S22](https://theasc.com/article/whos-afraid-of-red-green-and-blue/), [S26](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 출처는 개념·인접 원리를 뒷받침하며, 위 영역 계약과 판정 조건은 연구 설계 제안이다.

# 주제 11 — 헤어·메이크업·피부 표면·beauty capture·anti-plastic cues

## 결론 요약

이 증분 코퍼스는 헤어, 메이크업, 피부의 후보 어휘를 늘리는 것보다 **서로 다른 원인축과 검토 해상도를 분리하는 것**이 더 큰 개선 지점임을 보여준다.

- 헤어에서는 `컷/배열`과 `바람·수분·가닥 묶임 같은 순간 상태`가 현재 `hair_style` 안에 섞여 있다. 특히 `windblown/windswept` 계열은 프롬프트 115/924건에서 나타나고, 표본 2333·2654·2741은 뿌리-전체 질량-이탈 가닥-광택이 함께 읽힐 때 강했다. 별도 `hair_motion_state` 후보 슬롯과 좁은 exact profile `wind_displaced_hair_coherence`가 유효하다.
- 피부에서는 `plastic skin`, `beauty filter`, `airbrushed`, `waxy`, `retouching`, `smoothing` 같은 금지어가 중첩되어도 픽셀 결과는 매끈함부터 뚜렷한 미세결까지 갈렸다. 좁은 anti-plastic 어휘군 기준 398/924건이 하나 이상, 210건이 둘 이상, 48건이 셋 이상을 썼고, 167건은 대응하는 양성 피부 구성요소 없이 금지어만 썼다. 이 부정어 묶음을 후보팩이나 자동 negative에 수입하지 말고, `미세형상·국소 확산색·표면 정반사·하이라이트 롤오프·화장 커버리지·검토 가능 해상도`를 양성 소유축으로 분해해야 한다.
- 메이크업 데이터는 이미 상당히 강하다. `complexion_coverage`, `skin_finish`, `brow_style`, `eyeshadow_style`, `eye_makeup_line`, `lash_style`, `cheek_makeup`, `face_sculpting`, `lip_color_placement`, `lip_finish`, `makeup_wear_state`가 존재한다. 신규 스타일명을 더 넣기보다 `inclusive_makeup_beauty`의 비어 있는 `redundancy_rules`와 `coverage_repair`를 보강해 aggregate `makeup_style`이 구성 슬롯을 반복하거나 대신하지 못하게 하는 편이 낫다.
- 피부 모공, 미세 털, 입술 선, 메이크업 경계는 얼굴이 충분히 크게 보일 때만 검토할 수 있다. 표본 1939와 2213처럼 전신/원거리 구도에서는 프롬프트에 `visible pores`가 있어도 픽셀 게이트는 실패가 아니라 `UNSCORED`여야 한다.

최종 결정은 **`proposed`**다. 이 보고서는 연구·설계만 수행했고 런타임 자산, 생성 인덱스, 테스트, 프롬프트 생성기, 렌더 기록을 수정하지 않았다. 패키지/프롬프트 동작, 신규 렌더, 사용자 미감 판단은 모두 미검증 또는 미채점이다.

## 1. 범위와 표본 방법

### 동결 범위

- 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 매니페스트 SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, 누락 프롬프트 258개, 게시물 ID 1565–2746
- 대상 스킬 기준 리비전: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 연구 계약의 authored-source SHA-256:
  - visual obligations: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - tags/candidates: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - quality layers: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`

연구 도중 공유 작업 트리의 authored-source 파일에는 다른 병렬 작업의 변경이 계속 들어왔다. 따라서 위 SHA를 연구 시작 기준으로 유지하고, 현재 파일 검사는 **소유권과 기존 구조 확인**에만 사용했다. 이 보고서는 움직이는 작업 트리의 새 변경을 자신의 구현 성과로 간주하지 않는다.

### 프롬프트 전수 스캔

비어 있지 않은 924개 프롬프트 전체를 대소문자 무시 정규식으로 스캔했다. 한 프롬프트가 여러 범주에 중복 집계될 수 있다. `texture` 같은 일반 단어는 피부/헤어 카운트에서 제외하고, 해당 표면을 직접 지칭하는 문구만 세었다.

### 픽셀 표본

다음 규칙으로 15개 게시물, 각 2장, 총 **30/4,908장**을 고정했다.

- ID 구간: 초기 1565–1958, 중기 1959–2352, 후기 2353–2746
- 각 구간: 주제 양성 4개 게시물 + 근접 대조 1개 게시물
- 각 게시물: 매니페스트 순서의 첫 2개 다운로드 성공 이미지
- 양성: 프롬프트에서 헤어 물리, 메이크업 구성, 피부 미세구조, beauty capture, anti-plastic 중 다수 축이 명시된 게시물
- 근접 대조: 사람 중심 사진이지만 같은 주제의 상세 어휘가 없거나 매우 약한 게시물
- 검토 방식: 각 파일을 `detail=original`로 열어 전체 프레임과 native 세부를 확인했다.

이 30장에 대한 빈도는 표본 관찰일 뿐 전체 4,908장으로 일반화하지 않는다. 이미지로부터 정체성, 동일인 여부, 보호 특성, 건강, 매력, 성격, 직업, 민족성, 국적 또는 관계를 추론하지 않았다. 사람 관련 기술은 보이는 성인 표현, 헤어·화장·피부 표면, 자세와 공간 관계에 한정한다.

## 2. 프롬프트 측 발견과 카운트

### 2.1 세부 어휘 카운트

| 프롬프트 측 휴리스틱 | 매치/924 | 의미와 주의점 |
|---|---:|---|
| `hair_any` | 788 | `hair`, `hairstyle`, `bangs`, `fringe`, `flyaway` 중 하나. 매우 넓어 하드 프로필 근거가 아님 |
| hair strand/fiber | 179 | individual/fine/face-framing/realistic/detailed/grouped strands, hair fibers 등 |
| hair root/hairline | 94 | roots, hairline, baby hairs |
| hair flyaway | 95 | flyaway, stray hair |
| hair motion/wind | 115 | windblown, windswept, wind-tossed, hair와 wind/breeze의 근접 공기 |
| hair wet/damp | 20 | hair와 wet/damp/moisture의 근접 공기 |
| hair grouped/clumped | 13 | grouped strands, clumped hair/strands, strand bundles |
| `makeup_any` | 387 | makeup 또는 cosmetic 명시 |
| brow structure | 96 | groomed/defined/feathered/individual/straight/arched 등과 brow |
| lash structure | 127 | separated/individual/wispy/natural/wet/fanned lash, eyelash, mascara |
| eye geometry | 123 | eyeshadow, eyeliner, tightline, lash root, crease |
| cheek color | 187 | blush, bronzer, cheek wash |
| lip placement/finish | 250 | glossy/satin/matte/blurred/dewy/balm/stained lip, lip texture/finish, lipstick/tint |
| realistic/natural skin texture | 255 | 피부를 직접 수식하는 realistic/real/natural/authentic texture |
| visible/readable pores | 152 | visible/refined/realistic pores 또는 보존/가독성 문구 |
| fine facial hair | 76 | peach fuzz, fine facial hair, vellus |
| local color/texture variation | 71 | tonal variation, uneven tone, natural color variation, subtle imperfections |
| under-eye microdetail | 25 | under-eye texture/variation/fullness/detail/micro-veins |
| skin translucency | 25 | skin translucency, subsurface scattering, translucent skin edge |
| freckles | 32 | freckle/freckles |
| anti plastic-skin | 350 | plastic skin/texture 중심 |
| anti filter/smoothing | 203 | beauty filter, smoothing, airbrush, over-retouch |
| anti waxy/doll | 31 | waxy skin/texture, doll-like skin/features, doll symmetry |
| beauty close-resolution | 101 | beauty portrait/campaign/close-up, tight face crop, extreme close-up |

합집합 기준은 다음과 같다.

| 결합 범주 | 매치/924 |
|---|---:|
| hair microphysics | 350 |
| makeup components | 372 |
| skin microstructure | 417 |
| anti-plasticity | 402 |

### 2.2 시기별 문구 밀도

| ID 구간 | 비어 있지 않은 프롬프트 | hair microphysics | makeup components | skin microstructure | anti-plasticity | beauty close-resolution |
|---|---:|---:|---:|---:|---:|---:|
| 초기 1565–1958 | 382 | 61 (16.0%) | 114 (29.8%) | 94 (24.6%) | 27 (7.1%) | 26 (6.8%) |
| 중기 1959–2352 | 285 | 133 (46.7%) | 121 (42.5%) | 146 (51.2%) | 185 (64.9%) | 26 (9.1%) |
| 후기 2353–2746 | 257 | 156 (60.7%) | 137 (53.3%) | 177 (68.9%) | 190 (73.9%) | 49 (19.1%) |

이 증가는 **프롬프트 문체와 명세 밀도의 변화**를 보여줄 뿐 픽셀 품질 향상을 증명하지 않는다. 후기 프롬프트가 더 많은 피부·헤어·금지어를 쓰는 사실을 전역 기본값의 허가로 사용해서는 안 된다.

### 2.3 anti-plastic 부정어 누적

좁은 표면 부정어 8종을 별도로 셌다: `plastic skin`, `AI smoothing`, `beauty filter`, `airbrushed`, `waxy skin/texture`, `doll-like surface`, `excessive retouch`, `excessive/skin/face/digital smoothing`.

- 하나 이상: 398/924
- 둘 이상: 210/924
- 셋 이상: 48/924
- 대응 양성 피부 구성요소 없이 하나 이상: 167/924

이는 부정어가 실패 원인을 설명하지 못하는 경우가 많음을 보여준다. 현재 대상 스킬의 유지보수 계약도 modern authorial prompt에 blanket negative를 넣지 않고 자동 negative를 좁은 intent-neutral 결함 어휘로 제한한다. 따라서 코퍼스의 긴 negative 목록은 후보팩 원문으로 가져오지 않는다.

## 3. 픽셀 측 관찰과 표본 ID

### 3.1 게시물별 관찰

| 구간 | 게시물 | 역할 | 프롬프트 측 주장 | 2장 픽셀 관찰 | 정렬/발산 |
|---|---:|---|---|---|---|
| 초기 | 1634 | 양성 | 장식 업두, delicate makeup, porcelain/chok-chok skin, realistic skin texture | 묶인 헤어 질량과 이탈 가닥은 선명하다. 피부는 넓게 균일하고 강한 광택은 있으나 모공/국소결은 약하다. | 헤어는 정렬, `realistic skin texture`는 부분 발산 |
| 초기 | 1887 | 양성 | CCD 직광, semi-matte skin, lip texture, real skin texture | 가르마·긴 가닥·직광 핫스폿·립 광택은 보인다. 얼굴의 미세결은 제한적이다. | capture와 헤어는 정렬, 피부 결은 약함 |
| 초기 | 1939 | 양성 | visible pores, natural skin texture, dewy editorial makeup, anti-plastic | 전신 프레임에서 얼굴이 작아 모공/속눈썹/피부결 판정이 불가능하다. 헤어는 매끈한 덩어리와 전체 실루엣 위주다. | 프롬프트 증거 존재, 픽셀 게이트는 `UNSCORED` 대상 |
| 초기 | 1942 | 양성 | beauty portrait, visible pores, delicate texture, detailed hair strands | 얼굴 근접도와 헤어 가닥은 충분하다. 부드러운 국소 변화는 있으나 피부가 전반적으로 정제되어 미세결 강도는 제한된다. | 부분 정렬 |
| 초기 | 1842 | 근접 대조 | 작은 헤어핀과 soft flash 외 상세 어휘 거의 없음 | 긴 헤어의 가닥 묶음, 얼굴 주변 이탈 가닥, 아이라인과 립 색은 픽셀에 존재한다. 피부는 비교적 매끈하다. | 프롬프트 어휘 부재가 픽셀 부재를 뜻하지 않음 |
| 중기 | 2131 | 양성 | skin texture, asymmetry, blush/gloss/dewy variants, pores, hair strands, plastic-skin 금지 | 같은 게시물의 두 장이 크게 다르다. 01은 균일하고 정제된 표면, 02는 볼의 작은 표면 흔적과 국소 색 변화가 보인다. | 동일 프롬프트 제약만으로 픽셀 품질을 판정할 수 없음 |
| 중기 | 2207 | 양성 | sleek hair, face-crossing strands, winged liner, lashes, glossy lips, texture/no smoothing | 헤어 실루엣·가닥, 아이라인·립은 읽힌다. 직광 아래 피부는 광택과 평활감이 강하고 세부결은 약하다. | 메이크업/헤어 정렬, 피부는 부분 발산 |
| 중기 | 2290 | 양성 | luminous/dewy makeup, glossy blowout, authentic skin texture, no plastic | 뿌리·헤어 표면광·이탈 가닥, 아이라인, 립 마감, 피부의 미세한 밝기 변화가 함께 보인다. | 비교적 강한 정렬 |
| 중기 | 2333 | 양성 | wet loose windblown hair, strand motion blur, luminous skin, texture | 수분으로 묶인 가닥과 바람 방향, 젖은 광택, 흩어진 끝단이 일관된다. 한 장은 선글라스로 눈 화장 판정이 제한된다. | 헤어 상태의 강한 정렬, 일부 메이크업 `UNSCORED` |
| 중기 | 2213 | 근접 대조 | 주제 상세 어휘 없음 | 전신 스포츠 구도라 헤어 실루엣은 읽히지만 피부 미세결과 메이크업 경계는 판정하기 어렵다. | native detail eligibility의 하드 네거티브 |
| 후기 | 2589 | 양성 | baby hair, flyaways, freckles, under-eye texture, lip texture, satin lipstick, anti-retouch | 가르마·베이비헤어·층진 헤어 표면, 프리클과 립 선/색소는 보인다. 피부 전체는 여전히 매우 고르게 정제된다. | 구성요소는 정렬, anti-plastic 종합은 부분 정렬 |
| 후기 | 2632 | 양성 | skincare close-up, pores, fine facial hair, freckles, translucency, lip lines, skin shine | 모공·프리클·미세 주름·입술 선·눈썹/속눈썹·정반사와 확산색이 동시에 명확하다. | 표본 내 가장 강한 피부 양성 |
| 후기 | 2654 | 양성 | many wind-lifted strands, face crossing, pores, fine hairs, uneven tone, translucency, six anti-surface terms | 가르마와 전체 질량에서 여러 가닥이 한 방향으로 이탈하고 얼굴을 가로지른다. 피부 미세결과 립 선도 읽힌다. | 표본 내 가장 강한 바람 헤어 양성; 부정어 수가 원인임은 입증하지 못함 |
| 후기 | 2741 | 양성 | short bob, roots, grouped strands, flyaways, explicit makeup layers, pores, freckles, micro-shadows | 짧은 헤어의 뿌리·묶인 가닥·외곽 이탈, 테라코타 계열 눈/볼/입술 분포, 프리클과 하드라이트 미세그림자가 함께 보인다. | 헤어·메이크업·피부 축의 강한 정렬 |
| 후기 | 2554 | 근접 대조 | 의상/직물 명세 중심, 주제 상세 어휘 없음 | 포니테일 뿌리와 잔가닥, 자연광에 따른 얼굴 밝기 변화가 보이지만 미세결은 제한적이다. | 어휘 없이도 일부 표면 단서가 생기는 대조 |

### 3.2 표본 수준 요약

- 헤어의 전체 실루엣이나 일부 섬유/가닥 단서는 15개 게시물 대부분에서 보였지만, **뿌리-전체 질량-이탈 가닥-광택 방향이 모두 같은 상태를 설명하는 강한 사례**는 2333, 2654, 2741처럼 제한적이었다.
- native 피부 미세구조가 명확한 강한 양성은 2131의 한 변형, 2290, 2333, 2589, 2632, 2654, 2741이었다. 1942는 부분 양성이다. 이 수치는 표본 설명이지 전체 코퍼스 빈도가 아니다.
- 1939와 2213은 얼굴 영역이 작아 모공·미세 털·립 선·화장 경계 평가가 불가능했다. 원거리 결과에 native 게이트를 적용하면 잘못된 실패를 만든다.
- 1842와 2554는 상세 어휘가 없어도 헤어/표면 단서 일부가 나타났다. 즉 BM25F·키워드 매치가 낮다고 픽셀 가능성이 0인 것은 아니다.
- 9/12 양성 게시물 프롬프트가 하나 이상의 anti-plastic 지시를 포함했지만 결과는 균일 평활부터 선명한 미세결까지 넓게 갈렸다. 이 표본은 부정어의 인과적 유효성을 입증하지 않는다.

## 4. 프롬프트/픽셀 정렬과 발산

### 정렬된 관계

1. **가시적 헤어 상태는 명사보다 관계로 읽힌다.** 2333·2654에서는 단순 `wet` 또는 `windblown`이 아니라 뿌리, 기본 질량, 이탈 가닥, 얼굴/어깨와의 겹침, 방향성 광택이 함께 있을 때 상태가 강했다.
2. **피부의 자연스러움은 단일 texture가 아니라 다중 광학 단서다.** 2632는 모공/프리클/미세 주름 같은 공간 변화와 이마·코·볼의 정반사, 그 사이의 확산색이 동시에 있었다.
3. **메이크업은 배치와 표면 마감이 분리될 때 읽힌다.** 2741은 눈꺼풀 색 분포, 분리된 속눈썹, 볼 색, 입술 색/마감이 서로 다른 영역에서 읽히고, 피부 프리클과 미세결을 지우지 않았다.
4. **프레임 규모가 증거의 상한을 정한다.** beauty close-up인 2632와 full-length인 1939는 같은 native 피부 게이트로 평가할 수 없다.

### 발산과 가능한 원인

| 증상 | 가장 이른 의심 단계 | 근거 | 반증 조건 | 신뢰도 |
|---|---|---|---|---|
| `realistic skin texture`가 있으나 피부가 균일하게 매끈함 | 표현/소유권 또는 생성 반응 | 1634, 2207; 부정어 누적 통계 | 같은 조건에서 미세형상·국소 확산색·정반사 소유축을 분리해도 반복적으로 변화가 없다면 prompt-actuation 가설 약화 | 중간 |
| 같은 프롬프트에서 피부 표면이 크게 달라짐 | 생성/샘플링 | 2131의 두 장 | 동일 조건 반복에서 변동이 작고 특정 문구 변경에만 반응하면 sampling 가설 약화 | 중간 |
| 프롬프트에는 모공이 있으나 검토 불가 | 평가 가시성 | 1939, 2213 | native crop에서 모공/립선/화장 경계가 충분히 분해된다면 visibility 가설 반증 | 높음 |
| 헤어는 선명하지만 한 덩어리처럼 보임 | 내부 표현 또는 prompt actuation | 1939 대 2654 | 뿌리-가닥-방향-광택을 독립 제어한 결과도 동일한 솔리드 질량이면 generator-response 가설로 이동 | 중간 |
| 부정어가 많아도 anti-plastic 결과가 안정적이지 않음 | prompt priority/negative accumulation | 코퍼스 통계와 2131·2589·2654 | 반복 렌더에서 부정어 수만 증가시켜 미세구조 보존이 일관되게 향상되면 약화 | 낮음~중간; 렌더 실험 없음 |

## 5. 외부 기전 리서치

외부 자료는 후보 미감을 정하는 데 사용하지 않고, 물리적으로 안정된 분리축을 확인하는 데만 사용했다.

- Marschner 등은 개별 헤어 섬유에서 회전과 입출사 방향에 따라 달라지는 복수 정반사 성분을 측정했다. 이는 `glossy hair` 한 단어보다 가닥 방향, 섬유 연속성, 하이라이트 방향을 함께 소유해야 함을 지지한다. [Light Scattering from Human Hair Fibers](https://graphics.stanford.edu/papers/hair/)
- Weyrich 등은 얼굴 피부 반사를 공간적으로 변하는 표면 BRDF, diffuse albedo, diffuse subsurface scattering으로 분해했다. 이 보고서는 인구통계 분석을 사용하지 않고, **표면 정반사·국소 확산색·하부 산란을 구분해야 한다는 광학 구조**만 차용한다. [Analysis of Human Faces using a Measurement-Based Skin Reflectance Model](https://people.csail.mit.edu/addy/research/weyrich06-skin.pdf)

이 논문들은 생성 프롬프트가 물리 렌더러 매개변수를 직접 제어한다는 증거가 아니다. 여기서는 관찰/게이트 축을 분리하는 근거로만 사용한다.

## 6. 기존 데이터 중복과 소유권

### 6.1 이미 강한 부분

`assets/photo_prompt_visual_obligations.json`에는 다음과 같은 좁은 exact profile이 이미 있다.

- 메이크업/피부: `no_makeup_makeup_layering`, `smoky_eye_diffused_gradient`, `cut_crease_lid_separation`, `graphic_negative_space_eyeliner`, `glass_skin_specular_diffuse_balance`, `gradient_lip_center_distribution`, `sunburn_blush_cross_face_distribution`, `contour_highlight_cosmetic_sculpting`, `restrained_polished_natural_makeup_balance`, `sheer_complexion_texture_preservation`, `under_eye_high_cheek_blush_distribution`, `cheekbone_temple_blush_drape`
- 헤어: `two_block_disconnected_cut`, `hime_cut_structural`, `cornrow_scalp_row_topology`, `locs_cord_structure`, `bilateral_twin_tail_gather`, `balayage_ribbon_color_placement`, `wet_damp_clumped_hair_state`

`assets/photo_prompt_tags.json`의 관련 슬롯도 이미 넓다.

| 슬롯 | 현재 항목 수 |
|---|---:|
| `complexion_coverage` | 6 |
| `skin_condition` | 6 |
| `skin_finish` | 20 |
| `brow_style` | 5 |
| `lash_style` | 6 |
| `eye_makeup_line` | 5 |
| `eyeshadow_style` | 6 |
| `cheek_makeup` | 6 |
| `lip_color_placement` | 5 |
| `lip_finish` | 5 |
| `makeup_wear_state` | 6 |
| `hair_style` | 38 |
| `hair_color` | 15 |

특히 `semantic_policy.families.inclusive_makeup_beauty`는 위 구성 슬롯을 core/support로 이미 라우팅한다. 신규 메이크업 스타일명 추가는 우선순위가 낮다.

### 6.2 구조적 공백

1. `hair_style`이 컷, 배열, 색 배치, 환경 상태, 모션 상태를 함께 가진다. `wind_tossed_rooftop_hair`, `rain_damp_face_framing_hair`, `wet_damp_clumped_hair_state`처럼 상태 후보가 컷 후보와 동일 슬롯에 있다.
2. `skin_finish`가 matte/dewy/oily 같은 마감, 모공/미세 털 같은 미세구조, under-eye나 freckles 같은 국소 단서, 광원 반응을 함께 가진다.
3. `inclusive_makeup_beauty.redundancy_rules`와 `coverage_repair`가 비어 있어 aggregate `makeup_style`과 구성 슬롯의 중복 또는 불완전 채택을 구조적으로 막지 않는다.
4. `quality_profiles.portrait_editorial.prompt_focus`는 `pose readability`, `material styling`, `controlled light`만 포함한다. `photographic_craft.light_provenance`는 광원 출처/정반사를 다루지만 close human surface에 대한 구체적 refinement가 없다.
5. visual obligations의 `review_scale`은 thumbnail/native를 구분하지만, 해당 영역이 충분히 보이는지를 먼저 기록하는 eligibility 필드가 없다.

### 6.3 올바른 소유층

| 개념 | 소유층 |
|---|---|
| 헤어 컷/배열 | 기존 `hair_style` |
| 바람/수분/움직임에 의한 순간 헤어 상태 | 새 advisory `hair_motion_state`; 좁고 안정된 exact term만 visual obligation |
| 피부 화장 커버리지 | 기존 `complexion_coverage` |
| 피부 마감 | 기존 `skin_finish` |
| 모공·미세 털·립 선·국소 표면 변화 | 새 advisory `skin_microtexture` |
| 정반사 방향·확산색·하이라이트 롤오프 | quality-layer `light_provenance` refinement |
| 메이크업 부위별 형상/배치 | 기존 brow/eye/lash/cheek/lip slots |
| aggregate makeup label | `makeup_style` support/semantic anchor만; 구성 슬롯을 대신하지 않음 |
| 세부 검토 가능성 | render-review eligibility, prompt candidate가 아님 |
| anti-plastic false substitutes | profile contrast/reject substitutes와 pixel review; 자동 blanket negative가 아님 |

## 7. 제안 의미 구성요소와 혼동 경계

### 7.1 헤어 순간 상태

**Observable components**

1. 두피/가르마에서 시작하는 기본 질량과 뿌리 방향
2. 한 개의 우세한 힘/움직임 방향
3. 기본 질량에서 연속적으로 이탈한 복수 가닥
4. 서로 다른 두께·간격·끝 위치
5. 얼굴, 목, 의상 또는 배경과의 실제 겹침/가림
6. 가닥 방향을 따르는 하이라이트와 그림자
7. 수분 상태가 있을 때만 감소한 볼륨·묶임·부착

**Confusion negatives**

- 얼굴 주변에 무작위로 뿌린 정적 선
- root 연결이 없는 와이어형 가닥
- motion blur만 있고 선명한 기준 질량이 없음
- 드라이 헤어에 균일한 플라스틱 광택만 있음
- 젤/오일 광택을 젖은 수분 상태로 오인
- 머리 전체가 한 장의 검은 천이나 solid cape처럼 보임
- 배경 선이나 의상 섬유를 헤어 가닥으로 오인

### 7.2 피부 미세구조와 광학 반응

**Observable components**

1. `microgeometry`: 모공, 미세한 표면 불균일, 빛이 허용할 때의 fine facial hair, 입술 선
2. `diffuse/local color`: 넓은 피부톤 안의 작은 국소 색 변화; freckles/marks는 source-supported일 때만
3. `specular`: 이마·코·볼·입술 등 보이는 고면에서 광원 방향을 따르는 제한된 반사
4. `subsurface/diffuse softness`: 그림자 가장자리와 밝은 면 사이의 점진적 전이
5. `coverage`: 화장층의 불투명도와 경계; 표면 광택과 분리
6. `micro-shadow`: 코 옆, 입술, 눈꺼풀, 헤어라인의 국소 깊이
7. `retouch ceiling`: source-supported 미세구조를 지우지 않는 처리 상한

**Confusion negatives**

- 과노출로 결이 사라진 얼굴
- 전체 블러/beauty filter
- 균일하게 반복되는 합성 pore stamp
- 필름 그레인 또는 JPEG 노이즈만 있는 표면
- freckles만 있고 모공·확산색·반사 구조가 없음
- T-zone 유분 핫스폿만 있는 표면
- 색 조명이 만든 붉음/청색을 피부 고유색 또는 화장으로 오인
- 샤프닝 halo를 미세결로 오인

### 7.3 메이크업 레이어

**Observable components**

- coverage: sheer/light/medium/full/selective
- brow: 실제 모발 구조와 그루밍 형상
- eyeshadow: 눈꺼풀 내 색소 위치와 경계
- liner: lash line과의 접속, 두께, 끝점
- lashes: 뿌리 연결, 분리/군집, 길이 분포
- cheek: 양측 위치, hue, 확산 경계
- lip color placement: 중심/전체/외곽 경계
- lip finish: matte/satin/balm/gloss와 입술 선의 공존
- wear state: fresh/lived-in/rain-softened/tear-track/patchy/faded
- hierarchy: complexion과 각 부위 대비의 우선순위

**Confusion negatives**

- 조명 그림자를 eyeshadow/contour로 오인
- 피로 그림자, 눈물, 자극, 상처를 화장으로 오인
- 입술의 전체 그림자를 gradient lip으로 오인
- 반짝임만으로 gloss/skin finish를 판정
- aggregate `natural makeup` 한 문구가 모든 구성 레이어를 대신함
- 같은 효과를 `makeup_style`, `lip_finish`, `cheek_makeup`에서 중복 actuation

## 8. 후보팩/데이터 제안 — 정확한 필드와 레이어

### 제안 A — `hair_motion_state` advisory 슬롯 추가

**대상:** `assets/photo_prompt_tags.json`

```json
{
  "slots": {
    "hair_motion_state": [
      {
        "id": "directional_wind_displacement",
        "en": "wind-displaced hair with one coherent mass direction and multiple continuous strands lifting away from the rooted baseline"
      },
      {
        "id": "localized_face_crossing_strands",
        "en": "a few continuous hair strands cross the facial plane while remaining connected to the surrounding hair mass"
      },
      {
        "id": "motion_softened_strand_tips",
        "en": "only the fastest displaced hair tips soften with motion while the rooted hair mass remains sharp"
      },
      {
        "id": "moisture_weighted_directional_clumps",
        "en": "moisture-weighted hair clumps move coherently with reduced dry volume and traceable root-to-tip bundles"
      }
    ]
  }
}
```

라우팅 제안:

- 새 `semantic_policy.families.hair_surface_capture`
- `routed_slots`: `hair_style`, `hair_color`, `hair_motion_state`, `weather`, `motion`, `lighting`, `light_shape`, `shot_scale`, `focus`
- `steering_slots`: `hair_style`, `hair_motion_state`, `weather`, `motion`, `lighting`, `shot_scale`, `focus`
- 한 프롬프트에서 `hair_motion_state` 최대 1개; 수분 상태와 바람 상태를 동시에 택할 때는 동일 방향/질량 관계를 요구
- BM25F/embedding-only 발견은 advisory이며 자동 하드 의무가 아님

**소유권:** 컷과 배열은 `hair_style`, 환경 힘은 `weather/motion`, 순간 가닥 상태는 `hair_motion_state`, 광택 방향은 `lighting/light_provenance`.

### 제안 B — 좁은 visual obligation `wind_displaced_hair_coherence`

**대상:** `assets/photo_prompt_visual_obligations.json`

정확한 activation 후보:

```json
{
  "id": "wind_displaced_hair_coherence",
  "category": "hair_motion_state",
  "activation": {
    "exact_terms": [
      "windblown hair",
      "windswept hair",
      "wind-tossed hair",
      "바람에 흩날리는 머리",
      "바람에 날리는 헤어"
    ],
    "semantic_discovery_requires_component_evidence": true
  }
}
```

필수 component groups:

```text
rooted_baseline_mass
dominant_displacement_direction
multiple_continuous_displaced_strands
spatial_overlap_or_occlusion
strand_surface_response
wind_hair_confound_control
```

Render gates:

- thumbnail: 기본 헤어 질량과 우세한 이탈 방향이 즉시 읽힘
- both: 복수 가닥이 같은 힘 방향을 공유하지만 복제된 평행선처럼 보이지 않음
- native: 이탈 가닥이 뿌리 또는 주변 질량으로 연속되고 두께·간격·끝 위치가 달라짐
- native: 가닥의 하이라이트와 그림자가 같은 광원/가닥 방향을 따름
- both: motion blur alone, random static flyaway halo, solid sheet, dry gloss, wet clump alone가 대체하지 않음

이 exact profile은 **정확한 바람 헤어 요청**에만 하드 활성화한다. 설명형 검색으로 발견된 경우에는 optional candidate로 남긴다.

### 제안 C — `skin_microtexture` advisory 슬롯 분리

**대상:** `assets/photo_prompt_tags.json`

```json
{
  "slots": {
    "skin_microtexture": [
      {
        "id": "pores_local_surface_irregularity",
        "en": "locally varied pores and small surface irregularities remain readable without a uniform stamped pattern"
      },
      {
        "id": "fine_facial_hair_light_contingent",
        "en": "fine facial hairs resolve only on source-supported regions where close focus and grazing or back light make them visible"
      },
      {
        "id": "natural_lip_line_preservation",
        "en": "natural lip lines remain visible beneath the selected matte satin balm or gloss finish"
      },
      {
        "id": "localized_under_eye_surface_variation",
        "en": "subtle under-eye surface and tonal variation remains visible without implying fatigue health or age"
      }
    ]
  }
}
```

적용 규칙:

- source-supported 항목만 0–2개 선택; 전역 기본 없음
- `complexion_coverage`는 화장 불투명도, `skin_finish`는 matte/dewy/oily 등 마감, `skin_microtexture`는 미세형상만 소유
- freckles/beauty marks는 pigmentation이므로 이 슬롯의 필수 기본이 아님
- `inclusive_makeup_beauty`의 routed/steering slots에 추가하되 support/advisory로 유지

### 제안 D — quality-layer `human_surface_response` refinement

**대상:** `assets/photo_prompt_quality_layers.json`

`photographic_craft.dimensions[id=light_provenance].refinements`에 다음 구조를 제안한다.

```json
{
  "id": "human_surface_response",
  "facet_match": {
    "subject_kind": ["human"],
    "shot_scale": ["medium_close", "close_up", "extreme_close"]
  },
  "principle": "Close human surfaces should separate local diffuse color, controlled high-plane specular response, readable source-supported microtexture, and gradual highlight roll-off under one traceable light source.",
  "guidance": {
    "en": "keep local diffuse color, restrained high-plane specular response, source-supported microtexture, and highlight roll-off distinct under the same light",
    "ko": "같은 광원 아래 국소 확산색, 제한된 고면 정반사, 근거 있는 미세결, 하이라이트 롤오프가 서로 구분되게 한다"
  },
  "audit_terms": [
    "local diffuse color",
    "high-plane specular",
    "microtexture",
    "highlight roll-off"
  ]
}
```

이 refinement는 피부색, 광택량, 결 강도의 선호값을 설치하지 않는다. 선택된 `skin_finish`와 광원에 맞는 **일관성**만 요구한다.

### 제안 E — 메이크업 구성 coverage/redundancy 보정

**대상:** `assets/photo_prompt_tags.json.semantic_policy.families.inclusive_makeup_beauty`

기존 `routed_slots`와 `slot_signals`는 유지한다. 비어 있는 `coverage_repair`에 group-aware v2 구조를 제안한다.

```json
{
  "coverage_repair": {
    "policy_id": "inclusive-makeup-layer-coverage-v2",
    "applies_when_any_terms": [
      "layered makeup",
      "editorial makeup close-up",
      "beauty close-up"
    ],
    "required_any_slot_groups": [
      ["complexion_coverage", "skin_finish"],
      ["brow_style", "eyeshadow_style", "eye_makeup_line", "lash_style"],
      ["cheek_makeup", "lip_color_placement", "lip_finish"]
    ],
    "max_one_candidate_per_slot": true,
    "aggregate_makeup_style_role": "semantic_anchor_or_palette_only"
  }
}
```

`redundancy_rules` 제안 원칙:

- component slot이 이미 정확한 geometry/finish를 소유하면 `makeup_style`은 같은 literal을 반복하지 않음
- aggregate label은 source-supported perceptual direction을 한 번 유지할 수 있으나, 구성 슬롯을 대체하지 않음
- 약한 positive actuation을 보정하기 위해 동의어나 blanket negative를 쌓지 않음

기존 스키마가 `required_any_slot_groups`를 지원하지 않으므로 구현 시 validator/schema와 focused tests가 함께 필요하다. 이 보고서에서는 제안만 한다.

### 제안 F — native-detail visibility eligibility

**대상:** `scripts/audit_image_render_review.py`가 소유하는 render-review 계약 또는 인접 review schema. 프롬프트 후보가 아니다.

```json
{
  "detail_visibility": {
    "face_surface_resolvable": "yes|no|partial",
    "hair_root_and_strands_resolvable": "yes|no|partial",
    "makeup_edges_resolvable": "yes|no|partial",
    "limiting_factors": [
      "small_region",
      "occlusion",
      "depth_of_field",
      "motion_blur",
      "compression",
      "overexposure"
    ],
    "unscored_gate_ids": []
  }
}
```

- 고정 픽셀 임계값을 전역 설치하지 않는다.
- `모공과 센서/압축 노이즈를 구분할 수 있는가`, `립 선과 샤프닝을 구분할 수 있는가`, `가닥이 뿌리로 연속되는가`를 native에서 판정한다.
- 가시성 부족은 `UNSCORED`, 보이는 결함은 `FAIL`, 보이는 의무 충족은 `PASS`다.
- thumbnail은 헤어 실루엣, 메이크업 계층, 전체 피부 광택 분포만 본다.

### 명시적 비제안

- `no plastic skin`, `no waxy skin`, `no beauty filter`를 후보 슬롯이나 자동 negative에 추가하지 않는다.
- `porcelain`, `glass`, `dewy`, `matte`를 자연스러움의 전역 선호로 만들지 않는다.
- freckles, pores, peach fuzz, under-eye variation을 모든 성인 얼굴의 필수 기본으로 만들지 않는다.
- 특정 얼굴형, 피부색, 나이, 성별, 민족성, 매력 또는 건강 추론을 의미 데이터로 만들지 않는다.

## 9. thumbnail/native render gates

| 제안 축 | Thumbnail gate | Native gate | Hard negative |
|---|---|---|---|
| wind-displaced hair | 기본 질량과 한 방향의 이탈 실루엣 | 복수 가닥의 뿌리 연속성, 두께/간격 변화, 방향성 광택 | static random halo, blur-only, solid sheet, wet/gel-only |
| moisture-weighted hair | 볼륨 감소와 묶인 질량 | 여러 clump의 root-to-tip 연속, 국소 부착, 수분 광택 | dry gloss, oily root, styling gel only |
| skin microtexture | 국소 색 변화와 전체 광택 분포 | 모공/미세형상/입술 선/미세 털이 노이즈·샤프닝과 구분 | grain-only, pore stamp, blur, overexposure |
| skin optical response | 광택이 얼굴 전체를 균일하게 덮지 않음 | 정반사 방향, diffuse color, micro-shadow, roll-off가 한 광원과 일치 | oily hotspot-only, colored-light-only, flat fill |
| makeup layering | complexion과 눈/볼/입술 대비 계층 | 각 부위 색소의 위치·경계·표면 마감 | cast shadow, irritation, bruise, uniform fill, aggregate label only |
| beauty detail eligibility | 얼굴/헤어가 주제 크기로 읽힘 | 판정 대상 영역이 실제로 분해됨 | 원거리/가림/압축을 의미 실패로 오인 |

## 10. 회귀 및 held-out 테스트

### 10.1 정적/패키지 테스트 제안

1. 새 `hair_motion_state`, `skin_microtexture` 항목은 모두 비어 있지 않은 unordered `concept_terms`와 실제 slot owner를 가져야 한다.
2. `hair_style`과 `hair_motion_state`가 같은 literal 효과를 중복 출력하면 실패한다.
3. `skin_finish`, `complexion_coverage`, `skin_microtexture`, `light_provenance`의 소유 문구가 서로 교차 침범하면 실패한다.
4. `inclusive_makeup_beauty`에서 aggregate `makeup_style`만 선택되고 구성 슬롯 그룹이 비는 layered beauty case는 coverage warning 또는 repair 대상이 된다.
5. 자동 negative에 `plastic skin`, `beauty filter`, `airbrushed`, `waxy skin`이 새로 들어가면 실패한다.
6. visual obligation exact terms는 narrow boundary match만 하며, BM25F/embedding-only match는 optional candidate로 남아야 한다.

### 10.2 prompt-level causal pairs

| Pair | 유지할 축 | 바꿀 축 | 기대 |
|---|---|---|---|
| wind hair vs still hair | 인물·컷·광원·구도 | `hair_motion_state`만 | 뿌리/색/컷은 유지되고 이탈 방향만 바뀜 |
| wind hair vs random flyaway | 인물·컷·가닥 수 | 힘 방향/연속성 | random halo는 hard negative |
| wet clumps vs dry glossy hair | 컷·색·광원 | 수분/볼륨/묶임 | gloss alone가 wet state를 통과하지 못함 |
| sheer coverage vs dewy finish | 미세결·광원 | coverage 또는 finish 한 축 | 불투명도와 광택이 독립적으로 바뀜 |
| matte textured vs blurred matte | 마감·광원 | microtexture 유지 | blur가 matte skin을 대체하지 못함 |
| satin lip vs glossy lip | 색 배치·입술 형상 | finish | natural lip line 유지, specular 형태만 변함 |
| freckles vs anti-plastic | 광원·coverage·shot | freckles 유무 | freckles만으로 anti-plastic 통과 불가 |
| close vs full-length | 동일 스타일 | shot scale | native detail gate는 close에서만 score 가능 |

### 10.3 motivating regression cases

- 1634: `realistic skin texture` 문구만으로 microtexture PASS 금지
- 1939: 전신 프레임의 visible-pores gate는 `UNSCORED`
- 2131: 같은 프롬프트의 서로 다른 피부 결과를 prompt PASS 하나로 합치지 않음
- 2333: wet/wind hair에서 가닥 묶임, 볼륨 감소, 방향, 광택을 함께 검사
- 2632: 피부 정반사·diffuse color·microtexture가 모두 보이는 양성
- 2654: wind-displaced hair exact-profile 양성
- 2741: 짧은 헤어, 메이크업 레이어, freckles/pores가 공존하는 양성
- 1842·2554: 상세 키워드가 없어도 나타나는 픽셀 단서를 retrieval hard gate로 역추론하지 않음
- 2213: 원거리 detail eligibility 하드 네거티브

### 10.4 독립 held-out 제안

다음 게시물은 이 보고서의 30장 픽셀 표본에 사용하지 않았다. 구현 후 독립 검증용으로 보존한다.

- 초기: 1653, 1907
- 중기: 2188, 2283
- 후기: 2656, 2738, 2744

최소 평가 세트:

1. 길이·색·컷이 다른 wind hair 3건
2. wet/damp와 dry glossy hard negative 각 2건
3. close beauty skin 3건과 full-length visibility negative 2건
4. makeup geometry 3건과 cast-shadow/colored-light negative 2건
5. 하나의 스타일을 유지하며 microtexture만 바꾸는 invariant pair
6. 하나의 microtexture를 유지하며 광원만 바꾸는 intrinsic/induced pair

신규 렌더 평가를 수행할 경우 모델/버전, 설정, 종횡비, 참조 처리, 시도 정책을 고정하고 arm별 프롬프트 바이트를 동결해야 한다. 한 장 성공으로 일반적 개선을 주장하지 않는다.

## 11. 한계와 bounded decision

### 한계

- 픽셀은 4,908장 중 30장만 직접 검토했다. 표본 비율을 전체 코퍼스 빈도로 해석할 수 없다.
- 게시물 내 이미지들은 동일 프롬프트에서 생성되었을 가능성이 높지만, 생성기/버전/seed/참조 처리/후처리 기록이 없으므로 프롬프트 인과를 확정할 수 없다.
- 피부와 헤어의 미세결은 파일 해상도, 압축, 리사이즈, 샤프닝, 광원, 초점, 후보 생성기의 반응이 혼재한다.
- anti-plastic 문구 통계는 언어 패턴 증거일 뿐, 각 부정어의 효과 크기를 측정한 실험이 아니다.
- 외부 논문은 광학 분리축을 정의하는 데만 사용했다. 코퍼스 생성기가 그 파라미터를 직접 따르는지 검증하지 않았다.
- 사용자 미감 판단은 수집하지 않았다.
- 공유 작업 트리의 관련 authored-source 파일에 병렬 변경이 있었으므로, 이 보고서는 구현 diff나 최종 SHA의 소유권을 주장하지 않는다.

### 결정

**`proposed`**

- 연구 근거: 있음
- 후보팩/visual-obligation/quality-layer 설계: 제안됨
- 런타임 구현: 안 함
- 생성 인덱스 재빌드: 안 함
- 패키지/정적 검증: 안 함
- prompt-level behavior 평가: 안 함
- 신규 렌더 및 픽셀 qualification: 안 함
- 사용자 판단: `UNSCORED`

## 12. Evidence appendix

### 12.1 검토 이미지 30장

기준 루트: `generated/reactorprompt-export-20260902-incremental/`

```text
images/1634_DY7OAMTGkmz_01.jpg
images/1634_DY7OAMTGkmz_02.jpg
images/1887_DZpdADYmqiE_01.jpg
images/1887_DZpdADYmqiE_02.jpg
images/1939_DZ4LHOXGgno_01.jpg
images/1939_DZ4LHOXGgno_02.jpg
images/1942_DZ41dVlGvsV_01.jpg
images/1942_DZ41dVlGvsV_02.jpg
images/1842_DZkWUaHGoJl_01.jpg
images/1842_DZkWUaHGoJl_02.jpg
images/2131_Daoo4ExGs_m_01.jpg
images/2131_Daoo4ExGs_m_02.jpg
images/2207_Da96Ci_GpnK_01.jpg
images/2207_Da96Ci_GpnK_02.jpg
images/2290_DbVoi1YGjC9_01.jpg
images/2290_DbVoi1YGjC9_02.jpg
images/2333_DblCEmHGjTy_01.jpg
images/2333_DblCEmHGjTy_02.jpg
images/2213_Da9dGT9GjiW_01.jpg
images/2213_Da9dGT9GjiW_02.jpg
images/2589_DcYWJtXmpMp_01.jpg
images/2589_DcYWJtXmpMp_02.jpg
images/2632_DcgOoN-muVh_01.jpg
images/2632_DcgOoN-muVh_02.jpg
images/2654_DciZLkTmqFP_01.jpg
images/2654_DciZLkTmqFP_02.jpg
images/2741_Dcx0xZ8mlev_01.jpg
images/2741_Dcx0xZ8mlev_02.jpg
images/2554_DcQJjwRGoam_01.jpg
images/2554_DcQJjwRGoam_02.jpg
```

### 12.2 핵심 명령

매니페스트 구조와 표본 경로:

```bash
jq 'type, length, .[0], .[1]' generated/reactorprompt-export-20260902-incremental/manifest.json
```

기존 visual-obligation profile 목록:

```bash
jq -r '.profiles | to_entries[] | select((.key>=65 and .key<=81) or (.key>=314 and .key<=318)) | [.key,.value.id,.value.category] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json
```

관련 슬롯 수:

```bash
jq '.slots | {complexion_coverage:(.complexion_coverage|length),skin_condition:(.skin_condition|length),skin_finish:(.skin_finish|length),brow_style:(.brow_style|length),lash_style:(.lash_style|length),eye_makeup_line:(.eye_makeup_line|length),eyeshadow_style:(.eyeshadow_style|length),cheek_makeup:(.cheek_makeup|length),lip_color_placement:(.lip_color_placement|length),lip_finish:(.lip_finish|length),makeup_wear_state:(.makeup_wear_state|length),hair_style:(.hair_style|length),hair_color:(.hair_color|length)}' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json
```

프롬프트 카운트는 Python `json`, `re`로 924개 비어 있지 않은 `.prompt`를 전수 순회했다. 재현에 필요한 범주별 정규식은 2.1의 정의 그대로이며, 시기별 분모는 다음 ID 경계를 사용했다.

```text
early: 1565 <= id <= 1958
middle: 1959 <= id <= 2352
late: 2353 <= id <= 2746
```

픽셀 검토는 위 30개 절대 경로를 `view_image(detail="original")`로 열어 수행했다.

### 12.3 외부 1차 자료

- Marschner et al., *Light Scattering from Human Hair Fibers*, SIGGRAPH 2003: <https://graphics.stanford.edu/papers/hair/>
- Weyrich et al., *Analysis of Human Faces using a Measurement-Based Skin Reflectance Model*, ACM TOG 2006: <https://people.csail.mit.edu/addy/research/weyrich06-skin.pdf>

### 12.4 증거층 상태

| 증거층 | 상태 |
|---|---|
| 프롬프트 924개 전수 스캔 | 완료 |
| 코퍼스 픽셀 30장/15게시물 검토 | 완료, 표본 한정 |
| 현재 authored-source 소유권 검사 | 완료, 공유 작업 트리 병렬 변경 주의 |
| 외부 광학 기전 확인 | 완료, 1차 자료 2건 |
| 신규 후보/프로필 구현 | 미실행 |
| 생성 인덱스 갱신 | 미실행 |
| package/static validation | 미실행 |
| prompt behavior test | 미실행 |
| 신규 렌더 qualification | 미실행 |
| 사용자 미감 판단 | `UNSCORED` |

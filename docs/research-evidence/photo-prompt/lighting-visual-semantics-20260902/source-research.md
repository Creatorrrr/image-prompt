# 사진 조명 용어 기반 시각 의미·후보팩 강화 리서치

- 조사일: 2026-09-02
- 참조 대화: `6a977d64-2230-83ee-bca1-12754c285b5f` (`사진 조명 용어 조사`)
- 대상: `photo-prompt-image-generator`
- 상태: **리서치·데이터 구현 및 3-arm 평가 완료, 수정 필요(revise)**
- 구조화 제안: `candidate-data-proposal.json`
- 출처 원장: `evidence.jsonl`
- 개선 기록: `iteration-record.json`

## 1. 결론

참조 대화의 조명 어휘는 현재 후보 사전의 폭을 넓히는 데 충분하지만, 한 층으로 넣으면 세 가지 오류가 생긴다.

1. `softbox`, `Fresnel`, `CRI 95`, `3200 K` 같은 **장비·측정값**이 실제 픽셀에서 확인 가능한 효과처럼 취급된다.
2. `low-key`, `underexposed`, `crushed blacks`와 같이 **조명, 노출, 후보정**이 서로 대체된다.
3. `Rembrandt`, `loop`, `split`, `butterfly`처럼 가까운 패턴이 이름 하나로만 저장되어 **필수 그림자 기하**가 누락된다.

따라서 다음 네 증거 차선을 분리해야 한다.

| 차선 | 소유하는 것 | 픽셀 계약 예 | 픽셀로 주장하면 안 되는 것 |
|---|---|---|---|
| 광원·장면 상호작용 | 방향, 상대 크기, 그림자, 반사, 분리 | 넓은 shadow-edge transfer, 코-볼 그림자 연결 | 실제 조명 브랜드, 와트 수 |
| 카메라·광학 반응 | 플레어, 고스팅, 회절, 디포커스 | 반복된 ghost, veiling contrast loss | 특정 렌즈 모델 |
| 톤·색 재현 | 클리핑, 톤 분포, 색 분리 | 밝은 영역 우세이나 하이라이트 디테일 유지 | 실제 CCT·CRI·SSI 수치 |
| 후보정·필름 룩 | 곡선, 색조 분리, halation 룩 | 고휘도 경계 바깥의 국소 색 번짐 | 실제 필름 스톡·현상 공정 |

핵심 설계는 다음과 같다.

- 현재 작업트리에 보이는 `rembrandt_face_light_pattern`, `clamshell_dual_source_portrait_light`, `negative_fill_shadow_deepening_relation`은 재사용 대상으로 분류한다.
- 22개 좁은 시각 계약을 P0/P1 프로필 후보로 제안하되, 정확·문맥 완전 용어만 hard activation이 가능하게 한다.
- 장비명, 정량값, 조명 품질 지수는 candidate/setup metadata에만 둔다.
- 12개 스타일 묶음은 단일 명사 나열이 아니라 조명·방향·광질·명암·형태·색·그레이딩을 함께 움직이는 coherent cluster로 제안한다.
- `partial_is_fail`을 적용한다. 이름이나 분위기가 맞아도 필수 관찰 요소 하나가 빠지면 해당 의미는 실패다.
- 초기 산출물은 연구와 데이터 설계였고, 후속 구현에서 라우팅·후보 검색·프롬프트·생성·픽셀 평가까지 진행했다. 다만 공개 후보팩의 신규 candidate ID 노출과 모든 렌더 의미의 성공, 사용자 선호 성공은 주장하지 않는다.

## 2. 참조 대화의 어휘 지도

참조 대화는 조명을 24개 범주로 폭넓게 정리했다. 아래는 후보 데이터 설계에 필요한 대표 어휘다.

1. 광원: daylight, sun, skylight, ambient, available, LED, COB, tungsten, HMI, fluorescent, neon, candle, fire, practical, motivated, mixed source
2. 광질: hard, soft, harsh, diffused, direct, indirect, bounce, wrap, broad, point, specular, matte, feathered, flat, sculptural
3. 방향: front, side, back, three-quarter, top, under, cross, raking, grazing, contre-jour
4. 역할: key, fill, separation, rim, edge, kicker, hair, accent, background, eye, negative fill
5. 인물 패턴: flat, butterfly, loop, Rembrandt, split, broad, short, clamshell, ring, three-point
6. 광량·변화: illuminance, luminance, exposure, EV, stop, falloff, inverse-square, beam angle, hotspot, spill
7. 그림자: cast, form, core, contact, umbra, penumbra, edge softness, density, crushed, open, lifted, ambient occlusion
8. 하이라이트: specular, diffuse, blown, clipped, roll-off, bloom, glow, halation
9. 명암: global/local contrast, microcontrast, dynamic range, latitude, black/white point, milky, deep black, faded, punchy
10. 명암 미학: high-key, low-key, chiaroscuro, tenebrism, noir
11. 색온도·화이트밸런스: CCT, Kelvin, WB, tint, warm/cool, mixed temperature, mired, Duv
12. 색: hue, saturation, chroma, luminance, vibrance, density, complementary, analogous, monochrome, teal-orange, pastel, muted
13. 광원 색 품질: CRI/Ra, R9, TLCI, SSI, SPD, metamerism, green spike, magenta shift
14. 필터: CTO, CTB, CTS, plusgreen, minusgreen, ND, effects gel
15. 조명 제어 도구: softbox, octabox, stripbox, umbrella, beauty dish, lantern, scrim, reflector, flag, grid, snoot, barn door, gobo, Fresnel
16. 영화 조명: practical, motivated, negative fill, haze, selective highlight, source ownership
17. 자연광 시간대: dawn, sunrise, golden hour, sunset, blue hour, twilight, midday, overcast, open shade, window light
18. 자연광·대기 패턴: dappled light, crepuscular rays, haze, snow/water bounce, reflected sunlight
19. 렌즈 효과: flare, veiling flare, ghosting, starburst, bloom, glow, black-mist diffusion
20. 색보정·후보정: correction, grading, tone curve, lift/gamma/gain, HSL, color wheels, split toning, LUT
21. 필름 룩: grain, halation, shoulder/toe, latitude, push/pull, cross processing, bleach bypass, gate weave, fade
22. 감성 기술어: dreamy, clean, moody, dramatic, intimate, eerie, luxurious, nostalgic
23. 색감 스타일: warm-neutral, cool-neutral, muted, rich, pastel, monochrome, complementary separation
24. 조합: clean beauty, dreamy portrait, luxury fashion, editorial hard-side, motivated interior, noir, sunset rim, moonlight, filmic, Y2K direct flash

이 목록은 그대로 hard profile 목록이 아니다. 아래처럼 처리한다.

| 용어 종류 | 기본 처리 | 이유 |
|---|---|---|
| 그림자·하이라이트의 관계가 좁고 관찰 가능 | hard profile 후보 | 단일 프레임에서 반증 가능 |
| 장비명이나 배치명 | candidate/setup translation | 여러 장비가 같은 픽셀을 만들고 한 장비도 여러 픽셀을 만듦 |
| 정량 측정값 | explicit metadata only | 생성 픽셀만으로 실제 수치를 검증할 수 없음 |
| 분위기·감성 | advisory candidate | 형태·광원·톤 계약을 소유하지 않음 |
| 후보정 명칭 | postprocess lane | 실제 현장 조명과 혼합하면 원인 주장이 거짓이 됨 |
| 자연 시간대 | visible-look contract 또는 candidate | 실제 촬영 시각을 주장하지 않고 관찰 가능한 태양·하늘 관계만 소유 |

## 3. 현재 저장소 기준선

2026-09-02 조사 시점의 공유 작업트리를 읽기 전용으로 확인했다.

### 3.1 후보 슬롯

| 슬롯 | 현재 항목 수 |
|---|---:|
| `lighting` | 143 |
| `light_direction` | 18 |
| `light_type` | 76 |
| `light_intensity` | 16 |
| `light_shape` | 90 |
| `color` | 54 |
| `color_grading` | 7 |
| `film_emulation` | 18 |

대표적으로 `golden_hour`, `chiaroscuro`, `rembrandt_lighting`, `butterfly_lighting`, `clamshell_beauty_light`, `chiaroscuro_window_light`, `prism_flare_light`가 이미 있다. 그러나 다수는 한 줄짜리 후보이며, 서로 다른 슬롯을 같은 광학·톤 관계로 묶는 ownership가 없다.

### 3.2 시각 프로필

- 현재 파일은 275개 프로필을 포함한다.
- 공유 작업트리에는 이 조사에서 만든 것이 아닌 기존/동시 변경이 있다.
- 그 변경에는 다음 조명 프로필이 보인다.
  - `rembrandt_face_light_pattern`
  - `clamshell_dual_source_portrait_light`
  - `negative_fill_shadow_deepening_relation`
- 이 세 항목은 삭제하거나 재작성하지 않고 **재사용 및 회귀 검토 대상**으로 분류한다.
- 조사 시점 SHA-256:
  - `photo_prompt_tags.json`: `f635685b36b900f000a49181f03e3d797d0d36a39ed8b3458b9857dc82be3b40`
  - `photo_prompt_visual_obligations.json`: `017a9c3feb2764a20237106ba731a265b49444bc54dcd59205ef4217414aee53`

이 수치와 해시는 조사 스냅샷이지, 깨끗한 Git 기준선이나 이 작업의 변경 소유권 증명이 아니다.

### 3.3 구조적 공백

현재 데이터가 폭넓은 용어 검색에는 유리하지만 다음 공백이 남는다.

- `butterfly_lighting` 후보에는 코 아래 그림자가 언급되지만, 중앙축·그림자 위치·볼 모델링·catchlight·clamshell 배제 계약이 없다.
- `chiaroscuro`는 “high contrast” 한 문장으로 요약되어 형태 모델링과 단순 암부 증가를 구분하지 못한다.
- `golden_hour`는 따뜻한 역광 후보지만 낮은 태양 각도, 긴 그림자, 하늘-피사체 방향, warm grade 대체 금지가 없다.
- `prism_flare_light`는 굴절 색 줄무늬와 sparkle을 묶지만 lens ghost, veiling flare, diffraction starburst, post bloom과의 ownership 경계가 없다.
- `CRI`, `TLCI`, `SSI`가 후보화될 경우 “색이 좋아 보임”을 실제 측정값으로 오인할 위험이 있다.
- 후보 슬롯끼리 독립 추출되면 `soft key + hard shadow + flat fill + noir grade`처럼 인과적으로 충돌하는 팩이 만들어질 수 있다.

## 4. 출처 기반 의미 정리

### 4.1 hard/soft는 밝기가 아니라 shadow-edge transfer다

[ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)은 광질을 광원의 물리적 상대 크기와 그림자 경계 전이로 설명한다. 큰 확산면이나 바운스면은 작동 광원의 크기를 키워 더 넓은 전이를 만들고, 작은 광원은 경계가 선명한 그림자를 만든다. 광원의 세기 자체는 hard/soft의 정의가 아니다.

데이터 함의:

- `hard light`의 필수 증거는 짧은 penumbra, 일관된 cast-shadow 방향, 분명한 form shadow, 표면별 specular 응답이다.
- `soft light`의 필수 증거는 넓은 transition, 점진적인 form modeling, 넓은 specular, 열린 암부다.
- `hard = dark`, `soft = blurry`, `harsh = overexposed`를 금지 대체물로 둔다.
- softbox/umbrella/bounce는 결과를 만드는 방법일 뿐, hard profile의 픽셀 증거가 아니다.

### 4.2 key/fill/separation/background는 이름이 아니라 역할이다

ARRI는 key를 주 형상광, fill을 key가 만든 그림자를 두 번째 반대 그림자 없이 조절하는 광, separation/hair를 피사체와 배경을 분리하는 광, background light를 배경의 질감·색·방향 동기를 만드는 광으로 구분한다.

데이터 함의:

- “three-point lighting”은 세 램프를 그리는 계약이 아니다.
- 주 방향의 얼굴/물체 모델링, 그 그림자를 파괴하지 않는 fill, 배경에서 떨어지는 edge separation, 역할이 충돌하지 않는 shadow ownership가 필요하다.
- hard fill이 만든 이중 그림자, 배경 밝기만 올린 상태, rim만 있고 전면 정보가 없는 silhouette는 실패다.

### 4.3 인물 조명 패턴은 코·볼·얼굴 회전의 관계다

[Profoto의 고전 인물 조명 정리](https://www.profoto.com/us/en/still-photography/profoto-stories/character-portraits-with-john-russo-and-profoto-d2/ImportedBlogPage)는 다음 식별 단서를 제시한다.

- loop: 코 그림자가 아래·옆으로 내려가되 볼 그림자와 연결되지 않는다.
- Rembrandt: 코 그림자와 볼 그림자가 만나 반대쪽 눈 아래에 제한된 밝은 삼각형을 남긴다.
- split: 얼굴의 밝은 반과 어두운 반의 경계가 대체로 중앙축을 따른다.
- butterfly: 높은 정면광이 코 바로 아래에 중앙의 작은 그림자를 만든다.
- broad: 카메라에 더 많이 보이는 얼굴 면이 밝다.
- short: 카메라에 더 적게 보이는 얼굴 면이 밝고, 넓게 보이는 면은 어둡다.

데이터 함의:

- `Rembrandt`와 `loop`의 핵심 경계는 코 그림자와 볼 그림자의 연결 여부다.
- `broad/short`는 광원 방향만으로 판별할 수 없고 얼굴 회전과 밝은 면의 상대 관계가 필요하다.
- `butterfly`와 `clamshell`은 상부 key가 비슷하지만, clamshell은 하부 return과 high/low catchlight 관계를 추가로 가진다.
- 모든 인물 패턴은 특정 사람의 매력, 성격, 성별, 인종을 추론하지 않는다. 현재 프로필의 성인 제한은 요청된 인물 표현 범위만 보호한다.

### 4.4 high-key, low-key, chiaroscuro, tenebrism, noir는 같은 축이 아니다

[National Gallery의 chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro)는 밝고 어두운 톤의 대비를 이용해 입체 형태와 극적 효과를 만드는 기법으로 설명된다. [tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism)은 대부분 어두운 장 안에서 강한 밝은 부분을 고립시키는 경향에 더 가깝다. [BFI의 film noir 논의](https://www.bfi.org.uk/features/genres-where-draw-line)는 noir가 조명만으로 환원되지 않는 장르·서사·심리 범주임을 보여 준다.

제안 경계:

| 개념 | 소유해야 하는 가시적 관계 | 금지 대체물 |
|---|---|---|
| high-key | 밝은 톤 우세, 열린 암부, 하이라이트 디테일, 낮은 키-필 차이, 주 피사체 분리 | 전역 과노출, white clipping, 무채색 흰 배경만 |
| low-key | 어두운 톤 우세, 선택적 노출, 구조가 남는 암부, 명확한 시선 유도, 하이라이트 보존 | 전역 노출 부족, crushed black, 검은 의상만 |
| chiaroscuro | 빛-그림자가 형태를 모델링, 중간톤 연결, 방향성, 재질 변화 | 대비 슬라이더, 검은 배경, flat silhouette |
| tenebrism | 대부분 어두운 field, 급격히 고립된 밝은 pool, 주변의 절제된 단서, spotlight-like hierarchy | 일반 low-key, vignette, underexposure |
| noir | candidate style cluster | 조명 패턴 하나로 서사·시대·도덕성까지 hard 주장 금지 |

### 4.5 practical과 motivated는 “램프가 보인다”만으로 충분하지 않다

American Society of Cinematographers의 사례들은 practical이 프레임 안에 보이는 광원이고, 보이지 않는 보조광이 practical의 방향·색·범위를 이어 받아 장면을 증강할 수 있음을 보여 준다. motivated light는 무조건 현실주의나 우수한 조명과 동의어도 아니다.

필수 관계:

- 프레임 안의 plausible source
- source 주변의 밝기·색 falloff
- 피사체에 닿는 빛의 방향이 source와 일치
- 다른 ambient zone과 색/밝기 분리
- 그림자가 어느 광원에 속하는지 모순이 없음

`warm practicals + cool ambient`는 색보정만으로 만들 수 있으므로 visible source와 spatial ownership 없이 hard 통과시키지 않는다.

### 4.6 색온도·화이트밸런스·필터는 원인과 결과를 분리한다

[Nikon의 white balance 안내](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/setting-white-balance)는 WB가 중립 보정과 창의적 색 표현 모두에 쓰이고, 혼합광에서는 단일 설정이 장면 전체를 동일하게 중립화하지 못함을 설명한다. [Rosco Filter Facts](https://emea.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf)는 CTO/CTB, plusgreen/minusgreen, ND가 서로 다른 보정 목적을 가진다는 근거를 제공한다.

데이터 함의:

- `warm light`는 주황 재질, warm WB, warm grade와 분리해야 한다.
- `mixed color temperature`는 서로 다른 공간 zone과 경계 또는 중첩 증거가 필요하다.
- CTO/CTB/plusgreen/minusgreen은 사용자가 장비/필터를 명시했을 때 setup metadata로 보존하되, 색 결과만 보고 실제 젤을 추론하지 않는다.
- Kelvin, mired, Duv 수치는 요청 메타데이터로만 유지한다.

### 4.7 CRI·TLCI·SSI·SPD는 픽셀 스타일 용어가 아니다

- [CIE의 CRI 정의](https://cie.co.at/eilvterm/17-22-109)는 시험 광원과 기준 광원의 색 재현 비교 측정이다.
- [CIE의 colour fidelity 문서](https://www.cie.co.at/publications/colour-fidelity-index-accurate-scientific-use)는 CRI를 모든 목적의 완전한 품질 척도로 쓰는 데 한계가 있음을 다룬다.
- [EBU TLCI](https://tech.ebu.ch/publications/r137)는 카메라 시스템을 고려한 luminaire colorimetric performance 평가다.
- [SMPTE SSI](https://www.smpte.org/standards/ssi-standards)는 기준 SPD에 대한 스펙트럼 유사도 지표다.

따라서 `CRI 95`, `R9`, `TLCI`, `SSI`, `SPD`, `full spectrum`, `green spike`, `metamerism`은 다음 정책을 따른다.

- 수치나 장비 스펙을 hard visual profile로 만들지 않는다.
- 사용자가 명시한 수치는 원문 그대로 setup/capture metadata에 보존한다.
- 색이 자연스럽게 보인다는 이유로 특정 지수나 스펙트럼을 역추론하지 않는다.
- 색 분리, 피부색 편향, green/magenta cast는 별도의 관찰 가능한 결과 후보로만 표현한다.

### 4.8 inverse-square, EV, ratio는 구도 효과로 번역하되 수치는 주장하지 않는다

[IES inverse-square 정의](https://ies.org/definitions/inverse-square-law/)는 점광원 이상화에서 조도가 거리 제곱에 반비례하고, 유한한 큰 광원 근거리에서는 단순 적용이 제한됨을 명시한다.

데이터 함의:

- `rapid falloff`는 가까운 피사체와 먼 배경의 밝기 차, 공간 거리 앵커, 일관된 방향으로 번역한다.
- “2:1 ratio”, “4:1 ratio”, “one stop fill”은 요청 메타데이터다.
- 렌더 리뷰는 정확한 ratio를 측정했다고 주장하지 않고, low/moderate/high relative separation만 판정한다.
- `inverse-square look`이라는 모호한 명칭은 hard activation 금지다.

### 4.9 flare, ghosting, bloom, glow, halation은 서로 다른 차선이다

[ZEISS의 렌즈 반사 설명](https://lenspire.zeiss.com/photo/en/article/technical-article-on-t-coating-and-reduction-of-reflections-in-lenses/)은 내부 반사가 ghost image와 전역적인 haze/contrast loss를 만들 수 있음을 설명한다. [Kodak의 motion-picture film processing 자료](https://www.kodak.com/content/products-brochures/Film/Processing-KODAK-Motion-Picture-Films-Module-15.pdf)는 anti-halation 구조가 밝은 빛의 필름 내 산란과 halo를 줄이는 역할을 다룬다. [Adobe Lightroom 문서](https://helpx.adobe.com/lightroom/desktop/edit-photos/edit-photos.html)는 tone, clipping, color grading, clarity, dehaze, grain을 서로 다른 편집 제어로 분리한다.

| 용어 | 제안 가시적 계약 | 혼동 금지 |
|---|---|---|
| ghosting flare | 밝은 원광과 정렬된 반복 ghost, 조리개/렌즈 축을 따르는 위치 관계 | 임의 lens-leak overlay, 무지개 프리즘 |
| veiling flare | 강한 광원 쪽에서 넓은 haze와 국소 대비·black density 감소 | 안개 전체, 저대비 grade |
| bloom/glow | 고휘도 경계 주변의 부드러운 밝기 확산 | 실제 lens ghost, halation 색 번짐 |
| halation look | 강한 하이라이트 가장자리 바깥의 얇고 국소적인 warm/red-biased halo, 내부 디테일 보존 | 전역 glow, chromatic aberration, flare orb |
| starburst | 밝은 점광원에서 aperture-blade 회절과 연결된 방사형 spike | 그려 넣은 별, lens ghost |

실제 필름 스톡이나 현상 공정은 이미지 한 장으로 증명하지 않는다. `film halation look`만 표현한다.

### 4.10 golden hour와 blue hour는 색 하나가 아니라 공간·시간 단서 묶음이다

[PhotoPills의 golden/blue-hour 설명](https://www.photopills.com/articles/mastering-golden-hour-blue-hour-magic-hours-and-twilights), [NASA의 crepuscular rays 설명](https://science.nasa.gov/earth/earth-observatory/crepuscular-rays-and-light-scattering-150090/), [NOAA의 붉은 하늘 설명](https://gmd-int.cmdl.noaa.gov/grad/about/redsky/)을 함께 보면, 낮은 태양 각도·긴 대기 경로·산란·태양 고도와 지평선의 관계가 색만큼 중요하다.

제안 경계:

- golden-hour look: 낮은 방향의 따뜻한 직사광, 긴 그림자, 차가운/중립적인 열린 하늘 fill, 밝은 테두리 또는 긴 grazing highlight, 실제 낮은 광원 방향.
- blue-hour look: 태양 원반이 보이지 않는 twilight ambient, 깊은 청색/중립 하늘, 켜진 practical의 따뜻한 국소 pool, 하늘과 인공광의 밝기 균형.
- warm grade를 golden hour로, cool night grade를 blue hour로 통과시키지 않는다.
- 실제 촬영 시각, 위도, 날씨는 추론하지 않는다.

## 5. 제안 시각 프로필

세부 구성요소와 gate는 `candidate-data-proposal.json`에 구조화했다. 우선순위 요약은 다음과 같다.

### 5.1 재사용·감사 대상

| ID | 상태 | 감사 포인트 |
|---|---|---|
| `rembrandt_face_light_pattern` | 현재 작업트리에 존재 | loop·split cross-negative, cheek triangle의 thumbnail salience |
| `clamshell_dual_source_portrait_light` | 현재 작업트리에 존재 | butterfly single-key, ring catchlight, 하부 underlight 배제 |
| `negative_fill_shadow_deepening_relation` | 현재 작업트리에 존재 | 검은 플래그를 꼭 그리게 하는 과적합 여부, local shadow와 global grade 경계 |

### 5.2 P0 프로필 후보

1. `hard_light_shadow_edge_relation`
2. `soft_light_shadow_edge_relation`
3. `loop_face_light_pattern`
4. `butterfly_face_light_pattern`
5. `split_face_light_pattern`
6. `broad_face_light_orientation_relation`
7. `short_face_light_orientation_relation`
8. `key_fill_separation_background_roles`
9. `backlit_rim_edge_separation_relation`
10. `backlit_silhouette_mass_relation`
11. `high_key_tonal_distribution`
12. `low_key_selective_illumination`
13. `chiaroscuro_form_modeling_relation`
14. `tenebrist_dark_field_isolation`
15. `direct_on_camera_flash_snapshot_signature`
16. `motivated_practical_mixed_interior_relation`
17. `volumetric_occluded_light_shafts`

### 5.3 P1 프로필 후보

1. `golden_hour_low_sun_relation`
2. `blue_hour_ambient_practical_balance`
3. `lens_ghosting_flare_alignment`
4. `veiling_flare_contrast_loss_relation`
5. `film_halation_highlight_edge_relation`

P1은 의미가 덜 중요해서가 아니라, 생성기가 이름만 모방해 색·overlay로 대체하기 쉬워 먼저 P0의 회귀 기반을 세우는 편이 안전하기 때문이다.

## 6. 후보팩 강화안

후보팩은 장비 한 개나 분위기 단어 한 개가 아니라 서로 맞물리는 cluster로 구성한다.

| cluster | 1차 시각 목표 | 주요 slot | 핵심 금지 대체물 |
|---|---|---|---|
| `clean_beauty_clamshell` | 상부 soft key + 약한 하부 return + 깨끗한 catchlight | lighting, direction, type, intensity, shape, color, grading | ring-light disk, shadowless retouch |
| `soft_window_open_shadows` | 큰 창 방향, 넓은 전이, 열린 암부, 자연스러운 falloff | same | flat studio wash, blue window tint only |
| `rembrandt_studio_drama` | cheek triangle와 낮은 fill | same | generic side light, split face |
| `hard_side_editorial` | 짧은 penumbra, raking side, graphic cast shadow | same | contrast grade only |
| `luxury_controlled_specular` | 재질별 specular 분리, deep but detailed black | same | random gold glare, crushed black |
| `motivated_warm_practical_cool_ambient` | visible warm source와 cool ambient zone의 ownership | same | teal-orange LUT only |
| `noir_gobo_silhouette` | hard patterned pool, negative fill, 선택적 silhouette | same | noir label only, costume stereotype |
| `golden_hour_backlit_portrait` | low warm backlight, rim, long shadow, neutral sky fill | same | warm grade only |
| `blue_hour_city_practical` | twilight blue ambient와 따뜻한 practical의 균형 | same | midnight cyan grade |
| `direct_flash_y2k_snapshot` | near-axis hard flash, sharp near shadow, dark ambient background | same | studio strobe label, overexposure |
| `filmic_muted_halation` | highlight-edge halo, gentle rolloff, muted saturation, grain | lighting, shape, color, grading, film | bloom overlay, vintage preset name |
| `volumetric_haze_shafts` | source-occluder-medium-surface로 이어지는 shafts | lighting, direction, type, intensity, shape, color | flare streak, fog alone |

각 cluster는 하나의 primary tag를 갖고, 모든 항목에 `requires_primary_any_tags`를 둔다. 동일 query에서 cluster 항목이 함께 상위 후보에 나타나는지 검사하되, 검색 순위 통과를 렌더 성공으로 보고하지 않는다.

## 7. 장비·측정값·후보정 처리 정책

### 7.1 candidate/setup metadata 전용

- 장비: softbox, octabox, stripbox, umbrella, beauty dish, lantern, Fresnel, optical snoot
- 제어: grid, barn door, snoot, flag, cutter, gobo, scrim, reflector, V-flat
- 광원: LED, COB, HMI, tungsten, fluorescent, speedlight, strobe
- 측정: lux, foot-candle, EV, stop, exact ratio, beam angle, CCT, mired, Duv
- 품질 지표: CRI/Ra, R9, TLCI, SSI, SPD
- 필터: CTO, CTB, CTS, plusgreen, minusgreen, ND, product gel code

정책:

- 사용자가 명시하면 보존한다.
- 픽셀에서 장비나 측정값을 역추론하지 않는다.
- 장비 후보는 기대 효과를 함께 기술한다. 예: `large softbox`는 “넓은 shadow transition과 broad specular”를 후보로 제안하되 실제 장비 설치를 주장하지 않는다.
- modifier는 서로 겹치는 signature가 많으므로 bare term은 candidate-only다.

### 7.2 postprocess lane 전용

- tone curve, RGB curve, lift/gamma/gain, offset
- HSL, color mixer, color wheels, split toning, selective color
- LUT, film emulation, print emulation
- grain, bleach-bypass look, cross-process look, fade, gate-weave look
- global bloom/glow, diffusion filter look

조명 profile과 조합할 수 있지만 소유권은 섞지 않는다. 예를 들어 low-key profile이 통과하려면 tone curve가 아니라 선택적 조명 구조가 먼저 보여야 한다.

## 8. 회귀·평가 설계

### 8.1 구조 검사

- 모든 hard profile은 정확히 5개 이상의 component group, evidence field, render gate, reject substitute를 가진다.
- exact term은 영문·한글의 좁은 문맥 구로만 구성한다.
- bare `soft`, `hard`, `dramatic`, `moody`, `cinematic`, `noir`, `warm`, `cool`, `glow`는 hard activation 금지다.
- candidate cluster의 모든 항목은 source ID와 하나의 primary cluster를 가진다.
- 장비·수치 용어는 visual profile ID를 가질 수 없다.

### 8.2 라우팅 회귀

| 양성 | held-out 교차 음성 |
|---|---|
| Rembrandt cheek triangle | loop의 분리된 코 그림자, split 반면광 |
| butterfly centered nose shadow | clamshell의 하부 return, underlight |
| broad lighting | short lighting |
| rim edge separation | silhouette dark mass |
| high-key detailed whites | clipped white frame |
| low-key selective pool | global underexposure/crushed black |
| chiaroscuro form modeling | contrast slider/dark background |
| tenebrism | generic low-key |
| motivated practical | colored grade with no visible source |
| golden hour | warm midday grade |
| blue hour | cyan night grade |
| lens ghosting | prism rainbow, light leak, bloom |
| film halation | veiling flare, chromatic aberration, glow |

추가 규칙:

- exact/context term: 한 프로필만 hard 활성화
- negated term: hard 활성화 금지
- component paraphrase: optional discovery는 가능하지만 exact hard activation은 금지
- embedding/BM25F-only hit: advisory candidate만 허용
- 장비명만 있는 query: setup candidate는 허용하지만 pixel profile hard activation은 금지
- 선택된 프로필만 composed prompt의 필수 필드를 갖고, 선택되지 않은 프로필의 gate가 새어 나오지 않아야 한다.

### 8.3 후보 검색 회귀

- 12개 cluster 각각에 대해 대표 영문·한글 query를 분리한다.
- 각 query의 상위 후보에 cluster의 핵심 5개 slot이 함께 있어야 한다.
- 다른 cluster의 상충 항목이 함께 들어오면 실패다.
- `direct flash` query가 `soft window`, `film halation` query가 `lens ghost`, `golden hour` query가 `warm practical interior`를 강제하지 않아야 한다.
- 후보 순위 결과는 검색 일관성 증거이지 prompt 또는 pixel 품질 증거가 아니다.

### 8.4 이후 렌더 평가

초기 조사 단계에서는 실행하지 않았고, 후속 구현에서 아래 원칙으로 3개 독립 arm을 실행했다.

- 독립된 arm마다 입력을 동결한다.
- arm당 기록된 생성 1회, 숨은 재시도 금지.
- 출력이 없으면 `UNSCORED`; 품질 0점으로 해석하지 않는다.
- 각 profile의 모든 gate가 통과해야 한다. `partial_is_fail`.
- thumbnail은 첫눈의 패턴, native는 그림자 연결·halo·catchlight·클리핑을 검토한다.
- prompt/runtime PASS는 pixel PASS가 아니다.
- 사용자 미감과 의미 판단은 별도 평가다.

추천 첫 6개 독립 arm:

1. Rembrandt vs loop
2. butterfly vs clamshell
3. rim vs silhouette
4. high-key vs clipped exposure
5. low-key vs underexposure
6. halation vs ghosting/veiling flare

## 9. 구현 순서 제안

1. **P0-1 광질·패턴**: hard/soft, loop, butterfly, split, broad/short
2. **P0-2 역할·명암**: three-point roles, rim, silhouette, high/low-key
3. **P0-3 미학·장면 인과**: chiaroscuro, tenebrism, direct flash, practical, volumetric
4. **P1 자연광·광학·필름**: golden/blue hour, ghosting, veiling flare, halation
5. **후보 cluster**: 12개 cluster를 extension으로 추가하고 primary-tag coherence 테스트
6. **인덱스**: generated visual/semantic index는 source와 테스트가 안정된 뒤 스크립트로 재생성
7. **프롬프트 평가**: exact, negation, close substitute, candidate discovery, no-leak 회귀
8. **렌더 평가**: 독립 arm과 엄격한 gate 판정

한 번에 전부 구현하면 어느 프로필이나 후보 묶음이 회귀를 만들었는지 분리하기 어렵다. 위 순서는 의미 축을 격리하기 위한 실험 순서다.

## 10. 증거 한계

### 현재 확인됨

- 참조 대화의 24개 어휘 범주
- 외부 출처가 지지하는 정의·구분·측정 한계
- 현재 저장소의 후보 슬롯 수와 현재 작업트리에 보이는 프로필
- 제안 JSON·JSONL의 구조 및 내부 참조 무결성
- 22개 신규 hard profile, 12개 cluster와 84개 후보의 런타임 병합 및 인덱스 생성
- exact/negation/close-substitute/metadata 경계와 BM25F cluster 검색 회귀
- 독립된 3개 후보팩, composed prompt, runtime request, 단일 이미지 호출 계보
- Arm A와 C의 5/5 strict pixel gate, Arm B의 1/5 및 전체 11/15 판정
- 세 공개 v6 후보팩에서 hard profile은 노출되지만 목표 cluster·anchor candidate ID는 미노출됨

### 설계 추론

- 5개 component group의 정확한 문구
- 후보 cluster의 슬롯 구성과 ID
- priority P0/P1
- 생성기에 가장 잘 전달될 prompt wording

### 아직 확인되지 않음

- 이번 실행에서 렌더하지 않은 19개 신규 hard profile의 픽셀 충실도
- 공개 v6 후보팩에서 신규 cluster·anchor candidate를 composer가 직접 선택하는 경로
- Arm B의 volumetric shaft 관계 성공
- focused 범위를 넘는 embedding 검색 품질과 전체 테스트 스위트
- 사용자 선호 및 최종 판단

## 10.1 후속 구현·3-arm 결과

후속 구현은 `photo_prompt_lighting_extension.json`에 12개 cluster와 84개 후보를 추가하고, visual-obligation registry에 22개 신규 hard profile을 반영했다. 생성 인덱스는 300 profiles / 1,568 exact terms와 7,974 semantic entries / 768 dimensions / 16 shards로 재생성했다. focused 10개와 관련 21개, 총 31개 회귀가 통과했고, 각 cluster의 7개 후보는 완전 구성요소 BM25F query의 top 14 안에 모두 나타났다.

첨부 portrait는 보이는 성인 외형 참고로만 사용했다. identity, same-person, biometric, protected-trait, nationality, ethnicity, personality, occupation은 추론하지 않았다. 각 arm은 입력과 seed를 동결하고 native imagegen 1회만 호출했으며 retry, fallback, cross-arm input은 모두 0이다.

| Arm | 복합 컨셉 | 목표 의미 | 픽셀 결과 | 공개 후보팩 후보 노출 |
|---|---|---|---:|---|
| A | 진눈깨비 신호실의 기상 일지 제본 | motivated warm practical / cool ambient | 5/5 PASS | FAIL |
| B | 해안 안개 수확 시설의 메쉬 수리 | occluded volumetric shafts | 1/5 FAIL | FAIL |
| C | 거울 징 실험실의 반사막 파문 | local film-halation edge | 5/5 PASS | FAIL |

Arm B는 구름 틈과 메쉬라는 장애물만 읽혔다. source-anchored shaft, 공기 중 bounded path, 밝은 shaft와 어두운 gap의 분리, 수광면에 닿는 bounded shaft가 없으므로 `partial_is_fail`에 따라 실패다. 세 arm 모두 hard profile과 5개 gate는 public pack에 노출됐지만, 목표 cluster ID와 forced anchor candidate ID는 공개 표면에 없었다. 따라서 hard-profile 경로의 픽셀 결과와 신규 candidate record의 공개 선택 성공을 서로 대체하지 않는다.

상세 실행 보고서는 `artifacts/photo-runs/20260902-lighting-three-arm-reference-v1/aggregate_report.md`, root 교차판정은 `shared/root_pixel_cross_review.json`에 있다.

## 11. 출처

1. [ARRI Lighting Handbook](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf)
2. [Profoto — classic portrait lighting patterns](https://www.profoto.com/us/en/still-photography/profoto-stories/character-portraits-with-john-russo-and-profoto-d2/ImportedBlogPage)
3. [Profoto — broad lighting](https://www.profoto.com/gb/en/still-photography/tips-tricks/how-to-create-broad-lighting/ImportedBlogPage)
4. [Profoto — flash basics and hard/soft light](https://www.profoto.com/us/en/still-photography/profoto-stories/flash-photography-for-beginners-profoto-a1x/ImportedBlogPage)
5. [Nikon — setting white balance](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/setting-white-balance)
6. [Rosco Filter Facts](https://emea.rosco.com/sites/default/files/content/resource/2022-10/Rosco_FilterFacts09_22.pdf)
7. [CIE — colour rendering index](https://cie.co.at/eilvterm/17-22-109)
8. [CIE — colour fidelity index for scientific use](https://www.cie.co.at/publications/colour-fidelity-index-accurate-scientific-use)
9. [EBU — TLCI and TLMF](https://tech.ebu.ch/publications/r137)
10. [SMPTE — Spectral Similarity Index](https://www.smpte.org/standards/ssi-standards)
11. [IES — inverse-square law](https://ies.org/definitions/inverse-square-law/)
12. [Adobe Lightroom editing controls](https://helpx.adobe.com/lightroom/desktop/edit-photos/edit-photos.html)
13. [Kodak — motion-picture film processing module](https://www.kodak.com/content/products-brochures/Film/Processing-KODAK-Motion-Picture-Films-Module-15.pdf)
14. [Kodak — processing techniques](https://www.kodak.com/en/motion/page/processing-techniques/)
15. [ZEISS — lens reflections and flare](https://lenspire.zeiss.com/photo/en/article/technical-article-on-t-coating-and-reduction-of-reflections-in-lenses/)
16. [Nikon — aperture starburst](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/bright-idea-adding-star-power)
17. [National Gallery — chiaroscuro](https://www.nationalgallery.org.uk/paintings/glossary/chiaroscuro)
18. [National Gallery — tenebrism](https://www.nationalgallery.org.uk/paintings/glossary/tenebrism)
19. [BFI — genre boundary and film noir](https://www.bfi.org.uk/features/genres-where-draw-line)
20. [ASC — motivated and unmotivated lighting discussion](https://staging.ascmag.com/articles/shadows-and-shivers-for-blood-simple)
21. [ASC — visible practical and augmenting unit example](https://staging.ascmag.com/articles/manhattan-black-and-white-romantic-realism)
22. [PhotoPills — golden hour, blue hour, and twilight](https://www.photopills.com/articles/mastering-golden-hour-blue-hour-magic-hours-and-twilights)
23. [NASA — crepuscular rays and scattering](https://science.nasa.gov/earth/earth-observatory/crepuscular-rays-and-light-scattering-150090/)
24. [NOAA — red sky and atmospheric scattering](https://gmd-int.cmdl.noaa.gov/grad/about/redsky/)

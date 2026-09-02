# Topic 14 — Negative constraints, false substitutes, anatomy/object artifacts, failure prevention

## 상태와 제한된 결론

- **결정: `proposed`**
- 연구/설계 전용이다. 런타임 자산, 생성 인덱스, 테스트, 스킬 문서는 수정하지 않았다.
- 동결 코퍼스의 비어 있지 않은 프롬프트 **924개 전수**를 휴리스틱 스캔했고, 초기·중기·후기에 걸친 **21개 게시물의 실제 이미지 42장**을 직접 보았다.
- 핵심 결론은 negative 목록을 더 길게 만드는 것이 아니라 다음 순서로 실패 예방을 소유시키는 것이다.

  `요청된 positive invariant → 적용 대상/가시성 → 허용되는 의도적 변형 → 국소 실패 징후 → 올바른 소유 레이어 → thumbnail/native gate`

- 코퍼스의 `no text, logo, watermark, extra fingers, CGI, plastic skin...` 같은 반복 빈도는 전역 기본값의 근거가 아니다. 저해상도, 모션 블러, fisheye, 일러스트, 포장 타이포처럼 같은 단어가 **요청된 효과**인 사례가 실제로 존재한다.
- 새 broad visual-obligation profile은 제안하지 않는다. 일반 결함은 topic-neutral 품질/guard 계약이 소유하고, 의미의 false substitute는 이미 활성화된 **좁은 exact visual profile의 `reject_substitutes`와 render gates**가 소유해야 한다.
- 이번 픽셀 관찰은 코퍼스 출처 이미지에 대한 증거일 뿐, 제안 설계의 새 독립 렌더 검증이 아니다. 구현, 새 렌더 qualification, 사용자 판단은 모두 **`UNSCORED`**이다.

## 1. 범위와 방법

### 1.1 동결 경계

- manifest: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 모수: 1,182 posts, 4,908 images, 924 non-empty prompts, 904 unique prompt bodies, 258 missing prompts, IDs 1565–2746.
- target skill baseline: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- authored source는 동시 작업 중인 working tree와 섞지 않기 위해 해시가 고정된 snapshot commit `401f450e4c0ec32ef79c502e3c6a6666c9a106c4`에서 읽었다.
  - `photo_prompt_tags.json`: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - `photo_prompt_visual_obligations.json`: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - `photo_prompt_quality_layers.json`: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`

증거 레이어를 다음처럼 분리했다.

1. manifest 프롬프트 텍스트의 출현량.
2. 이미 전달된 코퍼스 픽셀의 직접 관찰.
3. 동결 authored assets와 현재 guard 함수의 소유권/동작 검사.
4. 제안 설계와 아직 수행하지 않은 검증.

### 1.2 프롬프트 전수 스캔

924개 `.prompt`를 소문자화해 다음 의미군을 대소문자 무시 정규식으로 검색했다.

- instruction-shaped directive: 문장/절 시작의 `no`, `without`, `avoid`, `exclude`, `do not`, `don't`, `never`.
- anatomy/hand negative: extra/missing/fused/warped/distorted/malformed 등과 finger/hand/limb/anatomy의 결합.
- text/brand: text, lettering, typography, signage, logo, watermark, signature의 제외·오류 문맥.
- medium/style suppression: CGI, 3D, anime, illustration, cartoon, painterly의 제외 문맥.
- skin/processing failure: plastic, waxy, airbrushed, beauty-filter, over-smoothed, over-retouched 등.
- identity boundary: `do not copy`, new/original identity, sole identity reference 등.
- object geometry: warped/fused/melted/floating/broken object, product, jewelry, wall, reflection 등.
- intentional artifact: low resolution, motion blur, compression/JPEG artifact, grain, moire, chromatic aberration, lens distortion, fisheye 등.
- dense negative footer: `No ...` 형식의 한 절이 80자 이상인 경우.

이는 문맥 분류기가 아니다. 예를 들어 `plastic-looking skin`은 대개 방지어지만, `cartoon style`이나 `low resolution`은 요청 효과일 수도 있다. 따라서 아래 수치는 **프롬프트 쪽 표현량**이고, 결함 발생률이나 negative 효과의 인과 증거가 아니다.

### 1.3 픽셀 표본

- early 1565–1958: 6 posts / 12 images.
- middle 1959–2352: 7 posts / 14 images.
- late 2353–2746: 8 posts / 16 images.
- 총 **21 posts / 42 images**.
- 각 게시물에서 manifest 순서상 `download_ok=true`인 첫 두 이미지를 고정했다.
- 양성은 손/물체 접촉, intentional artifact, text surface, exact semantic exclusion, long negative footer를 넓게 포함하도록 고르고, 인접한 no/short-negative controls도 포함했다.
- 42장 모두 접촉 시트에서 비교하고, 텍스트·손·물체·접촉이 핵심인 14장은 native 파일로 확대 확인했다.

## 2. 프롬프트 쪽 발견

### 2.1 전체 계수

| 휴리스틱 | posts | unique prompts | 해석 |
|---|---:|---:|---|
| instruction-shaped negative directive | 507 | 494 | 전체의 54.9%; semantic exclusion과 결함 방지 모두 포함 |
| `No ...` dense footer ≥80 chars | 96 | 94 | 긴 쉼표 목록 형태 |
| text/brand failure or exclusion | 386 | 377 | no-text와 unreadable-text가 혼재 |
| anatomy/hand negative | 303 | 300 | 가시성·관계와 무관한 footer도 포함 |
| positive anatomy/coherence wording | 105 | 105 | `correct/coherent/natural anatomy` 등 넓은 표현 |
| medium/style suppression | 170 | 166 | CGI/3D/anime/illustration/cartoon 등 |
| skin/processing failure terms | 473 | 463 | plastic/waxy/beauty-filter/smoothing 등 |
| identity/reference boundary | 69 | 67 | 동일성 자체를 픽셀에서 판단하지 않음 |
| people/count exclusion | 257 | 252 | extra/background people와 exact no-people 혼재 |
| object-geometry failure | 55 | 55 | warped/fused/melted/floating object 등 |
| blur/DoF exclusion | 77 | 77 | exact deep-focus 요구도 포함 |
| exposure/color failure | 112 | 109 | clipped highlights, crushed shadows, colored skin 등 |
| content/wardrobe/safety-like suppression | 31 | 30 | 전역 자동 negative로 수입 금지 |
| intentional capture/artifact language | 181 | 175 | 결함처럼 보일 수 있으나 요청된 효과일 수 있음 |

자주 나온 표면 표현은 다음과 같았다. 동일 프롬프트에서 여러 표현이 함께 나올 수 있다.

| literal family | posts | unique prompts |
|---|---:|---:|
| watermark | 470 | 461 |
| logo | 368 | 361 |
| no text/lettering/signage | 198 | 192 |
| extra fingers | 133 | 133 |
| extra limbs/arms/legs/hands | 73 | 72 |
| unrealistic/malformed/warped hands | 162 | 162 |
| correct/coherent/plausible anatomy | 71 | 71 |
| CGI/3D | 210 | 209 |
| anime/cartoon/illustration | 213 | 209 |
| plastic/waxy skin | 361 | 358 |
| beauty-filter/smoothing | 117 | 115 |
| unreadable/garbled/misspelled text | 36 | 36 |
| warped/deformed object or product | 20 | 20 |

### 2.2 ID 구간별 변화

| 구간 | prompt posts | directive | anatomy/hand | text/brand | medium/style | identity boundary | object geometry |
|---|---:|---:|---:|---:|---:|---:|---:|
| early | 382 | 77 | 8 | 47 | 10 | 2 | 0 |
| middle | 285 | 237 | 129 | 161 | 66 | 33 | 12 |
| late | 257 | 193 | 166 | 178 | 94 | 34 | 43 |

후반으로 갈수록 negative footer와 구체 결함어가 급증했다. 그러나 이는 작성 양식 변화다. 후반 이미지가 더 성공했다거나, 긴 목록이 성공 원인이라는 결론은 지지하지 않는다.

### 2.3 구조적 해석

1. **결함어는 가시성 조건 없이 반복된다.** 손이 프레임 밖인 셀피에도 `malformed hands, extra fingers`가 붙는다. 픽셀 검토에서 보이지 않는 손은 PASS가 아니라 `not_applicable` 또는, 손이 요청상 보여야 했다면 `missing_required_region=FAIL`이다.
2. **semantic exclusion과 defect suppression이 한 목록에 섞인다.** `no other people`, `blank screen`, `no background blur`는 장면 의미이고, `fused fingers`, `warped geometry`는 렌더 결함이다. 같은 lane에 두면 의미가 삭제될 수 있다.
3. **요청된 효과가 결함 용어와 겹친다.** low-resolution phone photo, motion blur, compression artifact, fisheye distortion, anime-style cosplay, illustrated portrait, package typography는 실제 코퍼스 요청이다.
4. **negative-only 성공 조건이 없다.** 1857처럼 요청 주체 자체가 사라진 경우 `no text/logos/signature`가 지켜져도 이미지가 성공할 수 없다. 먼저 positive invariant가 존재해야 한다.

## 3. 픽셀 쪽 관찰

| ID | 프롬프트 쪽 주장 | 두 이미지에서 보인 것 | 의미 |
|---:|---|---|---|
| 1586 | 별도 negative 목록 없는 겨울 공원 인물 | 주 피사체, 전화기, 눈길과 조명이 모두 읽히며 심각한 구조 파손 없음 | 긴 negative가 기본 coherence의 필요조건이 아님 |
| 1587 | fisheye, cartoon sweat drops, 초현실 고양이 | 곡률·근접 과장·코믹 장식이 함께 보임 | cartoon/fisheye를 전역 결함으로 막으면 요청 의미를 지움 |
| 1662 | tilt-shift miniature와 package title/typography | 큰 제목은 읽히고 미세 문구는 일부 장식적·불안정; 모형을 든 손/상자가 함께 보임 | text는 대상 surface와 요구 legibility 수준을 지정해야 함 |
| 1834 | anime-style cyber cosplay, bunny-ear headphones, sci-fi guitar weapon | photoreal cosplay와 장착형 토끼귀 헤드셋, 큰 소품이 읽힘 | `costume shortcut`은 nekomimi exact profile의 경계이지 cosplay 전역 금지가 아님 |
| 1857 | `Person and [XXX]`, 두 측면 인물, illustration, no text/logo/signature | 두 이미지 모두 요청한 두 주체가 없는 어두운 작업실/복도이며 실제 라벨성 글자도 보임 | unresolved placeholder 또는 prompt/image mismatch 가능성. positive subject gate가 먼저 실패 |
| 1939 | full-body, 양손 역할, metallic clutch; 긴 bad-hands/style/text footer | 전신, 양손, pedestal/clutch 관계가 대체로 일관적 | 보이는 성공을 negative 목록의 인과 효과로 돌릴 수 없음 |
| 2076 | exact no soft-focus blur, near/subject/far 모두 읽힘 | 곤돌라 내부, 인물, 창밖 산이 모두 읽힘 | 요청에 근거한 국소 semantic exclusion은 유효 |
| 2078 | instruction-shaped negative 없는 high-close street frame | 극단 시점에도 주체·다리·바닥 관계가 유지됨; 일부 손은 크롭/가림 | 명시 negative가 없어도 장면 coherence 가능; 숨은 손은 anatomy PASS 아님 |
| 2134 | low-resolution phone, motion blur, noise, compression artifacts 요청 | 부드럽고 낮은 해상도인 오래된 폰 사진 느낌이 보임 | `low resolution`/blur/artifact 자동 negative와 직접 충돌 가능 |
| 2158 | skyline/architecture/hand/style 결함을 길게 제외 | 얼굴·팔 길이 셀피와 환경은 읽히지만 손은 프레임 밖 | hand negative는 이 프레임에서 score 불가 |
| 2246 | 한 손은 swing support를 잡고 다른 손은 위로 자유롭게 뻗음 | native에서 grip contact와 free hand가 분리되어 읽힘 | positive actor-hand-support relation이 generic bad-hands보다 검증 가능 |
| 2299 | broken hands, distorted glasses, plastic smoothing 등 제외 | 안경·온실 기하·전경 잎은 읽히며 손은 대부분 가려짐 | profile별 가시성 조건 필요 |
| 2317 | angle/crop/outfit/identity와 여러 결함을 dense negative로 고정 | arm-to-camera, chair, monitors가 읽힘. 화면 글자는 지배적이지 않음 | 의미 잠금과 결함 방지를 같은 negative 목록에 넣지 말아야 함 |
| 2490 | cone pinch, 반대 손 지지, no phone/people/hands/text/logo 등 | 양손/아이스크림/세탁기 접촉은 대체로 coherent; 배경 상품 상자에 pseudo-lettering 존재 | 환경 소품과 no-typography가 긴장. surface-local text mode가 필요 |
| 2623 | cheek-cradling hand와 texture; plastic/waxy/airbrush/hand/style 긴 목록 | 손가락/볼 접촉은 읽히나 피부는 native에서도 매우 매끈함 | negative와 positive texture 문구가 있어도 픽셀 생존을 보장하지 않음 |
| 2641 | extreme fisheye가 가까운 손을 크게 만듦; malformed hand와 unrealistic proportions 제외 | 가까운 손의 크기 과장은 강하지만 주요 손가락·관절은 대체로 구분됨; 두 번째는 일부 blur/crop | projection-consistent stretch를 anatomy defect로 오판하면 안 됨 |
| 2666 | office selfie, no text/logo/malformed hand 등 | arm은 보이나 손은 프레임 밖, 사무실 물체는 읽힘 | 손 결함 gate는 N/A; 손 자체가 필수였으면 visibility failure |
| 2675 | 양팔을 카메라로 뻗음, desk paper는 unreadable markings; no readable text 등 | 팔은 보이고 손은 크롭, 문서는 의미 없는 작은 표시로 남음 | `abstract_nonlegible` text mode의 유효 사례; hand PASS는 아님 |
| 2680 | blank tablet, object full visibility, no people/hands/extra/duplicate/warp/text | blank screen과 주요 제품 기하는 성공; 가장자리 cup/mouse/pens 일부가 잘림 | negative 목록보다 `every object fully visible` positive gate가 실제 실패를 찾음 |
| 2711 | one hand, separate fingers, flower-stem contact; `keep frame free from...` 목록 | 꽃줄기 pinch와 손가락 분리는 대체로 읽힘 | 국소 positive relation이 유용. `keep ... free from`도 blanket-negative 변형으로 분류 필요 |
| 2742 | wet-hair beauty, malformed pupil/duplicate/extra limb/style/text 제외 | 손/물체는 없고 얼굴·젖은 머리·방울은 읽힘 | 관련 없는 anatomy 항목은 N/A; texture/face만 검토 가능 |

### 3.1 프롬프트/픽셀 정렬

- exact local state는 검증 가능했다: 2076의 환경까지 읽히는 deep focus, 2680의 blank screen, 2246과 2711의 contact relation.
- 요청된 artifact도 검증 가능했다: 2134의 낮은 해상도·softness, 2641의 fisheye 크기 과장, 1662의 package typography.
- 보이는 구조 관계를 먼저 쓴 사례가 단순 `bad hands` 목록보다 판정하기 쉬웠다.

### 3.2 발산과 false confidence

- 1857은 필수 주체가 사라졌고 no-text까지 지켜지지 않았다. negative 수가 많거나 적다는 것보다 **필수 positive presence**가 먼저다.
- 2623은 anti-plastic wording이 있어도 skin smoothing이 남는다. prompt presence는 pixel PASS가 아니다.
- 2680은 blank-screen gate는 통과하지만 full-object-visibility는 실패한다. 여러 독립 게이트의 부분 성공을 평균내면 안 된다.
- 2158, 2666, 2675처럼 손이 프레임 밖이면 `malformed hand 없음`을 anatomy 성공으로 세면 안 된다.
- 2641의 큰 손은 의도된 투영 효과다. 크기 비례 하나만으로 anatomy failure를 판정하면 false positive다.

## 4. 기존 소유권과 간극

### 4.1 `photo-negative-intent-guard/v1`: 유지해야 할 강점

정상 v5/v6 경로는 이미 다음을 제공한다.

- modern core의 `baseline_prompt_en`과 최종 `prompt_en`에서 `No...`, `Do not...`, `Avoid...`, `never touching...` 같은 instruction-shaped blanket negative를 차단.
- 자동 `negative_en`을 intent-neutral photographic/render defect vocabulary로 제한.
- requester exclusion은 directive prefix만 제거한 뒤 **완전 일치**할 때만 허용. substring/synonym/category 확장은 불가.
- identity-preservation negative는 identity-reference mode에서만 허용.
- pack-owned guard와 final audit의 vocabulary parity 및 hash 재검산.

이는 broad negative가 요청된 action, relationship, count, expression, wardrobe, genre를 삭제하는 문제를 이미 크게 줄인다.

### 4.2 현재 자동 negative와 legacy pool

동결 authored data와 generator source를 비교하면 다음과 같다.

- `negative_prompt_pools`의 고유 English terms: **86**.
- modern intent-neutral automatic set: **27**.
- modern guard에서 자동 허용되지 않는 legacy pool terms: **59**.
- 별도 identity-preservation set: **7**.
- legacy global `negative_prompt`: 18개 중 modern automatic 허용 12개, 차단 6개.
  - 차단되는 6개: `awkward expression`, `cropped-off head`, `duplicate faces`, `heavy JPEG artifacts`, `unnatural pose`, `unwanted text`.

이 분리는 적절하다. 다만 27개의 string-only set에도 `low resolution`, `cartoon style`, `illustration look`, `digital illustration`, `flat collage look`이 있다. 2134, 1834, 1857 같은 요청에서는 이들이 target effect일 수 있다. 현재 `authorial_negative_term_allowed`는 집합 membership, exact requester exclusion, identity mode를 보지만, 각 용어에 `affected_dimensions`나 요청 효과와의 충돌 메타데이터는 없다.

### 4.3 blanket detector의 scope 간극

현재 함수에 직접 입력했을 때 다음 세 문장은 모두 `[]`로 탐지되지 않았다.

- `Keep the frame free from a second person or hand, ... text, logos, watermark, illustration or CGI.`
- `Free of text, logos, and watermark.`
- `The blank tablet screen contains no interface or icons.`

앞의 두 문장은 global deletion directive일 수 있지만, 세 번째는 한 surface의 관찰 가능한 positive state다. 단순히 `free from`이나 모든 `no`를 새 regex로 막으면 세 번째까지 오탐한다. 필요한 것은 **negative clause의 출처·범위·대상 surface 분류**다.

### 4.4 visual obligations와 false substitutes

동결 `photo_prompt_visual_obligations.json`은 이미 좋은 소유 패턴을 가진다.

- profiles: **323**.
- `reject_substitutes`가 있는 profiles: 323, 총 substitute IDs **1,682**.
- `render_gates`가 있는 profiles: 323, 총 gates **1,549**.

특히 다음 exact profile은 그대로 재사용해야 한다.

- `medium_native_glitch`: malformed anatomy, fused object, broken text 하나를 glitch 의미로 인정하지 않음.
- `diegetic_reality_invariant_failure`: isolated synthesis defect를 세계 규칙 위반으로 인정하지 않음.
- `uncanny_coherence_mismatch`: random deformation, monster anatomy, horror makeup을 미묘한 coherence mismatch로 인정하지 않음.
- `mirror_selfie_reflection_device_topology`: direct selfie, empty mirror, detached phone이 mirror-selfie를 대체하지 못함.
- `hands_free_supported_drink_load`: 숨은 손/선반/입·빨대 지지가 hands-free balance를 대체하지 못함.

false substitute는 이처럼 **요청되거나 선택된 좁은 의미의 내부 경계**다. 1,682개를 전역 negative prompt로 합치면 의미를 파괴한다.

### 4.5 quality layer와 render repair

- quality의 `photographic_integration.baseline`은 shared light, contact shadow, weight, reflection, occlusion, material continuity를 통해 pasted/floating effect를 방지한다.
- `applicability_guards`는 glitch, cosplay, beastkin 등 theme-bound modifier가 primary context 없이 새 의미를 만들지 못하게 한다.
- `photo-render-repair/v1`은 lineage-bound event-critical object에 대해 required/transitional contact일 때만 native anatomy/contact gate를 추가한다. removal, relocation, concealment, transfer는 repair가 아니다.

남은 간극은 모든 장면에 같은 결함 목록을 붙이지 않고, **선택된 positive invariant와 예상 가시성으로부터 필요한 gate만 투영하는 공통 IR**이다.

## 5. 제안 의미 모델

### 5.1 observable components와 confusion negatives

| 실패 예방 의미 | observable components | confusion negatives |
|---|---|---|
| required subject presence | 요청된 주체 수, 각 주체의 구분 가능한 영역, 필수 역할/위치 | 깨끗한 빈 장면, 소품만 있음, 배경 인물이 주체를 대체 |
| human topology | 보이는 limb continuity, 관절 위치, 자연스러운 occlusion, 설명 가능한 digit count | fisheye foreshortening, crop, hair overlap, motion blur만으로 failure 판정 |
| hand-object interaction | affordance에 맞는 grip/contact patch, finger wrap, pressure/occlusion/contact shadow | hovering hand, fused hand-object, 물체 제거·이전, 근처에 있기만 함 |
| support and weight | base contact, 압축/그림자, 중심이 지지면 안쪽, 접지된 자세 | cropped support, 투명 지지대, 그림자만, 부유하는 소품 |
| object topology | 주요 part count, joins, continuous edges, stable symmetry/asymmetry, material interface | 의도적 비대칭 디자인, 화면 가장자리 crop, reflection 속 반복 |
| reflection/shadow ownership | source object와 대응하는 위치·형태·light direction·surface | specular highlight, intentional mismatch profile, 단순 darkness |
| text surface intent | surface, required/blank/abstract/nonlegible mode, 필요한 글자 수와 크기 | 모든 배경 문양을 text로 판정, required title을 watermark로 판정 |
| skin/material coherence | source-relative pores/weave/roughness, edge, highlight roll-off, 같은 물질 내 연속성 | 요청된 polished surface, low-res smoothing, specular wetness 자체 |
| requested capture artifact | source medium, 한 artifact family, 공간 범위, 강도, 보존할 내용 | random AI defect, unrelated filter stack, anatomy merge 하나 |
| projection/motion allowance | 같은 장면의 선·관절·깊이에 일관적인 투영 또는 궤적 | 국소적으로 끊긴 관절, 이유 없는 추가 limb, arbitrary smear |
| duplication/count | locked entity count, reflection/panel/sequence의 legitimate repeats | 거울 반사나 four-cut panel을 duplicate subject로 오판 |
| false substitute | active semantic profile의 모든 필수 component가 동시 존재 | 스타일·색·소품·한 표정·한 defect만으로 복합 의미 통과 |

### 5.2 source-relative 원칙

- anatomy는 이상적인 몸을 정의하지 않는다. 요청된 자세·시점 안에서 보이는 연결, 관절, 접촉, occlusion만 본다.
- object는 특정 상품 형태를 전역 기본값으로 만들지 않는다. 현재 요청의 part topology와 affordance를 기준으로 본다.
- texture는 무조건 더 거칠거나 더 많은 pores가 정답이 아니다. 요청된 material/capture fidelity와 비교한다.
- text는 `없음/있음` 이진값이 아니다. surface와 legibility 역할을 갖는다.
- artifact는 `나쁨` 이진값이 아니다. `forbidden defect`, `requested capture signature`, `semantic mechanism`을 분리한다.

## 6. 정확한 candidate/data 제안

### 6.1 새 topic-neutral IR: `photo-failure-prevention/v1`

이 계약은 optional aesthetic candidate가 아니라 composed planning/quality owner다.

```json
{
  "contract_version": "photo-failure-prevention/v1",
  "source_authorial_core_sha256": "<hash>",
  "protected_invariants": [
    {
      "invariant_id": "<stable id>",
      "dimension": "subject|count|action|text|style|camera|material|other",
      "source_text": "<request-grounded text>",
      "positive_prompt_evidence": "<literal visible state>",
      "priority": "P0|P1",
      "omission_counterfactual": "<material drift if absent>"
    }
  ],
  "intentional_artifacts": [
    {
      "artifact_id": "<id>",
      "mode": "capture_signature|semantic_mechanism",
      "family": "<grain|motion_blur|fisheye|jpeg|glitch|other>",
      "scope": "<entity/surface/region>",
      "strength": "source_relative_low|medium|high",
      "must_preserve": ["<content or topology>"],
      "conflicts_with_negative_term_ids": []
    }
  ],
  "controls": [
    {
      "control_id": "<id>",
      "failure_class": "presence|count|anatomy|contact|support|object_topology|reflection_shadow|text_surface|material|capture_artifact",
      "target_ref": "<entity or surface id>",
      "expected_visibility": "thumbnail|native|both|not_required",
      "required_positive_state": "<observable relation>",
      "allowed_variations": [],
      "failure_signatures": [],
      "runtime_lane": "positive_prompt|negative_en|pixel_gate_only",
      "affected_dimensions": [],
      "review_gate_id": "<fp_* id>"
    }
  ],
  "requester_exclusions": [
    {
      "source_text": "<complete exact active-span exclusion>",
      "target_scope": "global_frame|entity|surface",
      "runtime_negative_phrase": "<exact normalized complete exclusion or null>"
    }
  ]
}
```

### 6.2 자동 negative metadata: `photo-negative-term-policy/v1`

현재 string set을 바로 없애기보다 각 term에 다음 메타데이터를 추가하는 최소 확장을 제안한다.

```json
{
  "id": "low_resolution",
  "phrase": "low resolution",
  "defect_class": "capture_quality",
  "affected_dimensions": ["style", "camera", "material"],
  "automatic": true,
  "skip_if_positive_evidence_matches": ["low-resolution", "early smartphone", "compression artifacts"],
  "incompatible_profile_ids": [],
  "review_scale": "both"
}
```

필수 규칙:

- `affected_dimensions` 중 하나가 locked이고 frozen positive evidence가 term의 반대가 아니면 자동 negative를 suppress한다.
- exact requester exclusion은 기존처럼 완전 일치만 허용한다.
- `cartoon style`, `illustration look`, `digital illustration`, `low resolution`, `flat collage look`은 intent-neutral이라는 이름만 믿지 않고 target-effect conflict를 검사한다.
- generic `unrealistic hands`는 손이 material하고 expected-visible일 때만 보조로 쓰며, 핵심은 positive topology/contact gate다.
- 이 metadata는 authored policy/source에 두고 generated index나 candidate rank로 소유하지 않는다.

### 6.3 text surface field

`text` locked dimension 또는 composed IR에 다음 필드를 제안한다.

```json
{
  "text_surface_mode": "required_legible|diegetic_uncontrolled|abstract_nonlegible|blank_surface|requester_forbidden|unspecified",
  "target_surfaces": [],
  "required_strings": [],
  "allowed_background_marks": "none|nonlegible_only|unrestricted",
  "thumbnail_role": "primary|support|absent"
}
```

1662의 package title, 2490의 세탁소 상품 상자, 2675의 indistinct papers, 2680의 blank tablet을 같은 `no text`로 처리하지 않는다.

### 6.4 quality family와 gate IDs

`photo_prompt_quality_layers.json`의 conditional quality family로 다음 ID를 제안한다.

- `failure_prevention_integrity`
- `fp_required_subject_presence`
- `fp_required_entity_count`
- `fp_major_topology_continuity`
- `fp_hand_object_contact_integrity`
- `fp_object_part_geometry`
- `fp_support_weight_contact`
- `fp_reflection_shadow_ownership`
- `fp_text_surface_intent`
- `fp_requested_artifact_compatibility`
- `fp_false_substitute_rejection`

이 gate들은 항상 모두 켜지지 않는다. `photo-failure-prevention/v1.controls`에서 expected-visible이고 P0/P1인 것만 투영한다.

### 6.5 exact profiles: 추가보다 재사용

새 `bad_anatomy` 또는 `AI_artifact` visual profile은 제안하지 않는다. 다음 기존 exact profile을 의미가 정확히 요청되었을 때만 사용한다.

- `medium_native_glitch`
- `diegetic_reality_invariant_failure`
- `uncanny_coherence_mismatch`
- `mirror_selfie_reflection_device_topology`
- `hands_free_supported_drink_load`

BM25F/embedding-only 발견은 계속 advisory다. exact requester term이나 post-core selected profile만 그 profile의 complete components, `reject_substitutes`, gates를 hard하게 만든다.

## 7. thumbnail/native render gates

### 7.1 공통 선행 게이트

1. P0 required subject와 required object가 실제로 존재하는가.
2. 요청된 entity count와 action/contact state가 읽히는가.
3. intentional artifact allowance가 negative term에 의해 삭제되지 않았는가.
4. target region이 보여야 하는데 사라졌으면 `missing_required_region=FAIL`; 애초에 보일 필요가 없으면 `not_applicable`.

### 7.2 thumbnail

- required subject count와 주요 silhouette가 첫 읽기에 분리되는가.
- event-critical object가 소품 더미나 배경으로 사라지지 않는가.
- 손-물체, 몸-지지대, 주체-반사의 주요 관계가 축소 상태에서 존재하는가.
- 명백한 duplicate body/face, 끊긴 major limb, floating object, 잘못된 panel count가 보이지 않는가.
- required title, blank screen, no-people 같은 text/count surface state가 thumbnail 역할에 맞는가.
- glitch/reality-error 같은 의미는 exact profile의 first-read gate를 만족하며 일반 합성 defect와 구분되는가.

### 7.3 native

- 보이는 손가락/관절/limb의 연결과 occlusion이 설명 가능하고, 접촉 지점에서 물체와 녹아붙지 않는가.
- grip, pinch, support, tool use가 affordance와 맞으며 contact shadow/pressure/occlusion 중 필요한 단서가 있는가.
- 제품의 주요 part joins, 대칭/비대칭, 표면 경계, 반사/그림자가 같은 물체를 소유하는가.
- skin/material texture가 요청된 capture 해상도와 재질 안에서 연속적인가. 저해상도 요청에 pore absence를 무조건 실패로 세지 않는다.
- text surface가 `required_legible`, `abstract_nonlegible`, `blank` 중 선택한 모드와 맞는가.
- intentional fisheye/motion/compression/glitch는 공간적으로 일관되고, 요청하지 않은 anatomy/object merge와 분리되는가.

P0/P1 hard gate 하나라도 실패하면 `partial_is_fail`이다. hidden/blocked/undelivered는 품질 0이 아니라 `UNSCORED`; 사용자 선호는 별도다.

## 8. 회귀와 held-out 설계

| # | positive | hard negative | 핵심 검증 |
|---:|---|---|---|
| 1 | resolved 두 주체가 있는 illustrated profile | 1857처럼 clean room/no-text지만 주체가 없음 | subject presence가 negative compliance보다 선행 |
| 2 | requested early-phone low-resolution + noise | 동일 prompt에 automatic `low resolution` negative 삽입 | target-effect conflict suppression |
| 3 | photoreal anime cosplay의 장착형 bunny headset | nekomimi exact profile의 anti-costume를 cosplay에 전역 적용 | profile-local substitute 경계 |
| 4 | package title이 primary인 miniature | blanket `unwanted text` | `required_legible` text surface 유지 |
| 5 | fisheye로 커진 가까운 손, joints/digits coherent | 같은 투영에서 fused/extra/disconnected digit | projection allowance와 anatomy 분리 |
| 6 | flower stem pinch/contact | hovering fingers 또는 stem-hand fusion | contact patch와 affordance |
| 7 | blank tablet + 모든 필수 물체 fully visible | blank screen은 맞지만 물체 crop/duplicate | 독립 gate의 partial fail |
| 8 | mirror/phone/hand/gaze가 한 반사면에 결합 | direct selfie, detached phone, empty mirror | 기존 exact profile 재사용 |
| 9 | 한 medium-native glitch family가 반복 | malformed hand 하나를 glitch로 사용 | `medium_native_glitch` false substitute |
| 10 | 세 surface에 같은 world invariant failure | isolated object fusion/random shadow | `diegetic_reality_invariant_failure` 경계 |
| 11 | identity mode가 명시된 reference run | ordinary original-subject run에 identity negatives 자동 삽입 | identity lane gating |
| 12 | exact requester no-people/blank surface | candidate frequency만으로 extra-people/text를 hard 금지 | exact와 advisory 분리 |
| 13 | swing grip와 free hand가 둘 다 보임 | 물체 제거 또는 두 손 모두 free/숨김 | positive interaction 보존 |
| 14 | no-negative control 1586/2078 | blanket negative를 추가한 동일 장면 | global quality 개선 여부를 인과적으로 시험 |

### held-out 구성

- 본 보고서의 21개 posts는 첫 qualification scoring set에서 제외한다.
- portrait, product, text-forward graphic, intentional low-fidelity, special projection, mirror/reflection, non-person scene를 모두 포함한다.
- early/middle/late 작성 양식을 층화한다.
- 한 쌍 안에서는 subject/scene/camera/lighting/seed 가능한 입력을 고정하고 한 failure-prevention 축만 바꾼다.
- exact requester exclusion, automatic defect term, profile-local false substitute, pixel-only gate를 별도 arms로 둔다.
- prompt audit, delivered pixels, user judgment을 합산하지 않는다.

## 9. 한계와 결정

- 정규식은 부정문 범위, 병렬 목록, `[XXX]` 같은 placeholder, 한국어/영어 혼합, 의도적 스타일 용어를 완전히 분류하지 않는다.
- 42장 표본은 failure mechanism을 찾기 위한 목적 표본이며 4,908장 전체의 결함률이나 negative 효율을 추정하지 않는다.
- 1857의 심한 prompt/pixel 불일치는 generator failure, source pairing, placeholder 처리 중 어느 단계가 원인인지 이 자료만으로 판정하지 못한다.
- identity 동일성, 보호 특성, 실제 관계, 건강, 매력, 성격, 직업, 민족/국적 등은 픽셀에서 추론하지 않았다.
- 현재 함수 probe는 detector surface를 확인했을 뿐 전체 후보팩/compose/runtime suite를 실행한 것이 아니다.
- 구현하지 않았으므로 schema migration, backward compatibility, audit parity, index rebuild, prompt behavior는 미검증이다.
- 새 이미지 생성이 없으므로 제안 gate의 독립 render qualification과 사용자 판단은 `UNSCORED`다.

**결정은 `proposed`이다.** 기존 negative-intent firewall과 exact-profile false substitutes를 보존하면서, `photo-failure-prevention/v1`, term-level conflict metadata, conditional `fp_*` gates를 추가하는 방향이 가장 작은 재사용 가능한 보완이다.

## 부록 A — 픽셀 증거 경로

기준 디렉터리: `generated/reactorprompt-export-20260902-incremental/`

- 1586: `images/1586_DY1yjxkmkT__01.jpg`, `images/1586_DY1yjxkmkT__02.jpg`
- 1587: `images/1587_DY10cywGvWk_01.jpg`, `images/1587_DY10cywGvWk_02.jpg`
- 1662: `images/1662_DY9l8a3mvkn_01.jpg`, `images/1662_DY9l8a3mvkn_02.jpg`
- 1834: `images/1834_DZhVtv9mk5V_01.jpg`, `images/1834_DZhVtv9mk5V_02.jpg`
- 1857: `images/1857_DZnAmOrmuVf_01.jpg`, `images/1857_DZnAmOrmuVf_02.jpg`
- 1939: `images/1939_DZ4LHOXGgno_01.jpg`, `images/1939_DZ4LHOXGgno_02.jpg`
- 2076: `images/2076_DaZc8egGuUe_01.jpg`, `images/2076_DaZc8egGuUe_02.jpg`
- 2078: `images/2078_DaX-NK0GjDW_01.jpg`, `images/2078_DaX-NK0GjDW_02.jpg`
- 2134: `images/2134_DaojItYmfuP_01.jpg`, `images/2134_DaojItYmfuP_02.jpg`
- 2158: `images/2158_DauI7KYms5l_01.jpg`, `images/2158_DauI7KYms5l_02.jpg`
- 2246: `images/2246_DbDB5jUmvw3_01.jpg`, `images/2246_DbDB5jUmvw3_02.jpg`
- 2299: `images/2299_DbcuYZ-GmbV_01.jpg`, `images/2299_DbcuYZ-GmbV_02.jpg`
- 2317: `images/2317_DbiauDdmnlb_01.jpg`, `images/2317_DbiauDdmnlb_02.jpg`
- 2490: `images/2490_DcDNGdXGjJU_01.jpg`, `images/2490_DcDNGdXGjJU_02.jpg`
- 2623: `images/2623_DcgX-SbmrQD_01.jpg`, `images/2623_DcgX-SbmrQD_02.jpg`
- 2641: `images/2641_DcfQR7cmhdc_01.jpg`, `images/2641_DcfQR7cmhdc_02.jpg`
- 2666: `images/2666_DclmMmHmvGC_01.jpg`, `images/2666_DclmMmHmvGC_02.jpg`
- 2675: `images/2675_DclmlxMmpqo_01.jpg`, `images/2675_DclmlxMmpqo_02.jpg`
- 2680: `images/2680_Dcn2LesmjBy_01.jpg`, `images/2680_Dcn2LesmjBy_02.jpg`
- 2711: `images/2711_DcqCkahGovW_01.jpg`, `images/2711_DcqCkahGovW_02.jpg`
- 2742: `images/2742_Dcx0CYwmkWj_01.jpg`, `images/2742_Dcx0CYwmkWj_02.jpg`

## 부록 B — 재현 명령과 코드 표면

```bash
# 동결 입력
shasum -a 256 generated/reactorprompt-export-20260902-incremental/manifest.json
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json | shasum -a 256
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json | shasum -a 256
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json | shasum -a 256

# 모수
jq '[.[] | select((.prompt // "") != "")] | length' generated/reactorprompt-export-20260902-incremental/manifest.json
jq -c '.[] | select((.prompt // "") != "") | .prompt' generated/reactorprompt-export-20260902-incremental/manifest.json | sort -u | wc -l

# authored negative pools와 exact profiles
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json \
  | jq '{negative_prompt, negative_prompt_pools}'
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json \
  | jq '.profiles[] | select(.id == "medium_native_glitch" or .id == "diegetic_reality_invariant_failure" or .id == "uncanny_coherence_mismatch" or .id == "mirror_selfie_reflection_device_topology" or .id == "hands_free_supported_drink_load")'

# detector scope probe
PYTHONPATH=skills/photo-prompt-image-generator/scripts .venv/bin/python -c \
  'import prompt_generator as p; print(p.find_blanket_negative_directives("Keep the frame free from a second person, text, logos, and CGI."))'
```

전수 계수는 위 manifest 배열의 924개 비어 있지 않은 prompt에 섹션 1.2의 고정 정규식군을 적용해 post ID와 exact prompt body를 별도 집계했다. 픽셀 표본은 각 선택 ID의 첫 두 `download_ok=true` 경로로 고정했다.

## 부록 C — 외부 출처

외부 출처는 사용하지 않았다. 이번 주제의 결론은 동결 코퍼스, 실제 전달 픽셀, 대상 스킬의 authored source/guard behavior만으로 제한했다.

# Topic 03 — 카메라 시점·렌즈/원근·거리·심도·초점면

## 상태와 결론

- **결정: `proposed`**
- 모드: 연구/설계 전용. 런타임 자산, 생성 인덱스, 테스트, 스킬 문서는 수정하지 않았다.
- 대상: ReactorPrompt 증분 코퍼스의 비어 있지 않은 프롬프트 **924개 전수**와, 의도적으로 층화한 **17개 게시물의 실제 이미지 34장**.
- 핵심 제안: 현재처럼 `lens`나 `focus` 한 슬롯에 수치 렌즈, 투영, 심도, 초점 대상, 초점 기법을 섞지 말고, 다음의 인과 사슬을 독립 축으로 보존한다.

  `시점(vantage) → 카메라-피사체 기하(distance) → 투영/화각(projection/FoV) → 초점 해법(focus method) → 보이는 선명도 분포(visible sharpness distribution)`

- 코퍼스에서는 85mm, f-number, shallow depth of field 같은 수치/표현이 흔하지만, **빈도가 전역 기본값이나 하드 의무를 정당화하지 않는다**. 정확한 요청어·출처 문구는 계약으로 보존할 수 있으나, BM25F/임베딩 발견은 후보로만 남겨야 한다.
- 단일 생성 이미지에서 정확한 초점거리나 조리개 값을 역추론할 수 없다. 수치는 프롬프트/요청 계약 게이트이고, 원근, 곡률, 초점면, 층별 선명도는 픽셀 게이트이다.
- 이번 34장은 이미 전달된 코퍼스의 출처 픽셀 관찰이다. 새 후보팩의 독립 생성 검증도, 사용자 판단도 아니다. 따라서 새 설계의 렌더 적합성과 사용자 수용은 모두 **`UNSCORED`**이다.

## 1. 범위와 표본 방법

### 1.1 동결 입력

- manifest: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, ID 1565–2746.
- 기준 스킬 revision: `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 기존 authored source는 협업 중 작업 트리 변경과 섞이지 않도록 모두 해시가 고정된 snapshot commit `401f450e4c0ec32ef79c502e3c6a6666c9a106c4`의 `git show <commit>:<path>`로 읽었다.
  - `photo_prompt_tags.json`: `5ae9ae8311f418875a011d7fd887804c9b974f26941689679af55a1499406b00`
  - `photo_prompt_visual_obligations.json`: `64e73c97f12da099b18cb7be4e0086f0c51c66d63380c297ec7632709b4805bc`
  - `photo_prompt_quality_layers.json`: `99597926d0f136bfabaf5f8be28597aae82f15bdbe8e3bfcfbbb774b3ac0541f`

### 1.2 프롬프트 전수 스캔

924개 본문을 소문자화한 뒤, 각 축의 명시적 용어군을 정규식으로 세었다. 게시물 수와 고유 본문 수를 함께 기록했다. 이 방법은 문맥을 완전히 이해하는 분류기가 아니므로, 다음 두 값을 일부러 나눴다.

- `numeric_mm`: `35mm film`처럼 필름 포맷일 수도 있는 원시 숫자-mm 일치.
- `explicit_focal_context`: 숫자-mm가 `lens`, `equivalent`, `perspective`, `focal` 같은 광학 문맥과 함께 나온 더 엄격한 일치.

따라서 수치는 **프롬프트 쪽 어휘 사용량**이며, 그 효과가 4,908장 전체 픽셀에 실현되었다는 통계가 아니다.

### 1.3 픽셀 표본

- 세 ID 구간을 사용했다: early 1565–1958, middle 1959–2352, late 2353–2746.
- 희소하거나 구분력이 큰 시점/투영/초점 표현을 우선한 양성 13개 게시물과, 강한 광학 명시가 없거나 일부 축만 명시된 대조 4개 게시물을 골랐다.
- 각 게시물에서 manifest 순서상 다운로드에 성공한 첫 두 이미지를 고정하여 총 34장을 보았다.
- 접촉 시트에서 34장을 모두 비교하고, 핵심 사례는 원본 파일로 확대 확인했다.
- 이 표본은 메커니즘과 혼동 경계를 찾기 위한 목적 표본이다. 표본에서 관찰한 정렬 비율을 4,908장 전체 비율로 일반화하지 않는다.

## 2. 프롬프트 쪽 발견

### 2.1 축별 출현량

| 휴리스틱 축 | 게시물 | 고유 본문 | 해석 주의점 |
|---|---:|---:|---|
| topic union | 645 | 630 | 아래 카메라/초점 축 중 하나 이상 |
| viewpoint | 287 | 278 | eye/high/low/overhead/Dutch/ground-level 등 |
| raw numeric `mm` | 293 | 285 | 필름 포맷 등 비초점거리 문맥 포함 가능 |
| explicit focal context | 150 | 147 | lens/equivalent/perspective/focal 문맥으로 제한 |
| named lens class | 95 | 95 | wide, fisheye, tele, macro, tilt-shift 등 |
| explicit camera-subject distance | 34 | 33 | arm’s length, close working distance 등 |
| depth-of-field family | 262 | 258 | shallow/moderate/deep/bokeh/falloff 포함 |
| shallow DOF | 204 | 200 | `shallow focus` 포함 |
| moderate DOF | 20 | 20 | shallow-to-moderate 등 |
| deep DOF | 4 | 4 | near/mid/far 또는 everything-in-focus 지향 |
| explicit aperture | 87 | 84 | f/1.4, f/8 등 |
| explicit focus target/plane | 130 | 127 | eyes/face/foreground/background/plane 등 |
| background blur/bokeh | 134 | 134 | 원인보다 결과 표현인 경우가 많음 |
| explicit perspective effect | 40 | 40 | compression, exaggeration, distortion 등 |
| framing/working distance | 252 | 246 | close-up/medium/wide와 실제 거리 표현 혼재 |
| focus stack | 2 | 2 | 단일 촬영 심도와 별개인 합성 기법 |
| tilt-shift | 1 | 1 | 투영/초점면 기법을 함께 암시 |
| full-frame equivalent | 69 | 69 | 센서 기준을 일부 명시 |

세부적으로 eye-level은 150개 게시물, low-angle 72개, high-angle 32개, overhead/top-down 55개, Dutch/canted 10개였다. 숫자-mm 출현은 85mm 85회, 50mm 71회, 35mm 53회가 상위였지만, 이는 의미 적합성이나 결과 성공률이 아니다.

### 2.2 ID 구간별 분포

| 구간 | 비어 있지 않은 프롬프트 | viewpoint | raw numeric mm | distance | DoF | focus target | perspective effect |
|---|---:|---:|---:|---:|---:|---:|---:|
| early 1565–1958 | 382 | 35 | 23 | 3 | 103 | 35 | 4 |
| middle 1959–2352 | 285 | 95 | 94 | 10 | 74 | 36 | 9 |
| late 2353–2746 | 257 | 157 | 176 | 21 | 85 | 59 | 27 |

후반부에 수치와 시점 용어가 많아졌지만, 구간별 작성 양식과 중복 구성이 다르므로 이를 곧바로 취향 변화나 품질 향상으로 해석하지 않는다. 이 결과는 **코퍼스가 나중으로 갈수록 광학 문장을 더 명시적으로 작성했다**는 텍스트 관찰까지만 지지한다.

### 2.3 결합과 누락

| 결합/누락 | 게시물 |
|---|---:|
| numeric mm + explicit distance | 23 |
| numeric mm + DoF | 127 |
| numeric mm + aperture | 85 |
| DoF + focus target | 64 |
| shallow DoF + 복수 선명 대상 | 17 |
| numeric mm + full-frame-equivalent | 69 |
| numeric mm, distance 없음 | 270 |
| numeric mm, equivalence basis 없음 | 224 |
| DoF, explicit focus target 없음 | 198 |

가장 중요한 간극은 `렌즈 숫자 → 효과`를 잇는 기하가 자주 생략된다는 점이다. 예를 들어 85mm와 f/1.4를 적어도 카메라 거리, 피사체-배경 간격, 초점 대상이 없으면 압축감과 초점 분포는 결정되지 않는다. 반대로 렌즈 숫자가 없어도 높은 시점, 팔 길이 셀피, 배경의 점진적 연화처럼 원하는 결과를 충분히 지정할 수 있다.

## 3. 픽셀 쪽 관찰

| 구간 / ID | 프롬프트에 저자가 쓴 광학 주장 | 두 이미지에서 보인 효과 | 판정 |
|---|---|---|---|
| early / 1586 (control) | 넓고 고요한 겨울 구도, 강한 광학 수치 없음 | 인물은 선명하고 먼 도시/조명은 부드러움 | 비명시 광학 효과. 저자 문구가 없어도 결과에 초점 분포가 생김 |
| early / 1587 | fisheye portrait, wide-angle distortion | 원형 경계, 휜 실내선, 높은 시점, 크기 과장이 함께 보임 | 강한 정렬 |
| early / 1662 | high diagonal + tilt-shift miniature, 중앙만 선명, 상하 heavy blur | 중앙 선명 밴드와 상·하부 흐림, 축소 모형의 스케일 단서 | 정렬. 단, 모형 소품/문자/스케일 자체가 강한 혼동 변수 |
| early / 1902 | low/wide fashion, subtle fisheye-like distortion, shallow DoF | 낮고 넓은 패션 시점은 읽히지만 fisheye 곡률은 약함 | 부분 정렬. `fisheye-like`가 낮은 시점/크롭으로 대체됨 |
| early / 1953 | 위에서 아래로 든 스마트폰, gentle wide distortion | 높은 근접 셀피, 가까운 팔/얼굴의 크기 이득, 방은 부드럽게 읽힘 | 질적 정렬. 수치 광학값은 검증 불가 |
| early / 1956 (control) | 자연스러운 수영장 스트레칭, 광학 계약 없음 | 인물 평면은 선명, 배경은 읽히거나 약하게 연화 | 비명시 광학 효과 |
| middle / 2076 | 35mm, f/11, deep DoF, no bokeh; 실내/반사/산 모두 선명 | 인물, 곤돌라 내부·반사, 산이 모두 읽힘 | 의미 정렬. 35mm/f/11 자체는 픽셀에서 검증 불가 |
| middle / 2077 (control) | 밝은 셀피/거울형 medium shot, 광학 계약 없음 | 평평하고 넓은 선명도, 깊이 층은 약함 | 비명시 광학 효과 |
| middle / 2158 | arm’s length, 24–28mm phone wide, 환경이 보일 만큼 deep enough | 넓은 팔 길이 셀피 기하, 얼굴 선명, 스카이라인은 식별 가능하나 부드러움 | 강한 정렬. `환경 식별 가능`은 universal deep focus와 다름 |
| middle / 2245 | 85mm f/1.4, extremely shallow; 눈·손끝·물방울 모두 선명 | 눈, 안경, 가까운 손가락/물방울이 선명하고 배경은 검음 | 불충분. 대상들이 거의 같은 평면이고 배경 층이 없어 극얕은 심도를 입증하지 못함 |
| middle / 2299 | eye-level 40–50mm, shallow-to-moderate; 얼굴 선명, 앞/뒤 식물 연화 | 흐린 전경 잎 → 선명 인물 → 읽히지만 부드러운 온실의 세 층 | 강한 정렬 |
| late / 2470 | 85mm f/1.8, compressed perspective, shallow DoF | 근접 인물과 흐린 가까운 기둥/배경 | 효과는 정렬. 카메라 위치 비교가 없어 85mm/압축 원인은 독립 검증 불가 |
| late / 2641 | 15mm fisheye, 가까운 손 확대, 깊은 골목 | 매우 큰 가까운 손, 휘고 넓은 골목, 강한 깊이 확장 | 강한 정렬 |
| late / 2666 (qualitative control) | 약간 높은 selfie perspective만 명시; mm/aperture/DoF/focus target 없음 | 높은 근접 셀피와 넓게 보이는 사무실 | 시점 효과는 보이지만 광학 수치가 없어도 성립 |
| late / 2680 | 정확한 90° top-down, 50mm eq, f/8, broad DoF, 전체 선명 | 탑다운과 넓은 선명도는 분명함 | 시점 정렬. 물체가 거의 한 평면이라 깊은 DoF를 가혹하게 시험하지 않음 |
| late / 2711 | 100mm macro, very close, very shallow; 꽃·손끝·입술이 전면 초점면, 눈/머리/벽은 후퇴 | 꽃·손가락·입술뿐 아니라 눈도 꽤 읽히고, 배경/머리 가장자리만 부드러움 | 약한 발산. 지정한 좁은 단일 초점면보다 합성적 광범위 선명도로 보임 |
| late / 2742 | 85mm, close non-distorting, shallow DoF, 눈·입술·주근깨·물방울 선명 | 얼굴/눈/젖은 머리 선명, 배경 bokeh, 두드러진 왜곡 없음 | 효과 정렬. 정확한 85mm/거리 수치는 검증 불가 |

### 3.1 정렬 패턴

1. **관계로 쓴 문구가 숫자보다 검증 가능했다.** `가까운 손이 커짐`, `전경 잎 → 인물 → 온실`, `실내/반사/산이 모두 읽힘`은 픽셀에서 직접 확인할 수 있었다.
2. **특수 투영은 두 개 이상의 동반 효과가 있을 때 강했다.** fisheye는 원형 경계만이 아니라 곡선, 근접 크기 과장, 깊이 확장이 함께 보여야 했다.
3. **deep enough와 deep focus를 구분해야 했다.** 2158은 환경 인식에 충분하지만 모든 거리가 동일 미세 선명도일 필요가 없다.
4. **대조군도 결과 광학을 가진다.** 명시적 렌즈/심도 문구가 없어도 생성기는 자체적으로 배경 연화나 평평한 선명도를 선택했다. 따라서 비명시는 `효과 없음`이 아니라 `하드 의무 없음`이다.

### 3.2 발산과 과잉 주장 위험

- 1902의 낮은 시점·넓은 크롭을 fisheye 성공으로 세면 false positive가 된다.
- 2245처럼 거의 같은 평면에 있는 여러 선명 대상을 `f/1.4 극얕은 심도` 성공으로 세면 심도 시험이 되지 않는다.
- 2680처럼 거의 완전한 평면 배열의 전체 선명도는 탑다운에는 강한 증거지만 near/mid/far deep-focus에는 약한 증거다.
- 2711은 단일 전면 초점면을 말하지만 눈까지 넓게 읽혀, 문장과 선명도 분포 사이의 긴장이 있다. `매크로 크롭`이나 `배경 blur`만으로 초점면 계약을 통과시키면 안 된다.
- 단일 이미지에서 35mm와 50mm, 85mm와 먼 거리의 조합을 역산할 수 없다. 동일한 프레이밍은 카메라 위치와 크롭을 바꿔 비슷하게 만들 수 있다.

## 4. 외부 메커니즘 근거

- [Nikon — Understanding Focal Length](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)는 초점거리가 화각과 배율을 바꾼다고 설명한다. 이 보고서는 이를 `field_of_view`와 `projection effect`를 분리해야 하는 근거로 사용한다.
- [Sony — Factors of Defocus](https://www.sony.com/electronics/support/articles/00267923)는 배경 흐림이 조리개, 초점거리, 카메라-피사체 거리, 피사체-배경 거리의 결합이라는 점을 구분한다. 따라서 `85mm = shallow DoF` 같은 단일 슬롯 문구는 물리적 원인을 과도하게 합친다.
- [ZEISS — Depth of Field and Bokeh](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-depth-of-field-and-bokeh.pdf)는 동일 재현 배율에서 심도가 단순히 초점거리 하나로 결정되지 않고, 포맷/허용 흐림원 등도 관련되며 선명도는 경계에서 이진적으로 끊기지 않고 점진적으로 변한다는 기술적 배경을 제공한다.
- [Nikon — Special-Purpose Lenses](https://www.nikonusa.com/c/lenses/dslr-lenses/special-purpose)는 perspective-control/tilt 렌즈가 카메라 위치만 바꾸지 않고 초점면을 조절할 수 있음을 보여 준다. `tilted_plane`은 일반 shallow DoF와 다른 focus method여야 한다.
- [Sony — Focus Stacking vs. Focus Bracketing](https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7m4k/articles/00342633)은 서로 다른 초점 위치의 여러 캡처를 합쳐 확장 심도를 만드는 focus stacking을 설명한다. 단일 프레임 deep focus와 동일 후보로 취급하면 안 된다.

이 자료들은 안정적인 사진 메커니즘 정의에만 사용했다. 특정 ReactorPrompt 이미지가 실제로 어떤 카메라/렌즈로 촬영 또는 생성되었는지 인증하는 자료로 사용하지 않았다.

## 5. 기존 데이터 겹침과 올바른 소유권

### 5.1 현재 authored candidate source

동결 `photo_prompt_tags.json`에서 관련 슬롯은 다음과 같았다.

| 현재 슬롯 | 엔트리 수 | 겹침/문제 |
|---|---:|---|
| `camera_direction` | 44 | eye/high/low/top-down뿐 아니라 일부 방향·시점 의미가 넓게 혼재 |
| `camera_height` | 7 | 별도 슬롯이지만 `camera_direction`과 소유권 경계가 겹침 |
| `camera_type` | 25 | 장비/매체와 시점·캡처 문맥이 섞일 가능성 |
| `lens` | 33 | 렌즈 종류, 수치, 투영, 심도 효과를 함께 담음 |
| `focus` | 20 | 초점 대상, 심도, 초점면, diffusion, focusing behavior, stacking, 특수 렌즈를 혼합 |
| `shot_scale` | 8 | 프레이밍 크기 소유자로 유지할 가치가 있음 |

구체적 문제:

- `lens.85mm`의 현 문구가 `an 85mm portrait lens with shallow depth of field`로 렌즈와 심도를 결박한다.
- `focus` 안에는 `eye_focus`, 얼굴 autofocus 같은 대상, `shallow_depth`/`deep_focus` 같은 범위, foreground/background plane, `soft_focus` 같은 diffusion, `macro focus stack`, `zone`, `missed`, `infinity`, Lensbaby edge blur까지 같이 있다.
- `distance_narrative`는 사람 사이 거리/서사 간격이며 카메라-피사체 거리의 소유자가 아니다.
- 현재 quality coherence에는 top-down 대 low-angle, close-up 대 full-body 충돌은 있으나, **초점거리 ↔ 거리 ↔ 투영 ↔ DoF ↔ 초점면**의 일관성 규칙은 없다.

### 5.2 현재 quality source

`photo_prompt_quality_layers.json`의 동결본에는 재사용할 수 있는 기반이 있다.

- `close_camera_depth`: 근접 카메라에 focus falloff, foreground occlusion, lens perspective 또는 grain을 요구한다. 다만 **grain만으로는 근접 기하를 증명하지 못하므로** optics 게이트에서는 제외해야 한다.
- `frame_hierarchy` / `layered_depth_order`: 전경 방해, 피사체 평면, 배경 falloff의 순서를 다룬다.
- `close_focus_priority`: 초점 우선순위와 가장자리 거동을 다룬다.
- `shot_intent`: 거리/각도/타이밍의 이유를 요구한다.

이들은 구성과 품질의 보조 게이트로 유지하되, 광학 의미의 단일 소유자는 새 `photo-camera-optics/v1` IR로 두는 편이 낫다. 신체·의복·환경의 시각 의무 프로필이 렌즈 의미를 소유하게 해서는 안 된다.

## 6. 제안하는 source-relative 의미 축

절대 수치보다 출처 장면 안의 관계를 먼저 보존한다.

1. **시점 높이**: `subject_eye_level` 또는 장면의 기준 평면에 대한 `below / level / above / overhead`, 그리고 pitch를 별도 기록한다.
2. **roll**: 수평선/건축 수직에 대한 기울기. 몸의 기울기나 대각선 크롭과 분리한다.
3. **azimuth / body-side relation**: 정면, 3/4, 측면, 후면 같은 카메라-피사체 방위. 피사체 포즈가 아니라 관찰 위치다.
4. **카메라-피사체 거리**: `macro_working / arm_length / close / conversational / environmental / distant`. shot scale과 독립이다.
5. **피사체-배경 간격**: `touching / near / separated / far`, 또는 source-relative 순서. 배경 blur의 핵심 원인 중 하나다.
6. **화각**: 요청된 프레이밍과 장면 폭을 기준으로 `narrow / normal / wide / extreme_wide`. 수치 초점거리와 별개다.
7. **투영 효과**: `foreground_size_gain`, `depth_expansion`, `depth_compression`, `edge_curvature`, `vertical_convergence`처럼 보이는 결과를 기록한다.
8. **초점 대상**: 객체/부위와 그 상대 평면(`foreground / subject / background`)을 함께 기록한다.
9. **심도 범위**: `very_shallow / shallow / moderate / broad / deep_enough_for_context / near_to_far`, 그리고 층별 선명 상태를 함께 기록한다.
10. **초점 해법**: `single_plane / zone / infinity / focus_stack / tilted_plane / split_diopter / deliberate_miss`를 별도 축으로 둔다.
11. **falloff**: 어느 방향으로 얼마나 점진적으로 선명도가 줄어드는지 기록한다. 임의의 가우시안 영역 blur와 구분한다.
12. **수치 캡처 힌트**: `equivalent_focal_length_mm`, `aperture_f_number`, sensor/equivalence basis는 출처나 요청에 있을 때만 보존한다. 픽셀 관찰에서 새로 발명하지 않는다.

## 7. 제안 IR과 후보팩 필드

### 7.1 단일 소유 IR

조합 단계의 canonical owner로 아래 구조를 제안한다. 예시는 필드 계약이며 구현은 하지 않았다.

```json
{
  "schema": "photo-camera-optics/v1",
  "source": {
    "kind": "request_exact|reference_observation|candidate_advisory|authorial_choice",
    "literal_evidence": [],
    "confidence": "high|medium|low",
    "priority": "P0|P1|P2"
  },
  "vantage": {
    "height_relative_to_subject": "below|eye_level|above|overhead|unspecified",
    "pitch": "up|level|down|near_90_down|unspecified",
    "roll_degrees": null,
    "azimuth": "front|three_quarter|side|rear_three_quarter|rear|unspecified"
  },
  "distance": {
    "camera_subject": "macro_working|arm_length|close|conversational|environmental|distant|unspecified",
    "subject_background": "touching|near|separated|far|unspecified"
  },
  "field_of_view": {
    "relative_class": "extreme_wide|wide|normal|narrow|unspecified",
    "equivalent_focal_length_mm": null,
    "equivalence_basis": "full_frame|named_sensor|unknown|null"
  },
  "projection": {
    "family": "rectilinear|fisheye|telephoto_compressed|tilted_plane|split_diopter|unspecified",
    "visible_effects": [],
    "distortion_budget": "none|restrained|visible|extreme|unspecified"
  },
  "focus": {
    "method": "single_plane|zone|infinity|focus_stack|tilted_plane|split_diopter|deliberate_miss|unspecified",
    "primary_targets": [],
    "secondary_targets": [],
    "dof_extent": "very_shallow|shallow|moderate|broad|deep_enough_for_context|near_to_far|unspecified",
    "plane_states": {
      "foreground": "sharp|readable|soft|blurred|occluded|absent|unspecified",
      "subject": "sharp|readable|soft|blurred|absent|unspecified",
      "background": "sharp|readable|soft|blurred|absent|unspecified"
    },
    "falloff_direction": "front_to_back|back_to_front|center_band|dual_plane|none|unspecified",
    "falloff_strength": "gentle|moderate|strong|unspecified"
  },
  "capture_hint": {
    "aperture_f_number": null,
    "only_if_source_or_request_explicit": true
  },
  "compatibility": {
    "required_effects": [],
    "forbidden_substitutes": [],
    "conflicts": []
  },
  "omission_counterfactual": ""
}
```

### 7.2 authored candidate slot 재구성

`photo_prompt_tags.json`에는 아래의 좁은 후보 그룹을 제안한다.

- `camera_vantage`: 높이, pitch, roll, azimuth만 소유.
- `camera_subject_distance`: 카메라-피사체 작업 거리만 소유.
- `field_of_view`: source-relative 화각과 요청된 equivalence만 소유.
- `projection_geometry`: rectilinear/fisheye/tele-compressed 같은 기하 효과를 소유.
- `focus_priority`: 어느 객체/부위가 먼저 선명해야 하는지 소유.
- `depth_of_field`: 층별 선명도 범위와 falloff만 소유.
- `focus_method`: single-plane, stack, tilted-plane, split-diopter 등을 소유.
- `optical_blur_character`: optical bokeh/falloff와 diffusion/soft-focus를 구분.
- 기존 `shot_scale`: 화면 안 크롭/프레이밍만 소유하며 거리를 대신하지 않음.

구현 시 `lens.85mm`에서 shallow DoF를 제거해야 한다. 정확한 `85mm` 요청이 있으면 수치 힌트는 보존하되, shallow DoF는 `depth_of_field`에 독립적으로 존재할 때만 하드가 된다.

### 7.3 레이어별 책임

| 레이어 | 소유 내용 | 하드 여부 |
|---|---|---|
| authorial core / intent lock | 요청자가 정확히 지정한 시점, 수치, 초점 대상, 보이는 효과 | exact/request-grounded일 때만 hard |
| `photo_prompt_tags.json` | 넓은 탐색용 후보와 액추에이터 문구 | 기본 advisory |
| `references/camera-optics-contract.md` 제안 | 축 정의, 인과 일관성, 혼동 경계, 문장 구성 규칙 | 설계 지식; 구현 전에는 없음 |
| `photo_prompt_quality_layers.json`의 `optical_coherence` 제안 | 선택된 축들 사이의 충돌과 누락 검사 | 선택된 의도에 대한 quality gate |
| visual obligations | 특정 개념이 정말 카메라 관계를 핵심 의미로 가질 때의 보조 observable | 전역 optics owner로 사용하지 않음 |
| generated semantic index | 검색 산출물 | authored source 아님; 직접 편집 금지 |

## 8. 의미 구성요소와 혼동 경계

| 의미 | 필수 observable components | hard negatives / false substitutes |
|---|---|---|
| fisheye | 광범위 곡률 또는 주변부 휨 + 근접 물체 크기 이득 + 깊이 확장 | 높은 시점만, 원형 vignette만, 단순 wide crop |
| close rectilinear wide | 가까운 요소 크기 이득 + 수렴하는 깊이선 + 통제된 주변부 stretch | 낮은 시점만, 큰 얼굴 crop만, 몸 포즈로 만든 대각선 |
| telephoto compression | 먼 카메라 위치 + 좁은 화각 + 여러 거리 물체의 간격이 작아 보임 | bokeh만, 평평한 단색 배경만, 단순 crop |
| tilt-focus miniature | 높은 전체 조망 + 장면 기하에 맞는 선명 밴드 + 앞/뒤 falloff + 스케일 단서 | 화면 상하에 얹은 gradient blur만, 장난감 소품/문자만 |
| top-down flat-lay | 장면 평면에 거의 90° + 물체의 coplanar 배열 + 그 평면의 폭넓은 선명도 | 높은 각도의 인물 사진, 사선 table shot |
| macro focus plane | 재현 배율이 큰 디테일 + 이름 붙은 초점 평면 + 그 평면에서 점진적 falloff | 일반 사진을 crop/upscale, 배경 blur만 |
| context-readable moderate DoF | 주 피사체 crisp + 환경 식별 가능 + 층별 점진적 연화 | 피사체 컷아웃과 붙여 넣은 sharp 배경, 무조건적 generic bokeh |
| focus stack | 정지한 장면의 서로 다른 깊이 대상 + 확장 선명도 + 다중 초점 캡처/합성 방법 명시 | 움직이는 인물의 무설명 단일 프레임, 단순 deep focus |
| split diopter | 가까운 대상과 먼 대상의 두 분리 평면이 선명 + 중간 전이/분리 단서 | 모든 층이 같은 선명도, 서로 같은 거리의 두 얼굴 |
| deliberate missed focus | 의도된 대상의 빗나간 초점 + 대체 선명 평면 + 서사/매체상 이유 | 저해상도, 모션 블러, 전체 diffusion |

공통 혼동 변수:

- 피사체의 몸 기울기/포즈, 크롭, 대각선 건축선, 카메라 roll.
- 센서 크기, 크롭 계수, aspect ratio, 후처리 crop.
- 카메라-피사체 거리와 피사체-배경 거리.
- 모션 블러, 대기 haze, diffusion/beauty filter, 국소 contrast/oversharpening.
- 깊이 없는 평면 배경, 합성된 배경, vignette, 임의의 gradient/local blur.
- 조명·색의 주목도, 미니어처 소품/문자, 크기 비교 물체.

인물 픽셀에서는 보이는 성인 외형, 포즈, 스타일링, 동작, 공간 관계만 관찰했다. 정체성 동일성, 실제 관계, 보호 특성, 건강, 매력, 성격, 직업, 민족/국적 등은 추론하지 않았다.

## 9. 렌더 게이트

### 9.1 프롬프트/계약 게이트

- exact 요청의 수치 초점거리, equivalence basis, f-number가 그대로 보존되는가.
- 요청한 초점 대상과 상대 평면이 명시되는가.
- shallow/deep이 단독 수식어로 끝나지 않고 foreground/subject/background 상태로 풀리는가.
- 렌즈 후보가 심도나 카메라 거리를 몰래 하드 잠그지 않는가.
- focus stack/tilt/split-diopter를 일반 단일 초점과 혼동하지 않는가.
- 같은 필드에서 `very shallow`와 분리된 near/mid/far 모두 sharp처럼 물리적으로 충돌하는 요구가 있으면 revise/clarify하는가.

### 9.2 썸네일 게이트

- 시점/투영이 레이블이 아니라 주요 장면 기하를 바꾸는가.
- 첫 읽기에서 의도된 주 초점 대상 또는 초점 밴드가 하나로 잡히는가.
- context-readable이 목표면 환경의 정체가 축소 상태에서도 남는가.
- fisheye/tilt/top-down/split-plane 같은 특수 관계가 축소해도 구분되는가.
- 크롭, pose, vignette, 배경 blur 하나로 목표 의미를 대체하지 않는가.

### 9.3 원본(native) 게이트

- 곡률, 수렴, 크기 변화가 관련 표면과 깊이선 전반에서 일관적인가.
- 같은 초점 평면의 대상들은 비교 가능한 선명도를 가지며, 분리된 평면은 stack/split/tilt가 아닌 한 요청한 방향으로 연속적으로 falloff하는가.
- 흐림이 피사체 윤곽에 붙인 임의 마스크나 상·하 gradient처럼 보이지 않는가.
- deep focus는 near/mid/far가 모두 식별 가능해야 하지만, 대기 원근이 있는 먼 산까지 동일 microsharpness일 필요는 없다.
- focus stack은 정지 장면의 분리 깊이에 확장 선명도를 제공하고, halo/이음새/복제 테두리가 없어야 한다.
- 숫자 렌즈·조리개는 픽셀만으로 PASS 처리하지 않는다. 해당 수치의 **의도된 효과**만 픽셀에서 평가한다.

각 타깃의 필수 게이트 하나라도 실패하면 `partial_is_fail`로 둔다. 생성 차단·누락은 품질 0점이 아니라 `UNSCORED`, 사용자 수용은 별도 미평가다.

## 10. 회귀와 held-out 시험 설계

모든 인과 쌍은 피사체, 장면, 조명, aspect ratio, seed 가능한 입력을 고정하고 한 광학 축만 바꾼다. positive와 hard negative는 독립 생성으로 저장하며, 한 팔의 결과를 다른 팔의 입력으로 쓰지 않는다.

| # | positive | hard negative | 핵심 판정 |
|---:|---|---|---|
| 1 | 가까운 손+깊은 골목의 fisheye | 높은 각도 인물+원형 vignette | 곡률·근접 크기 이득·깊이 확장 3개 모두 |
| 2 | 가까운 rectilinear wide | 동일 장면의 low-angle crop-only | 수렴/크기 이득은 있으나 fisheye 곡률 없음 |
| 3 | 먼 카메라와 여러 평면의 tele compression | 얕은 bokeh만 있는 근접 portrait | 배경 흐림이 아니라 거리 간격 압축 |
| 4 | 흐린 전경 잎→선명 인물→읽히는 온실 | generic background blur 또는 pasted background | 3층 순서와 연속 falloff |
| 5 | 곤돌라 interior/reflection/mountain deep focus | 인물과 sharp 산을 합성한 장면 | near/mid/far의 재질/반사/경계 일관성 |
| 6 | 90° coplanar flat-lay | oblique high-angle table shot | 평면 법선과 카메라 pitch 관계 |
| 7 | 꽃/입술의 이름 붙은 macro plane | 분리된 눈·꽃·손가락이 모두 sharp인 `very shallow` 단일 평면 | 실제 초점면과 점진 falloff |
| 8 | 정지 제품의 focus stack | 움직이는 인물의 무설명 broad sharpness | 다중 캡처 방법과 확장 깊이의 적합성 |
| 9 | 높은 조망+일관된 중앙 focus band의 tilt miniature | toy text+상하 gradient blur | 장면 기하를 따르는 밴드/스케일 |
| 10 | 카메라 용어 없는 control은 authorial choice로만 광학을 선택 | 검색 유사도만으로 85mm/shallow를 hard 삽입 | advisory/hard 경계 |
| 11 | split-diopter: 가까운 소품과 먼 얼굴 두 평면 | 같은 거리 두 대상 또는 전체 deep focus | 분리 평면과 중간 전이 |
| 12 | `deep enough for context` | 모든 픽셀을 동일 선명화한 과도한 deep focus | 환경 식별성과 자연스러운 거리 감쇠 |

### held-out 구성

- 학습/설계 근거로 사용한 17개 게시물은 첫 회귀의 점수용 held-out에서 제외한다.
- early/middle/late 각 구간에서 최소 하나씩, portrait와 non-portrait를 모두 포함한다.
- 일반 렌즈 숫자 없이 관계 문장만 있는 표본, 숫자는 있지만 거리/초점면이 없는 표본, 특수 투영 표본을 분리한다.
- prompt audit, composed request audit, native pixel review, 사용자 판단을 같은 점수로 합치지 않는다.
- 동일 의미의 한국어/영어 표현과 full-frame-equivalent 유무를 언어/포맷 holdout으로 둔다.

## 11. 한계와 후속 조건

- 전수 스캔은 정규식 기반이라 부정문, 은유, 필름 포맷, 동일 본문의 변형을 완전히 분리하지 못한다. 고유 본문 수를 함께 제시했지만 의미 분류 정밀도 평가는 아니다.
- 34장 픽셀 표본은 목적 표본이다. 드문 메커니즘과 혼동 경계에는 유용하지만 코퍼스 전체 성공률을 추정하지 않는다.
- 이미지 파일에는 실제 촬영 EXIF/생성 파라미터를 인증하는 근거가 없으므로, 렌즈/조리개/카메라 모델은 프롬프트 주장으로만 기록했다.
- 본 보고서는 코드·자산·인덱스·테스트를 바꾸지 않았다. 따라서 proposed IR의 파서, 조합 우선순위, 후보팩 직렬화, backward compatibility는 아직 검증되지 않았다.
- 새 후보를 실제로 채택하려면 다음 순서가 필요하다: authored source 구현 → 생성 인덱스 재빌드 → focused contract/coherence 테스트 → 독립 positive/hard-negative 렌더 → thumbnail/native 이중 리뷰 → 사용자 판단.

**최종 결정은 `proposed`이다.** 핵심 구조와 회귀 조건은 구현 가능한 수준으로 구체화되었지만, 구현·렌더 적합성·사용자 판단은 모두 남아 있다.

## 부록 A — 픽셀 증거 파일

모든 경로의 기준 디렉터리는 `generated/reactorprompt-export-20260902-incremental/`이다.

- 1586: `images/1586_DY1yjxkmkT__01.jpg`, `images/1586_DY1yjxkmkT__02.jpg`
- 1587: `images/1587_DY10cywGvWk_01.jpg`, `images/1587_DY10cywGvWk_02.jpg`
- 1662: `images/1662_DY9l8a3mvkn_01.jpg`, `images/1662_DY9l8a3mvkn_02.jpg`
- 1902: `images/1902_DZuDDN0mkYs_01.jpg`, `images/1902_DZuDDN0mkYs_02.jpg`
- 1953: `images/1953_DZ44vuJmsGe_01.jpg`, `images/1953_DZ44vuJmsGe_02.jpg`
- 1956: `images/1956_DZsAndnmge1_01.jpg`, `images/1956_DZsAndnmge1_02.jpg`
- 2076: `images/2076_DaZc8egGuUe_01.jpg`, `images/2076_DaZc8egGuUe_02.jpg`
- 2077: `images/2077_DaaYKTUGp4p_01.jpg`, `images/2077_DaaYKTUGp4p_02.jpg`
- 2158: `images/2158_DauI7KYms5l_01.jpg`, `images/2158_DauI7KYms5l_02.jpg`
- 2245: `images/2245_DbDB_cGGiFp_01.jpg`, `images/2245_DbDB_cGGiFp_02.jpg`
- 2299: `images/2299_DbcuYZ-GmbV_01.jpg`, `images/2299_DbcuYZ-GmbV_02.jpg`
- 2470: `images/2470_DcAfPqLmgP5_01.jpg`, `images/2470_DcAfPqLmgP5_02.jpg`
- 2641: `images/2641_DcfQR7cmhdc_01.jpg`, `images/2641_DcfQR7cmhdc_02.jpg`
- 2666: `images/2666_DclmMmHmvGC_01.jpg`, `images/2666_DclmMmHmvGC_02.jpg`
- 2680: `images/2680_Dcn2LesmjBy_01.jpg`, `images/2680_Dcn2LesmjBy_02.jpg`
- 2711: `images/2711_DcqCkahGovW_01.jpg`, `images/2711_DcqCkahGovW_02.jpg`
- 2742: `images/2742_Dcx0CYwmkWj_01.jpg`, `images/2742_Dcx0CYwmkWj_02.jpg`

## 부록 B — 재현 명령과 산출 근거

```bash
# 동결 manifest와 authored source 확인
shasum -a 256 generated/reactorprompt-export-20260902-incremental/manifest.json
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json | shasum -a 256
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json | shasum -a 256
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json | shasum -a 256

# 전체/고유 프롬프트 모수
jq '[.[] | select((.prompt // "") != "")] | length' generated/reactorprompt-export-20260902-incremental/manifest.json
jq -r '.[] | select((.prompt // "") != "") | .prompt' generated/reactorprompt-export-20260902-incremental/manifest.json | sort -u | wc -l

# authored slot과 quality rule 검사 예시
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_tags.json \
  | jq '.slots | {lens, focus, camera_direction, camera_height, camera_type, shot_scale}'
git show 401f450e4c0ec32ef79c502e3c6a6666c9a106c4:skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json \
  | jq '.. | objects | select(.id? == "close_camera_depth" or .id? == "frame_hierarchy" or .id? == "layered_depth_order" or .id? == "close_focus_priority" or .id? == "shot_intent")'
```

전수 계수는 manifest 배열의 924개 비어 있지 않은 `.prompt`를 순회해 사전에 고정한 대소문자 무시 정규식 집합으로 게시물 ID와 본문 SHA를 집계했다. 표본은 각 선택 ID의 `.images[] | select(.download_ok == true) | .local_file` 중 처음 두 경로로 고정했다.

## 부록 C — 외부 출처

1. Nikon, [Understanding Focal Length](https://www.nikonusa.com/learn-and-explore/c/tips-and-techniques/understanding-focal-length)
2. Sony, [Factors of Defocus](https://www.sony.com/electronics/support/articles/00267923)
3. ZEISS, [Depth of Field and Bokeh](https://lenspire.zeiss.com/photo/app/uploads/2022/02/technical-article-depth-of-field-and-bokeh.pdf)
4. Nikon, [Special-Purpose Lenses](https://www.nikonusa.com/c/lenses/dslr-lenses/special-purpose)
5. Sony, [Focus Stacking vs. Focus Bracketing](https://www.sony.com/electronics/support/e-mount-body-ilce-7-series/ilce-7m4k/articles/00342633)

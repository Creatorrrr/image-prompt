# 촬영 매체·캡처 응답·후처리 시각 의미 리서치

- 주제: 촬영 매체, 스마트폰/전면 카메라, 콤팩트 디지털카메라, 스튜디오, 직광 플래시, 필름/그레인, 압축, 후처리
- 상태: `proposed`
- 모드: research/design only
- 대상 기준선: `skills/photo-prompt-image-generator` @ `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 코퍼스: ReactorPrompt incremental manifest SHA-256 `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`

## 결론 요약

이 코퍼스에서 재사용할 단위는 `iPhone`, `RAW`, `CCD`, `35mm`, `Kodak` 같은 장비·포맷·브랜드명이 아니라 다음의 **보이는 캡처 응답 관계 묶음**이다.

1. 카메라-피사체 거리와 근거리 원근
2. 광원 축과 노출 감쇠
3. 초점면과 광학적 선명도 변화
4. 하이라이트 숄더, 그림자 분리, 화이트밸런스 같은 톤 응답
5. 그레인·색 노이즈·노이즈 제거 같은 신호 응답
6. JPEG 블록/링잉 같은 출력·전송 응답
7. 얼굴·손·재질을 훼손하지 않는 피델리티 상한

프롬프트 측에서는 장비/매체 이름이 매우 자주 등장하지만 구성요소가 따라오지 않는다. `smartphone/iPhone/phone camera` 계열 217건 중 이 조사에서 정의한 근거리 기하 구성요소와 신호/출력 구성요소가 모두 있는 것은 21건뿐이고, 120건은 둘 다 없었다. `compact digital/CCD/digicam` 32건 중 플래시·아티팩트·제한적 톤 응답 세 묶음이 모두 있는 것은 1건이었다. 반면 픽셀 표본에서는 장비 이름보다 **근거리 셀피 기하**와 **직광 플래시의 피사체-배경 밝기 관계**가 훨씬 먼저 읽혔다.

현재 데이터에는 이미 `early_2000s_compact_digicam_social_repost`, `direct_on_camera_flash_snapshot_signature`, `highlight_rolloff_tone_response`, `mixed_illuminant_white_balance_relation`, `film_halation_highlight_edge_relation`처럼 좁고 잘 분해된 계약이 있다. 따라서 콤팩트 디카 프로필을 중복 추가하는 것보다 다음이 우선이다.

- 브랜드·장비·RAW 명칭을 `input metadata/advisory alias`로 낮추고, 보이는 효과 축과 분리한다.
- `quality_layers`에 명시적 캡처 매체가 선택됐을 때만 작동하는 `capture_response` 교차 슬롯 소유권을 둔다.
- 기존 `film_emulation`, `grain_profile`, `texture`, `quality`의 추상 후보를 보이는 효과와 혼동 경계로 보강한다.
- 전면 카메라 저조도 묶음은 후보팩으로만 제안한다. 관련 프롬프트가 4건뿐이고 8개 픽셀 모두에서 노이즈+압축 묶음이 완전하게 읽히지 않아 hard profile 승격 근거가 없다.

## 범위와 표본 방법

### 프롬프트 전수 스캔

- `manifest.json`의 `prompt_missing == false`이며 본문이 비어 있지 않은 924개 레코드를 모두 스캔했다.
- 분모: 924개 프롬프트, 고유 본문 904개.
- 정규식은 대소문자를 무시했다. `no HDR`, `no heavy retouching`처럼 부정문도 **해당 처리 축이 프롬프트에 언급되었다**는 집계에는 포함했다. 따라서 집계는 선호 방향이나 픽셀 성공률이 아니라 프롬프트 측 언급량이다.
- `35mm`는 렌즈 초점거리와 필름 포맷을 혼동하기 쉬워 `35mm film`, `35mm snapshot`, `film photography`처럼 필름 문맥이 붙은 경우만 별도 집계했다.

### 픽셀 표본

픽셀 표본은 빈도 추정용 무작위 표본이 아니라 혼동 경계를 찾기 위한 명시적 층화 표본이다.

- 핵심 표본: 22개 게시물에서 각 첫 2장, 합계 44장.
  - 초기 ID대: 1759, 1760, 1842, 1843, 1865, 1867, 1881, 1882
  - 중기 ID대: 2275, 2278, 2324, 2325, 2326, 2380, 2381
  - 후기 ID대: 2679, 2680, 2712, 2713, 2728, 2741, 2742
  - 양성: 장치명, 직광, 필름/그레인, 노이즈, JPEG/압축, clean digital 중 하나 이상을 명시한 게시물.
  - 근접 대조: 가까운 ID에서 장비 이름이 없거나, 같은 `CCD/RAW/film` 라벨이 있으나 관계 묶음이 다른 게시물.
- 좁은 전면 카메라 보충 표본: 전수 스캔에서 잡힌 4개 게시물 2102, 2156, 2535, 2712의 첫 2장씩 8장 전부.
- 2712가 중복되므로 실제 고유 표본은 **25개 게시물, 50장**이다.
- 1759, 1843, 1865, 2278, 2325, 2326, 2712, 2728의 첫 이미지는 중앙 512×512 native crop으로 다시 확인했다. 이 검토는 작은 그레인·노이즈·JPEG 경계 아티팩트가 썸네일 축소에서 사라지는 혼동을 줄이기 위한 보충이다.
- 관찰은 보이는 성인 표현, 촬영 기하, 빛, 색, 초점, 신호 질감으로 제한했다. 정체성, 실제 인물 동일성, 보호 특성, 실제 관계, 건강, 성격, 직업은 추론하지 않았다.

### 전달 인코딩 혼동

수집된 4,908장 자체의 파일 포맷은 JPEG 4,862장, WebP 33장, PNG 13장이다. 따라서 native 이미지에서 JPEG 계열 아티팩트를 보더라도 그것이 프롬프트로 의도된 `social repost`인지, 생성물 저장인지, 사이트 전달 과정의 재인코딩인지 이 코퍼스만으로는 귀속할 수 없다. 파일 포맷은 전달 메타데이터이고, 픽셀 관찰은 보이는 결과일 뿐이다.

## 프롬프트 측 발견과 집계

### 1차 언급 집계

| 휴리스틱 | 매치 게시물 | 고유 본문 | 경계 |
|---|---:|---:|---|
| `smartphone`, `phone camera`, `iPhone`, `mobile photo` | 217 | 210 | 장치명/계열 언급 |
| `front-facing phone`, `phone front camera`, `front camera`, `selfie camera` | 4 | 4 | 전면 카메라 명시 |
| phone/selfie/arm's-length 기하 표현 | 31 | 30 | 기하 단서 언급 |
| `compact digital camera`, `compact-camera`, `digicam`, `CCD` | 32 | 32 | 콤팩트/CCD 라벨 |
| iPhone/Canon PowerShot 등 명시적 브랜드·모델 | 102 | 98 | 입력 메타데이터 라벨 |
| `RAW photo`, `RAW-derived`, `RAW-level`, `ProRAW` | 16 | 15 | 포맷/워크플로 라벨 |
| direct/on-camera/built-in/harsh flash | 62 | 62 | 카메라축 직광 언급 |
| studio strobe/direct strobe | 2 | 2 | 스튜디오 스트로브 언급 |
| film mood/look/aesthetic, filmic, analog, 필름 브랜드 | 58 | 56 | 필름 에뮬레이션 라벨 |
| film/fine/subtle/visible/organic/analog grain | 201 | 198 | 그레인 언급 |
| sensor/digital/chroma/low-light/shadow/tonal noise | 52 | 49 | 디지털 노이즈 언급 |
| JPEG/JPG/mosquito noise/blocking/recompression | 17 | 17 | JPEG 출력 단서 |
| compression/compressed/macroblocking/bitrate | 64 | 62 | 압축 언급 |
| halation/optical bloom/bloom | 68 | 67 | 광휘·할레이션 언급 |
| post-processing/color grading/tone mapping/processing | 76 | 74 | 처리/그레이딩 언급 |
| beauty filter/heavy retouch/unedited 등 | 232 | 226 | 필터/리터칭 축 언급; 부정문 포함 |
| HDR/high dynamic range | 118 | 117 | HDR 축 언급; 부정문 포함 |
| clean digital/digital editorial capture/natural photographic finish | 12 | 12 | clean digital 명시 |
| studio portrait/photo/capture/setup/polish/lighting | 125 | 125 | 스튜디오 문맥; 촬영 매체와 동일하지 않음 |
| 필름 문맥이 명시된 `35mm` | 12 | 12 | 초점거리 `35mm` 제외 |

### 공기재와 구성요소 완성도

| 기준 라벨 | 라벨 분모 | 구성요소 1 | 구성요소 2 | 구성요소 3 | 전부 | 아무 구성요소도 없음 |
|---|---:|---:|---:|---:|---:|---:|
| phone 계열 | 217 | 근거리/셀피 기하 32 | 신호·압축·HDR 응답 86 | - | 두 축 모두 21 | 120 |
| compact/CCD 계열 | 32 | 직광 9 | 노이즈/프린징/JPEG 17 | 제한 톤·혼합 WB·감쇠 9 | 세 축 모두 1 | 12 |
| film-emulation 계열 | 58 | 그레인 42 | 하이라이트 숄더/할레이션 28 | 색 분리/필름 색 24 | 세 축 모두 12 | 7 |

선택 공기재는 다음과 같다.

- phone + sensor noise: 35
- phone + JPEG: 12
- phone + compression: 31
- phone + direct/on-camera flash: 15
- compact/CCD + direct/on-camera flash: 9
- compact/CCD + JPEG: 8
- film-emulation label + grain: 42
- direct/on-camera flash + grain: 31
- processing/grade + grain: 35

### 프롬프트 측 해석

1. `iPhone 17 Pro RAW`, `Canon PowerShot G7 X`, `35mm film mood`는 자주 시각 효과를 대신한다. 그러나 브랜드·모델·RAW는 그 자체로 픽셀에서 검증 가능한 효과가 아니다.
2. `smartphone-style`은 때때로 근거리 셀피가 아닌 일반 제3자 촬영 인물사진에도 붙는다. 1759가 대표적이다. 따라서 medium 라벨과 camera-to-subject topology를 분리해야 한다.
3. `film grain`, `fine grain`, `subtle compression`은 다른 구성요소 뒤에 한 번 덧붙는 경우가 많다. 효과 위치, 크기, 톤 의존성, 경계 보존 조건이 없어 생성기에서 생략되거나 전역 텍스처로 오용되기 쉽다.
4. `RAW-level skin detail`은 리터칭되지 않은 피부를 의미하는 표현처럼 쓰이지만 RAW는 파일/워크플로 정보다. clean digital, microtexture, sharpening, highlight response를 각각 말해야 한다.
5. 직광 프롬프트가 가장 관계적으로 구체적이었다. 실제 픽셀에서도 장비명보다 카메라축, 정면 반사, 근거리 피사체-원거리 배경의 노출 차이가 잘 읽혔다.

## 픽셀 측 관찰과 표본 ID

아래 관찰은 50장 표본에만 적용하며 전체 4,908장의 빈도로 일반화하지 않는다.

### daylight phone/film label과 근접 대조

- **1759 vs 1760**: 1759는 `smartphone-style`과 `subtle compression artifacts`를 명시하지만 두 장 모두 깨끗한 제3자 촬영형 해변 인물사진으로 읽혔다. 1760 대조도 유사하게 깨끗하며 차이는 주로 금빛 역광과 포즈였다. 스마트폰/압축 라벨은 첫인상 판별자가 아니었다.
- **1881 vs 1882**: 1881의 `smartphone photo with a soft 35mm film mood`는 부드러운 실내 자연광 사진으로 보였고, 그레인·할레이션·필름 톤 응답이 첫인상에서 분리되지 않았다. 1882의 일반 야외 사진도 비슷한 고해상도·매끈한 마감이었다.
- **2278 vs 2275**: 2278은 `iPhone 17 Pro RAW`, `sensor noise`를 명시하지만 두 장 모두 매우 정제된 에디토리얼 이미지로 보였다. 2275는 장비 라벨이 없는 석양 장면인데도 피사체와 원거리 배경의 노출 분리가 있어 장비명을 시각 원인으로 역추론할 수 없었다.
- **2325**: high handheld, 근거리 광각, 손가락의 원근 확대, 대각 구도는 phone/selfie capture를 강하게 지지했다. 반면 `mild JPEG sharpening`과 sensor grain은 native crop에서도 결정적으로 보이지 않았다.

### compact/CCD/direct-flash/strobe

- **1842, 1843**: 야간 주변광 속 정면 밝기와 색 조명은 보였지만 `CCD` 자체는 검증할 수 없었다. 1843의 compact-camera 명시는 픽셀보다 입력 메타데이터였다. 미세 그레인/디지털 노이즈는 썸네일에서 분리되지 않았다.
- **1865, 1867**: 두 게시물 모두 야간 배경보다 성인 피사체가 갑자기 밝고 정면 반사가 강했다. 1865의 direct flash와 1867의 soft flash 모두 유사한 소비자 스냅 광학을 만들었다. `CCD`보다 광원 축과 near/far exposure가 더 유효한 의미였다.
- **2326**: 근거리 top-down 광각과 harsh built-in flash가 함께 읽혔다. 코·볼·모자에 작은 정면 하이라이트가 있고 배경은 급격히 어두워졌다. 그러나 `JPEG softness`, `sensor noise`, `red-eye-era rendering`은 중앙 native crop에서 명확하지 않았다.
- **2381**: 카메라축에 가까운 hard strobe, 높은 시점, 강한 set color와 그림자가 썸네일에서 읽혔다. `subtle analog grain`은 판별자 역할을 하지 않았다.
- **2679**: 벽에 생긴 단단한 그림자, 장신구 하이라이트, 피사체-배경 분리가 on-camera flash를 강하게 지지했다. `color-negative film character`와 fine grain은 그보다 훨씬 약했다.
- **2728**: 어두운 바다/테라스와 밝은 피사체, 작은 정면 하이라이트는 flash pop을 지지했다. `Canon PowerShot`, `RAW-derived`, film grain은 픽셀만으로 검증되지 않았다.

### clean digital, processing, studio control

- **2380**: `RAW-level skin detail`, no excessive retouching을 명시하지만 두 장은 매우 매끈한 스튜디오 뷰티 마감으로 보였다. RAW 라벨은 미세 피부 구조의 보존을 보장하지 않았다.
- **2680**: top-down 제품 스튜디오 대조는 broad even light, 넓은 초점면, 매끈한 상업 마감으로 읽혔다. social/consumer-camera artifact가 붙으면 안 되는 hard negative다.
- **2713**: clean digital macro는 근접 피부·손가락·니트 디테일과 점진적 초점 이탈이 주된 단서였다. 장비명이 없어도 clean editorial response가 읽힐 수 있었다.
- **2741 vs 2742**: 2741의 `clean digital editorial capture`와 2742의 일반 naturalistic cinematic beauty 사진은 모두 고해상도·깨끗한 마감이었다. 두 장르의 차이는 색과 빛이었고, `clean digital` 라벨만의 배타적 픽셀 서명은 없었다.

### 전면 카메라 4개 게시물 전수 보충

- **2102**: 두 장 모두 뻗은 팔, 가까운 거리, 약한 광각 원근이 보였다. 낮 환경에서는 인위적인 노이즈나 압축을 요구하지 않아도 phone topology가 충분히 읽혔다.
- **2156**: `iPhone 17 Pro RAW`, straight-on front camera, grain/haze/compression을 명시하지만 두 장은 뷰티 필터처럼 부드럽고 정제되어 보였다. 프레임은 셀피처럼 보이나 신호/출력 아티팩트 묶음은 완성되지 않았다.
- **2535**: 저조도 파란 주변광, 근거리 high-angle 셀피는 읽혔지만 특정 iPhone 또는 실제 전면 센서임을 증명하지는 않았다. 명확한 shadow chroma noise나 JPEG 경계 아티팩트도 첫인상 판별자가 아니었다.
- **2712**: 어두운 방, 얼굴 중심의 근거리 프레임, 화면광처럼 보이는 아래쪽 푸른 빛은 저조도 영상통화 느낌을 만들었다. 그러나 두 장 모두 비교적 깨끗해 프롬프트의 noise+compression+focus miss가 모두 통과했다고 볼 수 없다.

### native crop 보충

1759, 1843, 1865, 2278, 2325, 2326, 2712, 2728의 중앙 512×512 crop에서는 다음을 확인했다.

- 직광의 정면 반사와 소재 응답은 남았다.
- 피부·머리카락·의류가 전반적으로 고해상도·매끈하게 보였다.
- `JPEG blocking/mosquito noise`, 특정 센서의 노이즈, 필름 입자라고 단정할 수 있는 완전한 아티팩트는 8개 crop 어디에서도 결정적이지 않았다.
- 이는 전체 프레임의 모든 미세 아티팩트가 없다는 증명이 아니라, 적어도 이 후보들이 썸네일/중앙 native first-read를 지배하지 않았다는 증거다.

## 프롬프트-픽셀 정렬과 불일치

| 관계 | 프롬프트 증거 | 픽셀 표본 | 결론 |
|---|---|---|---|
| 근거리 phone/selfie 기하 | high handheld, arm's length, 24–28mm, steep angle | 2102, 2325, 2326, 2535에서 비교적 잘 읽힘 | 라벨보다 기하가 강함 |
| direct/on-camera flash | 카메라축, 작은 광원, near/far drop | 1865, 2326, 2381, 2679, 2728에서 강함 | 조명 소유권이 핵심 |
| compact/CCD | CCD/compact label + 일부 noise/JPEG | 같은 직광을 가진 다른 장면과 구별 어려움 | 장비 라벨은 advisory |
| RAW | RAW/ProRAW/RAW-level 16건 | 2278, 2380, 2728은 서로 다른 깨끗한 마감 | RAW는 픽셀 스타일이 아님 |
| film label | film mood/look + grain/grade | 1881 등에서 clean digital과 구별 약함 | 효과 축 분해 필요 |
| grain/noise/compression | 201/52/64건 언급 | native 보충에서도 완전한 판별자 부족 | 위치·규모·보존 조건 필요 |
| clean digital | 12건 명시 | 2741과 일반 2742의 배타적 차이 없음 | 자연 디테일과 톤 응답으로 정의 |

불일치가 프롬프트 실패라고 단정되지는 않는다. 모델·버전·설정·seed·시도 정책이 고정되지 않았고, 수집본은 최종 전달 파일이므로 생성기 응답과 사이트 인코딩이 섞여 있다. 여기서 말할 수 있는 것은 **라벨 단독이 표본 픽셀의 안정적인 first-read가 아니었다**는 것뿐이다.

## 기존 데이터 중복과 소유권

### 현재 겹치는 데이터

- `photo_prompt_visual_obligations.json`
  - `early_2000s_compact_digicam_social_repost`: near-axis flash, close background shadow/falloff, limited dynamic range/mixed WB, CCD chroma/fringing, mild JPEG recompression을 이미 5개 필수 그룹과 thumbnail/native gate로 정의한다.
  - `direct_on_camera_flash_snapshot_signature`
  - `diffusion_filter_highlight_halation`
  - `mixed_illuminant_white_balance_relation`
  - `highlight_rolloff_tone_response`
  - `film_halation_highlight_edge_relation`
  - `overhead_social_snapshot_relation`, `mirror_selfie_reflection_device_topology`
- `photo_prompt_lighting_extension.json`
  - `direct_flash_y2k_snapshot`: near-camera axis, near/far drop, close shadow, compact hotspots를 소유한다.
  - `filmic_muted_halation`: 실제 밝은 경계에 국소화된 halo, protected highlight, color separation을 소유한다.
- `photo_prompt_tags.json`
  - medium 57개, camera_type 25개, film_emulation 18개, grain_profile 7개, lens_artifact 10개, color_grading 8개, texture 134개, quality 20개.
  - 관련 기존 후보: `smartphone_snapshot`, `selfie_camera_photo`, `smartphone_camera`, `front_facing_phone`, `compact_digital_camera`, `digicam_2000s_camera`, `smartphone_night_noise`, `ccd_chroma_noise`, `jpeg_social`, `compact_digicam_noise`, `clean_digital`, `phone_realism`, `no_hdr_natural_snapshot`, `consumer_camera_authenticity`, `fidelity_ceiling_natural_detail`.
- `photo_prompt_quality_layers.json`
  - `shot_intent`, `light_provenance`, `frame_hierarchy`, `decisive_moment`, `environment_consequence`의 다섯 photographic craft 차원이 있으나, 명시된 매체 라벨과 신호·톤·출력 응답을 교차 검증하는 독립 소유자는 없다.

### 소유권 제안

| 정보 | 올바른 소유 계층 | 비고 |
|---|---|---|
| iPhone/Canon/film-stock/RAW 이름 | `camera_type` 또는 `film_emulation`의 advisory input label | 픽셀 원인·증거로 승격 금지 |
| 근거리 거리·시점·원근·팔/기기 topology | camera/composition/visual obligation | 이 주제에서는 참조만 하고 재소유하지 않음 |
| flash 축·그림자·specular·near/far exposure | lighting extension + flash visual obligation | 기존 계약 재사용 |
| highlight rolloff, mixed WB, halation | 기존 tone/color/lighting visual obligations | 효과별 소유 |
| grain/noise/denoise | `grain_profile` | 전역 overlay가 아닌 신호 위치/규모를 명시 |
| chromatic fringe/flare/optical imperfection | `lens_artifact` | signal noise와 분리 |
| JPEG/소셜 재압축 | `texture` 또는 별도 export-response candidate | 전달 JPEG와 의도 효과를 분리 |
| 교차 슬롯 일관성, fidelity ceiling | `photo_prompt_quality_layers.json`의 제안 `capture_response` | 다른 슬롯을 복제하지 않고 의존성만 검사 |
| 좁은 완성 묶음 | `photo_prompt_visual_obligations.json` | 정확 용어 또는 구성요소 완성 시에만 hard |

### 현재 데이터의 핵심 빈틈

1. `film_emulation`의 다수 브랜드 항목은 `Kodak Portra 400 ... warm skin tones`처럼 라벨과 한두 결과 형용사만 갖고 있다. 후보 자체에 `label_provenance`, `claim_boundary`, `observable_axes`, `confusion_negatives`가 없다.
2. `phone_realism`, `consumer_camera_authenticity`, `clean_digital image quality`는 결과 방향이 추상적이다. 기하·빛·신호·출력 중 누가 그 효과를 소유하는지 알 수 없다.
3. `jpeg_social`은 `subtle ... feel`로 되어 있어 실제 JPEG 경계 아티팩트와 전역 blur/pixelation을 가르지 못한다.
4. `smartphone_night_noise`와 `ccd_chroma_noise`는 이름은 있으나 필름 그레인, 균일한 overlay, 뷰티 필터 softness와의 혼동 경계가 후보 데이터에 없다.
5. 기존 compact-digicam hard profile은 이미 충분히 강하다. 이 프로필과 새 후보 묶음이 중복 선택되지 않도록 compositional reuse 규칙이 필요하다.

## 제안 시각 구성요소와 혼동 경계

### 공통 `capture_response` 표현

| 축 | 관찰 가능한 구성요소 | 혼동 음성 예 |
|---|---|---|
| `capture_geometry` | 거리, 시야각, 근거리 크기 변화, 팔/기기 위치, 카메라 높이 | 장비 이름만 있는 일반 인물사진 |
| `light_exposure_response` | source axis, near/far brightness, shadow edge, compact hotspot, ambient survival | global overexposure, 단순 contrast grade |
| `focus_optical_response` | 초점면, 가장자리 이탈, motion/focus miss, optical softness 위치 | 전역 Gaussian blur, 얼굴만 뷰티 필터 |
| `tone_color_response` | highlight shoulder, black floor, mixed-WB 공간 분리, color separation | LUT 이름, 전역 orange-teal grade |
| `signal_response` | shadow-biased chroma/luma noise, denoising smear, scale-bounded grain | 전역 균일 grain overlay, skin plastic smoothing |
| `export_response` | 고대비 경계의 mild blocking/ringing/mosquito noise, detail survival | 거대한 pixelation, 얼굴 구조 파괴, delivery JPEG를 촬영 역사로 오인 |
| `fidelity_ceiling` | 얼굴·손·글자 없는 물체·재질 구조 보존, 과도한 sharpening 금지 | 가짜 저화질이 구조를 없애는 경우 |

### 후보 묶음 A: front-camera low-light social/video-call — advisory only

`observable components`

- arm-length 또는 그에 준하는 근거리 front-camera 원근
- 화면/한 개의 실내 practical이 소유하는 낮은 조도와 방향성
- 그림자 쪽에 국소화된 색/휘도 노이즈 또는 denoising softness
- 중심 초점은 남고 가장자리나 머리카락에 제한된 focus/edge softness
- 고대비 경계에만 가벼운 재압축 흔적, 얼굴 구조 보존

`confusion negatives`

- clean studio beauty portrait
- phone label만 붙은 third-person portrait
- uniform film-grain overlay
- global blur 또는 beauty-filter smoothing
- 과도한 pixelation과 읽을 수 없는 얼굴

`status boundary`

- 프롬프트 4건, 픽셀 8장 전수 보충에서 geometry는 대체로 보였지만 신호+출력 묶음은 완전하게 보이지 않았다.
- 후보팩/BM25F advisory로만 제안한다. hard exact profile은 `revise` 대상이다.

### 후보 묶음 B: compact direct-flash social snapshot — 기존 계약 재사용

- `early_2000s_compact_digicam_social_repost`와 `direct_on_camera_flash_snapshot_signature`를 그대로 소유자로 사용한다.
- 새 프로필을 만들지 않는다.
- 새 후보팩은 기존 프로필 ID를 참조하고 `compact_digital_camera`, `digicam_2000s_camera`, `compact_ccd_digicam`, `ccd_chroma_noise`, `jpeg_social`을 구성 후보로 연결한다.
- 정확한 장비/연도/계정/업로드 이력은 주장하지 않는다.

### 후보 묶음 C: film response without stock claim — advisory composition

`observable components`

- 톤별 규모가 보이는 restrained grain
- 작은 highlight core와 주변 밝은 단계가 남는 점진적 rolloff
- 실제 고휘도 경계에만 국소화된 halation, 필요한 경우에만 사용
- muted/saturated 등 현재 소스가 지지하는 color separation
- 피사체·재질을 파괴하지 않는 detail ceiling

`confusion negatives`

- 브랜드/필름-stock 이름만 있는 깨끗한 디지털 사진
- 전역 glow 또는 bloom
- 균일한 모노크롬 노이즈 overlay
- dust/scratch가 장면 전체에 붙는 가짜 archive texture
- underexposure를 rolloff로 오인

`claim boundary`

- `Kodak`, `Fuji`, `CineStill` 등은 사용자 입력 라벨 또는 버전된 에뮬레이션 별칭으로 보존할 수 있지만, 픽셀에서 실제 stock이나 현상 공정을 증명했다고 쓰지 않는다.

### 후보 묶음 D: clean digital editorial response

`observable components`

- focal-plane microtexture와 재질 경계 보존
- 작은 specular core 주위의 점진적 highlight shoulder
- 자연스러운 색 분리와 shadow detail
- 제한된 sharpening; halo와 crunchy pore 없음
- fake grain/JPEG/halation을 자동 추가하지 않음

`confusion negatives`

- waxy skin, 뷰티 필터, 전역 noise removal smear
- 과도한 local contrast/HDR halo
- RAW/8K/DSLR 라벨만 추가
- clean을 shadowless flat studio wash로 대체

## 후보팩/데이터 제안

### P0. 후보 수준의 메타데이터-효과 분리 필드

대상: 새 버전의 `assets/photo_prompt_capture_response_extension.json` 또는 동등한 authored source. 생성 인덱스에 직접 편집하지 않는다.

```json
{
  "id": "cap_front_camera_lowlight_response",
  "status": "advisory",
  "label_provenance": "versioned_vocab_or_user_input",
  "input_metadata_labels": ["front-facing phone camera", "video-call frame"],
  "observable_axes": [
    "arm-length near-field geometry",
    "source-owned low-light exposure",
    "shadow-biased chroma/luma noise or bounded denoising softness",
    "limited edge softness with focal detail retained",
    "mild recompression localized to high-contrast edges"
  ],
  "confusion_negatives": [
    "clean studio beauty portrait",
    "uniform film-grain overlay",
    "global blur",
    "destructive pixelation"
  ],
  "owners": {
    "geometry": "camera/composition",
    "light": "lighting",
    "signal": "grain_profile",
    "export": "texture",
    "ceiling": "quality_layers"
  },
  "claim_boundary": "appearance only; no exact device, sensor, app, upload, or recording-history claim",
  "activation": "advisory unless every required observable component has prompt evidence"
}
```

필수 필드는 `label_provenance`, `input_metadata_labels`, `observable_axes`, `confusion_negatives`, `owners`, `claim_boundary`, `activation`이다. 이 필드들이 없으면 장비명이 effect candidate로 잘못 승격되기 쉽다.

### P0. `quality_layers`의 조건부 `capture_response` 차원

대상: `assets/photo_prompt_quality_layers.json`의 `photographic_craft.dimensions`.

```json
{
  "id": "capture_response",
  "label": "capture and output response coherence",
  "activation": "only when an explicit capture modality or processing response is P0/P1 material",
  "baseline_principle": "Let a selected capture modality alter geometry, exposure, focus, signal, tone, or export behavior through observable evidence; a device or stock label alone does not count.",
  "owned_effects": ["signal_response", "tone_response", "export_response", "fidelity_ceiling"],
  "referenced_effects": ["capture_geometry", "light_provenance"],
  "prompt_budget": {"max_primary_clause": 1, "max_support_clauses": 2},
  "audit_terms": ["capture response", "signal response", "output response", "detail ceiling"]
}
```

- `capture_response`는 geometry와 light를 복제하지 않고 그 슬롯의 선택과 signal/tone/export가 모순되지 않는지만 검사한다.
- 현재 `prompt_dimension_limit: 2`를 존중한다. 매체가 소재적으로 중요하지 않으면 이 차원을 선택하지 않는다.
- 명시적 device label이 없다는 이유로 일반 사진에 인위적 grain/noise를 기본 추가하지 않는다.

### P1. 기존 후보의 효과 문구 보강

다음은 ID를 바꾸지 않고 authored source에서 `en` 또는 새 structured fields를 보강하는 제안이다.

| 기존 ID | 현재 문제 | 제안 효과 문구/필드 |
|---|---|---|
| `jpeg_social` | `subtle ... feel`로 너무 추상적 | `mild block and mosquito-noise traces localized around high-contrast edges while face, hand, and material detail survive` |
| `smartphone_night_noise` | 필름 그레인과 경계 없음 | `shadow-biased chroma/luma noise with bounded denoising softness; highlights and focal-plane features remain clean` |
| `ccd_chroma_noise` | CCD label이 원인처럼 보임 | `fine colored noise and restrained purple fringing concentrated in dark regions and bright contrast edges; appearance only` |
| `phone_realism` | 품질 추상어 | `near-field phone geometry and restrained computational response without beauty-filter smoothing or artificial HDR halos` |
| `consumer_camera_authenticity` | 장비 감성어 | `capture relation remains plausible through distance, flash/ambient response, focus behavior, and a bounded fidelity ceiling` |
| `clean_digital` | clean이 plastic과 혼동 | `clean digital response with focal microtexture, controlled sharpening, natural tone separation, and no invented degradation` |

### P1. 브랜드 film-emulation 후보의 별칭 강등과 effect-axis 연결

기존 18개 `film_emulation` 항목을 삭제하거나 모두 같은 효과로 만들지 않는다. 대신 다음 additive metadata를 붙이는 방향을 제안한다.

```json
{
  "label_kind": "emulation_alias_not_capture_proof",
  "claim_boundary": "do not claim actual stock, camera, lab, or development process from pixels",
  "requires_effect_any": ["grain_profile", "highlight_rolloff", "color_grading"],
  "forbids_label_only_hard_activation": true
}
```

실제 효과 값은 stock 이름에서 자동 추론해 고정하지 말고, 현재 소스 관찰 또는 사용자 지정에서 별도로 선택한다. `film_halation_highlight_edge_relation`은 모든 film label의 기본값이 아니라 고휘도 경계 증거가 있는 경우에만 조합한다.

### P1. 전면 카메라 advisory bundle

신규 후보 ID를 최소화하고 기존 것을 조합한다.

- medium: `selfie_camera_photo`
- camera_type: `front_facing_phone`
- grain_profile: `smartphone_night_noise`
- texture: `jpeg_social`, 단 명시적 출력 효과가 중요할 때만
- quality: `phone_realism`, `no_hdr_natural_snapshot`, `fidelity_ceiling_natural_detail`
- geometry: camera/composition 주제에서 소유하는 arm-length/near-field 후보
- light: 화면광/실내 practical의 source ownership 후보

이 묶음은 BM25F/embedding 후보로만 사용한다. `front camera` 단독으로 noise, compression, beauty smoothing을 자동 부여하지 않는다.

### P2. compact-digicam 중복 방지

- `early_2000s_compact_digicam_social_repost`가 hard active이면 동일 의미의 새 프로필이나 `direct_flash_y2k_snapshot` 전체를 중복 문구로 다시 쓰지 않는다.
- 한 프로필이 hard contract를 소유하고, 후보팩은 그 프로필의 component IDs를 채우는 방식으로 합성한다.
- hard exact activation은 모든 구성요소가 같은 프레임에서 확인돼야 하며 `partial_is_fail`이다.

## 썸네일/native 게이트

### front-camera low-light advisory 평가 게이트

| 스케일 | 게이트 |
|---|---|
| thumbnail | 근거리 front-camera 거리와 얼굴 중심의 원근이 먼저 읽힌다. 일반 망원/스튜디오 portrait가 아니다. |
| thumbnail | 낮은 조도가 한두 식별 가능한 광원에 의해 설명되고, 장면 전체가 임의로 파랗거나 어둡기만 하지 않다. |
| both | 중심 피사체는 읽히고 가장자리/머리카락의 softness나 focus miss는 제한적이다. |
| native | noise는 주로 어두운 영역에서 보이며 균일한 film-grain overlay가 아니다. denoising이 얼굴 구조를 지우지 않는다. |
| native | 재압축이 요청된 경우 고대비 경계에 약하게 국소화되고 얼굴·손·재질 디테일이 생존한다. |
| hard negative | beauty-filter smoothing, clean studio key, global blur, destructive pixelation은 대체하지 못한다. |

### film-response advisory 평가 게이트

| 스케일 | 게이트 |
|---|---|
| thumbnail | 색·톤 조직이 clean digital 대조와 구별되지만 브랜드/stock 이름 없이도 설명 가능하다. |
| both | near-white anchor가 점진적 숄더를 가지며 midtone과 색 분리가 남는다. |
| native | grain이 크기와 톤에 따라 보이고, 얼굴/손/재질을 가리는 균일 overlay가 아니다. |
| native | halation이 선택된 경우 실제 고휘도 경계에 얇게 국소화되고 global bloom이 아니다. |
| hard negative | stock 라벨, sepia/LUT, global glow, dust overlay만으로는 통과하지 못한다. |

### clean-digital 평가 게이트

| 스케일 | 게이트 |
|---|---|
| thumbnail | 주 피사체와 톤 계층이 깨끗하게 읽히되 HDR halo나 shadowless flatness가 없다. |
| both | focal-plane microtexture, hair/material edge, natural tonal separation이 함께 남는다. |
| native | sharpening halo, crunchy pores, waxy smoothing, invented grain/JPEG artifact가 없다. |
| hard negative | `RAW`, `8K`, `DSLR` 라벨만으로는 통과하지 못한다. |

## 회귀 및 held-out 테스트

### 정적/프롬프트 레이어

1. **브랜드 라벨 단독 hard-negative**
   - 입력: `shot on iPhone 17 Pro RAW`만 있고 기하·빛·신호·출력 구성요소가 없음.
   - 기대: camera/film label은 advisory 후보일 수 있지만 noise/HDR/JPEG/film response hard duty는 생기지 않는다.
2. **동일 기하, 다른 응답 causal pair**
   - A: daylight arm-length phone selfie, clean exposure.
   - B: 같은 거리·포즈에서 low-light front-camera, shadow noise/denoise softness를 명시.
   - 기대: geometry는 공유하지만 B만 signal-response 후보를 얻는다.
3. **동일 응답, 다른 장비 라벨 causal pair**
   - 동일한 near-axis flash, falloff, mixed WB, JPEG component를 두고 장비 브랜드만 바꾼다.
   - 기대: hard visual contract는 변하지 않는다.
4. **compact flash vs studio strobe hard negative**
   - compact: near-axis, close shadow, rapid near/far drop, ambient survival.
   - studio: off-axis large source, controlled background, no rapid consumer-flash falloff.
   - 기대: `direct_on_camera_flash_snapshot_signature`는 compact arm만 통과한다.
5. **film label vs film-response causal pair**
   - A: `35mm film look`만 있음.
   - B: grain scale, highlight shoulder, color separation, localized halation을 명시.
   - 기대: A는 advisory, B만 구성요소별 후보/정확 프로필을 얻는다.
6. **JPEG 전달 혼동 hard negative**
   - 입력 프롬프트에는 압축 요청이 없으나 fixture 파일은 JPEG.
   - 기대: 파일 확장자/전달 MIME만으로 `jpeg_social` 시각 의무를 활성화하지 않는다.
7. **제품 스튜디오 held-out**
   - 2680과 같은 top-down 제품사진.
   - 기대: `studio` 때문에 consumer camera, phone noise, social JPEG가 붙지 않는다.
8. **기존 compact profile 비중복 검사**
   - hard profile 활성 시 direct-flash/CCD/JPEG 문구가 두 번 반복되지 않고 각 효과 owner가 하나인지 검사한다.

### 렌더 레이어 계획

- 이번 연구에서는 생성하지 않았고 모든 렌더 평가는 `UNSCORED`다.
- 추후 승인 시 각 causal pair를 동일 모델/버전/종횡비/설정으로 독립 생성한다.
- 프롬프트 bytes를 arm별로 고정하고 가능하면 반복 생성해 샘플링 분산을 분리한다.
- exact hard profile은 같은 한 장에서 모든 gate를 통과해야 한다. 일부만 보이면 실패다.
- package/route PASS, prompt PASS, delivered image, pixel PASS, 사용자 선호는 각각 별도 기록한다.

## 외부 1차 자료가 정하는 경계

- [Adobe DNG 설명](https://helpx.adobe.com/camera-raw/desktop/dng-and-file-formats/digital-negative.html)은 DNG를 카메라 raw 정보를 저장하는 공개 파일 형식으로 설명한다. 따라서 `RAW/DNG`는 출력 픽셀의 고정 스타일 이름으로 취급하면 안 된다.
- [Apple ProRAW 공식 안내](https://support.apple.com/guide/iphone/take-apple-proraw-photos-iphae1e882a3/ios)는 ProRAW가 표준 RAW 정보와 iPhone image processing을 결합한다고 설명한다. `ProRAW`라는 입력 라벨 하나로 처리 없음, 특정 노이즈, 특정 톤을 가정할 수 없다.
- [ITU-T T.81 공식 레코드](https://www.itu.int/ITU-T/recommendations/rec.aspx?id=2633)와 [ITU의 JPEG 계열 설명](https://www.itu.int/rec/dologin_pub.asp?id=T-REC-T.Sup2-201103-I%21%21PDF-E&lang=f&type=items)은 baseline JPEG의 블록 기반 주파수 부호화 경계를 제공한다. 후보 gate는 막연한 `low quality`가 아니라 고대비 경계의 블록/링잉/모기 노이즈처럼 국소적이고 검증 가능한 결과를 보되, 수집본 자체의 JPEG 전달 인코딩과 생성 의도를 분리해야 한다.

## 한계와 bounded decision

- 픽셀 표본은 25개 게시물 50장으로, 전체 4,908장의 빈도 표본이 아니다.
- 생성 모델/버전, seed, 참조 이미지 처리, 시도 정책, 원본 raw 파일, 중간 처리 단계가 없다.
- 대부분의 수집 파일이 JPEG라 의도된 압축과 전달 재인코딩을 귀속할 수 없다.
- native 중앙 crop 8개는 화면 전체의 모든 미세 아티팩트 부재를 증명하지 않는다.
- 전면 카메라 명시 프롬프트는 4개뿐이며, 완전한 저조도 신호+압축 서명은 8개 이미지에서 안정적으로 확인되지 않았다.
- 외부 자료는 포맷/코덱 경계만 보강하며 코퍼스 픽셀의 생성 원인을 증명하지 않는다.
- 구현, 인덱스 재생성, package validation, 새 렌더, 사용자 미감 평가는 수행하지 않았다.

**결정: `proposed`.** 기존 compact-digicam/flash/rolloff/halation hard contract는 재사용하고, 브랜드·RAW 라벨과 보이는 캡처 응답을 분리하는 candidate metadata 및 조건부 `capture_response` quality dimension을 설계안으로 남긴다. 전면 카메라 저조도는 advisory candidate로만 두며 hard profile 승격은 `revise`다.

## 증거 부록

### 픽셀 표본 경로

- 1759: `generated/reactorprompt-export-20260902-incremental/images/1759_DZNH9JAmtJg_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1759_DZNH9JAmtJg_02.jpg`
- 1760: `generated/reactorprompt-export-20260902-incremental/images/1760_DZNLzElGvCm_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1760_DZNLzElGvCm_02.jpg`
- 1842: `generated/reactorprompt-export-20260902-incremental/images/1842_DZkWUaHGoJl_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1842_DZkWUaHGoJl_02.jpg`
- 1843: `generated/reactorprompt-export-20260902-incremental/images/1843_DZkV504mmU3_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1843_DZkV504mmU3_02.jpg`
- 1865: `generated/reactorprompt-export-20260902-incremental/images/1865_DZosKKPmmrr_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1865_DZosKKPmmrr_02.jpg`
- 1867: `generated/reactorprompt-export-20260902-incremental/images/1867_DZowdMAGuPP_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1867_DZowdMAGuPP_02.jpg`
- 1881: `generated/reactorprompt-export-20260902-incremental/images/1881_DZpiWEIGr_p_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1881_DZpiWEIGr_p_02.jpg`
- 1882: `generated/reactorprompt-export-20260902-incremental/images/1882_DZphcF4Gtyo_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/1882_DZphcF4Gtyo_02.jpg`
- 2102: `generated/reactorprompt-export-20260902-incremental/images/2102_DaffrQFGkl8_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2102_DaffrQFGkl8_02.jpg`
- 2156: `generated/reactorprompt-export-20260902-incremental/images/2156_DauKEHwGuTP_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2156_DauKEHwGuTP_02.jpg`
- 2275: `generated/reactorprompt-export-20260902-incremental/images/2275_DbIzUoLGqYm_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2275_DbIzUoLGqYm_02.jpg`
- 2278: `generated/reactorprompt-export-20260902-incremental/images/2278_DbIoSO9GmS7_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2278_DbIoSO9GmS7_02.jpg`
- 2324: `generated/reactorprompt-export-20260902-incremental/images/2324_DbicWHzGt-W_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2324_DbicWHzGt-W_02.jpg`
- 2325: `generated/reactorprompt-export-20260902-incremental/images/2325_DbiZ-JXGi_d_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2325_DbiZ-JXGi_d_02.jpg`
- 2326: `generated/reactorprompt-export-20260902-incremental/images/2326_DbiZ4y3GrIt_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2326_DbiZ4y3GrIt_02.jpg`
- 2380: `generated/reactorprompt-export-20260902-incremental/images/2380_Dbu6_h3GgF1_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2380_Dbu6_h3GgF1_02.jpg`
- 2381: `generated/reactorprompt-export-20260902-incremental/images/2381_Dbu6ebimvHy_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2381_Dbu6ebimvHy_02.jpg`
- 2535: `generated/reactorprompt-export-20260902-incremental/images/2535_DcLtoPzGjB__01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2535_DcLtoPzGjB__02.jpg`
- 2679: `generated/reactorprompt-export-20260902-incremental/images/2679_Dcn2zoVGhoi_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2679_Dcn2zoVGhoi_02.jpg`
- 2680: `generated/reactorprompt-export-20260902-incremental/images/2680_Dcn2LesmjBy_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2680_Dcn2LesmjBy_02.jpg`
- 2712: `generated/reactorprompt-export-20260902-incremental/images/2712_Dcp6M_6GtUa_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2712_Dcp6M_6GtUa_02.jpg`
- 2713: `generated/reactorprompt-export-20260902-incremental/images/2713_Dcp5gv6mhQq_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2713_Dcp5gv6mhQq_02.jpg`
- 2728: `generated/reactorprompt-export-20260902-incremental/images/2728_DcslulLmoIw_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2728_DcslulLmoIw_02.jpg`
- 2741: `generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_02.jpg`
- 2742: `generated/reactorprompt-export-20260902-incremental/images/2742_Dcx0CYwmkWj_01.jpg`, `generated/reactorprompt-export-20260902-incremental/images/2742_Dcx0CYwmkWj_02.jpg`

### 핵심 명령과 휴리스틱

```bash
# 분모
jq '[.[] | select(.prompt_missing == false and ((.prompt // "")|length>0))] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

# 파일 전달 포맷 분포
jq -r '.[].images[].local_file' generated/reactorprompt-export-20260902-incremental/manifest.json \
  | awk -F. '{print tolower($NF)}' | sort | uniq -c | sort -nr

# 기존 hard profile/slot 조사
rg -n 'early_2000s_compact_digicam_social_repost|direct_on_camera_flash_snapshot_signature|film_halation_highlight_edge_relation|highlight_rolloff_tone_response|smartphone_night_noise|jpeg_social' \
  skills/photo-prompt-image-generator/assets
```

전수 집계는 Python `re.search(..., re.I)`로 924개 본문을 순회했고, 표의 각 행에 적힌 표현군을 단어 경계 정규식으로 사용했다. 구성요소 완성도는 다음 묶음의 교집합으로 계산했다.

- phone: 장치 라벨 ∩ (`arm's-length|extended camera arm|front camera|high handheld|24–28mm`) ∩ (`sensor/chroma noise|compression|JPEG|HDR|focus miss|edge blur`)
- compact: compact/CCD 라벨 ∩ direct/on-camera flash ∩ (`noise|fringing|JPEG|compression`) ∩ (`clipped highlight|overexposure|limited dynamic range|mixed WB|rapid falloff|background shadow`)
- film: film-emulation 라벨 ∩ grain ∩ (`halation|highlight rolloff|bloom|protected/clipped highlight`) ∩ (`color separation|film color|color grading|palette response`)

### 임시 검토 산출물

다음 contact sheet와 native crop은 `/tmp`에서만 생성해 검토했고 저장소 산출물로 보존하지 않았다.

- `/tmp/capture-medium-sheet-1.jpg` … `/tmp/capture-medium-sheet-6.jpg`
- `/tmp/capture-medium-front-camera-all.jpg`
- `/tmp/capture-medium-native-centers.jpg`

이 보고서 외 런타임 asset, generated index, test, target skill 파일은 수정하지 않았다.

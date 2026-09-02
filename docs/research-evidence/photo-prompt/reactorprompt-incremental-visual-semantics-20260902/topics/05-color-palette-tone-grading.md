# 05. 색채 팔레트·화이트밸런스·톤 대비·그레이딩·색 분리

상태: `proposed`
모드: 리서치/설계 전용. 런타임 자산, 생성 인덱스, 테스트, 스킬 파일은 수정하지 않았다.

## Scope and sampling method

### 증거 경계

- 동결 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, ID 1565–2746.
- 프롬프트 텍스트 집계, 코퍼스 픽셀 관찰, 현재 저장소 자산 검사, 외부 색채 용어 자료를 서로 다른 증거 층으로 유지했다.
- 이 보고서는 코퍼스의 생성 모델, 시드, 참조 이미지 입력, 후처리 파이프라인을 알지 못한다. 따라서 프롬프트와 이미지가 함께 존재해도 특정 문구가 픽셀의 원인이라고 단정하지 않는다.
- 사람에 관한 픽셀 관찰은 화면에 보이는 성인 표현, 메이크업·의상·표면색·빛의 관계로 제한했다. 정체성, 동일인 여부, 보호 특성, 건강, 매력, 실제 직업이나 국적을 추론하지 않았다.

### 전체 프롬프트 스캔

924개 비어 있지 않은 프롬프트 전부를 대소문자 무시 한·영 정규식으로 게시물 단위 집계했다. 한 게시물이 여러 범주에 동시에 들어갈 수 있으며, 집계는 의미 판정이 아니라 보수적인 문자열 휴리스틱이다.

분리한 범주는 다음과 같다.

1. 명시적 색 이름 또는 표면색
2. 팔레트·배색·흑백/단색 체계
3. 화이트밸런스·색온도·전역 캐스트
4. 채도·저채도·고채도·파스텔/뮤트
5. 톤 대비·블랙 플로어·중간톤·하이라이트 롤오프
6. 컬러 그레이딩·필름 색감·후처리
7. 색 분리·보색·포인트 색·웜–쿨 관계
8. 색 조명·스필·바운스·네온/스크린 글로
9. 전역 색 워시를 막는 명시적 보존 가드

### 픽셀 표본

ID 구간을 초기(1565–1958), 중기(1959–2352), 후기(2353–2746)로 나누고 각 구간에서 색채 메커니즘을 2개 이상 명시한 게시물 2개를 골랐다. 각 양성 게시물에는 색 이름은 있을 수 있지만 위 메커니즘을 명시하지 않은 근접 게시물 1개를 대조군으로 붙였다. 각 게시물의 첫 2장을 보아 총 **12개 게시물·24장**을 검사했다.

- 썸네일 검사: 24장 모두, 3개의 4×2 접촉시트에서 첫 인상·팔레트 역할·전역 워시·색 분리를 관찰했다.
- 네이티브 검사: 12개 게시물의 첫 번째 이미지를 원본 크기로 열어 경계, 잔존 색, 하이라이트 질감, 암부 분리, 국소 캐스트를 재확인했다.
- 이 표본의 빈도는 4,908장 전체의 빈도로 일반화하지 않는다.

| 구간 | 양성 게시물 | 근접 대조군 | 선택 이유 |
|---|---:|---:|---|
| 초기 | 1883 | 1882 | 전역 흑백과 동일 표면의 국소 컬러 예외 대 색 이름 중심의 복숭아 계열 장면 |
| 초기 | 1916 | 1917 | 저채도·쿨–웜 균형 명시 대 물체 고유색 중심의 자연광 장면 |
| 중기 | 2132 | 2136 | 단일 블루 포인트·저채도·그레이드 대 일반적인 웜 스튜디오 색 |
| 중기 | 2299 | 2298 | 올리브 회색 캐스트·리프트 블랙·저대비 대 자연광의 크림/목재 고유색 |
| 후기 | 2467 | 2479 | 청록 그림자·따뜻한 피부 하이라이트·필름 톤 대 화면/의상 자체의 강한 색 |
| 후기 | 2741 | 2734 | 시안 배경·적색 의상·제한된 시안 바운스 대 중성 사무실의 파란 표면색 |

## Prompt-side findings and counts

아래 수치는 프롬프트 문자열 매치이며 픽셀 성공률이 아니다.

| 휴리스틱 범주 | 매치 게시물 | 그 게시물의 이미지 수 | 해석 경계 |
|---|---:|---:|---|
| 명시적 색 이름/표면색 | 900 | 3,723 | 머리·의상·배경 색도 포함하므로 팔레트 설계 증거가 아님 |
| 팔레트·배색·흑백/단색 | 168 | 665 | 색 목록만 있고 면적·역할·소유자가 없는 경우도 포함 |
| 화이트밸런스·색온도·캐스트 | 38 | 159 | 프롬프트 주장일 뿐 중성 기준면이나 광원 증거를 보장하지 않음 |
| 채도 분포 | 108 | 456 | 전역 채도인지 특정 물체/색만의 채도인지 추가 판별 필요 |
| 톤 대비·블랙·중간톤·하이라이트 | 141 | 602 | 밝기 분포, 노출, 톤 매핑, 조명 대비가 혼재 |
| 그레이딩·필름색·후처리 | 96 | 392 | 촬영광이나 표면색을 그레이드가 대신했는지 알 수 없음 |
| 색 분리·포인트색·웜–쿨 관계 | 10 | 42 | 관계형 명시가 매우 적음 |
| 색 조명·스필·바운스 | 22 | 78 | 색 배경이나 색 물체와 혼동 가능 |
| 전역 워시 방지 가드 | 3 | 12 | 국소 색 조명 아래 재질/피부 표면 보존을 직접 말한 사례가 드묾 |
| 위 메커니즘 중 하나 이상 | 390 | 1,616 | 범주 합은 중복 때문에 390보다 큼 |

주요 동시 매치는 `palette+grade` 17개, `palette+saturation` 35개, `palette+colored_light` 18개, `saturation+tone` 36개였다. 반면 `white_balance+grade`는 3개, `white_balance+color_separation`은 2개, `colored_light+wash_guard`는 2개뿐이었다. 이 차이는 색 이름과 스타일 룩은 풍부하지만, **색의 원인·공간 범위·보존 대상·혼동 경계**가 드물다는 뜻이다. 빈도가 낮다는 이유만으로 새 전역 기본값을 만들 수는 없지만 관계형 후보의 결손을 찾는 단서는 된다.

프롬프트에서 반복된 구조는 다음과 같다.

- `PALETTE ANCHOR`나 색 목록은 늘었지만, dominant/support/accent/neutral 역할이나 화면 점유·시선 우선순위를 항상 말하지는 않는다.
- `low saturation`, `lifted blacks`, `highlight roll-off`, `cinematic color grading`은 자주 함께 쓰여 서로 다른 톤 축을 한 스타일 묶음으로 압축한다.
- `neon-blue top`처럼 “neon”이 표면색 강도인지 발광 광원인지 모호한 문구가 있다.
- `cool-warm balance`나 `olive-grey cast`는 중성 기준면, 광원 위치, 동일 재질의 교차 조명 반응이 없으면 픽셀에서 검증하기 어렵다.
- `skin stays natural`, `never blue or painted`처럼 국소 색 바운스와 표시 표면색을 분리하는 가드는 3개 매치에 그쳤다.

## Pixel-side observations and sample IDs

아래는 **24장 표본에 한정한** 관찰이다. 각 행의 두 이미지 모두 썸네일로 보았고, 첫 번째 이미지는 네이티브로 재검사했다.

| ID | 역할 | 이미지 | 픽셀 관찰 |
|---:|---|---|---|
| 1883 | 양성 | `1883_DZpgpC_GigD_01.jpg`, `_02.jpg` | 두 장 모두 전역 흑백이 첫눈에 읽히고 가슴 선택 사각형 안의 같은 레이스/직물 표면만 다색으로 남는다. 네이티브에서 선택 핸들과 커서, 동일 무늬 연속성이 보여 “색 물체를 얹은 것”보다 국소 예외 관계가 강하다. |
| 1882 | 대조 | `1882_DZphcF4Gtyo_01.jpg`, `_02.jpg` | 복숭아·분홍 의상/메이크업/소품과 녹색 야외가 밝은 장면을 만든다. 전역 고노출과 하이라이트 소실이 팔레트 인상을 크게 좌우하지만 색 역할이나 그레이드 소유자는 명시적으로 분리되지 않는다. |
| 1916 | 양성 | `1916_DZxUzQkGuSZ_01.jpg`, `_02.jpg` | 저채도 dusty rose, 회갈색 배경, 어두운 머리는 일관된다. 그러나 썸네일에서 쿨–웜의 공간 분리나 중성 기준면은 약하다. `cool-warm balance`라는 문구가 관계형 픽셀 증거로 자동 승격될 수 없는 반례다. |
| 1917 | 대조 | `1917_DZxUAYkmuwx_01.jpg`, `_02.jpg` | 네이비·화이트 의상, 검은 좌석, 창밖 녹색이 자연광 아래 각 표면에 머문다. 전역 캐스트나 그레이드보다 물체 고유색과 밝기 차가 색 구성을 만든다. |
| 2132 | 양성 | `2132_Dap5qCGGiCZ_01.jpg`, `_02.jpg` | 파란 상의가 검은 배경과 저채도 피부/머리 사이의 단일 고채도 포인트로 즉시 읽힌다. 파란색이 피부나 배경으로 번지지 않아 이는 색 조명이 아니라 **표면색 포인트**다. `neon-blue`를 발광으로 해석하면 오분류된다. |
| 2136 | 대조 | `2136_DaqCRnTmi9i_01.jpg`, `_02.jpg` | 아이보리 새틴, 따뜻한 베이지 배경, 분홍 메이크업, 따뜻한 림이 조화롭지만 단일 포인트색이나 전역 그레이드 관계는 없다. 표면색과 따뜻한 광원이 함께 작동한다. |
| 2299 | 양성 | `2299_DbcuYZ-GmbV_01.jpg`, `_02.jpg` | 녹색 식물, 회색 스웨터, 유리·금속, 따뜻한 피부가 저·중대비로 분리되고 어두운 벤치의 블랙이 완전히 닫히지 않는다. 다만 `olive-grey cast`는 온실의 실제 녹색 표면과 채광에 의해 혼동되며, 중성 기준면 없이 전역 캐스트라고 확정할 수 없다. |
| 2298 | 대조 | `2298_Dbcq_-4mgy5_01.jpg`, `_02.jpg` | 크림색 의상/벽, 목재, 갈색 머리, 크루아상 색이 중성에 가까운 창광 아래 분리된다. 별도 그레이드 명칭 없이도 고유색·재질·빛의 조합이 안정적인 팔레트를 만든다. |
| 2467 | 양성 | `2467_DcAfXXLmuHQ_01.jpg`, `_02.jpg` | 청록 커튼/실내 그림자와 눈 위의 좁은 따뜻한 직사광 띠가 공간적으로 분리된다. 색 경계가 가림과 광선 띠를 따르며, 밝은 띠 안 피부 표면은 자연스러운 따뜻한 색을 유지한다. 네이티브에서 일부 강한 하이라이트가 있어도 눈·피부 질감과 차가운 암부가 함께 남는다. |
| 2479 | 대조 | `2479_DcAS04HGl0j_01.jpg`, `_02.jpg` | 분홍 광고 화면·상의와 초록 그래픽이 강한 색 읽기를 만들지만, 역사의 타일·천장 조명·바닥은 비교적 중성이다. 색은 화면 콘텐츠와 의상에 귀속되며 전역 핑크 그레이드가 아니다. |
| 2741 | 양성 | `2741_Dcx0xZ8mlev_01.jpg`, `_02.jpg` | 시안 배경, 적색 재킷, 아이보리 칼라, 따뜻한 피부/메이크업이 썸네일에서도 분명히 분리된다. 시안 바운스는 제한적이고 피부를 전역 파랑으로 만들지 않는다. 네이티브에서 의상 직물·주근깨·하이라이트 계조가 유지되어 팔레트와 표면 보존이 동시에 읽힌다. |
| 2734 | 대조 | `2734_DcslSCWml7h_01.jpg`, `_02.jpg` | 파란 스크럽과 장갑이 중성 사무실, 검은 머리, 표시 표면 피부와 분리된다. 파란색은 의상/소품의 고유색이며 화면 전체 화이트밸런스나 캐스트로 번지지 않는다. |

## Prompt/pixel alignment and divergences

### 정렬된 사례

- **1883:** “전체 흑백 + 특정 동일 표면만 컬러”가 두 이미지에서 첫눈에 읽힌다. 단순 색 이름보다 영역 소유권과 동일 표면 연속성이 강한 제어다.
- **2132:** 저채도 장면의 한 개 포인트 표면색이 유지된다. 같은 “blue”라도 조명 슬롯이 아니라 `color`의 표면색 소유자여야 한다.
- **2467:** 청록 그림자와 따뜻한 직사광의 경계가 광원/가림 경계를 따른다. 이는 전역 teal-orange 그레이드와 구별된다.
- **2741:** 배경 시안, 의상 적색, 중성/따뜻한 표시 표면이 동시에 유지된다. `cyan bounce`는 국소 유도 효과이고, 시안 배경색 자체나 전역 캐스트가 아니다.

### 불완전하거나 혼동된 사례

- **1916:** 프롬프트의 `cool-warm balance`는 픽셀에서 공간 관계로 약하다. 레이블만 있고 어느 면이 어떤 광원/색을 소유하는지 없기 때문이다.
- **2299:** `olive-grey cast`는 온실 식물과 회색 구조물의 고유색, 유리 채광, 필름 룩이 서로 혼동된다. 중성 기준면이나 동일 재질의 비교가 없으므로 캐스트 주장은 불확실하다.
- **1882:** 높은 밝기와 광범위한 하이라이트 소실이 “airy peach” 인상을 강화한다. 팔레트 후보가 노출·톤 응답을 소유하면 이 장면의 색 원인을 잘못 설명하게 된다.
- **2479:** 화면 자체의 분홍 콘텐츠는 지역적으로 강하지만 전체 장면은 중성이다. “프레임에 분홍이 많다”는 관찰만으로 핑크 전역 그레이드를 선택하면 오작동한다.

핵심 결론은 다음과 같다.

```text
표면 고유색 != 색 조명/바운스 != 화이트밸런스/전역 캐스트
               != 노출/톤 응답 != 전역/지역 그레이드
```

한 축의 성공이 다른 축의 증거를 대신하지 않는다.

## Existing-data overlap and ownership

### 현재 자산의 강점

- `photo_prompt_visual_obligations.json`에는 이미 다음과 같은 강한 관계형 프로필이 있다.
  - `mixed_illuminant_white_balance_relation`: 두 광원 정체성, 공간 분리, 중성 기준면, 같은 재질의 일관성, 그레이드 대체 금지.
  - `highlight_rolloff_tone_response`: near-white 기준, 점진적 숄더, 작은 클립 중심, 밝은 질감/색상 보존, flat/HDR 대체 금지.
  - `high_key_tonal_distribution`, `low_key_selective_illumination`, `film_halation_highlight_edge_relation` 등 톤/광원 관련 프로필.
- `photo_prompt_lighting_extension.json`은 12개 조명 클러스터를 `lighting`, `direction`, `source type`, `intensity`, `shape`, `color`, `color_grading`, `film_emulation`에 걸쳐 소스 소유형으로 묶는다. `motivated_warm_practical_cool_ambient`, `blue_hour_city_practical`, `filmic_muted_halation`은 색 조명과 전역 그레이드를 구분하려는 좋은 선례다.
- `photo_prompt_quality_layers.json`의 `colored_or_mixed_light`는 색 스필이 피사체·의상·소품·주변 표면에 같은 방향으로 이어져야 한다고 요구한다.

### 현재 자산의 빈틈과 중복

| 자산/층 | 현재 내용 | 문제 또는 빈틈 | 제안 소유자 |
|---|---|---|---|
| `photo_prompt_tags.json`의 `color` | 54개. 팔레트, 그레이드, 필름 캐스트, 색 조명, 패션 색을 한 슬롯에 포함 | `cool_blue color grade`, `blood-red accent light`, `warm Kodak Gold cast`처럼 서로 다른 원인이 같은 슬롯에 섞임 | 새 authored 색채 extension의 `color_effect_contract`로 원인 메타데이터 부여 |
| `color_grading` | 8개. 저채도 필름, 창광 앰버, 쿨 모닝, 그린 반사광, CCD 플래시 등 | 광원/환경 반사와 전역 그레이드가 혼재하고, black/midtone/highlight 축 분해가 약함 | 전역/지역 scope와 tone response를 명시한 그레이드 후보 |
| `film_emulation` | 18개 브랜드/포맷 룩 | 이름이 관찰 가능한 색·톤·입자·할레이션을 자동 보장하지 않음 | 브랜드 명칭은 advisory; 관찰 가능한 분해는 `color_grading`/`grain`/`halation` 각 소유자 |
| 조명 extension의 selective accent | `lit_editorial_neutral_selective_accent` | hard-side editorial 클러스터에 결합되어 일반적인 국소 색 예외가 아님 | 범용 selective-color 관계 프로필을 별도로 설계 |
| `neutral_base_single_lemon_accent` | 여름 패션용 한정 후보 | 한 색과 의상 맥락에 과적합 | dominant/support/accent/neutral 역할 관계로 일반화 |
| quality layer | `mood_palette`, `colored_or_mixed_light` | 색 정확도·팔레트 역할·전역 워시·색 분리 자체의 품질 게이트는 없음 | color-specific quality/visual-obligation 층 |
| 생성 `photo_prompt_visual_profile_index.json` | 검색용 파생물 | authored source가 아님 | 직접 편집 금지; source extension/registry에서 재생성 |

현재 `INTENT_LOCK_DIMENSIONS`에는 `color`가 이미 허용되어 있다. 따라서 `palette`나 `color_grade`를 새 최상위 intent dimension으로 추가하지 말고, 아래 하위 필드를 **`color` 내부의 원인·범위 표현**으로 유지해야 한다.

## Proposed semantic components and confusion boundaries

### 1. 공통 `color_effect_contract`

새 authored source(제안 파일명: `photo_prompt_color_extension.json`)의 후보와 visual profile이 공통으로 참조할 내부 계약을 제안한다. 이는 생성기에 그대로 출력할 수식어나 전역 기본값이 아니라, 누가 어떤 효과를 소유하는지 정하는 표현이다.

```json
{
  "color_effect_contract": {
    "effect_owner": "intrinsic_surface | illumination | capture_white_balance | global_grade | regional_grade | tone_response",
    "spatial_scope": "named_surface | source_owned_region | tone_band | masked_region | full_frame",
    "source_or_surface_anchor": [],
    "palette_roles": {
      "dominant": [],
      "supporting": [],
      "accent": [],
      "neutral_anchor": []
    },
    "saturation_distribution": {
      "global_level": "source_relative",
      "exceptions": []
    },
    "tone_response": {
      "black_floor": "source_relative",
      "shadow_detail": "source_relative",
      "midtone_placement": "source_relative",
      "highlight_shoulder": "source_relative",
      "clip_extent": "source_relative"
    },
    "preserve_relations": [],
    "reject_substitutes": [],
    "evidence_provenance": "requesting_user | current_source | versioned_vocabulary",
    "confidence": "high | medium | low"
  }
}
```

원칙:

- `intrinsic_surface`: 의상, 배경 벽, 제품, 식물처럼 물체/재질이 소유하는 색.
- `illumination`: 광원 방향·감쇠·가림을 따라 받는 면에 나타나는 색.
- `capture_white_balance`: 중성 또는 익숙한 기준면을 중심으로 한 캡처 해석. 색 물체나 배경 하나로 주장하지 않는다.
- `global_grade`: 전체 프레임에 적용되는 룩. 국소 광원 풀이나 그림자 방향을 만들 수 없다.
- `regional_grade`: 명시된 영역/톤 밴드/마스크 범위에만 적용되는 후처리. 실제 광원처럼 주장하지 않는다.
- `tone_response`: 밝기·계조 축. 색상 팔레트와 별도 소유한다.
- 사람의 표시 표면색 보존은 픽셀에서 보이는 표면의 자연스러운 재질·국소 변화만 뜻한다. 생물학적 피부색이나 정체성 주장이 아니다.

### 2. 좁은 exact hard profile 제안

#### `palette_role_hierarchy_relation`

Observable components:

1. 프레임 대부분을 차지하는 dominant 색군.
2. dominant를 연결하는 supporting 색군.
3. 개수와 면적이 제한된 accent 색군.
4. 화이트밸런스나 색 분리를 읽게 하는 neutral/familiar anchor.
5. 역할이 피사체·배경·소품·의상 중 어느 표면에 속하는지 명시.

Confusion negatives:

- 색 이름 나열만 있음.
- 모든 색이 같은 면적/채도로 경쟁함.
- accent가 전역 워시로 확장됨.
- 조명색을 물체 고유색으로 오인함.
- 단순히 화려하거나 다채로운 장면.

Activation:

- exact terms 또는 5개 component evidence가 모두 있을 때만 hard obligation.
- bare `palette`, 색상 목록, BM25F/embedding-only hit는 advisory.

#### `selective_color_same_surface_exception_relation`

Observable components:

1. base frame의 명확한 무채색/억제 채도 처리.
2. 하나의 제한된 예외 영역.
3. 예외가 원래 장면의 같은 표면·무늬·원근을 이어받음.
4. 예외 경계가 요청된 마스크/표면 경계를 따름.
5. 예외 밖 잔존 채도와 무관한 색 소품이 대체하지 않음.

Confusion negatives:

- 흑백 장면에 컬러 카드나 물체를 붙임.
- 예외 영역이 같은 표면과 연결되지 않음.
- 화면 전체에 약한 색이 남음.
- 단순 color splash, vignette, bloom, RGB glitch.

1883은 동기 사례로만 보존하고, 제품 라벨 영역·건축 유리 패널 같은 비인물 held-out가 추가되어야 한다.

#### `low_chroma_preserved_color_separation`

Observable components:

1. 전역 채도는 낮지만 2개 이상의 주요 재질 색군이 여전히 구분됨.
2. 인접 영역의 색 차 또는 명도/경계 보조가 유지됨.
3. 한정 accent가 있으면 채도 예외로 기록됨.
4. 암부와 중간톤이 회색 진흙처럼 합쳐지지 않음.
5. 표면 질감과 색이 함께 남음.

Confusion negatives:

- 전체 회색 워시.
- 저대비만 적용해 색 분리가 사라짐.
- 단일 고채도 물체가 장면 전체를 압도함.
- 블랙을 들어 올려 재질 경계가 사라짐.
- 색 분리 대신 과도한 sharpening/HDR edge 사용.

### 3. 기존 프로필을 재사용해야 하는 관계

- `mixed_illuminant_white_balance_relation`: 2467/2741 계열의 광원 분리에는 이 기존 프로필을 우선 재사용한다. 새 “warm-cool” 프로필을 중복 생성하지 않는다.
- `highlight_rolloff_tone_response`: 1882의 광범위한 밝은 영역, 2299의 유리, 2741의 얼굴/직물 하이라이트 검증에 재사용한다.
- `high_key_tonal_distribution`/`low_key_selective_illumination`: 밝은 팔레트나 어두운 팔레트 이름이 노출 분포를 대신하지 못하게 한다.
- `film_halation_highlight_edge_relation`: 필름 룩 이름과 국소 밝은 경계의 할레이션을 분리한다.

## Candidate-pack/data proposals with exact suggested fields or layer

### 제안 1: 새 authored color extension

제안 파일: `skills/photo-prompt-image-generator/assets/photo_prompt_color_extension.json`

- 형식은 기존 `photo-prompt-research-extension/v1` 패턴을 따른다.
- broad advisory candidates는 `slots.color`, `slots.color_grading`에 둔다.
- exact visual semantics는 `visual_semantics`와 visual-obligation registry에 연결한다.
- `photo_prompt_visual_profile_index.json`과 semantic index는 결과물일 뿐 직접 편집하지 않는다.

각 후보에 아래 메타데이터를 제안한다.

| 필드 | 의미 | 예시 |
|---|---|---|
| `effect_owner` | 색 효과의 단일 원인 소유자 | `intrinsic_surface`, `illumination`, `global_grade` |
| `spatial_scope` | 효과가 적용되는 범위 | `named_surface`, `source_owned_region`, `full_frame` |
| `source_or_surface_anchor` | 광원·받는 면·재질 기준 | `cyan wall bounce -> shadow-side cheek edge` |
| `palette_roles` | dominant/support/accent/neutral | 색 이름이 아니라 역할 배열 |
| `saturation_distribution` | 전역 채도와 예외 | `muted_global + saturated_blue_garment_exception` |
| `tone_response` | black/shadow/midtone/highlight/clip | `lifted_black`, `midtones_open`, `small_clip_core` |
| `preserve_relations` | 다른 축에서 유지할 것 | 재질 정체성, 중성 기준면, 표시 표면의 국소 색 변화 |
| `reject_substitutes` | 흔한 오대체 | `global_cyan_wash`, `colored_prop_only`, `teal_orange_lut_only` |

### 제안 2: 기존 후보의 재분류

- `cool_blue color grade`, `desaturated_cold_blue grade`, `warm Kodak Gold cast`는 `effect_owner=global_grade`로 이동/표시한다.
- `blood-red accent light`, `neon_magenta_cyan` 중 실제 빛 후보는 `effect_owner=illumination`으로 표시하고 광원·받는 면을 요구한다.
- `butter_yellow_palette`, `powder_blue_palette`, `neutral_base_single_lemon_accent` 같은 표면 중심 후보는 `effect_owner=intrinsic_surface`와 역할 관계를 가진다.
- `film_emulation` 브랜드 이름은 advisory를 유지한다. hard evidence에는 관찰 가능한 `color_grading`, `grain_profile`, `halation`, `tone_response`가 별도로 필요하다.

### 제안 3: 후보팩 출력 경계

- 현재 top-level intent lock은 `color`를 사용한다. 새 필드들은 `color` 내부 분석/후보 메타데이터이며 `palette`, `color_grade` 같은 새 intent dimension이 아니다.
- requester-locked `color`가 있으면 candidate는 잠긴 역할·표면·범위를 바꾸지 못한다.
- 후보팩에는 최종 색 문구를 강제하지 말고, 비선호적 후보 순서와 함께 `effect_owner`, `spatial_scope`, `preserve_relations`, `reject_substitutes`를 노출한다.
- exact profile이 활성화되면 component evidence와 hard render gate를 함께 전달한다. bare 색 이름은 hard duty가 아니다.

## Thumbnail/native render gates

| 관계 | 썸네일 게이트 | 네이티브 게이트 |
|---|---|---|
| 팔레트 역할 계층 | dominant가 먼저 읽히고 accent가 제한된 위치에서 두 번째로 읽힘 | 각 역할이 지정 표면에 남고, 색 스필이나 전역 워시가 역할 경계를 무너뜨리지 않음 |
| selective color | base 무채색과 단일 예외가 즉시 구분됨 | 예외가 같은 표면의 무늬·원근·질감을 이어받고, 예외 밖 잔존 채도가 없음 |
| 저채도 색 분리 | 장면은 muted로 읽히되 피사체·배경/재질이 회색 덩어리로 합쳐지지 않음 | 인접 주요 색군과 표면 질감이 보존되고 black/midtone/highlight가 분리됨 |
| 혼합 광원/WB | 따뜻한 영역과 차가운 영역이 공간적으로 읽힘 | 광원 방향·감쇠·가림, 중성 기준면, 같은 재질의 두 광원 반응이 일관됨 |
| tone response | 의도한 밝은/어두운 질량과 피사체 분리가 유지됨 | black floor, 암부 질감, 중간톤 배치, 하이라이트 숄더, 클립 범위가 각각 검토 가능 |
| 전역/지역 그레이드 | 전체 룩 또는 제한 영역이 의도된 범위에서 읽힘 | 그레이드가 광원 풀·그림자 방향을 위조하지 않고, 지정 범위 밖 고유색/재질이 유지됨 |

모든 hard gate는 `partial_is_fail`로 채점해야 한다. 예를 들어 저채도는 맞지만 주요 재질 색 분리가 실패하면 그 관계는 실패다. 생성 전달 실패는 `UNSCORED`이며 픽셀 0점이 아니다. 사용자 미감 평가는 별도다.

## Regression and held-out tests

### 정적/패키지 테스트

1. 모든 color 후보가 정확히 하나의 `effect_owner`를 가진다.
2. `illumination` 후보는 `source_or_surface_anchor`와 최소 한 개 receiving region을 가진다.
3. `capture_white_balance` 후보는 neutral/familiar anchor 없이는 hard profile이 될 수 없다.
4. `global_grade`는 light direction, shadow ownership, bounce source를 소유하지 않는다.
5. `tone_response`는 palette hue를 바꾸는 문구를 소유하지 않는다.
6. 새 authored source와 생성 visual/semantic index의 해시·항목 수가 일치한다.
7. `intent_lock.open_dimensions`에는 기존 `color`만 사용하고 `palette`, `color_grade` 같은 미지원 차원을 넣지 않는다.

### 프롬프트 행동 인과쌍

| 테스트 쌍 | 고정 | 변경 | 예상 판정 |
|---|---|---|---|
| 팔레트 역할 | 색 목록, 피사체, 조명 | dominant/support/accent의 면적·소유 표면만 교환 | 역할이 바뀌고 나머지 축은 유지 |
| selective color | 장면·무늬·프레이밍 | 같은 표면의 마스크 예외 대 별도 컬러 카드/소품 | 전자만 hard profile PASS |
| 고유색/색 조명 | 같은 적색 재질 | 중성광 대 국소 시안 바운스 | 적색 재질 정체성은 유지되고 받는 면만 변함 |
| 혼합 광원/전역 grade | 같은 warm/cool 색 값 | 소스·감쇠·가림이 있는 2광원 대 화면 좌우 teal-orange split | 전자만 WB/light relation PASS |
| 저채도 분리 | 같은 물체·채도 목표 | 주요 재질 간 색 분리 유지 대 회색/진흙 워시 | 전자만 separation PASS |
| tone response | 색상·조명·구도 | black floor/midtone/highlight shoulder만 변화 | 팔레트 후보는 동일, tone 후보만 변화 |

### 회귀 샘플과 held-out

- 동기 회귀: 1883(동일 표면 selective color), 2132(단일 표면 포인트색), 2467(광원 소유 warm/cool), 2741(국소 cyan bounce + 표시 표면 보존).
- hard negatives: 1882(고노출이 팔레트 인상을 지배), 1916(레이블은 있으나 쿨–웜 공간 분리가 약함), 2299(캐스트와 환경 고유색 혼동), 2479(강한 색 화면/의상이 전역 그레이드가 아님).
- unrelated held-out: 인물 이외의 제품, 음식, 건축, 자연 장면에서 각각 1쌍 이상. selective-color는 제품 패키지/건축 패널, WB는 흰 종이/회색 금속이 있는 실내, tone response는 유리·금속·흰 직물 장면을 포함한다.
- 향후 렌더 평가는 모델/버전, 종횡비, 참조 처리, 시도 정책을 arm별로 고정하고 반복 렌더를 사용해야 한다. 현재 보고서에서는 렌더를 생성하지 않았다.

## External mechanism references

- CIE의 image-capture `adopted white` 정의는 한 장면에서도 adopted white가 달라질 수 있고, 거의 흰 확산체조차 조명·관찰 기하에 따라 회색이나 유색으로 보일 수 있다고 명시한다. 따라서 “흰 물체가 있다”가 아니라 **중성 기준면과 조명 맥락**을 함께 기록해야 한다. [CIE e-ILV: white, adopted (image capture)](https://cie.co.at/eilv/1428)
- ACES 공식 문서는 Look Transform을 전체 이미지에 적용하는 체계적 룩으로 설명하고, 전통적인 grading은 전체 또는 선택 영역을 조정할 수 있다고 구분한다. 이는 `global_grade`와 `regional_grade`, 그리고 실제 광원에 의한 국소 색을 따로 소유해야 한다는 근거다. [ACES Look Transforms](https://docs.acescentral.com/system-components/look-transforms/), [ACES Look Transform use cases](https://docs.acescentral.com/system-components/look-transforms/use-cases/)
- ARRI의 공식 dynamic-range 자료는 더 큰 장면 대비를 렌더링할 때 비선형·국소 tone mapping이 쓰인다고 설명한다. 이 보고서는 이를 특정 숫자 기준이 아니라 palette hue와 tone response를 분리해야 한다는 용어 근거로만 사용한다. [ARRI Dynamic Range White Paper](https://www.arri.com/resource/blob/295460/e10ff8a5b3abf26c33f8754379b57442/2022-09-28-arri-dynamic-range-whitepaper-data.pdf)

## Limitations and bounded decision

### 한계

- 픽셀 검사는 24장 표본이다. 4,908장 전체의 색채 분포나 성공률을 대표하지 않는다.
- 프롬프트 정규식은 한·영 핵심 표현을 보수적으로 잡았지만 번역 변형, 은유, 색 이름의 문맥을 완전히 판별하지 못한다.
- 참조 이미지, 생성기, 시드, 모델 버전, 후처리 여부가 없어 프롬프트–픽셀 인과를 검증할 수 없다.
- 코퍼스는 인물 이미지 비중이 높다. 비인물 held-out 검증 없이는 범용 색채 프로필로 promote할 수 없다.
- 네이티브 검사는 게시물당 첫 이미지 1장, 나머지 12장은 썸네일 검사다.
- 런타임 적용, 후보팩 활성화, 생성 전달, 새 렌더 픽셀, 사용자 판단은 모두 미검증이다.

### 결정

`proposed`

제안 범위는 다음으로 제한한다.

1. 새 authored color extension에 공통 `color_effect_contract`를 두어 고유색·조명·화이트밸런스·전역/지역 그레이드·톤 응답의 소유자를 분리한다.
2. `palette_role_hierarchy_relation`, `selective_color_same_surface_exception_relation`, `low_chroma_preserved_color_separation` 세 exact hard profile을 설계한다.
3. 혼합 광원, 하이라이트 롤오프, 하이/로우키, 할레이션은 기존 강한 프로필을 재사용하고 중복 생성하지 않는다.
4. 브랜드 필름명·색 목록·bare mood/palette·BM25F/embedding hit는 계속 advisory로 둔다.

구현되지 않았으며, package/prompt/render/user 어느 층도 promote 판정을 받지 않았다.

## Evidence appendix

### 동결 해시

- Manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- Gallery snapshot SHA-256: `35142b192966bd01eefa7c7cfdc05e7ca83a2f1c2ac43a7e34e6e693689cc64f`
- Translation snapshot SHA-256: `d2483fc1eefc941ddf2a51137ac2114cea0de61e8be3c152c00d49cfe5ce6586`

### 검사 이미지 경로

모든 경로의 기준은 `generated/reactorprompt-export-20260902-incremental/`이다.

```text
images/1883_DZpgpC_GigD_01.jpg
images/1883_DZpgpC_GigD_02.jpg
images/1882_DZphcF4Gtyo_01.jpg
images/1882_DZphcF4Gtyo_02.jpg
images/1916_DZxUzQkGuSZ_01.jpg
images/1916_DZxUzQkGuSZ_02.jpg
images/1917_DZxUAYkmuwx_01.jpg
images/1917_DZxUAYkmuwx_02.jpg
images/2132_Dap5qCGGiCZ_01.jpg
images/2132_Dap5qCGGiCZ_02.jpg
images/2136_DaqCRnTmi9i_01.jpg
images/2136_DaqCRnTmi9i_02.jpg
images/2299_DbcuYZ-GmbV_01.jpg
images/2299_DbcuYZ-GmbV_02.jpg
images/2298_Dbcq_-4mgy5_01.jpg
images/2298_Dbcq_-4mgy5_02.jpg
images/2467_DcAfXXLmuHQ_01.jpg
images/2467_DcAfXXLmuHQ_02.jpg
images/2479_DcAS04HGl0j_01.jpg
images/2479_DcAS04HGl0j_02.jpg
images/2741_Dcx0xZ8mlev_01.jpg
images/2741_Dcx0xZ8mlev_02.jpg
images/2734_DcslSCWml7h_01.jpg
images/2734_DcslSCWml7h_02.jpg
```

### 주요 재현 명령

```bash
jq '[.[] | select(.prompt != null and (.prompt | length) > 0)] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq -r '.[] | select(.id==1883 or .id==1882 or .id==1916 or .id==1917 or .id==2132 or .id==2136 or .id==2299 or .id==2298 or .id==2467 or .id==2479 or .id==2741 or .id==2734) | [.id,.caption,.images[0].local_file,.images[1].local_file] | @tsv' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq -r '.slots.color[] | [.id,.en] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json
jq -r '.slots.color_grading[] | [.id,.en] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json
jq -r '.slots.film_emulation[] | [.id,.en] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_tags.json

jq -r '.profiles[] | select((.category // "") | test("color|tone|tonal|highlight|white_balance";"i")) | [.id,.category] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json
```

프롬프트 집계는 Node.js에서 924개 행을 한 번 읽고 위 “전체 프롬프트 스캔”의 한·영 정규식을 각 프롬프트에 `RegExp.test`하여 게시물 단위로 세었다. 픽셀 접촉시트는 표에 나열한 순서로 `ffmpeg`의 `scale`, `pad`, `xstack`을 사용해 임시 생성했으며, 보고서에는 파생 접촉시트를 보존하지 않았다.

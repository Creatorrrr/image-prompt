# 16. 비인물 도메인 커버리지: 제품·음식·건축·자연·시스템·증거 기록

상태: `proposed`
모드: 리서치/설계 전용. 런타임 자산, 생성 인덱스, 테스트, 대상 스킬은 수정하지 않았다.

## Scope and sampling method

### 증거 경계

- 동결 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, 고유 프롬프트 본문 904개, ID 1565–2746.
- manifest SHA-256: `0f4cdd97730a3009071c853b6006fbbf00e14cfe8541935663f35cf6a38f7732`
- 이 보고서는 프롬프트 텍스트, 전달된 코퍼스 픽셀, 현재 authored asset, 외부 자료, 사용자 판단을 서로 다른 증거 층으로 유지한다.
- 코퍼스 이미지의 생성 모델·시드·참조 이미지·후처리 경로는 알 수 없다. 프롬프트와 결과가 함께 있어도 특정 문구가 픽셀의 원인이라고 단정하지 않는다.
- 사람을 포함한 장면은 보이는 자세·행동·도구 접촉·공간 점유만 관찰했다. 정체성, 동일인 여부, 보호 특성, 실제 관계·직업·국적·건강·성격을 추론하지 않았다.
- 이 주제의 “비인물”은 **사람이 절대 없어야 한다**는 뜻이 아니다. 제품, 음식, 건축 공간, 자연 대상, 작동 시스템 또는 기록 대상이 의미의 주체이고, 사람이 있더라도 그 관계를 설명하는 보조 행위자여야 한다는 뜻이다.

### 924개 프롬프트 전수 스캔

비어 있지 않은 924개 프롬프트 전부를 한·영 대소문자 무시 정규식으로 게시물 단위 집계했다. 1차는 넓은 도메인 어휘 회수, 2차는 프롬프트 앞부분의 매체·주체·행동과 인물 우선 문구를 비교하는 주체 우선 휴리스틱, 3차는 실제 프롬프트와 픽셀의 수동 판독이었다.

1차 어휘군은 다음을 포함했다.

- 제품: `product`, `packshot`, `catalog`, `still life`, `flat lay`, `packaging`, 병·향수·주얼리·기기 및 한글 대응어
- 음식: `food`, `dish`, `meal`, `cooking`, 빵·커피·음료·과일·접시 및 한글 대응어
- 건축: `architecture`, `building`, `facade`, `interior design`, 방·호텔·다리·도시 경관 및 한글 대응어
- 자연: `landscape`, `mountain`, `forest`, `wildlife`, `flower`, `habitat`, 날씨·빙하 및 한글 대응어
- 시스템: `infrastructure`, `logistics`, `workflow`, `inspection`, `machine`, `process`, `system`, 공정·측정·보정 및 한글 대응어
- 증거 기록: `documentary`, `evidence`, `field record`, `condition survey`, `scale reference`, `monitoring`, `documentation` 및 한글 대응어

이 집계는 부정 프롬프트, 배경, 렌즈의 `camera system`, 색의 `color system`, 분위기의 `documentary-like`까지 회수한다. 따라서 **회수량이지 의미 양성 수가 아니다**.

### 픽셀 표본

ID 범위를 초기(1565–1958), 중기(1959–2352), 후기(2353–2746)로 나눴다. 비인물 주체 또는 관찰 가능한 도메인 관계가 강한 후보는 가능한 범위에서 해당 게시물의 이미지를 전부 보았고, 양성이 희박한 건축·시스템·증거 기록에는 사람 중심 배경, 스타일 단어, 3D 아이콘을 근접대조로 붙였다.

- 총 **23개 게시물·60장**을 직접 검사했다.
- 초기: 4개 게시물·12장
- 중기: 6개 게시물·15장
- 후기: 13개 게시물·33장
- 60장 모두 5개의 접촉시트에서 썸네일 첫 읽기, 주체 우선순위, 관계 연속성, 텍스트 의존성을 확인했다.
- 대표 8장은 네이티브 크기로 다시 열어 재질 경계, 접촉, 작은 상태 흔적, 연결부를 확인했다.
- 60장 표본의 빈도를 전체 4,908장의 빈도로 일반화하지 않는다.

| 구간 | 게시물 | 검사 이미지 | 역할 |
|---|---|---:|---|
| 초기 | 1603, 1810, 1849, 1940 | 12 | 공방 배경, 조리·설거지 행동, 객체 포스터, `documentary` 스타일의 대조 |
| 중기 | 2038, 2040, 2047, 2073, 2076, 2107 | 15 | 건축이 포함된 복합 레이아웃, 음식 준비 단계, 시스템 explainer, 자연/도시 배경 대조 |
| 후기 | 2388, 2572, 2577, 2578, 2625, 2626, 2648, 2649, 2650, 2673, 2677, 2680, 2685 | 33 | 제품·음식·자연 실양성, 음식 행동, 비사진 아이콘 및 인물 우선 음식 장면 대조 |

## Prompt-side findings and counts

아래 수치는 프롬프트 문자열 매치이며 픽셀 성공률이나 후보팩 활성화 근거가 아니다. 한 게시물이 여러 범주에 중복된다.

| 넓은 어휘 회수 범주 | 매치 게시물 | 해당 게시물 이미지 수 | 대표 혼동 |
|---|---:|---:|---|
| 제품/정물/객체 | 220 | 880 | 패션 `catalog portrait`, 손에 든 뷰티 제품, 장난감·미니어처, 부정 프롬프트 |
| 음식/조리/식당 | 76 | 300 | 식당 배경의 인물 사진, 완성 음식이 보이지 않는 생활 장면 |
| 건축/실내/건물 | 192 | 761 | 인물 뒤의 방·호텔·거리, `interior`가 차 내부를 뜻하는 경우 |
| 자연/야생/풍경 | 180 | 751 | 인물 배경의 꽃·산·바다, 판타지 생물, 색·날씨 분위기 |
| 시스템/공정/검사 | 25 | 86 | `camera/color/storm system`, 배경 기계, 동작 없는 연구소 장식 |
| 다큐멘터리/증거/기록 | 34 | 116 | `documentary style`, SNS 기록 사진, 복원 지시, 실제 증거 구조 없음 |
| 위 어휘군 중 하나 이상 | 513 | 2,085 | 도메인 주체가 아니라 배경·스타일·부정어인 경우를 포함 |

### 좁은 authorial-core 판독

넓은 회수군을 매체, 주체, 행동, 부정어 위치로 좁히고 프롬프트 본문을 판독했을 때 다음 그룹이 남았다. 그룹은 중복될 수 있다.

| 그룹 | 강한/부분 후보 ID | 판독 |
|---|---|---|
| 제품·정물 | 2388, 2680; 교차 2626, 2648, 2650 | 2388은 녹는 얼음 정물, 2680은 태블릿 중심 flat-lay다. 2626은 식물 정물, 2648·2650은 음식 타이포그래피여서 범주가 겹친다. |
| 음식 대상·조리 단계 | 1810, 2047, 2572, 2648, 2649, 2650, 2673 | 대상만 있는 음식 사진과 도구-재료-단계가 있는 조리 장면을 분리해야 한다. 2047은 2D 애니메이션이라 사진 매체 양성은 아니다. |
| 건축 | 순수 주체 0; 부분 2038, 2040 | 궁궐 공간은 상단 원경 패널에서만 읽히고 전체 레이아웃의 주체는 동일 인물·샷 크기 비교다. 순수 건축 사진 양성은 발견하지 못했다. |
| 자연 | 2625; 부분/변형 2076, 2577, 2578, 2626 | 2625가 가장 강한 자연 주체다. 2626은 스튜디오 식물 정물, 2577은 서식지 없는 동물 머리, 2578은 판타지 생물, 2076은 인물 우선 여행 사진이다. |
| 시스템 | 2073; 단일 단계 2047, 2572 | 2073만 입력·부품·경로·출력처럼 보이는 explainer를 직접 요구한다. 2047·2572는 공정 전체가 아닌 한 단계다. |
| 증거 기록 | 엄격 양성 0; 스타일 대조 1810, 1940, 2673 | `documentary`는 촬영 register일 뿐 관찰 대상·고정 참조·상태 경계·기록 절차를 만들지 않았다. |

핵심 분포는 **명시적 비인물 주체가 후기 ID에 집중**되고, 건축·시스템·증거 기록은 빈도보다도 정확한 관계 양성이 부족하다는 것이다. 이 결손은 새 전역 기본값의 근거가 아니라 held-out과 정확 프로필을 먼저 설계해야 할 이유다.

## Pixel-side observations and sample IDs

아래는 60장 표본에 한정한 관찰이다.

### 제품·정물

- **2388, 4/4장:** 흰 접시, 얼음, 얼음 속 라즈베리, 물방울과 녹은 물이 썸네일에서 하나의 정물 관계로 읽힌다. 네이티브에서는 얼음의 투명·불투명 영역, 젖은 접촉면, 접시 경계가 분리된다. 상업 제품 사진이라기보다 물질 상태 정물이다.
- **2680, 2/2장:** 중앙 태블릿이 가장 먼저 읽히고 주변 안경·노트·펜이 반복 간격으로 조직된다. 네이티브에서 금속, 유리, 종이, 플라스틱, 세라믹의 재질 반응과 접촉 그림자가 구별된다. 단, 실제 사용 상태나 기능은 검증되지 않는다.
- **2677, 2/2장; 2685, 1/1장:** 선물 상자·패키지의 실루엣, 바닥 접촉, 중심 계층은 명확하지만 3D game icon이다. “제품처럼 보이는 객체 관계”와 “제품 사진 매체”를 분리해야 하는 근접대조다.
- **1603, 2/2장:** 재봉틀·도구·테이블이 있지만 인물 얼굴과 상반신이 우선한다. 공방 소품의 존재만으로 제품·제작 시스템을 활성화하면 안 된다.

### 음식·조리

- **1810, 4/4장:** 손-주걱-냄비 접촉, 증기, stove support가 유지된다. 그러나 음식 자체의 전후 상태는 냄비 안에 가려지고 일부 장면은 카메라를 향한 인물 읽기가 더 강하다. 조리 행동 양성이지 재료 상태 기록 양성은 아니다.
- **1940, 4/4장:** 물-수도-접시-수세 도구 관계는 보이지만 이는 설거지 과업이다. `documentary-style`과 생활 흔적은 있어도 음식 상태나 증거 기록은 아니다.
- **2047, 1/1장:** 파를 자르는 손·칼·도마의 접촉, 조리 전 재료와 “완성 음식 없음”이 동시에 읽힌다. 단계 경계의 좋은 양성이지만 2D 애니메이션이므로 사진 품질 양성과 혼합하면 안 된다.
- **2572, 3/3장:** 팬, 손잡이, 뒤집개, 달걀, burner가 한 작업 그래프를 이룬다. 재료 상태와 도구 접촉이 모두 보이고 완성 접시로 치환되지 않는다. 사람은 크지만 시선과 두 손이 음식 단계로 향한다.
- **2648, 3/3장:** 오이 절단면·껍질·씨가 `SALAD` 글자 구조를 만든다. 문자 가독성과 식재료 재질이 동시에 유지되며, 접시가 지지면으로 읽힌다.
- **2649, 4/4장:** 우유 흐름, 커피 표면, 거품 경계가 보이며 `Lunch Time`은 대체로 읽힌다. 다만 글자가 물질 상태보다 먼저 읽혀 음식 사진과 타이포그래피의 소유권을 분리해야 한다.
- **2650, 4/4장:** 상추·토마토 재질은 보존되지만 두 장은 `SALAD`가 한 줄, 두 장은 `SA/AD`에 가까운 2행 배열로 갈린다. 프롬프트의 “single word”가 픽셀 read order에서 흔들린 사례다.
- **2673, 3/5장 표본:** 젓가락-면-그릇 접촉은 보이지만 얼굴이 첫 주체이고 얕은 심도로 음식의 상태가 보조화된다. food-context 양성이지만 food-primary 양성은 아니다.

### 건축·자연

- **2038, 1/1장; 2040, 3/3장:** 상단 원경에서 궁궐의 문, 마당, 축선, 인물-건축 스케일은 읽힌다. 그러나 중단 얼굴과 하단 눈이 전체 포스터의 주의를 가져가므로 건축 주체 양성은 아니다.
- **2076, 2/6장 표본:** gondola 창 밖 산악 지형, 설면, 나무가 깊은 초점으로 남지만 인물의 얼굴·흰 재킷이 첫 읽기다. 선명한 풍경 배경은 자연 주체와 동의어가 아니다.
- **2577, 1/1장:** 동물 머리의 외형은 명확하지만 habitat, 행동, 환경 스케일은 없다. 불꽃·청록 그레이드는 wildlife evidence를 대신하지 않는다.
- **2578, 1/1장:** 비행 자세, 날개, 구름, 먼 새의 스케일 비교는 읽히지만 대상이 판타지 생물이다. 자연/야생 정확 프로필의 실양성으로 자동 편입하면 안 된다.
- **2625, 2/2장:** 아래에서 본 연잎, 방사형 잎맥, 투과광, 하늘 틈, 한 개 꽃봉오리가 하나의 자연 주체로 읽힌다. 네이티브에서 잎맥·겹침·역광 경계가 유지된다. 다만 연못 수면이나 넓은 habitat는 프레임 밖이다.
- **2626, 3/3장:** 두 튤립의 꽃잎·줄기 구조와 스튜디오 지지 관계는 선명하다. 검은 배경의 botanical still-life이므로 `nature.habitat context`를 강제하면 오분류된다.

### 시스템·증거 기록

- **2073, 6/6장:** 스마트폰 exploded stack, 배터리-구동계, 냉장 순환, 3D printer 단계, 필터 경로, 로켓 순서가 각각 썸네일에서 “모듈과 흐름”으로 읽힌다. 화살표·빛나는 선·수직 분해가 연결을 강화하지만, 실제 기술적 정확성은 이 픽셀만으로 검증할 수 없다. **시각적 시스템 가독성은 기능적 진실의 증거가 아니다.**
- **1849, 2/4장 표본:** 거대 배경 객체와 작은 전경 carrier가 영화 포스터 관계를 만들지만 input, operation, output, evidence state는 없다. 계층적 관계가 있다는 이유만으로 시스템이라 부를 수 없다.
- **2107, 2/7장 표본:** 게시물 캡션은 조선소를 말하지만 프롬프트와 픽셀은 일반 도시 거리의 인물 중심 장면이다. 캡션 메타데이터가 prompt/pixel evidence를 대체할 수 없는 사례다.
- **1810·1940·2673:** 모두 프롬프트에 `documentary` 계열 문구가 있고 생활 행동이 보이지만, 관찰 대상의 고정 위치, 측정·척도, 상태 비교, 개입 전후 경계, 기록 식별자가 없다. 촬영 스타일과 증거 기록 ontology가 분명히 갈린다.

## Prompt/pixel alignment and divergences

### 정렬된 사례

- 2388의 `melting`, `water droplets`, 비대칭 접시 배치는 네 장에서 물질 상태·지지면·정물 계층으로 읽힌다.
- 2572의 손-팬-뒤집개-달걀-버너 관계는 세 장 모두 연결된다. `cooking` 레이블보다 접촉과 단계가 강한 제어다.
- 2625의 저각 연잎 canopy, 한 개 꽃봉오리, 잎맥, 하늘 틈은 두 장에서 일관된 자연 주체를 만든다.
- 2680의 중앙 태블릿과 주변 액세서리 계층은 두 장에서 유지된다.
- 2073의 `steps, layers, logical sequence`는 여섯 장 모두 분해·배열·흐름 표현으로 나타난다.

### 불완전하거나 잘못 소유될 수 있는 사례

- 2073은 prompt placeholder가 `[YOUR IDEA]`로 비어 있어 각 이미지의 실제 시스템 의미는 결과가 임의로 채운 것이다. 보이는 연결이 기술적으로 맞는지는 `UNSCORED`다.
- 2650은 재료 재질은 성공하지만 한 줄 단어 구조가 절반의 표본에서 2행으로 바뀐다. 재질 PASS가 read-order PASS를 대신하지 않는다.
- 2038·2040은 궁궐 공간을 포함하지만 전체 레이아웃의 주체는 인물 샷 스케일 비교다. 건축물이 선명하다는 사실이 architecture-primary PASS를 뜻하지 않는다.
- 2626은 자연 대상을 보여도 habitat는 없다. `plant` 하나로 habitat obligations를 활성화하면 스튜디오 botanical still-life을 잘못 실패시킨다.
- 2577·2578은 `wildlife photograph` 어휘가 있어도 각각 서식지 없는 동물 머리와 판타지 생물이다. 정확 프로필은 매체와 세계 상태를 함께 분기해야 한다.
- 1810·1940·2673의 `documentary`는 candid/lifestyle register다. evidence target, reference, state boundary가 없으므로 증거 기록으로 승격할 수 없다.
- 2107은 캡션과 픽셀이 어긋난다. caption, prompt, pixel을 합성한 단일 검색 레이블은 hard activation에 사용할 수 없다.

## Existing-data overlap and ownership

### 이미 있는 강점

`skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`에는 다음 quality profile이 이미 있다.

- 기본 도메인: `product`, `food`, `architecture`, `nature`, `documentary`
- 운영/증거: `science_inspection`, `mobility_logistics`, `agriculture_food_systems`, `biodiversity_monitoring`, `heritage_documentation`, `disaster_risk_operations`
- 상태/구조: `natural_process`, `longitudinal_place_state`, `visual_structure`

각 profile의 `prompt_focus`는 이미 좋은 방향을 갖는다. 예를 들어 product는 `surface accuracy / weight and contact / commercial hierarchy`, architecture는 `spatial scale / vertical and depth cues / material light`, science inspection은 `measurement legibility / scale and calibration evidence / controlled material state`를 요구한다.

`photo_prompt_tags.json`에도 비인물 주체와 관계를 표현할 수 있는 authored 후보가 풍부하다.

- 매체·장르: `product_catalog`, `ecommerce_photo`, `menu_photo`, `wildlife_photo`, `architecture_magazine_photo`, `scientific_record`, `documentary_photo`
- 주체: 제품·음식·동물·건축/인프라·기계·시료·monitoring station·cold-chain·repair 대상
- 관계 슬롯: `subject`, `action`, `capture_context`, `procedure_step`, `surface_material`, `space_condition`, `scale_relation`, `composition`, `focus`

`photo_prompt_research_extension.json`의 17개 preset에는 `loading_dock_forklift_handoff_record`, `heritage_condition_documentation`, `returned_product_reuse_assessment_record`, `produce_cold_chain_handoff_record`, `post_storm_building_safety_record`, `longitudinal_place_state_record`, `natural_process_trace_documentary` 등이 있어 좁은 evidence scene 후보가 이미 상당히 구체적이다.

### 현재 결손

- 기본 quality profile은 대부분 `prompt_focus` 세 줄이어서 component minimum, required evidence field, reject substitute, thumbnail/native gate가 없다.
- `visual_proposition.subject_classes.object_scene`는 object, food, environment, plant, sign을 하나로 묶는다. 제품의 support/contact, 음식의 material state, 건축의 enclosure/circulation, 자연의 habitat/state를 서로 교환할 위험이 있다.
- `photo_prompt_visual_obligations.json`에는 generic product/food/architecture/nature의 시작 ID가 없고, 이 범위에서 명확히 겹치는 정확 hard profile은 `forensic_scene_documentation_process` 정도다.
- evidence-heavy preset은 연구 확장에 있으나, 공통 “관찰 대상-참조-상태 경계” base contract가 authored hard profile로 공유되지 않는다.
- 시스템은 화살표·글로·exploded view만으로 쉽게 그럴듯해진다. 현재 quality focus만으로는 경로 연속성이나 입출력의 상호 대응을 fail-closed하기 어렵다.

### 올바른 소유층

| 내용 | 제안 소유층 | 이유 |
|---|---|---|
| 넓은 비인물 주체 분기·관계 예산 | `photo_prompt_quality_layers.json`의 `visual_proposition`/quality profile | broad term은 advisory여야 하며 전역 의무가 아니기 때문 |
| 좁은 정확 의미, required fields, reject substitutes, render gates | `photo_prompt_visual_obligations.json / profiles[]` | exact/core hit에서만 hard obligation을 만들기 때문 |
| 구체 주체·행동·캡처·절차·표면·공간 후보 | `photo_prompt_tags.json`의 기존 슬롯 | 새 병렬 schema 없이 조합 가능 |
| 특수 운영/증거 preset | `photo_prompt_research_extension.json` | 기존 17개 실험 preset과 같은 계층 |
| 생성 visual-profile index | 소유 금지 | generated index는 authored source가 아니며 구현 시 재생성 대상일 뿐 |

## Proposed semantic components and confusion boundaries

### 공통 domain-neutral 관계 문법

모든 비인물 장면을 같은 미학으로 만들지는 않되, 의미를 검사하는 최소 골격은 공유할 수 있다.

```text
primary evidence subject
  -> boundary / support / enclosure
  -> observable contact, path, or state relation
  -> scale, viewpoint, or reference that makes the relation legible
  -> local consequence or distinguishable state
```

공통 필드는 다음과 같다.

1. `primary_subject_class`: `product_object | food_material | built_space | natural_subject | bounded_system | evidence_target`
2. `subject_priority`: `primary | shared | contextual`; hard profile은 `primary` 또는 명시적 `shared`만 허용
3. `observation_mode`: 도메인별 hero, material study, preparation, circulation, habitat, flow, inspection 등
4. `support_or_boundary`: 지지면, 용기, enclosure, habitat boundary, system boundary, fixed ROI
5. `observable_relation`: 접촉, 변형, 흐름, 가림, 통과, 비교, 반복 관측
6. `state_evidence`: 현재 상태, 공존 단계, 국소 흔적; 단일 이미지가 보여주지 않는 elapsed time은 발명하지 않음
7. `scale_or_reference`: 주변 객체, 인체 스케일, 눈금, calibration target, 고정 landmark 중 해당되는 것
8. `viewpoint_support`: top-down, elevation, section-like view, fixed ROI, macro, deep focus 등 관계를 읽히게 하는 촬영 구조
9. `text_dependency`: `none | supporting | primary`; readable text만으로 의미가 성립하면 픽셀 의미는 불충분
10. `confusion_negative`: 가장 가까운 대체 실패 하나 이상

### 도메인별 observable axes

| 도메인 | 관찰 축 | 최소 component groups | 혼동 음성 |
|---|---|---|---|
| 제품 | 객체 외형/부품 경계, 지지·무게, 재질 분리, 상업 계층, 선택적 사용·스케일 | `object_topology`, `support_contact`, `material_response`; hero/flat-lay 중 한 mode | 사람 옆 소품, 부유 객체, 로고만 선명한 이미지, 3D 아이콘을 사진으로 오분류 |
| 음식 | 식재료/음식 정체, 절단·열·수분·거품 상태, 용기/도구 접촉, 준비/완성 단계 | `edible_material`, `state_trace`, `vessel_or_tool_contact`; 단계 명시 시 `stage_boundary` | 식당 인물만, 음식색 소품, 글자만 읽히고 재료가 불명확, 완성 음식으로 단계 치환 |
| 건축 | enclosure, 구조/개구부, circulation/depth, 재료 junction, 수직·스케일 | `spatial_volume`, `opening_or_path`, `material_junction`, `scale_cue` | 인물 뒤 장식 건물, facade texture만, wide lens 왜곡을 공간 의미로 오인 |
| 자연 | 대상 형태, habitat 또는 명시적 studio/specimen mode, 행동/생장/기상 상태, 깊이·스케일 | `subject_morphology`, `mode_context`, `state_or_behavior`; habitat mode일 때 `subject_habitat_relation` | 꽃 배경, 판타지 생물을 wildlife evidence로 오인, studio botanical에 habitat 강제 |
| 시스템 | system boundary, input, 연결/전달 경로, operation/control, output/state | `system_boundary`, `input`, `continuous_path`, `output_or_state`; 최소 4그룹 | 화살표·글로만, 분리 부품 나열, 기계 옆 인물, 기술적 정확성의 무근거 추론 |
| 증거 기록 | 관찰 대상, 고정 위치/참조, 상태 흔적, 캡처 방법, 시간/개입 경계 | `evidence_target`, `locator_or_reference`, `condition_state`, `capture_boundary`; 측정 주장 시 calibration | documentary mood, CCTV 룩, 표식 소품만, 단일 프레임에서 before/after 발명 |

## Candidate-pack/data proposals

### A. Broad advisory candidate

제안 ID: `nonportrait_subject_relation_budget`

- 소유: `photo_prompt_quality_layers.json / visual_proposition`
- 역할: 현재 `object_scene`을 여섯 subject class로 분리하고, class별로 한 개의 observable relation과 한 개의 confusion negative를 선택한다.
- 제안 필드: `primary_subject_class`, `subject_priority`, `observation_mode`, `support_or_boundary`, `observable_relation`, `state_evidence`, `scale_or_reference`, `viewpoint_support`, `text_dependency`, `confusion_negative`.
- broad activation: `product`, `food`, `architecture`, `nature`, `system`, `documentary` 일반어, 또는 facet/BM25F/embedding hit.
- activation 결과: **advisory only**. 일반어 하나로 아래 hard profile을 켜지 않는다.
- 인물 이식 방지: `body_pose`, `gaze`, `beauty`, `wardrobe`를 필수 필드로 갖지 않는다. 사람이 있는 경우에도 `operator_role`은 선택적이고 주체 우선순위를 바꾸지 않는다.

### B. Narrow exact hard profiles

아래 이름은 제안이며 구현되지 않았다.

#### 1. `product_surface_support_hierarchy`

- exact/core 예: `catalog product material study`, `packshot with support and material response`, `제품 소재·지지 카탈로그 기록`.
- required fields: `object_topology_phrase`, `support_contact_phrase`, `material_separation_phrase`, `commercial_hierarchy_phrase`, `nearest_substitute_exclusion_phrase`.
- exclude: `fashion catalog portrait`, `product held beside face`, `floating icon`, `logo mockup`, `packaging illustration`.
- thumbnail gates: 제품 객체가 첫 읽기이고 hero/flat-lay hierarchy가 무너지지 않음; 사람이나 장식 props가 주체를 빼앗지 않음.
- native gates: 이음·edge·반사·투명/불투명·접촉 그림자가 재질과 지지면에 맞고, 중복·부유·뒤틀림이 없음.

#### 2. `food_material_state_vessel_relation`

- exact/core 예: `food material-state study`, `preparation-stage food record`, `조리 단계 재료 상태 기록`.
- required fields: `edible_material_phrase`, `state_trace_phrase`, `vessel_or_tool_contact_phrase`, `stage_boundary_phrase`, `non_food_context_exclusion_phrase`.
- exclude: `restaurant portrait`, `food-colored prop`, `finished dish substituted for preparation stage`, `typography with unreadable ingredient identity`.
- thumbnail gates: 음식 또는 단계가 사람보다 먼저/공동으로 읽히고 용기·도구 관계가 남음; 요청한 한 줄/한 접시 구조가 유지됨.
- native gates: 절단면, 수분, 거품, 열·기름·김, 씨·섬유 등 재료 상태와 도구 접촉이 물리적으로 이어짐.

#### 3. `architecture_enclosure_circulation_scale`

- exact/core 예: `architectural space documentation`, `interior circulation study`, `건축 공간 동선 기록`.
- required fields: `spatial_volume_phrase`, `opening_or_path_phrase`, `material_junction_phrase`, `scale_anchor_phrase`, `perspective_control_phrase`.
- exclude: `street portrait`, `hotel fashion portrait`, `decorative facade backdrop`, `room moodboard`.
- thumbnail gates: enclosure와 이동/깊이 축이 첫 읽기이고 작은 인물이 있다면 스케일 cue로만 작동.
- native gates: 벽-바닥-천장, 기둥-보, 문/창 개구, 재료 junction과 수직선이 일관되고 wide-lens 휨이 구조를 위조하지 않음.

#### 4. `nature_habitat_subject_state`

- exact/core 예: `habitat-context wildlife record`, `botanical habitat observation`, `서식지 맥락 자연 관찰`.
- required fields: `subject_morphology_phrase`, `habitat_relation_phrase`, `state_or_behavior_phrase`, `depth_or_scale_phrase`, `studio_or_fantasy_exclusion_phrase`.
- exclude: `flower portrait background`, `studio botanical still-life`, `fantasy wildlife`, `colored fog nature mood` unless a separate mode/profile is exact.
- thumbnail gates: 자연 대상과 habitat의 관계가 동시에 읽히고 사람/스타일 효과가 의미를 대체하지 않음.
- native gates: 종/대상 형태를 과도하게 단정하지 않는 범위에서 잎맥·관절·지표·기상 흔적·가림·스케일 연속성이 유지됨.

#### 5. `bounded_system_input_path_output`

- exact/core 예: `bounded system flow explainer`, `operational input-to-output record`, `입력-경로-출력 시스템 기록`.
- required fields: `system_boundary_phrase`, `input_phrase`, `continuous_transfer_path_phrase`, `operation_or_control_phrase`, `output_state_phrase`, `decorative_flow_exclusion_phrase`.
- exclude: `camera system`, `color system`, `storm system`, `machine backdrop`, `glowing arrows only`, `exploded components without dependency`.
- thumbnail gates: input/path/output read order와 system boundary가 2–3초 안에 보임.
- native gates: 연결선·호스·컨베이어·접촉점·부품 junction이 끊기지 않고 방향과 상태 변화가 서로 모순되지 않음. 기능 정확성은 별도 전문 검증 없이는 `UNSCORED`.

#### 6. `documentary_evidence_target_reference_state`

- exact/core 예: `condition documentation record`, `inspection evidence scene`, `fixed-reference monitoring record`, `상태 조사 기록`.
- required fields: `evidence_target_phrase`, `locator_or_reference_phrase`, `condition_state_phrase`, `capture_method_phrase`, `time_or_intervention_boundary_phrase`, `documentary_style_exclusion_phrase`.
- exclude: `documentary style`, `candid lifestyle`, `CCTV look`, `evidence marker as decoration`, `single-frame invented before/after`.
- thumbnail gates: 무엇을 왜 기록하는지 target/reference/state 관계가 읽히고 인물·무드가 주체를 가리지 않음.
- native gates: 눈금·marker·fixed landmark·condition boundary가 대상과 같은 평면/위치 논리에 있고, 읽을 수 없는 텍스트나 임의 표식만으로 의미를 세우지 않음.
- 기존 `forensic_scene_documentation_process` 및 research extension의 좁은 preset은 이 base contract를 상속하거나 동등한 필드를 매핑하되, 각 도메인 고유 절차를 지우지 않는다.

### C. Candidate fields in existing slots

새 schema slot을 만들기 전에 기존 슬롯에 다음 candidate ID를 추가하는 설계가 우선이다.

| 슬롯 | 제안 candidate ID | 내용 |
|---|---|---|
| `subject` | `primary_product_object_material_study` | 주체 외형·부품 경계가 보이는 비브랜드 제품 객체 |
| `subject` | `food_material_at_declared_stage` | 조리/제공 단계가 명시된 음식·재료 |
| `subject` | `architectural_enclosure_and_path_subject` | enclosure와 circulation이 함께 읽히는 공간 |
| `subject` | `natural_subject_in_mode_context` | habitat 또는 명시적 studio/specimen mode의 자연 대상 |
| `subject` | `bounded_input_path_output_system` | 경계가 있는 시스템 주체 |
| `subject` | `fixed_reference_condition_target` | 위치·상태를 기록하는 evidence target |
| `action` | `showing_product_support_and_material_response` | 제품-지지면-재질 반응을 동시에 노출 |
| `action` | `showing_food_state_at_one_process_boundary` | 단일 조리 단계와 흔적을 노출 |
| `action` | `revealing_enclosure_opening_and_circulation` | 공간 체적·개구부·경로를 연결 |
| `action` | `showing_natural_subject_state_in_context` | 형태·상태·context를 연결 |
| `action` | `tracing_input_through_operation_to_output` | 시스템 경로를 끊김 없이 연결 |
| `action` | `recording_condition_against_fixed_reference` | evidence target과 참조를 같은 프레임 논리로 기록 |
| `capture_context` | `nonportrait_relation_first_capture` | 주체보다 relation을 가리지 않는 카메라/초점 선택 |
| `procedure_step` | `single_frame_state_boundary_check` | 보이는 현재/공존 단계만 주장 |
| `scale_relation` | `domain_relevant_scale_anchor` | 사람, 주변 객체, 눈금, fixed landmark 중 적합한 하나 |

## Thumbnail/native render gates

### 공통 gate

| 스케일 | PASS | FAIL |
|---|---|---|
| thumbnail | 도메인 주체와 핵심 관계가 2–3초 안에 읽힘; 인물·텍스트·스타일 효과가 의미를 가로채지 않음 | 장면 이름은 맞지만 관계가 배경 소품 수준; 글자·얼굴·글로가 유일한 첫 읽기 |
| native | 접촉, junction, 표면 상태, 연결 경로, 작은 참조가 물리적으로 이어짐 | 부유, 중복, 끊긴 파이프/도구, 잘못된 그림자, 불가능한 재질, 임의 marker |
| both | 요청한 observation mode와 주체 우선순위가 유지됨 | product↔icon, habitat↔studio, documentary style↔evidence 같은 범주 치환 |

`partial_is_fail`을 적용한다. 예를 들어 2073처럼 썸네일 시스템 read가 좋아도 native 기능 정확성이 검증되지 않았으면 전체 PASS가 아니라 해당 gate만 PASS이고 기능 truth는 `UNSCORED`다.

## Regression and held-out tests

### Corpus-backed regression pairs

| 프로필 | 양성/부분 양성 | hard negative | 판정 포인트 |
|---|---|---|---|
| product | 2680, 2388 | 1603, 2677, 2685 | 제품/정물 주체와 support/material hierarchy 대 공방 배경·3D 아이콘 |
| food | 2572, 2648, 2649 | 2673, 1940 | food state/tool contact 대 food-context portrait·비음식 생활 과업 |
| architecture | 부분 2038, 2040 | 2076, 2107 | 상단 공간 축은 보이지만 전체 primary 여부를 별도 gate; 순수 양성 부재 |
| nature | 2625 | 2626, 2076, 2577, 2578 | habitat-context 대 studio botanical·portrait background·서식지 없음·fantasy |
| system | 2073 | 1603, 1849 | input/path/output read 대 기계 배경·계층 포스터 |
| evidence | 코퍼스 엄격 양성 없음 | 1810, 1940, 2673 | `documentary` register가 evidence ontology를 활성화하지 않아야 함 |

### Prompt-only held-out

픽셀 검토에 사용하지 않은 다음 ID는 구현 후 retrieval/routing held-out으로 보존한다.

- 2410: 얼굴 옆 스마트폰. `product`가 있더라도 portrait/product-shared인지 검증.
- 2652, 2678, 2682: dessert/pouch mascot·icon. 사진 프로필과 object-render 관계 분리.
- 2121: restaurant portrait. 음식이 실제 주체가 아닐 때 food hard profile 비활성.
- 2104, 2106: 일반 street portrait. `street`, `building`을 architecture로 hard-route하지 않음.
- 1799: 업로드 사진 `restore` 지시. restoration/evidence exact activation 방지.
- 1826: laboratory decor의 cosplay portrait. 시스템·inspection 비활성.
- 2410과 2652 등은 prompt-only held-out이며 이 보고서에서 픽셀 품질을 평가하지 않았다.

### 새로 작성해야 할 exact positive cases

코퍼스에 양성이 없는 범주는 합성 프롬프트 fixture가 필요하다.

1. 빈 건축물 내부에서 entrance–corridor–stair–exit가 재료 junction과 사람 스케일 표식으로 연결된 architecture case.
2. 같은 facade의 고정 viewpoint에서 손상 부위, 눈금, 위치 anchor, 개입 전 상태가 보이는 evidence case.
3. input bin–transfer path–operation chamber–output bin이 한 프레임에서 연결된 system case.
4. 각 positive마다 얼굴 중심 인물, decorative arrows, unreadable label, random scale card, studio botanical을 hard negative로 붙인다.

### 평가 순서

1. authorial-core exact/core activation
2. 필수 component group과 required evidence field
3. prompt contract audit
4. 독립 frozen input으로 이미지 생성
5. thumbnail gate
6. native gate
7. hard-negative confusion gate
8. 사용자 판단

BM25F/embedding-only hit는 1번에서 hard obligation을 만들 수 없다. prompt/runtime PASS, pixel PASS, 사용자 선호를 서로 대체하지 않는다.

## Limitations and bounded decision

- 이 증분 코퍼스는 인물 중심이고 순수 건축·증거 기록 양성이 사실상 없다. 따라서 architecture/evidence 정확 프로필의 픽셀 자격을 이 코퍼스로 확정할 수 없다.
- 시스템 양성은 2073 한 게시물의 6개 3D explainer에 집중된다. 관계 가독성은 관찰했지만 기술적 정확성은 검증하지 않았다.
- 음식 타이포그래피는 readable text와 음식 재질이 결합된 특수 사례다. 일반 food photography의 대표 표본으로 일반화할 수 없다.
- 자연 표본은 habitat, studio botanical, animal close-up, fantasy wildlife가 섞여 있다. 한 개의 `nature` hard profile로 합치면 오분류된다.
- 픽셀 표본은 23개 게시물·60장뿐이며 전체 4,908장의 성공률을 나타내지 않는다.
- 외부 연구는 사용하지 않았다. 이번 결론은 동결 코퍼스와 현재 authored asset의 구조적 gap으로 충분히 도출되며, 건축 기록·과학 측정의 구체 규격을 구현할 때는 해당 authoritative standard를 별도 검토해야 한다.
- 구현, 인덱스 재생성, 테스트 실행, 독립 render qualification, 사용자 판단은 모두 수행하지 않았다.

### Bounded decision

- `nonportrait_subject_relation_budget`: **proposed** — broad advisory로만 도입 가치가 있다.
- `product_surface_support_hierarchy`: **proposed** — 2388·2680의 prompt/pixel 근거가 있다.
- `food_material_state_vessel_relation`: **proposed** — 음식 대상과 조리 단계를 분리하는 근거가 충분하다.
- `architecture_enclosure_circulation_scale`: **revise before implementation** — 순수 corpus positive가 없어 새 fixture와 독립 render qualification이 먼저다.
- `nature_habitat_subject_state`: **proposed with mode split** — habitat, studio botanical, fantasy를 분리해야 한다.
- `bounded_system_input_path_output`: **proposed, technically unscored** — 시각 gate는 제안 가능하지만 기능 truth는 전문 검증 전 `UNSCORED`다.
- `documentary_evidence_target_reference_state`: **revise before implementation** — 스타일 음성은 강하지만 corpus pixel positive가 없다. 기존 forensic profile과 research-extension preset을 base-contract 방식으로 통합 설계한 뒤 검증해야 한다.

종합 상태는 `proposed`다. 다만 architecture와 documentary evidence는 이 보고서만으로 hard profile 구현 준비가 끝난 것이 아니다.

## Evidence appendix

### Authored assets inspected

- `skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_tags.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_research_extension.json`
- generated visual-profile index는 authored source로 사용하지 않았다.

### Sample image paths

모든 경로는 `generated/reactorprompt-export-20260902-incremental/` 기준이다.

- 1603: `images/1603_DY4wThpmgYx_01.jpg`, `_02.jpg`
- 1810: `images/1810_DZaD3kuGlEA_01.jpg`–`_04.jpg`
- 1849: `images/1849_DZkQdmRmmqk_01.jpg`, `_02.jpg`
- 1940: `images/1940_DZ4HfCHmsLF_01.jpg`–`_04.jpg`
- 2038: `images/2038_DaQFMYlAf8o_01.jpg`
- 2040: `images/2040_DaQBLwnGllL_01.jpg`–`_03.jpg`
- 2047: `images/2047_DaP4pXOmmbL_01.jpg`
- 2073: `images/2073_DaaOpKwGhKL_01.jpg`–`_06.jpg`
- 2076: `images/2076_DaZc8egGuUe_01.jpg`, `_02.jpg`
- 2107: `images/2107_DaebeTGGsQQ_01.jpg`, `_02.jpg`
- 2388: `images/2388_Dbuy3raGlV7_01.jpg`–`_04.jpg`
- 2572: `images/2572_DcVdWWGmo6Q_01.jpg`–`_03.jpg`
- 2577: `images/2577_DcV-wPUmllI_01.jpg`
- 2578: `images/2578_DcV-QRQGmAZ_01.jpg`
- 2625: `images/2625_DcgVZAumsvM_01.jpg`, `_02.jpg`
- 2626: `images/2626_DcgVNgCmjJC_01.jpg`–`_03.jpg`
- 2648: `images/2648_DciZir7GtBv_01.jpg`–`_03.jpg`
- 2649: `images/2649_DciZ8lOGmgi_01.jpg`–`_04.jpg`
- 2650: `images/2650_DciZeBqGvj3_01.jpg`–`_04.jpg`
- 2673: `images/2673_Dcllog9mqn5_01.jpg`–`_03.jpg`
- 2677: `images/2677_Dcn2UlOGiqT_01.jpg`, `_02.jpg`
- 2680: `images/2680_Dcn2LesmjBy_01.jpg`, `_02.jpg`
- 2685: `images/2685_Dcn2ZfkGjA__01.jpg`

### Reproduction commands

프롬프트 행과 authored profile inventory:

```bash
jq '[.[] | select((.prompt_missing | not) and ((.prompt // "") | length > 0))] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

jq '.quality_profiles | keys' \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json

jq -r '.profiles[] | [.id, .category] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json

jq -r '.presets[] | [.id, .family] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_research_extension.json
```

도메인 집계는 Node로 manifest를 읽고 `rows.filter(r => regex.test(r.prompt))`를 여섯 한·영 정규식에 각각 적용했다. 게시물 이미지 수는 `hits.reduce((n, r) => n + r.images.length, 0)`로 합산했고, 합집합은 post ID `Set`으로 계산했다. 검사 파일 목록은 manifest의 `images[].local_file`에서 직접 해석했다.

접촉시트는 원본을 360×440 안에 종횡비 보존 축소하고 360×480 black pad 후 `ffmpeg` `xstack` 4열로 배치했다. 네이티브 표본은 원본 파일을 `detail=original`로 직접 열었다. 접촉시트는 `/tmp`에만 만들었고 연구 산출물에 포함하지 않았다.

### External sources

외부 출처 없음. 코퍼스 관찰과 현재 authored asset 비교만 사용했다.

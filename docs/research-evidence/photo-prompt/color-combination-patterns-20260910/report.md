# 색 조합 패턴의 시각 의미와 후보 데이터 강화 연구

색 조합 데이터는 색 이름의 목록보다 **어느 영역이 어떤 색의 역할을 맡고, 다른 영역과 어떤 관계를 이루는지**를 중심으로 강화하는 것이 적절하다. 핵심 단위는 `영역 소유자 → 색 관계 → 적용 범위 → 보존 조건 → 혼동 반례`다. 색상환 관계, 명도, 채도, 면적, 공간 배치, 조명, 그레이딩, 시간 순서를 분리하면 같은 색 조합으로도 서로 다른 촬영 의도를 표현할 수 있다.

원 대화 「색 조합 패턴 조사」의 1–15절에서 명명된 영어 패턴 용어 **150개를 66개 연구 의미군**으로 대응시켰다. 의미군은 27개 신규 세부 후보, 20개 매개변수 변형, 6개 서술형 후보, 4개 기존 데이터 재사용 검토, 1개 기존 관계 확장 검토, 2개 측정·지각 실험 항목, 6개 시퀀스 항목으로 나뉜다. 66개를 모두 독립 hard profile로 추가하라는 제안은 아니다.

근거 목록은 색채 용어 정의, 소프트웨어·장비 공식 문서, 예술가·촬영감독의 설명, 연구 초록, 원저 목차를 포함한 **27개 외부 자료**다. 각 의미군의 구성요소·반례·영문 제어 문장·픽셀 판정 조건은 이 근거를 바탕으로 작성한 **운영 설계 제안**이며 생성 성능이 검증된 규칙은 아니다. 특히 공간 배치에 관한 여러 표현은 국제 표준 용어가 아니라 현장에서 의미를 전달하는 서술어로 취급한다.

## 1. 근거의 수준과 주요 정정

원 대화는 유용한 조사 출발점이지만 그 안의 인용 식별자만으로 출처를 확인할 수는 없다. 아래 판단은 별도로 확인한 외부 자료와 현재 authored 데이터에 근거한다. 논문 3건은 검색 서비스가 제공한 초록·메타데이터 범위에 한정해 사용했으며, 전문이 필요한 효과 크기나 표본별 세부 결론은 사용하지 않았다.

Itten의 *The Elements of Color* 목차에서 일곱 색 대비를 다루는 절을 확인했다. 본문 전체를 열람한 것은 아니므로 원문을 상세 인용하지 않는다. 원 대화의 색상·명암·한난·보색·채도·면적·동시대비 축은 이번 대응표에서 모두 유지하되, 서로 배타적인 일곱 팔레트 종류나 현대 색측정의 단일 표준으로 취급하지 않는다.[^S27]

| 항목 | 구별해야 할 내용 | 데이터 반영 원칙 |
|---|---|---|
| Monochromatic / Achromatic | 한 유채색군의 변주와 무채색은 다르다. 사진에서 monochrome은 흑백까지 넓게 쓰일 수 있다. | `monochrome` 단독으로 유채색 단색·흑백·고대비를 동시에 강제하지 않는다. |
| Split complementary / Triadic | 기준색의 대향 쪽을 나눈 관계와 세 방향 균등 간격은 다른 패턴이다. | 두 의미군을 분리하고 인접 음성 사례로 교차 검사한다. |
| Tetradic / Rectangle / Square | 두 보색쌍, 직사각형 배치, 균등 사방 배치를 구별한다. | 상위 가족과 기하 변형 관계를 저장한다. |
| Double complementary / Double split complementary | 유사한 이름만으로 같은 스와치 구조라고 볼 수 없다. | 제품별 조화 규칙 이름은 제공자의 정의와 함께 보관한다. |
| Value / Lightness / Luminance | 미술의 톤 표현, 상대적 지각 밝기, 광도량을 구별한다. | 평가 지표의 이름과 색공간을 명시한다. |
| Saturation / Chroma | 일상어로 겹쳐 쓰여도 CIE 정의의 기준은 다르다. | 생성용 자연어와 측정 필드를 구분한다. |
| Warm–cool / CCT | 상대적인 따뜻함·차가움과 광원의 상관색온도는 다르다. | 임의의 유채색을 켈빈값으로 환산하지 않는다. |
| Bi-color | 장비 문맥에서는 가변 백색광, 연출 문맥에서는 두 색광을 뜻할 수 있다. | 장비명 단독으로 두 색의 화면 분할을 활성화하지 않는다. |
| Duotone / Two-color lighting | 톤을 제한 색조로 재해석하는 처리와 두 색광의 수광 관계가 다르다. | `grading`과 `illumination`에 각각 귀속한다. |
| Selective Color | Photoshop 조정 기능과 특정 영역의 색만 남기는 효과가 다르다. | 도구명 해석과 국소 색 보존 해석을 분리한다. |
| Gradient / Gradient Map | 공간 위치를 따른 변화와 명암값을 색으로 대응시키는 처리는 다르다. | 입력 축을 `spatial_path` 또는 `tone_band`로 기록한다. |
| Palette inversion | 서사상의 색 역할 반전과 이미지 음화 반전은 다르다. | 전후 프레임의 소유자 대응을 요구한다. |

Adobe의 공식 색 조합 교육은 단색·유사색·보색·삼색을 별도 조합으로 다룬다. 별도 제품 설명은 분할 보색·double split complementary·정방형을 구분한다. ColorAide의 공식 문서는 사용한 색공간에 따라 조화 계산의 결과가 달라지는 구현 사례를 제공한다.[^S06][^S07][^S08]

공식 자료도 문장 단위 검토가 필요하다. Adobe Express의 2026년 색상환 소개에는 split-complementary를 triadic과 같은 것으로 설명한 부분이 있다. 이 부분은 다른 교육 자료와 구현 문서의 구분에 맞지 않아 **정의 근거에서 제외**했다. 같은 페이지의 모든 문장을 권위만으로 채택하지 않는다.[^S09]

### 색 조화와 미적 성공의 분리

Schloss와 Palmer의 연구는 색쌍 전체에 대한 선호, 조화 판단, 배경 위 도형색의 선호를 구별한다. 따라서 보색 관계가 성립한다는 사실만으로 아름다움이나 시선 집중이 보장된다고 판정할 수 없다. 실험 색쌍에 대한 결과를 복잡한 사진 전체나 이미지 생성 모델의 성공률로 확대해서도 안 된다.[^S11]

이 원칙에 따라 `beautiful harmony`, `cinematic`, `luxurious`, `tense`는 픽셀 게이트의 정답이 아니다. 평가에서는 **의도한 색 구조가 보이는가**, **원래 피사체와 재질이 보존되는가**, **보기에 좋은가**를 별도 항목으로 둔다. 마지막 항목은 사용자 판단으로 남긴다.

### 60–30–10과 90–9–1

60–30–10은 실내 배색에서 주조색·보조색·강조색의 비중을 정하는 실무 지침으로 확인된다. 사진에 그대로 적용되는 지각 법칙이나 최적 비율이라는 근거는 확보하지 않았다. 원 대화의 90–9–1도 극단적인 면적 위계를 설명하는 예시로만 유지한다.[^S14]

사진의 일반 후보에는 `큰 기반 + 더 작은 보조 영역 + 한정된 강조 영역`을 사용한다. 숫자 비율은 명시적 요청이 있을 때만 보존하고, 전체 프레임·유채색 영역·지정 세트 면적 중 **분모**를 먼저 정해야 한다. 물체의 실제 표면적, 카메라에 투영된 면적, 시각적 주목도는 서로 같은 양이 아니다.

## 2. 현재 데이터의 강점과 부족한 연결

현재 작업 트리의 기본 authored 파일에서 직접 확인한 수량은 `color` 54개, `color_grading` 8개, `film_emulation` 18개, 기본 시각 프로필 333개다. **확장 병합 후 전체 수량은 아니다.** 확인한 파일의 해시는 [local-audit.json](local-audit.json)에 기록되어 있다.

기존 색채 연구 문서에는 표면색, 광원, 화이트밸런스, 톤 응답, 그레이딩의 구별이 이미 제안되어 있다. 이번 연구는 그 구별을 유지하면서 원 대화의 배색 패턴을 폭넓게 대응시킨다. 이전 문서의 코퍼스 빈도나 픽셀 관찰은 이번 연구에서 다시 측정한 결과로 사용하지 않는다.

| 현재 항목 | 확인한 의미와 문제 | 제안 |
|---|---|---|
| `color.monochrome` | 영문은 `high-contrast black and white`다. 단색이라는 ID에 흑백과 높은 대비가 묶여 있다. | 기존 ID 호환성을 보존하며 `chromatic_monochromatic`, `achromatic`, `contrast`를 의미상 분리한다. |
| `color.teal_orange` | 특정 두 색과 cinematic 표현이 묶여 있다. | 일반 보색 관계를 담당하는 대체 수단으로 쓰지 않는다. 실제 색 선택이 요청되었을 때만 해당 후보를 사용한다. |
| `color.cyan_magenta_split` | split이 표면 배색, 광원, 보정 중 무엇인지 불분명하다. | 소유자·효과 원인을 해석한 다음 좁은 변형으로 연결한다. |
| `color.blood_red_accent_light` | 색 슬롯 안에 조명 효과가 들어 있다. | 색광 후보가 `lighting` 차원을 침범할 수 있음을 명시적으로 관리한다. |
| `color_grading.green_summer_reflected_grade` | 반사광과 보정의 원인이 한 문장에 섞여 있다. | 관찰 가능한 반사광 관계와 그레이딩 선택을 구분한다. |
| `palette_role_hierarchy_relation` | 주조·보조·강조의 면적·위치 관계가 이미 있다. 현재 슬롯은 `color_grading`이다. | ID를 중복 추가하지 말고 표면·연출·보정 어느 경로에도 가능한 팔레트 역할로 확장할지 검토한다. |
| `selective_color_same_surface_exception_relation` | 같은 연속 표면 안의 국소 색 예외를 다룬다. | 물체 전체 하나만 색을 남기는 변형과 구별해 재사용한다. |
| `low_chroma_preserved_color_separation` | 저채도에서도 영역·재질의 작은 색 차이를 보존한다. | muted 후보의 일반 품질 관계로 재사용 가능하다. |
| `mixed_illuminant_white_balance_relation` | 방향·공간·재질·중성 기준을 포함한 혼합광 프로필이 있다. | 새로운 색온도 혼합 이름으로 중복 추가하지 않는다. |
| `high_key_tonal_distribution` | 상세한 밝은 톤 분포 의미가 있다. | 단순 흰 배경이나 노출 과다를 양성으로 취급하지 않는다. |
| `low_key_selective_illumination` | 어두운 분포 외에 선택적 조명까지 포함한다. | 어두운 팔레트 일반 요청에 선택적 조명을 무조건 추가하지 않는다. |

기존 항목에 대한 정확한 발견 위치는 `local-audit.json`의 `existing_overlap`에 있다. 색상환·색면·강조색·시퀀스 전체에 충분한 의미군이 이미 없다고 단정한 것이 아니라, 이번에 점검한 authored 색 항목과 관계 후보의 **직접 중복 및 정의 범위**를 확인한 것이다. 런타임 검색 회수율이나 현재 생성 이미지의 실패율은 측정하지 않았다.

## 3. 권장 의미 표현

### 소유자와 관찰 결과를 먼저 기록

동일한 결과색이라도 표면, 수광, 화이트밸런스, 보정 중 어느 경로로 만들어졌는지는 다를 수 있다. 생성 제어에는 의도한 경로를 기록하되 완성 픽셀만으로 실제 촬영·현상 이력을 확정하지 않는다. 한 장으로 확정할 수 없는 원인은 `unknown`으로 남겨도 된다.

다음은 연구용 중간 표현 예시다. 현행 런타임에서 그대로 읽는 스키마가 아니다.

```json
{
  "relation": "isolated_high_chroma_accent",
  "owners": {
    "base": ["background wall", "support surface"],
    "accent": ["requester-selected object"]
  },
  "effect_owner": "surface_appearance",
  "scope": "named_regions",
  "hue_relation": {"kind": "free", "wheel": null},
  "chroma_relation": "accent_greater_than_base",
  "lightness_relation": "preserve_request",
  "area_relation": {"kind": "accent_smaller_than_base", "ratio": null},
  "topology": "one_separated_accent_region",
  "protected_regions": ["requester-locked product markings"],
  "claim_limits": ["no guaranteed gaze or emotional response"]
}
```

`base`, `accent` 같은 역할과 실제 물체를 늦게 결합하면 특정 성별·의상·소품·색 이름에 고정되지 않는다. 후보가 소품을 새로 만들어야 한다면 `color` 변경만으로 처리할 수 없다. 허용된 대상·배경·구도 차원과 원래 요청을 함께 확인해야 한다.

### 색상환과 측정 색공간을 별도 필드로 유지

색상환의 기하를 직접 계산할 경우 기준을 먼저 고정한다. 원형 좌표의 회전으로 보색은 대향, 삼색은 세 방향 균등 간격, 정방형은 네 방향 균등 간격을 표현할 수 있다. 다만 전통 RYB의 각도와 sRGB 기반 HSL·OKLCH 각도를 그대로 교환하지 않는다.[^S08]

검사용 표시색은 ICC 프로파일·전달함수·백색점을 고려한 별도 수치로 기록한다. 연구 초안은 모든 입력에 특정 색상환을 몰래 적용하거나 정확한 각도 오차 한계를 강제하지 않는다. 수치 허용폭은 선택한 표현과 평가 표본에서 먼저 보정해야 한다.

### 채도와 명도는 서로 다른 비교 축

CIE는 saturation을 자기 밝기 기준, chroma를 유사하게 조명된 기준 영역에 상대적인 속성으로 설명한다. lightness 역시 유사 조명 아래의 흰 기준에 대한 상대 밝기다. 생성용 언어에서 익숙한 ‘채도’를 쓰더라도 측정 단계에서는 어떤 양을 비교하는지 별도 선언해야 한다.[^S01][^S02][^S03]

예를 들어 `Muted-on-Vivid`는 낮은 채도의 피사체와 더 강한 채도의 환경이라는 방향 관계다. 이를 단순한 muted 스타일로 축약하면 배경까지 낮은 채도로 바뀌며 원래 패턴이 사라진다. 반대로 피사체만 밝게 만들어 분리했다면 채도 대비 요청을 충족했다고 볼 수 없다.

하이키·로키·중간키는 밝은 톤·어두운 톤·중간톤 중 어디에 이미지의 분포가 집중되는지로 설명할 수 있다. 히스토그램은 이 분포를 보는 보조 수단이지만 색 영역의 위치나 피사체 소유자를 알려주지는 않는다.[^S15]

### 필수 의미와 선택적 장식을 분리

`triadic`에 세 색상군은 핵심이지만 특정 옷, 물체 셋, 균등 면적, 팝 분위기는 필수가 아니다. `color echo`의 핵심은 분리된 요소 사이 색의 반복이며 립·가방·간판이라는 소유자 목록은 하나의 예시다. `micro accent`의 핵심은 작은 비중과 목표 크기에서의 식별 가능성이지 특정 픽셀 크기가 아니다.

데이터 필드에는 `invariant`, `optional_realizations`, `parameters`, `confounders`를 구분하는 방식이 적절하다. 단, 이 명칭들은 설계 설명이며 실제 반영 시에는 현재 지원하는 의미 구성요소·후보 필드에 맞게 변환해야 한다. 검사기의 문자열 조건을 맞추기 위해 모든 프롬프트에 연구 문장을 복사하는 방식은 피한다.

## 4. 색상환 관계의 세부 설계

| 의미군 | 최소 시각 구성 | 독립적으로 선택할 축 | 주요 혼동 |
|---|---|---|---|
| 한 유채색군 | 지정 영역들의 같은 색상군 | 명도·채도 범위, 중성 예외 | 흑백, 전역 틴트 |
| 유사색 | 색상환의 인접 영역들 | 범위 폭, 지배색, 면적 | 한 색의 명도 변화 |
| 보색 | 구별되는 두 영역의 대향 색상군 | 실제 색, 비중, 표면·광원 원인 | 단순 두 색, 한난 대비 |
| 분할 보색 | 기준군 + 대향 양쪽의 두 군 | 분할 폭, 영역 소유자 | 삼색 균등 간격 |
| 삼색 | 구별되는 세 방향 색상군 | 세 색의 면적·채도, 중성 영역 | 세 개 물체, 세 광원 |
| 사색 | 두 대향쌍의 네 색상군 | 직사각형·정방형, 쌍의 위계 | 무질서한 다색 |
| 유사색 + 이탈 포인트 | 인접한 기반 + 범위 밖 한정 색군 | 포인트 위치·소유자·비중 | 전체 다색화 |

이 표의 수광·표면·면적 조건은 색상환 정의 자체가 아니라 사진 제어를 위한 제안이다. 여러 피사체가 있는 자연색 사진에서 머리·피부·식생 등 모든 픽셀을 억지로 세 색으로 바꾸면 원래 요청을 손상시킬 수 있다. `named_design_regions`와 `whole_frame_treatment`를 구분하고, 전역 듀오톤처럼 실제로 모든 색을 재해석하는 요청일 때만 전역 처리를 한다.

사색의 관계는 삼색보다 영역 식별 부담이 크다. 따라서 큰 사진에서 네 색이 모두 보이는 것과 썸네일에서 네 주요 색상군이 구분되는 것을 각각 검사한다. 연구 단계의 추가 우선순위는 용어의 유명세보다 실제 구별 가능성과 기존 데이터 결손에 둔다.

## 5. 면적·강조·반복 패턴

강조색을 표현할 때 다음 네 속성을 한 단어로 합치지 않는 것이 중요하다.

| 속성 | 질문 | 서로 구별되는 변형 |
|---|---|---|
| 색상군 수 | 강조색이 몇 계열인가 | 단일 색상군 / 여러 색상군 |
| 영역 수 | 같은 색이 몇 군데에 있는가 | 한 영역 / 반복 영역 |
| 면적 | 기반 대비 얼마나 작은가 | 지배색 / 보조색 / 작은 포인트 |
| 배치 | 어디에 어떻게 모였는가 | 고립 / 군집 / 분산 / 순서 반복 |

따라서 `Single Color Accent`와 `Repeated Accent`는 동시에 성립할 수 있다. 한 강조 색상군이 서로 떨어진 세 영역에서 반복될 수 있기 때문이다. 반면 `한 개 고립 영역`과 `여러 군집 영역`을 같은 범위의 필수 조건으로 묶으면 충돌한다.

`color echo`는 떨어진 소유자 사이 반복, `color rhythm`은 반복의 순서와 간격, `color bridge`는 다른 두 색 영역 사이의 연결 위치를 담당하게 한다. 이 세 표현을 무조건 동의어로 만들면 공간적 의미가 사라진다. 색의 공간 구성을 별도 변수로 다루는 연구와 지각색의 맥락 의존성은 이런 분해의 근거가 되지만, 이 영어 표현들이 모두 표준화된 학술 분류라는 뜻은 아니다.[^S05][^S12]

강조색의 실제 시선 효과는 얼굴·텍스트·밝기·선명도·위치와 경쟁한다. ‘강조색이 명백히 존재한다’는 구조 검사와 ‘시선이 그곳으로 갔다’는 지각 실험을 구별한다. 장면 설계 단계의 `focal color` 후보에는 전자를 쓰고 후자를 보장하지 않는다.

## 6. 공간·깊이·복잡도 패턴

`color blocking`은 큰 색면의 경계이고, `color zoning`은 이름 붙인 구역별 색의 배정이다. 색면은 평평한 배경에서도 가능하지만 구역은 상점 내부·피사체·환경 같은 의미 단위를 가질 수 있다. `color framing`은 둘러싸는 관계까지 필요하므로 단순히 피사체 옆에 색 소품 하나를 놓은 장면과 구별한다.

실제 사진가의 보정 사례에서도 큰 색면의 색을 맞추거나 대비시키는 작업이 확인된다. 다만 이는 특정 작업 방식의 사례이며 color blocking에 HSL 보정이 반드시 필요하다는 정의는 아니다.[^S25]

전경·중경·배경의 팔레트에는 색 외에 중첩·크기·지면 연결 등의 깊이 단서가 필요하다. 색이 다른 평면 세 띠만으로는 공간의 세 층을 입증하지 못한다. 대기원근에서는 원거리의 색 강도와 명암 대비 약화가 중요한 관계이며, 원경은 언제나 파랑이어야 한다는 규칙을 만들지 않는다.[^S21]

`Palette Density Contrast`는 명칭이 모호하므로 연구용으로 **유효 색상군 다양성의 범위간 차이**로 좁혀 정의한다. 배경의 잡다한 질감, 물체 수, 색상군 수, 채도는 각각 다른 양이다. 피부·직물의 미세한 톤 차이를 색상군 수로 과도하게 세지 않도록 의미 영역별 집계가 필요하다.

공간 그라디언트는 변하는 축과 경로를 함께 지정한다. 같은 물체의 좌우에서 Hue만 변하는 것, 같은 Hue의 밝기가 변하는 것, 순서 있는 여러 물체의 채도가 변하는 것은 별도 변형이다. Ombré를 의상이나 헤어에 적용하면 외형 차원도 영향을 받을 수 있으므로 색만 열린 요청에 새로운 헤어스타일을 추가하지 않는다.

## 7. 색온도·조명·그레이딩

### 상대 한난과 광원 제어

‘따뜻한 피사체 / 차가운 환경’은 상대적인 시각 관계다. 피부를 일정한 주황색으로 만드는 것과 같지 않으며, 자연스럽다는 말로 모든 피부 표현을 하나의 색으로 정규화해서도 안 된다. 보호 대상은 요청 또는 참조에서 확인된 표시 표면색과 질감으로 지정한다.

CCT는 플랑크 궤적에 가까운 광원의 색도를 설명하는 데 쓰이는 양이다. 임의의 포화 마젠타나 시안 광원을 모두 따뜻함·차가움의 켈빈 수치로 표현하면 의미가 틀어진다. amaran의 문서 역시 CCT를 조절하는 바이컬러 장비와 HSI를 다루는 RGB 제어를 구별한다.[^S04][^S16]

혼합광을 설계할 때는 `source A → receiver A`, `source B → receiver B`, `same material under both`, `white-balance anchor`를 기록한다. 광원 장비가 프레임에 반드시 보여야 하는 것은 아니다. 수광 방향·그림자·가림·표면 반응이 일관되게 보이면 연출 관계의 증거가 될 수 있지만, 실제 현장 장비·스펙트럼을 증명하지는 못한다.

### 색광별 소유 조건

| 연출 | 필요한 관계 | 피해야 할 대체 |
|---|---|---|
| 중성 주광 + 색 보조광 | 주광으로 형태가 읽히고 색 보조광은 지정 수광부에 작용 | 얼굴 전체에 임의 색 워시 |
| 색 주광 + 중성 보조광 | 색 주광과 보조광의 형태 역할이 유지 | 앞 항목과 광원 역할 뒤바꿈 |
| 색 림 | 광원 방향을 향한 윤곽 수광 | 후광 그래픽, 배경 페인트 경계 |
| 배경 워시 | 배경의 지정 범위가 빛을 받고 피사체와 스필 경계가 있음 | 장면 전체 색조 변경 |
| 교차 색광 | 분리된 방향, 수광면, 가림 경계 | 화면 좌우의 평면 필터 |

이 표는 수광 관계를 사진에서 구별하기 위한 설계안이다. 각 장면의 실제 주광·보조광 밝기 비율이나 광원 위치를 보편 숫자로 고정하지 않는다. 다색광 아래 항상 중성 피부를 요구하는 모순도 피해야 한다. 중성 주광이 닿는 보호 영역과 색광을 허용하는 영역을 따로 지정한다.

### 톤 기반 보정의 구분

Camera Raw의 Color Grading은 암부·중간톤·하이라이트를 따로 다룰 수 있다. `Three-Way`는 세 독립 제어 영역이라는 의미이며 세 영역이 반드시 서로 다른 Hue를 가져야 한다는 뜻은 아니다.[^S17]

Photoshop의 듀오톤은 원래 회색조를 복수 잉크의 곡선으로 재현하는 맥락을 가진다. 디지털 이미지 요청에서는 그와 비슷한 제한 색조 재해석을 뜻할 수도 있으므로 `print_duotone`과 `digital_duotone_look`을 구별한다. 자연색 사진에 두 가지 색 물체가 있다는 이유로 듀오톤 판정을 내리지 않는다.[^S18]

Photoshop의 Selective Color는 선택한 색 성분 안의 프로세스색을 조절하는 기능이다. 특정 물체 하나만 컬러로 남기는 효과를 요청했다면 `selective_chroma_retention` 같은 관찰 의미로 해석한다. 두 기능이 비슷한 결과를 만들 수 있어도 실제 도구 사용 이력은 픽셀만으로 확정할 수 없다.[^S19]

Gradient Map은 명암의 범위를 지정 그라디언트에 대응시킨다. 화면 좌표를 따른 그라디언트와 달리 서로 멀리 떨어져 있어도 같은 톤 조건은 동일한 매핑 규칙을 따른다. 생성 이미지에서는 원본 또는 매핑표가 없는 한 ‘이 도구를 사용했다’ 대신 ‘그런 톤-색 대응으로 보인다’고 제한한다.[^S20]

교차 현상은 지정된 것과 다른 필름 현상 공정을 쓰는 의미를 가진다. 모든 교차 현상이 같은 녹색 캐스트를 만든다는 식의 정의는 적절하지 않다. 생성 후보는 실제 공정 명칭과 구별해서 원하는 암부·중간톤·하이라이트의 색 이동을 서술해야 한다.[^S23]

## 8. 동시대비·등휘도·시간 패턴

### 동시대비

Albers의 색 연구는 주변 맥락 속에서 색이 어떻게 보이는지를 실험적으로 다룬다. 따라서 `simultaneous contrast`를 ‘서로 다른 두 색이 강하게 대비됨’과 같은 뜻으로 저장하면 본질을 놓친다.[^S10]

검증 설계는 두 단계다. 먼저 색 관리된 이미지에서 비교 자극이 같은 표시색인지 확인한다. 그다음 서로 다른 주변에서 보이는 차이를 통제된 관찰로 평가한다. 두 자극의 RGB 자체가 다르면 같은 자극의 맥락 효과라는 조건을 충족하지 않는다. 사진의 서로 다른 조명에 놓인 같은 물체색도 이 실험과 자동으로 같아지지 않는다.

자유로운 사진 생성에 즉시 적용할 hard profile보다 연구·검사용 프로필로 보관하는 편이 낫다. ‘착시처럼 보임’은 선택적 표현이 될 수 있지만 생리적 효과를 생성물 하나로 입증하지 않는다.

### 등휘도

등휘도 조건은 표시 장치와 관찰자 감도에 영향을 받는다. 관련 연구는 개인의 감도 차이에 따른 luminance match 변화를 다룬다. 그러므로 같은 HSV V, 같은 HSL L 또는 ‘비슷하게 밝아 보인다’는 설명을 곧바로 정확한 등휘도라 부르지 않는다.[^S13]

일반 사진 제어에는 ‘서로 다른 Hue, 근사하게 일치한 표시 휘도’를 사용한다. 실제 검증은 프로파일이 확인된 RGB를 선형광으로 변환한 뒤 상대 Y를 계산하고, 필요하다면 관찰자별 실험을 추가한다. sRGB·P3·전달함수의 구별은 W3C의 색공간 설명과 변환 자료를 참고할 수 있다.[^S24]

### 시퀀스

| 패턴 | 필요한 입력 | 허용할 주장 |
|---|---|---|
| Continuity | 비교 가능한 두 장면 이상 | 같은 소유자의 색 관계가 유지됨 |
| Progression / Arc | 변화 방향을 볼 수 있는 순서 표본 | 지정 축이 점진적으로 변화함 |
| Shift | 사건 전후와 전환 위치 | 선언한 경계에서 색 체계가 바뀜 |
| Inversion | 같은 소유자를 가진 전후 장면 | 대상별 색 역할이 뒤바뀜 |
| Motif | 외부에서 명시한 서사 대상과 반복 장면 | 대상과 색군의 결합이 반복됨 |
| Coding | 선언된 대상-색 대응표 | 그 대응 규칙이 유지됨 |

촬영감독 Storaro의 설명은 특정 작품에서 색을 서사에 연결한 실제 설계 사례다. 그 작품의 색 의미를 모든 사람·문화에 보편적인 감정 코드로 옮기지 않는다.[^S22] 샷간 색 일치를 다루는 소프트웨어 문서는 연속성 제어의 실무 근거를 제공하지만, 이야기의 의미까지 자동으로 증명하지 않는다.[^S26]

한 장의 후보팩에는 위 항목을 완결된 시퀀스 의미로 필수화하지 않는다. 단일 프레임은 시퀀스의 한 상태를 표현할 수 있을 뿐이다. 요청이 시리즈라면 프레임 순서, 대상의 지속성, 변화 축을 별도 상위 계획으로 관리한다.

## 9. 후보팩으로 옮기는 설계

### 데이터 층의 역할

| 층 | 보관할 내용 | 넣지 않을 내용 |
|---|---|---|
| 연구 근거 | 출처·적용 한계·용어 충돌·검토 상태 | 실행용 가중치로 꾸민 신뢰도 |
| 시각 의미 | 불변 관계·영역 소유자·혼동 경계·활성화 조건 | 특정 예시의 색·의상·성별을 전역 의무화 |
| 후보 | 짧은 시각 의미 단위·허용 차원·대안 | 출처 문장·논문 통계·반례 단어를 긍정 임베딩에 혼합 |
| 후보 조합 | 선택된 관계의 호환성·개별 범위 | 후보 선택만으로 연관 hard profile 자동 활성화 |
| 검증 | 실제 전달 의미·영역 관찰·판정 증거 | 프롬프트 PASS를 이미지 성공으로 대체 |

현재 `color`, `color_grading` 슬롯의 정책상 차원은 `color`이고, `lighting`은 `lighting`, `composition`은 `composition`이다. 따라서 연구 초안의 `affected_dimensions`는 **의미상 영향 범위**이며 현재 슬롯 정책과 반드시 그대로 호환되지는 않는다. 예컨대 색면의 위치를 바꾸는 후보는 구도에 영향을 주므로 색 슬롯 하나만으로 승격해서는 안 된다.

연구 JSON의 `schema_version`은 `photo-color-combination-research/v1`이고 `proposed_not_runtime_compatible` 상태다. 배포용 extension 스키마를 사칭하지 않는다. `source_terms`는 원 대화 용어 대응표이며 exact alias 목록이 아니다. 특히 반대 방향의 변형, 도구 이름과 결과 효과, 상위·하위 개념이 같은 행에 묶일 수 있으므로 반영 시 변형을 선택해야 한다.

### 조합 가능한 후보 예시

아래는 특정 색 이름을 고정하지 않는 조합 예시이며 성능을 입증한 최적 프롬프트가 아니다.

| 의도 | 선택할 의미 단위 | 합성 영문 예시 |
|---|---|---|
| 저채도 환경 속 한정 포인트 | 채도 대비 + 소유자 + 작은 면적 | `Keep the environment low in chroma and confine the stronger chromatic accent to the named object.` |
| 유사색 기반의 분리된 포인트 | 유사색 + 이탈 색군 + 고립 | `Build the main surfaces from neighboring hue families, with one separated accent outside that range.` |
| 색이 되풀이되는 인물과 배경 | 반복 색군 + 복수 소유자 | `Echo the garment's selected hue in a smaller, distant background element while keeping the two regions separate.` |
| 밝고 미묘한 색 층 | 밝은 톤 분포 + 톤 층 분리 | `Use a bright tonal field with small readable differences between the adjacent light surfaces.` |
| 중성 얼굴과 색 배경광 | 주광·보조광 역할 + 스필 범위 | `Keep the named front-lit facial region under a relatively neutral key and confine the colored wash to the background.` |
| 암부·밝은 톤의 색 분리 | 톤 구간 + 두 색 경향 + 보호 대상 | `Apply distinct color tendencies to shadows and highlights while retaining the requested middle-tone surface appearance.` |

`complementary + low chroma + unequal area + repeated accent`처럼 독립 축의 조합은 가능하다. 반면 같은 범위에 `achromatic`과 `high-chroma polychromatic`을 동시에 요구하거나, 같은 표면에 서로 다른 단일 강조색을 부여하면 충돌한다. 충돌은 문자열상의 단어 공존이 아니라 **같은 소유자·같은 범위·같은 축·같은 시점**에서 판정해야 한다.

[candidate-bundles.research.json](candidate-bundles.research.json)에는 이 원칙을 적용한 **8개 조합 초안**을 별도로 제공한다. 각각 실제 연구 후보 ID, 공유해야 할 소유자·범위 관계, 영향 차원을 연결하며 고정 색·가중치·자동 hard 활성화는 넣지 않았다. 기존 런타임 bundle 스키마로 사용하려면 별도 변환과 검증이 필요하다.

## 10. 보강 순서

**첫 단계는 기존 혼동을 정리하고 12개 핵심 관계부터 검증하는 것**이다. 이는 예상 사용 빈도를 측정한 순위가 아니라 정의 명료성, 기존 의미 결손, 사진에서 확인할 수 있는 정도를 기준으로 한 연구 판단이다.

| 순서 | 후보군 | 이유 |
|---|---|---|
| 1 | 유채색 단색 / 무채색의 분리 | 현재 monochrome의 대비·흑백 결합을 분해 |
| 2 | 유사색 / 보색 / 분할 보색 / 삼색 | 원 대화의 기본 색상환 패턴을 각각 관찰 가능하게 만듦 |
| 3 | 단일 강조색 / 영역간 채도 대비 | 색 이름을 고정하지 않고 역할을 표현 |
| 4 | 색 반복 / 큰 색면 | 히스토그램만으로 놓치는 공간 관계를 보강 |
| 5 | split toning / Gradient Map | 조명·공간 그라디언트와의 혼동을 정리 |

그와 함께 기존의 팔레트 역할 위계, 저채도 색 분리, 혼합광, 하이키는 동일 의미가 필요할 때 재사용한다. 로키 선택 조명과 같은 표면 선택색은 기존 프로필의 더 좁은 의미를 보존한다.

두 번째 단계에는 사색·정방형, 군집·분산·리듬, 색 프레이밍, 공간의 색상군 복잡도, 주광·보조광·림·워시를 포함한다. 이들은 더 많은 영역 또는 원인 관계를 요구하므로 첫 단계에서 영역 소유자와 평가 방식을 안정시킨 뒤 추가하는 것이 낫다.

세 번째 단계는 동시대비·등휘도와 시퀀스 패턴이다. 필요한 입력·측정 체계가 일반 사진 한 장의 검증과 다르므로 별도의 자격 검증을 거친다. 창작자는 이 표현들을 자유롭게 사용할 수 있지만 시스템은 검증하지 않은 물리·지각·서사 결과를 통과로 표시하지 않아야 한다.

## 11. 검증 설계

### 라우팅과 전달

`regression-cases.json`에는 양성 의미와 가까운 반례 또는 방향 역전을 짝지은 **36개 미실행 검토 사례**가 있다. 양성에 해당 의미가 드러나고 음성에서 같은 좁은 의미가 잘못 활성화되지 않는지 확인하는 것이 목적이다. 문자열을 새 규칙에 맞춰 바꾸는 것으로 통과시켜서는 안 된다.

필요한 검사 범위는 다음과 같다.

1. 정확한 요청, 한·영 패러프레이즈, 부정 표현, 도구·장비 문맥을 각각 확인한다.
2. 검색된 advisory 후보와 명시적 요청에서 비롯된 hard 의미를 구분한다.
3. 사용자가 고정한 실제 색·소유자·방향을 후보가 덮어쓰지 않는지 확인한다.
4. 후보팩과 축약 뷰에서 비교 방향·면적 위계·소유자가 사라지지 않는지 확인한다.
5. 연구 출처·반례·주장 제한이 긍정 검색용 문장에 섞이지 않는지 확인한다.
6. 실제 사용하는 extension·시각 registry·인덱스·해시 계약을 반영 후 재검증한다.

### 픽셀 관찰과 측정

| 검사 대상 | 관찰 단위 | 보조 측정 | 실패 또는 미판정 예 |
|---|---|---|---|
| Hue 관계 | 이름 붙인 의미 영역 | 색공간·색상환이 선언된 대표색과 분포 | 저채도 노이즈의 Hue를 주요 색으로 셈 |
| Chroma 관계 | 같은 소유자의 비교 가능한 면 | 영역별 chroma 분포 | 밝기를 채도라고 오인 |
| 명도 관계 | 피사체·배경의 지정 범위 | 선형광 Y 또는 선언된 L 계열 | 색공간을 모른 채 숫자를 비교 |
| 면적 관계 | 겹치지 않는 영역 마스크 | 분모가 명시된 투영 면적 | 3D 표면적과 화면 점유를 혼합 |
| 반복·고립 | 연결 성분과 의미 소유자 | 위치·영역 수·분리 거리 | 같은 히스토그램이니 같은 패턴이라 판정 |
| 조명 관계 | 수광면·가림·그림자 | 같은 재질의 서로 다른 수광 영역 | 페인트색을 색광으로 단정 |
| 톤 기반 처리 | 암부·중간톤·밝은 톤 | 톤 구간별 색 경향 | 좌우 배치만으로 split tone 판정 |
| 시퀀스 | 순서 있는 프레임의 같은 대상 | 소유자별 관계 변화 | 정지 이미지 한 장으로 arc 통과 |

마스크는 피부·의상·배경 같은 요청상 의미 단위를 기준으로 만들고, 반사·하이라이트·그림자의 포함 여부를 기록한다. 금속·유리·젖은 표면은 같은 물체 안에서도 다른 광원을 반사할 수 있으므로 대표색 한 점만으로 정의를 판정하지 않는다. 무채색 부근에서는 색상각이 불안정하므로 명도·채도와 함께 평가한다.

Hue 오차 몇 도, 강조 면적 몇 퍼센트 같은 전역 통과 기준은 이번 연구에서 정하지 않았다. 기준을 정하려면 색공간, 분할 방식, 목표 출력 크기, 사진의 재질·조명 변형을 포함한 양성·반례 표본에서 먼저 보정해야 한다. 숫자가 있다는 이유로 시각 의미가 객관적으로 검증되는 것은 아니다.

### 비교 렌더 계획

한정된 핵심 의미군부터 다음 세 조건을 비교하는 것이 적절하다.

| 조건 | 제어 내용 | 확인할 질문 |
|---|---|---|
| A | 기존 데이터와 현재 방식 | 원래 패턴이 어느 정도 표현되는가 |
| B | 새 관계 후보를 선택적으로 제공 | 후보가 의미를 더 분명하게 전달하는가 |
| C | 명시적 요청에 대응한 세부 시각 계약 | 강화가 요청 충실도를 높이며 다른 요소를 손상하지 않는가 |

대상·구도·조명·모델 설정을 가능한 범위에서 맞추고 참조 이미지 유무와 난수 제어 가능 여부를 기록한다. 하나의 렌더로 일반적 향상이나 인과관계를 주장하지 않는다. 인물·제품·실내/자연 공간에서 색군, 소유자, 면적, 광원 방향을 바꾼 추가 사례로 특정 예시에 대한 과적합을 점검한다.

각 결과는 프롬프트 감사, 런타임 전달, 실제 픽셀, 미적 판단으로 나눠 기록한다. 필수 관계가 일부만 보이면 의미 검증에서는 실패로 처리하고, 이미지가 없거나 원인이 판별되지 않으면 미판정으로 남긴다. 재시도는 원본 실패를 보존하며 이전 이미지와 근거 파일을 덮어쓰지 않는다.

## 12. 산출물과 적용 상태

| 파일 | 내용 |
|---|---|
| [pattern-catalog.md](pattern-catalog.md) | 66개 의미군의 개별 설명·관찰 조건·반례·영문 제어 문장·근거 |
| [candidate-research.json](candidate-research.json) | 같은 의미군의 구조화 초안, 활성화 제안, 영향 차원, 픽셀 게이트 |
| [candidate-bundles.research.json](candidate-bundles.research.json) | 소유자·범위를 공유하는 8개 후보 조합 설계 |
| [keyword-coverage.json](keyword-coverage.json) | 원 대화 150개 명명 용어와 의미군의 대응 |
| [sources.json](sources.json) | 27개 출처의 제목·발행 주체·날짜·지원 주장·접근 한계 |
| [local-audit.json](local-audit.json) | 현재 기본 데이터 수량·기존 ID 대응·소스 파일 해시 |
| [regression-cases.json](regression-cases.json) | 양성·인접 반례 36쌍의 미실행 검토 설계 |
| [validation.json](validation.json) | 연구 산출물의 구조 검사와 미실행 검증 단계 |
| [source-conversation.json](source-conversation.json) | 원 대화에서 제공받은 범위의 입력 근거 |
| [build_research.py](build_research.py) | 이 디렉터리의 JSON·카탈로그를 재구성하는 도구 |

연구 파일의 ID·출처 연결·구성요소·반례·원 대화 용어 존재·기존 ID 참조를 검사했다. 현재 런타임 데이터 반영, 임베딩 재생성, 실제 후보팩 생성, 모델 렌더, 픽셀 리뷰는 수행하지 않았다. 기존 작업 트리에 있던 변경은 이 연구의 구현 결과에 포함하지 않는다.

## 출처

아래 주석은 주장 옆의 번호와 연결된다. 발행일을 확인하지 못한 웹페이지는 추정 날짜를 쓰지 않았다. 모든 외부 자료의 확인일은 2026-09-10이다.

[^S01]: CIE. [Saturation, e-ILV 17-22-073](https://cie.co.at/eilvterm/17-22-073). CIE S 017:2020, 2020-12.
[^S02]: CIE. [Chroma, e-ILV 17-22-074](https://cie.co.at/eilvterm/17-22-074). CIE S 017:2020, 2020-12.
[^S03]: CIE. [Lightness, e-ILV 17-22-063](https://cie.co.at/eilvterm/17-22-063). CIE S 017:2020, 2020-12.
[^S04]: CIE. [Correlated colour temperature, e-ILV 17-23-068](https://cie.co.at/eilvterm/17-23-068). CIE S 017:2020, 2020-12.
[^S05]: CIE. [Perceived colour, e-ILV 17-22-040](https://www.cie.co.at/eilvterm/17-22-040). CIE S 017:2020, 2020-12.
[^S06]: Adobe, instruction by Vanessa Eckstein. [Color combinations in design](https://helpx.adobe.com/in_hi/illustrator/how-to/experiment-with-color-combinations-hybrid.html). 발행일 미확인.
[^S07]: Hep Svadja, Adobe. [Color Your Spring with Adobe Color Gradients](https://blog.adobe.com/en/publish/2020/04/27/color-your-spring-with-adobe-color-gradients). 2020-04-27.
[^S08]: ColorAide project. [Color Harmonies](https://facelessuser.github.io/coloraide/harmonies/). 발행일 미표시. 구현 관례와 색공간 비교의 근거이며 색채 조화의 국제 표준으로 취급하지 않음.
[^S09]: Adobe Express. [The color wheel explained and how colors work together](https://www.adobe.com/express/learn/blog/color-wheel-explained). 2026-05-28. 본문의 분할 보색·삼색 혼동을 확인하여 해당 설명은 제외.
[^S10]: Josef and Anni Albers Foundation. [Interaction of Color](https://www.albersfoundation.org/alberses/teaching/interaction-of-color). 웹 발행일 미표시. 1963년 저작과 교육적 접근을 설명하는 재단 자료.
[^S11]: Karen B. Schloss and Stephen E. Palmer. [Aesthetic response to color combinations: preference, harmony, and similarity](https://pubmed.ncbi.nlm.nih.gov/21264737/). *Attention, Perception, & Psychophysics* 73, 551–571, 2011; 온라인 2010-11-10. DOI 10.3758/s13414-010-0027-0. 색쌍 연구 초록 범위 사용.
[^S12]: Karen B. Schloss and Stephen E. Palmer. [The role of spatial organization in preference for color pairs](https://pubmed.ncbi.nlm.nih.gov/22208128/). *Perception* 40(9), 1063–1080, 2011. DOI 10.1068/p6992. 메타데이터·초록 범위 사용.
[^S13]: Kassandra R. Lee, Alex J. Richardson, Eric Walowit, Michael A. Crognale, and Michael A. Webster. [Predicting color matches from luminance matches](https://opg.optica.org/abstract.cfm?uri=josaa-37-4-A35). *Journal of the Optical Society of America A* 37, A35–A43, 2020; 온라인 2020-02-14. DOI 10.1364/JOSAA.381256. 초록 범위 사용.
[^S14]: Sherwin-Williams. [How to Build a Color Palette in 5 Simple Steps](https://blog.sherwin-williams.com/color/color-guidance/how-to-build-a-color-palette-in-5-simple-steps/). 발행일 미확인. 실내 배색 지침.
[^S15]: Adobe. [View histograms and pixel values in Photoshop](https://helpx.adobe.com/photoshop/using/viewing-histograms-pixel-values.html). 2023-05-24.
[^S16]: amaran. [Controlling Devices, Desktop App](https://help.amarancreators.com/en/amaran-desktop-app/controlling-devices). 발행일 미표시.
[^S17]: Adobe. [Make color and tonal adjustments in Adobe Camera Raw](https://helpx.adobe.com/camera-raw/desktop/using/make-color-tonal-adjustments-camera.html). 2026-08 업데이트로 검색됨; 일자 미확인.
[^S18]: Adobe. [Duotones](https://helpx.adobe.com/uk/photoshop/using/duotones.html). 2022-09-14.
[^S19]: Adobe. [Make selective color adjustments](https://helpx.adobe.com/photoshop/using/mix-colors.html). 2023-05-24.
[^S20]: Adobe. [Apply special color effects in Photoshop](https://helpx.adobe.com/photoshop/using/applying-special-color-effects-images.html). 2023-05-24.
[^S21]: Getty Museum Education. [Landscapes, Classical to Modern Curriculum: Background Information](https://www.getty.edu/education/for_teachers/curricula/landscapes/background2.html). 발행일 미표시.
[^S22]: Vittorio Storaro, American Society of Cinematographers. [Wonder Wheel: Who’s Afraid of Red, Green and Blue?](https://theasc.com/article/whos-afraid-of-red-green-and-blue/). 발행일 미확인. 작품별 촬영 설계의 1차 설명.
[^S23]: Lomography. [What is cross processing?](https://www.lomography.com/school/what-is-cross-processing-fa-bne2kolj). 발행일 미확인.
[^S24]: W3C CSS Working Group. [CSS Color Module Level 4](https://www.w3.org/TR/2026/CRD-css-color-4-20260908/). 2026-09-08 Candidate Recommendation Draft. 색 관리와 변환의 기술 근거이며 사진의 미적 평가 기준은 아님.
[^S25]: Adobe, Jonpaul Douglass 등 사진가 인터뷰. [One Tool, Three Ways: HSL Panel in Lightroom Classic CC](https://blog.adobe.com/en/publish/2018/07/18/one-tool-three-ways-hsl-panel-in-lightroom-classic-cc). 2018-07-18.
[^S26]: Adobe. [Color correction workflow in Premiere](https://helpx.adobe.com/premiere/desktop/correct-color/color-correction-fundamentals/color-correction-workflow.html). 2026-01-07.
[^S27]: Johannes Itten, edited by Faber Birren. [The Elements of Color](https://books.google.com/books/about/The_Elements_of_Color.html?id=ofvRhNBgoCoC). John Wiley & Sons, 1970. 서지와 목차만 사용.

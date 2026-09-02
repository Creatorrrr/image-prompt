# 04. 조명 기하·노출·그림자 소유·필·림·재질 반응

## 결론

**결정: `proposed`**

신규 ReactorPrompt 코퍼스는 조명 후보를 더 많은 분위기·장르 이름으로 늘리기보다 다음의 인과 사슬로 재구성할 근거를 제공한다.

```text
광원/발광체
-> 피사체 기준 입사 방향과 겉보기 크기
-> 차폐·유출·거리 감쇠
-> 키/필/반사/감산/분리 역할
-> 프레임과 영역별 노출·톤 응답
-> 재질별 확산·정반사·투과 응답
-> 대기/렌즈/후처리의 2차 광학 응답
```

프롬프트 924건 중 조명 결과를 가리키는 표현은 856건에서 발견됐지만, 이 연구가 정의한 6개 핵심 인과축을 모두 양성 문맥에서 함께 명시한 프롬프트는 3건뿐이었다. 반대로 `cinematic lighting` 같은 포괄 라벨만 있고 5개 선행 인과축이 없는 프롬프트는 54건이었다. 20개 게시물 40장 표본에서는 양성 게시물 17개의 34장 모두 적어도 하나의 큰 조명 단서는 재현했으나, 7개 게시물에서는 지정된 세부 광원·필·플래시·색 반사 중 하나 이상을 픽셀에서 따로 소유시키거나 검증할 수 없었다. 따라서 **스타일 라벨은 선택적 요약으로만 남기고, 실제 후보 데이터와 검토 게이트는 광원-그림자-필-노출-재질 관계를 소유해야 한다.**

이 문서는 연구·설계 결과이며 런타임 자산, 색인, 테스트, 생성 이미지를 변경하지 않았다. 후보팩 동작, 새 하드 프로필, 독립 렌더 자격, 요청자 판단은 모두 미검증이다.

## 범위와 표본 방법

### 고정 근거

- 코퍼스: `generated/reactorprompt-export-20260902-incremental/manifest.json`
- 범위: 게시물 1,182개, 이미지 4,908장, 비어 있지 않은 프롬프트 924개, 게시물 ID 1565–2746
- 런타임 기준: `skills/photo-prompt-image-generator` Git revision `8380c8aa0a3e501aaf5bb29fd3ca79c8896ddfab`
- 증거층은 다음처럼 분리했다.
  - **프롬프트 관찰:** manifest의 텍스트 전수 스캔
  - **코퍼스 픽셀 관찰:** 저장된 이미지 표본의 썸네일 및 원본 크기 검토
  - **패키지 관찰:** 현재 authored asset과 계약 파일 검토
  - **외부 기전 근거:** ARRI와 PBRT의 1차/권위 기술 자료
  - **사용자 판단:** 없음

### 프롬프트 전수 스캔

`manifest.json`에서 `prompt.strip()`이 비어 있지 않은 924개를 모두 읽었다. 대소문자를 무시한 정규식으로 아래 축을 계수했다. `positive-context`는 문장 또는 줄 앞부분 80자 안에 `no`, `avoid`, `without`, `negative prompt`, `--no`, `do not`, `never`가 있는 세그먼트를 제거한 휴리스틱이며, 문법 분석 결과가 아니다. 따라서 raw/positive 수치는 **프롬프트 측 탐색 증거**일 뿐 의미 정답이나 픽셀 빈도가 아니다.

### 픽셀 표본

전수 스캔의 축별 매치 목록을 ID 오름차순으로 정렬하고 각 목록에서 약 8등분 지점 후보를 출력했다. 그 후보에서 초기·중기·후기 ID와 다음 현상을 고르게 포함하도록 17개 양성 게시물을 목적 표집했다.

- 큰/작은 광원과 그림자 전이
- 창·태양·네온·플래시처럼 위치를 추적할 수 있는 광원
- 백라이트·림·필·반사광
- 국소 차폐 패턴
- 저조도·하이라이트 롤오프
- 금속·유리·젖은 표면·직물·꽃잎의 재질 반응
- 혼합 색광

여기에 광원 인과가 없거나 매우 포괄적인 3개 대조 게시물을 더했다. 게시물마다 `_01`, `_02` 두 이미지를 열어 **20개 게시물 40장**을 썸네일 스케일에서 비교했고, 그중 양성 12개 게시물의 첫 이미지와 대조 2개 게시물의 두 이미지씩, 총 **16장**을 원본 크기로 다시 열어 미세 그림자·모공·반사·투과·직물/꽃잎 디테일을 확인했다. 표본 비율을 4,908장 전체의 빈도로 일반화하지 않는다.

## 프롬프트 측 발견과 계수

### 축별 매치

| 탐색 축 | raw 프롬프트 | positive-context | 해석 경계 |
|---|---:|---:|---|
| 조명 결과 일반 (`light`, `sunlight`, `flash`, `shadow`, `highlight` 등) | 856 | 849 | 장면이 밝다는 말부터 구체 광원까지 혼합 |
| 광원 겉보기 크기·경연성 | 341 | 333 | `soft`가 항상 큰 광원을 뜻하는 것은 아님 |
| 입사 방향·기하 | 149 | 147 | 좌우·상하·전후·림·백라이트 표현 |
| 보이는/명명된 광원 | 436 | 419 | 태양·창·네온·램프·형광등 등; 보인다는 뜻은 아님 |
| 필·바운스·감산 | 116 | 111 | 광량비는 대부분 정량 불가 |
| 그림자 소유·경계 전이 | 84 | 81 | cast/contact/dappled/penumbra/falloff 계열 |
| 노출·톤 응답 | 209 | 170 | 부정 프롬프트에서 `overexposure`, `crushed shadows`가 많이 제거됨 |
| 림·에지 분리 | 93 | 91 | 단순 후광과 실제 후방광을 구분해야 함 |
| 재질 반응 | 615 | 610 | 재질명 자체와 조명에 의한 반응이 섞임 |
| 혼합/색 광원 구역 | 110 | 93 | 전체 그레이드와 공간적 색광을 구분해야 함 |
| 대기·광학 응답 | 201 | 193 | haze/bloom/halation/glow가 서로 혼동될 수 있음 |
| 명명된 인물 조명 패턴 | 1 | 1 | Rembrandt, butterfly, clamshell 등 명시적 패턴 |
| 플래시 | 132 | 103 | 캡처 장치명만으로 픽셀 서명이 완성되지는 않음 |
| 숫자 CCT/lux/watt 등 정확 계측 주장 | 9 | 9 | 픽셀만으로 확인할 수 없는 입력 주장 |

축별 정규식은 부록에 기록했다. `material response`의 높은 수치는 `glossy`, `matte`, `glass`, `translucent` 같은 재질 단어가 포함된 결과이므로, 조명이 그 표면에 실제로 어떤 하이라이트 형태를 만들었는지와 동일하지 않다.

### 6개 인과축 동시 커버리지

여기서 핵심 6축은 `광원 크기/경연성`, `입사 방향`, `필/바운스/감산`, `그림자 소유/전이`, `노출/톤`, `재질 반응`이다.

| 양성 문맥에서 함께 잡힌 축 수 | 프롬프트 수 |
|---:|---:|
| 0 | 171 |
| 1 | 322 |
| 2 | 251 |
| 3 | 114 |
| 4 | 47 |
| 5 | 16 |
| 6 | 3 |

이 표는 “축이 많을수록 좋은 프롬프트”라는 평가가 아니다. 장면에 필요 없는 축을 강제해서는 안 된다. 다만 스타일 라벨이 이미 구체 조명 설계라고 간주되거나, 한 축의 후보가 다른 축의 결과를 암묵적으로 채우는 현재 구조를 경계할 근거다.

### 프롬프트에서 반복된 유용한 관계

- **광원과 차폐가 함께 있는 표현:** `upper-left/front hard sunlight` + `shadow beneath fringe`, `leafy shadows across blanket and body`, `narrow slatted window beam`처럼 소스 방향과 수신면이 연결된 프롬프트가 픽셀 검토에 가장 유리했다.
- **필의 목적이 적힌 표현:** `frontal fill keeps inner folds visible`, `cool ambient fill keeps skin natural`처럼 필이 열어야 할 영역을 적으면 단순 “밝게”보다 검토 가능성이 높아졌다.
- **재질별 효과가 적힌 표현:** 젖은 바닥의 반사, 꽃잎의 넓은 그라데이션과 가장자리 투과, 금속/유리의 작은 반사처럼 수신 재질과 하이라이트 형태가 연결된 표현이 유용했다.
- **불필요하게 정확한 장비·수치:** `5600K ring softbox`, `4300K fill`은 픽셀에서 고키 정면광은 볼 수 있어도 정확 CCT와 장비 조합을 입증할 수 없다.
- **스타일 라벨 단독:** `bright soft lighting`, `cinematic lighting`은 생성 결과가 그럴듯해도 방향·필·그림자 소유를 고정하지 못한다.

## 픽셀 측 관찰과 표본 ID

아래 평가는 저장된 코퍼스 픽셀에만 해당한다. 프롬프트와 비슷해 보인다고 해서 해당 문구가 생성 원인이라는 뜻은 아니다.

| 게시물 | 검사 이미지 | 프롬프트 측 조명 약속 | 관찰된 픽셀 | 정렬/혼동 경계 |
|---|---|---|---|---|
| 1569 | 01, 02 | 측면의 따뜻한 햇빛, 차가운 그림자, 광택 자동차와 젖은 바닥 반사 | 창과 광선 방향, 젖은 바닥의 넓고 끊긴 반사, 차체의 작은 정반사가 함께 보임 | 큰 관계는 정렬. 얼굴 앞면을 여는 2차 필은 문구에서 소유되지 않음 |
| 1603 | 01, 02 | 밝은 창, airy backlight, soft shadows | 창이 장면 뒤/옆의 큰 광원으로 읽히고 그림자 전이는 부드러움 | 강한 림보다 전면이 고르게 밝음. 얼굴 필 또는 실내 반사를 따로 소유하지 않음 |
| 1772 | 01, 02 | direct flash, sharp flash highlights | 카메라축의 평평한 밝기와 피부·입술의 작은 핫스팟이 보임 | 가까운 뒤쪽 표면의 뚜렷한 플래시 그림자는 없어 현재 `direct_on_camera_flash` 하드 게이트 전체는 충족했다고 볼 수 없음 |
| 1840 | 01, 02 | 강한 창 백라이트, phone flare, hair/shoulder rim, 과노출 | 창 코어가 매우 밝고 머리·어깨 외곽과 먼지/플레어가 보임 | 전면 피부가 예상보다 읽혀 숨은 필/HDR/노출 복구가 개입한 듯 보이나 원인은 확정 불가 |
| 1953 | 01, 02 | purple/magenta LED + soft frontal fill | 방의 색광이 배경과 머리 가장자리까지 이어지고 얼굴은 비교적 중립적 정면광 | 색광 구역과 필의 역할은 대체로 분리되나 실제 LED 위치는 보이지 않음 |
| 2123 | 01, 02 | direct phone flash, hard local shadows, crushed background | 가까운 인물이 갑자기 밝고 배경이 급격히 어두워지며 턱·손가락·다리 아래 단단한 그림자가 보임 | 양성 대표. 전면 핫스팟, 근원거리 감쇠, 일부 환경 보존이 함께 읽힘 |
| 2149 | 01, 02 | 5600K ring softbox + 4300K side fill, high key | 넓은 고키 정면광, 열린 그림자, 백색 배경이 보임 | `5600K`, `4300K`, ring/softbox 장비 조합은 픽셀로 확인 불가. 효과와 장비 주장을 분리해야 함 |
| 2200 | 01, 02 | 강한 직사광과 몸/담요 위 굵은 잎 그림자 | 잎 모양의 경계가 얼굴·몸·체크 담요를 가로지르며 같은 방향과 투영 크기를 유지 | 강한 양성. 전역 대비나 프린트 무늬로 대체되지 않음 |
| 2262 | 01, 02 | harsh midday sun + direct flash | 푸른 들판의 강한 직사광, 밝은 인물, 단단한 형태 대비가 보임 | 플래시 효과를 개방 하늘 필과 분리하기 어려움. “플래시가 있었다”는 장비 주장은 미검증 |
| 2299 | 01, 02 | 흐린 빛이 온실 유리를 통과, 상단/좌측이 밝고 부드러운 롤오프 | 큰 유리 지붕 방향, 부드러운 얼굴 모델링, 유리·잎·안경의 서로 다른 반사가 보임 | 큰 관계 정렬. 필름/할레이션은 원본에서도 약해 독립 효과로 단정하지 않음 |
| 2467 | 01, 02 | 좁은 slatted window beam이 눈/코를 가로지름, 나머지는 soft shadow, warm bounce | 눈을 지나는 밝은 수평 띠와 어두운 상하 영역, 커튼/창 쪽 수신 흔적이 일관됨 | 강한 양성. 단순 얼굴 보정이나 전체 밝기 차이로 대체되지 않음 |
| 2552 | 01, 02 | 약한 on-camera fill flash + 좌측의 넓은 실내광, 턱/소파의 얕은 그림자 | 밝고 부드러운 실내광, 소파 접촉 그림자와 약한 얼굴 그림자 | 별도 플래시 방향/핫스팟이 명확하지 않아 큰 확산광만으로도 설명 가능 |
| 2564 | 01, 02 | upper-left strong directional studio light, deep controlled shadows | 코·턱·목의 방향성 그림자, 검은 재킷의 세부, 백색 배경과 선택적 빨강이 유지 | 강한 양성. 어두운 의상만으로 생긴 검정 덩어리가 아니라 얼굴 형태가 조명으로 모델링됨 |
| 2608 | 01, 02 | direct frontal flash + red neon, wet/glass reflections | 중립에 가까운 전면 얼굴과 붉은 머리 림, 네온 창·젖은 노면의 붉은 반사가 분리 | 강한 양성. 전체 빨강 LUT만이 아니라 실제 구역·수신면 관계가 보임 |
| 2626 | 01, 02 | upper-left large soft key + narrow rim + weak frontal fill | 꽃잎의 넓은 확산 그라데이션, 가장자리 밝기, 안쪽 접힌 면의 세부, 검은 배경이 동시에 유지 | 비인물 양성. 꽃잎 재질과 광원 크기·필 역할이 함께 읽힘 |
| 2683 | 01, 02 | cinematic side-backlight + strong soft rim | 머리·어깨 뒤쪽의 선택적 밝은 외곽과 읽히는 얼굴 형태 | 큰 관계 정렬. `cinematic` 자체가 기전을 설명하지 않으며 장비는 추론할 수 없음 |
| 2741 | 01, 02 | upper-left/front hard late-afternoon sun, fringe/jaw shadow, restrained cyan bounce | 코·턱·머리의 단단한 방향성 그림자와 작은 밝은 하이라이트가 보임 | 큰 관계 정렬. 피부 위 cyan bounce는 매우 절제되어 별도 색 필로 확정하기 어려움 |
| 1587 (대조) | 01, 02 | `bright soft lighting`만 있음 | 과장된 초광각 교실 장면에 고른 주변광이 생기지만 광원 역할·방향은 약함 | 포괄 라벨이 구체 인과를 소유하지 못하는 대조 |
| 1595 (대조) | 01, 02 | 명시적 조명 기전 없음 | 두 이미지 모두 부드러운 정면 스튜디오광처럼 보임 | 결과가 그럴듯해도 프롬프트 의무나 후보 기본값의 근거가 되지 않음 |
| 2554 (대조) | 01, 02 | 명시적 조명 기전 없음 | 창 옆의 강한 측/후방 일광, 투명 소매·레이스·금속 귀걸이의 반응이 보임 | 장면 맥락에서 모델이 만든 조명일 수 있으나 요청된 조명 의미라고 역추론하면 안 됨 |

표본 내 양성 34장은 모두 큰 조명 단서 하나 이상을 보존했다. 그러나 1603, 1772, 1840, 2149, 2262, 2552, 2741의 7개 게시물에서는 세부 광원·필·플래시·색 반사 중 하나 이상이 독립적으로 보이지 않거나, 다른 기전으로도 설명 가능했다. 이것은 `partial_is_fail`을 적용해야 하는 하드 프로필 평가와 “큰 분위기는 비슷하다”는 일반 관찰을 분리해야 함을 보여준다.

## 프롬프트/픽셀 정렬과 발산

### 정렬이 강했던 조건

1. **광원 방향과 수신면을 같은 문장에 묶었을 때**: 2200의 잎 그림자, 2467의 슬릿광, 2741의 머리/턱 그림자처럼 무엇이 어디에 떨어지는지 검토할 수 있었다.
2. **주광과 필의 역할을 다른 영역으로 나눴을 때**: 2608은 전면 플래시와 붉은 네온 구역, 2626은 꽃잎 주광·에지·내부 필을 구분할 수 있었다.
3. **재질명 대신 하이라이트 형태를 연결했을 때**: 1569의 차체/젖은 바닥, 2299의 유리/안경/잎, 2626의 꽃잎은 같은 빛에 서로 다른 반응을 보였다.
4. **노출 목표가 국소적일 때**: “눈은 읽히되 배경은 어둡게”, “검은 배경은 들지 않되 내부 꽃잎은 보이게” 같은 관계는 `balanced exposure`보다 검토 가능했다.

### 발산과 혼동

- **숨은 필:** 백라이트 장면에서 얼굴이 읽히는 것은 필, 바운스, HDR/톤 매핑, 생성기의 미적 보정 중 무엇 때문인지 픽셀만으로 구분할 수 없다.
- **장비명 과잉 주장:** ring softbox, 정확 CCT, full-power flash는 픽셀 결과만으로 확인할 수 없다. 보이는 효과와 장비 메타데이터를 분리해야 한다.
- **플래시 두 종류의 혼동:** 야간 직접 플래시는 근거리 밝기·핫스팟·뒤쪽 그림자·거리 감쇠가 핵심이지만, 일광 필 플래시는 기존 태양 그림자를 약화하면서 환경 노출을 유지한다. 현재 하나의 `direct_on_camera_flash_snapshot_signature`로 둘을 처리하면 잘못된 게이트를 강제한다.
- **림과 후광의 혼동:** 실제 림은 후방 방향, 선택적 실제 윤곽, 읽히는 전면 형태, 배경 분리를 함께 가져야 한다. 균일 AI 컷아웃 광륜이나 bloom은 대체가 아니다.
- **노출과 광량의 혼동:** `light_intensity` 안에 고키/로키, 클리핑, bloom, 거리 감쇠가 함께 있어 원인과 결과가 섞여 있다.
- **재질과 조명의 혼동:** `glossy`, `matte`, `translucent`는 고유 재질 속성이고, 하이라이트 폭·방향·투과 에지는 조명과 관찰 방향이 만든 결과다.
- **색광과 그레이드의 혼동:** 2608처럼 광원이 특정 표면과 젖은 바닥에 연결될 때만 source-owned colored light로 보아야 한다. 전역 teal/orange 또는 red LUT는 대체가 아니다.

## 기존 데이터 중복과 소유층

### 현재 authored source의 강점

1. `photo_prompt_lighting_extension.json`
   - 12개 cross-slot 조명 클러스터가 있다.
   - 각 클러스터는 `lighting`, `light_direction`, `light_type`, `light_intensity`, `light_shape`, `color`를 하나씩 연결하고, `color_grading` 11개와 `film_emulation` 1개를 더한다.
   - `semantic_policy.visual_actuation`은 조명·방향·광원 유형·상대 강도·형태·색·마감을 일관된 시스템으로 유지하라고 이미 요구한다.
   - `claim_boundary`는 픽셀로 fixture brand, wattage, lux, exact ratio, CCT, CRI/TLCI/SSI, SPD를 확정하지 못한다고 이미 올바르게 제한한다.

2. `photo_prompt_visual_obligations.json`
   - 조명/톤/광학과 직접 관련된 좁은 프로필은 29개다.
   - 이미 존재하는 중요한 인과 프로필: `hard_light_shadow_edge_relation`, `soft_light_shadow_edge_relation`, `key_fill_separation_background_roles`, `negative_fill_shadow_deepening_relation`, `backlit_rim_edge_separation_relation`, `direct_on_camera_flash_snapshot_signature`, `motivated_practical_mixed_interior_relation`, `highlight_rolloff_tone_response`, `chiaroscuro_form_modeling_relation`, `volumetric_occluded_light_shafts`, `film_halation_highlight_edge_relation`, `glass_skin_specular_diffuse_balance`.
   - 이 프로필들은 혼동 대체물과 thumbnail/both/native 게이트를 이미 가진다. 새 후보가 이 하드 의미를 복제해서는 안 된다.

3. `photo_prompt_quality_layers.json`
   - `photographic_craft.light_provenance`는 광원의 방향, 감쇠, bounce, exposure가 subject와 setting에 같이 작용해야 한다는 올바른 상위 원칙을 가진다.
   - `available_light_logic`, `artificial_light_logic`, `atmospheric_diffusion`, `instrument_light_logic`의 4개 조건부 refinement가 있다.

4. `photo_prompt_tags.json`
   - 현재 수: `lighting` 143, `light_direction` 18, `light_type` 76, `light_intensity` 16, `light_shape` 90.
   - 창, 태양, 네온, 형광등, 플래시, rim, caustic, gobo, slat, wet reflection, material reveal 등 넓은 어휘가 이미 있다.

### 구조적 공백

- **클러스터 중심:** 12개 lighting extension은 완성 스타일 묶음에는 강하지만, 924개 프롬프트에서 보인 임의 조합을 광원-수신 관계로 합성하기 어렵다.
- **슬롯 의미 혼합:** `light_shape`에는 광원 개구 형태, 그림자 패턴, 반사 핫스팟, 볼류메트릭 빔, bokeh, emissive 효과가 함께 있다. `light_intensity`에도 광량, 노출, 대비, bloom, falloff가 섞인다.
- **수신면 부재:** 많은 후보는 “rim light”, “soft window”처럼 결과를 말하지만 어떤 표면/영역이 그 효과를 받아야 하는지 필드로 소유하지 않는다.
- **지역 소유 부재:** 얼굴, 의상, 배경, 바닥, 유리, 젖은 표면의 노출과 반사를 따로 지정할 구조가 약하다.
- **일광 필 플래시 공백:** 야간 snapshot flash 하드 프로필은 있지만 기존 태양/환경광의 그림자를 약하게 채우는 fill-flash 관계는 별도 프로필이 없다.
- **표면 차폐 패턴 공백:** hard-light 프로필은 경계·방향을 잘 다루지만, 잎/슬랫 패턴이 여러 수신면을 따라 왜곡·연속되는 관계를 독립적으로 보장하지 않는다.
- **재질 집합 공백:** glass-skin과 luxury cluster는 있으나 같은 광원 아래 matte/gloss/translucent/wet/metal의 서로 다른 하이라이트 폭·방향·투과를 한 프레임에서 비교하는 일반 관계는 advisory 수준으로 정리되지 않았다.

### 권장 소유 경계

- **조명 주제 소유:** 광원, 방향, 크기, 차폐, 필/감산, falloff, source-owned color zone, 수신면의 밝기/그림자/하이라이트 결과.
- **색 주제 소유:** 전체 palette, white balance, grading, hue/saturation 관계. 단, 어느 광원이 어느 표면에 어떤 색으로 닿는지는 조명 소유.
- **재질/의상 주제 소유:** 고유 표면 재질·거칠기·투명/반투명 상태. 그 재질이 현재 광원 아래 보이는 반응은 조명과 공동 관계이되 문구 소유자는 한 번만 둔다.
- **캡처 매체 주제 소유:** 센서/필름/플래시 장치 서명, halation, diffusion, flare, compression. 조명은 장면 광학 입력과 수신 관계까지만 소유한다.
- **quality layer 소유:** 일반적인 believable source continuity. 특정 named look이나 고정 방향을 기본값으로 설치하지 않는다.

## 제안 시각 의미 성분과 혼동 경계

| 인과축 | 관찰 가능한 성분 | 혼동 음성 | 권장 소유층 | 썸네일 게이트 | 원본 게이트 |
|---|---|---|---|---|---|
| 1. source anchor | 보이는 태양/창/실광원 또는 프레임 밖에서도 추적 가능한 한 방향 | 단순 bright background, 전체 LUT, 광원 이름만 있음 | `lighting_causal_axes.source_anchor` advisory; exact phrase만 hard profile | 주된 밝기 방향이 하나 읽힘 | 반사·그림자·색 구역이 같은 소스를 가리킴 |
| 2. apparent size | 넓은 광원은 broad shadow/specular transfer, 작은 광원은 짧은 penumbra·compact highlight | blur, skin smoothing, sharpening, contrast slider | 기존 hard/soft 의무 재사용 | 그림자 전이 폭이 장면 스케일에서 읽힘 | compatible surface의 specular 폭과 form transition이 일치 |
| 3. incident vector | 피사체 기준 azimuth/elevation/depth, main lit plane과 shadow plane | 단순 좌우 밝기, pose 때문에 생긴 self-occlusion | `light_direction`을 source-relative vector로 확장 | 밝은 면과 어두운 면의 대순서 | 코/턱/주름/물체의 그림자 방향이 서로 모순되지 않음 |
| 4. occluder transfer | 잎·슬랫·창틀·물체가 만든 패턴, 여러 수신면에서 원근/곡률에 맞게 변형 | 프린트 무늬, screen overlay, global vignette | 새 narrow relation 후보 | 패턴과 주 피사체의 읽힘이 동시에 유지 | 경계가 표면 곡률·깊이·접촉을 따르고 occluder 논리가 일치 |
| 5. spill/falloff | 소스에서 멀어질수록 밝기/색 구역이 줄고, background contamination 여부가 보임 | vignette, DOF blur, dark background only | quality `light_provenance` + advisory axis | 근/원경 밝기 계층 | 바닥·벽·배경의 spill 경계와 반사가 같은 광원을 유지 |
| 6. key/fill/bounce/subtraction | 키가 주 그림자를 만들고 필은 두 번째 반대 그림자 없이 밀도만 열며 negative fill은 국소 반사를 줄임 | global exposure, split light, HDR lift, black styling | 기존 `key_fill...`, `negative_fill...` hard profile 재사용 | 키와 열린 그림자의 위계 | fill로 열린 내부 세부, stable key side, double shadow 부재 |
| 7. separation/rim | 선택적 실제 윤곽의 후방/후측광, 읽히는 전면, 배경과의 국소 분리 | cutout halo, bloom, overexposed edge, silhouette only | 기존 `backlit_rim...` 재사용 | 선택적 외곽과 배경 분리 | 머리·섬유·금속 등 실제 edge를 따라 폭과 강도가 변화 |
| 8. exposure distribution | highlight core, bright texture, midtone, structured shadow의 영역별 목표 | 전체 밝기, low-contrast grade, gray highlights, HDR halo | 기존 high/low key 및 highlight rolloff + 새 regional metadata | 흰 영역·중간톤·검정의 큰 분포 | 작은 clip core, 주변 질감/색, shadow detail 생존 |
| 9. source-owned color zones | warm/cool/colored sources가 공간적으로 분리되고 실제 수신면에 이어짐 | teal-orange LUT, material base color, background-only neon | lighting owns spatial source color; palette topic owns grade | 두 색 구역의 공간 분리 | 접촉/반사/그림자까지 source direction과 색이 일치 |
| 10. receiver/material response | diffuse value, specular shape, transmission/edge glow, microtexture가 재질별로 다름 | 단어만 glossy/matte, plastic smoothing, global glow | material intrinsic + lighting response relation | 재질 집합의 큰 밝기 위계 | 하이라이트 폭/방향, 투과, 미세결이 재질과 광원에 동시에 부합 |
| 11. participating medium | 소스-차폐-산란 매질-수신면으로 이어지는 shaft/atmospheric spread | fog only, painted god ray, lens flare streak | 기존 volumetric hard profile 재사용 | 빔과 어두운 gap이 분리 | occluder pattern과 landing surface가 이어짐 |
| 12. optical/post response | 밝은 source edge에 국소 halo, lens-aligned flare, 또는 bloom이 제한적으로 생김 | global glow, chromatic aberration, haze, clipped white | capture-medium/optics owner; 조명은 bright anchor만 제공 | 효과가 프레임 전체를 덮지 않음 | halo/ghost/flare의 위치와 core detail이 물리적 anchor에 정렬 |

ARRI Lighting Handbook는 광원의 물리적 크기와 shadow-edge transfer를 연결하고, key/fill/separation/background를 서로 다른 역할로 정의하며, diffuse value·specular highlight·shadow를 3차원 대비의 별도 성분으로 설명한다. 이 구조는 스타일 이름보다 위 12축을 쓰는 근거가 된다. PBRT의 microfacet 설명은 표면 거칠기와 미세 표면 법선 분포가 정반사 폭·형태를 바꾸고, masking/shadowing이 관찰 결과에 관여한다는 근거를 제공한다. 따라서 `glossy`나 `matte`를 조명 스타일처럼 쓰지 말고 광원, 관찰 방향, 재질 미세구조의 공동 결과로 검토해야 한다.

## 후보팩/데이터 제안

### 1. 스타일 클러스터는 요약으로 격하하고 인과축을 추가

기존 12개 `visual_semantics` 클러스터를 삭제할 근거는 없다. `golden_hour_backlit_portrait`, `direct_flash_y2k_snapshot` 같은 클러스터는 요청자가 그 전체 look을 원할 때 유용한 선택적 gestalt다. 다만 선택되면 아래 causal record로 즉시 분해되어야 하고, 클러스터 이름 자체가 런타임 의무를 대신하면 안 된다.

제안 위치: `photo_prompt_lighting_extension.json`의 새 authored source section `causal_axes` 및 `causal_relations`.

```json
{
  "id": "litcausal_small_direct_source_transfer",
  "mode": "advisory_postcore_open_dimension",
  "owner_axis": "source_apparent_size",
  "affected_dimensions": ["lighting"],
  "source_role": "key",
  "source_evidence": ["small acting source", "single readable direction"],
  "receiver_roles": ["primary_subject", "available_cast_shadow_surface"],
  "observable_outputs": [
    "short penumbra",
    "compact direction-owned specular",
    "decisive form shadow"
  ],
  "confusion_boundaries": [
    "contrast grade only",
    "oversharpening",
    "dark background only",
    "clipped highlights"
  ],
  "candidate_slot_ids": {
    "light_type": ["direct_sun", "hard_flash"],
    "light_shape": ["small_point_light"]
  },
  "hard_profile_ids": ["hard_light_shadow_edge_relation"]
}
```

필드 의미:

- `mode`: v6 post-core에서 조명이 open dimension일 때만 advisory로 제공
- `owner_axis`: 한 효과를 한 축이 소유하도록 하여 중복 문구 방지
- `source_role`: key/fill/separation/background/emissive/practical 중 역할
- `source_evidence`: 장면에서 확인할 수 있는 최소 광원 단서
- `receiver_roles`: 어떤 표면 또는 영역이 효과를 받아야 하는지
- `observable_outputs`: 최종 프롬프트에서 새로 저술할 수 있는 결과 관계
- `confusion_boundaries`: 후보 선택 시 같이 제시할 하드 음성
- `candidate_slot_ids`: 기존 슬롯 후보를 재사용하는 연결
- `hard_profile_ids`: exact activation 또는 composer opt-in일 때만 승격할 기존 의무

public v6 pack은 기존 원칙대로 점수·선택 답·고정 prompt prose를 노출하지 않고, unordered concept terms와 영향을 받는 `lighting` 차원만 제공해야 한다.

### 2. 우선 제안하는 advisory relation ID

| 제안 ID | 핵심 관계 | 연결할 기존 hard profile 또는 상태 |
|---|---|---|
| `litcausal_large_diffused_source_transfer` | 큰 acting source -> broad shadow/specular transfer + readable direction | `soft_light_shadow_edge_relation` |
| `litcausal_small_direct_source_transfer` | 작은 acting source -> short penumbra + compact highlight | `hard_light_shadow_edge_relation` |
| `litcausal_source_receiver_vector` | source-relative direction -> main plane/form shadow/cast shadow 일치 | hard/soft profile의 공통 기반 |
| `litcausal_occluder_pattern_surface_continuity` | 잎/슬랫/격자 -> 여러 표면에서 연속·왜곡되는 cast pattern | 새 narrow hard profile 후보 |
| `litcausal_open_bounce_fill` | key-owned shadow만 열고 반대 그림자를 만들지 않는 broad return | `key_fill_separation_background_roles` |
| `litcausal_local_negative_fill` | 주변 bounce 감산 -> key/exposure 유지 + 국소 shadow deepening | `negative_fill_shadow_deepening_relation` |
| `litcausal_daylight_fill_flash_balance` | 태양/환경 키 유지 + 플래시가 주 그림자 밀도만 완화 | 새 narrow hard profile 후보 |
| `litcausal_rim_with_front_readability` | 후방광 -> 선택적 rim + 읽히는 전면 + 배경 분리 | `backlit_rim_edge_separation_relation` |
| `litcausal_regional_highlight_rolloff` | 작은 clip core + 주변 bright texture/hue + midtone 유지 | `highlight_rolloff_tone_response` |
| `litcausal_multi_material_response` | 같은 소스 아래 matte/gloss/wet/metal/translucent의 서로 다른 응답 | advisory 우선, 충분한 holdout 후 exact 검토 |
| `litcausal_mixed_source_spatial_zones` | visible practical/ambient -> 방향·색·falloff가 다른 공간 구역 | `motivated_practical_mixed_interior_relation` |
| `litcausal_source_occluder_volume_receiver` | source -> occluder -> medium -> landing surface | `volumetric_occluded_light_shafts` |

### 3. 새 하드 프로필은 두 개만 우선 검토

현재 프로필이 이미 넓게 겹치므로 후보를 모두 하드 의무로 만들면 안 된다. 이 코퍼스에서 별도 혼동 경계가 분명한 두 관계만 우선 설계할 가치가 있다.

#### `patterned_cast_shadow_receiver_continuity`

- **활성:** 사용자가 leafy/slatted/lattice cast pattern과 수신면 관계를 정확히 요청한 경우만
- **필수 성분:** coherent source direction, identifiable occluder grammar, bright/dark pattern, surface-curvature/depth deformation, at least two connected receiver regions
- **reject:** printed pattern, projection overlay without shadow geometry, random face stripe, vignette, global contrast
- **thumbnail:** 패턴과 주 피사체가 함께 읽힘
- **native:** 패턴 경계와 스케일이 얼굴/직물/바닥의 곡률·깊이를 따라 바뀜

#### `daylight_fill_flash_balance_relation`

- **활성:** 사용자가 daylight fill flash 또는 sun-plus-fill-flash 관계를 정확히 요청한 경우만
- **필수 성분:** non-flash ambient/key direction remains visible, flash near camera axis, key-owned cast/form shadow remains but density is reduced, subject/background exposure both retained, no night-snapshot near/far blackout requirement
- **reject:** direct-flash night signature, flat studio wash, HDR shadow lift, white balance only, ambient-only bright face
- **thumbnail:** 태양/환경 방향과 플래시 보정이 동시에 읽힘
- **native:** 원래 키 그림자 방향은 유지되고 fill은 두 번째 반대 그림자 없이 shadow density만 연다

`multi_material_response`는 유망하지만 표본이 인물 중심이고 재질 조합이 제한되므로 우선 advisory로 두고 비인물 holdout을 더 모아야 한다.

### 4. quality layer 보강 방향

`photographic_craft.light_provenance`는 유지한다. 새 고정 스타일을 추가하지 말고 다음 두 질문을 audit metadata로 보강하는 편이 좁다.

1. `receiver_coverage`: subject, setting, prop/material 중 어떤 수신면이 같은 source evidence를 공유하는가?
2. `effect_owner`: direction, shadow transfer, fill, exposure, material response, optics 중 어느 층이 이 문구를 한 번만 소유하는가?

이 두 필드는 일반 원칙이지 프롬프트 기본 방향·대비·색을 설치하지 않는다.

## 회귀 및 held-out 테스트 설계

### 패키지/구조 테스트

1. 모든 causal record는 정확히 하나의 `owner_axis`와 한 개 이상의 `receiver_roles`를 가진다.
2. 한 cluster가 선택되면 광원, 방향, fill/exposure/material 관계 중 실제로 필요한 축만 decomposed record로 연결되고, summary label은 한 번만 남는다.
3. `light_intensity` 후보가 bloom/halation/falloff/contrast를 동시에 소유하지 못하게 한다.
4. `light_shape` 후보는 `source_aperture`, `cast_shadow_pattern`, `specular_shape`, `volumetric_path`, `emissive_shape` 중 하나로 세분된다.
5. advisory BM25F/embedding hit는 hard profile 또는 render gate를 만들지 않는다.
6. exact numeric CCT/lux/watt는 requester metadata 또는 trusted capture metadata가 없으면 픽셀 의무로 승격하지 않는다.

### 프롬프트 행동 causal pairs

각 pair는 subject/setting/camera를 고정하고 한 축만 바꾼다.

1. **source size pair:** small direct source vs large diffused source. 예상 변화는 shadow-edge/specular width이고 방향·프레이밍은 고정.
2. **fill pair:** key only vs broad fill vs negative fill. 예상 변화는 key-owned shadow density이며 key side와 overall exposure는 고정.
3. **flash pair:** 야간 direct snapshot flash vs daylight fill flash. 전자는 근원거리 감쇠/compact hotspot, 후자는 기존 일광 방향과 배경 노출 보존.
4. **occluder pair:** leafy/slatted cast pattern vs printed fabric pattern. 후자는 그림자 의무를 통과하면 안 됨.
5. **rim pair:** selective rear rim vs uniform cutout halo/bloom. 전면 형태와 실제 edge 추적 여부가 판정점.
6. **color pair:** spatial warm practical + cool ambient vs teal-orange global grade. 같은 색 팔레트라도 source landing과 shadow ownership이 다름.
7. **material pair:** 같은 광원 아래 matte cloth vs polished metal vs translucent petal. 광원 방향은 고정하고 highlight width/transmission만 달라져야 함.
8. **tone pair:** highlight rolloff vs global low contrast vs bloom. core shape, bright texture, midtone 생존을 분리 검토.

### 코퍼스 held-out fixture 후보

아래 ID는 이번 40장 픽셀 표본에 포함하지 않았다. 향후 pack/prompt 테스트를 작성할 때 motivating literals를 런타임 기본값으로 옮기지 않고 fixture로만 사용한다.

| 목적 | 양성/하드 음성 후보 |
|---|---|
| 완전 causal chain | 2740: rear warm rim + cool frontal fill + rolloff + knit/hair receivers |
| 수치/장비 과잉 주장 | 2713: 5000–5600K key 문구는 효과 검토와 장비 수치 검토를 분리 |
| clamshell 유사 관계 | 2715: frontal softbox + lower reflector; 원형 ring glare를 hard negative로 구성 |
| mixed source spatial ownership | 2739, 2545: neutral key/cool ambient 또는 visible practical/ambient 전이 |
| flash material response | 2640, 2150: sequin/skin/near-background hotspot과 거리 감쇠 |
| generic label hard negative | 1926, 2118: `cinematic lighting`만으로 방향·fill gate를 만들지 않음 |
| material nonportrait | 추가 꽃·제품·유리·금속 holdout 필요; 인물 표본만으로 promote 금지 |

### 렌더 검토 게이트

- **thumbnail:** source direction, light/dark mass, subject-background hierarchy, cast-pattern salience, rim separation, mixed-color zone, near/far flash drop처럼 첫 읽기 관계를 본다.
- **native:** penumbra, contact/cast shadow, catchlight, pores, hair fibers, fabric weave, petal veins, specular width, highlight core/rolloff, shadow internal detail을 본다.
- 모든 hard gate는 같은 프레임에서 통과해야 한다. 큰 분위기 하나가 보였다고 나머지를 보간하지 않는다.
- 한 번의 생성 결과로 후보 인과성을 주장하지 않는다. 같은 모델/설정, arm별 고정 prompt, 독립 반복, negative control이 필요하다.

## 한계와 경계 결정

- 40장은 목적 표본이며 4,908장 전체 분포를 나타내지 않는다.
- 40장은 썸네일, 16장은 원본 크기로 보았다. 원본을 보지 않은 이미지의 미세 반사·필름 효과는 평가하지 않았다.
- 프롬프트 정규식은 영어 중심이며 한국어/문장 구조와 부정 표현을 완전하게 분석하지 않는다.
- 코퍼스 이미지가 어떤 모델·seed·참조 이미지·후처리 경로로 생성됐는지 완전한 lineage가 없다. 프롬프트-픽셀 정렬은 원인 증명이 아니다.
- 픽셀은 광원 방향, 그림자 전이, highlight morphology, source-owned color zone, material response를 지지할 수 있지만 fixture brand, wattage, lux, exact ratio, CCT, CRI/TLCI/SSI/SPD를 입증하지 않는다.
- 외부 자료는 안정적인 광학/조명 기전만 보강하며 코퍼스 빈도나 후보 기본값의 근거로 사용하지 않았다.
- 사용자 미적 판단, 새 후보팩 생성, 런타임 prompt audit, 독립 렌더 자격, 일반화 성능은 모두 `UNSCORED`다.

따라서 현재 결정은 **`proposed`**다. 현재 12개 스타일 클러스터와 29개 좁은 의무 프로필을 유지하면서, post-core advisory 후보를 source-relative causal record로 보강하고, 새 하드 프로필은 patterned cast-shadow continuity와 daylight fill-flash balance 두 개만 별도 자격 평가하는 것이 가장 작은 일관된 변화다.

## 증거 부록

### 표본 이미지 경로

각 항목의 `_01.jpg`, `_02.jpg`를 검사했다.

```text
generated/reactorprompt-export-20260902-incremental/images/1569_DY1JnexGrj4_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1569_DY1JnexGrj4_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1587_DY10cywGvWk_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1587_DY10cywGvWk_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1595_DY142I3mhCH_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1595_DY142I3mhCH_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1603_DY4wThpmgYx_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1603_DY4wThpmgYx_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1772_DZNAfRbmj68_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1772_DZNAfRbmj68_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1840_DZkWoZZGgEe_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1840_DZkWoZZGgEe_02.jpg
generated/reactorprompt-export-20260902-incremental/images/1953_DZ44vuJmsGe_01.jpg
generated/reactorprompt-export-20260902-incremental/images/1953_DZ44vuJmsGe_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2123_DaiKtCtGhHm_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2123_DaiKtCtGhHm_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2149_DarjtS5GiRL_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2149_DarjtS5GiRL_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2200_Da7BV7Bmul4_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2200_Da7BV7Bmul4_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2262_DbK4NhoGpS2_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2262_DbK4NhoGpS2_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2299_DbcuYZ-GmbV_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2299_DbcuYZ-GmbV_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2467_DcAfXXLmuHQ_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2467_DcAfXXLmuHQ_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2552_DcQKKoSmvd0_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2552_DcQKKoSmvd0_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2554_DcQJjwRGoam_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2554_DcQJjwRGoam_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2564_DcLrhgjGh_0_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2564_DcLrhgjGh_0_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2608_DcdzbCUmrdO_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2608_DcdzbCUmrdO_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2626_DcgVNgCmjJC_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2626_DcgVNgCmjJC_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2683_Dcn1_tAGlAO_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2683_Dcn1_tAGlAO_02.jpg
generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_01.jpg
generated/reactorprompt-export-20260902-incremental/images/2741_Dcx0xZ8mlev_02.jpg
```

### 원본 크기 재검토 이미지

```text
1569_01, 1772_01, 1840_01, 2123_01, 2149_01, 2200_01,
2467_01, 2552_01, 2564_01, 2608_01, 2626_01, 2741_01,
1595_01, 1595_02, 2554_01, 2554_02
```

### 핵심 명령

```bash
jq '[.[] | select(.prompt != null and (.prompt | gsub("\\s"; "") | length) > 0)] | length' \
  generated/reactorprompt-export-20260902-incremental/manifest.json

python3 - <<'PY'
# manifest의 924개 비어 있지 않은 prompt를 읽고, 정규식 축별 raw/positive-context
# match count와 6축 coverage histogram을 산출했다.
PY

jq -r '.visual_semantics[] | [.id,.primary_visual_proposition] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_lighting_extension.json

jq -r '.profiles[] | select(.category|startswith("capture_lighting")) | .id' \
  skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations.json

jq -r '.photographic_craft.dimensions[] | [.id,.baseline_principle] | @tsv' \
  skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json
```

전수 스캔의 축 정규식 요약:

```text
source size: large|small|broad|narrow|hard|soft|diffused + light/source/sun/flash
direction: upper|lower|overhead|side|front|rear|back|three-quarter|raking|grazing + light
fill: fill light|bounce light|negative fill|ambient fill|open shadow|reflector
shadow: cast|contact|dappled|leafy|window|gobo|blind|penumbra|falloff
exposure: exposure|over/underexposure|rolloff|clip|crush|dynamic range|high/low key
material: specular|gloss|matte|satin|metal|glass|wet|translucent|subsurface
```

### 외부 1차/권위 자료

- [ARRI Lighting Handbook (official PDF)](https://www.arri.com/resource/blob/83996/409091c612f371b0c68b41d9dcb636db/arri-lighting-handbook-english-data.pdf): source size와 hard/soft shadow edge, key/fill/separation/background 역할, diffuse/specular/shadow 및 edge transfer 정의.
- [ARRI Lighting Handbook landing page](https://www.arri.com/en/learn-help/lighting/lighting-handbook): 제조사 공식 배포·판본 출처.
- [Physically Based Rendering, 4e — Roughness Using Microfacet Theory](https://www.pbr-book.org/4ed/Reflection_Models/Roughness_Using_Microfacet_Theory): 거칠기, microfacet normal distribution, masking/shadowing, anisotropic highlight shape의 기전.

# 배색 데이터 반영과 독립 이미지 테스트 결과

2026-10-06 착수 · 2026-10-07 완료. 주 작업 폴더에 활성 데이터와 두 인덱스를 반영했습니다. 독립 에이전트 3개가 첨부 사진을 활용해 네이티브 이미지를 총 5회 생성했습니다.

**새 시각 프로필의 검색 → 선택 → 이미지 표현은 2개 컨셉에서 확인했습니다. 합성 테스트 전체 통과는 1개이며, 나머지 2개에는 필수 세부 조건 실패가 남았습니다.** 일반 `pal_app_` 후보는 세 컨셉에서 채택되지 않았으므로 이미지 효과가 검증됐다고 보고하지 않습니다.

## 활성 데이터

연구 카드 100개 중 37개를 좁은 후보로 추가하고, 52개는 기존 관계 후보 23개의 선택적 문맥으로 보강했습니다. 새 시각 프로필은 13개, opt-in 이미지 게이트는 30개입니다. 문화·영화의 특정 사례·표지 기능·수치 데이터의 11개 주장은 보류 기록을 유지했습니다.

[후보 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_palette_applications_extension.json) · [시각 의미 원본](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_palette_applications.json) · [100개 채택/보류 대조](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/ADOPTION-MANIFEST.json)

팔레트 이름은 선택적 검색에 쓰입니다. 실제 요청의 완전한 관계 또는 적합한 명시적 선택만 필수 표현을 만듭니다. 속성 범위가 `*`였을 때 참조 얼굴/머리 보존 조건과 무관한 색 선택까지 차단되는 문제를 발견해, 실제 표면·의상·배경·광원·보정 경로로 좁혔습니다. parent/cross-dimension 잠금 검사는 유지했습니다. 고정된 연구 예시 물체를 사용자 요구나 실제 core owner로 위장하지 않았습니다.

이미지 생성 후 컵/배경 그라데이션의 실제 `surface.local_color` 잠금 경로를 추가 보완했습니다. 생성에 쓰인 generation 3와 마지막 활성 generation은 구분해 보존했습니다. 세 이미지에서 선택한 금속/수신 광 프로필의 원문·효과·게이트가 동일함을 직렬화 해시로 확인했습니다. 마지막에 수정한 미선택 컵/그라데이션 항목은 소프트웨어 잠금 검사만 통과했고 픽셀 검증은 수행하지 않았습니다.

semantic index는 10,476개, visual index는 2,249개입니다. 기존 10,439개 의미 벡터와 2,236개 시각 벡터의 문장/수치가 그대로 유지됐으며 삭제된 entry/shard는 없습니다. provider/model/dimensions는 Gemini / gemini-embedding-2 / 768입니다.

## 독립 테스트

설치된 최신 스킬과 같은 SHA-256 원문, 동일 사진, byte-exact 사용자 envelope를 고정했습니다. 각 에이전트는 별도 RNG seed로 독립 컨셉을 선택하고 core/controls/embodiment/중립 feature selection을 먼저 동결했습니다. 다른 arm의 컨셉·프롬프트·이미지를 입력으로 사용하지 않았다는 선언과 해시를 보존했습니다. 수정된 데이터로 replay할 때에도 이 입력 해시는 유지됐습니다. 선언과 해시는 절차 증거이며 모델 내부 지식의 독립성을 수학적으로 증명하지는 않습니다.

|컨셉|새 데이터의 실제 선택/픽셀|합성 조건|실제 호출|
|---|---|---|---|
|모델 선박 포장 · 반사 금속/보라 직물|pa_bounded_metal_trim · 2/2 PASS|5/5 PASS|2|
|천문대 문턱 정비 · 따뜻한 실내/푸른 외부|pa_local_color_under_separate_lights · 3/3 PASS|7/8 FAIL · 작은 빨강 탭의 직조 불명확|1|
|온실 차광막 · 교차선/작은 빨강 예외|노출 2개, 선택 0개 · 통합 coverage gap|7/8 FAIL · 모서리 탭 대신 앞면 패치|2|

최종 pack/composed/runtime 감사는 세 arm 모두 PASS입니다. 저장 이미지의 formal embodiment/선택된 opt-in 게이트는 각각 7/7, 8/8, 5/5였으며, 이 수치를 별도 합성 시나리오의 전체 성공과 혼동하지 않았습니다. 사용자 판단은 모두 `not_yet_received`이고 대표 승격은 false입니다. 일부 moe audit exit 1은 사용자 판단 대기 상태이며, schema failure/failed formal gate는 0개입니다.

각각의 이미지가 갖춘 조건만 판정했습니다. 첫 사진의 조건과 두 번째 사진의 조건을 합쳐 PASS로 만들지 않았습니다. 온실 첫 사진의 내부 X 스티치는 엄격한 peer review에서 실패로 정정했고 원래 리뷰도 역사 기록으로 보존했습니다. 후속 사진에서는 X가 사라졌지만 위치가 어긋나 여전히 FAIL입니다.

### 모델 선박 포장 작업 · 금속 반사와 보라색 직물

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/corrected-run/composed_prompt.json) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/test_case.json) · [검색/선택/효과/owner 추적](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/corrected-run/new_data_adoption_trace.json) · [픽셀 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/corrected-run/pixel_review.json) · [arm 전체 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/arm_summary.json)

![모델 선박 포장 작업 · 금속 반사와 보라색 직물](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm1/generated_images/boat-material-ownership-attempt2/native.png)

### 해변 천문대 문턱 정비 · 따뜻한 실내광과 푸른 외부광

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/prompt_en.generation3.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/test_case.json) · [검색/선택/효과/owner 추적](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/palette_selection_and_coverage.generation3.json) · [픽셀 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/native_test_case_result.json) · [arm 전체 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/arm2_completion_report.json)

![해변 천문대 문턱 정비 · 따뜻한 실내광과 푸른 외부광](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm2/generated_images/observatory-threshold-native-attempt-1/image.png)

### 온실 차광막 수선 확인 · 같은 천의 교차선과 작은 빨강 예외

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/attempt-2/final_prompt.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/test_case.json) · [검색/선택/효과/owner 추적](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/integration_trace.json) · [픽셀 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/attempt-2/pixel_test_review.json) · [arm 전체 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/qualification_summary.final.json)

![온실 차광막 수선 확인 · 같은 천의 교차선과 작은 빨강 예외](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/independent-runs/arm3/generated_images/greenhouse-grid-tab-native-2/arm3.png)

## 검증과 한계

변경 관련 48개 검사는 모두 통과했습니다. 검색·core·후보·인덱스 계약 93개에서는 92개 통과, 기존 의복 maintenance record의 `maintenance_only` 누락 1개 오류가 재현됐습니다. 새 팔레트 원본을 제외한 원래 inventory에서도 같은 오류가 발생함을 기록했습니다.

전체 회귀의 fail-fast 확인은 역사 V24–V31 source 보존 경계에서 중단됐습니다. 작업 전 manifest bytes를 최초 SHA와 일치하게 복원해 대조했으며 이 원래 manifest도 이전 보존 체계에 승인되지 않습니다. 기존 dirty 상태의 불일치로 구분하고 역사 fixture나 의복 기록을 임의로 고치지 않았습니다. 전체 suite PASS는 확인하지 않았습니다.

첫 선박 control에도 골드 디테일이 있었습니다. 이미지 도구의 seed를 통제하지 않았고 A/B/C 반복 비교·사용자 선호 판단을 수행하지 않았으므로 데이터만의 인과적 개선이나 일반화된 품질 향상은 주장하지 않습니다. HEX는 연구의 sRGB 근삿값이고 사진 픽셀의 정확한 색이나 실제 금속/도자기의 화학적 조성·인물의 실제 정체성을 검증하지 않습니다.

[현재 원본/인덱스 무결성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/FINAL-SOURCE-INTEGRITY.json) · [인덱스 재생성/벡터 보존](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/INDEX-REPORT.json) · [기존 오류 재현](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/BASELINE-FAILURE.json) · [역사 source 기존 불일치 대조](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/HISTORICAL-BASELINE-DIAGNOSTIC.json) · [전체 구조화 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/color-palette-integration-20261006/QUALIFICATION-REPORT.json)

## 결과를 반영한 다음 검증 계획

1. 같은 색/유사 선폭의 교차 그리드와 불균등 체크를 다른 변형으로 다룹니다. 기존 좁은 ID를 느슨하게 바꾸지 않고, 같은 carrier/교차 방향/폭·간격이 각각 읽히는 변형을 검토합니다. 새 구어체 holdout은 데이터 수정 전에 동결합니다.
2. 일반 팔레트 후보의 slot-focus grounding, 실제 owner/property 적합성, 제한된 후보 노출을 따로 조사합니다. 같은 저장 core로 positive/adjacent/negative 노출 검사를 먼저 만들고, 부적합한 팔레트를 모든 복잡한 장면에 강제로 노출하지 않습니다.
3. 작은 직물 강조는 native에서 확인 가능한 크기와 면적 역할을 사전 조정합니다. 모서리 탭은 모서리·연결·탭 자체의 동시 조건으로 판단하며 단순 빨강 패치로 대체하지 않습니다.
4. 보류 11개는 구체 장면/primary source/관할/데이터 타입을 보충한 뒤 가시적 색 응용과 출처·기능·수치 의미를 분리합니다.
5. 품질 개선 비교가 필요할 때 같은 core/controls로 A/B/C와 반복 샘플을 설계하고 실제 사용자 선호를 별도로 받습니다. 이번 결과는 해당 비교를 대신하지 않습니다.

주 작업 폴더의 기존 변경과 오래된 shard는 보존했습니다. commit/push/PR은 생성하지 않았습니다. 동결 arm JSON의 worktree 경로는 hash-bound 원문 보존을 위해 그대로 두었고, 이 보고서의 링크는 주 작업 폴더에 복사한 동일 바이트 결과를 가리킵니다.

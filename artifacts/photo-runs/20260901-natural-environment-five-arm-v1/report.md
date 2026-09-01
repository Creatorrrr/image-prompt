# 자연환경 시각 의미·후보팩 5-arm 렌더 자격시험

조사 기반 데이터 반영과 실제 픽셀 시험을 서로 다른 증거층으로 분리했다. 결론은 다음과 같다.

- 자연환경 후보 데이터: 7개 슬롯, 75개 후보
- 좁은 개념 믹스인: 12개
- 한 프레임에서 엄격히 판정 가능한 하드 시각 프로필: 8개
- 독립 서브에이전트: 5개
- built-in image generation: 팔당 1회, 총 5회
- 재생성·CLI/API fallback: 0회
- 자연환경 target gate: 25/25 PASS
- 참고 외관·통합 shared gate: 24/25 PASS
- 엄격한 전체 랜덤 테스트케이스: 3/5 PASS
- 사용자 미적 판단과 체감 유사도: pending

## 데이터 반영

후보팩에는 노령림, 습지 수문 모자이크, 범람원 구배, 조간대 대상, 카르스트 배수, 활동 빙하, 풍성사구, 열수지대, 적란운, 고산 수목한계, 맹그로브 뿌리, 산호초 횡단 구조를 `subject/action/location/surface/composition` 관계로 분해해 넣었다. 8개 하드 프로필은 단일 상징이 아니라 네 가지 관찰 구성요소와 관계, 다섯 개 픽셀 게이트, 명시적 혼동 대체물, 비추론 경계를 가진다.

상세 조사: [natural_environment_visual_semantics_20260901.md](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/natural_environment_visual_semantics_20260901.md)

검증 기록: [validation_summary.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-prompt-natural-environment-semantics-20260901/validation_summary.json)

## 독립 시험 결과

| Arm | 무작위 복합 콘셉트 | 환경 target | shared | 전체 테스트케이스 | 엄격 판정 근거 |
|---|---|---:|---:|---:|---|
| 01 | 석양의 마른 호수에서 폭풍을 취재하는 리포터 + 적란운 전체 구조 | 5/5 | 5/5 | PASS | 어두운 밑면·연속 대류탑·섬유상 모루·강수축이 한 셀로 보임 |
| 02 | 비 뒤 카르스트 고원에서 소실점에 표식을 두는 지형 사진가 | 5/5 | 5/5 | FAIL | 카르스트 구조는 PASS, 두 표식은 이미 꽂혀 있어 `놓는 중` 동작이 보이지 않음 |
| 03 | 비 갠 노령림 갭에서 nurse log의 갱신을 촬영하는 조사자 | 5/5 | 4/5 | FAIL | 노령림 구조는 PASS, 얼굴이 작고 하향이라 양 축척 외관 연속성은 FAIL |
| 04 | 해무가 걷히는 해안 사구에서 풍향천을 든 여행자 | 5/5 | 5/5 | PASS | 완만한 풍상면·마루·급경사 활강면·정렬 잔물결이 한 사구에 연결됨 |
| 05 | 진눈깨비 뒤 수목한계 경사면에서 지도를 읽는 산악 지도제작자 | 5/5 | 5/5 | PASS | 하부 숲→성긴 수목→크룸홀츠→무수목 고산대 순서가 유지됨 |

키워드 자체의 픽셀 자격은 5/5 모두 통과했다. 다만 첨부 참고 이미지의 활용까지 포함한 공통 프로토콜은 arm-03 때문에 4/5이며, 무작위 장면의 부차 동작까지 모두 요구하면 arm-02까지 실패하여 최종 3/5다. 부분 충족을 성공으로 합치지 않았다.

## 결과 이미지와 프롬프트

### Arm 01 — 적란운

![arm-01](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-01/render.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-01/composed_prompt.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-01/pixel_review.json) · [실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-01/run_manifest.json)

### Arm 02 — 카르스트

![arm-02](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-02/render.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-02/composed_prompt.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-02/pixel_review.json) · [실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-02/run_manifest.json)

### Arm 03 — 노령림

![arm-03](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/render.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/composed_prompt.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/pixel_review.json) · [실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-03/run_manifest.json)

### Arm 04 — 풍성사구

![arm-04](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-04/render.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-04/composed_prompt.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-04/pixel_review.json) · [실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-04/run_manifest.json)

### Arm 05 — 고산 수목한계

![arm-05](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-05/render.png)

[최종 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-05/composed_prompt.json) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-05/pixel_review.json) · [실행 기록](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/arm-05/run_manifest.json)

## 감사·계보

- 다섯 코어는 각자 로컬 의미 데이터에 접근하기 전에 동결됐다.
- coordinator-assigned 키워드는 사용자 원문에 있었다고 위조하지 않았다. post-core recipe-route 진단으로 현재 믹스인과 후보 ID 매핑만 검증했다.
- 최종 v6 후보팩, composed prompt, runtime request는 각 팔별로 해시 결속됐다.
- coordinator가 composed audit 5/5와 runtime reference audit 5/5를 다시 실행해 모두 PASS를 확인했다.
- 첨부 이미지는 일반적 성인 외관 참고로만 사용했다. 동일인·생체 신원·보호 특성·건강·매력·성격을 추론하지 않았다.
- 생성 성공 또는 감사 PASS를 픽셀 PASS로 대체하지 않았다.

교차 픽셀 판정: [cross_pixel_review.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/coordinator/cross_pixel_review.json)

최종 자격 요약: [qualification_summary.json](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260901-natural-environment-five-arm-v1/coordinator/qualification_summary.json)

## 결정

- 자연환경 데이터·라우팅·프롬프트 동작: `promote`
- 이번에 표본 추출한 5개 자연환경 키워드의 픽셀 의미: `qualified`
- 첨부 외관 참고와 무작위 부차 동작까지 포함한 전체 end-to-end 실행: `revise`
- 사용자 미적 판단 및 체감 유사도: `pending`

렌더를 고쳐서 실패를 숨기는 재시도는 하지 않았다. 따라서 arm-03의 외관 가독성 실패와 arm-02의 동작 실패는 다음 개선 반복의 실제 입력으로 남는다.

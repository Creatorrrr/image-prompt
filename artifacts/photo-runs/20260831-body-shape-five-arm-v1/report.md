# 여성 체형 키워드 5-arm 이미지 반영 시험

참조 이미지 SHA-256: `e3e010b75a48da02f914d7e8202690b3353450a78832daaefea0bbbc234aa5b3`

참조 역할은 얼굴 외관에 한정했다. 체형은 각 arm의 고정된 독립 프롬프트에서 생성했으며, 참조 사진의 몸을 추정하거나 복사하지 않았다. 얼굴 평가는 관찰 가능한 외관 연속성일 뿐 생체 신원 확인이 아니다.

## 결과 요약

| Arm | 키워드 | 복합 콘셉트 | 렌더 | 목표 체형 판정 | 주요 근거 |
|---|---|---|---|---|---|
| 01 | slender build | 생물발광 고산 종자은행 정비 | 성공 | PASS 4/4 | 전신, 좁은 몸통, 가는 팔다리, 렌즈·키 단독 대체 아님 |
| 02 | busty figure | 폭풍 속 해양 신호렌즈 복원 | moderation 차단 | UNSCORED | 저장 픽셀 없음 |
| 03 | top hourglass silhouette | 화산재 경보 중 지열 관측소 지도 제작 | 성공 | FAIL | 테이블·팔 가림과 원근 때문에 양측 윤곽과 상체 우세 불충족 |
| 04 | spoon-shaped figure | 침수 아르데코 역사 모자이크 보존 | 성공 | FAIL, reviewer split | 하부 관계는 보이나 벨트·광택 주름·기울기·넓은 스탠스 대체를 배제하지 못함 |
| 05 | diamond-shaped figure | 먼지폭풍 속 사막 전파망원경 보정 | 성공 | FAIL | 중앙이 최대 폭이 아니라 가장 좁아 hourglass/pear로 판독 |

후보팩·구성·정확한 런타임 참조 감사 결과는 5/5 PASS였다. 실제 출력은 4장이고 1장은 moderation 차단이다. 점수 가능한 4장 중 목표 키워드 완전 통과는 1장이다. 네 저장 이미지 모두 참조 사진과 비생체적 얼굴 외관 연속성은 통과했다.

`slender`는 체형 게이트는 통과했지만 정확한 캡슐 삽입 순간이 모호하고 읽을 수 있는 간판·라벨이 생성되어 전체 장면 통제는 실패했다. 따라서 키워드 반영 성공과 전체 장면 기술 성공은 구분한다.

## 렌더

### Arm 01 — slender build

![Arm 01 slender](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260831-body-shape-five-arm-v1/arms/arm-01/render-attempt-02.png)

### Arm 03 — top hourglass silhouette

![Arm 03 top hourglass](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260831-body-shape-five-arm-v1/arms/arm-03/render-attempt-01.png)

### Arm 04 — spoon-shaped figure

![Arm 04 spoon](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260831-body-shape-five-arm-v1/arms/arm-04/render-attempt-02.png)

### Arm 05 — diamond-shaped figure

![Arm 05 diamond](/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260831-body-shape-five-arm-v1/arms/arm-05/render-attempt-02.png)

## 판정 증거

- 최종 합의: `coordinator/evaluation/final-consensus.json`
- 루트 픽셀 검토: `coordinator/evaluation/root-review.json`
- 블라인드 교차검토: `coordinator/evaluation/reviews/`
- 참조 결속: `coordinator/reference_binding.json`
- 팔별 프롬프트·감사·원장: `arms/arm-01`부터 `arms/arm-05`

사용자 선호와 얼굴 외관 만족도는 직접 판정 전까지 `pending`이다.

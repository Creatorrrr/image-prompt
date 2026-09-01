# 노출 의상 5-arm 실제 렌더 테스트

최종 결과는 **5개 arm 모두 단일 최종 이미지에서 기술 gate PASS**, 총 **27/27 gate PASS**입니다. 이는 프롬프트 감사를 픽셀 성공으로 간주한 결과가 아니라, 저장된 native 이미지와 512px 썸네일을 각각 확인한 결과입니다. 사용자 취향 판단은 아직 `pending / unscored`이며 대표 이미지 승격은 하지 않았습니다.

| Arm | 랜덤 복합 컨셉 | 테스트 키워드 | 최초 결과 | 최종 결과 |
|---|---|---|---|---|
| A | 수력발전 터빈 홀에서 체인 호이스트로 침수 해치를 들어 올림 | 노출도 높은 판금·메일 판타지 아머 | 출력 필터 차단, 미평가 | attempt 2, 7/7 PASS |
| B | 비 내린 Lingotto 옥상 테스트 트랙에서 윈드삭 릴을 풀며 달림 | 구조적 오픈백 드레스 | 5/5 PASS | attempt 1, 5/5 PASS |
| C | Maras 소금 계단에서 구리 그릇의 염수를 아래 수조로 부음 | 완전히 둘러싸인 양옆 허리 컷아웃 | 4/5 FAIL | 외측 밴드만 수리한 attempt 2, 5/5 PASS |
| D | 폭우 속 빅토리아식 온실에서 환기 루버 핸드휠을 돌림 | 허벅지 높이 단일 사이드 슬릿 | 출력 필터 차단, 미평가 | attempt 2, 5/5 PASS |
| E | 비 온 뒤 해안 절벽 케이블카 터미널에서 브레이크 레버를 당김 | 불투명 베이스 위 시어 오간자 광학 레이어 | 출력 필터 차단, 미평가 | attempt 2, 5/5 PASS |

## 최종 이미지와 프롬프트

- A — [이미지](arms/revealing-arm-a/generated_images/attempt2/revealing-armor-native.png), [프롬프트](arms/revealing-arm-a/composed_prompt_attempt2.json), [7-gate 리뷰](arms/revealing-arm-a/pixel_review_attempt2.json)
- B — [이미지](arms/revealing-arm-b/generated_images/revealing-arm-b-native.png), [프롬프트](arms/revealing-arm-b/composed_prompt.json), [5-gate 리뷰](arms/revealing-arm-b/pixel_review.json)
- C — [이미지](arms/revealing-arm-c/generated_native_attempt2.png), [프롬프트](arms/revealing-arm-c/composed_prompt_attempt2.json), [5-gate 리뷰](arms/revealing-arm-c/pixel_review_attempt2.json)
- D — [이미지](arms/revealing-arm-d/generated_images/attempt2/run_local_thigh_high_side_slit_dress-attempt2-native.png), [프롬프트](arms/revealing-arm-d/composed_prompt_attempt2.json), [5-gate 리뷰](arms/revealing-arm-d/pixel_review_attempt2.json)
- E — [이미지](arms/revealing-arm-e/generated_images/attempt2/revealing-arm-e-attempt2.png), [프롬프트](arms/revealing-arm-e/composed_prompt_attempt2.json), [5-gate 리뷰](arms/revealing-arm-e/pixel_review_attempt2.json)

## 검증에서 드러난 핵심

- 오픈백은 뒤 3/4 전신, 머리카락 정리, 상단 고정부, 불투명 전면 측면을 동시에 요구하자 첫 시도에서 안정적으로 보였습니다.
- 사이드 컷아웃은 단순히 `paired side cutouts`라고 하면 옆선까지 열린 형태로 변질될 수 있었습니다. `underarm side seam–high hip seam을 연결하는 외측 불투명 밴드`를 명시한 단일 gate 수리 후 완전히 닫힌 두 개의 창으로 렌더되었습니다.
- 아머·하이 슬릿·시어의 첫 출력 차단은 픽셀 실패와 분리했습니다. target과 gate를 그대로 두고 반복적인 해부학 표현만 의복 랜드마크와 중립 카탈로그 구도로 정리한 두 번째 시도에서 이미지가 생성되었습니다. 이 관찰은 인과 증명이 아니라 이번 run의 회복 이력입니다.
- 시어는 단순한 `transparent`가 아니라 불투명 베이스, 오간자 직물 표면, 봉제선·가장자리, 배경 투과, 겹친 주름의 농도 증가가 함께 있어야 픽셀 의미가 고정됐습니다.
- 아머는 단순 금속 비키니가 아니라 판금·메일·버클·리벳·관절부가 먼저 읽히고, 상부 허벅지 개방부가 별도의 노출 증거로 보여야 통과했습니다.

총 built-in 이미지 호출은 9회(A 2, B 1, C 2, D 2, E 2)이며 유료 API fallback은 0회입니다. 최초 차단·실패 결과를 삭제하거나 성공 이미지와 합성하지 않았습니다.

상세 계약은 [테스트케이스](shared/test_cases.json), [사후 타깃 배정](shared/target_assignments_after_core.json), [코디네이터 픽셀 리뷰](shared/coordinator_pixel_review.json), [후보팩 데이터 피드백](shared/data_feedback.json)에서 확인할 수 있습니다.

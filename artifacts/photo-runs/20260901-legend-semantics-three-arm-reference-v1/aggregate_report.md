# 전설 시각 의미 3-arm 검증 보고서

## 결론

전설 시각 의미 데이터와 후보팩 반영은 구조·검색·프롬프트 층에서 통과했다. 실제 픽셀은 `partial = fail` 기준으로 3개 중 2개만 통과했으므로 이번 변경은 승격하지 않고 `revise`로 남긴다. 세 실행 모두 서로의 입력을 사용하지 않았고 각각 이미지 호출 1회, 재시도 0회였지만, pre-pack `visual_intent.bindings`가 비어 있어 깨끗한 독립 자격시험으로도 승격할 수 없다. 사용자 미감 판단은 별도이며 아직 미평가다.

| Arm | 무작위 복합 컨셉 | 패키지/프롬프트 | 루트 픽셀 | 프로필 게이트 | pre-pack 바인딩 |
| --- | --- | --- | --- | --- | --- |
| 01 | 절벽 틈의 고정 보물에 접근하는 성인 등반가와 접근선을 닫는 석재 수호자 | PASS | FAIL | 2/5 | FAIL |
| 02 | 수몰된 호반 거리와 원위치 기초를 기록하는 성인 수중 고고학자 | PASS | PASS | 5/5 | FAIL |
| 03 | 폭풍 뒤 해안 거석의 거대한 다섯 손가락 자국을 재는 성인 현장 연구자 | PASS | PASS | 5/5 | FAIL |

Arm 01은 성인 회수 시도와 수호자의 직접 차단은 보이지만, 보물 자체가 작은 금빛으로만 남아 `고정된 cache`, `이전 전 실패`, `현장 잔류`를 썸네일과 원본 양쪽에서 입증하지 못했다. Arm 02는 거리망·고정 기초·연결 건축·수중 점유·인물 축척을 모두 충족했다. Arm 03은 고정 거석·표면에 이어진 손 모양 홈·자와 표식에 의한 크기·석재 연속성·현장 기록 맥락을 모두 충족했다.

첨부 사진은 세 arm 모두에서 관찰 가능한 성인 얼굴·머리·메이크업 외형 단서로만 사용했다. 세 결과에서 해당 단서는 보였지만, 이는 동일 인물·신원·생체 특성에 관한 판단이 아니다.

## 데이터 반영 범위

- 8개 시각 의미 클러스터와 6개 슬롯별 8개 후보, 총 48개 후보를 추가했다.
- 6개 신규 하드 프로필에 각각 5개 구성 관계, 5개 리터럴 프롬프트 증거 필드, 5개 픽셀 게이트, 근접 오인 대상을 부여했다.
- 석화 전설은 기존 `continuous_metamorphosis_source_target_bridge` 계약을 재사용했다.
- 예언·운명·혈통·귀환하는 왕·memorate·현대전설·전설 순환은 후보 전용으로 두고 넓은 단어만으로 하드 프로필이 켜지지 않게 했다.

## 검증 경계

- 집중 전설 테스트: 9 passed, 124 subtests passed.
- 사전 검증: dictionary valid, visual index 246 profiles / 1,304 exact terms, semantic index 7,812 entries / Gemini embedding 2 / 768 dimensions.
- 기존 전체 visual-obligation 모듈: 23 tests 중 6 failures. 모두 기존 `clinical_nursing_duty_system`의 넓은 exact term `nurse`가 yandere fixture에서 함께 활성화되는 충돌이며, 실패 목록에 전설 프로필은 없다. 이 동시 작업 범위 밖의 회귀를 숨기거나 완화하지 않았다.
- 루트 픽셀 결과: 12/15 프로필 게이트 통과, 2/3 arm 통과, 따라서 전체 FAIL.
- 독립 실행 규약: cross-arm 3/3 통과, single-call/no-retry 3/3 통과, pre-pack binding 0/3 통과.

상세 판정은 `coordination/root_independent_pixel_review.json`, 무작위 선택은 `coordination/selection.json`, 각 arm의 프롬프트·후보팩·매니페스트·원본 이미지·자체 픽셀 리뷰는 각 arm 디렉터리에 보존했다.

# arm-02 figure coverage 검증 보고서

- 전체 판정: `PASS_VISUAL_TECHNICAL_USER_JUDGMENT_PENDING`
- 콘셉트: 옅은 석회석 사이클로라마 안의 성인 전신 패션 피겨를 한 장의 연속된 불투명 코발트 S자 조형 스크린이 가로지르는 포토리얼 스터디
- seed: `1949316982481159071`
- 테스트 프로필: `strategic_coverage_figure_study`
- 이미지 생성: built-in `image_gen` 1회, 재시도 0회
- 최종 이미지: `/Users/chasoik/Projects/image-prompt/artifacts/photo-runs/20260902-suggestive-editorial-three-arm-v1/arm-02-figure-coverage/final.png`
- 이미지 SHA-256: `d20643a8fee7960d7007a7b114492b2744be4cd87fbe13e09aa36eeb259efab0`

## 감사 경계

- composed prompt: `pass`, blocking failure 0
- exact runtime request: `pass`, failure 0
- 위 두 결과는 사전 계약·문자열·참조 바이트 검증이며 픽셀 통과 근거로 대체하지 않았다.
- thumbnail(340x512)과 native(1023x1537)를 각각 직접 열어 판정했다.

## 픽셀 게이트

| Gate | Scale | 판정 | 이미지 근거 |
|---|---|---:|---|
| `vo_figure_coverage_adult_holistic` | both | pass | 한 명의 명백한 성인 피사체가 머리부터 양쪽 부츠까지 완전한 주 피사체로 보인다. |
| `vo_figure_coverage_stable_opaque_path` | both | pass | 단일 코발트 S자 패널이 위쪽 프레임에서 바닥까지 끊기지 않은 불투명 경로로 중앙의 옷 입은 몸통과 골반을 가린다. |
| `vo_figure_coverage_contour_continuity` | native | pass | 스크린 양쪽에서 어깨·허리·골반·허벅지·다리 선이 해부학적으로 자연스럽게 이어지며 붙인 검열 막대처럼 보이지 않는다. |
| `vo_figure_coverage_light_negative_space` | thumbnail | pass | 좌측의 강한 대각 방향광과 들어 올린 팔, 굽힌 팔·허리, 벌어진 다리 주변의 인체 경계 빈 공간이 입체 형태를 분명히 한다. |
| `vo_figure_coverage_complete_pose` | both | pass | 머리, 몸통, 양팔, 양다리, 지지하는 양쪽 부츠와 비대칭 포즈가 한 장의 전신 프레임에서 함께 읽힌다. |

결과는 5/5 gate pass이며 주요 실패는 없다. `partial_is_fail`을 적용했고, 프롬프트/runtime PASS를 픽셀 PASS로 간주하지 않았다. 기술적 시각 계약은 통과했지만 요청자의 미감 판단은 아직 `pending`이다.

참조 이미지는 `appearance_reference`로만 사용했다. 보이는 성인 얼굴 비율, 긴 짙은 웨이브 머리, 자연스러운 피부 질감 외의 정체성·동일인 여부 등은 평가하거나 주장하지 않았다.

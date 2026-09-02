# 은근한 성인 패션 시각 의미 v2 독립 렌더 검증

## 결론

시각 의미·후보팩 수정은 구조적으로 적용됐고, 세 장의 실제 이미지를 확보했다. 엄격한 픽셀 결과는 `1 PASS / 2 FAIL`이다. 별도의 전략적 드레이프 arm 한 건은 출력 moderation에서 차단되어 `UNSCORED`이며 품질 0점으로 환산하지 않는다. 사용자 미감 판정은 세 이미지 모두 `pending`이다.

## 적용한 일반화 수정

- `adult_everyday_controlled_reveal_moment`를 5개에서 9개 하드 게이트로 확장했다. 한정된 목표 관계, 행동-경계 인과, 축소 화면의 얼굴-경계 이중 현저성, 경계를 닫으면 의미가 사라지는 반사실적 필요성을 추가했다.
- `strategic_coverage_figure_study`를 5개에서 7개 하드 게이트로 확장했다. 하나의 주 가림 운반체와 별도 완전 불투명 전신 의복이 없는 비중복 필요성을 추가했다.
- `adult_controlled_reveal_window_editorial`은 실제 라펠-기반층 접촉 동작만 기본 후보로 남겼다.
- `strategic_coverage_figure_study_editorial`은 주 가림 운반체가 되는 불투명 드레이프 경로로 후보를 좁혔다.
- 요청자가 지각 효과에 초점을 명시했는데 그 효과가 uncovered이면 렌더하지 않도록 skill 절차에 fail-closed 검사를 추가했다.
- 넓은 `은꼴사` 표현은 exact alias나 보편 정의로 승격하지 않았다.

## 독립 실행 결과

| Arm | 실제 이미지 | 기술 판정 | 게이트 | 픽셀에서 보이는 관계 |
|---|---:|---|---:|---|
| `arm-01-action-boundary` | 있음 | PASS | 14/14 | 손이 모스그린 랩 경계를 직접 잡고 크림 기반층·쇄골 구간을 한정하며, 축소본에서도 얼굴과 경계가 먼저 읽힘 |
| `arm-02-primary-drape` | 없음 | UNSCORED | 0/0/7 | 출력 moderation `sexual` 차단; 픽셀 판정 불가 |
| `arm-03-layer-intersection` | 있음 | FAIL | 12/14 | 네이비 재킷·아이보리 기반층·허리 경계는 보이나 밝은 상의가 변경 경계보다 먼저 읽히고 스트랩이 없음 |
| `arm-04-hair-boundary-replacement` | 있음 | FAIL | 7/9 | 머리를 모아 드러난 등·어깨와 브론즈 오픈백 경계는 강하게 보이나, 한 손이 가려지고 원래 열린 드레스만으로도 장면 의미가 유지됨 |

## 해석 경계

- 프롬프트·런타임 감사 PASS는 픽셀 PASS가 아니다.
- 독립 환경은 빈 에이전트 컨텍스트, 별도 arm 입력·후보팩·프롬프트·렌더·리뷰 디렉터리, 다른 arm 입력 금지로 구현했다. 이들은 같은 프로젝트 파일시스템을 공유하지만 서로의 arm 산출물은 입력으로 사용하지 않았다.
- 세 장을 만들기 위해 출력 차단된 arm은 보존하고, 그 산출물을 보지 않는 새 대체 arm을 별도로 실행했다. 차단 arm을 재시도하거나 점수 0으로 처리하지 않았다.
- `partial`과 누락은 실패로 판정했다.
- 이미지에서 정체성, 동일인, 생체정보, 보호 특성, 건강, 매력도, 성격, 직업, 민족, 국적, 관계를 추론하지 않았다.
- 요청자의 실제 `은꼴` 체감은 기술 계약과 별개이므로 직접 판정 전까지 대표 이미지 승격을 하지 않는다.

## 핵심 산출물

- `coordination/source_snapshot.json`
- `coordination/root_evaluation_contract.json`
- `coordination/replacement_evaluation_contract.json`
- `coordination/root_pixel_review.json`
- 각 arm의 `candidate_pack.json`, `composed_prompt.json`, 감사 결과, 렌더 요청, 픽셀 리뷰와 해시

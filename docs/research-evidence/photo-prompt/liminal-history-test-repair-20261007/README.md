# 반복되는 liminal 역사 검증 실패 수정

2026-10-08 완료. 주 작업 공간에 적용했다.

반복 실패의 원인은 테스트의 잘못된 비교 범위였다. 10월 2일의 한국어 문구 한 줄 변경과 21개 유지 항목을 확인하는 테스트가 현재 확장 목록으로 과거 전체 데이터를 재구성했다. 이후 추가된 물·공포·팔레트 항목을 Vocaloid 시점의 예상 밖 신규 항목으로 오인했다. 현재 dirty 테스트에는 pose 소유자를 제외하면서 의존 character-appearance overlay를 포함하는 변경도 있어, hand_pose.pv_steepled_fingers를 찾지 못하는 오류가 먼저 발생했다.

테스트를 삭제하거나 건너뛰지 않았다. 해시로 인증된 과거 baseline과 raw proposal로 전체 역사 데이터를 재현하고 정확한 한 행 변경 및 21개 유지 항목을 비교한다. 별도로 일반 로더로 읽은 현재 전체 데이터에서 검토 대상 22개 항목의 의미·문맥·가드·관련 bundle 의무를 검사한다. 고정 snapshot, 기대값, holdout은 수정하지 않았다.

영문 의미 변경, 범위 가드 변경, 유지 대상의 한국어 변경, 항목 누락은 여전히 실패한다. 관련 없는 미래 후보 추가는 허용한다. 현재 전체 데이터와 과거 전체 데이터가 같아야 한다는 잘못된 전제를 제거했다. 분리한 의상·Vocaloid·신체·악기 검증 25개도 별도로 통과했다.

회귀 실행 중 별도 test_maintenance_prose_is_external_and_hash_bound에서 KeyError: maintenance_only를 확인했다. 승계 레코드는 해당 분류를 이전 레코드에서 상속한다. 기존 Git 구현의 prior_maintenance_ref 해시·스키마·소유자·순환 검증을 복원하여 승계 체인을 확인하고, 최종 분류가 true인지를 계속 검사한다. 메타데이터 원문이나 해시를 고치지 않았다. 변경 전 dirty 테스트는 이 폴더에 보존했다.

## 검증 결과

| 실행 | 결과 |
|---|---|
| 관련 159개 최초 배치 | 158개 통과, 별도 메타데이터 검사 오류 1개 |
| 두 수정 후 대상 재검증 | 12개 통과 |
| 분리한 의상·Vocaloid·신체·악기 검증 | 25개 통과 |
| 주 작업 공간의 고유 테스트 최종 판정 | **184개 통과, 실패·오류 0개** |
| 격리 worktree의 liminal 파일 | 11개 통과 |
| 전체 unittest suite | 실행하지 않음 |

최종 판정은 테스트 ID별 최신 실제 결과의 합산이다. 메타데이터 검사 수정 후 159개 전체 배치를 반복하지 않았고, 수정한 대상 12개를 재검증했다. 최초 오류 로그도 그대로 보존했다.

이 작업에서 런타임 데이터나 인덱스를 수정하지 않았다. 보호 대상 파일 118개와 그중 authored/derived asset 107개의 bytes가 변경 전과 일치한다. 기존 역사 artifact의 SHA 검증도 모두 유지한다. 커밋·push는 수행하지 않았다.

[수정된 liminal 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_liminal_active_use_korean_data_cleanup.py:78) · [승계 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_candidate_semantics.py:111) · [원인과 유지한 불변조건](CAUSE-AND-REPAIR.json) · [최종 테스트 결과](TEST-RESULTS.json) · [원본 보존](PRESERVATION.json)

실행 근거: [최초 실패](failure-before.log), [159개 배치](related-tests.log), [수정 후 재검증](final-targeted-tests.log), [별도 소유 영역 검증](owning-integration-tests.log), [worktree 검증](worktree-liminal-tests.log). 변경 전 파일은 [liminal](test_before.py), [메타데이터 검사](candidate_semantics_before.py)에 보존했다.

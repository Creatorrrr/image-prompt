Agent-2 독립 테스트는 완료했으며 전체 픽셀 판정은 **FAIL**입니다. 첫 생성은 정식 gate 8/12, 같은 core의 targeted retry는 11/12 PASS입니다. 최종 `vo_soft_full_torso_volume`은 복부·허리·몸통의 연속적인 충분한 양감이 확인되지 않아 FAIL입니다. 보충 검사의 종아리 양감은 바지와 부츠 아래에서 UNOBSERVABLE입니다.

독립 seed는 `8290468901664686725`입니다. 운하 수문 옆 이동식 그림자극 트럭, 비 갠 황혼과 따뜻한 리허설 조명, 트레이싱 페이퍼 마스크, 배경막을 펼친 직후의 휴식을 하나의 작업 장면으로 작성했습니다. 새 인물의 28세 성인 무대 디자이너 설정과 체형·포즈는 독립 author 선택입니다. 첨부 사진은 보이는 얼굴·머리카락 안내로만 사용했습니다.

Core와 baseline은 2026-10-03T09:36:51.378284+00:00에 후보 조회 전에 동결했고 현재 core 파일 해시와 baseline 본문 해시가 일치합니다. 정확히 한 V6 pack(`fe67f8c9d33e817d`)을 사용했습니다. `slot:body_pose:sv_supported_m_legs`를 선택했고, `visual-concept:soft_full_figure_volume`과 `visual-concept:rb_support_compression`의 정식 gate 전체를 검사했습니다. `sv_seated_knees_apart`와 silhouette soft-volume 후보도 실제로 노출됐습니다. M형 optional visual-concept는 노출되지 않아 상세 M 판정은 보충 검사로 구분합니다.

| 정식 gate | 첫 생성 | retry |
|---|---|---|
| `vo_soft_full_multiregion` | FAIL | PASS |
| `vo_soft_full_torso_volume` | FAIL | FAIL |
| `vo_soft_full_limb_volume` | FAIL | PASS |
| `vo_soft_full_not_padding_or_value` | FAIL | PASS |
| `vo_rb_support_compression_1` | PASS | PASS |
| `vo_rb_support_compression_2` | PASS | PASS |
| `vo_rb_support_compression_3` | PASS | PASS |
| `embodiment_body_ownership` | PASS | PASS |
| `embodiment_joint_chain_and_reach` | PASS | PASS |
| `embodiment_support_and_balance` | PASS | PASS |
| `embodiment_contact_and_space` | PASS | PASS |
| `embodiment_visibility_and_projection` | PASS | PASS |

| 보충 fidelity | 첫 생성 | retry |
|---|---|---|
| `same_pelvis_seat_support` | PASS | PASS |
| `bent_spread_knees_m_projection` | PASS | PASS |
| `both_legs_and_boot_support` | PASS | PASS |
| `distributed_soft_volume` | FAIL | FAIL |

두 원본 모두 낮은 좌면에 지지된 같은 골반, 그보다 높은 두 벌어진 굽힌 무릎, 발→무릎→골반→무릎→발의 연결 M 윤곽, 두 발의 접지가 보입니다. 넓은 발폭만으로 M형을 판정하지 않았습니다. Retry에서 상완과 허벅지 양감은 개선됐지만, 몸통 양감 실패와 의복 아래 종아리의 관찰 불가를 그대로 유지합니다. 서로 다른 이미지의 성공 요소를 합쳐 통과시키지 않았습니다.

[최종 standalone prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/prompt.retry1.en.txt) · [첫 prompt](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/prompt.en.txt) · [첫 native 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_1.png) · [retry native 이미지](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_2.png) · [정확한 testcase](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/testcase.json)

[구조화 최종 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/final_report.json) · [후보 기여/선택 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/candidate_contribution_review.json) · [retry 계보](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/targeted_retry_lineage.json) · [최종 pixel audit](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_2.pixel_audit.json) · [보충 픽셀 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/tests/agent-2/native_attempt_2.supplemental_review.json)

| 바인딩 | SHA-256 |
|---|---|
| Frozen core 파일 | `2f360de8f56c9b42a28947d41085dba6679d63f1eb1cc39ba91edd49950d8dff` |
| Normalized pack core | `0ab4ef07013b7fa811e821030c4566508618537c61d32cba6417a3c1e49271ec` |
| Intent lock | `8b62fe2f7f81fab6fbae5d21757963f970180658789825d5bd4b81fb61a32010` |
| Effective visual contract | `fb4806678777e72af715c4805dbffbb158f85d4ceefa07d0e68e22bace166974` |
| Qualified inputs snapshot | `c3b4c38a2bbf0191bcf8bce7ee19944ba9800726ec21c20528d8319c42a3865a` |
| 최종 prompt 본문 | `ff89cbc2bd08350fcb481f1a97d7e687824edc3406c6c78d56d8ec4334263e85` |
| 첫 native 이미지 | `61318259bce6f0ac726500ee7034f82562d27ba968246b48dcbfa729fe03df87` |
| Retry native 이미지 | `5758ea1e89e6a2b147e31016f7a4d7f1ed99b0d080b00e8b2fe6a2824a8471ad` |

M 관계와 여러 영역 양감은 후보 조회 전 baseline에 이미 작성돼 있었습니다. 후보는 소유자 관계 바인딩과 관찰 가능한 구성요소, 정식 profile gate 7개를 추가했습니다. Baseline-only 이미지가 없으므로 개선을 새 데이터만의 효과로 주장할 수 없습니다. 사용자의 선호·수용 판정도 아직 없습니다.

Built-in native imagegen 두 호출은 모두 성공했고 원본을 변형 없이 저장했습니다. Composition/runtime audits는 두 회차 PASS, pixel audit schema 실패는 없습니다. 이미지 호출 성공과 픽셀 all-of qualification은 별도로 기록했습니다. 공유 ledger는 프로젝트 recorder로만 기록했으며 CLI/model fallback, 추가 pack 조회, 세 번째 생성은 없습니다. Retry 400단어의 advisory 초과와 좁은 수정 이유도 계보에 보존했습니다. Standalone 텍스트 파일에는 끝 개행 1개가 있으며 본문 해시는 그 개행을 포함하지 않는 JSON/native 입력을 가리킵니다.

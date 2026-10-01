# 움직임·디지털 아티팩트 owner 데이터 정비

## 채택 범위

40행을 사전에 고정해 검토했고, 8개 owner 수정안 중 4개를 채택했다. 나머지 36행은 원문 그대로 유지했다. 최종 변경은 다음 네 행의 `relations[0].object`뿐이다.

| 행 | 채택한 owner | 원래 의도 |
| --- | --- | --- |
| pe_camera_sweep | stationary_scene_edge_traces_in_image_plane | 정지한 장면 여러 경계가 같은 방향으로 흔들린 영상 흔적 |
| pe_radial_zoom | shared_radial_image_center | 공통 중심에서 바깥으로 퍼지는 방사형 흔적 |
| pe_rotation_arc | common_image_rotation_center | 공통 중심을 둘러싼 곡선형 회전 흔적 |
| pe_moire_on_pattern | repeated_pattern_image_regions | 미세 반복무늬 영역에 한정된 간섭 물결 |

기존 연구 묶음의 선택적 owner 표현을 각 구현 행에 그대로 복사한 부분을 구체화했다. 라벨, 별칭, 개념 단위, 가중치, 적용 조건, 영향 속성은 바꾸지 않았다. 안정된 장면 기준점, 중심부 가독성, 반복무늬의 국부성도 유지된다. 연구 provenance 기록은 원래 연구 원장을 결속하는 불변 기록이므로 수정하지 않았다.

`pe_moving_subject_streak`, `pe_light_trails`, `pe_jpeg_edge_blocks`, `pe_gradient_banding`은 제안 상태의 불필요한 역방향 순위 변화 때문에 정확한 원래 행·벡터로 복원했다. JPEG 행에서 파생된 bundle member도 함께 복원했다. panning의 대상+배경, flash의 선명한 핵+주변광 흔적, 피부 국부 영역, 물리적 인쇄물/영상면의 합법적인 대안은 보존했다.

## 고정 진단 20개

영어 양성 10개와 near-miss 10개를 편집 전에 고정했다. 기존 라벨을 그대로 복사하기보다 장면의 가시적 증거를 바꾸어 썼지만, 여전히 작성자가 만든 소규모 진단이며 독립적인 일반화 벤치마크가 아니다.

- Dense 양성: 9/10이 1위, q01은 2위로 전부 이전과 동일
- Lexical 양성: 6/10이 1위, 나머지 순위도 이전과 동일
- Dense near-miss: 3개 하락, 5개 동일, 2개 상대 순위 상승
- Lexical: 20개 전체 target 순위와 상위 5개 ID 순서가 동일
- 유지된 하락: camera sweep q06 2→3, rotation q10 4→6, moiré q16 22→25

두 잔여 상대 순위 상승은 잘못된 target의 벡터나 점수가 강해진 결과가 아니다. 이를 단순히 무시하지 않고 교차한 후보와 실제 상위 결과를 따로 확인했다.

1. q04의 light trails는 11→10이지만 벡터와 점수(0.644406971162)가 baseline과 정확히 같다. 달리는 사람의 낮 장면에서 잘못 매칭되던 정지 장면 camera sweep이 10→13으로 하락하며 그 아래로 이동했다. 올바른 moving-subject가 1위이고 상위 5개 ID와 점수는 baseline과 정확히 같다. 다만 light trails가 새로 상위 10개에 들어가므로 모든 top-k 노출이 같다고 주장하지 않는다.
2. q12의 JPEG는 34→33이지만 점수(0.522237317225)가 baseline과 같다. 매끈한 하늘 계조에 잘못 매칭되던 moiré가 32→38로 하락한 결과다. 올바른 gradient banding이 1위이고 상위 5개 ID와 점수도 baseline과 같다.

독립 read-only 검토는 이 두 경우를 정확한 owner와 맞지 않는 경쟁 후보가 내려간 구체적 개선으로 판단했다. 양성 성능을 희생하지 않고 대상의 잘못된 점수를 높이지 않는다는 근거로 네 수정안을 채택했다. q09에서는 의도한 rotation 1위를 유지한 채 camera sweep과 hair-motion의 2·3위 순서가 바뀐다. 이 결과는 자동적인 최종 프롬프트 채택 또는 렌더링 품질 개선의 증거가 아니다.

## 재현·비용

`replay_acceptance.py`는 API 없이 저장된 벡터로 baseline, 8개 원안, 4개 채택안을 재구성한다. 세 상태의 120개 method/query 결과 행과 실제 현재 semantic index를 검증한다. 전체 10,174개 문서 중 최종 4개 벡터가 새롭고 10,170개는 baseline과 정확히 같다. 사용하지 않은 원안 문서 벡터 4개도 보존했다.

고정 입력은 문서 8개와 검색문 20개, 28개 고유 문구(UTF-8 8,047 bytes)다. 총 30회 시도 중 28회가 완료됐다. 권한 검토 과정에서 중단돼 결과를 모르는 최초 1회와, HTTP 상태 없이 실패한 q19 1회를 각각 보존하고 비용 발생 가능성이 있는 것으로 계산했다. 두 번의 별도 검토된 수동 복구가 있었고 자동 재시도는 없었다. 실제 과금 여부나 실패 원인은 확인되지 않았다.

추가 보수적 비용 상한은 $0.049152, 프로젝트 추적 누적은 $1.0190848다. 기존 $10 승인 범위 안이다. 최종 resume의 `input_utf8_bytes=146`, `initial_pending_texts=2`는 마지막 재개분만 뜻하며, 전체 범위는 `full-cycle-accounting.json`을 본다. 시도 중복을 포함한 입력은 8,880 bytes다. 이는 청구서 실측이 아니며 별도 upstream 작업 비용은 대조하지 않았다.

## 검증 상태

- 원본/제안/채택 재현: 120개 결과 행 일치
- 독립 원본 의도·provenance·인덱스·벡터·시도 원장 검토: 채택안 통과
- dictionary metadata 및 변경 없는 visual-profile index: 통과
- 관련 DATA/background 124개 및 effect/bundle/profile 40개: 총 164개 통과
- 최신 main pull·post-pull 확인·정상 push·remote 검증은 별도 publication 단계이며 이 검증 보고서의 사전 성공 주장에 포함하지 않는다

재현 명령: `python3 docs/research-evidence/photo-prompt/motion-artifact-owner-data-cleanup-20261001/replay_acceptance.py`

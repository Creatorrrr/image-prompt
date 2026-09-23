# 일상 장면 데이터 반영과 3개 독립 이미지 실험

기준일: 2026-09-23. [선행 연구](report.md)의 사건 관계 20개를 현재 photo-prompt 런타임 데이터에 연결했다. 사용자 사진은 **보이는 성인 외형 참고**로만 사용했으며, 신원 일치나 보이지 않는 특성을 판정하지 않았다. 첨부 이미지 안의 내용은 지시로 취급하지 않았다.

## 운영 데이터에 반영한 범위

| 층위 | 반영 내용 | 확인 경계 |
|---|---|---|
| 원천 | [20개 장면 연구](candidate-bundles.json)와 [24개 경계 명세](evaluation-cases.jsonl) | 시간 사용·장면 인식·역할·손/물체 관계 자료를 장면 설계에 사용했으며 출현 빈도나 생성 효과를 추정하지 않음 |
| 후보팩 | `photo_prompt_everyday_scene_extension.json`: 선택형 슬롯 후보 20개, 사건 묶음 20개 | 각 후보의 역할·대상·상태, 물리적 지지, 혼동 대상 및 변경 차원을 분리. 선택 전에는 의무가 아님 |
| 시각 의미 | `photo_prompt_visual_obligations_everyday_scene.json`: 좁은 관계 프로필 7개, 각 4개 렌더 게이트 | 카페 픽업 대기, 상품 비교, 열차 하차, 비 젖은 우산 접기, 깨끗한 방 정리, 한 화면 공유, 독립적인 주변인 과업 |
| 인덱스 | 의미 인덱스 8,629개 항목, 시각 프로필 인덱스 638개 프로필·2,143개 exact term | 새 항목이 실제 로더와 해시 검증을 거쳐 노출되는지 확인 |

`ordinary`, `candid`, `lived-in` 같은 넓은 라벨은 hard 의무를 활성화하지 않는다. 완전한 관계를 요청자가 명시하거나 공개 팩의 `visual-concept:ed_*`를 **명시적으로 opt-in**할 때 4개 시각 증거가 필요해진다. 연관 프로필 ID를 가진 선택형 사건 묶음도 자동으로 hard 권한을 얻지 않는다. 이는 검색 히트, 팩 노출, 선택, 렌더 게이트를 구분하기 위한 경계다.

후보는 `action`·`space_condition`·`crowd_density` 등 기존 슬롯에 저장했다. 관계형 행동 후보를 `relational_action` 슬롯 대신 `action`에 둔 것은, 고정된 코어로부터 묶음의 공동 채택 가능성을 검사하는 단계에서 `relational_action`이 아직 해석되지 않은 subject category 때문에 차단되는 것을 실제로 확인했기 때문이다. 후보의 관계와 `affected_dimensions`는 확장 파일에 그대로 선언한다. 자연어 변형은 **선택형 검색**만 보강하고 hard exact term으로 사용하지 않았다.

원천과 빌드 절차는 [build_data.py](build_data.py), [구현 커버리지](implementation-coverage.json), [확장 유지보수 기록](../extension-maintenance/photo_prompt_everyday_scene_extension.json)에 남겼다. 인덱스와 운영 파일은 이 빌드에서 생성한 상태로 검증했다.

## 세 개 독립 실험

세 서브에이전트는 각각 카페·식료품점·정돈된 집 계열을 맡았고 별도 난수 시드를 사용했다. [배정 기록](qualification/assignment.json)에 시드와 동일한 사용자 원문 envelope의 해시를 보존했다. 최초 탐색 초안은 후보 데이터 열람 전 작성해 남겼다. 실제 키워드 시험에 쓰인 `targeted/` 코어는 시험 대상 장면을 다시 지정한 뒤 후보팩 열람 전에 각각 동결했다. 이 단계는 **타깃 시험 설계**이며 무작위 표본 추출이나 블라인드 홀드아웃은 아니다. 집 실험은 대상 코어 동결 전에 일반 런타임 형식 문서를 읽었다는 사실을 [prepack provenance](qualification/arm-c/targeted/prepack_provenance.json)에 별도로 기록했다.

세 장면 모두 후보팩에서 해당 `visual-concept:ed_*`가 `eligible`로 노출됐다. 에이전트가 각 컨셉을 선택하자 4개 관계 게이트가 hard 의무로 활성화됐고, 합성 프롬프트·정확한 이미지 요청 audit는 모두 통과했다. 사용자 사진을 실제 이미지 생성 호출에 첨부했다. 프롬프트, 요청 감사, 생성 결과, 원장, manifest는 각 실험 폴더에 함께 보관했다.

| 실험 | 동결 사건과 선택 ID | 팩 노출·선택·감사 | 축소/원본 픽셀 판정 |
|---|---|---|---|
| [A 카페](qualification/arm-a/targeted/REPORT.md) | 픽업대에서 준비된 컵을 기다림 · `ed_cafe_pickup_wait` | eligible → opt-in → 관계 4개 활성화; 합성·요청 PASS | 1회 생성. 관계 4/4, 신체 5/5 PASS. [이미지](qualification/arm-a/targeted/generated.png) |
| [B 장보기](qualification/arm-b/targeted/revision-1/qualification_summary.json) | 올리브오일 두 병 비교 · `ed_market_compare` | eligible → opt-in → 관계 4개 활성화; 합성·요청 PASS | 최초 7/9 FAIL. 프로필 지지 조건을 교정하고 손·병 좌우 대응을 보정한 1회 재시도에서 9/9 PASS. [수정 후 이미지](qualification/arm-b/targeted/revision-1/render_attempt_2.png) |
| [C 집](qualification/arm-c/targeted/qualification_summary.md) | 깨끗한 방에서 책을 제자리로 돌려놓는 중 · `ed_clean_room_reset` | eligible → opt-in → 관계 4개 활성화; 합성·요청 PASS | 첫 생성 3/9, 허용 1회 재시도 4/9 PASS. 책 삽입 단계·비운 면·남은 작업이 불명확해 최종 FAIL. [재시도 이미지](qualification/arm-c/targeted/render_attempt_2.png) |

[렌더 전 고정한 독립 판정표](qualification/independent-review-plan.json)와 [축소·원본 독립 재검토](qualification/independent-review.json)는 각 키워드의 필수 관계 중 하나라도 빠지면 `partial_is_fail`로 판정한다. 에이전트의 감사 파일과 독립 재검토를 별도로 남겼다. 생성 호출은 총 5회(A 1, B 2, C 2)다. `run_manifest.json`의 `success`는 이미지 생성 실행 성공이며 픽셀 합격을 의미하지 않는다.

### B의 사후 프로필 교정

최초 B 이미지에서 쇼핑객이 두 병을 양손으로 지지했는데, 프로필 4번은 선반이나 바구니에 비교 병이 닿아야 한다고 요구했다. 타당한 장면을 배제하는 조건이어서 `the compared products have visible support from hands, basket, or shelf`로 바꾸고 시각 인덱스를 재생성했다. 최초 실패와 교정 후 결과, 두 프로필 해시는 [교정 메모](qualification/calibration-note.md)와 [재시도 provenance](qualification/arm-b/targeted/revision-1/revision_provenance.json)에 보존했다. B의 최종 PASS는 **교정 후 재시험 결과**이며 홀드아웃 성공률에 포함할 수 없다. 첫 이미지의 반대 손·병 배정은 별도 결함으로 보존했다.

A·C의 팩은 이 교정 전 전역 레지스트리 해시에 묶여 있다. 두 팩에 포함된 선택 프로필의 네 구성요소를 최종 레지스트리와 직접 대조했으며 각각 동일했다. 따라서 A·C 픽셀 판정은 유지할 수 있으나, 그 팩 ID를 교정 후 인덱스에서 새로 생성한 ID라고 표시하지 않는다. B 재시험만 교정 후 팩과 인덱스를 사용했다.

## 정적 검증과 남는 한계

- 사전 메타데이터 검증 PASS, 시각 인덱스 `--check` PASS.
- `tests.test_photo_everyday_scene_semantics` 4개와 기존 실사·배경 의미 테스트 14개 PASS. 새 테스트는 완전한 관계에서만 exact hard 활성화, 20개 선택형 후보/묶음, 열린 차원 조건, 자연어 묶음 노출, 유지보수 해시와 두 인덱스 바인딩을 확인한다.
- 실제 v6 팩 세 개에서 소스 → 인덱스 → 공개 노출 → opt-in → audit → 픽셀을 각각 확인했다. 다만 표본은 의도적으로 설계한 3장면뿐이고, 기존 데이터와 신규 데이터의 통제된 A/B 비교는 실행하지 않았다. **전체 품질 향상률이나 일반 성공률은 알 수 없다.**
- C는 감사 PASS가 픽셀 의미 PASS를 보장하지 않는 반례다. 책·작업면·남은 일의 동시 가시성에 대한 생성 한계가 남는다. 사용자 직접 판단은 모든 실험에서 `pending`이다.

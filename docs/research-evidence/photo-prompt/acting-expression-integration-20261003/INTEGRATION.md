# 연기·표정 의미 데이터 반영 기록

실제 시각 의미 등록과 후보팩용 데이터 반영을 완료했다. 기존 계약을 사용했고 주제별 분기나 고정 감정→표정 라우터는 추가하지 않았다. 연구 패키지는 당시 검증 결과를 유지하는 역사적 자료로 보존했다.

## 반영 범위

| 자료 | 실제 변경 |
|---|---|
| 시각 의미 프로필 | 11개 추가. 각 프로필의 관찰 요소 2개를 증거 문장과 native gate로 연결 |
| 후보 | 37개 추가: expression 32, body_orientation 2, hand_pose 1, gaze_engagement 2 |
| 의미 묶음 | 11개 추가. 채택은 optional이며 프로필을 자동으로 필수화하지 않음 |
| 기존 항목 보강 | 12개 대상의 동등한 표현 또는 사용 문맥을 추가. 기존 의미·효과·가드는 유지 |
| 중복 정리 | 자기 손으로 자기 입을 가리는 후보와 `입틀막`을 하나로 통합 |
| 문맥 제한 | 14개 후보에 frozen primary context 가드; 성인 매혹 표현 3개에 adult 가드 |
| 운영 연결 | 기존 extension 목록과 required extension 목록에 등록 |
| 검색 색인 | 시각 프로필 1,507개와 exact term 3,661개; 의미 검색 항목 9,737개와 16개 shard 재생성 |

입술 압착과 입술 긴장, 입꼬리 하강, 안쪽 눈썹 상승과 모음, 한쪽 눈썹 상승, 코 주름, 윗입술 상승, squinch, 눈물 고임과 압착 입술의 복합 형태, 자기 손과 자기 입의 접촉을 서로 구별한다. 넓은 감정이나 매력·진정성·실제 심리 상태를 특정 얼굴 형태와 동일시하지 않는다. 시간 변화, microexpression 지속시간, 목소리와 연기 방법론은 단일 정지영상의 강제 후보로 넣지 않았다.

자료 파일:

- `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_acting_expression.json`
- `skills/photo-prompt-image-generator/assets/photo_prompt_acting_expression_extension.json`
- `docs/research-evidence/photo-prompt/extension-maintenance/acting-expression-20261003-v1.json`

`DATA-SOURCE-FREEZE.json`은 작성 데이터·운영 연결·검색 색인·shard·회귀 테스트의 정확한 파일 해시를 기록한다. 문맥과 출처의 한계는 외부 유지보수 기록에 두며 긍정 검색 문장에 섞지 않는다.

## 후보팩 동작에서 확인한 경계

세 이미지 사례는 표정 테스트를 필수로 동결했으므로 expression 슬롯의 optional 후보가 노출되지 않았다. 이는 잠긴 표정을 optional 후보가 교체하지 못하게 하는 기존 범위 규칙이다. 테스트 에이전트는 이 부재를 숨기거나 존재하지 않는 후보 ID를 삽입하지 않았다.

독립 baseline은 표정의 관찰 요소를 데이터 열람 전에 이미 분해했다. 이후 `agent_postcore_interpretation`의 `source_text`를 그 동결 필드 전체와 정확하게 바인딩하여 새 프로필을 선택했다. 최종 프롬프트에는 같은 의미의 canonical positive evidence를 추가했다. 사용자 원문·동결 core·intent lock은 보존했다. 이 경로는 해당 키워드가 사용자 원문에서 자동 exact 활성화됐다는 증거와 구별한다.

추가 합성 유지보수 사례에서는 expression을 열린 선택으로 두고 현행 V6 흐름 전체를 실행했다. `ae_lip_press`가 실제 public expression 후보에 노출됐고 채택 정책은 optional이었다. 해당 결과는 `V6-OPEN-EXPRESSION-PACK.json`에 보존했다. 이 합성 fixture를 실제 사용자의 별도 요청이나 이미지 생성 사례로 제시하지 않는다.

## 회귀 검사

새 데이터의 12개 테스트는 이중 언어·부정·문맥·입술/눈썹 혼동 경계, 성인 가드, 후보가 자기 태그로 문맥을 만들지 못하는 규칙, property lock, 기존 로봇/작업 의미의 보존, 부정·출처의 긍정 검색 유입 방지, 외부 기록 해시, 실제 merged index와 V6 후보 노출을 확인한다.

과거 상태를 재구성하는 3개 테스트는 pose extension을 제외하면서 새 acting overlay가 pose 소유 항목을 참조하는 문제를 발견했다. 그 역사적 projection에서 두 extension을 함께 제외하도록 수정했다. 역사적 기대값·해시·holdout은 변경하지 않았고 기존 의미를 비교하는 검사는 유지했다.

전체 unittest 발견 범위의 최종 결과와 예외의 귀속은 `FULL-SUITE-RESULT.json` 및 `FINAL-VERIFICATION.json`에 기록한다. 최초 병렬 실행 도구의 import path 오류는 작업 도구 문제로 보존하고, 올바른 import path에서 성공한 모듈 증거만 재사용했다. 재사용과 새 실행의 test ID multiset이 전체 발견 범위와 동일한지도 검사한다.

별도 illustration 스킬의 고정 photo baseline byte 검사 실패는 변경 전 Git `840d4b8f0dbcb977b3d02b5dbcce38894bcd0ec4`를 읽기 전용으로 추출한 checkout에서도 재현됐다. 실패를 숨기기 위해 해당 baseline을 갱신하지 않았다. 비교 로그는 `baseline-sibling-photo-regression.log`에 보존한다.

## 이미지 검증

서로 독립된 세 에이전트가 난수로 서로 다른 복잡한 컨셉을 고르고, 원본 요청 envelope·pre-core 기록·seed·동결 해시·V6 pack·standalone prompt·runtime 입력·native 원본·strict 픽셀 리뷰를 각 사례 폴더에 저장한다. 원본 사진은 허구의 성인 배우에 대한 보이는 얼굴·머리 참고로 사용한다.

픽셀 평가는 한 이미지의 모든 hard gate가 충족돼야 통과한다. partial은 실패이며 가려진 필수 요소는 UNOBSERVABLE이다. 시도 간 증거를 합산하지 않는다. 각 사례는 최초 생성과 최대 한 번의 국소 수리를 보존한다. 사용자 취향과 수용 여부는 기술 검증 결과에 포함하지 않는다.

최종 개별 결과·생성 파일·프롬프트·부모의 독립 재검토는 `artifacts/photo-prompt/acting-expression-20261003/RESULTS.md`와 `FINAL-VERIFICATION.json`에 모은다. 이번 세 사례 결과를 새 후보 37개 전체의 생성 성공률이나 보편적인 감정 인식 성능으로 확대 해석하지 않는다.

# Neutral expression alternatives: actual integration

요청한 시각 의미 대체 표현과 후보팩 반영을 완료했다. [앞선 연구](../neutral-expression-semantics-20261003/README.md)의 관찰 가능한 형태를 현재 데이터 계약으로 다시 작성했으며, 연구 JSON이나 평가·동기·이력 표현을 그대로 런타임 별칭으로 넣지 않았다. 독립 에이전트 세 명이 다른 무작위 복합 장면을 선택하고 첨부 사진으로 실제 이미지를 한 장씩 생성했다. [이미지 검증 결과](../neutral-expression-native-qualification-20261003/README.md)는 코드·검색 결과와 별도로 판정한다.

## 실제 반영

| 대상 | 변경 | 보존한 기준 |
| --- | --- | --- |
| 기존 시각 의미 44개 | 한국어·영어 positive paraphrase 176개 추가 | 기존 정의, 구성요소의 의미, 효과, render gate |
| 기존 morphology 프로필 14개 | 구성요소 대체 표현 86개, 공통 소유자 표현 28개 추가 | 모든 필수 그룹과 minimum/all-of 조건 |
| 기존 일반 후보 42개 | 대체 표현 154개 추가 | 기존 label, en, 효과, guard, lock |
| 신규 시각 의미 3개 | 국소 살집, 지정 몸통 구간의 안팎 곡선, 현재 입술 내밂 | 범위·소유자·현재 형태의 명시 |
| 신규 일반 후보 2개 | 국소 살집·국소 곡선 | `silhouette_proportion`의 기존 속성 검사 |
| 현재 입술 동작 후보 | 기존 `ae_pucker` 재사용·보강 | 원래 입술 두께와 현재 동작을 분리 |
| contextual usage | 시선/감정, 입술 구조/동작, 현재 표면/시간 물성 분리 기록 3개 | 양의 검색 원형에 넣지 않음 |

새 파일은 [시각 의미 extension](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_neutral_expression.json)과 [후보 extension](../../../../skills/photo-prompt-image-generator/assets/photo_prompt_neutral_expression_extension.json)이다. 공유 생성기 수정은 이 두 파일의 로딩 등록이다. 기존 시각 의미 세 파일에는 동일한 범위의 표현만 추가했다.

새 exact term은 `adult regional rounded soft volume`, `성인 특정 부위의 둥근 살집 윤곽`, `adult regional convex-concave contour transition`, `성인 지정 몸통 구간의 안팎 곡선 연결`, `current forward lip pout`, `현재 입술을 앞으로 내민 표정`의 여섯 가지 좁은 표현이다. `plump`, `fleshy`, `curvaceous`, `pouty` 단독 표현을 새 exact trigger로 올리지 않았다. 검색 노출은 선택 제안이며, core와 잠금·소유자·필수 구성요소 검사를 통과해야 채택할 수 있다. 국소 요청을 전신 체형으로 넓히거나 특정 가슴·허리·골반을 강제하지 않는다.

전체 registry는 **1,510개**, 일반 후보는 **9,703개/112개 슬롯**이다. Gemini embedding 2, 768차원을 유지하면서 바뀐 양의 원형만 다시 임베딩했다. 일반 semantic index는 **9,739개 entry/16개 shard**다. 이전 tracked shard 192개는 원본 그대로 복구해 보존했다. 재생성 중 대체된 이전 untracked 파생 generation까지 보존했다는 주장은 하지 않는다.

연구 44개 unit의 처리 결과는 좁은 프로필 추가 3개, 기존 의미 대체 표현 보강 24개, 기존 전체 계약 유지 5개, core 문맥에 남긴 항목 12개다. [RESEARCH-DISPOSITION.json](RESEARCH-DISPOSITION.json)에 연구의 181개 키워드 그룹과 이전 assistant 예시 25개, 후보 연구 초안 24개를 모두 연결했다. 이 원장에 연결된 것은 관찰 가능한 범위이며 181개 그룹 전체의 어휘·용례를 exact alias로 검증했다는 뜻은 아니다. 원래 연구의 외부 출처 ID와 검증 보류 범위도 남아 있다.

## 확인된 범위 오류 수정

실제 V6 전체 흐름에서 도덕적 `타락`을 봉투 수령·약속 포기로 작성했을 때 신체의 어둠 변형이 요구되는 오류를 재현했다. `embodied_corruption_transition` 데이터의 문맥 활성화 표현을 실제 신체 변형에 해당하는 표현으로 좁혔다. 기존 exact term과 변형 구성요소·gate는 유지했다.

[FULL-CORE-BEFORE.json](FULL-CORE-BEFORE.json)과 [FULL-CORE-AFTER.json](FULL-CORE-AFTER.json)에서 도덕적 선택은 FAIL→PASS, 실제 신체 변형·사용자 정의·부정 문맥은 PASS를 유지한다. 별도의 핵심 판단 분기나 키워드별 코드를 추가하지 않았다.

## 검증

- 새 회귀 테스트 **12개 PASS**: 좁은 단어 활성화, 물체/얼굴 다의어, 부정, advisory 보존, 모든 구성요소와 공통 소유자, 국소/전신 구별, 부분 속성 잠금, 구조/동작 분리, 양의 검색에서 문맥·제한 제외를 확인했다.
- 작성한 전체 문장 10개를 같은 검색 정책으로 비교해 기대 의미 접근은 **보강 전 0/10→후 10/10**, 예상 밖 hard obligation은 0개였다. 이는 **exact+BM25F의 어휘 접근 비교**다. 문장 전체는 검색 데이터에 넣지 않았지만 구성요소의 대체 표현은 포함되므로 독립적인 자연 요청 일반화 성능이나 픽셀 성능 지표로 해석하지 않는다.
- 기존 프로필 **1,507개**, 기존 일반 후보 **9,701개**의 정의·효과·필수 조건·guard 보존 검사 PASS. 문맥 활성화 예외는 위의 `embodied_corruption_transition` 하나다.
- dictionary validator, visual profile index check, `git diff --check` PASS. agent가 사용한 운영 입력 **92개**와 초기 동결 입력 A15/B14/C16개 해시가 끝까지 일치한다.
- 전체 unittest discovery **1,245개 실행**. 첫 전체 실행의 실패 batch 9개는 기록을 보존하고 수정한 뒤 **33개 테스트를 재검사해 모두 PASS**, 최종 미해결 실패는 0개다. [전체 최종 결과](FULL-SUITE-FINAL.json), [최초 실행](full-suite-parallel/RESULTS.json), [새 회귀 로그](focused-tests-final.log), [불변성·문장 비교](DATA-INVARIANTS-AND-HOLDOUTS.json).

과거의 snapshot 비교는 뒤에 추가된 neutral extension을 과거 로더에서 제외하고, 의미가 같은 표현 추가만 명시적으로 허용하도록 조정했다. 과거의 정의·label·효과·guard·gate를 새 값으로 덮어쓰지 않았다. sibling illustration의 **현재** photo baseline은 전체 public pack을 비교한 뒤 source/provenance hash 변화만 확인해 SHA와 pack ID만 갱신했다. 후보 64개, core, 제약, negative와 V1–V4 역사 기준선은 같다. [전체 비교](CURRENT-BOUNDARY-COMPARISON.json), [갱신 근거](BASELINE-REFRESH.json).

## 이미지 검증의 해석과 다음 개선

세 arm은 실제 요청 envelope와 별도로 자신의 합성 장면·단어 범위를 작성했다. `user_definitions=[]`를 유지했고, 운영 데이터나 다른 arm 결과를 보기 전에 core·baseline·controls·픽셀 조건을 동결했다. 데이터 준비 후 정상 V6 CLI로 후보를 조회·선택하고 prompt/runtime 감사에 통과한 정확한 문구와 첨부 파일로 native 생성을 수행했다. 첨부 사진의 보이는 얼굴·머리만 참고하고 각 인물의 성인 연령·체형·역할은 합성 장면에 명시했다.

첫 제본실 이미지는 아래배의 몸 볼륨과 옷 주름 구별, 지정 몸통 옆선의 연속 가시성에 실패했다. 광학 장면은 가는 체격·긴 사지를 보여도 `sinewy`에 필요한 국소 근육·힘줄 경계가 부족했다. 옥상 장면은 동결된 입술·시선·피부·도자기·가죽 관찰 조건을 통과했다. 따라서 대체 표현 접근과 후보팩 연결은 확인되지만 모든 단어가 항상 이미지에 구현된다고 결론 내릴 수 없다.

후속 픽셀 검증은 A의 지정 옆선을 팔과 분리하고 옷 주름과 몸 경계를 따로 확인하는 장면, B의 팔·손목을 충분한 native 크기로 보여 주는 장면을 새 core로 독립 작성해 실시한다. 지금 생성한 실패 이미지는 원래 동결 조건과 함께 남겨 비교 기준으로 쓴다. `slender_linear_build`의 기존 optional 계약은 긍정적인 좁은 폭 구성요소와 별도로 비시각적 owner-separation 문구를 요구해 B에서 선택을 거절한 제한이 있다. 이번 실행에서는 그 계약을 바꾸거나 실패를 숨기지 않았다. 필요하면 해당 owner의 분리 조건을 긍정적 형태 표현으로 재검토하되 기존 효과·잠금을 보존하고 별도 회귀·이미지 검증을 먼저 수행한다.

Native 도구가 실제 모델 이름을 반환하지 않아 이름은 unknown으로 기록했다. `partial`과 가림은 FAIL이며, 원본 픽셀 통과와 사용자 미적 수락은 별개다. 사용자 수락은 아직 받지 않았다. 세 장의 구성·관찰 차이는 [원본 검증 원장](../neutral-expression-native-qualification-20261003/ROOT-INDEPENDENT-PIXEL-REVIEW.json)에 남긴다.

## 변경과 작업 상태

[원본 상태](BASELINE-STATE.json), [변경 영수증](DATA-CHANGE-RECEIPT.json), [구성요소 대체 표현](COMPONENT-ALTERNATIVES.json), [최종 운영 해시](OPERATIONAL-INPUTS.json)를 저장했다. 작업 중 다른 작업에 의해 HEAD가 `acbf5e89`에서 `10937f95`로 이동했다. 우리가 commit/merge/push를 수행하지 않았고 관련 없는 기존 연구 수정도 보존했다. 최종 코드 검사와 native arm은 현재 실제 파일 해시를 기준으로 검증했다.

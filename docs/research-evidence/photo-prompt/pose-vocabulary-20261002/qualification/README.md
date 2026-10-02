# 포즈 반영 후 독립 이미지 테스트

2026-10-02. 독립 에이전트 3개가 서로 다른 난수 seed로 복잡한 컨셉·baseline·core·신체 배열·혼동 오답·픽셀 기준을 **후보 접근 전에** 고정했다. 반영 후 각자 V6 팩 1개와 native imagegen 1회씩 실행했다. 부모도 같은 원본 3장을 직접 열어 관찰했다. 첨부 초상은 얼굴·머리의 보이는 외관 참고로만 사용했고, 새 장면 주체는 성인으로 명시했다.

반영 대상 키워드의 엄격한 픽셀 판정은 **3/7 PASS, 3 FAIL, 1 UNOBSERVABLE**이다. 일반 지식 대조 항목인 OK 사인도 PASS다. 복합 장면 전체는 **0/3 PASS**이며, A·B는 FAIL, C는 필요한 완료 상태가 불가시여서 성공 집계에서 제외했다. 부분 충족을 장면 성공으로 바꾸지 않았다.

| 독립 컨셉 | 키워드 | 새 데이터 노출·채택 | 원본 판정 |
|---|---|---|---|
| A 겨울 해안 관측소 지도실 | 좌면에 교차 정강이로 앉기 | pv_cross_shins_seated_surface 번들 채택 | UNOBSERVABLE: 뒤쪽 발목 연결 가림 |
| A | 왼손바닥 좌면 지지 | pv_seated_palm_brace 미노출 | FAIL: 실제 오른손이 지지 |
| B 식물원 새벽 발레 연습 | modest spacing의 평발 second position | pv_ballet_second_flat 채택 | FAIL: 동결한 간격보다 넓음 |
| B | shallow demi-plié | pv_ballet_demi_plie_flat 채택 | FAIL: 굽힘이 깊음 |
| B | 둥근 overhead fifth arms | pv_ballet_fifth_arms_overhead 미노출 | PASS: 독립 baseline 구현 |
| C 해안 철도 신호 박물관 | half-kneeling | pv_half_kneel 번들 채택 | PASS |
| C | 왼손 V 사인 | pv_v_sign 미노출 | PASS: 독립 baseline 구현 |
| C | 오른손 OK 사인 | 원래 조사 밖 일반 지식 대조 | PASS: 반영 데이터 성과에서 제외 |

새 데이터에서 추적한 7개 목표 중 4개는 실제 팩에 노출·채택됐다. hand_pose·contact_point 쪽 3개 목표는 미노출이었다. 새 시각 의미 프로필은 직접 opt-in 후보로 노출·채택된 것이 없고, 일부 ID가 선택 번들의 advisory 연결 정보로만 보였다. 따라서 팔·V 픽셀이 맞았다는 사실을 새 후보나 프로필 채택 성공으로 집계하지 않는다.

B의 일반 `pv_ballet_second_flat` 정의는 lateral separation·outward knees/toes·grounded heel/forefoot·uncrossed ownership 4성분을 보여 준다. 그러나 독립 케이스는 그보다 좁은 modest spacing을 먼저 요구했으므로 케이스의 second position은 FAIL이다. 출처 후보의 넓은 의미와 독립 테스트의 추가 조건을 구분했다. 신규 후보의 채택과 독립 키워드 all-of가 함께 PASS한 항목은 C의 half-kneeling 하나다.

## 원본과 각 에이전트의 근거

| Arm | 컨셉 seed | 실제 pack seed | 원본 크기 | 보고서 |
|---|---:|---:|---|---|
| A | 1502416880209716418 | 2012744107882077902 | 1237×1272 | [A 상세](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-a-seated/qualification_report.md) |
| B | 608642126586136787 | 1312320717690390855 | 1024×1536 | [B 상세](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/report.md) |
| C | 2157385214743513717 | 8145926231557907273 | 1237×1272 | [C 상세](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-c-kneeling/report.md) |

이 seed는 컨셉/controls와 후보팩의 기록이다. Native imagegen에 seed 옵션을 제공하거나 동일 이미지의 재현성을 증명한 것은 아니다.

A: 오른손이 지지하고 왼손이 지도를 잡아 동결한 소유자 역할이 뒤바뀌었다. 뒤쪽 발목 연결과 일부 접촉 경계는 가려졌다. 바닥이 잘려 좌면의 낮은 높이도 확인할 수 없다.

![A 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-a-seated/native_image.png)

B: 팔은 둥근 oval·부드러운 팔꿈치·손끝 간격·낮은 어깨를 모두 보여 준다. 하체는 넓은 간격과 깊은 굽힘 때문에 동결한 좁은 변형/얕은 깊이를 충족하지 못한다. 닫힌 검은 케이스에서 violin 분류도 독립적으로 식별하지 못했다.

![B 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-b-ballet/native_result.png)

C: 한쪽 무릎과 반대 발의 지지, 오른손 thumb/index의 닫힌 OK 구멍과 나머지 세 손가락, 왼손의 펼친 두 손가락과 접힌 나머지를 확인했다. 전시판의 의도한 복구 완료 상태는 일반적인 upright signal display와 별도로 식별되지 않는다.

![C 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/arm-c-kneeling/native_attempt_1.png)

## 검증 층과 한계

작성·runtime 감사는 3/3 PASS다. 최소 요청 anchor를 자유 서술로 유지한 quality 경고는 보존했다. 에이전트의 5개 신체 게이트는 합계 11/15 PASS, 3 FAIL, 1 UNOBSERVABLE이다. A의 render-review는 실제 기술 게이트 실패를 기록했고, B·C의 기술 게이트는 통과했다. 대표 결과 승격과 사용자 판단은 별도이며 사용자 승인 값을 만들어 넣지 않았다.

[코디네이터 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/coordinator-review.json)에 에이전트와 부모의 읽기 차이도 남겼다. 부모는 A의 뒤쪽 발목 연결을 처음에 추정했다가 불가시 규칙으로 정정했고 최초 파일을 보존했다. C의 일반적인 upright apparatus를 부모는 장면 성립으로 읽었지만, 에이전트는 동결한 복구 전시판의 결과를 식별하지 못했다. 최종 all-of는 더 엄격한 관찰 경계를 적용해 C 성공을 제외했다.

[무결성 검사](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/artifact-verification.json)는 **403개 PASS**다. 소스 110개, 동결 입력, 실제 tool arguments와 감사된 runtime 원문의 일치, 원장, native 반환 파일과 보존 사본의 동일 바이트, 각 manifest 참조를 확인했다. 이 스크립트는 픽셀을 자동 판정하지 않는다. 각 원본 SHA는 manifest와 개별 보고서에 있다.

실제 호출 3회가 모두 이미지를 반환했고 blocked·추가 렌더·CLI 전환은 0회다. C의 호출 전 로깅 준비 실패 1건은 이미지 호출로 세지 않았다. A의 잘못 기록한 컨셉 seed와 B의 null seed는 실제 pack seed로 원장만 정정하고 원래 기록을 남겼다. 이미지·prompt·core·pack은 바꾸지 않았다.

이번 세 사례는 독립적으로 작성한 통합 테스트다. 에이전트의 사전 geometry를 본 뒤 출처 범위를 좁힌 변형 5개를 보강했으므로 무작위 모집단 holdout이나 반영 전후 인과 비교는 아니다. 새 158개 후보·34개 프로필 전체의 이미지 품질 자격, 실제 힘, 정체성·생체적 동일성 또는 사용자 수용을 주장하지 않는다. [노출·픽셀 보완 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/follow-up-plan.md)에 후속 경계와 종료 기준을 정리했다.

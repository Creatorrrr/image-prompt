# 인물 사진 구도 데이터 반영 및 독립 이미지 테스트

작성일: 2026-09-27. 대상: 현재 `image-prompt` 작업 공간의 photo-prompt-image-generator.

조사한 키워드를 실행 데이터와 후보팩 경로에 반영했고, 독립 서브에이전트 A·B·C가 서로 다른 랜덤 복합 장면으로 프롬프트 작성, 첨부 이미지 참조 생성, 픽셀 검증을 완료했다. **키워드 판정은 8/9 통과, 생성 전에 고정한 전체 장면 판정은 0/3 통과**다. 키워드가 보이는 것과 손의 접촉·지지·좌우·동작까지 유지되는 것은 별도 결과다.

## 1. 데이터 반영 결과

원래 ChatGPT 대화 「인물 사진 구도 조사」의 키워드를 출발점으로 작성한 [상세 리서치](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/report.md), [50개 개념 목록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/concept-catalog.json), [출처 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/sources.json)을 실제 런타임에 연결했다. 25개 출처 기록은 원문 확인 20개, PubMed 초록 1개, 원문 접근이 제한된 발췌 근거 4개로 구분되어 있다.

| 반영 대상 | 결과 | 확인 범위 |
|---|---:|---|
| 단일 이미지 구도·시각 제어 개념 PC/PX | 42개 | PC01–30, PX01–12 |
| 원자 후보 | 156개 | 18개 기존 슬롯, 한국어·영어 검색 표면 |
| 선택형 관계 번들 | 42개 | 구성요소와 영향 차원을 함께 검증 |
| 좁은 시각 의미 프로필 | 16개 | 프로필마다 필수 구성요소 4개 |
| 새 시각 판정 항목 | 64개 | 구성요소별 관찰 근거를 요구 |
| 새 데이터 전용 회귀 테스트 | 10개 통과 | 정확한 의미, 부정, 부분 일치, 소유·관계, 인덱스 |

스타일 PS01–05와 다중 이미지 형식 PM01–03, 총 8개 개념은 조사 자료에 유지했다. 이번 단일 이미지 관계 확장에는 실행 후보로 넣지 않았다. 조사된 50개 전체가 신규 픽셀 검증을 받았다는 의미는 아니다.

주요 변경 파일:

- [후보 확장 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_portrait_composition_extension.json)
- [시각 의미 프로필](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_portrait_composition.json)
- [후보 생성·라우팅 코드](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py)
- [등록 정책](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json)
- [출처와 해시를 연결한 유지보수 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/extension-maintenance/portrait-composition-research-20260927.json)
- [신규 회귀 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_portrait_composition_semantics.py)

넓은 키워드나 일부 구성요소만 발견되면 선택형 후보로 남긴다. 한국어·영어 모두 전체 4개 구성요소 정의가 정확히 일치할 때만 해당 필수 프로필을 활성화한다. 번들을 선택해도 연관 프로필을 자동으로 필수화하지 않는다. 단순 유사도는 후보 노출의 근거이고, 필수 의미를 선언하는 근거로 사용하지 않는다.

구도 프로필이 나이·정체성·직업·성격을 요구하거나 추론하지 않게 했다. 반사 얼굴의 초점은 보이지 않는 광학 거리 대신 **실제 반사된 눈과 표정이 해상되는지**로 판정한다. 테스트에서 발견한 한국어 표현 앞의 영어 부정(`not`, `without` 등) 처리 누락은 공통 부정 판별 함수에서 보완했고, 이번 주제에 한정한 예외 분기는 추가하지 않았다.

후보 검색에 사용하는 텍스트에서 조사 URL과 출처 ID를 제외했다. 같은 슬롯의 기존 영어 원자와 정확히 중복되는 신규 원자는 없다. 64개 프로필 구성요소에는 구별 가능한 한국어 관계 표현을 추가했다.

## 2. 인덱스와 기존 데이터 보존

Gemini `gemini-embedding-2`, 768차원 인덱스를 재구축하고 현재 소스 해시와 일치하는지 확인했다. 이전 인덱스와 비교해 기존 의미 항목 8,972개와 시각 프로필 944개의 저장 데이터가 그대로 유지됨을 확인했다. 현재 의미 항목은 9,128개, 시각 프로필은 960개다.

| 바인딩 | 현재 값 |
|---|---|
| dictionary hash | `2f25dd52e76a52be07fd44f6b573259bbea7f39bae4ee6f9dda2071ba935baf4` |
| visual registry hash | `2abe817e4e46df5c9cf5ff808fa2f31919e33f5f87cb3a610e0e26f87d1bb5fc` |
| 보존한 이전 dictionary hash | `e7e691b9355a6e4256f596676b9b67f99239641c468b42bcea9ba7a56f8f4698` |
| 보존한 이전 visual registry hash | `63af603a1b418d9a4c372538e8bb06f1e841e7e1063f5b11925a9e0ff4c18192` |

[소스·인덱스 검증 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/integration/verification.json)과 [검증 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/verify_integration.py)에 비교 근거가 있다. 이 검증은 저장·검색 데이터의 무결성을 확인하며, 이미지의 성공 판정을 대신하지 않는다.

## 3. 독립 테스트 방법

세 에이전트는 대화 이력을 공유하지 않고 시작했다. 실제 요청문, 이전 대화에서 조사한 키워드라는 데이터, 스킬 규칙, 중립적인 사전 선택 카테고리, 첨부 사진을 사용해 독립적인 랜덤 시드와 장면을 정했다. 서로의 컨셉·프롬프트·이미지를 입력으로 사용하지 않았다.

각 에이전트는 후보 데이터를 읽기 전에 장면, 기준 프롬프트, 핵심 의미, 몸과 물체의 관계, 테스트케이스를 고정했다. 그 뒤 새 인덱스를 사용하는 일반 semantic v6 후보팩을 한 번 생성하고, 실제 노출된 후보만 선택·재해석하거나 거절했다. 노출되지 않은 후보를 강제로 넣지 않았다.

첨부 사진은 눈으로 확인한 얼굴·머리의 외형 참고로 사용했다. 묘사한 활동과 장소, 성인 캐릭터 설정은 테스트용 창작이며 사진 속 실제 인물에 대한 추론이 아니다. 세 요청 모두 원본 참조 이미지 경로를 native 이미지 생성에 전달했다.

- 참조 파일: [첨부 원본](</Users/chasoik/Downloads/0CB25F47-BB90-4DBD-8993-733BA8282851(20260927-041323).jpeg>)
- 참조 SHA-256: `06d6c6feeed0d2397ec9562d46113cd221ac54a0e190295f0aa7f7868c22ece7`
- native 이미지 생성: 각 1회, 합계 3회. 각 원본 1,237 × 1,272 픽셀.
- 프롬프트 구성·실제 요청 사전 감사: 세 케이스 모두 통과. 일부 프롬프트 길이·포괄 의도 경고는 개별 보고서에 유지했다.
- 픽셀 확인: 각 작성 에이전트의 원본·축소 검토와 주 에이전트의 원본 재검토. 직접적인 사용자 취향·수용 판정은 아직 없다.

평가 중 테스트 기준을 낮추지 않았고, 재생성으로 첫 실패를 덮지 않았다. 저장된 manifest의 `status: success`는 도구 실행과 원본 저장 성공을 뜻하며, 전체 의미나 사용자 수용 성공을 뜻하지 않는다.

## 4. 케이스별 실제 결과

| 케이스 | 랜덤 복합 장면 | 대상 키워드 | 키워드 결과 | 고정한 전체 장면 |
|---|---|---|---:|---|
| A | 눈 오는 식물원 온실에서 동행에게 청사진 엽서를 건네는 티타임 | 테이블 너머 인물, 다른 사람의 어깨 너머 시점, 카메라 방향 제시 동작 | 3/3 통과 | 실패: 카드 아래쪽 대신 위쪽 가장자리를 잡음 |
| B | 비 오는 옛 철도 대합실의 등불 작업 공간에서 리본과 코트 단추를 비교 | 전경 보케, 유리 반사·투과, 주변부 굴절 | 3/3 통과 | 실패: 양손으로 수평 당기는 리본과 두 번째 손 연결이 보이지 않음 |
| C | 가을 해질녘 복원된 여객선 터미널에서 지도를 접다 멈춘 장면 | 앉은 삼각형, 대칭 건축과 비대칭 자세, 정지 인물과 이동 주변 | 2/3 통과 | 실패: 양팔 무릎 지지·지도 접기·고정한 발 좌우 관계가 유지되지 않음 |

### A — 테이블·어깨·카드의 깊이 관계

시드 `4400049719420549872`, pack `45b4dc93e9138bfd`, run `4f49bd93b0d8495f`.

테이블이 관찰자와 인물 사이에 놓이고 얼굴이 테이블 위에서 우세하다. 가까운 다른 사람의 흐린 어깨와 뒤쪽 주인공 얼굴의 선명도가 시점을 설명한다. 연결된 손과 팔이 엽서를 카메라 쪽으로 내밀면서 얼굴을 가리지 않는다. 세 키워드는 통과했다.

선택한 새 프로필은 PC03·PC16·PC17이며 새 시각 항목 12개가 모두 통과했다. 몸·접촉 항목 5개도 통과했다. 그러나 고정한 정확한 의미 필드 8개 중 `a_offer_camera.grasp`가 실패했다. 기준은 엽서 **아래쪽** 가장자리를 엄지와 검지로 잡는 것이고, 원본에서는 **위쪽/왼쪽 위** 가장자리를 잡는다. 일반 접촉 검사는 손과 카드의 연결만 확인하므로 이 정밀 조건을 대체할 수 없다. 따라서 파생 판정 17/17 통과와 전체 장면 실패를 동시에 기록한다.

[A 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/final_prompt.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/report.md) · [정확한 의미 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/semantic_assertion_pixel_review.json) · [실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/run_manifest.json)

![A — 온실의 엽서 전달 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_a/generated_original.png)

### B — 전경 흐림·유리·프리즘의 분리

시드 `1292956637129113158`, pack `51366a22b095f223`, run `e4f6279c33979f59`.

가까운 사프란색 천이 흐리고 뒤쪽 얼굴은 선명하다. 창틀과 빗방울 면이 유리 위치를 정하며, 실내 인물·행동과 상부 캐노피/전선 반사가 서로 다른 영역에서 함께 보인다. 오른쪽 끝에는 붉은 램프 윤곽의 변위·중복과 좁은 색 분산이 나타나지만 중앙 얼굴은 유지된다. 세 광학 키워드는 통과했다.

선택한 새 프로필 PC19·PC21·PC24의 시각 항목 12개가 통과했다. PC19 구성요소 3과 PC21 구성요소 2도 원자 후보로 선택했다. 그러나 코트 뒤에 가려진 두 번째 손의 연결을 확인할 수 없고 리본이 아래로 늘어진다. 양손으로 수평에 가깝게 당기는 고정 동작이 구현되지 않아 몸 소유, 관절·도달, 접촉·공간, 가시성·투영 항목 4개가 실패했다.

[B 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/prompt_en.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/report.md) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/pixel_review.json) · [실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/run_manifest.json)

![B — 철도 대합실 작업 공간 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_b/render_attempt_01.png)

### C — 대칭·비대칭·선택적 움직임

시드 `15331982403002488971`, pack `51054a89cc275ff7`, run `eb8aad56a5f9a763`.

중앙 출입문 양옆의 아치·램프가 대칭을 만들고 인물의 손·머리·어깨 자세가 비대칭이다. 두 여행자와 짐에는 옆 방향 흔적이 보이지만 얼굴·벤치·지도·건축은 비교적 선명하다. 두 키워드는 통과했다.

머리와 벌어진 팔꿈치가 삼각 윤곽을 일부 만들지만, 기준의 양팔과 두 무릎 지지가 동시에 읽히지 않는다. 한 손은 뺨을 받치고 다른 손은 펼친 지도를 잡는다. 지도 접기 동작과 배우 기준 왼발 바닥/오른발 단차도 유지되지 않았다. 화면 오른쪽의 배우 왼발이 단차에 올라간 반대 관계다. 지지·균형과 접촉·공간 항목이 실패했고, 삼각형 키워드도 엄격하게 실패로 남겼다.

PC09 프로필은 정상 후보팩에 노출됐지만, **얼굴·팔꿈치·무릎** 삼각형을 규정한다. 독립적으로 고정한 케이스는 **머리·두 팔꿈치** 삼각형이므로 이를 채택하면 기준을 바꾸게 된다. 에이전트는 이 프로필을 거절했다. PC27 구성요소 4의 얼굴 초점 우선순위와 PC29 전체 프로필은 선택했고, PC29 새 시각 항목 4개가 통과했다. PC09가 이 이미지로 검증되었다고 보고하지 않는다.

[C 프롬프트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/final_prompt_en.txt) · [테스트케이스](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/test_case.json) · [개별 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/report.md) · [픽셀 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/pixel_test_result.json) · [실행 manifest](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/run_manifest.json)

![C — 여객선 터미널 지도 장면 원본](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification/arm_c/generated_images/attempt-01.png)

## 5. 검증 결과와 회귀 실패의 범위

신규 테스트 10개는 모두 통과했다. 한국어·영어 전체 정의, 부분·부정 정의, 혼동 경계, 구성요소 근거 중복 거절, 연령·정체성 누출 방지, 42개 번들의 구성·차원 변형 거절, 유지보수 해시, 반사 초점의 관찰 가능성, 현재 인덱스의 바인딩을 검증했다. [최종 테스트 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/integration/portrait-final-tests.log)에 실제 실행 결과가 있다. 사전 검증·의미 인덱스 검증과 기존 장면 표현 경로 112/112 검증도 통과했다.

전체 저장소 회귀 검사에서는 실패가 발견되어 광범위 실행을 조기에 중단했다. **전체 회귀 검사를 완료하거나 통과했다고 주장하지 않는다.** 1,220개는 검색된 테스트케이스 수이며 실행·통과 수가 아니다. 발견한 실패는 추가 전 데이터를 정확한 해시로 메모리에 복원해 같은 현행 코드에서 비교했다.

| 발견한 실패 | 확장 전/후 비교 | 판단 |
|---|---|---|
| 기존 recipe의 누락 ID 140개 | raw base JSON을 쓰는 원래 테스트에서 목록 동일 | 이번 PC 데이터 추가 전에도 존재 |
| 의미 항목 수 기대값 6,910 | 이전 8,972, 현재 9,128 | 오래된 고정 기대값이 이전부터 불일치 |
| 기존 photo baseline 바이트 차이 | 현재·이전 출력 SHA `40e15001…`와 pack `87cdf166ba20cfe6` 동일, fixture와 다름 | 이번 추가 전에도 동일한 드리프트 |
| prepack 의미 바인딩 검사 | 이전·현재 pack `960c35cd7ff8cec4`, optional `pf_keep_ward` 동일 | fixture에서 명시적 선택 목록을 생략한 동일 실패 |
| `positive_inner_thigh_en` 라우팅 | hard와 optional 결과가 이전·현재 동일 | fixture의 빈 optional 기대값과 기존 후보가 불일치 |

두 진단 에이전트는 각각 [A의 재현 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/integration/arm_a_pc_preexisting_failure_diagnostic.json), [B의 재현 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/integration/broad-failure-attribution-b.json)에 비교 조건과 결과를 남겼다. 두 진단은 운영 소스·fixture·인덱스를 바꾸지 않았고 추가 이미지 호출도 하지 않았다. 메타데이터 검사 regex가 보석의 실제 `facet geometry`를 잡는 1건도 이전·현재가 같다는 추가 관찰을 남겼다. 이 비교는 발견한 실패의 귀속을 설명하며, 실행하지 않은 모든 검사의 통과를 보장하지 않는다.

[광범위 검사 경계 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/integration/broad-regression-boundary.json)은 `failed_early`, `full_suite_completed: false`로 보존했다. 기존 Y2K 작업을 포함한 관련 없는 작업은 유지했다.

## 6. 해석과 아직 검증하지 않은 범위

세 이미지에서 실제로 선택한 신규 프로필은 **7/16개**이고, 해당 **28개 시각 판정 항목은 모두 통과**했다. 선택한 추가 원자 후보는 3개다. 테이블·어깨·제시 물체의 깊이, 전경 흐림, 유리 반사·투과, 주변 굴절, 정지 얼굴과 이동 주변의 분리에는 이번 데이터가 프롬프트와 픽셀까지 연결된 근거가 있다.

전체 파생 시각·몸 판정은 43개 중 37개 통과, 6개 실패다. 여기에 A의 카드 가장자리처럼 파생 일반 접촉 검사에 포함되지 않은 정확한 의미 실패가 추가된다. 따라서 37/43이나 28/28을 전체 장면 성공으로 환산할 수 없다. 상세 접촉·지지·좌우·양손 동작은 이번 세 복합 장면에서 실패 증거를 얻었다.

세 테스트의 8/9는 이번에 고정한 9개 키워드 판정의 결과다. 모델의 일반적인 성공 확률이나 전체 구도 목록의 품질 추정치가 아니다. 나머지 9개 프로필·36개 항목과 42개 번들의 실제 공동 채택은 아직 이미지 검증을 받지 않았다. 조사 단계의 252개 설계 사례도 전체 실행된 회귀 또는 이미지 결과로 계산하지 않는다. 계절·복원 연혁 같은 맥락은 시각 단서와 창작 설정을 구분해 기록했다.

후속 개선 대상으로는 정확한 잡는 가장자리, 가려진 두 번째 손의 소유·연결, 배우 기준 좌우 지지, 두 팔 지지와 삼각형의 변형 구분이 확인됐다. 이번 결과의 실패 판정을 유지한 상태에서 각각 별도 가설과 테스트케이스로 다루어야 한다. 첨부 인물의 정체성이나 사용자의 미적 만족을 검증했다는 주장은 없다.

## 7. 재확인 가능한 증거

[최종 요약 JSON](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/qualification-summary.json)에 각 시드, pack/run ID, 원본 이미지 해시, core/intent/실행 계약 해시, 선택한 프로필, 판정 결과를 모았다. [최종 증거 검증 스크립트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/portrait-composition-20260927/verify_qualification.py)는 생성 없이 다음을 다시 확인한다.

- 세 고정 core와 요청 봉투의 파일 해시, 기준 프롬프트 문자열.
- 각 한 줄 실행 ledger와 manifest의 run·pack·참조·호출 수 일치.
- 선택한 신규 후보가 각 일반 composer catalog에 실제로 노출되었는지.
- 이미지 원본 SHA-256, PNG 크기, 픽셀 판정과 이미지 바인딩.
- 각 생성 시점의 소스 snapshot 파일 43개·78개·79개가 현재 그대로인지.
- 작성 에이전트와 주 에이전트의 키워드·전체 장면 결과 일치.

최종 재확인 결과는 통과했다. 이 무결성 통과는 위에 기록한 픽셀 실패를 변경하지 않는다.

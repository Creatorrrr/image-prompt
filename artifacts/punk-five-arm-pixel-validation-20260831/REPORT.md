# 펑크 시각 의미·후보팩 5개 독립 팔 픽셀 검증

## 결론

첨부 인물 사진을 외형 참고로만 사용해 다섯 개의 무작위 펑크 장르를 서로 독립적으로 설계하고, 정확 프리셋 후보팩으로 프롬프트를 구성해 이미지를 생성한 뒤 저장된 원본 픽셀에서 판정했다.

- 동결된 장르·혼동 방지·사진·참조 게이트: **48/50**
- 후보팩 작동 게이트: **14/20**
- 전체 하드 게이트: **62/70**
- 한 이미지에서 14개 게이트를 모두 통과한 팔: **0/5**
- 판정: **revise** — 넓은 장르 의미는 대부분 보이지만 후보 원자의 정확한 동일 객체 속성, 물리 연결, 인과적 공간 관계는 아직 승격할 수준이 아니다.
- 사용자 미감 판정: **pending**

프롬프트 구성 감사 5/5와 실제 렌더 요청 감사 5/5는 모두 통과했다. 따라서 아래 실패는 키워드나 참조가 요청에 들어가지 않은 문제가 아니라, 요청된 복합 관계가 최종 픽셀에서 충분히 명시적으로 보이지 않은 문제다.

## 실험 설계

난수 시드는 `01a055f1-4414-7822-a44a-30a917cef798`이며, 조사된 20개 펑크 장르의 고정 순서 풀에서 Python `random.Random(seed).sample(pool, 5)`로 Lunarpunk, Clockpunk, Atompunk, Raypunk, Stonepunk를 뽑았다. 각 서브에이전트는 다른 팔의 산출물을 보지 않고 다음을 독립 작성했다.

- 저자 코어와 복합 장면
- 장르 목표 게이트 5개
- 가장 가까운 장르 혼동 방지 게이트 2개
- 사진·성인·외형 참조·접촉 정합성 게이트 3개
- 정확 프리셋 후보 4개에 대응하는 작동 게이트 4개

모든 게이트는 생성 전에 동결했다. 한 이미지에서 모든 구성 요소가 보여야 하며, 부분적이거나 애매한 경우는 실패로 처리했다. 프롬프트 문장은 픽셀 증거로 사용하지 않았고, 서로 다른 시도의 증거를 합치지 않았다.

첨부 사진의 SHA-256은 `3d363f7e1bfde96cd153cd22550e11144de30cf0aec492a3c97007653ec92aea`이다. 용도는 긴 물결형 흑발, 얼굴 윤곽, 눈·눈썹·입술 등 넓고 관찰 가능한 성인 외형 단서뿐이다. 생체 동일인 판정이나 보호 특성 추론은 하지 않았다.

초기 의미 경로가 장르별 세계·소품 대신 일반 인물 후보만 노출한다는 실험 구성 오류를 발견했다. 이미 생성된 일반 이미지는 비교용 기준선으로 보존했지만 점수에는 사용하지 않았다. 이후 각 장르의 `punk_<keyword>_world` 정확 프리셋 v6를 다시 구성하고, 세계·메커니즘·진단·유지보수 후보 4개를 모두 선택한 타깃 이미지로만 후보팩을 판정했다. 소수 기준선과 타깃 이미지의 차이를 후보팩의 인과 효과로 주장하지 않는다.

## 결과 요약

| 장르 | 독립 복합 콘셉트 | 동결 게이트 | 후보 게이트 | 전체 | 엄격 판정 |
|---|---|---:|---:|---:|---|
| Lunarpunk | 달 조수 생태학자가 초승달 생물반응기에 발광 조류를 부어 살아 있는 습지 관측소를 기동 | 10/10 | 2/4 | 12/14 | FAIL |
| Clockpunk | 자정 시민 시간탑의 일식 리허설에서 대형 태엽 키로 천문시계와 기계 새 방출을 기동 | 9/10 | 3/4 | 12/14 | FAIL |
| Atompunk | 1962년 동위원소 과수원에서 원예사가 종자 금고를 조정하고 아날로그 로봇이 발광 과실을 건넴 | 10/10 | 3/4 | 13/14 | FAIL |
| Raypunk | 사막 광자 세마포어가 버블창 우편 로켓을 위해 색광 항로를 재연결 | 9/10 | 4/4 | 13/14 | FAIL |
| Stonepunk | 조수 관리인이 거석 관측소의 석영 구동 현무암 아스트롤라베를 기동해 파도와 외륜을 정렬 | 10/10 | 2/4 | 12/14 | FAIL |

## 1. Lunarpunk

![Lunarpunk generated result](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-01-lunarpunk/targeted_attempt-02.png)

초승달, 야간 습지, 발광 조류, 뿌리·균사 네트워크, 손으로 붓는 활성화 사건은 명확했다. 실패는 활성 배양 용기 자체에 두 개의 리필 이력 표시와 황동 수리 이음이 없고, 진단 타일이 엄지 크기보다 크며 하나의 국소 습윤 장애점을 가리키지 못한 것이다.

- [선택 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-01-lunarpunk/targeted_composed_prompt.json)
- [정확 후보팩](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-01-lunarpunk/candidate_pack.json)
- [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-01-lunarpunk/pixel_review_targeted_attempt_02.json)

## 2. Clockpunk

![Clockpunk generated result](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-02-clockpunk/targeted_attempt-02.png)

다중 천문 다이얼, 태엽·기어·밸런스, 삽입된 대형 키, 시간 보정 장비는 읽힌다. 그러나 기계 새는 열린 경첩식 우리에서 반쯤 나오는 상태가 아니라 완전히 밖에 있고, 감긴 배럴에서 식별 가능한 새 우리까지 이어지는 연속 링크도 독립적으로 읽히지 않는다.

- [선택 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-02-clockpunk/composed_prompt.json)
- [정확 후보팩](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-02-clockpunk/candidate_pack.json)
- [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-02-clockpunk/pixel_review_targeted_attempt_02.json)

## 3. Atompunk

![Atompunk generated result](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-03-atompunk/targeted_attempt-02.png)

1962년 원자로 온실, 아날로그 로봇, 코발트색 과실, 종자 금고, 보호 장구와 연속 엄빌리컬은 모두 강하게 반영됐다. 유일한 실패는 로켓 서비스 구조와 미터가 함께 보이지만, 미터가 갠트리에 물리적으로 장착된 계측계라는 관계가 모호하다는 점이다.

- [선택 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-03-atompunk/targeted_attempt-02_composed_prompt.json)
- [정확 후보팩](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-03-atompunk/candidate_pack.json)
- [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-03-atompunk/pixel_review_targeted_attempt_02.json)

## 4. Raypunk

![Raypunk generated result](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-04-raypunk/targeted_attempt-01.png)

크롬·파스텔 에나멜·원자 시대 스트림라인, 결정 키와 렌즈, 진공관·계기, 세 색 광선과 별도 진단 장비는 명확했다. 후보 4개는 모두 작동했지만, 우편 로켓의 붉고 푸른 배기 궤적이 하단의 녹색·주황·청색 항로와 교차하거나 그 항로를 따라 접근하지 않아 핵심 사건 게이트가 실패했다.

- [선택 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-04-raypunk/composed_prompt.json)
- [정확 후보팩](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-04-raypunk/candidate_pack.json)
- [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-04-raypunk/pixel_review_targeted_attempt_01.json)

## 5. Stonepunk

![Stonepunk generated result](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-05-stonepunk/targeted_attempt-02.png)

기능성 현무암 기어·홈, 석영 계측기, 수동 크랭크, 거석 관측소와 파도 결과는 강하게 반영됐다. 다만 뼈 레버 끝이 식별되지 않고 생가죽과 식물 섬유를 구분할 수 없어 세 가지 보조 재료가 증명되지 않는다. 예비 결속과 작은 추는 보이지만, 추가 교체 작업 중 실제 하중을 지지하는 관계도 모호하다.

- [선택 프롬프트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-05-stonepunk/composed_prompt_attempt_02.json)
- [정확 후보팩](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-05-stonepunk/candidate_pack.json)
- [픽셀 판정](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/arm-05-stonepunk/pixel_review_targeted_attempt_02.json)

## 후보팩 데이터 개선안

현재 게이트는 생성 후 약화하지 않는다. 다음 반복에서는 같은 게이트를 유지하면서 후보 원자 표현을 다음처럼 강화하는 편이 타당하다.

1. 후보마다 `visible_components`와 별도로 단 하나의 최우선 `primary_relation`을 둔다. 예: `meters mounted on gantry frame`, `rocket intersects ray corridor`, `counterweight line visibly bears the active load`.
2. `same_object_constraints`를 명시해 속성이 이웃 소품으로 이동하는 것을 막는다. Lunarpunk의 리필 표시와 수리 이음은 반드시 지금 붓고 있는 동일 용기에 있어야 한다.
3. 연결 후보에는 시작점·연속 경로·종점과 접촉 방식을 데이터로 분리한다. Clockpunk는 감긴 배럴 → 축·기어 링크 → 경첩식 새 우리를 한 경로로 고정한다.
4. 작은 진단·재료 차이는 `minimum_readable_scale`과 `foreground_zone`을 가진다. 화면 전체가 젖어 있으면 국소 습윤 진단은 성립하지 않는다는 반대 조건도 함께 둔다.
5. 장면 당 복수 후보를 모두 넣더라도 각 후보의 결합 요구 수를 줄이는 것이 아니라, 동일 객체·연결·인과 관계에 우선순위를 주고 부차 장식은 유연 치수로 내린다.
6. 정확 펑크 프리셋 경로가 세계·메커니즘·진단·유지보수 후보를 실제로 노출하는지 패키지 단계에서 강제한다. 일반 인물 후보만 나온 경우는 렌더 전에 실패시킨다.

이 개선안은 이번 실행에서 코드나 후보팩 원본에 적용하지 않았다. 이번 산출물은 진단·검증 패키지이며, 다음 반복에서 데이터를 수정한 후 같은 동결 게이트와 새로운 무관 홀드아웃 장르로 재검증해야 한다.

## 검증 및 증거 경계

- 펑크 의미 집중 테스트: 7/7 PASS
- 사진 프롬프트 사전 메타데이터: PASS
- 시각 프로필 인덱스: 82 프로필, 483 정확 용어, PASS
- 의미 인덱스: 6,910 항목, PASS
- 선택 프롬프트 감사: 5/5 PASS
- 선택 렌더 요청 감사: 5/5 PASS
- 저장 원본 픽셀 엄격 판정: 0/5 완전 PASS
- 전체 저장소 테스트 스위트: 실행하지 않았으므로 PASS를 주장하지 않음
- 사용자 미감·선호: 아직 판정받지 않았으므로 pending

통합 증거는 [실험 매니페스트](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/experiment_manifest.json), [코디네이터 픽셀 리뷰](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/review/coordinator_pixel_review.json), [검증 요약](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/review/validation_summary.json), [개선 반복 기록](/Users/chasoik/Projects/image-prompt/artifacts/punk-five-arm-pixel-validation-20260831/iteration_record.json)에 남겼다. 각 팔의 생성 계보, 요청, 해시와 실행 원장은 해당 팔의 `generation_provenance.json`, `run_manifest.json`, `runs/image_runs.ndjson`에 보존했다.

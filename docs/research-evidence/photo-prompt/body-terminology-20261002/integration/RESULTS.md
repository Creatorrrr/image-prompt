# 신체 용어 반영 및 독립 이미지 시험 결과

2026-10-02. 조사 결과를 실제 시각 의미 데이터와 V6 후보팩 검색에 반영했고, 독립 서브에이전트 3개가 첨부 사진을 사용해 서로 다른 복잡한 장면의 이미지를 각각 1회 생성했다. **세 사례 모두 완전 반영에는 실패했다.** 12개 관찰 조건 중 5개만 명확하게 충족했다. 프롬프트·runtime 감사 통과와 실제 픽셀 충족을 분리해 기록했다.

## 실제 반영 범위

| 데이터 | 이전 | 현재 | 반영 |
|---|---:|---:|---|
| 시각 프로필 | 1,419 | 1,496 | 신규 77, 기존 검색 보강 10, 원 계약 그대로 재사용 5 |
| ordinary 후보 | 9,590 | 9,664 | 신규 74, 기존 보강 18 |
| 슬롯 | 112 | 112 | 기존 슬롯을 사용 |
| semantic index 문서 | 9,626 | 9,700 | ordinary 후보와 기존 bundle을 포함 |

원 조사 91개 축과 소름의 관찰 요소 1개를 적용했다. 체형·비율·국소 윤곽·표면 질감·체모·손발·의복과 신체의 경계·접촉·자세에 따른 변화 등을 동의어 목록 대신 **관찰할 구성, 같은 대상의 소유권, 관계, 혼동 경계와 원본 픽셀 게이트**로 기록했다. 11개 측정·분류·커뮤니티·이력 지식 레코드는 연구 자료로 유지한다.

새 자산은 `photo_prompt_visual_obligations_body_morphology.json`과 `photo_prompt_body_morphology_extension.json`이다. 등록 목록·필수 extension 정책·기존 base 항목을 갱신하고 두 인덱스를 표준 builder로 재생성했다. Gemini `gemini-embedding-2`, 768차원, batch size 1을 사용했고 기존 호환 벡터를 재사용했다. 기록된 인덱스 해시는 [최종 코퍼스 영수증](LIVE-INTEGRATION-RECEIPT.json)에 있다.

기존 PFE authored source와 bundle, 허벅지 간격 프로필, 기존 contextual property-lock 소유권은 원 계약으로 복구했다. 기존 후보 13개의 모든 원 필드를 보존하면서 구조화 메타데이터 6필드를 추가했고, 기존 후보 5개의 의역은 허용된 문맥 확장으로 추가했다. 국소 hip indentation과 전체 waist-to-hip transition을 구분하는 한정 문맥도 검증했다. 검색 결과는 advisory이며 실제 사용자 의미나 hard duty가 되지 않는다.

## 독립 시험 방법

세 에이전트는 후보 데이터와 다른 사례를 보기 전에 각자 준비한 장면 집합에서 난수로 장면을 선택하고 baseline, V3 core, controls, feature selection, embodiment를 동결했다. 난수는 장면 선택 기록이며 이미지 생성 seed를 통제한 실험은 아니다. 실제 사용자 원문은 coordinator가 만든 envelope로 제공했다. 에이전트가 선택한 키워드를 사용자의 직접 지시였던 것처럼 표시하지 않았다. B의 anchor 형식 정정은 원 파일과 별도 정정 기록에 보존했다.

첨부 사진은 보이는 얼굴·머리 외형의 참고로 사용했다. 생성 인물의 25세 설정과 시험용 신체 조건은 창작 선택이며 참고 인물의 신체나 실제 나이를 추론한 결과가 아니다. 각 에이전트는 실제 사진을 `referenced_image_paths`로 전달했고 built-in `image_gen.imagegen`을 1회 호출했다. 관찰 가능한 모델명은 도구에서 보고되지 않았다.

첫 팩에서는 목표 후보 노출이 부족했다. 첫 팩을 보존한 채 동결된 visual priorities에 대응하는 source-opted-in 후보가 64개 제한 안에서 먼저 검색되도록 공통 검색을 보완했다. 모든 effect 차원과 property lock, 대상·문맥·제외 조건이 맞아야 한다. 검색 의역 12가족과 소름 축을 보강했지만 시험 문장 전체나 특정 장면을 prototype에 복사하지 않았다. 이 비교는 **데이터와 공통 검색을 함께 바꾼 동일 core 비교**이며 데이터만의 효과 또는 생성 품질의 인과적 향상을 증명하지 않는다.

## 원본 픽셀 결과

| 사례 | 서로 다른 복잡한 컨셉 | 독립 조건 | 통과 | strict gate | 전체 |
|---|---|---|---:|---:|---|
| A | 폭풍 직후 해안 온실에서 젖은 은색 차광막을 고정 | 긴 다리, 넓은 어깨, 완만한 어깨 경사, 적당한 근육 부피와 선명한 윤곽 | 2/4 | 6/9 | FAIL |
| B | 새벽 옥상에서 식물 사이아노타입 인화지를 수세 | 소름처럼 솟은 피부, 상완 솜털, 짙은 전완 체모, 손등 혈관 | 3/4 | 5/5 | FAIL |
| C | 해질녘 강변 인형극장에서 반투명 새 인형의 줄을 수리 | 긴 손가락/짧은 손바닥, 도드라진 손마디, 허리밴드 압흔, 지정 방향의 피부 주름 두 개 | 0/4 | 3/5 | FAIL |

**A:** 긴 다리의 상대 비율과 완만한 어깨 경사는 보인다. 앞쪽으로 모은 어깨의 폭은 확정하기 어렵다. 근육의 적당한 부피는 보이지만 상·하지의 선명한 면과 윤곽은 부족하다. 선택된 `toned_muscular_build`의 필수 3개 게이트가 실패했다. 신규 muscle-volume 후보와 보강한 기존 비율/definition 후보는 사용했지만 신규 shoulder-width/slope 프로필은 노출되지 않았다.

![A 온실 차광막 작업](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-a/generated_image.png)

[A 프롬프트·후보·판정 보고서](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-a/report.md) · [생성 기록](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-a/image_runs.ndjson)

**B:** 상완의 반복되는 미세한 돌기, 개별적으로 읽히는 짙은 전완 체모, 손등의 연속된 혈관 같은 경로는 보인다. 상완의 옅은 솜털은 개별 가닥과 피부 부착을 확정하기 어렵다. 신규 piloerection/hair-fiber 후보 2개가 노출·채택되었지만 두 후보의 전체 구성 충족은 PARTIAL이다. 혈관 후보는 미노출이었고 해당 조건은 원 baseline에서 유지한 시험 조건이다. Embodiment 5개가 통과해도 키워드 전체 충족은 실패한다. 외형 관찰은 피부 상태나 체모 유형에 대한 임상 진단이 아니다.

![B 옥상 사이아노타입 수세](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-b/generated_image.png)

[B 프롬프트·후보·판정 보고서](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-b/result_report.md) · [원본 픽셀 조건 평가](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-b/body_keyword_pixel_review.json)

**C:** 굽힌 손가락과 원근 때문에 손가락/손바닥 길이 비율을 판단할 수 없다. 손마디 돌출은 약하고 의복 압흔은 피부 주름과 분리하기 어렵다. 요청한 인물 기준 좌측의 짧은 주름 두 개가 나타나지 않았으며 손과 측굴 방향도 동결한 지시와 다르다. 신규 finger-proportion 후보 1개만 노출·채택되었고 나머지 3개 후보는 미노출이었다. 접촉·가시성 게이트도 실패했다.

![C 인형극장 수리](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-c/generated-image.png)

[C 프롬프트·후보·판정 보고서](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-c/report.md) · [원본 픽셀 조건 평가](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-c/pixel_test_results.json)

각 에이전트의 원본·native crop 평가에 더해 coordinator도 저장된 원본을 직접 확인했다. [별도 독립 판정](ROOT-INDEPENDENT-PIXEL-REVIEW.json)은 이미지·ledger·manifest SHA에 결합했다. C의 관찰 가능성 표시는 에이전트의 FAIL 세부 라벨과 다를 수 있지만 전체 자격 판정은 동일하다. **PARTIAL·UNASSESSABLE은 전체 통과가 아니다.**

## 자동 검사와 증거 경계

- 사전 검증과 source/index metadata 결합: [로그](dictionary.final-contract.log), [영수증](LIVE-INTEGRATION-RECEIPT.json).
- 신규 의미·advisory 검색·잠금 회귀: [14개 검사](discovery-focused-tests.log).
- 기존 계약 복구 후 관련 회귀: [47개 검사](contract-repair-focused-tests.log), 모두 통과.
- **전체 자동 검사 1,157개 / 116개 모듈 모두 PASS:** [발견 목록](full-suite-final/FULL-TEST-DISCOVERY.json), [최종 결과](full-suite-final/FULL-TEST-RESULTS.json). 모듈별 격리 프로세스 6개로 전체 discovery를 빠짐없이 실행했으며 미실행·실패 모듈은 없다.
- 최초 전체 실행의 실패는 [원 기록](FULL-TEST-RESULTS.json)으로 보존했다. 기존 source 계약 복구, 과거 코퍼스의 정확한 범위 비교, 실제 의미가 동일한 current checksum 검토를 거쳤다. 평가 holdout이나 과거 기대값을 실패 이미지에 맞춰 고치지 않았다.
- 세 사례 composed/runtime 감사는 통과했다. 최초 생성의 strict gate는 `audit_moe_render_review.py`로 검사했다. 이와 다른 repair-lineage 계약을 최초 생성에 적용하지 않았다.

이미지는 기존 계약 복구 전 통합 revision에서 생성했다. 생성에 쓰인 원 pack·runtime·ledger는 보존했다. 최종 코퍼스의 별도 post-contract-repair pack에서도 A의 선택 후보 4개·프로필 1개, B의 선택 후보 2개, C의 선택 후보 1개가 노출되며 전체 선택 계약이 정확히 같다. [A 호환성](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-a/contract_compatibility_receipt.post_contract_repair.md), [B 호환성](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-b/post_contract_repair_comparison.md), [C 호환성](/Users/chasoik/Projects/image-prompt/runs/body-morphology-integration-20261002/case-c/post_contract_repair_comparison.md)은 모두 PASS이며 새 이미지 호출은 없다. 이미지를 최종 revision에서 새로 생성했다고 표시하지 않는다. 사용자의 이미지 수용 판정은 아직 없다. 원 연구의 제안 70사례와 총 92개 축 전체를 픽셀로 검증했다고 주장하지 않는다.

## 결과를 바탕으로 한 후속 적용 계획

1. **미노출 축 검색:** 어깨 폭/경사, 손마디, 압흔, 측굴 주름의 independent 표현을 새 holdout에 동결한 후 BM25F의 관찰별 focus와 전체 cap에서 누락 원인을 비교한다. 특정 후보 ID를 강제로 넣거나 기존 시험 문장을 exact alias로 승격하지 않는다. 모든 차원·property lock·제외 조건을 유지한다.
2. **촬영 구도와 관찰 조건:** 넓은 어깨는 양쪽 경계가 보이는 각도, 근육 윤곽은 상·하지의 면이 읽히는 빛, 길이 비율은 덜 굽힌 손과 비교 가능한 손바닥, 솜털은 native에서 개별 가닥이 보이는 크기로 검증한다. 핵심 작업·소유권·접촉을 유지할 수 있는지 프롬프트와 이미지에서 각각 확인한다.
3. **실패 유형별 경계:** 소름/모공/물방울, 혈관/그림/주름, 의복 압흔/천 주름/피부 접힘, actor-left/right를 반례와 함께 기록한다. 현재 실패를 제거하지 않고 새로운 장면·표현으로 재검증한다.
4. **승격 기준:** 새 독립 사례에서 모든 구성·엄격 게이트와 native 픽셀 조건을 충족해야 재현 성공으로 센다. 프롬프트 감사, image delivery 또는 일부 키워드 통과만으로 전체 성공이나 사용자 수용을 대신하지 않는다.

후속 계획은 제안이며 이번 작업에서 실행한 추가 이미지나 새로운 수용 기준이 아니다.

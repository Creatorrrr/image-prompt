# 신체 의미 데이터 실제 반영과 독립 이미지 시험

2026-10-02. 원 조사 91개 축을 반영하고, 독립 시험에서 발견한 소름/모공의 구분을 1개 축으로 추가했다. [실제 코퍼스 영수증](LIVE-INTEGRATION-RECEIPT.json)과 [최종 92축 매핑](FINAL-INTEGRATION-MANIFEST.json), [추가 의역·근거](SUPPLEMENTAL-SOURCES.md)를 함께 읽는다. [초기 매핑](INTEGRATION-MANIFEST.json)은 복구 전 이력으로 보존한다.

| 항목 | 기준선 | 현재 |
|---|---:|---:|
| 시각 프로필 | 1,419 | 1,496 |
| ordinary 후보 | 9,590 | 9,664 |
| 슬롯 | 112 | 112 |
| semantic index 전체 문서 | 9,626 | 9,700 |

신규 프로필 77개, 기존 검색 보강 10개, 원 계약 그대로 재사용한 프로필 5개, 신규 후보 74개, 기존 보강 후보 18개다. 기존 후보 중 13개에는 구조화된 구성·관계·효과 메타데이터를 추가했고, 나머지 5개에는 허용된 `existing_slot_context_extensions`로 동등한 의역만 추가했다. 기존 ID를 모두 보존했다. 보강한 기존 프로필의 definition·component·evidence·render gate·exact activation 계약은 그대로 두고 검색 의역/개념 단위만 확장했다. 국소 hip indentation은 전체 waist-to-hip transition과 별도 소유자를 가지며, 기존 넓은 의미를 약화하지 않았다. 중복 활성화를 막는 한정된 제외 문맥을 기존 transition에 추가했다. 의복 압박·stance·pose surface 등의 연동 효과는 실제 차원과 property 경로를 선언한다. 11개 측정·분류·커뮤니티·이력 지식 레코드는 연구 자료로 유지했다.

두 인덱스는 Gemini embedding 2, 768차원, batch size 1로 재생성했다. 현재 source/index hash, 문서 집합 및 오래된 메타데이터 거부 계약을 검사했다. 이전에 저장되어 있던 tracked shard 세대는 보존했으며 이번 검증에는 현재 manifest가 지정하는 16개 shard만 사용한다.

## 기존 계약 복구와 현재 코퍼스 비교

전체 검사에서 드러난 기존 PFE bundle·maintenance receipt·허벅지 인덱스 의미 변화는 [계약 복구 기록](LEGACY-CONTRACT-REPAIR.json)에 남기고 원 authored source로 복구했다. `ctx_c109` 역시 원 `body.skin` property-lock 소유권을 [복구](CONTEXTUAL-SCOPE-REPAIR.json)했다. 현재 비인물 대조 팩은 과거 팩의 64개 후보 전체, frozen core, 네거티브와 모든 의미 필드가 정확히 같고 코퍼스·검색 메타데이터 6개 경로만 다르다. 이를 완전 비교한 뒤 current V5 checksum/pack ID 두 필드만 [갱신](CURRENT-BOUNDARY-REFRESH.json)했다. V1–V4 이력과 frozen lexical/pixel holdout은 수정하지 않았다.

Liminal 과거 코퍼스 검사는 뒤에 추가된 두 extension을 제외해 과거 범위를 비교한다. 기존 base 후보 13개에는 정확히 선언한 신규 메타데이터 6필드만 추가되었고, 모든 기존 필드가 frozen row와 같다는 검사를 먼저 수행한다. 그 후 과거 코퍼스 전체·21 keep·수정 대상 1개의 원 비교를 유지한다. 원 평가 기대값을 바꾸지 않았다. 이 보존 비교와 기존 계약 복구 후 관련 검사 47개가 통과했다.

## 최초 노출과 수정

세 독립 에이전트는 실제 사용자 원문 envelope를 공유하고, 서로의 사례와 후보 데이터를 읽기 전에 각자의 난수 장면·baseline·V3 core·controls·feature selection·embodiment를 동결했다. 각 장면 및 키워드는 사용자 원문에 있었던 것처럼 표시하지 않고 agent-authored 시험 선택으로 기록했다. 참조 사진은 보이는 얼굴·머리 외형에 한정했다.

첫 actual pack에서 목표 후보가 충분히 노출되지 않았다. baseline/visual priorities에 세부 뜻이 있었지만 슬롯 focus와 전체 64개 후보 제한이 관찰별 목표를 누락했다. 원 core를 바꾸는 대신 일반 검색에서 source-opted-in 후보가 frozen visual priorities에도 대응하도록 보완했다. 후보의 모든 효과가 열려 있고 property lock에 맞는 경우에만 이 우선순위를 받는다. 검색 결과는 선택 후보이며 requester assertion이나 hard duty로 바뀌지 않는다. 검색 표현 12가족을 보강했고 시험 문장 전체·장면·출처를 prototype에 복사하지 않았다.

첫 팩과 개선 팩을 모두 저장했다. 이번 비교는 **데이터 의역과 공통 검색 변경을 함께 적용한 동일 frozen-core 비교**이며 데이터만의 독립 효과 또는 픽셀 품질의 인과적 개선을 측정한 실험은 아니다. 미노출 프로필을 선택된 것처럼 만들지 않았고, 신규 후보가 충분하지 않은 부분은 보고서에서 남긴다.

## 실행 증거

- [데이터·기존 계약 보존](LIVE-INTEGRATION-RECEIPT.json)
- [최신 사전 검사](dictionary.final-contract.log)
- [검색·잠금 회귀 14개](discovery-focused-tests.log)
- [최종 전체 unittest 발견 목록](full-suite-final/FULL-TEST-DISCOVERY.json), [모듈별 실행](full-suite-final/full-suite-modules/), [최종 1,157개 PASS](full-suite-final/FULL-TEST-RESULTS.json)
- [최초 전체 실패 이력](FULL-TEST-RESULTS.json), [복구 후 관련 검사 47개](contract-repair-focused-tests.log)
- [사례 A](../../../../../runs/body-morphology-integration-20261002/case-a/): 폭풍 뒤 온실 차광막 고정, 다리 비율·어깨·근육
- [사례 B](../../../../../runs/body-morphology-integration-20261002/case-b/): 새벽 옥상 사이아노타입 수세, 소름·체모·혈관
- [사례 C](../../../../../runs/body-morphology-integration-20261002/case-c/): 해질녘 강변 인형극장 수리, 손가락·손마디·의복 압흔·측굴 주름

Prompt literal audit, runtime binding, 실제 native pixel 판정, 사용자 수용은 각각 다른 증거다. 최초 생성의 profile/embodiment strict gate는 `audit_moe_render_review.py`로 검사한다. `audit_image_render_review.py`의 lineage repair 계약은 이번 최초 생성에 해당하지 않는다. 독립 키워드 조건은 별도로 전부 평가하며, pack strict gate가 통과해도 이 조건이 partial이면 사례 전체를 통과로 보고하지 않는다. 사용자의 이미지 수용 판단은 아직 받지 않았다.

원 연구의 제안 70사례는 모두 실행했다고 표시하지 않는다. 이번에 구현한 자동 테스트와 실제 생성한 3개 독립 사례만 실행 증거로 센다. 92개 축 전체가 픽셀로 검증되었다고 확대하지 않는다. 최종 이미지·키워드 판정과 전체 자동 검사 결과는 `RESULTS.md`에 정리한다.

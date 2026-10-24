# 메카·로봇 데이터 반영 및 독립 이미지 테스트

2026-10-24 KST. 이 문서는 앞선 리서치 이후 사용자가 요청한 실제 반영과 이미지 테스트의 실행 기록이다. 독립 에이전트 3개가 첨부 사진을 사용해 각각 1회씩 생성했고, 부모 에이전트도 저장된 원본 픽셀을 직접 확인했다. 신규 후보 관계와 장면 전체의 완전성은 따로 판정한다.

## 반영한 데이터

| 항목 | 반영 범위 |
|---|---|
| 시각 의미 | 카드 108개, 관계 413개, 맥락 경계 32개, 원문 항목 323개 |
| 선택적 양성 후보 | 전체 한영 장면을 보존한 106개 |
| 진단용 기록 | 보류 카드 G03·K06 및 맥락 경계, 총 34개. 양성 검색에서 제외 |
| 슬롯 연결 | 실제 카탈로그의 선택적 binding 228개 |
| 기존 데이터 | 기존 후보의 본문·조건·효과·provenance, 기존 binding·catalog·정책 보존 |

구체적인 대상은 착용 프레임과 탑승 기체의 구분, 액추에이터 양끝 고정, 외장과 내부 프레임, 좌석과 조종자의 접점, 케이블 양끝, 정비 도구 끝과 기체 점검구, 인양과 지지, 기계 손상과 유기체 손상, 사진과 표시 화면·도면의 구분이다. 고유 설정·의식·의도·동의·기능을 보이는 외형으로 바꾸지 않았다.

새 후보는 완전한 선택적 창작 문장으로 등록했다. 연구 graph와 출처 인용은 검토 근거이며 기존 장면 소유자를 바꾸는 권한이 아니다. 모든 신규 기록의 `native_approval`은 `false`다. H-F2의 `inspiration_only` 노출과 특정 source의 완전한 네이티브 자격은 구분한다.

원본과 카드별 채택 판단은 [data-integration.json](integration-evidence/data-integration.json), [adoption-decisions.json](integration-evidence/adoption-decisions.json), [시각 의미 안내](../../../../skills/photo-prompt-image-generator/references/mecha-robot-visual-semantics.md)에 있다. 정확한 후보 CID는 첫 JSON의 `candidate_mapping`을 따른다.

## 검증과 런타임

소유자·양끝·양언어·진단 경계 회귀 검사 10개가 통과했다. 검사는 source 계약을 검증하며 생성 이미지 품질을 증명하지 않는다. [focused-tests.json](integration-evidence/focused-tests.json)

최신 설치된 봉인 커널을 그대로 보존하고 source만 추가했다. 작업본의 오래된 구현과 혼합하지 않았다. 첫 검색본은 네이티브 양성 후보 벡터 20,623개를 재사용하고 새 후보 106개만 로컬 모델에서 계산했으며, 전체 layout·payload·vector closure를 검증했다. H-F2의 기존 문서 벡터 20,625개도 동일하게 보존했다. [native-index-build.json](integration-evidence/native-index-build.json), [successor.json](integration-evidence/successor.json)

작업 중 기본 검색본에 캠퍼스, 이어 로맨틱 코미디 데이터가 추가돼 두 번의 활성화 사전 검사가 중단됐다. 해당 기본본을 덮어쓰지 않고 그 전체 source 위에 메카 모듈을 합친 후속본의 **설치·기본 활성화를 완료했다**. 기존 canonical source 21,947개를 유지하고 140개를 추가한 22,087개 기록 및 양성 20,928개, H-F2 문서 20,930개를 검증했다. 커널 코드는 기존과 동일하다. [최종 source 보존](integration-evidence/rebase2-canonical-source-validation.json), [설치·활성화](integration-evidence/rebase2-install-active.json), [설치 환경·기록기 확인](integration-evidence/default-runtime-check.json)

활성 H-F2는 `04dde7d3fc5db9cfd0d66cb9e1a99c5944b4f0dda7b959950b8eedfcedcdf7d0`, native는 `5f5ae5a10e1e445c428fe51a8d231fa9e546ebef4efb6d855ee11c127fa705f7`다. 세 이미지 테스트는 설치를 먼저 마친 동일한 메카 H-F2 `e1a3d0cb7623488dfbfff9f0b8337200cef8c0142248414c0a0f4b890faecc71` / native `e51d43e44abad75550a4213b3de14028697c1470dc1c42a31b895029886b32ea`에 고정했다. 이 두 버전의 메카 후보·binding 파일은 [byte-exact 대조](integration-evidence/runtime-mecha-parity.json)까지 통과했다. 이후 동시 변경을 보존한 기본본 활성화가 과거 테스트 버전까지 바꾸지는 않는다.

작업 시작 시 작업본 자체의 source와 파생 인덱스가 이미 달랐다. 이 사실과 설치된 봉인 검색본의 유효성은 별개다. 작업 중 작업본의 파생 인덱스도 다른 변경으로 갱신돼, 디렉터리 전체가 시작 시점과 byte-exact라는 주장은 하지 않는다. 메카 빌더는 별도 staging의 파생 파일만 작성했고 기존 후보 source를 보존했다. [pre-existing-index-state.json](integration-evidence/pre-existing-index-state.json), [protected-source-check.final.json](integration-evidence/protected-source-check.final.json)

## 독립 테스트의 방법

세 서브에이전트는 서로의 콘셉트·프롬프트·후보 선택을 받지 않았다. 각자 새 seed로 콘셉트를 정하고 candidate-free 기본 장면과 테스트케이스를 먼저 고정한 뒤 검색했다. 동일한 실제 사용자 요청과 동일한 첨부 사진을 사용했다. 사진은 보이는 얼굴·단발 형태의 참고이며 배경·복장·정체·서사의 증거로 쓰지 않았다.

| Arm | 독립 콘셉트 | 주요 구조 확인 |
|---|---|---|
| A | 폭풍 뒤 옥상 온실에서 휘어진 설비 문을 잡는 착용형 보조팔 작업자 | 신체와 외부 프레임, 커프·링크, 손의 그립과 지지 대상 |
| B | 말라붙은 내해의 거대 탐사 보행기와 열린 흉부 조종석의 파일럿 | 사람과 기체의 스케일·소유, 실제 선택한 조종석 접점 |
| C | 마지막 배가 떠난 여객터미널에서 서비스 로봇의 전완을 정비하는 작업자 | 별도 인간과 로봇, 점검구·내부 구조·공구 끝의 실제 접촉 |

각 arm은 신규 source의 실제 노출, 전체 의미 검토와 채택, 프롬프트 전달, 이미지 도구의 반환 파일, 저장 픽셀의 관계를 각각 기록한다. 사진의 분위기나 부품 하나의 유사성으로 전체 경로를 통과시키지 않는다. `partial_is_fail`, `UNOBSERVABLE_NOT_PASS`를 적용한다. 부모 검토 기준도 이미지 도착 전에 [parent-review-contract.json](integration-evidence/parent-review-contract.json)으로 고정했다.

세 장은 106개 양성 후보나 323개 원문 항목 전체에 대한 검증이 아니다. 앞선 48쌍 검색·12개 맥락 회귀 계획 전체를 실행한 것으로도 기록하지 않는다. 사용자 수용 판단은 아직 받지 않았다. 이미지 호출은 arm당 최초 1회 범위이며, 결과 저장이나 증거 보완만으로 재호출하지 않는다.

## 이미지 결과와 별도 판정

| Arm | 신규 데이터의 실제 사용 | 신규 후보 시각 관계 | 장면 전체의 엄격 판정 |
|---|---|---|---|
| A | 반환 32회·고유 원문 28개 중 신규 CID 0. 채택 없음 | 해당 없음. 신규 데이터의 원인적 기여 미입증 | 하네스→위팔 연결이 가려져 외부 지지 경로 불완전. 손잡이·받침대·부츠 접점은 보임 |
| B | F13, `cand_c8be7d8fe59c593eb879ec256793c82a`, baseline query에서 실제 반환·검토·프롬프트 반영 | **5/5 통과**. 기체 자신의 왼어깨 큰 사각판, 오른어깨 작은 둥근 외장, 같은 몸통 연결 | 인물의 손 역할이 프롬프트의 좌우와 반전. 부츠·조종석 바닥과 가까운 기계 다리의 지면 끝점이 가려짐 |
| C | J01, `cand_6706eaae3c8b52e7afef740b3b8c99da`, relational-action query에서 실제 반환·검토·프롬프트 반영 | **5/5 통과**. 몸통 소유 빈 소켓, 분리된 팔, 공기 간격, 두 분리 끝에서 나온 별도 케이블 | 공구 접촉은 보임. 지지 손이 노출 전완 프레임보다 손목·손바닥 쪽에 있으며 정확한 팔꿈치 구조는 불명확 |

위 2/3은 이번 세 사례에서 신규 원문이 실제 반환됐다는 관찰이며 전체 검색 recall이 아니다. B·C의 5/5는 선택한 보충 시각 명제의 검증이며 `native_approval`, 장면 전체의 완전 통과, 사용자의 수용 판단을 뜻하지 않는다. 엄격한 전체 장면 완전성은 세 장 모두 통과로 올리지 않았다.

### A — 옥상 온실의 착용형 보조팔

![A 생성 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-a/result.png)

A는 신규 후보 미노출을 실패로 보존했다. 기존에 발행된 receipt를 확인하면 baseline의 32개 rank window 안에 G01이 하나 있었지만 고정된 8개 sample에 들지 않았다. 나머지 세 query의 window에는 신규 CID가 없었다. sample 밖 원문을 읽거나 선택한 것으로 처리하지 않았고 재검색·재샘플링하지 않았다. [노출 증거](image-tests/arm-a/new-source-exposure.json)

또한 frozen concept/event 앵커의 `wearable robotic equipment`, `field work with robotic equipment`에는 사용자 소유의 넓은 메카 주제보다 좁은 에이전트의 구도 선택이 섞였다. 이는 작성 절차의 의미 소유 한계다. 구조적 freeze·감사 통과가 이 오류를 치유하지 않으므로 최신 스킬의 완전한 의미 자격 사례로 처리하지 않는다. 호출 후 core를 고치거나 순서를 소급 기록하지 않았다.

[A 상세 결과](image-tests/arm-a/report.md) · [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-a/prompt_en.txt) · [작성 한계](image-tests/arm-a/authoring-limitation.json) · [부모 픽셀 검토](integration-evidence/parent-pixel-review-a.json) · [테스트케이스](image-tests/arm-a/testcase.json)

### B — 말라붙은 내해의 탐사 보행기

![B 생성 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-b/results/inland-sea-walker.png)

기체가 정면에 가깝게 보여 자신의 왼어깨는 화면 오른쪽이다. 이쪽에 큰 사각판과 몸통 연결부가 있고 반대쪽에는 작은 둥근 외장과 연결부가 함께 보인다. 부모의 독립 검토와 arm의 검토가 F13 5개 게이트에 일치했다. 전체 프롬프트 대조에서 부모가 인물의 팔 좌우 반전을 추가로 발견했고, arm이 원본을 재확인해 관찰 기록을 수정했다. 프롬프트나 이미지를 바꾸지는 않았다.

[B 상세 결과](image-tests/arm-b/RESULT.md) · [프롬프트](image-tests/arm-b/prompt.txt) · [전달 증거](image-tests/arm-b/transport-proof.json) · [부모 픽셀 검토](integration-evidence/parent-pixel-review-b.json)

### C — 여객터미널의 서비스 로봇 정비

![C 생성 원본](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-c/result.png)

두 케이블 묶음이 각각 빈 소켓과 분리 팔의 끝에서 나오는 것을 같은 원본에서 확인했다. 두 끝 사이의 공기 간격이 남아 있으며 별개의 느슨한 전선으로 추정해 통과시킨 것이 아니다. 공구 축과 끝이 손목 쪽 체결부에 닿는 것도 보인다. 전체 팔의 정확한 관절 역할과 프롬프트의 모든 손 지지 위치를 이 국소 성공으로 대신 증명하지 않는다.

[C 상세 결과](image-tests/arm-c/report.md) · [C 사전 테스트케이스](image-tests/arm-c/testcase-pre-generation.json) · [프롬프트](/Users/chasoik/Projects/image-prompt/generated/photo-runs/mecha-20261024-arm-c/final_prompt_en.txt) · [부모 픽셀 검토](integration-evidence/parent-pixel-review-c.json)

## 남은 보강 순서

1. A의 후속 실행은 새 중립 core에서 메카 주제·참조 외형만 사용자 소유로 묶고 착용형·현장 작업은 에이전트 선택으로 남긴다. 기존 run의 타이밍과 기록은 보존한다.
2. 기존 48쌍 검색 및 12개 맥락 회귀 계획을 실행해 rank window 부재와 고정 sample 탈락을 구분한다. A05 같은 실제 구조 후보의 자연어 접근성을 확인하며, broad 용어를 동의어·자동 활성 조건으로 무리하게 붙이지 않는다.
3. 전체 자세 검증에서는 조종자의 좌우 손, 부츠·좌석 바닥, 기계 다리의 지면 끝점, 하네스 접속과 팔 관절을 충분한 크기로 배치한다. 필요하면 개요와 접점 상세를 다른 테스트로 분리한다. 이번 결과에 맞춰 기존 게이트를 낮추지는 않는다.
4. 106개 양성 후보 전체의 이미지 검증, 보류 출처 해소, 독립 양언어 검토와 특정 native 자격은 별도 남은 작업이다. 이번 두 보충 관계의 성공으로 일괄 승인하지 않는다.

## 실행 상태

**데이터 등록, 합본 설치·기본 활성화, 독립 생성 3회, 원본 픽셀 검토, 최종 증거 대조를 완료했다.** [FINAL-VALIDATION.json](integration-evidence/FINAL-VALIDATION.json)은 세 이미지의 해시, 동일 참조 사진, composed/native prompt 일치, 관리 리뷰 기록, 부모 픽셀 검토, 변경되지 않은 사전 테스트케이스와 활성 generation을 함께 대조한 결과다.

리뷰 기록은 3개 모두 유효하지만 엄격한 전체 장면 자격은 A 4/5, B 2/5, C 2/5로 **0/3 완전 통과**다. B·C의 보충 source 관계 5/5씩 통과와 구분한다. 실제 사용자 수용 판단은 아직 받지 않았다. 106개 전체의 native 승인·이미지 검증 또는 이전 48쌍 검색 계획 전체 완료로 확대하지 않는다. commit·push는 요청되지 않았으며 실행하지 않았다.


## 2차 보완·독립 재시험 (2026-10-24)

A12 상지 외골격 출처 1개·선택 바인딩 3개와 최상위 적격 후보를 유지하는 샘플링 v2를 반영했다. 같은 사진으로 독립 3안에서 각각 1회 생성하고 고정 기준으로 원본 픽셀을 재검토했다. 집중 테스트 76/76과 세 관리 리뷰 기록은 유효하지만, 엄격한 전체 프롬프트 충족은 **0/3**이다. A는 양팔 소유자 혼합(일반 1/5, 새 A12 3/8), B는 남은 전체 전완 받침 조건(8/9), C는 지지 손목 경로 가림(5/9)으로 실패했다. B의 실제 좌우·발 접점 및 C의 팔꿈치·중간 프레임 접점은 개선됐다.

신규 출처는 A 1개/B 0개/C 2개가 노출됐고 A만 A12를 참고 반영했다. 신규 출처의 완전한 픽셀 자격은 통과하지 않았고 native 승인도 올리지 않았다. 이전 결과·원장 행·고정 기준을 보존했다. 후속 수정 초안은 미생성이며 이번 결과를 대신하지 않는다. [2차 전체 결과](repair-round-2/REPAIR-RESULTS.md) · [최종 대조 명세](repair-round-2/FINAL-RESULTS.json)

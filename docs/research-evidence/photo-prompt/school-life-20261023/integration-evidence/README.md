# 학원물 자료 반영과 독립 참조 이미지 테스트

현재 사용자 요청에 따른 구현·실행 증거다. 상위 연구 폴더의 연구 당시 `NOT_RUN` 기록과 hash는 과거 사실로 보존한다.

## 구현 범위

의미 카드 90개와 원래 키워드 210개를 등록했다. 한영 전체 문장으로 구성한 시각 후보 66개, 양성 검색에서 제외하는 문맥 진단 24개, 기존 catalog와 연결하는 선택적 binding 139개다. 장면의 주인·관계 양끝·지지면·복식의 층위·기록 매체·혼동 경계와 비가시 주장의 한계를 보존한다. 연구 그래프는 source 사용 권한이나 native qualification으로 승격하지 않는다.

등록 직전의 기존 후보 20,613개와 binding 15,489개를 보존했다. 기존 모듈의 바이트가 동일함을 확인했다. 공유 작업에서 먼저 추가된 자료도 유지했다. 첫 등록 시도는 동시 소스 변경을 쓰기 전에 감지하여 중단했다. 이 작업이 남긴 미완료 revision은 새 모듈이 전혀 쓰이지 않았음을 확인한 뒤 정확한 token으로 종료하고, 최신 소스를 기반으로 다시 등록했다.

근거: `source-preservation.json`, `source-rebase.json`(실제 재기반이 필요했을 때), `source-revision-repair.json`, `data-integration.json`, `canonical-source-validation.json`.

## 검색 세대

설치된 검증 세대의 전체 source와 실행 코드를 그대로 복사하고 이번 90개 source 및 139개 binding만 더한다. 작업 중인 다른 코드나 미설치 자료는 이 설치에 포함하지 않는다. 설치된 source 기준 기존 CID는 20,329개이며, 작업 폴더 전체와 수가 다른 것은 별도의 설치 경계를 유지하기 때문이다. 새 설치 대상 CID는 20,419개다. canonical 변환은 literal의 정확한 소유와 원문을 보존하며, 원래 record와의 역변환 equality를 확인한다.

기존 양성 CID 19,846개의 native vector는 본문·recipe·space 일치 확인 후 재사용하고, 새 양성 66개는 동일한 local EmbeddingGemma-2 공간에서 계산한다. F2의 전체 문서·역색인·global 통계를 새 source union에서 봉인한다. 기존 설치와 과거 run은 보존한다. 실제 세대 ID·설치 상태는 `successor.json`, `install.json`을 따른다. 설치는 PASS이며 `activated:false`, `CURRENT_writes:0`이다. `install-active.json`은 생성되지 않았고 기본 세대 활성화는 수행하지 않았다.

## 사전 정의한 검색 점검

`retrieval-development-cases.json`의 202질의: 카드에서 파생한 66개 한영 시각 질의 132개, 32개 한영 경계 질의 64개, 일반 장면 한영 control 6개다. 전체 계획의 정확한 로컬 질의 벡터 202개를 먼저 계산했다. 실제 검색은 결과가 영속 저장되기 전에 고정한 대표 24질의(양성 12, 경계 6, 일반 대조 6)에 대해 완료했다. 양성 12질의는 모두 목표 후보가 top10에 나타났고 일반 대조 6질의는 새 학원물 후보의 top10 노출이 0건이었다. 양성 집합에는 진단 source가 없음을 확인했다. 나머지 178질의는 NOT_RUN이다. 원래 202질의 실행 시도는 결과 파일과 완료 상태를 남기지 못했으므로 성공으로 세지 않는다. 실제 범위·선정 시점은 `retrieval-execution-scope.json`, 완료된 순위 증거는 `retrieval-qualification.json`을 따른다. 경계 질의의 검색 결과를 본 것만으로 자동 추론·문장 채택의 안전성을 검증했다고 주장하지 않는다.

이 자료는 개발 점검이며 독립 holdout이 아니다. 이전 계획의 30사례 holdout과 보강 전후 36장 비교는 이번 요청의 독립 컨셉 3장 테스트로 대체하여 수행한 것으로 간주하지 않는다. 이번 3장은 현재 스킬과 새 자료가 연결되는지 확인하는 작동 사례이며 인과적 성능 개선이나 전체 장르 성공률을 증명하지 않는다.

## 독립 arm

실제 사용자 메시지 전체, literal active span, 이전 사용자의 정확한 학원물 topic, 실제 JPEG hash를 coordinator가 envelope로 먼저 고정했다. 세 agent는 서로의 프롬프트·후보·연구 자료를 보지 않고 최신 SKILL과 neutral precore만으로 core를 작성·동결했다. 컨셉과 연령·구도는 agent의 창작 선택이며 사용자 고정 조건이나 첨부 인물의 사실로 승격하지 않았다.

| Arm | 독립 장면 | 핵심 관찰 대상 |
|---|---|---|
| A | 방과 후 대학 학생회 공개 표결 | 진행자와 두 거수자의 주의, 회의록 작성자, 공유 책상과 학교 회의 맥락 |
| B | 학교 축제 전 미술 동아리의 실크스크린 인쇄 확인 | 두 손과 스크린 rail, hinge, 인쇄물, 동료가 가리키는 동일 결과물 |
| C | 방과 후 미술실의 그림 속 문간과 실제 문간의 차이 | 같은 3칸 상부창, 그림 속 실루엣과 실제 빈 공간, 시선, 양손과 그림판·탁자 지지 |

각 run은 `generated/photo-runs/school-life-20261023-{a,b,c}`다. core hash·스킬 hash·원본 envelope는 각 `arms/`와 run의 보고서에 남긴다. 테스트 기준은 후보/이미지를 보기 전에 작성하여 hash를 보존한다. 이후 실제 source 노출·심사·선택·프롬프트 audit·호출·반환 픽셀을 각각 기록한다.

이미지가 없는 호출은 `BLOCKED_UNSCORED`, 필요한 관계가 일부만 보이면 `partial_is_fail`, 가려진 증거는 `UNOBSERVABLE_NOT_PASS`다. reference 외형 유사성은 보이는 얼굴·머리 모양의 별도 판단이며 실제 신원이나 나이를 인증하지 않는다. 자세한 결과는 최종 작성되는 `INTEGRATION-RESULTS.md`와 각 arm의 보고서를 따른다.

## 발행 상태

이번 요청은 자료 반영과 테스트다. commit·push·PR은 수행하지 않는다. 소스 등록, 검증 설치 활성화, 로컬 생성 이미지, 사용자 수용을 구분한다.

빌드 중 다른 작업이 기본 검색 세대를 갱신했다(`default-advanced.json`). 이 변경을 덮어쓰지 않는다. 학원물 검증 세대는 비활성 설치하고 각 arm의 첫 retrieve에 `--runtime-store`와 `--generation-id`를 함께 명시하여 고정한다. 이후 run은 자신의 sealed binding을 재사용한다. 원래 계획의 기본 세대 활성화는 이번 실행의 완료 항목으로 세지 않는다. 작업 소스에 등록된 자료, 명시적으로 사용한 검증 세대, 현재 기본 세대는 별개의 상태다.

## 실제 생성과 원본 픽셀 결과

독립된 세 agent가 각각 내장 이미지 도구를 한 번 호출하여 PNG 세 장을 반환받았다. 재생성은 없다. 원본 참조의 실제 경로/hash를 각 native payload에 바인딩했고, 최종 프롬프트·native plan·호출·원본 이미지 hash를 각 run에 기록했다. 이미지 도구가 모델 이름을 노출하지 않았으므로 특정 모델 실행을 주장하지 않는다.

부모가 저장된 원본 세 장과 정확한 참조를 직접 다시 보았다. 부모는 사전 계획과 컨셉을 알고 있었으므로 블라인드 평가가 아니다. 사용자 선호·수용은 아직 확인되지 않았다. 학교 일상 주제와 참조 외형의 연속성은 세 장에서 모두 관찰됐지만, 사전에 정한 전체 사례는 모두 FAIL이다.

| Arm | 원본 픽셀 판정 | 필수 기준 미달 |
|---|---|---|
| A 학생회 표결 | 7/9; 전체 FAIL | A07 펜–노트 연결이 손에 가려짐. A08 핵심 기록 관계의 완전한 동시 가시성 부족. |
| B 미술부 축제 인쇄 | 11/14; 전체 FAIL | B08 젖은 잉크 상태, B09 손끝–종이 공기 간격, B12 잘리지 않은 종이 전체를 확인할 수 없음. |
| C 미술실 미스터리 | 7/8; 전체 FAIL | C01 지정한 남색 바지가 눈에 보이는 주름치마로 바뀜. 가로형 그림판→세로형 편차도 별도 관찰. |

B의 최초 독립 보고는 12/14였다. 부모가 종이 앞쪽 경계를 추가 점검하고 agent가 원본 하단을 재확인하여 B12를 비통과로 보정했다. 원래 보고서는 보존하고 별도 addendum으로 11/14를 기록했다. B02의 집게 인쇄물은 창 유리 앞·상부 창틀 아래에 걸려 보이며, 창문 전체 아래라는 정확한 위치는 입증하지 않는다. 원래 기준에 없던 sill 높이 조건을 추가하지 않았다.

자세한 gate별 증거는 `parent-arm-{a,b,c}-pixel-review.json`, `pixel-summary.json`과 각 run의 원본 pixel report/addendum을 따른다. 기술 기록의 유효성 PASS는 픽셀 기술 자격이나 전체 사례 PASS가 아니다.

## 새 데이터의 실제 영향

| Arm | 전체 고유 source / occurrence | 새 학원물 source / occurrence | 새 자료 최종 inspiration / native 채택 |
|---|---:|---:|---:|
| A | 33 / 33 | 8 / 8 | 0 / 0 |
| B | 36 / 40 | 5 / 6 | 0 / 0 |
| C | 34 / 40 | 5 / 8 | 0 / 0 |

모든 반환 source와 query별 occurrence의 완전한 본문·조건·effects를 검토하고, 독립 baseline과 구체 대안을 비교했다. A와 C는 기존 source의 일반적인 표제 가시성/창빛 경계 속성을 소폭 반영했고 B는 baseline을 유지했다. 새 학원물 source는 최종 시각 명제에 채택되지 않았다. 따라서 세 이미지에서 주제가 보인다는 관찰을 새 데이터로 인한 인과적 개선, 새 source의 native approval, 90개 의미 카드 전체의 픽셀 자격으로 승격하지 않는다.

## 후속 보강 계획

- A는 펜과 페이지 접점이 손 뒤로 숨지 않도록 노트 방향·손 위치·카메라 시선을 함께 설계한 후 같은 사례를 재시험한다.
- B는 종이 전체가 프레임 안에 남는 여백, 손끝 간격의 대조 배경, 젖은 잉크 표면을 구별할 광선을 별도의 관찰 관계로 다룬다.
- C는 바지의 분기와 그림판의 가로 방향이 실제로 보이는 구도를 다음 revision에서 설계한다. 현재 결과와 테스트 기준은 보존한다.
- 새 후보가 독립 장면에 실제 채택되지 않은 원인을 후보 적합성·닫힌 효과·조건·표현 범위별로 나누어 검토한다. 교실 소품이나 공동 주시라는 일반성만으로 시험·회의·포트폴리오 등 완전한 source를 잘라 쓰지 않는다.
- 위 수정은 이번 최초 3장 결과를 소급 변경하지 않는다. 새 revision/새 이미지가 필요하며 이번 실행에서는 수행하지 않았다. 원래 holdout·동일 core의 보강 전후 비교도 미실행으로 유지한다.

## 최종 산출물과 감사 상태

각 workflow의 최종 phase는 `prompt_delivered`이며, 세 run 각각의 workflow artifact 28개(합계84개)의 파일 hash가 일치한다. A/B는 관리형5개 신체관계 기술 gate에서도 미통과다. C는 이5개 관계 gate를 통과하지만 의복을 포함한 별도의 사전8개 testcase는 미통과다. 세 가지 판정 층을 합치지 않는다.

A의 최종 텍스트 파일에는 마지막 LF 한 개가 있다. 파일SHA는 `bd58508814ee7e13306938ec86a4e747297f1d692d3191e6f2d515d6afcf4cc3`, 실제 canonical native payload SHA는 `2213cb86edd86e1b01b5b60a2c5507711f3a91541fa62a84958126de5ec2095c`이다. LF를 제외한2045자가 정확히 같다. B/C는 텍스트 파일과 recorded payload가 바이트 단위로 같다. 원본 파일을 소급 수정하지 않았다.

| Arm | 원본 이미지 | 프롬프트 | 세부 픽셀 보고 |
|---|---|---|---|
| A | [PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-a/images/attempt-1.png) | [text](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-a/authoring/final_prompt.txt) | [report](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-20261023/integration-evidence/parent-arm-a-pixel-review.json) |
| B | [PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-b/results/arm-b-native-01.png) | [text](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-b/authored/final_prompt.txt) | [report](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-20261023/integration-evidence/parent-arm-b-pixel-review.json) |
| C | [PNG](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-c/images/native-1.png) | [text](/Users/chasoik/Projects/image-prompt/generated/photo-runs/school-life-20261023-c/authored/final_prompt.txt) | [report](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-20261023/integration-evidence/parent-arm-c-pixel-review.json) |

전체요약은 `pixel-summary.json`, source노출은 `composition-summary.json`, 최종바인딩은 `workflow-closeout.json`, 보존·해시는 `workflow-artifact-integrity.json`과 최종SHA256SUMS를 따른다. source 파일과 자료별 전역 pixel_qualification은 이번3장으로 PASS 승격하지 않았다.

최종 증거 목록: [SHA256SUMS](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/school-life-20261023/integration-evidence/SHA256SUMS). 범위와 제외 항목은 `EVIDENCE-SCOPE.json`에 적었다. 이 목록은 staging 허가가 아니다.

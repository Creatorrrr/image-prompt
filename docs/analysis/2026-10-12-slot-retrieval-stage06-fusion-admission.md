# 6단계: 슬롯 후보 fusion·한도 검증 및 수정

RRF 점수가 같은 경우에만 **현재 슬롯의 owning focus에 원본 alias가 긍정적으로 명시된 후보**를 ID 사전순보다 먼저 배치하도록 수정했다. 영문 사리·태국 의상 2건이 동일한 64·4·2 한도에서 회복됐다. 자연어 20개 사례의 후보 집합과 필요 후보 13개는 유지됐다. 7단계는 진행하지 않았다.

## 수정 범위와 원인

`retrieve_core_slots`의 private fusion 정렬에 조건 1개와 `Counter` 집계를 추가했다. RRF score와 lane count가 다른 후보의 순서는 바꾸지 않는다. 기존 broad/focal 교집합, eligibility, excluded·context·property lock, frozen observation, typed owner 대표 후보, 중복 제거와 admission을 유지했다. 원본 alias가 없거나 owning focus에 없는 동점은 기존 ID 순서를 유지한다. 별도 ID·언어·주제 whitelist와 padding·quota를 추가하지 않았다. public pack에는 rank·score·trace를 넣지 않았다.

두 영문 사례에서 목표 후보는 broad 1위·focus 2위, 일반 호텔 유니폼 후보는 broad 2위·focus 1위였다. 둘의 RRF는 `0.063508064516`으로 같았다. 기존 ID 정렬에서 일반 유니폼이 먼저 나오면서, 슬롯 cap 안에 있던 요청 의상 후보가 전체 cap에서 탈락했다. 원어 alias는 의상 owning focus에 명시돼 있으므로 이 동점만 해결했다. public 후보의 채택은 계속 optional이다.

무조건 whole 순위를 동점 기준으로 쓰는 비교는 자연어 13개 사례의 후보 집합을 바꿨고, whole 대표 추가·모든 focus 대표 추가는 각각 20개·20개를 바꿨다. 모든 focus 대표 추가는 기존 원어 양성을 8/10에서 4/10으로 줄였다. observation보다 첫 round를 먼저 두는 변경은 영문 2건과 원래 49건을 회복하지 못했다. 필요 이상의 변경은 채택하지 않았다. 최종 owning-alias 조건은 자연어 후보 집합 변경이 0개였다.

## 동일 입력 결과

| 검증 | A9 기준선 | 6단계 수정 |
|---|---:|---:|
| 원어 의상 양성의 목표 후보 노출 | 8/10 | 10/10 |
| 인쇄물·제외 조건의 의상 오노출 | 0/10 | 0/10 |
| 자연어 필요 후보 노출 | 13/13 | 13/13 |
| 자연어 후보 집합 변화 | 기준선 | 0/20 |
| 주체 의미 이탈 사례 | 2/20 | 2/20 유지 |
| 공개 CLI·composer view·재계산 오류 | 0/40 | 0/40 |
| 후보 삭제 변조 탐지 | 40/40 | 40/40 |
| core·controls 변경, cap 위반, private rank 유출 | 0 | 0 |

입력은 수정 전에 고정한 원어 20개·자연어 development 8개와 holdout 12개·원래 source 유래 probe 49개, 총 89개다. 원본 fixture, 정규화 core/controls와 기존 필요 후보 기준을 바꾸지 않았다. private trace는 실제 기준선 `retrieve_core_slots`와 89/89 일치했고, 최종 실제 코드도 owning-alias 단일 요소 실험과 89/89 일치했다. 공개 CLI 40개는 별도로 실행하고 fresh composer worker와 source 재계산·omission tamper를 검증했다. 과거에 이미 본 holdout이며 새로운 blind 평가로 주장하지 않는다.

주체가 비어 있던 자연어 4개는 그대로이며 이를 의미 PASS로 합산하지 않았다. `holdout-05-world-treaty-en`의 world survey 주체와 `holdout-10-fantasy-ko`의 rover 주체는 source/context guard가 허용하는 기존 이탈이다. 순위 변경으로 감추거나 해결했다고 세지 않았다. 후보 노출 검증이며, 후보를 선택·거절한 최종 composition, postcomposition embodiment, 이미지·픽셀·사용자 판단은 7단계 또는 별도 검증 범위다.

## 원래 49건의 현재 원인

전체 cap 탈락 44건, 슬롯 cap 탈락 4건, 현재 공개 source에 없음 1건이다. 최종 수정으로 이 49개 목표가 회복된 수는 0개다. 넓은 source 유래 문장을 장면 입력으로 만든 lower-level probe이며 독립적인 요청 품질 평가로 합산하지 않았다. 같은 cap에서 모든 source 제안을 강제로 노출하는 변경은 채택하지 않았다.

`procedure_step:ia_magnifier_target` 1건은 원본 primary의 미커밋 `photo_prompt_intellectual_activity_extension.json`에만 있다. primary manifest에는 등록돼 있지만 A9 source 파일과 manifest에는 없다. 별도 진행 중인 데이터를 이 단계에 섞어 복구하지 않았다. 슬롯 cap 4건은 observation 우선순위 또는 RRF 뒤의 슬롯 한도로 구분해 private trace에 보존했다.

## 실행 가능한 기준선 복구

깨끗한 A9 체크아웃은 semantic manifest가 참조하는 `9a302591…` 활성 shard 16개가 빠져 있어 publisher가 `missing snapshot member`로 거절했다. A9에 커밋된 16개는 다른 `9c14b95f…` 경로였다. 기존 검증 완료 generation `3f6fe854…`의 **manifest 참조 경로와 SHA-256이 일치하는 정확한 bytes**를 기준선·수정 worktree에 각각 복구했다. manifest·원본 source·index 내용을 맞춰 쓰거나 벡터를 계산하지 않았다. 복구 후 기준선 generation은 기존 `3f6fe854…`와 같았다. 수정 배포 범위에는 이 누락된 활성 shard 16개가 포함돼야 한다. 기존 shard와 역사 증거는 삭제하지 않았다.

원본 source와 loader·BM25F·semantic slot ID는 112개 슬롯·11,977개 후보 모두 일치하며 missing·extra·중복·label 변경이 0개다. semantic 12,013개와 visual 3,791개는 유지됐고 1,310개 asset 파일이 복구한 A9 기준선과 byte 단위로 같았다. tokenizer/공유 BM25F/index/text/vector 변경과 embedding 호출은 0개다. dictionary validator와 visual freshness check가 통과했다. 공유 ranker가 바뀌지 않았으므로 과거 전체 exact sweep을 새로 실행했다고 주장하지 않는다.

## 회귀와 상태

고유 selector 47개(새 fusion 테스트 4개 포함)가 통과했다. 밀집·희소·empty/no-hit, 모두 거절, source 순서 반전, 같은 cap, owning focus 밖 alias, type/lock/owner 경계, optional·재계산을 검사했다.

전체 discovery: 2102개 발견, 2018개 실제 실행, failure 30개·error 69개, 수집 오류 12개다. 실패 기록 99개가 A9 기준선에서 같은 selector·failure/error 종류·정규화 exception으로 재현됐고 신규/다른 exception 기록은 0개다. 이 중 역사 복구 7개는 초기 실행에서 set 순회 때문에 먼저 보고된 불일치 파일이 달랐다. 두 root의 asset bytes는 같고, 해시 시드 0에서 양쪽이 같은 color obligation 파일로, 해시 시드 6에서 원래 전체 실행과 같은 semantic manifest로 실패했다. 원래 로그를 보존하고 동일 시드·동일 selector의 실제 양쪽 재실행으로 차이를 설명했다. root·임시 디렉터리 표기만 정규화했으며 SHA와 실제 의미/예외는 유지했다. **전체 suite는 green이 아니다.** class setup 실패로 실행되지 못한 하위 테스트는 통과로 세지 않았다.

초기 실험의 중단, criterion 추출 오류, 누락 import와 새 순서 테스트의 과도한 provenance 순서 assertion은 별도 증거로 보존했고 최종 통과 수에 합산하지 않았다. runtime 코드와 입력 freeze를 확정한 뒤 최종 matching worker로 검증했다.

격리 runtime generation: `39c3674efbfb5d1281475bcd3c0ce1b0bccb96e167adb1c7a8cdfd94066cf771`. Source fingerprint: `0c915cc5dfee5d9222987668718de52c10ccd2df12404df62cd2139ea6c1cb20`. 코드 SHA-256: `3b92de145b0b2f40688e2042ffd0d20a3b0e20c8bf72ed1a5dae9e40cdd5f439`. 원본 main HEAD·Git index·기존 dirty 22개 파일·default CURRENT는 보존됐다. 수정은 `codex/slot-retrieval-stage06-fusion-cap` worktree에 미커밋 상태로 보관했으며 원격 push와 primary runtime 반영은 수행하지 않았다.

## 증거

`PLAN.md`, `INPUTS-FROZEN.json`, `CRITERIA-FROZEN.json`, `before-ties-trace-metrics.json`, `before-ties-traces/`, `owned-alias-ablation.json`, `DECISION.json`, `QUALIFIED-KERNEL-VALIDATION.json`, `PUBLIC-VALIDATION.json`, `qualified-native/`, `qualified-natural/`, `FOCUSED-VALIDATION.json`, `qualified-full-tests.json`, `BASELINE-FAILED-SELECTOR-REPLAY.json`, `FULL-FAILURE-CLASSIFICATION.json`, `MISSING-ACTIVE-SHARDS.json`, `PROBE-SOURCE-DIFFERENCE.json`, `RESIDUAL-SUBJECT-CAUSES.json`, `ASSET-PRESERVATION.json`, `qualified-inventory/inventory.json`, `PRESERVATION-FINAL.json`, `REVIEWED-SCOPE.json`.

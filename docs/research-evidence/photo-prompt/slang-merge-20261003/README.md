Pull 후 원격의 꿈 경계 비교 증거 보강과 로컬의 은어 대체 표현 보강을 함께 보존했습니다. `main`은 `bcb671ba488a31f4e84e5e0d8b0a740e4dd9c706`까지 fast-forward한 뒤 이 작업의 저장된 변경을 다시 적용했습니다. 충돌은 generated visual index 한 곳에서 발생했고, 통합 authored data와 양쪽의 호환 벡터로 visual·semantic index 및 BM25F를 다시 생성하여 해결했습니다.

원격의 `oneiric_dream_logic_discontinuity` 변경은 물체·패턴·문턱 비교 증거의 대체 표현과 gate 설명을 유지합니다. 로컬의 `composite_overwhelmed_expression`, `soft_full_figure_volume`, `bust_prominence_relation` 수정과 신규 12개 관찰 관계, 기존 owner 대체 표현, guard·property scope를 유지합니다. 같은 profile에서 양쪽이 의미를 덮어쓰는 충돌은 없었습니다. [양쪽 보존 증거](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/PRESERVATION.json)에 profile별 부모 일치와 나머지 source byte 보존을 기록했습니다.

검증 결과는 **154개 모듈 / 1,336개 테스트 PASS**, failure·error·skip 0입니다. 실제 발견한 테스트 ID를 모두 한 번씩 실행했고, 각 모듈의 시작·종료 source hash와 커밋할 별도 Git index가 일치합니다. Dictionary validator와 visual index check도 통과했습니다. [검증 요약](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/VERIFICATION.json)과 [전체 모듈 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/full-suite/FULL-SUITE-RESULT.json)를 보존했습니다.

시각 의미 profile 1,576개, semantic index 9,831개를 다시 생성했습니다. 같은 텍스트·provider·model·차원의 캐시만 재사용했고, 양쪽에 있는 동일 텍스트의 vector는 값이 같은지 검사했습니다. 추가 embedding 호출과 이미지 호출은 **0회**입니다. [인덱스 재생성 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/INDEX-RECONCILIATION.json)에 모든 row의 벡터 출처를 기록했습니다. 사용하지 않는 과거 index generation을 삭제하지 않았습니다.

세 arm의 원래 네 authored 입력과 seed로 후보팩을 재조회했습니다. 얼굴·양손 V, 지지된 M형과 전신 양감, 하트 동공·배꼽 기준 피부 문양·선 topology 후보가 모두 노출됩니다. 재조회는 후보 노출 확인이며 과거 이미지의 채택이나 품질 판정을 소급 변경하지 않습니다. 기존 V8 경계의 candidate pack은 **전체 byte가 동일**하고, V1–V7 기록과 frozen routing fixture·네 입력은 그대로 유지합니다. [재조회 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/RETRIEVAL.json)을 별도로 저장했습니다.

기존 native 이미지 5장, 프롬프트, core·참조·audit hash는 모두 동일합니다. 장면별 최종 픽셀 판정 **1 PASS / 2 FAIL**과 사용자 수용 미수신도 그대로입니다. [통합·이미지 연구 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-integration-20261003/README.md)는 당시의 receipt를 보존합니다. 전체 native-source archive는 로컬에 유지하며, 그 manifest·hash·native 원본과 감사 기록은 추적합니다.

관계없는 연구와 이전 index generation의 **204개 파일**은 병합 당시 byte가 같았고 커밋 범위에 포함하지 않습니다. 이후 같은 작업 폴더에서 그중 6개 연구 snapshot 파일도 바뀌었으며, 현재 바이트를 수정하거나 되돌리지 않았습니다. 관찰 hash는 검증 요약에 따로 기록합니다. 복구용 scoped stash는 출판 검증이 끝날 때까지 유지합니다. 새 자료의 source snapshot과 병합 증거는 원래 이미지 검증과 구분합니다.

전체 테스트가 끝난 뒤 같은 작업 폴더의 다른 연구가 source 9개를 변경했습니다. 이번 작업과 겹치는 main registry·body registry·generator는 테스트한 바이트를 별도 Git index에 고정했고, 다른 변경은 커밋 범위에서 제외했습니다. 동시 작업의 현재 source 바이트는 수정하지 않았습니다. [분리·보존 기록](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slang-merge-20261003/CONCURRENT-WORKTREE.json)에 발견 당시의 경로·hash와 검증 경계를 기록했습니다.

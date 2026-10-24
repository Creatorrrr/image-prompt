# 초현실 데이터와 이미지 시험 main 통합

초현실 제어의 관측 가능한 관계·혼동 경계·출처를 데이터에 반영하고, 최초 시험 3장과 surreal=3 시험 3장의 원본·입력·판정을 보존한다. 이미지의 주제 가시성, 장면의 완전한 구현, 후보 원문 전체의 native 자격과 사용자 수용은 각각 별도 판단이다.

## 변경 범위

- 새 완성 관계 19개, 긍정 검색 제외 진단 16개, 선택형 연결 38개, 기전 12개, 발견 경로 26개를 추가한다. C07은 보류한다.
- 재사용 source 6개 중 main에 없던 2개를 연구 당시 스냅샷과 같은 원문·조건·효과·출처로 보존하고, 그 4개 기존 연결을 함께 싣는다. 새로 저술한 변형으로 계산하지 않는다.
- main에 없는 비교 대상 3개는 채택 후보가 아니다. 2개 신규 기록의 연구 메타데이터에서 해당 항목을 활성 native 참조와 분리하고, 전체 원문이 보존된 decision-source snapshot의 역사적 출처로 연결한다. 긍정 한영 본문·조건·효과·출처·새 38개 연결은 바꾸지 않는다.
- 이전 main의 22,672개 후보와 17,488개 연결, catalog와 policies는 모두 그대로 보존한다. 최종 source는 후보 22,709개, 긍정 21,144개, 연결 17,530개다.
- 다른 작업의 dirty SKILL/실행 코드와 source 변경을 끼워 넣지 않는다. 기존 설치 H-F2 runtime과 전역 저장 control 설정을 변경하지 않는다.

## 검증

기준 main은 `e652bc786383837014c8bc4bd5ee2e7f76209487`, 최초 범위 커밋은 `77912a85d`다. 먼저 이 작업을 커밋한 다음 `git pull --no-rebase --no-edit origin main`을 실행했고, 추가 원격 변경은 없었다. 보호된 기본 체크아웃의 파일 bytes와 staging은 이 통합 중 건드리지 않는다.

전체 합집합에서 인덱스 `cdb13af2bc1e601051084c6d888b982ac07dd03a18b0e228db3666c67cdf02ce`를 다시 만들었다. 기존 호환 벡터 21,123개를 재사용하고 21개를 고정된 로컬 embeddinggemma-2로 계산했다. 외부 유료 embedding 호출은 없다. 원문·문서 recipe·모델 공간·전체 shard checksum 검증을 통과했다.

관련 source 회귀 테스트 57개와 하위 테스트 11개가 통과했다. 최종 dictionary 검사와 source 보존 검사 결과는 아래 증거 파일에 있다. 원래 연구 보고서의 Markdown hard-line-break 공백은 원본 hash 보존을 위해 유지했다.

초기 게시 준비에서 과거 비교 ID 3개 때문에 native closure 검사가 실패한 기록, pytest가 없는 embedding 전용 Python을 잘못 선택한 기록, 중단된 인덱스 writer의 pending 기록은 지우지 않았다. 실제 검증용 venv로 테스트를 실행했고, 과거 비교 참조를 올바른 출처로 분리한 다음 기존 pending revision의 같은 소유권으로 build·전체 검증·완료 절차를 마쳤다. 검사 기준이나 validator를 완화하지 않았다.

## 영구 이미지 시험 증거

각 항목에는 이미지, 실제 runtime prompt, 생성 전 testcase, pixel 결과, manifest, ledger row, controls·native plan·compose/runtime/review 감사가 있다. 아래 경로는 이 커밋에 포함되므로 작업 캐시나 워크트리가 없어져도 보존된다.

| 실행 | surreal | 컨셉 | 엄격한 장면 판정 | 영구 결과 |
|---|---:|---|---|---|
| 최초 A | 0 | 대리석 커튼 | FAIL: 손가락을 감싸는 말림 부족 | [이미지](image-test-evidence/initial-a/image.png) · [프롬프트](image-test-evidence/initial-a/prompt.txt) · [판정](image-test-evidence/initial-a/pixel-result.json) |
| 최초 B2 | 0 | 실제 자세와 어긋난 연결 그림자 | PASS | [이미지](image-test-evidence/initial-b2/image.png) · [프롬프트](image-test-evidence/initial-b2/prompt.txt) · [판정](image-test-evidence/initial-b2/pixel-result.json) |
| 최초 C | 0 | 세탁기 내부의 바다 | FAIL: 열린 문테 대신 고정 입구 접촉 | [이미지](image-test-evidence/initial-c/image.png) · [프롬프트](image-test-evidence/initial-c/prompt.txt) · [판정](image-test-evidence/initial-c/pixel-result.json) |
| 3 A | 3 | 수직 조수 경계 | FAIL: 수평·수직 수면의 연속 90도 경계 부족 | [이미지](image-test-evidence/surreal3-a/image.png) · [프롬프트](image-test-evidence/surreal3-a/prompt.txt) · [판정](image-test-evidence/surreal3-a/pixel-result.json) |
| 3 B | 3 | 천장에 거꾸로 선 인물 | PASS | [이미지](image-test-evidence/surreal3-b/image.png) · [프롬프트](image-test-evidence/surreal3-b/prompt.txt) · [판정](image-test-evidence/surreal3-b/pixel-result.json) |
| 3 C | 3 | 성냥갑 기관차 | FAIL: 동일 기관차·두 레일 전체 연속 부족 | [이미지](image-test-evidence/surreal3-c/image.png) · [프롬프트](image-test-evidence/surreal3-c/prompt.txt) · [판정](image-test-evidence/surreal3-c/pixel-result.json) |

초기 세 장은 명시 초현실 주제를 유지한 surreal=0 실행이다. 새 세 장은 실제 surreal=3 snapshot으로 생성했고, 초현실 주도성은 3/3, 엄격한 장면 판정은 1/3이다. 두 시험은 장면과 프롬프트가 달라 0→3의 효과 크기를 추정하는 통제 A/B가 아니다. 총 실제 이미지 호출은 6회이며 이번 게시 과정에는 새 이미지 호출이 없다. 사용자 수용은 pending이고, 신규 완성 후보 전체 의미의 native 픽셀 자격은 NOT_TESTED다.

## 증거와 정리 범위

- [source 합집합 보존](publication-evidence/source-union-validation.json)
- [과거 비교 참조 분리](publication-evidence/historical-reference-resolution.json)
- [기존 재사용 source의 원문 보존](publication-evidence/reused-source-preservation.json)
- [전체 native index](publication-evidence/native-index-build.json)
- [dictionary 검사](publication-evidence/dictionary-validation.json)
- [source 회귀 테스트](publication-evidence/source-tests-final.log)
- [중단 revision 복구·완료](publication-evidence/index-revision-recovery.json)
- [6개 영구 이미지 hash와 ledger ID](publication-evidence/publication-bundles.json)

푸시 후 원격 main과 로컬 통합 commit의 동일성을 확인한 뒤 전용 워크트리, 이 작업의 별도 build/model/store 복사본과 검증된 중복 이미지 캐시를 정리한다. 원본 참조 사진, 위 영구 연구·이미지 증거, 기존 활성 공유 runtime과 다른 작업의 파일은 보존한다. 최종 원격 SHA와 사후 보호 hash·정리 결과는 로컬 게시 영수증에 기록한다.

# 독립 입력 대조와 전체 발견 테스트 후속 검증

이 게시물은 DATA 수정 cycle을 추가하지 않습니다. 새 이미지나 임베딩 호출도 없습니다.

## 1. 고정 `120f07d0`의 전체 발견 테스트

2026-10-03 09:16:14–10:22:54 UTC에 별도 snapshot에서 149개 모듈, 발견된 1,302개 테스트 ID를 모두 실행했습니다.

- 성공한 테스트 메서드 1,297개
- 성공하지 못한 메서드 5개: 과거와 정확히 같은 누락 이미지/참조 파일 때문에 발생한 10개 assertion/subtest 실패와 1개 파일 오류
- skip·중복·재시작·새 실패·변경된 정규화 traceback 0개
- 과거 1,284개 ID 모두 유지, 새로 추가된 18개 메서드 모두 통과
- 실행 시작/끝의 snapshot HEAD·운영 소스가 같고 종료 시 작업 트리도 깨끗함

따라서 전체 suite가 green이라고 부르지 않습니다. 또한 이 실행은 이후 종교 도상 합류, oneiric DATA 및 별도의 다음 런타임 개발을 검증하지 않습니다. 고정 commit은 `120f07d025340bd067097f947ca23d4dd828e7cf`입니다.

별도 `31dbed9f` 파일 존재 검사에서는 같은 8개 고유 누락 경로가 현재 checkout에도 없었고, makeup core의 필요한 5개 glob 결과도 0개였습니다. 관련 테스트 4개·manifest 4개는 동일했습니다. 이는 파일 가용성 확인일 뿐 현재 main 전체 suite를 실행한 결과가 아닙니다.

## 2. 후보 자료를 보지 않은 새 입력 8개의 대조

초기 작성자는 저장소 후보·프로필·기존 검사 결과·수정 내용을 보지 않고 사람·물건·비인간 생명체·환경 각 2개씩, 총 8개 합성 요청과 초기 장면을 작성하고 hash로 동결했습니다. 실제 사용자 요청이나 인간이 작성한 표본은 아닙니다. project taxonomy/schema bookkeeping은 초기 문장 작성 뒤 다른 단계에서 수행했으므로 전체 pre-core 절차 준수나 실사용 성능이라고 주장하지 않습니다.

코드와 독립 upstream 데이터를 같게 둔 두 arm을 만들었습니다. 기준은 `31dbed9f0d22af97025cebcbceffc07b4250de35`이고, counterfactual은 DATA25–29의 정확한 다섯 프로필 수정만 제거했습니다. 그 다섯 레코드 및 필요한 두 옛 벡터는 `5bf8142304f484138474fff4af9b0660439fa331`에서 가져와 정확한 입력 텍스트로 검증했습니다. 다른 1,559개 프로필, 런타임/pre-core 27개 파일, 독립 종교 도상 자료는 동일합니다. 양쪽 1,564개 프로필/9,819개 일반 항목의 metadata·BM25F·벡터 결합도 검증했습니다.

결과는 다음처럼 분모 8개를 그대로 유지합니다.

- 4개는 양쪽에서 정상 후보팩 생성: 총 8회 실행. 전체 팩 바이트·모든 후보 ID/순서/적합성·core·필수 의무가 모두 동일
- 동일한 초기 문장을 유지하고 optional 채택을 0개로 둔 전체 구성 감사는 4개 모두 양쪽에서 통과
- 다른 4개는 원래 영어 문장의 blanket-negative 표현 검사에서 양쪽 모두 동일하게 거부됨. `not required`라는 선택적 비요구, 혼잡을 피하라는 지시, 실제 빈 장면 표현을 구분해 기록했으며 문장을 고쳐 통과시키거나 이를 사용자 배제로 바꾸지 않았음
- 실행 가능한 4개에서 다섯 수정 프로필은 hard 의무나 optional visual 후보로 나타나지 않음

따라서 여기서는 DATA25–29의 효과를 관찰하지 못했습니다. 제한된 부수 회귀 안정성 증거이며, 일반 검색 정확도 향상·8개 전부 성공·픽셀 품질 또는 전체 작성 workflow의 성공으로 해석하면 안 됩니다. 거부된 4개는 이 불변 fixture의 사전 조건 실패이며, 그 자연어 요청 자체를 제품이 처리할 수 없다는 증거도 아닙니다.

원래 요청/장면, envelope, 314개 metadata 파일 및 arm hash가 유지됩니다. 원문·기능선택 bookkeeping의 초안 오류와 metadata-only 수정 이력도 보존했습니다. 이미지 생성·외부 검색 임베딩 호출은 없습니다.

## 3. 독립 upstream 종교 도상 54개는 KEEP

새로 합류한 54개 프로필에 대해 실제 materializer로 157개 작성된 의무의 보존을 확인했습니다. 정규 binding 157개가 검증되고, 구성요소를 하나씩 뺀 157개 대조는 거부되며, 완전한 정확 경로 54개는 각자 의도한 대상만 해결합니다. 더 일반적인 종교 지식을 핑계로 선택된 도상 변형을 넓히지 않았습니다. 안전한 수정 leaf가 없어 모두 유지했습니다.

이 54개는 다른 작업에서 추가한 자료이며 이번 loop의 새 행·cycle·비용으로 세지 않습니다. 일부 원문은 excerpt-only 출처 한계가 있고 이 검사는 curatorial text 수준입니다. 원래 별도 이미지 검증의 엄격한 실패 판정을 통과로 바꾸지 않았습니다.

## 자료와 재현

코드·원문 snapshot 전체 복사는 중복 배포하지 않습니다. 위 고정 git commit과 arm 준비 script/파일 manifest로 재구성할 수 있습니다. 실행 당시 원본 hash와 공개 파일 hash는 구분합니다. 공개 자료는 로컬 경로를 `REPOSITORY_ROOT`, `EVIDENCE_ROOT`, `WORKSPACE_ROOT`, `EXTERNAL_HOME`, `EXECUTOR_HOME`로 정규화했으며 각 압축의 `publication-manifest.json`이 공개 바이트를 검증합니다. 실행 script의 이 경로들은 재현 환경에 맞게 지정해야 합니다.

- `full-regression-evidence.tar.gz`: 전체 ID 대조·모듈 결과·과거 실패 비교·라이브 파일 존재 검사
- `fresh-holdout-evidence.tar.gz`: 독립 초기 입력·schema 사전검사·두 arm 구성 증거·원시 팩·전체 leaf/순서/적합성 비교
- `religion-keep-evidence.tar.gz`: 원문/consumer 보존 및 의무 생략 대조

공개 압축 SHA-256:
- full-regression-evidence.tar.gz: `5631e894b307e87eeb3cb8a28144694ec81d5e24d915932837a4576bac80f191`
- fresh-holdout-evidence.tar.gz: `61c1d90fd9660a1197563730d303908c281efb9c76fcfbc2b6c5b249c0e962b4`
- religion-keep-evidence.tar.gz: `a5bb1296dc40acc2a494f5919ce0fe882e7a95c260f2d6a97165f5e9dd29f0a4`

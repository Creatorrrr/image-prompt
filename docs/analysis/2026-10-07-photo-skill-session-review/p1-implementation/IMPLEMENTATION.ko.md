# P1 구현 기록

단계 실행 도구와 재시도 허용 정보 추출을 구현하고 주 작업공간에 반영했다. 구현·회귀 검증 기준은 main의 `4f3d524ed035de8592e4b0c6ad5030b41ffc55af`이다. 연결된 별도 작업트리에서 검증한 뒤 파일을 선택적으로 복사했다. 작성 DATA와 다른 작업의 테스트·산출물은 최초 바이트를 보존했다.

## 변경

- **중립 초기 도구**: `precore/prepare_photo_run.py`의 init·controls·canonicalize·freeze로 원문, 명시적 구간, 설정과 작성 입력의 해시·ID를 연결한다. UTF-8/CRLF와 Unicode 문자 위치를 보존한다. 작성자가 작성한 core·범주 선택·신체·camera 검토를 검증한 뒤 동결하며, 판단이 비었거나 이미 제공된 binding이 틀리면 거부한다.
- **공유 검증**: 기존 순수 normalizer 12개를 `photo_authoring_wire.py`로 옮겼다. 함수 AST 12개가 기준 커밋과 동일하며 기존 생성기가 같은 구현에 위임한다. neutral catalog·신체·camera 검증도 공유한다.
- **단계 관리**: `scripts/photo_workflow.py`의 --run으로 조회·뷰·구성 감사·렌더 준비·실행·리뷰·상태·복구를 연결한다. immutable revision, 파일 SHA, freeze receipt와 정확한 runtime receipt를 사용한다. 첫 조회의 seed/policy와 pack/receipt 쌍을 보존하고, 불완전한 쌍을 새 pack으로 자동 대체하지 않는다.
- **실행 기록**: P0 API adapter를 재사용한다. 호출 전에 operation·timestamp·run ID를 저장하고 transient 호출도 예산에 센다. generic repair와 부모 retry의 상한을 적용한다. 레저는 lock·atomic replacement·동일 행 중복 방지·identity conflict 검사로 기존 바이트를 보존한다. 실제 호출 여부가 불확실하면 재호출하지 않는다.
- **native 연결**: 감사된 plan·start·관측 결과를 도구 환경의 bridge로 연결한다. 기록 시 plan과 원본 네 입력을 다시 감사한다. concrete file 없이 preview만 있으면 preview_only로 남긴다. 제공자 차단·unknown·저장·기록 실패, 기술 판정과 사용자 선호를 구분한다.
- **재시도 추출**: coordinator가 실제 부모·레저·리뷰·이미지·세대를 검증하고, 닫힌 허용 필드와 source pointer/SHA만 전달한다. 후보 목록, 미채택 prose, 이전 범주와 raw error는 출력하지 않는다. child 동결과 실행 전 부모 proof를 다시 검증한다. 수작업으로 저장한 v6 부모는 원본 manifest와 호환 immutable worker를 사용해 가져올 수 있다.
- **스킬 안내**: SKILL에 정확한 중립 파일과 좁은 retry 실행 예외를 명시했다. 상세 사용·복구·리뷰·부모 manifest 안내는 [photo-workflow.md](../../../../skills/photo-prompt-image-generator/references/photo-workflow.md)에 두었다. 독립 장면 작성, 초기 5~10 범주 선택, 의미·신체·공간·픽셀·사용자 판단은 계속 작성자가 수행한다.

## 검증 결과

신규 중립·상태·범위 테스트 18개와 감사기·native 파일 기록·부모 추출·child 동결·API journal을 확인한 offline 통합 테스트 8개가 통과했다. 통합 테스트에서 실제 composed/runtime 감사와 파일·프로세스 경계는 유지했다. API 제공자 응답과 native 파일은 유지보수 fixture다. 실제 이미지·embedding 호출은 0회다.

함수 AST 동등성 12/12, 스킬 구조·링크, dictionary validation, native bridge JavaScript 구문, whitespace 검사와 matching runtime publication도 통과했다. 검증한 generation은 `956332d237a7e24770080e93134feb26d03b4886f91a5858975d16d6f83e9432`다. 이 publication은 별도 작업트리의 main DATA와 구현 코드에 대한 증거이며, 주 작업공간의 다른 미커밋 DATA에 대한 별도 렌더 증명은 아니다.

[소스 동결](SOURCE_FREEZE.json), [normalizer 비교](NORMALIZER_EQUIVALENCE.json), [중립 검증](NEUTRAL_TESTS.log), [통합 검증](RUNTIME_TESTS.log), [runtime 게시](RUNTIME_PUBLICATION.json)에 근거를 남겼다.

## 전체 회귀

최종 소스 57개를 고정하고 전체 unittest discovery를 실행했다. 먼저 통과한 serial 항목 76개는 재사용하고 나머지를 네 프로세스의 독립 runtime store로 분리했다.

| 항목 | 결과 |
|---|---:|
| discovery 고유 항목 | 1,894 |
| 실행 기록: 테스트·수정된 import 항목 | 1,810 |
| 통과 메서드 | 1,773 |
| 실패 메서드 | 21 |
| 실패 assertion 항목: subtest 포함 | 37 |
| 오류 메서드: import 포함 | 16 |
| class setup 오류 | 9 |
| setup 오류 때문에 실행되지 못한 메서드 | 84 |
| 신규 테스트 통과 | 26/26 |
| 실패·오류 항목의 main 재현 | 62/62 |
| 새 회귀로 확인된 항목 | 0 |
| 검증 중 소스 변경 | 0 |

전체 suite가 통과한 상태는 아니다. 역사 fixture의 파일·이미지 누락, immutable SHA와 현재 자료의 차이, 이미 반영된 DATA와 과거 기대값의 차이가 구현 전 main에서도 재현됐다. 집합 순서와 처음 검출되는 역사 파일이 달라진 사례는 현재·main 양쪽을 `PYTHONHASHSEED=0`으로 실행해 같은 traceback을 확인했다. 비교에서는 작업공간 경로 접두사만 정규화했다. 역사 SHA 검사나 기대값은 수정하지 않았다.

Discovery의 `_FailedTest` ID 12개를 그대로 `loadTestsFromNames`에 전달하면 runner 자체의 AttributeError가 생겼다. 해당 placeholder 오류를 집계에서 제외하고 실제 12개 모듈을 현재·main에서 다시 import했다. 실제 import 오류 12개도 같은 main traceback으로 확인했다.

[전체 결과](FULL_REGRESSION.json), [전체 로그](FULL_REGRESSION.log), [main 대조](BASELINE_COMPARISON.json), [main 재현 로그](BASELINE_REPLAYS.log), [고정 hash seed 재현](CONTROLLED_CURRENT_REPLAYS.log), [import 재현](BASELINE_IMPORTS.log)에 기록했다. 역사 오류는 해당 84개 메서드와 12개 모듈의 회귀 검증 범위를 제한한다. 유지보수 검증은 렌더 픽셀·예술적 개선·실제 사용자 수락의 증명이 아니다.

## 수작업 감소 확인

고정된 camera-authoring maintenance fixture를 사용해 기존 CLI와 실행 도구를 비교했다. 같은 작성 core·controls·baseline이 유지됐으며, 새 도구 입력에서는 파생 SHA·ID를 직접 계산하거나 복사하지 않았다. 독립 장면·범주 선택·리뷰는 fixture의 작성 값을 그대로 사용했다.

| 경로 전달 지표 | 기존 CLI | 단계 도구 |
|---|---:|---:|
| 조회 입출력 경로 | 6 | --run 1 |
| 구성 감사 입력 경로 | 3 | --run + 작성 composed 2 |

공통 seed·source policy·runtime store 옵션은 위 경로 수에서 제외했다. composed의 여섯 binding 필드와 초기 입력·transport binding을 생략해도 도구가 연결하고 실제 감사기를 통과했다. 작성 SHA/ID 수는 새 경로에서 0개다. 재시도 작성자는 closed context와 projection audit만 읽으며, 부모 전체 파일은 coordinator가 검증한다.

구성 변조는 실제 감사에서 실패했고, 동결 파일 한 바이트 변경은 다음 단계에서 `stale_artifact`로 거부됐다. recorder crash fixture는 provider 호출 1회 뒤 저장된 recorder 인자를 두 번 재사용해 ledger row 1개를 유지했고 추가 이미지 호출은 0회였다.

실행 시간을 함께 기록했다. 조회는 기존 CLI 29.477초, 단계 도구 34.932초였고, 구성 감사는 각각 20.725초·21.899초였다. 정상 렌더 준비 37.859초, 구성 변조 감사 20.607초, stale 검출 0.002초, recorder crash/replay fixture 46.118초였다. 한 사례이며 cache·순서와 검증 범위가 달라 성능 개선율로 해석하지 않는다. 인간의 작성 시간·수정 왕복 시간은 측정하지 않았다. [측정값](USABILITY_MEASUREMENT.json)과 [측정 코드](USABILITY_MEASUREMENT.py)에 정확한 명령·조건을 보관했다.

## 지원 경계

- v2로 표현할 수 없는 모두-보존 국소 scope는 projection에 `scope_not_representable_in_lineage_v2`를 표시하고 실행을 거부한다. 차원을 임의로 열지 않는다.
- 호환 Python/generation이나 알려진 projection 구조가 없으면 코드로 중단한다.
- 실제 호출이 불확실하면 관측 근거로 조정하기 전까지 예산을 보수적으로 유지한다. 외부 제공자의 exactly-once를 보장하지 않는다.
- scope·원인·리뷰는 작성자의 실제 판단이다. 구조·바이트 감사가 의미나 픽셀을 대신 판정하지 않는다.

## 반영·보존

주 작업공간에 구현과 문서·테스트·검증 근거를 선택적으로 반영했다. 코드와 소스 57개의 SHA가 검증한 작업트리와 일치한다. 기존 tracked 변경 15개, untracked 4,011개 파일·4,276,152,706바이트의 해시가 최초 기록과 일치하고 누락은 0개다. Git HEAD와 index도 그대로다. [보존 검사](PRIMARY_PRESERVATION.json), [최초 반영 검사](INITIAL_APPLICATION.json), [최종 파일 목록](SCOPED_FILES.json)에 기록했다.

main 대조용 임시 작업트리는 깨끗한 기준 HEAD를 확인한 뒤 복구 가능한 archive로 정리했다. 구현 작업트리는 검토용으로 남겼다. 작업 변경은 커밋·푸시·PR 게시하지 않았다.

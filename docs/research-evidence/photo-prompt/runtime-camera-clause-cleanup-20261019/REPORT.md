# 카메라 레거시 모듈·import 187행 정리 결과

2026-10-19 · 작업 소스만 정리 · H 단독+F2·과거 실행·기존 작업·CURRENT 보존

**카메라 구문 모듈 1개와 사용하지 않는 import 2개를 제거했다. 소스 변경은
추가 0행·삭제 187행이며, 작업 소스의 Python 파일 수는 77개에서 76개가 됐다.**
설치된 H 단독+F2와 과거 실행의 봉인 소스는 그대로 유지했다.
검색 정책·후보 데이터·모델·설치 선택과 운영 CURRENT는 변경하지 않았다.
원래 root native CURRENT의 코드 74개와 작업 소스 77개 사이의 기존 차이는
별도 범위다. 이번 작업 소스는 76개이며 원래 CURRENT와 지문 보호는 유지했다.

## 실제 범위

| 대상 | 처리 | 삭제 행수 |
|---|---|---:|
| `scripts/photo_camera_clauses.py` | 구문 분석 모듈 전체 제거 | 185 |
| `scripts/photo_camera_evidence.py`의 `import re` | 미사용 import 제거 | 1 |
| 같은 파일의 `from photo_camera_clauses import bounded_camera_clauses` | 미사용 import 제거 | 1 |
| 합계 | 작업 소스 2경로 | 187 |

경로는 `skills/photo-prompt-image-generator/` 기준이다. 직전 제거한
`legacy_camera_clauses`만 사용하던 구문 모듈과 두 import다. 현재 source/test의
실제 호출은 없고, 남은 import 이름도 사용하지 않았다. module 안의 함수 6개와
내부 상수는 함께 제거했으며 남은 importer의 AST는 두 import를 제외하면 같다.
현재 카메라 선언·질의·요구 증거는 원래 `precore/photo_camera_authoring.py`가 제공한다.
다른 코드 정리나 인접 공백·포맷 변경을 확대하지 않았다.

원래 미커밋 파일 안의 14함수·580행, 수동 원본 검증 계약인
`validate_visual_profile_source` 8행은 이번 범위에서 제외했다. bytecode 21개,
root shard 5세대, provider와 activation/rollback 도구도 그대로다.

## 검증 후 적용

원본과 독립된 control/combined/operating 임시 프로젝트를 만들었다. assets와
모델은 독립적인 APFS 복사본이고 원본 hardlink는 사용하지 않았다. 변경 patch를
private에서 역적용해 원래 두 파일의 bytes가 정확히 복원됨을 확인한 뒤 다시
적용했다. 실제 원본은 아래 적용 전 게이트가 모두 통과한 뒤에만 수정했다.

| 검증 | 결과 | 근거 |
|---|---|---|
| 수정 작업 소스 operating | 48개 통과, skip 0 | `SOURCE-operating.json` |
| 수정 작업 소스 native | 70개 통과, skip 0 | `SOURCE-native.json` |
| 카메라 계약 대조 | control/제거본/실제 적용본에서 각각 10개, 동일한 성공·거부 동작 | `SOURCE-SMOKE-*.json` |
| 실제 소스 로드 | 제거본 경로·SHA, 모듈/두 export 부재, 구현 코드 76개 확인 | 위 SOURCE 결과 |
| 지문 보호 | 현재 구현 일치 허용·다른 구현 거부 유지 | SOURCE와 SMOKE 결과 |
| 설치된 H+F2 커널 | 기존 2목표의 전체 raw BM25F/cosine 배열과 CID 순서가 원래 issued 결과와 일치 | `INSTALLED.json` |
| 일반 H+F2 CLI | control/제거본/실제 적용 후 5명령씩, 합계 15명령 통과 | `MANAGED-*.json` |
| H+F2 검색 결과 | top8·전체 순서/점수 digest·목표 정보가 원래 결과와 일치 | 위 MANAGED 결과 |
| 원래 봉인 run 감사 | 1건, 코드 94개/전체 863멤버 검사와 원래 receipt·구성 감사 통과 | `HISTORY-frozen.json` |
| source/실험 archive | 과거 225+최근 225=450 저장 순서 및 전용 17검사 통과 | `HISTORY-archive.json` |
| 공개 native 조회 | 파생 private fixture에서 control/제거본/실제 적용본 출력 일치 | `HISTORY-native-view*.json` |
| 누락·변조 거부 | missing run/issued receipt, receipt checksum, generation 변조의 4종 거부 유지 | `HISTORY-negative.json` |
| 전체 보존 | 보호 경로 139,236개 및 CURRENT 168개 대조 통과 | `VERIFY-FINAL.json` |

회귀 검사는 설치된 원래 코드로 대신하지 않았다. 실제 수정된 작업 소스의 모듈
경로·SHA를 기록했고 원래 scripts/precore 읽기를 OS sandbox로 차단했다.
기존 미커밋 작업이 포함된 작업 소스를 복사해 118개 회귀를 실행했다. 별도의
깨끗한 HEAD checkout에서 전체 suite를 추가 실행한 결과는 아니다. 대신 HEAD의
Python 소스 77개에서도 해당 구문 함수의 남은 호출이 없음을 정적 확인했다
(`COMMITTED-SOURCE-BOUNDARY.json`).
테스트가 별도 임시 store/CURRENT를 만들고 발행·고정하는 동작은 허용했으나,
원래 프로젝트·다른 worktree·공유 runtime에는 쓸 수 없게 했다.
stdout에 기존 테스트 기록이 섞이는 경우 마지막 runner JSON과 worker exit,
실제 테스트 수·skip 수를 확인했다. 실패를 PASS로 재분류하거나 검사를 생략하지 않았다.

실제 적용 후의 source smoke는 원래 bytecode/확장 모듈 읽기도 차단했다.
적용한 source SHA가 통과한 private 복사본과 정확히 같아 118개 suite는 다시
실행하지 않았고, 실제 소스 로드·카메라 계약·일반 CLI·native view를 재확인했다.
원래 동작을 유지하기 위한 호환 stub이나 source 지문 예외는 추가하지 않았다.

검색은 원래 공통 풀 18,180 CID/18,182 RID 전체와 H 질의·F2를 유지한다.
각 목표에서 BM25F 1회·로컬 cosine 1회이며 기존 query vector/cache를 재사용했다.
Gemini·새 모델 추론·이미지 요청·새 의미 판정은 0회다.
원래 설치본의 코드 집합 hash와 H/native 세대 ID도 그대로다.

native 공개 조회는 기존 issued pack을 사용하는 private workflow에서 H binding을
제거해 공개 native 분기를 비교한 것이다. 별도의 원래 역사 run을 추가 발굴해
재현한 것으로 세지 않았다. 실제 원래 run 감사 범위는 1건이다.
archive의 기존 품질 HOLD도 그대로이며, 정리 검증 PASS가 검색 품질 개선을 뜻하지 않는다.
원래 store가 없는 41건과 대체 manifest 7개를 보존했고 이들을 재현 성공에 포함하지 않았다.

## 보존과 커밋 경계

원래 보호 139,236경로 중 이번 두 source의 정확한 승인 결과만 변경을 허용했다.
그 밖의 bytes·권한·inode·링크, CURRENT 전체 재고와 원문, 설치 선택·모델 lock·
봉인 세대·receipt/기존 run, 원래 main 변경/미추적 40,518경로와 다른 worktree
6,161경로를 보존했다. 다른 worktree의 HEAD/index와 원래 staging도 유지했다.
이전 분석 디렉터리 19파일 역시 기존 작업으로 보호했으며 함께 커밋하지 않았다.

`BASELINE-DELTA.json.gz`는 기존 분석 보호 목록에 19경로를 더한다. 원래 protection을
덮어쓰지 않았고 `AFTER-DELTA.json.gz`에는 이번 두 source의 before/after stamp만
별도로 기록했다. 실제 적용은 `APPLICATION.json`, 최종 게이트와 적용 후 결과는
`RESULT.json`을 따른다. application의 최초 상태는 적용 직후 후속 검증 대기 상태다.
최종 PASS 여부는 RESULT와 최종 보존 검사로 확정한다.

이번 작업에 해당하는 source 2경로, 새 유지보수 helper 1개와 이 증거 디렉터리만
명시적으로 stage해 커밋했다. 원래 미커밋 작업은 stage하지 않았다. 커밋 이후
보존과 커밋 범위를 다시 확인했으며 push·설치·운영 세대 발행·CURRENT 전환은 하지 않았다.

## 복원과 재현

원문은 시작 commit `2ab64d5a3e0bb0808edbaf163ab9c79b6189e361`과 TARGETS의
SHA로 식별된다. `PATCH.patch.gz`는 원문 patch의 무손실 gzip이며 역적용은 private에서
검증했다. 복원 전에는 현재 상태와 역적용 가능성을 확인하고 이번 patch만 되돌린다.
전체 파일 checkout/reset으로 나중의 작업을 덮어쓰지 않는다.

검증 helper는 `tools/photo_runtime_maintenance/camera_cleanup.py`다. 완료한
prepare/apply는 반복 실행을 거부한다. native/operating의 전체 원시 stdout/stderr는
결과 JSON에 보존했다. progress와 PRIVATE-PROJECTS의 임시 경로는 실행 당시
scratch이며 원문 복구에 필요한 유일한 자료가 아니다.

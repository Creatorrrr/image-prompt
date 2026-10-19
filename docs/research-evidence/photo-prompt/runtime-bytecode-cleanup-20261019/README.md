# Bytecode 228개 복원과 검사

현재 macOS 환경에서 검증했다. 원본 cache bytes만 복원하며 cache/source를 실행하지 않는다.
프로젝트 루트에서 아직 없는 임시 목적지를 지정한다. 원래 checkout·CURRENT·설치 세대는 교체하지 않는다.

## 원본-byte ZIP 복원

```sh
photo_zip_parent=$(mktemp -d -t photo-bytecode-zip)
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.14 tools/photo_runtime_maintenance/history_restore.py restore "$photo_zip_parent/root"
```

전체 228개를 원래 상대 경로·bytes·권한으로 새 루트에 복원한다. 기존 목적지·symlink·
경로 이탈·변조·member 충돌은 거부한다. matching 과거 compiler, source Git 객체,
모델·runtime store가 없어도 이 방식은 동작한다. 현재 helper는 표준 Python 3.12/3.14와
macOS의 배타적 atomic rename 환경을 검증했으며 별도 OS 검증을 주장하지 않는다.

## Git source 재컴파일

```sh
photo_git_parent=$(mktemp -d -t photo-bytecode-git)
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.14 tools/photo_runtime_maintenance/history_proof.py restore "$photo_git_parent/root"
```

RESTORE-LOCK-v2.json.gz의 commit/tree/blob·source SHA, 원래 header·compiled filename,
고정된 Python 3.12.13/3.14.3 executable SHA를 사용한다. 로컬 객체가 없거나 compiler가
바뀌면 실패하고 fetch·원격 fallback을 하지 않는다. 그런 경우 원본-byte ZIP을 사용한다.
일부 source commit은 현재 main 바깥의 보존된 local refs에 있으므로 새 clone에서도
Git 방식이 항상 가능하다고 가정하지 않는다.

복원 결과를 원래 경로에 설치하는 작업은 자동으로 하지 않는다. concurrent 파일을
덮어쓰는 checkout/reset/copy 명령을 복구 수단으로 사용하지 않는다.

## 새로운 결과 이름으로 재검사

```sh
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.14 tools/photo_runtime_maintenance/history_checks.py suite recheck-new-unique-label
PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.14 tools/photo_runtime_maintenance/history_checks.py native native-new-unique-label
```

이미 사용한 label은 거부한다. 새 검사 결과만 이번 증거 디렉터리에 추가하며 과거
결과를 덮어쓰지 않는다. suite는 운영 48개·실제 설치 두 질의/receipt·일반 CLI·
archive 450개 순위/17개 테스트·source 지문과 cache 읽기 차단을 확인한다.
새 native 검사는 별도 명시 실행이며 최종 실행은 70개 PASS다.

정리 후 POLICY는 경로 부재를 확인하고 같은 정책으로 기존 실제 파일을 차단했던
POLICY-baseline.json 근거를 연결한다. 존재하지 않는 파일에 대한 접근 실패만으로
새로운 실제 파일 읽기 차단을 입증했다고 표현하지 않는다.

## 증거 파일

- BASELINE.json.gz: 원래 139,187개 보호 경로·Git 상태·CURRENT 기준선.
- TARGETS.json.gz: 후보 228개의 정확한 경로·원래 SHA/mode/inode·분석 입력.
- REFERENCE-CLOSURE.json: 알려진 source/manifest/archive의 소비 경로 확인 범위.
- STAGE02.json: 첫 출처 연결 217개와 초기 보류 기록.
- STAGE02-FINAL.json / RESTORE-LOCK-v2.json.gz: 부모 tree를 확인한 최종 228개 출처.
- BYTECODE-RECOVERY.zip / BYTECODE-RECOVERY-LOCK.json / STAGE03.json: 원본 bytes와 봉인.
- JOURNAL-05/06.json / ABSENT.json / REMOVED.json: 격리·검증·실제 제거 경로.
- SUITE-baseline/absent-A/absent-B.json 및 component JSON: 실제 회귀 결과.
- NATIVE-final.json: native 70개 전체 결과·시간·sandbox receipt. progress JSON의 임시
  log 경로는 실행 중 관찰용이며 완료 후 이 결과에 전체 stderr를 보존했다.
- OFFLINE-FINAL.json / ZIP-INDEPENDENT.json: cache/격리 및 source/Git/model 없이 복원한 범위.
- SAFETY-03-FINAL/05/07-FINAL.json: 복원·충돌·삭제 gate 검사의 근거.
- GIT-BOUNDARY-07.json: 기존 index·출처 refs·커밋 범위·고정 기록의 Git anchor.
- VERIFY-07/08.json: 승인된 228개만 제외한 138,959개 보호 경로 검사.
- ACCOUNTING-08.json / REPORT.md: 크기 해석과 최종 결과.

완료된 freeze/prove/refine/quarantine/final 단계를 다시 실행하지 않는다. 기존 일회성
LOCK을 지워 강제로 재시도하지 않고 journal과 복구 수단을 먼저 확인한다.
나머지 bytecode 86개·기존 미커밋·shard/store·CURRENT는 이번 정리 대상이 아니다.

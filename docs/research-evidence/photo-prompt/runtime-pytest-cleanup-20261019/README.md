# pytest bytecode 복구

정리 결과는 REPORT.md, 복원 기준은 BYTECODE-RECOVERY-LOCK.json과
RESTORE-LOCK-v2.json.gz, 도구 지문은 TOOLCHAIN.json이다.
기존 경로를 덮어쓰지 않고 **아직 없는 새 디렉터리**에 복원한다.

프로젝트 루트에서 원본 bytes를 복원하는 명령:

```sh
python3 -B tools/photo_runtime_maintenance/pytest_restore.py restore /tmp/photo-pytest-recovered-new
```

원래 상대 경로 tests/__pycache__/…를 새 루트 아래에 만들고 전체 집합·SHA·권한을
확인한다. 목적지가 있으면 실패한다. 현재 macOS에서 Python 3.12/3.14로 검증했다.
이 경로에는 Git 객체·원문·옛 pytest 환경·모델·원래 cache·격리본·미커밋 분석이
필요하지 않다. 복원에 사용하는 유지보수 도구와 ZIP·seal·STAGE03 기록은 필요하다.
캐시 코드를 실행하거나 현재 checkout 위에 직접 덮어쓰는 명령이 아니다.

고정한 Git 소스로 pytest 재컴파일:

```sh
python3 -B tools/photo_runtime_maintenance/pytest_proof.py restore /tmp/photo-pytest-recompiled-new
```

이 경로는 .venv의 matching Python/pytest와 TOOLCHAIN.json의 파일들, lock에 기록된
로컬 commit/blob이 필요하다. 새 환경 설치·원격 fetch·누락 객체 추정은 하지 않는다.
원문은 private 복사본으로 컴파일하고 원래 compiled filename/header를 재현한다.
pytest writer/reader를 검증하지만 테스트 모듈이나 cache 본문을 실행하지 않는다.
부모 복원 제어기는 private 트리만 작성하며, 실제 Git·컴파일 subprocess는
네트워크 및 원래 프로젝트/운영 cache 쓰기가 차단된다.

원본-byte ZIP은 이 Git/pytest 복원 조건을 사용할 수 없을 때도 독립적으로 동작한다.
관련 역사 refs·다른 작업 트리·아카이브와 복원 lock을 GC/prune하지 않는다.

안전성 검사:

```sh
python3 -B tools/photo_runtime_maintenance/test_pytest_cleanup.py
```

운영/과거 재현 검사는 pytest_checks.py에서 새 label로 실행할 수 있다.
같은 label의 기존 검사 결과는 덮어쓰지 않는다. 검사 비용과 범위는 REPORT.md를 따른다.
pytest_state.py verify는 이번 고정 기준선과 비교하는 전용 검사다. 이후 새 작업으로
원본이 달라지면 차이를 조사해야 하며, 통과시키기 위해 기존 작업을 되돌리지 않는다.

freeze/prove/quarantine/final 같은 일회성 단계를 다시 실행하거나 완료된 journal과
.LOCK을 지워 제거를 반복하지 않는다. 원본 위치 복귀가 필요하면 새 루트에서 검증한
파일 중 지정한 것만 journal과 대조하고, 동시 생성 파일을 덮어쓰지 않는 방식으로 처리한다.

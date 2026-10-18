# 보류 항목 추가 정리 증거와 복원

실행 결과는 REPORT.md, 대상별 원래 경로와 hash는 TARGETS.json.gz,
shard의 Git/blob·봉인 동일본 연결은 RESTORE-LOCK.json.gz를 참고한다.
운영 진입점은 기존 `skills/photo-prompt-image-generator/scripts/photo_workflow.py`다.
아래 도구는 유지보수용이며 운영에서 자동 실행하지 않는다.

## shard를 빈 임시 루트에 복원

프로젝트 루트에서 다음을 실행한다. 각 destination은 아직 없어야 한다.
`--group`을 생략하면 8세대 전체(약 944MB)를 복원한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/deferred_restore.py restore \
  /tmp/photo-old-shard-from-git-20261019 --backend git \
  --group 09271c8c07daaa23da7919bf67c5c56379466ef816750b20f562c24088d20121

PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/deferred_restore.py restore \
  /tmp/photo-old-shard-from-seal-20261019 --backend sealed \
  --group 09271c8c07daaa23da7919bf67c5c56379466ef816750b20f562c24088d20121
```

복원 루트 아래에 원래 `skills/photo-prompt-image-generator/assets/...` 상대
경로가 만들어진다. 현재 워킹 트리에 자동으로 덮어쓰거나 CURRENT를 전환하지 않는다.
Git backend는 고정된 객체를 읽고, 없으면 fetch 없이 실패한다. sealed backend는
lock이 지정한 보존 세대가 필요하다. 기존 SOURCE-LOCK의 코드 묶음만으로는
후보 데이터·모델이 복원되지 않으므로 세대와 모델 설치도 보존한다.

## bytecode 원래 bytes 복원

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/bundles.py \
  --archive docs/research-evidence/photo-prompt/runtime-cleanup-execution-20261019/BYTECODE-RECOVERY.zip \
  --lock docs/research-evidence/photo-prompt/runtime-cleanup-execution-20261019/BYTECODE-RECOVERY-LOCK.json \
  --destination /tmp/photo-bytecode-restored-20261019
```

45개 파일을 원래 상대 경로로 검증·복원한다. 캐시 본문을 실행하지 않는다.
재생성에 사용한 source SHA·원본 header·compiled owner·interpreter 정보는
BYTECODE-REGENERATION.json에 있다.

## 지정한 과거 validator를 재검사

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/deferred_replay.py replay \
  a1f1996d11b68c9c8256111751b06c5831574593f7ddcc0e650ef5f7e40e7289 \
  --label manual-audit-20261019 --backend git
```

빈 임시 트리에 봉인 코드·데이터와 일치하는 모델 검증 파일을 복사하고,
기존 질의 벡터·결과를 재사용한다. 새 추론이나 원본 데이터·pointer 쓰기는 없다.
이미 존재하는 label의 결과 파일은 덮어쓰지 않으므로 새 label을 사용한다.
모든 과거 workflow의 절대 경로를 복구하거나 모든 역사 CLI를 재생하는 도구는 아니다.

`deferred_state.py freeze`, `deferred_restore.py prove`, `deferred_gc.py 4/5/6`은
완료된 이번 일회성 작업이다. 재실행해 기준선·검증 기록을 새로 만들지 않는다.

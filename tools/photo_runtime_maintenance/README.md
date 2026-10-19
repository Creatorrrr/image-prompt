# 사진 스킬 운영·재현 유지보수 검사

기본 스킬 실행은 `skills/photo-prompt-image-generator/scripts/photo_workflow.py`다.
이 도구들은 유지보수용이며 스킬 검색 경로에서 자동 import하지 않는다.

프로젝트 루트에서 검사 범위를 선택한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/checks.py operating --output /tmp/photo-operating-check.json
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/checks.py native --output /tmp/photo-native-check.json
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/checks.py archive --output /tmp/photo-archive-check.json
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/installed_checks.py --output /tmp/photo-installed-check.json
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/managed_smoke.py --output /tmp/photo-managed-check.json
```

- `operating`: main의 설치 dispatcher, BM25F, shard/oracle, 로컬 임베딩 계약 검사.
- `native`: main의 precore·기존 native·권한 전달·복구 회귀 검사. 임시 fixture에서
  실행하며 원래 runtime store와 프로젝트 파일에는 쓸 수 없다.
- `archive`: 분리된 실험의 원본 상대 경로를 임시 복원하고 저장 순위·집계·전용
  테스트를 재현한다. 현재 스킬의 기본 테스트 모듈 탐색에는 실험을 넣지 않는다.
- `installed_checks`: main 테스트를 대신 실행하는 것이 아니라 실제 설치된 코드로
  기존 두 질의의 전체 풀 점수·순위와 원래 H/native receipt·구성 감사를 검증한다.
- `managed_smoke`: 원본 store·run의 독립 복사본에서 평범한 CLI 진입점의
  retrieve/view/compose-audit/deliver와 기존 issued run의 view를 확인한다.
  기존 로컬 query 벡터를 재사용하며 원본 설치 선택과 CURRENT에는 쓰지 않는다.

네트워크는 OS sandbox로 차단하고 API 키와 외부 Python 경로를 제거한다.
실험 보관물과 운영 소스 lock의 복원 방법은 `docs/research-archives/photo-prompt/README.md`에 있다.
이 검사는 새 의미 판정·이미지 생성·품질 실험·운영 전환을 수행하지 않는다.
전체 테스트 suite나 모든 역사 실행에 대한 전수 검증을 뜻하지 않는다.

`state.py capture`, `classify.py`, `source_bundle.py`, `archive_experiments.py --remove`는
2026-10-19 정리의 고정 기준선/실행용이다. 완료된 기준선을 다시 만들거나
보호 목록을 새 상태로 덮어써서 정리 검증을 통과시키면 안 된다.

과거 실행과 provider 기록만 검증하려면 별도 진입점을 사용한다.

```sh
python3 -B tools/photo_runtime_maintenance/native_replay.py inspect --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py verify --run RUN
python3 -B tools/photo_runtime_maintenance/native_replay.py audit --run RUN
python3 -B tools/photo_runtime_maintenance/historical_evidence.py --result RESULT_JSON --output /tmp/new-history-check.json
```

`inspect`는 원래 receipt/manifest/코드 연결, `verify`는 전체 세대 파일 hash,
`audit`는 원래 봉인 코드의 receipt·구성 감사를 확인한다. 새 임베딩·원격 호출·
CURRENT 전환과 현재 소스로의 fallback은 제공하지 않는다. 필요한 원본이 없으면
거부/보류한다. 상세 범위와 남은 레거시는 `docs/research-archives/photo-prompt/REPLAY.md`를 따른다.

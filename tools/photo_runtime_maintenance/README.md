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

## 미사용 import·지역 변수 일괄 검사

`ruff.toml`은 현행 사진 스킬의 `scripts/`와 `precore/` Python만 검사한다.
Ruff 버전은 CI와 동일하게 고정하며 모델·이미지 API·runtime store를 읽지 않는다.

```sh
python3 -m pip install 'ruff==0.15.1'
ruff check --no-cache skills/photo-prompt-image-generator/scripts skills/photo-prompt-image-generator/precore
ruff check --no-cache --fix skills/photo-prompt-image-generator/scripts skills/photo-prompt-image-generator/precore
```

현재 규칙은 미사용 import `F401`과 지역 변수 `F841`이다. 포맷 변경·import 정렬·unsafe fix는 추가하지 않는다.
GitHub Actions의 `Photo skill unused imports`도 같은 버전·명령으로 PR/main을 검사한다.
새 위반은 가능한 한 한 번에 검토·정리하고 관련 실행 검증 후 묶어서 커밋한다.
기존 미커밋 작업은 자동 수정 결과와 별도로 보존하며 검토한 변경만 stage한다.

보존 예외는 다음 세 종류로 고정했다.

- generator 22개와 contextual appeal 1개의 공개 재노출은 `name as name`으로
  명시한다. 모듈의 공개 이름이나 import 순서를 바꾸지 않는다.
- `qualify_local_hybrid.c`는 모듈 로딩 순서를 보존하는 줄 단위 `# noqa: F401`이다.
- `photo_local_embedding.py`는 현재 설치본의 `worker_sha256`에 묶여 있어
  설정의 단일 파일 예외로 보존한다. 해당 파일의 바이트는 변경하지 않는다.
  별도 release 갱신 시에만 이 예외를 다시 검토한다.

연구/재현 archive, 설치된 봉인 코드, 데이터/색인/모델과 CURRENT는 자동 수정
대상이 아니다. 일반 `ruff check --fix .`도 이 범위·예외를 적용하지만 위의 두
디렉터리를 명시하면 큰 데이터 디렉터리 탐색을 피할 수 있다. 예외를 파일 전체나
규칙 전체로 확장해 새 미사용 import를 숨기지 않는다.

Ruff의 [재노출 규칙](https://docs.astral.sh/ruff/rules/unused-import/)과
[범위 설정](https://docs.astral.sh/ruff/configuration/)을 따른다. import lint는
동적 소비·과거 재현·데이터의 미사용 여부를 판정하는 도구가 아니다.

`F841`은 검사만 활성화하며 자동 수정 대상은 계속 `F401`로 제한한다.
지역 변수 정리는 반환값 사용과 호출 효과를 구분해 수동 검토한다. 계약 검증,
예외 발생, `dict.pop()` 같은 데이터 변경은 유지한다. 기존 미커밋 코드의 위반을
없애기 위해 해당 사용자 작업을 함께 수정·커밋하거나 파일 전체를 예외 처리하지 않는다.
[Ruff F841 문서](https://docs.astral.sh/ruff/rules/unused-variable/)를 참고한다.

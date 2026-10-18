# 사진 스킬 소스·연구 보관물

운영 진입점은 `skills/photo-prompt-image-generator/scripts/photo_workflow.py`다.
이 디렉터리의 보관물을 자동으로 검색하거나 실행하지 않는다.

## 현재 운영 소스

`h-f2-operating-source.zip`와 `SOURCE-LOCK.json`은 설치된 H 단독+F2의 코드
94개와 manifest/lock을 보존한다. 원 commit은 `8469562a46b7e6cbce438d185e7ebe90d15cf37c`다.
실행 중인 세대는 수정하지 않는다. 원문·벡터·모델은 lock에 명시된 보존 세대에 있다.
이 소스 보관물만으로 모델·후보 데이터가 새로 설치되는 것은 아니다.

프로젝트 루트에서 아직 없는 새 경로로 복원한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/bundles.py \
  --archive docs/research-archives/photo-prompt/h-f2-operating-source.zip \
  --lock docs/research-archives/photo-prompt/SOURCE-LOCK.json \
  --destination /tmp/photo-h-f2-source-restored
```

복원 도구는 파일 목록·hash·경로를 검증하고 기존 디렉터리를 덮어쓰지 않는다.
운영 선택, CURRENT, issued receipt는 변경하지 않는다.

## 비활성 후보 보강·독립 lane 실험

`source-review-and-lane-experiments.zip.part001` 등은 32MiB 이하로 나눈 하나의
ZIP이다. `EXPERIMENT-LOCK.json`이 각 부분과 합친 보관물 및 모든 파일의 hash를
검증한다. 두 이전 평가, Claude 논의, 모듈 6개와 테스트 2개의 원래 경로를 보존했다.
운영에서는 이 파일들을 자동으로 읽거나 import하지 않는다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/bundles.py \
  --archive docs/research-archives/photo-prompt/source-review-and-lane-experiments.zip \
  --lock docs/research-archives/photo-prompt/EXPERIMENT-LOCK.json \
  --destination /tmp/photo-experiments-restored
```

`--archive`는 부분 파일들을 합쳤을 때의 이름이며 단일 ZIP 파일이 따로 존재할
필요는 없다. 복원에는 모델·연구 checkout·원래 평가 소스가 필요하지 않다.
저장된 전체 순위와 집계를 재감사하고 실험 테스트를 실행하려면 다음을 사용한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/archive_experiments.py
```

위 명령은 임시 트리에 복원하고 네트워크·원래 연구 경로 접근을 차단한다.
기존 225개 순위와 최신 225개 순위, 실험 테스트 17개를 확인한다. `--remove`는
최초 정리 실행용 옵션이므로 일반 재현에서는 사용하지 않는다. 새 모델 추론이나
의미 판정, 운영 전환은 수행하지 않는다.

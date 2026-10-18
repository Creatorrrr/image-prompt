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

# 공유 작업 트리 관찰

이번 작업은 연구 폴더에만 파일을 썼다. 시작 시 primary checkout에는 이미 대량의 수정·삭제·untracked 항목이 있었다. 원 상태는 BASELINE.json에 저장했다. 그 파일을 복구·삭제·stage하지 않았다.

첫 보존 검사에서 다음 두 보호 파일의 hash가 기준과 달라진 것을 관찰했다.

- `skills/photo-prompt-image-generator/assets/photo_candidate_corpus_manifest.json`
- `skills/photo-prompt-image-generator/retrieval-runtime.json`

변경의 작성자·의도·정확한 시점은 단정하지 않는다. 이번 연구의 도구 호출은 두 파일에 쓰지 않았다. 운영 전체가 보존됐다는 PASS로 덮지 않고 `STRUCTURE_PASS_SOURCE_DRIFT_REQUIRES_REBASELINE` 상태로 기록한다. 최종 시점의 차이는 VALIDATION.json을 따른다.

연구 당시 95모듈·21,252 CID snapshot과 baseline은 그때의 자료다. 후속 구현은 현재 manifest·runtime·sealed 선택을 다시 읽고 새 evidence 폴더에서 기준을 수집해야 한다. 바뀐 source를 예전 source hash나 검색 성공으로 재표기하지 않는다.

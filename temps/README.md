# Temporary Validation Artifacts

이 디렉터리는 스킬 개발 및 검증 과정에서 사용하는 임시 스크립트와 비교·렌더링 이미지를 보관합니다.

- `output/`과 `outputs/` 하위 구조는 파일의 기존 출처를 구분할 수 있도록 유지합니다.
- 이 `README.md`만 Git에서 추적하며, 그 밖의 하위 파일과 폴더는 `.gitignore`로 제외합니다.
- 반복해서 사용할 스크립트는 임시 파일로 두지 말고 적절한 스킬의 `scripts/` 또는 프로젝트 도구 디렉터리로 옮깁니다.
- 일반 실행 산출물은 `artifacts/`, `output/`, `outputs/`, `.codex-artifacts/`, `.codex_runs/`에서도 기본적으로 제외합니다. 기존 연구 문서와 fixture가 참조하는 증거만 명시적인 예외로 유지합니다.
- 보존 대상, 인덱스 세대, 대용량 스냅샷의 복구 기준은 [`docs/git-tracking-policy.md`](../docs/git-tracking-policy.md)를 따릅니다.

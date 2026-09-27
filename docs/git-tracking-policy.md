# Git tracking policy

스킬 실행 자산과 검증에 필요한 선별된 증거를 추적하고, 개별 실행의 임시 파일·로그·소스 복사본은 기본적으로 제외합니다.

## 실행 산출물과 연구 증거

- `artifacts/`, `outputs/`: 각 디렉터리의 `.gitignore`는 모든 일반 실행 산출물을 제외하고 기존 연구 문서·fixture 및 그 증거 파일에서 이름으로 참조하는 파일만 허용합니다. 디렉터리 예외는 해당 파일까지 탐색하기 위한 것이며, 그 디렉터리의 다른 파일을 허용하지 않습니다.
- `output/`, `.codex-artifacts/`, `.codex_runs/`: 로컬 실행 산출물로 제외합니다.
- 새 연구 증거는 `docs/research-evidence/`에, 재사용하는 검증 입력은 `tests/fixtures/`에 선별해 보관합니다. 위 경로의 예외를 추가할 때에는 참조 문서나 fixture와 함께 검토합니다.
- `temps/`는 README만 추적합니다. pytest·Ruff·mypy 캐시와 대용량 source snapshot archive도 제외합니다.

2026-09-28 정리에서는 기존 증거 351개를 원래 경로에서 계속 추적하며, 나머지 실행 산출물 8512개는 Git 인덱스에서만 해제했습니다. 해당 실행 파일과 심볼릭 링크는 로컬 원래 위치에 보존합니다. 완전한 과거 실행 환경이나 소스 복사본이 필요하면 아래 복구 커밋을 사용합니다.

과거 baseline replay의 컴퓨터 절대경로 링크 8개도 인덱스에서만 해제하고 원래 위치에 남겼습니다. 실행 복사본에 있던 링크를 포함해 절대경로 링크 99개가 더 이상 추적되지 않습니다. 대상이 사라진 `.agents/skills/image-prompt-skill-improver` 링크는 제거하고, 유효한 상대경로 스킬 발견 링크는 유지합니다.

## 스킬 실행 자산

`skills/`의 작성된 데이터, 현재 semantic/visual 인덱스, manifest에 열거된 shard, `reverse-image-prompt/SKILL.compiled.*.md` 및 검증 fixture는 추적합니다. 생성 파일이라는 이유만으로 이 자산을 일괄 제외하지 않습니다.

semantic index를 갱신할 때에는 manifest와 그 manifest가 참조하는 shard를 함께 검토합니다. 커밋할 manifest, Git 인덱스의 manifest, 수정 중인 manifest가 참조하는 세대는 보존합니다. 모든 shard 세대에 적용하는 ignore 규칙이나 새 세대를 자동으로 숨기는 allowlist는 사용하지 않습니다.

이번에 해제한 이전 세대 12개, 192개 shard는 로컬에 남겼고 해당 세대만 `.git/info/exclude`에 기록했습니다. 이는 이 checkout의 로컬 보존용 설정이며 새 세대에는 적용되지 않습니다. 이전 세대로 돌아갈 때에는 이 로컬 exclude 설정도 확인합니다. 빌더의 기본 이전 세대 정리 기능은 파일 자체를 삭제하므로 로컬 보존과는 구분합니다.

## 대용량 스냅샷 보존과 복구

아래 두 archive는 Git 인덱스에서 해제했지만 원래 위치에 로컬 파일로 보존합니다. 인접한 보고서와 source snapshot manifest는 계속 추적합니다. 아래 기록은 외부 저장소에 업로드했다는 뜻이 아닙니다.

복구 커밋: `766c327d23d721bfc4bc459e4d596a4563fa7264`. 로컬 백업 브랜치 `codex/backup-before-push-cleanup-20260928`가 이 커밋과 정리 후 커밋의 이력을 보존합니다. 이 백업 브랜치는 로컬에만 유지하며, 복구 커밋은 원격 `main`에 포함되지 않습니다. 새 checkout에서는 이 커밋으로 복구할 수 없으므로 기존 로컬 파일 또는 로컬 백업 이력이 필요합니다.

- `docs/research-evidence/photo-prompt/angle-motion-20260927/high_angle/skill_source_snapshot.tar`
  - bytes: `1057771520`
  - SHA-256: `d6fd2677d12a1b1b7a34c1c825ced6eb30440978c52de4303ea31ceb868a12ac`
  - Git blob: `3a1933271103bf3731bb804c6b6300760d4680ee`
- `docs/research-evidence/photo-prompt/angle-motion-20260927/low_angle/source_snapshot.tar.gz`
  - bytes: `315661260`
  - SHA-256: `e86cb0b64f7350a7ee3928af27303de7fe0c88c0328687014e5ec04783fb5b2d`
  - Git blob: `8e0bc2ca3b3c60874907d59164155701f5d1ddf7`

Git 이력에서 복구할 경우 대상 폴더를 만들고 `git show 766c327d23d721bfc4bc459e4d596a4563fa7264:<repository-relative-path>` 출력을 해당 파일에 저장합니다. 위 SHA-256을 확인한 뒤 사용합니다. 오래된 실행 산출물도 같은 커밋과 원래 경로로 복구할 수 있습니다.

최초 추적 정리에서는 Git 이력을 보존했습니다. 이후 GitHub의 파일 크기 제한을 초과하는 archive가 미푸시 커밋 이력에 남아 있어, 2026-09-28에 원격에 없는 두 커밋을 최종 파일 상태의 단일 커밋으로 합쳤습니다. 원격에 이미 공유한 이력은 유지하고 `main`만 일반 푸시합니다. 이전 커밋은 위 로컬 백업 브랜치에 남아 있으므로 로컬 파일과 Git 객체의 디스크 용량은 줄지 않습니다. 로컬 파일 삭제 및 외부 저장소 업로드는 별도 작업입니다.

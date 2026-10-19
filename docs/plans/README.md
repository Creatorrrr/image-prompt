# 사진 스킬 계획 상태

- `photo-unused-functions-and-replay-separation.md`: 2026-10-19 계획 작성. 미사용
  함수 후보 9개와 과거 재현 경계를 8단계로 정리한다. H 단독+F2·기존 작업·CURRENT를
  보존하고, 지문/참조/재현 검증에 실패한 항목은 보류한다. 구현은 아직 하지 않았다.
- `photo-runtime-and-research-cleanup.md`: 2026-10-19 8단계 실행 완료. 운영·재현·기존
  미커밋 작업·CURRENT를 보존하고 불명확한 항목은 보류했다. 실제 범위는
  `docs/research-evidence/photo-prompt/runtime-cleanup-20261019/REPORT.md`에서 확인한다.
- `candidate-semantic-renewal.md`, `candidate-recall-followup.md`: 이전 실험의 고정
  입력이므로 원문을 유지한다. 두 계획의 실행 결과는 품질 HOLD이며 운영에 적용하지
  않았다. 원래 평가·코드·판정·점수는 `docs/research-archives/photo-prompt/`에 보관했다.

현재 기본은 설치된 H 단독+F2이며, 가장 최근 실험이나 이 계획 목록의 순서가
운영 버전을 선택하지 않는다. `retrieval-runtime.json`과 issued binding이 기준이다.

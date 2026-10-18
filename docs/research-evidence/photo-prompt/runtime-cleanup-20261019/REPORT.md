# 운영·재현 보존 정리 결과

2026-10-19 · 8단계 완료, 보류 포함 · 운영 H 단독+F2 및 CURRENT 유지

## 실제 정리한 범위

비활성 후보 보강·독립 lane 모듈 6개와 실험 테스트 2개, 최근 연구 파일 190개를
운영 개발 경로에서 분리했다. 원래 198개 경로와 추가 재현 입력을 포함한 465개
파일은 `docs/research-archives/photo-prompt/EXPERIMENT-LOCK.json` 및 분할 ZIP에
원래 상대 경로·내용 hash를 보존했다. 과거 FREEZE를 다시 쓰지 않았다.

설치 코드 94개는 원 Git commit `8469562a46b7e6cbce438d185e7ebe90d15cf37c`와
대조하고 `SOURCE-LOCK.json`/운영 소스 ZIP으로 복원 가능하게 했다. 실제 설치 세대를
수정하거나 연구 소스를 운영으로 승격하지 않았다. 후보 정본·리뷰·기존 671건 판정도 보존했다.

캐시는 깨끗한 기존 소스로 바이트 단위 재생성이 입증된 158개만 격리했다.
그 위치에 파일이 없는 상태에서 운영·설치·재현·보호 검사를 통과한 뒤 격리본을
제거했다. 논리 삭제 크기는 3,071,093 bytes(약 3.07MB)다. 저마다 원 소스 hash,
interpreter/magic, header, compile 설정과 exact regeneration 결과를 기록했다.

## 보존·보류한 범위

- 기존 미커밋 작업의 main 파일 경로 40,438개와 다른 작업 트리의 변경 경로
  6,161개를 그대로 유지했다. 일반 Git status가 디렉터리로 접어 보이는 수치와 다르다.
- 설치된 H/native 세대, 모든 발견된 기존 CURRENT 168개, receipt·receipt index,
  로컬 모델 설치, 사용자 이미지·최종 프롬프트·ledger를 유지했다.
- 카메라 구형 helper를 포함하는 모듈, Gemini provider 공용 모듈, 기존 전환·검증
  유지보수 CLI 등 4개 범위는 봉인·재현·유지보수와 연결되어 추가 삭제를 보류했다.
- 오래된 shard 12세대, 다른 역사 runtime/store와 불명확한 연구 증거는 보존했다.
  발견한 실행/receipt 참조 2,487건 중 store를 확인할 수 없는 41건도 보류했다.
- 원 소스가 없거나 변경 중인 경우, 다른 interpreter·경로에서 생성되었거나
  exact regeneration이 다른 bytecode 359개는 원래 위치에 남겼다.
- `candidate-authoring/v1`, 기존 native 진단·계약 거절·권한/효과·precore 격리,
  full-scan oracle, 후보 데이터와 슬롯 binding은 유지했다.

보류 항목이 모두 불필요하다고 판단한 것은 아니다. 이 작업에서 참조 해소와 복원
가능성을 증명하지 못한 항목을 제거하지 않았으며 다른 작업 트리는 정리하지 않았다.

## 검증 결과와 한계

| 검사 | 결과 |
|---|---|
| main 운영/검색/로컬 임베딩 계약 | 48개 PASS |
| main native·권한 전달·복구 회귀 | 70개 PASS |
| 분리된 실험 테스트 | 17개 PASS |
| 경로·변조·분할 복원·덮어쓰기 거부 | 4개 PASS |
| 과거/최신 저장 전체 순위 재현 | 각각 225개, 합계 450개 PASS |
| 실제 설치 코드의 기존 composition·lighting 질의 | 각 BM25F 1회·local cosine 1회, 점수·전체 순위 정확히 동일 |
| 기존 H/native receipt 및 native 구성 감사 | PASS |
| 일반 CLI 진입점의 issued view + 새 retrieve/view/compose-audit/deliver | 독립 복사본에서 PASS |
| 캐시 격리 상태의 운영·실제 설치·아카이브·보호 검사 | PASS |
| 마지막 CLI 재실행 및 보호 상태 | `TEST-MANAGED-08.json`, `VERIFY-08.json` 참조 |

공통 positive 풀 18,180 CID/18,182 actual RID, 슬롯당 1+1 검색, F2/RRF10,
CID 중복 제거와 top8을 유지했다. 실제 설치 코드의 두 질의는 원래 issued score와
비교했고, 일반 CLI 검사도 저장된 동일 결과를 얻었다. 새 로컬 추론 대신 원래
로컬 query 벡터/증거를 재사용했다. Gemini·새 의미 판정·이미지 도구 호출은 0회다.

네트워크, 원본 프로젝트/운영 store 쓰기와 원래 연구 checkout 읽기를 OS sandbox로
차단했다. 일반 CLI 검사는 원본 store/run의 독립 복사본과 기본 store 환경 변수
override를 사용했다. 원래 설치 선택과 issued run에는 결과를 쓰지 않았다.

확장 native suite는 처음의 300초 wrapper 제한을 초과했다. 같은 9개 모듈을
범위를 줄이지 않고 1,200초 제한으로 재실행하여 70개가 모두 통과했다.
전체 프로젝트 테스트, 모든 역사 실행, 새 요청의 의미 품질이나 이미지 품질을
전수 검증했다는 결과는 아니다. 이전 Q1의 57/126·29/40·HOLD 판단도 그대로 재현했다.

## 단계별 커밋

| 단계 | 결과 | 로컬 커밋 |
|---|---|---|
| 1 | 원본·미커밋·실행 참조 보호 기준선 | af06661ab |
| 2 | 운영 코드 94개 Git 출처·복원 검증 | b9370009b |
| 3 | 참조 그래프·198개 경로 분류·불명확 항목 보류 | 484676a45 |
| 4 | 465개 파일 재현 묶음·198개 경로 분리 | f4327ed30 |
| 5 | 운영/native/archive 검사 분리 및 실제 설치 검증 | a3f91e4a7 |
| 6 | 추가 레거시 4개 범위 보존·보류 | 5ee3880ca |
| 7 | 검증된 bytecode 158개 제거 | 9baab7817 |
| 8 | 최종 CLI·보호 확인 및 본 리포트 | 본 리포트를 포함하는 커밋 |

커밋은 이번 변경의 명시적 경로만 stage했다. 원래 수정·미추적 작업을 섞거나
stash/reset/clean하지 않았다. push·pull·설치·publish·CURRENT 전환은 수행하지 않았다.

## 용량과 복원

기존 실행 재현을 우선해 아카이브와 보호 자료를 추가했으므로 전체 저장 용량을
줄인 작업으로 해석하면 안 된다. 7단계까지 추적 파일의 논리 크기는 약 29.59MB
증가했고, 별도로 ignored bytecode 약 3.07MB를 제거했다. 최종 문서 크기는 이
수치에 추가된다. Git 이력은 제거하지 않았다. 실제 물리적 확보 공간은 실행 전
기준선이 없고 APFS/동시 할당 영향을 분리하지 못해 산정하지 않았다.

복원은 `docs/research-archives/photo-prompt/README.md`를 따른다. 기존 경로를
덮어쓰지 않는 새 임시 루트에서 보관물의 hash와 상대 경로를 검증한다.
일반 재현은 다음 명령으로 수행한다.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/photo_runtime_maintenance/archive_experiments.py
```

운영/native/실제 설치 검사와 복사본 CLI 검사는
`tools/photo_runtime_maintenance/README.md`에 별도 명령으로 문서화했다.

주요 근거: `BASELINE.json.gz`, `PROTECTED.json`, `ADDITIONAL-PROTECTED.json.gz`,
`RUN-BINDINGS.json.gz`, `ACTION-LIST.json`, `STAGE01`–`STAGE08.json`,
`TEST-*.json`, `GC-*.json`, `BYTECODE-GC.json`, `VERIFY-*.json`.

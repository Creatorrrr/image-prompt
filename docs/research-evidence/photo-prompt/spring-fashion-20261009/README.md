# 봄 패션 연구 자료

사용자가 참조한 `봄 패션 용어 조사`의 289개 키워드와 15개 검색 조합, 8개 코디를 바탕으로 작성했다. 실행 원본과 분리된 연구 자료다. 모든 카드·후보 초안은 `runtime_ready=false`다.

읽는 순서는 [리서치 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-spring-fashion-visual-semantics-research.md) → [상세 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009/semantic-cards.md) → [행별 반영표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009/term-plan.csv) → [단계별 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/spring-fashion-20261009/implementation-plan.md)이다.

| 파일 | 역할 |
|---|---|
| `thread-api-partial.md`, `thread-tail.tsv`, `thread-rows.json`, `thread-receipt.json` | API 절단과 브라우저 보완을 구분한 원문 인벤토리 |
| `sources.json` | 외부 자료 40개와 원문 대화의 확인 범위·제한 |
| `current-inventory.json`, `current-positive-neighbors.json`, `current-authored-entities.json` | 작성 원본의 조사 스냅샷과 긍정 표현 검토 이웃 |
| `cards-input*.tsv` | 118개 의미 카드의 작성 입력 |
| `semantic-cards.md`, `semantic-cards.json`, `candidate-drafts.json` | 상세 카드와 281개 선택형 문장 초안 |
| `term-plan.csv`, `term-plan.json` | 289개 행의 카드·직접 초안·기존 이웃·경로 대응 |
| `comparisons.tsv`, `regression-plan.json` | 비교 66쌍·변경 반례 14개·이미지 검증 계획 12묶음 |
| `implementation-plan.md`, `implementation-plan.json` | 실제 데이터 승격 작업과 종료 조건 |
| `validation.json`, `report-validation.json` | 연구 무결성과 문서 검사 결과 |
| `workspace-before.json`, `final-preservation.json` | 작업 전후 상태와 동시 작업 변동 기록 |
| `artifact-manifest.json` | 최종 연구 파일의 해시 |

`inspect_current.py`는 실행 원본을 읽어 조사 스냅샷을 다시 작성한다. 재실행 시 조사 시점이 바뀌므로 과거 기록을 유지할 필요가 있으면 새 폴더에서 사용한다. `build_research_artifacts.py`는 현재 폴더의 입력으로 연구 파생물을 재생성하며 실행 assets를 수정하지 않는다. `finalize_research.py`는 문서 링크·계수·표현 대응·보존 상태를 검사한다.

```bash
python3 docs/research-evidence/photo-prompt/spring-fashion-20261009/build_research_artifacts.py
python3 docs/research-evidence/photo-prompt/spring-fashion-20261009/finalize_research.py
```

무결성 PASS는 그래프의 실행 바인딩, 실제 속성 경로, 검색·선택·런타임·픽셀·사용자 수용을 확증하지 않는다. 기존 긍정 표현 이웃도 의미 동등성이나 누락 판정이 아니다. 외부 출처의 직접 확인 37개와 검색 설명만 확인한 3개, 원문만 근거인 카드 14개를 구분한다.

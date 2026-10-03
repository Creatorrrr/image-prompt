# 서브컬처 외형 리서치 패키지

2026-10-03. 연결 대화 [서브컬처 외형 용어 조사](chatgpt-conversation://6ac0831d-0450-83ee-a900-01dbfc850d62)의 키워드를 현재 데이터 규약과 대조한 **조사·초안·반영 계획**이다.

**먼저 읽을 문서:** [상세 리서치](RESEARCH.md) → [반영 계획](IMPLEMENTATION-PLAN.md) → [171개 용어 판단표](TERM-DECISIONS.md).

| 산출물 | 범위 | 읽는 목적 |
|---|---:|---|
| [출처와 확인 범위](SOURCES.md) | 외부 57개 + 원 대화 | 직접 확인한 사실과 연구자의 해석을 구분 |
| [원 용어 목록](TERM-INVENTORY.json) | 171개 | 원 조사에서 누락된 항목이 없는지 확인 |
| [의미 단위](SEMANTIC-UNITS.json) | 187개 | 부품·owner·property 제안·구조 관계·혼동·관찰 조건 |
| [후보 초안](CANDIDATE-DRAFTS.json) | 187개 | 슬롯/범위/잠금 검토 후 실제 authored 후보로 번역 |
| [기존 owner 비교](OWNER-MAP.json) | 32개 비교 행 | 재사용·부분 대응·비동일 경계와 실제 property 확인 |
| [사례집](CHARACTER-CASEBOOK.json) | 37개 | 이름 없는 부품 분해와 정확한 버전/확인 상태 |
| [직접 관찰 기록](REFERENCE-IMAGE-OBSERVATIONS.json) | 공식 도판 2장 | 실제로 본 그림과 아직 보지 않은 그림 구분 |
| [회귀 제안](REGRESSION-PROPOSALS.json) | 40개 혼동 쌍 + 12개 정책 | 부정·기관/장식·owner·잠금·부분 실패 평가 |
| [후보팩 맥락 제안](PACK-CONTEXT-PROPOSALS.json) | 8개 | 고정 core·전체 호환성·정상 거절 검증 |
| [집계](SUMMARY.json) | 전체 | 개수와 상태의 원장 |
| [리서치 검증](VALIDATION.json) | 구조/로컬 참조 | 파일 정합성 검증 결과 |
| [최종 운영 관찰](FINAL-VERIFICATION.json) | 현재 시점 | 시작 기준본과 최신 작업 트리의 차이 |

기준본 profile 1,510개·후보 항목 9,703개는 [Git 참조 카탈로그](REFERENCE-CATALOG-SNAPSHOT.json)에 보존했다. [positive-field probe](COVERAGE-AUDIT.json)는 단순 문자열 진단이며 실제 검색 품질 또는 의미 동등성 판정이 아니다.

초안 33개는 empty slot scope·cross-dimension·라벨만으로 인한 보류이고 나머지도 검토 대상이다. **운영 데이터 반영·52개 의미 회귀 실행·runtime 후보팩 실행·새 이미지 생성은 수행하지 않았다.** 연구 JSON은 runtime schema가 아니며 모든 후보의 즉시 runtime 채택 가능 상태는 false다.

재현은 저장한 기준본을 읽으며 운영 파일을 수정하지 않는다.

```sh
.venv/bin/python docs/research-evidence/photo-prompt/subculture-appearance-20261003/build_research_package.py
.venv/bin/python docs/research-evidence/photo-prompt/subculture-appearance-20261003/validate_research_package.py
```

첫 명령은 source/specs와 확인한 Git baseline에서 연구 JSON을 다시 만든다. 두 번째는 구조·ID·근거·범위 상태·로컬 링크를 검사한다. 두 명령의 PASS는 runtime 의미/생성 이미지/픽셀/사용자 수용의 PASS가 아니다. 공식 출처 재조회도 자동 수행하지 않는다.

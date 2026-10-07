# 키워드 기반 데이터 보강 연구 근거

2026-10-07 · 완료 범위: 상세 리서치·반영 계획. 운영 반영·이미지 생성은 미실행.

- [연구 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-prompt-keyword-enrichment-research.md)
- [반영 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-lexicon-research-20261007/implementation-plan.md)
- [40개 상세 제안 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-lexicon-research-20261007/research-proposals.md)
- [480개 대조표 CSV](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/keyword-lexicon-research-20261007/keyword-coverage.csv)

| 파일 | 내용 |
|---|---|
| keyword-coverage.json / .csv | 480개 표현의 출처 성격·슬롯 매핑·동일 구절 존재·BM25F 어휘 이웃. 동등성·eligibility·성공률의 판정표가 아님 |
| category-coverage.json | 최초 진단의 분류별 어휘 통계 |
| research-proposals.json / .md | 40개 제안의 components·relation·owner·effects·반례·기존 ID·출처 |
| sources.json | 공개 근거 24개, 검토 수준, 각 출처의 적용 한계와 미확보 자료 |
| source-snapshot.json | 480개 진단 시점의 원본·코드 SHA-256과 집계. 과거 파일 전체의 바이트 아카이브는 아님 |
| reference-current-state.json | 후속 제안 ID 검증 시점의 현재 원본과 최초 진단 이후 병행 변경 |
| current-reference-sources.zip | 2026-10-07 12:21:37 KST에 캡처한 현재 후보/프로필 원본 및 코드 135파일의 바이트. generated vectors와 원문 캐시는 제외 |
| source-archive-receipt.json | 위 ZIP의 파일별 hash·archive hash·검증 시점과의 차이 |
| validation.json | 연구 연결 검사 결과. production test 또는 native image pass가 아님 |
| audit_keyword_coverage.py | 현재 로더와 positive projection/BM25F를 사용하는 offline 진단 스크립트 |
| render_research_cards.py | 연구 ID·기존 source ID·출처 연결 검사와 카드 렌더링 |
| implementation-plan.md | P0 16개부터의 원본/인덱스/실제 pack/이미지 비교 적용 단계 |

원문 JSON·Markdown·읽기 안내는 gitignored 캐시인 `skills/prompt-trend-scout/data/raw/inbox/keyword-lexicon-20261007/`에 보관했다. 연구에는 원본 단편의 시각 의미와 출처 성격을 사용했고 완성 프롬프트 예시를 운영 원본에 복사하지 않았다.

현재 파일을 사용하는 스크립트를 다시 실행하면 원본과 코드가 변한 시점의 결과가 나온다. 기존 최초 스냅샷을 동일하게 재현했다고 주장하지 않으며, 새 연구 실행은 별도 디렉터리와 새 hash로 보관하는 것이 적절하다. ZIP은 후속 현재 상태의 바이트 보관이지 이전 11:56–11:58 KST 상태의 재구성이 아니다.

이번 연구는 query embedding API나 image generation API를 호출하지 않았다. 실제 frozen core, applicability, 후보팩 노출, 최종 선택, native pixels, 사용자 선호는 반영 단계에서 별도로 확인한다.


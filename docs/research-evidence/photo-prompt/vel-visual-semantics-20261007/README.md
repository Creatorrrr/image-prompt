# vel 시각 의미·후보팩 강화 연구 패키지

2026-10-07 · 참조 [프롬프트 분석 리스트 vel](https://chatgpt.com/c/6ac5bdb5-f8a4-83ee-adbd-170a43f642de)

**[상세 리서치](RESEARCH.md)** → **[반영 계획](IMPLEMENTATION-PLAN.md)** → **[60개 제안 카드](SEMANTIC-CARDS.md)**

**추가 조사:** 참조 대화 뒤쪽의 외형 요소 분해 전체 217개를 읽고 보완한 [추가 리서치](appearance-decomposition-followup/RESEARCH.md)와 [추가 반영 계획](appearance-decomposition-followup/IMPLEMENTATION-PLAN.md)이 있다. 원본 465개 외형 요소, 28개 관계 카드, 후보 초안 20개, 검토 메모 46개를 정리했다. 아래 수치와 검증은 최초 연구 당시 기록이며 추가 source 스냅샷과 구별한다.

원본 217개 표현·22분류를 모두 연결했다. 긍정 지시 100개, 이미지 설명 97개, 부정 지시 20개를 원래 출처·연령 문맥과 함께 유지한다. 실제 과거 생성 입력·이미지·SNS 원출처를 전수 재확인한 결과는 아니다.

| 산출물 | 규모 | 상태 |
|---|---:|---|
| [원본 키워드](SOURCE-KEYWORDS.json)와 [대조표](KEYWORD-CROSSWALK.md) | 217행 | 다운로드 SHA-256 및 전 행 연결 확인 |
| [구조화 의미 단위](SEMANTIC-UNITS.json) | 217개 | 원본 의미·극성·출처·연령 문맥 보존 |
| [제안 카드](RESEARCH-PROPOSALS.json) | 60개 | 연구자의 관계 설계 |
| [후보 초안](CANDIDATE-DRAFTS.json) | 46개 | 22개 재사용 검토 + 24개 새 관계 trial |
| [선택형 조합](BUNDLE-DRAFTS.json) | 12개 | 선택된 호환 멤버만 결합 |
| [외부 자료](SOURCES.md) | 20개 | 논문·기술 자료·소장품·제작자 기록; 확인 범위별 제한 표기 |
| [개발 회귀 사양](REGRESSION-PLAN.json) | 462개 | 계획, 미실행 |
| [native 대비군](PIXEL-QUALIFICATION-PLAN.json) | 18군 | 계획, 미실행 |
| [연구 검증 결과](VALIDATION.json) | PASS_RESEARCH_INTEGRITY | 원본 보존·ID·출처·링크·초안 상태 검사 |

현재 corpus 읽기 전용 대조는 98개 authored source, 112개 슬롯, 10,500개 후보 항목, 2,290개 profile을 사용했다. [어휘 이웃 JSON](CURRENT-COVERAGE.json), [CSV](LEXICAL-DIAGNOSTICS.csv), [초기 source 스냅샷](CURRENT-SOURCE-SNAPSHOT.json), [audit hash](AUDIT-SOURCE-HASHES.json)를 보존했다. 동일 구절 부재나 짧은 질의의 이웃은 실제 의미 누락·오채택·이미지 효과의 증거가 아니다.

이번 작업의 active runtime 채택·인덱스 배포·live candidate-pack 생성·이미지 생성은 모두 0회다. 생성 비용도 발생하지 않았다. 검증 시 기존 source/code snapshot의 hash 변화는 0개였다. 기존 dirty 작업은 연구의 baseline 스냅샷에 포함되며 새 구현의 시작 기준은 반영 시 다시 확인해야 한다.

재검증:

```bash
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/validate_research.py
```

초안 재조립:

```bash
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/build_research_artifacts.py
```

원본 수집: [참조 대화 텍스트](REFERENCED-CONVERSATION.md), [구조화 대화](REFERENCED-CONVERSATION.json), [원본 다운로드 영수증](SOURCE-DOWNLOAD-RECEIPT.json).

# vel 추가 외형 요소 분해 연구

**[추가 리서치](RESEARCH.md)** → **[반영 계획](IMPLEMENTATION-PLAN.md)** → **[28개 관계 카드](SEMANTIC-CARDS.md)**

참조 대화의 뒤쪽 응답과 첨부 전체 217개를 읽고 기존 연구를 보완했다. 22분류·19출처·긍정100/설명97/부정20을 유지했다. 원본의 외형 요소 465개를 보존하고, 키워드192개는 추가 관계 카드로, 나머지25개는 기존 계획으로 연결했다.

| 산출물 | 수/상태 |
|---|---|
| [전체 대조표](KEYWORD-CROSSWALK.md) / [구조화 단위](SEMANTIC-UNITS.json) | 217개 / 465 atoms, research only |
| [검토 메모](FIDELITY-CORRECTIONS.json) | 46개, source를 수정하지 않은 보존/한계 검토 |
| [관계 카드](RESEARCH-CARDS.json) | 28개: 새 관계13, 재사용7, guard8 |
| [후보 초안](CANDIDATE-DRAFTS.json) | 20개, runtime_ready=false |
| [선택형 메뉴](BUNDLE-DRAFTS.json) | 6개, 모든 멤버 동시 필수 아님 |
| [근거 자료](SOURCES.md) | 새 자료11 + 초기 계승12, 확인 범위/접근 제한 표기 |
| [현행 항목](EXISTING-ENTRY-REVIEW.json) / [adapter 계획](RUNTIME-MAPPING.json) | native loader 상세와 미실행 매핑 |
| [개발 회귀 사양](REGRESSION-PLAN.json) | 193개, PROPOSED_NOT_RUN |
| [픽셀 평가 계획](PIXEL-QUALIFICATION-PLAN.json) | 14군, 5군 pilot45장 계획 / 실제0장 |
| [검증](VALIDATION.json) | 연구 정합성 결과, runtime/pixel 효과와 별도 |

원본은 [JSON](SOURCE-DECOMPOSITION.json)과 [Markdown](SOURCE-DECOMPOSITION.md), [수집 영수증](SOURCE-DOWNLOAD-RECEIPT.json), [추가 대화](REFERENCED-CONVERSATION.md)에 보존했다. 직접 분해128/문맥결합36/해석예시32/제외20/대상1의 권한을 구별한다. 11개 보충 원문 인용은 참조 대화의 주장으로 계승했으며 역사적 원문/최종 입력/이미지를 이번에 독립 인증하지 않았다.

이번 native authored snapshot은 source100 / 슬롯후보10,518 / profile2,308이다. 초기 [상위 연구](../README.md)의 source98 / 슬롯후보10,500 / profile2,290 스냅샷은 당시 기록으로 보존했다. 새 corpus 증가는 이 연구에서 만든 것이 아니다.

재조립 및 검증:

```bash
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/appearance-decomposition-followup/build_followup.py
.venv/bin/python docs/research-evidence/photo-prompt/vel-visual-semantics-20261007/appearance-decomposition-followup/validate_followup.py
```

active 데이터/인덱스/pack/이미지 채택은 0회다. 이 디렉터리의 JSON은 runtime 입력 schema가 아니며 연구자가 선택한 관계/keeper/검증 사양이다.

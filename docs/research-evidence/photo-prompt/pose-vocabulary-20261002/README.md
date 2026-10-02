# 포즈 시각 의미·후보팩 보강 리서치

2026-10-02 · [참조 대화: 포즈 용어 조사](https://chatgpt.com/c/6abf0e48-7010-83ee-8bbf-7764bcfe2150)

**후속 반영 완료:** [구현 보고서](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/implementation/implementation-report.md), [독립 이미지 3개와 실제 판정](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/README.md), [후속 보완 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/pose-vocabulary-20261002/qualification/follow-up-plan.md). 아래 내용과 연구 JSON은 최초 리서치 시점의 기록으로 보존했다. 현재 반영량은 신규 후보 158개·프로필/번들 각각 34개이며, 원본 이미지의 장면 전체 판정은 0/3 PASS다.

원문 **398개 표 행**, **26개 용어군**을 검토하고 요가 **28개 이름**을 별도 분해했다. 결과는 **236개 관찰 정의 후보**, **51개 프로파일 검토안**(기존 3개 재사용·신규 48개), **224개 평가 사례 초안**이다. 42개 출처 레코드는 본문 읽기 34개, 검색 반환 본문 읽기 7개, 접근 실패 참고 단서 1개로 구분했다.

먼저 [상세 리서치](research-report.md)와 [반영 계획](implementation-plan.md)을 읽으면 된다. 핵심은 지지 자세, 관절 형태, 손가락/손바닥, 접촉 대상, 소유자, 관찰자 방향과 동작 단계를 각각 보존하는 것이다.

| 파일 | 용도 |
|---|---|
| [research-report.md](research-report.md) | 현행 감사, 26군 연구, 혼동 경계, 요가·발레·별칭과 근거/제한 |
| [implementation-plan.md](implementation-plan.md) | P0/P1/P2, 실제 파일 위치, 계약 조정, 팩/렌더 검증과 종료 기준 |
| [sources.json](sources.json) | 출처 직접 링크·역할·접근 상태·지원 범위 |
| [keyword-catalog.json](keyword-catalog.json) | 398개 행 + 28개 요가 자식의 처리 방향과 연결 |
| [candidate-data.proposed.json](candidate-data.proposed.json) | 236개 후보의 의미·소유자·속성·반례·가시성 초안 |
| [visual-profiles.proposed.json](visual-profiles.proposed.json) | 요청 전용 활성화·필수 구성요소·원본 게이트 검토안 |
| [evaluation-cases.proposed.jsonl](evaluation-cases.proposed.jsonl) | 부분 충족/가림/동음이의/범위 등을 포함한 사례 |
| [current-data-audit.json](current-data-audit.json) | 확장 병합 후 현행 후보·정책·74개 소스 해시 |
| [verification.json](verification.json) | 정적 수량/참조 검증 및 미실행 증거 층 |
| [seed-terms.txt](seed-terms.txt), [candidate-atoms.tsv](candidate-atoms.tsv), [row-decompositions.tsv](row-decompositions.tsv) | 재생성 가능한 연구 원본 |
| [build_research.py](build_research.py) | 이 폴더의 JSON/JSONL만 재생성하는 연구 도구 |

연구용 초안은 현재 런타임 스키마에 바로 넣는 파일이 아니다. 후보 64개에는 변형·참고 픽셀·개별 출처·동작 단계 확인이 남아 있고, 원본 생성 이미지로 승인된 후보는 없다. 평가 사례도 아직 생산 테스트로 연결하지 않았다.

이번 작업은 이 리서치 폴더만 추가했다. 생산 자산·인덱스는 변경하지 않았고 후보팩/이미지 생성은 실행하지 않았다. 기존 `docs/analysis/2026-10-02-visual-semantics-data-audit/`의 미추적 작업은 보존했다.

재생성 명령(저장소 루트):

```sh
.venv/bin/python docs/research-evidence/photo-prompt/pose-vocabulary-20261002/build_research.py
```

재생성 시점의 현재 자산을 읽어 현행 감사와 해시를 새로 기록한다. 따라서 이후 구현으로 자산이 바뀌면 과거 감사의 보존이 필요하다. 새 결과를 이전 기준의 감사로 오해하지 않도록 별도 날짜/리비전 산출물로 저장한다.

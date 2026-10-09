# 가을 패션 리서치 산출물

기준 대화는 `6ac7dd53-2098-83ee-8a3c-84c3a250f650`, 조사일은 2026-10-09 KST다.

주 보고서: [가을 패션 시각 의미·후보 데이터 상세 리서치와 반영 계획](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-09-autumn-fashion-visual-semantics-research.md).

- [상세 의미 카드](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/semantic-cards.md): 347개 용어 행을 연결한 111개 의미군과 본문 보충 카드 2개.
- [출처 원장](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/sources.md): 직접 사실·상품 사례·스타일 사용례의 권위와 확인 범위.
- [용어 반영 대조표](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/term-plan.csv): 347행의 우선순위, 처리 방식, 현재 표현 이웃.
- [후보 초안](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/candidate-proposals.json): 129개 구체 가시 구현. 신규 런타임 엔트리 수가 아니며 직접 로드 가능한 source 형식이 아니다.
- [적용 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/implementation-plan.json): W0~W6의 순서와 완료 기준.
- [검증 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/autumn-fashion-20261009/regression-plan.json): 의미 비교 56쌍, 변형 반례 12개, 이미지 검사 12묶음. 모두 미실행 계획.

재현 명령은 저장소 루트에서 실행한다.

```bash
python3 docs/research-evidence/photo-prompt/autumn-fashion-20261009/build_research_artifacts.py
python3 docs/research-evidence/photo-prompt/autumn-fashion-20261009/finalize_research.py
```

`audit_current.py`는 새 조사 시점의 원본 스냅샷과 표현 대조를 다시 만든다. 과거 시점을 보존하려면 기존 스냅샷을 덮어쓰지 말고 새 조사 폴더에서 실행한다. 이 작업에서 보존한 원본 시점은 2026-10-09 03:39:32~03:39:47 KST다.

연구 구조 PASS는 사실 확증·라이브 검색·이미지 성공과 다르다. 반영 전 소유자·조건·각 변형의 전체 효과·실제 속성 경로를 확정한다. 가족의 형제 변형은 하나의 all-of 의무가 아니다. 원본·색인·생성기·설정·Git ref는 이번 연구의 쓰기 대상에 포함되지 않는다.

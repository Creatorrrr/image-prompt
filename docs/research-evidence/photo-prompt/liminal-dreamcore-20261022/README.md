# 리미널·드림코어 리서치 패키지

2026-10-22. 연구 결과와 반영 계획이며 운영 데이터에 등록되지 않았다.

먼저 [RESEARCH.md](RESEARCH.md)를 읽고 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)로 이어서 보면 된다.

| 산출물 | 내용 |
|---|---|
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) | 원 대화 200개 항목 전체의 가시 의미·소유 관계·혼동 경계·주장 한계·출처 |
| [semantic-cards.json](semantic-cards.json) | 200개 카드와 성분/관계별 검토 gate 제안 |
| [candidate-drafts.json](candidate-drafts.json) | still/proxy/versioned 128개 연구용 구조 초안; 정식 runtime import 불가 |
| [REALIZATIONS.tsv](REALIZATIONS.tsv) | 32개 한영 장면 실현안·전제·효과 경계; 위 초안과 중첩되므로 수를 단순 합산하지 않음 |
| [SOURCES.tsv](SOURCES.tsv) | 출처 41개의 URL·실제 읽은 범위·한정된 확인 결과 |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 잘린 참조 대화 복원, 접근 실패, 메타데이터만 읽은 자료와 해석의 한계 |
| [existing-source-mapping.json](existing-source-mapping.json) | 기존 CID 23개의 full source·binding·해시와 통합 검토 제안 |
| [EXISTING-CORPUS-AUDIT.json](EXISTING-CORPUS-AUDIT.json) | 전체 content의 리미널 관련 정확 패턴 진단 45건; 실제 검색·의미 적합도 아님 |
| [PRIMITIVE-LEXICAL-AUDIT.json](PRIMITIVE-LEXICAL-AUDIT.json) | 12개 원자 표현의 지정 primary field 진단; 0건이 의미상 부재를 증명하지 않음 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 32·일반 대조 12·비시각 대조 4의 한영 평가 48개, NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 36장 비교와 추가 36장 확장 제안, NOT_RUN |
| [BASELINE.json](BASELINE.json) | 조사 시작 HEAD·기존 작업 상태·추적 파일 3,634개 해시 |
| VALIDATION.json / SHA256SUMS | 패키지 구조 검사와 기존 추적 파일 보존 대조; 의미/검색/이미지 성공과 별개 |

재생성·검증:

```sh
python3 docs/research-evidence/photo-prompt/liminal-dreamcore-20261022/build_research.py
python3 docs/research-evidence/photo-prompt/liminal-dreamcore-20261022/validate_research.py
```

첫 명령은 이 연구 폴더의 파생 문서/JSON만 쓰고, 기존 source/binding과 현행 catalog는 읽는다. 두 번째 명령은 결과와 checksum을 이 폴더에 쓴다. source가 바뀌었다면 재생성으로 옛 증거를 덮기 전에 조사 시점 차이를 기록해야 한다. 임베딩·이미지 API·운영 인덱스 게시를 수행하지 않는다.

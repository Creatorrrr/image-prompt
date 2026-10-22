# 러브크래프트적 공포 시각 의미·후보 데이터 조사

2026-10-22. [참조 대화](https://chatgpt.com/c/6ad9bf09-c888-83ec-a092-36fbff61fd93)의 키워드를 현재 프로젝트와 대조한 연구 패키지다. **한영 의미·관계 끝점·원전 판본 정교화를 먼저 하고, 중복을 확인한 신규 실현을 추가하는 순서**를 권한다.

먼저 [상세 조사](RESEARCH.md), 이어서 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

| 산출물 | 범위 |
|---|---|
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 13개 주제·16개 용어 표의 185개 항목 전체 경로 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 의미 카드 84개: 가시 실현 57개와 문맥/보류 27개 |
| [candidate-drafts.json](candidate-drafts.json) / [REALIZATIONS.tsv](REALIZATIONS.tsv) | 선택형 후보 초안 57개: 재사용7·정교화28·신규제안22. native CID/RID 아님 |
| [SOURCES.tsv](SOURCES.tsv) / [sources.json](sources.json) | 출처45개, 44개 한정 본문/정의/소개 검토, 1개 현재 이용불가 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [existing-source-mapping.json](existing-source-mapping.json) | 기존 의미80개·직접 매핑 후보79개의 전체 record/binding/hash 및 비교 판단 |
| [CORPUS-LEXICAL-AUDIT.json](CORPUS-LEXICAL-AUDIT.json) | snapshot 전체 후보의 지정 primary field 어휘 진단. 검색·의미 부재 증명이 아님 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 양성30·경계26·일반12·비가시/미해결12, 80사례/160개 한영 입력, NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 12사례×3안=36장 비교 제안, NOT_RUN |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 참조 대화 복원, 출처 읽기·판본·도판·서지의 미해결 범위 |
| [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 연구 구조·참조·소유 graph·저장 hash·mutation rejection과 파일 무결성 |
| [BASELINE.json](BASELINE.json) / [SOURCE-DRIFT.json](SOURCE-DRIFT.json) | 시작 source/HEAD/dirty와 변경 관찰. 구현 전에 새 기준 필요 |

84개 카드와 57개 초안은 중첩된다. 기존 180개 코스믹 카드 및 24개 관계 변형과도 합산하지 않는다. 모든 단어의 독립 원전 검증이나 native 승인·운영 등록을 의미하지 않는다.

재생성 및 구조 검사:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/lovecraftian-horror-20261022/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/lovecraftian-horror-20261022/research_evaluation.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/lovecraftian-horror-20261022/validate_research.py
```

`build_research.py`는 보존된 대화 표·출처 metadata·저술 카드와 **그 시점의 현 코퍼스**를 읽어 이 폴더의 파생 파일을 덮어쓴다. `validate_research.py`도 이 폴더의 검증·drift·최종 상태·해시 기록을 갱신한다. 후속 실행 전에는 현재 폴더를 별도 보존해야 한다. 네트워크·임베딩·이미지·runtime 쓰기를 수행하지 않는다.

`collect_sources.py`는 별도의 네트워크 수집 도구다. 현재 웹을 다시 읽고 `sources.json`을 **review pending 상태로 덮어쓴다**. 실제 집중 검토 없이 pending을 PASS로 바꾸면 안 된다. 임시 원문 캐시 없이도 위 세 명령은 실행된다. 도구가 반환한 raw fetch 실패와 웹 도구로 대체 검토한 상태는 이번 sources.json에 구분되어 있다.

이번 작업은 연구 폴더만 작성했다. 운영 source·검색 인덱스·설치본·CURRENT 수정, 신규 임베딩, 검색 실행, 이미지 생성, 픽셀 판정, 커밋·푸시는 하지 않았다. 구조 검사는 연구 자료의 무결성을 확인하며 예술적 품질·사용자 선호를 증명하지 않는다.

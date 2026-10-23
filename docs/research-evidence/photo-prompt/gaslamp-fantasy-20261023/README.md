# Gaslamp Fantasy 시각 의미·후보 데이터 리서치

2026-10-23. 참조 대화를 **크롬에서 끝까지 확인**하고, 상세 조사와 실제 데이터 반영 계획을 정리했다.

먼저 [RESEARCH.md](RESEARCH.md), 이어서 [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md)를 읽으면 된다.

| 산출물 | 범위 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 시각 구조·사회·복식·심령/마법·의학·성/폭력·제도/산업의 구분과 출처 판단 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | 기존 재사용/보완/신규 판단부터 native source·별도 index·검색·픽셀·게시까지의 순서와 완료 조건 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 원 대화 217행: 용어 191·창작 제도 10·작품 9·조합 7. 모두 카드에 연결 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 의미 카드 113개: still 29·proxy 50·context 34. 성분·소유자·방향 관계·혼동·주장 한계·출처·검토 gate |
| [candidate-drafts.json](candidate-drafts.json) | 위 카드 중 한영 가시/대리 실현 79개. runtime import/CID/RID/native approval이 아님 |
| [SCENE-DIRECTIONS.md](SCENE-DIRECTIONS.md) | 원문 조합 7개×저술 장면 대안 2개와 한 컷으로 입증할 수 없는 문맥 |
| [sources.json](sources.json) / [SOURCES.tsv](SOURCES.tsv) | 외부 44개 자료, 실제 접근 상태·읽은 범위·주장 한계 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [adoption-decisions.json](adoption-decisions.json) | source 20,341개 지정 필드 어휘 조사, 30개 full-record/binding snapshot, 18개 구체 채택 판단 제안 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 79·경계 42·일반 8·비가시 14·의역 probe 8 = 151사례/302개 한영 질의, NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 최초 12군×3 arm=36장 계획, 생성/픽셀 NOT_RUN |
| [reference-browser-access.json](reference-browser-access.json) / [reference-complete-rows.json](reference-complete-rows.json) | Chrome 전체 표 복원과 최초 글자수 제한 excerpt의 획득 경계 |
| [ACCESS-LIMITS.md](ACCESS-LIMITS.md) | 소장품 사진/영상·색인만 읽은 자료·미실행 단계의 한계 |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 원본 보호 기준선·연구 구조 검증·작업 중 drift·파일 무결성 |

113개 카드와 79개 초안은 중첩되므로 합산하지 않는다. 217개 원문 행을 모두 확보한 것과 각각의 정의·작품 전체를 독립 검증한 것은 다르다. 카드의 구체 배치는 저술한 선택적 실현이며 역사적 표준형 인증이 아니다.

**완료:** 원문 전체 표 확인·문헌 조사·기존 source의 읽기 전용 진단·연구 카드/초안·반영 계획·연구 패키지 구조 검증.

**미실행:** 운영 source/manifest 변경, native 자격, 인덱스/임베딩/실제 검색, 설치/게시, 프롬프트 실행/이미지/픽셀, 사용자 수용, commit/push. 원본 보호/동시 변경 관찰은 VALIDATION을 따른다.

재생성·검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/gaslamp-fantasy-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/gaslamp-fantasy-20261023/validate_research.py
```

`build_research.py`는 이 폴더의 파생 문서/JSON/TSV만 쓴다. `audit_corpus.py`와 BASELINE은 처음 조사 snapshot을 덮어쓰지 않는다. 구현 뒤의 새 source 조사는 별도 단계 폴더에 남긴다. 위 명령은 이미지·모델·실제 검색 API나 운영 등록을 호출하지 않는다.

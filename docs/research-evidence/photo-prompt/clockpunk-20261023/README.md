# Clockpunk 시각 의미·후보 데이터 리서치

> Git 발행 범위와 저장소에서 열 수 있는 생성 이미지는 [PUBLICATION.md](PUBLICATION.md)에 있다. 원래 연구·로컬 통합 상태와 구분하며, 이번 발행 파일은 PUBLICATION-SHA256SUMS로 검증한다.
>
> 후속 데이터 반영과 독립 이미지 시험은 [실행 기록](INTEGRATION-AND-IMAGE-TESTS.md)에 기록한다. 아래 연구 단계 상태와 구분한다. 원래 SHA256SUMS는 연구 스냅샷이며 당시 로컬 반영 파일은 INTEGRATION-SHA256SUMS로 검증한다.

2026-10-23. [참조 대화](https://chatgpt.com/c/6ada2cba-cb44-83ee-9f24-61beb17fe339)의 213개 표 항목을 바탕으로 **동력·기구·자동인형·천문·공방·공간·복식·제도·신체·성인 미학·폭력·철학·지역 전통**을 조사했다.

핵심은 장르 장식을 늘리기보다 **동력→전달→조절→출력**, 그리고 감기·정비·접근의 사람/기계 관계를 보강하는 것이다. 아스트롤라베/환구의/오러리 번역, `without steam` 보편 정의, 정지 사진의 반복·계산 오차 주장 등 기존 6개 CID의 구체적 보정 지점을 찾았다.

처음에는 [상세 조사](RESEARCH.md), 다음에는 [반영 계획](IMPLEMENTATION-PLAN.md)을 읽으면 된다.

| 산출물 | 범위 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 자료 판단·13개 논점·기존 오류/재사용·한계 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | P0/P1, 실제 반영 경로, native/인덱스/검색/픽셀/게시 단계와 종료 조건 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 16개 분야·17개 표·213개 원 항목 전체의 수작업 연결 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 의미 카드 88개: 구조 57·대리 장면 21·문맥 10. 소유자·방향 관계·혼동·근거·gate |
| [candidate-drafts.json](candidate-drafts.json) | 카드 중 78개의 한영 선택적 실현 초안. runtime import 불가 |
| [SCENE-BLUEPRINTS.md](SCENE-BLUEPRINTS.md) | 원 대화 7개 조합×3개 장면 대안과 남는 서사 경계 |
| [sources.json](sources.json) / [SOURCES.tsv](SOURCES.tsv) | 외부 45개 자료: 본문 지정 구절 37·공식 검색 색인 8, 실제 읽은 범위·접근 한계 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) / [existing-source-mapping.json](existing-source-mapping.json) | source 20,054개 지정 어휘 조사, 20개 일치 snapshot, 기존 CID/조건/효과/binding과 10개 구체 처리 판단 |
| [EVALUATION-CASES.tsv](EVALUATION-CASES.tsv) | 개발 88·경계/일반 32, 한영 240질의. 검색은 NOT_RUN |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 최초 12군×3 arm=36장 제안. 생성·픽셀은 NOT_RUN |
| [BASELINE.json](BASELINE.json) | 시작 HEAD·dirty/untracked·기존 tracked 파일 hash |
| [VALIDATION.json](VALIDATION.json) / [SHA256SUMS](SHA256SUMS) | 연구 참조·중복·owner graph·문맥 분리·snapshot/원본 보존 검사 |
| [WORKSPACE-OBSERVATIONS.md](WORKSPACE-OBSERVATIONS.md) | 작업 중 관찰된 별도 커밋·maintenance/다른 연구 폴더 변화와 증거 범위 |

45개 자료를 모두 완독하거나 원 소장품 사진·영상을 직접 검토한 것은 아니다. 213개 모든 개별 정의의 독립 검증도 아니다. 본문/색인/저술한 장면의 범위를 나눴고, 추가 기술·복식 검토가 필요한 7개 카드를 표시했다. 78개 초안은 88개 카드의 부분집합이므로 합산하지 않는다.

**현재 완료:** 문헌 조사·기존 source의 읽기 전용 진단·연구 카드/초안·반영 계획·연구 패키지 구조 검증. **미실행:** 운영 source/manifest 변경, native 자격, 인덱스/embedding/실제 검색, installed 활성화, 프롬프트 실행/이미지 생성/픽셀, 사용자 수용, 커밋/푸시. 기존 dirty 파일은 이번 작업 범위에 포함시키지 않았다. 최종 보존 결과는 VALIDATION을 따른다.

공유 작업 트리에서는 별도 HEAD 이동과 `maintenance.md` 변경, 다른 장르의 새 연구 폴더가 관찰됐다. 이를 무변경으로 처리하지 않았으며 연구 구조 PASS와 작업 트리 drift를 분리했다. 후보 원본 manifest/module snapshot은 검사 시점에 일치했다.

재생성/검증:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/clockpunk-20261023/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/clockpunk-20261023/validate_research.py
```

`audit_corpus.py`는 현재 source를 읽어 snapshot 증거를 새로 쓰므로 **후속 구현 후에는 기존 조사 증거에 재실행하지 말고 별도 단계 폴더로 보존**한다. baseline도 덮어쓰지 않는다. 위 명령에는 모델·이미지·검색 API나 운영 등록 호출이 없다. `SHA256SUMS`는 패키지 파일 바이트의 무결성 목록이며 내용의 사실성 인증이 아니다.

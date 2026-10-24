# 캠퍼스물 리서치와 반영 계획

참조 대화: [캠퍼스물 용어 조사](https://chatgpt.com/c/6adb6fa1-6c38-83ee-baf9-4f167419bcf2). 한국시간 2026-10-24 조사.

**[상세 리서치](RESEARCH.md)**와 **[반영 계획](IMPLEMENTATION-PLAN.md)**을 먼저 읽으면 된다. 이 패키지는 연구·선택안·후속 검증 설계이며 운영 데이터 변경 보고가 아니다.

| 산출물 | 내용 |
|---|---|
| [RESEARCH.md](RESEARCH.md) | 15개 논점의 조사 결과·출처·데이터 반영 의미 |
| [IMPLEMENTATION-PLAN.md](IMPLEMENTATION-PLAN.md) | P0/P1, 실제 변경 제안 경로, 재사용 심사, native/검색/프롬프트/픽셀/설치/발행 기준 |
| [KEYWORD-ATLAS.md](KEYWORD-ATLAS.md) / [keyword-routes.json](keyword-routes.json) | 전체 용어 356행의 관련 카드/문맥 연결 |
| [reference-concept-examples.json](reference-concept-examples.json) | 원 대화의 창작 조합 8개; 작품/외부 사례 아님 |
| [VISUAL-CARDS.md](VISUAL-CARDS.md) / [semantic-cards.json](semantic-cards.json) | 124카드: 가시 80·선택 연출 21·시간 1·문맥 22 |
| [candidate-drafts.json](candidate-drafts.json) | 가시/연출 101카드의 한영 실현 초안; runtime import 불가 |
| [SOURCES.md](SOURCES.md) / [sources.json](sources.json) | 외부 30건: 지정 본문 25·소장품 텍스트 2·검색 발췌만 1·접근 실패 2 |
| [CORPUS-FINDINGS.md](CORPUS-FINDINGS.md) | 105모듈·전체 CID 21,883·binding 16,698·149슬롯의 읽기 전용 조사; 14 CID 원문/조건/effects/binding 대조 |
| [existing-source-triage.json](existing-source-triage.json) | 기존 후보 재사용 6·정제 6·문맥 분리 2 제안, 승인 아님 |
| [BOUNDARY-CASES.tsv](BOUNDARY-CASES.tsv) | 별도 저술한 경계 36사례·72 한영 질의; 개발용이며 독립 holdout 아님 |
| [development-cases.json](development-cases.json) | 카드 파생 124사례·248질의; 실제 검색 미실행 |
| [PIXEL-PLAN.md](PIXEL-PLAN.md) | 첫 12사례 × 3 arms = 36장 비교 제안; 생성 0장 |
| [GAPS.md](GAPS.md) | 미검증 미학·재단·지역 관행·묶인 대안 구조와 후속 자료 |
| [BASELINE.json](BASELINE.json) / [VALIDATION.json](VALIDATION.json) | 조사 당시 상태와 보호 대상 파일의 이후 변동 관찰 |
| [WORKSPACE-OBSERVATIONS.md](WORKSPACE-OBSERVATIONS.md) | HEAD 진행·보호 범위·개별 형상 초안이 남은 용어의 명시 |
| [SHA256SUMS](SHA256SUMS) | 패키지 파일 바이트 무결성 목록; 사실성·검색·픽셀 인증 아님 |

참조 대화의 connector 응답은 잘렸으므로 Chrome 렌더링 본문과 26개 표를 추가 확보했다. 용어 356개·창작 조합 8개·표 밖 혼동 경계 6개를 분리했다. 연구 문맥에 성인 관계·성적 강압·폭력·범죄·위기 관련 항목을 보존했으며, 가시 외형과 신원·동의·원인·진단·권한·시간·소리의 사실을 구별했다.

관련 용어를 연결했다고 모두 같은 형상·동의어·검증된 정의라는 뜻은 아니다. 카드 124개와 초안 101개는 부분집합 관계이며 합산해서 신규 후보 수로 세지 않는다. 정확한 제안 구도는 연구자의 저술이다. 기관 문서와 소장품 설명이 모든 geometry를 증명하지 않으며 외부 원 이미지 픽셀은 이번에 검토하지 않았다.

연구 패키지 구조 검증과 실제 runtime 품질을 분리한다. 운영 source/manifest·기존 CURRENT 변경, native qualification, 실제 검색/embedding/index build·verify, 설치, 이미지 생성/픽셀, 사용자 수용, commit/push는 수행하지 않았다. 기존 작업 파일은 수정하지 않고 새 연구 폴더에만 작성했다. 최종 관찰 상태는 VALIDATION.json을 따른다.

최종 구조 검사는 27/27 통과했다. 비교한 기존 tracked 파일 7,656개와 source 모듈의 바이트 변동은 없었으나 공유 작업의 HEAD가 진행하여 `STRUCTURE_PASS_WORKSPACE_DRIFT_REQUIRES_REBASELINE`로 기록했다. 실제 반영 직전 최신 상태를 다시 확인한다.

재생성·구조 확인:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/campus-fiction-20261024/build_research.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/research-evidence/photo-prompt/campus-fiction-20261024/validate_research.py
```

기존 corpus/BASELINE snapshot은 후속 통합으로 덮어쓰지 않는다. 실제 반영 직전 최신 source와 상태를 새 단계 폴더에 다시 수집한다. validator는 공유 작업 트리의 변동을 관찰·기록하며 다른 작업의 변경을 복원하거나 삭제하지 않는다.

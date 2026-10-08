# 패션 핏 연구 증거와 반영 초안

2026-10-08 KST. 사용자 요청 범위는 참조 대화의 용어를 바탕으로 한 상세 연구와 반영 계획이다. 런타임 등록·인덱스 생성·실제 검색/구성·이미지 생성은 수행하지 않았다.

[전체 연구 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-08-fashion-fit-visual-semantics-research.md)를 먼저 읽고, 개별 변형은 아래 자료에서 확인한다.

| 파일 | 의미 |
|---|---|
| `seed-terms.txt` | 전체 대화 DOM에서 확인한 21분류 513개 용어 행의 이름 |
| `term-inventory.json` | 씨앗·별칭과 조사 당시 긍정 검색 필드의 문자 이웃 |
| `source-snapshot.json` | 01:19:52~01:20:07의 파일 hash·mode와 공식 로더 집계 |
| `current-positive-records.json` | 검토용 후보 751개·프로필 545개의 한정 발췌; 전체 검색 DB가 아님 |
| `source-notes.txt` / `sources.json` | 출처 41개의 확인 범위·접근 수준·한계 |
| `research-cards.txt` / `semantic-cards.json` / `semantic-cards.md` | 상세 의미군 64개; P0 30 / P1 28 / P2 6 |
| `candidate-proposals.json` | 선택형 영어 문장 119개와 가족 수준 관계·속성 초안 |
| `term-plan.json` / `term-plan.csv` | 513개 전수 반영 경로·출처·기존 문자 이웃 |
| `implementation-plan.json` | 의존 관계와 완료 조건을 가진 6단계 실행 계획 |
| `regression-plan.json` | 38비교·10변경 반례·12이미지 검증 묶음의 미실행 계획 |
| `existing-id-verification.json` | 카드에서 재사용 검토 대상으로 적은 ID의 원본 존재 확인 |
| `report-validation.json` | 보고서·참조·링크·원본 ID 존재 검사 |
| `final-preservation.json` | 시작/종료 파일 상태 차이, 이번 쓰기 범위, 전체 보존 주장의 한계 |
| `research-validation.json` | 연구 파일 ID·집계·매핑 무결성과 파일 SHA-256 |

문자 이웃은 의미 동등성·검색 성공·선택·이미지 결과가 아니다. 119개 초안도 신규 엔트리 목표치가 아니다. 의복·부위·상태의 변형을 선택하고, 구체 관계 노드·실제 스키마 경로·완전한 효과 범위를 확정한 뒤 기존 항목과 중복을 검토한다. 카드 한 개의 모든 대안을 한 프로필의 필수 조건으로 합치지 않는다.

측정·공정·내부 구조·동적 성능은 정지 사진의 hard gate로 추정하지 않는다. 출처 연결은 의미군 수준이며 513개 별칭 모두가 각각 독립 출처로 확증됐다는 뜻이 아니다. source 원장에 접근 오류와 후속 확인 범위를 보존했다.

`audit_current.py`는 당시 원본을 읽고 연구 폴더에만 증거를 작성한 절차다. 보존된 baseline을 현재 데이터로 덮어쓰지 않는다. `build_research_artifacts.py`는 메모에서 카드·원장·초안을 만들고, `finalize_research.py`는 문서 참조와 종료 파일 차이를 확인한다. 최종 산출물 hash는 종료 자료가 생성된 뒤 builder를 마지막으로 실행해 기록한다. 이 스크립트들은 런타임 빌더나 임베딩·이미지 API를 호출하지 않는다.

이번 작업이 작성한 것은 이 폴더와 위 보고서다. 동시에 변한 manifest/인덱스의 내용은 수정·되돌림·staging하지 않았다. 초기 untracked 상태 목록은 기록했으나 모든 untracked/ignored 파일의 바이트 보존을 검증한 것은 아니다.

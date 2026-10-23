# 아이돌물 리서치 패키지

게시 범위·main 통합 검증·영구 증거 위치·정리 정책은 [PUBLICATION.md](PUBLICATION.md)를 확인한다.

> 후속 실행: 실제 등록·설치·검색 결과는 [반영 결과](INTEGRATION-RESULTS.md), 세 독립 이미지 실험은 [이미지 테스트 결과](IMAGE-TEST-RESULTS.md)를 확인한다. 아래 수량과 미실행 표시는 최초 연구 스냅샷 당시의 상태다.

2026-10-23 KST. 참조 대화 [아이돌물 용어 조사](https://chatgpt.com/c/6adb5ac9-6bb0-83ee-b5e0-cfccf3213ca6)를 로그인된 Chrome에서 끝까지 읽고 진행한 연구다.

먼저 [상세 보고서](REPORT.md)를 읽고, 구현에는 [데이터 반영 계획](IMPLEMENTATION-PLAN.md), 검증에는 [검색·의미 평가 계획](EVALUATION-PLAN.md)과 [이미지 평가 계획](PIXEL-PLAN.md)을 사용한다.

| 자료 | 내용 |
|---|---|
| [키워드 처분표](KEYWORD-ATLAS.md) | 원문 용어 325개 각각의 선택형 카드·문맥·보류 연결 |
| [시각 카드](VISUAL-CARDS.md) | 한영 완전 명제 120개, 관찰 기준 360개 |
| [출처 목록](SOURCES.md) | 27개 출처의 확인 범위와 접근 한계 |
| [요약 JSON](SUMMARY.json) | 수량·가족별 범위·현재 미실행 상태 |
| [후보 초안](candidate-drafts.json) | 120개 연구 제안; 실제 V3 코퍼스로 직접 import 불가 |
| [문맥 구별](context-distinctions.json) | 비가시·시간·역할·관계 경계 45개 |
| [추가 조사 보류](holds.json) | 9개 주제, 원문 용어 46개; 삭제·우회·대체 아님 |
| [기존 코퍼스 진단](CORPUS-AUDIT.json) | 95개 등록 모듈, 21,252개 후보의 작업 소스 기준 어휘 조사와 해시 |
| [기존 소스별 처분](existing-source-triage.json) | 12개 CID의 재사용·분리·문맥 검토 메모 |
| [개발 평가 설계](evaluation-cases.json) | 76개 모두 not_run; 독립 holdout 아님 |
| [구조 검증 결과](VALIDATION.json) | 22개 점검 통과; 자연어·native·검색·이미지 검증과 구분 |
| [설치 recorder 점검](RUNTIME-CHECK.json) | 읽기 전용 실행 환경 확인; 신규 데이터 노출 증거는 아님 |

원문 provenance는 `conversation-full-visible.txt`, `conversation-table-rows.json`, `conversation-links.json`에 보존했다. `conversation-preview.json`은 잘린 도구 응답이다. `seed-keywords.json`은 헤더와 장면 예시를 제외한 정확한 325개 표 행이며, 예시 9개는 `seed-scene-examples.json`에 분리했다.

## 재현

저장소 루트에서 연구 산출물만 다시 작성하려면 다음을 순서대로 실행한다.

```bash
python3 docs/research-evidence/photo-prompt/idol-fiction-20261023/build_research.py
python3 docs/research-evidence/photo-prompt/idol-fiction-20261023/build_evaluation.py
python3 docs/research-evidence/photo-prompt/idol-fiction-20261023/validate_research.py
```

`audit_corpus.py`는 현재 작업 소스를 새로 읽어 기준 스냅샷을 덮어쓰므로, 과거 기준을 보존하려면 먼저 `CORPUS-AUDIT.json`과 해시 목록을 별도로 보존한다. 빌더는 런타임 manifest·후보 모듈·인덱스·설치 포인터를 수정하지 않는다. `DELIVERY-SHA256SUMS.txt`는 최초 연구 스냅샷의 해시 목록이다. 후속 등록·테스트 산출물은 `INTEGRATION-DELIVERY-SHA256SUMS.txt`로 별도 관리한다. 최초 연구 빌더를 다시 실행하면 과거 증거가 바뀌므로 기존 파일을 먼저 보존한다.

최초 연구 스냅샷 당시 실제 데이터 등록 0, native 자격 검토 0, 검색 평가 실행 0, 이미지 호출 0이었다. 공개 출처는 분야·기능·용례의 제한된 맥락 근거이며, 카드의 전체 장면은 저자가 만든 선택 대안이다. 구조 PASS가 출처 의미·정확한 표본·역할 승인·픽셀 품질을 보증하지 않는다.

# 영지물 시각 의미·후보 데이터 강화 리서치

2026-10-24, Asia/Seoul. 참조 대화: [영지물 용어 정리](https://chatgpt.com/c/6adb6fa8-75e8-83ee-b793-434d3667a266).

**영지물의 보강 단위는 성·귀족·중세 의상이라는 묶음보다, 땅·노동·생산·유통·기록·주민을 연결하는 구체적인 관계여야 한다.** 아래 연구 수량과 미실행 표시는 최초 조사 시점의 상태다. 후속 요청으로 시각 의미·후보 데이터를 반영하고 독립된 세 이미지 실험을 진행한 결과는 [반영·이미지 테스트 보고서](INTEGRATION-AND-IMAGE-TESTS.md)에 별도로 기록한다.

후속 반영은 새 선택형 시각 후보 22개, 긍정 검색에서 제외되는 시각 보류 36개와 문맥 진단 20개, 선택형 연결 56개를 등록하고 기존 완전한 후보 2개를 재사용한다. 374개 원문 표제는 탐색용 연결로 보존하며, 모든 표제의 정확한 정의나 역사 재현이 검증되었다는 뜻은 아니다.

## 읽을 문서

- [실패 보완과 동일 컨셉 재시험](repair-20261024/REPAIR-AND-RETEST-RESULTS.md): 원본 실패 분석, 보완 자료 8건(최종 긍정 7·진단 보류 1)·연결 21건, 독립 세 작성자의 재생성 및 실제 픽셀 판정.
- [조사 결과와 판단](RESEARCH.md): 핵심 정의, 시각화 방법, 혼동 경계, 기존 데이터 비교, 우선순위.
- [80개 카드 상세](SEMANTIC-DETAILS.md): 시각 제안 60개와 문맥 진단 20개. 한영 문장·소유자·연결·확인할 픽셀·출처.
- [반영 계획](IMPLEMENTATION-PLAN.md): 재사용·보정·신규 추가·보류, 실제 파일 위치, 단계별 완료 조건.
- [검색·회귀·픽셀 평가 계획](EVALUATION-PLAN.md): 실현 전체와 부분 관계를 구별하는 검증 설계.

## 산출물과 실제 상태

| 항목 | 이번 결과 | 한계 |
|---|---:|---|
| 원 대화 표 행 | 374행, 20절 | 복합 표제를 보존한 행 수. 고유 개념 수가 아님 |
| 출처 항목 | 37 | 본문/PDF 25, 초록 1, 출판사 소개 1, 검색 발췌 8, 접근 실패 2 |
| 시각 의미 카드 | 60 | 완전한 선택형 장면 초안. 역사 재현·native 자격은 미승인 |
| 문맥 진단 카드 | 20 | 법적 신분·권리·시간·동의·역사 신화 등; 긍정 시각 사실로 사용하지 않음 |
| 후보 초안 | 60 | 운영 candidate schema와 분리. 바로 manifest에 등록할 수 없음 |
| 역할 연결 제안 | 136 | 실제 149-slot catalog에 있는 이름만 사용. 역할 적합성 승인은 아님 |
| 기존 정본 직접 검토 | 8 CID | 전체 조건/effects·원문 보존. live retrieval/native/pixel 검증은 미수행 |
| 평가 사례 | 192 | 계획된 정·혼동·가림/오소유 사례 180 + 일반 대조 12. 실행 결과 아님 |

원문 표의 163행에는 제한된 시각 제안이, 155행에는 문맥 진단만 연결되어 있다. 나머지 56행은 키워드를 보존하고 정확한 정의·도판 보강을 대기한다. 연결된 행도 복합 표제 전체의 정의가 검증되었다는 뜻은 아니다. 건틀릿을 착용한 상태와 벗는 동작 같은 차이는 긍정 연결에서 제외했다. 상세 상태는 [reference-inventory.json](reference-inventory.json), 후속 항목은 [FOLLOWUP-BACKLOG.md](FOLLOWUP-BACKLOG.md)에 있다.

## 원 대화 복원

`read_thread`는 응답이 20,000자에서 잘렸다. 로그인된 Chrome의 정상 대화 화면에서 전체 본문 27,655자와 모든 표를 읽었으며, 18절의 여러 하위 표도 포함했다. 절별 행 수는 `14,15,20,17,19,18,22,18,18,22,20,22,18,23,17,16,24,32,9,10`으로 원문 DOM과 대조했다. 마지막 행은 ‘전쟁 후 영지 재건’이다.

원문의 첫 열 표제는 [reference_inventory.py](reference_inventory.py)에 전사했다. 이는 전체 대화의 byte-exact 백업이 아니다. 원 대화의 인용을 사실로 승격하지 않고 이번에 별도로 확인한 출처의 지원 범위를 기록했다.

## 데이터 파일

- [sources.json](sources.json): 출처 URL·접근 수준·지원 주장·일반화 한계.
- [semantic-cards.json](semantic-cards.json): 부품·owner·관계·출처·혼동·gate.
- [candidate-drafts.json](candidate-drafts.json): 독립적인 한영 실현·조건/effects 검토 항목·역할 연결 초안.
- [existing-source-mapping.json](existing-source-mapping.json): 현재 source 스캔과 수동 검토한 8개 정본.
- [scene-combinations.json](scene-combinations.json): 원 대화의 장면 조합 10개와 관련 카드. 자동 합성 지시 아님.
- [regression-cases.json](regression-cases.json): 향후 실행할 평가 사례와 기대 판단.
- [research-summary.json](research-summary.json): 계산된 수량·상태.
- [BASELINE.json](BASELINE.json): 조사 기준 HEAD·source module hash·dirty tracked file hash.

재생성: `python3 docs/research-evidence/photo-prompt/estate-management-20261024/build_research.py`.
무결성 확인: `python3 docs/research-evidence/photo-prompt/estate-management-20261024/validate_research.py`.

최초 조사 검사의 통과는 연결 무결성의 증거다. 번역의 의미 일치·역사 고증·검색 적합성·생성 이미지의 성공을 대신하지 않는다. 최초 조사에서는 이미지 생성·커밋·푸시를 수행하지 않았으며, 후속 실행 결과는 위 별도 보고서에 기록한다.

# 은어 기반 시각 의미·후보 데이터 연구

2026-10-03 — [적 은어 조사](chatgpt-conversation://6ac08aa8-0ea8-83ee-adba-a7a2c78c5aad) 대화의 키워드를 실제 데이터 계약과 외부 출처로 대조한 연구 패키지.

읽는 순서: [리서치 보고서](RESEARCH.md) → [반영 계획](IMPLEMENTATION-PLAN.md) → [후보 초안](CANDIDATE-DRAFTS.json) → [검증 기록](VALIDATION.json).

## 주요 결과

기존 아헤가오의 작은 O자·중앙 혀끝·피로 필수 계약은 용어 전체와 범위가 다르므로 우선 검토한다. 양손 V는 기존 후보를 재사용하면서 얼굴과 같은 인물·동시성 관계를 보강한다. 하트눈, M형 다리와 피부 문양은 위치·매체·지지·가시성으로 나눈다. 부위 명칭·평가어·역할어·사건어는 원뜻을 보존하면서 무근거 외형 추가를 막는다.

| 자료 | 수량·상태 |
|---|---|
| 참조 대화 | 완료된 3개 턴 |
| 표 행 / 표기 묶음 / 개별 표기 | 274 / 217 / 234 |
| 철자별 연구 처분 | 234개, 42개 작업 분류 |
| 출처 | 42개 기록, 관련 내용 확보 39, 접근 실패·게이트 3 |
| 관찰·문맥 단위 | 36개 |
| 후보 초안 | 28개, 명시 보류 6개 |
| 회귀 제안 | 92개, 모두 PROPOSED_NOT_RUN |
| 기준 exact resolver 진단 | 22개, 전체 파이프라인 평가 아님 |

철자 관련 텍스트를 읽은 표기 19개, 검색 관련 텍스트 확인 9개, 원어·번역·관련 뜻의 매핑 검토 19개다. 개별 근거가 필요한 187개는 별도 backlog로 남겼다. 전체 처분 완료는 전체 사전 검증 완료라는 뜻이 아니다.

## 데이터와 증거

- [CONVERSATION-RECEIPT.json](CONVERSATION-RECEIPT.json): 참조 대화와 untrusted data 경계.
- [TERM-INVENTORY.json](TERM-INVENTORY.json): SR/ST ID와 원문 행 위치.
- [TERM-DECISIONS.json](TERM-DECISIONS.json): 표기별 근거 상태·보존 의미·금지 추론·처분.
- [SOURCES.md](SOURCES.md), [SOURCES.json](SOURCES.json): 출처·확인 범위·한계.
- [SEMANTIC-UNITS.json](SEMANTIC-UNITS.json): 36개 형태·소유·관계·문맥 단위.
- [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json): 실제 slot·owner·효과와 6개 보류.
- [REGRESSION-PROPOSALS.json](REGRESSION-PROPOSALS.json): 검색 인덱스 밖 92개 holdout.
- [LEXICAL-BACKLOG.json](LEXICAL-BACKLOG.json): 철자별 직접 어휘 확인이 남은 항목.
- [INPUT-RECEIPT.json](INPUT-RECEIPT.json): 기준 HEAD·파일 해시·git 상태.
- [CURRENT-DATA-AUDIT.json](CURRENT-DATA-AUDIT.json): 기준 loader·owner·후보 scope·22개 진단.
- [VALIDATION.json](VALIDATION.json): 구조·참조·링크·최종 입력 해시 차이.

기준 loader는 1,510개 프로필·112개 슬롯·9,703개 후보를 읽었다. 공유 checkout의 다른 통합으로 파일 변경이 관찰되어, 이 숫자를 최종 현재 runtime 수치로 주장하지 않는다. 해시는 객체·진단을 읽은 뒤 수집했으므로 원자적인 한 시점의 runtime 스냅샷이라고 주장하지 않는다. 실제 반영 전 최신 해시·owner·loader·인덱스를 재확인한다.

## 재현 범위

`audit_inputs.py`는 현재 corpus를 읽고 이 연구 폴더에 기준 감사 파일을 작성한다. 최초 기준 기록을 보존하려면 실행 전 감사 파일을 다른 evidence 폴더에 복사한다. active assets와 derived indexes는 쓰지 않는다.

`validate_research.py`는 기록된 snapshot을 기준으로 연구의 참조·범위를 검사하고, 현재 파일 해시 차이를 별도로 기록한다. 현재 runtime의 의미·성능을 검증하는 테스트가 아니다.

```sh
.venv/bin/python docs/research-evidence/photo-prompt/slang-visual-semantics-20261003/validate_research.py
```

연구 구조 검사 PASS는 authored 반영, 새 v6 팩 채택, 프롬프트 품질, 네이티브 픽셀 또는 사용자 수용의 PASS가 아니다. 이번 연구에서는 이미지 생성과 runtime 데이터 반영을 수행하지 않았다.

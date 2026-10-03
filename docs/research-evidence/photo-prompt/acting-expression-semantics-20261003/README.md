# 연기 용어 시각 의미·후보팩 강화 조사 패키지

2026-10-03 KST. 원 대화: [연기 용어 조사](chatgpt-conversation://6abfdef9-2904-83ee-853f-e5e012a7db35).

**상세 리서치와 반영 계획까지 작성한 상태이다. 운영 자산·코드·manifest·파생 인덱스는 변경하지 않았다.**

## 읽는 순서

1. [상세 리서치](RESEARCH.md): 출처와 현행 원본 비교, 얼굴 형태, 32개 감정 묶음, 성인 호감·관용어, 시간·음성·방법론의 반영 범위.
2. [반영 계획](IMPLEMENTATION-PLAN.md): 파일별 변경 위치, P0–P4 단계, 문맥 guard, 검색·프롬프트·픽셀 기준.
3. [64개 개념 초안 목록](CATALOGUE.md): 각 개념의 관찰 요소·혼동 경계·출처.
4. [원 대화 368행 반영 경로](TERM-DECISIONS.md): 원 용어 묶음 전체 범위를 어떻게 보존할지.
5. [출처와 한계](SOURCES.md), [구조 검증 결과](VALIDATION.json).

## 자료 구성

| 파일 | 내용 |
|---|---|
| [SOURCE-TERM-GROUPS.json](SOURCE-TERM-GROUPS.json) | 원 대화의 13절·25표·368행과 추가 본문 용어 |
| [SOURCES.json](SOURCES.json) | 40개 출처의 지원 내용·확인 수준·한계 |
| [CURRENT-DATA-AUDIT.json](CURRENT-DATA-AUDIT.json) | 고정 커밋의 1,496 프로필·9,664 후보와 기존 ID |
| [KEYWORD-COVERAGE.json](KEYWORD-COVERAGE.json) | 양성 텍스트의 문자열 힌트; resolver 결과가 아님 |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | 기준 커밋과 원본 74개 파일의 SHA-256 |
| [PROPOSED-DATA.json](PROPOSED-DATA.json) | 64개 연구 설계와 필요한 문맥·관찰 매체 |
| [REUSE-PLAN.json](REUSE-PLAN.json) | 11개 기존 후보의 재사용 조건 |
| [DRAFT-VISUAL-PROFILES.json](DRAFT-VISUAL-PROFILES.json) | 11개 좁은 관찰 형태 프로필 초안 |
| [DRAFT-CANDIDATE-EXTENSION.json](DRAFT-CANDIDATE-EXTENSION.json) | 새 후보 38개와 optional bundle 11개 |
| [TERM-DECISIONS.json](TERM-DECISIONS.json) | 원 대화의 각 행에 대한 경로 결정 |
| [REGRESSION-CASES.jsonl](REGRESSION-CASES.jsonl) | 실행 전 문맥·부정·소유권·잠금 사례 75개 |
| [PIXEL-PLAN.json](PIXEL-PLAN.json) | 실행 전 정지 이미지 비교 11쌍, 시퀀스·음성 후속 계획 |
| [PACKAGE-COUNTS.json](PACKAGE-COUNTS.json) | 범위와 산출물 수량 |

## 재현과 검증 범위

기준 원본은 Git 커밋 `0adb5f6e56416e2656dfb4150d0724867530c2bc`이다. 공유 작업 디렉터리의 병합과 조사 원본이 섞이지 않도록 Git blob을 직접 읽었다. 새로 구현할 때에는 최신 병합 원본과 재비교해야 한다.

저장소 루트에서 실행하는 연구 스크립트는 다음이다.

```sh
python docs/research-evidence/photo-prompt/acting-expression-semantics-20261003/build_research_package.py
python docs/research-evidence/photo-prompt/acting-expression-semantics-20261003/validate_research_package.py
```

두 스크립트는 이 조사 디렉터리의 문서·초안·검증 결과만 작성한다. 원본 감사의 재현은 별도의 [audit_current_data.py](audit_current_data.py)이며 양성 표면 문자열 비교까지 수행해 더 오래 걸릴 수 있다. 순수 컴파일러가 고정 커밋과 달라졌으면 검사에서 중단한다.

구조 검증은 JSON/Python 구문, 해시, 기존 ID, 프로필 투영, 후보의 순수 메모리 병합·semantic schema, 보고서 링크를 다룬다. **75개 의미 사례의 실제 resolver 실행, 후보 순위·노출, guard 강제, 프롬프트 생성, 이미지·사용자 수용은 검사하지 않았다.**

문맥 요구는 연구 envelope에 기록되어 있으며 현재 초안만으로 강제되는 것은 아니다. 새 후보 파일의 JSON 구조가 유효해도 문맥 guard를 반영·검증하기 전 운영 manifest에 넣지 않는다. 이름 없는 묘사·원어·번역·반례·픽셀을 함께 확인해야 반영 성공으로 볼 수 있다.

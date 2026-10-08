# 흙·땅 시각 의미·후보 데이터 리서치

2026-10-08 KST · 연구·반영 계획 · 운영 반영 전

[흙 관련 용어 조사](https://chatgpt.com/c/6ac64439-5d78-83ee-9666-50854b9f786a)의 30개 범주·470개 표제어 행을 확인하고, 현재 후보·시각 프로필 원본과 대조했다. 결과는 120개 연구 단위, 359개 관찰 구성 제안, 후보·프로필 각 96개 초안이다. 출처 47건에는 본문 확인·검색 발췌·범위 확인·접근 실패·원 대화를 구분해 기록했다.

## 읽는 순서

1. [리서치 종합](research-report.md): 30개 범주의 보강 방향, 핵심 의미 구별, 현재 데이터 점검, 출처와 품질의 한계.
2. [반영 계획](implementation-plan.md): 다의어·표현 배율 확정 → 기존 ID 재사용 → P0 물리 단위 작성 → 원본·인덱스·runtime → 프롬프트·픽셀 검증.
3. [120개 상세 연구 카드](research-cards.md): 정의·소유 대상·관찰 표현·방향 있는 관계·혼동 경계·프레이밍·출처 확인 범위.

## 데이터와 근거

| 파일 | 내용과 사용 범위 |
|---|---|
| [original-keywords.json](original-keywords.json) | 원 대화의 30개 범주·470행. 마지막 조합 예시 표는 표제어 수에 포함하지 않음 |
| [sources.json](sources.json) | 47개 출처의 URL, 확인 상태, 확인 가능한 범위 |
| [research-units.json](research-units.json) | 120개 연구 단위의 정의·관찰·관계·배율·혼동 경계 |
| [keyword-routing.json](keyword-routing.json) | 470행에서 연구 queue로 가는 경로. 동일 외형이나 hard activation 매핑이 아님 |
| [candidate-proposals.json](candidate-proposals.json) | 96개 후보 초안과 신규/재사용 상태. wrapper를 운영 원본에 그대로 import하지 않음 |
| [visual-profile-proposals.json](visual-profile-proposals.json) | 96개 authored-component 초안. 채택·변형 분리·자연 한국어·활성화 검토가 남음 |
| [reuse-plan.json](reuse-plan.json) | 12개 연구 단위에 연결한 현재 원본 참조 20개. 의미 동등성은 후속 검토 |
| [existing-inventory.json](existing-inventory.json) | 원본 104개 파일의 해시와 표제어 대조 결과 |
| [existing-overlap-hints.json](existing-overlap-hints.json) | 107개 문자열 겹침 단서. 다른 뜻·부분 문자열을 포함하는 검토 입구 |
| [validation-case-plan.json](validation-case-plan.json) | 회귀 canary 80개·렌더 시나리오군 12개. 계획이며 실행 결과가 아님 |
| [research-validation.json](research-validation.json) | 참조·현재 순수 계약/컴파일러·property 잠금 검사 및 작업공간 지문 비교 |
| [workspace-before.json](workspace-before.json) | 초기 상태와 보호 파일 118개의 지문. 모든 ignored/untracked 파일의 보존 증거는 아님 |
| [source-conversation-cache.json](source-conversation-cache.json) | read_thread에서 받은 잘린 부분 자료. 전체 표제어는 브라우저에서 별도 확인 |

## 완료 상태

후보 96개와 프로필 96개의 소스 계약·컴파일러 검사, 120개 연구 단위의 참조 무결성, 기존 참조 20개의 실재, property 잠금 5건을 확인했다. 이 검사는 검색 정확도·최종 의미 적합성·렌더 품질을 측정하지 않는다. 96쌍은 확정 신규 항목 수가 아니며, 여러 변형을 담은 항목과 미완료 출처는 채택 전에 분리·보강·보류를 결정한다.

원본 inventory의 104개 파일은 최종 검사에서 동일했다. 초기 보호 파일 118개 중 의미 인덱스 파일 1개의 변경이 공유 작업공간에서 관측되었다. 이번 연구의 저작 파일은 이 폴더 안에 있으며, 인덱스 변경의 원인을 이 검사로 확정하거나 되돌리지 않았다. 검증 JSON의 pass는 연구 계약을 가리키며 전체 작업공간의 동일성 판정은 별도로 기록했다.

운영 데이터 등록·인덱스 재생성·runtime 게시·후보팩/이미지 생성·픽셀 심사·commit/push는 이번 작업에서 수행하지 않았다.

## 재현

저장소 루트에서 다음 순서로 실행한다. 첫 두 명령은 이 폴더의 파생 연구 파일만 다시 작성하며, 세 번째는 현재 원본 계약을 읽고 연구 검증 결과를 갱신한다. 원본 표제어·inventory·초기 지문과 종합 보고서는 입력 또는 수작업 저작 문서다.

~~~bash
.venv/bin/python docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/author_research.py
.venv/bin/python docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/validation-case-plan.py
.venv/bin/python docs/research-evidence/photo-prompt/soil-earth-semantics-20261008/validate_research.py
~~~

[연구 패키지 해시](research-package-manifest.json)는 전달 시점의 파일을 고정한다. 재현 뒤에는 파생 파일과 검증 결과가 달라질 수 있으므로 원래 manifest를 과거 전달 기록으로 보존한다.

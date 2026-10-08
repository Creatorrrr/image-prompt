# 셀카 포즈 시각 의미·후보 데이터 리서치

2026-10-08 KST · 상세 조사·초안·반영 계획 · 운영 반영 전

‘셀카 포즈 조사’의 18개 분류·180개 촬영 변형과 20개 요약 검색행을 확인했다. 180개 연구 카드, 소유 대상별 시각·촬영 구성요소 540개, 후보·프로필 각 79개 초안, 기존 원본 참조 119개, 출처 26건을 정리했다. 회귀 사례 68개와 대표 렌더 시나리오군 13개는 향후 실행 계획이다.

## 읽는 순서

1. [리서치 종합](research-report.md): 18개 분류의 보강 방향, 물리 관계·혼동 경계, 현재 데이터에서 확인한 문제와 출처 한계.
2. [반영 계획](implementation-plan.md): 정의/변형 결정 → 촬영 방식과 손 역할 → 좁은 원본 반영 → index/runtime → 검색·선택·literal → 픽셀 판정.
3. [180개 상세 카드](research-cards.md): 항목별 소유 대상·관찰 문장·방향 관계·촬영 조건·가시성·기존/신규 판단.

## 근거와 초안

| 파일 | 내용과 사용 범위 |
|---|---|
| [original-keywords.json](original-keywords.json) | 브라우저에서 확인한 180개 번호 행과 20개 요약 행의 표제어·분류 전사 |
| [source-conversation-cache.json](source-conversation-cache.json) | 잘린 read_thread 캐시. 전체 원문 저장본이 아님 |
| [sources.json](sources.json) | 출처 26건의 URL·확인 상태·지지 범위·한계. 외부 본문 확인 18건 |
| [seed-research.tsv](seed-research.tsv) | 번호별 시각·촬영 구성과 혼동 경계·가시성의 저작 입력 |
| [research-units.json](research-units.json) | 180개 연구 단위, 구성요소 540개, 소유·방향 관계·효과·반영 결정 |
| [keyword-routing.json](keyword-routing.json) | 200개 원문 행의 연구 경로. 런타임 exact alias 표가 아님 |
| [candidate-proposals.json](candidate-proposals.json) | 후보 79개 초안. 실제 actor/target 매핑과 잠금·변형 검토 후 채택하며 wrapper는 운영에 직접 import하지 않음 |
| [visual-profile-proposals.json](visual-profile-proposals.json) | 프로필 79개 초안. 순수 컴파일 성공이 활성화 승인이나 픽셀 합격은 아님 |
| [reuse-plan.json](reuse-plan.json) | 연구 단위 104개의 기존 원본 참조 119개. 전체 형태의 의미 동등성을 승인한 목록이 아님 |
| [existing-inventory.json](existing-inventory.json) | authored JSON 104개 파일의 지문과 원본 행. 행 수는 live loader 활성 수가 아님 |
| [current-data-audit.json](current-data-audit.json) | 긍정 이름의 문자열 대조 단서와 실제 소스에서 확인한 쟁점. 검색 성능 측정이 아님 |
| [validation-case-plan.json](validation-case-plan.json) | 회귀 설계 68개·렌더 시나리오군 13개와 비교 방법. end-to-end/픽셀 실행 전 |
| [research-validation.json](research-validation.json) | 연구 참조·순수 소스 계약/컴파일러·property 잠금과 기존 파일 지문 비교의 실제 검사 결과 |
| [workspace-before.json](workspace-before.json) | 캡처 시점의 원본·수정 tracked 파일 113개의 지문. 모든 ignored/untracked 보존의 증거는 아님 |
| [package-counts.json](package-counts.json) | 최종 연구 단위·초안·재사용·출처 확인 범위의 집계 |
| [research-package-manifest.json](research-package-manifest.json) | 전달 시점 연구 파일의 SHA-256. 재현 뒤 기존 전달 기록을 덮어쓰지 않음 |

## 검증 상태

180개 번호와 20개 요약 행의 경로, 출처 연결, 79개 후보의 순수 계약, 79개 프로필의 source/compiler 계약과 생성 게이트 237개, 기존 참조 119개의 실재를 확인했다. 연구 후보에 대해 14개 property 잠금 검사도 수행했다. 이 검사는 실제 resolver의 owner 매핑·검색 순위·후보 채택·최종 literal·이미지 품질을 측정하지 않는다. 한국어 양의 성분 문장은 31개 프로필군의 93개 성분에 들어 있으며 나머지 채택 항목도 후속 검토가 필요하다.

고양이 하트의 대표 손가락 배치와 밤비라는 이름의 hard activation은 출처/동등성 확인 전 보류했다. 원문의 성인 패션·부두아·반항·액션 범위는 연구 카드에 유지했다. 그림자·가림·손가락 형태 같은 픽셀 증거와 0.5 배율·실제 거리/높이·촬영자·셔터 원인 같은 입력/실행 조건을 구별했다.

authored 원본 104개는 검사 시 초기 지문과 같았다. 보호 파일 113개 가운데 semantic index·source manifest·visual profile index 3개의 변경이 공유 작업공간에서 관측됐다. 이번 연구의 저작 파일은 이 폴더 안에 있으며 해당 변경의 원인을 이 검사로 확정하거나 되돌리지 않았다. validation의 pass는 연구 계약을 가리키고 전체 작업공간 동일성을 뜻하지 않는다.

운영 소스 등록·인덱스 재생성·runtime 게시·후보팩 생성·이미지 생성·픽셀 판정·commit/push는 이번 작업에서 수행하지 않았다.

## 재현

저장소 루트에서 실행한다. 세 명령은 이 연구 폴더의 파생 연구 파일과 검사 결과만 저작한다. 기존 source snapshot·초기 지문·원 대화 캐시는 재수집하지 않으며 현재 파일이 달라졌다면 그 차이를 별도 기록한다.

```bash
.venv/bin/python docs/research-evidence/photo-prompt/selfie-pose-semantics-20261008/build_research.py
.venv/bin/python docs/research-evidence/photo-prompt/selfie-pose-semantics-20261008/plan_validation.py
.venv/bin/python docs/research-evidence/photo-prompt/selfie-pose-semantics-20261008/validate_research.py
```

재현 시 최종 manifest를 과거 전달 기록으로 보존한다. 위 빌더를 운영 assets 작성 도구로 사용하지 않는다.

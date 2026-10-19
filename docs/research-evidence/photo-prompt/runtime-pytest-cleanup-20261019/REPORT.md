# pytest bytecode 65개 정리 결과

2026-10-19 · 8단계 실행·검증 · H 단독+F2/CURRENT 보존

pytest bytecode **65개 / 807,566 logical bytes**를 실제로 정리했다. 원래 경로와
전용 격리 디렉터리 모두 부재하며, 이번 후보 중 최종 보류는 0개다. 기존에 보류한
다른 bytecode 21개 / 2,235,198 bytes는 원래 상태로 보존했다.

| 배치 | 정확한 재생성에 사용한 소스 | 실제 정리 | 원본 논리 bytes |
|---|---|---:|---:|
| A | 현재의 깨끗한 소스 | 47 | 479,822 |
| B | 과거 Git 소스 | 18 | 327,744 |
| 합계 | Python 3.14.3·pytest 9.0.3 | 65 | 807,566 |

두 배치 모두 현재 소스는 존재한다. 소스·테스트 모듈·cache 본문을 실행해 출처를
추정하지 않았으며, 고정한 소스의 private 복사본을 컴파일하고 원본 bytes 전체를
비교했다. 원래 소스 파일과 mtime은 수정하지 않았다.

## 단계별 결과와 커밋

| 단계 | 결과 | 커밋 |
|---|---|---|
| 1 | 정확한 65개, A/B 배분, 기존 작업·CURRENT·추가 보호 기준선 고정 | `f3713e0bd` |
| 2 | 소비 경로·Git 출처·pytest 도구 지문과 전체 bytes 재생성 검증 | `a6e198c2b` |
| 3 | 원본 ZIP·Git 재컴파일·독립 ZIP 복원과 안전성 검증 | `c80f90598` |
| 4 | 실제 설치·운영·일반 CLI·과거 archive 기준 검증 | `6fecfdae1` |
| 5 | A 47개 격리 후 원래/격리 경로 읽기 차단 상태의 회귀·보존 검증 | `bd9f1468f` |
| 6 | B 18개 추가 격리 후 합산 65개 부재 상태의 동일 검증 | `16ea994f4` |
| 7 | native 70개·안전성 53개·최종 복구 통과 후 실제 제거·보존 확인 | `5c577de6c` |
| 8 | 결과·복원 명령·회계·최종 보존 검증 | 이 보고서를 포함한 커밋 |

각 단계 검증 후 이번 작업의 경로만 커밋했다. push는 수행하지 않았다.
ignored cache 자체의 제거는 Git diff에 나타나지 않으므로 ABSENT/REMOVED,
JOURNAL-05/06, STAGE07과 보호·복구 결과로 실제 처리를 기록했다.

## 운영·과거 재현·복구 검증

| 검사 | 실제 결과 |
|---|---|
| working 운영 검사 | 48개 PASS |
| 실제 설치 H-F2 | composition/lighting 2개 목표의 점수·전체 순위·receipt 감사 PASS |
| 일반 CLI | 기존 view, 새 retrieve/view/compose-audit/deliver 5개 PASS |
| 실제 검색 호출 | 각 목표 BM25F 1회·local_cosine 1회, 저장 query vector 재사용 |
| 과거/최신 archive | 저장 순위 225+225개 동일, 실험 테스트 17개 PASS |
| pytest writer/reader | 65개 원본 전체 bytes와 읽기 계약 PASS |
| native·권한·전달·복구 | 70개 PASS, skip 0, 783.090초 |
| 삭제·복원 안전성 | 최종 53개 PASS: 신규 16, 기존 공유 검사 22+11+4 |
| 최종 오프라인 복구 | 원본 ZIP·Git/pytest 재컴파일 각각 65개 PASS |
| 독립 ZIP 복구 | Git·원문·기존 pytest·모델·원래 cache·격리본 읽기 차단하에 65개 PASS |
| 공개 Git 복원 CLI | 미커밋 분석·모델·원래 cache·격리본을 사용하지 않고 65개 PASS |
| 실제 제거 후 문서의 ZIP 명령 | 65개 PASS |
| 실제 제거 후 보호 검사 | 138,979개 보호 경로, CURRENT 168개 PASS |

기준, A 부재, A+B 부재 상태에서 운영·설치·일반 CLI·archive·pytest 검사를
확인했다. 실제 worker의 OS sandbox가 네트워크·원래 프로젝트/공유 runtime 쓰기와
원래 cache 65개·격리본 읽기를 차단한다. 같은 합산 부재/차단 조건의 성공 결과는
최종 단계에서 재사용했으며, native 70개는 최종 합산 부재 상태에서 한 번 실행했다.

source/code/model 지문은 세 실행에서 모두
`b8fe35370835f14b92923b00e106465dcbf8708dc3226b3973560c40db3b9254`로 같다
(source 764개, code 77개). 설치 선택 H 세대 `663038595155…`, native 세대
`9649504ffbcd…`, 운영 코드 지문 `493f1830db1f…`와 검색 정책을 유지했다.
공통 풀 전체 검색과 슬롯당 1+1 검색 경로는 실제 설치/CLI 검사에서 확인했다.

Gemini·새 로컬 임베딩 추론·새 의미 판정·실제 이미지 생성 호출은 없다. native
테스트의 이미지/도구 관찰은 오프라인 fixture이며 실제 이미지 생성 품질 검사가 아니다.
기존 HOLD 판정과 원래 workflow/receipt/FREEZE를 변경하지 않았다.

## 복구 수단과 보존 범위

원본-byte ZIP은 **368,182 bytes**이며 파일별 상대 경로·SHA·권한과 ZIP SHA를
봉인했다. Python 3.12로도 복원해 역사 Python/pytest 환경에 의존하지 않음을
확인했다. 원래 cache와 격리본을 사용할 수 없는 상태에서 두 복구 수단을 다시
검증했고, 실제 제거 후 문서의 복원 명령도 실행했다.

Git 재컴파일은 65개의 소스와 commit/tree/blob·compiled filename·원래 header를
고정한다. 필요한 source commit 10개는 모두 main의 선행 이력에 있다. Python과
pytest 및 관련 도구 파일 597개의 SHA를 기록했다. 도구나 객체가 없으면 자동 설치·
fetch하지 않으며, 그 경우에도 원본-byte ZIP 복원 경로를 사용할 수 있다.
정확한 복원 명령·전제·비덮어쓰기 정책은 README.md를 따른다.

기존 기준선 139,044개 보호 경로를 재사용하고 추가 85개의 stamp만 저장했다.
BASELINE-DELTA.json.gz는 11,729 bytes로, 기존 큰 기준선을 복제하지 않았다.
원래 65개만 의도된 부재로 인정하고 나머지 138,979개를 계속 비교했다.

main의 원래 modified/untracked 경로 40,463개와 다른 작업 트리 6,161개,
staged 내용, 다른 작업 트리 HEAD/index, 모든 CURRENT 168개와 설치 선택을
보존했다. 기존 미커밋 분석 13파일은 변경하거나 stage하지 않았다.

다음 항목도 보존했다.

- 대상 밖 cache 21개: 미커밋 소스 연결 5개, 일반 재생성 미입증 15개,
  과거 소스 미확보 pytest cache 1개.
- root shard 5세대, 공용·유지보수 모듈 4개, 모든 역사 store·봉인 코드·모델·
  소스/실험 아카이브와 다른 작업 트리.
- 고유 판정·리뷰·query vector·receipt/index·사용자 출력·이미지·ledger.
- 이전 미해결 실행 41건의 원본과 대체 세대. 이 41건을 새로 전부 replay하거나
  원래 절대 store 경로를 복구한 결과는 아니다.

이전 228개와 그 이전 bytecode/shard 제거는 이번 성과에 중복 집계하지 않았다.
Git 이력 재작성·GC/prune·stash/reset/clean·CURRENT 전환은 하지 않았다.

## 검증 중 발견한 사항과 처리

첫 참조 검사에서는 직전 분석 도구가 private `.pyc`를 만드는 한 줄을 미해결로
분류해 65개를 보류했다. 해당 파일 SHA와 44–46행을 확인해 원본 cache 실행이 아닌
임시 컴파일 출력임을 입증했다. 최초 기록은 남기고 REFERENCE-CLOSURE-FINAL과
STAGE02-FINAL에서 출처·재생성 65개를 다시 통과시켰다.

공개 Git CLI의 추가 검사에서 outer/inner sandbox 중첩이 호스트 제한으로 실패했다.
이 BLOCKED_HARNESS 기록을 보존하고, 실제 Git/컴파일 subprocess 경계마다 보호
정책을 추가하는 신뢰된 임시 launcher로 다시 실행해 65개를 검증했다. sandbox 실패를
캐시 회귀나 성공으로 처리하지 않았다.

SAFETY-07의 최초 그룹 설명은 분할 개수를 잘못 적었지만 실제 53개는 통과했다.
삭제 gate를 강화한 뒤 53개를 재실행하고 모듈별 16/22/11/4로 정확히 기록한
SAFETY-07-FINAL을 최종 근거로 사용했다. 기존 실패·중간 근거는 덮어쓰지 않았다.

## 크기와 최종 상태

7단계까지 새로 추적한 계획·도구·복구 ZIP·증거는 74파일 / 713,160 logical bytes다.
원본 cache 제거 807,566 bytes를 뺀 순변화는 -94,406 bytes이며, 최종 보고서·
복원 안내·8단계 증거는 여기에 추가된다(ACCOUNTING-08.json의 명시적 범위).
이는 논리 크기 계산이며 APFS 공유 블록 등 실제 물리 확보 공간은 측정하지 않았다.

JOURNAL-05/06은 `gc_done`이고 격리 디렉터리는 없다. 최종 보존 결과는
VERIFY-08.json, 단계 완료 기준은 STAGE08.json을 따른다. 일회성 .LOCK과 완료된
journal을 지워 제거를 반복하지 않는다. NATIVE-final-progress의 private log 경로는
실행 중 진행 확인용이며, 전체 로그는 NATIVE-final.json에 보존했다.

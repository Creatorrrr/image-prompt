# 과거 Git source 기반 bytecode 228개 추가 정리 결과

2026-10-19 · 8단계 완료 · H 단독+F2 및 기존 CURRENT 유지

## 실제 처리 결과

| 배치 | 파일 | 원래 파일의 논리 bytes | 결과 |
|---|---:|---:|---|
| A: 현재 source가 있음 | 25 | 807,269 | 격리·부재 검사 후 정리 |
| B: 현재 source가 없음 | 203 | 4,256,525 | 격리·부재 검사 후 정리 |
| 합계 | 228 | 5,063,794 | 실제 정리 228개, 이번 후보 중 DEFER 0개 |

원래 228개 경로와 이번 격리본은 모두 없다. 정확한 목록은 TARGETS.json.gz,
REMOVED.json, 이동·검증·최종 제거 기록은 JOURNAL-05/06.json에 있다.
B의 source는 과거 테스트 202개와 스크립트 1개다. 과거 source를 운영 경로에
복귀시키지 않았으며 cache와 그 source를 import/실행해 복원을 시험하지 않았다.

남은 원래 bytecode는 정확히 86개 / 3,042,764 bytes다. 미커밋 source 연결 5개,
재생성 미입증 15개, pytest rewrite 66개를 기존 상태로 유지했다. 이전 158개·45개
cache 및 구 shard 8세대 정리를 이번 수치에 중복 집계하지 않았다.

## 운영·기존 작업 보존

main의 기존 변경 경로 40,450개와 다른 작업 트리의 6,161개, 기존 수정 176개,
직전 분석의 미커밋 7파일을 보존했다. 승인된 이번 계획 파일과 이번 도구·실행
증거만 커밋했으며 기존 분석 파일은 stage하지 않았다. stash/reset/clean은 하지 않았다.
다른 작업 트리 HEAD와 staged 내용 및 이전에 고정한 index 자체의 SHA도 같다.

보호 기준선 139,187개 중 실제 승인 제거 대상 228개만 예외로 두어 최종
138,959개를 대조했다. 모든 알려진 CURRENT 168개, 실제 설치 선택·H/native
세대·코드·모델·receipt·receipt index·원래 실행 출력이 유지됐다.

현재 root native shard `2b40e6433faf…`, 미커밋 `511defb8e52e…`, `6235873c869b…`,
`85e3161b28b0…`, rollback `89b2a0e79319…` 등 5세대와 공용 모듈 4개,
모든 역사 store·기존 아카이브·사용자 이미지·프롬프트·ledger·리뷰·판정·vector를 유지했다.
원래 store 경로가 없던 실행 41건과 대체 4세대/7복사본도 그대로 두었다.

H 단독+F2의 공통 positive 풀 18,180 CID/18,182 RID, 단일 query, 슬롯당
BM25F 1회·local cosine 1회, F2/RRF10/top8/CID 중복 제거를 유지했다.
working source/code/model 지문은 정리 전후 동일하다(source SHA
`b8fe35370835f14b92923b00e106465dcbf8708dc3226b3973560c40db3b9254`, source 파일
764개·code 77개). 실제 설치 코드 94개와 설치 선택은 변경하지 않았다.

## 출처·참조와 복원 근거

알려진 보호 Python source 9,877개, 실행 메타데이터 438개, 검증된 source archive
563 members 및 기존 run binding을 조사했다. cache 관련 34개 행은 검사·복사 제외
등의 용도였으며 조사 범위에서 직접 cache 입력이나 미해결 소비 경로는 없었다.
외부·모든 과거 CLI의 참조를 전수 해소했다는 뜻은 아니다.

Python 3.12.13에서 18개, 3.14.3에서 210개를 정확한 source Git blob/SHA,
원래 header·compiled filename·최적화 설정으로 재생성했다. 상대 compiled filename
1개도 그대로 보존했다. 임시 source의 mtime만 header에 맞췄다.

첫 commit 연결 검사에서 빠졌던 11개는 변경/삭제 commit의 부모 tree에서 source를
찾아 다시 검증했다. 초기 217개 결과를 덮어쓰지 않고 STAGE02-FINAL.json과
RESTORE-LOCK-v2.json.gz에 228개 최종 결과를 추가했다. source commit 106개는
모두 보존된 로컬 refs에서 도달 가능하며 관련 commit/tree/blob 관계를 확인했다.

원본-byte BYTECODE-RECOVERY.zip은 2,167,750 bytes다. 상대 경로·SHA·크기·권한과
ZIP hash를 고정했다. ZIP 복원과 Git 재컴파일은 각각 전체 228개의 bytes·권한이 같다.
원래 cache와 격리 경로 읽기를 차단한 최종 재검증도 통과했다.

추가로 원래 source·Git 디렉터리·모델·runtime store·격리 경로를 모두 읽을 수 없는
실제 sandbox에서도 ZIP만으로 228개를 복원했다(ZIP-INDEPENDENT.json). Git 객체나
과거 compiler가 없어도 원본 cache bytes의 ZIP 복원은 가능하다.

Git 재컴파일 방식에는 잠근 source 객체와 과거 compiler가 필요하다. source commit
중 9개는 현재 main 조상 바깥의 보존된 refs에 있으므로 모든 새 clone에 자동으로
포함된다고 가정하지 않는다. 없으면 fetch하지 않고 실패하며 독립 ZIP 복원을 사용한다.
기존 Git refs나 다른 작업 트리를 변경·제거하지 않았다.

## 검증 결과

| 검사 | 최종 결과 |
|---|---|
| working 운영·검색·로컬 임베딩 계약 | 48개 PASS, 기준/A/B 부재 상태 |
| 실제 설치 H-F2 composition·lighting | 원래 lane 점수·전체 순위 동일, 1+1 호출 |
| H/native receipt와 구성 감사 | PASS |
| 일반 CLI issued view + 새 retrieve/view/compose-audit/deliver | 독립 임시 복사본에서 PASS |
| 과거/최신 저장 전체 순위 | 225 + 225 = 450개 PASS |
| 보존한 실험 테스트 | 17개 PASS |
| native·권한·workflow·복구 | 70개 PASS, 819.588초, skip 없음 |
| 새 복원·충돌·격리·삭제·기록 보존 안전성 | 22개 PASS |
| 기존 공용 복원·rollback·archive 안전성 | 15개 PASS, 동일 dependency 근거 재사용 |
| 최종 오프라인 복원 | ZIP/Git 각 228개 PASS |
| 원래 source·Git·모델·store 없는 ZIP 복원 | 228개 PASS |
| 최종 보호 파일·CURRENT | 138,959개 / CURRENT 168개 PASS |

A 25개와 B 203개는 각각 원래 경로가 없는 상태에서 회귀 검사를 통과했다.
격리본도 검증 프로세스가 읽지 못하게 하여 숨은 cache 의존성을 차단했다.
기존 native 9개 모듈은 범위를 줄이지 않고 최종 부재 상태에서 한 번 실행했다.

기존 검사 wrapper의 중첩 sandbox 제약을 발견해 새 검사 22개는 외부 sandbox로,
자체 subprocess sandbox를 가진 기존 15개는 원래 방식으로 확인했다.
초기 기록도 남겼고 실제 Git 누락 경로를 확인한 최종 안전성 근거를 사용했다.

회귀의 실제 실행 subprocess는 network·원래 프로젝트/운영 store 쓰기·이번 cache
및 격리본 읽기를 차단했다. fixture 준비는 검증된 launcher가 임시 독립 복사본으로
수행했다. 원래 CURRENT 변경은 0회이며 임시 fixture pointer 생성과 구분한다.
Gemini·새 로컬 임베딩 추론·이미지 생성·새 의미 판정은 모두 0회다.

마지막 전체 부재 검사와 같은 코드·입력·환경·차단 조건의 결과는 재사용했다.
정리 후 POLICY 단독 재검사도 통과했다. 이때 존재하지 않는 cache의 부재와,
같은 정책으로 실제 파일 읽기를 거부했던 기존 근거를 구분해 기록했다.

이 결과는 지정한 회귀·복원 범위의 성공이다. 과거 테스트 source 203개를 각각
실행하거나 역사 CLI 41건을 복구·전수 재생한 결과가 아니다. 새 요청의 의미 품질,
이미지 품질·외부 provider의 실서비스 결과를 새로 평가하지 않았다. 기존 HOLD
판정도 그대로 재현했다.

## 크기 해석

5,063,794 bytes는 원래 cache 파일의 논리 크기다. 복구 ZIP 약 2.17MB와
새 보호 기준선 7,778,651 bytes, 도구·검증 기록을 추가했다. 7단계까지 추적 트리
논리 크기는 10,780,619 bytes 증가했고, ignored cache 제거까지 반영한 논리 변화도
+5,716,825 bytes다. 마지막 문서·정산 기록은 이 수치에 추가된다(ACCOUNTING-08.json).

따라서 원래 cache 경로를 줄이고 복구 가능하게 보존한 작업이며 전체 디스크
사용량을 줄인 결과로 표현하지 않는다. APFS 공유 블록과 Git 객체까지 포함한
물리 확보 공간은 측정하지 않았다. Git GC/prune·이력 재작성은 하지 않았다.

## 단계별 커밋과 현재 상태

| 단계 | 결과 | 커밋 |
|---|---|---|
| 1 | 보호 기준선·228개 allowlist | `5e88145e7` |
| 2 | 참조·Git commit/tree/blob·정확한 재컴파일 | `de63b4239` |
| 3 | 독립 원본-byte ZIP·안전한 두 복구 경로 | `0a6eaa160` |
| 4 | 운영·설치·일반 CLI·archive 기준 | `9ee51f663` |
| 5 | A 25개 격리·부재 검증 | `255941479` |
| 6 | B 203개 격리·전체 부재 검증 | `20258f6fc` |
| 7 | native 70개·오프라인 복원·격리본 최종 제거 | `d330f19d3` |
| 8 | 최종 보존 확인·정산·결과·복원 안내 | 본 리포트를 포함하는 커밋 |

각 단계의 구현·검증 후 이번 경로만 커밋했다. ignored cache는 Git 삭제 diff가
아니라 경로 부재·journal·SHA·복구 검사로 증명한다. 실행 중 생성한 일회성
BATCH/FINALIZE `.LOCK`은 로컬 잠금으로 유지하며 ignore 규칙을 바꾸거나 force-stage하지 않았다.
원래 미커밋 작업은 그대로 남아 있으며 push는 수행하지 않았다.

복원·재검사 명령과 파일 설명은 같은 디렉터리 README.md를 따른다.

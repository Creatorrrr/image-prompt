# 슬롯별 독립 검색·필요 shard 적재 최종 리포트

계획의 1–9단계를 구현·검증하고 단계마다 별도 커밋했다. 착수 전 `origin/main`을 pull한 결과는 already up to date였다. 원격 main의 변경은 작업 기준에 이미 포함되어 있었다. 원본 후보·다대다 binding의 의도를 유지했으며 작업 전 수정되어 있던 다른 두 문서는 SHA까지 보존했다. [SYNC.json](SYNC.json), [EXECUTION.json](EXECUTION.json).

## 최종 동작

원본 후보 18,250개 중 positive 18,186개가 모든 슬롯의 공통 검색 공간이다. diagnostic 64개는 positive 검색에서 분리한다. 112개 관리 슬롯과 12,020개 persistent binding은 유지했다. 슬롯 태그나 binding 개수는 검색 상한이 아니다. 등록 태그가 없는 후보와 다른 태그 후보도 검색하고, 원래 guard·owner·effects·prerequisite를 유지하는 request-local 역할 제안을 만든다. 후보 payload·문서·벡터는 하나씩 소유하고 여러 슬롯의 역할 참조로 공유한다.

각 활성/지정 슬롯은 frozen core와 중립 슬롯 정의에 결합한 별도 쿼리로 **전역 BM25F + 실제 provider query embedding의 정확 cosine + RRF**를 실행한다. 슬롯별 두 lane 검색 이후에 unique 64개와 core/support 4/2개 표시 예산을 적용한다. 다른 슬롯의 상위 결과나 기존 tag로 후보 공간을 제한하지 않는다. 운영 hybrid에서 embedding 실패는 오류이며 keyword-only는 명시적 진단이다.

초기에는 compact source/routing metadata를 읽는다. 검색에는 필요한 posting page, 선택 payload, 정확 vector extent만 읽는다. 모든 영역을 routing 대상으로 두고 증명 가능한 상한 아래의 영역만 생략한다. 근사 벡터는 routing certificate용이며 최종 점수는 원래 float64 값이다. 상한이 약한 경우 전체를 순차 읽어도 정확성을 유지한다. 본문 cache는 64MiB, vector descriptor는 최대 64개다. Metadata와 전체 프로세스 RSS는 본문 cache 상한과 별도다.

운영 계약은 pack V8, slot-query-set V1, slot retrieval V2, composer view V4, generation/CURRENT/issued receipt V3다. 새 maintenance builder는 현재 native layout만 검증·재사용하며 source/index 전부 검증 후 active manifest와 generation을 게시한다. 요청 acquisition이나 감사가 인덱스를 자동 재생성하거나 eager 전체 스캔으로 fallback하지 않는다.

## 검증 결과

| 검사 | 결과 | 근거 |
|---|---|---|
| 112 슬롯 × 한국어·영어 | 실제 쿼리 224개, 두 lane/RRF 전체 스캔과 순위·점수 차이 0건 | [MATRIX.json](stage08/MATRIX.json) |
| 자연 요청 20건 | 독립 슬롯 쿼리 1,366개; 원래 필수 의무·hard gate와 정확 검색 대조 통과 | [NATURAL.json](stage08/NATURAL.json) |
| Provider 실행 | query context 총 1,590개, 정확 cache 재사용 제외 신규 호출 1,544회; 문서 재임베딩·이미지 호출 0회 | [QUALIFICATION.json](stage08/QUALIFICATION.json) |
| 레거시 삭제 후 재생 | 실제 224개 쿼리의 두 lane/RRF 순위 차이 0건; 신규 provider 호출 0회 | [POST-REMOVAL-REPLAY.json](stage09/POST-REMOVAL-REPLAY.json) |
| 공개 native 흐름 | 찻잔·골렘 각 46슬롯; source/view/compose/render preflight와 새 worker의 issued receipt 완전 재생 통과; 이전 receipt 거부 | [PUBLIC-FLOW.json](stage09/PUBLIC-FLOW.json) |
| 최종 전체 회귀 | **344 tests + 309 subtests 통과**, 631.66초 | [FINAL-REGRESSION.log.gz](stage09/FINAL-REGRESSION.log.gz) |
| 최종 무결성·보존 | active closure 722개 게시 SHA 대조, 제거 파일 부재, 운영 legacy 참조 0건, 다른 두 문서 SHA 보존 | [FINAL-INTEGRITY.json](stage09/FINAL-INTEGRITY.json) |

합성 벡터 단위 검사, 실제 provider 실행, 독립 전체 스캔, source/guard 보존, render preflight를 각각 구분했다. source 변경·같은 mtime의 변조·missing shard·cache eviction·게시 경쟁·최악의 전체 streaming도 테스트했다. 최종 전체 회귀는 코드 수정을 멈춘 뒤 실행했다. 변경 중 freshness 거부 및 evaluator 수정 전 실패 로그도 byte-exact로 보존한다.

## 성능과 한계

새 cold Reader는 metadata 약 22.18MB만 읽고 posting/vector/payload 본문 읽기 0건으로 시작한다. 측정 startup은 1.614초, peak RSS는 약 607MB로 기존 eager의 15.169초·약 1,440MB 대비 개선됐다. 최종 게시 acquisition에서도 본문 읽기 0건을 확인했다. 디코딩 metadata JSON은 약 73.46MB이며 Python 객체/RSS와 압축 파일 크기는 다르다.

3,850개 논리 vector leaf를 61개 물리 파일의 seekable extent로 저장한다. 실제 query 모두 일부 vector 영역을 생략했고, **동일한 최종 인덱스 전체 읽기 대비** 선택 vector 바이트 절감 중앙값은 45.6%다. 대표 쿼리별 3회 중앙값의 최대 검색 시간 비율은 전체 스캔 대비 1.182로 고정 기준 1.2를 통과했다. OS cache를 강제로 비우지는 않았고 API·metadata acquisition 시간은 이 비교에서 제외했다. 단일 표본의 초과 결과도 보존했다. [MEASURED-GATES.json](stage08/MEASURED-GATES.json), [PERFORMANCE-REPEATED.json](stage08/PERFORMANCE-REPEATED.json).

원래 float64를 직접 보존해 CPU 비용을 줄이는 대신 저장량이 커졌다. 선택 vector 바이트 중앙값 50,756,537은 이전 gzip JSON vector 전체 50,082,818보다 **1.3% 크다**. 따라서 기존 저장 형식보다 절대 vector 읽기 바이트가 줄었다고 주장하지 않는다. 독립 다중 슬롯 검색은 이전 단일 검색보다 계산이 많고, 공개 compose·preflight·새 worker 재생을 포함한 두 전체 흐름은 각각 186.32초·265.32초였다.

슬롯별 검색 실행과 정확성은 검증했지만 **슬롯별 의미 precision/recall은 완전 통과 판정이 아니다**. 중립 slot focus보다 core 문맥이 강해 영어 찻잔 사례의 112개 중 69개가 같은 top1이었다. source tag와 hash·API 실행을 의미 정답으로 사용하지 않으며 `review_required` 및 context blocked 상태를 유지한다. 선택적 후보를 전부 거절해도 필수 의미는 유지된다. [SEMANTIC-REVIEW.json](stage08/SEMANTIC-REVIEW.json).

이미지 생성/native pixel/사용자 미적 판단 및 실제 remote-before-retrieval 운영 재생은 실행하지 않았다. 로컬 게시·검색·감사 증거다.

## 운영 전환과 정리

새 layout `b5f6d42a235758dd446a30fa3c9a4ee7f2aff4b4e639a4bdd207fa34a5c233d0`에서 positive vector 18,186개를 모두 재사용했고 provider 호출 0회로 완전 검증했다. 공통 corpus SHA `fe4ebca755666de3c0656676295ed75b72a0210d73a64aead9d626c6b57493c9`는 보존했다.

최종 로컬 generation은 `6028917cf30299b9996122cbfdc1d49ea925e66fa6331c3b777c06f87beb1d12`, source fingerprint는 `7b25395267ba255fceaacc4c90f89e20f8ebf988de775402f84152636787f574`다. 이전 frozen query/단일 검색 후 tag 분배/eager loader/monolithic BM25F cache/old query·receipt adapter를 운영에서 제거했다. 오프라인 full-scan oracle만 build·평가 전용으로 남겼다.

이전 manifest 및 이 작업에서 만든 이전 namespace의 정확한 member 17,763개, 744,517,045바이트를 SHA 검증한 backup tar로 보존한 후 삭제했다. active closure 722개, authored source, fixtures, 역사 evidence와 다른 작업을 보호했다. 이전 local CURRENT도 namespace를 특정해 백업 후 제거했다. 과거 generation과 Git 이력은 복구·증거용이며 운영 호환 경로가 아니다. [REMOVAL-LEDGER.json](stage09/REMOVAL-LEDGER.json), [OLD-CURRENT-RETIREMENT.json](stage09/OLD-CURRENT-RETIREMENT.json).

## 단계별 커밋

| 단계 | 커밋 | 완료 내용 |
|---|---|---|
| 1 | `ca37146c` | 동결 기준·독립 oracle·I/O gate |
| 2 | `d1760079` | 슬롯 쿼리·역할 제안 계약 |
| 3 | `63fcf6fd` | 전체 검색 layout·통계·경계 |
| 4 | `0d41a411` | lazy reader·source applicability |
| 5 | `710daae3` | 정확 BM25F/cosine·certified pruning |
| 6 | `b0ac5acd` | 독립 슬롯 실행·공정 표시 예산 |
| 7 | `b3429a8a` | native workflow·view·issued receipt·audit |
| 8 | `b276b5bd` | 실제 112슬롯/자연 요청·성능·전체 회귀 |
| 9 | 이 리포트를 포함한 커밋 | native 게시·레거시 제거·삭제 후 전체 검증 |

9단계 커밋 제목은 `refactor(photo): retire single-query and eager production retrieval`다. 커밋 자신의 SHA를 문서에 자기 참조하지 않으며 Git 이력과 최종 응답에서 확인한다. 이번 요청의 변경은 로컬 main에 커밋하며 push는 실행하지 않았다.

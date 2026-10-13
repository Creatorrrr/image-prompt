# 9단계 — 새 운영 게시와 이전 경로 제거

공통 후보풀 원본은 그대로 유지했다. 새 native layout만 재사용하는 유지보수 빌더가 positive 18,186개 벡터를 전부 재사용했고 provider 호출 0회로 새 layout `b5f6d42a235758dd446a30fa3c9a4ee7f2aff4b4e639a4bdd207fa34a5c233d0`을 완전 검증했다. 운영 기본 계약은 pack V8, slot-query-set V1, slot retrieval V2, composer view V4, generation/current/receipt V3다.

단일 frozen query 모듈을 삭제했다. 기존 전체 index loader/writer, 모놀리식 BM25F cache store, eager shared views loader와 단일 core 검색 후 tag 분배 함수를 제거했다. 운영 코드에는 이전 query/schema reader나 fallback이 없다. positive-document projection, 전체 lexical/vector oracle와 `offline_vector_map`은 오프라인 build/qualification용으로만 남겼다. runtime audit는 필요한 posting/vector 점수와 전체 routing tree 생략 증명을 검증한다.

새 view는 persistent binding 유무와 관계없이 실제 request-local target slot을 표시한다. 각 후보 상세에는 원본 binding과 역할 제안의 conditions/effects/applicability를 제공한다. 후보 payload는 계속 한 번만 소유하며 역할 참조로 공유한다.

## 정확한 정리와 복구

REMOVAL-LEDGER.json에 manifest 및 이 작업에서 생성한 namespace별 정확한 파일 목록·SHA·크기를 기록했다. 17,763개, 744,517,045바이트를 백업 tar로 저장하고 모든 member SHA를 비교한 뒤 삭제했다. active manifest closure 722개, authored modules, fixtures, 역사 evidence와 다른 작업 파일은 보호했다. 임의 디렉터리 전체 삭제나 ignore를 사용하지 않았다. Git 이력과 workspace-backups의 검증한 tar로 복구할 수 있다.

root의 이전 namespace V1/CURRENT V2도 정확히 특정해 백업 후 active pointer를 제거했다. 이전 generation은 역사 자료로 보존하며 새 runtime에서 읽거나 호환하지 않는다. 다른 namespace는 건드리지 않았다.

## 삭제 후 검증

- POST-REMOVAL-REPLAY.json: 실제 영어·한국어 224개 slot query를 재생하고 8단계 독립 전체 스캔 결과와 SHA를 대조했다. 두 lane/RRF 순위 차이 0건, 신규 provider 호출 0회.
- SOURCE-VALIDATION-FINAL.log.gz: 후보 18,250개와 binding 12,020개에서 errors 0건. 파생 layout도 source/TF/DF/벡터/extent closure/quantization residual을 완전 검증했다.
- PUBLISHED-COLD-START.json: 게시된 CURRENT를 별도 provider로 acquired했을 때 metadata만 읽고 payload/posting/vector 본문 읽기 0건.
- PUBLIC-FLOW.json 및 public/: 실제 private query context를 사용하는 찻잔·골렘 pack, source audit, native view, compose audit, render preflight와 fresh worker의 issued receipt 완전 재생. 이미지 호출 0회. 이전 receipt 거부도 확인한다.
- MAINTENANCE-TESTS.log.gz / WIRE-REPLAY-TESTS.log.gz: retag 시 vector 전부 재사용, text 변경 1건만 embed, source race 시 active pointer 보존, cold 읽기/변조/epoch와 실제 직렬화 회귀.
- FINAL-REGRESSION.log.gz: 구현을 고정한 최종 전체 사진 회귀 검사에서 **344 passed, 309 subtests passed**, 631.66초. 변경 중 실행한 이전 실패 로그도 보존했으며 이전 실패를 pre-existing으로 처리하지 않았다.
- FINAL-INTEGRITY.json: 최종 CURRENT V3의 722개 active closure 파일을 게시 member SHA와 다시 대조했다. 제거 member 17,763개 부재, 운영 legacy 참조 0건, 운영 문서의 이전 pack/retrieval/receipt 참조 0건, 작업 전 다른 두 문서의 SHA 보존을 확인했다.

최종 generation은 `6028917cf30299b9996122cbfdc1d49ea925e66fa6331c3b777c06f87beb1d12`, source fingerprint는 `7b25395267ba255fceaacc4c90f89e20f8ebf988de775402f84152636787f574`다. 찻잔·골렘 공개 compose/render-preflight/fresh-worker 흐름은 각각 46개 슬롯을 독립 검색했고 모두 통과했다. 전체 흐름 시간은 각각 186.32초와 265.32초이며 반복 감사·새 worker 재생을 포함한다. 이를 단일 검색 latency로 사용하지 않는다.

8·9단계의 텍스트 로그는 원본 SHA와 바이트 수를 `LOG-ARCHIVE-LEDGER.json`에 기록해 gzip으로 보존했다. 압축 해제 결과는 원본과 byte-exact이며 실패 로그도 포함한다.

파일 재생에서 creative-controls 설명문 순서가 JSON mapping 순서에 의존한 문제가 드러났다. 원래 managed control 표시 순서를 고정해 값과 기존 SHA를 유지했으며 canonical wire roundtrip을 검증했다. snapshot을 재해석하거나 원래 control 수준을 바꾸지 않는다.

## 증명 범위

운영 기본값을 로컬에서 게시했다. 이미지 생성·native pixel·사용자 미적 판단은 이 작업 범위에서 실행하지 않았다. 8단계에서 확인한 core 문맥 우세/slot별 의미 적합성 한계는 계속 적용된다. 정확한 검색·무결성·guard 보존을 역할별 의미 recall의 완전한 통과로 주장하지 않는다. remote-before-retrieval의 실제 원격 운영 재생은 이번 로컬 게시 증거에 포함하지 않는다.

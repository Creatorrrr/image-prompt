# Photo Prompt Residual Runtime Boundary and Legacy Cleanup Goal

- 작성: 2026-08-12 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@4acba60c4424532ce957da345ad333ef02297f4c`
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: 현재 구현의 모든 기능을 유지하면서, 이번 메타데이터 경계 개편 뒤 남은 비시각적·출처 지향 데이터와 쓰이지 않는 레거시를 다시 확인해 무리하지 않는 범위에서 정리한다.
- 최종 제품/결과: candidate-pack의 공개 composition evidence, soft semantic scoring, 장면 원자, 최종 프롬프트에는 사용자 의도와 관찰 가능한 시각 정보만 참여하고, 비시각적 연구·시장·프로세스 제어는 명시적 private/control 경계에만 존재한다. audit·재현에 필요한 typed contract/provenance는 렌더링 evidence와 분리하고, audited composed JSON의 provenance는 API 이미지 실행 ledger까지 손실 없이 전달한다. 확인된 dead code와 stale 문서/캐시는 제거된다.
- 범위: candidate-pack 공개 투영과 semantic facet scoring의 제어 facet 분리, `market term nonvisual` 및 권리/연구 과정형 시각 텍스트 정제, API ledger 전달 누락과 retry 연결, 확인된 무참조 코드·상수·schema/caches 점검, stale 보고서 경로와 lifecycle 갱신, 필요한 semantic index 증분 재생성.
- 비목표: candidate-pack v3 전면 재설계, stable ID 일괄 rename, 외부 consumer가 사용할 수 있는 호환 분기 제거, 새 연구 수집, holdout 기준 완화, 이미지 생성·픽셀 품질 주장, 배포·push·PR, 별도 evaluator/artifact family 도입.

## 진척 계약

- 진척으로 인정: 실제 후보팩/선택/최종 프롬프트/API ledger 동작의 변경, 사용되지 않는 런타임 코드·데이터의 안전한 제거, 변경된 semantic text에 한정한 유효 index 갱신.
- 진척으로 인정하지 않음: 문서·테스트만 추가, 내부 문자열을 다른 출처명으로 치환, private 키를 계속 semantic score에 사용, API 호출 없이 ledger 계약만 설명, 사용 여부를 증명하지 않은 호환 코드 삭제.
- 검증-only 작업 상한: 제품 단계마다 focused 검증 1회, 최종 affected regression과 기존 검증 경로 1회. 기존 경로로 확인할 수 있으면 새 verifier/schema/artifact family를 만들지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, matching failure report 우선 갱신, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker`.

## 기준선과 미지수

- 현재 기준선: `4acba60`은 6,513-entry `semantic-text-v3`, 16개 current shard, candidate relevance 화이트리스트, 연구/fixture 패키지 분리를 포함하며 focused photo 316/316, scene 112/112, contradiction 667/667을 통과했다. 전체 526개에는 unrelated universal-scene 11 failures/1 error가 남아 있다.
- 재현된 잔여 결함: 기준선의 CJK character scene action은 이미 관찰 가능한 caring handoff와 reciprocal gaze로 정제되어 최종 프롬프트 literal 누출은 해소됐다. 그러나 같은 current pack의 candidate tag와 character grammar에는 `market_label_nonvisual`, `market_label_nonvisual_guard`, raw market/audience control metadata가 남아 있다. 일부 candidate facets에는 `content_basis`, `authorship_basis`, `market_origin`, `term_level`, `audience_scope`, `manifestation_mode`, `character_moe_grammar` 같은 control 정보가 남아 있다.
- 구조적 잔여: `content_basis`는 pack에서 숨겨졌지만 generic facet score에는 참여한다. `rights-cleared`/`copyrighted` 같은 법적·과정형 문구가 일부 semantic/public visual text에 남아 있다.
- 실행 경로 잔여: `generate_images_via_api.py`가 audited composed JSON의 `pack_id`, chosen IDs, composer, audit status, augmentation brief와 retry link를 ledger recorder에 전달하지 않는다. 무참조 함수 9개와 상수 1개, 무참조 ledger schema 및 생성 cache는 현재 사용 여부를 재확인한다.
- 고정 호환 경계: candidate-pack v2 shape와 stable IDs, `concept_mode=legacy`, custom/partial checkpoint loader, legacy score trace/fallback, slot fallback은 외부 호환 가능성이 있어 직접 사용 증거 없이 제거하지 않는다.
- 외부 전송 가정: 사용자는 새 payload hash와 Gemini 전송을 사전 승인했다. 전송 전 ordered payload의 count, UTF-8 byte size, SHA-256을 고정하고 기록한다. text-hash cache로 unchanged vectors를 재사용하며, 증분 방식이 index order/dimension/품질을 보장하지 못할 때만 전수를 전송한다.
- 적용 보고서:
  - `docs/failed-reports/2026-08-11-photo-runtime-metadata-contamination.md`: 현재 forward 재현이 기존 resolved 범위를 반박하므로 같은 failure lifecycle을 갱신하고 public/control 경계를 확장한다.
  - `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`: Gemini는 검증된 batch size 1과 cache/checkpoint 경로만 사용한다.
  - `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`: typed polarity, no-people, exact subject, negative bytes와 기존 공개 기능을 보존한다.
  - `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`: literal routing contract와 실제 semantic retrieval 근거를 분리하고 stale unknown/lifecycle을 갱신한다.
  - `docs/failed-reports/2026-08-08-character-moe-research-provenance-overclaim.md`: 연구 출처의 이름이 아니라 관찰 가능한 결과와 typed control만 runtime에 반영한다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 잔여 경계 고정 | matching failure report를 reopened 상태로 갱신하고, 대표 pack·score·prompt·API ledger·dead-ref 기준선을 고정한다 | 고정 seed CJK forward 재현, facet score probe, fake API/recorder probe, AST reference scan | 이미 해결된 final-prompt 누출과 남은 pack/score 누출을 구분하고 제거/보존/비공개 항목과 외부 호환 경계가 코드 증거로 확정됨 |
| 2. 공개 시각 경계 수리 | control-only facets/tags를 agent-visible pack과 semantic facet score에서 제외하고, scene atom의 비시각적 시장/정책 문구를 관찰 가능한 행동으로 바꾼다 | 대표 일반/CJK packs와 audit, control facet 가감 score parity, forbidden public-text scan | audit PASS prompt와 public pack에 비시각 control 문구 0건, 명시 route/scene 기능 유지 |
| 3. API 실행 계약 수리 | audited composed JSON의 pack provenance, chosen IDs, composer, audit status, augmentation brief와 retry link를 ledger recorder에 전달한다; 무참조 schema는 실제 검증에 연결하거나 안전하게 제거한다 | network-free fake image/recorder unit test와 exact prompt/negative byte assertion | 성공·실패·retry ledger가 문서 계약대로 기록되고 기존 CLI 사용법 유지 |
| 4. dead legacy와 문서 정리 | 정적·동적 무참조가 확인된 함수/상수와 생성 cache를 제거하고 stale fixture 경로/lifecycle을 갱신한다 | AST/load scan, `rg` reference scan, focused import/CLI tests | 기능 호환 분기는 유지되고 확인된 dead path와 stale path가 남지 않음 |
| 5. 증분 semantic 갱신과 최종 자격 | 변경 semantic text만 batch size 1로 임베딩하고 unchanged vector를 재사용해 새 manifest/shards를 원자적으로 기록한다 | payload count/bytes/hash, reuse/sent counts, check-index, retrieval/generalization/holdout, affected photo tests, scene/contradiction/diff checks | 모든 최종 기준 통과, current generation 하나, unrelated full-suite 기준선보다 악화 없음 |

## 최종 완료 기준

1. public candidate-pack의 시각 label/facet/tag/evidence, semantic relevance/score, mandatory visual atom, 최종 prompt에 연구 출처명·시장 라우터·법적/개발 과정형 비시각 문구가 0건이다. v2 호환을 위해 유지한 stable selection ID와 internal hard-guard 값은 이 조건에서 제외하되, label·semantic text·soft score·최종 prompt에는 참여하지 않는다.
2. control-only facet을 추가·제거해도 semantic score와 선택 결과가 바뀌지 않으며, 공개 visual facet과 명시적 route 기능은 유지된다.
3. 고정 CJK forward 사례가 같은 character route/atomic scene 기능을 유지하면서 audit PASS하고 `market term nonvisual` 또는 동등한 내부 제어문을 렌더링하지 않는다.
4. explicit API path가 prompt/negative bytes를 보존하고 pack provenance, chosen IDs, composer, audit status, augmentation brief, attempt/retry 관계를 ledger에 전달한다.
5. 정적·동적 무참조가 확인된 코드/상수/asset만 제거되고 deliberate legacy/custom compatibility 경로는 regression coverage와 함께 유지된다.
6. 새 semantic index는 exact logical order, 768 dimensions, manifest/shard hash/count를 통과하며 unchanged vectors를 재사용한다. 전송 payload의 count/bytes/SHA-256과 실제 sent/reused 수가 일치한다.
7. focused photo suites, dictionary, index, scene-expression, contradiction, generalization/holdout/retrieval 검증이 통과하고 unrelated full-suite 기준선보다 악화되지 않는다.
8. matching failed report와 stale execution-knowledge 경로/lifecycle이 현재 증거와 일치하며, 이미지 품질이나 외부 consumer 호환을 검증하지 않은 범위는 정직하게 남긴다.

## 완료 결과

- 공개/제어 경계: `authorship_basis`, `audience_scope`, `character_family`, `character_topic`, `content_basis`, `cultural_provenance`, `market_origin`, `safety_tier`, `term_level`은 내부 control/schema에 유지하고 public facet 및 soft semantic facet score에서는 제외했다. generic hard-guard matcher는 이 값을 읽을 수 있지만 현행 in-repo guard 소비자는 `safety_tier`뿐이다. preset-family routing ID, adult-eligibility/structural character-scene tag와 비시각 graph tag, router/policy/guard/edge 정보도 public composition evidence에서 제거했다.
- 시각 데이터: semantic/public text의 `rights-cleared`, `copyrighted`, 권리·개발 상태 표현 11건과 CJK 시장 비교·audience 우선순위 표현 2건, direct-only 호환 preset의 `legacy ... retained` 설명 1건을 관찰 가능한 오리지널 그래픽·제작 행위·조명·장면 표현으로 바꿨다. named source, 국가 시장 비교, audience 우선순위 marker는 validator와 semantic-input 검증으로 차단한다.
- 실행 계약: explicit Images API helper가 exact prompt/negative bytes, pack ID, chosen IDs, composer, audit status, augmentation brief, 원래 argv를 ledger에 전달하고 반환된 run ID로 다음 시도를 연결한다. recorder 실패는 성공으로 가장하지 않고 fail closed한다.
- dead legacy: 정의·호출 및 repository reference가 모두 0인 함수 9개와 상수 1개를 제거했다. 마지막 재검사에서 비활성 character grammar의 빈 `policy_ids`, 공개 preset candidate의 내부 `family`, `runtime_nodes[].role`과 중복되던 공개 `primary_runtime_id`도 제거했다. stable IDs, `concept_mode=legacy`, monolithic/custom/partial index loader, score trace/fallback, direct preset 호환은 사용 증거 또는 외부 호환 가능성이 있어 유지했다.
- Gemini 증분 갱신: 1차는 11 ordered texts / 6,273 UTF-8 compact-JSON bytes / SHA-256 `cb58ebd6d01cdfd1f726f7397bb2e233345f2df3733a2f538f2c8d8e8ee25f96`, 2차는 CJK 변경분 2 ordered texts / 1,832 bytes / SHA-256 `700534e3a600587f4a1dbfcfe55fa7f581ef9c5c3ad0f6f7ae1161ecdcbe1d30`만 각각 batch size 1로 전송했다. 2차 직전 index의 6,511개를 재사용했고, 기준선 대비 누적 logical delta는 13 texts / 8,104 bytes / SHA-256 `0a7c856660c899448851606258cf7dc20887e98695358e970fbd851bbd29450c`다. 최종 대조에서 6,500 baseline vectors가 byte-identical, 13개만 변경됐으며 추가·삭제는 0건이다.
- 최종 index: dictionary SHA-256 `76b4f712fb5bdd8aaf868853a0d59552aa815085da66e64ce5e6530cc9c196ca`, generation `76b4f712fb5bdd8a`, `semantic-text-v3`, `gemini-embedding-2`, 768 dimensions, 6,513 entries, 16 hash-valid shards, current generation 1개, partial checkpoint 0개다.
- 검색 자격: global real retrieval 22/22는 71 ordered requests / 68 unique texts / 6,381 bytes / SHA-256 `5702e85ca1e2d2d14a5a921438a89cd9dd19ab667dd4b2b87be497e730398040`을 사용했다. 1차 변경 경로 probe 3/3은 12 ordered requests / 812 bytes / SHA-256 `95d0c71bd372ce816342b1b7423f8818cc033117c5290606bc0e80e86d47d413`, 2차 CJK 던전 방송 probe 5/5는 중복 없는 17 ordered requests / 1,430 bytes / SHA-256 `31ac2034764ae6abf68fe4aef6db1a954c24311c2af3a4665718eff1aa756c1a`을 사용했다.
- 로컬 검증: affected photo full suite 319 tests + 597 subtests가 통과했다. 마지막 중복 `primary_runtime_id` 공개 제거 뒤에는 최종 candidate-pack/audit 계약 45 tests와 667 preset 공개 projection 전수 스캔을 다시 통과했다. dictionary/index, scene-expression 112/112, contradiction 667/667 및 violation 0, generalization 79/79, frozen holdout 24/24, domain holdout v2 6/6도 통과했다. 나머지 repository tests는 앞선 동일 범위 실행에서 206 tests + 1,134 subtests가 통과했고 12개 non-pass는 기존 universal-scene 기준선과 같은 범위여서 photo 회귀는 없다.
- 정직한 한계: 이미지를 새로 렌더링하지 않아 pixel 품질을 주장하지 않는다. repository 밖 candidate-pack/raw-asset consumer는 확인하지 못했다. character multilingual 96-case는 literal routing contract이며 독립 semantic holdout은 아니다. `aligning_rights_cleared_original_vehicle_wrap`, `rights_cleared_original` 같은 stable ID/control 값은 v2 호환을 위해 내부 선택 핸들로 남는다. `applicability.source`, selected-blueprint `source`, typed intent source처럼 audit 분기에 실제 사용되는 비리서치 provenance 필드도 visual evidence와 분리된 채 유지한다. raw authoring asset의 `market_origin`·`cultural_provenance`·`term_level` 등 8개 비-safety control facet과 character-scene `audience_familiarity`/`market_origin`은 공개/semantic/hard-guard 경로에는 참여하지 않지만 schema와 외부 raw-asset 호환성 때문에 남긴 v3 제거 후보이다. in-repo auditor가 직접 읽지 않는 quality-layer `source` trace와 public character topic/family/domain IDs도 외부 v2 consumer 증거가 없어 이번에 삭제하지 않은 차기 versioned-cleanup 후보다.

## 검증 수준과 예산

- 위험 수준: ordinary offline refactor + 승인된 bounded external embedding refresh.
- 반복 중 focused 검증: 수정 경로별 unit/contract test, 대표 fixed-seed pack/audit, dictionary validator.
- 최종 검증: affected photo tests, index integrity와 실제 retrieval, generalization/holdout, scene/contradiction, reference/forbidden scan, `git diff --check`를 각 한 번 수행한다.
- 외부 전송: 변경된 semantic text exact payload만 우선 사용한다. SDK cardinality가 보장된 batch size 1을 유지하고 API key는 출력·커밋하지 않는다. 증분 cache의 dimension/model/order parity가 깨질 때만 승인 범위 내 전수 재생성한다.
- 이미지 생성·pixel review: 이번 text/control/API-ledger 경계 목표의 필수 증거가 아니므로 수행하지 않는다.
- 검증 확장 전 질문 조건: stable ID 또는 candidate-pack major version 변경, 새로운 유료 서비스, 외부 consumer migration, 별도 평가 캠페인이 필요해질 때만 중단하고 질문한다.

## 중단 조건과 실행 지식

- 같은 원인의 제품 실패가 두 번 반복되면 세 번째 verifier를 만들지 않고 matching failure report를 갱신한 뒤 설계를 바꾸거나 사용자에게 질문한다.
- 기존 public ID/field 삭제가 불가피하거나 호환 동작과 오염 방지가 충돌하면 임의로 major schema를 올리지 않는다.
- semantic payload가 고정 후 다시 바뀌면 새 count/bytes/hash를 계산해 기록하고 최신 payload만 전송한다. partial checkpoint와 이전 current manifest는 새 manifest가 durable하기 전 삭제하지 않는다.
- 보고서에는 credential, token, raw vector, 민감 endpoint를 저장하지 않는다. exact payload는 semantic text 목록의 hash/count/bytes와 sanitised category만 기록한다.
- material failure는 재시도 전에 기존 matching report를 우선 갱신한다. 성공 보고서는 모든 기준 통과 후 기존 material failure 해결, 실패한 기본안의 비자명한 대안, 또는 비싸게 재구성되는 필수 절차 중 하나일 때만 최대 1건 작성한다.
- lifecycle 링크는 양방향으로 같은 변경에서 갱신하고, 보고서는 진척이나 별도 checkpoint가 아니다. 현재 소스와 직접 증거가 과거 보고서보다 우선한다.
- 실행 지식 보고서: 갱신 대상 `docs/failed-reports/2026-08-11-photo-runtime-metadata-contamination.md`, `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`; 완료 시 기존 passed report 갱신 또는 자격을 충족하는 새 passed report 최대 1건.

## Codex 실행 계약

- 각 checkpoint는 setup 이후 실제 product delta를 남긴다. 테스트·문서·schema만으로 목표를 완료하지 않는다.
- 최종 보고에는 기준선 commit, 실제 변경, exact Gemini payload와 reuse/sent 수, 완료 기준별 pass/fail, 실행 지식 경로, 남은 검증 한계를 포함한다.
- 범위·완료 기준·검증 예산을 자동으로 확대하지 않는다.

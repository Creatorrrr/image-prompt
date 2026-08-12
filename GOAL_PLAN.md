# Photo Prompt Candidate-Pack v3 Conservative Metadata Retirement Goal

- 작성: 2026-08-12 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@c2b3600`
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: 이번 개편 뒤 남은 v3 정리 후보를 전체 기능과 호환 경계를 보존하는 범위에서 정리하고, 스킬의 실질 기능과 무관한 출처·연구·시장·분류 흔적이 런타임 데이터나 공개 후보팩의 판단을 편향하지 않게 한다.
- 최종 제품/결과: 기본 candidate-pack v3와 주 authoring assets에는 렌더링·선택·안전·감사에 쓰이지 않는 control/source/taxonomy 필드가 없고, 공개 캐릭터 문법과 compatibility handle은 중립적인 이름을 사용한다. 명시적 v2 compatibility 모드는 기존 pack·선택·prompt 계약을 유지하며 실제 safety guard와 typed runtime provenance는 계속 동작한다.
- 범위: 미사용 raw control facet 8종과 character-scene audience/market 필드 제거, 관련 schema/validator 정리, candidate-pack v3 공개 projection, v2 compatibility mode, 비기능 source trace 제거, 제한된 내부 key rename, 중립 공개 alias, semantic index text-hash 재사용과 무전송 검증.
- 비목표: `safety_tier` 또는 실제 audit/selection provenance 제거, `concept_mode=legacy`·monolithic/custom/partial index·score/fallback·direct preset 호환 경로 제거, research-evidence/history 문서 삭제, semantic wording 개선, 새 리서치·이미지 생성·픽셀 품질 주장, 외부 배포·push·PR, 새 evaluator/service/artifact family 도입.

## 진척 계약

- 진척으로 인정: raw/runtime 데이터의 실제 제거 또는 rename, v3 pack shape와 기본 동작 변경, v2 compatibility adapter, consumer 근거에 따른 명시적 보존 결정, unchanged semantic vector의 새 manifest 재사용.
- 진척으로 인정하지 않음: 문서·테스트만 추가, 출처명을 다른 출처명으로 치환, 실제 consumer를 확인하지 않은 기능 필드 삭제, v3를 구현하지 않은 채 후보 목록만 재분류, 기존 검증기로 확인 가능한 사항을 위한 새 verifier 제작.
- 검증-only 작업 상한: 초기 baseline/consumer audit 1회 뒤 각 제품 단계당 focused 검증 1회, 마지막 affected regression/index 검증 1회. 검증-only checkpoint를 두 번 연속 만들지 않는다.
- 실행 지식 작업 상한: metadata-first로 관련 보고서 전문 최대 5건, matching report 우선 갱신, 성공 보고서 기본 최대 1건, 보고를 별도 checkpoint로 만들지 않는다.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker`.

## 기준선과 고정 결정

- 현재 기준선: `c2b3600`의 candidate-pack v2, 6,513-entry `semantic-text-v3`, 768 dimensions, 16 current shards, focused photo 319 tests + 597 subtests, scene 112/112, contradiction 667/667, generalization 79/79, holdout 24/24, domain holdout 6/6이다. unrelated universal-scene 12 non-pass는 별도 기준선이다.
- raw 잔여 후보: `authorship_basis`, `audience_scope`, `character_family`, `character_topic`, `content_basis`, `cultural_provenance`, `market_origin`, `term_level`과 character-scene `audience_familiarity`/`market_origin`은 public/soft-score에서 이미 제외되었고 현행 in-repo guard consumer가 없다. `safety_tier`는 실제 hard guard consumer가 있으므로 유지한다.
- v3 공개 잔여 후보: character grammar의 `domain`/`topic_id`/`family_id`, `quality_profile.source`, craft/final-touch `source`, 내부 inventory 연결용 `source_preset_id`, `character_moe_grammar` 공개 profile 이름, `aligning_rights_cleared_original_vehicle_wrap` 공개 selection handle이다.
- 보존 대상: `applicability.source`, selected render/scene binding `source`, typed intent source, audit/ledger provenance처럼 실제 분기·감사 consumer가 읽는 값은 이름만 보고 제거하지 않는다.
- 호환 결정: v3를 user-facing 기본 candidate pack으로 만들되 `--candidate-pack-version v2`와 programmatic v2 option을 유지한다. v2 모드는 기준선과 같은 선택·prompt/negative·pack shape를 내야 한다. 저장된 historical artifacts는 수정하지 않는다.
- semantic 결정: raw control과 공개 projection만 바꾸므로 ordered semantic text 6,513개는 byte-identical이어야 한다. dictionary hash가 바뀌어도 text hash로 모든 vector를 재사용한다. miss가 1개라도 생기면 count/bytes/SHA-256과 원인을 고정하고 Gemini 호출 전에 중단한다.
- 관련 과거 실행 보고서와 적용 교훈:
  - `docs/failed-reports/2026-08-11-photo-runtime-metadata-contamination.md`: source/control 이름을 semantic/public evidence로 되돌리지 않고 deferred raw/v3 boundary만 처리한다.
  - `docs/passed-reports/2026-08-12-photo-runtime-boundary-and-api-ledger.md`: safety와 typed provenance를 visual projection과 분리한 현재 계약을 보존한다.
  - `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`: prompt/negative bytes, exact subject, polarity, no-people와 selection 의미를 고정한다.
  - `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`: rebuild가 필요해도 text-hash cache와 검증된 batch-size-1 경로만 쓰며, 이번 목표에서는 zero-send를 우선한다.
  - `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`: multilingual route aliases는 literal routing contract이므로 public profile rename과 분리해 보존한다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. v2 기준선과 consumer 경계 고정 | 대표·전수 v2 pack의 selection/prompt/negative/정규화 hash를 고정하고 후보 필드를 remove/rename/retain으로 코드 소비 근거와 함께 확정한다 | repository reference/AST scan, fixed-seed baseline digest, 대표 audit | 각 후보의 live consumer와 v2 호환 책임이 코드 증거로 확정되고 이후 비교 기준이 저장됨 |
| 2. raw asset/schema 정리 | 8개 미사용 control facet과 character-scene audience/market 필드를 주 assets·facet vocab·validator에서 제거하고 `source_preset_id`를 중립 내부 key로 rename한다 | dictionary validator, asset forbidden-key scan, focused selection/guard tests | 안전·routing 결과를 바꾸지 않고 대상 raw 필드가 주 assets에서 0건이며 `safety_tier` guard는 유지됨 |
| 3. candidate-pack v3와 v2 adapter | v3에서 불필요 source trace와 character taxonomy IDs를 제거하고 공개 profile/selection handle을 중립 alias로 투영한다. 명시적 v2는 기준선 shape와 기존 IDs를 복원한다 | v2 baseline digest 비교, v3 schema/audit/composer, CLI version switch | 기본 v3가 깨끗한 공개 contract를 내고 explicit v2가 선택·prompt bytes와 pack 계약을 보존함 |
| 4. zero-send semantic manifest 전환 | 새 dictionary hash로 manifest/shards를 원자적으로 갱신하되 6,513 ordered texts와 vectors를 전부 cache 재사용한다 | pre/post semantic text hash, sent/reused count, check-index/shard hash | text diff 0, sent 0, reused 6,513, 768 dimensions와 단일 current generation 유지 |
| 5. 최종 자격과 지식 정리 | focused photo regression과 공개/raw forbidden scan을 통과시키고 현재 결과에 맞게 계획·matching report lifecycle만 갱신한다 | affected photo suites, scene/contradiction/generalization/holdout/index, `git diff --check` | 모든 최종 기준 통과, unrelated baseline 악화 0, 한계와 남은 functional legacy가 명시됨 |

## 최종 완료 기준

1. 기본 candidate-pack이 `photo-candidate-pack/v3`이고 공개 character grammar에 `domain`, `topic_id`, `family_id`가 없으며 nonfunctional quality/craft/final source trace가 없다.
2. 주 authoring assets와 facet vocab에 8개 폐기 control facet 및 character-scene audience/market 필드가 0건이고 validator가 이들의 재도입을 거부한다. `safety_tier`와 실제 hard guard는 통과한다.
3. v3 공개 profile/selection handle은 중립 이름을 쓰며 연구·시장·권리승인 과정 이름을 공개 판단 데이터로 노출하지 않는다.
4. 명시적 v2 compatibility 모드의 preset/slot selection, prompt/negative bytes와 normalized pack shape가 고정 기준선과 동일하다.
5. 실제 consumer가 있는 applicability, scene binding, typed intent, audit/ledger provenance와 deliberate legacy/custom/fallback 경로는 유지되고 affected regression이 통과한다.
6. semantic ordered text와 vector bytes는 기준선 6,513개 모두 동일하고 Gemini 전송은 0건이다. index manifest/shard integrity와 retrieval/generalization/holdout 계약이 통과한다.
7. focused photo suites와 scene/contradiction 검증은 기준선을 악화시키지 않고, repository full-suite의 unrelated baseline을 photo 회귀로 오인하지 않는다.
8. historical evidence/artifacts는 보존되고, 이미지 생성·외부 v2 consumer·픽셀 품질을 검증하지 않은 범위는 최종 결과에 명시한다.

## 검증 수준과 예산

- 위험 수준: medium ordinary offline schema/runtime refactor. 기본 공개 contract 변경은 versioned compatibility로 완화한다.
- 반복 중 focused 검증: 수정된 loader/projection/CLI/validator의 기존 unit·contract 테스트와 대표 fixed-seed pack만 실행한다.
- 최종 검증: affected photo suites, dictionary/index, scene/contradiction/generalization/holdout와 exact baseline digest를 한 번 수행한다.
- 외부 전송: 예상 0건. semantic miss가 발견되면 payload를 고정하되 이 목표의 자동 실행에서는 보내지 않는다.
- 검증 확장 전 질문 조건: v2 prompt/selection parity가 raw 필드 복원 없이는 불가능하거나, 새 semantic text·외부 consumer migration·새 서비스가 필수일 때만 중단한다.

## 중단 조건과 실행 지식

- 후보 필드가 selection, safety guard, audit, retry/ledger, runtime integration에 실제 사용되면 삭제하지 않고 retain 또는 versioned adapter로 재설계한다.
- 고정 v2 비교에서 동일 원인의 회귀가 두 번 반복되면 세 번째 verifier를 추가하지 않고 설계를 축소하거나 사용자에게 선택을 요청한다.
- semantic text가 하나라도 바뀌면 Gemini 호출 전에 diff와 exact count/bytes/SHA-256을 보고한다. 전송 승인 여부와 무관하게 원인 없는 semantic 변화는 허용하지 않는다.
- credential, token, raw vector, 민감 endpoint, 사용자/고객 데이터는 보고서와 로그에 저장하지 않는다. 필요한 외부 evidence는 sanitized hash/count와 접근 제한 reference만 기록한다.
- 시작·재개 시 report metadata를 module/path, environment, lifecycle, 최신순으로 평가하고 전문 읽기는 기본 최대 5건이다. 과거 보고서보다 현재 source/direct evidence가 우선한다.
- material failure는 재시도 전에 기존 matching failed report를 우선 갱신하고 같은 원인은 통합한다. lifecycle 변경은 관련 양쪽 report에서 같은 변경으로 연결한다.
- 성공 보고서는 모든 기준 통과 후 기존 material failure 해결, 실패한 기본안 뒤 비자명한 대안, 또는 현재 코드만으로 비싸게 복원되는 다단계 절차 중 하나를 충족할 때만 기본 최대 1건 작성·갱신한다. 단순 test pass나 문서 완료는 자격이 아니다.
- 실행 지식 보고는 별도 stage/checkpoint가 아니며 제품 delta를 대체하거나 다음 구현을 지연하지 않는다.
- 실행 지식 경로: 적용한 위 5개 보고서. 새 material failure가 없고 success qualification이 없으면 추가 보고서를 만들지 않는다.

## Codex 실행 계약

- `GOAL_PLAN.md`의 범위, progress contract, 검증 예산, 완료 기준을 권위 있는 경계로 사용한다.
- setup 이후 각 checkpoint는 product delta 또는 binding implementation decision을 남긴다. 테스트·문서·schema만으로 완료하지 않는다.
- 반복 중 focused 검증을 사용하고 마지막에 위험 비례 최종 검증을 한 번 수행한다.
- 최종 보고에는 실제 산출물, 변경 파일, 핵심 검증과 결과, 완료 기준별 pass/fail, 실행 지식 경로, 남은 위험을 포함한다.
- material scope 또는 validation program 확대 전에는 사용자에게 질문하며 자동 target uplift는 하지 않는다.

## 완료 결과 (2026-08-12 KST)

- 기본 candidate pack을 `photo-candidate-pack/v3`로 전환하고 `--candidate-pack-version v2` 및 programmatic v2 projection을 유지했다. v3는 공개 character profile을 `character_scene_grammar`로, itasha selection handle을 `aligning_original_graphics_vehicle_wrap`으로 투영하며 character taxonomy ID, nonfunctional quality/craft/final-touch source, inventory bookkeeping을 노출하지 않는다.
- 주 authoring assets에서 미사용 control/source key를 제거하고 validator가 재도입을 거부하게 했다. `safety_tier`와 applicability, selected-scene, typed-intent, audit/ledger provenance처럼 실제 consumer가 있는 필드는 유지했다.
- `c2b3600`과 현재 코드를 동일한 667 direct preset 및 `20260812 + index` seed로 교차 재생한 결과 normalized v2 pack, selection, prompt/negative mismatch는 각각 0건이었다. 같은 current sweep의 v3 forbidden-key/value 및 pack-integrity finding도 0건이었다.
- semantic ordered key/text는 6,513개, SHA-256 `f8dc5e9c5f2a3c355db77222c4b1b6648c34617692f8c552af26ebcdb8e93300`으로 기준선과 동일하다. text diff 0, vector diff 0, 16개 shard SHA 목록 동일, reused 6,513, sent 0이다. 새 dictionary hash는 `27c394c2bddb44b57e528d516d6fd6dcc926cf6b8e54587db0d3c86f13a77d04`, generation은 `27c394c2bddb44b5`다.
- 영향 범위 회귀는 `test_prompt_generator` 276/276과 `test_photo_prompt_contract_v2` 46/46을 통과했다. 후자는 첫 전체 실행에서 evaluator의 v2 기본-version 기대 1건이 실패했고, 기본 v3 기대값으로 수정한 뒤 해당 유일 실패를 재실행해 통과했다.
- dictionary/index integrity, scene-expression 112/112, contradiction 667/667(위반 0), generalization 79/79, frozen holdout 24/24, domain holdout v2 6/6이 통과했다. 외부 embedding 요청과 이미지 생성은 수행하지 않았다.
- 남은 경계: historical evidence와 deliberate internal legacy/custom/fallback 경로는 보존했다. 외부 v2 consumer와 렌더 픽셀 품질은 이번 offline 검증 범위에 포함되지 않는다.

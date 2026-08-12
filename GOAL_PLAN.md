# Photo Prompt Runtime Metadata Boundary Refactor Goal

- 작성: 2026-08-11 KST
- 상태: complete — stages 1–5 qualified
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@a53b1ec`
- 자동 목표 상향: 비활성

## 목표와 실제 산출물

- 원래 사용자 요청: 사진 프롬프트 스킬의 모든 기능을 유지하면서, 출처명·연구 과정·평가용 표현처럼 실질 기능과 무관하거나 분석을 편향할 수 있는 데이터가 런타임에 섞이지 않도록 최소한으로 리팩터링한다.
- 최종 제품/결과: 사용자 의미와 시각적 장면 정보만 검색·후보 선택·mandatory intent·최종 프롬프트에 참여하고, 내부 ID·태그·provenance·연구/검증 메타데이터는 typed control 또는 저장소 외부 증거로만 남는 실행 경계. 현재 manifest가 참조하는 시맨틱 shard 세대만 스킬에 포함한다.
- 범위: 의미 텍스트 화이트리스트, 후보팩 관련도 말뭉치, 비시각 mandatory/prompt 문구, character-domain 문맥 게이트, literal routing fixture의 정직한 재분류, 연구/검증 자산의 스킬 밖 이동, stale shard 정리, SKILL/maintenance 설명 정합성, 필요한 시맨틱 인덱스 재생성.
- 비목표: 공개 candidate-pack schema 전면 교체, 기존 stable ID 일괄 rename, 새 연구·출처 수집, 기준 완화, 이미지 생성·픽셀 품질 주장, 배포·commit·push·PR, 별도 evaluator나 로컬 embedding 모델 도입.

## 진척 계약

- 진척으로 인정: 런타임 출력 또는 선택 경계의 실제 수정, 일반 요청 오탐 감소, 연구 자산의 배포 스킬 밖 이동, stale vector 제거, 정제된 인덱스와 측정된 결과.
- 진척으로 인정하지 않음: 문서·테스트만 추가, 기존 메타 문자열을 다른 이름으로만 감춤, source ledger만 옮기고 오염된 벡터를 유지, 실패한 holdout 기대치를 구현에 맞춰 완화.
- 검증-only 작업 상한: 각 제품 단계마다 focused 검증 1회, 최종 affected regression 1회. 새 verifier/schema/artifact family는 만들지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, distinct material failure 보고서 1건, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker`.

## 기준선과 적용 교훈

- 수정 전 기준선: semantic manifest는 6,513개 entry와 `semantic-text-v2`, 16개 current shard를 가리켰다. 스킬에는 current 외 4개 tracked generation 약 183MB가 남아 있었다.
- 오염 경로: semantic text가 stable ID·tags·kind·모든 facet을 포함하며, 현재 index text에는 `character_moe` 134, `source_grounded` 136, market-researched 표식 376, `provenance_scope` 816 entry가 있다. 후보팩 관련도 말뭉치도 ID·tags·kind를 사용한다.
- 직접 제품 결함: CJK character preset의 compact prompt에 `nonvisual provenance`가 출력되고, subculture/worldbuilding render contract는 `source-grounded`를 positive mandatory intent로 노출한다.
- 검증 결합: character route 96개 alias가 domain gate와 96-case 파일에 정확히 공유된다. 이 파일은 독립 holdout이 아니라 literal routing contract fixture로 취급해야 한다.
- 외부 조건: 프로젝트 `.env`에 Gemini credential이 구성되어 있음만 확인했으며 값은 읽거나 출력하지 않았다. 기존 index는 새 manifest가 완성될 때까지 보존한다. 첫 승인 뒤 순방향 검사에서 공개 시각 텍스트 누수가 추가로 발견되어 payload가 바뀌었으므로, 최신 고정 payload에 대한 재승인 후에만 외부 임베딩을 재개한다.
- 적용 보고서:
  - `docs/failed-reports/2026-08-11-photo-mandatory-intent-polarity-contamination.md`: positive intent에는 사용자 가시 의미만 허용한다.
  - `docs/passed-reports/2026-08-11-photo-intent-preserving-optimization.md`: typed source/polarity, exact subject route, no-people 및 기존 byte 경계를 보존한다.
  - `docs/failed-reports/2026-08-08-character-moe-scoped-alias-drift.md`: literal alias fixture와 실제 일반화 근거를 혼동하지 않는다.
  - `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`: typed-domain selection gating과 generic leakage 방지를 보존한다.
  - `docs/failed-reports/2026-08-07-semantic-index-batch-response.md`: Gemini rebuild는 검증된 batch size 1과 cache/checkpoint 경로만 사용한다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 실패 경계와 기준선 고정 | 메타데이터 오염 failure report, 현재 출력·routing·index·asset 기준선 | 기존 명령으로 CJK prompt, specialty pack, generic route, index marker 수 재현 | 수정 대상과 의도적 비변경 경계가 고정됨 |
| 2. 오프라인 런타임 경계 | candidate relevance corpus에서 private ID/tag/facet 제거, character generic phrase에 문맥 게이트 적용, literal 96-case를 contract fixture로 재분류 | 일반 사진 negative controls와 96 literal contracts를 함께 실행 | generic 오탐 0, explicit 96 routes 유지, 일반 rule pack 회귀 없음 |
| 3. 패키지 경계 정리 | source ledger/crosswalk 및 검증 fixture를 runtime skill 밖으로 이동하고 참조 수정, SKILL을 실행 자원 중심으로 축약, current 외 shard 제거 | repository reference scan, manifest shard integrity, skill quick validation | 런타임 스킬에 source title/URL ledger 및 stale shard가 없음 |
| 4. 시각 데이터와 의미 텍스트 정제 | `source-grounded`, `researched`, `cited study`, `nonvisual provenance`를 visual/embedding/mandatory 필드에서 제거하고 명시적 semantic whitelist/recipe를 적용 | 전 preset prompt/pack forbidden-marker scan과 dictionary validation | 내부 메타가 positive output 또는 새 semantic text에 0건 |
| 5. 시맨틱 재생성 및 최종 자격 | 승인된 Gemini batch-size 1 경로로 changed embeddings와 manifest를 재생성하고 current generation만 유지 | check-index, focused photo suites, retrieval contracts, generic negatives, contradiction check, diff check | 모든 최종 기준이 통과하고 기존 unrelated full-suite baseline을 악화시키지 않음 |

## 현재 진행 상태

- 1단계 완료: 오염 경로와 현재 6,513-entry index, generic character-route 오탐, stale shard 기준선을 failure report에 고정했다.
- 2단계 완료: candidate relevance와 integration/source corpus는 공개 시각 텍스트 및 사용자 작성 intent만 사용한다. 96개 literal character routing contract는 유지하면서 4개 일반 사진 문구의 character-domain 오탐을 차단했다.
- 3단계 완료: raw research ledger/crosswalk는 `docs/research-evidence/photo-prompt/`, routing/generalization/holdout/baseline/visual-review fixture는 `tests/fixtures/photo_prompt/`로 이동했다. 런타임 skill asset에는 현재 semantic generation만 남기고, 빌더가 새 manifest 기록 후 이전 generation만 제거하도록 했다.
- 4단계 완료: semantic-text-v3는 `en`/`ko`/aliases/keywords/terms와 기능별 공개 caption만 임베딩하며 stable ID, tags, kind, facet을 제외한다. 공개 positive text와 장면 원자에서 연구 과정, 출처명, `provenance`, market-control 문구를 제거했고 재유입을 막는 기존 dictionary validator 회귀 기준을 추가했다.
- 직접 검증: 공개 관련도·typed polarity·hybrid augmentation·routing, 이동 fixture, shard round-trip/prune, 6,513개 semantic input 경계가 통과했다. `test_photo_prompt_contract_v2` 44/44, `test_prompt_generator` 272/272, rule generalization 79/79, holdout 24/24, domain holdout v2 6/6, current-scene audit 112/112, 667-preset contradiction check 667/667이 통과했다. 667개 모든 직접 preset을 한국어·영어 detailed rule mode로 생성한 결과 금지 marker와 생성 오류가 각각 0건이며, 독립 순방향 검사에서 발견한 CJK character 누수도 재현 후 해결했다. 전체 suite는 526개에서 기존 기준선과 정확히 같은 unrelated universal-scene 11 failures/1 error만 남았다. 의도적으로 달라진 rule candidate 출력은 10개 current golden과 versioned photo regression baseline v2로 갱신했고 v1 역사 hash는 보존했다.
- 시맨틱 재생성 완료: 승인된 SHA-256 `3ec1b84dbd98772c71a5daa5ebd3b4afc64a162c971a741da50aea35dbe98a57`의 6,513개 목록에서 checkpoint 973개를 재사용하고 5,540개를 `gemini-embedding-2`로 전송했다. 새 manifest는 dictionary hash `2c3f9d34a64d233eb6b2c1301c52a0087eb45a85870717da64d7fbc04b1fde3e`, `semantic-text-v3`, 768d, 6,513 entries와 16개 유효 shard를 가리킨다. entry order/hash/count 검증이 통과했고 generation 디렉터리는 `2c3f9d34a64d233e` 하나뿐이며 partial checkpoint는 제거됐다.
- 5단계 완료: 별도 승인을 받은 순서 고정 retrieval payload(22 cases, 71 requests, 고유 68 texts, UTF-8 6,381 bytes, SHA-256 `5702e85ca1e2d2d14a5a921438a89cd9dd19ab667dd4b2b87be497e730398040`)만 `gemini-embedding-2`에 전송했다. real semantic retrieval holdout은 22/22를 통과했다. 최종 `--check-index`, dictionary validator, skill quick validation, `git diff --check`, runtime order/hash/count, 단일 generation, 금지 marker 및 옛 asset 경로 검사도 모두 통과했다.

## 최종 완료 기준

1. 공개 positive prompt, mandatory intent, visual atom label에 연구 출처·개발 과정·검증 표식이 0건이다.
2. semantic text 생성은 명시적 사용자/시각 필드만 사용하며 stable ID, tags, kind, facet/provenance를 임베딩하지 않는다.
3. 명시적 character route 96개 contract는 유지되고 일반적인 관계·포즈·헤어·소품 사진 negative control은 character 전용 도메인으로 라우팅되지 않는다.
4. raw research title/URL ledger와 crosswalk는 런타임 skill package 밖에 있고 테스트·maintenance 참조가 유효하다.
5. semantic manifest가 가리키는 한 세대의 16개 shard만 추적되며 hash/count/order 검증이 통과한다.
6. 기존 public wrapper, rule/semantic 선택, candidate-pack v2, safety, negative prompt, no-people, adult-appeal 및 direct preset 기능이 유지된다.
7. focused photo tests와 dictionary/index/scene/contradiction 검증이 통과하며 unrelated full-suite 기준선보다 악화되지 않는다.

## 검증 수준과 예산

- 위험 수준: ordinary offline refactor + 외부 embedding rebuild 한 번. 외부 데이터는 정제된 공개 taxonomy text로 제한한다.
- 반복 중 focused 검증: routing unit tests, 대표 rule packs, direct polluted presets, reference scan, dictionary validator.
- 최종 검증: affected photo tests, semantic index integrity/retrieval, contradiction check, skill quick validation, `git diff --check`를 한 번 수행한다.
- 이미지 생성·pixel review는 텍스트/라우팅/패키지 경계 목표에 필요하지 않아 제외한다.
- 외부 API 호출 조건: corpus와 retrieval 평가 각각의 exact payload hash에 대한 사용자 명시 승인과 credential 구성을 확인했다. 승인된 두 payload 외 텍스트는 전송하지 않았다.

## 중단 조건과 실행 지식

- 향후 semantic text나 평가 fixture가 바뀌면 기존 승인을 재사용하지 않고 새 exact payload hash를 고정해 별도 승인을 받는다.
- 기존 공개 ID를 바꿔야만 해결되는 경우 compatibility map 또는 schema version 선택을 사용자에게 묻고 임의 변경하지 않는다.
- 같은 원인으로 두 번 실패하면 세 번째 verifier를 만들지 않고 failure report를 갱신한 뒤 설계를 바꾸거나 질문한다.
- 삭제 대상 shard는 current manifest와 Git 추적 상태를 다시 확인한 뒤에만 제거하며 Git으로 복구 가능하게 유지한다.
- 비밀·credential·민감 데이터는 보고서나 로그에 기록하지 않는다.
- material failure는 재시도 전에 기존 matching report를 갱신하거나 하나로 통합한다. 성공 보고서는 모든 기준 통과 후 실패 해결, 기본안 실패 뒤 비자명한 대안, 또는 비싸게 재구성되는 필수 절차 중 하나일 때만 최대 1건 작성한다.
- 보고서는 진척이나 별도 checkpoint가 아니며 현재 코드와 직접 증거가 과거 보고서보다 우선한다. lifecycle 변경 시 양방향 링크를 같은 변경에 반영한다.
- 실행 지식 보고서: 새 `docs/failed-reports/2026-08-11-photo-runtime-metadata-contamination.md`; 완료 시 자격을 충족하면 새 passed report 최대 1건.

## Codex 실행 계약

- 반복 중에는 focused 검증을 사용하고, 위험에 비례한 최종 검증을 한 번 수행한다.
- 최종 보고에는 실제 산출물, 변경 파일, 핵심 검증 결과, 완료 기준별 pass/fail, 실행 지식 경로와 남은 위험을 포함한다.
- 범위·검증 예산·완료 기준을 자동으로 확대하지 않는다.

# Independent Japanese-Subculture Moe Generation Goal

- 작성: 2026-08-13 14:35 KST
- 상태: completed
- 완료: 2026-08-13 15:53 KST
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@795691ed4f84`
- 자동 목표 상향: 비활성
- 이전 목표 경계: `795691e:GOAL_PLAN.md`의 v10 츤데레 픽셀 사용자 판정은 완료로 간주하지 않는다. 그 미해결 사실은 `docs/failed-reports/2026-08-12-moe-aesthetic-contract-user-preference-failure.md`에 보존하며, 이번 독립 5-arm 시험과 별개의 사용자 선호 목표로 둔다.

## 목표와 실제 산출물

- 원래 사용자 요청: 다섯 개의 서로 독립된 서브에이전트 환경에서 각 에이전트가 현재 `photo-prompt-image-generator` 스킬을 실제로 읽고 사용해, 첨부된 가상 성인 인물을 바탕으로 일본 서브컬처 스타일의 모에한 프롬프트와 이미지를 하나씩 독립 생성한다. 모든 결과가 식물에 물주는 장면으로 수렴한 이전 시험의 전달·선택 결함을 고치고 다시 시험한다.
- 최종 제품/결과: 일반적인 일본 서브컬처 모에 요청이 우연한 부분 문자열 때문에 식물 장면으로 라우팅되지 않는다. 각 에이전트는 후보팩 생성 전에 자기만의 구조화된 콘셉트 코어와 구체적인 일본 서브컬처 사진 스타일 근거를 작성하며, 후보팩·composed prompt·실제 이미지·호출 ledger를 자기 작업공간에 남긴다. 다섯 결과는 숨김이나 재시도 없이 함께 제시된다.
- 범위: v4 장면 relevance selector, typed Japanese-subculture photo style contract, 후보팩 이전 authorial request 계약, 관련 composer/audit 및 skill 문서, v2/v3 명시적 호환 경계, 5개 분리 worktree에서 각 1회 이미지 생성 시험.
- 비목표: 이전 v10 츤데레 한 장의 추가 qualification, 일반 사진 전체의 미학 재설계, 특정 기존 캐릭터·작가·브랜드 복제, 첨부 인물의 실제 신원 추론, 일러스트 생성기로 전환, 배포·push·PR, 기존 대규모 `output/` 이력 정리, 이미지 모델 전반의 보편적 모에 성능 주장.

## 진척 계약

- 진척으로 인정: selector/contract/composer의 실제 동작 변화, 고정 입력에서 달라진 장면·스타일·콘셉트 코어, 에이전트별 독립 prompt와 실제 픽셀, 실패를 포함한 정확한 호출 결과.
- 진척으로 인정하지 않음: 계획·테스트·schema·audit·manifest만 추가한 상태, `Japanese subculture` 또는 `moe`라는 라벨만 붙인 prompt, 같은 내부 장면을 말만 바꿔 다섯 번 재사용한 결과, prompt PASS를 픽셀 품질 PASS로 주장한 상태.
- 검증-only 작업 상한: 기준선 재현 1회 후 각 제품 단계당 focused 검증 1회, 마지막 affected regression 1회. 검증-only checkpoint를 두 번 연속 만들지 않는다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, matching failed report 우선 갱신, 성공 보고서 기본 최대 1건, 별도 checkpoint 금지.
- 진행 로그: `product delta -> direct evidence -> remaining product gap -> blocker`.

## 기준선과 고정 결정

- 현재 기준선: commit `795691e`의 default candidate pack은 v4이며 blueprint ID와 구체 장면 원자를 숨기고 에이전트가 장면을 새로 쓰게 한다. 그러나 내부 blueprint relevance가 요청 전체에서 길이 4 이상의 단어를 부분 문자열로 세기 때문에 `mist`가 `unmistakably`에 맞는다. 고정 seed `1301, 2603, 3907, 5209, 6503` 모두 내부 식물 관찰/급수 blueprint를 고른다.
- 최근 수정의 유효한 경계: v4 authorial scene과 pack privacy는 이전 v3의 구체 장면 복사를 줄였지만, 선택기 입력·일본 서브컬처 style evidence·후보팩 이전 에이전트 창작 provenance를 해결하지 않았다. 기존 v4 focused tests 5건과 dictionary/scene/semantic 무결성 검사는 통과했으므로 호환 기준선으로 유지한다.
- 독립성 정의: 다섯 에이전트는 같은 최종 source ref와 같은 사용자 첨부 이미지만 공유한다. 서로 다른 detached worktree·artifact 디렉터리·seed를 사용하고 다른 arm의 prompt/pack/image/message를 읽거나 입력으로 쓰지 않는다. 독립성 합격과 결과 다양성 평가는 분리한다.
- 스타일 정의: `일본 서브컬처 스타일`은 인종·국적·실존 인물을 추론하는 말이 아니다. 사진에서 보이는 구체적인 fashion/community/venue/styling 계열 하나와 최소 두 개의 시각 근거로 materialize해야 한다. 라벨만 있는 경우 fail-closed 한다.
- authorial 정의: 각 에이전트가 후보팩 생성 전에 `authorial_request/v1`의 subject, setting, event, style domain/evidence, variation key를 직접 확정한다. pack 이후에 선택된 내부 장면을 역으로 포장한 텍스트는 authorial provenance가 아니다.
- 관련 과거 실행 보고서와 적용 교훈:
  - `docs/failed-reports/2026-08-12-natural-moe-default-scene-repair-convergence.md`: generic natural request와 강하게 저술된 연구 장면의 relevance를 분리하고 no-preset end-to-end를 확인한다.
  - `docs/failed-reports/2026-08-12-atomic-scene-candidate-trace-leak.md`: selector를 고칠 때 score trace와 rule fallback 등 모든 projection branch에 같은 경계를 적용한다.
  - `docs/failed-reports/2026-08-12-moe-aesthetic-contract-user-preference-failure.md`: prompt/audit 합격을 픽셀 모에 합격으로 대체하지 않고, 첨부 identity 기준과 실제 결과를 보존한다.
  - `docs/failed-reports/2026-08-12-natural-moe-composite-mixin-gate.md`: 역할·종족·스타일이 합성될 때 한 축이 다른 축을 덮지 않게 하고 공개 wrapper까지 검증한다.
  - `docs/passed-reports/2026-08-07-subculture-taxonomy-on-demand-routing.md`: 기존 bilingual on-demand subculture extension과 scoped route를 재사용하되 rendered distinctiveness는 별도로 확인한다.

## 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 고정 재현과 실패 지식 결박 | 동일 입력/5 seed에서 식물 수렴과 substring evidence를 재현하고 matching failed report를 생성 또는 갱신한다 | 공개 wrapper pack과 private routing trace 비교 | `mist`/`unmistakably` 오탐과 후보팩 이전 콘셉트 부재가 재현 가능하고, 기대/관찰/원인이 재시도 전에 기록됨 |
| 2. 장면 relevance selector 수리 | scene-bearing intent와 age/identity/tone/safety control을 분리하고 boundary-aware matching 및 blueprint 전용 selection cues를 사용한다. opt-in private `--explain-scene-routing`은 점수 근거만 노출한다 | exact collision negative와 explicit plant positive focused test | generic 일본 서브컬처 모에 요청은 식물 장면을 relevance winner로 고르지 않고, 식물/물주기를 명시한 요청은 해당 장면을 계속 고름 |
| 3. typed 일본 서브컬처 사진 스타일 | 기존 subculture extension을 재사용해 `japanese_subculture_photo/v1`을 만들고 style family, 최소 두 visible cues, scoped exclusions를 pack/composition에 결박한다. 무관한 강테마 후보는 명시 의도 없이는 제외한다 | label-only/ethnicity-inference/irrelevant-theme mutation과 3개 이상 style family focused cases | 일반 요청도 구체적인 한 계열과 두 근거를 가지며 스타일 라벨만으로 통과하지 않고 국적·민족 외형을 발명하지 않음 |
| 4. 후보팩 이전 authorial request | CLI/public wrapper가 에이전트 작성 `authorial_request/v1`을 받아 canonical SHA와 `agent_prepack` provenance를 기록하고, v4 authored scene/core가 그 subject/setting/event/style 의미를 보존한다 | pack-before/pack-after provenance mutation, 5개 고정 variation input | pack 이후 역포장이나 빈 콘셉트는 실패하고, 유효한 pre-pack request는 composed prompt까지 보존됨 |
| 5. 버전·런타임 경계와 skill 지침 | 새 실행은 v4 preflight를 기본으로 하고 v2/v3에는 explicit `legacy_replay_reason`을 요구한다. manifest에 skill/source hash, pack version, concept-core hash, reference hash, image-call count를 기록하도록 스킬 실행 계약을 갱신한다 | v4 default와 explicit legacy replay focused regression | 오래된 v3를 새 실행으로 가장할 수 없고 기존 명시적 compatibility projection은 유지됨 |
| 6. 다섯 독립 arm 실제 재시험 | 최종 source ref로 detached worktree 5개를 만들고, 각 서브에이전트가 그 안의 스킬을 처음부터 읽은 뒤 독립 콘셉트·pack·prompt를 만들고 첨부 reference만 사용해 이미지 도구를 정확히 1회 호출한다 | arm별 manifest/ledger, native 픽셀 thumbnail+full review, 전체 결과 병렬 제시 | 5개 arm 모두 다른 arm 산출물 무참조를 증명하고 prompt와 실제 이미지 1개씩을 남김. 독립성 결과와 시각적 다양성 결과를 별도 보고함 |

## 최종 완료 기준

1. exact generic 입력과 다섯 고정 seed에서 우연한 substring 때문에 식물 관찰/급수 장면이 선택되지 않으며, 명시적 식물/물주기 요청은 해당 장면을 선택한다.
2. 새 v4 pack/composed prompt는 `japanese_subculture_photo/v1`의 구체 style family와 최소 두 visible cues를 보존하고, label-only·민족 외형 추론·무관 강테마 치환을 fail-closed 한다.
3. 유효한 `authorial_request/v1`은 후보팩 전에 생성된 canonical SHA와 provenance를 가지며 subject/setting/event/style 의미가 최종 prompt까지 보존된다.
4. default v4와 명시적 v2/v3 compatibility가 모두 동작하되 새 실행에서 legacy를 쓰려면 `legacy_replay_reason`이 필요하다.
5. 다섯 arm은 분리 worktree/입력/ledger를 가지며 다른 arm의 산출물을 읽지 않고 현재 스킬을 직접 사용했다는 증거를 남긴다. 결과 다양성은 독립성의 대리 지표로 쓰지 않는다.
6. 각 arm은 첨부 인물을 성인 identity reference로만 다루고, 일본 서브컬처 style evidence가 실제 prompt와 픽셀에 최소 두 가지 읽히는지 정직하게 판정한 이미지 1개를 남긴다. 생성 실패/정책 차단은 이미지 성공으로 세지 않는다.
7. selector/style/authorial/version focused tests와 affected photo regressions, dictionary/scene/semantic integrity, `git diff --check`가 통과한다.
8. 최종 보고는 다섯 prompt·이미지·manifest 경로, 독립성 판정, 시각 다양성 판정, 각 픽셀의 모에/style 한계, 미검증 범위를 숨김없이 제시한다.

## 검증 수준과 예산

- 위험 수준: medium. 로컬 offline prompt/product 변경과 이미지 생성이며 배포·외부 mutation은 없다.
- 반복 중 focused 검증: 수정한 selector/style/authorial/version 경계의 동결 사례만 실행한다. 제품 변경 없이 evaluator만 확장하지 않는다.
- 이미지 예산: 최종 arm당 exactly one image-tool call, 합계 5회. retry, best-of-N, favorable selection, 다른 arm 이미지의 편집·참조를 금지한다.
- 최종 검증: affected photo unit/contract suite, dictionary/scene/semantic 무결성, 다섯 arm manifest와 native pixels를 한 번 확인한다. 독립 검토는 이 계획의 기준만 재확인하고 새 기준을 만들지 않는다.
- 검증 확장 전 질문 조건: 기존 경로로 mandatory criterion을 확인할 수 없어 새 외부 service/평가 campaign이 필요하거나, 합계 5회를 넘는 이미지 호출·유료 API·배포·material scope 확대가 필요할 때 중단하고 묻는다.

## 중단 조건과 실행 지식

- 같은 고정 입력이 같은 selector 원인으로 제품 수정 2회 뒤에도 실패하면 단어를 임의 삭제하거나 seed를 고르지 않고 trace와 선택지를 보고한다.
- 스타일 family를 안전하게 materialize하려면 국적/민족/특정 IP를 추론해야만 하는 설계가 되면 그 접근을 중단하고 추상적인 community/fashion/venue 근거로 되돌린다.
- 유효한 pre-pack authorial request와 기존 v4 privacy/compatibility를 동시에 보존할 수 없으면 public/private 경계를 완화하지 말고 사용자에게 tradeoff를 묻는다.
- 이미지 호출이 픽스를 필요로 하는 입력 감사에서 실패하면 호출하지 않고 제품을 최대 2회 수정한다. 호출 뒤 무픽셀/정책 차단/시각 실패가 발생하면 해당 arm의 1회 결과로 보존하며 재시도하지 않는다.
- credential, token, secret, 민감 endpoint, 고객/개인정보는 보고서·로그·ledger에 저장하지 않는다. 첨부 파일은 경로·hash·`fictional adult identity reference` 역할만 기록하고 생체 신원을 추론하지 않는다.
- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/` 파일명·header metadata를 module/path, environment, status, 최신순으로 평가하고 전문은 기본 최대 5건만 읽는다. 충돌하면 현재 source와 직접 evidence가 우선한다.
- material failure는 재시도 전에 기존 matching failed report를 우선 갱신하고 같은 원인을 한 보고서에 통합한다. resolved/superseded lifecycle 변경은 관련 양쪽 보고서에 같은 변경으로 연결한다.
- 모든 최종 기준 통과 뒤에만 성공 보고서를 기본 최대 1건 작성한다. 자격은 기존 material failure 해결, 기본/문서화된 접근 실패 뒤 비자명한 대안, 또는 현재 코드만으로 비싸게 복원되는 다단계 재현 절차 중 하나여야 한다. 단순 테스트·문서·중간 빌드 통과는 자격이 아니다.
- 목표가 blocked/partial이면 passed report를 만들지 않고 matching failed report의 resolution/workaround 또는 최종 진행 요약에 검증된 부분 결과를 남긴다.
- 실행 지식 보고는 별도 stage/checkpoint가 아니며 제품 delta를 대체하거나 다음 구현을 지연하지 않는다.
- 적용 실행 지식: 위 5개 보고서. 새 material failure가 생기면 경로를 진행 로그와 최종 요약에 기록한다.

## 완료 결과 (2026-08-13)

- 완료 범위: selector의 `mist`/`unmistakably` 부분 문자열 충돌을 제거하고, `japanese-subculture-photo/v1`, 후보팩 이전 `authorial-request/v1`, v4 기본 및 명시적 legacy replay 경계, 독립 실행 manifest/ledger 계약을 구현했다.
- 기준 1 PASS: 다섯 고정 seed의 일반 일본 서브컬처 요청에서 식물 장면은 0/5였고, 명시적 식물 요청은 식물 blueprint를 계속 선택한다.
- 기준 2 PASS: v4 pack/composed prompt가 style family와 최소 두 visible cues를 보존하며 label-only, 민족 외형 추론, 무관 강테마 치환을 fail-closed 한다.
- 기준 3 PASS: 각 arm의 후보팩 이전 authorial request는 고유 canonical SHA와 `agent_prepack` provenance를 가지며 subject/setting/event/style 의미가 prompt까지 보존됐다.
- 기준 4 PASS: default v4가 동작하고 v2/v3는 `legacy_replay_reason` 없이는 새 실행에 사용할 수 없으며 명시적 compatibility projection은 유지된다.
- 기준 5 PASS: 다섯 detached worktree는 서로 다른 arm/worktree/seed/request/pack/prompt/image hash를 가지며 모든 manifest가 `cross_arm_inputs_used=false`를 기록한다. root-side JSON/NDJSON 경로 검사에서도 다른 arm 참조는 발견되지 않았다.
- 기준 6 PASS(정직한 픽셀 판정): 실제 이미지 5/5, 성인 identity 5/5, 요청 style family의 독립 visible cues 최소 두 개 5/5, 식물 장면 0/5였다. 행동 기반 모에 사건은 1/5만 읽혔고, 그 한 장도 exact negative 위반으로 완전 기술 적격은 0/5였다. 사용자 본인의 진짜 모에 판정은 5장 모두 pending이다.
- 기준 7 PASS: affected unit/contract suite 343/343, scene-expression 112/112, generalization 79/79, frozen holdout 24/24, domain-v2 holdout 6/6, dictionary metadata, 6,513-entry semantic index, Python compile, `git diff --check`가 통과했다.
- 기준 8 PASS: 다섯 prompt/image/manifest, 독립성·다양성·픽셀 한계와 실행 중 pre-materialization 오류를 `generated_images/japanese-subculture-moe-five-reference-v2-20260813/evaluation/review_summary.md`에 보존했다.
- 다양성 판정: 독립성은 통과했지만 style family는 Decora 2개와 retro arcade 3개, 총 2/8 계열에 수렴해 부분적이다. 독립성을 다양성의 대리 지표로 사용하지 않는다.
- 남은 별도 제품 gap: dense causal moe beat의 픽셀 전달력이 불안정하다. 현 5-call 예산을 숨은 재시도로 늘리지 않고 `docs/failed-reports/2026-08-13-independent-moe-causal-event-pixel-attrition.md`에 open failure로 기록했다. 후속 개선은 새 목표와 새 이미지 예산을 필요로 한다.
- 실행 절차 공개: root 배정에서 public wrapper 대신 internal `prompt_generator.py`를 지정하면서 절대 tags 경로를 빠뜨려 pack materialization 전 실패가 발생했다. 각 arm은 이미 동결한 authorial request로 v4 pack을 정확히 하나만 materialize했고 이미지 호출은 정확히 한 번, retry 0회였다.

## Codex 실행 계약

- 이 `GOAL_PLAN.md`의 범위, 진척 계약, 검증 예산, 완료 기준을 권위 있는 경계로 사용한다.
- setup 이후 각 checkpoint는 product delta, 사용자-visible artifact, measured candidate result 또는 binding implementation decision을 남긴다. 테스트·문서·schema만으로 완료하지 않는다.
- 반복 중 focused 검증을 사용하고 마지막에 위험 비례 최종 검증을 한 번 수행한다.
- 최종 보고에는 실제 산출물, 변경 파일, 핵심 검증과 결과, 완료 기준별 pass/fail, 실행 지식 경로, 남은 위험을 포함한다.
- material scope 또는 validation program 확대 전에는 사용자에게 질문하며 자동 target uplift는 하지 않는다.

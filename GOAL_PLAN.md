# Viewer-Perceived Creative Direction and Authorial Voice Goal

- 작성: 2026-08-08 16:31 KST
- 상태: complete
- 대상: `skills/photo-prompt-image-generator`
- 기준 ref: `main@b8fe45e` 위의 현재 미커밋 character-moe 자격 상태
- 권위 문서: 이 파일이 이번 장기 목표의 범위, 완료 기준, 검증 예산과 중단 조건을 정의한다.
- 선행 완료 목표: Research-Backed Moe and Subculture Character Grammar (`docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`)
- 자동 목표 상향: 비활성

## 1. 목표와 실제 산출물

### 원래 사용자 요청

후보팩에 주제 데이터를 더 넣는 방식이 아니라, 사용자가 창의적·독창적·기발한·작가적인 프롬프트나 이미지를 요청했을 때 관객이 최종 이미지에서 실제로 그 특성을 느끼도록 `photo-prompt-image-generator`의 생성 사고과정, 선택, 비평, 프롬프트 구성과 검증을 개선한다.

### 최종 제품/동작

1. 명시적 창의 요청이 별도 추가 지시 없이 `creative-direction` 경로를 자동 활성화한다.
2. 에이전트는 후보팩을 받은 뒤 곧바로 문장을 조립하지 않고, 평범한 기대 기준선과 서로 다른 concept move 여러 개를 만든 뒤 하나만 선택한다.
3. 선택된 개념은 친숙한 닻, 단 하나의 규칙 변화, 화면에서 확인 가능한 결과 연쇄, 관객의 발견 순서와 하나의 작가적 시각 문법을 가진다.
4. 기존 prompt audit은 이 구조가 실제 프롬프트 문구에 반영됐는지 검증하고, 고정 `artistic_final_touch` 문구는 작가성의 증거로 취급하지 않는다.
5. 세 가지 고정 주제의 구현 전·후 실제 이미지가 metadata-free 비교에서 평범한 기준선보다 독창성·기발함·의도 가독성이 개선되며, 주제 충실도와 사진적 완성도를 잃지 않는다.

### 범위

- `SKILL.md`, composition/creative-direction reference, candidate-pack creative contract, composed prompt audit, 관련 focused/unit tests.
- 기존 `--creativity`의 semantic breadth·novelty 기능과 구분되는 에이전트 수준 creative-direction workflow.
- 실행 전 동결한 세 주제의 baseline/final candidate pack, composed prompt, 실제 PNG와 기존 형식의 visual-review 결과.
- 기존 candidate pack, automatic safety, scene contract, typed character grammar, negative byte-preservation과 일반 요청의 보수 기본값 보존.

### 비목표

- 후보팩 taxonomy·preset·주제별 장면 데이터를 대량 추가하지 않는다.
- named artist 스타일 모방, 작가 이름 기반 프롬프트, 역사적으로 완전히 새로운 발상이라는 보장을 만들지 않는다.
- semantic index 재생성, 새 임베딩 서비스, 배포, commit, push, PR은 포함하지 않는다.
- 창의성 수치를 하나의 토큰/임베딩 거리나 클리셰 단어 개수로 환원하지 않는다.
- 사람 패널이나 장기 사용자 연구를 새 필수 서비스로 구축하지 않는다. 이번 목표는 동결된 metadata-free 직접 픽셀 검수까지 자격화하고 더 넓은 관객 연구는 후속 범위로 남긴다.

## 2. 진척 계약

- 진척으로 인정: creative request의 실제 runtime/composer 동작 변화, audit가 소비하는 binding contract, 감사된 창의 프롬프트, 실제 baseline/final PNG, 실패 원인을 고친 제품 delta.
- 진척으로 인정하지 않음: 문서·스키마·테스트·fixture·리뷰 양식만 추가, `--creativity` 숫자만 상향, 후보/형용사/초현실 장식만 증가, prompt audit PASS만으로 이미지 품질 주장, 성공한 렌더만 골라내기.
- setup checkpoint는 Stage 1 한 번뿐이다. 이후 checkpoint는 코드/스킬 동작 변화, 감사된 최종 프롬프트, 실제 이미지 또는 binding 구현 결정을 남겨야 한다.
- 검증-only 작업 상한: focused 검증은 제품 변경 직후 한 번, 전체 suite와 최종 visual qualification은 마지막 Stage 6에서 한 번만 실행한다.
- 실행 지식 작업 상한: 관련 보고서 전문 최대 5건, 성공 보고서 기본 최대 1건, 보고서 작업을 별도 checkpoint로 만들지 않는다.

## 3. 기준선과 고정 비교 조건

### 현재 기준선

- `SKILL.md`는 창의 요청에 `--creativity`를 높이도록 안내하지만, 높은 값도 기존 sampler-eligible 동일 슬롯 대안을 feature-token 거리로 골라 최대 두 개 교체하는 `creative_exploration`에 머문다.
- `creativity_settings`는 semantic profile, novelty와 batch diversity를 보간하며 관객 기대, concept move, 의미 회수, 작가적 관점을 별도 모델링하지 않는다.
- `visual_proposition`과 `artistic_final_touch` 감사는 관련 어휘 또는 고정 다큐멘터리 문구를 찾으며, 최종 픽셀에서 관객이 독창성과 의도를 읽는지는 증명하지 않는다.
- 이전 목표들은 scene/category/character mechanism의 픽셀 가독성은 자격화했지만, 같은 주제에서 평범한 예상과 비교한 surprise-to-insight 또는 authorial voice는 자격화하지 않았다.

### 고정 세 주제

1. `창의적이고 독창적인 도예가의 사진을 만들어줘.` — 현실 직업/행위
2. `도시의 고독을 기발하고 작가적인 사진으로 표현해줘.` — 추상 정서/도시 환경
3. `성인 변신 히로인의 이중 정체성과 회복을 독창적인 사진으로 만들어줘.` — 서브컬처 성인 캐릭터

### 비교 조건

- 구현 전 baseline과 구현 후 final은 같은 한국어 요청, 같은 repository image tool, 같은 aspect/quality 기본값을 사용한다.
- candidate pack은 재현 가능한 rule mode와 고정 seed `890101`, `890102`, `890103`을 사용한다. creative request의 기존 기준선은 `--creativity 1.0`으로 고정한다.
- 각 baseline/final은 최초 candidate pack 하나, 감사된 composed prompt 하나, 최초 이미지 하나를 사용한다. 성공해 보이는 여러 결과 중 선택하지 않는다.
- final이 필수 픽셀 기준을 실패하면 구체적인 product cause를 먼저 기록하고 같은 원인의 구현/프롬프트 수리는 최대 2회다. 각 수리 뒤에는 새 pristine pack/prompt/image 한 개만 생성하며 실패 결과를 보존한다.
- final 판정 항목은 구현 전에 고정한다: 주제 충실도, 평범한 기준선과 다른 핵심 전제, 하나의 규칙 변화, 최소 두 개의 가시적 결과 연쇄, surprise-to-insight, deliberate authorial choice, 무관한 anomaly stacking 부재, 사진적 정합성.
- 기존 visual-review 형식을 재사용한다. 새 holdout/review 쌍은 기존 scene/character 리뷰로 확인할 수 없는 관객 지각 창의성 비교를 위해서만 한 벌 추가한다.

### 적용한 과거 실행 지식

- `docs/failed-reports/2026-08-07-worldbuilding-render-scene-convergence.md`: routing과 prompt PASS가 실제 흥미·독창성을 증명하지 않는다. 지식과 render expression을 분리하고 pixels를 metadata-free로 판정한다.
- `docs/passed-reports/2026-08-07-research-scene-expression-render-quality.md`: 하나의 sparse event와 제한된 evidence가 데이터 밀도보다 장면 구별에 효과적이다. resolved scene을 ordinary candidate pool에 합성하지 않는다.
- `docs/failed-reports/2026-08-08-character-moe-pixel-action-legibility.md`: 프롬프트에 명사가 있어도 방향·동시성·정체성은 픽셀에서 사라질 수 있다. actor/action/result를 구체적으로 묶고 실패 픽셀을 보존한다.
- `docs/passed-reports/2026-08-08-character-moe-grammar-render-quality.md`: 비시각 router/guard와 sparse visual atom을 분리하고, 한 primary mechanism과 최대 두 support cue를 유지한다.
- `docs/failed-reports/2026-08-08-character-moe-final-integration-contract-drift.md`: 새 typed contract를 기존 route family의 일반 규칙에 억지로 맞추지 말고 올바른 semantic layer에서 검증한다.

## 4. 실행 단계

| 단계 | 실제 산출물/동작 변화 | 최소 직접 검증 | 완료 조건 |
|---|---|---|---|
| 1. 기준선 동결 | 세 고정 요청의 현행 pack, composed prompt, 최초 PNG, metadata-free baseline 판정과 한 벌의 holdout/review 계약 | pack/audit 상태와 PNG hash·크기·prompt/negative bytes 확인 | 세 사례 모두 현행 동작과 평범함/장식 누적 한계가 변경 전 증거로 보존되고 성공 기준은 아직 수정되지 않음 |
| 2. Creative-direction 생성 경로 | 명시적 창의 요청 자동 라우팅, `creative_direction` pack contract, agent runtime `creative_brief`, 서로 다른 concept move 최소 4안과 단일 선택 절차 | 세 fixed 요청에서 contract enabled, 일반 요청에서 disabled/absent, 후보팩 주제 데이터 증설 없음 | 프롬프트 작성 전 기대 기준선→복수 발상→단일 선택이 binding workflow로 작동 |
| 3. Authorial grammar와 감사 | familiar anchor, one rule break, visible consequence chain, reveal path, hidden aboutness, authorial vantage/time/omission/material rule과 literal prompt evidence를 기존 audit에 연결; 고정 final-touch는 surface craft로 재분류 | 정상 creative composed 1건 PASS, 필수 필드 누락·다중 rule break·선택되지 않은 proposal 혼합·prompt evidence 불일치 각각 fail | 문서만 채운 brief가 아니라 최종 prompt에 선택된 개념과 작가적 결정이 실제 반영됨 |
| 4. 세 최종 프롬프트 자격 | 세 fixed 요청에 서로 다른 concept operator를 사용한 감사 PASS 프롬프트와 rejected-cliche 기록 생성; 뻔한 안·장식 누적을 bounded repair | baseline 대비 구조적 비교와 focused tests | 세 프롬프트 모두 하나의 개념 전제, 최소 두 결과 연쇄, 관객 발견 순서와 서로 구별되는 작가적 문법을 가짐 |
| 5. 실제 이미지 비교 | 세 final 최초 PNG와 metadata-free baseline/final 비교; 픽셀 실패 시 제품 원인 수리와 bounded pristine rerender | 기존 visual-review 포맷으로 3 case × 고정 focus 판정, prompt metadata 없이 원본 픽셀 검사 | 3/3 final이 주제·사진 품질을 유지하고 각 baseline보다 독창성·기발함·의도 가독성 중 최소 두 축에서 명확히 개선되며 모든 필수 픽셀 focus PASS |
| 6. 닫힌 회귀와 완료 | focused 수리 결과, 기존 full unit, dictionary/scene/candidate 계약, `git diff --check`, 최종 visual review와 실행 지식 lifecycle 정리 | full suite 1회와 기존 직접 validator, current artifact hash 확인 | 모든 완료 기준 통과, 미해결 material failure 없음, 실제 제품 코드/스킬·프롬프트·이미지가 존재 |

## 5. 최종 완료 기준

1. 창의적·독창적·기발한·작가적 요청이 자동으로 creative-direction 경로를 활성화하고 일반 요청은 기존 보수 경로를 유지한다.
2. creative-direction은 후보팩 주제 데이터가 아니라 생성·선택 계약이며, 기존 candidate provenance, scene contract, safety, negative bytes와 호환된다.
3. 활성 creative run은 최소 네 개의 서로 다른 concept move를 만든 뒤 정확히 하나를 선택하고, 최종 prompt는 familiar anchor, 단 하나의 rule break, 최소 두 visible consequence, reveal path와 authorial grammar의 literal evidence를 포함한다.
4. 고정 `artistic_final_touch` 문구 또는 스타일 형용사만으로 authorial PASS를 받을 수 없고, named artist 모방 없이 frame/time/vantage/omission/material 선택이 하나의 aboutness를 지지한다.
5. audit는 missing brief, proposal 부족/중복, 다중 rule break, 선택안 혼합, prompt evidence 불일치를 거부하면서 ordinary composed prompt를 회귀시키지 않는다.
6. 동결 세 사례의 final 실제 이미지가 3/3 metadata-free 필수 focus를 통과하고 각 baseline보다 독창성·기발함·의도 가독성 중 최소 두 축에서 개선되며 주제 충실도와 사진적 정합성이 후퇴하지 않는다.
7. 기존 character grammar, scene-expression, candidate-pack, safety, semantic routing/index 상태를 불필요하게 변경하지 않고 focused/full 회귀와 `git diff --check`가 통과한다.
8. 실제 skill/runtime/audit 변경, 감사된 세 final prompt, 세 final PNG와 versioned visual result가 모두 존재한다. 계획·테스트·fixture·보고서만으로 완료할 수 없다.

## 6. 검증 수준과 예산

- 위험 수준: 중간. 로컬 agent workflow와 candidate/audit 계약 변경이며 외부 배포는 없지만, 일반 요청 회귀와 이미지 모델의 prompt-following 실패 가능성이 있다.
- 반복 중 검증: 변경 함수와 audit focused tests, 세 fixed rule-mode pack만 실행한다.
- 이미지 예산: baseline 3개 + final 최초 3개. 같은 product cause의 수리 뒤 pristine rerender는 사례당 최대 2개이며 실패 이미지를 삭제하지 않는다. 임의 이미지 편집이나 다수 생성 후 선별은 하지 않는다.
- 최종 검증: 기존 validator와 full unit 1회, 세 visual artifact의 hash/contract 검사 1회. 독립 verifier나 새 평가 프로그램을 추가하지 않는다.
- semantic dictionary text나 index entry가 바뀌면 이번 범위를 벗어난다. 외부 임베딩 전송이나 index rebuild를 시작하지 말고 먼저 질문한다.
- 검증이 구현 작업보다 커지거나, 세 사례로 주장할 수 없는 일반화 범위를 필수 기준으로 삼아야 할 경우 범위 확장 전에 질문한다.

## 7. 중단 조건

- 같은 근본 원인의 제품/픽셀 수리 2회 뒤에도 필수 기준이 실패할 때.
- 통과를 위해 기존 frozen routing, scene, character, safety, IP/culture 기준을 약화해야 할 때.
- 창의성을 증명하기 위해 대규모 후보 데이터, 새 유료 서비스, 외부 taxonomy/semantic 전송, 사람 모집, 배포 또는 파괴적 변경이 필요할 때.
- 현재 미커밋 character-moe 작업과 겹치는 변경을 분리할 수 없거나 그 자격 증거를 훼손할 위험이 있을 때.
- 이미지 모델이 prompt의 핵심 관계를 반복해서 잃어 구현과 model limitation을 구분할 수 없을 때. 이 경우 실패 결과와 확인된 sub-result를 보고하고 목표를 임의로 완화하지 않는다.

## 8. 실행 지식 계약

- 시작·재개 시 `docs/failed-reports/`와 `docs/passed-reports/`의 filename/header metadata를 관련도 순으로 검색하고, 전문은 기본 최대 5건만 읽는다. 현재 source와 direct evidence가 과거 보고서보다 우선한다.
- material failure가 가정이나 완료 기준을 깨거나 수리 방향을 바꾸면 재시도 전에 matching failed report를 생성 또는 갱신한다. 같은 원인은 한 보고서에 통합한다.
- evidence를 저장하기 전에 현재 날짜·시간을 확인하고 credential, token, secret, 민감 endpoint, 개인정보와 출처 원문을 제거한다. 필요한 경우 sanitized 결론과 접근 제한 evidence reference만 남긴다.
- 실패가 과거 passed report의 적용 범위를 깨면 failed/passed 양쪽 lifecycle을 같은 변경에서 연결한다. 해결 시 failed를 `resolved`, 성공 보고서에 `Resolves`, 기존 결과를 대체할 때 양쪽 `Superseded by`/`Supersedes`를 기록한다.
- 모든 최종 기준을 직접 통과한 뒤에만 목표당 기본 최대 한 개의 passed report를 작성한다. 자격은 다음 중 하나여야 한다: material failed report 해결, 동일 고정 조건에서 기본/문서화 접근 실패 뒤의 비자명한 대체, 또는 현재 코드만으로 싸게 복구할 수 없는 다단계 재현 절차. 중간 test PASS나 편리한 명령은 성공 보고서가 아니다.
- 목표가 blocked/partial이면 passed report를 만들지 않고 matching failed report 또는 최종 진행 로그에 검증된 sub-result를 남긴다.
- 실행 보고는 별도 stage/checkpoint가 아니며 제품 진척을 대신하거나 다음 product delta를 지연시키지 않는다.

## 9. 진행 로그 형식

각 checkpoint는 다음 순서로 이 파일에 추가한다.

`product delta -> direct evidence -> remaining product gap -> blocker -> execution-knowledge paths`

## 10. Codex 실행 프롬프트

```text
/goal Treat GOAL_PLAN.md as the authoritative outcome-first execution plan. Preserve its scope, progress contract, validation budget, completion criteria, and full execution-knowledge contract. Use metadata-first report search with at most five full reads by default; current evidence wins. Sanitize stored evidence, update stale or resolved reports bidirectionally, record material failures before retry, and create at most one qualified reusable success by default only after all final criteria pass. Reporting is not product progress or a separate checkpoint. After setup, advance through product or measured-result checkpoints, use focused verification during iteration, and run one risk-proportional final verification. Do not add verification programs or external gates unless the plan requires them or a real product defect makes them necessary. Ask before any material scope or validation expansion.
```

## 11. 진행 로그

### 2026-08-08 16:31 KST / 목표 생성 및 실행 지식 적용

- product delta: 이전 완료 GOAL_PLAN의 자격 상태를 passed/failed 보고서에 연결하고, 관객 지각 창의성과 작가적 시각 문법을 실제 skill/runtime/audit/image 결과로 개선하는 새 활성 목표를 작성했다.
- direct evidence: 관련 보고서 metadata 전체를 스캔하고, exact failure/architecture match 순으로 전문 5건을 읽어 기준선·검증 예산·중단 조건에 반영했다. 현재 `main@b8fe45e` 위 미커밋 character-moe 변경을 보존하며 commit/push와 semantic index 변경을 범위 밖으로 고정했다.
- remaining product gap: Stage 1의 세 baseline pack/prompt/image 동결부터 모든 제품 구현과 실제 렌더 비교가 남아 있다.
- blocker: 없음.
- execution-knowledge paths: 3절의 failed 3건과 passed 2건.

### 2026-08-08 16:41 KST / Stage 1 기준선 동결

- product delta: 세 고정 요청을 기존 최대 `--creativity 1.0` rule-mode 경로로 각각 한 번만 구성·감사·렌더하고, pack/prompt/PNG/result 및 구현 전에 고정한 비교 gate를 보존했다.
- direct evidence: pack `8407d0af26c37f14`, `78507b1e8fdc8266`, `8a28b8da1150dd51`는 audit status `pass`였으나 모두 quality `warn`이었다. 최초 PNG 3개는 사진적 정합성 3/3이지만 metadata-free 독창성·기발함·작가적 선택은 0/3이었고, 도시 고독은 익숙한 비 오는 뒷모습, 도예가는 distressed-luxury flatlay, 변신 회복은 평범한 자전거 수리로 수렴했다. 동결 계약은 `assets/render_creative_direction_holdout_v1.jsonl`, 상세 증거는 `generated_images/creative-direction-holdout-v1-20260808_163100/`에 있다.
- remaining product gap: Stage 2의 creative-direction pack/runtime 계약과 Stage 3의 authorial grammar binding audit 구현이 남아 있다.
- blocker: 없음.
- execution-knowledge paths: 기존 5건을 재사용했고 새 material failure는 발생하지 않았다.

### 2026-08-08 16:48 KST / Stage 2 creative-direction 경로 구현

- product delta: 명시적 창의 요청을 skill layer에서 자동으로 `--creativity 0.85+`에 라우팅하고, 높은 창의성 pack에 주제 데이터와 분리된 `photo-creative-direction/v1` 계약을 추가했다. 기존 `creative_exploration`은 slot breadth로 유지하되, 새 경로는 평범한 기준선 3개, 서로 다른 operator의 완성된 제안 4개 이상과 정확히 한 선택을 요구한다.
- direct evidence: 일반/0.74 pack에는 `creative_direction`이 없고 0.85 pack에는 결정론적으로 존재한다. 같은 seed의 preset·slot 후보 순서와 선택은 변하지 않았으며 focused candidate contract test가 통과했다.
- remaining product gap: 실제 composed prompt에서 선택안만 literal binding하고 authorial grammar를 fail-closed 검증하는 Stage 3 통합 자격 및 세 최종 프롬프트가 남아 있다.
- blocker: 없음.
- execution-knowledge paths: 새 별도 보고서 없이 기존 world/scene/character 실패 지식을 runtime contract에 적용했다.

### 2026-08-08 16:48 KST / Stage 3 authorial grammar 감사 구현

- product delta: `creative_brief` 감사가 ordinary baseline/rejected cliche, 제안 수·operator 고유성, 단일 scalar rule break, 선택 일치, visible consequence·reveal path, vantage/timing/omission/material rule, literal prompt evidence를 fail-closed 검증한다. 선택되지 않은 signature 혼합, evidence 불일치, 고정 final-touch 문구를 authorial evidence로 사용하는 것도 거부한다.
- direct evidence: 정상 brief PASS와 missing brief, 제안 부족, operator 중복, stacked rule, unselected signature 혼합, literal binding 불일치, final-touch 차용을 각각 거부하는 focused test가 함께 통과했다 (`2 tests`, `OK`).
- remaining product gap: 세 frozen request의 실제 pack에서 whole-audit PASS/quality PASS 프롬프트와 픽셀 결과를 만들어 이 계약이 문서·unit 수준을 넘어 작동함을 증명해야 한다.
- blocker: 없음.
- execution-knowledge paths: `references/creative-direction-contract.md`에 생성-선택-픽셀 검수 경계를 명시했다.

### 2026-08-08 16:59 KST / Stage 4 세 최종 프롬프트 자격

- product delta: frozen seed·scene 조건을 유지한 새 pack 3개에서 각각 `absence_as_evidence`(도예가), `controlled_impossibility`(도시 고독), `temporal_fold`(성인 변신 회복)를 선택했다. 각 brief는 서로 다른 4안을 완성한 뒤 1안만 선택하며, 선택되지 않은 signature는 prompt에 들어가지 않는다.
- direct evidence: 최종 prompt는 각각 120/109/120 words, composed audit `status=pass`, failures 0이다. quality warning은 pack이 생성 시 이미 `uncovered`로 표시한 번역 intent 보존 알림만 남고 photographic integration, craft, creative binding 경고는 0이다. negative bytes, scene atoms, character grammar와 safety pass를 보존했다.
- remaining product gap: 최초 final PNG 3개에서 core premise·두 consequence·surprise-to-insight·authorial choice가 실제로 보이는지 metadata-free 판정해야 한다.
- blocker: 없음.
- execution-knowledge paths: 새 material failure 없음; prompt PASS를 pixel PASS로 오인하지 않는 기존 failed report 경계를 유지한다.

### 2026-08-08 17:02 KST / Stage 5 최초 픽셀 판정과 material failure 기록

- product delta: 각 final prompt를 built-in image generator로 정확히 한 번 렌더하고 원본과 첫 attempt를 보존했다. 변신 사례는 8개 focus 전체 PASS했으나 도예가와 도시 고독은 각각 trace 물질화와 기본 인물 반사로 핵심 rule이 유실됐다.
- direct evidence: `03-transformation/final/attempt-01.png`는 현재 손과 케이스 속 장갑 낀 이전 손이 한 인물의 반복 각도로 읽힌다. `01-potter`의 원형은 금속 받침으로, `02-urban-solitude`의 노면은 정상 인물 반사로 렌더됐다. 해시·크기·고정 focus는 각 `attempt-01-review.json`에 있다.
- remaining product gap: 같은 실패 원인에 대한 첫 bounded pristine prompt repair와 rerender가 두 사례에 남아 있다.
- blocker: 없음. repair budget 0/2 사용 상태에서 진행한다.
- execution-knowledge paths: `docs/failed-reports/2026-08-08-creative-direction-pixel-premise-legibility.md` active.

### 2026-08-08 17:07 KST / Stage 5 첫 bounded repair

- product delta: 실패 픽셀의 관계만 구체화해 byte-identical same-seed pack에서 pristine prompt/image를 한 번씩 다시 만들었다. 도예가는 물리 ring/base를 금지하고 displaced-dust negative space로 변경해 통과했다. 도시 사례는 matte blank를 강화했지만 정상 반사 prior가 반복됐다.
- direct evidence: `01-potter/final/attempt-02.png`는 bare circle·off-center cup·material-only clue가 8 focus PASS다. `02-urban-solitude/final/attempt-02.png`는 완전한 사람 반사와 평범한 tote로 rule/consequence/insight가 다시 FAIL했다.
- remaining product gap: 도시 사례에 남은 마지막 repair 1회에서 이미 개발한 `functional_recontextualization` 안을 선택해 더 렌더 가능한 단일 기능 전환을 자격화한다.
- blocker: 없음. 같은 반사 부재 문구의 반복은 중단했고, urban repair budget 1/2를 사용했다.
- execution-knowledge paths: active pixel-premise failed report에 Repair 1 결과와 최종 repair 방향을 추가했다.

### 2026-08-08 17:10 KST / Stage 5 최종 metadata-free 픽셀 자격

- product delta: 도시 사례의 마지막 repair에서 이미 개발된 `functional_recontextualization` 안 하나를 선택해 tote를 휴대 가능한 방의 문턱으로 만들었다. 세 사례의 accepted PNG, 실패 attempt, audit/result와 versioned visual review를 모두 저장했다.
- direct evidence: 도시 final은 투명 tote 속 따뜻한 복도·문과 tote 바닥에서 젖은 노면으로 이어지는 마른 amber corridor를 동시에 보이고, 주변 neon rain reflection은 경계 밖에 머문다. 도예가 final은 displaced-dust empty footprint, 변신 final은 temporally delayed gloved-hand reflection을 보인다. `render_creative_direction_visual_review_v1.json`에서 3/3 × 8 fixed focus PASS, 각 baseline 대비 originality/ingenuity/intentionality 3축 개선, topic/photo no-regression이다.
- remaining product gap: full unit/validator/diff 검증, image-run ledger, failed/passed report lifecycle와 목표 완료 선언이 남아 있다.
- blocker: 없음. 도시 repair budget 2/2에서 통과했으며 추가 렌더를 만들지 않는다.
- execution-knowledge paths: active pixel-premise report는 최종 회귀 후 resolved로 닫고 자격 있는 passed report 한 건에 연결한다.

### 2026-08-08 17:41 KST / Stage 6 닫힌 회귀와 목표 완료

- product delta: creative-direction skill/runtime/audit, 세 감사된 final prompt, accepted PNG와 versioned visual review를 하나의 완료 상태로 닫았다. material pixel failure report를 resolved로 바꾸고 자격 있는 재사용 성공 보고서 한 건에 양방향 연결했다.
- direct evidence: dictionary validator PASS, merged scene routes 112/112 PASS, final pack/composed 3/3 PASS·negative content 동일·118/120/120 words, PNG hash 일치, visual focus 3/3 × 8 PASS, full suite `Ran 401 tests in 1551.172s — OK`, `git diff --check` PASS다. 일반/0.74 pack에는 creative contract가 없고 0.85 pack에는 결정론적으로 존재하며 기존 후보 선택 순서를 바꾸지 않는다.
- remaining product gap: 없음. 세 사례는 고정 직접 자격이지 역사적 새로움이나 전체 관객 모집단의 보장은 아니라는 제한을 유지한다.
- blocker: 없음.
- execution-knowledge paths: `docs/failed-reports/2026-08-08-creative-direction-pixel-premise-legibility.md` resolved; `docs/passed-reports/2026-08-08-viewer-perceived-creative-direction.md` current and resolves it.

# photo-prompt-image-generator P0 상세 실행 계획

작성일: 2026-10-07. 대상 HEAD: `f6b2f88fc9adeae0dfe59b78a7a0ecafc7b4c03a`와 현재 작업 폴더의 확인된 소스. 기존 미커밋 데이터·테스트 변경이 있는 상태다. 이 문서는 구현 계획이며, 이번 요청으로 코드·스킬·데이터를 수정하거나 이미지/API 호출을 실행하지 않는다.

기준 자료: [확인한 소스·해시](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/P0_PLAN_SOURCE.json), [계획 문서 검증](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/P0_PLAN_VALIDATION.json).

## 1. 목표와 완료 범위

[과거 세션 분석의 두 P0](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/REPORT.ko.md:56)를 다음 결과물로 구체화한다.

| 작업 | 해결할 문제 | 완료 결과 |
|---|---|---|
| P0-1: 의미 판정 | 값이 있는데도 ‘축 누락’, 관계가 있는데도 ‘연산자 누락’, 긍정 문맥을 못 찾았는데도 ‘다른 의미로 해결됨’으로 설명 | 원문·작성 규칙·실제 구조를 함께 제시하는 결정적 진단. 확인된 대응 표현을 인식하고 실제 부정·대상·방향 차이를 계속 구별 |
| P0-2: API 실행 경계 | `prompt_en`만 있는 입력도 실제 API 호출 지점에 도달 | 원본 pack·정확한 receipt·composed·runtime request를 검증한 입력만 전송. 성공·실패를 같은 입력에 연결 |

권장 구현 순서는 **재현 자료 고정 → 진단 개선 → API 감사 강제 → 제한된 어휘·필수 조건 조정 → 통합 검증**이다. 설명을 고치는 변경과 후보 판정이 달라지는 변경을 분리해 원인을 확인한다.

P0의 완료는 의미 판정과 실행 경계의 정확성이다. 사진의 매력, 픽셀 재현 향상, 사용자 선호 개선은 별도 실험이 필요하다. 전체 실행 도구, 스킬 본문의 대규모 축약, 세 조건 이미지 비교, 재시도 자동 수리, 모든 데이터의 의미 검토는 이번 범위에 포함하지 않는다.

## 2. 유지해야 할 기준

1. 사용자 의미·설정·authorial core를 동결한 후 조회한다. 미인식을 해결하려고 원문·core·baseline에 등록 문구를 덧붙이지 않는다.
2. 사용자 정의가 작성 프로필보다 우선한다. 프로필 적합도와 선택 후보는 advisory이며, 새 필수 시각 의무를 만들지 않는다.
3. `unrecognized`는 판정의 한계다. 실제 반대 의미, 누락, 다른 대상, 반대 방향을 각각 증거로 구분한다. embedding 점수로 자동 PASS하지 않는다.
4. 기존 사용자 속성 잠금, adult 문구의 조건부 적용, authorial direction, embodiment, render-repair, strict review를 보존한다.
5. pack의 원본과 receipt가 감사의 기준이다. composer view는 읽기 도구이며 원본을 대체하지 않는다.
6. composed 문장은 runtime에 연속 포함될 수 있다. 두 문자열의 전체 동등성을 공통 감사기의 새 조건으로 만들지 않는다. **API가 전송하는 문자열과 감사한 `runtime_prompt_en`은 정확히 같아야 한다.**
7. 준비 실패, 실제 호출, 제공자 오류, 이미지 저장 실패, 레저 실패, 픽셀 판독, 사용자 판단을 구분한다. 기록 실패를 새 이미지 호출로 복구하지 않는다.
8. 기존 다른 작업의 dirty 파일·untracked 산출물·과거 pack·레저를 보존한다. 과거 결과의 기준이나 해시를 새 구현에 맞춰 덮어쓰지 않는다.

근거: [스킬](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/SKILL.md), [조회 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/retrieval-contract.md), [실행 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/image-runtime.md), [유지보수 기준](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md).

## 3. 착수 전에 고정할 자료 — 단계 0

| 자료 | 고정 방법 | 용도 |
|---|---|---|
| 현재 판정 사례 | [어휘 점검](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/semantic_vocabulary_probe.json)과 10/5의 입력·진단 기록을 복사하고 해시 기록 | 설명 변경과 판정 변경의 전후 비교 |
| API 우회 재현 | [오프라인 점검](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-photo-skill-session-review/api_adapter_offline_probe.json)을 실패해야 할 입력으로 고정 | 미감사 입력이 호출 전에 차단되는지 확인 |
| 정상 실행 사례 | 현재 구현으로 생성·감사된 text-only pack, receipt, composed, `photo-image-render-request/v2` 한 묶음을 임시 runtime store에 고정 | 새 API preflight의 정상 경로 검증 |
| 반례 | 아래 표의 대상·방향·부정·문맥·변조 사례를 독립 fixture로 작성 | 수정에 맞춰 평가 기준을 낮추는 일 방지 |
| 소스와 작업 상태 | HEAD, 변경 파일, 핵심 소스 해시, runtime generation을 기록 | 다른 진행 작업과 변경 소유권 분리 |

네트워크·embedding·이미지 생성 함수를 대체하고 호출 횟수를 직접 센다. 정상 API fixture는 실제 감사기를 통과해야 한다. 모든 감사 함수를 항상 PASS로 대체한 fixture만으로 실행 경계를 검증하지 않는다.

진단의 단위 테스트는 불완전한 축을 직접 받을 수 있지만, 실제 pack 작성에서는 기존 core 구조 검증도 유지한다. 잘못된 core 구조를 새 진단 기능이 허용해서는 안 된다.

착수 산출물은 입력 해시와 기대 결과가 담긴 `p0_baseline.json`, 정상 실행 fixture, 재현 테스트다. 테스트 추가 위치는 `tests/fixtures/photo_prompt/`와 기존 관련 테스트이며, skill runtime assets에 평가 사례를 넣지 않는다.

## 4. P0-1A — 판정 동작을 보존하고 진단을 정확하게 만들기

### 4.1 진단의 공통 형태

`photo-meaning-diagnostics/v1`을 새 내부/공개 진단 객체로 정의하고 `semantic_consistency`와 `applicability` 아래에 노출한다. 각 항목은 다음을 가진다.

| 필드 | 내용 |
|---|---|
| `kind` | `axis`, `relation`, `context` |
| `code` | 아래의 구별된 사유 코드 |
| `source_path` / `source_id` | 읽은 동결 assertion·축·관계 또는 작성 프로필의 정확한 위치/ID |
| `raw_value` | 입력 원문 또는 실제 관계 객체. 정규화 결과로 대체하지 않음 |
| `expected` / `observed` | 기대 클래스·관계와 실제 인식 클래스·관계 |
| `evidence` | 인식한 작성 용어와 그 근거 문구. 근거가 없으면 빈 목록 |
| `match_basis` | 작성 클래스의 정확한 값/구문 매칭 등 실제 사용한 방식 |
| `blocking_effect` | 기존 필수 조건 판단에 영향을 주는지, 보조 진단인지 |

진단은 설명용이다. 숨겨진 검색 점수·사적 argv를 공개하거나, 해석 근거가 없는 확률을 만들지 않는다. 원문 근거를 추적할 수 없는 상황에서는 확인된 충돌로 단정하지 않는다.

### 4.2 축 판정

[현재 판정 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:5577)를 다음 상태로 세분화한다.

| 입력/인식 상태 | 코드 | 설명 |
|---|---|---|
| 필드가 없거나 유효 값이 없음 | `axis_absent` | 요구 축이 입력에 없음 |
| 원문 값은 있지만 작성 클래스가 없음 | `axis_value_unrecognized` | 값은 존재하나 현재 어휘로 분류할 수 없음 |
| 인식 클래스가 기대 클래스에 해당 | `axis_class_match` | 어떤 원문·alias가 어떤 클래스에 연결됐는지 제시 |
| 인식 클래스는 있지만 허용 클래스와 다름 | `axis_class_mismatch` | 기대·실제 클래스 차이. 이것만으로 실제 반대 의미라고 단정하지 않음 |
| 명시적 제외 클래스에 해당 | `axis_excluded_class` | 제외 규칙과 그 원문 근거를 함께 제시 |

상위 `consistent / incomplete / conflicting / not_applicable / superseded_by_requester_definition`은 유지한다. 단계 1에서는 기존 허용·거부 결과와 후보 선택을 바꾸지 않는다. `incomplete`의 요약 사유는 ‘필수 조건을 확인하지 못함’으로 정확하게 바꾼다.

새 출력의 `missing_axes`는 실제 부재만 담고, `unrecognized_axes`, `class_mismatch_axes`, `unmet_axes`를 분리한다. `unmet_axes`는 기존 필수 조건 미충족의 합집합이다. 소비자와 테스트를 같은 변경에서 수정하며 새 세대에 모호한 옛 집계 의미를 남기지 않는다.

### 4.3 관계 판정

[기존 signature](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:1369)를 판단 기준으로 재사용한다.

| 상태 | 코드 | 확인 사항 |
|---|---|---|
| 요구 operator 자체가 없음 | `relation_operator_absent` | 기대 operator와 실제 operator 목록 |
| operator는 있지만 `same_target.members`가 다름 | `relation_members_mismatch` | 기대·실제 구성원. 순서만 다른 경우는 동일 관계로 처리 |
| `contrasts.left/right`가 다름 | `relation_endpoints_mismatch` | 방향을 포함한 실제 endpoint 차이 |
| `temporal_order.first/then`이 바뀜 | `relation_order_mismatch` | 선후 순서 차이 |
| 관계가 정확히 일치 | `relation_match` | 일치한 원본 관계와 signature |

새 `missing_relation_operators`에는 실제 부재만 넣고, 구조 차이는 `relation_diagnostics`와 `unmet_relations`로 기록한다. 같은 operator가 여러 번 있으면 모든 관련 실제 구조를 남긴다. 자유문장의 비슷한 단어를 보고 typed 관계나 상대 ID를 자동으로 만들어 넣지 않는다.

### 4.4 문맥과 clarification의 설명 연결

[문맥 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:6166)에서 얻은 실제 이유와 근거를 resolution hit → clarification → composer view → composed audit까지 전달한다.

| 현재 원인 | 새 진단 | 해석 |
|---|---|---|
| `request_exclusion` | `request_exclusion_term_matched` | 작성 제외어가 어떤 입력 근거에 일치했는지 |
| `context_disambiguation_exclusion` | `context_exclusion_term_matched` | 명시된 제외 문맥 매칭. 실제 사용한 규칙을 제시 |
| `context_disambiguation_mismatch` | `positive_context_unrecognized` | 필요한 긍정 문맥 표현을 찾지 못함. 다른 의미가 확인됐다는 뜻이 아님 |
| 실제 existing adult gate 미충족 | `existing_adult_context_required` | 현재의 정확한 gate 부족만 설명. 문맥 미인식을 adult 부족으로 바꾸지 않음 |
| 사용자 정의 override | `requester_definition_precedence` | 프로젝트 기본 프로필로 재해석하지 않음 |

현재 `context_mismatch`의 ‘core가 다른 의미로 해결했다’라는 공통 문구를 실제 진단 사유로 대체한다. 단계 1에서는 기존 적용 가능성·필수 활성화 여부를 보존한다. 미확인 후보를 설명만 바꿔 자동 채택하거나 hard obligation으로 승격하지 않는다.

작성 프로필의 lexical 제외어 일치와 사용자 의미의 논리적 모순도 구분한다. 구체적인 반대 의미 근거가 없으면 ‘작성 규칙상 제외’라고 설명한다.

### 4.5 계약·뷰·감사

- 새 진단 객체를 generator의 단일 경로에서 만들고 조회 lane별 사유를 일관되게 투영한다. BM25F·embedding이 사유를 덮어쓰지 못하게 한다.
- clarification 출력 구조 변경은 `photo-semantic-clarification/v2`로 명시하고 producer·auditor 상수를 같이 갱신한다. candidate-pack-v6와 authorial-core-v3 자체는 유지한다.
- 기존 `compose_pack_view.py`의 `semantic_consistency`·`applicability` 투영에 새 근거가 보존되는지 검증한다. catalog는 사유를 요약하고 details는 전체 근거를 보여 준다.
- 원본 pack 감사는 pinned source에서 재계산한 진단·clarification과 비교한다. 조작된 사유나 빠진 근거를 그럴듯한 설명으로 받아들이지 않는다.
- 역사 pack의 v1을 새 v2처럼 재명명하거나 호환 branch로 의미를 바꾸지 않는다. 필요한 역사 재생은 해당 sealed implementation을 사용한다.

완료 기준: 고정 사례의 상위 판정·활성화·채택 가능성은 동일하고, 상세 사유만 올바르게 달라진다. 결과 차이가 생기면 단계 1의 변경으로 인정하지 않고 원인을 분리한다.

## 5. P0-1B — 확인된 표현과 개념별 필수 조건만 조정

이 단계부터 판정이 의도적으로 달라질 수 있다. 단계 1의 설명 개선과 별도로 전후 delta를 제출한다.

### 5.1 작성 어휘의 제한된 보강

1. 현재 `affectionate warmth directed at the same duet partner`가 클래스 미인식인 사례를 고정한다. `affectionate warmth`를 `surface_affect.open_warmth`의 확인된 대응 표현으로 추가하는 변경을 출발점으로 삼는다.
2. 한국어·영어·일본어는 실제 검토된 표현만 등록한다. 번역 문자열을 무차별 확장하지 않고 각 alias의 의미와 반례를 같이 기록한다.
3. 클래스 판정 전용 matcher를 분리해 원문·일치 근거·극성을 돌려준다. 전역 검색 tokenizer나 모든 profile activation을 한꺼번에 변경하지 않는다.
4. 정확한 authored 값/경계가 있는 구문을 근거로 삼는다. 현재의 단어 집합 포함만으로 떨어진 단어·부정·다른 대상을 자동 일치시키지 않는다.
5. 등록 구문 주변의 명확한 부정은 `axis_value_negated`, 긍정·부정이 섞여 범위가 불명확하면 `axis_polarity_unresolved`로 남긴다. 이 경우 긍정 클래스 자동 PASS를 막는다. 광범위한 자연어 추론기를 이번 P0에 추가하지 않는다.
6. 관계와 대상은 기존 typed assertion으로 확인한다. 축 어휘가 인식되어도 다른 상대·역방향 관계는 계속 미충족이다.

이 단계의 목표는 검토된 표현을 올바르게 인식하는 것이다. 모든 자유문장이나 모든 부정 구문을 해결했다고 선언하지 않는다. 지원 범위 밖의 표현은 정확한 미인식/미해결 사유로 남긴다.

### 5.2 얀데레의 추가 의도성 축

[10/5 근거](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-05-photo-semantic-matching-improvement-plan.md:62)에 따라 해당 프로필의 `affect_leak_intentionality`만 보조 설명으로 이동한다.

- 해당 축을 얀데레 `axis_requirements`와 그 축의 필수 제외 조건에서 제거하고 새 `axis_advisories`에 넣는다. `axis_advisories`는 클래스 목록과 필수 의미가 아닌 이유를 가진다.
- validator의 허용 필드·축/클래스 참조 검증과 pack 진단 투영을 함께 수정한다. 보조 조건은 상위 `incomplete/conflicting`의 원인이 될 수 없다.
- 입력에 있는 값은 그대로 보존한다. 의도적·비의도적 여부를 모르는 입력에 값을 채우지 않는다. 보조 조건 근거·부재는 보조 진단에 남긴다.
- 애정, 동일 상대, 경계를 넘는 소유 행동, 같은 상대의 관찰 가능한 결과는 그대로 검증한다. core의 공통 필수 축·관계·render gate를 삭제하지 않는다.
- 츤데레·쿨데레 등 다른 프로필의 의도성 규칙은 별도 근거 없이 바꾸지 않는다.

어휘와 필수 조건 변경은 각각 기대 delta가 달라 별도 비교한다. ‘표현 인식 때문에 통과’와 ‘불필요한 추가 축을 보조로 옮겨 통과’를 한 원인으로 합치지 않는다.

### 5.3 의미 검증 사례

| 사례 | 단계 1 기대 결과 | 단계 3 기대 결과 |
|---|---|---|
| 축 필드 없음 | `axis_absent` | 동일. 실제 필수 조건은 계속 미충족 |
| 값 존재, 등록 표현 없음 | `axis_value_unrecognized` | 검토 범위 밖이면 동일 |
| `affectionate warmth…`와 정확한 같은 상대 관계 | 기존 미충족 유지 + 미인식 이유 | `open_warmth` 인식. 나머지 요구까지 맞을 때만 적합 |
| `openly affectionate` | 기존 클래스 일치 유지 | 동일 |
| 등록 애정 표현의 명확한 부정 | 현재 lexical 결과와 한계를 보존해 기록 | 긍정 자동 일치 금지, 부정/극성 근거 제시 |
| 애정은 A, 통제는 B | 관계 구성원 차이 | 어휘가 늘어도 관계 차이는 미충족 |
| `same_target` 구성원의 나열 순서만 바뀜 | 일치 | 동일 |
| 선후 순서 반전 | `relation_order_mismatch` | 동일 |
| 긍정 문맥은 있으나 현재 용어로 미인식 | `positive_context_unrecognized` | 확인된 대응 표현만 인식. 다른 의미로 해결됐다고 단정 금지 |
| 명시적 제외 문맥 | 일치 규칙·원문을 제시 | 제외 근거 계속 보존 |
| 사용자 정의가 기본 프로필과 다름 | 사용자 정의 우선 | 동일 |
| 얀데레, 의도성만 미상/absent | 기존 추가 조건 미충족 이유를 제시 | 의도성은 보조. 다른 핵심 요구는 계속 필요 |
| 같은 값의 츤데레·쿨데레 | 기존 판정 유지 | 해당 프로필 규칙 유지 |
| 비인물 장면, 선택 후보 미채택 | 인물 의무 추가 없음 | 동일. 선택 후보 전부 미채택 가능 |

다국어의 새 바꿔 쓰기와 반례를 따로 둔다. 평가용 표현을 모두 alias로 등록한 뒤 일반화 성능이라고 보고하지 않는다.

## 6. P0-2 — API가 감사된 실행 입력만 소비하도록 변경

### 6.1 새 입력 계약과 CLI

기존 `generate_images_via_api.py`를 스킬의 감사된 API 진입점으로 유지하되, 단일 실행에 아래 파일을 필수로 받게 변경한다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/generate_images_via_api.py \
  --pack /absolute/path/pack.json \
  --runtime-receipt /absolute/path/pack.json.runtime-receipt.json \
  --composed /absolute/path/composed.json \
  --render-request /absolute/path/render-request.json \
  --concept "요청의 작업 이름" \
  --model gpt-image-2 --size 1024x1536 --attempts 2 \
  --dry-run
```

이것은 **구현 후 사용할 제안 명령**이다. 현재 CLI에 이 옵션이 이미 있다는 뜻은 아니다. `--runtime-store`, `--out-base`, `--slug`는 기존 저장 경로·식별 기능에 맞춰 선택적으로 지원한다. 기본 모델·크기·시도 상한은 현재 값을 유지하며 요청이나 승인된 런타임이 지정한 값을 임의로 바꾸지 않는다.

- 입력은 객체 또는 기존 공통 로더와 같은 1개 객체 목록만 허용한다. 다중 목록의 첫 항목을 조용히 고르지 않는다.
- 미감사 `--prompt-json`, 임의 폴더 스캔 `--prompt-dir`의 실행 경로를 제거한다. `--skip-audit`나 raw-prompt fallback을 추가하지 않는다.
- `--attempts`는 양의 정수만 받는다. 0·음수를 1회 호출로 보정하지 않는다.
- P0에서 batch runner나 reference API transport를 새로 만들지 않는다. 복수 실행은 명시적인 감사 입력 묶음마다 별도 실행한다.
- **현재 API 어댑터는 text-only다.** `references`가 비어 있지 않거나 참조가 필요한 identity contract가 있으면 `unsupported_reference_transport`로 호출 전에 실패한다. 파일 경로를 프롬프트에 쓰거나 참조 목록을 비워 대신 실행하지 않는다.

### 6.2 호출 직전 처리 순서

1. **파일을 한 번 읽고 보존한다.** pack·receipt·composed·render request의 원본 bytes와 파싱 객체를 읽는다. raw 파일 해시와 기존 canonical binding을 구분한다. 잘못된 타입·다중 객체·누락 파일은 여기서 차단한다.
2. **receipt 세대를 검증한다.** `RuntimeSnapshotProvider.from_receipt(pack, receipt)`로 정확한 generation을 읽는다. pack hash·source fingerprint·algorithm·cache binding·구현/환경 검증을 재사용한다. 실패하면 최신 generation을 재조회해 원래 입력의 의미를 바꾸지 않는다.
3. **composed 감사를 새로 실행한다.** `audit_composed_prompt(..., source_data=snapshot.data)`를 실행하고 `status == pass`와 실패 0개를 요구한다. `quality_status == warn`은 경고를 보존한다. 입력 JSON의 `audit_status: pass`는 권한이나 검증 결과로 믿지 않는다.
4. **runtime 감사를 별도로 실행한다.** 기존 `audit_image_render_request`에 같은 pack·composed·원본 request path를 전달한다. pack/core/intent/render-repair/visual-contract binding, composed 연속 포함, negative 보존, runtime label, reference 파일/해시를 검증한다.
5. **어댑터 지원 범위를 검증한다.** 참조가 있거나 identity 참조가 필요한 요청을 text-only 경로에서 차단한다. P0 text-only 입력의 runtime 텍스트는 감사된 composed 문장과 선택적 기존 `Avoid:` negative 구문으로 한정한다. 그 밖의 추가 문장은 미지원 입력으로 실패하며 어댑터가 삭제·완화하지 않는다. 이 제한은 API 어댑터에만 적용한다.
6. **실행할 입력을 고정한다.** `runtime_prompt_en` 문자열, 그 UTF-8 해시, model·size·`n=1`, 선택 ID, 감사 결과, 원본 binding을 immutable prepared object로 만든다. frozen dataclass만으로 안쪽 mutable dict가 보호된다고 가정하지 않는다.
7. **preflight 기록을 저장한다.** 고유 경로에 `photo-api-render-preflight/v1`을 쓰고 해시를 고정한다. pack·receipt·composed·request의 복사와 해시, source generation, 두 감사 결과, transport 지원 판정, 실제 전송 문자열/해시와 파라미터를 보존한다. 저장 실패는 API 호출 전에 종료한다.
8. **dry-run 또는 실제 호출로 분기한다.** dry-run은 API key 조회·네트워크·attempt 레저를 실행하지 않는다. 실제 호출에서는 이 시점에 key를 읽고 prepared object의 문자열을 그대로 전송한다. 감사 후 파일을 다시 읽어 입력을 갈아 끼우지 않는다.

`audit_boundary.runtime_prompt_audit_status: not_run`은 기존 v2 요청의 입력 선언이다. 별도 감사 결과를 sidecar에 저장하고 원본 request의 값을 `pass`로 덮어쓴 뒤 다시 감사하지 않는다. `inherits_composed_prompt_pass: false`도 유지한다.

전송 동일성은 **JSON을 디코딩한 `prompt` 값의 UTF-8 bytes**로 비교한다. JSON의 escaping·들여쓰기와 프롬프트 내용 변경을 혼동하지 않는다. 전송 때 `clean_spaces`, 번역, 단어 추가, negative 재결합, 모델 자동 하향 변경을 하지 않는다.

### 6.3 레저와 성공·실패 provenance

기존 레저의 `pack_id`, 선택 ID, composer, core/intent/render-repair hash, audit status, augmentation brief, 실제 호출 횟수와 retry 연결을 재사용한다. 새 API 행에는 다음 연결을 추가한다.

| 새 필드 | 의미 |
|---|---|
| `api_render_input_json` / `api_render_input_sha256` | 저장된 preflight sidecar의 경로와 정확한 파일 해시 |
| `runtime_prompt_sha256` | 전송한 문자열의 UTF-8 해시 |
| `requested_image_model` | 실제 요청 payload의 model |
| `observed_image_model` | 응답이 명시적으로 제공한 모델만 기록. 미관측이면 `null` |
| `image_size` | 전송한 size |
| `provider_request_id` | 관측한 응답 header/필드가 있을 때만 기록 |

필드는 `run_ledger.schema.json`과 `record_image_run.py`에 같이 정의한다. 역사 행에는 새 필드를 요구하지 않으며 새 API 진입점에서는 필수 연결이 빠지지 않도록 검증한다. 이미지 작성 모델과 실제 이미지 제공 모델을 혼동하지 않는다.

recorder는 sidecar의 실제 해시·통과한 감사 결과·prompt/negative·pack/선택 ID·runtime 해시·실행 파라미터를 현재 행과 비교한 뒤 append한다. 현재의 schema `additionalProperties: false`를 유지하고, 키를 임의로 붙여 우회하지 않는다.

`call_api`의 성공 반환은 이미지 bytes와 실제 관측된 response metadata를 전달하도록 바꾼다. 응답에 없는 모델 정보를 요청 model로 추정하지 않는다. API key·인증 header·`.env` 내용은 어떤 산출물에도 저장하지 않는다.

고유 실행 디렉터리와 배타적 파일 쓰기로 다른 실행의 preflight·이미지·오류 근거를 덮어쓰지 않는다. 준비 실패는 preflight 보고서에 남기고 `success/safety_block/error` attempt 레저에 실제 호출인 것처럼 추가하지 않는다.

### 6.4 실패와 재시도

| 결과 | 호출 횟수 | 후속 동작 |
|---|---|---|
| 입력·receipt·감사·transport 또는 preflight 저장 실패 | 0 | 실패 원인 보고. attempt 레저 없음 |
| API 오류 | 실제 invocation마다 1 | 전체 오류 bytes·request ID·오류 코드·같은 입력 연결 보존 |
| 명시적 policy/moderation block | 실제 invocation마다 1 | 동일 입력 자동 재호출 중단. 원문 자동 완화 없음 |
| 이미지 bytes 반환, 로컬 저장 실패 | 1 | `returned` 근거를 남기고 중단. 새 생성으로 대체하지 않음 |
| 오류 근거 또는 레저 기록 실패 | 이미 발생한 실제 호출 수 | 남은 bytes/파일·sidecar 보존 후 중단. recorder의 부분 append 여부를 확인해 기록만 복구 |
| 결과를 관측하지 못한 중단 | 발생한 호출은 보존 | 성공/차단을 추정하지 않고 미관측 결과를 별도 표시 |
| 정상 저장·기록 | 실제 호출 수 | 성공 경로와 해시 보고. 픽셀 PASS나 사용자 승인을 자동 부여하지 않음 |

다른 오류의 재시도는 기존 권한과 시도 상한 내에서만 수행한다. 모든 재시도는 같은 prepared input·prompt ID를 사용하고 바로 전 `run_id`를 `retry_of`로 연결한다. core/의미 수정이 필요하면 이 실행의 동일 입력 재시도로 처리하지 않는다. 누적 `image_call_count`의 각 행을 다시 합산하지 않는다.

[기존 오류 증거 테스트](/Users/chasoik/Projects/image-prompt/tests/test_photo_image_attempt_evidence.py)의 긴 HTTP body, 잘못된 UTF-8, body 읽기 실패, 정확한 moderation code 분류, 이미지 저장·증거·recorder 실패 시 중단 검사를 그대로 보존한다. fixture를 감사된 입력 묶음으로 바꾸되, preflight 실패 때문에 오류 경로를 시험하지 못하는 테스트로 약화하지 않는다.

### 6.5 API 검증 사례

| 사례 | 기대 결과 |
|---|---|
| `prompt_en`만 있는 과거 우회 입력 | 전송 0회, 준비 실패 |
| JSON의 self-declared PASS, 실제 composed 위반 | 전송 0회, fresh audit 실패 |
| pack ID/core/intent/repair/visual hash 변조 | 전송 0회, 해당 binding 실패 |
| 잘못된 receipt, generation 또는 구현/환경 불일치 | 전송 0회. latest/legacy fallback 없음 |
| negative 한 글자 변경, 추가 `Avoid:` 결합, composed 불연속 | 전송 0회 |
| runtime 금지 label 또는 미지원 추가 문장 | 전송 0회, 삭제 후 자동 호출 없음 |
| 참조 파일 누락·해시 변경 또는 유효 참조가 있는 요청 | 전송 0회. 유효 참조도 text-only에서 미지원 |
| 실제 참조가 필요한 identity 계약, 빈 reference 목록 | 전송 0회. 텍스트 설명으로 대체 금지 |
| 다중 JSON 객체 목록, 0/음수 시도 수 | 입력 오류, 전송 0회 |
| 유효 text-only 요청의 dry-run | 감사 통과, key 조회 0회·네트워크 0회·attempt 행 0개 |
| 유효 요청 실제 호출을 대체한 성공 | 전송 1회. decoded prompt UTF-8 동일, 이미지 hash·레저·sidecar 연결 일치 |
| 감사 후 원본 파일 변경 | 고정한 prepared input만 전송. 변경 파일 재독해 금지 |
| API 오류·moderation·저장·레저 실패 | 위 정책의 호출 수·원문 오류 보존·중단 검증 |
| 제공자가 model 정보를 돌려주지 않음 | requested model 기록, observed model `null` |
| 레저에 연결한 sidecar 변조 | append 전에 해시/binding 실패 |

실제 네트워크 함수는 테스트에서 호출되면 실패하게 하고, 필요한 provider 응답은 fake HTTP response로 제공한다. preflight 정상 사례는 기존 실제 감사기를 사용한다.

## 7. 변경 파일과 영향 범위

| 파일/범위 | 변경 내용 |
|---|---|
| [prompt_generator.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py) | 축·관계·문맥 진단, clarification 투영, 클래스 matcher, advisory 축 validator |
| [캐릭터 작성 데이터](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_character_moe_extension.json) | 검토된 alias, 얀데레의 추가 축만 보조 이동 |
| [compose_pack_view.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/compose_pack_view.py) | 새 진단의 요약·상세 보존 |
| [audit_composed_prompt.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py) | clarification v2, pinned source 재계산과 변조 검증 |
| [generate_images_via_api.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/generate_images_via_api.py) | 필수 입력 CLI, preflight, immutable 전송, 호출/저장/기록 연결 |
| [audit_image_render_request.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_image_render_request.py) | 기존 감사 재사용. 꼭 필요한 API 지원 범위 검사는 어댑터에 둠 |
| [record_image_run.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/record_image_run.py), [레저 schema](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/run_ledger.schema.json) | 새 sidecar·전송·모델 provenance 검증과 schema 동기화 |
| [photo_runtime_sources.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_runtime_sources.py) | 기존 receipt 기능 재사용. 필요 없는 최신성 시스템 재설계 금지 |
| semantic index·source manifest | 작성 데이터 변경으로 필요한 hash/derived output 갱신 |
| SKILL 및 retrieval-contract/image-runtime/maintenance references | 정확한 사유·새 API 명령·한계·역사 재생 안내만 갱신 |
| 관련 기존 테스트와 신규 테스트 | 진단·실행 경계·부정/관계·오류 기록 반례 |

신규 테스트 제안: `tests/test_photo_meaning_diagnostics.py`, `tests/test_photo_api_render_preflight.py`. 신규 경로는 계획이며 아직 생성되지 않았다. 기존 helper의 미감사 공개 진입점을 제거할 때 다른 현재 호출자를 검색해 함께 갱신한다. 역사 보고서·보존된 fixture·서브컬처 스킬을 blanket 치환하지 않는다.

## 8. 검증 및 runtime 세대 갱신

테스트 명령은 구현 후 적용할 목록이다. 이번 계획 작성에서 테스트 통과나 구현 완료를 주장하지 않는다.

### 8.1 진단·어휘 변경

```bash
.venv/bin/python -m unittest \
  tests.test_photo_meaning_diagnostics \
  tests.test_photo_character_response_concepts \
  tests.test_photo_visual_profile_retrieval \
  tests.test_photo_composer_view \
  tests.test_photo_authorial_core_v6 -v
```

기존과 새 구현을 같은 고정 입력에서 비교해 단계 1의 허용·거부 불변과 단계 3의 의도된 delta를 별도 JSON으로 기록한다. 출력 전체 golden을 무조건 다시 저장하지 않고 변경된 사유·근거·활성화만 검토한다.

### 8.2 API 경계·기록·하위 계약

```bash
.venv/bin/python -m unittest \
  tests.test_photo_api_render_preflight \
  tests.test_photo_image_attempt_evidence \
  tests.test_photo_run_manifest \
  tests.test_photo_visual_obligations \
  tests.test_photo_embodiment \
  tests.test_photo_render_repair \
  tests.test_photo_runtime_freshness -v
```

별도 임시 runtime store와 output/ledger 경로를 사용한다. 실제 API key나 공유 레저를 사용하지 않는다. CLI subprocess에서도 정상/누락/변조/dry-run을 확인해 함수 테스트만으로 끝내지 않는다.

### 8.3 불변 조건과 문서

```bash
.venv/bin/python -m unittest \
  tests.test_photo_prepack_isolation \
  tests.test_photo_authorship_policy \
  tests.test_photo_adult_appeal_scope -v
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
```

바뀐 표면에 해당하는 검사를 수행한다. 통과한 검사를 이유 없이 반복하거나 공유 파일을 건드렸다는 이유만으로 전체 suite를 매 단계 실행하지 않는다. 서로 독립적인 조회 경로가 함께 달라지거나 해결되지 않은 회귀 위험이 발견되면 그때 범위를 넓힌다.

### 8.4 DATA와 index의 순서

- 단계 1은 진단 코드 변경이므로 source generation을 새 구현으로 검증·발행한다. 작성 텍스트가 안 바뀌면 불필요한 embedding 재생성을 하지 않는다.
- 단계 3은 alias·profile schema 변경이므로 dictionary/source hash와 semantic index를 갱신한다. metadata만 맞춰 바꾸지 않고 현재 builder로 derived output을 재계산한다.
- 기존 vector는 검색 텍스트 bytes·provider·model·dimension이 동일한 항목만 재사용한다. 새 텍스트에 embedding이 필요하면 변경된 항목만 처리하고 현재 유지보수의 batch size 1 규칙을 따른다. 이를 ‘네트워크 호출 0회’ 검증과 분리해 비용·실행 사실을 기록한다.
- visual registry 내용이 같으면 visual vector 재생성을 목표로 삼지 않는다. 상위 source binding 변화 때문에 필요한 manifest 갱신은 현재 builder의 검사 결과에 따라 수행한다.
- 기존 cooperative source-update/완료/publication 절차를 사용한다. pending 상태나 잘못된 index를 hidden fallback으로 통과시키지 않는다. 새 worker에서 테스트하고, 과거 receipt의 generation을 최신 것으로 덮어쓰지 않는다.

## 9. 검토 단위와 단계별 종료 조건

| 순서 | 검토 단위 | 종료 조건 |
|---|---|---|
| 0 | 재현 입력·반례·정상 API fixture | 입력 hash, 현재 결과, 기대 결과가 고정됨. 외부 호출 없음 |
| 1 | P0-1A 진단·뷰·clarification 감사 | 기존 판정 동작 유지. 누락/미인식/구조 차이/문맥 미인식 설명 정확. 진단 변조 차단 |
| 2 | P0-2 API CLI·preflight·레저·문서 | 유효 입력만 전송. invalid/dry-run은 0회 호출. 원문 전송·오류·저장/기록 중단 규칙 검증 |
| 3a | P0-1B alias·극성 matcher | 확인된 표현 delta만 발생. 부정·불명확 극성의 긍정 자동 PASS 없음 |
| 3b | 얀데레 보조 축·validator·derived data | 해당 추가 축만 blocking에서 제외. 핵심 의미와 다른 프로필 불변, index 최신성 통과 |
| 4 | 통합·문서·소스 세대 전달 | 최종 소스에서 진단 → composed audit → API dry-run → fake provider 기록이 한 묶음으로 연결 |

검토 단위는 리뷰 가능한 변경 묶음이다. 이 계획만으로 commit·push·PR 생성·이미지 실행을 수행하는 것은 아니다. 구현 결과에는 각 단위의 scoped diff, 검증 로그, 기대/실제 delta와 최종 runtime generation을 남긴다.

## 10. 최종 완료 기준과 복구

다음 조건을 모두 충족하면 P0 완료로 판정한다.

- 동일한 동결 원문에 대해 진단의 원인·원문·작성 규칙·실제 구조가 연결된다. 값 미인식이 누락/모순으로 둔갑하지 않는다.
- 검토된 의미 대응 표현은 인식되고, 다른 상대·부정·선후 반전·사용자 정의 우선순위는 계속 구별된다.
- API 진입점에 미감사 raw prompt 우회 경로가 없다. receipt·두 감사·지원 범위 검증 실패 시 실제 호출이 0회다.
- 정상 전송은 감사한 runtime 문자열과 UTF-8 해시가 같다. 성공/실패 행이 정확한 preflight·source·pack·선택·모델 요청에 연결된다.
- 실제 오류 bytes 보존, 잘못된 UTF-8 처리, 정확한 block 분류, 저장/기록 실패 시 중단과 retry 연결이 기존보다 약화되지 않는다.
- 스키마·recorder·CLI·실행 안내가 일치하며 기존 unrelated 작업과 역사 산출물을 보존한다.
- 최종 보고서가 구현·오프라인 검증·index API 사용 여부·실제 이미지 호출 여부·픽셀/사용자 평가 여부를 따로 명시한다.

문제가 생기면 새 source generation의 사용을 멈추고 이전 generation과 호환되는 sealed worker를 선택한다. alias/보조 축 변경은 해당 작성 데이터와 그 derived generation 단위로 되돌린다. 공유 레저나 과거 입력을 수정해 정상처럼 보이게 만들지 않는다. 이미 반환된 이미지의 저장·레저 문제는 보존된 파일/bytes와 sidecar로 복구하고 새 이미지 호출을 하지 않는다.

이번 계획의 검증 수준은 소스·계약·전송 경계다. 실제 서비스 성공률과 사진 품질을 개선했다는 주장은 여기서 도출하지 않는다.

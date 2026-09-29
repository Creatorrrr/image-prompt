# Photo Prompt 스킬 레거시 제거 계획

- 작성일: 2026-09-29
- 대상: `photo-prompt-image-generator`와 저장소 안의 실제 호출부·검증 코드
- 조사 기준: `c432b515b37739b04f88555b9802040c1fbd8921`, 작성 시작 시 작업 트리 변경 없음
- 상태: 1–6단계 구현·데이터 전환·로컬 회귀 검증 완료. 기존 실패와 외부 API 검증 제한은 8절에 기록.

## 1. 목표와 범위

현재 스킬의 V6 흐름을 기준으로, 과거 스킬 버전의 입력·출력·검증 결과를 계속 받아주기 위한 코드와 테스트를 제거한다. 구형 입력은 명확한 오류로 거부하고, 자동 변환·호환 모드·이중 출력을 남기지 않는다.

사용자는 과거 버전 호환성이 필요 없다고 명시했다. 따라서 현재 maintenance 문서에 있는 구형 직렬화 결과·V5 라우터·과거 정책 재현 보존 지침도 이번 작업에서 함께 수정한다.

작업 범위에는 생성기, 래퍼, composed/runtime/pixel 감사기, composer view, 실행 기록, 의미 평가기, 인덱스 입출력, 관련 테스트와 문서를 포함한다. 다른 스킬은 사진 스킬을 호출하는 회귀 검증 경계만 수정한다.

기존 실행 기록·이미지·연구 자료의 원본과 해시는 보존한다. 앞으로 생성하는 결과의 `pack_id`와 해시는 변경될 수 있다. 과거 결과의 바이트 단위 재현은 완료 조건에 포함하지 않는다.

## 2. 지원 계약을 하나씩 확정

| 영역 | 작업 후 지원 형태 | 전환 내용 |
| --- | --- | --- |
| Candidate pack | `photo-candidate-pack/v6` | V2–V5 생성·투영·읽기·감사 지원 제거. CLI 기본값 V4 → V6 |
| 요청과 core | `photo-request-envelope/v1` + `photo-authorial-core/v3` | `authorial-request/v1`, core V1/V2 제거 |
| Intent lock | `photo-intent-lock/v2` | 현재 V1 예제·fixture를 V2로 전환. 전체 차원 잠금과 속성별 잠금 모두 유지 |
| 초기 creative controls | 현재 V2 snapshot 및 core 결합 | 정상 공개 생성 경로에서 snapshot·해시 결합 필수. 미결합 입력의 구형 adult-appeal 경로 제거 |
| Authorship | policy V2 + core binding V3 | 구형 추가 문구·결정 최소 개수 및 무표식 정책 추정 제거 |
| Prompt budget | `photo-authorial-prompt-budget/v2` | V1·무표식 예산 및 과거 moe 예산 해석 제거 |
| Candidate semantics | semantic surface V1 + 해당되는 bundle V1 | 현재 표식 검증 필수. 구형 팩을 위한 표식 누락 통과 제거 |
| Contextual appeal | contextual appeal V2 + dimension scope V4 | 구형 scope V1/V2와 preset 기반 호환 후보 조회 제거 |
| Embodiment | 현재 review V1 + preflight V1 | 현재 V6 정책·결합 필수. 비적용 대상은 명시적 `not_applicable` 유지 |
| Composer view | `photo-composer-view/v2` | V1 생성·검증 제거 |
| Render request | `photo-image-render-request/v2`, core V3 | 이미 V2인 요청 형식은 유지하고 core V2 수용만 제거 |
| 실행 manifest | `photo-independent-run-manifest/v2`, pack V6 | 구형 manifest 생성·버전별 결합 분기 제거 |

버전 숫자가 작다는 이유로 삭제하지 않는다. `photo-visual-intent/v1`, negative-intent guard, typed character response, semantic assertions, `moe-render-review/v1` 등은 현재 계약이다.

`--candidate-pack-version`은 값 `v6`만 허용하고 기본값도 `v6`로 둔다. 기존 명령의 형식 표시 용도로 유지하되 내부 버전 분기는 없앤다. `--legacy-replay-reason`과 `--authorial-request-json`은 제거한다.

사용자용 생성 진입점은 결합된 현재 core를 요구한다. core 없이 직접 샘플러 출력을 읽는 기존 평가·진단 호출은 내부 진단 인터페이스로 옮긴다. 목록 조회와 데이터 검증 같은 비생성 명령에 core를 요구하지는 않는다.

## 3. 제거 대상과 선행 작업

| 대상 | 제거할 내용 | 먼저 해야 할 일 |
| --- | --- | --- |
| 팩 조립 | V2 기본 팩 → V4 → V5 → V6 투영 사슬 | 현재 V6에 필요한 후보·privacy·제약 투영을 버전 독립 함수로 추출 |
| 구형 core | core V1/V2 정규화, 구형 source/provenance, `superseded_by_revision` 처리 | 현재 테스트 입력을 envelope + core V3로 전환 |
| Raw moe 라우터 | `resolve_moe_response_intent`, 구형 `moe_response_contract/v10`, 관련 directive·감사·pixel gate 분기 | typed character response 및 일반 semantic assertion 경로에 필요한 공통 로직 분리 |
| 옛 장면·adoption 계약 | V2/V3 selected blueprint, `atomic_scene` 공개 계약, 구형 `accepted/modified` 해석, V4 hybrid 계약 | 현재 scene 후보·bundle·관계 검증은 유지하고 옛 출력 스키마 전용 부분만 분리 |
| Adult appeal | `candidate_pack_legacy_adult_appeal`의 preset·axis tag 기반 호환 경로와 옛 adoption 예산 | 현재 contextual appeal이 재사용하는 activation·binding·combination 메타데이터 추출 |
| 구형 정책 허용 | authorship V1·무표식 minima, 구형 prompt budget, 없는 embodiment/semantic 표식 수용 | 모든 현재 fixture에 정상 정책을 넣고 누락·변조 시 실패하도록 전환 |
| 래퍼 | `concept-mode legacy`, 암묵적 legacy 기본값, legacy 전용 preset/slot 강제 주입 | 현재 soft 동작을 단일 concept 처리로 만들고 진단 호출을 이식 |
| 평가기 | V3 replay를 통한 내부 선택 관찰, `required_legacy_choices`, 품질 gate의 `legacy_passed` | 현재 샘플러의 내부 진단 결과를 직접 읽는 평가 인터페이스로 교체 |
| 이름·데이터 호환 | V3 profile/ID 변환, `soft_body_first_guard.slot` 단수 fallback | 사용 중인 authored data와 참조를 정식 ID·`slots` 형식으로 전환 |
| Extension 메타데이터 | `LEGACY_MAINTENANCE_KEYS`의 옛 문서 필드 예외 | 설명·출처를 현재 maintenance reference 구조로 옮긴 뒤 허용 예외 제거 |
| 보조 산출물 | composer view V1, manifest V1, 구형 pack/core의 감사 수용 | 현행 view·manifest·runtime fixture를 먼저 준비 |
| 의미 인덱스 | 최종 인덱스 `--monolithic` 쓰기와 구형 단일 파일 읽기 | 빌드 재개 checkpoint reader와 최종 shard reader를 분리 |

주요 근거:

- [팩 버전·기본값](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py), [V6 → V5 호출](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py), [현재 appeal의 legacy 함수 재사용](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py)
- [감사기의 구형 authorship 정책](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/audit_composed_prompt.py), [래퍼 기본 모드](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/generate_photo_prompt.py)
- [Composer view 두 버전 수용](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/compose_pack_view.py), [실행 기록 버전 분기](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/record_image_run.py)

## 4. 구현 순서

### 1단계 — 현재 입력과 테스트 기반 정리

1. 현재 정상 흐름의 envelope, controls snapshot, core V3, intent lock V2, embodiment review를 만드는 공통 fixture helper를 분리한다.
2. V5 테스트 모듈의 helper를 가져오는 현재 adult-appeal·authorship·creative-controls 테스트를 새 helper로 옮긴다.
3. 파일명에 V2/V5가 있는 테스트도 검사 내용별로 분류한다. 현재 의미·해시 결합·pre-core 격리 테스트는 이식하고, 구형 결과 재현만 검증하는 테스트는 제거 대상으로 기록한다.
4. 현재 정상 fixture의 후보 의미, 필수 의무, 공개 필드, 선택 후보의 선택성, 해시 결합을 변경 전 기준으로 확보한다. 기존 실패가 있으면 결과에 구분해 기록한다.

완료 기준: 현재 기능 테스트가 구형 테스트 파일의 helper에 의존하지 않고, 이후 비교할 현재 기능의 기준이 준비됨.

### 2단계 — 실제 호출부와 평가기 전환

1. `eval_semantic.py`의 generalization/retrieval holdout이 V3 출력으로 관찰하던 내부 선택 결과를 명시적 진단 인터페이스로 옮긴다. 이 진단 필드는 V6 공개 팩에 노출하지 않는다.
2. `legacy`/`soft` 이중 benchmark를 현재 동작 평가로 정리한다. 의미 보존·후보 coverage·diversity·bleed·guard 검증은 유지한다.
3. illustration 스킬의 사진 회귀 검증을 정상 결합 입력을 갖춘 V6 호출로 전환한다. 새 current baseline을 만들고 기존 baseline 원본은 보존한다.
4. 해당 호출부의 테스트와 현재 사용 설명의 명령도 함께 바꾼다. 평가용 자연어 사례와 holdout의 의미상 기대 결과는 그대로 유지한다.

확인된 외부 호출부는 [validate_photo_regression_baseline](/Users/chasoik/Projects/image-prompt/skills/subculture-illustration-image-generator/scripts/validate_illustration_assets.py)이다. 현재는 V4를 강제하고 실제 생성 명령을 실행하므로, 사진 스킬만 수정하면 이 경계 검증이 깨진다.

완료 기준: 실행 중인 평가·테스트가 V2–V5 출력, legacy concept 모드, 구형 replay 옵션을 요청하지 않음.

### 3단계 — V6 조립과 현재 데이터 구조 독립

1. 현재 privacy projection, 후보 정리, 생성 제약, augmentation 메타데이터를 버전 독립 함수로 추출한다.
2. V6를 직접 조립하도록 바꾼다. V2 공개 스키마를 중간 자료형으로 만들거나 V4/V5 projector를 거치지 않는다.
3. 현재 contextual appeal의 공통 메타데이터를 분리하고 legacy 후보 조회 호출을 없앤다.
4. active ID 참조, 단수 `slot` 필드, extension 문서 메타데이터를 현재 형식으로 정규화한다. 언어·표현 동의어용 aliases는 유지한다.
5. checkpoint 읽기와 최종 인덱스 읽기를 분리한다. 현재 shard의 entry 순서·해시 검사와 빌드 재개·벡터 캐시 재사용을 유지한다.

완료 기준: 현재 V6 생성과 인덱스 빌드가 구형 공개 스키마·호환 함수에 의존하지 않으며, 1단계의 현재 의미·필수 의무·privacy 기준을 만족함.

### 4단계 — 구형 분기와 수용 경로 제거

1. 3절의 구형 CLI, 버전별 normalizer/projector, raw moe 라우터, 옛 정책·예산 분기를 삭제한다.
2. generator와 각 감사기·viewer·기록기가 같은 현재 계약 집합만 허용하도록 맞춘다. 현재 정책 표식이 빠진 V6도 구형 기본값으로 보충하지 않고 오류 처리한다.
3. `audit_v4_authorial_pack`, `audit_authorial_core_v5`처럼 현행 검증도 수행하는 함수는 내용부터 분리한 뒤 역할에 맞는 이름으로 바꾼다.
4. 구형 pack/core/view/manifest의 거부를 경계별로 검증한다. 삭제한 옵션은 명확한 CLI 오류가 나야 한다.
5. 기능 코드를 검토해 사용처가 사라진 구형 전용 데이터만 제거한다. scene 후보, typed character graph, 현재 의미 검색 데이터는 남긴다.

완료 기준: 구형 입력의 생성·자동 변환·감사 성공 경로가 없고, 현재 모든 공개 진입점이 동일한 계약을 적용함.

### 5단계 — 테스트·문서·인덱스 마무리

1. 구형 호환 성공 테스트는 제거한다. 현재 의미를 검증하던 테스트는 V6 입력으로 유지하고, 필요한 구형 입력 거부 테스트만 추가한다.
2. SKILL, maintenance, composer/runtime 가이드의 버전·필수 입력·예제를 통일한다. `moe-response-legacy.md`와 그 참조는 현재 배포 대상에서 제거한다.
3. 인덱스에 영향을 주는 authored data·텍스트·BM25F 정책이 바뀐 경우에만 필요한 인덱스를 갱신한다. 동일 입력의 기존 벡터를 재사용하고, 단순 호환 코드 삭제만으로 전체 재임베딩하지 않는다.
4. `legacy`, `compat`, `v2/v3/v4/v5`, 구형 옵션·함수명을 재검색한다. 남은 항목을 현재 기능, 보존된 기록, 거부 테스트로 설명할 수 있어야 한다.

완료 기준: 활성 문서·테스트·데이터와 런타임의 지원 범위가 일치하고, 필요한 인덱스 해시 검사도 통과함.

### 6단계 — 회귀 검증과 결과 정리

1. 아래 핵심 시나리오와 변경 파일에 대응하는 집중 테스트를 실행한다.
2. 의미 평가, dictionary/scene 검증, 두 종류 인덱스 검사를 실행한다.
3. 생성·감사·평가·다른 스킬의 호출 경계를 함께 바꾸므로 마지막에 저장소 전체 테스트를 한 번 실행한다. 실패 시 원인을 확인하는 범위만 재실행한다.
4. 제거한 경로, 유지한 현재 기능, 실행한 검증, 기존 실패와 새 실패 유무를 정리한다.

완료 기준: 현재 기능의 의미상 회귀와 새 테스트 실패가 없고, 구형 지원 경로가 제거됐다는 코드·호출부 검토가 끝남.

## 5. 검증 시나리오와 실행 범위

| 시나리오 | 확인할 내용 |
| --- | --- |
| 정상 생성과 선택성 | 결합된 V6 생성, non-human/no-people, 의미·후보·privacy 유지, 후보를 선택하지 않는 경우도 정상 처리 |
| Core·controls·잠금 | 요청 원문·snapshot 해시 보존, 명시적 0, 전체·속성 잠금, 열린 차원 0개, baseline 유지와 빈 추가 결정 허용 |
| Typed 의미와 후보 | character response와 일반 assertion의 필수 evidence, 관계, 선택 bundle의 구성요소·gate, raw moe 라우터 제거 후 동작 |
| 검색·평가 | exact activation, optional semantic hit, 부정·동음이의·문맥 불일치, frozen holdout 기대 의미 유지 |
| 리뷰와 재시도 | embodiment 해당/비해당, stale prompt·미해결 검토 실패, 일반 retry와 prop repair의 보존 조건 |
| 전달과 기록 | composer view의 원본 hash, runtime 원문 결합, reference hash, 성공·차단된 실행의 manifest와 ledger |
| 구형 입력 거부 | V2–V5 pack, core V1/V2, view/manifest 구형 버전, 삭제 옵션, 필수 현재 정책 누락·변조 |
| 저장소 내 경계 | illustration의 V6 회귀 baseline, shard 최종 인덱스 읽기, checkpoint 재개, 동일 텍스트 벡터 재사용 |

집중 테스트는 현재의 `test_photo_authorial_core_v6`, `test_photo_authorship_policy`, `test_photo_initial_creative_controls`, `test_photo_adult_appeal_scope`, `test_photo_contextual_appeal`, `test_photo_candidate_semantics`, `test_photo_embodiment`, `test_photo_composer_view`, `test_photo_render_repair`, `test_photo_run_manifest` 및 이식한 pre-core 격리 테스트를 포함한다. raw moe 제거는 character/visual obligation·render-review 테스트도 함께 확인한다.

공유 호출부는 `test_subculture_illustration_photo_boundary`, `test_subculture_illustration_universal_scene_v3`, `test_subculture_illustration_moe_elements`의 사진 경계 검증을 확인한다. 테스트 이름은 실제 이식 결과에 맞게 갱신한다.

검증 명령은 다음과 같다. 저장소 루트에서 실행하며 실제 결과는 마지막 실행 기록에 정리한다.

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python skills/photo-prompt-image-generator/scripts/audit_scene_expression.py --current --compact
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --check-index
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --generalization-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --retrieval-holdout-check
.venv/bin/python skills/photo-prompt-image-generator/scripts/eval_semantic.py --quality-gate --quality-runs 2 --summary-only
git diff --check
```

평가기와 인덱스 검사는 기존 로컬 인덱스를 사용한다. 누락·stale 인덱스로 외부 API 호출이 필요해지는 경우는 별도 재생성 작업으로 명시하고, 오프라인 대체 결과를 실제 semantic 평가 통과로 기록하지 않는다.

## 6. 이번 제거에 섞지 않을 현재 기능

- **일반 retry lineage:** 현재 무버전 4필드 형태도 일반 재시도에 쓰인다. `photo-request-lineage/v2`는 `repair_targets`가 필수인 소품 수리용 확장이므로 단순 치환하면 일반 재시도가 사라진다. 이 기능은 유지하고 `legacy_fields` 같은 혼동되는 내부 이름을 정리한다.
- **현재 `/v1` 계약과 pixel gate 통합:** `moe`라는 파일명만 보고 render-review 감사기 전체를 삭제하지 않는다. 현재 typed·visual·embodiment gate 통합과 `partial_is_fail` 검증을 유지한다.
- **현재 검색·진단 fallback:** 오프라인 rule 모드, 현재 빈 후보 처리, domain facet 추론은 실제 호출 목적을 확인한다. 과거 버전 수용만을 위한 것으로 확인되지 않은 검색 동작은 이번 작업에서 변경하지 않는다.
- **Checkpoint와 별도 visual-profile index:** 최종 semantic index의 monolithic 호환 제거 범위를 넘어서 빌드 재개 파일이나 별도 visual-profile 인덱스 형식을 없애지 않는다.
- **증거·결과 보존:** 과거 runs·이미지·연구 기록의 삭제, 원본 해시 재작성, 구형 결과의 일괄 재감사는 하지 않는다. 필요시 과거 구현을 Git에서 확인한다. 현재의 historical-catalog 검사는 기록의 출처 검증 기능으로 유지한다.
- **이미지 품질 주장:** 이 작업의 완료 근거는 현재 계약·의미·호출부의 회귀 검증이다. 이미지 생성과 예술적 품질 평가는 이번 계획의 실행 범위에 포함하지 않는다.

## 7. 최종 완료 조건

1. 현재 pack/core/policy/view/manifest 계약만 생성·수용하며, 삭제한 입력과 옵션은 명확히 실패한다.
2. V6는 V2 기반 자료형, V4/V5 projector, raw moe 라우터, 구형 adult inventory 함수를 거치지 않는다.
3. 현재 의미·잠금·선택 후보·필수 gate·원문/해시 결합·pre-core 격리가 유지된다.
4. 평가기와 illustration 호출부가 현재 경로를 사용하고, 현재 기능 테스트가 구형 helper에 의존하지 않는다.
5. 새 회귀 실패가 없으며, 구형 지원 재현만을 위해 존재한 테스트·문서·예외가 정리된다.
6. 보존 대상인 과거 결과·연구 증거의 원본과 해시는 변경되지 않는다.

구현은 1–6단계 순서로 진행한다. 검토 가능한 변경 단위로 나누되, 최종 상태에 임시 호환 adapter나 `allow_legacy` 우회 옵션을 남기지 않는다.

## 8. 실행 기록

### 적용한 변경

- 공개 생성·감사·view·manifest를 위의 현재 계약 집합으로 통일했다. 구형 pack/core/정책, 구형 옵션과 필수 표식 누락은 오류가 된다.
- V6 조립을 현재 역할의 함수로 분리하고, raw moe 라우터·고정 hybrid route·구형 adult inventory·core 가설 교체·누락된 샘플러 이력을 preset 필터로 보충하는 경로를 제거했다.
- Python에 남아 있던 기본 slot-context 호환 규칙과 `builtin_slot_context_rules` 전환 플래그를 제거했다. 현재 데이터의 선언형 호환 규칙은 유지한다. 정책이 없는 진단의 표기도 `legacy-code-policy`에서 `unconfigured-policy`로 정리했다.
- `inspect_photo_sample.py`를 내부 샘플러 진단 진입점으로 분리했다. `photo-sampler-diagnostic/v1`은 공개 팩의 생성·감사 계약을 대신하지 않는다.
- concept 처리를 soft 모드로 통일했다. 일반화·검색 평가, 회귀 테스트와 illustration의 사진 호출부를 현재 입력 또는 명시적 진단으로 전환했다.
- 기존 V1–V3 illustration baseline과 기존 golden 파일을 보존하고, 실제 V6 호출용 `photo_regression_baseline_v4.json` 및 `tests/golden/current_sampler/`를 추가했다.
- illustration의 사진 호출부 수정으로 검증기 파일의 해시가 달라져, 현재 universal-scene baseline의 검증기 해시만 갱신했다. 이전 baseline 원본은 `docs/research-evidence/photo-prompt/legacy-removal-20260929/universal_scene_baseline_v2.json`에 바이트 그대로 보존했다.
- 현재 ID 참조·복수 `slots` 형식을 정리하고 extension 설명을 외부 maintenance 기록으로 보존했다. 완성된 의미 인덱스는 shard 형식만 받으며 별도 checkpoint의 재개 기능은 유지한다.
- 최종 의미 인덱스는 `b48bacd2edc7727f` 세대다. 기존 벡터 9,650개를 동일 텍스트로 모두 재사용했고 새 임베딩은 생성하지 않았다. 이번 작업의 사용하지 않는 중간 shard 세대는 `/tmp/photo-unused-index-generation-cf7c27ece215a641`에 옮겼다.

### 검증

| 항목 | 결과 |
| --- | --- |
| 변경 전 핵심 계약 기준 | 88 tests 통과 |
| 일반화 평가 | 79/79 사례 통과 |
| 실제 semantic retrieval holdout V4 | 22/22 사례 통과 |
| 장면 구조 | 112/112 경로 통과 |
| Dictionary | 최종 상태 검사 통과 |
| 의미 인덱스 | 최종 hash·recipe·vector 차원·9,650 entries 검사 통과 |
| Visual-profile index | 988 profiles / 2,509 exact terms 검사 통과 |
| 현재 계약 집중 재검증 | current boundary·core·authorship·render review·appeal scope·embodiment 86 tests 통과 |
| Illustration 경계·universal scene | 47 tests 통과 |
| 추가 호출부 집중 재검증 | beastkin·role garment·reactor·makeup·wizard·yandere 9 tests 통과 |
| 현재 golden | 별도 현재 fixture로 3 tests 통과 |
| Visual obligations | 26 tests 중 25개 통과. 나머지 1개 테스트의 실패 8개 subcase가 원래 코드의 사례·후보 목록과 정확히 일치 |
| 전체 로컬 회귀 | 1,262개를 116개 배치로 실행. 84개 배치 834 tests 통과, 초기 실패 32개 배치의 원인을 확인하고 집중 재검증 |
| 정적 확인 | 변경 Python 48개와 JSON 문법, `git diff --check` 통과. 삭제한 함수·모듈·옵션의 활성 참조 없음 |
| 외부 API를 쓰는 전체 품질 gate | `Network is unreachable`로 중단. 완료·통과로 계산하지 않음 |

전체 실행은 fixture 이식과 함께 진행되어 수정 전 테스트를 이미 읽은 배치도 포함한다. 반복적인 인덱스 생성으로 오래 걸리던 visual-obligations 배치 하나는 중단했고, 실제 생성한 인덱스를 복사·재사용하도록 테스트 helper를 바꾼 뒤 26개 모듈 검사를 다시 실행했다. 입력 registry의 해시를 매번 확인하며, 고정 사례·기대값·라우팅 로직은 바꾸지 않았다. 전체 테스트가 한 번에 모두 통과했다는 의미로 해석하지 않는다.

시각 라우팅의 남은 지연을 측정한 결과, 한 사례의 17.059초 중 정규식 컴파일이 15.916초였다. 인덱스만 재사용한 중간 실행도 중단하고, 최종 비교 실행에서는 테스트 프로세스의 CPython 정규식 캐시 용량만 65,536 / 32,768로 늘렸다. 실제 매칭 함수·패턴·기대값과 제품 런타임의 캐시 설정은 그대로다.

변경 전 인덱스와 현재 인덱스에서 `도내 1등 초절정 미소녀 지역 평판 여러 사람 시선`의 BM25F 상위 12개 결과는 동일하다. 기존 `test_semantic_index_ranks_new_keyword_families_near_the_top`은 `multi_observer_recognition_cue`를 상위 6개에 요구하지만 두 인덱스 모두 7위라 실패한다. 이 기대값은 완화하지 않았다. 경찰 role-scene의 기존 테스트는 데이터에 없는 세 장소를 요구하고 있었으므로, 변경 전부터 사용 중인 `controlled_public_safety_perimeter`를 검증하도록 fixture를 정리했다.

변경 전부터 존재한 실패도 보존했다. `test_skill_fail_closes_uncovered_focal_meaning`이 요구하는 네 문장은 원래 SKILL에도 없었고, `test_retrieval_holdout_and_research_evidence_contracts_are_versioned`의 영문 상투구 검사와 맞지 않는 기존 연구 기록 40개도 원본 그대로다. 전통 의상 frozen routing의 여섯 사례는 변경 전 HEAD 코드에서도 같은 추가 후보를 반환했다. 관련 원본 비교 결과와 전체 실행 메타데이터는 `docs/research-evidence/photo-prompt/legacy-removal-20260929/`에 저장했다.

일반 시각 라우팅 120개와 별도 holdout 14개도 변경 전 코드로 전부 비교했다. 일반 라우팅의 `positive_inner_thigh_en`, `candidate_contained_affect_components`, `positive_yandere_en`, `positive_yandere_ko`, `candidate_yandere_relation_components`, `negative_yandere_expression_only`, `negative_yandere_role_prop_only`, `candidate_kuudere_relation_components`에서만 기존 추가 후보가 나왔으며, 현재 테스트의 실패 사례와 반환 후보 목록이 모두 일치했다. 14개 holdout은 통과했다. 기대값을 완화하거나 해당 사례를 제외하지 않았다.

집중 재검증과 원본 비교에서 새 회귀 실패는 확인되지 않았다. 검증 결과 요약은 [verification.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/legacy-removal-20260929/verification.json), 마지막 시각 비교는 [visual-routing-comparison.json](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/legacy-removal-20260929/visual-routing-comparison.json)에 있다. 과거 runs·이미지·연구 증거와 고정 fixture의 기존 추적 파일은 변경하지 않았다.

이 검증은 코드·데이터·계약의 회귀 확인이다. 이번 작업에서 이미지 생성, 픽셀 품질 평가, 사용자 선호 판정, commit 또는 push는 수행하지 않았다.

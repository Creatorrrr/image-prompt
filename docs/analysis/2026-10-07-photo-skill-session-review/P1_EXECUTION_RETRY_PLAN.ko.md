# P1 상세 계획: 단계 실행 도구와 재시도 허용 정보 추출

작성일: 2026-10-07. 기준 커밋: 51efe32e7fa9e8ced47f03f397932dd150a02f03.

이 문서는 [기존 개선 보고서](./REPORT.ko.md)의 P1-1과 P1-3을 구체화한 구현 계획이다. 아래의 새 파일, CLI, 스키마, 상태값은 제안이며 현재 구현되어 있지 않다. P0의 의미 진단과 감사된 API 진입점은 이미 구현되어 있다. 현재 턴에서는 계획 문서만 작성한다.

## 1. 목표와 완료 범위

목표는 에이전트가 의미와 사진을 판단하는 동안 반복되는 JSON 연결, SHA 계산, 플래그 구성, 부모 정보 선별, 실행 기록 연결을 도구가 맡게 하는 것이다. 단계 실행 도구와 재시도 추출기는 같은 실행 상태와 산출물 참조를 공유한다.

완료 시 다음 흐름을 제공한다.

1. 원문과 에이전트가 지정한 범위로 envelope와 현재 설정을 준비한다.
2. 에이전트가 기본안·의미·범주·신체 검토를 작성하면, 중립 도구가 검증하고 동결한다.
3. 동결 산출물로 정확히 한 외부 pack과 그 receipt를 생성한다.
4. 에이전트가 작성한 최종안을 기존 감사기로 검증하고 정확한 렌더 입력을 준비한다.
5. 허가된 렌더를 실행하고 결과·오류·레저·리뷰를 같은 실행에 연결한다.
6. 재시도가 필요하면 실제 부모 원본에 결합한 허용 정보만 새 작성 단계에 전달한다.

성공 기준은 수작업 연결과 그에 따른 오류 감소다. 예술적 품질 향상, 픽셀 성공률 향상, 후보 데이터의 효과는 이 구현으로 증명하지 않는다. 기존 보고서의 세 조건 이미지 비교는 별도 범위다.

## 2. 현재 구현에서 확인한 출발점

| 현재 코드 근거 | 확인한 동작 | 계획에 미치는 영향 |
|---|---|---|
| SKILL의 Non-Negotiable Phase Boundary | 초기 core 동결 전에 assets·scripts·references·이전 pack 접근을 제한 | 새 초기 도구를 precore의 명시된 허용 경로로 추가해야 함 |
| prompt_generator.normalize_request_envelope | 원문 UTF-8 SHA와 문자열 구간을 검증. start/end는 Python 문자열 인덱스 | 바이트 위치와 문자 위치를 혼동하지 않고 계산을 자동화 |
| 같은 normalizer의 입출력 | 입력은 6개 필드, 출력에는 canonical_sha256과 envelope_id가 추가됨 | 정규화 출력 전체를 기존 입력 CLI에 다시 넣으면 안 됨 |
| generate_photo_prompt.main | core·controls·신체·camera 검토 이후 snapshot을 획득. pack과 receipt를 별도 저장 | 기존 생성기를 재사용하고 두 파일을 하나의 완료 단위로 관리 |
| 같은 CLI의 camera 플래그 | new-author-camera-evidence와 direction/height 조건부 검증 지원 | 새 작성 경로에서 누락되지 않도록 도구가 연결 |
| compose_pack_view | 알려진 선택 후보 목록만 미루고 나머지 필드는 그대로 노출 | post-core 읽기 도구로 재사용. 재시도 화이트리스트로 사용하지 않음 |
| photo_api_render / generate_images_via_api | 원본 4개 입력과 정확한 receipt, 두 감사, 실제 실행 문자열을 검증 | API 전송과 감사 로직을 새로 복제하지 않음 |
| normalize_request_lineage / composed 감사 | 부모 ID·SHA 형식과 내부 계약을 검증하지만 부모 원본을 인자로 받지 않음 | 새 추출기와 workflow 감사에서 실제 부모 산출물까지 대조 |
| photo-request-lineage/v2 | preserved_dimensions와 allowed_changes가 서로 겹치지 않아야 하고 둘 다 비어 있을 수 없음 | 모든 차원을 보존하는 국소 수리를 편의상 넓은 변경으로 바꾸면 안 됨 |
| compile_render_repair_contract | 물체 이름에 의존하지 않는 축·관계·gate와 추가 시도 상한을 생성 | 기존 generic 계약을 재사용하고 실패 gate에 맞게 범위를 좁힘 |
| audit_image_render_review | status는 기록 유효성, qualification_status는 기술 통과를 구분 | 기록이 유효한 실패 리뷰를 정상적인 수리 입력으로 받을 수 있음 |
| audit_moe_render_review | schema_failures, failed_hard_gates, user_judgment를 구분 | 실패 원인과 사용자 선호를 한 가지 성공/실패 값으로 합치지 않음 |
| record_image_run | timestamp·prompt ID·attempt로 run_id를 계산하고 NDJSON에 append | 실행 전 timestamp/identity를 보존하고 중복 append 방지 필요 |
| photo_runtime_sources | scripts/precore의 최상위 Python 및 precore JSON을 source에 결합 | 새 중립 파일도 새 generation과 호환 worker로 게시·검증 |

정확한 소스 바이트와 HEAD 일치는 [소스 기록](./P1_EXECUTION_RETRY_PLAN_SOURCE.json)에 남긴다. 읽은 25개 소스는 기준 커밋과 같다. 기존 미커밋 데이터와 다른 작업의 테스트는 변경 대상이 아니다.

## 3. 유지해야 할 작성·권한 경계

- 의미 해결, 원문 해석, 작품 방향, 장면의 인과관계, 후보 채택, 이미지 판독은 에이전트가 수행한다.
- 사용자 원문을 설정 설명, 부모 프롬프트, 에이전트의 요약으로 대체하지 않는다.
- 5~10개 중립 관찰 범주 선택과 기본안의 48~1,280단어 계약을 유지한다. 범주와 reason은 자동 선택하지 않는다.
- 설정은 현재 허용된 정의에서 한 번 해결하고 기본안부터 적용한다. 기존 authoring_brief를 손실 있게 다시 직렬화하지 않는다.
- scene·subject·pose·의미·supported 이유·literal evidence를 자동 작성하는 템플릿은 만들지 않는다.
- 초기 도구는 candidate-free여야 한다. 이름이 precore라고 해서 scripts를 가져와도 되는 것은 아니다.
- 과거 후보, 미채택 아이디어, 다른 실험 arm, 과거 범주 선택은 재시도 작성자에게 노출하지 않는다.
- 재시도에서도 필요한 기존 opt-in 의무는 보존한다. 선택된 의무를 편의상 선택 후보로 낮추지 않는다.
- 카메라 방향·높이와 촬영 주체는 에이전트가 구분한다. 도구가 장면 속 장치를 capture camera로 추정하지 않는다.
- 이미 주어진 사용자 권한을 다시 확인하는 승인 단계를 추가하지 않는다. 도구는 그 권한과 시도 범위를 기록하고 집행한다.
- prompt-only 실행은 렌더와 키 조회를 수행하지 않는다.
- 감사 통과, 파일 저장, 픽셀 판정, 사용자 수용을 별도 결과로 유지한다.

## 4. 도구 구조

### 4.1 초기 작성 도구

신설 경로는 precore/prepare_photo_run.py, precore/photo_authoring_wire.py, precore/photo_workflow_shapes.json으로 제안한다. 모두 skill의 precore 최상위에 둔다.

prepare_photo_run은 현재 요청, 지정 구간, 중립 설정 정의, 현재 에이전트가 작성한 산출물만 읽는다. assets·references·scripts, 이전 출력 디렉터리, runtime store에 접근하지 않는다. 초기 단계에서는 네트워크와 이미지 도구를 호출하지 않는다.

photo_authoring_wire에는 envelope/core/intent/assertion/lineage의 순수 구조 검증·공백·canonical hash 계산 중 필요한 부분을 추출한다. 현재 normalizer를 복제하여 두 구현이 드리프트하는 방식은 피한다. 기존 prompt_generator는 같은 중립 함수에 위임한다.

이 추출은 첫 구현 단위의 핵심 검토 대상이다. 의존성 그래프를 확인해 후보 데이터, 프로필 의미, 라우팅, 연구 예시가 들어오지 않는 부분만 옮긴다. 현재 구현과 정상/실패 결과, canonical payload, 해시를 동일하게 보존한다. 중립 분리가 성립하기 전에 초기 wrapper가 prompt_generator를 몰래 import하는 우회는 허용하지 않는다.

초기 shape는 필드 이름·타입·필수성만 제공한다. 실제 장면, 기본 범주, 포즈, 문구, 리뷰 상태는 채우지 않는다. 에이전트가 baseline을 한 번 작성하면 이후 baseline.txt 등은 읽기용 파생 파일로 만든다.

### 4.2 코어 이후 실행 도구

scripts/photo_workflow.py와 scripts/photo_workflow_state.py를 신설한다. 이 계층은 동결 증명서를 확인한 후 기존 생성기·뷰·감사기·P0 API adapter를 호출한다.

동결 전에도 status처럼 중립 메타데이터를 조회할 수 있도록 CLI의 단계별 import를 분리한다. status를 실행했는데 후보 모듈이 초기화되거나 pack을 읽는 일이 없어야 한다.

도구는 실행 폴더, 파일 역할, 해시, stage 상태, generation, receipt, operation ID를 연결한다. 재진입하면 임의로 마지막 단계를 추측하지 않고 검증된 산출물과 journal을 읽는다.

### 4.3 재시도 추출 도구

scripts/prepare_retry_context.py와 scripts/photo_retry_projection.py를 신설한다. 부모 pack 전체를 검사하는 coordinator 프로세스와, 추출 결과를 읽는 새 작성자의 지식 경계를 구분한다. 별도 LLM이나 하위 에이전트는 필요하지 않다.

SKILL에는 이 경로의 실행과 검증된 추출 결과 읽기만 재시도 예외로 명시한다. 새 작성자가 그 소스나 부모 pack 전체를 열어도 되는 일반 허용을 추가하지 않는다. stdout와 오류에는 허용된 projection 또는 오류 코드만 내보낸다. raw payload·stack·후보명을 포함할 수 있는 상세 진단은 coordinator 전용 파일에 보관한다.

## 5. 단계별 실행 인터페이스

아래 명령은 제안 CLI 이름이다. 구현 전에는 실행할 수 없다. 각 명령의 --run이 모든 현재 산출물의 위치를 연결하므로 긴 플래그를 다시 입력하지 않는다.

| 단계 | 제안 명령 | 자동 처리 | 에이전트 입력 |
|---|---|---|---|
| 준비 | prepare_photo_run init | 원문 보존, 지정 구간의 text/offset/SHA, 폴더, 중립 shape | 적용할 실제 메시지와 구간, 실행 목적 |
| 설정 | prepare_photo_run controls | 기존 resolver 호출, 현재 설정과 brief 저장 | 의미 해결 결과의 context와 선택한 override |
| 동결 | prepare_photo_run freeze | 중립 검증, 공백·해시·binding, catalog snapshot, freeze receipt | 기본안, 의미·속성·assertion, 5~10 범주와 이유, 신체 검토 |
| 조회 | photo_workflow retrieve | camera 플래그, generation, 한 pack와 receipt를 함께 저장 | 필요한 조건부 camera 축 선언, 선택한 조회 seed/policy |
| 후보 검토 | photo_workflow view | 현재 requirements/catalog 및 요청한 상세를 기존 뷰로 제공 | 검토할 후보와 채택 여부 |
| 구성 감사 | photo_workflow compose-audit | ID·source hash 연결, 기존 composed 감사, 경고 보존 | 최종 prompt, 채택 ID, 변경 이유, literal evidence, 새 신체 검토 |
| 실행 준비 | photo_workflow prepare-render | 정확한 runtime 문자열·참조·binding·runtime 감사 | 사용할 실행 도구와 파라미터, 참조 역할 |
| API 실행 | photo_workflow render-api | P0 adapter, operation journal, 결과 summary, 레저 연결 | 현재 사용자 권한 안의 실제 실행 |
| native 실행 | photo_workflow native-plan / native-result | 감사된 도구 payload와 완료 기록의 연결 | 실제 native 도구 호출과 관측된 결과 |
| 리뷰 | photo_workflow review-shape / review-audit | 실제 gate·scale·파일 SHA shape, 기존 review 감사 | 이미지 근거, pass/fail, 별도 예술적 관찰·사용자 판단 |
| 재시도 | photo_workflow retry-prepare | 부모 원본 검증과 허용 projection, child 참조 | 실제 실패 원인, 보존/수리 scope, 현재 요청 근거 |
| 상태·복구 | photo_workflow status / resume | 단계·바이트·operation 대조, 안전한 연결 작업 복구 | 필요한 새로운 작성 판단 또는 관측 결과 |

controls를 init과 함께 실행할 수는 있지만, context/override가 에이전트에게서 먼저 공급되어야 한다. compose-audit는 선택을 기다리며 누락된 chosen IDs를 자동으로 빈 선택으로 바꾸지 않는다. 기본안 유지 역시 에이전트의 명시적 결정이다.

### 5.1 원문과 구간

원문 파일은 read_bytes 후 UTF-8로 읽어 CRLF와 공백을 보존한다. request SHA는 같은 원문 UTF-8 바이트로 계산한다. envelope의 start/end는 문자열 위치이며 바이트 위치가 아니다. 한국어·일본어·emoji와 반복 구간을 테스트한다.

도구는 에이전트가 준 start/end에서 text를 추출한다. 여러 arm의 의미적 구분이나 적용할 구간을 자동 결정하지 않는다. 단일 전체 요청을 쓰는 명시적 모드만 전체 구간을 선택할 수 있다. 반복된 substring은 일치하는 한 구간을 임의 선택하지 않는다.

부모 source_text/span_id를 child 요청에 복사하지 않는다. child의 현재 실제 사용자 구간에 의미 보존과 수정의 근거를 다시 연결한다. 이전 요청이 현재 대화의 유효한 근거라면 그 실제 사용자 원문을 사용하고, 부모 baseline을 사용자 메시지로 둔갑시키지 않는다. 현재 envelope에서 근거를 표현할 수 없으면 needs_author_input을 반환한다.

### 5.2 동결 산출물

기존 CLI가 받는 raw wire 입력과 검증된 normalized 기록을 나눠 저장한다. envelope의 파생 ID를 입력에 억지로 추가하지 않는다. 기존 CLI에는 정확히 허용된 입력 shape를 넘긴다.

freeze_receipt에는 원문, envelope 입력 바이트, normalized envelope digest, core 입력 바이트, normalized core digest, intent lock, controls, catalog, selection, 신체 검토의 각각 다른 해시를 기록한다. 파일 SHA와 canonical contract SHA를 같은 값으로 취급하지 않는다.

baseline의 공백 정리는 literal evidence와 신체 검토를 확정하기 전에 한다. 공백 정리 뒤 phrase가 사라지면 evidence를 자동 치환하거나 supported 이유를 유지한 채 hash만 바꾸지 않는다. 에이전트가 현재 baseline에서 근거를 다시 지정하고 검토한다.

### 5.3 조회와 감사

retrieve는 freeze receipt와 현재 파일을 먼저 대조한다. 유효한 신체·feature·camera 검토 전에 후보 자산을 읽지 않는다. 새 작성에는 new-author-camera-evidence를 연결하고, 에이전트가 requested로 선언한 direction/height만 require-camera-evidence로 전달한다.

pack과 private receipt를 staging 폴더에 저장하고 둘의 binding 검증이 끝난 뒤 stage 완료를 기록한다. receipt 없이 pack만 존재하는 상태를 성공으로 간주하지 않는다. source가 pending/invalid면 이전 세대로 자동 fallback하지 않는다.

완료된 retrieve의 재진입은 같은 pack/receipt를 검증해 재사용한다. 초기 seed를 한 번 저장하고, 중단 때문에 새 seed로 다른 pack을 공개하지 않는다. 저장 직전 중단된 staging pair도 검증 가능한 경우에만 복구한다. source 관측 시각 등을 재생성해 항상 같은 바이트가 나온다고 가정하지 않는다.

compose-audit와 prepare-render는 정확한 receipt에 고정된 source로 실제 감사기를 호출한다. 기록된 PASS를 그대로 믿거나 최신 데이터로 오래된 pack을 재해석하지 않는다. source/worker가 다르면 호환 generation의 worker로 실행하거나 명확한 호환 오류로 중단한다.

## 6. 실행 상태와 중단 복구

새 스키마 이름은 photo-workflow-run/v1로 제안한다. 상태 파일은 현재 자료의 의미를 대신하는 데이터베이스가 아니라 파일 역할·바이트·단계·실행 이력을 가리킨다.

~~~json
{
  "schema_version": "photo-workflow-run/v1",
  "run_id": "opaque-run-id",
  "mode": "prompt_only",
  "phase": "core_frozen",
  "artifacts": {
    "request_envelope_input": {"path": "...", "sha256": "..."},
    "authorial_core_input": {"path": "...", "sha256": "..."},
    "freeze_receipt": {"path": "...", "sha256": "..."}
  },
  "source_binding": null,
  "render_scope": null,
  "operations": []
}
~~~

예시는 shape만 나타낸다. 실제 image 모드는 이미 주어진 authorization의 근거, 허용 lane, 실제 호출 상한을 별도로 기록한다. JSON의 true 하나가 사용자 권한을 만들어 주는 것은 아니다.

호출 권한이 아직 없는 lane이라도 정확한 입력 준비·감사·dry-run은 먼저 할 수 있다. 실제 호출 경계에서만 현재 권한을 확인한다. 이미 허가된 범위에는 다시 확인을 요구하지 않고, 새 유료 호출이 필요한 경우에는 준비된 구체적 실행을 대상으로 한 번만 요청한다.

정상 단계는 request_prepared → controls_bound → core_frozen → pack_bound → composition_audited → runtime_audited다. prompt-only는 여기에서 prompt_delivered로 끝날 수 있다. 이미지 요청은 invocation_reserved → invocation_started → result_received → result_saved → attempt_recorded → review_record_validated로 이어진다.

기술 판정과 사용자 판단은 phase 하나에 섞지 않는다. technical_qualification과 user_judgment를 별도로 보관한다. preview_only, provider_blocked, execution_unknown, persistence_failed, recorder_failed도 구분한다.

- 각 stage는 파일을 모두 준비한 뒤 atomic manifest 교체로 완료한다. 미완성 staging은 독립적으로 남긴다.
- source/정책/입력/결과 해시와 역할을 stage key에 결합한다. 파일 경로가 같다는 이유만으로 재사용하지 않는다.
- mutable 작성 파일이 바뀌면 파생 단계를 stale로 표시한다. 기존 frozen 파일과 과거 결과는 덮어쓰지 않고 새 revision을 만든다.
- local 연결·감사는 같은 바이트로 재진입할 수 있다. 이미지 생성은 이 규칙으로 재호출하지 않는다.
- 호출 직전에 durable operation과 timestamp를 보존한다. 완료 증거가 없으면 execution_unknown으로 둔다.
- 외부 제공자에 대해 exactly-once 호출을 보장한다고 주장하지 않는다. 중단된 실제 호출의 중복 실행을 막고, 불확실할 때 자동 실행을 멈춘다.
- lease나 PID가 사라졌다는 이유만으로 호출하지 않았다고 판단하지 않는다.
- 실행 lock은 state 갱신을 보호한다. 긴 native 호출 전체 동안 다른 status 조회를 막는 구조는 피한다.

## 7. 렌더·저장·레저 연결

### 7.1 API

현재 P0 adapter를 실제 전송 진입점으로 유지한다. workflow가 call_api를 직접 호출하거나 별도 약한 감사를 구현하지 않는다. 4개 원본 파일, receipt, preflight, runtime 원문, 모델·크기, 현재 시도 정책을 그대로 연결한다.

추가로 structured execution summary와 호출 시작/완료 hook 또는 동등한 journal 연결을 제공한다. 로그의 문자열을 파싱해 run_id나 저장 성공을 추정하지 않는다. dry-run은 키·이미지 호출·attempt row를 만들지 않는다.

### 7.2 native

Python CLI가 Codex native 도구를 직접 호출할 수 있다고 가정하지 않는다. native-plan은 감사된 payload, reference role/hash, operation ID, 허용 횟수, 실제 공유 오류 캡처 helper 연결을 제공한다. 실제 호출은 Codex 도구 실행 환경의 얇은 bridge가 수행한다.

bridge는 사전 준비한 정확한 입력을 읽고 한 operation으로 호출한다. native-result는 실제 관측 결과만 받는다. 도구가 반환한 concrete local file이 없으면 preview_only로 기록하고, 이를 이유로 추가 API 호출을 시작하지 않는다. UI blob·cache·추정 파일명에서 결과를 복원하는 기능은 추가하지 않는다.

참조가 필요한 입력을 API text-only lane에 맞춰 자동 삭제하지 않는다. 기존 runtime/reference audit와 정확한 첨부를 유지한다. 단순 경로 문자열을 프롬프트에 붙이는 방식은 첨부가 아니다.

### 7.3 중복 기록과 호출 예산

operation ID와 실제 attempt의 identity/timestamp를 호출 전에 고정한다. recorder에는 optional workflow_operation_id와 idempotent append 검증을 추가하는 방안을 사용한다. 스키마와 API/native 연결도 함께 갱신하고 역사 row는 그대로 유지한다.

같은 operation의 같은 row 재기록은 기존 row를 확인해 종료한다. 같은 identity에 다른 내용이 오면 충돌로 중단한다. 레저 기록 뒤 state 저장이 실패하면 기존 row를 연결해 복구하며 이미지를 다시 생성하지 않는다.

새 구성의 첫 실제 attempt도 부모 run_id를 retry_of로 연결할 수 있도록 API helper의 초기 retry 참조를 확장한다. helper 내부 transient retry는 바로 전 attempt를 계속 잇는다. core/request lineage와 실제 호출 retry_of는 서로 다른 연결이다.

호출 예산은 유일한 실제 invocation을 센다. 누적 image_call_count 행을 모두 합산하지 않는다. P0의 transient retry도 예산을 소비한다. 현재 generic repair 계약의 maximum_additional_attempts=1이 적용되면 API 기본 attempts=2를 그대로 실행해서 상한을 넘기지 않는다.

명시적 policy block, 결과 미관측, 저장 실패, recorder 실패는 자동 재호출하지 않는다. 바이트와 실패 원인을 보존한 뒤 현재 허용된 회복 작업만 수행한다.

## 8. 재시도 허용 정보 추출

### 8.1 입력과 산출물

입력은 부모 run의 정확한 envelope/core/controls, pack, private receipt, composed, runtime request, 실제 attempt 기록, 이미지/오류 evidence, 리뷰와 그 감사, 현재 retry 요청, 에이전트의 repair_decision이다. 각 파일의 역할과 SHA를 먼저 고정한다. 여러 객체 중 첫 번째를 임의 선택하지 않는다.

repair_decision은 실제 현재 요청의 span, 보존할 차원·속성, 실패 gate 또는 별도 관찰, 실패 원인, 수정하려는 local axes, 의미 수정 여부를 지정한다. 에이전트가 판단하는 값이며 도구가 이미지나 문장의 키워드로 생성하지 않는다.

산출물은 다음 셋으로 나눈다.

- retry_context.json: 새 작성자에게 전달하는 닫힌 허용 projection.
- retry_projection_audit.json: 부모 바이트·계약·scope·projection 일치 검증 결과.
- retry_coordinator_diagnostics.json: 원본 접근과 상세 오류의 coordinator 전용 기록. 작성자에게 자동 표시하지 않음.

제안 스키마는 photo-retry-context/v1이다. 새 context가 기존 core의 허용 필드인 것은 아니다. request_lineage/v2의 정확한 필드만 core에 넣고, projection 증명은 workflow 산출물로 연결한다.

### 8.2 추출 절차

1. 부모 파일 SHA와 ledger run_id, pack ID, core/intent/receipt/generation의 서로 다른 binding을 실제 원본과 대조한다.
2. 부모의 composed/runtime 감사를 그 generation과 호환되는 구현으로 확인한다. mutable 최신 DATA로 부모 의무를 다시 만들지 않는다.
3. 실제 chosen_visual_concept_ids로 effective visual contract를 도출한다. 선택되지 않은 opt-in gate를 섞지 않는다.
4. generic repair, character response, unconditional visual 의무 등 실제 적용되는 hard 계약을 모은다. 기존 도움 함수가 있는 부분은 재사용한다.
5. 리뷰 기록의 schema·이미지 SHA·gate set·scale을 검증한다. 기록 유효성과 gate 실패를 분리한다.
6. 현재 에이전트의 보존·수정 판단이 요청에 근거하는지 구조적으로 검증하고, 기존 잠금 및 실제 의무와 대조한다.
7. 필요한 owner → property → relation 연결을 유지하는 최소 허용 필드 집합을 만든다. 의무의 구성요소를 잃는 단순 JSON 잘라내기는 사용하지 않는다.
8. 경로별 allowlist로 값을 복사하고 각 값의 원본 역할·JSON pointer·해시를 붙인다. 알려지지 않은 필드는 자동 허용하지 않는다.
9. 출력 바이트와 canonical projection 해시를 저장하고, 실제 부모를 다시 기준으로 projection을 재계산해 대조한다.
10. child freeze와 렌더 전에도 같은 부모·decision·context binding을 검증한다. 해시가 있는 파일이라는 이유만으로 권한을 인정하지 않는다.

새 추출기를 과거 generation에 복사해 그 generation의 code hash를 바꾸지 않는다. 필요한 경우 immutable generation 안의 기존 감사 함수를 호환 Python worker에서 호출하는 제한된 bridge를 둔다. 현재 projection 코드는 그 worker가 검증한 계약의 알려진 구조를 읽는다. 지원하지 않는 과거 버전·환경·누락된 snapshot은 명확한 오류로 중단하고 historical audit 경로를 안내한다. importlib.reload나 버전 검증 생략은 하지 않는다.

### 8.3 출력 허용 정보

| 정보 묶음 | 출력할 내용 | 한계 |
|---|---|---|
| 부모 식별 | request/core/intent/pack/receipt/generation/run의 ID·SHA, 이미지 SHA | 전체 부모 텍스트를 담지 않음 |
| 보존 의미 | 현재 보존 scope에 해당하는 frozen 값, 필요한 required assertion과 literal evidence | 열린 과거 연출이나 advisory 제안 제외 |
| 속성 잠금 | dimension/target/property와 실제 증거 | 상위 property의 하위 속성까지 보호 |
| 관계 | 보존할 주체·대상·행동·같은 대상·접촉·결과의 필요한 연결 | 한 endpoint만 내보내 의미가 바뀌지 않게 함 |
| 유효 의무 | 보존 scope에 영향을 주는 hard 계약, gate ID·정의·scale·필수 증거 | 실제로 선택된 opt-in 포함 |
| 실패 | 유효한 리뷰의 관련 failed gate·scale·증거, 관측된 오류 코드·stage | raw HTTP body·stack·전체 리뷰 prose 제외 |
| 수정 범위 | 허용 dimensions/properties/local axes와 source 근거 | 실패했다는 사실이 새 변경 권한이 되지 않음 |
| 실행 조건 | 기존 참조 역할·SHA, 필요한 보존 control 값, 남은 시도 범위 | 과거 creative brief·후보 예시를 새 영감으로 전달하지 않음 |

선택된 opt-in은 effective hard contract의 내용만 전달한다. 후보 목록, 선택 이유, 조회 score, 미채택 ID 목록은 전달하지 않는다. context에 완전한 pack이나 parent_baseline_prompt_en 필드를 두지 않는다.

참조의 경로·SHA만으로 새 작성자가 실제 이미지의 속성을 판정했다고 기록하지 않는다. 현재 허용된 reference scope와 실제 관찰은 기존 규칙을 따른다. 예술적 평가와 사용자 비교 판단은 필요한 현재 결정에 관련된 관찰만 별도로 인용하며, hard gate로 승격하지 않는다.

### 8.4 수정 범위의 상한

허용 범위는 현재 요청/세션 권한, 부모의 동결 잠금, 실제 유효 의무, 에이전트가 지정한 실패·수리 scope의 교집합으로 계산한다. 같은 뜻을 다시 그린다는 이유로 부모의 모든 open_dimensions를 기본 수정 목록으로 내보내지 않는다.

generic local axes는 현재 계약의 object_geometry, contact_geometry, local_pose, camera, framing, lighting, material, occlusion을 재사용한다. 물체·장르·키워드별 분기를 만들지 않는다. camera/framing/lighting/material에는 현재 차원 매핑과 허용 조건을 적용하고, 나머지 축도 관계와 속성 잠금을 우회하지 못하도록 검사한다.

복합 assertion이나 evidence가 허용 scope와 금지된 과거 연출을 함께 포함하면 자동 요약·부분 문자열 추측으로 의미를 바꾸지 않는다. closure가 요청이 보존한 범위 안에 들어오면 필요한 원문을 그대로 유지한다. 그렇지 않으면 projection_scope_unresolved로 남기고 좁은 필드 선택이나 새 현재 요청 근거를 요구한다. 이는 새로운 사용자 승인 절차가 아니라 아직 해결되지 않은 작성 입력이다.

현재 request-lineage/v2는 preserved_dimensions와 allowed_changes 양쪽이 비어 있지 않아야 한다. 모든 차원을 보존하면서 접촉 형상만 국소 수정하는 scope 등 표현할 수 없는 경우는 scope_not_representable_in_lineage_v2로 표시한다. 도구가 composition을 임의로 열어 검증을 통과시키지 않는다.

이 P1의 필수 범위는 추출·검증과 기존 계약으로 표현 가능한 실행 연결이다. lineage의 더 정밀한 새 버전은 필요한 실제 사례를 모아 별도 계약 변경으로 설계한다. 제안 context의 leaf-level 허용 정보를 기존 v2 안에 미지원 필드로 밀어 넣지 않는다.

### 8.5 child 작성에 전달하는 shape

~~~json
{
  "schema_version": "photo-retry-context/v1",
  "parent_binding": {"request_id": "...", "core_sha256": "...", "ledger_run_id": "...", "generation_id": "..."},
  "source_artifacts": [{"role": "parent_core", "sha256": "..."}],
  "preserved_fields": [{"scope": {"dimension": "...", "target": "...", "property": "..."}, "value": "...", "source_pointer": "..."}],
  "required_relations": [],
  "effective_obligations": [],
  "reported_defects": [],
  "allowed_scope": {"dimensions": [], "properties": [], "local_axes": []},
  "repair_route": "local_realization_repair",
  "decision_binding": {"sha256": "...", "current_source_span_ids": []},
  "execution_scope": {"additional_invocation_limit": 1},
  "projection_sha256": "..."
}
~~~

예시의 빈 배열과 상한은 기본 적용값이 아니다. 실제 값은 검증된 부모와 현재 결정에서만 나온다. 필드마다 provenance를 완전하게 구현하고, 자료형·길이·unknown field 검증을 닫힌 스키마로 수행한다.

출력에 있는 부모 source_span_ids를 child로 상속하지 않는다. child의 repair_targets.source_span_ids, interaction_phrase, recognition_phrase와 required action assertion은 실제 child envelope와 새 baseline에서 에이전트가 작성·결합한다. 해시와 ID 연결만 자동 채운다.

선택 범주는 현재 중립 catalog에서 새로 선택한다. 부모 feature-selection record는 hash 확인에 필요한 opaque 참조를 제외하고 작성자에게 제공하지 않는다. 옛 agent 선택을 requester lock으로 승격하지 않는다.

## 9. 실패 원인과 실행 경로

| 원인/상태 | 누가 판정하는가 | 허용된 다음 작업 |
|---|---|---|
| 의미를 기본안이 잘못 해석 | 에이전트, 현재 사용자 근거 | meaning_rebuild: envelope/core를 새로 작성하고 다시 동결 |
| 에이전트 연출의 물리적 모순 | 에이전트의 전체 공간 검토 | 허용된 국소 연출 수정, 신체 검토와 감사 재실행 |
| 일관된 prompt와 실제 이미지의 차이 | 에이전트의 pixel review | failed gate 중심 local_realization_repair 또는 이미 허가된 동일 입력 시도 |
| 요구 scale에서 관측 불가 | 에이전트, 실제 scale·가림 근거 | 불통과를 유지. 허용 scope의 관측 방법/가림 수정만 검토 |
| 관측된 transient HTTP 오류 | 명시적인 코드 기반 도구 판정 | 같은 prepared input과 남은 budget 안에서 P0 retry |
| 명시적 policy block | 제공자의 관측된 코드·stage | 차단 기록·중단. 현재 원문이나 참조를 자동 완화하지 않음 |
| 파일 저장 실패 | 저장 처리의 관측된 결과 | 반환 bytes 복구·기록 수리. 새로운 이미지 호출 아님 |
| 레저/state 저장 실패 | 저장 처리의 관측된 결과 | 기존 증거로 idempotent 기록 복구 |
| 제공자 결과 미관측 | 관측 사실만 도구가 기록 | execution_unknown. 자동 호출 없이 실제 결과 reconciliation |
| 리뷰 schema·이미지 hash 실패 | 기존 감사기 | 기록 무결성 수정. 픽셀 실패나 창작 수리로 분류하지 않음 |
| 기술 통과지만 사용자/예술적 불만족 | 실제 사용자 판단 또는 에이전트 관찰 | 현재 승인 scope 안의 artistic revision. 가짜 failed gate 생성 금지 |

hard gate가 fail이라는 이유만으로 authored prompt가 틀렸는지, 모델이 다르게 그렸는지 자동 확정하지 않는다. 이미지 review는 에이전트의 관찰이며 도구 감사는 그 기록과 binding을 검사한다.

meaning_rebuild는 기존 동결 의미를 몰래 수정하는 retry로 처리하지 않는다. 사용자 명시 교정이 부모 관계를 바꾸는 경우 현재 requester_corrected 규칙을 적용하고, 기존 실패 기록을 사후 PASS로 다시 쓰지 않는다.

## 10. 파일 변경과 기존 구현 재사용

| 구현 영역 | 제안 파일 | 기존 연결 |
|---|---|---|
| 중립 입력·검증 | precore/prepare_photo_run.py, photo_authoring_wire.py, photo_workflow_shapes.json | 기존 creative_controls, core/envelope normalizer, neutral catalog |
| 단계 관리 | scripts/photo_workflow.py, photo_workflow_state.py | generate_photo_prompt, compose_pack_view, 세 종류 감사 |
| 재시도 추출 | scripts/prepare_retry_context.py, photo_retry_projection.py | 부모 generation, 실제 선택의 effective contract, 두 리뷰 감사 |
| 실제 실행 | scripts/generate_images_via_api.py, photo_api_render.py, 얇은 native bridge | P0 preflight·오류 bytes·기록 보존 |
| 중복 기록 | scripts/record_image_run.py, assets/run_ledger.schema.json | 기존 run_id/retry_of, optional operation ID와 append 검증 |
| 사용 문서 | SKILL.md, references/image-runtime.md, 새 post-core workflow 안내 | 초기 허용 경로, 새 작성 camera 옵션, 단계 실행과 retry exception |

새 역할 파일들은 계획상의 경로다. 기존 데이터 manifest에 workflow schema를 candidate extension으로 등록하지 않는다. 전술한 예시는 maintenance 문서이며 live 초기 작성 자료가 아니다.

중립 Python/JSON 파일은 현재 SourceInventory가 해시에 포함하는 최상위 경로에 둔다. 코드 변경 이후 matching worker와 새 runtime publication을 검증한다. 작성 DATA/semantic text가 바뀌지 않았다면 이 작업 때문에 embedding을 재생성하지 않는다. 기존 generation·shard·pack·ledger를 삭제하거나 다시 쓰지 않는다.

## 11. 검증 계획

아래 검증은 구현 시 수행할 기준이다. 계획 작성 턴에서 새 기능이나 새 테스트가 이미 통과했다고 주장하지 않는다.

| 테스트 묶음 | 중요한 사례 | 완료 기준 |
|---|---|---|
| precore 격리 | 금지 경로 read/import/network을 막은 프로세스에서 init/controls/freeze | 허용 입력만으로 동작, 후보 접근 0회 |
| normalizer 분리 | 다국어 구간, control span, property lock, typed assertion, invalid shape, 기존 holdout | 기존 canonical 결과·해시·reject 보존 |
| 입력 연결 | CRLF, emoji, 반복 substring, normalized 출력의 추가 필드, brief key order | 원문 보존, offset 정확, 잘못된 shape 재입력 거부 |
| 작성 판단 보존 | 미작성 reason·supported 검토·selection, missing chosen IDs | 도구가 의미/선택/통과 판단을 대신 채우지 않음 |
| 조회 원자성 | pack만 존재, receipt 불일치, seed 미저장, source pending, stale code | 한 쌍만 완료, 잘못된 generation 재사용 0회 |
| 실제 감사 | pack/composed/runtime 변조, extra prose, reference 불일치 | 실제 감사기로 호출 전 거부, 호출 수 0 |
| 재진입·중단 | 호출 전후 종료, bytes 저장 뒤 종료, ledger append 뒤 state 실패 | 중복 이미지 호출·중복 row 없음, unknown 보존 |
| budget | API transient, child repair, 동시 render, policy block, unknown | 유일 invocation을 세고 허가/계약 상한 유지 |
| retry 누출 | 금지 필드에만 sentinel 삽입, unselected opt-in, 이전 category, parent 전체 prompt | projection/stdout/error에 sentinel 노출 0 |
| 부모 대조 | 실제 부모 hash, selected effective gate, 이미지·review·receipt·worker 교체 | stale/다른 부모/가짜 PASS/변조 capsule 거부 |
| 리뷰 구분 | 유효한 fail gate, malformed record, unobservable, pending user | 기록·기술·관측·선호 상태를 정확히 유지 |
| scope | 부분 속성/상위 속성, 관계 endpoint, closure, requester correction, v2 표현 불가 | 권한 확대·의미 누락·가짜 span 생성 0 |
| 적용성 | 인물/비인물, 0개 채택, 정적 요청, reference native, prompt-only | 불필요한 gate나 live API 요구 없음 |

신규 테스트는 test_photo_workflow_precore, test_photo_workflow_state, test_photo_retry_context, test_photo_workflow_runtime_bridge로 제안한다. 구현을 그대로 따라 쓰는 tests보다 stage boundary·잘못된 부모·부정합·중단·누출을 검증한다.

관련 기존 suites는 authorial_core_v6, precore_feature_selection, initial_creative_controls, control_span_ownership, camera_evidence_structure, camera_clause_polarity, camera_owned_clauses, prepack_isolation, composer_view, api_render_preflight, image_attempt_evidence, run_manifest, runtime_freshness, render_repair를 사용한다.

실제 composed/runtime 감사와 file/process 경계의 freshness 검증을 유지한다. 모든 감사 결과를 mocked PASS로 바꾸지 않는다. 네트워크·이미지·embedding 호출은 offline 테스트에서 금지한다. 중립 core normalizer를 이동하는 변경은 여러 기존 경로에 영향을 주므로 최종 통합에서 전체 unittest discovery를 한 번 수행한다. 실패나 source 변경이 없으면 이미 통과한 검증을 반복하지 않는다.

## 12. 구현 순서와 검토 단위

| 단위 | 구현할 내용 | 끝나는 조건 |
|---|---|---|
| A. 중립 초기 도구 | 의존성 분리, raw/normalized 구분, init/controls/freeze, shape와 freeze receipt | 후보 접근 없이 현재 core 계약과 해시를 동일하게 재현 |
| B. 단계 실행과 감사 | run state, transactional pack/receipt, camera 옵션, view·compose-audit·prepare-render | 같은 바이트의 재진입, stale 차단, 기존 감사 통과 |
| C. 호출·기록·복구 | P0 adapter summary/hook, native plan/bridge, operation, budget, idempotent ledger | 중단/unknown/저장 실패에서 중복 호출 없이 복구 |
| D. 부모 projection | 실제 부모 검증, compatible worker, closed whitelist, source pointers, scope와 failure route | 누출·권한 확대 0, child에서 부모 proof 재검증 |
| E. 문서와 통합 | SKILL 허용 경로·짧은 명령, post-core 상세 안내, 기존/신규 tests, 입력 편의 계측 | 핵심 작성 규칙 유지, offline 통합 검증·원본 보존 확인 |

A는 가장 먼저 구조 검토한다. B 이후 prompt-only 실행만으로 수작업 감소를 확인할 수 있다. C는 실제 API 없이 provider fixture와 native contract fixture로 검증한다. D는 A/B/C의 파일 역할·해시·실행 결과가 안정된 뒤 연결한다. 각 단위는 source/test/문서를 함께 검토 가능한 변경으로 나눈다.

모든 구현은 기존 dirty work와 분리한 worktree에서 수행한다. 같은 scope의 파일을 선택적으로 stage하고, 부모·역사 holdout·기존 ledger의 해시 보존을 확인한다. 이 계획 자체는 코드 변경·commit·push·이미지 생성을 수행하지 않는다.

## 13. 수작업 감소를 측정하는 방법

동일한 작성 입력으로 기존 CLI와 새 실행 도구를 offline 비교한다. 입력은 maintenance fixture이며 live 초기 영감으로 사용하지 않는다. 의미와 baseline을 고정해 도구 편의의 효과를 측정한다.

| 지표 | 구현 목표 | 해석 |
|---|---|---|
| 사람이 계산·복사하는 SHA/derived ID | 0개 | 원문 의미나 evidence 작성은 포함하지 않음 |
| pack/receipt/감사/레저 간 수작업 플래그 전달 | --run과 단계별 현재 작성 입력으로 축소 | 내부 산출물 수가 줄었다는 뜻은 아님 |
| 기본안·최종안의 독립 입력 중복 | 각 문장 원본을 한 곳에 작성 | 읽기용 파생 파일은 도구가 생성 |
| 일부 파일만 수정했을 때 stale 발견 | 다음 관련 stage에서 반드시 검출 | silent repair 금지 |
| 재시도 작성자가 열어야 하는 부모 전체 파일 | 0개 | coordinator는 원본 검증을 위해 읽음 |
| 후보/미채택 prose/과거 category 노출 | 0건 | 허용된 기존 hard 의무의 유지와 구분 |
| crash 후 자동으로 반복된 이미지 호출 | 0건 | unknown은 실제 관측이 생기기 전까지 유지 |
| 창작·신체·pixel·사용자 판단의 자동 작성 | 0건 | 도구 편의를 위해 판단 책임을 지우지 않음 |

시간 감소율이나 품질 향상 수치는 구현 전에 제시하지 않는다. 정상 실행과 누락·변조·중단 사례 각각에서 입력 횟수, 수정 왕복, 재연결 오류, wall time을 측정해 결과를 보고한다. 실제 이미지 비교가 필요한 경우에는 별도 승인된 범위로 수행한다.

## 14. 주요 검토 결정

- 추천 구조는 candidate-free precore 도구와 post-core 상태 관리 CLI를 분리하는 방식이다.
- API 전송은 P0 구현을 재사용하고 native는 도구 환경의 bridge로 연결한다.
- parent whitelist는 일반 composition view와 별도로 닫힌 필드 정책을 갖는다.
- 현재 v2로 표현할 수 있는 retry부터 자동 연결한다. 표현 불가능한 국소 권한은 좁은 추출로 보존하고 지원 한계를 명시한다.
- 기록 무결성·실행 상태는 자동화하되 의미 해석·수리 원인·pixel 판독·사용자 선호는 에이전트와 실제 요청자에게 남긴다.

다음 실행 작업의 첫 검토 대상은 A의 중립 normalizer 의존성 분리다. 이 단계가 통과하면 B/C/D를 순서대로 연결하는 것이 가장 작은 검토 단위로 목표를 달성하는 방법이다.

# 불 관련 데이터 반영 계획

기준일: 2026-10-08. 이번 단계는 리서치와 구현 계획이다. 아래 경로의 신규 fire 파일은 아직 활성 source가 아닌 제안이다.

## 1. 목표와 완료 기준

검색된 “불” 주변 단어가 장면에 한꺼번에 들어오는 대신, **요청에 맞는 의미·소유자·관계가 정확히 노출되고 선택된 후보만 프롬프트를 보강**하도록 한다.

완료는 네 단계로 기록한다.

|단계|완료 증거|
|---|---|
|원본 데이터 반영|검토된 의미 카드·후보·프로필, provenance ledger, 기존 source 보존|
|검색과 후보팩 반영|fresh source/index/runtime generation, exact·paraphrase·hard-negative, pack exposure와 선택 receipt|
|프롬프트 반영|같은 owner에 대한 literal evidence, property lock 보존, 조합·runtime audit|
|이미지 기여 확인|원본 픽셀의 전체 gate, 통제 비교, 작성자 선호와 별도 사용자 판단|

리서치 카드 수·index build PASS·후보 노출·prompt audit·픽셀 PASS를 서로 대체하지 않는다. zero adoption도 유효한 결과다.

## 2. 우선순위

|우선순위|대상|먼저 하는 이유|
|---|---|---|
|P0|F001–F008의 연소 형태, F014 제트, F031–F043의 발광·불빛·열 경계, F045–F065의 연기·잔류물·열손상|기본 불 의미에서 잘못된 물질·소유를 만드는 오류를 줄임|
|P1|F070 배터리 플룸, F074–F099의 소방·산불·생활, F100–F117의 검토된 도구–재료·음식 관계|행위와 장소를 연결하는 실용 범위를 넓힘|
|P2|F118–F139의 태양·카메라·비연소|기존 space/editing source를 재사용하면서 혼동 경계를 보강|
|P3|F140–F155의 문화·판타지·신체·폭력·비유|명시된 맥락·동일 대상·tone·age·접촉 잠금이 필요|

우선순위 범위에 context 카드가 섞여 있어도 그것을 후보로 변환하지 않는다. 카드의 `renderable`, `meaning_basis`, 추가 출처 검토 여부가 우선이다. 금속 열처리·소결·유리화·낙화·화염 연마·웍헤이·일부 의례 판본 등은 추가 전문 근거를 확인한 뒤 승격한다. literal cold flame, 단일 화재 사진으로 판정하는 backdraft/detonation, 미세 입경·임상 진단·동기는 초기 active profile 범위에 넣지 않는다.

## 3. 실제 파일에 반영할 위치

|표면|현행 또는 제안 경로|반영 내용|
|---|---|---|
|기본 불 후보|제안: `skills/photo-prompt-image-generator/assets/photo_prompt_fire_relations_extension.json`|검토된 원자 후보·concept units·같은 대상의 relations·explicit effects|
|기본 불 시각 프로필|제안: `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_fire_relations.json`|선택된 실현의 `authored_components/v1` 또는 collective `v2`|
|기존 광학 후보|`assets/photo_prompt_editing_effects_extension.json`|F131–F133은 기존 ID 동치 검토 후 context/paraphrase 또는 경계 보강|
|기존 광학 프로필|`assets/photo_prompt_visual_obligations_editing_effects.json`|기존 bloom·film/image-plane 의미와 lens 의미 충돌 검토; 신규 gate 필요 여부 판단|
|기존 태양 후보|`assets/photo_prompt_space_extension.json`|F127 기존 coronagraph ID 재사용, 다른 관측 모드는 별도 sibling 검토|
|기존 조명·물 관계|`assets/photo_prompt_lighting_extension.json`, `assets/photo_prompt_water_relations_extension.json`|수광면·수면 반사 구조가 이미 같은 의미를 소유하면 그 정의 재사용|
|문화 도상|`assets/photo_prompt_religion_iconography_extension.json`, 대응 visual source|특정 판본의 provenance·도상 소유 검토 후 부분 확장|
|등록|`assets/photo_prompt_source_manifest.json`|승인된 candidate/profile basename·kind·required·unique load_order만 중앙 등록|
|연구 근거|이 폴더의 JSON/Markdown|출처 URL·title·연구 한계·seed accounting·adoption ledger 보존|
|파생 데이터|semantic/profile index manifests와 referenced shards|원본 반영 후 canonical builder로 재생성|

source 파일은 identity 기준으로 수정한다. 의미·carrier·소유·관측 방식이 다른 항목을 alias로 합치지 않는다. 같은 의미의 paraphrase/context 추가는 `existing_slot_context_extensions` 사용 가능성을 검토한다. 효과가 넓어지면 동일 ID의 사소한 문구 수정으로 숨기지 않고 새 원자 항목을 만든다.

후보와 의미 프로필은 별도의 역할을 유지한다. 별도 glossary loader·keyword conditionals·새 pack version·사전 scene recipe는 이번 데이터 반영에 필요하지 않다. 기존 consumer가 표현하지 못하는 의미가 발견되면 해당 항목을 보류하고 구체적 계약 결함으로 기록한다.

## 4. 먼저 확정할 source-to-runtime ledger

[RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)의 각 행을 실제 채택 판정으로 완성한다.

각 행에 stable unit ID, source file, entry/profile ID, source access level, 의미 동치, carrier와 owner role, slot, target/property, 영향을 받는 dimension, 맥락 prerequisites, exact/advisory 정책, 필요한 literal evidence, 반례, 검증 결과를 기록한다.

현재 후보 131개에는 proposed effects가 있으나 실제 consumer 연결은 pending이다. 문법이 통과했다는 이유로 owner가 실제 인물·사물에 결합했다고 승인하지 않는다. 특히 아래 항목을 먼저 확인한다.

|관계|보존할 소유·변경 범위|반드시 실패해야 할 변이|
|---|---|---|
|불빛|광원과 같은 receiver의 lighting, surface material과 구별|주황 피부색·다른 광원·전역 grade로 대체|
|연기·검댕|air medium의 입자와 selected surface의 deposit|공중 연기를 벽 texture로 이동|
|열 아지랑이|heated air path의 굴절 구조와 camera에 보이는 변위|camera blur slot으로만 처리해 atmosphere lock 우회|
|화염 제트|같은 nozzle–flame–지정 target|출구 분리·다른 인물 또는 target에 연결|
|광학 플레어|capture image plane의 optical artifact|lighting 슬롯으로 옮겨 잠긴 camera property 우회|
|태양 현상|same solar body·observation mode·channel|지상의 불·별도 태양 복제·잘못된 배색 |
|의복 열손상|같은 wearer의 같은 garment patch; appearance와 material|추가 노출·다른 옷·신체 손상·opacity 변경|
|촛농 접촉|같은 subject의 지정 skin patch와 deposit contact|다른 신체 부위·다른 인물·동의·sexual tone 추가|

`subject`, `concept`, `event` 등 frozen dimension이 닫혀 있으면 후보의 존재가 새 변경 권한을 만들지 않는다. core의 해당 의미가 이미 완성됐다면 baseline 유지가 정상이다. 신체·관능 후보의 eligibility는 실제 요청 문맥과 기존 controls/age/tone 계약에서 판단한다.

## 5. activation과 시각 프로필 작성

모든 새 live profile source는 `authored_components`로 작성한다. compiler가 생성하는 `component_semantics`, `required_evidence_fields`, `evidence_requirements`, `render_gates`, `composition_instruction`을 source에 중복 저장하지 않는다.

[PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)의 18개는 collective V2 예시다. 각 예시는 구성요소 3개를 하나의 선택된 실현으로 묶고 3개 field·4개 gate를 만든다. 이를 그대로 모든 불 용어의 필수 3요소로 채택하지 않는다. 정의상 필요한 duty와 선택적 연출을 검토해 atomic V1, collective V2 또는 기존 프로필 재사용으로 결정한다. F132처럼 기존 데이터와 가까운 프로토타입은 실제 신규 profile 개수에 그대로 더하지 않는다.

activation 원칙은 다음과 같다.

1. 요청 의미와 정의·부정·관측 방식은 candidate 조회 전에 독립적으로 해석하고 freeze한다.
2. `불`, `화염`, `파란 불`, `플레어`, `코로나`, `필라멘트`, `흑연` 등 넓거나 다의적인 단어에 장면 묶음을 hard activation하지 않는다.
3. 좁은 exact term에는 단일 의미·완전한 owner 관계·positive와 인접 hard negative가 있어야 한다.
4. BM25F·embedding·fusion hit는 advisory다. 검색 유사도·seed·creativity는 hard duty를 만들지 않는다.
5. 선택된 optional profile은 전체 계약을 채택한다. 일부 field/gate만 선택하거나 소유자가 틀린 부분을 hidden 처리하지 않는다.
6. 화면 밖 화원·EUV channel처럼 픽셀에 없는 정보는 requester/observation metadata로 결합한다. native gate에는 보이는 수광면·형태만 둔다.
7. requester definition·명시적 제외·정당한 property lock은 이후 taxonomy보다 우선한다.

prototype의 긴 complete-owned-proposition exact term은 충돌을 피하는 형태 예시다. 실전 alias 품질·형태소·negation·다국어 도달성을 검증한 exact 목록으로 간주하지 않는다.

## 6. 단계별 작업과 완료 조건

### 단계 A: 기준 상태 보존과 채택 범위 확정

현재 primary에는 다른 작업의 dirty/untracked 항목이 있다. 구현 시 active worktree/artifact를 확인하고 적합한 격리 checkout을 사용한다. 이번 research 폴더와 기존 사용자 작업을 별개로 보존한다. unrelated 파일을 reset/stash/stage하거나 파생 index의 충돌을 수작업으로 덮지 않는다.

현행 source/manifest/index의 hash와 관련 tests baseline을 새로 기록한다. 이 조사 시점의 source 상태가 구현 시점의 current라는 가정을 하지 않는다. P0 중 검토 완료된 실현을 선택하고 추가 전문 출처 항목과 기존 동치 항목을 ledger에서 분리한다.

완료: 원본 보존 receipt, 검토한 채택 목록, 기존 ID 재사용 또는 신설의 이유, source access 한계.

### 단계 B: 원자 데이터와 소유 관계 반영

새 fire 파일에는 검토된 후보만 넣고 중앙 manifest에 등록한다. fields는 기존 loader/validator가 이해하는 구조를 사용한다. 연구 URL·source title·bulk keyword 목록·정신 상태·연구 과정 문자열을 candidate text나 relevance text에 넣지 않는다.

같은 객체의 3요소를 무조건 복사하는 대신 source/receiver/target별 소유를 완성한다. 실제 범위를 `affected_dimensions`와 `affected_properties`로 선언한다. generic tags가 잘못된 place/role/species facet을 만들지 않도록 명시적 facets와 기존 applicability guards를 확인한다.

완료: dictionary validation, owner/property ledger, profile compile, unique gate ID, 기존 source 보존.

### 단계 C: 인덱스와 runtime generation 반영

source 변경을 cooperative update 경계 안에서 수행한다. 의미 텍스트나 registry hash가 바뀌면 semantic index와 visual-profile index를 각각 canonical builder로 재생성한다. field/recipe·BM25F 문서/통계·manifest·referenced shard 체크를 함께 수행한다.

캐시 벡터 재사용은 entry key, 완전한 입력 텍스트, provider, model, dimensions가 같은 경우에만 허용한다. 신규·변경 텍스트에는 실제 embedding이 필요할 수 있다. batch size 1 정책을 지킨다. 새 데이터의 “embedding 호출 0회”를 미리 약속하지 않는다.

source와 두 required index가 모두 유효할 때 immutable runtime generation을 발행하고 CURRENT 전환과 receipt를 검증한다. canonical builder는 publication hook을 가질 수 있으므로 격리 runtime store를 사용한다. 오래된 in-flight generation은 보존한다. 이번 연구 폴더는 runtime source manifest에 등록하지 않는다.

완료: fresh source fingerprint, 두 index deep check, generation receipt, source/index hash agreement, 실제 lookup 근거.

### 단계 D: 회귀·팩·프롬프트 검증

[REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 44쌍을 의미·exact·semantic paraphrase·선택/잠금 변이로 실행한다. fake-vector로 구조를 확인하고 real rebuilt index로 도달성을 확인한다. 해당 index를 썼다는 receipt가 필요하다.

현행 존재를 확인한 관련 suites는 다음과 같다.

- `tests.test_photo_core_retrieval`
- `tests.test_photo_bm25f_retrieval`
- `tests.test_photo_visual_profile_retrieval`
- `tests.test_photo_visual_obligations`
- `tests.test_photo_candidate_semantics`
- `tests.test_photo_research_integration`
- runtime freshness와 workflow bridge에 영향이 있으면 `tests.test_photo_runtime_freshness`, `tests.test_photo_workflow_runtime_bridge`

manifest와 dictionary는 `scripts/validate_photo_prompt_dictionary.py`로 확인한다. candidate slots·profile registry·양쪽 index를 넓게 변경하는 최종 반영에서는 full unittest discovery를 한 번 실행하고 baseline 실패와 신규 실패를 분리한다. 이미 통과한 검증은 새 변경·실패·미해결 위험 없이 반복하지 않는다. frozen holdout·historical source·과거 pack을 새로운 소스로 다시 해석해 PASS로 만들지 않는다.

후보 노출을 확인한 뒤 선택 여부·literal relation evidence·property lock·composed prompt·exact runtime string을 검증한다. zero adoption 사례도 포함한다. 일반 fire 문맥이 자동으로 무기·화상·판타지·성적 장면을 추가하는 mutation은 실패해야 한다.

완료: paired routing 결과, real-index exposure, 명시적 채택/거절, selected obligation 전체 evidence, prompt/runtime audit.

### 단계 E: 원본 픽셀과 실제 기여 확인

이미지 검증은 별도 구현·검증 단계다. [PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)에 10개 대표 사례와 A/B/C 프로토콜을 작성했다.

독립 baseline을 freeze한 뒤 A는 baseline, B는 현재 데이터, C는 검토된 fire 확장을 사용한다. 동일 requester meaning·controls·reference scope·camera scope·model·transport를 유지하고 각 arm의 source/index/runtime receipt를 분리한다. authoring 중 다른 arm의 후보·프롬프트를 초기 영감으로 사용하지 않는다.

원본 크기에서 selected pack의 gate 전체를 판정한다. partial·hidden·wrong owner는 실패이며, 생성 차단은 `blocked_unscored`로 보존한다. 방화·의도·통증·동의·온도·화학종처럼 픽셀이 지원하지 않는 주장은 gate에서 제외한다. 모든 시도와 원본·정확한 요청 bytes를 보존한다.

검토자는 설명 키워드 없이 먼저 이미지 인상을 보고 fidelity와 선호를 따로 판정한다. 사용자 수용은 실제 사용자 판단으로만 기록한다. 작은 pilot은 실행 가능성 확인이며 품질 개선의 일반적 증명이 아니다. 여러 독립 요청·반복 비교까지 확보한 뒤 개선을 주장한다.

완료: native gate 결과, 모든 시도 보존, 통제 비교, 별도 사용자 판단.

## 7. 이번 단계에서 확인한 것

[VALIDATION.json](VALIDATION.json) 기준으로 후보 131개의 현재 slot·dimension/property 구조, source 참조, 프로토타입 18개의 source/activation/compiler shape, evidence 54개·gate 72개 생성, 현재 등록 프로필과 gate ID 비충돌을 확인했다.

이 검증은 draft 형식의 정합성이다. 실제 owner consumer 연결, registered dictionary 전체 적합성, retrieval activation, 임베딩, runtime 발행, 후보팩·프롬프트 audit, 픽셀·사용자 수용은 pending이다.

연구 문서·초안·계획을 이 폴더에 저장했다. 실제 채택 전 검토해야 할 항목과 성공 조건이 모두 ledger·case에 연결되어 있어 다음 구현을 좁은 단계로 시작할 수 있다.


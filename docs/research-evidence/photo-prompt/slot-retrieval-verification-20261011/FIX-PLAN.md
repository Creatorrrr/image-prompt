# 슬롯 후보 조회 단계별 수정 계획

작성일: 2026-10-11 (Asia/Seoul) · 상태: 계획만 작성, 구현 미착수

목표는 **실제 데이터에서 요청 의미와 소유 범위에 맞는 후보를 조회하고, 맞지 않는 후보의 노출과 채택을 줄이는 것**이다. 한 장면에 모든 슬롯을 켜거나 114개 슬롯을 무조건 활성화하는 것을 목표로 삼지 않는다. 단계마다 수정·비교 검증·runtime 반영을 마친 뒤 다음 단계로 진행한다.

## 1. 기준선과 수정 원칙

근거는 [슬롯 조회 검증 리포트](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/REPORT.md)와 해당 디렉터리의 원시 결과다. 검증 당시의 작업 폴더에는 커밋되지 않은 수정이 포함되어 있다.

| 기준 | 확인된 상태 |
|---|---|
| HEAD | `218e339320f0e3c27aac3f2a48a9299812b16935` |
| 검증 generation | `f492f8a428edcf489d7fd9b0c2f2525b2dc7ac1c180446cf20f6eb5af7a19870` |
| source fingerprint | `614b5e4fb66959c7304e45bfbb1de601f6cbd892dd908812e2e7492f7ecf843b` |
| 적재 | 114개 슬롯, 12,043개 후보; source/loader/index ID 누락 없음 |
| 정확 표기 조회 | 40,638/40,643 적중; 5개 native alias가 토큰 0개 |
| 조회 경로 | 109개 슬롯 반환 확인; 5개 슬롯의 일반 조회 경로 차단 |
| 독립 장면 | 적합한 후보와 주체·상황이 다른 후보가 함께 노출 |
| 관련 회귀 검사 | 기존 검증에서 40개 통과; 전체 suite 통과를 뜻하지 않음 |

계획 작성 시 assets/scripts/precore 196개 파일이 검증 후 해시와 일치함을 다시 확인했다. 실제 구현을 시작할 때도 해시를 비교한다. 달라졌으면 변경분을 별도 기록하고 새 기준선을 만든다.

- 후보 접근 전 requester 원문, creative controls, authorial core, property lock, embodiment 검증 순서를 유지한다. 유지보수 데이터로 만든 probe를 실제 창작 성공률로 보고하지 않는다.
- 후보는 선택 사항이다. 조회 성공이 requester 의무·hard gate·최종 채택으로 바뀌지 않으며, 후보를 전부 거절하는 경로도 보존한다.
- 정상적인 subject/domain/context 제외를 조회 결함으로 세지 않는다. 특정 fixture를 통과시키기 위해 전역 guard를 풀지 않는다.
- source 의미·소유 범위 → focus와 eligibility → 순위와 cap 순으로 고친다. cap 확대나 synonym 추가를 첫 해결책으로 쓰지 않는다.
- 현재 schema에 없는 `enabled`/`status` 같은 필드를 임의로 넣지 않는다. 역할 구분은 우선 유지보수 명세와 검사로 표현하고, runtime schema 변경이 필요한 경우 별도 변경으로 다룬다.

## 2. 진행 순서

| 단계 | 독립적인 수정 단위 | 완료 시 확인할 결과 |
|---|---|---|
| 0 | 기준선·슬롯 역할·의미 평가 사례 고정 | 비교 입력과 판정 기준이 수정 전에 저장됨 |
| 1 | `occasion_context` 소유 범위 복구 | 실제 행사 의미가 있는 공개 CLI 입력에서 적합한 후보 반환 |
| 2 | 두 guard 슬롯의 데이터 역할 정리 | 시각 후보와 제어 지침이 구분되고, 근거 없는 억제가 유입되지 않음 |
| 3 | domain 연결 및 adult 후보 scope 정리 | 의미가 있는 경우만 해당 경로가 열리고 age-only 요청과 구분됨 |
| 4 | native alias 문자 지원 | 문제의 5개 표기 검색 성공 및 기존 문자 체계 비회귀 |
| 5 | 주체 typing·문맥·owner focus 개선 | 일반 장면의 의미 이탈 감소, 명시한 특수 장면의 검색 보존 |
| 6 | 남은 fusion·관측 우선순위·cap 문제 조정 | 같은 입력·같은 cap에서 필요한 후보의 노출 개선 |
| 7 | 통합 검증·runtime 반영·최종 보고 | 실제 CLI/receipt/audit로 새 generation과 변경 효과 확인 |

단계 4는 공유 tokenizer의 영향이 크므로 별도 변경으로 유지한다. 단계 6은 단계 5 후에도 순위·cap 문제가 남았다는 증거가 있을 때만 수행한다. 단계 7의 절차는 각 단계의 반영에도 적용하고 마지막에 전체 비교를 반복한다.

## 3. 단계별 작업

### 0단계 — 비교 가능한 기준선 만들기

1. 기존 변경 22개 tracked 경로와 untracked 작업을 보존한다. 구현은 격리된 작업 폴더에서 진행하고 현재 source·코드·index/shard 바이트를 재현한다. HEAD에서 만든 새 worktree에는 현재 미커밋 데이터가 자동으로 복사되지 않으므로 해시가 같은지 먼저 확인한다.
2. 114개 슬롯의 역할표를 작성한다. 각 행에는 출처, 후보 수, 실제 소유 차원, 필수 context/domain, 정상 제외 조건, 일반 후보/명시한 특수 맥락 후보/제어 데이터 구분, 대표 양성·음성 입력을 기록한다. 후보의 존재와 정상 사용 가능성을 따로 표시한다.
3. 기존 8개 장면은 개발용 재현 사례로 남긴다. 새 디렉터리에 현재 authoring 계약을 만족하는 원문·controls·feature selection·baseline·core·property lock·실제 검토한 embodiment record를 작성한다. 요청한 모든 속성과 주체 수·종류·owner를 freeze하고, camera가 요청된 경우 capture camera 소유도 명시한다. 기존 합성 record를 정상 검토 기록으로 재사용하지 않는다.
4. 후보 문구를 베끼지 않은 새 holdout 12개 이상을 한국어·영어로 나누어 고정한다. 일반 사람·물체·동물·환경, 명시한 fantasy/특수 맥락, 제외·부분 lock을 포함한다. 먼저 요청과 core를 고정하고 그 후 후보 적합성을 판정한다. 기존 8개 장면은 이미 진단에 사용했으므로 새 holdout으로 세지 않는다.
5. 이후 단계별로 양성 입력과 가장 가까운 음성 입력을 추가한다. 입력을 고친 실험과 코드만 고친 실험을 구분한다. 같은 frozen 입력을 쓰는 비교에서만 코드 변경의 효과를 주장한다.

**평가:** 후보를 `동일 의미`, `열린 속성에 대한 호환 가능한 제안`, `주체/맥락/locked property 충돌`, `판정 보류`로 구분한다. 의미가 같은 복수 후보를 허용한다. 단일 ID 적중만으로 의미 정확도를 계산하지 않는다. 판정 보류는 통과로 승격하지 않는다.

**검사:** [authorial core 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_authorial_core.py), [prepack 격리 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_prepack_isolation.py), [feature selection 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_precore_feature_selection.py), [embodiment 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_embodiment.py)를 기준으로 fixture 유효성을 확인한다.

**완료 기준:** 수정 전 결과와 평가표가 저장되고 새 fixture의 계약 오류가 0건이다. 독립 장면의 실제 의미 판단과 자동 구조 검사의 결과를 분리한다. 이 단계에서는 생산 데이터·retrieval 로직을 고치지 않는다.

### 1단계 — `occasion_context` 조회 복구

**대상:** [기본 tags](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json), [worldbuilding extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_worldbuilding_extension.json), [CJK worldbuilding extension](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_cjk_worldbuilding_extension.json)의 합계 106개 후보. 기본 tags에 있는 24개만 고치고 완료로 세지 않는다.

1. 후보별 실제 효과를 읽어 `affected_dimensions`와 필요한 `affected_properties`를 작성한다. 행사 시점은 `timing`, 행사 장소는 `setting`, 실제 동작은 `action` 등 현행 허용 차원에 연결하되, 후보가 바꾸는 효과를 빠뜨리지 않는다. 후보별 소유 범위를 우선하고 슬롯 전체에 넓은 차원을 일괄 부여하지 않는다.
2. 꽃·군중·특정 의식·문자 없는 장식 등 추가 효과도 별도로 검토한다. 기존 문구의 `no readable ...` 같은 억제 지침을 requester 제외나 의무로 옮기지 않는다. 필요한 관찰 상태는 후보의 선택 가능한 시각 의미로 정리한다.
3. [focus 생성 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:9815)가 행사·시점의 frozen 근거를 읽는지 확인한다. source scope 복구만으로 해결되면 generator 코드는 수정하지 않는다.

**검사:** 졸업식 직후·행사 준비·천체 관측 등의 적합한 KO/EN 사례로 서로 다른 source의 후보를 확인한다. 무관한 찻잔 사진, 명시적으로 제외한 행사, 고정된 시점·장소의 변경을 대조한다. [candidate semantics](/Users/chasoik/Projects/image-prompt/tests/test_photo_candidate_semantics.py)와 [core retrieval](/Users/chasoik/Projects/image-prompt/tests/test_photo_core_retrieval.py)에 재현 검사를 추가한다.

**완료 기준:** 세 source의 scope 검토 누락 0건, source 계약 검사 통과, 양성 입력의 공개 CLI에서 실제 해당 의미 후보 노출. 행사 근거가 없는 입력을 기본 행사로 채우지 않고 locked property를 바꾸는 채택은 audit에서 거절한다. 다른 슬롯의 source 변경은 이 단계에 섞지 않는다.

### 2단계 — `safety_profile` / `costume_absorption_guard` 역할 정리

**대상:** 기본 tags의 21개 safety profile과 12개 costume guard. 두 슬롯의 빈 ownership을 일괄 채워 활성화하지 않는다.

- `safety_profile`: 현재에는 비신체화·anti-likeness·anti-selfie·anti-sexualized 등 제어 문구가 있다. 일반 positive 후보로 활성화하지 않는 방향을 우선한다. 사용하는 코드·참조를 확인하고, 제어 용도의 유지 또는 후보 데이터에서의 정리를 명시한다. 이를 새 억제 규칙이나 pre-core 요청 분류기로 바꾸지 않는다.
- `costume_absorption_guard`: 장식과 신체 구조의 분리 같은 실제 owner 관계와 의상·신체 표현을 억제하는 지침을 행별로 나눈다. 시각 관계는 적합한 기존 슬롯의 선택 가능한 component/관계로 표현하고 실제 효과와 소유 범위를 선언한다. 업무 사물 중심 고정·anti-fetish 등 지침은 시각 후보로 활성화하지 않는다.
- helmet을 벗기거나 뒤로 미는 식의 연출, 새 귀·꼬리 추가, 의상이나 신체 가리기를 해부학 구분의 기본 해결책으로 강제하지 않는다. requester가 정한 신체·의상·reference 범위를 먼저 보존한다.
- 이동·제거가 필요한 ID는 출처와 모든 bundle/profile/graph 참조를 점검하고 변경 대응표를 남긴다. 과거 pack은 원래 generation으로 계속 감사한다. 과거 evidence와 receipt를 새 ID나 source hash로 덮어쓰지 않는다.

**검사:** 장식 귀/실제 귀, 머리 장식/뿔, 후드 trim/신체 털의 양성·인접 음성 사례와 locked wardrobe 사례. [positive retrieval](/Users/chasoik/Projects/image-prompt/tests/test_photo_positive_retrieval.py), candidate semantics, prepack isolation, 공개 composed audit를 확인한다.

**완료 기준:** 33개 행의 역할 결정과 참조 점검 완료, 근거 없는 의미 억제 유입 0건. 의도적으로 일반 후보에서 제외한 슬롯은 비활성 역할로 보고하며 조회 실패 숫자를 감추기 위해 성공으로 계산하지 않는다. source ID 수가 바뀌면 정당한 이동·정리와 실수로 누락한 ID를 구분한다.

### 3단계 — domain 연결과 adult 후보 소유 범위 정리

**대상:** [quality-layer routing](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json), [domain resolver](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:2646), 기본 tags 및 manifest에 등록된 관련 extension. `adult_context` 6개, `fetish_styling` 24개를 모두 검토한다.

1. **일반 사진 domain:** `portrait`/`fashion`/`beauty`/`social`을 필요로 하는 후보의 실제 의미와 routing 부재 영향을 확인한다. frozen 의미가 명확한 경우만 authored route에 연결한다. `style.domain` 값을 무조건 domain으로 복사하거나 negated 단어를 양성 근거로 사용하지 않는다. `capture_context`는 이미 반환된 사례가 있으므로 슬롯 전체를 고장난 것으로 취급하지 않는다.
2. **adult 전용 경로:** 사람의 성인 나이와 sexual/fetish 맥락을 구분한다. `adult`라는 age 단어 하나, 또는 intensity 값만으로 adult domain을 켜지 않는다. 기존 adult_appeal scope·eligibility를 확인하여 typed subject, requester 의미, creative controls, open property를 함께 보존하는 방식으로 연결한다.
3. **후보 scope:** 중립적인 패션 소재 연구·오리지널 캐릭터 design context까지 모두 `sexual_tone`에 속하지는 않는다. 각 후보의 실제 효과에 따라 appearance/material/style 등 적합한 경로로 정리하고, 성적 의미를 가진 행과 분리한다. 잘못된 성적 scope를 domain alias 추가로 가리지 않는다.
4. 일반 domain 데이터 변경과 adult eligibility 로직 변경을 별도 변경으로 검토한다. 필수 domain guard는 적합한 대체 조건이 입증되기 전까지 유지한다.

**검사:** 명시한 adult fashion/fetish 맥락, 중립 성인 portrait/패션 소재 연구, no-people/nonhuman, 명시 제외, 0 값 controls, sexual-tone/property lock, 같은 조건의 KO/EN 요청. [adult scope](/Users/chasoik/Projects/image-prompt/tests/test_photo_adult_appeal_scope.py), [adult visual semantics](/Users/chasoik/Projects/image-prompt/tests/test_photo_adult_appeal_visual_semantics.py), [creative controls](/Users/chasoik/Projects/image-prompt/tests/test_photo_initial_creative_controls.py), positive retrieval을 확인한다.

**완료 기준:** 정당한 맥락에서 필요한 슬롯/후보가 공개 CLI로 반환된다. 중립 성인 요청의 성적 domain 오인·명시 제외의 양성 역전·닫힌 property의 채택은 0건이다. 후보를 다른 슬롯으로 옮긴 경우 새 소유 범위와 참조까지 검증한다.

### 4단계 — 저장된 native alias 검색 지원

**대상:** [BM25F tokenizer](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/bm25f_retrieval.py:19)와 이를 공유하는 slot/semantic/visual BM25F 및 캐시 recipe.

1. `साड़ी`, `धोती`, `ชุดไทย`, `ثوب`, `عباية`가 빈 토큰이 되는 문제를 복구한다. Unicode letter/mark를 보존하는 분절을 검토하고 결합 문자·정규화·문자 경계를 테스트한다. 현행 Hangul 어미 처리와 CJK authored lexicon 처리를 보존한다.
2. 한국어 substring 오탐이나 mixed-script 별도 단어 결합을 늘리는 단순 `\w+` 교체는 피한다. generic tokenizer에 의상·문화별 의미 표를 넣지 않는다. transliteration synonym 추가로 native 표기의 실패를 숨기지 않는다.
3. tokenizer recipe를 갱신하고 공유 BM25F 산출물·메타데이터·캐시를 다시 생성한다. 새 코드에서 이전 recipe를 유효한 cache로 받아들이지 않게 한다. embedding text/vector space가 같으면 호환 검증을 거친 기존 벡터를 재사용한다.

**검사:** [BM25F 회귀 검사](/Users/chasoik/Projects/image-prompt/tests/test_photo_bm25f_retrieval.py), slot query fusion, positive retrieval, runtime freshness. 저장 native alias, 혼합 문자, 결합 문자, 구두점, KO/EN/CJK의 기존 양성·인접 음성을 검사한다. 전체 현재 corpus의 en/ko/alias exact 조회를 다시 실행한다.

**완료 기준:** 문제의 5개 native 표기로 정확한 source ID가 owning-slot cap 안에 반환된다. 유지된 원래 후보의 EN/KO 검색에 새 미적중이 없고, 새 normalization 오탐·오래된 cache 수용이 없다. 전체 적중과 cap 내 적중, 실제 pack 노출은 각각 보고한다.

### 5단계 — 주체 typing·문맥·owner focus 개선

**대상:** [subject category](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:1762), `core_slot_entry_eligible`, `core_slot_focus_queries`, 실제 문제가 있는 authored candidate/facet/context 데이터.

1. `coffee_cup`의 food/object 경계부터 고친다. 음료 내용물과 컵·용기 owner를 구분하고, 기존 음식 주체를 전역으로 object로 바꾸지 않는다. 적합한 기본 후보가 원래 데이터에 있는지 먼저 확인한다.
2. 찻잔→골렘/자동인형, 작은 새→창세 동물/와이번, 친구의 인사→노래방, 회로→rail 장치/살아 있는 갑옷처럼 추가 전제가 큰 후보를 검사한다. coarse category뿐 아니라 후보가 실제 요구하는 subtype·owner·역할·상황을 authored facet/context로 표현한다. 모든 fantasy 후보를 금지하는 전역 규칙은 만들지 않는다.
3. material/light/action 등의 focus가 해당 carrier·property의 frozen 근거를 읽는지 검증한다. 다른 owner의 색·방향·질감이나 전역 긴 scene 문구가 focus를 대체하지 않게 한다. source 데이터 수정과 projection 코드 수정은 분리해 비교한다.
4. 적합한 일반 후보가 없으면 그 의미의 관찰 가능한 component·관계 데이터를 보완한다. benchmark 문장을 alias로 복사하거나 동의어만 늘리지 않는다. 출처·추상화 근거는 연구 evidence에 남긴다.

**검사:** 앞선 8개 장면의 완전한 core 사례, 새 holdout, 물체/내용물·일반 새/요청한 fantasy 동물·친구 인사/요청한 노래방 등의 대조. [slot data cleanup](/Users/chasoik/Projects/image-prompt/tests/test_photo_slot_data_cleanup.py), core retrieval, candidate semantics, [camera owner](/Users/chasoik/Projects/image-prompt/tests/test_photo_camera_owned_clauses.py), positive retrieval을 확인한다.

**완료 기준:** 지적한 주체·상황 이탈이 재현 사례에서 해결되고 명시한 특수 장면의 검색은 유지된다. 고정 holdout에서 충돌 후보 비율이 줄고 필요한 후보의 cap 내 노출은 감소하지 않는다. 단순 추가 detail과 주체 변경을 구분해 평가한다. 의도적으로 비인간에서 제외되는 슬롯 등의 정상 guard는 보존한다.

### 6단계 — 근거가 남은 순위·공유 cap 문제만 조정

**대상:** `retrieve_core_slots`의 whole/focus BM25F fusion, frozen observation 우선순위, 슬롯 간 admission.

1. private 유지보수 trace에 focus 입력, eligible ID, whole/focus 순위, observation 경로, 슬롯 cap 탈락, 전체 cap 탈락을 기록한다. 원래 49건의 rank/fusion/cap 진단을 세부 원인으로 나눈다. query까지 바꾼 좁힌 probe는 cap만의 효과를 증명하지 않는다.
2. 동일한 frozen 입력에서 한 번에 하나의 요소만 바꿔 비교한다. 올바른 owner focus, 대표 후보 선택, observation 우선순위와 중복 처리 순으로 검토한다.
3. 전체 64개, core 4개/support 2개 한도를 기준으로 개선한다. cap 변경이 필요하다는 별도 증거가 없으면 유지한다. 새 default slot padding·필수 후보 수·무조건 모든 슬롯 quota는 넣지 않는다.
4. score/rank/trace는 maintenance evidence에만 둔다. public pack의 optional·unordered 표현과 audit 재계산 가능성을 유지한다.

**검사:** [slot query fusion](/Users/chasoik/Projects/image-prompt/tests/test_photo_slot_query_fusion.py), core retrieval, [runtime improvement](/Users/chasoik/Projects/image-prompt/tests/test_photo_retrieval_runtime_improvement.py), 밀집·희소 장면, empty query, 후보 전부 거절, 부분/전체 lock, tamper 검사.

**완료 기준:** 같은 cap에서 원인으로 확인한 필요한 후보의 노출이 개선되고 holdout precision·scope 경계가 악화되지 않는다. cap 위반·default padding·core 변경·private rank 유출 0건. 효과가 없거나 문제의 원인이 source/context라면 해당 순위 수정은 채택하지 않는다.

### 7단계 — 통합 검증과 runtime 반영

1. source manifest를 유일한 등록부로 사용한다. 원본 source와 참조를 먼저 고치고 derived index를 재생성한다. index JSON이나 shard를 수작업으로 맞추지 않는다.
2. 먼저 격리된 runtime store에서 검증한다. cooperating 수정은 `source_update(root, store)`로 묶고 중간 빌더/validator 실행에는 필요 시 `--no-runtime-publication`을 쓴다. 변경 영향에 맞춰 semantic index와 visual sidecar를 정합하게 만든 뒤 publisher로 검증 완료된 generation을 생성한다.
3. text가 바뀐 문서만 호환되는 embedding 재사용 조건을 확인해 재빌드한다. provider/model/dimensions/text/recipe가 다르면 재사용하지 않는다. policy-only 변경도 source hash binding과 필요 sidecar를 갱신한다. tokenizer 변경은 공유 BM25F recipe와 파생물을 함께 갱신한다.
4. 실제 전체 source exact 조회, 114개 역할표에 따른 경로 검사, 새 authoring benchmark의 공개 CLI·composer view·receipt·`audit_core_retrieval`을 수행한다. 선택한 후보를 사용하는 composition과 후보를 거절한 composition을 별도 작성하여 전체 composed audit와 실제 postcomposition embodiment 검토도 확인한다.
5. source/ID/hash 변조, candidate 삭제, stale cache/receipt/code, 중단된 publication을 검증한다. 새 generation은 완성된 뒤 원자적으로 활성화하고 구 generation과 receipt는 보존한다. 코드 변경에는 matching CLI/worker를 사용한다.
6. 단계별 관련 회귀 검사를 먼저 수행한다. 공유 tokenizer·eligibility·routing 변경은 영향 범위 전체로 확장한다. 넓은 suite가 실패하면 같은 수정 전 기준선에서 해당 selector를 재현하고 신규 실패/기준선 실패/미해결을 구분한다. 미실행·미해결 suite를 통과로 보고하지 않는다.

**공통 완료 기준:** loader/index ID 정합성, source freshness, core/lock/negative-intent 경계, 공개 CLI 및 audit 오류가 0건이다. 의도한 데이터 정리로 바뀐 수는 ID 대응표로 설명한다. 자연어 평가의 분모와 정상 제외를 유지하고 단계별 개선·회귀를 함께 보고한다. 이미지 생성·픽셀 품질·사용자 선호는 이 수정 검증의 별도 범위다.

## 4. 매 단계에 남길 측정값과 산출물

| 측정 | 분모와 판정 |
|---|---|
| source 적재 정합성 | 현재 등록된 슬롯/ID 전체; 의도한 이동·정리는 별도 ledger |
| exact addressability | 현재 en/ko/명시 alias별 전체·cap 2/4·top 24; 유지된 기존 질의는 개별 회귀 비교 |
| eligible/focus 경로 | frozen context로 사용 가능한 후보 및 슬롯; 정상 제외와 ownership/focus 결함 분리 |
| 실제 pack recall | 필요한 의미의 후보가 owning-slot/전체 cap 후 노출된 사례 비율 |
| 후보 precision | 판정 가능한 노출 후보 중 동일 의미/호환 제안의 비율; 충돌·보류 수 별도 |
| 경계 회귀 | 제외 역전, owner 혼동, locked property 변경 채택, candidate→hard duty, core 변경 건수 |
| 비용과 모드 | 실제 keyword/hybrid 등 실행 모드, rebuild 문서 수·벡터 재사용·API 호출 여부 |

새 evidence는 원래 검증 디렉터리와 분리해 단계별로 저장한다. 원본 [exact 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/exact-recall.ndjson), 합성 probe, 옛 REPORT/SUMMARY, runtime generation을 덮어쓰지 않는다. 기존 harness는 실행 시 원래 위치에 쓰는 파일이 있으므로 새 출력 위치를 지원하게 복사·조정한 뒤 사용한다.

각 단계의 산출물은 수정 전후 입력·결과, source/code diff와 해시, 평가표, test/audit 로그, index rebuild 내역, generation/receipt, 실패와 정상 제외의 설명이다. 실행 시점에 테스트 대상과 합격 기준을 먼저 고정하며 holdout을 실패 후 편집하지 않는다.

## 5. 반영·되돌리기와 첫 작업 범위

- 변경은 단계별로 독립 검토 가능한 단위로 만든다. 구현 diff에는 관계없는 dirty 파일을 포함하지 않는다. 커밋·푸시·PR 상태는 실제 수행 여부와 분리해 보고한다.
- source·코드·index의 검증이 끝난 단위를 matching worker와 함께 반영한다. 중간 revision을 live 요청에 노출해 mismatch를 회피하지 않는다. 지연된 옛 publisher가 CURRENT를 덮지 않는지 확인한다.
- 되돌릴 때는 직전 통과 source·코드·필수 index 묶음과 matching worker를 복구하고 정상 publisher로 재검증한다. CURRENT 포인터만 손으로 옛 generation에 바꾸어 freshness 검사를 우회하지 않는다. 과거 pack replay는 원래 generation을 지정한다.
- 단계별 결과가 완료 기준을 못 맞추면 해당 변경은 반영하지 않고 원인을 기록한다. 이미 통과한 다른 단계와 원본 사용자 작업은 보존한다.

**첫 구현 묶음은 0단계의 비교 기준 마련 → 1단계의 `occasion_context` 복구**로 권장한다. 재현된 구조 결함이 명확하고 변경 범위를 세 source의 해당 슬롯으로 한정할 수 있다. 두 guard의 의미 변경, adult routing, Unicode tokenizer, 순위 조정은 각각 다음 변경으로 진행한다.

이 문서는 계획이다. 생산 source·코드·index 수정, 새로운 embedding/이미지 호출, runtime 반영, 커밋·푸시는 이번 계획 작성에서 수행하지 않았다. 구현 시에는 [스킬 유지보수 계약](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/references/maintenance.md)을 현재 코드와 함께 확인한다.

# 보컬로이드 외형 리서치 반영 계획

2026-10-04. 연구 산출물을 검토 가능한 authored data로 바꾸는 계획이다. 이 문서의 단계는 아직 실행하지 않았다. 기존 미커밋 캐릭터 외형 작업과 generated shards는 시작 상태 그대로 보존했다.

## 적용 원칙

1. 캐릭터명·상품명·연도·모듈명은 provenance다. 이름을 요청한 경우에도 자동으로 머리/옷/색/몸을 묶는 alias를 추가하지 않는다. 이름 기반 전체 디자인 resolver가 필요하면 별도 요청과 별도 source/version 계약으로 다룬다.
2. 데이터는 같은 owner의 관찰 가능한 구성요소와 directed relation을 기준으로 작성한다. region, attachment, material, surface motif, coverage, anatomy와 representation은 독립 속성이다.
3. 기존 프로파일 ID와 범위를 유지한다. high twin tail, 다른 lace subtype, external costume wing 같은 sibling이 필요한 경우 기존 기본 정의를 넓혀 서로 다른 의미를 합치지 않는다.
4. pre-core는 registry/candidate/index를 읽지 않는 기존 독립 규칙을 유지한다. 연구·정비 과정에서 파일을 읽은 것과 이미지 요청의 pre-core 해석은 별개다.
5. post-core는 frozen request/core에 대해 후보 슬롯과 registry 의미를 검색한 뒤 immutable v6 pack을 생성한다. exact contextual meaning, advisory 검색 hit, 선택된 조건, prompt evidence, pixels를 별도 기록한다.
6. 미해결 source·owner·property는 advisory/보류 상태로 둔다. scope가 빈 prop를 일괄 appearance에 편입하거나 candidate cap을 늘려서 덮지 않는다.

## 우선순위와 범위

|묶음|카드/관계|작업|완료 조건|
|---|---|---|---|
|P0 지역/연결/평면 형태|K09, K17, K34, K35, K44, K51–K56, K68|14개 후보 초안 중 1차 구조와 counterpart profile 작성|owner·component·property·source가 모두 확정되고 context holdout 통과|
|P1 의복·장식 변형|K02, K12, K24, K39–K42, K46–K47, K57, K59–K62, K64, K66–K67, K69–K71 중 scope 확정분|기존 정의 보강 또는 sibling; wing plate 포함|기존 기본 의미 회귀 없음, 재질·부착의 원본 증거 확보|
|P2 자료/매체/owner 선행|K04, K10, K18–K23, K25, K45, K58, K63, K70, K72|불충분 source, adult/chibi, independent prop scope 해소|선행 조건 해결 전 자동 채택 없음|

P0/P1은 카드의 초기 priority보다 실제 dependency를 우선한다. 예를 들어 후면 체결점을 보이지 않는 source로 확정할 수 없으면 P0처럼 보이는 항목도 보류한다. 26개 `new`는 연구 구조 수이며 profile 수/증가량은 중복 제거 뒤 확정한다.

## 단계 1 — 시점·판본·소유자 확정

작업 직전 현재 HEAD/dirty files, registry source hash, generated index 상태를 다시 기록한다. 지금 연구의 baseline은 HEAD `dee9f95896cf1e8eaa60d4cb02925b19f5c91374`와 기존 파일 86개 hash다. 다른 작업이 바뀌었으면 연구의 crosswalk를 최신 authored source와 다시 비교한다. 통합 작업은 별도 checkout/worktree에서 하고, 현재 수정 파일을 reset/stash하거나 generated index를 강제로 덮지 않는다.

자료에는 `case_label`, 상품/연도 `version`, `representation`, `source_id`, 원 URL, retrieval date, bytes hash, visible region, source qualification status를 유지한다. research schema는 그대로 runtime assets로 복사하지 않는다.

추가 확보가 필요한 자료는 다음과 같다.

|항목|현재 부족한 증거|요구하는 일차 자료|수용 조건|
|---|---|---|---|
|짧은 뒤묶음 K04|Len 기본 3면도의 독립 묶임점 불확정|후면의 tie/root가 분명한 공식 디자인|tie point와 짧은 tail 연결 동시 확인|
|고리 braid K10|Tianyi 200px와 V5 Lite HTML|해당 판본의 큰 정면/후면 setting art|braid crossing + 접힌 loop + fastening|
|freckle/lace/stitch K15/K41/K67|작은 face/패키지/그림 선|큰 공식 art 또는 실제 textile 보완 자료|작은 dot/실·open cell/봉제 경계 구분 가능|
|pinafore K45|검정 몸판만으로 apron/overdress 구분 부족|끈·bib·skirt의 전후면|trouser/apron과 다른 연결 확인|
|OLIVER/SONiKA|2차 source 또는 200px 대체 자료|동일 판본 공식 setting/package full art|초기 3D/의상 세부·wrap 영역을 판본별 확인|
|독립 소품 K58/K63/K70/K72|prop scope 없음/소품 정체성 불확정|owner/접속과 request effect scope|인물/소품/동료를 나누고 실제 umbrella/shaft 정체성 확인|

**단계 종료 기준:** 102행 provenance를 유지하고, 채택 대상 모든 source의 판본/매체/owner와 관찰 가능한 component를 특정한다. 불확정 사례는 qualified sample에서 제외하고 연구 lead로 남긴다.

## 단계 2 — 기존 의미와 중복 제거

[KEYWORD-RESEARCH.json](KEYWORD-RESEARCH.json)의 existing profile ID/definition을 최신 source와 대조한다. 의미의 identity는 라벨 일치가 아니라 carrier, cardinality, attachment, topology, spatial/color region, requested property와 적용 대상이다.

- 재사용 24개는 먼저 holdout을 측정한다. 부족한 positive paraphrase만 추가하고 새 ID를 만들지 않는다.
- 보강 15개는 기존 역할을 좁게 유지한다. high root, same garment hem, plate transmission 같은 modifier/sibling의 필요를 따로 판단한다.
- 새 구조 26개는 실제 source가 뒷받침한 범위부터 작성한다. independent prop이나 medium별 body 의미는 P2 dependency를 해결한다.
- 경계 7개는 adult activation, chibi medium, 실제 소품 이름을 유지한다. 모호함을 alias 확대나 몸 비율 추정으로 해소하지 않는다.

특별히 중복을 막을 조합은 `hime_cut_structural` vs K09, `sca_x16` vs K51, `midi_controller_external_sound_source` vs K54, `pfe_midriff` vs K34, `sw_cutout` vs 일반 K35, `clothing_ct062_*`/tailcoat vs K44, costume wing vs creature wing, garter band vs support strap, mesh vs motif lace다.

**단계 종료 기준:** 모든 제안이 reuse/modify/sibling/new/hold 중 하나로 정해지고 관련 기존 ID를 연결한다. 기존 ID를 지우거나 반례를 positive embedding에 넣지 않는다.

## 단계 3 — 시각 의미와 후보 원본을 함께 작성

### 시각 의미 프로파일

`activation`에 exact contextual terms, semantic component evidence, 요청된 carrier를 두고 관련 연령 조건을 유지한다. `semantics`에는 positive definition/구성요소, contrast, claim limits를 분리한다. `concept_candidate`에는 허용된 dimension/target/property를 넣는다.

`authored_components`의 하나의 authored source에서 match terms, `*_phrase` evidence field, instruction, native render gate를 컴파일한다. required relation이 같은 owner에 속하는지와 cardinality/연결 경로를 literal phrase에 포함한다. 모든 component를 all-of로 요구하되 요청에서 선택하지 않은 색·길이·원인·기능까지 의무로 넣지 않는다.

예시 3개는 [PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)에 있다. 현재 compiler가 evidence/gates를 만들 수 있다는 형식 확인까지 완료했으며, 전체 registry load/activation/opt-in/이미지 자격은 이 단계에서 별도로 검증해야 한다.

### 일반 후보 원본

entry마다 `id`, `ko/en`, positive aliases/paraphrases/keywords/embedding text, `concept_units`, directed `relations`, `affected_dimensions`, `affected_properties`, 필요할 때 `core_assertion_discovery`를 작성한다. 범위가 확정되지 않은 independent prop에는 discovery=true를 복사하지 않는다.

짧은 라벨만 남기지 않는다. 예를 들어 equalizer candidate는 “이퀄라이저” 대신 **평행 세로열·높이 차이·같은 옷 면**을 각각 온전한 positive unit으로 가진다. 공개 의미는 [photo_candidate_semantics.py:206](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/photo_candidate_semantics.py:206)의 `semantic_source`가 보존하도록 한다.

optional 관계 묶음은 `visual_semantics`의 component groups와 member candidate/slot, associated profile ID를 사용한다. `hard_profile_ids`라는 필드명이 있어도 association 자체가 hard obligation 승격은 아니다. `candidate_only`와 independent request component evidence 규칙을 유지하고 actual selected effects가 core lock/exclusion과 맞아야 한다.

### 반영할 파일

모든 경로는 `skills/photo-prompt-image-generator/assets/` 기준이다. 기존 domain source에 일반 구조를 넣는 것을 기본으로 삼는다.

|원본 파일|대상 구조|작성 조건|
|---|---|---|
|`photo_prompt_visual_obligations_subculture_appearance.json` / `photo_prompt_subculture_appearance_extension.json`|K09, hair hardware, cheek glyph, equalizer/keyboard/panel graphics|외형/표면 carrier와 color/length 분리|
|`photo_prompt_visual_obligations_clothing_structure.json` / `photo_prompt_clothing_structure_extension.json`|crop length, bounded opening, asymmetric hem, pinafore|기존 swimsuit/skin exposure와 ownership 분리|
|`photo_prompt_visual_obligations_accessory_structure.json` / `photo_prompt_accessory_structure_extension.json`|ear-mouth headset, circular arm gear, cap cross, legwear subtype|각 부품 접속과 wearable carrier 유지|
|`photo_prompt_visual_obligations_costume_cosplay.json` / `photo_prompt_costume_cosplay_extension.json`|rear costume panel, external wings, ear/mask placement|creature anatomy와 외부 costume support 분리|
|`photo_prompt_visual_obligations_textile_surface.json` / `photo_prompt_textile_surface_extension.json`|openwork/실/투과가 실제로 확인된 textile variants|`material` scope; 평면 무늬를 재질 의미로 섞지 않음|
|기존 body/character appearance 원본|필요한 기존 owner/age/medium 경계 보강만|기존 진행 중 작업과 stable identity로 통합; 무조건 덮어쓰기 금지|

원문 provenance와 관찰 한계는 research ledger에 유지한다. 이 단계에서는 별도 `vocaloid` runtime 파일이나 신규 이름 router가 필수라고 가정하지 않는다. 기존 extension이면 loader 등록을 추가할 이유가 없다. dedicated source가 실제로 필요해진 경우에만 schema/등록/검증을 함께 설계한다.

**단계 종료 기준:** candidate entry와 counterpart profile의 뜻·owner·property가 일치하고 compiler/schema를 통과한다. open/locked property·exclusion·명시된 user definition을 지키며 scope 미해결 후보는 자동 노출/채택되지 않는다.

## 단계 4 — generated index 재생성

authored sources를 먼저 통합한 뒤 semantic/visual profile index와 BM25F/exact surfaces를 재생성한다. 기존 dirty/generated shards는 새 데이터처럼 덮어 합치지 않는다. 새로운 index의 source hash가 실제 통합 원본에 묶여야 한다.

재사용 vector는 provider/model/dimensions와 **exact positive text**가 모두 일치할 때만 허용한다. 새/바뀐 positive text는 새 embedding이 필요할 수 있다. 현재 설정은 `gemini` / `gemini-embedding-2` / 768이며 실제 실행 시 loader 값과 다시 대조한다. 이번 연구에서 embedding 호출은 0회이고, 향후 0회 재생성을 보장하지 않는다.

도구는 기존 [build_semantic_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_semantic_index.py), [build_visual_profile_index.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py), [validate_photo_prompt_dictionary.py](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py)다. semantic builder의 `--dry-run`, visual builder의 `--check`와 `--cache-index`를 사용하되 현재 설정과 생성 순서에 맞춘다. placeholder를 그대로 명령으로 실행하지 않는다.

**단계 종료 기준:** current authored data와 index metadata/hash가 일치하고 `load_runtime_data()`가 통과한다. exact/BM25F/embedding이 같은 qualified 의미를 참조하고 removed/renamed IDs가 orphan이 되지 않는다. slot cap 4 core / 2 support, total 64 등의 기존 제한은 유지한다.

## 단계 5 — 실제 retrieval·후보팩·선택 검증

[PLANNED-HOLDOUTS.json](PLANNED-HOLDOUTS.json)의 36개 요청을 독립적으로 해석하여 core를 freeze한다. baseline corpus와 enriched corpus의 source/index hash를 각각 기록하고 같은 request/core로 비교한다. 학습/positive aliases에 그대로 넣지 않은 paraphrase, 최소 차이 반례, negation, owner, property lock, 연도·매체 경계를 포함한다.

|측정/검증|성공 기준|실패 시 조치|
|---|---|---|
|명시한 positive 구조|해당 열린 슬롯의 목표 entry를 기본 후보 범위에서 노출하고 profile candidate의 component match를 확인|positive wording/source scope를 개선; cap 확대부터 하지 않음|
|semantic/RRF 정렬|case별 rank/score와 top-k relevance를 기록; 실제 slot 기본 cap 기준 recall도 보고|한 평균으로 다른 family의 실패를 숨기지 않음|
|반례·부정·다른 owner|새 잘못된 hard activation 0건|carrier/component/negation 증거 조건 수정|
|body/medium/variant|chibi→human geometry, name→outfit bundle, year 혼합, identity 변경 0건|미해결 의미를 clarification/advisory로 유지|
|property lock·user definition|닫힌 property 변경·명시 user definition 무시 0건|slot/effect scope와 compatibility를 수정|
|public candidate 내용|authored unit과 directed relation 보존; unselected candidate는 optional|`semantic_source`/bundle association 결과를 실제 pack에서 확인|
|selected opt-in|같은 실제 owner/target/property에만 hard evidence/gates가 붙음|association 자체 승격 또는 owner 누락을 수정|
|pack integrity|원본 immutable pack과 audit hash 유지|뷰/후보팩을 직접 편집하지 않고 재생성|

현재 수량 제한 때문에 일부 matching advisory가 노출되지 않으면 실제 rank/cap/compatibility 이유를 분리한다. “검색 hit 있음”이나 높은 embedding similarity만으로 성공을 보고하지 않는다.

관련 기존 회귀는 `test_photo_hair_visual_semantics`, `test_photo_candidate_semantics`, `test_photo_visual_profile_retrieval`, `test_photo_bm25f_retrieval`, `test_photo_positive_retrieval`, `test_photo_clothing_terminology_semantics`, `test_photo_costume_cosplay_semantics`, `test_photo_body_morphology_semantics`, `test_photo_subculture_appearance_alternatives`, `test_photo_character_appearance_100`에서 변경과 맞는 모듈을 선택한다. 새로운 관계와 경계만 의미 있는 회귀로 추가하고 research 파일 생성 자체를 테스트하는 코드를 늘리지 않는다.

**단계 종료 기준:** 36개 request별 결과·노출 이유·선택 결과를 남긴다. positive geometry의 노출과 negative/owner boundary를 동시에 통과해야 data/retrieval layer를 승인한다. runtime/schema, actual pack, prompt evidence의 결과를 각각 기록한다.

## 단계 6 — 원본 픽셀 검증과 수용

[PLANNED-PIXEL-CASES.json](PLANNED-PIXEL-CASES.json)의 8개 family를 사용한다. first wave는 source와 scope가 확정된 regional hair / flat motifs / headset-hair hardware / garment opening부터 진행하고, 팔 장비·외부 날개·표식으로 확장한다. 독립 소품 family P08은 prop owner/effect scope를 해결한 뒤 실행한다. P04 crop/cutout은 배타적인 두 요청으로 분리한다.

baseline/enriched 두 arm은 같은 independently frozen request/core를 사용한다. candidate를 보이게 하려고 locked medium·pose·framing을 바꾸지 않는다. 해당 요청의 프레임으로 관계가 보이지 않으면 visibility 조건을 명시하고 `UNOBSERVABLE`로 기록한다.

각 실행에는 source/index/core/pack/prompt/image hash, 선택 profile/entry ID, literal component phrase, required relation, 원본 해상도 판정을 남긴다. `PASS`는 모든 선택된 component와 directed same-owner relation이 동시에 보일 때만 준다. 일부만 만족하면 `FAIL`; 필수 관계 가림은 `UNOBSERVABLE`이다. source 그림과 닮은 분위기, prompt audit, renderer process 종료만으로 pixel 합격을 주지 않는다.

실제 렌더 수·반복 수·비용은 실행 범위에서 정한다. 데이터 반영/검증을 요청한 것과 이미지 생성·외부 공개·commit/push는 별도 실행 범위다. 지금 연구에서는 어느 이미지도 생성하거나 외부 게시하지 않았다.

**단계 종료 기준:** data/schema, retrieval/pack, prompt, native pixels, 사용자 수용을 따로 보고한다. 깨진 필수 관계가 남아 있으면 integration/data 성공과 rendered 성공을 구분하고 qualification을 완료로 표시하지 않는다.

## 최종 인수 조건

- 원문 용어 72개와 추가 relation lead 24개의 처리 상태가 추적 가능하다.
- 판본/매체·소유자·긍정 정의·반례·선택 가능한 effect·source 한계를 기록한다.
- 새 후보는 실제 counterpart profile/owner/target/property와 이어지고 unresolved scope를 자동 채택하지 않는다.
- 원본에서 generated index를 재생성하며 현재 runtime source/index 계약을 통과한다.
- 36개 문맥·negation·owner holdout에서 잘못된 hard activation/lock 변경이 없고 목표 노출을 case별로 설명한다.
- 선택한 pixel family의 모든 required relation을 원본 해상도에서 확인하고 `partial_is_fail`을 적용한다.
- 기존 dirty/untracked 작업을 보존하고 결과를 단계별로 검토할 수 있다.

지금 완료된 부분은 상세 연구, 실제 source 관찰, 현행 데이터 대조, 14/3개 prototype 구조 검증, 실행 계획 작성이다. 위 통합·검색·생성 이미지 단계는 후속 실행이다.

# 시각 의미·후보팩 데이터 반영 계획

2026-10-06 KST · 실행 전 계획 · 활성 자산/런타임/인덱스 변경 없음

목표는 참조 대화의 이름을 캐릭터 preset으로 늘리는 것이 아니라, **같은 소유자의 부품·표면·연결·겹침·지역 배치**를 정확하게 검색하고 선택할 수 있게 만드는 것이다. 작품명·편수·원작/영화/무대·팬 작가·상품 범위는 출처 메타데이터로 유지한다. 연구 결과의 사실 상태와 채택 가능 상태는 별개다.

## 1. 채택 대상과 우선순위

120개 연구 단위, 후보 초안 111개와 선택형 묶음 8개를 작성했다. 111개를 모두 신규 entry로 추가하는 목표는 세우지 않는다. 기존 profile 60개·후보 14개와의 연결을 검토하여 재사용, 좁은 variant/sibling, 새 관계, 메타데이터, 보류로 나눈다. 전체 연결은 [RUNTIME-MAPPING.json](RUNTIME-MAPPING.json)에 있다.

|단계|우선 카드|할 일|완료 조건|
|---|---|---|---|
|P0 기존 원자 보강|H008/H011/H024/H048/H049/H050/H062/H070/H072/H097–H103/H111/H112|정확히 같은 구조의 한국어·영어 풀이, component evidence, carrier 표현을 보강. 다른 판본/owner는 분리.|기존 ID·guard·뜻·소유·문맥 보존, 새로운 별칭이 무관한 요구를 강제하지 않음.|
|P1 관계와 형태 차이|H002–H006/H027/H028/H040/H043/H058/H061/H063/H065/H075–H082|층, 위치, 접합, motif adjacency, 범위, 색 영역을 새 relation 또는 좁은 sibling으로 작성.|각 관계의 endpoint가 실제 carrier에 묶이며 모든 선택 component의 evidence/gate가 있음.|
|P2 소유·슬롯 확정|H051/H052/H054/H066/H068/H083/H084/H086/H088/H093–H095/H108/H109/H113–H119|얼굴/치아/손톱/투명성/소품/다중 인물의 target과 경로를 심사. 일반 형태는 특정 작품의 미확인 사실과 분리.|잘못된 슬롯에 넣지 않고 property lock·매체·소유·scope를 검사. 근거 없는 판본 사실은 보류.|
|P3 사례 출처 보충|H017/H019/H029/H033/H047/H052/H060/H068/H083/H084/H108/H109/H113–H118 및 43개 source lead|해당 편·장면·책 원문·캐스트·공개 스틸과 대조. H118 고정부 등 눈에 보이는 구조는 별도 검증.|확인한 문장/부위만 source-backed로 승격. 색·재질·뒤쪽·공정·기능을 한꺼번에 승격하지 않음.|
|메타데이터 유지|H007/H026/H035/H057/H091/H092/H105/H107|판본 선택, 시간 변화, 변장/팬 해석 경계를 설명.|원작·영화 색 혼합, TS로 신체 강제, 한 스틸로 변신 이력 추정이 없음.|

P0도 즉시 무조건 채택하는 목록이 아니다. H062의 성인/보철 guard, H072의 nonhuman owner/effects, H111의 문화적 명칭과 H112의 broad robe 범위는 기존 계약을 먼저 확인한다. H018과 H104의 낡은 표면은 중복 후보를 줄이고 기존 source owner 한 곳으로 수렴시킨다. H105의 visible distress 형태와 실제 제작 과정은 분리한다.

H051의 작은 피부 점은 자연 색소인지 화장인지 원본 픽셀만으로 확정하지 않는다. H075는 선택한 가면의 눈 구멍을 다루며 입 구멍을 모든 부분 가면의 필수 부품으로 만들지 않는다.

## 2. 원본 파일별 배치

아래 이름은 현재 존재하는 원본 파일을 확인한 것이다. 기준 디렉터리는 `/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/`다. 최종 수정 위치는 단순 family 분류보다 **현재 ID가 정의된 실제 source owner**를 우선한다.

|의미 영역|profile 원본|후보 원본|배치 원칙|
|---|---|---|---|
|교복 층·칼라·capelet·tier geometry|photo_prompt_visual_obligations_clothing_structure.json|photo_prompt_clothing_structure_extension.json|garment 표면·여밈·층을 연결. 색·재질·길이는 선택 modifier로 분리.|
|가면·귀걸이·목걸이·안경|photo_prompt_visual_obligations_accessory_structure.json|photo_prompt_accessory_structure_extension.json|head/ear/neck/prop carrier 확인. 기존 안경 profile의 실제 owner가 character_appearance이면 그 source를 보존.|
|머리·국소 얼굴·표식|photo_prompt_visual_obligations_subculture_appearance.json|photo_prompt_subculture_appearance_extension.json|머리 길이/흐름/상태/색 위치를 독립화. 피부·눈·손톱에 hair 경로를 재사용하지 않음.|
|mesh·lace·chiffon·velvet·pleats|photo_prompt_visual_obligations_textile_surface.json|photo_prompt_textile_surface_extension.json|carrier와 weave/open cells/reflection/fold를 분리. 제작 공정은 요청·근거가 있을 때만.|
|보철·몸의 연결|photo_prompt_visual_obligations_body_morphology.json|photo_prompt_body_morphology_extension.json|현재 성인/잔존 사지/소켓 guard 보존. 마법 대체 손은 다른 접합을 검토.|
|팔·시선·소품 접촉|photo_prompt_visual_obligations_pose_vocabulary.json|photo_prompt_pose_vocabulary_extension.json|손–소품, 머리–시선 대상, 인물별 소유를 연결. 현재 다른 작업의 수정과 충돌 검사.|
|비인간 topology·얼굴 세부|photo_prompt_visual_obligations_character_appearance.json 또는 현재 root registry|현재 ID의 tags/research/관련 extension source|이미 있는 정확한 구조를 재사용. hippogriff_eagle_horse_topology는 root registry에 있음.|

`RUNTIME-MAPPING.json`의 `photo_prompt_character_appearance_extension.json`은 **현재 존재하지 않는 후보 파일 이름 제안**이다. 확정 배치가 아니다. 현재 tags의 `hippogriff_eagle_horse_subject`/`hippogriff_turning_eagle_horse_profile` 또는 기존 owner의 확장이 충분하면 그 파일을 사용한다. 별도 중립 extension이 필요하면 schema와 실제 loader 목록까지 함께 검토하고 등록한다. 파일을 만들어 놓기만 하면 자동 로드된다고 가정하지 않는다.

현재 visual profile loader는 `prompt_generator.py`의 `VISUAL_OBLIGATION_EXTENSION_FILENAMES` 목록을 순회한다. root JSON의 임의 `extensions` 키나 폴더의 모든 파일을 로드한다는 전제로 작업하지 않는다. 후보 extension도 실제 로드 경로를 확인한다.

## 3. 연구 명세를 런타임 계약으로 옮기는 방법

연구 JSON의 `harry-potter-research-*/v1`, `source_refs`, `qualification`, `*_proposal` 필드를 활성 asset에 통째로 복사하지 않는다. 출처와 판본 대조는 이 연구 폴더에 유지하고, 기존 런타임 schema에 허용된 필드만 투영한다.

1. **기존 의미 검사**: 현재 definition·activation·concept_candidate·affected effects·authorial guard를 읽고 실제 동일 구조인지 판단한다. `slicked_back_wet`를 dry swept-back으로, `ca_bushy_tail`를 scalp hair로, 교차 흉터를 비교차 각진 이마 선으로 넓히지 않는다.
2. **component 명세**: 각 부품의 observable predicate와 same-owner 연결을 쓰고 `photo-authored-visual-components/v1`으로 옮긴다. `match_terms`, `evidence_field`의 `_phrase` suffix, `evidence_terms`, `min_content_words`, concrete instruction, render gate를 작성한다. 단순 부품 수보다 관계가 중요하다.
3. **hard eligibility**: `photo-visual-hard-activation/v1`의 conjunction을 실제 요청 근거에 맞춰 작성한다. 한국어/영어 carrier와 관계의 긍정 문맥이 필요하며 부정 문맥은 제외한다. 이름 하나, bundle association, agent가 만든 core phrase, BM25F/embedding hit는 요청자 권한을 만들지 않는다.
4. **후보 entry**: 선택형 `concept_units`와 directed `relations`, 정확한 slot, affected_dimensions/properties를 작성한다. 누락된 효과가 있는 profile은 다른 슬롯에 무리하게 끼우지 않고 보류한다. definition override와 요청자의 상세 지정이 기본 사전보다 우선한다.
5. **묶음**: B01–B08은 선택 편의를 위한 제안이다. 선택한 member의 효과만 적용한다. 전체 effect union은 전체 부품을 자동 채택할 권한이 아니다. 교복 묶음은 치마·바지·눈색·연령·몸 비율을 정하지 않는다.
6. **긍정 검색 문장**: 고유명사 없는 affirmative 형태·관계만 corpus에 둔다. source URL, 인물/편수/상품명, research status, 부정 예시, 실패 로그, ID를 embedding text에 섞지 않는다. 오인 예시는 별도 fixture에 둔다.

H002/H058/H077의 [PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)은 실제 compiler 계약을 이용한 3개 형식 예시다. component 3개 → evidence fields 3개·render gates 3개의 투영을 검사한다. 아직 전체 registry validator·owner·activation·runtime effects·pack·이미지에 합격한 profile은 아니다. 특히 prototype의 좁은 alias/hard groups는 최종 activation 설계로 승인된 것이 아니다.

`RUNTIME-MAPPING.json`의 property path는 초안이다. 예를 들어 `body.skin.pigment_dots`, `wardrobe.details.mask.coverage_apertures`를 썼다고 현행 consumer의 지원이 증명된 것은 아니다. 실제 `property_effects_allowed`·parent/child overlap·target resolution으로 검사해야 한다. teeth→eye_detail, nail→face makeup, nonhuman→human body, sky mark→skin mark 대체를 피한다.

## 4. 구현 단계와 제출할 증거

### 단계 A — 새 기준점과 좁은 채택 목록

구현 시작 시 HEAD·dirty paths·원본 해시·active index manifest를 새로 기록한다. 이번 snapshot은 연구 시점의 98개 authored/code 파일과 두 index manifest만 고정한다. 모든 untracked 이미지나 shard 바이트를 저장한 완전한 백업은 아니다.

별도 작업 checkout에서 필요한 authored 변경을 선택적으로 가져오고 어느 원본 hash를 검증하는지 명시한다. 현재 다른 작업을 reset/stash/덮어쓰기하거나 임의로 commit하지 않는다. 활성 index manifest가 참조하는 shard와 검증용 baseline을 보호한다.

제출물: adoption manifest. 각 H 카드에 reuse/modify/sibling/new/context/hold, 최종 source file·stable ID·slot·owner·effects·source-supported facts를 기록한다. 비슷한 뜻은 중복 제거하고 미확정 세부를 별도 유지한다.

### 단계 B — P0/P1 원본 데이터

먼저 학교복 층/지역 배색, 각진 이마 선, 모래시계/고리/chain 연결, 가면 범위/새김, 두 motif 관계를 작은 단위로 반영한다. 현재 넓은 정의를 바꾸는 대신 차이가 실질적인 경우 좁은 sibling을 추가한다. 머리의 젖음/정돈 상태, 피부 점의 자연 기원, 3D tier와 주름, 날개/옷 문양을 혼동하지 않는지 리뷰한다.

제출물: authored diff, source ID 보존 대조, profile compiler/registry-load 결과, candidate effect contract 결과. 신규 수치보다 정확한 연결과 이전 의미 보존을 완료 조건으로 둔다.

### 단계 C — P2/P3와 held cases

teeth/nails/prop/multi-participant/transparent figure의 현재 slot과 target resolution을 확인한다. 연구용 분해만 가능한 항목은 optional inspiration으로 유지하고, full morphology의 의무 profile로 승격하지 않는다. 미확인 사례는 scene/version/부위가 드러나는 1차 자료를 확보한 사실만 승격한다.

공식 요약과 원문 책명이 충돌하는 Firenze 사례, replica의 상충 수치, material appearance만으로 fiber/봉제 공정을 추정하는 항목은 별도 보류표에 남긴다. 구체적인 팬 그림 세 사례의 관찰이 전 세계 여성형 디자인의 표준을 만들지 않는다.

제출물: held-case ledger와 owner/slot decision. 새 런타임 schema나 loader 수정이 필요하면 데이터만으로 해결 가능한 범위를 먼저 반영하고, 남은 구조 변경은 근거와 영향 범위를 따로 리뷰한다.

### 단계 D — derived index와 후보팩

원본을 채택한 뒤 semantic index와 visual profile index를 재생성한다. source hashes·stable IDs·정확한 positive text·provider/model/dimensions가 맞는 cached vectors만 재사용한다. 생성 index의 ours/theirs 선택이나 손수 entry 번호 수정으로 합치지 않는다. 새 manifest 작성 전후 실제 shard 참조/checksum을 확인한다. 이전 generation의 정리는 이번 반영에서 필수 작업이 아니다.

아래는 **구현 시 사용할 명령 예시이며 이번 연구에서 실행하지 않았다**. 작업 checkout 루트에서 실행하고 output 경로와 캐시를 해당 checkout의 채택 원본에 맞춘다.

```sh
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress --keep-stale-generations
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --cache-index skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

visual builder에는 dry-run이 없다. `--check`는 이미 만든 index와 registry의 정합성 검사다. 기존 output/cache의 compatible vector가 없으면 embedding 호출이 필요하며 모델·차원·text가 바뀐 항목을 임의 재사용하지 않는다.

pre-core의 독립 해석 규칙은 유지한다. 비교용 요청/core를 사전 동결한 후 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → obligations/concept candidates/clarification → immutable v6 pack의 실제 순서를 검증한다. bindings가 바뀌면 새 successor artifact를 만들고 기존 baseline pack을 덮어쓰지 않는다. hit, exposed candidate, accepted effect, literal prompt를 각각 기록한다.

제출물: index identity report, baseline/treatment pack JSON과 hash, provenance/slot/owner/effects trace. retrieval 성공만으로 실제 채택이나 원본 픽셀 개선을 주장하지 않는다.

### 단계 E — 회귀와 원본 이미지

회귀는 같은 문장을 반복하는 alias 테스트보다 **부품 누락·부정·다른 소유·advisory origin·locked property·요청자 재정의·판본 충돌**을 중심으로 한다. [REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 1,080건은 120개 카드에서 파생된 명세다. 실행 완료·독립 holdout으로 보고하지 않는다.

현재 존재하는 테스트 모듈을 분야별로 선택하여 변경에 맞는 범위를 실행한다. 다음은 좁은 검증 예시다.

```sh
python3 -m unittest tests.test_photo_uniform_costume_paraphrases tests.test_photo_costume_cosplay_semantics tests.test_photo_character_appearance_100 tests.test_photo_fantasy_visual_semantics
python3 -m unittest tests.test_photo_candidate_semantics tests.test_photo_visual_profile_retrieval tests.test_photo_positive_retrieval tests.test_photo_bm25f_retrieval
python3 -m unittest tests.test_photo_authorial_core_v6 tests.test_photo_core_retrieval tests.test_photo_object_morphology_ownership tests.test_photo_body_morphology_semantics
python3 -m unittest tests.test_photo_semantic_index tests.test_photo_visual_profile_shards
```

새 fixture에는 card의 영어 문장을 그대로 재사용하지 않는 한국어 구어 표현·장면 문맥·복수 owner·미선택 판본을 별도로 작성한다. 이 연구의 작성자가 카드 내용을 본 후 만든 fixture는 blind independent holdout이 아니다. 독립 평가를 주장하려면 별도 검토자가 동결 corpus 밖의 요청을 작성하고 평가 전에 고정한다.

[PIXEL-QUALIFICATION-PLAN.json](PIXEL-QUALIFICATION-PLAN.json)은 20개 그룹의 synthetic scenario·오인 변형·all-of 요소·가시성 조건을 정의한다. source still을 본 기록과 새 생성 이미지 판정을 구분한다. baseline A와 adopted-data B는 같은 고정 요청/core/모델/설정을 사용하고, 제공되지 않는 seed·정확한 deterministic control은 제공되지 않았다고 기록한다. 확률적 결과 1쌍으로 개선 원인을 확정하지 않는다. 품질 개선을 주장할 경우 여러 독립 생성 결과와 실제 n을 함께 보고한다.

선택한 부품과 same-owner 연결을 원본 픽셀에서 모두 확인한다. 썸네일의 인상만으로 미세 새김·눈색·흉터·mesh·손–소품 접촉을 판정하지 않는다. 사용자 framing/pose lock을 몰래 바꿔 가시성을 확보하지 않는다. 필수 부위가 가려지면 `UNOBSERVABLE_NOT_PASS`, 일부 만족은 `FAIL`, 생성 차단/미출력은 `BLOCKED_UNSCORED`다. 기술 판정과 사용자 미감 평가는 별도로 유지한다.

## 5. 완료 보고의 판정표

|증거 층|완료 조건|이번 연구의 상태|
|---|---|---|
|리서치/참조 연결|149 수신 행·120 단위·출처·기존 ID 연결과 미확정 범위 명시|작성 완료; 구조 검증은 VALIDATION.json에 기록|
|활성 원본|실제 schema·component/owner/effects·기존 뜻 보존|NOT_PERFORMED|
|derived index|채택 source identity·cache/shard/checksum 정합성|NOT_PERFORMED|
|후보팩|고정 core에 실제 노출/선택/효과 추적|NOT_PERFORMED|
|프롬프트/런타임|선택한 관계가 literal prompt와 실행 경로에 보존|NOT_PERFORMED|
|원본 생성 이미지|실제 이미지별 all-of 관찰, 차단/가림 분리|NOT_PERFORMED|
|사용자 평가|실제 결과의 미감/목적 적합성 확인|pending|

이번 요청의 완료 범위는 상세 리서치와 구체적인 반영 계획 작성이다. 활성 자산 증가·후보팩 노출·이미지 품질이 이미 개선됐다고 보고하지 않는다.

# 물 시각 의미·후보 데이터 반영 계획

이 계획의 구현·index·후보팩·이미지 단계는 `PROPOSED_NOT_RUN`이다. 이번 작업에서 완료한 것은 345행의 조사 범위 연결, 192개 연구 카드, 117개 후보 초안과 구체적인 채택·평가 명세다. 원본 연구를 활성 runtime schema로 통째로 복사하지 않는다.

## 1. 우선 반영 단위와 순서

|순서|카드|구현 목적|채택 방식|
|---|---|---|---|
|P0-A 물–표면 경계|W004/W006/W007/W014/W019–W028|beading·film·rivulet·meniscus·condensation·bubble·foam·impact를 구분|현재 소재 후보의 정확한 동치만 확장; 다른 carrier·행동은 좁은 sibling|
|P0-B 광학·수면|W046–W056/W152/W190|광원–수면–수광면과 같은 물체의 연속성을 보존|기존 caustic/glitter label 재사용 검토 + 누락된 관계의 원본 profile|
|P0-C 동작·장비·젖음|W144–W162|snorkel·scuba·fin·tewak·피부·머리·천의 owner를 분리|기존 `sw_wet`·`sw_wetsuit`·젖은 헤어 뜻 보존; 수중 헤어·장비 연결은 새 sibling|
|P0-D 물길·해안 topology|W032–W036/W064/W067/W069–W080/W169|충돌·항적·합류·재합류·격리·장벽·이안류 연결|자연환경 source를 먼저 재사용; 서로 다른 geometry는 개별 atom|
|P1 생태·얼음·심해·흔적|W039–W045/W088–W121/W151/W166/W175|holdfast·root·body appendage·ice rim·plume·aftermath를 명시|출처 범위와 종·판본 차이를 고정한 뒤 선택형 후보|
|P2 분해·맥락·추가 근거|45개 family 및 30개 context, 근거 미확인 visual 카드|다른 의미를 aliases로 뭉치거나 비가시적 의미를 shape로 강제하는 오류 방지|family별 atomic 후보 확정; context는 research glossary로 유지; source gap은 추가 조사|

P0는 현재 78개 연구 카드에 지정되어 있으나 일괄 구현 수량 목표가 아니다. 작은 패치마다 owner·effect·회귀 증거가 성립한 카드만 채택한다. P2에서도 물·관능·폭력·공포·의례 용어는 coverage에서 유지하며, 시각적으로 검증할 수 있는 관계와 해석을 분리한다.

## 2. 실제 파일 배치와 유지보수 계약

현행 `prompt_generator.py`의 filename view는 `photo_source_manifest.SourceFiles`를 사용한다. 확장 파일 등록의 단일 원본은 `assets/photo_prompt_source_manifest.json`이다. root registry의 임의 `extensions` 필드나 폴더 전체 스캔, generator 안의 또 다른 filename 목록을 추가하지 않는다. 오래된 연구 계획의 수동 loader 목록과 현행 구조를 혼동하지 않는다.

|반영 영역|기존 원본을 먼저 검토|분리하는 기준|
|---|---|---|
|수면·경계·광학·흐름 원자|`photo_prompt_tags.json`, root `photo_prompt_visual_obligations.json`|기존의 짧은 caustic/glitter/bubble 후보는 실제 의미가 같은 부분만 확장|
|습지·하천·조간대·빙하·생태 배경|`photo_prompt_natural_environment_extension.json`, root visual registry|기존 대상·flow·root·canopy 명세를 중복 작성하지 않음|
|수영복·잠수복|`photo_prompt_swimwear_extension.json`, `photo_prompt_visual_obligations_swimwear.json`|천 물방울·panel·입구를 보존; 방수 성능·체형·투명도를 추가 의미로 강제하지 않음|
|천 밀착·부분 투과|`photo_prompt_textile_surface_extension.json`, `photo_prompt_visual_obligations_textile_surface.json`, root sheer profile|젖음·밀착·비침·아래층 소유·의복 노출 lock을 각각 분리|
|피부·hair·접촉·흔적|tags, tactile reality extension/profile, root wet hair profile|피부/의복/유리의 다른 carrier, 공기/수중의 다른 물리 상태는 별도 후보|
|반영·비 오는 공간·물얼룩|emotional place 및 realistic background extension/profile|기존 reflection owner·wet/dry·runoff 정의를 그대로 재사용할 수 있는지 확인|
|신규 공통 물 구조|제안: `photo_prompt_aquatic_structure_extension.json`, `photo_prompt_visual_obligations_aquatic_structure.json`|기존 owner로 충분하지 않을 때만 신설하고 중앙 manifest에 각각 등록|
|성분·감각·상징·의례·진단·시간적 과정|연구 폴더의 glossary와 seed/card 연결|그 이름만으로 anatomy·pose·노출·재난·sexual tone을 자동 활성화하지 않음|

두 aquatic 파일은 **현재 활성 파일이 아닌 제안 경로**다. runtime slot을 새로 만들 필요는 아직 확인되지 않았다. 기존 슬롯에 들어갈 수 없는 effect가 발견되면 원본의 label을 다른 슬롯으로 억지 이동하지 않고 adoption ledger에서 보류한다.

모든 활성 visual profile source에는 `authored_components`를 쓴다. compiler가 생성하는 `component_semantics`, `required_evidence_fields`, `evidence_requirements`, `render_gates`, `composition_instruction`을 source에 손으로 중복 작성하지 않는다. 현행은 flat V1과 grouped V2를 모두 지원한다. 하나의 관계가 여러 component를 함께 요구하면 V2의 collective obligation을 쓰고, 같은 역할을 여러 evidence field에 과도하게 복제하지 않는다.

[PROFILE-PROTOTYPES.json](PROFILE-PROTOTYPES.json)의 W007/W049/W146/W190은 V1 형식의 투영 예시다. component compiler를 호출해 각 3개 evidence field·3개 gate가 나오는 것만 검증했다. 실제 alias·activation·owner/property·runtime validator·index·이미지에 합격한 profile이 아니다.

## 3. 재사용·확장·sibling 판단

각 카드의 최종 adoption ledger에는 다음 항목을 쓴다: stable source ID, 실제 source file, slot, meaning equivalence, affected dimensions, 실제 target/property path, owner resolution, direct requester activation 근거, 필요한 component/관계, literal prompt evidence, source 범위, 기존 guard 보존, 검증 결과.

`RUNTIME-MAPPING.json`에 연결한 기존 ID는 **검토할 원본의 위치**다. 비슷한 단어가 발견됐다는 이유로 동일 의미라고 승인하지 않는다.

|사례|결정할 내용|
|---|---|
|윤슬 ↔ `sparkling_water_reflection_highlights`|같은 광원–수면 반사 의미인지 확인한 뒤 한국어 paraphrase/키워드 보강|
|ordinary meniscus ↔ `liquid_holding_intent`|후자는 초현실 의미이므로 ordinary meniscus를 그 정의에 끼워 넣지 않음|
|W049 ↔ 기존 caustic labels|빛 모양만 기존 entry가 소유하는지, 수광면·수면 물성 추가가 다른 effect인지 구분|
|W156 ↔ `wet_damp_clumped_hair_state`|동일 물 밖 상태이면 재사용; W157 수중 퍼짐은 sibling|
|피부 물방울 ↔ `sw_wet`|의복에서 피부로의 carrier 전환은 동치 alias가 아님|
|젖은 천 ↔ `sheer_garment_optical_layering`|wetness가 transmission을 의무화하지 않음; 사용자가 비침을 지정한 경우에만 광학 duty 결합|
|수몰 실내/난파 ↔ `ghost_ship_former_vessel_breach`|초현실 breach·former vessel 의미가 없으면 재사용하지 않음|
|해녀 ↔ 일반 diving equipment|작업·부유체–그물주머니·판본 맥락을 따로 매핑하고 실린더를 자동 추가하지 않음|

`existing_slot_context_extensions`는 검토된 동치 paraphrase·context의 보강에만 사용한다. 다른 동작·소재·대상·소유는 새 원자 후보가 필요하다. weight를 크게 올려 관계 결함을 보정하거나 일반 `water` token을 hard route로 쓰지 않는다.

## 4. owner·effects·lock의 구현 기준

현재 117개 draft에는 slot dimension 제안만 있고 실제 affected property는 비워 두었다. 이는 '영향 없음'이 아니라 미매핑 상태다. 구현 시 실제 consumer가 지원하는 target/property를 확인해 완성해야 한다. source 파일을 만들었거나 graph 문자열이 있다고 owner resolution이 작동한다고 가정하지 않는다.

|선택 관계|반드시 구분할 소유·영향|검증할 mutation|
|---|---|---|
|caustic|광원·물 경계·피부/바닥/벽 수광면; lighting와 material geometry 영향|바닥의 무늬를 피부 문신으로 대체, 수면을 제거|
|wet hair|같은 subject의 scalp–strand; 매질·volume·contact|다른 인물의 헤어 변경, air와 underwater duty 혼합|
|cloth transmission|같은 garment patch·섬유·아래층; material opacity·피복 범위|불투명 lock 우회, wardrobe slot에서 surface_material slot으로 옮겨 효과 숨김|
|split shot|한 수면·동일 몸/줄기·수상/수중 view; composition·framing·geometry|상하 콜라주, waterline 두 개, required limb concealment|
|gear|같은 diver의 mouth–hose–cylinder·foot–fin|다른 인물에게 hose endpoint 이전, mouthpiece 분리|
|river topology|same channel·bar·receiving water; setting과 geometry|합류와 분기 교환, 재합류 제거, 지류 endpoint 분리|

효과는 슬롯의 표면 이름이 아니라 실제 target/property로 비교한다. 다른 슬롯으로 옮겨 잠긴 property를 우회할 수 없어야 한다. 의미·identity·pose·의복 opacity·시점이 requester-locked이면 원본을 유지한다. 아직 owner나 property를 소비하는 경로가 없는 카드에는 필수 gate를 약하게 붙여 '일단 활성화'하지 않는다.

hard activation은 직접 긍정 요청에서 해당 carrier와 관계가 정당하게 확인되거나, 정당하게 선택한 opt-in obligation에 의해 생겨야 한다. BM25F/embedding hit, broad water tag, bundle membership, 연구자가 쓴 prose는 새 요청자 의무의 근거가 아니다. 사용자의 재정의·부정·요청 범위가 기본 사전보다 우선한다.

## 5. 구현 단계와 산출물

### A. 최신 기준점과 채택 ledger

구현 시작 시 HEAD, dirty/untracked paths, authored source hashes, source manifest, 현재 semantic/visual manifest와 참조 shard를 다시 기록한다. 이번 `CHECKOUT-SNAPSHOT.json`은 연구 시점의 열거된 live inputs 해시이며 모든 그림·fixture·shard 바이트를 백업한 것은 아니다.

기존 dirty 작업을 reset/stash/덮어쓰지 않는다. 필요한 현재 authored 변경을 가져갈 경우 별도 검증 checkout에서 파일별 SHA를 대조한다. 첫 구현 범위는 P0-A/B 중 약 8–12개 관계 또는 검증 가능한 작은 묶음으로 정하고, 범위는 ledger에 실제 선택 ID로 기록한다.

제출물: 최신 snapshot, adoption ledger, source gaps, reuse/sibling 결정과 보존할 기존 ID 목록.

### B. 좁은 원본 작성과 compiler·effect 검증

동치 paraphrase는 기존 source에 반영하고, ordinary meniscus·crown·Snell window·submerged hair·equipment continuity처럼 의미 차이가 분명한 항목은 좁은 sibling으로 작성한다. 새 파일이 필요하면 두 source 종류를 중앙 manifest에 등록한다. family 45개는 분해 전까지 후보 하나로 활성화하지 않는다.

제출물: authored diff, compiler/registry/manifest validation, owner/property resolution 결과, 기존 의미·guard 대조, explicit opacity/geometry lock mutation 결과. prototype 형식 통과와 실제 registry 합격을 나누어 보고한다.

### C. positive corpus와 derived index

검색 corpus에는 검토된 긍정 label·paraphrase·component·관계만 둔다. URL·source 제목·research status·ID answer list·오인 예시·실패 로그·부정 문장을 embedding text에 넣지 않는다. 맥락 card의 임상·동의·용도·성분·비가시적 뜻을 시각 atom처럼 index에 넣지 않는다.

원본 채택 후 semantic index와 visual profile index를 각각 재생성한다. 동일 entry key·전체 text·provider·model·dimensions가 맞는 cached vector만 재사용한다. registry hash만 바뀐 경우에도 필요한 manifest 정합성을 새로 확인한다. BM25F는 같은 authored source의 파생 표현이며 별도 뜻 저장소가 아니다. 생성된 index의 ours/theirs 선택이나 array position 수동 수정으로 합치지 않는다.

다음 명령은 **향후 구현 예시이며 이번 연구에서 실행하지 않았다**. 실제 checkout의 help·cache 경로·vector 설정을 다시 확인하고 적용한다.

```sh
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
python3 skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress --keep-stale-generations
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --cache-index skills/photo-prompt-image-generator/assets/photo_prompt_visual_profile_index.json --batch-size 1
python3 skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

visual builder의 `--check`는 이미 생성된 index와 원본의 정합성 검사다. 새 text는 embedding이 필요하며 다른 vector space나 text의 cache를 재사용하지 않는다. 이번 구현의 필수 범위에 오래된 generation 삭제를 넣지 않는다.

제출물: source/index hashes, exact compatible-vector reuse 근거, shard 참조·checksum 검증, BM25F 갱신과 language/negation 회귀 결과.

### D. 동결 core → 실제 후보팩 → 선택 효과

연구 카드·원본·평가 답안을 보지 않은 평가 컨텍스트에서 실제 요청을 해석하고 core를 동결한다. pre-core feature catalog와 controls의 기존 예외 범위는 유지하며 이 리서치 폴더를 pre-core 사전으로 쓰지 않는다.

실제 흐름은 `retrieve_core_slots` → `candidate_pack_resolve_visual_profiles` → obligations/concept candidates/clarification → immutable V6 pack이다. 다음 항목을 각각 기록한다: 어떤 원본의 후보가 노출됐는지, 무엇을 선택했는지, 어떤 effect가 허용·차단됐는지, 최종 literal prompt가 해당 carrier와 관계를 어떻게 보존하는지. pack을 후편집하지 않고 변경이 있으면 successor artifact를 만든다.

W049를 검색할 수 있었다는 사실만으로 물 바닥의 관계가 채택된 것이 아니며, W162가 노출됐다는 사실만으로 불투명 옷의 lock을 바꾸어도 된다는 뜻이 아니다. 공개 pack에는 점수·랭킹·vector·matched answer keys를 새로 노출하지 않는다.

제출물: 고정 요청/core/pack hashes, source ID별 exposure·selection·effect trace, literal evidence·owner 검증, composition/runtime audit.

### E. 회귀와 원본 픽셀 비교

16개 [회귀 그룹](REGRESSION-PLAN.json)은 카드 문장을 그대로 반복하는 alias test보다 부품 누락·다른 소유·부정·locked property·요청자 재정의·advisory origin·가림을 검증한다. 연구자가 카드를 본 뒤 작성한 예시는 blind independent holdout으로 보고하지 않는다. 별도 평가 컨텍스트에서 한국어 구어 요청·고유명 없는 장면·복수 owner·다른 표면의 같은 빛 모양을 작성하고 평가 전에 고정한다.

기존 테스트는 실제 변경 영역에 맞춰 선택한다. 새 manifest/profile/candidate 전체 변경이 넓은 영역에 걸치면 dictionary와 관련 full discovery로 넓히되, 이미 통과한 검증을 이유 없이 반복하지 않는다. 일부 suite가 historical fixture 문제로 실패하면 source hash와 fixture 상태를 먼저 대조하고 의미 기준을 약화하지 않는다.

```sh
python3 -m unittest tests.test_photo_candidate_semantics tests.test_photo_visual_profile_retrieval tests.test_photo_positive_retrieval
python3 -m unittest tests.test_photo_natural_environment_semantics tests.test_photo_tactile_reality_semantics tests.test_photo_swimwear_semantics tests.test_photo_textile_opacity_effect_scope
python3 -m unittest tests.test_photo_object_morphology_ownership tests.test_photo_core_retrieval tests.test_photo_authorial_core_v6 tests.test_photo_prepack_isolation
python3 -m unittest tests.test_photo_structure_maintenance tests.test_photo_semantic_index
```

이미지 비교에서는 A=기존 채택 원본, B=새 채택 원본을 같은 요청 의미·모델·제공되는 설정으로 비교한다. 지원되지 않는 seed 제어나 결정성을 있다고 보고하지 않는다. 한 쌍의 확률적 생성으로 데이터 개선의 원인을 단정하지 않고 실제 시도 수와 선택·프롬프트 차이를 함께 기록한다.

각 [픽셀 그룹](PIXEL-QUALIFICATION-PLAN.json)의 component와 directed relation을 원본 해상도에서 모두 확인한다. 작은 방울·cloth weave·gear endpoint·ice rim을 썸네일 인상으로 판정하지 않는다. 사용자의 framing·pose lock을 바꾸어 어려운 endpoint를 숨기지 않는다. 부분 만족은 `FAIL_PARTIAL_IS_FAIL`, 요구 부위가 가려진 경우 `UNOBSERVABLE_NOT_PASS`, 출력 없음은 `BLOCKED_UNSCORED`다. 모든 hard duty가 보이는 기술 PASS와 사용자 미감 평가는 별도로 보고한다.

제출물: 원본 이미지·각 시도 ledger, literal prompt와 선택한 효과, same-owner all-of 판정, 장면별 defect, 비교 조건과 실제 n, 사용자 평가 상태.

## 6. 완료 조건과 단계별 증거

|증거 층|완료 조건|이번 요청의 상태|
|---|---|---|
|연구 범위|345 seed 연결·192 카드·오인 경계·근거 범위·미확정 항목|작성; 구조 검증은 VALIDATION.json 확인|
|원본 데이터|실제 schema·등록·owner/property·기존 뜻·guard 보존|NOT_PERFORMED|
|index|채택 source identity·text/vector·manifest/shard 정합성|NOT_PERFORMED|
|후보팩|동결 core에 실제 target 후보 노출·선택·허용 효과|NOT_PERFORMED|
|프롬프트·runtime|literal 관계·lock·owner와 실행 경로 보존|NOT_PERFORMED|
|원본 픽셀|필수 component·같은 owner 관계 all-of 확인|NOT_PERFORMED|
|사용자 평가|실제 사진의 미감·목적 적합성 판단|pending|

완료 보고는 이 표를 유지한다. 연구 패키지 PASS를 활성 데이터 증가·후보팩 개선·이미지 성공으로 표현하지 않는다. source gap·property 미매핑·가림은 별도 ledger에 남겨 다음 구현에서 검토 가능한 상태로 유지한다.

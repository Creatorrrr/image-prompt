# 시각 의미·후보 데이터 반영 계획

상태: **PLANNED_NOT_IMPLEMENTED**. 연구 산출물은 활성 schema가 아니다. 이 계획의 목적은 장식의 실제 구조·owner·범위가 요청별 후보팩에 도달하고, 채택된 의미가 최종 이미지까지 유지되는 것이다.

## 완료 조건

1. 선택한 authored 원자의 의미·관계·source·실제 dimension/target/property가 정확하며 중복/참조 오류가 없다.
2. broad style과 좁은 selected variant, 제작 사실과 가시 대리조건, 원본 source와 연구자 제안을 구분한다.
3. 문맥·소유·잠금상 eligible한 후보의 stable ID가 실제 v6 pack에 노출된다. 필요한 hard 의미와 optional 분모를 분리한다.
4. 선택한 후보의 전체 effects가 core와 호환되며 required 관계가 final prompt와 실제 runtime argument에 남는다.
5. 원본 픽셀에서 bound required 관계가 모두 확인된다. 가림·너무 작은 구조·부분 충족은 통과하지 않는다.
6. 사용자 수용은 별도 상태로 기록한다. 구조 검증이나 좋은 분위기를 완성된 사용자 수용으로 보고하지 않는다.

## P0. 시작점·owner·중복을 확정

입력: [CHECKOUT-SNAPSHOT.json](CHECKOUT-SNAPSHOT.json), [AUTHORING-INVENTORY.json](AUTHORING-INVENTORY.json), [ADOPTION-MAP.json](ADOPTION-MAP.json).

- 구현 시 현재 HEAD, 등록된 authored 파일, 해시, 생성 인덱스의 source binding을 다시 확인한다. shared checkout의 다른 작업은 보존한다. 필요하면 분리된 worktree에서 구현한다.
- 144개 단위의 `reuse / extend-existing / new-visible-atom / optional-family / context-only / defer` 결정을 실제 owner 단위로 확정한다. 71개 초안을 같은 수의 새 ID로 복사하지 않는다.
- 재사용 후보 16개 `(file,slot,id)`와 프로파일 identity 3개를 실제 본문/guard/effects까지 대조한다. 배열 위치를 선택 근거로 쓰지 않는다.
- 기존 `profiles`와 dictionary의 `visual_semantics`를 함께 조사한다. 지금의 정확 라벨 일치 14건이나 raw profile 라벨 일치 0건을 데이터 갭의 수로 해석하지 않는다.
- 특히 `sff_pro_j06`과 `sff_relation_pro_r31`의 열린 선재 의미를 보존하면서 바탕판형 필리그리를 분리한다. 단독 물체의 장식을 wearable `main_subject` target으로 바인딩하지 않는다.

**종료:** 각 채택 단위에 현재 source 파일·stable ID·owner·shape·전체 effects·선택형 관계·원천 근거가 연결되어 있다. 문맥/시대/공정에 근거가 부족한 항목은 보류 이유가 기록된다.

## P1. 먼저 재료와 부착 구조를 보강

첫 묶음은 **필리그리 열린/바탕판형, 그래뉼레이션/음각, 클루아조네/샹르베, 직조/망/브리지/안감, 코우칭, 코르셋 여밈**이다. native 파일럿의 핵심 실패를 작은 원자로 검사할 수 있다.

| 범위 | 우선 후보 초안 | 현재 source/owner 접근 | 필요한 의미 보강 |
|---|---|---|---|
| 주얼리 선재/입자/색칸 | GD13–GD24 | accessory structure + 기존 `sff_pro_j06/j07` 의미 검토 | wire/plate/grain/partition, 열린/바탕판 분기, bound owner |
| 중립 물체의 세공 | GD07–GD10, GD16–GD28, GD71 | 기존 prop/object owner 우선 | wearable 의미 재사용과 object target의 분리 |
| 직물 표면 | GD29–GD37 | textile surface + historical womenswear 재사용 | motif/ground/sheens, net/bridge/lining, laid-thread/tie-stitch |
| 트리밍/레이어/여밈 | GD38–GD42 | textile surface, clothing structure, accessory structure | attachment edge, layer order, panel/eyelet/lace continuity |

명시된 구조가 같은 owner에 속해야 한다. positive definition·components에는 가시 의미를 적고, 실제 제작법·진위·숨은 구조의 한계는 `claim_limits`, 다른 형태와의 차이는 contrast/reject 필드에 둔다. semantic positive retrieval text에 경고·타 후보의 부정·ID를 반복하여 검색을 유도하지 않는다.

`filigree` 일반 라벨 하나에 관통 구멍을 required로 넣지 않는다. `open-backed wire filigree`처럼 명확한 선택형만 정확한 구멍 의무를 가진다. 보빈/니들·르푸세/체이싱·에칭/선각은 제작 의미와 가시 변형을 분리한다.

**종료:** 원자의 연결·바탕·가림 경계가 표현되고 R20/R21/R24/R28/R29/R30/R34 같은 대조 사례의 의미와 owner가 보존된다. 활성화 전 현재 schema의 effects 검증을 통과한다.

## P2. 모티프·건축·밀도 관계를 보강

- 모티프: 잎/줄기/스크롤, 넓은 교차 띠, 로카유 프레임, 중앙 필드, 로제트, 장식 그로테스크의 부분과 연결을 재사용한다. GD05–GD12/GD53/GD54/GD70.
- 건축: plate/bar, ogee, 세/네 로브, fan ribs, finial, muqarnas, flame-like tracery를 별도 변형으로 등록한다. GD43–GD52/GD69. `pf_muqarnas`의 셀·층·전이 의무를 보존한다.
- 밀도: GD01–GD04의 effect를 장식 대상 경계와 scale hierarchy로 바인딩한다. 전체 프레임과 국소 표면의 범위를 분리한다.
- 형상 전이: GD51은 건축 모티프를 작은 목 장식으로 옮기는 명시 저작 변형이다. 그 목 장식의 프레임·부착을 별도로 검토한다.
- 가고일의 물길/출구, 실제 역사적 이름, 문자 내용, 기계 작동은 픽셀 형태와 다른 증거를 요구한다. 근거 없이 하드 프로파일을 넓히지 않는다.

**종료:** R10–R19/R23/R36의 구조 구별이 유지되고, 밀도가 주변 대상·피부·배경으로 번지지 않는다. required contour가 가려지면 의미/픽셀 상태를 미통과로 기록한다.

## P3. broad style·성인/허구·조합을 연결

Gothic Maximalism은 고딕 구조/모티프와 밀도/계층 선택을 결합한다. Gothic Baroque는 요청된 고딕 부재와 바로크의 볼륨/흐름을 구별하여 결합한다. Ornate Gothic은 장식 부착과 고딕 형태를 관계짓는다. 이 합성어들을 고정한 시대·의상·소품·색의 bundle로 등록하지 않는다.

[BUNDLE-DRAFTS.json](BUNDLE-DRAFTS.json)의 12개는 **선택 구조**다. 열린/바탕판 필리그리, plate/bar tracery, 세/네 로브, 서로 다른 에나멜 기법은 대안이며 한 번에 모두 required로 만들지 않는다. 반대로 채택한 구체 layer sequence나 lacing relation은 필요한 모든 관계를 함께 보존한다.

상복/메멘토 모리/바니타스/성유물함, 성인 fetish/bondage-inspired/erotic macabre, 장식 그로테스크/body horror/gore, greeble/kitbash/biomechanical을 별도 semantic/context 축으로 유지한다. 피부 노출·실제 구속·성행위·죽음 사건·신체 손상 강도·작동을 스타일 명칭에서 추가하지 않는다. 요청된 성인·허구 문맥은 의미에서 지우지 않고 기존 context guards와 bound event/owner로 처리한다.

좁은 형태 채택을 보류한 8개 항목은 추리게레스코의 부위별 패턴, 빈 분리파 세부형, 산업/사이버고스, 벌레스크의 공연별 복식, queer maximalism 명칭 범위, 에로구로/근대 문화의 세부 연출이다. 더 구체적인 작품·제작자·공연·연대 근거와 도판 대조 후 확장한다. 표현을 삭제하는 보류가 아니라 **현재 근거 이상의 고정 외형을 만들지 않는 결정**이다.

**종료:** 일반 고딕과 현대 goth, 패션 명칭과 연령/성적 의미, 상징과 event, 착용 소품과 허구 몸의 변형이 서로 다른 단위로 남는다. 조합의 전체 effects와 배타 선택을 검증한다.

## P4. 현재 schema 변환·등록·인덱스·회귀

연구의 `predicate_description_en`, `target_binding`, `proposed_property_area`를 그대로 runtime schema로 복사하지 않는다. 현재 계약에 맞는 `concept_units`, 관계의 `id/type/subject/object`, 실제 `affected_dimensions`와 `affected_properties`로 변환한다. 여기에 필요한 target/property가 현재 generic 계약에서 표현되지 않으면 범용 계약의 표현력과 호환성을 별도로 검토한다.

검증 경로는 현재 `photo_candidate_semantics.py`, `photo_contracts.py`, `visual_profile_contracts.py`와 dictionary/registry validators다. 새 source 파일이 정말 필요한 경우에만 `prompt_generator.py`의 extension manifests에 등록한다. 후보팩 구성·검색에 주제 전용 regex, synonym router, 새 의미 저장소를 추가하지 않는다.

검토를 마친 authored source에서 `build_semantic_index.py`와 `build_visual_profile_index.py`를 실행해 파생 데이터를 재생성한다. 양쪽 authored 변경을 identity로 보존한다. 벡터 재사용은 text/provider/model/dimensions/hash가 일치하는 캐시만 사용하며, 새 텍스트를 옛 벡터로 가장하지 않는다. 기존 immutable regression proof를 재해싱해 합격으로 바꾸지 않는다. 실제 데이터/pack 변경에 맞는 successor proof를 만든다.

회귀 범위:

1. [REGRESSION-PLAN.json](REGRESSION-PLAN.json)의 92개 자연어/잠금/control probe를 실제 cases로 변환한다. candidate lead는 노출 보장이나 선택 의무가 아니다.
2. 선택형 exact/context-valid hard 의미, BM25F/embedding advisory 의미, requester definition, 부정/인용 문맥을 구분한다.
3. 완전한 effects가 잠금과 호환되는 eligible 후보의 실제 노출을 stable ID로 측정한다. missing expected hard coverage는 렌더 전에 처리한다.
4. 합성 후보가 재료·색·의상 실루엣·body geometry·배경·event·camera를 부당하게 바꾸지 않는지 검사한다.
5. 주변 원자·기존 owner의 관련 회귀, stale index/registry binding 검사를 완료한다. 변경/실패/남은 우려가 없으면 불필요하게 같은 검사를 반복하지 않는다.

**종료:** 데이터 validator와 관련 회귀가 통과하고, eligible 노출·선택 또는 정당한 optional 거절·전체 효과 보존·프롬프트 바인딩이 요청별 artifacts로 확인된다. 이 단계는 이미지 합격을 의미하지 않는다.

## P5. 원본 픽셀 파일럿과 확장

첫 파일럿: H01/H02/H05/H06/H08/H09/H13/H14 × 전/후 2개 arm × 독립 3회 = **48개 이미지**. 동일한 core·provider/model·size/quality·composition protocol을 유지하고 authored/index 증분만 바꾼다. 생성 도구가 seed를 제공하지 않으면 독립 반복이다.

연구자가 쓴 시나리오는 실제 사용자의 요청 원문이 아니다. 실행 시 실제 요청 envelope와 명시적으로 채택한 fixture의 경로/해시·저작 provenance를 구분해 보존한다. agent 작성 fixture를 `requesting_user`의 byte-exact 메시지로 재라벨링하지 않는다. 이미지 skill을 실행할 때는 독립 baseline/core가 동결되기 전 assets·index·pack·이전 render를 읽지 않는 현재 경계를 지킨다. 이번 연구 문서를 읽은 agent의 평가 계획을 독립 pre-core 생성의 증거로 쓰지 않는다.

각 arm에 보존할 것: 실제 요청/fixture provenance, core와 잠금 해시, authored/index 해시, full immutable pack, eligible/노출 ID, 선택/거절 이유, 전체 effects, literal required phrase map, final prompt, 실제 도구 인자, 원본 이미지, native review crop, gate별 판정.

| 보고층 | 분모와 증거 | 완료 판단 |
|---|---|---|
| 데이터 | 채택 단위와 의미/owner/effect 계약 | 누락·중복·dangling reference 없음 |
| 노출 | 문맥·owner·전체 locks상 eligible한 후보 | actual stable ID 존재; required/advisory 분리 |
| 채택 | 노출된 후보와 composer 판단 | 필요한 관계 선택 또는 정당한 optional 거절 |
| 의미 보존 | core + final prompt + 실제 runtime 인자 | 대상·관계·재료·노출·event·구도 바인딩 유지 |
| 픽셀 | bound required native all-of gates | 모든 관계가 같은 owner에서 판정 가능 |
| 수용 | 사용자 검토 | 별도 확인 상태 |

partial required coverage는 실패다. required 관계가 가림·크롭·너무 작은 스케일 때문에 판정 불가하면 `UNOBSERVABLE_NOT_PASS`. 생성 차단/도구 미가용은 `BLOCKED_UNSCORED`. target 후보가 노출·선택·프롬프트에 도달하지 않았다면 픽셀 변화로 데이터의 인과 개선을 주장하지 않는다.

첫 구조가 안정된 후 H03/H04/H07/H10–H12/H15–H22로 세공·역사·성인·허구·매체 범위를 넓힌다. 강한 시대/기법/진위/실제 기능 주장에는 그 주장을 검증할 별도 근거가 있어야 한다.

## 이번 요청의 실제 완료 범위

조사, authored 인벤토리, 용어별 의미/형태/한계, 후보·조합 초안, 반영 결정, 구현 단계, 의미/픽셀 검증 계획, 패키지 구조 검증을 제공한다. 활성 assets·index·generator·tests는 이 연구 작업으로 채택하지 않았다. 커밋·푸시·PR·이미지 생성도 실행하지 않았다. 구현을 시작하기 전에 snapshot의 현재성을 다시 확인한다.

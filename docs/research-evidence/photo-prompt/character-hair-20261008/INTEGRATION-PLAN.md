# 헤어 시각 의미·후보팩 반영 계획

기준일: 2026-10-08 Asia/Seoul. 현재 상태: **조사·설계 완료를 위한 반영안**. 아래 단계의 런타임 구현·인덱스 발행·이미지 검증은 이번 작업에서 실행하지 않는다.

## 목표와 완료 경계

원본 H001–H454가 필요한 모발 소유자, 부위, 형태, 배치, 접합, 상태를 설명하는 데 쓰이고, 후보팩이 그 의미를 유지하는 선택지를 제공하도록 강화한다. 성공은 단어 수가 아니라 중요한 차이를 보존하는 정의·관계, 올바른 후보 대응, 회귀 방지, 관찰 가능한 출력으로 판정한다.

이번 연구의 완료 조건은 입력 전사와 provenance, 전체 용어의 처리 방향, 출처와 한계를 갖춘 핵심 의미 카드, 현행 데이터의 재사용 경로, 후보·프로필 초안, 검증 계획을 저장하는 것이다. 다음 구현 작업의 완료 조건은 별도로 source/schema/compiled index/실제 조회/선택 결과를 검증하는 것이다. 생성 이미지 품질과 사용자 수용은 이후 별도 증거다.

## 실행 원칙

- 사용자에게 필요한 결과를 끝내고, 조사·설계·구현·노출·선택·픽셀의 완료 상태를 구분한다.
- 원본 이름을 보존하고 출처를 붙인다. 구조나 언어 표기가 겹치면 증거로 범위를 좁히며, 유사 검색 결과만으로 의미를 고정하지 않는다.
- 기존 ID·관계·동결 요청·maintenance 이력을 우선 확인한다. 같은 의미를 중복 신설하거나 기존 뜻을 조용히 바꾸지 않는다.
- 프로필과 슬롯 후보를 용도별로 유지한다. 데이터는 작성자의 의미를 보조하고 선택된 의미를 실현한다.
- 실패·접근 불가·가림·보류를 성공으로 보고하지 않는다. 다른 좋은 요소로 필수 관계 실패를 상쇄하지 않는다.
- 기존 dirty/untracked 작업을 보존한다. 실제 구현 시작 시 별도 작업 영역의 시작 상태와 병합 대상 source를 다시 확정한다.

Research 계약: 주요 경계에는 교육기관·저자·살롱·제조사·문화기관·플랫폼의 직접 자료를 쓴다. 지역적 용례, API 정의, 검색에 남은 과거 본문을 분리한다. 카드의 최소 서명과 게이트는 자료에서 도출한 설계로 표기한다.

Retrieval 계약: 독립적인 작성자 core를 먼저 동결한다. 이후 exact/BM25F/embedding은 의미·후보 발견을 보조한다. generic 이름이나 embedding score가 새 의무를 만들지 않는다. 정확하고 요청 문맥에 맞는 의미는 해당 요청 계약으로 다루고, local-data의 broad alias로 hard 의무를 확대하지 않는다.

Experiment 계약: 독립적으로 작성한 holdout 입력, 혼동 대조, 공존 사례, 소유자·잠금 사례를 이용한다. 인덱스가 만들어졌다는 사실을 검색 개선이나 픽셀 구현으로 바꾸지 않는다.

Persistence 계약: authored source와 외부 maintenance 레코드가 권위다. derived 인덱스를 직접 편집하지 않는다. 새 record와 successor/hash를 남겨 기존 run의 봉인된 자료와 재생을 보존한다.

## P0 — 먼저 바로잡을 의미 경계

| 대상 | 현행 관찰·문제 | 변경 제안 | 완료 판정 |
|---|---|---|---|
| `wet_damp_clumped_hair_state` | `wet-look hair` alias에 실제 수분·뭉침·무게 증거가 연결됨 | H368 연출 표면 / H369 실제 수분 상태 분리. 실제 젖음의 비부착 처짐 대안 유지. 물속 부유는 별도 환경 | dry-gel wet look이 water/rain/contact를 강제하지 않고, 실제 rain-damp 요청에는 해당 증거가 남음 |
| 발레아주 | 방법 이름이 darker roots/불규칙 ribbon/옴브레 배제라는 대표 외형에 연결됨 | 방법·뿌리·길이 경사·가닥 폭·경계 전이를 분리. 현행 ribbon형은 좁은 실현안으로 보존 | balayage와 ombré를 공존 가능하게 표현하고, 명시된 ribbon형 요청은 기존 duty 유지 |
| `Hair bow` / `Hair scarf` | 모발 재료와 천 재료의 이름 충돌 | H204/H387, H397/H447의 owner/material/origin/attachment 분리 | 천 보우·스카프가 모발 자체 형태의 evidence로 통과하지 않음 |
| `Graduation`, `Level`, `Ombre`, `color blocking` | 행사·공간·전역 색과 다른 sense의 exact surface가 존재 | hair-cut / hair-color 소유자 문맥과 관계로 분리 | 잘못된 slot이나 전역 그레이딩이 헤어 요청의 증거가 되지 않음 |
| pigtails, box/knotless, A-line/stacked | 용례가 중첩되는 이름을 배타 클래스로 만들 위험 | 묶음 수와 weave, partition과 root form, perimeter와 stacking을 독립 축으로 저장 | 공존 사례를 통과하고, 숨은 시술 원인을 확정하지 않음 |
| fine / density / volume | 개별 직경·뿌리 분포·외곽 부피가 혼용될 위험 | 각각의 측정·외형과 관찰 제한을 기록 | 일반 인물사진으로 actual diameter/count/임상 진단을 했다고 보고하지 않음 |

wet-hair 수정 범위에는 base 프로필 외에 Y2K `y2kr_wet_hair`, water `water_w156/157`, horror `hr_wet_hair_skin_contact`와 실제 source의 관련 프로필을 함께 대조한다. 단, horror의 **명시적 skin-contact 변형**처럼 좁은 의미의 의무는 유지한다. 모든 젖음에 접촉을 강제하거나, 접촉 변형의 접촉을 없애는 일괄 정규화는 하지 않는다.

P0 alias 수정 전에는 exact activation의 코드 경로, 기존 독립 입력, archived pack의 source receipt와 historical replay를 조사한다. 이 보고서의 static finding은 live activation 재현 완료를 뜻하지 않는다.

## P1 — 의미 카드와 기존 항목의 대응 확정

1. `RESEARCH-CROSSWALK.json`의 전체 454행을 검토한다. source-grounded card, 공통 축으로의 확장, 추가 직접 자료가 필요한 hold, 비시각 문맥을 구분한다. 한 행에 여러 카드, 여러 행에 같은 카드 연결을 허용한다.
2. base뿐 아니라 manifest의 모든 candidate/profile source를 읽어 구조가 맞는 기존 ID를 찾는다. `KEYWORD-CROSSWALK.json`의 문자열 대조는 시작점이며 absence/동등성 판정이 아니다.
3. 기존 이름만 있는 항목은 가능한 구조·owner·effects를 보강한다. 이미 구조가 풍부한 Y2K/subculture/character-appearance 항목은 재사용한다. 같은 부위의 의미가 다르면 별도 변형을 제안한다.
4. 자연색·펌·염료 지속성·설치법은 결과 외형과 분리한다. 69개 색명·색 배치 입력은 공통 hue/lightness/saturation/temperature와 region/boundary grammar를 재사용한다. 이름마다 universal RGB나 브랜드 level을 만들지 않는다.
5. H115의 `Gail-style parted hair`는 전사본에 그대로 둔다. 별도 검색 표기는 근거와 보류 상태를 붙인다. H432처럼 관심·주제에만 해당하는 말에는 모발 hard profile을 만들지 않는다.

우선순위는 커트의 부위별 길이·연결, 앞머리의 coverage/edge/length, 밑동 수·높이, scalp/free braid 경로, 색 면·겉/안층·뿌리/끝이다. 그 다음 장식 접합과 문화적 형태, 판타지 재료·효과를 확장한다. 출처 부족을 인기·유사도·자료량으로 대체하지 않는다.

## P2 — source authoring과 후보·프로필·번들 작성

제안 신규 파일은 `skills/photo-prompt-image-generator/assets/photo_prompt_character_hair_extension.json` 및 `photo_prompt_visual_obligations_character_hair.json`이다. 실제 적용 시 중복되지 않는 manifest의 다음 kind별 load order에 등록한다. 하드코딩 파일 목록을 하나 더 만들지 않는다. 기존 의미 수정은 해당 기존 owner source와 successor maintenance에서 수행하며 새 파일에 같은 ID를 덮어 넣지 않는다.

| 층 | 작성할 것 | 제외하거나 따로 둘 것 |
|---|---|---|
| 의미 카드/maintenance | H ID, 출처 URL·읽은 상태·지지 범위, region, minimum signature, 혼동 경계, 아직 미검증인 항목 | runtime에 임의 provenance/namespace/status 키를 주입하지 않음 |
| 슬롯 후보 | 긍정 문구, `concept_units`, 방향을 가진 `relations`, `affected_dimensions`, `affected_properties` | 성격·나이·성별·민족성·우연히 함께 나온 색·원인·의상 등을 헤어의 기본값으로 복사하지 않음 |
| 시각 프로필 | 명시적으로 선택된 의미의 구성요소, 의무, evidence와 render gate | 모든 이름에 프로필을 강제하거나, 모든 프로필을 관례적인 5그룹으로 부풀리지 않음 |
| 번들 | 동일 owner/region의 후보·프로필 대응, 공간적 연결, ambiguity 조건 | 여러 style/color/accessory가 함께 있다는 이유만으로 필수 조합 만들지 않음 |

`CANDIDATE-DRAFTS.json`은 런타임에 넣기 전의 review wrapper다. wrapper에 있는 연구 키를 runtime source로 그대로 복사하지 않는다. 신규 ID는 provisional이며 기존 slot/ID와 semantic equivalence를 최종 확인한다. 재사용 ID에는 alias-only enrichment와 의미 수정의 경계를 따로 기록한다.

현행 후보 관계는 `{id,type,subject,object}`이고 속성 효과는 `{dimension,target,property}`다. `dimension: appearance`, `target: main_subject`를 기본 헤어 소유자로 사용한다. `hair`/`hair.color` 같은 부모 lock, 기존 넓은 property와의 교차를 검사한다. 조명·material 차원으로 효과 이름을 옮겨 같은 모발 lock을 우회하지 않는다. 세부 property명은 현재 호출부와 실제 잠금 계약에 맞춰 검토한다.

`canonical_concept_id`는 같은 slot의 존재하는 항목에만 연결하고 cycle을 금지한다. `existing_slot_context_extensions`는 기존 항목의 `paraphrases/contexts` 보강에만 쓴다. 효과·의미·기존 제한의 수정 통로로 사용하지 않는다. `contexts`는 긍정 검색 prototype과 구분한다.

profile source는 `authored_components` v1/v2를 사용한다. generated `component_semantics`, `required_evidence_fields`, `evidence_requirements`, `render_gates`, `composition_instruction`을 authored source에 중복 작성하지 않는다. v2 collective obligation은 여러 component/evidence를 묶을 수 있고 활성화된 duty는 discovery score 때문에 줄어들지 않는다. `PROFILE-AND-BUNDLE-PLAN.json`의 gate 설명은 설계이며 실제 profile schema serialization은 이 계약에 맞춰 작성한다.

`maintenance_ref`는 `photo-extension-maintenance-ref/v1`의 record ID와 sha256로 연결한다. 실제 구현 완료 후 canonical source body hash를 계산하여 외부 record와 successor를 작성한다. 연구 시점의 raw hash를 미래 구현 hash로 재사용하지 않는다.

## P3 — manifest·인덱스·발행

변경 대상 authored source와 maintenance record가 확정된 뒤 검증한다. 그 다음 후보용 semantic text/BM25F/index와 profile index를 각각 재생성한다. 후보 검색과 의미 검색을 일대일 합병하지 않는다.

현행 스크립트의 점검 가능한 경로는 다음과 같다. 아래는 **실행 계획**이며 이번 연구에서 빌드하지 않았다. 실제 구현 전에 `--help`와 현재 runtime publisher 계약을 재확인한다.

```text
validate_photo_prompt_dictionary.py --tags <tags> --no-runtime-publication
build_semantic_index.py --tags <tags> --output <candidate-index> --dry-run --no-runtime-publication
build_semantic_index.py --tags <tags> --output <candidate-index> --provider <provider> --model <model> --dimensions <n> --no-runtime-publication
build_visual_profile_index.py --registry <base-registry> --output <profile-index> --cache-index <compatible-index> --no-runtime-publication
build_visual_profile_index.py --registry <base-registry> --output <profile-index> --check --no-runtime-publication
publish_photo_runtime_snapshot.py --source-root <skill-root> --runtime-store <isolated-runtime-store>
```

실제 filename/argument와 publication 순서는 해당 시점의 CLI가 권위다. publisher의 --complete-update는 중단된 maintenance update의 명시적 복구 옵션이므로 일반 검증 성공을 만들기 위해 임의 사용하지 않는다. profile index의 `--synthetic-sources`는 조사 검증 도구에 한정하고 production authored 의미의 대체물로 사용하지 않는다. candidate cache는 기존 output의 exact semantic text에 대해 동작하고 `--no-cache`는 사용하지 않는 선택이다. 존재하지 않는 `--reuse` 옵션을 가정하지 않는다.

벡터 재사용 조건은 text/provider/model/dimensions가 모두 동일한 것이다. 달라진 정의나 relation은 새 text에 해당하므로 다시 만든다. API 작업량과 비용은 dry-run 결과 뒤 계산한다. 이 계획은 API 호출이나 유료 embedding 승인을 이미 받은 것으로 해석하지 않는다.

source update가 pending인 동안 freshness가 fail-closed 동작하는지 확인한다. 새 source와 오래된 compiled index를 섞은 검증 성공을 발표하지 않는다. 현재 16 shard와 후보 노출 cap(core slot 4/support 2, total 64)을 자료 수 때문에 자동 확대하지 않는다. alias만 늘리면 같은 slot의 다른 의미가 밀릴 수 있으므로 실제 노출의 다양성과 정확도를 측정한다.

## P4 — 데이터·조회·선택 회귀 검증

| 검증 층 | 입력·사례 | 통과 기준 |
|---|---|---|
| source integrity | unique slot/ID, canonical cycle, manifest kind/order, source hash, schema/effect keys, relation endpoints | 중복·누락·계약 위반 없음; 현재 dirty 작업 보존 |
| 이름·scope | 한/영 표기, H022 분리, H204/H387와 H397/H447, graduation/level의 다른 sense | owner가 맞는 의미만 exact 대상으로 채택; broad ambiguous alias는 확대하지 않음 |
| 부정·공존 | no-bangs, no-braid, A-line+stacked, box+knotless, full+blunt+micro, wet-looking dry hair | 부정된 의미가 선택 duty가 되지 않음; 공존 가능한 축을 배타화하지 않음 |
| 속성 lock | hair/style/color/inner-layer/root-height/장식, same owner 다른 dimension 경로 | 부모·자식과 관련 carrier 효과가 잠금을 준수; undeclared effect를 우회 수단으로 사용하지 않음 |
| retrieval | 독립 작성한 holdout, exact/BM25F/advisory embedding, generic 동명이의어, top-k exposure | 단순 hit보다 올바른 scope/상위 노출/의미 다양성의 개선; nonvisual·context·confounder가 긍정 prototype을 오염시키지 않음 |
| 실제 pack/prompt | frozen prepack core→조회→선택→의무→최종 문구, 선택 0개 대조 | local data가 pre-core 의미를 작성하지 않음; 선택된 관계·소유자가 final prompt까지 유지 |
| history/freshness | archived core/pack receipts, successor record, pending state | 과거 봉인 자료 재생 가능; 현재 source/index 불일치는 성공 처리하지 않음 |

기존 tests에서 관련 범위는 `test_photo_hair_visual_semantics.py`, `test_photo_wet_hair_weight_alternative.py`, `test_photo_candidate_semantics.py`, `test_photo_visual_profile_retrieval.py`, `test_photo_visual_obligations.py`, `test_photo_prepack_isolation.py`, `test_photo_runtime_freshness.py`, `test_photo_runtime_boundary_history.py`다. 새로운 의미 경계를 다루는 독립 fixture를 먼저 확정하고 대상 suite를 실행한다. 기존 테스트를 이름만 바꿔 반복하거나 source와 같은 문장을 테스트 oracle로 복사하지 않는다.

정량 보고는 query별 올바른 owner/sense의 순위·노출·잘못 활성화된 duty, 제외·부정 유지, 공존 통과율을 함께 남긴다. 이 보고서에는 실행 전 숫자 목표나 개선률을 만들어 넣지 않았다. 충분성은 위의 critical boundary case가 통과하고 새 holdout에서 같은 오류가 재발하지 않는지로 확인한다.

## P5 — 픽셀 검증과 채택 판단

이미지 검증을 진행하는 별도 단계에서 동일한 독립 core와 통제 조건으로 baseline/후보 차이를 비교한다. 원래 holdout을 데이터에 맞추어 고치지 않는다. French/Dutch 두피 경로, 히메/젤리피시 뒤 cap, high/low 밑동, 겉/안층 색, 장식 재료·접합처럼 실패 영향이 큰 관계를 우선한다.

필수 부위가 같은 프레임에 보이는 view를 선택하고 전체 관계를 all-of로 판정한다. 필요한 부위가 가려졌으면 `UNOBSERVABLE_NOT_PASS`, 일부만 맞으면 해당 duty 실패로 남긴다. 결과 사진만으로 자연색/펌/설치법/임상 원인/성격을 입증하지 않는다. 정지 프레임의 prehensile/floating hair는 접촉·공중 위치만 확인하며 시간적 운동·의지는 추가 증거가 필요하다.

픽셀 fixture 수는 조사 카드 수에 비례해 부풀리지 않는다. 우선 관계 대조를 검증하고, 새로운 실패가 있는 경우 그 경계까지 확장한다. moderation-blocked/생성 실패/관찰 불가를 PASS로 바꾸거나 프롬프트를 조용히 바꿔 같은 시험이라고 주장하지 않는다. 이미지 생성 요청·실행 범위가 정해지기 전에는 이 단계의 이미지를 만들지 않는다.

최종 채택 보고는 authored source, generated index, 조회 노출, selected candidate IDs, final prompt, native pixels, 사용자 수용을 따로 기록한다. 의미 카드가 늘었다는 이유만으로 마지막 두 층까지 달성했다고 발표하지 않는다.

## 실제 변경 경로와 review 단위

실제 반영 작업을 시작하면 P0 의미 수정, P1/P2 구조 source 확장, P3 index regeneration, P4 회귀 결과를 각각 리뷰 가능한 변경 단위로 정리한다. 이 순서는 별도 PR/배포를 자동 생성한다는 뜻이 아니다. 지금은 연구 신규 파일만 작성하고 기존 runtime·source·tests·history를 수정하지 않는다.

연구에서 보류된 항목은 다음 구현의 blocker 목록으로 넘긴다. 단순 색·길이 변형은 공통 축을 재사용하고, 현재 본문이 안 열리는 출처나 특정 subtype의 핵심 정의는 직접 근거를 보완한 뒤 채택한다. 반복적인 감시·스케줄·자동 successor 목표를 만들지 않고 이 계획의 한정된 결과를 마무리한다.

# 종교·신화 시각 의미·후보팩 반영 계획

기준일: 2026-10-03. 연구 결과: [RESEARCH.md](RESEARCH.md). 이 문서는 실행할 변경과 통과 조건을 정의한다. 현재 운영 자산·로더·테스트·인덱스에는 연구 결과를 반영하지 않았다.

## 목표와 반영 단위

목표는 특정 종교 이름을 입력했을 때 관습적인 이미지를 자동 추가하는 것이 아니라, **요청이 지정한 도상과 변형의 구성 요소·소유자·관계를 보존하면서 적합한 후보를 발견하고 채택하는 것**이다. 같은 이름의 다른 팔 수·다른 지물·다른 시대를 섞지 않고, 부정어·제외·property lock·표현 매체를 유지해야 한다.

연구 단위 140개 중 후보 관찰 초안 110개를 A 41 / B 47 / C 22로 나눴다. 맥락 30개는 활성 후보를 만들지 않는다. **110개 관찰 초안은 최종 후보 엔트리 수가 아니다.** 하나의 초안이 여러 슬롯의 원자 후보로 분해되거나, 기존 의미로 합쳐지거나, 출처·소유권 부족으로 보류될 수 있다. 최종 profile·candidate 수는 아래 설계와 검증 뒤 확정한다.

실행 목록과 구성원은 [BATCH-PLAN.json](BATCH-PLAN.json), 판단 근거는 [CANDIDATE-DRAFTS.json](CANDIDATE-DRAFTS.json)에 있다. 연구상의 작업 묶음당 최대 8단위는 검토 크기 제한이며, runtime bundle의 최대 구성원 8개와 별개다.

## D0. 기준 상태·출처·의미 소유자 확정

1. 작업 시작 직전에 branch·HEAD·dirty 파일·현재 로더 상태를 다시 기록한다. [LIVE-AUDIT.json](LIVE-AUDIT.json)의 해시가 그대로라고 가정하지 않는다. 다른 작업의 수정과 연구 폴더를 보존하고, 필요한 경우 적합한 기존 worktree를 확인한 뒤 분리된 작업 공간을 사용한다.
2. 110개 단위마다 `existing_owner_id`, `variant_id`, 실제 core target, property, 허용 slot/dimension, profile 필요 여부를 작성한다. 긍정 필드의 단어 일치는 기존 소유자를 찾는 단서이며 의미 동등성의 판정이 아니다.
3. 사용할 출처의 소장번호·판본·날짜·지역·보존 상태와 구성 요소를 원본 도판에서 대조한다. `SEARCH_EXCERPT_ONLY` 자료와 `cerberus_two_heads`의 미확정 도판은 활성 반영 전 확인한다. `NO_USABLE_BODY`인 네 팔 친나마스타 추가 자료는 현재 어떤 활성 근거로도 사용하지 않는다.
4. 재현할 원본의 권리·공개 범위를 확인하고 자료 링크와 검토 기록을 남긴다. 유물 기록과 도상 재구성은 요청의 매체·복원 범위에 맞춰 구분한다. 특정 공동체의 공개 작품 설명을 다른 공동체의 보편 도상으로 확장하지 않는다.

**D0 산출물:** 단위별 소유권 결정표, 원본 도판 검토 기록, 기존 profile/candidate 재사용표, 보류 사유, 입력 해시. 출력은 유지보수 증거이며 runtime 스키마에 출처 본문을 삽입하지 않는다.

## D1. 동일 의미는 기존 소유자를 보강하고 다른 변형은 분리

| 판단 | 변경 방법 | 완료 조건 |
|---|---|---|
| 기존 의미·타입·효과와 동일 | 기존 ID 유지. 긍정 표기·동의 표현·요청 맥락을 필요한 범위에서 보강 | 필수 요소·속성 소유·lock 범위가 넓어지지 않음 |
| 같은 이름이지만 개수·연결·사건 단계가 다름 | 별도 변형 의미 ID와 필요시 별도 profile | 명시 변형이 이웃 변형을 활성화하지 않음 |
| 자료가 특정 혼합형을 기록 | 기본 구별 + 해당 혼합형의 명시 범위 | 전역 상호 배타 규칙으로 정당한 혼합형을 배제하지 않음 |
| 설명이 해석·서사·효능뿐임 | 유지보수 맥락으로 보존 | 긍정 검색·픽셀 의무·인물 정체로 승격되지 않음 |
| 원본·소유권·활성 조건이 불명확 | `HOLD` 유지 | 후보 수를 채우기 위해 임의 유형을 만들지 않음 |

`existing_slot_context_extensions`는 동일 의미의 paraphrase/context를 추가하는 용도로만 쓴다. 다른 물건·신체 구조·행위·property 효과를 기존 엔트리에 덧붙이는 통로로 쓰지 않는다. 연구의 22–23절 중복 색인은 기존 단위로 링크하며 중복 의미 ID를 생성하지 않는다.

### 이집트 계량의 구체 결정

`heart_ani_roles`는 기존 `egyptian_heart_weighing_judgment`를 재사용한다. 기존 5그룹인 `deceased_subject`, `heart_feather_balance`, `anubis_attendance`, `thoth_recording`, `judgment_consequence`를 보존한다. 출처 보강과 역할 검증을 추가하되 아누비스·토트·암미트의 소유를 바꾸지 않는다.

`heart_maat_figure`는 연구상 별도 변형이다. 제안 ID `egyptian_heart_weighing_maat_figure`는 아직 운영 ID가 아니다. 마아트 상을 지정한 core가 기존 단독 깃털 의무까지 동시에 요구하지 않도록 현재 데이터의 요청 활성 조건·제외 조건으로 표현 가능한지 확인한다. 표현 불가이면 이 변형은 맥락으로 남기고 일반 활성화 계약의 개선을 별도 설계한다. 이집트 전용 라우트나 이름 감지 분기를 추가하지 않는다.

## D2. 슬롯 소유권과 후보의 원자성

현재 정책은 `action`/`relational_action` → action, `anatomical_connection` → body_geometry, `composition` → composition, `location` → setting, 복식·액세서리 → appearance, `surface_material` → material을 허용한다. 초안의 힌트가 허용 차원에 들어간다는 것과 실제 property가 유효하다는 것은 다르다. 연구의 `<bind_actual_frozen_core_target>`와 제안 경로를 실제 대상·속성으로 교체한 후 계약 검증을 통과시킨다.

복합 관찰은 다음처럼 분해한다.

| 연구 단위 | 분해할 효과 | 지켜야 할 경계 |
|---|---|---|
| 나타라자 | 요청된 body 구조, 손의 동작, 손별 지물, 관계가 보이는 구도 | `action` 후보 하나가 신체·지물·배경까지 새로 만들 권한을 갖지 않음 |
| 도교 의례복 | 의복 표면의 문양 위치·재료 외관 | 옷의 거북·뱀을 착용자의 해부 구조로 바꾸지 않음 |
| 키마이라 | 한 core 개체의 등 머리·꼬리 연결 | 세 개체를 추가하거나 species lock을 우회하지 않음 |
| 하누키아 | 이미 core가 지정한 기물의 홀더 구조와 가시 구도 | 가지 수와 점화 위치를 혼동하지 않음 |
| 미투나 | 이미 core에 있는 두 대상의 접촉·시선 | 추가 인물·관계·성행위를 후보가 추론하지 않음 |

### `prop` 27건의 선행 설계

현재 `slot_dimensions.prop = []`, `unknown_scope = not_eligible_for_bundle_adoption`이다. 성유물함·금강저/방울·성물·아차·헤이 티키·도표 등 27개 초안은 새 `prop` 차원을 발명해서 통과시킬 수 없다.

- **core가 기물을 명시한 경우:** 기물의 사실적 요구는 core 의미 의무가 소유한다. 선택 후보는 해당 대상의 기존 허용 property만 다룬다. 구도 후보는 이미 요청된 지물이 읽히는 배치·프레이밍만 조정할 수 있다.
- **선택 후보가 기물을 새로 넣어야 하는 경우:** 현재 계약에서 채택 보류. 실제 대상·property·잠금 경계를 정의하는 범용 기물 소유권 설계가 먼저 필요하다. policy·validator·property-lock 회귀를 함께 변경하는 별도 범위로 기록한다.
- 기물 효과를 `aesthetic_trend`·`composition`에 이름만 바꿔 숨기거나 `subject`/`person_origin`으로 인물 정체를 변형하지 않는다.

**D2 통과 조건:** 모든 활성 member에 실제 target/property가 있고 slot 허용 차원·lock·core count/identity를 지킨다. unknown scope 후보는 채택되지 않는다. 해결되지 않은 단위는 단계 A에 있어도 보류한다.

## D3. 작성할 파일과 기존 로더 접점

아래 이름은 운영 반영 시 제안 경로다. 이번 리서치에서 생성하지 않았다.

| 파일/접점 | 계획한 변경 |
|---|---|
| `skills/photo-prompt-image-generator/assets/photo_prompt_religion_iconography_extension.json` | 기존 extension 계약에 맞춘 slots·visual_semantics·필요한 동일 의미 맥락. 출처 본문·연구 질문·priority 필드는 넣지 않음 |
| `skills/photo-prompt-image-generator/assets/photo_prompt_visual_obligations_religion_iconography.json` | 요청에서 활성화할 변형의 관찰 그룹·관계. 기존 의미는 기존 registry의 ID 재사용 |
| `skills/photo-prompt-image-generator/scripts/prompt_generator.py` | 파일을 만들었을 때 기존 `RESEARCH_EXTENSION_FILENAMES`와 `VISUAL_OBLIGATION_EXTENSION_FILENAMES`에 등록. 별도 이름 감지 경로 없음 |
| candidate semantic policy | 신규 extension이 적용되는 기존 정책의 required extension 연결. 기물 소유권을 확장하려면 별도 D2 설계·검증 |
| 유지보수 증거 레코드 | 출처·도판 검토·결정·혼동 경계·원본 SHA를 보존하고 `maintenance_ref`로 연결 |
| 파생 인덱스 | authored 데이터 정합성 확인 후 빌더로 재생성. JSON·임베딩·BM25F 수동 수정 없음 |

runtime extension은 `photo-prompt-research-extension/v1`의 허용 키만 사용한다. 현재 허용 키는 `schema_version`, `facet_vocab`, `slots`, `coherence_rules`, `character_mechanism_graph`, `slot_applicability`, `visual_semantics`, `maintenance_ref`, `existing_slot_context_extensions`다. 별도 의무 확장은 `photo-visual-obligation-registry-extension/v1`, 병합 registry는 `photo-visual-obligation-registry/v3` 계약이다.

semantic 묶음도 현재 `BUNDLE_SOURCE_KEYS`의 허용 필드만 작성한다. 관계는 운영 계약의 `id/type/subject/object`로 번역하고 연구의 `owner_binding_status`를 그대로 복사하지 않는다. `maintenance_ref`는 현재 `contract_version/record_id/sha256` 형식으로 만든다. **SOURCES·SEMANTIC-UNITS·CANDIDATE-DRAFTS JSON을 로더에 직접 넣지 않는다.**

정확한 키·schema·tuple은 구현 직전에 소스를 재확인한다. 현재 읽은 접점은 `prompt_generator.py`의 extension tuple과 `load_json`/`load_visual_obligation_registry`, `photo_candidate_semantics.py`의 strict key 집합·policy 검증이다.

## D4. 단계별 작성·검증 순서

각 작업 묶음은 도판 대조 → 소유권 결정 → authored profile/candidate → 단위·계약 회귀 → 인덱스 → 동일 core 후보팩 → 생성·픽셀 판정 순으로 진행한다. 단계 전체를 먼저 대량 작성한 뒤 오류를 찾지 않는다.

| 단계 | 연구 초안 | 우선 사례 | 선행 조건·완료 기준 |
|---|---:|---|---|
| A | 41 | halo/mandorla, 미흐라브·민바르, 바르톨로메오·베드로 지물의 구도, 탈리트·테필린, 도교 의례복, 기존 심장 계량 | 원본·대상 소유·표현 매체 확인. 단순 형태라도 `prop`와 검색 발췌 자료는 보류 조건 우선 |
| B | 47 | 두르가 4/8팔, 나타라자, 피에타·성모 안식, 가네샤, 나가 지지, 켄타우로스 변형, 미투나, 마앙가카 | 변형 명시·개체/부분 count·손/지물·지지/접촉 관계. 기록된 혼합형 허용 |
| C | 22 | 헤바즈라 8/16, 친나마스타의 소유된 세 흐름, 슬레이프니르, 케르베로스 두 머리, 스리 얀트라·세피로트, 레비스·바포메트 판본 | 복잡한 count·도표 전사·객체/판본 확인. 불명확한 자료는 맥락 유지. 원본·네이티브 픽셀 검증 필수 |

첫 실행 사례는 `head_halo`, `body_mandorla`, `mihrab_minbar`, `muqarnas_cells`, `tallit_corner_fringe`, `daoist_robe_sky`, `peter_keys`, `bartholomew_knife` 중 D0–D2를 통과한 단위에서 시작한다. 동일 core에 이미 필요한 대상을 보존하고 후보가 바꿀 수 있는 범위가 좁은 사례부터 계약 경로를 검증한다. `heart_ani_roles`는 기존 소유자 재사용의 첫 사례로 삼되 BM 도판 검토 후 진행한다.

## D5. 요청·후보팩 회귀

[REGRESSION-PROPOSALS.json](REGRESSION-PROPOSALS.json)의 387건은 설계 템플릿이다. 양성 fixture를 실제 request envelope와 검증된 frozen core로 작성하고, 예상 후보 ID·profile·target·property·거절 사유를 구체화해야 실행 가능한 테스트가 된다. 구현 시 기존 관련 테스트를 유지하고, 새 데이터 범위에 맞는 사례를 추가한다.

필수 검증은 다음과 같다.

1. **명시 양성:** 선택 변형이 적합한 optional 후보를 노출한다. 정확한 의무는 요청 근거로만 활성화된다. 노출·선택·채택·의무 활성화를 별도 확인한다.
2. **부정·이웃:** ‘넣지 않는다’, 이웃 도상의 이름, 다른 팔 수·판본·매체가 잘못 활성화되지 않는다. 검색에서 가까워도 의미가 바뀌지 않는다.
3. **소유·잠금:** 북/불 손 바꾸기, 지물 보유자 바꾸기, 머리 수 바꾸기, core 밖 인물 추가, 잠긴 property 변경을 거절한다.
4. **동일 core 비교:** 기준과 변경 팩의 core SHA가 같다. 관련 optional 노출만 비교하고, 다른 사건·sexual tone·identity·count·medium 변화가 없는지 확인한다.
5. **공통 계약:** unknown scope는 보류, 문헌 맥락은 비시각, 기록된 혼합형은 허용, 부분 가림은 의미 충족으로 간주하지 않는다.

표적 사례는 ‘마아트 상을 깃털로 대체’, ‘하누키아를 9가지로 바꿈’, ‘그리스 세이렌을 인어로 바꿈’, ‘켄타우로스의 자료 특정 인간 다리를 없앰’, ‘미투나에 성교 추가’, ‘루치아 얼굴에 상해 추가’, ‘가면을 생물학적 얼굴로 바꿈’, ‘드라포를 베베로 바꿈’, ‘두 개의 말로 여덟 다리 대체’다. 각 경우 실제 core와 mutation fixture를 따로 작성한다.

현재 발견 예산 15개·assertion당 3개, joint adoption 최대 8묶음·묶음당 8member, 최소 공유 단어 3개를 유지한다. 후보 수를 늘리기 위해 예산을 넓히지 않는다. source-only 설명·부정 예·유지보수 태그가 긍정 검색 텍스트나 runtime score에 들어가지 않는지도 검증한다.

기존 `tests/test_photo_mythology_visual_semantics.py`의 10묶음/60후보와 `tests/test_photo_legend_visual_semantics.py`의 8묶음/48후보 기준은 이유 없이 수정하지 않는다. 새 extension의 수량을 별도로 검증하고 기존 profile·회귀를 유지한다. 직접 영향 범위는 `test_photo_candidate_semantics`, `test_photo_semantic_guidance_data`, `test_photo_death_afterlife_semantics` 및 새 도상 단위 테스트다.

## D6. 검증·인덱스 재생성 명령

아래는 **미실행 계획 명령**이다. 저장소 루트에서 해당 작업 공간의 런타임·실제 CLI를 확인한 뒤 수행한다. visual profile 빌더의 `--check`는 현재 존재하지만 semantic index 빌더에는 같은 옵션이 없다.

```sh
# authored 변경 후, 인덱스 의존 실패는 baseline과 분리해 기록
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py

# 해당 데이터 영향 범위의 회귀
.venv/bin/python -m unittest tests.test_photo_mythology_visual_semantics tests.test_photo_legend_visual_semantics tests.test_photo_death_afterlife_semantics tests.test_photo_candidate_semantics tests.test_photo_semantic_guidance_data

# 변경 임베딩/API 호출량을 확인하는 읽기 전용 계획
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run

# authored 정합성 확인 후 파생 데이터 재생성
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 1 --progress

# 파생 데이터까지 포함한 최종 validator와 표적 회귀
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
```

같은 source·recipe·model·dimension을 가진 캐시 벡터만 재사용한다. 새/변경 텍스트의 임베딩은 API 호출이 필요할 수 있으며 실패·checkpoint·완료 manifest를 구별한다. 단순 `--dry-run` 성공이나 기존 인덱스 파일의 존재는 갱신 성공이 아니다. 최종 semantic index는 로더·validator가 요구하는 source 해시와 일치하는지 확인한다. 표적 검증이 통과한 뒤 전체 테스트는 새로운 실패나 교차 영향이 있을 때 필요한 범위로 넓힌다.

## D7. 생성·네이티브 픽셀 qualification

[PIXEL-GATES.json](PIXEL-GATES.json)의 110건은 선정 변형의 모든 구성 요소·관계를 확인하는 계획이다. 원본 도판 검토와 새 이미지 픽셀 검증은 다른 증거다. 운영 변경을 실제로 평가하는 단계에서는 사용자 요청·frozen core·팩·선택·prompt/negative bytes·해시·생성 시도·이미지 경로·원본 해상도 검토를 연결한다.

작은 대표 묶음부터 시작한다. A의 기존 심장 계량과 복식 표면, B의 두르가 4/8팔·키마이라 연결, C의 슬레이프니르·도표처럼 오류 유형이 다른 사례를 고른다. 모든 필수 그룹·소유 관계·count·구조가 보이면 `PASS`, 틀리면 `FAIL`, 판단 불가이면 `UNOBSERVABLE`이다. `partial_is_fail`을 유지하고 가림으로 사라진 필수 손·다리를 통과시키지 않는다. 일반 요청에 없는 자료 세부를 새 의무로 만들지도 않는다.

도표·문자는 전체 인상보다 원본 노드/간선·방향·문자 전사 기준으로 검토한다. 의례 동작의 정지 이미지는 실제 회전 방향·수행 지속·신앙적 효능을 인증할 수 없다. 유물 결손을 기록하는 경우 원래의 결손은 새 이미지 오류와 구별한다.

생성이 moderation으로 차단되면 차단된 시도로 기록하며 품질 실패나 성공으로 바꾸지 않는다. 기술 픽셀 통과와 사용자 선호·수용도 별도로 기록한다. 이번 연구에서는 생성/API 호출과 이 단계의 판정을 수행하지 않았다.

## 반영 완료 기준과 회복

| 증거 단계 | 완료 기준 |
|---|---|
| 연구 | 모든 참고 행의 추적, 출처 접근 상태, 관찰/맥락/보류 분리, 정합성 PASS |
| authored | 실제 owner/target/property, strict schema, 기존 의미·lock 보존, unknown scope 보류 |
| 파생 데이터 | 등록된 확장과 source 해시 일치, builder·validator 확인 |
| 후보팩 | 동일 frozen core에서 노출·채택·거절 이유 확인, 후보 선택의 의무 승격 없음 |
| 회귀 | 표적 양성·부정·이웃·lock·변형 사례의 실제 실행 통과 |
| 픽셀 | 해당 배치 필수 요소·관계의 ALL_OF 통과. 판단 불가를 통과로 간주하지 않음 |
| 사용자 수용 | 기술 qualification과 별도로 기록 |

통과한 배치와 보류 배치를 분리해 반영한다. 실패 시 해당 배치의 authored 변경·로더 등록·그로부터 만든 파생 인덱스만 함께 복구한다. 연구 근거와 실패 로그는 보존하며 기존 신화·전설 owner ID 및 다른 작업의 변경은 유지한다. 검토 가능한 diff와 결과를 남기고, commit·push·배포는 실제 구현 작업의 권한과 범위에 맞춰 처리한다. 현재 단계에서는 수행하지 않았다.

## 계속 조사할 범위

새 초안이 없는 94행과 맥락 수준인 62행은 [FOLLOWUP-RESEARCH.md](FOLLOWUP-RESEARCH.md)의 전통별 질문으로 이어 간다. 먼저 충돌 가능성이 큰 링가·요니, 칼리/차문다/바이라바/바라히, 7가지 메노라, 그리스 고르곤·히드라·키클롭스, 북유럽 세계수·노른, 베베·샹고를 조사한다. 이름·도상·기능을 구별할 수 있는 시기·지역이 확인된 두 자료가 우선이며, 단일 작품이나 이견이 있는 개념은 그 한계를 유지한다.

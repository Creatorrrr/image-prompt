# 슬롯 후보 조회 검증 리포트

검증일: 2026-10-11 (Asia/Seoul)

데이터 적재와 정확 표기 검색은 대부분 정상이다. 그러나 **모든 슬롯에서 장면에 맞는 후보가 잘 불러와진다고 판정할 수는 없다.** 114개 슬롯 중 109개는 실제 retrieval 함수가 원본 후보를 반환하는 것을 확인했고, 5개 슬롯은 현재 정의로 일반 slot inventory 조회 경로가 막힌다. 독립 장면에서는 적합한 후보와 의미가 다른 후보가 함께 노출됐다.

## 1. 대상과 증거 범위

- 현재 작업 폴더의 데이터를 검증했다. HEAD: `218e339320f0e3c27aac3f2a48a9299812b16935`. 커밋에 없는 기존 수정도 포함한다.
- 검증 generation: `f492f8a428edcf489d7fd9b0c2f2525b2dc7ac1c180446cf20f6eb5af7a19870`.
- source fingerprint: `614b5e4fb66959c7304e45bfbb1de601f6cbd892dd908812e2e7492f7ecf843b`.
- [사전 계획](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/PLAN.md)을 작성한 뒤 실행했다. 원본/코드 수정, 이미지 생성, embedding API 호출, 커밋/푸시는 수행하지 않았다.
- source 기반 227개 probe와 좁힌 12개 probe는 **유지보수용 하위 함수 입력**이다. 일부는 사진 prompt로 쓰지 않는 placeholder를 사용한다. 전체 스킬 authoring 절차나 정상 사진 요청의 품질 검증으로 계산하지 않는다.
- 공개 CLI의 8개 장면은 후보 문구를 복사하지 않은 별도 fixture다. 최소 core/intent-lock 및 합성 embodiment review를 사용한 구조 검증이며, 전체 authoring 요구사항·공간적 타당성·최종 composition·픽셀 품질 검증은 아니다.

## 2. 수치 결과

| 검사 | 실제 결과 | 해석 |
|---|---:|---|
| 원본 → loader | 12,043/12,043 | 등록 슬롯/ID 누락·중복 없음 |
| slot BM25F / semantic index | 12,043/12,043 | 슬롯 문서 누락·잉여 없음 |
| 정확 표기 질의 | 40,638/40,643 | 토큰이 비는 5개 alias 실패 |
| 정확 표기의 슬롯 한도 내 순위 | 40,407/40,643 | cap 2/4 이내; 실제 pack 노출률과는 다름 |
| 첫·마지막 후보 probe | 146/227 target 노출 | 205건 eligible; rank/fusion/관측 우선순위/공유 cap이 추가로 작동 |
| focus를 좁힌 추가 probe | 11/12 target, 12/12 슬롯 노출 | 경로가 없는 슬롯과 넓은 입력에서 밀린 슬롯을 구분 |
| 실제 retrieval 함수 후보 반환 | 109/114 슬롯 | 모든 후보가 모든 context에서 노출된다는 뜻은 아님 |
| 공개 CLI 후보팩 생성 | 8/8 | 8개 pack에서 서로 다른 슬롯 94개 관찰 |
| 공개 CLI 예상 슬롯 노출 | 47/54 검사 | 검증 가설이며 정상 scope 제외도 포함 |
| composer view ID 보존 | 8/8 | slot 후보 ID 보존 |
| 원본 기반 core retrieval 재계산 | 8/8, 오류 0 | `audit_core_retrieval` 검사만 수행 |
| 후보 1개 삭제 변조 검출 | 8/8 | 무결성 검사 작동 |
| 관련 회귀 테스트 | 40/40 | 검색·계약 검사; 의미 적합성을 자동 보증하지 않음 |

인덱스에는 슬롯 외 character graph 문서 36개도 있지만 slot BM25F에는 슬롯 후보 12,043개만 사용한다. 반환된 ID는 모두 원본의 동일 슬롯/ID에 존재했다. 모든 측정에서 전체 cap 64와 해당 슬롯의 2/4 cap을 지켰고 조회 전후 core 해시가 같았다.

## 3. 현재 경로가 막힌 5개 슬롯

| 슬롯 | 후보 수 | 원인 |
|---|---:|---|
| `occasion_context` | 106 | `slot_dimensions`가 빈 배열이고 후보 `affected_dimensions` fallback도 없음 |
| `safety_profile` | 21 | 같은 소유 차원 누락 |
| `costume_absorption_guard` | 12 | 같은 소유 차원 누락 |
| `adult_context` | 6 | 필수 domain `adult`를 만들 현재 routing alias 행이 없음 |
| `fetish_styling` | 24 | 같은 `adult` domain 연결 누락 |

**총 169개 후보**가 source와 index에는 있지만 일반 slot inventory 경로에서 노출될 수 없다. `occasion_context`는 core slot 목록에도 있어 목록 등록만으로 실제 조회가 보장되지 않음을 보여준다. 두 guard 슬롯의 비활성화가 의도라면 비활성 데이터로 명시하고, 의도가 아니라면 소유 범위를 복구해야 한다.

소유 차원이 없으면 [focus 생성](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:9815)이 즉시 빈 query를 반환한다. 근거: [원본 소유 차원](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json:176), [occasion_context](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_tags.json:303), [인벤토리](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/inventory.json).

[domain resolver](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:2741)은 [authored routing](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/assets/photo_prompt_quality_layers.json:467)의 alias 행을 순회한다. `style.domain`을 직접 domain 값으로 복사하지 않는다. `adult`를 style에 적거나 sensual/fetish를 올려도 이 두 슬롯의 `require_domain_match`를 만족시키지 못한다. 활성 adult 축의 CLI 장면에서도 해당 출처 후보가 ordinary 슬롯과 adult-axis inventory에 없었다. **adult 축의 다른 검색 전체가 고장났다는 뜻은 아니다:** 해당 장면의 두 contextual axis는 `keyword` 모드로 각각 12개 후보를 반환했다.

근거: [도달 가능성 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/reachability-diagnostics.json), [adult 장면 pack](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/public-cli/08-fashion-en/candidate-pack.json).

## 4. 전체 후보 표기 검색

생산 코드 `rank_bm25f`와 owning slot의 모든 후보 ID를 사용했다. 모든 en/ko 필드 및 중복을 제거한 모든 명시 alias를 조회했다. 다른 ranker·mock·인위적 source 축소를 사용하지 않았다.

| 표기 | 질의 수 | 기대 ID 적중 | 슬롯 cap 2/4 내 |
|---|---:|---:|---:|
| 영어 | 12,043 | 12,043 | 12,043 |
| 한국어 필드 | 12,043 | 12,043 | 12,040 |
| 명시 alias | 16,557 | 16,552 | 16,324 |

한국어 필드가 영어 문구로 저장된 데이터도 있으므로 순수 한국어 benchmark로 해석하지 않는다. 정확 표기 검사는 기계적 검색 가능성이다. 후보 문구를 모르는 사용자의 paraphrase 정확도나 semantic precision을 뜻하지 않는다.

미적중 5건은 모두 `costume_style` alias다.

| 저장 alias | 후보 ID | tokens |
|---|---|---|
| `साड़ी` | `sari_continuous_drape_system` | `[]` |
| `धोती` | `dhoti_waist_leg_drape_system` | `[]` |
| `ชุดไทย` | `thai_chut_thai_regional_ensemble` | `[]` |
| `ثوب` | `arabian_thobe_ankle_length_robe` | `[]` |
| `عباية` | `abaya_outer_robe_system` | `[]` |

[token regex](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/bm25f_retrieval.py:22)은 ASCII/Hangul/Japanese/Han 범위를 사용한다. 위 문자만으로 질의하면 slot BM25F 결과는 0개다. 같은 후보의 다른 영어·한국어 표기는 찾을 수 있다.

한국어 필드 중 cap 밖 3건은 `hair_style:chrh_hair_cut_fade`의 `페이드`(3위), `garment_detail:opening_frock_coat_long_skirt_2`의 `조끼 앞판`(3위), `garment_detail:y2kr_low_rise`의 `낮은 허리선`(4위)다. 검색 결과에는 존재했다. [40,643건 원시 결과](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/exact-recall.ndjson) / [집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/exact-recall-summary.json).

## 5. 검색과 pack 노출의 차이

초기 227건에서 target 미노출 81건의 진단은 다음과 같다.

| 진단 | 건수 | 의미 |
|---|---:|---|
| ranking / fusion / 공유 cap | 49 | eligible이며 lexical 순위가 있지만 최종 target 없음; 관측 우선순위도 포함 |
| 소유 차원 또는 focus 없음 | 12 | 6건은 dead slot, 6건은 최소 fixture의 surreal concept 근거 부족 |
| declared / primary context 미충족 | 7 | 필요한 context의 frozen 입력 입증 부족 |
| slot domain 미충족 | 5 | adult 슬롯 및 capture fixture |
| entry domain 미충족 | 4 | 후보별 선언 domain 필터 |
| slot subject category 제외 | 2 | human fixture의 surface_material 제외 |
| slot domain 명시 제외 | 1 | documentary capture fixture |
| 기타 eligibility | 1 | 원시 입력 및 source guard 진단 보관 |

정상 scope 제외를 조회 오류로 계산하지 않았다. broad probe는 기본 human context로 `surface_material`을 막았지만 object/plant CLI에서 같은 슬롯이 노출됐다. surreal 3개 슬롯도 concept anchor가 있는 CLI에서 조회됐다. 구조적으로 막힌 슬롯이 아니다.

좁힌 probe는 **source를 바꾸지 않고** focus를 명시해 반환 가능성을 확인한 것이다. 11건은 같은 target이 나왔고 `social_cue`는 primary context 미충족으로 다른 source 후보가 나왔다. 원래 실패를 지우거나 이를 사진 요청 성공률로 계산하지 않았다.

`capture_context`도 처음 두 표본은 domain에서 제외됐지만 scientific-inspection 근거를 넣은 별도 입력에서 `instrument_confusion_pair_diagnostic_capture`가 반환됐다. [추가 context](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/capture-context-supplement.json) / [좁힌 조회](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/narrow-probe-summary.json) / [초기 집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/slot-probe-summary.json).

## 6. 독립 장면의 의미 적합성

슬롯 이름과 적합한 후보를 분리해 읽어야 한다. 아래는 실제 source 내용을 읽은 정성 검토이며 모든 후보의 precision 점수는 아니다. 후보는 선택 사항이고 최종 composition에 채택하지 않았다.

| frozen primary subject | 실제 subject 후보 | 검토 |
|---|---|---|
| 우산을 잡고 기다리는 단발 성인 여성 | `local_legend_teller_subject` | adult/human은 맞으나 설화 전달자·청중·장소 흔적이라는 추가 의미 |
| 파란 도자기 찻잔 | `constructed_golem_subject`, `ceramic_automaton_figure` | object/material 범주에 기대어 골렘·자동인형으로 이탈 |
| 새벽 바위 해안 | `cumulonimbus_storm_cell_subject`, `fire_f123` | 폭풍 셀·태양 가장자리 plasma로 이탈 |
| 잔디에 착지한 작은 새 | `earth_diver_creation_subject`, `heraldic_wyvern_subject` | 일반 animal 범주만 맞고 창세 동물·와이번 의미 추가 |
| 역 승강장에서 인사하는 성인 친구 둘 | `karaoke_friend_group` | friends만 맞으며 노래방의 group으로 확장 |
| 작업대 전기 시연 회로 | `rail_switch_actuator`, `hollow_living_armor_subject` | rail 장치·살아 있는 갑옷으로 이탈 |
| 이슬 맺힌 초록 잎 | `mycelium_forest_floor`, `water_w093` | fungi 또는 해저 잎 군락으로 이탈 |
| 검은 새틴 드레스와 앵클부츠의 성인 모델 | `mature_elegant_model` | adult model 범주 부합; mature/elegant는 추가 판단 필요 |

도움 되는 반환도 있었다: `location:rainy_bus_stop_shelter`, `location:rocky_coast`, `hair_style:chrh_hair_cut_supp_french_bob`, `prop:porcelain_teacup_saucer_prop`, `light_direction:backlight`, `footwear:spf_sf108_04`(부츠 shaft가 같은 착용자의 발목에서 끝남), `light_shape:electric_short_spark_gap`(두 금속 끝을 연결하는 짧은 발광 채널).

`subject:coffee_cup`는 실제 데이터에 있으나 `food`로 분류되어 typed `object`인 찻잔 fixture에서 eligible하지 않았다. 파일 미적재가 아닌 source typing/guard 경계 문제다. [category 함수](/Users/chasoik/Projects/image-prompt/skills/photo-prompt-image-generator/scripts/prompt_generator.py:1762) / [원본 내용과 장면 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/independent-scene-diagnostics.json).

**판정:** exact/self-query addressability는 높지만 field projection·coarse category·source context·rank/fusion만으로 주체/상황의 세부 의미 적합성이 충분히 보장되지 않는다. frozen core는 유지되므로 이런 후보를 primary subject 대신 자동 채택해서는 안 된다. 검토자의 거절이 여전히 필요한 단계다.

## 7. 공개 CLI와 audit 범위

| fixture | 슬롯 / ordinary 후보 수 | 예상 슬롯 미노출 |
|---|---:|---|
| 01-rain-portrait-ko | 64 / 64 | 없음 |
| 02-blue-cup-en | 45 / 64 | 없음 |
| 03-coast-fog-ko | 36 / 64 | 없음 |
| 04-small-bird-ko | 37 / 64 | `contact_point` |
| 05-greeting-en | 64 / 64 | `relational_action`, `capture_context` |
| 06-circuit-en | 35 / 64 | `surface_material` |
| 07-dew-leaf-ko | 44 / 64 | 없음 |
| 08-fashion-en | 64 / 64 | `surface_material`, `adult_context`, `fetish_styling` |

bird의 `contact_point`는 human-only 정책, fashion의 `surface_material`은 nonhuman category 정책 때문에 제외됐다. friend의 capture는 허용 domain 입증이 부족했고, circuit의 surface focus는 typed subject에만 투영됐다. 가설 실패를 모두 구현 결함으로 세지 않았다. 모든 요청 property를 완전하게 lock한 별도 authoring benchmark는 후속 과제이며 여기서는 최소 core를 소비하는 검색 경로를 관찰했다.

모든 CLI 결과는 같은 generation을 사용했다. 실제 slot mode는 `same_slot_core_focus_and_frozen_observation_bm25f_rrf`다. adult contextual 검색은 `keyword`였으며 새 query embedding을 사용하는 hybrid 검증을 수행하지 않았다. composer view는 slot ID를 보존했다. 원본 재계산과 deletion 검사는 retrieval 계약만 확인한다. 전체 `audit_composed_prompt.py`·render 검사·후보 채택·이미지 검증을 수행했다고 보고하지 않는다.

[공개 CLI 집계](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/public-cli-summary.json) / [독립 입력](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/independent-scenes.json) / [실행 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/public-cli-run.log).

## 8. 수정 우선순위 제안

1. `occasion_context` owning dimensions를 명시하고 두 guard 슬롯의 의도된 활성/비활성 상태를 정리한다. synonyms 추가로 해결되지 않는다.
2. `adult` domain의 frozen meaning 전달과 declared routing을 연결한다. `capture_context`가 사용하는 portrait/fashion/beauty/social domain도 현재 alias 행이 없는 영향을 점검한다. adult intensity를 domain 의미로 자동 대체하지 않는다.
3. source alias의 문자 체계와 tokenizer 지원 범위를 맞추거나 지원하지 않는 alias를 명시한다. exact-source alias의 token 0개 회귀를 추가한다.
4. primary subject typing/context를 좁히고 일반 물체·동물·환경과 fantasy/role/event 후보 혼입을 검증한다. 적합한 후보를 제거하는 typing 경계도 다룬다.
5. 모든 요청 property를 freeze한 natural-scene benchmark에서 recall@slot-cap, precision, 관련 슬롯 cap 탈락을 측정한다. source-copy probe 통과로 대체하지 않는다.

이번 작업은 진단이며 source/runtime 로직은 고치지 않았다.

## 9. 보존과 재현

assets/scripts/precore **196개 파일 해시가 전후 동일**했다. HEAD와 기존 tracked dirty 경로 22개 목록도 같았다. 산출물은 이 evidence 디렉터리에 추가했다. [보존 확인](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/preservation.json).

재현에는 같은 source 바이트와 compatible Python/코드를 사용한다. pinned generation을 최신 데이터로 바꿔 해석하지 않는다.

- [전체 source/표기 harness](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/verify_inventory.py)
- [114개 슬롯 harness](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/verify_slot_probes.py)
- [공개 CLI harness](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/verify_public_cli.py)
- [domain/context 진단](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/verify_diagnostics.py)
- [좁힌 focus harness](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/verify_narrow_probes.py)
- [보고서 생성](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/build_report.py)
- [40개 테스트 로그](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/focused-tests.log) / [dictionary validation](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/dictionary-validation.log)

## 10. 슬롯별 전체 결과

`CLI+함수`는 공개 CLI 및 하위 함수, `함수`는 유지보수 probe만 관찰됐다는 뜻이다. 초기 target hit는 첫·마지막 후보의 값이며 의미 적합성 점수가 아니다. 114행 및 source/실제 ID는 [CSV](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/SLOT-RESULTS.csv)와 [기계 판독 요약](/Users/chasoik/Projects/image-prompt/docs/research-evidence/photo-prompt/slot-retrieval-verification-20261011/SUMMARY.json)에 있다.

| 슬롯 | 데이터 수 | exact ID 적중/질의 | 초기 target hit/probe | 조회 경로 |
|---|---:|---:|---:|---|
| `action` | 1045 | 3156/3156 | 2/2 | CLI+함수 |
| `adult_context` | 6 | 16/16 | 0/2 | adult domain 라우팅 없음 |
| `aesthetic_trend` | 143 | 633/633 | 2/2 | CLI+함수 |
| `aftermath_trace` | 81 | 286/286 | 2/2 | 함수 |
| `ambient_particle` | 34 | 99/99 | 2/2 | CLI+함수 |
| `anatomical_connection` | 73 | 281/281 | 2/2 | CLI+함수 |
| `apparatus_pov` | 7 | 15/15 | 2/2 | CLI+함수 |
| `appearance_type` | 29 | 65/65 | 2/2 | CLI+함수 |
| `atmosphere` | 2 | 5/5 | 2/2 | CLI+함수 |
| `body_evidence_region` | 12 | 30/30 | 1/2 | 함수 |
| `body_framing` | 19 | 40/40 | 2/2 | CLI+함수 |
| `body_marking` | 25 | 65/65 | 1/2 | CLI+함수 |
| `body_orientation` | 48 | 213/213 | 2/2 | CLI+함수 |
| `body_pose` | 159 | 683/683 | 2/2 | CLI+함수 |
| `brow_style` | 9 | 37/37 | 2/2 | CLI+함수 |
| `camera_direction` | 50 | 133/133 | 2/2 | CLI+함수 |
| `camera_height` | 12 | 35/35 | 2/2 | CLI+함수 |
| `camera_type` | 33 | 68/68 | 2/2 | CLI+함수 |
| `caption_context` | 6 | 13/13 | 2/2 | CLI+함수 |
| `capture_context` | 163 | 551/551 | 0/2 | 함수 |
| `capture_mode` | 12 | 39/39 | 2/2 | CLI+함수 |
| `cheek_makeup` | 9 | 47/47 | 2/2 | CLI+함수 |
| `color` | 240 | 858/858 | 2/2 | CLI+함수 |
| `color_grading` | 71 | 266/266 | 2/2 | CLI+함수 |
| `companion_animal` | 9 | 18/18 | 2/2 | CLI+함수 |
| `complexion_coverage` | 6 | 31/31 | 2/2 | CLI+함수 |
| `composition` | 661 | 2130/2130 | 1/2 | CLI+함수 |
| `concept_tension` | 20 | 82/82 | 2/2 | CLI+함수 |
| `contact_point` | 121 | 466/466 | 2/2 | CLI+함수 |
| `costume_absorption_guard` | 12 | 24/24 | 0/2 | 소유 차원 없음 |
| `costume_style` | 210 | 678/683 | 1/2 | CLI+함수 |
| `crowd_density` | 19 | 95/95 | 2/2 | CLI+함수 |
| `distance_narrative` | 14 | 28/28 | 2/2 | CLI+함수 |
| `duty_prop_state` | 11 | 28/28 | 1/2 | 함수 |
| `emotional_contradiction` | 11 | 26/26 | 2/2 | CLI+함수 |
| `expression` | 164 | 536/536 | 1/2 | CLI+함수 |
| `eye_detail` | 29 | 86/86 | 2/2 | CLI+함수 |
| `eye_makeup_line` | 7 | 33/33 | 2/2 | CLI+함수 |
| `eyeshadow_style` | 14 | 56/56 | 2/2 | CLI+함수 |
| `face_sculpting` | 6 | 29/29 | 2/2 | CLI+함수 |
| `face_shape_relation` | 24 | 103/103 | 2/2 | CLI+함수 |
| `facial_hair` | 7 | 28/28 | 2/2 | CLI+함수 |
| `fetish_styling` | 24 | 79/79 | 0/2 | adult domain 라우팅 없음 |
| `film_emulation` | 28 | 103/103 | 2/2 | CLI+함수 |
| `focus` | 47 | 171/171 | 2/2 | CLI+함수 |
| `footwear` | 96 | 347/347 | 2/2 | CLI+함수 |
| `format` | 26 | 59/59 | 2/2 | CLI+함수 |
| `frame_anchor_medium` | 10 | 31/31 | 2/2 | CLI+함수 |
| `garment_detail` | 1171 | 4411/4411 | 2/2 | CLI+함수 |
| `gaze_engagement` | 31 | 119/119 | 2/2 | CLI+함수 |
| `gaze_target` | 37 | 111/111 | 2/2 | CLI+함수 |
| `genre` | 64 | 136/136 | 2/2 | CLI+함수 |
| `grain_profile` | 14 | 42/42 | 2/2 | CLI+함수 |
| `hair_color` | 43 | 139/139 | 1/2 | CLI+함수 |
| `hair_style` | 200 | 731/731 | 2/2 | CLI+함수 |
| `hand_pose` | 89 | 339/339 | 2/2 | CLI+함수 |
| `intent_state` | 14 | 37/37 | 1/2 | CLI+함수 |
| `lash_style` | 8 | 38/38 | 1/2 | CLI+함수 |
| `lens` | 40 | 111/111 | 2/2 | CLI+함수 |
| `lens_artifact` | 26 | 84/84 | 1/2 | CLI+함수 |
| `light_direction` | 36 | 106/106 | 1/2 | CLI+함수 |
| `light_intensity` | 29 | 90/90 | 0/2 | CLI+함수 |
| `light_shape` | 125 | 367/367 | 2/2 | CLI+함수 |
| `light_type` | 94 | 246/246 | 2/2 | CLI+함수 |
| `lighting` | 236 | 719/719 | 2/2 | CLI+함수 |
| `lip_color_placement` | 9 | 36/36 | 1/2 | CLI+함수 |
| `lip_finish` | 8 | 39/39 | 0/2 | CLI+함수 |
| `location` | 965 | 2997/2997 | 2/2 | CLI+함수 |
| `makeup_decoration` | 9 | 38/38 | 0/2 | CLI+함수 |
| `makeup_style` | 39 | 125/125 | 0/2 | CLI+함수 |
| `makeup_wear_state` | 6 | 30/30 | 0/2 | CLI+함수 |
| `material` | 1 | 3/3 | 1/1 | 함수 |
| `medium` | 66 | 139/139 | 1/2 | CLI+함수 |
| `mood` | 158 | 392/392 | 2/2 | CLI+함수 |
| `motion` | 64 | 201/201 | 1/2 | CLI+함수 |
| `narrative_core` | 56 | 239/239 | 1/2 | 함수 |
| `narrative_phase` | 46 | 163/163 | 0/2 | CLI+함수 |
| `occasion_context` | 106 | 447/447 | 0/2 | 소유 차원 없음 |
| `partner_framing` | 17 | 49/49 | 0/2 | 함수 |
| `partner_role` | 22 | 44/44 | 0/2 | 함수 |
| `person_origin` | 25 | 50/50 | 0/2 | 함수 |
| `platform_framing` | 12 | 40/40 | 2/2 | CLI+함수 |
| `procedure_step` | 83 | 281/281 | 0/2 | CLI+함수 |
| `prop` | 1006 | 3627/3627 | 2/2 | CLI+함수 |
| `prop_direction` | 20 | 55/55 | 1/2 | CLI+함수 |
| `proxemics` | 10 | 24/24 | 1/2 | 함수 |
| `quality` | 57 | 190/190 | 0/2 | CLI+함수 |
| `reflection_logic` | 34 | 152/152 | 1/2 | CLI+함수 |
| `relational_action` | 93 | 316/316 | 0/2 | 함수 |
| `safety_profile` | 21 | 44/44 | 0/2 | 소유 차원 없음 |
| `scale_relation` | 15 | 38/38 | 1/2 | CLI+함수 |
| `sensory_focus` | 14 | 28/28 | 0/2 | CLI+함수 |
| `shot_scale` | 9 | 29/29 | 2/2 | CLI+함수 |
| `silhouette_proportion` | 94 | 387/387 | 1/2 | CLI+함수 |
| `situation_context` | 128 | 543/543 | 2/2 | CLI+함수 |
| `skin_condition` | 11 | 25/25 | 1/2 | 함수 |
| `skin_finish` | 40 | 135/135 | 1/2 | 함수 |
| `social_cue` | 14 | 43/43 | 0/2 | 함수 |
| `space_condition` | 37 | 158/158 | 2/2 | CLI+함수 |
| `species_marker` | 26 | 54/54 | 1/2 | CLI+함수 |
| `subject` | 690 | 2315/2315 | 1/2 | CLI+함수 |
| `subject_framing` | 58 | 233/233 | 1/2 | CLI+함수 |
| `surface_material` | 519 | 1811/1811 | 0/2 | CLI+함수 |
| `surreal_anchor` | 28 | 66/66 | 0/2 | CLI+함수 |
| `surreal_concept` | 38 | 114/114 | 0/2 | CLI+함수 |
| `surreal_physics_detail` | 70 | 209/209 | 0/2 | CLI+함수 |
| `texture` | 214 | 631/631 | 1/2 | CLI+함수 |
| `time_of_day` | 20 | 88/88 | 0/2 | CLI+함수 |
| `transition_stage` | 10 | 30/30 | 1/2 | CLI+함수 |
| `viewer_position` | 19 | 43/43 | 1/2 | 함수 |
| `wardrobe_style` | 397 | 1463/1463 | 2/2 | CLI+함수 |
| `wearable_accessory` | 375 | 1197/1197 | 1/2 | CLI+함수 |
| `weather` | 59 | 230/230 | 1/2 | CLI+함수 |
| `world` | 104 | 320/320 | 1/2 | CLI+함수 |

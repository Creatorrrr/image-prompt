# 시각 의미·후보 데이터 반영 계획

2026-10-07 · 연구 결과의 적용 설계 · 운영 반영은 아직 실행하지 않음

[연구 보고서](/Users/chasoik/Projects/image-prompt/docs/analysis/2026-10-07-prompt-keyword-enrichment-research.md)의 40개 제안 중 **P0 16개부터 작은 배치로 반영한다.** 동일 의미는 기존 원본에 보강하고, 다른 owner·action·material·relation은 별도 후보로 작성한다. 480개 표현을 새 엔트리 480개로 바꾸거나, 40개 제안을 새 hard profile 40개로 만드는 목표를 두지 않는다.

## 1. 실제로 달라져야 할 결과

자연스러운 한국어·영어 요청에서 기존 의미가 더 잘 발견되어야 한다. 선택된 후보는 현재 장면의 대상·속성·관계를 구체적으로 도와야 하고, 새로운 물건·상대·의상·날씨가 좁은 변경 범위에 숨어 들어가면 안 된다. 의도한 시각 의미가 프롬프트에 실현되고 원본 크기의 그림에서도 읽히는지 확인한 다음, 사용자에게 더 좋은 작품인지 별도로 비교한다.

| 결과 | 판정 자료 | 완료 조건 |
|---|---|---|
| 의미 접근 개선 | frozen-core 기반 검색·exposure 기록 | 동등 의미 gold set에서 개선, 인접 다른 뜻의 채택 감소 |
| 의미 권위 보존 | exact/optional/opt-in 계약 | 잘못된 hard activation 0, requester definition 우선 |
| 범위 보존 | property/owner locks와 composition audit | 잠긴 대상·속성 변경 0 |
| 원본·파생물 일치 | source manifest와 양쪽 index hash | stale/누락/중복 없이 최신 원본에 바인딩 |
| 이미지 충실도 | literal evidence + strict native review | 해당 arm의 모든 유효 hard gate 통과 |
| 작품의 유용성 | 블라인드 비교와 사용자 판단 | 요청 의도를 보존한 개선인지 별도 확인 |

“노출 개수”, “선택 개수”, “프롬프트 길이”는 목표 점수가 아니다. 선택하지 않은 후보도 유효한 결과다.

## 2. 작업 순서와 의존 관계

| 단계 | 입력 | 구체적 작업 | 산출물 | 다음 단계 조건 |
|---|---|---|---|---|
| A. 기준 고정 | 최신 작업 트리·기존 연구 | 진행 중 변경과 동일 의미를 다시 비교, 원본/코드/정책 해시·바이트 보관 | before-source snapshot, 영향 ID 목록 | 이전 변경 보존·연구 기준 명확 |
| B. P0 의미 심사 | 16개 제안 카드 | owner·component·relation·effect·반례·기존 동등성 판정 | reviewed-reflection ledger | 자동 어휘 이웃을 동의어로 승격하지 않음 |
| C. 원본 작성 | 승인된 반영 범위의 ledger | 기존 보강·선택형 번들·필요한 새 원자/프로필 작성 | 작은 authored source diff | 구조·의미·범위 검사 통과 |
| D. 파생물 재생성 | 변경된 authored sources | 양쪽 BM25F와 필요 벡터/index 재생성 | 인덱스·runtime publication snapshot | 완전한 최신 hash binding |
| E. 검색·합성 검증 | 고정 요청·core·gold set | 실제 resolver/pack/audit와 인접 반례·lock 검사 | before/after exposure·prompt evidence | 잘못된 hard activation·lock 변경 0 |
| F. native 비교 | 의미 검증을 통과한 일부 문법 | 고정 입력 arm 비교, 원본 크기 리뷰·선호 비교 | runtime ledger·images·review | 이미지 충실도와 미감 판단을 분리해 기록 |
| G. P1 확장 | P0 결과·새 실패 유형 | 나머지 22개를 중복·범위·효과 기준으로 재평가 | 두 번째 scoped diff와 검증 | 고정 데이터 수 대신 근거로 확대 |
| H. 매체 확장 | G39·G40와 실제 출력 요구 | 종이 작품 촬영/순수 일러스트 경로 결정 | 별도 medium contract와 데이터 | photo 경계와의 충돌 없음 |

단계 A에서는 연구 중 바뀐 캐릭터 그래프와 실행 코드도 읽는다. intentional/involuntary affect 축이 advisory로 정리된 변경을 새 필수 조건으로 되돌리지 않는다. 병행 작업이 있는 primary checkout에서 전체 원본이나 생성된 인덱스를 덮어쓰는 구현을 하지 않는다. 구현을 시작할 때 적합한 기존 작업 트리를 확인하고, 필요하면 별도 clean worktree에서 작은 diff를 만든다. 이번 연구는 worktree 생성·운영 데이터 수정·commit/push를 수행하지 않았다.

## 3. 첫 배치 16개의 구체적 반영

| 제안 | 먼저 읽을 원본 | 적용안 | 대표 반례 |
|---|---|---|---|
| G11 지지 다리 | pose vocabulary + 기존 contrapposto | 단순 지지 동등 표현을 보강, 전신 변형은 별도 유지 | 모든 지지를 특정 전신 자세로 확대 |
| G16 넓은 여백 | subject_field_negative_space_relation | 자연스러운 배경 여백 표현·구도 조건 보강 | 신체 내부 틈으로 오인 |
| G17 한 강조점 | color_relations·palette_applications | 강조색 owner·범위·다중 accent 반례 보강 | 붉은 물건/빛을 함께 늘림 |
| G18 공동 가독성 | realistic_background·portrait_composition | 얼굴·손·장소를 읽히게 하는 조건부 focus 번들 검토 | shallow DOF가 필수 접촉을 지움 |
| G05 태도와 반응 | expression·intent_state·character mechanism graph | 형식적 태도와 국소 반응의 맥락·관계 보강 | 옆눈질만으로 archetype 강제 |
| G07 웃음 이완 | candid_laugh·acting_expression | 같은 actor의 눈/입 상태가 다른 소규모 관계 trial | 단순 명상·졸음을 같은 뜻으로 처리 |
| G09 카메라 관계 | companion viewpoint·viewer_position | 기존 카메라 위치와 current task의 동등 표현 보강 | 실제 친구/호감 사실 추론 |
| G13 연필 접촉 | intellectual_activity·tool contact phase | 손-연필-지지된 종이-국소 선 관계 trial | pencil brows·page hold와 혼동 |
| G14 가방 놓기 | postcontact phase·pose vocabulary | 손의 release와 가방의 새 지지/경로 관계 trial | 소품 부유·관절 단절 |
| G02 장르 운반체 | ethereal_gothic_scene·worldbuilding | 기존 건축/풍경에 두 장르를 배정하는 선택형 관계 | 장르 라벨로 임의 장식 증식 |
| G03 장소와 의상 대비 | everyday/realistic location·wardrobe | 두 기존 운반체의 대비와 공통 조명 | light-only 후보가 의상/장소 변경 |
| G23 플래시+실내광 | lighting·capture context | flash receiver와 warm ambient receiver 관계 | 다중 스튜디오광 자동 추가 |
| G24 광학 층 | editing_effects·photo_era·lens_artifact | bloom/halation/condensation/fog의 경계 심사 | 원인이 다른 흔적을 동의어로 합침 |
| G28 재료 대비 | textile_surface·photorealism·palette_applications | 두 재료 owner의 공통 빛 반응 관계 번들 | 모든 표면을 같은 광택으로 처리 |
| G34 물 접촉 | water_relations·contact point | 접촉점/수면/국소 반응의 owner 관계 trial | 일반 하천·초현실 음성 잔물결과 혼동 |
| G37 선→실→입체 | imaginal transition·paper artifact surface | 원상태·중간 재료·결과의 연속 경계 trial | 그림 옆 소품 배치·경계 소실 |

이 목록은 새 데이터를 작성하라는 할당량이 아니다. 실제 기존 의미가 충분하면 동등 표현과 검증만 보강한다. 기존 원본의 effects와 새 문법의 전체 effects가 다르면 긴 문장을 paraphrase에 밀어 넣지 않는다.

### 반영 원본의 선택 규칙

1. 원본 후보와 의미·owner·전제·전체 효과가 같으면 기존 ID를 유지한다. 기존 파일 또는 reviewed equivalent context extension에 한국어·영어 paraphrase를 추가한다.
2. 기존 원자 여러 개의 연결이 새 의미를 만든다면 선택형 번들로 작성한다. 모든 member가 같은 frozen context와 property locks에서 함께 가능한지 확인한다.
3. 원자 자체가 다른 경우에만 새 후보를 만든다. G29 faille는 섬유·직조·색·실루엣을 분리한 재료 후보의 예다.
4. 별도 시각 duty가 필요할 때만 새 프로필을 만든다. 모호한 미감 라벨에는 새 hard alias를 만들지 않는다.
5. 원본 예시 문장을 runtime source로 복사하지 않는다. 24개 recipe는 관계 역할의 검토 재료이며 인물·소품·팔레트가 고정된 자동 preset이 아니다.

새 cross-domain 원본이 필요한 경우의 파일명 후보는 `photo_prompt_visual_grammar_extension.json`과 `photo_prompt_visual_obligations_visual_grammar.json`이다. 파일을 생성할 때만 source manifest에 정확히 등록한다. 의미의 소유자가 기존 도메인에 있으면 해당 원본에 유지하며, 새 파일에 이중 정의를 만들지 않는다. 파일명은 구현 시 검토할 제안이다.

출처 URL·연구 판단·라이브러리 ID·효과의 미검증 상태는 docs/research-evidence의 ledger에 유지한다. runtime positive fields에는 화면에서 읽을 수 있는 의미를 넣고, counterexample·claim limit·contextual_usage·출처 설명을 긍정 검색 증거로 사용하지 않는다.

## 4. 후보·시각 프로필·후보팩의 변경 구분

| 층 | 작성하는 것 | 작성하지 않는 것 |
|---|---|---|
| 후보 원본 | 구체적인 concept_units, directed relations, ownership, affected dimensions/properties, 적용 전제 | 추상 미감 수식어를 무조건 필수 의미로 변환 |
| 시각 의미 원본 | definition·paraphrase·혼동 경계·authored components·증거 및 pixel duty | 검색 유사도나 인기 점수에 의한 hard activation |
| 검색 인덱스 | 현재 원본과 정책에서 파생된 BM25F·벡터·hash manifest | 충돌한 generated JSON의 수작업 합치기 |
| 요청별 후보팩 | frozen core/request로부터의 새 exposure와 opt-in 계약 | 과거 pack 수동 편집이나 결과물의 원본화 |
| 작성·픽셀 리뷰 | 선택된 관계의 literal evidence와 strict native gate | 출처 링크·형용사 개수를 의미 충족으로 계산 |

일반 후보나 번들에 연관 profile ID가 있어도 profile은 자동으로 켜지지 않는다. 실제 requester duty 또는 독립적인 opt-in 선택이 있어야 한다. 후보의 의미와 profile의 전체 hard 의미가 다르면 연관 ID도 단순 참고로 취급한다.

단순 `closed lips`에 `lip pressing` duty를, 일반 `negative space`에 body-bounded duty를, `miniature-looking`에 실제 축소 크기 duty를 추가하지 않는다. 이런 경계는 잘못된 hard activation 0 기준의 핵심이다.

## 5. 검색과 합성 검증 설계

### 검증 수량은 실행 계획이며 완료 실적이 아니다

전체 40개 문법마다 10개 사례를 설계해 **400개 목표 사례**를 만든다. 첫 P0 16개는 160개, 이후 photo 관련 P1 22개는 220개, P2 매체 경로는 20개다. 현재 상세 카드에는 문법마다 독립적으로 작성한 긍정 요청 예와 혼동 반례가 있고, 나머지 사례를 아래 기준으로 확장한다.

| 문법당 사례 | 개수 | 의도 |
|---|---:|---|
| 자연스러운 한국어 긍정 요청 | 2 | profile 라벨을 복사하지 않는 표현 |
| 자연스러운 영어 긍정 요청 | 2 | 언어와 문장 변화 |
| 인접한 다른 뜻 | 2 | 역할·owner·재료·관계가 다른 가까운 의미 |
| 부정·대조 문장 | 1 | “그 의미는 원하지 않는다”가 activation이 되지 않음 |
| property/owner 잠금 또는 전제 미충족 | 2 | 부분적 변경 허용과 전체 effects의 불일치 |
| 매체·비인간·가림/크롭 경계 | 1 | 범위에 맞는 선택 또는 정상적인 rejection |

케이스는 연구자가 만든 evaluation fixture라고 표시한다. 실제 사용자가 제출한 요청이나 그 만족도 평가로 표시하지 않는다. 개발용 6개와 고정 holdout 4개를 나눠 데이터 편집 전에 hash를 고정한다. 원문의 긴 구절을 그대로 exact alias와 holdout 양쪽에 넣지 않는다. 실제 요청 사례를 추후 넣을 때도 의미와 개인정보 범위를 따로 검토한다.

현재의 대조표에 나온 BM25F 어휘 이웃을 gold 정답으로 삼지 않는다. gold는 해당 요청과 독립적으로 작성된 core의 의미·scope를 검토하여, 받아들일 수 있는 후보/프로필과 반드시 거절할 인접 의미를 별도로 지정한다. 후보 전부를 거절하는 올바른 사례도 포함한다.

### 검증은 실제 워크플로를 따른다

비교용 기본 장면은 프로젝트 후보 데이터·이 연구 문서·이전 pack을 읽지 않는 새 authoring context에서 요청, 일반 지식, 허용 neutral catalog와 creative controls로 작성한다. 먼저 freeze하고, 동일 envelope/core/controls를 현재 데이터 A와 보강 데이터 B에 전달한다. 연구 문서의 내용이 pre-core baseline에 이미 섞인 경우에는 독립 작성 증거로 인정하지 않는다.

실제 resolver에서 exact 의미, optional discovery, context eligibility, exposed inventory를 기록한다. 최종 선택·거절의 이유, literal evidence, 관계 endpoint, 전체 effects도 별도로 기록한다. 현재 code의 candidate cap을 임의로 늘리지 않고, 동일 cap에서 다양성과 의미 접근을 비교한다.

영어 구절의 어휘 hit뿐 아니라 한국어 요청 → 독립 baseline → 실제 optional/exact 검색 → pack exposure를 검증한다. embedding-only paraphrase 사례는 실제 질의 벡터 경로로 별도 실행하며, 지금의 offline BM25F 진단이 그 검증을 대신하지 않는다.

### 기록할 측정값

- 허용 gold 후보의 Recall@현행 cap과 잘못된 이웃의 노출/선택 비율.
- wrong hard activation, requester definition 위반, owner/property lock drift의 사례 수.
- 동등 문장에 따른 exact/optional 계약의 안정성.
- 선택된 후보의 concept_units·relation evidence·literal evidence 완전성.
- 최종 prompt conformance와 실제 runtime bytes의 binding.
- 그림의 owner·접촉·속성·count·국소 texture fidelity.
- 원문의 요청 전달, 초점 위계, 재료 차이, 자연스러운 순간에 대한 블라인드 비교와 사용자 선호.

0건 오류는 이 고정 사례 안에서의 결과다. 모든 요청에서의 완전성을 주장하지 않는다. Recall@cap에는 전제와 scope가 실제로 충족되는 gold만 포함한다. 단순 노출 증가를 선택 품질이나 미감 개선으로 해석하지 않는다.

## 6. 인덱스와 코드 검증

이번은 원본 데이터 중심의 변경으로 설계한다. 새 의미를 Python의 하드코딩 예문으로 추가하지 않는다. 기존 계약으로 표현할 수 없는 문제가 구체적으로 재현될 때만 코드 변경을 별도 diff로 검토한다.

후보 labels·aliases·paraphrases·concept units·relations·embedding text를 바꾸면 semantic index의 원본 hash와 BM25F를 다시 작성한다. visual profile을 바꾸면 visual profile index의 registry hash·positive text·BM25F를 다시 작성한다. source manifest 등록도 함께 검증한다.

기존 벡터는 key, 전체 input text, provider, model, dimensions가 실제로 같은 경우에만 재사용한다. 새롭거나 달라진 텍스트는 현행 계약대로 batch size 1로 임베딩한다. “짧은 표현 몇 개만 추가”해도 embedding input 전체가 달라질 수 있으므로 zero API call을 미리 보장하지 않는다. 원본 텍스트에서 계산한 필요 건수와 예상 비용을 기록한 뒤 실행 범위를 결정한다.

아래 명령은 **구현 이후의 검증 메뉴**다. 이번 연구에서 실행한 production 테스트나 인덱스 갱신을 뜻하지 않는다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
.venv/bin/python -m unittest tests.test_photo_candidate_semantics tests.test_photo_positive_retrieval tests.test_photo_bm25f_retrieval tests.test_photo_core_retrieval tests.test_photo_visual_profile_retrieval tests.test_photo_visual_obligations
.venv/bin/python -m unittest tests.test_photo_authorial_core_v6 tests.test_photo_authorial_direction_scope
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --dry-run
```

실제 candidate/profile 원본이 바뀐 배치만 각각의 인덱스를 재생성한다. 테스트는 바뀐 도메인에 맞춰 acting expression, portrait composition, color relations, palette applications, textile effect scope 등을 추가한다. 의도치 않은 넓은 위험이나 여러 독립 route가 바뀐 경우에만 전체 suite로 확장한다.

```bash
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --batch-size 1 --keep-stale-generations --progress
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
```

위 재생성 명령은 새 의미 텍스트가 있으면 API를 사용한다. 별도 작업 트리의 출력에서 양쪽 freshness와 runtime publication binding을 확인하고 적용한다. 원본 간 충돌은 identity로 해결하며 generated index는 합쳐진 원본에서 다시 만든다. 현재 primary의 dirty source와 관계없는 untracked shard를 이 작업에 섞지 않는다.

## 7. native 이미지 비교의 단계

먼저 검색·scope·prompt 검증에서 문제가 없는 문법을 고른다. 초기 pilot은 4개 장면군 × 현재/보강 2개 arm × 4회 표본 = **32장 제안**이다. 예시는 웃음 이완, 공동 가독성, 재질 대비, 그림-실 경계다. 비용과 실행 요청을 확정한 뒤 수행하는 후속 단계이며 이번에 이미지를 만들지 않았다.

pilot이 문제를 좁히면 8개 장면군 × 기존/동등 표현 보강/관계 보강 3개 arm × 4회 표본 = **96장 설계**로 확장할 수 있다. 앞 pilot과 똑같은 입력·모델·설정인 arm은 재사용 여부를 기록한다. 32+96장을 무조건 생성한다는 계획이 아니다.

모델·버전·aspect ratio·해상도·creative controls·참조 사용 범위·runtime prompt bytes를 고정한다. API가 seed를 지원하는 경우에만 같은 seed로 paired comparison을 한다. seed가 없으면 같은 seed라고 주장하지 않고 반복 표본을 무작위 순서로 비교한다. 후보 결과 중 좋은 그림 하나만 골라 전체 개선의 증거로 제시하지 않는다.

원본 크기에서 물성·작은 접촉·모근·중간 경계를 보고, thumbnail에서 전체 위계·실루엣·accent 위치를 본다. hard duty가 가려졌거나 일부만 보이면 통과시키지 않는다. 요청된 가림 자체를 없애고 통과율을 올리지도 않는다. 의미가 보존되지 않은 결과의 높은 선호 점수를 보강 성공으로 처리하지 않는다.

TIFA/DSG식의 원자 질문을 참고하되 native review의 authority를 평가 모델 하나에 맡기지 않는다. 예를 들어 G37은 “종이 위 평면 선이 있는가”, “입체 실이 있는가”, “둘이 같은 경계에서 이어지는가”, “그 실이 요청한 결과 형태와 연결되는가”를 나누고 존재 질문에 관계 질문이 의존하게 한다. 대상이 없으면 그 대상의 속성만 맞다고 답해 평균점수를 높이지 않는다. [TIFA](https://arxiv.org/abs/2303.11897), [DSG](https://google.github.io/dsg/)

시각적 충실도와 “더 마음에 드는가”를 다른 질문으로 평가한다. HPS 같은 점수는 보조 참고만 가능하며 requesting-user judgment를 대체하지 않는다. [HPS v2](https://arxiv.org/abs/2306.09341) 작은 pilot 표본의 우세는 탐색 결과로 표시한다. 확증이 필요하면 장면군/요청 단위의 변동성과 effect size를 보고 표본수를 설계한다.

## 8. P1과 매체 경로의 확대 조건

P1 22개는 P0의 새 실패를 해결하거나 독립적인 재사용 가치가 있을 때 확대한다. 같은 문장 구조를 팔레트·원단 이름만 바꿔 대량 복제하지 않는다. 동등 표현은 기존 ID에, 새 관계는 번들에, 별도 원자는 정확한 effect와 prerequisites가 있는 새 후보에 둔다.

G39·G40의 공유 원리는 photo composition에도 활용할 수 있지만, 붓질·워시·선 처리 자체는 illustration 의미다. 기존 `pe_watercolor_print`·`pe_pencil_print`는 사진 속 종이 작품을 표현하는 경우에만 사용한다. 순수 수채/2D가 요청 결과라면 해당 medium을 보존하는 별도 경로의 계약부터 정한다. photographic skin, DSLR, lens-grain 기본값을 그 경로에 자동 상속하지 않는다.

## 9. 반영 작업의 최종 전달물

각 배치는 changed source IDs, 원본 diff, 출처-의미-후보 매핑 ledger, 갱신 index hash, 검증된 실제 pack/exposure, 선택·거절·literal evidence, runtime binding을 함께 전달한다. 이미지 비교까지 실행한 배치는 원본 이미지와 strict native review, 통과·실패·미관측 상태와 사용자 판단도 포함한다.

실제 선택률·미감 효과·생성 성공률이 미측정인 항목을 “검증 완료”로 표시하지 않는다. 특정 데이터가 semantic correctness를 갖춘 상태와 대표 작품으로 승격된 상태를 구별한다. 연구·계획 단계의 완료는 운영 배포나 PR 생성의 완료를 의미하지 않는다.

이번 전달물의 상태는 다음과 같다: 연구 원본과 대조표·40개 카드·반영 계획 작성 완료, 참조 ID와 출처 연결 검사 완료, production source/index 변경 및 이미지 비교 미실행.


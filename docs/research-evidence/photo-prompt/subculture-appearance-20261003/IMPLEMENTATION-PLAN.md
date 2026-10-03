# 시각 의미 데이터·후보팩 반영 계획

작성일: 2026-10-03 · 이 문서는 반영안이며 운영 반영은 수행하지 않았다.

## 목표와 완료 조건

171개 원 용어의 의미를 **정확한 부품·기점·소유자·비율·가림·재질 관계**로 검색하고, 요청한 core와 잠금을 보존한 후보만 제안할 수 있게 한다. 넓은 팬 용어나 캐릭터 조합의 색·성별·나이·몸·의상·행동을 다른 요청에 강제하는 경로는 만들지 않는다.

완료는 새 alias 수나 profile 수로 판단하지 않는다. 다음 결과가 각각 증명돼야 한다.

1. authored 단위와 실제 owner/target/property가 연결되고 기존 의미와 중복·충돌하지 않는다.
2. exact 문맥과 유사 검색의 권한 차이가 유지되며 부정·반례·다른 소유자에서 hard 의무가 새로 생기지 않는다.
3. open dimension뿐 아니라 각 property 잠금과 exclusion을 지키며, 하나의 전체 후보팩에서 서로 호환되는 후보만 남는다.
4. 선택된 관계가 composition/evidence/render gate까지 연결되고 부분 대체·가림을 PASS로 처리하지 않는다.
5. 실제 이미지에서 선택한 관계의 필수 요소가 관찰된다. 사용자 선호·수용은 별도 기록한다.

이번 연구 데이터의 `runtime_eligible_now`는 모두 false다. 앞으로 채택할 수 있는 새 profile 수는 기존 owner 검토·실험 결과 후 결정하며 187개 초안을 전부 새 runtime 항목으로 만드는 것이 목표가 아니다.

## 0단계 — 최신 운영 상태와 기준점 고정

- 기준본 `900848816f88a494e5bf16ea475a25074d584911`의 registry 1,510개·후보 항목 9,703개를 참고하되, 적용 시작 시 최신 checkout의 diff·HEAD·loader·두 index의 hash를 다시 읽는다.
- 작업 중 다른 데이터 반영이 진행됐으므로 [LIVE-DRIFT-RECEIPT](LIVE-DRIFT-RECEIPT.json)의 오류를 최신 상태라고 고정하지 않는다. 최신 loader 실패 또는 stale hash가 남아 있으면 authored 작업과 파생 인덱스 작업을 먼저 정리한 뒤 해당 배치를 검증한다.
- unrelated 작업을 유지하고, 필요한 격리 checkout은 현재 작업 상태와 사용자 의도에 맞춰 선택한다. 본 연구가 타 작업의 conflict·부분 index를 덮어쓰는 복구 근거가 되지는 않는다.
- 적용 대상 파일과 원본 hash, 새로 바뀔 의미·ID, 허용된 변경 범위를 배치 영수증에 남긴다.

**통과 조건:** 현재 runtime 로드·index 메타데이터 확인과 기준본 대비 새 owner diff가 설명 가능함. 연구 스냅샷의 PASS를 최신 runtime PASS로 재사용하지 않음.

## 1단계 — 의미 중복과 alias 권한 검토

[OWNER-MAP](OWNER-MAP.json)의 비교표를 출발점으로 실제 profile definition, component groups, owner scope, affected properties, reject substitutes, evidence/render 의무를 함께 읽는다.

| 사례 | 우선 조치 | 동의어로 합치면 안 되는 범위 |
|---|---|---|
| H03 히메컷 | 기존 `hime_cut_structural`과 `hair_style.hime_cut`에 동등한 KO/EN 문맥만 보강 | 모든 앞머리·직모·검정색·일반 레이어 |
| H04 트윈테일 | 기존 양쪽 gather 관계 재사용 | 검은 리본 포함 특정 후보와 범용 gather의 의미 차이 |
| B03–B11·A01–A04 | 기존 부위별 morphology owner를 조합 | 키·근육·체적·비례를 한 몸 라벨로 합치기 |
| G01 분리 소매 | 기존 costume cuff의 간격 관계 검토 | 별도 소매 전체 길이·플레어·손 덮개까지 동일시 |
| A09·A10 | 기존 하부/측면 chest coverage owner 재사용 | 몸 체적·중앙 neckline·다른 위치의 노출 |
| A17·A19 | 기존 가터 연결/hem-stockings interval owner 재사용 | 독립 thigh band·허벅지 사이 배경 틈 |
| P09 바이저 | 기존 helmet visor와 sun visor를 반례로 비교 | 표시 가면·통합 인공 얼굴·햇빛 가리개 전체를 하나의 alias로 합치기 |

원 대화의 `／`나 `·`는 곧 의미 동등성을 보증하지 않는다. wolf cut/shag, pompadour/regent, small/flat bust, yaeba/fang, petticoat/historical pannier, fur/feather, SD의 두 용법은 분리한다. 메카쿠레·지토메·중성적·고딕·메카무스메 같은 상위 용어는 정확한 scope가 확정될 때까지 해석 맥락/advisory로 둔다.

동등한 항목에만 `existing_slot_context_extensions`를 사용한다. 다른 기관·부착 대상·행동·property 효과가 필요한 경우 새 관계 단위로 둔다. 기존 ID·owner·guard를 보존한다. 출처의 인상·성격·판매 문구·역사 설명·반례 텍스트를 긍정 alias/lookup field로 복사하지 않는다.

**통과 조건:** 각 변경에 `REUSE_EQUIVALENT / SPLIT_RELATION / CONTEXT_ONLY / HOLD` 중 하나와 근거가 있고, 같은 owner의 충돌 후보·중복 exact trigger가 설명됨.

## 2단계 — 작고 검토 가능한 authored 배치

첫 3개 배치는 실패가 명확히 보이는 기점/가림/부착 관계부터 시작한다. 각 배치 8개 이하의 **검토 단위**이며, 결과에 따라 기존 항목 확장으로 끝날 수도 있다. 실제 profile 수를 미리 확정하지 않는다.

| 순서 | 검토할 단위 | 우선 이유 | 직접 증거/반례 |
|---|---|---|---|
| 1 | H01·H02·H05·H06·H13·H14·X10·X03 | 머리 수·나선·별도 리본·눈 가림이 명확히 다름 | 테토 삼면도, 포니드릴 공식 용례, R01–R06 |
| 2 | F01·F02·F04·F05·F08·F13·X01·X04 | 눈 영역/치열/장식 귀를 성격·다른 부위와 분리 | 사전·눈 영역 자료·R08–R15·R21 |
| 3 | G01·G04·G08·G14·G18·G20·A17·A19 | 옷의 연결·지지·edge 관계를 기존 owner로 보강 | 미쿠 의상·제조사 제품 구성·R30–R35 |

다음 배치는 body 독립축 재사용, N08·N11–N12·N22, 신체/장비 분리 X02·X07·X11–X13 순으로 검토한다. 인외 body 전환, 소품 조립, 자유 부유, 손상·공포 항목은 아래 scope 보류를 먼저 해결한다. 넓은 복식 19개는 이 부품들이 안정된 뒤 조건부 맥락을 보강한다.

배치별 작성 항목은 KO/EN 관찰 문장, positive concept unit, 소유자+연결/가림/비교 관계, 실제 dimension과 target/property, 직접 관찰 가능 부위, 반례, exact 활성화 범위, 선택 시 evidence/render gate, 출처/유지보수 근거다. 추상적 shape/mood 라벨만 가진 항목은 discovery 대상으로 올리지 않는다.

### 파일 배치

- 기존 머리 의미는 `photo_prompt_tags.json`, `photo_prompt_visual_obligations.json`의 기존 owner를 보존한다. 해당 소유자의 실제 위치는 최신 checkout에서 다시 찾는다.
- 몸 비율/기관 연결은 `photo_prompt_body_morphology_extension.json`과 `photo_prompt_visual_obligations_body_morphology.json`에 있는 owner부터 검토한다.
- 기존 옷/속층/여밈 관계는 clothing structure·costume cosplay extension/obligations, 귀 장식·가면은 accessory structure, 표면 효과는 textile surface의 owner와 비교한다.
- 동등하지 않은 새 외형 관계를 모을 경우 `photo_prompt_subculture_appearance_extension.json`과 `photo_prompt_visual_obligations_subculture_appearance.json`을 **새 authored 파일명 제안**으로 사용한다. 일반 extension loader의 등록만 필요하며 용어별 generator 분기를 추가하지 않는다.
- `photo_prompt_subculture_extension.json`의 제작 활동·커뮤니티·행사 자료는 해당 소유 범위를 유지한다. 외형 리서치 때문에 전체를 코스튬 키워드 사전으로 대체하지 않는다.

### 실제 property로 번역하는 예

연구 B05의 속성 제안은 `subject.body.frame.compact_breadth`다. 검증된 기존 `bm_stocky_build`의 실제 효과는 dimension `body_geometry`, target `main_subject`, property `body.body.width_length_relation`이다. 동등하다면 기존 실제 property에 묶어야 한다. 연구용 문자열을 새 runtime property로 그대로 넣으면 잠금과 기존 owner 비교를 우회할 수 있다.

새 머리 나선은 appearance dimension 안에서 의미를 표현할 수 있어도 실제 hair owner/property namespace가 결정돼야 한다. 새 귀 기관/사이보그/사지 전환은 기존 species와 subject를 바꾸는 효과가 있는지 별도로 검토한다. ‘표면 재질’이라는 carrier 이름만으로 몸 geometry 변경을 숨기지 않는다.

**통과 조건:** 새 후보의 실제 `affected_dimensions`, `affected_properties` 객체, core target, `concept_units` 및 관계가 validator를 통과하고 같은 property의 잠금을 시험함. research JSON의 복사로 완료 처리하지 않음.

## 3단계 — 보류한 범위의 해결 또는 유지

현재 초안 기준 보류는 33개다. 이 수치는 검토 결과에 따라 달라질 수 있다.

| 범위 | 수 | 처리 계획 |
|---|---:|---|
| `prop`, `aftermath_trace`의 empty scope | 10 | 후보 채택 보류 유지. 소품/손상의 target/property를 검토하는 별도 정책안이 선행돼야 함. `scale_relation`·`surface_material`로 우회하지 않음. |
| 하나의 슬롯 범위를 넘는 dimension | 22 | 몸/종/subject/매체/자유 부유 효과를 분해하고 core에서 이미 고정된 상태와 추가 변경을 구분. 분해할 수 없는 복합 효과는 별도 scope 정책 검토 전 보류. |
| B12 중성적이라는 라벨 | 1 | 실제 어깨·허리·골반 관계가 명시된 뒤 기존 owner 사용. 정체성 추론을 위한 후보로 만들지 않음. |

Protogen 종족 규칙, BRS/ENA/키트 정확 버전, 일부 팬/라이선스 사례도 해당 canonical 연결을 보류한다. generic 표시 패널·기관 부착 같은 연구 해석은 별도로 관찰/검증할 수 있으나 canonical 종족 규칙의 검증을 대신하지 않는다.

**통과 조건:** 해결한 보류에 실제 dimension/target/property 정책과 lock 테스트가 있음. 해결되지 않은 초안의 자동 채택률은 0이며 연구 metadata로 남을 수 있음.

## 4단계 — 검색·인덱스 재생성

사전/alias/positive concept/relation/embedding text가 바뀌면 dictionary semantic index를 재생성한다. registry가 바뀌면 visual-profile index도 재생성한다. 파생 index와 shard를 수동으로 의미 편집하지 않는다. 병합은 authored owner에서 해결하고, 동일한 입력 텍스트·provider/model/dimensions/entry key의 벡터만 재사용한다. 새/변경 텍스트는 현재 유지보수 규약의 batch size 1로 임베딩한다.

```sh
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --batch-size 1
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_visual_profile_index.py --check
.venv/bin/python skills/photo-prompt-image-generator/scripts/build_semantic_index.py --progress
.venv/bin/python skills/photo-prompt-image-generator/scripts/validate_photo_prompt_dictionary.py
```

설정된 임베딩 공급자의 실행 조건은 해당 배치 시작 시 확인한다. 위 명령은 반영 계획이며 이번 리서치에서 실행하지 않았다.

exact term도 validated positive core scope 이후에만 의무가 될 수 있다. BM25F/embedding/RRF는 advisory다. source prose, usage context, claim limits, rejects를 label/긍정 feature로 잘못 투영하지 않는다. KO/EN 직접 서술, JA/Kana 표기, 로마자 용례를 구분하고 긴 조각 안의 우연한 substring으로 hard 활성화하지 않는다. 모에소데 관련 용어에도 `규모에`·`외모에` 같은 인접 음절 반례를 둔다.

**통과 조건:** stale hash가 없음, 동일 입력 벡터 재사용 기록이 있음, exact 문맥·유사도 문맥·substring 반례에서 권한이 유지됨.

## 5단계 — 의미 회귀와 기존 계약 검증

[REGRESSION-PROPOSALS](REGRESSION-PROPOSALS.json)의 40개 혼동 쌍과 12개 정책 시나리오를 실제 matcher/core/candidate/render fixture schema로 번역한다. 연구의 예문을 곧 exact alias로 등록하지 않는다. 먼저 별도 고정 요청과 unseen paraphrase를 만들어 일반화 여부를 비교한다. 기존 lexical/generalization holdout은 실패를 피하려고 수정하지 않는다.

배치와 직접 관련된 hair/body/costume 후보 테스트부터 실행하고, 실제 데이터 변경의 범위에 따라 유지보수 규약의 전체 unittest discovery를 마친다. 다음은 관련된 현재 파일을 기준으로 한 시작 목록이다.

```sh
.venv/bin/python -m unittest tests.test_photo_hair_visual_semantics -v
.venv/bin/python -m unittest tests.test_photo_body_morphology_semantics -v
.venv/bin/python -m unittest tests.test_photo_costume_cosplay_semantics -v
.venv/bin/python -m unittest tests.test_photo_candidate_semantics -v
.venv/bin/python -m unittest tests.test_photo_authorial_core_v6 -v
.venv/bin/python -m unittest tests.test_photo_precore_feature_selection -v
.venv/bin/python -m unittest tests.test_photo_bm25f_retrieval -v
.venv/bin/python -m unittest tests.test_photo_visual_profile_retrieval -v
.venv/bin/python -m unittest discover -s tests
```

fake-vector 계약 테스트와 실제 generated index 테스트를 구분한다. 통과 수 외에 변경된 의미, owner swap, negation, exclusion, cross-carrier property lock, component 선택에서 gate까지의 연결을 검토한다. 단순 문자열 probe를 의미 회귀의 PASS로 사용하지 않는다.

**통과 조건:** 잠금·excluded feature·잘못된 owner로 의무/채택이 새는 경우 0, 선택된 구성요소의 gate 누락 0. 일반화·positive recall은 배치 이전 기준과 비교하고 분모/실패 ID를 남긴다.

## 6단계 — 고정 core의 후보팩 비교

[PACK-CONTEXT-PROPOSALS](PACK-CONTEXT-PROPOSALS.json)의 8개 맥락은 runtime pack이 아니라 검증 요청 제안이다. 별도로 요청을 작성하고 후보 자료를 보기 전 initial core를 만든 뒤 freeze/hash를 고정한다. 이후 한 외부 후보팩을 조회하고 요청 근거·open dimension·target/property 잠금·exclusion·전체 pack 호환성을 검토한다. 리서치 사전으로 core를 선작성하거나 후보가 채택되도록 core 문장을 고치지 않는다.

현재 기준 정책은 discovery **총 후보 최대 15**, assertion당 최대 3, 공유 content word 최소 3이다. bundle은 최대 8개, bundle당 member 최대 8이다. 이 수치를 ‘assertion을 최대 15개 추가한다’로 오해하지 않는다. 실제 pack에서 후보/owner 중복 제거와 self-contained guard를 유지한다. 창의적으로 변형한 후보도 소수로 제한되고 권한이 높아지지 않는다.

비교표에는 요청·고정 core hash·기존/신규 pack·노출된 후보 ID·의미 근거·거절 이유·채택 후 달라진 property·evidence/render gate를 남긴다. 연구 187개 전체를 동시에 주입하지 않는다. 후보를 모두 거절한 결과도 올바른 결과다.

**통과 조건:** body·wardrobe·material·species·style의 잠금 위반 0, 명칭만으로 맥락 전체를 흡수한 채택 0, 중복/충돌 owner 채택 0. 노출·선택·prompt audit을 픽셀 성공으로 부르지 않음.

## 7단계 — 실제 픽셀 qualification과 수용

운영 후보로 옮긴 작은 배치에서 실제 이미지 생성 검증을 별도로 수행한다. 요청하지 않은 이미지 생성은 이번 연구에 포함하지 않았다.

우선 테스트 장면은 (1) 트윈 드릴/별도 리본, (2) 한눈/양눈 가림, (3) 눈꼬리/눈꺼풀/삼백안, (4) 기호 눈 영역, (5) 귀 기관/머리띠, (6) 뿔/투구, (7) 지행형 지지, (8) 인공 신체/장갑/소켓, (9) 분리 소매, (10) 속치마/골반, (11) 가터/노출띠, (12) 실제 망사/인쇄무늬다. 검증 가능한 프레임을 선택하고 어려운 모든 관계를 한 이미지에 몰아넣지 않는다.

각 결과는 원본 요청, core hash, 후보 선택 근거, prompt/negative bytes와 hash, 도구/모델/참조, attempt, 저장 artifact, native scale 판정, 사용자 판정을 분리해 보존한다. 실제 캐릭터 복제가 필요한 요청이 아니라면 연구 provenance의 이름·전체 팔레트를 생성 prompt에 넣지 않는다.

- 선택된 관계의 **모든** 필수 component+owner가 관찰되면 PASS.
- 하나라도 구조가 다르거나 다른 부품으로 대체되면 FAIL (`partial_is_fail`).
- 가림/해상도/프레임 때문에 필수 관계를 판정할 수 없으면 UNOBSERVABLE, PASS 계산에 포함하지 않음.
- 도구가 generation을 막으면 `moderation_blocked` attempt이며 이미지 품질 결과가 없음.
- 기술적 픽셀 PASS 뒤에도 사용자 수용 여부는 별도다.

프레임 변경으로 숨겨진 관계를 보이게 했을 때는 core 의도와 잠금을 유지해야 한다. 통과할 때까지 평가 기준이나 holdout을 느슨하게 바꾸지 않는다.

## 배치 영수증과 회수 방법

각 배치는 authored 파일/ID·이전/이후 hash·왜 재사용/분리했는지·새 색/기관/행동 효과 여부·인덱스 재생성 기록·테스트 실패 ID·후보팩 비교·픽셀 결과를 함께 남긴다. 문제가 발견되면 해당 authored 배치와 연결 index만 되돌릴 수 있게 한다. 캐릭터 버전 오류나 속성 scope 오류를 전체 기존 데이터를 교체하는 이유로 사용하지 않는다.

일정 대신 위 통과 조건으로 진행한다. 지금 바로 수행 가능한 다음 작업은 **최신 owner 대조와 첫 8개 검토 단위의 authored 배치 설계**다. 데이터 반영·실제 pack·이미지 검증의 실행 상태를 각각 갱신해야 최종 완료를 판단할 수 있다.
